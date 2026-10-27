#!/usr/bin/env python3
"""Scan every pool against the current build and rank what would gain the most.

  python3 tools/scan.py            # writes ss14/thea/scan.md and prints the headline list
  python3 tools/scan.py --top 15

Sections: craft line swaps per item (same side + group, so the item stays legal), legendary swaps per slot,
kismets, unboosted / Judgment-line slate nodes, hero memory affixes, prism affixes, talent nodes per point.
Gains are DPS multipliers from tools/engine.py on the current build (belt on). Craft costs per T1 hit come
from docs/crafting.md (basic ~320 FE, advanced ~201 FE, ultimate ~1,160 FE).
Lines the parser can't price (mechanics) are listed under "needs hand pricing" — that's where hidden gems hide.
"""
import argparse
import copy
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine  # noqa: E402
import stats  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "ss14" / "thea" / "scan.md"

SLOT_POOL = {"helmet": "INT_Helmet", "chest": "INT_Chest_Armor", "gloves": "INT_Gloves", "boots": "INT_Boots",
             "belt": "Belt", "neck": "Necklace", "ring_l": "Ring", "ring_r": "Ring", "weapon_m": "Wand", "weapon_s": "Wand"}
CRAFTED = {"ring_l", "ring_r", "weapon_m", "weapon_s", "boots", "belt"}
COST_T1 = {"Basic Affix": 320, "Advanced Affix": 201, "Ultimate Affix": 1160}


def relevant(line):
    return any(s.key in stats.THEA for s in stats.parse(line))


def gain(b, t, base_dps, change):
    b2, t2 = engine.apply(b, t, change)
    return engine.dps(b2, t2)["dps"] / base_dps


def pool(slot):
    return json.loads((DATA / "affixes" / f"{SLOT_POOL[slot]}.json").read_text(encoding="utf-8"))


def families(p):
    fam = {}
    for side in ("prefix", "suffix"):
        for r in p[side]:
            k = (side, r["group"], stats.template(r["modifier"]))
            fam.setdefault(k, {})[r["tier"]] = r["modifier"]
    return fam


def craft_swaps(b, t, base, top):
    out = []
    for g in b["gear"]:
        if g["slot"] not in CRAFTED:
            continue
        fam = families(pool(g["slot"]))
        tmpl_of = {k[2]: k for k in fam}
        current = []
        for l in g["lines"]:
            k = tmpl_of.get(stats.template(l))
            if k:
                current.append((l, k))
        have = {k[2] for _, k in current}
        rows = []
        for l, (side, group, tm) in current:
            for (s2, g2, tm2), tiers in fam.items():
                if s2 != side or g2 != group or (tm2 in have and tm2 != tm):
                    continue
                t1 = tiers.get("1") or tiers.get("2")
                if not t1 or not relevant(t1):
                    continue
                gn = gain(b, t, base, {"remove_lines": [[g["slot"], l]], "add_lines": [[g["slot"], t1]]})
                gn0 = gain(b, t, base, {"remove_lines": [[g["slot"], l]], "add_lines": [[g["slot"], tiers["0"]]]}) \
                    if tiers.get("0") else None
                if gn > 1.005:
                    fe = COST_T1.get(group)
                    per = fe / ((gn - 1) * 100) if fe else None
                    rows.append((gn, gn0, l, t1, tiers.get("0"), group, per))
        rows.sort(key=lambda r: -r[0])
        out.append((g, rows[:top]))
    return out


def legendary_swaps(b, t, base, top):
    legs = json.loads((DATA / "legendaries.json").read_text(encoding="utf-8"))
    by_slot = defaultdict(list)
    for it in legs:
        by_slot[it.get("slot")].append(it)
    out = []
    for g in b["gear"]:
        cls = SLOT_POOL.get(g["slot"])
        rows = []
        for it in by_slot.get(cls, []):
            for corr in (False, True):
                lines = it.get("corroded") if corr else it.get("lines")
                if not lines:
                    continue
                # placeholders like <Random stat affix>: take the best option listed on the page
                chosen, specials = [], []
                rotating = False
                for l in lines:
                    if re.search(r"by turns|in turn", l, re.I):
                        rotating = True
                        specials.append(l)
                        continue
                    if l.startswith("<") and l.endswith(">"):
                        opts = (it.get("other") or {}).get(l + (" Corroded" if corr else "")) or (it.get("other") or {}).get(l) or []
                        best, bg = None, 1.0
                        for o in opts:
                            gg = gain(b, t, base, {"remove": [f"gear:{g['slot']}"], "add_items": [[g["slot"], [o]]]})
                            if gg > bg:
                                best, bg = o, gg
                        if best:
                            chosen.append(best)
                        continue
                    if stats.parse(l) and not rotating:
                        chosen.append(l)
                    elif stats.parse(l):
                        specials.append("(rotating) " + l)
                    elif stats.special(l) or re.search(r"\d", l):
                        specials.append(l)
                gn = gain(b, t, base, {"remove": [f"gear:{g['slot']}"], "add_items": [[g["slot"], chosen]]})
                rows.append((gn, it["name"] + (" (corroded)" if corr else ""), chosen, specials))
        rows.sort(key=lambda r: -r[0])
        out.append((g, rows[:top]))
    return out


