"""Strategy search for Vlad on top of bottomup.py: evaluate any setup (compasses, probe, tree nodes) at today's prices and his times.

Yields come from the CN calibration (bottomup.fit); every multiplier is re-applied from HIS setup. Lotteries (items with < 25
drops in 46k runs) are valued at their observed rate per instance-map of the column they drop from (or globally).
Time: 40 s bare map [Vlad] + CN seconds per mechanic instance (fitted), with Vlad's overrides (Machines 180 s).
"""
import collections, itertools, json, math, sys
import numpy as np
import runs as RN, mech, chart
from bottomup import *

VLAD_TIME = {"Cruising_Mechanical_Compass_%28Artifact%29": 180.0, "Mechanical_Compass": 180.0, "Brilliant_Mechanical_Compass": 180.0, "tree:Machines": 180.0,
             "Revelation_Hunting_Astrolabe": 35.0, "General_Hunting_Astrolabe": 10.0, "Hunting_Astrolabe": 10.0, "War_Compass": 5.0, "Wild_War_Compass": 5.0, "tree:War": 5.0, "tree:Hunting": 10.0,
             "Onslaught_Might_Compass": 180.0, "Mecha_Might_Compass_%28Artifact%29": 180.0, "Flourishing_Might_Compass": 180.0, "Might_Compass": 180.0, "tree:Might": 180.0, "Flourishing_Gods_Compass": 240.0}
MIN_TIME = 10.0
BASE_TIME = 40.0
BEACON = 3.29; RES_PRICE = 0.11
CONST_KEY = {v: k for k, v in mech.CONSTELLATION.items()}      # mechanic -> constellation page key

def lottery_attribution(F):
    """lottery item -> (column, drops per instance-map) or ('global', drops per map)."""
    R, cols, X = F["R"], F["cols"], F["X"]
    runs = np.array([r["count"] for r in R]); inst = np.zeros((len(R), len(cols)))
    for s, st in enumerate(F["setups"]):
        for j, k in enumerate(cols):
            if k == "generic": inst[s, j] = 1
            elif k.startswith("tree:"): inst[s, j] = 0 if any(mech.compass_family(c) == k[5:] for c in st.compasses) else st.appear(k[5:]) / 100
            else: inst[s, j] = st.compasses.get(k, 0)
    out = {}
    for i, x in F["lottery"].items():
        d = np.array([r["loot"].get(i, 0.0) * r["count"] for r in R])
        best = ("global", d.sum() / runs.sum(), d.sum())
        for j, k in enumerate(cols):
            if k == "generic": continue
            m = inst[:, j] > 0
            if m.sum() < 3 or d[m].sum() < 5: continue
            g = d.sum() / runs.sum(); maps = (inst[m, j] * runs[m]).sum()
            rate = (d[m].sum() + 2) / (maps + 2 / g)      # shrunk toward the global per-map rate
            # attribute if the rate with the column is >= 5x the rate without
            without = d[~m].sum() / max(1.0, runs[~m].sum())
            if rate > 5 * (without + 1e-9) and rate > best[1] * 1.5: best = (k, rate, d[m].sum())
        out[i] = best
    return out

class Plan(Setup):
    def __init__(self, compasses=None, probes=None, nodes=None, resonance=31, pets=None):
        super().__init__(resonance=resonance, compasses=compasses or {}, probes=probes or {}, nodes=nodes or [])
    def inst_columns(self, cols):
        out = {}
        for k in cols:
            if k == "generic": out[k] = 1.0
            elif k.startswith("tree:"):
                M = k[5:]
                if any(mech.compass_family(c) == M for c in self.compasses): continue
                a = self.appear(M) / 100
                if a > 0: out[k] = a
            else:
                q = self.compasses.get(k, 0)
                if q > 0: out[k] = q
        return out

def evaluate(F, LA, plan, verbose=False):
    cols, Y = F["cols"], F["Y"]
    inst = plan.inst_columns(cols); Qg = plan.Qg()
    items = collections.Counter(); by_col = collections.Counter(); secs = BASE_TIME
    T = F["T"]
    for k, n in inst.items():
        j = cols.index(k)
        M = "generic" if k == "generic" else (k[5:] if k.startswith("tree:") else (mech.compass_family(k) or "generic"))
        add, im = (1.0, 1.0) if M == "generic" else plan.mech_mult(M, k)
        Xk = n * im * add * plan.transgression(M) * (1.0 if M in NQ_MECH else Qg)
        if k != "generic" and F.get("xmax", {}).get(k, 0) > 0: Xk = min(Xk, XCAP * F["xmax"][k] * max(1.0, n))   # support cap: no extrapolation past CN
        cm = {cls: plan.class_mult(cls, M) for cls in ("compass", "fluor", "ember", "legendary", "other", "probe", "beacon")}
        if k != "generic": secs += n * max(MIN_TIME, VLAD_TIME.get(k, T.get(k, 0.0)))
        for i, y in F["colitems"][j]:
            q = y * Xk * cm[item_class(i)]
            if RN.name(i) in NQ_ITEMS: q /= Qg
            if RN.name(i) in EXCL_MEMORIES: q *= plan.excl_fluor_mult()
            items[i] += q; by_col[k] += val(i, q)
    lot = 0.0
    for k in ["global"] + list(inst):
        for i, rate in F["lot_by_col"].get(k, []):
            q = rate if k == "global" else rate * inst[k]
            items[i] += q; lot += val(i, q); by_col["lottery:" + k] += val(i, q)
    gross = sum(val(i, q) for i, q in items.items())
    refund = 0.9 if any("10% chance to not consume Compasses" in t for _, t, _ in plan.nodes) else 1.0
    cost = BEACON + plan.res * RES_PRICE + refund * sum(pname(k) * q for k, q in plan.compasses.items()) + sum(pname(k) * q for k, q in plan.probes.items())
    net = gross - cost
    return dict(gross=gross, cost=cost, net=net, secs=secs, net_per_min=net / (secs / 60), items=items, by_col=by_col, lottery=lot, Qg=Qg, pool=plan.pool())

