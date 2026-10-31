"""Parse Torchlight: Infinite's UE_game.log (the file etor reads) into per-map loot and cost.

ItemChange@ lines carry inventory stack totals (BagNum = new total of that stack, Add = new stack of that size, Delete = gone);
deltas per item come from tracking each stack's guid. Blocks "ItemChange@ ProtoName=<Action> start/end": Spv3Open = a map was
opened (compasses / probe / beacon / resonance consumed -> map start), PickItems = loot, XchgReceive / XchgBuy = auction (ignored).
Item ids are the same base ids etor and tlidb use (5028 resonance, 100300 FE, 10262 Alert Outlaw ...).
Usage: python3 gamelog.py UE_game.log [more logs...]
"""
import re, sys, os, collections, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs as RN

TS = re.compile(r"^\[(\d{4})\.(\d{2})\.(\d{2})-(\d{2})\.(\d{2})\.(\d{2}):(\d{3})\]")
PROTO = re.compile(r"ItemChange@ ProtoName=(\w+) (start|end)")
CHG = re.compile(r"ItemChange@ (Delete|Update|Add) Id=(\d+)_(\S+) (?:BagNum=)?(\d*)\s?in PageId=(-?\d+) SlotId=(\d+)")
RESET = re.compile(r"ItemChange@ Reset PageId=(-?\d+)")
ENTRY = re.compile(r"\+\d+\+(\w+) \[(.*)\]\s*$")      # "+7+Id [210321]" / "+16+FId [1141]": first field of a list entry
FIELD = re.compile(r"^[|\s]*\+(\w+) \[(.*)\]\s*$")    # "|   | +Description [..]"
IGNORE_IDS = {"100200"}            # [etor] skipped too (not a drop)
AUCTION = {"XchgReceive", "XchgBuy", "XchgSell", "XchgCancel"}

def ts(line):
    m = TS.match(line)
    if not m: return None
    y, mo, d, h, mi, s, ms = map(int, m.groups())
    return datetime.datetime(y, mo, d, h, mi, s, ms * 1000, tzinfo=datetime.timezone.utc)

def parse(paths):
    """-> list of maps: dict(start, entered, end, next_open, deaths, cost{id: qty}, loot{id: qty}, picks, map_id).
    start = Spv3Open (cost consumed), entered = _JoinFightSuccess into a +maptype area, end = _JoinFightSuccess back in
    MainCity (or the next Spv3Open), deaths = FightFailureView count (he revives and keeps going)."""
    stacks = {}                      # guid -> (base_id, total)
    maps = []; cur = None; block = None; block_items = []
    last_t = None; ent = None; eff = []    # map-entry effect dump: "+Description [..]" then "+Id [..]" (compasses, Void Chart, card, resonance affixes)
    join = None                      # time of the last _JoinFightSuccess whose area lines we are still reading
    join_map = None                  # +mapId seen inside that area block (2026-10-31 logs print it BEFORE +maptype; 10-30 logs after)
    join_left = 0                    # lines left to look for the marker
    for path in paths:
        for line in open(path, encoding="utf-8", errors="replace"):
            t = ts(line)
            if t is not None:
                if ent and "Id" in ent and "Description" in ent: eff.append((last_t, ent["Id"], ent["Description"]))
                last_t = t; ent = None
            else:                                         # effect entries: "+N+Key [v]" opens one, "| +Key [v]" adds a field; field order varies per launch
                mm = ENTRY.search(line)
                if mm:
                    if ent and "Id" in ent and "Description" in ent: eff.append((last_t, ent["Id"], ent["Description"]))
                    ent = {mm.group(1): mm.group(2)}
                else:                                     # a bare "+FId [..]" also opens one (single-entry dumps have no "+N+" prefix)
                    mm = FIELD.search(line)
                    if mm:
                        if ent is None or mm.group(1) in ent:
                            if ent and "Id" in ent and "Description" in ent: eff.append((last_t, ent["Id"], ent["Description"]))
                            ent = {}
                        ent[mm.group(1)] = mm.group(2)
            if "_JoinFightSuccess()" in line: join = t; join_map = None; join_left = 3000; continue
            if join is not None:                          # the area dump that follows (a timestamped header, then "+key [value]" lines)
                join_left -= 1
                if "+mapId [" in line:
                    join_map = line.split("[")[1].split("]")[0]
                    if cur is not None and cur["entered"] == join: cur["map_id"] = join_map
                if "+maptype [" in line:
                    if cur is not None and cur["entered"] is None: cur["entered"] = join; cur["map_id"] = join_map
                    join = None
                elif "+checkType [MainCity]" in line:
                    if cur is not None and cur["entered"] is not None and cur["end"] is None: cur["end"] = join
                    join = None
                elif join_left <= 0:
                    join = None
                if t is None: continue                    # dump lines never carry item changes
            if cur is not None and cur["end"] is None and "FightResult@ Open FightFailureView" in line: cur["deaths"] += 1
            m = PROTO.search(line)
            if m:
                if m.group(2) == "start": block = m.group(1); block_items = []
                else:
                    deltas = collections.Counter()
                    for base, delta in block_items: deltas[base] += delta
                    if block == "Spv3Open":
                        if cur: cur["end"] = cur["end"] or t; cur["next_open"] = t; maps.append(cur)
                        cur = dict(start=t, entered=None, end=None, next_open=None, deaths=0, map_id=None,
                                   cost=collections.Counter({b: -d for b, d in deltas.items() if d < 0}), loot=collections.Counter(), picks=0)
                    elif block in AUCTION or block is None or block == "ResetItemsLayout": pass
                    else:
                        if cur is not None and cur["end"] is None:
                            for b, d in deltas.items():
                                if d > 0: cur["loot"][b] += d
                            if block in ("PickItems", "PickItem"): cur["picks"] += 1
                    block = None; block_items = []
                continue
            if RESET.search(line): continue
            m = CHG.search(line)
            if not m: continue
            kind, base, guid, num, page, slot = m.groups()
            if base in IGNORE_IDS: continue
            num = int(num) if num else 0
            prev = stacks.get(guid, (base, 0))[1]
            if kind == "Delete": stacks.pop(guid, None); delta = -prev
            else: stacks[guid] = (base, num); delta = num - prev
            if block is not None: block_items.append((base, delta))
    if cur: maps.append(cur)
    # one effect dump per map, at map entry (2026-10-30/31 logs): attach the ids active in that map; the Confusion Card is the 7xxxxxxx id
    for m in maps:
        lo = m["start"] - datetime.timedelta(seconds=2); hi = m["end"] or m["next_open"] or (m["start"] + datetime.timedelta(hours=1))
        m["effects"] = {i: d for tt, i, d in eff if tt is not None and lo <= tt <= hi}
        m["card"] = next((re.sub("<[^>]+>", "", d) for i, d in m["effects"].items() if len(i) == 8 and i[:2] in ("71", "72")), None)
    return maps

