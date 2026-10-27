import sys, json, copy
sys.path.insert(0, __import__('os').path.dirname(__file__))
import scen as S
def decomp(alloc, prism, roll=27, freed="Precise: Weapon Amplification", ped="Impermanence"):
    comp, legs = S.prism_stats(alloc, prism)
    rows = []
    def run(label, **kw):
        b, tr = S.build_new(alloc, comp, **kw)
        r = S.E.dps(b, tr); rows.append((label, r["dps"] / S.BASE_DPS, r["sheet"]))
    S.CORES["Prophet"] = "Spell Ripple"
    run("Lich -> Warlock (+spare points), Pedigree = Defensiveness only", lw=False, ped_core=None)
    S.CORES["Prophet"] = "Frozen Lotus"
    run("+ Spell Ripple out, Frozen Lotus back (Phantasmagoria in)", lw=False, ped_core=None)
    run(f"+ Lone Walker's ({roll}% roll + {comp:.0f}% comp), {freed}, -77 INT, no Hasten", lw=True, ped_core=None, roll=roll, freed=freed)
    run(f"+ Pedigree Lv.1 core: {ped}", lw=True, ped_core=ped, roll=roll, freed=freed)
    prev = 1.0
    for label, x, sh in rows:
        print(f"  x{x:6.3f}  (step x{x/prev:5.3f})  {label}"); prev = x
    sh = rows[-1][2]
    print(f"  sheet: lvl {sh['level_chromatic']}, INT {sh['INT']:.0f}, crit {sh['crit_chance']:.1f}% / {sh['crit_damage']:.0f}%, cast {sh['cast_speed']:.0f}, CDR {sh['cdr']:.1f}, dur {sh['duration']:.0f}, boon margin {sh['boon_margin']:.3f}, Focus {sh['max_focus']}")
    return rows
