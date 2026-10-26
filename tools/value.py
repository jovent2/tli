#!/usr/bin/env python3
"""Marginal value of a change on a character's current sheet.

Every function returns a multiplier on DPS (1.05 = +5%). Defaults come from the character's
stats.json (default: ss14/thea/stats.json). These are the same rules as docs/mechanics.md.

CLI examples:
  python3 tools/value.py increased 18            # +18% to the increased pool
  python3 tools/value.py flat 97                 # +97 avg flat added damage
  python3 tools/value.py additional 10           # +10% additional
  python3 tools/value.py cast 6
  python3 tools/value.py projspeed 12            # through Gale
  python3 tools/value.py critrating 30           # +30% increased crit rating
  python3 tools/value.py critdmg 14
  python3 tools/value.py frostbite_rating 7.7
  python3 tools/value.py frostbite_effect 12.3
  python3 tools/value.py levels 2                # +2 main-skill levels
  python3 tools/value.py attributes 13           # +13 to STR+DEX+INT
  python3 tools/value.py focus 1                 # +1 max Focus Blessing
  python3 tools/value.py double 2
  python3 tools/value.py --stats other/char/stats.json increased 18
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATS = ROOT / "ss14" / "thea" / "stats.json"


def load(path=DEFAULT_STATS):
    return json.loads(Path(path).read_text())


def ratio(new, old):
    return new / old


def increased(s, pct):
    p = s["increased_pool_pct"]
    return ratio(1 + (p + pct) / 100, 1 + p / 100)


def flat(s, avg_added, effectiveness=None):
    e = s["added_damage_effectiveness"] if effectiveness is None else effectiveness
    b = s["base_damage_avg"]
    return ratio(b + avg_added * e, b)


def additional(s, pct):
    return 1 + pct / 100


def cast(s, pct):
    c = s["cast_speed_increased_pct"]
    return ratio(1 + (c + pct) / 100, 1 + c / 100)


def projspeed(s, pct):
    ps, share = s["proj_speed_increased_pct"], s.get("gale_share", 0.6)
    return ratio(1 + share * (ps + pct) / 100, 1 + share * ps / 100)


def _crit_factor(chance, cd_pct, on_crit):
    p = min(chance, 100) / 100
    return (1 - p) + p * (cd_pct / 100) * on_crit


def critrating(s, inc_pct=0.0, flat_rating=0.0):
    base, inc = s["crit_base_rating"] + s.get("crit_flat_rating", 0), s["crit_rating_increased_pct"]
    old_ch = base * (1 + inc / 100) / 100
    new_ch = (base + flat_rating) * (1 + (inc + inc_pct) / 100) / 100
    oc = s.get("on_crit_multiplier", 1.0)
    return ratio(_crit_factor(new_ch, s["crit_damage_pct"], oc), _crit_factor(old_ch, s["crit_damage_pct"], oc))


def critdmg(s, pct):
    ch, cd, oc = s["crit_chance_pct"], s["crit_damage_pct"], s.get("on_crit_multiplier", 1.0)
    return ratio(_crit_factor(ch, cd + pct, oc), _crit_factor(ch, cd, oc))


def frostbite(s, d_rating=0.0, d_effect=0.0):
    """Max Frostbite Rating caps at 120 (tlidb glossary)."""
    cap = s.get("frostbite_cap", 120)
    r, e = min(cap, s["frostbite_rating"]), s["frostbite_effect_pct"]
    old = 1 + r * (1 + e / 100) / 100
    new = 1 + min(cap, r + d_rating) * (1 + (e + d_effect) / 100) / 100
    return ratio(new, old)


def level_mult(lv):
    m = 1.0
    for l in range(21, lv + 1):
        m *= 1.10 if l <= 30 else 1.08
    return m


def levels(s, n):
    lv = s["main_skill_level"]
    return ratio(level_mult(lv + n), level_mult(lv))


def attributes(s, n):
    a, per = s["attributes_total"], s["attribute_ratio_per_point"]
    return ratio(1 + per * (a + n), 1 + per * a)


def focus(s, n=1):
    """+n max Focus Blessing. Adds each per-stack additional source the sheet lists."""
    f = s["max_focus"]
    m = 1.0
    for pct in s["focus_per_stack_additional_pct"].values():  # each is its own additional multiplier
        m *= ratio(1 + pct * (f + n) / 100, 1 + pct * f / 100)
    cd_per = s.get("focus_per_stack_crit_damage_pct", 0.0)
    if cd_per:
        m *= critdmg(s, cd_per * n)
    return m


def _double_factor(c):
    c = c / 100
    return 1 + c if c <= 1 else 2 * (1 + min(1.0, c - 1))


def double(s, pct):
    c = s["double_chance_pct"]
    return ratio(_double_factor(c + pct), _double_factor(c))


FUNCS = {
    "increased": lambda s, v: increased(s, v),
    "flat": lambda s, v: flat(s, v),
    "additional": lambda s, v: additional(s, v),
    "cast": lambda s, v: cast(s, v),
    "projspeed": lambda s, v: projspeed(s, v),
    "critrating": lambda s, v: critrating(s, inc_pct=v),
    "critflat": lambda s, v: critrating(s, flat_rating=v),
    "critdmg": lambda s, v: critdmg(s, v),
    "frostbite_rating": lambda s, v: frostbite(s, d_rating=v),
    "frostbite_effect": lambda s, v: frostbite(s, d_effect=v),
    "levels": lambda s, v: levels(s, int(v)),
    "attributes": lambda s, v: attributes(s, v),
    "focus": lambda s, v: focus(s, int(v)),
    "double": lambda s, v: double(s, v),
}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=sorted(FUNCS))
    ap.add_argument("amount", type=float)
    ap.add_argument("--stats", default=str(DEFAULT_STATS))
    a = ap.parse_args(argv)
    s = load(a.stats)
    m = FUNCS[a.kind](s, a.amount)
    print(f"{a.kind} {a.amount:g}: x{m:.4f}  ({(m - 1) * 100:+.2f}%)")


if __name__ == "__main__":
    main()
