"""Every BUILD and PLACE our tape emits, and why the environment refused it.

11 pens stand by day 10 and only 5 animals live in them, so the herd is losing at both ends: some
BUILDs never raise a structure and some PLACEs never fill one. Both are silent.

`_apply_unit_action` on PLACE (`kaggriculture.py:447`) needs **all four** of:

    the unit is standing on the tile                    -- a blocked move puts it on the neighbour
    the tile is a structure of the animal's own kind     -- COW and SHEEP want PASTURE, GOOSE a COOP
    the structure is empty                              -- `"animal" not in tile`
    the animal is in the unit's own inventory            -- `_inv_take`, so a PICKUP must precede it

Miss any one and it returns without spending the turn and without a word. BUILD_PASTURE is the same
shape: LOCKED ground or an occupied tile and nothing happens.

Prints the verdict for every BUILD and PLACE op, with the tile and the carried inventory at that turn.
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
STRUCTURE = {"COW": "PASTURE", "SHEEP": "PASTURE", "GOOSE": "COOP"}


def main():
    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, rep = dayplan.emit(sched)
    plan = B.build_plan(script.arrays())

    from kaggle_environments import make
    env = make("kaggriculture", debug=True)
    env.reset(2)

    verdicts = collections.Counter()
    detail = []

    for t in range(len(plan)):
        obs = env.state[0].observation
        me = obs["farms"][0]
        priv = obs["private"]
        board = me["tiles"]
        invs = priv.get("inventories") or []
        real = [list(me["farmer"])] + [list(h) for h in (me.get("hands") or [])]

        farmer, hands_, market = plan[t]
        acts = [farmer] + list(hands_[:len(real)])

        for u, a in enumerate(acts):
            if not a or a[0] not in ("PLACE", "BUILD_PASTURE", "BUILD_COOP", "PICKUP"):
                continue
            x, y = real[u]
            tile = board[y][x]
            inv = dict(invs[u]) if u < len(invs) else {}
            if a[0] == "PICKUP":
                item = a[1]
                have = (priv.get("shed") or {}).get(item, 0)
                v = "ok" if have > 0 else "SHED_EMPTY"
                if tuple((x, y)) not in set(R.shed_access_tiles()):
                    v = "NOT_AT_SHED"
            elif a[0] in ("BUILD_PASTURE", "BUILD_COOP"):
                v = "LOCKED" if tile == "LOCKED" else ("OCCUPIED" if tile is not None else "ok")
            else:
                item = a[1]
                if tile == "LOCKED":
                    v = "LOCKED"
                elif not isinstance(tile, dict):
                    v = "NO_STRUCTURE"
                elif tile.get("kind") != STRUCTURE.get(item):
                    v = f"WRONG_STRUCTURE({tile.get('kind')} for {item})"
                elif "animal" in tile:
                    v = "ALREADY_STOCKED"
                elif inv.get(item, 0) <= 0:
                    v = "NOT_CARRIED"
                else:
                    v = "ok"
            verdicts[f"{a[0]}:{v.split('(')[0]}"] += 1
            if v != "ok":
                detail.append(f"turn {t:3d} (day {t // TPD:2d} h{t % TPD:2d}) unit {u} ({x},{y}) "
                              f"{' '.join(str(z) for z in a):24s} {v:22s} inv={inv} "
                              f"shed={ {k: v2 for k, v2 in (priv.get('shed') or {}).items() if k in STRUCTURE} }")

        env.step([{"farmer": farmer, "hands": hands_[:len(real)], "market": market},
                  {"farmer": ["PASS"], "hands": [], "market": []}])
        if env.state[0].status == "DONE":
            break

    for k in sorted(verdicts):
        print(f"  {k:44s} {verdicts[k]}")
    print()
    for line in detail[:45]:
        print(line)
    if len(detail) > 45:
        print(f"... and {len(detail) - 45} more")


if __name__ == "__main__":
    main()
