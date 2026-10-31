#!/usr/bin/env python3
"""Drop quantity on his Machines farm: the multiplier chain from his sheet, and the natural experiments in the logs that test it.

Sheet [Vlad 2026-10-31] — "Drop Quantity" lines add into one pool, every "additional" line multiplies on top (tlidb Drop_quantity):
  pool:        Path of Progression 30, Twilight Sparks 30, Kong 18, Sky's Dome 26 (Miss Melancholy - Pink 42), Netherrealm tree 25,
               Flourishing Profound Probe 20, resonance 100 (31; 15 -> 75), Profound 100, Confusion Card +20/+30 when picked
  additional:  Twilight Sparks 13 and 3, tree 12, card 100 (any Confusion Card), Drones 25 and 40 (tree), Cruising (A) 100 (Drones),
               Strength in Numbers 20 (Normal monsters, Drones are Normal), Kong / Sky's Dome "+24% additional Fluorescent Memory Shards"
               (unproven: the Pink-for-Sky's swap tests it), drone card 10 (Conservative - Machine)
  Profound also: +65% monster quantity.
Sources [Vlad]: Shadows only from Drones, ~99% of Secrets from Drones, ~95% of Maud's / Tomorrow's / Lost Secrets / Crow's / Hundredfold from
rares or chests. Counts are drop events (pickups; a drop and its copies = one), Secrets as items / mean copies (they come in pile sweeps).
Experiments in the logs (Colorful Machines maps with the engine): card +30% / +20% DQ, drone card, resonance 15 vs 31, Flourishing on/off,
Strength in Numbers -> Transgression, pets (Kong + Sky's Dome vs Pink), probe (Flourishing vs Fluorescent). Cards last 4 maps (Attempts 0/4),
so they come in blocks.
Usage: python3 tools/farm/quantity.py LOG [LOG ...]
"""
import sys, os, math, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gamelog as G, replication as R

POOL_BASE = {"Path of Progression": 30, "Twilight Sparks": 30, "Netherrealm tree": 25, "Profound": 100}
PET_POOL = {"8130": 18, "8120": 26, "19320": 42}                 # Kong, Sky's Dome, Miss Melancholy - Pink
PET_FMS = {"8130": 0.24, "8120": 0.24}                           # "+24% additional Fluorescent Memory Shards Drop Quantity"
RES_POOL = {0: 15, 1: 30, 3: 45, 7: 60, 15: 75, 31: 100}         # resonance -> Drop Quantity [Vlad]
CARD_POOL = {"71100210": 30, "71100200": 20}
ADD_ALL = [0.13, 0.03, 0.12, 1.00]                               # Twilight Sparks x2, tree, Confusion Card
ADD_DRONES = [0.25, 0.40, 1.00, 0.20]                            # tree x2, Cruising (A), Strength in Numbers (Normal monsters)
REPL = {"215803": 0.5, "71090100": 0.2, "71090110": 0.3, "12030": 0.2}
MACHINES = "10154"


def res_pool(n):
    return max(v for k, v in RES_POOL.items() if n >= k) if n else 15


def load(paths):
    out = []
    for path in paths:
        maps = [m for m in G.parse([path]) if G.is_stack(m)]
        ev = collections.defaultdict(list)
        for k, t, i, q in sorted(R.pickups([path], maps), key=lambda r: (r[0], r[1])):
            lst = ev[k]
            if lst and lst[-1][1] == i and (t - lst[-1][2]).total_seconds() <= 1.0: lst[-1][0] += q; lst[-1][2] = t
            else: lst.append([q, i, t])
        for k, m in enumerate(maps):
            e = m["effects"]
            if MACHINES not in m["cost"] or "215803" not in e or not m.get("catalyst") or not m.get("pets"): continue
            card = next((i for i in e if len(i) == 8 and i[:2] in ("71", "72")), None)
            pets = set(m["pets"])
            out.append(dict(t=m["start"], card=card, pets=pets, res=m["cost"].get("5028", 0), crystal="15003" in m["catalyst"],
                            flour="12000" in m["cost"], fluo="12030" in m["cost"], sin=any("Strength" in G.RN.name(i) for i in m["cost"]),
                            transg=any("Transgression" in G.RN.name(i) for i in m["cost"]),
                            secrets=m["loot"].get("6002", 0), rare_events=sum(1 for q, i, t in ev.get(k, []) if i != "6216"),
                            shadow_events=sum(1 for q, i, t in ev.get(k, []) if i == "6216")))
    return out


def copies(r):
    p = (0.1 if "8120" in r["pets"] else 0) + 0.5 + (0.3 if r["crystal"] else 0) + REPL.get(r["card"], 0) + (0.2 if r["fluo"] else 0)
    kong = "8130" in r["pets"]
    return (1 + p + (0.2 if kong else 0)) * (1.26 if kong else 1.0)


def pool(r, card=True):
    return (100 + sum(POOL_BASE.values()) + sum(PET_POOL.get(p, 0) for p in r["pets"]) + res_pool(r["res"])
            + (20 if r["flour"] else 0) + (CARD_POOL.get(r["card"], 0) if card else 0)) / 100


def chain(r, scope="drones", fms=None, pool_on=None):
    """total quantity multiplier on a memory drop (scope: drones = Secrets / Shadows, plane-exclusive; rares = the big memories).
    Default = the 10-31 read [Vlad + XD's drone column]: plane-exclusive memories from Drones get no pool and no Memory Shards line, only
    the "additional" lines; the big memories (normal) get pool + generic additional + Memory Shards. fms / pool_on override."""
    pool_on = (scope != "drones") if pool_on is None else pool_on
    fms = (scope != "drones") if fms is None else fms
    add = list(ADD_ALL) + (ADD_DRONES if scope == "drones" else []) + ([0.10] if r["card"] == "72020400" and scope == "drones" else [])
    if not r["sin"] and scope == "drones": add.remove(0.20)
    if fms: add += [PET_FMS[p] for p in r["pets"] if p in PET_FMS]
    return (pool(r) if pool_on else 1.0) * math.prod(1 + a for a in add)


