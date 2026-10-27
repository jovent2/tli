#!/usr/bin/env python3
"""Thea DPS engine: build.json + trees.json + tlidb data -> stat sheet -> DPS.

  python3 tools/engine.py                       # sheet (vs in-game), every multiplier, DPS
  python3 tools/engine.py --belt-off            # same with the belt removed (how Vlad measures)
  python3 tools/engine.py --remove gear:belt --remove slates:Fallen\\ Starlight
  python3 tools/engine.py --add-line ring_l "+30% Critical Strike Rating"
  python3 tools/engine.py --test                # run ss14/thea/tests.json and report fit

Everything here follows docs/mechanics.md. Where the game was measured to disagree with tlidb
text, the measured rule wins and is marked [measured].
"""
import argparse
import copy
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stats  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CHAR = ROOT / "ss14" / "thea"
DATA = ROOT / "data"

_SKILLS = None


def skills():
    global _SKILLS
    if _SKILLS is None:
        _SKILLS = {s["key"]: s for s in json.loads((DATA / "skills.json").read_text(encoding="utf-8"))}
    return _SKILLS


def skill_value(key, level, rx, idx=0):
    """Number captured by rx in a skill's level-`level` text (levels capped at 40 in tlidb tables)."""
    s = skills()[key]
    lv = str(max(1, min(40, int(level))))
    text = re.sub(r"\+(?=[\d(])", "", " / ".join(s["levels"][lv]))  # tlidb writes "+69%" on some levels, "69%" on others
    m = re.search(rx, text)
    if not m:
        raise KeyError(f"{key} L{lv}: /{rx}/ not in: {text[:200]}")
    return float(m.group(1 + idx))


def level_mult(lv):
    m = 1.0
    for l in range(21, int(lv) + 1):
        m *= 1.10 if l <= 30 else 1.08
    return m


# --------------------------------------------------------------------------- collect stats

_PANELS = None


def panels_data():
    global _PANELS
    if _PANELS is None:
        _PANELS = {p["key"]: p for p in json.loads((DATA / "talents.json").read_text(encoding="utf-8"))}
    return _PANELS


def tree_lines(trees):
    panels = panels_data()
    out = []
    for pa in trees["panels"]:
        lay = {n["id"]: n for n in panels[pa["panel"]]["layout"]}
        for nid, rank in pa["nodes"].items():
            for l in lay[nid]["lines"]:
                if l.startswith("(Max Active"):
                    continue
                out.append((f"tree:{pa['panel']}:{nid}", l, rank))
        core = next((c for c in panels[pa["panel"]]["cores"] if c["name"] == pa.get("core")), None)
        if core:
            for l in core["lines"]:
                out.append((f"core:{core['name']}", l, 1))
    return out


def scale_slate_value(v, eff):
    """Slate line value with Judgment effect; '+1' style lines round (1 x 1.54 -> 2)."""
    x = v * (1 + eff / 100)
    return round(x) if abs(v) <= 3 and float(v).is_integer() else x


def collect(build, trees):
    """All (source, Stat) pairs plus explicit effects."""
    recs = []
    ctx = build["context"]

    def add_line(src, line, mult=1.0, eff=0.0):
        for s in stats.parse(line):
            v = s.value
            if eff:
                v = scale_slate_value(v, eff)
            v *= mult
            c = (s.cond or "")
            if "each activated Tangle" in c:
                v *= ctx["tangles_active"]
            if c == "500_int":
                pass  # resolved after INT is known (not used by this build)
            recs.append((src, s.key, v, s.cond, line))

    for g in build["gear"]:
        for l in g["lines"]:
            add_line(f"gear:{g['slot']}", l)
        for e in g.get("effects", []):
            recs.append((f"gear:{g['slot']}", e["key"], e["value"], None, e["why"]))
    for m in build["memories"]:
        for l in m["lines"]:
            add_line(f"memory:{m['slot']}", l)
    for sl in build["slates"]:
        for l in sl["lines"]:
            add_line(f"slates:{sl['name']}", l, eff=sl.get("effect_pct", 0))
        for e in sl.get("effects", []):
            recs.append((f"slates:{sl['name']}", e["key"], e["value"], None, e["why"]))
    for p in build["pacts"]:
        for l in p["lines"]:
            add_line(f"pact:{p['name']}", l)
        for e in p.get("effects", []):
            recs.append((f"pact:{p['name']}", e["key"], e["value"], None, e["why"]))
    for l in build["kismets"]["lines"]:
        add_line("kismets", l)
    for src, l, rank in tree_lines(trees):
        add_line(src, l, mult=rank)
    return recs


