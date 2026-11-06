#!/usr/bin/env python3
"""Forward drop model per mechanic family: base x pool^a x additional^b x free compass effects, fitted on every logged
Deep Space strategy of the family, with the text supplying the pool / additional multipliers of every known line and the data
supplying the exponents (a, b), the base, and the effect of compasses whose text is conditional (Generous, Bountiful, probes...).

Checkpoint 2 (pets per phase, FE split):
  Pets. A player carries 3 regular drop pets + the season's special slots (always up). Regular slots: the Fuel trio (Chalk / Surging
  Gold / Twilight Sparks) all map, swapped to the Outlaw trio (Prof. SOURCE / Shro-Shroom / Sparks) for the Carjack. Special slots:
  Lady Obituary + Miss Melancholy - Azure (Vigil), Avatar of Moon + Miss Melancholy - Cyan (Lunaria), Eternity Summoner + Plaintive
  Ball of Thread - Flower (Dark Surge) - assumed for every CN player, rank 6. Which lines work on which loot comes from the XD matrix
  (data/ext/pactspirit_drop_effects.json); generic map monsters (no matrix entry) take every line. Replicates (Prof. SOURCE recode,
  Elegy, Avatar of Moon strumming) count as x(1 + 2p): replicated once, then again. Chalk's 1.3% fuel set per kill is ignored [Vlad].
  Mechanic loot (mods, Remnants, Lunar Dust...): one phase, one pet set:
    pool_s = 1 + 1.00 (resonance, capped) + 0.25 (Path) + 0.4 Sinful + 0.8 Sinful(A) + 0.4 Flourishing + 0.02 Profound micros
             + 0.01 Commodities micros + flat pet lines that work;  add_s = 1.15^(DS affixes) x family lines x compass text x pet add x replicates
    log q_si = log base_i + a_i log pool_s + b_i log add_s + sum_c gamma_ic x_sc + hero,   WLS (runs, cap 150), ridge 0.5 on gammas, HC1.
  FE (whole map) = generic FE + mechanic FE, each with its own pets, fitted jointly (nonlinear least squares in log space):
    FE_s = exp(sum_c gamma_c x_sc + hero) x [ B_g pool_g^a add_g + B_m pool_m^a add_m^b ]
    generic: pool_g = pool with Fuel-trio flat, add_g = DS affixes x Fuel-trio additional (fuel lines work on map monsters);
    mechanic: pool_m / add_m as the mechanic's loot (family lines, compass text, phase pets). The fit decides the split B_m / B_g.
Output: data/ext/model/checkpoint2.md / .json, and the calibration against Vlad's own maps (--logs).
  python3 tools/farm/model.py [--family outlaw|vigil|lunaria|darksurge|all] [--md out.md] [--json out.json] [--logs LOG ...]
"""
import argparse
import collections
import glob
import json
import math
import os
import re
import sys

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN  # noqa: E402
import ds_scan as D  # noqa: E402

STAGES = ["week3", "week2", "day7", "day6", "day5", "day4", "day3", "day2", "day1"]
EXT = RN.EXT
MATRIX = json.load(open(os.path.join(EXT, "pactspirit_drop_effects.json")))
AFF = {s: {str(r["rank"]): r["lines"] for r in v} for s, v in MATRIX["servant_affixes"].items()}
SNAME = {x["slug"]: x["name"] for x in MATRIX["servants"]}
FRIGHT = 3.5
FUEL_TRIO = ["SSR6330", "SR6320", "SSR19330"]            # Chalk, Surging Gold, Twilight Sparks
OUTLAW_TRIO = ["SSR16130", "SR16120", "SSR19330"]        # Prof. SOURCE, Shro-Shroom, Twilight Sparks
SPECIAL = {"vigil": ["SSR20130", "SR20120"], "lunaria": ["SSR19130", "SR19120"], "darksurge": ["SSR6230", "SR6220"]}
FAMILIES = {
    "outlaw": dict(compasses=["Alert_Outlaw_Compass"], cons=("Outlaw",), play=("otherworld_special_action", "security_guard"), regular=OUTLAW_TRIO),
    "vigil": dict(compasses=["All-Evil_Vigil_Compass", "Evernight_Vigil_Compass", "Phantom_Vigil_Compass"], cons=("Afterlight",), play=("night_watch", "night_watch"), regular=FUEL_TRIO),
    "lunaria": dict(compasses=["Lunar_Stele_Lunaria_Compass", "Pristine_Lunaria_Compass", "Moonlit_Casket_Lunaria_Compass", "Lunaria_Compass"], cons=("Lunaria",), play=("music_performance", "music_performance"), regular=FUEL_TRIO),
    "darksurge": dict(compasses=["Divine_Warrior_Dark_Surge_Compass", "Bandit_Dark_Surge_Compass", "Dark_Surge_Compass"], cons=("Dark_Surge",), play=("dark_tide", "dark_tide"), regular=FUEL_TRIO),
}
LOOT_TYPE = [("Flame_Elementium", "fuel"), ("Flame_Sand", "flame_sand"), ("Expansion_Mod", "component"), ("Base_Mod", "component"), ("Fossil", "fossil"),
             ("Divine_Remnant", "void_divinity_crafting_material"), ("Divinity", "void_divinity_crafting_material"), ("Secret", "memory_fluorescence"),
             ("Shadow", "memory_fluorescence"), ("Memory", "memory_fluorescence"), ("Lunar", "hero_memory_revival_material"), ("Corrosion", "corrosion_material"),
             ("TOWER_Token", "tower_chip")]
