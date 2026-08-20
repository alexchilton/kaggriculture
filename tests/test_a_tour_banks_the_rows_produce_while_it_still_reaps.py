"""Produce the row is SELLING today reaches the shed while the market is open, not at dusk.

`BANK_ONLY_AFTER_THE_LAST_HARVEST` is read off Seb's day 4, where the harvest is REVENUE -- nothing
that day depends on it, so it can wait for the closing trip.  Day 8 of the Kawashigi tape is the
opposite case and the rule is wrong there.

Measured, seed 11, day 8 -- the first milk day.  `COW` is `first_yield_day 8`, so the two cows
placed on day 0 open the day holding six units each, and both boards agree on it:

    ours d8 dawn   CO@3,4 y6   CO@4,4 y6      tape d8 dawn   CO@4,3 y6   CO@4,4 y6

The row is `sells {FERTILIZER 6, MILK 12}` and `buys {WHEAT 17}` on a $4 dawn bank, so that milk is
not revenue, it is the day's WORKING CAPITAL -- the wheat it pays for is what feeds ten animals.
We harvest all twelve units and sell all twelve, thirteen hours late:

    h05  u4 HARVEST      h08  u4 HARVEST      h09-h17  twelve milk in hand, bank $13
    h17  u4 DROP         h18  shed 12, SELL MILK 12     h19  bank $1,873, nothing left to buy

The tape banks the same milk at h05 with two `PLACE/MILK` and spends it through the day.  It closes
`feed 10/10` and `care 10/10`; we close 2 and 2.

`reaping` is the only thing stopping it -- with the flag forced off in a probe the milk reaches the
shed at h07 and h12 and the money lands at h09 and h13.

Two conditions have to hold together to open it, and NEITHER works alone:

    the row sells it     true on Seb's day 4 as well, where fourteen wheat harvests meet a
                         `WHEAT 49` row and banking at dusk is exactly right.  On its own it
                         deletes `BANK_ONLY_AFTER_THE_LAST_HARVEST` outright.
    `rush`               on its own it is the reverted `BANK_MID_TOUR_WHEN_THE_DAY_IS_UNFUNDED`,
                         which fired on fertilizer rounds too and cost d6 `buy_product 5/5 -> 4/5`.

Measured per day, seed 11: `rush` is True on d1, d6 and d8 and False on d0, d2-d5, d7 and d9-d12.

It also has to be folded into `reaping` itself rather than into one branch.  Traced on d8, all
1,678 blocked stops read `owed=False`, so they fall to the FREE DROP and never reach the selective
`_bank` branch, which requires `owed_ahead` -- an exemption written for that branch alone measured
as a byte-identical day 8.  See `BANK_THE_ROWS_PRODUCE_WHILE_REAPING`.
"""
import importlib

import pytest

DP = importlib.import_module("kagg.search.cover")

SHED = [(4, 4)]


@pytest.fixture(autouse=True)
def _flag_on(monkeypatch):
    """The mechanism is tested here; the SHIPPED DEFAULT is False.

    Measured on the 17-day grid, seed 11, kawashigi -- switching it on gains 18 exact cells
    (447 -> 465: the herd goes 13/14 -> 14/14 from d10, and feed/care reach 14/14 on five days)
    and loses $1,098 over the season, mostly on d9 and d10 where sells drop 22/25 -> 17/25 and
    78/91 -> 69/91.  d8's own target cells do not move at all: `buy_product 5/17`, `feed 2/10`
    and `care 2/10` are identical either way.

    It is off because the cash it frees on d8 has nothing to buy.  The wheat row credits
    `state["ordered"]` when an order is QUEUED, so the twelve units the book refused at h01 drive
    `owed` to 0 and the row is never re-offered, however much money lands at h08.  Turn that
    around -- credit the FILL -- and this becomes worth re-measuring on top of it.
    """
    monkeypatch.setattr(DP, "BANK_THE_ROWS_PRODUCE_WHILE_REAPING", True)


def _cow(tile):
    """A pen holding six milk: the produce, and the reason `reaping` is true."""
    return DP.Job(tile, [("HARVEST", None)], gives={"MILK": 6}, products=frozenset({"MILK"}))


def _pen(tile):
    """A feed stop, so the hand is carrying a ration that a DROP would bin."""
    return DP.Job(tile, [("FEED", None)], needs={"WHEAT": 1})


def _tour():
    """Harvest a cow, feed a pen, harvest a second cow -- standing on the shed between each.

    The hand carries exactly the wheat the pen ahead will eat, so the ration is `owed_ahead` and
    the milk is the only surplus.
    """
    work = [_cow((4, 3)), _pen((4, 5)), _cow((3, 4))]
    return work, DP.materialise((4, 4), work, carry={"WHEAT": 1}, depots=SHED,
                                wanted={"MILK": 12}, deliver=True, rush=True)


