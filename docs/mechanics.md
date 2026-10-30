# Mechanics — the damage chain and verified rules

Status tags: **[tlidb]** = stated on tlidb, **[tested]** = confirmed by an in-game pull (see the
character's `tests.md`), **[Vlad]** = Vlad stated it from in-game, **[model]** = our working
assumption, consistent with tests but not proven on its own.

## Hit DPS chain

```
DPS = Base
    × (1 + Σ increased%)                       one pool: damage + spell + projectile + cold/elemental + ...
    × Π (1 + additional_i)                     every distinct additional source multiplies
    × level multiplier                         (it IS an additional multiplier, listed separately for clarity)
    × enemy-side                               frostbite, curse, frail, infiltration, mark, paralysis, res, armor
    × crit factor
    × double/quad factor
    × projectiles that hit
    × casts per second × casting sources (tangles)
```

### Base and flat [tlidb][tested]
- Base = skill base damage at its level (Chromatic Shot: 498–831 phys at lv20, avg 664.5; base stops growing after 20).
- Flat "Adds X–Y damage to spells" goes into base, scaled by the skill's **added-damage effectiveness** (Chromatic Shot 123%).
- Because the base is small and the increased pool is huge, flat lines beat %-damage lines of the same tier (tested on wands: T0 flat phys ×1.18 vs the 75% spell line it replaced ×1.09).

### Skill levels [tlidb]
- Past lv20 base damage stops; each level **21–30: +10% additional (multiplies)**, **31+: +8% additional (multiplies)**. lv36 = 1.1^10 × 1.08^6 = ×4.116.
  tlidb Skill Level help (verbatim): "After the skill exceeds Lv. 20, its Base Damage and the Base Damage of its Minions will no longer change. However, for every level beyond this level, this skill and its Minions will gain additional damage. At Lv. 21 - 30, each level +10% additional damage (multiplies) At Lv. 31 or higher, each level +8% additional damage (multiplies)."
  **No cap at 40**: skill tables on tlidb stop at 40, but the rule says 31 or higher. Lv41 = another x1.08 (~85% confident; no 41+ pull yet). Ignore the old loading-screen Tip #1044 ("+6% past Lv. 30"), it contradicts the help page and Chromatic's own table (base stops at 20).
  Chromatic is Lv40 in game with the S+C slate (model 40, 2026-10-27).
- Level sources stack by tag: all-skills, spell, cold, physical, projectile, main-skill. Supports and auras get their own levels (support +X levels, Off The Beaten Track +4 support levels).

### Increased vs additional [Vlad][tested]
- All "increased" (no word "additional") of the types that apply add into one pool. On Vlad's sheet "damage bonus" = damage + spell + projectile; cold/elemental shown separately but in the same pool.
- "additional" modifiers from different sources multiply.
- Stacks of the **same** buff add before multiplying (Focus Blessing 5%/stack → 10 stacks = +50%, not 1.05^10; God's Boon stacks add within each of their bonuses).
- Text that says **"(multiplies)"** compounds per stack (Iced Drinker's Cage 1.14^4, Dirty Tricks 1.12^n, skill levels).
- On-person conditional additionals of the same kind add with each other ("+10% additional vs Frozen" + "+15.4% additional vs Frozen" = +25.4%). Enemy-side "taken" modifiers multiply with each other.

### Crit [tlidb]
- Final rating = Σ base rating × (1 + Σ increased%) × Π(1 + additional). Spells use the spell's base rating: **500**. Flat rating (e.g. Malign Embrace per tangle) adds to the base.
- Crit chance = rating / 100 (%). Capped at 100%.
- Crit damage base 150%. Crit factor = (1 − p) + p × CD × (on-crit multipliers, e.g. Malign's +21% additional per active tangle → ×1.42 at 2 tangles).

### Double / quad [tlidb][Vlad][tested]
- All double-damage chances sum. Over 100%, the overflow is quad chance, total capped at 200%.
- Factor: chance ≤ 100: 1 + c; chance > 100: 2 × (1 + min(1, c − 1)). At ≥200% every hit is ×4.
- Vlad sits at the cap with Tidewell water up, so extra double chance is worth ~nothing on a boss.

### Cast speed [tested]
- casts/s = skill base (Chromatic 1.54) × (1 + Σ increased cast%) × Π additional (Spell Aggression ×1.07, Hasten ×1.08).
- Aim's −16% cast is flat and NOT scaled by Empower effect.
- Tangles cast the linked spell at the player's cast speed (not Activation Medium's 0.4 s).

### Projectiles [tested]
- **Chromatic supports in the engine (2026-10-28)**: only what's slotted counts. Activation Medium: Tangle [tlidb]: "+(11-15)% additional" T1 (T2 1-5, T0 21-25),
  auto-creates Tangles every 0.4 s below the cap, +1 Tangle per trigger. Overload: +4.7%/Focus stack at lv34, max 8 stacks. Multiple Projectiles: +18.6% at lv29
  x a projectile part 1.256 fitted from the 2026-10-25 pull (MP x1.49 total without Lightchaser). Spell Tangle lv34 +29.4%, Manifold +27.5%.
- Chromatic Shot fires 3 shots, shotgun falloff 80%. Lightchaser's tracking makes extra projectiles overlap (Multiple Projectiles was worth ~×1.33 with Lightchaser, not ×1.49).
- **Open (2026-10-27):** Iron Lion r1 (Sword Rain, outer ring) gives Projectile Quantity +2 → Chromatic should fire 5, but the engine counts 3 (1 + 0.8 + 0.64). The absolute pull still matches (9.4 vs 9.5 T), so the projectile factor is effectively calibrated, not derived. tlidb wording: "-20% base damage coefficient for subsequent Projectiles of Shotgun Effect"; "Shotgun Effect takes effect when dealing damage to the same enemy more than once" → reads as each extra shot at 80% (linear: 5 shots = 4.2, 7 = 5.8 → MP ×1.38, close to the measured ×1.33). Price anything that changes projectile quantity from a pull, not the engine. Losing Iron Lion would cost ~×0.62 on that read.

### Gale (Marksman core / belt base affix) [tlidb][tested]
- "60% of the Projectile Speed bonus is also applied to the additional bonus for Projectile Damage."
- Only the **increased** projectile speed bonus feeds it; "additional projectile speed" (Lightchaser) does not.
- Factor = 1 + 0.6 × proj_speed%. Belt-off tests match.

### Attributes on Chromatic Shot [Vlad][tested]
- +0.5% additional damage per point of STR+DEX+INT; Lightchaser raises it to 0.75%/point.

### Enemy side
- **Frostbite** [tlidb]: base rating 10; each rating point = +1% additional cold taken; Frostbite Effect scales that per-point bonus → factor 1 + rating × (1 + effect%)/100. **Frozen above 100 rating. Max Frostbite Rating is capped at 120** — any max-frostbite source past 120 is wasted. Frozen non-legendary bosses get Frost-Sealed 1 s every 3 s.
- **Freeze** counts as its own ailment type for Dirty Tricks.
- Additional Ignite / Improved Corrosion (lit, T1) add 1-1 base Ignite / Wilt damage, so a cold Tidewell ignites and a lightning Storm wilts [Vlad]. Dirty Tricks counts 6 on the dummy.
- **Dirty Tricks** [tlidb]: +12% additional hit damage (multiplies) per ailment type on the enemy. Ailments: Ignite, Frostbite, Freeze, Shock, Numbed, Trauma, Wilt. Frail/Weaken/Slow/Curse/Paralysis are NOT ailments.
- **Mark / Enhanced Mark** [tlidb]: Mark = −20% evasion, +10% additional crit damage taken. Enhanced Mark = +15% additional projectile damage taken for 3 s, counts as Mark (so also the +10% crit taken).
- **Target Projection** [tlidb]: inflicts Enhanced Mark on hit AND "the supported skill deals +X% additional damage to Marked enemies" (lv20 14.5%, lv29 16.6%, lv36 18%). On paper ×1.166 × 1.15 × 1.095 = ×1.47 at lv29. **[tested] it measured ~×1.25** (9.9 T replacing Lightchaser, which is worth ×1.14) — one part is not applying in game; unresolved which. Engine (2026-10-29): TP = 1.166 x 1.095 (Mark crit taken) = x1.277, Enhanced Mark proj-taken = 1.0; the fitted dummy constants were divided by 1.095 at the same time (they had absorbed it).
- **Resistance**: bosses 30% all res [Vlad]; penetration subtracts. **Penetration can take res below 0** [Vlad 2026-10-27] (tlidb's help only says so for ARP). 24.8 pen -> 5.2% left now.
- **Armor** [tlidb]: monster reduction = Armor / (0.9 × Armor + 30000), monster armor up to 27,273 → **50%** max. Only **60%** of armor reduction applies to non-physical damage → 30% vs a cold hit. Armor DMG Mitigation Penetration subtracts from that reduction and **can take it below 0** (extra damage taken) [tlidb Armor DMG Mitigation Penetration help] (10% pen → ×0.80). Vlad: use the 60% rule. **[model]** whether pen comes off before or after the 60%.

### Hit cap [Vlad]
- A single hit caps at **5 T**. The training dummy display caps at **10 T DPS**; measure with the belt off (Gale) and scale back up.
- "Highest DPS in the last 5 seconds" = the best single 1-second window.

## Buffs and blessings
- **Focus Blessing** [tlidb]: +5% additional damage per stack (added), base max 4, 10 s, gaining a stack refreshes all.
- **Agility Blessing**: +4% attack/cast and +2% additional damage per stack, base max 4.
- **God's Boon** (Thea, Wisdom of The Gods) [tlidb][tested]: consumes all Focus. Bonus per stack: Wisdom (L1 20 / L2 28 / L3 36 / L4 44 / L5 52% additional if it consumed max Focus, 10 s, CD 15 s) + Predicted Reincarnation (+8% additional per Focus consumed at L3, max 5) + Farewell Prophecy (+6% double per Focus consumed at L3, max 8). **Prophecy of Purity** gives +1 max Boon stack (2 total; 3 is impossible). Each bonus adds across stacks; different bonuses multiply. Two stacks are permanent when duration ≥ 2 × cooldown. Cooldown = 15 / (1.5 Reincarnation × (1 + CDR)); duration = 10 × (1 + skill effect duration).
- **Tangle duration** [tlidb Tangle rules]: base 8 s; at the cap a new Tangle replaces the oldest. Skill Effect Duration applies [Vlad 2026-10-28].
  Vlad: 8 x 0.7 (Peculiar Vibe -30% additional) x 1.59 (duration +59%), no Tangle Duration lines -> **8.9 s**. A dropped Tangle = Dormant x1.4 instead of x1.8 (-22%).
- The "+1 Max Charges" lines also reach God's Boon [Vlad]: 3 charges. It auto-casts at full Focus, so charges are spent as soon as they're up (nothing banked for
  when a stack expires); sustained it is still one Boon per cooldown, no uptime gain, boon_margin unchanged.
- **Tangles** [tlidb][Vlad]: base max 2, cap 4; attach to the highest-rarity enemy within 8 m; Peculiar Vibe = +1 Tangle that can be applied to enemies (global count, not per enemy). Unattached tangles are dormant. **Dormant Entanglement**: +40% additional tangle damage per inactive tangle. 2 attached + 2 dormant = 2 casts × 1.8.

## Defense
- **Block** [tlidb]: attack/spell block chance cap 100%; block ratio base 30%, cap 60% (raisable to 80%). Block applies to hits and reflection only — DoTs are never blocked. Defensiveness (Sentinel core) +25% block ratio.
- **Iced Drinker's Cage**: −7% DoT taken per stack (multiplies), 4 stacks → ×0.75.
- Player armor: reduction = Armor / (0.9 × Armor + 3000 + 300 × min(enemy level, 90)), max 80%, 60% vs non-physical.

## Systems
- **Talent panels** [Vlad][tlidb]: node values are per rank × rank. Columns gated at 0/3/6/9/12/15/18 points; cores at 12 and 24. A medium/legendary needs the micro before it (pairs) — price nodes as pairs, never singly.
- **Ethereal Prism**: installed on a non-core node (replaces it) and replaces the panel's core with its own; random affixes affect an area around it.
- **Divinity slates** [Vlad][tested]: purple (brand) lines can't be rerolled into yellow (fixed) lines.
  - Nether King **Judgment** boosts slates on its connecting lines; Judgment applies **−30% to its own brand talent effects** (so a "+10% effect" brand gives 7%).
  - **Sparks of Moth Fire** copies the last talent of each adjacent slate (not cores). The copy is not hit by Judgment's −30% → copied +10% brand gives the full 10. With ≥50% effect, "+1" lines become "+2" (tested: +1 Focus / +1 spell level → +2).
- **Hero memories**: a Base Trait slot takes an Epic-or-lower Progress memory at −58% base stats and random affixes (numbers shown in game are already cut).
- **Kismets (Destinies)**: installed into pact-page minor nodes, replacing their effect.
- **Pantheon's Elegy dirges** [Vlad]: Goddess of Hunting = Precise: Swiftness gains +120% attack and cast speed (scales with aura effect); Steel Vanguard = lv20 Swiftness Dew and Resistance Dew.

### Empower effect [tested 2026-10-27]
- SOU cast-speed test (Vlad, 10 Focus, 4 Agility): no SOU 207, both supports out 231, Well-Fought Battle only: casts 1/2/3/4 = 234/237/240/240 (+12.5% effect per cast, 3 stacks), Mass Effect only 247, both 256. SOU's 24% cast (3% x 8 Focus) scales x1.375 (WFB x3), x1.667 (ME), x2.04 (both). **Mass Effect is at full +67.5% (3 charges); empower effect 2.04 = model.**
- Follower (Tartarus) Periodic Burst = +20% atk/cast speed [Vlad] (the player support's text is +30% for 2 s — different skill).
- Weakness Infiltration on Speed Phantom: +30% Infiltration Effect taken -> Tartarus Cold Infiltration 13% -> 16.9% while Speed Phantom hits (modeled).
- Absolute pulls (belt off + Ring L off): full 9.4 vs model 12.70 (+35%); standing still (no Speed Phantom) 6.8 vs 8.55 (+26%); Speed Phantom share x1.382 vs x1.485. Ratio tests are within ~5%, so the absolute scale is off by one constant (enemy res/armor, the fitted projectile factor 2.44, or tangles). Open.

### Dummy calibration constant [fitted 2026-10-27]
- Sheet = model on every stat, ratio tests within ~5%, absolute pulls were +35% (full) / +26% (standing still). Engine carries one fitted constant `dummy_scale` = 0.767.
- Vlad: res and armor are right; the gap is Chromatic shots flying off ("bolts into narnia"), i.e. a hit-rate constant. It scales everything equally, so it changes no upgrade price (pen/arp included).
- **2026-10-28: gone.** Today's pulls match the raw model (rms 3.2%), dummy_scale = 1.0. Only yesterday's era tests keep 0.767.

### Sealed mana [tlidb]
- Actual Sealed Mana = Initial Sealed Mana / (1 + Sealed Mana Compensation). Auras seal 50% each, times each support's Mana Cost Multiplier (AA 100%, Restrain 100%, Increased Area 110%, CDR 110%, Seal Conversion 100%; Off The Beaten Track fixes supports at 95%).
- Restrain's compensation is local to its aura; Lone Walker's "+2% aura effect per +3%" reads the global stat (assumed).
- tlidb glossary says each INT gives +0.05% max ES; Vlad's character doesn't have it — don't count it.

### Talent pairing [Vlad 2026-10-27]
- A node paired to the one on its left needs that left node **maxed** (3/3, or 1/1 for a legendary) before it takes any point. A prism cell counts as maxed. `tools/tree.py` and `tools/tree_opt` enforce it; every plan tree before 19:28 on 2026-10-27 broke this rule.

### Block / EHP [2026-10-27]
- Block [tlidb]: attack and spell block chance separate, cap 100%; block ratio 30% base (+25% Defensiveness = 55%), max 60% (80 with raisers). Hits only, not DoT.
  **Dual wielding gives +30% Attack Block Chance** [Vlad 2026-10-30, in game; tlidb implies it: Twinblade Onslaught removes it, Ronin's Tradeoff is -30%].
  Block ratio upper limit 60 -> 80 only via "+10% Block Ratio and Block Ratio Upper Limit" / Invulnerability (other hero panels) and The Brave's +5% Max; none in his panels.
  Kismets: Micro Fate Block Ratio 1-3, Medium 4-6; Attack/Spell Block micro 6-8, medium 12-15. Memory T0 random block line 25-31 (one type per line).
  Ring/belt Advanced prefix "Attack and Spell Block" T1 12-15 / T0 16-20 (both types). Vorax chest Advanced prefix +(12-15)% Attack and Spell Block.
- Low Mana = current mana under 35% of max [glossary]; at 97% sealed it is always on, so the belt's "-X% additional damage taken at Low Mana" is permanent (read, ~90%).
- Defense = Armor + Evasion + ES [glossary]: a "+X% Defense" line is +X% ES for Vlad.
- ES model: gear/memory flat (boots (146 + 304) x 1.6 local = 720; belt base 80 / Arcanist 110) x (1 + tree/slate ES%); pinned to the sheet (7.3k) with +129 flat (legendary bases).
- EHP vs elemental hits = ES / (0.40 res x (1 - block x ratio) x Low Mana). Now ES x 2.5; block cap + Defensiveness + Low Mana = ES x 6.78.
- Spell Ripple prism [Vlad]: 3x3 centred area, +2% sealed mana compensation per medium RANK in the area (his 18% = 3 maxed mediums). Prisms never on god panels.

### Hit cap, prisms, Pedigree [2026-10-27]
- **5T per hit** [Vlad]: engine caps every projectile hit (crit x double/quad x damage roll) at 5e12; the real hit is the model hit / dummy_scale (hit-rate constant; 1.0 now).
  Current build: biggest hit ~1.7T, no effect. Big multipliers past ~x2 start losing to the cap; variance (Impermanence) loses most.
- Ethereal Prism [tlidb]: installs on a non-core node (that node is lost; the slot still satisfies pairing for the next node). Area affixes
  ("All Micro/Medium/Legendary Medium Talent within the area also gain ...") scale per rank. Phantasmagoria: +75% to random affixes (2% -> 3.5% comp).
  Area anchors [Vlad]: 3x4 = 1 column left, 1 right, 1 row above, 2 below; 4x3 = 1 left, 2 right, 1 above, 1 below. A Phantasmagoria rolls ONE comp affix: micro OR medium.
- Defense [tlidb glossary] = Armor + Evasion + Energy Shield.
- Pedigree of Gods variants [tlidb]: <micro/medium> <micro/medium> <medium or Lv.1 core> | <micro/medium> <medium or Lv.1 core> <Lv.2 core>. Lv.1 = 12-pt god cores, Lv.2 = 24-pt cores.
- Impermanence [tlidb]: phys min x0.1 / max x1.8, then all min x0.68 / max x1.32 -> average base x1.43 (modeled via the damage range).

### Aura pulls 2026-10-28 [tested] (no belt / ring L / Spell Amp / Precise Proj, DE slot swapped; Swiftness = MS only = baseline)
- Domain Expansion x1.377 (model 1.404): works on the whole hit, not only Spell Ripple pulses (that would be ~x1.17).
- Precise Weapon Amp x1.547 (model with phys-origin share only 1.438; whole hit 1.505): **WA hits the whole Chromatic hit**, the wand's flat cold included. Engine changed.
- Precise Projectiles ~x1.51 (from 8.0 / 7.3 x DE), model 1.427.
- Blizzard + Freezing Point 246%: **1 debuff, no stacking** [tested 11:31: Blizzard off 5.2 -> 3.0 = x1.733, model x1.707]. Nothing in the text stacks it
  (Blizzard "+10% additional Cold Damage taken for 6s"; FP: CD 2 s, debuff 4 s, debuff scaled by Empower Effect); the 2-stack read was mine and wrong.
- Precise Projectiles: x1.37-1.51 from the rounded pulls, model 1.427 - fine.
- **Absolute scale (12:05)**: the overnight change was the **Chromatic supports** (Vlad's screenshot): Activation Medium: Tangle T1 11% / Overload / Condensed Cold /
  Multiple Projectiles / Target Projection (repo had Spell Tangle / Manifold / Lightchaser / TP / CC). Modeled -> today's six pulls fit dummy_scale **0.851** (rms 3%).
  Yesterday with Spell Tangle fits 0.767 (x1.11 unexplained); with the medium already in slot 1 it fits 0.895 and one constant 0.862 covers all 8 pulls (rms 3.9%).

### Drop replication stacking [Vlad 2026-10-29, in-game observation]
- Every "X% chance to be replicated once" source (compasses, probes, pets' "replicated 1 time" lines, Creation's Fluorescent crystal
  buff) adds into ONE x2 chance, capped at 100%: a drop is never doubled twice. Kong's "replicated 2 times" (13%) rolls AFTER that, per
  copy (x3): 4 = one of two copies tripled, 6 = both; 5 is impossible and 6 is the most ever seen. Expected copies = (1 + min(1, sum)) x 1.26.
- Machines stack: Creation 30 + Colorful (Artifact) 50 + Kong 20 + Sky's Dome 10 = 110% -> capped; the Fluorescent probe's 20% and a
  plain Colorful add nothing there.
- **Skill slots** [Vlad 2026-10-30]: 5 active + 4 passive; auras live in the passive slots, so a freed active slot (e.g. a curse moved to a gear trigger) can only take an active skill (empower, curse, sentry...).
- **Gear curse triggers** [tlidb]: Necklace base affix "Triggers Lv. 20 Biting Cold Curse upon dealing damage to enemies. Cooldown: 0.2 s"; Ring base affix the same for Timid / Entangled Pain; chest ult prefix "You can cast 1 additional Curses" (T1; T0 adds 8-10% Curse Effect). A triggered curse is a fixed level and has no supports (no Deepened Curse). Engine: ctx `biting_cold_level` / `timid_level`.
- **Ice Bond** [tlidb]: Empower + Sentry; Euphoria while the Sentry is within its area around you: "+N% additional Cold Damage against Frostbitten enemies" (24% at L20, +0.25%/level), scaled by Empower Effect (its own WFB / Mass Effect). Engine: in skills.others with its supports. Whether Mass Effect's charges apply to it is unverified.
- **Fervor** [tlidb]: Fervor Rating +1 per hit on an Elite while Fervor is active (10 s base), max 100, +2% Attack and Spell Critical Strike Rating per point (= +200% increased on the rating pool). Sources: Necklace ult prefix "Have Fervor" (T0 +5% / T0+ +12% additional), Vorax Limb: Digits base affix, Ronin slate "Endless Fervor", Dawn Break (belt), Opening Heart (DEX helmet).
- **Spell Ripple** [tlidb]: "(Main) Spell Skills on hit have a 50% chance to spawn a Pulse, dealing True Damage equal to 150% of Hit Damage. Interval: 0.03s" — the Pulse is its own hit (own 5 T cap), so under the cap Ripple keeps its x1.5 (measured 2026-10-25) while per-hit multipliers don't. Engine applies ripple outside the cap factor.
- **Hit cap in practice** [Vlad 2026-10-30]: the 5 T per-hit cap only binds on the dummy. Real maps stack damage-taken penalties on enemies (two x0.5 is normal, Profound Machines ~x0.05), so real hits stay far below it. Price decisions uncapped (`ring_plan.py` default); the engine's cap stays for dummy-pull predictions (`--dummy`).
- **Vorax gear** [tlidb, Digits page]: "You can only equip 1 Vorax Gear". Ultimate affixes are added by special organs (one organ = one named Ultimate affix, with its graft slots); a pool line with no special organ (e.g. the Digits "+(25-30)% additional damage against Frozen enemies") is not craftable.
- **Core Organs** [tlidb]: each legendary's organ page lists its graft slots and suture cost, e.g. Dawn Break "Graft: Boots、Ring、Belt", 5 Tenacious Sutures; Chaotic Ending same slots, 1 Tenacious; Malign Embrace "Graft: Helmet、Necklace", 1 Exquisite Suture. "Legendary affixes on Vorax gear will not take effect when that corresponding Legendary gear is equipped." Special organs name their Ultimate affix and slots (Flawless Spine: Impalement = ARP, Flawless Ears: Echoing = CDR; Boots/Ring/Belt).
- **Elite** [tlidb glossary]: rare monsters and bosses (Fervor Rating, "hit an Elite" conditions).
- **God's Boon uptime** (assumption, 2026-10-30): with margin m = 0.5 (1+duration)(1+CDR) < 1 the 2nd stack is up clamp(2m - 1) of the time (recast on cooldown); `ring_plan.py` time-weights 2 vs 1 stacks. The engine itself still takes ctx boons.

