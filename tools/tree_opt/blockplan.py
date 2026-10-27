"""Block plan (2026-10-27): Lich -> Warlock (Dirty Tricks), Pedigree Defensiveness + OTBT, Spell Ripple prism (3x3 centred,
+2% sealed mana comp per medium rank in its area) on a third panel X, new CDR+Gale belt. Tree search over X and prism cell.

Rules [Vlad]: paired node needs its left node maxed (prism cell counts as maxed), column gates, 24 pts per panel, 110 total,
prisms never on god panels, prism area must hold >= 9 medium ranks (18% comp) so the 3 mana auras still fit after Lich.
"""
import sys, os, copy, json, itertools
sys.path.insert(0, os.path.dirname(__file__))
import scen as S, opt3
E = S.E

GOD = ("God_of_Might", "Goddess_of_Hunting", "Goddess_of_Knowledge", "God_of_War", "Goddess_of_Deception", "God_of_Machines", "New_God", "Nether_King")
FIXED = ["Goddess_of_Knowledge", "Magister", "Warlock"]
CANDIDATES = [k for k in sorted(S.PAN) if k not in GOD and k not in FIXED]
MIN_COMP_RANKS = 9

TREES0 = json.load(open(os.path.join(os.path.dirname(__file__), "..", "..", "ss14", "thea", "trees.json")))
CUR = {p["panel"]: dict(p["nodes"]) for p in TREES0["panels"]}
WARLOCK_SEED = {"96_80": 3, "224_80": 3, "352_80": 3, "480_80": 3, "480_176": 3, "608_176": 1, "96_272": 3, "224_272": 3,
                "352_464": 3, "480_464": 3, "736_368": 3, "864_368": 1}          # the valid 26 from re3 (ES nodes included, unlocked)
BASE_LOCKS = {("Goddess_of_Knowledge", "224_176"): 3, ("Goddess_of_Knowledge", "352_176"): 3}   # Vlad keeps GoK cast/MS nodes


def cells(X):
    if X not in S.CELLS:
        S.CELLS[X] = S.cells(X)
    return S.CELLS[X]


def prism(X, nid):
    c = cells(X)[nid]
    return (X, nid, 3, 3, c["ci"] - 1, c["ri"] - 1)


def comp_ranks(alloc, pr):
    k = pr[0]
    return sum(alloc.get(k, {}).get(cid, 0) for cid in S.area(pr) if S.CELLS[k][cid]["kind"] == "M")


def placements(X):
    """prism cells whose 3x3 area holds >= 3 medium cells (9 ranks possible)."""
    out = []
    for nid in cells(X):
        pr = prism(X, nid)
        if sum(S.CELLS[X][c]["mr"] for c in S.area(pr) if S.CELLS[X][c]["kind"] == "M") >= MIN_COMP_RANKS:
            out.append(pr)
    return out


def make_valid(pr):
    def valid(alloc):
        probs = S.valid(alloc, pr)
        if comp_ranks(alloc, pr) < MIN_COMP_RANKS:
            probs.append("comp")
        return probs
    return valid


# ---------------------------------------------------------------- external state used while searching trees (the fit is redone exactly later)
def gear_mod(b, belt_lines=("+94% damage", "+20% Cooldown Recovery Speed", "+34% chance to deal Double Damage", "-18% additional damage taken at Low Mana"),
             ring_frost=32, ring_int=None, kismet_int=60, orange_block=True):
    belt = next(g for g in b["gear"] if g["slot"] == "belt")
    belt["name"] = "Arcanist Girdle (20% CDR base, Gale)"; belt["lines"] = list(belt_lines)
    r = next(g for g in b["gear"] if g["slot"] == "ring_r"); r["lines"][r["lines"].index("+20 to Max Frostbite Rating")] = f"+{ring_frost} to Max Frostbite Rating"
    rl = next(g for g in b["gear"] if g["slot"] == "ring_l"); rl["lines"].remove("+52 Intelligence")
    if ring_int: rl["lines"].append(f"+{ring_int} Intelligence")
    L = b["kismets"]["lines"]; L[next(i for i, l in enumerate(L) if l.endswith("Intelligence"))] = f"+{kismet_int} Intelligence"
    if orange_block:
        m = next(m for m in b["memories"] if m["slot"] == "trait")
        for l in ("+18% Spell Critical Strike Damage", "+18% Cold Skill Critical Strike Damage"): m["lines"].remove(l)
    return b


