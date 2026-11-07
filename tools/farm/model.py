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

Checkpoint 1c (2026-11-07 03:00), three changes on top of 1b, all from the loot-class rulebook (docs/loot_classes.md):
  * whole-map FE gets two additional regressors by text scope: general additional (DS affixes, pet additionals: every drop in the map)
    and the mechanic's own additional (its tree lines, Evernight x2 / All-Evil x4.5, Generous, Bountiful: only what its monsters drop),
    each with its own exponent. On mechanic loot both are the same class, so one exponent as before.
  * Generous (+15% additional from Rare monsters; all four mechanics' monsters are rare [Vlad]) and Bountiful (+200% on the 30% enhanced
    = x1.6) are text lines in the mechanic's additional product, not fitted dummies.
  * the probes other than Flourishing and other mechanics' compasses stay in the regression as nuisance dummies (they absorb who runs
    what) but are not on the card: their lines are typed/other with no verdict for this loot.
  --check writes the per-strategy test: every logged setup's lines, what the card predicts, what the player got.
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
    # pets per PHASE (2026-11-07, Vlad): 3 regular drop pets + the season's special slots, always up. Regular = Fuel trio (Chalk / Surging Gold /
    # Twilight Sparks) all map, swapped to the Outlaw trio (Prof. SOURCE / Shro-Shroom / Lumidrake) for the Carjack only. Special slots: the
    # Vigil pair (Lady Obituary / Melancholy Azure), Lunaria pair (Avatar of Moon / Melancholy Cyan), Dark Surge pair (Eternity Summoner /
    # Plaintive Flower). One pet set per mechanic, applied to every loot type of that mechanic.
    "outlaw": dict(compasses=["Alert_Outlaw_Compass"], cons=("Outlaw",), play=("otherworld_special_action", "security_guard"),
                   trio={"*": ["SSR16130", "SR16120", "R16110"]}),
    "vigil": dict(compasses=["All-Evil_Vigil_Compass", "Evernight_Vigil_Compass", "Phantom_Vigil_Compass"], cons=("Afterlight",), play=("night_watch", "night_watch"),
                  trio={"*": ["SSR6330", "SR6320", "SSR19330", "SSR20130", "SR20120"]}),
    "lunaria": dict(compasses=["Lunar_Stele_Lunaria_Compass", "Pristine_Lunaria_Compass", "Moonlit_Casket_Lunaria_Compass", "Lunaria_Compass"], cons=("Lunaria",), play=("music_performance", "music_performance"),
                    trio={"*": ["SSR6330", "SR6320", "SSR19330", "SSR19130", "SR19120"]}),
    "darksurge": dict(compasses=["Divine_Warrior_Dark_Surge_Compass", "Bandit_Dark_Surge_Compass", "Dark_Surge_Compass"], cons=("Dark_Surge",), play=("dark_tide", "dark_tide"),
                      trio={"*": ["SSR6330", "SR6320", "SSR19330", "SSR6230", "SR6220"]}),
}
LOOT_TYPE = [("Flame_Elementium", "fuel"), ("Flame_Sand", "flame_sand"), ("Expansion_Mod", "component"), ("Base_Mod", "component"), ("Fossil", "fossil"),
             ("Divine_Remnant", "void_divinity_crafting_material"), ("Divinity", "void_divinity_crafting_material"), ("Secret", "memory_fluorescence"),
             ("Shadow", "memory_fluorescence"), ("Memory", "memory_fluorescence"), ("Lunar", "hero_memory_revival_material"), ("Corrosion", "corrosion_material"),
             ("TOWER_Token", "tower_chip")]
