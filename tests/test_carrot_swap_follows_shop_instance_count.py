"""CARROT_SWAP: plant carrot instead of wheat once the shop draw actually favours carrot.

## Why this is a different question from what has already been asked and answered

Two things in this codebase already touch carrot, and neither is this:

- `CARROT_LATE` (a 0/1 timing dial) measured FLAT -- 65.1% vs 64.1% win rate over 384 games
  (`data/logs/exp_cow_carrot_2026-08-12.log`). It only moves WHEN carrot is planted, never WHETHER.
- `SHOP_ADAPT_CROPS`'s `("WHEAT", "CARROT")` pair (`REGISTER.md` C-23, `test_the_field_follows_the_
  shop_draw.py`) IS a board-conditional wheat<->carrot substitution, and it is OFF for a measured
  reason: scored in dollars via a season-long headroom model, it was measured TOGETHER with
  `("TOMATO", "STRAWBERRY")` at 0.806 vs HEAD's 0.871 over 232 matched games -- a real loss -- and
  independently, ladder-wide, carrot growers bank below the field median ($79,847 vs $82,136).

  That measurement is strong prior evidence against carrot as a crop full stop, and it is not
  neatly isolated: the 232-game sweep never separated `WHEAT<->CARROT` from
  `TOMATO<->STRAWBERRY`, and the swap sizing is a season-long dollar/headroom score, not the plain
  shop-instance count this file tests. This file exists to close that gap with its own mechanism,
  measured on its own -- see `docs/carrot_swap_2026-08-12.md` for the full record and the head-to-
  head with the numbers above.

## The mechanism under test

`_carrot_swap` counts unlocked shop INSTANCES from `kaggriculture.SHOPS`, weighting a
single-product shop double (the same convention `town_drain_remaining` already uses, because a
shop that buys only one thing drains it twice as fast as a shop with three). WHEAT is carried by
5 of 8 shop types (none single-product); CARROT by 2 -- `PET_CAFE` (single-product, doubled) and
`FARMERS_MARKET`. Only once carrot's weighted count strictly exceeds wheat's does anything move,
and only the schedule's still-UNPLANTED wheat -- ground already committed (`planted + live`) is
never re-labelled, the same anchor rule `_adapt_crops` uses one field over.

WHEAT and CARROT are cadence-compatible one-shots (`router.CROP_TABLE`): both `first_yield_day 2`,
`max_yield_day` 4 and 3. The swap is therefore free in tour-shape terms; it is not free in value --
WHEAT yields 6 units at $25 base ($150, $10 seed) against CARROT's 4 units at $35 base ($140, $20
seed) -- so this is a genuine trade, not a strict upgrade, which is exactly why it needs the shop
draw to justify it rather than being a permanent swap.
"""

import collections

import pytest

from kagg.search import schedule_agent_1455mh as SA
from kagg.search import router as RT


ALL_LAND = ("NW", "NE", "SW", "SE")


def blank_board(unlocked=ALL_LAND):
    return [["LOCKED" if RT.R.quadrant_of(x, y) not in unlocked else None
             for x in range(10)] for y in range(10)]


def sched_for(crop, qty, day=0):
    base = dict(plants=[], animals_bought={}, builds=0, places=[], hires=0, land=0,
                seeds={}, buys={}, sells={}, hands=0)
    out = {d: dict(base) for d in range(30)}
    out[day]["plants"] = [crop] * qty
    return out


def pin_crops(sched, day, shops):
    """The crops `_refresh_pins` chooses, given this shop draw. Fresh state every call."""
    state = dict(pins={}, planted=collections.Counter(), pen_for={})
    pins = SA._refresh_pins(state, sched, day, blank_board(), set(ALL_LAND),
                            unlocked_shops=list(shops))
    return collections.Counter(v[1] for v in pins.values() if v[0] == "PLANT")


