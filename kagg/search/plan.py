"""The search space: a *farm plan*, and its encoding as a vector of categorical genes.

Why a plan and not raw actions
------------------------------

The obvious thing to search on a 750k-step/sec simulator is the raw action sequence: 719 turns of
`Actions`, one op per unit plus a market order list. That space is hopeless and, worse, it is
*untransferable*. Three reasons, all specific to this environment:

1. **Size.** 719 turns x 15 units x 9 ops is ~10^10000 sequences, with a single scalar at the end.
2. **It is not the same problem in the real environment.** An open-loop script assumes it knows
   where every unit is standing. The simulator spawns every hired hand on the NW shed tile while
   the reference balances them across all four (`kagg/sim/parity.py` documents this), and the real
   environment spawns weeds the simulator only matches statistically. An open-loop script that is
   optimal in the simulator desynchronises in the reference on turn one and never recovers.
3. **The interesting decisions are not per-turn.** What actually determines a season is which tile
   grows what, when it is planted, when it is cut, how many hands are paid for that day, and how
   much of the shed goes to market at what price. Those are ~30 decisions a season, not 10,000.

So the search space here is a **closed-loop plan** executed by a deliberately mechanical
interpreter (`kagg.search.executor`). The plan carries all of the strategy; the executor carries
none of it -- it walks a unit to the nearest tile in its block that has an outstanding job and does
that job. Because the executor is closed-loop on the *observed* state, it self-corrects the hand
spawn divergence, weed spawns, and anything else the two implementations disagree about, and the
identical code runs against both the batched simulator and a real observation dict.

This is deliberately *not* the heuristic's parameter vector. `scripts/tune_heuristic.py` tunes 17
dials on top of hand-written routing, crop priorities and sell rules; the experiment log calls that
layer exhausted ("ES tunes numbers; it cannot invent structure"). Here there is no crop priority
order, no filler crop, no sell cadence and no hire curve to inherit -- every tile chooses its own
crop and its own planting phase independently, every five-day block chooses its own sell rate per
product, and every day chooses its own headcount. 277 genes, initialised uniform.

Encoding
--------

Every gene is a **categorical** index, not a float. Crop choice, planting phase and land timing have
no meaningful metric, and the ones that do (headcount, sell quantity) are strongly non-linear in
their effect. A factored categorical distribution -- one probability table per gene -- is therefore
the natural CEM/EDA model, and it makes the learned distribution directly readable: after the
search, `p(gene=WHEAT)` for each tile *is* the answer to "what should this tile grow".

Genes, in order:

===================  ====  ======  ====================================================
name                 dims  values  meaning
===================  ====  ======  ====================================================
``crop_of``          100   6       crop for tile i, or FALLOW (never farm this tile)
``phase``            100   5       plant tile i only on days where ``day % 5 == phase``
``stop_plant``       1     8       last day on which anything is planted
``harvest_par``      5     5       per crop: how ripe to let it get before cutting
``hires``            30    8       target headcount for each day of the season
``sell_qty``         30    6       units offered per sell tick, per product per 5-day block
``sell_every``       1     6       hours between sell ticks
``floor_frac``       5     6       per product: refuse to sell below this fraction of base
``seed_reserve``     1     5       cash kept back from seed buying
``land_day``         3     9       earliest day each extra quadrant may be bought
``dump_day``         1     6       from this day, sell everything regardless of price
===================  ====  ======  ====================================================
"""

from dataclasses import dataclass

import numpy as np

BOARD = 10
TILES = BOARD * BOARD
SEASON_DAYS = 30
N_BLOCKS = 6           # 5-day blocks, for the sell schedule
BLOCK_DAYS = 5

# Crop order is `kaggle_environments.envs.kaggriculture.CROPS`, which is also the first five
# entries of PRODUCTS, so a crop id doubles as a product id.
CROP_NAMES = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"]
N_CROPS = len(CROP_NAMES)
FALLOW = -1

BASE_PRICE = np.array([25.0, 35.0, 60.0, 120.0, 250.0])
SEED_COST = np.array([10.0, 20.0, 50.0, 100.0, 80.0])
FIRST_YIELD_DAY = np.array([2, 2, 8, 10, 10], dtype=np.int16)
MAX_YIELD_DAY = np.array([4, 3, 8, 10, 12], dtype=np.int16)
ONGOING = np.array([False, False, True, True, False])

