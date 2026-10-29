"""Vlad's Profound farming plan: per-mechanic numbers from the logged CN runs, rescaled to his quantity multiplier and times.

Per mechanic variant (compass key): from runs that used it (>= 0.5/run) we take, per run, the loot value split into
  q_loot  - loot the Drop Quantity pool applies to (XD matrix) excluding jackpots
  nq_loot - loot it does not apply to (exclusive fluorescent memories, Overrealm interior, Hunting main rewards, Vorax...)
  excl    - the mechanic's exclusive jackpots (>= 1000 FE), pooled
  generic - everything else (map loot); scales with Q
  cost    - that compass, at today's price
  t_cn    - CN total map time
Vlad: Q from his own sources, time = 40 s + (t_cn - CN rush base 0.5 min) per mechanic, Machines fixed at his 3 min.
"""
import sys, os, collections, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN, mech, features as F, groups as GR, permech as PM
RN.PRICES["100300"] = {"id": "100300", "price_fe": 1.0}

NQ_ITEMS = {"Disappearing_Shadow"}                     # Machines-exclusive fluorescent memory: quantity does not apply (XD)
NQ_MECH = {"Vorax", "Sandlord", "Mistville", "FrozenCanvas"}   # whole gameplay ignores quantity (XD)
CN_BASE_MIN = 0.5
VLAD = dict(bare_min=40 / 60, machines_min=3.0, beacon=3.29, resonance=31 * 0.11)

def variant_table(min_runs=150):
    R = RN.load(); V = {}
    for r in R:
        f = F.extract(r); n = r["count"]
        if any(RN.name(i) == "Snowpaper_Fragment" for i in r["cost"]): continue
        mechs = PM.mechanics_of(r, f)
        for M in mechs:
            variants = [RN.name(i) for i, q in r["cost"].items() if RN.typ(i) in ("罗盘", "星盘") and mech.compass_family(RN.name(i)) == M and q >= 0.5] or ["(tree only)"]
            for key in variants:
                g = V.setdefault((M, key), dict(runs=0, strats=0, q=0.0, nq=0.0, excl=0.0, generic=0.0, dur=0.0, Q=0.0, tree=0.0, other_mech=0.0))
                g["runs"] += n; g["strats"] += 1; g["dur"] += r["dur_s"] * n; g["Q"] += f["Q"] * n; g["tree"] += f.get(f"t:{M}", 0) * n
                g["other_mech"] += (len(mechs) - 1) * n
                for i, qq in r["loot"].items():
                    v = RN.value(i, qq) * n; c = GR.cat(i); nm = RN.name(i)
                    if (RN.price(i) or 0) >= 1000:
                        if nm in PM.EXCL.get(M, ()): g["excl"] += v
                    elif c in PM.SIG.get(M, ()):
                        if M in NQ_MECH or nm in NQ_ITEMS or (M == "Overrealm"): g["nq"] += v
                        else: g["q"] += v
                    else: g["generic"] += v
    out = {}
    for (M, key), g in V.items():
        n = g["runs"]
        if n < min_runs: continue
        price = 0.0 if key == "(tree only)" else (RN.price(next((i for i in RN.ITEMS if RN.name(i) == key), "")) or 0.0)
        out[(M, key)] = dict(runs=n, strats=g["strats"], Q=g["Q"] / n, tree=g["tree"] / n, q=g["q"] / n, nq=g["nq"] / n, excl=g["excl"] / n,
                             generic=g["generic"] / n, t_cn=g["dur"] / n / 60, price=price, other=g["other_mech"] / n)
    return out

def vlad_Q(plunder=(), probe="Flourishing_Profound_Probe", profound_major=True, profound_micros=3, commodities_micros=0, extra_pct=0.0):
    pool = 100.0 + (30 if profound_major else 0) + 2 * profound_micros + commodities_micros + extra_pct
    if probe == "Flourishing_Profound_Probe": pool += 20
    for p in plunder: pool += {"Sinful_Plunder_Compass": 40, "Sinful_Plunder_Compass_%28Artifact%29": 80}[p]
    return (1 + pool / 100) * 2.0

def evaluate(mechs, V, plunder=(), probe="Flourishing_Profound_Probe", base_generic=45.0, base_Q=4.6, full_clear=True):
    """mechs: list of (M, variant). Returns FE/run breakdown and FE/min for Vlad."""
    Q = vlad_Q(plunder, probe)
    t = VLAD["bare_min"]; cost = VLAD["beacon"] + VLAD["resonance"] + (RN.price(next((i for i in RN.ITEMS if RN.name(i) == probe), "")) or 0.0 if probe else 0)
    for p in plunder: cost += RN.price(next(i for i in RN.ITEMS if RN.name(i) == p)) or 0
    value = base_generic * Q / base_Q if full_clear else 0.0
    rows = []
    for M, key in mechs:
        g = V[(M, key)]; s = Q / g["Q"]
        v = g["q"] * s + g["nq"] + g["excl"]
        tm = VLAD["machines_min"] if M == "Machines" else max(0.15, g["t_cn"] - CN_BASE_MIN)
        value += v; cost += g["price"]; t += tm
        rows.append((M, key, g["q"] * s, g["nq"], g["excl"], g["price"], tm))
    return dict(Q=Q, value=value, cost=cost, net=value - cost, t=t, per_min=(value - cost) / t, rows=rows)

if __name__ == "__main__":
    V = variant_table()
    print(f"{'mechanic':14s} {'variant':38s} {'price':>6s} {'runs':>6s} {'Qcn':>4s} {'tree':>4s} {'q-loot':>6s} {'nq':>5s} {'excl':>5s} {'gen':>5s} {'CNmin':>5s} {'+mech':>5s}")
    for (M, key), g in sorted(V.items(), key=lambda kv: -(kv[1]["q"] + kv[1]["nq"] + kv[1]["excl"] - kv[1]["price"])):
        print(f"{M:14s} {key[:38]:38s} {g['price']:6.1f} {g['runs']:6d} {g['Q']:4.1f} {g['tree']:4.0f} {g['q']:6.1f} {g['nq']:5.1f} {g['excl']:5.0f} {g['generic']:5.0f} {g['t_cn']:5.2f} {g['other']:5.2f}")
