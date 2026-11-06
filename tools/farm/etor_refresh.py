#!/usr/bin/env python3
"""One-shot etor refresh for a scan (resume-safe, ~1 req / 5.5 s): prices snapshot, trend board, leaderboards, strategy details
keyed by the board they sit on (week boards give details since 11-06), price history per item.

  python3 tools/farm/etor_refresh.py all --stages week3,week2 [--time 13] [--charts data/ext/etor_charts/items.txt]
  python3 tools/farm/etor_refresh.py prices | wind STAGE | lb STAGE... | details STAGE... | charts FILE

Files: data/ext/prices_etor_s14_<date>.json, etor_strategies_s14/wind_<stage>_<offset>.json, lb_<stage>_<offset>.json,
details/<stage>_<key>.json, etor_charts/<item>.json ({trend: [{timestamp, price, minPrice, maxPrice}], interval 1d}).
"""
import datetime
import glob
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etor_fetch as EF  # noqa: E402

CDIR = os.path.join(EF.EXT, "etor_charts")


def wind(stage):
    os.makedirs(EF.SDIR, exist_ok=True)
    for off in range(0, 5000, 100):
        out = os.path.join(EF.SDIR, f"wind_{stage}_{off}.json")
        d = EF.get(f"{EF.API}/strategy/windboard?seasonId={EF.SEASON}&stage={stage}&limit=100&offset={off}")
        if d is None:
            print("wind failed", stage, off, flush=True)
            break
        json.dump(d, open(out, "w"), ensure_ascii=False)
        n = len(d["data"]["items"])
        print(f"wind {stage} offset {off}: {n} items of {d['data'].get('total')}", flush=True)
        if n < 100:
            break
        time.sleep(EF.GAP)


def details(stages, time_label="13"):
    os.makedirs(EF.DDIR, exist_ok=True)
    todo = []
    for stage in stages:
        for f in sorted(glob.glob(os.path.join(EF.SDIR, f"lb_{stage}_*.json"))):
            for it in json.load(open(f))["data"]["items"]:
                if time_label and str(it["timeLabel"]) != str(time_label):
                    continue
                if os.path.exists(os.path.join(EF.DDIR, f"{stage}_{it['key']}.json")):
                    continue
                todo.append((it["count"], stage, it["key"]))
    todo.sort(reverse=True)
    print(f"{len(todo)} details to fetch (~{len(todo) * EF.GAP / 60:.0f} min)", flush=True)
    for n, (cnt, stage, key) in enumerate(todo, 1):
        d = EF.get(f"{EF.API}/strategy/detail?seasonId={EF.SEASON}&stage={stage}&strategyKey={key}")
        if d is None:
            print("failed", stage, key, flush=True)
            time.sleep(EF.GAP)
            continue
        json.dump(d, open(os.path.join(EF.DDIR, f"{stage}_{key}.json"), "w"), ensure_ascii=False)
        if n % 20 == 0:
            print(f"{n}/{len(todo)} ({stage} {key}, {cnt} runs)", flush=True)
        time.sleep(EF.GAP)


def get_json(url, tries=3):
    import urllib.request
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            print(f"  retry {k + 1}: {str(e)[:120]}", flush=True)
            time.sleep(EF.GAP * (2 + 2 * k))
    return None


def charts(path, interval="1d"):
    os.makedirs(CDIR, exist_ok=True)
    items = [x.split()[0] for x in open(path) if x.strip() and not x.startswith("#")]
    for n, i in enumerate(items, 1):
        out = os.path.join(CDIR, f"{i}.json")
        if os.path.exists(out) and time.time() - os.path.getmtime(out) < 20 * 3600:
            continue
        d = get_json(f"{EF.API}/chart/{EF.SEASON}/{i}?interval={interval}")   # no "success" field on this endpoint
        if d is None or not d.get("trend"):
            print("chart: no history for", i, flush=True)
            time.sleep(EF.GAP)
            continue
        d["fetched"] = datetime.datetime.now().isoformat(timespec="minutes")
        json.dump(d, open(out, "w"), ensure_ascii=False)
        print(f"chart {n}/{len(items)} {i}: {len(d.get('trend', []))} days", flush=True)
        time.sleep(EF.GAP)


def get_arg(a, flag, default):
    return a[a.index(flag) + 1] if flag in a else default


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(0)
    cmd = a[0]
    if cmd == "prices":
        EF.fetch_prices()
    elif cmd == "wind":
        wind(a[1])
    elif cmd == "lb":
        EF.fetch_lb(a[1:])
    elif cmd == "details":
        details([s for s in a[1:] if not s.startswith("--")], get_arg(a, "--time", "13"))
    elif cmd == "charts":
        charts(a[1])
    elif cmd == "all":
        stages = get_arg(a, "--stages", "week3,week2").split(",")
        EF.fetch_prices()
        time.sleep(EF.GAP)
        wind(stages[0])
        time.sleep(EF.GAP)
        EF.fetch_lb(stages)
        time.sleep(EF.GAP)
        ch = get_arg(a, "--charts", None)
        if ch:
            charts(ch)
            time.sleep(EF.GAP)
        details(stages, get_arg(a, "--time", "13"))
        print("done", flush=True)
