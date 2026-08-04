"""`routines.grow()` must emit a chain that survives the dawn reset and the atomic PLANT rule.

`ranch()` is safe by construction: it binds to a shed-access tile and therefore never emits a movement
op, so no edit can invalidate a later position. `grow()` cannot inherit that -- there are only four
shed-access tiles and animals want them, so a crop block sits on the other ~96 and the routine has to
route. Every test here exists because that reintroduces a failure mode `ranch()` had designed out.

The two that would have caught a real bug rather than a typo:

* `test_the_block_is_re_walked_from_spawn_every_day` -- `_end_of_day` teleports every unit back to
  spawn (`jax_sim.py:1228-1236`). A routine that walks to the block once and then waters for the rest
  of the season waters the *spawn tile*. `ranch()`'s docstring records this exact defect starving every
  animal outside (4,4).
* `test_an_ongoing_crop_is_harvested_on_every_eligible_day` -- once `production_count` reaches
  `MAX_YIELD` the tile's `max_lifespan_step` is set and `_decay_plants` eats a unit every other step.
  Accumulated yield rots in about a day. HARVEST is a no-op when nothing is ready, so the cheap
  correct policy is to harvest daily and make decay unreachable.
"""

import numpy as np
import pytest

from kagg.search import routines as R


def _ops_on_day(script, unit, day):
    lo, hi = day * R.TURNS_PER_DAY, (day + 1) * R.TURNS_PER_DAY
    return [R.OP_NAMES[int(o)] for o in script.unit_op[lo:hi, unit]]


def _tile_visited(script, unit, day, tile):
    """Replay the day's movement ops and report whether the unit ever stands on `tile`."""
    pos = list(R.SPAWN)
    seen = {tuple(pos)}
    for name in _ops_on_day(script, unit, day):
        if name == "NORTH":
            pos[1] -= 1
        elif name == "SOUTH":
            pos[1] += 1
        elif name == "EAST":
            pos[0] += 1
        elif name == "WEST":
            pos[0] -= 1
        seen.add(tuple(pos))
    return tuple(tile) in seen


def _op_positions(script, unit, day, op_name):
    """Positions at which `op_name` is emitted, by replaying movement from spawn."""
    pos = list(R.SPAWN)
    out = []
    for name in _ops_on_day(script, unit, day):
        if name == "NORTH":
            pos[1] -= 1
        elif name == "SOUTH":
            pos[1] += 1
        elif name == "EAST":
            pos[0] += 1
        elif name == "WEST":
            pos[0] -= 1
        elif name == op_name:
            out.append(tuple(pos))
    return out


NW_BLOCK = [(3, 3), (4, 3)]          # two tiles adjacent to spawn, inside the starting quadrant


def test_the_block_is_re_walked_from_spawn_every_day():
    """**The property `ranch()` got for free and this routine must earn.**"""
    s = R.grow(R.Script(), "WHEAT", NW_BLOCK, plant_day=0)
    for day in range(0, R.SEASON_DAYS):
        for tile in NW_BLOCK:
            assert _tile_visited(s, 0, day, tile), (
                f"day {day}: unit never reaches {tile}. Every day starts at spawn {R.SPAWN} because "
                "`_end_of_day` teleports the crew, so each day needs its own full walk.")


def test_every_working_op_lands_on_a_block_tile_and_never_on_spawn():
    """A WATER emitted while standing on the shed is the silent version of the bug above."""
    s = R.grow(R.Script(), "WHEAT", NW_BLOCK, plant_day=0)
    for op_name in ("PLANT", "WATER", "HARVEST"):
        for day in range(0, R.SEASON_DAYS):
            for pos in _op_positions(s, 0, day, op_name):
                assert pos in [tuple(t) for t in NW_BLOCK], (
                    f"day {day}: {op_name} emitted at {pos}, which is not in the block")


def test_a_crop_is_watered_every_day_it_is_in_the_ground():
    """`consecutive_unwatered >= 2` kills the plant, for ongoing crops too."""
    s = R.grow(R.Script(), "STRAWBERRY", [(3, 3)], plant_day=0)
    for day in range(1, R.SEASON_DAYS):
        assert "WATER" in _ops_on_day(s, 0, day), f"day {day} has no WATER; the plant dies at 2 days"


