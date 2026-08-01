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

from kagg.rl import jax_act as A, jax_obs, jax_policy as P
from kagg.sim import jax_sim as J

RUN_DIR = pathlib.Path("data/jax_rl_runs")
TURNS_PER_DAY = J.TURNS_PER_DAY
EPISODE_TURNS = 719


def staggered_states(batch, n_phases, seed=0):
    """`n_phases` independent sim states, started at evenly spread points in the season.

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
    per_group = batch // n_phases
    states = []
    for k in range(n_phases):
        phase = (k * (EPISODE_TURNS + 1)) // n_phases
        s = J.reset(per_group, seed=seed + k)
        states.append(s._replace(step_index=jnp.asarray(phase, dtype=J._I)))
    return jax.tree_util.tree_map(lambda *xs: jnp.stack(xs), *states)


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


def make_rollout(model, batch, horizon, gamma, gae_lambda, n_phases):
    """Build the jitted rollout: `horizon` turns of self-play across all phase groups, plus GAE.

    `gamma` and `gae_lambda` are pinned to float32. A bare Python float promotes to float64 under
    the x64 flag `jax_sim` sets, and `gamma * next_value` would then drag the whole advantage and
    return computation into float64 -- which this card runs at 1/32 rate. See `jax_policy.DTYPE`.
    """
    gamma = jnp.asarray(gamma, dtype=jnp.float32)
    gae_lambda = jnp.asarray(gae_lambda, dtype=jnp.float32)
    per_group = batch // n_phases

    # One vmapped call covers every phase group, so staggering costs no extra wall-clock: the
    # groups differ only in their scalar `step_index`, which vmap maps over.
    v_encode = jax.vmap(jax_obs.encode)
    v_masks = jax.vmap(A.masks_for)
    v_step = jax.vmap(J.step)

    @functools.partial(jax.jit, static_argnums=())
    def rollout(params, value_params, opp_params, use_opp, state, key):
        def one_turn(carry, _):
            state, key = carry
            key, sub = jax.random.split(key)

            # Observations are stored, not recomputed: the update needs exactly the inputs the
            # behaviour policy saw, and re-encoding from a later state would silently score the
            # actions against the wrong observation.
            tiles, units, glob = v_encode(state)              # [K, b, P, ...]
            obs = (_pack(tiles), _pack(units), _pack(glob))
            heads, _v_self = model.apply(params, *obs)
            # Values for the bootstrap come from `value_params`, which is either the live params
            # (default) or a slow EMA copy. Actions always come from the live policy.
            _h_t, value = model.apply(value_params, *obs)
            masks = jax.tree_util.tree_map(_pack_flat, v_masks(state))
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
            seat = jnp.arange(2)[None, None, :]
            take_opp = (use_opp[:, None, None] & (seat == 1))
            take_opp = jnp.broadcast_to(take_opp, (n_phases, per_group, 2)).reshape(-1)
            actions = jax.tree_util.tree_map(
                lambda mine, theirs: jnp.where(
                    take_opp.reshape((-1,) + (1,) * (mine.ndim - 1)), theirs, mine),
                actions, opp_actions)

            # Back to [K, b*P, ...] for the simulator, which knows nothing about the phase axis.
            # `to_sim_actions` expects the seat axis already folded in, matching `masks_for`.
            grouped = jax.tree_util.tree_map(
                lambda a: a.reshape(n_phases, per_group * 2, *a.shape[1:]), actions)
            sim_actions = jax.vmap(A.to_sim_actions, in_axes=(0, None))(grouped, per_group)
            nxt = v_step(state, sim_actions)

            # `just_done` is [K]: each phase group crosses its own episode boundary on its own
            # turn, which is the whole point of staggering. Paid on the transition, never on the
            # level -- `step_index > LAST_STEP` stays true afterwards, so testing it directly would
            # pay the terminal reward on every remaining turn of the rollout.
            was_over = state.step_index > J.LAST_STEP                 # [K]
            now_over = nxt.step_index > J.LAST_STEP
            just_done = now_over & ~was_over

            money = nxt.farm.money                                    # [K, b, 2]
            won = (money > money[..., ::-1]).astype(jnp.float32)
            tie = (money == money[..., ::-1]).astype(jnp.float32)
            reward = jnp.where(
                just_done[:, None, None], won + 0.5 * tie, 0.0).astype(jnp.float32)

            # Restart inside the scan, per group. Resetting only in Python after the rollout lets
            # the simulator keep stepping past turn 719 into a season that does not exist, and
            # those invalid turns would still be trained on. The PRNG key carries across so a new
            # episode does not replay the old one's weed draws.
            fresh = J.reset(per_group)
            nxt = jax.tree_util.tree_map(
                lambda new, old: jnp.where(
                    just_done.reshape((-1,) + (1,) * (old.ndim - 1)), new, old),
                jax.tree_util.tree_map(
                    lambda x: jnp.broadcast_to(x, (n_phases, *x.shape)), fresh)._replace(
                        key=nxt.key),
                nxt,
            )

            done_flat = jnp.broadcast_to(
                just_done[:, None, None], (n_phases, per_group, 2)).reshape(-1)
            out = dict(
                logp=logp, value=value, reward=reward.reshape(-1),
                done=done_flat, actions=actions, masks=masks, obs=obs,
                # Rows the frozen opponent chose are not ours to learn from: their log-probs come
                # from different parameters, so including them would make the PPO ratio a ratio of
                # two unrelated policies.
                trainable=~take_opp,
            )
            return (nxt, key), out

        (final_state, key), traj = jax.lax.scan(
            one_turn, (state, key), None, length=horizon)

        # Bootstrap from the value of the state we stopped in, across all phase groups.
        t, u, g = v_encode(final_state)
        _h, last_value = model.apply(value_params, _pack(t), _pack(u), _pack(g))

        def gae(carry, x):
            adv, next_value = carry
            reward, value, done = x["reward"], x["value"], x["done"]
            # A finished episode has no successor, so the bootstrap is cut there.
            next_value = jnp.where(done, 0.0, next_value)
            adv = jnp.where(done, 0.0, adv)
            delta = reward + gamma * next_value - value
            adv = delta + gamma * gae_lambda * adv
            return (adv, value), adv

        _carry, advantages = jax.lax.scan(
            gae, (jnp.zeros_like(last_value), last_value),
            {k: traj[k] for k in ("reward", "value", "done")},
            reverse=True,
        )
        returns = advantages + traj["value"]
        return final_state, key, traj, advantages, returns

    return rollout


def make_update(model, clip, vf_coef, ent_coef, max_grad_norm, optimiser):
    """Build the jitted PPO update over one rollout's minibatches."""

    def loss_fn(params, batch_data):
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

        loss = policy_loss + vf_coef * value_loss + ent_coef * entropy_loss
        approx_kl = ((batch_data["old_logp"] - logp) * w).sum() / w_sum
        clip_frac = ((jnp.abs(ratio - 1.0) > clip).astype(jnp.float32) * w).sum() / w_sum
        return loss, dict(policy_loss=policy_loss, value_loss=value_loss,
                          entropy=entropy.mean(), approx_kl=approx_kl, clip_frac=clip_frac)

    @jax.jit
    def update(params, opt_state, batch_data):
        (loss, aux), grads = jax.value_and_grad(loss_fn, has_aux=True)(params, batch_data)
        grads, gnorm = _clip_by_norm(grads, max_grad_norm)
        updates, opt_state = optimiser.update(grads, opt_state, params)
        params = optax.apply_updates(params, updates)
        return params, opt_state, {**aux, "loss": loss, "grad_norm": gnorm}

    return update


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
    ap.add_argument("--ent-coef", type=float, default=0.003,
                    help="0.02 was far too high for a large factored space in Orbit Wars; start "
                         "low and raise only if entropy collapses")
    ap.add_argument("--max-grad-norm", type=float, default=0.5)
    ap.add_argument("--d-model", type=int, default=128)
    ap.add_argument("--layers", type=int, default=3)
    ap.add_argument("--heads", type=int, default=4)
    ap.add_argument("--opponent-frac", type=float, default=0.25,
                    help="fraction of phase groups whose seat 1 is played by a frozen past self. "
                         "Pure self-play shares parameters between both seats, so a mutual draw is "
                         "a stable outcome nothing pushes against; a frozen opponent does not "
                         "co-operate in standing still. 0 disables.")
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
    act_gib = (
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
    tiles, units, glob = jax.vmap(jax_obs.encode)(state)
    params = model.init(sub, _pack(tiles), _pack(units), _pack(glob))
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
    pool = [jax.device_get(params)]

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
    update = make_update(model, args.clip, args.vf_coef, args.ent_coef,
                         args.max_grad_norm, optimiser)

    n_seats = 2 * args.batch
    flat_n = args.horizon * n_seats
    wins, games = 0.0, 0.0
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
        # Which phase groups face a frozen opponent this update. Rotating the choice means every
        # group spends most of its time in self-play and some of it under cross-play, rather than
        # permanently splitting the batch into two populations that never meet.
        n_opp = int(round(args.opponent_frac * args.n_phases))
        use_opp = np.zeros(args.n_phases, dtype=bool)
        if n_opp:
            use_opp[[(it * n_opp + j) % args.n_phases for j in range(n_opp)]] = True
        opp_params = pool[it % len(pool)]

        state, key, traj, advantages, returns = rollout(
            params, target_params, opp_params, jnp.asarray(use_opp), state, sub)

        # Episodes restart inside the scan now, so there is no Python-level reset here. Doing both
        # would reset a second time one turn into the new episode and silently discard it.
        finished = np.asarray(traj["done"]).sum()
        if finished:
            rewards = np.asarray(traj["reward"])[np.asarray(traj["done"])]
            wins += float(rewards.sum())
            games += float(rewards.size)

        # Re-encode observations once per rollout for the update passes.
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

        idx = np.arange(flat_n)
        n_chunks = max(1, flat_n // args.minibatch_size)
        metrics = None
        for _ in range(args.epochs):
            np.random.shuffle(idx)
            for chunk in np.array_split(idx, n_chunks):
                chunk = jnp.asarray(chunk)
                mb = dict(
                    old_logp=batch_data_full["old_logp"][chunk],
                    old_value=batch_data_full["old_value"][chunk],
                    trainable=batch_data_full["trainable"][chunk],
                    adv=batch_data_full["adv"][chunk],
                    returns=batch_data_full["returns"][chunk],
                    actions={k: v[chunk] for k, v in batch_data_full["actions"].items()},
                    masks={k: v[chunk] for k, v in batch_data_full["masks"].items()},
                    obs=tuple(x[chunk] for x in batch_data_full["obs"]),
                )
                params, opt_state, metrics = update(params, opt_state, mb)
                target_params = ema_update(target_params, params, args.target_ema)

        ret = np.asarray(batch_data_full["returns"])
        val = np.asarray(traj["value"]).reshape(-1)
        var = ret.var()
        ev = float(1.0 - (ret - val).var() / var) if var > 1e-8 else float("nan")

        # **Explained variance is a lie until a terminal reward lands inside the window.**
        # Episodes are 719 turns and a rollout is `horizon` turns, so most rollouts contain no
        # reward at all. With every reward zero, the return is pure value bootstrap and the
        # advantage is derived from the same value function, so EV measures the critic against
        # itself and comes out near 1.0 on an untrained network. `CLAUDE.md` makes EV > 0.5 a
        # committed kill criterion for this exact frame, so an EV that cannot fail is worse than
        # no EV: it would retire the kill criterion by accident. `ev_signal` is the honest number
        # -- EV restricted to rollouts that actually contained a terminal reward -- and `nan` there
        # means "not yet measurable", not "passing".
        # Select on `done`, not on `reward != 0`. A loss scores 0, so filtering by nonzero reward
        # keeps only the winners -- every selected return is then 1.0, the variance is 0, and EV
        # comes out NaN. That made the one honest kill-criterion metric permanently unmeasurable.
        rewarded = np.asarray(traj["done"]).reshape(-1)
        if rewarded.any():
            r_ret, r_val = ret[rewarded], val[rewarded]
            r_var = r_ret.var()
            ev_signal = float(1.0 - (r_ret - r_val).var() / r_var) if r_var > 1e-8 else float("nan")
        else:
            ev_signal = float("nan")

        row = {
            "update": it,
            "turns": (it + 1) * args.horizon * args.batch,
            "ret_mean": float(ret.mean()), "ret_std": float(ret.std()),
            "explained_variance": ev,
            "ev_signal": ev_signal,
            "rewarded_frac": float(rewarded.mean()),
            "trainable_frac": float(np.asarray(traj["trainable"]).mean()),
            "pool": len(pool),
            "win_rate": float(wins / games) if games else float("nan"),
            "episodes": int(games),
            "sps": float((it + 1) * args.horizon * args.batch / (time.time() - t_start)),
            **{k: float(v) for k, v in metrics.items()},
        }
        with log_path.open("a") as fh:
            fh.write(json.dumps(row) + "\n")

        # Print every update. Printing every tenth saves nothing and produced a five-minute silence
        # that read as a hang -- which, given how many genuine silent deaths this run has had, is
        # the one thing the log must never do. An update is ~20s; a line each is cheap.
        if True:
            sig = "  n/a" if np.isnan(ev_signal) else f"{ev_signal:+.3f}"
            print(
                f"[{it:5d}] ret {row['ret_mean']:+.4f}+/-{row['ret_std']:.4f}  "
                f"ev {ev:+.3f} (signal {sig})  ent {row['entropy']:.1f}  "
                f"clip {row['clip_frac']:.3f}  kl {row['approx_kl']:+.4f}  "
                f"wr {row['win_rate']:.3f}  ep {int(games)}  {row['sps']:,.0f} turns/s",
                flush=True,
            )
        if args.opponent_frac and it and it % args.pool_every == 0:
            pool.append(jax.device_get(params))
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
