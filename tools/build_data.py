#!/usr/bin/env python3
"""Build the structured, searchable dataset in data/ from the crawled pages (data/pages/*.json).

Outputs
  data/index.json            every page: key, name, categories, summary
  data/search.jsonl          one record per page AND per list entry / table row, with full text
  data/catalog/<Page>.json   every list card of every category page (entries / table rows), verbatim
  data/affixes/<Slot>.json   craft pools per gear slot: prefix/suffix rows with tier, range, level, weight, group;
                             base affixes, corrosion base, base items
  data/legendaries.json      every legendary: slot, base, level, season, base + corroded lines, drop source
  data/talents.json          every talent panel: cores and nodes with column/row, points, ranks, pairing edges
  data/skills.json           every skill: kind, tags, description, stats, per-level table
  data/heroes.json           heroes and their trait pages
  data/glossary.json         tlidb hyperlink definitions (name -> definition)
  data/INDEX.md              human-readable table of contents with counts
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "data" / "pages"
OUT = ROOT / "data"

CATEGORY_PAGES = """Hero Talent Ethereal_Prism Pactspirit Destiny Inventory Legendary_Gear Follower Active_Skill
Support_Skill Passive_Skill Activation_Medium_Skill Magnificent_Support_Skill Noble_Support_Skill
Modularization_Skill Tartarus_Skill Origin_Tartarus_Skill Craft Corrosion Blending_Rituals TOWER_Sequence
Graft Memory_Revival Nether_Kings_Divinity Netherrealm Confusion_Card_Library Void_Chart Compass Probe
Season_Compass Path_of_the_Brave Tip Path_of_Progression Help Divinity_Slate Hero_Memories""".split()

SKILL_PAGES = {
    "Active_Skill": "Active", "Support_Skill": "Support", "Passive_Skill": "Passive",
    "Activation_Medium_Skill": "Activation Medium", "Magnificent_Support_Skill": "Magnificent Support",
    "Noble_Support_Skill": "Noble Support", "Modularization_Skill": "Modularization",
    "Tartarus_Skill": "Tartarus", "Origin_Tartarus_Skill": "Origin Tartarus",
}


def load_pages():
    pages = {}
    for p in PAGES.glob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        pages[d["key"]] = d
    return pages


def clean_header(h):
    return re.sub(r"\s*/\s*\d+\s*$", "", h or "").strip() or None


def keyify(name):
    return name.replace("'", "").replace("’", "").replace(" ", "_")


def display_name(d):
    k = d["key"]
    want = k.lower()
    for c in d["cards"][:3]:
        for line in c.get("text", [])[:6]:
            if keyify(line).lower() == want or keyify(line).lower().replace(":", "") == want:
                return line
        for e in c.get("entries", [])[:50]:
            if e.get("key") == k and e.get("name"):
                return e["name"]
    return k.replace("_", " ")


def page_lines(d):
    out = []
    for c in d["cards"]:
        h = c.get("header")
        if h:
            out.append(f"## {h}")
        out += c.get("text", [])
        for e in c.get("entries", []):
            nm = e.get("name")
            out.append((nm + ": " if nm else "") + " · ".join(e.get("lines", [])))
        for t in c.get("tables", []):
            for r in t["rows"]:
                out.append(" | ".join(r["cells"]))
    return out


def summary_of(d, n=6):
    lines = []
    for c in d["cards"][:3]:
        for l in c.get("text", []):
            if l in ("SS14Season",) or re.fullmatch(r"SS\d+Season", l):
                continue
            lines.append(l)
        for e in c.get("entries", [])[:3]:
            lines.append((e.get("name", "") + ": " + " · ".join(e.get("lines", [])[:3])).strip(": "))
        if len(lines) >= n:
            break
    return lines[:n]


# --------------------------------------------------------------------------- categories

def categorize(pages):
    cats = defaultdict(set)
    for src in CATEGORY_PAGES:
        d = pages.get(src)
        if not d:
            continue
        for c in d["cards"]:
            h = clean_header(c.get("header")) or c.get("tab") or src
            label = f"{src.replace('_', ' ')} > {h}" if h != src.replace("_", " ") else src.replace("_", " ")
            for e in c.get("entries", []):
                if e.get("key"):
                    cats[e["key"]].add(label)
            for t in c.get("tables", []):
                for r in t["rows"]:
                    for k in r.get("links", []):
                        cats[k].add(label)
    # gear slot pages: linked from Inventory/Craft "Gear" cards and containing a "<X> Craft" tab
    for k, d in pages.items():
        if any((c.get("tab") or "").endswith("Craft") and c.get("tables") for c in d["cards"]):
            cats[k].add("Gear slot")
    return cats


# --------------------------------------------------------------------------- catalog (verbatim lists)

def build_catalog(pages):
    out_dir = OUT / "catalog"
    out_dir.mkdir(exist_ok=True)
    counts = {}
    for src in CATEGORY_PAGES:
        d = pages.get(src)
        if not d:
            continue
        cards = []
        for c in d["cards"]:
            item = {"card": clean_header(c.get("header")) or c.get("tab"), "tab": c.get("tab")}
            if c.get("entries"):
                item["entries"] = c["entries"]
            if c.get("tables"):
                item["tables"] = c["tables"]
            if c.get("text"):
                item["text"] = c["text"]
            cards.append(item)
        (out_dir / f"{src}.json").write_text(json.dumps({"page": src, "cards": cards}, ensure_ascii=False, indent=1),
                                             encoding="utf-8")
        cs = {}
        for cc in cards:
            n = len(cc.get("entries", [])) + sum(len(t["rows"]) for t in cc.get("tables", []))
            if n:
                cs[cc["card"]] = cs.get(cc["card"], 0) + n
        counts[src] = cs
    return counts


# --------------------------------------------------------------------------- affix pools

ROW_RX = re.compile(r"^(?P<tier>\d\+?)$")


def build_affixes(pages):
    out_dir = OUT / "affixes"
    out_dir.mkdir(exist_ok=True)
    base_to_slot = {}
    slots = {}
    for k, d in pages.items():
        craft = [c for c in d["cards"] if (c.get("tab") or "").endswith("Craft")]
        tables = [t for c in craft for t in c.get("tables", []) if t.get("header") and "Modifier" in t["header"]]
        if not tables:
            continue
        def rows(t):
            hdr = t["header"]
            out = []
            for r in t["rows"]:
                cells = dict(zip(hdr, r["cells"]))
                if cells.get("T") in (None, "", "T") or cells.get("Modifier") in (None, "Modifier"):
                    continue
                lvl = cells.get("Lv")
                wt = cells.get("Wt")
                out.append({"tier": cells.get("T"), "modifier": cells.get("Modifier"),
                            "level": int(lvl) if lvl and lvl.isdigit() else lvl,
                            "weight": int(wt) if wt and wt.isdigit() else wt,
                            "group": cells.get("Library")})
            return out
        pref = rows(tables[0]) if len(tables) > 0 else []
        suf = rows(tables[1]) if len(tables) > 1 else []
        base_aff, corr = [], []
        for c in craft:
            t = c.get("text") or []
            if t and t[0] == "Base Affix":
                base_aff = t[1:]
            elif t and t[0] == "Corrosion Base":
                corr = t[1:]
        bases, legs, legs_c = [], [], []
        for c in d["cards"]:
            h = clean_header(c.get("header")) or ""
            if h == "Legendary Gear":
                legs = [e.get("name") for e in c.get("entries", [])]
            elif h == "Legendary Gear Corroded":
                legs_c = [e.get("name") for e in c.get("entries", [])]
            elif c.get("entries") and h and h.replace(" ", "_") == k:
                bases = [{"name": e.get("name"), "key": e.get("key"), "lines": e.get("lines")} for e in c["entries"]]
                for b in bases:
                    if b["name"]:
                        base_to_slot[b["name"]] = k
        slot = {"slot": k, "name": display_name(d), "prefix": pref, "suffix": suf, "base_affixes": base_aff,
                "corrosion_base": corr, "base_items": bases, "legendaries": sorted(set(n for n in legs if n))}
        # group affixes by modifier family for quick reading: strip numbers
        slots[k] = slot
        (out_dir / f"{k}.json").write_text(json.dumps(slot, ensure_ascii=False, indent=1), encoding="utf-8")
    return slots, base_to_slot


# --------------------------------------------------------------------------- legendaries

def parse_item_page(d):
    first = d["cards"][0] if d["cards"] else {}
    lines = list(first.get("text", []))
    season = next((l for l in lines if re.fullmatch(r"SS\d+Season", l)), None)
    lines = [l for l in lines if l != season]
    name = lines[0] if lines else display_name(d)
    rest = lines[1:]
    req = None
    if rest and rest[0].startswith("Require lv"):
        req = rest[0].replace("Require lv", "").strip()
        rest = rest[1:]
    item = {"key": d["key"], "name": name, "season": season, "require_level": req, "lines": rest}
    for c in d["cards"][1:]:
        h = c.get("header")
        if h == "Corroded":
            item["corroded"] = c.get("text", [])
        elif h == "Info":
            for l in c.get("text", []):
                if ":" in l:
                    a, b = l.split(":", 1)
                    item[a.strip().lower().replace(" ", "_")] = b.strip()
        elif h == "Drop Source":
            item["drop_source"] = c.get("text", []) + [e.get("name") for e in c.get("entries", []) if e.get("name")]
        elif h:
            item.setdefault("other", {})[h] = c.get("text") or [
                (e.get("name") or "") + ": " + " · ".join(e.get("lines", [])) for e in c.get("entries", [])]
    return item


def build_legendaries(pages, cats, base_to_slot):
    items = []
    for k, d in pages.items():
        if not any("Legendary Gear" in c for c in cats.get(k, ())):
            continue
        if not d["cards"]:
            continue
        it = parse_item_page(d)
        it["slot"] = base_to_slot.get(it.get("base"))
        items.append(it)
    items.sort(key=lambda x: (x.get("slot") or "~", x["name"]))
    (OUT / "legendaries.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    return items


# --------------------------------------------------------------------------- talents

def build_talents(pages, cats):
    panels = []
    prof = pages.get("Talent")
    prof_keys = []
    if prof:
        for c in prof["cards"]:
            if clean_header(c.get("header")) == "Profession":
                prof_keys = [(e.get("key"), e.get("lines", [])) for e in c.get("entries", []) if e.get("key")]
    for k, meta in prof_keys:
        d = pages.get(k)
        if not d:
            continue
        nodes = []
        cores = []
        for c in d["cards"]:
            for e in c.get("entries", []):
                lines = e.get("lines", [])
                if not lines:
                    continue
                head = [x.strip() for x in lines[0].split("|")]
                rec = {"name": head[0], "lines": lines[1:]}
                for tok in head[1:]:
                    m = re.fullmatch(r"(\d+)pts", tok)
                    if m:
                        rec["points"] = int(m.group(1))
                    m = re.fullmatch(r"\d+/(\d+)", tok)
                    if m:
                        rec["max_rank"] = int(m.group(1))
                src = next((l for l in rec["lines"] if l.startswith("Source:")), None)
                if src:
                    rec["source"] = src.replace("Source:", "").strip()
                    rec["lines"] = [l for l in rec["lines"] if l != src]
                if rec.get("max_rank") == 1 and rec["name"] not in ("Legendary Medium Talent", "Medium Talent", "Micro Talent") \
                        and rec.get("points") in (12, 24):
                    rec["type"] = "Core"
                    cores.append(rec)
                else:
                    rec["type"] = rec["name"]
                    nodes.append(rec)
        # layout from the svg graph
        layout = []
        if d.get("svg"):
            g = d["svg"][0]
            pos = []
            for n in g["nodes"]:
                if "x" not in n:
                    continue
                cx, cy = n["x"] + n.get("width", 64) / 2, n["y"] + n.get("height", 64) / 2
                rec = {"cx": cx, "cy": cy, "name": n.get("name"), "lines": n.get("lines", []),
                       "icon": n.get("icon")}
                if n.get("alt"):
                    rec["alt"] = n["alt"]
                pos.append(rec)
            xs = sorted({p["cx"] for p in pos if p["cy"] > 0})
            ys = sorted({p["cy"] for p in pos if p["cy"] > 0})
            colpts = [0, 3, 6, 9, 12, 15, 18]
            def near(px, py):
                best, bd = None, 1e9
                for i, p in enumerate(pos):
                    dd = (p["cx"] - px) ** 2 + (p["cy"] - py) ** 2
                    if dd < bd:
                        best, bd = i, dd
                return best
            links = defaultdict(set)
            for x1, y1, x2, y2 in g["edges"]:
                if abs(x1 - x2) > 200 or abs(y1 - y2) > 200 or min(y1, y2) < 40:  # skip the column axis line
                    continue
                a, b = near(x1, y1), near(x2, y2)
                if a is not None and b is not None and a != b:
                    links[a].add(b)
                    links[b].add(a)
            for i, p in enumerate(pos):
                if p["cy"] <= 0:
                    p["slot"] = "core"
                else:
                    ci = xs.index(p["cx"]) if p["cx"] in xs else None
                    p["column_points"] = colpts[ci] if ci is not None and ci < len(colpts) else None
                    p["row"] = ys.index(p["cy"]) + 1
                p["id"] = f"{int(p['cx'])}_{int(p['cy'])}"
                p["connects"] = sorted(f"{int(pos[j]['cx'])}_{int(pos[j]['cy'])}" for j in links[i])
                # max rank from the node list (match on effect text)
                for n in nodes + cores:
                    if n["lines"] and p["lines"] and n["lines"][0] == p["lines"][0]:
                        p["max_rank"] = n.get("max_rank")
                        break
                layout.append(p)
        panels.append({"key": k, "name": display_name(d), "info": meta, "cores": cores, "nodes": nodes,
                       "layout": layout})
    (OUT / "talents.json").write_text(json.dumps(panels, ensure_ascii=False, indent=1), encoding="utf-8")
    return panels


# --------------------------------------------------------------------------- skills

def build_skills(pages):
    skills = {}
    for src, kind in SKILL_PAGES.items():
        d = pages.get(src)
        if not d:
            continue
        for c in d["cards"]:
            h = clean_header(c.get("header")) or ""
            for e in c.get("entries", []):
                k = e.get("key")
                if not k:
                    continue
                s = skills.setdefault(k, {"key": k, "name": e.get("name"), "kind": kind})
                if h.endswith("Tag"):
                    s["tags"] = [t.strip() for t in ", ".join(e.get("lines", [])).split(",") if t.strip()]
                else:
                    s["description"] = e.get("lines", [])
    for k, s in skills.items():
        d = pages.get(k)
        if not d:
            continue
        first = d["cards"][0].get("text", []) if d["cards"] else []
        s["page_header"] = [l for l in first if not re.fullmatch(r"SS\d+Season", l)]
        for c in d["cards"]:
            h = clean_header(c.get("header")) or ""
            if h == "Progression":
                for t in c.get("tables", []):
                    s["levels"] = {r["cells"][0]: r["cells"][1:] for r in t["rows"] if r["cells"]}
            elif h == "Info":
                s["info"] = c.get("text", [])
            elif h and h not in ("Progression",):
                s.setdefault("other", {})[h] = c.get("text") or [
                    (e.get("name") or "") + ": " + " · ".join(e.get("lines", [])) for e in c.get("entries", [])] or [
                    " | ".join(r["cells"]) for t in c.get("tables", []) for r in t["rows"]]
    out = sorted(skills.values(), key=lambda s: (s["kind"], s.get("name") or s["key"]))
    (OUT / "skills.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


# --------------------------------------------------------------------------- heroes, glossary

def build_heroes(pages):
    heroes = []
    hp = pages.get("Hero")
    if not hp:
        return heroes
    # Hero list entries are "Hero | Trait" and link straight to the trait page
    for c in hp["cards"]:
        for e in c.get("entries", []):
            k = e.get("key")
            if not k:
                continue
            nm = e.get("name") or k
            hero, _, trait = nm.partition(" | ")
            rec = {"hero": hero.strip(), "trait": trait.strip() or nm, "key": k, "blurb": e.get("lines", [])}
            d = pages.get(k)
            if d:
                rec["cards"] = [x for x in d["cards"] if not (clean_header(x.get("header")) or "").startswith(
                    ("Skill Shop", "Outfit"))]
            heroes.append(rec)
    (OUT / "heroes.json").write_text(json.dumps(heroes, ensure_ascii=False, indent=1), encoding="utf-8")
    return heroes


def build_glossary(pages):
    g = {}
    tip = pages.get("Tip")
    if tip:
        for c in tip["cards"]:
            if clean_header(c.get("header")) == "Hyperlink":
                for t in c.get("tables", []):
                    for r in t["rows"]:
                        if len(r["cells"]) >= 2:
                            g.setdefault(r["cells"][0], []).append(r["cells"][1])
    (OUT / "glossary.json").write_text(json.dumps(g, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    return g


# --------------------------------------------------------------------------- index + search

def build_index(pages, cats):
    index = []
    with open(OUT / "search.jsonl", "w", encoding="utf-8") as f:
        for k in sorted(pages):
            d = pages[k]
            name = display_name(d)
            cs = sorted(cats.get(k, ()))
            index.append({"key": k, "name": name, "categories": cs, "summary": summary_of(d)})
            f.write(json.dumps({"id": k, "kind": "page", "key": k, "name": name, "categories": cs,
                                "text": page_lines(d)}, ensure_ascii=False) + "\n")
        for src in CATEGORY_PAGES:
            d = pages.get(src)
            if not d:
                continue
            for ci, c in enumerate(d["cards"]):
                h = clean_header(c.get("header")) or c.get("tab")
                for ei, e in enumerate(c.get("entries", [])):
                    f.write(json.dumps({"id": f"{src}#{ci}.{ei}", "kind": "entry", "source": src, "card": h,
                                        "key": e.get("key"), "name": e.get("name") or (e.get("lines") or [""])[0],
                                        "text": e.get("lines", [])}, ensure_ascii=False) + "\n")
                for ti, t in enumerate(c.get("tables", [])):
                    for ri, r in enumerate(t["rows"]):
                        f.write(json.dumps({"id": f"{src}#{ci}.t{ti}.{ri}", "kind": "row", "source": src, "card": h,
                                            "header": t.get("header"), "name": r["cells"][0] if r["cells"] else "",
                                            "text": [" | ".join(r["cells"])], "links": r.get("links")},
                                           ensure_ascii=False) + "\n")
    (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=0), encoding="utf-8")
    return index


def write_md(counts, slots, legs, panels, skills, heroes, gloss, index):
    L = ["# Data index", "",
         "Built by `tools/build_data.py` from the tlidb crawl (`tools/crawl.py`). Search with `tools/find.py`.", "",
         f"- Pages crawled: **{len(index)}**",
         f"- Gear slots with craft pools: **{len(slots)}** → `data/affixes/<Slot>.json`",
         f"- Legendaries: **{len(legs)}** → `data/legendaries.json`",
         f"- Talent panels: **{len(panels)}** → `data/talents.json`",
         f"- Skills: **{len(skills)}** → `data/skills.json`",
         f"- Hero traits: **{len(heroes)}** → `data/heroes.json`",
         f"- Glossary terms: **{len(gloss)}** → `data/glossary.json`",
         "- Every list page verbatim → `data/catalog/<Page>.json`",
         "- Full-text records (pages, list entries, table rows) → `data/search.jsonl`", "",
         "## Catalog pages", ""]
    for src, cs in counts.items():
        L.append(f"- **{src.replace('_', ' ')}** — " + ", ".join(f"{k} ({v})" for k, v in cs.items() if k))
    L += ["", "## Gear slots", ""]
    for k, s in sorted(slots.items()):
        L.append(f"- `{k}` — {len(s['prefix'])} prefix rows, {len(s['suffix'])} suffix rows, "
                 f"{len(s['base_items'])} bases, {len(s['legendaries'])} legendaries")
    L += ["", "## Talent panels", ""]
    for p in panels:
        L.append(f"- `{p['key']}` — {', '.join(c['name'] for c in p['cores'])}")
    (OUT / "INDEX.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    pages = load_pages()
    cats = categorize(pages)
    counts = build_catalog(pages)
    slots, base_to_slot = build_affixes(pages)
    legs = build_legendaries(pages, cats, base_to_slot)
    panels = build_talents(pages, cats)
    skills = build_skills(pages)
    heroes = build_heroes(pages)
    gloss = build_glossary(pages)
    index = build_index(pages, cats)
    write_md(counts, slots, legs, panels, skills, heroes, gloss, index)
    print(f"pages {len(pages)} | slots {len(slots)} | legendaries {len(legs)} | panels {len(panels)} | "
          f"skills {len(skills)} | heroes {len(heroes)} | glossary {len(gloss)}")


if __name__ == "__main__":
    main()
