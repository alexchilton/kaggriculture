"""What a single tile actually produces over a season.

The published Object Types table lists a "max yield / tile / day" column that does not
mean what it looks like for ongoing crops.
`_daily_refresh_plants` stops an ongoing crop once `production_count > max_yield`, so the cap
is on production *events*, not on units and certainly not per day. Unfertilized, a tomato or
strawberry tile yields four units for its whole life and then dies. Fertilized, each event
grants 2 instead of 1, so the same four events yield **eight**.
Animals are the opposite: there is no lifetime cap, so they produce until they starve.

Getting this wrong by an order of magnitude changes every strategic conclusion, so the
constants here are measured in the live environment by :func:`probe_crop` and
:func:`probe_animal`, and `tests/test_production.py` re-measures them on every run.

All figures are single-tile, one farmer, no animal CARE bonus, 30-day season.
CARE is unexercised, so the animal numbers are floors too.
"""

from typing import NamedTuple

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

SEASON_DAYS = 30

# Units one tile yields over a season under optimal play, WITHOUT fertilizer.
# These are floors, not ceilings -- see TILE_YIELD_FERTILIZED.
TILE_YIELD_PER_SEASON = {
    "WHEAT": 28,
    "CARROT": 29,
    "TOMATO": 8,
    "STRAWBERRY": 6,
    "MELON": 12,
}

# With fertilizer kept active, measured the same way.
#
# Fertilizer **doubles** ongoing-crop lifetime output, which is not obvious and matters a lot.
# The lifetime cap is on production *events* (`production_count > max_yield`), while
# `yield_units` is only a *holding* cap. A fertilized event adds 2 units instead of 1, so
# harvesting between events collects 2 x max_yield over the plant's life instead of max_yield.
#
# Melon gains nothing: its watering window already fills `max_yield` unfertilized.
TILE_YIELD_FERTILIZED = {
    "WHEAT": 42,
    "CARROT": 39,
    "TOMATO": 16,
    "STRAWBERRY": 12,
    "MELON": 12,
}

# Fertilizer is free from animals: every fed animal sets `fertilizer_available` daily and
# COLLECT_FERTILIZER takes it for one action. Buying it instead costs $100 base.
# This is the wheat -> animal -> fertilizer -> premium-crop loop, and it is the main
# structural reason to keep animals.
FERTILIZER_MARKET_BASE = 100
FERTILIZER_ACTIVE_DAYS = 3  # FERTILIZE sets fertilized_until_day = day + 2, inclusive

# Units one animal yields over a season, fed every day, harvested before it fills.
# Keyed by product rather than animal, since that is what the market trades.
ANIMAL_YIELD_PER_SEASON = {
    "EGG": 26,
    "MILK": 11,
    "WOOL": 8,
}

# Seeds actually bought and planted per tile per season, measured. A final cycle that cannot
# finish before day 29 is still planted and still paid for, which `SEASON_DAYS // cycle_days`
# missed for strawberry (2 not 1) and tomato (3 not 2).
PLANTINGS_PER_SEASON = {"WHEAT": 8, "CARROT": 11, "TOMATO": 3, "STRAWBERRY": 2, "MELON": 3}
PLANTINGS_FERTILIZED = dict(PLANTINGS_PER_SEASON)  # measured identical: fertilizer changes
# units per event, not the number of cycles that fit in a season.

PRODUCT_TO_ANIMAL = {a["product"]: name for name, a in kg.ANIMALS.items()}


def cycle_days(crop):
    """Days from planting to the harvest that clears the tile."""
    cd = kg.CROPS[crop]
    if cd["ongoing"]:
        # Productions land every `interval` days from `first_yield_day`, `max_yield` times.
        return cd["first_yield_day"] + cd["interval"] * (cd["max_yield"] - 1)
    return cd["max_yield_day"]


def first_harvest_day(crop):
    """Earliest day a full-value harvest is available from a day-0 planting."""
    return cycle_days(crop)


def units_per_cycle(crop):
    """Units a single planting yields, played optimally and without fertilizer."""
    cd = kg.CROPS[crop]
    if cd["ongoing"]:
        return cd["max_yield"]
    # Starts at 1 unit; each watering inside the window adds 1, capped at max_yield.
    window_start = (cd["max_yield_day"] + 1) // 2
    waterings = cd["max_yield_day"] - window_start + 1
    return min(cd["max_yield"], 1 + waterings)


def seed_cost_per_tile_season(crop, fertilized=False):
    """Total seed spend to keep one tile planted all season.

    Uses the *measured* number of plantings rather than `SEASON_DAYS // cycle_days`, which
    disagreed with what the probe actually spends: a cycle that cannot finish before the season
    ends is still planted and still paid for, so strawberry costs two seeds and tomato three,
    not the one and two the division predicted.
    """
    table = PLANTINGS_FERTILIZED if fertilized else PLANTINGS_PER_SEASON
    return kg.CROPS[crop]["seed"] * table[crop]


class ProbeResult(NamedTuple):
    """What a single-tile probe measured: total units, and when things happened."""

    units: int
    harvests: list  # [(day, units), ...]
    plantings: list  # [day, ...] -- one seed bought and spent per entry


