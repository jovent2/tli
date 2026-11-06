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
DS resonance affixes 0 -> 2                          |    112 |  27.1 |    +12 |  +2.8
Evernight Vigil -> All-Evil Vigil                    |     99 |  26.1 |     -0 |  +1.9
drop Sinful Plunder                                  |    107 |  26.0 |     +7 |  +1.8
DS resonance affixes 0 -> 1                          |    105 |  25.5 |     +5 |  +1.2
+1 Vigil micro                                       |    100 |  24.3 |     +0 |  +0.1
+1 Outlaw micro                                      |    100 |  24.2 |     +0 |  +0.0
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
ght Vigil -> All-Evil Vigil + drop Flourishing probe | net    176/map |  45.4/min (+lottery  58.7) |  233 s | FE  107 | cost  163
  result: Generous Elite, Sinful Plunder, Alert Outlaw, All-Evil Vigil, DS affixes 2, Overrealm kept; items: Flame Elementium 107.22 (107), Expansion Mod - Warlock 0.71 (41), Nether Kings Divine Remn 0.66 (40), Expansion Mod - Vanguard 0.42 (14), Sprout of Legends 0.04 (5), Matchless Ember 17.32 (5)

## Regular pet slots on this setup (59 candidate pets, every trio): Fuel trio = 0
   +0.0/min | Cloudgatherer - Surging Gold, Twilight Sparks, Chalk Spirit
   -2.7/min | Happy Chonky, Cloudgatherer - Surging Gold, Chalk Spirit
   -3.3/min | Cloudgatherer - Surging Gold, Chalk Spirit, Corgi Fighter No.32
   -3.3/min | Twilight Sparks, Chalk Spirit, Corgi Fighter No.32
   -3.4/min | Happy Chonky, Twilight Sparks, Chalk Spirit
   -3.6/min | Cloudgatherer - Surging Gold, Chalk Spirit, Starfish Chanter
   -3.7/min | Twilight Sparks, Chalk Spirit, Starfish Chanter
   -3.9/min | Cloudgatherer - Surging Gold, Twilight Sparks, Corgi Fighter No.32

# Search: 1152 setups (mechanic set x elite x Sinful x probe x DS affixes 0/2 x Overrealm with a Vigil), his tree lines, Fuel trio, ranked by net FE per in-map minute
rank | /min | +lottery | net/map | s | FE | cost | setup
 1 |  46.1 |  59.4 |   179 |  233 |  107 |  146 | Alert Outlaw, All-Evil Vigil, Sinful Plunder, DS x2, Overrealm
 2 |  45.4 |  58.7 |   176 |  233 |  107 |  163 | Alert Outlaw, All-Evil Vigil, Generous Elite, Sinful Plunder, DS x2, Overrealm
 3 |  45.2 |  58.6 |   176 |  233 |  101 |  133 | Alert Outlaw, All-Evil Vigil, DS x2, Overrealm
 4 |  44.1 |  57.5 |   172 |  233 |  101 |  150 | Alert Outlaw, All-Evil Vigil, Generous Elite, DS x2, Overrealm
 5 |  43.4 |  66.8 |    96 |  133 |  107 |  144 | Alert Outlaw, All-Evil Vigil, Sinful Plunder, DS x2
 6 |  43.2 |  56.5 |   168 |  233 |  113 |  173 | Alert Outlaw, All-Evil Vigil, Sinful Plunder, Flourishing probe, DS x2, Overrealm
 7 |  42.9 |  56.3 |   167 |  233 |  113 |  191 | Alert Outlaw, All-Evil Vigil, Generous Elite, Sinful Plunder, Flourishing probe, DS x2, Overrealm
 8 |  42.7 |  56.1 |   166 |  233 |  113 |  175 | Alert Outlaw, All-Evil Vigil, Sinful Plunder (A), DS x2, Overrealm
 9 |  42.5 |  55.8 |   165 |  233 |  113 |  193 | Alert Outlaw, All-Evil Vigil, Generous Elite, Sinful Plunder (A), DS x2, Overrealm
