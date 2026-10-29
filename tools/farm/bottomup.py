"""Bottom-up Profound farming model.

Every CN strategy (629, 46k runs) is decoded into: instance columns (each compass / astrolabe key it consumed per map, or a
mechanic forced by its Void Chart appearance nodes, plus 'generic' = the plane's own monsters) and, per column, the multipliers
its own setup gave that column: generic quantity pool (resonance, Profound, Commodities, Sinful Plunder, Flourishing probe) x 2
(card) where XD says quantity applies, the mechanic's "additional" nodes / compass lines, compass-class multipliers (Compass
constellation, Ecliptics, Compass probe), fluorescent replication, ember lines.
Then per item, NNLS:  loot[s][i] = sum_k y[i][k] * X[s][k][class(i)]   -> y = items per instance per map with every multiplier = 1.
A strategy for Vlad is priced by re-applying HIS multipliers to those naked yields.
Pets are not logged on etor: the yields carry the CN average pets; Vlad's pets are assumed comparable (rank 6 drop pets).
"""
import collections, math, re, json, os, sys
import numpy as np
from scipy.optimize import nnls
import runs as RN, mech

FE = "100300"
TAX = 0.875
RES_CURVE = [(0, 15), (1, 30), (3, 45), (7, 60), (15, 75), (31, 100)]
def res_bonus(n):
    if n >= 31: return 100.0
    for (a, va), (b, vb) in zip(RES_CURVE, RES_CURVE[1:]):
        if a <= n <= b: return va + (vb - va) * (n - a) / (b - a)
    return 15.0

# --- which gameplay ignores the generic Drop Quantity pool (XD pactspirit matrix: "+X% Drop Quantity" pet lines = none) ---
NQ_MECH = {"Vorax", "Sandlord", "Mistville", "FrozenCanvas", "Overrealm"}
NQ_ITEMS = {"Disappearing_Shadow"}
# Exclusive Fluorescent Memories (Focus Fluorescent Compass: +50% chance): plane-exclusive + gameplay-exclusive [tlidb]
EXCL_MEMORIES = {"Disappearing_Shadow", "Immolating_World", "Concoction_Recipe", "Immortality_Concoction_Recipe", "Antonius_Research", "Antoniuss_Help", "Clergys_Thinking",
                 "Silent_Avowal", "Tyrants_Iron_Fist", "Silent_Monologue", "Blade-dancers_Fingers", "Illusory_Chimera", "Corrupted_Axis", "Glorious_Axis", "Inheritance_Axis"}

# --- item classes (for class multipliers) ---
def item_class(i):
    t = RN.typ(i); n = RN.name(i)
    if t in ("罗盘", "星盘"): return "compass"
    if t == "探针": return "probe"
    if t == "记忆荧光": return "fluor"
    if t == "灰烬": return "ember"
    if t == "信标": return "beacon"
    if t in ("传奇装备", "装备蓝图"): return "legendary"
    return "other"

# --- multiplier compasses / probes (not instances) ---
POOL_COMPASS = {"Sinful_Plunder_Compass": 40, "Sinful_Plunder_Compass_%28Artifact%29": 80, "Flourishing_Profound_Probe": 20}
COMPASS_ADD = {"Ecliptic_Astrolabe": 15, "Vast_Ecliptic_Astrolabe": 30, "Ascendant_Ecliptic_Astrolabe": 30, "Compass_Profound_Probe": 20}
FLUOR_REP = {"Fluorescent_Compass": 10, "Colorful_Fluorescent_Compass": 20, "Colorful_Fluorescent_Compass_%28Artifact%29": 50, "Fluorescent_Profound_Probe": 20}
EMBER_ADD = {"Ember_Compass": 30, "Bounty_Ember_Compass": 50, "Ember_Profound_Probe": 20}
GEAR_ADD = {"Gear_Profound_Probe": 20}
TRANSGRESSION = {"Transgression_Plunder_Compass": 90}      # +3% additional for Normal monsters x 30 stacks [Vlad: always 30]
NON_INSTANCE = set(POOL_COMPASS) | set(COMPASS_ADD) | set(FLUOR_REP) | set(EMBER_ADD) | set(GEAR_ADD) | set(TRANSGRESSION) | {"Focus_Fluorescent_Compass", "Novel_Compass", "Lavish_Novel_Compass", "Conquering_Novel_Compass", "Renown_Edge_Compass", "Reserve_Ember_Compass", "Beacon_Profound_Probe"}

