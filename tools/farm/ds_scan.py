#!/usr/bin/env python3
"""Deep Space scan on the freshest etor boards: every logged strategy re-valued at today's prices, grouped by the exact
compass/astrolabe/probe set it ran, with lotteries split out, deaths per run (etor logs them), the spread across players,
price trends of the loot, and the net per minute at Vlad's speed.

  python3 tools/farm/ds_scan.py [--stages week3,week2] [--min-runs 60] [--top 30] [--show N] [--all] [--json out.json]

Per strategy (one player's setup over its runs): loot and cost per run from /strategy/detail, valued at the latest price file
(12.5% tax on sales, FE untaxed, Secrets at the exchange value), duration and deaths from the board entry.
Groups: the compass/astrolabe/probe keys consumed on >= 50% of runs (+ DS resonance bucket) and the constellations in the talent label.
Steady loot = items with >= MIN_DROPS drops across the group; the rest is "lottery" and shown separately.
Vlad's speed: seconds per map from his own logs for the mechanics he has run (VLAD_S), else CN seconds x 1.2.
Filters (--all turns them off): no Cage, Doll, Might, Cruising/Machines, Clockwork.
"""
import argparse
import collections
import glob
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN  # noqa: E402

EXT = RN.EXT
SDIR = os.path.join(EXT, "etor_strategies_s14")
MIN_DROPS = 8
SKIP_COST = {"Deep_Space_Beacon", "Netherrealm_resonance", "Deep_Space_Resonance", "Glacial_Abyss_Beacon_%28Timemark_8%29"}
OUT = {"Cage": ("囚笼", "Golden_Cage", "Cage_Astrolabe"), "Doll": ("玩偶", "Collection_Doll", "Clockwork"), "Might": ("巨力", "Might_Compass", "Mecha_Might"),
       "Machines": ("Cruising_Mechanical",)}
# His seconds per map on the mechanics he has run in Deep Space (his logs 11-05/06; 10-30 for Machines), else CN x 1.2.
VLAD_S = {("Evernight_Vigil", "Shadow_Overrealm"): 209, ("Alert_Outlaw", "All-Evil_Vigil"): 124, ("Cruising_Mechanical",): 200}
VLAD_FACTOR = 1.2


def short(n):
    return (n.replace("_Compass", "").replace("_Astrolabe", " astro").replace("_Probe", " probe").replace("_%28Artifact%29", " (A)")
            .replace("%28Artifact%29", "(A)").replace("_", " ").strip())


def load(stages):
    """Latest board first: a key found in week3 is taken from week3 (its detail file week3_<key>.json), else week2 ..."""
    rows = {}
    for stage in stages:
        for f in sorted(glob.glob(os.path.join(SDIR, f"lb_{stage}_*.json"))):
            for it in json.load(open(f))["data"]["items"]:
                if str(it["timeLabel"]) != "13" or it["key"] in rows:
                    continue
                df = os.path.join(SDIR, "details", f"{stage}_{it['key']}.json")
                if not os.path.exists(df):
                    continue
                d = json.load(open(df))["data"]
                n = it["count"]
                loot = {x["id"]: x["quantity"] / n for x in d["items"]["loot"]}
                cost = {x["id"]: x["quantity"] / n for x in d["items"]["cost"]}
                rows[it["key"]] = dict(key=it["key"], stage=stage, name=it["name"], count=n, dur_s=it["avgDuration"] / 1000.0,
                                       deaths=it.get("deathCount", 0) / n, etor_eff=it["avgEfficiency"], talent_label=it["talentLabel"],
                                       loot=loot, cost=cost, talents={t["key"]: t["count"] for t in d["talents"]},
                                       player=it.get("playerId"))
    return list(rows.values())


def signature(r):
    keys = []
    for i, q in r["cost"].items():
        n = RN.name(i)
        if n in SKIP_COST or q < 0.5:
            continue
        if n.endswith("Compass") or "Astrolabe" in n or "Probe" in n or "%29" in n:
            keys.append(n)
    return tuple(sorted(keys))


def family(r):
    return "+".join(t for t in r["talent_label"].replace(",", "、").split("、") if t and t != "幽邃")


