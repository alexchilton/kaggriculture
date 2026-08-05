"""Macro-routines: the chain is the unit of search, not the sub-action.

**Why this module exists.** A sub-action search cannot find the animal economy, and that is a
structural fact rather than a tuning problem. Two mechanics close the door:

- `consecutive_unfed >= 2` escapes the animal (`kaggriculture.py:786`), so buying one you will not
  feed every day is a *deterministic* loss of $300-$500, not a bad expectation.
- FEED is illegal until an animal is on the board, unfed, with a unit standing on it carrying wheat
  (`jax_masks.py:93`), so a policy samples FEED from a distribution where it has zero mass.

Every prefix of the chain is therefore money-negative and every complete chain needs ~15 coordinated
edits at specific tiles on specific days. A hill-climber selecting on money rejects step one forever;
PPO learns to stop buying animals, which re-masks FEED and closes the loop. Both failures are the
same wall.

The fix is not a better optimiser. It is a representation in which a partial chain **cannot be
expressed**. A routine emits the whole chain or nothing, so the valley is not crossed -- it is not in
the space. What the search then owns is *which* routine, *where*, *when* and *how many*, which is
strategy, while correctness lives in the decoder.

**The ranch cell.** The four shed-access tiles are `(4,4) (5,4) (4,5) (5,5)` -- the inner corners
around the shed. PICKUP, DROP and shed-PLACE test only shed-adjacency, and FEED/CARE/HARVEST test
only that the unit stands on the animal's tile. Put the pen *on* a shed-access tile and one unit can
run the entire loop -- draw feed, feed, care, harvest, deposit -- **without ever moving**, in 5 of
the day's 24 turns. That matters beyond convenience: a unit's tile is the cumulative sum of its
movement ops, so in an open-loop script one edited step silently invalidates every later op. A
zero-movement routine has no such coupling, which is what makes it a safe unit of search.

**Land is the gate.** Only `(4,4)` is in NW, the sole quadrant unlocked at the start; the other three
cells begin LOCKED. `LAND_ORDER` is `['NE','SW','SE']` at `[1000, 2000, 4000]`, bought in sequence,
so cell `(5,5)` costs $7,000 of land to reach. This is also why an agent that never buys land plays
the whole season on 25 tiles of 100.
"""

import numpy as np

# ---------------------------------------------------------------------------
# The reference's own tables, mirrored. Kept as literals rather than imported so this module has no
# dependency on `reference/`, and pinned by `tests/test_routines.py` against the geometry helpers.
# ---------------------------------------------------------------------------

OP_NAMES = [
    "PASS", "NORTH", "SOUTH", "EAST", "WEST",
    "WATER", "HARVEST", "PLANT", "DIG",
    "PICKUP", "DROP", "PLACE", "FEED", "CARE", "COLLECT_FERTILIZER", "FERTILIZE",
    "BUILD_COOP", "BUILD_PASTURE",
]
OP = {n: i for i, n in enumerate(OP_NAMES)}

PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]
CROPS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"]
ANIMAL_NAMES = ["GOOSE", "COW", "SHEEP"]
ITEMS = PRODUCTS + ANIMAL_NAMES          # the `unit_item` domain, 12 wide

ANIMALS = {
    "GOOSE": {"cost": 300, "structure": "COOP",    "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},
    "COW":   {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},
}
STRUCTURE_OP = {"COOP": OP["BUILD_COOP"], "PASTURE": OP["BUILD_PASTURE"]}

LAND_ORDER = ["NE", "SW", "SE"]
LAND_PRICES = [1000, 2000, 4000]

BOARD_SIZE = 10
TURNS_PER_DAY = 24
SEASON_DAYS = 30
T_DEFAULT = 719          # the recorder's length: 30 days of 24 turns, minus the unplayed last turn
U_DEFAULT = 24


def quadrant_of(x, y, board_size=BOARD_SIZE):
    half = board_size // 2
    return ("N" if y < half else "S") + ("W" if x < half else "E")


def shed_access_tiles(board_size=BOARD_SIZE):
    """The four inner-corner tiles around the shed, in the reference's NWSE order."""
    half = board_size // 2
    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]


SPAWN = (4, 4)          # `_default_spawn`: the only shed-access tile inside the starting quadrant


def spawn_order(board_size=BOARD_SIZE, n=8):
    """Unit index -> the tile that unit spawns on at dawn.

    Mirrors `_spawn_hand`: minimum occupancy over the shed-access tiles, ties broken by NWSE index.
    The farmer occupies `(4,4)` first, so hands land on `(5,4)`, `(4,5)`, `(5,5)` in that order --
    **exactly one per ranch cell, with no movement required by any of them.**

    Note it does *not* filter for unlocked quadrants, so a hand really does spawn on a LOCKED tile.
    It can still PICKUP and DROP there (those test only shed-adjacency) but cannot BUILD, because a
    LOCKED tile is the string `"LOCKED"` rather than `None`.
    """
    tiles = shed_access_tiles(board_size)
    occ = {t: 0 for t in tiles}
    occ[tuple(SPAWN)] += 1
    order = [tuple(SPAWN)]
    for _ in range(n):
        best = min(occ.items(), key=lambda kv: (kv[1], tiles.index(kv[0])))[0]
        order.append(best)
        occ[best] += 1
    return order


def spawn_tile(unit, board_size=BOARD_SIZE):
    """Where `unit` actually stands at dawn -- which is `SPAWN` only for unit 0 and its cycle.

    Hands fill the shed-access tiles in NWSE order and wrap every four, so unit 2 wakes on `(4,5)`
    and unit 3 on `(5,5)`. `grow()` routed every unit from `SPAWN` regardless, which is a correct
    walk from the wrong origin: the unit arrives displaced by the difference, and then PLANT, WATER
    and HARVEST land on tiles it does not own and silently no-op. Measured on one melon block, same
    chain, only the unit changed: $15,575 for unit 0 against $5,402 for unit 2 and $1,920 for unit 3.
    """
    return spawn_order(board_size, n=unit + 1)[unit]


def unit_for_cell(tile, board_size=BOARD_SIZE):
    """The lowest unit index that spawns on `tile`.

    Also the number of hands that must be hired that day to bring it into existence, since hands are
    dismissed every dawn (`kaggriculture.py:849`) and unit `k` is the `k`-th hand.
    """
    for i, t in enumerate(spawn_order(board_size)):
        if t == tuple(tile):
            return i
    raise ValueError(f"{tile} is not a spawn tile")


