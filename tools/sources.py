#!/usr/bin/env python3
"""Build the "where do I get X" index: every source of every stat, across every system.

  python3 tools/sources.py                 # writes data/sources.json and data/sources/<key>.md
  python3 tools/sources.py focus.max       # print the sources of one stat to the terminal

Systems covered: gear craft pools (with tiers/groups), Priceless base affixes, corrosion base pools,
legendaries (base and corroded), talent nodes and cores, Divinity slate nodes, Ethereal prism affixes,
destinies (kismets), hero memory affixes, Nether King nodes, pactspirits, graft affixes.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stats  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def cat(k):
    return json.loads((DATA / "catalog" / f"{k}.json").read_text(encoding="utf-8"))


def collect():
    src = defaultdict(list)   # key -> list of records

    def add(system, where, line, extra=None):
        for s in stats.parse(line):
            r = {"system": system, "where": where, "line": line, "value": s.value, "lo": s.lo, "hi": s.hi}
            if s.cond:
                r["cond"] = s.cond
            if extra:
                r.update(extra)
            src[s.key].append(r)

    # gear craft pools: one record per (slot, side, modifier family) with its tiers
    for f in sorted((DATA / "affixes").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for side in ("prefix", "suffix"):
            fam = defaultdict(list)
            for r in d[side]:
                fam[(stats.template(r["modifier"]), r["group"])].append(r)
            for (tmpl, group), rows in fam.items():
                best = rows[0]
                t1 = next((x for x in rows if x["tier"] == "1"), None)
                t0 = next((x for x in rows if x["tier"] == "0"), None)
                tiers = {x["tier"]: x["modifier"] for x in rows}
                for s in stats.parse((t1 or best)["modifier"]):
                    rec = {"system": "craft", "where": f"{d['slot']} {side} ({group})", "line": (t1 or best)["modifier"],
                           "value": s.value, "lo": s.lo, "hi": s.hi, "tiers": tiers,
                           "t0": t0["modifier"] if t0 else None, "weight_t1": t1["weight"] if t1 else None}
                    if s.cond:
                        rec["cond"] = s.cond
                    src[s.key].append(rec)
        for l in d.get("base_affixes", []):
            add("priceless base", d["slot"], l)
        for l in d.get("corrosion_base", []):
            add("corrosion base", d["slot"], l)

    for it in json.loads((DATA / "legendaries.json").read_text(encoding="utf-8")):
        w = f"{it['name']} ({it.get('slot') or it.get('base')})"
        for l in it.get("lines", []):
            add("legendary", w, l)
        for l in it.get("corroded", []):
            add("legendary corroded", w, l)
        for h, ls in (it.get("other") or {}).items():
            for l in ls:
                add("legendary random", f"{w} {h}", l)

    for p in json.loads((DATA / "talents.json").read_text(encoding="utf-8")):
        for c in p["cores"]:
            for l in c["lines"]:
                add("talent core", f"{p['name']}: {c['name']} ({c.get('points')} pts)", l)
        for n in p["layout"]:
            if n.get("slot") == "core":
                continue
            for l in n["lines"]:
                add("talent", f"{p['name']} {n['id']} {n['name']} (col {n.get('column_points')}, x{n.get('max_rank')})", l)
            for alt in n.get("alt", []):
                for l in alt["lines"]:
                    add("talent alt", f"{p['name']} {n['id']} [{alt.get('source')}]", l)

    for c in cat("Divinity_Slate")["cards"]:
        if c["card"] in ("Legendary Divinity Slate", "Non-Legendary Divinity Slate"):
            kind = "slate legendary node" if c["card"].startswith("Legendary") else "slate node"
            for e in c.get("entries", []):
                head = (e.get("lines") or [""])[0]
                for l in e.get("lines", [])[1:]:
                    add(kind, head, l)
        if c["card"] == "Legendary Gear":
            for e in c.get("entries", []):
                for l in e.get("lines", []):
                    add("legendary slate", e.get("name"), l)

    for c in cat("Ethereal_Prism")["cards"]:
        for t in c.get("tables", []):
            for r in t["rows"]:
                if len(r["cells"]) >= 3:
                    for part in r["cells"][0].split(" / "):
                        add("prism affix", f"{r['cells'][1]} ({r['cells'][2]})", part)
        for e in c.get("entries", []):
            for l in e.get("lines", []):
                add("prism", e.get("name"), l)

    for c in cat("Destiny")["cards"]:
        for e in c.get("entries", []):
            for l in e.get("lines", []):
                add("destiny (kismet)", e.get("name"), l)

    for c in cat("Hero_Memories")["cards"]:
        if c["card"] in ("Base Stats", "Fixed Affix", "Random Affix"):
            for t in c.get("tables", []):
                for r in t["rows"]:
                    tier, mod, lvl, wt, source = (r["cells"] + [""] * 5)[:5]
                    add(f"memory {c['card'].lower()}", f"{source} T{tier}", mod, {"weight": wt, "tier": tier})

    for c in cat("Nether_Kings_Divinity")["cards"]:
        for e in c.get("entries", []):
            head = (e.get("lines") or [""])[0]
            for l in e.get("lines", [])[1:]:
                add("nether king", head, l)

    for c in cat("Pactspirit")["cards"]:
        for e in c.get("entries", []):
            for l in e.get("lines", []):
                add("pactspirit", e.get("name"), l)

    for c in cat("Graft")["cards"]:
        for t in c.get("tables", []):
            for r in t["rows"]:
                if len(r["cells"]) >= 3:
                    add("graft affix", f"{r['cells'][1]} ({r['cells'][2]})", r["cells"][0])

    for c in cat("Corrosion")["cards"]:
        for t in c.get("tables", []):
            for r in t["rows"]:
                if len(r["cells"]) >= 3:
                    add("corrosion base", f"{r['cells'][2]} T{r['cells'][0]}", r["cells"][1])
    return src


def write(src):
    out = DATA / "sources"
    out.mkdir(exist_ok=True)
    for f in out.glob("*.md"):
        f.unlink()
    (DATA / "sources.json").write_text(json.dumps(src, ensure_ascii=False), encoding="utf-8")
    idx = ["# Where to get each stat", "",
           "Generated by `tools/sources.py` from `data/`. One file per stat key (see `tools/stats.py` for keys).",
           "Values are the T1 roll for craft affixes (T0 shown alongside), the listed range otherwise.", "",
           "| stat | sources | systems |", "|---|---|---|"]
    for key in sorted(src, key=lambda k: (k not in stats.THEA, k)):
        recs = src[key]
        systems = sorted({r["system"] for r in recs})
        mark = "**" if key in stats.THEA else ""
        idx.append(f"| {mark}[{key}]({key}.md){mark} | {len(recs)} | {', '.join(systems)} |")
        L = [f"# {key}", "", f"{len(recs)} sources. " + ("Thea scales with this." if key in stats.THEA else ""), ""]
        by = defaultdict(list)
        for r in recs:
            by[r["system"]].append(r)
        for system in sorted(by):
            rows = sorted(by[system], key=lambda r: -abs(r["value"]))
            L += [f"## {system} ({len(rows)})", ""]
            seen = set()
            for r in rows:
                sig = (r["where"], r["line"])
                if sig in seen:
                    continue
                seen.add(sig)
                extra = ""
                if r.get("t0"):
                    extra = f"  · T0: {r['t0']}"
                if r.get("cond"):
                    extra += f"  · *cond: {r['cond']}*"
                L.append(f"- **{r['where']}** — {r['line']}{extra}")
            L.append("")
        (out / f"{key}.md").write_text("\n".join(L), encoding="utf-8")
    (out / "README.md").write_text("\n".join(idx) + "\n", encoding="utf-8")


def main():
    src = collect()
    if len(sys.argv) > 1:
        key = sys.argv[1]
        for r in sorted(src.get(key, []), key=lambda r: (r["system"], -abs(r["value"]))):
            print(f"[{r['system']}] {r['where']}: {r['line']}" + (f"  (cond {r['cond']})" if r.get("cond") else ""))
        return
    write(src)
    tot = sum(len(v) for v in src.values())
    print(f"{len(src)} stat keys, {tot} sources; Thea-relevant keys: {sum(1 for k in src if k in stats.THEA)}")


if __name__ == "__main__":
    main()
