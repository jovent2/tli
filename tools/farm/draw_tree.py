"""Draw a constellation with a plan's picked nodes highlighted and numbered in click order (PNG via matplotlib)."""
import collections, math, os, sys, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import chart

def click_order(ck, idxs):
    nodes, adj, start = chart.graph(ck)
    parent = {start: None}; order = [start]; q = [start]
    while q:
        u = q.pop(0)
        for v in sorted(adj[u]):
            if v not in parent: parent[v] = u; order.append(v); q.append(v)
    picked = set(idxs); seq = []
    # DFS from start, spoke by spoke, only through picked nodes
    def dfs(u):
        for v in sorted(adj[u]):
            if v in picked and v not in seq and parent.get(v) == u:
                seq.append(v); dfs(v)
    dfs(start)
    return nodes, adj, start, seq

def draw(ck, idxs, out_png, title=None):
    nodes, adj, start, seq = click_order(ck, idxs)
    num = {v: i + 1 for i, v in enumerate(seq)}
    cx = [n["x"] + n["size"] / 2 for n in nodes]; cy = [-(n["y"] + n["size"] / 2) for n in nodes]
    fig, ax = plt.subplots(figsize=(15, 15)); ax.set_aspect("equal"); ax.axis("off")
    for u in adj:
        for v in adj[u]:
            if u < v:
                on = u in num and v in num or (u == start and v in num)
                ax.plot([cx[u], cx[v]], [cy[u], cy[v]], color="#f0a000" if on else "#777777", lw=4 if on else 1.2, zorder=1)
    short = collections.OrderedDict()
    for i, n in enumerate(nodes):
        r = n["size"] / 2
        picked = i in num
        if i == start: col, ec = "#ffffff", "#000000"
        elif picked: col, ec = ("#ffd27f" if n["name"] == "Micro Node" else "#ff7f2a"), "#000000"
        else: col, ec = ("#e8e8e8" if n["name"] == "Micro Node" else "#c8c8c8"), "#999999"
        ax.add_patch(Circle((cx[i], cy[i]), r, facecolor=col, edgecolor=ec, lw=2 if picked else 1, zorder=2))
        if picked:
            ax.text(cx[i], cy[i], str(num[i]), ha="center", va="center", fontsize=13 if n["name"] == "Micro Node" else 15, fontweight="bold", zorder=3)
            if n["name"] != "Micro Node":
                key = " · ".join(n["lines"]); lab = short.setdefault(key, (n["name"], []))
                lab[1].append(num[i])
        elif n["name"] != "Micro Node" and n["lines"]:
            ax.text(cx[i], cy[i], "", fontsize=6)
    ax.set_xlim(min(cx) - 120, max(cx) + 120); ax.set_ylim(min(cy) - 120, max(cy) + 120)
    name = ck.replace("_Talent_Constellation", "").replace("_", " ")
    ax.set_title(title or f"{name} — {len(num)} points (numbers = click order; orange = medium/major, yellow = micro)", fontsize=16)
    # legend of the picked medium/major nodes
    lines = []
    for key, (nm, ns) in short.items():
        t = key.split(" · "); t = [x for x in t if not x.startswith("Timemark")]
        lines.append(f"#{','.join(map(str, ns))} {nm[:22]}: " + " · ".join(t)[:150])
    micro = [i for i in num if nodes[i]["name"] == "Micro Node"]
    if micro:
        mt = collections.Counter(" · ".join(nodes[i]["lines"]) for i in micro)
        for t, c in mt.items(): lines.append(f"{c}x micro: {t[:120]}")
    fig.text(0.02, 0.01, "\n".join(textwrap.fill(l, 150) for l in lines), fontsize=9.5, va="bottom", ha="left", family="DejaVu Sans")
    plt.subplots_adjust(bottom=0.04 + 0.018 * sum(1 + len(l) // 150 for l in lines))
    fig.savefig(out_png, dpi=90, bbox_inches="tight"); plt.close(fig)
    return out_png, seq

if __name__ == "__main__":
    from vlad_plans import *
    F, LA = vlad_fit()
    A = {"Alert_Outlaw_Compass": 1, "Bandit_Dark_Surge_Compass": 1, "Phantom_Vigil_Compass": 1}
    plan, split = optimize_tree(F, LA, Plan(A, {"Flourishing_Profound_Probe": 1}, PROFOUND))
    e = evaluate(F, LA, plan); print(f"{e['net_per_min']:.0f} FE/min net {e['net']:.0f} {e['secs']:.0f}s")
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    for ck, idxs in plan.picked.items():
        png, seq = draw(ck, idxs, os.path.join(outdir, ck.replace("_Talent_Constellation", "") + ".png"))
        print(png, len(seq))
