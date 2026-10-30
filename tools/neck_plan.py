#!/usr/bin/env python3
"""Sacrificer's Necklace plan vs I Am Truth, on Vlad's terms (2026-10-30 22:00).

Both sides get one wand at T0 Double Damage (+34%), so Double is at the quad cap on both and the belt's 18% does not count.
Plan side:
  neck: I Am Truth -> Sacrificer's Necklace, base affix "Triggers Lv. 20 Biting Cold Curse upon dealing damage to enemies. Cooldown: 0.2 s"
        ult prefix  "You can apply 1 additional Tangle(s) to enemies / +(5-8)% Tangle Damage Enhancement" (T1)  [or +2 Active Skill Level]
        ult suffix  "+(15-20)% Aura Effect" at 18
        adv suffix  "+(61-78)% Critical Strike Damage" T0
        adv prefix  T0 INT: not counted (the chest's INT line becomes "You can cast 1 additional Curses" [Vlad])
  belt: Hasten -> +25% Cooldown Recovery Speed (base), 18% Double -> +30% Skill Effect Duration (ult suffix); keeps Gale
  skills: the Biting Cold slot -> Timid (same supports); tangles 3 attached / 1 dormant (4 max with Peculiar Vibe)
Usage: python3 tools/neck_plan.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine

NECK = ["You can apply 1 additional Tangle(s) to enemies", "+8% Tangle Damage Enhancement", "+18% Aura Effect", "+70% Critical Strike Damage"]
NECK_ACTIVE = ["+2 Active Skill Level", "+18% Aura Effect", "+70% Critical Strike Damage"]
TIMID = "Timid [Preparation, Terrain of Malice, Deepened Curse, Increased Area]"
WAND_DD = [["weapon_m", "+34% chance to deal Double Damage"]]
BELT = {"remove_lines": [["belt", "+18% chance to deal Double Damage"]],
        "add_lines": [["belt", "+30% Skill Effect Duration"], ["belt", "+25% Cooldown Recovery Speed"]]}


def plan(neck, tangles=(3, 1), timid=True, belt=True, aura_delta=0.0):
    ch = {"remove": ["gear:neck"], "add_items": [["neck", list(neck)]],   # copy: callers append to it
          "add_lines": list(WAND_DD) + (BELT["add_lines"] if belt else []),
          "remove_lines": BELT["remove_lines"] if belt else [],
          "context": {"tangles_active": tangles[0], "tangles_dormant": tangles[1], "hasten": not belt, "biting_cold_level": 20}}
    if timid:
        ch["replace_skill"] = [["Biting Cold", TIMID]]
    if aura_delta:
        ch["stat_delta"] = {"aura.effect": aura_delta}
    return ch


def base(aura_delta=0.0):
    ch = {"add_lines": list(WAND_DD)}
    if aura_delta:
        ch["stat_delta"] = {"aura.effect": aura_delta}
    return ch


def run(label, ch_a, ch_b, b, t):
    ra = engine.dps(*engine.apply(b, t, ch_a)); rb = engine.dps(*engine.apply(b, t, ch_b))
    sa, sb = ra["sheet"], rb["sheet"]
    print(f"\n== {label}: {engine.fmt_T(ra['dps'])} -> {engine.fmt_T(rb['dps'])}  = x{rb['dps'] / ra['dps']:.3f}")
    print(f"   Boon margin {sa['boon_margin']:.2f} -> {sb['boon_margin']:.2f}   duration {sa['duration']:.0f} -> {sb['duration']:.0f}   CDR {sa['cdr']:.0f} -> {sb['cdr']:.0f}"
          f"   Chromatic L{sa['level_chromatic']:.0f} -> L{sb['level_chromatic']:.0f}   double {ra['double_chance']:.0f}% -> {rb['double_chance']:.0f}%")
    keys = sorted(set(ra["mult"]) | set(rb["mult"]) | set(ra["enemy"]) | set(rb["enemy"]))
    rows = []
    for k in keys:
        va = ra["mult"].get(k, ra["enemy"].get(k, 1.0)); vb = rb["mult"].get(k, rb["enemy"].get(k, 1.0))
        if abs(vb / va - 1) > 0.002:
            rows.append((vb / va, k, va, vb))
    for r, k, va, vb in sorted(rows, key=lambda x: -abs(x[0] - 1)):
        print(f"   x{r:6.3f}  {k[:70]:70s} {va:.3f} -> {vb:.3f}")
    print(f"   x{rb['crit'] / ra['crit']:6.3f}  crit factor {ra['crit']:.3f} -> {rb['crit']:.3f}")
    print(f"   x{rb['casts_per_tangle'] / ra['casts_per_tangle']:6.3f}  casts/s/tangle {ra['casts_per_tangle']:.2f} -> {rb['casts_per_tangle']:.2f}")
    print(f"   x{rb['double'] / ra['double']:6.3f}  double x{ra['double']:.2f} -> x{rb['double']:.2f}")
    return rb["dps"] / ra["dps"]


if __name__ == "__main__":
    b, t = engine.load()
    print("baseline (as built, belt on):", engine.fmt_T(engine.dps(b, t)["dps"]))
    run("tangle neck, Timid, belt rework (today)", base(), plan(NECK), b, t)
    run("same, after the prism (+63% aura effect on both)", base(63), plan(NECK, aura_delta=63), b, t)
    run("+2 Active instead of the tangle (today)", base(), plan(NECK_ACTIVE, tangles=(2, 2)), b, t)
    run("+2 Active, after the prism", base(63), plan(NECK_ACTIVE, tangles=(2, 2), aura_delta=63), b, t)
    run("tangle neck but the 3rd tangle does not attach (2/2)", base(), plan(NECK, tangles=(2, 2)), b, t)
    run("tangle neck without Timid (no +1 curse on the chest)", base(), plan(NECK, timid=False), b, t)
