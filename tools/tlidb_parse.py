"""Generic structural parser for tlidb pages.

Every tlidb page is a set of cards (often inside tab panes). A card holds either
  - a table (craft affix pools, level tables, drop tables), or
  - a grid of entries (div.col): icon + linked name + lines of text (items, talents, skills...), or
  - plain text (help, rules, item detail).
parse_page() turns a page into {"title", "url", "cards": [...]} without interpreting it, so nothing
is lost; category-specific views are built on top of this in tools/build_data.py.
"""
import re
import urllib.parse

from bs4 import BeautifulSoup, NavigableString, Tag

LANGS = {"tw", "cn", "ko", "ja", "ru", "de", "fr", "es", "pt", "th", "vi", "en"}
BLOCK = {"div", "p", "li", "ul", "ol", "tr", "td", "th", "table", "h1", "h2", "h3", "h4", "h5", "h6",
         "section", "article", "header", "footer", "dl", "dt", "dd", "hr", "form"}


def normalize(href: str):
    """tlidb internal link -> canonical page key like 'Israfels_Laws' (English), else None."""
    if not href or href.startswith(("#", "javascript:", "mailto:")):
        return None
    u = urllib.parse.urlparse(href)
    if u.netloc and u.netloc not in ("tlidb.com", "www.tlidb.com"):
        return None
    path = urllib.parse.unquote(u.path).lstrip("/")
    if not path:
        return None
    parts = path.split("/")
    if parts[0] in LANGS:
        if parts[0] != "en":
            return None
        parts = parts[1:]
    if not parts or not parts[0] or len(parts) > 1:
        return None
    key = parts[0]
    if re.search(r"\.(png|jpg|jpeg|webp|gif|svg|css|js|ico|xml|txt)$", key, re.I):
        return None
    if key in ("privacy",):
        return None
    return key


def text_lines(el) -> list[str]:
    """Text of an element split into lines at <br> and block boundaries; inline stays joined."""
    out, cur = [], []

    def flush():
        s = re.sub(r"\s+", " ", "".join(cur)).strip()
        if s:
            out.append(s)
        cur.clear()

    def walk(node):
        for ch in node.children:
            if isinstance(ch, NavigableString):
                if ch.__class__.__name__ in ("Comment", "Doctype", "Declaration"):
                    continue
                cur.append(str(ch))
            elif isinstance(ch, Tag):
                if ch.name in ("script", "style", "noscript", "img", "button", "input"):
                    continue
                if ch.name == "br":
                    flush()
                    continue
                if "justify-content-between" in (ch.get("class") or []):
                    # name / points / ranks rows: one line, tokens separated
                    flush()
                    toks = [re.sub(r"\s+", " ", t.get_text(" ", strip=True)) for t in ch.find_all(recursive=False)]
                    out.append(" | ".join(t for t in toks if t))
                    continue
                blk = ch.name in BLOCK
                if blk:
                    flush()
                walk(ch)
                if blk:
                    flush()

    walk(el)
    flush()
    return out


def _owner_card(el):
    p = el.parent
    while p is not None:
        if isinstance(p, Tag) and p.name == "div" and "card" in (p.get("class") or []):
            return p
        p = p.parent
    return None


def _table(t: Tag) -> dict:
    header, rows = None, []
    for tr in t.find_all("tr"):
        cells = tr.find_all(["td", "th"], recursive=False)
        if not cells:
            continue
        vals = [" / ".join(text_lines(c)) for c in cells]
        if header is None and tr.find("th", recursive=False) is not None:
            header = vals
            continue
        row = {"cells": vals}
        if tr.get("data-tier") is not None:
            row["tier"] = tr.get("data-tier")
        links = [k for k in (normalize(a.get("href")) for a in tr.find_all("a", href=True)) if k]
        if links:
            row["links"] = sorted(set(links))
        rows.append(row)
    return {"header": header, "rows": rows}


def _entry(col: Tag) -> dict | None:
    body = col.select_one("div.flex-grow-1") or col
    a = body.find("a", href=True)
    lines = text_lines(body)
    if not lines:
        return None
    e = {"lines": lines}
    if a is not None:
        e["name"] = a.get_text(" ", strip=True)
        k = normalize(a.get("href"))
        if k:
            e["key"] = k
        if lines and lines[0] == e["name"]:
            e["lines"] = lines[1:]
    img = col.find("img")
    if img is not None and img.get("alt"):
        e["icon"] = img.get("alt")
    return e


