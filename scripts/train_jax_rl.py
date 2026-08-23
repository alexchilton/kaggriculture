"""PPO self-play for the per-turn policy, on the batched JAX simulator.

Run:
    python scripts/train_jax_rl.py --batch 512 --updates 2000

## The frame, and the commitments it inherits

- **Terminal reward only: win 1, loss 0.** Alex's call, 2026-08-01, and it now governs every policy
  in the project -- see `CLAUDE.md`, where the old per-step-bank-delta bullet is marked no longer in
  force. It is also what the field did: of the top finishers we have write-ups for, four used a
  terminal signal and none used a per-step bank delta. The ladder is Elo, so a $43k win and a $4k
  win score the same.
- **gamma 0.9987 per turn, which is 0.97 per game-day.** Stated in game-days because that is the
  unit the decision was made in and the unit the horizon is legible in: 0.97^30 = 0.40, so a
  terminal reward still carries 40% of its value at the first turn. Per *turn* 0.97 would be
  0.97^720 = 3e-10, which is no signal at all -- the same number means two completely different
  things depending on the unit, so both are printed at startup.
- **Legality masking, never quality masking.** See `kagg/rl/jax_masks.py`.

## What to watch, in order

1. `ret_std = 0.00` or `ret = 0.00 +/- 0.00` -- **stop everything**. The reward is not reaching the
   algorithm. This is the single most valuable line in the log and it is checked first.
2. `explained_variance` must pass **0.5** early. `CLAUDE.md` makes that a committed kill criterion
   for exactly this frame: below it, the frame is wrong and no amount of tuning fixes it. The
   strategy env clears 0.89, but that is a 30-step problem and clearing it there proves nothing here.
3. `clip_frac` climbing past ~0.3 is the early warning that the step size is too big -- the Orbit
   Wars lesson, where it moved before the return curve did.
4. `entropy` collapsing toward zero early means the policy is committing before it has explored.
   Raise `--ent-coef`, but only one dial at a time.

## Self-play

Both seats are driven by the same parameters, so every game produces two trajectories with exactly
opposite outcomes and the mean terminal reward is 0.5 by construction. That is a *check*, not a
result: if mean reward drifts away from 0.5 the seats are not symmetric and something is wrong with
the seating or the reward assignment.
"""

import argparse
import functools
import json
import pathlib
import pickle
import time

import jax
import jax.numpy as jnp
from jax import lax
import numpy as np
import optax

from kagg.rl import (commit as CM, curriculum, jax_act as A, jax_heuristic as HEUR, jax_obs,
                     jax_carrot as CARROT, jax_homestead as HOME, jax_rancher as RANCH,
                     jax_policy as P, league, net_worth)
from kagg.rl.jax_policy import NEG_INF
from kagg.sim import jax_sim as J
from kagg.sim import ops as O


# The bundle legality mask needs the vocabulary. It is loaded once here rather than threaded through
# every signature: the vocabulary is a global property of a trained model, like a tokenizer, and it
# must be byte-identical across labelling, fitting and play or every bundle index means something
# different. `market_bundles.load_vocab` raises if it is missing rather than inventing one.
_BUNDLE_SELLS = None
_BUNDLE_TABLES = None


def _bundle_sells():
    global _BUNDLE_SELLS
    if _BUNDLE_SELLS is None:
        from kagg.il import market_bundles as _MB
        from kagg.rl import jax_policy as _PP
        _BUNDLE_SELLS = _MB.valid_table(_MB.load_vocab(), pad_to=_PP.N_BUNDLES)
    return _BUNDLE_SELLS


def _bundle_tables():
    """The decode tables `jax_act.to_sim_actions` needs: bundle index -> which orders go out.

    **This trainer had not been run since the argument was added.** `to_sim_actions` gained its
    third parameter in `f75174e` (2026-08-22); this file was last touched in `7f24249` (2026-08-20)
    and still called it with two, so every invocation died in the first traced turn. Padded to the
    head width for the reason `market_bundles.tables` gives -- JAX clamps an out-of-range gather
    under jit rather than raising, so an unpadded table returns a real, confidently-emitted, wrong
    order.
    """
    global _BUNDLE_TABLES
    if _BUNDLE_TABLES is None:
        from kagg.il import market_bundles as _MB
        from kagg.rl import jax_policy as _PP
        _BUNDLE_TABLES = {k: jnp.asarray(v) for k, v in
                          _MB.tables(_MB.load_vocab(), pad_to=_PP.N_BUNDLES).items()}
    return _BUNDLE_TABLES


# TF32 tensor cores for matmuls. Ender runs `--matmul-precision high` by default; JAX's own default
# on this card is the slowest, most precise setting, which buys nothing for a 643k-parameter policy
# whose inputs are already normalised counts.
jax.config.update("jax_default_matmul_precision", "tensorfloat32")

RUN_DIR = pathlib.Path("data/jax_rl_runs")

# Short names for the op census printed each update, in `kagg.sim.ops` code order.
O_NAMES = ("noop", "N", "S", "E", "W", "water", "harv", "plant", "dig", "pick", "drop",
           "place", "feed", "care", "fert+", "fert!", "coop", "pasture")

# **The census runs over the POLICY op space, which is wider than the simulator's.**
#
# `commit.N_POLICY_OPS` is `O.N_OPS + 5`; tokens 18-22 are the `COMMIT_*` macros and are translated
# to primitives before `jax_sim` ever sees them. The census one-hotted over `O.N_OPS`, and
# `jax.nn.one_hot` returns all-zeros for an out-of-range index, so **every COMMIT draw was counted
# as nothing at all** -- the behaviour under test was the one behaviour missing from the log that
# exists to judge it. Worse than a gap: the printed percentages normalise by the primitive total,
# so they were shares of primitive draws wearing the label "share of unit-turns".
COMMIT_O_NAMES = ("cWATER", "cHARV", "cFEED", "cPLANT", "cPICK")
POLICY_O_NAMES = O_NAMES + COMMIT_O_NAMES

# The scripted wheat trader. Buy early, hold, sell late -- measured at $3,989 from a $3,000 start
# with zero crew actions, against a price path that rose $25 -> $46 monotonically because the town
# drains wheat all season and wheat's glut curve is `log`, so it never floors.
TRADER_BUY_UNTIL = 12
TRADER_SELL_FROM = 20
TRADER_LOT = 5

# League priority (Ender's `_select_league_opponent`) lives in `kagg/rl/league.py`, with the pool
# itself. It was duplicated here as three loose constants alongside three parallel lists.
TURNS_PER_DAY = J.TURNS_PER_DAY
EPISODE_TURNS = 719

# How many turns before a terminal count as "near-terminal" for the value-loss share diagnostic.
# Eight is a quarter of the default 32-turn horizon: wide enough that the window usually contains a
# terminal when one is in the slice at all, narrow enough that "near" still means near.
NEAR_TERMINAL_TURNS = 8


def initial_virgin(seeded):
    """Whether a slot's FIRST completed episode should have its reward suppressed.

    **True only for `staggered_states`.** That builds a slot at, say, turn 700 on an *empty* board
    with $3,000 a side, which is a legal state and an impossible position: `won = money > money[::-1]`
    is then decided by the day/board mismatch, and the scripted farmer -- which gates planting on
    `day <= LAST_PLANT_DAY` -- declines to act at all, so both sides stand still and the game scores
    an exact tie worth 0.5. Suppressing that first reward is right.

    **False for a curriculum-seeded slot, and it was wrongly True.** A curriculum board is a real
    recorded position, or `J.reset` at turn 0 for the day-0 rung. Those first episodes are genuine
    results and were being thrown away -- one per slot on every process start *and* on every
    `--resume`, which is exactly the window a human reads after relaunching a run.
    """
    return bool(not seeded)


def warn_if_phases_inert(n_phases, seeded):
    """Say so when `--n-phases` has no effect, because a flag that silently does nothing lies.

    `state = staggered_states(...)` runs at startup and is then overwritten by `state = seed_states`
    whenever a curriculum is set, so under a curriculum `--n-phases` stops controlling episode-start
    staggering entirely -- the mix's own day spread does it instead. The evening handoff listed
    `--n-phases 12` as an active mitigation for P1 on the strength of the flag being on the command
    line.

    Worth stating plainly: staggering changes *when* terminal rows arrive, never what fraction of
    rows they are. No setting of this flag can move P1's ~0.14% terminal density.
    """
    if seeded and n_phases and n_phases > 1:
        print(f"NOTE: --n-phases {n_phases} is INERT under a curriculum -- the seeded states "
              f"replace the staggered ones, so the mix's day spread sets episode phase. It cannot "
              f"change terminal-row density either way.", flush=True)


def staggered_states(batch, n_phases, seed=0):
    """One state whose games start at evenly spread points in the season.

    `jax_sim.State` now keeps `step_index` **per game**, so this is a single state with a phase
    vector -- not, as it was, `n_phases` separate states glued together with `vmap`. That earlier
    shape gave only `n_phases` distinct phases for the whole batch, so terminations still arrived in
    bursts, just smaller ones; and it multiplied the compiled graph by the number of groups, which
    is why compile time went from ninety seconds to over ten minutes. `n_phases` is kept as a knob
    only so a run can deliberately coarsen the spread; the default of one phase per game is what
    the fix is for.

    **This is the fix for the single worst property the first training run had.** `jax_sim.State`
    keeps `step_index` as one scalar for the whole batch, so every game in a state is in lockstep
    and *structurally cannot* desynchronise. With a 64-turn horizon against 719-turn episodes that
    means every game terminates on the same update: terminal reward arrived in one burst roughly
    every eleven updates and was absent from the other ten. The critic therefore spent ten updates
    out of every eleven regressing onto its own predictions -- a bootstrap with no unique fixed
    point at gamma near 1 -- and was measured drifting to a value of 1.315, which is impossible
    when the reward is capped at 1. Raising the batch size does not help at all: it makes the burst
    bigger, not more frequent.

    Holding several states at different phases fixes it without touching the simulator, so parity
    is untouched and does not need re-gating. Each state keeps its own scalar `step_index`, and
    `jax.vmap` runs them together, so the phase axis costs nothing in wall-clock.

    The first episode of each group is a partial one -- a farm at turn 400 with an empty board is a
    valid state but not a typical one -- which is the one-off price of staggering. Every episode
    after that is a full season starting from a genuine reset.
    """
    groups = max(1, min(n_phases, batch))
    idx = np.arange(batch)
    phase = ((idx % groups) * (EPISODE_TURNS + 1)) // groups
    # `reset_with_shops`: a plain `reset` leaves every shop at `NEVER`, which measured a season-long
    # town drain of 140 wheat against the reference's ~700 and held end-of-season wheat at $37
    # instead of $51. Every RL and eval entry point had taken that default.
    return J.reset_with_shops(batch, seed=seed, phase=phase)


def _pack(x):
    """[K, b, P, ...] -> [K*b*P, ...], the layout the network consumes.

    `jax_obs.encode` keeps the seat axis separate, so under vmap it returns four leading axes.
    """
    return x.reshape(-1, *x.shape[3:])


def _pack_flat(x):
    """[K, b*P, ...] -> [K*b*P, ...].

    `jax_act.masks_for` already folds the seat axis into the batch before returning, so its vmapped
    output has one leading axis fewer than `encode`'s. Using the same packer for both silently
    produced `[K*b*P*U, N_OPS]` and only surfaced as a broadcast error two frames later.
    """
    return x.reshape(-1, *x.shape[2:])


def ema_update(target, params, decay):
    """Slow-moving copy of the parameters, for bootstrap targets.

    The critic regresses onto targets built from its own predictions at the truncation boundary, so
    any bias there is baked into the next round of targets -- a feedback loop with no anchor. Phase
    staggering is the real fix, because it puts a genuine terminal reward in every update; an EMA
    target is the belt to that pair of braces, decoupling "the thing being regressed toward" from
    "the thing being updated". `decay = 0` disables it, which is the default: it is a second change
    to the same mechanism, and this project's own rule is one delta at a time.
    """
    if not decay:
        return params
    return jax.tree_util.tree_map(lambda t, p: decay * t + (1.0 - decay) * p, target, params)


# **Who holds seat 1, as a property of the episode rather than of the update.**
#
# This used to be four boolean arrays recomputed in the Python loop every update. The game state,
# however, persists across updates: a season is 720 turns and `--horizon` is 32, so a game spans
# ~22.5 updates and its seat-1 role was re-drawn on every one of them. Measured over one season's
# worth of updates, a single game faced a mean of **4.9 distinct opponents**, e.g.
#
#   opp idle farm self trade opp self farm opp self farm self trade farm self farm opp self ...
#
# Three things followed, and the third is the one that matters:
#
#  - The per-opponent win rate was measuring nothing. `farm:0.445/91x` meant "games that happened to
#    carry the farm label on their *final* update", and those games spent 30% of their season
#    against the farmer.
#  - It is why all four columns read ~0.5. For 35% of updates seat 1 is driven by the live policy,
#    which spends its stake down to $0, so both seats finish near zero, `money == money` holds, and
#    the tie pays 0.5. Four labels, one number: the draw rate of two starved farms.
#  - **The opponent ladder did not exist.** The farmer cannot bank its $23,783 while holding the
#    seat for 30% of updates with the policy dismantling the farm in between, so the policy had
#    never played a full game against *any* coherent opponent. Verified against a replay of the
#    update-250 checkpoint: played properly to completion it loses 32/32 and banks $0 against the
#    farmer's $30,292, while the log claimed 0.445.
#
# So the role is drawn when a game resets and held until it terminates. It has to live in the scan
# carry rather than in the Python loop, because restarts happen inside the scan.
#
# Shares are now sampled rather than partitioned exactly, which gives up the exactness the strided
# permutation was written for -- at batch 256 the realised share of a p=0.30 role has an s.d. of
# ~2.9%, and `role_counts` logs what actually happened so this is checked rather than assumed.
(ROLE_SELF, ROLE_POOL, ROLE_FARM, ROLE_TRADE, ROLE_IDLE, ROLE_RANCH, ROLE_CARROT,
 ROLE_HOME, ROLE_TAPE) = range(9)
N_ROLES = 9
ROLE_NAMES = ("self", "pool", "farm", "trade", "idle", "ranch", "carrot", "home", "tape")

# One list, because the per-opponent census and the opponent-by-day cross-tab have to agree on
# both the names and the order or the two views of the same rows disagree silently.
OPPONENT_FLAGS = (("idle", "vs_idle"), ("trade", "vs_trade"), ("farm", "vs_farm"),
                  ("ranch", "vs_ranch"), ("carrot", "vs_carrot"), ("home", "vs_home"),
                  ("pool", "vs_pool"), ("tape", "vs_tape"))
OPPONENT_NAMES = tuple(n for n, _ in OPPONENT_FLAGS)

PRODUCT_NAMES = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON",
                 "EGG", "MILK", "WOOL", "FERTILIZER")

# `market.py` builds `ITEMS = PRODUCTS + ANIMALS` in exactly this order, and `jax_sim.N_ITEMS`
# is that same length, so the PICKUP census and the `item` action head share one index space.
# The pickup line printed twelve bare decimals against that space, which is unreadable in the
# only place the wheat-versus-animal question can be answered.
ANIMAL_NAMES = ("GOOSE", "COW", "SHEEP")
ITEM_NAMES = PRODUCT_NAMES + ANIMAL_NAMES

# **Teacher market rates -- a reference column, explicitly NOT a target.**
#
# Share of turns carrying a non-zero order, measured over the 17,975 rows of `bc_top25.npz` (the
# top-25 leaderboard seats). Printed beside our own rates because "is 0.24 a lot?" is unanswerable
# without something to compare to.
#
# **These are day-2 numbers from a 62-day competition** (launched 2026-07-30). The field will move,
# and `CLAUDE.md` records the standing rule that a teacher is a sparring partner and never the
# final policy -- so a gap against this column is information, not an error to correct. Two entries
# are worth knowing regardless of meta, because they are arithmetic rather than fashion:
#
#   - the teacher BUYS fertilizer on exactly 0.000 of turns and SELLS it on 0.179. It is collected
#     free from animals with COLLECT_FERT. Buying it is buying what they harvest and sell.
#   - the teacher BUYS wheat on 0.455 of turns, its single most common market action, because wheat
#     is the input to the animal economy -- bought cheap, fed to livestock, sold on as milk and wool
#     at ~83% of the winner's revenue.
TEACHER_BUY = (0.455, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.000)
TEACHER_SELL = (0.367, 0.021, 0.002, 0.019, 0.023, 0.001, 0.070, 0.093, 0.179)


def _blend_seat(mine, theirs, seat_mask):
    """Put `theirs`'s actions on the masked seat, field by field, on a `jax_sim.Actions`.

    **A heuristic opponent leaves `order_op/order_item/order_qty` as None.** It has no explicit
    order SEQUENCE, only per-product vectors, while `to_sim_actions` fills those columns for the
    policy -- so a plain `tree_map` over the two pytrees hands `jnp.where` a None and dies. That is
    what had killed this trainer outright since `f75174e` (2026-08-22).

    Dropping the columns for the whole batch would also take the sequence away from the POLICY's
    seat, and the sequence is load-bearing: the environment settles slots in order, measured at
    bank $484 with a sheep missing against the tape's $13 on one turn of the teacher's opening.

    `_explicit_orders` (`jax_sim.py:947`) keys presence off `order_op` **per seat** --
    `(e_op != ORDER_NONE).any(axis=2)` is `[B, P]` -- so writing ORDER_NONE into the heuristic's
    seat makes exactly that seat fall back to the canonical `_order_book` derivation from its
    vectors, while the policy's seat keeps its explicit list. `ORDER_NONE` is 0, which is also what
    `Actions`' own default columns hold.
    """
    def one(a, b):
        if b is None:
            b = jnp.zeros_like(a)                  # ORDER_NONE: this seat falls back
        return jnp.where(seat_mask.reshape(seat_mask.shape + (1,) * (a.ndim - 2)), b, a)

    return mine._replace(**{f: one(getattr(mine, f), getattr(theirs, f))
                            for f in J.Actions._fields})