# text lines of each family's own constellation, as (substring, kind, size); kind: add (multiplicative), flat (into the pool)
LINES = {
    "outlaw": [("+1% additional Drop Quantity for all Security", "add", 0.01), ("+6% additional Drop Quantity for all Security", "add", 0.06),
               ("Super Sonic", "add", 0.23), ("Hyper-Hardened", "add", 0.23), ("for every 10 Escort Bodyguard", "add", 0.10),
               ("+30% additional Drop Quantity for all Security personnel after", "add", 0.30 * 0.15)],  # Bounty Orders: Oppressive's fitted presence effect on CN is x0.97-1.11 (fit.py), i.e. rarely activated; Vlad ~15%
    # Afterlight (2026-11-07 03:45, checked on the tlidb graph): Grief: Mourn (+15%, node 50) and the White Night +12% (node 58) are LEAVES
    # off micros 49 / 57, so 30 micros are reachable without them, and 0 of 180 CN Vigil players show either: CN skips them. The coffin
    # (19) and goblin-appear (23) nodes are pass-through and also never decode: those two are in every CN tree and in the base. So +15% and
    # WN +12% are real extra lines (text, exponent from the family's b, unidentified on CN); WN +12% only during White Night (fraction unknown).
    "vigil": [("+1% additional Drop Quantity for the Vigil", "add", 0.01), ("+8% additional Drop Quantity for the Vigil", "add", 0.08),
              ("+15% additional Drop Quantity for the Vigil", "add", 0.15), ("During White Night Mode, +12%", "add", 0.12)],
    "lunaria": [("+1% additional Drop Quantity for Lunaria", "add", 0.01), ("+4% additional Drop Quantity for Lunaria", "add", 0.04),
                ("+6% additional Drop Quantity for Lunaria", "add", 0.06)],
    "darksurge": [],
}
COMPASS_TEXT = {"All-Evil_Vigil_Compass": ("vigil", FRIGHT + 1), "Evernight_Vigil_Compass": ("vigil", 2.0), "Pristine_Lunaria_Compass": ("lunaria", 2.0)}
RARE_TEXT = {"Generous_Elite_Compass": 1.15, "Bountiful_Elite_Compass": 1 + 2.0 * 0.3}     # generic additional on the mechanic's (rare) monsters
NUISANCE = ["Compass_Deep_Space_Probe", "Gear_Deep_Space_Probe", "Fluorescent_Deep_Space_Probe", "Alert_Outlaw_Compass", "All-Evil_Vigil_Compass", "Evernight_Vigil_Compass",
            "Lunar_Stele_Lunaria_Compass", "Conquering_Novel_Compass", "Divine_Warrior_Dark_Surge_Compass", "Containment_Overrealm_Compass", "Shadow_Overrealm_Compass",
            "Full_Load_Outlaw_Compass", "Lavish_Novel_Compass"]
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
        lines = AFF.get(s, {}).get("6", [])
        again = any("100%" in l and "replicat" in l for l in lines)       # "100% chance ... replicated again": doubles the copies
        for l, w in zip(lines, v["works"].get("6", [])):
            if w != "yes":
                continue
            l = l.strip()
            m = re.match(r"\+(\d+)% Drop Quantity( for TOWER Securities| from Wraiths)?$", l)
            if m:
                flat += int(m.group(1)) / 100; continue
            m = re.match(r"\+(\d+(?:\.\d+)?)% additional Drop Quantity( from all Wraiths in the Vigil)?$", l)
            if m:
                add *= 1 + float(m.group(1)) / 100; continue
            m = re.match(r"\+(\d+)% additional Flame Fuel Drop Quantity$", l)          # Chalk / Surging fuel lines (the matrix says where they work)
            if m and loot == "fuel":
                add *= 1 + int(m.group(1)) / 100; continue
            m = re.match(r"\+(\d+)% Lunari Drop Quantity$", l)
            if m and loot == "hero_memory_revival_material":
                flat += int(m.group(1)) / 100; continue
            m = re.search(r"(\d+(?:\.\d+)?)% chance .*replicat", l)                 # Prof. SOURCE recode, Elegy, Avatar of Moon: x(1 + p x copies)
            if m and "Bottled" not in l and float(m.group(1)) < 100:
                k = re.search(r"replicated (\d+) (?:additional )?time", l)
                add *= 1 + float(m.group(1)) / 100 * (int(k.group(1)) if k else 1) * (2 if again else 1)
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


