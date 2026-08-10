"""A hand that cannot carry its load home is given less to carry, not one more job.

The market reads the SHED and nothing else (`kaggriculture._process_market`), and
`_drop_inventories_to_shed` (`kaggriculture.py:812`) empties every hand at the dusk rollover -- after
the market has closed. So produce that ends the day in a hand is produce that was never for sale.

`cover.plan` added the walk home LAST, out of whatever turns the assignment had not already spent:

    route = materialise(..., deliver=False, ...)
    if deliver:
        home = materialise(..., deliver=True, ...)
        if turns(home) <= budget[u]:
            route = home

-- and when it did not fit, kept the longer tour and dropped the trip. Day 4 of `seb1326`, seed 11:
five of six tours were planned with no closing drop at all, u2 finished the day two moves from the
shed and u6 three moves, both loaded, and the row banked 19 units of the 55 it asked for. The 36 it
missed re-offered on day 5, which is why day 5 opens on $9 and cannot buy its melon seed.

The trade is never good. The marginal job is one harvest -- six units of wheat at ~$22 -- and the
stranded load is the eight to twenty units already in the hand, plus whatever the day meant to buy
with them. This is why the rule is stated as an invariant of `plan` and not as an option: there is
no board on which stranding the row beats dropping a job.
"""
import importlib

import pytest

DP = importlib.import_module("kagg.search.cover")

SHED = [(4, 4)]


def _harvest(tile, units=6):
    return DP.Job(tile, [("HARVEST", None)], gives={"WHEAT": units},
                  products=frozenset({"WHEAT"}))


def _ends_at_a_depot(route):
    return bool(route) and getattr(route[-1], "depot", False) and route[-1].drop


def _carried(route):
    """What the tour is still holding when it stops, if it never banks."""
    held = 0
    for s in route:
        if getattr(s, "depot", False) and s.drop:
            held = 0
        elif isinstance(s, DP.Job):
            held += sum(s.gives.values())
    return held


#: Four harvests in a line walking AWAY from the shed. All four plus the walk back is 12 turns; the
#: budget is 10, so the full tour cannot come home and a shorter one can.
LINE = [(3, 4), (2, 4), (1, 4), (0, 4)]


def test_a_tour_that_cannot_come_home_is_shortened_until_it_can():
    out, _left = DP.plan({0: (4, 4)}, [_harvest(t) for t in LINE], {0: 10},
                         depots=SHED, wanted={"WHEAT": 40}, deliver=True, day=4)
    route = out[0]["route"]
    assert _ends_at_a_depot(route), (
        f"the tour ends holding {_carried(route)} WHEAT away from the shed, so none of it is for "
        f"sale today\n  route: {route}"
    )


def test_nothing_the_row_wants_ends_the_tour_in_a_hand():
    out, _left = DP.plan({0: (4, 4)}, [_harvest(t) for t in LINE], {0: 10},
                         depots=SHED, wanted={"WHEAT": 40}, deliver=True, day=4)
    assert _carried(out[0]["route"]) == 0, (
        f"{_carried(out[0]['route'])} units of the row finish the day in a hand\n"
        f"  route: {out[0]['route']}"
    )


@pytest.mark.parametrize("day", [0, 2, 4, 7, 11])
def test_the_rule_is_not_day_specific(day):
    """It was gated on `day in RANK_HOME_DAYS`, i.e. day 4 alone.  The market behaves the same way
    on every day of the season, so the invariant has to as well."""
    out, _left = DP.plan({0: (4, 4)}, [_harvest(t) for t in LINE], {0: 10},
                         depots=SHED, wanted={"WHEAT": 40}, deliver=True, day=day)
    assert _ends_at_a_depot(out[0]["route"]), (
        f"day {day}: tour strands {_carried(out[0]['route'])} WHEAT\n  route: {out[0]['route']}"
    )


def test_a_tour_carrying_nothing_the_row_wants_is_left_alone():
    """The narrowing that keeps this honest: shortening a tour costs a job, so it is only ever paid
    for by produce the market is actually waiting for."""
    jobs = [DP.Job(t, [("WATER", None)]) for t in LINE]
    out, _left = DP.plan({0: (4, 4)}, jobs, {0: 10},
                         depots=SHED, wanted={"WHEAT": 40}, deliver=True, day=4)
    worked = sum(1 for s in out[0]["route"] if isinstance(s, DP.Job))
    assert worked == len(LINE), (
        f"a tour that banks nothing was shortened to {worked} of {len(LINE)} jobs anyway\n"
        f"  route: {out[0]['route']}"
    )
