"""The field should follow the shops, exactly as the herd already does. Today it does not.

`_refresh_pins` builds its planting target from the reference schedule's `plants` rows and nothing
else:

    want = collections.Counter()
    for d in sorted(sched):
        if d <= day:
            want.update(sched[d].get("plants") or [])

No part of that path reads `town["unlocked_shops"]`, so the same 24 WHEAT / 17 MELON / 41
STRAWBERRY goes into the ground on every board. `SHOP_ADAPT_HERD` already fixed exactly this defect
for COW/SHEEP; this is the same defect one field over.

## What the draw actually does to demand

Measured off the 87 recorded ladder tapes in `data/seed_scripts/top_guys`, reading each game's
closing `market.inventory` and its own `town.unlocked_shops`. Units the town removes over a season:

    STRAWBERRY      387  ..  1282     4 shop types of 8 carry it
    CARROT           29  ..   924     2 of 8, but PET_CAFE is single-product so it counts double
    TOMATO          208  ..   924     2 of 8
    WHEAT           745  ..  1282     5 of 8, the most widely carried
    MELON            29  ..    29     0 of 8 -- the town centre alone, on EVERY board

A 3.3x swing on strawberry and a 32x swing on carrot is not noise, and it is knowable: shops are
`shared: True` in the observation, so the draw is a fact we are handed and currently discard.

## Why these two pairs and no others

The herd swap is free because COW and SHEEP both build a PASTURE, so nothing in the build schedule,
the geometry or the routing moves. The crop analogue of "same pen" is "same cadence", because the
cadence is what the tour is cut against:

    WHEAT      first_yield_day 2   one-shot    max_yield_day 4
    CARROT     first_yield_day 2   one-shot    max_yield_day 3
    TOMATO     first_yield_day 8   ongoing     interval 1
    STRAWBERRY first_yield_day 10  ongoing     interval 2

`(WHEAT, CARROT)` are both short one-shots yielding from day 2; `(TOMATO, STRAWBERRY)` are both
ongoing crops that hold their tile for the rest of the season. Swapping inside a pair leaves the
watering rhythm and the harvest rhythm intact.

**MELON is deliberately not in any pair.** Its appetite is 29 on every board there is, so whether to
plant it is not a question the shop draw can answer -- it is a fixed-quantity question, and a
different one. Bundling it here would confound the two.
"""

import collections

import pytest

from kagg.search import schedule_agent as SA
from kagg.search import router as RT


#: All four quadrants, because the schedule's 41 strawberry tiles do not fit in NW's 25 and a pin
#: loop that runs out of ground measures the board, not the rule.
ALL_LAND = ("NW", "NE", "SW", "SE")


def blank_board(unlocked=ALL_LAND):
    return [["LOCKED" if RT.R.quadrant_of(x, y) not in unlocked else None
             for x in range(10)] for y in range(10)]


def sched_for(crop, qty, day=0):
    """A schedule whose only instruction is `qty` plantings of `crop`, placed on `day`."""
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


#: Four SMOOTHIE_SHOPs carry STRAWBERRY and MILK only -- no TOMATO at all. Drawn on seed 91001027,
#: whose closing book shows STRAWBERRY absorption 1282 against TOMATO 208.
STRAWBERRY_BOARD = ["SMOOTHIE_SHOP"] * 4 + ["BAKERY", "BRUNCH_SPOT", "BRUNCH_SPOT", "FARMERS_MARKET"]

#: Five PIZZA_SHOPs carry TOMATO, MILK and WHEAT -- no STRAWBERRY. Drawn on seed 91019456, whose
#: closing book shows TOMATO absorption 924 against STRAWBERRY 387.
TOMATO_BOARD = ["PIZZA_SHOP"] * 5 + ["BAKERY", "BRUNCH_SPOT", "SMOOTHIE_SHOP"]

