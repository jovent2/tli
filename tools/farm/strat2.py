#!/usr/bin/env python3
"""Step 2: a per-map simulator on the checkpoint-2 model, the marginal table on Vlad's Overrealm loop, and the strat search.

Simulator (one setup -> FE per map, seconds, deaths, lottery):
  families present = the mechanics whose compass is in the setup. Primary family (for FE and the unfitted "other" items): vigil > outlaw >
  lunaria > darksurge. Mechanic items come from the family that owns the loot type (mods: outlaw, Nether King's / Goddess remnants: vigil,
  Lunar dust: lunaria), generic items (Sprout, fossils, embers, Tomorrow's...) from the primary family's fit.
  Free compass effects: on FE every fitted effect applies (another mechanic's compass on FE *is* that mechanic's FE); on a mechanic's own
  items only the global compasses apply (Generous, Bountiful, Compass / Fluorescent probe) - another mechanic's compass or the Gear probe
  on Warlock mods measures who runs them, not a drop mechanic.
  Pets: Fuel trio in the regular slots (swappable), Outlaw trio in the Carjack, special slots as in model.py. Card: constant (Vlad: even out).
  Bounty Orders: the CN assumption (half the time) - the model as fitted, not tuned to him.
  Overrealm: not modelled. His own 71 Evernight + Shadow maps supply the block (loot inside + the exit dump, seconds, deaths, by floors);
  the matrix says Overrealm loot ignores Drop Quantity, so nothing else in the setup touches it.
  Time (in map, + 20 s town): 108 s base map (his Alert maps 11-05: 127 s with a Carjack and an All-Evil, no Overrealm), + 19 s Evernight
  delivery, + 5 s Carjack, + his Overrealm seconds; mechanics he has never run: CN median x 1.2 (flag).

  python3 tools/farm/strat2.py --overrealm-block LOG ...   # (re)build data/ext/model/overrealm_block.json from his logs
  python3 tools/farm/strat2.py [--md out.md]               # loop table + search
"""
import argparse
import collections
import datetime
import itertools
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN  # noqa: E402
import model as M  # noqa: E402

RES = json.load(open(os.path.join(RN.EXT, "model", "checkpoint2.json")))
BLOCK_FILE = os.path.join(RN.EXT, "model", "overrealm_block.json")
BYNAME = {RN.name(i): i for i in RN.ITEMS}
GLOBAL_FREE = {"Generous_Elite_Compass", "Bountiful_Elite_Compass", "Compass_Deep_Space_Probe", "Fluorescent_Deep_Space_Probe"}
PLAYSTYLE = {"Gear_Deep_Space_Probe"}            # measures who runs it, not a drop mechanic: never applied
OWNER = M.OWNER
SE_MAX = 0.4                                     # an exponent with a wider bar than this is unidentified: the text's 1 is used instead
FLAGS = set()
PRIMARY = ["vigil", "outlaw", "lunaria", "darksurge"]
BEACON = "Deep_Space_Beacon"
TOWN = 20.0
BASE_S = 108.0
PHASE_S = {"Evernight_Vigil_Compass": 19.0, "Alert_Outlaw_Compass": 5.0, "All-Evil_Vigil_Compass": 0.0, "Phantom_Vigil_Compass": 19.0, "Strength_in_Numbers_Soldier_Compass": 5.0}
# compasses with no usable CN data inside his exclusions (their players are all Machines / Doll): priced from the text on the generic
# (normal-monster) part of the map only. Strength in Numbers: +20% additional for Normal monsters (+10 groups not priced). Transgression:
# +3% per Rare killed up to 30, taken at ~10 stacks = x1.3, and -2% damage per stack not priced.
TEXT_GENERIC = {"Strength_in_Numbers_Soldier_Compass": 1.2, "Transgression_Plunder_Compass": 1.3}
SLOTS = 4
NEVER_RUN = {"lunaria": 1.2, "darksurge": 1.2}      # CN seconds x factor for mechanics he has not run
VIGIL_NODES = {"+1% additional Drop Quantity for the Vigil": 15, "+8% additional Drop Quantity for the Vigil": 1, "+15% additional Drop Quantity for the Vigil": 1, "During White Night Mode, +12%": 1}
OUTLAW_NODES = {"+1% additional Drop Quantity for all Security": 18, "+6% additional Drop Quantity for all Security": 1, "Super Sonic": 1, "for every 10 Escort Bodyguard": 1,
                "+30% additional Drop Quantity for all Security personnel after": 1}
