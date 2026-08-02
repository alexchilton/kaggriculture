"""Behaviour cloning on the top leaderboard seats, producing a warm start for `train_jax_rl.py`.

    .venv/bin/python -u scripts/bc_replay.py --top 25 2>&1 | tee data/logs/bc_replay.log
    kagg-train <the usual flags> --init data/bc_runs/<stamp>/latest.pkl

**What this is for, stated so the wrong bar is not applied to it again.** The previous BC attempt was
gated as a standalone agent -- `P(noop)` at spawn 0.9920 against a 0.98 bar, "the checkpoint banks
$0" -- and parked on covariate shift. For a warm start that is the wrong test. The checkpoint does not
have to play well; it has to move the weights somewhere PPO's own exploration reaches the animal
economy, and PPO produces on-policy data from its first update, which is the correction a fixed
replay set cannot provide.

**Why the animal economy needs this and a hint would not do.** `jax_masks.py:93` is
`masks[O.FEED] = has_animal & ~fed & carrying_wheat`. FEED is not merely unlearned, it is *illegal*
until an animal is on the board, unfed, and a unit is standing on it carrying wheat -- so a prior or
bonus toward FEED is computed over a distribution where FEED has zero mass. And buying the animal
first is a *deterministic* loss, not a bad expectation: `escaped = has_animal & (unfed >= 2)`
(`jax_sim.py:1057`) against first-yield days of GOOSE 4, COW 8, SHEEP 6 at $300-$500. The policy
correctly learned to stop buying animals, which closes the loop -- no animals means FEED stays
masked means animals can never be fed. What breaks that loop is a state distribution in which
animals exist, and cloning seats that banked $112k-$132k is the cheapest source of one.

The success criterion is therefore **not** a number this script prints. It is FEED leaving zero in
the PPO run that `--init`s from the checkpoint, and `bank med` leaving $0.

Everything about the loss -- legality gating, live-slot weighting, all-trade-mode cloning of the
conditioned heads, label smoothing -- lives in `kagg/il/bc.py` so it can be tested. See
`tests/test_bc_replay.py`; four of its cases each pin a mistake this project has already paid for.
"""

import argparse
import pathlib
import pickle
import time

import jax
import jax.numpy as jnp
import numpy as np
import optax

from kagg.il import bc
from kagg.rl import jax_obs, jax_policy as P
from kagg.sim import ops as O

RUN_DIR = pathlib.Path("data/bc_runs")

# The ops worth reading in a census. The animal chain first, because it is the reason this exists.
CENSUS = {"FEED": O.FEED, "CARE": O.CARE, "COLLFERT": O.COLLECT_FERT, "PLACE": O.PLACE,
          "PICKUP": O.PICKUP, "PASTURE": O.BUILD_PASTURE, "HARV": O.HARVEST,
          "PLANT": O.PLANT_OP, "WATER": O.WATER, "NOOP": O.NOOP}


