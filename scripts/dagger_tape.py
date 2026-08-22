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

# **`encode` is 12.9 ms of a 14 ms turn, and only because it is dispatched op by op.** Measured
# 2026-08-22 over 240 turns: teacher 2.08, step 1.14, adapt 0.86, encode 12.89. It is array code
# with a static shape, so jitting it is free and roughly halves the rollout.
_encode = jax.jit(jax_obs.encode)

#: op code -> name, for the per-op agreement breakdown. Inverted from the same table the labels are
#: built with, so the two cannot drift.
OP_NAME = {code: name for name, code in RP.OP_CODE.items()}


def greedy_action(heads, masks):
    """Argmax over legal options, conditioning on `op` before the heads it selects.

    `crop`/`item`/`qty` carry a `[.., MAX_UNITS, N_OPS, K]` axis, so they cannot be masked or
    argmaxed until `op` has been chosen; `A.condition_all` is what collapses that axis.

    **Written here rather than imported from `scripts/play_checkpoint.py`, which is broken.** Its
    `_greedy` still assigns `out["trade"] = cond["trade"]` (`play_checkpoint.py:108`), a head that
    stopped existing when the market became a single `bundle` categorical, so it raises `KeyError`
    on the first call. Its own docstring already records `eval_policy.py:41` rotting the same way.
    Not fixed here because that script is not what this change is about.
    """
    cond = {k: jnp.argmax(P._masked_logits(heads[k], masks[k]), axis=-1) for k in A.CONDITION_HEADS}
    conditioned = A.condition_all(heads, cond)
    return {k: jnp.argmax(P._masked_logits(conditioned[k], masks[k]), axis=-1) for k in A.ALL_HEADS}


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
                          opponent=opp, opponent_name="recorded", melon_at_d3=None))
    return games


def opponent_pool(limit):
    """Recorded opponents from `data/opponent_pool_ranked.json`, as `(name, actions, melon_at_d3)`.

    **Why vary the opponent at all.** Re-running a tape on its own seed is byte-identical, so it is
    more epochs and not more data. Varying the SEED changes the town -- shop timing, prices, money --
    but not the opponent, and `melon_branch` reads the OPPONENT's melon tile count on day 3
    (`melon_branch.py:215`). Without opponent variation that latch is constant per tape, so the
    student sees the branch decision confounded with game identity and can key on anything.

    This is also the honest answer to the review's suggestion of opponent-feature DROPOUT, which was
    declined: dropout can only teach the net to ignore the opponent block, and the melon count lives
    in that block. Variation teaches the invariance where the action is invariant AND the dependence
    where it is not.

    The pool records `melon_at_d3` per entry, so both branches are reachable: Ryo 11, tetsuya 0,
    Matteo 12 against `melon_branch.OPPONENT_MELON = 9`.
    """
    path = REPO / "data/opponent_pool_ranked.json"
    if not path.exists() or limit <= 0:
        return []
    out = []
    for entry in json.loads(path.read_text())[:limit]:
        replay = REPO / entry["replay"]
        if not replay.exists():
            continue
        doc = json.loads(replay.read_text())
        seat = int(entry["seat"])
        actions = [((s[seat] or {}).get("action") or {}) for s in doc["steps"][1:]]
        out.append((entry["name"], actions, entry.get("melon_at_d3")))
    return out


