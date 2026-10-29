# Profound farming plan (2026-10-29, prices of that day; tools/farm/)

Basis: 629 logged CN Profound strategies / 46k runs (etor), re-valued at today's prices, seller tax 12.5% on everything
but FE, consumables at market. Vlad: bare Glacial Abyss Profound map 40 s, 31 resonance, 4 compass slots, 1 Profound probe
slot, 92 Star + 4 Prime, any rank-6 drop pet, no deaths. Quantity multiplier Q = (1 + pool) x 2 (the card's +100%).

## What the data says (CN, net FE per minute at today's prices, their speed)
| forced mechanics | runs | FE/map gross | cost | min | net/min | note |
|---|---|---|---|---|---|---|
| Hunting (Revelation Astrolabe) + Compass tree | 219 | 109-148 | 59-151 | 0.9-1.3 | 45-80 | 19-28 compasses per map |
| Machines (Cruising Artifact) ice/steel | 555 | 228 | 81 | 1.6 | 92 | 87 FE/map Disappearing Shadow (= LW blueprint token), Gaze lottery 61 |
| Overrealm tree only | 568 | 182 | 28 | 2.1 | 75 | Inverse Image 7k at 1/46 maps: lottery |
| Arcana + Hunting | 192 | 216 | 32 | 2.6 | 70 | Undetermined Fate lottery |
| Dark Surge + Outlaw (+War) | 1,300 | 110-150 | 24-61 | 1.4-1.5 | 53-56 | blueprint jackpots |
| Dark Surge + Lunaria + War | 718 | 105 | 45 | 1.3 | 45 | steady |
| Afterlight | 868 | 105 | 57 | 1.1 | 43 | divinity items are cheap now |
| Clockwork Ballet (20k runs, the CN favourite) | 20,881 | 153 | 141 | 1.7 | 7 | compass prices fell; dead at today's prices |

## Plan A - Safari compass farm (primary)
Per map (Vlad): 25 compasses worth ~115 FE after tax, +48 generic, +17 global legendary EV = ~180 FE; cost 59 (Revelation 22,
Vast Ecliptic 16, Ecliptic 1.4, Compass Probe 13, beacon 3.3, resonance 3.4); time 40 s + ~35 s = ~1.3 min.
**Net ~120 FE/map, ~95 FE/min (~5,700 FE/hour).** Model, +-30%: the compass sample is 219 runs by two players.
- Compasses: Revelation Hunting Astrolabe, Vast Ecliptic Astrolabe, Ecliptic Astrolabe, 4th slot Sinful Plunder (13.5 FE, +40%
  quantity: +28 FE/map at this value, net +14) or leave it empty.
- Probe: Compass Profound Probe (13 FE, +20% additional compass quantity).
- Tree (92): Compass 51 = all 37 "+1.4% additional Compass Drop Quantity" micros + "+4%" + "5% replicated" + "+2.5% per compass
  inserted" + "2% / 3% / 1% more valuable" mediums + whatever "more likely to be X" mediums the path needs (prefer Vorax, Overrealm,
  Might, Mechanical, Dark Surge, Outlaw, Afterlight, Lunaria, Arcana, Cube: the expensive types). Hunting 37 = Mistrustful card
  (Safari mode, mandatory), both "2 Safari Bosses" mediums, Insidious card, "+12%" and "+7% per Safari boss" mediums, "+7% Safari"
  medium, "5% replicate" medium, "skip buff selection" medium, all 18 "+1% Safari rewards" micros, 6 "+1% per Safari boss" micros,
  3 "1% replicate" micros, 1 "3% replicate final boss" micro. Profound 4 Prime = micro + "+30% quantity (2 lives)" major, micro +
  "10% chance not to consume compasses" major.
