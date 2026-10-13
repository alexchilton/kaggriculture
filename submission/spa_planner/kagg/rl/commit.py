"""Multi-turn commitments: one decision that spans the walk instead of one per step.

## The problem this exists for, measured

`jax_obs.py` records it: over 412,992 owned-unit actions the policy placed 4,591 animals and **fed
12**, planted 13,439 crops and **harvested 98**. Setup actions -- PLANT, PLACE -- happen on the tile
a unit already stands on, in one action, and the policy does them *more* than the teacher. Every
maintenance action -- WATER, HARVEST, FEED, CARE, COLLECT_FERT -- requires walking back to a tile on
a later turn, and `_end_of_day` resets every unit to spawn, dismisses every hand and empties every
inventory. So the walk is re-motivated from scratch each dawn.

A four-turn walk is four *independent* draws that must all land, and the payoff arrives days later
through a terminal reward the critic explains at `ev_signal < 0.3`. 98 successes in 413k actions
means there is effectively no completed trajectory for the critic to learn from. The policy did not
fail to learn farming; it learned exactly the subset of farming that survives a one-step credit
horizon.

**The spatial half of this was already tried and did not work.** `jax_obs` hands the policy signed
direction and inverse distance to the nearest `needs_water`, `is_ripe`, `needs_feed` and `empty`
tile, on Ender's precomputed-geometry argument. Knowing *where* the job is does not make four turns
of zero reward survive a noisy advantage estimate. The failure was never spatial ignorance.

## What a commitment is, and why it is a fact rather than a judgment

`CLAUDE.md` blesses legality masking -- a statement about what the rules permit -- and forbids
masking for *quality*, which is a statement about what is worth doing. A commitment is on the first
side of that line, and the reason is that it never touches **which** job is chosen: every `COMMIT_*`
token sits in the same categorical as NOOP and every primitive op, drawn from the same distribution,
with no bias toward any of them. What it removes is the requirement to re-choose the same walk on
every intermediate turn. Plant-then-water is a rule of the simulator, not a strategy anyone picked.

Two conditions keep it there, and both are load-bearing rather than stylistic:

- **Every category with a target gets one.** Offering commitment to FEED because FEED is the most
  dramatic gap in the op table would be selective attention, and selective attention is a judgment.
- **`MAX_COMMIT_TURNS` stays small relative to a day.** At a few turns this compresses a
  conjunction. Pushed toward a whole day it starts scripting the unit's schedule, and then any
  win-rate gain belongs to the script rather than to the policy -- which is exactly the
  ceiling-capping failure the standing rule is about. **If a future session finds that raising it
  "works better", that is the signal it has crossed the line, not a tuning result.**

## Why this lives outside `jax_sim`

The commitment state is not part of the game. Putting it in `Farm` would change a simulator whose
whole value is that it matches the reference field for field over 300 full-length episodes, and the
parity gate would be testing a different object than the one Kaggle runs. So this module is an
action *selection* wrapper: it turns the policy's `COMMIT_*` token into the ordinary primitive op a
unit would have submitted anyway, and the simulator never learns commitments exist.

## How the PPO ratio stays exact

A committed unit's intermediate turns are **excluded from the density**, using the same mechanism
`active_unit_heads` already uses for heads an op does not read. They are not scored as
probability 1; they contribute nothing to either side of the ratio, so `exp(0 - 0) = 1` for that
slot by construction. The decision mask is derived from the **stored** commitment state, exactly as
the active set is derived from the stored op, so behaviour and update agree on which turns were
decisions. `tests/test_commit.py` pins that.
"""

from typing import NamedTuple

import jax.numpy as jnp

from kagg.sim import jax_sim as J
from kagg.sim import ops as O

