"""On d29 a load must reach the shed with market turns still to come, not just before the close.

Alex, 2026-08-24: *"it needs a sell signal before h23 on day 29 only"*.

**What `must_walk_home_now` guarantees today, and what it does not.** It sends a loaded hand home
when `(24 - hour) <= dist + 1 + LAST_DAY_WALK_SLACK`, which reserves the walk and one DROP turn. So
the load lands in the shed before the close -- and that is all it reserves. Selling is a separate
turn, the offer clears one unit at a time, and the price walks down as it goes.

Measured on ladder game 98335212, seed 34935263, our live agent against their recorded actions:

    h16  shed_total=2  carried=38  sells=[]
    h17  shed_total=2  carried=38  sells=[]
    h18  shed_total=2  carried=38  sells=[]
    h19  shed_total=2  carried=38  sells=[]
    h20  shed_total=2  carried=38  sells=[]
    h21  shed_total=2  carried=38  sells=[('WOOL', 4), ('WHEAT', 8)]
    h22  shed_total=2  carried=26  sells=[('MILK', 15), ('WHEAT', 10)]

Thirty-eight units in hands for six hours with an empty shed and no sell orders at all, then a
drop at h21 with two turns left. The shed still held WOOL 4 and FERTILIZER 2 at the close.

The walk has to start early enough that the DROP is followed by market turns, so the bound needs a
sell reserve on top of `dist + 1`.
"""

import pytest

SA = pytest.importorskip("kagg.search.schedule_agent")

TPD = 24
LAST_DAY = 29
DEPOT = (5, 4)


def _walks(hour, pos, held=None, day=LAST_DAY):
    return SA.must_walk_home_now(day, hour, pos, held or {"WOOL": 4}, [DEPOT])


def test_a_loaded_hand_leaves_early_enough_to_sell_what_it_drops():
    """**The acceptance test.** A hand two tiles out must already be walking well before the hour
    that merely lets it arrive: arriving is not banking, and banking is not selling."""
    pos = (5, 2)                                   # dist 2 -> walk 2, DROP 1
    drop_only = TPD - (SA.RT.dist(pos, DEPOT) + 1)  # the old bound, ignoring slack
    assert _walks(drop_only - SA.LAST_DAY_SELL_TURNS, pos), (
        "must be walking with the sell reserve still ahead of it")


def test_the_reserve_leaves_real_market_turns_after_the_drop():
    """The property the number has to have. Whatever the distance, the hour the walk begins plus the
    walk plus the DROP must still leave `LAST_DAY_SELL_TURNS` turns before the close."""
    for pos in [(5, 4), (5, 2), (2, 4), (0, 0)]:
        first = next(h for h in range(TPD) if _walks(h, pos))
        lands = first + SA.RT.dist(pos, DEPOT) + 1
        assert TPD - lands >= SA.LAST_DAY_SELL_TURNS, (pos, first, lands)


def test_an_empty_handed_unit_is_never_dragged_home():
    """Guard. The rule exists to bank a load; a unit holding nothing has nothing to bank and its
    turns are worth more spent working."""
    assert not _walks(0, (0, 0), held={})
    assert not _walks(20, (0, 0), held={"WOOL": 0})


def test_no_earlier_day_is_touched():
    """**The blast radius, and it is the reason this is safe.** Every day before the last banks its
    load in the closing sweep for free, so firing there would spend turns to buy nothing. `d29 only`
    is Alex's instruction and `upkeep_buys_nothing` is the gate that enforces it."""
    for day in (0, 10, 27, 28):
        assert not _walks(23, (0, 0), day=day)