def test_an_ongoing_crop_is_harvested_on_every_eligible_day():
    """Decay starts the moment the lifetime cap is hit, so waiting for a schedule loses yield."""
    first = R.CROP_TABLE["STRAWBERRY"]["first"]
    s = R.grow(R.Script(), "STRAWBERRY", [(3, 3)], plant_day=0)
    for day in range(first, R.SEASON_DAYS):
        assert "HARVEST" in _ops_on_day(s, 0, day), (
            f"day {day} (age {day} >= first yield {first}) has no HARVEST -- accumulated units decay")


def test_an_ongoing_crop_is_planted_exactly_once():
    """HARVEST does not clear an ongoing tile, so replanting it would be a wasted seed and turn."""
    s = R.grow(R.Script(), "STRAWBERRY", [(3, 3)], plant_day=0)
    plants = sum(_ops_on_day(s, 0, d).count("PLANT") for d in range(R.SEASON_DAYS))
    assert plants == 1, f"ongoing crop planted {plants} times"


def test_a_one_shot_crop_runs_more_than_one_cycle():
    """HARVEST clears a non-ongoing tile to EMPTY, which is where wheat's multi-cycle yield comes from."""
    s = R.grow(R.Script(), "WHEAT", [(3, 3)], plant_day=0)
    plants = sum(_ops_on_day(s, 0, d).count("PLANT") for d in range(R.SEASON_DAYS))
    assert plants > 1, "wheat planted once; the tile is cleared on harvest and should be reused"


def test_two_blocks_of_one_crop_on_one_day_order_the_sum_of_their_seeds():
    """The atomic rule drops EVERY request for a crop when demand exceeds seeds, not just the excess."""
    s = R.Script()
    R.grow(s, "WHEAT", [(3, 3), (4, 3)], plant_day=0, unit=0)
    R.grow(s, "WHEAT", [(3, 4)], plant_day=0, unit=1)
    ordered = int(s.buy_seed[0, R.CROPS.index("WHEAT")])
    assert ordered == 3, (
        f"ordered {ordered} wheat seeds for 3 tiles planted on day 0; `maximum` would give 2 and the "
        "atomic rule would then fail all three plants")


def test_seeds_are_ordered_before_the_turn_that_plants_them():
    """Demand is tested against seeds held at the START of the turn."""
    s = R.grow(R.Script(), "WHEAT", [(3, 3)], plant_day=0)
    seed_turns = np.flatnonzero(s.buy_seed[:, R.CROPS.index("WHEAT")] > 0)
    plant_turns = np.flatnonzero(s.unit_op[:, 0] == R.OP["PLANT"])
    assert len(seed_turns) and len(plant_turns)
    assert seed_turns[0] < plant_turns[0], (
        f"seeds ordered at turn {seed_turns[0]} but planted at {plant_turns[0]}")


def test_co_located_blocks_share_hands_rather_than_each_hiring_their_own():
    """Same `maximum` argument `ranch()` makes: unit 2 existing already provides units 0 and 1."""
    s = R.Script()
    R.grow(s, "WHEAT", [(3, 3)], plant_day=0, unit=1)
    R.grow(s, "CARROT", [(3, 4)], plant_day=0, unit=2)
    assert int(s.hire[0]) == 2, f"hired {int(s.hire[0])}; two co-located blocks need max(1,2)=2 hands"


def test_a_day_that_cannot_fit_in_24_turns_raises_rather_than_spilling():
    """A silent overflow would write ops into the next dawn, where the unit has been teleported away."""
    far_block = [(x, 0) for x in range(5)]        # a full row at the top of NW, 4 steps from spawn
    with pytest.raises(ValueError, match="turns"):
        R.grow(R.Script(), "WHEAT", far_block + [(x, 1) for x in range(5)], plant_day=0)


def test_a_block_spanning_two_quadrants_is_refused():
    """v1 routes inside one quadrant; a cross-quadrant path has to order land before the walk."""
    with pytest.raises(ValueError, match="quadrant"):
        R.grow(R.Script(), "WHEAT", [(3, 3), (7, 3)], plant_day=0)


def test_a_block_outside_nw_orders_its_land_first():
    """Movement is blocked by LOCKED at the target cell, so the parcel must be bought before the walk."""
    s = R.grow(R.Script(), "WHEAT", [(7, 3)], plant_day=5, land_day=1)
    bought = np.flatnonzero(s.buy_land > 0)
    assert len(bought) == R.land_purchases_for((7, 3))
    assert bought[0] // R.TURNS_PER_DAY == 1, "land not ordered on land_day"