# --- mechanic "additional drop quantity" lines (nodes and compasses), per mechanic: list of (regex, kind) ---
# kind 'add' -> multiplies (1 + x/100) per node; 'addper' -> x per stack * STACKS; 'inst' -> multiplies the instance count
ADD_RULES = {
    "Afterlight": [(r"\+(\d+)% additional Drop Quantity (?:for|in) the Vigil", "add"), (r"\+(\d+)% additional Drop Quantity in Vigil gameplay for each stack of Fright", "add3")],
    "Overrealm": [(r"\+([\d.]+)% additional Drop Quantity in the Overrealm", "add")],
    "Lunaria": [(r"\+(\d+)% additional Drop Quantity for Lunaria gameplay", "add"), (r"\+(\d+)% additional Drop Quantity when Combo reaches 11", "add"), (r"\+(\d+)% additional Drop Quantity for Lunari monsters", "add")],
    "Outlaw": [(r"\+(\d+)% additional Drop Quantity for all Security personnel(?! after)", "add"), (r"\+(\d+)% additional Drop Quantity for all Security personnel after activating", "add"), (r"\+(\d+)% additional Drop Quantity for the Outlaw gameplay", "add"), (r"-(\d+)% additional Drop Quantity for all Security personnel", "sub")],
    "Machines": [(r"\+(\d+)% additional Drop Quantity during Trial: God of Machines", "add"), (r"\+(\d+)% additional Drop Quantity at the start of each round", "add"), (r"\+(\d+)% additional Drop Quantity for Drones", "add"), (r"-(\d+)% additional Drop Quantity during Trial: God of Machines", "sub"),
                 (r"\+(\d+)% chance to have 1 additional attack round", "inst_pct3"), (r"number of attacking monsters during Trial: God of Machines \+([\d.]+)%", "inst_pct"), (r"2 echelon\(s\) of Drones will show up", "inst2"), (r"2 additional echelons of Drones", "inst2"), (r"several additional echelons of Drones", "inst_dull")],
    "Hunting": [(r"\+(\d+)% additional Drop Quantity for Safari bosses' Hunting Rewards", "add"), (r"\+(\d+)% additional Drop Quantity for Stage Final Boss's Hunting Rewards(?! for every)", "addfb"),
                (r"\+([\d.]+)% additional Drop Quantity for Stage Final Bosses' Hunting Rewards(?: and [^·]*)? for every 1 Safari Boss defeated", "addfb_stack"), (r"(\d+) Safari Boss\(es\) will appear", "safari_n"),
                (r"(\d+)% chance for 2 additional Safari Boss", "safari_2x"), (r"(\d+)% chance for 6 additional Safari Boss", "safari_6x"), (r"Trial: Goddess of Hunting is replaced by Trial: Goddess of Hunting \(Safari\)", "safari_mode"),
                (r"(\d+)% chance to replicate Stage Final Bosses", "fb_rep"), (r"100% chance to replicate the Stage Final Boss", "fb_rep100")],
    "ClockworkBallet": [(r"increases the chance for Compass Cogwheels to drop from Clockwork Ballet Games by (\d+)%", "cog"), (r"final reward to get \+(\d+)% Drop Quantity", "add"), (r"SSS Rating is enhanced: \+(\d+)% Drop Quantity", "add"), (r"default quantity of Cogwheels in Clockwork Ballet Games \+1", "add8")],
    "Creation": [(r"\+(\d+)% additional Creation Engine Drop Quantity", "add"), (r"-(\d+)% additional Creation Engine Drop Quantity", "sub"), (r"\+(\d+)% chance to generate 1 additional Creation Engine", "inst_pct_half"), (r"(\d+) additional Creation Engine\(s\) appear", "inst_plus_half"), (r"Significantly increases Creation Engine Quantity", "inst2")],
    "Vorax": [(r"\+([\d.]+)% additional Drop Quantity from Vorax-infected monsters", "add"), (r"\+(\d+)% chance for 1 group of Vorax-infected monsters to appear", "inst_pct_q")],
    "Might": [(r"\+(\d+)% additional Drop Quantity (?:during Trial: God of Might|for Trial: God of Might and Dwarven Automatons)", "add"), (r"-(\d+)% additional Drop Quantity during Trial: God of Might", "sub"), (r"\+(\d+)% chance for 1 additional trial monster", "inst_pct"), (r"\+(\d+) to the Max Level in Trial: God of Might", "lvl"), (r"\+(\d+)% additional Drop Quantity during Trial: God of Might$", "add")],
    "DarkSurge": [(r"Corrosion Energy granted by monsters Corroded by Dark Surge \+(\d+)%", "inst_pct"), (r"Corrosion Energy granted by monsters Corroded by Dark Surge is significantly reduced", "ds_cap")],
    "Arcana": [(r"\+(\d+)% chance for Notes of Arcana to drop", "notes"), (r"(\d+) additional Tarot Trial\(s\) appear", "inst_plus_1")],
    "Cube": [(r"\+(\d+)% additional Drop Quantity for Malice Incarnations", "add"), (r"-(\d+)% additional Desire Crystal Drop Quantity", "sub")],
    "Sandlord": [(r"Oasis Coins dropped have a (\d+)% chance to be replicated once", "rep"), (r"(\d+)% chance for 1 additional wave", "inst_pct")],
    "Aeterna": [(r"Aeterna Reverberations dropped by Kins of Aeterna have a (\d+)% chance to be replicated once", "rep")],
    "Mistville": [(r"Resident's Eyes dropped by Mistville \"Residents\" have a (\d+)% chance to be replicated once", "rep"), (r"\+(\d+)% chance for 1 additional Mistville Resident", "inst_pct")],
    "FrozenCanvas": [(r"Snowpaper Fragments dropped have a (\d+)% chance to be replicated once", "rep")],
    "Blacksail": [(r"Void Sea Treasure drops to be replicated 1 additional time", "rep3")],
    "Cage": [(r"\+(\d+)% additional Drop Quantity for Cages of Original Sin", "add")],
    "War": [(r"Trial: God of War's Duration\+(\d+)%", "inst_pct"), (r"\+(\d+)% God of War Trial Duration", "inst_pct")],
    "Gods": [],
}
APPEAR = {  # constellation -> regex of the appearance nodes
    "Afterlight": r"\+(\d+)% chance for the Vigil gameplay to appear", "Overrealm": r"\+(\d+)% chance for the \"Door\" leading to the Overrealm to appear",
    "Lunaria": r"\+(\d+)% chance for lots of Lunar Stone Statues", "Outlaw": r"\+(\d+)% chance for a TOWER Transport Vehicle", "Machines": r"\+(\d+)% chance for Trial: God of Machines to appear",
    "Hunting": r"\+(\d+)% chance for Trial: Goddess of Hunting to appear", "ClockworkBallet": r"\+(\d+)% chance for Clockwork Ballet Games to appear", "Creation": r"\+(\d+)% chance for Creation Engines to appear",
    "Vorax": r"\+(\d+)% chance for groups of Vorax-infected monsters to appear", "Might": r"\+(\d+)% chance for Trial: God of Might to appear", "DarkSurge": r"\+(\d+)% chance for Netherrealm stages to be completely flooded",
    "Arcana": r"\+(\d+)% chance for there to be tarot cards", "Cube": r"\+(\d+)% chance for Malice to be accumulating", "Sandlord": r"\+(\d+)% chance for Sand Pirates to appear", "Aeterna": r"\+(\d+)% chance for Kin of Aeterna",
    "Mistville": r"\+(\d+)% chance for Mistville", "FrozenCanvas": r"\+(\d+)% chance for a Dyed Snow Monster", "Blacksail": r"\+(\d+)% chance for Netherrealm stages to be marked by a Plane Anchor", "Nightmare": r"\+(\d+)% chance for Dream Lotuses",
    "War": r"\+(\d+)% chance for Trial: God of War to appear", "Cage": r"\+(\d+)% chance for Cages of Original Sin to appear",
}
COMPASS_TEXT = {}
def _load_compass_text():
    for page in ("Compass", "Probe"):
        d = json.load(open(os.path.join(RN.ROOT, "data", "catalog", f"{page}.json")))
        for c in d["cards"]:
            for e in c.get("entries", []):
                COMPASS_TEXT[e["key"].replace("(", "%28").replace(")", "%29")] = " · ".join(e["lines"])
