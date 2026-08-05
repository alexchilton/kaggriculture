"""Pen by pen and animal by animal: what the schedule asks for, what we emit, what the board holds.

`tests/test_the_farm_matches_the_tape_day_by_day.py` ends at `pens 12 against the tape's 14` and
`animals 6 against the tape's 14` -- and the second number is the season, because the winner draws
most of its revenue from milk and wool. A pen count does not say whether the BUILD failed, the PLACE
failed, the animal was never bought, or the animal escaped, and those are four different bugs:

    BUILD_PASTURE   silent no-op on LOCKED ground or on an occupied tile
    BUY_ANIMAL      silent no-op on a short bank (`_do_buy_animal`)
    PLACE           needs the animal CARRIED, so a PICKUP must precede it, on a shed tile
    escape          two consecutive unfed days and the animal is gone, the structure remains
                    (`kaggriculture.py:786`)

Prints per day: the schedule's builds and places, the ops we emitted, the animals we bought, and the
board's own pen and animal count -- so the day a pen stops matching names which of the four it was.
"""

import collections
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import dayplan, routines as R
import build_script_submission as B

TPD = R.TURNS_PER_DAY
SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")


def main():
    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, rep = dayplan.emit(sched)
    plan = B.build_plan(script.arrays())
    buy_animal = np.asarray(script.buy_animal)

    from kaggle_environments import make
    env = make("kaggriculture", debug=True)
    env.reset(2)

    print(f"{'day':>4} {'sched b/p':>10} {'emitted BUILD/PLACE':>20} {'bought':>16} "
          f"{'pens':>5} {'animals':>8} {'unfed>0':>8}  notes")
    for t in range(len(plan)):
        day, hour = divmod(t, TPD)
        if hour == 0:
            me = env.state[0].observation["farms"][0]
            pens = animals = unfed = 0
            for row in me["tiles"]:
                for cell in row:
                    if isinstance(cell, dict) and cell.get("kind") in ("PASTURE", "COOP"):
                        pens += 1
                        if "animal" in cell:
                            animals += 1
                            if cell.get("consecutive_unfed", 0) > 0:
                                unfed += 1
            row_s = sched.get(day, {})
            emitted = collections.Counter()
            for tt in range(t, min(t + TPD, len(plan))):
                f, h, _m = plan[tt]
                n = 16
                for a in [f] + list(h[:n]):
                    if a and a[0] in ("BUILD_PASTURE", "BUILD_COOP", "PLACE", "PICKUP"):
                        emitted[a[0]] += 1
            bought = {R.ANIMAL_NAMES[i]: int(v)
                      for i, v in enumerate(buy_animal[t:t + TPD].sum(axis=0)) if v}
            want_b = row_s.get("builds", 0)
            want_p = len(row_s.get("places") or [])
            note = ""
            if emitted["PLACE"] < want_p:
                note += f"emitted {emitted['PLACE']} PLACE of {want_p}  "
            builds = emitted["BUILD_PASTURE"] + emitted["BUILD_COOP"]
            print(f"{day:>4} {f'{want_b}/{want_p}':>10} "
                  f"{f'{builds}/{emitted[chr(80) + chr(76) + chr(65) + chr(67) + chr(69)]}':>20} "
                  f"{str(bought or ''):>16} {pens:>5} {animals:>8} {unfed:>8}  {note}")
        farmer, hands_, market = plan[t]
        n = len(env.state[0].observation["farms"][0].get("hands") or [])
        env.step([{"farmer": farmer, "hands": hands_[:n], "market": market},
                  {"farmer": ["PASS"], "hands": [], "market": []}])
        if env.state[0].status == "DONE":
            break


if __name__ == "__main__":
    main()
