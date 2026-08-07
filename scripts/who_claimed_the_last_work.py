"""Why does one unit plant and water all evening while five others PASS?

`scripts/the_stranded_carrier.py` showed day 6 ending with u5 working every turn from h16 to h23
while carrying an undelivered fertilizer, and u0, u2, u3, u4, u6 idle. The obvious reading is that
the fertilizer is stranded on a BUSY unit for want of anyone else -- but five units are doing
nothing, so that reading cannot be right.

The suspect is the claim system. Idle units are topped up from `nodes_for(busy)`, and
`_claimed_tiles` retires every tile already on a committed unit's route. If u5 holds the last
unclaimed work, the idle units are offered an empty board and PASS -- not because there is no work,
but because the work is spoken for by the one unit that also needs to go home.

Prints per hour: each unit's remaining route length, and how many candidate nodes the board still
has once claims are applied. `routelen=0` on five units beside `unclaimed=0` is the claim theory;
`unclaimed>0` on idle units means something else is refusing the work.
"""
import json, pathlib, sys, collections
sys.path.insert(0, ".")
from kagg.search import schedule_agent as SA, router as RT
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy
from kaggle_environments import make

DAY = 6
replay, schedule, team = TAPES["seb"]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

seen = {}
_real = SA._router_acts


def _spy(state, sched_, day, hour, tiles, units, invs, shed, seeds, unlocked):
    out = _real(state, sched_, day, hour, tiles, units, invs, shed, seeds, unlocked)
    if day == DAY:
        routes = state["routes"]
        live = [u for u in range(len(units)) if u in routes]
        idle = [u for u in live if not routes.get(u, {}).get("route")]
        claimed = SA._claimed_tiles(units, routes, idle, SA.STEAL_FROM_DAY_MARGIN)
        allnodes = RT.build_nodes(tiles, day, shed, collections.Counter(), unlocked,
                                  state.get("pins") or {}, hour)
        unclaimed = [n for n in allnodes if tuple(n.tile) not in claimed]
        seen[hour] = dict(
            routelen={u: len(routes.get(u, {}).get("route") or []) for u in live},
            idle=idle, nodes=len(allnodes), unclaimed=len(unclaimed),
            unclaimed_tiles=[tuple(n.tile) for n in unclaimed][:8],
            carrying={u: {k: v for k, v in (invs[u] if u < len(invs) else {}).items() if v}
                      for u in live},
        )
    return out


SA._router_acts = _spy

env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
env.reset(2)
agent = SA.make_agent(thin, 0, router=True)
opp = tape_policy(replay, team, 1)

for t in range(24 * (DAY + 1)):
    o0, o1 = env.state[0].observation, env.state[1].observation
    a0, a1 = agent(o0), opp(o1, t)
    n0 = len(o0["farms"][0].get("hands") or [])
    n1 = len(o0["farms"][1].get("hands") or [])
    env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
              {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

for hour in sorted(seen):
    if hour < 13:
        continue
    d = seen[hour]
    rl = " ".join(f"u{u}={n}" for u, n in sorted(d["routelen"].items()))
    carry = {u: c for u, c in d["carrying"].items() if c}
    print(f"h{hour:>2} nodes={d['nodes']:<3} unclaimed={d['unclaimed']:<3} idle={d['idle']}")
    print(f"     routelen {rl}")
    print(f"     carrying {carry}")
    if d["unclaimed"]:
        print(f"     still free: {d['unclaimed_tiles']}")
