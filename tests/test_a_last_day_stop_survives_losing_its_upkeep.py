"""A solved stop on the last day must keep its seat when the day strips ops from its job.

`cover._apply_precomputed` seats a stop by the exact key `(tile, ops)`. That is right on an
ordinary day -- a tuple that stops matching means the board is not the board the day was solved
for. On the LAST day it is the landmine the brief names: dropping FEED/CARE from a pen's job
(they pay out at a rollover into a day 30 that does not exist) changes the key, so the stop
LEAVES the solved route and falls to greedy insertion instead of getting two turns cheaper.
That is exactly how `NO_UPKEEP_ON_THE_LAST_DAY = True` measured harvest 396 -> 389 and was parked.

The rule pinned here: on the last day only, a stop whose exact key misses is still seated on the
unit the solve chose, provided the job at that tile is a REDUCED form of the solved stop -- its
ops a subset of the solved ops. A job the solve never described (not a subset) stays a miss, and
every earlier day keeps the exact-key rule untouched.
"""
import importlib

import pytest

DP = importlib.import_module("kagg.search.cover")
R = importlib.import_module("kagg.search.routines")

LAST_DAY = R.SEASON_DAYS - 1
FULL = ("FEED", "CARE", "COLLECT_FERTILIZER", "HARVEST")
DEPOTS = tuple(sorted(DP.SHED))


def _call(day, plan, jobs, units, monkeypatch):
    monkeypatch.setitem(DP.PRECOMPUTED_ROUTES, day, plan)
    DP.PRECOMPUTED_MISSES.clear()
    out = DP._apply_precomputed(day, units, jobs, [23] * len(units), DEPOTS, {}, None, False,
                                False, None)
    assert out is not None, "the plan was not applied at all; the test is aimed at nothing"
    return out


def test_a_reduced_stop_keeps_the_seat_the_solve_chose(monkeypatch):
    """The defect. Upkeep stripped from the job must not move the stop off its solved unit.

    Unit 0 is parked ON the tile, so greedy insertion would seat the job there; the solve says
    unit 1. Only the tile-match fallback can honour the solve.
    """
    job = DP.Job((5, 2), [("COLLECT_FERTILIZER", None), ("HARVEST", None)])
    routes, left = _call(LAST_DAY, {1: [((5, 2), FULL)]}, [job], [(5, 2), (4, 4)], monkeypatch)
    assert job in routes[1], (
        f"the last day dropped a stop whose FEED/CARE were removed: routes={routes}, left={left}, "
        f"misses={DP.PRECOMPUTED_MISSES}. `_apply_precomputed` still matches on the exact op "
        f"tuple, so freeing upkeep turns throws the stop to greedy insertion.")
    assert not DP.PRECOMPUTED_MISSES, (
        f"the reduced stop was recorded as a board mismatch: {DP.PRECOMPUTED_MISSES}")


def test_a_job_the_solve_never_described_is_still_a_miss(monkeypatch):
    """The guard. Tile-matching must not seat arbitrary work -- ops must be a subset."""
    job = DP.Job((5, 2), [("WATER", None)])
    routes, _left = _call(LAST_DAY, {1: [((5, 2), FULL)]}, [job], [(5, 2), (4, 4)], monkeypatch)
    assert job not in routes[1], (
        f"a WATER job was seated on a solved FEED/CARE/COLLECT/HARVEST stop: {routes}")
    assert DP.PRECOMPUTED_MISSES and DP.PRECOMPUTED_MISSES[0][0] == LAST_DAY, (
        "the mismatch was not recorded as a miss")


@pytest.mark.parametrize("day", [12, 20, 28])
def test_every_earlier_day_keeps_the_exact_key(day, monkeypatch):
    """d0-d28 bank their load overnight for free; their keying must stay byte-identical."""
    job = DP.Job((5, 2), [("COLLECT_FERTILIZER", None), ("HARVEST", None)])
    routes, _left = _call(day, {1: [((5, 2), FULL)]}, [job], [(5, 2), (4, 4)], monkeypatch)
    assert DP.PRECOMPUTED_MISSES and DP.PRECOMPUTED_MISSES[0][0] == day, (
        f"d{day} tile-matched a stop whose ops changed; only the last day may. routes={routes}")