# **Every category with a geometry feature gets a commitment, including PLANT.**
#
# The four `_target()` features in `jax_obs.encode` are `needs_water`, `is_ripe`, `needs_feed` and
# `empty`, and all four are offered here.
#
# PLANT was left out of the first version of this file, on the argument that it is a *setup* op done
# on the tile a unit already stands on and is the one op the policy already does more often than the
# teacher -- so committing to it would spend turns on the thing that is not broken. That argument is
# a claim about what is **worth doing**, which is precisely the quality judgment `CLAUDE.md` draws
# the line at. Offering commitment only to the ops whose absence is dramatic is selective attention,
# and selective attention chosen from a results table is exactly how a "shape" becomes a policy.
# The mechanism is offered uniformly; the policy decides what to use.
#
# CARE and COLLECT_FERT stand on the same animal tiles as FEED, so `needs_feed` geometry carries a
# unit to all three; they are reached by committing to the tile, not by a separate target.
# **`COMMIT_PICKUP` is the fifth, and it is here because of a measurement rather than a hunch.**
#
# FEED consumes one WHEAT from the *unit's own* inventory, and `_end_of_day` empties every unit's
# hands, so the real chain is shed -> PICKUP -> animal -> FEED. With only `COMMIT_FEED` built,
# measured over four game-days of random play on a day-15 board: the FEED op fired 629 times and
# only **144 of those units (22.9%) were carrying wheat**. 77% walked the whole way and fired a
# NOOP. A commitment that reliably delivers a unit to an animal it cannot feed is not a fix.
#
# It is a separate category rather than a two-legged FEED **on purpose**. A commitment that went
# shed-then-animal would be the first one to encode *ordering*, and ordering is where a mechanism
# starts becoming a plan -- the next step is the seven-op animal-acquisition chain, and by then the
# script is the strategy. Each commitment stays "walk to a tile of kind X and do the one legal thing
# there"; chaining two of them is the policy's decision to learn, not ours to hard-code.
COMMIT_WATER, COMMIT_HARVEST, COMMIT_FEED, COMMIT_PLANT, COMMIT_PICKUP = range(5)
N_COMMIT = 5

# The primitive op each commitment fires on arrival.
ARRIVAL_OP = jnp.asarray(
    [O.WATER, O.HARVEST, O.FEED, O.PLANT_OP, O.PICKUP], dtype=jnp.int32)  # noqa

# **Policy op space = the simulator's 18 ops plus one token per commitment.**
#
# The simulator's `N_OPS` is deliberately untouched: `ops.py` is shared with the parity harness, and
# an op the reference has never heard of would make "300/300 exact" a statement about a different
# game. Tokens `>= O.N_OPS` are translated here and never reach `jax_sim`.
N_POLICY_OPS = O.N_OPS + N_COMMIT
NO_COMMIT = -1

# Turns a commitment may run before it is abandoned. Four is a median walk on a 10x10 board with
# units starting at the shed, and a quarter of the 24-turn day -- see the docstring's second
# condition on why this must not grow.
MAX_COMMIT_TURNS = 4

# See `_nearest`: `jax_sim` turns on x64 globally, so every integer here states its width or the
# commitment state silently becomes int64 and `lax.scan`'s carry check rejects it.
IDX = jnp.int32
FAR = jnp.asarray(10_000, dtype=IDX)


class CommitState(NamedTuple):
    """Per-unit commitment, carried alongside `jax_sim.State` in the rollout scan.

    A NamedTuple so it is a pytree and threads through `jit` and `scan` exactly as `State` does.

    `target` is **frozen when the commitment is made** and never recomputed. Re-deriving "nearest
    dry tile" every turn would let the ranking change under the unit as it moves, so it could walk
    between two tiles and arrive at neither -- a live-lock that would look exactly like the failure
    this module exists to fix.
    """

    category: jnp.ndarray   # [B, P, U] int32, NO_COMMIT when free
    target: jnp.ndarray     # [B, P, U, 2] int32, frozen (x, y) at commit time
    turns: jnp.ndarray      # [B, P, U] int32, counts down to 0
    # **The crop is frozen with the target, and for the same reason the target is.**
    # PLANT is the one arrival op that reads an argument. The arrival turn is excluded from the
    # density, so the crop sampled *then* is an unscored draw -- using it would let an unscored
    # sample decide what gets planted. Freezing the crop the policy chose on the commit turn, which
    # IS scored, keeps the decision and its consequence in the same place.
    crop: jnp.ndarray       # [B, P, U] int32
    item: jnp.ndarray       # [B, P, U] int32  -- PICKUP's argument, frozen for the same reason
    qty: jnp.ndarray        # [B, P, U] int32