LINES = {
    "outlaw": [("+1% additional Drop Quantity for all Security", "add", 0.01), ("+6% additional Drop Quantity for all Security", "add", 0.06),
               ("Super Sonic", "add", 0.23), ("Hyper-Hardened", "add", 0.23), ("for every 10 Escort Bodyguard", "add", 0.10),
               ("+30% additional Drop Quantity for all Security personnel after", "add", 0.30 * 0.5)],   # Bounty Orders: assume activated half the time on CN
    "vigil": [("+1% additional Drop Quantity for the Vigil", "add", 0.01), ("+8% additional Drop Quantity for the Vigil", "add", 0.08),
              ("+15% additional Drop Quantity for the Vigil", "add", 0.15), ("During White Night Mode, +12%", "add", 0.12)],
    "lunaria": [("+1% additional Drop Quantity for Lunaria", "add", 0.01), ("+4% additional Drop Quantity for Lunaria", "add", 0.04),
                ("+6% additional Drop Quantity for Lunaria", "add", 0.06)],
    "darksurge": [],
}
COMPASS_TEXT = {"All-Evil_Vigil_Compass": ("vigil", FRIGHT + 1), "Evernight_Vigil_Compass": ("vigil", 2.0), "Pristine_Lunaria_Compass": ("lunaria", 2.0)}
FLAT_COMPASS = {"Sinful_Plunder_Compass": 0.4, "Sinful_Plunder_Compass_%28Artifact%29": 0.8, "Flourishing_Deep_Space_Probe": 0.4}
FREE = ["Generous_Elite_Compass", "Bountiful_Elite_Compass", "Compass_Deep_Space_Probe", "Gear_Deep_Space_Probe", "Fluorescent_Deep_Space_Probe",
        "Alert_Outlaw_Compass", "All-Evil_Vigil_Compass", "Evernight_Vigil_Compass", "Lunar_Stele_Lunaria_Compass", "Conquering_Novel_Compass",
        "Divine_Warrior_Dark_Surge_Compass", "Containment_Overrealm_Compass", "Shadow_Overrealm_Compass", "Full_Load_Outlaw_Compass", "Lavish_Novel_Compass"]
FE = "100300"


def loot_type(item):
    n = RN.name(item)
    for k, t in LOOT_TYPE:
        if k in n:
            return t
    return "legendary_gear" if (RN.price(item) or 0) > 300 else None


