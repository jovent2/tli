#!/usr/bin/env python3
"""How Fluorescent Memory replication works, fitted from game logs (2026-10-31: 98 rare-memory drops + 107 Colorful Machines maps,
10-30 full-day + 10-31 logs).

Sources per map, all read from the log: Colorful Fluorescent (A) 50% (effect 215803), Melancholy card 20% / 30% (71090100 / 71090110),
the Catalyst Creation Engine's Fluorescent crystal (gameplay 7602 code 15003; buff "Fluorescent memories dropped have a 30% chance to be
replicated once", binary, the engine picks [Vlad]), Sky's Dome 10% (pet, every map), Kong "20% replicated 1 time" + "13% replicated
2 times" [Vlad] (pet, every map).
Two kinds of evidence:
  rare drops   size of each rare-memory drop (Shadow, Tomorrow's Direction, Lost Secrets, Hundredfold, Maud's Trick, Crow's Wail; the same
               item picked within 1 s = one drop; same-item pickups 1-20 s apart are rare: 2 of 98) -> the whole copy distribution
  Secrets/map  Secrets drop in piles and merge, so only the per-map mean is usable; it scales with the mean copy count. The engine picks the
               crystal at random -> maps with / without the Fluorescent crystal are a clean test of whether a 30% source adds on top of 50%
Once-rules: add-cap (one roll at the sum, cap 100%) / indep-any (each rolls, any hit = 1 copy) / indep-each (each rolls, each hit = its own
copy) / highest (only the biggest chance). Kong: once per drop or on each copy; its two lines exclusive or independent; 2nd line 10% or 13%.
Merge share m = two drops swept into one pickup.
Usage: python3 tools/farm/replication_fit.py LOG [LOG ...]
"""
import sys, os, math, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gamelog as G, replication as R
SMAX = 16
RULES = ["add-cap", "indep-any", "indep-each", "highest"]
LABEL = {"add-cap": "chances add, one roll, cap 100%", "indep-any": "each rolls, any hit = 1 copy",
         "indep-each": "each rolls, each hit = its own copy", "highest": "only the biggest chance counts"}
MACHINES = "10154"           # Cruising Mechanical (A) in the cost = his Machines stack


def load(paths):
    """-> (rare drops [dict(size, colorful, card, catalyst)], Colorful Machines maps with the engine [dict(secrets, ncat, colorful, card, catalyst)])"""
    rows, out = [], []
    for path in paths:
        maps = [m for m in G.parse([path]) if G.is_stack(m)]
        for m in maps:
            e = m["effects"]
            m["src"] = dict(colorful="215803" in e, card=30 if "71090110" in e else 20 if "71090100" in e else 0,
                            catalyst="15003" in m.get("catalyst", []))
            if MACHINES in m["cost"] and m["src"]["colorful"] and m.get("catalyst"):
                out.append(dict(secrets=m["loot"].get("6002", 0), ncat=m["catalyst"].count("15003"), **m["src"]))
        ev = collections.defaultdict(list)
        for k, t, i, q in sorted(R.pickups([path], maps), key=lambda r: (r[0], r[1])):
            lst = ev[k]
            if lst and lst[-1][1] == i and (t - lst[-1][2]).total_seconds() <= 1.0: lst[-1][0] += q; lst[-1][2] = t
            else: lst.append([q, i, t])
        for k, lst in ev.items():
            rows += [dict(size=q, **maps[k]["src"]) for q, i, t in lst]
    return rows, out


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
    """distribution of once-copies added to the original"""
    if rule == "add-cap": q = min(1.0, sum(ps)); return [1 - q, q]
    if rule == "indep-any": q = 1 - math.prod(1 - p for p in ps); return [1 - q, q]
    if rule == "highest": q = max(ps); return [1 - q, q]
    d = [1.0]
    for p in ps: d = conv(d, [1 - p, p])
    return d


def mean_copies(ps, rule):
    if rule == "add-cap": return 1 + min(1.0, sum(ps))
    if rule == "indep-each": return 1 + sum(ps)
    if rule == "indep-any": return 2 - math.prod(1 - p for p in ps)
    return 1 + max(ps)


def kong(k1, k2, mode):
    return [1 - k1 - k2, k1, k2] if mode == "excl" else [(1 - k1) * (1 - k2), k1 * (1 - k2), (1 - k1) * k2, k1 * k2]


def size_dist(r, rule, kmode, kapply, k1, k2, m=0.0):
    K = kong(k1, k2, kmode); out = [0.0] * (SMAX + 1)
    for e, pe in enumerate(extra(once_ps(r), rule)):
        if not pe: continue
        n = 1 + e
        if kapply == "per-drop": d = conv([0] * n + [1], K)
        else:
            d = [1.0]
            for _ in range(n): d = conv(d, conv([0, 1.0], K))
        for s, x in enumerate(d): out[s] += pe * x
    return [(1 - m) * a + m * b for a, b in zip(out, conv(out, out))] if m else out