def land_purchases_for(tile, board_size=BOARD_SIZE):
    """How many sequential BUY_LAND orders are needed before `tile` is unlocked.

    `_do_buy_land` ignores its caller's wishes and unlocks `LAND_ORDER[n_already_bought]`, so
    reaching SE costs all three purchases whether or not NE and SW are wanted.
    """
    q = quadrant_of(*tile, board_size=board_size)
    if q == "NW":
        return 0
    return LAND_ORDER.index(q) + 1


class Script:
    """A mutable action tape: `[T, U]` unit ops plus the per-turn market vector.

    Deliberately plain arrays rather than a builder DSL. The optimiser mutates *plans*, expands them
    through the routines below into one of these, and hands the arrays straight to the simulator --
    the same arrays `scripts/build_script_submission.py` already turns into a verified submission.
    """

    #: `(day, unit) -> turns already claimed today`. Turn 0 of a day is the market order, so work
    #: starts at 1 and a day holds `TURNS_PER_DAY - 1` ops.
    #:
    #: **This exists so two routines can share a unit.** Both `ranch()` and `grow()` used to lay their
    #: day out from `d + 1` on the assumption that they owned the whole day, and `op()` assigns
    #: `unit_op[t, u]` directly -- so calling both for one unit silently overwrote the first. Measured
    #: on a 2-pen group plus a 4-tile block: 327 + 434 ops composed to 441, losing 320 of them, and the
    #: herd stopped being fed on 29 of 30 days. Nothing raised and nothing reported it.
    #:
    #: That mattered because one chain = one unit capped the farm. Covering the leader's 14 pens plus
    #: ~100 tile-plantings needed 14 chains, forcing unit 17, and the hire ladder resets every dawn:
    #: 9 hands is $88/day but 17 is $4,180/day, i.e. $125,400 a season -- more than he banks in total.
    #: He does it with twelve hands because his hands tend a pen *and* crop tiles on the same day.
    #:
    #: Claiming turns instead of assuming them makes an overfull day a **refusal the caller can count**
    #: rather than an overwrite nobody can see, which is the same contract the land gate now honours.
    def __init__(self, T=T_DEFAULT, U=U_DEFAULT):
        self.T, self.U = T, U
        self._claimed = {}
        self._pos = {}
        self.unit_op = np.zeros((T, U), np.int64)      # 0 == PASS
        self.unit_crop = np.zeros((T, U), np.int64)
        self.unit_item = np.zeros((T, U), np.int64)
        self.unit_qty = np.zeros((T, U), np.int64)
        self.sell = np.zeros((T, len(PRODUCTS)), np.int64)
        self.buy_seed = np.zeros((T, len(CROPS)), np.int64)
        self.buy_product = np.zeros((T, len(PRODUCTS)), np.int64)
        self.buy_animal = np.zeros((T, len(ANIMAL_NAMES)), np.int64)
        self.hire = np.zeros(T, np.int64)
        self.buy_land = np.zeros(T, np.int64)

    def arrays(self):
        return {f: getattr(self, f) for f in
                ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
                 "buy_product", "buy_animal", "hire", "buy_land")}

    def turns_left(self, day, unit):
        """Work turns still free for `unit` on `day`. `TURNS_PER_DAY - 1` if nothing has claimed yet."""
        return TURNS_PER_DAY - self._claimed.get((day, unit), 1)

    def claim(self, day, unit, n, what=""):
        """Reserve `n` consecutive work turns for `unit` on `day` and return the first of them.

        Raises when the day cannot hold them, which is the whole point: the caller then refuses the
        chain and counts it, instead of writing over another routine's ops.
        """
        used = self._claimed.get((day, unit), 1)      # turn 0 is the market order
        if used + n > TURNS_PER_DAY:
            raise ValueError(
                f"day {day} unit {unit}: {what or 'this routine'} needs {n} turns but only "
                f"{TURNS_PER_DAY - used} of {TURNS_PER_DAY - 1} remain (another routine on the same "
                f"unit has claimed {used - 1}); use fewer tiles, a larger cadence, or another unit")
        self._claimed[(day, unit)] = used + n
        return day * TURNS_PER_DAY + used

    def where(self, day, unit, default):
        """Where `unit` stands partway through `day`, so a second routine walks from there.

        Without this a combined chain is wrong even when it fits: `grow()` computes its walk from
        `spawn_tile(unit)`, but after `ranch()` the unit is standing at a pen, so every MOVE lands
        somewhere else and the ops that follow act on the wrong tile.
        """
        return self._pos.get((day, unit), tuple(default))

    def stand(self, day, unit, pos):
        """Record where `unit` finished its ops on `day`."""
        self._pos[(day, unit)] = tuple(pos)

    def op(self, t, u, name, item=None, qty=0, crop=None):
        """Write one unit op. Out-of-range turns are dropped so a routine may run past the season."""
        if not (0 <= t < self.T):
            return
        self.unit_op[t, u] = OP[name]
        if item is not None:
            self.unit_item[t, u] = ITEMS.index(item)
            self.unit_qty[t, u] = qty
        if crop is not None:
            self.unit_crop[t, u] = CROPS.index(crop)


# ---------------------------------------------------------------------------
# Routines
# ---------------------------------------------------------------------------

