"""How much probability does the clone put on the teacher's action? Not: is the argmax right.

    JAX_PLATFORMS=cpu python -u scripts/how_confident_is_the_clone.py --ckpt <path> --run <dir>

WHY THIS AND NOT AGREEMENT
--------------------------
Every 1.0000 measured on this clone -- 64 trained towns, the latch table, 8 exact held-out towns --
came from a greedy `argmax`. PPO does not argmax. It SAMPLES, and at update 0, before a single
gradient step, the sampled clone banked a median of $16.

Those two facts are not in conflict, and no amount of extra training reconciles them, because they
measure different things:

    agreement    is the argmax the teacher's action?          per decision, forgiving
    confidence   how much mass is ON the teacher's action?    compounds over the season

A season is ~7,000 live unit-decisions. A policy that is right at the argmax with p=0.99 reproduces
the whole season with probability 0.99^7000, which is 1 in 10^30. At p=0.999 it is still 1 in 1,100.
Sampling does not need the argmax to be right; it needs the distribution to be sharp.

WHAT IS PRINTED
---------------
Over the stored expert rows, per head, the mean and the geometric mean of `p(teacher action)`, and
the fraction of decisions above 0.9 / 0.99. The geometric mean is the one that matters: raised to
the number of decisions in a season it IS the probability of a clean rollout.

READ IT
    p ~ 0.999+   the clone is sharp; the sampled failure is elsewhere and RL's entropy bonus is
                 the next suspect.
    p ~ 0.9      the objective never asked for confidence. Cross-entropy is minimised long before
                 the mass concentrates, and 1.0000 agreement is exactly what that looks like.
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--run", required=True, help="run dir holding aggregate.pkl")
    ap.add_argument("--rows", type=int, default=2048)
    args = ap.parse_args()

    import jax.numpy as jnp

    from kagg.il import market_bundles as MB, replays as RP
    from kagg.rl import jax_policy as P

    spec = importlib.util.spec_from_file_location("dagger_tape", REPO / "scripts/dagger_tape.py")
    DT = importlib.util.module_from_spec(spec)
    sys.modules["dagger_tape"] = DT
    spec.loader.exec_module(DT)

    ck = pickle.load(open(args.ckpt, "rb"))
    a = ck.get("args") or {}
    model = P.Policy(d_model=int(a.get("d_model", 128)), n_heads=int(a.get("heads", 4)),
                     n_layers=int(a.get("layers", 3)))
    params = ck["params"]
    vocab = MB.load_vocab(str(ck.get("vocab_path") or a.get("vocab")))
    bundle_ok = MB.valid_table(vocab, pad_to=P.N_BUNDLES)

    agg = pickle.load(open(pathlib.Path(args.run) / "aggregate.pkl", "rb"))
    rows = list(agg.get("expert", []))
    rng = np.random.default_rng(0)
    rows = [rows[i] for i in rng.choice(len(rows), min(args.rows, len(rows)), replace=False)]
    class_w = DT.bundle_class_weights(rows, 1.0)

    print("ckpt %s\nrows %d expert turns\n" % (args.ckpt, len(rows)), flush=True)

    # `op` is per unit and is masked; `bundle` is one per turn. They are collected separately
    # because the number of decisions per season differs by an order of magnitude, and it is the
    # COUNT that turns a per-decision probability into a per-season one.
    probs = collections.defaultdict(list)
    for start in range(0, len(rows), 256):
        chunk = rows[start:start + 256]
        batch = DT.stack(chunk, class_w)
        heads, _v = model.apply(params, *batch["obs"])
        masks, labels = batch["masks"], batch["labels"]
        live = np.asarray(batch["unit_live"]).astype(bool)

        for name in ("op", "bundle"):
            if name not in heads:
                continue
            logits = jnp.where(masks[name], heads[name], -jnp.inf)
            p = np.asarray(jnp.exp(logits - jnp.log(jnp.sum(jnp.exp(logits), axis=-1,
                                                            keepdims=True))))
            lab = np.asarray(labels[name])
            if name == "op":
                for i in range(len(chunk)):
                    for u in np.flatnonzero(live[i]):
                        probs["op"].append(float(p[i, u, int(lab[i, u])]))
            else:
                flat_p = p.reshape(len(chunk), -1)
                flat_l = lab.reshape(len(chunk))
                for i in range(len(chunk)):
                    probs["bundle"].append(float(flat_p[i, int(flat_l[i])]))

    print("  %-8s %8s %10s %10s %8s %8s" %
          ("head", "n", "mean p", "geo-mean", ">0.9", ">0.99"), flush=True)
    for name, vals in probs.items():
        v = np.clip(np.asarray(vals), 1e-12, 1.0)
        print("  %-8s %8d %10.5f %10.5f %7.1f%% %7.1f%%"
              % (name, len(v), v.mean(), float(np.exp(np.log(v).mean())),
                 100.0 * (v > 0.9).mean(), 100.0 * (v > 0.99).mean()), flush=True)

    # The number that actually predicts the rollout. Per-season decision counts are taken from the
    # sample itself, scaled to a full 719-turn season, rather than assumed.
    turns = len({(r.get("ep"), r.get("turn")) for r in rows}) or 1
    for name, vals in probs.items():
        v = np.clip(np.asarray(vals), 1e-12, 1.0)
        per_turn = len(v) / turns
        per_season = per_turn * 719
        logp = float(np.log(v).mean()) * per_season
        print("\n  %s: %.1f decisions/turn -> %.0f per season" % (name, per_turn, per_season),
              flush=True)
        print("    P(whole season sampled exactly) = %.3e" % np.exp(logp), flush=True)


if __name__ == "__main__":
    main()
