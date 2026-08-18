"""A SAFE ongoing tile is offered water on alternate days, not every day.

`router.crop_ops` waters an ongoing crop down three branches. The first two are mandatory -- the
tile is on the brink (`consecutive_unwatered >= 1`), or it produces tomorrow and is fertilized. The
third is a top-up, and its comment says:

    **The same parity alternation the one-shot branch above already ships.**
    ... Parity offers HALF and flips daily, so no tile is skipped twice running.

The condition underneath it does not contain the parity term. The one-shot branch has
`(tile[0] + tile[1] + day) % 2 == 0`; this one has `tile is not None and not upkeep_buys_nothing(day)`
and nothing else, so every safe ongoing tile is offered water on every single day of its life.

Water does not grow an ongoing crop. `_daily_refresh_crops` advances `yield_units` off the calendar
alone -- `days_since_first`, `interval`, `production_count` (`reference/kaggriculture.py:786-800`).
`was_watered` is read for exactly two things: `consecutive_unwatered >= 2` weeds the tile (`:783`),
and it gates the fertilizer doubling (`:799`). So on a safe, unfertilized, non-producing tile a water
buys nothing whatsoever, and `consecutive_unwatered` starts at 1 and weeds at 2, which is the
every-SECOND-day rule the comment is describing.

Measured 2026-08-18, strawberry arm, own seed 70683142, every WATER classified by the tile's dawn
state -- 39 strawberry standing, all age 1-8 against a `first` of 10, so none can produce:

    d12   55 waters emitted, his 32     17 land on a SAFE tile on its OFF-parity day
    d13   61 waters emitted, his 43     21 land on a SAFE tile on its OFF-parity day

Each is a work turn plus the walk to reach it, for nothing.
"""
import pytest

from kagg.search import router as RT


def _safe_strawberry(planted_day=11):
    """An ongoing tile watered yesterday: not on the brink, far from its first yield."""
    return {"kind": "PLANT", "crop": "STRAWBERRY", "planted_day": planted_day,
            "yield_units": 0, "watered_today": False, "consecutive_unwatered": 0,
            "fertilized_until_day": -1}


def _waters(cell, day, tile):
    return [o for o in RT.crop_ops(cell, day, have_fertilizer=False, tile=tile) if o[0] == "WATER"]


def test_the_safe_tile_is_offered_water_on_its_parity_day():
    """(x + y + day) even -- the tile's turn. It must be offered."""
    tile = (3, 8)                                   # 3 + 8 + 13 == 24, even
    assert _waters(_safe_strawberry(), 13, tile), "a safe ongoing tile is never offered water at all"


def test_the_safe_tile_is_skipped_on_its_off_parity_day():
    """(x + y + day) odd -- tomorrow's turn. Watering it today buys nothing."""
    tile = (3, 8)                                   # 3 + 8 + 12 == 23, odd
    got = _waters(_safe_strawberry(), 12, tile)
    assert got == [], (
        f"a safe ongoing strawberry is offered {got} on its off-parity day; water does not grow an "
        "ongoing crop and the tile cannot weed tonight, so this turn buys nothing")


def test_a_tile_on_the_brink_is_still_watered_on_either_parity():
    """The alternation must never reach the second dry night. This is the branch above it."""
    for day in (12, 13):
        cell = _safe_strawberry()
        cell["consecutive_unwatered"] = 1
        assert _waters(cell, day, (3, 8)), f"d{day}: a tile one night from weeding was not watered"