def kismets(b, t, base, top):
    cat = json.loads((DATA / "catalog" / "Destiny.json").read_text(encoding="utf-8"))
    rows = []
    for c in cat["cards"]:
        for e in c.get("entries", []):
            nm = e.get("name") or ""
            size = "micro" if nm.startswith("Micro") else "medium" if nm.startswith("Medium") else None
            if not size:
                continue
            ref = "+13 Intelligence" if size == "micro" else "+27 Intelligence"
            lines = [l for l in e.get("lines", []) if stats.parse(l)]
            if not lines:
                continue
            gn = gain(b, t, base, {"replace_kismet": [ref, lines]})
            rows.append((gn, nm, lines, size))
    rows.sort(key=lambda r: -r[0])
    return rows[:top]


def slate_nodes(b, t, base, top):
    cat = json.loads((DATA / "catalog" / "Divinity_Slate.json").read_text(encoding="utf-8"))
    seen, rows = set(), []
    for c in cat["cards"]:
        if c["card"] != "Non-Legendary Divinity Slate":
            continue
        for e in c.get("entries", []):
            head = (e.get("lines") or [""])[0]
            if not head.startswith(("Micro", "Medium", "Legendary Medium", "Ultimate", "Nether")):
                continue  # core talents only go on a legendary slate's core slot (Pedigree)
            lines = [l for l in e.get("lines", [])[1:] if relevant(l)]
            if not lines:
                continue
            sig = (head.split("|")[-1].strip(), tuple(lines))
            if sig in seen:
                continue
            seen.add(sig)
            g0 = gain(b, t, base, {"add_slate": [lines, 0]})
            g54 = gain(b, t, base, {"add_slate": [lines, 54]})
            rows.append((g0, g54, head, lines))
    rows.sort(key=lambda r: -r[0])
    return rows[:top]


def memory_affixes(b, t, base, top):
    cat = json.loads((DATA / "catalog" / "Hero_Memories.json").read_text(encoding="utf-8"))
    rows = []
    for c in cat["cards"]:
        if c["card"] not in ("Random Affix", "Fixed Affix"):
            continue
        for tb in c.get("tables", []):
            for r in tb["rows"]:
                tier, mod, lvl, wt, src = (r["cells"] + [""] * 5)[:5]
                if tier not in ("0", "1") or not relevant(mod):
                    continue
                gn = gain(b, t, base, {"add_memory_line": mod})
                rows.append((gn, c["card"], src, tier, mod, wt))
    rows.sort(key=lambda r: -r[0])
    # current memory lines' own value (what you'd give up)
    cur = []
    for m in b["memories"]:
        for l in m["lines"]:
            if relevant(l):
                gn = gain(b, t, base, {"remove_memory_line": [str(m["slot"]), l]})
                cur.append((1 / gn, m["slot"], l))
            elif re.search(r"Minion", l):
                cur.append((1.0, m["slot"], l))
    cur.sort(key=lambda r: r[0])
    return rows[:top], cur


def prism_affixes(b, t, base, top):
    cat = json.loads((DATA / "catalog" / "Ethereal_Prism.json").read_text(encoding="utf-8"))
    rows, specials = [], []
    for c in cat["cards"]:
        for tb in c.get("tables", []):
            for r in tb["rows"]:
                txt, src, typ = (r["cells"] + [""] * 3)[:3]
                for part in txt.split(" / "):
                    if relevant(part):
                        rows.append((gain(b, t, base, {"add_slate": [[part], 0]}), src, typ, part))
                    elif re.search(r"Focus|Tangle|Spell|Cold|Critical|Projectile", part) and re.search(r"\d", part):
                        specials.append((src, typ, part))
    rows.sort(key=lambda r: -r[0])
    return rows[:top], specials[:top * 2]