ALL_PETS = sorted(s for s in M.AFF if "6" in M.AFF[s])


def cname(c):
    return c.replace("_Compass", "").replace("_%28Artifact%29", " (A)").replace("_Deep_Space_Probe", " probe").replace("_", " ")


def nodes_of(setup):
    out = collections.Counter()
    for fam, d in setup["nodes"].items():
        for k, v in d.items():
            out[(fam, k)] += v
    return out


def pet_adjust(fname, loot, pets, assumed):
    """(dflat, ratio_add) to move a phase's multipliers from the assumed regular trio to `pets`."""
    fam = M.FAMILIES[fname]; play, branch = fam["play"]
    f0, a0 = M.pet_mult(play, branch, loot, assumed); f1, a1 = M.pet_mult(play, branch, loot, pets)
    return f1 - f0, a1 / a0


def exponent(c, k, fname, item):
    return c[k][0]          # model.py already replaced unidentified exponents by the text's 1 and refitted


def item_qty(fname, item, setup, mechanic_free_only):
    r = RES[fname].get(item)
    if not r:
        return 0.0
    c = r["coef"]; fam = M.FAMILIES[fname]; cost = setup["comp"]; nodes = nodes_of(setup); generic = r.get("generic", False)
    cost = dict(cost); cost["Deep_Space_Resonance"] = 2 * setup["dsres"]
    pool, add = M.setup_mult(fname, fam, nodes, cost, item, generic=generic)
    if not generic:
        add *= setup.get("extra_add", {}).get(fname, 1.0)
    if setup["pets"] != M.FUEL_TRIO:
        lt = M.loot_type(item) or "fuel"
        if generic:
            f0, a0 = M.pet_mult(None, None, lt, M.FUEL_TRIO); f1, a1 = M.pet_mult(None, None, lt, setup["pets"]); pool += f1 - f0; add *= a1 / a0
        elif fam["regular"] == M.FUEL_TRIO:
            df, ra = pet_adjust(fname, lt, setup["pets"], M.FUEL_TRIO); pool += df; add *= ra
    lg = c["const"][0] + exponent(c, "a", fname, item) * math.log(pool) + exponent(c, "b", fname, item) * math.log(add)
    for k, (b, se) in c.items():
        if k in ("const", "a", "b") or k.startswith("hero") or abs(b) <= 1.96 * se or k in PLAYSTYLE:
            continue
        if mechanic_free_only and k not in GLOBAL_FREE:
            continue
        lg += b * cost.get(k, 0.0)
    return math.exp(lg)


def fe_qty(fname, setup):
    fe = RES[fname].get("FE_split")
    fam = M.FAMILIES[fname]; cost = dict(setup["comp"]); cost["Deep_Space_Resonance"] = 2 * setup["dsres"]; nodes = nodes_of(setup)
    if not fe:
        return item_qty(fname, M.FE, setup, False), 0.0
    c = fe["coef"]; pg, ag, pm, am = M.fe_mults(fname, fam, nodes, cost); am *= setup.get("extra_add", {}).get(fname, 1.0)
    if setup["pets"] != M.FUEL_TRIO:
        f0, a0 = M.pet_mult(None, None, "fuel", M.FUEL_TRIO); f1, a1 = M.pet_mult(None, None, "fuel", setup["pets"])
        pg += f1 - f0; ag *= a1 / a0
        if fam["regular"] == M.FUEL_TRIO:
            df, ra = pet_adjust(fname, "fuel", setup["pets"], M.FUEL_TRIO); pm += df; am *= ra
    g = math.exp(c["Bg"][0]) * pg ** c["a"][0] * ag ** c["c"][0]; m = math.exp(c["Bm"][0]) * pm ** c["a"][0] * am ** c["b"][0]
    f = 1.0
    for k, (b, se) in c.items():
        if k in ("Bg", "Bm", "a", "b", "c") or k.startswith("hero") or abs(b) <= 1.96 * se:
            continue
        f *= math.exp(b * cost.get(k, 0.0))
    return g * f, m * f


def families(setup):
    return [f for f in PRIMARY if any(c in setup["comp"] for c in M.FAMILIES[f]["compasses"])]


