"""The executor must not buy livestock it cannot feed.

**The measurement this file exists for.** `docs/executor_livestock_broken_2026-08-04.md` ran the
leaders' own allocation -- `P.leaders_genome()`, 14 pastures, COW 8 / SHEEP 6, `feed_wheat=2` -- through
`X.decide` against all three hand-written opponents and banked **$0** in all three, losing 3/3 against
opponents banking $31,777 / $4,762 / $3,633.

Per game it ordered **29 animals** against a specified herd of 14, and **15** units of wheat against the
leaders' **967**. Live animals over the season went `1.0 -> 0.0 -> 0.0 -> 3.0 -> 1.7 -> 0.0`.

That is not three independent bugs, it is one cycle, and every arrow is a line of code in `decide`:

    stocking = day >= plan.stock_day            # true from day 0 for the WHOLE season
      -> the $3,000 stake is spent on animals
      -> money hits 0
      -> wheat_budget = (money - seed_reserve) / WHEAT_PRICE_CAP  ->  0, so no feed is ordered
      -> jax_sim escapes the animal at consecutive_unfed >= 2, taking the purchase price
      -> herd_size = (view.animal >= 0).sum()  ->  0, so want_wheat -> 0
         (now feed would not be ordered even if the money came back)
      -> placed = (view.animal == a).sum() + shed_animals  drops as they die
      -> room = herd - placed  reopens  ->  RE-BUYS  ->  back to the top

The economically correct condition is the one the existing suite states in prose and never asserts:
"a plan that buys and does not feed is strictly worse than one that never buys". An animal is only
worth its purchase price if the feed to keep it alive is also affordable. These tests assert that.

Reference costs: COW $400, SHEEP $500, GOOSE $300; wheat is budgeted at `WHEAT_PRICE_CAP` $60.
"""

import numpy as np
import pytest

from kagg.search import executor as X
from kagg.search import plan as P

pytest.importorskip("kagg.search.executor")

TILES = X.TILES
STAKE = 3_000.0          # what every game actually starts with


def _plan(**over):
    g = np.zeros(P.N_GENES, dtype=np.int64)
    for name, values in over.items():
        lo, hi = P.gene_slice(name)
        g[lo:hi] = values
    return P.decode(g)


def _kinds(mapping):
    k = np.full((1, TILES), X.EMPTY, dtype=np.int64)
    for ord_, kind in mapping.items():
        k[0, ord_] = kind
    return k


def _view(day=10, hour=0, n_units=2, unit_at=None, **over):
    base = dict(
        day=day, hour=hour,
        kind=np.full((1, TILES), X.EMPTY, dtype=np.int64),
        crop=np.full((1, TILES), -1, dtype=np.int64),
        planted_day=np.zeros((1, TILES), dtype=np.int64),
        watered=np.zeros((1, TILES), dtype=bool),
        yield_units=np.zeros((1, TILES), dtype=np.int64),
        unit_ord=np.full((1, X.MAX_EXEC_UNITS),
                         int(X.SHED_ORDS[0]) if unit_at is None else int(unit_at), dtype=np.int64),
        n_units=np.array([n_units]),
        money=np.array([20_000.0]),
        seeds=np.zeros((1, P.N_CROPS), dtype=np.int64),
        shed=np.zeros((1, P.N_CROPS), dtype=np.int64),
        prices=np.full((1, P.N_CROPS), 100, dtype=np.int64),
        n_land=np.array([0]),
        animal=np.full((1, TILES), -1, dtype=np.int64),
        fed_today=np.zeros((1, TILES), dtype=bool),
        cared_today=np.zeros((1, TILES), dtype=bool),
        consecutive_unfed=np.zeros((1, TILES), dtype=np.int64),
        fertilizer_available=np.zeros((1, TILES), dtype=bool),
        shed_animals=np.zeros((1, P.N_ANIMALS), dtype=np.int64),
        shed_wheat=np.array([0]),
        carried_wheat=np.zeros((1, X.MAX_EXEC_UNITS), dtype=np.int64),
        carried_animal=np.full((1, X.MAX_EXEC_UNITS), -1, dtype=np.int64),
    )
    base.update(over)
    return X.View(**base)


def _pastures(n):
    """`n` standing empty pens, so the pen gate is satisfied and only money is under test."""
    return _kinds({i: X.PASTURE for i in range(n)})


COW = 1          # index into ANIMAL_COST / herd


# ---- the purchase must price in the feed ---------------------------------------------------------


