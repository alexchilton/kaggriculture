"""The plan executor must be able to run the livestock half, in the order the rules require.

**Why this file exists.** `d14bb94` gave the genome `herd`, `stock_day`, `feed_wheat`, `fert_policy`
and PASTURE/COOP tiles, and `executor.py` reads none of them -- so every gene is inert and CEM is still
searching the crop-only subspace. Round 1 of the search reached $42,087 with no animals at all, against
leaders banking $100k-$144k who draw 34.9% of revenue from milk and wool
(`docs/episode_teardown_2026-08-03.md`).

**The ordering constraint is the whole risk, and it is not hypothetical.** `jax_frontier.py` is marked
BROKEN in its own docstring for exactly this: it bought its four starter animals, `max empty pens` over
240 turns was **0**, so they sat in the shed as dead capital and it banked **$380**. An earlier version
sent a unit to PICKUP an animal with no route to a pen and PICKUP hit **70.5% of all actions**.

So the sequence is a hard requirement, not a preference:

    BUILD_PASTURE on an EMPTY structure tile     (free and instant, `jax_sim.py:613`)
      -> BUY_ANIMAL, but only if a pen is standing and empty
      -> PICKUP the animal from the shed
      -> PLACE it on the empty structure
      -> FEED it, which needs the unit to be CARRYING WHEAT (`jax_masks.py:96`)
      -> CARE, HARVEST, COLLECT_FERTILIZER

**And feeding is not optional.** `jax_sim.py:1159` escapes an animal at `consecutive_unfed >= 2`,
taking the full purchase price with it. A plan that buys and does not feed is strictly worse than one
that never buys -- which is what $380 looks like. `test_an_animal_is_never_bought_without_a_pen_to_put_it_in`
and `test_a_hungry_animal_is_fed_before_anything_optional` are the two that keep this honest.

Leaders' reference numbers, for calibration: `COW 8, SHEEP 6, GOOSE 0`, 14 pastures, **0 coops**, 967
units of wheat bought as feed, and 318 COLLECT_FERTILIZER against 107 FERTILIZE.
"""

import numpy as np
import pytest

from kagg.search import executor as X
from kagg.search import plan as P
from kagg.sim import ops as O

pytest.importorskip("kagg.search.executor")

TILES = X.TILES


def _plan(**over):
    """One plan, all genes at category 0 unless overridden."""
    g = np.zeros(P.N_GENES, dtype=np.int64)
    for name, values in over.items():
        lo, hi = P.gene_slice(name)
        g[lo:hi] = values
    return P.decode(g)


def _view(day=10, hour=0, n_units=2, unit_at=None, **over):
    """A batch of one, empty NW quadrant, nothing planted.

    `unit_at` is the serpentine ordinal every unit stands on. It defaults to the shed, because that is
    where the simulator respawns the crew each dawn -- but a test asking "does this op fire on tile N"
    has to stand the unit on tile N, or it measures a walk instead of the op.
    """
    base = dict(
        day=day, hour=hour,
        kind=np.full((1, TILES), X.EMPTY, dtype=np.int64),
        crop=np.full((1, TILES), -1, dtype=np.int64),
        planted_day=np.zeros((1, TILES), dtype=np.int64),
        watered=np.zeros((1, TILES), dtype=bool),
        yield_units=np.zeros((1, TILES), dtype=np.int64),
        # **Units start on the shed**, because that is where the simulator respawns the whole crew
        # every dawn (`ops.SHED_TILES`). Parking them on tile 0 made the dawn PICKUP window
        # unreachable and the first version of this fixture tested a state the game never produces.
        unit_ord=np.full((1, X.MAX_EXEC_UNITS),
                        int(X.SHED_ORDS[0]) if unit_at is None else int(unit_at), dtype=np.int64),
        n_units=np.array([n_units]),
        money=np.array([20_000.0]),
        seeds=np.zeros((1, P.N_CROPS), dtype=np.int64),
        shed=np.zeros((1, P.N_CROPS), dtype=np.int64),
        prices=np.full((1, P.N_CROPS), 100, dtype=np.int64),
        n_land=np.array([0]),
    )
    base.update(_animal_defaults())
    base.update(over)
    return X.View(**base)


