"""Per-strategy features for the logged runs: quantity multiplier, compass usage by family/tier, constellation points, probe."""
import collections, re
import runs as RN, mech

RES_CURVE = [(0, 15), (1, 30), (3, 45), (7, 60), (15, 75), (31, 100)]   # resonance count -> +% Drop Quantity [Vlad]
def res_bonus(n):
    if n >= 31: return 100.0
    for (a, va), (b, vb) in zip(RES_CURVE, RES_CURVE[1:]):
        if a <= n <= b: return va + (vb - va) * (n - a) / (b - a)
    return 15.0

PLUNDER = {"Sinful_Plunder_Compass": 40, "Sinful_Plunder_Compass_%28Artifact%29": 80}
PROBE_Q = {"Flourishing_Profound_Probe": 20, "Flourishing_Deep_Space_Probe": 40}
TIER = {"artifact": 2, "enh": 1, "base": 0}

def tier(key):
    if "Artifact" in key: return "artifact"
    base_names = ("War_Compass", "Might_Compass", "Mechanical_Compass", "Dark_Surge_Compass", "Blacksail_Compass", "Cube_Compass", "Aeterna_Compass",
                  "Nightmare_Compass", "Folklore_Compass", "Frozen_Canvas_Compass", "Arcana_Compass", "Sandlord_Compass", "Outlaw_Compass", "Overrealm_Compass",
                  "Vorax_Compass", "Lunaria_Compass", "Creation_Compass", "Afterlight_Compass", "Vigil_Compass", "Hunting_Astrolabe", "Doll_Astrolabe",
                  "Cage_Astrolabe", "Ecliptic_Astrolabe", "Sinful_Plunder_Compass", "Novel_Compass", "Soldier_Compass", "Veteran_Compass", "Elite_Compass",
                  "Boss_Compass", "Beacon_Compass", "Militant_Compass", "Ember_Compass", "Fluorescent_Compass")
    return "base" if key in base_names else "enh"

def extract(r):
    f = collections.Counter()
    res = r["cost"].get("5028", 0.0); f["res_per_run"] = res
    q = res_bonus(res)
    for i, n in r["cost"].items():
        k = RN.name(i); t = RN.typ(i)
        if k in PLUNDER: q += PLUNDER[k] * n
        if k in PROBE_Q: q += PROBE_Q[k] * n
        if t == "探针": f["probe:" + k] += n
        if t in ("罗盘", "星盘"):
            fam = mech.compass_family(k)
            if fam: f[f"c:{fam}"] += n; f[f"ct:{fam}:{tier(k)}"] += n
        if t == "信标": f["beacons_per_run"] += n
    cons = collections.Counter(); micro_q = 0.0; prof_major_q = 0.0
    for c, node, cnt in r["nodes"]:
        m = mech.CONSTELLATION.get(c, c)
        cons[m] += cnt
        txt = " ".join(node["lines"])
        mm = re.search(r"\+(\d+)% Drop Quantity$", txt.split(" · ")[0]) if node["name"] == "Micro Node" else None
        if node["name"] == "Micro Node" and re.search(r"In Netherrealm stages, \+(\d+(?:\.\d+)?)% Drop Quantity$", txt):
            micro_q += float(re.search(r"\+(\d+(?:\.\d+)?)% Drop Quantity", txt).group(1)) * cnt
        if node["name"] == "Major Node" and "+25% Drop Quantity" in txt: prof_major_q += 30.0 * cnt   # Vlad: 30% in game
    q += micro_q + prof_major_q
    for m, pts in cons.items(): f[f"t:{m}"] = pts
    f["Q"] = (1 + q / 100) * 2.0        # x2 = the Confusion card's +100% additional (assumed every map)
    return f
