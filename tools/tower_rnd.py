"""TOWER Sequence In-Depth R&D odds: 4 picks of chips 1-7, offered 4/2/2/2 (Vlad 2026-10-27); optimal-pick DP per target set."""
import itertools, functools
from fractions import Fraction
N = 7
WAND_ADV = {(1,4,5,7): "explode", (1,3,5,7): "Spell Burst +25%", (1,1,1,5): "cold @800 INT", (2,2,2,4): "Control Spell",
            (3,3,6,7): "Spell Amp +120%", (4,4,5,6): "+35%/-10% cast", (5,5,6,6): "Overload", (2,3,5,6): "+1 Focus/+1 Agi"}
def solve(values, offers=(4,2,2,2), distinct=False):
    """values: {sorted code tuple: value}; returns expected value under optimal picks and P(hit each code)."""
    L = len(offers)
    def offer_sets(k):
        if distinct: return [(c, 1) for c in itertools.permutations(range(1, N+1), k)]
        return [(c, 1) for c in itertools.product(range(1, N+1), repeat=k)]
    OS = {k: offer_sets(k) for k in set(offers)}
    @functools.lru_cache(None)
    def V(state):
        if len(state) == L: return values.get(state, 0.0)
        k = offers[len(state)]; tot = 0.0
        for c, w in OS[k]:
            tot += max(V(tuple(sorted(state + (x,)))) for x in set(c))
        return tot / len(OS[k])
    @functools.lru_cache(None)
    def P(state):   # distribution of final codes under the optimal policy
        if len(state) == L: return {state: 1.0}
        k = offers[len(state)]; out = {}
        for c, w in OS[k]:
            best = max(set(c), key=lambda x: (V(tuple(sorted(state + (x,)))), -x))
            for f, p in P(tuple(sorted(state + (best,)))).items(): out[f] = out.get(f, 0) + p / len(OS[k])
        return out
    return V(()), P(())
for distinct in (False, True):
    print(f"\n=== offers {'distinct' if distinct else 'iid'} 1-7, picks from 4/2/2/2")
    for code, name in [((2,2,2,4), "Control Spell"), ((3,3,6,7), "Spell Amp"), ((4,4,5,6), "+35%"), ((5,5,6,6), "Overload"), ((2,3,5,6), "Focus/Agi")]:
        v, _ = solve({code: 1.0}, distinct=distinct)
        print(f"  only {name:14s} {code}: P = {v*100:.2f}%  -> {640/v:,.0f} FE per hit")
    targets = {(2,2,2,4): 1, (3,3,6,7): 1, (4,4,5,6): 1, (5,5,6,6): 1}
    v, dist = solve(targets, distinct=distinct)
    print(f"  any of the 4 Vlad named: P = {v*100:.2f}% -> {640/v:,.0f} FE per hit;", {WAND_ADV.get(k, k): round(p*100, 2) for k, p in sorted(dist.items(), key=lambda x: -x[1]) if k in WAND_ADV})
    # value-weighted (current-build gains replacing 16% cast; Spell Amp dead now)
    vals = {(5,5,6,6): 26.1, (2,2,2,4): 21.3, (4,4,5,6): 16.0, (2,3,5,6): 12.8}
    v, dist = solve(vals, distinct=distinct)
    hit = sum(p for k, p in dist.items() if k in vals)
    print(f"  max expected gain (Overload/Control/+35%/Focus): EV +{v:.2f}% per try, P(any useful) {hit*100:.2f}% -> {640/v:,.0f} FE per 1%;",
          {WAND_ADV[k]: round(p*100, 2) for k, p in sorted(dist.items(), key=lambda x: -x[1]) if k in WAND_ADV})
print("\n=== take-first-useful-hit, current build vs LW plan values")
for label, vals in [("current", {(5,5,6,6): 26.1, (2,2,2,4): 21.3, (4,4,5,6): 16.0, (2,3,5,6): 12.8}),
                    ("LW plan", {(5,5,6,6): 16.0, (2,2,2,4): 11.7, (4,4,5,6): 5.8, (2,3,5,6): 8.3})]:
    for distinct in (False, True):
        v, dist = solve(vals, distinct=distinct)
        hit = sum(p for k, p in dist.items() if k in vals)
        print(f"  {label:8s} {'distinct' if distinct else 'iid':8s}: P(useful) {hit*100:5.2f}%  cost to first hit {640/hit:6,.0f} FE  avg gain +{v/hit:.1f}%  -> {640/v:.0f} FE per 1%")
# Basic, if it's 4/2/2 picks of 3 chips (assumption)
print("\n=== Basic (assumed 3 picks from 4/2/2)")
for code, name in [((4,5,6), "Cold pen"), ((1,2,6), "8% add spell"), ((2,3,4), "6% ARP")]:
    for distinct in (False, True):
        v, _ = solve({code: 1.0}, offers=(4,2,2), distinct=distinct)
        print(f"  {name:12s} {code} {'distinct' if distinct else 'iid'}: {v*100:.2f}%")