def setup_mult(fam, nodes, cost, item, pets, split=False):
    """(pool, add) from the text for one setup; with split=True -> (pool, add_general, add_mechanic). cost = {name: qty per run};
    nodes = Counter of (con, line). General additional = DS affixes + pet additionals (every drop); mechanic additional = the family's
    tree lines, its compass text, Generous / Bountiful (its monsters are rare)."""
    def cnt(s):
        return sum(c for (con, ln), c in nodes.items() if s in ln)
    pool = 1 + 1.0 + 0.25 + sum(v * cost.get(k, 0) for k, v in FLAT_COMPASS.items()) + 0.02 * cnt("In Netherrealm stages, +2% Drop Quantity") + 0.01 * cnt("In Netherrealm stages, +1% Drop Quantity")
    gen = 1.15 ** (cost.get("Deep_Space_Resonance", 0) / 2)
    mech = 1.0
    for sub, kind, size in LINES[fam]:
        n = cnt(sub)
        if n:
            mech *= (1 + size) ** n
    for comp, (f, mult) in COMPASS_TEXT.items():
        if f == fam and cost.get(comp, 0):
            mech *= mult ** cost[comp]
    for comp, mult in RARE_TEXT.items():
        if cost.get(comp, 0):
            mech *= mult ** cost[comp]
    lt = loot_type(item)
    if pets and lt:
        pf, pa = pets.get(lt, (0.0, 1.0))
        pool += pf; gen *= pa
    return (pool, gen, mech) if split else (pool, gen * mech)


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


FE = "100300"


def fit(fname, fam, R, md):
    rows = [r for r in R if any(c in {RN.name(i) for i, q in r["cost"].items() if q >= 0.5} for c in fam["compasses"])]
    pets = family_pets(fam)
    val = collections.Counter()
    for r in rows:
        for i, q in r["loot"].items():
            val[i] += RN.value(i, q) * r["count"]
    items = [i for i, v in val.most_common(12) if RN.price(i)]
    nuis = [c for c in NUISANCE if c not in fam["compasses"] and sum(1 for r in rows if any(RN.name(i) == c and q >= 0.3 for i, q in r["cost"].items())) >= 3]
    heroes = sorted({r["hero"] for r in rows})
    md.append(f"\n# {fname}: {len(rows)} strategies, {sum(r['count'] for r in rows)} runs; assumed pets in the mechanic ({', '.join(SNAME[s] for s in fam['trio']['*'])}), by loot type: " +
              "; ".join(f"{lt}: flat +{f * 100:.0f}% add x{a:.2f}" for lt, (f, a) in pets.items() if lt in ("fuel", "component", "void_divinity_crafting_material", "memory_fluorescence", "legendary_gear")))
    md.append("item | base/map (naked, at pool 1 / add 1, assumed pets divided out) | a (pool exp) | b (additional exp; FE: general / mechanic) | nuisance dummies (who runs it; NOT on the card) | spread (resid sd)")
    out = {}
    for item in items:
        recs = []
        for r in rows:
            q = r["loot"].get(item, 0)
            if q * r["count"] < 3:
                continue
            cost = {RN.name(i): v for i, v in r["cost"].items()}
            pool, gen, mech = setup_mult(fname, r["nodes"], cost, item, pets, split=True)
            adds = [math.log(gen), math.log(mech)] if item == FE else [math.log(gen * mech)]
            x = [1.0, math.log(pool)] + adds + [cost.get(c, 0.0) for c in nuis] + [1.0 if r["hero"] == h else 0.0 for h in heroes[1:]]
            recs.append((x, math.log(q), min(r["count"], 150)))
        if len(recs) < 25:
            continue
        X = np.array([x for x, *_ in recs]); y = np.array([y for _, y, _ in recs]); w = np.array([w for *_, w in recs], float)
        keep = [j for j in range(X.shape[1]) if j == 0 or X[:, j].std() > 0]
        names = ["const", "a"] + (["b_gen", "b_mech"] if item == FE else ["b"]) + nuis + [f"hero {h}" for h in heroes[1:]]
        nfree = 4 if item == FE else 3
        Xk = X[:, keep]; sw = np.sqrt(w)
        lam = np.diag([0.0] * min(nfree, Xk.shape[1]) + [0.5] * max(Xk.shape[1] - nfree, 0))
        A = (Xk * sw[:, None]).T @ (Xk * sw[:, None]) + lam
        b = np.linalg.solve(A, (Xk * sw[:, None]).T @ (y * sw))
        res = y - Xk @ b; n, k = Xk.shape
        Ainv = np.linalg.pinv(A); meat = (Xk * (w * res)[:, None]).T @ (Xk * (w * res)[:, None]); se = np.sqrt(np.clip(np.diag(Ainv @ meat @ Ainv) * n / max(n - k, 1), 0, None))
        coef = {names[j]: (float(b[t]), float(se[t])) for t, j in enumerate(keep)}
        frees = ", ".join(f"{c.replace('_Compass', '').replace('_%28Artifact%29', ' (A)').replace('_Probe', ' probe').replace('_', ' ')} x{math.exp(v[0]):.2f}±{math.exp(v[0]) * v[1]:.2f}"
                          for c, v in coef.items() if c not in ("const", "a", "b", "b_gen", "b_mech") and not c.startswith("hero") and abs(v[0]) > 1.96 * v[1])
        bcol = (f"{coef['b_gen'][0]:.2f}±{coef['b_gen'][1]:.2f} / {coef['b_mech'][0]:.2f}±{coef['b_mech'][1]:.2f}" if item == FE else f"{coef['b'][0]:.2f}±{coef['b'][1]:.2f}")
        md.append(f"{RN.name(item)[:30]} | {math.exp(coef['const'][0]):.3f} | {coef['a'][0]:.2f}±{coef['a'][1]:.2f} | {bcol} | {frees or '—'} | {float(np.sqrt(np.average(res ** 2, weights=w))):.2f} (n={n})")
        out[item] = dict(coef=coef, pets=pets.get(loot_type(item), (0.0, 1.0)), n=n, nuis=nuis)
    return out, pets