def talent_nodes(b, t, base, top):
    trees = t
    alloc = {pa["panel"]: pa["nodes"] for pa in trees["panels"]}
    rows = []
    for key, p in engine.panels_data().items():
        if key not in alloc:
            continue
        for n in p["layout"]:
            if n.get("slot") == "core":
                continue
            lines = [l for l in n["lines"] if relevant(l)]
            if not lines:
                continue
            rank = n.get("max_rank") or 1
            have = alloc[key].get(n["id"], 0)
            gn = gain(b, t, base, {"add_slate": [lines * rank, 0]}) if not have else \
                1 / gain(b, t, base, {"tree_remove": [key, n["id"]]})
            rows.append(((gn - 1) / rank, gn, key, n["id"], n["name"], lines, rank, bool(have)))
    rows.sort(key=lambda r: -r[0])
    return rows


def fmt(x):
    return f"x{x:.3f} ({(x - 1) * 100:+.1f}%)"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=10)
    a = ap.parse_args(argv)
    b, t = engine.load()
    base = engine.dps(b, t)["dps"]
    L = ["# Scan — everything ranked against the current build", "",
         f"Generated by `tools/scan.py` on the build in `build.json` (model {engine.fmt_T(base)} with belt). "
         "Gains are whole-build DPS multipliers. Craft FE/1% uses T1 hit cost per group (docs/crafting.md).", ""]

    L += ["## Craft line swaps (same side + group, item stays legal)", ""]
    for g, rows in craft_swaps(b, t, base, a.top):
        if not rows:
            continue
        L += [f"### {g['slot']} — {g['name']}", "", "| replace | with T1 | gain T1 | gain T0 | FE/1% (T1) |", "|---|---|---|---|---|"]
        for gn, gn0, old, t1, t0, group, per in rows:
            L.append(f"| {old} | {t1} ({group.split()[0]}) | {fmt(gn)} | {fmt(gn0) if gn0 else '-'} | {per:.0f} |" if per else
                     f"| {old} | {t1} | {fmt(gn)} | {fmt(gn0) if gn0 else '-'} | - |")
        L.append("")

    L += ["## Legendary swaps per slot (best random-affix option taken; mechanics lines need hand pricing)", ""]
    for g, rows in legendary_swaps(b, t, base, a.top):
        good = [r for r in rows if r[0] > 0.97]
        if not good:
            continue
        L += [f"### {g['slot']} — vs {g['name']}", ""]
        for gn, name, chosen, specials in good[: a.top]:
            sp = f"  · *hand-price:* {' | '.join(specials[:3])}" if specials else ""
            L.append(f"- **{name}** {fmt(gn)}{sp}")
        L.append("")

    L += ["## Kismets (replacing one INT kismet of the same size)", ""]
    for gn, nm, lines, size in kismets(b, t, base, a.top * 2):
        L.append(f"- {fmt(gn)} **{nm}** — {' · '.join(lines)}")
    L.append("")

    L += ["## Slate nodes (one node added: unboosted corner / on the Judgment line x1.54)", ""]
    for g0, g54, head, lines in slate_nodes(b, t, base, a.top * 2):
        L.append(f"- {fmt(g0)} / {fmt(g54)} **{head}** — {' · '.join(lines)}")
    L.append("")

    mem, cur = memory_affixes(b, t, base, a.top * 2)
    L += ["## Hero memory affixes (T0/T1, value of adding one)", ""]
    for gn, card, src, tier, mod, wt in mem:
        L.append(f"- {fmt(gn)} {src} {card} T{tier} — {mod} (weight {wt})")
    L += ["", "Current memory lines, weakest first (what replacing them costs):", ""]
    for v, slot, l in cur:
        L.append(f"- slot {slot}: {l} — worth {fmt(v)}")
    L.append("")

    pr, sp = prism_affixes(b, t, base, a.top)
    L += ["## Prism affixes", ""]
    for gn, src, typ, part in pr:
        L.append(f"- {fmt(gn)} {part} ({src}, {typ})")
    L += ["", "Prism affixes that are mechanics (hand-price):", ""]
    for src, typ, part in sp:
        L.append(f"- {part} ({src}, {typ})")
    L.append("")

    tn = talent_nodes(b, t, base, a.top)
    L += ["## Talent nodes in your four panels, per point", "",
          "Unallocated nodes worth the most per point, then allocated nodes worth the least (pair rules not enforced here; "
          "use tools/tree.py to check a swap).", ""]
    L += ["### best unallocated"] + [f"- {fmt(1 + r[0])}/pt {r[2]} {r[3]} {r[4]} x{r[6]}: {' · '.join(r[5])}"
                                       for r in [x for x in tn if not x[7]][: a.top]]
    L += ["", "### weakest allocated"] + [f"- {fmt(1 + r[0])}/pt {r[2]} {r[3]} {r[4]} x{r[6]}: {' · '.join(r[5])}"
                                          for r in sorted([x for x in tn if x[7]], key=lambda r: r[0])[: a.top]]
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
