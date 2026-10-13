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
#
# **The animal products were missing until 2026-08-05, and they are half the game.** This dict held the
# five crops only, so $151,750 of demand -- including MILK, the single largest market at $78,432 -- was
# invisible to every allocation argument the project has made. With them in, the ranking is:
#
#     MILK   500 x 160 = $78,432      <- the biggest market in the game
#     STRAW  572 x 120 = $66,586
#     WOOL   284 x 200 = $56,736
#     MELON  140 x 250 = $35,000
#     TOMATO 374 x  60 = $21,574
#     EGG    338 x  50 = $16,582
#     WHEAT  662 x  25 = $15,986      <- seventh of eight, and yet the leader plants 40 tiles of it
#     CARROT 338 x  35 = $11,484
#                        $302,380 total
#
# That immediately explains the leader's farm, and `scripts/allocation_calculator.py` reproduces it:
# a cow yields 66 milk a season so 7.6 cows fill the drain -- **he runs 8**; a sheep yields 48 wool so
# 5.9 fill it -- **he runs 6**; and geese are the worst pen into the smallest animal market, so he runs
# none. The herd is not a strategy to be searched, it is drain divided by yield.
#
# Wheat is the exception that proves the rule. Its own market is nearly worthless, seventh of eight,
# and he plants 40 tiles anyway -- because it is an **input**: 14 pens eat ~420 units a season, $10,500
# of feed, and wheat is the only crop that returns cash by day 3 to fund the day-7 land. A revenue
# ranking scores it last; it belongs in the plan on cost avoidance and cash timing.
#: Highest unit index a chain may be assigned. The hire ladder makes anything past the high
#: teens self-defeating, so this is a backstop rather than a target.
MAX_UNITS = 20

# **Re-measured 2026-08-08 against 1.32.6, the version the ladder actually runs.** The numbers
# above are 1.32.2's and are kept because the *argument* they support still holds -- milk is the
# biggest market, wheat is an input rather than a crop -- but every figure in them is too large.
#
# The machine had `kaggle-environments` 1.32.2 installed while the competition moved to 1.32.6, so
# every fixture in this project was measured on a different game from the one it plays.
# 1.32.6 doubles `townCenterSellInterval` 12 -> 24 and deletes `TOWN_CENTER_DEMAND_SCHEDULE`, the
# ramp that multiplied centre demand x2 from day 10 and x4 from day 20. Against the real
# environment the whole market is **$204,379, not $302,380** -- the planner was sizing the farm
# against a market 40% bigger than the one that exists:
#
#     product     1.32.2   1.32.6   over      $ 1.32.6
#     STRAWBERRY     572      452   1.27x       54,225
#     MILK           500      322   1.55x       51,510
#     WOOL           284      204   1.39x       40,875
#     WHEAT          662      553   1.20x       13,814
#     EGG            338      256   1.32x       12,778
#     TOMATO         374      209   1.79x       12,566
#     CARROT         338      317   1.06x       11,110
#     MELON          140       30   4.67x        7,500
#
# **Melon is the row that matters and it is exact.** No shop carries melon, so the town centre is
# its only buyer: 719 playable steps at one tick per 24 turns is 30 units a season, on every seed,
# with zero variance. The old 140 was 60 ticks ramped 1/2/4 -- three separate 1.32.2 facts
# compounding. The tape we ship sells 96 of them and we sell ~110, which is why melon quotes at the
# price floor for most of the season: the book takes 30 and never recovers the rest.
#
# **Every other row is a mean over a distribution, and the spread is wide.** 1.32.6 draws shops
# *with replacement* up to `MAX_SHOP_INSTANCES = 8`, so a product served by a repeated shop drains
# twice as fast: over seeds 1000-1031 wool ranges 30 to 678 and carrot 30 to 894. A single number
# cannot express that, and sizing production to the mean is a bet on the draw. Left as a mean here
# because that is what this table's callers expect; making the planner read the *live* unlock set
# is the honest fix and is not attempted in this change.
#
# Regenerate with `PYTHONPATH=. python3 -u scripts/drain_table.py --seeds 32`, which prints the
# replacement dict. Pinned by `tests/test_the_drain_table_matches_the_environment.py`.
DRAIN_UNITS = {"WHEAT": 553, "CARROT": 317, "TOMATO": 209, "STRAWBERRY": 452, "MELON": 30,
               "EGG": 256, "MILK": 322, "WOOL": 204}

# **Two block sizes, because how often a tile is watered decides how many a unit can hold.**
# Watering every tile every day costs ~3 turns per tile, so a 24-turn day fits four and six raises.
# Visiting half the tiles each day is legal -- death needs two *consecutive* dry days and base
# production never tests watering -- and holds eight. See `routines.grow`'s `water_every`.
#
# Both are cut, because neither dominates: strawberry gains +52% on eight alternate-day tiles while
# melon loses 28% (its one-shot harvest window shuts at max_day 12 and a missed visit forfeits it).
# **Three sizes, because pens leave gaps that only a small block can fill.** Widening the cut to every
# window was not enough on its own: the six tiles stranded on 2026-08-05 sat in three disjoint runs of
# *two* -- `{(2,0),(3,0)}`, `{(3,1),(2,1)}`, `{(0,2),(1,2)}` -- separated by the tiles the cow pens took,
# so no 4-tile window could span them. A pair block can.
#
# A 2-tile chain is expensive per tile: it costs a whole unit, and a unit costs hires. It exists for the
# gaps, and the search will only take it where two tiles are worth more than the hand that works them.
SMALL_BLOCK_SIZE = 2
BLOCK_SIZE = 4
WIDE_BLOCK_SIZE = 8

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


