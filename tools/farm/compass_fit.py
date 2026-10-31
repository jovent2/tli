#!/usr/bin/env python3
"""What each compass / probe does to one loot item, fitted across the CN etor strategy leaderboards (real logged runs).

Each etor strategy = one player's setup averaged over its runs: loot and cost per run (a compass at 0.9 = on 90% of the runs).
Weighted least squares of log(item per run) on the compass / probe fractions + a Deep Space dummy, weights = runs (capped at 150),
HC1 robust 95% intervals. Default population: drone farmers (Cruising Mechanical Compass (Artifact) on >= 50% of runs).

Usage: python3 tools/farm/compass_fit.py [--item 6002] [--clean] [--all]
  --item   loot id (6002 Secret of the Glacial Abyss, 6127 Immolating Flame, 100300 FE, ...)
  --clean  only strategies with Transgression and Cruising on >= 90% of runs
  --all    every strategy, not only drone farmers
"""
import argparse
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN  # noqa: E402

FEATS = dict(Focus="10103", ColorfulA="10104", Colorful="10102", SiN="10023", Transgression="10003", Cruising="10154",
             FluoDSprobe="12031", FlourDSprobe="12001", FluoProbe="12030", FlourProbe="12000", SinfulA="10002", Sinful="10001")


def fit(rows, item, feats):
    X, y, w = [], [], []
    for r in rows:
        v = r["loot"].get(item, 0)
        if v <= 0:
            continue
        deep = 1.0 if any("Deep_Space_Beacon" in RN.name(i) for i in r["cost"]) else 0.0
        astro = max([q for i, q in r["cost"].items() if "Astrolabe" in RN.name(i)] + [0])
        X.append([1.0, deep, astro] + [r["cost"].get(FEATS[f], 0) for f in feats])
        y.append(math.log(v))
        w.append(min(r["count"], 150))
    X, y, w = np.array(X), np.array(y), np.array(w, float)
    names = ["const", "DeepSpace", "astrolabes"] + list(feats)
    keep = [j for j in range(X.shape[1]) if j == 0 or X[:, j].std() > 0]
    X, names = X[:, keep], [names[j] for j in keep]
    sw = np.sqrt(w)
    b, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
    res = y - X @ b
    n, k = X.shape
    bread = np.linalg.pinv((X * w[:, None]).T @ X)
    meat = (X * (w * res)[:, None]).T @ (X * (w * res)[:, None])
    se = np.sqrt(np.diag(bread @ meat @ bread * n / (n - k)))
    return names, b, se, n, float(np.sqrt(np.average(res ** 2, weights=w))), int(w.sum())


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--item", default="6002")
    ap.add_argument("--clean", action="store_true")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args(argv)
    R = RN.load(time_label=None)
    rows = R if a.all else [r for r in R if r["cost"].get(FEATS["Cruising"], 0) >= 0.5]
    if a.clean:
        rows = [r for r in rows if min(r["cost"].get(FEATS["Transgression"], 0), r["cost"].get(FEATS["Cruising"], 0)) >= 0.9]
    feats = [f for f in FEATS if not (f == "Cruising" and not a.all)]
    names, b, se, n, sd, wsum = fit(rows, a.item, feats)
    print(f"{RN.name(a.item)}: {n} strategies ({sum(r['count'] for r in rows)} runs), residual sd {sd:.2f}; x = multiplier for using it on every run")
    for nm, bb, s in zip(names, b, se):
        if nm != "const":
            print(f"  {nm:14s} x{math.exp(bb):5.2f}  (95% {math.exp(bb - 1.96 * s):.2f}-{math.exp(bb + 1.96 * s):.2f})")


if __name__ == "__main__":
    main()
