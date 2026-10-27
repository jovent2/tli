#!/usr/bin/env python3
"""Turn a line of TLI game text into stat keys.

  >>> parse("+(13–14)% additional Cold Damage for every stack of Focus Blessing")
  [Stat(key='add.cold_per_focus', value=13.5, lo=13.0, hi=14.0, cond=None)]

  python3 tools/stats.py "+18% Spell Damage" "+1 to Max Focus Blessing Stacks"
  python3 tools/stats.py --coverage          # how much of the game's text is understood

Key families (what the engine and scanners use):
  inc.*     increased damage (pool):   damage spell projectile cold elemental physical area
  add.*     additional damage:         damage spell cold projectile elemental hit vs_frozen vs_cursed on_crit
            *_per_focus variants are per Focus Blessing stack
  enh.*     "Damage Enhancement" (tangle, focus...) — treated as its own additional multiplier
  crit.*    rating_inc (%), flat, dmg, dmg_per_focus
  cast.*    inc, add          proj.speed
  attr.*    int str dex all int_pct all_pct
  lvl.*     all spell cold physical projectile spell_projectile main active support (+ others)
  focus.max  bless.duration  double.chance  pen.res  pen.armor  frost.max  frost.effect
  dur  cdr  flat.cold  flat.physical  flat.fire|lightning|erosion  tangle.max  tangle.attach
  curse.effect  aura.effect  aggression.effect
  es.flat es.pct es.add  res.fire|cold|lightning|erosion|ele|all  block.attack|spell|ratio  life.*  ms
  enemy.*   debuffs applied to the enemy (cold_infiltration, frail, paralysis, ...)
cond = a condition the line depends on (e.g. "focus" when it needs Focus Blessing active).
"""
import re
import sys
from dataclasses import dataclass, asdict

RANGE = r"[+-]?\(?-?\d+(?:\.\d+)?(?:\s*–\s*-?\d+(?:\.\d+)?)?\)?"  # en dash = range; " - " separates min/max
NUM_RX = re.compile(r"([+-]?)\(?(-?\d+(?:\.\d+)?)(?:\s*[–]\s*(-?\d+(?:\.\d+)?))?\)?")


@dataclass
class Stat:
    key: str
    value: float
    lo: float
    hi: float
    cond: str | None = None


def numbers(line):
    out = []
    for m in NUM_RX.finditer(line):
        sign, a, b = m.group(1), float(m.group(2)), m.group(3)
        lo, hi = a, float(b) if b is not None else a
        if sign == "-" and lo > 0:
            lo, hi = -lo, -hi
        out.append((lo, hi))
    return out


# (regex on the line with numbers replaced by '#', key or callable, cond)
# First match wins, so specific patterns go before general ones.
R = []


def rule(pat, key, cond=None, idx=0):
    R.append((re.compile("^" + pat + "$", re.I), key, cond, idx))


# --- skip noise
rule(r"\(Max Active Divinity: #\)", None)
rule(r"\(Max Active Divinity Slate: #\)", None)
rule(r"Require lv #.*", None)

# --- per-Focus scaling
rule(r"# ?% additional Cold Damage for every stack of Focus Blessing", "add.cold_per_focus")
rule(r"# ?% additional Spell Damage per stack of Focus Blessing owned", "add.spell_per_focus")
rule(r"# ?% (?:Spell )?Critical Strike Damage per stack of Focus Blessing owned", "crit.dmg_per_focus")
rule(r"# ?% additional (?:Spell )?Damage at Max Focus Blessings?", "add.spell", "max_focus")
rule(r"# to Max Focus Blessing Stacks", "focus.max")
rule(r"# to Max Focus Blessing Stacks while having at least # Intelligence", "focus.max", "500_int")
rule(r"# to Max Focus Blessing Stacks if you have landed a Critical Strike or Reaped in the last #s", "focus.max", "crit_recent")
rule(r"# ?% (?:Focus )?Blessing Duration", "bless.duration")

# --- additional damage
rule(r"# ?% additional damage", "add.damage")
rule(r"# ?% additional Spell Damage", "add.spell")
rule(r"# ?% additional Cold Damage", "add.cold")
rule(r"# ?% additional Elemental Damage", "add.elemental")
rule(r"# ?% additional Projectile Damage", "add.projectile")
rule(r"# ?% additional Hit Damage", "add.hit")
rule(r"# ?% additional damage against Frozen enemies", "add.vs_frozen")
rule(r"# ?% additional damage against Cursed enemies", "add.vs_cursed")
rule(r"# ?% additional damage on Critical Strike", "add.on_crit")
rule(r"# ?% additional damage applied to Life", "add.damage")   # Steel Vanguard legendary; bosses are all Life [Vlad: = 8% additional]
rule(r"# ?% additional damage when having both Sealed Mana and Life", "add.damage", "sealed_both")
rule(r"# ?% additional Spell Damage when the Energy Shield is not low", "add.spell", "es_not_low")
rule(r"# ?% additional Cast Speed", "cast.add")
rule(r"# ?% Tangle Damage Enhancement", "enh.tangle")
rule(r"# ?% additional Tangle Damage", "add.tangle")