def episode_specs(games, opponents, seeds, rng):
    """The (tape, opponent, seed) combinations an episode is drawn from.

    Index 0 of every axis is the RECORDED configuration -- the tape's own seed and its own
    opponent -- so the validated case stays in the mix rather than being replaced by variants.
    """
    specs = []
    for game in games:
        for oi in range(max(1, len(opponents) + 1)):
            for si in range(max(1, seeds)):
                spec = dict(game)
                if oi > 0:
                    name, actions, melon = opponents[oi - 1]
                    spec = dict(spec, opponent=actions, opponent_name=name, melon_at_d3=melon)
                if si > 0:
                    # A fresh town. The start state is FIXED across every recorded game -- only the
                    # opponent, the shop unlock timing and the weeds vary -- so a foreign seed is
                    # not a broken board, it is the same board with a different market. Which is
                    # exactly what the ladder serves up.
                    spec = dict(spec, cfg=dict(spec["cfg"], seed=int(rng.integers(1, 2 ** 31 - 1))))
                specs.append(spec)
    return specs


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
        tiles, units, glob = _encode(sim_state)
        flat = (A._flat(tiles), A._flat(units), A._flat(glob))
        masks = A.masks_for(sim_state, bundle_ok)

        n_units = 1 + len(obs["farms"][seat].get("hands") or [])
        labels = RP.encode_action(teacher_action, n_units)

        # `unit_live` gates the unit heads. MAX_UNITS is 24 against a crew of a few, so scoring dead
        # slots makes ~85% of the loss a constant -- a padding mistake this project has made three
        # times, once in this very loss.
        live = np.asarray(units[..., 0]).reshape(2, -1)[seat] > 0.5

        heads, _v = model.apply(params, *flat)
        key, ka = jax.random.split(key)
        sampled = A.sample(ka, heads, masks)[0]
        # **Both decodes are measured, because which one to SHIP is an open question.**
        # `neural.py` refuses argmax on the grounds that independent marginals compose into "never
        # sell". That reasoning is from the mean-field era; the market is now one joint `bundle`
        # categorical with op-conditioned argument heads, so per-head greedy along the conditioning
        # order is coherent. Over 719 compounding turns the difference between 0.99 and 1.0 per-turn
        # is 0.99^719 ~ 0.0007 against near-certainty of staying on tape. CLAUDE.md: "a decision to
        # skip a fix can expire when the problem changes."
        greedy = greedy_action(heads, masks)

        # **"Can it repeat the teacher yet" is the stopping criterion, and it is free here.** Both
        # sides are already in hand: the student's own action and the teacher's label, on a state
        # the student is standing in. Measured on the SAMPLED action rather than an argmax, because
        # sampling is what the agent actually plays -- `neural.py` refuses argmax on the grounds
        # that it destroys the joint. Directly comparable to the BC checkpoint's holdout numbers,
        # which are bundle 0.9728 / op 0.8530 against tetsuya.
        t_op = np.asarray(labels["op"])
        t_bundle = int(np.asarray(labels["bundle"]).reshape(-1)[0])
        m = live[: len(t_op)]
        for name, act in (("", sampled), ("g_", greedy)):
            a_op = np.asarray(act["op"])[seat]
            if m.any():
                stats[name + "op_hit"] += int((a_op[: len(t_op)][m] == t_op[m]).sum())
            a_bundle = int(np.asarray(act["bundle"]).reshape(-1)[seat])
            stats[name + "bundle_hit"] += int(a_bundle == t_bundle)
            if t_bundle != 0:                  # the teacher actually traded this turn
                stats[name + "traded_hit"] += int(a_bundle == t_bundle)
        stats["op_n"] += int(m.sum())
        stats["bundle_n"] += 1
        stats["traded_n"] += int(t_bundle != 0)

        # **Which ops it has learned, not just how many.** A single `op` number cannot say whether
        # the net has the whole vocabulary slightly wrong or three ops badly wrong -- and those need
        # different fixes. Counted per TEACHER op, on the greedy decode, live slots only.
        g_op_slots = np.asarray(greedy["op"])[seat][: len(t_op)]
        for slot in np.flatnonzero(m):
            name = OP_NAME.get(int(t_op[slot]), str(int(t_op[slot])))
            stats["opseen_" + name] += 1
            if int(g_op_slots[slot]) == int(t_op[slot]):
                stats["ophit_" + name] += 1

        # Who moves the world. beta=1 is plain BC on teacher states; beta=0 is pure DAgger, the
        # student driving and the teacher only labelling.
        drive_teacher = bool(rng.random() < beta)
        if drive_teacher:
            action = teacher_action
            stats["turns_teacher"] += 1
        else:
            action = NEURAL.decode_action(sampled, n_units, vocab, seat=seat)
            stats["turns_student"] += 1

        rows.append(dict(obs=[np.asarray(x)[seat] for x in flat],
                         masks={k: np.asarray(v)[seat] for k, v in masks.items()},
                         labels={k: np.asarray(v) for k, v in labels.items()},
                         unit_live=live,
                         # Which pool this row belongs to. A turn the TEACHER drove is on-tape and
                         # is the trajectory worth protecting from dilution; a turn the student
                         # drove is a correction label.
                         by_teacher=drive_teacher))

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


