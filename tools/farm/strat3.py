#!/usr/bin/env python3
"""The evaluator and the strat search on checkpoint 1c (tools/farm/model.py, data/ext/model/checkpoint1c.json).

Rule: a candidate exists only if its line belongs to a class the card has an exponent for (flat pool / additional, per the loot-class
rulebook docs/loot_classes.md). Per setup: every item of every mechanic present = base x pool^a x additional^b from the text of that
setup (compasses, DS affixes, tree lines, phase pets), x price, summed; FE from the lead mechanic's card (vigil > outlaw > lunaria >
darksurge) with the other present mechanics' measured presence effect on map FE; the unfitted rest of a family's loot as its CN
average (steady vs lottery). Minus compass cost, over seconds at Vlad's speed. Tree: DQ lines of Outlaw / Afterlight / Lunaria /
Profound / Commodities, cheapest paths from each root, knapsack over the point budget. Overrealm: out of the search (his loop with its
measured block is the reference line only).

  python3 tools/farm/strat3.py [--budget 96] [--md out.md]
"""
import argparse
import collections
import glob
import itertools
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN  # noqa: E402
import model as M  # noqa: E402
import ds_scan as D  # noqa: E402

CARD = json.load(open(os.path.join(RN.EXT, "model", "checkpoint1c.json")))
BLOCK = json.load(open(os.path.join(RN.EXT, "model", "overrealm_block.json")))
BYNAME = {RN.name(i): i for i in RN.ITEMS}
OWNER = {"component": "outlaw", "void_divinity_crafting_material": "vigil", "hero_memory_revival_material": "lunaria", "corrosion_material": "darksurge"}
PRIMARY = ["vigil", "outlaw", "lunaria", "darksurge"]
PRESENCE = {"Alert_Outlaw_Compass": "outlaw", "All-Evil_Vigil_Compass": "vigil", "Evernight_Vigil_Compass": "vigil", "Lunar_Stele_Lunaria_Compass": "lunaria", "Divine_Warrior_Dark_Surge_Compass": "darksurge"}
TOWN, BASE_S = 20.0, 108.0
PHASE_S = {"Evernight_Vigil_Compass": 19.0, "Alert_Outlaw_Compass": 5.0}
NEVER_RUN = {"lunaria": 1.2, "darksurge": 1.2}
SLOTS = 4
VLAD_NODES = {"outlaw": {"+1% additional Drop Quantity for all Security": 18, "+6% additional Drop Quantity for all Security": 1, "Super Sonic": 1, "for every 10 Escort Bodyguard": 1, "+30% additional Drop Quantity for all Security personnel after": 1},
              "vigil": {"+1% additional Drop Quantity for the Vigil": 15, "+8% additional Drop Quantity for the Vigil": 1, "+15% additional Drop Quantity for the Vigil": 1, "During White Night Mode, +12%": 1}}
PETS = {f: M.family_pets(M.FAMILIES[f]) for f in M.FAMILIES}
OTHER = {}       # family -> (steady, lottery) FE/map of items not on the card, CN run-weighted


def load_other():
    R = D.load(M.STAGES)
    R = [r for r in R if not any(x in r["talent_label"] for x in ("囚笼", "玩偶", "机械", "巨力"))]
    for f, fam in M.FAMILIES.items():
        rows = [r for r in R if any(c in {RN.name(i) for i, q in r["cost"].items() if q >= 0.5} for c in fam["compasses"])]
        n = sum(r["count"] for r in rows); qty = collections.Counter(); vals = collections.Counter()
        for r in rows:
            for i, q in r["loot"].items():
                qty[i] += q * r["count"] / n; vals[i] += RN.value(i, q) * r["count"] / n
        fitted = set(CARD[f])
        OTHER[f] = (sum(v for i, v in vals.items() if i not in fitted and qty[i] >= 0.125), sum(v for i, v in vals.items() if i not in fitted and qty[i] < 0.125))


