"""A hand does not put the herd's dinner in the shed on a day whose market sells it.

`REDRAW_RATHER_THAN_CARRY` (`cover.py:582`) lets a hand standing on a depot bank the row's produce
and "take its wheat straight back". The re-draw is planned as a certainty. It is not one:
`_process_market` runs AFTER the unit phase in the same turn (`kaggriculture.py:922` then `:928`),
so a SELL order in that turn lifts the goods out of the shed BEFORE the hand comes back for them --
and on this board the row's produce and the herd's dinner are the same commodity.

Measured, seed 11 day 4, Seb's tape. Our herd hand u4 runs one tour over four pens:

    h1  PICKUP COW 1     h2  PICKUP WHEAT 4    h3  FEED (4,4)   h4 CARE   h5 COLLECT_FERTILIZER
    h6  DROP                                   <- banks 1 fertilizer, sheds 3 wheat with it
    h7  PICKUP COW 1     h8  PICKUP WHEAT 1    <- asked for 3; the market sold the rest
    h10 FEED (4,3)       h11 CARE
    h14 PLACE COW (3,3)                        <- arrives empty; the cow is never fed or cared for

The day's orders sell `WHEAT 5/12/12/20` and `FERTILIZER 5/1`, and the h6 turn sells one of each.
The shed then reads empty from h9 to h18, so `FETCH_THE_FEED_AND_RETURN` cannot rescue it either --
its gate is `shed["WHEAT"] > 0`. Result on the tape grid: `feed 5/7`, `care 5/7`.

**Seb never makes the trip.** On the same day and the same board he draws the whole shed at dawn
across TWO carriers (`u1 PICKUP WHEAT 3` at h1, `u2 PICKUP WHEAT 3` at h2), sends a third hand out
with the cow, and emits no DROP at all before h18 -- every one of his seven drops is the closing
bank run. He buys exactly the wheat we buy: 6 in the shed at dawn, 1 purchased. He is not better
supplied; he simply never spends a wheat on a round trip. See `docs/how_seb_feeds_the_herd.md`.

So the rule is not "never re-draw". It is: **do not bank an item the day's own SELL row is going to
lift out of the shed while you are standing next to it.** A hand carrying fertilizer for the market
and wheat for four pens must keep the lot and deliver at the end, exactly as the free drop above it
already refuses to do when anything is owed ahead.
"""
import collections

import pytest

from kagg.search import cover as DP

SHED = DP.SHED[0]


def _pen(tile, place=None):
    """A pen's day: feed it, care for it, take the fertilizer. `place` puts an animal in first.

    `gives` is load-bearing here and not decoration. `materialise` decides whether to bank a load
    from what the tour PREDICTS the hand will be holding, and a pen that does not declare its
    fertilizer never accumulates one -- so `spare` stays 0 and no drop is ever considered. A first
    cut of this file omitted it and all five tests passed against the very defect they describe.
    """
    ops = ([("PLACE", place)] if place else []) + [("FEED", "WHEAT"), ("CARE", None)]
    gives = None
    if not place:
        ops.append(("COLLECT_FERTILIZER", None))
        gives = {"FERTILIZER": 1}
    return DP.Job(tile, ops, gives=gives, products=frozenset(gives or ()))


def _d4_herd_tour():
    """The four pens our day-4 herd hand is given, in the order `materialise` receives them."""
    return [_pen((4, 4)), _pen((4, 3)), _pen((3, 3), place="COW"), _pen((4, 2))]


def _drops_before_the_last_pen(route):
    """Every mid-tour DROP: a depot that empties the hand while pens are still ahead."""
    last_job = max(i for i, stop in enumerate(route) if not getattr(stop, "depot", False))
    return [i for i, stop in enumerate(route[:last_job])
            if getattr(stop, "depot", False) and stop.drop]


