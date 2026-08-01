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

from kagg.rl import jax_act as A, jax_heuristic as HEUR, jax_obs, jax_policy as P
from kagg.rl.jax_policy import NEG_INF
from kagg.sim import jax_sim as J
from kagg.sim import ops as O

# TF32 tensor cores for matmuls. Ender runs `--matmul-precision high` by default; JAX's own default
# on this card is the slowest, most precise setting, which buys nothing for a 643k-parameter policy
# whose inputs are already normalised counts.
jax.config.update("jax_default_matmul_precision", "tensorfloat32")

RUN_DIR = pathlib.Path("data/jax_rl_runs")

# Short names for the op census printed each update, in `kagg.sim.ops` code order.
O_NAMES = ("noop", "N", "S", "E", "W", "water", "harv", "plant", "dig", "pick", "drop",
           "place", "feed", "care", "fert+", "fert!", "coop", "pasture")

# The scripted wheat trader. Buy early, hold, sell late -- measured at $3,989 from a $3,000 start
# with zero crew actions, against a price path that rose $25 -> $46 monotonically because the town
# drains wheat all season and wheat's glut curve is `log`, so it never floors.
TRADER_BUY_UNTIL = 12
TRADER_SELL_FROM = 20
TRADER_LOT = 5

# League priority, ported from Ender's `_select_league_opponent`.
POOL_PRIORITY_FLOOR = 0.1
POOL_PRIORITY_TEMP = 1.0
POOL_PRIORITY_ALPHA = 0.2
TURNS_PER_DAY = J.TURNS_PER_DAY
EPISODE_TURNS = 719


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
    return J.reset(batch, seed=seed, phase=phase)


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
ROLE_SELF, ROLE_POOL, ROLE_FARM, ROLE_TRADE, ROLE_IDLE = range(5)
N_ROLES = 5
ROLE_NAMES = ("self", "pool", "farm", "trade", "idle")


