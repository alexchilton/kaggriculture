"""The alternate-day rule synchronises the field, and the spike is what kills tiles.

`crop_ops` offers a survival water only at `consecutive_unwatered >= 1` -- a tile watered yesterday
is safe tonight, so watering it buys nothing. That is right, it is what Seb does, and it takes zero
weeds through day 7.

It stops being right once the field outgrows the crew, because it makes every tile come due on the
SAME day. Measured on seed 11 against tape `91422988`, tiles at `consecutive_unwatered >= 1` at
dawn against how many got water before dusk:

     day plants on brink rescued MISSED=dead     idle turns
       9     37       19      18           1            99
      12     52       15      13           2           136
      15     52       34      28           6             2
      17     42       24      22           2             -

    total left to die over d0-d20: 13   (16 over the full season: 14 strawberry, 2 melon)

Two distinct failures, one cause. **d15 is saturation** -- 34 due at once, two idle turns in the
whole day, six unreachable by any assignment. **d12 is the opposite** -- fifteen due, 136 idle
turns, and two die anyway. The off-day has turns going spare while the on-day cannot cover its
backlog, and both are the same synchronisation.

**The rule works and SHIPS OFF, and the reason is the interesting part.**

It was built on the argument that the earlier `>= 0` widening had been rejected for reasons that had
expired -- that rejection was justified by a waters-per-tile table taken from the OLD LEADER's tape
(which waters daily, unlike Seb), and was measured over d0-d7 where 17 tiles fit inside one day with
room to spare. Both of those observations are true. The conclusion drawn from them was not.

Measured, seed 11, tape 91422988, final bank:

    baseline                     $79,905    16 tiles starved,  1 animal escaped
    with the top-up              $63,645     5 tiles starved,  2 animals escaped
    crew planner d0-d3 alone     $91,943    18 tiles starved,  0 animals escaped
    crew planner + top-up        $62,284    11 tiles starved,  0 animals escaped

It does exactly what it was built to do -- brink misses over d0-d20 fall 13 -> 4, and the board
carries zero dry tiles from d27 -- and it costs $16k-$30k a season. The tiles are worth less than
the turns needed to save them. **The trough day's idle turns are not free**, because spending them
puts the hand somewhere else when the next spike lands, and that is the thing the "expired" argument
failed to account for.

So this file pins the SHAPE of the rule, not its being live:

  - it is priced far below a survival water, so a tile that dies tonight is never outranked;
  - it starts only from the day the field can no longer be covered in one pass.

If it is ever switched back on, it should be switched on as that priced, late-season rule -- not as
the blanket widening, which has now been rejected twice on measurement.
"""
import importlib

import pytest

RT = importlib.import_module("kagg.search.router")


@pytest.fixture
def top_up(monkeypatch):
    """The rule ships OFF -- it saves tiles and loses $16k-$30k a season doing it (see the note on
    `router.TOP_UP_SAFE_TILES`). These tests pin its SHAPE, so that if it is ever switched back on
    it is switched on as the priced, late-season rule it was designed as and not as the blanket
    widening that was rejected twice."""
    monkeypatch.setattr(RT, "TOP_UP_SAFE_TILES", True)


def _tile(crop="STRAWBERRY", cu=0, watered=False, planted=0, held=0):
    return {"kind": "PLANT", "crop": crop, "consecutive_unwatered": cu,
            "watered_today": watered, "planted_day": planted, "yield_units": held,
            "fertilized_until_day": -1}


def _ops(cell, day):
    return RT.crop_ops(cell, day, have_fertilizer=False)


def _water_prize(cell, day):
    return next((p for o, _i, p in _ops(cell, day) if o == "WATER"), None)


def test_a_safe_tile_is_offered_a_top_up_once_the_field_is_too_big_for_one_pass(top_up):
    """The whole point. Red before `TOP_UP_SAFE_TILES`: a tile at `consecutive_unwatered = 0` gets
    no WATER offer at all, so on the trough day the hands have nothing to do and the spike day
    inherits the entire field."""
    safe = _tile(cu=0, planted=0)
    assert _water_prize(safe, day=RT.TOP_UP_FROM_DAY + 2) is not None, (
        "a tile watered yesterday was offered nothing on a late day. That is what leaves 136 idle "
        "turns on d12 while the d13 spike runs at 37 tiles due at once."
    )


def test_the_top_up_never_outranks_a_tile_that_dies_tonight(top_up):
    """The half that must never soften. `consecutive_unwatered >= 2` weeds the tile outright
    (`kaggriculture.py:770`), so a survival water is an asset; a top-up is a convenience."""
    day = RT.TOP_UP_FROM_DAY + 2
    dying = _water_prize(_tile(cu=1, planted=0), day)
    safe = _water_prize(_tile(cu=0, planted=0), day)
    assert dying is not None, "a tile one dry day from weeding was not offered water at all"
    assert safe is not None, "no top-up offered; see the previous test"
    assert safe < dying, (
        f"the top-up is priced at {safe} against a survival water's {dying}. Priced level or above, "
        "a spike day spends its turns on tiles that were never at risk and the ones that were die."
    )


def test_the_early_days_are_left_alone(top_up):
    """d0-d6 is matched to the tape op for op and must stay matched. Seventeen tiles fit in one day;
    the top-up there is ~31 walk turns for nothing, which is exactly what the earlier widening was
    measured to cost."""
    assert RT.TOP_UP_FROM_DAY >= 7, (
        f"TOP_UP_FROM_DAY is {RT.TOP_UP_FROM_DAY}. Below 7 it changes days whose grid is exact."
    )
    assert _water_prize(_tile(cu=0, planted=0), day=3) is None, (
        "a safe tile was offered a top-up inside the first week. Seb waters alternate days there "
        "and takes zero weeds doing it."
    )


@pytest.mark.parametrize("cu", [1, 2])
def test_a_tile_at_risk_is_still_offered_water_on_every_day(cu):
    """Guards against a refactor that folds the two branches together and loses the survival case."""
    for day in (3, 8, 15):
        assert _water_prize(_tile(cu=cu, planted=0), day) is not None, (
            f"a tile at consecutive_unwatered={cu} was offered no water on day {day}."
        )
