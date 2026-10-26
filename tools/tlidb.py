#!/usr/bin/env python3
"""Read tlidb.com pages directly (raw HTML, no summarizer in between).

Usage:
  python3 tools/tlidb.py PAGE                 # clean text of the page
  python3 tools/tlidb.py PAGE --tables        # every table as rows (JSON lines)
  python3 tools/tlidb.py PAGE --grep REGEX    # text lines matching REGEX (with context)
  python3 tools/tlidb.py PAGE --refresh ...   # re-download instead of using the cache

PAGE is the tlidb path, e.g. "Wand", "Gale", "Israfels_Laws", "en/Tartarus_Season",
or a full https://tlidb.com/... URL.

URL rules (learned the hard way): drop apostrophes, spaces become underscores
("Israfel's Laws" -> Israfels_Laws). Pages are cached under data/raw/ (gitignored).

Library use:
  from tools.tlidb import page_text, page_tables
"""
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "raw"
BASE = "https://tlidb.com/"


def page_url(page: str) -> str:
    if page.startswith("http"):
        return page
    page = page.strip().replace("'", "").replace("’", "").replace(" ", "_")
    return BASE + urllib.parse.quote(page, safe="/_%-().:")


def cache_path(url: str) -> Path:
    name = url.replace(BASE, "").replace("/", "__") or "index"
    name = re.sub(r"[^A-Za-z0-9_.%()-]", "_", name)
    return CACHE / f"{name}.html"


def fetch(page: str, refresh: bool = False) -> str:
    url = page_url(page)
    path = cache_path(url)
    if path.exists() and not refresh:
        return path.read_text(encoding="utf-8")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (tli-notes)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        html = r.read().decode("utf-8", errors="replace")
    CACHE.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return html


def _soup(html: str):
    from bs4 import BeautifulSoup  # lxml parser handles tlidb's unclosed <td>/<tr>
    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    return soup


BLOCK = ["div", "p", "li", "ul", "ol", "tr", "td", "th", "table", "h1", "h2", "h3", "h4", "h5", "h6",
         "section", "article", "header", "footer", "nav", "dl", "dt", "dd", "hr"]


def page_text(page: str, refresh: bool = False) -> list[str]:
    """Non-empty text lines of the page body, in order. Inline tags (spans, links) stay
    on one line; block tags and <br> break lines."""
    soup = _soup(fetch(page, refresh))
    body = soup.find("main") or soup.body or soup
    for br in body.find_all("br"):
        br.replace_with("\n")
    for el in body.find_all(BLOCK):
        el.insert_before("\n")
        el.insert_after("\n")
    lines = [re.sub(r"\s+", " ", s).strip() for s in body.get_text("").split("\n")]
    out = []
    for l in lines:
        if l and (not out or out[-1] != l):
            out.append(l)
    return out


def page_tables(page: str, refresh: bool = False) -> list[dict]:
    """Every <table>: nearest heading, header row, data rows (cell text), and tier attr."""
    soup = _soup(fetch(page, refresh))
    tables = []
    for i, t in enumerate(soup.find_all("table")):
        h = t.find_previous(["h1", "h2", "h3", "h4", "h5", "h6"])
        rows = []
        header = None
        for tr in t.find_all("tr"):
            cells = [re.sub(r"\s+", " ", c.get_text(" ", strip=True)) for c in tr.find_all(["td", "th"], recursive=False)]
            if not cells:
                continue
            if header is None and tr.find("th"):
                header = cells
                continue
            row = {"cells": cells}
            if tr.get("data-tier") is not None:
                row["tier"] = tr.get("data-tier")
            rows.append(row)
        tables.append({"index": i, "heading": h.get_text(" ", strip=True) if h else None,
                       "header": header, "rows": rows})
    return tables


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page")
    ap.add_argument("--tables", action="store_true")
    ap.add_argument("--grep")
    ap.add_argument("-C", type=int, default=2, help="context lines for --grep")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args(argv)
    if a.tables:
        for t in page_tables(a.page, a.refresh):
            print(json.dumps(t, ensure_ascii=False))
        return
    lines = page_text(a.page, a.refresh)
    if a.grep:
        rx = re.compile(a.grep, re.I)
        hits = [i for i, l in enumerate(lines) if rx.search(l)]
        shown = set()
        for i in hits:
            for j in range(max(0, i - a.C), min(len(lines), i + a.C + 1)):
                if j not in shown:
                    print(("> " if j == i else "  ") + lines[j])
                    shown.add(j)
            print("--")
        return
    print("\n".join(lines))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:  # piping into head
        sys.exit(0)