def probe_crop(crop, seed=3, days=SEASON_DAYS, fertilize=False):
    """Play one farmer on one tile optimally for `crop`; return a :class:`ProbeResult`.

    With `fertilize=True` the tile is kept under fertilizer continuously, bought from the
    market. That doubles ongoing-crop lifetime output (see `TILE_YIELD_FERTILIZED`) and for
    non-ongoing crops fills the watering window faster.

    Non-ongoing crops are held until the watering window closes, because harvesting clears
    the tile and an early harvest throws away the remaining bonus waterings.
    Ongoing crops accumulate on the tile and are taken in one go, which is both
    action-efficient and what makes late selling possible.
    """
    from kaggle_environments import make

    cd = kg.CROPS[crop]
    harvests = []
    plantings = []

    def agent(obs, cfg):
        day = obs["day"]
        farm = obs["farms"][0]
        fx, fy = farm["farmer"]
        tile = farm["tiles"][fy][fx]
        private = obs["private"]
        seeds = private["seeds"]
        shed = private["shed"]
        carried = private["inventories"][0] if private.get("inventories") else {}

        market = [["BUY_SEED", crop, 1]] if seeds.get(crop, 0) < 1 else []
        if fertilize and shed.get("FERTILIZER", 0) + carried.get("FERTILIZER", 0) < 2:
            market.append(["BUY_PRODUCT", "FERTILIZER", 2])

        act = ["PASS"]
        if tile is None:
            if seeds.get(crop, 0) >= 1:
                act = ["PLANT", crop]
                plantings.append(day)
        elif isinstance(tile, dict) and tile.get("kind") == "WEED":
            act = ["DIG"]
        elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
            age = day - tile["planted_day"]
            units = tile.get("yield_units", 0)
            # Ongoing crops are harvested eagerly: `yield_units` is a holding cap, so leaving
            # units on the tile throws away the next event's production. Non-ongoing crops are
            # held until the watering window closes, because harvest clears the tile.
            ripe = units > 0 if cd["ongoing"] else age >= cd["max_yield_day"]
            # Near the end there is no time left to fill the tile, so take what is standing.
            flush = day >= days - 1 and units > 0
            needs_fert = fertilize and tile.get("fertilized_until_day", -1) < day

            if not tile.get("watered_today"):
                act = ["WATER"]
            elif needs_fert:
                act = ["FERTILIZE"] if carried.get("FERTILIZER", 0) >= 1 else ["PICKUP", "FERTILIZER", 2]
            elif (ripe or flush) and units > 0 and age >= cd["first_yield_day"]:
                act = ["HARVEST"]
                harvests.append((day, units))
        return {"farmer": act, "hands": [], "market": market}

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run([agent, "pass"])
    return ProbeResult(sum(u for _, u in harvests), harvests, plantings)


def probe_animal(product, seed=3):
    """Place one animal, feed it daily from bought wheat, harvest whenever it holds units.

    Returns (total_units, harvests). Wheat for feed is bought from the market rather than
    grown, which keeps the measurement about the animal instead of about a wheat operation.

    The structure is built on the farmer's spawn tile, which is one of the four shed-access
    tiles, so `PICKUP` and `FEED` both work without the farmer ever moving.
    PLACE and FEED draw from the unit's carried inventory, not the shed, and that inventory
    is emptied back into the shed every night -- hence the daily PICKUP.
    """
    from kaggle_environments import make

    animal = PRODUCT_TO_ANIMAL[product]
    structure = kg.ANIMALS[animal]["structure"]
    harvests = []

    def agent(obs, cfg):
        day = obs["day"]
        farm = obs["farms"][0]
        fx, fy = farm["farmer"]
        tile = farm["tiles"][fy][fx]
        private = obs["private"]
        shed = private["shed"]
        carried = private["inventories"][0] if private.get("inventories") else {}
        placed = isinstance(tile, dict) and "animal" in tile
        market = []

        if shed.get("WHEAT", 0) + carried.get("WHEAT", 0) < 4:
            market.append(["BUY_PRODUCT", "WHEAT", 10])
        if not placed and shed.get(animal, 0) + carried.get(animal, 0) < 1:
            market.append(["BUY_ANIMAL", animal, 1])

        act = ["PASS"]
        if tile is None:
            act = ["BUILD_COOP"] if structure == "COOP" else ["BUILD_PASTURE"]
        elif isinstance(tile, dict) and tile.get("kind") == structure and not placed:
            if carried.get(animal, 0) >= 1:
                act = ["PLACE", animal]
            elif shed.get(animal, 0) >= 1:
                act = ["PICKUP", animal, 1]
        elif placed:
            if tile.get("yield_units", 0) > 0:
                act = ["HARVEST"]
                harvests.append((day, tile["yield_units"]))
            elif not tile["fed_today"]:
                act = ["FEED"] if carried.get("WHEAT", 0) >= 1 else ["PICKUP", "WHEAT", 2]
        return {"farmer": act, "hands": [], "market": market}

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run([agent, "pass"])
    return ProbeResult(sum(u for _, u in harvests), harvests, [])
