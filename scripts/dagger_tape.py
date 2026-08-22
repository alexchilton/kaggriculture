"""DAgger against the SHIPPED AGENT, rolled out in the reference environment.

    "why dataset - because it needs to not be bc but teacher per step per turn.
     dataset would just be like passing in the tapes of kawa"

That is the whole design. A recorded trajectory is behaviour cloning on カワシギ's tapes, already
tried. Here the teacher is *called* at every state the student produces, so the labels land on the
student's own distribution.

**Why the reference environment and not `jax_sim`.** `scripts/bc_dagger.py` runs its rollout inside
a `lax.scan`, which is fast and requires the teacher to be array code. Our teacher is the shipped
Python agent. Porting it to arrays would be a second implementation of the agent that has to agree
with the first one forever -- the exact thing `kagg/rl/adapter.py`'s docstring refuses -- and the
measurement says it would buy little:

    teacher     2.08 ms/turn   (17.90 ms averaged over a full 719-turn season)
    step        1.14 ms/turn
    adapt       0.86 ms/turn
    encode     12.89 ms/turn   <-- the real bottleneck, and it is unjitted

The teacher is not the cost. See `docs/dagger_tape_teacher_2026-08-22.md`.

**Every primitive here already existed.** This file is plumbing, not new machinery:

    teacher, per turn      kagg/il/tape_teacher.TapeTeacher
    dict action -> labels  kagg/il/replays.encode_action   (returns exactly jax_act.ALL_HEADS)
    dict obs -> features   kagg/rl/adapter.state_from_obs + jax_obs.encode
    heads -> dict action   kagg/agents/neural.decode_action
    loss / optimiser       scripts/bc_dagger.make_step, whose `fit` half is reused verbatim

**The seeds do not vary, and that is deliberate.** The start state is fixed and `weedSpawnChance`
is 0.0, so the four tapes' own seeds are the four games. Diversity comes from the STUDENT deviating
as `beta` anneals, not from resampling the town -- and a tape replayed on a foreign seed is a tape
played into a board its plan does not describe.

Usage:

    .venv/bin/python -u scripts/dagger_tape.py --rounds 8 --episodes 4 --horizon 719 \
        --vocab data/il/bundle_vocab.json --tag tape 2>&1 | tee data/logs/dagger_tape.log
"""
import argparse
import collections
import json
import pathlib
import pickle
import sys
import time

import jax
import jax.numpy as jnp
import numpy as np
import optax

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from kagg.agents import neural as NEURAL                                       # noqa: E402
from kagg.il import market_bundles as MB, replays as RP                        # noqa: E402
from kagg.il.tape_teacher import TapeTeacher                                   # noqa: E402
from kagg.rl import adapter as AD, jax_act as A, jax_obs, jax_policy as P      # noqa: E402
from kagg.search import schedule_agent as SA                                   # noqa: E402

RUN_DIR = REPO / "data/dagger_tape"
TPD = 24


def tape_games():
    """The four recordings, each with the economy and seed it was actually played on.

    `info.seed`, never `configuration.seed`: the latter is None on every recording, so reading it
    there leaves `env.reset()` drawing a fresh town. Two runs of the verifier disagreed by 499 turns
    on one tape before this was found.
    """
    import breakdown as B

    games = []
    for key, (tape_path, team) in sorted(SA.REPLAY_OPENING_TAPE.items()):
        doc = json.loads((REPO / tape_path).read_text())
        seat = doc["info"]["TeamNames"].index(team)
        cfg = B.env_config(REPO / tape_path)
        cfg.pop("steps", None)
        cfg["seed"] = int(doc["info"]["seed"])
        # Weeds off for the first curriculum, which is the stated plan: "after it learns without
        # weeds let them come in". A weed is an unwatered crop, so with weeds on the student's own
        # misses would rewrite the board under a time-indexed teacher.
        cfg["weedSpawnChance"] = 0.0
        opp = [((s[1 - seat] or {}).get("action") or {}) for s in doc["steps"][1:]]
        games.append(dict(key=key, name=pathlib.Path(tape_path).name, seat=seat, cfg=cfg,
                          opponent=opp))
    return games


