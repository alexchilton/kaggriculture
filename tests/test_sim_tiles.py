"""Parity tests for the batched tile transitions.

These drive **randomly generated farm states** through the batched implementation and through
`kaggriculture`'s own functions, then compare field by field. Random states rather than
hand-written ones because the interesting bugs are in combinations nobody thinks to write down --
a plant that both matures and starts decaying on the same day, a fertilized tile that was not
watered, an ongoing crop one event past its cap.

`CLAUDE.md` makes parity a hard gate: do not train on this sim until it matches exactly.
"""

import numpy as np
import pytest

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.sim.tiles import (
    CROP_INDEX,
    CROPS,
    EMPTY,
    NO_CROP,
    PLANT,
    TILES,
    TURNS_PER_DAY,
    WEED,
    TileState,
    daily_refresh_plants,
    decay_plants,
)


def _random_states(rng, batch, day):
    """Build matching batched and reference-dict tile states.

    Returns (TileState, list of per-game lists of reference tile dicts).
    """
    state = TileState(batch)
    reference = []

    for b in range(batch):
        row = []
        for t in range(TILES):
            roll = rng.random()
            if roll < 0.15:
                row.append(None)
                continue
            if roll < 0.25:
                state.kind[b, t] = WEED
                row.append({"kind": "WEED"})
                continue

            crop = CROPS[rng.integers(len(CROPS))]
            cd = kg.CROPS[crop]
            planted = int(rng.integers(0, max(1, day + 1)))
            watered = bool(rng.random() < 0.6)
            unwatered = int(rng.integers(0, 3))
            units = int(rng.integers(0, cd["max_yield"] + 1))
            # Mix of "no clock yet" and clocks either side of the current step.
            if rng.random() < 0.4:
                mls = -1
            else:
                mls = int(rng.integers(0, (day + 3) * TURNS_PER_DAY))
            fert = -1 if rng.random() < 0.6 else int(rng.integers(0, day + 2))

            tile = {
                "kind": "PLANT",
                "crop": crop,
                "planted_day": planted,
                "watered_today": watered,
                "consecutive_unwatered": unwatered,
                "yield_units": units,
                "max_lifespan_step": mls,
                "fertilized_until_day": fert,
            }
            row.append(tile)

            state.kind[b, t] = PLANT
            state.crop[b, t] = CROP_INDEX[crop]
            state.planted_day[b, t] = planted
            state.watered_today[b, t] = watered
            state.consecutive_unwatered[b, t] = unwatered
            state.yield_units[b, t] = units
            state.max_lifespan_step[b, t] = mls
            state.fertilized_until_day[b, t] = fert
        reference.append(row)

    return state, reference


def _as_farm(row):
    """Wrap a flat list of tiles as the nested board the reference functions expect."""
    return {"tiles": [row[i * 10:(i + 1) * 10] for i in range(10)]}


def _compare(state, reference, label):
    """Assert every tile in every game agrees, field by field."""
    for b, row in enumerate(reference):
        flat = [cell for r in _as_farm(row)["tiles"] for cell in r]
        for t, tile in enumerate(flat):
            kind = state.kind[b, t]
            if tile is None:
                assert kind == EMPTY, f"{label}: game {b} tile {t} should be empty"
                continue
            if tile.get("kind") == "WEED":
                assert kind == WEED, f"{label}: game {b} tile {t} should be a weed, got {kind}"
                continue
            assert kind == PLANT, f"{label}: game {b} tile {t} should be a plant, got {kind}"
            assert state.crop[b, t] == CROP_INDEX[tile["crop"]], f"{label}: crop, game {b} tile {t}"
            for field in ("yield_units", "max_lifespan_step", "consecutive_unwatered"):
                assert state.__getattribute__(field)[b, t] == tile[field], (
                    f"{label}: {field} mismatch, game {b} tile {t}: "
                    f"{state.__getattribute__(field)[b, t]} != {tile[field]}"
                )
            assert bool(state.watered_today[b, t]) == bool(tile["watered_today"]), (
                f"{label}: watered_today, game {b} tile {t}"
            )


