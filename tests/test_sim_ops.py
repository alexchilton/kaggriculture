"""Parity tests for batched unit operations.

Each test drives the same random board and the same op through the batched implementation and
through `kaggriculture._apply_unit_action`, then compares. The reference is the authority; where
these disagree, this code is wrong.
"""

import numpy as np
import pytest

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.sim import ops as O
from kagg.sim.tiles import (
    BOARD,
    CROP_INDEX,
    CROPS,
    EMPTY,
    LOCKED,
    PLANT,
    TILES,
    TURNS_PER_DAY,
    WEED,
    TileState,
)

OP_NAMES = {
    O.NORTH: "NORTH", O.SOUTH: "SOUTH", O.EAST: "EAST", O.WEST: "WEST",
    O.WATER: "WATER", O.HARVEST: "HARVEST", O.DIG: "DIG", O.NOOP: "PASS",
}


def _paired_board(rng, crop, day, lock_quadrant=True):
    """One game, as both a TileState and a reference farm dict."""
    state = TileState(1)
    rows = [[None] * BOARD for _ in range(BOARD)]

    for y in range(BOARD):
        for x in range(BOARD):
            t = y * BOARD + x
            if lock_quadrant and x >= BOARD // 2 and y < BOARD // 2:
                state.kind[0, t] = LOCKED
                rows[y][x] = "LOCKED"
                continue
            roll = rng.random()
            if roll < 0.3:
                continue  # empty
            if roll < 0.4:
                state.kind[0, t] = WEED
                rows[y][x] = {"kind": "WEED"}
                continue
            planted = int(rng.integers(0, max(1, day + 1)))
            units = int(rng.integers(0, kg.CROPS[crop]["max_yield"] + 1))
            watered = bool(rng.random() < 0.4)
            fert = -1 if rng.random() < 0.7 else day
            rows[y][x] = {
                "kind": "PLANT", "crop": crop, "planted_day": planted,
                "watered_today": watered, "consecutive_unwatered": 0,
                "yield_units": units, "max_lifespan_step": -1,
                "fertilized_until_day": fert,
            }
            state.kind[0, t] = PLANT
            state.crop[0, t] = CROP_INDEX[crop]
            state.planted_day[0, t] = planted
            state.yield_units[0, t] = units
            state.watered_today[0, t] = watered
            state.fertilized_until_day[0, t] = fert
    return state, {"tiles": rows, "farmer": [0, 0], "hands": []}


def _flat(farm):
    return [c for row in farm["tiles"] for c in row]


def _assert_tiles_match(state, farm, label):
    for t, cell in enumerate(_flat(farm)):
        k = state.kind[0, t]
        if cell is None:
            assert k == EMPTY, f"{label}: tile {t} expected empty, got {k}"
        elif cell == "LOCKED":
            assert k == LOCKED, f"{label}: tile {t} expected locked"
        elif cell.get("kind") == "WEED":
            assert k == WEED, f"{label}: tile {t} expected weed, got {k}"
        else:
            assert k == PLANT, f"{label}: tile {t} expected plant, got {k}"
            assert state.yield_units[0, t] == cell["yield_units"], f"{label}: units at {t}"
            assert bool(state.watered_today[0, t]) == bool(cell["watered_today"]), f"{label}: watered at {t}"


@pytest.mark.parametrize("op", [O.NORTH, O.SOUTH, O.EAST, O.WEST])
@pytest.mark.parametrize("start", [(0, 0), (4, 4), (9, 9), (5, 0), (0, 5)])
def test_movement_matches_the_reference_including_blocked_moves(op, start):
    """Edges and LOCKED tiles both block, and a blocked move still costs the turn."""
    rng = np.random.default_rng(7)
    state, farm = _paired_board(rng, "WHEAT", day=3)
    farm["farmer"] = list(start)

    pos = O.move(state, np.array([start], dtype=np.int64), np.array([op]))
    kg._apply_unit_action(farm, kg._new_private(), 0, [OP_NAMES[op]], BOARD, 3, TURNS_PER_DAY, 100)

    assert list(pos[0]) == list(farm["farmer"]), f"{OP_NAMES[op]} from {start}"


