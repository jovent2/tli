# Crafting and costs (as observed by Vlad, SS14)

Prices drift; ask Vlad for current ones before a big pricing pass. Last update: 2026-10-26.

## How a craft works [Vlad]
- You roll **one** mod at a time and choose to keep the old or the new one. Nothing can roll worse than what you have.
- Affix groups: Basic / Advanced / Ultimate, on both prefix and suffix. A Priceless item has 2 ultimate, 2 advanced, 2 basic (3 prefix + 3 suffix).
- **Tier upgrade**: upgrades one affix by a tier; if it's at min T1 the upgrade is forced into T0 range. 30% success.
- "Truth is divine" rolls everything (all affixes) — not used for targeted crafting.
- Divinity slate purple (brand) lines can't become yellow (fixed) lines.
- tlidb lists a weight (`Wt`) per affix tier on the slot pages; how embers narrow the pool is not yet understood, so use Vlad's observed odds below.

## Costs [Vlad]
| Action | Cost | Odds |
|---|---|---|
| Basic mod roll | 10 embers + 1 FE (ember 0.22 FE) = 3.2 FE | ~1% T1 |
| Advanced mod roll | 10 embers (0.37 FE) + 3 FE = 6.7 FE | ~3.33% T1 |
| Ultimate mod roll (e.g. Tangle) | 30 FE + 1 ultimate ember (28 FE) = 58 FE | ~5% T1 |
| Tier upgrade (wand prefix, 2026-10-25) | 300 embers × 0.22 + 30 FE + 1 sacred fossil (12 FE) = 108 FE | 30% |
| Tier upgrade (skill-level / crit lines) | 90 FE + 300 embers × 0.37 + 3 fossils × 12 = 237 FE | 30% |

Expected cost to hit = cost / odds. Price per 1% = expected cost / (gain − 1) × 100.

## Big purchases seen
- Nether King slate with "+10% effect for non-legendary slates on the line" brand: ~4,000–4,500 FE.
- Pantheon's Elegy belt ~13,000 FE, + ~2,500 FE to put Gale on it.
- Slate +1 spell line: ~3% odds per roll.

## Divinity slates [Vlad + tlidb Brand Divinity Slate help]
- A base slate (e.g. GoK's Divinity with fixed +1 Spell Skill Level and +8% additional spell) ~300 FE. It drops with 1-3 Divinity Slots: Magic (blue) micro only, Rare (purple) up to medium, Legendary (gold/orange) up to legendary medium.
- **Inscribe** adds a micro, then upgrades micro -> medium -> legendary medium. Branding to full rare (mediums) costs ~0.
- **Medium -> legendary**: 2 Transcendence Wedge (Legendary) = ~14 FE. The legendary is random from the slate god's pool:
  GoK slate = Goddess of Knowledge + Magister + Prophet + Arcanist + Elementalist legendary mediums (36 nodes in tlidb; Vlad sees 2.96% per node ~ 1/34). ~75% read on the exact pool.
- **Divinity Pact - <Panel>** forces the branded node to come from that panel (GoK 5 legendaries, Magister 10, Prophet 7, Arcanist 6, Elementalist 8). Pacts exist for all 30 panels; which ones a GoK slate accepts is unconfirmed.
- **Overwrite** re-rolls micro/medium nodes. **Legendary nodes and New God nodes can't be overwritten.**
- **Restore** (Unifying Wedge, ~16 FE each) wipes ALL brands. Wedges per restore escalate 1, 1, 2, 4, 8, 16 — nobody restores at 16.
- Branded slates (and restored ones) become untradeable.
- Restores are the scarce resource: 1 + 6 tries per slate. A legendary miss in a slot can only be undone by a restore, which also wipes the hits in the other slots, so brand the slot that sets the floor first (e.g. a Focus node), and overwrite purple mediums last.
- A brand never rolls a node already on the slate (the pool excludes fixed and branded nodes; 34 left on a 2-fixed slate = 2.96%). Pact panels are equal odds. Overwriting medium/purple brands is free.
- Plan crafts with `tools/slate_plan.py` (exact keep/restore decision model, naked or pact per roll). Rule of thumb: buy the base with the nodes whose pacts are expensive (GoK +1 Spell, Elementalist +1 Cold) and roll the ones whose pact is cheap and has 2 good nodes in its panel (Arcanist: Focus + 8% additional).
- Divinity Pacts come from Divinity Pact Fragments (recycling slates), exchanged at the Heart of Rapacity [tlidb]; market price per pact: ask Vlad.
- Max Active Divinity 1: the same node on two divinity slates only counts once (e.g. GoK's "+1 to Max Focus" is already GoK #1's fixed node; Arcanist's "+1 Max Focus / regen 0.4% mana" is a different node and stacks).

## TOWER Sequence [tlidb TOWER_Sequence help]
- R&D on non-Legendary weapons (and shields). **One sequence per weapon**; it doesn't replace base affixes. Re-roll until you hit the target.
- Basic R&D (Base Mod, pick 3 chips) -> Intermediate sequences only. In-Depth R&D (Expansion Mod - Warlock for wands, pick 4 chips) -> Advanced.
  The picked chip colours (any order) must match a sequence's colour code (e.g. Overload 5|5|6|6), else the R&D fails. Mods aren't refunded if interrupted.
- Wand Intermediate: 8% additional Spell (1|2|6) · 16% Cast Speed (3|6|7) · +55 Spell Crit Rating (1|4|7) · 8% All Stats (1|2|3) · 6% ARP (2|3|4) ·
  8% Cold/Fire/Lightning/Erosion pen (cold 4|5|6) · 10% additional damage on Crit (1|2|5).
- Wand Advanced: Lv20 Overload (5|5|6|6) · Lv25 Control Spell (2|2|2|4) · +35% additional dmg / -10% additional cast (4|4|5|6) ·
  +1 Focus +1 Agility -1 Tenacity (2|3|5|6) · +120% Spell Amp aura / -20% its compensation (3|3|6|7) · +25% Spell Burst hit (1|3|5|7) ·
  200-220 cold at 800 INT (1|1|1|5) · True-damage explode (1|4|5|7).
- In-Depth R&D [Vlad 2026-10-27]: **640 FE per try**. Chips are numbers 1-7; 4 picks, the 1st from 4 offered, then 2, 2, 2 (you don't see later offers).
- Odds with optimal picks (`tools/tower_rnd.py`; iid offers / no repeats within an offer): Overload 3.7% / 5.3% · Control Spell 2.8% / 4.2% ·
  +35% 6.2% / 8.6% · Spell Amp 6.2% / 8.6% · Focus/Agility 8.5% / 10.7% · any useful (Overload/Control/+35%/Focus) 12.9% / 16.0%.
- Pick rule for "any useful": 1st 5 or 6 (else 2 > 4 > 3, never 1/7); then the other of 5/6 (else 4); then 5 or 6 (else 4, else 2/3); last one completes.
- Unknown: whether a failed R&D keeps the old sequence (assumed yes), whether a success can be declined, Basic R&D cost/pick structure.
