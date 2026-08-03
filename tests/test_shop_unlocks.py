"""Anything that trains or measures must run a real town drain, not a frozen market.

**The bug these pin.** `jax_sim.reset(unlock_schedule=None)` fills `unlock_day` with `NEVER`, and
`_drain` is `shops + centre` where `shops = (unlock_day <= day) @ SHOP_PULL`. Every RL and eval
entry point called `reset` without a schedule, so the shop term was zero for the whole season and
the town bought 140 wheat against the reference's 698 -- holding end-of-season wheat at $37 instead
of $51 and milk at $263 instead of $340.

**Why the tests target the callers and not `reset`'s default.** `_run_lockstep` passes
`unlock_schedule=None` to *both* simulators, so making `None` sample would desynchronise the parity
gate at construction. The default stays frozen and the callers move -- which means the guard has to
be on the callers, at the exact place the bug occurred. `parity.py` could never have caught this: it
passes the same schedule to both sims, so it proves jax-vs-numpy agreement given a schedule and says
nothing about whether the caller supplies one. Fourth instance of "a gate only tests what it
exercises".
"""

import numpy as np
import pytest

from kagg.economics import market as M
from kagg.sim import jax_sim as J
from kagg.sim import town as W

PRODUCTS = list(M.PRODUCTS)
WHEAT = PRODUCTS.index("WHEAT")

# The frozen-town and reference figures this bug was measured at, kept as guards so a change to
# SHOP_PULL or the centre schedule cannot quietly move the baseline these assertions rest on.
FROZEN_WHEAT_DRAIN = 140
REFERENCE_WHEAT_DRAIN = 698


def _season_drain(unlock_days):
    """Units the town removes over a full season, by walking `_drain`'s own rules on the host."""
    shop_pull = np.asarray(J.SHOP_PULL)
    centre_pull = np.asarray(J.CENTER_PULL)
    total = np.zeros(shop_pull.shape[1], dtype=np.int64)
    for step in range(J.TURNS_PER_DAY * 30):
        day = step // J.TURNS_PER_DAY
        if step % W.SHOP_INTERVAL == 0:
            total += (np.asarray(unlock_days) <= day).astype(np.int64) @ shop_pull
        if step % W.CENTER_INTERVAL == 0:
            mult = 1
            for threshold, m in J._CENTER_SCHEDULE:
                if day >= threshold:
                    mult = m
            total += mult * centre_pull
    return total


def _price_at_season_end(unlock_days, product):
    import jax.numpy as jnp
    i0 = np.array([M.I0[p] for p in PRODUCTS], dtype=np.int64)
    inv = i0 - _season_drain(unlock_days)
    idx = PRODUCTS.index(product)
    return int(np.asarray(J.price(jnp.asarray(inv, dtype=jnp.float32)[None, :]))[0][idx])


# ---- the baseline this was measured against -------------------------------------------------


def test_frozen_town_baseline_is_what_the_bug_was_measured_at():
    """Guard. If this moves, every figure quoted in the bug report is stale."""
    frozen = _season_drain(np.full(J.N_SHOPS, J.NEVER))
    assert frozen[WHEAT] == FROZEN_WHEAT_DRAIN
    assert _price_at_season_end(np.full(J.N_SHOPS, J.NEVER), "WHEAT") == 37


def test_reference_schedule_baseline():
    """One shop every three days, all eight open by day 24 -- the reference's own behaviour."""
    reference = np.array([J.SHOP_UNLOCK_INTERVAL * (k + 1) for k in range(J.N_SHOPS)])
    assert reference.max() == 24 < 30, "a shop must not unlock after the season ends"
    assert _season_drain(reference)[WHEAT] == REFERENCE_WHEAT_DRAIN
    assert _price_at_season_end(reference, "WHEAT") == 51


# ---- the sampler ---------------------------------------------------------------------------


def test_random_unlock_days_opens_every_shop_on_the_reference_cadence():
    """Every game gets the same *set* of unlock days -- one shop every three days -- in a random order."""
    unlock = np.asarray(J.random_unlock_days(16, seed=3))
    assert unlock.shape == (16, J.N_SHOPS)
    assert unlock.max() == 24 and unlock.min() == J.SHOP_UNLOCK_INTERVAL
    want = [J.SHOP_UNLOCK_INTERVAL * (k + 1) for k in range(J.N_SHOPS)]
    for game in unlock:
        assert sorted(game.tolist()) == want


