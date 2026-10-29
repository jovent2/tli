"""Group the logged Profound runs by forced mechanics (compass >= 0.5/run) and report value composition."""
import sys, os, collections, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN, mech, features as F
RN.PRICES["100300"] = {"id": "100300", "price_fe": 1.0}
CAT = {"燃料": "fuel", "灰烬": "ember", "化石": "fossil", "罗盘": "compass", "星盘": "compass", "传奇装备": "legendary", "装备蓝图": "legendary",
       "记忆荧光": "fluor", "神骸": "divinity", "冥王的神格": "divinity", "异度棱镜": "prism", "棱镜水平仪": "prism", "棱镜校尺": "prism", "棱镜修复仪": "prism", "特殊棱镜": "prism",
       "命运": "destiny", "命运相关": "destiny", "复苏材料": "lunar", "复苏材料（月相）": "lunar", "侵蚀材料": "darksurge", "黑潮敕令": "darksurge",
       "元件": "outlaw", "高塔筹码": "outlaw", "渴瘾兑换材料": "vorax", "普通器官": "vorax", "触媒技能": "medium", "崇高辅助技能": "noble", "华贵辅助技能": "magnif",
       "塔罗斯技能": "talos", "始源塔罗斯技能": "talos", "信标": "beacon", "通用道具": "misc", "探针": "probe", "香料": "spice", "神威纹章": "emblem",
       "辅助技能": "support", "被动技能": "passive", "神格契约": "pact", "画中雪原": "canvas", "迷城残响": "aeterna", "永恒迷城": "aeterna", "雾都怪谈": "mistville",
       "欲念原核": "cube", "虚海请柬": "blacksail", "原初之核": "misc", "升华之楔": "misc", "追忆游丝": "misc", "追忆碎絮": "misc", "神威辉石": "misc"}
def cat(i):
    return CAT.get(RN.typ(i), "other:" + RN.typ(i))

def forced(r):
    fams = set()
    for i, q in r["cost"].items():
        if RN.typ(i) in ("罗盘", "星盘"):
            f = mech.compass_family(RN.name(i))
            if f and not f.startswith("generic") and q >= 0.5: fams.add(f)
    return tuple(sorted(fams))

def table(min_runs=300):
    R = RN.load()
    G = collections.defaultdict(lambda: dict(runs=0, strats=0, gross=0.0, cost=0.0, dur=0.0, Qw=0.0, cats=collections.Counter(), jack=0.0))
    for r in R:
        f = F.extract(r); key = forced(r); g = G[key]; n = r["count"]
        g["runs"] += n; g["strats"] += 1; g["gross"] += r["gross"] * n; g["cost"] += r["cost_fe"] * n; g["dur"] += r["dur_s"] * n; g["Qw"] += f["Q"] * n
        for i, q in r["loot"].items():
            v = RN.value(i, q) * n
            if (RN.price(i) or 0) >= 1000: g["jack"] += v
            else: g["cats"][cat(i)] += v
    rows = [(k, g) for k, g in G.items() if g["runs"] >= min_runs]
    rows.sort(key=lambda kg: -(kg[1]["gross"] - kg[1]["cost"]) / (kg[1]["dur"] / 60))
    return rows

if __name__ == "__main__":
    rows = table()
    print(f"{'forced mechanics':34s} {'runs':>5s} {'str':>3s} {'Q':>4s} {'steady':>6s} {'jack':>5s} {'cost':>5s} {'min':>4s} {'net/min':>7s} | top categories (FE/run)")
    for k, g in rows:
        n = g["runs"]; steady = sum(g["cats"].values()) / n
        top = ", ".join(f"{c} {v/n:.0f}" for c, v in g["cats"].most_common(6))
        print(f"{'+'.join(k) or '(none)':34s} {n:5d} {g['strats']:3d} {g['Qw']/n:4.1f} {steady:6.0f} {g['jack']/n:5.0f} {g['cost']/n:5.0f} {g['dur']/n/60:4.1f} {(g['gross']-g['cost'])/(g['dur']/60):7.0f} | {top}")