# --- increased damage
rule(r"# ?% damage", "inc.damage")
rule(r"# ?% Spell Damage", "inc.spell")
rule(r"# ?% Projectile Damage", "inc.projectile")
rule(r"# ?% Cold Damage", "inc.cold")
rule(r"# ?% Elemental Damage", "inc.elemental")
rule(r"# ?% Physical Damage", "inc.physical")
rule(r"# ?% Area Damage", "inc.area")
rule(r"# ?% damage while Focus Blessing is active", "inc.damage", "focus")
rule(r"# ?% damage when having Focus Blessing", "inc.damage", "focus")
rule(r"# ?% Spell Damage when having Focus Blessing", "inc.spell", "focus")
rule(r"# ?% Spell Damage while Focus Blessing is active", "inc.spell", "focus")
rule(r"# ?% Cold Damage, # ?% Minion Cold Damage", "inc.cold")
rule(r"# ?% damage, # ?% Minion Damage", "inc.damage")

# --- crit
rule(r"# ?% (?:Spell )?Critical Strike Rating", "crit.rating_inc")
rule(r"# ?% Critical Strike Rating, # ?% Minion Critical Strike Rating", "crit.rating_inc")
rule(r"# (?:Spell |Attack and Spell )?Critical Strike Rating", "crit.flat")
rule(r"# ?% (?:Spell |Cold Skill |Spell Skill )?Critical Strike Damage", "crit.dmg")
rule(r"# ?% Critical Strike Damage against enemies", "crit.dmg")
rule(r"Upon inflicting damage, # ?% Hit Damage for every type of Ailment the enemy has", "inc.hit_per_ailment")
rule(r"# ?% additional Physical Damage", "add.physical")

# --- speed
rule(r"# ?% (?:Attack and )?Cast Speed", "cast.inc")
rule(r"# ?% Cast Speed when Focus Blessing is active", "cast.inc", "focus")
rule(r"# ?% Attack and Cast Speed, # ?% Minion Attack and Cast Speed", "cast.inc")
rule(r"# ?% Attack Speed and Cast Speed when having Agility Blessing", "cast.inc", "agility")
rule(r"# ?% Projectile Speed", "proj.speed")
rule(r"# ?% additional Projectile Speed", "proj.speed_add")
rule(r"# ?% Movement Speed", "ms")

# --- attributes
rule(r"# Intelligence", "attr.int")
rule(r"# Strength", "attr.str")
rule(r"# Dexterity", "attr.dex")
rule(r"# to All Stats", "attr.all")
rule(r"# ?% Intelligence", "attr.int_pct")
rule(r"# ?% All Stats", "attr.all_pct")
rule(r"# Strength and Intelligence", "attr.str_int")
rule(r"# Dexterity and Intelligence", "attr.dex_int")

# --- levels
rule(r"# to All Skills' Levels", "lvl.all")
rule(r"# Spell Skill Level", "lvl.spell")
rule(r"# Cold Skill Level", "lvl.cold")
rule(r"# Physical Skill Level", "lvl.physical")
rule(r"# Projectile Skill Level", "lvl.projectile")
rule(r"# Spell Projectile Skill Level", "lvl.spell_projectile")
rule(r"# (?:to )?Main Skill Level", "lvl.main")
rule(r"# Active Skill Level", "lvl.active")
rule(r"# Support Skill Level", "lvl.support")
rule(r"# (Fire|Lightning|Erosion|Attack|Minion|Passive|Defensive|Beam) Skill Level", "lvl.other")

# --- double, pen, frostbite, timing
rule(r"# ?% chance to deal Double Damage", "double.chance")
rule(r"# ?% Elemental and Erosion Resistance Penetration", "pen.res")
rule(r"Damage Penetrates # ?% (?:Elemental|Cold) Resistance", "pen.res")
rule(r"# ?% (?:Elemental|Cold) (?:Resistance )?Penetration", "pen.res")
rule(r"# ?% Armor DMG Mitigation Penetration", "pen.armor")
rule(r"# to Max Frostbite Rating", "frost.max")
rule(r"# ?% Frostbite Effect", "frost.effect")
rule(r"# ?% Skill Effect Duration", "dur")
rule(r"# ?% Cooldown Recovery Speed", "cdr")

