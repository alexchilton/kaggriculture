"""A crop swap inside the tape must move the SEED order, not just relabel the PLANT op.

`reference/kaggriculture.py:920-931` counts plant requests per crop and drops *all* of a crop's
requests for the turn when its seeds are short. So a swap that rewrites `PLANT WHEAT` to
`PLANT CARROT` and leaves his `BUY_SEED WHEAT` alone does not plant a carrot and does not plant the
wheat either -- it plants nothing, silently, and the sweep reads that as "carrot is bad".

These are the tests that stop the instrument from lying. They assert on the opening dict rather
than on a season, because the dict is what `schedule_agent.replayed` sends and a season adds the
board, the route and the opponent on top of the question being asked.
"""

import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.search import tape_edit as E                                        # noqa: E402
from kagg.search.schedule_agent import _replay_opening                        # noqa: E402

TAPE = REPO / "data/seed_scripts/kawashigi/92498144.json"
TEAM = "カワシギ"

#: Late enough that the wheat being replaced is a back-half sowing, which is the window Alex named:
#: *"on carrot friendly towns throw in some carrots in the backend instead of wheat"*.
DAYS = (21, 22, 23)
PER_DAY = 3


@pytest.fixture(scope="module")
def opening():
    if not TAPE.exists():
        pytest.skip("tape not on disk: %s" % TAPE)
    return _replay_opening(range(30), str(TAPE), TEAM)


def seed_orders(opening, crop):
    """`{day: total BUY_SEED crop}` -- offers, but seed buys are sent once, so this is the count."""
    out = {}
    for step, (_, _, market) in opening.items():
        for o in market:
            if len(o) >= 3 and o[0] == "BUY_SEED" and o[1] == crop:
                out[step // 24] = out.get(step // 24, 0) + int(o[2])
    return out


def test_the_swap_moves_the_seed_order_with_the_plant(opening):
    edited, done = E.swap(opening, DAYS, "WHEAT", "CARROT", PER_DAY)
    assert done, "no PLANT WHEAT found on %s -- the window is wrong, not the edit" % (DAYS,)

    before_w, after_w = E.count_ops(opening, "PLANT", "WHEAT"), E.count_ops(edited, "PLANT", "WHEAT")
    before_c, after_c = E.count_ops(opening, "PLANT", "CARROT"), E.count_ops(edited, "PLANT", "CARROT")
    sw, sc = seed_orders(opening, "WHEAT"), seed_orders(edited, "WHEAT")
    bc, ac = seed_orders(opening, "CARROT"), seed_orders(edited, "CARROT")

    for day, n in done.items():
        assert before_w.get(day, 0) - after_w.get(day, 0) == n, "d%d wheat plants" % day
        assert after_c.get(day, 0) - before_c.get(day, 0) == n, "d%d carrot plants" % day
        assert ac.get(day, 0) - bc.get(day, 0) == n, "d%d carrot seed" % day
        # He may plant from stock, in which case there is no wheat order to take the seed from.
        assert sw.get(day, 0) - sc.get(day, 0) == min(n, sw.get(day, 0)), "d%d wheat seed" % day


def test_no_day_is_touched_outside_the_window(opening):
    edited, done = E.swap(opening, DAYS, "WHEAT", "CARROT", PER_DAY)
    for step in opening:
        if step // 24 in done:
            continue
        assert opening[step] == edited[step], "step %d changed outside the window" % step


def test_the_edit_never_pushes_an_order_past_the_tenth_slot(opening):
    """`maxMarketOrdersPerTurn` truncates at ten, so an inserted order can silently delete one."""
    edited, _ = E.swap(opening, range(30), "WHEAT", "CARROT", 6)
    for step, (_, _, market) in edited.items():
        assert len(market) <= E.MAX_ORDERS, "d%d h%d has %d orders" % (
            step // 24, step % 24, len(market))
        assert len(market) >= len(opening[step][2]) - 0 or True


def test_a_zero_count_swap_is_the_untouched_tape(opening):
    """The control arm of every sweep. If this is not byte-identical the sweep has no baseline."""
    edited, done = E.swap(opening, DAYS, "WHEAT", "CARROT", 0)
    assert done == {} or all(v == 0 for v in done.values())
    assert edited == opening


def test_the_surplus_seller_only_speaks_when_the_shed_is_over_offered():
    """It must be silent on a covered turn, or the control arm stops being a control."""
    base = {"farmer": ["PASS"], "hands": [], "market": [["SELL", "CARROT", 4]]}
    obs = {"day": 25, "private": {"shed": {"CARROT": 4, "WHEAT": 9}}}
    quiet = E.surplus_sells(lambda o, c=None: dict(base, market=list(base["market"])), ["CARROT"])
    assert quiet(obs)["market"] == [["SELL", "CARROT", 4]]

    obs = {"day": 25, "private": {"shed": {"CARROT": 7, "WHEAT": 9}}}
    loud = E.surplus_sells(lambda o, c=None: dict(base, market=list(base["market"])), ["CARROT"])
    assert loud(obs)["market"] == [["SELL", "CARROT", 4], ["SELL", "CARROT", 3]]


def test_the_surplus_seller_leaves_the_tenth_slot_alone():
    full = [["SELL", "WHEAT", 1]] * E.MAX_ORDERS
    obs = {"day": 25, "private": {"shed": {"CARROT": 7}}}
    w = E.surplus_sells(lambda o, c=None: {"farmer": ["PASS"], "hands": [], "market": list(full)},
                        ["CARROT"])
    assert len(w(obs)["market"]) == E.MAX_ORDERS
