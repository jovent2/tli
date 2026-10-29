"""Greedy strategy search for Vlad: 4 compass slots, 1 Profound probe, 92 Star + 4 Prime, Profound T8 Glacial Abyss.
For every candidate compass set the tree is re-optimized (best_subtree per constellation + knapsack over the budget split)."""
import itertools, sys, collections
import runs as RN, mech, chart
from bottomup import *
from plan2 import *

STAR = 92; PRIME = 4; PROF_STAR = 25            # Profound: 2 micros + 30% major + 12% major (25 Star extra) = 4 Prime + 25 Star
INSTANCE_CANDIDATES = ["Cruising_Mechanical_Compass_%28Artifact%29", "Revelation_Hunting_Astrolabe", "General_Hunting_Astrolabe", "Hunting_Astrolabe", "Collection_Doll_Astrolabe_%28Artifact%29", "Collection_Doll_Astrolabe",
                       "Alert_Outlaw_Compass", "Full_Load_Outlaw_Compass", "Bounty_Outlaw_Compass", "Outlaw_Compass", "Containment_Overrealm_Compass", "Overrealm_Compass", "Shadow_Overrealm_Compass",
                       "Lunar_Stele_Lunaria_Compass", "Moonlit_Casket_Lunaria_Compass", "Pristine_Lunaria_Compass", "Lunaria_Compass", "All-Evil_Vigil_Compass", "Evernight_Vigil_Compass", "Phantom_Vigil_Compass", "Vigil_Compass",
                       "Bandit_Dark_Surge_Compass", "Divine_Warrior_Dark_Surge_Compass", "Dark_Surge_Compass", "Consultation_Vorax_Compass", "Scavenger_Vorax_Compass", "The_Fated_Arcana_Compass", "Sandlord_Compass",
                       "Onslaught_Might_Compass", "Mecha_Might_Compass_%28Artifact%29", "Flourishing_Might_Compass", "Flourishing_Gods_Compass", "Mystery_Treasure_Gods_Compass", "War_Compass", "Strength_in_Numbers_Soldier_Compass", "Soldier_Compass", "Elite_Compass", "Record_Creation_Compass", "Creation_Compass", "Uncanny_Folklore_Compass"]
MULT_CANDIDATES = ["Generous_Elite_Compass", "Bountiful_Elite_Compass", "Sinful_Plunder_Compass", "Sinful_Plunder_Compass_%28Artifact%29", "Vast_Ecliptic_Astrolabe", "Ascendant_Ecliptic_Astrolabe", "Ecliptic_Astrolabe", "Colorful_Fluorescent_Compass_%28Artifact%29", "Colorful_Fluorescent_Compass",
                   "Focus_Fluorescent_Compass", "Transgression_Plunder_Compass", "Bounty_Ember_Compass", "Ember_Compass"]
PROBES = ["Flourishing_Profound_Probe", "Compass_Profound_Probe", "Gear_Profound_Probe", "Ember_Profound_Probe", "Fluorescent_Profound_Probe"]
GENERIC_CONST = ["Compass_Talent_Constellation", "Commodities_Talent_Constellation", "Legendary_Gear_Talent_Constellation", "Gear_Talent_Constellation", "Beacon_Talent_Constellation"]

def constellations_for(plan):
    cs = set(GENERIC_CONST)
    for k in plan.compasses:
        M = mech.compass_family(k)
        if M and M in CONST_KEY: cs.add(CONST_KEY[M])
    return sorted(cs)

def optimize_tree(F, LA, plan, budget=STAR - PROF_STAR, extra_consts=()):
    consts = sorted(set(constellations_for(plan)) | set(extra_consts))
    per = best_tree(F, LA, plan, consts, budget)
    # knapsack over constellations: value curve per budget
    best = {0: (0.0, {})}
    for ck in consts:
        res, _ = per[ck]; nxt = dict(best)
        for b0, (v0, split) in best.items():
            for k in range(1, budget - b0 + 1):
                if k not in res: continue
                v = v0 + res[k][0]
                if b0 + k not in nxt or v > nxt[b0 + k][0]: nxt[b0 + k] = (v, dict(split, **{ck: k}))
        best = nxt
    b, (v, split) = max(best.items(), key=lambda kv: kv[1][0])
    return apply_tree(plan, per, split), split