def _cut_blocks(size=BLOCK_SIZE):
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
        # **Every window, not every size-th one.** The stride used to be `size`, which made the block
        # set a disjoint *partition* -- and a partition strands tiles. A two-pen ranch takes 2 tiles out
        # of a 4-tile block and the other 2 become unreachable, because no block in the vocabulary
        # covers them. Measured on the best genome of 2026-08-05: 18 NW tiles worked, **6 stranded**
        # (`(0,2) (1,2) (2,0) (2,1) (3,0) (3,1)`), and two slots idle with nowhere legal to go.
        #
        # Overlapping blocks in the vocabulary are harmless now that `decode()` refuses a chain whose
        # ground is already claimed: a genome picking two overlapping blocks loses the later slot and
        # scores worse, so the search avoids it on its own.
        for i in range(0, len(tiles) - size + 1):
            blocks.append(tuple(tiles[i:i + size]))
    return tuple(blocks)


def _fits_in_a_day(block, water_every=1):
    """Whether `grow()` can work `block` inside 24 turns. Cheaper to check once than to catch later."""
    try:
        R.grow(R.Script(T=R.TURNS_PER_DAY * 3), "WHEAT", list(block), plant_day=0,
               water_every=water_every)
        return True
    except ValueError:
        return False


# Narrow blocks are worked daily; wide ones only alternate-day, which is the only cadence they fit in.
# `WATER_EVERY_FOR_BLOCK` records which is which so `decode()` never has to guess, and so a wide block
# can never be handed a daily chain that would raise.
SMALL_BLOCKS = tuple(b for b in _cut_blocks(SMALL_BLOCK_SIZE) if _fits_in_a_day(b, 1))
NARROW_BLOCKS = tuple(b for b in _cut_blocks(BLOCK_SIZE) if _fits_in_a_day(b, 1))
WIDE_BLOCKS = tuple(b for b in _cut_blocks(WIDE_BLOCK_SIZE) if _fits_in_a_day(b, 2))
ALL_BLOCKS = _cut_blocks(BLOCK_SIZE)
BLOCKS = SMALL_BLOCKS + NARROW_BLOCKS + WIDE_BLOCKS
WATER_EVERY_FOR_BLOCK = {b: 1 for b in SMALL_BLOCKS}
WATER_EVERY_FOR_BLOCK.update({b: 1 for b in NARROW_BLOCKS})
WATER_EVERY_FOR_BLOCK.update({b: 2 for b in WIDE_BLOCKS})
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


def _fits_a_pen_group(group):
    """Whether one unit can run every pen in `group` inside 24 turns, at any start day.

    Several start days, not one, because the feed cadence is indexed off `start_day`: which pens are
    fed on the peak day -- the last build day, when the chain has every earlier pen live *and* raises
    one more -- depends on the parity. A group validated only at day 0 raised at day 11 for a start
    day of 8, and `decode()` would have swallowed that as a skipped slot.
    """
    for start in (0, 1, 8, 9):
        try:
            R.ranch(R.Script(), "COW", list(group), start_day=start,
                    land_day=max(0, start - 4), unit=0)
        except ValueError:
            return False
    return True


def _cut_pen_groups():
    """Pens a single chain may hold: one unit, one slot, several animals.

    How many fit depends on the walk, so each candidate is validated rather than assumed -- the same
    approach `WIDE_BLOCKS` takes. A group near the shed fits four; the far NW corner is eight moves
    away and fits three.

    This is what breaks the herd/crop deadlock. One pen per chain meant five pens ate five of eight
    slots and left three for crops = 12 crop tiles, while strawberry alone is a $68,640 market needing
    ~48. Four pens on one chain frees three slots and cuts the hire bill, since fewer distinct units
    are needed at dawn.
    """
    # Singles first and for every tile a pen could previously stand on, so the multi-pen vocabulary
    # strictly *adds*: a lone remote pen was the whole of task #22 and must stay reachable.
    groups = [(c,) for c in RANCH_CELLS]
    groups += [(b[0],) for b in NARROW_BLOCKS + WIDE_BLOCKS]
    groups.append(tuple(RANCH_CELLS))             # the shed 2x2: no walk to the shed at all
    for block in NARROW_BLOCKS + WIDE_BLOCKS:
        for n in (4, 3, 2):
            if len(block) >= n:
                groups.append(tuple(block[:n]))
    seen, out = set(), []
    for g in groups:
        key = tuple(sorted(g))
        if key in seen:
            continue
        seen.add(key)
        if _fits_a_pen_group(g):
            out.append(g)
    return tuple(out)


RANCH_GROUPS = _cut_pen_groups()

