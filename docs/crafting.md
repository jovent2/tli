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
- Pact pricing rule: one pact try = p(target) x gain(target). FE per 1% = (14 + pact + restore before the try) / (p x gain%). Random wedges only win when pacts cost more than ~2-3x the wedges (see ss14/thea/plans.md, new GoK slate).
- Divinity Pacts come from Divinity Pact Fragments (recycling slates), exchanged at the Heart of Rapacity [tlidb]; market price per pact: ask Vlad.
- Max Active Divinity 1: the same node on two divinity slates only counts once (e.g. GoK's "+1 to Max Focus" is already GoK #1's fixed node; Arcanist's "+1 Max Focus / regen 0.4% mana" is a different node and stacks).
