# Thea — SS14 Tartarus — current build

## Re-sync 2026-10-30 19:57 (screenshots; overrides the older sections below where they differ)
- **Belt** Elder Sage Girdle (rare, ilvl 100), base Gale + Hasten: T0 +19% Attack and Spell Block · T0 +410 max ES · T1 -15% additional damage taken at
  Low Mana · T0 +12% Elemental Res / +13% avoid Elemental Ailments · T0 +34% Cold Res · T2 +18% Double Damage. (The old Magic Girdle's +31 INT / +47% damage are gone.)
- **Boots** Long Night Sorcerer's (ilvl 89): T1 +58% crit dmg mitigation · T1 +60% gear ES · T1 +304 gear ES · T1 +56% Crit Damage · T2 +18% Erosion Res · T1 +40% MS. No Hasten line any more.
- **Ring L** Perishing Inferno Flame (ilvl 86), base +12% fire res: T1 +15% Attack and Spell Block (was +52 INT) · T1 +323 ES · T1 +68% damage · T1 +20% lightning · T1 +25% erosion · T1 +114% crit rating.
- **Ring R** Eternal Sleep Ice (Priceless, ilvl 100), base +12% cold res + Spell Aggression: T0 +404 ES · T0 +85% damage · T1 +20% Elemental and Erosion Res Penetration (was armor pen) · T1 +31 max frostbite · T0 +35% fire res · T1 Barrier per 5 m.
- **Wands** both Headless Cleric (Priceless, ilvl 100), base +40% spell dmg, +8% additional spell dmg. M: T1 +2 Cold / T1 +2 Physical skill level · T0 adds 87-106 phys · T1 +37% double · T1 +47% Tangle Dmg Enh · T0 +132% Elemental Dmg.
  S: T2 +2 Spell / T1 +2 Physical skill level · T0 adds 84-112 cold · T0 +226% crit rating · T0 +47% cast · T1 +40% double.
- **Trait-slot memory** (Epic Progress 40/40, +4 trait): +15% cast · +10% minion AS · +2 hero trait level · +9% Attack Block · +5% Spell Block (to be rolled to 9). The two crit dmg lines are gone.
- **Slates**: Fallen Starlight lv89 on the line (+40%): +5.6% cold res · +4.2% life/ES · +3 Horizontal Projectile Penetrations · +16.8% INT. Fallen Starlight lv86 off the line: +3% life/ES ·
  +10% attack crit / +3% crit dmg · +8% CDR +1 charge · +12% Spell Block / +15% ES from shield. Pedigree = Dirty Tricks. (Corner of Divinity: unconfirmed, see Open.)
- **Kismets** (13): 3 Medium Block Ratio (6) · 1 Fluffy Ball (medium, 40-60% crit dmg mitigation) · 3 Micro Lightning Res · 1 Micro Crit Dmg · 5 Micro INT. Model: +18% ratio, +68 INT, +18% light res, +13% crit dmg.
- **Trees** (113 pts): GoK 26 (+18% dmg medium now 3/3) · Magister 26 (crit micro/medium at 352_80/480_80 out, +4% spell block micro x3 + 12% spell block legendary in) ·
  Prophet 24 (cold res legendary out, cold res micro 1/3; prism slot pending the Phantasmagoria) · Lich 37 (+352_272 x3, +480_272 ES/Blur legendary).
- **Block from the model = in game**: attack 30 (dual wield) + 19 + 15 + 9 = 73 · spell 19 + 15 + 5 + 12 + 24 = 75 · ratio 30 + 18 = 48.
- **Res (model, gear+slates+kismets)**: fire 59 · cold 68 · lightning 50 · erosion 43 (cap 75).
- Engine after the sync: 33.3 T belt off / 82.5 T belt on, but the regression pulls were taken on the old gear (tests now 10-30% off): needs a fresh sheet + belt-off pull.
- Open: Corner of Divinity still equipped? Prophet: Spell Ripple still installed, and is Frozen Lotus the core now? Memory slot 1 lines (build.json has 5, the 10-27 note says INT only).


**Boss setup** (Vlad 2026-10-28). For clearing he swaps about half of it: Lightchaser, Swiftness, Blink, 2 different pets. Not modeled; boss upgrades carry over.

Wisdom of The Gods. Chromatic Shot cast through Spell Tangle, 100% phys → cold, dual Priceless wands,
God's Boon held at 2 stacks permanently. Last full sync: 2026-10-26. Lines marked **(?)** need a fresh
screenshot from Vlad.

Current DPS on the boss dummy: **10 T with the belt off** (2026-10-26 13:34) → ~27 T with it
(belt factor ×2.75). 9.7 T with belt AND Ring L off. Hit cap 5 T; per hit ~2 T.

## Sheet (2026-10-26 13:47, hitting the dummy, everything up)
Damage bonus 544% · cold 142% · cast speed 262% (6.44 casts/s per tangle) · crit 71.67% (crit rating bonus 785%) ·
crit damage 515% · projectile speed 213% · INT 543 / STR 152 / DEX 45 · max Focus 10 ·
skill effect duration 59% · CDR 30% · frostbite effect 104.8% · max frostbite 101 (?) · cold pen 24.8 · armor pen 10.
Machine-readable copy: `stats.json`.

## Hero trait
- Wisdom of The Gods **L4**: +44% additional per Boon stack if it consumed max Focus, 10 s, CD 15 s (Base Trait slot memory gives +2 trait levels).
- Predicted Reincarnation L3: +50% additional Boon CDR; +8% additional per Focus consumed, max 5 → +40%/stack.
- Farewell Prophecy L3: +6% double per Focus consumed, max 8 → +48%/stack.
- Prophecy of Purity L3: +1 Boon stack (2 total), +5% skill effect duration.
- Boon at 2 stacks: (1 + 0.88) × (1 + 0.80) = ×3.38; double +96. Duration 10 × 1.59 = 15.9 s vs cooldown 15 / (1.5 × 1.30) = 7.7 s → permanent.

## Hero memories (all 50/50)
- Slot 1 Memory of Origin lv86: +110 INT · +16% cast · (purple) +18% minion crit dmg · +47% cold skill crit dmg (T1) · +40% projectile speed (T1)
- Slot 2 Memory of Discipline lv86: +642 max ES · +16% cast · (purple) +28% minion dmg · +41% spell crit dmg (T1) · +40% projectile speed (T1)
- Slot 3 Memory of Progress lv89: +30% MS · +10% skill effect duration · (purple) +40% minion crit rating · +104% spell crit rating (T0) · +54% spell crit dmg (T0)
- Base Trait slot: Epic Memory of Progress 40/40, trait +4, values already cut 58%: +15% cast · (purple) +10% minion AS · +2 hero trait level · +18% spell crit dmg · +18% cold skill crit dmg

## Gear
- **Helmet** Malign Embrace (corroded) lv89: +347 gear ES · +2 max Tangles · +155 spell crit rating and +21% additional damage on crit per activated Tangle · nearby enemies guaranteed crit. Energy 58.
- **Chest** Iced Drinker's Cage (corroded) lv93: +338 gear ES (+170 base) · main skill level +0 · Extreme Coldness (+50 max frostbite, cold only) · 1 Cage stack per frostbite (1 s) → 4 stacks ×1.14^4 damage, ×0.93^4 DoT taken · +33% control effects received. Energy 122.
- **Neck** I Am Truth (corroded) lv88: +5 INT (base) · +4 all skill levels · +99 STR · +40% skill effect duration.
- **Gloves** Israfel's Laws (corroded) lv90, All Magic Grip base (120 ES): +349 gear ES · +25% blessing duration · +14% additional cold per Focus stack · +1% crit dmg per Focus stack. Energy 61.
- **Belt** Magic Girdle (rare) lv83, base affix **Gale**: +31 INT · +220 max ES · +47% damage · +19% lightning / +17% cold / +16% erosion res. Worth ×2.75 total.
- **Boots** Long Night Sorcerer's Boots (rare INT) lv89: +58% crit dmg mitigation · +60% gear ES · +304 gear ES · +40% MS · **Hasten** (+8% additional cast, +8% cast, +8% additional MS) replaced one res line (lightning or fire (?)) · remaining res line (?). Energy 61.
- **Ring L** Perishing Inferno Flame Ring (rare) lv86, base +12% fire res. Prefix: T1 +52 INT · T2 +221 ES · T1 +64% damage. Suffix: T2 +18% lightning res · T1 +27% erosion res · T1 +120% crit rating.
- **Ring R** Eternal Sleep Ice Ring (Priceless) lv100, base +12% cold res + Spell Aggression on spell cast: +210 max ES · T0 +81% damage · T2 +10% armor DMG mitigation pen · T2 +20 max frostbite · +27% fire res · Barrier per 5 m moved.
- **Wand M** Headless Cleric Wand (Priceless) lv100, base +40% spell dmg, +8% additional spell dmg. Energy 40.
  - Prefix: T1 +2 Cold Skill Level · T1 +2 Physical Skill Level · T0 Adds 87–106 Physical Damage to Spells
  - Suffix: T1 +37% double damage · T2 +34% Tangle Damage Enhancement · T1 +106% Elemental Damage
- **Wand S** Headless Cleric Wand (Priceless) lv100, base +40% spell dmg, +16% cast. Energy 59.
  - Prefix: T2 +2 Spell Skill Level · T1 +2 Physical Skill Level · T0 Adds 84–112 Cold Damage to Spells
  - Suffix: T1 +166% Critical Strike Rating · T0 +47% Cast Speed · T1 +40% double damage

## Skills
- **Chromatic Shot** (Spell/Projectile/Area/Physical, cold via Condensed Cold), lv ~38 (2026-10-28 screenshot): Activation Medium: Tangle (T1, roll 11%) · Overload · Condensed Cold (Noble T1, roll +20% additional) · Multiple Projectiles · Target Projection. Lightchaser, Manifold, Spell Tangle out.
- **Aim** (Empower): Preparation · Well-Fought Battle · Mass Effect.
- **Secret Origin Unleash** (Empower): Preparation · Mass Effect · Well-Fought Battle · Resurgence.
- **Biting Cold** (Curse): Preparation · Terrain of Malice · Deepened Curse · Increased Area.
- **Speed Phantom** (Mobility/Empower): Quick Mobility · Weakness Infiltration · Exhaustion. (Weakness Infiltration's +30% Infiltration effect probably not doing anything.)
- **Auras** (Aura Amplification lv29 on each): Precise Projectiles [Restrain, Increased Area, AA] · Spell Amplification [AA, Increased Area, Restrain] · Frigid Domain [Restrain, CDR, AA] · Domain Expansion [AA, Seal Conversion → sealed life, enables Lich +10% "both sealed"]. Sealed mana 2.94%, life 6.73%.

## Talent trees (110 pts)
Node values are per rank × ranks. Coordinates x_y from the old JSON (x = column 0/3/6/9/12/15/18 → 96..864, y = row 80..464).

### Goddess of Knowledge — 26 · cores Peculiar Vibe (12) + Acquaintance (24, Dormant Entanglement + 25% additional spell)
- +9% dmg micro ×3 → +18% dmg medium ×3 (+81% dmg)
- +3% cast/+2% MS micro ×3 → +6% cast/−4 cost/+4% MS medium ×3 (+27% cast, +18% MS) — kept for the MS
- +9% spell dmg micro ×3 → +1 Spell Skill Level legendary
- +10% Focus duration/+10% dmg w/ Focus micro ×3 → +1 Max Focus legendary
- +6% area/+6% proj speed micro ×3 → +12% area/+12% proj speed medium ×3 (+54% proj speed, +18% area)

### Magister — 24 · core Bunch (+1 max Focus, +3% additional spell dmg per Focus)
- +15% spell crit micro ×3 → +20% crit/+5% crit dmg medium ×3
- +10% Focus duration/+10% spell dmg w/ Focus micro ×3 → legendary: Focus stack on Spell Burst consume / Tangle cast
- +10% Focus duration/+4% cast w/ Focus micro ×3 → +5% spell crit dmg per Focus legendary
- +8 INT micro ×3 → +12% INT legendary
- +3% max ES micro ×3 → +6% max ES medium ×3

### Prophet — 27 · core slot = Ethereal Prism **Spell Ripple** (main-spell hit 50% → pulse of 150% hit as True dmg)
- Prism sits on the 12-pt +4% frostbite effect micro (that node is lost); 3×3 area: mediums +2% sealed mana comp; "2 legendary mediums in area → 100 Blur" not active.
- +15% crit micro ×3 → +20% crit/+5% crit dmg medium ×3
- +2 max frostbite micro ×3 → +5 max frostbite medium ×3 → +10% additional vs Frozen legendary
- +8% frostbite effect medium ×3 → +20% frostbite effect legendary
- +3% life/ES micro ×3 → +6% life/ES medium ×3
- +4% cold res micro ×3 → +18% cold res legendary

### Lich — 33 · core Off The Beaten Track (+4 support levels, support mana multiplier fixed 95%)
- +15% crit micro ×3 → +20% crit/+5% crit dmg medium ×3
- +9% dmg micro ×3 → +6% atk/cast medium ×3 → +1 all skill levels legendary
- +5 all stats micro ×3 → +10 all stats medium ×3
- 1.5% CDR micro ×3 → +8% CDR +1 charge legendary
- +3% life/ES micro ×3, +6% life/ES medium ×1
- +3% atk/cast micro ×2
- +3% life/ES micro ×3 → +10% additional dmg with both sealed mana and life legendary

Tree crit total 315% (Magister/Prophet/Lich 105 each).

## Divinity slates (layout changed 2026-10-26)
- **Nether King's Divinity** (the 4.5k one): Judgment active; brand "+10% effect increase multiplier for non-legendary Divinity slates along the connecting line" (−30% from Judgment → 7%). Lost vs the old one: Frail on spell damage, the +11% double, +12% INT. Skull cells: top-left, top-right, bottom-right.
- **Sparks of Moth Fire**: adjacent to the Nether King, copies the +10% brand at full value → slates on the line show **Effect +54%**, so "+1" lines are "+2".
- **GoK slate #1** (L, lv89, on line, 54%): +1 Cold Skill Level · +1 Max Focus (GoK node) · +5 Max Frostbite · +20% Frostbite Effect · Cold Infiltration (2026-10-27 re-read)
- **GoK slate #2** (F, lv86, on line, 54%, new 2026-10-27): fixed +1 Cold Skill Level, +1 Spell Skill Level · purple +6% life / +6% ES · Arcanist +1 Max Focus (MAD1) · medium +12% area / +12% proj speed. Bought S+C base 400 + one Arcanist pact 84.
- **Fallen Starlight**: +skill effect duration, +CDR +1 charge, fire DoT/ignite lines. Now off the boosted line (?).
- **Pedigree of Gods** (core slot): Dirty Tricks · +10% Agility duration & +3% atk/cast w/ Agility · +8 STR · crits eliminate below 8% life.
- Hunting slate removed. Three empty cells form a corner shape (unboosted).

## Pactspirits (all ranks active)
- **Witch of the Night** r6: Night Feather Entanglement (1 stack per active tangle, max 2; +7% additional tangle dmg and +3% CDR per stack, ×1.5 effect) · +8% additional spell dmg while NFE · 1 Focus per 1 s at max NFE. Free minors: spell crit 22+22+45.
- **Iron Lion** r1: first line only. Free minors: proj speed 7+7+14, proj dmg 10+10+20.
- **Dreamweaver** r6: +19% additional elemental dmg for spells · up to 4.8% + 12% ele pen · +4% additional. Free minors: ele pen 2+2+4, ele dmg 12+24.
- **Kismets (Destinies)**: 13 slots, originally all INT. Since 2026-10-26 some INT kismets swapped to lightning res (4 micros, 5–7 each) to free a boots res line for Hasten. Current layout (?). Values: INT micro 12–15 / medium 24–30; lightning micro 5–7 / medium 10–14.

## Follower (Tartarus)
- Tidewell III [Additional Ignite, Glacial Freeze]: water +20% double for spells inside; Ignite; Cold Infiltration on frostbitten (+13% additional cold taken).
- Lightning Storm III [Improved Corrosion, Coercion]: Numbed, Wilt, Paralysis (CC).
- Swift Shadow Raid III [Periodic Burst, Deep Wounds]: +40% proj speed 4 s, +20% atk/cast 4 s, Trauma.
- Ailment types on the boss for Dirty Tricks: Frostbite, Freeze, Ignite, Numbed, Wilt, Trauma = 6 → ×1.97.

## Kismets / block (2026-10-30 19:49, Vlad)
- The big INT kismets are gone; 3 Medium Fate: Block Ratio (6 each) -> block ratio 48%; attack block 73% (incl. +30% from dual wielding), spell block 75%.
  Prophet being reselected (24 pts in the screenshot: cold res legendary and 2 ranks of the +4% cold res micro dropped). Direction: Prophet + Lich stay,
  Pedigree = Dirty Tricks, Phantasmagoria (micro, aura effect) on Prophet 352_176, block capped through kismets, Vorax chest to refund INT/res.

## Kismets (2026-10-27, Vlad's totals)
- 13 destinies: +152 INT · +14% crit dmg · +20% lightning res · +60% crit strike damage mitigation. Slots: Witch 6 (Spell Dmg I x2, Spell Dmg II, Cast I x2, Cast II positions), Iron Lion 3 (knockback positions), Dreamweaver 4 (Ele Dmg I, Cast I x2, Cast II).

## Skills / memories / followers re-read (2026-10-27 12:38)
- Chromatic Shot: Activation Medium: Tangle T1 11%, Overload, Condensed Cold (Noble) T1, Multiple Projectiles, Target Projection (2026-10-28).
- Aim [Preparation, Well-Fought Battle, Mass Effect] · SOU [Preparation, Mass Effect, Well-Fought Battle, Resurgence] · Biting Cold [Preparation, Terrain of Malice, Deepened Curse, Increased Area] · **Speed Phantom [Quick Mobility, Weakness Infiltration, Mass Effect]** (Exhaustion out).
- Auras: Precise Projectiles [AA, Restrain, Increased Area] · Spell Amplification [Restrain, AA, Increased Area] · Domain Expansion [AA, Restrain, CDR] · Frigid Domain [Seal Conversion, AA].
- Memories: slot 1 **Memory of Origin, revived**: +176 INT only (+60% base stat) + revived affix "Base Trait slots" (the old cast/cold crit dmg/proj speed lines are gone) · slot 2 Discipline +642 ES, 16% cast, 28% minion dmg, 41% spell crit dmg, 40% proj speed · slot 3 Progress lv89: 30% MS, 10% duration, 40% minion crit, 104% spell crit rating, 54% spell crit dmg · base trait slot: Epic Progress lv86 40/40 (cut 58%): 15% cast, 10% minion AS, +2 hero trait level, 18% spell crit dmg, 18% cold crit dmg.
- Traits: Wisdom of The Gods L4; Predicted Reincarnation, Farewell Prophecy, Prophecy of Purity L3.
- Followers: Tidewell III [Additional Ignite, Glacial Freeze] · Lightning Storm III [Improved Corrosion, Coercion (Paralysis)] · Swift Shadow Raid III [Periodic Burst, Deep Wounds].
