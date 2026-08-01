"""Parity between the JAX simulator and the numpy one, at full episode length.

The numpy sim is the reference here. It is already gated against `reference/kaggriculture.py`
(60/60 full-length episodes exact), so matching it field for field inherits that guarantee.

**These tests are long on purpose.** The numpy sim passed a 200-step end-to-end check and then
failed the 719-step gate 40 out of 40, because a seed was being spent on plants that never landed
and the farm starved only gradually. A short parity check is a different test from a long one, not
a cheaper version of it. Every test here that claims parity runs the full 719 steps and compares
*every* state array after *every* step, not just the bank at the end.
"""

import numpy as np
import pytest

from kagg.sim import ops as O
from kagg.sim.farm import MAX_UNITS, N_CROPS, N_LAND, SHED_CAP
from kagg.sim.game import Actions, Game
from kagg.sim.market import ANIMALS, ITEMS, N_ANIMALS, N_ITEMS, N_PRODUCTS, PRODUCT_INDEX
from kagg.sim.parity import random_script
from kagg.sim.tiles import CROPS

jax_sim = pytest.importorskip("kagg.sim.jax_sim")

EPISODE = 719

TILE_FIELDS = (
    "kind", "crop", "planted_day", "watered_today", "consecutive_unwatered",
    "yield_units", "max_lifespan_step", "fertilized_until_day",
)
FARM_FIELDS = ("seeds", "shed", "carried", "unit_pos", "n_units", "hires_today", "n_land")


# ---- comparison ------------------------------------------------------------------------------


def _mismatches(game, state, label=""):
    """Every way the two simulators' states differ, as human-readable strings."""
    problems = []

    def check(name, a, b):
        a, b = np.asarray(a), np.asarray(b)
        if not np.array_equal(a, b):
            where = np.argwhere(a != b)[:3]
            problems.append(f"{label}{name}: {len(np.argwhere(a != b))} differ, first at "
                            f"{where.tolist()} numpy={a[tuple(where[0])]} jax={b[tuple(where[0])]}")

    check("money", game.money(), state.farm.money)
    check("inventory", game.inventory, state.inventory)
    for p in range(2):
        for field in TILE_FIELDS:
            check(f"tiles[{p}].{field}",
                  getattr(game.tiles[p], field), getattr(state.tiles, field)[:, p])
        for field in FARM_FIELDS:
            check(f"farm[{p}].{field}",
                  getattr(game.farms[p], field), getattr(state.farm, field)[:, p])
    return problems


def _run_lockstep(action_stream, batch, unlock_schedule=None, steps=EPISODE,
                  starting_money=3000.0):
    """Drive both simulators with identical actions, asserting equality after every step."""
    game = Game(batch, starting_money=starting_money, weed_chance=0.0,
                unlock_schedule=unlock_schedule)
    state = jax_sim.reset(batch, starting_money=starting_money,
                          unlock_schedule=unlock_schedule)
    # Peaks rather than end-of-episode values, so a test can prove it actually visited the states
    # it claims to cover -- a random script usually ends broke with an empty shed.
    peak = {"shed": 0, "units": 1, "land": 0, "carried": 0}

    for t in range(steps):
        actions = action_stream(t)
        game.step(actions)
        state = jax_sim.step(state, jax_sim.from_numpy_actions(actions))

        problems = _mismatches(game, state, label=f"step {t}: ")
        assert problems == [], "\n".join(problems)

        peak["shed"] = max(peak["shed"], int(game.farms[0].shed.sum(axis=1).max()))
        peak["units"] = max(peak["units"], int(game.farms[0].n_units.max()))
        peak["land"] = max(peak["land"], int(game.farms[0].n_land.max()))
        peak["carried"] = max(peak["carried"], int(game.farms[0].carried.sum()))
    return game, state, peak


# ---- action sources --------------------------------------------------------------------------


