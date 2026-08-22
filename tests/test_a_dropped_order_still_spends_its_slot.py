"""An invalid order does not shuffle the ones behind it forward. Position is the pairing key.

**Read from the reference, not from our comments about it.** `_process_market` truncates each
player's list POSITIONALLY and only then parses it:

    reference/kaggriculture.py:555   queues.append(q[:max_orders])
    reference/kaggriculture.py:568   ostate = _parse_order(q[i])
    reference/kaggriculture.py:643   if n <= 0: return None

So an order with a non-positive quantity becomes `None` **at the position it was written**. The slot
is spent. The order behind it does not move up.

Both of our simulators compacted instead: `e_present` tested validity, `cumsum` assigned slots, and
an invalid entry at position 3 pulled positions 4..10 down by one. The comment sitting on that code
in both files cited :534 truncating before parsing -- the right fact, the backwards consequence.

**Why position matters and a contents comparison cannot see it.** `_process_market` walks the two
players' lists BY SLOT: the i-th orders are quoted against each other and against the same
pre-commit inventory. Shifting our list up by one pairs our orders against different opponent orders
than the reference would, so a contested unit is priced differently -- and every order is still
individually present and correct, which is why nothing that compares order SETS reports anything.

**Unreachable from today's decode**, by two independent guards: `orders_from_heads` floors every
quantity at `max(1, ...)`, and `slot_tables` caps at `orders[:MAX_ORDERS]`. This pins the rule
anyway, because both guards are in quantity-handling code that is still being edited -- the
animal-repeat change produced a 12-order turn earlier this same week.

The default vector path is deliberately NOT changed. There a zero means "this product has no order",
an empty entry in a per-product vector rather than something the agent wrote, so compaction is
correct and is what the 719-step reference parity gate verifies.
"""

import numpy as np
import pytest

from kagg.sim.game import (
    MAX_ORDERS,
    ORDER_BUY_PRODUCT,
    ORDER_BUY_SEED,
    ORDER_HIRE,
    ORDER_NONE,
    ORDER_SELL,
    Actions,
    Game,
)


def book(rows):
    """`rows` is a list of (op, item, qty) written at consecutive positions, seat 0."""
    act = Actions(1, 2)
    for k, (op, item, qty) in enumerate(rows):
        act.order_op[0, 0, k] = op
        act.order_item[0, 0, k] = item
        act.order_qty[0, 0, k] = qty
    op, item, qty = Game._order_book(Game(1, weed_chance=0.0), act)
    return [(int(op[0, 0, k]), int(item[0, 0, k]), int(qty[0, 0, k])) for k in range(MAX_ORDERS)]


def jax_book(rows):
    jnp = pytest.importorskip("jax.numpy")
    from kagg.sim import jax_sim as JS

    act = Actions(1, 2)
    for k, (op, item, qty) in enumerate(rows):
        act.order_op[0, 0, k] = op
        act.order_item[0, 0, k] = item
        act.order_qty[0, 0, k] = qty
    jx = JS.Actions(
        **{f: jnp.zeros((1, 2, JS.MAX_UNITS), dtype=jnp.int32)
           for f in ("unit_op", "unit_crop", "unit_item", "unit_qty")},
        sell=jnp.zeros((1, 2, JS.N_PRODUCTS), dtype=jnp.int32),
        buy_seed=jnp.zeros((1, 2, JS.N_CROPS), dtype=jnp.int32),
        buy_product=jnp.zeros((1, 2, JS.N_PRODUCTS), dtype=jnp.int32),
        buy_animal=jnp.zeros((1, 2, JS.N_ANIMALS), dtype=jnp.int32),
        hire=jnp.zeros((1, 2), dtype=jnp.int32),
        buy_land=jnp.zeros((1, 2), dtype=bool),
        order_op=jnp.asarray(act.order_op, dtype=jnp.int32),
        order_item=jnp.asarray(act.order_item, dtype=jnp.int32),
        order_qty=jnp.asarray(act.order_qty, dtype=jnp.int32),
    )
    op, item, qty = JS._order_book(jx)
    op, item, qty = np.asarray(op), np.asarray(item), np.asarray(qty)
    return [(int(op[0, 0, k]), int(item[0, 0, k]), int(qty[0, 0, k])) for k in range(MAX_ORDERS)]


#: A hole at position 1. The reference parses `q[1]` to None and moves on to `q[2]` AS position 2.
WITH_A_HOLE = [(ORDER_SELL, 0, 5), (ORDER_BUY_SEED, 0, 0), (ORDER_BUY_PRODUCT, 0, 3),
               (ORDER_HIRE, 0, 1)]


def test_the_order_behind_a_dropped_one_keeps_its_position():
    got = book(WITH_A_HOLE)
    assert got[0][0] == ORDER_SELL
    assert got[1][0] == ORDER_NONE, (
        "the zero-quantity seed order must leave an empty slot: the reference spends position 1 on "
        "it (`_parse_order` returns None) and does not pull the order behind it forward")
    assert got[2][0] == ORDER_BUY_PRODUCT, (
        "compacted -- BUY_PRODUCT moved from position 2 to 1. `_process_market` pairs the two "
        "players' i-th orders, so this trades against a different opponent order than the "
        "reference would, at a different contested price")
    assert got[3][0] == ORDER_HIRE


def test_both_simulators_agree_about_the_hole():
    assert jax_book(WITH_A_HOLE) == book(WITH_A_HOLE)


def test_a_hire_with_no_quantity_still_takes_its_slot():
    """HIRE and BUY_LAND carry no quantity; a zero there is absence of a number, not an empty order."""
    got = book([(ORDER_HIRE, 0, 0), (ORDER_SELL, 0, 4)])
    assert got[0][0] == ORDER_HIRE and got[0][2] == 1
    assert got[1][0] == ORDER_SELL


def test_a_list_with_no_holes_is_unchanged():
    """The common case must be untouched: every live decode emits quantities floored at 1."""
    rows = [(ORDER_SELL, 2, 7), (ORDER_HIRE, 0, 1), (ORDER_BUY_SEED, 1, 3)]
    got = book(rows)
    assert got[:3] == [(ORDER_SELL, 2, 7), (ORDER_HIRE, 0, 1), (ORDER_BUY_SEED, 1, 3)]
    assert all(slot[0] == ORDER_NONE for slot in got[3:])
    assert jax_book(rows) == got


def test_the_default_vector_path_still_compacts():
    """The regression guard. Per-product vectors are sparse by nature and MUST compact.

    A zero in `sell` means "no wheat order", not "an order for zero wheat", so compaction there is
    correct and is what the reference parity gate verifies over 719 steps.
    """
    act = Actions(1, 2)
    act.sell[0, 0, 3] = 6          # a single order, in a high-numbered product slot
    op, _item, qty = Game._order_book(Game(1, weed_chance=0.0), act)
    assert int(op[0, 0, 0]) == ORDER_SELL, "the vector path must still pack into slot 0"
    assert int(qty[0, 0, 0]) == 6
