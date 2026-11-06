#!/usr/bin/env python3
"""His Evernight Vigil + Shadow Overrealm loop from the game log: per-phase loot, floors, and the what-ifs (floors, DS resonance,
Generous Elite, Sinful (A)) priced at today's prices.

  python3 tools/farm/overrealm_loop.py LOG [LOG ...]

Phases per map: pre (map before the Overrealm door), vigil (GameplayType 8100 enter -> "We have delivered the soul"), ovr (the pact
config switch "(Overrealm)" -> Stop_Mus_Gameplay_S12_Ov), post (after it: the exit reward dump lands 4-17 s later + the rest of the map).
Floors = `LevelMgr:_FastEnterLevelSuccess()` count - 1 inside the Overrealm window.
"""
import collections
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gamelog as G  # noqa: E402
import runs as RN  # noqa: E402

MARK = {"vigil_enter": "GAMEPLAY_ENTER] Result=Success GameplayType=8100", "vigil_done": "We have delivered the soul",
        "ovr_enter": "Switched to another pact configuration plan (Overrealm)", "ovr_stop": "Stop_Mus_Gameplay_S12_Ov",
        "floor": "LevelMgr:_FastEnterLevelSuccess()", "death": "FightResult@ Open FightFailureView"}


def walk(paths):
    """-> pickups [(t, {id: qty})], marks [(t, kind)]; stacks tracked like gamelog.parse."""
    stacks = {}; block = None; items = []; picks = []; marks = []
    for p in paths:
        for line in open(p, encoding="utf-8", errors="replace"):
            t = G.ts(line)
            if t is None:
                continue
            for k, s in MARK.items():
                if s in line:
                    marks.append((t, k))
                    break
            m = G.PROTO.search(line)
            if m:
                if m.group(2) == "start":
                    block = m.group(1); items = []
                else:
                    if block in ("PickItems", "PickItem"):
                        d = collections.Counter()
                        for b, dl in items:
                            d[b] += dl
                        picks.append((t, {b: v for b, v in d.items() if v > 0}))
                    block = None; items = []
                continue
            if G.RESET.search(line):
                continue
            m = G.CHG.search(line)
            if not m:
                continue
            kind, base, guid, num, page, slot = m.groups()
            if base in G.IGNORE_IDS:
                continue
            num = int(num) if num else 0
            prev = stacks.get(guid, (base, 0))[1]
            if kind == "Delete":
                stacks.pop(guid, None); delta = -prev
            else:
                stacks[guid] = (base, num); delta = num - prev
            if block is not None:
                items.append((base, delta))
    return picks, marks


def per_map(maps, picks, marks):
    out = []
    for m in maps:
        if not m["end"]:
            continue
        t0, t1 = (m["entered"] or m["start"]), m["end"]
        if (t1 - t0).total_seconds() > 1200:
            continue
        mk = [(t, k) for t, k in marks if t0 <= t <= t1]
        first = lambda k: next((t for t, kk in mk if kk == k), None)  # noqa: E731
        last = lambda k: next((t for t, kk in reversed(mk) if kk == k), None)  # noqa: E731
        ve, vd, oe, os_ = first("vigil_enter"), first("vigil_done"), first("ovr_enter"), last("ovr_stop")
        floors = max(0, sum(1 for t, k in mk if k == "floor") - 1) if oe else 0
        ph = collections.defaultdict(collections.Counter)
        for t, d in picks:
            if not (t0 <= t <= t1):
                continue
            if oe and os_ and oe <= t <= os_ + datetime.timedelta(seconds=3):
                p = "ovr"
            elif ve and vd and ve <= t <= vd + datetime.timedelta(seconds=3):
                p = "vigil"
            elif oe and os_ and t > os_:
                p = "post"
            else:
                p = "pre"
            ph[p].update(d)
        out.append(dict(m=m, floors=floors, vigil_s=(vd - ve).total_seconds() if ve and vd else None,
                        ovr_s=(os_ - oe).total_seconds() if oe and os_ else None, deaths=sum(1 for t, k in mk if k == "death"),
                        phases=ph, total_s=(t1 - t0).total_seconds()))
    return out


def val(c):
    return sum(RN.value(i, q) for i, q in c.items())


def main(paths):
    M = G.parse(paths)
    picks, marks = walk(paths)
    ms = [m for m in M if any("Overrealm" in RN.name(i) for i in m["cost"])]
    rows = per_map(ms, picks, marks)
    n = len(rows)
    cost = sum(RN.value(i, q, sold=False) for r in rows for i, q in r["m"]["cost"].items()) / n
    gross = sum(val(sum(r["phases"].values(), collections.Counter())) for r in rows) / n
    secs = sum(r["total_s"] for r in rows) / n
    print(f"{n} Overrealm maps, prices {os.path.basename(RN.PRICE_FILE)}: gross {gross:.0f} cost {cost:.0f} net {gross - cost:.0f}/map, "
          f"{secs:.0f} s in map (+~20 s town) -> {(gross - cost) / ((secs + 20) / 60):.1f} FE/min; deaths {sum(r['deaths'] for r in rows) / n:.2f}/map")
    tot = collections.defaultdict(collections.Counter)
    for r in rows:
        for p, c in r["phases"].items():
            tot[p].update(c)
    for p in ("pre", "vigil", "ovr", "post"):
        c = tot[p]; top = sorted(((RN.value(i, q), i, q) for i, q in c.items()), reverse=True)[:6]
        print(f"  {p:5s} {val(c) / n:5.0f} FE/map: " + ", ".join(f"{RN.name(i).replace('_', ' ')[:26]} {q / n:.2f} ({v / n:.1f})" for v, i, q in top))
    byf = collections.defaultdict(list)
    for r in rows:
        byf[r["floors"]].append(r)
    print("  floors | maps | Overrealm s | map s | deaths/map | gross/map")
    for f in sorted(byf):
        rs = byf[f]
        print(f"  {f:6d} | {len(rs):4d} | {sum(r['ovr_s'] or 0 for r in rs) / len(rs):11.0f} | {sum(r['total_s'] for r in rs) / len(rs):5.0f} | "
              f"{sum(r['deaths'] for r in rs) / len(rs):10.2f} | {sum(val(sum(r['phases'].values(), collections.Counter())) for r in rs) / len(rs):9.0f}")
    adv = [sum(1 for r in rows if r["floors"] >= k) for k in (1, 2, 3, 4)]
    print(f"  advance rates 1->2 {adv[1] / adv[0]:.0%}, 2->3 {adv[2] / max(adv[1], 1):.0%}, 3->4 {adv[3] / max(adv[2], 1):.0%}; "
          f"mean floors {sum(r['floors'] for r in rows) / n:.2f}")


if __name__ == "__main__":
    main(sys.argv[1:])
