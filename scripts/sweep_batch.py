"""Find the batch size that actually feeds the GPU.

At batch 128 the card sat at 14-75% and delivered ~400 turns/s, which puts a 1B-step run -- the
scale the 8th-place finisher used on this same GPU -- at about a month. The simulator alone does
44,700 steps/s, so the policy is not the wall; the batch is simply too small to keep the device
busy. This measures where that stops being true.

Reports **marginal** rate, not cumulative: the first update carries the whole XLA compile, and
averaging it in understates steady-state throughput by 3-5x. That mistake is already recorded in
`docs/experiment_log.md` from the sim benchmark, where an idle-board measurement produced "1,032x".
"""

import argparse
import time

import jax
import jax.numpy as jnp
import numpy as np
import optax

from kagg.rl import jax_act as A, jax_obs, jax_policy as P
from kagg.sim import jax_sim as J

import importlib.util
import pathlib

_spec = importlib.util.spec_from_file_location(
    "train_jax_rl", pathlib.Path(__file__).parent / "train_jax_rl.py")
_train = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_train)


def measure(batch, horizon, minibatch, d_model, layers, heads, updates=4):
    model = P.Policy(d_model=d_model, n_heads=heads, n_layers=layers)
    key = jax.random.PRNGKey(0)
    state = J.reset(batch)
    tiles, units, glob = jax_obs.encode(state)
    params = model.init(key, A._flat(tiles), A._flat(units), A._flat(glob))

    optimiser = optax.adam(3e-4)
    opt_state = optimiser.init(params)
    rollout = _train.make_rollout(model, batch, horizon, 0.998732, 0.95)
    update = _train.make_update(model, 0.2, 0.5, 0.003, 0.5, optimiser)

    flat_n = horizon * 2 * batch
    n_chunks = max(1, flat_n // minibatch)
    marginal = []

    for it in range(updates):
        t0 = time.perf_counter()
        key, sub = jax.random.split(key)
        state, key, traj, advantages, returns = rollout(params, state, sub)

        def flatten(x):
            return x.reshape(flat_n, *x.shape[2:])

        data = dict(
            old_logp=flatten(traj["logp"]), adv=flatten(advantages),
            returns=flatten(returns),
            actions={k: flatten(v) for k, v in traj["actions"].items()},
            masks={k: flatten(v) for k, v in traj["masks"].items()},
            obs=tuple(flatten(x) for x in traj["obs"]),
        )
        idx = np.arange(flat_n)
        np.random.shuffle(idx)
        for chunk in np.array_split(idx, n_chunks):
            chunk = jnp.asarray(chunk)
            mb = dict(
                old_logp=data["old_logp"][chunk], adv=data["adv"][chunk],
                returns=data["returns"][chunk],
                actions={k: v[chunk] for k, v in data["actions"].items()},
                masks={k: v[chunk] for k, v in data["masks"].items()},
                obs=tuple(x[chunk] for x in data["obs"]),
            )
            params, opt_state, metrics = update(params, opt_state, mb)
        jax.block_until_ready(params)
        marginal.append(time.perf_counter() - t0)

    # Drop the first: it is compilation, not throughput.
    steady = float(np.median(marginal[1:])) if len(marginal) > 1 else marginal[0]
    turns = horizon * batch
    return turns / steady, marginal[0], steady


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--horizon", type=int, default=64)
    ap.add_argument("--minibatch-size", type=int, default=256)
    ap.add_argument("--d-model", type=int, default=128)
    ap.add_argument("--layers", type=int, default=3)
    ap.add_argument("--heads", type=int, default=4)
    ap.add_argument("--batches", type=int, nargs="+", default=[128, 256, 512, 1024])
    args = ap.parse_args()

    print(f"devices: {jax.devices()}")
    print(f"horizon {args.horizon}, minibatch {args.minibatch_size}, "
          f"d_model {args.d_model}, layers {args.layers}\n")
    print(f"{'batch':>6} {'compile s':>10} {'steady s':>9} {'turns/s':>10} "
          f"{'days for 1B':>12}")
    for batch in args.batches:
        try:
            rate, compile_s, steady = measure(
                batch, args.horizon, args.minibatch_size,
                args.d_model, args.layers, args.heads)
            days = 1e9 / rate / 86400
            print(f"{batch:>6} {compile_s:>10.1f} {steady:>9.2f} {rate:>10,.0f} {days:>12.1f}")
        except Exception as exc:                                  # OOM is the expected failure
            print(f"{batch:>6}   FAILED: {type(exc).__name__}: {str(exc)[:60]}")


if __name__ == "__main__":
    main()