# --- flat added
rule(r"Adds # - # Cold Damage to (?:Attacks and )?Spells", "flat.cold")
rule(r"Adds # - # Physical Damage to (?:Attacks and )?Spells", "flat.physical")
rule(r"Adds # - # (Fire|Lightning|Erosion) Damage to (?:Attacks and )?Spells", "flat.other")

# --- tangles, curses, auras
rule(r"# Max Tangle Quantity", "tangle.max")
rule(r"You can apply # additional Tangle\(s\) to enemies", "tangle.attach")
rule(r"# ?% Curse Effect", "curse.effect")
rule(r"# ?% Aura Effect", "aura.effect")
rule(r"# ?% Spell Aggression Effect", "aggression.effect")

# --- enemy debuffs
rule(r"Inflicts Cold Infiltration when dealing damage.*", "enemy.cold_infiltration")
rule(r"Inflicts Frail (?:when dealing|on) Spell Damage.*", "enemy.frail")

# --- defense
rule(r"# (?:Max|gear) Energy Shield", "es.flat")
rule(r"# ?% (?:Max|gear) Energy Shield", "es.pct")
rule(r"# ?% additional Max Energy Shield", "es.add")
rule(r"# ?% Max Life and Max Energy Shield", "es.pct")
rule(r"# ?% Max Life, # ?% Max Energy Shield", "es.pct", None, 1)
rule(r"# ?% (Fire|Cold|Lightning|Erosion) Resistance", "res.one")
rule(r"# ?% Elemental Resistance", "res.ele")
rule(r"# ?% Elemental and Erosion Resistance", "res.all")
rule(r"# ?% Attack Block Chance", "block.attack")
rule(r"# ?% Spell Block Chance", "block.spell")
rule(r"# ?% Attack and Spell Block Chance", "block.both")
rule(r"# ?% Block Ratio", "block.ratio")
rule(r"# Max Life", "life.flat")
rule(r"# ?% Max Life", "life.pct")

# --- more specific / conditional lines worth knowing about
rule(r"# ?% additional Cold Damage and # ?% Cold Penetration when you have at least # stack\(s\) of Focus Blessing",
     "add.cold", "focus>=N")
rule(r"You can cast # additional Curses", "curse.extra")
rule(r"# ?% chance to gain # stacks? of Focus Blessing on (?:defeat|hit)", "focus.gain")
rule(r"# ?% Max Cold Resistance", "res.max_cold")
rule(r"# ?% Attack Speed, Cast Speed, and Movement Speed when having Hasten", "cast.inc", "hasten")
rule(r"# ?% damage per stack of any Blessing", "inc.damage_per_blessing")
rule(r"# Horizontal Projectile Penetration\(s\)", "proj.penetration")
rule(r"# ?% Cold Infiltration Effect", "enemy.cold_infiltration_effect")
rule(r"# Empower Skill Level", "lvl.empower")
rule(r"# ?% (?:additional )?Tangle Duration", "tangle.duration")
rule(r"# ?% damage against Cursed enemies", "inc.vs_cursed")
rule(r"# ?% Projectile Critical Strike Rating", "crit.rating_inc", "projectile")
rule(r"# ?% additional damage to Elites", "add.vs_elite")
rule(r"Additional # ?% Skill Effect Duration", "dur")
rule(r"# ?% additional Critical Strike Damage against Paralyzed enemies", "crit.dmg_add", "paralyzed")
rule(r"# ?% (Fire and Cold|Cold and Lightning) Resistance", "res.two")
rule(r"# ?% Critical Strike Damage Mitigation", "def.crit_mitigation")
rule(r"# ?% chance to avoid Spell Damage", "def.spell_avoid")
rule(r"Adds # - # \w+ Damage to the gear", "weapon.local")
rule(r"# ?% (?:gear Attack Speed|Gear Physical Damage|Attack Critical Strike Rating for this gear)", "weapon.local")
rule(r"# to Attack Skill Level", "lvl.other")
rule(r"# ?% Skill Area", "area")
rule(r"# Max Spell Burst", "other.spell_burst")

TEMPLATE_RX = re.compile(RANGE)
# lines that are mechanics rather than plain stats: flagged for a human (or Claude) to price by hand
SPECIAL_HINT = re.compile(r"for every|for each|per \d|chance for that cast|trigger the Main Spell Skill|"
                          r"is also applied|supported by Lv|Replaces|Converts|Gains .* stack|when .* recently", re.I)

RES_NAMES = ("Fire", "Cold", "Lightning", "Erosion")


def template(line):
    return TEMPLATE_RX.sub("#", line).strip()


