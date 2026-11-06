#!/usr/bin/env python3
"""Does the drop-quantity text predict the data? Per family and loot item, each player's setup is turned into the text's two
multipliers — the flat pool (1 + resonance (capped +100%) + Sinful + probe + +2%/+1% micros) and the additional product (DS affixes,
Generous, Bountiful, the family's additional lines, Vigil compasses) — and observed log(drops per run) is regressed on log(flat)
and log(additional) with hero and the other compasses as controls. Slope 1.0 = the loot scales exactly as written; 0 = that class
does nothing to it. Cards and pets are not logged, conditional lines (Bounty Order, Fright stacks, White Night) are assumed always on,
so slopes under 1 are the realised share of the written effect.  Usage: python3 tools/farm/texttest.py
"""
import sys, math
import numpy as np
sys.path.insert(0, '/home/claude/tli/tools/farm')
import runs as RN, fit as F
R = F.load_all()
def q(r, n): return sum(v for i, v in r['cost'].items() if RN.name(i) == n)
def cnt(r, s): return sum(c for (con, ln), c in r['nodes'].items() if s in ln)
def flat(r):
    return 1 + 1.0 + 0.4 * q(r, 'Sinful_Plunder_Compass') + 0.8 * q(r, 'Sinful_Plunder_Compass_%28Artifact%29') \
         + 0.4 * q(r, 'Flourishing_Deep_Space_Probe') + 0.02 * cnt(r, 'In Netherrealm stages, +2% Drop Quantity') + 0.01 * cnt(r, 'In Netherrealm stages, +1% Drop Quantity')
def add_common(r):
    return 1.15 ** (q(r, 'Deep_Space_Resonance') / 2) * 1.15 ** q(r, 'Generous_Elite_Compass') * 1.6 ** q(r, 'Bountiful_Elite_Compass')
def add_outlaw(r):
    return add_common(r) * (1.23 if cnt(r, 'Super Sonic') or cnt(r, 'Hyper-Hardened') else 1) * 1.01 ** cnt(r, '+1% additional Drop Quantity for all Security') * 1.06 ** cnt(r, '+6% additional Drop Quantity for all Security')
def add_vigil(r):
    return add_common(r) * 1.01 ** cnt(r, '+1% additional Drop Quantity for the Vigil') * 1.08 ** cnt(r, '+8% additional Drop Quantity for the Vigil') * 1.12 ** cnt(r, 'During White Night Mode, +12%') \
         * (2.0 ** q(r, 'Evernight_Vigil_Compass')) * (3.0 ** q(r, 'All-Evil_Vigil_Compass'))
def add_overrealm(r):
    return add_common(r) * 1.015 ** cnt(r, '+1.5% additional Drop Quantity in the Overrealm') * 1.03 ** cnt(r, '+3% additional Drop Quantity in the Over') * 1.06 ** cnt(r, '+6% additional Drop Quantity in the Over') * 1.10 ** cnt(r, '+10% additional Drop Quantity in the Over') * 1.02 ** cnt(r, '+2% additional Drop Quantity in the Over') * 1.04 ** cnt(r, '+4% additional Drop Quantity in the Over')
def add_machines(r):
    return add_common(r) * 1.2 ** q(r, 'Strength_in_Numbers_Soldier_Compass') * 1.74 ** q(r, 'Transgression_Plunder_Compass') * 1.25 ** cnt(r, '+25% additional Drop Quantity for Drones') * 1.4 ** cnt(r, '+40% additional Drop Quantity for Drones')
def test(name, fam, item, addf, controls, pred=None):
    rows = [r for r in F.family_rows(R, F.FAMILIES[fam]) if pred is None or pred(r)]
    recs = [(math.log(flat(r)), math.log(addf(r)), math.log(r['loot'][item]), min(r['count'], 150), r['hero'], [q(r, c) for c in controls]) for r in rows if r['loot'].get(item, 0) * r['count'] >= 3]
    if len(recs) < 25: print(name, 'too few'); return
    heroes = sorted({x[4] for x in recs})
    X = np.array([[1, x[0], x[1]] + [1.0 if x[4] == h else 0.0 for h in heroes[1:]] + x[5] for x in recs]); y = np.array([x[2] for x in recs]); w = np.array([x[3] for x in recs], float)
    keep = [j for j in range(X.shape[1]) if j == 0 or X[:, j].std() > 0]; X = X[:, keep]
    sw = np.sqrt(w); b, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
    res = y - X @ b; n, k = X.shape
    bread = np.linalg.pinv((X * w[:, None]).T @ X); meat = (X * (w * res)[:, None]).T @ (X * (w * res)[:, None]); se = np.sqrt(np.diag(bread @ meat @ bread * n / (n - k)))
    fl = [math.exp(x[0]) for x in recs]; ad = [math.exp(x[1]) for x in recs]
    print(f"{name:30s} n={n:3d} | flat {b[1]:+.2f} ({b[1]-1.96*se[1]:+.2f}..{b[1]+1.96*se[1]:+.2f}) spread {min(fl):.1f}-{max(fl):.1f} | additional {b[2]:+.2f} ({b[2]-1.96*se[2]:+.2f}..{b[2]+1.96*se[2]:+.2f}) spread {min(ad):.1f}-{max(ad):.1f} | sd {math.sqrt(np.average(res**2, weights=w)):.2f}")
C = ['Alert_Outlaw_Compass', 'All-Evil_Vigil_Compass', 'Containment_Overrealm_Compass', 'Lunar_Stele_Lunaria_Compass', 'Evernight_Vigil_Compass', 'Shadow_Overrealm_Compass', 'Cruising_Mechanical_Compass_%28Artifact%29', 'Colorful_Fluorescent_Compass_%28Artifact%29', 'Fluorescent_Deep_Space_Probe']
print('slope: 1.0 = multiplies as written, 0 = that class does nothing to this loot')
test('Outlaw: Warlock', 'outlaw', '360404', add_outlaw, C)
test('Outlaw: Vanguard', 'outlaw', '360405', add_outlaw, C)
test('Outlaw: FE (whole map)', 'outlaw', '100300', add_outlaw, C)
test('Vigil: Remnants', 'vigil', '394119', add_vigil, C)
test('Vigil: FE (whole map)', 'vigil', '100300', add_vigil, C)
test('Overrealm: FE (whole map)', 'overrealm', '100300', add_overrealm, C)
test('Overrealm: Sprouts', 'overrealm', '5031', add_overrealm, C)
test('Overrealm: Secrets', 'overrealm', '6002', add_overrealm, C)
test('Machines DS: Secrets', 'machines', '6002', add_machines, C)
test('Machines DS: FE', 'machines', '100300', add_machines, C)
test('Lunaria: FE', 'lunaria', '100300', add_common, C)
