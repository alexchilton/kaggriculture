"""Feed must be ordered against the herd the plan *intends*, not the herd already standing on tiles.

One theory, one test. The theory, read off `data/logs/diverge_by_day_147k.log` -- where the `wheat`
column is 0 on all thirty days while 14 animals escape and the season ends on $0:

    executor.py:390    herd_size  = (view.animal >= 0).sum(axis=1)
    executor.py:391    want_wheat = np.where(herd_size > 0, plan.feed_wheat * max(herd_size, 1), 0)

`herd_size` counts animals **already placed on a tile**. Not `plan.herd`, and not
`view.shed_animals`. So on turn 0 of day 0 nothing is placed, `want_wheat` is 0, no wheat is ordered
and `fetch_wheat` is gated off -- while the *same turn* spends the opening stake on animals. By the
time an animal is standing on a pen and `want_wheat` finally goes positive, there is no money left.

That is the same self-closing loop as `jax_masks.py:93` -- `masks[O.FEED] = has_animal & ~fed &
carrying_wheat` -- reappearing one layer up in the decoder: you cannot buy feed until you own an
animal, and buying the animal is what consumes the money for the feed. An animal bought without feed
escapes at `consecutive_unfed >= 2` and loses its full purchase price, so ordering them in this
sequence is strictly worse than not buying the animal at all.

Reference point for what the plan is trying to reproduce: the $147,178 seat (episode 89873723 seat 0)
holds 4 animals from day 0 and buys 967 units of wheat across the season.
"""

import numpy as np
import pytest

from kagg.search import executor as X
from kagg.search import plan as P
from kagg.sim.tiles import EMPTY, PASTURE

COW = P.ANIMAL_NAMES.index("COW")


def _opening_view(n_pens=6, money=3000.0):
    """Turn 0 of day 0: pens standing, nothing placed, nothing in the shed, full stake in hand."""
    tiles = 100
    kind = np.full((1, tiles), EMPTY, dtype=np.int64)
    kind[0, :n_pens] = PASTURE
    return X.View(
        day=0,
        hour=0,
        kind=kind,
        crop=np.full((1, tiles), -1, dtype=np.int64),
        planted_day=np.zeros((1, tiles), dtype=np.int64),
        watered=np.zeros((1, tiles), dtype=bool),
        yield_units=np.zeros((1, tiles), dtype=np.int64),
        unit_ord=np.zeros((1, X.MAX_EXEC_UNITS), dtype=np.int64),
        n_units=np.array([1]),
        money=np.array([money]),
        seeds=np.zeros((1, P.N_CROPS), dtype=np.int64),
        shed=np.zeros((1, P.N_CROPS), dtype=np.int64),
        prices=np.zeros((1, P.N_CROPS), dtype=np.int64),
        n_land=np.array([0]),
    )


def _plan_wanting_a_herd(n_pens=6, feed=2, herd=4):
    """A minimal genome: pens on the first tiles, a COW target, stocking from day 0."""
    g = np.zeros(P.N_GENES, dtype=np.int64)
    lo, _ = P.gene_slice("crop_of")
    g[lo:lo + n_pens] = P.CROP_GENE_PASTURE
    a, _ = P.gene_slice("herd")
    g[a + COW] = P.herd_gene(herd)
    lo, _ = P.gene_slice("stock_day")
    g[lo] = int(np.argmin(np.abs(P.STOCK_DAYS - 0)))
    lo, _ = P.gene_slice("feed_wheat")
    g[lo] = int(np.argmin(np.abs(P.FEED_WHEAT - feed)))
    return P.decode(g[None])


def test_feed_is_ordered_on_the_same_turn_the_first_animal_is():
    """The animal and its feed are one chain. A turn that buys the one must order the other."""
    plan = _plan_wanting_a_herd()
    d = X.decide(_opening_view(), plan)

    animals = int(d.buy_animal.sum())
    wheat = int(d.buy_product[0, X.WHEAT_ITEM])
    assert animals > 0, "the plan asks for a herd from day 0, so animals must be ordered"
    assert wheat > 0, (
        f"turn 0 orders {animals} animal(s) and {wheat} wheat. Feed must be ordered against the "
        f"herd the plan intends, not the herd already standing on a tile -- an animal bought with no "
        f"feed escapes at consecutive_unfed >= 2 and loses its whole purchase price.")


def test_the_feed_order_covers_the_intended_herd_not_the_placed_one():
    """`feed_wheat` is units per animal, so the order must scale with the target, not with zero."""
    plan = _plan_wanting_a_herd(feed=2, herd=4)
    d = X.decide(_opening_view(), plan)
    want = int(plan.feed_wheat[0]) * int(plan.herd[0].sum())
    assert int(d.buy_product[0, X.WHEAT_ITEM]) >= want, (
        f"ordered {int(d.buy_product[0, X.WHEAT_ITEM])} wheat for a target herd of "
        f"{int(plan.herd[0].sum())} at {int(plan.feed_wheat[0])} units each -- {want} needed")


def test_feed_outranks_the_marginal_animal_when_cash_is_short():
    """On a stake that cannot cover both, feed wins: a starved animal is worth less than no animal.

    $700 buys one COW and its feed, or two COWs and nothing to give them. The second COW is a
    guaranteed loss of its purchase price, so the decoder must not order it.
    """
    plan = _plan_wanting_a_herd(feed=2, herd=4)
    d = X.decide(_opening_view(money=700.0), plan)
    animals = int(d.buy_animal.sum())
    wheat = int(d.buy_product[0, X.WHEAT_ITEM])
    assert wheat >= 2 * animals or animals == 0, (
        f"on $700 the decoder ordered {animals} animal(s) with {wheat} wheat; it must not own more "
        f"animals than it has bought feed for")
