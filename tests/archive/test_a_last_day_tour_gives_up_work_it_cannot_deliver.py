"""A d29 tour that cannot walk its load home gives up trailing jobs until it can.

On every other day this is a trade -- the overnight sweep banks whatever the tour ends up
holding, so a job is always worth more than a walk. On the LAST day the sweep lands after the
market is gone: produce a tour cannot deliver is discarded, so the trailing jobs that strand it
are turns spent making things to throw away. The d29 trace shows u7 watering and harvesting at
(7,1)-(7,2) through h22 and ending the season at (7,2) holding 12 units; the tape harvests 19
to our 26 on its d29 and strands 7 units to our 26.

The reserve pricing (`cover.cost`) cannot reach this: d29 is precomputed and
`_apply_precomputed` seats solved stops without ever pricing them. The one place a solved tour
can shed work for its walk home is the trim in `cover.plan`, which existed
(`TRIM_A_TAIL_THAT_CANNOT_COME_HOME`) and was off, gated to a day set that never contained a
delivering day.
"""
import collections
import importlib

import pytest

C = importlib.import_module("kagg.search.cover")
R = importlib.import_module("kagg.search.routines")

LAST_DAY = R.SEASON_DAYS - 1
DEPOTS = tuple(sorted(C.SHED))


def _plan_last_day(monkeypatch):
    """Two harvests on one solved tour: work 5 turns, walk home 11, budget 10.

    The whole tour cannot come home (11 > 10); dropping the trailing job can (10 <= 10).
    Costs probed against `materialise`/`turns` directly before freezing them here.
    """
    j1 = C.Job((0, 1), [("HARVEST", None)], gives={"WHEAT": 4}, products=frozenset({"WHEAT"}))
    j2 = C.Job((0, 3), [("HARVEST", None)], gives={"WHEAT": 4}, products=frozenset({"WHEAT"}))
    monkeypatch.setitem(C.PRECOMPUTED_ROUTES, LAST_DAY,
                        {0: [((0, 1), ("HARVEST",)), ((0, 3), ("HARVEST",))]})
    out, _left = C.plan([(0, 0)], [j1, j2], [10], DEPOTS,
                        wanted=collections.Counter({"WHEAT": 10}), deliver=True, day=LAST_DAY)
    return out[0]


def test_a_last_day_tour_trims_its_tail_to_reach_the_shed(monkeypatch):
    tour = _plan_last_day(monkeypatch)
    closes = [s for s in tour["route"] if getattr(s, "depot", False) and s.drop]
    assert closes, (
        f"the d{LAST_DAY} tour keeps both harvests and ends away from the shed, so both loads "
        f"are discarded at the close: route={tour['route']}, cost={tour['cost']}. The walk home "
        f"costs 11 against a budget of 10, and nothing gives up the trailing job.")
    assert tour["cost"] <= 10, f"the trimmed tour still busts its budget: {tour['cost']}"


def test_an_ordinary_day_keeps_the_job_and_takes_the_sweep(monkeypatch):
    """d10 delivers too (`WALK_THE_LOAD_HOME_DAYS`), and its trade goes the other way: the
    overnight sweep banks the load free, so work must never be given up for the walk."""
    j1 = C.Job((0, 1), [("HARVEST", None)], gives={"WHEAT": 4}, products=frozenset({"WHEAT"}))
    j2 = C.Job((0, 3), [("HARVEST", None)], gives={"WHEAT": 4}, products=frozenset({"WHEAT"}))
    monkeypatch.setitem(C.PRECOMPUTED_ROUTES, 10,
                        {0: [((0, 1), ("HARVEST",)), ((0, 3), ("HARVEST",))]})
    out, _left = C.plan([(0, 0)], [j1, j2], [10], DEPOTS,
                        wanted=collections.Counter({"WHEAT": 10}), deliver=True, day=10)
    kept = [s for s in out[0]["route"] if not getattr(s, "depot", False)]
    assert len(kept) == 2, (
        f"d10 gave up a job for its walk home; only the last day may -- every other day banks "
        f"the load in the overnight sweep: {out[0]['route']}")
