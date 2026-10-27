"""Warlock / Phantasmagoria / Lone Walker's scenario builder + tree helpers."""
import sys, copy, json, math
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..'))
import engine as E
B0, T0 = E.load()
BASE_DPS = E.dps(B0, T0)["dps"]
PAN = E.panels_data()
COLX = [96, 224, 352, 480, 608, 736, 864]; ROWY = [80, 176, 272, 368, 464]
def cells(key):
    p = PAN[key]; ty = {tuple(n["lines"]): n.get("type", "") for n in p["nodes"]}
    out = {}
    for c in p["layout"]:
        if c.get("slot") == "core": continue
        x, y = map(int, c["id"].split("_"))
        kind = ty.get(tuple(c["lines"]), "")
        kind = "L" if "Legendary" in kind else ("M" if "Medium" in kind else ("m" if "Micro" in kind else "?"))
        left = [cc for cc in c.get("connects", []) if int(cc.split("_")[0]) < x]
        out[c["id"]] = dict(id=c["id"], ci=COLX.index(x), ri=ROWY.index(y), gate=c.get("column_points") or 0,
                            mr=c.get("max_rank") or 1, kind=kind, left=left, lines=c["lines"])
    return out
PANELS = ["Goddess_of_Knowledge", "Magister", "Prophet", "Warlock"]
CELLS = {k: cells(k) for k in PANELS + ["Lich"]}
CORES = {"Goddess_of_Knowledge": "Acquaintance", "Magister": "Bunch", "Prophet": "Frozen Lotus", "Warlock": "Dirty Tricks"}
def valid(alloc, prism=None):
    """alloc: {panel: {nid: rank}}; prism: (panel, nid, ...) or None. Returns list of problems."""
    probs = []
    for k, nodes in alloc.items():
        tot = sum(nodes.values())
        if tot < 24: probs.append(f"{k} core needs 24, has {tot}")
        for nid, r in nodes.items():
            c = CELLS[k][nid]
            if r > c["mr"]: probs.append(f"{k} {nid} rank")
            if tot < c["gate"]: probs.append(f"{k} {nid} gate {c['gate']}")
            if c["left"] and not any(nodes.get(l, 0) >= CELLS[k][l]["mr"] or (prism and prism[0] == k and prism[1] == l) for l in c["left"]):   # left must be MAXED [Vlad]
                probs.append(f"{k} {nid} needs {c['left']}")
            if prism and prism[0] == k and prism[1] == nid: probs.append(f"{k} {nid} under prism")
    return probs
def area(prism):
    k, nid, W, H, c0, r0 = prism
    return [cid for cid, c in CELLS[k].items() if c0 <= c["ci"] < c0 + W and r0 <= c["ri"] < r0 + H and cid != nid]
KINDS = ("m",)   # which node kind the prism's compensation affix counts: ("m",) micro or ("M",) medium (Vlad: one or the other)
def prism_stats(alloc, prism, per=3.5):
    k = prism[0]; nodes = alloc.get(k, {})
    comp = sum(per * nodes.get(cid, 0) for cid in area(prism) if CELLS[k][cid]["kind"] in KINDS)
    legs = sum(1 for cid in area(prism) if CELLS[k][cid]["kind"] == "L" and nodes.get(cid, 0) > 0)
    return comp, legs
def placements(k, shapes=("3x4", "4x3")):
    """Vlad: 3x4 = 1 column left, 1 right, 1 row above, 2 below. 4x3 = 1 left, 2 right, 1 above, 1 below."""
    out = []
    for nid, c in CELLS[k].items():
        for sh in shapes:
            W, H = (3, 4) if sh == "3x4" else (4, 3)
            c0, r0 = c["ci"] - 1, c["ri"] - 1
            if c0 < 0 or r0 < 0 or c0 + W > 7 or r0 + H > 5: continue
            out.append((k, nid, W, H, c0, r0))
    return out
def current_alloc():
    tr = json.load(open(''+__import__('os').path.join(__import__('os').path.dirname(__file__), '..', '..', 'ss14', 'thea', 'trees.json')+''))
    return {pa["panel"]: dict(pa["nodes"]) for pa in tr["panels"] if pa["panel"] != "Lich"}

# ---------------------------------------------------------------- scenario build
def build_new(alloc, comp, ped_core="Impermanence", roll=27, freed="Precise: Weapon Amplification", int_loss=77, me_charges=2,
              lw=True, keep_lich=False, otbt=False, extra_effects=()):
    b = copy.deepcopy(B0)
    trees = {"panels": []}
    for k, nodes in alloc.items():
        trees["panels"].append({"panel": k, "core": CORES.get(k), "nodes": dict(nodes)})
    # Pedigree: Defensiveness (Lv.2) + Lv.1 damage core; no more Dirty Tricks effect
    ped = next(s for s in b["slates"] if s["name"].startswith("Pedigree"))
    ped["lines"] = ["+25% Block Ratio"]
    ped["effects"] = []
    if ped_core == "Impermanence": ped["effects"] = [{"key": "special.impermanence", "value": 1, "why": "Impermanence"}]
    elif ped_core == "Insight": ped["lines"].append("+30% additional Spell Damage")          # skill cost irrelevant: Frozen Lotus
    elif ped_core == "Blunt": ped["lines"].append("+30% additional Physical Damage")
    elif ped_core == "Third": ped["effects"] = [{"key": "cast.inc", "value": 21, "why": "Third time's a charm (3 stacks)"}]
    if ped_core == "Third": b["context"]["hasten"] = True
    if lw:
        b["gear"] = [g for g in b["gear"] if g["slot"] != "boots"] + [{"slot": "boots", "name": "Lone Walker's Boots", "lines": ["+50% Movement Speed"],
            "effects": [{"key": "aura.effect", "value": roll + 2 * math.floor(comp / 3 + 1e-9), "why": f"LW roll {roll} + comp {comp:.1f}"}]}]
        b["granted_auras"] = [{"name": "Spell Amplification", "precise": True, "level": 20}]
        o = []
        for x in b["skills"]["others"]:
            if x.startswith("Spell Amplification"): x = f"{freed} [Aura Amplification, Restrain]"
            elif x.startswith("Precise Projectiles"): x = "Precise Projectiles [Aura Amplification, Restrain]"
            elif x.startswith("Domain Expansion"): x = "Domain Expansion [Aura Amplification, Restrain]"
            o.append(x)
        b["skills"]["others"] = o
        if ped_core != "Third": b["context"]["hasten"] = False
        b["kismets"]["lines"] = [f"+{152 - int_loss} Intelligence"] + b["kismets"]["lines"][1:]
    b["context"]["off_the_beaten_track"] = otbt
    b["context"]["mass_effect_charges"] = me_charges
    for e in extra_effects:
        b["gear"].append({"slot": "_x", "name": "x", "lines": [], "effects": [e]})
    return b, trees
def evaluate(alloc, prism, **kw):
    comp, legs = prism_stats(alloc, prism) if prism else (0, 0)
    b, tr = build_new(alloc, comp, **kw)
    r = E.dps(b, tr)
    return r["dps"] / BASE_DPS, comp, legs, r
