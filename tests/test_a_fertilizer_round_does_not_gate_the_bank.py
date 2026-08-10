"""A HARVEST ahead stops the tour banking.  A fertilizer collection does not.

`BANK_ONLY_AFTER_THE_LAST_HARVEST` was measured on day 4, where the yielding jobs are HARVESTs, and
it was written against `Job.yields()` -- which is `any(o in YIELDING)`, and `YIELDING` is
`("HARVEST", "COLLECT_FERTILIZER")`.  So it silently gates on fertilizer too, and a day whose only
production IS fertilizer cannot bank at all until its last pen has been walked.

That is what day 5 costs us, seed 11, `seb1326`.  Hour by hour, our own run:

    h03-h19   bank $17, unchanged for seventeen consecutive hours
    h05-h18   the crew carries FERTILIZER 1 -> 2 -> 3 -> 4, never dropped
    h03-h19   we re-offer BUY_SEED STRAWBERRY 1 and BUY_SEED MELON 1 on EVERY one of those turns
    h20       the fertilizer is finally dropped and sold; the seed arrives at h21
    dusk      one STRAWBERRY and one MELON still in the bag, unplanted

Strawberry seed is $100 and melon $80 (`kaggriculture.py:15`), so $17 buys neither.  The fertilizer
in the crew's hands was the day's entire cash, and the rule was holding it.

Seb's own hours say the gate is HARVEST and only HARVEST:

    d4   HARVEST 5 7 9 10 11 12 12 14 15 15 15 15 16 19   DROP 19 22 22 22 23
    d6   COLLECT_FERTILIZER 3 4 6 8 10 11 14              DROP 9 15 17 19

Day 6 is the counterexample in his own play: he banks at h9 with three fertilizer collections still
ahead of him.  Day 4 is the rule this file leaves alone -- every drop lands on or after his last
harvest.

The wider claim, that a tour must not bank before its last HARVEST, is
`test_the_tour_banks_only_after_its_last_harvest.py` and must keep passing.
"""
import importlib

import pytest

DP = importlib.import_module("kagg.search.cover")

SHED = [(4, 4)]


def _harvest(tile, units=3):
    return DP.Job(tile, [("WATER", None), ("HARVEST", None)],
                  gives={"WHEAT": units}, products=frozenset({"WHEAT"}))


def _fert(tile):
    """A pen round.  It yields, but the produce is one unit and the day needs its price NOW."""
    return DP.Job(tile, [("COLLECT_FERTILIZER", None)],
                  gives={"FERTILIZER": 1}, products=frozenset({"FERTILIZER"}))


def _drop_positions(route):
    return [n for n, s in enumerate(route) if isinstance(s, DP.Depot) and s.drop]


def _last_of(route, op):
    return max((n for n, s in enumerate(route)
                if isinstance(s, DP.Job) and any(o == op for o, _i in s.ops)), default=-1)


def test_a_fertilizer_round_may_bank_before_its_last_pen():
    """Seb's day 6: DROP at h9, with fertilizer still to collect at h10, h11 and h14."""
    work = [_fert((4, 3)), _fert((4, 5)), _fert((3, 4)), _fert((5, 4))]
    route = DP.materialise((4, 4), work, depots=SHED, wanted={"FERTILIZER": 4})
    last = _last_of(route, "COLLECT_FERTILIZER")
    early = [n for n in _drop_positions(route) if n < last]
    assert early, (
        "the fertilizer round cannot bank until its last pen: drops at "
        f"{_drop_positions(route)}, last collection at {last}\n"
        "  This is the $17 plateau -- day 5 h03-h19 with the crew holding four fertilizer.\n"
        f"  route: {route}"
    )


def test_a_harvest_still_gates_the_bank_when_fertilizer_is_mixed_in():
    """The narrowing must not become 'anything yielding may bank'.

    A tour that collects fertilizer AND still has wheat to cut is a day-4 tour, and day 4's rule
    stands: nothing banks until the wheat is in.
    """
    work = [_fert((4, 3)), _harvest((4, 5)), _fert((3, 4)), _harvest((5, 4))]
    route = DP.materialise((4, 4), work, depots=SHED, wanted={"WHEAT": 20, "FERTILIZER": 4})
    last = _last_of(route, "HARVEST")
    early = [n for n in _drop_positions(route) if n < last]
    assert not early, (
        f"banked before the last harvest: drops at {early}, last HARVEST at {last}\n"
        f"  route: {route}"
    )


@pytest.mark.parametrize("n_pens", [2, 4, 6])
def test_the_pen_round_banks_however_many_pens_it_walks(n_pens):
    tiles = [(4, 3), (4, 5), (3, 4), (5, 4), (3, 3), (5, 5)][:n_pens]
    work = [_fert(t) for t in tiles]
    route = DP.materialise((4, 4), work, depots=SHED, wanted={"FERTILIZER": n_pens})
    last = _last_of(route, "COLLECT_FERTILIZER")
    early = [n for n in _drop_positions(route) if n < last]
    assert early, (
        f"{n_pens} pens: no bank before the last collection at {last}, drops at "
        f"{_drop_positions(route)}\n  route: {route}"
    )