# Opening seed cost per tile. Duplicated from `scheduler.SEED_COST` rather than imported, because
# `scheduler` imports this module and the cycle would not resolve. Pinned by the land-gate tests.
SEED_COST = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}

OPENING_BANK = 3000                 # `kaggriculture.py:237` startingMoney
C_OPENING_BANK = OPENING_BANK       # alias used by `_bank_estimate`, defined above its first use

# The first day a farm can possibly have sold anything. Wheat is the fastest crop: planted on day 0 it
# is harvestable at age 2, the harvest sits in `carried` until the dusk auto-drop, and the sell order
# therefore lands on day 3's market. Before that, the opening bank is the whole of the farm's money and
# any land ordered has to fit inside it.
EARLIEST_REVENUE_DAY = 3


def working_units(n):
    """Slot `k` drives unit `k`. Consecutive, because a skipped unit is a hand hired and left idle.

    **This used to skip units 3, 7, 11 ... and the reason given for it was false.** Those units wake on
    `(5,5)` in SE, and the docstring claimed "both of that tile's neighbours are locked until the farm
    owns SE, which costs all three parcels -- $7,000". `(4,5)` is indeed SW, but `(5,4)` is **NE, the
    first $1,000 parcel**, so one NORTH step gets the unit out. Measured turn by turn:

        turn  1: NORTH  at (5, 4)   <- NE, needs 1 parcel
        turn  5: EAST   at (7, 4)
        turn  8: PLANT  at (7, 2)
        turn  9: WATER  at (7, 2)

    and a full-season melon chain on an NE block emits 247 ops at 15 of the 23 work turns. The $1,920
    measurement that justified skipping was taken on a **NW** block, where unit 3 really must cross
    locked ground -- and that was generalised into "inert for the season".

    The cost of the skip was not "a few dollars a day", as the old docstring said. Hands are hired in
    sequence, so unit `k` is the `k`-th hire and reaching unit 14 means paying for hands 1-14. Skipping
    three of them inflates the hire count past a Fibonacci cliff:

        skipping:  12 slots -> max unit 14 -> 14 hands = $   986/day = $ 29,580/season
                   14 slots -> max unit 17 -> 17 hands = $ 4,180/day = $125,400/season
        consecutive: 12 slots -> 12 hands = $   376/day = $ 11,280/season
                     14 slots -> 14 hands = $   986/day = $ 29,580/season

    against the leader's **12 hands, all used**, $7,916 as actually ramped. $125,400 is more than he
    banks all season, and it is what made 14 chains unaffordable.

    A chain on an SE-spawn unit is still only worth placing on ground it can reach -- `decode()` refuses
    the unreachable combinations rather than letting the walk stop at a locked border and work the wrong
    tile, which is the silent no-op this project keeps paying for.
    """
    return list(range(n))