def totals(recs):
    t = defaultdict(float)
    for src, key, v, cond, line in recs:
        t[key] += v
    return t


# --------------------------------------------------------------------------- sheet

def sheet(build, trees):
    recs = collect(build, trees)
    t = totals(recs)
    ctx = build["context"]
    sh = {}
    # levels
    lv_all = t["lvl.all"]
    sh["level_chromatic"] = 20 + lv_all + t["lvl.spell"] + t["lvl.cold"] + t["lvl.physical"] + t["lvl.projectile"] + t["lvl.main"]
    otbt = 4 if ctx.get("off_the_beaten_track", True) else 0                 # Lich core: +4 support levels
    sh["level_support_spell"] = 20 + lv_all + otbt + t["lvl.spell"]        # Spell Tangle, Manifold
    sh["level_support_proj"] = 20 + lv_all + otbt + t["lvl.projectile"]    # Target Projection
    sh["level_support_plain"] = 20 + lv_all + otbt                         # AA, Mass Effect, WFB, Deepened Curse, Restrain
    sh["level_aura_spell"] = 20 + lv_all + t["lvl.spell"]                  # Spell Amplification
    sh["level_aura_cold"] = 20 + lv_all + t["lvl.cold"]                    # Frigid Domain
    sh["level_aura_proj"] = 20 + lv_all + t["lvl.projectile"]              # Precise Projectiles
    sh["level_aura_plain"] = 20 + lv_all                                   # Domain Expansion
    sh["level_empower"] = 20 + lv_all + t["lvl.spell"]                     # Aim, SOU (Spell)
    sh["level_biting_cold"] = 20 + lv_all + t["lvl.spell"] + t["lvl.cold"]
    sh["level_speed_phantom"] = 20 + lv_all + t["lvl.spell"] + t["lvl.physical"]
    # attributes
    base = build["hero"]["base_attributes"]
    all_ = t["attr.all"]
    sh["INT"] = (base["INT"] + t["attr.int"] + all_ + t["attr.str_int"] + t["attr.dex_int"]) * (1 + (t["attr.int_pct"] + t["attr.all_pct"]) / 100)
    sh["STR"] = (base["STR"] + t["attr.str"] + all_ + t["attr.str_int"]) * (1 + t["attr.all_pct"] / 100)
    sh["DEX"] = (base["DEX"] + t["attr.dex"] + all_ + t["attr.dex_int"]) * (1 + t["attr.all_pct"] / 100)
    # damage pool as the in-game sheet shows it
    sh["damage_bonus"] = t["inc.damage"] + t["inc.spell"] + t["inc.projectile"] + (t["inc.vs_cursed"] if ctx.get("enemy_cursed", True) else 0)
    sh["cold_bonus"] = t["inc.cold"] + t["inc.elemental"]
    sh["increased_pool"] = sh["damage_bonus"] + sh["cold_bonus"] + t["inc.area"]
    # buffs that show on the sheet while hitting the dummy
    aim_lv = sh["level_empower"]
    sou_cast = skill_value("Secret_Origin_Unleash", aim_lv, r"\+?([\d.]+)% Cast Speed for every stack") * min(4 + t["focus.max"], 8)
    sh["empower_effect"] = empower_effect(sh, ctx.get("mass_effect_charges", 3))
    dis = set(ctx.get("disabled", []))
    if "Secret Origin Unleash" in dis:
        sou_cast = 0
    aim_pen = 0 if "Aim" in dis else -16
    burst = 0 if "Swift Shadow Raid" in dis else ctx.get("periodic_burst", 20)   # follower (Tartarus) Periodic Burst: +20% [Vlad]; the player support is +30% for 2 s
    cast = t["cast.inc"] + 4 * ctx["agility"] + sou_cast * sh["empower_effect"] + aim_pen + burst  # Agility, SOU, Aim -16 (flat), Periodic Burst +20
    sh["cast_speed"] = cast
    sh["proj_speed"] = t["proj.speed"] + (0 if "Swift Shadow Raid" in dis else 40) + (0 if "Precise Projectiles" in dis else
        aura_value("Precise_Projectiles", sh["level_aura_proj"], r"\+?([\d.]+)% Projectile Speed", sh))  # + SSR 40
    sh["crit_flat"] = 500 + t["crit.flat"]
    sh["crit_rating_bonus"] = t["crit.rating_inc"]
    sh["crit_chance"] = min(100.0, sh["crit_flat"] * (1 + sh["crit_rating_bonus"] / 100) / 100)
    sh["max_focus"] = 4 + t["focus.max"]
    sh["crit_damage"] = 150 + t["crit.dmg"] + t["crit.dmg_per_focus"] * sh["max_focus"]
    sh["max_focus"] = 4 + t["focus.max"]
    sh["frostbite_rating"] = min(120, 10 + t["frost.max"])
    sh["frostbite_effect"] = t["frost.effect"]
    sh["double_on_person"] = t["double.chance"]
    sh["res_pen"] = t["pen.res"]
    sh["armor_pen"] = t["pen.armor"]
    sh["duration"] = t["dur"] + (5 if build["hero"]["trait_levels"].get("Prophecy of Purity", 0) >= 3 else 0)
    sh["cdr"] = t["cdr"] + 3 * ctx["nfe_stacks"] * 1.5  # NFE +3% CDR/stack x1.5 Witch
    # God's Boon: 2 permanent stacks need duration >= 2 x cooldown (CD 15 s / (1.5 Reincarnation x (1 + CDR)))
    boon_cd = 15 / (1.5 * (1 + sh["cdr"] / 100))
    sh["boon_margin"] = 10 * (1 + sh["duration"] / 100) / (2 * boon_cd)
    sh["_totals"] = t
    sh["_recs"] = recs
    return sh


