# Profound farming plan (2026-10-29 23:00, bottom-up model; prices of 2026-10-29)

## Deep Space (2026-10-30 16:00) — raw etor strategies, today's prices, FE drops now counted
Method: `tools/farm/deepspace.py` (docs/farming.md). 908 Deep Space strategies / 113k runs, no Cage, no Safari. Net = steady loot
(items with >= 8 drops in the group, 12.5% tax, FE untaxed) minus everything the map consumed. CN seconds; Vlad's seconds unknown
except "Machines 3 min, Might slow". Correction: every raw-strategy number before this message priced FE drops at 0 (bug in runs.py);
all nets were 13-100/map low, order unchanged.

| setup (4 compasses + probe) | cost/map | gross | net/map | CN s | CN FE/min | evidence |
|---|---|---|---|---|---|---|
| **Ember farm**: Onslaught Might 39 + Reserve Ember 5.7 + Bounty Ember 2.5 + Flourishing Gods 21 + Ember DS probe 5 | 108 | 219 | 111 | 86 | **77** | 1 player, 124 runs (day5). Tree Might+Commodities |
| Machines: Cruising Mechanical (A) 23.5 + Colorful Fluorescent (A) 7 + Transgression Plunder 44 + Strength in Numbers 1 + Fluorescent DS probe 29 | 139-145 | 233-259 | 91-112 | 83-112 | 54-66 | 28 strategies, 3,500 runs; median player 56-68, best 89-94 |
| Doll compass farm: Collection Doll (A) 110 + Ascendant Ecliptic 53 + Vast Ecliptic 16 + Sinful Plunder (A) 45 + Flourishing DS probe 29 (or Compass DS probe 115) | 270-350 | 369-424 | 87-100 | 117-123 | 43-51 | 190 strategies, 25k runs; median 34-49, best 95-194 |
| Alert Outlaw stack: Alert 32 + All-Evil Vigil 62 + Generous Elite 16 + Sinful (A) 45 + Flourishing probe | 227 | 312 | 79 | 99 | 48 | 20 strategies, 2,477 runs; median player 30 |
| Legendary Gear / Bountiful Elite / Might-gear hunts | 180-360 | | <= 0 steady | | | lotteries; not income |

Ember farm, what it is (tlidb): Onslaught Might Compass forces Trial: God of Might and replaces the Statue with an Onslaught Automaton
(invincible until the trial reaches max level, then "drastically" more drops when killed). Might node Mad - Might: embers dropped in the
trial have 3.5% chance to become Ultimate Embers, -75% additional drop quantity in the trial. Reserve Ember Compass: Ultimate Embers
replicated once (x2). Bounty Ember +50% ember quantity, Ember DS probe +40%, Flourishing Gods +25% per Divine Blessing stack (stack at
trial level 10). CN loot/map: Ultimate Ember 9.31 (20.7 FE today, 24 yesterday), Matchless 53, Precious 80, FE 13.4, Onslaught/Flourishing
Might compass 0.13 each (Willful - Might at level 10). Check: UE / (Matchless+Precious) = 7.0% = 3.5% x 2 — the mechanic as written.
A second player (77 runs, Might compasses on 58% of maps, 4-way split tree) got ~6.5 UE per Might map. Cost 108 = compasses 68 + beacon
23.5 + 2.85 DS resonance + probe 5. Net at UE = 15 FE: ~65/map.
Vlad's FE/min by his map time: 86 s 77, 100 s 67, 120 s 55, 150 s 44, 180 s 37. Break-even vs Profound Safari (~50/min) at ~130 s.
Crawl complete (2,443 details): 4 clean Ember-farm players, 305 runs. Three at 74-86 s/map: 9.31 / 7.97 / 9.67 UE per map = 83 / 70 / 93 FE/min;
one at 149 s/map got 4.17 UE = 32/min (slow trial = half the embers, not just half the maps). Run-weighted 58.6/min. The no-Mad variant
(50 runs, Bounty + Flourishing Gods + Onslaught + Sinful, no Reserve) drops 268 Matchless + 382 Precious = 123 FE of regular embers at 130 s
-> Mad's -75% costs ~100 FE and the 3.5% returns 145-170: Mad wins by 50-70/map. Confidence: medium (4 players), high on the mechanism.
UE price is the other risk (it fell 14% in a day).

