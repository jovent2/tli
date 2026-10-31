#!/usr/bin/env python3
"""How Fluorescent Memory replication works, fitted from game logs (first fit 2026-10-31: 98 rare-memory drops + 107 Colorful Machines maps,
10-30 full-day + 10-31 logs).

Replicate sources per map, all read from the log: Colorful Fluorescent (A) 50% (effect 215803), Melancholy card 20% / 30% (71090100 / 71090110),
Catalyst Creation Engine Fluorescent crystal 30% (gameplay 7602 code 15003; binary, the engine picks [Vlad]), Fluorescent Profound Probe 20%
(12030 in the cost), drop pets from the area dump (gamelog m["pets"]): Cloudgatherer - Sky's Dome 10% once (8120), Kong (8130) 20% once +
13% "replicated 2 times" [Vlad; tlidb rank 6]. Miss Melancholy - Pink (19320) is Drop Quantity only.
Evidence:
  rare drops   size of each rare-memory drop on Machines maps (Shadow, Tomorrow's Direction, Lost Secrets, Hundredfold, Maud's Trick, Crow's
               Wail; the same item picked within 1 s = one drop; same-item pickups 1-20 s apart are rare) -> the whole copy distribution
  Secrets/map  Secrets come as pile sweeps, so only the per-map mean is usable; it scales with the mean copy count. The engine picks the crystal
               at random -> a clean A/B on whether a 30% source adds on top of Colorful's 50%. Base fitted per setup (pets + probe), so Drop
               Quantity changes between setups don't leak in.
Models: once-rule  add-cap (one roll at the sum, cap 100%) / indep-any (each rolls, stop at the first hit = one copy) / indep-each (each rolls,
                   every hit its own copy) / highest (only the biggest chance)
        Kong       list (its 20% rolls with the once-sources, its x3 on every copy after) / copy (both lines on every copy) / drop (both once)
        merge share m = two drops swept into one pickup
Usage: python3 tools/farm/replication_fit.py LOG [LOG ...]
"""
import sys, os, math, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gamelog as G, replication as R
SMAX = 18
RULES = ["indep-each", "indep-any", "highest", "add-cap"]
PLACES = ["list", "copy", "drop"]
LABEL = {"add-cap": "chances add, one roll, cap 100%", "indep-any": "each rolls, stop at first hit", "indep-each": "each rolls, every hit a copy",
         "highest": "only the biggest chance"}
MACHINES = "10154"           # Cruising Mechanical (A) in the cost = his Machines stack
PROBE, SKY, KONG = "12030", "8120", "8130"


def sources(m):
    e = m["effects"]; pets = m.get("pets")
    return dict(colorful="215803" in e, card=30 if "71090110" in e else 20 if "71090100" in e else 0,
                catalyst="15003" in m.get("catalyst", []), probe=PROBE in m["cost"],
                sky=(SKY in pets) if pets else True, kong=(KONG in pets) if pets else True)


def setup_key(m):
    return (tuple(sorted(m["pets"])) if m.get("pets") else None, tuple(sorted(i for i in m["cost"] if i.startswith("120"))))


def load(paths):
    """-> (rare drops [dict(size, sources...)], Colorful Machines maps with the engine [dict(secrets, setup, sources...)])"""
    rows, out = [], []
    for path in paths:
        maps = [m for m in G.parse([path]) if G.is_stack(m)]
        for m in maps:
            m["src"] = sources(m)
            if MACHINES in m["cost"] and m["src"]["colorful"] and m.get("catalyst"):
                out.append(dict(secrets=m["loot"].get("6002", 0), setup=setup_key(m), **m["src"]))
        ev = collections.defaultdict(list)
        for k, t, i, q in sorted(R.pickups([path], maps), key=lambda r: (r[0], r[1])):
            lst = ev[k]
            if lst and lst[-1][1] == i and (t - lst[-1][2]).total_seconds() <= 1.0: lst[-1][0] += q; lst[-1][2] = t
            else: lst.append([q, i, t])
        for k, lst in ev.items():                    # Machines maps only: elsewhere other mechanics replicate too (Vigil maps: Lady Obituary's
            if MACHINES in maps[k]["cost"]:           # Elegy x2 then x2 again -> Maud's x3 / Tomorrow's x3 with no Fluorescent source on 10-30)
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
    return (([0.10] if r["sky"] else []) + ([0.50] if r["colorful"] else []) + ([r["card"] / 100] if r["card"] else [])
            + ([0.30] if r["catalyst"] else []) + ([0.20] if r["probe"] else []))