def aura_value(key, level, rx, sh, aa_level=None):
    aa = aura_amp(sh)
    return skill_value(key, level, rx) * (1 + aa / 100)


def aura_amp(sh):
    return skill_value("Aura_Amplification", sh["level_support_plain"], r"([\d.]+)% Aura effect")


def mass_effect(sh, charges=3):
    # "+X% effect for the supported skill for every +1 Charge, up to +3X%" — charges = extra max charges the skill has
    lv = sh["level_support_plain"]
    per = skill_value("Mass_Effect", lv, r"([\d.]+)% effect for the supported skill for every")
    cap = skill_value("Mass_Effect", lv, r"up to ([\d.]+)%")
    return min(cap, per * charges)


def empower_effect(sh, charges=3):
    lv = sh["level_support_plain"]
    wfb = skill_value("Well-Fought_Battle", lv, r"([\d.]+)% Effect every time") * 3
    return 1 + (wfb + mass_effect(sh, charges)) / 100


# --------------------------------------------------------------------------- DPS

def dps(build, trees, verbose=False):
    sh = sheet(build, trees)
    t = sh["_totals"]
    ctx = build["context"]
    tl = build["hero"]["trait_levels"]
    m = {}  # name -> multiplier

    base = 664.5 + 1.23 * (t["flat.cold"] + t["flat.physical"])
    base_phys = 664.5 + 1.23 * t["flat.physical"]
    def _flat_minmax(key):
        lo = hi = 0.0
        for src, k2, v, cond, line in sh["_recs"]:
            if k2 != key: continue
            mm = re.search(r"Adds\s+([\d.]+)\s*[-–]\s*([\d.]+)", line)
            a, b2 = (float(mm.group(1)), float(mm.group(2))) if mm else (v, v)
            lo += a; hi += b2
        return lo, hi
    (fp_lo, fp_hi), (fc_lo, fc_hi) = _flat_minmax("flat.physical"), _flat_minmax("flat.cold")
    base_min = 498 + 1.23 * (fp_lo + fc_lo); base_max = 831 + 1.23 * (fp_hi + fc_hi)
    if t["special.impermanence"]:
        base_min = 498 * 0.1 * 0.68 + 1.23 * (fp_lo * 0.1 * 0.68 + fc_lo * 0.68)
        base_max = 831 * 1.8 * 1.32 + 1.23 * (fp_hi * 1.8 * 1.32 + fc_hi * 1.32)
        base_phys = (498 * 0.1 * 0.68 + 831 * 1.8 * 1.32) / 2 + 1.23 * (fp_lo * 0.1 * 0.68 + fp_hi * 1.8 * 1.32) / 2
    if t["special.impermanence"]:
        rng = lambda lo, hi, phys: ((lo * (0.1 if phys else 1)) * 0.68 + (hi * (1.8 if phys else 1)) * 1.32) / 2
        fp = [r for r in sh["_recs"] if r[1] == "flat.physical"]; fc = [r for r in sh["_recs"] if r[1] == "flat.cold"]
        def flat_rng(rs, phys):
            tot = 0.0
            for src, key, v, cond, line in rs:
                mm = re.search(r"Adds\s+([\d.]+)\s*[-–]\s*([\d.]+)", line)
                lo, hi = (float(mm.group(1)), float(mm.group(2))) if mm else (v, v)
                tot += rng(lo, hi, phys)
            return tot
        base = rng(498, 831, True) + 1.23 * (flat_rng(fp, True) + flat_rng(fc, False))
    m["level"] = level_mult(sh["level_chromatic"])
    m["increased"] = 1 + sh["increased_pool"] / 100
    attr = sh["INT"] + sh["STR"] + sh["DEX"]
    lc = ctx.get("lightchaser", True)
    m["attributes (0.75%/pt w/ Lightchaser, else 0.5%)"] = 1 + (0.0075 if lc else 0.005) * attr
    # supports
    m["Spell Tangle"] = 1 + skill_value("Spell_Tangle", sh["level_support_spell"], r"([\d.]+)% additional damage") / 100
    m["Manifold"] = 1 + skill_value("Manifold_Entanglement", sh["level_support_spell"], r"([\d.]+)% additional damage") / 100
    m["Lightchaser roll [Vlad]"] = 0.84 if lc else 1.0
    m["Condensed Cold roll [Vlad]"] = 1.20
    tp = skill_value("Target_Projection", sh["level_support_proj"], r"([\d.]+)% additional damage to Marked")
    m["Target Projection vs Marked"] = 1 + tp / 100
    m["Enhanced Mark (proj taken) [measured: not applying]"] = 1.0
    # tangles
    m["Dormant Entanglement"] = 1 + 0.40 * ctx["tangles_dormant"]
    m["NFE"] = 1 + 0.07 * 1.5 * ctx["nfe_stacks"]
    m["Tangle Damage Enhancement"] = 1 + t["enh.tangle"] / 100
    # blessings and boon
    f = sh["max_focus"]   # Thea sits at max Focus while hitting (Boon refills in <1 s)
    m["Focus Blessing"] = 1 + 0.05 * f
    m["Israfel per Focus"] = 1 + t["add.cold_per_focus"] * f / 100
    m["Bunch per Focus"] = 1 + t["add.spell_per_focus"] * f / 100
    m["Agility Blessing"] = 1 + 0.02 * ctx["agility"]
    wis = {0: 0, 1: 20, 2: 28, 3: 36, 4: 44, 5: 52}[tl["Wisdom of The Gods"]]
    rein = {0: 0, 1: 4, 2: 6, 3: 8, 4: 10, 5: 11}[tl["Predicted Reincarnation"]] * 5
    stacks = ctx["boons"] if tl["Prophecy of Purity"] > 0 else 1
    m["Boon: Wisdom"] = 1 + wis * stacks / 100
    m["Boon: Reincarnation"] = 1 + rein * stacks / 100
    # additional damage lines from gear/tree/slates/pacts (each source its own multiplier)
    for src, key, v, cond, line in sh["_recs"]:
        if key in ("add.damage", "add.spell", "add.cold", "add.elemental", "add.hit", "add.projectile") or (key == "add.vs_cursed" and ctx.get("enemy_cursed", True)):
            name = f"{line[:60]} [{src}]"
            m[name] = m.get(name, 1.0) * (1 + v / 100)
    frozen = sh["frostbite_rating"] > 100
    vs_frozen = t["add.vs_frozen"] if frozen else 0
    m["vs Frozen (on-person, added)"] = 1 + vs_frozen / 100
    # auras and empowers
    # Auras come from build.skills.others ("Name [supports]"); "Precise: Name" uses the Precise table; Stand as One in the
    # supports adds its per-aura effect x auras affecting you (max 5). Weapon Amp only hits the phys-origin part of the hit.
    others = build.get("skills", {}).get("others", [])
    aura_defs = [("Spell Amplification", "Spell_Amplification", sh["level_aura_spell"], r"([\d.]+)% additional Spell Damage"),
                 ("Frigid Domain", "Frigid_Domain", sh["level_aura_cold"], r"\+?([\d.]+)% additional Cold Damage"),
                 ("Precise Projectiles", "Precise_Projectiles", sh["level_aura_proj"], r"\+?([\d.]+)% additional Projectile Damage"),
                 ("Domain Expansion", "Domain_Expansion", sh["level_aura_plain"], r"\+?([\d.]+)% additional Area Damage"),
                 ("Weapon Amplification", "Weapon_Amplification", 20 + t["lvl.all"] + t["lvl.physical"], r"\+?([\d.]+)% additional Physical Damage")]
    present = []
    for name, key, lv, rx in aura_defs:
        for x in others:
            head = x.split(" [")[0].strip()
            if head in (name, "Precise: " + name):
                present.append((name, ("Precise_" + key) if head.startswith("Precise: ") else key, lv, rx, x))
        for g in build.get("granted_auras", []):   # e.g. Lone Walker's Boots: "You have a Lv. 20 Precise Spell Amplification" (no supports)
            if g["name"] == name:
                present.append((name, ("Precise_" + key) if g.get("precise") else key, g["level"], rx, "granted"))
    other_auras = [x for x in others if x.split(" [")[0].strip().startswith(("Precise: Energy Fortress", "Energy Fortress"))]
    n_auras = min(5, len(present) + len(other_auras))
    sao = skill_value("Precise_Stand_as_One", sh["level_support_plain"], r"([\d.]+)% Aura Effect for each Aura")
    phys_share = base_phys / base
    for name, key, lv, rx, raw in present:
        eff = (1 + (aura_amp(sh) / 100 if "Aura Amplification" in raw else 0) + t["aura.effect"] / 100
               + (sao * n_auras / 100 if "Stand as One" in raw else 0))
        v = skill_value(key, lv, rx) * eff / 100
        if name == "Weapon Amplification":
            m[name] = phys_share * (1 + v) + (1 - phys_share)
        else:
            m[name] = 1 + v
    ee = sh["empower_effect"]
    m["Aim"] = 1 + skill_value("Aim", sh["level_empower"], r"([\d.]+)% additional damage for Projectile") * ee / 100
    m["Secret Origin Unleash"] = 1 + skill_value("Secret_Origin_Unleash", sh["level_empower"], r"([\d.]+)% additional Spell Damage") * ee / 100
    # Euphoria: 8 stacks in the best 1 s window; Mass Effect on Speed Phantom scales it (+3 charges: ME, Fallen Starlight, Lich -> full 'up to')
    sp_me = any(x.startswith("Speed Phantom") and "Mass Effect" in x for x in build.get("skills", {}).get("others", []))
    sp_eff = 1 + (mass_effect(sh, ctx.get("mass_effect_charges", 3)) / 100 if sp_me else 0)
    m["Speed Phantom Euphoria"] = 1 + skill_value("Speed_Phantom", sh["level_speed_phantom"], r"([\d.]+)% additional Spell Damage, up to") * 8 * sp_eff / 100
    m["Spell Aggression"] = 1.07 if ctx["spell_aggression"] else 1.0
    if t.get("special.judgment_slate_bonus"):
        m["Judgment Offspring (+3% per slate on the line)"] = 1 + t["special.judgment_slate_bonus"] * ctx.get("slates_on_line", 0) / 100
    m["Cage (1.14^4)"] = 1.14 ** 4
    ls = ctx.get("follower_lightning_storm", True)
    ailments = 1 + (1 if frozen else 0) + 1 + (2 if ls else 0) + 1   # frostbite, freeze, ignite, numbed+wilt, trauma
    has_dt = t["special.dirty_tricks"] > 0 or any(pa.get("core") == "Dirty Tricks" for pa in trees["panels"])
    if has_dt:
        m[f"Dirty Tricks ({ailments} ailments)"] = 1.12 ** ailments
    if t["inc.hit_per_ailment"]:   # Warlock "+15% Hit Damage for every type of Ailment" -> increased pool
        m["increased"] *= (1 + (sh["increased_pool"] + t["inc.hit_per_ailment"] * ailments) / 100) / (1 + sh["increased_pool"] / 100)
    if t["add.physical"]:          # e.g. Blunt: additional physical only on the phys-origin part of the hit
        ps = base_phys / base
        m["additional Physical (phys-origin share)"] = ps * (1 + t["add.physical"] / 100) + (1 - ps)
    m["Gale"] = 1 + t["special.gale"] / 100 * sh["proj_speed"] / 100   # belt base affix; 0 without it
    # enemy side
    e = {}
    e["Frostbite"] = 1 + sh["frostbite_rating"] * (1 + sh["frostbite_effect"] / 100) / 100
    e["Biting Cold"] = 1 + skill_value("Biting_Cold", sh["level_biting_cold"], r"\+?([\d.]+)% additional Cold Damage taken") * (1 + t["curse.effect"] / 100) / 100
    e["Deepened Curse"] = 1 + skill_value("Deepened_Curse", sh["level_support_plain"], r"([\d.]+)% additional damage") / 100
    # Weakness Infiltration on Speed Phantom: +30% Infiltration Effect taken for 4 s when it deals damage
    sp_wi = any(x.startswith("Speed Phantom") and "Weakness Infiltration" in x for x in build.get("skills", {}).get("others", []))
    e["Cold Infiltration (Tartarus)"] = 1 + 0.13 * (1.3 if sp_wi and "Speed Phantom" not in ctx.get("disabled", []) else 1.0)
    e["Paralysis"] = 1.15 if ls else 1.0
    e["Frail"] = 1.15 if t.get("enemy.frail") else 1.0
    e["Resistance"] = 1 - max(0.0, 30 - sh["res_pen"]) / 100
    e["Armor (50% x 60% - pen)"] = 1 - max(0.0, 0.5 * 0.6 - sh["armor_pen"] / 100)
    # One fitted constant for the dummy: ratio tests are within ~5%, the absolute T scale was 26-35% high (2026-10-27).
    # Most likely the dummy's real res/armor; keep it separate so pen/arp pricing can be re-checked against it.
    e["Dummy calibration (fitted, see mechanics.md)"] = ctx.get("dummy_scale", 1.0)
    for name in ctx.get("disabled", []):
        for d in (m, e):
            for k in list(d):
                if k.startswith(name):
                    d[k] = 1.0
    # crit, double, projectiles, casts
    p = sh["crit_chance"] / 100
    oncrit = 1 + t["add.on_crit"] / 100
    crit = (1 - p) + p * sh["crit_damage"] / 100 * oncrit
    dbl_c = sh["double_on_person"] + (20 if ctx["in_tidewell"] else 0) + (6 * 8 * stacks if tl["Farewell Prophecy"] >= 3 else 0)
    dbl = 1 + dbl_c / 100 if dbl_c <= 100 else 2 * (1 + min(1.0, dbl_c / 100 - 1))
    proj = 1 + 0.8 + 0.8 ** 2
    casts = (1.54 * (1 + sh["cast_speed"] / 100) * (1.07 if ctx["spell_aggression"] else 1) * (1.08 if ctx["hasten"] else 1)
             * (1 + t["cast.add"] / 100))
    ripple = 1.5 if any(pa.get("core") == "Spell Ripple" for pa in trees["panels"]) else 1.0
    hit = base * math.prod(m.values()) * math.prod(e.values())
    cap = ctx.get("hit_cap", 5e12)
    real = hit / ctx.get("dummy_scale", 1.0)          # per-hit damage before crit/double, without the hit-rate constant
    a_u, b_u = base_min / base, base_max / base         # damage roll range relative to the average
    def e_min(K):                                       # E[min(cap, K*u)], u ~ U[a_u, b_u]
        if K * b_u <= cap: return K
        if K * a_u >= cap: return cap
        tt = cap / K
        return (K * (tt * tt - a_u * a_u) / 2 + cap * (b_u - tt)) / (b_u - a_u)
    cd = sh["crit_damage"] / 100 * oncrit
    q = min(1.0, max(0.0, dbl_c / 100 - 1)) if dbl_c > 100 else 0.0
    dbl_states = [(4, q), (2, 1 - q)] if dbl_c > 100 else [(2, dbl_c / 100), (1, 1 - dbl_c / 100)]
    capped = uncapped = 0.0
    for w in (1.0, 0.8, 0.64):                          # shotgun falloff: each projectile is its own hit
        for cm, pc in ((cd, p), (1.0, 1 - p)):
            for dm, pd in dbl_states:
                K = real * w * cm * dm
                capped += pc * pd * e_min(K); uncapped += pc * pd * K
    cap_factor = capped / uncapped if uncapped else 1.0
    per_cast = hit * crit * dbl * proj * ripple * cap_factor
    total = per_cast * casts * ctx["tangles_active"]
    out = {"sheet": sh, "mult": m, "enemy": e, "base": base, "crit": crit, "double_chance": dbl_c, "double": dbl,
           "proj": proj, "casts_per_tangle": casts, "ripple": ripple, "hit": hit, "dps": total, "cap_factor": cap_factor,
           "max_hit": real * cd * (4 if dbl_c > 100 else 2) * b_u}
    return out


