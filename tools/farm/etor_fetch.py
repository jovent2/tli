"""Fetch etor strategy leaderboards and strategy details (rate limit ~1 req / 5 s, 429 "频繁" when faster).

  python3 etor_fetch.py lb week2 [week1 ...]        -> data/ext/etor_strategies_s14/lb_<stage>_<offset>.json (500 per stage)
  python3 etor_fetch.py details [--time 13] [--max N] [--exclude 囚笼,狩猎]
      -> details/<stage>_<key>.json for every leaderboard entry of that timeLabel (13 = Deep Space, 12 = Profound)
         that has no detail file yet, most-played first.
  python3 etor_fetch.py prices                       -> data/ext/prices_etor_s14_<today>.json
"""
import json, glob, os, sys, time, datetime, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXT = os.path.join(ROOT, "data", "ext"); SDIR = os.path.join(EXT, "etor_strategies_s14"); DDIR = os.path.join(SDIR, "details")
API = "https://etor-beta.710421059.xyz/etor-api/api"
SEASON = "1601"
GAP = 5.5

def get(url, tries=6):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as r:
                d = json.loads(r.read().decode("utf-8"))
            if d.get("success"): return d
            msg = json.dumps(d, ensure_ascii=False)[:200]
        except Exception as e:
            msg = str(e)[:200]
            if "404" in msg: return None                      # week1/week2 keys have no detail endpoint
        wait = GAP * (2 + 2 * k)
        print(f"  retry {k + 1} in {wait:.0f}s: {msg}", flush=True); time.sleep(wait)
    return None

def fetch_lb(stages):
    os.makedirs(SDIR, exist_ok=True)
    for stage in stages:
        for off in range(0, 500, 50):
            out = os.path.join(SDIR, f"lb_{stage}_{off}.json")
            d = get(f"{API}/strategy/leaderboard?seasonId={SEASON}&stage={stage}&limit=50&offset={off}")
            if d is None: print("failed", stage, off); break
            json.dump(d, open(out, "w"), ensure_ascii=False)
            n = len(d["data"]["items"]); print(f"{stage} offset {off}: {n} items", flush=True)
            if n < 50: break
            time.sleep(GAP)

def entries(time_label):
    keys = {}
    for f in sorted(glob.glob(os.path.join(SDIR, "lb_*.json"))):
        stage = os.path.basename(f)[3:].rsplit("_", 1)[0]
        for it in json.load(open(f))["data"]["items"]:
            if time_label and it["timeLabel"] != time_label: continue
            keys.setdefault(it["key"], (stage, it))
    return keys

def fetch_details(time_label="13", max_n=None, exclude=()):
    os.makedirs(DDIR, exist_ok=True)
    todo = []
    for key, (stage, it) in entries(time_label).items():
        if os.path.exists(os.path.join(DDIR, f"{stage}_{key}.json")): continue
        if stage.startswith("week"): continue                # the week boards' keys 404 on /detail (2026-10-30)
        if any(x in it["talentLabel"] for x in exclude): continue
        todo.append((it["count"], stage, key))
    todo.sort(reverse=True)
    if max_n: todo = todo[:max_n]
    print(f"{len(todo)} details to fetch (~{len(todo) * GAP / 60:.0f} min)", flush=True)
    for n, (cnt, stage, key) in enumerate(todo, 1):
        d = get(f"{API}/strategy/detail?seasonId={SEASON}&stage={stage}&strategyKey={key}")
        if d is None: print("failed", stage, key, flush=True); time.sleep(GAP); continue
        json.dump(d, open(os.path.join(DDIR, f"{stage}_{key}.json"), "w"), ensure_ascii=False)
        if n % 10 == 0: print(f"{n}/{len(todo)} ({stage} {key}, {cnt} runs)", flush=True)
        time.sleep(GAP)

def fetch_prices():
    d = get(f"{API}/prices-snapshot/{SEASON}")
    prev = sorted(glob.glob(os.path.join(EXT, "prices_etor_s14_*.json")))
    meta = {r["id"]: r for r in json.load(open(prev[-1]))["items"]} if prev else {}
    items = [{"id": r["id"], "key": meta.get(r["id"], {}).get("key"), "name_cn": meta.get(r["id"], {}).get("name_cn"),
              "type_cn": meta.get(r["id"], {}).get("type_cn"), "price_fe": r["price"], "updated": r.get("updatedAt")} for r in d["data"]]
    out = os.path.join(EXT, f"prices_etor_s14_{datetime.date.today().isoformat()}.json")
    json.dump({"source": f"{API}/prices-snapshot/{SEASON} fetched {datetime.datetime.now().isoformat(timespec='minutes')} (etor_fetch.py); key/name/type from the previous file. Unit: Flame Elementium.", "items": items}, open(out, "w"), ensure_ascii=False, indent=0)
    print("prices ->", out, len(items))

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(0)
    if a[0] == "lb": fetch_lb(a[1:])
    elif a[0] == "prices": fetch_prices()
    elif a[0] == "details":
        tl = a[a.index("--time") + 1] if "--time" in a else "13"
        mx = int(a[a.index("--max") + 1]) if "--max" in a else None
        ex = a[a.index("--exclude") + 1].split(",") if "--exclude" in a else ()
        fetch_details(tl, mx, ex)
