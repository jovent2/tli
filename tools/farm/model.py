#!/usr/bin/env python3
"""Forward drop model per mechanic family: naked base x pool^a x additional^b x free compass effects, fitted on every logged
Deep Space strategy of the family, with the text supplying the pool / additional multipliers of every known line and the data
supplying the exponents (a, b), the base, and the effect of compasses whose text is conditional (Generous, Bountiful, probes...).

For a strategy s and loot item i:
  pool_s   = 1 + 1.00 (resonance, capped) + 0.25 (Path of Progression) + 0.4 Sinful + 0.8 Sinful(A) + 0.4 Flourishing probe
             + 0.02 x Profound "+2% DQ" micros + 0.01 x Commodities "+1% DQ" micros + flat pet lines (assumed trio, if they work on i)
  add_s    = 1.15^(DS affixes) x family lines (text) x additional pet lines x Fright 3.5 (All-Evil) x 2 (Evernight) ...
  log q_si = log base_i + a_i log pool_s + b_i log add_s + sum_c gamma_ic x_sc + hero,   WLS, weight = runs (cap 150), HC1.
Which pet line classes work on i comes from the XD matrix (data/ext/pactspirit_drop_effects.json).
Checkpoint 1 output: base per item (at a = b = 1 reference setup), a, b, free coefficients, spread; and the prediction for Vlad's
own setup against his logs.   python3 tools/farm/model.py [--family outlaw|vigil|lunaria|darksurge|all] [--md out.md]
"""
import argparse
import collections
import glob
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN  # noqa: E402
import ds_scan as D  # noqa: E402

STAGES = ["week3", "week2", "day7", "day6", "day5", "day4", "day3", "day2", "day1"]
EXT = RN.EXT
MATRIX = json.load(open(os.path.join(EXT, "pactspirit_drop_effects.json")))
AFF = {s: {str(r["rank"]): r["lines"] for r in v} for s, v in MATRIX["servant_affixes"].items()}
SNAME = {x["slug"]: x["name"] for x in MATRIX["servants"]}
FRIGHT = 3.5
FAMILIES = {
    "outlaw": dict(compasses=["Alert_Outlaw_Compass"], cons=("Outlaw",), play=("otherworld_special_action", "security_guard"),
                   trio={"component": ["SSR16130", "SR16120", "R16110"], "fuel": ["SSR6330", "SR6320", "SSR19330"]}),
    "vigil": dict(compasses=["All-Evil_Vigil_Compass", "Evernight_Vigil_Compass", "Phantom_Vigil_Compass"], cons=("Afterlight",), play=("night_watch", "night_watch"),
                  trio={"*": ["SSR20130", "SR20120", "SSR19330"], "fuel": ["SSR6330", "SR6320", "SSR19330"]}),
    "lunaria": dict(compasses=["Lunar_Stele_Lunaria_Compass", "Pristine_Lunaria_Compass", "Moonlit_Casket_Lunaria_Compass", "Lunaria_Compass"], cons=("Lunaria",), play=("music_performance", "music_performance"),
                    trio={"*": "best", "fuel": ["SSR6330", "SR6320", "SSR19330"]}),
    "darksurge": dict(compasses=["Divine_Warrior_Dark_Surge_Compass", "Bandit_Dark_Surge_Compass", "Dark_Surge_Compass"], cons=("Dark_Surge",), play=("dark_tide", "dark_tide"),
                      trio={"*": "best", "fuel": ["SSR6330", "SR6320", "SSR19330"]}),
}
LOOT_TYPE = [("Flame_Elementium", "fuel"), ("Flame_Sand", "flame_sand"), ("Expansion_Mod", "component"), ("Base_Mod", "component"), ("Fossil", "fossil"),
             ("Divine_Remnant", "void_divinity_crafting_material"), ("Divinity", "void_divinity_crafting_material"), ("Secret", "memory_fluorescence"),
             ("Shadow", "memory_fluorescence"), ("Memory", "memory_fluorescence"), ("Lunar", "hero_memory_revival_material"), ("Corrosion", "corrosion_material"),
             ("TOWER_Token", "tower_chip")]
# text lines of each family's own constellation, as (substring, kind, size); kind: add (multiplicative), flat (into the pool)
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


def loot_type(item):
    n = RN.name(item)
    for k, t in LOOT_TYPE:
        if k in n:
            return t
    return "legendary_gear" if (RN.price(item) or 0) > 300 else None


