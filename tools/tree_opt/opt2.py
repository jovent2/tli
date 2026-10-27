"""Hard-constraint variant: fill every micro/medium in the prism area, guarantee 2 legendaries (with their left chain),
keep defence locks, then local-search the remaining points (single + double swaps)."""
import sys, copy, json, itertools
sys.path.insert(0, __import__('os').path.dirname(__file__))
import scen as S, opt as O
O.LOCKS = O.defensive_locks()
def chain(k, nid, alloc, prism):
    """cells (with rank 1) needed so nid satisfies pairing, walking left."""
    need = []; cur = nid
    while True:
        c = S.CELLS[k][cur]
        if not c["left"] or any(l in alloc.get(k, {}) or l in need or (prism[0] == k and prism[1] == l) for l in c["left"]): break
        cur = c["left"][0]; need.append(cur)
    return need
def setup(alloc, prism, n_leg=2):
    a = copy.deepcopy(alloc); k = prism[0]
    a[k].pop(prism[1], None)
    locks = dict(O.LOCKS)
    for cid in S.area(prism):
        c = S.CELLS[k][cid]
        if c["kind"] in ("m", "M"):
            a[k][cid] = c["mr"]; locks[(k, cid)] = c["mr"]
            for ch in chain(k, cid, a, prism): a[k].setdefault(ch, 1); locks[(k, ch)] = max(1, locks.get((k, ch), 0))
    legs = [cid for cid in S.area(prism) if S.CELLS[k][cid]["kind"] == "L"]
    have = [cid for cid in legs if a[k].get(cid, 0) > 0]
    for cid in sorted(set(legs) - set(have), key=lambda c: len(chain(k, c, a, prism))):
        if len(have) >= n_leg: break
        for ch in chain(k, cid, a, prism): a[k].setdefault(ch, 1); locks[(k, ch)] = max(1, locks.get((k, ch), 0))
        a[k][cid] = 1; have.append(cid)
    for cid in have[:n_leg]: locks[(k, cid)] = 1
    return a, locks
def trim(a, locks, prism, kw, total=110):
    """remove lowest-value unlocked ranks until within budget."""
    while sum(sum(v.values()) for v in a.values()) > total:
        best = None
        for k in S.PANELS:
            for nid, r in list(a.get(k, {}).items()):
                if r <= locks.get((k, nid), 0): continue
                a2 = copy.deepcopy(a); a2[k][nid] -= 1
                if a2[k][nid] == 0: del a2[k][nid]
                if S.valid(a2, prism): continue
                sc = O.score(a2, prism, kw)[0]
                if best is None or sc > best[0]: best = (sc, a2)
        if best is None: raise RuntimeError("cannot trim")
        a = best[1]
    return a
def search(a, locks, prism, kw, rounds=40):
    O.LOCKS = locks
    cur = O.score(a, prism, kw)
    for _ in range(rounds):
        spent = sum(sum(v.values()) for v in a.values())
        adds, rems = O.moves(a, prism)
        if spent < 110 and adds:
            a = max(adds, key=lambda x: O.score(x, prism, kw)[0]); cur = O.score(a, prism, kw); continue
        rs = sorted(rems, key=lambda x: -O.score(x, prism, kw)[0])[:8]
        improved = False
        for ar in rs:   # single swap
            ad, _ = O.moves(ar, prism)
            if not ad: continue
            bst = max(ad, key=lambda x: O.score(x, prism, kw)[0]); sb = O.score(bst, prism, kw)
            if sb[0] > cur[0] + 1e-6: a, cur, improved = bst, sb, True; break
        if improved: continue
        for ar in rs[:4]:   # double swap: remove two, add two
            _, r2 = O.moves(ar, prism)
            r2 = sorted(r2, key=lambda x: -O.score(x, prism, kw)[0])[:4]
            for arr in r2:
                ad, _ = O.moves(arr, prism)
                if not ad: continue
                b1 = max(ad, key=lambda x: O.score(x, prism, kw)[0])
                ad2, _ = O.moves(b1, prism)
                if not ad2: continue
                b2 = max(ad2, key=lambda x: O.score(x, prism, kw)[0]); sb = O.score(b2, prism, kw)
                if sb[0] > cur[0] + 1e-6: a, cur, improved = b2, sb, True; break
            if improved: break
        if not improved: break
    return a, cur
def run(prism, start, kw={}, n_leg=2):
    a, locks = setup(start, prism, n_leg)
    O.LOCKS = locks
    a = trim(a, locks, prism, kw)
    return search(a, locks, prism, kw)
if __name__ == "__main__":
    out = json.load(open('/tmp/claude-0/-home-claude/51955565-d5d5-5a4a-a40e-88663b34fdef/scratchpad/wl/all.json'))
    start = out[2]["alloc"]
    res = []
    for pr in [("Prophet", "608_176", 4, 3, 2, 0), ("Prophet", "608_176", 4, 3, 3, 0), ("Prophet", "224_176", 4, 3, 0, 0),
               ("Prophet", "352_176", 4, 3, 1, 0), ("Prophet", "480_176", 4, 3, 2, 0), ("Prophet", "480_176", 4, 3, 1, 0)]:
        try:
            a, cur = run(pr, start)
        except Exception as e:
            print(pr, "ERR", e); continue
        print(pr, "x", round(cur[1], 3), "comp", cur[2], "legs", cur[3], "valid", not S.valid(a, pr), {k: sum(v.values()) for k, v in a.items()}, flush=True)
        res.append({"prism": pr, "x": cur[1], "comp": cur[2], "legs": cur[3], "alloc": a})
    json.dump(res, open('/tmp/claude-0/-home-claude/51955565-d5d5-5a4a-a40e-88663b34fdef/scratchpad/wl/best2.json', 'w'))