def save_resume(run, params, opt_state, rnd, seen_total, rng, args, pools=None, extra=None):
    """Everything needed to continue this run on a different day.

    **Params alone are not a resumable run.** Restarting from them restarts Adam cold and, worse,
    restarts the reservoir empty -- which silently turns Dataset Aggregation back into iterative BC
    and throws away round 0, the only round whose states are the tape's own.

    `latest.pkl` is small (~7 MB) and written every round. The aggregate is ~13.7 KB a turn, so it
    is written separately and less often; losing at most `--save-data-every` rounds of it on a hard
    power-off is the trade.
    """
    tmp = run / "latest.pkl.tmp"
    with open(tmp, "wb") as fh:
        pickle.dump(dict(params=jax.device_get(params), opt_state=jax.device_get(opt_state),
                         round=rnd, seen_total=seen_total, rng=rng.bit_generator.state,
                         args=vars(args), tile_features=jax_obs.TILE_FEATURES,
                         unit_features=jax_obs.UNIT_FEATURES,
                         global_features=jax_obs.GLOBAL_FEATURES, n_bundles=P.N_BUNDLES,
                         **(extra or {})),
                    fh, protocol=5)
    # Renamed into place, never written in place: a power cut during the write would otherwise
    # leave a truncated checkpoint that loads as far as the corruption and then fails.
    tmp.replace(run / "latest.pkl")

    if pools is not None:
        tmp = run / "aggregate.pkl.tmp"
        with open(tmp, "wb") as fh:
            pickle.dump(pools, fh, protocol=5)
        tmp.replace(run / "aggregate.pkl")