def build(alloc, pr, gear=gear_mod, **kw):
    X = pr[0]
    me = 3 if alloc.get("Lich", {}).get("864_176", 0) else 2
    S.CORES[X] = "Spell Ripple"; S.CORES["Warlock"] = "Dirty Tricks"; S.CORES["Magister"] = "Bunch"; S.CORES["Goddess_of_Knowledge"] = "Acquaintance"
    b, t = S.build_new(alloc, 0, lw=False, ped_core=None, otbt=True, me_charges=me)
    gear(b)
    for k, v in kw.items(): b["context"][k] = v
    return b, t


def dpsT(alloc, pr, **kw):
    b, t = build(alloc, pr, **kw)
    return E.dps(b, t)["dps"] / 1e12


def seed(X, pr, extra=None):
    a = {"Goddess_of_Knowledge": dict(CUR["Goddess_of_Knowledge"]), "Magister": {k: v for k, v in CUR["Magister"].items() if k != "608_176"},
         "Warlock": dict(WARLOCK_SEED), X: {}}
    if X == "Lich": a["Warlock"] = dict(WARLOCK_SEED)
    C = cells(X)
    def chain(nid):
        for l in C[nid]["left"]:
            if l == pr[1]: return
            a[X][l] = C[l]["mr"]; chain(l); return
    for cid in S.area(pr):
        if C[cid]["kind"] == "M":
            a[X][cid] = C[cid]["mr"]; chain(cid)
    for nid, r in (extra or {}).items():
        a[X][nid] = r; chain(nid)
    return a


