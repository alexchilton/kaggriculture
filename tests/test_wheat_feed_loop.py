"""The farm must be able to feed its own animals, not sell wheat and buy it back.

This is the fertilizer bug mirrored, and Alex spotted the pattern before I did:

    fertilizer:  pens SELL it,  crops BUY it   -> the farm pays the spread twice
    wheat:       crops SELL it, pens BUY it    -> the farm pays the spread twice

Identical structure, opposite direction. The fertilizer side got a gene on 2026-08-05; wheat did not,
because nothing looked at it.

Every piece already exists and none of them are connected:

* `ranch()` FEEDs 30 times a season and PICKUPs wheat 31 times -- and orders all 30 units from the
  market, unconditionally.
* `grow(sell=False)` keeps its harvest in the shed rather than selling it.
* `ops.pickup()` takes from the shed **by item index, not by origin**, so a pen will happily eat wheat
  the farm grew.

So the wheat -> animal -> fertilizer loop that `production.py:53` calls "the main structural reason to
keep animals" is expressible today and no genome can reach it, because `decode()` always leaves
`grow(sell=True)` and `ranch()` has no way to stop buying.

The size of it: five pens buy 120 wheat at $25 = **$3,000 a season**, while one 4-tile wheat block
yields 112 units -- enough for roughly four pens -- and `grow()` currently dumps those 112 onto the
market, walking our own wheat price from $25 down to $21 while the pens buy at the top of it.

Whether the loop beats buying is for the search to decide, not for this test. What it asserts is that
the option exists and that turning it on cannot starve the herd, which is the one failure mode that
matters: `consecutive_unfed >= 2` escapes the animal for a deterministic $300-$500 loss.
"""

import numpy as np
import pytest

from kagg.search import chains as C
from kagg.search import routines as R

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
          "buy_product", "buy_animal", "hire", "buy_land")
WHEAT = R.PRODUCTS.index("WHEAT")
NW_BLOCK = [b for b in C.BLOCKS if C.land_cost(b[0]) == 0][0]


def _run(script, seed=0):
    import jax.numpy as jnp
    from kagg.sim import jax_sim as J

    state = J.reset_with_shops(1, seed=seed)
    arrs = script.arrays()
    for t in range(script.T):
        acts = {f: jnp.asarray(np.stack([np.asarray(arrs[f][t]),
                                         np.zeros_like(np.asarray(arrs[f][t]))])[None])
                for f in FIELDS}
        state = J.step(state, J.Actions(**acts), weed_chance=0.0)
    return state


def test_the_premise_a_pen_eats_wheat_it_did_not_buy():
    """`pickup` is source-agnostic, which is what makes the whole loop possible."""
    import inspect
    from kagg.sim import ops as O

    assert "shed[games, item]" in inspect.getsource(O.pickup)


def test_a_pen_can_be_told_not_to_buy_its_feed():
    """The switch itself. Without it no genome can ever run the loop."""
    s = R.ranch(R.Script(), "COW", R.SPAWN, start_day=0, land_day=0, buy_feed=False)
    assert int(np.asarray(s.buy_product)[:, WHEAT].sum()) == 0, \
        "the pen still orders wheat from the market"
    ops = [R.OP_NAMES[int(o)] for o in np.asarray(s.unit_op)[:, 0]]
    assert ops.count("FEED") > 25, "it must still feed every day -- just from the shed"
    assert ops.count("PICKUP") > 25, "and still draw the wheat it feeds"


def test_a_pen_that_buys_its_feed_is_unchanged():
    """The default must not move; every animal measurement in the project used it."""
    s = R.ranch(R.Script(), "COW", R.SPAWN, start_day=0, land_day=0)
    assert int(np.asarray(s.buy_product)[:, WHEAT].sum()) == 30


def test_a_wheat_chain_can_hold_its_harvest_for_the_herd():
    s = R.grow(R.Script(), "WHEAT", list(NW_BLOCK), plant_day=0, unit=1, sell=False)
    assert int(np.asarray(s.sell)[:, WHEAT].sum()) == 0


def test_the_loop_actually_feeds_the_animals():
    """The one failure that matters. `consecutive_unfed >= 2` escapes the animal, so a herd relying on
    grown wheat must still have wheat in the shed on every feeding day."""
    s = R.Script()
    R.grow(s, "WHEAT", list(NW_BLOCK), plant_day=0, unit=1, sell=False)
    R.ranch(s, "COW", R.SPAWN, start_day=4, land_day=0, buy_feed=False)
    state = _run(s)
    from kagg.sim import jax_sim as J
    alive = int((np.asarray(state.tiles.animal)[0, 0] != J.NO_ANIMAL).sum())
    assert alive == 1, "the cow starved on grown wheat; the loop does not close"


def test_the_genome_can_express_the_loop():
    """`decode()` must reach it, which is the whole point -- `grow(sell=...)` has existed all along
    and no genome could ever set it."""
    g = np.zeros((8, len(C.GENES)), dtype=np.int64)
    g[0] = (C.KINDS.index("grow"), R.CROPS.index("WHEAT"),
            next(i for i, b in enumerate(C.BLOCKS) if b == NW_BLOCK),
            C.START_DAY_CHOICES.index(0), C.LAND_DAY_CHOICES.index(0), 0, 0, 0)
    g[1] = (C.KINDS.index("ranch"), R.ANIMAL_NAMES.index("COW"),
            C.RANCH_TILES.index(R.SPAWN), C.START_DAY_CHOICES.index(4),
            C.LAND_DAY_CHOICES.index(0), 0, 0, 0)
    # `feed_loop` on: the wheat chain holds its harvest and the pen eats out of the shed.
    g[0, C.GENES.index("feed_loop")] = 1
    g[1, C.GENES.index("feed_loop")] = 1
    script, _used, skipped = C.decode(g.reshape(-1), 8)
    assert skipped == 0
    assert int(np.asarray(script.buy_product)[:, WHEAT].sum()) == 0, "the pen still buys feed"
    assert int(np.asarray(script.sell)[:, WHEAT].sum()) == 0, "the wheat chain still sells its crop"


def test_the_loop_is_off_by_default_in_the_genome():
    """A zero genome must decode to the behaviour every prior measurement was taken against."""
    g = np.zeros((8, len(C.GENES)), dtype=np.int64)
    g[1] = (C.KINDS.index("ranch"), R.ANIMAL_NAMES.index("COW"),
            C.RANCH_TILES.index(R.SPAWN), C.START_DAY_CHOICES.index(0),
            C.LAND_DAY_CHOICES.index(0), 0, 0, 0)
    script, _used, _skipped = C.decode(g.reshape(-1), 8)
    assert int(np.asarray(script.buy_product)[:, WHEAT].sum()) == 30


def test_only_wheat_can_hold_its_harvest():
    """A melon chain refusing to sell would simply never earn. The loop is about feed, so it applies
    to the crop the animals eat and to no other."""
    g = np.zeros((8, len(C.GENES)), dtype=np.int64)
    melon_block = next(i for i, b in enumerate(C.BLOCKS) if C.land_cost(b[0]) == 0)
    g[0] = (C.KINDS.index("grow"), R.CROPS.index("MELON"), melon_block,
            C.START_DAY_CHOICES.index(2), C.LAND_DAY_CHOICES.index(0), 0, 0, 0)
    g[0, C.GENES.index("feed_loop")] = 1
    script, _used, _skipped = C.decode(g.reshape(-1), 8)
    melon = R.PRODUCTS.index("MELON")
    assert int(np.asarray(script.sell)[:, melon].sum()) > 0, \
        "feed_loop must not stop a melon chain from selling melon"
