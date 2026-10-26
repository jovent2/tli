#!/usr/bin/env python3
"""Crawl tlidb.com (English) into data/raw (HTML cache) and data/pages (generic parsed JSON).

  python3 tools/crawl.py --depth 2            # crawl from the nav category pages
  python3 tools/crawl.py --only Israfels_Laws Magister
  python3 tools/crawl.py --reparse            # re-parse cached HTML without fetching

Polite: a few workers, small delay, retries. Safe to re-run; cached pages are not re-fetched
unless --refresh.
"""
import argparse
import json
import sys
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tlidb_parse import parse_page  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PAGES = ROOT / "data" / "pages"
SEEDS = """Hero Talent Ethereal_Prism Pactspirit Destiny Inventory Legendary_Gear Follower Active_Skill
Support_Skill Passive_Skill Activation_Medium_Skill Magnificent_Support_Skill Noble_Support_Skill
Modularization_Skill Tartarus_Skill Origin_Tartarus_Skill Craft Corrosion Blending_Rituals TOWER_Sequence
Graft Memory_Revival Nether_Kings_Divinity Netherrealm Confusion_Card_Library Void_Chart Compass Probe
Season_Compass Path_of_the_Brave Tip Path_of_Progression Help Divinity_Slate Hero_Memories""".split()

_lock = threading.Lock()


def raw_path(key):
    return RAW / f"en__{key}.html"


def fetch(key, refresh=False, delay=0.15):
    p = raw_path(key)
    if p.exists() and not refresh:
        return p.read_text(encoding="utf-8"), False
    url = "https://tlidb.com/en/" + urllib.parse.quote(key, safe="_%-().'")
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (tli-notes crawler)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                html = r.read().decode("utf-8", errors="replace")
            p.write_text(html, encoding="utf-8")
            time.sleep(delay)
            return html, True
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise
            last = e
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(2 * (attempt + 1))
    raise last


def process(key, refresh=False):
    html, fetched = fetch(key, refresh)
    d = parse_page(html, key)
    (PAGES / f"{key}.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return key, d["links"], fetched


def main(argv=None):
    import urllib.parse  # noqa: F401  (used in fetch)
    ap = argparse.ArgumentParser()
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max", type=int, default=20000)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--reparse", action="store_true")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args(argv)
    RAW.mkdir(parents=True, exist_ok=True)
    PAGES.mkdir(parents=True, exist_ok=True)

    if a.reparse:
        n = 0
        for p in sorted(RAW.glob("en__*.html")):
            key = p.name[4:-5]
            d = parse_page(p.read_text(encoding="utf-8"), key)
            (PAGES / f"{key}.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            n += 1
        print(f"reparsed {n}")
        return

    frontier = list(a.only) if a.only else list(SEEDS)
    depth_of = {k: 0 for k in frontier}
    done, failed = set(), {}
    fetched_n = 0
    t0 = time.time()
    while frontier and len(done) < a.max:
        batch, frontier = frontier, []
        with ThreadPoolExecutor(a.workers) as ex:
            futs = {ex.submit(process, k, a.refresh): k for k in batch if k not in done}
            for f in as_completed(futs):
                k = futs[f]
                done.add(k)
                try:
                    _, links, fetched = f.result()
                    fetched_n += fetched
                except Exception as e:  # noqa: BLE001
                    failed[k] = repr(e)
                    continue
                d = depth_of[k]
                if d < a.depth and not a.only:
                    for l in links:
                        if l not in depth_of:
                            depth_of[l] = d + 1
                            frontier.append(l)
                if len(done) % 200 == 0:
                    print(f"[{time.time() - t0:6.0f}s] done {len(done)} fetched {fetched_n} "
                          f"queued {len(frontier)} failed {len(failed)}", flush=True)
    print(f"FINISHED done {len(done)} fetched {fetched_n} failed {len(failed)} in {time.time() - t0:.0f}s")
    (ROOT / "data" / "crawl_report.json").write_text(json.dumps(
        {"done": len(done), "failed": failed, "depth": a.depth,
         "depth_of": depth_of}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    import urllib.parse  # noqa: E402
    main()
