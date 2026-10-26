# data — the whole of tlidb, structured

Built from a full crawl of tlidb.com (English). See `INDEX.md` for counts and the list of every slot and panel.

## Look things up
```
python3 tools/find.py max focus                      # anything mentioning both words, ranked
python3 tools/find.py tangle --kind entry            # only list entries (talent nodes, destinies, slate nodes...)
python3 tools/find.py frostbite --cat "Legendary"    # restrict by category / source page
python3 tools/find.py --name "Israfel" --full        # by name, full text
python3 tools/find.py --page Wisdom_of_The_Gods      # one page, all text
python3 tools/find.py cold --regex "\+\d+ to Max Frostbite"
```

## Files
| File | What it is |
|---|---|
| `search.jsonl` | Every page, every list entry and every table row as one record with its full text. What `find.py` reads. |
| `index.json` | Every page: key, display name, categories (which list it came from), short summary. |
| `affixes/<Slot>.json` | Craft pools per gear slot (`Wand`, `Ring`, `INT_Boots`, ...): prefix and suffix rows with tier, modifier text/range, item level, roll weight, group (Basic/Advanced/Ultimate); Priceless base affixes; corrosion base pool; base items; slot legendaries. |
| `legendaries.json` | Every legendary: slot, base, required level, season, base lines, corroded lines, random-affix pools, drop source. |
| `talents.json` | All 32 talent panels: cores, nodes (type, points, max rank, effect), and the panel layout from tlidb's graph (`id` = `x_y` centre like `608_176`, column points, row, which nodes it connects to — micro→medium pairs). |
| `skills.json` | Every skill (active, support, passive, activation medium, magnificent, noble, modularization, tartarus): tags, description, page stats, per-level table. |
| `heroes.json` | Every hero trait page: trait nodes with L1–L5 text, Prophecy of Revelation talent swaps. |
| `glossary.json` | tlidb hyperlink definitions (term → definition), e.g. Frostbite, Gale, Enhanced Mark. |
| `catalog/<Page>.json` | Every category page verbatim: Pactspirit, Destiny (kismets), Ethereal Prism (+ prism affix pool), Divinity Slate, Nether King's Divinity, Hero Memories (all affix pools with weights), Corrosion, Graft, Memory Revival, Craft (all 2,526 affixes with source), Netherrealm, Compass, Void Chart, ... |
| `crawl_report.json` | Last crawl: pages, failures. |
| `pages/`, `raw/` | Parsed page dumps and HTML cache (gitignored; rebuild with the tools). |

## Rebuild
```
python3 tools/crawl.py --depth 2      # fetch (cached pages are skipped; add --refresh to re-download)
python3 tools/crawl.py --reparse      # re-parse cached HTML after a parser change
python3 tools/build_data.py           # rebuild everything in data/
```