def opponent_action(game, turn, n_hands):
    """The opponent the tape actually faced, replayed. Trimmed to its live crew."""
    act = game["opponent"][turn] if turn < len(game["opponent"]) else {}
    return {"farmer": act.get("farmer") or ["PASS"],
            "hands": list(act.get("hands") or [])[:n_hands],
            "market": act.get("market") or []}


def run_episode(game, params, model, vocab, bundle_ok, key, beta, horizon, rng):
    """One season. Returns per-turn rows for OUR seat only, plus a small diagnostic counter.

    Only our seat is kept. The jitted rollout in `bc_dagger.py` trains on both seats of self-play;
    here the opponent is a fixed recording with no teacher behind it, so its rows carry no label
    and are dropped rather than fabricated.
    """
    from kaggle_environments import make

    env = make("kaggriculture", configuration=game["cfg"], debug=False)
    env.reset(2)
    seat = game["seat"]
    teacher = TapeTeacher(seat)
    rows, stats = [], collections.Counter()

    for turn in range(horizon):
        if env.done:
            break
        obs = env.state[seat].observation
        # **The teacher is asked EVERY turn, even when the student drives.** Its latches, purchase
        # counter and sell ledger are carried across turns; skipping a query does not skip that
        # state, it corrupts it, and silently.
        teacher_action = teacher.act(obs)

        # **The opponent's private state must be the STUB, not its real shed.** A submission only
        # ever sees its own, so feeding the real one here trains the student on information it can
        # never have at inference -- a distribution shift, not a free win. `neural.py:230` builds it
        # exactly this way for the same reason, and this file must match it or the checkpoint plays
        # worse in the game than it scored in training.
        privates = [obs["private"] if p == seat else AD.agent_private_stub() for p in range(2)]
        sim_state = AD.state_from_obs(obs, privates)
        tiles, units, glob = jax_obs.encode(sim_state)
        flat = (A._flat(tiles), A._flat(units), A._flat(glob))
        masks = A.masks_for(sim_state, bundle_ok)

        n_units = 1 + len(obs["farms"][seat].get("hands") or [])
        labels = RP.encode_action(teacher_action, n_units)

        heads, _v = model.apply(params, *flat)
        key, ka = jax.random.split(key)
        sampled = A.sample(ka, heads, masks)[0]

        # Who moves the world. beta=1 is plain BC on teacher states; beta=0 is pure DAgger, the
        # student driving and the teacher only labelling.
        drive_teacher = bool(rng.random() < beta)
        if drive_teacher:
            action = teacher_action
            stats["turns_teacher"] += 1
        else:
            action = NEURAL.decode_action(sampled, n_units, vocab, seat=seat)
            stats["turns_student"] += 1

        # `unit_live` gates the unit heads. MAX_UNITS is 24 against a crew of a few, so scoring dead
        # slots makes ~85% of the loss a constant -- a padding mistake this project has made three
        # times, once in this very loss.
        live = np.asarray(units[..., 0]).reshape(2, -1)[seat] > 0.5
        rows.append(dict(obs=[np.asarray(x)[seat] for x in flat],
                         masks={k: np.asarray(v)[seat] for k, v in masks.items()},
                         labels={k: np.asarray(v) for k, v in labels.items()},
                         unit_live=live))

        hands = [len((env.state[0].observation["farms"][i] or {}).get("hands") or []) for i in (0, 1)]
        pair = [None, None]
        pair[seat] = teacher.sendable(action, hands[seat])
        pair[1 - seat] = opponent_action(game, turn, hands[1 - seat])
        env.step(pair)

    stats["bank"] = int((env.state[0].observation["farms"][seat] or {}).get("money") or 0)
    stats["opponent_bank"] = int(
        (env.state[0].observation["farms"][1 - seat] or {}).get("money") or 0)
    stats["latches"] = teacher.latches
    return rows, stats, key


