#!/usr/bin/env python3
"""Vorax ring L (Vorax Limb: Digits) and the 5 T hit cap [Vlad 2026-10-30 23:00; priced 23:40].

Vlad's ring: L A U | L A U, base "+1 to Max Focus Blessing Stacks"; L "Have Fervor" + L "+1% additional damage per (2-3) Fervor Rating" (two Dawn Break
organs: Graft Boots/Ring/Belt, 5 Tenacious Sutures per graft); A +16-20% block, U ARP 18-22 | A crit dmg 61-78, U CDR 27-34 (belt keeps Hasten).
Fervor Rating: +1 per hit on an Elite (rares and bosses) while Fervor is active, max 100, no base decay -> 100 on a boss = +200% crit rating, +50% (2)/+33% (3).

The finding: a single hit caps at 5 T [Vlad]. With this ring the top hits model at ~15 T (cap factor ~0.5), so per-hit lines (ARP, crit dmg, Focus, levels,
Dawn Break's +50%, aura, Cage, Frozen Lotus, double damage) stop paying, and what pays is hits per second: Hasten, cast speed, Spell Aggression, attached
tangles, Spell Ripple (its Pulse is a separate hit: "True Damage equal to 150% of Hit Damage", its own cap).
Two worlds (everything else as planned: Sacrificer's neck INT / +1 attachable Tangle / 2nd ult / crit dmg, Ice Bond [WFB, ME] in Biting Cold's slot,
3 tangles on / 1 off, one wand T0 Double, belt Hasten + its dead 18% Double -> +28% Skill Effect Duration):
  cage  Iced Drinker's Cage chest + Spell Ripple prism (core = Ripple)
  robe  Long Night Sorcerer's Robe (T0 proj speed 53 / T0 INT 70 / T0 crit rating 140 / T1 aura 18 / base ARP 6) + Phantasmagoria (+63% aura) with
        Extreme Coldness in the freed Prophet core
God's Boon: the 2nd stack's uptime is taken as clamp(2 x margin - 1) (recast on cooldown; assumption), DPS time-weighted between 2 and 1 stacks.
Usage: python3 tools/ring_plan.py
"""
import sys, os, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine

IB = "Ice Bond [Well-Fought Battle, Mass Effect, Preparation, Increased Area]"
ROBE = ["+170 gear Energy Shield", "+460 gear Energy Shield", "+53% Projectile Speed", "+70 Intelligence",
        "+140% Critical Strike Rating", "+18% Aura Effect", "+6% Armor DMG Mitigation Penetration"]
NECK_BASE = ["+70 Intelligence", "You can apply 1 additional Tangle(s) to enemies", "+8% Tangle Damage Enhancement", "+70% Critical Strike Damage"]
NECK_U2 = {"aura": ["+18% Aura Effect"], "active": ["+2 Active Skill Level"], "fervor": ["+200% Critical Strike Rating"], "none": []}
FERVOR = "+200% Critical Strike Rating"          # Have Fervor at 100 Fervor Rating: +2% crit rating per point
BLOCK, ARP, CRITD, CDR = ("+18% Attack and Spell Block Chance", "+20% Armor DMG Mitigation Penetration",
                          "+70% Critical Strike Damage", "+30% Cooldown Recovery Speed")
RINGS = {   # None = the current rare ring L (Perishing Inferno Flame Ring: block 15, ES, 68% dmg | 20 light, 25 ero, 114% crit rating)
    "current rare ring L": None,
    "Vlad: Focus base | 2 Dawn Break L": ["+1 to Max Focus Blessing Stacks", FERVOR, "+50% additional damage", BLOCK, ARP, CRITD, CDR],
    "Fervor base | 1 Dawn Break L, B res": [FERVOR, "+50% additional damage", BLOCK, ARP, CRITD, CDR, "+30% Lightning Resistance"],
    "Fervor base | no organ, B ES + B res": [FERVOR, "+400 Max Energy Shield", BLOCK, ARP, CRITD, CDR, "+30% Lightning Resistance"],
}
B, T = engine.load()


def change(ring_lines=None, neck_u2="active", world="robe", belt_hasten=True, belt_dur=True, extra_lines=(), delta=None):
    rm = ["gear:neck"] + (["gear:chest"] if world == "robe" else []) + (["gear:ring_l"] if ring_lines is not None else [])
    items = [["neck", NECK_BASE + NECK_U2[neck_u2]]] + ([["chest", ROBE]] if world == "robe" else []) \
            + ([["ring_l", list(ring_lines)]] if ring_lines is not None else [])
    ch = {"remove": rm, "add_items": items,
          "add_lines": [["weapon_m", "+34% chance to deal Double Damage"]] + ([["belt", "+28% Skill Effect Duration"]] if belt_dur else []) + list(extra_lines),
          "remove_lines": [["belt", "+18% chance to deal Double Damage"]] if belt_dur else [],
          "replace_skill": [["Biting Cold", IB]],
          "context": {"tangles_active": 3, "tangles_dormant": 1, "biting_cold_level": 20, "hasten": belt_hasten}}
    sd = dict(delta or {})
    if world == "robe":
        sd["aura.effect"] = sd.get("aura.effect", 0) + 63
    if sd:
        ch["stat_delta"] = sd
    return ch


