"""End to end: sample the bundle head and check the simulator receives what was drawn.

The old market path could pass every unit test and still emit nothing, because the failure lived in
the composition -- six calibrated marginals decoding to "never trade". So this test does not check a
head in isolation. It samples, decodes, and reads the `jax_sim.Actions` the simulator would consume.

The specific regression it pins: `hire` arriving as a COUNT. `jax_act.to_sim_actions` used to do
`u("hire").astype(bool)` against a field `jax_sim.py:258` documents as "COUNT of hands to hire this
turn, not a flag", capping every learned policy at one hand per turn.
"""

import jax
import jax.numpy as jnp

from kagg.il import market_bundles as MB
from kagg.rl import jax_act as A


def _vocab():
    return MB.Vocabulary.from_bundles([
        MB.bundle_of([]),
        MB.bundle_of([["HIRE"]] * 10),
        MB.bundle_of([["SELL", "WHEAT", 4]]),
        MB.bundle_of([["BUY_SEED", "WHEAT", 2], ["HIRE"], ["HIRE"]]),
    ])


def _jnp_tables(vocab):
    return {k: jnp.asarray(v) for k, v in MB.tables(vocab).items()}


def test_a_bundle_of_ten_hires_reaches_the_sim_as_ten():
    vocab = _vocab()
    tables = _jnp_tables(vocab)
    ten = vocab.index(MB.bundle_of([["HIRE"]] * 10))

    batch = 1
    actions = {
        "op": jnp.zeros((batch * 2, 13), dtype=jnp.int32),
        "crop": jnp.zeros((batch * 2, 13), dtype=jnp.int32),
        "item": jnp.zeros((batch * 2, 13), dtype=jnp.int32),
        "qty": jnp.zeros((batch * 2, 13), dtype=jnp.int32),
        "bundle": jnp.full((batch * 2,), ten, dtype=jnp.int32),
        "qty_sell": jnp.zeros((batch * 2, 9), dtype=jnp.int32),
        "qty_buy_product": jnp.zeros((batch * 2, 9), dtype=jnp.int32),
        "qty_buy_seed": jnp.zeros((batch * 2, 5), dtype=jnp.int32),
    }
    sim = A.to_sim_actions(actions, batch, tables)
    assert int(sim.hire[0, 0]) == 10, "the hire COUNT must survive the decode"
    assert sim.hire.dtype != jnp.bool_, "hire is a count, never a flag"


def test_the_empty_bundle_emits_no_orders():
    """78.7% of teacher turns. It must decode to silence, not to a stray order."""
    vocab = _vocab()
    tables = _jnp_tables(vocab)
    batch = 1
    actions = {
        "op": jnp.zeros((batch * 2, 13), dtype=jnp.int32),
        "crop": jnp.zeros((batch * 2, 13), dtype=jnp.int32),
        "item": jnp.zeros((batch * 2, 13), dtype=jnp.int32),
        "qty": jnp.zeros((batch * 2, 13), dtype=jnp.int32),
        "bundle": jnp.zeros((batch * 2,), dtype=jnp.int32),
        # Deliberately non-zero: a quantity for a product the bundle never selected must be ignored.
        "qty_sell": jnp.full((batch * 2, 9), 3, dtype=jnp.int32),
        "qty_buy_product": jnp.full((batch * 2, 9), 2, dtype=jnp.int32),
        "qty_buy_seed": jnp.full((batch * 2, 5), 2, dtype=jnp.int32),
    }
    sim = A.to_sim_actions(actions, batch, tables)
    assert int(sim.sell.sum()) == 0
    assert int(sim.buy_product.sum()) == 0
    assert int(sim.buy_seed.sum()) == 0
    assert int(sim.hire.sum()) == 0


def test_a_selected_product_always_moves_at_least_one_unit():
    """Bucket 0 means "do nothing". If the bundle selected the product, that is a contradiction, and
    the bundle is the decision carrying the coordination -- so it floors at one."""
    vocab = _vocab()
    tables = _jnp_tables(vocab)
    sell_wheat = vocab.index(MB.bundle_of([["SELL", "WHEAT", 4]]))
    batch = 1
    actions = {
        "op": jnp.zeros((batch * 2, 13), dtype=jnp.int32),
        "crop": jnp.zeros((batch * 2, 13), dtype=jnp.int32),
        "item": jnp.zeros((batch * 2, 13), dtype=jnp.int32),
        "qty": jnp.zeros((batch * 2, 13), dtype=jnp.int32),
        "bundle": jnp.full((batch * 2,), sell_wheat, dtype=jnp.int32),
        "qty_sell": jnp.zeros((batch * 2, 9), dtype=jnp.int32),   # bucket 0 == "do nothing"
        "qty_buy_product": jnp.zeros((batch * 2, 9), dtype=jnp.int32),
        "qty_buy_seed": jnp.zeros((batch * 2, 5), dtype=jnp.int32),
    }
    sim = A.to_sim_actions(actions, batch, tables)
    assert int(sim.sell.sum()) >= 1


def test_the_head_names_match_what_the_policy_emits():
    """A head list and a network that disagree fail at the first forward pass, loudly -- but only if
    something checks. `ALL_HEADS` is what every loss and decoder iterates."""
    assert set(A.MARKET_HEADS) == {"bundle", "qty_sell", "qty_buy_product", "qty_buy_seed"}
    assert "trade" not in A.ALL_HEADS
    assert A.CONDITION_HEADS == ("op",)
