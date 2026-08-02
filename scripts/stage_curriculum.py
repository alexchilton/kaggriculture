"""Walk the curriculum back one stage at a time, re-anchoring the KL prior at each step.

**Why this exists rather than `--curriculum-anneal`.** That flag moves the start day on the update
clock and leaves `--kl-prior` pinned to the original BC checkpoint for the whole run. Two problems,
both of which this script exists to remove:

1. **The anchor goes stale.** The prior is a fixed reference to a clone that was competent at the
   states the *clone* visited. As the schedule walks back, the policy's state distribution moves and
   the anchor does not, so the KL term stops regularising and starts fighting -- pulling a policy
   that has learned day-20 play back toward a checkpoint that has not.
2. **A fixed anchor caps the ceiling, and the codebase already says so.** `bc.rank_seats`'s docstring
   warns that a mid-band clone is only safe as `--init` "because `--init` is params-only with no KL
   anchor -- PPO can walk away from a mediocre clone. Anchoring to one would be the thing
   `CLAUDE.md` forbids: a heuristic that becomes the policy." The run that finally worked
   (`ppo-20260802-091956`) does init *and* anchor to the same checkpoint, which is exactly the
   combination `--init`'s own help text cautions against. Re-anchoring each stage to the policy that
   just succeeded is what turns that from a permanent ceiling into a per-stage starting condition.

**Why the advance is gated on a measurement and not on the clock.** `curriculum.schedule`'s docstring
makes the argument for the clock: a win-rate-driven schedule is self-confirming, because the metric
that advances the curriculum is the metric that judges it. That argument is right about the *win
rate* and does not extend to the value probe, which is an independent measurement of the critic on
held-out replay boards and is not a function of the policy's own outcomes. So the gate here is the
probe, plus a bank check that a clock cannot fake:

- **The value gap must grow.** `HANDOFF_2026-08-02.md`: "If the gap between V(has animals) and V(no
  animals) grows, chaining is working. If it stays at +0.05, the schedule will regress and more days
  will not help." This is the measurement that predicts whether backward chaining can carry credit
  at all, so it is the one thing that must move before the day does.
- **The bank must be above the seed.** At update 0 every slot is freshly seeded, so `money_med` on
  that line *is* the seed-day bank for the stage. Ending above it means the position was grown;
  ending level with it means it was inherited and held, which is the failure the handoff names --
  "a win can be inherited" -- and which a win rate near 0.5 cannot distinguish from a draw.
- **The win rate is reported and never gated on**, for the reason above and because the trainee is
  seeded into the richer seat by default.

**Entropy is a warning, not a gate.** A rising entropy trend was the tell for the failure this whole
line of work fixed, so it is surfaced -- but it was measured oscillating 11.3 -> 12.6 -> 11.3 with
the resample cycle on a healthy run, so treating a single rise as a stop would halt a working
schedule. Reported as a warning, judged by a human.

**The ladder is five-day steps, and the cost of that is episode length.** At 24 turns a day, a stage
at day 25 runs ~120-turn episodes and a stage at day 0 runs 719. With `--horizon 32` the number of
truncated segments the critic must bootstrap GAE across goes roughly 4 -> 8 -> 11 -> 15 -> 19 -> 22,
and terminal games per update falls by about the same factor. That decay is expected and is not the
constant-outcome bug of the turn-0 runs, which was a dead *signal* rather than a thin one; the tell
that distinguishes them is `terminal_ret_std`, which was 0.0-0.4 then and ~0.5 now.
"""

import argparse
import json
import math
import pathlib

# Five-day steps. Not one-day steps: each stage ends in a gate decision and a checkpoint, and the
# point of the staging is to stop and measure, so a step small enough to need thirty gates defeats
# it. Not larger: day 0-8 is where the strategic choice actually lives (`HANDOFF_2026-08-02.md`,
# "a board is a position, not a strategy"), so the ladder spends its last three stages there.
LADDER = (25, 20, 15, 10, 5, 0)