@pytest.mark.parametrize("step", [0, 1, 47, 48, 49, 240, 719])
def test_decay_matches_the_reference_on_random_states(step):
    """The alternate-step decay parity is easy to get wrong, so it is swept across steps."""
    rng = np.random.default_rng(step)
    state, reference = _random_states(rng, batch=6, day=step // TURNS_PER_DAY)

    decay_plants(state, step)
    for row in reference:
        farm = _as_farm(row)
        kg._decay_plants(farm, step)
        row[:] = [cell for r in farm["tiles"] for cell in r]

    _compare(state, reference, f"decay at step {step}")


@pytest.mark.parametrize("day", [0, 1, 5, 11, 16, 23, 29])
def test_daily_refresh_matches_the_reference_on_random_states(day):
    """Watering enforcement, ongoing production, the event cap, and the lifespan clock."""
    rng = np.random.default_rng(1000 + day)
    state, reference = _random_states(rng, batch=6, day=day)

    daily_refresh_plants(state, day)
    for row in reference:
        farm = _as_farm(row)
        kg._daily_refresh_plants(farm, day, TURNS_PER_DAY)
        row[:] = [cell for r in farm["tiles"] for cell in r]

    _compare(state, reference, f"daily refresh on day {day}")


def test_a_full_season_of_alternating_transitions_stays_in_parity():
    """The real test: 30 simulated days of refresh and decay, never resynchronised.

    Any divergence compounds, so surviving a whole season is far stronger evidence than surviving
    one transition.

    The loop **waters most tiles and replants weeds each day**, which matters: an earlier version
    of this test did neither, so every plant died of thirst by day 5 and the remaining 25 days
    compared two identical boards of weeds. It passed while proving almost nothing. Watering keeps
    plants alive long enough to reach maturity, start their lifespan clock, and decay -- which is
    the part worth testing.
    """
    rng = np.random.default_rng(99)
    state, reference = _random_states(rng, batch=4, day=0)

    for day in range(30):
        # Water ~85% of living plants, and replant a few weeds, so the board keeps turning over.
        water = (state.kind == PLANT) & (rng.random(state.kind.shape) < 0.85)
        state.watered_today = np.where(water, True, state.watered_today)
        replant = (state.kind == WEED) & (rng.random(state.kind.shape) < 0.15)
        crop_id = int(rng.integers(len(CROPS)))
        for b, row in enumerate(reference):
            for t, tile in enumerate(row):
                if water[b, t] and isinstance(tile, dict):
                    tile["watered_today"] = True
                if replant[b, t]:
                    row[t] = kg._new_plant(CROPS[crop_id], day, TURNS_PER_DAY)
        state.plant(replant, crop_id, day)

        for hour in (0, 7, 15, 23):
            step = day * TURNS_PER_DAY + hour
            decay_plants(state, step)
            for row in reference:
                farm = _as_farm(row)
                kg._decay_plants(farm, step)
                row[:] = [cell for r in farm["tiles"] for cell in r]

        daily_refresh_plants(state, day)
        for row in reference:
            farm = _as_farm(row)
            kg._daily_refresh_plants(farm, day, TURNS_PER_DAY)
            row[:] = [cell for r in farm["tiles"] for cell in r]

        _compare(state, reference, f"season, after day {day}")

    # Guard against the vacuity that made the earlier version of this test meaningless.
    assert (state.kind == PLANT).sum() > 20, "season ended with no living plants to compare"


def test_planting_matches_new_plant():
    """`plant` must reproduce `_new_plant`, including the planting-day-counts-as-unwatered rule."""
    for crop in CROPS:
        state = TileState(1)
        mask = np.zeros((1, TILES), dtype=bool)
        mask[0, 3] = True
        state.plant(mask, CROP_INDEX[crop], day=5)

        expected = kg._new_plant(crop, 5, TURNS_PER_DAY)

        assert state.kind[0, 3] == PLANT
        assert state.crop[0, 3] == CROP_INDEX[crop]
        assert state.planted_day[0, 3] == expected["planted_day"]
        assert state.yield_units[0, 3] == expected["yield_units"]
        assert state.consecutive_unwatered[0, 3] == expected["consecutive_unwatered"]
        assert state.max_lifespan_step[0, 3] == expected["max_lifespan_step"]
        # Untouched tiles stay untouched.
        assert state.kind[0, 4] == EMPTY and state.crop[0, 4] == NO_CROP
