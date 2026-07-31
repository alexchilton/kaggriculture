"""Hand-written plans, used as the fixed opposition the search plays against.

These are **not** candidates and nothing is tuned here. They exist because a search needs a field
to be a best response to, and `CLAUDE.md` is emphatic that a field of one weak opponent produces
numbers about twice reality. Each is a plain-language transcription of a profile from
`kagg.arena.pool.OPPONENTS` into the plan language:

- ``melon_wheat``  -- the current heuristic's shape: the free quadrant in melon, wheat everywhere
  else, ten hands, continuous selling with a price floor, land bought as it becomes affordable.
- ``wheat_only``   -- the pool's ``wheat_only``.
- ``carrot_small`` -- the pool's ``carrot_25``: one quadrant of carrots, no expansion. Copied from
  an agent that actually beat this project on the ladder.

Whether these are *strong enough* to be worth searching against is a measured question, not an
assumed one -- `scripts/search_plans.py --calibrate` plays them in the real environment against
`kagg.arena`'s opponent pool and reports what they score.
"""

import numpy as np

from kagg.search.plan import (
    DUMP_DAYS,
    FLOOR_FRACS,
    HARVEST_DELTA,
    HIRE_LEVELS,
    LAND_DAYS,
    N_CROPS,
    SEED_RESERVES,
    SELL_EVERY,
    SELL_QTYS,
    STOP_PLANT_DAYS,
    TILES,
    gene_slice,
    N_GENES,
)
from kagg.search.executor import ORDER

WHEAT, CARROT, TOMATO, STRAWBERRY, MELON = range(N_CROPS)


def _cat(table, value):
    """Index of the table entry closest to `value` -- the genes are categorical, so snap."""
    return int(np.argmin(np.abs(np.asarray(table, dtype=float) - float(value))))


def nw_quadrant():
    """Serpentine positions inside the always-unlocked NW quadrant."""
    return [i for i, (x, y) in enumerate(ORDER) if x < 5 and y < 5]


def genome(crops, phase_mod=5, hands=10, sell_qty=25, sell_every=4, floor=0.5,
           stop_plant=24, dump_day=28, land_days=(6, 12, 20), reserve=200,
           harvest_delta=0):
    """Build one genome. `crops` maps serpentine tile position -> crop id, or None for fallow."""
    g = np.zeros(N_GENES, dtype=np.int64)

    lo, hi = gene_slice("crop_of")
    for i in range(TILES):
        c = crops[i]
        g[lo + i] = 0 if c is None else c + 1

    lo, hi = gene_slice("phase")
    for i in range(TILES):
        g[lo + i] = i % max(1, phase_mod)

    g[gene_slice("stop_plant")[0]] = _cat(STOP_PLANT_DAYS, stop_plant)
    lo, hi = gene_slice("harvest_par")
    g[lo:hi] = _cat(HARVEST_DELTA, harvest_delta)

    lo, hi = gene_slice("hires")
    g[lo:hi] = _cat(HIRE_LEVELS, hands)

    lo, hi = gene_slice("sell_qty")
    g[lo:hi] = _cat(SELL_QTYS, sell_qty)

    g[gene_slice("sell_every")[0]] = _cat(SELL_EVERY, sell_every)
    lo, hi = gene_slice("floor_frac")
    g[lo:hi] = _cat(FLOOR_FRACS, floor)
    g[gene_slice("seed_reserve")[0]] = _cat(SEED_RESERVES, reserve)

    lo, hi = gene_slice("land_day")
    for k in range(3):
        g[lo + k] = _cat(LAND_DAYS, land_days[k])
    g[gene_slice("dump_day")[0]] = _cat(DUMP_DAYS, dump_day)
    return g


def melon_wheat():
    nw = set(nw_quadrant())
    return genome([MELON if i in nw else WHEAT for i in range(TILES)])


def wheat_only():
    return genome([WHEAT] * TILES)


def carrot_small():
    nw = set(nw_quadrant())
    return genome(
        [CARROT if i in nw else None for i in range(TILES)],
        land_days=(999, 999, 999),
    )


def opposition():
    """The fixed field the search plays against."""
    return np.stack([melon_wheat(), wheat_only(), carrot_small()])


NAMES = ("melon_wheat", "wheat_only", "carrot_small")