# The mixed band. Measured at day 25: the top-by-bank default puts 46 of 48 boards at five or more
# animals (median 17), and the $15-35k band puts 45 of 48 at zero to four -- which makes FEED
# illegal on almost every board and hands back the DIG/NOOP attractor this work exists to escape.
# $35-70k is 15 of 48 low-animal: genuinely mixed, without the attractor.
#
# **The band is a proxy for strategy and it weakens the earlier the stage.** `rank_seats` filters on
# *final* bank, so at day 20 it selects "seats that ended in this band" rather than "boards that look
# like this now" -- and by day 5 a $50k finisher's board and a $120k finisher's board are nearly the
# same board. Set once; do not re-tune per stage on the belief it is still doing the same work.
BAND = (35_000.0, 70_000.0)

STATE_FILE = "data/curriculum_stages.json"

# Growth smaller than this in the value gap is noise, not chaining. The probe averages over ~40
# replays x 12 sampled turns per seat, and the handoff's own "stays at +0.05" example is the failure
# case, so the margin has to be well inside that to discriminate.
GAP_TOL = 0.01


def load_rows(run_dir):
    """`log.jsonl` as a list of dicts, tolerating a half-written trailing line.

    The trainer appends a line per update while running, so reading a live run can catch a partial
    write. Skipping an unparseable final line is correct here and would be wrong anywhere that
    needed the count to be exact.
    """
    rows = []
    for line in pathlib.Path(run_dir, "log.jsonl").read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _finite(values):
    return [v for v in values if v is not None and isinstance(v, (int, float))
            and not math.isnan(v) and not math.isinf(v)]


def _mean(values):
    vals = _finite(values)
    return sum(vals) / len(vals) if vals else None


def stage_metrics(rows, tail=25):
    """Summarise a stage's log into the numbers the gate reads.

    `tail` is the trailing window averaged for the "recent" figures. Defaulted to the resample
    period so the window covers a whole seed-pool cycle: a shorter one reads the pool it happens to
    land on rather than the stage.
    """
    if not rows:
        return {"updates": 0}

    tail_rows = rows[-tail:]
    seed_bank = None
    for row in rows:
        if row.get("money_med") is not None:
            seed_bank = float(row["money_med"])
            break

    bank_now = _mean([r.get("money_med") for r in tail_rows])
    ent_recent = _mean([r.get("entropy") for r in tail_rows])
    ent_all = _finite([r.get("entropy") for r in rows])

    return {
        "updates": int(rows[-1].get("update", len(rows) - 1)) + 1,
        "win_rate": _mean([r.get("win_rate") for r in tail_rows]),
        "wr_farm": _mean([r.get("wr_farm") for r in tail_rows]),
        "wr_idle": _mean([r.get("wr_idle") for r in tail_rows]),
        "ev_signal": _mean([r.get("ev_signal") for r in tail_rows]),
        "seed_bank": seed_bank,
        "bank_now": bank_now,
        "bank_gain": (bank_now - seed_bank) if (bank_now is not None
                                               and seed_bank is not None) else None,
        "entropy": ent_recent,
        "entropy_min": min(ent_all) if ent_all else None,
        "terminal_ret_std": _mean([r.get("terminal_ret_std") for r in tail_rows]),
        "n_terminal": _mean([r.get("n_terminal") for r in tail_rows]),
        "kl_prior": _mean([r.get("kl_prior") for r in tail_rows]),
    }