def greedy(F, LA, start=None, steps=5, verbose=True, extra_consts=(), fixed=()):
    plan = start or Plan({}, {}, PROFOUND)
    plan, split = optimize_tree(F, LA, plan, extra_consts=extra_consts)
    cur = evaluate(F, LA, plan); hist = [(cur["net_per_min"], dict(plan.compasses), dict(plan.probes), split)]
    for step in range(steps):
        best = None
        slots = sum(plan.compasses.values())
        cands = []
        fams = {mech.compass_family(k) for k in plan.compasses if mech.compass_family(k) and not mech.compass_family(k).startswith("generic")}
        # one gameplay compass per family: a second "the stage has X" compass does not add a second X
        if slots < 4: cands += [("c", k) for k in INSTANCE_CANDIDATES + MULT_CANDIDATES if k not in plan.compasses and not (mech.compass_family(k) in fams)]
        if not plan.probes: cands += [("p", k) for k in PROBES]
        cands += [("-c", k) for k in plan.compasses if k not in fixed]
        for kind, k in cands:
            comp, prob = dict(plan.compasses), dict(plan.probes)
            if kind == "c": comp[k] = 1
            elif kind == "p": prob[k] = 1
            else: comp.pop(k)
            p2, sp2 = optimize_tree(F, LA, Plan(comp, prob, PROFOUND), extra_consts=extra_consts)
            e = evaluate(F, LA, p2)
            if best is None or e["net_per_min"] > best[0]: best = (e["net_per_min"], p2, sp2, kind, k)
        if best is None or best[0] <= cur["net_per_min"] + 0.5: break
        plan, split = best[1], best[2]; cur = evaluate(F, LA, plan)
        if verbose: print(f"  step {step + 1}: {best[3]} {best[4][:40]:40s} -> {cur['net_per_min']:.0f} FE/min  (net {cur['net']:.0f}/map, {cur['secs']:.0f} s)", flush=True)
        hist.append((cur["net_per_min"], dict(plan.compasses), dict(plan.probes), split))
    return plan, split, cur, hist

def describe_tree(plan):
    c = collections.Counter(); names = collections.defaultdict(collections.Counter)
    for m, txt, cnt in plan.nodes:
        if m == "Profound": continue
        c[m] += cnt; names[m][txt[:90]] += cnt
    return c, names

if __name__ == "__main__":
    F, LA = load_fit()
    seeds = {
        "free (greedy from empty)": None,
        "Machines (Cruising + Focus + Colorful A + Transgression)": Plan({"Cruising_Mechanical_Compass_%28Artifact%29": 1, "Focus_Fluorescent_Compass": 1, "Colorful_Fluorescent_Compass_%28Artifact%29": 1, "Transgression_Plunder_Compass": 1}, {}, PROFOUND),
        "Machines (Cruising fixed, rest free)": Plan({"Cruising_Mechanical_Compass_%28Artifact%29": 1}, {}, PROFOUND),
        "Safari (Revelation fixed)": Plan({"Revelation_Hunting_Astrolabe": 1}, {}, PROFOUND),
        "Dark Surge (Bandit fixed)": Plan({"Bandit_Dark_Surge_Compass": 1}, {}, PROFOUND),
        "Outlaw (Alert fixed)": Plan({"Alert_Outlaw_Compass": 1}, {}, PROFOUND),
    }
    results = []
    for name, seed in seeds.items():
        print(f"\n===== {name}", flush=True)
        plan, split, cur, hist = greedy(F, LA, seed, steps=3, fixed=tuple(seed.compasses) if seed else ())
        results.append((cur["net_per_min"], name, plan, split, cur))
        e = report(F, LA, plan, name + " [optimized]")
        c, names = describe_tree(plan)
        print("   tree:", dict(c), "| split:", {k.replace('_Talent_Constellation', ''): v for k, v in split.items()})
        for m, nn in names.items(): print(f"     {m}: " + "; ".join(f"{v}x {t[:60]}" for t, v in nn.most_common(6)))
    print("\n\n===== RANKING (net FE/min at Vlad's times)")
    for v, name, plan, split, cur in sorted(results, reverse=True):
        print(f"  {v:6.0f} FE/min  {name:28s} net {cur['net']:5.0f}/map  {cur['secs']:4.0f} s  compasses {list(plan.compasses)} probe {list(plan.probes)}")