# --------------------------------------------------------------------------- variants

def load():
    b = json.loads((CHAR / "build.json").read_text(encoding="utf-8"))
    t = json.loads((CHAR / "trees.json").read_text(encoding="utf-8"))
    return b, t


def apply(build, trees, change):
    """change: {"remove": ["gear:belt", ...], "add_lines": [[slot, line], ...], "remove_lines": [[slot, line]],
                "context": {...}, "trait_levels": {...}}"""
    b, t = copy.deepcopy(build), copy.deepcopy(trees)
    for r in change.get("remove", []):
        kind, _, name = r.partition(":")
        if kind == "gear":
            b["gear"] = [g for g in b["gear"] if g["slot"] != name]
        elif kind == "slates":
            b["slates"] = [s for s in b["slates"] if s["name"] != name]
        elif kind == "pact":
            b["pacts"] = [p for p in b["pacts"] if p["name"] != name]
        elif kind == "memory":
            b["memories"] = [m for m in b["memories"] if str(m["slot"]) != name]
    for slot, lines in change.get("add_items", []):
        b["gear"].append({"slot": slot, "name": "candidate", "lines": list(lines)})
    if change.get("replace_kismet"):
        ref, lines = change["replace_kismet"]
        ks = b["kismets"]["lines"]
        if ref in ks:
            ks.remove(ref)
        ks.extend(lines)
    if change.get("add_slate"):
        lines, eff = change["add_slate"]
        b["slates"].append({"name": "candidate", "effect_pct": eff, "lines": list(lines)})
    for slot, lines in change.get("set_memory", {}).items():
        m = next(x for x in b["memories"] if str(x["slot"]) == str(slot))
        m["lines"] = list(lines)
    if change.get("add_memory_line"):
        b["memories"].append({"slot": "candidate", "name": "candidate", "lines": [change["add_memory_line"]]})
    if change.get("remove_memory_line"):
        slot, line = change["remove_memory_line"]
        m = next(x for x in b["memories"] if str(x["slot"]) == slot)
        m["lines"].remove(line)
    if change.get("tree_remove"):
        panel, nid = change["tree_remove"]
        pa = next(x for x in t["panels"] if x["panel"] == panel)
        pa["nodes"].pop(nid, None)
    for sname, line in change.get("remove_slate_lines", []):
        sl = next(x for x in b["slates"] if x["name"] == sname)
        sl["lines"].remove(line)
    if change.get("stat_delta"):
        b["gear"].append({"slot": "_delta", "name": "test delta", "lines": [],
                          "effects": [{"key": k, "value": v, "why": "test delta"} for k, v in change["stat_delta"].items()]})
    if change.get("disable"):
        b["context"]["disabled"] = sorted(set(b["context"].get("disabled", [])) | set(change["disable"]))
    for slot, line in change.get("add_lines", []):
        g = next(x for x in b["gear"] if x["slot"] == slot)
        g["lines"].append(line)
    for slot, line in change.get("remove_lines", []):
        g = next(x for x in b["gear"] if x["slot"] == slot)
        g["lines"].remove(line)
    b["context"].update(change.get("context", {}))
    b["hero"]["trait_levels"].update(change.get("trait_levels", {}))
    return b, t


