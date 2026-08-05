"""One day, unit by unit: his tape against ours. The smallest thing that can be exactly right.

Alex's call, and it is the correct unit of work. Matching a season is 30 coupled problems; matching
day 0 is one, and every later day is the same problem with more state. If day 0 is not exact there is
no point measuring day 13.
"""
import argparse, collections, json, pathlib, sys
sys.path.insert(0, "."); sys.path.insert(0, "scripts")
import numpy as np
from kagg.search import dayplan, routines as R

ap = argparse.ArgumentParser()
ap.add_argument("--day", type=int, default=0)
ap.add_argument("--replay", default="data/seed_scripts/new_leader/90016067.json")
ap.add_argument("--team", default="somewhere after")
a = ap.parse_args()
TD = 24

d = json.load(open(a.replay))
seat = d["info"]["TeamNames"].index(a.team)
his = collections.defaultdict(list)
his_market = []
for t in range(a.day * TD, (a.day + 1) * TD):
    s = d["steps"][t][seat] or {}
    act = s.get("action") or {}
    his["farmer"].append(act.get("farmer") or ["PASS"])
    for i, h in enumerate(act.get("hands") or []):
        his[f"hand{i}"].append(h or ["PASS"])
    for o in (act.get("market") or []):
        his_market.append((t % TD, o))

sched = {int(k): v for k, v in
         json.loads(pathlib.Path("data/seed_scripts/new_leader/schedule.json").read_text()).items()}
script, rep = dayplan.emit(sched)
names = {v: k for k, v in R.OP.items()}
op = np.asarray(script.unit_op); crop = np.asarray(script.unit_crop)
item = np.asarray(script.unit_item); qty = np.asarray(script.unit_qty)
ours = collections.defaultdict(list)
for t in range(a.day * TD, min((a.day + 1) * TD, op.shape[0])):
    for u in range(op.shape[1]):
        nm = names.get(int(op[t, u]), "PASS")
        if nm == "PLANT":
            nm = f"PLANT:{R.CROPS[int(crop[t,u])]}"
        elif nm in ("PICKUP", "PLACE"):
            nm = f"{nm}:{R.ITEMS[int(item[t,u])]}x{int(qty[t,u])}"
        ours["farmer" if u == 0 else f"hand{u-1}"].append(nm)

row = sched[a.day]
print("=" * 108)
print(f"DAY {a.day}: HIS SCHEDULE -> HIS TAPE  vs  HIS SCHEDULE -> OUR TAPE")
print("=" * 108)
print(f"  schedule says: hands {row['hands']}  builds {row['builds']}  places {row['places']}  "
      f"plants {len(row['plants'])}  land {row['land']}")
print(f"  seeds {row['seeds']}  buys {row['buys']}")
print()

def census(seq):
    c = collections.Counter(x[0] if isinstance(x, list) else x.split(":")[0] for x in seq)
    c.pop("PASS", None)
    return c

keys = sorted(set(his) | set(ours), key=lambda k: (k != "farmer", k))
print(f"{'unit':>8} {'HIS ops':>8} {'OUR ops':>8}   his                              | ours")
for k in keys:
    h, o = his.get(k, []), ours.get(k, [])
    hc, oc = census(h), census(o)
    hs = " ".join(f"{a_}:{b}" for a_, b in hc.most_common(6))
    os_ = " ".join(f"{a_}:{b}" for a_, b in oc.most_common(6))
    print(f"{k:>8} {sum(hc.values()):>8} {sum(oc.values()):>8}   {hs:<32} | {os_}")

print()
print(f"{'turn':>5} {'HIS farmer':>22} {'OUR farmer':>22} | {'HIS hand0':>20} {'OUR hand0':>20}")
for i in range(TD):
    hf = his["farmer"][i] if i < len(his["farmer"]) else ["-"]
    of = ours["farmer"][i] if i < len(ours["farmer"]) else "-"
    h0 = his["hand0"][i] if i < len(his.get("hand0", [])) else ["-"]
    o0 = ours["hand0"][i] if i < len(ours.get("hand0", [])) else "-"
    print(f"{i:>5} {' '.join(map(str,hf)):>22} {str(of):>22} | "
          f"{' '.join(map(str,h0)):>20} {str(o0):>20}")

print()
print("HIS market orders this day:")
for turn, o in his_market:
    print(f"   turn {turn:>2}: {o}")
print("OUR market orders this day:")
arrs = script.arrays()
import build_script_submission as B
for t in range(a.day * TD, (a.day + 1) * TD):
    m = B.market_orders(t, arrs)
    if m:
        print(f"   turn {t % TD:>2}: {m}")
