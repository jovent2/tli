
import math
base = (498+831)/2                      # lv20 base, flat after 20
lvl = 1.10**10 * 1.08**6                 # lv36: 21-30 +10% each, 31+ +8% each
inc = 1 + 6.67
AA = 1.1225
m = {
 'attributes 791x0.75%': 1+0.0075*791,
 'Condensed Cold 20% x hit 20%': 1.20*1.20,
 'Lightchaser 20% x roll -16%': 1.20*0.84,
 'Spell Tangle': 1.25, 'Manifold': 1.20, 'Multiple Proj': 1.15,
 'Dormant x2': 1.80, 'NFE 2x10.5%': 1.105**2, 'Tangle Dmg Enh 34%': 1.34,
 'Witch 8%': 1.08, 'Dreamweaver 19% x 4%': 1.19*1.04, 'Acquaintance 25%': 1.25,
 'GoK slate#2 11.2%': 1.112, 'Lich sealed both 10%': 1.10,
 'Bunch 3%x8': 1.24, 'Focus 5%x8': 1.40, 'Agility 2%x4': 1.08,
 'Israfel 14%x8': 2.12, 'Frigid Domain': 1+0.39*AA, 'Spell Amp': 1+0.405*AA,
 'Precise Proj': 1+0.38*AA, 'Domain Exp': 1+0.36*AA,
 'Aim': 1+0.3825*1.9, 'SOU': 1+0.182*1.9,
 'Boon x2 (1.2*1.4)^2': (1.2*1.4)**2, 'Spell Aggression 7%': 1.07, 'Hunting after dash 14%': 1.14,
 'Cage 1.14^4': 1.14**4, 'Prophet vs Frozen': 1.10, 'Dirty Tricks 1.12^6': 1.12**6,
}
enemy = {
 'Frostbite 101 x 1.44': 1+1.01*1.44, 'Biting Cold 45.5%': 1.455, 'Deepened Curse 5%': 1.05,
 'Frail 15%': 1.15, 'Cold Infiltration 13%': 1.13,
 'res 30-24.8': 1-0.052, 'armor max 27273 nonphys 60% - 10% pen': 1-(0.5*0.6-0.10),
}
crit_chance = 0.763; crit_dmg = 4.58; malign = 1.42
crit = (1-crit_chance) + crit_chance*crit_dmg*malign
dbl = 4.0   # 204% -> quad on every hit (overflow capped at 100%)
ripple = 1.5
proj = sum(0.8**i for i in range(7))
cast = 1.54*(1+2.016)*1.07
tangles = 2

self_mult = math.prod(m.values()); enemy_mult = math.prod(enemy.values())
hit = base*lvl*inc*self_mult
print(f"base {base:.1f} x lvl {lvl:.3f} x inc {inc:.2f} = {base*lvl*inc:,.0f}")
print(f"self additional product = {self_mult:,.1f}")
for k,v in m.items(): print(f"  {k:32s} x{v:.3f}")
print(f"enemy-side product = {enemy_mult:.3f}")
for k,v in enemy.items(): print(f"  {k:40s} x{v:.3f}")
print(f"avg hit per projectile before crit/double: {hit:,.0f}")
print(f"crit factor {crit:.3f} | double x{dbl} | ripple x{ripple} | projectiles x{proj:.3f}")
per_cast = hit*enemy_mult*crit*dbl*ripple*proj
print(f"per cast (7 proj): {per_cast:,.0f}")
print(f"casts/s per tangle {cast:.2f} x {tangles} = {cast*tangles:.2f}")
dps = per_cast*cast*tangles
print(f"DPS vs boss: {dps:,.0f}  ({dps/1e9:.2f} B)")
print(f"without ripple: {dps/1.5:,.0f} | with armor ignored: {dps/enemy['armor max 27273 nonphys 60% - 10% pen']:,.0f}")