def gate(metrics, gap, prev_gap, min_updates=200, gap_tol=GAP_TOL):
    """(passed, reasons, warnings) for advancing to the next stage.

    `prev_gap` is None for the first staged run, which has nothing to have grown from. That stage
    records a baseline and is allowed through on the bank and signal checks alone -- refusing it
    would make the ladder unstartable.
    """
    reasons, warnings = [], []

    if metrics.get("updates", 0) < min_updates:
        reasons.append(f"only {metrics.get('updates', 0)} updates, wanted {min_updates}")

    if gap is None:
        reasons.append("value probe produced no gap (need >=5 boards at 0 and at 4+ animals)")
    elif prev_gap is None:
        warnings.append(f"first stage: recording value gap {gap:+.4f} as the baseline, "
                        "nothing to compare against yet")
    elif gap < prev_gap + gap_tol:
        reasons.append(f"value gap {gap:+.4f} did not grow over previous {prev_gap:+.4f} "
                       f"(needs +{gap_tol:.3f}); chaining is not carrying credit, so a further "
                       f"day will not help")

    gain = metrics.get("bank_gain")
    if gain is None:
        reasons.append("no bank figures in the log")
    elif gain <= 0:
        reasons.append(f"bank {gain:+,.0f} against the seed day: the position was inherited and "
                       f"held, not grown")

    ev = metrics.get("ev_signal")
    if ev is None:
        reasons.append("no ev_signal in the log")
    elif ev <= 0:
        reasons.append(f"ev_signal {ev:+.3f} is not positive; the critic is not learning this stage")

    ent, ent_min = metrics.get("entropy"), metrics.get("entropy_min")
    if ent is not None and ent_min is not None and ent > ent_min + 1.0:
        warnings.append(f"entropy {ent:.2f} is {ent - ent_min:.2f} above this stage's low "
                        f"{ent_min:.2f} -- the erosion tell. It was measured oscillating on a "
                        f"healthy run, so this is a look-at-it, not a stop.")

    tstd = metrics.get("terminal_ret_std")
    if tstd is not None and tstd < 0.2:
        reasons.append(f"terminal_ret_std {tstd:.3f} is near the constant-outcome range that made "
                       f"1,300 updates go nowhere; outcomes are not varying")

    return (not reasons), reasons, warnings


def next_day(day, ladder=LADDER):
    """The day after `day` on the ladder, or None at the end."""
    rungs = list(ladder)
    if day not in rungs:
        below = [d for d in rungs if d < day]
        return max(below) if below else None
    i = rungs.index(day)
    return rungs[i + 1] if i + 1 < len(rungs) else None


def build_command(day, prior, init, band=BAND, ent_coef=0.01, early_limit=0, resample=25,
                  updates=20000, behind=False, root="", min_updates=200):
    """The training command for a stage, with the two bugs this project has already paid for barred.

    Both are the same class of failure -- a flag that silently produces a run which looks fine and
    trains nothing -- and both are cheaper to make unrepresentable than to re-diagnose.
    """
    if not ent_coef:
        raise ValueError(
            "--ent-coef 0 with --kl-prior removes the regulariser entirely: reg_coef = "
            "args.ent_coef and regulariser = reg_coef * kl_prior, so the KL shares the entropy "
            "coefficient. This instruction was in --kl-prior's help text, cost two runs via "
            "--kl-coef, and survived into --kl-prior.")
    if early_limit:
        raise ValueError(
            f"--early-limit {early_limit} with a curriculum truncates every early env on its first "
            f"turn, because the limit is an absolute turn number and a seeded episode starts past "
            f"it. It shows up as `wr nan` and `tstd 0.000`, not as an error. Must be 0.")
    if not prior or not init:
        raise ValueError(
            "a stage needs both --kl-prior and --init. Re-anchoring is the point: the prior is what "
            "stops the previous stage's competence eroding, and the init is what carries it in.")

    prefix = f"{root.rstrip('/')}/" if root else ""
    cmd = [
        f"{prefix}scripts/train_jax_rl.py" if root else "kagg-train",
        "--batch", "256", "--horizon", "32", "--updates", str(updates),
        "--minibatch-size", "512", "--epochs", "2", "--n-phases", "256",
        "--opponent-frac", "0.15", "--idle-frac", "0.10", "--trade-frac", "0.00",
        "--farm-frac", "0.40", "--early-limit", "0", "--seat-coef", "1.0",
        "--ent-coef", str(ent_coef), "--lr", "3e-5", "--pool-every", "50", "--ckpt-every", "50",
        "--curriculum-day", str(day), "--curriculum-resample", str(resample),
        "--kl-prior", str(prior), "--init", str(init),
    ]
    if band and band[0] is not None:
        cmd += ["--curriculum-min-bank", str(int(band[0]))]
    if band and band[1] is not None:
        cmd += ["--curriculum-max-bank", str(int(band[1]))]
    if behind:
        cmd.append("--curriculum-behind")
    return cmd


def read_state(path=STATE_FILE):
    p = pathlib.Path(path)
    return json.loads(p.read_text()) if p.exists() else {"stages": []}


def write_state(state, path=STATE_FILE):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2) + "\n")


