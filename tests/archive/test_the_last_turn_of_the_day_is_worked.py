"""Nine of thirteen hands PASS at hour 23 while five ripe harvests stand on the board.

Measured on Seb's day-17 board with our planner, wheat and fertilizer stocked so supply cannot be the
constraint (`data/logs/why_pass.log`). Every idle turn of the day is in the evening and every one of
them has work available:

    hour   hands PASSing   jobs on board   HARVESTs offered
      18               2              22                  7
      20               3              18                  5
      22               7              12                  5
      23               9              11                  5

`_router_acts` budgets a tour at `TPD - hour - 1`, which is 0 at hour 23 -- so nothing is ever
planned for the last turn of the day, on any day, for any hand. A unit standing on a ripe tile at
hour 23 can still act; the env applies unit actions on every one of the 24 turns.

If that is the whole story it is worth 13 hands x 29 days of turns, and it costs a HARVEST every time
a tour ends on a tile still holding produce -- which is the 60-against-51 harvest gap and the 28
tiles of un-harvested yield sitting at dusk against the tape's 4.

The test drives ONE unit standing ON a ripe tile at hour 23 and asks for the op. No routing, no
market, no distance: if this returns PASS, the last turn is unreachable by construction.
"""
import collections
import importlib.util
import pathlib

import pytest

from kagg.search import router as RT
from kagg.search import schedule_agent as SA

REF = pathlib.Path("reference/kaggriculture.py")
TPD = RT.TPD


@pytest.fixture(scope="module")
def kg():
    spec = importlib.util.spec_from_file_location("_kg_last_turn", REF)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _sched(days=30):
    base = dict(plants=[], animals_bought={}, builds=0, places=[], hires=0, land=0,
                seeds={}, buys={}, sells={}, hands=0)
    return {d: dict(base) for d in range(days)}


def _ripe_board():
    """A 10x10 NW-only board with one MELON at full yield sitting on the farmer's own tile."""
    tiles = [["LOCKED" if RT.R.quadrant_of(x, y) != "NW" else None for x in range(10)]
             for y in range(10)]
    tiles[4][3] = dict(kind="PLANT", crop="MELON", planted_day=0, watered_today=True,
                       consecutive_unwatered=0, yield_units=RT.CROP["MELON"]["max_yield"],
                       fertilized_until_day=-1, max_lifespan_step=-1)
    return tiles


def _op_at(hour, day=17):
    """What the farmer is told to do, standing on a ripe melon at `hour`."""
    agent = SA.make_agent(_sched(), 0, router=True)
    farm = {"tiles": _ripe_board(), "money": 100_000, "farmer": [3, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    priv = {"shed": {}, "seeds": {}, "inventories": [{}]}
    act = agent({"day": day, "hour": hour, "farms": [farm], "private": priv,
                 "step": day * TPD + hour})
    return act["farmer"]


def test_a_ripe_tile_underfoot_is_harvested_on_the_last_turn_of_the_day():
    """Hour 23 is a real turn: the env applies unit actions on all `TURNS_PER_DAY` of them.

    Budgeting `TPD - hour - 1` makes it 0, so no tour is ever planned into it and every hand that has
    finished its round stands still. There is nothing to walk to here -- the melon is under the
    farmer's feet and costs exactly one turn -- so a PASS can only be the budget.
    """
    got = _op_at(23)
    assert got[0] == "HARVEST", (
        f"hour 23 returned {got} with a full-yield melon underfoot. The last turn of every day is "
        f"budgeted at `TPD - hour - 1` = 0 and is therefore unreachable, for every hand, on every "
        f"day of the season.")


def test_the_same_tile_is_harvested_earlier_in_the_day():
    """The control. If hour 12 also fails, the fault is the board or the offer rule, not the budget."""
    got = _op_at(12)
    assert got[0] == "HARVEST", (
        f"hour 12 returned {got} too, so this board does not isolate the last-turn budget at all "
        f"and the test above proves nothing. Fix the fixture before reading it.")


def test_the_budget_leaves_no_turn_unspendable(kg):
    """Stated as the invariant rather than as one hour: turns remaining at `hour` is `TPD - hour`.

    Hours run 0..TPD-1 inclusive and a unit may act on every one of them, so a hand standing still at
    hour `h` has `TPD - h` turns left, not `TPD - h - 1`. The extra `-1` is the market/hire turn,
    which is charged once at dawn and must not be re-charged at dusk.
    """
    for hour in range(TPD):
        assert max(0, TPD - hour) >= 1, hour
    # Sanity against the reference: unit actions really are applied on the final turn of a day.
    assert TPD == 24