def run(ch, world="robe"):
    b2, t2 = engine.apply(B, T, ch)
    for pa in t2["panels"]:
        if pa["panel"] == "Prophet":
            pa["core"] = "Extreme Coldness" if world == "robe" else "Spell Ripple"
    return engine.dps(b2, t2)


def run_mix(ch, world="robe"):
    """(dps, result) with the 2nd Boon stack time-weighted: uptime clamp(2 x margin - 1)."""
    r2 = run(ch, world); f = max(0.0, min(1.0, 2 * r2["sheet"]["boon_margin"] - 1))
    if f >= 1.0:
        return r2["dps"], r2
    c1 = copy.deepcopy(ch); c1["context"]["boons"] = 1
    return f * r2["dps"] + (1 - f) * run(c1, world)["dps"], r2


def line(label, d, r, ref=None):
    rel = f"x{d / ref:.3f}  " if ref else ""
    s = r["sheet"]
    print(f"  {rel}{d / 1e12:6.1f} T  max hit {r['max_hit'] / 1e12:4.1f} T  cap {r['cap_factor']:.2f}  crit {s['crit_chance']:3.0f}%  margin {s['boon_margin']:.2f}  {label}")


if __name__ == "__main__":
    print(f"today (model) {engine.fmt_T(engine.dps(B, T)['dps'])}, max hit {engine.dps(B, T)['max_hit'] / 1e12:.1f} T; hit cap 5 T")
    for world in ("cage", "robe"):
        print(f"\n== ring L options, world '{world}'")
        ref = None
        for name, rl in RINGS.items():
            d, r = run_mix(change(rl, neck_u2="fervor" if rl is None else "active", world=world), world)
            ref = ref or d
            line(name, d, r, ref)
    print("\n== robe+Phantasmagoria swap, per ring (robe / cage)")
    for name, rl in RINGS.items():
        nk = "fervor" if rl is None else "active"
        a = run_mix(change(rl, neck_u2=nk, world="cage"), "cage")[0]; e = run_mix(change(rl, neck_u2=nk, world="robe"), "robe")[0]
        print(f"  x{e / a:.3f}  {name}")
    for world in ("cage", "robe"):
        V = RINGS["Vlad: Focus base | 2 Dawn Break L"] if world == "cage" else RINGS["Fervor base | no organ, B ES + B res"]
        d0, r0 = run_mix(change(V, world=world), world)
        print(f"\n== single choices, world '{world}' on '{'Vlad ring' if world == 'cage' else 'no-organ ring'}' ({d0 / 1e12:.1f} T)")
        res = [l for l in V if l != CDR]
        d, r = run_mix(change(res, world=world, extra_lines=[["ring_l", "+15% Elemental Resistance"], ["ring_l", "+15% Erosion Resistance"]]), world)
        line("ring ult suffix +15% ele / +15% erosion res instead of CDR", d, r, d0)
        d, r = run_mix(change(V, world=world, belt_dur=False), world); line("belt keeps its 18% Double (no duration line)", d, r, d0)
        neck = change(V, world=world); neck["add_items"][0][1] = [l for l in neck["add_items"][0][1] if "Intelligence" not in l]
        neck["stat_delta"] = dict(neck.get("stat_delta", {}), **{"add.spell": 3.27, "cast.add": 3.27})
        d, r = run_mix(neck, world); line("Trauma: ring R base SA -> Immune to Trauma, neck INT -> SA line (+50% SA effect)", d, r, d0)
        for u in ("aura", "none"):
            d, r = run_mix(change(V, neck_u2=u, world=world), world); line(f"neck 2nd ult: {u} instead of +2 Active", d, r, d0)
        ch = change(V, world=world); ch["add_lines"] = [x for x in ch["add_lines"] if "Double" not in x[1]]
        d, r = run_mix(ch, world); line("wand T0 Double Damage not crafted", d, r, d0)
        ch = change(V, world=world); ch["context"].update({"tangles_active": 4, "tangles_dormant": 0})
        d, r = run_mix(ch, world); line("4th tangle attached (4 on / 0 off)", d, r, d0)