def previous_gap(state):
    """The most recent recorded value gap, or None if no stage has been recorded."""
    for stage in reversed(state.get("stages", [])):
        if stage.get("value_gap") is not None:
            return float(stage["value_gap"])
    return None


def value_gap(checkpoint):
    """V(4+ animals) - V(0 animals) for a checkpoint, or None if the probe cannot form both groups.

    Imported lazily and reused from `diagnose_policy` rather than reimplemented, so there is exactly
    one definition of this number and a change to the probe cannot silently diverge from the gate.

    The probe samples whole recorded seasons, not the curriculum day, so it stays measurable at
    every stage -- including day 0, where no *seeded* board has animals but the replay boards it
    reads still span 0 to a full herd.
    """
    import pickle

    import jax
    import numpy as np

    from kagg.rl import jax_policy as P
    from scripts.diagnose_policy import value_vs_animals

    with pathlib.Path(checkpoint).open("rb") as fh:
        ck = pickle.load(fh)
    saved = ck.get("args") or {}
    model = P.Policy(d_model=saved.get("d_model", 128), n_heads=saved.get("heads", 4),
                     n_layers=saved.get("layers", 3))
    by_count = value_vs_animals(jax.device_put(ck["params"]), model)

    none = by_count.get(0, [])
    some = [v for n, vs in by_count.items() if n >= 4 for v in vs]
    if len(none) < 5 or len(some) < 5:
        return None
    return float(np.mean(some) - np.mean(none))


def remote_path(local, remote_root):
    """Map a local checkpoint path onto the training box, which roots the project elsewhere.

    Keyed on the `data/` segment because that is the one directory both trees share by construction
    (`RUN_DIR` is `data/jax_rl_runs` under whichever root). A path with no `data/` segment is passed
    through rather than guessed at: a path that does not exist on the box kills the run on startup,
    which is loud, whereas a *plausible* wrong path would anchor the next stage to the wrong
    checkpoint and look exactly like a working handover.
    """
    p = pathlib.PurePosixPath(local).as_posix()
    root = remote_root.rstrip("/")
    if "data/" in p:
        return f"{root}/data/{p.split('data/', 1)[1]}"
    return p if p.startswith("/") else f"{root}/{p}"


def curriculum_day_of(run_dir):
    """The `--curriculum-day` a run was launched with, read from its own checkpoint."""
    import pickle

    with pathlib.Path(run_dir, "latest.pkl").open("rb") as fh:
        ck = pickle.load(fh)
    return (ck.get("args") or {}).get("curriculum_day")


