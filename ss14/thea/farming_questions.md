# Farming model — questions for Vlad (2026-10-29)

Already in hand (don't re-explain): the full compass / astrolabe / probe / season-compass lists, all 27 Void Chart
constellations node by node, the Confusion Card library, the 69 drop pets and the official XD matrix of which pet lines
work in which gameplay, plane/timemark tables, exclusive-drop pages, CN prices for 1,530 items, and 500+ logged CN
farming runs with their Void Chart allocation, compasses, loot and cost (docs/farming.md).

## A. Prices (decides whether the CN list is usable at all)
1. Which server are you on (global TapTap / Google, or CN)? etor is a CN-server tool. You paid 4,500 for Phantasmagoria;
   the CN list says 96. Give me your trade-house price for: Ultimate Ember, Sacred Fossil, Deep Space Beacon, Glacial Abyss
   Beacon (Timemark 8), Netherrealm Resonance (per 1), Sinful Plunder Compass (normal and Artifact), Bountiful Elite Compass,
   Golden Cage Astrolabe. If the ratios hold I rescale the CN list; if they don't I need a price source for your server.
2. Selling: what's the lowest value you bother listing (0.3 FE compasses?), and is there a listing tax / fee?

## B. The map loop as it is now (tlidb's help is from an older version)
3. The 3 cards: every map? You pick 1 of 3; is the effect for that one map only, and is the +100% from the pick the only
   bonus (no "attempts" left over)? What decides the 3 offered — the card nodes you activated in the Void Chart plus
   timemark? Can you reroll / skip?
4. Resonance: what does the stage screen show for drop quantity at 0 / 10 / 20 / 31 resonance (is it linear, per base
   affix)? Is 31 the max? Same question for Deep Space Resonance if you use it.
5. Stacking: the stage info panel should show one total "Drop Quantity" number. With a +40% compass, a +20% probe and
   31 resonance, does it read 160% (adds) or something else? And does the card's +100% show inside that number or
   separately ("additional")?
6. Tiers you can run: Profound T8 only, or Deep Space too (needs Rank 5+ beacons)? Is there a daily attempt limit on
   Profound / Deep Space (the Profound node says "-4 stage attempts")? Why Glacial Abyss and not another plane?
7. Slots: how many Compass slots and Probe slots on your map screen right now, and how many you can unlock.

## C. Your assets
8. Void Chart: screenshot (or list) of every constellation you have points in, with the node counts — 92 points — and
   the 4 Prime points in Profound. Plus: how many Star Talents are unspent, and what a reset costs you (Winding Keys /
   Elixir).
9. Drop pets: which Drop Pactspirits you own, their rank (1-6), which 3 are installed, and which one follows you.
10. Stock: beacons by plane/tier, compasses/astrolabes/probes worth mentioning, resonance count, liquid FE.
11. Map time: your current clear time per Profound map with the setup you run, and how many hours a day you farm.
12. Build limits: which mechanics you clear without dying or stalling (Vigil, Cage, Overrealm, Clockwork Ballet, Arcana,
    Mistville, Sandlord, Vorax, Warden...), and which ones you skip because they're slow or dangerous. Deaths per map now.
13. What the FE is for: a target list (LW 26% 15k, memories, prisms...) or just max FE/hour? Any drops you'd rather
    farm than buy?
14. Season mechanic (Tartarus in Riot / Warden): do you run the endgame with Shackles compasses, and is it worth your time
    in your experience? Any season-exclusive loop I should know about.

## Answers (Vlad, 2026-10-29 16:02)
1. Same server economy as the CN list ("99.9% the same"; the quoted prices match his). CN price list is valid.
2. Listing tax 1 FE per 8 FE (12.5%); can't list under 1 FE. Everything is value: list, use, or it stacks.
3. Deck = Void Chart card nodes + timemark. Reroll: ~1 per 12 maps.
4. Profound only, not Deep Space. Resonance -> drop quantity: 0:+15%, 1:+30, 3:+45, 7:+60, 15:+75, 31:+100 (don't model under 31).
5. tlidb "Drop quantity" page: Final = base x (1 + sum of Drop Quantity bonuses) x prod(1 + each additional bonus).
   Quantity = number of drop INSTANCES; the amount/tier of each instance rolls on its own (FE stack 1/5/10/50, legendary tier).
   Quantity never improves the roll. Some gameplay rewards ignore quantity (Cubes of Rapacity, Dream Bubbles, Chests of Folklores, Splendor Eggs...).
6. "Stage attempts" = lives per map. The Profound node is +30% quantity for 2 lives (tlidb says +25%); he never dies in Profound.
7. 1 Profound probe slot, 4 compass slots.
8. Void Chart reset is free; I design the allocation (92 Star + 4 Prime).
9. Any drop pet at rank 6 is available (whale). 10. Liquid FE: whatever the strategy needs.
11. Map time depends on the mechanics: God of Machines / Might slow, War / Hunting instant. 12. Any mechanic, no deaths.
13. FE/hour, drops valued at market. 14. Tartarus (Warden) out of scope.

## Round 2 (asked 16:10, answered 16:24)
1. Beacons are not self-sustaining unless you farm them -> cost a T8 beacon per map (GA T8 3.3 FE) or take Beacon nodes/compasses.
2. Deep Space probes do not fit the Profound probe slot.
3. Cage: Deep Space only. "Try it in Profound and you make -11k FE/hr." Cage constellation and Cage Astrolabes are out.
4. 92 Star Talents and 4 Prime are the cap.
5. The 1 FE listing minimum is per listing: stacks of cheap compasses are fine.
6. Bare Profound Glacial map: 40 s. God of Machines: 3 min.
7. Mechanics he doesn't force with the tree or a compass he doesn't do.
8. Card pick: whatever fits the farm (Mystery Chests usually good, drop quantity, the farmed mechanic's card).
