"""Local search for talent allocations under the real pairing rule (left node MAXED before the right one) [Vlad 2026-10-27].

Moves: +1 rank, -1 rank, and pair moves (max the left node and put 1 rank in the right one / strip a right node and its left).
Swap = best removal-type move followed by best add-type move; repeated until no improvement. Budget is fixed (default 110).
score(alloc) -> float is supplied by the caller; valid(alloc) -> list of problems (scen.valid with the prism).
"""
import copy


def total(a):
    return sum(sum(v.values()) for v in a.values())


def _adds(a, panels, cells, valid, locks):
    out = []
    for k in panels:
        nodes = a.get(k, {})
        for nid, c in cells[k].items():
            r = nodes.get(nid, 0)
            if r < c["mr"]:
                a2 = copy.deepcopy(a); a2.setdefault(k, {})[nid] = r + 1
                if not valid(a2):
                    out.append(a2)
                elif r == 0 and c["left"]:            # pair move: max a left node, then 1 rank here
                    for l in c["left"]:
                        a3 = copy.deepcopy(a); a3.setdefault(k, {})[l] = cells[k][l]["mr"]; a3[k][nid] = 1
                        if not valid(a3):
                            out.append(a3)
    return out


def _rems(a, panels, cells, valid, locks):
    out = []
    for k in panels:
        for nid, r in list(a.get(k, {}).items()):
            if r <= locks.get((k, nid), 0):
                continue
            a2 = copy.deepcopy(a); a2[k][nid] = r - 1
            if a2[k][nid] == 0:
                del a2[k][nid]
            if not valid(a2):
                out.append(a2)
            elif locks.get((k, nid), 0) == 0:          # whole node, plus anything that depended on it being maxed
                a3 = copy.deepcopy(a); del a3[k][nid]
                for n2, c2 in cells[k].items():
                    if n2 in a3[k] and nid in c2["left"] and locks.get((k, n2), 0) == 0:
                        del a3[k][n2]
                if not valid(a3):
                    out.append(a3)
    return out


def optimize(a, panels, cells, score, valid, locks=None, budget=110, iters=300, verbose=False, topk=40):
    locks = locks or {}
    a = copy.deepcopy(a)
    cur = score(a)
    for it in range(iters):
        if total(a) < budget:
            adds = [x for x in _adds(a, panels, cells, valid, locks) if total(x) <= budget]
            if adds:
                sc = [(score(x), i) for i, x in enumerate(adds)]
                # value per point so pair moves don't win just by spending more
                best = max(sc, key=lambda s: (s[0] - cur) / max(1, total(adds[s[1]]) - total(a)))
                a, cur = adds[best[1]], best[0]
                continue
        improved = False
        rems = _rems(a, panels, cells, valid, locks)
        rs = sorted(((score(x), i) for i, x in enumerate(rems)), reverse=True)[:topk]
        for s_r, i in rs:
            a_r = rems[i]
            # refill to budget greedily, then compare
            b = a_r; sb = s_r
            for _ in range(budget - total(a_r)):
                adds = [x for x in _adds(b, panels, cells, valid, locks) if total(x) <= budget]
                if not adds:
                    break
                sc = [(score(x), j) for j, x in enumerate(adds)]
                bj = max(sc, key=lambda s: (s[0] - sb) / max(1, total(adds[s[1]]) - total(b)))
                b, sb = adds[bj[1]], bj[0]
            if total(b) <= budget and sb > cur + 1e-9:
                a, cur, improved = b, sb, True
                break
        if verbose:
            print(it, round(cur, 4), total(a))
        if not improved:
            break
    return a, cur
