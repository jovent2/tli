# Farming — data sources and what we know (started 2026-10-29)

Goal: answer "what should I farm" with numbers: FE/hour per map setup (plane x tier x compasses x probes x
resonance x Confusion card x Void Chart x drop pets), valued at real prices.

## Sources (all fetched raw with curl from the shell; no WebFetch)
| What | Where | Repo copy |
|---|---|---|
| Prices, CN server, season s14 (id 1601), unit = Flame Elementium | `https://etor-beta.710421059.xyz/etor-api/api/prices-snapshot/1601` (JSON; `?format=protobuf` also works) and `/api/prices-t15/1601` (price x1000 + 23 recent deltas) | `data/ext/prices_etor_s14_<date>.json` (1,530 items) |
| etor item table: id -> Chinese name, type, tlidb English page key | `https://etor-beta.710421059.xyz/assets/game_static_data-*.js` (a `JSON.parse('...')` literal; parse the string, never execute the JS) | `data/ext/etor_items.json` (2,249 items) |
| etor crowdsourced strategy leaderboard (real logged runs: avg FE/run, FE/min, run count, map, Void Chart allocation as node md5s, compasses/probes used, loot and cost item tallies) | `/api/strategy/leaderboard?seasonId=1601&stage=<legacy|week1|day1..7>&limit=50&offset=N` (500 per stage), `/api/strategy/detail?seasonId=1601&stage=S&strategyKey=K`, `/api/strategy/stage-options`. Rate limit: 429 "频繁" if faster than ~1 req / 5 s | `data/ext/etor_strategies_s14/` |
| Official XD "Pactspirit Drop Effect Query": 27 gameplays x 65 drop pactspirits x rank 1-6: which pet affix lines take effect in which gameplay/loot type (full / partial / none) | `https://tl-servant-loot-websearch.workers.xd-sites.com/s/0vry3amsnrrc/data/ui-data-part-{0..6}.js` (JS string parts -> one JSON; `texts` has 13 locales incl. en) | `data/ext/pactspirit_drop_effects.json` (English, compacted) |
| Void Chart (27 constellations, 1,574 nodes), Compasses (79 + 12 astrolabes), Probes (15), Season Compasses, Confusion Card library (218), drop pactspirits (69), timemarks per plane, exclusive-drop pages | tlidb (already in `data/catalog/*.json` and `data/pages/`) | `data/` |

Other etor endpoints seen in the bundle (not pulled): `/api/strategy/windboard` (trend board), `/api/race/*`,
`/api/player/death-leaderboard`, `/api/chart/<item>/<season>?interval=`, `/api/torchlight/7881/price` (FE in RMB).
The bundle also holds the etor request-signing private key (RSASSA-PKCS1-v1_5 / SHA-256) used for `/api/prices/<season>`
with `timestamp` + `signature` params; the snapshot endpoints don't need it.

etor's Void Chart node keys are `md5(Chinese node text)` (verified on "异界关卡中，+2% 掉落稀有度" = e4244a48...).
The bundle only ships 10 constellations' layouts; the Compass/Cage ones used by the top strategies are not in it,
so to decode a strategy's allocation fully we need the Chinese node texts (tlidb.com/cn/Void_Chart) to hash.

