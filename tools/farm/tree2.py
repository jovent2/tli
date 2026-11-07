#!/usr/bin/env python3
"""Step 2b: the Void Chart search on top of strat2's simulator. For each candidate compass set, allocate the point budget over the
constellations whose lines the model can price (Outlaw, Afterlight, Lunaria, Profound, Commodities) and report the best trees as
explicit node paths from each constellation's Initial Node.

Per constellation: every subset of its priced mediums -> cheapest connected subtree from the root containing them (Steiner, nearest-
terminal heuristic over every terminal order), then grow it one node at a time, always the adjacent node that adds the most priced
micros per point (a non-priced node is taken only to reach micros behind it). That gives a curve points -> node set -> line counts.
Curves are priced through strat2.simulate on the compass set, then combined across constellations by a knapsack over points.
Nodes the model cannot price (goblins, coffins, "more likely Warlock", spawn rates, Bounty refreshes) are worth 0 here: not "useless",
unknown. Profound +12% additional costs its micro + the node + 25 Star Talents = 27 points (assumption: Star Talents are tree points;
0 of 467 CN Deep Space players take it). Profound +25% / -4 attempts excluded (he dies 0.5 per map on 6 attempts).

  python3 tools/farm/tree2.py [--budget 96] [--sets N] [--md out.md]
"""
import argparse
import collections
import itertools
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN  # noqa: E402
import model_cp2 as M  # noqa: E402
import strat2 as S  # noqa: E402

# priced lines per constellation: (substring of the node text, family key for the simulator, kind)
CONS = {
    "Outlaw": dict(fam="outlaw", micro="+1% additional Drop Quantity for all Security personnel",
                   mediums={"+6%": "+6% additional Drop Quantity for all Security", "Super Sonic": "Super Sonic", "Hyper-Hardened": "Hyper-Hardened",
                            "Oppressive": "+30% additional Drop Quantity for all Security personnel after", "Imperious": "for every 10 Escort Bodyguard"},
                   exclusive=[("Super Sonic", "Hyper-Hardened")]),
    "Afterlight": dict(fam="vigil", micro="+1% additional Drop Quantity for the Vigil",
                       mediums={"+8%": "+8% additional Drop Quantity for the Vigil", "+15%": "+15% additional Drop Quantity for the Vigil",
                                "White Night": "White Night Mode can appear", "WN +12%": "During White Night Mode, +12%"},
                       requires={"WN +12%": "White Night"}),
    "Lunaria": dict(fam="lunaria", micro="+1% additional Drop Quantity for Lunaria gameplay",
                    mediums={"+4%": "+4% additional Drop Quantity for Lunaria gameplay", "+6%": "+6% additional Drop Quantity for Lunaria gameplay"}),
    "Profound": dict(fam="profound", micro="In Netherrealm stages, +2% Drop Quantity", mediums={"+12% additional": "+12% additional Drop Quantity"}, extra_cost={"+12% additional": 25}),
    "Commodities": dict(fam="commodities", micro="In Netherrealm stages, +1% Drop Quantity", mediums={}),
}


def graph(con):
    g = RN.GRAPH[f"{con}_Talent_Constellation"]
    nodes = g["nodes"]
    center = {(n["x"] + n["size"] / 2, n["y"] + n["size"] / 2): n["i"] for n in nodes}
    adj = collections.defaultdict(set)
    for e in g["edges"]:
        a, b = center.get((e[0], e[1])), center.get((e[2], e[3]))
        if a is None or b is None:
            continue
        adj[a].add(b); adj[b].add(a)
    return nodes, adj


def bfs(adj, sources):
    dist = {s: 0 for s in sources}; prev = {}; q = list(sources)
    for u in q:
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1; prev[v] = u; q.append(v)
    return dist, prev


def steiner(adj, terminals):
    """Cheapest connected set containing node 0 and the terminals: nearest-terminal growth, best over every terminal order."""
    best = None
    for order in itertools.permutations(terminals):
        tree = {0}
        for t in order:
            if t in tree:
                continue
            dist, prev = bfs(adj, list(tree))
            if t not in dist:
                tree = None; break
            u = t
            while u not in tree:
                tree.add(u); u = prev[u]
        if tree is not None and (best is None or len(tree) < len(best)):
            best = set(tree)
        if len(terminals) > 5:
            break
    return best


