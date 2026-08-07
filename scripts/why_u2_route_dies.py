"""u2 walks five turns to (1,3) on day 6 and does nothing when it arrives.

From `scripts/who_claimed_the_last_work.py`: u2 holds a one-node route from h16 to h20, reaches
(1,3) at h21, and by then its route is empty -- while `build_nodes` still lists (1,3) and (0,3) as
work and eight units stand idle to dusk.

A stop is popped in `_router_acts` when `_live_ops` returns nothing for it. `_live_ops` gates
item-bearing ops on THIS UNIT'S inventory, so a node the board considers live can be dead for the
particular unit walking to it. This prints, each hour, u2's route head, the cell there, u2's
inventory, and what `_live_ops` returns -- so the reason the stop dies is read off, not guessed.
"""
import json, pathlib, sys, collections
sys.path.insert(0, ".")
from kagg.search import schedule_agent as SA, router as RT
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy
from kaggle_environments import make

DAY, WATCH = 6, 2
replay, schedule, team = TAPES["seb"]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

_real = SA._router_acts
rows = []


def _spy(state, sched_, day, hour, tiles, units, invs, shed, seeds, unlocked):
    # Read the route BEFORE this turn walks it -- that is the tour u2 is committed to.
    if day == DAY and hour >= 14:
        st = (state.get("routes") or {}).get(WATCH) or {}
        route = st.get("route") or []
        inv = collections.Counter(invs[WATCH] if WATCH < len(invs) else {})
        pins = state.get("pins") or {}
        head = tuple(route[0].tile) if route else None
        info = ""
        if head:
            cell = tiles[head[1]][head[0]]
            live = SA._live_ops(head, cell, day, inv, pins, seeds)
            kind = cell.get("kind") if isinstance(cell, dict) else cell
            info = (f"head={head} kind={kind} live_ops={live} "
                    f"ops_on_route={[(o, i) for o, i in route[0].ops]}")
            if isinstance(cell, dict) and kind == "PLANT":
                info += (f" crop_ops={RT.crop_ops(cell, day, inv.get('FERTILIZER', 0) > 0)}"
                         f" cell={ {k: v for k, v in cell.items() if k != 'kind'} }")
        rows.append(f"h{hour:>2} pos={units[WATCH]} inv={dict(inv)} routelen={len(route)} {info}")
    return _real(state, sched_, day, hour, tiles, units, invs, shed, seeds, unlocked)


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

print("\n".join(rows))
