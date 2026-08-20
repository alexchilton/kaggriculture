"""Plot a training run's `log.jsonl` to a PNG. Works for BC, DAgger and RL.

Both `fit_bc.py` and `train_jax_rl.py` write one JSON object per step -- per epoch and per update
respectively -- so one plotter reads both. Nothing here knows which produced the file: it plots the
numeric keys it finds, grouped so that quantities on the same scale share an axis.

**A PNG on disk, not a hosted page.** Written next to the log unless `--out` says otherwise, so it
opens in an editor while the run continues.

    python -u scripts/plot_run.py /home/alex/bc_bundle.log.jsonl
    python -u scripts/plot_run.py data/rl_runs/<tag>/log.jsonl --out data/logs/rl.png

**Read the agreement panel, not the loss panel.** A falling loss with flat
`holdout_bundle_agreement_traded` is the failure this whole pipeline exists to catch: the model is
getting better at predicting the 78.9% of turns where the teacher does nothing, and no better at the
21.1% that carry all the money. The two curves are deliberately drawn on the same axes so that gap
is visible rather than inferred.
"""

import argparse
import json
import pathlib
import sys

#: Panels, in order. Each is (title, [key substrings], ylabel). A key is drawn in the FIRST panel
#: whose patterns it matches, so the specific ones come before the general ones.
PANELS = [
    ("Held-out agreement with the teacher", ["agreement"], "fraction of rows"),
    ("Market activity", ["empty_rate", "market_rate", "trade_rate"], "fraction of turns"),
    ("Win rate / return", ["win", "reward", "return", "bank"], ""),
    ("Loss", ["loss"], "nats"),
    ("Other", [], ""),
]


def rows_of(path):
    out = []
    for line in pathlib.Path(path).read_text().splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass          # a partially written last line while the run is live
    return out


def x_axis(rows):
    """Whichever step counter the writer used. `fit_bc` says epoch, `train_jax_rl` says update."""
    for key in ("update", "epoch", "step", "iteration"):
        if key in rows[0]:
            return key, [r.get(key, i) for i, r in enumerate(rows)]
    return "row", list(range(len(rows)))


def assign(keys):
    """Group keys into panels. First match wins, so 'holdout_...agreement' beats 'loss'."""
    groups = {title: [] for title, _, _ in PANELS}
    for k in keys:
        for title, patterns, _ in PANELS:
            if not patterns:                      # the catch-all
                continue
            if any(p in k for p in patterns):
                groups[title].append(k)
                break
        else:
            groups["Other"].append(k)
    return groups


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log", help="path to a log.jsonl written by fit_bc.py or train_jax_rl.py")
    ap.add_argument("--out", default=None, help="PNG path (default: alongside the log)")
    ap.add_argument("--skip", type=int, default=0, help="drop the first N rows (warm-up)")
    args = ap.parse_args()

    rows = rows_of(args.log)[args.skip:]
    if not rows:
        raise SystemExit("no rows in %s" % args.log)

    import matplotlib
    matplotlib.use("Agg")                          # no display on the training box
    import matplotlib.pyplot as plt

    xname, xs = x_axis(rows)
    numeric = sorted({k for r in rows for k, v in r.items()
                      if isinstance(v, (int, float)) and not isinstance(v, bool)
                      and k not in (xname, "seconds")})
    groups = {t: ks for t, ks in assign(numeric).items() if ks}
    if not groups:
        raise SystemExit("nothing numeric to plot in %s" % args.log)

    fig, axes = plt.subplots(len(groups), 1, figsize=(11, 3.1 * len(groups)), sharex=True)
    if len(groups) == 1:
        axes = [axes]

    for ax, (title, keys) in zip(axes, groups.items()):
        for k in keys:
            ys = [r.get(k) for r in rows]
            pts = [(x, y) for x, y in zip(xs, ys) if y is not None]
            if pts:
                # Wide lines for the two that decide whether a run is working at all.
                lw = 2.4 if "traded" in k or k.endswith("win_rate") else 1.3
                ax.plot([p[0] for p in pts], [p[1] for p in pts], label=k, linewidth=lw)
        ylabel = next(y for t, _, y in PANELS if t == title)
        ax.set_ylabel(ylabel)
        ax.set_title(title, loc="left", fontsize=10)
        ax.grid(alpha=0.25)
        ax.legend(fontsize=7, ncol=2)

    axes[-1].set_xlabel(xname)
    fig.suptitle("%s   (%d rows)" % (pathlib.Path(args.log).name, len(rows)), fontsize=11)
    fig.tight_layout()

    out = pathlib.Path(args.out) if args.out else pathlib.Path(args.log).with_suffix(".png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=130)
    print("wrote %s" % out)

    # The last row as text too, because a PNG on the training box is not something Alex can see
    # without pulling it, and a log path is not a result.
    last = rows[-1]
    print("\nlast row (%s=%s):" % (xname, last.get(xname)))
    for k in numeric:
        if k in last:
            print("   %-38s %.4f" % (k, last[k]))


if __name__ == "__main__":
    sys.exit(main())