_load_compass_text()
def ctext(key): return COMPASS_TEXT.get(key, "")

class Setup:
    """Everything the multipliers need, for a CN strategy (from its logged cost + nodes) or for a planned setup."""
    def __init__(self, resonance=31, compasses=None, probes=None, nodes=None, prof_major_q=0):
        self.res = resonance; self.compasses = compasses or {}; self.probes = probes or {}
        self.nodes = nodes or []                 # [(mechanic_or_constellation, text, count)]
        self.prof_major_q = prof_major_q
    @staticmethod
    def from_strategy(r):
        comp, prob = {}, {}
        for i, q in r["cost"].items():
            k = RN.name(i); t = RN.typ(i)
            if t in ("罗盘", "星盘"): comp[k] = comp.get(k, 0) + q
            elif t == "探针": prob[k] = prob.get(k, 0) + q
        nodes = [(mech.CONSTELLATION.get(c, c), " · ".join(n["lines"]), cnt) for c, n, cnt in r["nodes"]]
        return Setup(resonance=r["cost"].get("5028", 0.0), compasses=comp, probes=prob, nodes=nodes)
    def all_lines(self):
        for m, txt, cnt in self.nodes: yield m, txt, cnt
        for k, q in list(self.compasses.items()) + list(self.probes.items()):
            yield mech.compass_family(k) or "?", ctext(k), q
    # --- generic pool ---
    def pool(self):
        q = res_bonus(self.res)
        for k, v in POOL_COMPASS.items(): q += v * (self.compasses.get(k, 0) + self.probes.get(k, 0))
        for m, txt, cnt in self.nodes:
            mm = re.search(r"In Netherrealm stages, \+(\d+)% Drop Quantity$", txt)
            if mm and m in ("generic:commodities", "Profound"): q += float(mm.group(1)) * cnt
            if m == "Profound" and "+25% Drop Quantity" in txt: q += 30.0 * cnt          # [Vlad] 30% in game
        return q
    def generic_add(self):
        a = 2.0                                                                            # the Confusion card's +100% additional
        for m, txt, cnt in self.nodes:
            if m == "Profound" and "+12% additional Drop Quantity" in txt: a *= 1.12 ** cnt
            if m == "Profound" and "-50% additional Drop Quantity" in txt: a *= 0.5 ** cnt
        return a
    def Qg(self): return (1 + self.pool() / 100) * self.generic_add()
    # --- class multipliers ---
    def compass_mult(self):
        a = 1.0; rep = 0.0
        for m, txt, cnt in self.all_lines():
            for mm in re.finditer(r"\+([\d.]+)% additional Compass Drop Quantity(?! for each)", txt): a *= (1 + float(mm.group(1)) / 100) ** cnt
            mm = re.search(r"\+([\d.]+)% additional Compass Drop Quantity for each Compass inserted", txt)
            if mm: a *= (1 + float(mm.group(1)) / 100 * sum(self.compasses.values())) ** cnt
            mm = re.search(r"Compasses dropped(?: from [^·]*)? have a (\d+)% chance to be replicated once", txt)
            if mm: rep += float(mm.group(1)) * cnt
        return a * (1 + min(1.0, rep / 100))
    def fluor_mult(self):
        rep = 0.0
        for k, v in FLUOR_REP.items(): rep += v * (self.compasses.get(k, 0) + self.probes.get(k, 0))
        return 1 + min(1.0, rep / 100)
    def excl_fluor_mult(self): return 1 + 0.5 * self.compasses.get("Focus_Fluorescent_Compass", 0)
    def transgression(self, M):
        t = sum(v * self.compasses.get(k, 0) for k, v in TRANSGRESSION.items())
        if t <= 0: return 1.0
        return 1 + t / 100 if M == "Machines" else (1 + 0.6 * t / 100 if M == "generic" else 1.0)
    def ember_mult(self, M="generic"):
        a = 1.0
        for k, v in EMBER_ADD.items(): a *= (1 + v / 100) ** (self.compasses.get(k, 0) + self.probes.get(k, 0))
        for m, txt, cnt in self.nodes:
            might = "Trial: God of Might" in txt
            if might and M != "Might": continue
            for mm in re.finditer(r"\+(\d+)% additional Ember Drop Quantity", txt): a *= (1 + float(mm.group(1)) / 100) ** cnt
            mm = re.search(r"Embers dropped(?: during Trial: God of Might)? have a (\d+)% chance to be replicated once", txt)
            if mm: a *= 1 + float(mm.group(1)) / 100 * cnt
        return a
    def gear_mult(self):
        a = 1.0
        for k, v in GEAR_ADD.items(): a *= (1 + v / 100) ** self.probes.get(k, 0)
        return a
    def class_mult(self, cls, M="generic"):
        return {"compass": self.compass_mult(), "fluor": self.fluor_mult(), "ember": self.ember_mult(M), "legendary": self.gear_mult()}.get(cls, 1.0)
    # --- mechanic multipliers ---
    def appear(self, M):
        rx = APPEAR.get(M); p = 0.0
        if not rx: return 0.0
        for m, txt, cnt in self.nodes:
            if m == M:
                mm = re.search(rx, txt)
                if mm: p += float(mm.group(1)) * cnt
        return min(100.0, p)
    def mech_mult(self, M):
        """(additional multiplier, instance multiplier) from this setup's nodes + compass lines for mechanic M."""
        add = 1.0; inst = 1.0; fb_add = 1.0; fb_stack = 0.0; safari = 0.0; safari_mode = False; fb_rep = 0.0; cog = 0.0; notes = 0.0; rep = 0.0; lvl = 0
        for m, txt, cnt in self.all_lines():
            if m != M: continue
            for rx, kind in ADD_RULES.get(M, []):
                for mm in re.finditer(rx, txt):
                    x = float(mm.group(1)) if mm.groups() else 0.0
                    if kind == "add": add *= (1 + x / 100) ** cnt
                    elif kind == "add3": add *= (1 + 3 * x / 100) ** cnt
                    elif kind == "add8": add *= 1.08 ** cnt
                    elif kind == "sub": add *= (1 - x / 100) ** cnt
                    elif kind == "inst_pct": inst *= (1 + x / 100) ** cnt
                    elif kind == "inst_pct3": inst *= (1 + x / 300) ** cnt
                    elif kind == "inst_pct_half": inst *= (1 + x / 200) ** cnt
                    elif kind == "inst_pct_q": inst *= (1 + x / 100 / 4) ** cnt
                    elif kind == "inst_plus_half": inst *= (1 + x / 2) ** cnt
                    elif kind == "inst_plus_1": inst *= (1 + x) ** cnt
                    elif kind == "inst2": inst *= 2.0 ** cnt
                    elif kind == "inst_dull": inst *= 1.6 ** cnt
                    elif kind == "addfb": fb_add *= (1 + x / 100) ** cnt
                    elif kind == "addfb_stack": fb_stack += x * cnt
                    elif kind == "safari_n": safari += x * cnt
                    elif kind == "safari_2x": safari += 2 * x / 100 * cnt
                    elif kind == "safari_6x": safari += 6 * x / 100 * cnt
                    elif kind == "safari_mode": safari_mode = True
                    elif kind == "fb_rep": fb_rep += x * cnt
                    elif kind == "fb_rep100": fb_rep += 100 * cnt
                    elif kind == "cog": cog += x * cnt
                    elif kind == "notes": notes += x * cnt
                    elif kind == "rep": rep += x * cnt
                    elif kind == "rep3": rep += 3 * cnt
                    elif kind == "lvl": lvl += x * cnt
                    elif kind == "ds_cap": inst *= 0.5
        if M == "Hunting":
            # Safari mode (Mistrustful card / Revelation): rewards scale with the number of Safari bosses (4 = Revelation's base) x their
            # additional; the final boss adds fb_add x (1 + stack% x min(15, bosses)) on top (weighted 1/4 of the column).
            fb = fb_add * (1 + fb_stack / 100 * min(15, safari)) * (1 + min(1, fb_rep / 100))
            self._hunt = dict(safari=safari, fb=fb, mode=safari_mode)
            if safari > 0: inst *= (safari / 4) * 0.75 + 0.25 * fb / add
            else: add *= fb
        if M == "ClockworkBallet": add *= (1 + cog / 100) ** 0.5   # cogwheel chance -> compass share of the final reward (concave, fitted shape)
        if rep: add *= 1 + min(1, rep / 100)
        if lvl: inst *= 1 + lvl / 10
        return add, inst

