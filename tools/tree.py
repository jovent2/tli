#!/usr/bin/env python3
"""Validate a talent allocation against tlidb's panel data and total up what it gives.

  python3 tools/tree.py ss14/thea/trees.json            # check + per-panel totals + grand total
  python3 tools/tree.py ss14/thea/trees.json --nodes    # also list every allocated node

Allocation file format:
  {"panels": [{"panel": "Magister", "core": "Bunch", "prism_at": null,
               "nodes": {"352_80": 3, "480_80": 3, ...}}]}
Node ids are tlidb layout centres "x_y" (columns x = 96,224,352,480,608,736,864 = 0,3,...,18 pts;
rows y = 80,176,272,368,464). See data/talents.json.

Checks: node exists, rank <= max rank, column gate (points spent elsewhere in the panel >= column
points, approximated by total panel points), pairing (a node connected to an allocated node on its left
must have that left node allocated), core point requirement.
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NUM = re.compile(r"[+-]?\d+(?:\.\d+)?")


def load_panels():
    return {p["key"]: p for p in json.loads((ROOT / "data" / "talents.json").read_text(encoding="utf-8"))}


def scale(line, rank):
    """Multiply every number in a stat line by rank; return (template, values)."""
    vals = [float(x) * rank for x in NUM.findall(line)]
    return NUM.sub("{}", line), vals


def fmt(template, vals):
    out = template
    for v in vals:
        s = f"{v:+g}" if template.startswith("{}") else f"{v:g}"
        out = out.replace("{}", s, 1)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("alloc")
    ap.add_argument("--nodes", action="store_true")
    a = ap.parse_args(argv)
    panels = load_panels()
    alloc = json.loads(Path(a.alloc).read_text(encoding="utf-8"))
    grand = defaultdict(lambda: None)
    problems = []
    for pa in alloc["panels"]:
        key = pa["panel"]
        p = panels.get(key)
        if not p:
            problems.append(f"{key}: unknown panel")
            continue
        lay = {n["id"]: n for n in p["layout"]}
        spent = sum(pa["nodes"].values()) + (0 if not pa.get("prism_at") else 0)
        print(f"\n## {p['name']} — {spent} pts, core {pa.get('core')}"
              + (f", prism at {pa['prism_at']}" if pa.get("prism_at") else ""))
        core = next((c for c in p["cores"] if c["name"] == pa.get("core")), None)
        if pa.get("core") and not core and pa.get("core_source") != "prism":
            problems.append(f"{key}: core '{pa.get('core')}' not on this panel (prism/slate core?)")
        elif core and spent < core.get("points", 0):
            problems.append(f"{key}: core {core['name']} needs {core['points']} pts, have {spent}")
        totals = defaultdict(lambda: None)
        for nid, rank in sorted(pa["nodes"].items(), key=lambda kv: (int(kv[0].split('_')[1]), int(kv[0].split('_')[0]))):
            n = lay.get(nid)
            if not n:
                problems.append(f"{key} {nid}: no such node")
                continue
            mr = n.get("max_rank") or (1 if "Legendary" in (n["name"] or "") else 3)
            if rank > mr:
                problems.append(f"{key} {nid}: rank {rank} > max {mr}")
            if n.get("column_points") and spent < n["column_points"]:
                problems.append(f"{key} {nid}: column {n['column_points']} pts, panel has {spent}")
            x, y = map(int, nid.split("_"))
            left = [c for c in n.get("connects", []) if int(c.split("_")[0]) < x]
            if left and not any(c in pa["nodes"] or c == pa.get("prism_at") for c in left):
                problems.append(f"{key} {nid}: needs {left} first")
            lines = [l for l in n["lines"] if not l.startswith("(Max Active") and l != "Legendary Medium Talent"]
            if a.nodes:
                print(f"  {nid} col{n.get('column_points')} {n['name']} x{rank}: " + " · ".join(lines))
            for l in lines:
                t, v = scale(l, rank)
                for agg in (totals, grand):
                    cur = agg[t]
                    agg[t] = v if cur is None else [x1 + x2 for x1, x2 in zip(cur, v)]
        print("  totals: " + " | ".join(fmt(t, v) for t, v in totals.items()))
    print("\n## All panels")
    for t, v in sorted(grand.items(), key=lambda kv: kv[0]):
        print("  " + fmt(t, v))
    print("\n## Problems" if problems else "\nNo problems.")
    for pr in problems:
        print("  - " + pr)


if __name__ == "__main__":
    main()