#: Eight WHEAT-buying shop instances (weight 8), no CARROT anywhere (weight 0).
WHEAT_HEAVY_BOARD = ["BAKERY", "PIZZA_SHOP", "BRUNCH_SPOT", "ICE_CREAM_SHOP", "BAKERY",
                     "PIZZA_SHOP", "BRUNCH_SPOT", "ICE_CREAM_SHOP"]

#: Two PET_CAFEs (single-product, weight 2 each = 4) + FARMERS_MARKET (weight 1) = carrot 5,
#: against FARMERS_MARKET's own WHEAT weight of 1. Carrot strictly outweighs wheat, 5 to 1.
CARROT_HEAVY_BOARD = ["PET_CAFE", "PET_CAFE", "FARMERS_MARKET", "YARN_STORE", "YARN_STORE",
                      "SMOOTHIE_SHOP", "SMOOTHIE_SHOP", "SMOOTHIE_SHOP"]

#: One PET_CAFE (weight 2) against one BAKERY (weight 1): carrot leads, but not the tie case.
#: Used only where a board with SOME of each is needed.
MIXED_BOARD = ["PET_CAFE", "BAKERY", "YARN_STORE", "YARN_STORE", "YARN_STORE", "YARN_STORE",
              "YARN_STORE", "YARN_STORE"]

#: One PET_CAFE (weight 2) against two WHEAT shops (BAKERY + PIZZA_SHOP, weight 1 each = 2): a tie.
TIE_BOARD = ["PET_CAFE", "BAKERY", "PIZZA_SHOP", "YARN_STORE", "YARN_STORE", "YARN_STORE",
            "YARN_STORE", "YARN_STORE"]


def test_carrot_swap_ships_off_by_default():
    """The gate. OFF must restore current behaviour exactly -- see docs/carrot_swap_2026-08-12.md
    for the byte-identical grid check, which needs the full env harness and lives outside pytest."""
    assert SA.CARROT_SWAP is False


def test_carrot_shop_weights_counts_instances_and_doubles_single_product_shops():
    """The counting primitive, in isolation. Two PET_CAFEs = weight 4, not 2 -- duplicates count,
    and PET_CAFE is single-product so each instance is worth two of a multi-product shop's."""
    carrot_w, wheat_w = SA._carrot_shop_weights(CARROT_HEAVY_BOARD)
    assert carrot_w == 5, f"expected 2*PET_CAFE(2) + FARMERS_MARKET(1) = 5, got {carrot_w}"
    assert wheat_w == 1, f"expected FARMERS_MARKET(1) only, got {wheat_w}"

    carrot_w, wheat_w = SA._carrot_shop_weights(WHEAT_HEAVY_BOARD)
    assert carrot_w == 0
    assert wheat_w == 8, f"8 wheat-buying shop instances, none single-product, got {wheat_w}"


def test_carrot_swap_moves_unplanted_wheat_when_carrot_shops_outweigh_wheat_shops():
    """The core theory: a carrot-heavy draw moves wheat ground to carrot; a wheat-heavy draw does
    not. Same schedule (20 WHEAT), two draws -- only the shop mix differs."""
    carroty = SA._carrot_swap(collections.Counter({"WHEAT": 20}), collections.Counter(),
                              collections.Counter(), SA.CARROT_SWAP_FROM_DAY, CARROT_HEAVY_BOARD)
    wheaty = SA._carrot_swap(collections.Counter({"WHEAT": 20}), collections.Counter(),
                             collections.Counter(), SA.CARROT_SWAP_FROM_DAY, WHEAT_HEAVY_BOARD)
    assert carroty["CARROT"] > 0, f"carrot-heavy board did not swap anything: {dict(carroty)}"
    assert wheaty.get("CARROT", 0) == 0, f"wheat-heavy board swapped anyway: {dict(wheaty)}"
    assert wheaty["WHEAT"] == 20, "wheat-heavy board must keep the schedule's own row untouched"


