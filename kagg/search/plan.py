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

# ---- livestock -----------------------------------------------------------------------------------
#
# **Added 2026-08-04. The search space could not express the strategy that is winning.**
# `docs/episode_teardown_2026-08-03.md`: the top three agents all submit the same plan -- COW 8,
# SHEEP 6, GOOSE 0, 14 pastures, 0 coops, 967 units of wheat bought as feed -- and draw 34.9% of
# revenue from milk and wool plus ~6% from reselling fertiliser collected free off the animals.
# `crop_of` had six categories, five crops and fallow, so a tile could not hold a structure and CEM
# was searching the crop-only subspace we have already measured losing.

# A tile's *use* is one decision, so structures are extra `crop_of` categories rather than a second
# competing gene block. Gene values: 0 = fallow, 1..5 = crop, 6 = coop, 7 = pasture.
CROP_GENE_COOP = N_CROPS + 1
CROP_GENE_PASTURE = N_CROPS + 2
NO_STRUCTURE, COOP, PASTURE = 0, 1, 2

ANIMAL_NAMES = ["GOOSE", "COW", "SHEEP"]
N_ANIMALS = len(ANIMAL_NAMES)

# Target headcount per species. The measured meta is COW 8 / SHEEP 6, so the ladder brackets both
# and reaches well past them -- a search that cannot exceed the known point cannot improve on it.
HERD_LEVELS = np.array([0, 2, 4, 6, 8, 10, 12, 16], dtype=np.int16)

# Day to start stocking. Animals pay from `ANIMAL_FIRST_YIELD_DAY` (goose 4, sheep 6, cow 8) and a
# structure is free to build (`jax_sim.py:613`), so the only cost of going early is the cash.
STOCK_DAYS = np.array([0, 2, 4, 6, 8, 12, 16, NEVER], dtype=np.int16)

# Units of wheat to hold *per animal* for feeding. `jax_masks.py:96` gates FEED on `carrying_wheat`,
# and an animal unfed two nights escapes with the whole purchase price. The leaders bought 967 units
# for 14 animals over a season.
FEED_WHEAT = np.array([0, 1, 2, 4, 8], dtype=np.int16)

# What to do with fertiliser. COLLECT_FERTILIZER is free -- no action cost, one per animal per day --
# and FERTILIZE doubles a watered plant's yield for three days (`jax_sim.py:1096`). The leaders do
# both: 318 collects, 107 fertilises, and 406 units sold for ~$21,900.
FERT_SELL, FERT_APPLY, FERT_APPLY_THEN_SELL = 0, 1, 2
N_FERT_POLICIES = 3

