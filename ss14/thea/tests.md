# Thea — test log

Metric: "Highest DPS in the last 5 seconds" on the boss dummy (= best 1-second window). Dummy display
caps at 10 T and hits cap at 5 T, so from 2026-10-26 on, tests are done with the belt off (÷2.75).
Quad-damage RNG gives roughly ±10% on a single pull.

## 2026-10-25 — calibration (baseline 9.0 T, supports ST / Manifold / Lightchaser / Multiple Proj / Condensed Cold, Spell Ripple on)
| Change | Measured | Model said | Notes |
|---|---|---|---|
| Spell Ripple off | 6.0 | — | Ripple ≈ ×1.5 |
| Belt (Gale) off | 3.3 | 3.6 | Gale ×2.48 confirmed as additional proj dmg |
| Biting Cold off | 5.5 | ~5.9 | Deepened Curse goes with it |
| Precise Projectiles off | 7.1 | ~7 | |
| Lightchaser off | 7.9 | ~7.9 | |
| Lightchaser + Multiple Proj off | 5.3 | 5.3 | |
| Frostbite effect −20% | 8.4 | ~8.4 | |
| Mass Effect off (Empowers) | 7.5 | ~7.5 | |
| No dash (Hunting, Weakness Infiltration) | 6.5 | ~7.0 | Weakness Infiltration probably does nothing |
| No dormant, 2 tangles | 3.8 | ~3.9 | Dormant ×1.8 |
| Wand S off | 1.4 | 1.75 | unresolved |
| Secret Origin Unleash off | 5.4 | ~5.5 | |
| Witch off (465 INT) | 5.5 | ~5.5 | |
| Dreamweaver off (513 INT) | 4.5 | ~4.6 | |
| Prophecy of Purity off | 4.4 | 4.4 | 1 Boon stack |
| Lightning Storm off (−2 ailments) | 5.5 | ~5.6 | Dirty Tricks per type |
| Ring R off (arp ring) | 4.45 | 4.3 / 4.6 | between the two armor reads |

## 2026-10-25 — supports and wands
| Config | Measured | Model | Notes |
|---|---|---|---|
| Target Projection in place of Lightchaser | 9.9 | 10.1 | TP = ×1.277 (Enhanced Mark × Mark crit taken) |
| ST / Manifold / MP / TP / CC (LC out) | 10.0 (cap) / belt off 3.5 | 3.6 | |
| Overload lv35 (4.75%/Focus) in a support slot | 8.9 | 9.2 | lost to TP |
| Final: ST / Manifold / Lightchaser / TP / CC | — | — | Vlad keeps Lightchaser + TP |

## 2026-10-26
| Config | Measured (belt off) | Model | Notes |
|---|---|---|---|
| After Hasten boots + kismet res swap, Purity on | 5.5 | — | ≈ 15 T with belt |
| Purity off | 2.4–2.7 | 2.71–2.86 | quad RNG |
| Base Trait slot memory → Wisdom L4 (44%) | 8.7 | 8.3 if Wisdom doubles / 7.4 if not | **Wisdom doubles with 2 Boons — confirmed** |
| New Nether King + Sparks, both GoK slates on the line (Hunting out, Frail/DD/INT lost) | 8.6 | 8.3 | Sparks copy escapes Judgment's −30% → +1 becomes +2 |
| Slate roll: +30.8% frostbite effect | 10.0 | ~9.9 | |
| Belt off + "INT ring" off | 9.7 | — | Vlad: "I'm way higher than 27.5 T". Ring L alone should be ~×1.2, so 10 → 9.7 means something else was meant, or the 10 was a lucky pull (?) |

## 2026-10-27 — new Spell + Cold GoK slate
| Config | Measured (belt off) | Model | Notes |
|---|---|---|---|
| New GoK #2 (+1 Cold, +1 Spell, Arcanist Focus, +6% life/ES, +12% area/proj speed), belt off + Ring L (INT ring) off | 9.4 | 9.55 | -1.6%. Ring off to stay under the 10 T display cap. Model belt-off without the ring removal: 12.78 T; with belt 34.0 T. Ring assumed L (Ring R off would be 6.1). |
| SOU cast-speed test (10 Focus): both out / WFB x3 / ME / both | 231 / 240 / 247 / 256 | 231 / 239.8 / 247.2 / 256 (empower 2.042) | Mass Effect full confirmed |
| Standing still (Speed Phantom not cast), belt off + Ring L off | 6.8 | 8.55 | +26%: absolute scale off; Speed Phantom share x1.382 measured vs x1.485 |