def simulate(setup, block=None):
    fams = families(setup)
    if not fams:
        return None
    prim = fams[0]
    items = {}
    done = set()
    for fname in fams:
        for item in RES[fname]:
            if item in ("FE_split", "_other", M.FE) or item in done:
                continue
            owner = OWNER.get(M.loot_type(item))
            if owner:
                if owner != fname:
                    continue                  # a mechanic's loot comes only from its own family's fit; owner absent -> not in the map
            elif fname != prim:
                continue                      # generic items from the primary family only
            items[item] = item_qty(fname, item, setup, mechanic_free_only=bool(owner))
            done.add(item)
    g, m = fe_qty(prim, setup)
    tg = 1.0
    for c, mult in TEXT_GENERIC.items():
        tg *= mult ** setup["comp"].get(c, 0.0)
    if tg != 1.0:
        g *= tg
        for i in list(items):
            if not OWNER.get(M.loot_type(i)):
                items[i] *= tg
    items[M.FE] = g + m
    steady = sum(RN.value(i, q) for i, q in items.items()) + RES[prim]["_other"]["steady"] * tg
    lottery = RES[prim]["_other"]["lottery"]
    secs = BASE_S + sum(PHASE_S.get(c, 0.0) * q for c, q in setup["comp"].items())
    flags = []
    for f in fams:
        if f in NEVER_RUN:
            secs = max(secs, RES[f]["_other"]["secs"] * NEVER_RUN[f]); flags.append(f"time: CN x{NEVER_RUN[f]} ({f} never run)")
    cost = sum(RN.value(BYNAME[c], q, sold=False) for c, q in setup["comp"].items() if c in BYNAME) + RN.value(BYNAME[BEACON], 1, sold=False) + 2 * setup["dsres"] * RN.price(BYNAME["Deep_Space_Resonance"])
    deaths = RES[prim]["_other"]["deaths"]
    ovr = None
    if setup.get("overrealm") and block:
        ovr = block; steady += ovr["gross"]; secs += ovr["secs"]; cost += RN.value(BYNAME["Shadow_Overrealm_Compass"], 1, sold=False)
    return dict(items=items, fe_generic=g, fe_mech=m, steady=steady, lottery=lottery, cost=cost, net=steady - cost, secs=secs,
                per_min=(steady - cost) / ((secs + TOWN) / 60), per_min_lot=(steady + lottery - cost) / ((secs + TOWN) / 60), deaths=deaths, flags=flags, ovr=ovr)


# ------------------------------------------------------------------ the Overrealm block from his logs
def build_block(logs):
    import gamelog as G
    import overrealm_loop as O
    maps = G.parse(logs); picks, marks = O.walk(logs)
    ms = [m for m in maps if any("Overrealm" in RN.name(i) for i in m["cost"])]
    rows = O.per_map(ms, picks, marks)
    # exit dump: pickups within 20 s after the Overrealm stop
    byf = collections.defaultdict(list)
    for r in rows:
        m = r["m"]; t0, t1 = (m["entered"] or m["start"]), m["end"]
        mk = [(t, k) for t, k in marks if t0 <= t <= t1]
        oe = next((t for t, k in mk if k == "ovr_enter"), None); os_ = next((t for t, k in reversed(mk) if k == "ovr_stop"), None)
        loot = collections.Counter()
        if oe and os_:
            for t, d in picks:
                if oe <= t <= os_ + datetime.timedelta(seconds=20):
                    loot.update(d)
        byf[r["floors"]].append(dict(loot=loot, secs=r["ovr_s"] or 0.0, deaths=r["deaths"]))
    out = {"maps": len(rows), "by_floors": {}}
    tot = collections.Counter(); tsec = 0.0; tdeath = 0.0
    for f, rs in sorted(byf.items()):
        n = len(rs); loot = collections.Counter()
        for r in rs:
            loot.update(r["loot"])
        gross = sum(RN.value(i, q) for i, q in loot.items()) / n
        out["by_floors"][str(f)] = dict(maps=n, gross=gross, secs=sum(r["secs"] for r in rs) / n, deaths=sum(r["deaths"] for r in rs) / n,
                                        top=[(RN.name(i), round(q / n, 2), round(RN.value(i, q) / n, 1)) for i, q in sorted(loot.items(), key=lambda kv: -RN.value(kv[0], kv[1]))[:6]])
        tot.update(loot); tsec += sum(r["secs"] for r in rs); tdeath += sum(r["deaths"] for r in rs)
    n = len(rows)
    out.update(gross=sum(RN.value(i, q) for i, q in tot.items()) / n, secs=tsec / n, deaths=tdeath / n,
               top=[(RN.name(i), round(q / n, 2), round(RN.value(i, q) / n, 1)) for i, q in sorted(tot.items(), key=lambda kv: -RN.value(kv[0], kv[1]))[:10]],
               prices=os.path.basename(RN.PRICE_FILE))
    json.dump(out, open(BLOCK_FILE, "w"), indent=1)
    return out