def line_effect(l, loot):
    """-> ('flat', x) | ('add', mult) | None for one pet line on this loot type (rank 6 text)."""
    l = l.strip()
    m = re.match(r"\+\s?(\d+)% Drop Quantity( for TOWER Securities| from Wraiths| in the Overrealm)?$", l)
    if m:
        return "flat", int(m.group(1)) / 100
    m = re.match(r"\+(\d+(?:\.\d+)?)% additional Drop Quantity( from all Wraiths in the Vigil)?$", l)
    if m:
        return "add", 1 + float(m.group(1)) / 100
    m = re.match(r"\+(\d+)% additional Flame Fuel Drop Quantity$", l)
    if m and loot == "fuel":
        return "add", 1 + int(m.group(1)) / 100
    m = re.match(r"\+(\d+)% additional Gear Drop Quantity$", l)
    if m and loot == "legendary_gear":
        return "add", 1 + int(m.group(1)) / 100
    m = re.match(r"\+(\d+)% Lunari Drop Quantity$", l)
    if m and loot == "hero_memory_revival_material":
        return "flat", int(m.group(1)) / 100
    m = re.search(r"(\d+(?:\.\d+)?)% chance .*replicat", l)
    if m and "Bottled" not in l and float(m.group(1)) < 100:
        p = float(m.group(1)) / 100
        return "add", 1 + 2 * p          # replicated once; the "100% ... again" line doubles the copy
    return None


def pet_mult(play, branch, loot, slugs):
    """-> (flat sum, additional product) of the lines of these pets that work on this loot: matrix if it has the entry, else all lines."""
    servs = (MATRIX["effects"].get(play, {}).get(branch, {}).get(loot) or {}) if play else {}
    flat, add = 0.0, 1.0
    for s in slugs:
        lines = AFF.get(s, {}).get("6", [])
        works = servs.get(s, {}).get("works", {}).get("6") if servs else None
        if play and servs and works is None:
            works = ["none"] * len(lines)          # listed play, pet not listed for this loot: nothing works
        for k, l in enumerate(lines):
            if works is not None and works[k] != "yes":
                continue
            e = line_effect(l, loot)
            if e is None:
                continue
            if e[0] == "flat":
                flat += e[1]
            else:
                add *= e[1]
    return flat, add


def node_lines(r):
    out = collections.Counter()
    for k, c in r["talents"].items():
        if k in RN.MD5:
            con, node = RN.MD5[k]
            out[(con.replace("_Talent_Constellation", ""), " / ".join(node["lines"]))] += c
    return out


def base_pool(nodes, cost):
    def cnt(s):
        return sum(c for (con, ln), c in nodes.items() if s in ln)
    return 1 + 1.0 + 0.25 + sum(v * cost.get(k, 0) for k, v in FLAT_COMPASS.items()) + 0.02 * cnt("In Netherrealm stages, +2% Drop Quantity") + 0.01 * cnt("In Netherrealm stages, +1% Drop Quantity")


def family_add(fam, nodes, cost):
    def cnt(s):
        return sum(c for (con, ln), c in nodes.items() if s in ln)
    add = 1.0
    for sub, kind, size in LINES[fam]:
        n = cnt(sub)
        if n:
            add *= (1 + size) ** n
    for comp, (f, mult) in COMPASS_TEXT.items():
        if f == fam and cost.get(comp, 0):
            add *= mult ** cost[comp]
    return add


def phase_pets(fname, fam, loot):
    """(flat, add) of the assumed pet set during this family's mechanic, on this loot type."""
    play, branch = fam["play"]
    return pet_mult(play, branch, loot, fam["regular"] + SPECIAL.get(fname, []))


def generic_pets(loot):
    return pet_mult(None, None, loot, FUEL_TRIO)


def setup_mult(fname, fam, nodes, cost, item):
    """(pool, add) for one mechanic-loot item in one setup, phase pets included."""
    lt = loot_type(item)
    pool = base_pool(nodes, cost); add = 1.15 ** (cost.get("Deep_Space_Resonance", 0) / 2) * family_add(fname, nodes, cost)
    if lt:
        pf, pa = phase_pets(fname, fam, lt)
        pool += pf; add *= pa
    return pool, add


def fe_mults(fname, fam, nodes, cost):
    """(pool_g, add_g, pool_m, add_m): generic-map FE (Fuel trio) and mechanic FE (phase pets)."""
    pool = base_pool(nodes, cost); res = 1.15 ** (cost.get("Deep_Space_Resonance", 0) / 2)
    gf, ga = generic_pets("fuel"); mf, ma = phase_pets(fname, fam, "fuel")
    return pool + gf, res * ga, pool + mf, res * family_add(fname, nodes, cost) * ma


