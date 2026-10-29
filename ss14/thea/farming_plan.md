# Profound farming plan (2026-10-29 23:00, bottom-up model; prices of 2026-10-29)

Model: `tools/farm/bottomup.py` + `plan2.py` + `search.py` + `vlad_plans.py` (method in `docs/farming.md`). 629 CN Profound
strategies / 46k runs decoded item by item; every strategy's loot divided by the multipliers its own setup gave each drop channel
(pool, card, mechanic "additional" nodes and compass lines, compass-class lines, fluorescent replication, Focus, Transgression),
NNLS per item -> naked yield per compass key; Vlad's plan re-applies his multipliers, capped at the largest multiplier CN ever ran
for that compass (no extrapolation past the data). Per-column observed/predicted on CN: 0.89-1.11. Items with < 25 drops in 46k
runs are lotteries, valued at their shrunk observed rate. Pets not logged (CN's pets inside the yields; Vlad's assumed comparable).
Prices: today's etor list, 12.5% tax, FE untaxed. Time: 40 s bare map [Vlad], Machines/Might 180 s [Vlad], other mechanics CN
seconds x 40/58 (Vlad clears the plane 1.45x faster than CN; mechanic time scaled the same). Tree: 92 Star - 25 (the +12% node)
= 67 Star optimized by tree-knapsack; Profound 4 Prime = 2 micros + 30% major + 12% additional major.

## Ranking (net FE/min, Vlad's times)
| plan | FE/min | net/map | cost/map | s/map | what pays |
|---|---|---|---|---|---|
| **A. Alert Outlaw + Bandit Dark Surge + Phantom Vigil + Lunaria, Flourishing probe** | **156** | 183 | 51 | 70 | FE 54, Blueprint Eternity 43 (1 per ~80 maps), Warlock/Vanguard mods 39, Nether King's Divine Remnant 21, Edicts 16 |
| A-cheap: Outlaw + Bandit + Vigil + Lunaria base compasses, Flourishing probe | 136 | 176 | 11 | 77 | blueprint lottery 82 (hot: 33-pt DS tree), FE 30 |
| Alert + Bandit + Flourishing probe only (greedy optimum at CN times) | 145 | 136 | 39 | 56 | |
| C. Clockwork: Collection Doll + Vast + Ecliptic + Sinful, Compass probe | 111 | 138 | 69 | 75 | compasses 139 (Consultation Vorax, Sinful (A), Fated Arcana, Containment...) |
| D. Safari: Revelation + Vast + Ecliptic + Sinful (A), Compass probe | 76 | 96 | 99 | 75 | compasses 117 |
| **B. Machines as run: Cruising + Focus + Colorful (A) + Transgression** | **45** | 164 | 86 | 220 | Disappearing Shadow 0.62/map = 132, Secrets 136 = 36, FE 24 |
| Machines + Outlaw + Dark Surge (Cruising + Focus + Alert + Bandit) | 37 | 152 | 64 | 244 | the 4-minute map kills whatever is bolted on |
| single mechanics (+ tree): Bandit DS 105 · Alert Outlaw 94 · Outlaw 92 · Phantom Vigil 88 · Lunaria 69 · Lunar Stele 64 · Evernight 64 · Strength in Numbers 64 · Revelation 62 · Collection Doll 56 · Overrealm 28 · Fated Arcana 26 · Might <= 3 · Containment Overrealm, Mecha Might (A), Consultation Vorax, Bountiful Elite negative | | | | | CN-time version; Vlad-speed ~x1.15 |

Machines is a good map and a bad minute: 164 net per map is the best single map in the list, but 3 min 40 s per map puts it at
a third of plan A. The Machines FE/min only moves with the map time (2 min total -> 82/min, still under A).

## Plan A, exactly
Compasses: Alert Outlaw (29), Bandit Dark Surge (0.9), Phantom Vigil (= Phantom Afterlight, 12), Lunaria (0.3). Probe: Flourishing
Profound (2). Beacon 3.3, resonance 31 (3.4). Cost 51/map (the Profound refund node makes it 46).
Tree, 67 Star + Profound: Dark Surge 31 = 24x "+3% Corrosion Energy" micros, 2x "+10%", "+10% · -5% dmg per eruption", "+40%
Corrosion Energy", "subsequent eruptions automatic", "higher chance of Legendary gear from Eruption" (Disgraceful), "Ultimate
Legendary chance +430% / no non-Legendary gear" (Humiliated). Afterlight 16 = 12x "+1% additional for the Vigil", "+8%",
"White Night Mode", "+12% during White Night", "+15% (Grief, Phantom Flames)". Outlaw 12 = 9x "+1% for Security personnel",
"+6%", "reinforcements more likely Rare", "+30% after activating a Bounty Order" (Oppressive). Commodities 8 = "+1% Drop
Quantity" micros (leftovers). Profound: 2 micros + 30% + 12%.
Expected per map: FE 54, Blueprint Eternity 0.011 (3,789 each), Expansion Mod Warlock 0.40 (70), Vanguard 0.33 (51), Nether King's
Divine Remnant 0.33 (72), Edict Doom 0.68 (12), Edicts Dive/Ruin/Dart ~1.1 each (3), Tank mods, Omni-Elixir Notes lottery 8 FE EV.
Variance: a third of the value is a 3,789 FE blueprint every ~80 maps and a 9,788 FE Omni-Elixir every ~1,100; the steady part
(FE, mods, remnants, edicts) is ~120 net/map = 100 FE/min on its own.
Why it beats compasses: Outlaw/Dark Surge/Vigil cost 0.3-29 FE per map and add 10-15 s each; compass farms cost 70-100 FE per map
in astrolabes and probes and compass prices keep sliding.

## Plan B (Machines) — what the model says about Vlad's run
- CN's logged Machines trees are 26x "+1% chance for 1 additional attack round" + "+25% for Drones" + attackers/intervals. **None of
  the 555-run CN Machines strategies took the echelon nodes** ("2 echelons / -100%", "2 additional echelons", Dull) nor Obtuse.
  Their effect with Cruising is unknown to the data -> modeled as neutral. If they double drones, Machines is ~90 FE/min; if the
  "-100% additional during Trial" on the first one kills drone drops under Cruising (likely why CN skips it), it is a trap.
- With his compasses and the CN-shaped tree: 0.62 Disappearing Shadow, 136 Secrets, 24 FE per map; the Fluorescent probe adds +18
  net in the model but not in game (replication already capped by Creation 30 + Colorful (A) 50 + pets 30).
- Earlier slot answers stand (tools/farm/machines.py): Focus stays, Transgression > Strength in Numbers (time test pending), probe out.

## Open
- Echelon nodes with Cruising (Vlad to test or recall): the only thing that could move Machines above 60 FE/min.
- Plan A test: 10 maps, time per map and the counts of mods / edicts / remnants; expect ~70 s and ~120 net without a blueprint.
- Pets for plan A (XD matrix, to do): the three that work on Outlaw/Dark Surge/Vigil loot.
- Pets, card picks, Clockwork rating play and second-same-family compasses are not in the model.

## Earlier (superseded) numbers
Top-down rescaling of CN leaderboards (plan A Safari 95 FE/min, Machines 40) and the first machines.py pass: kept in git history
(commit e89c36b and before); the bottom-up model replaces them.
