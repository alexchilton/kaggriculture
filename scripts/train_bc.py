"""Behaviour cloning on the winners' replays.

**Why this exists.** Per-turn PPO from scratch converges to doing nothing, and the op census makes
the reason plain rather than mysterious: with terminal-only reward a draw pays 0.5 and acting
incompetently pays 0, so a policy that has not discovered farming is *correct* to stand still. It
settles at 95% NOOP within four updates and every game then draws at $3,000. That is a rational
local optimum, not a bug, and no amount of entropy or opponent tuning moves it -- `ent_coef` was
already raised 6.7x for no measurable effect.

Supervised learning does not have to discover anything. The teachers here banked $118k-$128k; our
best heuristic banks $51k and the RL policy ends on $7.

The checkpoint this writes is meant to be used **twice**:

1. as the **initialisation** for PPO, so training starts inside the economy rather than outside it;
2. as the **prior** for a KL penalty, replacing the entropy bonus.

The second is Ender's fix from the Orbit Wars write-ups and it is the one that matters. An entropy
bonus pulls the policy toward *uniform*, which is the wrong target in either direction -- he had
runaway action and biased his prior toward halting; we have runaway inaction and want the opposite.
Regularising toward a *sensible* prior is the general form, and a cloned $120k agent is a far better
prior than anything hand-written. It is also a soft penalty rather than a mask, so it does not
become the quality-masking anti-pattern `CLAUDE.md` records as an Orbit Wars failure.

Run:  .venv/bin/python -u scripts/train_bc.py --epochs 4 2>&1 | tee data/logs/train_bc.log
"""

import argparse
import pickle
import time
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np
import optax

from kagg.rl import jax_policy as P

DATA = Path("data/il")
OUT = Path("data/bc")

# The heads a turn actually decides. `op` dominates the loss by count -- 24 unit slots against one
# scalar for `hire` -- so each head is averaged separately and then weighted, rather than summing
# raw per-element losses and letting slot count decide importance.
HEAD_WEIGHTS = {
    "op": 1.0, "crop": 0.3, "item": 0.3, "qty": 0.2,
    "sell": 0.5, "buy_product": 0.5, "buy_seed": 0.5, "buy_animal": 0.3,
    "hire": 0.3, "buy_land": 0.2,
}


def load(limit_shards=None):
    shards = sorted(DATA.glob("shard_*.npz"))
    if limit_shards:
        shards = shards[:limit_shards]
    if not shards:
        raise SystemExit(f"no shards in {DATA}; run scripts/build_il_dataset.py first")

    tiles, units, glob, labels = [], [], [], {}
    for s in shards:
        z = np.load(s)
        tiles.append(z["tiles"])
        units.append(z["units"])
        glob.append(z["glob"])
        for k in z.files:
            if k.startswith("y_"):
                labels.setdefault(k[2:], []).append(z[k])
    return (np.concatenate(tiles), np.concatenate(units), np.concatenate(glob),
            {k: np.concatenate(v) for k, v in labels.items()})


def cross_entropy(logits, target):
    """Mean cross-entropy over whatever leading axes the head has."""
    logp = jax.nn.log_softmax(logits, axis=-1)
    picked = jnp.take_along_axis(logp, target[..., None].astype(jnp.int32), axis=-1)[..., 0]
    return -picked.mean()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=4)
    ap.add_argument("--batch", type=int, default=256)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--shards", type=int, default=None)
    ap.add_argument("--holdout", type=float, default=0.05)
    args = ap.parse_args()

    tiles, units, glob, labels = load(args.shards)
    n = len(tiles)
    print(f"{n:,} rows  tiles{tiles.shape[1:]} units{units.shape[1:]} glob{glob.shape[1:]}")

    # Held out by *index block* rather than at random: consecutive rows are consecutive turns of the
    # same game, so a random split leaks a turn's near-duplicate neighbours into validation and the
    # score comes back flattering.
    n_val = int(n * args.holdout)
    idx_val = np.arange(n - n_val, n)
    idx_tr = np.arange(0, n - n_val)
    print(f"train {len(idx_tr):,}  val {len(idx_val):,} (held out as a trailing block, not at random)")

    model = P.Policy()
    key = jax.random.PRNGKey(0)
    params = model.init(key, jnp.asarray(tiles[:2], jnp.float32),
                        jnp.asarray(units[:2], jnp.float32),
                        jnp.asarray(glob[:2], jnp.float32))
    n_params = sum(x.size for x in jax.tree_util.tree_leaves(params))
    print(f"{n_params:,} parameters")

    opt = optax.chain(optax.clip_by_global_norm(1.0), optax.adamw(args.lr))
    opt_state = opt.init(params)

    def loss_fn(params, batch):
        heads, _value = model.apply(params, batch["tiles"], batch["units"], batch["glob"])
        total, parts = 0.0, {}
        for k, w in HEAD_WEIGHTS.items():
            if k not in heads:
                continue
            ce = cross_entropy(heads[k], batch[f"y_{k}"])
            parts[k] = ce
            total = total + w * ce
        return total, parts

    @jax.jit
    def step(params, opt_state, batch):
        (loss, parts), grads = jax.value_and_grad(loss_fn, has_aux=True)(params, batch)
        updates, opt_state = opt.update(grads, opt_state, params)
        return optax.apply_updates(params, updates), opt_state, loss, parts

    @jax.jit
    def op_accuracy(params, batch):
        """Top-1 on the op head -- the only number that says whether it learned to *act*."""
        heads, _ = model.apply(params, batch["tiles"], batch["units"], batch["glob"])
        pred = heads["op"].argmax(axis=-1)
        return (pred == batch["y_op"]).mean(), (pred != 0).mean(), (batch["y_op"] != 0).mean()

    def make_batch(idx):
        b = {"tiles": jnp.asarray(tiles[idx], jnp.float32),
             "units": jnp.asarray(units[idx], jnp.float32),
             "glob": jnp.asarray(glob[idx], jnp.float32)}
        for k, v in labels.items():
            b[f"y_{k}"] = jnp.asarray(v[idx])
        return b

    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(0)
    started = time.time()

    for epoch in range(args.epochs):
        order = rng.permutation(idx_tr)
        run, seen = 0.0, 0
        for i in range(0, len(order) - args.batch, args.batch):
            batch = make_batch(order[i:i + args.batch])
            params, opt_state, loss, parts = step(params, opt_state, batch)
            run += float(loss)
            seen += 1
            if seen % 100 == 0:
                print(f"  epoch {epoch} step {seen:5d}  loss {run / seen:.4f}", flush=True)

        vb = make_batch(idx_val[:4096])
        acc, pred_act, true_act = op_accuracy(params, vb)
        _vl, vparts = loss_fn(params, vb)
        print(f"epoch {epoch}: train {run / max(1, seen):.4f}  "
              f"val op-acc {float(acc):.3f}  "
              f"predicted-acting {float(pred_act):.3f} vs teacher {float(true_act):.3f}  "
              f"| " + "  ".join(f"{k}:{float(v):.3f}" for k, v in vparts.items()), flush=True)

        with (OUT / "bc.pkl").open("wb") as fh:
            pickle.dump({"params": params, "epoch": epoch}, fh)

    print(f"\nwrote {OUT / 'bc.pkl'} in {time.time() - started:.0f}s")
    print("Use it twice: --init for PPO, and as the KL prior that replaces the entropy bonus.")


if __name__ == "__main__":
    main()
