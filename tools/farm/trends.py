#!/usr/bin/env python3
"""Price history of the loot and consumables that carry the Deep Space setups (etor /chart, 1-day candles; `etor_refresh.py charts`).

  python3 tools/farm/trends.py [--days 7] [--min-price 1]
Prints: item, price now, change over 7 and 14 days, season high and low, days of data. Loot that is sliding at 5%+ a week is
flagged; a setup whose income sits on it is overvalued by today's price.
"""
import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN  # noqa: E402

CDIR = os.path.join(RN.EXT, "etor_charts")


def series(i):
    f = os.path.join(CDIR, f"{i}.json")
    if not os.path.exists(f):
        return []
    return [(t["timestamp"], t["price"]) for t in json.load(open(f)).get("trend", []) if t.get("price")]


def change(tr, days):
    if len(tr) < days + 1:
        return None
    a, b = tr[-days - 1][1], tr[-1][1]
    return b / a - 1 if a else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-price", type=float, default=1.0)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args(argv)
    rows = []
    for f in glob.glob(os.path.join(CDIR, "*.json")):
        i = os.path.basename(f)[:-5]
        if not i.isdigit():
            continue
        tr = series(i)
        if not tr:
            continue
        now = tr[-1][1]
        if now < a.min_price and not a.all:
            continue
        rows.append((i, RN.name(i), now, change(tr, 7), change(tr, 14), max(p for _, p in tr), min(p for _, p in tr), len(tr)))
    rows.sort(key=lambda r: (r[3] if r[3] is not None else 0))
    print(f"{'item':44s} {'now':>8} {'7d':>6} {'14d':>6} {'high':>8} {'low':>8} days")
    for i, n, now, c7, c14, hi, lo, d in rows:
        flag = "  <- sliding" if c7 is not None and c7 <= -0.05 else ("  <- rising" if c7 is not None and c7 >= 0.05 else "")
        print(f"{n[:44]:44s} {now:8.2f} {('%+.0f%%' % (c7 * 100)) if c7 is not None else '  n/a':>6} {('%+.0f%%' % (c14 * 100)) if c14 is not None else '  n/a':>6} {hi:8.2f} {lo:8.2f} {d:3d}{flag}")


if __name__ == "__main__":
    main()
