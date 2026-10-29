"""Which mechanic drops which item: lift of each item's per-map count in strategies running mechanic M vs not.
Strategy 'runs M' = M-family compass consumed on most maps (>= 0.5/run) or >= 8 points in M's constellation."""
import collections, sys
import runs as RN, features as FT, mech

def mechanics_of(r):
    f = FT.extract(r); M = set()
    for k, v in f.items():
        if k.startswith("c:") and not k.startswith("c:generic") and v >= 0.5: M.add(k[2:])
        if k.startswith("t:") and not k.startswith("t:generic") and k != "t:Profound" and v >= 8: M.add(k[2:])
    return M, f

def table(R=None, min_val=0.3, min_lift=2.5):
    R = R or RN.load()
    S = [(r, *mechanics_of(r)) for r in R]
    mechs = sorted({m for _, M, _ in S for m in M})
    items = sorted({i for r in R for i in r["loot"]})
    out = {}
    for i in items:
        best = None
        for m in mechs:
            w = [r["loot"].get(i, 0.0) for r, M, _ in S if m in M]; wo = [r["loot"].get(i, 0.0) for r, M, _ in S if m not in M]
            if len(w) < 5 or not wo: continue
            mw, mwo = sum(w) / len(w), sum(wo) / len(wo)
            lift = mw / mwo if mwo > 0 else (float("inf") if mw > 0 else 0)
            if best is None or lift > best[1]: best = (m, lift, mw, len(w))
        if best:
            m, lift, mw, n = best
            val = RN.value(i, mw)
            out[i] = dict(mech=m if lift >= min_lift else "generic", lift=lift, per_map=mw, val=val, n=n)
    return out, mechs, S

if __name__ == "__main__":
    out, mechs, S = table()
    print("mechanics:", mechs)
    rows = sorted(out.items(), key=lambda x: -x[1]["val"])
    print(f"{'id':>8} {'item':44s} {'type':8s} {'mech':14s} {'lift':>7} {'per map':>8} {'FE/map':>7} {'n':>4}")
    for i, d in rows:
        if d["val"] < 0.3: continue
        print(f"{i:>8} {RN.name(i)[:44]:44s} {RN.typ(i)[:8]:8s} {d['mech']:14s} {d['lift']:7.1f} {d['per_map']:8.2f} {d['val']:7.1f} {d['n']:4d}")