def wls(X, y, w, names, ridge_from=3, lam=0.5):
    keep = [j for j in range(X.shape[1]) if j == 0 or X[:, j].std() > 0]
    Xk = X[:, keep]; sw = np.sqrt(w)
    pen = np.diag([0.0] * min(ridge_from, Xk.shape[1]) + [lam] * max(Xk.shape[1] - ridge_from, 0))
    A = (Xk * sw[:, None]).T @ (Xk * sw[:, None]) + pen
    b = np.linalg.solve(A, (Xk * sw[:, None]).T @ (y * sw))
    res = y - Xk @ b; n, k = Xk.shape
    Ainv = np.linalg.pinv(A); meat = (Xk * (w * res)[:, None]).T @ (Xk * (w * res)[:, None])
    se = np.sqrt(np.clip(np.diag(Ainv @ meat @ Ainv) * n / max(n - k, 1), 0, None))
    return {names[j]: (float(b[t]), float(se[t])) for t, j in enumerate(keep)}, float(np.sqrt(np.average(res ** 2, weights=w))), n


def fmt_free(coef, skip=("const", "a", "b", "c", "Bg", "Bm")):
    return ", ".join(f"{c.replace('_Compass', '').replace('_%28Artifact%29', ' (A)').replace('_Probe', ' probe').replace('_', ' ')} x{math.exp(v[0]):.2f}±{math.exp(v[0]) * v[1]:.2f}"
                     for c, v in coef.items() if c not in skip and not c.startswith("hero") and abs(v[0]) > 1.96 * v[1]) or "—"