def node_tuple(constellation_key, n, cnt=1):
    return (mech.CONSTELLATION.get(constellation_key, constellation_key), " · ".join(n["lines"]), cnt)

def best_tree(F, LA, plan, constellations, budget, prime=4):
    """Greedy allocation across constellations: for each, best_subtree with linearized node values; then pick the budget split."""
    base = evaluate(F, LA, plan)["net"]
    per = {}
    for ck in constellations:
        def value(n, ck=ck):
            if n["name"] == "Initial Node": return 0.0
            p2 = Plan(dict(plan.compasses), dict(plan.probes), plan.nodes + [node_tuple(ck, n)], plan.res)
            return evaluate(F, LA, p2)["net"] - base
        res, nodes = chart.best_subtree(ck, value, budget)
        per[ck] = (res, nodes)
    return per

def apply_tree(plan, per, split):
    nodes = list(plan.nodes); picked = {}
    for ck, k in split.items():
        res, gnodes = per[ck]
        if k in res:
            picked[ck] = [idx for idx in res[k][1] if gnodes[idx]["name"] != "Initial Node"]
            for idx in picked[ck]: nodes.append(node_tuple(ck, gnodes[idx]))
    out = Plan(dict(plan.compasses), dict(plan.probes), nodes, plan.res); out.picked = picked
    return out

PROFOUND = [("Profound", "In Netherrealm stages, +2% Drop Quantity", 2), ("Profound", "In Netherrealm stages, +25% Drop Quantity · Netherrealm stage challenge attempts -4", 1),
            ("Profound", "In Netherrealm stages, +12% additional Drop Quantity · Activating of this node costs 25 additional Star Talent(s)", 1)]   # 4 Prime + 25 Star

PRICE_BY_NAME = {}
for _i in RN.ITEMS:
    if RN.name(_i) not in PRICE_BY_NAME or RN.price(_i): PRICE_BY_NAME[RN.name(_i)] = RN.price(_i) or 0.0
def pname(k): return PRICE_BY_NAME.get(k, 0.0)

XCAP = 1.2       # a column's multiplier may exceed the largest CN-observed multiplier for that column by at most this factor

def load_fit():
    F = fit(); F["T"] = duration_fit(F); LA = lottery_attribution(F)
    F["xmax"] = {k: float(F["X"][:, j].max()) for j, k in enumerate(F["cols"])}
    F["colitems"] = [[(i, F["Y"][i][j]) for i in F["items"] if F["Y"][i][j] > 0] for j in range(len(F["cols"]))]
    F["lot_by_col"] = collections.defaultdict(list)
    for i, (k, rate, drops) in LA.items(): F["lot_by_col"][k].append((i, rate))
    return F, LA

def report(F, LA, plan, title=""):
    e = evaluate(F, LA, plan)
    print(f"\n### {title}: gross {e['gross']:.0f}  cost {e['cost']:.0f}  NET {e['net']:.0f} FE/map  {e['secs']:.0f} s  => {e['net_per_min']:.0f} FE/min   (pool +{e['pool']:.0f}%, Qg x{e['Qg']:.2f}, lottery {e['lottery']:.0f})")
    print("   compasses:", {k: round(v, 2) for k, v in plan.compasses.items()}, "probes:", plan.probes)
    for k, v in sorted(e["by_col"].items(), key=lambda kv: -kv[1])[:8]: print(f"   {v:7.1f} FE  {k}")
    top = sorted(e["items"].items(), key=lambda kv: -val(kv[0], kv[1]))[:10]
    print("   top items:", ", ".join(f"{RN.name(i)[:28]} {q:.2f} ({val(i, q):.0f})" for i, q in top))
    return e

if __name__ == "__main__":
    F, LA = load_fit()
    print("lottery attribution:", {RN.name(i)[:30]: (k, round(r, 5), int(d)) for i, (k, r, d) in sorted(LA.items(), key=lambda kv: -kv[1][1] * price(kv[0]))[:15]})
    # Vlad's current Machines run
    vlad = Plan({"Cruising_Mechanical_Compass_%28Artifact%29": 1, "Focus_Fluorescent_Compass": 1, "Colorful_Fluorescent_Compass_%28Artifact%29": 1, "Transgression_Plunder_Compass": 1}, {}, PROFOUND)
    report(F, LA, vlad, "Vlad now: Cruising + Focus + Colorful(A) + Transgression, no tree yet")