def test_a_short_script_is_truncated_rather_than_overrun():
    """`Script.op` promises "out-of-range turns are dropped so a routine may run past the season", and
    the market arrays have to honour the same contract. They did not: `buy_seed[d]` was written
    unguarded, so a script shorter than a season raised IndexError at day 2. Found by
    `chains._fits_in_a_day`, which probes a block against a two-day script.
    """
    short = R.Script(T=R.TURNS_PER_DAY * 2)
    R.grow(short, "WHEAT", [(3, 3)], plant_day=0)          # must not raise
    assert short.unit_op.shape[0] == R.TURNS_PER_DAY * 2


def test_a_tile_is_watered_on_the_day_it_is_planted():
    """**The bug the money test found.** A seedling starts at `consecutive_unwatered = 1`, so dusk
    takes it to 2 and `_daily_refresh_plants` turns it into a WEED on its first night. Traced in
    `data/logs/crop_trace.log`:

        turn   3  PLANT  kind 0->3  yld 1  unwat 1
        turn  23  PASS   kind 2                unwat 2     <- 2 == WEED

    Everything after that is silently dead: WATER needs `kind == PLANT` and PLANT needs `EMPTY`, so a
    weeded tile refuses both while the routine keeps paying for seeds.
    """
    s = R.grow(R.Script(), "WHEAT", [(3, 3)], plant_day=0)
    day0 = _ops_on_day(s, 0, 0)
    assert "PLANT" in day0 and "WATER" in day0, f"day 0 ops are {[o for o in day0 if o != 'PASS']}"
    assert day0.index("WATER") > day0.index("PLANT"), "watered before planting"


def _run(script, seed=0):
    """Final money for seat 0, seat 1 passing. Weeds off, so the number is exact."""
    import jax.numpy as jnp
    from kagg.sim import jax_sim as J

    fields = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
              "buy_product", "buy_animal", "hire", "buy_land")
    state = J.reset_with_shops(1, seed=seed)
    arrs = script.arrays()
    for t in range(script.T):
        acts = {f: jnp.asarray(np.stack([np.asarray(arrs[f][t]),
                                         np.zeros_like(np.asarray(arrs[f][t]))])[None])
                for f in fields}
        state = J.step(state, J.Actions(**acts), weed_chance=0.0)
    return float(np.asarray(state.farm.money)[0, 0])


@pytest.mark.parametrize("crop_name", R.CROPS)
def test_a_crop_routine_pays_for_itself(crop_name):
    """**The test that caught the real bug.** Measured before the fix, every crop lost exactly its
    seed cost -- i.e. banked zero revenue:

        WHEAT -60  CARROT -160  TOMATO -50  STRAWBERRY -100  MELON -240

    Cause: a harvest lands in `carried`, and `_drop_to_shed` only runs at dusk (`jax_sim.py:1230`), so
    a SELL emitted on the harvest day itself quotes against a shed that does not hold the crop yet.
    `ranch()` avoids this by standing on a shed tile and emitting DROP before its sell; a crop block is
    out in the field where DROP cannot reach the shed, so the sell has to wait for the next dawn.
    """
    base = _run(R.Script())
    s = R.Script()
    R.grow(s, crop_name, [(3, 3)], plant_day=0)
    got = _run(s)
    assert got > base, f"{crop_name} lost money: ${got:,.0f} vs baseline ${base:,.0f}"


def test_a_harvest_is_sold_after_the_shed_has_received_it():
    """The structural form of the same property, independent of prices."""
    s = R.grow(R.Script(), "WHEAT", [(3, 3)], plant_day=0)
    harvest_days = {int(t) // R.TURNS_PER_DAY
                    for t in np.flatnonzero(s.unit_op[:, 0] == R.OP["HARVEST"])}
    sell_days = {int(t) // R.TURNS_PER_DAY
                 for t in np.flatnonzero(s.sell[:, R.PRODUCTS.index("WHEAT")] > 0)}
    assert sell_days, "nothing is ever sold"
    for d in sell_days:
        assert (d - 1) in harvest_days, (
            f"selling on day {d} with no harvest on day {d-1}; carried stock only reaches the shed "
            "at dusk, so a same-day sell finds it empty")


def test_the_crop_table_matches_the_simulator():
    """These are literals here so the module stays dependency-free; they must not drift."""
    from kagg.sim import tiles as T
    for i, name in enumerate(R.CROPS):
        row = R.CROP_TABLE[name]
        assert row["first"] == int(T.FIRST_YIELD_DAY[i]), name
        assert row["max_day"] == int(T.MAX_YIELD_DAY[i]), name
        assert row["max_yield"] == int(T.MAX_YIELD[i]), name
        assert row["ongoing"] == bool(T.ONGOING[i]), name