def fit_fe(fname, fam, rows, free, own, heroes, md):
    """FE = exp(gamma x + hero) [Bg pool_g^a add_g + Bm pool_m^a add_m^b], NLS in log space, weights sqrt(runs cap 150)."""
    recs = []
    for r in rows:
        q = r["loot"].get(FE, 0)
        if q * r["count"] < 3:
            continue
        cost = {RN.name(i): v for i, v in r["cost"].items()}
        pg, ag, pm, am = fe_mults(fname, fam, r["nodes"], cost)
        x = [cost.get(c, 0.0) for c in free] + [1.0 if r["hero"] == h else 0.0 for h in heroes[1:]]   # own compasses: text only, no dummy
        recs.append((pg, ag, pm, am, x, math.log(q), min(r["count"], 150)))
    names = free + [f"hero {h}" for h in heroes[1:]]
    X = np.array([x for *_, x, _, _ in recs]); keep = [j for j in range(X.shape[1]) if X[:, j].std() > 0]
    X = X[:, keep]; names = [names[j] for j in keep]
    PG, AG, PM, AM = (np.array([rec[k] for rec in recs]) for k in range(4))
    gf_const, ga_const = generic_pets("fuel"); ma_const = phase_pets(fname, fam, "fuel")[1]
    y = np.array([rec[5] for rec in recs]); w = np.array([rec[6] for rec in recs], float); sw = np.sqrt(w)
    lam = 0.5
    if AM.std() < 1e-9 and PM.std() < 1e-9:
        md.append(f"FE: mechanic multipliers do not vary in this family -> split unidentified, single-component fit only")
        return None

    def model(p):
        lBg, lBm, a, b, c = p[:5]; g = p[5:]
        return np.log(np.exp(lBg) * PG ** a * AG ** c + np.exp(lBm) * PM ** a * AM ** b) + X @ g

    def resid(p):
        return np.concatenate([(y - model(p)) * sw, np.sqrt(lam) * p[5:]])
    y0 = np.average(y, weights=w)
    lo = [-np.inf, -np.inf, 0.0, 0.0, 1.0 - 1e-9] + [-np.inf] * X.shape[1]; hi = [np.inf, np.inf, 3.0, 3.0, 1.0 + 1e-9] + [np.inf] * X.shape[1]   # c fixed at 1: DS resonance at text on generic FE (Outlaw family fits it 1.03±0.13 when free)
    sol = None
    for share in (0.1, 0.3, 0.5, 0.7, 0.9):          # multi-start: mechanic share and b
        for b0 in (0.5, 1.0):
            p0 = np.array([y0 + math.log(1 - share) - math.log(np.median(PG) * np.median(AG)), y0 + math.log(share) - math.log(np.median(PM) * np.median(AM) ** b0), 1.0, b0, 1.0] + [0.0] * X.shape[1])
            s_ = least_squares(resid, p0, bounds=(lo, hi))
            if sol is None or s_.cost < sol.cost:
                sol = s_
    p = sol.x; r = y - model(p); n = len(y); k = len(p)
    J = sol.jac[:n] / sw[:, None]                       # d model / d p
    A = (J * w[:, None]).T @ J + np.diag([0, 0, 0, 0, 0] + [lam] * X.shape[1])
    Ainv = np.linalg.pinv(A); meat = (J * (w * r)[:, None]).T @ (J * (w * r)[:, None])
    se = np.sqrt(np.clip(np.diag(Ainv @ meat @ Ainv) * n / max(n - k, 1), 0, None))
    coef = {"Bg": (float(p[0]), float(se[0])), "Bm": (float(p[1]), float(se[1])), "a": (float(p[2]), float(se[2])), "b": (float(p[3]), float(se[3])), "c": (float(p[4]), float(se[4]))}
    coef.update({names[j]: (float(p[5 + j]), float(se[5 + j])) for j in range(X.shape[1])})
    sd = float(np.sqrt(np.average(r ** 2, weights=w)))
    # the split at the family's typical setup (run-weighted medians of the multipliers)
    med = lambda v: float(np.median(np.repeat(v, (w / w.min()).astype(int).clip(1, 50))))  # noqa: E731
    g_part = math.exp(p[0]) * med(PG) ** p[2] * med(AG) ** p[4]; m_part = math.exp(p[1]) * med(PM) ** p[2] * med(AM) ** p[3]
    md.append(f"Flame_Elementium (split) | generic {math.exp(p[0]):.3f} x pool^a x add_g^c (add_g = DS res x Fuel pets {med(AG):.2f}) + mechanic {math.exp(p[1]):.3f} x pool^a x add_m^b | "
              f"a {p[2]:.2f}±{se[2]:.2f} | b {p[3]:.2f}±{se[3]:.2f}, c {p[4]:.2f}±{se[4]:.2f} | {fmt_free(coef)} | {sd:.2f} (n={n}); at the typical setup: generic {g_part:.0f} + mechanic {m_part:.0f} "
              f"= {g_part + m_part:.0f} FE/map, mechanic share {m_part / (g_part + m_part):.0%} (pool_g {med(PG):.2f}, pool_m {med(PM):.2f}, add_m {med(AM):.2f})")
    # the same question linearly: FE against pool, DS resonance and the family's own multipliers (lines x compass text) with separate exponents
    Xl = np.array([[1.0, math.log(rec[0] - gf_const + 0), math.log(rec[1] / ga_const), math.log(rec[3] / (rec[1] / ga_const) / ma_const)] + list(rec[4]) for rec in recs])
    lin, sdl, _ = wls(Xl, y, w, ["const", "pool", "DSres", "lines"] + names, ridge_from=4)
    ex = lambda k: f"{lin[k][0]:.2f}±{lin[k][1]:.2f}" if k in lin else "n/a (constant in family)"  # noqa: E731
    md.append(f"Flame_Elementium (linear check) | exponents: pool {ex('pool')}, DS resonance {ex('DSres')}, family lines x compass text {ex('lines')} "
              f"(text would be 1 on the mechanic's share of FE) | sd {sdl:.2f}")
    return dict(coef=coef, n=n, split=dict(generic=g_part, mechanic=m_part, pool_g=med(PG), add_g=med(AG), pool_m=med(PM), add_m=med(AM)),
                linear={k: lin[k] for k in ("pool", "DSres", "lines") if k in lin})


