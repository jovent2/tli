"""Weighted ridge regression of per-run value (steady and jackpot) and duration on the strategy features."""
import sys, os, collections, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN, features as F
RN.PRICES["100300"] = {"id": "100300", "price_fe": 1.0}
JACK = 1000.0

def split_value(r):
    steady = jack = 0.0
    for i, q in r["loot"].items():
        v = RN.value(i, q)
        if (RN.price(i) or 0) >= JACK: jack += v
        else: steady += v
    return steady, jack

def design(R, cols):
    X = np.zeros((len(R), len(cols)))
    for a, r in enumerate(R):
        for b, c in enumerate(cols):
            X[a, b] = 1.0 if c == "const" else r["f"].get(c, 0.0)
    return X

def wls(X, y, w, lam=1.0):
    W = np.sqrt(w)[:, None]
    A = X * W; b = y * W[:, 0]
    reg = lam * np.eye(X.shape[1]); reg[0, 0] = 0
    beta = np.linalg.solve(A.T @ A + reg, A.T @ b)
    pred = X @ beta
    r2 = 1 - np.sum(w * (y - pred) ** 2) / np.sum(w * (y - np.average(y, weights=w)) ** 2)
    return beta, r2

def main():
    R = RN.load()
    for r in R:
        r["f"] = F.extract(r); r["steady"], r["jack"] = split_value(r)
    cnt = collections.Counter()
    for r in R:
        for k, v in r["f"].items():
            if k.startswith(("c:", "t:", "probe:")) and v: cnt[k] += r["count"]
    cols = ["const"] + [k for k, n in cnt.items() if n >= 150 and not k.startswith("ct:")]
    X = design(R, cols); w = np.array([r["count"] for r in R], float)
    Q = np.array([r["f"]["Q"] for r in R])
    out = {}
    for name, y in (("steady/Q", np.array([r["steady"] for r in R]) / Q), ("jack", np.array([r["jack"] for r in R])), ("dur_s", np.array([r["dur_s"] for r in R]))):
        beta, r2 = wls(X, y, w, lam=2.0); out[name] = beta
        print(f"\n== {name}: weighted R2 {r2:.2f}")
    print(f"\n{'feature':34s} {'runs':>6s} {'steady/Q':>9s} {'jackpot':>8s} {'dur_s':>7s}")
    for b, c in enumerate(cols):
        print(f"{c:34s} {int(cnt.get(c, w.sum())):6d} {out['steady/Q'][b]:9.2f} {out['jack'][b]:8.2f} {out['dur_s'][b]:7.1f}")
    return R, cols, out

if __name__ == "__main__":
    main()
