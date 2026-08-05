"""Play the day-planner's tape in the real environment. The number that decides whether it works.

Everything else measured so far is a proxy: op counts, turns per hand, walk ratio. They located the
bug, but the tape either banks money or it does not.
"""
import argparse, collections, json, pathlib, sys
sys.path.insert(0, "."); sys.path.insert(0, "scripts")
import numpy as np
from kagg.search import dayplan, routines as R
import build_script_submission as B

ap = argparse.ArgumentParser()
ap.add_argument("--opponent", default="starter")
ap.add_argument("--games", type=int, default=3)
ap.add_argument("--no-fertilize", action="store_true")
a = ap.parse_args()

sched = {int(k): v for k, v in
         json.loads(pathlib.Path("data/seed_scripts/new_leader/schedule.json").read_text()).items()}
script, rep = dayplan.emit(sched, fertilize=not a.no_fertilize)
plan = B.build_plan(script.arrays())

def agent(obs, config=None):
    step = int(obs.get("step", 0) or 0)
    if step >= len(plan):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    farmer, hands_, market = plan[step]
    farms = obs.get("farms") or []
    me = int(obs.get("player", 0) or 0)
    n = len(farms[me].get("hands", []) or []) if me < len(farms) else 0
    return {"farmer": farmer, "hands": hands_[:n], "market": market}

from kaggle_environments import make
finals, curve = [], {}
for g in range(a.games):
    env = make("kaggriculture", debug=False)
    res = env.run([agent, a.opponent])
    obs = (res[-1][0] or {}).get("observation") or {}
    farms = obs.get("farms") or []
    finals.append(float(farms[0]["money"]) if len(farms) == 2 else 0.0)
    if not curve:
        for t, step in enumerate(res):
            o = (step[0] or {}).get("observation") or {}
            f = o.get("farms") or []
            if len(f) == 2 and t % 24 == 0:
                curve[t // 24] = (float(f[0]["money"]),
                                  len(f[0].get("hands") or []),
                                  len(f[0].get("livestock") or []))

print("=" * 96)
print(f"DAY PLANNER -- his schedule through the per-day assigner, {a.games} games vs {a.opponent}")
print("=" * 96)
print(f"  pens {rep['pens']}  crop tiles {rep['crops']}  refusals {len(rep['refused'])}")
print(f"  ours  ${np.mean(finals):>12,.0f}   min ${min(finals):,.0f}  max ${max(finals):,.0f}")
print(f"  his   ${141_256:>12,}")
print(f"  routines.py at the same schedule: $22,347")
print()
print(f"{'day':>4} {'OUR bank':>12} {'HIS bank':>12} {'hands':>6} {'herd':>5}")
for day in range(30):
    m, h, a_ = curve.get(day, (float('nan'), 0, 0))
    print(f"{day:>4} {m:>12,.0f} {(sched[day]['money_dawn'] or 0):>12,.0f} {h:>6} {a_:>5}")