def columns(R):
    """Instance columns: compass keys used by >= 3 strategies, tree-forced mechanics, 'generic'."""
    cnt = collections.Counter()
    for r in R:
        for i, q in r["cost"].items():
            k = RN.name(i)
            if RN.typ(i) in ("罗盘", "星盘") and k not in NON_INSTANCE and q >= 0.3: cnt[k] += 1
    cols = ["generic"] + sorted(k for k, n in cnt.items() if n >= 3)
    cols += [f"tree:{M}" for M in APPEAR]
    return cols

def design(R, cols):
    """X[s][k] base multiplier (no class), plus per-strategy setup for class multipliers."""
    setups = [Setup.from_strategy(r) for r in R]
    X = np.zeros((len(R), len(cols)))
    for s, (r, st) in enumerate(zip(R, setups)):
        Qg = st.Qg()
        for j, k in enumerate(cols):
            if k == "generic": X[s, j] = Qg * st.transgression("generic"); continue
            if k.startswith("tree:"):
                M = k[5:]
                if any(mech.compass_family(c) == M for c in st.compasses): continue      # compass-forced: the compass column carries it
                inst = st.appear(M) / 100
                if inst <= 0: continue
            else:
                M = mech.compass_family(k) or "generic"; inst = st.compasses.get(k, 0)
                if inst < 0.3: continue
            add, im = st.mech_mult(M)
            X[s, j] = inst * im * add * st.transgression(M) * (1.0 if M in NQ_MECH else Qg)
    return X, setups

