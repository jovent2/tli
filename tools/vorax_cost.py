#!/usr/bin/env python3
"""Expected FE cost of a Vorax chest with a Core Organ (Vlad's crafting rules, 2026-10-30).

Rules [Vlad]: a Vorax piece has 3 prefix + 3 suffix slots, at most 2 Advanced + 2 Ultimate + 2 Legendary affixes. A craft of a type lands on a
random slot of that side but never makes the item illegal (so with 2 U already, an Ultimate craft overwrites the U). A Core Organ offers
2 of the legendary's affixes (1 if it has only 2) and the chosen one lands on a random slot of the 6; if it lands on an Advanced or Ultimate
slot the item is scrap. One uncorroded legendary disenchants into one organ; one Exquisite Suture per graft.

Two regimes:
  filled   = Vlad's: craft B A U B A U first, then the organ -> lands on a B with 2/6 (1st) and 1/5 (2nd, can't hit the L); wrong = new chest.
  basics   = fill all six slots with Rotten Organ (Fine) basics first (0.5 FE each) -> every slot is a B, the organ can only land on a B;
             the Advanced/Ultimate affixes are crafted afterwards (junk specials to fix the slot layout, then the real ones on top).
Usage: python3 tools/vorax_cost.py
"""
CHEST = 4000.0            # Vorax chest with the +20% Block Ratio base [Vlad]
SUTURE = 424.0            # Exquisite Suture, etor 2026-10-30
RAINBOW = 400.0           # uncorroded Double Rainbow [Vlad]; list 260 for a corroded one
CAGE = 3000.0             # uncorroded Iced Drinker's Cage [Vlad]; list 3,160
JUNK = 2 * 0.54 + 2 * 1.57 + 2 * 13.0   # Rotten Fine x2 (basics), Rotten Matchless x2 (advanced), 2 cheapest specials (ultimates)
BASICS6 = 6 * 0.54

MODS = {"aura 20% (Nerve: Entwined)": 575, "cold/pen at 8 Focus (Tongue: Apathetic)": 18, "+2 Active (Nerve: Compelling)": 202,
        "sealed comp prefix (Nerve: Unsealed)": 370, "proj speed: 1 of 5 adv prefixes x Vital Matchless 62.5": 5 * 62.5,
        "10% ele res: 1 of 10 adv suffixes x 62.5": 10 * 62.5, "basic (ES 2/10 or crit 1/8) x Vital Fine 22": 6 * 22}


def comb(n, k):
    from math import comb as c
    return c(n, k)


def p_offered(pool, wanted):
    """P(at least one wanted affix among the 2 offered out of `pool`)."""
    return 1 - comb(pool - wanted, 2) / comb(pool, 2)


def one_line(attempt, p_off, p_land, restart):
    """Expected cost to place one legendary line. Each attempt costs `attempt`; with p_off the wanted line is offered (else nothing);
    if offered it lands right with p_land, else the item is scrap and `restart` (chest + work so far) is paid again."""
    p_ok = p_off * p_land
    p_ruin = p_off * (1 - p_land)
    # E = attempt + (1 - p_off) E + p_ruin (restart + E)
    return (attempt + p_ruin * restart) / (1 - (1 - p_off) - p_ruin)


def rainbow(regime):
    attempt = RAINBOW + SUTURE
    prep = CHEST + (JUNK if regime == "filled" else BASICS6)
    land = 2 / 6 if regime == "filled" else 1.0
    e = one_line(attempt, p_offered(4, 1), land, prep)
    return prep + e


def cage(regime, lines=2):
    attempt = CAGE + SUTURE
    prep = CHEST + (JUNK if regime == "filled" else BASICS6)
    land1 = 2 / 6 if regime == "filled" else 1.0
    e1 = one_line(attempt, p_offered(5, 2), land1, prep)           # either wanted line (Cage stacks / Extreme Coldness)
    if lines == 1:
        e1 = one_line(attempt, p_offered(5, 1), land1, prep)       # Cage stacks only
        return prep + e1
    land2 = 1 / 5 if regime == "filled" else 1.0
    e2 = one_line(attempt, p_offered(4, 1), land2, prep + e1)      # the other wanted line; scrap = redo everything
    return prep + e1 + e2


if __name__ == "__main__":
    mods = sum(MODS.values()) - MODS["+2 Active (Nerve: Compelling)"] - MODS["sealed comp prefix (Nerve: Unsealed)"]   # one ult prefix: cold/pen
    print(f"mods after the organ (aura, cold/pen, proj speed, 10% res, one basic): ~{mods:,.0f} FE  ({', '.join(f'{k} {v:.0f}' for k, v in MODS.items())})")
    for regime in ("filled", "basics"):
        print(f"\n== regime: {regime}")
        print(f"  Rainbow (+19% line):                 {rainbow(regime):10,.0f} FE  (+ mods {mods:,.0f})")
        print(f"  Cage, Cage-stacks line only:          {cage(regime, 1):10,.0f} FE")
        print(f"  Cage, stacks + Extreme Coldness:      {cage(regime, 2):10,.0f} FE")
