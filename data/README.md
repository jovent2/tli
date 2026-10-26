# data

Scraped tlidb data as JSON, one file per category. Not built yet — next step after the repo setup.

Planned files (each entry keeps its tlidb URL and the date it was scraped):
- `affixes/<slot>.json` — craft affix pools per slot: prefix/suffix, basic/advanced/ultimate, every tier with range, level and weight; Priceless base affixes; corrosion bases.
- `legendaries.json` — every legendary: slot, base, level, base and corroded affixes.
- `talents/<panel>.json` — every panel: cores, nodes with point column and ranks (pairing from screenshots where known).
- `slates.json` — slate types, fixed and brand node pools per god, Nether King mods.
- `prisms.json` — prisms, their core, random-affix pools.
- `memories.json` — hero memory base/fixed/random pools.
- `pacts.json` — pactspirits, pact pages, destinies (kismets).
- `skills/*.json` — active/support/passive skills with tags and level tables.
- `hero/<hero>.json` — trait trees with L1–L5 values.

`raw/` is the HTML cache from `tools/tlidb.py` (gitignored).
