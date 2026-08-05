"""A one-shot crop's yield IS its watering. Our cadence halved it for three of the five crops.

`reference/kaggriculture.py:373-386` -- WATER on a NON-ongoing crop, inside the age window
`[(max_yield_day + 1) // 2, max_yield_day]`, adds 1 to `yield_units` directly, or 2 if the tile is
fertilized, capped at `max_yield`. Outside that window it does nothing but reset the dry-day counter.

`reference/kaggriculture.py:756-757` -- `_daily_refresh_plants` does `if not cd["ongoing"]: continue`.
So a one-shot crop gets **no yield at all** from the nightly refresh. Every unit it ever produces came
from a WATER op inside the window.

Ongoing crops are the opposite: the refresh grows them on a fixed interval whether or not anyone
watered, and watering only prevents the two-dry-day death and gates the fertilizer doubling.

`dayplan._tasks_for_day` applied one rule to both -- water when `day - last_water >= 2` -- which is
right for ongoing crops and throttles one-shot crops to half rate inside a window that is only three
days wide for wheat. The same split was already measured in `kagg/search/routines.py:708-771` and
never wired into the day planner:

    melon (one-shot)      daily $15,575   every-other-day $11,167   -28%
    strawberry (ongoing)  daily  $6,182   every-other-day  $9,395   +52%

These tests pin the rule, not the cadence, so they stay true if the cadence is retuned later.
"""

import sys

import pytest

sys.path.insert(0, "scripts")

from kagg.search import routines as R


def window(crop):
    """The days after planting on which a WATER actually adds yield."""
    info = R.CROP_TABLE[crop]
    if info["ongoing"]:
        return []
    return list(range((info["max_day"] + 1) // 2, info["max_day"] + 1))


def test_the_one_shot_window_is_narrow_enough_that_every_day_counts():
    """Wheat's is three days wide. Watering every other day forfeits a third of it before any
    other consideration, and that is the cheapest yield in the game to leave on the floor."""
    assert window("WHEAT") == [2, 3, 4]
    assert window("MELON") == [6, 7, 8, 9, 10, 11, 12]
    assert window("CARROT") == [2, 3]
    assert window("STRAWBERRY") == [], "ongoing crops take no yield from watering"
    assert window("TOMATO") == []


@pytest.mark.parametrize("crop", ["WHEAT", "CARROT", "MELON"])
def test_a_one_shot_crop_is_watered_on_every_day_of_its_window(crop):
    """The contract. Miss a day inside the window and that unit is gone -- there is no catch-up,
    because the nightly refresh skips one-shot crops entirely."""
    from kagg.search import dayplan

    farm = dayplan.Farm()
    tile = (1, 1)
    days = window(crop)
    watered = []
    for day in range(0, max(days) + 2):
        if day == 0:
            farm.crops[tile] = dict(crop=crop, planted=0, last_water=0,
                                    last_harvest=0, fert_until=-1)
            continue
        tasks = dayplan._tasks_for_day(farm, day, [], [], fertilize=False)
        this = next((t for t in tasks if t["tile"] == tile), None)
        if this and "WATER" in this["ops"]:
            watered.append(day)
            farm.crops[tile]["last_water"] = day
        if this and "HARVEST" in this["ops"]:
            farm.crops[tile]["last_harvest"] = day

    missed = [d for d in days if d not in watered]
    assert not missed, (
        f"{crop}: window is {days}, we water on {watered}, missing {missed} -- "
        f"{len(missed)} of {len(days)} yield units forfeited on every tile of this crop")


def test_an_ongoing_crop_is_not_watered_every_day():
    """The other half of the rule, so a fix for the one above cannot quietly become 'water everything
    daily'. Strawberry measured +52% on the alternate-day cadence precisely because its yield comes
    from the nightly refresh and the spare turns are worth more elsewhere."""
    from kagg.search import dayplan

    farm = dayplan.Farm()
    tile = (2, 2)
    farm.crops[tile] = dict(crop="STRAWBERRY", planted=0, last_water=0,
                            last_harvest=0, fert_until=-1)
    watered = 0
    for day in range(1, 15):
        tasks = dayplan._tasks_for_day(farm, day, [], [], fertilize=False)
        this = next((t for t in tasks if t["tile"] == tile), None)
        if this and "WATER" in this["ops"]:
            watered += 1
            farm.crops[tile]["last_water"] = day
    assert watered <= 8, f"strawberry watered {watered} times in 14 days; every other day is the rule"