## What the data says so far (CN server, week 1 of s14)
- Top etor strategies (500 logged, week1): Deep Space maps, Void Chart = Compass constellation full (37 x "+1.4%
  additional Compass Drop Quantity" micros + mediums, ~55 pts) + Cage constellation (27 x "+1% additional Drop Quantity
  for Cages" micros, ~36 pts) + Profound, running Golden Cage Astrolabe (384 FE) + Bountiful Elite Compass (183 FE) +
  Sinful Plunder (Artifact) + Flourishing/Compass Deep Space Probes. etor: 400-690 FE/run gross, 3-4.5 min/run,
  130-165 FE/min. Valued at 29 Oct prices the gross is ~885 FE/run and the consumables ~590 FE/run (net ~300).
  The loot is almost entirely Compasses/Astrolabes (Consultation Vorax 54, Containment Overrealm 160, Collection Doll
  Astrolabe (Artifact) 105, Sinful Plunder (Artifact) 40 ...) + Sacred Fossils.
- Reference CN prices (FE): Ultimate Ember 24, Sacred Fossil 11.5, Truth Fossil 1.9, Netherrealm Resonance 0.11,
  Deep Space Resonance 3.8, Deep Space Beacon 24, Glacial Abyss T8 beacon 3.3, Sprout of Legends 141,
  Phantasmagoria prism 96 (Vlad paid 4,500 on his server -> the two economies may not map; calibrate before using).

## Rules (tlidb; Vlad's in-game description overrides where they differ)
- Planes: Glacial Abyss, Blistering Lava Sea, Steel Forge, Thunder Wastes, Voidlands (Timemark 1-8, 8-1..8-4,
  Profound Timemark 8), Deep Space (needs Rank 5+ Beacons, "additional drop quantity bonus").
- Compasses: consumed on stage start; most carry "+X% additional Max Life" for monsters; Astrolabes = special compasses.
- Probes: consumed when the portal opens; Profound/Deep Space variants.
- Netherrealm Resonance adds Base Affixes; "Drop quantity increases with the number and danger of the Base affixes".
  Vlad: 31 resonance = +100% drop quantity.
- Confusion Cards: Vlad: 3 cards offered on opening a map, pick 1, its effect + "+100% additional drop quantity"
  (glossary: "+100% additional drop quantity in Netherrealm stages with a Confusion Card"). tlidb's help still
  describes the old Chaos Invasion (3 cards pulled onto random stages, 4 attempts each) — stale.
- Void Chart: Star Talents from Plane Watchers (+ Path of Progression), Prime Star Talents from Travelers; 27
  constellations; the big nodes of gameplay constellations add that gameplay's Confusion Cards to the deck.
  Profound constellation (22 Prime): +25% Drop Quantity / -4 stage attempts, +12% additional Drop Quantity (costs 25
  Star Talents extra), -50% additional drop quantity but no prerequisites in non-gameplay constellations, 10% chance
  to not consume Compasses, rarer Confusion Cards, +1 card drawn (30%), etc.
- Plane Watcher Chest: not affected by Drop Quantity bonuses.
- **Drop quantity** [tlidb Drop_quantity page, Vlad]: Final expected quantity = base x (1 + sum of "Drop Quantity" bonuses)
  x prod(1 + each "additional Drop Quantity"). Quantity multiplies the number of drop INSTANCES only; each instance's
  amount/tier rolls independently (FE stacks 1/5/10/50; legendary tiers) and quantity never improves the roll. Not every
  gameplay reward scales (Cubes of Rapacity, Dream Bubbles, Chests of Folklores, Splendor Eggs...).
- Resonance -> Drop Quantity [Vlad]: 0:+15%, 1:+30, 3:+45, 7:+60, 15:+75, 31:+100 (run 31; 3.4 FE at 0.11 each).
- Card every map: pick 1 of 3 from the deck (Void Chart card nodes + timemark), +100% additional on top of the card's
  effect; ~1 reroll per 12 maps [Vlad]. "Stage attempts" = lives per map [Vlad].
- Slots [Vlad]: 4 compass slots, 1 Profound probe slot. Listing tax 1 FE per 8 (12.5%), nothing under 1 FE listable.
- No Profound beacon item: Profound T8 opens with the plane's T8 beacon (GA T8 3.3 FE); Deep Space Beacons (24 FE) drop
  in Profound T8 (tlidb), and the Beacon constellation can turn 10% of dropped beacons into them.
- Prices: Vlad confirms the CN list matches his server.

## etor label decoding (from the bundle)
- mapLabel: 0 ice (Glacial Abyss), 1 fire (Blistering Lava Sea), 2 steel, 3 thunder, 4 dark (Voidlands); 深空 Deep Space; 画雪 Frozen Canvas map,
  迷城 Mistville map, 万界 Myriad; dogmatic/tidecaller = boss fights. timeLabel: K1..K8 timemarks (9/10 = 8-1/8-2 ...), **12 = Profound (U8)**, 13 = Deep Space.
- Leaderboards hold 659 Profound runs (mostly day 2-4, before CN moved to Deep Space); avgEarnings is valued at the prices of the day
  the runs happened, so re-value loot from `/api/strategy/detail` with current prices before comparing.

- Scope [Vlad]: Profound T8 Glacial Abyss only. Cage (constellation + astrolabes) is Deep Space-only, never in Profound. Deep Space
  probes don't fit the Profound probe slot. 92 Star / 4 Prime are the cap. Beacons cost a T8 beacon per map unless farmed.
  Bare map 40 s, God of Machines +3 min; other mechanic times from the logged runs.
- `data/ext/void_chart_graph.json`: all 27 constellations with node positions, edges (from tlidb's svg), English + Chinese text and
  the etor key = md5("\n".join(Chinese lines)) — decodes the Void Chart allocation of any logged strategy.
- `data/ext/etor_strategies_s14/details/`: strategy details (loot / cost tallies, Void Chart keys) for the Profound runs.

- **Map base affixes** (torchcodex `mapAffix.html`, raw curl -> `data/ext/map_affixes_torchcodex.json`; tlidb has no pool): 175 affixes
  in three timemark pools (target 2 / 8 / 13); the Timemark-8 pool is 94 lines (77 at "ItemRarity" 0.15, 17 at 0.25 — the column is
  either the roll weight or the per-affix drop bonus, torchcodex doesn't say). The rare-monster **protective dome** ("proximity shield")
  is a MAP affix, two variants: "Upon receiving Projectile Damage, Rare monsters gain a protective dome with a radius of 5m (enemies
  outside cannot deal damage to targets in the dome)" and "Rare monsters have a 50% chance to gain a 5-meter radius protective dome".
  Nothing on tlidb/torchcodex ignores it. 31 resonance = 5 rolled affixes (1/3/7/15/31 = one more affix per doubling) -> a dome line
  on ~11% of maps; it is all-or-nothing per map, visible in the base-affix list before entering, and tlidb: "You may reset affixes on a
  map to avoid dangerous harmful affixes" (re-rolling costs the 31 resonance again = 3.4 FE; ~0.4 FE/map on average).
  Same pool, same counter: "-90% / -40% additional damage from attacks dealt from more than 6m away" (anti-ranged).
- **Replication stacking** [Vlad 2026-10-29, seen in game]: every "X% chance to be replicated once" source (compasses, probe, pets'
  once-lines, Creation's Fluorescent crystal 30%) adds into ONE chance capped at 100% (so at most x2); Kong's "replicated 1 time
  (20%) / 2 times (13%)" is rolled afterwards on each memory (x1.46). 4 and 6 memories from one drop are seen, never more.
  Consequence: once the once-chance is at 100% (Creation 30 + Colorful (Artifact) 50 + Sky's Dome 10 = 90, +anything), more
  "replicate once" sources do nothing; the Fluorescent Profound Probe is worth ~0 there.

## Tools (tools/farm/)
- `runs.py` loads the leaderboard entries + details, values loot at the latest price file (12.5% tax, FE untaxed), decodes trees.
- `features.py` per-strategy quantity multiplier Q (resonance curve, plunder compasses, probe, Profound/Commodities micros, x2 card),
  compass usage by family/tier, constellation points. `mech.py` compass -> mechanic. `groups.py` / `permech.py` grouped tables.
- `fit.py` ridge regression (too collinear to trust alone). `plan.py` Vlad-rescaled per-mechanic combos.
- `chart.py` tree-knapsack over a constellation graph; `hunting_plan.py` node values for the Safari compass farm.
- Quantity applies per gameplay as XD's pet matrix says (pet "+X% Drop Quantity" lines yes/no): see plan.py NQ_* sets.

## Result -> ss14/thea/farming_plan.md (2026-10-29). Questions: ss14/thea/farming_questions.md
