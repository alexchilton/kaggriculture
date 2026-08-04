"""A season as a bag of chain instances: the search space the routines were built to serve.

`routines.py` gives us two chain builders and argues why they are the right atom -- a partial chain
cannot be expressed, so the money-negative valley in front of the animal economy is not crossed, it is
absent. What it never had was something that *chooses* chains. This module is that: a fixed-length
genome where each slot is one chain instance, and a decoder that turns a genome into a 720-turn tape.

**One chain per unit, and that is what makes the decode safe.** A unit's position is the cumulative sum
of its movement ops, so two chains sharing a unit would interleave their walks and both would end up
somewhere neither intended -- silently, because a blocked move is a no-op rather than an error. Slot `i`
owns unit `i` outright. That also prices the genome honestly: unit `i` means hiring `i` hands every
dawn, and `HIRE_COST` is Fibonacci in the day's hire count, so slot 9 is expensive in a way slot 2 is
not. The search sees that cost in the score without being told about it.

**Blocks, not tiles.** A slot picks a pre-cut block of adjacent tiles rather than a raw tile, for two
reasons. It keeps the genome small enough for a categorical CEM, and it keeps the per-day walk short --
the turn budget is 24 and a scattered block spends all of it moving. Blocks are cut in serpentine order
and every one is validated at import to fit inside a day, so an unfittable block cannot be proposed.

**Allocation is capacity-matched, and that is measurable rather than a matter of taste.**
`data/logs/market_ceiling.log` puts melon's whole-season town drain at 140 units against strawberry's
572, and `data/logs/crop_pays.log` measures a melon tile at +$3,182 against strawberry's +$803. Melon
therefore looks four times better per tile and saturates after roughly eleven tiles, at which point the
twelfth sells at the price floor. The leaders plant exactly 11 melon and 40 strawberry. `DRAIN_UNITS`
below records that ceiling so a seeded genome can start there instead of rediscovering it.
"""

import numpy as np

from kagg.search import routines as R

# Whole-season town drain per product, from `kagg/economics/market.py`'s schedule as measured in
# `data/logs/market_ceiling.log`. This is the number of units the town removes, i.e. how much can be
# sold before inventory gluts and the price collapses toward the floor.
DRAIN_UNITS = {"WHEAT": 662, "CARROT": 338, "TOMATO": 374, "STRAWBERRY": 572, "MELON": 140}

BLOCK_SIZE = 4
START_DAY_CHOICES = (0, 1, 2, 3, 5, 8, 12)
LAND_DAY_CHOICES = (0, 4, 8, 12, 16, 99)      # 99 == never; a chain outside NW then simply no-ops
KINDS = ("off", "grow", "ranch")


def _quadrant_tiles(quadrant):
    half = R.BOARD_SIZE // 2
    xs = range(0, half) if quadrant.endswith("W") else range(half, R.BOARD_SIZE)
    ys = range(0, half) if quadrant.startswith("N") else range(half, R.BOARD_SIZE)
    return [(x, y) for y in ys for x in xs]


def _cut_blocks():
    """Pre-cut blocks of adjacent tiles, nearest quadrant first, shed-access tiles reserved.

    The four shed-access tiles are excluded because `ranch()` needs them: a pen on one of those runs
    its whole loop with no movement at all, which is the property that makes an animal chain safe.
    Spending them on crops would force every animal to walk and reintroduce exactly the coupling
    `routines.py` was written to avoid.
    """
    reserved = set(R.shed_access_tiles())
    blocks = []
    for quadrant in ("NW", "NE", "SW", "SE"):
        tiles = [t for t in R.serpentine(_quadrant_tiles(quadrant)) if t not in reserved]
        for i in range(0, len(tiles) - BLOCK_SIZE + 1, BLOCK_SIZE):
            blocks.append(tuple(tiles[i:i + BLOCK_SIZE]))
    return tuple(blocks)


