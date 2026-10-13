"""Observations for the per-turn policy: `jax_sim.State` -> per-seat entity tokens.

The policy sees the board as **entities, not a picture**: 100 tile tokens, 24 unit tokens and one
global token, all encoded per seat so self-play can drive both sides from one set of parameters.
That shape is deliberate -- it is what worked for every top finisher whose write-up we have, and
`docs/lessons_carried_over.md` records the entity transformer as the transferable win from Orbit
Wars.

Three encoding decisions worth stating, because each one is a choice and not an accident:

- **The opponent's board is a summary, not 100 more tokens.** `contrarian`'s entire edge is reading
  what the opponent grows and switching off a contested crop, so the information has to be present;
  but which *tile* they used never mattered, only the mix. Fourteen aggregate numbers on the global
  token buy that at a fraction of the attention cost of doubling the sequence.
- **Everything is scaled to roughly unit range**, because the raw quantities span money in the tens
  of thousands and a boolean. Divisors are fixed constants rather than running statistics: a
  normaliser that drifts during self-play makes an old checkpoint silently incomparable.
- **Nothing here is a quality judgment.** These are facts about the state. Anything resembling
  "this tile is a good idea" belongs in the policy, not the features -- hand-built priors in the
  observation are how a heuristic's ceiling gets baked in where nobody can see it.
"""

import jax.numpy as jnp

from kagg.sim import jax_sim as J

N_KINDS = 6           # EMPTY, LOCKED, WEED, PLANT, COOP, PASTURE
_XS = jnp.arange(J.BOARD * J.BOARD) % J.BOARD
_YS = jnp.arange(J.BOARD * J.BOARD) // J.BOARD
N_CROPS = J.N_CROPS
N_ANIMAL_KINDS = len(J.ANIMAL_STRUCTURE)

# The trailing `opponent` block of `glob`: the other seat's board summary. Named because three
# separate things below are expressed relative to it, and a literal 14 in each is three chances to
# drift apart.
_OPPONENT_WIDTH = N_KINDS + N_CROPS + N_ANIMAL_KINDS          # 14

# **These three are asserted against the real arrays by
# `tests/test_train_metrics.py::test_the_declared_feature_widths_match_the_arrays`.** All three had
# gone stale -- UNIT_FEATURES said 16 against an actual 28, unchanged since the nearest-job geometry
# landed, and the handoff even records "Unit features 16 -> 28". Nothing broke, because flax infers
# real shapes at trace time and the only other reader is a printed memory estimate, but a constant
# that lies is the kind of thing that gets trusted later.
TILE_FEATURES = N_KINDS + N_CROPS + N_ANIMAL_KINDS + 13      # 27
UNIT_FEATURES = 4 + J.N_ITEMS + 4 * 3                        # 28
# The `+ 3` before the opponent block is `land_afford`, `hire_afford` and `rehire_afford` -- the
# third arrived with P3 and moved this from 59 to 60. Written as `_OPPONENT_WIDTH` rather than a
# literal 14 so the next feature cannot make this constant lie again.
#: Days in a season, for the day one-hot. 30, and the clip below depends on it.
N_DAYS = 30

# **The clock as one-hots, not only as two smooth scalars.**
#
# `day / 30` and `hour / 24` are kept -- they carry ordering, which a one-hot does not -- but they
# cannot carry identity. A tape-replaying teacher is a ~719-entry lookup keyed on the turn, and that
# target is maximally high-frequency in a scalar that moves 1/24 per step. Nets fit low frequencies
# first, so asking a 3-layer trunk to carve two smooth scalars into 719 bins spends capacity
# manufacturing a positional code that costs 54 floats to hand over.
#
# On-tape the board is itself a strong proxy for the turn -- turn 300 looks nothing like turn 100 --
# which is why plain BC fits at all. **Off-tape, which is precisely where DAgger collects, that
# correlation breaks and the clock is the only reliable key.**
_TIME_WIDTH = J.TURNS_PER_DAY + N_DAYS                       # 24 + 30 = 54