def extra(ps, rule):
    """distribution of once-copies added to the original"""
    if not ps: return [1.0]
    if rule == "add-cap": q = min(1.0, sum(ps)); return [1 - q, q]
    if rule == "indep-any": q = 1 - math.prod(1 - p for p in ps); return [1 - q, q]
    if rule == "highest": q = max(ps); return [1 - q, q]
    d = [1.0]
    for p in ps: d = conv(d, [1 - p, p])
    return d


def mean_copies(ps, rule):
    if not ps: return 1.0
    if rule == "add-cap": return 1 + min(1.0, sum(ps))
    if rule == "indep-each": return 1 + sum(ps)
    if rule == "indep-any": return 2 - math.prod(1 - p for p in ps)
    return 1 + max(ps)


def size_dist(r, rule, place, k1=0.20, k2=0.13, m=0.0):
    kong = r["kong"]
    ps = once_ps(r) + ([k1] if kong and place == "list" else [])
    K = [(1 - k1) * (1 - k2), k1 * (1 - k2), (1 - k1) * k2, k1 * k2]          # both Kong lines, independent: +0 / +1 / +2 / +3
    per = [0, 1.0] if not kong else ([0, 1 - k2, 0, k2] if place == "list" else conv([0, 1.0], K))
    out = [0.0] * (SMAX + 1)
    for e, pe in enumerate(extra(ps, rule)):
        if not pe: continue
        n = 1 + e
        if kong and place == "drop": d = conv([0] * n + [1], K)
        else:
            d = [1.0]
            for _ in range(n): d = conv(d, per)
        for s, x in enumerate(d): out[s] += pe * x
    return [(1 - m) * a + m * b for a, b in zip(out, conv(out, out))] if m else out


def mean_memories(r, rule, place, k1=0.20, k2=0.13):
    if not r["kong"]: return mean_copies(once_ps(r), rule)
    if place == "list": return mean_copies(once_ps(r) + [k1], rule) * (1 + 2 * k2)
    return mean_copies(once_ps(r), rule) * (1 + k1 + 2 * k2)


def ctx_key(r):
    return tuple(r[k] for k in ("colorful", "card", "catalyst", "probe", "sky", "kong"))


def rare_fit(rows):
    """-> {(rule, place, k2): (loglik, m)} with the best merge share per model"""
    ctx = collections.defaultdict(list)
    for r in rows: ctx[ctx_key(r)].append(min(r["size"], SMAX))
    res = {}
    for rule, place, k2 in itertools.product(RULES, PLACES, [0.13, 0.10]):
        base = {c: size_dist(dict(zip(("colorful", "card", "catalyst", "probe", "sky", "kong"), c)), rule, place, k2=k2) for c in ctx}
        best = None
        for m in [i / 50 for i in range(26)]:
            ll = 0.0
            for c, sizes in ctx.items():
                p = base[c]; pm = [(1 - m) * a + m * b for a, b in zip(p, conv(p, p))] if m else p
                ll += sum(math.log(max(1e-12, pm[s])) for s in sizes)
            if best is None or ll > best[0]: best = (ll, m)
        res[(rule, place, k2)] = best
    return res


def secrets_fit(maps, rule, place):
    """Secrets/map = base(setup) x mean memories x noise (sd = c x mean), base and c per setup -> loglik"""
    ll = 0.0
    for key in {r["setup"] for r in maps}:
        g = [r for r in maps if r["setup"] == key]
        k = [mean_memories(r, rule, place) for r in g]; y = [r["secrets"] / x for r, x in zip(g, k)]; n = len(y)
        if n < 3: continue
        best = None
        for b in [x / 10 for x in range(100, 1500)]:
            c = math.sqrt(sum((v - b) ** 2 for v in y) / (n * b * b))
            if c <= 0: continue
            v = -sum(math.log(c * b * x) for x in k) - n / 2
            if best is None or v > best: best = v
        ll += best
    return ll


def predict(setup, rule, place, k2=0.13, cat=0.79):
    """size distribution per drop (sizes 1..7+) and mean memories for a setup dict (catalyst mixed at its map share)"""
    tot = [0.0] * 8; mean = 0.0
    for c, w in ((True, cat), (False, 1 - cat)):
        r = dict(setup, catalyst=c); p = size_dist(r, rule, place, k2=k2)
        for s in range(1, SMAX + 1): tot[min(s, 7)] += w * p[s]
        mean += w * mean_memories(r, rule, place, k2=k2)
    return tot, mean


