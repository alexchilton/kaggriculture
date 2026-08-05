"""Dead-reckoned position against the real one, per unit per turn. The first divergence is the bug.

`scripts/which_tile_is_missing.py` walks each unit forward from its spawn by applying our own MOVE
ops, and lands every one of the 126 PLANT ops on exactly the tile the schedule asks for. The real
environment then plants only 50 of them, and reports the unit standing somewhere else entirely --
unit 3 pinned on `(5,5)` for the whole season, unit 2 on a PASTURE.

Both cannot be right, and the reference says which: `_apply_unit_action` **ignores a move onto
LOCKED** (`kaggriculture.py:313`) and returns without spending the turn or reporting anything. So a
path that clips a locked tile leaves the unit behind by one step, and every op after it lands on the
wrong tile -- a whole day of work aimed at a neighbour.

Dead reckoning cannot see that, which is why the emitter's own accounting says 126/126.

Prints the first divergence per unit per day, and a census of how many turns each unit spends with a
position our emitter does not believe in.
"""

import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import dayplan, routines as R
import build_script_submission as B

TPD = R.TURNS_PER_DAY
SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
D = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}


def main():
    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, rep = dayplan.emit(sched)
    plan = B.build_plan(script.arrays())

    from kaggle_environments import make
    env = make("kaggriculture", debug=True)
    env.reset(2)

    n_slots = 16
    reck = {u: list(R.spawn_tile(u)) for u in range(n_slots)}
    drift = collections.Counter()
    first = {}
    lost_ops = collections.Counter()
    lost_by_day = collections.defaultdict(list)

    for t in range(len(plan)):
        day = t // TPD
        obs = env.state[0].observation
        me = obs["farms"][0]
        board = me["tiles"]
        real = [list(me["farmer"])] + [list(h) for h in (me.get("hands") or [])]
        n = len(real)

        if t % TPD == 0:                      # `_end_of_day` teleports everyone home
            for u in range(n_slots):
                reck[u] = list(R.spawn_tile(u))

        farmer, hands_, market = plan[t]
        acts = [farmer] + list(hands_)

        # ops handed to a unit slot the farm does not own are dropped before the env ever sees them
        for u in range(n, len(acts)):
            if acts[u][0] != "PASS":
                lost_ops[acts[u][0]] += 1
                lost_by_day[day].append((t, u, acts[u]))

        for u in range(min(n, len(acts))):
            if reck[u] != real[u]:
                drift[u] += 1
                first.setdefault((u, day), (t, tuple(reck[u]), tuple(real[u])))

        # advance dead reckoning exactly as the emitter believes, and the env as it truly is
        for u, a in enumerate(acts):
            if a[0] in D:
                dx, dy = D[a[0]]
                reck[u] = [reck[u][0] + dx, reck[u][1] + dy]

        env.step([{"farmer": farmer, "hands": hands_[:n], "market": market},
                  {"farmer": ["PASS"], "hands": [], "market": []}])
        if env.state[0].status == "DONE":
            break

    print("ops handed to unit slots the farm does not own:", dict(lost_ops))
    print("ops dropped for a nonexistent unit, by day:")
    for day in sorted(lost_by_day):
        rows = lost_by_day[day]
        slots = sorted({u for _, u, _ in rows})
        print(f"  day {day:2d}: {len(rows):3d} ops on slots {slots}  "
              f"{collections.Counter(a[0] for _, _, a in rows).most_common(4)}")
    print()
    print("turns spent on a tile the emitter does not believe in, per unit:", dict(sorted(drift.items())))
    print()
    print("first divergence per unit per day (day, turn, we think -> really):")
    for (u, day), (t, r, actual) in sorted(first.items())[:40]:
        print(f"  unit {u}  day {day:2d}  turn {t:3d}   we think {r}   really {actual}")


if __name__ == "__main__":
    main()
