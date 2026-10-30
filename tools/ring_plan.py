#!/usr/bin/env python3
"""Vlad's Vorax ring L (2026-10-30 22:52) on top of the Sacrificer's Necklace + Ice Bond world, and what the 5 T hit cap does there.

Ring L = Vorax Limb: Digits, layout L A U | L A U, base "+1 to Max Focus Blessing Stacks":
  L  Have Fervor                                   (Organ: Dawn Break — Graft: Boots/Ring/Belt; Tenacious Suture x5)
  L  +1% additional damage per (2-3) Fervor Rating  (same organ; 100 rating -> +50% / +33%)
  A  +(16-20)% Attack and Spell Block Chance        (Vital Organ (Matchless), random adv prefix)
  U  +(18-22)% Armor DMG Mitigation Penetration     (Flawless Spine: Impalement)
  A  +(61-78)% Critical Strike Damage               (Vital Organ (Matchless), random adv suffix)
  U  +(27-34)% Cooldown Recovery Speed              (Flawless Ears: Echoing) -> the belt keeps Hasten, I Am Truth's duration is not needed
The current rare ring L (+68% damage, +114% crit rating, 15% block, 20% light / 25% ero res, 323 ES) goes.
Belt: 18% double -> +30% Skill Effect Duration (ult suffix), Hasten stays. Both sides: one wand at T0 double.
Usage: python3 tools/ring_plan.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine
from neck_plan import plan, base, NECK

IB = "Ice Bond [Well-Fought Battle, Mass Effect, Preparation, Increased Area]"
RING = ["+200% Critical Strike Rating", "+50% additional damage", "+18% Attack and Spell Block Chance", "+20% Armor DMG Mitigation Penetration",
        "+70% Critical Strike Damage", "+30% Cooldown Recovery Speed", "+1 to Max Focus Blessing Stacks"]


def neck_world(hasten_kept=True):
    """Sacrificer's neck (tangle / 18% aura / 70% crit dmg / 70 INT counted), Ice Bond in the freed active slot, belt double -> duration."""
    ch = plan(NECK + ["+70 Intelligence"], timid=False, belt=True)
    ch["replace_skill"] = [["Biting Cold", IB]]
    if hasten_kept:
        ch["context"]["hasten"] = True
        ch["add_lines"] = [l for l in ch["add_lines"] if l[1] != "+25% Cooldown Recovery Speed"]
    return ch


def ring_world(ring=RING, **kw):
    ch = neck_world(**kw)
    ch["remove"].append("gear:ring_l")
    ch["add_items"].append(["ring_l", list(ring)])
    return ch


def main():
    b, t = engine.load()
    R = lambda ch: engine.dps(*engine.apply(b, t, ch))
    A, N, W = R(base()), R(neck_world()), R(ring_world())
    row = lambda name, r: print(f"  {name:52s} {r['dps'] / 1e12:6.1f} T  cap {r['cap_factor']:.3f}  max hit {r['max_hit'] / 1e12:4.1f} T  crit {r['sheet']['crit_chance']:3.0f}%  Boon {r['sheet']['boon_margin']:.2f}")
    print("## worlds (both with one wand at T0 double)")
    row("today", A); row("neck world (Hasten kept, no ring CDR: Boon < 1)", N); row("+ Vorax ring L", W)
    print(f"  ring vs the current ring L: x{W['dps'] / N['dps']:.3f}   whole package vs today: x{W['dps'] / A['dps']:.3f}   (uncapped x{(W['dps'] / W['cap_factor']) / A['dps']:.2f})")
    print("\n## the ring line by line (order matters under the cap; each line = ring without it)")
    for line in RING:
        r = R(ring_world([l for l in RING if l != line]))
        print(f"  x{W['dps'] / r['dps']:.3f}  {line}")
    r = R(ring_world([l if l != "+50% additional damage" else "+33% additional damage" for l in RING]))
    print(f"  per-3 roll of the Dawn Break line instead of per-2: x{r['dps'] / W['dps']:.3f}")
    print("\n## in the ring world, what the 5 T hit cap leaves of the next projects")
    def show(name, ch, tree=None):
        b2, t2 = engine.apply(b, t, ch)
        if tree:
            tree(t2)
        r = engine.dps(b2, t2)
        unc = (r["dps"] / r["cap_factor"]) / (W["dps"] / W["cap_factor"])
        print(f"  x{r['dps'] / W['dps']:.3f}  {name:66s} ({r['dps'] / 1e12:.0f} T, cap {r['cap_factor']:.2f}; uncapped x{unc:.2f})")
    ch = ring_world(); ch["stat_delta"] = {"aura.effect": 63}; show("Phantasmagoria 18 aura ranks (+63% aura), Ripple kept", ch)
    def kill_ripple(t2):
        for pa in t2["panels"]:
            if pa.get("core") == "Spell Ripple": pa["core"] = "Extreme Coldness"
    ch = ring_world(); ch["stat_delta"] = {"aura.effect": 63}; show("the planned swap: aura prism in the Spell Ripple core's place", ch, kill_ripple)
    ch = ring_world(); ch["stat_delta"] = {"cast.inc": 63}; show("18 micro ranks of cast speed (+63%) instead", ch)
    sup = b["skills"]["main"]["supports"]
    for victim in ("Target Projection", "Overload", "Chromatic Shot: Condensed Cold"):
        ch = ring_world(); ch["main_supports"] = [("Multiple Projectiles" if s.startswith(victim) else s) for s in sup]
        show(f"Multiple Projectiles instead of {victim}", ch)
    ch = ring_world(); ch["context"].update({"tangles_active": 4, "tangles_dormant": 0}); show("a 4th attached tangle (no source on gear yet)", ch)
    ch = ring_world(); ch["add_lines"] = [l for l in ch["add_lines"] if "Double" not in l[1]]; show("the wand's T0 double dropped", ch)


if __name__ == "__main__":
    main()
