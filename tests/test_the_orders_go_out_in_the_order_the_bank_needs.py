"""A turn's orders must leave in the order the environment settles them: SELL first.

**Why this exists.** Found by review, 2026-08-20, and it is the third instance this week of the
same disease -- code that runs, returns something plausible, and is wrong only where nothing looks.

`bundle_of` stores a turn's orders as a SORTED multiset (`market_bundles.py:59`), and the sort is
alphabetical on the op name:

    BUY_ANIMAL < BUY_LAND < BUY_PRODUCT < BUY_SEED < HIRE < SELL

`orders_from_heads` then walked that stored order and emitted it verbatim, so every SELL came LAST.

That matters because the environment does not settle a turn's orders simultaneously. It commits
them **in sequence** -- slot i takes its money before slot i+1 is quoted (`reference/kaggriculture.py`,
`_process_market`) -- and both of our simulators lay the slots out in the order an agent writes
them: sells, seeds, products, animals, HIRE, BUY_LAND (`game.py:70-77`, mirrored at
`jax_sim.py:_order_book`). `market_bundles`' own module docstring says why that order is the one the
teacher uses: the same turn's sells are what fund the ten hires.

So the two paths disagreed. `to_sim_actions` (jit, used by every sim-side evaluation) sold first;
`orders_from_heads` (used by `kagg/agents/neural.py`, the REAL environment) sold last. A student
replaying the teacher's exact bundle would have its hires and purchases refused on a thin bank --
and no sim-side number could show it, because the sim path was the correct one. It would appear
only in the real environment, which is precisely where DAgger rolls out and where the gate runs.

This test pins the emitted ORDER, not just the contents.
"""

import numpy as np
import pytest

from kagg.il import market_bundles as MB
from kagg.sim.market import ANIMALS, PRODUCTS
from kagg.sim.tiles import CROP_INDEX

CROPS = [c for c, _ in sorted(CROP_INDEX.items(), key=lambda kv: kv[1])]

#: The order an agent writes orders in, which is the order the environment gives them slots in.
#: `kagg/sim/game.py:70-77` defines it and `jax_sim._order_book` mirrors it.
CANONICAL = ["SELL", "BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "HIRE", "BUY_LAND"]


def decode(orders):
    vocab = MB.Vocabulary.from_bundles([MB.bundle_of([]), MB.bundle_of(orders)])
    qty_sell = np.zeros(len(PRODUCTS), dtype=np.int32)
    qty_bp = np.zeros(len(PRODUCTS), dtype=np.int32)
    qty_bs = np.zeros(len(CROPS), dtype=np.int32)
    for o in orders:
        n = int(o[2]) if len(o) > 2 else 1
        if o[0] == "SELL":
            qty_sell[PRODUCTS.index(o[1])] = n
        elif o[0] == "BUY_PRODUCT":
            qty_bp[PRODUCTS.index(o[1])] = n
        elif o[0] == "BUY_SEED":
            qty_bs[CROPS.index(o[1])] = n
    return MB.orders_from_heads(vocab, vocab.index(MB.bundle_of(orders)),
                                qty_sell, qty_bp, qty_bs, PRODUCTS, CROPS, ANIMALS)


def test_a_sell_is_emitted_before_the_hire_it_pays_for():
    """The teacher's own pattern: sell the shed, then hire ten hands with the proceeds.

    Alphabetically HIRE sorts before SELL, so the buggy decode emitted all ten hires first and the
    environment refused them on a bank that had not yet received the sale.
    """
    out = decode([["SELL", "WHEAT", 30]] + [["HIRE"]] * 10)
    ops = [o[0] for o in out]
    assert ops[0] == "SELL", (
        "emitted %r first. The environment commits slot i's money before quoting slot i+1, so a "
        "hire placed ahead of the sell that funds it is refused on a thin bank." % ops[0])
    assert ops.count("HIRE") == 10, "lost hires: %r" % ops


def test_every_op_kind_comes_out_in_the_canonical_slot_order():
    """One order of each kind. The emitted sequence must match `game.py`'s slot layout exactly."""
    out = decode([["BUY_LAND"], ["HIRE"], ["BUY_ANIMAL", "COW", 1],
                  ["BUY_SEED", "MELON", 2], ["BUY_PRODUCT", "WHEAT", 5], ["SELL", "MELON", 4]])
    ops = [o[0] for o in out]
    assert ops == CANONICAL, "emitted %r, canonical is %r" % (ops, CANONICAL)


def test_the_decoders_agree_on_order_for_every_bundle_in_the_live_vocabulary():
    """The property test whose absence let this ship.

    Three decoders must agree forever -- `to_sim_fields`, `orders_from_heads` and
    `to_sim_actions`. This checks the one thing a per-bundle contents comparison cannot see: that
    what `orders_from_heads` emits is non-decreasing in canonical slot rank.
    """
    vocab = MB.load_vocab()
    rank = {op: i for i, op in enumerate(CANONICAL)}
    qty = np.ones(len(PRODUCTS), dtype=np.int32)
    qty_bs = np.ones(len(CROPS), dtype=np.int32)

    bad = []
    for i in range(vocab.size):
        ranks = [rank[o[0]] for o in
                 MB.orders_from_heads(vocab, i, qty, qty, qty_bs, PRODUCTS, CROPS, ANIMALS)]
        if ranks != sorted(ranks):
            bad.append((i, vocab.bundle(i)))
    assert not bad, "%d of %d bundles decode out of slot order, e.g. %r" % (
        len(bad), vocab.size, bad[:3])


def test_the_ten_order_cap_keeps_the_sells():
    """`maxMarketOrdersPerTurn` is 10 and the environment DROPS the rest.

    With sells last, a bundle of eleven orders lost its sell and kept ten hires -- the exact
    inversion of what the turn was for. Sells first means the cut falls on the purchases instead,
    which is the survivable half.
    """
    out = decode([["SELL", "WHEAT", 12]] + [["HIRE"]] * 10)
    assert len(out) == 11, "decoder should emit all 11; the environment does the truncating"
    assert out[0][0] == "SELL", "the order that survives truncation must be the sell"
