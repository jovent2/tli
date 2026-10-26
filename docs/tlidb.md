# tlidb.com — how to read it

tlidb is accurate (when something looked wrong it was us reading the wrong level/rank).
The whole site is already crawled into `data/` — search there first with `tools/find.py`
(see `data/README.md`). Read live pages raw from the shell; never through WebFetch.

```
python3 tools/tlidb.py Gale                       # page text
python3 tools/tlidb.py Wand --tables              # affix tables as JSON lines
python3 tools/tlidb.py Israfels_Laws --grep Focus # matching lines with context
python3 tools/tlidb.py Wand --refresh             # bypass the cache (data/raw/)
```

## URL rules
- `https://tlidb.com/<Name>` with spaces → `_` and apostrophes dropped: `Israfel's Laws` → `Israfels_Laws`, `Pantheon's Elegy` → `Pantheons_Elegy`, `Goddess of Hunting's Dirge` → `Goddess_of_Huntings_Dirge`.
- Some pages live under a language prefix: `en/Tartarus_Season`, `en/Marksman`.
- Unsure of the name: WebSearch with `allowed_domains: ["tlidb.com"]`, then read the result with the tool.

## Page types seen so far
- **Item base / slot pages** (`Wand`, `Ring`, `Belt`, `INT_Boots`, ...): "<Slot> Craft" tables. Columns `T | Modifier | Lv | Wt | Library`: tier (0+, 0, 1, 2, ...), modifier text with ranges, item-level requirement, roll weight, and Basic / Advanced / Ultimate Affix. First table = prefixes, second = suffixes. Then a Base Affix list (Priceless bases) and the Corrosion Base pool. The page also lists that slot's legendaries.
- **Legendary item pages** (`Israfels_Laws`, `Malign_Embrace`): base and corroded affixes with ranges.
- **Talent panel pages** (`Magister`, `Prophet`, `Ranger`, ...): cores with point requirements, then every micro/medium/legendary node with its point column and max ranks. Node pairing (which micro leads to which medium) is NOT shown on tlidb; get it from Vlad's screenshots.
- **Skill pages** (`Target_Projection`, `Overload`): tags, mana multiplier, per-level table 1–40.
- **Mechanic pages** (`Frostbite`, `Armor`, `Critical_Strike`, `Double_Damage`, `Skill_Level`, `Block`, `Tangle`, `Proximity`): rule text and formulas.
- **Hero pages** (`Wisdom_of_The_Gods`): every trait node with L1–L5 values.
- **Hero memories** (`Hero_Memories`, `Memory_of_Origin`): base stats, fixed affixes, random affixes with tiers and weights.
- **Season pages** (`en/Tartarus_Season`, `Outlaw_Season`, ...): what each season added.
- **Slates / prisms** (`Divinity_Slate`, `Sparks_of_Moth_Fire`, `Unmatched_Valor`, `Replicate`).

## Gotchas
- The first ~60 lines of every page are site navigation. The page title appears right after the language list.
- Values like `+(13–14)%` are ranges; tier rows give each tier's range.
- tlidb labels everything "beta data" in the footer; ignore that line.