def predict(res, fname, item, nodes, cost, pets, nuisance=False):
    """The card's prediction for one setup: base x pool^a x additional^b (x nuisance dummies only if asked, for the per-strategy check)."""
    c = res[item]["coef"]
    pool, gen, mech = setup_mult(fname, nodes, cost, item, pets, split=True)
    lg = c["const"][0] + c["a"][0] * math.log(pool)
    lg += (c["b_gen"][0] * math.log(gen) + c["b_mech"][0] * math.log(mech)) if item == FE else c["b"][0] * math.log(gen * mech)
    if nuisance:
        for k, (b, se) in c.items():
            if k not in ("const", "a", "b", "b_gen", "b_mech") and not k.startswith("hero"):
                lg += b * cost.get(k, 0.0)
    return math.exp(lg), pool, gen, mech


def check(results, R, md, top=25):
    """Per logged strategy: its lines, the card's prediction, what the player got. Card only (no nuisance dummies), then with them."""
    md.append("\n# Per-strategy check: the card's prediction vs the player's actual, by family (the top strategies by runs; full list in the json)")
    md.append("Lines shown: compasses, DS affixes, the family's additional lines (micros x count, mediums); pool / general / mechanic multipliers; pred = card only, pred+ = with the nuisance dummies")
    allrows = {}
    for fname, (res, pets) in results.items():
        fam = FAMILIES[fname]
        rows = [r for r in R if any(c in {RN.name(i) for i, q in r["cost"].items() if q >= 0.5} for c in fam["compasses"])]
        rows.sort(key=lambda r: -r["count"])
        items = [i for i in res if i != FE][:3] + ([FE] if FE in res else [])
        md.append(f"\n## {fname}: " + " | ".join(RN.name(i)[:22] for i in items))
        md.append("runs | setup (compasses, DS affixes, lines) | pool / gen / mech | " + " | ".join("pred (pred+) / actual" for _ in items))
        fam_rows = []
        for r in rows:
            cost = {RN.name(i): v for i, v in r["cost"].items()}
            comps = ", ".join(f"{k.replace('_Compass', '').replace('_%28Artifact%29', '(A)').replace('_Deep_Space_Probe', ' probe').replace('_', ' ')}" + (f" x{v:.1f}" if v < 0.95 else "")
                              for k, v in cost.items() if v >= 0.3 and k not in ("Deep_Space_Beacon", "Netherrealm_resonance", "Deep_Space_Resonance"))
            lines = []
            for sub, kind, size in LINES[fname]:
                n = sum(c for (con, ln), c in r["nodes"].items() if sub in ln)
                if n:
                    lines.append(f"{sub.split(' additional')[0].strip('+ ')}{' x' + str(n) if n > 1 else ''}" if size <= 0.01 else sub.split(" for ")[0].split(" additional")[0].replace("During White Night Mode, ", "WN ").strip())
            cells = []; rec = dict(key=r["key"], runs=r["count"], cost=cost, items={})
            for it in items:
                if it not in res:
                    cells.append("—"); continue
                p, pool, gen, mech = predict(res, fname, it, r["nodes"], cost, pets)
                pn = predict(res, fname, it, r["nodes"], cost, pets, nuisance=True)[0]
                act = r["loot"].get(it, 0.0)
                cells.append(f"{p:.2f} ({pn:.2f}) / {act:.2f}")
                rec["items"][it] = dict(pred=p, pred_nuis=pn, actual=act, pool=pool, gen=gen, mech=mech)
            fam_rows.append(rec)
            if len(fam_rows) <= top:
                md.append(f"{r['count']:4d} | {comps}; DS x{int(cost.get('Deep_Space_Resonance', 0) / 2)}; {', '.join(lines) or 'no family lines'} | {pool:.2f} / {gen:.2f} / {mech:.2f} | " + " | ".join(cells))
        # summary: run-weighted ratio actual/pred and the spread
        for it in items:
            if it not in res:
                continue
            lr = [(math.log(x["items"][it]["actual"] / x["items"][it]["pred"]), x["runs"]) for x in fam_rows if x["items"][it]["actual"] > 0]
            if lr:
                m = sum(l * w for l, w in lr) / sum(w for _, w in lr); sd = math.sqrt(sum((l - m) ** 2 * w for l, w in lr) / sum(w for _, w in lr))
                md.append(f"  {RN.name(it)[:24]}: actual / card over {len(lr)} strategies = x{math.exp(m):.2f} (run-weighted), spread x/ {math.exp(sd):.2f}")
        allrows[fname] = fam_rows
    return allrows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", default="all")
    ap.add_argument("--md", default=None)
    ap.add_argument("--json", default=None)
    ap.add_argument("--check", default=None, help="write the per-strategy check json here (and its table into --md)")
    a = ap.parse_args(argv)
    R = D.load(STAGES)
    hero = {}
    for f in glob.glob(os.path.join(D.SDIR, "lb_*.json")):
        for it in json.load(open(f))["data"]["items"]:
            hero[it["key"]] = it.get("heroId")
    for r in R:
        r["hero"] = str(hero.get(r["key"])); r["nodes"] = node_lines(r)
    R = [r for r in R if not any(x in r["talent_label"] for x in ("囚笼", "玩偶", "机械", "巨力"))]
    md = [f"Forward model, checkpoint 1c (1 + pets per phase + FE split by text scope + Generous/Bountiful as text) — prices {os.path.basename(RN.PRICE_FILE)}; pool = 1 + 1.00 res + 0.25 Path + flat lines; add = DS affixes x family lines x pets; Fright {FRIGHT}"]
    results = {}
    for fname, fam in (FAMILIES.items() if a.family == "all" else [(a.family, FAMILIES[a.family])]):
        results[fname] = fit(fname, fam, R, md)
    if a.check:
        rows = check(results, R, md)
        json.dump(rows, open(a.check, "w"), indent=0)
    text = "\n".join(md)
    print(text)
    if a.md:
        open(a.md, "w").write(text + "\n")
    if a.json:
        json.dump({f: {i: dict(coef=v["coef"], pets=v["pets"], n=v["n"]) for i, v in res[0].items()} for f, res in results.items()}, open(a.json, "w"), indent=0)


if __name__ == "__main__":
    main()