def fmt_T(x):
    return f"{x / 1e12:.2f} T"


def report(res, ingame=None):
    sh = res["sheet"]
    print("## Sheet (computed)" + ("  vs in-game" if ingame else ""))
    keys = ["damage_bonus", "cold_bonus", "cast_speed", "proj_speed", "crit_rating_bonus", "crit_chance", "crit_damage",
            "INT", "STR", "DEX", "max_focus", "frostbite_rating", "frostbite_effect", "duration", "cdr",
            "double_on_person", "res_pen", "armor_pen", "level_chromatic"]
    for k in keys:
        v = sh[k]
        g = (ingame or {}).get(k)
        d = f"   in-game {g:g}  (Δ {v - g:+.1f})" if g is not None else ""
        print(f"  {k:22s} {v:8.1f}{d}")
    print("\n## Multipliers")
    for k, v in sorted(res["mult"].items(), key=lambda kv: -kv[1]):
        print(f"  x{v:7.3f}  {k}")
    print("  enemy side:")
    for k, v in res["enemy"].items():
        print(f"  x{v:7.3f}  {k}")
    print(f"\n  base {res['base']:.1f} | crit factor {res['crit']:.3f} | double {res['double_chance']:.0f}% -> x{res['double']:.2f}"
          f" | projectiles x{res['proj']:.2f} | casts/s/tangle {res['casts_per_tangle']:.2f} | ripple x{res['ripple']}")
    print(f"\n  DPS {fmt_T(res['dps'])}")