Tree for the Ember farm (92 Star + 4 Prime; pictures `ss14/thea/trees/deepspace_ember/{Might,Commodities,Profound,Loadout}.png`):
- Might 42: CN's 35 (Mad, Willful, Irritable on path, 13 "+1% ember" micros, 15% + 35% ember replicate, +1/+1/+3 max level,
  +4%/floor, +5% trial drop, 17 "+2% extra trial monster" path micros) + Mania (30%: a Might Sentinel, kill it -> +50% trial drop; 4 pts)
  + 3 pts on the +10%-extra-monster spoke. Not taken: +140% ember but UE -> Flame Sand (kills the farm), Dwarven Automaton spokes.
- Commodities 25: ember spoke (5 x 2% + 8% replicate, bosses 10% +1 ember), 15 x "+1% Drop Quantity" with the 3 extra-monster mediums.
- Profound (4 Prime + 25 Star): +2%, +25%/-4 attempts (skip it if he dies > 2x per map in Deep Space), +2%, +12% additional.
Play: start the trial first, push levels (the Automaton is invincible until max level), kill the Automaton, finish the map.
Cards in the deck from the tree: Irritable - Might (ember replicate 15/20/40%), Willful - Might (+100% trial drop, 1 attempt), Mad.

### Full day 2026-10-30 10:39 -> 10-31 04:38 EET (UE_game-backup log, 111 maps, `gamelog.py`, Secrets at the exchange value)
| stack | maps | s/map | deaths | net/map | FE/min of map time | Shadows |
|---|---|---|---|---|---|---|
| Machines: Cruising (A) + Focus + Colorful (A) + Strength in Numbers + Flourishing probe | 82 | 127 | 3 | 63.9 | 30.2 | 21 in 9 drops |
| Machines with Transgression, no probe (12:23-12:44) | 9 | 102 | 0 | -23.3 | -12 | 0 |
| Alert Outlaw + Bandit Dark Surge + Phantom Vigil + Lunaria + Flourishing (10:40-11:32) | 12 | 102 | 7 | 46.1 | 24 | - |
| Deep Space Machines (15:16-15:23) | 3 | 150 | 3 | 43.7 | 16 | 0 |
| Ecliptic + Vast Ecliptic + Revelation Hunting astrolabes + Lunaria | 3 | 86 | 5 | -37.0 | - | - |
All 92 Cruising maps: 29.5 FE/min, 24 Shadows in 10 drops (0.11 drops/map, 2.4 each), +9/map without them. Whole day: 6,037 net, 220 min in maps
= 27.5 FE/min. The first 25 Machines maps (12:23-14:34) = 48/min (3 drops x5 x3 x3); the other 67 = 24/min (7 drops of 1-3). Drop pets identical on
every Machines map (servantId list in the join dump) -> variance, not setup.
Not in this table: 6 runs of the season board's final map (`S16FinalMap`, entered from town, 33-52 s each) = +1,217 FE (Flame Elementium
116-201 a run + Flame Sand, embers, compasses); the 10-31 session had one more (+240). Day total with them ~7,250 net.