def make_rollout(model, batch, horizon, gamma, gae_lambda, n_phases):
    """Build the jitted rollout: `horizon` turns of self-play across all phase groups, plus GAE.

    `gamma` and `gae_lambda` are pinned to float32. A bare Python float promotes to float64 under
    the x64 flag `jax_sim` sets, and `gamma * next_value` would then drag the whole advantage and
    return computation into float64 -- which this card runs at 1/32 rate. See `jax_policy.DTYPE`.
    """
    gamma = jnp.asarray(gamma, dtype=jnp.float32)
    gae_lambda = jnp.asarray(gae_lambda, dtype=jnp.float32)
    per_group = batch // n_phases
    # Even-numbered envs are the early-game ones, matching Ender's split exactly.
    is_early = (jnp.arange(batch) % 2) == 0
    _EARLY_ROWS = jnp.repeat(is_early, 2)         # [B*2], for splitting per-seat statistics

    @functools.partial(jax.jit, static_argnums=())
    def rollout(params, value_params, opp_params, roles, role_logp, virgin,
                early_limit, state, key):
        def one_turn(carry, _):
            state, roles, virgin, key = carry
            key, sub = jax.random.split(key)

            # Seat-1 role, held for the life of the episode. Derived here rather than passed in, so
            # every use below reads the same per-game value the reward will later be attributed to.
            use_opp = roles == ROLE_POOL
            use_farm = roles == ROLE_FARM
            use_trade = roles == ROLE_TRADE
            use_idle = roles == ROLE_IDLE

            # Observations are stored, not recomputed: the update needs exactly the inputs the
            # behaviour policy saw, and re-encoding from a later state would silently score the
            # actions against the wrong observation.
            tiles, units, glob = jax_obs.encode(state)         # [B, P, ...]
            obs = (A._flat(tiles), A._flat(units), A._flat(glob))
            heads, _v_self = model.apply(params, *obs)
            # Values for the bootstrap come from `value_params`, which is either the live params
            # (default) or a slow EMA copy. Actions always come from the live policy.
            _h_t, value = model.apply(value_params, *obs)
            masks = A.masks_for(state)
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
            take_opp = take_opp | take_idle | jnp.broadcast_to(
                (use_trade | use_farm)[:, None] & (seat == 1), (batch, 2)).reshape(-1)

            sim_actions = A.to_sim_actions(actions, batch)

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
                hire=jnp.where(trade_seat, False, sim_actions.hire),
                buy_land=jnp.where(trade_seat, False, sim_actions.buy_land),
            )

            # **The only opponent in the pool that can punish a bad farm.**
            #
            # It banks $23,783 over a season against the trader's $3,368 and the idle seat's
            # $3,000, and it runs natively here rather than through a callback -- see
            # `kagg/rl/jax_heuristic.py`. The idle and trader seats are beatable by a fixed amount,
            # so they are a floor; this one has actual play in it.
            farm_seat = jnp.broadcast_to(use_farm[:, None] & (seat == 1), (batch, 2))
            heur = HEUR.actions(state)
            sim_actions = jax.tree_util.tree_map(
                lambda mine, theirs: jnp.where(
                    farm_seat.reshape(farm_seat.shape + (1,) * (mine.ndim - 2)), theirs, mine),
                sim_actions, heur)
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

            # Restart inside the scan, per group. Resetting only in Python after the rollout lets
            # the simulator keep stepping past turn 719 into a season that does not exist, and
            # those invalid turns would still be trained on. The PRNG key carries across so a new
            # episode does not replay the old one's weed draws.
            # Only the per-game fields are selected. `key` and `unlock_day` are not per game --
            # the PRNG key is a single [2] array for the whole state -- so a blanket tree_map over
            # the State tries to broadcast a [B] mask against it and fails.
            fresh = J.reset(batch)
            restart = just_done | truncate
            pick = lambda new, old: jnp.where(                       # noqa: E731
                restart.reshape((-1,) + (1,) * (old.ndim - 1)), new, old)
            nxt = nxt._replace(
                step_index=pick(fresh.step_index, nxt.step_index),
                tiles=jax.tree_util.tree_map(pick, fresh.tiles, nxt.tiles),
                farm=jax.tree_util.tree_map(pick, fresh.farm, nxt.farm),
                inventory=pick(fresh.inventory, nxt.inventory),
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
                trunc=jnp.broadcast_to(pseudo_trunc[:, None], (batch, 2)).reshape(-1),
                # Rows the frozen opponent chose are not ours to learn from: their log-probs come
                # from different parameters, so including them would make the PPO ratio a ratio of
                # two unrelated policies.
                trainable=~take_opp,
                # Which rows belong to a game the frozen opponent is playing in. Not the same as
                # `~trainable`: that marks the opponent's own seat, while this marks *both* seats
                # of a cross-play game, so the live policy's side of one can be picked out.
                crossplay=jnp.broadcast_to(
                    (use_opp | use_idle | use_trade | use_farm)[:, None],
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
                roles=roles,
            )

            # **Re-draw the role only for games that just ended.** A surviving game keeps the
            # opponent it has been playing all season, which is the entire point of this change.
            key, krole = jax.random.split(key)
            drawn = jax.random.categorical(krole, role_logp, shape=(batch,))
            nxt_roles = jnp.where(restart, drawn, roles)
            # Once a slot restarts it has been reset to turn 0 on an empty board, so from here its
            # episodes are genuine and their terminal rewards count.
            nxt_virgin = virgin & ~restart
            return (nxt, nxt_roles, nxt_virgin, key), out

        (final_state, final_roles, final_virgin, key), traj = jax.lax.scan(
            one_turn, (state, roles, virgin, key), None, length=horizon)

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


def _norm(counts):
    """Counts -> shares. All-zero stays all-zero rather than becoming NaN, because "this head was
    never exercised" is a reading worth seeing rather than a blank."""
    total = float(sum(counts))
    return [c / total for c in counts] if total > 0 else [0.0 for _ in counts]


# The heads that spend money. Shaped toward "do not transact" at init, for the reason argued in
# `hand_prior_heads` -- and deliberately *not* including `sell`, which brings money in, or `trade`,
# whose near-uniform spread is healthy and is the coordinating latent the product heads read.
SPEND_HEADS = ("buy_seed", "buy_animal", "buy_land", "hire")


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
        n_legal = jnp.maximum(m.sum(axis=-1, keepdims=True), 1)
        # log p for the non-noop options, so that noop takes `noop_p` and the rest split the
        # remainder. Written in log space directly rather than as logits to normalise.
        others = jnp.log((1.0 - noop_p) / jnp.maximum(n_legal - 1, 1))
        is_noop = jnp.arange(logits.shape[-1]) == O.NOOP
        out[k] = jnp.where(is_noop, jnp.log(noop_p), others)
    return out


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


def make_update(model, clip, vf_coef, ent_coef, max_grad_norm, optimiser, seat_coef=0.0,
                kl_coef=0.0, prior_params=None, hand_noop_p=0.0, spend_p=0.0):
    """Build the jitted PPO update over one rollout's minibatches."""

    def loss_fn(params, batch_data, reg_coef):
        tiles, units, glob = batch_data["obs"]
        heads, value = model.apply(params, tiles, units, glob)
        logp, entropy = A.evaluate(heads, batch_data["masks"], batch_data["actions"])

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
        # `sell` and `buy_product` carry a trade-mode axis that the masks do not, so the raw heads
        # are `[N, N_PRODUCTS, N_TRADE_MODES, K]` against a `[N, N_PRODUCTS, K]` mask and the
        # broadcast simply fails. More importantly, the distribution the policy actually acted from
        # is the slice its sampled mode selected -- a KL against a marginal over modes would
        # regularise something the policy never sampled from.
        if kl_coef:
            cond = A.condition_on_trade(heads, batch_data["actions"]["trade"])
        if kl_coef and (hand_noop_p or spend_p):
            kl_prior = kl_to_prior(
                cond, hand_prior_heads(cond, batch_data["masks"], hand_noop_p, spend_p),
                batch_data["masks"])
        elif prior_params is not None and kl_coef:
            prior_heads, _pv = model.apply(prior_params, tiles, units, glob)
            prior_cond = A.condition_on_trade(
                jax.lax.stop_gradient(prior_heads), batch_data["actions"]["trade"])
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
        if kl_coef and (hand_noop_p or spend_p or prior_params is not None):
            regulariser = reg_coef * kl_prior
        else:
            regulariser = reg_coef * entropy_loss

        loss = policy_loss + vf_coef * value_loss + regulariser + seat_coef * seat_loss
        approx_kl = ((batch_data["old_logp"] - logp) * w).sum() / w_sum
        clip_frac = ((jnp.abs(ratio - 1.0) > clip).astype(jnp.float32) * w).sum() / w_sum
        return loss, dict(policy_loss=policy_loss, value_loss=value_loss, seat_loss=seat_loss,
                          entropy=entropy.mean(), approx_kl=approx_kl, clip_frac=clip_frac,
                          kl_prior=kl_prior)

    @jax.jit
    def update(params, opt_state, batch_data, reg_coef):
        (loss, aux), grads = jax.value_and_grad(loss_fn, has_aux=True)(
            params, batch_data, reg_coef)
        grads, gnorm = _clip_by_norm(grads, max_grad_norm)
        updates, opt_state = optimiser.update(grads, opt_state, params)
        params = optax.apply_updates(params, updates)
        return params, opt_state, {**aux, "loss": loss, "grad_norm": gnorm}

    @functools.partial(jax.jit, static_argnames=("epochs", "n_chunks", "chunk"))
    def run_epochs(params, opt_state, data, key, epochs, n_chunks, chunk, reg_coef):
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
                params, opt_state, metrics = update(params, opt_state, mb, reg_coef)
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
                         "than any guess. Set --ent-coef 0 when using this: it replaces the "
                         "entropy bonus rather than joining it.")
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
                    help="updates over which --kl-coef decays linearly to zero. 0 keeps it flat.")
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
    ap.add_argument("--trade-frac", type=float, default=0.25,
                    help="fraction of games whose seat 1 only trades wheat: buys early, sells late, "
                         "every unit passing. It banks $3,989 from a $3,000 start using zero crew "
                         "actions, so unlike --idle-frac a do-nothing policy LOSES to it rather "
                         "than drawing. That removes the 0.5 payoff for inaction, which is the "
                         "actual fixed point -- our idle farm is a stable $3,000 forever, where "
                         "Ender's game punished standing still on its own. 0 disables.")
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
    ap.add_argument("--resume", default=None, help="path to a checkpoint .pkl to continue from")
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

    model = P.Policy(d_model=args.d_model, n_heads=args.heads, n_layers=args.layers)
    key = jax.random.PRNGKey(args.seed)
    key, sub = jax.random.split(key)

    if args.batch % args.n_phases:
        raise SystemExit(f"--batch {args.batch} must be divisible by --n-phases {args.n_phases}")
    state = staggered_states(args.batch, args.n_phases, seed=args.seed)
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
            prior_params = jax.device_put(pickle.load(fh)["params"])
        print(f"KL prior loaded from {args.kl_prior} (coef {args.kl_coef}, "
              f"ent_coef {args.ent_coef})", flush=True)

    pool = [jax.device_get(params)]
    # **Opponents are sampled by how well they do against us, not round-robin.**
    #
    # Ender: "prioritised based on recent winrate, with more difficult checkpoints being played
    # more often. This seems especially important for the 4-player game mode." Ours was
    # `pool[it % len(pool)]`, which plays the random initialisation exactly as often as the best
    # checkpoint in the pool -- a lottery rather than a curriculum.
    #
    # `pool_wr[i]` is an EMA of the *opponent's* win rate, so a checkpoint that beats us has a high
    # value and gets picked more. His weights, ported directly:
    #     weight = floor + winrate ** temperature,  plus 0.25 while a member is unplayed
    pool_wr = [0.5]
    pool_games = [0]
    if prior_params is not None:
        pool.append(jax.device_get(prior_params))
        pool_wr.append(0.5)
        pool_games.append(0)

    start_update = 0
    best_wr = -1.0
    if args.resume:
        ck = load_checkpoint(args.resume)
        params, opt_state = ck["params"], ck["opt_state"]
        start_update = ck["update"] + 1
        best_wr = ck.get("best") or -1.0
        print(f"resumed from {args.resume} at update {start_update}")

    latest_ckpt = run / "latest.pkl"
    best_ckpt = run / "best.pkl"
    # Save immediately, so the run is known to be checkpointable before hours are invested in it.
    save_checkpoint(latest_ckpt, params, opt_state, start_update - 1, args)
    print(f"checkpoints: {latest_ckpt} (every {args.ckpt_every} updates) and {best_ckpt}")
    print(f"log:  {log_path}")
    print(f"tail: scripts/deploy_train.sh watch", flush=True)

    rollout = make_rollout(model, args.batch, args.horizon, gamma, args.gae_lambda,
                           args.n_phases)
    update, run_epochs = make_update(model, args.clip, args.vf_coef, args.ent_coef,
                                     args.max_grad_norm, optimiser, seat_coef=args.seat_coef,
                                     kl_coef=args.kl_coef, prior_params=prior_params,
                                     hand_noop_p=args.hand_prior,
                                     spend_p=args.spend_prior)

    # Role probabilities, in `ROLE_NAMES` order. Self-play is the remainder, as it always was, but
    # now explicitly rather than by falling through a partition.
    role_p = np.array([0.0, args.opponent_frac, args.farm_frac,
                       args.trade_frac, args.idle_frac], dtype=np.float64)
    if role_p[1:].sum() > 1.0:
        raise SystemExit(
            f"opponent/farm/trade/idle fracs sum to {role_p[1:].sum():.2f} > 1.0")
    role_p[ROLE_SELF] = 1.0 - role_p[1:].sum()
    print("seat-1 roles, sticky per episode: "
          + "  ".join(f"{n}:{p:.0%}" for n, p in zip(ROLE_NAMES, role_p)))
    role_logp = jnp.log(jnp.asarray(role_p, dtype=jnp.float32) + 1e-12)
    # Initial draw. Games are mid-season at their staggered phases, so this is the only point where
    # a role is assigned to a game that did not just start -- unavoidable, and it washes out within
    # one season as each game terminates and re-draws.
    roles = jax.random.categorical(
        jax.random.PRNGKey(args.seed + 1), role_logp, shape=(args.batch,))
    # Every slot starts mid-season on an empty board, so no slot's *first* termination is a real
    # result. Cleared per slot as soon as it restarts. See where `reward` is computed.
    virgin = jnp.ones((args.batch,), dtype=bool)

    n_seats = 2 * args.batch
    flat_n = args.horizon * n_seats
    wins, games = 0.0, 0.0
    # Cumulative, per opponent type, in the same units as `wins`/`games` above.
    opp_wins = {k: 0.0 for k in ("idle", "trade", "farm", "pool")}
    opp_games = {k: 0.0 for k in ("idle", "trade", "farm", "pool")}
    opp_draws = {k: 0.0 for k in ("idle", "trade", "farm", "pool")}
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
        w = np.array([POOL_PRIORITY_FLOOR + max(wr, 1e-6) ** POOL_PRIORITY_TEMP
                      + (0.25 if g <= 0 else 0.0)
                      for wr, g in zip(pool_wr, pool_games)], dtype=np.float64)
        opp_idx = int(np.random.default_rng((args.seed, it)).choice(
            len(pool), p=w / w.sum()))
        opp_params = pool[opp_idx]

        state, roles, virgin, key, traj, advantages, returns = rollout(
            params, target_params, opp_params, roles, role_logp, virgin,
            jnp.asarray(args.early_limit, dtype=jnp.int32), state, sub)

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
        for _name, _flag in (("idle", "vs_idle"), ("trade", "vs_trade"),
                             ("farm", "vs_farm"), ("pool", "vs_pool")):
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
        )

        # Explained variance, also reduced on device. `ev` over everything is mostly the critic
        # scoring itself on reward-free rows; `ev_signal` restricts to rows where an episode
        # actually ended, which is the only version that can fail.
        ret_d = batch_data_full["returns"]
        val_d = flatten(traj["value"])
        ev_d = 1.0 - (ret_d - val_d).var() / jnp.maximum(ret_d.var(), 1e-8)
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
        op_counts = (jax.nn.one_hot(op_rows, O.N_OPS, dtype=jnp.float32)
                     * live_units[..., None]).sum(axis=(0, 1))

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
        op_counts_full = (jax.nn.one_hot(op_rows, O.N_OPS, dtype=jnp.float32)
                          * full_live[..., None]).sum(axis=(0, 1))

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
        seat_rows = batch_data_full["trainable"].astype(jnp.float32)
        n_seat = jnp.maximum(seat_rows.sum(), 1.0)
        trade_counts = (jax.nn.one_hot(batch_data_full["actions"]["trade"],
                                       P.N_TRADE_MODES, dtype=jnp.float32)
                        * seat_rows[:, None]).sum(axis=0)
        # Bucket 0 of `BUY_BUCKETS`/`SELL_BUCKETS` is quantity zero, so "> 0" is "actually traded".
        buy_rate = ((batch_data_full["actions"]["buy_product"] > 0).astype(jnp.float32)
                    * seat_rows[:, None]).sum(axis=0) / n_seat
        sell_rate = ((batch_data_full["actions"]["sell"] > 0).astype(jnp.float32)
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
        buy_animal_rate = ((batch_data_full["actions"]["buy_animal"] > 0).astype(jnp.float32)
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
        # three -- bucket 0 of `BUY_BUCKETS` is quantity zero.
        def _spend(name):
            a = batch_data_full["actions"][name]
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
        reg_coef = args.ent_coef
        if args.kl_anneal:
            reg_coef *= max(0.0, 1.0 - it / float(args.kl_anneal))

        n_chunks = max(1, flat_n // args.minibatch_size)
        key, ekey = jax.random.split(key)
        params, opt_state, metrics = run_epochs(
            params, opt_state, batch_data_full, ekey,
            epochs=args.epochs, n_chunks=n_chunks, chunk=args.minibatch_size,
            reg_coef=reg_coef)
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
            "terminal_ret_std": terminal_ret_std, "op_counts": op_counts,
            "trade_counts": trade_counts, "buy_rate": buy_rate,
            "sell_rate": sell_rate, "crop_counts": crop_counts,
            "item_counts": item_counts,
            "buy_animal_rate": buy_animal_rate,
            "role_counts": role_counts,
            "seed_rate": seed_rate, "hire_rate": hire_rate, "land_rate": land_rate,
            **by_opp,
            **{k: v for k, v in metrics.items()},
        })
        wins += float(stats["reward_sum"])
        games += float(stats["done_count"])
        for _name in opp_wins:
            opp_wins[_name] += float(stats[f"rew_{_name}"])
            opp_games[_name] += float(stats[f"done_{_name}"])
            opp_draws[_name] += float(stats[f"draw_{_name}"])

        # **Record how this opponent did, or the priority weights never change.**
        #
        # `reward_sum / done_count` is the *live policy's* win rate on cross-play rows this update,
        # so the opponent's is one minus that. Only updated when this update actually finished games
        # against it -- terminal rows are ~0.14% of rows, so an update can legitimately see none,
        # and folding a zero-sample estimate into the EMA would drag every member toward 0.5 and
        # flatten the curriculum back into the round-robin this replaces.
        n_done = float(stats["pool_done"])
        if n_done > 0:
            opp_wr = 1.0 - float(stats["pool_reward"]) / n_done
            a = POOL_PRIORITY_ALPHA
            pool_wr[opp_idx] = (1 - a) * pool_wr[opp_idx] + a * opp_wr
            pool_games[opp_idx] += int(n_done)
        ev = float(stats["ev"])
        ev_signal = float(stats["ev_signal"])

        row = {
            "update": it,
            "turns": (it + 1) * args.horizon * args.batch,
            "ret_mean": float(stats["ret_mean"]), "ret_std": float(stats["ret_std"]),
            "explained_variance": ev,
            "ev_signal": ev_signal,
            "rewarded_frac": float(stats["rewarded_frac"]),
            "n_terminal": float(stats["n_terminal"]),
            "seat_sum": float(stats["seat_sum"]),
            "seat_sum_absdev": float(stats["seat_sum_absdev"]),
            "value_mean": float(stats["value_mean"]),
            "terminal_ret_std": float(stats["terminal_ret_std"]),
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
            **{f"draws_{k}": (float(opp_draws[k] / opp_games[k]) if opp_games[k] else float("nan"))
               for k in opp_draws},
            # **Turns produced by *this process*, over the time this process has been running.**
            # `(it + 1)` counts from update 0, so on a resume it credited every pre-resume turn
            # against post-resume wall-clock and printed 13,082 t/s on a card doing about 1,100.
            # `turns` above is deliberately left cumulative: it measures the lineage's progress,
            # which is the thing a checkpoint inherits. Rate is a property of the run.
            "sps": float((it + 1 - start_update) * args.horizon * args.batch
                         / (time.time() - t_start)),
            **{k: float(stats[k]) for k in
                 ("loss", "policy_loss", "value_loss", "seat_loss", "entropy",
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
        chain = ("plant", "water", "harv", "drop", "pick")
        mix = " ".join(
            f"{n}:{counts[O_NAMES.index(n)] / total_ops:.2%}" for n in chain)
        mix += f"  | noop:{counts[0] / total_ops:.0%}"
        moves = sum(counts[O_NAMES.index(n)] for n in ("N", "S", "E", "W"))
        mix += f" move:{moves / total_ops:.0%} crew:{row['mean_units']:.1f}"
        cf = row["op_counts_full"]
        tf = max(1.0, sum(cf))
        if args.early_limit:
            # Only the full-season rows can legally reach a harvest, so their chain is the one
            # worth reading when early-game envs are on.
            mix += ("\n         full-season only  "
                    + " ".join(f"{n}:{cf[O_NAMES.index(n)] / tf:.2%}" for n in chain))
        print(
            f"[{it:5d}] ret {row['ret_mean']:+.4f}+/-{row['ret_std']:.4f} "
            f"tstd {row['terminal_ret_std']:.3f}  "
            f"ev {ev:+.3f} (signal {sig})  ent {row['entropy']:.1f}  "
            f"clip {row['clip_frac']:.3f}  kl {row['approx_kl']:+.4f}  "
            f"wr {row['win_rate']:.3f}/{int(games)}x  term {int(stats['n_terminal'])}  "
            f"{vnet}V {row['value_mean']:.3f} {vnet}sum {row['seat_sum']:.3f} "
            f"seatL {row['seat_loss']:.4f}  klP {row['kl_prior']:.3f}  "
            f"{row['sps']:,.0f} t/s\n"
            f"         vs " + "  ".join(
                f"{k}:{row[f'wr_{k}']:.3f}/{row[f'games_{k}']}x/d{row[f'draws_{k}']:.0%}"
                if row[f"games_{k}"] else f"{k}: n/a"
                for k in ("idle", "trade", "farm", "pool")) + "\n"
            f"         ops {mix}\n"
            # `trade` is the coordinating latent for both conditioned market heads, so its spread
            # is the first thing to read: near-uniform is healthy, one mode near 1.00 is the
            # collapse that would make `buy` structurally unreachable rather than merely rare.
            f"         trade {'/'.join(f'{x:.2f}' for x in _norm(row['trade_counts']))}"
            f"  buy {'/'.join(f'{x:.3f}' for x in row['buy_rate'])}"
            f"  sell {'/'.join(f'{x:.3f}' for x in row['sell_rate'])}"
            f"  crop {'/'.join(f'{x:.2f}' for x in _norm(row['crop_counts']))}\n"
            # PICKUP is the link between wheat sitting in the shed and a unit able to FEED.
            f"         pickup {'/'.join(f'{x:.2f}' for x in _norm(row['item_counts']))}"
            f"  buyanimal {'/'.join(f'{x:.4f}' for x in row['buy_animal_rate'])}\n"
            # Realised seat-1 mix. Sticky roles are sampled, so this is measured, not guaranteed.
            f"         roles " + "  ".join(
                f"{n}:{x:.0%}" for n, x in zip(ROLE_NAMES, _norm(row['role_counts'])))
            + f"  |  spend seed:{row['seed_rate']:.3f} hire:{row['hire_rate']:.3f} "
              f"land:{row['land_rate']:.3f}"
            + f"  bank med ${row['money_med']:,.0f} max ${row['money_max']:,.0f}",
            flush=True,
        )
        if args.opponent_frac and it and it % args.pool_every == 0:
            pool.append(jax.device_get(params))
            pool_wr.append(0.5)
            pool_games.append(0)
            if len(pool) > args.pool_size:
                # Drop from the *middle*, never the ends. Evicting the oldest would leave a pool of
                # near-identical recent snapshots -- which is how self-play starts cycling: the
                # policy forgets strategies it used to beat, rediscovers a counter to its recent
                # self, loses to something from ten thousand updates ago, and every local win rate
                # looks healthy throughout. Keeping the first entry preserves an anchor that cannot
                # drift, and keeping the newest preserves the frontier.
                pool.pop(len(pool) // 2)

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
