"""Bottom-up drop model, step 1: naked per-mechanic drop rates from the CN strategy loot tallies.

loot[s][i] / Q[s] = gamma[i] + sum_M beta[i][M] * x[s][M]        (NNLS per item, rows weighted by sqrt(runs))
  Q[s]   = generic quantity multiplier of strategy s (resonance curve, Profound major, Commodities micros, Plunder compasses,
           Flourishing probe) x 2 for the Confusion card
  x[s][M] = instances of mechanic M per map: M-family compasses consumed per run (capped at 2), or 1 if >= 8 points in M's constellation
Result: beta[i][M] = items of i per map from one instance of M at Q = 1 (under the CN average mechanic-specific tree / compass tier),
gamma[i] = generic drops per map at Q = 1 (plane monsters, Plane Watcher chest...).
"""
import collections, math, json, sys, os
import numpy as np
from scipy.optimize import nnls
import runs as RN, features as FT, mech

MECHS = ['Afterlight', 'Arcana', 'ClockworkBallet', 'Creation', 'Cube', 'DarkSurge', 'Gods', 'Hunting', 'Lunaria', 'Machines', 'Might',
         'Mistville', 'Outlaw', 'Overrealm', 'Sandlord', 'Vorax', 'War']

def design(R):
    X, Q, W, names = [], [], [], []
    for r in R:
        f = FT.extract(r)
        row = []
        for M in MECHS:
            c = f.get(f"c:{M}", 0.0); t = f.get(f"t:{M}", 0.0)
            row.append(min(c, 2.0) if c >= 0.5 else (1.0 if t >= 8 else 0.0))
        X.append([1.0] + row); Q.append(f["Q"]); W.append(math.sqrt(r["count"])); names.append(r["key"])
    return np.array(X), np.array(Q), np.array(W), names

def fit(R=None, min_total_value=5.0):
    R = R or RN.load()
    X, Q, W, _ = design(R)
    items = sorted({i for r in R for i in r["loot"] if RN.price(i)})
    beta = {}
    for i in items:
        y = np.array([r["loot"].get(i, 0.0) for r in R]) / Q
        b, res = nnls(X * W[:, None], y * W)
        beta[i] = b
    return beta, R, X, Q

def per_mechanic(beta, min_fe=0.2):
    """FE per map (taxed) at Q=1 per mechanic instance, by item."""
    out = {M: [] for M in ["generic"] + MECHS}
    for i, b in beta.items():
        for j, M in enumerate(["generic"] + MECHS):
            if b[j] > 0:
                v = RN.value(i, b[j])
                if v >= min_fe: out[M].append((v, b[j], i))
    return out

if __name__ == "__main__":
    beta, R, X, Q = fit()
    pm = per_mechanic(beta)
    print(f"{len(R)} strategies; Q range {Q.min():.2f}-{Q.max():.2f}; instances per mechanic:", {M: int((X[:, j + 1] > 0).sum()) for j, M in enumerate(MECHS)})
    for M in ["generic"] + MECHS:
        rows = sorted(pm[M], reverse=True); tot = sum(v for v, _, _ in rows)
        print(f"\n== {M}: {tot:.1f} FE/map per instance at Q=1  (x Q for a real map)")
        for v, q, i in rows[:14]: print(f"   {v:7.2f} FE  {q:9.3f}/map  {RN.name(i)[:46]:46s} {RN.typ(i)[:8]:8s} @ {RN.price(i):.2f}")