def test_sampled_drain_varies_by_order_and_dwarfs_the_frozen_town():
    """**The total is NOT order-invariant, and that is faithful, not a defect.**

    Per-shop total pull runs 2-4 units, so giving an early day to a heavy shop drains more over the
    season. Measured over 400 sampled orders, wheat drain spans **500-770** (median 626) against the
    identity order's 698 and the frozen town's 140. The reference randomises the same way, so this
    spread is a property of the game rather than of the sampler.
    """
    unlock = np.asarray(J.random_unlock_days(64, seed=7))
    wheat = np.array([_season_drain(game)[WHEAT] for game in unlock])
    assert wheat.min() > 3 * FROZEN_WHEAT_DRAIN, "sampled drain is not far above a frozen town"
    assert 450 <= wheat.min() and wheat.max() <= 820, f"drain spread {wheat.min()}-{wheat.max()}"
    assert wheat.std() > 0, "order variation produced no spread at all"


def test_shop_order_varies_across_the_batch():
    """The order is the simulator's one seed-to-seed variation; a shared order is one market path."""
    unlock = np.asarray(J.random_unlock_days(64, seed=1))
    assert not np.all(unlock == unlock[0]), "every game in the batch has the same shop order"


def test_sampler_is_deterministic_in_its_seed():
    a = np.asarray(J.random_unlock_days(8, seed=5))
    b = np.asarray(J.random_unlock_days(8, seed=5))
    c = np.asarray(J.random_unlock_days(8, seed=6))
    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)


# ---- the default must stay frozen, or the parity gate desynchronises ------------------------


def test_plain_reset_default_is_unchanged():
    """`_run_lockstep` passes None to both sims. This default must not start sampling."""
    assert np.all(np.asarray(J.reset(2).unlock_day) == J.NEVER)
    assert np.all(np.asarray(J.reset(2, unlock_schedule={}).unlock_day) == J.NEVER)


def test_explicit_dict_schedule_is_unchanged():
    unlock = np.asarray(J.reset(2, unlock_schedule={3: 0, 6: 1, 9: 2}).unlock_day)
    assert (unlock[0, 0], unlock[0, 1], unlock[0, 2]) == (3, 6, 9)
    assert unlock[0, 3] == J.NEVER
    assert np.all(unlock[0] == unlock[1]), "an explicit dict stays shared across the batch"


def test_reset_accepts_a_per_game_array():
    """A dict cannot express "a different order per game", which is what the reference produces."""
    days = J.random_unlock_days(4, seed=2)
    state = J.reset(4, unlock_schedule=days)
    assert np.array_equal(np.asarray(state.unlock_day), np.asarray(days))
    with pytest.raises(ValueError, match="expected"):
        J.reset(4, unlock_schedule=np.zeros((3, J.N_SHOPS), dtype=np.int32))


def test_reset_with_shops_is_the_fixed_entry_point():
    state = J.reset_with_shops(8, seed=4)
    unlock = np.asarray(state.unlock_day)
    assert unlock.max() == 24, "shops must all open within the season"
    assert not np.all(unlock == unlock[0])
    assert _season_drain(unlock[0])[WHEAT] > 3 * FROZEN_WHEAT_DRAIN


@pytest.mark.parametrize("product,frozen,real",
                         [("WHEAT", 37, 51), ("STRAWBERRY", 219, 297), ("EGG", 58, 76),
                          ("MILK", 263, 340), ("TOMATO", 77, 98)])
def test_end_of_season_prices_the_frozen_town_understated(product, frozen, real):
    """The measured 27-38% understatement, pinned per product."""
    reference = np.array([J.SHOP_UNLOCK_INTERVAL * (k + 1) for k in range(J.N_SHOPS)])
    assert _price_at_season_end(np.full(J.N_SHOPS, J.NEVER), product) == frozen
    assert _price_at_season_end(reference, product) == real


# ---- the callers that were wrong ------------------------------------------------------------


def test_curriculum_day_zero_rung_drains():
    """`states_at_mix`'s day-0 rung is `J.reset(n)`, which was a frozen town."""
    from kagg.rl import curriculum

    state = curriculum.states_at_mix(4, {0: 1.0}, seed=0)
    unlock = np.asarray(state.unlock_day)
    assert not np.all(unlock == J.NEVER), "the day-0 rung trains in a frozen market"
    assert unlock.max() < 30


def test_chain_states_drains():
    """The synthetic chain rung is a fresh `J.reset` too, and P7 is about to deploy it."""
    from kagg.rl import curriculum

    unlock = np.asarray(curriculum.chain_states(4).unlock_day)
    assert not np.all(unlock == J.NEVER), "the chain rung trains in a frozen market"


def _load_trainer():
    import importlib.util
    import pathlib

    path = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "train_jax_rl.py"
    spec = importlib.util.spec_from_file_location("train_jax_rl_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_trainer_staggered_states_drain():
    """`staggered_states` builds the no-curriculum seed pool and every run's opening state."""
    unlock = np.asarray(_load_trainer().staggered_states(12, 4, seed=0).unlock_day)
    assert not np.all(unlock == J.NEVER), "the trainer's seed states train in a frozen market"
