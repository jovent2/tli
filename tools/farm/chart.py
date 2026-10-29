"""Void Chart allocation: tree-knapsack per constellation (connected to the Initial Node), value per node from a scoring function."""
import json, os, math, collections, functools
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = json.load(open(os.path.join(ROOT, "data", "ext", "void_chart_graph.json")))

def graph(key):
    g = G[key]; nodes = g["nodes"]
    cx = [n["x"] + n["size"] / 2 for n in nodes]; cy = [n["y"] + n["size"] / 2 for n in nodes]
    def nearest(x, y): return min(range(len(nodes)), key=lambda i: math.hypot(cx[i] - x, cy[i] - y))
    adj = collections.defaultdict(set)
    for x1, y1, x2, y2 in g["edges"]:
        a, b = nearest(x1, y1), nearest(x2, y2)
        if a != b: adj[a].add(b); adj[b].add(a)
    start = next(i for i, n in enumerate(nodes) if n["name"] == "Initial Node")
    return nodes, adj, start

def best_subtree(key, value, budget):
    """Max total value of a connected set containing the start, with at most `budget` non-start nodes. Returns per-budget (value, nodes)."""
    nodes, adj, start = graph(key)
    # root the tree (constellations are trees; if a cycle exists, BFS tree is used)
    parent = {start: None}; order = [start]; q = [start]
    while q:
        u = q.pop(0)
        for v in adj[u]:
            if v not in parent: parent[v] = u; order.append(v); q.append(v)
    children = collections.defaultdict(list)
    for v, p in parent.items():
        if p is not None: children[p].append(v)
    # dp[u] = list over k (points used in u's subtree incl. u) -> (value, set)
    dp = {}
    for u in reversed(order):
        cost = 0 if u == start else 1
        cur = {cost: (value(nodes[u]) if u != start else 0.0, [u])}
        for c in children[u]:
            nxt = {}
            for k1, (v1, s1) in cur.items():
                for k2, (v2, s2) in dp[c].items():
                    k = k1 + k2
                    if k > budget: continue
                    if k not in nxt or v1 + v2 > nxt[k][0]: nxt[k] = (v1 + v2, s1 + s2)
                # also the option of not taking child c at all is already `cur` itself
                if k1 not in nxt or v1 > nxt[k1][0]: nxt[k1] = (v1, s1)
            cur = nxt
        dp[u] = cur
    res = {}
    best = (0.0, [])
    for k in range(0, budget + 1):
        if k in dp[start] and dp[start][k][0] > best[0]: best = dp[start][k]
        res[k] = best
    return res, nodes
