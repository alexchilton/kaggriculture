"""emit(his schedule) must equal his tape. Measured cell by cell, not farm against farm.

The emitter is a function. Its input is his schedule; its correct output is his tape. So the only
question that matters is how much of his tape it reproduces, and every cell that differs is the
defect -- there is no "our farm" in this measurement at all.
"""
import argparse, collections, json, pathlib, sys
sys.path.insert(0, "."); sys.path.insert(0, "scripts")
import numpy as np
from kagg.search import dayplan, routines as R

ap = argparse.ArgumentParser()
ap.add_argument("--days", default="0")
ap.add_argument("--replay", default="data/seed_scripts/new_leader/90016067.json")
ap.add_argument("--team", default="somewhere after")
a = ap.parse_args()
TD = 24
days = [int(x) for x in a.days.split(",")]

d = json.load(open(a.replay))
seat = d["info"]["TeamNames"].index(a.team)
sched = {int(k): v for k, v in
         json.loads(pathlib.Path("data/seed_scripts/new_leader/schedule.json").read_text()).items()}
script, rep = dayplan.emit(sched)
names = {v: k for k, v in R.OP.items()}
op = np.asarray(script.unit_op)

def his_cell(t, u):
    s = d["steps"][t][seat] or {}
    act = s.get("action") or {}
    if u == 0:
        o = act.get("farmer")
    else:
        hands = act.get("hands") or []
        o = hands[u - 1] if u - 1 < len(hands) else None
    if not o:
        return "PASS"
    return {"MOVE": o[1] if len(o) > 1 else "MOVE"}.get(o[0], o[0])

for day in days:
    total = match = 0
    hist_his, hist_ours = collections.Counter(), collections.Counter()
    per_unit = {}
    for u in range(13):
        hm = ho = 0
        for t in range(day * TD, (day + 1) * TD):
            h = his_cell(t, u)
            o = names.get(int(op[t, u]), "PASS") if t < op.shape[0] and u < op.shape[1] else "PASS"
            hist_his[h] += 1; hist_ours[o] += 1
            total += 1
            if h == o:
                match += 1
                hm += 1
            ho += 1
        per_unit[u] = (hm, ho)
    print("=" * 96)
    print(f"DAY {day}: emit(his schedule) vs his tape -- {match}/{total} cells match "
          f"({100*match/max(total,1):.0f}%)")
    print("=" * 96)
    print(f"{'unit':>6} {'cells match':>12}")
    for u, (m, n) in per_unit.items():
        if n:
            print(f"{u:>6} {m:>7}/{n:<4}")
    print(f"\n{'op':>20} {'HIS':>5} {'EMITTED':>8} {'gap':>6}")
    for k in sorted(set(hist_his) | set(hist_ours), key=lambda k: -hist_his[k]):
        if k == "PASS":
            continue
        print(f"{k:>20} {hist_his[k]:>5} {hist_ours[k]:>8} {hist_ours[k]-hist_his[k]:>+6}")