def _script_actions(scripts):
    """Turn `random_script` output into per-step numpy `Actions`, as `parity.run_sim` does."""
    batch = len(scripts)

    def stream(step):
        actions = Actions(batch)
        for b, script in enumerate(scripts):
            entry = script[step]
            for p in range(2):
                ops, crops, items, qtys = entry["units"][p]
                actions.unit_op[b, p, 0] = ops[0]
                actions.unit_crop[b, p, 0] = crops[0]
                actions.unit_item[b, p, 0] = items[0]
                actions.unit_qty[b, p, 0] = qtys[0]
                for item, n in entry["sell"][p].items():
                    actions.sell[b, p, PRODUCT_INDEX[item]] = n
                for crop, n in entry["buy_seed"][p].items():
                    actions.buy_seed[b, p, CROPS.index(crop)] = n
                for item, n in entry["buy_product"][p].items():
                    actions.buy_product[b, p, PRODUCT_INDEX[item]] = n
                for animal, n in entry["buy_animal"][p].items():
                    actions.buy_animal[b, p, ANIMALS.index(animal)] = n
                actions.hire[b, p] = entry["hire"][p]
                actions.buy_land[b, p] = entry["buy_land"][p]
        return actions

    return stream


def _dense_actions(rng, batch, steps, hire_rate=0.06, land_rate=0.004):
    """Random actions for *all 24 unit slots*, plus hiring and land.

    `random_script` only ever drives the farmer, so on its own it never exercises the unit-slot
    loop past index 0, never fills the shed to its cap, and never buys land. This does, because
    the slot loop and the shed-overflow walk are exactly the two places where the JAX port
    restructures the numpy sim's control flow.
    """
    # All eighteen ops, not just the nine crop ones. Restricting this pool to the ops the port
    # already had is what let the JAX sim ship with no atomic-PLANT rule and pass 14/14.
    weights = np.array([
        0.06, 0.04, 0.04, 0.04, 0.04, 0.14, 0.10, 0.09, 0.05,   # crop game
        0.06, 0.04, 0.06, 0.07, 0.04, 0.04, 0.03, 0.03, 0.03,   # logistics and animals
    ])
    weights = weights / weights.sum()
    ops_pool = np.array([
        O.NOOP, O.NORTH, O.SOUTH, O.EAST, O.WEST, O.WATER, O.HARVEST, O.PLANT_OP, O.DIG,
        O.PICKUP, O.DROP, O.PLACE, O.FEED, O.CARE, O.COLLECT_FERT, O.FERTILIZE,
        O.BUILD_COOP, O.BUILD_PASTURE,
    ])

    frames = []
    for t in range(steps):
        a = Actions(batch)
        a.unit_op[:] = rng.choice(ops_pool, size=(batch, 2, MAX_UNITS), p=weights)
        a.unit_crop[:] = rng.integers(0, N_CROPS, size=(batch, 2, MAX_UNITS))
        a.unit_item[:] = rng.integers(0, N_ITEMS, size=(batch, 2, MAX_UNITS))
        a.unit_qty[:] = rng.integers(1, 4, size=(batch, 2, MAX_UNITS))
        a.sell[:] = np.where(
            rng.random((batch, 2, N_PRODUCTS)) < 0.12, rng.integers(0, 6, (batch, 2, N_PRODUCTS)), 0
        )
        a.buy_seed[:] = np.where(
            rng.random((batch, 2, N_CROPS)) < 0.25, rng.integers(1, 4, (batch, 2, N_CROPS)), 0
        )
        a.buy_product[:] = np.where(
            rng.random((batch, 2, N_PRODUCTS)) < 0.10, rng.integers(1, 4, (batch, 2, N_PRODUCTS)), 0
        )
        a.buy_animal[:] = np.where(
            rng.random((batch, 2, N_ANIMALS)) < 0.05, 1, 0
        )
        a.hire[:] = rng.random((batch, 2)) < hire_rate
        a.buy_land[:] = rng.random((batch, 2)) < land_rate
        if t == 0:
            # Land is 1000/2000/4000 and the bank starts at 3000, so a random 0.4%-per-turn draw
            # essentially never fires once seeds have drained the bank. Buy it while it is
            # affordable, or the quadrant-unlock path is never exercised at all.
            a.buy_land[:] = True
            a.buy_seed[:] = 0
        frames.append(a)

    return lambda step: frames[step]


# ---- tests -----------------------------------------------------------------------------------