def ranch(script, animal, tile, start_day, land_day=0, sell=True, unit=None,
          collect_fertilizer=True, sell_fertilizer=True, buy_land=True, buy_feed=True,
          feed_every=None, build_every=1):
    """Build pens on `tile`, stock them, and keep every animal fed for the rest of the season.

    `tile` takes a single tile or a list of them. **A list is one chain, one unit, one slot** --
    which is the point, because 1 pen = 1 slot meant five pens ate five of eight slots and left three
    for crops, i.e. 12 crop tiles against the leader's 60-75. Strawberry alone is a $68,640 market
    needing ~48 tiles, so those slots decide the whole farm.

    The arithmetic. Per animal per day the loop is PICKUP, FEED, CARE, COLLECT_FERTILIZER, HARVEST =
    five turns, and the four shed cells form a 2x2 block one unit walks in four moves:

        4 moves + 4 animals x 5 turns = 24   just over the 23 available work turns
        feeding every other day:  4 + 4 x 3.5 = 18   comfortable

    `feed_every` is that cadence and defaults to whatever fits. It is safe for the same reason
    alternate-day watering is: `jax_sim.py:1243` escapes an animal only after **two consecutive**
    missed feeds, so a gap of one leaves the streak at 1 and the next feed resets it. The leader
    feeds 319 times across 14 animals -- **22.8 each, not 30** -- so he is not feeding daily either.
    CARE, COLLECT_FERTILIZER and HARVEST stay daily: they are cheap and none of them gates survival.

    Emits the complete chain and nothing partial. There is deliberately no primitive that buys an
    animal without also committing the feed loop that keeps it alive -- that combination is the
    $300-$500 deterministic loss the search must never be able to propose.

    **Everything here is a consequence of the dawn reset** (`kaggriculture.py:847-851`), which
    dismisses every hand, teleports the farmer back to `(4,4)` and resets the hire ladder:

    - Those hires repeat **every day**. The Fibonacci ladder resets daily, so three hands cost
      $1+$1+$2 = $4/day, about $120 across a season.
    - Carried inventory is auto-deposited at dusk, so the daily DROP is only needed to get product
      into the shed in time for that day's sell order.
    - **The walk repeats every day too**, which is the whole reason a pen may now sit anywhere. The
      first version of this routine walked once, on the start day, and then fed thin air for the rest
      of the season because dawn had teleported the unit home. The refusal that replaced it -- only
      shed-access tiles, so no movement op was ever needed -- was a real safety property but it
      capped the herd at four, one per quadrant, against the leader tape's **14** pens. Worse than
      four in practice: cells three and four cost $3,000 and $7,000 of land against a $3,000 opening
      bank, so substituting them scored $0 and 0/16 wins and the usable cap was two.

      `grow()` already solved this the honest way -- re-walk from spawn every single day -- and that
      is what happens here now. Two consequences follow from being off the shed, and both are
      deliberate: a remote pen cannot DROP (the op tests shed-adjacency, so out in the field it is a
      wasted turn), and its goods therefore only reach the shed at the dusk auto-drop, which pushes
      its sell order to the **next dawn** rather than the same afternoon.

    A pen still on a shed-access tile keeps the old zero-movement day exactly as it was, including
    the same-day DROP and sell. That is why those four cells remain worth having and why the search
    should still prefer them: they are strictly cheaper per day than anywhere else on the board.

    `land_day` is separate from `start_day` because `_do_buy_land` silently no-ops when money is
    short and the parcels cost $1,000/$2,000/$4,000 in sequence. Funding SE means earning first, so
    when to buy land is a plan parameter, never a default.

    **`collect_fertilizer` defaults on, and leaving it off was this routine's biggest omission.**
    A fed animal sets `fertilizer_available` every night and COLLECT_FERTILIZER takes it for *no
    action cost* (`plan.py:144`), so a day without one abandons a free unit. It is not a rounding
    error: FERTILIZER is 23.1% of winner sales against milk's 9.1% (`shepherd.py:28`) and the
    leaders banked ~$21,900 from 406 units. Every animal verdict this project produced before this
    landed was measured on a milk-only cow, which is why the search kept concluding animals do not
    pay. The collect is ordered **before** the DROP: fertilizer sits in `carried` until it is
    dropped, so a collect after the drop would not reach the shed in time for that day's sell.
    """
    if animal not in ANIMALS:
        raise ValueError(f"unknown animal {animal}")

    # One tile or many. Normalised early so everything below is written against a list.
    tiles = ([tuple(tile)] if isinstance(tile, tuple) and tile and isinstance(tile[0], int)
             else [tuple(t) for t in tile])
    if not tiles:
        raise ValueError("ranch() needs at least one tile")
    if len(set(tiles)) != len(tiles):
        raise ValueError(f"duplicate pen tiles {tiles}")
    # One quadrant, with the shed cells as the deliberate exception: they are the contiguous 2x2 block
    # around the shed, one per quadrant by construction, and adjacent to each other -- `(4,4)` to
    # `(5,4)` is a single EAST step. Refusing them would refuse the only pen group that needs no walk
    # to the shed at all. Everything else routes inside one quadrant, as `grow()` does.
    quads = {quadrant_of(*t) for t in tiles}
    if len(quads) > 1 and not set(tiles) <= set(shed_access_tiles()):
        raise ValueError(f"pens span quadrants {sorted(quads)}; one chain routes inside one quadrant")
    tiles = serpentine(tiles)
    tile = tiles[0]                      # the chain's anchor: its unit, its land, its walk
    info = ANIMALS[animal]
    a_idx = ANIMAL_NAMES.index(animal)
    wheat = PRODUCTS.index("WHEAT")
    prod_idx = PRODUCTS.index(info["product"])
    fert_idx = PRODUCTS.index("FERTILIZER")
    at_shed = tile in shed_access_tiles()
    # A shed cell is worked by whoever wakes on it -- anyone else would have to walk to it for no
    # reason. Anywhere else, the caller owns the choice and unit 0 is the free default, since the
    # farmer costs no hire.
    if unit is None:
        u = unit_for_cell(tile) if at_shed else 0
    else:
        u = unit
    # **Everything drawn from the shed must be drawn at `SPAWN`.** `ops.py:216` gates PICKUP, DROP
    # and PLACE's shed branch on the tile being shed-access *and unlocked*, and three of the four
    # shed tiles sit in quadrants that start LOCKED. A hand waking on `(5,4)` therefore picks up
    # nothing at all -- no error, no cow, no wheat -- which is why the first remote pen banked $1,437
    # against an empty farm's $3,000 and left the board with zero animals on it.
    #
    # A pen *on* a shed cell is the exception and keeps its zero-movement day: this routine buys the
    # parcel its own quadrant needs, so by `land_day` the cell is unlocked and PICKUP works where the
    # unit already stands. Walking such a cell out to `(4,4)` and back would cost two turns a day to
    # solve a problem it does not have.
    zero_movement = at_shed and tuple(spawn_tile(u)) == tile
    to_spawn = [] if zero_movement else _path_ops(spawn_tile(u), SPAWN)
    walk = [] if zero_movement else _path_ops(SPAWN, tile)

    # --- land: every parcel up to and including this cell's quadrant ------
    # **One per day, not one per turn.** These used to go out on turns `land_day*24 + 0,1,2`, so a
    # cell in SE asked for $1,000 + $2,000 + $4,000 inside three turns against a $3,000 bank.
    # `_do_buy_land` no-ops when money is short rather than refusing the plan, so the third order
    # simply evaporated -- the farm never goes negative, it just quietly owns less land than the
    # chain thinks it does, and the pen then walks until a LOCKED tile stops it and builds there.
    #
    # Spacing does not make $7,000 affordable; only earning does. What it buys is a schedule the
    # search can actually express, so `land_day` chooses between plans that differ instead of
    # between plans that all collapse to "whatever the opening bank covered". The leader tape is the
    # shape to aim at: parcels on **day 7 and day 10**, spaced, and the third never bought at all.
    #
    # `buy_land=False` hands the schedule to the caller. A BUY_LAND order is a claim on a shared,
    # ordered, farm-level resource -- `_do_buy_land` unlocks `LAND_ORDER[n_already_bought]` and
    # ignores which quadrant was wanted -- so two chains each privately ordering "the parcels I need"
    # over-buy as soon as their days differ. A pen on NE wanting day 7 and a pen on SW wanting day 10
    # emitted orders on days 7, 10 and 11: three parcels, $7,000, when NE + SW is $3,000. `decode()`
    # consolidates instead. Standalone callers keep the self-sufficient default.
    if buy_land:
        for k in range(land_purchases_for(tile)):
            t = (land_day + k) * TURNS_PER_DAY
            if 0 <= t < script.T:
                script.buy_land[t] = 1

    # --- the crew this cell needs, re-hired every dawn --------------------
    # `maximum`, not `+=`: a cell needing 3 hands already provides units 1 and 2 for the nearer
    # cells, so co-located routines must not each add their own.
    for day in range(start_day, SEASON_DAYS):
        t = day * TURNS_PER_DAY
        if u > 0 and t < script.T:
            script.hire[t] = max(int(script.hire[t]), u)

    build_op = "BUILD_PASTURE" if info["structure"] == "PASTURE" else "BUILD_COOP"

    # How often each animal is fed. `None` means "as often as the day allows": the survival rule is a
    # two-strike one (`jax_sim.py:1243`, two consecutive missed feeds and the animal escapes), so a
    # cadence of 2 is safe and halves both the turns and the wheat bill. One pen has room to feed
    # daily; four do not, and rather than raise, the chain stretches the cadence until it fits.
    if feed_every is None:
        feed_every = 1 if len(tiles) <= 2 else 2
    if feed_every < 1:
        raise ValueError("feed_every must be at least 1")
    if feed_every > 2:
        raise ValueError("feed_every above 2 starves the herd: two missed feeds and it escapes")
    if build_every < 1:
        raise ValueError("build_every must be at least 1")
    feed_shifts = [tiles[i::feed_every] for i in range(feed_every)]

    def day_loop(day, setup):
        """One day over the group. **One pen is built per day**, not all of them at once.

        Building four pens on a single day needs 32 turns of a 24-turn day: each is BUILD, PICKUP,
        PLACE, FEED, CARE, HARVEST on top of the walk. Staggering costs nothing -- an animal placed on
        day `start_day + i` simply starts producing `i` days later -- and it matches cash flow, since
        four animals is $1,600 against a $3,000 opening bank. The leader does the same: 14 pens with
        `BUILD_PASTURE` spread across the season rather than clustered.
        """
        d = day * TURNS_PER_DAY
        if d >= script.T:
            return
        # Pens built so far, and the one being raised today.
        # **How fast the group fills, which is a cash decision and not a fact about pens.**
        # This was `day - start_day`: one pen every single day, unconditionally. With four chains all
        # starting on day 0 that buys four animals a day for four days -- $6,800 against a $3,000 bank --
        # so most of them silently no-op while the feed and hire bills carry on. Measured: 16 ordered,
        # 8 realised, bank $301 on day 10, and a faithful copy of the leader's shape banked $10,875
        # where a three-cow plan banked $38,948.
        #
        # The leader's herd arrives 4 on day 0, then +2, +1, +4, +1, +2 through day 10. He is not
        # building slowly because pens are slow; he is building at the rate his revenue funds.
        # Pen `i` is raised on day `start_day + i*build_every`. A pen counts as *live* only from the day
        # after it is placed, so `live` is the pens whose build day has strictly passed -- a **ceiling**
        # division, not a floor. Flooring it left the day-0 animal out of `live` until day 3, so it went
        # unfed for two consecutive nights, escaped, and the whole plan banked exactly $0.
        elapsed = max(0, day - start_day)
        n_live = min(len(tiles), -(-elapsed // build_every))
        building = (tiles[n_live] if n_live < len(tiles) and elapsed % build_every == 0
                    else None)
        live = tiles[:n_live]
        if not live and building is None:
            return
        # Feed only what exists. The shift index walks the live herd so each animal is reached at
        # least every `feed_every` days.
        feeding = [t for t in feed_shifts[(day - start_day) % feed_every] if t in live]
        # **A pen must be fed on the day it is placed.** `consecutive_unfed` starts at 0 and ticks
        # every night, so an animal placed on day D and first fed on D+2 escapes overnight on D+1 --
        # before it has produced anything, for the full purchase price. Measured: four pens placed on
        # consecutive days, zero alive at the bell.
        if building is not None:
            feeding = feeding + [building]
        # Order feed a turn ahead of drawing it, so the market has resolved either way. One unit of
        # wheat per animal actually being fed today, not per animal owned.
        #
        # `buy_feed=False` lives off the shed instead, which is the wheat -> animal -> fertilizer loop
        # `production.py:53` calls the main structural reason to keep animals. It only closes if some
        # `grow("WHEAT", ..., sell=False)` chain is stocking that shed: `pickup` takes by item index
        # and does not care where the wheat came from, but `consecutive_unfed >= 2` escapes the animal
        # for a deterministic $300-$500, so an empty shed is not a small mistake.
        if buy_feed and feeding:
            script.buy_product[d, wheat] += len(feeding)
        if building is not None:
            script.buy_animal[d, a_idx] += 1

        # `(op_name, item, qty)`, built before any of it is written so the day's length can be
        # checked. PICKUP only works next to the shed, so everything the unit must carry -- the
        # animals on the build day, the wheat every day -- is drawn at spawn *before* the walk.
        seq = []
        pos = script.where(day, u, spawn_tile(u))
        if not (zero_movement and len(tiles) == 1):
            for m in _path_ops(pos, SPAWN):
                seq.append((m, None, 0))
            pos = tuple(SPAWN)
        if building is not None:
            seq.append(("PICKUP", animal, 1))
        if feeding:
            seq.append(("PICKUP", "WHEAT", len(feeding)))

        for t_ in [t for t in tiles if t in live or t == building]:
            for m in _path_ops(pos, t_):
                seq.append((m, None, 0))
            pos = t_
            if t_ == building:
                seq.append((build_op, None, 0))
                seq.append(("PLACE", animal, 1))
                seq.append(("FEED", None, 0))
                # CARE on the build day too: `pending_care_bonus` accumulates while it waits, so the
                # turn is banked rather than spent. No COLLECT_FERTILIZER or HARVEST -- both need an
                # overnight tick the animal has not had yet.
                seq.append(("CARE", None, 0))
                continue
            if t_ in feeding:
                seq.append(("FEED", None, 0))
            # CARE grants +1 yield on the next fed production day, and `pending_care_bonus` accumulates
            # while it waits, capped at `max_held`. One turn a day for roughly double output; it is why
            # CARE correlates +0.441 with money across 312 real leaderboard seats. Kept daily even on a
            # non-feeding day: it is cheap and it does not gate survival.
            seq.append(("CARE", None, 0))
            if collect_fertilizer:
                # `fertilizer_available` is set overnight for animals already alive, so a pen raised
                # today has nothing to give -- which the `continue` above already skips.
                seq.append(("COLLECT_FERTILIZER", None, 0))
            seq.append(("HARVEST", None, 0))

        if at_shed and pos in shed_access_tiles():
            # Only worth a turn where it can succeed: DROP tests shed-adjacency, so out in the field
            # it is a no-op and `_drop_to_shed` moves the goods at dusk regardless.
            seq.append(("DROP", None, 0))

        # Claim the turns rather than assume them, so a crop block sharing this unit cannot be
        # overwritten -- and so an overfull day raises here instead of vanishing.
        t = script.claim(day, u, len(seq),
                         what=f"{len(tiles)} pen(s) at {tiles} from {spawn_tile(u)}")
        for op_name, item, qty in seq:
            script.op(t, u, op_name, item=item, qty=qty)
            t += 1
        script.stand(day, u, pos)

        if sell:
            # Over-requesting is safe: `_process_market` stops when the shed runs dry. Selling daily
            # is the naive cadence -- it walks our own price down the glut curve -- and the timing is
            # a plan parameter the search should own rather than something fixed here.
            #
            # A shed pen has already DROPped, so it can sell this afternoon. A remote pen's goods sit
            # in `carried` until dusk, so its order has to wait for the next dawn or it quotes
            # against a shed that does not hold them -- measured at exactly zero revenue in
            # `test_grow_routine.py`.
            t_sell = t + 1 if at_shed else (day + 1) * TURNS_PER_DAY
            if t_sell < script.T:
                # Scaled by the herd, not by one animal: a four-pen chain has four animals' worth of
                # product in the shed and an order for one animal's worth would leave three unsold.
                script.sell[t_sell, prod_idx] += info["max_held"] * max(1, len(live))
                if collect_fertilizer and sell_fertilizer:
                    # **Selling and feeding it to plants are rival uses, and this used to be neither
                    # a choice nor visible.** The pen sold every unit it collected while
                    # `grow(fertilize=True)` bought units back off the same market -- the farm
                    # trading with itself and paying the spread twice. FERTILIZER is 23.1% of winner
                    # sales, so selling is not obviously wrong; a cow yields ~29 units a season and a
                    # fertilized 4-tile block wants ~40, so feeding is not obviously wrong either.
                    # It is a genuine trade-off and the search now owns it.
                    script.sell[t_sell, fert_idx] += max(1, len(live))

    for day in range(start_day, SEASON_DAYS):
        day_loop(day, setup=(day == start_day))
    return script


# Which crops fertilizer is worth a turn on, derived from the measured season yields in
# `kagg/economics/production.py` rather than restated here -- a second copy would drift, and the
# whole point is that melon must never be fertilized by accident. Melon gains exactly nothing (12
# units either way, its watering window already fills `max_yield`) while tomato and strawberry
# double. FERTILIZE is active for the day it is spent plus two more, so a tile wants one every
# third day and not daily.
def _crops_fertilizer_helps():
    from kagg.economics import production as _P
    return frozenset(c for c in CROPS
                     if _P.TILE_YIELD_FERTILIZED[c] > _P.TILE_YIELD_PER_SEASON[c])


FERTILIZER_HELPS = _crops_fertilizer_helps()
FERTILIZER_ACTIVE_DAYS = 3

CROP_TABLE = {
    # `first`/`max_day` are ages in days since planting; `ongoing` crops are never cleared by a
    # harvest and accrue to a lifetime cap instead. Mirrored from `kagg.sim.tiles`, pinned by tests.
    "WHEAT":      {"first": 2,  "max_day": 4,  "max_yield": 6, "ongoing": False},
    "CARROT":     {"first": 2,  "max_day": 3,  "max_yield": 4, "ongoing": False},
    "TOMATO":     {"first": 8,  "max_day": 8,  "max_yield": 4, "ongoing": True},
    "STRAWBERRY": {"first": 10, "max_day": 10, "max_yield": 4, "ongoing": True},
    "MELON":      {"first": 10, "max_day": 12, "max_yield": 6, "ongoing": False},
}

# `_DX`/`_DY` in `kagg.sim.ops`: NORTH is dy=-1, SOUTH dy=+1, EAST dx=+1, WEST dx=-1. So north is
# *smaller* y, which agrees with `quadrant_of` calling y < half "N". Getting this backwards would
# send every path the wrong way and is silent, because a blocked move is a no-op rather than an error.
def _axis_ops(src, dst):
    """Movement ops `src` -> `dst`, X then Y. Safe only when the whole rectangle is unlocked."""
    ops = []
    dx = dst[0] - src[0]
    dy = dst[1] - src[1]
    ops += ["EAST"] * dx if dx > 0 else ["WEST"] * (-dx)
    ops += ["SOUTH"] * dy if dy > 0 else ["NORTH"] * (-dy)
    return ops


def _path_ops(src, dst):
    """Movement ops walking `src` -> `dst`, routed through `SPAWN` so the walk never starts by
    stepping into locked land.

    The previous version went X-then-Y from wherever the unit stood, with the comment "any order
    works inside one quadrant". That assumption breaks the moment the origin is in a *different*
    quadrant from the destination, which is the normal case: hands spawn on the shed-access tiles,
    and three of those four are in quadrants that start LOCKED.

    `ops.py:86` ignores a move onto a LOCKED tile and the unit simply loses the turn -- silently.
    So unit 2, spawning on `(4,5)` in SW, spent four turns pushing WEST into locked ground and then
    walked north from where it had never left, arriving on a row it did not own. Measured on one
    melon block: $5,402 against unit 0's $15,575.

    `SPAWN` `(4,4)` is the one tile that is never locked, and every shed-access tile is one step from
    it, so leaving via `SPAWN` is legal for any unit whose neighbour-to-`SPAWN` is unlocked. Unit 3 on
    `(5,5)` is a genuine exception -- both its neighbours are locked on day 0 and it cannot move at
    all until a parcel is bought. That is the game, not the routing, and the ops are emitted anyway
    so the chain starts working the moment the land arrives.
    """
    src, dst = tuple(src), tuple(dst)
    if src == dst:
        return []
    spawn = tuple(SPAWN)
    # Only the *first* leg -- out of a shed-access tile -- can start in locked ground. Hops between
    # tiles of a block start on land the chain already works, so they take the direct route. Sending
    # those through SPAWN too would walk the unit home between every pair of adjacent tiles: 56 turns
    # for a 4-tile block against a 24-turn day.
    if src == spawn or src not in shed_access_tiles():
        return _axis_ops(src, dst)
    # Step to SPAWN first -- Y then X, because the shed tiles differ from SPAWN on one axis only.
    out = []
    dy = spawn[1] - src[1]
    dx = spawn[0] - src[0]
    out += ["SOUTH"] * dy if dy > 0 else ["NORTH"] * (-dy)
    out += ["EAST"] * dx if dx > 0 else ["WEST"] * (-dx)
    return out + _axis_ops(spawn, dst)


def serpentine(tiles):
    """Order `tiles` so consecutive entries are adjacent where possible: rows, alternating direction.

    A boustrophedon keeps the walk between tiles at one step instead of jumping back to the row start,
    which matters because the turn budget is the binding constraint on how many tiles one unit can work.
    """
    rows = {}
    for x, y in tiles:
        rows.setdefault(y, []).append((x, y))
    out = []
    for i, y in enumerate(sorted(rows)):
        row = sorted(rows[y], key=lambda t: t[0], reverse=bool(i % 2))
        out += row
    return out


def grow(script, crop_name, tiles, plant_day, harvest_age=None, land_day=0, sell=True, unit=0,
         buy_fertilizer=True, buy_land=True, water_every=1,
         fertilize=False):
    """Plant, water and harvest a block of tiles, re-walking from spawn every day.

    The crop analogue of `ranch()`, and structurally harder for one reason: `ranch()` is safe because
    it binds to a shed-access tile and therefore **never emits a movement op**, so an edit cannot
    invalidate later positions. There are only four such tiles and animals want them, so a crop block
    lives on the other ~96 and this routine has to route. Everything below follows from that.

    - **The walk repeats every day.** `_end_of_day` teleports every unit back to spawn at dawn
      (`jax_sim.py:1228-1236`), so a routine that walks to the block once and then emits WATER for the
      rest of the season waters the *spawn tile*. This is the same defect `ranch()` records fixing.
    - **Water every day, both crop types.** `_daily_refresh_plants` kills any PLANT tile at
      `consecutive_unwatered >= 2` regardless of `ONGOING`. The yield *bonus* only lands for
      non-ongoing crops inside `[(max_day+1)//2, max_day]` (`jax_sim.py:632-636`), which tempts a
      reader into skipping water for tomato and strawberry -- that kills them.
    - **One-shot crops cycle, ongoing crops do not.** HARVEST sets a non-ongoing tile back to EMPTY
      (`jax_sim.py:651`), so wheat can be replanted the next day and run several cycles a season.
      An ongoing tile survives its harvest and keeps producing to a lifetime cap.
    - **Ongoing crops are harvested every eligible day, deliberately.** Once `production_count` hits
      `MAX_YIELD` the tile's `max_lifespan_step` is set and `_decay_plants` eats a unit every other
      step, so accumulated yield rots. HARVEST is a silent no-op when nothing is ready
      (`doable` requires `units > 0`), so harvesting daily costs one turn and makes decay unreachable
      rather than merely unlikely.
    - **Seeds are ordered at dawn and planted later the same day.** The atomic PLANT rule
      (`jax_sim.py:565-582`) tests a turn's requests against seeds held at the *start* of that turn and
      drops **every** request for a crop when demand exceeds supply, not just the excess. Ordering on
      turn `d` and planting from `d+1` means the seeds have settled. `+=` is correct here, unlike the
      `maximum` used for hires: two blocks of the same crop on one day need the sum of their seeds,
      whereas they *share* the hands they hire.
    - **No DROP, and therefore the sell waits for the next dawn.** `_end_of_day` calls `_drop_to_shed`
      unconditionally (`jax_sim.py:1230`), so a harvest reaches the shed at dusk without a walk back.
      But it is in `carried` until then, so a SELL on the harvest day itself quotes against a shed that
      does not hold the crop. `ranch()` gets away with a same-day sell only because it stands on a shed
      tile and emits DROP first; out in a field, DROP cannot reach the shed. Measured: selling same-day
      banked **zero revenue on every crop**, losing exactly the seed cost
      (`tests/test_crop_routine.py::test_a_crop_routine_pays_for_itself`).

    Raises rather than truncates when a day's work will not fit in 24 turns -- a silently overflowing
    day would spill ops into the next dawn, where the unit has been teleported away.
    """
    if crop_name not in CROP_TABLE:
        raise ValueError(f"unknown crop {crop_name}")
    tiles = [tuple(t) for t in tiles]
    if not tiles:
        raise ValueError("grow() needs at least one tile")
    quads = {quadrant_of(*t) for t in tiles}
    if len(quads) > 1:
        raise ValueError(f"block spans quadrants {sorted(quads)}; v1 routes inside one quadrant only")

    info = CROP_TABLE[crop_name]
    c_idx = CROPS.index(crop_name)
    prod_idx = PRODUCTS.index(crop_name)
    ordered = serpentine(tiles)
    if water_every < 1:
        raise ValueError("water_every must be at least 1")
    # **How often a tile is visited, which sets how much land one unit can hold.**
    #
    # Watering every tile every day costs about three turns per tile -- the WATER plus the walk -- so a
    # 24-turn day caps a block at four. Six raises. That single default is why our farm is 12-16 crop
    # tiles while the leader works 60-75.
    #
    # The game does not require it. Death needs **two consecutive** dry days (`tiles.py:157`), so one
    # dry day leaves the streak at 1 and the next visit resets it; and base production never tests
    # watering at all (`tiles.py:178` -- watering gates only the fertilizer doubling). So `water_every=2`
    # visits half the tiles each day and legally holds **eight**.
    #
    # It is opt-in per chain because it is not universally good. Measured, one unit, whole season:
    # strawberry 4 daily $6,182 -> 8 alternate $9,395 (**+52%**), melon 4 daily $15,575 -> 8 alternate
    # $11,167 (**-28%**). Strawberry is ongoing and produces on a fixed interval, so it does not care
    # which days it is visited. Melon is one-shot with a window that shuts at `max_day` 12, and a
    # missed visit forfeits the harvest to `decay_plants`. Wheat is worse still at 2-4 days.
    #
    # Why it matters: strawberry is the largest market in the game -- drain 572 at base 120 is $68,640
    # against melon's 140 at 250 for $35,000 -- and filling it needs ~48 tiles. At four tiles a unit
    # that is twelve slots and out of reach; at eight it is six.
    shifts = [ordered[i::water_every] for i in range(water_every)]
    # Default to the top of the bonus-water window: the most yield from one planting. A caller wanting
    # more cycles of a fast crop passes a smaller age explicitly -- that trade is a plan parameter.
    age_to_harvest = info["max_day"] if harvest_age is None else harvest_age
    if age_to_harvest < info["first"]:
        raise ValueError(f"{crop_name} cannot be harvested before age {info['first']}")

    # One parcel per day, for the reason spelled out in `ranch()`, and skippable for the same reason:
    # `decode()` owns the farm-level schedule when more than one chain wants land.
    if buy_land:
        for k in range(land_purchases_for(ordered[0])):
            t = (land_day + k) * TURNS_PER_DAY
            if 0 <= t < script.T:
                script.buy_land[t] = 1

    # `maximum`, not `+=`: co-located routines share the crew, exactly as in `ranch()`.
    for day in range(plant_day, SEASON_DAYS):
        t = day * TURNS_PER_DAY
        if unit > 0 and t < script.T:
            script.hire[t] = max(int(script.hire[t]), unit)

    # Per-tile planting day, so one-shot crops can start a fresh cycle after each harvest.
    planted = {t: None for t in ordered}
    # Last day each tile's fertilizer is still active, so a tile is re-dosed every third day rather
    # than every day. `fertilize` is opt-in: turning it on by default would silently re-price every
    # measurement taken before it existed.
    fertilized_until = {t: -1 for t in ordered}
    # Has this tile already carried a crop of ours? Only then can it have sat EMPTY long enough to
    # catch a weed, and only then is a DIG before the next PLANT worth its turn.
    harvested = {t: False for t in ordered}
    fertilizing = fertilize and crop_name in FERTILIZER_HELPS

    for day in range(plant_day, SEASON_DAYS):
        d = day * TURNS_PER_DAY
        # `Script.op` drops out-of-range turns so a routine may run past the season; the market arrays
        # are raw indexing and must honour the same contract explicitly.
        if d >= script.T:
            break
        jobs = {}
        dig_tiles = []
        # Which tiles this unit reaches today. With `water_every=1` this is the whole block, exactly as
        # before; with 2 it alternates halves, so every tile is visited every second day.
        today = shifts[(day - plant_day) % water_every]
        for tile in today:
            p = planted[tile]
            if p is None:
                # **WATER on the planting day, not from the next one.** A seedling is already at
                # `consecutive_unwatered = 1`, so skipping today's water lets dusk take it to 2 and
                # `_daily_refresh_plants` turns it into a WEED on its first night -- after which WATER
                # (needs `kind == PLANT`) and PLANT (needs `EMPTY`) both silently no-op forever while
                # the routine keeps buying seeds. Traced in `data/logs/crop_trace.log`.
                #
                # **DIG first, but only on a tile we have already cropped once.** `_spawn_weeds` fires
                # at 0.005 per EMPTY tile per turn, so ground that has sat idle for a day carries
                # `1 - 0.995**24` ~ 11% of being a WEED -- and PLANT needs EMPTY, so a weed there
                # kills the tile for the rest of the season, silently, while the seed orders continue.
                #
                # An open-loop tape cannot see which tile weeded, and it does not need to: `dig()`
                # acts only on WEED, PLANT or an empty structure (`ops.py:156`), so on clean ground it
                # is a no-op costing one turn. That is insurance, and it is what the leader does --
                # all 23 of his inspectable digs land on an EMPTY tile and nine of the first twelve
                # are immediately followed by PLANT, WATER
                # (`docs/new_leader_somewhere_after_2026-08-05.md`).
                #
                # Never before a *first* plant: that ground was never idle under us, so the turn would
                # be pure loss. And it is **dropped rather than raising** when the day is full, for
                # the same reason the fertilizing is: a block that fits without insurance must keep
                # fitting, or adding the option would silently shrink the search's reachable board.
                # A 4-tile replant day needs 25 of 24 turns with four digs, so this matters.
                if harvested[tile]:
                    dig_tiles.append(tile)
                jobs[tile] = ["PLANT", "WATER"]
            else:
                age = day - p
                if info["ongoing"]:
                    jobs[tile] = ["WATER"] + (["HARVEST"] if age >= info["first"] else [])
                elif age >= age_to_harvest:
                    # Water first: it still lands inside the bonus window on the harvest day itself.
                    jobs[tile] = ["WATER", "HARVEST"]
                else:
                    jobs[tile] = ["WATER"]

        n_plant = sum(1 for v in jobs.values() if "PLANT" in v)
        if n_plant:
            script.buy_seed[d, c_idx] += n_plant

        fert_tiles = []
        if fertilizing:
            for tile in today:
                if fertilized_until[tile] >= day:
                    continue                    # still active from an earlier application
                if "HARVEST" in jobs[tile] and not info["ongoing"]:
                    continue                    # cleared to EMPTY tonight, so the bonus never lands
                fert_tiles.append(tile)

        def _sequence(fert, digs=()):
            """The day's ops as `(op_name, tile)`, from spawn. Built before writing so the length
            can be checked -- adding fertilizer or a dig must never turn a legal block into a
            raising one."""
            seq = []
            pos = script.where(day, unit, spawn_tile(unit))
            if fert:
                # **Drawn on `SPAWN`, not wherever this unit woke up.** PICKUP needs a shed-access
                # tile that is *unlocked* (`ops.py:216`) and only `(4,4)` is always both, so a hand
                # spawning in NE or SW picked up nothing and every FERTILIZE after it no-opped. The
                # step costs nothing in turns: `_path_ops` routes out through `SPAWN` anyway.
                for op_name in _path_ops(pos, SPAWN):
                    seq.append((op_name, None))
                pos = tuple(SPAWN)
                seq.append(("PICKUP", None))
            for tile in today:
                for op_name in _path_ops(pos, tile):
                    seq.append((op_name, None))
                pos = tile
                if tile in digs:
                    # Immediately before the PLANT, which is the only ordering that helps: it clears
                    # a weed that would otherwise make the PLANT a silent no-op.
                    seq.append(("DIG", tile))
                for op_name in jobs[tile]:
                    seq.append((op_name, tile))
                if tile in fert:
                    seq.append(("FERTILIZE", tile))
            return seq

        # Against the turns *still free* on this unit today, not against a whole empty day: a pen group
        # sharing the unit has already claimed some, and measuring the optional extras against the full
        # day would overflow the claim and raise where dropping the insurance would have fitted.
        budget = script.turns_left(day, unit)
        seq = _sequence(fert_tiles, dig_tiles)
        if dig_tiles and len(seq) > budget:
            # Insurance is the first thing to go: it protects an 11% risk, while overflowing the day
            # pushes work past the dawn teleport and loses it outright.
            dig_tiles = []
            seq = _sequence(fert_tiles, dig_tiles)
        if fert_tiles and len(seq) > budget:
            # Drop the fertilizing rather than raise. A block that fits unfertilized must keep
            # fitting, or switching the option on would silently shrink the search's reachable board.
            fert_tiles = []
            seq = _sequence(fert_tiles, dig_tiles)

        if fert_tiles and buy_fertilizer:
            # **Order it, exactly as the seeds above are ordered.** The PICKUP draws from the shed
            # and nothing else ever stocks it: `ranch()` sells its collected fertilizer the same day,
            # so even a farm with four cows hands the crop unit an empty shed. Without this the
            # FERTILIZE ops are emitted, counted, and refused by `ops.py:378` for want of a carried
            # unit -- which is why `fertilize=1` and `fertilize=0` scored identically to the dollar
            # in all eight slots of the $64,146 genome.
            script.buy_product[d, PRODUCTS.index("FERTILIZER")] += len(fert_tiles)

        # Claim, for the reason spelled out on `Script.claim`: a pen group may share this unit, and
        # writing from `d + 1` regardless is what silently deleted 42% of a combined chain's ops.
        t = script.claim(day, unit, len(seq),
                         what=f"{len(today)} of {len(ordered)} tiles")
        for op_name, _tile in seq:
            if op_name == "PICKUP":
                script.op(t, unit, "PICKUP", item="FERTILIZER", qty=len(fert_tiles))
            else:
                script.op(t, unit, op_name, crop=crop_name if op_name == "PLANT" else None)
            t += 1
        if today:
            script.stand(day, unit, today[-1])
        for tile in fert_tiles:
            fertilized_until[tile] = day + FERTILIZER_ACTIVE_DAYS - 1

        if sell and any("HARVEST" in v for v in jobs.values()):
            # **Next dawn, not this evening.** The harvest is in `carried` until `_drop_to_shed` runs at
            # dusk, so a sell on this day finds an empty shed. Over-requesting is safe --
            # `_process_market` stops when the shed runs dry -- and the cadence itself is a plan
            # parameter, not a fact about the crop.
            n_harvested = sum(1 for v in jobs.values() if "HARVEST" in v)
            t_sell = (day + 1) * TURNS_PER_DAY
            if t_sell < script.T:
                script.sell[t_sell, prod_idx] += info["max_yield"] * n_harvested

        for tile in today:
            if "HARVEST" in jobs[tile]:
                # Records that this ground has been cropped, so its next PLANT gets a DIG first.
                harvested[tile] = True
            if "PLANT" in jobs[tile]:
                planted[tile] = day
            elif "HARVEST" in jobs[tile] and not info["ongoing"]:
                planted[tile] = None       # cleared to EMPTY, so it replants next day

    return script


# ---------------------------------------------------------------------------
# Inspection helpers, used by the tests to check the tape rather than trust it
# ---------------------------------------------------------------------------

def _turns_with(script, unit, op_name):
    return np.flatnonzero(np.asarray(script.unit_op)[:, unit] == OP[op_name])


def feed_days(script, unit):
    return {int(t) // TURNS_PER_DAY for t in _turns_with(script, unit, "FEED")}


def place_day(script, unit):
    ts = _turns_with(script, unit, "PLACE")
    return int(ts[0]) // TURNS_PER_DAY if len(ts) else None


def build_turn(script, unit):
    ops = np.asarray(script.unit_op)[:, unit]
    ts = np.flatnonzero((ops == OP["BUILD_PASTURE"]) | (ops == OP["BUILD_COOP"]))
    return int(ts[0]) if len(ts) else None
