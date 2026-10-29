"""Bottom-up Machines (Cruising Artifact) farm model: every slot / node / pet priced as marginal FE per map.

Drone drops split into: common fluorescent memories (+ Gaze lottery) which take the Drop Quantity pool, generic "additional",
fluorescent-specific "additional" and replications; the exclusive memory (Disappearing Shadow) which takes no pool and no
fluorescent-specific additional (XD matrix: Kong's +24% fluorescent line is 'none' on the exclusive, his replications 'yes').
Calibrated on the CN full stack (555 runs, ice/steel): per map 105 Secret of the Glacial Abyss, 0.5 Disappearing Shadow,
1.0 Tomorrow's Direction, 0.0063 Gaze, 21 FE. CN stack assumed: Cruising, Transgression (30 stacks), Strength in Numbers,
Focus or Colorful (Artifact), Fluorescent probe, tree +25% drones + Obtuse +40%, card x2, pets Kong/Sparks/Sky's Dome, pool ~110.
"""
TAX = 0.875
PRICE = dict(cruising=22, transgression=44.8, sin=1.0, colorful_art=8.0, colorful=0.908, focus=5.0, fluor_compass=0.313, fluor_probe=6.0,
             sinful=13.5, sinful_art=40.0, beacon=3.29, resonance=3.41, flourishing_probe=2.0)
# CN-measured yields per map (full stack)
CN = dict(secret=105 * 0.3, tomdir=1.0 * 6.71, other_common=5.0, gaze=0.0063 * 9666, exclusive=0.5 * 241, fe=21.0, generic=15.0)

def stack(opts):
    """opts: set of option names. Returns per-map multipliers for common (pool-applicable) and exclusive memories, relative to the CN stack."""
    pool_cn = 110.0 + 74.0          # resonance/micros + pets (Kong 18, Sparks 30, Dome 26)
    pool = 100 + 30 + 6 + (74 if "pets" in opts else 0) + (40 if "sinful" in opts else 0) + (80 if "sinful_art" in opts else 0) + (20 if "flourishing_probe" in opts else 0) + opts.get("extra_pool", 0) if isinstance(opts, dict) else 0
    return pool

def value(o):
    """o: dict of flags. Returns dict of FE/map (taxed) and the cost."""
    pool = 100 + 30 + 2 * o.get("prof_micros", 2) + o.get("commod_micros", 0) + (74 if o.get("pets", True) else 0) + 40 * o.get("sinful", 0) + 80 * o.get("sinful_art", 0) + (20 if o.get("flourishing_probe") else 0)
    pool_cn = 110 + 74
    gen_add = (1.9 if o.get("transgression", True) else 1) * (1.2 if o.get("sin", True) else 1) * (2 if o.get("cruising", True) else 0) * (1.25 if o.get("node25", True) else 1) * (1.4 if o.get("obtuse", True) else 1) * (1.164 if o.get("pets", True) else 1)
    gen_add_cn = 1.9 * 1.2 * 2 * 1.25 * 1.4 * 1.164
    fl_add = (1.24 if o.get("pets", True) else 1) * (1.24 if o.get("pets", True) else 1)          # Kong + Dome, common only
    fl_add_cn = 1.24 * 1.24
    # Replication [Vlad 2026-10-29, seen in game: 4- and 6-memory drops, never 5]: every "replicated once" source (incl. Kong's 20%,
    # Dome's 10%, Creation's 30% crystal buff, Colorful 50/20, probe 20) adds into ONE x2 chance capped at 100%; Kong's "replicated
    # 2 times" (13%) rolls per copy AFTER that (x3) -> expected x(1 + min(1, sum)) x 1.26.
    once = ((0.2 + 0.1) if o.get("pets", True) else 0) + (0.5 if o.get("colorful_art") else 0) + (0.2 if o.get("colorful") else 0) + (0.1 if o.get("fluor_compass") else 0) + (0.2 if o.get("fluor_probe", True) else 0) + (0.3 if o.get("creation", True) else 0)
    rep = (1 + min(1.0, once)) * (1.26 if o.get("pets", True) else 1)
    rep_cn = (1 + min(1.0, 0.3 + 0.25 + 0.2)) * 1.26     # CN: Kong 20 + Dome 10 + half Colorful(Artifact) + Fluorescent probe 20
    excl_focus = (1.5 if o.get("focus") else 1); excl_focus_cn = 1.25
    drones = o.get("drones", 1.0)          # tree: extra rounds / attackers vs the CN tree
    common = (CN["secret"] + CN["tomdir"] + CN["other_common"] + (CN["gaze"] if o.get("gaze", True) else 0)) * drones * ((1 + pool / 100) / (1 + pool_cn / 100)) * (gen_add / gen_add_cn) * (fl_add / fl_add_cn) * (rep / rep_cn)
    excl = CN["exclusive"] * drones * (gen_add / gen_add_cn) * (rep / rep_cn) * (excl_focus / excl_focus_cn)
    generic = (CN["fe"] + CN["generic"]) * ((1 + pool / 100) / (1 + pool_cn / 100)) * (1.2 if o.get("sin", True) else 1) / 1.2
    cost = PRICE["beacon"] + PRICE["resonance"] + sum(PRICE[k] for k in ("cruising", "transgression", "sin", "colorful_art", "colorful", "focus", "fluor_compass", "fluor_probe", "sinful", "sinful_art", "flourishing_probe") if o.get(k, k in ("cruising", "transgression", "sin", "fluor_probe")))
    cost -= 0.10 * sum(PRICE[k] for k in ("cruising", "transgression", "sin", "colorful_art", "colorful", "focus", "fluor_compass", "sinful", "sinful_art") if o.get(k, k in ("cruising", "transgression", "sin"))) if o.get("prof_refund", True) else 0
    gross = TAX * (common + excl) + generic   # FE untaxed inside generic approx
    return dict(common=TAX * common, excl=TAX * excl, generic=generic, gross=gross, cost=cost, net=gross - cost)