# **Which shops are trading RIGHT NOW.** This was absent, and its absence was load-bearing: the
# `q4_branch` latch that picks which of four tapes the agent replays is literally "the yarn store is
# unlocked", read on day 5 (`q4_branch.py:242`). The student had to reproduce that branch with half
# its input missing, visible only as a lagged town-drain effect on the inventory vector. On the four
# fixed training games that is confounded with game identity, so training looks fine and deployment
# against a fresh draw fails invisibly.
_SHOP_WIDTH = J.N_SHOPS                                      # 8

# **What the board has stopped saying, appended at the END of `glob`.**
#
# Three things, and they share one property: a single turn's observation cannot answer them, so they
# are carried (`jax_sim.State.opp_snapshot`, `unlock_day`) rather than derived.
#
#   snapshot   the opponent's position on days 1, 3 and 5 -- the days we commit. The live opponent
#              block says what they hold NOW; the melon count the agent latched on day 3 is gone
#              from a day-20 board, and it is what picks which of four tapes plays out.
#   shop dates how long each shop slot has been trading. `shop_open` says only whether it is open,
#              and the `q4_branch` latch is "was the yarn store up by day 5" -- a question about a
#              date, unanswerable from a bit.
#   latches    the two branch decisions themselves, stated. The raw numbers above are also present,
#              so a policy is free to find a different rule; this states the one the teacher uses.
#
# **APPENDED, not inserted, and that is load-bearing.** `jax_policy.migrate_params` grows an input
# projection's leading axis by padding with ZERO rows, so every checkpoint fitted on the 122-wide
# `glob` keeps its trained weights and its day-one behaviour is bit-identical. Insert these anywhere
# else and all 122 existing columns change meaning, and every checkpoint silently reads garbage.
_SNAPSHOT_WIDTH = len(J.SNAPSHOT_DAYS) * J.SNAPSHOT_WIDTH
_SHOP_DATE_WIDTH = J.MAX_INSTANCES
_LATCH_WIDTH = 2
_MEMORY_WIDTH = _SNAPSHOT_WIDTH + _SHOP_DATE_WIDTH + _LATCH_WIDTH

#: Column scales for one `seat_summary` row, in its order: kinds, crops, animals, money, units, land.
#: The count blocks use the same divisors as the live opponent block, so a snapshot and a current
#: reading are on one scale and their difference is meaningful without a learned alignment.
_SNAPSHOT_SCALE = jnp.concatenate([
    jnp.full((6,), 100.0), jnp.full((N_CROPS,), 100.0), jnp.full((N_ANIMAL_KINDS,), 20.0),
    jnp.asarray([50_000.0, 24.0, 3.0]),
]).astype(jnp.float32)

#: The shop the `q4_branch` latch turns on (`q4_branch.TRIGGER_SHOP`), and the day it is read.
#: Duplicated from `kagg.search` because `kagg.rl` must not import it; pinned by
#: `tests/test_the_snapshot_days_are_the_days_we_commit.py`.
YARN_STORE_INDEX = 3
Q4_LATCH_DAY = 5
MELON_LATCH_DAY = 3
OPPONENT_MELON = 9
#: Offset of MELON inside the crop block of a `seat_summary` row. Taken from the same table the
#: encoder uses everywhere else, not written as a literal 4.
CROP_INDEX_MELON = __import__("kagg.sim.tiles", fromlist=["CROP_INDEX"]).CROP_INDEX["MELON"]

GLOBAL_FEATURES = (3 + 2 + _TIME_WIDTH + _SHOP_WIDTH + J.N_PRODUCTS * 2 + N_CROPS + J.N_ITEMS
                   + 3 + 3 + _OPPONENT_WIDTH + _MEMORY_WIDTH)        # 122 + 61 = 183

