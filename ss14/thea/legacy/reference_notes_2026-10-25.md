# TLI SS14 Thea (Wisdom of The Gods) — reference pulled from tlidb, 2026-10-25

## Build skeleton (inferred from files; confirm with Vlad)
- Hero: Thea 1 / Wisdom of The Gods. Main skill: Chromatic Shot (lv36 in sheet) + Lightchaser (Magnificent, slot 3). Cast as Spell Tangle (Malign Embrace helmet, 2 active / 4 max tangles).
- Phys→cold conversion (Prophet legendary medium "Converts 100% Physical to Cold" or Mind Blade?), Extreme Coldness core from Iced Drinker's Cage, Frozen Lotus core (Prophet, +25% additional cold, skills cost no mana).
- Auras in file: Precise Projectiles, Domain Expansion, Ice Focus (?), Weapon Amplification (phys→cold'd). Aura Amplification lv29 on each (12.25%). Restrain + Off The Beaten Track for reservation.
- Prism: Haze (+12% additional spell dmg with Spell Aggression), Lich col15 top row.
- Trees: Goddess of Knowledge 29, Magister 24, Prophet 30, Lich 27 = 110 pts.

## Hero trait (tlidb /Wisdom_of_The_Gods)
- Base L5: +52% additional dmg for 10s if God's Boon consumes max Focus stacks; auto-casts at max; CD 15s. Artificial Moon: +10% area per Focus consumed (max 5).
- Prophecy of Truth L5: +3% additional dmg per Legendary Medium Talent, up to 20 (=+60%).
- Prophecy of Revelation L5: +24% additional dmg while having all 3 blessings; swaps panel-4 talents for blessing talents (GoM/GoK/GoH panels only).
- Predicted Justice: biggest max-stack bonus of Agility/Tenacity also applies to Focus max; -5% CDR at L5.
- Prophecy of Punishment L5: Lucky dmg + 5% additional MAX dmg per Agility stack when Agility stacks == Focus stacks.
- Predicted Reincarnation L5: +50% additional Boon CDR; +11% additional dmg per Focus consumed (max 5 = +55%).
- Farewell Prophecy L5: +8% double dmg chance per Focus consumed (max 8); overflow → quad dmg.
- Prophecy of Purity L5: Boon buffs stack +1 more; +25% skill effect duration.
- Relevant Revelation (Magister/Prophet/Elementalist) blessing talents: +1 max Focus at 500 INT; Frail on spell dmg +8% Frail effect per max Focus (max 18); +4 max Frostbite rating per max Focus; +5 crit rating vs Frostbitten per max Focus; Cold Infiltration vs Frostbitten; +1 cold skill lvl / 0.6% additional fire+lightning per max Focus if dealt cold recently; +3% atk/cast per max Focus at full mana.

## Chromatic Shot (tlidb)
- Spell, Projectile, Area, Physical, Horizontal. Main stat STR/DEX/INT. 8 mana, 1.54 cast/s, 123% added-dmg effectiveness at 20. 498–831 phys at lv20 (flat from 20→40; levels past 20 only matter via support/quality? — verify).
- 3 shots, can shotgun same enemy, shotgun falloff 80%. 10% explode on kill (25% max life true dmg, 5m).
- Lightchaser (Magnificent, slot 3): +20% additional dmg; **+25% additional damage ratio granted by main attribute**; +30% additional proj speed; better tracking. Roll: (−12…−9)% T0, (−14…−13)% T1, (−17…−16)% T2 additional dmg.
- Condensed Cold (Noble) exists — not fetched yet.

## Aura rules (tlidb /Aura)
- Positive value = base × (1 + Σ increased aura effect) × Π(1 + additional). Same-name: only one applies; Precise wins; then level > value.
- Aura Amplification support: +5.25% at L1 … +10% at L20, +12.25% at L29, +15% at L40. +100% skill area.
- Precise: Spell Amplification: +40% additional spell dmg at L20 (L25 43%, L30 45.5%). 50% sealed mana.
- Restrain +10% compensation; Precise Restrain +25%. Precise: Selfishness +24% effect, −12% comp. Precise: Stand as One +6% per aura on you (max 5 = +30%). Precise: Disciplined +35% comp, −19% additional effect. Precise: Malleable +30% near elite else −15% additional, −15% comp.
- Off The Beaten Track (Lich core, 24pts): +4 support skill level; support mana multiplier fixed 95%.

## Gear
- Lone Walker's Boots (DEX, Boots of Calamity base, lv58): random Lv20 Precise bonus-damage aura (Spell Amp / Cruelty / Deep Pain / Radical Order); +50% MS; +(15–30)% aura effect when affected by (4–5)+ auras; +2% aura effect per +3% sealed mana compensation. Corroded: Lv(25–30) aura; +(55–65)% MS; +(38–45)% aura effect at (3–4)+ auras; +1% aura effect per +1% comp.
- DEX boots suffix/prefix pool has NO aura-effect affix (base affix only on chests: +(7–8)% aura effect; chest ultimate suffix +(15–20)% aura effect; DEX chest base +(6–8)% comp).
- Iced Drinker's Cage (INT chest): +170 gear ES base; +(300–350) gear ES; (−1…+1) main skill lvl; Extreme Coldness (+50 max frostbite, cold only); 1 Cage stack on frostbite (1s); control effects received +(1–50)%. Corroded: +(400–450) ES, +(1–2) main skill lvl, +20 max frostbite, 2 Cage stacks, immune to frostbite.
  - Cage buff CONFIRMED by Vlad: 4 stacks × +14% additional dmg (×1.14^4), −7% DoT taken per stack (0.93^4).
- Chromatic Shot attribute scaling CONFIRMED by Vlad: +0.5% additional dmg per point of (STR+DEX+INT); Lightchaser raises it to 0.75% per point. Script's 835 = total attributes at the time.
- DPS model from calculate_lone_walkers script: all "additional" sources multiply; aura value = base × (1 + local AA + global aura effect); Precise granted aura has no supports; crit factor = (1−p + p·cd·malign) with p=chance, cd=crit dmg multiplier; ES = base + Δgear ES × 1.72 global.
- Malign Embrace (INT helmet): +(250–350) ES, +2 max tangles, +(150–180) spell crit rating and +(18–23)% additional dmg on crit per activated tangle, nearby enemies guaranteed crit. Corroded: +(400–450) ES, +(12–20)% additional spell dmg, +(195–225)/+(26–30)% per tangle. Sheet shows 21% per tangle, 2 active → ×1.42 (matches script).

## Prophet panel (tlidb)
- Cores (24): Frostbitten (frostbite on cold hit, +40% effect); Extreme Coldness; Mind Blade (30% phys as cold w/o wand/staff; +25% additional cold with wand/staff); Frozen Lotus (+25% additional cold, no mana cost).
- Notable: legendary medium 18pts +10% additional vs Frozen; +20% frostbite effect; Focus stack on hitting frostbitten (0.1s); phys→cold 100% convert (18pts); medium 15pts +5 max frostbite / +8% frostbite effect / +5% INT; micro 15 +10% dmg while Focus active.
- Frostbite: +1% additional cold taken per frostbite rating; frozen above 100. Sheet: max frostbite 101, effect 56%.

## Lich panel (tlidb)
- Cores (24): Indifference (+1% additional per 5 remaining energy, max 50%); Ward (13% sealed mana/life as ES); Off The Beaten Track; Stab In The Back (blur).
- Legendary 18: +1 all skill levels; +8% CDR +1 charge; +10% additional dmg with both sealed mana and life; +8% comp. Medium 15: +3% comp. Micro 12: 1.5% comp.

## TALENT TREE (screenshots 2026-10-25; grid = 7 cols at 0/3/6/9/12/15/18 pts × 5 rows; coords as x_y like the old JSON: x=96,224,352,480,608,736,864; y=80,176,272,368,464)
Assumption: tlidb node values are PER RANK (3/3 = 3× the listed value). Verify against sheet totals.

### Goddess of Knowledge — 26 pts (cores: 12-slot + 24-slot, icons unconfirmed)
- 96_272 micro +9% dmg ×3 = +27% dmg
- 224_272 medium +18% dmg ×3 = +54% dmg
- 224_176 micro +3% cast speed +2% MS ×3 = +9% cast, +6% MS
- 352_176 medium +6% cast speed −4 cost +4% MS ×3 = +18% cast, +12% MS
- 736_176 micro +9% spell dmg ×3 = +27% spell dmg
- 864_176 legendary +1 Spell Skill Level
- 736_368 micro +10% Focus duration / +10% dmg while Focus active ×3 = +30% / +30%
- 864_368 legendary +1 Max Focus Blessing
- 352_464 micro +15% spell crit rating ×3 = +45%
- 480_464 medium +20% spell crit rating +5% spell crit dmg ×3 = +60% / +15%
(Dropped vs old JSON: 352_272 area/proj speed.)

### Magister — 24 pts (core 24-slot, purple vortex, unconfirmed: Bunch?)
- 352_80 micro +15% spell crit ×3 = +45%
- 480_80 medium +20% spell crit +5% crit dmg ×3 = +60% / +15%
- 480_176 micro +10% Focus duration / +10% spell dmg w/ Focus ×3 = +30% / +30%
- 608_176 legendary: Focus stack on Spell Burst consume / on Tangle cast
- 736_176 micro +10% Focus duration / +4% cast speed w/ Focus ×3 = +30% / +12%
- 864_176 legendary +5% spell crit dmg per Focus stack
- 608_272 micro +8 INT ×3 = +24 INT
- 736_272 legendary +12% INT
- 96_464 micro +3% max ES ×3 = +9% ES
- 224_464 medium +6% max ES ×3 = +18% ES

### Prophet — 27 pts (core 24-slot: galaxy/snowflake icon; Prism Spell Ripple installed at 608_176, 3×3 area = cols 9–15, rows 1–3)
- 352_80 micro +15% crit rating ×3 = +45%
- 480_80 medium +20% crit +5% crit dmg ×3 = +60% / +15% (in prism area; medium → +2% comp)
- 608_80 micro +2 max frostbite ×3 = +6 (prism area)
- 736_80 medium +5 max frostbite ×3 = +15 (prism area; +2% comp)
- 864_80 legendary +10% additional dmg vs Frozen
- 608_176 = PRISM (replaces 12pts micro +4% frostbite effect)
- 736_176 medium +8% frostbite effect ×3 = +24% (prism area; +2% comp)
- 864_176 legendary +20% frostbite effect
- 96_272 micro ×3 and 224_272 medium ×3: EITHER +9%/+18% cold dmg (→ +27%+54% = +81% cold) OR +3%/+6% life&ES — ICON AMBIGUOUS, ask
- 352_272 micro +4% cold res ×3 = +12%; 480_272 legendary +18% cold res (prism area; counts as 1 legendary medium in area)
- Prism affixes: all mediums in area +2% sealed mana comp; "2 legendary mediums in area → 100 fixed Blur rating" — only ONE legendary (480_272) allocated in area → likely NOT active.
- Spell Ripple core: Main spell hits 50% chance to spawn Pulse = 150% hit dmg as True dmg, interval 0.03s. If it REPLACES the Prophet core, Frozen Lotus is gone (old script assumed Frozen Lotus ×1.25 and no mana cost) — CONFIRM.

### Lich — 33 pts (core 24-slot: orange fire icon, unconfirmed: Off The Beaten Track?)
- 352_80 micro +15% crit ×3 = +45%
- 480_80 medium +20% crit +5% crit dmg ×3 = +60% / +15%
- 608_80 micro +9% dmg ×3 = +27% dmg
- 736_80 medium +6% atk/cast ×3 = +18% cast
- 864_80 legendary +1 to All Skills' Levels
- 480_176 micro +5 all stats ×3 = +15; 608_176 medium +10 all stats ×3 = +30 → +45 all stats
- 736_176 micro 1.5% CDR ×3 = +4.5%; 864_176 legendary +8% CDR +1 max charges
- 96_272 micro +3% life/ES ×3 = +9%; 224_272 medium +6% life/ES ×1
- 224_368 micro +3% atk/cast ×2 = +6%
- 736_368 micro +3% life/ES ×3 = +9%; 864_368 legendary +10% additional dmg when having both Sealed Mana and Sealed Life
- No compensation nodes taken (Bow01 row all 0).
Old JSON's Haze prism in Lich is gone; Spell Ripple now in Prophet.

### CORES CONFIRMED (Vlad): GoK = Peculiar Vibe (12pt, +1 Tangle, −30% additional Tangle duration) + Acquaintance (24pt, Dormant Entanglement, +25% additional spell dmg). Magister = Bunch (+1 max Focus, +3% additional spell dmg per Focus stack). Prophet core = Spell Ripple (prism REPLACES Frozen Lotus: main-spell hits 50% → Pulse = 150% hit dmg as True, 0.03s interval). Lich = Off The Beaten Track.
- Max tangles: 1 base + 1 Peculiar Vibe + 2 Malign = 4. Active 2.
- Mana: irrelevant. Tangles are TRIGGERED casts (no mana) and skill cost is heavily reduced. Drop the old script's Frozen Lotus ×1.25 cold and "no mana cost".
- Prophet row-3 left pair = life & ES: +9% and +18% (not cold dmg).
- Per-rank values ×rank CONFIRMED. Deliverable: I build the stat page, Vlad compares to in-game.

### Tree totals: damage +108%; spell dmg +27% (+30% w/ Focus); dmg w/ Focus +30%; spell crit rating +315% (+89% Witch page); crit dmg +60% (+5%/Focus, Magister leg.); cast speed +63% (+12% w/ Focus); INT +24 +45(all stats) +12%; STR/DEX +45; skill levels +1 spell +1 all; max ES +9+18+9+6+9 = +51%; max frostbite +21, frostbite effect +44%; cold res +30%; CDR +12.5% +1 charge; +10% additional dmg (sealed mana & life); +10% additional vs Frozen; MS +18%.

## SLATES (screenshots 2026-10-25)
- Pedigree of Gods (lv100, Max Active Divinity Slate 1): +10% Agility duration & +3% atk/cast w/ Agility; +8 STR; crits eliminate enemies <8% life; CORE = Dirty Tricks (+12% additional Hit dmg, multiplies, per Ailment type on the enemy). Replaced Insight.
- Nether King's Divinity: Judgment (lv89): fixed +11% double dmg chance. Brands: Source 25% Attack Aggression on defeat (not active, shield icon); Offspring: Inflicts Frail on spell dmg (ACTIVE, +15% spell dmg taken); Offspring +12% INT (ACTIVE).
- GoK Divinity #1 (lv89): fixed +5% spell crit dmg per Focus stack (MAD1 — duplicates Magister tree node, only one counts), +1 max Focus (MAD1). Brands: +20% crit rating +5% crit dmg; +1 Spell Skill Level; Converts 100% Physical → Cold (MAD1) ← THE conversion source.
- GoK Divinity #2 (lv86): fixed +1 Spell Skill Level; consumes 4% current mana on main skill cast (0.03s), +8% additional spell dmg (MAD1). Brands: +20% crit +5% crit dmg; channeled (dead); +1 max Focus (MAD1 — duplicate of #1, only one +1 counts) + 0.4% mana regen w/ Focus.
- Goddess of Hunting Divinity (lv87): fixed +2 horizontal projectile penetration; +10% additional dmg 4s after mobility skill. Brands: +12% proj speed ×2; +15% projectile crit dmg.
- Fallen Starlight (lv86, all effects +40%): +12.6% fire DoT/minion fire, adds 14–14 base Ignite dmg; +5.6% skill effect duration; +11.2% CDR +1 max charges (MAD1 — same node as Lich 864_176 +8%; only one active, slate's 11.2% presumably).
  - Purpose: God's Boon uptime. Boon buff 10s × (1 + 40% neck + 10% memory + 5% Purity + 5.6% slate) ≈ 16s; CD 15s / (1.5 Reincarnation × (1 + CDR)) ≈ 8s → with Prophecy of Purity (+1 stack) two Boons overlap permanently: Reincarnation ×1.40², Farewell 2×48% double dmg.
- Board: 5 slates placed + pedigree; 3 Nether King skull cells (top-left, top-right, bottom-right). Left blue 4-tile slate not identified in screenshots — ASK.
- Condensed Cold (Noble, slot 5, 110% mana): +20% additional dmg; converts 100% phys→cold; frostbite on cold hit; gains Cold tag; +(23–25)% additional hit dmg at T1 (T0 27–31, T2 19–21).
- CORRECTION: Tangle cast rate = cast speed, NOT 0.4s (that was the Activation Medium text). Focus regen (Magister 608_176) = tangles × casts/s.

## SLATE CORRECTIONS (Vlad)
- Only equipped slates were sent. GoK #1 has +1 max Focus; GoK #2's line is +1 max Focus REGEN-mana variant — i.e. #1 = +1 Max Focus (MAD1), #2 = mana regen line (no second +1 Max). Only one +1 max Focus total from slates.
- Judgment (Nether King) BOOSTS BY +40% every slate placed between its skull cells: Fallen Starlight, the GoK "consume knowledge" slate (#2, 4% mana consume / +8% additional spell), and the Hunting slate. That's why Fallen Starlight shows "Effect: +40%" (8→11.2 CDR, 4→5.6 duration). So GoK #2 and Hunting values are ×1.4 too (+8% additional spell → 11.2%? +1 spell level stays; +20% crit → 28%; Hunting +12% proj speed → 16.8%, +15% proj crit dmg → 21%; +10% additional after mobility → 14%; +2 pen stays?). CONFIRM which lines scale.
- Dirty Tricks confirmed as the better pedigree core (Insight was the previous one).

## SKILLS (screenshots 2026-10-25)
- Chromatic Shot [1 Spell Tangle, 2 Manifold Entanglement, 3 Lightchaser (Magnificent) T1, 4 Multiple Projectiles, 5 Condensed Cold (Noble) T1].
- Aim (Spell, Persistent, Empower) [Preparation, Well-Fought Battle, Mass Effect, locked].
- Secret Origin Unleash (Spell, Persistent, Empower) [Preparation, Mass Effect, Well-Fought Battle, Resurgence, locked].
- Biting Cold (Spell, Area, Persistent, Cold, Curse) [Activation Medium: Elite (slot 1, triggers when Elite within 6–20m, 0.2s), Terrain of Malice, Deepened Curse, Increased Area, locked].
- Precise Projectiles aura [Restrain, Increased Area, Aura Amplification, locked] — lv20: +35% additional projectile dmg, +35% additional projectile ailment dmg, +10% proj speed.
- Spell Amplification aura [Aura Amplification, Increased Area, Restrain, locked] — lv20: +35% additional spell dmg.
- Frigid Domain aura [Restrain, Cooldown Reduction, Aura Amplification, locked] — lv20: +35% additional cold dmg.
- Domain Expansion aura [Aura Amplification, Seal Conversion, locked] — lv20: +33% additional area dmg (+ailment), +20% area at 8+ enemies. Seal Conversion → sealed LIFE → enables Lich legendary "+10% additional dmg with both Sealed Mana and Sealed Life".
- Displayed: Sealed Life 6.73%, Sealed Mana 2.94% → reservation is a non-issue.
- No mobility / defensive skill shown. Locked slots = energy.

### Skill level derivation
Sources: +4 all (neck), +1 all (Lich), +1 spell (GoK tree), +1 spell (GoK slate #1 brand), +1 spell (GoK slate #2 fixed), +2 cold +2 phys (wand M), +2 spell +2 phys (wand S), +4 support (OTBT), 0 main (chest).
- Chromatic Shot (Spell/Proj/Area/Phys + Cold via Condensed): 20 + 5 all + 5 spell + 4 phys + 2 cold = 36 ✔ (matches sheet).
- Untagged supports (MP, AA, Restrain, Increased Area, CDR, Seal Conversion, Preparation, Mass Effect, WFB, Resurgence, Deepened Curse, Terrain of Malice, Act. Medium): 20+5+4 = 29 (AA 29 ✔ matches sheet).
- Spell Tangle, Manifold (Support, Spell): 34. Magnificent/Noble are tiered (T1), not leveled.
- Auras: Precise Projectiles 25; Spell Amplification 30; Frigid Domain 27; Domain Expansion 25.
- Aim / Secret Origin Unleash (Spell): 30. Biting Cold (Spell, Cold): 32.

## SKILLS — ROUND 2
- Speed Phantom (mobility) [Quick Mobility, Weakness Infiltration (+22% additional for SP, +30% Infiltration effect taken by enemies for 4s on dmg), Exhaustion (+60% Weaken chance, +17% additional), locked]. Level 29? (no Spell tag → 20+5 = 25; mobility).
- Aim (lv30): Euphoria 6s, +38.25% additional dmg & ailment dmg for Projectile/Beam skills, −16% atk/cast speed. CD 10s, 15 mana.
- Secret Origin Unleash (lv30): Euphoria 6s, +18.2% additional spell dmg, +3% cast speed per Focus stack (max 8 = +24%). CD 10s.
  - Both: Preparation (auto every 8s), Mass Effect (+1 charge, +20% effect per charge up to +60%), Well-Fought Battle (+10% effect per cast, 3 stacks = +30%). Duration 6s × (1+ ~60% skill effect duration) ≈ 9.6s > 8s → permanent. Effect multipliers: (1+0.6+0.3) = ×1.9 on the buff value → Aim ≈ +72.7% additional proj dmg; SOU ≈ +34.6% additional spell + cast speed.
- Tangle rules (tlidb): attach range 8m; prefers highest rarity; active only when attached; triggers at the linked spell's cast interval; base duration 8s; base max 2, cap 4; new tangle replaces oldest at cap. Peculiar Vibe = +1 Tangle PER ENEMY (base 1 → 2) → on a single boss only 2 of 4 can attach = "2 active". Dormant Entanglement (Acquaintance): presumably unattached tangles persist dormant instead of expiring — confirm.
- OTBT insight: support mana multiplier fixed at 95% → every support on an aura multiplies its reservation by 0.95. Increased Area / CDR on auras are RESERVATION FILLERS (3 supports → ×0.857). Seal Conversion on Domain Expansion = move one aura to Life so 4 auras fit.
- Blessed Leap discarded: Agility stacks stay low (1 per 6s cycle, blessings expire).
- Empowered Insight discarded (26% is weak).
- Fetch rule: tlidb pages are reachable only when Vlad pastes the URL (or a search surfaced it).

## MECHANICS (tlidb, fetched 2026-10-25) — search with allowed_domains=tlidb.com, then fetch the result URL
- Focus Blessing: 5% ADDITIONAL dmg per stack (base). Base max 4, duration 10s, gaining any stack refreshes all; all lost if duration ends. God's Boon consumes all. Vlad max Focus = 4 + 1 GoK tree + 1 Bunch + 1 slate = 7.
- Agility Blessing: +4% atk/cast & +2% additional dmg per stack. Base max 4, 10s, refresh-on-gain → trait's 1-per-6s keeps it at 4 permanently: +16% cast, +8% additional.
- Tenacity: per stack 4% damage reduction (from earlier fetch); max 4 assumed.
- Dormant Entanglement: +40% ADDITIONAL Tangle Damage per INACTIVE tangle. 4 owned, 2 attached (per-enemy cap 1 + Peculiar Vibe) → 2 dormant → ×1.80. Peculiar Vibe's 2nd active tangle doubles cast rate, worth it over 3 dormant.
- Tangle: attach 8m, prefers highest rarity, base duration 8s (Peculiar −30% additional), triggers at the linked spell's cast interval, base max 2 / cap 4, oldest replaced.
- Tangle Damage Enhancement: wand suffix +34% (ultimate suffix range 40–50 → his is a lower tier). Treated as a separate multiplier on tangle-cast skills ("Tangle Damage"). GoK micro +9% tangle dmg not taken.
- Night Feather Entanglement: 1 stack per active tangle, max 2 (vhpg), +50% NFE effect; per-stack base effect not on tlidb — ASK. +8% additional spell while present; Focus every 1s at max.
- Ailments (tlidb): Ignite, Frostbite, Freeze, Shock, Numbed, Trauma, Wilt (Freeze is a separate ailment at >100 rating). Dirty Tricks on a Frozen boss = Frostbite + Freeze = 1.12² = 1.2544. Frail/Weaken/Slow/Curse are NOT ailments. Extra types come from FOLLOWER Tartarus skills: Wilt Spike (Wilt), Double Thrusts (Trauma), Lightning Storm (Numbed) → up to 5 types = 1.12^5 = 1.76.
- Frostbite rating: starts 10, cap 120; +1% additional cold taken per rating; Frozen above 100; "Frostbite Effect" scales the per-rating bonus (assumed). Vlad max rating 101 (10+50+20+21).
- Biting Cold lv32: cursed enemies take +45.5% cold dmg; duration 5s base; CD 8s (Terrain). With ~+60% skill effect duration → 8s → Preparation = 100% uptime everywhere; Activation Medium: Elite = elites only.
- Base spell crit rating = 500 (5%). Crit chance = 500 × (1 + Σincreased) + flat; cap? (ask).
- Monsters: bosses 30% all res, max armor (Armor page, per Vlad). Armor vs spell: check Armor page.
- Aim −16% cast speed is NOT affected by Empower effect bonuses (flat −16%).
- Tartarus Riot compasses: Mercury −45% additional dmg taken, Redgold −70%.

## FOLLOWER (Vlad): Tidewell III [Additional Ignite, Glacial Freeze] → Ignite + Frostbite; Lightning Storm III [Improved Corrosion, Coercion] → Numbed + Wilt; Swift Shadow Raid III [Periodic Burst, Deep Wounds] → Trauma. Dirty Tricks types on boss: Frostbite, Freeze, Ignite, Numbed, Wilt, Trauma = 6 → 1.12^6 = 1.97.
- Max Focus = 8 (4 base + GoK tree + Bunch + slate#1 + slate#2; the two slate nodes are different nodes, both count).
- Crit: Final rating = (500 base + flat) × (1 + Σincreased) × Π(1+additional); chance = rating/100; base crit dmg 150%.
- Attributes: STR +0.2 life/pt, DEX +0.02% evasion/pt, INT +0.05% max ES & +0.5 mana/pt. Heroes start 0 res, −20% all res at lv48/58/80 (−60 total), max res 75.
- Cold Infiltration = −10% cold res (res reduction, not pen). Boss 30% res − 24.8% pen = 5.2% left → Infiltration overshoots; not worth a slate.
- Aura values: Spell Amp lv30 40.5, Frigid Domain lv27 39, Precise Projectiles lv25 38 (+10% proj speed), Domain Expansion lv25 36 — all ×1.1225 (AA lv29). All 50% sealed. Progression +0.6/level 20→25, +0.5/level after.
- Boots gear ES = (146 base + 304) × 1.6 = 720 ✔ (script). Malign base 120, Cage base 170, Israfel base UNKNOWN (120–146).
- Energy: 500.
- Stat page v1 computed in scratchpad/thea_stats.py (2026-10-25).

## FOLLOWER DETAIL (tlidb Tartarus pages) — Tartarus supports are their OWN versions, not the player ones
- Tidewell III: Water Area 6s, allied SPELLS inside +20% double damage chance; torrents 0.7s. Supports: Additional Ignite (base ignite + 100% ignite chance → Ignite type), Glacial Freeze (Tartarus) = inflicts COLD INFILTRATION on enemies with ≥1 frostbite rating → +13% additional cold taken (and −5% MS).
- Lightning Storm III: Numbed on hit. Supports: Improved Corrosion (base wilt + 100% wilt chance → Wilt), Coercion (Paralysis within 10m on cast — CC, not an ailment).
- Swift Shadow Raid III: on cast, you and allies +40% PROJECTILE SPEED for 4s. Supports: Periodic Burst (Tartarus) = +20% attack & cast speed for unit AND allies for 4s; Deep Wounds (Trauma).
- Dirty Tricks types: Frostbite, Freeze, Ignite, Numbed, Wilt, Trauma = 6 → ×1.97.
- Witch pact page: 6 destiny slots carry a base +3% damage each = +18% damage (free).
- NFE (Vlad): +7% additional Tangle Damage and +3% CDR per stack, before the Witch's +50% effect → 10.5% / 4.5% per stack, 2 stacks.
- Additional modifiers are always compounded (TLI rule).

## CORRECTIONS 2026-10-25 16:45
- GoK 352_464 / 480_464 are NOT crit: they are Area micro (+6% area, +6% proj speed ×3) and Area medium (+12%/+12% ×3) → +18% skill area, +54% proj speed. Tree crit = Magister 105 + Prophet 105 + Lich 105 = 315.
- Israfel's Laws base = All Magic Grip, 120 ES → ES 6,247.
- tlidb URL rule: drop apostrophes (Israfels_Laws), search with allowed_domains=tlidb.com.

## STATUS 2026-10-26 12:48 — belt off 8.7 T → ~24 T (belt factor ×2.75: Gale 2.48 × 47% dmg 1.065 × 31 INT 1.04). Dummy caps 10 T and 5 T per hit; always measure belt-off.
- Wisdom of the Gods now Trait Level 4 = +44% additional per Boon stack (Base Trait slot: Epic-or-lower Progress Memory installed, lines shown post-58% cut: +15% cast, +18 spell crit dmg, +18 cold crit dmg, +2 trait level). CONFIRMED Wisdom doubles with 2 Boon stacks: Boon = 1.88 × 1.80 = ×3.38. Purity rank 3 = +1 Boon stack (cap 2; 3 impossible). Duration 16.1 s vs CD ~7.7 s — protect the 2-stack margin (~4%).
- Double: on-person 88 (wands 37+40, Judgment 11) + water 20 + Farewell 96 = 204 (184 out) → quad every hit.
- Boots: Hasten (advanced affix: +8% additional cast, +8% cast, +8% additional MS) replaced a res line; res rebuilt with lightning kismets. INT now 504 (STR 152, DEX 45; attr 701 → ×6.26). Damage bonus 485 + cold 142 = 627% pool; cast 230% (+Hasten); crit 76.3% (rating bonus 842); crit dmg 458 (+36 from trait memory).
- Costs: basic roll 3.2 FE @1% T1 (320/hit); advanced 6.7 FE @3.33% (201/hit); ultimate 58 FE @5% (1,160/hit). Current FE-per-1% ladder: ring L INT→arp (adv, ~90), ring res→T1 crit dmg (adv, ~200 + kismets, net ×1.05 now), Focus/frostbite ults (150–170), tangle T1 (145), Pantheon's Elegy (+120% cast via Precise Swiftness, 15.5k: 320–420/1%, buy later; needs a real 3rd dirge e.g. God of Machines +2–4 main skill).
- Nether King Judgment "+10%/non-legendary" mod does NOT work as hoped (4.5k test, to resell). Prism Spell Ripple sits on Prophet +4% frostbite effect micro (−12% effect = ÷1.05); moving it to the empty INT micro and buying the effect micro back (3 pts) is the best Prophet rate left.

## STAT PAGE v3 (superseded by STATUS above)
- Damage bonus +667% | Cold +142% | Phys 0
- Additional cold ×3.63 | Cast speed +208% → **+230% (2026-10-25 19:15: wand S cast affix rerolled 25 → 47, T0 max)** (×1.07 additional) | Proj speed +246.8% (×1.30 additional)
- Supports now: Spell Tangle, Manifold, Lightchaser, Target Projection (replaced Multiple Projectiles; TP = ×1.277 = Enhanced Mark 16.6% proj taken × Mark 10% crit dmg taken), Condensed Cold. Baseline 9.9 T (belt off 3.5–3.6 T; belt factor ×2.725; dummy caps at 10 T → always test belt-off). After cast 47: predicted 10.6 T (belt off 3.9 T).
- 2026-10-25 19:22: wand S +75% spell dmg prefix rerolled → Adds Physical Damage to Spells, upgraded to T0 (87–89 to 106–108; ×1.23 effectiveness, converted to cold by Condensed Cold). Net ×1.083 → baseline 11.5 T (belt off 4.2 T). Vlad prefers phys over cold flat (future Weapon Amp / phys% options).
- Costs (Vlad): ember 0.22 FE each; mod roll = 10 embers + 1 FE; tier upgrade = 300 embers + 30 FE + sacred fossil (12 FE), 30% odds; tangle ult roll = 30 FE + ult ember 28 FE, T1 tangle ~5%. Vlad will NOT put arp on wands.
- Wand plan agreed: ult = 1 double + 1 spell lvl + 2 tangle (arp vs 2nd tangle undecided, hinges on armor read); keep spell dmg % (not flat); 1 cast + 1 ele basic; adv = skill levels + spell crit dmg.
- Spell crit rating 7,630 → 76.3% | Crit dmg 433% | Cold pen 24.8 | Armor pen 10
- Skill effect duration 60.6 | CDR 24.7 | ES 6,247 | Res 61/59/56/43 | Attr ×6.93

## STAT PAGE v2 (superseded) (dummy; 8 Focus, 4 Agility, 2 tangles, 2 NFE, Euphoria×2, Aggression, 2 Boons, follower buffs up)
- Damage bonus (dmg+spell+proj): 330+18+279+40 = +667%
- Cold damage: +142% | Phys: 0
- Additional cold: ×2.12 (Israfel) × 1.438 (Frigid) × 1.19 (Dreamweaver) = ×3.63 (+263%)
- Cast speed (increased): 181.6 + 20 (Periodic Burst) = +201.6%; additional ×1.07 aggression
- Proj speed (increased): 152.8 + 40 (SSR) = +192.8%; additional ×1.30 Lightchaser
- Spell crit rating: 810 × (1+9.47) = 8481 → 84.8% (tree 420 disputed by Vlad)
- Crit dmg: 433%
- Cold pen 24.8 | Armor pen 10 | Skill effect duration 60.6 | CDR 15.7 + 9 (NFE) = 24.7
- ES ~6,250–6,300 | Res 61/59/56/43 (no level penalty)
- Attribute ×6.93 (791 attr)

## GEAR DUMP (screenshots 2026-10-25, all equipped)
- Helmet: Malign Embrace, lv89, corroded. +347 gear ES; +2 max Tangle; +155 spell crit rating & +21% additional dmg on crit per activated Tangle; nearby enemies guaranteed crit (on you). Energy 58.
- Chest: Iced Drinker's Cage, lv93, corroded. +338 gear ES (+170 base ES on top per tlidb); 0 main skill level roll; Extreme Coldness; 1 Cage stack per frostbite (1s); control effects received +33%. Energy 122.
- Neck: I Am Truth, lv88, corroded. +5 INT (base); +4 to all skills' levels; +99 STR; +40% skill effect duration.
- Gloves: Israfel's Laws, lv90, corroded. +349 gear ES; +25% blessing duration; +14% additional cold dmg per Focus Blessing stack; +1% crit dmg per Focus stack. Energy 61.
- Belt: Magic Girdle (rare), lv83, BASE AFFIX = GALE (Marksman core: 60% of projectile speed bonus also applied as ADDITIONAL projectile damage → 0.6 × 246.8% = ×2.48). MISSED ON FIRST PASS. +31 INT; +220 max ES; +47% dmg / +19% lightning res; +17% cold res; +16% erosion res.
- Boots: Long Night Sorcerer's Boots (rare INT), lv89. +58% crit dmg mitigation; +60% gear ES; +304 gear ES / +19% lightning res; +22% fire res; +40% movement speed. Energy 61.
- Ring L: Perishing Inferno Flame Ring (rare), lv86, base +12% fire res. +52 INT; +221 max ES; +64% dmg / +18% lightning res; +27% erosion res; +120% crit rating.
- Ring R: Eternal Sleep Ice Ring – Priceless, lv100, base +12% cold res + gains Spell Aggression when casting a spell skill. +210 max ES; +81% dmg (T0); +10% armor DMG mitigation penetration / +20 max frostbite rating; +27% fire res; 100% chance to gain Barrier per 5m moved.
- Wand M (main): Headless Cleric Wand – Priceless, lv100, base +40% spell dmg, +8% additional spell dmg. Energy 40. (screenshot 2026-10-25 19:24)
  - Prefix: T1 +2 Cold Skill Level | T1 +2 Physical Skill Level | T0 Adds 87–106 Physical Damage to Spells (was +67% spell dmg; rolled T1 then upgraded 1st try)
  - Suffix: T1 +37% double dmg | T2 +34% Tangle Damage Enhancement (T1 = 40–50) | T1 +106% Elemental Damage
- Wand S (off): Headless Cleric Wand – Priceless, lv100, base +40% spell dmg, +16% cast speed. Energy 59. (screenshot 2026-10-25 19:24)
  - Prefix: T2 +2 Spell Skill Level (T1 = +3) | T1 +2 Physical Skill Level | T0 Adds 84–112 Cold Damage to Spells (was +75% spell dmg; rolled T1 then upgraded 3rd try)
  - Suffix: T1 +166% Critical Strike Rating | T0 +47% Cast Speed (was +25%) | T1 +40% double dmg
- Flat added total: (96.5 + 98) × 1.23 effectiveness = 239 → Chromatic Shot base 665 → 904 (×1.36). Spell dmg lost 142 → increased pool 809 → 667 (÷1.185). Net wand session: ×1.071 (cast) × 1.148 (flat) = ×1.23 → baseline 9.9 → ~12.2 T (belt off ~4.5 T). Remaining wand upgrades: tangle 34→T1 (+8%), spell lvl +2→+3 (+8%), crit rating → spell crit dmg (+3%, +8% after GoK crit pair).
  - Dual-wielding wands → Mind Blade (if taken) gives +25% additional cold; Chromatic Shot gets +2 cold +2 phys +2 spell skill level from wands, +4 from neck.

## Hero Memories (all 50/50, trait +3)
- Slot 1 Memory of Origin lv86: +110 INT; +16% cast speed; +18% minion crit dmg; +47% cold skill crit dmg; +40% projectile speed.
- Slot 2 Memory of Discipline lv86: +642 max ES; +16% cast speed; +28% minion dmg; +41% spell crit dmg; +40% projectile speed.
- Slot 3 Memory of Progress lv89: +30% movement speed; +10% skill effect duration; +40% minion crit rating; +104% spell crit rating; +54% spell crit dmg.

## Pactspirits (page screenshot) — CORRECTED
- Three Battle Pactspirits installed, all active, each with its own pact page: Witch of the Night rank 6, Iron Lion rank 1, Dreamweaver rank 6. Rank = pactspirit tier, unlocks its lines in order.
- Witch of the Night (Spell Legendary; spell dmg / spell crit / cast speed minor nodes): 1 Night Feather Entanglement stack per active Tangle (max 2); +50% NFE effect; +8% additional spell dmg while NFE; at max NFE stacks gain 1 Focus Blessing per 1s. (Rank 6 → all lines on.)
- Dreamweaver (Spell Legendary; elemental dmg / ele pen / cast speed): +19% additional elemental dmg for spell skills; 1.2% ele res pen per elemental hit (max 4); +3% ele res pen per recent elemental hit (max 4); +4% additional dmg. (Rank 6 → all on.)
- Iron Lion (Attack Legendary; knockback / proj speed / proj dmg): rank 1 only → first line: Projectile Quantity +2 (per tlidb line order; confirm). Later lines (+8% additional atk/cast speed w/ no enemies in proximity, +48% knockback, +14% proj speed) not unlocked.
- "Kismets" = Destinies (tlidb term): installed into already-allocated pact nodes, replacing the node's original effect. Vlad circled 13 blue nodes = 13 Destinies, every one carries INT. Kismet INT = total INT − (gear+memories+tree). Destiny slots replace the pact pages' minor nodes (spell dmg / spell crit / cast speed for Witch & Dreamweaver page sections; proj dmg/speed for Iron Lion section) — exact replaced minors still unknown.
- Pact pages, FINAL (per Vlad; each page = 6 small + 3 big minors, 3 stat types):
  - Witch of the Night: free = Spell Crit I +22% ×2, Spell Crit II +45% → +89% spell crit rating. Kismets (INT): 2× Spell Dmg I, Spell Dmg II, 2× Cast Speed I, Cast Speed II (6).
  - Iron Lion: free = all proj speed (7%+7%+14% = +28%) and all proj dmg (10%+10%+20% = +40%). Kismets: the 3 knockback nodes (3).
  - Dreamweaver: free = all ele pen (2%+2%+4% = +8% elemental resistance penetration), Ele Dmg I +12%, Ele Dmg II +24% → +36% elemental dmg. Kismets: 1× Ele Dmg I, 2× Cast Speed I, Cast Speed II (4).
  - Total kismets = 13 (matches the 13 circled). All INT.
  - Big nodes as noted above (Witch: NFE/+8% additional spell dmg/Focus per 1s at max NFE; Dreamweaver: +19% additional ele spell dmg, up to +4.8%+12% ele pen, +4% additional; Iron Lion r1: +2 projectile quantity).
- Hero trait levels CONFIRMED: Predicted Reincarnation L3 (+50% Boon CDR, +8% additional dmg per Focus consumed, max 5 → ×1.40), Farewell Prophecy L3 (+6% double dmg chance per Focus consumed, max 8), Prophecy of Purity L3 (+1 Boon stack, +5% skill effect duration). All other trait nodes rank 0 (incl. base Wisdom of The Gods).

