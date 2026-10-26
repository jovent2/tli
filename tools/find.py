#!/usr/bin/env python3
"""Search the scraped tlidb data (data/search.jsonl).

  python3 tools/find.py focus blessing                 # all terms must appear (name or text), ranked
  python3 tools/find.py "max focus" --kind entry       # only list entries (talent nodes, destinies, affix rows...)
  python3 tools/find.py tangle --cat legendary         # filter by category / source substring
  python3 tools/find.py --name "Israfel"               # name match only
  python3 tools/find.py frostbite --regex "\\+\\d+ to Max Frostbite"
  python3 tools/find.py gale --full                    # print full text of hits
  python3 tools/find.py --page Israfels_Laws           # dump one page's text

Kinds: page (a whole tlidb page), entry (an item in a list card), row (a table row: affixes, glossary...).
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEARCH = ROOT / "data" / "search.jsonl"


def records():
    with open(SEARCH, encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--kind", choices=["page", "entry", "row"])
    ap.add_argument("--cat", help="substring of category / source page / card")
    ap.add_argument("--name", help="substring of the name")
    ap.add_argument("--regex", help="regex that must match some text line")
    ap.add_argument("--full", action="store_true", help="print all text lines of each hit")
    ap.add_argument("--page", help="print one page's full text")
    ap.add_argument("-n", type=int, default=30, help="max hits")
    a = ap.parse_args(argv)

    if a.page:
        for r in records():
            if r["kind"] == "page" and r["key"].lower() == a.page.lower():
                print(f"# {r['name']}  ({r['key']})  {', '.join(r.get('categories') or [])}")
                print("\n".join(r["text"]))
                return
        print("not found", file=sys.stderr)
        return

    terms = [t.lower() for t in a.terms]
    rx = re.compile(a.regex, re.I) if a.regex else None
    hits = []
    for r in records():
        if a.kind and r["kind"] != a.kind:
            continue
        name = (r.get("name") or "")
        if a.name and a.name.lower() not in name.lower():
            continue
        ctx = " ".join([*(r.get("categories") or []), r.get("source") or "", r.get("card") or ""]).lower()
        if a.cat and a.cat.lower() not in ctx:
            continue
        text = r.get("text") or []
        blob = (name + "\n" + "\n".join(text)).lower()
        if any(t not in blob for t in terms):
            continue
        if rx and not any(rx.search(l) for l in text):
            continue
        score = sum(3 for t in terms if t in name.lower()) + sum(blob.count(t) for t in terms)
        score += {"entry": 2, "row": 1, "page": 0}[r["kind"]]
        hits.append((score, r))
    hits.sort(key=lambda x: -x[0])
    for score, r in hits[: a.n]:
        where = ", ".join(r.get("categories") or []) or f"{r.get('source')} > {r.get('card')}"
        key = r.get("key") or ""
        print(f"[{r['kind']}] {r.get('name')}  {('(' + key + ')') if key else ''}  — {where}")
        text = r.get("text") or []
        if a.full:
            for l in text:
                print("    " + l)
        else:
            shown = [l for l in text if any(t in l.lower() for t in terms)] or text
            for l in shown[:4]:
                print("    " + l[:220])
    if len(hits) > a.n:
        print(f"... {len(hits) - a.n} more (use -n)")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
