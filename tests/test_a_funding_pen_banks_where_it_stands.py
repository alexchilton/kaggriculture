"""A pen that funds the day banks its produce ON THE PEN, the turn after it is harvested.

Pens sit on shed-access tiles (`_refresh_pins`), so a hand standing on one is already standing on
the shed. Kawashigi's day 8, read off the raw replay -- he never walks anywhere to bank the milk:

    u4   h02 (4,4) PICKUP/WHEAT   h03 FEED   h04 CARE   h05 HARVEST   h06 PLACE/MILK
                                                                          ^ same tile, next turn

`SELL MILK 12` is in that same h06 order block, and the unit phase runs before `_process_market`
(`kaggriculture.py:922` then `:928`), so it lands and sells in one turn.

Ours banks on the way to the NEXT job instead: every delivery path in `materialise` computes
`d = nearest(depots, pos, j.tile)` for the TRANSITION, so the stop is planned as part of moving on.
On day 8 that put the milk in the shed at h07 with the banking flag on and h11 without it, against
a sale asked at h05. Measured on the forced-order run, the cost of those two hours:

    h05  bank $24  shed MILK 0   asked BWHEAx2 SMILKx12  -> ALL FAILED
    h08  bank $24  shed MILK 0   asked BWHEAx2           -> FAILED
    h10  bank $24  shed MILK 0   asked BWHEAx3           -> FAILED

The bank sits at $24 from h04 to midnight and seven wheat go unbought, while the town holds 9,900+
wheat all day. Stock never binds; cash does, and the cash is the milk.

`PLACE <item> <n>` is quantified (`kaggriculture.py:381-395`), so this costs ONE turn and no
movement, and the herd's ration stays in the hand -- `_bank` prefers it here on cost. See
`BANK_ON_THE_PEN_THAT_FUNDS_THE_DAY`.
"""
import importlib

import pytest

DP = importlib.import_module("kagg.search.cover")

SHED = [(4, 4), (4, 5), (5, 4), (5, 5)]


@pytest.fixture(autouse=True)
def _flags(monkeypatch):
    """Shipped defaults, except the flag under test. The point is that this works ALONE."""
    monkeypatch.setattr(DP, "BANK_ON_THE_PEN_THAT_FUNDS_THE_DAY", True)
    monkeypatch.setattr(DP, "BANK_THE_ROWS_PRODUCE_WHILE_REAPING", False)


def _cow(tile, ripe=True):
    ops = [("FEED", "WHEAT"), ("CARE", None), ("COLLECT_FERTILIZER", None)]
    gives = {}
    if ripe:
        ops.append(("HARVEST", None))
        gives = {"MILK": 6}
    j = DP.Job(tile, ops, needs={"WHEAT": 1}, gives=gives,
               products=frozenset({"MILK"} if ripe else set()))
    j.funds = ripe
    return j


def _route(work, carry=None):
    return DP.materialise((4, 4), work, carry=carry or {"WHEAT": 2}, depots=SHED,
                          wanted={"MILK": 12}, deliver=True, rush=True)


def _banked_at(route, tile):
    """Index of a depot stop on `tile` that banks MILK, or None."""
    for n, s in enumerate(route):
        if isinstance(s, DP.Depot) and tuple(s.tile) == tile and (s.drop or s.place.get("MILK")):
            return n
    return None


def test_the_milk_is_banked_on_the_pen_not_on_the_way_to_the_next_job():
    """A harvest still lies ahead, so every existing path refuses -- and this one must not."""
    work = [_cow((4, 4)), _cow((4, 5)), _cow((3, 3), ripe=False)]
    route = _route(work)
    first = next(n for n, s in enumerate(route) if isinstance(s, DP.Job) and s.tile == (4, 4))
    at = _banked_at(route, (4, 4))
    assert at is not None and at == first + 1, (
        "the milk is not banked on the pen the turn after it is harvested\n"
        f"  first ripe pen at route position {first}, bank at {at}\n  route: {route}"
    )


def test_it_banks_with_place_so_the_ration_survives():
    """One turn, no movement, and the wheat the next pen eats never leaves the hand."""
    work = [_cow((4, 4)), _cow((4, 5)), _cow((3, 3), ripe=False)]
    route = _route(work)
    at = _banked_at(route, (4, 4))
    stop = route[at]
    assert stop.place.get("MILK", 0) > 0 and not stop.drop, (
        f"banked with an all-or-nothing DROP instead of a quantified PLACE\n  stop: {stop!r}\n"
        f"  route: {route}"
    )
    assert stop.turns == 1, f"the on-pen bank cost {stop.turns} turns, not one\n  stop: {stop!r}"


def test_a_pen_that_is_not_on_shed_ground_is_left_alone():
    """The whole justification is that the pen IS the shed. Off it, this must not fire."""
    work = [_cow((0, 0)), _cow((4, 5)), _cow((3, 3), ripe=False)]
    route = _route(work)
    assert _banked_at(route, (0, 0)) is None, (
        f"planned a bank on (0,0), which is not shed ground\n  route: {route}"
    )


def test_a_pen_the_row_is_not_waiting_on_is_left_alone():
    """Not 'bank every harvest' -- only the produce the day's row is selling."""
    work = [_cow((4, 4)), _cow((4, 5)), _cow((3, 3), ripe=False)]
    route = DP.materialise((4, 4), work, carry={"WHEAT": 2}, depots=SHED,
                           wanted={"WHEAT": 20}, deliver=True, rush=True)
    first = next(n for n, s in enumerate(route) if isinstance(s, DP.Job) and s.tile == (4, 4))
    nxt = route[first + 1] if first + 1 < len(route) else None
    assert not (isinstance(nxt, DP.Depot) and nxt.place.get("MILK")), (
        f"banked milk on a day whose row does not sell it\n  route: {route}"
    )