def ds_res(r):
    q = sum(v for i, v in r["cost"].items() if RN.name(i) == "Deep_Space_Resonance")
    return 0 if q < 0.5 else (1 if q < 1.5 else 2 if q < 3 else 3)


def excluded(sig, fam):
    s = " ".join(sig) + " " + fam
    return [k for k, pats in OUT.items() if any(p in s for p in pats)]


def vlad_seconds(sig, cn_s):
    for keys, s in VLAD_S.items():
        if all(any(k in x for x in sig) for k in keys):
            return s, "his logs"
    return cn_s * VLAD_FACTOR, f"CN x{VLAD_FACTOR}"


def trend(items, days=7):
    """Value-weighted price change over the last `days` days for a loot basket {id: value share}."""
    tot = 0.0; w = 0.0
    for i, v in items.items():
        f = os.path.join(EXT, "etor_charts", f"{i}.json")
        if not os.path.exists(f):
            continue
        tr = json.load(open(f)).get("trend", [])
        if len(tr) < days + 1:
            continue
        a, b = tr[-days - 1]["price"], tr[-1]["price"]
        if a and b:
            tot += v * (b / a - 1); w += v
    return tot / w if w else None


def group(R, min_runs=1, show_all=False):
    G = collections.defaultdict(list)
    for r in R:
        G[(signature(r), family(r), ds_res(r))].append(r)
    out = []
    for (sig, fam, res), rs in G.items():
        n = sum(r["count"] for r in rs)
        if n < min_runs:
            continue
        ex = excluded(sig, fam)
        if ex and not show_all:
            continue
        loot = collections.Counter(); cost = collections.Counter(); secs = 0.0; deaths = 0.0
        for r in rs:
            for i, q in r["loot"].items():
                loot[i] += q * r["count"]
            for i, q in r["cost"].items():
                cost[i] += q * r["count"]
            secs += r["dur_s"] * r["count"]; deaths += r["deaths"] * r["count"]
        steady_items = {i: RN.value(i, q) / n for i, q in loot.items() if q >= MIN_DROPS and RN.price(i)}
        lottery_items = {i: RN.value(i, q) / n for i, q in loot.items() if 0 < q < MIN_DROPS and RN.price(i)}
        steady = sum(steady_items.values()); lottery = sum(lottery_items.values())
        c = sum(RN.value(i, q, sold=False) for i, q in cost.items()) / n
        d = secs / n
        # per-player spread: net/min (steady only) per strategy, weighted by runs when taking quantiles
        per = sorted(((sum(RN.value(i, q) for i, q in r["loot"].items() if loot[i] >= MIN_DROPS)
                       - sum(RN.value(i, q, sold=False) for i, q in r["cost"].items())) / (r["dur_s"] / 60), r["count"]) for r in rs)
        acc = 0; med = None; top = []
        for v, cnt in per:
            acc += cnt
            if med is None and acc >= n / 2:
                med = v
        tail = [v for v, cnt in per for _ in range(max(1, cnt // 10))]
        top3 = statistics.mean(tail[-max(1, len(tail) // 3):]) if tail else None
        vs, src = vlad_seconds(sig, d)
        out.append(dict(sig=sig, fam=fam, res=res, strategies=len(rs), runs=n, steady=steady, lottery=lottery, cost=c, secs=d,
                        net=steady - c, per_min=(steady - c) / (d / 60), med_per_min=med, top_per_min=top3, deaths=deaths / n,
                        vlad_s=vs, vlad_src=src, vlad_per_min=(steady - c) / (vs / 60), excluded=ex,
                        steady_items=steady_items, lottery_items=lottery_items, loot=loot, cost_items=cost, rs=rs,
                        trend7=trend(steady_items)))
    return out


def show(g, k=None, full=False):
    sig = " + ".join(short(s) for s in g["sig"]) or "(no compass)"
    res = f" + DS res x{g['res']}" if g["res"] else ""
    print(f"\n## {('#%d ' % k) if k is not None else ''}{sig}{res}  [{g['fam']}]  {g['strategies']} players, {g['runs']} runs"
          + (f"  EXCLUDED: {','.join(g['excluded'])}" if g["excluded"] else ""))
    tr = f"{g['trend7'] * 100:+.0f}%/7d" if g["trend7"] is not None else "n/a"
    print(f"  CN: steady {g['steady']:.0f} - cost {g['cost']:.0f} = net {g['net']:.0f}/map at {g['secs']:.0f} s = {g['per_min']:.1f}/min "
          f"(median player {g['med_per_min']:.0f}, top third {g['top_per_min']:.0f}); lottery +{g['lottery']:.0f}/map; deaths {g['deaths']:.2f}/run; loot price trend {tr}")
    print(f"  Vlad: {g['vlad_s']:.0f} s ({g['vlad_src']}) -> {g['vlad_per_min']:.1f}/min steady, {(g['net'] + g['lottery']) / (g['vlad_s'] / 60):.1f} with lotteries")
    top = sorted(g["steady_items"].items(), key=lambda kv: -kv[1])[:10 if not full else 25]
    print("  loot/map: " + ", ".join(f"{short(RN.name(i))} {g['loot'][i] / g['runs']:.2f} ({v:.1f})" for i, v in top))
    if g["lottery_items"]:
        lt = sorted(g["lottery_items"].items(), key=lambda kv: -kv[1])[:6]
        print("  lottery: " + ", ".join(f"{short(RN.name(i))} {int(g['loot'][i])} drops ({v:.1f}/map)" for i, v in lt))
    print("  cost/map: " + ", ".join(f"{short(RN.name(i))} {q / g['runs']:.2f} ({RN.value(i, q, sold=False) / g['runs']:.1f})" for i, q in g["cost_items"].items()))
    if full:
        for r in sorted(g["rs"], key=lambda r: -r["count"])[:12]:
            net = sum(RN.value(i, q) for i, q in r["loot"].items() if g["loot"][i] >= MIN_DROPS) - sum(RN.value(i, q, sold=False) for i, q in r["cost"].items())
            print(f"    {r['count']:4d} runs {r['dur_s']:5.0f} s net {net:6.0f}/map = {net / (r['dur_s'] / 60):5.1f}/min deaths {r['deaths']:.2f}  {r['name'][:70]}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--stages", default="week3,week2")
    ap.add_argument("--min-runs", type=int, default=60)
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--show", type=int, default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--sort", default="vlad", choices=["vlad", "cn", "top"])
    ap.add_argument("--json", default=None)
    a = ap.parse_args(argv)
    R = load(a.stages.split(","))
    print(f"{len(R)} Deep Space strategies with details from {a.stages} ({sum(r['count'] for r in R)} runs); prices {os.path.basename(RN.PRICE_FILE)}")
    G = group(R, a.min_runs, a.all)
    key = {"vlad": lambda g: -g["vlad_per_min"], "cn": lambda g: -g["per_min"], "top": lambda g: -(g["top_per_min"] or -1e9)}[a.sort]
    G.sort(key=key)
    if a.show is not None:
        show(G[a.show - 1], a.show, full=True)
        return
    print(f"{len(G)} setups with >= {a.min_runs} runs" + ("" if a.all else " (Cage / Doll / Might / Machines / Clockwork out)"))
    print("\n#  | Vlad/min | CN/min (med / top3) | net/map | steady | cost | s | deaths | lottery | trend | runs | setup")
    for k, g in enumerate(G[:a.top], 1):
        sig = " + ".join(short(s) for s in g["sig"]) + (f" + DSres{g['res']}" if g["res"] else "")
        tr = f"{g['trend7'] * 100:+.0f}%" if g["trend7"] is not None else "n/a"
        print(f"{k:2d} | {g['vlad_per_min']:6.1f} | {g['per_min']:5.1f} ({g['med_per_min']:4.0f} / {g['top_per_min']:4.0f}) | {g['net']:5.0f} | {g['steady']:5.0f} | {g['cost']:4.0f} | {g['secs']:4.0f} | {g['deaths']:4.2f} | {g['lottery']:4.0f} | {tr:>5} | {g['runs']:5d} | {sig[:95]} [{g['fam'][:18]}]")
    if a.json:
        json.dump([{k: v for k, v in g.items() if k not in ("rs", "loot", "cost_items")} for g in G], open(a.json, "w"), ensure_ascii=False, indent=0, default=str)


if __name__ == "__main__":
    main()