def _fits_in_a_day(block):
    """Whether `grow()` can work `block` inside 24 turns. Cheaper to check once than to catch later."""
    try:
        R.grow(R.Script(T=R.TURNS_PER_DAY * 2), "WHEAT", list(block), plant_day=0)
        return True
    except ValueError:
        return False


ALL_BLOCKS = _cut_blocks()
BLOCKS = tuple(b for b in ALL_BLOCKS if _fits_in_a_day(b))
# Recorded rather than silently dropped: a block excluded here is board the search cannot reach, and
# `scripts/search_chains.py` prints the count so shrinking coverage is visible.
UNREACHABLE_BLOCKS = tuple(b for b in ALL_BLOCKS if b not in BLOCKS)

RANCH_CELLS = tuple(R.shed_access_tiles())

OPENING_BANK = 3000                 # `kaggriculture.py:237` startingMoney


def land_cost(tile):
    """What unlocking `tile`'s quadrant costs in total, since parcels are bought in a fixed order."""
    return sum(R.LAND_PRICES[:R.land_purchases_for(tile)])


SEED_COST = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}


# Blocks and cells the farm already owns at spawn. The seed stays inside these: land is bought out of
# working capital and working capital is what binds -- the first parcel alone is a third of the opening
# bank, before a single seed. The *search* is not restricted; it owns `land_day` and buying SE late is a
# strategy it is free to find.
OWNED_BLOCKS = tuple(b for b in BLOCKS if max(land_cost(t) for t in b) == 0)
OWNED_CELLS = tuple(c for c in RANCH_CELLS if land_cost(c) == 0)

# Genome layout: one row per slot, five categorical genes per row.
GENES = ("kind", "what", "block", "start_day", "land_day")
N_KINDS = len(KINDS)
N_WHAT = max(len(R.CROPS), len(R.ANIMAL_NAMES))
GENE_SIZES = (N_KINDS, N_WHAT, max(len(BLOCKS), len(RANCH_CELLS)), len(START_DAY_CHOICES),
              len(LAND_DAY_CHOICES))


def n_genes(n_slots):
    return n_slots * len(GENES)


def decode(genome, n_slots):
    """Genome -> `Script`. Slot `i` owns unit `i`; an over-budget or illegal slot is skipped.

    Skipping rather than raising is deliberate and mirrors the argument `script_mutate.py` makes: an
    unusable proposal should score worse, not crash the search. But it is *counted* and returned, so a
    genome that is mostly unusable is visible as such instead of quietly reading as a weak strategy.
    """
    g = np.asarray(genome, dtype=np.int64).reshape(n_slots, len(GENES))
    script = R.Script()
    used, skipped = [], 0

    for slot in range(n_slots):
        kind = KINDS[int(g[slot, 0]) % N_KINDS]
        if kind == "off":
            continue
        what_i, block_i, start_i, land_i = (int(x) for x in g[slot, 1:])
        start_day = START_DAY_CHOICES[start_i % len(START_DAY_CHOICES)]
        land_day = LAND_DAY_CHOICES[land_i % len(LAND_DAY_CHOICES)]
        try:
            if kind == "ranch":
                cell = RANCH_CELLS[block_i % len(RANCH_CELLS)]
                animal = R.ANIMAL_NAMES[what_i % len(R.ANIMAL_NAMES)]
                # `ranch()` derives its own unit from the cell -- the pen must be worked by whoever
                # spawns on it -- so the slot index does not choose the unit here.
                R.ranch(script, animal=animal, tile=cell, start_day=start_day, land_day=land_day)
                used.append(("ranch", animal, cell, start_day))
            else:
                block = BLOCKS[block_i % len(BLOCKS)]
                crop = R.CROPS[what_i % len(R.CROPS)]
                R.grow(script, crop, list(block), plant_day=start_day, land_day=land_day, unit=slot)
                used.append(("grow", crop, block, start_day))
        except ValueError:
            skipped += 1
    return script, used, skipped