def test_price_is_bit_identical_to_numpy():
    """One wrong rounding here shifts every sale in the game and looks like a strategy change.

    Checked far outside anything an episode can reach: inventory starts at 10,000, the town can
    only drain about 1,200 a season and both sheds together can only add about 6,000.
    """
    import kagg.sim.market as market

    inventory = np.arange(-30_000, 120_000, dtype=np.int64)[:, None] * np.ones(
        (1, N_PRODUCTS), dtype=np.int64
    )
    assert np.array_equal(market.price(inventory), np.asarray(jax_sim.price(inventory)))


def test_initial_state_matches_numpy():
    game = Game(3, weed_chance=0.0)
    state = jax_sim.reset(3)
    assert _mismatches(game, state) == []


@pytest.mark.parametrize("seed", [0, 1])
def test_full_length_episode_matches_numpy(seed):
    """719 steps of `parity.random_script`, every state array compared every step."""
    rng = np.random.default_rng(seed)
    scripts = [random_script(rng, steps=EPISODE) for _ in range(2)]
    unlocks = {2: 0, 5: 3, 9: 6, 14: 1, 19: 4, 26: 7}

    _run_lockstep(_script_actions(scripts), batch=2, unlock_schedule=unlocks)


def test_full_length_episode_with_all_units_hiring_and_land():
    """The stress case: 24 live unit slots, a full shed, hiring, and land purchases."""
    rng = np.random.default_rng(17)
    stream = _dense_actions(rng, batch=3, steps=EPISODE, hire_rate=0.9, land_rate=0.02)

    # A deliberately rich bank. Every one of these paths is gated on affordability, so at the real
    # starting 3000 a random script goes broke on day one and the full crew, the third quadrant and
    # a shed at its cap are simply never reached -- the test would pass without testing them.
    _game, _state, peak = _run_lockstep(
        stream, batch=3, unlock_schedule={1: 0, 6: 2, 12: 5}, starting_money=1_000_000.0
    )

    # A test that never reached the interesting states would pass vacuously. Ask what a passing
    # run would look like if the mechanism were broken -- here, an episode that never hired, never
    # bought land and never put anything in a shed proves nothing about the paths it claims.
    assert peak["land"] == N_LAND, f"not every quadrant was bought, peaked at {peak['land']}"
    assert peak["units"] >= MAX_UNITS, f"the crew never filled up, peaked at {peak['units']}"
    assert peak["shed"] > 0, "nothing ever reached a shed"
    assert peak["carried"] > 0, "nothing was ever harvested and carried"


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_shed_overflow_destroys_the_same_haul_as_the_numpy_sim(seed):
    """Direct test of the one place the JAX port replaces a sequential walk with a prefix sum.

    `drop_to_shed` fills the shed unit by unit and product by product and **destroys** whatever
    does not fit, so which unit loses its haul depends entirely on walk order. The JAX version
    computes that from a `cumsum` instead of walking; if the order were wrong the totals would
    still often agree, so this compares the per-product breakdown with the cap deliberately biting.

    Random scripts do not reach this state -- the dense episode above peaks at a shed of 3 -- so
    the carried inventory is injected rather than earned.
    """
    rng = np.random.default_rng(seed)
    batch = 4
    game = Game(batch, weed_chance=0.0)
    state = jax_sim.reset(batch)

    carried = rng.integers(0, 7, size=(batch, 2, MAX_UNITS, N_ITEMS))
    shed = rng.integers(0, 12, size=(batch, 2, N_ITEMS))
    assert carried.sum(axis=(2, 3)).min() > SHED_CAP, "the cap must actually bite"

    for p in range(2):
        game.farms[p].carried[:] = carried[:, p]
        game.farms[p].shed[:] = shed[:, p]
    game.step_index = 23
    import jax.numpy as jnp
    state = state._replace(
        # Per game now, not one scalar for the batch: episodes have to be able to run out of
        # phase with each other, which is what puts a terminal reward in every training update.
        step_index=jnp.full((batch,), 23, dtype=jnp.int32),
        farm=state.farm._replace(
            carried=jnp.asarray(carried, dtype=jnp.int32),
            shed=jnp.asarray(shed, dtype=jnp.int32),
        ),
    )

    actions = Actions(batch)
    game.step(actions)
    state = jax_sim.step(state, jax_sim.from_numpy_actions(actions))

    assert _mismatches(game, state) == []
    assert int(np.asarray(state.farm.shed).sum(axis=-1).min()) == SHED_CAP


