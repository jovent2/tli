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
- **His prices are the global server's** [Vlad 11-01], not etor's CN snapshot (a proxy only): 11-01 Transgression 39, Focus 6, Secrets 0.26 on
  the AH after tax (0.32 FE + 3 Flame Sand at the exchange). Ask for his price before a decision that hinges on one.
- **Drop quantity** [tlidb Drop_quantity page, Vlad]: Final expected quantity = base x (1 + sum of "Drop Quantity" bonuses)
  x prod(1 + each "additional Drop Quantity"). Quantity multiplies the number of drop INSTANCES only; each instance's
  amount/tier rolls independently (FE stacks 1/5/10/50; legendary tiers) and quantity never improves the roll. Not every
  gameplay reward scales (Cubes of Rapacity, Dream Bubbles, Chests of Folklores, Splendor Eggs...).
- Resonance -> Drop Quantity [Vlad]: 0:+15%, 1:+30, 3:+45, 7:+60, 15:+75, 31:+100 (run 31; 3.4 FE at 0.11 each).
- **His quantity sheet [Vlad 2026-10-31] and what his logs say about it** (`tools/farm/quantity.py`, 99 Colorful Machines maps):
  pool (adds): Path of Progression 30, Twilight Sparks 30, Kong 18, Sky's Dome 26 (Miss Melancholy - Pink 42), tree 25, Flourishing probe 20,
  resonance 100, Profound 100 (+ card 20/30) = +349% -> x4.49. Additional (multiply): Twilight Sparks 13 / 3, tree 12, card 100 (any Confusion
  Card), Drones 25 / 40, Cruising (A) 100 (Drones), Strength in Numbers 20 (Normal monsters, Drones included), Kong / Sky's Dome "+24% additional
  Fluorescent Memory Shards" each (unproven). Drone memories x75.6 (x49.2 if the FMS lines don't work), rare/chest memories x18.0. Profound also
  +65% monster quantity (not in the chain). Sources [Vlad]: Shadows only from Drones, ~99% of Secrets from Drones, ~95% of the big memories
  (Maud's, Tomorrow's, Lost Secrets, Crow's, Hundredfold) from rares or chests.
  - Pool vs "every line its own multiplier": +30% DQ card x1.07 (95% 0.87-1.33; sheet x1.067, own-multiplier x1.30), +20% card x1.02 (sheet
    x1.045 / x1.20), resonance 15 vs 31 x1.03 (sheet x0.944 / x0.875). Joint: the pool wins 10:1 to 33:1. +30% DQ = x1.067 = ~+4 FE/map on his
    non-Shadow loot (58.6 FE/map), each +10 points ~+1.3. Drone card (+10% additional Drones) x1.03 (sheet x1.10): can't tell.
  - Odd one: the "no bonus" cards (+20% compass DQ, +1 Blessed monster, +8% attack round, 12 maps) came out x0.76 (95% 0.61-0.95) — three
    4-map blocks (cards last 4 maps: Attempts 0/4) at ~50 Secrets vs ~72 around them; the chest / boss-memory cards (3 maps) were normal (x1.03).
    Against those 12 a 20% replicate card would be worth x1.49, impossible -> read as cold blocks, but watch it.
  - Shadows: XD's matrix (pet lines only, CN test branch) for plane-exclusive memories from Drones: pets' flat "+X% Drop Quantity" (Twilight 30,
    Kong 18, Sky's 26, Pink 42) and the "+24% additional Fluorescent Memory Shards" lines = no; Twilight Sparks' "+13% / +3% additional Drop
    Quantity" and every replicate line = yes. From the Creation Engine the flat lines apply too. Reading: Shadows from Drones skip the pool and
    take only "additional" lines (x10.95 on his sheet vs x75.6 for Secrets) -> a +30% quantity card does nothing for Shadows. Untested for the
    non-pet lines (12 Shadow drops in 99 maps).
  - **Working read per item (2026-10-31 evening, Vlad)**: Secret of the Glacial Abyss and Disappearing Shadow are **plane-exclusive** Fluorescent
    Memories (in-game exclusive drop list; tlidb files Secrets under "Drops everywhere"). tlidb: exclusive = plane-exclusive + gameplay-exclusive,
    and the gameplay-exclusive ones (Antonius's Help / Research, Clergy's Thinking, Concoction Recipe, Immortality Concoction Recipe) drop only in
    Path of the Brave / Creation Engine — so XD's "Gameplay Exclusive" column under Machine Drones can only be the plane-exclusive ones (the
    Drone tip and the Dull - Machine card: drones drop plane-exclusive memories). Hence, for Secrets and Shadows from Drones: **the flat
    "+X% Drop Quantity" pool does nothing, the Memory Shards lines do nothing, every "additional" line works, replicates work**, and Focus
    Fluorescent (+50% chance for exclusive memories) works (**wrong for Focus: CN etor data says x0.92, see "Focus does nothing" below**). The big memories (normal, rares / chests) take pool + generic additional + Shards.
    Chains on his sheet: Secrets / Shadows x10.95 (before Focus), big memories x18.0. Evidence: his first evening tally fits "Shards does
    nothing" (x1.10 vs x0.84); the DQ cards / resonance (x1.07 / x1.02 / x1.03) fit "no pool" and "pool x4.49" equally (1.1-1.3:1); Transgression
    (an additional for Normal monsters) moved Secrets x1.34. Confidence ~75%. Settling test: ~20 maps at 0 resonance (Secrets flat if no pool,
    -19% if pool).
  - With the 10-29 log (170 maps, Kong + Sky's on all): +30% DQ card x1.10 (0.89-1.35), +20% x1.07 (0.89-1.28), resonance 15 x1.045, no probe
    x0.99 -> no pool vs pool 2.3:1, still open. "+30% additional Drop Quantity for Drones" card (new, 14 maps) x1.22 (0.94-1.58; read x1.30),
    +10/15% x1.05 (read x1.10); Transgression for Strength in Numbers x1.42 (1.15-1.75). No pet contrast in it, so the Shards line waits for
    the Pink log.
  - **Per drone (log(drones) in the model, residual sd 0.37 -> 0.21)**: +30% DQ card x1.05 (0.93-1.18), +20% x0.99, resonance 15 x1.01
    (0.92-1.10), resonance 7 x1.30 (2 maps) -> **no pool on Secrets beats pool 11:1**. "+X% additional Drop Quantity for Drones" cards: +30%
    x1.23 (1.07-1.42), +10/15% x1.15 (1.02-1.29) -> additional works, ~9,500:1 over nothing. Transgression for SiN x1.62 (1.42-1.85).
  - **Settled 10-31 evening (Pink log, 218 maps)**: Pink for Sky's x0.976 (0.88-1.09) per drone vs x0.835 if pool + Shards applied -> Memory
    Shards off ~10^7:1, pool off 49:1 on Secrets. Fluorescent probe for Flourishing x1.055 (0.96-1.16). See docs/mechanics.md.
  - **Trial Drop Quantity is not Drone Drop Quantity** (2026-10-31, CN text via `tools/tlidb.py PAGE --lang cn`). English writes both as
    "...Drop Quantity during Trial: God of Machines"; the Chinese source doesn't. Trial lines name the trial as the owner: Void Chart +5% node
    "机械之神试炼额外 +5% 掉落数量", +7% node "每当新回合开始，机械之神试炼额外 +7% 掉落数量" (per round), +6% node, the Drones node's
    "机械之神试炼额外 -100% 掉落数量", Conservative - Machine card +10/15%, Brilliant / Cruising compass "机械之神试炼的掉落数量额外 ±100%"
    (the trial's drop quantity; same possessive as Strength in Numbers' "普通怪物的掉落数量"). Drone lines name the drones: "机械之神试炼中，
    无人机额外 +X% 掉落数量" (Cruising +100, tree +25 / +40, Obtuse - Machine cards +10/15/30). Proof that the trial lines miss drones: he runs
    Cruising's -100% and still gets ~70 Secrets/map from drones, and additional lines multiply (x0 if it applied). So +5% / +6% / +7% /
    Conservative only scale the trial's own reward (the statue loot), which Cruising (and the Drones node) already multiply by 0: dead for him.
    Grammar (CN): scope = 期间 / 中 ("during" / "in"), owner = the noun before 额外 +X% 掉落数量 (no noun = everything: "异界关卡中，额外 +12%
    掉落数量"). The +7% = trigger 每当新回合开始 + owner 机械之神试炼. God of Might's tree has the same per-floor mechanic as two separate nodes,
    trial ("巨力之神试炼额外 +4%", EN "during Trial: God of Might") and automatons ("矮人机甲在试炼范围内额外 +4%"), and EN writes the same
    construct as "for Trial: God of Might and Dwarven Automatons" on the +5% node: the English "during" carries nothing.
  - **Focus does nothing measurable on plane-exclusive memories** (2026-10-31, `tools/farm/compass_fit.py` on the CN etor leaderboards:
    202 drone strategies, 19,458 logged runs, mostly Deep Space). Secrets x0.92 (95% 0.80-1.06; clean subset the same), Immolating Flame x0.92
    (0.69-1.23); the tooltip's x1.5 is ~9 se out. The same fit sees the replicates as advertised: Colorful (A) x1.33, Fluorescent Deep Space
    Probe (40%) x1.40, Colorful (20%) x1.03 (0.88-1.21). CN meta: 177 of 202 drone strategies run Transgression + Strength in Numbers +
    Cruising (A) + Colorful (A) (+ Fluorescent probe); 9 run Focus. Same-family compasses stack (Sinful (A) + Sinful in 212 strategies,
    one strategy runs Colorful (A) + Colorful every map). His two no-Focus test maps (Transgression + SiN, no Colorful / Kong / Sky's): 77 and 70.
    His own logs agree (11-01): Transgression vs SiN with Focus on both sides x1.44 (-> Transgression x1.73 with SiN x1.2); Transgression
    added with Focus removed x1.74 -> Focus ~x1.00 (at most x1.09 even if Transgression sat at its x1.9 cap).
  - **Shadows and Transgression** (11-01, corrected twice the same night). Official rule (tlidb Drop quantity, examples 1-5): quantity
    = more independent rolls of the same drop (+100% on a 50% drop -> 25% none / 50% one / 25% two), so on a rare item it makes the
    drop happen MORE OFTEN; pile size comes from replication. Vlad's ETor tally: Transgression + SiN 50 Shadows in 161 maps (0.31/map)
    vs Focus + SiN 42 in 194 (0.22/map) = x1.44 (x1.77 without a 0-in-30 day) — fits the x1.74 Secrets take. His logs, drop events
    (a drop + its copies = one): Focus + SiN 29 in 202 maps (0.144/map; 18 in 167 = 0.108 without a hot 10-29), Transgression + SiN
    6 in 31 (0.194/map, 3.5 Shadows each) = x1.35; Transgression replacing SiN (Focus kept) 4 in 43. Expected on the current setup:
    ~0.19 drops/map (one per ~5 maps; x1.74 on a ~0.11 base). My two reads that night ('no Shadow boost, 700:1' and then 'bigger
    piles, same drop rate') came from 10 vs 33 drop events in the logs: noise, both wrong.
  - **Transgression stacks**: +3% additional per Rare killed, cap 30. Rares spawned before the trial (log, rarity-3 'Monster Created'):
    median 28 on his Transgression maps, 30+ on 12 of 33 tonight; median 41 by trial end -> ~x1.8 entering the trial, x1.9 during it;
    measured x1.74 (95% 1.57-1.93). Starting the trial after the 30th rare is worth ~+3% on drone loot.
  - Big memories are too rare to measure quantity (0.68 drops/map: +30% card 0.50/map, +20% card 1.11/map); Shadows 0.12/map.
  - Naked rates (no quantity, no copies): Secrets 0.33/map from Drones (0.51 if the FMS lines don't work), big-memory drops 0.037/map.
  - Transgression in place of Strength in Numbers (+ no Flourishing on 7 of 8): Secrets per copy x1.34 (95% 0.99-1.81).
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
- **Replication (fitted 2026-10-31, `tools/farm/replication_fit.py`: 88 rare-memory drops on Machines maps + Secrets on 107 Colorful Machines
  maps, 10-30 + 10-31 logs; drop pets per map from the area dump, probe from the cost)** — replaces the 10-29 rule "once-chances add up, cap 100%".
  **Every "replicated once" (Kong's 20% included) rolls on its own and every hit adds its own copy**, no cap, P(no once-copy) = prod(1 - p);
  **then Kong's "13% replicated 2 times" rolls on every copy** (x3). Memories per drop = (1 + sum p) x 1.26.
  - Rare-drop sizes kill add-up (5.5 drops of 1 predicted of 88 on Colorful maps, 24 observed) and "roll in order, stop at the first hit" with
    Kong's 20% in the list (Vlad's 10-31 read: a drop is then 1 or 2 copies before the x3, so 1/2/3/4/6 only; observed 6 fives and 3 of 7+, and
    13 threes vs 6 fours where it says 8 vs 19). They don't separate every-hit-a-copy from biggest-only; Secrets/map does: the engine's random
    Fluorescent crystal raises Secrets x1.18 (95% x1.02-1.35, stratified by setup and card) — predicted x1.00 biggest-only, x1.06-1.09
    stop-at-first-hit, x1.15-1.19 every-hit. Joint: every-hit (Kong 20% in the list) -521.5, Kong 20% per copy -522.6, stop-at-first-hit
    -525.1 (Vlad's exact placement -538.8), biggest-only -526.3, add-up -686.6. Confidence medium-high.
  - Sizes 1..7+ of the 88 Colorful-map drops: observed 24/32/13/6/6/4/3, every-hit 19/30/17/11/7/2/2.
  - Refit with the 10-29 log too (Vlad's 1.3 GB backup; 52 Machines maps on the Fluorescent probe): 196 rare drops on Colorful maps, sizes
    47/64/40/20/12/4/9 vs every-hit 39/62/38/27/17/7/7. Joint: every-hit -981.3 (Kong 20% in the list; per copy -981.8), stop-at-first-hit
    -1013.8 at its best placement (-1107.6 Vlad's exact read), biggest-only -1015.9, add-up -1554.5. Crystal on Secrets x1.15 (95% 1.06-1.25).
  - Data: 98 rare drops = 240 items (Maud's 134, Tomorrow's 39, Shadow 27, Lost Secrets 22, Hundredfold 17, Crow's 1) on 127 maps, every
    PickItems block checked; the fit keeps the 88 on Machines maps (Vigil maps replicate through Lady Obituary's Elegy: Maud's x3 / Tomorrow's x3
    on an Alert Outlaw + Phantom Vigil map with no Fluorescent source). Secrets (7,600) come as ~1,500 sweeps of piles (13-17 pickups/map, mean
    4-5), so a pickup is not a drop; with the crystal the pickups per map stay ~13.5 and get bigger (mean 4.2 -> 5.2): copies, not extra drops.
  - Drop pets change between farms (gamelog m["pets"]): Machines = Kong 8130 + Sky's Dome 8120 (+ Twilight Sparks, Miss Melancholy - Azure,
    Lady Obituary, Heartbloom - Iris, Twin Inquisitors); a few Machines maps ran without Kong/Sky's (Benign Bug / Doro-Doro, Divinity pets).
  - His Machines stack (Sky's Dome 10 + Kong 20 + Colorful (A) 50 + crystal 30 on 79% of maps): 2.04 copies before the x3, 2.57 memories per
    drop; 22% of drops end as a 1 with everything on — variance, not a dead buff. Memories 83.5 FE/map (Shadows 50, Secrets 29.4 at the
    exchange): +10% of replicate = x1.049 = +4.1 FE/map; Melancholy 30 / 20 card +12.3 / +8.2.
  - `bottomup.py` still caps replicate sums at 100% (the old rule); it only matters where a strategy's lines pass 100%.
- **Catalyst Creation Engine** runs in the first 2-12 s of most Machines maps: `gameplay type 7602 received notifyId 104 / 101 / 103 / 102`; the 102
  NotifyData holds the two activated crystal codes (15001 / 15002 / 15003; some maps get a second round). gamelog.parse -> m["catalyst"]. **15003 is
  the Fluorescent crystal**: buff "Fluorescent memories dropped have a 30% chance to be replicated once" [Vlad: binary, two picks = one buff, the
  engine picks]; the buff line itself is not in the log, only the activation (tlidb's "Drop Quantity Bonus" wording is wrong for this one). Secrets/map
  56 without / 71 with (no card); two picks 79 vs one 68 (+15% ± 12%, not separable). 15001 / 15002 don't move Secrets. (A 10-31 read here called
  it drop quantity: that came from testing it under the add-up rule.)
- How a drop looks in the log: one pickup = one ground stack: `ItemChange@ Add Id=6216_<guid> BagNum=3` is a Shadow drop of 3. The once-copy is
  sometimes its own ground item, picked 0.2-0.4 s later (10-30 13:02: Shadow x3 then x2, 245 ms). A pickup can sweep several ground items
  (1/3 of PickItems blocks hold more than one item type), so x5-x7 Maud's are likely two drops. Drop-spawn lines (`UDropInstanceMgr@
  AddInstance`) carry no item id.
- **Void Variables** = map-entry effects 61000xx (6100001/10/12 +1/3/8 blessed Rares, 6100002/11 +2/5 Disciple groups, 6100003/4 Magic / Rare
  Treasure Sentries, 6100005 monsters on a larger scale, 6100007 Rift Portal chance, 6100013 +1 Calamity Warlord, 6100006 landmines,
  6100009 artillery barrage; the last two have no text, named from their sound cues: 26-40 `Minecave_Landmine_Blast` a map vs ~3, and 284
  `Mountain_PaoJi_Explosion_Hvy` (炮击, bombardment) in its one map and none in any other = tlidb's "wall cannons" variable). His
  10-29..10-31 Machines maps: 0.38 per map (63 of 196 maps); with vs without: non-drone loot median 25.5 vs 24.2 FE, FE drops 15.8 vs 15.9,
  Secrets per drone 0.98 vs 1.00 -> no measurable value on a drone farm (they add rares and packs, not drones).
  Spread (255 stack maps): 180 none, 62 one, 13 two, never three; 0.34 / 0.35 / 0.38 per map on 10-29 / 30 / 31. Per 100 maps: Rare Treasure
  Sentries 6.7, +2 Disciple 5.5, larger scale 4.7, Magic Treasure Sentries 3.5, +1 blessed 3.5, Rift Portal 2.7, +3 blessed 2.7, +5 Disciple
  2.0, 6100006 1.6, Calamity Warlord 0.8, 6100009 0.4, +8 blessed 0.4. Non-drone loot (winsorized at 91 FE; baseline 29.7) per type on Machines
  maps: Rare TS +6 (16 maps; big memories 5.2 vs 2.0), +2 Disciple -7 (12), larger scale +8.5 (10), Magic TS +4 (8), +1 blessed +7.5 (7; big
  memories 9.9), Rift +7 (4), +3 blessed +15 (6), +5 Disciple +2.5 (5), 6100006 +5 (4), Calamity Warlord +32 (2), 6100009 -16 (1).
  Average ~+3 FE per variable (± 3.4) -> ~1 FE/map now; the VV node adds ~1 per doubling of the rate.
- **Map-entry effect dump**: at map entry the log lists every active effect ("+Id [..]" + "+Description [..]", field order varies per launch):
  compasses (Colorful (A) 215803, Focus 215802), Void Chart nodes, resonance affixes, and the **Confusion Card** picked (7xxxxxxx: Melancholy
  71090100 = 20% / 71090110 = 30% replicate, 71100200/71100210 = +20/+30% Drop Quantity, 72020400 = +10% Drones ...). `gamelog.parse` stores
  them as m["effects"] / m["card"]. Pets are in the join dump (`+servantId`, `+starLevel`): his Machines maps all ran Kong (8130) r5,
  Cloudgatherer - Sky's Dome (8120) r5, Twilight Sparks (19330) r5. The Fluorescent crystal's 30% buff is not in
  the dump (granted after entry): read it from the 7602 lines.

## Tools (tools/farm/)
- `runs.py` loads the leaderboard entries + details, values loot at the latest price file (12.5% tax, FE untaxed), decodes trees.
- `features.py` per-strategy quantity multiplier Q (resonance curve, plunder compasses, probe, Profound/Commodities micros, x2 card),
  compass usage by family/tier, constellation points. `mech.py` compass -> mechanic. `groups.py` / `permech.py` grouped tables.
- `fit.py` ridge regression (too collinear to trust alone). `plan.py` Vlad-rescaled per-mechanic combos.
- `chart.py` tree-knapsack over a constellation graph; `hunting_plan.py` node values for the Safari compass farm.
- Quantity applies per gameplay as XD's pet matrix says (pet "+X% Drop Quantity" lines yes/no): see plan.py NQ_* sets.
- `gamelog.py` per-map loot/cost from his game log (+ effects, card, catalyst crystals, drop pets); `replication.py` / `replication_fit.py`
  Fluorescent replication rule fit (rare-drop sizes + Secrets/map); `quantity.py` his quantity chain and the in-log quantity experiments.
- `killspeed.py` drone lifetimes (spawn -> death, FIFO) vs Secrets / Shadows per drone, per map.
- `compass_fit.py` what each compass / probe does to one loot item across the etor strategies (WLS on log item/run, robust CIs;
  default population: drone farmers = Cruising (A) on >= 50% of runs; `--item`, `--clean`, `--all`).

## Bottom-up model (2026-10-29 late; tools/farm/bottomup.py, plan2.py, search.py) — the one to use
- `attrib.py` / `model.py`: first passes (lift per mechanic, family-level NNLS) — superseded, kept for reference.
- `bottomup.py`: each CN strategy -> instance columns = every compass/astrolabe key it consumed per map (one column per key:
  Revelation vs General Hunting are different products), mechanics forced by appearance nodes (`tree:<M>`), and `generic` (the
  plane's own monsters). Per column and strategy the multiplier its setup gave that channel: generic pool (resonance curve,
  Profound 30%/12% + micros, Commodities micros, Sinful compasses, Flourishing probe) x 2 card — only where XD says quantity applies
  (NQ: Vorax, Sandlord, Mistville, Frozen Canvas, Overrealm, Disappearing Shadow); the mechanic's "+X% additional" nodes and compass
  lines (`ADD_RULES`, incl. instance-count nodes: echelons, attack rounds, Safari bosses, Creation engines, Vorax groups, Might
  levels, Dark Surge corrosion); class multipliers: compass drops (Compass constellation 1.4%x37, +4%, +2.5%/compass inserted,
  Ecliptics, Compass probe, replication), fluorescent replication (capped sum — old rule, see Replication), Focus x1.5 on exclusive memories (wrong: ~x1.0, see Focus below), ember lines
  (Might's only on Might columns), Gear probe; Transgression x1.9 on Machines, x1.54 on generic. Then NNLS per item (rows weighted
  by sqrt(runs)) -> naked yield per instance with every multiplier at 1. Items with < 25 drops in 46k runs are lotteries: valued at
  the shrunk observed rate per column (>= 5 drops there) or globally.
  In-sample: weighted R2 0.78 on per-strategy gross, median error 18%, family means within ~10-30%.
- `plan2.py`: `Plan(compasses, probes, nodes)` evaluated at Vlad's constraints: re-applies his multipliers, prices at today's list,
  cost = beacon + 31 resonance + compasses (x0.9 with the Profound refund node) + probe, time = 40 s + per instance (his: Machines
  180 s, Might 180 s, Hunting ~10-35 s, War 5 s; CN-fitted otherwise, floor 10 s). `best_tree` = chart.best_subtree per
  constellation with linearized node values + knapsack over the budget split (92 - 25 Star; Profound 4 Prime fixed).
- `search.py`: greedy over compass slots / probe with the tree re-optimized per candidate; one gameplay compass per family.
- Not modeled: pets (not logged by etor -> yields carry CN's pets; Vlad's assumed comparable), the card pick itself (x2 assumed every
  map), compass "more valuable type" nodes, Creation crystal choices, Clockwork rating/time play, anything a second same-family
  compass adds on top of the first.

## Result -> ss14/thea/farming_plan.md (2026-10-29). Questions: ss14/thea/farming_questions.md

## In-game notes from Vlad's runs (2026-10-30)
- Afterlight: Grief's "Phantom Flames" trail on the ground does nothing to him; **White Night Mode spawns Weeping Osil, which hits
  very hard (no number on the node)**. Phantom Afterlight: the phantoms must be escorted to the front of the procession for the next
  one to spawn — done right it is 3 chests per Vigil.
- Outlaw: there is no vehicle "cache"; all Carjack mods drop from the Security personnel mobs. First 20 maps with the Warlock /
  Vanguard nodes: 1 Warlock, 0 Vanguard, 4 Tank, 3 Sniper (CN mix would be ~70% Warlock+Vanguard) — open question.
- Machines (Cruising): the echelon nodes are the drone source; CN's logged trees are his tree.


## 2026-10-30 — the column model failed on the stack (lesson)
`bottomup.py`/`plan2.py` predicted 202-219 net/map for Alert Outlaw + Bandit + Phantom + Lunaria; Vlad's 25 maps gave ~25 non-lottery and
the only CN Alert+Bandit stack -21. Cause: per-compass NNLS columns share items (FE, resonance, embers), each column is evaluated at the top
CN multiplier (x1.2 cap), and the top-multiplier CN strategies are already over-predicted in-sample (linear-in-multiplier fails at the top:
drop quantity does not scale the fixed-count drops like mods/remnants). Run-weighted obs/pred over 629 strategies = 1.5, R^2 < 0 (the 0.78
reported earlier was per-column with shared items double-counted). Rule from now on: **rank plans on raw CN strategies with the same compass
set (`runs.py`, run-weighted net/map and s/map), and on Vlad's own game log (`gamelog.py`)**; use the column model only for marginal
questions inside one mechanic (which tree node, which card), never for cross-mechanic FE/min.

## Game log (`tools/farm/gamelog.py`)
TLI writes `<drive>:\TapTap\PC Games\TorchlightInfinite\UE_game\TorchLight\Saved\Logs\UE_game.log` (+ `UE_game-backup-<date>.log`
rotations); etor reads the same file. Per map: `ItemChange@ ProtoName=Spv3Open start/end` lists what the map cost (beacon 400007, compasses
by item id, probe, resonance 5028) -> a stack map is identified by its cost signature; `_JoinFightSuccess()` followed by `+maptype [Mystic]`
= entered the map, followed by `+checkType [MainCity]` = back in town (map end); `FightResult@ Open FightFailureView` = a death (he revives
and continues); `PickItems` blocks = loot, by stack guid deltas. Keep the raw log out of the repo (account ids).
- 2026-10-31 log format: the area dump after `_JoinFightSuccess()` prints `+mapId` BEFORE `+maptype` (10-30: after). The parser stopped at
  mapId, never saw the entry, and counted everything up to the next map open as loot (AH/prism crafting in town, the Secrets exchange: +681 FE of
  phantom loot on 16 maps). Fixed: the join block is read until `+maptype` / `+checkType [MainCity]` in any order (3,000-line limit).
- Town blocks seen: `Push2` = NPC exchanges / crafting results (Fluorescent Memory sets at the Spacetime Wanderer, prism levelling),
  `ExchangeItem`, `XchgForSale` (listing), `XchgBuy` / `XchgReceive` (AH). Only in-map blocks count as map loot.
- The season board's final map (`+maptype [S16FinalMap]`, mapId 344; board UI lines `S16Board*`) is entered from town with no Spv3Open, so
  gamelog.parse opens no map for it and its loot is outside every per-map number: 33-56 s a run, 64-283 FE (Flame Elementium 116-201 + Flame
  Sand, embers, compasses, a few memories). 10-30: 6 runs = 1,217 FE; 10-31: 1 run = 240. Its memory drops are left out of the replication fit.
- **Machines trial in the log** (gamelog m["machine"]): `FightMgr@ShowMachineTitleStart` = he opened the machine, one
  `ShowMachineTitleLevelInfo` per attack round (3; 4 when the extra round procs: 39 of 170 maps), every drone spawn / death plays a sound
  (`..._Small_Drones_Appear'` / `..._Mechanic_Drones_Die'` requested-row warnings), `God_Machinery_MonAtk'` per statue hit, `God_Machinery_Succ'`
  = done. 10-29..10-31: 78 drones per map (12-194; 72 on 3 rounds, 101 on 4), ~95% of Secrets picked between start and success (Vlad: 99%
  from drones). Drone kills explain 53% of the map-to-map Secrets spread; standard maps 0.85 Secrets per drone (naked ~1.9% per drone before
  copies x2.66, additional x10.95, Focus x1.5); Shadows ~2 drops per 1,000 drones.
- **Drone kill speed vs loot** (2026-10-31, `tools/farm/killspeed.py`, 25,692 drone deaths in the 10-29..10-31 logs): drones are
  NpcId 1052033 ("Drop Prop Debug:create monster NpcId=1052033,eId=...", rarity 1); deaths have no id, so lifetimes pair FIFO. No drone
  dies before 1.97 s (fly-in floor); 36% die within 2.5 s, median 2.7 s. Per map (222): Secrets per copy per drone x0.98 (0.84-1.15) going
  from 0 to 100% fast kills, x1.03 per extra second of median lifetime; Shadows per 1,000 drones 1.05 / 1.74 / 2.71 from the slowest to
  the fastest third. Killing fast costs nothing. `UDropInstanceMgr@ AddInstance!` = ground drop instances (0-0.3 s after a death, 62 per
  trial, corr 0.79 with Secrets) but they merge when many drones die at once (0.08-0.12 per death in 9+ bursts vs ~0.4 alone), so an
  instance count per kill looks like 'fast kills drop less' when it's only AoE merging piles.
- **Cruising airships** (2026-11-01): Airship Station [tlidb, CN] "触碰即可召唤飞空艇；击落不同品质的飞空艇，将生成对应数量的无人机梯队" — touch
  to summon an airship; shooting down airships of different 品质 (rarity tier) spawns that many drone echelons; nothing about time.
  Log: drone (1052033) spawn bursts are 4 (76%), 12 (17%), 8 (3%), 16 (1-2%) = 1-4 echelons of 4. Cruising-only units: 1052100-1052103
  (rarity 4, ~3.4 per trial, two at a time ~8 s into a round, then 'Drones_Call' / 'Drones_Airdrop' sounds) = best read for the four
  airship tiers (~60%); ids never change after spawn. 105220x (1052200 r1, 1052201/2 r2) come in bunches of 4-16. Deaths have no ids,
  so airship -> drones can't be linked. Kill-speed thirds: same burst mix (4: 76/75/77%, 12: 17/18/17%) and drones per map (77/78/80),
  so no sign that slower kills roll better airships at 36T speeds; a 6+ s airship lifetime is untested (test: drones per round on maps
  where he lets airships live 6+ s).
- Drop-pet block: the first pet sits on the header line (`+dropServantContractData+1+servantId [8130]`) and the order changes between
  joins; until the 10-31 fix the parser dropped that first pet, so 10-29 looked like Kong / Sky's Dome swapping every map. They were on all of them.
- The join dump also lists the active drop pets (`+servantId [..]` with `+starLevel`); compare them across maps before blaming a setup change.
  Backup logs (`UE_game-backup-<date>.log`) hold whole launches (10-30: 1.1 GB, 18 h, parses in ~25 s).
- **Fluorescent Memory exchanges** (Spacetime Wanderer): Secret of the Glacial Abyss 30 -> 10 draws of 10 Flame Sand or 10 FE. All his turn-ins
  10-29..11-01: 23,865 memories (22,968 Secrets); Secrets-only sessions 6,024 Secrets -> 1,910 FE + 17,970 Flame Sand = 99 units per 30, FE on
  9.6% of 1,988 draws (95% 8.3-10.9%) -> **0.32 FE + 3.0 Flame Sand per Secret** in `gamelog.EXCHANGE` (AH 0.3, 0.26 after tax). The first read
  (24 exchanges, 12.5%) said 0.417. Other recipes seen: 5 Disappearing Shadow -> Blueprint: Lone Walker's Boots (35 Shadows turned in),
  War Compass x30 and Ultimate Ember x11 from other memory sets. Flame Sand: 73,200 spent on 10-30 for 244 of item 101300 (300 each; not in
  etor's table, unknown) — no FE value assigned yet.

## Deep Space ranking (`tools/farm/deepspace.py`, 2026-10-30)
Raw etor strategies (timeLabel 13) grouped by the compass/astrolabe/probe set they ran (qty >= 0.5/map; beacon and resonance excluded
from the key) and by the constellations in the talent label; run-weighted loot and cost at today's prices; items with < 8 drops in the
whole group are "rare" and shown separately. Crawl: `etor_fetch.py details --time 13 --exclude 囚笼,狩猎` (day stages only; week-board
keys 404 on /detail). 2026-10-30 ~16:00: 908 strategies / 113k runs decoded.
- **Bug fixed 2026-10-30**: `runs.py` priced Flame Elementium at 0 (no FE row in the price snapshot), so every raw-strategy net before
  this (Profound corrected table, Deep Space first cut) was short by the FE drops: 13-100 FE/map. Order of the ranking unchanged.
- etor's talent list skips some on-path nodes (card nodes like Irritable - Might, the "+7 groups" mediums in Commodities, Compass #12):
  `draw_tree.realize()` adds the path; a CN "巨力×22" is 35 real points.
- Deep Space results (FE/min, steady, CN seconds): Ember/Might farm 77 (1 player, 124 runs, 86 s); Machines (Cruising (A) + Colorful
  Fluorescent (A) + Transgression Plunder + Strength in Numbers + Fluorescent probe) 54-66 over ~5,000 runs at 83-112 s, cost 139;
  Doll compass farm 43-51 over 25k runs at 117-123 s, cost 270-350; Alert Outlaw stack (All-Evil Vigil + Generous Elite + Sinful (A))
  48 over 2,477 runs at 99 s (100 FE/map in raw FE), median player 30. Profound with FE counted: Machines 51-60, Safari ~50 (+rare).

## Deep Space scan 2 (2026-11-06) — tools, rules and what the logs taught (`tools/farm/ds_scan.py`, `etor_refresh.py`, `trends.py`)
- **etor is the global market** [Vlad 11-06]: its prices are his prices and its leaderboards hold EU/NA/CN players alike (the site is
  just in Chinese). The week boards (`stage=week1..3`) now return `/strategy/detail` (tested 11-06); `deathCount` on every board entry
  = deaths over the entry's runs (Deep Space week2 median 3.7 deaths a run). `etor_refresh.py all --stages week3,week2 --charts ...`
  = prices snapshot + trend board (`/strategy/windboard?stage=`, 4,769 recipes, `compat|time|clusters|items` keys, heat) + boards +
  details keyed by board + `/chart/<season>/<item>?interval=1d` price history (no `success` field; FE has no history).
- `ds_scan.py`: strategies from the freshest board first (week3, then week2), re-valued at the latest price file, grouped by compass /
  astrolabe / probe set (+ DS resonance bucket) and talent family (sorted set); steady vs lottery (< 8 drops in the group), deaths/run,
  median player and top third, `tank` = monster HP multiplier from the compass lines alone (life x / damage-taken), 7-day value-weighted
  price trend of the group's steady loot, and net/min at Vlad's seconds (`VLAD_S`: Overrealm loop 209 s, Alert stack 124 s, Machines
  200 s; else CN x1.2). `--all` keeps Cage / Doll / Might / Machines (incl. the 机械 tree) groups; `--show N` prints one group's players.
- **XD matrix read as loot classes** (`servant_affixes` x `effects[play][branch][loot]`, rank 6, `data/ext/pactspirit_loot_classes.txt`
  for the full table). Per loot type the pet lines that work: flat "+X% Drop Quantity", "+X% additional Drop Quantity" (generic),
  typed additional ("+X% additional <type> Drop Quantity"), replication. Pets are the only lines XD lists, so compass / tree lines are
  mapped to the same classes by analogy (an assumption, ~80%). Results for his mechanics:
  - Outlaw Security personnel (fuel, Sand, fossils, mods, memories, TOWER tokens, legendary gear): flat yes, additional yes,
    replicate some. **Bounty Chests: nothing scales** (fixed count).
  - Afterlight / Vigil (fuel, Nether King's Divinity, Divine Remnant, compasses): flat yes, additional yes, typed partly, replicate some.
  - Overrealm: the normal Overrealm (fuel, prisms, prism material): flat + additional. **The "endgame" Overrealm loot (fossils,
    legendary / precious gear, prisms, special prism, memories, Sand) ignores quantity entirely; only replication (Key of Overrealm).**
    tlidb: "The drops in the Overrealm are not affected by any Pactspirits other than Overrealm Pactspirits"; the Overrealm inherits
    timemark, resonance, some probes, compasses and talent bonuses from the stage.
  - Goddess of Hunting: the goddess's compass / astrolabe loot ignores quantity (none 64/65); Safari-boss (invasion) compass loot
    scales flat + additional; emblems / exclusive legendaries scale.
  - Lunaria: everything scales (flat + additional). Sandlord spice / probes: nothing scales. Mystery Chests: fuel / Sand / memories /
    legendary gear scale; exclusive legendaries don't. Gods Chest: additional only. Vorax, Frozen Canvas, Mistville: nothing scales.
    Machines drones: exclusives additional-only (as measured). Dark Surge: fuel, corrosion, legendary gear, tickets scale.
  - Type-specific lines ("+X% additional Fluorescent Memory Drop Quantity", "+X% Fuel Drop Quantity") are their own additive pool
    applied to the item count of a drop that already happened: bigger piles, never more frequent drops [tlidb
    Drop_Quantity_Bonuses_for_Certain_Item_Types, examples 1-3].
- **Deep Space's own bonus**: the map-entry dump carries effect 106 "+200% additional Drop Quantity" on every DS map (x3 on everything
  that takes additional), beside Profound's pool. DS resonance: 2 consumed = 1 affix = +15% additional [Vlad]; CN runs 2.7-3.2 a map.
  Lives in DS: 6 (2 with the +25% / -4 attempts Prime node) [Vlad].
- **His 11-05/06 logs (47 maps, `/home/claude/work/log8/`)**, today's prices:
  - Evernight Vigil + Shadow Overrealm + Generous Elite + Sinful Plunder + Flourishing DS probe (25 maps): gross 226, cost 110,
    net 116/map; map 209 s median, town gap 7-30 s normally (median open-to-open 301 s includes breaks); deaths 0.48/map.
    By phase (`phases.py`): pre-Overrealm map 54 FE (FE 22, fossils 12.6, Remnant 7), **Vigil 56 FE in 19 s** (Remnant 0.36 = 22,
    FE 12, legendary remnants), inside the Overrealm floors 10 FE, **after the Overrealm 102 FE** = mostly the exit reward dump 4-17 s
    after it ends (FE 63, Sprout of Legends 0.16 = 19) plus the rest of the map. Floors reached 1 / 2 / 3 / 4 on 7 / 12 / 6 / 1 maps
    (advance 72% -> 37% -> 14%); ~42 s a floor; gross by floors 142 / 234 / 288 / 155 (the 4-floor map had 3 deaths).
    Markers: Vigil = `GAMEPLAY_ENTER ... GameplayType=8100` -> dialogue "We have delivered the soul"; Overrealm = "Switched to another
    pact configuration plan (Overrealm)" (a separate pact config switches in at the door) -> `Stop_Mus_Gameplay_S12_Ov`;
    floors = `LevelMgr:_FastEnterLevelSuccess()` count - 1 = `S12RewardRuneTitleTips` count (one rune per floor).
  - Alert Outlaw + All-Evil Vigil + Generous Elite + Sinful (A) + Flourishing DS probe (20 maps): gross 152, cost 211, **net -60/map**
    at 124 s, deaths 0.65/map. Outlaw + map 125 FE (FE 61, Vanguard 0.65, Warlock 0.10, Tank 0.40, Sniper 0.35), Vigil 26 FE
    (Remnant 0.25, FE 5.85). CN same setup (+3 DS resonance, 7 players, 720 runs): gross 323 (FE 116, Remnant 0.93, Warlock 0.95,
    Vanguard 0.46), net 101 at 103 s, 4.2 deaths a run; worst CN player 24/min.
  - **Fright stacks = 0 for him** (85%): CN Alert + Evernight gets Remnant 0.46 vs All-Evil 0.93 (x2 = Fright x4 vs Evernight's built-in
    x2); his All-Evil 0.25 vs Evernight 0.36. The three Manifestations are the three rarity-4 units (NpcId 2993000) created at Vigil
    start on every map; no death marker for them; his Vigil lasts 19 s. Evernight's "+100% additional Drop Quantity for the Vigil" is
    effect 211910 in the dump; All-Evil's Fright text is there too but no runtime Fright events are logged.
  - **Warlock**: with both "more likely" nodes CN gets Warlock 0.78 / Vanguard 0.57 a map (124 players, 9k runs; Warlock 35-45% of mods
    for nearly every player, no hero effect); without either 0.44 / 0.33. His 10-30 + 11-05: 3 Warlock in 38 mods (8%) — unexplained.
    Mods scale with quantity: 0.17/map on Profound 10-30 -> 1.5/map in DS (x3 + Sinful (A)).
  - Outlaw walkthrough [Vlad]: stand still, nexus spawns at 15 / 25 / 35 kills and dies at once, over at 50 kills; mods drop in the
    first ~10 s of the Outlaw (gameplay types 7001 / 7011). Security personnel ids 2951xx-2953xx (rarity 1-3), ~500 spawns a map.
  - Overrealm tree: the +3/6/10% (with monsters take -10/-20/-30%), attempts -1/-2/-2 and time -3/-4/-5 s mediums only scale loot
    dropped inside the floors (~10 FE/map); the two "+50% chance of advancing to the next level" mediums (depth 5 each: 4 micros +
    node; Restrained card node behind one) are what moves floors. No CN player takes them (70 of 75 Overrealm players run Containment,
    whose keys force the doors). tlidb: entering level 3 or 4 guarantees an extra Bottled Shadow (a reward affix for one round).
- Price trends 10-16 -> 11-06 (`trends.py`): Nether King's Remnant 70.8 (+4%/7d, +41%/14d); Warlock 66 (flat); Sprout 141 (flat);
  Sacred Fossil 8.0 (-20%/7d, -37%/14d); UE 16 (-26%); Immolating Flame 81 (-34%); Blueprint Eternity 2,542 (-29%); Shadows 183
  (-19% vs 10-30); Secrets 0.30 flat. Compass costs rising: Alert 37 (+19%), Evernight 21 (+14%), Generous 17.5 (+6%).

### Checkpoint 1b (2026-11-07 02:40) — `tools/farm/model.py` = checkpoint 1 + pets per phase, `data/ext/model/checkpoint1b.md`
After checkpoint 1 the session was compacted; the pet fix was done as a rewrite (`model_cp2.py`) that also brought in an FE split
(generic + mechanic), a refit rule for unidentified exponents and a generic-item treatment, then a simulator (`strat2.py`) and a tree
search (`tree2.py`) with text-priced guesses (Strength in Numbers / Transgression, Profound +12% at 27 pts) on top. Vlad called it:
the ranking's top was driven by the guesses. Parked. The line to continue from is checkpoint 1b: checkpoint 1's code with only the
agreed pet change (3 regular pets + special slots; Fuel trio all map, Outlaw trio in the Carjack; replicates and fuel lines per the
matrix). Exponents and free effects identical to checkpoint 1; only the bases moved. Findings from the parked branch worth re-testing
one at a time, each as its own labelled step with a before/after: (1) Outlaw tree lines do not move whole-map FE (linear check: exponent
0.02±0.11, DS resonance 1.03±0.13); (2) Generous shows no effect on Vigil loot; (3) the Profound +2% micros / +12% additional block.

### Forward model checkpoint 2 (2026-11-06) — parked, `tools/farm/model_cp2.py`, `data/ext/model/checkpoint2.md`
- Pets per **phase**, not per loot type: 3 regular drop pets (Fuel trio Chalk / Surging Gold / Twilight Sparks all map, Outlaw trio
  Prof. SOURCE / Shro-Shroom / Sparks swapped in for the Carjack) + the season's special slots always up (Lady Obituary, Melancholy Azure,
  Heartbloom Iris, Twin Inquisitors in Vlad's area dump; `gamelog` m["pets"] lists all 7). Replicates parsed as x(1+2p): Prof. SOURCE recode
  x1.56, Elegy x1.5, Avatar of Moon x1.5. Chalk / Surging "+X% additional Flame Fuel" lines: dead on Carjack, Vigil, Lunaria loot (XD matrix),
  alive on generic monsters and Dark Surge. Chalk's 1.3% fuel set per kill ignored [Vlad: "garbage"].
- Whole-map FE fitted as generic + mechanic (NLS). **Outlaw lines do not move map FE** (exponent 0.02±0.11); DS resonance at text (1.03±0.13);
  checkpoint 1's "b=0.5 = Carjack share" was those two averaged. Vigil multipliers act at 0.33±0.05 on map FE (wraith FE ~1/3-1/2 of the map).
  Pool exponent on FE 0.73 (Outlaw) / 0.35 (Vigil). Mechanic-loot exponents unchanged from checkpoint 1.

## Per-family fits (2026-11-06 evening, `tools/farm/fit.py`, tables in `data/ext/fits/<family>.md`)
Method: for each mechanic family (every Deep Space strategy running that compass: outlaw 292 strategies / 24k runs, vigil 178 /
15.6k, overrealm 88 / 6.4k, machines 196 / 19.4k, lunaria), one WLS log-linear model per loot item: log(drops per run) on every
compass / probe fraction, DS resonance affixes, Netherrealm resonance, hero class, and every node of the family's own constellations
(+ Profound, Commodities) as a count (micros add); light ridge, HC1 CIs, runs as weights. Nodes everyone in the family runs are
unidentified ("fixed in family"), cards and pets are not logged. Per-unit multipliers (a compass on every run, one DS affix, one point).
Headline numbers (* = CI excludes 1):
- **Outlaw**: Alert compass Warlock x3.95* / Vanguard x3.5* / FE x1.27*; Warlock node x1.44* Warlock; Vanguard node x1.77* Vanguard
  (x0.91* Warlock); Tank node x1.79* Tank; "+1% for all Security personnel" micro x1.01-1.02 per point on mods (= text); Oppressive,
  Bodyguard stacks, Expansion node, Hyper-Hardened, Super Sonic: ~x1.0. Generous x0.98 mods / x1.10 FE (1.00-1.21) -> ~+9 FE for
  17.5. Sinful (A) x1.14* FE; Sinful x1.05 FE; Flourishing probe Vanguard x1.33*, Tank x1.29*, FE x1.11*, fossil x1.5* (~+20 FE for
  27.4); DS affix FE x1.12 (0.99-1.28), mods ~1.0; Bountiful x1.3-1.5* everything (167 FE); All-Evil FE x1.77* (its Vigil), mods
  x0.76-0.84; Evernight FE x1.34*.
- **Vigil**: All-Evil Remnants x2.77* (1.8-4.3), FE x1.31*; Evernight Remnants x1.32 (0.83-2.1); Bountiful x1.46* Remnants, x1.41* FE;
  Generous x1.18 (0.94-1.47) Remnants, x1.12 FE; Sinful (A) x1.24 (0.97-1.6); DS affix Remnants x1.14 (0.86-1.5), FE x1.31*;
  "+1% for the Vigil" micro x1.00 (0.98-1.02) per point on Remnants; Judgment node x1.12*; White Night / +8% medium FE x1.26*;
  "bosses always drop an additional" x0.77* (confounded: taken by weaker players?); Goblin +100% x0.78 (0.54-1.15).
- **Overrealm** (thin): Containment FE x1.84*, Sprout x6*, Secrets x2.2*, fossil x0.28*; Shadow Overrealm Sprout x4.9 (0.7-33);
  Flourishing probe FE x1.38*; the -10/-20/-30% mediums and the +1.5% micros: CIs straddle 1 (unidentified at 88 strategies).
- **Machines (DS)**: Colorful (A) Secrets x1.42*, Colorful x1.16*, Fluorescent DS probe Secrets x1.27*, Focus x1.00 (0.78-1.27),
  SiN x1.23 (0.95-1.6), Transgression x1.31 (0.8-2.2); Shadows too sparse per strategy to fit.
- Generous Elite flip-flop, resolved: the cruder cross-setup fits said x0.94 and then x1.44 on mods; the family fit with the nodes in
  says ~x1.0 on mods, x1.10-1.18 on FE/Remnants -> roughly pays for itself (17.5), nothing more. The 11-06 plan's "drop Generous"
  and the later "keep it, x1.44" were both overclaims.
- **Text vs data** (`tools/farm/texttest.py`, 11-06): slope of observed log(loot/run) on the text's log(flat pool) and
  log(additional product), hero + other compasses controlled. Flat pool (Sinful +40/+80, probe +40, +2%/+1% micros; resonance capped
  +100% for everyone): Outlaw Warlock +0.43 (-0.04..0.91), Outlaw FE +0.64 (0.37..0.92), Vigil FE +0.63, Overrealm FE +1.5 (1.0..2.1),
  Lunaria FE +0.77, **drone Secrets -0.46 (-0.85..-0.07): the flat pool does nothing for drone exclusives, as measured on his logs**.
  Additional product: Warlock +0.95 (0.73..1.18), Vanguard +0.74, Outlaw FE +0.49, Vigil Remnants +0.67, Vigil FE +0.76, Overrealm FE
  +0.73, Lunaria FE +0.85, drone Secrets +0.60. Read: the lines work in the direction written at ~50-95% of the written size on
  average, the gap being conditional lines not always on (Bounty Order, 3 Fright stacks, White Night, Bodyguard stacks) and the
  unlogged card. Super Sonic / Hyper-Hardened: both are "+23% additional Drop Quantity, only one takes effect"; 98% of Outlaw players
  run one, so the per-feature fit can only measure their difference (~x1.0) — "x1.0" in `fits/outlaw.md` means "same as the other
  one", not "does nothing".
