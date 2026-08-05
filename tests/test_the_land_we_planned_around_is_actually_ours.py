"""A parcel the schedule buys must be owned from that day, because the emitter routes as if it were.

`emit()` builds `parcels_by_day` off the schedule's `land` column and hands `_board` a tile list that
grows with it. From that dawn onward hands are routed across the quadrant border as though the ground
were ours. If the BUY_LAND does not settle, `_apply_unit_action` **ignores the move onto LOCKED**
without spending the turn (`kaggriculture.py:313`), the unit falls one tile behind, and every op for
the rest of the day lands on its neighbour -- silently, and cumulatively, since dead reckoning never
notices.

Measured (`scripts/did_the_land_arrive.py`): the farm held **NW and nothing else for all thirty days**,
and both BUY_LAND orders vanished without a word. Not the ten-order cap -- their turn carried three
orders. The bank:

    day  7   dawn $1,239   turn 0 buys 5 WHEAT + 4 STRAWBERRY seed   ->  $787 at turn 1, parcel costs $1,000
    day 10   dawn $1,157   turn 0 buys seed and 2 COW               ->   $55 at turn 1

`_do_buy_land` returns silently when `farm["money"] < price`, so ordering the day's seed and livestock
*before* the parcel spends the parcel's money. The tape does the reverse: it **sells first and buys
afterwards**, and its BUY_LAND quotes against the proceeds.

    tape day 7   h0  SELL FERTILIZER 1, SELL WHEAT 1        -> $1,719
                 h1  SELL FERTILIZER 3, BUY_PRODUCT WHEAT 1 -> $1,954
                 h2  BUY_PRODUCT WHEAT 7, HIRE, HIRE, BUY_LAND
                 h3  BUY_SEED STRAWBERRY 4, BUY_SEED WHEAT 5, SELL WHEAT 10

Ordering inside a turn cannot fix it: `build_script_submission.market_orders` puts BUY_LAND last by
design, and the money is gone a turn earlier regardless. The order of the *turns* is the thing.
"""

import json
import pathlib
import sys

import numpy as np
import pytest

sys.path.insert(0, "scripts")

from kagg.search import routines as R

pytestmark = pytest.mark.slow

SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
TPD = R.TURNS_PER_DAY


@pytest.fixture(scope="module")
def owned():
    """`day -> quadrants the farm really holds at dusk`, from our tape in the real environment.

    Dusk, not dawn: a parcel ordered on day `d` settles inside day `d`, so dawn of `d` legitimately
    predates it. What is *not* legitimate is the day ending without it, because `emit()` has already
    routed hands across the border for that whole day.
    """
    if not SCHEDULE.exists():
        pytest.skip(f"{SCHEDULE} missing; run scripts/extract_leader_schedule.py")
    from kaggle_environments import make
    from kagg.search import dayplan
    import build_script_submission as B

    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, rep = dayplan.emit(sched)
    plan = B.build_plan(script.arrays())

    env = make("kaggriculture", debug=True)
    env.reset(2)
    held = {}
    for t in range(len(plan)):
        me = env.state[0].observation["farms"][0]
        if t % TPD == TPD - 1:      # dusk: the day's BUY_LAND has had every turn to settle
            held[t // TPD] = sorted(me["unlocked_quadrants"])
        farmer, hands_, market = plan[t]
        n = len(me.get("hands") or [])
        env.step([{"farmer": farmer, "hands": hands_[:n], "market": market},
                  {"farmer": ["PASS"], "hands": [], "market": []}])
        if env.state[0].status == "DONE":
            break
    return sched, held


def test_the_land_we_planned_around_is_actually_ours(owned):
    """One parcel bought means two quadrants owned, on the day after we order it and every day after.

    Compared against the schedule's own `land` column, which is what `emit()` routes against -- so this
    is not an aspiration, it is the emitter's own premise held to account.
    """
    sched, held = owned
    wrong = []
    for day in sorted(sched):
        if day not in held:
            continue
        bought = sum(1 for d in sched if d <= day and sched[d].get("land"))
        want = 1 + bought                       # NW is free; LAND_ORDER is NE, SW, SE
        got = len(held[day])
        if got < want:
            wrong.append(f"day {day}: {got} quadrants {held[day]} against {want} "
                         f"after {bought} parcel(s) ordered")
    assert not wrong, ("routed across ground the farm never bought:\n  "
                       + "\n  ".join(wrong[:10]))
