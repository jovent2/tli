"""Mechanic classification of compasses / astrolabes / probes and of Void Chart constellations."""
import re
# compass key (tlidb) -> mechanic family; generic quantity/monster compasses -> 'generic:<kind>'
FAMILIES = [
    ("Vigil", "Afterlight"), ("Afterlight", "Afterlight"), ("Overrealm", "Overrealm"), ("Dark_Surge", "DarkSurge"),
    ("Lunaria", "Lunaria"), ("Vorax", "Vorax"), ("Creation", "Creation"), ("Outlaw", "Outlaw"), ("Sandlord", "Sandlord"),
    ("Arcana", "Arcana"), ("Frozen_Canvas", "FrozenCanvas"), ("Folklore", "Mistville"), ("Nightmare", "Nightmare"),
    ("Aeterna", "Aeterna"), ("Cube", "Cube"), ("Blacksail", "Blacksail"), ("Mechanical", "Machines"), ("Might", "Might"),
    ("War_Compass", "War"), ("Hunting_Astrolabe", "Hunting"), ("Doll_Astrolabe", "ClockworkBallet"), ("Cage_Astrolabe", "Cage"),
    ("Gods_Compass", "Gods"), ("Ecliptic_Astrolabe", "generic:compassqty"),
    ("Plunder_Compass", "generic:quantity"), ("Novel_Compass", "generic:rarity"), ("Soldier_Compass", "generic:normals"),
    ("Veteran_Compass", "generic:magics"), ("Elite_Compass", "generic:rares"), ("Boss_Compass", "generic:bosses"),
    ("Beacon_Compass", "generic:beacon"), ("Renown_Edge", "generic:legendary"), ("Militant_Compass", "generic:priceless"),
    ("Ember_Compass", "generic:ember"), ("Fluorescent_Compass", "generic:fluorescent"),
]
def compass_family(key):
    for pat, fam in FAMILIES:
        if pat in key: return fam
    return None
CONSTELLATION = {  # tlidb page key -> mechanic
    "Afterlight_Talent_Constellation": "Afterlight", "Overrealm_Talent_Constellation": "Overrealm", "Dark_Surge_Talent_Constellation": "DarkSurge",
    "Lunaria_Talent_Constellation": "Lunaria", "Vorax_Talent_Constellation": "Vorax", "Creation_Talent_Constellation": "Creation",
    "Outlaw_Talent_Constellation": "Outlaw", "Sandlord_Talent_Constellation": "Sandlord", "Arcana_Talent_Constellation": "Arcana",
    "The_Frozen_Canvas_Talent_Constellation": "FrozenCanvas", "Folklore_Talent_Constellation": "Mistville", "Nightmare_Talent_Constellation": "Nightmare",
    "Aeterna_Talent_Constellation": "Aeterna", "Cube_Talent_Constellation": "Cube", "Blacksail_Talent_Constellation": "Blacksail",
    "Machine_Talent_Constellation": "Machines", "Might_Talent_Constellation": "Might", "War_Talent_Constellation": "War",
    "Hunting_Talent_Constellation": "Hunting", "Clockwork_Ballet_Talent_Constellation": "ClockworkBallet", "Cage_Talent_Constellation": "Cage",
    "Beacon_Talent_Constellation": "generic:beacon", "Compass_Talent_Constellation": "generic:compassqty", "Commodities_Talent_Constellation": "generic:commodities",
    "Gear_Talent_Constellation": "generic:gear", "Legendary_Gear_Talent_Constellation": "generic:legendary", "Profound_Talent_Constellation": "Profound",
}