def _animal_defaults():
    """The fields `View` gains for livestock. Kept in one place so a rename shows up once."""
    return dict(
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


# ---- structures ----------------------------------------------------------------------------------


def test_a_structure_tile_gets_built():
    """`structure_of` says PASTURE and the tile is EMPTY, so a unit must go and build it.
    Free and instant, so there is never a reason to defer."""
    crop = np.zeros(TILES, dtype=np.int64)
    crop[0] = P.CROP_GENE_PASTURE
    d = X.decide(_view(unit_at=0), _plan(crop_of=crop))
    assert O.BUILD_PASTURE in list(d.unit_op[0]), "nobody was sent to build the pasture"


def test_a_coop_tile_builds_a_coop_not_a_pasture():
    crop = np.zeros(TILES, dtype=np.int64)
    crop[0] = P.CROP_GENE_COOP
    d = X.decide(_view(unit_at=0), _plan(crop_of=crop))
    assert O.BUILD_COOP in list(d.unit_op[0])


def test_a_built_structure_is_not_rebuilt():
    """The tile is already a PASTURE, so BUILD would be a wasted turn forever."""
    crop = np.zeros(TILES, dtype=np.int64)
    crop[0] = P.CROP_GENE_PASTURE
    v = _view(kind=_kinds({0: X.PASTURE}))
    d = X.decide(v, _plan(crop_of=crop))
    assert O.BUILD_PASTURE not in list(d.unit_op[0])


# ---- buying, and the ordering that broke jax_frontier --------------------------------------------


def test_an_animal_is_never_bought_without_a_pen_to_put_it_in():
    """**The regression that cost `jax_frontier` its season.** No structure standing, so no purchase --
    an animal with nowhere to go is dead capital and, worse, invites a PICKUP loop."""
    d = X.decide(_view(), _plan(herd=[0, P.herd_gene(8), 0], stock_day=0))
    assert int(d.buy_animal[0].sum()) == 0, "bought an animal with no pen built"


def test_an_animal_is_bought_once_an_empty_pen_exists():
    crop = np.zeros(TILES, dtype=np.int64)
    crop[0] = P.CROP_GENE_PASTURE
    v = _view(kind=_kinds({0: X.PASTURE}))
    d = X.decide(v, _plan(crop_of=crop, herd=[0, P.herd_gene(8), 0], stock_day=0))
    assert int(d.buy_animal[0, 1]) > 0, "a pen is standing and empty and no cow was ordered"


def test_buying_stops_at_the_herd_target():
    """Two pens, target of two cows, both already placed -- so nothing more is ordered."""
    crop = np.zeros(TILES, dtype=np.int64)
    crop[:2] = P.CROP_GENE_PASTURE
    v = _view(kind=_kinds({0: X.PASTURE, 1: X.PASTURE}),
              animal=_animals({0: 1, 1: 1}))
    d = X.decide(v, _plan(crop_of=crop, herd=[0, P.herd_gene(2), 0], stock_day=0))
    assert int(d.buy_animal[0].sum()) == 0


def test_nothing_is_bought_before_the_stocking_day():
    crop = np.zeros(TILES, dtype=np.int64)
    crop[0] = P.CROP_GENE_PASTURE
    v = _view(day=3, kind=_kinds({0: X.PASTURE}))
    pl = _plan(crop_of=crop, herd=[0, P.herd_gene(8), 0], stock_day=_gene(P.STOCK_DAYS, 8))
    assert int(X.decide(v, pl).buy_animal[0].sum()) == 0


# ---- placing -------------------------------------------------------------------------------------


def test_an_animal_in_the_shed_is_collected_and_placed():
    """Two steps, and both must be reachable: PICKUP at the shed, then PLACE on the empty pen."""
    crop = np.zeros(TILES, dtype=np.int64)
    crop[0] = P.CROP_GENE_PASTURE
    pl = _plan(crop_of=crop, herd=[0, P.herd_gene(8), 0], stock_day=0)

    holding = _view(kind=_kinds({0: X.PASTURE}), shed_animals=np.array([[0, 1, 0]]))
    ops = list(X.decide(holding, pl).unit_op[0])
    assert O.PICKUP in ops or O.NORTH in ops or O.SOUTH in ops or O.EAST in ops or O.WEST in ops

    carrying = _view(unit_at=0, kind=_kinds({0: X.PASTURE}),
                     carried_animal=_carry_animal(0, 1))
    d = X.decide(carrying, pl)
    assert O.PLACE in list(d.unit_op[0]), "a unit carrying a cow past an empty pen must place it"


# ---- maintenance: the half that has never once fired ---------------------------------------------


def test_a_hungry_animal_is_fed_before_anything_optional():
    """**The acceptance test for the whole feature.** An animal one night from escaping, and a unit
    carrying wheat, must produce FEED. `jax_sim.py:1159` escapes at `consecutive_unfed >= 2`, so this
    is the difference between an asset and a $400 write-off."""
    crop = np.zeros(TILES, dtype=np.int64)
    crop[0] = P.CROP_GENE_PASTURE
    v = _view(unit_at=0, kind=_kinds({0: X.PASTURE}), animal=_animals({0: 1}),
              consecutive_unfed=_ints({0: 1}), carried_wheat=_carry_wheat(0, 2))
    d = X.decide(v, _plan(crop_of=crop, feed_wheat=_gene(P.FEED_WHEAT, 2)))
    assert O.FEED in list(d.unit_op[0]), "a hungry animal next to carried wheat was not fed"


def test_a_fed_animal_is_not_fed_twice():
    crop = np.zeros(TILES, dtype=np.int64)
    crop[0] = P.CROP_GENE_PASTURE
    v = _view(kind=_kinds({0: X.PASTURE}), animal=_animals({0: 1}),
              fed_today=_bools({0: True}), carried_wheat=_carry_wheat(0, 2))
    assert O.FEED not in list(X.decide(v, _plan(crop_of=crop)).unit_op[0])


def test_wheat_is_bought_as_feed_rather_than_grown():
    """The leaders buy 967 units of wheat. `feed_wheat` is units held *per animal*, so a herd with an
    empty shed has to place a BUY_PRODUCT order."""
    crop = np.zeros(TILES, dtype=np.int64)
    crop[0] = P.CROP_GENE_PASTURE
    v = _view(kind=_kinds({0: X.PASTURE}), animal=_animals({0: 1}))
    d = X.decide(v, _plan(crop_of=crop, feed_wheat=_gene(P.FEED_WHEAT, 4)))
    assert int(d.buy_product[0, 0]) > 0, "no wheat ordered for a herd with an empty shed"


def test_an_animal_with_product_is_harvested():
    crop = np.zeros(TILES, dtype=np.int64)
    crop[0] = P.CROP_GENE_PASTURE
    v = _view(unit_at=0, kind=_kinds({0: X.PASTURE}), animal=_animals({0: 1}),
              yield_units=_ints({0: 3}), fed_today=_bools({0: True}))
    assert O.HARVEST in list(X.decide(v, _plan(crop_of=crop)).unit_op[0])


def test_free_fertiliser_is_collected():
    """No action cost, one per animal per day (`jax_masks.py:98`). The leaders run 318 collects a
    season and sell 406 units for ~$21,900; our pool takes none of it."""
    crop = np.zeros(TILES, dtype=np.int64)
    crop[0] = P.CROP_GENE_PASTURE
    v = _view(unit_at=0, kind=_kinds({0: X.PASTURE}), animal=_animals({0: 1}),
              fed_today=_bools({0: True}), cared_today=_bools({0: True}),
              fertilizer_available=_bools({0: True}))
    assert O.COLLECT_FERT in list(X.decide(v, _plan(crop_of=crop)).unit_op[0])


# ---- a plan with no animals must be unchanged ----------------------------------------------------


def test_a_crop_only_plan_is_untouched():
    """`best_plan.json` has no structures and no herd. Adding livestock must not change what it does,
    or the CEM baseline and every saved plan silently become a different agent."""
    crop = np.zeros(TILES, dtype=np.int64)
    crop[:20] = 5                                        # melon everywhere
    v = _view(seeds=np.array([[0, 0, 0, 0, 10]]))
    d = X.decide(v, _plan(crop_of=crop))
    assert int(d.buy_animal[0].sum()) == 0
    for op in (O.BUILD_PASTURE, O.BUILD_COOP, O.FEED, O.CARE, O.COLLECT_FERT, O.PLACE):
        assert op not in list(d.unit_op[0]), f"{op} fired on a crop-only plan"


# ---- helpers -------------------------------------------------------------------------------------


def _kinds(mapping):
    a = np.full((1, TILES), X.EMPTY, dtype=np.int64)
    for i, v in mapping.items():
        a[0, i] = v
    return a


def _animals(mapping):
    a = np.full((1, TILES), -1, dtype=np.int64)
    for i, v in mapping.items():
        a[0, i] = v
    return a


def _ints(mapping):
    a = np.zeros((1, TILES), dtype=np.int64)
    for i, v in mapping.items():
        a[0, i] = v
    return a


def _bools(mapping):
    a = np.zeros((1, TILES), dtype=bool)
    for i, v in mapping.items():
        a[0, i] = v
    return a


def _carry_wheat(unit, qty):
    a = np.zeros((1, X.MAX_EXEC_UNITS), dtype=np.int64)
    a[0, unit] = qty
    return a


def _carry_animal(unit, animal):
    a = np.full((1, X.MAX_EXEC_UNITS), -1, dtype=np.int64)
    a[0, unit] = animal
    return a


def _gene(table, value):
    hits = np.flatnonzero(np.asarray(table) == value)
    if not len(hits):
        raise ValueError(f"{value} not in {list(table)}")
    return int(hits[0])