def curve(con, spec):
    """-> list of (points, counts dict, node set) for every medium subset and micro count."""
    nodes, adj = graph(con)
    text = {n["i"]: " / ".join(n["lines"]) for n in nodes}
    micros = {i for i, t in text.items() if spec["micro"] in t and nodes[i]["name"] == "Micro Node"}
    med_nodes = {k: next(i for i, t in text.items() if sub in t and nodes[i]["name"] != "Micro Node") for k, sub in spec["mediums"].items()}
    out = []
    keys = list(spec["mediums"])
    for r in range(len(keys) + 1):
        for subset in itertools.combinations(keys, r):
            if any(a in subset and b in subset for a, b in spec.get("exclusive", [])):
                continue
            if any(k in subset and req not in subset for k, req in spec.get("requires", {}).items()):
                continue
            tree = steiner(adj, [med_nodes[k] for k in subset])
            if tree is None:
                continue
            extra = sum(spec.get("extra_cost", {}).get(k, 0) for k in subset)
            tree = set(tree)
            while True:
                pts = len(tree) - 1 + extra
                counts = {spec["micro"]: len(tree & micros)}
                for k in subset:
                    counts[spec["mediums"][k]] = 1
                out.append((pts, counts, frozenset(tree), tuple(subset)))
                # grow: adjacent micro first; else the adjacent node with the most micros within 2 steps behind it
                frontier = {v for u in tree for v in adj[u] if v not in tree}
                if not frontier:
                    break
                cand = [v for v in frontier if v in micros]
                if cand:
                    tree.add(cand[0]); continue
                def behind(v):
                    seen = {v}; q = [v]
                    for _ in range(2):
                        q = [w for u in q for w in adj[u] if w not in tree and w not in seen and not seen.add(w)]
                    return sum(1 for w in seen if w in micros)
                v = max(frontier, key=behind)
                if behind(v) == 0:
                    break
                tree.add(v)
    return out, text


def path_text(tree, con, text):
    """The node set as a readable path from the Initial Node (BFS order)."""
    nodes, adj = graph(con)
    sub = {u: [v for v in adj[u] if v in tree] for u in tree}
    order = []; seen = {0}; q = [0]
    for u in q:
        order.append(u)
        for v in sub[u]:
            if v not in seen:
                seen.add(v); q.append(v)
    short = lambda t: (t[:70] + "…") if len(t) > 70 else t  # noqa: E731
    return [f"{i}:{short(text[i]) or 'Initial'}" for i in order if i != 0]


def value_curve(setup, block, con, spec, pts_cap):
    """points -> (best net/map, counts, tree) for this constellation on this compass set (others at zero)."""
    pts_curve, text = curve(con, spec)
    base = S.simulate(S.clone(setup, nodes={}), block)["net"]
    best = {}
    for pts, counts, tree, subset in pts_curve:
        if pts > pts_cap:
            continue
        s = S.clone(setup, nodes={spec["fam"]: counts})
        if "+12% additional Drop Quantity" in counts:
            s["add_all"] = 1.12
        v = S.simulate(s, block)["net"] - base
        if pts not in best or v > best[pts][0]:
            best[pts] = (v, counts, tree, subset)
    # monotone: more points never worse (you can leave them unspent)
    pts_sorted = sorted(best)
    run = None
    for p in pts_sorted:
        if run is None or best[p][0] > run[0]:
            run = best[p]
        else:
            best[p] = run
    return best, text


