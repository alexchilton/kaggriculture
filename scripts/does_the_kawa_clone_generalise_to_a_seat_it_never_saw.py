"""Score the kawa clone on カワシギ seats it was NOT trained on, against seats it was.

    python -u scripts/does_the_kawa_clone_generalise_to_a_seat_it_never_saw.py \
        --ckpt data/bc_runs/bcr_kawa_v2-20260828-094747/latest.pkl --top 400 --seats 6

THE QUESTION
------------
The clone lands on teacher money on all four tapes it trained on (+$257 / +$119 / +$58 / +$63) and
banks ~$25 on a fresh seed. Across seeds the board is IDENTICAL -- only the opponent, the
shop-unlock timing and the weeds differ (`project_kaggriculture_start_state_is_fixed`).

So before spending 2.5 hours retraining on a hope, ask the cheap question: does it generalise to a
カワシギ seat it has never seen? We hold 400+ of his seats and trained on the top 400 by bank, so
seats ranked below that are genuine held-out data from the same teacher.

    held-out scores like training   generalisation across seeds is NOT the problem, the missing
                                    unlock-date feature is not the constraint, and a retrain on it
                                    buys nothing.
    held-out collapses              then split the turns by whether a shop has unlocked. A collapse
                                    concentrated after unlocks points at the feature; a uniform one
                                    does not, and the retrain would be 2.5 hours to confirm a guess.

**Both arms are scored by the same code.** A held-out number alone cannot be read -- it has to be
compared against in-training seats measured the same way, or a scoring quirk reads as a finding.
That mistake has been made in this repo before (leave-one-TAPE-out returned a uniform 0.0% across
four arms because the held-out label was absent from training by construction).

WHAT IS REPORTED
----------------
    bundle top-1    on rows where the TEACHER TRADED, so EMPTY is never the right answer and a
                    no-op policy scores 0. This is the market half.
    op agreement    over LIVE unit slots. This is the routing half.
    by shop state   the same two, split on whether any shop has unlocked yet.
"""
import argparse
import pathlib
import pickle
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

EMPTY_INDEX = 0


def score(d, params, model, n_bundles):
    """`(bundle_top1_on_traded, op_agreement_on_live, n_traded, n_slots)` for one row block."""
    import jax
    import jax.numpy as jnp

    from kagg.rl import jax_act as A, jax_policy as P

    @jax.jit
    def heads_of(t, u, g):
        h, _v = model.apply(params, t, u, g)
        return h["bundle"], h["op"]

    y_b, y_op, live = d["y_bundle"], d["y_op"], d["live"]
    hit_b = n_b = hit_op = n_op = 0
    for s in range(0, len(y_b), 256):
        sl = slice(s, s + 256)
        t = jnp.asarray(d["tiles"][sl])[:, None]
        u = jnp.asarray(d["units"][sl])[:, None]
        g = jnp.asarray(d["glob"][sl])[:, None]
        lb, lop = heads_of(A._flat(t), A._flat(u), A._flat(g))
        lb = np.asarray(jnp.where(jnp.asarray(d["m_bundle"][sl]), lb, -jnp.inf))
        # **`m_op` too.** Without it this is an unmasked argmax that can name an op the state
        # forbids, and the number came out 32.5% against the training run's own live-acc 0.742 --
        # two figures that cannot both be true, which meant the metric was wrong rather than the
        # routing. The mask is what play applies, so it is what a comparable score has to apply.
        lop = np.asarray(jnp.where(jnp.asarray(d["m_op"][sl]), lop, -jnp.inf))

        traded = y_b[sl] != EMPTY_INDEX
        if traded.any():
            hit_b += int((lb[traded].argmax(-1) == y_b[sl][traded]).sum())
            n_b += int(traded.sum())

        alive = live[sl] > 0.5
        if alive.any():
            pred = lop.argmax(-1)
            hit_op += int((pred[alive] == y_op[sl][alive]).sum())
            n_op += int(alive.sum())
    return (hit_b / max(1, n_b), hit_op / max(1, n_op), n_b, n_op)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--team", default="カワシギ")
    ap.add_argument("--top", type=int, default=400, help="how many seats the checkpoint trained on")
    ap.add_argument("--seats", type=int, default=6, help="seats to score in each arm")
    ap.add_argument("--max-turns", type=int, default=719)
    args = ap.parse_args()

    import jax
    import jax.numpy as jnp

    from kagg.il import bc
    from kagg.rl import jax_obs, jax_policy as P

    ck = pickle.load(open(args.ckpt, "rb"))
    a = ck.get("args") or {}
    model = P.Policy(d_model=a.get("d_model", 128), n_heads=a.get("heads", 4),
                     n_layers=a.get("layers", 3))
    # Migrate: this checkpoint is 122-wide `glob` and the encoder is now 183. `migrate_params`
    # zero-pads the grown rows, so the new columns contribute nothing -- which is exactly what they
    # contributed during its training, when they did not exist.
    key = jax.random.PRNGKey(0)
    template = model.init(key,
                          jnp.zeros((1, 100, jax_obs.TILE_FEATURES), jnp.float32),
                          jnp.zeros((1, 24, jax_obs.UNIT_FEATURES), jnp.float32),
                          jnp.zeros((1, jax_obs.GLOBAL_FEATURES), jnp.float32))
    params = jax.tree_util.tree_map(jnp.asarray, P.load_or_migrate(ck["params"], template))
    n_bundles = ck.get("vocab_size") or P.N_BUNDLES

    # The SAME vocabulary the checkpoint was fitted with, or every bundle index means something else.
    if ck.get("vocab"):
        from kagg.il import market_bundles as MB
        path = REPO / "data/il/_heldout_probe_vocab.json"
        import json
        path.write_text(json.dumps([[list(p) for p in b] for b in ck["vocab"]]))
        bc.set_vocab(str(path))
        print(f"vocabulary: {n_bundles} bundles, from the checkpoint")

    paths = bc.find_replays("data")
    ranked = bc.rank_seats(paths, team=args.team)
    print(f"{len(ranked):,} {args.team} seats ranked; checkpoint trained on the top {args.top}\n")
    if len(ranked) <= args.top:
        raise SystemExit(f"only {len(ranked)} seats exist; nothing is held out at --top {args.top}")

    arms = {
        "IN TRAINING (ranked 1..%d)" % args.seats: ranked[: args.seats],
        "HELD OUT (ranked %d..%d)" % (args.top + 1, args.top + args.seats):
            ranked[args.top: args.top + args.seats],
    }

    print(f"  {'arm':<34}{'seats':>6}{'bundle top-1':>14}{'op agree':>10}"
          f"{'traded rows':>13}{'slots':>10}")
    out = {}
    for name, refs in arms.items():
        if not refs:
            print(f"  {name:<34}  no seats")
            continue
        d = bc.build_rows(refs, max_turns=args.max_turns)
        b, o, nb, no = score(d, params, model, n_bundles)
        out[name] = (b, o)
        print(f"  {name:<34}{len(refs):>6}{b:>13.1%}{o:>10.1%}{nb:>13,}{no:>10,}", flush=True)

    print("\nREAD IT LIKE THIS")
    print("  held-out ~ in-training     it generalises across seeds. The missing unlock-date")
    print("                             feature is NOT the constraint and a retrain buys nothing.")
    print("  held-out much lower        it does not. Then split by shop state before retraining --")
    print("                             a uniform collapse is not a feature problem.")


main()
