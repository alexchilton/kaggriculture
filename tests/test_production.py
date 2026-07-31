"""Tests for the per-tile production model.

The published Object Types table reads as though tomato yields 4 units per tile per *day*.
It does not: an ongoing crop yields 4 units for its entire life.
Believing the table overstates premium output by more than tenfold and inverts the whole
strategic conclusion, so the real figures are pinned here against the live environment.
"""

import pytest

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.economics.production import (
    ANIMAL_YIELD_PER_SEASON,
    SEASON_DAYS,
    TILE_YIELD_FERTILIZED,
    TILE_YIELD_PER_SEASON,
    cycle_days,
    probe_animal,
    probe_crop,
    seed_cost_per_tile_season,
    units_per_cycle,
)


@pytest.mark.parametrize("crop,expected", sorted(TILE_YIELD_PER_SEASON.items()))
def test_measured_tile_yield_matches_the_recorded_constant(crop, expected):
    """Re-measures in the live env, so the constants cannot silently rot."""
    total = probe_crop(crop).units

    assert total == expected


@pytest.mark.parametrize("product,expected", sorted(ANIMAL_YIELD_PER_SEASON.items()))
def test_measured_animal_yield_matches_the_recorded_constant(product, expected):
    total = probe_animal(product).units

    assert total == expected


def first_cycle(result, crop):
    """Harvests belonging to the first planting.

    The boundary is inclusive for non-ongoing crops, because harvest clears the tile and the
    replant happens on the same day; exclusive for ongoing crops, which are only replaced once
    the plant has died.
    """
    if len(result.plantings) < 2:
        return result.harvests
    boundary = result.plantings[1]
    if kg.CROPS[crop]["ongoing"]:
        return [(d, u) for d, u in result.harvests if d < boundary]
    return [(d, u) for d, u in result.harvests if d <= boundary]


def first_cycle_units(result, crop):
    return sum(units for _, units in first_cycle(result, crop))


@pytest.mark.parametrize("crop", ["TOMATO", "STRAWBERRY"])
def test_ongoing_crops_cap_production_events_not_units_per_day(crop):
    """The single most consequential rule in the production model.

    `_daily_refresh_plants` stops once `production_count > max_yield`, so the cap is on
    production *events*. Unfertilized that is `max_yield` units for the plant's whole life --
    not `max_yield` a day as the Object Types table reads.
    """
    max_yield = kg.CROPS[crop]["max_yield"]
    per_day_reading = max_yield * SEASON_DAYS  # what the table appears to promise

    assert first_cycle_units(probe_crop(crop), crop) == max_yield
    # Only a couple of lifetimes fit in a season, so the season total stays a small
    # multiple of max_yield rather than anything close to a daily rate.
    assert TILE_YIELD_PER_SEASON[crop] <= 3 * max_yield
    assert TILE_YIELD_PER_SEASON[crop] < 0.2 * per_day_reading


@pytest.mark.parametrize("crop", ["TOMATO", "STRAWBERRY"])
def test_fertilizer_doubles_ongoing_crop_lifetime_output(crop):
    """Because the cap counts events, and a fertilized event grants 2 units instead of 1.

    Found by adversarial review of the first version of this model, which treated fertilizer
    as a minor omission. It is worth 2x on exactly the two crops the premium argument leans on,
    and animals supply it free via COLLECT_FERTILIZER.
    """
    plain = first_cycle_units(probe_crop(crop), crop)
    fertilized = first_cycle_units(probe_crop(crop, fertilize=True), crop)

    assert fertilized == 2 * plain
    assert TILE_YIELD_FERTILIZED[crop] == 2 * TILE_YIELD_PER_SEASON[crop]


def test_fertilizer_does_not_help_melon():
    """Melon's watering window already fills `max_yield` unfertilized, so there is no headroom."""
    assert TILE_YIELD_FERTILIZED["MELON"] == TILE_YIELD_PER_SEASON["MELON"]


def test_ongoing_crops_are_an_order_of_magnitude_worse_per_tile_than_wheat():
    """Stated as a test because the economics doc claimed the opposite."""
    assert TILE_YIELD_PER_SEASON["WHEAT"] > 4 * TILE_YIELD_PER_SEASON["STRAWBERRY"]
    assert TILE_YIELD_PER_SEASON["WHEAT"] > 3 * TILE_YIELD_PER_SEASON["TOMATO"]


def test_animals_have_no_lifetime_production_cap():
    """`_daily_refresh_animals` has no `production_count` check, unlike plants.

    A goose therefore out-produces its own `max_held` many times over, which is what makes
    animals the only uncapped premium source.
    """
    total = probe_animal("EGG").units

    assert total > 4 * kg.ANIMALS["GOOSE"]["max_held"]


def test_units_per_cycle_model_agrees_with_the_measured_first_cycle():
    """The closed-form used by the planner must match what the env actually grants."""
    for crop in TILE_YIELD_PER_SEASON:
        assert first_cycle_units(probe_crop(crop), crop) == units_per_cycle(crop), crop


def test_cycle_days_model_agrees_with_the_measured_last_harvest_of_the_first_cycle():
    """`cycle_days` is when the plant is finished, not when it first pays out.

    Ongoing crops are harvested eagerly, so their first harvest lands on `first_yield_day`
    while the cycle runs until the final production event.
    """
    for crop in TILE_YIELD_PER_SEASON:
        cycle = [d for d, _ in first_cycle(probe_crop(crop), crop)]

        assert max(cycle) == cycle_days(crop), crop
        if kg.CROPS[crop]["ongoing"]:
            assert min(cycle) == kg.CROPS[crop]["first_yield_day"], crop


def test_seed_cost_uses_measured_plantings_not_a_season_division():
    """Regression test for a wrong closed form found by review.

    `SEASON_DAYS // cycle_days` predicted 1 strawberry seed and 2 tomato seeds. The probe
    actually buys 2 and 3, because a final cycle that cannot ripen before day 29 is still
    planted and still paid for.
    """
    assert seed_cost_per_tile_season("STRAWBERRY") == 2 * kg.CROPS["STRAWBERRY"]["seed"]
    assert seed_cost_per_tile_season("TOMATO") == 3 * kg.CROPS["TOMATO"]["seed"]

    for crop in TILE_YIELD_PER_SEASON:
        measured = len(probe_crop(crop).plantings)

        assert seed_cost_per_tile_season(crop) == measured * kg.CROPS[crop]["seed"], crop