### Vlad's Profound Machines, 2026-10-30 log (25 maps 12:23-14:34 EET; the earlier label "10:23-12:40" was UTC)
107 s/map, 0 deaths, net 73/map = 41 FE/min **of map time** (25 x 107 s = 45 min of a 137-min window; on the clock 1,825 net / 137 min = 13 FE/min; that file is one game launch only, the rest of the day is in UE_game-backup-*.log) — all of it 11 Disappearing Shadows (227 FE, plane-exclusive memory) in 3 maps (x5, x3, x3:
one drop event replicated by Colorful (A) 50% + probe 40% + Focus); without them -14/map. CN Profound Machines: 0.50 Shadow/map over
432 runs; Vlad 0.44 — at par; a 13-map gap at ~0.135 events/map happens 17% of the time. Secrets 78/map vs CN 85-127; FE 15 vs 20-29.
Transgression in Profound (10 maps): Secrets 89 vs 71, i.e. +5 FE for 44 — drop it there.
**Focus Fluorescent**: +50% chance for *Exclusive* (plane / gameplay) memories. Disappearing Shadow is one -> Focus stays in Profound
(CN: 0.51 with vs 0.48 without, 7 strategies). Immolating Flame (119, the Deep Space money) is a "Deep Space difficulty" drop, not
exclusive: CN Deep Space Machines with Focus 0.59/map (761 runs) vs without 0.77 (16.7k runs) -> no Focus in Deep Space.
Deep Space Machines for Vlad: same tree, swap Focus -> Transgression 44 + Strength in Numbers 1, Profound probe -> Fluorescent DS probe
29 (+0.24 Immolating +59 Secrets = +39 net for 29), T8 beacon -> DS beacon 23.5: CN net 108/map at 105 s = 62/min (8,199 runs);
at his 107 s ~60/min vs 41 in Profound.

### Vlad's Profound Machines, 2026-10-31 log (16 maps 11:53-12:57 EET) — "biggest Secrets of Glacial Abyss farmer"
Stack: Cruising Mechanical (A) 23.5 + Focus Fluorescent 5.5 + Colorful Fluorescent (A) 7 + Strength in Numbers 1 (no Transgression) + Flourishing
Profound Probe 2.1 + GA T8 beacon 3.1 + 28 resonance = 45.3/map. 93 s median in map (mean 114; one 359 s map), 13 s town between maps -> 107 s/map,
0 deaths; on the clock 678 net / 68 min = 10 FE/min (38 min in town: AH restocks, the prism, the exchange). Loot: 1,069 Secrets (66.8/map; 10-30: 78, CN 85-127), FE 16.5/map, 3 Disappearing Shadows from 2 drop events (x1, x2; 10-30: 11 from
3 events x5/x3/x3 — same event rate ~0.13/map, the replication rolled low). Net 42/map = 24 FE/min with Secrets at the exchange (32/map = 18 at AH
price); without the Shadows +5/map: the stack is the Shadow lottery plus Secrets.
**Secrets at the Spacetime Wanderer**: 30 Secrets -> "random Flame x10" = 10 draws, each 10 Flame Sand or 10 FE. 24 exchanges: 300 FE + 2,100
Flame Sand -> 0.417 FE per Secret (+2.9 Flame Sand, the Enchant currency, untradeable) vs 0.26 selling at 0.3 after tax = +60%, ~+10 FE/map.
Probe, pet and card, re-priced 2026-10-31 on his quantity sheet (docs/farming.md; pool x4.49, replication: every hit a copy, Kong 20% in the
list, 13% x3 per copy; memories 83.5 FE/map = Shadows 50.1 + Secrets 29.4 + big memories 4.0; non-Shadow loot 58.6 FE/map). Earlier lines here
used tlidb's stale pet numbers.
- Miss Melancholy - Pink (+42% DQ) for Sky's Dome (+26% DQ, +24% additional FMS, 10% replicate): pool +16 = +2.1, Sky's FMS gone = memories
  x0.806 = -6.5 (if the line works), its 10% replicate gone = -4.1 -> **-8.5 FE/map** (-2.0 if the FMS line does nothing).
