"""Print what the bundle head actually emits, turn by turn, in a real game.

    python -u scripts/what_does_the_bundle_head_do_on_a_real_turn.py \
        --ckpt data/bc_runs/bcr_kawa_v2-20260828-094747/latest.pkl --seed 9000 --turns 240

WHY THIS EXISTS
---------------
Two facts that cannot both be acted on by guessing:

    offline, on rows where the teacher traded   top-1 basket 86.7%, mean P(true) 75.8%
    in play, planner drives the units           9-39 market orders in 719 turns

Two hypotheses have already been wrong today. The decode was blamed -- `mean P(EMPTY)` is 2.6%, so
there was no mass on EMPTY to reclaim. Covariate shift was blamed -- the start board is FIXED across
every game, and it was asserted without measurement. A third guess is not worth making.

So this stops inferring and prints the quantity. Per turn:

    argmax          which bundle the head picks AFTER masking -- what actually gets played
    p_top           its probability, so "confident and wrong" is distinguishable from "flat"
    unmasked        which bundle it would pick with no mask at all
    killed          whether the mask removed the unmasked first choice. THIS is the number that
                    says the mask is the problem rather than the head.
    p_empty         mass on index 0

A masking failure and a head failure look identical from the outside -- both emit nothing -- and
they have opposite fixes, so the two columns that separate them are `unmasked` and `killed`.
"""
import argparse
import collections
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