def _last_harvest(route):
    return max((n for n, s in enumerate(route) if isinstance(s, DP.Job) and s.harvests()),
               default=-1)


def test_the_milk_is_banked_before_the_last_cow_is_reached():
    work, route = _tour()
    last = _last_harvest(route)
    banked = [n for n, s in enumerate(route[:last])
              if isinstance(s, DP.Depot) and (s.drop or s.place.get("MILK", 0) > 0)]
    assert banked, (
        "six milk stay in hand until the tour finishes reaping, so the market never sees them "
        f"while it is open\n  last harvest at route position {last}\n  route: {route}"
    )


def test_the_ration_is_not_dumped_to_bank_the_milk():
    """A hand that DOES owe a ration ahead banks selectively, with `PLACE`.

    `_bank` chooses on cost -- `PLACE MILK` is one turn against `DROP` plus a `PICKUP WHEAT` at
    two -- so the wheat its next pen is about to eat never leaves the hand.  Binning and re-drawing
    the ration is what shifted the cash timing when this was tried as a `rush`-only exemption.
    """
    work, route = _tour()
    last = _last_harvest(route)
    dumps = [n for n, s in enumerate(route[:last]) if isinstance(s, DP.Depot) and s.drop]
    assert not dumps, (
        f"banked the milk with an all-or-nothing DROP at {dumps}, binning the pen's ration\n"
        f"  route: {route}"
    )
    placed = [s for s in route[:last] if isinstance(s, DP.Depot) and s.place.get("MILK", 0) > 0]
    assert placed, f"no quantified PLACE of the milk before the last harvest\n  route: {route}"


def test_the_free_drop_is_reached_when_nothing_is_owed_ahead():
    """The shape day 8 ACTUALLY has, and the reason this cannot live in one branch.

    Traced on d8, every one of the 1,678 stops blocked by `reaping` reads

        free=True  spare=7  owed=False  held={FERTILIZER 1, MILK 6}  after={}

    -- nothing owed ahead, so the hand falls to the FREE DROP and never reaches the selective
    `_bank` branch, which requires `owed_ahead`.  An exemption written for the selective branch
    alone measured as a byte-identical day 8.

    The free drop is safe here by construction: it already refuses whenever anything in the hand is
    owed to a later job, so the all-or-nothing `DROP` has no ration to bin.
    """
    work = [_cow((4, 3)), DP.Job((4, 5), [("WATER", None)]), _cow((3, 4))]
    route = DP.materialise((4, 4), work, depots=SHED, wanted={"MILK": 12}, deliver=True, rush=True)
    last = _last_harvest(route)
    banked = [n for n, s in enumerate(route[:last]) if isinstance(s, DP.Depot)]
    assert banked, (
        "a hand owing nothing ahead still carries the row's milk past the shed to dusk\n"
        f"  last harvest at route position {last}\n  route: {route}"
    )


def test_a_row_that_does_not_sell_the_produce_still_waits_for_dusk():
    """The exemption is 'the row is waiting for it', not 'bank whenever'.

    With the milk unsold today there is nothing to fund, so
    `BANK_ONLY_AFTER_THE_LAST_HARVEST` must still hold and the tour must walk past the shed.
    """
    work = [_cow((4, 3)), _pen((4, 5)), _cow((3, 4))]
    route = DP.materialise((4, 4), work, carry={"WHEAT": 1}, depots=SHED,
                           wanted={"WHEAT": 20}, deliver=True, rush=True)
    last = _last_harvest(route)
    early = [n for n, s in enumerate(route[:last]) if isinstance(s, DP.Depot)]
    assert not early, (
        f"banked at {early} on a day whose row does not sell milk\n  route: {route}"
    )


def test_a_day_that_can_pay_its_own_bill_still_waits_for_dusk():
    """`rush` is the other half, and it is what keeps Seb's day 4 intact.

    A day whose row sells the produce but which is NOT short of cash has nothing waiting on the
    sale, so the harvest is revenue and the closing trip is the right place for it.  Without this
    half the exemption fires on every harvest day and deletes the rule it is amending.
    """
    work = [_cow((4, 3)), _pen((4, 5)), _cow((3, 4))]
    route = DP.materialise((4, 4), work, carry={"WHEAT": 1}, depots=SHED,
                           wanted={"MILK": 12}, deliver=True, rush=False)
    last = _last_harvest(route)
    early = [n for n, s in enumerate(route[:last]) if isinstance(s, DP.Depot)]
    assert not early, (
        f"banked at {early} on a day that can pay its own bill\n  route: {route}"
    )