def test_hiring_actually_fills_unit_slots_during_the_day():
    """Guards the loop bound: the slot loop runs to max(n_units), so hiring must widen it."""
    batch = 2
    game = Game(batch, weed_chance=0.0)
    state = jax_sim.reset(batch)

    reached = 0
    for t in range(48):
        actions = Actions(batch)
        actions.hire[:] = True
        actions.unit_op[:, :, :] = O.SOUTH
        game.step(actions)
        state = jax_sim.step(state, jax_sim.from_numpy_actions(actions))
        reached = max(reached, int(game.farms[0].n_units.max()))
        assert _mismatches(game, state, label=f"step {t}: ") == []

    assert reached > 5, f"hiring never grew the crew past {reached}"


def test_atomic_plant_blocks_every_request_for_a_crop_the_seed_store_cannot_cover():
    """Two units, one seed, both asking for it: the reference plants neither, so neither may.

    This needs its own test because the random streams above cannot be trusted to reach it. The
    rule only *discriminates* when `0 < seeds < demand` -- with no seeds both rules plant nothing,
    and with enough seeds both plant everything. Across 2,400 player-turns of the dense stream that
    window opened twice, and neither time did the plant land on an empty tile. The JAX port shipped
    with no atomic-PLANT rule at all and this file still passed 14/14.
    """
    from kagg.sim.tiles import CROP_INDEX, EMPTY, PLANT

    wheat = CROP_INDEX["WHEAT"]
    game = Game(1, weed_chance=0.0)
    state = jax_sim.reset(1)

    def turn(fill):
        actions = Actions(1)
        fill(actions)
        game.step(actions)
        return jax_sim.step(state, jax_sim.from_numpy_actions(actions))

    # Turn 0: hire a hand and buy exactly one wheat seed.
    def setup(a):
        a.hire[0, 0] = True
        a.buy_seed[0, 0, wheat] = 1
    state = turn(setup)
    assert int(game.farms[0].n_units[0]) == 2, "the crew never grew, so nothing is being tested"
    assert int(game.farms[0].seeds[0, wheat]) == 1

    # Turn 1: put the two units on different empty tiles inside the unlocked quadrant.
    state = turn(lambda a: a.unit_op.__setitem__((0, 0, slice(0, 2)), [O.NORTH, O.WEST]))
    positions = {tuple(game.farms[0].unit_pos[0, u]) for u in range(2)}
    assert len(positions) == 2, f"units share a tile, so only one plant could land anyway: {positions}"
    for x, y in positions:
        assert game.tiles[0].kind[0, y * 10 + x] == EMPTY

    # Turn 2: both ask for wheat. Demand is 2 against 1 seed, so the reference drops both.
    def both_plant(a):
        a.unit_op[0, 0, :2] = O.PLANT_OP
        a.unit_crop[0, 0, :2] = wheat
    state = turn(both_plant)

    assert _mismatches(game, state) == []
    assert int(game.farms[0].seeds[0, wheat]) == 1, "a blocked PLANT must not spend the seed"
    assert int((game.tiles[0].kind[0] == PLANT).sum()) == 0, "the blocked PLANT landed anyway"