# Gene value tables. Index into these with the categorical gene.
STOP_PLANT_DAYS = np.array([14, 16, 18, 20, 22, 24, 26, 30], dtype=np.int16)
# For a crop that clears the tile when cut, how many days past `max_yield_day` to wait; for an
# ongoing crop, how many units to let pile up (its cap is 4) before cutting.
HARVEST_DELTA = np.array([-2, -1, 0, 1, 2], dtype=np.int16)
ONGOING_THRESHOLD = np.array([1, 2, 3, 4, 4], dtype=np.int16)
HIRE_LEVELS = np.array([0, 2, 4, 6, 8, 10, 12, 14], dtype=np.int16)
SELL_QTYS = np.array([0, 2, 5, 10, 25, 100], dtype=np.int32)
SELL_EVERY = np.array([1, 2, 3, 4, 6, 12], dtype=np.int16)
FLOOR_FRACS = np.array([0.0, 0.3, 0.5, 0.7, 0.9, 1.1])
SEED_RESERVES = np.array([0.0, 200.0, 500.0, 1000.0, 2000.0])
NEVER = np.int16(999)
LAND_DAYS = np.array([0, 3, 6, 9, 12, 15, 18, 21, NEVER], dtype=np.int16)
DUMP_DAYS = np.array([20, 22, 24, 26, 28, NEVER], dtype=np.int16)

# (name, number of genes, number of categories)
SPEC = (
    ("crop_of", TILES, N_CROPS + 1),
    ("phase", TILES, 5),
    ("stop_plant", 1, len(STOP_PLANT_DAYS)),
    ("harvest_par", N_CROPS, len(HARVEST_DELTA)),
    ("hires", SEASON_DAYS, len(HIRE_LEVELS)),
    ("sell_qty", N_BLOCKS * N_CROPS, len(SELL_QTYS)),
    ("sell_every", 1, len(SELL_EVERY)),
    ("floor_frac", N_CROPS, len(FLOOR_FRACS)),
    ("seed_reserve", 1, len(SEED_RESERVES)),
    ("land_day", 3, len(LAND_DAYS)),
    ("dump_day", 1, len(DUMP_DAYS)),
)

N_GENES = sum(n for _, n, _ in SPEC)
N_CATS = np.concatenate([np.full(n, k, dtype=np.int64) for _, n, k in SPEC])

_OFFSETS = {}
_o = 0
for _name, _n, _k in SPEC:
    _OFFSETS[_name] = (_o, _o + _n)
    _o += _n


def gene_slice(name):
    """(start, stop) index of a named gene block inside a genome vector."""
    return _OFFSETS[name]


@dataclass(frozen=True)
class Plan:
    """A decoded population of plans, every field already expanded to ``[N, ...]``.

    Held as arrays rather than objects because the executor drives the whole population -- and
    every replicate of it -- in one pass over the batch dimension.
    """

    crop_of: np.ndarray        # [N, TILES] int8, -1 = fallow
    phase: np.ndarray          # [N, TILES] int8
    stop_plant: np.ndarray     # [N] int16
    harvest_par: np.ndarray    # [N, N_CROPS] int8, index into HARVEST_DELTA/ONGOING_THRESHOLD
    hires: np.ndarray          # [N, SEASON_DAYS] int16, target headcount
    sell_qty: np.ndarray       # [N, N_BLOCKS, N_CROPS] int32
    sell_every: np.ndarray     # [N] int16
    floor_frac: np.ndarray     # [N, N_CROPS] float64
    seed_reserve: np.ndarray   # [N] float64
    land_day: np.ndarray       # [N, 3] int16
    dump_day: np.ndarray       # [N] int16

    @property
    def size(self):
        return self.crop_of.shape[0]

    def repeat(self, times):
        """Tile the population ``times`` over, so each plan gets several replicate games."""
        return Plan(
            crop_of=np.repeat(self.crop_of, times, axis=0),
            phase=np.repeat(self.phase, times, axis=0),
            stop_plant=np.repeat(self.stop_plant, times, axis=0),
            harvest_par=np.repeat(self.harvest_par, times, axis=0),
            hires=np.repeat(self.hires, times, axis=0),
            sell_qty=np.repeat(self.sell_qty, times, axis=0),
            sell_every=np.repeat(self.sell_every, times, axis=0),
            floor_frac=np.repeat(self.floor_frac, times, axis=0),
            seed_reserve=np.repeat(self.seed_reserve, times, axis=0),
            land_day=np.repeat(self.land_day, times, axis=0),
            dump_day=np.repeat(self.dump_day, times, axis=0),
        )

    def take(self, index):
        """Select plans by index array, in order."""
        index = np.asarray(index)
        return Plan(*(getattr(self, f.name)[index] for f in self.__dataclass_fields__.values()))


