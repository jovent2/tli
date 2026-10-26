
# Thea SS14 stat page, conditions: hitting a dummy, 8 Focus, 4 Agility, 2 active tangles, Euphoria x2, Spell Aggression, Boon x2
INT, STR, DEX = 594, 99+45+8, 45
attr = INT+STR+DEX

dmg = dict(GoK_micro=27, GoK_medium=54, Lich_micro=27, GoK_focus_micro=30, belt=47, ringL=64, ringR=81)
spell = dict(GoK_micro=27, Magister_focus=30, wandM=40+67, wandS=40+75)
ele = dict(wandM=106, Dreamweaver_page=36)
proj = dict(IronLion=40)
print("DAMAGE % :", sum(dmg.values()), dmg)
print("SPELL %  :", sum(spell.values()), spell)
print("ELE/COLD%:", sum(ele.values()), ele, " cold-specific: 0")
print("PROJ %   :", sum(proj.values()))
print("PHYS %   : 0")
print("TOTAL increased applying to the hit:", sum(dmg.values())+sum(spell.values())+sum(ele.values())+sum(proj.values()))

AA = 1.1225  # Aura Amplification lv29
auras = dict(SpellAmp30=39*0 + 40.5, FrigidDomain27=39, PreciseProj25=38, DomainExp25=36)
auras_eff = {k: round(v*AA,1) for k,v in auras.items()}
print("AURAS (x1.1225):", auras_eff)
add_cold = [("Israfel 14%x8",112), ("Frigid Domain", auras_eff["FrigidDomain27"])]
print("ADDITIONAL COLD %:", add_cold, "product", round((2.12)*(1+auras_eff['FrigidDomain27']/100),3))

cast = dict(GoK=27, Magister_focus=12, Lich=24, memories=32, wandS=25, wandS_base=16, Agility4=16, SOU=round(24*1.9,1), Aim=-16)
cast_inc = sum(cast.values())
cast_final = 1.54*(1+cast_inc/100)*1.07
print("CAST SPEED increased:", cast_inc, cast, "| x1.07 aggression | casts/s per tangle:", round(cast_final,2), "| 2 tangles:", round(2*cast_final,2))

crit_flat = 500 + 155*2
crit_inc = dict(tree=420, Witch=89, memory=104, wandS=166, ringL=120, slates=20+28)
crit_rating = crit_flat*(1+sum(crit_inc.values())/100)
print("CRIT RATING: flat", crit_flat, "increased", sum(crit_inc.values()), crit_inc, "-> rating", round(crit_rating), "chance", round(crit_rating/100,1), "%")
chd = dict(tree=60, slates=12, mem_cold=47, mem_spell=41+54, Israfel=8, Magister_leg=40, Hunting=21)
print("CRIT DMG: 150 base +", sum(chd.values()), "=", 150+sum(chd.values()), "%", chd)

ps = dict(memories=80, IronLion=28, Hunting=round(24*1.4,1), PreciseProjAura=round(10*AA,1))
print("PROJ SPEED increased:", sum(ps.values()), "x1.30 Lightchaser ->", round((1+sum(ps.values())/100)*1.3,2), "x")
print("COLD PEN: 24.8 (Dreamweaver 8+4.8+12) | ARMOR PEN: 10 (ring)")
print("SKILL EFFECT DURATION: 60.6 (neck40 mem10 Purity5 slate5.6) | CDR: 15.7 (slate 11.2 + Lich 4.5), Boon +50% additional")

for g in (120,146):
    gear = (120+347)+(170+338)+(g+349)+(146+304)*1.6
    flat = 220+221+210+642
    pct = 51 + INT*0.05
    print(f"ES (gloves base {g}): gear {gear:.0f} + flat {flat} = {gear+flat:.0f} x {1+pct/100:.3f} = {(gear+flat)*(1+pct/100):.0f}")
res = dict(fire=12+22+27, cold=12+17+30, lightning=19+19+18, erosion=16+27)
print("RES raw:", res, "| minus 60 (lv48/58/80):", {k:v-60 for k,v in res.items()})
print("ATTR total", attr, "-> Lightchaser x", round(1+0.0075*attr,2))
