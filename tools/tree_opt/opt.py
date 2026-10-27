import sys, time, copy
sys.path.insert(0, __import__('os').path.dirname(__file__))
import scen as S
TOTAL = 110
def need_comp():
    b, tr = S.build_new(S.current_alloc(), 0)
    sh = S.E.sheet(b, tr)
    R = S.E.skill_value("Restrain", sh["level_support_plain"], r"([\d.]+)% Sealed Mana Compensation")
    return 150 - 100 - R, R, sh["level_support_plain"]
NEED, R, LV = need_comp()
def score(alloc, prism, kw):
    x, comp, legs, r = S.evaluate(alloc, prism, **kw)
    pen = 0
    if prism:
        if comp < NEED: pen += (NEED - comp) * 0.05      # strong penalty per missing % compensation
        if legs < 2: pen += 0.5
    return x - pen, x, comp, legs
def moves(alloc, prism):
    adds, rems = [], []
    for k in S.PANELS:
        nodes = alloc.get(k, {})
        for nid, c in S.CELLS[k].items():
            r = nodes.get(nid, 0)
            if r < c["mr"]:
                a2 = copy.deepcopy(alloc); a2[k][nid] = r + 1
                if not S.valid(a2, prism): adds.append(a2)
            if r > 0:
                a2 = copy.deepcopy(alloc); a2[k][nid] = r - 1
                if a2[k][nid] == 0: del a2[k][nid]
                if not S.valid(a2, prism): rems.append(a2)
    return adds, rems
def optimize(alloc, prism, kw, iters=60, verbose=False):
    alloc = copy.deepcopy(alloc)
    if prism:   # free the prism cell
        k, nid = prism[0], prism[1]
        alloc[k].pop(nid, None)
    cur = score(alloc, prism, kw)
    for it in range(iters):
        spent = sum(sum(v.values()) for v in alloc.values())
        adds, rems = moves(alloc, prism)
        if spent < TOTAL and adds:
            best = max(adds, key=lambda a: score(a, prism, kw)[0])
            alloc = best; cur = score(alloc, prism, kw); continue
        # try swap: best removal then best add
        sc_r = sorted(((score(a, prism, kw)[0], i) for i, a in enumerate(rems)), reverse=True)[:6]
        improved = False
        for s_r, i in sc_r:
            a_r = rems[i]
            adds2, _ = moves(a_r, prism)
            if not adds2: continue
            best = max(adds2, key=lambda a: score(a, prism, kw)[0])
            sb = score(best, prism, kw)
            if sb[0] > cur[0] + 1e-6:
                alloc, cur, improved = best, sb, True
                break
        if not improved: break
        if verbose: print(it, round(cur[1], 4), cur[2], cur[3])
    return alloc, cur
if __name__ == "__main__":
    print(f"comp needed {NEED:.1f}% (Restrain {R:.1f}% at support lv{LV})")
    base = S.current_alloc()
    base["Warlock"] = {"96_80": 3, "224_80": 3, "352_80": 3, "480_80": 3, "608_176": 1, "480_176": 3, "352_464": 3, "480_464": 3, "736_368": 2}
    t0 = time.time()
    pr = ("Prophet", "608_176", 4, 3, 3, 0)
    al, cur = optimize(base, pr, {}, verbose=True)
    print("time", round(time.time() - t0, 1), "s", cur)
    for k, v in al.items(): print(k, sum(v.values()), dict(sorted(v.items(), key=lambda kv: (int(kv[0].split('_')[0]), int(kv[0].split('_')[1])))))

# ---------------------------------------------------------------- defence locks
DEF_KEYS = ("es.", "life.", "res.", "block")
def defensive_locks():
    cur = S.current_alloc(); locks = {}
    for k, nodes in cur.items():
        for nid, r in nodes.items():
            keys = [st.key for l in S.CELLS[k][nid]["lines"] for st in S.E.stats.parse(l)]
            if keys and all(any(kk.startswith(d) for d in DEF_KEYS) for kk in keys):
                locks[(k, nid)] = r
    return locks
LOCKS = {}
_moves = moves
def moves(alloc, prism):
    adds, rems = _moves(alloc, prism)
    rems = [a for a in rems if all(a.get(k, {}).get(n, 0) >= r for (k, n), r in LOCKS.items())]
    return adds, rems
