# Checkpoint 1b = checkpoint 1 + the pet fix, nothing else (2026-11-07 02:40)
Code: tools/farm/model.py = commit b3d36e4 (checkpoint 1) with one change, pets per phase: 3 regular drop pets + the season's special slots,
always up; Fuel trio all map, Outlaw trio only for the Carjack; replicate lines (Prof. SOURCE recode, Elegy, Avatar of Moon) and Chalk /
Surging fuel lines counted where the XD matrix says yes. Everything else (model, fits, weights, free effects) is checkpoint 1 as written in
its docstring. What moved vs checkpoint 1: the "naked" bases only (pets are one constant per family); every exponent, bar and free compass
effect is identical. The checkpoint-2 rewrite and the step-2 simulator / tree search are parked as model_cp2.py / strat2.py / tree2.py
(data/ext/model/checkpoint2.md, step2.md, tree2*.md): a drifted branch, read docs/farming.md.

Forward model, checkpoint 1 + pets per phase — prices prices_etor_s14_2026-11-06.json; pool = 1 + 1.00 res + 0.25 Path + flat lines; add = DS affixes x family lines x pets; Fright 3.5

# outlaw: 291 strategies, 24193 runs; assumed pets in the mechanic (Prof. SOURCE, Shro-Shroom, Lumidrake), by loot type: fuel: flat +103% add x1.61; component: flat +103% add x1.61; memory_fluorescence: flat +103% add x1.61; void_divinity_crafting_material: flat +0% add x1.00; legendary_gear: flat +103% add x1.61
item | base/map (naked, at pool 1 / add 1, after dividing out the assumed pets) | a (pool exp) | b (add exp) | free compass effects | spread (resid sd)
Flame_Elementium | 4.273 | 1.06±0.21 | 0.53±0.12 | Bountiful Elite x1.23±0.05, All-Evil Vigil x2.20±0.08, Evernight Vigil x1.56±0.08, Lunar Stele Lunaria x1.74±0.07, Containment Overrealm x4.04±0.46 | 0.18 (n=291)
Expansion_Mod_-_Warlock | 0.012 | 1.73±0.41 | 0.97±0.22 | Generous Elite x1.32±0.13, Bountiful Elite x1.77±0.15, Gear Deep Space probe x0.30±0.10, All-Evil Vigil x1.20±0.08, Evernight Vigil x1.66±0.17 | 0.34 (n=290)
Nether_Kings_Divine_Remnant | 1.605 | -2.06±0.99 | -0.02±0.50 | Generous Elite x0.54±0.16, All-Evil Vigil x12.41±5.45, Evernight Vigil x5.79±2.44, Lavish Novel x0.29±0.16 | 0.38 (n=148)
Expansion_Mod_-_Vanguard | 0.011 | 1.68±0.57 | 0.71±0.33 | Generous Elite x1.38±0.15, Bountiful Elite x1.61±0.17, Gear Deep Space probe x0.18±0.06 | 0.43 (n=290)
Sprout_of_Legends | 0.020 | 0.04±0.67 | 0.65±0.37 | Gear Deep Space probe x0.18±0.11, All-Evil Vigil x1.86±0.25, Evernight Vigil x1.46±0.28, Lunar Stele Lunaria x1.68±0.38 | 0.46 (n=157)
Sacred_Fossil | 0.004 | 2.48±0.72 | 0.38±0.35 | All-Evil Vigil x2.19±0.21, Evernight Vigil x1.71±0.23, Lunar Stele Lunaria x2.10±0.25 | 0.49 (n=280)
Netherrealm_resonance | 7.082 | 1.13±0.23 | 0.38±0.21 | All-Evil Vigil x1.24±0.08, Lunar Stele Lunaria x1.14±0.07, Containment Overrealm x1.35±0.19 | 0.34 (n=291)
Tomorrows_Direction | 0.167 | 0.39±0.32 | 0.78±0.20 | All-Evil Vigil x1.96±0.12, Evernight Vigil x1.41±0.17, Lunar Stele Lunaria x1.50±0.11, Containment Overrealm x3.52±0.71, Lavish Novel x0.24±0.07 | 0.32 (n=291)
Matchless_Ember | 1.764 | 0.83±0.18 | 0.43±0.13 | Bountiful Elite x1.17±0.05, All-Evil Vigil x2.19±0.09, Evernight Vigil x1.54±0.14, Lunar Stele Lunaria x1.70±0.08, Containment Overrealm x4.09±0.55 | 0.20 (n=291)
Flawless_Lunar_Dust | 0.433 | -2.11±0.87 | 0.29±0.73 | Generous Elite x0.58±0.14, Bountiful Elite x0.44±0.10, Lunar Stele Lunaria x20.10±6.65, Conquering Novel x0.35±0.08 | 0.36 (n=69)
Expansion_Mod_-_Tank | 0.005 | 1.97±0.56 | 0.47±0.27 | Generous Elite x1.40±0.13, Bountiful Elite x1.79±0.17, Gear Deep Space probe x0.27±0.09, Evernight Vigil x1.65±0.24, Lavish Novel x0.50±0.16 | 0.42 (n=287)