EMPTY_INDEX = 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--seed", type=int, default=9000)
    ap.add_argument("--turns", type=int, default=240)
    ap.add_argument("--show", type=int, default=24, help="how many turns to print in full")
    args = ap.parse_args()

    import jax.numpy as jnp
    from kaggle_environments import make

    from kagg.agents import neural as NEURAL
    from kagg.rl import adapter as AD, jax_act as A, jax_obs, jax_policy as P
    from kagg.search import schedule_agent as SA

    # The planner arm: play all 30 days from the target rows rather than replaying a tape.
    SA.REPLAY_OPENING_DAYS = ()

    model, params, vocab = NEURAL.load_for_probe(args.ckpt) if hasattr(NEURAL, "load_for_probe") \
        else (None, None, None)
    if model is None:                                   # no probe helper; rebuild it here
        import pickle

        import jax
        ck = pickle.load(open(args.ckpt, "rb"))
        from kagg.il import market_bundles as MB
        raw = ck.get("vocab")
        vocab = MB.Vocabulary([tuple(tuple(p) for p in b) for b in raw])
        a = ck.get("args") or {}
        model = P.Policy(d_model=a.get("d_model", 128), n_heads=a.get("heads", 4),
                         n_layers=a.get("layers", 3))
        # **Migrate, do not load raw.** `glob` is 183 wide since the latch/snapshot features landed
        # and this checkpoint is 122. `jax_policy.migrate_params` zero-pads the grown rows of the
        # input projection, which is exactly what `neural.make_agent` does -- so this probe sees the
        # same weights the hybrid harness plays, rather than crashing on the width.
        import numpy as _np
        probe = jax.random.PRNGKey(0)
        _t = jnp.zeros((1, jax_obs.TILE_FEATURES * 0 + 100, jax_obs.TILE_FEATURES), jnp.float32)
        _u = jnp.zeros((1, 24, jax_obs.UNIT_FEATURES), jnp.float32)
        _g = jnp.zeros((1, jax_obs.GLOBAL_FEATURES), jnp.float32)
        template = model.init(probe, _t, _u, _g)
        params = jax.tree_util.tree_map(jnp.asarray, P.load_or_migrate(ck["params"], template))

    bundle_ok = NEURAL._bundle_sells(vocab)
    # Which vocabulary entries contain a SELL at all. The question is not only "what did it pick"
    # but "how much mass does it put on selling anything", and whether there was anything TO sell.
    sell_idx = [i for i in range(vocab.size)
                if any(o and o[0] == "SELL" for o in vocab.bundle(i))]
    print(f"{len(sell_idx)} of {vocab.size} bundles contain a SELL")
    print(f"ckpt   {args.ckpt}")
    print(f"vocab  {vocab.size} bundles   seed {args.seed}   {args.turns} turns\n", flush=True)

    env = make("kaggriculture",
               configuration={"seed": args.seed, "weedSpawnChance": 0.0}, debug=False)
    env.reset(2)
    # The same planner construction the hybrid harness uses: `TapeTeacher` on seat 0 with
    # `REPLAY_OPENING_DAYS` emptied, so the states here are exactly the states the hybrid visits.
    from kagg.il.tape_teacher import TapeTeacher
    planner = TapeTeacher(0)
    memo = AD.GameMemo()

    rows, killed_n, traded_n = [], 0, 0
    legal_counts = []
    for turn in range(args.turns):
        if env.done:
            break
        obs = env.state[0].observation
        memo.observe(obs, step=turn)
        privates = [obs["private"] if p == 0 else AD.agent_private_stub() for p in range(2)]
        state = AD.state_from_obs(obs, privates, step=turn, memo=memo)
        tiles, units, glob = jax_obs.encode(state)
        heads, _v = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
        masks = A.masks_for(state, bundle_ok)

        raw = np.asarray(heads["bundle"])[0]
        m = np.asarray(masks["bundle"])[0]
        legal_counts.append(int(m.sum()))
        masked = np.where(m, raw, -np.inf)
        pr = np.exp(raw - raw.max())
        pr /= pr.sum()
        unmasked_top = int(raw.argmax())
        top = int(masked.argmax())
        was_killed = (unmasked_top != EMPTY_INDEX) and not bool(m[unmasked_top])
        killed_n += was_killed
        traded_n += top != EMPTY_INDEX
        shed = dict((obs.get("private") or {}).get("shed") or {})
        shed_n = sum(int(v or 0) for v in shed.values())
        p_sell = float(pr[sell_idx].sum())
        rows.append((turn, top, float(pr[top]), unmasked_top, float(pr[unmasked_top]),
                     was_killed, float(pr[EMPTY_INDEX]), int(m.sum()), shed_n, p_sell,
                     ",".join(f"{k}:{v}" for k, v in sorted(shed.items()) if v)))

        # Let the planner drive the game forward, so the states are the ones the hybrid visits.
        n_units = 1 + len(obs["farms"][0].get("hands") or [])
        act = planner.sendable(planner.act(obs), n_units)
        opp = {"farmer": ["PASS"], "hands": [], "market": []}
        env.step([act, opp])

    print(f"{'turn':>5} {'argmax':>7} {'p_empty':>8} {'P(sell)':>8} {'shed':>6}  shed contents")
    # Print the turns where there was actually something to sell -- an empty shed makes the head's
    # silence correct and says nothing.
    stocked = [r for r in rows if r[8] > 0]
    for r in stocked[:args.show]:
        print(f"{r[0]:>5} {r[1]:>7} {r[6]:>8.3f} {r[9]:>8.3f} {r[8]:>6}  {r[10][:60]}")
    if not stocked:
        print("  (the shed was empty on every turn -- the planner put nothing in it)")

    n = len(rows)
    print(f"\nover {n} turns")
    print(f"  turns the head would trade UNMASKED   {sum(1 for r in rows if r[3] != EMPTY_INDEX):>5}"
          f"  ({sum(1 for r in rows if r[3] != EMPTY_INDEX) / max(1, n):.1%})")
    print(f"  turns it trades AFTER masking         {traded_n:>5}  ({traded_n / max(1, n):.1%})")
    print(f"  mask killed the first choice          {killed_n:>5}  ({killed_n / max(1, n):.1%})")
    print(f"  mean legal bundles per turn           {np.mean(legal_counts):>7.1f} of {vocab.size}")
    print(f"  mean P(EMPTY)                         {np.mean([r[6] for r in rows]):>7.3f}")
    print(f"  turns with ANYTHING in the shed       {len(stocked):>5}  "
          f"({len(stocked) / max(1, n):.1%})")
    if stocked:
        print(f"  mean P(any SELL) when shed is stocked {np.mean([r[9] for r in stocked]):>7.3f}")
        print(f"  max  P(any SELL) when shed is stocked {max(r[9] for r in stocked):>7.3f}")
        print(f"  mean P(EMPTY)     when shed is stocked {np.mean([r[6] for r in stocked]):>7.3f}")
        print(f"  peak shed size                        {max(r[8] for r in stocked):>7}")

    top_choices = collections.Counter(r[3] for r in rows)
    print("\n  most-wanted bundles (unmasked argmax):")
    for b, c in top_choices.most_common(6):
        print(f"    {b:>4} x{c:<5} {list(vocab.bundle(b))[:4]}")

    print("\nREAD IT LIKE THIS")
    print("  unmasked HIGH, after-masking LOW    the mask is the bug -- the head wants to trade.")
    print("  unmasked LOW too                    the head itself emits EMPTY on these states,")
    print("                                      and the 86.7% offline is measured elsewhere.")


main()