def rare_fit(rows):
    """-> sorted [(loglik, rule, kmode, kapply, (k1, k2), m)] (best merge share per model)"""
    ctx = collections.defaultdict(list)
    for r in rows: ctx[(r["colorful"], r["card"], r["catalyst"])].append(min(r["size"], SMAX))
    res = []
    for rule, kmode, kapply, kk in itertools.product(RULES, ["excl", "indep"], ["per-drop", "per-copy"], [(0.20, 0.13), (0.20, 0.10)]):
        base = {c: size_dist(dict(colorful=c[0], card=c[1], catalyst=c[2]), rule, kmode, kapply, *kk) for c in ctx}
        best = None
        for m in [i / 50 for i in range(21)]:
            ll = 0.0
            for c, sizes in ctx.items():
                p = base[c]; pm = [(1 - m) * a + m * b for a, b in zip(p, conv(p, p))] if m else p
                ll += sum(math.log(max(1e-12, pm[s])) for s in sizes)
            if best is None or ll > best[0]: best = (ll, rule, kmode, kapply, kk, m)
        res.append(best)
    return sorted(res, reverse=True)


def secrets_fit(maps, rule):
    """Secrets/map = base x mean copies x noise (sd = c x mean) -> (loglik, base, c)"""
    k = [mean_copies(once_ps(r), rule) for r in maps]; y = [r["secrets"] / x for r, x in zip(maps, k)]; n = len(y)
    best = None
    for b in [x / 10 for x in range(200, 1200)]:
        c = math.sqrt(sum((v - b) ** 2 for v in y) / (n * b * b))
        ll = -sum(math.log(c * b * x) for x in k) - n / 2
        if best is None or ll > best[0]: best = (ll, b, c)
    return best


def main(paths):
    rows, maps = load(paths)
    print(f"{len(rows)} rare-memory drops; contexts (colorful, card, catalyst):",
          sorted(collections.Counter((r['colorful'], r['card'], r['catalyst']) for r in rows).items()))
    print(f"{len(maps)} Colorful Machines maps with the engine, {sum(r['catalyst'] for r in maps)} with the Fluorescent crystal")
    rf = rare_fit(rows)
    print("\n== rare drops: best models (log-likelihood)")
    for ll, rule, kmode, kapply, kk, m in rf[:6]:
        print(f"  {ll:8.2f}  {rule:10s} Kong {kmode:5s} {kapply:8s} {kk[0]:.2f}/{kk[1]:.2f}  merge {m:.2f}")
    best = {rule: next(x for x in rf if x[1] == rule) for rule in RULES}
    sf = {rule: secrets_fit(maps, rule) for rule in RULES}
    print("\n== Secrets per map (Colorful Machines): observed vs predicted, base fitted per rule")
    print("  crystal card maps   observed     " + "  ".join(f"{r:>10s}" for r in RULES))
    ctx = collections.defaultdict(list)
    for r in maps: ctx[(r["catalyst"], r["card"])].append(r["secrets"])
    for c in sorted(ctx):
        xs = ctx[c]; n = len(xs); mu = sum(xs) / n; se = math.sqrt(sum((x - mu) ** 2 for x in xs) / max(1, n - 1) / n)
        ps = once_ps(dict(colorful=True, card=c[1], catalyst=c[0]))
        print(f"  {c[0]!s:7s} {c[1]:3d} {n:4d}  {mu:6.1f} ± {se:4.1f}   " + "  ".join(f"{sf[r][1] * mean_copies(ps, r):10.1f}" for r in RULES))
    num = den = 0.0                                            # catalyst effect on log Secrets, stratified by card
    for card in (0, 20, 30):
        a = [math.log(r["secrets"]) for r in maps if r["card"] == card and r["catalyst"] and r["secrets"] > 0]
        b = [math.log(r["secrets"]) for r in maps if r["card"] == card and not r["catalyst"] and r["secrets"] > 0]
        if len(a) > 1 and len(b) > 1:
            va = sum((x - sum(a) / len(a)) ** 2 for x in a) / (len(a) - 1); vb = sum((x - sum(b) / len(b)) ** 2 for x in b) / (len(b) - 1)
            v = va / len(a) + vb / len(b); num += (sum(a) / len(a) - sum(b) / len(b)) / v; den += 1 / v
    eff = num / den; s = 1 / math.sqrt(den); ps0 = once_ps(dict(colorful=True, card=0, catalyst=False)); ps1 = ps0 + [0.30]
    print(f"  Fluorescent crystal effect (stratified by card): x{math.exp(eff):.3f} (95% x{math.exp(eff - 1.96 * s):.2f}-x{math.exp(eff + 1.96 * s):.2f});"
          " predicted " + ", ".join(f"{r} x{mean_copies(ps1, r) / mean_copies(ps0, r):.2f}" for r in RULES))
    print("\n== joint (rare drops + Secrets/map)")
    for rule in sorted(RULES, key=lambda r: -(best[r][0] + sf[r][0])):
        print(f"  {best[rule][0] + sf[rule][0]:8.2f}  {LABEL[rule]:38s} (rare {best[rule][0]:8.2f}, Secrets {sf[rule][0]:8.2f})")
    col = [r for r in rows if r["colorful"]]
    obs = collections.Counter(min(r["size"], 7) for r in col)
    print(f"\n== sizes of the {len(col)} rare drops on Colorful maps (7 = 7+): observed vs each rule's best model")
    print("  observed                              " + " ".join(f"{obs[s]:5d}" for s in range(1, 8)))
    for rule in RULES:
        ll, _, kmode, kapply, kk, m = best[rule]; tot = [0.0] * 8
        for r in col:
            p = size_dist(r, rule, kmode, kapply, *kk, m=m)
            for s in range(1, SMAX + 1): tot[min(s, 7)] += p[s]
        print(f"  {LABEL[rule]:38s}" + " ".join(f"{tot[s]:5.1f}" for s in range(1, 8)))


if __name__ == "__main__":
    main([a for a in sys.argv[1:] if not a.startswith("--")])
