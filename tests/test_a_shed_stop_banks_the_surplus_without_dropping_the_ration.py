"""A hand standing at the shed banks what it does not need and KEEPS what it does.

`DROP` is all-or-nothing (`kaggriculture.py:333`): it empties the whole inventory. So a herd tour that
wants to bank one fertilizer has to dump the wheat its next pens are about to eat and then spend a
second turn drawing the same wheat back. `materialise` plans exactly that -- `REDRAW_RATHER_THAN_CARRY`
emits `Depot(drop=True, pick=after[i])` and its own comment prices it honestly: "the DROP plus one turn
per item drawn back".

There is a one-turn version of the same trip and the tape uses it. `PLACE <item> <n>` on a
shed-adjacent tile is a QUANTIFIED shed drop (`kaggriculture.py:381-395`): it moves n of one item into
the shed and leaves the rest of the hand alone. Kawashigi's day 1 never emits DROP at all -- his single
bank of the day is `PLACE FERTILIZER` at h18.

Measured on day 1, seed 11, kawashigi tape, before this test existed. The farmer works alone on a
24-turn budget and the planner priced his tour at 18:

    Shed(4,4)[WHEATx3]          1     PICKUP
    Job(4,4) FEED CARE COLLECT  3
    Shed(4,4)[DROP+WHEATx2]     2     dump the load, take the ration back
    Job(4,3) FEED CARE COLLECT  3
    Shed(4,4)[DROP+WHEATx1]     2     dump the load, take the ration back
    Job(2,4) FEED CARE COLLECT  3

The fourth pen -- `Job(3, 4)` -- priced at 25 in every position and went UNCOVERED, one turn over
budget, while two of the tour's turns were spent re-drawing wheat it had just binned. That is the whole
of `feed 3/4` and `care 3/4` on the day, and the chain it starts is the reason the season is short an
animal: the sheep miss a production night, d6 shears 9 where the tape shears 12, and d7 cannot afford
its third animal.

The assertion is on the MECHANISM, not on day 1: no planned shed stop may pay to re-draw an item it
dropped on the same stop. Day 1 is asserted separately below because it is the day that pays for it.
"""
import collections
import importlib

import pytest

import kagg.plan as _PLAN
import kagg.search.cover as C

SEED = 11
DAY = 1

PEN_OPS = [("FEED", "WHEAT"), ("CARE", None), ("COLLECT_FERTILIZER", None)]


def pen(tile):
    """One pen's whole day: eat a wheat, give back a fertilizer."""
    return C.Job(tile, PEN_OPS, needs={"WHEAT": 1}, gives={"FERTILIZER": 1})


def test_a_shed_stop_does_not_redraw_what_it_just_dropped():
    """Two pens on the shed's doorstep, one wheat each, and a row that wants the fertilizer."""
    start = C.SHED[0]
    work = [pen(start), pen((4, 3))]
    route = C.materialise(start, work, {}, C.SHED, {"FERTILIZER": 3}, deliver=False, rush=True)
    guilty = [s for s in route if getattr(s, "depot", False) and s.drop and s.pick]
    assert not guilty, (
        f"a shed stop drops its whole hand and immediately draws it back: {guilty} in {route}. "
        "DROP is all-or-nothing, so this costs one turn to bin the ration plus one to replace it. "
        "PLACE <item> <n> banks the surplus alone in a single turn -- see kaggriculture.py:381-395, "
        "and the tape's own d1, which PLACEs its fertilizer and never DROPs.")


@pytest.fixture(scope="module")
def feeds_by_day():
    """`{day: FEED ops our seat emitted}`, playing the shipped plan against the kawashigi tape."""
    import scripts.breakdown as B

    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = _PLAN.load(schedule)

    seen = collections.Counter()
    make = SA.make_agent

    def factory():
        inner = make(sched, 0, router=True)

        def play(obs, _t=None):
            act = inner(obs)
            for op in [act.get("farmer")] + list(act.get("hands") or []):
                if op and op[0] == "FEED":
                    seen[obs.get("day")] += 1
            return act

        return play

    B.run(factory, lambda: B.tape_policy(replay, team, 1), SEED, 0.0, stop_day=DAY + 1,
          economy=B.env_config(replay), shops=B.recorded_shops(replay))
    return seen


def test_the_premise_day_one_has_four_pens_to_feed(feeds_by_day):
    """Guard. With fewer than four on the row the assertion below would pass vacuously."""
    row = _PLAN.load().get(DAY) or {}
    assert int(row.get("feeds", 0) or 0) == 4, \
        f"d{DAY} no longer feeds 4 on the tape -- this test is measuring nothing"


def test_day_one_feeds_every_pen_it_owns(feeds_by_day):
    row = _PLAN.load().get(DAY) or {}
    want = int(row.get("feeds", 0) or 0)
    got = feeds_by_day[DAY]
    assert got == want, (
        f"d{DAY} fed {got} pens against the tape's {want}. The fourth pen prices one turn over a "
        "24-turn budget, and two of that tour's turns are spent re-drawing wheat the same stop "
        "dropped. Bank the surplus with PLACE and the pen fits.")