def main(paths):
    rows, maps = load(paths)
    print(f"{len(rows)} rare-memory drops; contexts (colorful, card, catalyst, probe, sky, kong):",
          sorted(collections.Counter(ctx_key(r) for r in rows).items()))
    print(f"{len(maps)} Colorful Machines maps with the engine, {sum(r['catalyst'] for r in maps)} with the Fluorescent crystal; setups:",
          dict(collections.Counter(str(r["setup"]) for r in maps)))
    rf = rare_fit(rows)
    joint = []
    for rule, place in itertools.product(RULES, PLACES):
        k2, (ll, m) = max(((k2, rf[(rule, place, k2)]) for k2 in (0.13, 0.10)), key=lambda x: x[1][0])
        sl = secrets_fit(maps, rule, place); joint.append((ll + sl, ll, sl, m, k2, rule, place))
    joint.sort(reverse=True)
    print("\n== joint log-likelihood (rare drop sizes + Secrets/map)")
    for j, ll, sl, m, k2, rule, place in joint:
        tag = "   <- each rolls, stop at first hit, Kong 20% in the list (Vlad's 10-31 read)" if (rule, place) == ("indep-any", "list") else ""
        print(f"  {j:8.2f}  rare {ll:8.2f} (merge {m:.2f}, Kong x2 {k2:.2f})  Secrets {sl:8.2f}   {LABEL[rule]:30s} Kong={place}{tag}")
    num = den = 0.0                                            # crystal effect on log Secrets, stratified by setup and card
    for key in {(r["setup"], r["card"]) for r in maps}:
        a = [math.log(r["secrets"]) for r in maps if (r["setup"], r["card"]) == key and r["catalyst"] and r["secrets"] > 0]
        b = [math.log(r["secrets"]) for r in maps if (r["setup"], r["card"]) == key and not r["catalyst"] and r["secrets"] > 0]
        if len(a) > 1 and len(b) > 1:
            va = sum((x - sum(a) / len(a)) ** 2 for x in a) / (len(a) - 1); vb = sum((x - sum(b) / len(b)) ** 2 for x in b) / (len(b) - 1)
            v = va / len(a) + vb / len(b); num += (sum(a) / len(a) - sum(b) / len(b)) / v; den += 1 / v
    if den:
        eff = num / den; s = 1 / math.sqrt(den)
        print(f"  Fluorescent crystal effect on Secrets (stratified): x{math.exp(eff):.3f} (95% x{math.exp(eff - 1.96 * s):.2f}-x{math.exp(eff + 1.96 * s):.2f})")
    best = joint[0]; col = [r for r in rows if r["colorful"]]
    obs = collections.Counter(min(r["size"], 7) for r in col)
    print(f"\n== sizes of the {len(col)} rare drops on Colorful maps (7 = 7+)")
    print("  observed                                         " + " ".join(f"{obs[s]:5d}" for s in range(1, 8)))
    for j, ll, sl, m, k2, rule, place in [best] + [x for x in joint if (x[5], x[6]) == ("indep-any", "list")]:
        tot = [0.0] * 8
        for r in col:
            p = size_dist(r, rule, place, k2=k2, m=m)
            for s_ in range(1, SMAX + 1): tot[min(s_, 7)] += p[s_]
        print(f"  {LABEL[rule] + ', Kong=' + place:48s} " + " ".join(f"{t:5.1f}" for t in tot[1:]))
    print("\n== per 100 rare drops, Colorful maps, crystal on 79% of maps, no card")
    setups = {"Sky's Dome + Flourishing probe (10-30/31)": dict(colorful=True, card=0, probe=False, sky=True, kong=True),
              "Pink + Fluorescent probe": dict(colorful=True, card=0, probe=True, sky=False, kong=True)}
    for name, st in setups.items():
        for j, ll, sl, m, k2, rule, place in [best] + [x for x in joint if (x[5], x[6]) == ("indep-any", "list")]:
            tot, mean = predict(st, rule, place, k2=k2)
            print(f"  {name:42s} {LABEL[rule] + ', Kong=' + place:44s} " + " ".join(f"{100 * t:5.1f}" for t in tot[1:])
                  + f"   mean {mean:.2f} memories/drop")


if __name__ == "__main__":
    main([a for a in sys.argv[1:] if not a.startswith("--")])
