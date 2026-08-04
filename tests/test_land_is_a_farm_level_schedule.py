"""Land is bought once by the farm, not once per chain that happens to want it.

`_do_buy_land` ignores which quadrant the caller wanted and unlocks `LAND_ORDER[n_already_bought]`.
So a BUY_LAND order is a claim on a **shared, ordered, farm-level** resource, and two chains that each
privately order "the parcels I need" over-buy the moment their days differ.

Measured before this fix -- a pen on NE wanting its ground by day 7 and a pen on SW wanting its ground
by day 10:

    BUY_LAND orders at days [7, 10, 11]
    3 orders = $7,000 spent, when NE + SW is $3,000

The third order buys SE, which nothing asked for and which the leader never buys at all. It hid
because every chain used to share one `land_day` -- `ranch()` writes `buy_land[t] = 1` by assignment,
so identical days collapsed onto the same turns and the count came out right by accident. Give the
chains different days, which is exactly the leader's shape (**NE day 7, SW day 10**), and the farm
quietly spends $4,000 it does not have.

The fix belongs in `decode()`, not in the routines: only the whole genome knows which quadrants are
wanted and by when. A routine keeps emitting its own land when used standalone, because
`tests/test_land_orders_are_spaced.py` and the herd measurements rely on that.
"""

import numpy as np

from kagg.search import chains as C
from kagg.search import routines as R

NE_CELL = (5, 4)          # 1 parcel
SW_CELL = (4, 5)          # 2 parcels cumulative
SE_CELL = (5, 5)          # 3 parcels cumulative


def _land_days(script):
    """One entry per BUY_LAND *order*, not per turn that holds one.

    `build_script_submission.market_orders` emits `[["BUY_LAND"]] * buy_land[t]`, since HIRE and
    BUY_LAND are atomic per order *slot* rather than per turn. So two orders on one turn is two
    parcels, and counting nonzero turns would undercount.
    """
    b = np.asarray(script.buy_land)
    return [int(t) // R.TURNS_PER_DAY for t in np.flatnonzero(b > 0) for _ in range(int(b[t]))]


def _genome(rows, n_slots=8):
    """`rows` is a list of `(kind, what, tile, start_day, land_day)`."""
    g = np.zeros((n_slots, len(C.GENES)), dtype=np.int64)
    for slot, (kind, what, tile, start_day, land_day) in enumerate(rows):
        block_i = (C.RANCH_TILES.index(tile) if kind == "ranch"
                   else next(i for i, b in enumerate(C.BLOCKS) if b[0] == tile))
        what_i = (R.ANIMAL_NAMES if kind == "ranch" else R.CROPS).index(what)
        row = [C.KINDS.index(kind), what_i, block_i,
               C.START_DAY_CHOICES.index(start_day), C.LAND_DAY_CHOICES.index(land_day)]
        # Pad the option genes rather than listing them: every gene added to GENES has otherwise
        # broken every literal row in this suite, three times so far.
        g[slot] = row + [0] * (len(C.GENES) - len(row))
    return g.reshape(-1)


def test_the_premise_land_is_bought_in_a_fixed_order():
    assert R.LAND_ORDER == ["NE", "SW", "SE"]
    assert R.land_purchases_for(NE_CELL) == 1
    assert R.land_purchases_for(SW_CELL) == 2
    assert R.land_purchases_for(SE_CELL) == 3


def test_two_chains_on_different_days_buy_two_parcels_not_three():
    """The core claim, and the leader's exact shape: NE by day 7, SW by day 10."""
    script, _used, _skipped = C.decode(
        _genome([("ranch", "COW", NE_CELL, 9, 7), ("ranch", "COW", SW_CELL, 12, 10)]), 8)
    days = _land_days(script)
    assert len(days) == 2, (
        f"{len(days)} BUY_LAND orders on days {days}; NE + SW is two parcels and $3,000, a third "
        f"order buys SE for $4,000 that nothing asked for")
    assert days == [7, 10], f"expected the parcels on days 7 and 10, got {days}"


def test_a_shared_day_still_buys_the_right_count():
    """The case that used to work by accident must keep working."""
    script, _used, _skipped = C.decode(
        _genome([("ranch", "COW", NE_CELL, 9, 7), ("ranch", "COW", SW_CELL, 9, 7)]), 8)
    days = _land_days(script)
    assert len(days) == 2, f"got {days}"
    assert days[0] == 7, f"the first parcel was wanted by day 7, got {days}"
    # Spread, not stacked: two parcels resolving in one turn are judged against one day's bank.
    assert days[1] > days[0], f"both parcels land on day {days[0]}; $3,000 in one day"


def test_the_earliest_request_wins_for_each_parcel():
    """Parcel `j` is bought as soon as the *first* chain needing it says so, and never earlier than
    parcel `j-1` -- they unlock in sequence, so an out-of-order day would be meaningless."""
    script, _used, _skipped = C.decode(
        _genome([("ranch", "COW", SW_CELL, 14, 12),      # needs NE then SW, wants them by 12
                 ("ranch", "COW", NE_CELL, 8, 5)]), 8)   # needs NE only, wants it by 5
    days = _land_days(script)
    assert days == sorted(days), f"parcels must be ordered non-decreasingly, got {days}"
    assert days[0] == 5, f"NE was wanted by day 5 and is bought on day {days[0]}"


def test_a_farm_wanting_nothing_buys_nothing():
    """Every NW chain: no orders at all, so an all-NW genome never touches its bank."""
    nw_tile = next(b[0] for b in C.BLOCKS if C.land_cost(b[0]) == 0)
    script, _used, _skipped = C.decode(
        _genome([("grow", "MELON", nw_tile, 2, 0)]), 8)
    assert _land_days(script) == []


def test_a_routine_on_its_own_still_buys_its_own_land():
    """`decode()` owns the schedule, but a routine used directly must remain self-sufficient --
    `tests/test_land_orders_are_spaced.py` and the herd sweeps depend on it."""
    s = R.ranch(R.Script(), "COW", SW_CELL, start_day=12, land_day=10)
    assert _land_days(s) == [10, 11], "a standalone chain still spaces its own parcels one per day"