## 2026-10-28 10:45 — Blizzard FP 246% in Speed Phantom's slot (assumed), boss dummy, display caps at 10 T
| config | measured | model (DE x1.404, scale 0.767) | H1: DE dead, scale 1.077 | H2: DE works, all x1.39 |
|---|---|---|---|---|
| no belt, no ring L | >= 10 (cap) | 11.7 | 11.7 | 16.3 |
| + no Domain Expansion | >= 10 (cap) | 8.4 | 11.7 | 11.6 |
| + no Spell Amp | **8.0** | 5.75 | **8.1** | 8.0 |
| decisive: no belt/ring/SA, DE ON | ? | 8.1 | **8.1** | **11.2 (cap)** |
- H1 also reproduces yesterday's 9.4 / 6.8 exactly (DE x1.404 x 0.767 = 1.077 ~ the old constant was DE). H2 needs a new x1.39 that wasn't there yesterday.
- Real full DPS: H1 41.5 T · H2 57.8 T. Pending the decisive pull (and confirmation that Blizzard is in).
- 10:51 Vlad: no belt / ring / Spell Amp with DE ON = >= 10 (cap) -> **DE works (>= x1.25); H1 rejected.** Real full DPS = 8 x 7.22 = **~58 T**.
  The model is x1.39 low at these configs. Fits if Blizzard is worth ~x2.4, not the modeled x1.71 (2 debuff stacks: 4 s duration on a 2 s CD -> 1 + 2 x 70.7%);
  needs >= x1.86 even at DE/SA floors. Decisive: the 8 T config with Blizzard off -> 4.7 T (1 stack) vs 3.3 T (2 stacks).

## 2026-10-28 11:31 — Blizzard stacks (no belt / ring L / Precise Proj / Spell Amp, Swiftness in DE's slot)
| config | measured | model (1 stack, dummy 1.0) | notes |
|---|---|---|---|
| as above (repeat of 10:57) | 5.2 | 5.25 | 10:57 read 5.3 |
| + Blizzard off | 3.0 | 3.08 | **Blizzard x1.733 = 1 stack** (model x1.707; 2 stacks would be x2.41 -> 2.2 T) |
- Refit: today's six absolute pulls rms 3.2% with **no constant** (dummy_scale 1.0). Yesterday's 9.4 / 6.8 fit at 0.767 (kept as era context).
| no belt / ring L / SA / PP, Precise WA -> Swiftness (Lightchaser -10 r5, CC +29 r5) | 7.4 | 6.86 at the old scale -> refit 0.917 | full kit 82 T |

### 2026-10-31 18:13 — new robe (rare chest), aura effect 68% -> 79% [Vlad, sheet; tree changed a lot, engine not re-anchored]
| config | in game | note |
|---|---|---|
| naked robe, auras off | 3 T | |
| naked robe, auras on (68% aura effect) | 25 T | Precise Projectile x1.64 (17% proj speed), Spell Amp x1.68, Precise Weapon Amp x1.75, Frigid Domain x1.69 (product x8.15) |
| robe T1 INT / T2 aura effect 11% / T1 crit rating, auras off | 4 T | |
| same, auras on (79% aura effect) | 36 T | x1.69 (18% proj speed) / x1.72 / x1.80 / x1.73 (product x9.05) |
- Each aura's bonus scales with (1 + aura effect): bases Spell Amp 40.5%, Precise Weapon Amp 44.6%, Frigid Domain 41.1%, Precise Projectile 38.1% (+ its
  proj-speed part); predicted at 79%: x1.725 / x1.799 / x1.735 / x1.682 vs read x1.72 / x1.80 / x1.73 / x1.69. +1% aura effect = +0.95% damage at 79%.