def cname(c):
    return c.replace("_Compass", "").replace("_%28Artifact%29", " (A)").replace("_Deep_Space_Probe", " probe").replace("_", " ")


def nodes_of(setup):
    return collections.Counter({(f, k): v for f, d in setup["nodes"].items() for k, v in d.items()})


def predict(fname, item, setup, presence=False):
    c = CARD[fname][item]["coef"]; nodes = nodes_of(setup)
    cost = dict(setup["comp"]); cost["Deep_Space_Resonance"] = 2 * setup["dsres"]
    pool, gen, mech = M.setup_mult(fname, nodes, cost, item, PETS[fname], split=True)
    gen *= setup.get("add_all", 1.0)
    lg = c["const"][0] + c["a"][0] * math.log(pool)
    lg += (c["b_gen"][0] * math.log(gen) + c["b_mech"][0] * math.log(mech)) if item == M.FE else c["b"][0] * math.log(gen * mech)
    if presence:                              # other mechanics present: their measured effect on this card's map FE
        for comp, fam in PRESENCE.items():
            if fam != fname and comp in c and cost.get(comp, 0):
                lg += c[comp][0] * cost[comp]
    return math.exp(lg)


def families(setup):
    return [f for f in PRIMARY if any(c in setup["comp"] for c in M.FAMILIES[f]["compasses"])]


def simulate(setup, overrealm=None):
    fams = families(setup)
    if not fams:
        return None
    prim = fams[0]; items = {}
    for f in fams:
        for item in CARD[f]:
            if item == M.FE or item in items:
                continue
            owner = OWNER.get(M.loot_type(item))
            if owner and owner != f:
                continue                      # another mechanic's loot: its own card, or nothing if it is absent
            if not owner and f != prim:
                continue
            items[item] = predict(f, item, setup)
    items[M.FE] = predict(prim, M.FE, setup, presence=True)
    steady = sum(RN.value(i, q) for i, q in items.items()) + OTHER[prim][0]; lottery = OTHER[prim][1]
    secs = BASE_S + sum(PHASE_S.get(c, 0.0) * q for c, q in setup["comp"].items()); flags = []
    for f in fams:
        if f in NEVER_RUN:
            secs *= NEVER_RUN[f]; flags.append(f"{f}: card off by x2 per player, time CN x{NEVER_RUN[f]}")
    cost = sum(RN.value(BYNAME[c], q, sold=False) for c, q in setup["comp"].items() if c in BYNAME) + RN.value(BYNAME["Deep_Space_Beacon"], 1, sold=False) + 2 * setup["dsres"] * RN.price(BYNAME["Deep_Space_Resonance"])
    if overrealm:
        steady += overrealm["gross"]; secs += overrealm["secs"]; cost += RN.value(BYNAME["Shadow_Overrealm_Compass"], 1, sold=False)
    net = steady - cost
    return dict(items=items, steady=steady, lottery=lottery, cost=cost, net=net, secs=secs, per_min=net / ((secs + TOWN) / 60), per_min_lot=(net + lottery) / ((secs + TOWN) / 60), flags=flags)


def clone(s, **kw):
    t = json.loads(json.dumps(s)); t.update(kw); return t


def top_items(sim, k=5):
    return ", ".join(f"{RN.name(i).replace('_', ' ')[:22]} {q:.2f} ({RN.value(i, q):.0f})" for i, q in sorted(sim["items"].items(), key=lambda kv: -RN.value(kv[0], kv[1]))[:k])