def main(paths):
    M = load(paths)
    print(f"{len(M)} Colorful Machines maps with the engine and a pet dump")
    std = [r for r in M if {"8120", "8130"} <= r["pets"] and r["flour"] and r["sin"] and not r["transg"] and r["res"] in (15, 31)]
    r0 = std[0] if std else M[0]
    s0 = dict(r0, card=None, res=31)
    print(f"his chain on a standard map (Kong + Sky's Dome, Flourishing, 31 resonance, no DQ card): pool x{pool(s0):.2f}; Secrets / Shadows (drones, "
          f"plane-exclusive) x{chain(s0):.2f} (x{chain(s0, pool_on=True, fms=True):.1f} if pool and Memory Shards applied), big memories "
          f"x{chain(s0, 'rares'):.1f}; Focus x1.5 on the exclusive ones not included")
    sec = np.mean([r["secrets"] / copies(r) / chain(r) for r in std]) if std else float("nan")
    print(f"naked rates (no quantity, no copies) on standard maps: Secrets {sec:.2f}/map (drones), rare/chest memory drops "
          f"{np.mean([r['rare_events'] / chain(r, 'rares') for r in std]):.3f}/map; observed {np.mean([r['secrets'] for r in std]):.1f} Secrets, "
          f"{np.mean([r['rare_events'] for r in std]):.2f} rare drops, {np.mean([r['shadow_events'] for r in std]):.2f} Shadow drops per map")
    # log Secrets per copy on the contrasts; the sheet's prediction = the change applied alone to a standard map
    OTHER = ("71200100", "71100300", "72020100")                  # +20% compass DQ, +1 Blessed monster, +8% attack round: nothing for Secrets
    CHEST = ("71100000", "71090300")                               # 4-6 Mystery Chests, Bosses drop 8 additional Fluorescent Memories
    feats = [("card +30% DQ", lambda r: r["card"] == "71100210", lambda r: dict(r, card="71100210")),
             ("card +20% DQ", lambda r: r["card"] == "71100200", lambda r: dict(r, card="71100200")),
             ("card +10% add. Drones", lambda r: r["card"] == "72020400", lambda r: dict(r, card="72020400")),
             ("card no bonus (compass/blessed/round)", lambda r: r["card"] in OTHER, lambda r: dict(r, card="71100300")),
             ("card chests / boss memories", lambda r: r["card"] in CHEST, None),
             ("resonance 15 (vs 31)", lambda r: r["res"] == 15, lambda r: dict(r, res=15)),
             ("Transgression for SiN", lambda r: r["transg"], None),
             ("no Flourishing", lambda r: not r["flour"] and not r["fluo"], lambda r: dict(r, flour=False)),
             ("Pink for Sky's Dome", lambda r: "19320" in r["pets"] and "8120" not in r["pets"], lambda r: dict(r, pets=(r["pets"] - {"8120"}) | {"19320"})),
             ("Fluorescent probe for Flourishing", lambda r: r["fluo"], lambda r: dict(r, flour=False, fluo=True))]
    use = [r for r in M if "8130" in r["pets"] and r["secrets"] > 0 and r["res"] in (15, 31)]
    cols = []                                   # [name, indicator vector, [appliers]]; near-identical columns (< 3 maps apart) are merged
    for nm, f, ap in feats:
        v = np.array([f(r) for r in use], float)
        if not 0 < v.sum() < len(use): continue
        for c in cols:
            if np.abs(c[1] - v).sum() < 3: c[0] += " + " + nm; c[2].append(ap); break
        else: cols.append([nm, v, [ap]])
    X = np.column_stack([np.ones(len(use))] + [c[1] for c in cols])
    y = np.array([math.log(r["secrets"] / copies(r)) for r in use]); n, k = X.shape
    b, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X @ b; XtXi = np.linalg.pinv(X.T @ X)
    cov = XtXi @ ((X * res[:, None] ** 2).T @ X) @ XtXi * n / (n - k)
    r0 = dict(card=None, pets={"8130", "8120", "19330", "20120", "20130", "21120", "21130"}, res=31, crystal=True, flour=True, fluo=False, sin=True, transg=False)
    print(f"\n== Secrets per copy, {n} maps (log scale, residual sd {math.sqrt(res @ res / (n - k)):.2f}) vs the sheet (change alone on a standard map)")
    for j, (nm, v, aps) in enumerate(cols, 1):
        se = math.sqrt(cov[j, j]); r1 = dict(r0)
        if all(aps):
            for ap in aps: r1 = ap(r1)
            pr, prp = chain(r1) / chain(r0), chain(r1, pool_on=True, fms=True) / chain(r0, pool_on=True, fms=True)
            sheet = f"read x{pr:.3f}" + (f" (x{prp:.3f} if pool + Memory Shards applied)" if abs(pr - prp) > 1e-3 else "")
        else: sheet = "sheet: no fixed number"
        print(f"  {nm:46s} n={int(v.sum()):3d}  x{math.exp(b[j]):.3f} (95% x{math.exp(b[j] - 1.96 * se):.2f}-x{math.exp(b[j] + 1.96 * se):.2f})   {sheet}")


if __name__ == "__main__":
    main([a for a in sys.argv[1:] if not a.startswith("--")])