def make_rollout(model, batch, horizon, gamma, gae_lambda, n_phases, shaping_coef=0.0,
                 tape_actions=None):
    """Build the jitted rollout: `horizon` turns of self-play across all phase groups, plus GAE.

    `gamma` and `gae_lambda` are pinned to float32. A bare Python float promotes to float64 under
    the x64 flag `jax_sim` sets, and `gamma * next_value` would then drag the whole advantage and
    return computation into float64 -- which this card runs at 1/32 rate. See `jax_policy.DTYPE`.

    `tape_actions` is `{head: [n_tapes, EPISODE_TURNS, ...]}` from
    `scripts/build_opponent_tape_actions.py` -- 31 real recorded seats, replayed by turn index at
    seat 1 wherever the role is `ROLE_TAPE`. None disables the role.
    """
    gamma = jnp.asarray(gamma, dtype=jnp.float32)
    gae_lambda = jnp.asarray(gae_lambda, dtype=jnp.float32)
    # Even-numbered envs are the early-game ones, matching Ender's split exactly.
    is_early = (jnp.arange(batch) % 2) == 0
    _EARLY_ROWS = jnp.repeat(is_early, 2)         # [B*2], for splitting per-seat statistics

    # **The tape a slot faces is its slot index, not a draw.** A per-episode draw would have to ride
    # in the scan carry beside `roles`; keying off the slot makes it sticky by construction and
    # touches nothing. `batch` and `n_tapes` are coprime often enough that the pairing with the
    # staggered start phase cycles over `lcm(batch % n_tapes ...)` rather than repeating -- and the
    # slot's board seed varies independently, so a tape is not welded to one board.
    _TAPE_IDS = None if tape_actions is None else jnp.arange(batch) % len(tape_actions["op"])
    _TAPE_LAST = None if tape_actions is None else (tape_actions["op"].shape[1] - 1)

    # **Built here, eagerly, and NOT lazily inside the scan.** A lazy global whose first call lands
    # inside `one_turn` caches the tracer, which then escapes the transformation and raises
    # `UnexpectedTracerError` on the next update. Binding it in `make_rollout`'s own body -- which
    # runs before anything is traced -- makes the closure capture concrete arrays.
    _TABLES = _bundle_tables()

    @functools.partial(jax.jit, static_argnums=())
    def rollout(params, value_params, opp_params, roles, role_logp, virgin,
                early_limit, state, key, seed_states):
        def one_turn(carry, _):
            state, roles, virgin, key, cmt = carry
            key, sub = jax.random.split(key)

            # Seat-1 role, held for the life of the episode. Derived here rather than passed in, so
            # every use below reads the same per-game value the reward will later be attributed to.
            use_opp = roles == ROLE_POOL
            use_farm = roles == ROLE_FARM
            use_trade = roles == ROLE_TRADE
            use_idle = roles == ROLE_IDLE
            use_ranch = roles == ROLE_RANCH
            use_carrot = roles == ROLE_CARROT
            use_home = roles == ROLE_HOME
            use_tape = roles == ROLE_TAPE

            # Observations are stored, not recomputed: the update needs exactly the inputs the
            # behaviour policy saw, and re-encoding from a later state would silently score the
            # actions against the wrong observation.
            tiles, units, glob = jax_obs.encode(state)         # [B, P, ...]
            obs = (A._flat(tiles), A._flat(units), A._flat(glob))
            heads, _v_self = model.apply(params, *obs)
            # Values for the bootstrap come from `value_params`, which is either the live params
            # (default) or a slow EMA copy. Actions always come from the live policy.
            _h_t, value = model.apply(value_params, *obs)
            masks = A.masks_for(state, _bundle_sells())
            actions, logp, _ent = A.sample(sub, heads, masks)

            # **Opponent pool.** In pure self-play both seats share parameters, so a mutual draw is
            # a stable outcome that no gradient pushes against: 0.5 is a perfectly good return when
            # the opponent is a mirror, and it can be reached by both sides simply declining to
            # take risk. Seating a frozen past self opposite the live policy in some groups removes
            # that fixed point -- the frozen side does not co-operate in standing still.
            key, kopp = jax.random.split(key)
            opp_heads, _ = model.apply(opp_params, *obs)
            opp_actions, _olp, _oent = A.sample(kopp, opp_heads, masks)

            # `use_opp` is per phase group. Seat 0 is always the live policy; seat 1 is the frozen
            # opponent wherever the flag is set, so those groups produce genuine cross-play.
            seat = jnp.arange(2)[None, :]
            take_opp = (use_opp[:, None] & (seat == 1))
            take_opp = jnp.broadcast_to(take_opp, (batch, 2)).reshape(-1)
            actions = jax.tree_util.tree_map(
                lambda mine, theirs: jnp.where(
                    take_opp.reshape((-1,) + (1,) * (mine.ndim - 1)), theirs, mine),
                actions, opp_actions)

            # **A seat that does nothing, and it is not a joke opponent.**
            #
            # Self-play against a frozen *self* cannot escape a mutual draw: both sides share the
            # failure, so neither is ever punished for it. Measured over 15 updates, `ret` sat at
            # 0.4925 with a standard deviation of **0.0030** -- a mix of wins and losses would be
            # near 0.5 -- so essentially every game was ending in a draw. `ev_signal` was `n/a` on
            # 8 of 12 updates for exactly that reason: all terminal rewards equal 0.5, so there is
            # no variance to explain, and the win rate was climbing toward 0.5 from below because
            # 0.5 *is* the draw value. It was converging to do-nothing, not learning to win.
            #
            # The cure does not need `contrarian` and cannot use it: a Python heuristic cannot run
            # inside a compiled scan, and the adapter bridges dicts *into* a State, not out. It
            # needs an opponent that merely refuses to lose money. `eval_policy` has the policy
            # ending a season on **$7 against a $3,000 start**, so a seat that passes every turn
            # and banks its opening $3,000 beats it outright, and the draw is broken.
            #
            # `NOOP` is op 0 and bucket 0 of every market head is quantity 0, so all-zeros *is*
            # that agent -- no network, no parameters, nothing to keep in sync.
            take_idle = jnp.broadcast_to(
                use_idle[:, None] & (seat == 1), (batch, 2)).reshape(-1)
            actions = jax.tree_util.tree_map(
                lambda a: jnp.where(
                    take_idle.reshape((-1,) + (1,) * (a.ndim - 1)), 0, a),
                actions)
            # **A seat that replays a real recorded player, by turn index.**
            #
            # Every other opponent here is a heuristic, and the measured ceiling of that whole
            # family is about $15k -- so "beat the pool" is a question about $15k play, while the
            # ladder is decided at $130k-$180k. These 31 seats are downloaded games: the actions a
            # human-designed schedule actually sent, including its market cadence.
            #
            # Time-indexed, not state-conditioned. On a board the student has pushed far off the
            # tape's own line the recorded action can be a no-op or a refused purchase, and the
            # simulator will simply reject it. That is acceptable for an OPPONENT -- it degrades
            # toward a weaker player rather than toward an illegal one -- and it is exactly why the
            # same tapes cannot serve as a DAgger teacher, which needs a correct label rather than a
            # plausible one.
            #
            # 5.39% of the recorded turns carry a market bundle the 151-entry vocabulary cannot
            # express; those fall to EMPTY, so the tape opponent drops about one trade in twenty.
            if tape_actions is not None:
                idx = jnp.clip(state.step_index, 0, _TAPE_LAST)          # [B]
                take_tape = jnp.broadcast_to(
                    use_tape[:, None] & (seat == 1), (batch, 2)).reshape(-1)
                replayed = {}
                for head, mine in actions.items():
                    table = tape_actions.get(head)
                    if table is None:
                        replayed[head] = mine
                        continue
                    picked = table[_TAPE_IDS, idx]                       # [B, ...]
                    theirs = jnp.broadcast_to(
                        picked[:, None], (batch, 2) + picked.shape[1:]
                    ).reshape((batch * 2,) + picked.shape[1:])
                    replayed[head] = jnp.where(
                        take_tape.reshape((-1,) + (1,) * (mine.ndim - 1)),
                        theirs.astype(mine.dtype), mine)
                actions = replayed

            take_opp = take_opp | take_idle | jnp.broadcast_to(
                (use_trade | use_farm | use_ranch | use_carrot | use_home | use_tape)[:, None]
                & (seat == 1),
                (batch, 2)).reshape(-1)

            # **Commitments are resolved here, between the policy and the simulator.**
            #
            # `actions["op"]` may hold a `COMMIT_*` token, which `jax_sim` has never heard of.
            # `commit.resolve` turns it into the primitive the unit would have submitted anyway --
            # a step along the frozen path, or the arrival op -- and reports which unit-turns were
            # the policy's own decision. The undecided ones are dropped from the density below, so
            # the PPO ratio never compares an action the policy did not choose.
            u32 = lambda k: A._unflat(actions[k], batch).astype(jnp.int32)   # noqa: E731
            sim_op, sim_crop, sim_item, sim_qty, cmt_next, decided = CM.resolve(
                cmt, state, u32("op"), u32("crop"), u32("item"), u32("qty"))
            sim_actions = A.to_sim_actions(actions, batch, _TABLES)._replace(
                unit_op=sim_op.astype(J._I), unit_crop=sim_crop.astype(J._I),
                unit_item=sim_item.astype(J._I),
                unit_qty=P.UNIT_QTY_BUCKETS[sim_qty].astype(J._I))

            # **Re-score the behaviour log-prob against the decision mask, or the ratio is a lie.**
            #
            # `A.sample` above ran before commitments were resolved, so its `logp` still counts the
            # unit-turns that turned out to be walk steps -- while `A.evaluate` in the update will
            # drop them. Storing the un-masked number would make `exp(new - old)` a comparison of
            # two different sums on every turn a commitment was running: no error, no NaN, just a
            # gradient pointing somewhere arbitrary. Re-scoring costs nothing (same heads, same
            # masks, no second forward pass) and routes both sides through the one `_score`.
            decided_flat = A._flat(decided)
            logp, _ent = A.evaluate(heads, masks, actions, decided_flat)

            # **A seat that trades wheat and nothing else, so the draw stops being available.**
            #
            # The idle opponent above cannot fix the collapse, because it *is* the collapse: two
            # sides doing nothing draw at exactly $3,000 each, and a draw pays 0.5 against a maximum
            # of 1. Ender never faced this as cleanly -- in his game standing still still loses
            # ground, while here an idle farm is a stable fixed point.
            #
            # This one ends the season ahead. Measured directly: an agent that PASSes every unit and
            # only buys wheat early and sells it late banks **$3,989** against a $3,000 start, using
            # zero crew actions -- `BUY_PRODUCT` and `SELL` are absent from `_apply_unit_action` and
            # settle in the market phase, so they cost nothing a farmer could otherwise be doing.
            # The price path is what makes it free money: the town drains wheat all season and
            # `above_func` is `log`, so it never floors. Measured $25 -> $46 monotonically.
            #
            # So a do-nothing policy now *loses* to this seat rather than drawing with it, which is
            # the whole point: it removes the 0.5 payoff for inaction instead of trying to
            # regularise around it.
            day = state.step_index // J.TURNS_PER_DAY
            trade_seat = jnp.broadcast_to(
                use_trade[:, None] & (seat == 1), (batch, 2))
            buy = (day < TRADER_BUY_UNTIL)[:, None] & trade_seat
            sell = (day >= TRADER_SELL_FROM)[:, None] & trade_seat
            wheat = O.WHEAT_ITEM

            def _set(arr, rows, col, value):
                return arr.at[:, :, col].set(jnp.where(rows, value, arr[:, :, col]))

            sim_actions = sim_actions._replace(
                unit_op=jnp.where(trade_seat[..., None], O.NOOP, sim_actions.unit_op),
                buy_product=_set(sim_actions.buy_product, buy, wheat, TRADER_LOT),
                sell=_set(sim_actions.sell, sell, wheat, TRADER_LOT),
                # 0, not False: `hire`/`buy_land` are integer counts, so a bool literal here would
                # force the whole array back to bool and collapse any count above one.
                hire=jnp.where(trade_seat, 0, sim_actions.hire),
                buy_land=jnp.where(trade_seat, 0, sim_actions.buy_land),
            )

            # **The only opponent in the pool that can punish a bad farm.**
            #
            # It banks $23,783 over a season against the trader's $3,368 and the idle seat's
            # $3,000, and it runs natively here rather than through a callback -- see
            # `kagg/rl/jax_heuristic.py`. The idle and trader seats are beatable by a fixed amount,
            # so they are a floor; this one has actual play in it.
            # **The only opponent in the pool that uses the animal economy.**
            #
            # `jax_rancher` banks $12,078 against the scripted farmer's $23,783, so it is the
            # WEAKER opponent on money -- and that is not the point. Every other seat in this
            # rollout has FEED, CARE and COLLECT_FERT at exactly 0.00%, so nothing the policy ever
            # faces is punished for ignoring the half of the game that `CLAUDE.md` measures as the
            # half that wins (FEED +0.452, CARE +0.441 over 312 real seats). A trainee can climb
            # the whole pool without ever meeting a herd.
            #
            # It has existed, JAX-native and jit-safe, since 2026-08-01 and was wired only into
            # `bc_dagger`. This is the first run that plays against it.
            # **The carrot fleet, a port of a public Kaggle baseline.** It banks $3,410 from
            # $3,000 against `jax_heuristic`'s $23,783, so it is by far the weakest farmer here --
            # and that is the point. Outcome variance is `p(1 - p)`, so an opponent the policy is
            # *near* teaches more per game than one permanently above it, and this one sits just
            # above the $3,000 an idle seat holds and just above what the policy currently manages
            # from a real start. It also differs in kind rather than dial: melon on 16 tiles over a
            # long cycle against carpeting every tile with carrot on a three-day one, which is the
            # tempo diversity `CLAUDE.md` says this pool has never had.
            carrot_seat = jnp.broadcast_to(use_carrot[:, None] & (seat == 1), (batch, 2))
            sim_actions = _blend_seat(sim_actions, CARROT.actions(state), carrot_seat)

            ranch_seat = jnp.broadcast_to(use_ranch[:, None] & (seat == 1), (batch, 2))
            sim_actions = _blend_seat(sim_actions, RANCH.actions(state), ranch_seat)

            # **The only seat that farms and ranches at once.** Every other opponent is a
            # specialist, so a trainee can climb the whole pool without meeting a board that both
            # contests the crop market and keeps livestock. It is composed from the two above rather
            # than ported -- weaker than `farm` on bank ($24,957 vs $30,292, 0/48) and here for its
            # strategy class, not its strength. See `kagg/rl/jax_homestead.py`.
            home_seat = jnp.broadcast_to(use_home[:, None] & (seat == 1), (batch, 2))
            sim_actions = _blend_seat(sim_actions, HOME.actions(state), home_seat)

            farm_seat = jnp.broadcast_to(use_farm[:, None] & (seat == 1), (batch, 2))
            sim_actions = _blend_seat(sim_actions, HEUR.actions(state), farm_seat)
            nxt = J.step(state, sim_actions)

            # `just_done` is [B]: every game crosses its own episode boundary on its own turn,
            # which is the whole point. Paid on the transition, never on the level --
            # `step_index > LAST_STEP` stays true afterwards, so testing it directly would pay the
            # terminal reward on every remaining turn of the rollout.
            was_over = state.step_index > J.LAST_STEP                 # [B]
            now_over = nxt.step_index > J.LAST_STEP
            just_done = now_over & ~was_over

            # **Early-game envs: replay the opening over and over instead of once a season.**
            #
            # Ender dedicates half his rollout envs to this -- "when they reach this many env
            # turns, they truncate, bootstrap from the pre-reset state, and immediately reset into
            # a fresh game". Our phase staggering spreads *terminations* so they do not arrive in a
            # burst, which is a different problem: it does nothing to concentrate gradient on the
            # opening, which is diluted one-turn-in-720 across a season.
            #
            # The opening is exactly where our chain breaks -- buy seed, walk out, plant, water it
            # for days. Training on it constantly is the cheapest way to make that sequence common
            # enough to learn.
            #
            # **A truncation is not a termination and must not be treated as one.** There is no
            # terminal reward, and the trace is cut while the *bootstrap survives*: the value of
            # the state we stopped in is a real estimate of what the rest of that season was worth,
            # and zeroing it would teach the policy that the season ends at turn 150 with nothing.
            early = jnp.asarray(early_limit) > 0
            truncate = early & is_early & (nxt.step_index >= early_limit) & ~just_done

            money = nxt.farm.money                                    # [B, 2]
            won = (money > money[:, ::-1]).astype(jnp.float32)
            tie = (money == money[:, ::-1]).astype(jnp.float32)

            # **A phase-seeded episode's first ending is not a result, and must not be paid.**
            #
            # `staggered_states` starts game `i` at turn `phase(i)` on an EMPTY board with $3,000 a
            # side (`jax_sim.py:329-341` moves `step_index` and nothing else), so a slot seeded at
            # turn 700 terminates twenty turns later having played twenty turns, and
            # `won = money > money[::-1]` is then decided by an artifact of the day/board mismatch
            # rather than by play. The scripted farmer makes it worse in a way that is easy to miss:
            # its own logic reads `day = step_index // TURNS_PER_DAY` and gates planting on
            # `day <= LAST_PLANT_DAY` (`jax_heuristic.py:179`), so on a fresh board that claims to be
            # day 29 it declines to plant or hire at all. Both sides therefore stand still and the
            # game is scored as an exact tie -- which pays 0.5.
            #
            # This fires on **every** run start, not only on a resume: `staggered_states` runs
            # unconditionally at startup, before the `--resume` branch. One illegitimate terminal
            # reward per game slot, every time the process starts.
            #
            # A truncation is already handled correctly a few lines down -- no reward, bootstrap
            # kept. This is the same treatment for the same reason, so `virgin` tracks whether a
            # slot has yet completed a genuine reset-to-turn-0 episode.
            reward = jnp.where(
                (just_done & ~virgin)[:, None], won + 0.5 * tie, 0.0).astype(jnp.float32)

            # **Potential-based shaping on net worth, filling the zeros the terminal reward leaves.**
            #
            # There is no new pathway here: `reward` is already a per-turn `[B, 2]` slot that happens
            # to hold 0.0 on 718 of 719 turns, and GAE already consumes it every turn. This fills it.
            #
            # `F(s, s') = gamma * PHI(s') - PHI(s)` leaves the optimal policy **provably** unchanged
            # (Ng, Harada & Russell 1999); at gamma 1.0 the terms telescope to `PHI(end) - PHI(start)`,
            # so it cannot pay for a detour. That is what makes it categorically different from the
            # per-step bank delta `CLAUDE.md` marks NO LONGER IN FORCE -- that one *was* the reward and
            # changed the objective to margin maximisation, which an Elo ladder does not score.
            #
            # Net worth rather than cash, because a cash potential punishes the animal chain at the
            # moment of investment -- see `kagg/rl/net_worth.py`. At `shaping_coef 0.0` this term is
            # byte-exactly zero and the run is identical to one made before it existed.
            #
            # **Suppressed on the terminal turn**, for the same reason the terminal reward is
            # suppressed on a virgin slot: `nxt` there is the *reset* board, so `PHI(after)` would be
            # the opening stake and the difference would book the whole season's net worth as a loss on
            # its last turn. The telescoping still holds within an episode; only the seam is dropped.
            if shaping_coef:
                shaped = net_worth.net_worth_shaping(state, nxt, coef=shaping_coef)
                reward = reward + jnp.where(just_done[:, None], 0.0, shaped).astype(jnp.float32)

            # Restart inside the scan, per group. Resetting only in Python after the rollout lets
            # the simulator keep stepping past turn 719 into a season that does not exist, and
            # those invalid turns would still be trained on. The PRNG key carries across so a new
            # episode does not replay the old one's weed draws.
            # Only the per-game fields are selected. `key` and `unlock_day` are not per game --
            # the PRNG key is a single [2] array for the whole state -- so a blanket tree_map over
            # the State tries to broadcast a [B] mask against it and fails.
            # **What a restarting slot restarts INTO.** Without a curriculum this is `J.reset`,
            # an empty farm at turn 0. With one it is a real recorded board part-way through a
            # winner's season, and the difference is the whole experiment.
            #
            # It is passed in rather than built here because building it parses replay JSON on the
            # host, which cannot happen inside a jitted scan -- and because the schedule changes it
            # only every few hundred updates, so rebuilding per update would dominate the run.
            #
            # The reward is untouched: still win/lose at the end of the season. What changes is the
            # state distribution, not the signal. That distinction is the reason this is not the
            # banned thing -- potential-based shaping is provably equivalent to initialising the
            # value function (Wiewiora 2003), so importing a hand-designed intermediate value would
            # be shaping through another API; changing where episodes begin is not, because the
            # agent still has to win from wherever it lands and is judged only on whether it did.
            #
            # Measured property that makes this work: seeded at day 15 and left alone, a board goes
            # from 22 crops and 19 animals to zero of each within three game-days -- crops die after
            # two unwatered days and animals escape after two unfed ones. So a seeded position
            # cannot be held by standing still, which is exactly what a weak scripted opponent
            # would have allowed.
            # **Bank at the moment the season ends, captured BEFORE the restart overwrites it.**
            #
            # `money_med` is `farm.money` sampled when the update happens to end, with every game at
            # a different point in its season -- so it measures typical cash ON HAND, not an
            # outcome. It rose $922 -> $2,600 overnight while a replay of the same checkpoint ended
            # every game on $0, and both numbers were honest: the policy had learnt to go broke
            # later. The outcome question -- did it finish with more than the $3,000 it started
            # with -- needs the bank on terminal rows, and three lines later `pick` has already
            # replaced it with the seed state's.
            end_money = nxt.farm.money
            fresh = seed_states
            restart = just_done | truncate
            pick = lambda new, old: jnp.where(                       # noqa: E731
                restart.reshape((-1,) + (1,) * (old.ndim - 1)), new, old)
            nxt = nxt._replace(
                step_index=pick(fresh.step_index, nxt.step_index),
                tiles=jax.tree_util.tree_map(pick, fresh.tiles, nxt.tiles),
                farm=jax.tree_util.tree_map(pick, fresh.farm, nxt.farm),
                inventory=pick(fresh.inventory, nxt.inventory),
                # **`unlock_day` is per game and must be restored with the rest of the board.**
                # It was omitted while every entry point left it at the constant `NEVER`, where the
                # omission could not be observed. Now that a restarting slot's seed state carries a
                # real per-game shop order, keeping the finished game's schedule would pair one
                # game's board with another game's market -- and the town drain drives every price
                # the new episode trades at.
                unlock_day=pick(fresh.unlock_day, nxt.unlock_day),
            )

            # **A virgin ending is a truncation, not a termination**, and the distinction is load
            # bearing: `gae` zeroes the bootstrap on `done` and keeps it on `trunc`. Marking one
            # `done` with a suppressed reward would teach the critic that a state twenty turns into
            # a phase-seeded board is worth exactly zero -- replacing a wrong reward with a wrong
            # value target. Cutting only the advantage trace is the treatment truncation already
            # gets, for the same reason.
            #
            # It also drops these games from `n_terminal` and from every win rate, which is right:
            # they are not results and should not be counted as any opponent's.
            real_done = just_done & ~virgin
            pseudo_trunc = truncate | (just_done & virgin)
            done_flat = jnp.broadcast_to(real_done[:, None], (batch, 2)).reshape(-1)
            out = dict(
                logp=logp, value=value, reward=reward.reshape(-1),
                done=done_flat, actions=actions, masks=masks, obs=obs,
                end_money=end_money.reshape(-1),
                trunc=jnp.broadcast_to(pseudo_trunc[:, None], (batch, 2)).reshape(-1),
                # Rows the frozen opponent chose are not ours to learn from: their log-probs come
                # from different parameters, so including them would make the PPO ratio a ratio of
                # two unrelated policies.
                trainable=~take_opp,
                # Which rows belong to a game the frozen opponent is playing in. Not the same as
                # `~trainable`: that marks the opponent's own seat, while this marks *both* seats
                # of a cross-play game, so the live policy's side of one can be picked out.
                crossplay=jnp.broadcast_to(
                    (use_opp | use_idle | use_trade | use_farm | use_ranch
                     | use_carrot | use_home)[:, None],
                    (batch, 2)).reshape(-1),
                # Games against a *pool checkpoint* specifically. `crossplay` covers every scripted
                # seat too, which is right for the win-rate metric and wrong for deciding how hard
                # a given checkpoint is -- see where the priority EMA is updated.
                vs_pool=jnp.broadcast_to(use_opp[:, None], (batch, 2)).reshape(-1),
                # The same split, per scripted seat. One blended win rate cannot distinguish
                # "loses to everything" from "beats the floor and is shut out by the farmer", and
                # those two readings point at opposite fixes -- the first is exploration, the
                # second is opponent difficulty. The flags already exist to route the pool EMA;
                # carrying them through costs three broadcasts and makes the scoreboard readable.
                vs_idle=jnp.broadcast_to(use_idle[:, None], (batch, 2)).reshape(-1),
                vs_trade=jnp.broadcast_to(use_trade[:, None], (batch, 2)).reshape(-1),
                vs_farm=jnp.broadcast_to(use_farm[:, None], (batch, 2)).reshape(-1),
                vs_ranch=jnp.broadcast_to(use_ranch[:, None], (batch, 2)).reshape(-1),
                vs_carrot=jnp.broadcast_to(use_carrot[:, None], (batch, 2)).reshape(-1),
                vs_home=jnp.broadcast_to(use_home[:, None], (batch, 2)).reshape(-1),
                vs_tape=jnp.broadcast_to(use_tape[:, None], (batch, 2)).reshape(-1),
                roles=roles,
                # **Which unit-turns were the policy's own decision**, in network-flat layout.
                # False on the intermediate turns of a commitment: the unit was walking a path it
                # chose earlier, so scoring that turn would credit the policy for an action it did
                # not take. Stored rather than recomputed for the same reason the observations are
                # -- the update must mask exactly what the behaviour policy masked.
                decided=decided_flat,
            )

            # **Re-draw the role only for games that just ended.** A surviving game keeps the
            # opponent it has been playing all season, which is the entire point of this change.
            key, krole = jax.random.split(key)
            drawn = jax.random.categorical(krole, role_logp, shape=(batch,))
            nxt_roles = jnp.where(restart, drawn, roles)
            # Once a slot restarts it has been reset to turn 0 on an empty board, so from here its
            # episodes are genuine and their terminal rewards count.
            nxt_virgin = virgin & ~restart
            # Night respawns every unit, dismisses every hand and empties every inventory, so a walk
            # in progress is invalid whatever its timer says. A restarting slot is a fresh game and
            # must not inherit a commitment either.
            nxt_cmt = CM.clear_at_night(cmt_next, nxt)
            nxt_cmt = jax.tree_util.tree_map(
                lambda a, z: jnp.where(
                    restart.reshape((-1,) + (1,) * (a.ndim - 1)), z, a),
                nxt_cmt, CM.init(batch))
            return (nxt, nxt_roles, nxt_virgin, key, nxt_cmt), out

        (final_state, final_roles, final_virgin, key, _final_cmt), traj = jax.lax.scan(
            one_turn, (state, roles, virgin, key, CM.init(batch)), None, length=horizon)

        # Bootstrap from the value of the state we stopped in, across all phase groups.
        t, u, g = jax_obs.encode(final_state)
        _h, last_value = model.apply(value_params, A._flat(t), A._flat(u), A._flat(g))

        def gae(carry, x):
            adv, next_value = carry
            reward, value, done = x["reward"], x["value"], x["done"]
            # A finished episode has no successor, so the bootstrap is cut there.
            next_value = jnp.where(done, 0.0, next_value)
            # A *truncated* one does have a successor we simply stopped looking at, so its
            # bootstrap stands and only the advantage trace is cut. Zeroing the bootstrap here
            # instead would teach the policy that the world ends at the truncation point.
            adv = jnp.where(done | x["trunc"], 0.0, adv)
            delta = reward + gamma * next_value - value
            adv = delta + gamma * gae_lambda * adv
            return (adv, value), adv

        _carry, advantages = jax.lax.scan(
            gae, (jnp.zeros_like(last_value), last_value),
            {k: traj[k] for k in ("reward", "value", "done", "trunc")},
            reverse=True,
        )
        returns = advantages + traj["value"]
        return final_state, final_roles, final_virgin, key, traj, advantages, returns

    return rollout


