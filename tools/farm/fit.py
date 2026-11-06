#!/usr/bin/env python3
"""What each compass, probe, resonance affix and Void Chart node does to a mechanic's loot — fitted per mechanic family on every
logged etor strategy that runs it (Deep Space + Profound), one joint model per loot item.

Design: inside a family (e.g. every strategy with an Alert Outlaw compass) the compasses, probes, resonance and the nodes of the
family's own constellations vary across players while the mechanic is the same, so their coefficients are identified. Nodes of
unrelated constellations are left out (they only track which other mechanic the player stacks, which the other compasses already
carry). Model per item: log(drops per run) = const + sum coef * x, WLS (weight = runs, cap 150), light ridge, HC1 errors.
Features: compass / astrolabe / probe fractions, DS resonance affixes (res / 2), Netherrealm resonance / 31, hero class, node line
counts (micros add). Cards and pets are not logged by etor; they average out over the family's runs.
Unidentified = everyone in the family runs it (prints as "fixed in family") — not "useless".

  python3 tools/farm/fit.py [--family outlaw|vigil|overrealm|machines|lunaria|all] [--lam 1.0] [--min-drops 3] [--md out.md]
"""
import argparse
import collections
import glob
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN  # noqa: E402
import ds_scan as D  # noqa: E402

STAGES = ["week3", "week2", "day7", "day6", "day5", "day4", "day3", "day2", "day1"]
SKIP = {"Deep_Space_Beacon", "Netherrealm_resonance", "Deep_Space_Resonance", "Glacial_Abyss_Beacon_%28Timemark_8%29"}
FAMILIES = {
    "outlaw": dict(compass="Alert_Outlaw", cons=("Outlaw", "Profound", "Commodities"),
                   items=["360404", "360405", "360406", "360407", "100300", "300006"]),
    "vigil": dict(compass="Vigil", cons=("Afterlight", "Profound", "Commodities"),
                  items=["394119", "100300", "300006", "5031"]),
    "overrealm": dict(compass="Overrealm", cons=("Overrealm", "Profound", "Commodities", "Gear"),
                      items=["100300", "5031", "300006", "6002", "394119"]),
    "machines": dict(compass="Cruising_Mechanical", cons=("Machine", "Profound", "Commodities", "Fluorescent"),
                     items=["6002", "6216", "6127", "100300"]),
    "lunaria": dict(compass="Lunaria", cons=("Lunaria", "Profound", "Commodities"),
                    items=["100300", "6002", "300006", "394119"]),
}
NAME = {"360404": "Warlock mod", "360405": "Vanguard mod", "360406": "Sniper mod", "360407": "Tank mod", "100300": "FE", "300006": "Sacred Fossil",
        "394119": "Nether King's Remnant", "5031": "Sprout of Legends", "6002": "Secrets", "6216": "Shadows", "6127": "Immolating Flame"}


def node_lines(r):
    out = collections.Counter()
    for k, c in r["talents"].items():
        if k in RN.MD5:
            con, node = RN.MD5[k]
            out[(con.replace("_Talent_Constellation", ""), " / ".join(node["lines"]))] += c
    return out


def load_all():
    R = D.load(STAGES)
    hero = {}
    for f in glob.glob(os.path.join(D.SDIR, "lb_*.json")):
        for it in json.load(open(f))["data"]["items"]:
            hero[it["key"]] = it.get("heroId")
    for r in R:
        r["hero"] = str(hero.get(r["key"]))
        r["nodes"] = node_lines(r)
    return [r for r in R if not any(x in r["talent_label"] for x in ("囚笼", "玩偶"))]


def family_rows(R, fam):
    return [r for r in R if any(fam["compass"] in RN.name(i) and q >= 0.5 for i, q in r["cost"].items())]


def build(rows, cons):
    n = len(rows)
    comp = collections.Counter()
    for r in rows:
        for i, q in r["cost"].items():
            if RN.name(i) not in SKIP and q >= 0.5:
                comp[RN.name(i)] += 1
    comp = sorted(c for c, k in comp.items() if k >= 3)
    nodes = collections.Counter()
    for r in rows:
        for k in r["nodes"]:
            if k[0] in cons:
                nodes[k] += 1
    cols = [("const", "")] + [("compass", c) for c in comp] + [("res", "DS resonance affix (2 res)"), ("res", "Netherrealm resonance /31")]
    fixed = []
    for k, cnt in sorted(nodes.items()):
        vals = [r["nodes"].get(k, 0) for r in rows]
        if cnt >= 3 and len(set(vals)) > 1 and (cnt <= n - 3 or max(vals) > 1):
            cols.append(("node", k))   # varies: presence or count
        elif cnt > n - 3:
            fixed.append(k)
    heroes = sorted({r["hero"] for r in rows})
    cols += [("hero", h) for h in heroes[1:]]
    X = np.zeros((n, len(cols)))
    for i, r in enumerate(rows):
        q = {RN.name(k): v for k, v in r["cost"].items()}
        for j, (kind, key) in enumerate(cols):
            if kind == "const":
                X[i, j] = 1.0
            elif kind == "compass":
                X[i, j] = q.get(key, 0.0)
            elif kind == "res":
                X[i, j] = q.get("Deep_Space_Resonance", 0.0) / 2 if "DS" in key else q.get("Netherrealm_resonance", 0.0) / 31
            elif kind == "node":
                X[i, j] = r["nodes"].get(key, 0)
            elif kind == "hero":
                X[i, j] = 1.0 if r["hero"] == key else 0.0
    return cols, X, fixed


