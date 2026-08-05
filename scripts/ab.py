"""Tape A against tape B under identical conditions. The only scoreboard that means anything.

    tape A  --extract-->  schedule  --emit-->  tape B

If B were A, B would score what A scores. It does not, and the whole difference is the emitter.

**Both seats must be driven, from `steps[1]`.** Getting either wrong destroys the measurement and
both were gotten wrong here before this file existed:

  - `steps[0].action` is the placeholder recorded at reset and is never applied, so replaying from
    index 0 shifts every turn by one and puts each day boundary out of place. Measured on this
    episode: offset 0 gives $45,387, offset 1 gives $149,662 against a recorded $141,256.
    (This applies only to REPLAYING a recording. A live agent is called at step 0 normally and its
    order lands -- tested, shifting our own plan by one turn makes it worse, not better.)
  - The market is shared, so prices move with the opponent's orders. Replaying A against `starter`
    instead of against its actual opponent gave $50,216 and looked like proof that A's $141k was
    unreachable. It is not: A reproduces.

`configuration` is taken from the episode too, minus the timeouts, so board size, weed chance, shop
intervals and the order cap all match.
"""
import argparse, json, sys
sys.path.insert(0, "."); sys.path.insert(0, "scripts")
import numpy as np
from kaggle_environments import make
from kagg.search import dayplan
import build_script_submission as B

ap = argparse.ArgumentParser()
ap.add_argument("--replay", default="data/seed_scripts/new_leader/90016067.json")
ap.add_argument("--team", default="somewhere after")
ap.add_argument("--schedule", default="data/seed_scripts/new_leader/schedule.json")
a = ap.parse_args()

d = json.load(open(a.replay))
teams = d["info"]["TeamNames"]
seat = teams.index(a.team)
other = 1 - seat
cfg = {k: v for k, v in (d.get("configuration") or {}).items()
       if k not in ("actTimeout", "runTimeout")}


def recorded(s, offset=1):
    out = []
    for st in d["steps"][offset:]:
        act = (st[s] or {}).get("action") or {}
        out.append({"farmer": act.get("farmer") or ["PASS"],
                    "hands": list(act.get("hands") or []),
                    "market": list(act.get("market") or [])})
    return out


def replayer(tp):
    def agent(obs, config=None):
        t = int(obs.get("step", 0) or 0)
        if t >= len(tp):
            return {"farmer": ["PASS"], "hands": [], "market": []}
        r = tp[t]
        farms = obs.get("farms") or []
        me = int(obs.get("player", 0) or 0)
        n = len(farms[me].get("hands", []) or []) if me < len(farms) else 0
        return {"farmer": r["farmer"], "hands": r["hands"][:n], "market": r["market"]}
    return agent


sched = {int(k): v for k, v in json.load(open(a.schedule)).items()}
script, rep = dayplan.emit(sched)
plan = B.build_plan(script.arrays())


def emitted(obs, config=None):
    t = int(obs.get("step", 0) or 0)
    if t >= len(plan):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    f, h, m = plan[t]
    farms = obs.get("farms") or []
    me = int(obs.get("player", 0) or 0)
    n = len(farms[me].get("hands", []) or []) if me < len(farms) else 0
    return {"farmer": f, "hands": h[:n], "market": m}


def run(me):
    env = make("kaggriculture", configuration=cfg, debug=False)
    res = env.run([me, replayer(recorded(other))])
    curve = {}
    for t, step in enumerate(res):
        o = (step[0] or {}).get("observation") or {}
        fs = o.get("farms") or []
        if len(fs) == 2 and t % 24 == 0:
            curve[t // 24] = float(fs[0]["money"])
    fs = ((res[-1][0] or {}).get("observation") or {}).get("farms") or []
    return (float(fs[0]["money"]) if len(fs) == 2 else 0.0), curve


a_final, a_curve = run(replayer(recorded(seat)))
b_final, b_curve = run(emitted)

print("=" * 76)
print(f"A/B -- both against '{teams[other]}' own tape, episode configuration")
print("=" * 76)
print(f"  TAPE A  recorded tape        ${a_final:>11,.0f}")
print(f"  TAPE B  emitted from its schedule ${b_final:>11,.0f}")
print(f"  ratio                        {a_final / max(b_final, 1):>11.1f}x")
print(f"  emitter refusals             {len(rep['refused']):>11}")
print()
print(f"{'day':>4} {'TAPE A':>12} {'TAPE B':>12} {'B/A':>7}")
for day in range(30):
    av, bv = a_curve.get(day, 0.0), b_curve.get(day, 0.0)
    print(f"{day:>4} {av:>12,.0f} {bv:>12,.0f} {(bv / av if av else 0):>7.2f}")