def role_logits_per_slot(role_p, seed_days, n_slots):
    """Per-slot role distribution, with `idle` confined to day-0 slots.

    **`vs idle` is five different questions wearing one label.** Under symmetric seats the idle
    opponent holds its opening bank for the whole episode, and openings span **$623 at day 0 to
    $54,031 at day 25** -- an 87x spread. So at day 25 "beat idle" asks whether you can out-earn a
    five-figure position in five days, and at day 0 it asks whether you can make money at all from
    a real start. Only the second is the check the metric is read as, and the aggregate has sat at
    0.995 for the whole run precisely because the other rungs are near-saturated.

    Confining idle to day-0 slots makes the label constant over the thing it describes, which is
    the property `CLAUDE.md` demands of an aggregate. The freed budget is not deleted: the returned
    logits are unnormalised, so `jax.random.categorical` renormalises per slot and idle's share
    goes back to the *real* opponents on every non-day-0 slot, where the open problem actually is.

    A floor of `log(1e-12)` rather than `-inf` -- finite, matching how a zero `--trade-frac` is
    already expressed one line up, and leaving no `-inf` to turn into a NaN if the row is ever
    reduced over.
    """
    lp = jnp.log(jnp.asarray(role_p, dtype=jnp.float32) + 1e-12)
    out = jnp.broadcast_to(lp, (n_slots, len(role_p)))
    if seed_days is None:
        return out
    day0 = jnp.asarray(seed_days) == 0
    return out.at[:, ROLE_IDLE].set(
        jnp.where(day0, lp[ROLE_IDLE], jnp.log(jnp.asarray(1e-12, dtype=jnp.float32))))


def op_census(op_rows, live, n_ops=CM.N_POLICY_OPS):
    """Count chosen ops over `live` rows, one bin per op in the space `n_ops` describes.

    Extracted so the width is a named argument that a test can pin. Inline it was
    `jax.nn.one_hot(op_rows, O.N_OPS)`, and the silent truncation of every token >= `O.N_OPS` was
    invisible at the call site -- `one_hot` does not raise on an out-of-range index, it returns a
    zero row, so the count simply went missing with nothing to read as wrong.
    """
    return (jax.nn.one_hot(op_rows, n_ops, dtype=jnp.float32) * live[..., None]).sum(axis=(0, 1))


def _norm(counts):
    """Counts -> shares. All-zero stays all-zero rather than becoming NaN, because "this head was
    never exercised" is a reading worth seeing rather than a blank."""
    total = float(sum(counts))
    return [c / total for c in counts] if total > 0 else [0.0 for _ in counts]


# The heads that spend money. Shaped toward "do not transact" at init, for the reason argued in
# `hand_prior_heads` -- and deliberately *not* including `sell`, which brings money in, or `trade`,
# whose near-uniform spread is healthy and is the coordinating latent the product heads read.
SPEND_HEADS = ("buy_seed", "buy_animal", "buy_land", "hire")

# **Share of the non-noop op mass the COMMIT class takes, when at least one commit is legal.**
#
# A class-level split, and the distinction from a per-op marginal is the whole point: this says
# nothing about *which* commit or *which* primitive, so there is no strategy in it to inherit. The
# `CLAUDE.md` entry that forbids a per-op prior forbids "feed 8%, water 2%" -- a claim about what a
# good farmer does. This is a claim about action *granularity*, which is a property of the action
# space rather than of good play, and it rests on two measured structural facts:
#
#   - `MAX_COMMIT_TURNS = 4`. One commit draw stands in for up to four primitive move draws, and
#     those intermediate turns are excluded from the PPO density entirely. Flat-per-token weights
#     one COMMIT_WATER equal to one N despite roughly 4x the behavioural footprint per draw.
#   - Legality is asymmetric in the same direction. Movement is legal nearly every turn; a commit
#     is legal only when a valid target is in range. So flat-over-legal under-serves the commit
#     class twice over, on footprint and on frequency, and both push the same way.
#
# 0.40 against a raw flat share of 5/23 = 21.7%, i.e. about 2x, from "an average commit replaces
# ~2 primitive draws". The multiplier should eventually be set from the measured realised walk
# length under an active commit rather than asserted; 0.40 is the starting point, not a result.
#
# **Why this is not the "mostly walk" fragment in reverse.** Flat-over-legal is not neutral here:
# because movement is legal almost always and the specialist ops rarely are, a flat scheme spends
# most of its mass on movement on a typical turn -- nobody wrote "prefer walking", the legality
# shape wrote it. That is the same policy-fragment failure the known-bad entry describes, at the
# opposite frequency extreme. Reweighting *within* the primitives to fix it would be the forbidden
# per-op marginal relabelled, so the class boundary is the only place the correction belongs.
COMMIT_PRIOR_SHARE = 0.40


def hand_prior_heads(heads, masks, noop_p, spend_p=0.0):
    """A prior that is a *shape*, not a policy: `noop_p` on doing nothing, the rest spread evenly.

    **This is what Ender actually did, and the distinction matters.** He used no imitation learning
    at all -- 8th place from scratch, under $200, on this class of hardware -- and his prior was two
    numbers typed into a config: `halt_init_prob=0.9` and `fraction_init_ratio=1:1:1:1:10`. Not a
    cloned agent.

    Two consequences follow, and they are why this is worth trying before the cloned prior:

    - **It cannot cap the ceiling.** A prior containing no strategy offers no strategy to inherit,
      so it sidesteps the risk `CLAUDE.md` attaches to letting a heuristic become the policy. A
      behaviour-cloned prior does not: it encodes actual play, at the level of whatever it cloned.
    - **It cannot be adversarial the way a collapsed clone can.** `KL(policy || prior)` taxes the
      policy for putting mass where the prior has none, and the current BC checkpoint assigns 6e-5
      to moving at the spawn state -- so as a prior it would punish PPO for the one behaviour it
      needs to discover. A flat `noop_p` cannot do that by construction.

    Only `op` is shaped, and **not** because the market heads are healthy -- they are not. Decoding
    them as independent marginals under-fires catastrophically (argmax emits zero orders, because
    nine separate "probably not sell" decisions compose into "never sell") and sampling them
    independently over-fires (banking $1 on noise). But that is a *correlation* failure: the
    marginals themselves discriminate 12:1, and the joint has structure the factorisation cannot
    represent. A flat prior over each market head would not fix a missing correlation and might
    blunt marginals that are already good, so the fix there is an autoregressive decode over order
    slots, not a shaped prior. Shaping `op` alone also keeps this to one delta.

    **`spend_p` revisits exactly that decision, because the problem it reasoned about has changed.**
    The paragraph above declined to shape the market heads on the grounds that their failure was
    *under*-firing from a broken joint decode. That decode landed, and the failure is now the
    opposite: measured on a trained checkpoint, `buy_seed` fires on 29.1% of turns and `hire` on
    24.8%, the bank reaches $0 within five game-days and stays there for twenty-five, and the policy
    consequently loses to an opponent that takes no action at all and finishes on its untouched
    $3,000. Every rung of the ladder then reads flat -- `farm` and `trade` 0.000, `pool` 0.500 --
    because a loss and a draw are both gradient-free once the critic predicts them.

    So the shape is "transacting is rare", applied only to the heads that *spend*: `buy_seed`,
    `buy_animal`, `buy_land`, `hire`. Not `sell`, which brings money in, and not `trade`, whose
    near-uniform spread is healthy and which the product heads condition on.

    **Why this is a shape and not a policy, which is the whole question.** It says purchases are rare
    at initialisation. It says nothing about *which* purchase, or *when*: no day-10 land rule, no crop
    preference, no herd size -- all of which are readable off the replays and all of which would be
    strategy the policy inherits rather than discovers. Ender's own prior was of exactly this form,
    one number meaning "mostly halt". And unlike a legality mask it is annealable: `--kl-anneal`
    decays the coefficient, so the constraint is a starting condition rather than a ceiling. Set
    `--spend-prior 0` to disable it entirely.

    **The check that this has not capped anything**, and it must actually be run: the trained policy's
    spend rates should end up *above* `spend_p`, not pinned at it. A rate that sits exactly on the
    prior means the KL term is doing the deciding and the anneal is too slow.
    """
    out = {}
    for k, logits in heads.items():
        if k in SPEND_HEADS and spend_p > 0.0:
            # Bucket 0 is "no purchase" for every one of these heads -- quantity zero for the buy
            # ladders, False for the two binary ones -- so this is the same construction as `op`'s
            # noop, with the same meaning.
            n_legal = jnp.maximum(masks[k].sum(axis=-1, keepdims=True), 1)
            others = jnp.log(spend_p / jnp.maximum(n_legal - 1, 1))
            is_none = jnp.arange(logits.shape[-1]) == 0
            out[k] = jnp.where(is_none, jnp.log(1.0 - spend_p), others)
            continue
        if k != "op" or noop_p <= 0.0:
            # Uniform over legal options: KL against a uniform prior is just negative entropy, so
            # these heads keep exactly the behaviour the entropy bonus used to give them.
            #
            # **`noop_p <= 0.0` is load-bearing and its absence NaN'd a run.** The caller's guard was
            # widened from `if hand_noop_p:` to `if (hand_noop_p or spend_p):` so that
            # `--spend-prior` could work on its own -- which let `noop_p = 0.0` reach the `op` branch
            # below, where `jnp.log(noop_p)` is `-inf`. The KL then went NaN and took the whole run
            # with it: ret nan, V nan, ent 0.0, every spend rate 0.000 and the bank frozen at
            # exactly $3,000, inside ten updates.
            #
            # It survived its smoke test because that run passed `--hand-prior 0.3` and the deploy
            # did not, so the two differed in precisely the argument that mattered. Two updates was
            # also too short: the failure needed ~50. A prior touching five heads deserved a longer
            # test than a decode change.
            out[k] = jnp.zeros_like(logits)
            continue
        m = masks[k]
        # noop takes `noop_p`; the remainder is split between the two op CLASSES and then flat
        # within each. See `COMMIT_PRIOR_SHARE` for why the class boundary is the only structural
        # correction available without becoming a per-op marginal. Written in log space directly
        # rather than as logits to normalise.
        idx = jnp.arange(logits.shape[-1])
        is_noop = idx == O.NOOP
        is_commit = idx >= O.N_OPS
        n_commit = (m & is_commit).sum(axis=-1, keepdims=True)
        n_prim = (m & ~is_commit & ~is_noop).sum(axis=-1, keepdims=True)
        rest = 1.0 - noop_p
        # With no commit legal this turn the class does not exist and primitives take the lot --
        # the split must never invent mass for an option the board cannot offer.
        commit_mass = jnp.where(n_commit > 0, COMMIT_PRIOR_SHARE * rest, 0.0)
        prim_mass = rest - commit_mass
        # Floored before the log. `jnp.log(0.0)` is `-inf`, and an `-inf` sitting in a masked-out
        # slot has already taken a run to NaN in this file once -- see the `noop_p <= 0.0` note
        # above. The floor is far below any reachable probability, so it changes nothing legal.
        commit_each = jnp.log(jnp.maximum(commit_mass, 1e-30) / jnp.maximum(n_commit, 1))
        prim_each = jnp.log(jnp.maximum(prim_mass, 1e-30) / jnp.maximum(n_prim, 1))
        out[k] = jnp.where(is_noop, jnp.log(noop_p),
                           jnp.where(is_commit, commit_each, prim_each))
    return out


# Heads the *hand* prior keeps when a BC prior is also supplied. Everything else takes the BC
# prior. Extracted from `loss_fn` so the choice is testable: as an inline dict comprehension it was
# invisible, and its consequence -- that `--spend-prior` was accepted and then silently discarded
# whenever `--kl-prior` was set -- could not be asserted anywhere.
#
# **`SPEND_HEADS` was added here on 2026-08-02, and the reason is that the problem inverted.**
#
# `--spend-prior` was built to cap a *hyperactive* policy: `buy_seed` firing on 29.1% of turns, the
# bank at $0 by game-day five. It was then correctly recorded as known-bad "as a bankruptcy fix on
# an inert policy". The policy is now the opposite failure -- measured on `league1`, every spend
# rate sits *on* the BC prior rather than above it:
#
#     head          BC prior implies    measured
#     buy_land           0.0%            0.000
#     buy_animal         0.1%            0.0002
#     buy_seed           0.9%            0.012
#     hire               6.3%            0.073
#
# which is exactly the reading `CLAUDE.md` names as the test that a prior has capped the ceiling.
# Against an inert policy a 5% shape prior is a FLOOR, not a cap: it pulls from below, which is the
# direction now wanted. Same flag, same value, opposite effect, because the policy moved -- which
# is the "a decision to skip a fix can expire when the problem changes" entry, a third time.
#
# `hire` is included deliberately rather than left on the BC prior. It is the worst-affected head
# -- ~0.42 is needed for a crew of ten against a measured 0.073 -- so protecting it from the shape
# prior would protect the head that most needs releasing. A 5% pull from below still beats a 6.3%
# pin, and if 5% later proves too tight for `hire` specifically that is a value question, not a
# reason to leave it glued to a day-2 checkpoint.
HAND_PRIOR_HEADS_WITH_BC = ("op",) + SPEND_HEADS


def merge_priors(hand_prior, bc_prior, hand_heads=HAND_PRIOR_HEADS_WITH_BC):
    """Pick, per head, which of the two priors governs it.

    Neither prior is right everywhere. The BC prior has the market heads roughly right and the `op`
    head wrong -- it predates commitments, so its zero-padded commit logits hold 2.4% of op mass
    against 21.7% uniform, a 9x suppression of the behaviour under test. The hand prior is the
    reverse: correct about `op`, and *uniform* on every head it does not shape, which pushes those
    heads toward buying on 40-75% of turns.

    **The trap this makes visible.** `--spend-prior` shapes `buy_seed`, `buy_animal`, `buy_land` and
    `hire`, and every one of them is outside `hand_heads`, so supplying `--kl-prior` discards all
    four without a word. A run can pass `--spend-prior 0.05`, log it in its own args line, and have
    it govern nothing.
    """
    return {k: (hand_prior[k] if k in hand_heads else bc_prior[k]) for k in hand_prior}


def kl_to_prior(heads, prior_heads, masks):
    """Mean KL(current || prior) over every head, respecting legality masks.

    **Ender's fix, and it replaces the entropy bonus rather than joining it.** An entropy bonus
    pushes toward *uniform*, which is never the target: you do not want "do nothing" and every
    farming op to be equally likely. His write-up is blunt about it -- a higher halt-bias
    initialisation "quickly regressed" until he swapped the entropy term for a KL penalty against a
    sensible prior, which "resulted in a huge immediate improvement".

    Our failure is the mirror image of his. He had runaway action and biased the prior toward
    halting; we have a policy that reaches 95% NOOP within four updates and never once improves on
    its initialisation. Same instrument, opposite direction -- which also explains why raising
    `ent_coef` 6.7x did nothing measurable: uniform was the wrong target either way.

    The prior is either a behaviour-cloned network or a hand-specified shape -- see
    `hand_prior_heads`. Either way it is a *soft* penalty rather than a mask, so it stays clear of
    the quality-masking anti-pattern `CLAUDE.md` records as an Orbit Wars failure: nothing is
    forbidden, some things are merely made expensive to abandon.
    """
    total = 0.0
    for k, logits in heads.items():
        m = masks[k]
        cur = jax.nn.log_softmax(jnp.where(m, logits, NEG_INF), axis=-1)
        pri = jax.nn.log_softmax(jnp.where(m, prior_heads[k], NEG_INF), axis=-1)
        p = jnp.exp(cur)
        # Illegal entries contribute nothing: their probability is zero under both distributions.
        kl = jnp.where(m, p * (cur - pri), 0.0).sum(axis=-1)
        total = total + kl.mean()
    return total


def kl_fraction(kl_anneal, it):
    """How much of the regulariser is still the KL at update `it`. 1.0 -> all KL, 0.0 -> all entropy.

    Clamped at zero on both ends. A negative fraction would flip the KL's sign and actively push
    the policy *away* from the prior, which is the opposite of releasing it.
    """
    if not kl_anneal:
        return 1.0
    return max(0.0, 1.0 - it / float(kl_anneal))


def terminal_loss_shares(sq_err, trainable, done, near_turns=NEAR_TERMINAL_TURNS):
    """How much of the value loss the terminal and near-terminal rows carry. Diagnostic only.

    Item 1 of `docs/critic_terminal_blindness_2026-08-03.md`, which asks for a measurement before any
    third mechanism is added to the value loss. The premise stated throughout this file is that
    terminal rows are ~0.14% of the batch (one turn in 719) and the critic therefore trains almost
    entirely on its own bootstrap. But **count share and loss share are different numbers**, and only
    the second one says whether upweighting those rows would change the gradient: a terminal row's
    target is the true outcome rather than a bootstrap, so its squared error is typically far larger.
    If 0.14% of rows already carry 2% of the loss they have 14x leverage and upweighting is a much
    smaller intervention than the row count suggests. `term_leverage` near 1.0 is the case that makes
    upweighting worth doing.

    Nothing here enters `loss_fn`, so a run with this instrumentation trains bit-identically to one
    without it.

    All three arrays are `[horizon, rows]`, not flattened, because `near` has to shift along the
    horizon axis. Rows whose terminal falls outside the window simply do not count as near, which is
    honest -- we cannot see it. `jnp.roll` is deliberately avoided: it wraps, which would make the top
    of the window adjacent to the bottom.
    """
    tr = trainable.astype(jnp.float32)
    ended = done & trainable
    term = ended.astype(jnp.float32)
    total = jnp.maximum((sq_err * tr).sum(), 1e-8)
    n_rows = jnp.maximum(tr.sum(), 1.0)

    loss_share = (sq_err * term).sum() / total
    row_share = term.sum() / n_rows

    near = ended
    for s in range(1, near_turns):
        near = near | jnp.concatenate(
            [ended[s:], jnp.zeros((s,) + ended.shape[1:], dtype=bool)], axis=0)
    near_f = near.astype(jnp.float32) * tr

    return dict(
        term_loss_share=loss_share,
        term_row_share=row_share,
        term_leverage=loss_share / jnp.maximum(row_share, 1e-8),
        near_loss_share=(sq_err * near_f).sum() / total,
        near_row_share=near_f.sum() / n_rows,
    )


def blend_regulariser(reg_coef, kl_frac, kl_prior, entropy_loss, kl_active):
    """The single regulariser term, handing over from KL to entropy as the prior anneals out.

    **Why a handover and not a sum.** The long comment in `loss_fn` is right that under Ender's
    structure the KL *replaces* entropy rather than adding to it, and that a separate `--kl-coef`
    alongside `--ent-coef 0` cost two runs by leaving effectively no regulariser at all. Summing
    the two would also double-count: `hand_prior_heads` returns a uniform prior for every head it
    does not shape, and `KL(p || uniform) = -H(p) + const`, so on those heads the KL already *is*
    an entropy bonus. So the two share one coefficient and trade weight on a convex blend.

    **What this fixes.** `--kl-anneal` used to decay `reg_coef` itself, and `reg_coef` is the whole
    regulariser when a prior is set -- so annealing the prior away annealed *everything* away and
    the run finished with nothing holding the policy. Measured on `ppo-20260802-085329`: entropy
    13.35 -> 26.70 while the win rate fell 0.525 -> 0.291 over 66 updates, with `ev_signal` still
    rising. The critic was fine; the anchor had come off.

    At `kl_frac = 1.0` this is exactly the old expression, so a run without `--kl-anneal` is
    unchanged to the last bit. Pinned by `tests/test_kl_anneal.py`.
    """
    if not kl_active:
        return reg_coef * entropy_loss
    return reg_coef * (kl_frac * kl_prior + (1.0 - kl_frac) * entropy_loss)