10 |  42.4 |  55.8 |   165 |  233 |  107 |  160 | Alert Outlaw, All-Evil Vigil, Flourishing probe, DS x2, Overrealm
11 |  42.2 |  65.6 |    94 |  133 |  107 |  162 | Alert Outlaw, All-Evil Vigil, Generous Elite, Sinful Plunder, DS x2
12 |  41.9 |  65.3 |    93 |  133 |  101 |  131 | Alert Outlaw, All-Evil Vigil, DS x2
13 |  41.8 |  55.1 |   162 |  233 |  107 |  177 | Alert Outlaw, All-Evil Vigil, Generous Elite, Flourishing probe, DS x2, Overrealm
14 |  40.8 |  54.4 |   155 |  228 |   83 |   97 | All-Evil Vigil, DS x2, Overrealm
15 |  40.2 |  52.6 |   169 |  252 |   77 |   95 | Alert Outlaw, Evernight Vigil, DS x2, Overrealm
16 |  40.2 |  52.5 |   169 |  252 |   81 |  108 | Alert Outlaw, Evernight Vigil, Sinful Plunder, DS x2, Overrealm
17 |  40.2 |  53.8 |   153 |  228 |   88 |  110 | All-Evil Vigil, Sinful Plunder, DS x2, Overrealm
18 |  40.0 |  63.4 |    89 |  133 |  101 |  148 | Alert Outlaw, All-Evil Vigil, Generous Elite, DS x2
19 |  39.9 |  53.3 |   155 |  233 |  118 |  220 | Alert Outlaw, All-Evil Vigil, Generous Elite, Sinful Plunder (A), Flourishing probe, DS x2, Overrealm
20 |  39.8 |  53.1 |   155 |  233 |  118 |  203 | Alert Outlaw, All-Evil Vigil, Sinful Plunder (A), Flourishing probe, DS x2, Overrealm
21 |  39.6 |  51.9 |   166 |  252 |   81 |  126 | Alert Outlaw, Evernight Vigil, Generous Elite, Sinful Plunder, DS x2, Overrealm
22 |  39.2 |  51.6 |   165 |  252 |   77 |  113 | Alert Outlaw, Evernight Vigil, Generous Elite, DS x2, Overrealm
23 |  38.9 |  52.2 |   151 |  233 |  107 |  174 | Alert Outlaw, All-Evil Vigil, Sinful Plunder, Fluorescent probe, DS x2, Overrealm
24 |  38.4 |  61.8 |    85 |  133 |  113 |  172 | Alert Outlaw, All-Evil Vigil, Sinful Plunder, Flourishing probe, DS x2
25 |  38.2 |  51.5 |   148 |  233 |  107 |  191 | Alert Outlaw, All-Evil Vigil, Generous Elite, Sinful Plunder, Fluorescent probe, DS x2, Overrealm
26 |  38.0 |  51.4 |   148 |  233 |  101 |  161 | Alert Outlaw, All-Evil Vigil, Fluorescent probe, DS x2, Overrealm
27 |  37.9 |  61.3 |    84 |  133 |  113 |  189 | Alert Outlaw, All-Evil Vigil, Generous Elite, Sinful Plunder, Flourishing probe, DS x2
28 |  37.9 |  51.2 |   147 |  233 |   79 |  119 | Alert Outlaw, All-Evil Vigil, DS x0, Overrealm
29 |  37.8 |  51.1 |   147 |  233 |   84 |  132 | Alert Outlaw, All-Evil Vigil, Sinful Plunder, DS x0, Overrealm
30 |  37.6 |  60.9 |    83 |  133 |  113 |  174 | Alert Outlaw, All-Evil Vigil, Sinful Plunder (A), DS x2
31 |  37.2 |  49.8 |   153 |  247 |   63 |   59 | Evernight Vigil, DS x2, Overrealm
32 |  37.1 |  60.5 |    82 |  133 |  113 |  191 | Alert Outlaw, All-Evil Vigil, Generous Elite, Sinful Plunder (A), DS x2
33 |  37.0 |  60.4 |    82 |  133 |  107 |  158 | Alert Outlaw, All-Evil Vigil, Flourishing probe, DS x2
34 |  36.9 |  50.3 |   144 |  233 |  101 |  178 | Alert Outlaw, All-Evil Vigil, Generous Elite, Fluorescent probe, DS x2, Overrealm
35 |  36.9 |  49.2 |   155 |  252 |   81 |  123 | Alert Outlaw, Evernight Vigil, Flourishing probe, DS x2, Overrealm
36 |  36.8 |  49.1 |   155 |  252 |   85 |  136 | Alert Outlaw, Evernight Vigil, Sinful Plunder, Flourishing probe, DS x2, Overrealm
37 |  36.7 |  50.3 |   140 |  228 |   65 |   83 | All-Evil Vigil, DS x0, Overrealm
38 |  36.7 |  49.2 |   152 |  248 |   99 |  122 | All-Evil Vigil, Lunar Stele Lunaria, DS x2, Overrealm | time: CN x1.2 (lunaria never run)
39 |  36.5 |  48.8 |   154 |  252 |   85 |  153 | Alert Outlaw, Evernight Vigil, Generous Elite, Sinful Plunder, Flourishing probe, DS x2, Overrealm
40 |  36.5 |  50.1 |   139 |  228 |   88 |  124 | All-Evil Vigil, Flourishing probe, DS x2, Overrealm