def load_resume(run):
    """`(state, aggregate)` from a run directory, or `(None, [])` if there is nothing to continue."""
    latest = pathlib.Path(run) / "latest.pkl"
    if not latest.exists():
        return None, []
    with open(latest, "rb") as fh:
        state = pickle.load(fh)
    agg_path = pathlib.Path(run) / "aggregate.pkl"
    pools = {"expert": [], "student": [], "seen_expert": 0, "seen_student": 0}
    if agg_path.exists():
        with open(agg_path, "rb") as fh:
            loaded = pickle.load(fh)
        # A flat list is a pre-2026-08-22 aggregate, from before the pools were split. Everything in
        # it was collected under one uniform reservoir, so its provenance is unrecoverable; treat it
        # as student data rather than claim it is expert.
        pools = loaded if isinstance(loaded, dict) else dict(pools, student=list(loaded))
    return state, pools


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
                    help="seasons per round, drawn from the tape x opponent x seed combinations")
    ap.add_argument("--opponent-pool", type=int, default=0,
                    help="recorded opponents from data/opponent_pool_ranked.json to mix in; 0 uses "
                         "only each tape's own recorded opponent")
    ap.add_argument("--seeds", type=int, default=1,
                    help="town draws per tape/opponent pair; 1 uses only the tape's recorded seed")
    ap.add_argument("--playout", type=int, default=1,
                    help="student-driven seasons per round, reported and never trained on. The "
                         "bank is the measure agreement only proxies.")
    ap.add_argument("--holdout", type=int, default=0,
                    help="episode combinations reserved for measurement only, never trained on. "
                         "A DIAGNOSTIC, not a gate: memorising the tape is the goal, so this does "
                         "not guard against overfitting -- it separates having memorised the "
                         "PROGRAM (same on every seed) from having memorised the DRAW (prices, "
                         "opponent bank), which look identical on the training metric and do not "
                         "survive a fresh town. Run with the teacher driving, so the states stay "
                         "on-tape and the only thing that varies is the market.")
    ap.add_argument("--horizon", type=int, default=719)
    ap.add_argument("--beta0", type=float, default=1.0,
                    help="teacher-execution probability in round 0, annealed to 0 by the last round")
    ap.add_argument("--lr", type=float, default=1e-4,
                    help="3e-4 on a warm start disturbs the checkpoint before it refits it")
    ap.add_argument("--epochs", type=int, default=1,
                    help="optimiser passes over the AGGREGATE each round")
    ap.add_argument("--batch-turns", type=int, default=512,
                    help="turns per gradient step over the aggregate")
    ap.add_argument("--aggregate-cap", type=int, default=60000,
                    help="total turns kept; ~19 KB each, so 60k is roughly 1.15 GB")
    ap.add_argument("--expert-cap", type=int, default=20000,
                    help="of --aggregate-cap, turns reserved for TEACHER-driven states, which a "
                         "single uniform reservoir would dilute to their proportional share")
    ap.add_argument("--anneal-rounds", type=int, default=10,
                    help="rounds over which beta reaches 0, once the anneal has been earned")
    ap.add_argument("--anneal-after-agree", type=float, default=0.80,
                    help="greedy op agreement on fresh states before beta starts annealing")
    ap.add_argument("--vocab", default=str(REPO / "data/il/bundle_vocab.json"))
    ap.add_argument("--d-model", type=int, default=128)
    ap.add_argument("--heads", type=int, default=4)
    ap.add_argument("--layers", type=int, default=3)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tag", default="tape")
    ap.add_argument("--init", default=None,
                    help="warm-start from a BC checkpoint, e.g. data/ckpt/bc_bundle.best.pkl")
    ap.add_argument("--resume", default=None,
                    help="continue a run directory: params, optimiser state, reservoir and round")
    ap.add_argument("--save-data-every", type=int, default=10,
                    help="rounds between writes of the aggregate; latest.pkl is written every round")
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    games = tape_games()
    print("tapes: " + ", ".join("%s %s seat %d seed %d"
                                % (g["key"], g["name"], g["seat"], g["cfg"]["seed"])
                                for g in games), flush=True)
    opponents = opponent_pool(args.opponent_pool)
    if opponents:
        print("opponents: " + ", ".join("%s (melon d3 %s)" % (n, m) for n, _a, m in opponents),
              flush=True)
    all_specs = episode_specs(games, opponents, args.seeds, rng)
    # The held-out combinations are taken from the END, which is where the varied seeds and
    # opponents sit; index 0 of every axis is the recorded configuration and stays in training.
    holdout_specs = all_specs[len(all_specs) - args.holdout:] if args.holdout else []
    specs = all_specs[:len(all_specs) - len(holdout_specs)]
    print("episode pool: %d combinations (%d train, %d held out) from %d tapes x %d opponents "
          "x %d seeds" % (len(all_specs), len(specs), len(holdout_specs), len(games),
                          len(opponents) + 1, max(1, args.seeds)), flush=True)

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
        # **A narrower checkpoint is MIGRATED, not refused.** `jax_policy.load_or_migrate` zero-pads
        # the grown rows of an input projection (`jax_policy.py:320-337`), so a checkpoint trained
        # before `glob` carried the clock one-hots and the open-shop bits loads with day-one
        # behaviour bit-identical to what it had -- the new columns contribute exactly nothing until
        # they are trained. Refusing instead would mean throwing away every checkpoint on every
        # feature addition, which is how a project ends up never adding features.
        #
        # The vocabulary is still a hard refusal: it is an artifact, not an architecture, and a
        # bundle index that means a different order in the loss than at play time is a mismatch
        # nothing offline would show, because every index is still a valid index.
        if ckpt.get("vocab_size") not in (None, vocab.size):
            raise SystemExit("checkpoint %s was built on a %s-entry vocabulary, this run has %d"
                             % (init_path, ckpt.get("vocab_size"), vocab.size))
        was = (ckpt.get("tile_features"), ckpt.get("unit_features"), ckpt.get("global_features"))
        now = (jax_obs.TILE_FEATURES, jax_obs.UNIT_FEATURES, jax_obs.GLOBAL_FEATURES)
        params = jax.tree_util.tree_map(jnp.asarray, P.load_or_migrate(ckpt["params"], params))
        if was != now:
            print("warm start MIGRATED: tile/unit/glob %s -> %s; the new columns start at zero"
                  % (was, now), flush=True)
        hold = ckpt.get("holdout") or {}
        print("warm start: %s  epoch %s  holdout bundle %.4f / op %.4f"
              % (init_path, ckpt.get("epoch"), hold.get("bundle_agreement", float("nan")),
                 hold.get("op_agreement", float("nan"))), flush=True)

    optimiser = optax.chain(optax.clip_by_global_norm(0.5), optax.adam(args.lr))
    opt_state = optimiser.init(params)

    run = (pathlib.Path(args.resume) if args.resume
           else RUN_DIR / ("%s-%s" % (args.tag, time.strftime("%Y%m%d-%H%M%S"))))
    run.mkdir(parents=True, exist_ok=True)
    print("params: {:,}   run dir: {}".format(n_params, run), flush=True)
    print("tile/unit/glob widths: %d/%d/%d  -- a PPO run must use the same or this will not load"
          % (jax_obs.TILE_FEATURES, jax_obs.UNIT_FEATURES, jax_obs.GLOBAL_FEATURES), flush=True)

    from bc_dagger import make_step

    # **Built ONCE, outside the round loop.** It was rebuilt every round, which re-traced and
    # recompiled `fit` and `evaluate` for no functional reason: `beta` is consumed only by the
    # jitted `rollout`, which this script does not use -- the rollout here is the Python loop over
    # the reference environment.
    _rollout, fit, evaluate = make_step(model, None, 1, args.horizon, optimiser, 0.0,
                                        tables, bundle_ok)

    aggregate, seen_total, first_round = [], 0, 0
    expert, student, seen_expert, seen_student = [], [], 0, 0
    anneal_start, last_agree = None, 0.0
    if args.resume:
        state, pools = load_resume(run)
        if state is None:
            print("resume: nothing to continue in %s, starting fresh" % run, flush=True)
        else:
            widths = {"tile_features": jax_obs.TILE_FEATURES,
                      "unit_features": jax_obs.UNIT_FEATURES,
                      "global_features": jax_obs.GLOBAL_FEATURES, "n_bundles": P.N_BUNDLES}
            bad = {k: (state.get(k), v) for k, v in widths.items() if state.get(k) != v}
            if bad:
                # **Resume refuses where `--init` migrates, and the difference is the reservoir.**
                # Migrating the params would be easy; the stored `aggregate.pkl` holds observations
                # encoded at the OLD width, and there is no honest way to widen a cached observation
                # -- the new columns were never observed. A run whose features changed is a new run.
                raise SystemExit(
                    "resume %s does not match this build: %s (checkpoint, live).\n"
                    "The reservoir was encoded at the old width. Start a fresh run directory and "
                    "use --init to carry the weights over." % (run, bad))
            params = jax.tree_util.tree_map(jnp.asarray, state["params"])
            opt_state = jax.tree_util.tree_map(
                lambda x: jnp.asarray(x) if hasattr(x, "shape") else x, state["opt_state"])
            seen_total = int(state["seen_total"])
            first_round = int(state["round"]) + 1
            rng.bit_generator.state = state["rng"]
            expert, student = pools["expert"], pools["student"]
            seen_expert, seen_student = pools["seen_expert"], pools["seen_student"]
            anneal_start = state.get("anneal_start")
            last_agree = float(state.get("last_agree", 0.0))
            # **The gate is re-read against the CURRENT bar on resume.** Raising
            # `--anneal-after-agree` on a run that already started annealing must actually take
            # effect; otherwise the restored `anneal_start` keeps the handover running at the old,
            # lower standard and the new argument is silently ignored -- a byte-identical result
            # that reads exactly like a measured null.
            if anneal_start is not None and last_agree < args.anneal_after_agree:
                print("resume: bar raised to %.4f and agreement is %.4f -- anneal reset, the "
                      "teacher drives again" % (args.anneal_after_agree, last_agree), flush=True)
                anneal_start = None
            print("resume: %s at round %d, expert %d + student %d turns, %d seen, "
                  "anneal_start %s, last greedy op agreement %.4f"
                  % (run, first_round, len(expert), len(student), seen_total,
                     anneal_start, last_agree), flush=True)

    for rnd in range(first_round, args.rounds):
        # **Beta must not be tied to `--rounds`.** It was, which coupled the exploration schedule to
        # an arbitrary stopping point: asking for more rounds silently made the teacher drive for
        # longer. The anneal is its own schedule now, and the run length is decided by agreement.
        # **Beta anneals when the student has earned it, not when the round counter says so.**
        #
        # A fixed schedule spends its later rounds labelling boards the student has wrecked, with a
        # TIME-INDEXED teacher whose answer there is "the tape's action anyway" -- frequently
        # illegal on that board, and never a route back to the tape. Those labels are close to
        # worthless, and the previous run spent rounds 10+ collecting them at op agreement 0.17.
        #
        # So the teacher keeps driving until greedy op agreement on fresh states clears the bar,
        # and only then does the student take the wheel. Measured on the GREEDY decode because that
        # is the ceiling: sampled agreement can sit low purely from entropy while the argmax is
        # already right.
        if anneal_start is None and last_agree >= args.anneal_after_agree:
            anneal_start = rnd
            print("beta anneal starts at round %d (greedy op agreement %.4f >= %.4f)"
                  % (rnd, last_agree, args.anneal_after_agree), flush=True)
        if anneal_start is None:
            beta = args.beta0
        else:
            progress = (rnd - anneal_start) / max(1, args.anneal_rounds - 1)
            beta = args.beta0 * max(0.0, 1.0 - progress)

        t_start = time.time()
        fresh, banks = [], []
        agree = collections.Counter()
        for ep in range(args.episodes):
            game = specs[(rnd * args.episodes + ep) % len(specs)]
            ep_rows, stats, key = run_episode(game, params, model, vocab, bundle_ok, key, beta,
                                              args.horizon, rng)
            fresh.extend(ep_rows)
            agree.update({k: v for k, v in stats.items()
                          if k.startswith(("op_", "bundle_", "traded_", "g_", "opseen_", "ophit_"))})
            banks.append(("%s v %s" % (game["name"][:8], game["opponent_name"][:12]),
                          stats["bank"], stats["opponent_bank"], stats["latches"]))

        # **Aggregate. The first D in DAgger is Dataset Aggregation and it is not decoration.**
        # Fitting only the newest round is iterative BC on a distribution that moves under the
        # student, and it lets the net forget states it already learned to recover from -- the
        # oscillation the algorithm exists to prevent. `bc_dagger.py` fits the round's rollout
        # alone; that is the shortcut, not the algorithm.
        # **Two pools, because one uniform reservoir does NOT protect the expert states.**
        #
        # The previous comment here claimed it did. It was wrong, and the arithmetic is simple: a
        # uniform reservoir keeps every round at its PROPORTIONAL share, so after 400 rounds
        # (1.15M turns seen against a 60k cap) round 0 survives as about 150 rows. The trajectory
        # the student most needs -- the tape's own -- would have been diluted to noise exactly as
        # the run got long.
        #
        # So teacher-driven turns get their own protected pool, and only the student-driven pool is
        # reservoir-sampled. `expert_cap` is a floor on how much of the aggregate is always the real
        # thing.
        for row in fresh:
            pool = expert if row.pop("by_teacher") else student
            # **The expert pool expands into budget the student pool is not using.** While beta is 1
            # every turn is teacher-driven, so the student pool is empty and a fixed `--expert-cap`
            # would discard expert turns while 40k of a 60k budget sat idle. `--expert-cap` is a
            # FLOOR on the expert share, not a ceiling on it.
            cap = (max(args.expert_cap, args.aggregate_cap - len(student)) if pool is expert
                   else args.aggregate_cap - min(len(expert), args.expert_cap))
            seen = seen_expert if pool is expert else seen_student
            seen += 1
            if pool is expert:
                seen_expert = seen
            else:
                seen_student = seen
            seen_total += 1
            if len(pool) < cap:
                pool.append(row)
            else:
                j = int(rng.integers(0, seen))
                if j < cap:
                    pool[j] = row
        aggregate = expert + student

        # Minibatched, because the aggregate grows every round and one step over all of it is a
        # single enormous gradient rather than an epoch.
        # **Score the FRESH states before fitting them.** The training loss is over the aggregate,
        # which is dominated by earlier rounds; a loss falling on data already fitted says nothing
        # about the states the policy is producing now. This is `-mean log p(teacher action)` on
        # exactly the states just visited, and it is the honest progress number.
        fresh_loss, fresh_heads = evaluate(params, stack(fresh[: args.batch_turns]))

        losses = []
        order = np.arange(len(aggregate))
        for _ in range(args.epochs):
            rng.shuffle(order)
            for start in range(0, len(order), args.batch_turns):
                chunk = [aggregate[i] for i in order[start:start + args.batch_turns]]
                if not chunk:
                    continue
                params, opt_state, loss, per_head = fit(params, opt_state, stack(chunk))
                losses.append(float(loss))

        wins = sum(1 for _n, b, o, _l in banks if b > o)
        op_ag = agree["op_hit"] / max(1, agree["op_n"])
        bd_ag = agree["bundle_hit"] / max(1, agree["bundle_n"])
        tr_ag = agree["traded_hit"] / max(1, agree["traded_n"])
        g_op = agree["g_op_hit"] / max(1, agree["op_n"])
        g_bd = agree["g_bundle_hit"] / max(1, agree["bundle_n"])
        g_tr = agree["g_traded_hit"] / max(1, agree["traded_n"])
        # **`W` is the TEACHER's win rate while beta is high, not the student's.** At beta=1 the
        # teacher drives every turn, so that column only becomes a statement about the student as
        # beta anneals to 0. Agreement is the number that answers "can it repeat the teacher yet",
        # and it is measured on states the student is standing in at every beta.
        print("round %3d  beta %.2f  sample op %.4f bundle %.4f traded %.4f | "
              "greedy op %.4f bundle %.4f traded %.4f | fresh %6.4f agg %6.4f | n %6d  W%d/%d %4.0fs"
              % (rnd, beta, op_ag, bd_ag, tr_ag, g_op, g_bd, g_tr,
                 float(fresh_loss), float(np.mean(losses[-8:])),
                 len(aggregate), wins, len(banks), time.time() - t_start),
              flush=True)
        print("           per-head (fresh)  "
              + "  ".join("%s %.4f" % (h, float(v)) for h, v in sorted(fresh_heads.items())),
              flush=True)
        # Per-op agreement, worst first. A single `op` number cannot distinguish "the whole
        # vocabulary is slightly wrong" from "three ops are badly wrong", and those want different
        # fixes. Only ops the teacher used at least 20 times, so a 1-of-2 does not lead the table.
        by_op = sorted(((agree["ophit_" + n] / agree["opseen_" + n], n, agree["opseen_" + n])
                        for n in {k[len("opseen_"):] for k in agree if k.startswith("opseen_")}
                        if agree["opseen_" + n] >= 20), key=lambda r: r[0])
        if by_op:
            print("           per-op (greedy)   "
                  + "  ".join("%s %.3f/%d" % (n, r, c) for r, n, c in by_op[:8]), flush=True)

        # **How it actually PLAYS, which agreement only proxies.** One season with the student
        # driving every turn, reported and NOT trained on -- the bank is the thing, and a per-turn
        # agreement number cannot tell you whether 0.83 is a good season or a bankrupt one. This is
        # the project's own rule: prefer a replay to an aggregate.
        for spec in specs[:args.playout]:
            _rows, pstats, key = run_episode(spec, params, model, vocab, bundle_ok, key,
                                             0.0, args.horizon, rng)
            print("           PLAYOUT %-22s student %8d  opponent %8d  %s  latches %s"
                  % (spec["name"][:8] + " v " + spec["opponent_name"][:10], pstats["bank"],
                     pstats["opponent_bank"],
                     "WIN " if pstats["bank"] > pstats["opponent_bank"] else "loss",
                     pstats["latches"]), flush=True)

        last_agree = g_op

        # **The held-out probe. Reported, never trained on, and it gates nothing.**
        # Run with the TEACHER driving so the states stay on-tape: the tape is identical, the target
        # actions are identical, and the only thing that differs is the town draw. So a gap between
        # this and the training number is the net having memorised prices rather than the program.
        if holdout_specs:
            ho = collections.Counter()
            for spec in holdout_specs:
                _rows, hstats, key = run_episode(spec, params, model, vocab, bundle_ok, key,
                                                 1.0, args.horizon, rng)
                ho.update({k: hstats[k] for k in ("op_n", "bundle_n", "traded_n",
                                                  "g_op_hit", "g_bundle_hit", "g_traded_hit")})
            print("           held out (%d)     greedy op %.4f  bundle %.4f  traded %.4f"
                  % (len(holdout_specs), ho["g_op_hit"] / max(1, ho["op_n"]),
                     ho["g_bundle_hit"] / max(1, ho["bundle_n"]),
                     ho["g_traded_hit"] / max(1, ho["traded_n"])), flush=True)
        for name, bank, opp, latch in banks:
            print("           %-16s bank %8d  opp %8d  latches %s" % (name, bank, opp, latch),
                  flush=True)

        # Written every round so the machine can be switched off between any two of them. The
        # aggregate is large, so it goes less often; at worst `--save-data-every` rounds of
        # reservoir are lost on a hard power-off, and never the params or the optimiser.
        due = ((rnd + 1) % max(1, args.save_data_every) == 0) or (rnd + 1 == args.rounds)
        save_resume(run, params, opt_state, rnd, seen_total, rng, args,
                    pools=(dict(expert=expert, student=student, seen_expert=seen_expert,
                                seen_student=seen_student) if due else None),
                    extra=dict(anneal_start=anneal_start, last_agree=last_agree))

    print("done. checkpoints in %s" % run, flush=True)


if __name__ == "__main__":
    main()