# ------------------------------------------------------------------ setups
def vlad_loop():
    return dict(comp={"Evernight_Vigil_Compass": 1.0, "Generous_Elite_Compass": 1.0, "Sinful_Plunder_Compass": 1.0, "Flourishing_Deep_Space_Probe": 1.0},
                dsres=0, nodes={"vigil": dict(VIGIL_NODES), "outlaw": dict(OUTLAW_NODES)}, pets=list(M.FUEL_TRIO), overrealm=True)


def clone(s, **kw):
    t = json.loads(json.dumps(s)); t.update(kw); return t


def moves(setup):
    """Every single change to a setup: (label, new setup)."""
    out = []
    comp = setup["comp"]
    for c in ("Generous_Elite_Compass", "Bountiful_Elite_Compass", "Alert_Outlaw_Compass", "Lunar_Stele_Lunaria_Compass", "Divine_Warrior_Dark_Surge_Compass",
              "Strength_in_Numbers_Soldier_Compass", "Transgression_Plunder_Compass"):
        if c in comp:
            out.append((f"drop {cname(c)}", clone(setup, comp={k: v for k, v in comp.items() if k != c})))
        else:
            if c == "Bountiful_Elite_Compass" and "Generous_Elite_Compass" in comp:
                out.append((f"Generous -> Bountiful", clone(setup, comp={**{k: v for k, v in comp.items() if k != "Generous_Elite_Compass"}, c: 1.0})))
            elif c == "Generous_Elite_Compass" and "Bountiful_Elite_Compass" in comp:
                continue
            else:
                out.append((f"add {cname(c)}", clone(setup, comp={**comp, c: 1.0})))
    vig = [c for c in comp if "Vigil" in c]
    for c in ("All-Evil_Vigil_Compass", "Evernight_Vigil_Compass"):
        if vig and c not in comp:
            out.append((f"{cname(vig[0])} -> {cname(c)}", clone(setup, comp={**{k: v for k, v in comp.items() if k != vig[0]}, c: 1.0})))
    sin = [c for c in comp if "Sinful" in c]
    for c in ("Sinful_Plunder_Compass", "Sinful_Plunder_Compass_%28Artifact%29"):
        if c not in comp:
            out.append(((f"{cname(sin[0])} -> " if sin else "add ") + cname(c), clone(setup, comp={**{k: v for k, v in comp.items() if k not in sin}, c: 1.0})))
    if sin:
        out.append((f"drop {cname(sin[0])}", clone(setup, comp={k: v for k, v in comp.items() if k not in sin})))
    pr = [c for c in comp if "Probe" in c]
    for c in ("Flourishing_Deep_Space_Probe", "Compass_Deep_Space_Probe", "Fluorescent_Deep_Space_Probe"):
        if c not in comp:
            out.append(((f"{cname(pr[0])} -> " if pr else "add ") + cname(c), clone(setup, comp={**{k: v for k, v in comp.items() if k not in pr}, c: 1.0})))
    if pr:
        out.append((f"drop {cname(pr[0])}", clone(setup, comp={k: v for k, v in comp.items() if k not in pr})))
    for d in (0, 1, 2):
        if d != setup["dsres"]:
            out.append((f"DS resonance affixes {setup['dsres']} -> {d}", clone(setup, dsres=d)))
    if setup.get("overrealm"):
        out.append(("drop the Overrealm", clone(setup, overrealm=False)))
    # tree: one more Vigil micro, the +8 / +15 / WN mediums if missing; Outlaw mediums
    for fam, line, lab in (("vigil", "+1% additional Drop Quantity for the Vigil", "+1 Vigil micro"), ("outlaw", "+1% additional Drop Quantity for all Security", "+1 Outlaw micro")):
        n = clone(setup); n["nodes"].setdefault(fam, {}); n["nodes"][fam][line] = n["nodes"][fam].get(line, 0) + 1
        out.append((lab, n))
    return out


def show(sim, label=""):
    return (f"{label:52s} | net {sim['net']:6.0f}/map | {sim['per_min']:5.1f}/min (+lottery {sim['per_min_lot']:5.1f}) | {sim['secs'] + TOWN:4.0f} s | "
            f"FE {sim['items'][M.FE]:4.0f} | cost {sim['cost']:4.0f}" + (" | " + "; ".join(sim["flags"]) if sim["flags"] else ""))