def pet_lines(play, branch, loot, slugs):
    """-> (flat sum, additional product) of the working lines of these pets on this loot, per the matrix (rank 6)."""
    servs = MATRIX["effects"].get(play, {}).get(branch, {}).get(loot)
    flat, add = 0.0, 1.0
    if not servs:
        return flat, add
    import re
    for s in slugs:
        v = servs.get(s)
        if not v:
            continue
        for l, w in zip(AFF.get(s, {}).get("6", []), v["works"].get("6", [])):
            if w != "yes":
                continue
            m = re.match(r"\+(\d+)% Drop Quantity( for TOWER Securities| from Wraiths)?$", l.strip())
            if m:
                flat += int(m.group(1)) / 100; continue
            m = re.match(r"\+(\d+(?:\.\d+)?)% additional Drop Quantity( from all Wraiths in the Vigil)?$", l.strip())
            if m:
                add *= 1 + float(m.group(1)) / 100
    return flat, add


def best_trio(play, branch, loot):
    servs = MATRIX["effects"].get(play, {}).get(branch, {}).get(loot, {})
    scored = []
    for s in servs:
        f, a = pet_lines(play, branch, loot, [s])
        scored.append((f + 3 * (a - 1), s))
    scored.sort(reverse=True)
    return [s for _, s in scored[:3]]


def node_lines(r):
    out = collections.Counter()
    for k, c in r["talents"].items():
        if k in RN.MD5:
            con, node = RN.MD5[k]
            out[(con.replace("_Talent_Constellation", ""), " / ".join(node["lines"]))] += c
    return out


def setup_mult(fam, nodes, cost, item, pets):
    """(pool, add) from the text for one setup. cost = {name: qty per run}; nodes = Counter of (con, line)."""
    def cnt(s):
        return sum(c for (con, ln), c in nodes.items() if s in ln)
    pool = 1 + 1.0 + 0.25 + sum(v * cost.get(k, 0) for k, v in FLAT_COMPASS.items()) + 0.02 * cnt("In Netherrealm stages, +2% Drop Quantity") + 0.01 * cnt("In Netherrealm stages, +1% Drop Quantity")
    add = 1.15 ** (cost.get("Deep_Space_Resonance", 0) / 2)
    for sub, kind, size in LINES[fam]:
        n = cnt(sub)
        if n:
            add *= (1 + size) ** n
    for comp, (f, mult) in COMPASS_TEXT.items():
        if f == fam and cost.get(comp, 0):
            add *= mult ** cost[comp]
    lt = loot_type(item)
    if pets and lt:
        pf, pa = pets.get(lt, (0.0, 1.0))
        pool += pf; add *= pa
    return pool, add


def family_pets(fam):
    play, branch = fam["play"]
    out = {}
    for lt in ("fuel", "flame_sand", "fossil", "component", "memory_fluorescence", "void_divinity_crafting_material", "hero_memory_revival_material", "corrosion_material", "legendary_gear", "tower_chip"):
        trio = fam["trio"].get(lt, fam["trio"].get("*"))
        if trio == "best":
            trio = best_trio(play, branch, lt)
        if not trio:
            continue
        out[lt] = pet_lines(play, branch, lt, trio)
    return out