INGAME = {  # Vlad's sheet 2026-10-26 13:47
    "damage_bonus": 544, "cold_bonus": 142, "cast_speed": 262, "crit_rating_bonus": 785, "crit_chance": 71.67,
    "crit_damage": 515, "proj_speed": 213, "INT": 543, "STR": 152, "DEX": 45, "duration": 59, "cdr": 30, "max_focus": 10,
}


def run_tests(build, trees):
    tests = json.loads((CHAR / "tests.json").read_text(encoding="utf-8"))
    print(f"current build model: {fmt_T(dps(build, trees)['dps'])} with belt")
    groups = defaultdict(list)
    for tc in tests["tests"]:
        if tc.get("skip"):
            continue
        if tc.get("common"):   # era state applied under both before and after (e.g. pre-revival Memory of Origin)
            build_e, trees_e = apply(build, trees, tc["common"])
        else:
            build_e, trees_e = build, trees
        b1, t1 = apply(build_e, trees_e, tc.get("after", {}))
        if "measured" in tc:   # absolute pull on the current build (T), e.g. belt off + ring off under the 10 T display cap
            pred, meas = dps(b1, t1)["dps"] / 1e12, tc["measured"]
        else:
            b0, t0 = apply(build_e, trees_e, tc.get("before", {}))
            pred = dps(b1, t1)["dps"] / dps(b0, t0)["dps"]
            meas = tc["measured_after"] / tc["measured_before"]
        err = pred / meas - 1
        groups[tc.get("group", "current")].append((tc["name"], meas, pred, err))
    for g, rows in groups.items():
        print(f"\n## {g}")
        for name, meas, pred, err in rows:
            flag = "  <-- off" if abs(err) > 0.10 else ""
            unit = " T" if g == "absolute" else ""
            print(f"  {name[:62]:62s} measured {'' if unit else 'x'}{meas:5.3f}{unit}  model {'' if unit else 'x'}{pred:5.3f}{unit}  ({err:+.0%}){flag}")
        rms = math.sqrt(sum(r[3] ** 2 for r in rows) / len(rows))
        print(f"  -> {len(rows)} tests, rms error {rms:.1%}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--belt-off", action="store_true")
    ap.add_argument("--remove", action="append", default=[])
    ap.add_argument("--add-line", nargs=2, action="append", default=[], metavar=("SLOT", "LINE"))
    ap.add_argument("--test", action="store_true")
    a = ap.parse_args(argv)
    b, t = load()
    if a.test:
        run_tests(b, t)
        return
    ch = {"remove": a.remove + (["gear:belt"] if a.belt_off else []), "add_lines": a.add_line}
    b, t = apply(b, t, ch)
    res = dps(b, t)
    report(res, INGAME)


if __name__ == "__main__":
    main()