def stack(rows):
    """Per-turn dicts -> the `batch_data` the jitted `fit` already consumes."""
    obs = tuple(jnp.asarray(np.stack([r["obs"][i] for r in rows])) for i in range(3))
    masks = {k: jnp.asarray(np.stack([r["masks"][k] for r in rows])) for k in rows[0]["masks"]}
    labels = {k: jnp.asarray(np.stack([r["labels"][k] for r in rows]))
              for k in rows[0]["labels"] if not k.startswith("w_")}
    live = jnp.asarray(np.stack([r["unit_live"] for r in rows]))
    return dict(obs=obs, masks=masks, labels=labels, unit_live=live)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=8)
    ap.add_argument("--episodes", type=int, default=4,
                    help="seasons per round; 4 plays each tape once")
    ap.add_argument("--horizon", type=int, default=719)
    ap.add_argument("--beta0", type=float, default=1.0,
                    help="teacher-execution probability in round 0, annealed to 0 by the last round")
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--epochs", type=int, default=1,
                    help="optimiser passes over the AGGREGATE each round")
    ap.add_argument("--batch-turns", type=int, default=512,
                    help="turns per gradient step over the aggregate")
    ap.add_argument("--vocab", default=str(REPO / "data/il/bundle_vocab.json"))
    ap.add_argument("--d-model", type=int, default=128)
    ap.add_argument("--heads", type=int, default=4)
    ap.add_argument("--layers", type=int, default=3)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tag", default="tape")
    ap.add_argument("--init", default=None,
                    help="warm-start from a BC checkpoint, e.g. data/ckpt/bc_bundle.best.pkl")
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    games = tape_games()
    print("tapes: " + ", ".join("%s %s seat %d seed %d"
                                % (g["key"], g["name"], g["seat"], g["cfg"]["seed"])
                                for g in games), flush=True)

    # **The vocabulary is an artifact, not a constant** -- it must be the same one a later PPO run
    # loads, or the bundle indices mean different things in the loss and at play time. Measured
    # 2026-08-22: the four tapes emit 148 distinct bundles and this 197-entry vocabulary covers
    # 2876/2876 tape turns, so nothing needs rebuilding for them.
    vocab = MB.Vocabulary.from_bundles(
        [tuple(tuple(pair) for pair in b) for b in json.loads(pathlib.Path(args.vocab).read_text())],
        max_size=P.N_BUNDLES)
    # **`pad_to` must be the head width, and omitting it is not a crash you can rely on.** The
    # vocabulary is 197 and the bundle head is 256. The mask mismatch does raise, but the TABLES do
    # not: JAX clamps an out-of-range gather under jit, so an unpadded 197-row table indexed at 200
    # silently returns row 196 -- a real, confidently-emitted, wrong order.
    tables = {k: jnp.asarray(v) for k, v in MB.tables(vocab, pad_to=P.N_BUNDLES).items()}
    bundle_ok = jnp.asarray(MB.valid_table(vocab, pad_to=P.N_BUNDLES))
    print("bundle vocabulary: %d of %d slots, from %s" % (vocab.size, P.N_BUNDLES, args.vocab),
          flush=True)

    model = P.Policy(d_model=args.d_model, n_heads=args.heads, n_layers=args.layers)
    key = jax.random.PRNGKey(args.seed)
    key, sub = jax.random.split(key)

    # Initialise on a real board from the adapter, so the observation widths are the ones the
    # reference environment actually produces.
    from kaggle_environments import make

    probe = make("kaggriculture", configuration=games[0]["cfg"], debug=False)
    probe.reset(2)
    p_obs = probe.state[0].observation
    p_state = AD.state_from_obs(p_obs, [p_obs["private"] if p == 0 else AD.agent_private_stub()
                                        for p in range(2)])
    t0, u0, g0 = jax_obs.encode(p_state)
    params = model.init(sub, A._flat(t0), A._flat(u0), A._flat(g0))
    n_params = sum(x.size for x in jax.tree_util.tree_leaves(params))

    # Same dtype guard the PPO trainer has: `jax_sim` enables x64 for parity, so anything that does
    # not state its dtype silently becomes float64, and this card runs f64 at 1/32 rate.
    bad = [k for k, v in jax.tree_util.tree_leaves_with_path(params) if v.dtype != jnp.float32]
    if bad:
        raise SystemExit("non-float32 params: %s" % (bad[:3],))

    # **Warm start from BC, and refuse rather than adapt on a mismatch.** The observation widths and
    # the bundle head are part of the checkpoint, not of this script; a checkpoint trained against
    # any other width is a different network wearing the same filename. Every field is compared and
    # a mismatch is fatal, because the failure mode of loading anyway is a net that trains happily
    # and means something else.
    if args.init:
        init_path = pathlib.Path(args.init)
        with open(init_path, "rb") as fh:
            ckpt = pickle.load(fh)
        want = {"tile_features": jax_obs.TILE_FEATURES, "unit_features": jax_obs.UNIT_FEATURES,
                "global_features": jax_obs.GLOBAL_FEATURES, "n_bundles": P.N_BUNDLES,
                "vocab_size": vocab.size}
        bad = {k: (ckpt.get(k), v) for k, v in want.items() if ckpt.get(k) != v}
        if bad:
            raise SystemExit("checkpoint %s does not match this build: %s (checkpoint, live)"
                             % (init_path, bad))
        shapes_old = jax.tree_util.tree_structure(ckpt["params"])
        if shapes_old != jax.tree_util.tree_structure(params):
            raise SystemExit("checkpoint %s has a different parameter tree" % init_path)
        params = jax.tree_util.tree_map(jnp.asarray, ckpt["params"])
        hold = ckpt.get("holdout") or {}
        print("warm start: %s  epoch %s  holdout bundle %.4f / op %.4f"
              % (init_path, ckpt.get("epoch"), hold.get("bundle_agreement", float("nan")),
                 hold.get("op_agreement", float("nan"))), flush=True)

    optimiser = optax.chain(optax.clip_by_global_norm(0.5), optax.adam(args.lr))
    opt_state = optimiser.init(params)

    run = RUN_DIR / ("%s-%s" % (args.tag, time.strftime("%Y%m%d-%H%M%S")))
    run.mkdir(parents=True, exist_ok=True)
    print("params: {:,}   run dir: {}".format(n_params, run), flush=True)
    print("tile/unit/glob widths: %d/%d/%d  -- a PPO run must use the same or this will not load"
          % (jax_obs.TILE_FEATURES, jax_obs.UNIT_FEATURES, jax_obs.GLOBAL_FEATURES), flush=True)

    from bc_dagger import make_step

    aggregate = []
    for rnd in range(args.rounds):
        beta = args.beta0 * max(0.0, 1.0 - rnd / max(1, args.rounds - 1))
        _rollout, fit = make_step(model, None, 1, args.horizon, optimiser, beta, tables, bundle_ok)

        t_start = time.time()
        fresh, banks = [], []
        for ep in range(args.episodes):
            game = games[ep % len(games)]
            ep_rows, stats, key = run_episode(game, params, model, vocab, bundle_ok, key, beta,
                                              args.horizon, rng)
            fresh.extend(ep_rows)
            banks.append((game["name"], stats["bank"], stats["opponent_bank"], stats["latches"]))

        # **Aggregate. The first D in DAgger is Dataset Aggregation and it is not decoration.**
        # Fitting only the newest round is iterative BC on a distribution that moves under the
        # student, and it lets the net forget states it already learned to recover from -- the
        # oscillation the algorithm exists to prevent. `bc_dagger.py` fits the round's rollout
        # alone; that is the shortcut, not the algorithm.
        aggregate.extend(fresh)

        # Minibatched, because the aggregate grows every round and one step over all of it is a
        # single enormous gradient rather than an epoch.
        losses = []
        order = np.arange(len(aggregate))
        for _ in range(args.epochs):
            rng.shuffle(order)
            for start in range(0, len(order), args.batch_turns):
                chunk = [aggregate[i] for i in order[start:start + args.batch_turns]]
                if not chunk:
                    continue
                params, opt_state, loss = fit(params, opt_state, stack(chunk))
                losses.append(float(loss))

        wins = sum(1 for _n, b, o, _l in banks if b > o)
        print("round %2d  beta %.2f  fresh %5d  aggregate %6d  loss %8.4f  W%d/%d  %5.0fs"
              % (rnd, beta, len(fresh), len(aggregate), float(np.mean(losses[-8:])),
                 wins, len(banks), time.time() - t_start),
              flush=True)
        for name, bank, opp, latch in banks:
            print("           %-16s bank %8d  opp %8d  latches %s" % (name, bank, opp, latch),
                  flush=True)

        with open(run / ("round%02d.pkl" % rnd), "wb") as fh:
            pickle.dump(dict(params=jax.device_get(params), vocab_size=vocab.size,
                             round=rnd, beta=beta, loss=losses[-1]), fh)

    print("done. checkpoints in %s" % run, flush=True)


if __name__ == "__main__":
    main()
