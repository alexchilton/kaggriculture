"""Plot a training run's `log.jsonl`, so a trend is read off a curve instead of a tail.

**Why this exists.** Every wrong conclusion in this project so far came from reading a *level* off
the last line of the log -- `wr_pool 0.990`, `ev 0.789`, `bank med $2,600` -- when the question was
always about a *trend*, and often about a trend in a different variable than the one being quoted.
A cumulative rate over 10 games and one over 45 look identical in a tail and completely different
on a curve.

Two conventions here, both deliberate:

- **Cumulative rates are differenced into windowed rates.** `wr_*` in the log is cumulative over the
  whole run, so it is monotone-ish by construction and hides recent change entirely. Every win-rate
  panel shows the *incremental* rate over a window, which is what "is it improving" actually asks.
- **`ev_signal` is plotted with its gaps.** It is uncomputable whenever every finished game that
  update had the same outcome, and those gaps are information -- they were 46% of updates before the
  pool and day-0 fixes. Interpolating across them would erase the thing worth seeing.

    python3 scripts/plot_run.py data/jax_rl_runs/<run>/log.jsonl -o data/logs/run.png
"""

import argparse
import json
import math
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

OPPONENTS = ("idle", "carrot", "farm", "ranch", "pool")
DAYS = (0, 10, 15, 20, 25)


def _nan(v):
    return v is None or (isinstance(v, float) and math.isnan(v))


