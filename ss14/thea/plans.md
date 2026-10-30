# Thea — plans, priced options, open questions

All multipliers on the sheet in `stats.json` unless dated. FE per 1% = expected cost / % gained.

## Decided / in progress
- **One slate swap** on the Judgment line: get a +1 Cold Skill Level (→ +2) where slate #1 has nothing worth keeping → ×1.166. Slate #2's 12.32% additional → +2 cold only nets ×1.04, skip.
- Slate purple lines: roll the weak ones toward **+5 max frostbite** (×1.051 at ×1.54) and **12% proj speed** (×1.049). Other purple options are within 3% of each other; cast is last.
- **Corner slate** (three empty cells, unboosted): 5% crit dmg per Focus (×1.10) or "+10% additional after mobility" (×1.10) beat any pen line (×1.055–1.06). Candidate for **Wilt immunity** (Goddess of Deception slate can roll Shadowmaster's "Immune to Wilt").
- **Magister Frail** (18-pt legendary "Inflicts Frail on spell damage") to replace the Frail lost with the old Nether King: costs 75 crit rating + 15 crit dmg, nets ×1.045.
- **Prophet prism move**: Spell Ripple sits on the +4% frostbite effect micro (costs ÷1.05). Put it on the empty INT micro instead and buy the effect micro back (3 pts).

## Wand crafting ladder (FE per 1%)
1. Tangle Damage Enhancement T2 34 → T1 (+8%): ~145 FE/1%. Take T0 (55–65) on sight.
2. Spell Skill Level +2 → +3 (+8%).
3. Skill-level tier upgrades (T1 +2 → T0 +3, half the time still +2): ~200 FE/1%.
4. Crit rating 166 → T0: ~226 FE/1% and worse after crit changes — skip; eventually replace with spell crit dmg.
- Vlad will not put armor pen on wands. Keeps spell damage % over flat cold on future rolls (phys/weapon-amp options).

## Frostbite cap (found 2026-10-27 in the tlidb glossary)
- **Max Frostbite Rating caps at 120.** At 101 there are only 19 useful points left (×1.127 total at 104.8% effect). Everything below is priced with the cap; earlier quotes that went past 120 were wrong.

## Rings
- **Ring L**: two ultimate slots. INT 52 → **armor pen** (×1.13 net, ~90 FE/1%) first; second ult **damage → +1 Max Focus** (×1.076). Crit → max frostbite is now only ×1.01 net (the +30 is capped at +19) — dead option.
- **Heart of Magic** (ring, graft): base ×1.24 < Ring L ×1.28; corroded ×1.44 (+12% over Ring L) but −57 res. Buy only cheap.
- Ring L res → T1 crit dmg (advanced, ×1.108) after freeing the res with kismets: needs 16 more lightning res (3 micros or medium + micro, ~40 INT → net ×1.05).
- **Ring R**: max frostbite T2 20 → T1 ~32 (+12 → 113, under the cap: ×1.07, ~166 FE/1%); arp T2 10 → T1 ~15 (×1.06 on the 60% armor rule, ~185 FE/1%).
- Frostbite headroom is shared: Ring R T1 (+12) + slate +5 line (+7.7) already fills it to ~121. Cage corrosion's +20 max frostbite is then worth nothing.

## Big buys
- **Pantheon's Elegy** (~13k + ~2.5k for Gale): Hunting dirge (Precise: Swiftness +120% atk/cast, scales with aura effect) ≈ ×1.33 now; + Steel Vanguard (Swiftness Dew + Resistance Dew); third dirge decides it (God of Machines +2–4 main skill ×1.17–1.36, Prophet +40% frostbite effect, God of War +15–20% additional on crit). Loses 47% dmg, 31 INT, 220 ES, 52 res. ×1.37–1.48 with a real third dirge → 320–420 FE/1%. Good mapping belt (MS, area dirge option).
- **Corrosion** (values only, no budget): I Am Truth corroded is +7–8 all skills (tlidb) → +3–4 levels ×1.26–1.33 · Israfel corroded 18–19 per Focus (and +4% crit dmg per Focus) ×1.21 · Malign corroded +12–20% additional spell ×1.12–1.20 · Cage +20 max frostbite ≤ ×1.127 and 0 once the cap is filled elsewhere.
- **Immolating World** (neck): Vlad thinks it's the strongest Thea unique. With 40% CDR you instantly gain full Focus and Tenacity; +4 Tenacity → 8/8 → True Flame Immolation base 3,728 vs Chromatic's ~2,390 effective. **Not priced yet — do it properly.**

## Defense plan (after DPS is enough; target ≥ 15 T)
- Memories: all 6 random lines → 3 spell block + 3 attack block (31% each), Ring L INT → block T1 → 100% block. **Defensiveness** (+25% block ratio → 55%) via the Pedigree slate (with Off The Beaten Track); swap **Lich → Warlock** and take Dirty Tricks there.
- Priced: memories ÷2.0 (÷1.81 keeping one proj speed line), Lich → Warlock ×1.14, ES −24%. Lands ~13.5 T (six block) / ~15 T (five block + one proj speed).
- Lich's CDR replaced by **Priceless boots with CDR implicit** (24%): CDR 33.5 / duration 55 → Boon 2.07 stacks, OK.
- Ailment immunities: Ignite (Fallen Starlight slot), Trauma (ring base), CC (prism), Wilt (missing → Goddess of Deception slate).
- DoT: Cage ×0.75 DoT taken; block does nothing vs DoT → res + ES + regen.

## Hero memories
- Shape is right (3 crit dmg, 1 crit rating, 2 proj speed). Real gains: T1 → T0 on the four T1 lines (×1.12 total); the three purple minion lines are dead slots — memories with a player line there (crit dmg 38–42, proj speed 30, crit 80, damage 44–52) would be up to ×1.25.

## Vorax chest with a Core Organ (2026-10-30 17:50, corrected after Vlad) — belt ON (proj speed pays through Gale)
Vlad's rules that I had wrong: a belt Blending Ritual replaces Gale (no); Extreme Coldness on GEAR does not block the Frozen Lotus core — Max Active
Divinity 1 is about slate/core divinities — so the real comparison is Cage chest + Frozen Lotus core (after the Spell Ripple -> aura-effect/CC-immune prism
swap) vs Vorax chest + Extreme Coldness in the Prophet core (Frozen Lotus x1.25 lost); penetration takes res below 0 (parser was dropping the pen half of
the "+8% cold +15% pen at 8 Focus" line — fixed in stats.py); Double Rainbow with all three elemental res identical = 3 pairs = 1.19^3 = x1.685 [Vlad];
one pair = x1.19 (if the game counts floor(3/2), the package is x1.15 instead of x1.63 — check on the dummy).
Engine, vs the Cage chest (Cage x1.69; Extreme Coldness kept via the core), then /1.25 for Frozen Lotus:
  Rainbow x1.685 · +20% Aura Effect x1.245 · +45% proj speed x1.113 (belt on) · +100 INT (block-ratio base, kismets/ring back to INT) x1.128 ·
  T1 crit rating x1.115 · ultimate prefix: "+8% add cold +15% cold pen" x1.18 (res 5% -> -10%) > +2 Active Skill Level x1.166 > 20% sealed comp (7 Lich pts)
  = x2.04 engine -> **x1.63 over the Cage** (x1.57 belt off); Vlad's own count 1.55. Adv suffix: 10% ele res is what makes Rainbow's condition true;
  18% INT or 60% crit dmg would be x1.11 each if the res were already equal. 2nd Rainbow line (-7% taken per pair, x0.80 taken) if both legendary lines come.
- Organ: Iced Drinker's Cage (his own chest) as the alternative: Cage stacks x1.69 = Rainbow's x1.685, but if Extreme Coldness can be its 2nd line the
  Prophet core stays Frozen Lotus -> x1.25 over the Rainbow version and no res balancing; costs the 3,160 chest instead of a 260 Rainbow. Open: are the
  organ's 2 affix options picked or rolled?
- Engine fixes 2026-10-30: Cage multiplier follows the chest's buff.cage effect (was hardcoded); the cold+pen Focus line now yields add.cold and pen.res.
- Cost (tools/vorax_cost.py, Vlad's crafting rules 2026-10-30 18:00): chest with Block Ratio base 4,000; uncorroded Rainbow 400 / Cage 3,000 +
  Exquisite Suture 424 per graft; organ offers 2 of the legendary's affixes (Rainbow 4: wanted line 1/2; Cage 5: either of 2 wanted 7/10, then the other
  1/2); the line lands on a random one of the 6 slots and must hit a Basic (2/6, then 1/5 — can't hit the L), else the chest is scrap.
  Expected: Rainbow 17.0k (+ mods ~1.7k: aura = Flawless Nerve: Entwined 575, cold/pen = Flawless Tongue: Apathetic 18, +2 Active = Nerve: Compelling 202,
  comp = Nerve: Unsealed (Pre-fix) 370, proj speed 1-of-5 adv prefixes x Vital Organ Matchless 62.5 = 312, 10% ele res 1-of-10 x 62.5 = 625, basic x Vital
  Fine 22). Cage stacks only 37.8k; Cage stacks + Extreme Coldness 168k (Vlad's nested count 160k). If the organ can be grafted onto an all-Basic item
  (six Rotten Organ Fine, 0.5 each) the landing odds vanish: Rainbow 5.7k, Cage one line 12.6k, Cage both lines 15.7k (-> keeps Frozen Lotus, x2.04).

## Open questions for Vlad
- Which boots res line Hasten replaced; current kismet layout.
- Exact lines on each GoK slate and where Fallen Starlight sits now.
- Max frostbite now (did the +5 frostbite slate line land?).
- Wand S off test (1.4 vs 1.75 predicted) never resolved.
- The 9.7 T "INT ring off" test — what was removed.

## Prism (found 2026-10-27 in the raw prism affix pool)
- Only one Ethereal Prism (+ one Inverse Image) can be installed.
- **Keen Intellect alone vs Spell Ripple: x1.23** (3 Empower skills x1.443, Speed Phantom as Mobility +13% additional cast, Biting Cold as Curse +6% res pen / +6% arp) vs Ripple's measured x1.5.
- **Slot 3 legendary affix "Mutated Core Talents no longer replace the original talent, but add [core]"** (cost -5% ele res / -30 all stats / -8% defense): Prophet keeps its own core (Mind Blade +25% additional cold with a wand). On the Ripple prism x1.25; on a Keen Intellect prism x1.54 total. ~70% read that each prism rolls only its own core's mutate. Need prices: Keen Intellect prism, Legendary Prism Gauge.
- Frail on a slate vs the 7.7% crit dmg per Focus line (~77 crit dmg): x1.15 vs x1.149 — even, keep as is (and the +3 pen line for clear).

## Slates (priced 2026-10-27 on the screenshot build)
- **GoK #2 dead orange brand (channeled +8%) is the best slot on the board**: -> +1 Spell Skill Level (+2 on the line) x1.224 · +1 Cold Skill Level x1.183 · +5% crit dmg per Focus x1.147 · +10% vs Frozen x1.140 · +12% INT x1.099.
- GoK #2 dead purple brand (Spell Burst charge): -> +12% proj speed or +5 max frostbite x1.049 (frostbite 108.7 -> 116.4, under the 120 cap) · crit/crit dmg x1.044 · frostbite effect x1.042.
- A Corner of Divinity is worth x1.154 (77 crit dmg at 10 Focus) + 3 pen for clear. Replacing it with a non-legendary slate carrying +1 all skills on the line (+2) nets x1.11 and loses the pen — not first.
- Fallen Starlight: 0 DPS, it is the Boon 2-stack margin (duration/CDR). Stays.
- Max Active Divinity 1 on the Corner's crit dmg per Focus does not block the Magister tree copy: both are needed to reach the sheet's crit dmg.
- Prism slot 3: Vlad wants Immune to Crowd Control there, not the mutate-core affix.
- Ideas welcome without prices, but no double-corrosion / Vaal-style suggestions on expensive bases.

## New GoK slate to replace GoK #2 (2026-10-27, `tools/slate_plan.py`)
- Facts (Vlad, 12:00): every base = 2 fixed legendary nodes + 2 legendary (orange) slots + 1 rare (purple). A brand can't roll a node already on the slate (pool excludes it; 36 - 2 fixed = 34 -> his 2.96%). Equal odds inside a pact panel. **Overwriting mediums/purple is free.** The slate "+8% additional Spell Damage" line IS the Arcanist node (mana consume doesn't matter). Naked roll 14 FE, Unifying Wedge 16 FE.
- Prices: pacts GoK 277 · Arcanist 70 · Magister 50 · Elementalist 170 · Prophet 180. Bases (fixed pair): S+A 300 (owned, branded, sunk) · F+A 180 · S+F 900 · C+F 750 · **S+C 400** · F+Z 388 · F+B 150 · C+A 66 (read "cold spell 66" as +1 Cold + 8% additional).
- Node letters: S +1 Spell (GoK) · F +1 Focus (Arcanist) · A +8% additional (Arcanist) · C +1 Cold (Elementalist) · E ele pen per ailment (Elementalist, ~5% left before enemy res is gone) · Z +10% vs Frozen · B +20% frostbite effect (Prophet) · I +12% INT (Magister). Dead for us: GoK Focus (MAD1 dup of GoK #1, ~85%), Magister crit/Focus (the Corner), Frail (tree), Cold Infiltration (GoK #1), the rest.
- For Vlad the GoK pool is 1 good node (S), not 2. On an S base the GoK pact is 4 dead nodes.
- Baseline = GoK #2 after its free purple -> +12% proj speed (x1.049 on the current sheet; do it now).
- Finished 2-leg slates (2 fixed + 2 brands, free purple): S F C Z 1.201 · S F A C 1.183 · S F C B 1.163 · S F C I 1.158 · S F A Z 1.140. 3-leg: S F A C Z 1.349.
- **Decision (lam 150 FE/1%): buy the S+C base (400).** Each round: Arcanist pact on slot 1 (F or A, 1/3). F -> stop, free medium in slot 2: x1.105. A -> Arcanist pact on slot 2 for F (1/5): x1.183, miss -> restore. Dead -> restore (from restore 4 on, also try slot 2). Ends: x1.105 64%, x1.183 13%, x1.054 12%, nothing 12%. ~5 Arcanist pacts; ~570 FE of rolls/restores + 400 = ~970 FE for +9.6% expected (~100 FE/1%). Worth buying up to ~880 FE (~410 at lam 100).
- Owned S+A slate: same Arcanist plan only reaches x1.049 (F + medium), ~290 FE for +2.9% expected. Fallback only.
- S+F (900, worth <= 361), C+F (750, <= 211), F+A, F+Z, F+B, C+A: don't buy.
- 3-leg bases (need price + whether they also have a rare slot): worth up to S+C 1,780 · S+Z 1,176 · S+F 974 · C+F 771 · S+A 751. 2-leg S+Z worth up to 385 (no price yet).
- **2026-10-27 12:18 — Arcanist Focus landed on the first try** (S+C base, lv86): fixed +1 Cold, +1 Spell; brands purple +6% life/+6% ES, orange Arcanist Focus, orange +2.5% ES regain (medium). Spent 400 + 84 = 484 FE.
  Orange 2 options (expected gain vs keeping its medium at +10.5%): Prophet pact +9.0% (194 FE) · Arcanist +8.0% (84) · naked +7.0% (14) · Magister +6.4% · Elementalist +6.2%. Any miss drops to x1.054 and only a restore (which wipes Focus) undoes it. **Decision: stop. Free-overwrite the mediums to +5 frostbite and +12% proj speed, equip in GoK #2's spot.**
  Prediction vs the current build: x1.159 with the belt; belt-off 12.12 -> 13.40 T (x1.105; proj speed only feeds Gale, invisible belt-off).

## Pactspirits (scanned 2026-10-27 from the pact page screenshot + tlidb)
- Board matches the encoded setup: Witch r6 (3 free spell crit nodes, 6 kismets), Iron Lion r1 (6 free proj speed/dmg nodes, 3 kismets on knockback), Dreamweaver r6 (5 free pen/ele nodes, 4 kismets). 13 kismets = 9 micro + 4 medium.
- Only spell legendary worth a look: **The Bone worm's Daughter** (L6: +140 flat spell crit rating at 2 ailments, +14% +36% crit dmg, +4% additional; ring Spell Dmg / Crit Dmg nodes). Engine: in Iron Lion's slot x1.31 (L6) / x1.14 (L1), but that loses Sword Rain's +2 projectiles (~x0.62) -> net loss. In Witch's slot x1.22 on paper, but Witch's NFE is 9% CDR and the Boon 2-stack margin is only 1.03 (without it 0.958 -> Boon breaks). In Dreamweaver's slot x0.85. **Keep all three.**

## Model open items (2026-10-27)
- Speed Phantom now has **Mass Effect** (Exhaustion was +17% for Speed Phantom's own hits only, dead for Chromatic). Engine still models Euphoria as 8 stacks x 3.25% without ME. Unknowns: Euphoria stacks on a single dummy (1 per enemy hit per Remnant), and ME charges (ME +1, Fallen Starlight +1 max charges, Lich +1). Test: belt off + Ring L off, no Speed Phantom casts.
- Periodic Burst (tlidb now): +30% atk/cast speed for 2 s after a mobility skill, a stack every 6 s. Engine uses a permanent +20 cast speed.
- Memory Revival (tlidb): revival adds a revived affix (Young Moon), raises base stats (Wax and Wane) or fixed affix tiers (Rising Moon); only 1 revived memory can be installed. Vlad's revived Origin shows no other affixes; INT 543 and the 9.4 T pull both fit that.

## Auras: Precise versions, Weapon Amp, Stand as One (priced 2026-10-27, boss/dummy)
- Prices (Vlad): Precise Frigid Domain 270 · Precise Spell Amplification 475 · Precise Precise Projectiles 950 · Precise Domain Expansion 470 · Precise Weapon Amplification 138 · Precise: Stand as One 2,450 each (one per aura).
- Precise = +5 points of additional at the same level (x AA 12.25%): Frigid x1.038 (70 FE/1%) · Spell Amp x1.039 (123) · Precise Proj x1.039 (241) · Domain Expansion x1.000 on bosses (its extra is +4% additional area at 5+ enemies: x1.03 in packs).
- Weapon Amp hits only the phys-origin part of the hit (Vlad: works on converted phys, not on the wand's flat cold). Base 904 = 664.5 Chromatic phys + 118.7 flat phys (86.7%) + 120.5 flat cold. **Precise WA = x1.438 effective; in Domain Expansion's place x1.024 for 138 FE (~59 FE/1%)**, loses DE's +20% area at 8+ enemies. Plain WA in DE's place x0.989 (loss). Max 4 auras equipped (5th only via Spell Amplification: Lone Walkers — separate discussion).
- Stand as One with 5 auras: +34.5% aura effect, x1.088-1.097 each; all five x1.56 for 12,250 FE (218 FE/1%) vs four x1.33 for 9,800 (294 FE/1%).
- Stand as One: +6.9% aura effect per aura affecting you (lv29) x 4 = +27.6% on the supported aura. x1.071-1.081 each (300-350 FE/1%); all four x1.35 for 9,800 FE. Goes in the filler slot (Increased Area on Precise Proj / Spell Amp, CDR on DE; Frigid shows an open slot).
- Order: Precise Frigid -> Precise WA in DE's place -> Precise Spell Amp -> Precise Proj -> Stand as One. Engine now reads auras (incl. Precise: and Stand as One) from build.skills.others.
- One Stand as One copy (best on Frigid): 4 auras x1.077 (316 FE/1%), 5 auras x1.097 (253 FE/1%).

## Lone Walker's Boots (priced 2026-10-27, from the build)
- tlidb: +1615 evasion · granted random Lv20 Precise bonus-damage aura (want: Precise Spell Amplification) · +50% MS · +(15-30)% aura effect at 4-5+ auras · +2% aura effect per +3% Sealed Mana Compensation.
- Compensation 18% (Vlad: from the prism): Spell Ripple prism gives +2% comp to the mediums in its area, 3 mediums x 3 ranks = 18% -> +12% aura effect. Not in build.json yet (prism lines missing; add them).
- Costs: Hasten (x1.08 additional cast + 7% cast). Crit mitigation 118% now (58 boots + 60 Fluffy Ball) -> a second Fluffy Ball (medium 40-60%) in place of a medium INT (~25). Fire res 61% (boots 22 + rings 12/27) -> 39%; +21 needed; fire fates 5-7 / 10-14 = 2.25 INT per 1% -> ~50 INT. Total ~-77 INT.
- ES (build): flat 3,337 (helmet 347, chest 508, gloves 469, boots 720, belt 220, rings 431, Discipline 642) x (1 + trees 90% + slate 9.24%) ~6.65k (Vlad: no INT -> ES bonus on his character). LW + Precise EF ~8.1k (+22%); LW without EF ~5.2k (-22%).
- Precise Energy Fortress lv25: +346 ES, +19.3% additional, x aura effect (AA 12.25 + boots 39 at a 27% roll = x1.51) -> +524 ES, +29% additional.
- Results at -77 INT (roll 15 / 27 / 30%):
  - EF in Spell Amp's slot: x1.05 / **x1.18** / x1.21 damage, ES ~8.75k / 9.03k / 9.10k (+16-20%).
  - Precise WA in Spell Amp's slot + EF in DE's slot: x1.08 / **x1.21** / x1.25, same ES (loses DE's area at 8+ enemies).
  - Precise WA, no EF: x1.61 / **x1.87** / x1.95, ES ~5.82k (-23%).
- Need: LW price for a Spell Amp + ~27% roll.

### Lone Walker's as a compensation-scaling build (2026-10-27)
- Rule [tlidb]: actual sealed mana = initial / (1 + compensation). Auras seal 50%. Support mana multipliers: AA 100%, Restrain 100%, Increased Area 110%, CDR 110%, Seal Conversion 100%; Off The Beaten Track fixes them at 95%.
- Now: 3 mana auras x 50% x 0.95^3 / (1 + 18% + Restrain 14.5%) = 97.1% sealed.
- Vlad's idea: drop the filler supports and OTBT, take +1 all skills -> supports lv26 (Restrain 13%). Global compensation needed:
  all 4 auras on mana: 87% (91% keeping ~2% mana free) · keep OTBT instead: 66% · Frigid on life (Seal Conversion), 3 on mana: 37%.
- LW then turns every +3% global compensation into +2% aura effect on all 5 auras (~0.75% damage per 1% compensation).
- DPS vs now (LW, Precise WA in Spell Amp's slot, -77 INT, no Hasten, no OTBT, +1 all, 27% roll): comp 87% all on mana (loses Lich's +10% sealed mana+life) x3.09 · comp 87% Frigid on life x3.40 · comp 37% Frigid on life x2.29 · comp 60% x2.77.
- Global compensation sources: Lich (legendary +8% MAD1, medium 3% x3, micro 1.5% x3), helmet ultimate prefix 15-20% + base 6-8% (or corrosion base 10-15%), necklace ultimate suffix 15-20% + base 6-8%, prism area +2% per rank on nodes (now 18%), Lich/Nether King slates +8% / +3%, Glacier Caster Shield (offhand, n/a).
- Engine: `off_the_beaten_track` context switch added.

## Lich -> Warlock + Phantasmagoria + Lone Walker's — FIRST PASS, SUPERSEDED (counted micro AND medium comp; wrong area anchor)
Vlad's plan: Lich out, Warlock in (Dirty Tricks core), Pedigree -> 2-core Pedigree (Defensiveness + a damage Lv.1 core), Spell Ripple prism out
(Frozen Lotus core back), Ethereal Prism: Phantasmagoria (+75% random affixes: 3.5% sealed mana comp per micro/medium rank in area,
"2 legendary mediums in area: Immune to CC / -25% Defense"), Lone Walker's (comp -> aura effect), Frigid on life.
- Comp needed with Frigid on life, no OTBT (supports lv24, Restrain 12%): 38%.
- **Best prism spot: Prophet 608_176** (same cell as Spell Ripple, the +4% frostbite effect micro), 4 wide x 3 tall, columns 352-736, rows 80-272:
  9 micro/medium (27 ranks = 94.5% comp -> LW +62% aura effect, +89% with a 27% roll) + 2 legendaries (480_272 cold res, 480_176 "Inflicts Frostbite", 1 pt, CC only).
  If the 4-wide area extends to the RIGHT of the prism instead, use Prophet 352_176 (columns 224-608), same 94.5% + CC.
- Pedigree Lv.1 core (with the 5T hit cap modeled): Insight (+30% additional spell; Frozen Lotus kills the skill-cost downside) best and unconditional;
  Third time's a charm ~equal in the damage build (+2%, needs movement); Blunt -1%; Impermanence worst (x1.43 uncapped, but crit+quad hits go far past 5T).
- Results vs now (34.4 T with belt; dps with belt):
  - tank, prism left-anchored: x1.84 (63 T), freed slot Precise Energy Fortress, Warlock life/ES 27% -> ES ~7.5k (+13%, after -25% Defense) 
  - damage, left: x2.83 (98 T), Precise WA in the freed slot -> ES ~4.3k (-35%); hit cap factor 0.87
  - tank, right-anchored (352_176): x1.67 (57.5 T) · damage right: x2.66 (91.5 T)
- Steps (tank, left): Lich -> Warlock x0.94 · Spell Ripple -> Frozen Lotus x0.83 · LW (+89% aura effect) + EF, -77 INT, no Hasten x1.86 · Insight x1.30.
- Costs to fix: Boon margin 1.03 -> 0.93 (Lich's 12.5% CDR gone; needs +9% CDR or +12% duration, else 2nd stack ~86% uptime, ~x0.94 sustained);
  Mass Effect 3 -> 2 charges and +1 all skills (lvl 39) gone (both modeled); CC immune costs 25% Defense (= armor + evasion + ES).
- Assumptions: Phantasmagoria has both the micro and medium 3.5% affix and it scales per rank (like Spell Ripple's 18%); LW roll 27%; Defense -25% added to the ES% pool.

## Lich -> Warlock + Phantasmagoria + Lone Walker's — corrected 2026-10-27 14:10 (`plan_trees_{tank,damage}_{micro,medium}.json`)
- Vlad: a Phantasmagoria has EITHER "3.5% comp per micro" OR "per medium" in its area (per rank, like Spell Ripple's 18%). Areas: 3x4 = 1 col left, 1 right,
  1 row above, 2 below; 4x3 = 1 left, 2 right, 1 above, 1 below. Need 38% (Frigid on life, no OTBT) + 2 legendaries (CC).
- **Micro prism (best): Prophet 352_176** (the empty +6% attack/cast medium), 4x3 = columns 224-608, rows 80-272. Micros counted: +15% crit (have),
  +2 max frostbite (have), +3% attack/cast (new 3), +4% frostbite effect (new 3, Spell Ripple's old cell), +4% cold res (have), +8 INT (new 3) = 18 ranks = 63%.
  Legendaries: cold res (have) + "Inflicts Frostbite" (1 pt, CC only). Tank x1.57 (Impermanence, 54 T, ES ~7.2k +8%) / damage x2.40 (Insight, 82 T, ES ~4.3k -35%).
- **Medium prism: Prophet 608_176** (Spell Ripple's cell), 3x4 = columns 480-736, rows 80-368. Mediums: crit (have), +5 max frostbite (have), +8% frostbite effect (have),
  +5% INT (new 3), 2.5% regain (new 3) = 15 ranks = 52.5%. Tank x1.47 (Impermanence, 51 T, ES ~7.0k) / damage x2.23 (Insight, 77 T).
- Pedigree Lv.1 core: tank (Energy Fortress, hits stay under 5T) -> Impermanence; damage (Precise WA, cap bites) -> Insight. Third time's a charm last in both.
- Warlock 24 is the same in every variant. Boon CDR (margin 0.93) parked by Vlad.

### Prices and buy order (Vlad 2026-10-27 14:19; model at LW roll 26%)
- Prices: Lone Walker's 26% roll 15,000 · Phantasmagoria (micro) 4,500 · Pedigree Defensiveness + Impermanence 6,000 · kismets ~0 · Precise Energy Fortress: ask.
- Tank micro plan at 26%: **x1.553 (53.5 T)**, ES ~7.2k (Precise EF) / ~6.8k (plain EF, same DPS). 25,500 FE -> **461 FE per 1%** (+ EF).
- Roll: 15% x1.423 · 26% x1.553 · 30% x1.599 (each roll point ~0.75%; a 30% is worth <= ~1.4k more at the package rate).
- Buy order (both end at x1.553):
  - **LW first** (current trees, Spell Ripple prism 18% comp, Precise EF in Spell Amp's slot): x1.167 for 15k (898 FE/1%), ES ~8.1k (+21%);
    then Warlock + Pedigree + Phantasmagoria 10.5k: x1.331 (317 FE/1%), ES -> 7.2k (CC immune -25% Defense).
  - Trees first: x1.035 for 10.5k (mana fits: 3 auras x 55% / 1.75 = 94%), then LW x1.50.
- Glass reference: LW + Precise WA in Spell Amp's slot on the current trees x1.851 for 15.1k (163 FE/1%), ES ~5.2k (-22%).
- Checked: Precise WA in Domain Expansion's slot of the tank plan is x1.04 only (DE is x1.64 there: "additional Area Damage" counts on Chromatic).

## TOWER Sequences on the wands (priced 2026-10-27; one per wand, `docs/crafting.md`)
- Now: wand M "+8% additional Spell Damage", wand S "+16% Cast Speed" (both already in build.json).
- Intermediate, replacing S's 16% cast (current build / after the LW tank plan): 8% additional Spell x1.031 / x1.011 · 6% ARP x1.027 / x1.007 ·
  10% additional on Crit x1.018 / x1.001 (adds into the on-crit bucket with Malign's 42%) · 8% All Stats x1.015 / x0.993 · +55 Spell Crit x1.008 / x1.005 ·
  8% Cold pen x1.007 / x0.993 (res floored at 0; ~x1.035 if res can go negative). M's 8% additional Spell is already the best Intermediate.
  Under the 5T cap (LW plan) all Intermediates are within 1% of 16% cast speed: cast speed isn't capped.
- Advanced (In-Depth R&D), in place of S's 16% cast: Lv20 Overload x1.261 / x1.160 (+4% per Focus, 8 stacks = +32%) · Lv25 Control Spell x1.213 / x1.117
  (read: its -50% crit rating is the additive kind, 754 -> 704%) · +35% / -10% cast x1.160 / x1.058 · +1 Focus +1 Agility x1.128 / x1.083.
  Pairs: Overload + Control Spell x1.482 / x1.242 · Overload + 35% x1.418 / x1.173 · Overload + Focus x1.378 / x1.227.
  Dead: Spell Burst +25% (no Spell Burst), 200-220 cold (needs 800 INT, have 543), +120% Spell Amp (-20% its compensation; doesn't fit at 97% sealed).
- Vlad: pen can go negative -> 8% Cold pen is the best Intermediate for S: x1.036 (8% spell x1.031, ARP x1.027); after the LW plan x1.014.
- In-Depth R&D 640 FE/try. Chasing one code: Overload ~17.2k FE (3.7%/try, x1.261 -> 659 FE/1%), Control Spell ~22.6k.
  Taking the first useful hit (Overload/Control/+35%/Focus): 12.9%/try, ~4.9k FE to a hit, avg +17.8% -> **278 FE/1% now, 485 after the LW plan**
  (220 / 380 if an offer never repeats a number).
- Vlad takes 8% Cold pen on S now (cheap). vs cold pen: Overload +21.7%, Control +17.1%, +35% +12.0%, Focus +8.9% -> optimal picks EV +1.77%/try,
  **361 FE per 1%**, stop at the first hit (pick table in docs/crafting.md).
- Vlad 2026-10-27 14:42: in the tank plan the memories get re-rolled to block (every mod -> T0 attack/spell block, 3 attack + 3 spell, to cap block).
  Their damage lines go, so hits drop well under 5T: the cap haircuts above ("after the LW plan") mostly vanish, and the x1.553 for the tank
  package assumed the current memories. Price the block re-roll when Vlad brings it up (parked by him).

## Block plan: Lich -> Warlock, Pedigree Defensiveness + OTBT (3.5k), memories + ring L to block (priced 2026-10-27 14:44)
- Free find first: **tree reshuffle on the CURRENT build (Lich kept) x1.134** (`plan_trees_reshuffle_now.json`): GoK +18% dmg 1->3, +20% spell crit 0->3,
  +15% spell crit 0->1, +9% spell 3->1, +9% dmg 3->1; Magister +20% spell crit 1->3, Focus-on-Spell-Burst 1->0 (dead), +8 INT 3->1, Focus dur 3->2;
  Prophet 1.5% cold pen 0->3 (pen goes negative), +15% crit 3->2, +2 max frostbite 3->1 (108.7 -> 104.7, still Frozen). Crit 69 -> 77%.
- B1 = Lich -> Warlock (24, same as the tank plan) + 9 spare reshuffled, Pedigree Defensiveness + OTBT, Spell Ripple kept (`plan_trees_warlock_otbt.json`):
  **x0.961 (33.1 T)**; mana 97.4% sealed (Restrain 14% at support lv28) fits; Boon margin 0.93 (parked); Mass Effect 2 charges; Chromatic lv39.
- Memory lines read as fixed (cast / duration / minion) vs random (crit dmg, crit rating, proj speed), from the tlidb pools. Block T0: random 25-31, fixed 15-21,
  trait slot x0.42 (-58%); ring "Attack and Spell Block" is an Advanced prefix (T1 12-15, T0 16-20) = the INT line's group (64% damage is Basic).
- Line values on B1: 40% proj speed x1.11 each (feeds additional proj dmg) · 54% spell crit dmg x1.11 · 47% cold crit x1.097 · 104% spell crit rating x1.095 ·
  26% cast x1.086 · 41% spell crit x1.083 · 16% cast x1.051 · ring INT x1.080 / 64% dmg x1.076 · trait 18% crit lines x1.035 each · minion lines and duration x1.000.
- Vlad's version (6 random -> block, ring -> block): x0.499 on B1 -> **x0.480 (16.5 T)**.
- Best (max rolls, fixed slots can roll block): attack = 3 minion lines (21 each) + trait minion AS (8.8) + Discipline 16% cast (21) + ring 15 = 107.8;
  spell = Discipline 41% spell crit dmg (31) + Progress 104% crit rating (31) + trait 18% spell + 18% cold crit (13 each) + ring 15 = 103.
  Keeps both 40% proj speed, 26% cast, 47% cold crit, 54% spell crit dmg, 10% duration. x0.690 on B1 -> **x0.664 (22.9 T)**.
  Average rolls (28/18, ring 13.5): best x0.633 -> 21.0 T; ring T0 18: 21.8 T. Orange memory + ring untouched: 104/104 -> 21.7 T.
- **CORRECTION (Vlad 14:56): fixed memory affixes can't be re-rolled** (fixed = fixed). The 22.9 T layout above is invalid. Options Vlad priced:
  new Discipline with fixed cast + fixed block (+ES base) 3,333 FE; Discipline fixed block + minion (loses 16% cast) ~1,000; Progress duration + block: not obtainable.
- Other block sources found: belt "+31 INT" is an Advanced prefix -> "Attack and Spell Block" (T1 12-15, T0 16-20); Magister 352_464 +4% spell block micro x3
  + 480_464 legendary +12% spell block (4 pts: x0.956 on B1); INT kismets -> Medium Fate Spell/Attack Block 12-15 (for 24-30 INT) / Micro 6-8 (for 12-15 INT).
- Re-priced (only random slots, orange memory random lines, ring INT, belt INT, INT kismets, Magister nodes):
  mid rolls (28 / 13.5): **18.1 T** (x0.524): convert Discipline 41% spell crit, Progress 104% crit rating, both orange 18% crit lines, ring INT, belt INT,
  4 medium INT kismets, Magister +24% spell block. Keeps Origin 47% cold crit + 40% proj speed, Discipline 40% proj speed, Progress 54% spell crit dmg.
  Max rolls (31 / 15): 20.0 T with 2 kismets (spell exactly 100). New Discipline cast + block (3,333): 20.0 T mid (x1.105, 316 FE/1%) / 20.9 T max (699 FE/1%).
  ~1,000 Discipline (block + minion) is worse than keeping the current one.
- **Boon (Prophecy of Purity 2nd stack) without Lich** (2026-10-27 15:46): margin = 0.5 x (1 + duration) x (1 + CDR) = 0.5 x 1.59 x 1.17 = 0.93 ->
  2nd stack up 86% -> **x0.923 sustained** (2 stacks are x2.23 vs 1). The block-plan T above assume full Boon: real 18.1 -> 16.7 T, 20.0 -> 18.5 T.
  Need (1+dur)(1+CDR) >= 2: +8.8% CDR or +12.7% duration. No CDR/duration nodes on GoK/Magister/Prophet/Warlock.
  Fixes: **Discipline fixed +10% CDR + block** (instead of cast + block): margin 1.01, 19.0 T sustained (best) · Discipline fixed +10% duration + block: margin 0.989, 18.8 T ·
  Prophecy of Purity L4 (+15% dur vs +5) 0.989, L5 (+25%) 1.047 · Kismet: Scorpion Stinger +3-5% dur 0.959 (x0.955) · Pedigree micro/medium slot Lich +4% dur 0.954 ·
  I Am Truth CDR variant instead of its 40% duration: 0.934 (no). Belt/boots CDR are Ultimate suffixes (not on rares).
- **Vlad's order (2026-10-27 16:20)**: 1) Pedigree Defensiveness + OTBT 3.5k first (only 3 on the market); 2) Arcanist Girdle with 20% CDR implicit (150 FE) + Gale (4,200 FE);
  3) roll memories. Belt base-affix pool also has 20-25% duration, 6-8% sealed comp, 7-8% aura effect, Has Hasten (tlidb).
  - Belt CDR 20 -> CDR 37, Boon margin **1.089** (fixed). Belt Advanced prefix -> Attack and Spell Block T0 16-20 (tier upgrade from T1).
  - The new belt must rebuild the old one's +47% damage (x1.055) and the 3 res lines (19/17/16); +220 ES is defence only.
  - Result (sustained, Boon full): current memories **19.0 T** mid rolls (memory 28, ring T1 13.5, belt T0 18, 3 block fates) / 20.0 T max rolls;
    + Discipline cast + block 3,333: 20.9 T (x1.100, 333 FE per 1%). Converts: Discipline 41% spell crit, Progress 104% crit rating, orange 18% x2, belt + ring INT.
  - Tip: buy the Pedigree now but slot it (and respec Lich -> Warlock) when the belt is ready: in between the Boon dip makes it 30.5 T sustained.
- **Full layout v2 (Vlad 16:27 + belt pool)** -> **21.7 T sustained** (Boon 1.089):
  - Belt (Arcanist Girdle, 20% CDR base + Gale; 1 adv + 2 ult + basics): prefix = Adv Attack & Spell Block T0 · Ult -(16-18)% additional damage taken at Low Mana
    (Low Mana = under 35% mana; 97% sealed -> always on) · Basic % damage T0 73-94 (+0.8 T vs 47%). Suffix = Ult Double Damage (only 7% counts, 193 -> 200 cap: x1.036)
    · Basic lightning T0 + cold (T1 is enough). Loses the old belt's 220 ES and its 16% erosion (erosion 43 -> 27).
  - Res: lightning ring 22 + belt ~31 + 1 kismet ~7 = 60; cold belt + ring 12 + Prophet 30 >= 60; fire 61 unchanged. Frees 2 lightning micro kismets.
  - Kismets: 2 big INT -> medium attack + spell block; 1 small INT -> micro attack block; freed lightning micros -> 1 micro attack block + 1 INT. INT ~400.
  - Block (avg rolls): attack belt 19 + ring 19 + orange 11 + medium 13.5 + 2 micros 7 + 1 memory roll 28 = 104.5; spell belt 19 + ring 19 + orange 11 + medium 13.5
    + 1 memory roll 28 + Magister micro x3 12 = 102.5. Memory rolls: Discipline 41% spell crit (attack) + Progress 104% crit rating (spell); keeps both proj speeds,
    47% cold crit, 54% spell crit. Vlad's version with 1 micro attack fate: 19.7 T (belt 47%, no Double) but attack 97.5-99 at average rolls.
- **Layout v3 (Vlad 17:08: fates maxed and cheap, avoid main-memory rolls; belt basic prefix ES vs damage)**:
  - Fate maxes: block micro 8 / medium 15 (2 smalls > 1 big), INT 15 / 30 and res 7 / 14 (even). Block goes in micro slots, INT stays in mediums.
  - Kismets: 7 micros -> block (5 INT micros + 2 freed lightning micros); 3 INT mediums (incl. the reserved one) 90 INT; crit dmg micro, 1 lightning micro, crit mitigation medium stay.
  - Attack = belt 19 + ring 19 + orange 11 + 3 micros 24 + one memory roll 28 (Discipline 41% spell crit) = 101; spell = belt 19 + ring 19 + orange 11 + 4 micros 32
    + Magister 24 (4 pts) = 105. **23.1 T** with the belt's 80% damage, **21.1 T** with 440 ES instead (damage line x1.095 vs +12% ES base).
  - Zero main-memory rolls: 2 INT mediums -> block instead of the memory roll (attack 103 / spell 105): 22.5 T (dmg belt) / 20.5 T (ES belt).
  - Margins need belt + ring >= 37 combined (T0 16-20 each); if they roll low, the crit dmg micro becomes the 8th block micro.
  - Why 22.5 T (from B1 33.1): new belt x1.027 · ring INT -> block x0.923 · orange crit lines x0.933 · kismets 152 -> 30 INT **x0.803** · Magister 4 pts x0.956. INT 556 -> 326.
  - Wand "+2 Physical Skill Level" -> INT (same Advanced prefix group; T1 64-90, T0 91-117, T0+ 135-152): in the block plan break-even ~90 INT; one wand T0 104 x1.027,
    117 x1.050; both wands x1.024 / x1.062 (the second barely pays). Current build (INT 556): a loss even at 117 (x0.977). The same line's tier upgrade +2 -> +3 is x1.08.

## Prophet vs another panel (Spell Ripple prism moved onto it), block plan, no LW (2026-10-27 19:07)
- Final T (block plan with the new belt, ring R frostbite T1 32, external block/res solved exactly; `scratchpad panels/pan.py + ext.py`):
  **Prophet 26.8 T** (no memory rolls; 27.3 with 2) · Arcanist 23.1 (needs 2 memory rolls) · Steel Vanguard with ele res nodes 22.8 (1 roll; ~24.6 if its
  "8% additional damage applied to Life" legendary counts as +8%) · Sentinel full block (42 attack / 60 spell from the tree) 22.8 (1 roll; its "+40% damage
  if Blocked recently" x3 would be ~x1.13 on bosses that hit you, not on the dummy) · Marksman 22.8 · Druid 21.5.
- Why Prophet: Frostbite is the biggest enemy-side multiplier (x3.2-3.5). Prophet's +44% frostbite effect (x1.17), +21 rating (to the 120 cap; without it
  rating 107 with ring T1), +10% additional vs Frozen, 4.5% cold pen, INT nodes, and 30 cold res (saves 3 kismet slots for block).
- Ring R frostbite T2 20 -> T1 32 on the current build: rating 116.4 -> 120 cap, x1.02 only. Without Prophet it's what keeps enemies Frozen.
- Re-run 19:17 (Vlad: SV's "8% additional damage applied to Life" = 8% additional; now parsed as add.damage). Zero memory rolls everywhere:
  **Prophet 26.8 T** vs Steel Vanguard 23.5 T (26 pts: ES 6, ele res 6, crit 6, aura effect 6, 736_176 + 8% legendary 2; the optimizer sends the other 4 to GoK)
  vs Sentinel full block 22.4 T (ring INT 60 kept, belt block, 4 res micros) vs Arcanist 23.1 (needs 2 memory rolls: no cold res).
  Node value on the block-plan tree: Prophet frostbite package 8 pts x1.390 (effect 44% x1.180, rating +12 to the cap x1.077, +10% vs Frozen x1.100),
  INT 4 pts x1.106, cold pen 3 pts x1.047, crit 6 pts x1.128 · SV aura effect 6 pts x1.171, 8% legendary path 2 pts x1.090, crit x1.128, ele res x1.000.
  Sentinel's 21 block points cost x0.66 of tree damage; external block (fates, orange, ring) is cheaper per block point.
- Ring R frostbite in the panel runs was T1 32 everywhere: Prophet's rating nodes already trimmed to +12 (608_80 x1, 736_80 x2), the rest moved to INT/pen.
  Prophet / SV tree ratio by ring frostbite: 20 (now) x1.355 · T1 32 x1.19 (final 26.8 vs 23.5) · T0 42 x1.13 (Prophet frees ~2 more points; final ~x1.08-1.10).

## RE-RUN under the real pairing rule (left node maxed; Vlad 2026-10-27 19:28). Everything tree-based above this line is superseded.
- Validator and optimizer were wrong (left node only needed 1 point). Current trees.json passes the real rule; every plan tree failed it.
  `tools/tree_opt/opt3.py` = new search (pair moves, wider swaps). LW plan trees (plan_trees_{tank,damage}_{micro,medium}.json) are INVALID, redo when LW comes back.
- **Reshuffle now (Lich kept): x1.066, 36.1 -> 38.5 T** (`plan_trees_reshuffle_now.json`): GoK +18% damage 1->3; Magister +20% spell crit 1->3,
  Focus duration 480_176 3->0, Focus-on-Spell-Burst 1->0. (The x1.134 earlier was illegal.)
- B1 (Lich -> Warlock, Def + OTBT, block-plan gear incl. ring T1 frostbite): **Prophet 33.4 T tree-only -> block plan 22.2 T** (zero memory rolls; 22.6 with 2).
  Prophet now must run 608_80 3/3 -> 736_80 3/3 -> 864_80 for the +10% vs Frozen: 7 points, worth only x1.015 over the best other use of 7 points.
- **Steel Vanguard instead: 31.3 T tree-only -> 22.0 T** (`plan_trees_warlock_sv.json`; SV 28 pts: ES 6, ele res 6, crit 6, aura effect 6, 736_176 3/3 + 8% legendary;
  GoK 32). Within noise of Prophet; SV's 18% ele res covers lightning + cold with no res kismets.

## BLOCK PLAN — full run 2026-10-27 20:30 (`tools/tree_opt/blockplan.py` + `blockfit.py`; plan trees `plan_trees_block_lich_*.json`)
Spec (Vlad): Lich -> Warlock (Dirty Tricks), Pedigree Defensiveness + OTBT, Spell Ripple prism (3x3 centred, +2% comp per medium rank, eaten cell counts
as maxed for pairing) on any non-god panel, new Arcanist Girdle (20% CDR base + Gale, 2B/2A/2U over 3+3), block 100/100 from anything except boots,
res 60/60/60/40, ring R frostbite T1, belt/ring/fates divined, memory block NOT divined (28), kismets 9 micro + 2 medium (2 mediums reserved = blank),
ES nodes free, EHP = ES vs elemental hits (res x0.40, block 55% x0.45, Low Mana x0.82 = ES x6.78; now ES x2.5). Model ES pinned to the sheet (7.3k) with +129 flat.
- Search: all 22 non-god panels x every prism cell with >= 9 medium ranks in its 3x3 (tree DPS only, real pairing rule) -> then ES packages, then the exact external fit.
  Tree-only (max DPS, no ES nodes): **Lich (prism on 608_80, the +9% dmg micro) 40.9** · Prophet 37.3 · Arcanist 33.1 · Steel Vanguard 30.3 · Marksman 29.2 · Ranger 29.2 ·
  Elementalist 28.8 · Shadowdancer 27.5 · Druid 27.2 · Warrior 26.5 · Sentinel 26.5 · ... · Artisan 19.8. Prism on Magister (Bunch dead, x1.46 incl. its Focus) loses everywhere.
- **Lich stays and holds the prism; Prophet goes.** Lich keeps +1 all skills (Chromatic 40), the 3rd Mass Effect charge, +10% additional (sealed mana+life), 12.5% CDR,
  crit and all-stats nodes; OTBT comes from the Pedigree. Frozen holds at 107 rating with ring R T1 (T2 would be 95 = NOT Frozen: the T1 is mandatory).
  Lich also has the cheapest ES in the tree: 352_272 x3 + 480_272 legendary = +19% ES for 4 points.
- Frontier, Lich (final T after the fit, 2 memory rolls):
  | ES packages | tree pts | T | ES | EHP ele |
  | none (Lich 736_368 path 9%) | - | 33.7 | 3,981 | 27.0k (x1.5) |
  | + Lich 352_272/480_272 (19%) | 4 | 32.4 | 4,675 | 31.7k |
  | + Warlock 96/224_272 (27%) | 10 | 29.4 | 5,661 | 38.4k |
  | + Magister 96/224_464 (27%) | 16 | 26.9 | 6,647 | 45.0k (x2.5) |
  | + Lich 96/224_272 (27%) = **TANK** | 22 | **24.1** | 7,633 | **51.7k (x2.8)** |
  | + Magister 352_272 + 608_464 | 28 | 21.2 | 8,452 | 57.3k |
  Same policy on the other panels (W+X+M ES): Prophet 23.6 T / 44.8k · Steel Vanguard 20.4 / 44.8k · Arcanist 20.1 / 47.0k. Max-DPS policy: Prophet 30.7, Arcanist 27.5, SV 25.2.
- **TANK, one memory roll (recommended): 23.4 T (x0.65 vs 36.1), ES 7,633, EHP 51.7k ele / 20.7k phys / 23.3k DoT** (`plan_trees_block_lich_tank1.json`):
  - Trees (110): GoK 24 (crit 352_80 x3 + 480_80 x1, cast x6, +9% spell x3, +1 spell lvl, Focus dur/dmg x3, +1 Focus, area/proj x6; drops +9%/+18% dmg), Magister 28
    (crit x6, Focus dur x3, +5% crit dmg/Focus, +8 INT x3, +12% INT x1, +9% spell x3, Frail, ES 96/224_464 x6, spell block 352_464 x3 + 480_464; drops 480_176 Focus dur, Spell-Burst Focus),
    Warlock 24 (vs cursed 352/480_80 x6, curse effect x3, +8% additional vs cursed, ES x6, +9% dmg x3, +15% per ailment, crit 352_464 x3 + 480_464 x1),
    Lich 34 (crit x6, cast x3, +1 all skills, all stats x6, CDR x3 + legendary, ES 96/224_272 x6 + 352_272 x3 + 480_272, 736_368 x3, +10% additional; prism eats 608_80).
  - Belt: 20% CDR base + Gale | Adv +20% block, Adv +78 INT, Ult -18% dmg taken at Low Mana | Basic cold 35, Basic lightning 35, Ult Double 34 (only 7 counts).
  - Ring L: Advanced prefix 52 INT -> +20% Attack and Spell Block; everything else stays. Ring R frostbite T2 -> T1.
  - Memories: Discipline random "+41% Spell Crit Dmg" -> attack block 28; orange memory both 18% crit lines -> block (11.8 each, spell side); nothing else.
  - Kismets (11 free): 4 micros attack block (8), 1 medium spell block (15), 5 res micros (cold x2, lightning x1, erosion x2), 1 medium INT (30); the +14% crit dmg micro goes.
    Block: attack = belt 20 + ring 20 + roll 28 + 4 micros 32 = 100; spell = 40 + Magister 24 + orange 23.6 + medium 15 = 102.6.
    Res: fire 61 · cold 12 + 35 + 14 · lightning 22 + 35 + 7 · erosion 27 + 14 = 41.
  - Sheet: INT 401, crit 74%/462%, cast 253, Chromatic 40, Focus 10, ME 3 charges, CDR 50, Boon margin 1.19, mana 97.1% sealed (Restrain 14.5 + prism 18).
  - Two rolls (Discipline + Progress 104% crit rating) instead of Magister block + orange: 24.1 T (`plan_trees_block_lich_tank.json`). Zero rolls: infeasible with 2 reserved mediums
    (needs a 3rd free medium or Prophet's cold res; Prophet zero-roll = 19.4 T).
- Knobs: belt Adv +26% Defense instead of +78 INT: 21.1 T / 58.1k (same trade both ways). Belt base +8% Aura Effect instead of 20% CDR (Lich's CDR keeps Boon at 1.03): x1.09 ->
  26.3 T; only if Gale isn't on the CDR belt yet. Lighter: L1+W+M only (26.9 T / 45.0k, `plan_trees_block_lich_mid.json`). Max DPS at block cap: 33.7 T / 27.0k (`_dps.json`).
- Ring L replaced by a priceless INT ring (2B/2A/2U): best = block 20 + 26% ele/erosion pen + 22% armor pen | lightning 35 + 156% crit + 78% crit dmg -> **39.6 T at 47k EHP**
  on the TANK tree (pen goes negative; loses the ring's 323 ES). Ring Ultimate pool also has "+1 Max Focus / +5% additional" and "+30% additional vs Frozen". Price unknown.
- **Belt base decided (Vlad 21:19): Has Hasten.** With Hasten on the belt the boots' "Has Hasten" suffix rolls to +60% Critical Strike Damage (Advanced suffix, T1 max;
  T0 61-78): TANK-1 23.4 -> **26.6 T (x1.136)**, T0 78% -> 27.5 T (x1.177). Aura-effect base was x1.089. After LW the belt keeps Hasten (x1.08 cast + 8% additional MS).
  Boon margin back to today's 1.03 (Lich CDR, no belt CDR). Gale not on any belt yet.
- Hasten alternatives (22:24): follower support Synchronized Haste (Hasten 4 s on cast, permanent like Periodic Burst) sits in SSR's pool; an SSR III with Periodic Burst +
  Deep Wounds + Synchronized Haste = 9k on the market (= aura belt possible: x1.09 -> ~1,000 FE/1%, no). Tempering a 3rd slot: 500 FE, 20% success, random support (~21),
  failure bricks the slot -> ~1%/try, ~50k expected. Other skills with it (Blink, Frigid Transmission, Speed Phantom, Star Stalker, Life Tonic, Lone Wolf melee "Swift Phantom")
  would replace Tidewell/Lightning Storm and lose Dirty Tricks ailments. Decision: Hasten belt; SSR only if one shows up under ~3k.
- Fallen Starlight (23:10): its "+1 Max Charges" = the 3rd Mass Effect charge = **x1.147** on the block layout (26.6 -> 23.2 T without it); a Starlight with Lich's
  "+10% additional (sealed mana + life)" instead is x1.10 and would need Boon CDR from elsewhere (CDR-24 belt route 22.4 T, x0.84; Hasten belt with CDR Ultimate
  suffix instead of Double 24.6 T, x0.93). Keep the current Starlight.
- **Speed Phantom -> Blizzard [Activation Medium: Elite, Well-Fought Battle, Blizzard: Freezing Point, Mass Effect]** (2026-10-28): debuff 10% additional cold taken
  x empower 2.04 x (1 + FP roll). FP 246% -> x1.707 = **x1.235 over Speed Phantom as measured** (9.4 / 6.8 = x1.382; the model's x1.485 overstates it 7%).
  Ice Bond (lv34, 27.5% vs Frostbitten x 2.04) = x1.56; Blizzard beats it above FP ~175%. Read: "+X% additional Empower Effect" multiplies the empower effect (TLI "additional").
  Elite-only (Activation Medium: Elite). Triggers cost no mana [Vlad].
- ~~Domain Expansion may be dead~~ - it works (x1.377 measured). **Precise Weapon Amp in DE's slot = +12.3% measured (8.2 vs 7.3), model +7.2%: swap it.**
- **Real DPS (2026-10-28 11:40, dummy_scale 1.0): 54.1 T full build; ~61 T with Precise WA in DE's slot** (measured ratio; model 58.0). Max hit 2.0 T, cap not binding.
  Blizzard is 1 stack (x1.733 measured). Plan T numbers above were at dummy 0.767: multiply them by 1.30 for absolute T (ratios unchanged).

## Chromatic supports (2026-10-28 12:05, current build, model at dummy 0.851)
- Now: Activation Medium: Tangle T1 11% / Overload / Condensed Cold / Multiple Projectiles / Target Projection = 54.3 T full.
- Overload vs Manifold in its slot: Overload x1.079 (keep). MP vs Lightchaser: MP x1.27 (keep; MP x1.49 measured 10-25 vs Lightchaser x1.17).
- **Medium T0 (21-25%)**: x1.108 at 23%; T1 max 15% x1.036.
- ~~Spell Tangle alone in the medium's slot (x1.166 on paper)~~ - scrapped: tangles last 8.9 s, so holding 4 needs a cast every ~2.2 s while bossing; each drop is -22%.
  Spell Tangle + Manifold (one cast per ~5 s, all 4 drop together if late) = x1.080 vs now. **A T0 medium beats it (x1.108) with no recasts.**
- INT is worth ~7% less per point without Lightchaser (0.5%/pt attribute scaling instead of 0.75%) -> the block plan's INT losses shrink; re-run it on these supports.

## Hero trait comparison (2026-10-28 12:40, his gear with the trait swapped; core L4, others L3 unless noted)
- **Thea 1 Wisdom of The Gods x7.50** (engine, trait off = 7.2 T): Wisdom x1.88 x Reincarnation x1.80 x Farewell x1.96 (all quad: 97% before it) x Agility x1.13
  (4 stacks: +2% additional each = x1.08, and +4% cast each: 240 -> 256% cast = x1.047). Boon alone x6.63; if a Gemma gets 4 Agility elsewhere, Thea's edge over
  Gemma 3 is x1.66 instead of x1.87. Purity's 2nd stack alone x2.23. Tidewell's +20 double x1.116 (it's all quad). All L5: x9.84 (71 T).
- Gemma 2 Frostbitten Heart (FH4 / Deepfreeze 3 / Dance 3 / Blooming 3, exact tlidb values) **x3.62 (26 T)**: Cold Pulse +38% x1.38, Deepfreeze +10% x1.10,
  frostbite 116 -> 171 rating at 160% effect (Deepfreeze L3: cap 200, +55%) x1.61, Dance of Frost 4 x 12% x1.48. Frigid Infusion instead of Blooming x3.66.
  Rating stacked to 200 x4.11 (30 T). All L5 x5.19 (38 T). Frostbite is already x3.38 on his sheet, so the frostbite lines only add x1.6.
- Gemma 1 Ice-Fire Fusion (Vlad: Gemma 1, not 3), every fire line read as cold: Fusion 4 / Embrace 3 / Restless 3 / Bone-piercing 3 **x2.96 (21 T)**: Rampage +30% x1.30 (7.7 s vs
  5.9 s CD -> permanent), Embrace both lines x1.35, Restless 18% pen x1.19, Bone-piercing "42% of cold as extra cold" x1.42. All L5 x3.82 (28 T).
  (As written, fire on a cold sheet: x1.76.) Read: Gemma buffs at full uptime, her additional-cold lines multiply.
- **Gemma 3 Flame of Pleasure** (FoP 4 / Groaning Echo 3 / Infernal Damnation 3 / Dress Licker 3, fire read as cold) **x4.01 sustained (29 T)**:
  Purgatory +68% x Dress Licker +40% damage taken (enemy-side, multiply) x2.35, Dress Licker +30% fire -> cold x1.30, Infernal Damnation +8%/s ramp over a
  10 s Purgatory (6.5 s x1.54 duration; CD 6.2 s, 2 charges, ~0.5 s auto-cast gap) avg x1.36 / peak x1.72. Dummy best second x5.26 (38 T): the ramp flatters pulls.
  Fire as written x3.10; if Purgatory ignores skill duration x3.54. All L5 x4.93 (peak x6.52). Boss must stay inside Purgatory (~10 m with +70% area).
- Hero memory upgrades: Predicted Reincarnation L3 -> L5 **x1.167**, Wisdom L4 -> L5 x1.085, Farewell L3 -> L5 x1.036 (quad caps at 200%), Purity L5 x1.00 (margin already >= 1).
- **I Am Truth (+4 all / +99 STR / +40% duration) on his sheet: x1.85 burst, x2.47 sustained** (2026-10-28 14:50). +4 all skills x1.64 (Chromatic L36 -> 40 x1.36,
  the rest is auras / Aim / SOU / Biting Cold / Blizzard / supports x1.205). 99 STR x1.12. 40% duration x1.00 on the dummy, **x1.34 sustained**: without it the Boon
  margin is 0.77 and the 2nd stack is up 54% (sustained = u + (1-u) x 0.448, u = 2 x margin - 1). The CDR roll (40%) holds it too (margin 1.01).
  Without the 40%: Thea trait x5.6 sustained vs Gemma 3 x3.7 (Purgatory 7.4 s). Replacing it: belt Ultimate +31% duration margin 0.97; + Purity L5 1.10; Purity L5 alone 0.90.

## 2026-10-29 21:00 — Projectile Penetration support (proximity-shield mobs in Machines)
No ignore for monster shield bubbles exists (scanned every tlidb page: legendaries, prisms, kismets, talents, slates, memories,
pacts, supports, traits). Cheap mitigation: **Projectile Penetration** support (free, lv20) on Chromatic Shot in place of Target
Projection: at support level 29 it is +4 Horizontal Projectile Penetrations and +19.5% additional. CORRECTION 20:45: TP is x1.277
measured (x1.47 on paper), so the swap is x0.936 (-6%; -19% by the text), not +2.5% - clear kit only, and only if the test shows
penetrating projectiles keep their damage after crossing a shield. Overload stays
(swapping it instead is x0.868). "Always Penetrate" exists only skill-specifically (Burning Shot Noble, Frost Spike Origin,
Clockwork Core/Stasis Vault); other +2 sources are Marksman's Legendary Medium, Sweeping Fury prism/slate, Bow/Crossbow/Musket affix.
Untested: whether a projectile that crossed a shield keeps 1 damage after penetrating.