def _parse_part(part):
    t = template(part)
    nums = numbers(part)
    for rx, key, cond, idx in R:
        if rx.match(t):
            if key is None:
                return []
            if key == "res.one":
                el = next((n for n in RES_NAMES if f"{n} Resistance" in part), "x").lower()
                key = f"res.{el}"
            if nums:
                lo, hi = nums[min(idx, len(nums) - 1)]
                if key.startswith("flat.") and len(nums) >= 2:  # Adds (a–b) - (c–d): avg of min and max
                    lo, hi = (nums[0][0] + nums[1][0]) / 2, (nums[0][1] + nums[1][1]) / 2
            else:
                lo = hi = 1.0
            return [Stat(key, (lo + hi) / 2, lo, hi, cond)]
    return None


from functools import lru_cache


@lru_cache(maxsize=None)
def _parse_cached(line):
    return tuple(_parse_uncached(line))


def parse(line: str) -> list[Stat]:
    return [Stat(**asdict(s)) for s in _parse_cached(line)]


def _parse_uncached(line: str) -> list[Stat]:
    """Stats in a line. ' / '-separated parts (two-line affixes) and 'X and Y' lines are split.
    Unparsed parts are dropped; use special() to find lines that need hand pricing."""
    out = []
    for part in [p.strip() for p in line.split(" / ") if p.strip()]:
        r = _parse_part(part)
        if r is None and " and " in part:
            # "+X Spell Critical Strike Rating and +Y% additional damage on Critical Strike for each activated Tangle"
            m = re.search(r"\s(for each|per|while|when)\s.*$", part)
            tail = m.group(0) if m else ""
            core = part[: m.start()] if m else part
            pieces = [p.strip() for p in re.split(r"\s+and\s+(?=[+-]?\(?\d)", core)]
            if len(pieces) > 1:
                r = []
                for p in pieces:
                    rr = _parse_part(p)
                    if rr:
                        for s in rr:
                            s.cond = (s.cond or "") + (tail.strip() if tail else "") or None
                        r += rr
        if r:
            out += r
    return out


def special(line: str) -> bool:
    """True if the line is a mechanic (conditional / per-X / conversion) the parser can't price."""
    return bool(SPECIAL_HINT.search(line)) and not parse(line)


# stats Thea's damage depends on (used to decide what's "relevant")
THEA = {"inc.damage", "inc.spell", "inc.projectile", "inc.cold", "inc.elemental", "inc.area",
        "add.damage", "add.spell", "add.cold", "add.elemental", "add.projectile", "add.hit", "add.vs_frozen",
        "add.vs_cursed", "add.on_crit", "add.cold_per_focus", "add.spell_per_focus", "add.tangle", "enh.tangle",
        "crit.rating_inc", "crit.flat", "crit.dmg", "crit.dmg_per_focus", "cast.inc", "cast.add", "proj.speed",
        "attr.int", "attr.str", "attr.dex", "attr.all", "attr.int_pct", "attr.all_pct", "attr.str_int", "attr.dex_int",
        "lvl.all", "lvl.spell", "lvl.cold", "lvl.physical", "lvl.projectile", "lvl.spell_projectile", "lvl.main",
        "lvl.active", "lvl.support", "focus.max", "double.chance", "pen.res", "pen.armor", "frost.max",
        "frost.effect", "dur", "cdr", "flat.cold", "flat.physical", "tangle.max", "tangle.attach", "curse.effect",
        "aura.effect", "aggression.effect", "enemy.cold_infiltration", "enemy.frail", "bless.duration"}


def coverage():
    import glob
    import json
    from collections import Counter
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    lines = []
    for f in glob.glob(str(root / "data/affixes/*.json")):
        d = json.load(open(f))
        for side in ("prefix", "suffix"):
            lines += [r["modifier"] for r in d[side]]
    for it in json.load(open(root / "data/legendaries.json")):
        lines += it.get("lines", []) + it.get("corroded", [])
    for p in json.load(open(root / "data/talents.json")):
        for n in p["nodes"]:
            lines += n["lines"]
    parsed = Counter()
    miss = Counter()
    for l in lines:
        if not re.search(r"\d", l):
            continue
        st = parse(l)
        if st:
            parsed[l] += 1
        else:
            miss[template(l)] += 1
    tot = sum(parsed.values()) + sum(miss.values())
    print(f"numeric lines {tot}: parsed {sum(parsed.values())} ({100 * sum(parsed.values()) / tot:.0f}%)")
    print("top unparsed templates:")
    for t, n in miss.most_common(40):
        print(f"  {n:4d}  {t}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--coverage":
        coverage()
    else:
        for l in sys.argv[1:]:
            print(l, "->", [asdict(s) for s in parse(l)])
