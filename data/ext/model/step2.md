Step 2 — prices prices_etor_s14_2026-11-06.json, model checkpoint 2, Fright 3.5, Overrealm block from his 69 maps (84 FE, 100 s, 0.49 deaths per map)

# His loop (Evernight + Shadow Overrealm + Generous + Sinful + Flourishing, no DS affixes, Fuel trio), the model's view
as run                                               | net    100/map |  24.2/min (+lottery  36.8) |  247 s | FE   54 | cost  104
  items: Flame Elementium 54.44 (54), Nether Kings Divine Remn 0.36 (22), Netherrealm resonance 35.20 (3), Sacred Fossil 0.46 (3), Sprout of Legends 0.02 (2), Tomorrows Direction 0.38 (2); Overrealm block (his 69 maps): 84 FE in 100 s, 0.49 deaths
  his measured 11-06: net 123/map, 214 s in map, 33.8/min (the model's map part: FE 54 = generic 34 + wraith 21)

## Marginals, one change at a time from the loop as run (FE/map and /min deltas; > ~15 FE/map is a real difference, less is noise)
change | net/map | /min | delta/map | delta/min
add Alert Outlaw                                     |    124 |  29.5 |    +24 |  +5.2
drop Flourishing probe                               |    121 |  29.4 |    +21 |  +5.2
drop Generous Elite                                  |    116 |  28.3 |    +17 |  +4.0
add Strength in Numbers Soldier                      |    114 |  27.1 |    +14 |  +2.9
DS resonance affixes 0 -> 2                          |    112 |  27.1 |    +12 |  +2.8
Evernight Vigil -> All-Evil Vigil                    |     99 |  26.1 |     -0 |  +1.9
drop Sinful Plunder                                  |    107 |  26.0 |     +7 |  +1.8
DS resonance affixes 0 -> 1                          |    105 |  25.5 |     +5 |  +1.2
+1 Vigil micro                                       |    100 |  24.3 |     +0 |  +0.1
+1 Outlaw micro                                      |    100 |  24.2 |     +0 |  +0.0
add Transgression Plunder                            |     94 |  22.7 |     -6 |  -1.5
Flourishing probe -> Fluorescent probe               |     93 |  22.6 |     -7 |  -1.6
add Lunar Stele Lunaria                              |     91 |  21.9 |     -9 |  -2.3 | time: CN x1.2 (lunaria never run)
Sinful Plunder -> Sinful Plunder (A)                 |     77 |  18.6 |    -23 |  -5.7
add Divine Warrior Dark Surge                        |     70 |  17.0 |    -30 |  -7.3 | time: CN x1.2 (darksurge never run)
drop the Overrealm                                   |     17 |   6.9 |    -83 | -17.3
Flourishing probe -> Compass probe                   |     22 |   5.4 |    -78 | -18.8
Generous -> Bountiful                                |    -29 |  -7.0 |   -129 | -31.2

## Greedy path: apply the best change, recompute, repeat while it gains > 1/min
add Alert Outlaw                                     | net    124/map |  29.5/min (+lottery  41.8) |  252 s | FE   66 | cost  140
add Alert Outlaw + DS resonance affixes 0 -> 2       | net    154/map |  36.5/min (+lottery  48.8) |  252 s | FE   85 | cost  153
e affixes 0 -> 2 + Evernight Vigil -> All-Evil Vigil | net    167/map |  42.9/min (+lottery  56.3) |  233 s | FE  113 | cost  191
 -> All-Evil Vigil + add Strength in Numbers Soldier | net    187/map |  47.1/min (+lottery  60.1) |  238 s | FE  124 | cost  192
ength in Numbers Soldier + add Transgression Plunder | net    196/map |  49.3/min (+lottery  62.4) |  238 s | FE  143 | cost  220
+ add Transgression Plunder + drop Flourishing probe | net    203/map |  51.0/min (+lottery  64.1) |  238 s | FE  136 | cost  193
lunder + drop Flourishing probe + drop the Overrealm | net    120/map |  52.1/min (+lottery  74.6) |  138 s | FE  136 | cost  191
  result: Generous Elite, Sinful Plunder, Alert Outlaw, All-Evil Vigil, Strength in Numbers Soldier, Transgression Plunder, DS affixes 2, Overrealm dropped; items: Flame Elementium 135.89 (136), Expansion Mod - Warlock 0.71 (41), Nether Kings Divine Remn 0.66 (40), Expansion Mod - Vanguard 0.42 (14), Sprout of Legends 0.06 (7), Matchless Ember 27.01 (7)

## Regular pet slots on this setup (59 candidate pets, every trio): Fuel trio = 0
   +0.0/min | Cloudgatherer - Surging Gold, Twilight Sparks, Chalk Spirit
   -4.1/min | Happy Chonky, Cloudgatherer - Surging Gold, Chalk Spirit
   -7.2/min | Cloudgatherer - Surging Gold, Chalk Spirit, Corgi Fighter No.32
   -7.7/min | Cloudgatherer - Surging Gold, Chalk Spirit, Starfish Chanter
   -8.6/min | Happy Chonky, Twilight Sparks, Chalk Spirit
   -9.3/min | Cloudgatherer - Surging Gold, Plaintive Ball of Thread - Gold Leaf, Chalk Spirit
   -9.9/min | Miss Melancholy - Pink, Cloudgatherer - Surging Gold, Chalk Spirit
  -10.1/min | Twilight Sparks, Chalk Spirit, Corgi Fighter No.32

# Search: 2624 setups (mechanics x elite x Sinful x Strength in Numbers / Transgression x probe x DS affixes 0/2 x Overrealm; at most 4 compasses + probe), his tree lines, Fuel trio, ranked by net FE per in-map minute
rank | /min | +lottery | net/map | s | FE | cost | setup
 1 |  50.4 |  72.9 |   116 |  138 |  128 |  161 | Alert Outlaw, All-Evil Vigil, Strength in Numbers Soldier, Transgression Plunder, DS x2
 2 |  50.0 |  72.5 |   115 |  138 |  117 |  145 | Alert Outlaw, All-Evil Vigil, Sinful Plunder, Strength in Numbers Soldier, DS x2
 3 |  48.8 |  61.8 |   194 |  238 |  111 |  134 | Alert Outlaw, All-Evil Vigil, Strength in Numbers Soldier, DS x2, Overrealm
 4 |  48.2 |  70.7 |   111 |  138 |  111 |  132 | Alert Outlaw, All-Evil Vigil, Strength in Numbers Soldier, DS x2
 5 |  46.9 |  69.4 |   108 |  138 |  136 |  188 | Alert Outlaw, All-Evil Vigil, Strength in Numbers Soldier, Transgression Plunder, Flourishing probe, DS x2
 6 |  46.4 |  68.9 |   107 |  138 |  111 |  149 | Alert Outlaw, All-Evil Vigil, Generous Elite, Strength in Numbers Soldier, DS x2
 7 |  46.3 |  59.3 |   184 |  238 |  117 |  161 | Alert Outlaw, All-Evil Vigil, Strength in Numbers Soldier, Flourishing probe, DS x2, Overrealm
 8 |  46.1 |  59.4 |   179 |  233 |  107 |  146 | Alert Outlaw, All-Evil Vigil, Sinful Plunder, DS x2, Overrealm
 9 |  45.6 |  68.1 |   105 |  138 |  124 |  173 | Alert Outlaw, All-Evil Vigil, Sinful Plunder, Strength in Numbers Soldier, Flourishing probe, DS x2
10 |  45.2 |  58.6 |   176 |  233 |  101 |  133 | Alert Outlaw, All-Evil Vigil, DS x2, Overrealm
11 |  45.1 |  58.4 |   175 |  233 |  116 |  161 | Alert Outlaw, All-Evil Vigil, Transgression Plunder, DS x2, Overrealm
12 |  44.8 |  67.3 |   103 |  138 |  124 |  175 | Alert Outlaw, All-Evil Vigil, Sinful Plunder (A), Strength in Numbers Soldier, DS x2
13 |  44.5 |  57.8 |   173 |  233 |  106 |  126 | All-Evil Vigil, Strength in Numbers Soldier, Transgression Plunder, DS x2, Overrealm
14 |  44.1 |  57.5 |   172 |  233 |  101 |  150 | Alert Outlaw, All-Evil Vigil, Generous Elite, DS x2, Overrealm
15 |  44.0 |  57.3 |   171 |  233 |   91 |   98 | All-Evil Vigil, Strength in Numbers Soldier, DS x2, Overrealm
16 |  43.9 |  66.4 |   101 |  138 |  117 |  159 | Alert Outlaw, All-Evil Vigil, Strength in Numbers Soldier, Flourishing probe, DS x2
17 |  43.8 |  67.2 |    97 |  133 |  123 |  173 | Alert Outlaw, All-Evil Vigil, Sinful Plunder, Transgression Plunder, DS x2
18 |  43.6 |  57.0 |   170 |  233 |   97 |  111 | All-Evil Vigil, Sinful Plunder, Strength in Numbers Soldier, DS x2, Overrealm
19 |  43.5 |  55.6 |   186 |  257 |   86 |   96 | Alert Outlaw, Evernight Vigil, Strength in Numbers Soldier, DS x2, Overrealm
20 |  43.4 |  66.8 |    96 |  133 |  107 |  144 | Alert Outlaw, All-Evil Vigil, Sinful Plunder, DS x2
21 |  43.2 |  56.5 |   168 |  233 |  113 |  173 | Alert Outlaw, All-Evil Vigil, Sinful Plunder, Flourishing probe, DS x2, Overrealm
22 |  42.8 |  65.3 |    98 |  138 |  117 |  177 | Alert Outlaw, All-Evil Vigil, Generous Elite, Strength in Numbers Soldier, Flourishing probe, DS x2
23 |  42.7 |  56.1 |   166 |  233 |  113 |  175 | Alert Outlaw, All-Evil Vigil, Sinful Plunder (A), DS x2, Overrealm
24 |  42.7 |  56.0 |   166 |  233 |  123 |  189 | Alert Outlaw, All-Evil Vigil, Transgression Plunder, Flourishing probe, DS x2, Overrealm
25 |  42.4 |  55.8 |   165 |  233 |  107 |  160 | Alert Outlaw, All-Evil Vigil, Flourishing probe, DS x2, Overrealm
26 |  42.2 |  65.6 |    94 |  133 |  107 |  162 | Alert Outlaw, All-Evil Vigil, Generous Elite, Sinful Plunder, DS x2
27 |  41.9 |  65.3 |    93 |  133 |  101 |  131 | Alert Outlaw, All-Evil Vigil, DS x2
28 |  41.8 |  55.1 |   162 |  233 |  107 |  177 | Alert Outlaw, All-Evil Vigil, Generous Elite, Flourishing probe, DS x2, Overrealm
29 |  41.7 |  54.8 |   166 |  238 |  111 |  162 | Alert Outlaw, All-Evil Vigil, Strength in Numbers Soldier, Fluorescent probe, DS x2, Overrealm
30 |  41.7 |  65.1 |    92 |  133 |  116 |  160 | Alert Outlaw, All-Evil Vigil, Transgression Plunder, DS x2
31 |  41.1 |  60.9 |   108 |  157 |  104 |  123 | Alert Outlaw, Evernight Vigil, Strength in Numbers Soldier, Transgression Plunder, DS x2
32 |  41.0 |  53.5 |   169 |  248 |  108 |  123 | All-Evil Vigil, Lunar Stele Lunaria, Strength in Numbers Soldier, DS x2, Overrealm | time: CN x1.2 (lunaria never run)
33 |  40.8 |  54.2 |   159 |  233 |  112 |  154 | All-Evil Vigil, Strength in Numbers Soldier, Transgression Plunder, Flourishing probe, DS x2, Overrealm
34 |  40.8 |  54.4 |   155 |  228 |   83 |   97 | All-Evil Vigil, DS x2, Overrealm
35 |  40.7 |  53.8 |   162 |  238 |   87 |  120 | Alert Outlaw, All-Evil Vigil, Strength in Numbers Soldier, DS x0, Overrealm
36 |  40.6 |  64.0 |    90 |  133 |  112 |  138 | All-Evil Vigil, Sinful Plunder, Strength in Numbers Soldier, Transgression Plunder, DS x2
37 |  40.6 |  64.0 |    90 |  133 |  106 |  125 | All-Evil Vigil, Strength in Numbers Soldier, Transgression Plunder, DS x2
38 |  40.4 |  52.5 |   173 |  257 |   91 |  123 | Alert Outlaw, Evernight Vigil, Strength in Numbers Soldier, Flourishing probe, DS x2, Overrealm
39 |  40.3 |  52.6 |   169 |  252 |   85 |   89 | Evernight Vigil, Strength in Numbers Soldier, Transgression Plunder, DS x2, Overrealm
40 |  40.2 |  52.6 |   169 |  252 |   77 |   95 | Alert Outlaw, Evernight Vigil, DS x2, Overrealm

## Best per mechanic set
 50.4/min (+lot  72.9) | Alert Outlaw + All-Evil Vigil              | with Strength in Numbers Soldier, Transgression Plunder, DS x2 | items: Flame Elementium 128.40 (128), Nether Kings Divine Remn 0.59 (36), Expansion Mod - Warlock 0.48 (28), Expansion Mod - Vanguard 0.27 (9), Matchless Ember 26.06 (7)
 48.8/min (+lot  61.8) | Alert Outlaw + All-Evil Vigil + Overrealm  | with Strength in Numbers Soldier, DS x2 | items: Flame Elementium 111.06 (111), Nether Kings Divine Remn 0.59 (36), Expansion Mod - Warlock 0.48 (28), Expansion Mod - Vanguard 0.27 (9), Matchless Ember 20.05 (5)
 44.5/min (+lot  57.8) | All-Evil Vigil + Overrealm                 | with Strength in Numbers Soldier, Transgression Plunder, DS x2 | items: Flame Elementium 105.70 (106), Nether Kings Divine Remn 0.59 (36), Sprout of Legends 0.05 (7), Matchless Ember 20.14 (5), Netherrealm resonance 54.51 (5)
 43.5/min (+lot  55.6) | Alert Outlaw + Evernight Vigil + Overrealm | with Strength in Numbers Soldier, DS x2 | items: Flame Elementium 86.28 (86), Expansion Mod - Warlock 0.48 (28), Nether Kings Divine Remn 0.35 (21), Expansion Mod - Vanguard 0.27 (9), Matchless Ember 14.32 (4)
 41.1/min (+lot  60.9) | Alert Outlaw + Evernight Vigil             | with Strength in Numbers Soldier, Transgression Plunder, DS x2 | items: Flame Elementium 103.63 (104), Expansion Mod - Warlock 0.48 (28), Nether Kings Divine Remn 0.35 (21), Expansion Mod - Vanguard 0.27 (9), Matchless Ember 18.62 (5)
 41.0/min (+lot  53.5) | All-Evil Vigil + Lunar Stele Lunaria + Overrealm | with Strength in Numbers Soldier, DS x2 | items: Flame Elementium 108.26 (108), Nether Kings Divine Remn 0.59 (36), Matchless Ember 19.85 (5), Sprout of Legends 0.04 (5), Sacred Fossil 0.60 (4)
 40.6/min (+lot  64.0) | All-Evil Vigil                             | with Sinful Plunder, Strength in Numbers Soldier, Transgression Plunder, DS x2 | items: Flame Elementium 111.87 (112), Nether Kings Divine Remn 0.66 (40), Sprout of Legends 0.06 (7), Matchless Ember 20.88 (6), Netherrealm resonance 61.80 (6)
 40.3/min (+lot  52.6) | Evernight Vigil + Overrealm                | with Strength in Numbers Soldier, Transgression Plunder, DS x2 | items: Flame Elementium 85.31 (85), Nether Kings Divine Remn 0.35 (21), Netherrealm resonance 54.51 (5), Tomorrows Direction 0.75 (4), Matchless Ember 14.39 (4)
 38.7/min (+lot  51.1) | Evernight Vigil + Lunar Stele Lunaria + Overrealm | with Strength in Numbers Soldier, DS x2 | items: Flame Elementium 84.11 (84), Nether Kings Divine Remn 0.35 (21), Sacred Fossil 0.60 (4), Matchless Ember 14.19 (4), Netherrealm resonance 41.93 (4)
 37.2/min (+lot  58.2) | All-Evil Vigil + Lunar Stele Lunaria       | with Strength in Numbers Soldier, Transgression Plunder, DS x2 | items: Flame Elementium 125.17 (125), Nether Kings Divine Remn 0.59 (36), Matchless Ember 25.81 (7), Sprout of Legends 0.05 (7), Sacred Fossil 0.78 (5)
 34.1/min (+lot  54.6) | Evernight Vigil                            | with Strength in Numbers Soldier, Transgression Plunder, DS x2 | items: Flame Elementium 85.31 (85), Nether Kings Divine Remn 0.35 (21), Netherrealm resonance 54.51 (5), Tomorrows Direction 0.75 (4), Matchless Ember 14.39 (4)
 33.1/min (+lot  53.6) | Evernight Vigil + Lunar Stele Lunaria      | with Strength in Numbers Soldier, Transgression Plunder, DS x2 | items: Flame Elementium 101.02 (101), Nether Kings Divine Remn 0.35 (21), Sacred Fossil 0.78 (5), Matchless Ember 18.44 (5), Netherrealm resonance 54.51 (5)
 31.4/min (+lot  58.9) | Lunar Stele Lunaria                        | with Strength in Numbers Soldier, Transgression Plunder, DS x2 | items: Flame Elementium 102.57 (103), Sprout of Legends 0.16 (19), Netherrealm resonance 61.43 (5), Flawless Lunar Dust 0.10 (2), Sacred Fossil 0.26 (2)
 28.6/min (+lot  48.0) | Alert Outlaw + Lunar Stele Lunaria         | with Strength in Numbers Soldier, Transgression Plunder, DS x2 | items: Flame Elementium 93.80 (94), Expansion Mod - Warlock 0.48 (28), Expansion Mod - Vanguard 0.27 (9), Tomorrows Direction 1.38 (7), Sprout of Legends 0.04 (5)
 22.4/min (+lot  43.2) | Alert Outlaw                               | with Strength in Numbers Soldier, DS x2 | items: Flame Elementium 44.30 (44), Expansion Mod - Warlock 0.48 (28), Expansion Mod - Vanguard 0.27 (9), Tomorrows Direction 0.75 (4), Sprout of Legends 0.03 (4)
 -4.3/min (+lot  61.1) | Divine Warrior Dark Surge                  | with Strength in Numbers Soldier, DS x0 | items: Flame Elementium 19.74 (20), Netherrealm resonance 100.03 (9)

## Exponents the data could not pin (bar > 0.4 or negative), set to the text's 1 and refitted: outlaw Expansion_Mod_-_Warlock: a; outlaw Nether_Kings_Divine_Remnant: a/b; outlaw Expansion_Mod_-_Vanguard: a; outlaw Sprout_of_Legends: a/b; outlaw Sacred_Fossil: a/b; outlaw Flawless_Lunar_Dust: a/b; outlaw Expansion_Mod_-_Tank: a; vigil Nether_Kings_Divine_Remnant: a; vigil Expansion_Mod_-_Warlock: a/b; vigil Expansion_Mod_-_Vanguard: a/b; vigil Sprout_of_Legends: a/b; vigil Sacred_Fossil: a/b; vigil Tomorrows_Direction: a; vigil Netherrealm_resonance: a; vigil Goddess_of_Huntings_Divine_Remnant_-_Legendary: a; lunaria Flame_Elementium: a; lunaria Expansion_Mod_-_Warlock: a/b; lunaria Nether_Kings_Divine_Remnant: a/b; lunaria Flawless_Lunar_Dust: a; lunaria Expansion_Mod_-_Vanguard: a/b; lunaria Sprout_of_Legends: a/b; lunaria Sacred_Fossil: a/b; lunaria Luminous_Lunar_Dust: a; lunaria Crude_Lunar_Dust: a; lunaria Netherrealm_resonance: a; lunaria Tomorrows_Direction: a/b; darksurge Flame_Elementium: a/b; darksurge Expansion_Mod_-_Warlock: a/b; darksurge Expansion_Mod_-_Vanguard: a/b; darksurge Netherrealm_resonance: a/b