def _report(day, metrics, gap, prev_gap, passed, reasons, warnings):
    print(f"\n=== stage at game-day {day}: {metrics.get('updates', 0)} updates ===")
    fmt = [
        ("win rate", metrics.get("win_rate"), "{:.3f}"),
        ("  vs farmer", metrics.get("wr_farm"), "{:.3f}"),
        ("  vs idle", metrics.get("wr_idle"), "{:.3f}"),
        ("ev_signal", metrics.get("ev_signal"), "{:+.3f}"),
        ("entropy", metrics.get("entropy"), "{:.2f}"),
        ("kl_prior", metrics.get("kl_prior"), "{:.3f}"),
        ("terminal_ret_std", metrics.get("terminal_ret_std"), "{:.3f}"),
        ("terminal games/update", metrics.get("n_terminal"), "{:.0f}"),
        ("seed-day bank", metrics.get("seed_bank"), "${:,.0f}"),
        ("bank now", metrics.get("bank_now"), "${:,.0f}"),
        ("bank vs seed", metrics.get("bank_gain"), "{:+,.0f}"),
    ]
    for name, value, spec in fmt:
        print(f"  {name:22s} {spec.format(value) if value is not None else 'n/a'}")

    print(f"  {'value gap':22s} "
          f"{f'{gap:+.4f}' if gap is not None else 'n/a'}"
          f"{f'  (previous {prev_gap:+.4f})' if prev_gap is not None else '  (no baseline yet)'}")

    for w in warnings:
        print(f"\n  WARNING: {w}")
    if passed:
        print("\n  GATE PASSED")
    else:
        print("\n  GATE HELD:")
        for r in reasons:
            print(f"    - {r}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("run_dir", help="the finished stage's run directory (holds log.jsonl, latest.pkl)")
    ap.add_argument("--day", type=int, default=None,
                    help="the stage's curriculum day; read from the checkpoint if omitted")
    ap.add_argument("--checkpoint", default="latest.pkl",
                    help="checkpoint within run_dir to probe and to anchor the next stage to")
    ap.add_argument("--min-updates", type=int, default=200)
    ap.add_argument("--tail", type=int, default=25, help="trailing updates averaged for 'recent'")
    ap.add_argument("--skip-probe", action="store_true",
                    help="skip the value probe (fast, but the gate cannot pass without it)")
    ap.add_argument("--record", action="store_true",
                    help="write this stage into the state file. Without it, nothing is recorded and "
                         "the next stage's gate has no baseline to compare against.")
    ap.add_argument("--state", default=STATE_FILE)
    ap.add_argument("--remote-root", default="/home/alex/kagg",
                    help="root on the training box, for the emitted launch command")
    ap.add_argument("--behind", action="store_true",
                    help="emit the next stage with --curriculum-behind (poorer seat, so a win "
                         "cannot be inherited). Meaningless at day 0, where both seats are equal.")
    ap.add_argument("--no-band", action="store_true", help="emit the next stage without band flags")
    args = ap.parse_args()

    run_dir = pathlib.Path(args.run_dir)
    ckpt = run_dir / args.checkpoint
    day = args.day if args.day is not None else curriculum_day_of(run_dir)
    if day is None:
        raise SystemExit("could not determine the stage's curriculum day; pass --day")

    metrics = stage_metrics(load_rows(run_dir), tail=args.tail)
    gap = None if args.skip_probe else value_gap(ckpt)
    state = read_state(args.state)
    prev = previous_gap(state)

    passed, reasons, warnings = gate(metrics, gap, prev, min_updates=args.min_updates)
    _report(day, metrics, gap, prev, passed, reasons, warnings)

    if args.record:
        state.setdefault("stages", []).append({
            "day": day, "run_dir": str(run_dir), "checkpoint": str(ckpt),
            "value_gap": gap, "passed": passed, **metrics,
        })
        write_state(state, args.state)
        print(f"\n  recorded in {args.state}")

    if not passed:
        print("\nNot advancing. The gate is the point: a schedule that advances because outcomes "
              "went degenerate looks identical to one that advanced because the policy improved.")
        return

    nxt = next_day(day)
    if nxt is None:
        print(f"\nDay {day} is the last rung. Nothing left to anneal -- the policy now trains on "
              f"the real opening and is the first thing here that could be submitted.")
        return

    remote_ckpt = remote_path(ckpt, args.remote_root)
    cmd = build_command(nxt, prior=remote_ckpt, init=remote_ckpt,
                        band=None if args.no_band else BAND, behind=args.behind,
                        root=args.remote_root)

    print(f"\n=== next stage: game-day {nxt} ===")
    print(f"  prior and init re-anchored to {remote_ckpt}")
    print(f"  episodes grow to ~{(30 - nxt) * 24} turns "
          f"(~{max(1, ((30 - nxt) * 24) // 32)} horizon segments), so expect terminal games per "
          f"update to fall by roughly the same factor. Watch terminal_ret_std, not the count.\n")
    print("  " + " \\\n    ".join(
        [f"PYTHONPATH={args.remote_root} XLA_PYTHON_CLIENT_PREALLOCATE=false "
         f"{args.remote_root}-venv/bin/python -u " + cmd[0]] + _pairs(cmd[1:])))
    print(f"\n  tee to {args.remote_root}/data/logs/train.log and run it under tmux, or it is "
          f"invisible.")


def _pairs(rest):
    """Group `--flag value` into single lines so the emitted command is readable."""
    out, i = [], 0
    while i < len(rest):
        if rest[i].startswith("--") and i + 1 < len(rest) and not rest[i + 1].startswith("--"):
            out.append(f"{rest[i]} {rest[i + 1]}")
            i += 2
        else:
            out.append(rest[i])
            i += 1
    return out


if __name__ == "__main__":
    main()