def fit(fname, fam, R, md):
    rows = [r for r in R if any(c in {RN.name(i) for i, q in r["cost"].items() if q >= 0.5} for c in fam["compasses"])]
    pets = family_pets(fam)
    val = collections.Counter()
    for r in rows:
        for i, q in r["loot"].items():
            val[i] += RN.value(i, q) * r["count"]
    items = [i for i, v in val.most_common(12) if RN.price(i)]
    free = [c for c in FREE if c not in fam["compasses"] and sum(1 for r in rows if any(RN.name(i) == c and q >= 0.3 for i, q in r["cost"].items())) >= 3]
    own = [c for c in fam["compasses"] if sum(1 for r in rows if any(RN.name(i) == c and q >= 0.3 for i, q in r["cost"].items())) >= 3]
    heroes = sorted({r["hero"] for r in rows})
    md.append(f"\n# {fname}: {len(rows)} strategies, {sum(r['count'] for r in rows)} runs; assumed pets per loot type: " +
              "; ".join(f"{lt}: flat +{f * 100:.0f}% add x{a:.2f}" for lt, (f, a) in pets.items() if lt in ("fuel", "component", "void_divinity_crafting_material", "memory_fluorescence", "legendary_gear")))
    md.append("item | base/map (naked, at pool 1 / add 1, after dividing out the assumed pets) | a (pool exp) | b (add exp) | free compass effects | spread (resid sd)")
    out = {}
    for item in items:
        recs = []
        for r in rows:
            q = r["loot"].get(item, 0)
            if q * r["count"] < 3:
                continue
            cost = {RN.name(i): v for i, v in r["cost"].items()}
            pool, add = setup_mult(fname, r["nodes"], cost, item, pets)
            x = [1.0, math.log(pool), math.log(add)] + [cost.get(c, 0.0) for c in free] + [cost.get(c, 0.0) for c in own if len(own) > 1] + [1.0 if r["hero"] == h else 0.0 for h in heroes[1:]]
            recs.append((x, math.log(q), min(r["count"], 150)))
        if len(recs) < 25:
            continue
        X = np.array([x for x, *_ in recs]); y = np.array([y for _, y, _ in recs]); w = np.array([w for *_, w in recs], float)
        keep = [j for j in range(X.shape[1]) if j == 0 or X[:, j].std() > 0]
        names = ["const", "a", "b"] + free + ([c for c in own] if len(own) > 1 else []) + [f"hero {h}" for h in heroes[1:]]
        Xk = X[:, keep]; sw = np.sqrt(w)
        lam = np.diag([0.0, 0.0, 0.0] + [0.5] * (Xk.shape[1] - 3))
        A = (Xk * sw[:, None]).T @ (Xk * sw[:, None]) + lam
        b = np.linalg.solve(A, (Xk * sw[:, None]).T @ (y * sw))
        res = y - Xk @ b; n, k = Xk.shape
        Ainv = np.linalg.pinv(A); meat = (Xk * (w * res)[:, None]).T @ (Xk * (w * res)[:, None]); se = np.sqrt(np.clip(np.diag(Ainv @ meat @ Ainv) * n / max(n - k, 1), 0, None))
        coef = {names[j]: (float(b[t]), float(se[t])) for t, j in enumerate(keep)}
        frees = ", ".join(f"{c.replace('_Compass', '').replace('_%28Artifact%29', ' (A)').replace('_Probe', ' probe').replace('_', ' ')} x{math.exp(v[0]):.2f}±{math.exp(v[0]) * v[1]:.2f}"
                          for c, v in coef.items() if c not in ("const", "a", "b") and not c.startswith("hero") and abs(v[0]) > 1.96 * v[1])
        md.append(f"{RN.name(item)[:30]} | {math.exp(coef['const'][0]):.3f} | {coef['a'][0]:.2f}±{coef['a'][1]:.2f} | {coef['b'][0]:.2f}±{coef['b'][1]:.2f} | {frees or '—'} | {float(np.sqrt(np.average(res ** 2, weights=w))):.2f} (n={n})")
        out[item] = dict(coef=coef, pets=pets.get(loot_type(item), (0.0, 1.0)), n=n)
    return out, pets


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", default="all")
    ap.add_argument("--md", default=None)
    ap.add_argument("--json", default=None)
    a = ap.parse_args(argv)
    R = D.load(STAGES)
    hero = {}
    for f in glob.glob(os.path.join(D.SDIR, "lb_*.json")):
        for it in json.load(open(f))["data"]["items"]:
            hero[it["key"]] = it.get("heroId")
    for r in R:
        r["hero"] = str(hero.get(r["key"])); r["nodes"] = node_lines(r)
    R = [r for r in R if not any(x in r["talent_label"] for x in ("囚笼", "玩偶", "机械", "巨力"))]
    md = [f"Forward model, checkpoint 1 — prices {os.path.basename(RN.PRICE_FILE)}; pool = 1 + 1.00 res + 0.25 Path + flat lines; add = DS affixes x family lines x pets; Fright {FRIGHT}"]
    results = {}
    for fname, fam in (FAMILIES.items() if a.family == "all" else [(a.family, FAMILIES[a.family])]):
        results[fname] = fit(fname, fam, R, md)
    text = "\n".join(md)
    print(text)
    if a.md:
        open(a.md, "w").write(text + "\n")
    if a.json:
        json.dump({f: {i: dict(coef=v["coef"], pets=v["pets"], n=v["n"]) for i, v in res[0].items()} for f, res in results.items()}, open(a.json, "w"), indent=0)


if __name__ == "__main__":
    main()
