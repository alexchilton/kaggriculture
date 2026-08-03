"""Every dollar a farm gains or loses must be attributable to a named cause.

**Why this exists.** `HANDOFF_2026-08-03.md` item 1: the farmer replay's bank falls -21/day to day
10 and then -552/day to day 15. That is a cliff, not a decay, and a policy converged on inaction
cannot produce a cliff -- so something *happens* in that window. `play_checkpoint` reports the bank
per game-day, which shows the cliff and cannot say what caused it.

The instrument is a per-turn decomposition of the money delta. The thing that makes it trustworthy
is the invariant tested here: **the named components must sum to the observed change exactly.** A
decomposition that leaves a residual is describing something other than what happened, which is the
exact failure species `CLAUDE.md` records for the per-opponent win rate -- correct per row, and
measuring the wrong thing.

Exact means exact. Money is float64 under `jax_enable_x64` and every mutation is an add of a
quoted price, so there is no rounding to tolerate. `atol=0` is deliberate; loosen it and this test
stops being able to fail.
"""

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from kagg.sim import jax_sim as J


# Both entry points are jitted here for speed, and that is also the honest path: training runs
# `step` inside a `lax.scan` and `play_checkpoint` runs `step_accounted` inside one, so neither is
# ever executed op-by-op in production. Eager mode dispatches every primitive in the ten-slot
# market loop separately and takes seconds per turn.
_STEP = jax.jit(J.step)
_STEP_ACCT = jax.jit(J.step_accounted)


def _random_actions(key, batch):
    """Legal-ish noise across the whole action space, including the money-moving orders."""
    keys = jax.random.split(key, 12)
    shape_u = (batch, J.N_PLAYERS, J.MAX_UNITS)
    return J.Actions(
        unit_op=jax.random.randint(keys[0], shape_u, 0, 18).astype(J._I),
        unit_crop=jax.random.randint(keys[1], shape_u, 0, J.N_CROPS).astype(J._I),
        unit_item=jax.random.randint(keys[2], shape_u, 0, J.N_ITEMS).astype(J._I),
        unit_qty=jax.random.randint(keys[3], shape_u, 1, 6).astype(J._I),
        sell=jax.random.randint(
            keys[4], (batch, J.N_PLAYERS, J.N_PRODUCTS), 0, 4).astype(J._I),
        buy_product=jax.random.randint(
            keys[5], (batch, J.N_PLAYERS, J.N_PRODUCTS), 0, 3).astype(J._I),
        buy_seed=jax.random.randint(
            keys[6], (batch, J.N_PLAYERS, J.N_CROPS), 0, 3).astype(J._I),
        buy_animal=jax.random.randint(
            keys[7], (batch, J.N_PLAYERS, J.N_ANIMALS), 0, 2).astype(J._I),
        hire=jax.random.randint(keys[8], (batch, J.N_PLAYERS), 0, 3).astype(J._I),
        buy_land=jax.random.randint(keys[9], (batch, J.N_PLAYERS), 0, 2).astype(J._I),
    )


def test_step_accounted_returns_the_same_state_as_step():
    """The accounting must not change the simulation. Same seed, same actions, same state.

    This is the guard that matters most: `step` is the function 300/300 full-length parity episodes
    were verified against, and an instrument that perturbs what it measures would invalidate that
    gate silently.
    """
    batch = 8
    state = J.reset(batch)
    key = jax.random.PRNGKey(0)
    plain, accounted = state, state
    for _ in range(60):
        key, sub = jax.random.split(key)
        actions = _random_actions(sub, batch)
        plain = _STEP(plain, actions)
        accounted, _acct = _STEP_ACCT(accounted, actions)

    for name in plain._fields:
        a, b = getattr(plain, name), getattr(accounted, name)
        if isinstance(a, tuple):          # nested NamedTuple (tiles, farm)
            for f in a._fields:
                np.testing.assert_array_equal(
                    np.asarray(getattr(a, f)), np.asarray(getattr(b, f)),
                    err_msg=f"{name}.{f} diverged")
        else:
            np.testing.assert_array_equal(np.asarray(a), np.asarray(b), err_msg=name)


@pytest.mark.parametrize("seed", [0, 1, 2, 3])
def test_the_components_sum_to_the_money_delta_exactly(seed):
    """hire + land + trade == the actual change in the bank, every turn, every game, every seat.

    Random actions are used precisely because they reach combinations a trained policy does not:
    hiring and land-buying on the same turn, buys that fail on affordability, sells into a floored
    market. `CLAUDE.md` records three separate times that a gate only tests what it exercises.
    """
    batch = 16
    state = J.reset(batch)
    key = jax.random.PRNGKey(seed)

    for turn in range(120):
        key, sub = jax.random.split(key)
        actions = _random_actions(sub, batch)
        before = np.asarray(state.farm.money)
        state, acct = _STEP_ACCT(state, actions)
        after = np.asarray(state.farm.money)

        delta = after - before
        named = (np.asarray(acct["trade"])
                 - np.asarray(acct["hire"])
                 - np.asarray(acct["land"]))
        np.testing.assert_array_equal(
            delta, named,
            err_msg=f"unattributed money at turn {turn}: "
                    f"max residual {np.abs(delta - named).max()}")