LOTTERY_MAX = 25      # items with fewer total drops than this across all 46k runs are lotteries: valued globally, not fitted

def lotteries(R):
    tot = collections.Counter(); runs = sum(r["count"] for r in R)
    for r in R:
        for i, q in r["loot"].items(): tot[i] += q * r["count"]
    L = {}
    for i, n in tot.items():
        if n < LOTTERY_MAX and (RN.price(i) or 0) > 0:
            L[i] = dict(drops=n, ev_per_map=val(i, n / runs), price=price(i))
    return L

def fit(R=None, min_runs_item=1):
    R = R or RN.load()
    cols = columns(R); X, setups = design(R, cols)
    W = np.sqrt(np.array([r["count"] for r in R]))
    L = lotteries(R)
    items = sorted({i for r in R for i in r["loot"] if (RN.price(i) or i == FE) and i not in L})
    Y = {}
    colM = ["generic" if k == "generic" else (k[5:] if k.startswith("tree:") else (mech.compass_family(k) or "generic")) for k in cols]
    cm = {}
    for cls in ("compass", "fluor", "ember", "legendary", "other", "probe", "beacon"):
        cm[cls] = np.array([[st.class_mult(cls, M) for M in colM] for st in setups])
    for i in items:
        cls = item_class(i); y = np.array([r["loot"].get(i, 0.0) for r in R])
        Xi = X * cm[cls]
        if RN.name(i) in NQ_ITEMS: Xi = Xi / np.array([st.Qg() for st in setups])[:, None]   # exclusive memory: pool does not apply
        if RN.name(i) in EXCL_MEMORIES: Xi = Xi * np.array([st.excl_fluor_mult() for st in setups])[:, None]
        b, _ = nnls(Xi * W[:, None], y * W)
        Y[i] = b
    return dict(cols=cols, Y=Y, R=R, X=X, setups=setups, items=items, lottery=L)

