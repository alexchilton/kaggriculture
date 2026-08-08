"""Stock the remaining schedule will never ask for is not offered at all, so it rots until day 29.

**The measurement that motivated this, and it refutes the theory it was written from.** The stated
cause of the milk pile-up was that we under-sell the rows and so arrive at each day holding more than
the row names. `scripts/probe_sell.py --prod MILK` traces both sides turn by turn on the `seb` tape,
seed 11, weeds off, and says the opposite:

    day 10  offered ours  6  tape  6   row asks  6
    day 11  offered ours  3  tape  3   row asks  3
    day 12  offered ours  6  tape  6   row asks  6      shed at dusk ours 12, tape 9
    day 15  offered ours 24  tape 24   row asks 24
    ...
    day 28  offered ours  6  tape  6   row asks  6      shed at dusk ours 67, tape 16

We meet EVERY milk row exactly, on the day, all season. Both sides start day 12 holding 6, both sell
6, and we end on 12 to his 9 -- because we ran 44 more CARE ops over the season and simply produce
more milk than he does. The `sh:milk +521` row is not a selling failure at all; it is production the
schedule has no line for, because `sells` is an absolute count read off HIS board.

What IS wrong is what happens to it. Nothing releases stock the rows never name, so 51 units of milk
sit in the shed from day 12 to day 29 and are then dumped in one day by `LIQUIDATE_LAST_DAY` --
into a book that `market_price` walks down one unit at a time. The last-day liquidation already
concedes the principle ("stock has no terminal value"); the same argument applies on any day for
stock the REMAINING rows will never ask for, and there it is worth more because it is spread out.

One theory, one test. This pins the release, not the money.
"""

import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import router as RT
from kagg.search import schedule_agent

def blank_board(unlocked=("NW",)):
    """A 10x10 board with every tile outside `unlocked` set to "LOCKED", as the env does.

    Copied from `tests/test_router.py` rather than imported: `tests/` is not a package, and a
    two-line fixture is not worth making it one.
    """
    return [["LOCKED" if RT.R.quadrant_of(x, y) not in unlocked else None
             for x in range(10)] for y in range(10)]


def empty_sched(days=30, **row):
    base = dict(plants=[], animals_bought={}, builds=0, places=[], hires=0, land=0,
                seeds={}, buys={}, sells={}, hands=0)
    return {d: dict(base, **(row if d == 0 else {})) for d in range(days)}


def _offer_a_day(sched, shed, day=0, money=3000):
    """Total units of each product OFFERED across one full day, driving the agent turn by turn.

    No market: the shed is handed back unchanged every turn, which is deliberate. The question is
    what the agent is willing to offer against a given holding, and a draining shed would confound
    that with how fast the book absorbs it.
    """
    board = blank_board()
    agent = schedule_agent.make_agent(sched, 0, router=True)
    farm = {"tiles": board, "money": money, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    total = {}
    for hour in range(RT.TPD):
        act = agent({"day": day, "hour": hour, "farms": [farm], "step": day * RT.TPD + hour,
                     "private": {"shed": dict(shed), "seeds": {}, "inventories": [{}]}})
        for o in act["market"]:
            if o[0] == "SELL":
                total[o[1]] = total.get(o[1], 0) + int(o[2])
    return total


def test_milk_the_rest_of_the_season_never_asks_for_is_released():
    """Day 0 asks MILK 4 and no later day asks for milk at all. We hold 40.

    Thirty-six of those units are provably unsellable under the row policy: every remaining row is
    zero, so they can only leave the shed on the last day. They must be released now instead, at the
    per-offer `rate` the price-impact argument bounds -- 4 at a time, not 40 in one order.
    """
    sched = empty_sched(sells={"MILK": 4})
    offered = _offer_a_day(sched, {"MILK": 40})
    assert offered.get("MILK", 0) >= 40, (
        f"offered {offered.get('MILK', 0)} of 40 against a season that asks for 4 -- "
        f"the other 36 sit until day 29")


def test_no_single_offer_exceeds_the_per_offer_rate():
    """The release is BOUNDED. A dump is the known-bad arm and must not be what this becomes.

    `market_price` falls monotonically in inventory and a SELL walks n units down that curve one at a
    time, measured as wool 123 units -> 138 for REVENUE $29,041 -> $21,811. `rate` -- the largest
    single day the schedule has ever asked for -- is what bounds one offer, and releasing surplus
    must not widen it.
    """
    sched = empty_sched(sells={"MILK": 4})
    board = blank_board()
    agent = schedule_agent.make_agent(sched, 0, router=True)
    farm = {"tiles": board, "money": 3000, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    biggest = 0
    for hour in range(RT.TPD):
        act = agent({"day": 0, "hour": hour, "farms": [farm], "step": hour,
                     "private": {"shed": {"MILK": 40}, "seeds": {}, "inventories": [{}]}})
        for o in act["market"]:
            if o[:2] == ["SELL", "MILK"]:
                biggest = max(biggest, int(o[2]))
    assert biggest <= 4, f"one order offered {biggest} units against a rate of 4 -- that is a dump"


def test_a_schedule_without_shed_dusk_is_unaffected_by_the_shed_target():
    """`shed_dusk` is an OPT-IN field and no schedule on disk carries one. Pin that it is inert.

    The branch exists so `scripts/probe_shed_target.py` can measure the arm -- selling down to the
    tape's own dusk holding lands the final bank within $62 of his against $5,533 -- but it costs d4
    and d5, which currently match, so it is not fed. A test that the absent field changes nothing is
    what keeps "not fed" an honest statement rather than an assumption.
    """
    sched = empty_sched(sells={"MILK": 4})
    assert all("shed_dusk" not in r for r in sched.values())
    without = _offer_a_day(sched, {"MILK": 40})
    for r in sched.values():
        r["shed_dusk"] = None                      # the shape a schedule missing the field can take
    assert _offer_a_day(sched, {"MILK": 40}) == without


def test_the_shed_target_only_ever_widens_the_release():
    """With the field present it is a FLOOR, never a cap. Selling less is the -$16,025 arm."""
    sched = empty_sched(sells={"MILK": 4})
    sched[20]["sells"] = {"MILK": 30}              # so `still_owed` alone releases nothing
    held_back = _offer_a_day(sched, {"MILK": 40})
    sched[0]["shed_dusk"] = {"MILK": 90}           # a target far above what we hold
    assert _offer_a_day(sched, {"MILK": 40}) == held_back, "a high target must not cancel the row"


def test_stock_the_remaining_rows_DO_ask_for_is_still_held():
    """The counter-case, so the release cannot quietly become "sell everything".

    Same 40 units of milk, but day 20 asks for 30 of them. Only ten are surplus, so the day's offers
    must stay at the row's own 4 -- there is nothing here the schedule has not already planned for.
    """
    sched = empty_sched(sells={"MILK": 4})
    sched[20]["sells"] = {"MILK": 30}
    offered = _offer_a_day(sched, {"MILK": 40})
    assert offered.get("MILK", 0) <= 12, (
        f"offered {offered.get('MILK', 0)} against a row of 4 with 30 more asked for on day 20")
