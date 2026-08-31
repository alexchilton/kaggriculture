"""Train the frozen aggregate for N epochs and watch whether movement agreement leaves 0.000.

    python -u scripts/does_movement_ever_leave_zero.py --run data/dagger_tape/<run> --epochs 50

THE QUESTION, AND WHY IT IS CHEAP
---------------------------------
Two DAgger runs reported movement at exactly 0.000 over 45,485 labels and were read as a collapse.
Then the checkpoint's own metadata said `round: 1, init: None` -- a **cold start, ~56 Adam steps**
at lr 1e-4 on a zero-init 966k net, because every run dies at the end of round 1 on the
`bundle_miss` guard (`dagger_tape.py:984`). "Collapsed" and "barely trained" produce identical
tables, and they want opposite responses.

A full DAgger round costs ~58 minutes, almost all of it rollout. But the aggregate rows already hold
`obs`, `masks`, `labels` and `unit_live` -- everything the loss and the greedy decode need. So the
optimisation question can be answered with **no environment, no rollout and no teacher**: fit the
stored rows and watch the per-op numbers.

    movement leaves 0.000    it was undertrained. Raise `--epochs` in the live run (it uses 1) and
                             fix the vocab guard so rounds accumulate.
    movement stays 0.000     something structural survives, and the commit-token relabel in
    while the loss falls     `docs/fable_movement_collapse_2026-08-28.md` becomes the next move.

WHAT IS REUSED, DELIBERATELY
----------------------------
`bc_dagger.make_step`'s `fit` and `dagger_tape.stack` / `bundle_class_weights`, imported rather than
reimplemented. A second copy of the loss would answer a different question than the one the training
run asks, and this file exists precisely to be compared against that run.

Agreement here is measured on the SAME rows being fitted, so it is a training-set number and says
nothing about generalisation. That is the right scope: the question is whether the objective can
express movement at all, not whether it transfers.
"""
import argparse
import collections
import importlib.util
import pathlib
import pickle
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="a dagger run dir holding latest.pkl + aggregate.pkl")
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--every", type=int, default=5)
    ap.add_argument("--batch-turns", type=int, default=512)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--bundle-alpha", type=float, default=1.0)
    ap.add_argument("--score-rows", type=int, default=2048, help="rows scored for agreement")
    ap.add_argument("--target", type=float, default=1.0,
                    help="stop as soon as scored overall agreement reaches this. The teacher is a "
                         "fixed schedule, so 1.0 is attainable and is the actual goal.")
    ap.add_argument("--patience", type=int, default=4,
                    help="stop if the best scored agreement has not improved for this many "
                         "scoring checks (a check every --every epochs). 0 disables.")
    ap.add_argument("--resume", action="store_true",
                    help="restart from offline_latest.pkl in the run dir: params, optimiser "
                         "state, epoch counter and the shuffle RNG. Refuses if the checkpoint "
                         "was written by a different model shape.")
    args = ap.parse_args()

    import jax
    import jax.numpy as jnp
    import optax

    from kagg.il import market_bundles as MB, replays as RP
    from kagg.rl import jax_policy as P

    DT = _load("dagger_tape", REPO / "scripts/dagger_tape.py")
    BD = _load("bc_dagger", REPO / "scripts/bc_dagger.py")

    run = pathlib.Path(args.run)
    ck = pickle.load(open(run / "latest.pkl", "rb"))
    agg = pickle.load(open(run / "aggregate.pkl", "rb"))
    rows = list(agg.get("expert", [])) + list(agg.get("student", []))
    a = ck.get("args") or {}
    print("run    %s" % run, flush=True)
    print("rows   %d expert + %d student   round %s   init %s"
          % (len(agg.get("expert", [])), len(agg.get("student", [])), ck.get("round"), a.get("init")),
          flush=True)

    model = P.Policy(d_model=int(a.get("d_model", 128)), n_heads=int(a.get("heads", 4)),
                     n_layers=int(a.get("layers", 3)))
    params = ck["params"]
    optimiser = optax.chain(optax.clip_by_global_norm(0.5), optax.adam(args.lr))
    opt_state = optimiser.init(params)

    vocab = MB.load_vocab(str(ck.get("vocab_path") or a.get("vocab")))
    bundle_ok = MB.valid_table(vocab, pad_to=P.N_BUNDLES)
    # Built exactly as `dagger_tape.py:667` builds it. `loss_fn` indexes `tables` by column name to
    # decide which heads a bundle activates, so `None` is not a permissive default -- it raises.
    tables = {k: jnp.asarray(v) for k, v in MB.tables(vocab, pad_to=P.N_BUNDLES).items()}
    _rollout, fit, _evaluate = BD.make_step(model, None, 1, 719, optimiser, 0.0, tables, bundle_ok)

    class_w = DT.bundle_class_weights(rows, args.bundle_alpha)
    OP_NAME = {v: k for k, v in RP.OP_CODE.items()}
    MOVES = ("NORTH", "SOUTH", "EAST", "WEST")

    def agreement(params, sample):
        """Greedy masked op argmax against the stored labels, per teacher op. No env."""
        seen, hit = collections.Counter(), collections.Counter()
        for start in range(0, len(sample), 256):
            chunk = sample[start:start + 256]
            batch = DT.stack(chunk, class_w)
            # `stack` hands the observation over as a 3-tuple `(tiles, units, glob)`, already
            # network-flat -- not as three named keys.
            heads, _v = model.apply(params, *batch["obs"])
            pick = np.asarray(jnp.argmax(
                jnp.where(batch["masks"]["op"], heads["op"], -jnp.inf), axis=-1))
            lab = np.asarray(batch["labels"]["op"])
            live = np.asarray(batch["unit_live"]).astype(bool)
            for i in range(len(chunk)):
                for u in np.flatnonzero(live[i]):
                    n = OP_NAME.get(int(lab[i, u]), str(int(lab[i, u])))
                    seen[n] += 1
                    hit[n] += int(pick[i, u] == lab[i, u])
        return seen, hit

    def latch_report(params):
        """Has it learned the LATCHES -- the only two bits of the teacher that are not fixed?

        The 16 episodes are 4 tapes x 4 town draws, and each tape IS a latch combination:
        `(melon_armed, q4_armed)` from the opponent's melon count at d3 and a yarn store by d5.
        The teacher plays a different season on each arm.

        Split by day band, because the latches fire at known moments:

            d0-d3    before either latch. All four arms are the SAME teacher, so high agreement
                     here says nothing about latching -- it is the shared opening.
            d4-d11   after the melon latch (d3). The melon and strawberry arms diverge here.
            d12+     after the q4 latch, whose route table starts at d12.

        **The tell is the SHAPE, not the level.** If d0-d3 is high and d4+ collapses on the arms
        this episode is not, the student has learned one season and is playing it everywhere -- it
        has not learned to read the latch. If all four arms hold up after d4, it has.
        """
        TPD_ = 24
        BANDS = (("d0-d3", 0, 4), ("d4-d11", 4, 12), ("d12+", 12, 99))
        by = collections.defaultdict(lambda: [0, 0])
        for start in range(0, len(rows), 256):
            chunk = rows[start:start + 256]
            batch = DT.stack(chunk, class_w)
            heads, _v = model.apply(params, *batch["obs"])
            pick = np.asarray(jnp.argmax(
                jnp.where(batch["masks"]["op"], heads["op"], -jnp.inf), axis=-1))
            lab = np.asarray(batch["labels"]["op"])
            live = np.asarray(batch["unit_live"]).astype(bool)
            for i, r in enumerate(chunk):
                day = int(r.get("turn", 0)) // TPD_
                band = next((b for b, lo, hi in BANDS if lo <= day < hi), None)
                if band is None:
                    continue
                tape = str(r.get("ep"))[:30]
                for u in np.flatnonzero(live[i]):
                    by[(tape, band)][0] += 1
                    by[(tape, band)][1] += int(pick[i, u] == lab[i, u])

        tapes = sorted({k[0] for k in by})
        print("\nHAS IT LEARNED THE LATCH  (unit-op agreement per episode x day band)", flush=True)
        print("  %-32s %10s %10s %10s" % ("episode", *[b for b, _l, _h in BANDS]), flush=True)
        for t in tapes:
            cells = []
            for b, _lo, _hi in BANDS:
                n, h = by[(t, b)]
                cells.append("%.3f" % (h / n) if n else "   -  ")
            print("  %-32s %10s %10s %10s" % (t, *cells), flush=True)
        print("  d0-d3 high everywhere is the SHARED opening, not latching. The question is whether",
              flush=True)
        print("  d4-d11 and d12+ hold up on every arm, or only on one.", flush=True)

    rng = np.random.default_rng(0)
    sample = [rows[i] for i in rng.choice(len(rows), min(args.score_rows, len(rows)), replace=False)]

    def report(tag, params):
        seen, hit = agreement(params, sample)
        tot = sum(seen.values()) or 1
        overall = sum(hit.values()) / tot
        mv_seen = sum(seen[m] for m in MOVES)
        mv_hit = sum(hit[m] for m in MOVES)
        print("%-10s overall %.4f  |  MOVEMENT %.4f (%d/%d)  |  %s"
              % (tag, overall, mv_hit / max(1, mv_seen), mv_hit, mv_seen,
                 "  ".join("%s %.3f" % (m, hit[m] / max(1, seen[m])) for m in MOVES)), flush=True)
        return overall

    def opening_report(params):
        """d0-d3 agreement per DAY and per EPISODE -- the opening, before either latch fires.

        **The average cannot see this.** The opening is 96 of 719 turns and it is the part every
        later day is conditioned on: the five HIREs, the animals and the seed. A whole-season number
        of 0.66 is consistent with a perfect opening and with a broken one.

        Broken out by episode because the 16 rows are 4 tapes x 4 town draws: if the opening only
        holds on the recorded seed and not the three fresh ones, that is memorisation of a town, and
        it will not survive the ladder.
        """
        TPD_ = 24
        by = collections.defaultdict(lambda: [0, 0])
        for start in range(0, len(rows), 256):
            chunk = rows[start:start + 256]
            chunk = [r for r in chunk if int(r.get("turn", 9999)) < 4 * TPD_]
            if not chunk:
                continue
            batch = DT.stack(chunk, class_w)
            heads, _v = model.apply(params, *batch["obs"])
            pick = np.asarray(jnp.argmax(
                jnp.where(batch["masks"]["op"], heads["op"], -jnp.inf), axis=-1))
            lab = np.asarray(batch["labels"]["op"])
            live = np.asarray(batch["unit_live"]).astype(bool)
            for i, r in enumerate(chunk):
                day = int(r.get("turn", 0)) // TPD_
                ep = r.get("ep")
                for u in np.flatnonzero(live[i]):
                    for key in (("day", day), ("ep", ep)):
                        by[key][0] += 1
                        by[key][1] += int(pick[i, u] == lab[i, u])

        print("\nOPENING d0-d3, unit-op agreement (the 96 turns every later day inherits)",
              flush=True)
        for d in range(4):
            n, h = by[("day", d)]
            if n:
                print("  day %d   %.4f  (%d/%d)" % (d, h / n, h, n), flush=True)
        print("  per episode (tape x town draw):", flush=True)
        for k in sorted((k for k in by if k[0] == "ep"), key=lambda k: str(k[1])):
            n, h = by[k]
            if n:
                print("    %-34s %.4f  (%d/%d)" % (str(k[1])[:34], h / n, h, n), flush=True)

    # A 400-epoch fit is ~4 hours, and writing the weights only at the end means a crash at epoch
    # 399 costs all of it. `offline_latest.pkl` is rewritten every `--every` epochs and carries the
    # optimiser state and the shuffle RNG as well as the params -- restoring params alone would
    # resume with a fresh Adam moment estimate and a re-run epoch order, which is a different run.
    latest = run / "offline_latest.pkl"
    shape = {"d_model": int(a.get("d_model", 128)), "heads": int(a.get("heads", 4)),
             "layers": int(a.get("layers", 3)), "rows": len(rows)}

    # **`vocab_size` and the three feature widths are not optional bookkeeping.**
    # `dagger_tape.py:725` reads `ckpt.get("vocab_size")` and treats a MISSING value as "different",
    # by design -- an unrecorded vocabulary cannot be shown to match. Omitting it makes the next
    # `--init` reset the bundle head to random and print one line saying so. That happened on
    # 2026-08-31 at 08:30 and threw away a market head fitted to 0.99516. The widths feed the
    # migration message the same way.
    provenance = {"vocab_size": vocab.size,
                  "tile_features": jax_obs.TILE_FEATURES,
                  "unit_features": jax_obs.UNIT_FEATURES,
                  "global_features": jax_obs.GLOBAL_FEATURES}

    def save(path, epoch, p, o=None):
        tmp = path.with_suffix(".pkl.tmp")
        with open(tmp, "wb") as f:
            pickle.dump({"params": p, "opt_state": o, "epoch": epoch,
                         "rng_state": rng.bit_generator.state, "shape": shape,
                         "args": a, "vocab": ck.get("vocab"),
                         "vocab_path": ck.get("vocab_path"), "round": ck.get("round"),
                         "offline_epochs": epoch, **provenance}, f)
        tmp.replace(path)  # atomic: a kill mid-write must not leave a truncated checkpoint

    start_epoch = 0
    if args.resume:
        if not latest.exists():
            raise SystemExit("--resume: no %s. Drop --resume to start from latest.pkl." % latest)
        prev = pickle.load(open(latest, "rb"))
        if prev.get("shape") != shape:
            raise SystemExit("--resume refused: checkpoint shape %s, this run %s. Loading across a "
                             "shape change gives garbage, not a warm start."
                             % (prev.get("shape"), shape))
        params, opt_state = prev["params"], prev["opt_state"]
        start_epoch = int(prev["epoch"])
        rng.bit_generator.state = prev["rng_state"]
        print("RESUMED %s   epoch %d/%d   optimiser state and shuffle RNG restored"
              % (latest, start_epoch, args.epochs), flush=True)

    # **Keep the BEST scored params, not the last.** Measured on this very run: epoch 50 scored
    # overall 1.0000 and epoch 75 fell back to 0.9999. Saving only the final epoch ships whichever
    # point the loop happened to stop on, which is not the same thing as the best fit.
    best_score, best_params, best_epoch, stale = report("epoch %d" % start_epoch, params), params, \
        start_epoch, 0

    base = np.arange(len(rows))
    stopped = None
    for ep in range(start_epoch + 1, args.epochs + 1):
        order = base.copy()
        rng.shuffle(order)
        losses = []
        for start in range(0, len(order), args.batch_turns):
            chunk = [rows[i] for i in order[start:start + args.batch_turns]]
            if not chunk:
                continue
            params, opt_state, loss, _ph = fit(params, opt_state, DT.stack(chunk, class_w))
            losses.append(float(loss))
        if ep % args.every == 0 or ep == args.epochs:
            print("epoch %-3d loss %.4f" % (ep, float(np.mean(losses))), flush=True)
            score = report("  ->", params)
            save(latest, ep, params, opt_state)
            if score > best_score:
                best_score, best_params, best_epoch, stale = score, params, ep, 0
                save(run / "offline_best.pkl", ep, params)
            else:
                stale += 1
            print("  ckpt   %s   best %.4f @ epoch %d" % (latest, best_score, best_epoch),
                  flush=True)
            if score >= args.target:
                stopped = "target %.4f reached at epoch %d" % (args.target, ep)
                break
            if args.patience and stale >= args.patience:
                stopped = ("no improvement on %d checks; best %.4f @ epoch %d"
                           % (stale, best_score, best_epoch))
                break

    print("\nEARLY STOP  %s" % (stopped or "not triggered; ran the full %d epochs" % args.epochs),
          flush=True)
    params = best_params
    print("reporting and saving the BEST params: %.4f @ epoch %d" % (best_score, best_epoch),
          flush=True)

    opening_report(params)
    latch_report(params)

    # Parenthesised: `%` binds tighter than `/`, so the unbracketed form applies `%` to the Path.
    # That crashed AFTER a 15-minute fit and threw the weights away, twice.
    # Named for the epoch the weights are actually FROM, not for `--epochs` -- early stopping means
    # those two differ, and a file called `400epochs` holding epoch-50 weights is a trap.
    out = run / ("offline_%depochs.pkl" % best_epoch)
    with open(out, "wb") as f:
        pickle.dump({"params": params, "args": a, "vocab": ck.get("vocab"),
                     "vocab_path": ck.get("vocab_path"), "round": ck.get("round"),
                     "offline_epochs": best_epoch, "epoch": best_epoch, **provenance}, f)
    print("\nwrote %s" % out, flush=True)

    print("\nREAD IT", flush=True)
    print("  MOVEMENT climbs off 0.000   undertrained, not collapsed. Raise --epochs in the run.", flush=True)
    print("  MOVEMENT pinned at 0.000    structural; see docs/fable_movement_collapse_2026-08-28.md", flush=True)
    print("  while loss keeps falling    fix 4, the commit-token relabel.", flush=True)


if __name__ == "__main__":
    main()
