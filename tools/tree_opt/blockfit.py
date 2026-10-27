"""External fit for the block plan: given a tree (alloc + prism), choose the new belt's 6 lines, ring L's state, the orange
memory's lines, main-memory block rolls (last resort) and the 11 free kismets (9 micro + 2 medium; the other 2 mediums are
reserved) so that attack and spell block reach 100%, res reach the targets, and DPS is maximal. Reports ES / EHP.

Rolls [Vlad 2026-10-27]: belt/ring/fates divined to max; memory block NOT divined (T0 mid 28; the Epic trait-slot memory x0.42).
Fates: block micro 8 / medium 15, INT 15 / 30, res 7 / 14. Block ratio 30 + 25 (Defensiveness) = 55%.
"""
import sys, os, copy, itertools, math
sys.path.insert(0, os.path.dirname(__file__))
import blockplan as B
S, E = B.S, B.E

TARGET = {"fire": 60, "cold": 60, "lightning": 60, "erosion": 40}
BLOCK_RATIO = 0.55
MEM_ROLL = 28.0          # T0 random block affix, mid roll (25-31)
ORANGE_LINE = round(28 * 0.42, 1)
BOOTS_ES = 720.0         # (146 base + 304) x 1.6 local
BELT_BASE_ES = {"Magic Girdle": 80.0, "Arcanist": 110.0}

# belt pool (max rolls). (group, side, text)
BELT_P = {"dmg": ("B", "+94% damage"), "es": ("B", "+455 Max Energy Shield"), "block": ("A", "+20% Attack and Spell Block Chance"),
          "int": ("A", "+78 Intelligence"), "def": ("A", "+26% Defense"), "lowmana": ("U", "-18% additional damage taken at Low Mana")}
BELT_S = {"res": ("B", None), "eleres": ("A", "+12% Elemental Resistance"), "double": ("U", "+34% chance to deal Double Damage"),
          "cdr": ("U", "+31% Cooldown Recovery Speed"), "dur": ("U", "+31% Skill Effect Duration")}
RES_LINE = {"fire": "+35% Fire Resistance", "cold": "+35% Cold Resistance", "lightning": "+35% Lightning Resistance", "erosion": "+35% Erosion Resistance"}
MEM_CANDIDATES = [(2, "+41% Spell Critical Strike Damage"), (3, "+104% Spell Critical Strike Rating"), (1, "+47% Cold Skill Critical Strike Damage")]
ORANGE_LINES = ["+18% Spell Critical Strike Damage", "+18% Cold Skill Critical Strike Damage"]


def belt_structures():
    out = []
    for pre in itertools.combinations(BELT_P, 3):
        for suf in itertools.combinations_with_replacement(BELT_S, 3):
            if any(suf.count(x) > 1 for x in suf if x != "res"): continue
            groups = [BELT_P[x][0] for x in pre] + [BELT_S[x][0] for x in suf]
            if groups.count("B") == 2 and groups.count("A") == 2 and groups.count("U") == 2:
                out.append((pre, suf))
    return out


def es_calibration():
    """flat ES constant so the model matches Vlad's sheet (7.3k, 2026-10-27 with ring L 323 / ring R 404)."""
    b, t = E.load(); recs = E.collect(b, t)
    flat = sum(v for s, k, v, c, l in recs if k == "es.flat") - 304 + BOOTS_ES + BELT_BASE_ES["Magic Girdle"]
    pct = sum(v for s, k, v, c, l in recs if k == "es.pct" and s != "gear:boots")
    return 7300.0 / (1 + pct / 100) - flat
CAL = es_calibration()


def es_of(b, t, belt_base=BELT_BASE_ES["Arcanist"]):
    recs = E.collect(b, t)
    flat = sum(v for s, k, v, c, l in recs if k == "es.flat") - 304 + BOOTS_ES + belt_base + CAL
    pct = sum(v for s, k, v, c, l in recs if k in ("es.pct", "defense.pct") and s != "gear:boots")
    return flat * (1 + pct / 100)


