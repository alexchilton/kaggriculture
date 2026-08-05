"""tape -> schedule -> tape. The emitter is only correct if this is the identity.

Alex's framing, and it is the strongest test available: extract and emit are supposed to be inverses.
Feed the tape's own placements back through the emitter and the tape must come out. Anything that
differs is the emitter, because the input is the tape's own ground truth -- there is no second farm
in this measurement and no target anyone chose.
"""
import argparse, collections, json, pathlib, sys
sys.path.insert(0, "."); sys.path.insert(0, "scripts")
import numpy as np
from kagg.search import dayplan, routines as R

ap = argparse.ArgumentParser()
ap.add_argument("--tape", default="data/seed_scripts/new_leader/tape.json")
ap.add_argument("--schedule", default="data/seed_scripts/new_leader/schedule.json")
ap.add_argument("--days", default="")
a = ap.parse_args()
TD = 24

tape = json.loads(pathlib.Path(a.tape).read_text())
sched = {int(k): v for k, v in json.loads(pathlib.Path(a.schedule).read_text()).items()}

# ---- tape -> tile-level placements
placements = collections.defaultdict(lambda: dict(plants=[], builds=[]))
pending_build = {}
for r in tape:
    for c in r["units"]:
        if not c or not c.get("tile"):
            continue
        tile = tuple(c["tile"])
        if c["op"] == "PLANT":
            placements[r["day"]]["plants"].append((tile, c["arg"]))
        elif c["op"] in ("BUILD_PASTURE", "BUILD_COOP"):
            pending_build[tile] = r["day"]
        elif c["op"] == "PLACE" and c["arg"] in R.ANIMAL_NAMES:
            # PLACE is not animals-only: the tape also PLACEs products (13 WOOL placements on day
            # 29). Only an animal going into a pen is a build, which is why the naive count read 27
            # placements against 14 pens.
            day = pending_build.pop(tile, r["day"])
            placements[day]["builds"].append((tile, c["arg"]))
placements = {d: v for d, v in placements.items()}

script, rep = dayplan.emit(sched, placements=placements)
names = {v: k for k, v in R.OP.items()}
op = np.asarray(script.unit_op)

def tape_cell(t, u):
    if t >= len(tape):
        return "PASS"
    c = tape[t]["units"][u] if u < len(tape[t]["units"]) else None
    if not c:
        return "PASS"
    return {"MOVE": c["arg"]}.get(c["op"], c["op"])

days = [int(x) for x in a.days.split(",")] if a.days else list(range(30))
tot = mat = 0
per_day = {}
hist_t, hist_e = collections.Counter(), collections.Counter()
for day in days:
    dt = dm = 0
    for t in range(day * TD, (day + 1) * TD):
        for u in range(13):
            h = tape_cell(t, u)
            e = names.get(int(op[t, u]), "PASS") if t < op.shape[0] and u < op.shape[1] else "PASS"
            hist_t[h] += 1; hist_e[e] += 1
            dt += 1
            if h == e:
                dm += 1
    per_day[day] = (dm, dt)
    tot += dt; mat += dm

print("=" * 92)
print(f"ROUND TRIP  tape -> schedule -> tape : {mat}/{tot} cells ({100*mat/max(tot,1):.1f}%)")
print("=" * 92)
print(f"  placements fed back: {sum(len(v['plants']) for v in placements.values())} plants, "
      f"{sum(len(v['builds']) for v in placements.values())} builds")
print(f"  emitter refusals:    {len(rep['refused'])}")
print()
print(f"{'day':>4} {'match':>10}   {'day':>4} {'match':>10}   {'day':>4} {'match':>10}")
items = [f"{d:>4} {m:>5}/{n:<4}" for d, (m, n) in sorted(per_day.items())]
for i in range(0, len(items), 3):
    print("   ".join(items[i:i + 3]))
print()
print(f"{'op':>20} {'TAPE':>7} {'EMITTED':>8} {'gap':>7}")
for k in sorted(set(hist_t) | set(hist_e), key=lambda k: -hist_t[k]):
    if k == "PASS":
        continue
    print(f"{k:>20} {hist_t[k]:>7} {hist_e[k]:>8} {hist_e[k]-hist_t[k]:>+7}")