def unit_can_reach(unit, tile, parcels_owned):
    """Can `unit` walk from its spawn to `tile` across ground the farm owns?

    Movement onto a LOCKED tile is ignored without complaint (`ops.py:86`), so a chain whose walk crosses
    locked ground does not fail -- it stops short and does a whole season of work on whatever tile it is
    standing on. That is why an SE-spawn unit scored $1,920 on a NW block and got written off as inert,
    and why a replica of the leader's ramp emitted six crop chains and planted **zero** tiles.

    Two conditions, and the second is the subtle one:

    - the **target** must be owned, or there is nowhere legal to work;
    - the unit must be able to **leave its spawn**. A hand may wake on a LOCKED tile -- `spawn_order`
      does not filter for unlocked -- and PICKUP/DROP still work there since they test only
      shed-adjacency. Escaping needs one orthogonally adjacent tile that is owned.

    The shed cells are `(4,4) (5,4) (4,5) (5,5)`, so `(5,5)` touches `(5,4)` in NE and `(4,5)` in SW but
    **not** `(4,4)` diagonally. So an SE-spawn unit escapes as soon as NE (the first $1,000 parcel) is
    bought -- which is what the turn-by-turn showed, one NORTH step -- and is genuinely stuck before then.
    Requiring the *spawn* to be owned would restate the false belief this replaces.
    """
    spawn = tuple(R.spawn_tile(unit))
    if R.land_purchases_for(tuple(tile)) > parcels_owned:
        return False
    if R.land_purchases_for(spawn) <= parcels_owned:
        return True
    x, y = spawn
    return any(0 <= nx < R.BOARD_SIZE and 0 <= ny < R.BOARD_SIZE
               and R.land_purchases_for((nx, ny)) <= parcels_owned
               for nx, ny in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)))


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
# `feed_loop` is `fert_trade`'s mirror image, and the farm was making the same mistake in both
# directions: pens SOLD fertilizer while crops BOUGHT it, and crops SELL wheat while pens BUY it --
# paying the market spread twice on each. On a `ranch` chain this gene means "eat out of the shed
# instead of ordering feed"; on a `grow WHEAT` chain it means "hold the harvest for the herd". On any
# other crop it is ignored, since a melon chain that refuses to sell simply never earns.
# `water_every` is not a gene: it is a property of the *block*, since a wide block only fits a day at
# all on the alternate cadence and a narrow one gains nothing from it. Keeping it out of the genome
# avoids a whole axis of combinations that would decode to a raise. `WATER_EVERY_FOR_BLOCK` carries it.
GENES = ("kind", "what", "block", "start_day", "land_day", "fertilize", "fert_trade", "feed_loop")
N_KINDS = len(KINDS)
N_WHAT = max(len(R.CROPS), len(R.ANIMAL_NAMES))
GENE_SIZES = (N_KINDS, N_WHAT, max(len(BLOCKS), len(RANCH_GROUPS)), len(START_DAY_CHOICES),
              len(LAND_DAY_CHOICES), 2, 2, 2)


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
    g, first_order = _land_requests(genome, n_slots)
    if not first_order:
        return 0
    # What the chains themselves cost before any land: seeds for a first planting, animals per pen.
    # A gate that ignores this judged a $7,000 land plan the same as a $1,000 one.
    # Split by when the money is actually due: `upfront` is charged once, `per_day` accrues.
    upfront = 0.0
    per_day = 0.0
    max_unit = 0
    units = working_units(n_slots)
    for slot in range(n_slots):
        kind = KINDS[int(g[slot, 0]) % N_KINDS]
        if kind == "off":
            continue
        max_unit = max(max_unit, units[slot])
        block_i = int(g[slot, 2])
        if kind == "ranch":
            grp = RANCH_GROUPS[block_i % len(RANCH_GROUPS)]
            animal = R.ANIMAL_NAMES[int(g[slot, 1]) % len(R.ANIMAL_NAMES)]
            upfront += R.ANIMALS[animal]["cost"] * len(grp)
            # Feed, every other day. A standing bill, so it belongs in `per_day` -- a gate that priced
            # only the purchase let a herd look cheaper than it is, and one that charged the whole
            # season up front made every herd unaffordable.
            per_day += 25.0 * len(grp) / 2
        else:
            blk = BLOCKS[block_i % len(BLOCKS)]
            upfront += SEED_COST[R.CROPS[int(g[slot, 1]) % len(R.CROPS)]] * len(blk)
    # **Hires, which Alex is right to insist on.** Hands are dismissed and re-hired every dawn on a
    # Fibonacci ladder that resets daily, so the crew is a standing cost for the whole season and it
    # grows steeply: 6 hands is $20/day, 9 is $88, 12 is $376, 14 is $986. A genome reaching unit 14
    # owes $29,580 over thirty days before it plants anything, and a land gate blind to that would wave
    # through a farm whose crew alone outspends the parcels.
    if max_unit > 0:
        from kagg.sim.farm import HIRE_COST
        # Hires are re-paid every dawn, so this is a daily rate, not a season total. Steep: 6 hands is
        # $20/day, 9 is $88, 12 is $376, 14 is $986.
        per_day += float(np.asarray(HIRE_COST)[:max_unit].sum())

    # Walk the real curve where we can. `_affordable`'s straight line is kept only as the fallback for
    # callers without a full genome.
    curve = cash_curve(genome, n_slots)
    # The cheapest chain waiting on each parcel. **Land has to leave enough behind to plant on**, or the
    # farm buys ground it cannot use -- worse than not buying at all. $3,000 of parcels against a $3,000
    # bank passed a bare `spent <= curve[day]` check and then had nothing for the seed, which is how a
    # two-parcel plan bought one and silently relocated. Same rule as `scheduler.schedule`, so the gate
    # and the scheduler agree about what is affordable instead of disagreeing quietly.
    follow_on = {}
    for slot in range(n_slots):
        kind = KINDS[int(g[slot, 0]) % N_KINDS]
        if kind == "off":
            continue
        block_i = int(g[slot, 2])
        if kind == "ranch":
            grp = RANCH_GROUPS[block_i % len(RANCH_GROUPS)]
            cost = float(R.ANIMALS[R.ANIMAL_NAMES[int(g[slot, 1]) % len(R.ANIMAL_NAMES)]]["cost"])
        else:
            grp = BLOCKS[block_i % len(BLOCKS)]
            cost = float(SEED_COST[R.CROPS[int(g[slot, 1]) % len(R.CROPS)]] * len(grp))
        need_j = R.land_purchases_for(grp[0]) - 1
        if need_j >= 0:
            follow_on[need_j] = min(follow_on.get(need_j, cost), cost)

    bought, spent = 0, 0
    for j in sorted(first_order):
        spent += R.LAND_PRICES[j]
        day = min(first_order[j], R.SEASON_DAYS - 1)
        if spent + follow_on.get(j, 0.0) > curve[day]:
            break
        bought = j + 1
    return bought