- Pets (rank 6): Doro-Doro Dorothy, Benign Bug, Twilight Sparks (all lines verified on Safari-boss compass drops in XD's matrix).
- Card: Mystery Chests or any +drop-quantity card; Hunting cards if offered.
- Risks: compass prices are sliding (Revelation 43 -> 22, Collection Doll 40 -> 18 over the window); 25 compasses a map is
  ~1,200 listings an hour at full speed; whether general Drop Quantity applies to Safari-boss compasses is XD's word, unverified.

## Plan B - Machines (alternative; decided by Vlad's Machines time)
CN: 228 FE/map gross (Disappearing Shadow 87, Gaze Upon the Reflection 61 = 1 per 159 maps, Secret of the Glacial Abyss 23, FE 21),
cost 81 (Cruising Mechanical (Artifact) 22, Transgression Plunder 45, Strength in Numbers Soldier 1, Focus Fluorescent 5,
Fluorescent Probe 6), 1.6 min total map time with the Machines tree (24 "+1% extra attack round" micros, "attack interval 1 s / 3 s"
mediums, "+25% drone quantity", "+0.6% attackers"). Net 147/map.
- Vlad at his stated 3 min Machines: 3.7 min/map -> ~40 FE/min (25 without the Gaze lottery). At CN speed (~2 min with the
  interval nodes): ~75 FE/min. Disappearing Shadow x5 (read) = Blueprint: Lone Walker's Boots, his own target item.
- Pets: Kong, Twilight Sparks, Cloudgatherer - Sky's Dome.

## Not recommended now
Clockwork Ballet (compass prices), Afterlight (divinity items 72 FE and the Nether King's Divinities unpriced), Might
(compasses 41-162 FE for 97 FE of embers), Overrealm (2+ min for a 1/80 lottery), Outlaw (34 FE of mods for a 29 FE compass).

## Tests before committing
1. Plan A, 10 maps: count compasses and their listed value, time per map. Expect ~25 compasses / ~115 FE / ~1.3 min.
2. Plan B, 5 maps with the Machines tree: time per map. Under 2 min makes it competitive, 3 min does not.

## Plan B bottom-up (2026-10-29 evening, tools/farm/machines.py) - answers the slot question
Drone memories split: common ones (Secret of the Glacial Abyss 105/map, Tomorrow's Direction 1, Gaze 1/159) take the Drop
Quantity pool, all "additional", fluorescent "additional" and replications; the exclusive Disappearing Shadow (0.5/map, 241 FE)
takes no pool and no fluorescent-specific additional (XD matrix), but generic additional and replications. CN full stack = base.
Per map, taxed, Vlad's pool (31 res + Profound 30 + micros + pets 74 = 210): common+Gaze 110, exclusive 94, FE/generic 39 =
gross 243, cost 81, **net 162 FE/map** (97 without the Gaze lottery).
- Transgression Plunder (44.8): x1.9 on drone drops at 30 stacks -> +96 gross, **+56 net**. Needs ~30 rare kills before the drones
  (check the stack counter when the trial starts; at 15 stacks it is +45 gross, break-even).
- Colorful Fluorescent (Artifact) (8): 50% replicate on every memory incl. the exclusive -> +68 gross, **+61 net**.
- Strength in Numbers Soldier (1): x1.2 on normals (drones) + 10 groups -> +40.
- Fluorescent Profound Probe (6): 20% replicate -> +28. Focus Fluorescent (5): x1.5 exclusive -> +42 but needs a slot:
  Cruising + Trans + SiN + ColA (162) > Trans + ColA + Focus (157) > Trans + SiN + Focus (128). Sinful Plunder: +7 / +3, no.
- Pets: Kong 82 FE/map, Sky's Dome 45, Twilight Sparks 38 (next best replacement Idling Weasel - Sparkle: -12). Keep the three.
- Tree: Machine 39 = spoke 62-76 (echelons x2, +25%, Obtuse +40%) + Dull (77-80) + interval spoke 40-47 (3 s / 1 s) + attackers
  spoke 24-27 + Paranoid spoke 16-17/28-31; saturates after that (1 FE/pt). Rest: Commodities 15 "+1% quantity" micros (0.5/pt),
  Legendary Gear "Ultimate +32%" / "Precious+ 9%" mediums (~0.5/pt). Profound Prime 4: +30% major and 10% compass refund.
- 19:10 correction (Vlad): Focus Fluorescent stays (x1.5 on the exclusive, +42 net for 5 FE; the 5-FE tie against Strength in Numbers
  is noise). With Focus fixed: **Cruising + Focus + Colorful (Artifact) + Transgression = 157 net/map** (103 without Gaze) > + Strength
  in Numbers 126 > + Colorful 119. Transgression at 15 stacks: gross +78, net +33, still ahead of SiN. Two fluorescent compasses stack
  (CN ran Colorful + Colorful (Artifact) together).
- Profound "+12% additional, 25 extra Star Talents": x1.12 on ~240 gross = **+29 FE/map for 26 points** - better than Commodities or
  Legendary Gear leftovers (~0.5 FE/pt). Vlad runs it; I had wrongly dismissed it.
- Vlad's tree: Machine 43 + Creation 24 (100% Creation Engines, Fluorescent crystals: "30% chance to duplicate fluorescent memories",
  Gold crystal = guaranteed exclusive memory) + Profound 30% / 12%. Creation is unpriced: only 2 CN strategies used the constellation;
  the Machines+Creation one took 4 Gaze in 89 maps (7x the usual rate). Need the crystal buff text/scope, crystals per map, time.
- 19:30 (Vlad): replication = one summed once-chance capped at 100%, Kong x1.46 after. Machines re-run: 4th slot Transgression +69
  net (needs the time test; -60% damage dealt), Strength in Numbers +30, Colorful / Fluorescent Compass +6. Probe: Fluorescent +0
  (and -40% damage taken) -> cut; Flourishing +4. Creation's 30% is worth +19, Colorful (Artifact) +25, Focus +18 in this stack.