## Best per mechanic set
 46.1/min (+lot  59.4) | Alert Outlaw + All-Evil Vigil + Overrealm  | with Sinful Plunder, DS x2 | items: Flame Elementium 107.22 (107), Nether Kings Divine Remn 0.66 (40), Expansion Mod - Warlock 0.54 (31), Expansion Mod - Vanguard 0.31 (10), Sprout of Legends 0.04 (5)
 43.4/min (+lot  66.8) | Alert Outlaw + All-Evil Vigil              | with Sinful Plunder, DS x2 | items: Flame Elementium 107.22 (107), Nether Kings Divine Remn 0.66 (40), Expansion Mod - Warlock 0.54 (31), Expansion Mod - Vanguard 0.31 (10), Sprout of Legends 0.04 (5)
 40.8/min (+lot  54.4) | All-Evil Vigil + Overrealm                 | with , DS x2 | items: Flame Elementium 83.49 (83), Nether Kings Divine Remn 0.59 (36), Sprout of Legends 0.03 (4), Matchless Ember 12.91 (4), Goddess of Huntings Divi 0.36 (3)
 40.2/min (+lot  52.6) | Alert Outlaw + Evernight Vigil + Overrealm | with , DS x2 | items: Flame Elementium 76.64 (77), Expansion Mod - Warlock 0.48 (28), Nether Kings Divine Remn 0.35 (21), Expansion Mod - Vanguard 0.27 (9), Matchless Ember 11.94 (3)
 37.2/min (+lot  49.8) | Evernight Vigil + Overrealm                | with , DS x2 | items: Flame Elementium 63.09 (63), Nether Kings Divine Remn 0.35 (21), Netherrealm resonance 34.94 (3), Tomorrows Direction 0.48 (3), Matchless Ember 9.23 (3)
 36.7/min (+lot  49.2) | All-Evil Vigil + Lunar Stele Lunaria + Overrealm | with , DS x2 | items: Flame Elementium 98.86 (99), Nether Kings Divine Remn 0.59 (36), Matchless Ember 16.54 (4), Sprout of Legends 0.03 (4), Sacred Fossil 0.50 (3)
 35.2/min (+lot  47.7) | Evernight Vigil + Lunar Stele Lunaria + Overrealm | with , DS x2 | items: Flame Elementium 74.71 (75), Nether Kings Divine Remn 0.35 (21), Sacred Fossil 0.50 (3), Matchless Ember 11.82 (3), Netherrealm resonance 34.94 (3)
 34.1/min (+lot  54.5) | Alert Outlaw + Evernight Vigil             | with , DS x2 | items: Flame Elementium 76.64 (77), Expansion Mod - Warlock 0.48 (28), Nether Kings Divine Remn 0.35 (21), Expansion Mod - Vanguard 0.27 (9), Matchless Ember 11.94 (3)
 33.9/min (+lot  58.2) | All-Evil Vigil                             | with , DS x2 | items: Flame Elementium 83.49 (83), Nether Kings Divine Remn 0.59 (36), Sprout of Legends 0.03 (4), Matchless Ember 12.91 (4), Goddess of Huntings Divi 0.36 (3)
 28.7/min (+lot  49.9) | Evernight Vigil                            | with , DS x2 | items: Flame Elementium 63.09 (63), Nether Kings Divine Remn 0.35 (21), Netherrealm resonance 34.94 (3), Tomorrows Direction 0.48 (3), Matchless Ember 9.23 (3)
 27.9/min (+lot  48.9) | All-Evil Vigil + Lunar Stele Lunaria       | with , DS x2 | items: Flame Elementium 98.86 (99), Nether Kings Divine Remn 0.59 (36), Matchless Ember 16.54 (4), Sprout of Legends 0.03 (4), Sacred Fossil 0.50 (3)
 25.5/min (+lot  46.5) | Evernight Vigil + Lunar Stele Lunaria      | with , DS x2 | items: Flame Elementium 74.71 (75), Nether Kings Divine Remn 0.35 (21), Sacred Fossil 0.50 (3), Matchless Ember 11.82 (3), Netherrealm resonance 34.94 (3)
 19.3/min (+lot  46.9) | Lunar Stele Lunaria                        | with , DS x2 | items: Flame Elementium 65.75 (66), Sprout of Legends 0.10 (12), Netherrealm resonance 39.38 (4), Flawless Lunar Dust 0.10 (2), Luminous Lunar Dust 0.62 (1)
 18.2/min (+lot  37.5) | Alert Outlaw + Lunar Stele Lunaria         | with Sinful Plunder, DS x2 | items: Flame Elementium 67.26 (67), Expansion Mod - Warlock 0.54 (31), Expansion Mod - Vanguard 0.31 (10), Tomorrows Direction 0.95 (5), Sprout of Legends 0.03 (4)
 17.0/min (+lot  38.6) | Alert Outlaw                               | with , DS x2 | items: Flame Elementium 36.91 (37), Expansion Mod - Warlock 0.48 (28), Expansion Mod - Vanguard 0.27 (9), Tomorrows Direction 0.63 (3), Sprout of Legends 0.03 (3)
 -6.2/min (+lot  59.1) | Divine Warrior Dark Surge                  | with , DS x0 | items: Flame Elementium 18.17 (18), Netherrealm resonance 83.36 (7)