def land_schedule(genome, n_slots):
    """`[day, ...]` -- one entry per parcel the farm should buy, in unlock order.

    A BUY_LAND order is a claim on a **shared, ordered** resource: `_do_buy_land` unlocks
    `LAND_ORDER[n_already_bought]` and ignores which quadrant the caller wanted. So the farm must
    order parcels once, centrally, and a chain's `land_day` is a *deadline* -- "my ground by day D" --
    not a private purchase.

    Letting each chain buy its own was correct only by accident. `ranch()` writes `buy_land[t] = 1` by
    assignment, so chains sharing a `land_day` collapsed onto the same turns and the count came out
    right. Give them different days -- which is the leader's actual shape, **NE day 7 and SW day 10** --
    and a pen on NE plus a pen on SW emitted orders on days 7, 10 and 11: three parcels for $7,000
    when two cost $3,000, the third being an SE the leader never buys.

    Parcel `j` is bought as soon as the earliest chain needing it asks, and never before parcel
    `j - 1`, since they unlock in sequence.
    """
    _g, first_order = _land_requests(genome, n_slots)
    days, prev = [], -1
    for j in sorted(first_order):
        # Never before the previous parcel, and never on the same day as it. Two parcels resolving in
        # one day are judged against one day's bank -- $1,000 + $2,000 against a $3,000 opening stake
        # is the double-buy that `test_land_orders_are_spaced.py` was written for, one level up.
        prev = max(prev + 1, first_order[j])
        days.append(prev)
    return days


def _land_requests(genome, n_slots):
    """`(gene rows, {parcel index: earliest day it is wanted})`."""
    g = np.asarray(genome, dtype=np.int64).reshape(n_slots, len(GENES))
    first_order = {}
    for slot in range(n_slots):
        kind = KINDS[int(g[slot, 0]) % N_KINDS]
        if kind == "off":
            continue
        block_i = int(g[slot, 2])
        tile = (RANCH_GROUPS[block_i % len(RANCH_GROUPS)][0] if kind == "ranch"
                else BLOCKS[block_i % len(BLOCKS)][0])
        need = R.land_purchases_for(tile)
        if not need:
            continue
        day = LAND_DAY_CHOICES[int(g[slot, 4]) % len(LAND_DAY_CHOICES)]
        for j in range(need):
            first_order[j] = min(first_order.get(j, 10 ** 6), day)
    return g, first_order


# A deliberately pessimistic estimate of what a farm has earned by a given day, used only to decide
# whether a land order can clear. It is not a revenue model -- the simulator is that -- it is a floor,
# so a plan that cannot pay even optimistically is refused.
#
# Grounded on the measured seasons rather than fitted: our farms sit between $200 and $1,200 for the
# first ten days and only pass $10,000 around day 12 (`data/logs/diff_vs_leader.log`), and the leader
# runs at $42-$1,700 for eleven days before compounding. So earnings before day 10 are worth very
# little, and a parcel bought early has to come from the opening bank whatever day it is ordered on.
EARN_PER_DAY_AFTER = 10          # the day compounding actually starts, from both measured seasons
EARN_RATE = 900.0                # $/day after that, floored well under the ~$2,500 we measure


def cash_curve(genome, n_slots, parcel_days=()):
    """Day-by-day bank estimate for a whole genome, respecting when money is actually due.

    Replaces a straight line through `EARN_RATE`, which was wrong in three ways at once and produced
    three different wrong answers on 2026-08-05: it charged the *whole season's* feed and hires on the day
    of a land order (nothing could ever buy land), then charged every chain's purchase cost regardless of
    when the chain starts (a plan whose pens go up on day 20 was judged as though it had bought them on
    day 3), and it credited revenue from a chain's start day rather than its first production day (two cow
    chains appeared to have earned $5,340 by day 3 when the real bank was $1,800, so land was bought on
    day 3 instead of the leader's day 7).

    This walks the days instead. A chain charges its purchase on its start day, its feed from then on, and
    earns nothing until `start + payback`. Crew is charged daily at the Fibonacci rate for the highest
    unit in play. Still an *estimate* -- the simulator is the judge -- but one whose errors are in the size
    of the revenue rather than in the timing of anything.
    """
    from kagg.sim.farm import HIRE_COST
    from kagg.economics import production as P

    hc = np.asarray(HIRE_COST)
    g = np.asarray(genome, dtype=np.int64).reshape(n_slots, len(GENES))
    units = working_units(n_slots)
    events = []                       # (day, one-off cost, per-day cost, earns_from, per-day revenue)
    for slot in range(n_slots):
        kind = KINDS[int(g[slot, 0]) % N_KINDS]
        if kind == "off":
            continue
        start = START_DAY_CHOICES[int(g[slot, 3]) % len(START_DAY_CHOICES)]
        block_i = int(g[slot, 2])
        if kind == "ranch":
            grp = RANCH_GROUPS[block_i % len(RANCH_GROUPS)]
            animal = R.ANIMAL_NAMES[int(g[slot, 1]) % len(R.ANIMAL_NAMES)]
            a = R.ANIMALS[animal]
            # One pen per day, so the purchases are spread exactly as `ranch()` spreads them.
            for k in range(len(grp)):
                events.append((start + k, float(a["cost"]), 25.0 / 2, start + k + a["first_yield_day"],
                               a["max_held"] * PRICE_BASE[a["product"]] * 0.5
                               / max(a["interval"], 1)))
            continue
        blk = BLOCKS[block_i % len(BLOCKS)]
        crop = R.CROPS[int(g[slot, 1]) % len(R.CROPS)]
        y = max(P.TILE_YIELD_FERTILIZED[crop], P.TILE_YIELD_PER_SEASON[crop])
        events.append((start, float(SEED_COST[crop] * len(blk)), 0.0,
                       start + R.CROP_TABLE[crop]["first"] + 1,
                       y * len(blk) * PRICE_BASE[crop] * 0.5 / R.SEASON_DAYS))
    max_unit = max((units[s] for s in range(n_slots)
                    if KINDS[int(g[s, 0]) % N_KINDS] != "off"), default=0)
    crew = float(hc[:max_unit].sum()) if max_unit else 0.0

    parcels = list(parcel_days)
    bank, curve = float(OPENING_BANK), []
    for day in range(R.SEASON_DAYS):
        for d, once, _pd, _ef, _rev in events:
            if d == day:
                bank -= once
        for d, _once, pd, earns_from, rev in events:
            if day >= d:
                bank -= pd
            if day >= earns_from:
                bank += rev
        bank -= crew
        for j, pday in enumerate(parcels):
            if pday == day:
                bank -= R.LAND_PRICES[j]
        curve.append(bank)
    return curve