- Fluorescent Profound Probe (5.5, 20% replicate) for Flourishing (2.1, +20% DQ): +8.2 memories, -2.6 quantity, -3.4 cost -> +2.2, a wash.
- Both (his 10-31 evening): -6.3 FE/map if the FMS line works, +0.2 if not. **Evening check**: Secrets/map x0.84 vs the same cards yesterday if
  Sky's FMS line works, x1.04 if it doesn't (map noise ~34%, so ~30 maps separate them at ~3 sigma). Rare-drop sizes per 100 drops: fitted rule
  21/34/20/13/8/3/2, "stop at the first hit" 21/57/3/17/0/1/0.
- **Re-priced on the plane-exclusive read** (pool and Shards don't touch Secrets / Shadows = 79.5 of 108.7 FE/map; the flat pool only moves the
  ~29 FE/map of FE, big memories and the rest): +30% DQ card +1.9 FE/map, +20% +1.3; drone card (+10% additional, Machines trial) x1.10 on
  Secrets + Shadows = +8.0, level with Melancholy 20 (+8.2), behind Melancholy 30 (+12.3). Pink for Sky's Dome: +1.0 pool, -4.1 replicate, -0.8
  Shards on big memories = -3.9 FE/map; Fluorescent probe for Flourishing: +8.2 - 1.3 - 3.4 = +3.5; both = -0.4. Best: Sky's Dome + Fluorescent
  probe (+3.5). Resonance 31 vs 15 = +1.6 for 1.8 FE (break-even), 31 vs 0 = +5.5 for 3.4 (+2.1).
- First tally [Vlad 10-31 evening]: 13 maps Flourishing 905 Secrets (69.6/map), 19 maps Fluorescent probe 1,457 (76.7/map) = x1.10
  (se of the log ratio ~0.12). If the 19 were all Pink: "Memory Shards line does nothing" (x1.04) 0.5 sigma off, "works" (x0.84) 2.2 sigma ->
  ~10:1 for "does nothing", cards and crystals unchecked; the log decides.
- Confusion Card: Melancholy 30 = +12.3 FE/map, Melancholy 20 = +8.2, +30% DQ = +3.9, +20% DQ = +2.6 (+ the Shadow share for the replicate
  cards, so lumpy).
Town that session (not map loot): bought + levelled a Phantasmagoria (1,888 + gauges 70 + Prism Level III 749) and listed it 2 min later.

