#!/usr/bin/env python3
"""How Fluorescent Memory replication works, measured from game logs (2026-10-31, Vlad's 10-30 + 10-31 logs).

A drop of a memory is picked up as one stack (the replicated copies come in the same pickup, or a second pickup within ~1 s), so per
memory the pickup sizes give the replication outcome; a "single" (x1, nothing within 1 s) is a drop that no replication source copied.
Every map's active effects are dumped at map entry (gamelog.parse -> m["effects"], m["card"]): Colorful Fluorescent (A) 215803 (50%),
Melancholy cards 71090100 (20%) / 71090110 (30%) "Fluorescent Memories dropped have a X% chance to be replicated once". Pets are in the join
dump (servantId): Kong rank 5 (20% replicated 1 time, 10% 2 times), Cloudgatherer - Sky's Dome rank 5 (10% once).
Rule candidates for the "replicated once" chances (Kong rolls afterwards):
  add-and-cap   chances add, capped at 100%            -> P(single) = max(0, 1 - sum) x 0.7
  independent   each source rolls on its own            -> P(single) = prod(1 - p) x 0.7
  highest-only  only the biggest chance counts          -> P(single) = (1 - max p) x 0.7
Rare memories only (Shadow, Tomorrow's Direction, Lost Secrets, Hundredfold, Maud's Trick, Crow's Wail): Secrets drop in piles and merge.
Usage: python3 tools/farm/replication.py LOG [LOG ...]
"""
import sys, os, re, collections, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gamelog as G
from math import comb

RARE = {"6216": "Shadow", "6153": "Tomorrow", "6007": "Lost Secrets", "6125": "Hundredfold", "6004": "Maud", "6003": "Crow"}
SOURCES = {"215803": 0.50, "71090100": 0.20, "71090110": 0.30, "12030": 0.20}   # Colorful (A), Melancholy 20 / 30, Fluorescent probe (cost id)
PETS_ONCE = [0.10]          # Sky's Dome rank 5
KONG_NONE = 0.70            # Kong rank 5: 20% +1, 10% +2


def pickups(paths, maps):
    """[(map index, t, item, qty)] for every PickItems block inside a map window."""
    stacks = {}; block = None; items = []; t0 = None; out = []
    wins = [(k, m["entered"], m["end"]) for k, m in enumerate(maps) if m["entered"] and m["end"]]
    for path in paths:
        for line in open(path, encoding="utf-8", errors="replace"):
            m = G.PROTO.search(line)
            if m:
                if m.group(2) == "start": block = m.group(1); items = []; t0 = G.ts(line)
                else:
                    if block in ("PickItems", "PickItem") and t0 is not None:
                        d = collections.Counter()
                        for b, x in items: d[b] += x
                        for k, a, e in wins:
                            if a <= t0 <= e:
                                for i, q in d.items():
                                    if i in RARE and q > 0: out.append((k, t0, i, q))
                                break
                    block = None
                continue
            m = G.CHG.search(line)
            if not m: continue
            kind, base, guid, num, page, slot = m.groups(); num = int(num) if num else 0
            prev = stacks.get(guid, (base, 0))[1]
            if kind == "Delete": stacks.pop(guid, None); delta = -prev
            else: stacks[guid] = (base, num); delta = num - prev
            if block: items.append((base, delta))
    return out


def chances(m):
    ps = [p for i, p in SOURCES.items() if i in m["effects"] or i in m["cost"]]
    if "15003" in m.get("catalyst", []): ps.append(0.30)   # Catalyst Creation Engine, Fluorescent crystal: 30% replicated once [Vlad]
    return ps + PETS_ONCE


def predict(ps):
    return {"add-and-cap": max(0.0, 1 - sum(ps)) * KONG_NONE,
            "independent": __import__("math").prod(1 - p for p in ps) * KONG_NONE,
            "highest-only": (1 - max(ps)) * KONG_NONE}


def binom_tail(k, n, p):     # P(X >= k)
    return sum(comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


def main(paths):
    maps = [m for m in G.parse(paths) if G.is_stack(m)]
    pk = pickups(paths, maps)
    drops = collections.defaultdict(list)                     # merge same item within 1 s = one drop
    for k, t, i, q in sorted(pk, key=lambda r: (r[0], r[1])):
        lst = drops[k]
        if lst and lst[-1][1] == i and (t - lst[-1][2]).total_seconds() <= 1.0: lst[-1][0] += q; lst[-1][2] = t
        else: lst.append([q, i, t])
    groups = collections.defaultdict(lambda: [0, 0, collections.Counter(), None])
    for k, lst in drops.items():
        ps = chances(maps[k]); key = "+".join(f"{int(p * 100)}" for p in sorted(ps, reverse=True))
        g = groups[key]; g[3] = ps
        for q, i, t in lst:
            g[0] += 1; g[1] += q == 1; g[2][q] += 1
    print(f"{len(maps)} maps, {sum(g[0] for g in groups.values())} rare-memory drops")
    tot = collections.Counter()
    for key, (n, s1, sizes, ps) in sorted(groups.items(), key=lambda kv: -kv[1][0]):
        pr = predict(ps)
        print(f"once-chances {key:14s} drops {n:3d} singles {s1:3d} = {s1 / n:4.0%} | predicted " +
              "  ".join(f"{r} {v:4.0%} (P>= obs {binom_tail(s1, n, v):.3f})" for r, v in pr.items()) + "  | sizes " + " ".join(f"{q}:{c}" for q, c in sorted(sizes.items())))
        for r, v in pr.items(): tot[r] += v * n
    n = sum(g[0] for g in groups.values()); s1 = sum(g[1] for g in groups.values())
    print(f"all: {s1} singles of {n}; expected " + ", ".join(f"{r} {v:.1f}" for r, v in tot.items()))


if __name__ == "__main__":
    main([a for a in sys.argv[1:] if not a.startswith("--")])