def decode(genomes):
    """Turn ``[N, N_GENES]`` categorical genomes into a :class:`Plan`."""
    g = np.asarray(genomes, dtype=np.int64)
    if g.ndim == 1:
        g = g[None, :]
    n = g.shape[0]

    def block(name):
        lo, hi = _OFFSETS[name]
        return g[:, lo:hi]

    crop = block("crop_of") - 1                      # 0 -> FALLOW, 1..5 -> crop id
    sell = SELL_QTYS[block("sell_qty")].reshape(n, N_BLOCKS, N_CROPS)
    return Plan(
        crop_of=crop.astype(np.int8),
        phase=block("phase").astype(np.int8),
        stop_plant=STOP_PLANT_DAYS[block("stop_plant")[:, 0]],
        harvest_par=block("harvest_par").astype(np.int8),
        hires=HIRE_LEVELS[block("hires")],
        sell_qty=sell,
        sell_every=SELL_EVERY[block("sell_every")[:, 0]],
        floor_frac=FLOOR_FRACS[block("floor_frac")],
        seed_reserve=SEED_RESERVES[block("seed_reserve")[:, 0]],
        land_day=LAND_DAYS[block("land_day")],
        dump_day=DUMP_DAYS[block("dump_day")[:, 0]],
    )


def uniform_probs():
    """The initial CEM distribution: uniform over every gene's categories.

    Deliberately uninformed. Seeding it from the heuristic would reintroduce exactly the prior the
    search exists to escape.
    """
    k = int(N_CATS.max())
    probs = np.zeros((N_GENES, k))
    for i, cats in enumerate(N_CATS):
        probs[i, :cats] = 1.0 / cats
    return probs


def sample(probs, n, rng):
    """Draw ``n`` genomes from a factored categorical distribution ``[N_GENES, K]``."""
    cum = np.cumsum(probs, axis=1)
    cum /= cum[:, -1:]
    draws = rng.random((n, probs.shape[0]))
    out = (draws[:, :, None] > cum[None, :, :]).sum(axis=2)
    return np.minimum(out, (N_CATS - 1)[None, :]).astype(np.int64)


def random_genomes(n, rng):
    return sample(uniform_probs(), n, rng)


def describe(genome):
    """A human-readable summary of one genome, for the experiment log."""
    plan = decode(genome[None, :])
    lines = []
    counts = {}
    for c in plan.crop_of[0]:
        name = "FALLOW" if c < 0 else CROP_NAMES[c]
        counts[name] = counts.get(name, 0) + 1
    lines.append("tiles: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    lines.append(f"stop_plant day {int(plan.stop_plant[0])}, dump day {int(plan.dump_day[0])}")
    lines.append("hires by day: " + " ".join(str(int(h)) for h in plan.hires[0]))
    lines.append(f"sell every {int(plan.sell_every[0])}h, reserve ${plan.seed_reserve[0]:.0f}")
    for c, name in enumerate(CROP_NAMES):
        qty = " ".join(str(int(q)) for q in plan.sell_qty[0, :, c])
        lines.append(
            f"  {name:<11} sell/tick by block: {qty}"
            f" | floor {plan.floor_frac[0, c]:.1f}x base"
            f" | harvest par {int(plan.harvest_par[0, c])}"
        )
    lines.append("land days: " + " ".join(str(int(d)) for d in plan.land_day[0]))
    return "\n".join(lines)