#: Two PET_CAFEs. Single-product, so each counts double: CARROT absorption 924 on seed 90997714.
CARROT_BOARD = ["PET_CAFE"] * 2 + ["BAKERY", "BRUNCH_SPOT", "FARMERS_MARKET", "ICE_CREAM_SHOP",
                                   "PIZZA_SHOP", "SMOOTHIE_SHOP"]

#: No PET_CAFE and no FARMERS_MARKET, so nothing carries CARROT: absorption 29, seed 91019456.
WHEAT_BOARD = ["PIZZA_SHOP"] * 5 + ["BAKERY", "BRUNCH_SPOT", "SMOOTHIE_SHOP"]


#: What the reference schedule actually asks for, and therefore the scale at which this decision is
#: taken. It matters here: TOMATO and STRAWBERRY are worth the SAME per tile -- 2 cycles x 4 units x
#: $60 against 1 cycle x 4 x $120, both $480 gross, both $100 of seed -- so nothing separates them
#: until one of the two books runs out of room. At 20 tiles neither does, and the pair is a coin
#: flip; at 41 the tomato book on a strawberry-heavy draw saturates and the rest must go to
#: strawberry. Testing the pair below its saturation point would only measure the tie-break.
SCHEDULE_STRAWBERRY_TILES = 41


def test_the_crop_swap_is_disabled_and_stays_disabled():
    """The pairs below swap toward crops the whole ladder has priced at zero. Evidence, not opinion.

    Every PLANT action in the official episode datasets for 2026-08-09 and -10, 2,744 seats:

        WHEAT 69.3%   STRAWBERRY 20.0%   MELON 10.5%   CARROT 0.2%   TOMATO 0.0%

    TOMATO is three actions in one game all season. Carrot growers bank below the field median.
    The local ladder sweep agreed independently at 0.806 against 0.871 over 232 matched games.

    This test is the record of that decision, so re-enabling the flag with these pairs goes red
    rather than quietly shipping. The mechanism itself is still exercised by the tests below, which
    call `_adapt_crops` directly -- it works, it is simply aimed wrong, and the note on the flag
    explains why no correct pair exists until the headroom model prices a marginal unit off the
    curve instead of counting the town's drain.
    """
    assert SA.SHOP_ADAPT_CROPS is False, (
        "SHOP_ADAPT_CROPS was re-enabled -- read its docstring and "
        "docs/the_ladder_is_two_scripts.md before changing this")


def adapt_only(crop, qty, day, shops, planted=None):
    """`_adapt_crops` on its own, bypassing the disabled flag, so the mechanism stays covered."""
    return SA._adapt_crops(collections.Counter({crop: qty}),
                           planted or collections.Counter(), collections.Counter(),
                           day, list(shops), 29)


def test_a_strawberry_row_becomes_tomato_when_no_shop_wants_strawberry():
    """The ongoing pair. Same schedule, two draws; the crop must follow the draw."""
    rich = adapt_only("STRAWBERRY", SCHEDULE_STRAWBERRY_TILES, SA.CROP_ADAPT_FROM_DAY,
                      STRAWBERRY_BOARD)
    poor = adapt_only("STRAWBERRY", SCHEDULE_STRAWBERRY_TILES, SA.CROP_ADAPT_FROM_DAY,
                      TOMATO_BOARD)
    assert rich["STRAWBERRY"] > poor["STRAWBERRY"], (
        f"identical planting on both boards: strawberry-rich {dict(rich)}, tomato-rich {dict(poor)}")
    assert poor["TOMATO"] > rich["TOMATO"], (
        f"the freed tiles did not become tomato: {dict(poor)}")


def test_a_wheat_row_becomes_carrot_when_the_town_eats_carrot():
    """The short one-shot pair. PET_CAFE is single-product, so it drains carrot twice as fast."""
    carroty = adapt_only("WHEAT", 20, SA.CROP_ADAPT_FROM_DAY, CARROT_BOARD)
    wheaty = adapt_only("WHEAT", 20, SA.CROP_ADAPT_FROM_DAY, WHEAT_BOARD)
    assert carroty["CARROT"] > wheaty["CARROT"], (
        f"identical planting on both boards: carrot board {dict(carroty)}, "
        f"wheat board {dict(wheaty)}")