# vigil: 177 strategies, 15529 runs; assumed pets in the mechanic (Chalk Spirit, Cloudgatherer - Surging Gold, Twilight Sparks, Lady Obituary, Miss Melancholy - Azure), by loot type: fuel: flat +132% add x1.88; component: flat +0% add x1.00; memory_fluorescence: flat +0% add x1.00; void_divinity_crafting_material: flat +132% add x1.88; legendary_gear: flat +0% add x1.00
item | base/map (naked, at pool 1 / add 1, after dividing out the assumed pets) | a (pool exp) | b (add exp) | free compass effects | spread (resid sd)
Flame_Elementium | 5.533 | 0.54±0.32 | 1.17±0.14 | Bountiful Elite x1.25±0.06, Alert Outlaw x1.23±0.07, Lunar Stele Lunaria x1.19±0.07, Conquering Novel x0.73±0.07, Containment Overrealm x2.09±0.24, All-Evil Vigil x0.29±0.07, Evernight Vigil x0.59±0.08 | 0.15 (n=177)
Nether_Kings_Divine_Remnant | 0.075 | 0.22±0.60 | 0.72±0.27 | Bountiful Elite x1.21±0.12, Containment Overrealm x0.51±0.11 | 0.30 (n=177)
Expansion_Mod_-_Warlock | 0.232 | -0.94±0.59 | 1.56±0.40 | Alert Outlaw x11.84±2.83, Full Load Outlaw x6.67±3.01, All-Evil Vigil x0.05±0.03, Evernight Vigil x0.26±0.09 | 0.32 (n=149)
Expansion_Mod_-_Vanguard | 0.757 | -2.01±0.57 | 1.19±0.58 | Generous Elite x0.63±0.13, Alert Outlaw x14.10±3.49, Full Load Outlaw x5.80±3.25, All-Evil Vigil x0.06±0.06, Evernight Vigil x0.14±0.07 | 0.38 (n=142)
Sprout_of_Legends | 0.041 | -1.21±0.68 | 1.54±0.54 | Containment Overrealm x2.33±0.98 | 0.42 (n=119)
Sacred_Fossil | 0.147 | 0.45±0.60 | 0.91±0.40 | Bountiful Elite x1.48±0.25, Lunar Stele Lunaria x1.44±0.17, Evernight Vigil x0.48±0.17 | 0.44 (n=176)
Tomorrows_Direction | 0.198 | 0.23±0.44 | 1.18±0.30 | All-Evil Vigil x0.25±0.12, Evernight Vigil x0.52±0.14 | 0.27 (n=177)
Netherrealm_resonance | 12.441 | 0.73±0.42 | 0.63±0.34 | — | 0.34 (n=177)
Matchless_Ember | 2.989 | 0.29±0.23 | 1.17±0.23 | Bountiful Elite x1.26±0.08, Alert Outlaw x1.30±0.08, Lunar Stele Lunaria x1.28±0.09, Conquering Novel x0.72±0.10, Containment Overrealm x2.65±0.78, All-Evil Vigil x0.26±0.09, Evernight Vigil x0.55±0.09 | 0.19 (n=177)
Goddess_of_Huntings_Divine_Rem | 0.022 | 0.59±0.66 | 0.76±0.32 | Bountiful Elite x1.25±0.14 | 0.30 (n=173)