@pytest.mark.parametrize("seed", [0, 1])
def test_gross_sell_minus_gross_buy_equals_net_trade(seed):
    """`sell - buy == trade`, checked against a counter that was built a different way.

    `trade` is *recovered* as a residual (everything not hire and not land); `sell` and `buy` are
    *accumulated* inside the market loop. They are deliberately not the same computation, so this
    is a real cross-check rather than an identity. Without it the split could be quietly wrong in
    both halves and still satisfy the total.

    The split is what answers "does the chain ever terminate in money": a season that sells nothing
    and a season that sells $600 while spending $1,200 both show a net of -$648.
    """
    batch = 16
    state = J.reset(batch)
    key = jax.random.PRNGKey(seed)
    for turn in range(120):
        key, sub = jax.random.split(key)
        state, acct = _STEP_ACCT(state, _random_actions(sub, batch))
        np.testing.assert_array_equal(
            np.asarray(acct["sell"]) - np.asarray(acct["buy"]),
            np.asarray(acct["trade"]),
            err_msg=f"gross halves disagree with net trade at turn {turn}")


def test_gross_components_are_never_negative():
    """Money cannot flow backwards through a gross counter."""
    batch = 16
    state = J.reset(batch)
    key = jax.random.PRNGKey(3)
    for _ in range(120):
        key, sub = jax.random.split(key)
        state, acct = _STEP_ACCT(state, _random_actions(sub, batch))
        assert np.asarray(acct["sell"]).min() >= 0.0
        assert np.asarray(acct["buy"]).min() >= 0.0


def test_a_pure_sell_books_income_and_no_spend():
    """Selling from a stocked shed lands entirely in `sell`, with `buy` untouched."""
    batch = 4
    state = J.reset(batch)
    shed = np.asarray(state.farm.shed).copy()
    shed[:, :, :J.N_PRODUCTS] = 20                    # something to sell
    state = state._replace(farm=state.farm._replace(shed=jnp.asarray(shed)))
    zeros = jax.tree_util.tree_map(
        jnp.zeros_like, _random_actions(jax.random.PRNGKey(0), batch))
    actions = zeros._replace(sell=jnp.ones_like(zeros.sell))

    before = np.asarray(state.farm.money)
    state, acct = _STEP_ACCT(state, actions)
    after = np.asarray(state.farm.money)

    assert np.asarray(acct["sell"]).sum() > 0, "a sell order earned nothing"
    np.testing.assert_array_equal(np.asarray(acct["buy"]), np.zeros_like(before))
    np.testing.assert_array_equal(after - before, np.asarray(acct["sell"]))


def test_spend_components_are_never_negative():
    """`hire` and `land` are costs. A negative one would mean the sign convention slipped."""
    batch = 16
    state = J.reset(batch)
    key = jax.random.PRNGKey(7)
    for _ in range(120):
        key, sub = jax.random.split(key)
        state, acct = _STEP_ACCT(state, _random_actions(sub, batch))
        assert np.asarray(acct["hire"]).min() >= 0.0
        assert np.asarray(acct["land"]).min() >= 0.0


def test_hiring_is_charged_and_attributed_to_hire():
    """A turn whose only money-moving order is a hire books its whole cost under `hire`.

    Pinning the attribution and not merely the sum: a decomposition that put the hire cost in
    `trade` would still satisfy the invariant above and be useless for reading the cliff.
    """
    batch = 4
    state = J.reset(batch)
    zeros = jax.tree_util.tree_map(
        jnp.zeros_like, _random_actions(jax.random.PRNGKey(0), batch))
    actions = zeros._replace(hire=jnp.ones_like(zeros.hire))

    before = np.asarray(state.farm.money)
    state, acct = _STEP_ACCT(state, actions)
    after = np.asarray(state.farm.money)

    assert np.asarray(acct["hire"]).sum() > 0, "a hire order cost nothing"
    np.testing.assert_array_equal(np.asarray(acct["trade"]), np.zeros_like(before))
    np.testing.assert_array_equal(np.asarray(acct["land"]), np.zeros_like(before))
    np.testing.assert_array_equal(before - after, np.asarray(acct["hire"]))


def test_buying_land_is_charged_and_attributed_to_land():
    """The first quadrant costs exactly `LAND_PRICES[0]`, booked under `land`."""
    batch = 4
    state = J.reset(batch)
    zeros = jax.tree_util.tree_map(
        jnp.zeros_like, _random_actions(jax.random.PRNGKey(0), batch))
    actions = zeros._replace(buy_land=jnp.ones_like(zeros.buy_land))

    state, acct = _STEP_ACCT(state, actions)
    expected = float(np.asarray(J.LAND_PRICES)[0])
    np.testing.assert_array_equal(
        np.asarray(acct["land"]), np.full((batch, J.N_PLAYERS), expected))
    np.testing.assert_array_equal(np.asarray(acct["hire"]),
                                  np.zeros((batch, J.N_PLAYERS)))


def test_a_night_turn_still_balances():
    """Night hauls to the shed and resets the crew to one. It must move no money.

    Worth its own test because `_end_of_day` zeroes `hires_today`, which is what makes the hire
    cost impossible to recover from state deltas alone on the last turn of a day -- the reason this
    accounting is threaded out of `_process_market` rather than reconstructed outside it.
    """
    batch = 8
    state = J.reset(batch)
    key = jax.random.PRNGKey(11)
    night_turns = 0
    for turn in range(J.TURNS_PER_DAY * 2):
        key, sub = jax.random.split(key)
        actions = _random_actions(sub, batch)
        before = np.asarray(state.farm.money)
        is_night = bool(((int(np.asarray(state.step_index)[0]) + 1) % J.TURNS_PER_DAY) == 0)
        state, acct = _STEP_ACCT(state, actions)
        after = np.asarray(state.farm.money)
        if is_night:
            night_turns += 1
            named = (np.asarray(acct["trade"]) - np.asarray(acct["hire"])
                     - np.asarray(acct["land"]))
            np.testing.assert_array_equal(after - before, named,
                                          err_msg=f"night turn {turn} lost money to nothing")
    assert night_turns == 2, f"expected to cross two nights, crossed {night_turns}"
