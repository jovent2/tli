"""The plans for Vlad, priced with mechanic times scaled to his speed (bare map 40 s vs CN 58 s), full node lists."""
import sys, collections
from search import *
import plan2

def vlad_fit():
    F, LA = load_fit()
    scale = 40.0 / 58.0
    for k, v in list(F["T"].items()):
        if k != "generic" and k not in VLAD_TIME: F["T"][k] = v * scale
    plan2.MIN_TIME = 7.0
    return F, LA

def show(F, LA, name, comp, prob):
    plan, split = optimize_tree(F, LA, Plan(comp, prob, PROFOUND)); e = evaluate(F, LA, plan)
    print(f"\n## {name}\n**{e['net_per_min']:.0f} FE/min** — net {e['net']:.0f}/map, gross {e['gross']:.0f}, cost {e['cost']:.0f}, {e['secs']:.0f} s/map (pool +{e['pool']:.0f}%, lottery EV {e['lottery']:.0f})")
    print("compasses: " + ", ".join(k.replace('_', ' ').replace('%28', '(').replace('%29', ')') for k in comp) + (" · probe: " + ", ".join(k.replace('_', ' ') for k in prob) if prob else ""))
    print("by source: " + ", ".join(f"{k.replace('_', ' ').replace('%28', '(').replace('%29', ')')[:34]} {v:.0f}" for k, v in sorted(e["by_col"].items(), key=lambda kv: -kv[1])[:6]))
    top = sorted(e["items"].items(), key=lambda kv: -val(kv[0], kv[1]))[:10]
    print("items/map: " + ", ".join(f"{RN.name(i).replace('_', ' ')[:28]} {q:.2f} ({val(i, q):.0f} FE)" for i, q in top))
    c, names = describe_tree(plan)
    print(f"tree ({sum(c.values())} Star + Profound 4 Prime/25 Star): " + ", ".join(f"{k.replace('generic:', '')} {v}" for k, v in c.items()))
    for m, nn in names.items():
        print(f"  - {m.replace('generic:', '')}: " + "; ".join(f"{v}x {t[:95]}" for t, v in nn.most_common(12)))
    return e

if __name__ == "__main__":
    F, LA = vlad_fit()
    show(F, LA, "A. Outlaw + Dark Surge + Vigil + Lunaria (the stack)", {"Alert_Outlaw_Compass": 1, "Bandit_Dark_Surge_Compass": 1, "Phantom_Vigil_Compass": 1, "Lunaria_Compass": 1}, {"Flourishing_Profound_Probe": 1})
    show(F, LA, "A-cheap. same with base compasses (11 FE/map)", {"Outlaw_Compass": 1, "Bandit_Dark_Surge_Compass": 1, "Vigil_Compass": 1, "Lunaria_Compass": 1}, {"Flourishing_Profound_Probe": 1})
    show(F, LA, "B. Machines as you run it", {"Cruising_Mechanical_Compass_%28Artifact%29": 1, "Focus_Fluorescent_Compass": 1, "Colorful_Fluorescent_Compass_%28Artifact%29": 1, "Transgression_Plunder_Compass": 1}, {})
    show(F, LA, "C. Clockwork Ballet compass farm", {"Collection_Doll_Astrolabe": 1, "Vast_Ecliptic_Astrolabe": 1, "Ecliptic_Astrolabe": 1, "Sinful_Plunder_Compass": 1}, {"Compass_Profound_Probe": 1})
    show(F, LA, "D. Safari compass farm", {"Revelation_Hunting_Astrolabe": 1, "Vast_Ecliptic_Astrolabe": 1, "Ecliptic_Astrolabe": 1, "Sinful_Plunder_Compass_%28Artifact%29": 1}, {"Compass_Profound_Probe": 1})

def spoke_order(plan):
    """Print the plan's picked nodes per constellation in click order (BFS from the Initial Node), spoke by spoke."""
    import chart
    for ck, idxs in getattr(plan, "picked", {}).items():
        nodes, adj, start = chart.graph(ck)
        parent = {start: None}; order = [start]; q = [start]
        while q:
            u = q.pop(0)
            for vv in sorted(adj[u]):
                if vv not in parent: parent[vv] = u; order.append(vv); q.append(vv)
        spokes = collections.defaultdict(list)
        for vv in idxs:
            u = vv
            while parent[u] != start: u = parent[u]
            spokes[u].append(vv)
        print(f"\n[{ck.replace('_Talent_Constellation', '')}] {len(idxs)} points")
        for s, vs in spokes.items():
            vs = sorted(vs, key=lambda x: order.index(x)); seq = []
            for vv in vs:
                t = " · ".join(nodes[vv]["lines"])
                if seq and seq[-1][0] == t: seq[-1][1] += 1
                else: seq.append([t, 1])
            print("  spoke: " + "  ->  ".join(f"{t[:72]}{' x' + str(c) if c > 1 else ''}" for t, c in seq))