def windowed_rate(rows, wr_key, games_key, w):
    """Differenced cumulative rate: the rate over each window, not since the run began."""
    xs, ys = [], []
    for i in range(w, len(rows), max(1, w // 2)):
        a, b = rows[i - w], rows[i]
        ga = a.get(games_key) or 0
        gb = b.get(games_key) or 0
        if gb - ga <= 0:
            continue
        fa = 0.0 if _nan(a.get(wr_key)) else a[wr_key]
        fb = 0.0 if _nan(b.get(wr_key)) else b[wr_key]
        xs.append(b["update"])
        ys.append((fb * gb - fa * ga) / (gb - ga))
    return xs, ys


def series(rows, key, default=float("nan")):
    x = [r["update"] for r in rows]
    y = [default if _nan(r.get(key)) else r.get(key, default) for r in rows]
    return x, y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log", help="path to a run's log.jsonl")
    ap.add_argument("-o", "--out", default="data/logs/run.png")
    ap.add_argument("--window", type=int, default=0,
                    help="updates per win-rate window; 0 picks ~1/25th of the run")
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.log) if l.strip()]
    if not rows:
        raise SystemExit(f"{args.log} is empty")
    w = args.window or max(5, len(rows) // 25)
    lo, hi = int(rows[0]["update"]), int(rows[-1]["update"])

    fig, ax = plt.subplots(3, 3, figsize=(19, 12))
    fig.suptitle(f"{pathlib.Path(args.log).parent.name}   updates {lo}-{hi}   "
                 f"({len(rows)} logged, win rates windowed over {w})", fontsize=13)
    a = ax.ravel()

    # 1. The critic on the target that matters. `ev` over all rows is mostly the critic predicting
    # its own bootstrapped values -- terminal rows are ~0.1% of the batch -- so the two are plotted
    # together precisely so they are never confused again.
    x, y = series(rows, "explained_variance")
    a[0].plot(x, y, lw=0.8, alpha=0.5, label="ev (all rows, mostly bootstrap)")
    x, y = series(rows, "ev_signal")
    a[0].plot(x, y, lw=1.2, color="crimson", label="ev_signal (terminal rows)")
    a[0].axhline(0.5, ls="--", c="k", lw=0.8, label="0.5 kill criterion")
    a[0].set_title("explained variance"); a[0].legend(fontsize=7); a[0].set_ylim(-0.2, 1.05)

    # 2. Overall win rate, windowed.
    x, y = windowed_rate(rows, "win_rate", "episodes", w)
    a[1].plot(x, y, color="k")
    a[1].axhline(0.5, ls="--", c="grey", lw=0.8)
    a[1].set_title("win rate (windowed, all opponents)"); a[1].set_ylim(0, 1)

    # 3. Per opponent. This is the panel that shows an opponent saturating -- a flat line at 0.99 or
    # 0.01 is a rung contributing no gradient, whatever its level says.
    for o in OPPONENTS:
        x, y = windowed_rate(rows, f"wr_{o}", f"games_{o}", w)
        if x:
            a[2].plot(x, y, label=o, lw=1.1)
    a[2].axhline(0.5, ls="--", c="grey", lw=0.8)
    a[2].set_title("win rate by opponent (windowed)"); a[2].legend(fontsize=7); a[2].set_ylim(0, 1)

    # 4. Per seed day. Only d0 is the task we are scored on; the rest are 'continue a position'.
    for d in DAYS:
        x, y = windowed_rate(rows, f"wr_day{d}", f"games_day{d}", w)
        if x:
            a[3].plot(x, y, label=f"d{d}" + (" (scored task)" if d == 0 else ""), lw=1.1)
    a[3].axhline(0.5, ls="--", c="grey", lw=0.8)
    a[3].set_title("win rate by seed day (windowed)"); a[3].legend(fontsize=7); a[3].set_ylim(0, 1)

    # 5. Money. `money_med` is cash on hand sampled mid-season, NOT an outcome -- it rises when the
    # policy merely goes broke later. Labelled so that is not misread again.
    x, y = series(rows, "money_med")
    a[4].plot(x, y, color="seagreen")
    if not _nan(rows[-1].get("bank_final_med")):
        x2, y2 = series(rows, "bank_final_med")
        a[4].plot(x2, y2, color="darkgreen", lw=1.4, label="median bank at TERMINATION")
        a[4].legend(fontsize=7)
    a[4].axhline(3000, ls="--", c="k", lw=0.8)
    a[4].set_title("bank: median cash on hand (mid-season, not an outcome)")

    # 6. Losses.
    for k, c in (("policy_loss", "tab:blue"), ("value_loss", "tab:orange"),
                 ("seat_loss", "tab:green"), ("kl_prior", "tab:red")):
        x, y = series(rows, k)
        a[5].plot(x, y, label=k, lw=1.0, color=c)
    a[5].set_yscale("symlog", linthresh=1e-3)
    a[5].set_title("loss components"); a[5].legend(fontsize=7)

    # 7. Exploration. Total entropy is summed over every head, so it cannot show the op head
    # collapsing onto one token while the rest stay spread -- which is the failure mode that looks
    # identical to "it is learning" in the aggregate.
    x, y = series(rows, "entropy")
    a[6].plot(x, y, label="entropy (all heads, summed)", lw=0.9)
    if not _nan(rows[-1].get("op_entropy")):
        x2, y2 = series(rows, "op_entropy")
        a[6].twinx().plot(x2, y2, color="crimson", lw=1.2, label="op head only")
        a[6].plot([], [], color="crimson", label="op head only (right axis)")
    a[6].set_title("entropy"); a[6].legend(fontsize=7)

    # 8. Does it spend? The whole animal/land economy lives here, and it has sat near zero.
    for k, c in (("seed_rate", "tab:brown"), ("hire_rate", "tab:purple"),
                 ("land_rate", "tab:red")):
        x, y = series(rows, k)
        a[7].plot(x, y, label=k, lw=1.0, color=c)
    xa = [r["update"] for r in rows]
    ya = [sum(r.get("buy_animal_rate") or [0]) for r in rows]
    a[7].plot(xa, ya, label="buy_animal (sum)", lw=1.0, color="tab:olive")
    a[7].set_yscale("symlog", linthresh=1e-4)
    a[7].set_title("spend rates"); a[7].legend(fontsize=7)

    # 9. Is there signal at all? `terminal_ret_std == 0` means every finished game that update had
    # the same outcome, i.e. no gradient from the outcome. It was 46% of updates before the fixes.
    x, y = series(rows, "terminal_ret_std")
    a[8].plot(x, y, color="k", lw=0.9, label="terminal_ret_std")
    zero = sum(1 for r in rows if (r.get("terminal_ret_std") or 0) == 0.0) / len(rows)
    xn, yn = series(rows, "n_terminal")
    a[8].twinx().plot(xn, yn, color="tab:blue", lw=0.7, alpha=0.6)
    a[8].set_title(f"outcome signal  (std==0 on {zero:.0%} of updates; blue = games finished)")
    a[8].legend(fontsize=7)

    for p in a:
        p.grid(alpha=0.25)
        p.set_xlabel("update")
    fig.tight_layout()
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=110)
    print(f"wrote {out}  ({len(rows)} updates, {lo}-{hi})")


if __name__ == "__main__":
    main()
