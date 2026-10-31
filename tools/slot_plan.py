#!/usr/bin/env python3
"""The 5th active slot (Biting Cold today) priced against the other skills that could sit there, and the
Biting Cold neck base ("Triggers Lv. 20 Biting Cold Curse upon dealing damage", cooldown 0.2 s) that frees it.

Uncapped (real maps), boss setup, on build.json. Usage: python3 tools/slot_plan.py [--duration PCT]

Blink model for the slotted Biting Cold [tlidb]: Terrain of Malice makes the curse an area that lasts the curse
duration (5 s x (1 + duration)) and sets the CD to 8 s; Preparation prepares the skill every 8 s. Below 60%
duration the area is gone for 8 - 5 (1 + d) s of every 8 s. Deepened Curse needs the enemy cursed for 2 s
(read: the blink restarts that), so it is off for the blink + 2 s.
"""
import argparse
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine as E  # noqa: E402

BC = "Biting Cold"
SUPPORTS = "[Preparation, Well-Fought Battle, Mass Effect]"


def run(b, t, change=None, drop_bc=False, add_skill=None):
    b = copy.deepcopy(b)
    if drop_bc:
        b["skills"]["others"] = [x for x in b["skills"]["others"] if not x.startswith(BC)]
    if add_skill:
        b["skills"]["others"].append(add_skill)
    ch = copy.deepcopy(change or {})
    ch.setdefault("context", {})["hit_cap"] = 1e30
    bb, tt = E.apply(b, t, ch)
    return E.dps(bb, tt)


def blink(d):
    """(seconds with no curse, seconds with Biting Cold but no Deepened Curse) per 8 s Preparation cycle."""
    gap = max(0.0, 8.0 - 5.0 * (1 + d))
    return gap, (min(2.0, 8.0 - gap) if gap > 0 else 0.0)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--duration", type=float, help="skill effect duration %% for the blink (default: the sheet's)")
    a = ap.parse_args(argv)
    b, t = E.load()
    full = run(b, t)
    sh = full["sheet"]
    d = (a.duration if a.duration is not None else sh["duration"]) / 100
    ee = sh["empower_effect"]
    no_curse = {"disable": [BC], "context": {"enemy_cursed": False}}

    empty = run(b, t, no_curse, drop_bc=True)["dps"]
    bc_only = run(b, t, {"disable": ["Deepened Curse"]})["dps"]
    gap, dc_off = blink(d)
    today = (gap * empty + dc_off * bc_only + (8 - gap - dc_off) * full["dps"]) / 8

    rows = [
        (f"Biting Cold + Deepened Curse, no blink (60%+ duration)", full["dps"]),
        (f"Biting Cold at {d:.0%} duration (off {gap:.2f} s, Deepened Curse off {gap + dc_off:.2f} s per 8 s)", today),
        ("Ice Bond " + SUPPORTS, run(b, t, no_curse, drop_bc=True, add_skill="Ice Bond " + SUPPORTS)["dps"]),
        ("Blazing Spin (+435% crit rating x empower effect)",
         run(b, t, {**no_curse, "stat_delta": {"crit.rating_inc": 435 * ee}}, drop_bc=True)["dps"]),
        ("Frost Release (+15 cold pen, unscaled; the +81% only lasts 5 casts)",
         run(b, t, {**no_curse, "stat_delta": {"pen.res": 15}}, drop_bc=True)["dps"]),
        ("empty slot", empty),
        ("neck base Lv20 Biting Cold, slot empty", run(b, t, {"context": {"biting_cold_level": 20}}, drop_bc=True)["dps"]),
        ("neck base Lv20 Biting Cold + Ice Bond in the slot",
         run(b, t, {"context": {"biting_cold_level": 20}}, drop_bc=True, add_skill="Ice Bond " + SUPPORTS)["dps"]),
    ]
    print(f"sheet: duration {sh['duration']:.0f}% (blink at {d:.0%}), CDR {sh['cdr']:.1f}%, empower effect x{ee:.2f}, "
          f"crit {sh['crit_chance']:.1f}%, Biting Cold L{sh['level_biting_cold']}, uncapped")
    print(f"{'option':<92}{'vs empty':>9}{'vs today':>9}")
    for name, v in rows:
        print(f"{name:<92}{v / empty:>9.3f}{v / today:>9.3f}")


if __name__ == "__main__":
    main()
