"""TOWER In-Depth R&D: exact expectimax over every offer (4/2/2/2 picks of chips 1-7), values = damage gain of each wand sequence vs the one held. Prints the full pick table."""
import itertools, functools
# gains vs S holding 8% Cold pen (current build): x1.261/1.036 etc.
base = 1.036
vals = {(5,5,6,6): (1.261/base-1)*100, (2,2,2,4): (1.213/base-1)*100, (4,4,5,6): (1.160/base-1)*100, (2,3,5,6): (1.128/base-1)*100}
print({k: round(v, 1) for k, v in vals.items()})
offers = (4,2,2,2)
@functools.lru_cache(None)
def V(state):
    if len(state) == 4: return vals.get(state, 0.0)
    k = offers[len(state)]; cs = list(itertools.product(range(1,8), repeat=k))
    return sum(max(V(tuple(sorted(state+(x,)))) for x in set(c)) for c in cs)/len(cs)
@functools.lru_cache(None)
def dist(state):
    if len(state) == 4: return {state: 1.0}
    k = offers[len(state)]; cs = list(itertools.product(range(1,8), repeat=k)); out = {}
    for c in cs:
        best = max(sorted(set(c)), key=lambda x: V(tuple(sorted(state+(x,)))))
        for f, p in dist(tuple(sorted(state+(best,)))).items(): out[f] = out.get(f, 0) + p/len(cs)
    return out
ev = V(()); d = dist(())
print(f"EV per try +{ev:.2f}%  -> {640/ev:.0f} FE per 1%; P(useful) {sum(p for k,p in d.items() if k in vals)*100:.2f}%")
print({k: round(p*100, 2) for k, p in d.items() if k in vals})
def order(state):
    sc = {x: V(tuple(sorted(state+(x,)))) for x in range(1,8)}
    return " > ".join(f"{x}({v:.1f})" for x, v in sorted(sc.items(), key=lambda kv: -kv[1]) if v > 0) or "nothing"
print("\npick 1:", order(()))
for a in range(1,8):
    if V((a,)) > 0: print(f"  have {a}: pick 2:", order((a,)))
for s in itertools.combinations_with_replacement(range(1,8), 2):
    if V(s) > 0: print(f"  have {s}: pick 3:", order(s))
for s in itertools.combinations_with_replacement(range(1,8), 3):
    if V(s) > 0: print(f"  have {s}: pick 4:", order(s))
# chase-one comparison and greedy-max-P comparison
for code in vals:
    @functools.lru_cache(None)
    def W(state, code=code):
        if len(state) == 4: return 1.0 if state == code else 0.0
        k = offers[len(state)]; cs = list(itertools.product(range(1,8), repeat=k))
        return sum(max(W(tuple(sorted(state+(x,)))) for x in set(c)) for c in cs)/len(cs)
    p = W(()); print(f"chase {code} only: {p*100:.2f}%/try, {640/p:,.0f} FE per hit, {640/(p*vals[code]):.0f} FE per 1%")
print("\n--- keep rolling after a hit (worse hits overwrite, so they count negative)")
names = {(5,5,6,6): "Overload", (2,2,2,4): "Control", (4,4,5,6): "+35%", (2,3,5,6): "Focus"}
for held in [(2,3,5,6), (4,4,5,6), (2,2,2,4)]:
    hv = vals[held]
    rel = {k: v - hv for k, v in vals.items() if k != held}
    for dead in [(1,4,5,7), (1,3,5,7), (1,1,1,5), (3,3,6,7)]: rel[dead] = -hv
    @functools.lru_cache(None)
    def U(state, rel=tuple(sorted(rel.items()))):
        r = dict(rel)
        if len(state) == 4: return r.get(state, 0.0)
        k = offers[len(state)]; cs = list(itertools.product(range(1,8), repeat=k))
        return sum(max(U(tuple(sorted(state+(x,)))) for x in set(c)) for c in cs)/len(cs)
    e = U(())
    print(f"  holding {names[held]:8s}: EV +{e:.2f}%/try -> {640/e:,.0f} FE per 1%")
