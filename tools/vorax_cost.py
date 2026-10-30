#!/usr/bin/env python3
"""Expected FE cost of a Vorax chest with a Core Organ (Vlad's crafting rules, 2026-10-30 18:10).

Rules [Vlad]: 3 prefix + 3 suffix slots; at most 2 Advanced + 2 Ultimate + 2 Legendary affixes per item. A craft of a type lands on a
random slot of that side among the slots that keep the item legal — a Legendary affix CAN be overwritten by a normal craft, which is why
the layout must be B A U | B A U before the organ: then an A craft can only land on the A and a U craft only on the U (anything else
would be a 3rd A / 3rd U). A Core Organ offers 2 of the legendary's affixes (1 if it only has 2); the chosen line lands on a random one
of the 6 slots (the 2nd organ can't hit the 1st L). Landing on a B = done. Landing on an A or U: the side is L B U or L B A; the item
is not lost, the chest is reset to B A U B A U with junk organs and the next organ is tried (Vlad), OR, before resetting, a junk craft
of the missing type on that side: 1/3 lands on the B (done), 1/3 overwrites the L (organ lost), 1/3 flips L B U <-> L B A (try again)
-> the organ is saved half the time ("walk"). The 2nd organ landing on the 1st L's side (L A L / L L U) can't be walked: whichever L
the junk craft overwrites, one organ is lost and the other L sits in a valid side. Wrong landings never cost the chest.
Usage: python3 tools/vorax_cost.py
"""
CHEST = 4000.0            # Vorax chest with the +20% Block Ratio base [Vlad]
SUTURE = 424.0            # Exquisite Suture, etor 2026-10-30
RAINBOW = 400.0           # uncorroded Double Rainbow [Vlad] (list: 260 corroded)
CAGE = 3000.0             # uncorroded Iced Drinker's Cage [Vlad] (list 3,160)
JUNK = 2 * 0.54 + 2 * 1.57 + 2 * 13.0   # B A U B A U with Rotten Fine / Rotten Matchless / the cheapest specials: ~30 FE per reset

MODS = {"aura 20% (Flawless Nerve: Entwined)": 575, "cold/pen at 8 Focus (Flawless Tongue: Apathetic)": 18, "+2 Active (Nerve: Compelling)": 202,
        "sealed comp prefix (Nerve: Unsealed)": 370, "proj speed: 1 of 5 adv prefixes x Vital Organ Matchless 62.5": 5 * 62.5,
        "10% ele res: 1 of 10 adv suffixes x 62.5": 10 * 62.5, "basic (ES 2/10 or crit 1/8) x Vital Fine 22": 6 * 22}


def comb(n, k):
    from math import comb as c
    return c(n, k)


def p_offered(pool, wanted):
    """P(at least one wanted affix among the 2 offered out of `pool`)."""
    return 1 - comb(pool - wanted, 2) / comb(pool, 2)


def one_line(attempt, p_off, p_land, p_walkable, walk):
    """Expected cost to place one legendary line; a miss costs the organ + a reset (JUNK), never the chest.
    p_land: lands on a free B; p_walkable: lands on an A/U of a side with no other L (junk-craft walk saves it 1/2 of the time);
    the rest (2nd organ landing on the 1st L's side) always costs one organ and leaves one good L in a valid side."""
    p_ok = p_off * (p_land + (p_walkable * 0.5 if walk else 0.0))
    return (attempt + p_off * (1 - p_land) * JUNK) / p_ok


def rainbow(walk):
    return CHEST + JUNK + one_line(RAINBOW + SUTURE, p_offered(4, 1), 2 / 6, 4 / 6, walk)


def cage(walk, lines=2):
    attempt = CAGE + SUTURE
    if lines == 1:
        return CHEST + JUNK + one_line(attempt, p_offered(5, 1), 2 / 6, 4 / 6, walk)
    e1 = one_line(attempt, p_offered(5, 2), 2 / 6, 4 / 6, walk)   # either wanted line (Cage stacks / Extreme Coldness)
    e2 = one_line(attempt, p_offered(4, 1), 1 / 5, 2 / 5, walk)   # the other line: 1/5 the free B, 2/5 the other side's A/U (walk),
                                                               # 2/5 the first L's side -> one organ lost, one good L remains (sides matter: each side ends L A U)
    return CHEST + JUNK + e1 + e2


if __name__ == "__main__":
    mods = sum(MODS.values()) - MODS["+2 Active (Nerve: Compelling)"] - MODS["sealed comp prefix (Nerve: Unsealed)"]   # one ult prefix: cold/pen
    print(f"mods after the organ (aura, cold/pen, proj speed, 10% res, one basic): ~{mods:,.0f} FE")
    for k, v in MODS.items(): print(f"   {k}: {v:.0f}")
    for walk in (False, True):
        print(f"\n== {'reset after a wrong landing (Vlad)' if not walk else 'junk craft on the L side first: saves the organ 1/2 of the time'}")
        print(f"  Rainbow (+19% line):                 {rainbow(walk):9,.0f} FE  (+ mods {mods:,.0f})")
        print(f"  Cage, Cage-stacks line only:          {cage(walk, 1):9,.0f} FE")
        print(f"  Cage, stacks + Extreme Coldness:      {cage(walk, 2):9,.0f} FE")
