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

# **Every day, not a grid.** These were coarse -- `(0, 1, 2, 3, 5, 8, 12)` and `(0, 4, 8, 12, 16, 99)`
# -- purely so `search_chains.py`'s uniform categorical had fewer bins to converge over. Nothing else
# depended on it, and the beam enumerates rather than sampling, so it paid the restriction and got
# nothing back. It was also provably too coarse to describe the target: the leader tape buys land on
# **days 7 and 10** (`data/seed_scripts/replay_89873723_seat0.npz`, turns 169 and 260), and neither
# day existed on the old grid. A search that cannot express the winner's move cannot find it.
#
# The cost lands on the CEM, which now samples 30 bins per day-gene instead of 6 or 7 and needs more
# draws for the same convergence. It saturates by generation 10 of 30, so it has the headroom.
#
# **Widening repoints every saved genome.** `decode` reads these by index, so an old index 6 meant
# day 12 under the old tuple and means day 6 now. Any `.npz` written before this commit must be
# re-run, not reloaded -- the same hazard `plan.py` records for `best_plan.json`.
START_DAY_CHOICES = tuple(range(R.SEASON_DAYS))
LAND_DAY_CHOICES = tuple(range(R.SEASON_DAYS)) + (99,)  # 99 == never; a chain outside NW then no-ops
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

# Where a pen may stand. The four shed cells come **first** so their indices stay small and stable,
# and because they are strictly cheaper: a pen there runs its whole day without a movement op, while
# anywhere else pays the walk out and back in turns and cannot DROP.
#
# Everything after them is one tile per crop block, which is the whole of the rest of the board at
# block granularity. `ranch()` refused to leave the shed until 2026-08-04, so the herd was capped at
# four against the leader tape's **14** -- and really at two, because cells three and four need
# $3,000 and $7,000 of land against a $3,000 opening bank. Re-using the `block` gene rather than
# adding a fifth means the beam's slot-to-cell binding disappears too: any slot can now propose a pen
# anywhere, where before `catalog()` offered slot `k` only cell `k`.
RANCH_TILES = RANCH_CELLS + tuple(b[0] for b in BLOCKS)

OPENING_BANK = 3000                 # `kaggriculture.py:237` startingMoney

# The first day a farm can possibly have sold anything. Wheat is the fastest crop: planted on day 0 it
# is harvestable at age 2, the harvest sits in `carried` until the dusk auto-drop, and the sell order
# therefore lands on day 3's market. Before that, the opening bank is the whole of the farm's money and
# any land ordered has to fit inside it.
EARLIEST_REVENUE_DAY = 3


def working_units(n):
    """The first `n` unit indices that can actually do anything, in cost order.

    Hands fill the four shed-access tiles in NWSE order and the cycle repeats every four, so units 3,
    7, 11 ... wake on `(5,5)` in SE. Both of that tile's neighbours are locked until the farm owns SE,
    which costs all three parcels -- **$7,000** against a $3,000 opening bank -- and `ops.py:86`
    ignores a move onto locked ground without complaint. The leader tape buys two parcels and never
    buys SE, and neither has any plan our search has found, so those units are inert for the season.

    Measured on one identical melon block, changing only the unit: $15,575 / $15,545 / $15,515 for
    units 0-2 against **$1,920** for unit 3, and $15,365 / $15,215 / $14,975 against **$1,050** for
    unit 7. Mapping slot `k` to unit `k` therefore threw away two of every eight slots while still
    paying to hire them.

    Skipping costs hires and the cost is small: hands are re-hired every dawn on a Fibonacci ladder
    that resets daily, so reaching unit 9 rather than unit 7 is a few dollars a day.
    """
    out, u = [], 0
    while len(out) < n:
        if R.spawn_tile(u) != tuple(R.shed_access_tiles()[3]):
            out.append(u)
        u += 1
    return out


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

