"""Marginal upgrade comparison; does not overwrite equipped build checkpoints."""
import json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
BASE=0.40  # user's approximate native multiplier per damage aura
LOCAL=0.1225  # Aura Amplification 29, last support-level checkpoint
COMP=17.0
BOOT_ROLL=27.0
ES=5882.0
ES_MULT=1.72  # last confirmed global increased ES; no extra ES multipliers assumed
CAGE=(1.14**4)*1.25

def aura_product(global_effect, physical_fraction=1.0, b=BASE, local=LOCAL):
    # Four socketed auras: projectile, area, cold, physical. The physical
    # portion is converted to cold; flat cold added separately bypasses it.
    ordinary=1+b*(1+local+global_effect/100)
    weapon=1+physical_fraction*b*(1+local+global_effect/100)
    precise=1+.40*(1+global_effect/100) # granted Precise Spell 20, no supports
    return ordinary**3 * weapon * precise

old=(1+BASE*(1+LOCAL))**4
boot_effect=BOOT_ROLL+2*COMP/3
boot_product=aura_product(boot_effect)
out={
 'status':'Proposed upgrades; no purchases or authoritative equipment changes',
 'inputs':{'global_aura_effect':0,'global_compensation':COMP,'boots':'normal, Precise Spell 20, 27% aura effect','aura_model':'Four current auras approximated at 40% native each; four linked auras plus granted Precise Spell after swap','local_aura_amplification_assumption':LOCAL,'last_ES':ES,'last_global_ES_bonus':72,'lost_boot_item_ES':720,'current_Cage_skill_level_roll':0,'current_Cage_item_ES_range':[470,520]},
 'boots_global_aura_effect':boot_effect,
 'boots_damage_vs_current':boot_product/old,
 'boots_ES_using_last_checkpoint':ES-720*ES_MULT,
 'Cage_and_Frozen_Lotus_factor':CAGE,
 'Cage_dot_taken_factor':.93**4,
 'boots_gain_if_compensation_rounds_down_to_complete_3pct_groups':aura_product(BOOT_ROLL+2*math.floor(COMP/3))/old,
 'chests':[],
}
p=.7792; cd=5.14; malign=1.42
crit60=(1-p+p*(cd+.6)*malign)/(1-p+p*cd*malign)
out['free_suffix_60_crit_damage_factor']=crit60
for name,flat,percent,aura,comp in [('T2',280,46,14,12),('T1',400,66,20,20),('T0',520,86,26,26),('T0+',676,112,34,34)]:
    additional_effect=8+aura+2*comp/3
    final_effect=boot_effect+additional_effect
    aura_gain=aura_product(final_effect)/boot_product
    # If the +8% aura base replaces the +170 gear ES base, intrinsic=0.
    item_es=flat*(1+percent/100)
    row={'tier':name,'craft':{'aura_base':8,'flat_gear_ES':flat,'percent_gear_ES':percent,'ultimate_aura':aura,'ultimate_global_compensation':comp},'global_aura_effect':final_effect,'extra_aura_effect_from_chest':additional_effect,'aura_gain_vs_LW_Cage':aura_gain,'damage_vs_LW_Cage_empty_suffix':aura_gain/CAGE,'damage_vs_LW_Cage_with_60_crit_damage':aura_gain/CAGE*crit60,'damage_vs_original_with_60_crit_damage':aura_product(final_effect)/old/CAGE*crit60,'item_ES_if_170_base_replaced':item_es,'item_ES_if_170_base_retained':(170+flat)*(1+percent/100),'total_ES_range_if_base_replaced':[ES+(-720+item_es-old_item)*ES_MULT for old_item in [520,470]],'total_ES_range_if_base_retained':[ES+(-720+(170+flat)*(1+percent/100)-old_item)*ES_MULT for old_item in [520,470]]}
    out['chests'].append(row)

lo,hi=0.,150.
for _ in range(80):
    mid=(lo+hi)/2
    if aura_product(boot_effect+mid)/boot_product<CAGE:lo=mid
    else:hi=mid
out['chest_extra_aura_effect_needed_to_replace_Cage_empty_suffix']=hi
lo,hi=0.,150.
for _ in range(80):
    mid=(lo+hi)/2
    if aura_product(boot_effect+mid)/boot_product*crit60<CAGE:lo=mid
    else:hi=mid
out['chest_extra_aura_effect_needed_with_60_crit_damage']=hi
out['T1_additional_ES_instead_of_comp']={
 'global_aura_effect':boot_effect+28,
 'damage_vs_LW_Cage_with_60_crit_damage':aura_product(boot_effect+28)/boot_product/CAGE*crit60,
 'ES_range':[(ES+(-720+664-old_item)*ES_MULT)*1.15 for old_item in [520,470]]}
out['native_aura_strength_sensitivity']={str(b):aura_product(boot_effect,b=b)/((1+b*(1+LOCAL))**4) for b in [.35,.40,.45]}
out['physical_fraction_sensitivity']={str(f):aura_product(boot_effect,physical_fraction=f)/old for f in [1,.95,.9]}
out['reservation']={'mana_auras':3,'life_auras':1,'free_granted_aura':1,'mana_reserved_assuming_Restrain29_three_supports_OffTheBeatenTrack':3*.5*.95**3/(1+.17+.145),'mana_reserved_with_T1_20comp_chest':3*.5*.95**3/(1+.37+.145),'rare_chest_cost_note':'Changing Frozen Lotus to Extreme Coldness restores mana costs; check casts against the available mana and regeneration.'}
out['attribute_loss_sensitivity']={str(n):((1+.0075*(835-n)+.31)/(1+.0075*835+.31)) for n in [50,100]}
file=ROOT/'ss14_thea_lone_walkers_2026-10-25.json'
file.write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
