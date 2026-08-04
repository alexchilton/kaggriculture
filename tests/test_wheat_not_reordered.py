"""Wheat already in hand must count against the feed requirement.

One theory, one test. `executor.py`:

    short = np.maximum(want_wheat - view.shed_wheat, 0)

`view.shed_wheat` is *shed* stock. A unit at the shed picks feed up at dawn (`fetch_wheat`), which
moves it out of the shed and into `carried_wheat` -- so the shed reads 0 again and `short` reads the
whole requirement on the very next turn. The order is therefore re-emitted every turn of every day,
24 times over, no matter how much wheat the farm is already carrying.

Measured in `data/logs/cash_ledger.log`, days 0-7 of the $147,178 seat's own encoded plan:

    day     open      sold  |    seeds  animals   wheat   hires   land |    close
      0    3,000       810  |    1,040    1,600     825       7      0 |      273
      6      335     1,437  |        0        0   1,225      20  1,000 |      310
    over 8 days: earned $6,459 | seeds $1,120  animals $2,000  wheat $5,075

$5,075 of wheat in eight days -- 203 units -- for twelve animals whose requirement is 24 units held.
The seat being copied bought 967 units across the *whole thirty-day season*. Day 0 asks for $3,465
against a $3,000 stake, so the market part-fills and the farm opens already broken; the balance then
never reaches the $1,000 for the first land parcel, so the melon and strawberry tiles are planted six
days late and miss their day-10 first yield.

The fix is to count what the farm holds anywhere -- shed plus every unit's hands -- against the
requirement, which is what "hold `feed_wheat` units per animal" meant in the first place.
"""

import numpy as np
import pytest

from kagg.search import executor as X
from kagg.search import plan as P
from kagg.sim.tiles import EMPTY, PASTURE

COW = P.ANIMAL_NAMES.index("COW")
FEED_PER_HEAD = 2
HERD = 4


def _view(shed_wheat, carried_wheat, money=3000.0):
    """Four pens with a cow on each, and feed split between the shed and the crew's hands."""
    tiles = 100
    kind = np.full((1, tiles), EMPTY, dtype=np.int64)
    kind[0, :HERD] = PASTURE
    animal = np.full((1, tiles), -1, dtype=np.int64)
    animal[0, :HERD] = COW
    carried = np.zeros((1, X.MAX_EXEC_UNITS), dtype=np.int64)
    carried[0, 0] = carried_wheat
    return X.View(
        day=3, hour=5,
        kind=kind,
        crop=np.full((1, tiles), -1, dtype=np.int64),
        planted_day=np.zeros((1, tiles), dtype=np.int64),
        watered=np.zeros((1, tiles), dtype=bool),
        yield_units=np.zeros((1, tiles), dtype=np.int64),
        unit_ord=np.zeros((1, X.MAX_EXEC_UNITS), dtype=np.int64),
        n_units=np.array([4]),
        money=np.array([money]),
        seeds=np.zeros((1, P.N_CROPS), dtype=np.int64),
        shed=np.zeros((1, P.N_PRODUCTS), dtype=np.int64),
        prices=np.zeros((1, P.N_PRODUCTS), dtype=np.int64),
        n_land=np.array([0]),
        animal=animal,
        shed_wheat=np.array([shed_wheat]),
        carried_wheat=carried,
    )


def _plan():
    g = np.zeros(P.N_GENES, dtype=np.int64)
    lo, _ = P.gene_slice("crop_of")
    g[lo:lo + HERD] = P.CROP_GENE_PASTURE
    a, _ = P.gene_slice("herd")
    g[a + COW] = P.herd_gene(HERD)
    lo, _ = P.gene_slice("feed_wheat")
    g[lo] = int(np.flatnonzero(P.FEED_WHEAT == FEED_PER_HEAD)[0])
    return P.decode(g[None])


def test_wheat_in_the_shed_satisfies_the_requirement():
    """The baseline: requirement met from the shed alone, so nothing is ordered."""
    d = X.decide(_view(shed_wheat=HERD * FEED_PER_HEAD, carried_wheat=0), _plan())
    assert int(d.buy_product[0, X.WHEAT_ITEM]) == 0


def test_wheat_carried_by_a_unit_also_satisfies_it():
    """**The bug.** The same wheat, moved from the shed into a unit's hands, must still count.

    This is the whole failure: `fetch_wheat` does exactly this move at dawn, so under the old
    condition the requirement reset to full on every turn after the pickup.
    """
    d = X.decide(_view(shed_wheat=0, carried_wheat=HERD * FEED_PER_HEAD), _plan())
    assert int(d.buy_product[0, X.WHEAT_ITEM]) == 0, (
        f"ordered {int(d.buy_product[0, X.WHEAT_ITEM])} more wheat while the crew is already "
        f"carrying {HERD * FEED_PER_HEAD} units -- the full requirement for a herd of {HERD}")


def test_a_genuine_shortfall_is_still_ordered():
    """The fix must not silence the order entirely -- half the feed held means half is still wanted."""
    held = HERD * FEED_PER_HEAD // 2
    d = X.decide(_view(shed_wheat=0, carried_wheat=held), _plan())
    ordered = int(d.buy_product[0, X.WHEAT_ITEM])
    assert ordered == HERD * FEED_PER_HEAD - held, (
        f"holding {held} of {HERD * FEED_PER_HEAD} and ordered {ordered}")