def ehp(es, lowmana, blocked=True):
    hit = (1 - BLOCK_RATIO) if blocked else 1.0
    lm = 0.82 if lowmana else 1.0
    return dict(ele=es / (0.40 * hit * lm), phys=es / (hit * lm), dot=es / (0.40 * lm))


def fates(att_need, spl_need, res_def):
    """res_def: {elem: deficit}. 9 micros + 2 mediums. Returns (int_total, used) or None."""
    best = None
    res_slots = {e: d for e, d in res_def.items() if d > 0}
    for med_res in range(0, 3):
        for med_blk in range(0, 3 - med_res):
            # res: mediums (14) on the biggest deficits first, then micros (7)
            d = dict(res_slots); mr = med_res
            while mr > 0 and d:
                e = max(d, key=d.get); d[e] -= 14; mr -= 1
                if d[e] <= 0: del d[e]
            mic_res = sum(math.ceil(x / 7) for x in d.values())
            # block: mediums (15) then micros (8)
            a, s = att_need, spl_need; mb = med_blk
            for _ in range(mb):
                if a >= s: a -= 15
                else: s -= 15
            mic_blk = max(0, math.ceil(a / 8)) + max(0, math.ceil(s / 8))
            mic_left = 9 - mic_res - mic_blk
            if mic_left < 0: continue
            med_left = 2 - med_res - med_blk
            it = 15 * mic_left + 30 * med_left
            if best is None or it > best[0]:
                best = (it, dict(res_micros=mic_res, res_mediums=med_res, block_micros=mic_blk, block_mediums=med_blk, int_micros=mic_left, int_mediums=med_left))
    return best


