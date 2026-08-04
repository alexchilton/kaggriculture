"""Milk, wool, eggs and fertiliser must be sellable. They currently are not, at all.

One theory, one test. Read off `data/logs/diverge_by_day_147k.log`, where the shed's produce climbs
to 30 units by day 20 and never moves again while the bank sits at $0:

    market.PRODUCTS = [WHEAT, CARROT, TOMATO, STRAWBERRY, MELON, EGG, MILK, WOOL, FERTILIZER]
    executor.Decision.sell : [B, N_CROPS]        <- five wide
    executor.View.shed     : farm.shed[:, :N_CROPS]
    executor.View.prices   : price(inventory)[:, :N_CROPS]

So `decide` can only ever emit a SELL for the five crops. EGG, MILK, WOOL and FERTILIZER have no sell
path, and the executor cannot even see that it holds them. `docs/episode_teardown_2026-08-03.md`
measures the leaders drawing ~83% of revenue from converting bought wheat into milk and wool, so this
is not an efficiency loss -- the animal half of the economy produces goods the decoder cannot trade.

Why it hid: `CLAUDE.md` -- "a gate only tests what it exercises". The livestock genes, the livestock
ops and the FEED/CARE/HARVEST chain were all added on 2026-08-04 and every one of them was tested.
The sell path stayed five wide, so no test could fail on it. This is the fourth instance of that
pattern recorded in `CLAUDE.md` and the mechanism is identical each time.
"""

import numpy as np
import pytest

from kagg.search import executor as X
from kagg.search import plan as P
from kagg.sim.market import PRODUCTS
from kagg.sim.tiles import EMPTY, PASTURE

ANIMAL_PRODUCTS = ["EGG", "MILK", "WOOL", "FERTILIZER"]


def test_the_product_list_is_wider_than_the_crop_list():
    """The premise, stated as a check so a future change to either list is caught here."""
    assert PRODUCTS[:P.N_CROPS] == P.CROP_NAMES
    assert [p for p in PRODUCTS[P.N_CROPS:]] == ANIMAL_PRODUCTS


def _view_holding_animal_produce(qty=20):
    """Late season, shed full of milk and wool, nothing growing, a herd standing on pens."""
    tiles = 100
    kind = np.full((1, tiles), EMPTY, dtype=np.int64)
    kind[0, :4] = PASTURE
    shed = np.zeros((1, len(PRODUCTS)), dtype=np.int64)
    for name in ANIMAL_PRODUCTS:
        shed[0, PRODUCTS.index(name)] = qty
    animal = np.full((1, tiles), -1, dtype=np.int64)
    animal[0, :4] = P.ANIMAL_NAMES.index("COW")
    return dict(
        day=25, hour=0,
        kind=kind,
        crop=np.full((1, tiles), -1, dtype=np.int64),
        planted_day=np.zeros((1, tiles), dtype=np.int64),
        watered=np.zeros((1, tiles), dtype=bool),
        yield_units=np.zeros((1, tiles), dtype=np.int64),
        unit_ord=np.zeros((1, X.MAX_EXEC_UNITS), dtype=np.int64),
        n_units=np.array([4]),
        money=np.array([5000.0]),
        seeds=np.zeros((1, P.N_CROPS), dtype=np.int64),
        prices=np.full((1, P.N_CROPS), 100, dtype=np.int64),
        n_land=np.array([0]),
        animal=animal,
    ), shed


def test_a_shed_full_of_milk_and_wool_produces_a_sell_order():
    """Day 25, past any dump day, 20 units of each animal product held. It must be traded."""
    kwargs, shed = _view_holding_animal_produce()
    # The full nine-wide shed. Passing `shed[:, :N_CROPS]` here would be padded back to nine with
    # zeros by `View.__post_init__`, silently deleting the stock this test is about.
    view = X.View(shed=shed, **kwargs)

    g = np.zeros(P.N_GENES, dtype=np.int64)
    lo, _ = P.gene_slice("dump_day")
    g[lo] = int(np.argmin(np.abs(P.DUMP_DAYS - 20)))
    plan = P.decode(g[None])

    d = X.decide(view, plan)
    assert d.sell.shape[1] == len(PRODUCTS), (
        f"`Decision.sell` is {d.sell.shape[1]} wide against {len(PRODUCTS)} products, so "
        f"{ANIMAL_PRODUCTS} have no sell path at all")
    for name in ANIMAL_PRODUCTS:
        i = PRODUCTS.index(name)
        assert int(d.sell[0, i]) > 0, f"holding 20 {name} on day 25 and selling none of it"


def test_the_view_built_from_a_real_game_can_see_what_it_holds():
    """A decoder cannot decide to sell a thing it cannot observe.

    Asserted against `rollout.build_view`, not against a hand-built `View`. The slicing lives at the
    call site, so a `View` constructed in a test with 9-wide arrays proves nothing about the executor
    -- an earlier version of this test did exactly that and passed while the bug was live.
    """
    from kagg.search import rollout
    from kagg.sim.game import Game

    game = Game(1, rng=np.random.default_rng(0), unlock_schedule={})
    view = rollout.build_view(game, 0, day=0, hour=0)
    assert view.shed.shape[1] == len(PRODUCTS), (
        f"`build_view` exposes {view.shed.shape[1]} of {len(PRODUCTS)} products' stock, so the "
        f"executor cannot see that it holds {ANIMAL_PRODUCTS}")
    assert view.prices.shape[1] == len(PRODUCTS), (
        f"`build_view` exposes {view.prices.shape[1]} of {len(PRODUCTS)} products' prices")
