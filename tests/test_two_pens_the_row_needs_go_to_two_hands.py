"""Two pens the day's row is waiting on are worked in PARALLEL, not stacked on one hand.

Day 8 of the Kawashigi tape, seed 11.  `COW` is `first_yield_day 8`, so the two cows placed on day 0
open the day holding six units each -- twelve milk, which is exactly his `SELL MILK 12`.  That sale
is at h05 and it funds the day: the row is `sells {FERTILIZER 6, MILK 12}` and `buys {WHEAT 17}` on
a $4 dawn bank, and the wheat is what feeds ten animals.

His plan, read off the raw replay -- one hand per ripe pen, both banking into the shed together:

    u4   h02 (4,4) PICKUP/WHEAT   h03 FEED   h04 CARE   h05 HARVEST   h06 PLACE/MILK
    u2                                                  h04 HARVEST   h06 PLACE/MILK

Ours puts BOTH ripe cows on one hand, as jobs 0 and 1 of u4's tour:

    u4   0. (4,4) [FEED, CARE, COLLECT_FERTILIZER, HARVEST]  4t  funds
         1. (4,3) [FEED, CARE, COLLECT_FERTILIZER, HARVEST]  4t  funds

Both are correctly flagged `funds` and both are at the FRONT of the tour, so neither the ordering
nor the flag is wrong -- but eight turns of work run back to back on one hand, so the second cow's
milk cannot reach the shed before ~h08 however good the delivery rule is.  Two hours late fills
exactly as much as thirteen: forcing the tape's own d8 orders on top of an early-banking fix was
byte-identical, `sell 6/18`, because `SELL MILK 12` at h05 found an empty shed.

`greedy` ranks placements on `(added turns, unit, tile, index)` -- pure cheapest-insertion -- so
appending the second cow to the hand already standing on the first always wins.  That is the right
rule for ordinary work and the wrong one for the two stops the day's cash depends on.

See `ONE_HAND_PER_FUNDING_PEN`.
"""
import importlib

import pytest

DP = importlib.import_module("kagg.search.cover")

SHED = [(4, 4)]


def _pen(tile, ripe=False):
    """A pen. A ripe one yields the product the row is waiting for, so it FUNDS the day."""
    ops = [("FEED", "WHEAT"), ("CARE", None), ("COLLECT_FERTILIZER", None)]
    gives = {}
    if ripe:
        ops.append(("HARVEST", None))
        gives = {"MILK": 6}
    j = DP.Job(tile, ops, gives=gives, products=frozenset({"MILK"} if ripe else set()))
    j.funds = ripe
    return j


def _routes(units, jobs, budget):
    work, _unc = DP.cover(units, jobs, budget, depots=SHED, wanted={"MILK": 12}, rush=True, day=8)
    return work


def _home(work, tile):
    for u, seq in work.items():
        for j in seq:
            if j.tile == tile:
                return u
    return None


def test_the_two_ripe_pens_do_not_land_on_the_same_hand():
    """The measurement that matters: two hands, so the two harvests happen at the same time."""
    ripe = [(4, 4), (4, 3)]
    jobs = [_pen(ripe[0], ripe=True), _pen(ripe[1], ripe=True),
            _pen((3, 3)), _pen((3, 4))]
    work = _routes([(4, 4), (4, 5)], jobs, [24, 24])
    a, b = _home(work, ripe[0]), _home(work, ripe[1])
    assert a is not None and b is not None, f"a ripe pen was dropped entirely\n  work: {work}"
    assert a != b, (
        f"both ripe pens went to hand u{a}, so their harvests run back to back\n"
        f"  work: { {u: [j.tile for j in s] for u, s in work.items()} }"
    )


def test_a_third_ripe_pen_still_finds_a_hand():
    """The rule is a PREFERENCE, never a refusal -- it must not leave a funding pen uncovered."""
    ripe = [(4, 4), (4, 3), (3, 4)]
    jobs = [_pen(t, ripe=True) for t in ripe] + [_pen((3, 3))]
    work = _routes([(4, 4), (4, 5)], jobs, [24, 24])
    for t in ripe:
        assert _home(work, t) is not None, (
            f"ripe pen {t} left uncovered by the spread rule\n"
            f"  work: { {u: [j.tile for j in s] for u, s in work.items()} }"
        )


def test_ordinary_pens_still_pack_onto_one_hand():
    """Nothing about ordinary work changes -- cheapest insertion is right for it.

    Without this the rule would be a general round-robin, which is measured in `greedy`'s own
    docstring as converting 776 idle turns into 742 extra moves for no extra work.
    """
    jobs = [_pen(t) for t in [(4, 4), (4, 3), (3, 3), (3, 4)]]
    work = _routes([(4, 4), (0, 0)], jobs, [24, 24])
    sizes = sorted(len(s) for s in work.values() if s)
    assert sizes and sizes[-1] >= 3, (
        f"ordinary pens were spread across hands instead of chained\n"
        f"  work: { {u: [j.tile for j in s] for u, s in work.items()} }"
    )
