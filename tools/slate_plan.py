"""Plan a Divinity slate craft that replaces GoK #2 (see ss14/thea/plans.md, docs/crafting.md).
Exact decision model: buy a base (2 fixed legendary nodes), roll each orange slot naked (14 FE, 1/pool) or with a
Divinity Pact (14 + pact, 1/panel pool), keep / restore (Unifying Wedges 16,16,32,64,128,256). Pools exclude nodes
already on the slate. Mediums and the purple are overwritten for free (best medium). Gains are vs GoK #2 after its
free purple overwrite to +12% proj speed. lam = FE you'd pay per 1%.
Usage: python3 tools/slate_plan.py [lam]            rank every base (2 and 3 legendary slots)
       python3 tools/slate_plan.py lam BASE NSLOTS   decision tree for one base (BASE = two node letters)
Nodes: S +1 Spell (GoK) F +1 Focus (Arcanist) A +8% additional spell (Arcanist) C +1 Cold (Elementalist)
       E ele pen per ailment (Elementalist) Z +10% vs Frozen (Prophet) B +20% frostbite effect (Prophet) I +12% INT (Magister)"""
import sys, functools, json
sys.path.insert(0, 'tools')
import engine as E
b, t = E.load()
G2 = "Goddess of Knowledge's Divinity #2 (F, lv86, Spell+Cold)"
g2 = next(s for s in b["slates"] if s["name"] == G2)
g2["lines"] = [l for l in g2["lines"] if "Spell Burst" not in l] + ["+12% Projectile Speed"]   # free purple overwrite first
BASE = E.dps(b, t)["dps"]
L = {"S": ["+1 Spell Skill Level"], "F": ["+1 to Max Focus Blessing Stacks"], "C": ["+1 Cold Skill Level"],
     "A": ["+8% additional Spell Damage"], "Z": ["+10% additional damage against Frozen enemies"], "B": ["+20% Frostbite Effect"],
     "I": ["+12% Intelligence"], "E": ["+9% Elemental Resistance Penetration"]}
MEDS = [["+5 to Max Frostbite Rating"], ["+20% Critical Strike Rating", "+5% Critical Strike Damage"], ["+20% Critical Strike Rating", "+5% Critical Strike Damage"]]
@functools.lru_cache(None)
def value(nodes, nmeds):
    lines = []
    for ch in nodes: lines += L[ch]
    for m in MEDS[:nmeds]: lines += m
    lines += ["+12% Projectile Speed"]
    bb, tt = E.apply(b, t, {"remove": ["slates:" + G2], "add_slate": [lines, 54]})
    return E.dps(bb, tt)["dps"] / BASE
PANELS = {"g": ("S", 4), "a": ("FA", 4), "e": ("CE", 6), "p": ("ZB", 5), "m": ("I", 9)}
PACT = {"g": 277, "a": 70, "e": 170, "p": 180, "m": 50}
NAKED, REST = 14, [16, 16, 32, 64, 128, 256]
def dist(action, present):
    """present: tuple of slot contents + fixed nodes. returns [(outcome, p)]"""
    if action == "naked":
        out, n = [], 0
        for pk, (useful, dead) in PANELS.items():
            u = [x for x in useful if x not in present]
            d = dead - sum(1 for x in present if x == "d" + pk)
            out += [(x, 1) for x in u] + [("d" + pk, d)] if d else [(x, 1) for x in u]
            n += len(u) + d
        return [(x, w / n) for x, w in out]
    useful, dead = PANELS[action]
    u = [x for x in useful if x not in present]
    d = dead - sum(1 for x in present if x == "d" + action)
    n = len(u) + d
    return [(x, 1 / n) for x in u] + ([("d" + action, d / n)] if d else [])
def cost(a): return NAKED + (0 if a == "naked" else PACT[a])
def gain(v): return max(0.0, (v - 1) * 100)
def final_value(fixed, slots):
    nodes = "".join(sorted(fixed + "".join(s for s in slots if s not in ("M",) and not s.startswith("d"))))
    return value(nodes, sum(1 for s in slots if s == "M"))