def allocate(setup, block, budget):
    curves = {}; texts = {}
    for con, spec in CONS.items():
        if spec["fam"] in ("outlaw", "vigil", "lunaria") and not any(c in setup["comp"] for c in M.FAMILIES[spec["fam"]]["compasses"]):
            continue
        curves[con], texts[con] = value_curve(setup, block, con, spec, budget)
    # knapsack over constellations
    cons = list(curves)
    dp = {0: (0.0, {})}
    for con in cons:
        nd = dict(dp)
        for spent, (v, picks) in dp.items():
            for p, (dv, counts, tree, subset) in curves[con].items():
                if p == 0 or spent + p > budget:
                    continue
                tot = v + dv
                if spent + p not in nd or tot > nd[spent + p][0]:
                    nd[spent + p] = (tot, {**picks, con: (p, dv, counts, tree, subset)})
        dp = nd
    spent, (v, picks) = max(dp.items(), key=lambda kv: kv[1][0])
    # exact value of the combination (the knapsack adds per-constellation gains; interactions are multiplicative, recompute)
    nodes = {}; add_all = 1.0
    for con, (p, dv, counts, tree, subset) in picks.items():
        fam = CONS[con]["fam"]; nodes.setdefault(fam, {}).update(counts)
        if "+12% additional Drop Quantity" in counts:
            add_all = 1.12
    s = S.clone(setup, nodes=nodes); s["add_all"] = add_all
    return spent, picks, S.simulate(s, block), texts


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=96)
    ap.add_argument("--sets", type=int, default=10)
    ap.add_argument("--md", default=None)
    ap.add_argument("--no-extras", action="store_true", help="leave out the text-priced Strength in Numbers / Transgression")
    a = ap.parse_args(argv)
    if a.no_extras:
        S.TEXT_GENERIC.clear()
    block = json.load(open(S.BLOCK_FILE))
    md = [f"Void Chart search — budget {a.budget} points, prices {os.path.basename(RN.PRICE_FILE)}, model checkpoint 2, Fright {M.FRIGHT}; the compass sets are the best per mechanic set from strat2's search, each re-optimised with its tree"]
    # candidate compass sets: strat2's search, best per mechanic set, plus his loop
    seen = set(); cands = []
    for pm, s, sim in S.search(block, []):
        key = tuple(sorted(c for c in s["comp"] if any(c in M.FAMILIES[f]["compasses"] for f in M.FAMILIES))) + (("Overrealm",) if s["overrealm"] else ())
        if key in seen:
            continue
        seen.add(key); cands.append(s)
        if len(cands) >= a.sets:
            break
    cands.append(S.vlad_loop())
    results = []
    for s in cands:
        s0 = S.clone(s, nodes={}); base = S.simulate(s0, block)
        spent, picks, sim, texts = allocate(s0, block, a.budget)
        results.append((sim["per_min"], s, spent, picks, sim, base, texts))
    results.sort(key=lambda t: -t[0])
    md.append("\nrank | /min with tree | /min no tree | net/map | points | compass set | tree summary")
    for k, (pm, s, spent, picks, sim, base, texts) in enumerate(results):
        summary = "; ".join(f"{con} {p}pt (+{dv:.0f}): " + ", ".join(f"{kk}" for kk in subset) + f" + {counts.get(CONS[con]['micro'], 0)} micros" for con, (p, dv, counts, tree, subset) in picks.items())
        md.append(f"{k + 1:2d} | {pm:5.1f} | {base['per_min']:5.1f} | {sim['net']:5.0f} | {spent:3d} | " + ", ".join(S.cname(c) for c in s["comp"]) + f", DS x{s['dsres']}" + (", Overrealm" if s.get("overrealm") else "") + f" | {summary}")
    md.append("\n# The trees, node by node (index:text, from the Initial Node outward), for the top 3")
    for pm, s, spent, picks, sim, base, texts in results[:3]:
        md.append(f"\n## {pm:.1f}/min — " + ", ".join(S.cname(c) for c in s["comp"]) + f", DS x{s['dsres']}" + (", Overrealm" if s.get("overrealm") else "") + f" — {spent} points; items: {S.top_items(sim)}")
        for con, (p, dv, counts, tree, subset) in picks.items():
            md.append(f"  {con} ({p} points, +{dv:.0f} FE/map): " + " -> ".join(path_text(tree, con, texts[con])))
    text = "\n".join(md); print(text)
    if a.md:
        open(a.md, "w").write(text + "\n")


if __name__ == "__main__":
    main()