BEACON_IDS = {"400007"}                      # Glacial Abyss Beacon (Tier 8)
def is_stack(mp, need=None):
    """A real Netherrealm map: a beacon (or any compass/probe) in the cost. need = set of ids that must all be present."""
    if need: return all(i in mp["cost"] for i in need)
    return any(i in BEACON_IDS for i in mp["cost"]) or any(RN.name(i).endswith("Compass") or "Probe" in RN.name(i) for i in mp["cost"])

# Items worth more at the Spacetime Wanderer than on the AH (FE per item, untaxed). Secret of the Glacial Abyss: 30 -> "random Flame x10" =
# 10 draws of 10 Flame Sand or 10 FE; 2026-10-31 log: 24 exchanges (720) -> 300 FE + 2,100 Flame Sand = 0.417 FE each (AH 0.3, 0.26 after tax).
EXCHANGE = {"6002": 300 / 720}
def price(i): return 1.0 if i == RN.FE_ID else (RN.price(i) or 0.0)
def value(items, sold=True):
    return sum(q * (EXCHANGE[i] if (sold and i in EXCHANGE) else price(i) * (0.875 if (sold and i != RN.FE_ID) else 1.0))
               for i, q in items.items())

def report(maps, only_stack=True):
    if only_stack: maps = [m for m in maps if is_stack(m)]
    print(f"{len(maps)} maps")
    tot_loot = collections.Counter(); tot_cost = collections.Counter(); secs = 0.0; gaps = 0.0; ng = 0; deaths = 0
    for k, mp in enumerate(maps, 1):
        t0 = mp["entered"] or mp["start"]
        dur = (mp["end"] - t0).total_seconds() if mp["end"] else float("nan")
        secs += dur if mp["end"] else 0
        gap = (mp["next_open"] - mp["start"]).total_seconds() if mp["next_open"] else float("nan")
        if mp["next_open"]: gaps += gap; ng += 1
        deaths += mp["deaths"]
        lv = value(mp["loot"]); cv = value(mp["cost"], sold=False)
        top = sorted(mp["loot"].items(), key=lambda kv: -value({kv[0]: kv[1]}))[:6]
        card = (mp.get("card") or "-")[:28]
        print(f"map {k:2d} {t0.strftime('%H:%M:%S')}Z {dur:5.0f}s (open-to-open {gap:5.0f}s) deaths {mp['deaths']}  loot {lv:6.1f}  cost {cv:5.1f}  net {lv - cv:6.1f} | card {card:28s} | " + ", ".join(f"{RN.name(i)[:22]} x{q}" for i, q in top))
        tot_loot.update(mp["loot"]); tot_cost.update(mp["cost"])
    n = len(maps); done = sum(1 for m in maps if m["end"])
    L, C = value(tot_loot), value(tot_cost, sold=False)
    print(f"\nTOTAL loot {L:.0f}  cost {C:.0f}  net {L - C:.0f} over {n} maps = {(L - C) / max(1, n):.1f} net/map; deaths {deaths}")
    print(f"in-map time {secs / 60:.1f} min for {done} maps = {secs / max(1, done):.0f} s/map -> {(L - C) / max(1, n) / (secs / max(1, done) / 60):.0f} FE/min in map;"
          f" open-to-open {gaps / max(1, ng):.0f} s/map -> {(L - C) / max(1, n) / (gaps / max(1, ng) / 60):.0f} FE/min wall")
    print("cost per map:", {RN.name(i)[:26]: f"{q / n:.2f} x {price(i):.2f}" for i, q in tot_cost.most_common(12)})
    print("loot per map:")
    for i, q in sorted(tot_loot.items(), key=lambda kv: -value({kv[0]: kv[1]}))[:30]:
        print(f"   {RN.name(i)[:36]:36s} {q / n:8.3f}/map  {value({i: q}) / n:6.1f} FE/map  (price {price(i)})")

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    maps = parse(args)
    report(maps, only_stack="--all" not in sys.argv)
