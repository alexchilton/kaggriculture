"""Did training change anything, and did it change it in a useful direction?

**Why this is not answerable from the loss curve.** A randomly-initialised policy has near-zero
logits, so its argmax is an arbitrary but CONSTANT class -- and if that class happens to be the
empty bundle, it scores 0.788 agreement with the teacher having learned nothing whatsoever. That is
exactly the figure the first trained checkpoint reported. Without an untrained baseline on the same
rows, "0.788" and "learned the teacher's prior" and "learned nothing" are indistinguishable.

So this compares checkpoints -- including a fresh init as the zero point -- on three things:

  1. **The weights.** Per-parameter-group norms, and the relative change from the baseline. If a
     head's weights have not moved, no amount of falling total loss involved it. This catches a head
     that is receiving no gradient, which has happened in this project before.
  2. **The output distribution** on a fixed batch of held-out states: entropy, how many distinct
     classes the argmax ever selects, and the probability mass on the empty bundle. A collapsed head
     has low entropy AND one distinct argmax; an untrained head has HIGH entropy and one distinct
     argmax. Those are different failures and the agreement number cannot tell them apart.
  3. **Agreement with the teacher**, split by whether the teacher traded, so a model that only
     learned the majority class is visible as such.

    python -u scripts/compare_checkpoints.py --rows /home/alex/rows_r0b \
        --ckpt /home/alex/bc_bundle.ep0.pkl --ckpt /home/alex/bc_bundle.best.pkl
"""

import argparse
import glob
import pathlib
import pickle
import sys

import jax
import jax.numpy as jnp
import numpy as np

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.rl import jax_act as A, jax_obs, jax_policy as P     # noqa: E402


def flat_groups(params, prefix=""):
    """Leaf arrays keyed by their path, so two checkpoints can be compared group by group."""
    out = {}
    for k, v in params.items():
        name = "%s/%s" % (prefix, k) if prefix else str(k)
        if isinstance(v, dict):
            out.update(flat_groups(v, name))
        else:
            out[name] = np.asarray(v)
    return out


def head_report(logits, label, name, traded=None):
    """Entropy, argmax spread and agreement for one head on one batch."""
    logits = np.asarray(logits, dtype=np.float64)
    shifted = logits - logits.max(axis=-1, keepdims=True)
    p = np.exp(shifted)
    p /= p.sum(axis=-1, keepdims=True)
    ent = float(-(p * np.log(p + 1e-12)).sum(axis=-1).mean())
    amax = logits.argmax(axis=-1)
    distinct = int(len(np.unique(amax)))
    agree = float((amax == label).mean())
    row = {"head": name, "entropy": ent, "distinct_argmax": distinct, "agreement": agree,
           "max_entropy": float(np.log(logits.shape[-1]))}
    if traded is not None and traded.any():
        row["agreement_traded"] = float((amax[traded] == label[traded]).mean())
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True, help="row directory; the LAST shard is used")
    ap.add_argument("--ckpt", action="append", default=[],
                    help="repeatable. A fresh init is always prepended as the baseline.")
    ap.add_argument("--n", type=int, default=4096)
    args = ap.parse_args()

    shards = sorted(glob.glob(args.rows.rstrip("/") + "/*.npz"))
    if not shards:
        raise SystemExit("no npz under %s" % args.rows)
    d = np.load(shards[-1])
    sl = slice(0, min(args.n, len(d["y_bundle"])))
    tiles = jnp.asarray(d["tiles"][sl], dtype=jnp.float32)
    units = jnp.asarray(d["units"][sl], dtype=jnp.float32)
    gfeat = jnp.asarray(d["glob"][sl], dtype=jnp.float32)
    y_bundle = d["y_bundle"][sl]
    y_op = d["y_op"][sl]
    live = d["live"][sl]
    traded = y_bundle != 0
    print("probe: %s rows from %s   teacher traded on %.1f%% of them"
          % (format(sl.stop, ","), pathlib.Path(shards[-1]).name,
             100.0 * traded.mean()), flush=True)

    model = P.Policy()
    baseline = model.init(jax.random.PRNGKey(0), tiles[:1], units[:1], gfeat[:1])

    loaded = [("UNTRAINED (fresh init)", baseline)]
    for path in args.ckpt:
        with pathlib.Path(path).open("rb") as fh:
            raw = pickle.load(fh)
        loaded.append((pathlib.Path(path).name, P.load_or_migrate(raw["params"], baseline)))

    base_groups = flat_groups(baseline)

    for name, params in loaded:
        heads, _v = model.apply(params, tiles, units, gfeat)
        print("\n" + "=" * 78)
        print(name)
        print("=" * 78)

        rows = [head_report(heads["bundle"], y_bundle, "bundle", traded)]
        op_logits = np.asarray(heads["op"])
        rows.append(head_report(op_logits[live], y_op[live], "op (live slots)"))

        print("  %-18s %9s %9s %9s %9s %9s"
              % ("head", "entropy", "of max", "distinct", "agree", "agree/tr"))
        for r in rows:
            print("  %-18s %9.3f %9.3f %9d %9.3f %9s"
                  % (r["head"], r["entropy"], r["entropy"] / max(1e-9, r["max_entropy"]),
                     r["distinct_argmax"], r["agreement"],
                     ("%.3f" % r["agreement_traded"]) if "agreement_traded" in r else "-"))

        # **Where the weights actually moved.**
        #
        # ABSOLUTE change, not relative. Every output head is zero-initialised
        # (`jax_policy.py:195`, `kernel_init=zero`), so dividing by the baseline norm divides by
        # zero: the first version of this printed changes of 3.4e9 for exactly the heads that had
        # trained normally, and they read as an explosion rather than as a broken denominator.
        #
        # A group at exactly 0.0 received no gradient at all. That is not automatically a bug --
        # the value head is zero here because `bc.loss` has no value target and BC does not train
        # it -- but it must be visible, because a head silently receiving nothing looks identical
        # to a head that is merely learning slowly.
        groups = flat_groups(params)
        deltas = []
        for k in sorted(groups):
            b, cur = base_groups.get(k), groups[k]
            if b is None or b.shape != cur.shape:
                continue
            deltas.append((float(np.linalg.norm(cur - b)), k, float(np.linalg.norm(cur))))
        deltas.sort(reverse=True)
        if deltas and name != loaded[0][0]:
            print("\n  weight change from init, ABSOLUTE L2  (top 6, then anything unmoved)")
            print("    %-52s %10s %10s" % ("group", "|delta|", "|now|"))
            for dl, k, now in deltas[:6]:
                print("    %-52s %10.4f %10.4f" % (k[-52:], dl, now))
            unmoved = [(dl, k, now) for dl, k, now in deltas if dl == 0.0]
            for dl, k, now in unmoved:
                print("    %-52s %10.4f %10.4f   <-- NO GRADIENT" % (k[-52:], dl, now))
            if not unmoved:
                print("    (every group moved)")

    print("\n" + "-" * 78)
    print("How to read this:")
    print("  An UNTRAINED head has entropy near its maximum and ONE distinct argmax -- it is")
    print("  uninformative, not collapsed. A COLLAPSED head has LOW entropy and one distinct")
    print("  argmax: it is confidently wrong, and that is the failure that survives training.")
    print("  Agreement alone cannot separate them, because predicting the empty bundle every")
    print("  turn scores 0.789 either way.")


if __name__ == "__main__":
    main()
