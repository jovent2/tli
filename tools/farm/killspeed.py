#!/usr/bin/env python3
"""Does killing drones fast cost loot? Drone lifetimes from the game log vs Secrets / Shadows per drone.

Drones are NpcId 1052033 ("Drop Prop Debug:create monster NpcId=1052033,eId=..." at spawn, rarity 1); every death plays
'..._Elite_Mechanic_Drones_Die' (no entity id), so lifetimes pair deaths to spawns first-in-first-out (spawn groups share a timestamp).
Per map: share of drones dead within 2.5 s of spawning, median lifetime; then log(Secrets per copy per drone) on each (day dummies,
the +30% drone card and Transgression as controls), and Shadow drops per 1,000 drones by thirds of the fast-kill share.
Usage: python3 -I tools/farm/killspeed.py LOG [LOG ...]
"""
import bisect
import collections
import datetime as dt
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gamelog as G  # noqa: E402
import quantity as Q  # noqa: E402

DRONE = "create monster NpcId=1052033"


def lifetimes(paths):
    ev = []
    for path in paths:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.startswith("["):
                    continue
                if DRONE in line:
                    ev.append((G.ts(line), 0))
                elif "Drones_Die'" in line and "requested row 'Play" in line:
                    ev.append((G.ts(line), 1))
    ev.sort(key=lambda x: (x[0], x[1]))
    alive, out = collections.deque(), []
    for t, k in ev:
        if k == 0:
            if alive and (t - alive[-1]).total_seconds() > 120:
                alive.clear()
            alive.append(t)
        else:
            out.append((t, (t - alive.popleft()).total_seconds() if alive else None))
    return out


def main(paths):
    M = Q.load(paths)
    D = lifetimes(paths)
    dts = [d[0] for d in D]
    L_all = [L for t, L in D if L is not None]
    print(f"{len(D)} drone deaths, {len(L_all)} paired; shortest lifetime {min(L_all):.2f} s, "
          f"{sum(L < 2.5 for L in L_all) / len(L_all):.0%} within 2.5 s, median {np.median(L_all):.2f} s")
    rows = []
    for r in M:
        if r["drones"] <= 0 or r["secrets"] <= 0:
            continue
        a, b = bisect.bisect_left(dts, r["t"]), bisect.bisect_left(dts, r["t"] + dt.timedelta(minutes=6))
        Ls = [L for t, L in D[a:b] if L is not None]
        if len(Ls) >= 20:
            rows.append(dict(r=r, fast=sum(L < 2.5 for L in Ls) / len(Ls), med=float(np.median(Ls)), day=r["t"].strftime("%m-%d")))
    days = sorted({x["day"] for x in rows})
    y = np.array([math.log(x["r"]["secrets"] / Q.copies(x["r"]) / x["r"]["drones"]) for x in rows])
    print(f"{len(rows)} maps; fast-kill share {np.mean([x['fast'] for x in rows]):.2f} "
          f"(range {min(x['fast'] for x in rows):.2f}-{max(x['fast'] for x in rows):.2f})")
    for name, key in (("fast-kill share (0 -> 1)", "fast"), ("median lifetime (+1 s)", "med")):
        v = np.array([x[key] for x in rows])
        X = np.column_stack([np.ones(len(rows))] + [[float(x["day"] == d) for x in rows] for d in days[1:]]
                            + [[float(x["r"]["card"] == "72020420") for x in rows], [float(x["r"]["transg"]) for x in rows], v])
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ b
        se = math.sqrt(np.linalg.pinv(X.T @ X)[-1, -1] * (res @ res) / (len(y) - X.shape[1]))
        print(f"  Secrets per copy per drone vs {name}: x{math.exp(b[-1]):.3f} (95% {math.exp(b[-1] - 1.96 * se):.2f}-{math.exp(b[-1] + 1.96 * se):.2f})")
    rows.sort(key=lambda x: x["fast"])
    k = len(rows) // 3
    for name, g in (("slowest third", rows[:k]), ("middle third", rows[k:2 * k]), ("fastest third", rows[2 * k:])):
        dr = sum(x["r"]["drones"] for x in g)
        sh = sum(x["r"]["shadow_events"] for x in g)
        print(f"  {name:14s} fast share {np.mean([x['fast'] for x in g]):.2f}: {sh} Shadow drops / {dr} drones = {1000 * sh / dr:.2f} per 1,000")


if __name__ == "__main__":
    main(sys.argv[1:])
