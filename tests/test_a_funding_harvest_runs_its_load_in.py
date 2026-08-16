"""A hand that takes a split funding harvest walks the produce straight to the shed.

The last piece of the day-8 chain, and the only one that is deliberately a WALK.

`SPLIT_THE_FUNDING_HARVEST` lets a second hand take a ripe pen's HARVEST on its own, which is what
the tape does.  On its own that loses ground: the hand harvests and then CARRIES the milk, because
every delivery rule in `materialise` refuses a trip that is not free -- `DELIVER_MIN` exists to stop
a small load buying a walk, `DROP_WHERE_THE_TOUR_ALREADY_STANDS` requires zero detour, and
`BANK_ON_THE_PEN_THAT_FUNDS_THE_DAY` requires the pen to BE shed ground.

Geometry, seed 11, day 8, measured:

    shed-access tiles   (4,4) (4,5) (5,4) (5,5)
    our ripe cows       (4,4) IS shed ground     (3,4) is NOT

So cow A banks on its own pen for one turn and no walking, and cow B cannot -- it needs a walk
whoever harvests it.  The tape has the same geometry (his cows are (4,3) and (4,4)) and answers it
by making that harvest a dedicated ERRAND:

    his u2   h04 HARVEST   ...   h06 (4,4) PLACE/MILK

Harvest, walk, deposit, nothing else.  The walk IS the point: the milk is the day's working capital
-- the row buys `WHEAT 17` on a $4 dawn bank to feed ten animals -- so two turns of walking buy the
whole afternoon.  Every existing rule prices that trip as a cost against a load; this one prices it
against the DAY.

See `THE_FUNDING_HARVEST_RUNS_ITS_LOAD_IN`.
"""
import importlib

import pytest

DP = importlib.import_module("kagg.search.cover")

SHED = [(4, 4), (4, 5), (5, 4), (5, 5)]


def _harvest(tile):
    """A split funding harvest: the HARVEST alone, carrying the row's produce."""
    j = DP.Job(tile, [("HARVEST", None)], gives={"MILK": 6}, products=frozenset({"MILK"}))
    j.funds = True
    return j


def _chore(tile):
    return DP.Job(tile, [("WATER", None)])


def _route(work, start=(4, 4)):
    return DP.materialise(start, work, depots=SHED, wanted={"MILK": 12}, deliver=True, rush=True)


def _first_bank(route):
    for n, s in enumerate(route):
        if isinstance(s, DP.Depot) and (s.drop or s.place.get("MILK")):
            return n, s
    return None, None


def test_the_load_goes_in_before_the_next_job():
    """Off-depot pen, more work ahead: the milk must not ride along with it."""
    work = [_harvest((4, 3)), _chore((0, 0)), _chore((0, 1))]
    route = _route(work)
    n, stop = _first_bank(route)
    assert n is not None, f"the milk is carried, never banked early\n  route: {route}"
    jobs_before = [s for s in route[:n] if isinstance(s, DP.Job)]
    assert len(jobs_before) == 1, (
        f"banked only after {len(jobs_before)} jobs, so the market missed it\n  route: {route}"
    )
    assert tuple(stop.tile) in {tuple(t) for t in SHED}, f"banked off shed ground: {stop!r}"


def test_an_on_depot_pen_still_banks_where_it_stands():
    """The zero-walk case must not regress into a trip."""
    work = [_harvest((4, 4)), _chore((0, 0))]
    route = _route(work)
    n, stop = _first_bank(route)
    assert n == 1 and tuple(stop.tile) == (4, 4), (
        f"the on-pen bank was displaced by the errand rule\n  route: {route}"
    )


def test_an_ordinary_harvest_is_not_sent_on_an_errand():
    """Only a pen the row is WAITING on justifies the walk."""
    j = DP.Job((4, 3), [("HARVEST", None)], gives={"MILK": 6}, products=frozenset({"MILK"}))
    route = DP.materialise((4, 4), [j, _chore((0, 0))], depots=SHED,
                           wanted={"WHEAT": 20}, deliver=True, rush=True)
    n, _ = _first_bank(route)
    jobs_before = [s for s in route[:n] if isinstance(s, DP.Job)] if n is not None else []
    assert n is None or len(jobs_before) > 1, (
        f"sent an errand for produce the row does not sell\n  route: {route}"
    )