# lunaria: 87 strategies, 5492 runs; assumed pets in the mechanic (Chalk Spirit, Cloudgatherer - Surging Gold, Twilight Sparks, Avatar of Moon, Miss Melancholy - Cyan), by loot type: fuel: flat +136% add x1.75; component: flat +0% add x1.00; memory_fluorescence: flat +136% add x1.75; void_divinity_crafting_material: flat +0% add x1.00; legendary_gear: flat +136% add x1.75
item | base/map (naked, at pool 1 / add 1, after dividing out the assumed pets) | a (pool exp) | b (add exp) | free compass effects | spread (resid sd)
Flame_Elementium | 10.208 | 0.54±0.62 | 0.76±0.18 | Alert Outlaw x1.51±0.15, All-Evil Vigil x1.85±0.19 | 0.15 (n=87)
Expansion_Mod_-_Warlock | 1.239 | -1.59±1.89 | 0.96±0.69 | Alert Outlaw x5.61±4.21 | 0.47 (n=64)
Nether_Kings_Divine_Remnant | 0.371 | -0.78±2.37 | 1.04±0.62 | All-Evil Vigil x4.02±1.52, Conquering Novel x0.41±0.16 | 0.21 (n=26)
Flawless_Lunar_Dust | 0.006 | 1.34±1.12 | 1.15±0.32 | — | 0.30 (n=86)
Expansion_Mod_-_Vanguard | 0.007 | 1.41±1.95 | 0.04±0.72 | Alert Outlaw x5.71±4.18 | 0.36 (n=61)
Sprout_of_Legends | 19.659 | -5.25±2.80 | 1.23±1.23 | All-Evil Vigil x6.31±4.71, Conquering Novel x0.27±0.17 | 0.47 (n=48)
Sacred_Fossil | 0.209 | -1.18±1.37 | 1.51±0.53 | Alert Outlaw x3.53±1.37, All-Evil Vigil x4.46±1.68, Divine Warrior Dark Surge x2.49±1.08 | 0.41 (n=84)
Luminous_Lunar_Dust | 0.009 | 2.64±1.31 | 0.33±0.31 | Divine Warrior Dark Surge x1.94±0.59 | 0.25 (n=87)
Crude_Lunar_Dust | 0.079 | 2.50±1.63 | 0.51±0.34 | Divine Warrior Dark Surge x2.03±0.73 | 0.25 (n=86)
Netherrealm_resonance | 72.703 | -0.73±1.75 | 0.32±0.24 | — | 0.31 (n=87)
Tomorrows_Direction | 0.032 | 0.93±0.94 | 0.39±0.36 | Alert Outlaw x3.03±0.81, All-Evil Vigil x3.27±0.84 | 0.32 (n=87)

# darksurge: 50 strategies, 4151 runs; assumed pets in the mechanic (Chalk Spirit, Cloudgatherer - Surging Gold, Twilight Sparks, Eternity Summoner, Plaintive Ball of Thread - Flower), by loot type: fuel: flat +94% add x2.68; component: flat +0% add x1.00; memory_fluorescence: flat +0% add x1.00; void_divinity_crafting_material: flat +0% add x1.00; legendary_gear: flat +94% add x1.16
item | base/map (naked, at pool 1 / add 1, after dividing out the assumed pets) | a (pool exp) | b (add exp) | free compass effects | spread (resid sd)
Flame_Elementium | 0.677 | 2.14±0.87 | 0.75±0.60 | Lunar Stele Lunaria x2.22±0.24 | 0.21 (n=50)
Expansion_Mod_-_Warlock | 0.068 | 0.92±1.34 | 2.85±0.72 | Alert Outlaw x10.40±5.14, Full Load Outlaw x2.11±0.50 | 0.25 (n=29)
Expansion_Mod_-_Vanguard | 0.421 | -1.50±2.33 | -1.94±2.07 | Alert Outlaw x9.41±7.14, Divine Warrior Dark Surge x0.30±0.18, Bandit Dark Surge x0.21±0.10, Dark Surge x0.23±0.16 | 0.33 (n=31)
Netherrealm_resonance | 18.339 | 1.54±0.46 | 1.12±0.75 | Lunar Stele Lunaria x0.25±0.10 | 0.22 (n=50)

# Calibration against Vlad's maps (unchanged from checkpoint 1: pets are a constant inside a family, so only the bases moved)
setup | item | model | his
Alert + All-Evil (20 maps 11-05; pool 4.48, add 3.23) | Warlock | 0.79 | 0.10
Alert + All-Evil (20 maps 11-05; pool 4.48, add 3.23) | Vanguard | 0.41 | 0.65
Alert + All-Evil (20 maps 11-05; pool 4.48, add 3.23) | Tank | 0.26 | 0.40
Alert + All-Evil (20 maps 11-05; pool 4.48, add 2.76) | FE | 84.42 | 67
All-Evil (same maps; pool 4.77, add 13.67) | Remnants | 0.79 | 0.30  (the All-Evil multiplier that fits him: x1.16 vs text 4.5)
Evernight (71 maps 11-05/06; pool 4.37, add 6.07) | Remnants | 0.49 | 0.48 / 0.59 (0.535 over both days)
Evernight | FE whole map | 60 | 93 (his includes the Overrealm's FE, not in the model)