def fit(fname, fam, R, md):
    rows = [r for r in R if any(c in {RN.name(i) for i, q in r["cost"].items() if q >= 0.5} for c in fam["compasses"])]
    val = collections.Counter()
    for r in rows:
        for i, q in r["loot"].items():
            val[i] += RN.value(i, q) * r["count"]
    items = [i for i, v in val.most_common(12) if RN.price(i)]
    free = [c for c in FREE if c not in fam["compasses"] and sum(1 for r in rows if any(RN.name(i) == c and q >= 0.3 for i, q in r["cost"].items())) >= 3]
    own = [c for c in fam["compasses"] if sum(1 for r in rows if any(RN.name(i) == c and q >= 0.3 for i, q in r["cost"].items())) >= 3]
    heroes = sorted({r["hero"] for r in rows})
    petsum = {}
    for lt in ("fuel", "component", "void_divinity_crafting_material", "hero_memory_revival_material", "memory_fluorescence", "fossil", "legendary_gear"):
        petsum[lt] = phase_pets(fname, fam, lt)
    gf, ga = generic_pets("fuel")
    md.append(f"\n# {fname}: {len(rows)} strategies, {sum(r['count'] for r in rows)} runs; pets in the mechanic ({', '.join(SNAME[s] for s in fam['regular'] + SPECIAL.get(fname, []))}): " +
              "; ".join(f"{lt} flat +{f * 100:.0f}% add x{a:.2f}" for lt, (f, a) in petsum.items() if f or a != 1) + f"; generic map FE (Fuel trio): flat +{gf * 100:.0f}% add x{ga:.2f}")
    md.append("item | base/map (at pool 1 / add 1, assumed pets inside pool/add) | a (pool exp) | b (add exp) | free compass effects | spread (resid sd)")
    out = {}
    for item in items:
        recs = []
        for r in rows:
            q = r["loot"].get(item, 0)
            if q * r["count"] < 3:
                continue
            cost = {RN.name(i): v for i, v in r["cost"].items()}
            pool, add = setup_mult(fname, fam, r["nodes"], cost, item)
            x = [1.0, math.log(pool), math.log(add)] + [cost.get(c, 0.0) for c in free] + [cost.get(c, 0.0) for c in own if len(own) > 1] + [1.0 if r["hero"] == h else 0.0 for h in heroes[1:]]
            recs.append((x, math.log(q), min(r["count"], 150)))
        if len(recs) < 25:
            continue
        X = np.array([x for x, *_ in recs]); y = np.array([y for _, y, _ in recs]); w = np.array([w for *_, w in recs], float)
        names = ["const", "a", "b"] + free + ([c for c in own] if len(own) > 1 else []) + [f"hero {h}" for h in heroes[1:]]
        coef, sd, n = wls(X, y, w, names)
        md.append(f"{RN.name(item)[:30]} | {math.exp(coef['const'][0]):.3f} | {coef['a'][0]:.2f}±{coef['a'][1]:.2f} | {coef['b'][0]:.2f}±{coef['b'][1]:.2f} | {fmt_free(coef)} | {sd:.2f} (n={n})")
        out[item] = dict(coef=coef, pets=petsum.get(loot_type(item), (0.0, 1.0)), n=n)
        if item == FE:
            fe = fit_fe(fname, fam, rows, free, own, heroes, md)
            if fe:
                out["FE_split"] = fe
    return out


# ---------------------------------------------------------------- calibration against Vlad's own maps
VLAD_NODES = {   # his constellation lines, as (family line substring -> count), from what he listed
    "outlaw": {"+1% additional Drop Quantity for all Security": 18, "+6% additional Drop Quantity for all Security": 1, "Super Sonic": 1, "for every 10 Escort Bodyguard": 1},
    "vigil": {"+1% additional Drop Quantity for the Vigil": 15, "+8% additional Drop Quantity for the Vigil": 1, "+15% additional Drop Quantity for the Vigil": 1, "During White Night Mode, +12%": 1},
}
VLAD_EXTRA_ADD = {"outlaw": (1 + 0.30 * 0.15) * 1.12, "vigil": 1.0}     # Oppressive at 15% realised, Profound +12% additional (11-05 tree)


def vlad_nodes(fname):
    return collections.Counter({(fname, k): v for k, v in VLAD_NODES.get(fname, {}).items()})


def predict(res, fname, fam, item, nodes, cost, extra_add=1.0):
    c = res[item]["coef"]
    pool, add = setup_mult(fname, fam, nodes, cost, item); add *= extra_add
    lg = c["const"][0] + c["a"][0] * math.log(pool) + c["b"][0] * math.log(add)
    for k, (b, _) in c.items():
        if k in ("const", "a", "b") or k.startswith("hero"):
            continue
        lg += b * cost.get(k, 0.0)
    return math.exp(lg), pool, add