def test_a_tour_that_still_owes_wheat_does_not_bank_it_where_the_market_will_sell_it():
    """The day-4 tour, with a row that sells both wheat and fertilizer. No mid-tour DROP.

    This is the failing case. `wanted` carries WHEAT because the row sells 49 of it, which is
    exactly what makes the re-draw unsafe -- the same shed, the same turn, and the market goes
    second.
    """
    work = _d4_herd_tour()
    route = DP.materialise(SHED, work, carry=None, depots=DP.SHED,
                           wanted={"WHEAT": 49, "FERTILIZER": 6}, deliver=True)
    bad = _drops_before_the_last_pen(route)
    assert not bad, (
        "the tour banks its load at "
        + ", ".join(repr(route[i]) for i in bad)
        + " while pens ahead still owe WHEAT, on a day whose row sells WHEAT -- the market lifts it "
          "out of the shed in the same turn and the re-draw comes back short.\nroute: "
        + " -> ".join(repr(s) for s in route))


def test_the_redraw_is_still_allowed_when_the_row_is_not_selling_the_feed():
    """The rule that is being narrowed, not deleted.

    `REDRAW_RATHER_THAN_CARRY` was added for a measured reason: on day 1 a hand held fertilizer
    from h5 to h16 and we sold four units for $2 less than the tape because we cannot spread what
    is not in the shed. That case is a row selling FERTILIZER only. Nothing there competes with the
    wheat, so the drop-and-redraw is safe and must survive.
    """
    work = _d4_herd_tour()
    route = DP.materialise(SHED, work, carry=None, depots=DP.SHED,
                           wanted={"FERTILIZER": 6}, deliver=True)
    stops = [s for s in route if getattr(s, "depot", False) and s.drop]
    assert stops, (
        "narrowing the rule to 'not an item the row sells' must not switch it off entirely -- a row "
        "that sells only FERTILIZER leaves the wheat uncontested and the hand should still bank and "
        f"re-draw.\nroute: {' -> '.join(repr(s) for s in route)}")


def test_a_tour_owing_nothing_ahead_still_drops_freely():
    """`DROP_WHERE_THE_TOUR_ALREADY_STANDS` is untouched: the last pen owes nothing after it."""
    work = [_pen((4, 4))]
    route = DP.materialise(SHED, work, carry=collections.Counter({"FERTILIZER": 4}),
                           depots=DP.SHED, wanted={"FERTILIZER": 6}, deliver=True)
    assert any(getattr(s, "depot", False) and s.drop for s in route), (
        "a hand with nothing owed ahead must still bank its produce.\nroute: "
        + " -> ".join(repr(s) for s in route))


@pytest.mark.parametrize("wanted", [{"WHEAT": 49, "FERTILIZER": 6}, {"WHEAT": 5}])
def test_the_placed_cows_pen_keeps_its_feed_in_hand(wanted):
    """Whatever else the tour does, the wheat for the PLACE stop must still be in hand when it
    arrives.

    Walks the route the way the executor does -- a Depot with `drop` empties the hand, a `pick`
    fills it -- and checks the balance at the moment the placement stop is reached. This is the
    invariant the day-4 failure violates, stated without reference to any particular rule, so a
    future flag that reintroduces the round trip by another route still breaks a named test.
    """
    work = _d4_herd_tour()
    route = DP.materialise(SHED, work, carry=None, depots=DP.SHED, wanted=wanted, deliver=True)
    hand = collections.Counter()
    for stop in route:
        if getattr(stop, "depot", False):
            if stop.drop:
                hand = collections.Counter()
            hand.update(stop.pick)
            continue
        if any(o == "PLACE" for o, _i in stop.ops):
            assert hand["WHEAT"] > 0, (
                f"the hand reaches the placement at {stop.tile} holding {dict(hand)} -- no wheat, so "
                f"the animal it puts in the ground cannot be fed today and starts its "
                f"`consecutive_unfed` count.\nroute: {' -> '.join(repr(s) for s in route)}")
        for op, item in stop.ops:
            if item and op in DP.DRAWN and hand[item] > 0 and op != "PLACE":
                hand[item] -= 1