def test_carrot_swap_requires_carrot_to_strictly_outweigh_wheat():
    """A tie must not swap -- ties fall to wheat, the schedule's own choice, exactly as
    `_adapt_crops` breaks ties toward the pair's first (cheaper-seed) member one field over."""
    tied = SA._carrot_swap(collections.Counter({"WHEAT": 20}), collections.Counter(),
                           collections.Counter(), SA.CARROT_SWAP_FROM_DAY, TIE_BOARD)
    assert tied.get("CARROT", 0) == 0, f"a tied draw swapped: {dict(tied)}"
    assert tied["WHEAT"] == 20


def test_carrot_swap_never_relabels_ground_already_planted():
    """The anchor rule. `planted + live` wheat must survive untouched -- only the schedule's
    still-unplanted remainder can move. This is the herd's `state['bought']` overshoot guard,
    the same one `_adapt_crops` needed for the identical reason one field over."""
    want = collections.Counter({"WHEAT": 20})
    planted = collections.Counter({"WHEAT": 12})
    live = collections.Counter({"WHEAT": 3})
    got = SA._carrot_swap(want, planted, live, SA.CARROT_SWAP_FROM_DAY, CARROT_HEAVY_BOARD)
    assert got["WHEAT"] >= 15, f"already-committed ground (12 planted + 3 live) was re-labelled: {dict(got)}"
    assert got["WHEAT"] + got.get("CARROT", 0) == 20, (
        f"pair total drifted from the schedule's 20: {dict(got)}")


def test_carrot_swap_keeps_the_pair_total_tile_count_unchanged():
    """The COUNT the schedule asks for is exactly preserved through `_refresh_pins`; only the crop
    label floats. Verified end-to-end, not just on the helper function directly."""
    sched = sched_for("WHEAT", 24)
    for shops in (CARROT_HEAVY_BOARD, WHEAT_HEAVY_BOARD, MIXED_BOARD, TIE_BOARD):
        was = SA.CARROT_SWAP
        SA.CARROT_SWAP = True
        try:
            got = pin_crops(sched, SA.CARROT_SWAP_FROM_DAY, shops)
        finally:
            SA.CARROT_SWAP = was
        assert sum(got.values()) == 24, f"{shops[0]} board: {dict(got)} != 24 tiles"


def test_carrot_swap_before_its_start_day_keeps_the_schedules_own_crop():
    """Before `CARROT_SWAP_FROM_DAY` the reference mix stands untouched, same reasoning as
    `CROP_ADAPT_FROM_DAY`: one shop draw is too little signal to commit ground against."""
    got = SA._carrot_swap(collections.Counter({"WHEAT": 20}), collections.Counter(),
                          collections.Counter(), SA.CARROT_SWAP_FROM_DAY - 1, CARROT_HEAVY_BOARD)
    assert got == collections.Counter({"WHEAT": 20}), (
        f"day {SA.CARROT_SWAP_FROM_DAY - 1} already swapped: {dict(got)}")


def test_carrot_swap_off_does_not_touch_refresh_pins_at_all():
    """The gate must be inert, not just default-off: with the flag False, a carrot-heavy board
    must plant identically to a wheat-heavy one. This is the property the byte-identical grid
    check in docs/carrot_swap_2026-08-12.md depends on."""
    sched = sched_for("WHEAT", 24)
    assert SA.CARROT_SWAP is False, "run this test with the flag at its shipped default"
    carroty = pin_crops(sched, SA.CARROT_SWAP_FROM_DAY, CARROT_HEAVY_BOARD)
    wheaty = pin_crops(sched, SA.CARROT_SWAP_FROM_DAY, WHEAT_HEAVY_BOARD)
    assert carroty == wheaty == collections.Counter({"WHEAT": 24}), (
        f"flag OFF still varied by board: carrot-board {dict(carroty)}, wheat-board {dict(wheaty)}")