# Genome layout: one row per slot, six categorical genes per row.
#
# **`fertilize` was added on 2026-08-04 and it changes the row stride, so every genome saved before
# that date is unreadable at this layout** -- the same repointing the `start_day`/`land_day` grids
# caused, but worse, because a wrong stride silently reinterprets *all* five other genes rather than
# shifting one. Re-run the search rather than loading an old `.npz`.
#
# Fertilizer is a per-chain choice and not a global switch because it is worthless on exactly the
# crop the beam likes most. Measured season yield per tile, plain -> fertilized: strawberry 6 -> 12
# and tomato 8 -> 16 both double, wheat 28 -> 42, carrot 29 -> 39, and **melon 12 -> 12**. A blanket
# "fertilize everything" would spend a turn a day per tile on melon for nothing, so `grow()` also
# refuses melon outright via `FERTILIZER_HELPS`, derived from `production.py` rather than restated.
# `fert_trade` is the one gene whose meaning depends on the chain's kind, because the two sides of the
# same decision live in different routines. On a `grow` chain it is `buy_fertilizer`: pay ~$100 a unit
# to dose a crop. On a `ranch` chain it is `sell_fertilizer`: offer the herd's free output to a market
# where FERTILIZER is 23.1% of winner sales. Those are rival uses of one good and the farm was doing
# both blindly -- pens dumping every unit they collected while crop chains bought units back off the
# same market, paying the spread twice. Measured on one block, selling beat applying about 6:1, but
# that was one 4-tile block with two cows and it is exactly the kind of narrow measurement this
# project has been burned by, so the search owns the choice rather than inheriting my answer.
GENES = ("kind", "what", "block", "start_day", "land_day", "fertilize", "fert_trade")
N_KINDS = len(KINDS)
N_WHAT = max(len(R.CROPS), len(R.ANIMAL_NAMES))
GENE_SIZES = (N_KINDS, N_WHAT, max(len(BLOCKS), len(RANCH_TILES)), len(START_DAY_CHOICES),
              len(LAND_DAY_CHOICES), 2, 2)


def n_genes(n_slots):
    return n_slots * len(GENES)


def reachable_quadrants(genome, n_slots):
    """Which quadrants the farm will actually own, given what its own chains order and when.

    Land is bought in the fixed order NE -> SW -> SE at $1,000 / $2,000 / $4,000, and `_do_buy_land`
    **silently no-ops when money is short** rather than refusing the plan. So a genome ordering all
    three parcels on day 0 against a $3,000 bank gets two of them and no error, and the chains aimed
    at the third walk until a LOCKED tile stops them and build wherever they land -- the farm is real,
    the money is real, and the reported plan is fiction (`tests/test_locked_chain_relocates.py`).

    This is a deliberately *pessimistic* estimate and only counts what the opening bank can cover
    before anything is earned. It is not a cash-flow model: revenue genuinely does fund later parcels,
    which is why the leader buys on days 7 and 10 and why waiting is worth up to +$22,911 here
    (`data/logs/land_day7.log`). Ordering a parcel out of *future* revenue is a legitimate strategy,
    so a chain is only skipped when its ground could not be bought on the day it is ordered even with
    the whole opening bank -- which is exactly the day-0 triple-buy that has been distorting results.
    """
    g = np.asarray(genome, dtype=np.int64).reshape(n_slots, len(GENES))
    orders = []                      # (day, parcels_needed) per chain that wants land
    for slot in range(n_slots):
        if KINDS[int(g[slot, 0]) % N_KINDS] == "off":
            continue
        kind = KINDS[int(g[slot, 0]) % N_KINDS]
        block_i = int(g[slot, 2])
        tile = (RANCH_TILES[block_i % len(RANCH_TILES)] if kind == "ranch"
                else BLOCKS[block_i % len(BLOCKS)][0])
        need = R.land_purchases_for(tile)
        if need:
            orders.append((LAND_DAY_CHOICES[int(g[slot, 4]) % len(LAND_DAY_CHOICES)], need))
    if not orders:
        return 0
    # The earliest day by which each parcel index is ordered. `ranch()`/`grow()` space their own
    # parcels one per day from `land_day`, so chain k's j-th parcel is ordered on `land_day + j`.
    first_order = {}
    for day, need in orders:
        for j in range(need):
            first_order[j] = min(first_order.get(j, 10**6), day + j)
    bought, spent = 0, 0
    for j in sorted(first_order):
        spent += R.LAND_PRICES[j]
        # Nothing has been earned before `EARLIEST_REVENUE_DAY`, so parcels ordered that early are
        # judged against the opening bank alone. Later ones are allowed through: revenue really does
        # fund them, and judging *those* against the opening bank is what made the search believe day
        # 0 was optimal when waiting is worth up to +$22,911.
        if first_order[j] < EARLIEST_REVENUE_DAY and spent > OPENING_BANK:
            break
        bought = j + 1
    return bought