def _svgs(soup) -> list[dict]:
    """Talent-panel style SVG graphs: node images with tooltips, connecting lines, column labels."""
    out = []
    for svg in soup.find_all("svg"):
        nodes = []
        for im in svg.find_all("image"):
            title = im.get("data-bs-title")
            n = {k: float(im.get(k)) for k in ("x", "y", "width", "height") if im.get(k) is not None}
            if title:
                tip = BeautifulSoup(title, "lxml")
                nm = tip.find(class_="sp-node-name")
                n["name"] = nm.get_text(" ", strip=True) if nm else None
                if nm:
                    nm.decompose()
                n["lines"] = text_lines(tip.body or tip)
            href = im.get("xlink:href") or im.get("href")
            if href:
                n["icon"] = href.rsplit("/", 1)[-1]
            nodes.append(n)
        edges = [[float(l.get(k)) for k in ("x1", "y1", "x2", "y2")] for l in svg.find_all("line")
                 if all(l.get(k) is not None for k in ("x1", "y1", "x2", "y2"))]
        labels = [{"x": float(t.get("x") or 0), "y": float(t.get("y") or 0), "text": t.get_text(strip=True),
                   "class": " ".join(t.get("class") or [])} for t in svg.find_all("text")]
        if nodes or edges:
            out.append({"viewBox": svg.get("viewbox") or svg.get("viewBox"), "nodes": nodes,
                        "edges": edges, "labels": labels})
    return out


def parse_page(html: str, key: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    svgs = _svgs(soup)
    title = soup.title.get_text(strip=True) if soup.title else key
    title = re.sub(r"\s*-\s*Torchlight: Infinite Wiki\s*$", "", title)
    cards = []
    for card in soup.select("div.card"):
        hdr = card.find("div", class_="card-header", recursive=False)
        header = text_lines(hdr) if hdr else []
        c = {"header": " ".join(header) if header else None}
        pane = card.find_parent("div", class_="tab-pane")
        if pane is not None and pane.get("id"):
            c["tab"] = pane.get("id")
        tables = [_table(t) for t in card.find_all("table") if _owner_card(t) is card]
        cols = [d for d in card.find_all("div", class_="col") if _owner_card(d) is card]
        if tables:
            c["tables"] = tables
        if cols:
            c["entries"] = [e for e in (_entry(d) for d in cols) if e]
        if not tables and not cols:
            # plain card: text minus nested cards
            clone = BeautifulSoup(str(card), "lxml").find("div", class_="card")
            for sub in clone.find_all("div", class_="card"):
                if sub is not clone:
                    sub.decompose()
            h2 = clone.find("div", class_="card-header", recursive=False)
            if h2:
                h2.decompose()
            lines = [l for l in text_lines(clone) if l not in ("Reset", "Search")]
            if lines:
                c["text"] = lines
        if c.get("text", [None])[0] == "Sites":  # site footer
            continue
        if len(c) > 1:
            cards.append(c)
    # tables that sit directly in a tab pane (e.g. "<Slot> Craft" prefix/suffix pools), not in a card
    tab_label = {a.get("href")[1:]: a.get_text(" ", strip=True)
                 for a in soup.select("ul.nav-tabs a[href^='#']")}
    orphan = {}
    for t in soup.find_all("table"):
        if _owner_card(t) is not None:
            continue
        pane = t.find_parent("div", class_="tab-pane")
        pid = pane.get("id") if pane is not None else None
        tb = _table(t)
        prev = t.find_previous(string=lambda s: s and s.strip() and s.parent.name not in ("script", "style"))
        if prev:
            tb["before"] = prev.strip()[:80]
        orphan.setdefault(pid, []).append(tb)
    for pid, tbs in orphan.items():
        cards.append({"header": tab_label.get(pid, pid), "tab": pid, "tables": tbs})
    links = sorted({k for k in (normalize(a.get("href")) for a in soup.find_all("a", href=True)) if k})
    d = {"key": key, "title": title, "cards": cards, "links": links}
    if svgs:
        d["svg"] = svgs
    return d