def search(X, pr, locks=None, extra=None, iters=300, score=None, kicks=0, seed_rng=1, warm=None):
    panels = FIXED + [X]
    S.PANELS = panels
    a0 = seed(X, pr, extra)
    valid = make_valid(pr)
    lk = dict(BASE_LOCKS); lk.update(locks or {})
    for (k, n), r in lk.items():
        if k in a0: a0[k][n] = max(a0[k].get(n, 0), r)
    sc = score or (lambda a: dpsT(a, pr))
    # if the seed is over budget, trim unlocked ranks (lowest loss first) until it fits
    while opt3.total(a0) > 110:
        best = None
        for k in a0:
            for n, r in list(a0[k].items()):
                if r <= lk.get((k, n), 0): continue
                a2 = copy.deepcopy(a0); a2[k][n] -= 1
                if a2[k][n] == 0: del a2[k][n]
                if valid(a2): continue
                x = sc(a2)
                if best is None or x > best[0]: best = (x, a2)
        if best is None: break
        a0 = best[1]
    relaxed = lambda a: [p for p in valid(a) if "core needs 24" not in p]
    if relaxed(a0):
        return None, 0.0, relaxed(a0)
    # 1. fill X to 24 greedily (best DPS per point) under the relaxed rule
    while sum(a0[X].values()) < 24:
        adds = [x for x in opt3._adds(a0, [X], S.CELLS, relaxed, lk)]
        if not adds: break
        base = sc(a0)
        best = max(adds, key=lambda x: (sc(x) - base) / max(1, opt3.total(x) - opt3.total(a0)))
        a0 = best
    # 2. trim to budget under the strict rule (every panel keeps >= 24)
    while opt3.total(a0) > 110:
        best = None
        for k in a0:
            for n, r in list(a0[k].items()):
                if r <= lk.get((k, n), 0): continue
                a2 = copy.deepcopy(a0); a2[k][n] -= 1
                if a2[k][n] == 0: del a2[k][n]
                if valid(a2): continue
                x = sc(a2)
                if best is None or x > best[0]: best = (x, a2)
        if best is None: break
        a0 = best[1]
    if valid(a0):
        return a0, sc(a0), valid(a0)
    a1, cur = opt3.optimize(a0, panels, S.CELLS, sc, valid, lk, budget=110, iters=iters)
    # path B: optimise under the relaxed rule first (panels may dip under 24), then repair short panels and finish strictly
    aB = seed(X, pr, extra)
    for (k, n), r in lk.items():
        if k in aB: aB[k][n] = max(aB[k].get(n, 0), r)
    aB, cB = opt3.optimize(aB, panels, S.CELLS, sc, relaxed, lk, budget=110, iters=iters)
    for _ in range(40):
        short = [k for k in panels if sum(aB.get(k, {}).values()) < 24]
        if not short: break
        k = short[0]; best = None
        for x in opt3._adds(aB, [k], S.CELLS, relaxed, lk):
            drop = None
            for k2 in panels:
                if k2 == k: continue
                for n2, r2 in list(x[k2].items()):
                    if r2 <= lk.get((k2, n2), 0): continue
                    a3 = copy.deepcopy(x); a3[k2][n2] -= 1
                    if a3[k2][n2] == 0: del a3[k2][n2]
                    if opt3.total(a3) > 110 or relaxed(a3): continue
                    v = sc(a3)
                    if drop is None or v > drop[0]: drop = (v, a3)
            if drop and (best is None or drop[0] > best[0]): best = drop
        if best is None: break
        aB = best[1]
    if not valid(aB) and opt3.total(aB) <= 110:
        aB, cB = opt3.optimize(aB, panels, S.CELLS, sc, valid, lk, budget=110, iters=iters)
        if cB > cur + 1e-9:
            a1, cur = aB, cB
    # path C: warm start from a given allocation (e.g. the unconstrained optimum): add the locked nodes (+chains), trim to budget, optimise
    if warm is not None:
        aW = copy.deepcopy(warm)
        C = cells(X)
        def chainW(k, nid):
            for l in S.CELLS[k][nid]["left"]:
                if pr[0] == k and l == pr[1]: return
                if aW[k].get(l, 0) < S.CELLS[k][l]["mr"]:
                    aW[k][l] = S.CELLS[k][l]["mr"]; chainW(k, l)
                return
        for (k, n), r in lk.items():
            aW.setdefault(k, {})
            if aW[k].get(n, 0) < r:
                aW[k][n] = r; chainW(k, n)
        guard = 0
        while (opt3.total(aW) > 110 or valid(aW)) and guard < 80:
            guard += 1; best = None
            for k in aW:
                for n, r in list(aW[k].items()):
                    if r <= lk.get((k, n), 0): continue
                    a2 = copy.deepcopy(aW); a2[k][n] -= 1
                    if a2[k][n] == 0: del a2[k][n]
                    pv = valid(a2)
                    if pv and opt3.total(a2) <= 110: continue
                    x = sc(a2) - (100 if pv else 0)
                    if best is None or x > best[0]: best = (x, a2)
            if best is None: break
            aW = best[1]
        if opt3.total(aW) <= 110 and not valid(aW):
            aW, cW = opt3.optimize(aW, panels, S.CELLS, sc, valid, lk, budget=110, iters=iters)
            if cW > cur + 1e-9:
                a1, cur = aW, cW
    # iterated local search: kick (drop a few random unlocked ranks), refill, re-optimise, keep if better
    import random
    rng = random.Random(seed_rng)
    for _ in range(kicks):
        a2 = copy.deepcopy(a1)
        for _k in range(rng.randint(3, 7)):
            opts = [(k, n) for k in a2 for n, r in a2[k].items() if r > lk.get((k, n), 0)]
            if not opts: break
            k, n = rng.choice(opts)
            a3 = copy.deepcopy(a2); a3[k][n] -= 1
            if a3[k][n] == 0: del a3[k][n]
            if not valid(a3): a2 = a3
        a3, c3 = opt3.optimize(a2, panels, S.CELLS, sc, valid, lk, budget=110, iters=iters)
        if c3 > cur + 1e-9 and not valid(a3):
            a1, cur = a3, c3
    return a1, cur, valid(a1)


def tree_stats(alloc, pr):
    b, t = build(alloc, pr); recs = E.collect(b, t); tt = E.totals(recs); sh = E.sheet(b, t)
    tree = lambda key: sum(v for s, k, v, c, l in recs if k == key and s.startswith("tree"))
    return dict(att=tt["block.attack"], spl=tt["block.spell"], both=tt["block.both"], cold=tree("res.cold"), light=tree("res.lightning"),
                fire=tree("res.fire"), ero=tree("res.erosion"), ele=tree("res.ele"), es_pct=tree("es.pct"), comp_tree=tt["mana.comp"],
                comp_prism=2 * comp_ranks(alloc, pr), INT=sh["INT"], frost=sh["frostbite_rating"], lvl=sh["level_chromatic"], boon=sh["boon_margin"], cdr=sh["cdr"])
