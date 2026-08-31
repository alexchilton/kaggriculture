"""Does the clone still play when it is dropped into `jax_sim`? Greedy, so sampling cannot be blamed.

    python -u scripts/control_what_the_clone_banks_under_greedy.py \
        --ckpt data/dagger_tape/season_fast-20260822-235031/pinned_round27.pkl \
        --vocab data/il/bundle_vocab_teacher_pre_topup.json

THE QUESTION THIS SEPARATES
---------------------------
Warm-starting `train_jax_rl.py` from `pinned_round27.pkl` produced a policy banking a MEDIAN OF $7
against a $3,000 start, nooping 61% of turns (`data/logs/rl_smoke.log`, 2026-08-28). The same
checkpoint reproduces its teacher to $126k-$150k on the four tapes. Two explanations fit, and they
have opposite fixes:

  A. **Sampling.** The $126k is an argmax property. PPO explores by sampling, and at the smoke's
     74.8 nats a sampled draw is nowhere near the argmax over 719 turns x 12 units.
     -> the levers are --ent-coef, --kl-coef, --lr. The run is worth having.

  B. **The observation bridge.** The clone was trained and measured on features built by
     `adapter.state_from_obs` from the REFERENCE env. Training feeds it a native `jax_sim.State`.
     If those two produce different tensors the clone is looking at a different game.
     -> no RL setting fixes it, and the 300/300 sim parity gate does not cover it: parity tests the
        SIMULATOR against the reference, not the ENCODER's two entry points.

Greedy decode in `jax_sim` tells them apart. Near the teacher's money means A. Near $7 means B.

**The vocabulary is pinned and asserted.** `market_bundles.load_vocab` defaults to the 197-entry
`bundle_vocab.json`; this checkpoint records `vocab_size=149` while naming
`bundle_vocab_teacher.json`, which is 151. Bundle index 50 is a different basket in each and nothing
offline shows it -- every index is still a valid index. `load_vocab` is patched rather than having
`DEFAULT_VOCAB` reassigned, because the default is bound at definition time.
"""
import argparse
import json
import pathlib
import pickle
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--vocab", required=True)
    ap.add_argument("--games", type=int, default=16)
    ap.add_argument("--horizon", type=int, default=719)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    with open(args.ckpt, "rb") as fh:
        ckpt = pickle.load(fh)
    want = ckpt.get("vocab_size")
    bundles = json.loads(pathlib.Path(args.vocab).read_text())
    if want is not None and len(bundles) != want:
        raise SystemExit(f"vocab {args.vocab} has {len(bundles)} entries, checkpoint wants {want}. "
                         f"Every bundle index above the first insertion means a different basket.")

    import jax
    import jax.numpy as jnp
    from kagg.il import market_bundles as MB

    pinned = MB.Vocabulary.from_bundles([tuple(tuple(p) for p in b) for b in bundles],
                                        max_size=None)
    _real = MB.load_vocab
    MB.load_vocab = lambda *a, **k: pinned          # noqa: E731 -- before any bundle is read

    from kagg.rl import commit as CM, jax_act as A, jax_obs, jax_policy as P
    from kagg.sim import jax_sim as J

    cargs = ckpt.get("args") or {}
    model = P.Policy(d_model=cargs.get("d_model", 128), n_heads=cargs.get("heads", 4),
                     n_layers=cargs.get("layers", 3))
    params = ckpt["params"]
    bundle_ok = jnp.asarray(MB.valid_table(pinned, pad_to=P.N_BUNDLES))
    # `pad_to` must be the HEAD width, not the vocab size: JAX clamps an out-of-range gather under
    # jit, so a 149-row table indexed at 200 would silently return row 148 -- a confidently emitted
    # wrong order (`market_bundles.tables`).
    tables = {k: jnp.asarray(v) for k, v in MB.tables(pinned, pad_to=P.N_BUNDLES).items()}

    print(f"ckpt {args.ckpt} round {ckpt.get('round')}")
    print(f"vocab {args.vocab} -> {len(bundles)} bundles (checkpoint wants {want})")
    print(f"{args.games} games, {args.horizon} turns, GREEDY (argmax over legal)")

    state = J.reset_with_shops(args.games, seed=args.seed)
    # **The commit layer is part of the action semantics, not an optimisation.** `train_jax_rl`
    # overrides `to_sim_actions`' unit ops with `CM.resolve` (`train_jax_rl.py:515-518`): a policy op
    # may be a `COMMIT_*` token, and a unit already walking ignores the policy entirely. Running the
    # control without it would decode the same logits into different ops, so a low bank here would
    # not be evidence about the thing training does.
    cmt = CM.init(args.games)

    for t in range(args.horizon):
        tiles, units, glob = jax_obs.encode(state)
        heads, _v = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
        masks = A.masks_for(state, bundle_ok)
        cond = {k: jnp.argmax(P._masked_logits(heads[k], masks[k]), axis=-1)
                for k in A.CONDITION_HEADS}
        conditioned = A.condition_all(heads, cond)
        act = {k: jnp.argmax(P._masked_logits(conditioned[k], masks[k]), axis=-1)
               for k in A.ALL_HEADS}

        u32 = lambda k: A._unflat(act[k], args.games).astype(jnp.int32)   # noqa: E731
        sim_op, sim_crop, sim_item, sim_qty, cmt, _decided = CM.resolve(
            cmt, state, u32("op"), u32("crop"), u32("item"), u32("qty"))
        sim_actions = A.to_sim_actions(act, args.games, tables)._replace(
            unit_op=sim_op.astype(J._I), unit_crop=sim_crop.astype(J._I),
            unit_item=sim_item.astype(J._I), unit_qty=sim_qty.astype(J._I))
        state = J.step(state, sim_actions)
        cmt = CM.clear_at_night(cmt, state)
        if t % 120 == 0:
            m = np.asarray(state.farm.money)[:, 0]
            print(f"  turn {t:>3} day {t // 24:>2}  bank med ${np.median(m):>10,.0f}  "
                  f"max ${m.max():>10,.0f}", flush=True)

    money = np.asarray(state.farm.money)
    own = money[:, 0]
    print(f"\nFINAL seat 0 bank over {args.games} games")
    print(f"  median ${np.median(own):,.0f}   mean ${own.mean():,.0f}   "
          f"min ${own.min():,.0f}   max ${own.max():,.0f}")
    print(f"  starting money was $3,000")
    print("\nVERDICT")
    if np.median(own) > 40_000:
        print("  A -- the clone plays in jax_sim. The $7 was SAMPLING. Levers: ent-coef/kl/lr.")
    elif np.median(own) < 5_000:
        print("  B -- the clone does NOT play in jax_sim under argmax either. The observation "
              "bridge is the suspect, and no RL setting fixes that.")
    else:
        print("  neither cleanly -- report the number, do not pick a story.")

    MB.load_vocab = _real


main()