def price(i): return 1.0 if i == FE else (RN.price(i) or 0.0)
def val(i, q): return q * price(i) * (1.0 if i == FE else TAX)

def column_value(F, k, top=12):
    j = F["cols"].index(k); rows = []
    for i in F["items"]:
        q = F["Y"][i][j]
        if q > 0: rows.append((val(i, q), q, i))
    rows.sort(reverse=True)
    return sum(v for v, _, _ in rows), rows[:top]

def duration_fit(F):
    """seconds per map = base + sum_k t_k * instances (NNLS)."""
    R, cols = F["R"], F["cols"]; setups = F["setups"]
    X = np.zeros((len(R), len(cols)))
    for s, st in enumerate(setups):
        X[s, 0] = 1.0
        for j, k in enumerate(cols[1:], 1):
            if k.startswith("tree:"):
                M = k[5:]
                if any(mech.compass_family(c) == M for c in st.compasses): continue
                X[s, j] = st.appear(M) / 100
            else: X[s, j] = st.compasses.get(k, 0)
    y = np.array([r["dur_s"] for r in R]); W = np.sqrt(np.array([r["count"] for r in R]))
    t, _ = nnls(X * W[:, None], y * W)
    return dict(zip(cols, t))

if __name__ == "__main__":
    F = fit()
    cols = F["cols"]; R = F["R"]
    used = {k: int((F["X"][:, j] > 0).sum()) for j, k in enumerate(cols)}
    T = duration_fit(F)
    print(f"{len(R)} strategies, {len(cols)} columns; lottery items (< {LOTTERY_MAX} drops): {len(F['lottery'])}, global EV {sum(x['ev_per_map'] for x in F['lottery'].values()):.1f} FE/map")
    for i, x in sorted(F["lottery"].items(), key=lambda kv: -kv[1]["ev_per_map"])[:12]: print(f"     lottery {x['ev_per_map']:5.2f} FE/map  {x['drops']:5.0f} drops  {RN.name(i)[:40]} @ {x['price']:.0f}")
    print("\n== per-instance naked value at all multipliers = 1 (x pool x additional x class for a real map), and CN seconds per instance")
    for k in cols:
        if used[k] < 3: continue
        tot, rows = column_value(F, k)
        print(f"\n{k}: {tot:.1f} FE/instance  [{used[k]} strategies, {T.get(k, 0):.0f} s]")
        for v, q, i in rows[:8]: print(f"     {v:7.2f} FE  {q:9.3f}  {RN.name(i)[:44]:44s} {RN.typ(i)[:6]:6s} @ {price(i):.2f}")
