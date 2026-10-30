"""Logged etor runs (CN, season 14) joined with prices, item names and the Void Chart graph.

load() -> list of dicts, one per leaderboard entry (Profound by default):
  key, stage, name, count, dur_s, etor_earn, etor_eff, map, loot {id: qty/run}, cost {id: qty/run}, talents {md5: count},
  nodes [(constellation, node)], compasses {key: per run}, gross (FE/run at today's prices, seller tax on sellables),
  cost_fe, net, net_per_min.
Prices: data/ext/prices_etor_s14_*.json (latest). Tax: 12.5% on sold items, FE untaxed [Vlad].
"""
import json, glob, os, re, collections
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXT = os.path.join(ROOT, "data", "ext")
TAX = 0.125
FE_ID = "100300"

def _latest_prices():
    f = sorted(glob.glob(os.path.join(EXT, "prices_etor_s14_*.json")))[-1]
    P = json.load(open(f))["items"]
    return {r["id"]: r for r in P}, f

PRICES, PRICE_FILE = _latest_prices()
ITEMS = {r["id"]: r for r in json.load(open(os.path.join(EXT, "etor_items.json")))}
GRAPH = json.load(open(os.path.join(EXT, "void_chart_graph.json")))
MD5 = {n["md5"]: (k, n) for k, v in GRAPH.items() for n in v["nodes"] if n["md5"]}
# etor hashes multi-line nodes with other joins (no card line, "\n" literal, single line...): add every variant so Obtuse / Dull /
# Extravagant / Oppressive ... decode (2026-10-29: 25 of 27 leftover keys were these)
import hashlib as _h
def _variants(lines):
    L = [l for l in lines if l]; core = [l for l in L if "混乱卡牌" not in l]    # the card line, not every "时刻 8 及以上" line (Willful - Might)
    for sep in ("\n", "", " ", "\\n", "\r\n", "<br>", "\n\n", "；", ";"):
        yield sep.join(L); yield sep.join(core)
    yield "\n".join(L) + "\n"
    for l in L: yield l
for _k, _v in GRAPH.items():
    for _n in _v["nodes"]:
        _cn = _n.get("cn") or []
        if isinstance(_cn, str): _cn = [_cn]
        for _t in _variants(_cn):
            _hh = _h.md5(_t.encode("utf-8")).hexdigest()
            if _hh not in MD5: MD5[_hh] = (_k, _n)

def price(i):
    if i == FE_ID: return 1.0                      # FE is the unit; it has no row in the price snapshot (was 0 -> every net was short by the FE drops)
    r = PRICES.get(i)
    return float(r["price_fe"]) if r else None

def name(i):
    r = ITEMS.get(i)
    return (r["key"] or r["name_cn"]) if r else f"?{i}"

def typ(i):
    r = ITEMS.get(i)
    return r["type_cn"] if r else "?"

def value(i, qty, sold=True):
    p = price(i)
    if p is None: return 0.0
    if i == FE_ID or not sold: return p * qty
    return p * qty * (1 - TAX)

def load(time_label="12", stages=None):
    rows = {}
    for f in sorted(glob.glob(os.path.join(EXT, "etor_strategies_s14", "lb_*.json"))):
        stage = os.path.basename(f)[3:].rsplit("_", 1)[0]
        if stages and stage not in stages: continue
        for it in json.load(open(f))["data"]["items"]:
            if time_label and it["timeLabel"] != time_label: continue
            rows.setdefault(it["key"], (stage, it))
    out = []
    for key, (stage, it) in rows.items():
        df = os.path.join(EXT, "etor_strategies_s14", "details", f"{stage}_{key}.json")
        if not os.path.exists(df): continue
        d = json.load(open(df))["data"]
        n = it["count"]
        loot = {x["id"]: x["quantity"] / n for x in d["items"]["loot"]}
        cost = {x["id"]: x["quantity"] / n for x in d["items"]["cost"]}
        talents = {t["key"]: t["count"] for t in d["talents"]}
        nodes = [(MD5[k][0], MD5[k][1], c) for k, c in talents.items() if k in MD5]
        gross = sum(value(i, q) for i, q in loot.items())
        cost_fe = sum(value(i, q, sold=False) for i, q in cost.items())
        dur = it["avgDuration"] / 1000.0
        out.append(dict(key=key, stage=stage, name=it["name"], count=n, dur_s=dur, etor_earn=it["avgEarnings"], etor_eff=it["avgEfficiency"],
                        map=it["mapLabel"], talent_label=it["talentLabel"], loot=loot, cost=cost, talents=talents, nodes=nodes,
                        gross=gross, cost_fe=cost_fe, net=gross - cost_fe, net_per_min=(gross - cost_fe) / (dur / 60) if dur else 0,
                        tags=d.get("tags", [])))
    return out

if __name__ == "__main__":
    R = load()
    print(len(R), "profound strategies,", sum(r["count"] for r in R), "runs; prices from", os.path.basename(PRICE_FILE))
    unpriced = collections.Counter()
    for r in R:
        for i, q in r["loot"].items():
            if price(i) is None: unpriced[(i, name(i), typ(i))] += q * r["count"]
    print("unpriced loot (total qty):", unpriced.most_common(25))