def wls_ridge(X, y, w, lam):
    sw = np.sqrt(w)
    Xw, yw = X * sw[:, None], y * sw
    pen = np.diag([0.0] + [lam] * (X.shape[1] - 1))
    A = Xw.T @ Xw + pen
    b = np.linalg.solve(A, Xw.T @ yw)
    res = y - X @ b
    n, k = X.shape
    Ainv = np.linalg.pinv(A)
    meat = (X * (w * res)[:, None]).T @ (X * (w * res)[:, None])
    se = np.sqrt(np.clip(np.diag(Ainv @ meat @ Ainv) * n / max(n - k, 1), 0, None))
    return b, se, float(np.sqrt(np.average(res ** 2, weights=w)))


def label(c):
    kind, key = c
    if kind == "node":
        line = key[1].replace("In Netherrealm stages, ", "").replace("In Netherrealm Stages, ", "")
        return f"{key[0]}: {line if len(line) <= 88 else line[:40] + '…' + line[-46:]}"
    if kind == "hero":
        return f"hero {key}"
    return key.replace("_Compass", "").replace("_%28Artifact%29", " (A)").replace("_Probe", " probe").replace("_", " ") if kind == "compass" else key


def run_family(R, name, fam, lam, min_drops, out):
    rows = family_rows(R, fam)
    cols, X, fixed = build(rows, fam["cons"])
    runs_n = sum(r["count"] for r in rows)
    out.append(f"\n# {name}: {len(rows)} strategies, {runs_n} runs, {len(cols)} features; nodes fixed in family (everyone runs them, unidentified): {len(fixed)}")
    for k in fixed:
        out.append(f"  fixed: {k[0]}: {k[1][:110]}")
    table = {}
    for item in fam["items"]:
        idx = [i for i, r in enumerate(rows) if r["loot"].get(item, 0) * r["count"] >= min_drops]
        if len(idx) < 25:
            out.append(f"\n## {NAME.get(item, item)}: only {len(idx)} strategies drop it, skipped")
            continue
        y = np.array([math.log(rows[i]["loot"][item]) for i in idx]); w = np.array([min(rows[i]["count"], 150) for i in idx], float)
        Xi = X[idx]
        keep = [j for j in range(Xi.shape[1]) if j == 0 or Xi[:, j].std() > 0]
        b, se, sd = wls_ridge(Xi[:, keep], y, w, lam)
        mean_q = sum(rows[i]["loot"][item] * rows[i]["count"] for i in idx) / sum(rows[i]["count"] for i in idx)
        out.append(f"\n## {NAME.get(item, item)} ({item}): {len(idx)} strategies, {mean_q:.2f}/map on average, price {RN.price(item):.2f}, residual sd {sd:.2f}")
        for t, j in enumerate(keep):
            if j == 0:
                continue
            table.setdefault(cols[j], {})[item] = (b[t], se[t])
    # one line per feature across the family's items
    out.append("\nfeature | " + " | ".join(NAME.get(i, i) for i in fam["items"]))
    for c in cols[1:]:
        if c not in table:
            continue
        cells = []
        for item in fam["items"]:
            if item in table[c]:
                bb, s = table[c][item]
                star = "*" if abs(bb) > 1.96 * s else " "
                cells.append(f"x{math.exp(bb):4.2f}{star} ({math.exp(bb - 1.96 * s):.2f}-{math.exp(bb + 1.96 * s):.2f})")
            else:
                cells.append("—")
        out.append(f"{label(c)[:92]:92s} | " + " | ".join(cells))
    out.append("(* = 95% CI excludes 1; per unit: a compass on every run, one DS affix, 31 Netherrealm resonance, one node point)")
    return table


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", default="all")
    ap.add_argument("--lam", type=float, default=1.0)
    ap.add_argument("--min-drops", type=float, default=3)
    ap.add_argument("--md", default=None)
    a = ap.parse_args(argv)
    R = load_all()
    out = [f"etor fits, prices {os.path.basename(RN.PRICE_FILE)}, {len(R)} strategies total"]
    fams = FAMILIES if a.family == "all" else {a.family: FAMILIES[a.family]}
    for name, fam in fams.items():
        run_family(R, name, fam, a.lam, a.min_drops, out)
    text = "\n".join(out)
    print(text)
    if a.md:
        open(a.md, "w").write(text + "\n")


if __name__ == "__main__":
    main()
