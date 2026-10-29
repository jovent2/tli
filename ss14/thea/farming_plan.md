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
| **A. Alert Outlaw + Bandit Dark Surge + Phantom Vigil + Lunaria, Flourishing probe** | **172** | 202 | 51 | 70 | FE 58, Blueprint Eternity 43 (1 per ~80 maps), Warlock/Vanguard mods 50, Nether King's Divine Remnant 21, Edicts 16 |
| A-cheap: Outlaw + Bandit + Vigil + Lunaria base compasses, Flourishing probe | 136 | 176 | 11 | 77 | blueprint lottery 82 (hot: 33-pt DS tree), FE 30 |
| Alert + Bandit + Flourishing probe only (greedy optimum at CN times) | 145 | 136 | 39 | 56 | |
| C. Clockwork: Collection Doll + Vast + Ecliptic + Sinful, Compass probe | 111 | 138 | 69 | 75 | compasses 139 (Consultation Vorax, Sinful (A), Fated Arcana, Containment...) |
| D. Safari: Revelation + Vast + Ecliptic + Sinful (A), Compass probe | 76 | 96 | 99 | 75 | compasses 117 |
| **B. Machines as run: Cruising + Focus + Colorful (A) + Transgression** | **49** | 179 | 86 | 220 | Disappearing Shadow 0.66/map = 138, Secrets 148 = 39, FE 26 |
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
Expected per map: FE 58, Blueprint Eternity 0.011 (3,789 each), Expansion Mod Warlock 0.50 (70), Vanguard 0.42 (51), Nether King's
Divine Remnant 0.33 (72), Edict Doom 0.68 (12), Edicts Dive/Ruin/Dart ~1.1 each (3), Tank mods, Omni-Elixir Notes lottery 8 FE EV.
Click order (spokes from the Initial Node): Dark Surge 27 = three corrosion spokes (2 micros -> Disgraceful -> 4 micros; 2 micros
-> +10% -> 4 micros -> +10%·-5% dmg -> +40%; 2 micros -> +10% -> 6 micros -> medium -> medium); Afterlight 16 = one spoke: 3 micros
-> +8% -> 6 micros -> Grief +15% -> White Night -> 3 micros -> +12% White Night; Outlaw 16 = one spoke: 3 micros -> +6% -> 3 micros
-> Rare reinforcements -> 3 micros -> Oppressive +30% -> 3 micros -> Imperious; Commodities 8 = +1% quantity micros (3/3/2).
Variance: a third of the value is a 3,789 FE blueprint every ~80 maps and a 9,788 FE Omni-Elixir every ~1,100; the steady part
(FE, mods, remnants, edicts) is ~120 net/map = 100 FE/min on its own.
Why it beats compasses: Outlaw/Dark Surge/Vigil cost 0.3-29 FE per map and add 10-15 s each; compass farms cost 70-100 FE per map
in astrolabes and probes and compass prices keep sliding.

### 4th slot and pets (22:00)
4th slot on Alert + Bandit + Phantom: Lunaria (0.3) +18 FE/map for ~7 s = flat per minute (172 either way; its value is FE/dust
plus the Omni-Elixir Notes lottery, 9,788 FE per ~1,100 maps); Strength in Numbers (1) 165/min; Sinful (13.5) 165, Sinful (A) (40)
150 - the pool is already +162%, more quantity is not worth a slot; Lunar Stele (27) 160; Creation (0.5) shows 183 but its column is
5 CN strategies that happened to drop Blueprint Eternity - noise, not a reason. Nothing beats an empty slot per minute.
Pets (XD matrix, rank 6; generic "+X% Drop Quantity" lines apply to Dark Surge, Vigil and Outlaw Security-personnel drops, not to
Outlaw trade/order rewards): Twilight Sparks (+30 quantity, +3% and +13% additional ~ +29% at his pool), Corgi Fighter No.32 (+36,
+5% additional ~ +19%), Letice (+38 ~ +15%) or Miss Melancholy - Azure (+30 and Vigil +2.6% additional / +6% from Wraiths).
Phantom Vigil Compass (etor name) = Phantom Afterlight Compass (tlidb).

## Plan B (Machines) — what the model says about Vlad's run
- Correction (23:50): etor never logs the two echelon nodes (64 "2 echelons / -100%", 68 "2 additional echelons") and hashed
  Obtuse / Dull / Paranoid with another text join. By the graph (drone spoke 62->76, 77->80) every CN tree with +25% has both
  echelon nodes, and once decoded most CN Machines trees carry Obtuse + Dull too: **CN's Machines tree is Vlad's tree.** Trees are
  now closed under path prerequisites and the extra md5 joins decode (runs.py / bottomup.closed_nodes). The echelon nodes are
  modeled as the drone source (x2 each, Dull x1.5, a prior — their absolute effect is not identifiable because every CN tree has them).
- With his compasses and tree: 0.66 Disappearing Shadow, 148 Secrets, 26 FE per map = 179 net at 220 s = 49 FE/min. The Fluorescent
  probe adds +18 net in the model but not in game (replication already capped by Creation 30 + Colorful (A) 50 + pets 30).
- Earlier slot answers stand (tools/farm/machines.py): Focus stays, Transgression > Strength in Numbers (time test pending), probe out.

## Open
- Plan A test: 10 maps, time per map and the counts of mods / edicts / remnants; expect ~70 s and ~120 net without a blueprint.
- Pets for plan A (XD matrix, to do): the three that work on Outlaw/Dark Surge/Vigil loot.
- Pets, card picks, Clockwork rating play and second-same-family compasses are not in the model.

## Earlier (superseded) numbers
Top-down rescaling of CN leaderboards (plan A Safari 95 FE/min, Machines 40) and the first machines.py pass: kept in git history
(commit e89c36b and before); the bottom-up model replaces them.