# ------------------------------------------------------------------ Void Chart
CONS = {
    "Outlaw": dict(fam="outlaw", micro="+1% additional Drop Quantity for all Security personnel",
                   mediums={"+6%": "+6% additional Drop Quantity for all Security", "Super Sonic": "Super Sonic", "Hyper-Hardened": "Hyper-Hardened",
                            "Oppressive": "+30% additional Drop Quantity for all Security personnel after", "Imperious": "for every 10 Escort Bodyguard"},
                   exclusive=[("Super Sonic", "Hyper-Hardened")]),
    "Afterlight": dict(fam="vigil", micro="+1% additional Drop Quantity for the Vigil",
                       mediums={"+8%": "+8% additional Drop Quantity for the Vigil", "+15%": "+15% additional Drop Quantity for the Vigil",
                                "White Night": "White Night Mode can appear", "WN +12%": "During White Night Mode, +12%"}, requires={"WN +12%": "White Night"}),
    "Lunaria": dict(fam="lunaria", micro="+1% additional Drop Quantity for Lunaria gameplay",
                    mediums={"+4%": "+4% additional Drop Quantity for Lunaria gameplay", "+6%": "+6% additional Drop Quantity for Lunaria gameplay"}),
    "Profound": dict(fam="profound", micro="In Netherrealm stages, +2% Drop Quantity", mediums={"+12% additional": "+12% additional Drop Quantity"}, extra_cost={"+12% additional": 25}),
    "Commodities": dict(fam="commodities", micro="In Netherrealm stages, +1% Drop Quantity", mediums={}),
}


def graph(con):
    g = RN.GRAPH[f"{con}_Talent_Constellation"]; nodes = g["nodes"]
    center = {(n["x"] + n["size"] / 2, n["y"] + n["size"] / 2): n["i"] for n in nodes}
    adj = collections.defaultdict(set)
    for e in g["edges"]:
        a, b = center.get((e[0], e[1])), center.get((e[2], e[3]))
        if a is not None and b is not None:
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
    return best


def curve(con, spec):
    nodes, adj = graph(con); text = {n["i"]: " / ".join(n["lines"]) for n in nodes}
    micros = {i for i, t in text.items() if spec["micro"] in t and nodes[i]["name"] == "Micro Node"}
    med = {k: next(i for i, t in text.items() if sub in t and nodes[i]["name"] != "Micro Node") for k, sub in spec["mediums"].items()}
    out = []; keys = list(spec["mediums"])
    for r in range(len(keys) + 1):
        for subset in itertools.combinations(keys, r):
            if any(a in subset and b in subset for a, b in spec.get("exclusive", [])) or any(k in subset and req not in subset for k, req in spec.get("requires", {}).items()):
                continue
            tree = steiner(adj, [med[k] for k in subset])
            if tree is None:
                continue
            extra = sum(spec.get("extra_cost", {}).get(k, 0) for k in subset); tree = set(tree)
            while True:
                counts = {spec["micro"]: len(tree & micros)}
                for k in subset:
                    counts[spec["mediums"][k]] = 1
                out.append((len(tree) - 1 + extra, counts, frozenset(tree), tuple(subset)))
                frontier = {v for u in tree for v in adj[u] if v not in tree}
                cand = [v for v in frontier if v in micros]
                if cand:
                    tree.add(cand[0]); continue
                def behind(v):
                    seen = {v}; q = [v]
                    for _ in range(2):
                        q = [w for u in q for w in adj[u] if w not in tree and w not in seen and not seen.add(w)]
                    return sum(1 for w in seen if w in micros)
                if not frontier:
                    break
                v = max(frontier, key=behind)
                if behind(v) == 0:
                    break
                tree.add(v)
    return out, text


def path_text(tree, con, text):
    nodes, adj = graph(con); sub = {u: [v for v in adj[u] if v in tree] for u in tree}
    order = []; seen = {0}; q = [0]
    for u in q:
        order.append(u)
        for v in sub[u]:
            if v not in seen:
                seen.add(v); q.append(v)
    return [f"{i}:{(text[i][:60] + '…') if len(text[i]) > 60 else text[i]}" for i in order if i != 0]


CURVES = {}