if __name__ == "__main__":
    base = dict(cruising=True, transgression=True, sin=True, colorful_art=True, fluor_probe=True, pets=True, gaze=True)
    b = value(base)
    print("BASE (Cruising + Transgression + Strength in Numbers + Colorful(Artifact), Fluorescent probe, Kong/Sparks/Dome):")
    print(f"   common+Gaze {b['common']:.0f}  exclusive {b['excl']:.0f}  generic {b['generic']:.0f}  gross {b['gross']:.0f}  cost {b['cost']:.1f}  NET {b['net']:.0f} FE/map")
    bg = value(dict(base, gaze=False)); print(f"   without the Gaze lottery: gross {bg['gross']:.0f} net {bg['net']:.0f}")
    print("\nMARGINAL value of each piece (net FE/map, base minus base-without-it):")
    for k, label in (("transgression", "Transgression Plunder (44.8 FE, x1.9 at 30 stacks)"), ("sin", "Strength in Numbers Soldier (1 FE, x1.2 normals)"), ("colorful_art", "Colorful Fluorescent (Artifact) (8 FE, 50% replicate)"), ("fluor_probe", "Fluorescent Profound Probe (6 FE, 20% replicate)"), ("pets", "the three pets together")):
        v = value(dict(base, **{k: False})); print(f"   {label:58s} +{b['net'] - v['net']:5.0f}   (gross +{b['gross'] - v['gross']:.0f}, cost {PRICE.get(k, 0)})")
    print("\nADDING to the base (needs a free slot):")
    for k, label in (("focus", "Focus Fluorescent (5 FE, x1.5 exclusive)"), ("colorful", "Colorful Fluorescent (0.9 FE, 20% replicate)"), ("fluor_compass", "Fluorescent Compass (0.3 FE, 10% replicate)"), ("sinful", "Sinful Plunder (13.5 FE, +40 pool)"), ("sinful_art", "Sinful Plunder (Artifact) (40 FE, +80 pool)")):
        v = value(dict(base, **{k: True})); print(f"   {label:58s} {v['net'] - b['net']:+5.0f}")
    print("\nSWAPS within 4 slots (Cruising fixed):")
    for name, o in (("Trans + SiN + ColA (base)", base), ("Trans + SiN + Focus", dict(base, colorful_art=False, focus=True)), ("Trans + ColA + Focus (no SiN)", dict(base, sin=False, focus=True)),
                    ("SiN + ColA + Focus (no Transgression)", dict(base, transgression=False, focus=True)), ("Trans + ColA + Colorful (no SiN)", dict(base, sin=False, colorful=True)), ("Trans + SiN + Sinful(Art) (no ColA)", dict(base, colorful_art=False, sinful_art=1))):
        v = value(o); print(f"   {name:42s} net {v['net']:5.0f}  (gross {v['gross']:.0f}, cost {v['cost']:.0f})")