def fit(alloc, pr, ring_modes=("asis", "block", "int78"), mem_max=2, force=None, verbose=False, ring_lines=None):
    """force: dict of belt constraints {"pre": set(...), "suf": [...]} to pin lines (for the EHP frontier)."""
    X = pr[0]
    b0, t0 = B.build(alloc, pr, gear=lambda b: None)
    recs0 = E.collect(b0, t0)
    tree = lambda key: sum(v for s, k, v, c, l in recs0 if k == key and s.startswith("tree"))
    t_att, t_spl, t_both = tree("block.attack"), tree("block.spell"), tree("block.both")
    t_res = {e: tree("res." + e) + tree("res.ele") * (e != "erosion") + tree("res.all") for e in TARGET}
    cache = {}
    def evaluate(belt_lines, ring, ob, nmem, kis_int, crit_keep):
        key = (tuple(belt_lines), ring, ob, nmem, kis_int, crit_keep)
        if key in cache: return cache[key]
        b = copy.deepcopy(b0)
        belt = next(g for g in b["gear"] if g["slot"] == "belt"); belt["name"] = "Arcanist Girdle (20% CDR base, Gale)"
        belt["lines"] = ["+20% Cooldown Recovery Speed"] + list(belt_lines)
        rr = next(g for g in b["gear"] if g["slot"] == "ring_r"); rr["lines"][rr["lines"].index("+20 to Max Frostbite Rating")] = "+32 to Max Frostbite Rating"
        rl = next(g for g in b["gear"] if g["slot"] == "ring_l")
        if ring_lines is not None: rl["lines"] = list(ring_lines[ring])
        else:
            rl["lines"].remove("+52 Intelligence")
            if ring == "asis": rl["lines"].append("+52 Intelligence")
            elif ring == "int78": rl["lines"].append("+78 Intelligence")
            elif ring == "block": rl["lines"].append("+20% Attack and Spell Block Chance")
        m = next(m for m in b["memories"] if m["slot"] == "trait")
        for l in ORANGE_LINES[:ob]: m["lines"].remove(l)
        for sl, l in MEM_CANDIDATES[:nmem]: next(mm for mm in b["memories"] if mm["slot"] == sl)["lines"].remove(l)
        L = b["kismets"]["lines"]; L[next(i for i, l in enumerate(L) if l.endswith("Intelligence"))] = f"+{kis_int} Intelligence"
        if not crit_keep: L.remove("+14% Critical Strike Damage")
        r = E.dps(b, t0); sh = r["sheet"]
        es = es_of(b, t0); lm = any("Low Mana" in l for l in belt_lines)
        cache[key] = dict(dps=r["dps"] / 1e12, es=es, ehp=ehp(es, lm), INT=sh["INT"], crit=sh["crit_chance"], boon=sh["boon_margin"], cap=r["cap_factor"])
        return cache[key]
    best = None
    for pre, suf in belt_structures():
        if force:
            if "pre" in force and not set(force["pre"]) <= set(pre): continue
            if "suf" in force and not all(suf.count(x) >= force["suf"].count(x) for x in set(force["suf"])): continue
            if "no" in force and any(x in force["no"] for x in pre + suf): continue
        nres = suf.count("res"); ele = 12 if "eleres" in suf else 0
        for ring in ring_modes:
            ring_both = 20 if (ring == "block" or (ring_lines is not None and any("Block" in l for l in ring_lines[ring]))) else 0
            if ring_lines is not None:
                rres = {e: sum(float(l.split("%")[0].lstrip("+")) for l in ring_lines[ring] if l.endswith(RES_LINE[e].split("% ")[1])) for e in TARGET}
            else:
                rres = {"fire": 12, "cold": 0, "lightning": 22, "erosion": 27}
            base_res = {"fire": 22 + 27 + rres["fire"], "cold": 12 + rres["cold"], "lightning": rres["lightning"], "erosion": rres["erosion"]}
            both = (20 if "block" in pre else 0) + ring_both + t_both
            for elems in itertools.combinations(TARGET, nres):
                res = {e: base_res[e] + t_res[e] + (35 if e in elems else 0) + (ele if e != "erosion" else 0) for e in TARGET}
                res_def = {e: TARGET[e] - res[e] for e in TARGET}
                for ob in range(0, 3):
                    for nmem in range(0, mem_max + 1):
                        singles = [ORANGE_LINE] * ob + [MEM_ROLL] * nmem
                        for crit_keep in (1, 0):
                            best_f = None
                            for mask in range(1 << len(singles)):
                                a = sum(v for i, v in enumerate(singles) if mask >> i & 1); s = sum(singles) - a
                                att_need = 100 - both - t_att - a; spl_need = 100 - both - t_spl - s
                                f = fates(max(0, att_need), max(0, spl_need), res_def)
                                if f is None: continue
                                it = f[0] - (15 if crit_keep else 0)
                                if f[1]["int_micros"] - crit_keep < 0: continue
                                if best_f is None or it > best_f[0]: best_f = (it, f[1], mask)
                            if best_f is None: continue
                            kis_int = best_f[0]
                            belt_lines = [BELT_P[x][1] for x in pre] + [RES_LINE[e] for e in elems] + [BELT_S[x][1] for x in suf if x != "res"]
                            r = evaluate(belt_lines, ring, ob, nmem, kis_int, crit_keep)
                            if best is None or r["dps"] > best["dps"]:
                                best = dict(r, belt=belt_lines, ring=ring, orange_block=ob, mem_rolls=nmem, kismet_int=kis_int, crit_micro=crit_keep,
                                            fates=best_f[1], res=res, block_tree=(t_att, t_spl, t_both))
    return best


def describe(r):
    f = r["fates"]
    return (f"{r['dps']:5.1f} T | ES {r['es']:.0f} | EHP ele {r['ehp']['ele']/1000:.1f}k phys {r['ehp']['phys']/1000:.1f}k dot {r['ehp']['dot']/1000:.1f}k | INT {r['INT']:.0f} crit {r['crit']:.1f}% boon {r['boon']:.2f}\n"
            f"      belt {r['belt']}\n      ring L {r['ring']} | orange->block {r['orange_block']} | memory rolls {r['mem_rolls']} | crit micro kept {r['crit_micro']}\n"
            f"      fates: block micros {f['block_micros']} / mediums {f['block_mediums']}, res micros {f['res_micros']} / mediums {f['res_mediums']}, INT micros {f['int_micros']} / mediums {f['int_mediums']} -> kismet INT {r['kismet_int']}\n"
            f"      res {r['res']} | tree block {r['block_tree']}")