## Exponents the data could not pin (bar > 0.4 or negative), set to the text's 1 and refitted: outlaw Expansion_Mod_-_Warlock: a; outlaw Nether_Kings_Divine_Remnant: a/b; outlaw Expansion_Mod_-_Vanguard: a; outlaw Sprout_of_Legends: a/b; outlaw Sacred_Fossil: a/b; outlaw Flawless_Lunar_Dust: a/b; outlaw Expansion_Mod_-_Tank: a; vigil Nether_Kings_Divine_Remnant: a; vigil Expansion_Mod_-_Warlock: a/b; vigil Expansion_Mod_-_Vanguard: a/b; vigil Sprout_of_Legends: a/b; vigil Sacred_Fossil: a/b; vigil Tomorrows_Direction: a; vigil Netherrealm_resonance: a; vigil Goddess_of_Huntings_Divine_Remnant_-_Legendary: a; lunaria Flame_Elementium: a; lunaria Expansion_Mod_-_Warlock: a/b; lunaria Nether_Kings_Divine_Remnant: a/b; lunaria Flawless_Lunar_Dust: a; lunaria Expansion_Mod_-_Vanguard: a/b; lunaria Sprout_of_Legends: a/b; lunaria Sacred_Fossil: a/b; lunaria Luminous_Lunar_Dust: a; lunaria Crude_Lunar_Dust: a; lunaria Netherrealm_resonance: a; lunaria Tomorrows_Direction: a/b; darksurge Flame_Elementium: a/b; darksurge Expansion_Mod_-_Warlock: a/b; darksurge Expansion_Mod_-_Vanguard: a/b; darksurge Netherrealm_resonance: a/b