def solve(fixed, nslots, lam, max_rest=6, actions=("naked", "g", "a", "e", "p", "m")):
    @functools.lru_cache(None)
    def st(k, slots):
        opts = [(lam * gain(final_value(fixed, slots)), ("accept",))]
        if k < max_rest and any(s != "M" for s in slots):
            opts.append((-REST[k] + st(k + 1, ("M",) * nslots)[0], ("restore",)))
        if "M" in slots:
            i = slots.index("M")
            present = tuple(fixed) + slots
            for a in actions:
                ev = -cost(a)
                for x, p in dist(a, present):
                    ev += p * st(k, slots[:i] + (x,) + slots[i + 1:])[0]
                opts.append((ev, ("roll", i, a)))
        return max(opts, key=lambda o: o[0])
    out, tot, rolls = {}, [0.0], {}
    mass = [0.0] * (max_rest + 2); mass[0] = 1.0
    def walk(k, slots, pr):
        ev, act = st(k, slots)
        if act[0] == "accept":
            key = fixed + "+" + "".join(sorted(s if not s.startswith("d") else "-" for s in slots))
            p0, v0 = out.get(key, (0, final_value(fixed, slots)))
            out[key] = (p0 + pr, v0); return
        if act[0] == "restore":
            tot[0] += pr * REST[k]; mass[k + 1] += pr; return
        _, i, a = act
        rolls[a] = rolls.get(a, 0) + pr; tot[0] += pr * cost(a)
        for x, p in dist(a, tuple(fixed) + slots):
            walk(k, slots[:i] + (x,) + slots[i + 1:], pr * p)
    for k in range(max_rest + 1):
        if mass[k] > 0: walk(k, ("M",) * nslots, mass[k])
    restores_used = sum(mass[1:])
    eg = sum(p * gain(v) for p, v in out.values())
    first = st(0, ("M",) * nslots)[1]
    return dict(net=st(0, ("M",) * nslots)[0], cost=tot[0], gain=eg, out=out, rolls=rolls, first=first,
                asis=gain(final_value(fixed, ("M",) * nslots)))

NAMES = {"g": "GoK pact", "a": "Arcanist pact", "e": "Elem pact", "p": "Prophet pact", "m": "Magister pact", "naked": "naked"}
def show(fixed, nslots, lam, price=None):
    r = solve(fixed, nslots, lam)
    top = sorted(r["out"].items(), key=lambda kv: -kv[1][0])[:5]
    pr = f"{price:4d}" if price is not None else "   ?"
    tot = r["cost"] + (price or 0)
    print(f"{fixed} {nslots}leg base {pr}: as bought +{r['asis']:.1f}% | rolls+restores {r['cost']:4.0f} FE, total {tot:5.0f}, E[gain] {r['gain']:5.2f}%, "
          f"{tot / r['gain'] if r['gain'] else 0:4.0f} FE/1% | max base price at {lam} FE/1%: {r['net']:5.0f} | "
          + ", ".join(f"{NAMES[a]} {n:.2f}" for a, n in sorted(r['rolls'].items(), key=lambda kv: -kv[1])) + " | ends "
          + ", ".join(f"{k} x{v:.3f} {p*100:.0f}%" for k, (p, v) in top))
    return r
def tree(fixed, nslots, lam, rounds=(0,)):
    acts = ("naked", "g", "a", "e", "p", "m")
    @functools.lru_cache(None)
    def st(k, slots):
        opts = [(lam * gain(final_value(fixed, slots)), ("accept",))]
        if k < 6 and any(s != "M" for s in slots):
            opts.append((-REST[k] + st(k + 1, ("M",) * nslots)[0], ("restore",)))
        if "M" in slots:
            i = slots.index("M"); present = tuple(fixed) + slots
            for a in acts:
                ev = -cost(a) + sum(p * st(k, slots[:i] + (x,) + slots[i + 1:])[0] for x, p in dist(a, present))
                opts.append((ev, ("roll", i, a)))
        return max(opts, key=lambda o: o[0])
    def show(k, slots, depth, pr):
        ev, act = st(k, slots)
        lab = " ".join(s if not s.startswith("d") else "dead" for s in slots)
        if act[0] == "roll":
            print("  " * depth + f"[{lab}] ({pr*100:.1f}%) -> roll slot {act[1]+1} with {NAMES[act[2]]}")
            agg = {}
            for x, p in dist(act[2], tuple(fixed) + slots):
                key = x if not x.startswith("d") else "dead"
                agg.setdefault(key, [0, slots[:act[1]] + (x,) + slots[act[1]+1:]])[0] += p
            for key, (p, ns) in agg.items():
                show(k, ns, depth + 1, pr * p)
        else:
            print("  " * depth + f"[{lab}] ({pr*100:.1f}%) x{final_value(fixed, slots):.3f} -> {act[0]}")
    for k in rounds:
        print(f"--- {fixed}, round after {k} restores")
        show(k, ("M",) * nslots, 0, 1.0)

if __name__ == "__main__":
    import itertools
    lam = float(sys.argv[1]) if len(sys.argv) > 1 else 150
    if len(sys.argv) > 3:
        tree(sys.argv[2], int(sys.argv[3]), lam, rounds=(0, 4, 6))
        show(sys.argv[2], int(sys.argv[3]), lam)
    else:
        rows = []
        for a, c in itertools.combinations("SFACZBIE", 2):
            for n in (2, 3):
                r = solve(a + c, n, lam)
                rows.append((r["net"], a + c, n, r["gain"], r["cost"]))
        for net, fx, n, g, c in sorted(rows, reverse=True)[:25]:
            print(f"{fx} {n} legendary slots: worth up to {net:5.0f} FE | then ~{c:4.0f} FE of rolls/restores for +{g:.1f}% expected")
