"""A quantity the teacher traded must come back out of the decode as the SAME number.

**Why this exists.** `SELL_BUCKETS = [0,1,3,10,30]` and `BUY_BUCKETS = [0,1,2,5]` were written
down, never measured. Measured against 20,000 turns per shard of the teacher's own play
(`scripts/measure_quantity_ladders.py`, 2026-08-20):

    SELL         70,411 orders  max 68   mean projection error 27.2%
    BUY_PRODUCT  ~18,000 orders max 134  mean projection error 35.3%
    BUY_SEED     28,123 orders  max 23   mean projection error 16.5%

The distribution is near-continuous -- SELL uses every value from 1 to 24 with no gaps and no
clustering on the rungs -- so the ladder is not a coarse view of a peaky distribution, it is a
lossy encoding of a flat one. `SELL WHEAT 18` (2,983 orders) projects onto 30, a 67% overshoot,
and `BUY_SEED CARROT 8` projects onto 5.

That error is a FLOOR. It is not reachable by training, it is not visible in a falling loss, and
imitation is the one setting where it is pure loss: the teacher's number is known exactly.

So the label path and the decode path must agree on the exact integer, and this test pins that.
"""

import numpy as np
import pytest

from kagg.il import market_bundles as MB
from kagg.rl import jax_policy as P
from kagg.sim.market import ANIMALS, PRODUCTS
from kagg.sim.tiles import CROP_INDEX

CROPS = [c for c, _ in sorted(CROP_INDEX.items(), key=lambda kv: kv[1])]

# Quantities the teacher actually traded, taken from the histogram above. 18 and 12 are the two
# that the old SELL ladder mangled worst while being common (2,983 and 3,867 orders).
TEACHER_SELL_QUANTITIES = [1, 2, 4, 6, 12, 18, 24, 63]
TEACHER_SEED_QUANTITIES = [1, 3, 7, 8, 11, 12, 23]


def decode_one(orders, qty_sell, qty_bp, qty_bs):
    """Run an order list through the vocabulary and back out of `orders_from_heads`."""
    vocab = MB.Vocabulary.from_bundles([MB.bundle_of([]), MB.bundle_of(orders)])
    return MB.orders_from_heads(
        vocab, vocab.index(MB.bundle_of(orders)),
        qty_sell, qty_bp, qty_bs, PRODUCTS, CROPS, ANIMALS)


@pytest.mark.parametrize("n", TEACHER_SELL_QUANTITIES)
def test_a_sell_quantity_comes_back_exactly(n):
    """Not 'close to n'. n. The teacher's number is known, so any error here is self-inflicted."""
    qty_sell = np.zeros(len(PRODUCTS), dtype=np.int32)
    qty_sell[PRODUCTS.index("WHEAT")] = n
    out = decode_one([["SELL", "WHEAT", n]], qty_sell,
                     np.zeros(len(PRODUCTS), dtype=np.int32), np.zeros(len(CROPS), dtype=np.int32))
    assert out == [["SELL", "WHEAT", n]], (
        "decoded %r for a teacher SELL of %d -- the head cannot express the number it was "
        "trained on" % (out, n))


@pytest.mark.parametrize("n", TEACHER_SEED_QUANTITIES)
def test_a_seed_purchase_comes_back_exactly(n):
    """`BUY_SEED CARROT 8` is the order Fable named; it projected onto 5 on the old ladder."""
    qty_bs = np.zeros(len(CROPS), dtype=np.int32)
    qty_bs[CROPS.index("CARROT")] = n
    out = decode_one([["BUY_SEED", "CARROT", n]], np.zeros(len(PRODUCTS), dtype=np.int32),
                     np.zeros(len(PRODUCTS), dtype=np.int32), qty_bs)
    assert out == [["BUY_SEED", "CARROT", n]], (
        "decoded %r for a teacher BUY_SEED of %d" % (out, n))


def test_the_head_is_wide_enough_for_what_the_teacher_trades():
    """A cap of 64 covers 99.79% of SELL and 97.50% of BUY_PRODUCT (measured, same run).

    Pinned so that narrowing the head is a test failure rather than a silent loss of the large
    late-season sells, which are where the money is.
    """
    assert P.MAX_QTY >= 64, "quantity head narrowed to %d; the teacher sells up to 68" % P.MAX_QTY


def test_a_quantity_above_the_cap_clamps_rather_than_wraps():
    """The teacher's largest BUY_PRODUCT is 134. A wrap would decode 134 as 6.

    Clamping understates. Wrapping is a different order entirely, and an index that lands outside a
    head is silently clamped by JAX under jit rather than raised, so this must be handled at the
    label end where it is still ordinary Python.
    """
    assert MB.clamp_qty(134) == P.MAX_QTY - 1
    assert MB.clamp_qty(0) == 0
    assert MB.clamp_qty(18) == 18


def test_a_selected_product_never_decodes_as_zero():
    """The bundle named the product; a zero quantity would contradict it and emit a dead order.

    Same floor-at-one rule as `to_sim_fields` and `jax_act.to_sim_actions`. All three must agree or
    the policy plays differently depending on which decoder ran.
    """
    out = decode_one([["SELL", "WHEAT", 4]], np.zeros(len(PRODUCTS), dtype=np.int32),
                     np.zeros(len(PRODUCTS), dtype=np.int32), np.zeros(len(CROPS), dtype=np.int32))
    assert out == [["SELL", "WHEAT", 1]], "decoded %r; a named product must sell at least one" % out