# Base market prices, for the cash estimate only. `kagg/sim/market.py` owns the real curve.
PRICE_BASE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250,
              "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}


def _bank_estimate(day, upfront, per_day):
    """Pessimistic bank on `day`: the stake, plus what has been earned, minus what has been spent.

    **`per_day` is pro-rated and that is the whole point.** The first version of this charged the entire
    season's feed and hires against the bank on the day of the land order -- $11,280 of hires and $3,375
    of feed for a ten-chain farm -- so a day-7 purchase was judged against $3,000 minus $21,515 and
    nothing could ever buy land. That replaced "always yes" with "always no" and lost the same 50 tiles a
    different way. Recurring costs are paid out of recurring revenue, day by day, and only the days that
    have actually elapsed can have been paid.
    """
    earned = max(0, day - EARN_PER_DAY_AFTER) * EARN_RATE
    return C_OPENING_BANK + earned - upfront - per_day * day


def _affordable(first_order, upfront=0.0, per_day=0.0):
    """How many parcels the farm can really buy, in unlock order.

    **The amount matters, not only the day.** This used to refuse a parcel only when it was ordered
    before `EARLIEST_REVENUE_DAY` *and* the running total exceeded the opening bank; from day 3 onward
    every parcel was assumed affordable whatever it cost and whatever else the farm had committed. So a
    two-parcel plan passed, bought one, and `_do_buy_land` silently no-opped the other -- after which the
    chain walked until a LOCKED tile stopped it and built there, while `decode()` still reported it as
    `used`.

    The search then learned the wrong lesson from every land genome it tried, stopped proposing land, and
    stayed on **25 tiles against the leader's 75**. That is the entire gap.
    """
    bought, spent = 0, 0
    for j in sorted(first_order):
        spent += R.LAND_PRICES[j]
        if spent > _bank_estimate(first_order[j], upfront, per_day):
            break
        # Nothing has been earned before `EARLIEST_REVENUE_DAY`, so parcels ordered that early are
        # judged against the opening bank alone. Later ones are allowed through: revenue really does
        # fund them, and judging *those* against the opening bank is what made the search believe day
        # 0 was optimal when waiting is worth up to +$22,911.
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
    # **Occupied ground, which nothing tracked until 2026-08-05.** Two slots could claim the same tiles
    # and PLANT simply no-ops on the second, so the chain produced nothing while `decode()` reported it
    # as `used`. Confirmed in that day's best genome: slot 5's four tiles were a subset of slot 1's
    # eight-tile melon block, so the season grew **zero wheat** while ordering 16 wheat seeds -- and the
    # slot still scored +$1,564 because its unit's crop-agnostic WATER and HARVEST ops landed on melon.
    # It was a second hand on someone else's block wearing a wheat label, and every conclusion drawn
    # from "the search chose wheat" was wrong.
    #
    # Earlier slots win, so the same genome always decodes to the same tape.
    claimed = set()
    # One central schedule, so two chains wanting the same quadrant on different days do not buy it
    # twice -- and a chain on SW does not drag SE along behind it. See `land_schedule`.
    land_days = sorted(land_schedule(genome, n_slots))
    for day in land_days:
        t = day * R.TURNS_PER_DAY
        if 0 <= t < script.T:
            script.buy_land[t] += 1

    def parcels_by(day):
        """Parcels the farm owns **on `day`**, which is what reachability must be judged against.

        The season-end count is the wrong clock. Units cycle NW/NE/SW/SE, so units 1, 2 and 3 wake on
        tiles that are LOCKED on day 0 however much land gets bought later -- and a chain that starts
        before its ground or its spawn is unlocked walks into a locked border, stops, and does a whole
        season of work on the wrong tile without raising. Judging by the end of the season declared
        those chains legal, which is how a replica of the leader's ramp emitted 13 chains and planted
        zero tiles.
        """
        return sum(1 for d in land_days if d <= day)

    plan = []
    busy_units = set()
    for slot in range(n_slots):
        kind = KINDS[int(g[slot, 0]) % N_KINDS]
        if kind == "off":
            continue
        what_i, block_i, start_i, land_i, fert_i, trade_i, feed_i = (int(x) for x in g[slot, 1:])
        start_day = START_DAY_CHOICES[start_i % len(START_DAY_CHOICES)]
        land_day = LAND_DAY_CHOICES[land_i % len(LAND_DAY_CHOICES)]
        ground = (RANCH_GROUPS[block_i % len(RANCH_GROUPS)] if kind == "ranch"
                  else BLOCKS[block_i % len(BLOCKS)])
        tile = ground[0]
        if set(ground) & claimed:
            # Another slot already holds some of this ground. Emitting the chain anyway buys seed for
            # tiles it can never plant and puts a second unit on someone else's block.
            skipped += 1
            continue
        if R.land_purchases_for(tile) > affordable:
            # The ground cannot be bought on the day this chain orders it. Emitting the chain anyway
            # is what produced a genome claiming pens on (7,8), (2,8) and (6,9) while the animals
            # ended up on (7,4), (2,4) and (6,4): the walk stops at the locked border and BUILD fires
            # there. Skipping is counted, so an unaffordable genome reads as unaffordable.
            skipped += 1
            continue
        # **The unit must be able to WALK to the ground, not merely own it.**
        # `working_units` is now consecutive, so a slot can land on a unit that wakes in a quadrant the
        # farm has not bought -- units 3, 7, 11 spawn on `(5,5)` in SE and units 2, 6, 10 on `(4,5)` in
        # SW. Movement onto LOCKED ground is ignored without complaint (`ops.py:86`), so such a chain does
        # not fail: it walks until the border stops it and then does a whole season of PLANT, WATER and
        # HARVEST on whatever tile it is standing on.
        #
        # Measured on a replica of the leader's own ramp: 13 chains emitted, 12 hands hired, 312
        # fertilizer sales ordered -- and **zero planted tiles**, because the six crop chains had been
        # handed units 7-12. Every one of them was a phantom. This is the check that turns that into a
        # counted refusal.
        # **The unit is assigned, not looked up.** A static `slot -> unit` map cannot be right, because
        # whether a unit is usable depends on the chain's ground and start day, not on its index:
        #
        # - skipping SE-spawn units (the old `working_units`) leaves them hired and idle, and reaching
        #   unit 14 then costs 17 hands -- $125,400 a season against the leader's $7,916;
        # - handing slot k unit k blindly puts chains on units that wake on locked ground, where the walk
        #   stops at the border and a whole season of ops lands on the wrong tile. Slot 3 banked $2,408
        #   against slot 2's $9,331 that way.
        #
        # So take the lowest-numbered unit that is free and can actually reach this ground today. Lowest
        # keeps the hire ladder short; reachability keeps the chain real. A shed-cell pen still uses the
        # hand that wakes on it, since anyone else would have to walk there for no reason.
        # **The unit is chosen at EMISSION time, not here, because whether a job fits depends on the
        # turns already claimed on that unit -- and that is only known once earlier chains have been
        # written.** Choosing here forced one job per hand, and one job per hand is what caps the farm:
        #
        #   - a hand is dismissed and re-hired at every dawn and the ladder is Fibonacci, so the crew
        #     costs its whole partial sum every day: 8 hands $54, 12 hands $376, 16 hands $2,583;
        #   - a hand given one chain does ~2 useful ops in its 23 turns. Census against the leader:
        #     540 productive ops and 2,758 PASS turns for us, 2,438 and 357 for him.
        #
        # So every unit of capacity cost a ladder rung and delivered almost nothing, and the measured
        # farm peaked at 5 chains ($32,460) and fell off a cliff at 15 ($2,609) -- against his 14 pens
        # and ~61 tiles on 12 hands. Only the *pen cell* case is fixed here, because a shed-cell pen
        # must be worked by whoever wakes on it or it walks for no reason.
        fixed_unit = None
        if kind == "ranch" and ground[0] in RANCH_CELLS and len(ground) == 1:
            fixed_unit = R.unit_for_cell(ground[0])
            if not unit_can_reach(fixed_unit, tile, parcels_by(start_day)):
                skipped += 1
                continue
        elif not any(unit_can_reach(u, tile, parcels_by(start_day)) for u in range(MAX_UNITS)):
            # No unit can walk to this ground on this day at all, so the chain is a phantom whatever
            # the packing does. Counted, so an unreachable genome reads as unreachable.
            skipped += 1
            continue
        pen_unit = fixed_unit
        # **Emission is deferred so pens can claim their turns before crop blocks.**
        # Two chains may now share a unit (`Script.claim`), and the order they claim in decides whether
        # they fit. A shed pen is zero-movement when it goes first, but if a crop block has already run
        # the unit is standing out in the field, so `Script.where` correctly makes the pen walk back --
        # 7 extra moves, and 15 + 7 + 7 = 29 of 23 turns, so the pen is refused. Reversed, the pen costs
        # 7 turns and the block's own walk is unchanged: 22 of 23, and both fit.
        #
        # Pens go first for a second reason that outranks turn-packing: an animal escapes after two
        # consecutive missed feeds, so pen work is survival-critical while a missed WATER is not.
        #
        # Ground is still claimed above in **slot order**, so "earlier slots win" is unchanged and the
        # same genome still decodes to the same tape. Only the turn-claim order differs.
        plan.append((0 if kind == "ranch" else 1, slot, kind, what_i, block_i, start_day,
                     land_day, fert_i, trade_i, feed_i, pen_unit))

    # **A scratch script for probing whether a job fits on a unit.**
    # Whether `claim` raises depends only on `_claimed` and `_pos`, never on the op arrays, so a probe
    # needs those two dicts copied and nothing else. Reusing one scratch script and resetting the two
    # dicts costs two small dict copies per candidate; a `deepcopy` of the real script costs ~1MB, and
    # `decode` runs thousands of times inside a search.
    probe = R.Script()

    def _write(target, unit, kind, what_i, block_i, start_day, land_day, fert_i, trade_i, feed_i):
        """Emit one chain onto `unit`. Raises ValueError if the day will not take it."""
        if kind == "ranch":
            group = RANCH_GROUPS[block_i % len(RANCH_GROUPS)]
            animal = R.ANIMAL_NAMES[what_i % len(R.ANIMAL_NAMES)]
            R.ranch(target, animal=animal, tile=list(group), start_day=start_day,
                    land_day=land_day, unit=unit,
                    sell_fertilizer=bool(trade_i % 2), buy_land=False,
                    buy_feed=not bool(feed_i % 2))
            return ("ranch", animal, group, start_day), group
        block = BLOCKS[block_i % len(BLOCKS)]
        crop = R.CROPS[what_i % len(R.CROPS)]
        hold = bool(feed_i % 2) and crop == "WHEAT"
        R.grow(target, crop, list(block), plant_day=start_day, land_day=land_day,
               unit=unit, fertilize=bool(fert_i % 2),
               buy_fertilizer=bool(trade_i % 2), buy_land=False, sell=not hold,
               water_every=WATER_EVERY_FOR_BLOCK[block])
        return ("grow", crop, block, start_day), block

    for (_rank, slot, kind, what_i, block_i, start_day, land_day, fert_i, trade_i, feed_i,
         fixed_unit) in sorted(plan, key=lambda r: (r[0], r[1])):
        ground = (RANCH_GROUPS[block_i % len(RANCH_GROUPS)] if kind == "ranch"
                  else BLOCKS[block_i % len(BLOCKS)])
        # **Units already carrying work are tried FIRST, in ascending order, and a new hand is opened
        # only when no existing one has room.** That is the whole fix: it is first-fit bin packing over
        # each hand's 22 work turns, and it is what turns 15 hands into 12 for the leader's own farm
        # (`tests/test_the_crew_bill_must_not_dwarf_the_farm.py`).
        if fixed_unit is not None:
            candidates = [fixed_unit]
        else:
            candidates = [u for u in (sorted(busy_units)
                                      + [u for u in range(MAX_UNITS) if u not in busy_units])
                          if unit_can_reach(u, ground[0], parcels_by(start_day))]
        chain_unit = None
        for cand in candidates:
            probe._claimed = dict(script._claimed)
            probe._pos = dict(script._pos)
            try:
                _write(probe, cand, kind, what_i, block_i, start_day, land_day,
                       fert_i, trade_i, feed_i)
            except ValueError:
                continue
            chain_unit = cand
            break
        if chain_unit is None:
            skipped += 1
            continue
        busy_units.add(chain_unit)
        try:
            record, ground_used = _write(script, chain_unit, kind, what_i, block_i, start_day,
                                         land_day, fert_i, trade_i, feed_i)
            claimed.update(ground_used)
            used.append(record)
        except ValueError:
            # The probe said it fitted and the real write did not, which can only happen if the two
            # disagree -- counted rather than swallowed, so it shows up instead of silently shrinking
            # the farm.
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

    # **Non-overlapping, which matters now that blocks are cut at every window.** `OWNED_BLOCKS` used to
    # be a partition, so walking it with a cursor gave disjoint ground for free. Sliding windows overlap
    # heavily, and `decode()` now (correctly) skips a chain whose tiles another slot already holds -- so
    # taking consecutive entries produced a seed with three illegal chains out of eight.
    taken = set()

    def next_block(cursor):
        while cursor < len(OWNED_BLOCKS):
            b = OWNED_BLOCKS[cursor]
            if not (set(b) & taken):
                return cursor, b
            cursor += 1
        return cursor, None

    block_cursor = 0
    for slot in range(n_slots):
        kind, what, start_day = plan[slot]
        if kind == "grow":
            block_cursor, chosen = next_block(block_cursor)
            if chosen is None:
                break                                 # out of land we own; leave the rest "off"
        g[slot, 0] = KINDS.index(kind)
        if kind == "ranch":
            g[slot, 1] = R.ANIMAL_NAMES.index(what)
            g[slot, 2] = next(i for i, gr in enumerate(RANCH_GROUPS)
                              if gr == (OWNED_CELLS[slot % len(OWNED_CELLS)],))
        else:
            g[slot, 1] = R.CROPS.index(what)
            g[slot, 2] = BLOCKS.index(chosen)
            taken.update(chosen)
            block_cursor += 1
        g[slot, 3] = START_DAY_CHOICES.index(start_day)
        g[slot, 4] = LAND_DAY_CHOICES.index(0)         # nothing here needs land; 0 is a no-op
    return g.reshape(-1)