def top_items(sim, k=6):
    return ", ".join(f"{RN.name(i).replace('_', ' ')[:24]} {q:.2f} ({RN.value(i, q):.0f})" for i, q in sorted(sim["items"].items(), key=lambda kv: -RN.value(kv[0], kv[1]))[:k])


def loop_table(block, md):
    base = vlad_loop(); s0 = simulate(base, block)
    md.append("\n# His loop (Evernight + Shadow Overrealm + Generous + Sinful + Flourishing, no DS affixes, Fuel trio), the model's view")
    md.append(show(s0, "as run") + f"\n  items: {top_items(s0)}; Overrealm block (his {block['maps']} maps): {block['gross']:.0f} FE in {block['secs']:.0f} s, {block['deaths']:.2f} deaths")
    md.append(f"  his measured 11-06: net 123/map, 214 s in map, 33.8/min (the model's map part: FE {s0['items'][M.FE]:.0f} = generic {s0['fe_generic']:.0f} + wraith {s0['fe_mech']:.0f})")
    md.append("\n## Marginals, one change at a time from the loop as run (FE/map and /min deltas; > ~15 FE/map is a real difference, less is noise)")
    md.append("change | net/map | /min | delta/map | delta/min")
    rows = []
    for lab, s in moves(base):
        sim = simulate(s, block)
        rows.append((sim["per_min"] - s0["per_min"], lab, sim))
    for d, lab, sim in sorted(rows, reverse=True):
        md.append(f"{lab:52s} | {sim['net']:6.0f} | {sim['per_min']:5.1f} | {sim['net'] - s0['net']:+6.0f} | {d:+5.1f}" + (" | " + "; ".join(sim["flags"]) if sim["flags"] else ""))
    md.append("\n## Greedy path: apply the best change, recompute, repeat while it gains > 1/min")
    cur, sc = base, s0; path = []
    for _ in range(8):
        best = None
        for lab, s in moves(cur):
            sim = simulate(s, block)
            if best is None or sim["per_min"] > best[2]["per_min"]:
                best = (lab, s, sim)
        if best is None or best[2]["per_min"] - sc["per_min"] <= 1.0:
            break
        cur, sc = best[1], best[2]; path.append(best[0])
        md.append(show(sc, " + ".join(path)[-52:]))
    md.append(f"  result: {', '.join(cname(c) for c in cur['comp'])}, DS affixes {cur['dsres']}, Overrealm {'kept' if cur.get('overrealm') else 'dropped'}; items: {top_items(sc)}")
    return cur, sc


