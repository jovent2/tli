"""Deep Space (etor timeLabel 13) strategy ranking at today's prices — raw strategies grouped by the compass set they ran.

No column model: a group's numbers are the run-weighted loot and cost of the CN strategies that ran exactly that compass/probe set.
Items with fewer than MIN_DROPS drops in the whole group are lotteries: their value is shown separately with the drop count, so a
2-drop jackpot is visible as such; everything with enough drops to have a rate (a 2,000 FE legendary at 1 per 15 maps included) is "steady".

  python3 deepspace.py [--exclude 囚笼,狩猎] [--min-runs 60] [--top 25] [--show GROUP#]
"""
import sys, os, collections, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN

RARE_PER_MAP = 0.1      # (unused now)
MIN_DROPS = 8           # an item with fewer drops in the whole group is a lottery: shown separately with its drop count
SKIP_COST = {"Deep_Space_Beacon", "Netherrealm_resonance", "Deep_Space_Resonance"}

def short(n):
    return (n.replace("_Compass", "").replace("_Astrolabe", " Astro").replace("_Probe", " Probe").replace("%28Artifact%29", "(A)")
             .replace("_%28Artifact%29", "(A)").replace("_", " ").strip())

def signature(r):
    keys = []
    for i, q in r["cost"].items():
        n = RN.name(i)
        if n in SKIP_COST or q < 0.5: continue
        if n.endswith("Compass") or "Astrolabe" in n or "Probe" in n or "%29" in n: keys.append(n)
    return tuple(sorted(keys))

def family(r):
    return "+".join(t for t in r["talent_label"].split("、") if t and t != "幽邃")

def group(R, exclude=(), min_runs=1):
    G = collections.defaultdict(list)
    for r in R:
        if any(x in r["talent_label"] for x in exclude): continue
        G[(signature(r), family(r))].append(r)
    out = []
    for (sig, fam), rs in G.items():
        n = sum(r["count"] for r in rs)
        if n < min_runs: continue
        loot = collections.Counter(); cost = collections.Counter(); secs = 0.0
        for r in rs:
            for i, q in r["loot"].items(): loot[i] += q * r["count"]
            for i, q in r["cost"].items(): cost[i] += q * r["count"]
            secs += r["dur_s"] * r["count"]
        steady = sum(RN.value(i, q) for i, q in loot.items() if q >= MIN_DROPS) / n
        rare_items = [(RN.value(i, q) / n, i, q) for i, q in loot.items() if 0 < q < MIN_DROPS and RN.price(i)]
        rare = sum(v for v, i, q in rare_items)
        c = sum(RN.value(i, q, sold=False) for i, q in cost.items()) / n
        d = secs / n
        nets = sorted(((sum(RN.value(i, q) for i, q in r["loot"].items() if loot[i] >= MIN_DROPS) - r["cost_fe"]) / (r["dur_s"] / 60), r["count"]) for r in rs)
        out.append(dict(sig=sig, fam=fam, strategies=len(rs), runs=n, gross=steady + rare, steady=steady, rare=rare, cost=c, secs=d,
                        net_steady=steady - c, net=steady + rare - c, per_min=(steady - c) / (d / 60), per_min_all=(steady + rare - c) / (d / 60),
                        rare_items=sorted(rare_items, reverse=True)[:6], loot=loot, cost_items=cost, rs=rs, nets=nets,
                        stages=collections.Counter(r["stage"] for r in rs)))
    return out

def show(g, k=None):
    sig = " + ".join(short(s) for s in g["sig"]) or "(no compass)"
    print(f"\n## {('#%d ' % k) if k is not None else ''}{sig}  [{g['fam']}]  {g['strategies']} strategies, {g['runs']} runs, stages {dict(g['stages'])}")
    print(f"   {g['secs']:.0f} s/map | gross {g['gross']:.0f} = steady {g['steady']:.0f} + rare {g['rare']:.0f} | cost {g['cost']:.0f} | "
          f"NET steady {g['net_steady']:.0f}/map = {g['per_min']:.1f} FE/min; with rare {g['net']:.0f}/map = {g['per_min_all']:.1f}/min")
    n = g["runs"]
    print("   cost: " + ", ".join(f"{short(RN.name(i))} {q / n:.2f}x{RN.price(i) or 0:.0f}" for i, q in sorted(g["cost_items"].items(), key=lambda kv: -RN.value(kv[0], kv[1], sold=False))[:8]))
    st = sorted(((RN.value(i, q) / n, i, q) for i, q in g["loot"].items() if q >= MIN_DROPS), reverse=True)[:8]
    print("   steady: " + ", ".join(f"{short(RN.name(i))[:24]} {q / n:.2f}/map ({v:.0f})" for v, i, q in st))
    if g["rare_items"]: print("   rare:   " + ", ".join(f"{short(RN.name(i))[:24]} {q:.0f} drops ({v:.0f}/map)" for v, i, q in g["rare_items"]))
    if len(g["nets"]) > 1:
        w = [c for v, c in g["nets"]]; vs = [v for v, c in g["nets"]]
        print(f"   steady FE/min across strategies: min {vs[0]:.0f}, median {vs[len(vs) // 2]:.0f}, max {vs[-1]:.0f}")

if __name__ == "__main__":
    a = sys.argv[1:]
    ex = a[a.index("--exclude") + 1].split(",") if "--exclude" in a else ("囚笼", "狩猎")
    mr = int(a[a.index("--min-runs") + 1]) if "--min-runs" in a else 60
    top = int(a[a.index("--top") + 1]) if "--top" in a else 25
    R = RN.load(time_label="13")
    print(f"{len(R)} Deep Space strategies with details, {sum(r['count'] for r in R)} runs; prices {os.path.basename(RN.PRICE_FILE)}")
    G = sorted(group(R, ex, mr), key=lambda g: -g["per_min"])
    print(f"\n{'#':>3} {'FE/min':>6} {'+rare':>6} {'net':>5} {'cost':>5} {'s':>4} {'runs':>5} {'strat':>5}  compasses [tree]")
    for k, g in enumerate(G[:top], 1):
        print(f"{k:3d} {g['per_min']:6.1f} {g['per_min_all']:6.1f} {g['net_steady']:5.0f} {g['cost']:5.0f} {g['secs']:4.0f} {g['runs']:5d} {g['strategies']:5d}  {' + '.join(short(s) for s in g['sig'])[:70]} [{g['fam'][:18]}]")
    if "--show" in a:
        for k in a[a.index("--show") + 1].split(","): show(G[int(k) - 1], int(k))