def make_update(model, clip, vf_coef, ent_coef, max_grad_norm, optimiser, seat_coef=0.0,
                kl_coef=0.0, prior_params=None, hand_noop_p=0.0, spend_p=0.0):
    """Build the jitted PPO update over one rollout's minibatches."""

    def loss_fn(params, batch_data, reg_coef, kl_frac):
        tiles, units, glob = batch_data["obs"]
        heads, value = model.apply(params, tiles, units, glob)
        logp, entropy = A.evaluate(heads, batch_data["masks"], batch_data["actions"],
                                   batch_data.get("decided"))

        # Rows chosen by a frozen opponent carry log-probs from other parameters; including them
        # would make the ratio a comparison of two unrelated policies. Weight them out rather than
        # index them out, so every minibatch keeps a static shape and the graph stays jittable.
        w = batch_data["trainable"].astype(jnp.float32)
        w_sum = jnp.maximum(w.sum(), 1.0)

        ratio = jnp.exp(logp - batch_data["old_logp"])
        adv = batch_data["adv"]
        # Normalising per minibatch is standard and matters here: terminal-only rewards make raw
        # advantages tiny for most of an episode and large at the end. Statistics are taken over
        # the trainable rows only, or the opponent's rows would shift the mean.
        adv_mean = (adv * w).sum() / w_sum
        adv_var = ((adv - adv_mean) ** 2 * w).sum() / w_sum
        adv = (adv - adv_mean) / (jnp.sqrt(adv_var) + 1e-8)

        unclipped = ratio * adv
        clipped = jnp.clip(ratio, 1 - clip, 1 + clip) * adv
        policy_loss = -(jnp.minimum(unclipped, clipped) * w).sum() / w_sum

        # Value clipping, the same trust region the policy gets. The critic here regresses onto
        # targets that are mostly built from its own past predictions, so an unconstrained value
        # step can move a long way on one minibatch and take the next round of bootstrap targets
        # with it -- the feedback loop that let the value drift to 1.315 before phases were
        # staggered. Taking the max of the clipped and unclipped errors is pessimistic on purpose.
        old_value = batch_data["old_value"]
        v_clipped = old_value + jnp.clip(value - old_value, -clip, clip)
        value_loss = (jnp.maximum(
            jnp.square(value - batch_data["returns"]),
            jnp.square(v_clipped - batch_data["returns"]),
        ) * w).sum() / w_sum
        entropy_loss = -(entropy * w).sum() / w_sum

        # **Op-head entropy on its own. A metric only -- it is not in the objective.**
        #
        # The logged `entropy` is a sum over every head, and a sum cannot separate the two ways the
        # commit-class prior split can fail: the class share rising because commits are being used
        # (intended) and the op head collapsing onto one commit token it now spams (a new policy
        # fragment) can move the total the same way. Without this isolated number, "working" and
        # "revert" are the same reading.
        _op_mask = batch_data["masks"]["op"]
        _op_logp = jax.nn.log_softmax(jnp.where(_op_mask, heads["op"], -jnp.inf), axis=-1)
        # `p * logp` is `0 * -inf = nan` on a masked slot, so the masked terms are zeroed rather
        # than relied on to vanish -- the same NaN shape this file has already been bitten by.
        _op_ent = -jnp.where(_op_mask, jnp.exp(_op_logp) * _op_logp, 0.0).sum(axis=-1)
        op_entropy = (_op_ent.reshape(w.shape[0], -1).mean(axis=-1) * w).sum() / w_sum

        # **Seat-sum consistency: V(seat 0) + V(seat 1) = 1.**
        #
        # The two seats of a game are the same board seen from opposite sides, so their win
        # probabilities add to one -- win 1 + loss 0, or tie 0.5 twice. This is arithmetic, not a
        # property of a good critic: it holds for any policy at any skill level, and it holds on
        # **100% of rows**, against the ~0.14% that carry a terminal reward (one turn in 719).
        #
        # That distinction is why this is not reward shaping. It invents no reward and expresses no
        # opinion about which actions are good; it only forbids the critic from claiming both sides
        # of the same game are winning. Measured before adding it, the sum was 1.17 and climbing to
        # 1.28 while mean(V) was 0.64 -- i.e. `sum` was almost exactly `2 x V`, meaning the critic
        # was seat-blind, emitting one global number that drifted upward rather than predicting
        # anything about the position.
        #
        # Rows arrive as [B*P] with the seat axis innermost, so a reshape recovers the pairs.
        pairs = value.reshape(-1, 2)
        seat_loss = jnp.square(pairs.sum(axis=-1) - 1.0).mean()

        # KL to the behaviour-cloned prior. Computed only when a prior is supplied, so a run without
        # one costs nothing and behaves exactly as before.
        # **The KL is taken over the *conditioned* heads, not the raw ones.**
        #
        # `sell` and `buy_product` carry a trade-mode axis, and `crop`/`item`/`qty` an op axis, that
        # the masks do not: the raw heads are `[N, N_PRODUCTS, N_TRADE_MODES, K]` and
        # `[N, MAX_UNITS, N_OPS, K]` against `[N, N_PRODUCTS, K]` and `[N, MAX_UNITS, K]` masks, and
        # the broadcast simply fails. More importantly, the distribution the policy actually acted
        # from is the slice its sampled conditioning variable selected -- a KL against a marginal
        # over modes or ops would regularise something the policy never sampled from.
        #
        # `A.condition_all` applies both steps, so this cannot drift out of step with `A.evaluate`
        # above by remembering one and forgetting the other.
        if kl_coef:
            cond = A.condition_all(heads, batch_data["actions"])
        if kl_coef and (hand_noop_p or spend_p):
            prior = hand_prior_heads(cond, batch_data["masks"], hand_noop_p, spend_p)
            # **Both priors at once, each on the head it is right for.** Measured on a day-25
            # board, P(act) implied by each:
            #
            #                  BC prior   uniform (what the hand prior gives an unshaped head)
            #     buy_seed         0.9%     75.0%
            #     buy_product      0.4%     40.0%
            #     buy_animal       0.1%     50.0%
            #     hire             6.3%     50.0%
            #     buy_land         0.0%     46.7%
            #     sell             6.6%     27.3%
            #
            # `hand_prior_heads` returns *uniform* for every head it does not shape, and
            # `KL(p||uniform)` is negative entropy -- so those heads are pushed toward buying on
            # 40-75% of turns. That is what emptied a $53,373 inherited farm down to $14 and lost
            # to an opponent that does nothing. `--spend-prior` covers only four of the six; nothing
            # covers `buy_product` or `sell`.
            #
            # The BC prior has the market right and the `op` head wrong: it predates commitments, so
            # its zero-padded commit logits carry 2.4% of the mass against 21.7% uniform -- a 9x
            # suppression of the one behaviour under test. Neither prior is correct everywhere, and
            # there is no reason to use one where the other is better.
            if prior_params is not None:
                bc_heads, _pv = model.apply(prior_params, tiles, units, glob)
                bc_cond = A.condition_all(
                    jax.lax.stop_gradient(bc_heads), batch_data["actions"])
                prior = merge_priors(prior, bc_cond)
            kl_prior = kl_to_prior(cond, prior, batch_data["masks"])
        elif prior_params is not None and kl_coef:
            prior_heads, _pv = model.apply(prior_params, tiles, units, glob)
            prior_cond = A.condition_all(
                jax.lax.stop_gradient(prior_heads), batch_data["actions"])
            kl_prior = kl_to_prior(cond, prior_cond, batch_data["masks"])
        else:
            kl_prior = jnp.asarray(0.0, dtype=jnp.float32)

        # **The KL substitutes for entropy on the head that has a prior, and shares its
        # coefficient. It is not a separate term with a separate dial.**
        #
        # Read off Ender's actual source rather than his write-up, which does not make this clear:
        #
        #     halt_reg = new_halt_entropy
        #     if has_halt_prior:
        #         halt_reg = -halt_prior_kl                     # KL *replaces* entropy, this head
        #     total_regularizer = halt_reg + ... + target_used * new_target_entropy
        #     loss_ent = -entropy_coef * entropy                # one coefficient for all of it
        #
        # Heads without a prior keep plain entropy. There is no `kl_coef` anywhere in his code.
        #
        # Getting this wrong is why two runs here learned nothing: a separate `--kl-coef 0.01`
        # alongside `--ent-coef 0` -- which this script's own help text recommended -- left the
        # objective with a KL contribution of 0.00025 and no entropy at all, so effectively no
        # regulariser. Under his structure, zeroing the entropy coefficient zeroes the KL too.
        # The KL term *is* the whole regulariser when a prior is set, and adding entropy alongside
        # would double-count it: `hand_prior_heads` returns a uniform prior for every head it does
        # not shape, and `KL(p || uniform) = -H(p) + const`, so minimising that KL already maximises
        # entropy on exactly the heads Ender leaves on plain entropy. Only `op` differs, and there
        # the KL pulls toward `noop_p` instead of toward uniform -- which is the point.
        #
        # **The anneal now hands over instead of switching off.** `--kl-anneal` used to decay
        # `reg_coef`, which is the entire regulariser on this branch, so releasing the prior
        # released everything. `blend_regulariser` trades the weight across to entropy instead, so
        # the objective always has something in it. `kl_frac == 1.0` reproduces the old expression
        # exactly, which is what a run without `--kl-anneal` gets.
        kl_active = bool(kl_coef) and (hand_noop_p or spend_p or prior_params is not None)
        regulariser = blend_regulariser(reg_coef, kl_frac, kl_prior, entropy_loss, kl_active)

        loss = policy_loss + vf_coef * value_loss + regulariser + seat_coef * seat_loss
        approx_kl = ((batch_data["old_logp"] - logp) * w).sum() / w_sum
        clip_frac = ((jnp.abs(ratio - 1.0) > clip).astype(jnp.float32) * w).sum() / w_sum
        return loss, dict(policy_loss=policy_loss, value_loss=value_loss, seat_loss=seat_loss,
                          entropy=entropy.mean(), op_entropy=op_entropy,
                          approx_kl=approx_kl, clip_frac=clip_frac,
                          kl_prior=kl_prior)

    @jax.jit
    def update(params, opt_state, batch_data, reg_coef, kl_frac):
        (loss, aux), grads = jax.value_and_grad(loss_fn, has_aux=True)(
            params, batch_data, reg_coef, kl_frac)
        grads, gnorm = _clip_by_norm(grads, max_grad_norm)
        updates, opt_state = optimiser.update(grads, opt_state, params)
        params = optax.apply_updates(params, updates)
        return params, opt_state, {**aux, "loss": loss, "grad_norm": gnorm}

    @functools.partial(jax.jit, static_argnames=("epochs", "n_chunks", "chunk"))
    def run_epochs(params, opt_state, data, key, epochs, n_chunks, chunk, reg_coef, kl_frac):
        """Every minibatch of every epoch as a single dispatch.

        The obvious loop -- shuffle in numpy, slice per minibatch, call a jitted update -- costs one
        host-to-device transfer of the index array *per minibatch*. At 128 chunks and 2 epochs that
        is 256 round trips per update, each one a separate dispatch with its own launch latency,
        for an update whose actual arithmetic is a few hundred milliseconds. Permuting on device and
        scanning over the chunks collapses all of it into one call.
        """
        def one_epoch(carry, ekey):
            params, opt_state = carry
            # Permute **seat pairs**, not rows. Rows arrive as [B*P] with the seat axis innermost,
            # so rows 2k and 2k+1 are the two seats of one game at one turn. Shuffling rows
            # independently scatters those partners into different minibatches, and the
            # V(seat0)+V(seat1)=1 term then pairs unrelated rows and optimises nothing -- measured:
            # the seat sum climbed 1.17 -> 1.34 with the loss active, exactly as without it.
            # Permuting pairs keeps each partner adjacent, and every minibatch stays a whole
            # number of games.
            n_pairs = (n_chunks * chunk) // 2
            pair_perm = jax.random.permutation(ekey, n_pairs)
            perm = jnp.stack([2 * pair_perm, 2 * pair_perm + 1], axis=-1).reshape(-1)
            perm = perm.reshape(n_chunks, chunk)

            def one_minibatch(carry, rows):
                params, opt_state = carry
                mb = jax.tree_util.tree_map(lambda x: x[rows], data)
                params, opt_state, metrics = update(params, opt_state, mb, reg_coef, kl_frac)
                return (params, opt_state), metrics

            (params, opt_state), metrics = lax.scan(one_minibatch, (params, opt_state), perm)
            return (params, opt_state), metrics

        keys = jax.random.split(key, epochs)
        (params, opt_state), metrics = lax.scan(one_epoch, (params, opt_state), keys)
        # Report the last minibatch of the last epoch, matching what the Python loop reported.
        return params, opt_state, jax.tree_util.tree_map(lambda m: m[-1, -1], metrics)

    return update, run_epochs


def _clip_by_norm(grads, max_norm):
    norm = optax.global_norm(grads)
    scale = jnp.minimum(1.0, max_norm / (norm + 1e-8))
    return jax.tree_util.tree_map(lambda g: g * scale, grads), norm


def save_checkpoint(path, params, opt_state, update, args, best=None):
    """Write params + optimiser state atomically.

    Atomically because a checkpoint half-written when the process is killed is worse than no
    checkpoint: it looks resumable and is not. Write to a temp file, then rename -- rename is
    atomic on the same filesystem, so a reader either sees the old file or the new one.

    A previous run in this project saved *nothing* over 448k steps because the save trigger was
    misconfigured and nobody checked until it was over. So `--ckpt-every` is in updates (a unit
    that appears in the log every line), not steps, and the first save happens immediately.
    """
    path = pathlib.Path(path)
    tmp = path.with_suffix(".tmp")
    payload = {
        "params": jax.device_get(params),
        "opt_state": jax.device_get(opt_state),
        "update": update,
        "args": vars(args),
        "best": best,
    }
    with tmp.open("wb") as fh:
        pickle.dump(payload, fh, protocol=pickle.HIGHEST_PROTOCOL)
    tmp.replace(path)


