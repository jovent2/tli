#!/usr/bin/env python3
"""Fit how Fluorescent Memory replication works from game logs (2026-10-31; first fit: 98 rare-memory drops, 10-30 + 10-31 logs).

Drops: rare memories (Shadow, Tomorrow's Direction, Lost Secrets, Hundredfold, Maud's Trick, Crow's Wail), same item picked within 1 s = one drop.
Sources per map (all from the log): Colorful Fluorescent (A) 50% (effect 215803), Melancholy card 20% / 30% (71090100 / 71090110), Catalyst
Creation Engine's Fluorescent crystal (gameplay 7602 code 15003) = buff "Fluorescent memories dropped have a 30% chance to be replicated once"
[Vlad: binary, random pick], Sky's Dome 10% (pet, always), Kong "20% replicated 1 time" + "10-13% replicated 2 times" (pet, always).
Models: once-rule {add-cap, indep-any, indep-each, highest} x Kong {exclusive / independent lines} x {per-drop, per-instance, multiply, kong-first}
x Kong 2-times {10%, 13%}, plus a merge share m (two drops swept into one pickup). Output: log-likelihoods, per-context fitted once-chance.
Usage: python3 tools/farm/replication_fit.py LOG [LOG ...]
"""
import sys, os, math, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gamelog as G, replication as R
SMAX = 16

def drops(paths):
    rows = []
    for path in paths:
        maps = [m for m in G.parse([path]) if G.is_stack(m)]
        ev = collections.defaultdict(list)
        for k, t, i, q in sorted(R.pickups([path], maps), key=lambda r: (r[0], r[1])):
            lst = ev[k]
            if lst and lst[-1][1] == i and (t - lst[-1][2]).total_seconds() <= 1.0: lst[-1][0] += q; lst[-1][2] = t
            else: lst.append([q, i, t])
        for k, lst in ev.items():
            m = maps[k]; e = m["effects"]
            src = dict(colorful="215803" in e, card=30 if "71090110" in e else 20 if "71090100" in e else 0, catalyst="15003" in m.get("catalyst", []))
            rows += [dict(size=q, **src) for q, i, t in lst]
    return rows

def conv(a, b):
    out = [0.0] * (SMAX + 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if i + j <= SMAX: out[i + j] += x * y
    return out

def once_ps(r):
    return [0.10] + ([0.50] if r["colorful"] else []) + ([r["card"] / 100] if r["card"] else []) + ([0.30] if r["catalyst"] else [])

def extra(ps, rule):
    if rule == "add-cap": q = min(1.0, sum(ps)); return [1 - q, q]
    if rule == "indep-any": q = 1 - math.prod(1 - p for p in ps); return [1 - q, q]
    if rule == "highest": q = max(ps); return [1 - q, q]
    d = [1.0]
    for p in ps: d = conv(d, [1 - p, p])
    return d

def kong(k1, k2, mode):
    return [1 - k1 - k2, k1, k2] if mode == "excl" else [(1 - k1) * (1 - k2), k1 * (1 - k2), (1 - k1) * k2, k1 * k2]

def size_dist(r, rule, kmode, kapply, k1, k2):
    K = kong(k1, k2, kmode); out = [0.0] * (SMAX + 1)
    for e, pe in enumerate(extra(once_ps(r), rule)):
        if not pe: continue
        n = 1 + e
        if kapply == "per-drop": d = conv([0] * n + [1], K)
        elif kapply == "per-instance":
            d = [1.0]
            for _ in range(n): d = conv(d, conv([0, 1.0], K))
        else:
            d = [0.0] * (SMAX + 1)
            for kk, pk in enumerate(K):
                s = n * (1 + kk) if kapply == "multiply" else (1 + kk) * (1 + e)
                if s <= SMAX: d[s] += pk
        for s, x in enumerate(d): out[s] += pe * x
    return out

def loglik(rows, *args, m=0.0):
    ll = 0.0
    for r in rows:
        p = size_dist(r, *args); pm = [(1 - m) * a + m * b for a, b in zip(p, conv(p, p))]
        ll += math.log(max(1e-12, pm[min(r["size"], SMAX)]))
    return ll

def main(paths):
    rows = drops(paths)
    print(f"{len(rows)} drops; contexts (colorful, card, catalyst):", sorted(collections.Counter((r['colorful'], r['card'], r['catalyst']) for r in rows).items()))
    res = []
    for rule, kmode, kapply, kk in itertools.product(["add-cap", "indep-any", "indep-each", "highest"], ["excl", "indep"],
                                                     ["per-drop", "per-instance", "multiply", "kong-first"], [(0.20, 0.13), (0.20, 0.10)]):
        res.append(max((loglik(rows, rule, kmode, kapply, *kk, m=m), rule, kmode, kapply, kk, m) for m in [i / 50 for i in range(21)]))
    res.sort(reverse=True)
    for ll, rule, kmode, kapply, kk, m in res[:8]: print(f"  {ll:8.2f}  once={rule:10s} kong {kmode:5s} {kapply:12s} {kk[0]:.2f}/{kk[1]:.2f}  merge {m:.2f}")
    for rule in ["add-cap", "indep-any", "indep-each", "highest"]:
        b = max(x for x in res if x[1] == rule); print(f"  best once={rule:10s} {b[0]:8.2f}")
    # per-context once-chance, Kong per instance (independent lines 20/10), merge 0.12
    K = kong(0.20, 0.10, "indep")
    def dist(q):
        out = [0.0] * (SMAX + 1)
        for n, pn in ((1, 1 - q), (2, q)):
            d = [1.0]
            for _ in range(n): d = conv(d, conv([0, 1.0], K))
            for s, x in enumerate(d): out[s] += pn * x
        return [(0.88) * a + 0.12 * b for a, b in zip(out, conv(out, out))]
    ctx = collections.defaultdict(list)
    for r in rows: ctx[(r["colorful"], r["catalyst"], r["card"])].append(r["size"])
    print("\nfitted once-chance per context (95% range) vs add-cap / independent / highest:")
    for c, sizes in sorted(ctx.items()):
        qs = [i / 100 for i in range(101)]; ll = [sum(math.log(max(1e-12, dist(q)[min(s, SMAX)])) for s in sizes) for q in qs]
        b = max(range(101), key=lambda i: ll[i]); ok = [i for i in range(101) if ll[i] >= ll[b] - 1.92]
        ps = once_ps(dict(colorful=c[0], catalyst=c[1], card=c[2]))
        print(f"  colorful={c[0]!s:5s} catalyst={c[1]!s:5s} card={c[2]:2d}: {len(sizes):3d} drops  {qs[b]:4.0%} ({qs[ok[0]]:.0%}-{qs[ok[-1]]:.0%})  "
              f"| {min(1, sum(ps)):.0%} / {1 - math.prod(1 - p for p in ps):.0%} / {max(ps):.0%}")

if __name__ == "__main__":
    main([a for a in sys.argv[1:] if not a.startswith("--")])
