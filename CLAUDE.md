# tli — Vlad's Torchlight: Infinite workspace

This repo is how Claude keeps everything about Vlad's TLI characters between sessions:
game data, verified mechanics, his current builds, test results and plans.
Every new session starts by reading this file, then the files listed under "Read first".

## Read first (every session)
1. `docs/mechanics.md` — the damage chain and every rule we have proven in game. Use it; don't re-derive.
2. The active character folder (right now `ss14/thea/`): `build.md` (current state), `plans.md`, the latest entries of `tests.md` and `history.md`.
3. `docs/tlidb.md` before touching tlidb, `docs/crafting.md` before pricing any craft.

## How to work with Vlad
- He wants the math done, not discussed. Price things as multipliers on HIS current sheet, give the number, then the decision.
- He gives in-game numbers; those are ground truth. tlidb is accurate too (check the level/rank you're reading — e.g. Wisdom of the Gods is 52% at L5 but he has L4 = 44%).
- Anything he names (item, node, skill, prism, slate) gets looked up on tlidb BEFORE commenting. Never guess an item's text.
- Be proactive: scan the pools (affixes, slates, prisms, legendaries, kismets) for things he hasn't considered.
- Direct, no hedging, no "in/out of water" style double numbers unless he asks. State a confidence when something is a read, not a proof. Disagree once, then drop it. Own mistakes in one line and fix them.
- Casual tone, he's an engineer (C++), plays a lot, knows the game better than tlidb does in places.

## Game data
- The whole of tlidb is already in `data/` (see `data/README.md`). Start every lookup with
  `python3 tools/find.py <words>` — it searches every page, list entry and table row.
- Structured sets for pricing: `data/affixes/<Slot>.json` (craft pools with tiers and weights),
  `data/legendaries.json`, `data/talents.json` (with node pairing), `data/skills.json`, `data/heroes.json`,
  `data/glossary.json`, `data/catalog/<Page>.json` (pacts, destinies, prisms, slates, memories, corrosion...).
- Proactive scans: when pricing a slot, walk its whole pool in `data/affixes/` through `tools/value.py`, not just
  the lines Vlad mentioned.
- Live page if something seems missing or outdated: `python3 tools/tlidb.py PAGE [--tables|--grep REGEX] --refresh`.
  The shell reaches tlidb.com directly. Do NOT use WebFetch for tlidb (it paraphrases, truncates and sometimes
  invents text). WebSearch with `allowed_domains: ["tlidb.com"]` is fine for finding a page name.
- Data is a snapshot; tlidb updates with patches. Re-crawl at the start of a new season (`data/README.md`).

## Keeping the repo current
- When Vlad changes gear/tree/slates/skills or reports stats: update `ss14/<char>/build.md` and add a dated line to `history.md`.
- When he reports a measurement: add it to `tests.md` with the config and what the model predicted.
- When a mechanic is proven (or disproven): update `docs/mechanics.md` and note the test that proved it.
- Commit with a short message describing the change. Small commits are fine.
- Personal info about Vlad does not go here (that lives in Claude's memory). Only game stuff.

## Layout
- `docs/` — mechanics, tlidb notes, crafting/costs.
- `tools/` — `tlidb.py` (raw page reader), `value.py` (marginal-value calculator).
- `data/` — scraped game data (JSON). `data/raw/` is the page cache, gitignored.
- `ss14/` — season 14 (Tartarus). `ss14/thea/` is the current character.
