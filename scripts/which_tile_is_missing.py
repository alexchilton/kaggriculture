"""Which requested tile did the emitter not plant, and on what day.

The census tests say `plants day 1: 16 against the tape's 17`. A count does not say which tile, and
the tile is the whole question -- a refusal in the chooser looks identical to a PLANT emitted onto
LOCKED ground, which is a silent no-op (`ops.py:86`, `_apply_unit_action`).

Prints, per day: the tiles the schedule asks for, the tiles our tape actually plants (read back off
`unit_op`/`unit_crop` plus the position we walk the unit to), and the set difference.
"""

import collections
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import routines as R
from kagg.search import dayplan

TPD = R.TURNS_PER_DAY
SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")


def main():
    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, report = dayplan.emit(sched)

    names = {v: k for k, v in R.OP.items()}
    op = np.asarray(script.unit_op)
    crop = np.asarray(script.unit_crop)

    # walk every unit forward from its spawn so a PLANT op can be attributed to a tile
    n_units = op.shape[1]
    pos = {u: list(R.spawn_tile(u)) for u in range(n_units)}

    planted = collections.defaultdict(list)
    D = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
    for t in range(op.shape[0]):
        day = t // TPD
        if t % TPD == 0:  # dawn: units are teleported home (`_end_of_day`)
            for u in range(n_units):
                pos[u] = list(R.spawn_tile(u))
        for u in range(n_units):
            nm = names.get(int(op[t, u]), "PASS")
            if nm in D:
                dx, dy = D[nm]
                pos[u] = [pos[u][0] + dx, pos[u][1] + dy]
            elif nm == "PLANT":
                planted[day].append((tuple(pos[u]), R.CROPS[int(crop[t, u])]))

    total_want = total_got = 0
    for day in sorted(sched):
        want = [(tuple(t), c) for t, c in (sched[day].get("plant_tiles") or [])]
        if not want and not planted[day]:
            continue
        got = planted[day]
        total_want += len(want)
        total_got += len(got)
        missing = collections.Counter(want) - collections.Counter(got)
        extra = collections.Counter(got) - collections.Counter(want)
        flag = "" if not (missing or extra) else "   <-- "
        print(f"day {day:2d}  want {len(want):2d}  got {len(got):2d}{flag}"
              f"{'missing ' + str(sorted(missing.elements())) if missing else ''}"
              f"{'  extra ' + str(sorted(extra.elements())) if extra else ''}")
    print(f"\ntotal want {total_want}  got {total_got}")
    if report.get("refused"):
        print(f"refused: {report['refused'][:10]}")


if __name__ == "__main__":
    main()
