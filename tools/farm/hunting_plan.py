"""Node values for the Safari (Hunting) compass farm and the best 92-point allocation."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chart
C_SAFARI, C_FINAL, C_GENERIC, Q_LOOT = 88.0, 22.0, 12.0, 50.0   # FE/run at Vlad's baseline (CN-measured stack, Q 4.7)
C_ALL = C_SAFARI + C_FINAL + C_GENERIC
BOSSES = 4                                                          # Revelation astrolabe; each "2 Safari Bosses" medium adds 2

def v_compass(n):
    t = " · ".join(n["lines"])
    if n["name"] == "Initial Node": return 0
    m = re.search(r"\+([\d.]+)% additional Compass Drop Quantity", t)
    if m and "for each Compass inserted" in t: return 4 * float(m.group(1)) / 100 * C_ALL
    if m and "Cages" not in t: return float(m.group(1)) / 100 * C_ALL
    m = re.search(r"Compasses dropped have a ([\d.]+)% chance to be replicated", t)
    if m: return float(m.group(1)) / 100 * C_ALL
    m = re.search(r"([\d.]+)% chance to become (a more|the most) valuable", t)
    if m: return float(m.group(1)) / 100 * C_ALL * (0.5 if "more" in m.group(2) else 1.0)
    if "more likely to be" in t: return 0.8
    if "Giantism" in t: return 0.1
    return 0.0

def v_hunting(n):
    t = " · ".join(n["lines"]); nm = n["name"]
    if nm == "Initial Node": return 0
    if "replaced by Trial: Goddess of Hunting (Safari)" in t: return 1000.0       # Mistrustful: needed for Safari bosses
    if "2 Safari Boss(es) will appear" in t: return 40.0
    m = re.search(r"\+([\d.]+)% additional Drop Quantity for Stage Final Bosses' Hunting Rewards for every 1 Safari Boss", t)
    if m: return float(m.group(1)) / 100 * 8 * C_FINAL
    m = re.search(r"\+([\d.]+)% additional Drop Quantity for Safari bosses' Hunting Rewards", t)
    if m: return float(m.group(1)) / 100 * C_SAFARI + float(m.group(1)) / 100 * C_FINAL
    m = re.search(r"Compasses dropped from Safari bosses' Hunting Rewards have a ([\d.]+)% chance to be replicated", t)
    if m: return float(m.group(1)) / 100 * C_SAFARI
    m = re.search(r"Probes dropped from Safari bosses' Hunting Rewards have a ([\d.]+)% chance", t)
    if m: return float(m.group(1)) / 100 * 2.0
    if "buff selection stage" in t: return 5.0
    m = re.search(r"([\d.]+)% chance to replicate Stage Final Bosses", t)
    if m: return float(m.group(1)) / 100 * C_FINAL
    if nm.startswith("Crafty"): return 4.0
    if nm.startswith("Deceitful"): return 4.0
    if nm.startswith("Cunning"): return 1.0
    if "Ghost to spawn" in t: return 1.0
    return 0.0

def v_commodities(n):
    t = " · ".join(n["lines"])
    m = re.search(r"\+([\d.]+)% Drop Quantity$", t)
    if m: return float(m.group(1)) / 236 * Q_LOOT          # additive pool at 236% -> marginal
    if "Netherrealm Resonance" in t and "chance to drop" in t:
        m = re.search(r"([\d.]+)% chance to drop (\d+) additional", t)
        if m: return float(m.group(1)) / 100 * int(m.group(2)) * 0.11
    m = re.search(r"Embers dropped have a ([\d.]+)% chance to be replicated", t)
    if m: return float(m.group(1)) / 100 * 4.0
    m = re.search(r"Flame Sand dropped has a ([\d.]+)% chance", t)
    if m: return float(m.group(1)) / 100 * 1.0
    return 0.0

if __name__ == "__main__":
    out = {}
    for key, fn, budget in (("Hunting_Talent_Constellation", v_hunting, 50), ("Compass_Talent_Constellation", v_compass, 60), ("Commodities_Talent_Constellation", v_commodities, 30)):
        res, nodes = chart.best_subtree(key, fn, budget); out[key] = (res, nodes)
        print(f"\n{key}: value by points")
        print("  " + " ".join(f"{k}:{res[k][0]:.0f}" for k in range(0, budget + 1, 2)))
    # combine: 92 points over the three
    H, Cc, Cm = out["Hunting_Talent_Constellation"][0], out["Compass_Talent_Constellation"][0], out["Commodities_Talent_Constellation"][0]
    best = None
    for h in range(0, 51):
        for c in range(0, 61):
            m = 92 - h - c
            if m < 0 or m > 30: continue
            v = H[h][0] + Cc[c][0] + Cm[m][0]
            if best is None or v > best[0]: best = (v, h, c, m)
    print("\nbest split of 92:", best)
    v, h, c, m = best
    for key, k in (("Hunting_Talent_Constellation", h), ("Compass_Talent_Constellation", c), ("Commodities_Talent_Constellation", m)):
        res, nodes = out[key]; chosen = res[k][1]
        import collections
        cnt = collections.Counter(" · ".join(nodes[i]["lines"])[:100] + f" [{nodes[i]['name']}]" for i in chosen if nodes[i]["name"] != "Initial Node")
        print(f"\n## {key} ({k} pts, value {res[k][0]:.0f} FE/run)")
        for txt, n in cnt.most_common(): print(f"  {n:2d} x {txt}")
        print("  node ids:", sorted(i for i in chosen if nodes[i]["name"] != "Initial Node"))
