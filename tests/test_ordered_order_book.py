"""A turn's market orders must be expressible in their recorded slot order, not just as totals.

`Actions` carries one quantity per product per turn, and `_order_book` lays those out in a fixed
canonical sequence -- sells, seeds, products, animals, HIRE, BUY_LAND. That is what every agent in this
project emits, so it was sufficient until we tried to replay a real tape.

**The measurement that makes this necessary** (`data/logs/replay_tape_day0.log`): driving the winner's
own day-0 actions for both seats through `kagg.sim` reproduces money, crew, pens and animals
**dollar- and count-exact for turns 0 through 10**, then diverges by $32 at turn 11. Turn 11 of
episode 89873723 seat 0 is:

    [["SELL", "WHEAT", 1], ["BUY_PRODUCT", "WHEAT", 2], ["SELL", "WHEAT", 2]]

Two sells straddling a buy of the same product. Per-product totals collapse that to `SELL 3` then
`BUY 2`, and `_process_market` walks slots in order: SELL raises inventory, `BUY_PRODUCT` quotes at
`inventory - 1`, so moving both sells ahead of the buy reprices it. Against the reference,
`tests/test_split_sell_orders.py` measures $58 for the recorded order against $33 for the merged one.

Note this is *not* the same as splitting a sell for its own sake -- any partition of one SELL settles
identically, which the sibling test file pins. It is specifically interleaving a buy of the same
product that order matters for.

So `Actions` gains an optional explicit order list. When supplied it is used verbatim; when absent the
canonical compaction is unchanged, which is what keeps every existing agent and the parity gate intact.
"""

import numpy as np
import pytest

from kagg.sim.game import (
    MAX_ORDERS,
    ORDER_BUY_PRODUCT,
    ORDER_SELL,
    Actions,
    Game,
)
from kagg.sim.market import PRODUCTS

WHEAT = PRODUCTS.index("WHEAT")


def _game(money=8.0, wheat=19):
    game = Game(1, starting_money=money, weed_chance=0.0, rng=np.random.default_rng(0))
    for seat in range(2):
        game.farms[seat].shed[:, WHEAT] = wheat
    return game


def test_actions_exposes_an_explicit_order_list():
    """The interface itself, so a caller can tell whether the feature is present."""
    actions = Actions(1)
    assert hasattr(actions, "order_op"), "Actions has no explicit order-list field"
    assert actions.order_op.shape == (1, 2, MAX_ORDERS)
    assert actions.order_item.shape == (1, 2, MAX_ORDERS)
    assert actions.order_qty.shape == (1, 2, MAX_ORDERS)
    # Empty by default, so existing callers keep the canonical compaction.
    assert not actions.order_op.any()


def test_the_recorded_slot_order_is_preserved():
    """**The bug.** SELL 1 / BUY 2 / SELL 2 must not settle as SELL 3 / BUY 2."""
    straddled = _game()
    a = Actions(1)
    for seat in range(2):
        a.order_op[0, seat, :3] = [ORDER_SELL, ORDER_BUY_PRODUCT, ORDER_SELL]
        a.order_item[0, seat, :3] = [WHEAT, WHEAT, WHEAT]
        a.order_qty[0, seat, :3] = [1, 2, 2]
    straddled.step(a)

    merged = _game()
    b = Actions(1)
    for seat in range(2):
        b.sell[0, seat, WHEAT] = 3
        b.buy_product[0, seat, WHEAT] = 2
    merged.step(b)

    got = float(straddled.farms[0].money[0])
    collapsed = float(merged.farms[0].money[0])
    assert got != collapsed, (
        "the explicit order list settled identically to the merged form, so slot order is still "
        "being ignored")
    assert got == pytest.approx(58.0, abs=0.5), (
        f"recorded order should bank $58 as the reference does; got ${got:,.2f} "
        f"(merged form banks ${collapsed:,.2f})")


def test_the_canonical_compaction_is_unchanged_when_no_list_is_given():
    """Every existing agent supplies per-product totals only, and must behave exactly as before."""
    with_totals = _game()
    a = Actions(1)
    for seat in range(2):
        a.sell[0, seat, WHEAT] = 3
        a.buy_product[0, seat, WHEAT] = 2
    with_totals.step(a)

    explicit = _game()
    b = Actions(1)
    for seat in range(2):
        b.order_op[0, seat, :2] = [ORDER_SELL, ORDER_BUY_PRODUCT]
        b.order_item[0, seat, :2] = [WHEAT, WHEAT]
        b.order_qty[0, seat, :2] = [3, 2]
    explicit.step(b)

    assert float(with_totals.farms[0].money[0]) == pytest.approx(
        float(explicit.farms[0].money[0]), abs=0.01), (
        "spelling the canonical order out explicitly must give the canonical result")


def test_a_zero_quantity_slot_is_dropped_not_spent():
    """`_parse_order` rejects qty <= 0, and a dropped order must not shift the ones after it.

    The reference truncates positionally *before* parsing (`reference/kaggriculture.py:534`), so a
    caller must not be able to pad. Zero-quantity entries are therefore compacted out of the explicit
    list too, matching `present = c_qty > 0`.
    """
    game = _game()
    a = Actions(1)
    for seat in range(2):
        a.order_op[0, seat, :4] = [ORDER_SELL, ORDER_SELL, ORDER_BUY_PRODUCT, ORDER_SELL]
        a.order_item[0, seat, :4] = [WHEAT, WHEAT, WHEAT, WHEAT]
        a.order_qty[0, seat, :4] = [1, 0, 2, 2]      # the zero must vanish, not occupy a slot
    game.step(a)

    reference_equivalent = _game()
    b = Actions(1)
    for seat in range(2):
        b.order_op[0, seat, :3] = [ORDER_SELL, ORDER_BUY_PRODUCT, ORDER_SELL]
        b.order_item[0, seat, :3] = [WHEAT, WHEAT, WHEAT]
        b.order_qty[0, seat, :3] = [1, 2, 2]
    reference_equivalent.step(b)

    assert float(game.farms[0].money[0]) == pytest.approx(
        float(reference_equivalent.farms[0].money[0]), abs=0.01)