def predict_fe(res, fname, fam, nodes, cost, extra_add=1.0):
    fe = res.get("FE_split")
    if not fe:
        return None
    c = fe["coef"]; pg, ag, pm, am = fe_mults(fname, fam, nodes, cost); am *= extra_add
    g = math.exp(c["Bg"][0]) * pg ** c["a"][0] * ag ** c["c"][0]; m = math.exp(c["Bm"][0]) * pm ** c["a"][0] * am ** c["b"][0]
    f = 1.0
    for k, (b, _) in c.items():
        if k in ("Bg", "Bm", "a", "b", "c") or k.startswith("hero"):
            continue
        f *= math.exp(b * cost.get(k, 0.0))
    return g * f, m * f


def calibrate(results, logs, md):
    import gamelog as G
    maps = [m for m in G.parse(logs) if m.get("end") and m.get("cost")]
    groups = collections.defaultdict(list)
    for m in maps:
        names = {RN.name(i) for i in m["cost"]}
        if "Alert_Outlaw_Compass" in names:
            groups["Alert + All-Evil" if "All-Evil_Vigil_Compass" in names else "Alert"].append(m)
        elif "Evernight_Vigil_Compass" in names:
            groups["Evernight (+ Overrealm)"].append(m)
    md.append("\n# Calibration against Vlad's own maps (a check, not an eraser): his tree lines, his compasses per map, Fright 3.5, pets as assumed")
    for gname, ms in groups.items():
        n = len(ms)
        cost = collections.Counter()
        for m in ms:
            for i, q in m["cost"].items():
                cost[RN.name(i)] += q / n
        obs = collections.Counter()
        for m in ms:
            for i, q in m["loot"].items():
                obs[i] += q / n
        md.append(f"\n## {gname}: {n} maps; compasses " + ", ".join(f"{k.replace('_Compass', '').replace('_', ' ')} {v:.2f}" for k, v in cost.items() if v >= 0.3))
        md.append("item | model | his | ratio his/model")
        for fname, items in (("outlaw", ["360404", "360405", "360407"]), ("vigil", ["394119"])):
            if fname not in results or not any(c in cost for c in FAMILIES[fname]["compasses"]):
                continue
            res = results[fname]; fam = FAMILIES[fname]; nodes = vlad_nodes(fname)
            for item in items:
                if item not in res:
                    continue
                p, pool, add = predict(res, fname, fam, item, nodes, dict(cost), VLAD_EXTRA_ADD[fname])
                md.append(f"{RN.name(item)[:28]} ({fname}; pool {pool:.2f}, add {add:.2f}) | {p:.3f} | {obs.get(item, 0):.3f} | x{obs.get(item, 0) / p:.2f}")
            fe = predict_fe(res, fname, fam, nodes, dict(cost), VLAD_EXTRA_ADD[fname])
            if fe:
                md.append(f"FE whole map ({fname} split: generic {fe[0]:.0f} + mechanic {fe[1]:.0f}) | {fe[0] + fe[1]:.0f} | {obs.get(FE, 0):.0f} | x{obs.get(FE, 0) / (fe[0] + fe[1]):.2f}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", default="all")
    ap.add_argument("--md", default=None)
    ap.add_argument("--json", default=None)
    ap.add_argument("--logs", nargs="*", default=[])
    a = ap.parse_args(argv)
    R = D.load(STAGES)
    hero = {}
    for f in glob.glob(os.path.join(D.SDIR, "lb_*.json")):
        for it in json.load(open(f))["data"]["items"]:
            hero[it["key"]] = it.get("heroId")
    for r in R:
        r["hero"] = str(hero.get(r["key"])); r["nodes"] = node_lines(r)
    R = [r for r in R if not any(x in r["talent_label"] for x in ("囚笼", "玩偶", "机械", "巨力"))]
    md = [f"Forward model, checkpoint 2 — prices {os.path.basename(RN.PRICE_FILE)}; pool = 1 + 1.00 res + 0.25 Path + flat lines + phase pets; add = DS affixes x family lines x compass text x phase pets (incl. replicates); Fright {FRIGHT}"]
    results = {}
    for fname, fam in (FAMILIES.items() if a.family == "all" else [(a.family, FAMILIES[a.family])]):
        results[fname] = fit(fname, fam, R, md)
    if a.logs:
        calibrate(results, a.logs, md)
    text = "\n".join(md)
    print(text)
    if a.md:
        open(a.md, "w").write(text + "\n")
    if a.json:
        json.dump(results, open(a.json, "w"), indent=0)


if __name__ == "__main__":
    main()
