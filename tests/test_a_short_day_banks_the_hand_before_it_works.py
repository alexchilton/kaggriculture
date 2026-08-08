"""On a `rush` tour, produce already in the hand goes to the shed FIRST, not last.

## The gap

`BANK_THE_HAND_WHEN_SHORT` (`schedule_agent.py`) diverts a unit carrying the row's produce on a
cash-short day by marking it idle, which triggers a re-solve. The re-solve hands it a fresh tour of
work and the produce rides along. `materialise` then has three places it can drop:

    mid-tour     cover.py:452   gated on `load >= DELIVER_MIN`, which is 6
    the free drop cover.py:448  gated on a zero-detour depot
    the close    cover.py:480   fires -- but it is the LAST stop of the tour

Seed 11, day 4: unit u0 holds 4 FERTILIZER and u6 holds 2 from h8. Four is under `DELIVER_MIN`, so
the only drop is the closing one, which lands after every job the tour was just given. Traced:

    h08  shed 0   u0 4F/0W   u6 2F/0W
    h15  shed 0   u0 4F/0W   u6 2F/0W        -- still carried, seven hours later
    h23  shed 0   hands 28
    midnight -- `_drop_inventories_to_shed` banks it, after the market has closed

We ended day 4 on $939 against a $1,000 parcel. The six fertilizer are worth about $576.

## The rule

`rush` already means "this day is short of cash" -- `_solve` passes `fund=short_of_cash` straight
through to `plan(rush=...)` and on into `materialise`. It currently only reorders WORK (`Job.funds`).
It must also mean: a hand that STARTS the tour holding the row's produce banks it before working.

Once, at the front. Not a lowered `DELIVER_MIN` -- the docstring at `cover.py:408` records that
dropping the threshold on a short day planned a shed trip after every stop and left eight animals
unfed. This fires exactly once per tour and cannot do that.

## The guards that must not be lost

- `DROP` is all-or-nothing (`kaggriculture.py:333`). A hand whose remaining tour still owes any of
  what it carries must not shed it -- that is the failure that cost eight cows.
- A hand carrying less than `BANK_MIN` is not worth a walk. This is the same judgement
  `DELIVER_MIN` makes, at the lower threshold that a cash-short day justifies.
- `rush=False` is the overwhelming majority of days. Nothing about them may move.
"""

import collections
import sys

sys.path.insert(0, ".")

from kagg.search import cover as C

SHED = C.nearest(C.SHED, (0, 0))
FAR = (max(SHED[0] + 4, 6), max(SHED[1] + 4, 6))


def _job(tile, needs=None):
    """A plain HARVEST that draws nothing unless told to."""
    return C.Job(tile, [("HARVEST", None)], needs=needs or {}, gives={})


def _leads_with_a_drop(route):
    """Is the very first stop a shed trip that empties the hand?"""
    return bool(route) and getattr(route[0], "depot", False) and route[0].drop


def test_a_rush_tour_banks_a_carried_load_before_its_first_job():
    """The whole thing. Four fertilizer in hand, a cash-short day, work far from the shed."""
    route = C.materialise(FAR, [_job(FAR), _job((FAR[0], FAR[1] - 1))],
                          carry={"FERTILIZER": 4}, wanted={"FERTILIZER": 6}, rush=True)
    assert _leads_with_a_drop(route), (
        "a rush tour started holding 4 FERTILIZER the row wants and went to work anyway; "
        "the only drop is the closing one, so the market never sees it.\n    route: "
        + " ".join(("SHED" if getattr(s, "depot", False) else str(s.tile)) for s in route))


def test_an_ordinary_day_is_completely_unchanged():
    """`rush=False` is nearly every day of the season. It may not move at all."""
    work = [_job(FAR), _job((FAR[0], FAR[1] - 1))]
    calm = C.materialise(FAR, work, carry={"FERTILIZER": 4}, wanted={"FERTILIZER": 6}, rush=False)
    assert not _leads_with_a_drop(calm)


def test_it_will_not_shed_what_the_tour_still_owes():
    """`DROP` is all-or-nothing. Feed the remaining stops need is not surplus at any threshold."""
    work = [_job(FAR, needs={"FERTILIZER": 4}), _job((FAR[0], FAR[1] - 1))]
    route = C.materialise(FAR, work, carry={"FERTILIZER": 4}, wanted={"FERTILIZER": 6}, rush=True)
    assert not _leads_with_a_drop(route), (
        "the tour's own FERTILIZE still needs all four and DROP takes the whole hand")


def test_a_hand_below_the_threshold_does_not_buy_a_walk():
    """One unit in hand is not worth a trip, on a short day or any other."""
    route = C.materialise(FAR, [_job(FAR)],
                          carry={"FERTILIZER": 1}, wanted={"FERTILIZER": 6}, rush=True)
    assert not _leads_with_a_drop(route)


def test_only_what_the_row_actually_wants_counts():
    """`wanted` is the row's unmet sells. Produce nothing is waiting for is not money today."""
    route = C.materialise(FAR, [_job(FAR)],
                          carry={"FERTILIZER": 4}, wanted={"WOOL": 6}, rush=True)
    assert not _leads_with_a_drop(route)


def test_the_carried_load_is_gone_after_the_drop():
    """A leading drop that leaves the hand full has changed nothing downstream."""
    route = C.materialise(FAR, [_job(FAR)],
                          carry={"FERTILIZER": 4}, wanted={"FERTILIZER": 6}, rush=True)
    assert _leads_with_a_drop(route)
    drawn = collections.Counter()
    for stop in route:
        if getattr(stop, "depot", False):
            drawn += stop.pick
    assert drawn["FERTILIZER"] == 0, "it banked the load and immediately drew it back out"
