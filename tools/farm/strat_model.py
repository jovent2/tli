#!/usr/bin/env python3
"""Price Deep Space setups on Vlad's own base rates, with the text multipliers haircut by the text-vs-data slopes.

Base = his 11-06 loop (51 maps, by phase: map 42, Vigil 63, Overrealm 130 FE/map at today's prices) and his 11-05 Alert maps
(Outlaw phase ~78 FE/map at Sinful (A) + Generous). A change multiplies a phase by (text multiplier) ** slope, slopes from
texttest.py: additional lines 0.7 on Vigil / map loot, 0.95 on mods, 0.73 on Overrealm FE; flat-pool lines 0.5 on Vigil / Outlaw /
map, 1.0 on Overrealm FE. Compass swaps use the family fits (fits/*.md) where the text has no number (Generous, Containment).
Jackpots (Inverse Image, Gaze...) are counted from CN drop rates, not fitted. Time: his seconds (+20 s town).
  python3 tools/farm/strat_model.py
"""
BASE = dict(map=42.0, vigil=63.0, ovr=130.0, outlaw=0.0)   # FE/map, his loop today
COST_LOOP = 110.0                                           # Evernight 21 + Shadow 1.5 + Generous 17.5 + Sinful 13.6 + probe 27.4 + beacon 23.5 + res 6.4
SEC_LOOP = 215 + 20
S = dict(add_vigil=0.7, add_map=0.6, add_mods=0.95, add_ovr=0.73, flat=0.5, flat_ovr=1.0)
POOL_NOW = 1 + 1.0 + 0.4 + 0.4 + 0.1       # resonance, Sinful, probe, Profound micros (~5)


def pool_factor(delta, slope):
    return ((POOL_NOW + delta) / POOL_NOW) ** slope


def show(name, phases, cost, secs, note="", jackpot=0.0):
    gross = sum(phases.values())
    net = gross - cost
    print(f"{name:58s} gross {gross:4.0f} (map {phases['map']:3.0f} vigil {phases['vigil']:3.0f} ovr {phases['ovr']:3.0f} outlaw {phases['outlaw']:3.0f})"
          f" cost {cost:3.0f} net {net:4.0f}/map | {secs:3.0f} s -> {net / (secs / 60):5.1f} FE/min" + (f" (+{jackpot / (secs / 60):.0f} jackpot EV = {(net + jackpot) / (secs / 60):.0f})" if jackpot else "") + f"  {note}")


def main():
    b = dict(BASE)
    show("A0 his loop today", b, COST_LOOP, SEC_LOOP)
    # A1: DS resonance affix (+15% additional, 6.8 FE)
    a1 = dict(map=b["map"] * 1.15 ** S["add_map"], vigil=b["vigil"] * 1.15 ** S["add_vigil"], ovr=b["ovr"] * 1.15 ** S["add_ovr"], outlaw=0)
    show("A1 + DS resonance affix", a1, COST_LOOP + 6.8, SEC_LOOP)
    # A2: card +30% Drop Quantity instead of the gear card (flat pool)
    a2 = {k: v * (pool_factor(0.3, S["flat"]) if k != "ovr" else pool_factor(0.3, S["flat_ovr"])) for k, v in a1.items()}
    show("A2 + pick the +30% DQ card", a2, COST_LOOP + 6.8, SEC_LOOP, "vs today's +50% gear card")
    # A3: Alert in Generous's slot: Outlaw phase from his 11-05 maps (78 at Sinful (A) + Generous) -> his pool, no Generous
    outlaw = 78 * pool_factor(-0.4, S["flat"]) / 1.15 ** 0.7
    outlaw *= 1.15 ** S["add_mods"]                     # DS affix on it
    outlaw *= 1.37 ** 0.9                               # Outlaw pets on the kill (Twilight / Shro-Shroom / Prof. SOURCE vs Fuel pets)
    a3 = dict(map=a2["map"] / 1.10, vigil=a2["vigil"] / 1.18, ovr=a2["ovr"], outlaw=outlaw)   # Generous out: fits x1.10 FE, x1.18 Remnants
    show("A3 + Alert Outlaw instead of Generous (+pets)", a3, COST_LOOP + 6.8 - 17.5 + 37, SEC_LOOP + 15, "+70% monster life")
    # A4: Sinful (A) instead of Sinful
    a4 = {k: v * (pool_factor(0.4, S["flat"]) if k != "ovr" else pool_factor(0.4, S["flat_ovr"])) for k, v in a3.items()}
    show("A4 + Sinful (A) instead of Sinful", a4, COST_LOOP + 6.8 - 17.5 + 37 + 31, SEC_LOOP + 15, "-50% dmg taken instead of -30%")
    # Floors: his own data, 2 floors 204 gross / 199 s vs 3 floors 323 / 275 s
    print("\nFloors (his 51 maps today): 1 floor 129 gross in 126 s (8 FE/min net), 2 floors 204 / 199 s (26), 3 floors 323 / 275 s (43), 4 floors 306 / 266 s (41)."
          " Advance 82% -> 48% -> 45%; the 1-floor maps carry 0.78 deaths/map (a death inside ends the Overrealm).")
    # B: Containment instead of Shadow (family fit: FE x1.84 vs Shadow x1.20 -> x1.53 on Overrealm FE; Sprouts same; jackpots 130/map EV from drops)
    bb = dict(a2); bb["ovr"] = a2["ovr"] * 1.53
    show("B  A2 + Containment instead of Shadow", bb, COST_LOOP + 6.8 + 105, SEC_LOOP + 45, "keys force floors 3-4; CN players die 6-7/run", jackpot=130)
    # C: the Alert + All-Evil stack on HIS base: Vigil at x4 (3 stacks) vs Evernight x2, haircut 0.67; Outlaw as A3 with Sinful (A)
    vig = b["vigil"] * (4 / 2) ** 0.67 * 1.15 ** S["add_vigil"]
    out = 78 * 1.15 ** S["add_mods"] * 1.37 ** 0.9
    c = dict(map=b["map"] * 1.15 ** S["add_map"] * pool_factor(0.4, S["flat"]), vigil=vig, ovr=0, outlaw=out)
    show("C  Alert + All-Evil + Generous + Sinful (A) + probe + DS affix", c, 42.5 + 58 + 36 + 17.4 + 27.4 + 23.5 + 6.4 + 6.8, 124 + 20, "needs the 3 ghosts dead before the loot; his 11-05 measured -60")
    c0 = dict(c); c0["vigil"] = b["vigil"] / 2 * 1.15 ** S["add_vigil"]
    show("C0 same with 0 Fright stacks (what he got on 11-05)", c0, 42.5 + 58 + 36 + 17.4 + 27.4 + 23.5 + 6.4 + 6.8, 124 + 20)
    # D: Alert + Evernight + Shadow Overrealm + Sinful + probe + DS affix (= A3)
    print("\nD  = A3: the loop with Alert in Generous's slot.")


if __name__ == "__main__":
    main()
