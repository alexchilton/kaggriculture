"""DAgger against a live in-sim teacher, producing a warm-start checkpoint for `train_jax_rl.py`.

**Why a live oracle and not a replay set.** The previous BC attempt was parked on covariate shift:
corrective labels were "96.7% non-noop and entirely WEST and NORTH -- the learner never leaves spawn,
so the teacher never demonstrates anything else", and the checkpoint "plays well from a state a good
player produced and cannot produce one". That is a property of a *fixed* demonstration set: it can
never show recovery from a state the student wanders into, because the student was not there when the
set was recorded.

Both teachers here run inside the compiled simulator, so they can be asked "what would you do?" at
whatever state the student actually reached, every turn. That is DAgger's whole point and it is the
structural fix for exactly the failure that parked the track. No `pure_callback`, no serialisation,
no replay files -- the teacher is array code in the same scan as the student.

**Choose the teacher deliberately, because they teach different halves.**

  --teacher heuristic   the crop economy: melon in, water it, harvest, sell. Banks $23,783.
                        `buy_animal` is hard-zero (`jax_heuristic.py:192`) and it never FEEDs, so it
                        CANNOT teach the animal economy. Do not use it and expect FEED.
  --teacher rancher     the animal economy: pasture, place, feed, care, collect fertiliser. Keeps
                        9-10 animals alive to day 29 -- the only thing in this project that does --
                        but banks only $12,078 and spends 37% of its actions on PICKUP against a
                        measured winner target of 2.3%. A weaker teacher that demonstrates the ops
                        the policy has never once emitted.

FEED has fired exactly zero times in every RL run to date. If that is the gap being targeted, the
teacher has to be `rancher`, with the caveat that it will also teach the shed thrash.

**What this deliberately does not do.** It trains params only. `--init` in `train_jax_rl.py` restores
params and leaves the optimiser fresh, and there is no KL-anchor to the BC checkpoint -- Ender's own
warning applies, recorded in `hand_prior_heads`: a collapsed clone as a prior "would punish PPO for
the one behaviour it needs to discover". Warm-start, then let PPO move freely; anchor later only if
it is measurably unlearning something good, as a separate experiment.

**Ordering constraint that will waste a run if ignored.** The observation width is part of the
checkpoint. Tiles are 27 and the global token 59 as of the animal-age and price features; a BC
checkpoint trained against any other width will not load. Always train BC against the observation
that the PPO run will use.

    .venv/bin/python -u scripts/bc_dagger.py --teacher rancher --rounds 8 --batch 64
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

from kagg.rl import jax_act as A, jax_heuristic as HEUR, jax_obs, jax_policy as P
from kagg.il import market_bundles as MB
from kagg.rl import jax_rancher as RANCH
from kagg.sim import jax_sim as J

EPISODE_TURNS = 719
RUN_DIR = pathlib.Path("data/bc_runs")


def _bucket_index(raw, buckets):
    """Nearest bucket index for a raw quantity, for the UNIT quantity ladder only.

    Market quantities no longer go through here. Their class index is the quantity itself, so the
    label is `clip(raw, 0, MAX_QTY - 1)` and the teacher's number survives exactly -- which is the
    whole point in imitation, where that number is known.
    """
    d = jnp.abs(raw[..., None] - buckets.reshape((1,) * raw.ndim + (-1,)))
    return jnp.argmin(d, axis=-1)


def _exact_qty(raw):
    """A teacher quantity -> its own class index, clamped to the head width.

    Clamped, never wrapped: the teacher's largest BUY_PRODUCT is 134 and `134 % 64 == 6` would be a
    different order. `jnp.clip` matches `market_bundles.clamp_qty`, which is the Python path the
    offline labeller uses; the two must agree or BC and DAgger train against different targets.
    """
    return jnp.clip(raw.astype(jnp.int32), 0, P.MAX_QTY - 1)


def teacher_labels(sim_actions, tables):
    """`J.Actions` -> the head-index dict the student's `evaluate` scores against.

    Every head the simulator reads gets a label, and now every head HAS one. The old `trade` mode
    was a latent no teacher could supply -- it was labelled 0 and excluded from the loss, which also
    meant only the mode-0 slice of `sell` and `buy_product` was ever trained while play sampled the
    mode. The bundle removes the problem rather than working around it: a teacher's order list IS
    the bundle, so `bundle_index_of` reads the label straight off the actions it played.

    `tables` is `market_bundles.tables(vocab)` in `jnp` form, the same object `to_sim_actions` uses,
    so the label a teacher gets and the orders a student emits are indexed identically.
    """
    b2 = lambda x, buckets: _bucket_index(x, buckets)          # noqa: E731
    return {
        "op": sim_actions.unit_op.astype(jnp.int32),
        "crop": sim_actions.unit_crop.astype(jnp.int32),
        "item": sim_actions.unit_item.astype(jnp.int32),
        "qty": b2(sim_actions.unit_qty, P.UNIT_QTY_BUCKETS),
        "bundle": A.bundle_index_of(sim_actions, tables),
        "qty_sell": _exact_qty(sim_actions.sell),
        "qty_buy_product": _exact_qty(sim_actions.buy_product),
        "qty_buy_seed": _exact_qty(sim_actions.buy_seed),
    }


# Every head is scored now. The exclusion here used to exist because `trade` had no teacher; the
# bundle does, so there is nothing left to leave out.
SCORED_HEADS = A.ALL_HEADS

# **Not every head is an equally important decision, and a flat mean says they are.**
#
# `op` and `bundle` are read on every turn. The other six are conditional, and their modal answer is
# 0 -- roughly 79% of turns place no market order at all, so the three `qty_*` heads are mostly
# "predict zero", learn it quickly, and then dominate any fall in a 1/8-weighted average. That made
# the reported loss drop 7x while agreement against the teacher got worse, which is a metric telling
# a story the policy was not living.
#
# One block, so the weights cannot scatter. They are parameters, not switches: every head is still
# scored, none is gated off.
HEAD_WEIGHTS = {"op": 3.0, "bundle": 3.0}


def make_step(model, teacher_fn, batch, horizon, optimiser, beta, tables, bundle_ok):
    """One DAgger round: roll the *student* out, label every state with the teacher, fit.

    `beta` is the probability that a turn is actually *executed* by the teacher rather than the
    student. beta=1 is plain behaviour cloning on teacher states -- which is what failed before,
    because the student never sees its own mistakes. beta=0 is pure DAgger: the student drives and
    the teacher only labels, so every label lands on a state the student really produced. Annealing
    from high to low is the standard schedule and is why this can escape the spawn fixation.
    """

    @jax.jit
    def rollout(params, state, key):
        def one_turn(carry, _):
            state, key = carry
            key, ka, kb = jax.random.split(key, 3)

            tiles, units, glob = jax_obs.encode(state)
            obs = (A._flat(tiles), A._flat(units), A._flat(glob))
            masks = A.masks_for(state, bundle_ok)
            student_actions, _lp, _e = A.sample(ka, model.apply(params, *obs)[0], masks)

            teacher_sim = teacher_fn(state)
            labels = teacher_labels(teacher_sim, tables)

            # Who actually moves the world this turn.
            take_teacher = jax.random.uniform(kb, (batch,)) < beta
            flat_take = jnp.repeat(take_teacher, 2)
            student_sim = A.to_sim_actions(student_actions, batch, tables)
            sim_actions = jax.tree_util.tree_map(
                lambda s, t: jnp.where(
                    flat_take.reshape(batch, 2, *((1,) * (s.ndim - 2))), t, s),
                student_sim, teacher_sim)

            nxt = J.step(state, sim_actions)
            done = (nxt.step_index > J.LAST_STEP) & ~(state.step_index > J.LAST_STEP)
            # `reset_with_shops`: a plain reset never opens a shop, so DAgger would collect its
            # student states -- and therefore its teacher labels -- in a market with a fifth of the
            # real season wheat demand.
            fresh = J.reset_with_shops(batch)
            pick = lambda new, old: jnp.where(                  # noqa: E731
                done.reshape((-1,) + (1,) * (old.ndim - 1)), new, old)
            nxt = nxt._replace(
                step_index=pick(fresh.step_index, nxt.step_index),
                tiles=jax.tree_util.tree_map(pick, fresh.tiles, nxt.tiles),
                farm=jax.tree_util.tree_map(pick, fresh.farm, nxt.farm),
                inventory=pick(fresh.inventory, nxt.inventory),
                # Per game, so it restarts with the rest of the board. Omitting it was invisible
                # while every schedule was the constant `NEVER`; it is not now.
                unlock_day=pick(fresh.unlock_day, nxt.unlock_day),
            )
            # Only slots the teacher can be held responsible for: a live unit's action.
            unit_live = units[..., 0].reshape(batch * 2, -1) > 0.5
            return (nxt, key), dict(obs=obs, masks=masks, labels=labels, unit_live=unit_live)

        (final, key), traj = jax.lax.scan(one_turn, (state, key), None, length=horizon)
        return final, key, traj

    def head_active(labels):
        """Per-head element mask: does the teacher's own choice make this field readable?

        Three families:
          * `op` and `bundle` are always read.
          * `crop`/`item`/`qty` are read only for the op that consumes them -- `active_unit_heads`
            (`jax_act.py:131`) is the same rule `sample` and `evaluate` apply, so scoring anything
            else trains a slice the decode never looks at, e.g. `crop | WATER`.
          * `qty_*` are read only for the products the chosen BUNDLE actually names. The bundle is
            the coordinating decision; a quantity for a product not in it is not a decision.
        """
        act = A.active_unit_heads(labels["op"])
        out = {h: act[h] for h in A.UNIT_HEADS}
        out["bundle"] = None
        b = labels["bundle"].reshape(-1)
        for head, col in (("qty_sell", "sell"), ("qty_buy_product", "buy_product"),
                          ("qty_buy_seed", "buy_seed")):
            if col in tables:
                out[head] = jnp.take(tables[col], b, axis=0) > 0
            else:
                out[head] = None
        return out

    def loss_fn(params, batch_data):
        heads, _v = model.apply(params, *batch_data["obs"])
        # Conditioned on the *teacher's* own op -- the same slice `jax_act.evaluate` will score at
        # rollout time. `condition_all` returns every head, conditioned or not, so there is no
        # per-head branch to keep in step here. The market half needs no conditioning now: the
        # bundle is the coordinating decision and it is a label, not a latent.
        cond = A.condition_all(heads, batch_data["labels"])
        active = head_active(batch_data["labels"])
        total, n, per_head = 0.0, 0.0, {}
        for h in SCORED_HEADS:
            src = cond[h]
            lab = batch_data["labels"][h]
            mask = batch_data["masks"][h]
            logp, _ent = P.eval_head(src, mask, lab)
            # **Only score a label the student is allowed to emit.** A masked-illegal option carries
            # `NEG_INF = -1e9`, so a single illegal label swamps the whole objective -- the first run
            # of this reported a loss of 5.3e7 that did not move, because the teacher names an item
            # and a quantity on every unit slot including ones where nothing is legal, and those
            # rows were being asked for an infinite log-probability. You cannot clone an action the
            # student has no way to take.
            legal = jnp.take_along_axis(mask, lab[..., None], axis=-1)[..., 0]
            logp = jnp.where(legal, logp, 0.0)
            w = legal.astype(jnp.float32)
            if h in A.UNIT_HEADS:
                # **Dead unit slots carry no information and must not be averaged in.** `MAX_UNITS`
                # is 24 against a crew of a few, so scoring every slot makes ~85% of the loss a
                # constant -- the padding mistake this project has now made three times, once in
                # this very loss.
                w = w * batch_data["unit_live"].astype(jnp.float32)
            if active.get(h) is not None:
                w = w * active[h].astype(jnp.float32)
            head_loss = -(logp * w).sum() / jnp.maximum(w.sum(), 1.0)
            per_head[h] = head_loss
            weight = HEAD_WEIGHTS.get(h, 1.0)
            total = total + weight * head_loss
            n += weight
        return total / n, per_head

    @jax.jit
    def fit(params, opt_state, batch_data):
        (loss, per_head), grads = jax.value_and_grad(loss_fn, has_aux=True)(params, batch_data)
        updates, opt_state = optimiser.update(grads, opt_state, params)
        return optax.apply_updates(params, updates), opt_state, loss, per_head

    @jax.jit
    def evaluate(params, batch_data):
        """The same objective without a gradient step, for scoring FRESH states before fitting them.

        Needed because the training loss is computed over the aggregate, which is dominated by old
        rounds. A loss that falls on data the policy has already been fitted to says nothing about
        whether the policy has improved on the states it is producing NOW.
        """
        return loss_fn(params, batch_data)

    return rollout, fit, evaluate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--teacher", choices=("heuristic", "rancher"), default="rancher",
                    help="rancher teaches the animal economy (FEED/CARE/COLLECT_FERT); heuristic "
                         "teaches crops and CANNOT teach FEED -- its buy_animal is hard-zero")
    ap.add_argument("--vocab", required=True,
                    help="JSON list of bundles, from scripts/build_bundle_vocab.py. "
                         "Required: a vocabulary that differs between labelling and "
                         "play makes every bundle index mean something else, and "
                         "nothing offline would show it.")
    ap.add_argument("--rounds", type=int, default=8)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--horizon", type=int, default=32)
    ap.add_argument("--epochs", type=int, default=4)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--beta0", type=float, default=0.9,
                    help="teacher-execution probability in round 0, annealed to 0 by the last round")
    ap.add_argument("--d-model", type=int, default=128)
    ap.add_argument("--heads", type=int, default=4)
    ap.add_argument("--layers", type=int, default=3)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tag", default="bc")
    args = ap.parse_args()

    teacher_fn = HEUR.actions if args.teacher == "heuristic" else RANCH.actions
    model = P.Policy(d_model=args.d_model, n_heads=args.heads, n_layers=args.layers)
    key = jax.random.PRNGKey(args.seed)
    key, sub = jax.random.split(key)
    state0 = J.reset_with_shops(args.batch, seed=args.seed)   # also the rollout start, see below
    t, u, g = jax_obs.encode(state0)
    params = model.init(sub, A._flat(t), A._flat(u), A._flat(g))
    n_params = sum(x.size for x in jax.tree_util.tree_leaves(params))

    # Same dtype guard the PPO trainer has: `jax_sim` enables x64 for parity, so anything that does
    # not state its dtype silently becomes float64, and this card runs f64 at 1/32 rate.
    bad = [k for k, v in jax.tree_util.tree_leaves_with_path(params) if v.dtype != jnp.float32]
    if bad:
        raise SystemExit(f"non-float32 params: {bad[:3]}")

    optimiser = optax.chain(optax.clip_by_global_norm(0.5), optax.adam(args.lr))
    opt_state = optimiser.init(params)

    # **The vocabulary is an artifact, not a constant.** It must be the SAME one the labels were
    # built with and the same one a later PPO run loads, or the bundle indices mean different things
    # in the loss and at play time -- a mismatch nothing offline would show, because every index is
    # still a valid index. `--vocab` is required for that reason.
    vocab = MB.Vocabulary.from_bundles(
        [tuple(tuple(pair) for pair in b) for b in json.loads(pathlib.Path(args.vocab).read_text())],
        max_size=P.N_BUNDLES)
    tables = {k: jnp.asarray(v) for k, v in MB.tables(vocab).items()}
    bundle_ok = jnp.asarray(MB.valid_table(vocab))
    print(f"bundle vocabulary: {vocab.size} of {P.N_BUNDLES} slots, from {args.vocab}", flush=True)

    run = RUN_DIR / f"{args.tag}-{time.strftime('%Y%m%d-%H%M%S')}"
    run.mkdir(parents=True, exist_ok=True)
    print(f"teacher: {args.teacher}   params: {n_params:,}   run dir: {run}")
    print(f"tile/unit/glob widths: {jax_obs.TILE_FEATURES}/{jax_obs.UNIT_FEATURES}/"
          f"{jax_obs.GLOBAL_FEATURES}  -- a PPO run must use the same or this will not load",
          flush=True)

    state = state0
    for rnd in range(args.rounds):
        beta = args.beta0 * max(0.0, 1.0 - rnd / max(1, args.rounds - 1))
        rollout, fit, _evaluate = make_step(model, teacher_fn, args.batch, args.horizon, optimiser,
                                            beta, tables, bundle_ok)
        key, kr = jax.random.split(key)
        state, key, traj = rollout(params, state, kr)

        flat_n = args.horizon * args.batch * 2

        data = dict(
            obs=tuple(x.reshape((flat_n,) + x.shape[2:]) for x in traj["obs"]),
            masks={k: v.reshape((flat_n,) + v.shape[2:]) for k, v in traj["masks"].items()},
            # **Labels carry three leading axes and obs/masks carry two.** The teacher speaks in
            # `J.Actions`, which is `[batch, seats, ...]`, so a scanned label is
            # `[horizon, batch, seats, ...]`; obs and masks are already seat-flattened by `A._flat`
            # before the scan, so they are `[horizon, batch*seats, ...]`. Collapsing both with the
            # same slice silently doubles the label width.
            labels={k: v.reshape((flat_n,) + v.shape[3:]) for k, v in traj["labels"].items()},
            unit_live=traj["unit_live"].reshape((flat_n,) + traj["unit_live"].shape[2:]),
        )
        losses = []
        for _ in range(args.epochs):
            params, opt_state, loss, per_head = fit(params, opt_state, data)
            losses.append(float(loss))
        print("           per-head loss  "
              + "  ".join("%s %.4f" % (h, float(v)) for h, v in sorted(per_head.items())),
              flush=True)

        # What the teacher actually demonstrated, on live slots only. If FEED is zero here the
        # teacher cannot teach it, and no amount of student training will conjure it.
        ops = np.asarray(jax.device_get(data["labels"]["op"]))
        live = np.asarray(jax.device_get(data["unit_live"]))
        cnt = np.bincount(ops[live].ravel(), minlength=18).astype(float)
        tot = max(1.0, cnt.sum())
        show = {"FEED": 12, "CARE": 13, "COLLFERT": 14, "HARV": 6, "WATER": 5,
                "PLANT": 7, "PICKUP": 9, "NOOP": 0}
        mix = "  ".join(f"{k}:{100 * cnt[i] / tot:.2f}%" for k, i in show.items())
        print(f"[round {rnd}] beta {beta:.2f}  loss {losses[0]:.4f} -> {losses[-1]:.4f}\n"
              f"           teacher demo mix  {mix}", flush=True)

        with (run / "latest.pkl").open("wb") as fh:
            pickle.dump({"params": jax.device_get(params), "update": -1,
                         "args": vars(args), "best": None,
                         "widths": (jax_obs.TILE_FEATURES, jax_obs.UNIT_FEATURES,
                                    jax_obs.GLOBAL_FEATURES)}, fh,
                        protocol=pickle.HIGHEST_PROTOCOL)

    print(f"\ndone. warm-start with:  kagg-train ... --init {run}/latest.pkl")


if __name__ == "__main__":
    main()