# Fixed scales. Chosen from measured ranges, and frozen so checkpoints stay comparable.
MONEY_SCALE = 50_000.0
PRICE_SCALE = 250.0
INVENTORY_SCALE = 500.0

# **Cost to rebuild a crew of N from the lone farmer every night leaves you with.**
#
# `HIRE_REBUILD_COST[n] == sum(HIRE_COST[:n - 1])`, so index by `n_units` directly. Built as a
# prefix sum rather than computed inline because the quantity is a *table lookup* on the simulator's
# own cost ladder -- deriving it in the encoder would leave two expressions that could drift.
# `[0]` and `[1]` are both 0: a farm with one unit has nothing to re-hire.
HIRE_REBUILD_COST = jnp.concatenate([
    jnp.zeros((1,), dtype=jnp.float32),
    jnp.cumsum(jnp.concatenate([jnp.zeros((1,), dtype=jnp.float32),
                                J.HIRE_COST.astype(jnp.float32)]))[:-1],
])

# Column offsets from the END of `glob`, so inserting a feature above them cannot shift them and
# silently repoint a test or a diagnostic at the wrong number. `opponent` is the trailing block.
# `_MEMORY_WIDTH` is in here because the memory block is appended AFTER the opponent block, so it
# now sits between these three and the end. Leaving it out would repoint all three by 61 columns --
# silently, since every index is still a valid index.
REHIRE_AFFORD_INDEX = -(1 + _OPPONENT_WIDTH + _MEMORY_WIDTH)
HIRE_AFFORD_INDEX = -(2 + _OPPONENT_WIDTH + _MEMORY_WIDTH)
LAND_AFFORD_INDEX = -(3 + _OPPONENT_WIDTH + _MEMORY_WIDTH)


def _one_hot(x, n):
    return (x[..., None] == jnp.arange(n)).astype(jnp.float32)