def op_census(op_labels, live):
    """Op shares over **live slots only**.

    `MAX_UNITS` is 24 against a crew of about twelve, so a share taken over every slot is mostly
    padding. That mistake produced a "95% NOOP" reading that misdirected most of a day, and it has
    now been made in three separate places in this project.
    """
    sel = np.asarray(op_labels)[np.asarray(live) > 0.5]
    counts = np.bincount(sel.ravel(), minlength=O.N_OPS).astype(float)
    total = max(1.0, counts.sum())
    return {name: 100.0 * counts[i] / total for name, i in CENSUS.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=25,
                    help="how many seats to clone, richest first. Seats, not replays: in 89197802 "
                         "the losing seat still banked $106,091.")
    ap.add_argument("--min-bank", type=float, default=None,
                    help="clone every seat above this final bank instead of a fixed count")
    ap.add_argument("--max-bank", type=float, default=None,
                    help="cap the teachers' final bank. The seats on disk skew strong -- 207 of 312 "
                         "clear $70k -- and a $130k player's actions are conditioned on a board a "
                         "student banking $0 cannot produce, which is why the clone waters 12.5%% on "
                         "a teacher's board and 2.77%% on its own. A mid band (--min-bank 15000 "
                         "--max-bank 35000, 41 seats, median $24,066) is nearer the scripted "
                         "farmer's $30,292 and is reachable. Trades ceiling for reachability; safe "
                         "only because --init carries no KL anchor, so PPO can leave the clone.")
    ap.add_argument("--max-turns", type=int, default=None, help="cap turns per seat (for a smoke run)")
    ap.add_argument("--epochs", type=int, default=6)
    ap.add_argument("--batch", type=int, default=256)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--holdout", type=float, default=0.05,
                    help="validation fraction, held out as a trailing block of whole seats rather "
                         "than at random: consecutive rows are consecutive turns of one game, so a "
                         "random split leaks each turn's near-duplicate neighbours into validation")
    ap.add_argument("--smooth", type=float, default=0.05,
                    help="label smoothing. Bounds the achievable logit gap, which matters because "
                         "the parked BC run learned P(move)=6e-5 at the spawn state -- an absorbing "
                         "state that banks exactly the $3,000 start. 0 disables.")
    ap.add_argument("--d-model", type=int, default=128)
    ap.add_argument("--heads", type=int, default=4)
    ap.add_argument("--layers", type=int, default=3)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--cache", default=None,
                    help="npz to write the built rows to (and reuse). The build is Python-side dict "
                         "walking and is the slow half; the cache also ships to the GPU box.")
    ap.add_argument("--tag", default="bcr")
    args = ap.parse_args()

    run = RUN_DIR / f"{args.tag}-{time.strftime('%Y%m%d-%H%M%S')}"
    run.mkdir(parents=True, exist_ok=True)
    print(f"run dir: {run}", flush=True)

    # ---------------------------------------------------------------- rows
    if args.cache and pathlib.Path(args.cache).exists():
        z = np.load(args.cache)
        rows = {k: z[k] for k in z.files}
        print(f"loaded {len(rows['tiles']):,} cached rows from {args.cache}", flush=True)
    else:
        paths = bc.find_replays("data")
        if not paths:
            raise SystemExit("no replays in data/ -- run scripts/fetch_replays.py first")
        t0 = time.time()
        ranked = bc.rank_seats(paths, min_bank=args.min_bank, max_bank=args.max_bank)
        band = args.min_bank is not None or args.max_bank is not None
        chosen = ranked if band else ranked[: args.top]
        banks = [r.bank for r in chosen]
        print(f"ranked {len(ranked)} seats across {len(paths)} replays in {time.time() - t0:.0f}s")
        print(f"cloning {len(chosen)} seats, ${min(banks):,.0f}-${max(banks):,.0f} "
              f"(median ${float(np.median(banks)):,.0f})", flush=True)

        rows = bc.build_rows(chosen, max_turns=args.max_turns, log_every=2000)
        print(f"built {len(rows['tiles']):,} rows in {time.time() - t0:.0f}s", flush=True)
        if args.cache:
            pathlib.Path(args.cache).parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(args.cache, **rows)
            print(f"cached rows to {args.cache}", flush=True)

    n = len(rows["tiles"])
    widths = (jax_obs.TILE_FEATURES, jax_obs.UNIT_FEATURES, jax_obs.GLOBAL_FEATURES)
    print(f"tile/unit/glob widths: {widths[0]}/{widths[1]}/{widths[2]}"
          f"  -- the PPO run must use the same or --init will refuse it", flush=True)

    demo = op_census(rows["y_op"], rows["live"])
    print("teacher demo mix (live slots):  "
          + "  ".join(f"{k}:{v:.2f}%" for k, v in demo.items()), flush=True)
    if demo["FEED"] == 0.0:
        raise SystemExit("the chosen seats never FEED -- wrong teachers, and cloning them cannot "
                         "possibly move the op this exists for")

    # A trailing block, not a random split: consecutive rows are consecutive turns of one game.
    n_val = int(n * args.holdout)
    idx_tr, idx_val = np.arange(0, n - n_val), np.arange(n - n_val, n)
    print(f"train {len(idx_tr):,}  val {len(idx_val):,}", flush=True)

    # ---------------------------------------------------------------- model
    model = P.Policy(d_model=args.d_model, n_heads=args.heads, n_layers=args.layers)
    key = jax.random.PRNGKey(args.seed)
    params = model.init(key, jnp.asarray(rows["tiles"][:2]), jnp.asarray(rows["units"][:2]),
                        jnp.asarray(rows["glob"][:2]))
    n_params = sum(x.size for x in jax.tree_util.tree_leaves(params))

    # `jax_sim` enables x64 for parity, so anything that does not state its dtype -- including
    # `self.param()` -- silently becomes float64, and the training GPU runs f64 at 1/32 rate.
    bad = [k for k, v in jax.tree_util.tree_leaves_with_path(params) if v.dtype != jnp.float32]
    if bad:
        raise SystemExit(f"non-float32 params: {bad[:3]}")
    print(f"{n_params:,} parameters", flush=True)

    opt = optax.chain(optax.clip_by_global_norm(1.0), optax.adamw(args.lr))
    opt_state = opt.init(params)

    def loss_fn(params, batch):
        heads, _value = model.apply(params, batch["tiles"], batch["units"], batch["glob"])
        return bc.loss(heads, batch, smooth=args.smooth)

    @jax.jit
    def step(params, opt_state, batch):
        (total, parts), grads = jax.value_and_grad(loss_fn, has_aux=True)(params, batch)
        updates, opt_state = opt.update(grads, opt_state, params)
        return optax.apply_updates(params, updates), opt_state, total, parts

    @jax.jit
    def op_scores(params, batch):
        """Accuracy split by whether the teacher acted, and the predicted FEED rate.

        **The aggregate is close to worthless here.** Live slots where the teacher did nothing are
        the easy majority and trivially predictable; a model can read 77% overall while being right
        39% of the time on the slots that carry a decision. Only `acted` says whether it learned to
        play, and `feed` says whether it learned the op this whole track exists for.
        """
        heads, _ = model.apply(params, batch["tiles"], batch["units"], batch["glob"])
        # Score the masked distribution, which is what the policy will actually sample from.
        pred = P._masked_logits(heads["op"], batch["m_op"]).argmax(axis=-1)
        y, live = batch["y_op"], batch["live"] > 0.5
        acted, idle = live & (y != 0), live & (y == 0)
        correct = pred == y
        m = lambda sel: (correct & sel).sum() / jnp.maximum(sel.sum(), 1)   # noqa: E731
        rate = lambda sel: (live & sel).sum() / jnp.maximum(live.sum(), 1)  # noqa: E731
        return (m(live), m(acted), m(idle), rate(pred != 0),
                rate(pred == O.FEED), rate(y == O.FEED))

    def make_batch(idx):
        out = {}
        for k, v in rows.items():
            out[k] = jnp.asarray(v[idx], jnp.float32) if v.dtype.kind == "f" else jnp.asarray(v[idx])
        return out

    rng = np.random.default_rng(args.seed)
    val = make_batch(idx_val[: 4096]) if len(idx_val) else make_batch(idx_tr[:4096])
    started = time.time()

    for epoch in range(args.epochs):
        order = rng.permutation(idx_tr)
        run_loss, seen = 0.0, 0
        for i in range(0, len(order) - args.batch + 1, args.batch):
            params, opt_state, total, parts = step(params, opt_state, make_batch(order[i:i + args.batch]))
            run_loss += float(total)
            seen += 1
            if seen % 100 == 0:
                print(f"  epoch {epoch} step {seen:5d}  loss {run_loss / seen:.4f}", flush=True)

        acc, acc_acted, acc_idle, act_rate, feed_pred, feed_true = op_scores(params, val)
        _vl, vparts = loss_fn(params, val)
        print(f"epoch {epoch}: train {run_loss / max(1, seen):.4f}  live-acc {float(acc):.3f}  "
              f"**ACTED {float(acc_acted):.3f}**  idle {float(acc_idle):.3f}  "
              f"acting {float(act_rate):.3f}\n"
              f"          FEED predicted {float(feed_pred) * 100:.2f}% vs teacher "
              f"{float(feed_true) * 100:.2f}%\n"
              f"          " + "  ".join(f"{k}:{float(v):.3f}" for k, v in vparts.items()),
              flush=True)

        with (run / "latest.pkl").open("wb") as fh:
            pickle.dump({"params": jax.device_get(params), "update": -1, "best": None,
                         "args": vars(args) | {"teacher": f"top-{args.top} replay seats"},
                         "widths": widths}, fh, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"\ndone in {time.time() - started:.0f}s. warm-start with:\n"
          f"  kagg-train <the usual flags> --init {run}/latest.pkl\n"
          f"Success is not a number above. It is FEED leaving zero in that PPO run.")


if __name__ == "__main__":
    main()
