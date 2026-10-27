"""Price branding a new GoK slate that would replace GoK #2 (see ss14/thea/plans.md).
Usage: python3 tools/slate_brand.py [--pact FE] [--lam FE_PER_1PCT]
Pair values come from engine.py (new slate on the line at 54%, replacing GoK #2); the decision model
(upgrade slot 1, slot 2, accept or restore) is solved exactly over the 6 restores."""
import sys, json, itertools, functools, argparse
sys.path.insert(0, 'tools')
import engine as E

def pair_values():
    b, t = E.load()
    base = E.dps(b, t)["dps"]
    G2 = "Goddess of Knowledge's Divinity #2 (F, lv86)"
    FIX = ["+1 Spell Skill Level", "+8% additional Spell Damage"]
    N = {"F": ["+1 to Max Focus Blessing Stacks"], "S": ["+1 Spell Skill Level"], "C": ["+1 Cold Skill Level"],
         "Z": ["+10% additional damage against Frozen enemies"], "B": ["+20% Frostbite Effect"], "I": ["+12% Intelligence"], "D": []}
    def val(brands):
        bb, tt = E.apply(b, t, {"remove": ["slates:" + G2], "add_slate": [FIX + brands, 54]})
        return E.dps(bb, tt)["dps"] / base
    V = {}
    for a, c in itertools.combinations_with_replacement(N, 2):
        v = val(N[a] + N[c]) if a != c else val(N[a])
        V[a + c] = V[c + a] = v
    return V
V = None
M_FACTOR = 1.0443           # slot left as the crit medium it has now
W = 14                      # 2 Transcendence Wedges
REST = [16, 16, 32, 64, 128, 256]   # restore k+1 cost (Unifying Wedge 16 FE x 1,1,2,4,8,16)
RND = 0.0296
DIST = {
    "random":   {"F": RND, "S": RND, "C": RND, "Z": RND, "B": RND, "I": RND},
    "Arcanist": {"F": 1/6},
    "GoK":      {"S": 1/5},
    "Elem":     {"C": 1/8},
    "Prophet":  {"Z": 1/7, "B": 1/7},
    "Magister": {"I": 1/10},
}
for d in DIST.values(): d["D"] = 1 - sum(d.values())
def pair(a, b):
    global V
    if V is None: V = pair_values()
    if b == "M": return V[a + "D"] * M_FACTOR
    return V[a + b]
def gain(v): return max(0.0, (v - 1) * 100)   # keep GoK #2 if the new slate is worse

def solve(lam, price, max_restores=6):
    def cost(a): return W + (0 if a == "random" else price.get(a, price.get("all", 0)))
    @functools.lru_cache(None)
    def start(k):  # value at the start of round k (k restores used)
        best = (0.0, "quit")
        for a, d in DIST.items():
            ev = -cost(a) + sum(p * mid(k, x) for x, p in d.items())
            best = max(best, (ev, a))
        return best[0]
    def restore_ev(k):
        return -REST[k] + start(k + 1) if k < max_restores else -1e18
    @functools.lru_cache(None)
    def mid(k, x1):  # slot 1 holds x1, slot 2 still the medium
        opts = [lam * gain(pair(x1, "M")), restore_ev(k)]
        for a, d in DIST.items():
            opts.append(-cost(a) + sum(p * end(k, x1, x2) for x2, p in d.items()))
        return max(opts)
    @functools.lru_cache(None)
    def end(k, x1, x2):
        return max(lam * gain(pair(x1, x2)), restore_ev(k))
    # policy trace by simulation-free enumeration: compute expected cost, gain, outcome distribution
    def policy_start(k):
        best = (0.0, "quit")
        for a, d in DIST.items():
            ev = -cost(a) + sum(p * mid(k, x) for x, p in d.items())
            best = max(best, (ev, a))
        return best[1]
    def policy_mid(k, x1):
        opts = [(lam * gain(pair(x1, "M")), "keep medium"), (restore_ev(k), "restore")]
        for a, d in DIST.items():
            opts.append((-cost(a) + sum(p * end(k, x1, x2) for x2, p in d.items()), a))
        return max(opts)[1]
    def policy_end(k, x1, x2):
        return "accept" if lam * gain(pair(x1, x2)) >= restore_ev(k) else "restore"
    # forward pass
    out, ecost = {}, 0.0
    def walk(k, prob):
        nonlocal ecost
        a = policy_start(k)
        if a == "quit": out["quit"] = out.get("quit", 0) + prob; return
        ecost += prob * cost(a)
        for x1, p1 in DIST[a].items():
            q = prob * p1
            a2 = policy_mid(k, x1)
            if a2 == "keep medium":
                key = x1 + "+medium"; out[key] = out.get(key, 0) + q
            elif a2 == "restore":
                ecost += q * REST[k]; walk(k + 1, q)
            else:
                ecost += q * cost(a2)
                for x2, p2 in DIST[a2].items():
                    r = q * p2
                    if policy_end(k, x1, x2) == "accept":
                        key = "".join(sorted(x1 + x2)); out[key] = out.get(key, 0) + r
                    else:
                        ecost += r * REST[k]; walk(k + 1, r)
    walk(0, 1.0)
    def outval(key):
        if key == "quit": return 1.0
        if key.endswith("+medium"): return pair(key[0], "M")
        return pair(key[0], key[1])
    egain = sum(p * gain(outval(k)) for k, p in out.items())
    first = policy_start(0)
    return dict(first=first, after_F=policy_mid(0, "F"), after_S=policy_mid(0, "S"), after_D=policy_mid(0, "D"),
                ecost=ecost, egain=egain, out=out, fe_per_pct=ecost / egain if egain else None)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pact", type=float, nargs="*", default=[0, 10, 25, 50, 100])
    ap.add_argument("--lam", type=float, nargs="*", default=[100, 150, 200], help="FE you'd pay per 1%%")
    a = ap.parse_args()
    for lam in a.lam:
        for P in a.pact:
            r = solve(lam, {"all": P})
            top = sorted(r["out"].items(), key=lambda kv: -kv[1])[:5]
            print(f"FE/1% limit {lam:.0f}, pact {P:.0f} FE: slot1 {r['first']}, after Focus {r['after_F']}, after dead {r['after_D']} | "
                  f"E[cost] {r['ecost']:.0f} FE, E[gain] {r['egain']:.2f}%, {r['fe_per_pct']:.0f} FE/1% | " + ", ".join(f"{k} {v*100:.0f}%" for k, v in top))
