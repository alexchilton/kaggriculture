"""The herd's feed outranks the day's shopping in EVERY turn, not just hour 0.

`_wheat_row_first` already moves `BUY_PRODUCT WHEAT` in front of HIRE / BUY_ANIMAL / BUY_SEED, and
its reasoning is not about dawn at all -- `_process_market` walks the slots in order and
`_do_buy_product` re-checks the bank per unit (`kaggriculture.py:666-673`), so a late slot is paid
out of whatever the earlier ones left.  That is true on every turn of every day.  It is gated on
`hour == 0`.

Day 8 of the Kawashigi tape, seed 11, is decided at **h01**.  The row asks `WHEAT 17`; we emit:

    h00   SELL FERTILIZER 6, HIRE x9                              -- no wheat order at all
    h01   HIRE, HIRE, BUY_SEED WHEAT 5, BUY_SEED STRAWBERRY 4, BUY_PRODUCT WHEAT 13

with a bank of $440.  Ahead of the wheat in that same turn sit $144 of hires (the fibonacci ladder,
after nine hires at h00) and $450 of seed -- $400 of it STRAWBERRY at $100 a unit.  $594 committed
against $440, so ONE wheat clears.

The tape puts the feed first in both of its spending turns:

    h00   SELL FERTILIZER 6, HIRE x5, BUY_PRODUCT WHEAT 9, BUY_SEED WHEAT 3
    h05   SELL MILK 12, BUY_ANIMAL SHEEP 1, HIRE, BUY_PRODUCT WHEAT 2, BUY_SEED STRAWBERRY 4

`BUY_PRODUCT` before `BUY_SEED`, both times.

Day 8 totals 5 of 17 and it decomposes exactly: 0 at h00 (nothing asked), 1 at h01 (starved by the
seed), and four singles at h03-h06 -- four because `state["ordered"]` credited all thirteen queued
at h01, leaving `owed = 17 - 13 = 4`.  Then the asking stops while money arrives all afternoon.

This file covers the SLOT half.  SELLs are still never moved: a SELL settles before any atomic order
in a later slot, which is what lets a thin day fund its own purchases.

See `WHEAT_ROW_OUTRANKS_SHOPPING_ALL_DAY`.
"""
import importlib

import pytest

SA = importlib.import_module("kagg.search.schedule_agent_1455mh")


@pytest.fixture(autouse=True)
def _flags(monkeypatch):
    monkeypatch.setattr(SA, "WHEAT_ROW_OUTRANKS_SHOPPING", True)
    monkeypatch.setattr(SA, "WHEAT_ROW_OUTRANKS_SHOPPING_ALL_DAY", True)


def _d8_h01():
    """The real h01 order block, in the order the agent emits it."""
    return [["HIRE"], ["HIRE"],
            ["BUY_SEED", "WHEAT", 5], ["BUY_SEED", "STRAWBERRY", 4],
            ["BUY_PRODUCT", "WHEAT", 13]]


def _ops(orders):
    return [(o[0], o[1] if len(o) > 1 else None) for o in orders]


def test_the_feed_moves_ahead_of_the_seed_at_hour_one():
    out = SA._wheat_row_first(_d8_h01(), 1)
    ops = _ops(out)
    wheat = ops.index(("BUY_PRODUCT", "WHEAT"))
    straw = ops.index(("BUY_SEED", "STRAWBERRY"))
    assert wheat < straw, (
        "the herd's feed is still queued behind $400 of strawberry seed on a $440 bank\n"
        f"  order: {ops}"
    )


def test_it_still_works_at_hour_zero():
    """The existing behaviour is an extension of, not a replacement for, hour 0."""
    out = SA._wheat_row_first(_d8_h01(), 0)
    ops = _ops(out)
    assert ops.index(("BUY_PRODUCT", "WHEAT")) < ops.index(("BUY_SEED", "STRAWBERRY")), ops


def test_a_sell_is_never_moved():
    """A SELL settles before any atomic order in a later slot -- that is what funds a thin day."""
    orders = [["SELL", "FERTILIZER", 6], ["HIRE"], ["BUY_SEED", "STRAWBERRY", 4],
              ["BUY_PRODUCT", "WHEAT", 13]]
    out = SA._wheat_row_first(orders, 5)
    assert _ops(out)[0] == ("SELL", "FERTILIZER"), (
        f"the sell was displaced, so the turn can no longer fund itself\n  order: {_ops(out)}"
    )


def test_nothing_moves_when_the_feed_is_already_first():
    orders = [["BUY_PRODUCT", "WHEAT", 2], ["BUY_SEED", "STRAWBERRY", 4]]
    assert SA._wheat_row_first(list(orders), 7) == orders
