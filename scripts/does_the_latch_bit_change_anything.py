"""Flip the latch bit on a fixed board. If the action does not change, the latch was never learned.

    python -u scripts/does_the_latch_bit_change_anything.py --ckpt <path>

THE QUESTION THIS SETTLES
-------------------------
The clone scores `greedy op 1.0000` on the sixteen training towns and the run holds **0 held out**.
That number is consistent with two completely different things:

    learned    it reads `melon_armed` / `q4_armed` from `glob` and branches on them.
    memorised  it identifies the episode from the clock one-hots and the prices -- both of which are
               in the observation -- and replays "on this board at turn 264, do X". No latch needed.

Agreement cannot separate them, and neither can a season total. Only intervening on the bit can.

WHAT IT DOES
------------
Take a real board past the latch day, encode it once, then re-encode with ONLY the latch column
changed and compare the greedy action. Everything else -- tiles, units, clock, prices, opponent
snapshot -- is held identical, so any difference in output is caused by the bit and nothing else.

    action changes    the policy is reading the latch. It may still be wrong about what to do with
                      it, but the wiring is live.
    action identical  the bit is inert. The policy is keyed on something else, and it will not
                      transfer to a town where that something else differs.

**The raw melon count is flipped too, in the same direction.** `glob` carries both the stated bit
and the day-3 snapshot the bit is derived from, so moving only the bit leaves a contradictory
observation the net has never seen -- and "no change" there would be ambiguous between "ignores the
bit" and "trusts the count instead". Both are moved so the two agree.
"""
import argparse
import pathlib
import pickle
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--run", required=True, help="run dir holding aggregate.pkl")
    ap.add_argument("--min-turn", type=int, default=96, help="only turns past the melon latch (d4+)")
    ap.add_argument("--rows", type=int, default=400)
    args = ap.parse_args()

    import importlib.util

    import jax.numpy as jnp

    from kagg.rl import jax_obs, jax_policy as P

    spec = importlib.util.spec_from_file_location("dagger_tape", REPO / "scripts/dagger_tape.py")
    DT = importlib.util.module_from_spec(spec)
    sys.modules["dagger_tape"] = DT
    spec.loader.exec_module(DT)

    ck = pickle.load(open(args.ckpt, "rb"))
    a = ck.get("args") or {}
    model = P.Policy(d_model=int(a.get("d_model", 128)), n_heads=int(a.get("heads", 4)),
                     n_layers=int(a.get("layers", 3)))
    params = ck["params"]

    agg = pickle.load(open(pathlib.Path(args.run) / "aggregate.pkl", "rb"))
    rows = [r for r in (list(agg.get("expert", [])) + list(agg.get("student", [])))
            if int(r.get("turn", 0)) >= args.min_turn]
    rng = np.random.default_rng(0)
    rows = [rows[i] for i in rng.choice(len(rows), min(args.rows, len(rows)), replace=False)]

    # Column offsets, from `jax_obs`: the memory block is appended at the END of `glob`.
    #   [ ... opponent(14) | snapshot(3 x 17) | shop_age(8) | melon_armed(1) | q4_armed(1) ]
    G = jax_obs.GLOBAL_FEATURES
    MELON_BIT, Q4_BIT = G - 2, G - 1
    snap_w = jax_obs.SNAPSHOT_WIDTH if hasattr(jax_obs, "SNAPSHOT_WIDTH") else 17
    snap0 = G - 2 - jax_obs._SHOP_DATE_WIDTH - jax_obs._SNAPSHOT_WIDTH
    melon_day = jax_obs.SNAPSHOT_DAYS.index(jax_obs.MELON_LATCH_DAY) if hasattr(
        jax_obs, "SNAPSHOT_DAYS") else 1
    melon_col = snap0 + melon_day * snap_w + 6 + jax_obs.CROP_INDEX_MELON

    print("ckpt %s   rows %d (turn >= %d)" % (args.ckpt, len(rows), args.min_turn), flush=True)
    print("glob width %d   melon_bit col %d   q4_bit col %d   melon_count col %d\n"
          % (G, MELON_BIT, Q4_BIT, melon_col), flush=True)

    batch = DT.stack(rows, DT.bundle_class_weights(rows, 1.0))
    tiles, units, glob = batch["obs"]
    glob = np.array(glob)

    def greedy(g):
        heads, _v = model.apply(params, tiles, units, jnp.asarray(g))
        picks = DT.greedy_action(heads, batch["masks"])
        return {k: np.asarray(v) for k, v in picks.items()}

    base = greedy(glob)

    for name, bit_col, count_col in (("melon", MELON_BIT, melon_col), ("q4", Q4_BIT, None)):
        flipped = glob.copy()
        cur = flipped[:, bit_col]
        flipped[:, bit_col] = 1.0 - cur
        if count_col is not None:
            # Move the raw count with the bit so the observation stays self-consistent: above the
            # threshold when armed, below it when not. Scale matches `_SNAPSHOT_SCALE` (crops / 100).
            hi = (jax_obs.OPPONENT_MELON + 3) / 100.0
            flipped[:, count_col] = np.where(flipped[:, bit_col] > 0.5, hi, 0.0)

        alt = greedy(flipped)
        changed = {}
        for k in ("op", "bundle", "crop", "item", "qty"):
            if k not in base:
                continue
            d = np.asarray(base[k]) != np.asarray(alt[k])
            changed[k] = (int(d.sum()), int(d.size))

        total = sum(c for c, _n in changed.values())
        print("FLIP %s bit  ->  %s" % (name.upper(),
                                       "ACTION CHANGES" if total else "NO CHANGE AT ALL"), flush=True)
        for k, (c, n) in changed.items():
            print("    %-8s %6d of %6d differ  (%.2f%%)" % (k, c, n, 100.0 * c / max(1, n)),
                  flush=True)
        print(flush=True)

    print("READ IT", flush=True)
    print("  changes      the policy reads the latch; the wiring is live.", flush=True)
    print("  no change    the bit is inert -- it keyed on the clock and the board instead, and", flush=True)
    print("               1.0 agreement on 16 towns is memorisation, not a learned branch.", flush=True)


if __name__ == "__main__":
    main()