def init(batch, players=2, units=J.MAX_UNITS):
    """All units free."""
    shape = (batch, players, units)
    return CommitState(
        category=jnp.full(shape, NO_COMMIT, dtype=IDX),
        target=jnp.zeros((*shape, 2), dtype=IDX),
        turns=jnp.zeros(shape, dtype=IDX),
        crop=jnp.zeros(shape, dtype=IDX),
        item=jnp.zeros(shape, dtype=IDX),
        qty=jnp.zeros(shape, dtype=IDX),
    )


def _candidates(state):
    """[B, P, TILES] bool per commitment category: tiles worth walking to.

    **These mirror `jax_masks.unit_op_mask` exactly**, because a target that points at a tile where
    the arrival op is illegal spends the whole walk and then fires nothing. `jax_obs` records that
    same bug being fixed once already -- its HARVEST target covered only the crop half of the mask,
    so units were pulled toward ripe melons and never toward a goose with eggs waiting.
    """
    t = state.tiles
    day = (state.step_index // J.TURNS_PER_DAY)[:, None, None]
    is_plant = t.kind == J.PLANT
    has_animal = t.animal != J.NO_ANIMAL
    crop_safe = jnp.clip(t.crop, 0, J.N_CROPS - 1)
    ripe = is_plant & (t.yield_units > 0) & ((day - t.planted_day) >= J.FIRST_YIELD_DAY[crop_safe])
    # PLANT additionally needs a seed in the shed, which is a farm-level fact rather than a tile
    # one; broadcast it so an empty tile stops being a target the moment the seed runs out.
    has_seed = (state.farm.seeds.sum(axis=-1) > 0)[..., None]
    # PICKUP is legal on a shed tile when the shed holds anything. The shed tiles are fixed board
    # positions, so this candidate is a constant mask gated on stock -- mirroring
    # `jax_masks.PICKUP = on_shed & shed_any`.
    n_tiles = t.kind.shape[-1]
    is_shed = jnp.zeros((n_tiles,), dtype=bool).at[J.SHED_TILES].set(True)
    # No LOCKED term: a shed tile is a standing position and the shed is always owned. This mirror
    # was faithful to `jax_masks` including its bug, and the bug reduced COMMIT_PICKUP to the single
    # tile (4,4) -- the other three shed-access tiles are LOCKED on day 0. See
    # `tests/test_a_hand_can_use_the_shed_from_a_locked_tile.py`.
    shed_ok = is_shed[None, None, :] & ((state.farm.shed.sum(axis=-1) > 0)[..., None])
    return jnp.stack([
        is_plant & ~t.watered_today,                       # WATER
        ripe | (has_animal & (t.yield_units > 0)),         # HARVEST
        has_animal & ~t.fed_today,                         # FEED
        (t.kind == J.EMPTY) & has_seed,                    # PLANT
        shed_ok,                                           # PICKUP
    ], axis=0)                                             # [N_COMMIT, B, P, TILES]


def _nearest(candidate, pos):
    """Nearest candidate tile to each unit, by Manhattan distance. Returns `(xy, found)`.

    Ties break toward the lowest flat index, which is deterministic and therefore reproducible
    between the rollout and any replay of it.
    """
    # **Every dtype here is pinned to int32, and that is load-bearing.**
    # `jax_sim` enables `jax_enable_x64` globally, so a bare `jnp.arange` is int64 and would
    # promote the whole commitment state -- which then fails `lax.scan`'s carry type check with a
    # message about the target, several frames from the actual cause. The same hazard `jax_policy`
    # documents for float32.
    xs = (jnp.arange(J.BOARD * J.BOARD, dtype=IDX) % J.BOARD).astype(IDX)
    ys = (jnp.arange(J.BOARD * J.BOARD, dtype=IDX) // J.BOARD).astype(IDX)
    dx = xs[None, None, None, :] - pos[..., 0:1].astype(IDX)
    dy = ys[None, None, None, :] - pos[..., 1:2].astype(IDX)
    dist = jnp.where(candidate[:, :, None, :], jnp.abs(dx) + jnp.abs(dy), FAR).astype(IDX)
    nearest = jnp.argmin(dist, axis=-1)
    found = jnp.take_along_axis(dist, nearest[..., None], axis=-1)[..., 0] < FAR
    return jnp.stack([xs[nearest], ys[nearest]], axis=-1).astype(IDX), found


def commit_mask(state):
    """[B, P, U, N_COMMIT]: a commitment is legal when a reachable target of that kind exists.

    Legality only -- it says a dry tile exists somewhere, not that watering is the right move. A
    unit already standing on the target may still commit; it arrives on the first step and fires the
    op immediately, which is the same outcome as choosing the primitive op directly.
    """
    cand = _candidates(state)
    live = J._ARANGE_UNITS[None, None, :] < state.farm.n_units[:, :, None]
    found = jnp.stack([_nearest(cand[c], state.farm.unit_pos)[1] for c in range(N_COMMIT)], axis=-1)
    return found & live[..., None]


def _step_toward(pos, target):
    """One primitive move op that reduces Manhattan distance, or NOOP when already there.

    x before y, matching `jax_heuristic._step_toward`, so a committed walk and a heuristic walk
    trace the same path and a divergence between them is a real difference rather than tie-breaking.
    """
    dx = target[..., 0] - pos[..., 0]
    dy = target[..., 1] - pos[..., 1]
    return jnp.where(
        dx > 0, O.EAST,
        jnp.where(dx < 0, O.WEST,
                  jnp.where(dy > 0, O.SOUTH,
                            jnp.where(dy < 0, O.NORTH, O.NOOP))))


def resolve(commit, state, policy_op, policy_crop, policy_item=None, policy_qty=None):
    """Turn policy ops (which may be `COMMIT_*` tokens) into simulator ops.

    Returns `(sim_op, sim_crop, sim_item, sim_qty, new_commit, decided)`:

    - `sim_op` [B, P, U] -- ops in the simulator's 0..17 space, safe to hand to `jax_sim.step`.
    - `sim_crop` / `sim_item` / `sim_qty` -- the argument heads, taken from the commitment when one
      is running and from the policy otherwise.
    - `new_commit` -- commitment state for the next turn.
    - `decided` [B, P, U] bool -- **whether this unit-turn was the policy's decision.** False on the
      intermediate turns of a walk, and those turns are dropped from the PPO density entirely.

    A unit that was already committed ignores `policy_op` completely: it walks, or it arrives and
    fires its op. That is the whole mechanism -- the walk costs one decision, not one per turn.
    """
    pos = state.farm.unit_pos
    busy = commit.category != NO_COMMIT

    # ---- units that were already walking -------------------------------------------------------
    at_target = (pos == commit.target).all(axis=-1)
    cat_safe = jnp.clip(commit.category, 0, N_COMMIT - 1)
    arrive_op = ARRIVAL_OP[cat_safe]
    walk_op = _step_toward(pos, commit.target)
    # Arriving and finding the job already gone -- another unit watered it, the animal was fed --
    # fires the op anyway; `jax_sim` maps an illegal op to NOOP, which is the same outcome as
    # abandoning. Not worth a branch.
    busy_op = jnp.where(at_target, arrive_op, walk_op)
    # The commitment ends when the unit arrives or the timer runs out. `turns` counts the turns
    # still allowed *after* this one.
    busy_done = at_target | (commit.turns <= 1)

    # ---- units that were free and may have just committed ---------------------------------------
    is_commit_token = policy_op >= O.N_OPS
    new_cat = jnp.clip(policy_op - O.N_OPS, 0, N_COMMIT - 1)
    cand = _candidates(state)
    # One gather per category, then select -- `N_COMMIT` is 3, so this is cheaper and far simpler
    # than a dynamic gather, and it keeps every shape static for `scan`.
    nearest = [_nearest(cand[c], pos) for c in range(N_COMMIT)]
    # `[B, P, U, N_COMMIT, 2]` and `[B, P, U, N_COMMIT]`, then select the drawn category.
    all_targets = jnp.stack([n[0] for n in nearest], axis=-2)
    all_found = jnp.stack([n[1] for n in nearest], axis=-1)
    fresh_target = jnp.take_along_axis(
        all_targets, new_cat[..., None, None].repeat(2, axis=-1), axis=-2)[..., 0, :]
    fresh_found = jnp.take_along_axis(all_found, new_cat[..., None], axis=-1)[..., 0]

    # A commit token whose target vanished between the mask and the draw degrades to NOOP rather
    # than to a random primitive: silently substituting a *different* action is how a policy ends up
    # being scored for something it did not choose.
    starts = is_commit_token & fresh_found & ~busy
    free_op = jnp.where(is_commit_token, O.NOOP, policy_op)
    # Commit and arrive on the same turn when the unit already stands on the target.
    starts_at_target = starts & (pos == fresh_target).all(axis=-1)
    free_op = jnp.where(starts_at_target, ARRIVAL_OP[new_cat], free_op)
    free_op = jnp.where(starts & ~starts_at_target, _step_toward(pos, fresh_target), free_op)

    sim_op = jnp.where(busy, busy_op, free_op)

    # ---- next-turn commitment state -------------------------------------------------------------
    keep_busy = busy & ~busy_done
    start_new = starts & ~starts_at_target
    category = jnp.where(keep_busy, commit.category,
                         jnp.where(start_new, new_cat, NO_COMMIT)).astype(IDX)
    target = jnp.where((keep_busy | start_new)[..., None],
                       jnp.where(keep_busy[..., None], commit.target, fresh_target),
                       jnp.zeros_like(commit.target)).astype(IDX)
    turns = jnp.where(keep_busy, commit.turns - 1,
                      jnp.where(start_new, MAX_COMMIT_TURNS, 0)).astype(IDX)
    if policy_item is None:
        policy_item = jnp.zeros_like(policy_crop)
    if policy_qty is None:
        policy_qty = jnp.zeros_like(policy_crop)

    # **Every argument head is frozen at commit time, not just `crop`.**
    # PLANT reads `crop`, PICKUP reads `item` and `qty`, and the arrival turn is excluded from the
    # density -- so any argument taken from that turn would be an *unscored* draw deciding what the
    # unit actually does. One uniform rule rather than a special case per op.
    freeze = lambda old, new: jnp.where(  # noqa: E731
        keep_busy, old, jnp.where(start_new, new, 0)).astype(IDX)
    crop = freeze(commit.crop, policy_crop)
    item = freeze(commit.item, policy_item)
    qty = freeze(commit.qty, policy_qty)

    # A running commitment uses what it decided; a free unit uses what it just chose.
    sim_crop = jnp.where(busy, commit.crop, policy_crop)
    sim_item = jnp.where(busy, commit.item, policy_item)
    sim_qty = jnp.where(busy, commit.qty, policy_qty)

    return (sim_op, sim_crop, sim_item, sim_qty,
            CommitState(category, target, turns, crop, item, qty), ~busy)


def clear_at_night(commit, state):
    """Drop every commitment on a day boundary.

    **Not optional.** `jax_sim._end_of_day` returns every unit to spawn, dismisses every hand and
    empties every inventory, so a walk in progress is invalidated by the reset whatever the timer
    says. Leaving it set would send a unit toward a target it can no longer reach from a position it
    no longer occupies.
    """
    new_day = (state.step_index % J.TURNS_PER_DAY) == 0
    keep = ~new_day[:, None, None]
    return CommitState(
        category=jnp.where(keep, commit.category, NO_COMMIT).astype(IDX),
        target=jnp.where(keep[..., None], commit.target, 0).astype(IDX),
        turns=jnp.where(keep, commit.turns, 0).astype(IDX),
        crop=jnp.where(keep, commit.crop, 0).astype(IDX),
        item=jnp.where(keep, commit.item, 0).astype(IDX),
        qty=jnp.where(keep, commit.qty, 0).astype(IDX),
    )