def seeded_genome(n_slots, rng=None):
    """A genome at the leaders' measured allocation, as CEM's starting point rather than uniform noise.

    Their season, extracted in `docs/`: 14 pens (8 cow, 6 sheep), strawberry 40 tiles, melon 11, wheat
    10, two land parcels bought around days 6 and 9, crew ramping 5 -> 13 rather than flat. Only four
    ranch cells exist here, so the animal count is necessarily smaller than theirs -- the point of the
    seed is the *shape* (animals first, melon capped near its drain, strawberry bulk), not a copy.

    **The first version of this was worse than an empty tape**: it banked $0 against $3,000 for a farm
    that does nothing, because it bought four animals on day 0 with `land_day=8`. Three of the four pens
    stood on land the farm did not own, `PLACE` failed silently on a LOCKED tile, and the feed and crew
    were paid for thirty days of nothing. Two rules come out of that, and `tests/test_seeded_genome.py`
    pins both:

    - **A ranch cell's land must be unlocked before its animal is bought**, so `land_day <= start_day`.
    - **At most one parcel before the farm has earned anything.** The second costs $2,000 of a $3,000
      bank, and the season is decided by working capital -- see `data/logs/sell_timing_sweep.log`.

    The measured cause of the $0 was **over-commitment, not ordering**. Day 0 spent $1,853 on two cows
    and a parcel; day 1 then asked for 12 melon at $80 and 12 strawberry at $100, $2,160 against $1,147.
    The atomic PLANT rule drops *every* request for a crop when demand exceeds seeds held, so the farm
    bought nothing, planted nothing, and starved the animals it had already paid for.

    So the seed is staged by **cash flow**, which is what the crop table actually rewards:

    - Wheat first. $10 a seed, harvestable at age 2 and topping out at age 4, so it is the only crop
      that returns money inside the first week -- and `ranch()` buys wheat as feed every day regardless,
      so growing it also removes a purchase.
    - Melon next, capped near its 140-unit town drain (`data/logs/market_ceiling.log`), at $80 a seed
      the best per-tile crop measured (+$3,182 in `data/logs/crop_pays.log`).
    - Strawberry last. $100 a seed for a first harvest at age 10 is the biggest hole in the season and
      wants to be dug once there is revenue to dig it with.

    One animal, on the free cell. A ranch slot's unit is derived from its cell, so slot `i` must hold
    cell `i` or two chains collide on one unit and interleave their walks.
    """
    rng = rng or np.random.default_rng(0)
    g = np.zeros((n_slots, len(GENES)), dtype=np.int64)
    melon_blocks = max(1, round(DRAIN_UNITS["MELON"] / (12 * BLOCK_SIZE)))

    # (kind, what, start_day). Every entry is affordable at the bank the entries before it leave behind.
    plan = [("ranch", "COW", 0), ("grow", "WHEAT", 0), ("grow", "WHEAT", 0)]
    plan += [("grow", "MELON", 2)] * melon_blocks
    plan += [("grow", "STRAWBERRY", d) for d in (5, 8, 12)]
    plan += [("grow", "WHEAT", 3)] * n_slots           # pad: cheap, and it feeds the animals

    block_cursor = 0
    for slot in range(n_slots):
        kind, what, start_day = plan[slot]
        if kind == "grow" and block_cursor >= len(OWNED_BLOCKS):
            break                                     # out of land we own; leave the rest "off"
        g[slot, 0] = KINDS.index(kind)
        if kind == "ranch":
            g[slot, 1] = R.ANIMAL_NAMES.index(what)
            g[slot, 2] = RANCH_CELLS.index(OWNED_CELLS[slot % len(OWNED_CELLS)])
        else:
            g[slot, 1] = R.CROPS.index(what)
            g[slot, 2] = BLOCKS.index(OWNED_BLOCKS[block_cursor])
            block_cursor += 1
        g[slot, 3] = START_DAY_CHOICES.index(start_day)
        g[slot, 4] = LAND_DAY_CHOICES.index(0)         # nothing here needs land; 0 is a no-op
    return g.reshape(-1)
