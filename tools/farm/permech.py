"""Per-mechanic pooled numbers from the logged Profound runs: signature loot, exclusive jackpots, cost, CN time."""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN, mech, features as F, groups as GR
RN.PRICES["100300"] = {"id": "100300", "price_fe": 1.0}
SIG = {"Afterlight": {"divinity"}, "Lunaria": {"lunar"}, "Overrealm": {"prism"}, "DarkSurge": {"darksurge"}, "Outlaw": {"outlaw"}, "Arcana": {"destiny"},
       "Vorax": {"vorax"}, "Machines": {"fluor"}, "Might": {"ember"}, "Hunting": {"compass"}, "ClockworkBallet": {"compass"}, "Mistville": {"medium", "mistville"},
       "FrozenCanvas": {"noble", "magnif", "canvas"}, "Sandlord": {"spice", "probe"}, "War": {"beacon"}, "Gods": {"emblem"}, "Creation": {"fluor"},
       "Aeterna": {"aeterna"}, "Cube": {"cube"}, "Blacksail": {"blacksail"}, "Nightmare": set()}
EXCL = {"Lunaria": {"Omni-Elixir_Notes", "Iron_Nest"}, "Overrealm": {"Inverse_Image", "Gaze_Upon_the_Reflection"}, "Arcana": {"Undetermined_Fate"},
        "DarkSurge": {"Blueprint_Eternity", "Blueprint_Pantheons_Elegy", "Blueprint_Lone_Walkers_Boots"}, "Might": {"Blueprint_Eternity", "Blueprint_Pantheons_Elegy", "Blueprint_Lone_Walkers_Boots"}}

def mechanics_of(r, f):
    fams = set(GR.forced(r))
    for k, v in f.items():
        if k.startswith("t:") and v >= 15 and not k[2:].startswith("generic") and k[2:] != "Profound": fams.add(k[2:])
    return fams

def table():
    R = RN.load()
    M = collections.defaultdict(lambda: dict(runs=0, sig=0.0, excl=0.0, glob=0.0, generic=0.0, cost=0.0, dur=0.0, Q=0.0, strats=0, cats=collections.Counter(), jack=collections.Counter()))
    for r in R:
        f = F.extract(r); mechs = mechanics_of(r, f); n = r["count"]
        if any(RN.name(i) == "Snowpaper_Fragment" for i in r["cost"]): continue
        for m in mechs | {"(all)"}:
            g = M[m]; g["runs"] += n; g["strats"] += 1; g["dur"] += r["dur_s"] * n; g["Q"] += f["Q"] * n
            for i, q in r["cost"].items():
                if RN.typ(i) in ("罗盘", "星盘") and mech.compass_family(RN.name(i)) == m: g["cost"] += RN.value(i, q, False) * n
            for i, q in r["loot"].items():
                v = RN.value(i, q) * n; c = GR.cat(i); nm = RN.name(i)
                if (RN.price(i) or 0) >= 1000:
                    g["jack"][nm] += v
                    if nm in EXCL.get(m, ()): g["excl"] += v
                    else: g["glob"] += v
                elif c in SIG.get(m, ()): g["sig"] += v; g["cats"][c] += v
                else: g["generic"] += v
    return M

if __name__ == "__main__":
    M = table()
    print(f"{'mechanic':16s} {'runs':>6s} {'str':>3s} {'Q':>4s} {'sig/run':>7s} {'excl':>5s} {'glob':>5s} {'generic':>7s} {'cost':>5s} {'CNmin':>5s} | signature cats | exclusive jackpots")
    for m, g in sorted(M.items(), key=lambda kv: -kv[1]["runs"]):
        n = g["runs"]
        if n < 100: continue
        cats = ", ".join(f"{c} {v/n:.0f}" for c, v in g["cats"].most_common(3))
        ex = ", ".join(f"{i[:16]} {v/n:.0f}" for i, v in g["jack"].most_common(4) if i in EXCL.get(m, ()))
        print(f"{m:16s} {n:6d} {g['strats']:3d} {g['Q']/n:4.1f} {g['sig']/n:7.1f} {g['excl']/n:5.0f} {g['glob']/n:5.0f} {g['generic']/n:7.1f} {g['cost']/n:5.0f} {g['dur']/n/60:5.2f} | {cats} | {ex}")
