"""A stop's dawn op-list must contain the work that stop's own earlier ops will create.

`_live_ops` re-derives the work at a tile from the LIVE board every turn, calling the same
`router.crop_ops` the dawn plan called. That is the whole point of committing to a visit order
rather than a script. But the dawn call reads the board as it is at hour 0, and by the time the unit
is standing there its own first op has already changed that board -- so `_live_ops` finds work the
plan never paid a turn for, and the turns come out of the END of the tour.

Measured on seed 11, day 16, tape victor, with every job seated and nothing uncovered:

    u9   priced 22 of 23   h13 (6,1) FERTILIZE   h14 (6,1) WATER   <- unpriced
                           h16 (6,0) FERTILIZE   h17 (6,0) WATER   <- unpriced
                           h19 (7,0) WATER  h20 HARVEST  h21 PLANT
                           h22 (7,0) WATER                         <- unpriced
                           h23 walks EAST, out of hours
                           (8,0) WATER is the next stop and is NEVER REACHED

    u13  priced 23 of 23   same shape at (7,2), (8,2) and (9,4)
                           (9,2) FERTILIZE and (9,0) WATER NEVER REACHED

`(8,0)` and `(9,0)` end day 16 as WEED. They die of thirst because the plan spent their water
elsewhere without counting it. This is not a coverage failure -- `cover` seats 61/61 -- and it is
not a search failure. Both the shipped greedy and `scripts/solve_day.py` price a tour by its job's
op list, so an op list that is short by one turn makes every routing result optimistic, including
the offline solver's "47/47" on day 12.

Two sites, one shape:

1. **FERTILIZE then WATER on an ongoing crop.** The ongoing branch of `crop_ops` tests `fertilized`
   in the WATER clause and only appends the FERTILIZE afterwards, so at dawn the tile is "not
   fertilized" and the water it unlocks is skipped. The one-shot branch four lines above gets this
   right: it appends FERTILIZE and sets `fertilized = True` *before* pricing the water.

2. **PLANT then WATER on a cleared tile.** `PLANT_THEN_WATER` prices the chained seed with a
   synthetic cell carrying `consecutive_unwatered: 0`. The environment starts a fresh plant at
   `1` -- `kaggriculture.py:209`, "planting day counts as unwatered" -- and `yield_units` at 1 for a
   one-shot (`:210`). At 0 the survival-water clause cannot fire, so the water is free at dawn and
   costs a turn at the stop.
"""
import pytest

from kagg.search import router as RT

DAY = 16


def _ongoing_tile_about_to_be_fertilised():
    """A strawberry that produces tomorrow, is safe tonight, and is worth fertilising today.

    `first` 10 and `interval` 2, so `age + 1 == 10` is a production day. `consecutive_unwatered` 0
    keeps the survival-water clause out of it, which is what leaves the fertilizer-enabled water as
    the only water on offer -- and therefore the only thing this test can be measuring.
    """
    return {"kind": "PLANT", "crop": "STRAWBERRY", "planted_day": DAY - 9,
            "watered_today": False, "consecutive_unwatered": 0, "yield_units": 0,
            "fertilized_until_day": -1}


def test_a_tile_the_plan_will_fertilise_is_priced_for_the_water_that_unlocks():
    cell = _ongoing_tile_about_to_be_fertilised()
    dawn = [op for op, _item, _prize in RT.crop_ops(cell, DAY, True)]

    after = dict(cell, fertilized_until_day=DAY)
    live = [op for op, _item, _prize in RT.crop_ops(after, DAY, True)]
    assert live == ["WATER"], (
        "PREMISE: once the FERTILIZE has run, `_live_ops` must find a WATER here, otherwise this "
        f"test is not measuring the overrun. Got {live}."
    )

    assert dawn == ["FERTILIZE", "WATER"], (
        "The dawn plan prices this stop at %d turn(s) and the crew will spend %d: it fertilises, "
        "re-reads the cell, and finds the water the fertilizer just made worth doing. The turn "
        "comes out of the tail of the tour. Got %r." % (len(dawn), len(dawn) + len(live), dawn)
    )


def test_a_seed_chained_onto_a_harvest_is_priced_for_its_planting_day_water():
    """The synthetic cell `PLANT_THEN_WATER` prices must match the one the environment creates."""
    assert RT.PLANT_THEN_WATER, "this test only means anything while the chain is on"

    fresh = {"kind": "PLANT", "crop": "WHEAT", "planted_day": DAY, "watered_today": False,
             "consecutive_unwatered": 1, "yield_units": 1, "fertilized_until_day": -1}
    real = [op for op, _item, _prize in RT.crop_ops(fresh, DAY, True)]
    assert real == ["WATER"], (
        "PREMISE: `kaggriculture.py:209` starts a fresh plant at `consecutive_unwatered` 1, so the "
        f"survival water is due on the planting day itself. Got {real}."
    )

    tiles = [[None] * 10 for _ in range(10)]
    tiles[0][0] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": DAY - 4, "watered_today": True,
                   "consecutive_unwatered": 0, "yield_units": 6, "fertilized_until_day": -1}
    nodes = RT.build_nodes(tiles, DAY, {"WHEAT": 9, "FERTILIZER": 9}, {}, {"NW"}, {},
                           replant={"WHEAT": 1})
    node = next((n for n in nodes if tuple(n.tile) == (0, 0)), None)
    assert node is not None, "the ripe wheat at (0,0) must be a routing node at all"
    ops = [o[0] for o in node.ops]
    assert ops.count("PLANT") == 1, (
        f"PREMISE: `REPLANT_A_CLEARED_TILE` must chain a seed onto this harvest. Got {ops}."
    )

    assert ops[-1] == "WATER", (
        "The chained seed is priced without the water its own planting day owes it, so the stop is "
        "one turn cheaper in the plan than in the day. Got %r." % (ops,)
    )