def load_checkpoint(path):
    with pathlib.Path(path).open("rb") as fh:
        return pickle.load(fh)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=512, help="games in flight; each gives 2 seats")
    ap.add_argument("--horizon", type=int, default=128, help="turns per rollout")
    ap.add_argument("--updates", type=int, default=2000)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--minibatch-size", type=int, default=256,
                    help="ROWS per gradient step, not a count of minibatches. This must be a size: "
                         "a count makes the chunk scale with batch*horizon, and transformer "
                         "activation memory is linear in rows -- 2048 rows is ~8 GiB and 32768 "
                         "rows (batch 512, horizon 128, 4 minibatches) would be ~128 GiB. That is "
                         "how the first GPU run OOMed. 256 rows is ~1 GiB and leaves room for the "
                         "rollout buffers alongside.")
    ap.add_argument("--shaping-coef", type=float, default=0.0,
                    help="weight on potential-based NET WORTH shaping (`kagg/rl/net_worth.py`). "
                         "0.0 is byte-exactly off. This is NOT the per-step bank delta CLAUDE.md "
                         "retired: `F = gamma*PHI(s') - PHI(s)` telescopes to PHI(end)-PHI(start) at "
                         "gamma 1.0, so the optimal policy is provably unchanged (Ng, Harada & "
                         "Russell 1999) and only the TIMING of credit moves. Net worth rather than "
                         "cash because a cash potential punishes the animal chain at the moment of "
                         "investment. Set --value-margin alongside it or the critic clips.")
    ap.add_argument("--value-margin", type=float, default=0.0,
                    help="how far outside [0, 1] the value head may reach. The head is a sigmoid on "
                         "purpose -- an unbounded critic was measured at 1.315 while ev read +0.98 -- "
                         "but with shaping a return is terminal + coef*(PHI(end)-PHI(s)), which "
                         "exceeds those bounds. Widens the guard rather than removing it. Rule of "
                         "thumb: --shaping-coef times PHI's working range (~0.25 for a $28k season).")
    ap.add_argument("--gamma-per-day", type=float, default=0.97,
                    help="discount per GAME DAY; converted to per-turn internally")
    ap.add_argument("--gae-lambda", type=float, default=0.95)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--clip", type=float, default=0.2)
    ap.add_argument("--vf-coef", type=float, default=0.5)
    ap.add_argument("--ent-coef", type=float, default=0.02,
                    help="Raised from 0.003 once inactive heads stopped being scored: that took "
                         "entropy from ~100 nats to ~10, so the same coefficient was an ~30x "
                         "weaker bonus than intended and entropy collapsed 9.7 -> 2.1 in ten "
                         "updates. The Orbit Wars warning against 0.02 was about a *large* "
                         "MultiDiscrete space measured on the old scale.")
    ap.add_argument("--max-grad-norm", type=float, default=0.5)
    ap.add_argument("--d-model", type=int, default=128)
    ap.add_argument("--layers", type=int, default=3)
    ap.add_argument("--heads", type=int, default=4)
    ap.add_argument("--seat-coef", type=float, default=1.0,
                    help="weight on the V(seat0)+V(seat1)=1 consistency loss. Not reward shaping: "
                         "it is an identity that holds for any policy, and it anchors the critic "
                         "on 100%% of rows instead of the 0.14%% carrying a terminal reward. "
                         "0 disables.")
    ap.add_argument("--opponent-frac", type=float, default=0.25,
                    help="fraction of phase groups whose seat 1 is played by a frozen past self. "
                         "Pure self-play shares parameters between both seats, so a mutual draw is "
                         "a stable outcome nothing pushes against; a frozen opponent does not "
                         "co-operate in standing still. 0 disables.")
    ap.add_argument("--kl-prior", type=str, default=None,
                    help="path to a behaviour-cloned checkpoint to use as the KL prior. Ender's "
                         "fix: an entropy bonus pushes toward uniform, which is the wrong target "
                         "in either direction -- he had runaway action and biased toward halting, "
                         "we reach 95%% NOOP and want the opposite. Regularising toward a sensible "
                         "prior is the general form, and a cloned $100k agent is a better prior "
                         "than any guess. "
                         "**DO NOT set --ent-coef 0 with this.** The KL REPLACES the entropy term "
                         "but SHARES its coefficient (`reg_coef = args.ent_coef`, and "
                         "`regulariser = reg_coef * kl_prior`), matching Ender's structure -- so "
                         "zeroing --ent-coef zeroes the KL too and the run trains with no "
                         "regulariser at all. This exact instruction was already in this help text "
                         "once, cost two runs, was fixed for --kl-coef, and survived here.\n"
                         "Measured motivation: on `ppo-20260802-085329` entropy climbed 13.35 -> "
                         "26.70 while the win rate fell 0.525 -> 0.291 over 66 updates, with "
                         "clip_frac flat at 0.23-0.31 and ev_signal RISING to +0.293. The critic "
                         "was learning; the entropy bonus was eating the policy.")
    ap.add_argument("--hand-prior", type=float, default=0.0,
                    help="P(noop) for a hand-specified KL prior, e.g. 0.3. This is what Ender "
                         "actually used -- he ran no imitation learning at all and his prior was "
                         "two numbers in a config. A prior containing no strategy cannot cap the "
                         "ceiling and cannot punish exploration the way a collapsed clone can. "
                         "Takes precedence over --kl-prior when both are given. 0 disables.")
    ap.add_argument("--spend-prior", type=float, default=0.0,
                    help="P(transact) for the four money-spending heads (buy_seed, buy_animal, "
                         "buy_land, hire), e.g. 0.05. Measured motivation: a trained checkpoint "
                         "fires buy_seed on 29.1%% of turns and hire on 24.8%%, reaches $0 by game-day "
                         "five and stays there, and therefore loses to an opponent that acts not at "
                         "all and keeps its $3,000 -- which flattens every rung of the ladder. "
                         "This is a *shape* ('transacting is rare'), not a policy: it says nothing "
                         "about which purchase or when, so there is no strategy to inherit. Anneal "
                         "it with --kl-anneal; unlike a mask it is a starting condition, not a "
                         "ceiling. Verify it has not capped anything by checking the trained spend "
                         "rates end up ABOVE this value rather than pinned to it. 0 disables.")
    ap.add_argument("--kl-coef", type=float, default=1.0,
                    help="0 disables the KL entirely; any non-zero value switches the regulariser "
                         "from entropy to KL-against-the-prior. The *strength* comes from "
                         "--ent-coef, which they share, matching Ender's structure.")
    ap.add_argument("--kl-anneal", type=int, default=0,
                    help="updates over which the KL's SHARE of the regulariser decays linearly to "
                         "zero, handing the weight over to entropy at the same --ent-coef. 0 keeps "
                         "it flat, which is byte-identical to the behaviour before the handover "
                         "existed. "
                         "**It no longer decays the coefficient itself.** It used to, and that was "
                         "dangerous: on the prior branch the KL *is* the whole regulariser, so "
                         "annealing it annealed everything and the run finished with nothing "
                         "holding the policy. Measured on `ppo-20260802-085329` -- entropy 13.35 "
                         "-> 26.70 while the win rate fell 0.525 -> 0.291 over 66 updates, with "
                         "ev_signal still RISING. The critic was fine; the anchor had come off. "
                         "See `blend_regulariser` and `tests/test_kl_anneal.py`.")
    ap.add_argument("--early-limit", type=int, default=0,
                    help="if >0, even-numbered envs truncate at this many turns and restart, so "
                         "the opening is trained on constantly instead of once a season. Ender's "
                         "`--earlygame-env-turn-limit`. **Count in turns, not days: there are 24 "
                         "turns to a day.** Melon becomes harvestable at day 10 = turn 240 and its "
                         "window closes at day 12 = turn 288, so anything below ~264 truncates "
                         "before a melon can legally be picked and those rows are structurally "
                         "incapable of completing the chain -- which then reads as the policy "
                         "failing to learn it. 288 covers melon; 96 covers wheat, which yields at "
                         "day 2 = turn 48.")
    ap.add_argument("--farm-frac", type=float, default=0.25,
                    help="fraction of games whose seat 1 is the JAX-native farmer, which banks "
                         "$23,783 a season against the trader's $3,368 and the idle seat's $3,000. "
                         "It is the only opponent in the pool that can punish a bad farm: the other "
                         "two are beatable by a fixed amount, so they are a floor, while this one "
                         "has real play in it. 0 disables.")
    ap.add_argument("--homestead-frac", type=float, default=0.0,
                    help="fraction of games whose seat 1 is `jax_homestead`, the only opponent that "
                         "farms AND ranches at once. Measured head to head (bench_jax_agents.py): "
                         "it banks $24,957 against `jax_heuristic`'s $30,292 and loses to it 0/48, "
                         "so it is NOT the strongest seat available and is not here to be one. It "
                         "is here because every other opponent is a specialist -- `farm` has no "
                         "FEED, no CARE and `buy_animal=zeros`, `ranch` grows nothing and buys all "
                         "295 of its wheat orders -- so a trainee can climb the whole pool without "
                         "ever meeting a seat that contests the crop market AND punishes ignoring "
                         "livestock. The public meta runs 8 cows, 5 sheep, 5 strawberry plots and "
                         "12 hands (`docs/public_meta_2026-08-03.md`); nothing in this pool did.")
    ap.add_argument("--carrot-frac", type=float, default=0.0,
                    help="fraction of games whose seat 1 is `jax_carrot`, a port of the public "
                         "baseline `makimakiai/kaggriculture-carrot-fleet-simple-python-baseline`. "
                         "It banks $3,410 from $3,000 -- by far the weakest farmer available, and "
                         "that is why it is here. Outcome variance is p(1-p), so an opponent the "
                         "policy is NEAR teaches more per game than one permanently above it: the "
                         "farmer at $23,783 holds us near 0.09 and contributes almost no gradient, "
                         "while this sits just above an idle seat's $3,000 and just above what the "
                         "policy manages from a real start, so it should sit near 0.5 and cross as "
                         "the policy improves. It also differs in KIND rather than dial -- melon on "
                         "16 tiles over a long cycle against carpeting every tile with carrot on a "
                         "three-day one -- which is the tempo diversity CLAUDE.md records this pool "
                         "has never had. 0 disables.")
    ap.add_argument("--trade-frac", type=float, default=0.25,
                    help="fraction of games whose seat 1 only trades wheat: buys early, sells late, "
                         "every unit passing. It banks $3,989 from a $3,000 start using zero crew "
                         "actions, so unlike --idle-frac a do-nothing policy LOSES to it rather "
                         "than drawing. That removes the 0.5 payoff for inaction, which is the "
                         "actual fixed point -- our idle farm is a stable $3,000 forever, where "
                         "Ender's game punished standing still on its own. 0 disables.")
    ap.add_argument("--tape-frac", type=float, default=0.0,
                    help="fraction of games whose seat 1 REPLAYS a real recorded player, drawn from "
                         "the 31 downloaded seats in --tape-actions. Every other opponent in this "
                         "pool is a heuristic and the whole family caps out near $15,000, while the "
                         "ladder is decided at $130,000-$180,000 -- so 'beats the pool' has never "
                         "been a question about ladder-strength play. These are time-indexed: on a "
                         "board pushed far off the tape's own line the recorded action degrades "
                         "toward a no-op, which is fine for an opponent and is exactly why the same "
                         "tapes cannot serve as a teacher. 0 disables.")
    ap.add_argument("--tape-actions", default="data/il/opponent_tape_actions.npz",
                    help="head labels for the recorded seats, from "
                         "scripts/build_opponent_tape_actions.py")
    ap.add_argument("--ranch-frac", type=float, default=0.0,
                    help="fraction of games whose seat 1 is `jax_rancher`. It banks $12,078 "
                         "against the scripted farmer's $23,783, so it is the WEAKER opponent -- "
                         "and that is not why it is here. Every other seat in the rollout runs "
                         "FEED, CARE and COLLECT_FERT at exactly 0.00%%, so nothing the policy "
                         "ever faces is punished for ignoring the animal economy, which is the "
                         "half of the game that wins (FEED +0.452, CARE +0.441 over 312 real "
                         "seats). A trainee can climb the entire opponent pool without once "
                         "meeting a herd. `jax_rancher` has been JAX-native and jit-safe since "
                         "2026-08-01 and was wired only into bc_dagger until now.")
    ap.add_argument("--idle-frac", type=float, default=0.25,
                    help="fraction of games whose seat 1 passes every turn and banks its opening "
                         "$3,000. A frozen past self shares the policy's failures, so self-play "
                         "settled into mutual draws -- ret 0.4925 +/- 0.0030 over 15 updates, and "
                         "ev_signal n/a on 8 of 12 because every terminal reward was 0.5. The "
                         "policy ends a season on $7, so an opponent that merely does nothing "
                         "beats it and the draw breaks. 0 disables.")
    ap.add_argument("--pool-every", type=int, default=50,
                    help="updates between snapshots added to the opponent pool")
    ap.add_argument("--pool-size", type=int, default=5)
    ap.add_argument("--target-ema", type=float, default=0.0,
                    help="decay for a slow EMA copy of the params used for bootstrap value "
                         "targets. 0 disables. Phase staggering already anchors the critic with a "
                         "real reward every update; this is the second line of defence and is off "
                         "by default so the two are not changed together.")
    ap.add_argument("--n-phases", type=int, default=12,
                    help="independent sim states, started at evenly spread points in the season. "
                         "jax_sim keeps one scalar step_index per state, so all games in a state "
                         "terminate together and cannot drift apart; with 719-turn episodes and a "
                         "64-turn horizon that put every terminal reward in one burst per ~11 "
                         "updates. 12 groups gives roughly one termination per update instead. "
                         "Must divide --batch.")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tag", default="ppo")
    ap.add_argument("--ckpt-every", type=int, default=25,
                    help="updates between checkpoints. In UPDATES, not steps: a previous run in "
                         "this project saved nothing across 448k steps because the trigger was in "
                         "a unit nobody was watching.")
    ap.add_argument("--curriculum-day", type=int, default=0,
                    help="seed episodes from REAL recorded boards at this game-day instead of from "
                         "an empty farm at turn 0, walking the day down to 0 over "
                         "--curriculum-anneal updates. 0 disables. Motivation, measured: every "
                         "opponent currently returns a CONSTANT outcome (0.000 vs idle and the "
                         "farmer, 0.060 vs the trader, 89%% draws vs a frozen self, because two "
                         "bankrupt farms tie exactly), and a constant has no gradient at any model "
                         "size. A day-15 board carries ~18 animals and ~$9k, so outcomes vary at "
                         "once -- and it cannot be held by standing still: left alone, 22 crops and "
                         "19 animals go to zero within three game-days. The reward is unchanged.")
    ap.add_argument("--curriculum-anneal", type=int, default=0,
                    help="updates per one-day step of --curriculum-day toward 0. 0 holds the day "
                         "fixed. Clock-driven on purpose: advancing the schedule on win rate makes "
                         "the metric that judges the curriculum the metric that advances it.")
    ap.add_argument("--curriculum-mix", type=str, default=None,
                    help="seed from SEVERAL game-days at once, as 'day:frac,day:frac' summing to 1 "
                         "-- e.g. '25:0.8,0:0.2'. Mutually exclusive with --curriculum-day and with "
                         "--curriculum-anneal. Why this rather than annealing the day: pure backward "
                         "annealing reaches day 0 LAST, with the least exposure, on weights "
                         "specialised for maintenance, and when the schedule steps off day 25 that "
                         "distribution is gone from the data -- re-anchoring a KL prior preserves "
                         "the behaviour partially, nothing preserves the data. A mix removes both by "
                         "construction. What a small day-0 share buys, stated so it is not "
                         "over-claimed: episodes are ~120 turns at day 25 and 719 at day 0 and every "
                         "slot emits --horizon turns per update, so a 20%% SLOT share is about a 4%% "
                         "share of terminal EPISODES, each carrying its reward over ~22 horizon "
                         "segments instead of ~4. So it does not buy policy credit on the opening. "
                         "It buys COVERAGE -- opening states stay in the distribution so the critic "
                         "can learn to value them -- and that has to come first, because policy "
                         "gradient on an opening is worth nothing until the critic separates a good "
                         "one from a bad one. Shift the mix on the value probe "
                         "(scripts/diagnose_policy.py, section 4: V spread within early-day boards), "
                         "NOT on the update count, which is why there is deliberately no flag that "
                         "anneals the mix automatically.")
    ap.add_argument("--curriculum-min-bank", type=float, default=None,
                    help="lower bound on a seed board's seat final bank")
    ap.add_argument("--curriculum-max-bank", type=float, default=None,
                    help="upper bound, and this is the anti-bias dial. Ranking by final bank and "
                         "taking the top gives a pool that is almost one strategy: of 48 day-25 "
                         "boards, 46 carry five or more animals, median 17. The seats are not "
                         "uniform though -- one banked $86,206 with FEED ZERO (163 plants, 1,256 "
                         "waterings) and 30 of 124 seats above $60k are bottom-quartile feeders; "
                         "bank correlates with feed count at only 0.227. Measured pools: "
                         "$15-35k gives median 0 animals (45/48 boards under five) and is nearly "
                         "pure crop play; $35-70k gives median 16 but 15/48 low-animal, i.e. MIXED. "
                         "The mixed band is the one where the policy chooses a strategy rather than "
                         "inheriting ours.")
    ap.add_argument("--curriculum-top", type=int, default=0,
                    help="cap the number of recorded seats the seed pool is drawn from. 0 (default) "
                         "means ALL of them. This was hard-coded to 200 while 312 seats exist on "
                         "disk, so 112 boards were never used and a --batch 256 pool had to draw "
                         "some boards twice. Fewer distinct boards is an overfitting surface: a "
                         "restarting slot goes back into seed_states[i] by index, so with "
                         "--curriculum-resample 25 and ~4-update day-25 episodes each slot replays "
                         "ITS OWN board about 7 times before the pool changes. Lower --curriculum-"
                         "resample and raise this together; they are the same knob, board diversity.")
    ap.add_argument("--curriculum-resample", type=int, default=25,
                    help="updates between redrawing the seed pool, even when the schedule's day has "
                         "not moved. The pool is indexed elementwise on restart, so without this a "
                         "fixed --curriculum-day reuses the SAME board per slot for the whole run "
                         "-- about nine repeats of one recorded game per slot over 33 updates, "
                         "which trains against a memorised set rather than a distribution. 0 keeps "
                         "the old build-on-day-change-only behaviour.")
    ap.add_argument("--curriculum-symmetric", action="store_true",
                    help="give BOTH seats seat 0's entire position -- cash, crops, animals, units, "
                         "land, tiles -- so the only difference between the players is what they DO. "
                         "By default both seats come from the same recorded turn, which means a real "
                         "strong player against their real opponent and the trainee inheriting the "
                         "richer side: a win can then be inherited rather than earned and no win rate "
                         "can tell the two apart. Levelling only the CASH would not fix it, because "
                         "at day 25 the gap is mostly assets (16 animals against 4) while the banks "
                         "differ ~13%% ($69k against $61,440). Both sides remain a real, internally "
                         "consistent board, so this cannot trigger the empty-opponent tie bug -- but "
                         "no recorded game had two identical farms, so the PAIRING is synthetic even "
                         "though each board is real. Makes `vs idle` a real test: idle then holds the "
                         "same rich farm we do and its crops die after two unwatered days, so failing "
                         "to beat it proves we are not maintaining a farm. Needs --curriculum-mix.")
    ap.add_argument("--curriculum-mirror", action="store_true",
                    help="play every seeded board from BOTH sides: half the batch inherits the "
                         "richer of the two recorded seats and half the poorer, on the same boards. "
                         "Both seats come from one recorded turn, so a seeded game is never "
                         "symmetric -- and by default the trainee always gets the richer side, which "
                         "means a win can be inherited rather than earned and a win rate cannot tell "
                         "the two apart. Mirroring cancels that in the aggregate WITHOUT editing the "
                         "board: equalising the two seats' money would fabricate a position no "
                         "recorded game produced, and an inconsistent two-seat board is what made "
                         "the scripted farmer decline to act and scored every episode a 0.5 tie. "
                         "Measured symptom this exists for: 0.77 against an opponent that takes no "
                         "actions at all, from the richer seat. Ignored without --curriculum-mix.")
    ap.add_argument("--curriculum-behind", action="store_true",
                    help="seed the trainee into the POORER of the two recorded seats. Both seats "
                         "come from one recorded turn either way, so this only chooses which side "
                         "it inherits. Default (richer seat) makes the position beatable on the "
                         "seed alone, which is the fastest route to a non-constant outcome and is "
                         "also indistinguishable in a win rate from having learned anything -- the "
                         "tell is a bank curve flat from the seed day rather than rising. This flag "
                         "is the check: a win from the poorer seat has to be earned.")
    ap.add_argument("--resume", default=None, help="path to a checkpoint .pkl to continue from")
    ap.add_argument("--init", default=None,
                    help="warm-start PARAMS ONLY from a BC checkpoint (scripts/bc_dagger.py), "
                         "leaving the optimiser fresh and the update counter at zero. Params only "
                         "and deliberately no KL-anchor to the same checkpoint: `hand_prior_heads` "
                         "records that a collapsed clone as a prior 'would punish PPO for the one "
                         "behaviour it needs to discover', and init-plus-anchor double-commits to "
                         "whatever bad habit the clone has. Anchor later as a separate experiment "
                         "if PPO is measurably unlearning something good. Ignored with --resume.")
    args = ap.parse_args()

    gamma = args.gamma_per_day ** (1.0 / TURNS_PER_DAY)

    run = RUN_DIR / f"{args.tag}-{time.strftime('%Y%m%d-%H%M%S')}"
    run.mkdir(parents=True, exist_ok=True)
    log_path = run / "log.jsonl"

    print(f"devices: {jax.devices()}")
    print(f"discount: {args.gamma_per_day} per game-day = {gamma:.6f} per turn")
    print(f"          terminal reward retains {args.gamma_per_day ** 30:.3f} of its value at t=0")
    print(f"batch {args.batch} games ({2 * args.batch} seats), horizon {args.horizon} turns, "
          f"{args.n_phases} phase groups of {args.batch // args.n_phases}")

    # Preflight, because the first GPU run OOMed and the cause was not obvious from the flags.
    # Transformer activation memory is linear in minibatch ROWS and quadratic in sequence length;
    # the rollout buffer is linear in horizon * seats. Both are printed so an OOM is predictable
    # from the log rather than discovered 40 seconds in.
    rows = args.horizon * 2 * args.batch
    tokens = 1 + J.TILES + J.MAX_UNITS
    # 1.6x fudge on the analytic figure. The plain attention+MLP arithmetic said 3.26 GiB for a
    # 1024-row minibatch that then failed asking for 5.25 GiB: the epoch `lax.scan` keeps the whole
    # rollout resident while each chunk's activations are live, and XLA's own temporaries are not
    # in the formula either. An estimate that reads low is worse than no estimate -- it gets
    # believed right up to the OOM.
    act_gib = 1.6 * (
        args.minibatch_size * args.heads * tokens * tokens * 4
        + args.minibatch_size * tokens * args.d_model * 5 * 4
    ) * args.layers * 2 / 2**30
    buf_gib = args.horizon * 2 * args.batch * (
        J.TILES * jax_obs.TILE_FEATURES + J.MAX_UNITS * jax_obs.UNIT_FEATURES
        + jax_obs.GLOBAL_FEATURES) * 4 / 2**30
    print(f"rollout rows/update {rows:,}  minibatch {args.minibatch_size} rows "
          f"({max(1, rows // args.minibatch_size)} grad steps x {args.epochs} epochs)")
    print(f"est. memory: activations ~{act_gib:.2f} GiB, rollout buffer ~{buf_gib:.2f} GiB "
          f"(16 GiB card)")
    if act_gib + buf_gib > 11.0:
        print("  WARNING: estimate is close to the card. Lower --minibatch-size or --horizon.")
    print(f"run dir: {run}")

    model = P.Policy(d_model=args.d_model, n_heads=args.heads, n_layers=args.layers,
                     value_margin=args.value_margin)
    key = jax.random.PRNGKey(args.seed)
    key, sub = jax.random.split(key)

    if args.batch % args.n_phases:
        raise SystemExit(f"--batch {args.batch} must be divisible by --n-phases {args.n_phases}")
    state = staggered_states(args.batch, args.n_phases, seed=args.seed)

    # The pool a restarting slot restarts into. Without a curriculum it is the same empty-farm reset
    # the rollout used to build inline; with one it is real recorded boards, rebuilt whenever the
    # schedule's day changes.
    cur_day = 0
    seed_days = None
    # Whether the opening `state` is a seeded board rather than `staggered_states`' empty mid-season
    # one. Drives `initial_virgin` and the `--n-phases` notice, so both read the same fact.
    _seeded_start = False
    # **The mix is deliberately not annealable.** Its whole premise is that the composition moves on
    # the value probe rather than on the update counter, so a flag that walked it on the clock would
    # reintroduce exactly what it exists to avoid. Combining it with --curriculum-day would also
    # leave two sources of truth for what a restarting slot restarts into.
    cur_mix = curriculum.parse_mix(args.curriculum_mix) if args.curriculum_mix else None
    if cur_mix and args.curriculum_day:
        raise SystemExit(
            "--curriculum-mix and --curriculum-day both set. The mix already names every day it "
            f"seeds from ({', '.join(str(d) for d in sorted(cur_mix, reverse=True))}); "
            "--curriculum-day would be a second, conflicting answer to what a restarting slot "
            "restarts into.")
    if cur_mix and args.curriculum_anneal:
        raise SystemExit(
            "--curriculum-mix with --curriculum-anneal. The mix exists so the composition shifts on "
            "the value probe, not the update count; annealing it on the clock is the thing it "
            "replaces. Shift the mix by relaunching with new fractions once the probe justifies it.")

    if cur_mix:
        seed_states, seed_days = curriculum.states_at_mix(
            args.batch, cur_mix, seed=args.seed, behind=args.curriculum_behind,
            min_bank=args.curriculum_min_bank, max_bank=args.curriculum_max_bank,
            mirror=args.curriculum_mirror, symmetric=args.curriculum_symmetric,
            top=args.curriculum_top or None, with_days=True)
        state = seed_states
        _seeded_start = True
        seats = "poorer" if args.curriculum_behind else "richer"
        counts = curriculum.mix_counts(args.batch, cur_mix)
        # Terminal episodes per update per day, so the log states the share that actually matters
        # rather than the slot share, which over-reads the early days by about six-fold.
        eps = {d: n * args.horizon / max(1, (30 - d) * TURNS_PER_DAY) for d, n in counts.items()}
        tot = sum(eps.values()) or 1.0
        shares = "  ".join(f"day {d}: {counts[d]} slots ({100 * counts[d] / args.batch:.0f}%), "
                           f"~{100 * eps[d] / tot:.0f}% of terminal episodes"
                           for d in sorted(counts, reverse=True))
        # **What each rung actually STARTS with, because `vs idle` is unreadable without it.**
        #
        # Under symmetric seats the idle opponent holds its opening money for the whole episode, so
        # "beat idle" means "end above the number below" -- and those numbers span $612 at day 0 to
        # $53,373 at day 25, an 87x spread. One aggregate `vs idle` averages five different games.
        #
        # Worse, the day-0 SEEDED board is a recorded seat that has already spent ~$2,400 of its
        # opening $3,000 on seed, so it starts at $612 holding 7.5 seeds. A real Kaggle game starts
        # at $3,000 holding none. A policy can therefore beat idle on the day-0 rung while ending
        # BELOW its starting money in a real game -- which is exactly what a turn-0 replay showed
        # while `vs idle` read 1.000.
        try:
            starts = []
            for d in sorted(counts, reverse=True):
                probe = curriculum.states_at_mix(
                    8, {d: 1.0}, seed=args.seed, behind=args.curriculum_behind,
                    min_bank=args.curriculum_min_bank, max_bank=args.curriculum_max_bank,
                    mirror=args.curriculum_mirror, symmetric=args.curriculum_symmetric,
                    top=args.curriculum_top or None)
                starts.append(f"day {d}: ${float(jnp.mean(probe.farm.money[:, 0])):,.0f}")
            print("         seeded START money (idle holds this all episode):  "
                  + "   ".join(starts), flush=True)
        except Exception as exc:                                   # noqa: BLE001
            print(f"         (could not probe seeded start money: {exc})", flush=True)
        seat_desc = ("SYMMETRIC seats (both sides get seat 0's whole position; only actions differ)"
                     if args.curriculum_symmetric else
                     "MIRRORED seats (half richer, half poorer, same boards)" if args.curriculum_mirror
                     else f"{seats} seat on every board -- a win can be INHERITED")
        print(f"curriculum: MIXED seeding, {seat_desc}, no annealing -- shift the mix on the "
              f"value probe\n  {shares}", flush=True)

        # Same trap as the single-day path, but the binding day is the LATEST in the mix: a slot
        # seeded at day 25 truncates against a limit of 288 whatever the other slots do, and a mix
        # containing day 0 would otherwise pass a check written against the minimum.
        latest_turn = max(cur_mix) * TURNS_PER_DAY
        if args.early_limit and args.early_limit <= latest_turn:
            raise SystemExit(
                f"--early-limit {args.early_limit} is at or below turn {latest_turn} (game-day "
                f"{max(cur_mix)}, the latest in the mix), so those slots would truncate immediately "
                f"and never finish an episode. Use --early-limit 0 with a curriculum.")
    elif args.curriculum_day:
        # Update 0, not `start_update`: the loop re-derives the day on its first iteration and
        # rebuilds the pool if a resume lands further down the schedule, so this only has to be a
        # valid starting board.
        cur_day = curriculum.schedule(0, args.curriculum_anneal, args.curriculum_day)
        seed_states = curriculum.states_at_day(args.batch, day=cur_day, seed=args.seed,
                                               behind=args.curriculum_behind,
                                               min_bank=args.curriculum_min_bank,
                                               max_bank=args.curriculum_max_bank)
        # Seeded slots start on a real board too, not just restart onto one -- otherwise the first
        # episode of every slot is the empty-board game the curriculum exists to avoid.
        state = seed_states
        _seeded_start = True
        seats = "poorer" if args.curriculum_behind else "richer"
        print(f"curriculum: seeding from real boards at game-day {cur_day} ({seats} seat), "
              f"annealing one day per {args.curriculum_anneal or 'never'} updates", flush=True)

        # **`--early-limit` is an absolute turn number and a seeded episode starts past it.**
        # Truncation fires on `step_index >= early_limit`, so a slot seeded at day 15 (turn 360)
        # against a limit of 288 truncates on its first turn, restarts to turn 360, and truncates
        # again -- forever. Half the batch (the even envs) then produces no episodes at all, which
        # shows up as `wr nan` and `tstd 0.000` rather than as an error.
        #
        # The flag's purpose is to train the opening more often than once a season; a curriculum
        # already shortens every episode, so the two do not compose.
        start_turn = args.curriculum_day * TURNS_PER_DAY
        if args.early_limit and args.early_limit <= start_turn:
            raise SystemExit(
                f"--early-limit {args.early_limit} is at or below the curriculum's start turn "
                f"{start_turn} (game-day {args.curriculum_day}), so every early env would truncate "
                f"immediately and never finish an episode. Use --early-limit 0 with a curriculum.")
    else:
        seed_states = J.reset_with_shops(args.batch, seed=args.seed)
    warn_if_phases_inert(args.n_phases, seeded=_seeded_start)
    tiles, units, glob = jax_obs.encode(state)
    params = model.init(sub, A._flat(tiles), A._flat(units), A._flat(glob))
    n_params = sum(x.size for x in jax.tree_util.tree_leaves(params))
    print(f"params: {n_params:,}")

    # Refuse to start in float64. `jax_sim` enables x64 for parity, so anything that does not state
    # its dtype silently becomes float64 -- and this card runs float64 at 1/32 rate. That cost a
    # measured 24 turns/s against a simulator doing 44,700/s, and nothing about the logs looked
    # wrong. A loud failure at startup is worth more than a slow run that finishes next month.
    bad = sorted({str(x.dtype) for x in jax.tree_util.tree_leaves(params)} - {"float32"})
    if bad:
        raise SystemExit(
            f"policy parameters are {bad}, expected float32 only.\n"
            "Something dropped an explicit dtype -- see kagg/rl/jax_policy.py::DTYPE."
        )
    print("dtype check: all policy params float32")

    optimiser = optax.adam(args.lr)
    opt_state = optimiser.init(params)
    target_params = params
    # The pool starts holding the initial policy: an untrained opponent is still a real opponent,
    # and beating it is the first thing worth being able to measure.
    # **The behaviour-cloned prior, used for three things at once.**
    #
    # As the KL target it replaces the entropy bonus; as `--init` it starts the policy inside the
    # economy instead of outside it; and dropped into `pool` it is the first opponent in this run's
    # history that has ever farmed. Every existing pool member is a frozen copy of the policy at
    # some point in its life, and the policy has always been inert -- so the "opponent pool" was
    # entirely self-referential and could not punish standing still.
    prior_params = None
    if args.kl_prior:
        with open(args.kl_prior, "rb") as fh:
            raw = pickle.load(fh)["params"]
        # A pre-op-axis checkpoint is tiled onto the new argument heads rather than rejected. See
        # `jax_policy.migrate_params`: the tiling reproduces the checkpoint's own marginal on every
        # op slice, so the prior it anchors to is behaviourally the checkpoint, not an approximation
        # of it. Without this the op-axis change would silently cost us the KL anchor.
        prior_params = jax.device_put(P.load_or_migrate(raw, params))
        print(f"KL prior loaded from {args.kl_prior} (coef {args.kl_coef}, "
              f"ent_coef {args.ent_coef})", flush=True)

    # **One list of records, not three lists indexed in parallel.** It was `pool`, `pool_wr` and
    # `pool_games`, kept in step by hand at four call sites, and eviction updated only the first --
    # which killed a run at update 250 with `ValueError: a and p must have same size` and, before
    # that, silently attributed every win-rate EMA to the wrong checkpoint. See `kagg/rl/league.py`.
    pool = league.Pool(max_size=args.pool_size)
    # **Seeded AFTER `--resume`, not here.** This used to be `pool.add(params)` on the line below,
    # thirty lines before the resume block replaces `params` with the checkpoint's -- so every
    # resumed run spent `--opponent-frac` of its batch playing a *randomly initialised network*.
    # Measured when it finally bit: `wr_pool` read **1.000 over 80 games** while `bank_final_med`
    # halved from $18,332 to $6,783 and `wr_farm` went from 0.254 to 0/141 in 75 updates. Nearly
    # half the policy's experience was against an opponent that cannot teach anything, and the
    # policy drifted toward beating it.
    #
    # Nothing about it was visible: a fresh run seeds the pool from its own init, which is correct,
    # so the bug only exists on the resume path and only shows up as "the pool got easy".
    # **Opponents are sampled by how well they do against us, not round-robin.**
    #
    # Ender: "prioritised based on recent winrate, with more difficult checkpoints being played
    # more often. This seems especially important for the 4-player game mode." Ours was
    # `pool[it % len(pool)]`, which plays the random initialisation exactly as often as the best
    # checkpoint in the pool -- a lottery rather than a curriculum.
    #
    # `Member.wr` is an EMA of the *opponent's* win rate, so a checkpoint that beats us has a high
    # value and gets picked more. His weights, ported directly:
    #     weight = floor + winrate ** temperature,  plus 0.25 while a member is unplayed
    if prior_params is not None:
        pool.add(jax.device_get(prior_params))

    start_update = 0
    best_wr = -1.0
    if args.init and not args.resume:
        with pathlib.Path(args.init).open("rb") as fh:
            bc = pickle.load(fh)
        # **The observation width is part of the checkpoint.** A BC run trained against a different
        # tile/unit/global width cannot load here, and the failure would otherwise surface as an
        # opaque shape error deep in `apply`. Say so plainly instead.
        want = (jax_obs.TILE_FEATURES, jax_obs.UNIT_FEATURES, jax_obs.GLOBAL_FEATURES)
        got = tuple(bc.get("widths") or ())
        if got and got != want:
            raise SystemExit(
                f"--init checkpoint was trained on observation widths {got}, this build is {want}. "
                f"Retrain BC against the current observation.")
        params = jax.device_put(P.load_or_migrate(bc["params"], params))
        print(f"warm-started params from {args.init} "
              f"(teacher: {bc.get('args', {}).get('teacher', '?')}); optimiser is fresh")
    if args.resume:
        ck = load_checkpoint(args.resume)
        # **A resume must migrate too, and the optimiser state cannot come with it.**
        #
        # This branch used to assign `ck["params"]` straight through, so a checkpoint from before an
        # observation gained a feature failed with a shape error deep inside `apply` -- while
        # `--init` and `--kl-prior` three lines up both went through `load_or_migrate`. P3 added a
        # `glob` column, which is exactly that case, and resuming `league1` is the whole point of it.
        #
        # `opt_state` holds Adam's first and second moments, shaped like the parameters. Widening a
        # kernel therefore invalidates them, and there is no honest value to pad in: a moment is a
        # running average of gradients that were never taken for the new row. So the optimiser is
        # restarted rather than reshaped, and it says so -- a silently mismatched moment array is the
        # kind of thing that shows up as an unexplained instability twenty updates later.
        # `load_or_migrate` returns its input *unchanged* when the checkpoint already fits, so
        # identity is the exact test for "did anything have to be reshaped" -- no shape walk needed.
        # `opt_state` was built by `optimiser.init(params)` above from the freshly initialised
        # parameters, so it already has this architecture's shapes and is the right thing to keep.
        resumed = P.load_or_migrate(ck["params"], params)
        migrated = resumed is not ck["params"]
        params = jax.device_put(resumed)
        if migrated:
            print(f"resumed from {args.resume} and MIGRATED to this architecture "
                  f"(observation widths are now "
                  f"{(jax_obs.TILE_FEATURES, jax_obs.UNIT_FEATURES, jax_obs.GLOBAL_FEATURES)}); "
                  f"**optimiser state discarded** -- Adam's moments do not fit the new shapes.",
                  flush=True)
        else:
            opt_state = ck["opt_state"]
        start_update = ck["update"] + 1
        best_wr = ck.get("best") or -1.0
        print(f"resumed from {args.resume} at update {start_update}")

    # The pool's first member is the policy we are actually starting from. On a fresh run that is
    # the initialisation; on a resume it is the checkpoint. Seeding it before the resume block made
    # every resumed run play a random network for `--opponent-frac` of its batch -- see the comment
    # where `pool` is constructed.
    pool.add(jax.device_get(params))

    latest_ckpt = run / "latest.pkl"
    best_ckpt = run / "best.pkl"
    # Save immediately, so the run is known to be checkpointable before hours are invested in it.
    save_checkpoint(latest_ckpt, params, opt_state, start_update - 1, args)
    print(f"checkpoints: {latest_ckpt} (every {args.ckpt_every} updates) and {best_ckpt}")
    print(f"log:  {log_path}")
    print(f"tail: scripts/deploy_train.sh watch", flush=True)

    # **Load the recorded seats before the rollout is built**, because the rollout captures them as
    # closure constants. A missing file with `--tape-frac 0` is not an error; with a non-zero frac
    # it is, and it must fail here rather than silently seating a self-play opponent under a label
    # that says `tape` -- the unstable-label failure CLAUDE.md records for `farm:0.445`.
    tape_actions = None
    if args.tape_frac > 0:
        with np.load(args.tape_actions) as npz:
            tape_actions = {k: jnp.asarray(npz[k]) for k in npz.files
                            if k not in ("names",) and not k.startswith("w_")}
        n_tapes, n_turns = tape_actions["op"].shape[:2]
        print(f"tape opponents: {n_tapes} recorded seats x {n_turns} turns, "
              f"heads {sorted(tape_actions)}", flush=True)
        if n_turns != EPISODE_TURNS:
            raise SystemExit(f"tape actions are {n_turns} turns, episode is {EPISODE_TURNS}")

    rollout = make_rollout(model, args.batch, args.horizon, gamma, args.gae_lambda,
                           args.n_phases, shaping_coef=args.shaping_coef,
                           tape_actions=tape_actions)
    update, run_epochs = make_update(model, args.clip, args.vf_coef, args.ent_coef,
                                     args.max_grad_norm, optimiser, seat_coef=args.seat_coef,
                                     kl_coef=args.kl_coef, prior_params=prior_params,
                                     hand_noop_p=args.hand_prior,
                                     spend_p=args.spend_prior)

    # Role probabilities, in `ROLE_NAMES` order. Self-play is the remainder, as it always was, but
    # now explicitly rather than by falling through a partition.
    role_p = np.array([0.0, args.opponent_frac, args.farm_frac,
                       args.trade_frac, args.idle_frac, args.ranch_frac,
                       args.carrot_frac, args.homestead_frac,
                       args.tape_frac if tape_actions is not None else 0.0], dtype=np.float64)
    if role_p[1:].sum() > 1.0:
        raise SystemExit(
            "opponent/farm/trade/idle/ranch/carrot/homestead/tape fracs sum to "
            f"{role_p[1:].sum():.2f} > 1.0")
    role_p[ROLE_SELF] = 1.0 - role_p[1:].sum()
    print("seat-1 roles, sticky per episode: "
          + "  ".join(f"{n}:{p:.0%}" for n, p in zip(ROLE_NAMES, role_p)))
    # Per-slot, so `idle` can be confined to the day-0 rung. See `role_logits_per_slot`.
    role_logp = role_logits_per_slot(role_p, seed_days, args.batch)
    pool_hold = league.hold_updates(args.horizon, EPISODE_TURNS)
    print(f"pool: one member holds the seat for {pool_hold} updates "
          f"(= {EPISODE_TURNS} turns / horizon {args.horizon}), so a game faces at most two")
    # Initial draw. Games are mid-season at their staggered phases, so this is the only point where
    # a role is assigned to a game that did not just start -- unavoidable, and it washes out within
    # one season as each game terminates and re-draws.
    roles = jax.random.categorical(
        jax.random.PRNGKey(args.seed + 1), role_logp, shape=(args.batch,))
    # Without a curriculum every slot starts mid-season on an empty board, so no slot's *first*
    # termination is a real result. With one, the opening state IS a seeded board and its first
    # episode is genuine -- see `initial_virgin`. Cleared per slot as soon as it restarts anyway.
    virgin = jnp.full((args.batch,), initial_virgin(seeded=_seeded_start), dtype=bool)

    n_seats = 2 * args.batch
    flat_n = args.horizon * n_seats
    wins, games = 0.0, 0.0
    # Cumulative, per opponent type, in the same units as `wins`/`games` above.
    day_wins, day_games = {}, {}
    opp_wins = {k: 0.0 for k in OPPONENT_NAMES}
    opp_games = {k: 0.0 for k in OPPONENT_NAMES}
    opp_draws = {k: 0.0 for k in OPPONENT_NAMES}
    # Cumulative opponent-by-day cells, keyed `"{opponent}_d{day}"`. Cumulative because a single
    # update splits ~10 finished games across up to 25 cells, and a per-update cell rate is noise.
    opp_day_wins, opp_day_games = {}, {}
    t_start = time.time()

    # Loud, because a silent exit here is exactly what could not be diagnosed: the process wrote
    # its startup checkpoint, returned exit code 0, and produced no `log.jsonl` at all -- which
    # looks identical to a crash from the outside but is not one. If the loop is never entered,
    # this line says so; if the first rollout dies, the traceback below says that instead.
    print(f"entering training loop: updates {start_update}..{args.updates}, "
          f"{flat_n:,} rows/update", flush=True)
    # The first rollout traces and compiles the whole scan -- sim, policy and GAE -- which takes
    # minutes and prints nothing. Silence at this exact point is also what every genuine failure
    # looked like, so say plainly that silence is expected here.
    print(f"compiling the first rollout ({args.horizon}-turn scan); this takes a few minutes and "
          f"prints nothing until update 0", flush=True)
    if start_update >= args.updates:
        print(f"NOTHING TO DO: start_update {start_update} >= updates {args.updates}", flush=True)

    for it in range(start_update, args.updates):
        key, sub = jax.random.split(key)
        # Seat-1 roles are now sticky per episode and live in the rollout's scan carry, so there
        # is nothing to partition here. The history of this line is worth keeping, because it was
        # wrong three times in three different ways and each fix exposed the next:
        #
        #  1. Four independent strided picks, each dropping indices another had claimed. The strides
        #     shared residue classes, so **every** trader pick collided and was filtered out: the
        #     realised mix was pool 14.8%, farmer 30.1%, trader 0.0%, idle 2.7%, self 52.3%.
        #  2. One rotating permutation `(arange + it) % batch`, which made the shares exact and
        #     reintroduced contiguity -- a game's index is its phase, so each role got a contiguous
        #     band of the season and the scripted seats never played the endgame at all.
        #  3. A strided permutation, which spread the bands correctly and still re-drew every role
        #     every update, while a game spans ~22.5 updates. A game faced a mean of 4.9 distinct
        #     opponents per season and no measurement of any of them was valid.
        #
        # See the block comment above `make_rollout` for what that cost.
        # **One member holds the seat for a whole episode.** Drawn per update, seat 1 was played
        # by ~23 different checkpoints per game -- see `league.select`. `pool_hold` is derived from
        # the horizon rather than exposed as a flag, because the correct value is arithmetic:
        # however many updates it takes to cover `EPISODE_TURNS`.
        opp_idx = pool.select(args.seed, it, hold=pool_hold)
        opp_params = pool.params(opp_idx)

        # The curriculum's start day walks down on the update clock, and the seed pool is rebuilt
        # only when it changes -- building it parses replay JSON, so per-update would dominate.
        # Deliberately clock-driven rather than win-rate-driven: a schedule advanced by the same
        # metric that judges it is self-confirming, and a curriculum advancing because outcomes
        # went degenerate would look identical to one advancing because the policy improved.
        if cur_mix:
            # No day to re-derive: the mix is fixed for the run by design. Only the resample fires,
            # and it must, for the same elementwise-reuse reason as the single-day path -- with a mix
            # the reuse is worse, because a slot would be pinned to one board AND one game-day for
            # the whole run.
            if args.curriculum_resample and it % args.curriculum_resample == 0:
                seed_states, seed_days = curriculum.states_at_mix(
                    args.batch, cur_mix, seed=args.seed + it, behind=args.curriculum_behind,
                    min_bank=args.curriculum_min_bank, max_bank=args.curriculum_max_bank,
                    mirror=args.curriculum_mirror,
                    symmetric=args.curriculum_symmetric, top=args.curriculum_top or None,
                    with_days=True)
                # **Rebuild the per-slot role logits, because which slots are day-0 just changed.**
                # `idle` is confined to the day-0 rung, and that confinement is expressed as a mask
                # over slot indices -- so a resample that reassigns days without rebuilding this
                # would leave idle seated against whichever rungs happened to be day-0 last time.
                # Exactly the stale-label failure this file keeps being bitten by.
                role_logp = role_logits_per_slot(role_p, seed_days, args.batch)
                days = ", ".join(str(d) for d in sorted(cur_mix, reverse=True))
                print(f"         curriculum: reseeding mixed pool (days {days})"
                      f"{' (trainee in the poorer seat)' if args.curriculum_behind else ''}",
                      flush=True)
        elif args.curriculum_day:
            want_day = curriculum.schedule(it, args.curriculum_anneal, args.curriculum_day)
            # **Resample even when the day has not moved.** The pool is indexed elementwise on
            # restart (`fresh = seed_states`), so slot `i` restarts into `seed_states[i]` every
            # time. Rebuilding only on a day change meant that with `--curriculum-anneal 0` the
            # same `batch` boards were reused for the entire run -- roughly nine repeats of one
            # recorded game per slot over 33 updates, which is an overfitting surface rather than
            # a curriculum. Costs a few seconds of replay parsing per rebuild.
            if want_day != cur_day or (args.curriculum_resample
                                       and it % args.curriculum_resample == 0):
                cur_day = want_day
                seed_states = curriculum.states_at_day(
                    args.batch, day=cur_day, seed=args.seed + it, behind=args.curriculum_behind,
                    min_bank=args.curriculum_min_bank, max_bank=args.curriculum_max_bank)
                print(f"         curriculum: seeding from game-day {cur_day}"
                      f"{' (trainee in the poorer seat)' if args.curriculum_behind else ''}",
                      flush=True)

        state, roles, virgin, key, traj, advantages, returns = rollout(
            params, target_params, opp_params, roles, role_logp, virgin,
            jnp.asarray(args.early_limit, dtype=jnp.int32), state, sub, seed_states)

        # Episode bookkeeping is reduced **on device** to three scalars. Pulling the full `done`
        # and `reward` arrays back to the host, as this did, forces a synchronisation on every
        # update and blocks the pipeline on a transfer whose only purpose is a running average.
        # **Seat-sum consistency.** For a matched (game, turn) pair the two seats are the same
        # board from opposite sides, so V(seat 0) + V(seat 1) must be 1 in expectation for ANY
        # policy -- win 1 + loss 0, or tie 0.5 twice. It is not a property of a *good* critic, it
        # is arithmetic, and it holds on 100% of rows rather than the ~0.14% that carry a terminal
        # reward. If this sum tracks 1 while mean(V) sits at 0.82, the critic is consistent and the
        # high mean says something about which states get sampled. If it climbs with mean(V), both
        # seats are claiming to win the same game and the critic is provably broken.
        #
        # **It describes whichever net produced `traj["value"]`, which is not always the one being
        # trained.** Under `--target-ema` that is the slow EMA copy, and an EMA is not the network
        # any gradient has touched: at decay 0.99 it still carries `0.99^n` of the random
        # initialisation, which is 53% at update 63. A run with the EMA on therefore printed
        # `V 0.606 sum 1.212` -- the exact signature of a seat-blind critic -- while `seat_loss`
        # on the live net read 0.0006, i.e. a seat sum of 1.02 and perfectly healthy. The diagnostic
        # was reporting the untrained initialisation showing through the average, and it was read as
        # the anchor having failed. `seat_loss` is the live net and is the one to trust; the column
        # is labelled in the log line so the two cannot be confused again.
        v_pairs = traj["value"].reshape(traj["value"].shape[0], -1, 2)
        seat_sum = v_pairs.sum(axis=-1)
        seat_sum_mean = seat_sum.mean()
        seat_sum_absdev = jnp.abs(seat_sum - 1.0).mean()

        # **Win rate over cross-play rows only, because every other row is pinned.**
        #
        # Summing reward across both seats of a game is arithmetically 0.5 -- one winner and one
        # loser, always. Restricting to `trainable` was supposed to fix that and does not: in a
        # self-play group *both* seats are trainable, so both are counted and the pair still
        # averages exactly 0.5. At `--opponent-frac 0.25` a self-play game contributes two pinned
        # rows and a cross-play game one free row, so 86% of what was measured could not move, and
        # it duly read 0.500 to three decimals on every update of a 63-update run.
        #
        # The live policy's seat in a cross-play game is the only row whose outcome is not
        # determined by its partner. That is the whole signal, so measure exactly it, and log the
        # count alongside because a few dozen rows an update is a noisy estimate that should be
        # read as such.
        live = traj["trainable"] & traj["crossplay"]
        done_live = traj["done"] & live
        done_count = done_live.sum()
        reward_sum = jnp.where(done_live, traj["reward"], 0.0).sum()

        # **The league EMA needs games against *that checkpoint*, not against anything at all.**
        #
        # `crossplay` is true for the idle seat, the trader and the farmer as well as for the pool
        # checkpoint. Feeding all of it into one checkpoint's difficulty estimate means up to three
        # quarters of the evidence has nothing to do with that checkpoint, and the priority
        # weighting then pushes sampling in the wrong direction -- the opposite of what it is for.
        pool_live = traj["trainable"] & traj["vs_pool"] & traj["done"]
        pool_done = pool_live.sum()
        pool_reward = jnp.where(pool_live, traj["reward"], 0.0).sum()

        # Per-opponent-type win rate, on the same rows `done_live` counts: the live policy's own
        # seat, in a finished game, against one named opponent. Counts are logged beside each rate
        # because a few games an update is a noisy estimate and a bare 0.33 hides whether it came
        # from one game or thirty -- the same mistake `wr` made before its count was printed.
        by_opp = {}
        for _name, _flag in OPPONENT_FLAGS:
            _rows = traj["trainable"] & traj[_flag] & traj["done"]
            by_opp[f"done_{_name}"] = _rows.sum()
            by_opp[f"rew_{_name}"] = jnp.where(_rows, traj["reward"], 0.0).sum()
            # **Draws counted separately, because a mean of 0.5 has two very different causes.**
            #
            # In symmetric self-play one seat wins and one loses, so the mean is 0.5 by construction
            # at any skill -- that is arithmetic, not a plateau, and it is true of AlphaZero too.
            # What separates a healthy mirror from a dead one is variance: fifty wins and fifty
            # losses gives mean 0.5 with real gradient, a hundred draws gives mean 0.5 with none.
            #
            # Right now it is the second: both seats bank $0 and `money == money` is exact, so every
            # mirror game is a guaranteed tie. `wr_pool` alone cannot tell those apart, which is the
            # same shape as every other metric in this file that had to be fixed -- correct on its
            # own terms and unable to answer the question being asked of it.
            by_opp[f"draw_{_name}"] = jnp.where(
                _rows, (traj["reward"] == 0.5).astype(jnp.float32), 0.0).sum()

        # **Per-SEED-DAY win rate, which the aggregate cannot show.** With
        # `--curriculum-mix 25:0.6,20:0.1,15:0.1,10:0.1,0:0.1` the day-25 slots supply ~83% of
        # terminal episodes, so `wr` and even `wr_farm` are day-25 numbers wearing a mix's name: the
        # four middle rungs could improve dramatically or die entirely and neither would move.
        #
        # The seed day is a CONSTANT per slot -- a restarting slot goes back into `seed_states[i]` by
        # index -- so no scan carry is needed and this is computed here, outside jit, on the same
        # rows `by_opp` uses: the live policy's own seat, in a finished game. `traj` rows are
        # [horizon, batch * 2], so the batch axis has to be exposed before the day mask can apply;
        # a mask broadcast against the flat axis would silently attribute rows to the wrong day.
        by_day = {}
        # **Opponent CROSSED with seed day, because neither margin can be read on its own.**
        #
        # `wr_farm` averages over whatever day mix the curriculum happened to be serving, and
        # `wr_day0` averages over whatever opponent mix it happened to be serving. When
        # `--curriculum-resample` moves the mix, a *constant* policy shows a moving `wr_farm` --
        # this run's farm rate fell 0.73 -> 0.03 across the update-125 resample purely because the
        # day-0 share of finished games went 0% -> 70%, and read as a collapse. Neither existing
        # margin can distinguish that from a real one; the cross-tab can, because opponent and day
        # are both held fixed inside a cell.
        by_opp_day = {}
        if seed_days is not None:
            _n = args.batch
            _shape = (-1, _n, 2)
            _rows_all = (traj["trainable"] & traj["done"]).reshape(_shape)
            _rew_all = traj["reward"].reshape(_shape)
            _days = jnp.asarray(seed_days)[None, :, None]
            for _d in sorted(set(int(x) for x in seed_days), reverse=True):
                _m = _rows_all & (_days == _d)
                by_day[f"done_d{_d}"] = _m.sum()
                by_day[f"rew_d{_d}"] = jnp.where(_m, _rew_all, 0.0).sum()
                # Same rows the margin above counts, split once more by opponent. Cells are
                # individually small -- a 25-cell split of ~10 finished games an update -- so
                # every cell is logged with its own count and read cumulatively, never as a
                # single-update rate.
                for _name, _flag in OPPONENT_FLAGS:
                    _mo = _m & traj[_flag].reshape(_shape)
                    by_opp_day[f"done_{_name}_d{_d}"] = _mo.sum()
                    by_opp_day[f"rew_{_name}_d{_d}"] = jnp.where(_mo, _rew_all, 0.0).sum()

        # Terminal rows carry return == reward, so their spread should be ~0.25 and `ev_signal`
        # should always be computable. It reported n/a on half the updates, so count them.
        n_terminal = traj["done"].sum()
        rewarded_frac = traj["done"].mean()

        def flatten(x):
            return x.reshape(flat_n, *x.shape[2:])

        batch_data_full = dict(
            old_logp=flatten(traj["logp"]),
            old_value=flatten(traj["value"]),
            trainable=flatten(traj["trainable"]),
            adv=flatten(advantages),
            returns=flatten(returns),
            actions={k: flatten(v) for k, v in traj["actions"].items()},
            masks={k: flatten(v) for k, v in traj["masks"].items()},
            obs=tuple(flatten(x) for x in traj["obs"]),
            # The behaviour policy's own decision mask. `A.evaluate` must be given exactly this,
            # not a recomputed version -- see the note where it is stored.
            decided=flatten(traj["decided"]),
        )

        # Explained variance, also reduced on device. `ev` over everything is mostly the critic
        # scoring itself on reward-free rows; `ev_signal` restricts to rows where an episode
        # actually ended, which is the only version that can fail.
        ret_d = batch_data_full["returns"]
        val_d = flatten(traj["value"])
        ev_d = 1.0 - (ret_d - val_d).var() / jnp.maximum(ret_d.var(), 1e-8)

        # **Shaping diagnostics.** `traj["reward"]` holds terminal + shaping; the terminal part is
        # non-zero only on `done` rows, so differencing gives the shaping contribution without
        # carrying a second array through the scan.
        _r = flatten(traj["reward"])
        _terminal_part = jnp.where(flatten(traj["done"]), _r, 0.0)
        _shape_part = _r - _terminal_part
        shape_abs_mean = jnp.abs(_shape_part).mean()
        shape_share = jnp.abs(_shape_part).sum() / jnp.maximum(jnp.abs(_r).sum(), 1e-8)
        # The critic's representable range. `rescale_value` maps a sigmoid onto [-margin, 1+margin],
        # so a return outside that band cannot be predicted and the value loss is bounded below by
        # the overshoot -- while `ev` stays high, because the predictions remain self-consistent.
        _lo, _hi = -args.value_margin, 1.0 + args.value_margin
        ret_clipped = ((ret_d < _lo) | (ret_d > _hi)).mean()
        done_d = batch_data_full["trainable"] & flatten(traj["done"])
        w = done_d.astype(jnp.float32)
        n = jnp.maximum(w.sum(), 1.0)
        r_mean = (ret_d * w).sum() / n
        r_var = ((ret_d - r_mean) ** 2 * w).sum() / n
        e_var = (((ret_d - val_d) - ((ret_d - val_d) * w).sum() / n) ** 2 * w).sum() / n
        ev_sig_d = jnp.where(r_var > 1e-8, 1.0 - e_var / jnp.maximum(r_var, 1e-8), jnp.nan)

        # **The spread of returns on rows that actually resolved.**
        #
        # `ret_std` is taken over every row of the rollout, and only ~0.14% of rows carry a reward
        # -- one turn in 719. For the rest GAE's `return = advantage + value` collapses to the value
        # bootstrap, so `ret_mean` tracks `value_mean` almost exactly and `ret_std` describes the
        # *critic's* output spread, not the distribution of outcomes. A small `ret_std` was read
        # here as "every game is ending in a draw"; it supports no such conclusion, and the two
        # possibilities -- genuine draws, or a critic that has collapsed onto one number -- are
        # indistinguishable from it. `r_var` above is the statistic that separates them and it was
        # computed and thrown away.
        terminal_ret_std = jnp.sqrt(jnp.maximum(r_var, 0.0))

        # **How much of the value loss the terminal rows actually carry.**
        #
        # Item 1 of `docs/critic_terminal_blindness_2026-08-03.md`, which asks for a measurement
        # before any third mechanism is added. The premise everywhere in this file is that terminal
        # rows are ~0.14% of the batch and the critic therefore trains on its own bootstrap -- but
        # *count* share and *loss* share are different numbers, and only the second one says whether
        # upweighting those rows would change the gradient. A terminal row's target is the true
        # outcome rather than a bootstrap, so its squared error is usually far larger than a
        # reward-free row's; if 0.14% of rows already carry 2% of the loss they have 14x leverage and
        # upweighting is a much smaller intervention than the count suggests.
        #
        # Read-only. These feed the log and nothing else -- no term here enters `loss_fn`, so a run
        # with this instrumentation is bit-identical in its training to one without it.
        _hr = traj["done"].shape                                 # [horizon, rows]
        _shares = terminal_loss_shares(
            sq_err=((ret_d - val_d) ** 2).reshape(_hr),
            trainable=traj["trainable"],
            done=traj["done"])
        term_loss_share = _shares["term_loss_share"]
        term_row_share = _shares["term_row_share"]
        term_leverage = _shares["term_leverage"]
        near_loss_share = _shares["near_loss_share"]
        near_row_share = _shares["near_row_share"]

        # **What the policy is actually doing, which no scalar has ever shown.**
        #
        # Every metric in this log is an aggregate: returns, entropy, a win rate. None of them can
        # distinguish a policy that farms badly from one that stands still, and both look identical
        # in a loss curve. The op census is the diagnostic that found two structural bugs in the
        # heuristic agents in a single run today, and it costs one one-hot sum here. Counted over
        # the live policy's own rows only, so the idle opponent's NOOPs are not mistaken for ours.
        # **Count only slots the farm actually owns.** `trainable` marks rows that are ours rather
        # than an opponent's; it says nothing about whether a *unit* exists. `MAX_UNITS` is 24 and a
        # crew is ten or so, so fourteen slots in every row are NOOP by construction -- roughly 58%
        # of the census before the policy decides anything. Every "95% noop" reading today was that
        # padding plus the real rate, and the real rate is materially lower. This is the same
        # mistake that was found and fixed in the behaviour-cloning loss and never carried across.
        unit_exists = batch_data_full["obs"][1][..., 0] > 0.5      # `live` is unit feature 0
        live_units = batch_data_full["trainable"][:, None] & unit_exists
        op_rows = batch_data_full["actions"]["op"]
        op_counts = op_census(op_rows, live_units)

        # **Split the census by whether the row can reach a harvest at all.**
        #
        # Early-game envs truncate and restart, so if the limit falls before a crop's
        # `first_yield_day` those rows are *structurally* incapable of a legal HARVEST -- the mask
        # requires `day - planted >= FIRST_YIELD_DAY`. Aggregating them with full-season rows gives
        # a harvest rate that is part policy and part arithmetic, and reads as the policy failing at
        # something it was never allowed to attempt. Same species of mistake as counting unit slots
        # the farm does not own.
        full_rows = jnp.tile(~jnp.repeat(
            jnp.asarray((np.arange(args.batch) % 2) == 0), 2)[None, :],
            (args.horizon, 1)).reshape(-1)
        full_live = live_units & full_rows[:, None]
        op_counts_full = op_census(op_rows, full_live)

        # **The market heads have never been logged, and FEED has never once fired.**
        #
        # `masks[O.FEED]` and `jax_sim`'s FEED gate impose the identical three conditions, and the
        # shed/PICKUP/item-mask path is proven working -- `buy_animal` deposits to the shed exactly
        # as `buy_product` would, and 4,591 animals were placed through it. So FEED is reachable,
        # and wheat simply never arrives. Which leaves two explanations that no metric here can
        # separate:
        #
        #  - `trade` has collapsed onto one mode. `sell` and `buy_product` are the only
        #    `CONDITIONED_HEADS`: their distribution is whichever slice the sampled mode selects,
        #    so a collapsed `trade` means wheat's slice is never drawn however good its marginal
        #    is. `buy_animal` is unconditioned, straight off `gtok` -- which is exactly the split
        #    between the thing that happens thousands of times and the thing that never happens.
        #    `hand_prior_heads` shapes only `op`; every other head gets a uniform KL target, which
        #    is the treatment already shown not to prevent `op`'s own collapse.
        #  - Or the compound probability of purchase *and* routing *and* a live animal is simply
        #    tiny, and it is rare rather than blocked.
        #
        # A census distinguishes "never sampled" from "sampled vanishingly rarely" and costs the
        # same one-hot sum the op census already does. Per-product rather than WHEAT-only, so no
        # item index is hard-coded here; name the column when reading it.
        # **Read off the BUNDLE, because the `trade` head no longer exists.** The market heads were
        # replaced by a single bundle index in the 2026-08-22 refactor -- `P.N_TRADE_MODES` is gone
        # and `actions["trade"]`, `["sell"]`, `["buy_product"]` and `["buy_animal"]` with it. The
        # question this census answers is unchanged, so it is re-derived rather than deleted: the
        # bundle row says WHICH kinds of order go out, and the four counts below are the same four
        # modes the old head enumerated. `trade_counts` is now (sells / buys seed / buys product /
        # hires), one column each, and the print at the bottom of this file reads it positionally.
        seat_rows = batch_data_full["trainable"].astype(jnp.float32)
        n_seat = jnp.maximum(seat_rows.sum(), 1.0)
        _tb = _bundle_tables()
        bundle_rows = batch_data_full["actions"]["bundle"]
        _any = lambda col: (_tb[col][bundle_rows] > 0).any(axis=-1)          # noqa: E731
        trade_counts = jnp.stack([
            (_any("sell") * seat_rows).sum(),
            (_any("buy_seed") * seat_rows).sum(),
            (_any("buy_product") * seat_rows).sum(),
            ((_tb["hire"][bundle_rows] > 0) * seat_rows).sum(),
        ])
        # Class 0 of a market quantity head is quantity zero, so "> 0" is "actually traded". The
        # quantity is only read for the products the bundle activated, so gate on both.
        buy_rate = (((batch_data_full["actions"]["qty_buy_product"] > 0)
                     & (_tb["buy_product"][bundle_rows] > 0)).astype(jnp.float32)
                    * seat_rows[:, None]).sum(axis=0) / n_seat
        sell_rate = (((batch_data_full["actions"]["qty_sell"] > 0)
                      & (_tb["sell"][bundle_rows] > 0)).astype(jnp.float32)
                     * seat_rows[:, None]).sum(axis=0) / n_seat
        # `crop` is a unit head and only PLANT reads it, so count it where a plant was chosen.
        planting = live_units & (op_rows == O.PLANT_OP)
        crop_counts = (jax.nn.one_hot(batch_data_full["actions"]["crop"],
                                      J.N_CROPS, dtype=jnp.float32)
                       * planting[..., None]).sum(axis=(0, 1))

        # **Which item a PICKUP actually takes, which is the last unmeasured link in the FEED
        # chain.** `masks[O.CARE]` and `masks[O.FEED]` differ by exactly one term --
        # `carrying_wheat` -- and CARE fires while FEED never has. Wheat does reach the shed
        # (`buy_product` runs at 2-22% on the two buyable items), and units pick up hundreds of
        # times per update, so the open question is whether those PICKUPs are taking wheat or
        # taking the animals they then PLACE. `ITEMS = PRODUCTS + ANIMALS`, so the two live in one
        # index space and a single census over it answers the question outright.
        picking = live_units & (op_rows == O.PICKUP)
        item_counts = (jax.nn.one_hot(batch_data_full["actions"]["item"],
                                      J.N_ITEMS, dtype=jnp.float32)
                       * picking[..., None]).sum(axis=(0, 1))

        # **How much capital the animal economy is currently burning.**
        #
        # An animal escapes after two unfed nights (`jax_sim.py:1057`, `unfed >= 2`) and every
        # first-yield day is later than that -- GOOSE 4, COW 8, SHEEP 6. So while FEED sits at
        # exactly zero, every animal bought is a *certain* total loss of its $300-$500 against a
        # $3,000 opening bank, not a bad expected value. The policy is therefore receiving correct
        # and strongly negative advantage on `buy_animal`, which hardens into an aversion that has
        # to be unlearned later -- the hire collapse's shape, but deterministic rather than
        # probabilistic. `PLACE` counts bound this from above and mix in ordinary shed-drops, so
        # count the purchase head itself. It is binary per animal type.
        # Off the bundle now, for the same reason `trade_counts` is: there is no `buy_animal` head
        # any more. The bundle row carries a count per animal type, so this is the same quantity.
        buy_animal_rate = ((_tb["buy_animal"][bundle_rows] > 0).astype(jnp.float32)
                           * seat_rows[:, None]).sum(axis=0) / n_seat

        # **Where the $3,000 goes.**
        #
        # The policy spends its whole opening stake inside five game-days and banks $0 for the
        # remaining twenty-five, verified by replay. That is below the floor of its own opponent
        # ladder -- the idle seat takes no action at all and finishes on $3,000, so an agent doing
        # literally nothing beats ours, and every rung above idle is consequently flat: `farm` and
        # `trade` both read 0.000 and `pool` reads 0.500, so no opponent supplies any gradient.
        #
        # Fixing the leak is worth more than any strategy change, because it is what makes the whole
        # ladder informative again. `buy_product` and `buy_animal` are already counted and are far
        # too small to explain it; these three are the remaining ways to burn a bank quickly.
        # `buy_seed` is per crop so its action is [rows, N_CROPS]; `hire` and `buy_land` are single
        # binary decisions, so [rows]. "Any nonzero this turn" is the comparable rate across all
        # three -- class 0 of a market quantity head is quantity zero.
        # Off the bundle for the same reason as `trade_counts` above: `buy_seed`, `hire` and
        # `buy_land` stopped being heads of their own in the 2026-08-22 refactor. The bundle row
        # carries all three, so the rate measured is unchanged -- "did this turn's chosen bundle
        # fire this kind of order at all".
        def _spend(col):
            a = _tb[col][bundle_rows]
            fired = (a > 0).any(axis=tuple(range(1, a.ndim))) if a.ndim > 1 else (a > 0)
            return (fired.astype(jnp.float32) * seat_rows).sum() / n_seat

        seed_rate = _spend("buy_seed")
        hire_rate = _spend("hire")
        land_rate = _spend("buy_land")

        # Realised role shares. Sticky roles are *sampled*, so the mix is no longer exact by
        # construction the way the strided partition made it -- which means it has to be measured.
        # Three of the four previous versions of this assignment were wrong and two of them looked
        # fine, so print what actually happened rather than what was asked for.
        role_counts = jax.nn.one_hot(traj["roles"], N_ROLES, dtype=jnp.float32).sum(axis=(0, 1))

        # **Anneal the regulariser, which Ender says mattered and which this flag never did.**
        #
        # `--kl-anneal` was parsed and then never read anywhere in this file -- a dead argument for
        # the one mechanism his write-up singles out: "reducing this coefficient later in training
        # resulted in significant improvement". It could not have worked as written either, because
        # `ent_coef` was captured as a Python float when `make_update` built its closure, so it was
        # baked into the compiled graph and constant for the whole run. It is now a traced value.
        #
        # **It decays the KL's *share*, not the coefficient.** Decaying `reg_coef` zeroed the whole
        # regulariser, because on the prior branch the KL *is* the whole regulariser -- so the flag
        # that was meant to release the prior released the policy entirely. `kl_frac` hands the
        # weight over to entropy instead; see `blend_regulariser`.
        reg_coef = args.ent_coef
        kl_frac = jnp.asarray(kl_fraction(args.kl_anneal, it), dtype=jnp.float32)

        n_chunks = max(1, flat_n // args.minibatch_size)
        key, ekey = jax.random.split(key)
        prev_params = params
        params, opt_state, metrics = run_epochs(
            params, opt_state, batch_data_full, ekey,
            epochs=args.epochs, n_chunks=n_chunks, chunk=args.minibatch_size,
            reg_coef=reg_coef, kl_frac=kl_frac)
        # **How far the weights actually moved this update, relative to their own size.**
        #
        # `approx_kl`, `clip_frac` and `grad_norm` all describe the *behaviour* change or the
        # gradient before the optimiser touches it. None of them says whether the network is
        # effectively frozen. A run can show a healthy `grad_norm` and a sane `approx_kl` while the
        # learning rate is too small for anything to move -- and at `--lr 3e-5` on a 727k-parameter
        # net that is a live possibility, not a hypothetical.
        #
        # `||dtheta|| / ||theta||` is one pass over the parameters per update and is scale-free, so
        # it is comparable across runs and architectures. Rough reading: ~1e-3 is ordinary
        # progress, sustained ~1e-5 means the net is standing still and the lr is the binding
        # constraint, and ~1e-1 means it is being thrown around and something upstream is wrong.
        _leaves_new = jax.tree_util.tree_leaves(params)
        _leaves_old = jax.tree_util.tree_leaves(prev_params)
        _delta = jnp.sqrt(sum(jnp.sum((a - b) ** 2) for a, b in zip(_leaves_new, _leaves_old)))
        _scale = jnp.sqrt(sum(jnp.sum(a ** 2) for a in _leaves_new))
        param_drift = _delta / jnp.maximum(_scale, 1e-12)
        target_params = ema_update(target_params, params, args.target_ema)

        # One transfer per update, of scalars only.
        stats = jax.device_get({
            "done_count": done_count, "reward_sum": reward_sum,
            "pool_done": pool_done, "pool_reward": pool_reward,
            "n_terminal": n_terminal,
            "seat_sum": seat_sum_mean, "seat_sum_absdev": seat_sum_absdev,
            "value_mean": flatten(traj["value"]).mean(),
            "rewarded_frac": rewarded_frac, "ev": ev_d, "ev_signal": ev_sig_d,
            "ret_mean": ret_d.mean(), "ret_std": ret_d.std(),
            # **Is the shaping doing anything, and is the critic able to represent it.**
            #
            # `shape_share` is the share of total absolute reward that came from shaping rather than
            # from the win/loss. Near 0 means the coefficient is too small to matter; near 1 means it
            # has become the objective, which invariance does NOT protect against -- the theorem
            # fixes the optimum, not what PPO does with clipping and finite samples.
            #
            # `ret_clipped` is the fraction of GAE returns falling outside `[-margin, 1 + margin]`,
            # i.e. outside what the sigmoid head can express. **This is the important one.** A clipped
            # critic looks exactly like a confident one: `explained_variance` stays high because the
            # predictions are self-consistent, and the error is invisible. Any non-zero reading here
            # means `--value-margin` is too small and every conclusion from the run is suspect.
            "shape_share": shape_share, "shape_abs_mean": shape_abs_mean,
            "ret_clipped": ret_clipped, "ret_min": ret_d.min(), "ret_max": ret_d.max(),
            "terminal_ret_std": terminal_ret_std, "op_counts": op_counts,
            "term_loss_share": term_loss_share, "term_row_share": term_row_share,
            "term_leverage": term_leverage,
            "near_loss_share": near_loss_share, "near_row_share": near_row_share,
            "trade_counts": trade_counts, "buy_rate": buy_rate,
            "sell_rate": sell_rate, "crop_counts": crop_counts,
            "item_counts": item_counts,
            "buy_animal_rate": buy_animal_rate,
            "role_counts": role_counts,
            "seed_rate": seed_rate, "hire_rate": hire_rate, "land_rate": land_rate,
            **by_opp,
            **by_day,
            **by_opp_day,
            **{k: v for k, v in metrics.items()},
        })
        wins += float(stats["reward_sum"])
        games += float(stats["done_count"])
        for _k in [k for k in stats if k.startswith("done_d")]:
            _d = _k[len("done_d"):]
            day_games[_d] = day_games.get(_d, 0.0) + float(stats[_k])
            day_wins[_d] = day_wins.get(_d, 0.0) + float(stats[f"rew_d{_d}"])
        for _name in opp_wins:
            opp_wins[_name] += float(stats[f"rew_{_name}"])
            opp_games[_name] += float(stats[f"done_{_name}"])
            opp_draws[_name] += float(stats[f"draw_{_name}"])
        # Keyed off the cell names the rollout actually produced, so a day rung that the
        # curriculum is not currently serving simply never appears rather than logging a zero
        # that would read as "played it and lost every time".
        for _cell in by_opp_day:
            if not _cell.startswith("done_"):
                continue
            _key = _cell[len("done_"):]
            opp_day_games[_key] = opp_day_games.get(_key, 0.0) + float(stats[_cell])
            opp_day_wins[_key] = opp_day_wins.get(_key, 0.0) + float(stats[f"rew_{_key}"])

        # **Record how this opponent did, or the priority weights never change.**
        #
        # `reward_sum / done_count` is the *live policy's* win rate on cross-play rows this update,
        # so the opponent's is one minus that. `Pool.record` ignores a zero-sample update itself.
        n_done = float(stats["pool_done"])
        if n_done > 0:
            pool.record(opp_idx, 1.0 - float(stats["pool_reward"]) / n_done, n_done)
        ev = float(stats["ev"])
        ev_signal = float(stats["ev_signal"])

        _fin = np.asarray(jax.device_get(traj["done"] & traj["trainable"] & ~traj["trunc"]))
        _em = np.asarray(jax.device_get(traj["end_money"]))
        _bank_final_med = float(np.median(_em[_fin])) if _fin.any() else float("nan")

        row = {
            "update": it,
            "turns": (it + 1) * args.horizon * args.batch,
            "ret_mean": float(stats["ret_mean"]), "ret_std": float(stats["ret_std"]),
            "shape_share": float(stats["shape_share"]),
            "shape_abs_mean": float(stats["shape_abs_mean"]),
            "ret_clipped": float(stats["ret_clipped"]),
            "ret_min": float(stats["ret_min"]), "ret_max": float(stats["ret_max"]),
            "explained_variance": ev,
            "ev_signal": ev_signal,
            "rewarded_frac": float(stats["rewarded_frac"]),
            "n_terminal": float(stats["n_terminal"]),
            "seat_sum": float(stats["seat_sum"]),
            "seat_sum_absdev": float(stats["seat_sum_absdev"]),
            "value_mean": float(stats["value_mean"]),
            "terminal_ret_std": float(stats["terminal_ret_std"]),
            # Value-loss share carried by terminal and near-terminal rows. See where these are
            # computed: `term_leverage` near 1.0 is the case that makes upweighting worth doing.
            "term_loss_share": float(stats["term_loss_share"]),
            "term_row_share": float(stats["term_row_share"]),
            "term_leverage": float(stats["term_leverage"]),
            "near_loss_share": float(stats["near_loss_share"]),
            "near_row_share": float(stats["near_row_share"]),
            "op_counts": [float(x) for x in jax.device_get(stats["op_counts"])],
            "op_counts_full": [float(x) for x in jax.device_get(op_counts_full)],
            "trade_counts": [float(x) for x in stats["trade_counts"]],
            "buy_rate": [float(x) for x in stats["buy_rate"]],
            "sell_rate": [float(x) for x in stats["sell_rate"]],
            "crop_counts": [float(x) for x in stats["crop_counts"]],
            "item_counts": [float(x) for x in stats["item_counts"]],
            "buy_animal_rate": [float(x) for x in stats["buy_animal_rate"]],
            "role_counts": [float(x) for x in stats["role_counts"]],
            **{k: float(stats[k]) for k in ("seed_rate", "hire_rate", "land_rate")},
            # The bank itself, seat 0 = the live policy. The most direct statement of the leak
            # there is: a season that ends on $0 has spent its whole stake and earned nothing.
            "money_med": float(np.median(np.asarray(jax.device_get(state.farm.money))[:, 0])),
            # **Outstanding work on the live policy's own board, logged beside `crew`.**
            #
            # `hire` tripled to 0.331 the moment its prior target was removed, while every farming
            # op collapsed and `bank med` fell to $527 -- so the open question is whether the crew
            # is sized to anything at all. Deliberately logged rather than enforced: a prior that
            # asserted "hire in proportion to work" would be a ratio read off what happens to work,
            # which is the policy-prior `CLAUDE.md` forbids, and it would also make this question
            # permanently unanswerable by construction.
            "param_drift": float(jax.device_get(param_drift)),
            # Median bank of games that actually FINISHED this update, on the live policy's own
            # seat. Against a $3,000 start this reads directly as "did we make money" -- the
            # question `money_med` cannot answer. nan when nothing terminated, which is honest:
            # with day-0 slots synchronised, most updates resolve no full-season game at all.
            "bank_final_med": _bank_final_med,
            "jobs_med": float(np.median(
                np.asarray(jax.device_get(HEUR.outstanding_jobs(state)))[:, 0])),
            "money_max": float(np.asarray(jax.device_get(state.farm.money))[:, 0].max()),
            # **Over the trainable policy's own rows, not every row in the rollout.**
            # `unit_exists` spans both seats of every game, so with `--farm-frac 0.30` this was
            # averaging our crew together with the scripted farmer's `TARGET_HANDS = 10` and
            # reading high. `live_units` is the same mask the op census already uses. Third time
            # this project has computed a rate over rows the policy does not own -- after the
            # `MAX_UNITS` op census and the behaviour-cloning loss.
            "mean_units": float(jax.device_get(
                (live_units.sum(axis=-1).sum()
                 / jnp.maximum(batch_data_full["trainable"].sum(), 1.0)))),
            "trainable_frac": float(jax.device_get(traj["trainable"].mean())),
            "pool": len(pool),
            "win_rate": float(wins / games) if games else float("nan"),
            "episodes": int(games),
            **{f"wr_{k}": (float(opp_wins[k] / opp_games[k]) if opp_games[k] else float("nan"))
               for k in opp_wins},
            **{f"games_{k}": int(opp_games[k]) for k in opp_games},
            **{f"wr_day{d}": (day_wins[d] / day_games[d] if day_games[d] else float("nan"))
               for d in day_games},
            **{f"games_day{d}": int(day_games[d]) for d in day_games},
            **{f"draws_{k}": (float(opp_draws[k] / opp_games[k]) if opp_games[k] else float("nan"))
               for k in opp_draws},
            # Opponent x seed day. Only cells with games are emitted, and each rate ships beside
            # its own count -- a cell at 0.00 over 3 games and one at 0.00 over 300 are different
            # claims and the rate alone cannot tell them apart.
            **{f"wr_{k}": (opp_day_wins[k] / opp_day_games[k]) if opp_day_games[k] else float("nan")
               for k in opp_day_games},
            **{f"games_{k}": int(opp_day_games[k]) for k in opp_day_games},
            # **Turns produced by *this process*, over the time this process has been running.**
            # `(it + 1)` counts from update 0, so on a resume it credited every pre-resume turn
            # against post-resume wall-clock and printed 13,082 t/s on a card doing about 1,100.
            # `turns` above is deliberately left cumulative: it measures the lineage's progress,
            # which is the thing a checkpoint inherits. Rate is a property of the run.
            "sps": float((it + 1 - start_update) * args.horizon * args.batch
                         / (time.time() - t_start)),
            **{k: float(stats[k]) for k in
                 ("loss", "policy_loss", "value_loss", "seat_loss", "entropy", "op_entropy",
                  "approx_kl", "clip_frac", "grad_norm", "kl_prior")},
        }
        with log_path.open("a") as fh:
            fh.write(json.dumps(row) + "\n")

        # Every update gets a line. Printing every tenth saved nothing and produced a five-minute
        # silence that read as a hang -- the one thing this log must never do, given how many
        # genuine silent deaths there have been. An update is ~20s; a line each is cheap.
        sig = "  n/a" if np.isnan(ev_signal) else f"{ev_signal:+.3f}"
        # `V` and `sum` describe whichever net produced the rollout values. Say which, so that an
        # EMA copy carrying half the random initialisation is never again read as the live critic.
        vnet = "t" if args.target_ema else ""
        # **The op mix, because no scalar in this log can tell farming badly from standing still.**
        # `tstd` is the return spread on rows that actually resolved -- the statistic that separates
        # "every game drew" from "the critic collapsed onto one number", which `ret_std` cannot.
        # **The productive ops are always shown, not the top five.**
        #
        # Printing whichever five happened to be largest hid the only thing worth watching: the
        # policy explores all seventeen legal ops, and the failure is not that it never tries to
        # farm but that the *chain* never completes. One update measured 773 plants against 9
        # harvests. A top-five view showed noop and four movement ops and nothing else, which reads
        # as "it only knows how to walk" and is wrong.
        counts = row["op_counts"]
        total_ops = max(1.0, sum(counts))
        # **Both chains, because the animal one is the one being worked on.** This listed only the
        # crop chain, so `feed`, `care`, `place` and `pasture` never appeared -- and "FEED leaving
        # zero" is the committed gate for the whole BC warm-start. The gate was unreadable in the
        # log it is meant to be read from, which is the same class of mistake as a rate computed
        # over `MAX_UNITS`: not wrong arithmetic, just not showing the thing being decided on.
        # Six of the top seven ops by correlation with money are the wheat -> animal -> product
        # pipeline, so the animal chain is if anything the more important half.
        # `fert!` (FERTILIZE) was missing here while `fert+` (COLLECT_FERT) was present, so the
        # census could show the policy *acquiring* fertiliser and never show it *spending* any.
        # It buys FERTILIZER on 19.3% of turns and sells on 24.5% with the teacher at 0.0/17.9%,
        # and whether a single unit of it ever reached a plant was not a question the log could
        # answer. FERTILIZE doubles a watered plant's yield for three days, so the difference
        # between "sound melon play" and "buy-and-resell churn paying the spread" was invisible.
        # Third omission of this shape today, after `carrot` and `home` in the opponent scoreboard.
        chain = ("plant", "water", "harv", "drop", "pick",
                 "place", "feed", "care", "fert+", "fert!", "pasture")
        mix = " ".join(
            f"{n}:{counts[O_NAMES.index(n)] / total_ops:.2%}" for n in chain)
        mix += f"  | noop:{counts[0] / total_ops:.0%}"
        moves = sum(counts[O_NAMES.index(n)] for n in ("N", "S", "E", "W"))
        mix += f" move:{moves / total_ops:.0%} crew:{row['mean_units']:.1f}"
        # **The COMMIT class, aggregated, because it is the pass/fail number for the prior split.**
        # A chosen commit mechanically removes up to four future move draws for that unit, so the
        # signature to watch is commit share rising *while* move share falls in the same window --
        # either alone is ambiguous. Printed per-token too: the class rising because one token is
        # being spammed is a new policy fragment, not the intended effect.
        cm_counts = [counts[len(O_NAMES) + i] for i in range(CM.N_COMMIT)]
        mix += (f"\n         commit {sum(cm_counts) / total_ops:.2%} = "
                + " ".join(f"{n}:{c / total_ops:.2%}"
                           for n, c in zip(COMMIT_O_NAMES, cm_counts)))
        cf = row["op_counts_full"]
        tf = max(1.0, sum(cf))
        if args.early_limit:
            # Only the full-season rows can legally reach a harvest, so their chain is the one
            # worth reading when early-game envs are on.
            mix += ("\n         full-season only  "
                    + " ".join(f"{n}:{cf[O_NAMES.index(n)] / tf:.2%}" for n in chain))
        # **Per-seed-day win rates, in the HUMAN log and not only the JSON.**
        #
        # These have existed in `log.jsonl` for a while and were left there, which made the one
        # number people actually read -- the aggregate `wr` -- a day-25 number wearing a mix's
        # name. It is what hid four dead rungs sitting at 0.50 for 200 updates.
        #
        # Built as a plain string here rather than inline in the `print` below: the previous
        # attempt at this line was written as an f-string plus a conditional expression inside the
        # implicit concatenation, which broke and was reverted rather than fixed.
        day_bits = []
        for d in sorted(cur_mix or {}, reverse=True):
            g = row.get(f"games_day{d}", 0)
            if g:
                day_bits.append(f"d{d}:{row[f'wr_day{d}']:.3f}/{int(g)}x")
            else:
                day_bits.append(f"d{d}: n/a")
        day_line = ("         by seed day  " + "  ".join(day_bits) + "\n") if day_bits else ""

        # **The opponent-by-day grid, which is the only un-confounded win rate in this log.**
        #
        # Printed as a grid and not a flat run of `farm_d0:0.09/121x` tokens because every
        # question asked of it is a comparison -- one opponent across days, or one day across
        # opponents -- and a flat list makes both directions unreadable. A cell with no games
        # prints `--`, never `0.00`: "did not play this" and "played and lost every time" are
        # different claims and the whole point of this block is to stop conflating things.
        grid_line = ""
        _days_desc = sorted(cur_mix or {}, reverse=True)
        _live_opps = [o for o in OPPONENT_NAMES
                      if any(row.get(f"games_{o}_d{d}") for d in _days_desc)]
        if _live_opps:
            def _cell(o, d):
                g = int(row.get(f"games_{o}_d{d}") or 0)
                return f"{row[f'wr_{o}_d{d}']:.2f}/{g}" if g else "--"
            grid_line = (
                "         wr by opponent x seed day  (cumulative, rate/games)\n"
                + f"         {'':>7}" + "".join(f"{'d' + str(d):>12}" for d in _days_desc) + "\n"
                + "\n".join(f"         {o:>7}" + "".join(f"{_cell(o, d):>12}" for d in _days_desc)
                            for o in _live_opps) + "\n")

        # **PICKUP by item name, and only the items actually picked up.**
        #
        # This printed twelve bare decimals over the `ITEMS` index space, so the one question the
        # census exists to answer -- are units picking up WHEAT to FEED with, or picking up the
        # animals they then PLACE -- meant counting commas against a name list kept somewhere
        # else. Zero-share items are dropped rather than shown as 0.00: with twelve slots and two
        # or three ever used, the zeros are the noise and the survivors are the whole signal.
        _picks = row["item_counts"]
        _pick_total = sum(_picks)
        _pick_hits = sorted((i for i, x in enumerate(_picks) if x > 0), key=lambda i: -_picks[i])
        pickup_line = (
            "         pickup "
            + ("  ".join(f"{ITEM_NAMES[i]}:{_picks[i] / _pick_total:.2f}" for i in _pick_hits)
               if _pick_hits else "none")
            + f"  ({_pick_total:,.0f} total)  |  buyanimal "
            + "  ".join(f"{n}:{x:.3f}" for n, x in zip(ANIMAL_NAMES, row["buy_animal_rate"]))
            + "\n")

        # **Market lines with product names and the teacher's rate beside ours.**
        #
        # `buy 0.240/0.000/0.000/0.000/0.000/0.000/0.000/0.000/0.262` is unreadable, and worse, the
        # seven zeros are STRUCTURAL -- only WHEAT and FERTILIZER are in `jax_sim.BUYABLE`, so the
        # policy is masked out of the rest. Printed as a bare list it reads as "the policy refuses
        # to buy seven products" when it cannot buy them at all.
        #
        # **Read the teacher column as a reference point, not a target.** These are the top-25
        # leaderboard seats scraped on day 2 of a 62-day competition; their play is an early-meta
        # artifact and will not be what wins. It is here because "how does this compare to people
        # who are currently beating us" is the question the raw numbers cannot answer, not because
        # matching it is the goal -- `CLAUDE.md` is explicit that a teacher is a sparring partner
        # and never the final policy.
        buyable = [i for i, b in enumerate(np.asarray(J.BUYABLE)) if b]
        def _mkt(rates, teacher, keep):
            return "  ".join(
                f"{PRODUCT_NAMES[i][:5]}:{rates[i]:.3f}(t{teacher[i]:.3f})" for i in keep)
        buy_line = ("         BUY  " + _mkt(row["buy_rate"], TEACHER_BUY, buyable)
                    + "   (only these two are buyable)\n")
        sell_keep = sorted(range(len(PRODUCT_NAMES)),
                           key=lambda i: -max(row["sell_rate"][i], TEACHER_SELL[i]))[:6]
        sell_line = ("         SELL " + _mkt(row["sell_rate"], TEACHER_SELL, sorted(sell_keep))
                     + "\n")

        print(
            f"[{it:5d}] ret {row['ret_mean']:+.4f}+/-{row['ret_std']:.4f} "
            f"tstd {row['terminal_ret_std']:.3f}  "
            f"ev {ev:+.3f} (signal {sig})  ent {row['entropy']:.1f} (op {row['op_entropy']:.2f})  "
            f"clip {row['clip_frac']:.3f}  kl {row['approx_kl']:+.4f}  "
            f"wr {row['win_rate']:.3f}/{int(games)}x  term {int(stats['n_terminal'])}  "
            f"{vnet}V {row['value_mean']:.3f} {vnet}sum {row['seat_sum']:.3f} "
            f"seatL {row['seat_loss']:.4f}  klP {row['kl_prior']:.3f}  "
            f"{row['sps']:,.0f} t/s\n"
            # Terminal rows: what share of the batch they are, what share of the value loss they
            # carry, and the ratio. `lev` near 1 means they pull no harder than a bootstrap row.
            f"         termrows {row['term_row_share']:.4%} vloss {row['term_loss_share']:.2%} "
            f"lev {row['term_leverage']:.1f}x   "
            f"near{NEAR_TERMINAL_TURNS} rows {row['near_row_share']:.2%} "
            f"vloss {row['near_loss_share']:.2%}\n"
            # Shaping, and whether the critic can represent what shaping did to the returns.
            # `CLIP` is printed loudly because a clipped critic reads as a confident one -- `ev`
            # stays high on self-consistent predictions and nothing else in the log would show it.
            + (f"         shape {row['shape_share']:.1%} of |r|  mean {row['shape_abs_mean']:.2e}  "
               f"ret [{row['ret_min']:+.3f}, {row['ret_max']:+.3f}] vs head "
               f"[{-args.value_margin:+.2f}, {1 + args.value_margin:+.2f}]"
               + (f"   ** CLIPPED {row['ret_clipped']:.2%} OF ROWS -- RAISE --value-margin **"
                  if row["ret_clipped"] > 0 else "") + "\n"
               if args.shaping_coef else "")
            # `OPPONENT_NAMES`, not a hand-written tuple. The literal that was here listed
            # (the `+` is load-bearing: the block above ends an implicit-concatenation run.)
            # ("idle", "trade", "farm", "ranch", "pool") and had silently dropped `carrot` since it
            # was added -- a seat can be 20% of the batch and invisible on the scoreboard, which is
            # the same species as the census that could not emit FEED and so could not fail on it.
            + "         vs " + "  ".join(
                f"{k}:{row[f'wr_{k}']:.3f}/{row[f'games_{k}']}x/d{row[f'draws_{k}']:.0%}"
                if row[f"games_{k}"] else f"{k}: n/a"
                for k in OPPONENT_NAMES) + "\n"
            + day_line
            + grid_line
            + f"         ops {mix}\n"
            # `trade` is the coordinating latent for both conditioned market heads, so its spread
            # is the first thing to read: near-uniform is healthy, one mode near 1.00 is the
            # collapse that would make `buy` structurally unreachable rather than merely rare.
            f"         trade {'/'.join(f'{x:.2f}' for x in _norm(row['trade_counts']))}"
            # Crops named for the same reason PICKUP is: five bare decimals against an index
            # order held in another file is not readable, and rotation is the thing being judged.
            + "  crop " + "  ".join(
                f"{PRODUCT_NAMES[i][:5]}:{x:.2f}"
                for i, x in enumerate(_norm(row['crop_counts']))) + "\n"
            + buy_line + sell_line
            # PICKUP is the link between wheat sitting in the shed and a unit able to FEED.
            + pickup_line
            # Realised seat-1 mix. Sticky roles are sampled, so this is measured, not guaranteed.
            + "         roles " + "  ".join(
                f"{n}:{x:.0%}" for n, x in zip(ROLE_NAMES, _norm(row['role_counts'])))
            + f"  |  spend seed:{row['seed_rate']:.3f} hire:{row['hire_rate']:.3f} "
              f"land:{row['land_rate']:.3f}"
            + f"  bank med ${row['money_med']:,.0f} max ${row['money_max']:,.0f}"
            f"  jobs {row['jobs_med']:.0f}  dW {row['param_drift']:.2e}"
            # The outcome number. `bank med` above is cash on hand mid-season; this one is what
            # games actually FINISHED on, which is the only version that answers "did we profit".
            + (f"  END ${row['bank_final_med']:,.0f}"
               if row['bank_final_med'] == row['bank_final_med'] else "  END n/a"),
            flush=True,
        )
        if args.opponent_frac and it and it % args.pool_every == 0:
            # `Pool.add` evicts from the middle, keeping the anchor and the frontier, and carries
            # each member's win-rate record with it. See `kagg/rl/league.py`.
            pool.add(jax.device_get(params))
            print(f"         pool {len(pool)}: {pool.summary()}", flush=True)

        if it % args.ckpt_every == 0:
            save_checkpoint(latest_ckpt, params, opt_state, it, args, best=best_wr)
        # "Best" is win rate against the running self-play population, which is the only score we
        # have mid-run. It is noisy early; treat it as a snapshot to evaluate later, not a ranking.
        if games > 200 and row["win_rate"] > best_wr:
            best_wr = row["win_rate"]
            save_checkpoint(best_ckpt, params, opt_state, it, args, best=best_wr)

        # The stop-everything check, per CLAUDE.md. Only meaningful once episodes have finished:
        # before that every reward is legitimately zero and a zero spread means nothing.
        if games > 50 and row["ret_std"] == 0.0:
            print("\nSTOP: ret_std is 0 with finished episodes -- reward is not reaching the "
                  "algorithm. Do not tune anything until this is understood.", flush=True)
            save_checkpoint(latest_ckpt, params, opt_state, it, args, best=best_wr)
            break

    print(f"\ndone. log at {log_path}")


if __name__ == "__main__":
    # A bare traceback to stderr is not enough here: under systemd, stderr and stdout are the same
    # appended file and a run has already been seen to end with exit code 0 and no explanation.
    # Printing explicitly and re-raising guarantees the reason lands in the log that gets read.
    import traceback
    try:
        main()
    except BaseException as exc:            # BaseException: SystemExit and KeyboardInterrupt too
        print(f"\n=== TERMINATED: {type(exc).__name__}: {exc} ===", flush=True)
        traceback.print_exc()
        raise
    else:
        print("=== main() returned normally ===", flush=True)