def value_curve(setup, con, spec, budget):
    if con not in CURVES:
        CURVES[con] = curve(con, spec)
    pts_curve, text = CURVES[con]
    base = simulate(clone(setup, nodes={}))["net"]; best = {}
    for pts, counts, tree, subset in pts_curve:
        if pts > budget:
            continue
        s = clone(setup, nodes={spec["fam"]: counts})
        if "+12% additional Drop Quantity" in counts:
            s["add_all"] = 1.12
        v = simulate(s)["net"] - base
        if pts not in best or v > best[pts][0]:
            best[pts] = (v, counts, tree, subset)
    run = None
    for p in sorted(best):
        if run is None or best[p][0] > run[0]:
            run = best[p]
        else:
            best[p] = run
    return best, text


def allocate(setup, budget):
    curves = {}; texts = {}
    for con, spec in CONS.items():
        if spec["fam"] in M.FAMILIES and not any(c in setup["comp"] for c in M.FAMILIES[spec["fam"]]["compasses"]):
            continue
        curves[con], texts[con] = value_curve(setup, con, spec, budget)
    dp = {0: (0.0, {})}
    for con in curves:
        nd = dict(dp)
        for spent, (v, picks) in dp.items():
            for p, (dv, counts, tree, subset) in curves[con].items():
                if p == 0 or spent + p > budget:
                    continue
                if spent + p not in nd or v + dv > nd[spent + p][0]:
                    nd[spent + p] = (v + dv, {**picks, con: (p, dv, counts, tree, subset)})
        dp = nd
    spent, (v, picks) = max(dp.items(), key=lambda kv: kv[1][0])
    nodes = {}; add_all = 1.0
    for con, (p, dv, counts, tree, subset) in picks.items():
        nodes.setdefault(CONS[con]["fam"], {}).update(counts)
        if "+12% additional Drop Quantity" in counts:
            add_all = 1.12
    s = clone(setup, nodes=nodes); s["add_all"] = add_all
    return spent, picks, simulate(s), texts, s


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=96)
    ap.add_argument("--md", default=None)
    a = ap.parse_args(argv)
    load_other()
    md = [f"Strat search on checkpoint 1c — prices {os.path.basename(RN.PRICE_FILE)}, Fright {M.FRIGHT}, {SLOTS} compass slots + probe + beacon, budget {a.budget} points, net FE per in-map minute (+{TOWN:.0f} s town)"]
    # reference: his loop as run, with the measured Overrealm block
    loop = dict(comp={"Evernight_Vigil_Compass": 1.0, "Generous_Elite_Compass": 1.0, "Sinful_Plunder_Compass": 1.0, "Flourishing_Deep_Space_Probe": 1.0}, dsres=0, nodes=VLAD_NODES)
    s0 = simulate(loop, overrealm=BLOCK)
    md.append(f"\nReference, his loop as run (Evernight + Shadow Overrealm + Generous + Sinful + Flourishing, his tree; Overrealm = his measured block {BLOCK['gross']:.0f} FE / {BLOCK['secs']:.0f} s): "
              f"card net {s0['net']:.0f}/map, {s0['per_min']:.1f}/min (he measures 123 and 34); items: {top_items(s0)}")
    # 1. compass search with his tree
    mechs = []
    singles = ["Alert_Outlaw_Compass", "Evernight_Vigil_Compass", "All-Evil_Vigil_Compass", "Lunar_Stele_Lunaria_Compass", "Divine_Warrior_Dark_Surge_Compass"]
    for k in (1, 2, 3):
        for combo in itertools.combinations(singles, k):
            if sum(1 for c in combo if "Vigil" in c) > 1:
                continue
            mechs.append(combo)
    out = []
    for mech, el, si, pr in itertools.product(mechs, [(), ("Generous_Elite_Compass",), ("Bountiful_Elite_Compass",)], [(), ("Sinful_Plunder_Compass",), ("Sinful_Plunder_Compass_%28Artifact%29",)], [(), ("Flourishing_Deep_Space_Probe",)]):
        if len(mech) + len(el) + len(si) > SLOTS:
            continue
        for dsres in (0, 2):
            s = dict(comp={c: 1.0 for c in mech + el + si + pr}, dsres=dsres, nodes=VLAD_NODES)
            sim = simulate(s)
            out.append((sim["per_min"], s, sim))
    out.sort(key=lambda t: -t[0])
    md.append(f"\n# Compass search with his current tree: {len(out)} setups")
    md.append("rank | /min | +lottery | net/map | s | FE | cost | setup")
    for k, (pm, s, sim) in enumerate(out[:25]):
        md.append(f"{k + 1:2d} | {pm:5.1f} | {sim['per_min_lot']:5.1f} | {sim['net']:5.0f} | {sim['secs'] + TOWN:4.0f} | {sim['items'][M.FE]:4.0f} | {sim['cost']:4.0f} | " + ", ".join(cname(c) for c in s["comp"]) + f", DS x{s['dsres']}" + (" | " + "; ".join(sim["flags"]) if sim["flags"] else ""))
    best_per = {}
    for pm, s, sim in out:
        key = tuple(sorted(c for c in s["comp"] if c in PRESENCE))
        best_per.setdefault(key, (pm, s, sim))
    md.append("\n## Best per mechanic set (his tree)")
    for key, (pm, s, sim) in sorted(best_per.items(), key=lambda kv: -kv[1][0]):
        md.append(f"{pm:5.1f}/min (+lot {sim['per_min_lot']:5.1f}) | {' + '.join(cname(c) for c in key):50s} | with " + (", ".join(cname(c) for c in s["comp"] if c not in key) or "nothing") + f", DS x{s['dsres']} | {top_items(sim, 4)}" + (" | " + "; ".join(sim["flags"]) if sim["flags"] else ""))
    # 2. tree search on the best setup of each mechanic set
    md.append(f"\n# Tree search ({a.budget} points, DQ lines only; unpriced nodes at 0; Profound +12% = 27 points assumed) on the best compass setup of each mechanic set")
    md.append("rank | /min with tree | /min his tree | net/map | points | setup | tree")
    res = []
    for key, (pm, s, sim) in sorted(best_per.items(), key=lambda kv: -kv[1][0])[:10]:
        spent, picks, sim2, texts, s2 = allocate(clone(s, nodes={}), a.budget)
        res.append((sim2["per_min"], s, spent, picks, sim2, pm, texts))
    res.sort(key=lambda t: -t[0])
    for k, (pm2, s, spent, picks, sim2, pm, texts) in enumerate(res):
        summary = "; ".join(f"{con} {p}pt (+{dv:.0f}): " + ", ".join(subset) + f" + {counts.get(CONS[con]['micro'], 0)} micros" for con, (p, dv, counts, tree, subset) in picks.items())
        md.append(f"{k + 1:2d} | {pm2:5.1f} | {pm:5.1f} | {sim2['net']:5.0f} | {spent:3d} | " + ", ".join(cname(c) for c in s["comp"]) + f", DS x{s['dsres']} | {summary}" + (" | " + "; ".join(sim2["flags"]) if sim2["flags"] else ""))
    md.append("\n# The trees, node by node (index:text from the Initial Node outward), top 3")
    for pm2, s, spent, picks, sim2, pm, texts in res[:3]:
        md.append(f"\n## {pm2:.1f}/min — " + ", ".join(cname(c) for c in s["comp"]) + f", DS x{s['dsres']} — {spent} points; items: {top_items(sim2)}")
        for con, (p, dv, counts, tree, subset) in picks.items():
            md.append(f"  {con} ({p} points, +{dv:.0f} FE/map): " + " -> ".join(path_text(tree, con, texts[con])))
    text = "\n".join(md); print(text)
    if a.md:
        open(a.md, "w").write(text + "\n")


if __name__ == "__main__":
    main()