def search(block, md):
    mechs = [("Evernight_Vigil_Compass",), ("All-Evil_Vigil_Compass",), ("Alert_Outlaw_Compass",), ("Lunar_Stele_Lunaria_Compass",), ("Divine_Warrior_Dark_Surge_Compass",),
             ("Alert_Outlaw_Compass", "Evernight_Vigil_Compass"), ("Alert_Outlaw_Compass", "All-Evil_Vigil_Compass"), ("Alert_Outlaw_Compass", "Lunar_Stele_Lunaria_Compass"),
             ("Evernight_Vigil_Compass", "Lunar_Stele_Lunaria_Compass"), ("All-Evil_Vigil_Compass", "Lunar_Stele_Lunaria_Compass")]
    elites = [(), ("Generous_Elite_Compass",), ("Bountiful_Elite_Compass",)]
    sinfuls = [(), ("Sinful_Plunder_Compass",), ("Sinful_Plunder_Compass_%28Artifact%29",)]
    extras = [(), ("Strength_in_Numbers_Soldier_Compass",), ("Transgression_Plunder_Compass",), ("Strength_in_Numbers_Soldier_Compass", "Transgression_Plunder_Compass")]
    probes = [(), ("Flourishing_Deep_Space_Probe",), ("Compass_Deep_Space_Probe",), ("Fluorescent_Deep_Space_Probe",)]
    out = []
    for mech, el, si, ex, pr in itertools.product(mechs, elites, sinfuls, extras, probes):
        for dsres in (0, 2):
            for ovr in ((False, True) if any("Vigil" in m for m in mech) else (False,)):
                if len(mech) + len(el) + len(si) + len(ex) + (1 if ovr else 0) > SLOTS:
                    continue
                comp = {c: 1.0 for c in mech + el + si + ex + pr}
                s = dict(comp=comp, dsres=dsres, nodes={"vigil": dict(VIGIL_NODES), "outlaw": dict(OUTLAW_NODES)}, pets=list(M.FUEL_TRIO), overrealm=ovr)
                sim = simulate(s, block)
                if sim:
                    out.append((sim["per_min"], s, sim))
    out.sort(key=lambda t: -t[0])
    md.append(f"\n# Search: {len(out)} setups (mechanics x elite x Sinful x Strength in Numbers / Transgression x probe x DS affixes 0/2 x Overrealm; at most {SLOTS} compasses + probe), his tree lines, Fuel trio, ranked by net FE per in-map minute")
    md.append("rank | /min | +lottery | net/map | s | FE | cost | setup")
    seen = 0
    for k, (pm, s, sim) in enumerate(out[:40]):
        md.append(f"{k + 1:2d} | {pm:5.1f} | {sim['per_min_lot']:5.1f} | {sim['net']:5.0f} | {sim['secs'] + TOWN:4.0f} | {sim['items'][M.FE]:4.0f} | {sim['cost']:4.0f} | "
                  + ", ".join(cname(c) for c in s["comp"]) + f", DS x{s['dsres']}" + (", Overrealm" if s["overrealm"] else "") + (" | " + "; ".join(sim["flags"]) if sim["flags"] else ""))
    # the best without the Overrealm and the best of each mechanic set
    md.append("\n## Best per mechanic set")
    best = {}
    for pm, s, sim in out:
        key = tuple(sorted(c for c in s["comp"] if any(c in M.FAMILIES[f]["compasses"] for f in M.FAMILIES))) + (("Overrealm",) if s["overrealm"] else ())
        if key not in best:
            best[key] = (pm, s, sim)
    for key, (pm, s, sim) in sorted(best.items(), key=lambda kv: -kv[1][0]):
        md.append(f"{pm:5.1f}/min (+lot {sim['per_min_lot']:5.1f}) | {' + '.join(cname(c) for c in key):42s} | with " + ", ".join(cname(c) for c in s["comp"] if c not in key) + f", DS x{s['dsres']} | items: {top_items(sim, 5)}")
    return out


def pet_search(setup, block, md):
    """Best regular trio for this setup (the special slots and the Carjack trio stay)."""
    special = {p for v in M.SPECIAL.values() for p in v}
    cands = [s for s in ALL_PETS if s not in special and any(M.line_effect(l, "fuel") or M.line_effect(l, "void_divinity_crafting_material", "night_watch") for l in M.AFF[s]["6"])]
    base = simulate(setup, block)["per_min"]
    rows = []
    for trio in itertools.combinations(cands, 3):
        s = clone(setup, pets=list(trio)); sim = simulate(s, block)
        rows.append((sim["per_min"] - base, trio))
    rows.sort(reverse=True)
    md.append(f"\n## Regular pet slots on this setup ({len(cands)} candidate pets, every trio): Fuel trio = 0")
    for d, trio in rows[:8]:
        md.append(f"  {d:+5.1f}/min | " + ", ".join(M.SNAME[s] for s in trio))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--overrealm-block", nargs="*", default=None)
    ap.add_argument("--md", default=None)
    a = ap.parse_args(argv)
    if a.overrealm_block:
        b = build_block(a.overrealm_block)
        print(json.dumps({k: v for k, v in b.items() if k != "by_floors"}, indent=1)); print(json.dumps(b["by_floors"], indent=1))
        return
    block = json.load(open(BLOCK_FILE))
    md = [f"Step 2 — prices {os.path.basename(RN.PRICE_FILE)}, model checkpoint 2, Fright {M.FRIGHT}, Overrealm block from his {block['maps']} maps ({block['gross']:.0f} FE, {block['secs']:.0f} s, {block['deaths']:.2f} deaths per map)"]
    cur, sc = loop_table(block, md)
    pet_search(cur, block, md)
    search(block, md)
    fx = [f"{f} {RN.name(i)}: {'/'.join(r['fixed'])}" for f in RES for i, r in RES[f].items() if isinstance(r, dict) and r.get("fixed")]
    md.append("\n## Exponents the data could not pin (bar > 0.4 or negative), set to the text's 1 and refitted: " + "; ".join(fx))
    text = "\n".join(md); print(text)
    if a.md:
        open(a.md, "w").write(text + "\n")


if __name__ == "__main__":
    main()
