"""Did the parcel we planned around actually get bought, and on which day.

Every remaining position divergence has the same shape -- `we think (5,1), really (4,1)`, `we think
(0,5), really (0,4)` -- which is a unit trying to step into NE or SW and being refused. The emitter
computes `parcels_by_day` straight off the schedule's `land` column and routes as though the ground
were ours from that dawn. If the BUY_LAND never settles, every op aimed past the quadrant border is
emitted onto locked ground and silently lost, and it stays lost for the rest of the season.

`_do_buy_land` (`kaggriculture.py:680`) returns silently when the bank is short, and `_process_market`
truncates each turn's queue to `maxMarketOrdersPerTurn` = 10 -- so there are two independent ways for
the order to vanish without a word.

Prints, per day: the bank at dawn, the BUY_LAND orders we issued and at which turn, how many market
orders shared that turn, and which quadrants the farm actually owns.
"""

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
    buy_land = np.asarray(script.buy_land)

    from kaggle_environments import make
    env = make("kaggriculture", debug=True)
    env.reset(2)

    print(f"{'day':>4} {'dawn $':>10} {'want':>4} {'turn':>5} {'orders that turn':>17}  quadrants owned")
    for t in range(len(plan)):
        if t % TPD == 0:
            day = t // TPD
            me = env.state[0].observation["farms"][0]
            want = int(buy_land[t:t + TPD].sum())
            turns = [i for i in range(t, min(t + TPD, len(plan))) if buy_land[i]]
            crowd = len(plan[turns[0]][2]) if turns else 0
            print(f"{day:>4} {me['money']:>10,.0f} {want:>4} "
                  f"{(turns[0] % TPD if turns else -1):>5} {crowd:>17}  "
                  f"{sorted(me['unlocked_quadrants'])}"
                  f"{'   <-- ordered but not owned' if want and crowd >= 10 else ''}")
        farmer, hands_, market = plan[t]
        n = len(env.state[0].observation["farms"][0].get("hands") or [])
        env.step([{"farmer": farmer, "hands": hands_[:n], "market": market},
                  {"farmer": ["PASS"], "hands": [], "market": []}])
        if env.state[0].status == "DONE":
            break


if __name__ == "__main__":
    main()