def encode(state):
    """Return `(tiles, units, glob)` for both seats.

    Shapes are `[B, P, TILES, TILE_FEATURES]`, `[B, P, MAX_UNITS, UNIT_FEATURES]` and
    `[B, P, GLOBAL_FEATURES]`. Seat `p` sees its own farm in full and the other seat in aggregate.
    """
    t, farm = state.tiles, state.farm
    # `[B]`, not a scalar: `jax_sim` keeps `step_index` per game so episodes can run out of phase.
    day = (state.step_index // J.TURNS_PER_DAY).astype(jnp.float32)        # [B]
    hour = (state.step_index % J.TURNS_PER_DAY).astype(jnp.float32)        # [B]
    # Integer copies for the one-hots. The day is clipped rather than wrapped: a step index past the
    # bell must saturate at the last day, not read as day 0 -- `_one_hot` of an out-of-range value
    # is an all-zero row, which is a third meaning nobody wants.
    day_i = jnp.clip(state.step_index // J.TURNS_PER_DAY, 0, N_DAYS - 1)    # [B]
    hour_i = state.step_index % J.TURNS_PER_DAY                            # [B]
    hour_1h = _one_hot(hour_i, J.TURNS_PER_DAY)                            # [B, 24]
    day_1h = _one_hot(day_i, N_DAYS)                                       # [B, 30]
    # Slot-indexed since 1.32.6 draws shops with replacement, so two slots can name the same shop:
    # reduce with a max over slots to get one bit per SHOP, not per slot.
    shop_open = jnp.max(
        _one_hot(state.unlock_shop, J.N_SHOPS)
        * (state.unlock_day <= day_i[:, None])[..., None].astype(jnp.float32),
        axis=1)                                                            # [B, N_SHOPS]
    day_t = day[:, None, None]                                             # against [B, P, TILES]
    day_g = day[:, None]                                                   # against [B, P]

    # ---- tiles ---------------------------------------------------------------------------------
    is_plant = t.kind == J.PLANT
    has_animal = t.animal != J.NO_ANIMAL
    tiles = jnp.concatenate(
        [
            _one_hot(t.kind, N_KINDS),
            _one_hot(jnp.where(is_plant, t.crop, -1), N_CROPS),
            _one_hot(jnp.where(has_animal, t.animal, -1), N_ANIMAL_KINDS),
            (t.yield_units / 8.0).astype(jnp.float32)[..., None],
            t.watered_today.astype(jnp.float32)[..., None],
            (t.consecutive_unwatered / 2.0).astype(jnp.float32)[..., None],
            # Age drives every yield rule, so give it directly rather than making the net subtract.
            jnp.where(is_plant, (day_t - t.planted_day) / 30.0, 0.0)
            .astype(jnp.float32)[..., None],
            # **The same fact for animals, which had been left out.** `t.placed_day` was used
            # nowhere in this file: crops got their age with the comment above explaining why, and
            # the animal half of the identical rule got nothing. `jax_sim`'s production rule is
            #     days_since = day - placed_day - ANIMAL_FIRST_YIELD_DAY[a]
            #     produces   = (days_since >= 0) & (days_since % ANIMAL_INTERVAL[a] == 0)
            # so without age the policy cannot tell a goose that yields tomorrow from one that
            # yields in four days, and has to discover HARVEST timing by trial against a terminal
            # reward. This is the same asymmetry as the `is_ripe` target -- the crop economy had the
            # feature and the animal economy did not -- and the animal ops are the two strongest
            # money predictors in the game (FEED +0.452, CARE +0.441 over 312 real seats).
            jnp.where(has_animal, (day_t - t.placed_day) / 30.0, 0.0)
            .astype(jnp.float32)[..., None],
            # **Turns until this animal next produces**, which is the modulo above precomputed
            # rather than derived through reward. Intervals differ per species -- goose 1, cow 2,
            # sheep 3 -- so the periodicity is not something age alone reveals without also learning
            # a per-species phase. Inverted so "produces today" reads 1 and "far off" reads near
            # zero, matching how the nearest-job distances are scaled.
            #
            # It is a fact, not a judgment: it says when product appears, not that harvesting is
            # what the unit should do.
            (1.0 / (1.0 + jnp.where(
                has_animal,
                jnp.maximum(0, J.ANIMAL_FIRST_YIELD_DAY[jnp.maximum(t.animal, 0)]
                            - (day_t - t.placed_day))
                + jnp.where(
                    (day_t - t.placed_day)
                    >= J.ANIMAL_FIRST_YIELD_DAY[jnp.maximum(t.animal, 0)],
                    (-(day_t - t.placed_day
                       - J.ANIMAL_FIRST_YIELD_DAY[jnp.maximum(t.animal, 0)]))
                    % jnp.maximum(J.ANIMAL_INTERVAL[jnp.maximum(t.animal, 0)], 1),
                    0),
                1000).astype(jnp.float32))).astype(jnp.float32)[..., None],
            (t.fertilized_until_day >= day_t).astype(jnp.float32)[..., None],
            t.fed_today.astype(jnp.float32)[..., None],
            t.cared_today.astype(jnp.float32)[..., None],
            t.fertilizer_available.astype(jnp.float32)[..., None],
            (t.pending_care_bonus / 4.0).astype(jnp.float32)[..., None],
            (t.consecutive_unfed / 2.0).astype(jnp.float32)[..., None],
            # An animal two days unfed escapes tonight; that cliff is worth its own feature.
            (has_animal & (t.consecutive_unfed >= 1)).astype(jnp.float32)[..., None],
        ],
        axis=-1,
    )

    # ---- units ---------------------------------------------------------------------------------
    live = J._ARANGE_UNITS[None, None, :] < farm.n_units[:, :, None]
    pos = farm.unit_pos
    flat = pos[..., 1] * J.BOARD + pos[..., 0]
    on_shed = (flat[..., None] == J.SHED_TILES).any(axis=-1)

    # **Where the nearest job is, given rather than derived.**
    #
    # This file already takes that position elsewhere -- "Age drives every yield rule, so give it
    # directly rather than making the net subtract" -- and it is the move Ender's whole
    # target-selection pipeline is built on: precompute the intercept geometry and hand it to the
    # policy rather than making a transformer learn orbital mechanics from raw positions through
    # reward alone. Ours is the trivial version of the same problem, Manhattan distance on a static
    # 10x10 grid.
    #
    # Measured motivation: over 412,992 owned-unit actions the policy placed 4,591 animals and fed
    # 12, and planted 13,439 crops and harvested 98. Setup actions -- one-shot, on the tile the unit
    # already occupies -- are common; maintenance actions, which require *returning to the same tile
    # on a later day*, are three orders of magnitude rarer. Every unit is reset to spawn each night,
    # so every return is a fresh multi-step walk whose payoff arrives days later, and the chance of
    # sampling one correctly decays exponentially with its length. With 98 successes in 413k actions
    # there is essentially no completed trajectory for the critic to learn from.
    #
    # This is a fact, not a quality judgment: it says where the nearest dry plant is, not that
    # watering is what the unit ought to do. `CLAUDE.md` draws the line at masking to *force* an
    # action, which this does not do -- a unit is free to ignore it, as it is free to ignore `age`.
    def _target(candidate):
        """Signed direction and distance to the nearest tile satisfying `candidate`. [B, P, U, 3]"""
        dx = _XS[None, None, None, :] - pos[..., 0:1]
        dy = _YS[None, None, None, :] - pos[..., 1:2]
        dist = jnp.abs(dx) + jnp.abs(dy)
        masked = jnp.where(candidate[:, :, None, :], dist, 999)
        nearest = jnp.argmin(masked, axis=-1)[..., None]
        found = jnp.take_along_axis(masked, nearest, axis=-1) < 999
        take = lambda a: jnp.take_along_axis(a, nearest, axis=-1)   # noqa: E731
        return jnp.concatenate([
            jnp.where(found, take(dx) / (J.BOARD - 1.0), 0.0),
            jnp.where(found, take(dy) / (J.BOARD - 1.0), 0.0),
            # Distance is inverted so "nothing to do" and "very far" are both near zero, and a job
            # underfoot is 1. A raw distance would make the absent case indistinguishable from a
            # nearby one only by the sign of a separate flag.
            jnp.where(found, 1.0 / (1.0 + take(masked).astype(jnp.float32)), 0.0),
        ], axis=-1).astype(jnp.float32)

    is_plant_t = t.kind == J.PLANT
    needs_water = is_plant_t & ~t.watered_today
    has_animal_t = t.animal != J.NO_ANIMAL

    # **Mirror `jax_masks.HARVEST` exactly, or this points units at jobs they cannot do and hides
    # jobs they can.** The mask is `ripe_plant | (has_animal & units_held > 0)`, and this target
    # was only the crop half of it -- so a unit got a directional pull toward a ripe melon and
    # none at all toward a goose with eggs waiting. FEED has never once fired in 90 updates and
    # animal-product harvest sits with it; giving the crop economy geometry the animal economy
    # does not have would keep it that way by construction.
    #
    # The crop half also dropped the mask's `FIRST_YIELD_DAY` condition, which made it *broader*
    # than legality: it pointed at seedlings carrying yield they are not yet old enough to take.
    # A target that says "go here" for an illegal op is worse than no target -- it spends the walk
    # and then masks the payoff.
    crop_safe_t = jnp.clip(t.crop, 0, N_CROPS - 1)
    ripe_crop = (is_plant_t & (t.yield_units > 0)
                 & ((day_t - t.planted_day) >= J.FIRST_YIELD_DAY[crop_safe_t]))
    is_ripe = ripe_crop | (has_animal_t & (t.yield_units > 0))
    needs_feed = has_animal_t & ~t.fed_today

    # **A dead slot has no position, and the two encoders must agree on what it reads.**
    #
    # `jax_sim.reset` parks the 23 unhired slots on the spawn tile, so their x, y and on_shed read
    # 0.444/0.444/1.0; `adapter.state_from_obs` built them from an observation that has no such
    # units and left them at 0. `live` is 0 either way, but the transformer attends over every
    # token, and 23 tokens differing on three features is not nothing: measured 2026-08-28, the
    # LIVE farmer's op came out 1 through `jax_sim` and 17 through the adapter
    # (`scripts/diff_the_two_ways_a_board_becomes_features.py`).
    #
    # **The fix belongs in `adapter`, and putting it here instead cost a whole training run.**
    # The first attempt multiplied these three columns by `live`, which reads as a tidy one-line
    # fix and is not an append: it CHANGES THE MEANING of three existing unit features. Every
    # checkpoint was fitted with dead slots at 0.444/0.444/1.0. `migrate_params` zero-pads columns
    # that are NEW; it cannot repair a column whose meaning moved, so the warm start's unit
    # projection silently read a different feature than it was trained on. Movement is decoded per
    # unit off this token, and it went to exactly 0.000 across 12,844 WEST, 12,960 NORTH and 10,013
    # EAST labels -- not "learned badly", unreachable.
    #
    # So `adapter` parks its dead slots at spawn to match `jax_sim`, and these three columns are
    # left exactly as every checkpoint knows them.
    units = jnp.concatenate(
        [
            live.astype(jnp.float32)[..., None],
            (pos[..., 0] / (J.BOARD - 1.0)).astype(jnp.float32)[..., None],
            (pos[..., 1] / (J.BOARD - 1.0)).astype(jnp.float32)[..., None],
            on_shed.astype(jnp.float32)[..., None],
            jnp.minimum(farm.carried / 10.0, 3.0).astype(jnp.float32),
            _target(needs_water),
            _target(is_ripe),
            _target(needs_feed),
            _target(t.kind == J.EMPTY),
        ],
        axis=-1,
    )

    # ---- opponent summary ----------------------------------------------------------------------
    # Seat 0's opponent is seat 1 and vice versa, so a reversal along the player axis gives each
    # seat the other's aggregate without materialising two separate encodings.
    kind_counts = jnp.stack(
        [(t.kind == k).sum(axis=-1) for k in range(N_KINDS)], axis=-1) / 100.0
    crop_counts = jnp.stack(
        [((t.kind == J.PLANT) & (t.crop == c)).sum(axis=-1) for c in range(N_CROPS)],
        axis=-1) / 100.0
    animal_counts = jnp.stack(
        [(t.animal == a).sum(axis=-1) for a in range(N_ANIMAL_KINDS)], axis=-1) / 20.0
    board_summary = jnp.concatenate(
        [kind_counts, crop_counts, animal_counts], axis=-1).astype(jnp.float32)
    opponent = board_summary[:, ::-1]
    opp_money = farm.money[:, ::-1]

    # ---- global --------------------------------------------------------------------------------
    prices = (J.price(state.inventory) / PRICE_SCALE).astype(jnp.float32)
    inventory = ((state.inventory - J.INV0) / INVENTORY_SCALE).astype(jnp.float32)
    b = farm.money.shape[0]

    # **What the next purchase costs, as a share of everything the farm has.**
    #
    # `money`, `n_land` and `hires_today` are all present, but no price is. The policy therefore has
    # to learn the lookups `n_land -> {1000, 2000, 4000}` and `hires_today -> mult * fib(n)` through
    # reward alone, and the reward is terminal -- 700 turns after the purchase.
    #
    # Measured motivation: `LAND_PRICES[0] + LAND_PRICES[1]` is exactly $3,000, the opening bank, and
    # both purchases are affordability-legal. A policy that buys two quadrants on day 0 is broke for
    # the remaining twenty-five days, which is precisely what the update-250 replay does -- $3,000 to
    # $0 by day 5, then nothing. Across 312 real seats the median first land purchase is turn 242
    # (day 10) and the top decile buys 1.59 quadrants; the seat that bought three from turn 1 banked
    # $9,443 against the leaders' $130k. So the quadrant is not a bad buy, it is a bad buy *now*, and
    # "now" is a function of the price against the bank.
    #
    # The ratio is the fact the mask already computes and then throws away: `land_ok` tests
    # `money >= LAND_PRICES[n_land]` and exposes only the boolean, so "costs a third of everything"
    # and "costs 3%" are indistinguishable to the policy. This says what it costs, not whether to
    # buy -- the same side of `CLAUDE.md`'s line as `age` and the nearest-job geometry.
    safe_money = jnp.maximum(farm.money, 1.0)
    next_land = J.LAND_PRICES[jnp.minimum(farm.n_land, J.N_LAND - 1)]
    land_afford = jnp.where(farm.n_land < J.N_LAND,
                            jnp.minimum(next_land / safe_money, 4.0), 0.0)
    next_hire = J.HIRE_COST[jnp.minimum(farm.hires_today, J.MAX_UNITS)]
    hire_afford = jnp.minimum(next_hire / safe_money, 4.0)

    # **What the crew already owned costs to KEEP, as a share of the bank.**
    #
    # There is no upkeep line in this game -- `_end_of_day` and `_night` move no money -- but
    # `_night` does `n_units = ones_like(n_units)` (`jax_sim.py:1138`), so the crew is dismissed
    # every night and a crew of N is *rented* at `sum(HIRE_COST[:N-1])` every morning. `HIRE_COST`
    # is Fibonacci: $33/day at eight units, $54 at nine, $143 at eleven, $376 at thirteen.
    #
    # **Measured, this is the largest single drain in the game.** On the stopped `league1`
    # checkpoint the per-day hire column reads -54, -88, -88, -116, -143, -88, -143 through the back
    # half of the season -- crews of 9, 10 and 11 rebuilt each morning -- totalling **-$2,122**
    # against the season's entire gross sales of $2,300. It did not move when the frozen-market bug
    # was fixed, so it is not a pricing artifact.
    #
    # **`hire_afford` above cannot express it, and not by a small margin.** It reads
    # `HIRE_COST[hires_today]`, and `hires_today` resets each morning, so at the moment the day's
    # hiring decision is taken `next_hire` is `HIRE_COST[0]` = **$1** -- identical for a lone farmer
    # and for a crew of eleven. That is a true statement about the *first* hire and says nothing
    # about the $143 the day's programme costs, nor that the same bill falls again tomorrow and
    # every day to the bell.
    #
    # A fact, not a judgment: it states the price of a position already held and expresses no
    # opinion about whether to hold it -- the same side of `CLAUDE.md`'s line as `land_afford`.
    # Clipped at 4.0 like both neighbours, so one ratio cannot dominate the global token when the
    # bank approaches zero; above 4x the bank the crew is unaffordable either way.
    rehire_afford = jnp.minimum(
        HIRE_REBUILD_COST[jnp.clip(farm.n_units, 0, J.MAX_UNITS)] / safe_money, 4.0)

    # ---- the memory block ------------------------------------------------------------------------
    # `NEVER` means "that day has not come yet". It is emitted as ZERO rather than as a huge number:
    # an unset slot must not dominate the token, and zero is what an untrained padded column already
    # contributes, so a checkpoint migrated into this width starts from exactly where it left off.
    raw_snap = state.opp_snapshot.astype(jnp.float32)                  # [B, P, D, W]
    unset = raw_snap >= float(J.NEVER)
    snapshot = jnp.where(unset, 0.0, raw_snap / _SNAPSHOT_SCALE)
    snapshot = snapshot.reshape(snapshot.shape[:2] + (_SNAPSHOT_WIDTH,))

    # How long each slot has been trading, in days, as a fraction of the season. 0 for a slot that is
    # not open yet -- which `shop_open` already says, so the two agree rather than contradict.
    shop_age = jnp.where(state.unlock_day <= day[:, None],
                         (day[:, None] - state.unlock_day) / float(N_DAYS), 0.0).astype(jnp.float32)

    # The two branch decisions, stated. `melon_armed` reads the day-3 snapshot's MELON column, which
    # is the number `melon_branch.trigger` counts; it is 0 before day 3, when the branch is undecided
    # rather than false. `q4_armed` asks whether any slot holding the yarn store opened by day 5 --
    # answerable from `unlock_day` alone, and only since the adapter stopped stamping every open shop
    # day 0 (`adapter.GameMemo`).
    _melon_col = 6 + CROP_INDEX_MELON
    _melon_day = J.SNAPSHOT_DAYS.index(MELON_LATCH_DAY)
    melon_count = jnp.where(unset[:, :, _melon_day, _melon_col], 0.0,
                            raw_snap[:, :, _melon_day, _melon_col])
    melon_armed = ((melon_count >= OPPONENT_MELON)
                   & (day >= MELON_LATCH_DAY)[:, None]).astype(jnp.float32)[..., None]
    yarn_by_d5 = ((state.unlock_shop == YARN_STORE_INDEX)
                  & (state.unlock_day <= Q4_LATCH_DAY)).any(axis=-1)
    q4_armed = (yarn_by_d5 & (day >= Q4_LATCH_DAY)).astype(jnp.float32)

    glob = jnp.concatenate(
        [
            (farm.money / MONEY_SCALE).astype(jnp.float32)[..., None],
            (opp_money / MONEY_SCALE).astype(jnp.float32)[..., None],
            # The lead is the quantity the terminal reward actually turns on, so state it directly.
            ((farm.money - opp_money) / MONEY_SCALE).astype(jnp.float32)[..., None],
            jnp.broadcast_to((day / 30.0)[:, None], (b, 2))[..., None],
            jnp.broadcast_to((hour / 24.0)[:, None], (b, 2))[..., None],
            # **Inserted HERE, above the afford block, and not appended.** `REHIRE_AFFORD_INDEX` and
            # its two neighbours are offsets from the END of `glob` precisely so a new feature
            # cannot silently repoint them; appending would have moved them into this block and
            # `tests/test_rehire_cost_feature.py` reads them.
            jnp.broadcast_to(hour_1h[:, None, :], (b, 2, J.TURNS_PER_DAY)),
            jnp.broadcast_to(day_1h[:, None, :], (b, 2, N_DAYS)),
            jnp.broadcast_to(shop_open[:, None, :], (b, 2, J.N_SHOPS)),
            jnp.broadcast_to(prices[:, None, :], (b, 2, J.N_PRODUCTS)),
            jnp.broadcast_to(inventory[:, None, :], (b, 2, J.N_PRODUCTS)),
            jnp.minimum(farm.seeds / 10.0, 5.0).astype(jnp.float32),
            jnp.minimum(farm.shed / 50.0, 3.0).astype(jnp.float32),
            (farm.n_units / 24.0).astype(jnp.float32)[..., None],
            (farm.n_land / 3.0).astype(jnp.float32)[..., None],
            (farm.hires_today / 12.0).astype(jnp.float32)[..., None],
            land_afford.astype(jnp.float32)[..., None],
            hire_afford.astype(jnp.float32)[..., None],
            rehire_afford.astype(jnp.float32)[..., None],
            opponent,
            # ---- the memory block, appended -- see `_MEMORY_WIDTH` -----------------------------
            snapshot,
            jnp.broadcast_to(shop_age[:, None, :], (b, 2, J.MAX_INSTANCES)),
            melon_armed,
            jnp.broadcast_to(q4_armed[:, None], (b, 2))[..., None],
        ],
        axis=-1,
    )
    return tiles, units, glob