def decode(genome, n_slots):
    """Genome -> `Script`. Slot `i` drives `working_units(n_slots)[i]`; an unusable slot is skipped.

    Skipping rather than raising is deliberate and mirrors the argument `script_mutate.py` makes: an
    unusable proposal should score worse, not crash the search. But it is *counted* and returned, so a
    genome that is mostly unusable is visible as such instead of quietly reading as a weak strategy.
    """
    g = np.asarray(genome, dtype=np.int64).reshape(n_slots, len(GENES))
    script = R.Script()
    used, skipped = [], 0
    # Slot -> unit, skipping the SE spawns that cannot move without the $7,000 parcel. See
    # `working_units`; this used to be the identity and threw away two of every eight slots.
    units = working_units(n_slots)
    # How much land this genome can really afford on the day it orders it. A chain standing on ground
    # beyond that is skipped and counted, rather than silently relocating.
    affordable = reachable_quadrants(genome, n_slots)

    for slot in range(n_slots):
        kind = KINDS[int(g[slot, 0]) % N_KINDS]
        if kind == "off":
            continue
        what_i, block_i, start_i, land_i, fert_i, trade_i = (int(x) for x in g[slot, 1:])
        start_day = START_DAY_CHOICES[start_i % len(START_DAY_CHOICES)]
        land_day = LAND_DAY_CHOICES[land_i % len(LAND_DAY_CHOICES)]
        tile = (RANCH_TILES[block_i % len(RANCH_TILES)] if kind == "ranch"
                else BLOCKS[block_i % len(BLOCKS)][0])
        if R.land_purchases_for(tile) > affordable:
            # The ground cannot be bought on the day this chain orders it. Emitting the chain anyway
            # is what produced a genome claiming pens on (7,8), (2,8) and (6,9) while the animals
            # ended up on (7,4), (2,4) and (6,4): the walk stops at the locked border and BUILD fires
            # there. Skipping is counted, so an unaffordable genome reads as unaffordable.
            skipped += 1
            continue
        try:
            if kind == "ranch":
                cell = tile
                animal = R.ANIMAL_NAMES[what_i % len(R.ANIMAL_NAMES)]
                # A shed cell must be worked by whoever wakes on it, or the pen walks for no reason,
                # so `ranch()` picks the unit there. A pen anywhere else takes the slot's own unit --
                # otherwise every remote pen would collide on unit 0 and interleave its walks.
                R.ranch(script, animal=animal, tile=cell, start_day=start_day, land_day=land_day,
                        unit=None if cell in RANCH_CELLS else units[slot],
                        sell_fertilizer=bool(trade_i % 2))
                used.append(("ranch", animal, cell, start_day))
            else:
                block = BLOCKS[block_i % len(BLOCKS)]
                crop = R.CROPS[what_i % len(R.CROPS)]
                R.grow(script, crop, list(block), plant_day=start_day, land_day=land_day,
                       unit=units[slot], fertilize=bool(fert_i % 2),
                       buy_fertilizer=bool(trade_i % 2))
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
            g[slot, 2] = RANCH_TILES.index(OWNED_CELLS[slot % len(OWNED_CELLS)])
        else:
            g[slot, 1] = R.CROPS.index(what)
            g[slot, 2] = BLOCKS.index(OWNED_BLOCKS[block_cursor])
            block_cursor += 1
        g[slot, 3] = START_DAY_CHOICES.index(start_day)
        g[slot, 4] = LAND_DAY_CHOICES.index(0)         # nothing here needs land; 0 is a no-op
    return g.reshape(-1)