def test_both_seats_are_paid_the_same_price_on_a_contested_unit():
    """`_process_market` quotes both seats before either commits, so a contested unit pays equally.

    Like the atomic PLANT rule above, this needs its own test: the random streams almost never have
    both players holding stock of the same product on the same turn, so re-quoting between the
    seats -- which is what this port did -- costs seat 1 a dollar a unit without any test noticing.
    In real play both agents sell the same staples every turn, so it is the normal case.

    The shed is written directly rather than farmed up to, because reaching a contested sale
    through harvest and the nightly drop takes most of a season and proves nothing extra.
    """
    melon = PRODUCT_INDEX["MELON"]
    batch = 1
    game = Game(batch, weed_chance=0.0)
    state = jax_sim.reset(batch)

    for p in range(2):
        game.farms[p].shed[:, melon] = 20
    state = state._replace(farm=state.farm._replace(shed=state.farm.shed.at[:, :, melon].set(20)))

    actions = Actions(batch)
    actions.sell[:, :, melon] = 20
    game.step(actions)
    state = jax_sim.step(state, jax_sim.from_numpy_actions(actions))

    assert _mismatches(game, state) == []

    banks = game.money()[0]
    assert int(game.farms[0].shed[0, melon]) == 0, "nothing was actually sold"
    assert banks[0] == banks[1], f"contested units must pay both seats alike, got {banks}"


def test_a_batch_of_different_scripts_stays_independent():
    """Games in a batch must not contaminate each other -- the whole point of batching."""
    rng = np.random.default_rng(5)
    scripts = [random_script(rng, steps=EPISODE) for _ in range(4)]
    _run_lockstep(_script_actions(scripts), batch=4, unlock_schedule={3: 1, 11: 4})


def test_rollout_matches_stepping_one_turn_at_a_time():
    """`rollout` scans the same step function; a divergence means the scan carries state wrong."""
    rng = np.random.default_rng(31)
    steps = 96
    stream = _dense_actions(rng, batch=2, steps=steps)
    frames = [stream(t) for t in range(steps)]

    state = jax_sim.reset(2)
    scanned, banks = jax_sim.rollout(state, jax_sim.stack_actions(frames))

    looped = jax_sim.reset(2)
    for f in frames:
        looped = jax_sim.step(looped, jax_sim.from_numpy_actions(f))

    assert np.array_equal(np.asarray(scanned.farm.money), np.asarray(looped.farm.money))
    assert np.array_equal(np.asarray(scanned.tiles.kind), np.asarray(looped.tiles.kind))
    assert banks.shape == (steps, 2, 2)


def test_full_length_rollout_matches_the_numpy_sim():
    """A whole 719-step episode inside one XLA call, against the numpy sim turn by turn.

    `rollout` is what training will actually call, so it gets its own full-length gate rather than
    inheriting one from `step`. The per-step `[T, B, P]` bank the scan emits is compared against
    the numpy sim's bank at every turn, and the final state is compared field for field.
    """
    rng = np.random.default_rng(23)
    stream = _dense_actions(rng, batch=2, steps=EPISODE, hire_rate=0.3, land_rate=0.01)
    frames = [stream(t) for t in range(EPISODE)]

    game = Game(2, starting_money=250_000.0, weed_chance=0.0)
    numpy_banks = []
    for f in frames:
        game.step(f)
        numpy_banks.append(game.money().copy())

    state = jax_sim.reset(2, starting_money=250_000.0)
    final, banks = jax_sim.rollout(state, jax_sim.stack_actions(frames))

    assert np.array_equal(np.stack(numpy_banks), np.asarray(banks))
    assert _mismatches(game, final) == []


def test_weeds_spawn_at_roughly_the_configured_rate():
    """The one place the JAX sim is its own RNG stream, so check the rate, not the sequence."""
    rate = 0.05
    state = jax_sim.reset(64, seed=3)
    empty_before = int((np.asarray(state.tiles.kind) == 0).sum())

    actions = jax_sim.zero_actions(64)
    for _ in range(24):
        state = jax_sim.step(state, actions, weed_chance=rate)

    weeds = int((np.asarray(state.tiles.kind) == 2).sum())
    expected = rate * empty_before
    assert 0.6 * expected < weeds < 1.4 * expected, \
        f"{weeds} weeds against ~{expected:.0f} expected"


def test_done_flags_at_the_same_step_as_the_numpy_sim():
    game = Game(1, weed_chance=0.0)
    state = jax_sim.reset(1)
    actions = Actions(1)
    jax_actions = jax_sim.from_numpy_actions(actions)

    for _ in range(EPISODE):
        np_done = game.step(actions)
        state = jax_sim.step(state, jax_actions)
        assert bool(jax_sim.done(state)) == np_done
    assert np_done is True
