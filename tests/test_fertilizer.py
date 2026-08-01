"""What FERTILIZE actually does, measured rather than read off the tables.

The published Object Types table is known to mislead -- CLAUDE.md pins two cases where it cost a
day -- and the yield rules for the two crop families live in different functions with different
semantics, which is easy to read wrong:

- **ongoing** crops (TOMATO, STRAWBERRY) accrue in `_daily_refresh_plants`, once per interval;
- **non-ongoing** crops (WHEAT, CARROT, MELON) accrue *inside the WATER action itself*, only while
  `(max_yield_day + 1) // 2 <= age <= max_yield_day`.

Fertilizer is `bonus = 2 if fertilized else 1` in both. It therefore does **not** raise the ceiling
for a non-ongoing crop -- `max_yield` caps it either way -- it reduces the number of watered days
needed to reach that ceiling. That distinction decides whether it is worth an action, so it is
measured here directly against the environment.
"""

import pytest
from kaggle_environments.envs.kaggriculture import kaggriculture as kg


def _plant(crop, day=0):
    farm = {"tiles": [[None] * 10 for _ in range(10)], "farmer": [0, 0], "hands": [],
            "money": 3000.0}
    private = {"shed": {}, "seeds": {crop: 1}, "inventories": [{}]}
    kg._apply_unit_action(farm, private, 0, ["PLANT", crop], 10, day, 24)
    return farm, private


def _water_days(crop, days, fertilise_on=None):
    """Plant on day 0, water on each day in `days`, optionally fertilising first. Returns yield."""
    farm, private = _plant(crop)
    for day in days:
        if fertilise_on is not None and day == fertilise_on:
            private["inventories"][0]["FERTILIZER"] = 1
            kg._apply_unit_action(farm, private, 0, ["FERTILIZE"], 10, day, 24)
        kg._apply_unit_action(farm, private, 0, ["WATER"], 10, day, 24)
        farm["tiles"][0][0]["watered_today"] = False      # next day
    return farm["tiles"][0][0]["yield_units"]


def test_melon_accrues_yield_on_watering_not_on_the_daily_tick():
    """A melon watered outside its window gains nothing, however often it is watered."""
    early = _water_days("MELON", [0, 1, 2, 3, 4, 5])       # window opens at age 6
    assert early == 1, f"melon gained yield before its window: {early}"


def test_the_melon_window_is_age_six_to_twelve():
    window_start = (kg.CROPS["MELON"]["max_yield_day"] + 1) // 2
    assert window_start == 6
    assert kg.CROPS["MELON"]["max_yield_day"] == 12

    inside = _water_days("MELON", [6, 7, 8])
    assert inside == 4, f"three watered days in-window should give 1+3: {inside}"


def test_fertiliser_does_not_raise_the_ceiling_for_melon():
    """`max_yield` caps both. Fertiliser buys speed, not total yield -- the claim worth pinning."""
    cap = kg.CROPS["MELON"]["max_yield"]
    plain = _water_days("MELON", list(range(6, 13)))
    fert = _water_days("MELON", list(range(6, 13)), fertilise_on=6)

    assert plain == cap
    assert fert == cap, "fertiliser must not exceed max_yield"


def test_fertiliser_reaches_the_cap_in_fewer_watered_days():
    """The actual benefit, and the reason it is worth an action under a tight action budget.

    Converter's census shows up to 13 melon tiles dry on the same day, so tiles that miss enough of
    the seven-day window never reach the cap at all. Fertiliser is active for `day..day+2`.
    """
    plain = _water_days("MELON", [6, 7, 8])
    fert = _water_days("MELON", [6, 7, 8], fertilise_on=6)

    assert fert > plain, f"fertiliser bought nothing over three days: {fert} vs {plain}"
    assert fert == kg.CROPS["MELON"]["max_yield"], (
        f"three fertilised waterings should hit the cap: {fert}")


@pytest.mark.parametrize("crop", ["TOMATO", "STRAWBERRY"])
def test_ongoing_crops_take_their_yield_from_the_daily_tick_instead(crop):
    """Watering an ongoing crop grants nothing directly; the daily refresh does the work."""
    farm, private = _plant(crop)
    kg._apply_unit_action(farm, private, 0, ["WATER"], 10, 0, 24)

    assert farm["tiles"][0][0]["yield_units"] == 0