def test_an_animal_is_not_bought_when_there_is_no_money_left_to_feed_it():
    """**The core assertion.** One pen, one cow's worth of cash exactly, an empty shed, and
    `feed_wheat=2`. Buying spends the lot and the animal starves in two days, taking the $400 with it.
    The purchase is only rational if the feed is affordable too."""
    v = _view(kind=_pastures(1), money=np.array([float(X.ANIMAL_COST[COW])]), shed_wheat=np.array([0]))
    pl = _plan(herd=[0, P.herd_gene(2), 0], stock_day=0, feed_wheat=2)
    d = X.decide(v, pl)
    assert int(d.buy_animal[0].sum()) == 0, (
        "bought an animal with no money left for feed -- this is the $0 season")


def test_an_animal_is_bought_when_the_feed_is_affordable():
    """The other side of the same gate, so the fix cannot be "never buy anything"."""
    v = _view(kind=_pastures(4), money=np.array([20_000.0]))
    pl = _plan(herd=[0, P.herd_gene(2), 0], stock_day=0, feed_wheat=2)
    d = X.decide(v, pl)
    assert int(d.buy_animal[0].sum()) > 0, "the feed gate has blocked an affordable purchase"


def test_the_stake_is_not_spent_down_to_nothing_on_livestock():
    """14 pens standing and the real $3,000 stake -- the leaders' plan exactly.

    14 animals at $400-500 is $5,600-7,000, so it cannot afford the herd anyway; the requirement is
    that whatever it does buy leaves enough to feed them and still plant. The measured run left $0
    from day 5 to the end of the season.
    """
    v = _view(kind=_pastures(14), money=np.array([STAKE]))
    pl = _plan(herd=[0, P.herd_gene(8), P.herd_gene(6)], stock_day=0, feed_wheat=2)
    d = X.decide(v, pl)
    spend = float((d.buy_animal[0] * X.ANIMAL_COST).sum())
    bought = int(d.buy_animal[0].sum())
    feed_needed = bought * 2 * X.WHEAT_PRICE_CAP        # one day of feed at the budgeting price
    assert STAKE - spend >= feed_needed, (
        f"spent ${spend:,.0f} of the ${STAKE:,.0f} stake on {bought} animals, leaving "
        f"${STAKE - spend:,.0f} against ${feed_needed:,.0f} of feed")


def test_a_starved_herd_is_not_immediately_rebought():
    """**The re-buy loop, which is how 14 became 29.** The pens are standing and empty because the
    animals escaped. Nothing has changed that would let a replacement survive, so buying again just
    posts the purchase price a second time."""
    v = _view(kind=_pastures(8), money=np.array([500.0]), shed_wheat=np.array([0]))
    pl = _plan(herd=[0, P.herd_gene(8), 0], stock_day=0, feed_wheat=2)
    d = X.decide(v, pl)
    assert int(d.buy_animal[0].sum()) == 0, "re-bought into an empty pen with no feed available"


# ---- feed must be ordered for animals that exist but are not yet placed --------------------------


def test_feed_is_ordered_for_animals_still_waiting_in_the_shed():
    """`herd_size` counts `view.animal >= 0`, which is *placed* animals only. Three cows sitting in the
    shed awaiting a PLACE are real, purchased, and will starve on the same clock, but they contribute
    nothing to `want_wheat`, so no feed is ordered for them."""
    v = _view(kind=_pastures(4), money=np.array([20_000.0]),
              shed_animals=np.array([[0, 4, 0]]), shed_wheat=np.array([0]))
    pl = _plan(herd=[0, P.herd_gene(4), 0], stock_day=0, feed_wheat=2)
    d = X.decide(v, pl)
    assert int(d.buy_product[0, X.WHEAT_ITEM]) > 0, (
        "no feed ordered for a herd that is bought but not yet placed")


def test_feed_is_ordered_for_a_placed_herd():
    """The control for the test above: placed animals do drive `want_wheat` today, and must keep
    doing so after the fix."""
    animal = np.full((1, TILES), -1, dtype=np.int64)
    animal[0, :4] = COW
    v = _view(kind=_pastures(4), money=np.array([20_000.0]), animal=animal,
              shed_wheat=np.array([0]))
    pl = _plan(herd=[0, P.herd_gene(4), 0], stock_day=0, feed_wheat=2)
    d = X.decide(v, pl)
    assert int(d.buy_product[0, X.WHEAT_ITEM]) >= 8, (
        "4 animals at feed_wheat=2 needs 8 units of wheat")