# (name, number of genes, number of categories)
# **Append-only.** Inserting a block would repoint every gene after it and silently change what
# `best_plan.json` means -- `agent.py` loads that file as the default plan. `pad_genome` migrates a
# genome saved before the livestock blocks existed, and `tests/test_plan_animals.py` pins that it
# decodes to exactly the same plan it did before.
SPEC = (
    ("crop_of", TILES, N_CROPS + 3),          # + coop, + pasture
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
    # --- livestock, appended 2026-08-04 ---
    ("herd", N_ANIMALS, len(HERD_LEVELS)),
    ("stock_day", 1, len(STOCK_DAYS)),
    ("feed_wheat", 1, len(FEED_WHEAT)),
    ("fert_policy", 1, N_FERT_POLICIES),
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
    structure_of: np.ndarray   # [N, TILES] int8, NO_STRUCTURE / COOP / PASTURE
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
    herd: np.ndarray           # [N, N_ANIMALS] int16, target headcount per species
    stock_day: np.ndarray      # [N] int16, day to start buying animals (NEVER = none)
    feed_wheat: np.ndarray     # [N] int16, wheat units held per animal for FEED
    fert_policy: np.ndarray    # [N] int8, FERT_SELL / FERT_APPLY / FERT_APPLY_THEN_SELL

    @property
    def size(self):
        return self.crop_of.shape[0]

    def repeat(self, times):
        """Tile the population ``times`` over, so each plan gets several replicate games.

        Iterates the dataclass fields rather than naming each one, because the hand-written version
        listed eleven fields and adding a twelfth meant every replicate silently carried a default.
        """
        return Plan(*(np.repeat(getattr(self, f), times, axis=0)
                      for f in self.__dataclass_fields__))

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

    raw_use = block("crop_of")                       # 0 -> FALLOW, 1..5 -> crop, 6 coop, 7 pasture
    crop = raw_use - 1
    structure = np.where(raw_use == CROP_GENE_COOP, COOP,
                         np.where(raw_use == CROP_GENE_PASTURE, PASTURE, NO_STRUCTURE))
    # A structure tile grows nothing. Without this the executor would try to plant a pasture, which
    # is the class of bug that left `jax_frontier` with `max empty pens: 0` and $380 in the bank.
    crop = np.where(structure != NO_STRUCTURE, FALLOW, crop)
    sell = SELL_QTYS[block("sell_qty")].reshape(n, N_BLOCKS, N_CROPS)
    return Plan(
        crop_of=crop.astype(np.int8),
        structure_of=structure.astype(np.int8),
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
        herd=HERD_LEVELS[block("herd")],
        stock_day=STOCK_DAYS[block("stock_day")[:, 0]],
        feed_wheat=FEED_WHEAT[block("feed_wheat")[:, 0]],
        fert_policy=block("fert_policy")[:, 0].astype(np.int8),
    )


def herd_gene(count):
    """The gene value whose `HERD_LEVELS` entry is `count`, for writing a known plan down by hand."""
    hits = np.flatnonzero(HERD_LEVELS == count)
    if not len(hits):
        raise ValueError(f"herd size {count} is not on the ladder {list(HERD_LEVELS)}")
    return int(hits[0])


def pad_genome(genome):
    """Migrate a genome saved before a block was appended, by filling the new genes with category 0.

    `kagg/search/best_plan.json` holds a 277-gene genome from before the livestock blocks existed and
    `agent.py` loads it as the default plan. Category 0 is `HERD_LEVELS[0] == 0` and
    `FEED_WHEAT[0] == 0`, i.e. no animals -- so a padded old genome decodes to exactly the plan it
    always decoded to, which is what `tests/test_plan_animals.py` asserts.

    A genome that is *longer* than `N_GENES` is an error rather than something to truncate: it means
    the file was written by a newer version and silently dropping its tail would run a different plan
    than the one that was saved.
    """
    g = np.asarray(genome, dtype=np.int64)
    if g.shape[-1] > N_GENES:
        raise ValueError(f"genome has {g.shape[-1]} genes, more than the current {N_GENES}")
    if g.shape[-1] == N_GENES:
        return g
    pad = np.zeros(g.shape[:-1] + (N_GENES - g.shape[-1],), dtype=np.int64)
    return np.concatenate([g, pad], axis=-1)


# **Livestock is in the sampled space.** Set False only to reproduce a crop-only search.
#
# A hand-written plan with 14 animals and `feed_wheat = 2` on the $3,000 opening stake went bankrupt
# ($7 banked, 5 FEEDs a season against the leaders' 319). That is one point in the space, not a verdict
# on the space -- the herd size, the stocking day and the feed reserve are exactly what the search is
# for, and it will find that a big herd on a small stake starves. Gating the genes off because one
# hand-picked setting failed would have hidden the search's own answer.
LIVESTOCK_ENABLED = True


def uniform_probs():
    """The initial CEM distribution: uniform over every gene's categories.

    Deliberately uninformed. Seeding it from the heuristic would reintroduce exactly the prior the
    search exists to escape.
    """
    k = int(N_CATS.max())
    probs = np.zeros((N_GENES, k))
    for i, cats in enumerate(N_CATS):
        probs[i, :cats] = 1.0 / cats
    if not LIVESTOCK_ENABLED:
        # Zero the structure categories and every non-zero herd level, then renormalise. The genes
        # still exist and still decode -- they are simply never drawn, so tonight's run searches the
        # same crop-only space that produced $42,087 rather than exploring a half the executor cannot
        # yet keep alive. See the flag's comment for the measurement.
        lo, hi = _OFFSETS["crop_of"]
        probs[lo:hi, CROP_GENE_COOP] = 0.0
        probs[lo:hi, CROP_GENE_PASTURE] = 0.0
        for name in ("herd", "stock_day", "feed_wheat", "fert_policy"):
            a, b = _OFFSETS[name]
            probs[a:b, :] = 0.0
            probs[a:b, 0] = 1.0
        probs[lo:hi] /= probs[lo:hi].sum(axis=1, keepdims=True)
    return probs


def leaders_genome():
    """The plan the top of the leaderboard actually runs, encoded as a genome.

    Measured from replay JSON in `docs/episode_teardown_2026-08-03.md`, not guessed.
    `Dmitry Larko` (#1), `IY` (#4) and `Juste Me` (#5) submit byte-identical integers:

        14 BUILD_PASTURE, 0 BUILD_COOP
        seeds  MELON 21   STRAWBERRY 44   WHEAT 66
        animals COW 8   SHEEP 6   GOOSE 0
        306 hires over 30 days (~12 hands rebuilt every dawn), 2 land, 967 wheat bought as feed
        cows from day 0; land on days 7 and 10

    **This is a starting point for search, not an answer.** The whole reason to have it is that CEM
    around a known-good plan beats CEM from uniform: we already know these numbers work, so the
    question is only whether better ones exist nearby.

    The *spatial* layout is ours, not theirs -- the counts are measured but which tile holds what is
    not extracted yet, so pastures go nearest the shed and the crops fill outward in serpentine order.
    CEM will move them.
    """
    g = np.zeros(N_GENES, dtype=np.int64)

    use = np.zeros(TILES, dtype=np.int64)
    use[:14] = CROP_GENE_PASTURE
    use[14:35] = 5                                    # gene 5 -> MELON  (21 tiles)
    use[35:79] = 4                                    # gene 4 -> STRAWBERRY (44 tiles)
    lo, hi = _OFFSETS["crop_of"]
    g[lo:hi] = use

    def put(name, value):
        a, b = _OFFSETS[name]
        g[a:b] = value

    put("phase", 0)
    put("stop_plant", int(np.argmin(np.abs(STOP_PLANT_DAYS - 20))))
    put("harvest_par", 2)                             # HARVEST_DELTA 0: cut at max_yield_day
    put("hires", int(np.argmin(np.abs(HIRE_LEVELS - 12))))
    put("sell_every", int(np.argmin(np.abs(SELL_EVERY - 2))))
    put("floor_frac", 1)                              # 0.3 of base: sell unless the price collapses
    put("seed_reserve", 1)                            # keep $200 back
    put("dump_day", int(np.argmin(np.abs(DUMP_DAYS - 26))))
    put("herd", 0)
    put("stock_day", 0)                               # cows on day 0, as measured
    put("feed_wheat", int(np.argmin(np.abs(FEED_WHEAT - 2))))
    put("fert_policy", FERT_APPLY_THEN_SELL)

    a, b = _OFFSETS["herd"]
    g[a] = 0                                          # GOOSE 0
    g[a + 1] = herd_gene(8)                           # COW 8
    g[a + 2] = herd_gene(6)                           # SHEEP 6

    a, b = _OFFSETS["land_day"]
    g[a] = int(np.argmin(np.abs(LAND_DAYS - 6)))      # first extra quadrant ~day 7
    g[a + 1] = int(np.argmin(np.abs(LAND_DAYS - 9)))  # second ~day 10
    g[a + 2] = len(LAND_DAYS) - 1                     # NEVER

    a, b = _OFFSETS["sell_qty"]
    g[a:b] = 3                                        # SELL_QTYS 10 per tick per product per block
    return g


def probs_around(genome, concentration=0.55):
    """A CEM start distribution centred on `genome`, with the rest spread over the alternatives.

    `concentration` is the probability mass on the seeded category; the remainder is uniform over the
    others so every value stays reachable. This is the difference between "search from scratch" and
    "search around what we know works" -- `uniform_probs` throws away the only measurement we have of
    a plan that banks $100k+.

    Deliberately not 1.0. A point start collapses CEM's first generation to one plan and it can only
    walk downhill from there; `CLAUDE.md` records the winner's curse biting at +40% reported against
    +12.8% held out, and keeping mass on the alternatives is what leaves room to escape it.
    """
    g = np.asarray(pad_genome(genome), dtype=np.int64)
    k = int(N_CATS.max())
    probs = np.zeros((N_GENES, k))
    for i, cats in enumerate(N_CATS):
        cats = int(cats)
        if cats == 1:
            probs[i, 0] = 1.0
            continue
        rest = (1.0 - concentration) / (cats - 1)
        probs[i, :cats] = rest
        probs[i, int(g[i])] = concentration
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
    # **Structures are counted, not folded into FALLOW.** A pasture tile decodes to `crop_of == FALLOW`
    # by design, so the first version of this reported 14 pastures as "FALLOW=35" and never mentioned
    # the herd at all -- a livestock plan and a crop plan printed identically. Third instance today of
    # a census dropping a column and the zero being read as a fact.
    counts = {}
    for c, st in zip(plan.crop_of[0], plan.structure_of[0]):
        if st == COOP:
            name = "COOP"
        elif st == PASTURE:
            name = "PASTURE"
        else:
            name = "FALLOW" if c < 0 else CROP_NAMES[c]
        counts[name] = counts.get(name, 0) + 1
    lines.append("tiles: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    herd = ", ".join(f"{n} {int(v)}" for n, v in zip(ANIMAL_NAMES, plan.herd[0]) if v)
    fert = ["sell", "apply", "apply then sell"][int(plan.fert_policy[0])]
    lines.append(f"herd: {herd or 'none'} | stock from day {int(plan.stock_day[0])}"
                 f" | feed {int(plan.feed_wheat[0])} wheat/animal | fertiliser: {fert}")
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