def test_the_swap_never_changes_how_many_tiles_are_planted():
    """The schedule's COUNT is kept exactly -- only the crop floats. This is what caps the total.

    The herd's equivalent guard is `state["bought"]`; the same failure is available here. A target
    recomputed from scratch each turn, against a `planted` counter that only ever grows, buys up to
    BOTH ceilings as the choice flips -- measured at COW 20 + SHEEP 18 against a schedule asking 21.
    """
    for crop, qty in (("STRAWBERRY", SCHEDULE_STRAWBERRY_TILES), ("WHEAT", 24)):
        sched = sched_for(crop, qty)
        for shops in (STRAWBERRY_BOARD, TOMATO_BOARD, CARROT_BOARD, WHEAT_BOARD):
            got = pin_crops(sched, SA.CROP_ADAPT_FROM_DAY, shops)
            assert sum(got.values()) == qty, f"{crop} on {shops[0]}: {dict(got)} != {qty} tiles"


def test_the_count_holds_once_the_swap_has_already_spent_ground():
    """The total must survive a NON-ZERO anchor, which is the only case that can overshoot.

    Every other test here builds a fresh state, so `planted + live` is zero and the pair's remainder
    is trivially the schedule's own row. The real agent is never in that position after day 6: the
    strawberry row has been going into tomato ground for a day or more, so TOMATO stands at `want 0,
    anchor 8` while STRAWBERRY stands at `want 20, anchor 3`.

    Clamping each crop's remainder at zero drops tomato's -8 and hands the pair strawberry's full 17
    on top of the 8 already spent -- 28 tiles against a schedule asking for 20. Measured on the
    d0-d16 grid as 38 strawberry AND 22 tomato where the schedule asks for 41 tiles altogether.

    This is the herd's `state["bought"]` overshoot exactly (COW 20 + SHEEP 18 against a target of
    21), and it is invisible to any test that starts from an empty field.
    """
    want = collections.Counter({"STRAWBERRY": 20})
    planted = collections.Counter({"TOMATO": 8, "STRAWBERRY": 3})
    got = SA._adapt_crops(want, planted, collections.Counter(), SA.CROP_ADAPT_FROM_DAY,
                          TOMATO_BOARD, 29)
    total = got["TOMATO"] + got["STRAWBERRY"]
    assert total == 20, f"pair inflated to {total} tiles against a row of 20: {dict(got)}"
    assert got["TOMATO"] >= 8 and got["STRAWBERRY"] >= 3, (
        f"ground already planted was un-committed: {dict(got)} against anchor {dict(planted)}")


def test_melon_is_never_swapped_for_anything():
    """No shop carries melon on any board, so no draw can inform it. It must pass through untouched."""
    sched = sched_for("MELON", 12)
    for shops in (STRAWBERRY_BOARD, TOMATO_BOARD, CARROT_BOARD, WHEAT_BOARD):
        got = pin_crops(sched, SA.CROP_ADAPT_FROM_DAY, shops)
        assert got == collections.Counter({"MELON": 12}), f"melon was reallocated: {dict(got)}"


def test_the_opening_keeps_the_schedules_own_crops():
    """Before `CROP_ADAPT_FROM_DAY` the reference mix stands, exactly as the herd's floor does.

    Only 20% of the season's shop-weighted demand is on the board at day 3 and 39% at day 6, and an
    early planting is the one with the longest run left to pay for itself.
    """
    sched = sched_for("STRAWBERRY", 20)
    for shops in (STRAWBERRY_BOARD, TOMATO_BOARD):
        got = pin_crops(sched, SA.CROP_ADAPT_FROM_DAY - 1, shops)
        assert got == collections.Counter({"STRAWBERRY": 20}), (
            f"day {SA.CROP_ADAPT_FROM_DAY - 1} already floated the mix: {dict(got)}")