@pytest.mark.parametrize("crop", CROPS)
@pytest.mark.parametrize("day", [0, 2, 3, 5, 10, 12])
def test_water_matches_the_reference_including_the_bonus_window(crop, day):
    """The window is `(max_yield_day + 1) // 2 <= age <= max_yield_day`, fertilizer doubles it."""
    rng = np.random.default_rng(hash((crop, day)) % 2**31)
    for x, y in ((1, 1), (2, 3), (4, 4), (0, 7)):
        state, farm = _paired_board(rng, crop, day)
        farm["farmer"] = [x, y]

        O.water(state, np.array([[x, y]]), np.array([True]), day)
        kg._apply_unit_action(farm, kg._new_private(), 0, ["WATER"], BOARD, day, TURNS_PER_DAY, 100)

        _assert_tiles_match(state, farm, f"WATER {crop} day {day} at {(x, y)}")


@pytest.mark.parametrize("crop", CROPS)
@pytest.mark.parametrize("day", [1, 4, 9, 13, 20])
def test_harvest_matches_the_reference_and_clears_only_non_ongoing(crop, day):
    rng = np.random.default_rng(hash((crop, day, "h")) % 2**31)
    for x, y in ((1, 1), (3, 2), (4, 4)):
        state, farm = _paired_board(rng, crop, day)
        farm["farmer"] = [x, y]
        private = kg._new_private()

        carried = np.zeros((1, len(CROPS)), dtype=np.int64)
        carried = O.harvest(state, np.array([[x, y]]), np.array([True]), day, carried)
        kg._apply_unit_action(farm, private, 0, ["HARVEST"], BOARD, day, TURNS_PER_DAY, 100)

        _assert_tiles_match(state, farm, f"HARVEST {crop} day {day} at {(x, y)}")
        expected = private["inventories"][0].get(crop, 0)
        assert carried[0, CROP_INDEX[crop]] == expected, f"carried units, {crop} day {day}"


def test_dig_matches_the_reference():
    rng = np.random.default_rng(11)
    for x, y in ((1, 1), (2, 2), (3, 4), (0, 9)):
        state, farm = _paired_board(rng, "WHEAT", day=5)
        farm["farmer"] = [x, y]

        O.dig(state, np.array([[x, y]]), np.array([True]))
        kg._apply_unit_action(farm, kg._new_private(), 0, ["DIG"], BOARD, 5, TURNS_PER_DAY, 100)

        _assert_tiles_match(state, farm, f"DIG at {(x, y)}")


def test_a_batch_of_games_each_doing_a_different_op_stays_in_parity():
    """The point of the module: same-indexed unit, different op per game, one vector pass."""
    rng = np.random.default_rng(3)
    day = 4
    positions, states, farms, chosen = [], [], [], []
    for op in (O.WATER, O.HARVEST, O.DIG, O.NOOP):
        st, fm = _paired_board(rng, "WHEAT", day)
        x, y = 2, 3
        fm["farmer"] = [x, y]
        states.append(st)
        farms.append(fm)
        positions.append((x, y))
        chosen.append(op)

    batch = TileState(len(states))
    for i, st in enumerate(states):
        for field in ("kind", "crop", "planted_day", "watered_today", "consecutive_unwatered",
                      "yield_units", "max_lifespan_step", "fertilized_until_day"):
            getattr(batch, field)[i] = getattr(st, field)[0]

    pos = np.array(positions, dtype=np.int64)
    ops = np.array(chosen)
    carried = np.zeros((len(states), len(CROPS)), dtype=np.int64)

    O.water(batch, pos, ops == O.WATER, day)
    carried = O.harvest(batch, pos, ops == O.HARVEST, day, carried)
    O.dig(batch, pos, ops == O.DIG)

    for i, (fm, op) in enumerate(zip(farms, chosen)):
        kg._apply_unit_action(fm, kg._new_private(), 0, [OP_NAMES[op]], BOARD, day, TURNS_PER_DAY, 100)
        single = TileState(1)
        for field in ("kind", "crop", "planted_day", "watered_today", "consecutive_unwatered",
                      "yield_units", "max_lifespan_step", "fertilized_until_day"):
            getattr(single, field)[0] = getattr(batch, field)[i]
        _assert_tiles_match(single, fm, f"batched {OP_NAMES[op]}")