### Alert Outlaw + All-Evil Vigil stack (Deep Space) — the one he likes
Alert Outlaw 32 + All-Evil Vigil 62 + Generous Elite 16 (not Bountiful: the Bountiful version is -7/min over 804 runs) + Sinful Plunder (A)
45 + **Flourishing Deep Space Probe** 29 + beacon 23.5 + ~3 resonance = 227/map. 26 strategies / 2,842 runs: gross 309 (FE 100, Nether
King's Divine Remnant 0.80 = 47, Warlock 0.75 = 45, Vanguard 0.39 = 16, Fossil 9, Tank 5), net 77 at 100 s = 46/min run-weighted; median
player 31/min, top third 70-97/min (net 110-173 at 80-107 s) on the same tree — good players: FE 113, Warlock 0.95, Remnant 0.96 per map;
the rest FE 91 / 0.61 / 0.71. The FE engine is All-Evil: each Manifestation killed = Fright stack (max 3) = +100% additional Vigil drop.
Tree (pictures `ss14/thea/trees/deepspace_alert/`): Outlaw 28 (#48-75: 21 "+1% Security" micros, +6%, reinforcements Rare, Oppressive
+30% after Bounty Order, Imperious +2%/10 bodyguards, Super Sonic +23%, Expansion Mods more likely, Warlock more likely), Afterlight 39
(29 "+1% Vigil" micros, Noble Coffins +25%, Vigil Goblin + its +100%, Nether King's Divinity replicate 10% / +1 from Wraith bosses /
Banishment / Judgment, +8%, White Night + its +12%), Profound +12% additional (25 Star) = 92; Prime +2%/+2%/+2%/+12%, no -4 attempts.

Decision: run 5 Ember maps with the log on (cost ~540 FE) -> `gamelog.py` gives s/map and UE/map; above ~130 s it loses to Safari.
Machines in Deep Space is the same FE/min as Machines in Profound (CN 51-60 there) and needs his bubble fix (3 min maps = 22-30/min).
Doll is the safest number (25k runs) but 350 FE a map of compasses and a timing minigame; at CN speed 43-51/min.


## CORRECTION 2026-10-30 10:30 — the stack numbers below are wrong; read this first
Reality check against Vlad's own maps (game log, `tools/farm/gamelog.py`) and the raw CN strategies:
- Vlad, 25 stack maps (22 on etor 10-29 night + 3 in today's log): ~25 net/map **non-lottery** at 1:45-2:05 per map (today: 129 s/145 s/105 s,
  3 deaths; FE 23.7/map, edicts ~2/map, 0 Expansion mods in 3 maps, 3 God of Might remnants in one map). The 712 FE of Mercury Purged
  (3 in 22 maps) is a 0.004/map CN lottery (4 drops in 1,036 Lunaria maps) = 1 FE/map EV, not income.
- CN strategies that run Alert Outlaw (66 of them, incl. the Bountiful/Generous Elite + Sinful (A) stackers): gross 41-108, **net -178 to +31**
  at today's prices (Alert 29 FE, Warlock 28). Warlock 0.19-0.49/map, Vanguard 0.15-0.49. Alert Outlaw is a loss at today's mod prices for
  everyone; the only CN Alert+Bandit stack (61 runs, 102 s): gross 68, cost 90, net -21. Phantom + Lunaria (156 runs, 91 s, cost 20):
  gross 79 non-lottery, net ~59 = 39 FE/min.
- Why the model said 202-219 net/map: it sums per-compass NNLS columns, each evaluated at (1.2x) the largest multiplier any CN strategy
  ran for that compass, all four at once; the top-multiplier CN strategies are themselves over-predicted by the fit (pred 95 for the Alert
  column of a strategy whose whole gross was 80), the "generic" FE is shared between columns, and no CN strategy runs the four together.
  Per-column obs/pred looked fine because each column's item list includes FE. Raw run-weighted obs/pred over all 629 strategies: 1.5 with
  R^2 < 0, binned: strategies predicted > 200 gross observe 0.55x of it. The column model is retired for ranking; rank on raw CN strategies
  (`runs.py`) scaled by Vlad's times, and on Vlad's own logs.

### Corrected ranking (raw CN strategies, today's prices; "Vlad" = his measured or VLAD_TIME seconds)
| plan | CN net/map | CN s | CN FE/min | Vlad s | Vlad FE/min |
|---|---|---|---|---|---|
| Bandit DS + Phantom Vigil + Lunaria + Flourishing probe (drop Alert) | ~45-60 (Phantom+Lunaria 59; Bandit adds edicts ~8, costs 0.9) | 91 | 39 | ~100 | 27-36 |
| Machines: Cruising (A) + Sinful/Transgression etc. (7 CN strategies, 432 runs) | 74-99 (gross 160, cost 81) | 80-111 | 50-68 | 200 (bubbles) | 22-30 |
| Safari: Revelation Hunting + Ecliptics (219 runs) | 38-65 (one Artifact-Sinful one: -19) | 54-68 | 43-58 | ? | ? |
| Clockwork: Collection Doll + Ecliptics (3,514 runs) | 50-65 (gross 102-130, cost 60-70) | 93-131 | 30-38 | ? | ? |
| Alert Outlaw + Bandit + Phantom + Lunaria (what he ran) | CN: -21; Vlad: ~25 non-lottery | 102 | <0 | 105-145 | ~13 + lottery EV ~17/map (1-in-1,000 tickets) |
Lottery EV per map (items < 25 drops / 46k runs, shrunk): global 7, Lunaria 8 (Omni-Elixir Notes 9,788 at 0.0009/map), Bandit 2, Dark Surge 4.
Next: his backup logs (`UE_game-backup-*.log`) for the 22-run session and any Machines/Safari sessions -> his own s/map and net/map
per plan; then the table gets his columns and the recommendation is whichever of Phantom/Lunaria/Bandit vs Machines wins on HIS minutes.

## Safari compass farm (2026-10-30 12:00) — from the CN Revelation strategies, not the column model
CN: 冰图 罗盘×54/狩猎×35 (30 runs, 68 s, gross 125, cost 59, net 65 = 58/min) and 罗盘×51/狩猎×35 (84 runs, 54 s, gross 97, net 38 = 43/min);
the Sinful-added versions did worse (net 28; Artifact Sinful -19). Pooled 114 runs: gross ~104, net ~45, 58 s -> 46/min at CN speed.
Loadout: Revelation Hunting Astrolabe 22 + Vast Ecliptic 16.2 + Ecliptic 1.4 + Lunaria 0.3 (filler for the +2.5%/compass node; CN used
War 2.9) + Compass Profound Probe 13; beacon 3.3, resonance 3.4 => 59.6/map. Drops are compasses: Collection Doll (A) 0.13 (105 FE),
Containment Overrealm 0.07 (160), Fated Arcana 0.40 (23), Consultation Vorax 0.17 (54), Alert 0.23, Sinful 0.40, Sinful (A) 0.13,
Unrivaled Veteran 0.47, Mystery Treasure Gods 0.23 ... (per map, 30-run strategy).
Tree (92 Star): Compass 56 = 35 micros, 5% replicate, +4%, +2.5%/compass inserted (#12, on the ring; etor never logs it but 35 micros
are unreachable without it), 2%/3% more valuable, 1% most valuable, Tomorrow's Direction, Giantism, families Raid/Militant/Lunaria/
Creation(mine, Record 29 FE)/Afterlight/Might/Mechanical/Dark Surge/Cube/Arcana/Outlaw/Overrealm/Vorax. Hunting 36 = 18 "+1% Safari/final"
micros, 6 "+1%/boss" micros, 3 "1% compass replicate" micros, skip-buff, Insidious (on path; etor doesn't log it), Mistrustful (Safari
mode, +135% final boss), 2x "2 Safari bosses" (one with 25%/3% extra), +7%/boss, +12%/boss, +7%, 5% compass replicate. Profound: 3 micros
+ 25% major (the generic Drop Quantity's effect on Hunting Rewards is unproven; CN ran 2 Profound micros only). Pictures:
ss14/thea/trees/hunting/{Compass,Hunting,Loadout}.png.
Play: Statue of Hunting is at the stage start -> start the trial first, kill all Safari bosses (4 astrolabe + 2 + 2, 25% for +2, 3% for
+6) BEFORE the final boss spawns (blessings only stack until it spawns), then the final boss; it carries up to 15 stacks x (6.5+7+12+6)%.
Expected for Vlad: ~45 net/map at ~50 s => ~55 FE/min (medium confidence: 114 CN runs, his Safari time unknown). Game log will tell.

---
### Superseded (2026-10-29 23:00) — kept for the trees and card priorities, which still hold; the FE/min numbers do not


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

### 22:50 — Outlaw mod-mix nodes (missed, now in)
The model had no rule for "Mods dropped from Carjacks are more likely to be Expansion Mods / - Warlock / - Vanguard", so the
optimizer gave them 0. CN Outlaw loot by group: with the Warlock node Warlock 0.25/map vs 0.137 without (+38% mod value), Vanguard
node +21% on top; every serious CN Outlaw farmer has the Expansion node (valued x1.5 as a prior). Outlaw tree now 18 = micros ->
+6% -> Rare reinforcements -> Oppressive, and the side spoke to Expansion Mods -> Warlock, Vanguard (Imperious out). Stack 179 FE/min,
211 net/map. Drawings in ss14/thea/trees/with_lunaria/.

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
