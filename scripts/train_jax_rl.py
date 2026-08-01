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
import json
import pathlib
import pickle
import time

import jax
import jax.numpy as jnp
import numpy as np
import optax

from kagg.rl import jax_act as A, jax_obs, jax_policy as P
from kagg.sim import jax_sim as J

RUN_DIR = pathlib.Path("data/jax_rl_runs")
TURNS_PER_DAY = J.TURNS_PER_DAY
EPISODE_TURNS = 719


def make_rollout(model, batch, horizon, gamma, gae_lambda):
    """Build the jitted rollout: `horizon` turns of self-play, plus GAE.

    `gamma` and `gae_lambda` are pinned to float32. A bare Python float promotes to float64 under
    the x64 flag `jax_sim` sets, and `gamma * next_value` would then drag the whole advantage and
    return computation into float64 -- which this card runs at 1/32 rate. See `jax_policy.DTYPE`.
    """
    gamma = jnp.asarray(gamma, dtype=jnp.float32)
    gae_lambda = jnp.asarray(gae_lambda, dtype=jnp.float32)

    @jax.jit
    def rollout(params, state, key):
        def one_turn(carry, _):
            state, key = carry
            key, sub = jax.random.split(key)

            # Observations are stored, not recomputed: the update needs exactly the inputs the
            # behaviour policy saw, and re-encoding from a later state would silently score the
            # actions against the wrong observation.
            tiles, units, glob = jax_obs.encode(state)
            obs = (A._flat(tiles), A._flat(units), A._flat(glob))
            heads, value = model.apply(params, *obs)
            masks = A.masks_for(state)
            actions, logp, _ent = A.sample(sub, heads, masks)

            sim_actions = A.to_sim_actions(actions, batch)
            nxt = J.step(state, sim_actions)

            # Terminal reward, win 1 / loss 0, paid on the last turn of the episode only.
            done = nxt.step_index > J.LAST_STEP
            money = nxt.farm.money                                   # [B, 2]
            won = (money > money[:, ::-1]).astype(jnp.float32)
            tie = (money == money[:, ::-1]).astype(jnp.float32)
            reward = jnp.where(done, won + 0.5 * tie, 0.0).astype(jnp.float32)   # [B, 2]

            out = dict(
                logp=logp, value=value, reward=A._flat(reward),
                done=jnp.broadcast_to(done, (batch, 2)).reshape(-1),
                actions=actions, masks=masks, obs=obs,
            )
            return (nxt, key), out

        (final_state, key), traj = jax.lax.scan(
            one_turn, (state, key), None, length=horizon)

        # Bootstrap from the value of the state we stopped in.
        _h, last_value, _m = A.forward(params, model, final_state)

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

        ratio = jnp.exp(logp - batch_data["old_logp"])
        adv = batch_data["adv"]
        # Normalising per minibatch is standard and matters here: terminal-only rewards make raw
        # advantages tiny for most of an episode and large at the end.
        adv = (adv - adv.mean()) / (adv.std() + 1e-8)

        unclipped = ratio * adv
        clipped = jnp.clip(ratio, 1 - clip, 1 + clip) * adv
        policy_loss = -jnp.minimum(unclipped, clipped).mean()
        value_loss = jnp.square(value - batch_data["returns"]).mean()
        entropy_loss = -entropy.mean()

        loss = policy_loss + vf_coef * value_loss + ent_coef * entropy_loss
        approx_kl = jnp.mean(batch_data["old_logp"] - logp)
        clip_frac = jnp.mean((jnp.abs(ratio - 1.0) > clip).astype(jnp.float32))
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
    print(f"batch {args.batch} games ({2 * args.batch} seats), horizon {args.horizon} turns")

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

    state = J.reset(args.batch)
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

    rollout = make_rollout(model, args.batch, args.horizon, gamma, args.gae_lambda)
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
    if start_update >= args.updates:
        print(f"NOTHING TO DO: start_update {start_update} >= updates {args.updates}", flush=True)

    for it in range(start_update, args.updates):
        key, sub = jax.random.split(key)
        state, key, traj, advantages, returns = rollout(params, state, sub)

        # An episode that ended restarts, so games keep flowing without a Python-level reset.
        finished = np.asarray(traj["done"]).sum()
        if finished:
            rewards = np.asarray(traj["reward"])[np.asarray(traj["done"])]
            wins += float(rewards.sum())
            games += float(rewards.size)
        if bool(np.asarray(state.step_index) > J.LAST_STEP):
            state = J.reset(args.batch)

        # Re-encode observations once per rollout for the update passes.
        def flatten(x):
            return x.reshape(flat_n, *x.shape[2:])

        batch_data_full = dict(
            old_logp=flatten(traj["logp"]),
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
                    adv=batch_data_full["adv"][chunk],
                    returns=batch_data_full["returns"][chunk],
                    actions={k: v[chunk] for k, v in batch_data_full["actions"].items()},
                    masks={k: v[chunk] for k, v in batch_data_full["masks"].items()},
                    obs=tuple(x[chunk] for x in batch_data_full["obs"]),
                )
                params, opt_state, metrics = update(params, opt_state, mb)

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
        rewarded = np.asarray(traj["reward"]).reshape(-1) != 0
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
            "win_rate": float(wins / games) if games else float("nan"),
            "episodes": int(games),
            "sps": float((it + 1) * args.horizon * args.batch / (time.time() - t_start)),
            **{k: float(v) for k, v in metrics.items()},
        }
        with log_path.open("a") as fh:
            fh.write(json.dumps(row) + "\n")

        if it % 10 == 0 or it < 5:
            sig = "  n/a" if np.isnan(ev_signal) else f"{ev_signal:+.3f}"
            print(
                f"[{it:5d}] ret {row['ret_mean']:+.4f}+/-{row['ret_std']:.4f}  "
                f"ev {ev:+.3f} (signal {sig})  ent {row['entropy']:.1f}  "
                f"clip {row['clip_frac']:.3f}  kl {row['approx_kl']:+.4f}  "
                f"wr {row['win_rate']:.3f}  ep {int(games)}  {row['sps']:,.0f} turns/s",
                flush=True,
            )
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
