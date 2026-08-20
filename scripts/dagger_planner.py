"""DAgger round N: the STUDENT drives, the PLANNER labels the states it reached.

**Why this exists, and why it is out of scan.** `scripts/bc_dagger.py` runs the teacher as array
code inside a `jax.scan`, which is fast and useless here: our teacher is the shipped Python planner
(`submission/main.py`) and cannot be traced. So the loop is ordinary Python against the real
`kaggle_environments` env, and the cost is what makes that acceptable --
`scripts/measure_solve_cost.py` measured forcing every day through the live solver at **1.2x** the
shipped replay path (0.0108 vs 0.0092 s/turn, seed 12345, d0-d12), not the ~100x that was assumed.

**What DAgger buys that round 0 cannot.** Round 0 (`label_games.py`) is teacher-on-teacher-states:
beta = 1, plain behaviour cloning. It teaches the student what the teacher does on the teacher's own
trajectory, and says nothing about the states the student reaches when it is slightly wrong. That
gap is measured in this project: 86.2% per-decision accuracy on teacher states scored 79.3% error on
the policy's own trajectory. The board is an OUTPUT of the action sequence, so a small early
divergence compounds into a board no stored route was solved for -- which is exactly the state the
student needs a label for, and exactly the state round 0 contains none of.

**The planner is stateful, and that is wanted.** It plans a whole day once, at hour 0
(`docs/architecture.md`), and holds that plan across the day's 24 turns. Feeding it the student's
observations means its internal plan is built from the student's board, so the label is "what the
planner would do FROM HERE", not "what the planner would have done in its own game". A fresh teacher
instance per game keeps one game's drift out of the next.

**beta mixes who actually moves, not who labels.** Every visited state is labelled by the planner
regardless. `--beta` only decides which action is EXECUTED, so beta=1 reproduces round 0 exactly and
beta=0 is a pure student rollout. The default is 0: the point of a later round is the student's own
distribution, and the standard practical choice against a fixed expert is to stop mixing after
round 0. Raise it if the student is so bad that its rollouts never reach a useful state.

Output is the SAME JSONL schema as `label_games.py`, so `build_bc_rows.py` consumes both without
knowing which round produced a row.

    python -u scripts/dagger_planner.py --checkpoint /home/alex/bc_bundle.pkl \
        --games 40 --worker 0 --out /home/alex/labels_r1 --teacher submission/main.py
"""

import argparse
import json
import pathlib
import random
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.label_games import obs_snapshot                  # noqa: E402


def load_teacher(path):
    """A fresh module per call. The planner keeps per-game state in module scope, so two games
    sharing one instance would carry day 29's plan into day 0 of the next."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("teacher_%d" % random.randrange(1 << 30), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.agent


def empty_action():
    """What the environment reads as 'do nothing'. Used only when the student raises."""
    return {"farmer": ["PASS"], "hands": [], "market": []}


def play(seed, out_fh, student, teacher_factory, beta, opponent):
    """One game. Both seats are recorded; both are labelled by the planner.

    The OPPONENT seat matters and is not incidental. The market is contested -- selling into the
    same book as the other player is what moves the price -- so a student rolled against an idle
    opponent visits states no ranked game contains. The opponent is the teacher by default, which
    is also what round 0 used, so the two rounds differ in the student's seat and nothing else.
    """
    from kaggle_environments import make

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)

    # One teacher instance per SEAT per GAME: seat 0's labeller follows seat 0's board all season.
    labellers = [teacher_factory(), teacher_factory()]
    movers = [student, opponent]

    turns, student_errors, taught = 0, 0, 0
    while not env.done:
        snaps, executed = [], []
        for seat in (0, 1):
            ob = env.state[seat].observation
            cfg = env.configuration
            snaps.append(obs_snapshot(ob, seat))

            # **The label always comes from the planner, and always first.** Calling it before the
            # student keeps the label a function of the state alone: if the student mutated the
            # observation dict in place, a label taken afterwards would describe a board the
            # environment never had.
            label = labellers[seat](ob, cfg)
            taught += 1

            if beta >= 1.0 or (beta > 0.0 and random.random() < beta):
                act = label
            else:
                try:
                    act = movers[seat](ob, cfg)
                except Exception as exc:                      # noqa: BLE001
                    # A student that crashes mid-season must not lose the whole game's labels. The
                    # turn is recorded, the seat passes, and the count is reported -- a silent
                    # fallback here would read as a student that likes doing nothing.
                    student_errors += 1
                    if student_errors <= 3:
                        print("   seat %d turn %d student raised: %s" % (seat, turns, exc),
                              flush=True)
                    act = empty_action()
            executed.append(act)

            # The row pairs the state with the PLANNER's action, never the executed one. That is
            # the whole of DAgger: learn the expert's answer on the learner's states.
            out_fh.write(json.dumps({"seed": seed, "seat": seat, "round": "dagger",
                                     "obs": snaps[seat], "act": label}) + "\n")

        env.step(executed)
        turns += 1

    banks = [(s.get("reward") or 0.0) for s in env.steps[-1]]
    return turns, banks, student_errors, taught


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", required=True, help="the BC checkpoint the student plays")
    ap.add_argument("--teacher", default="submission/main.py")
    ap.add_argument("--games", type=int, default=10)
    ap.add_argument("--worker", type=int, default=0)
    ap.add_argument("--out", required=True)
    ap.add_argument("--beta", type=float, default=0.0,
                    help="probability a turn is EXECUTED by the teacher. Labelling is unaffected.")
    ap.add_argument("--seed-base", type=int, default=1_000_000,
                    help="offset from round 0's seeds so the two rounds do not share games")
    args = ap.parse_args()

    if not 0.0 <= args.beta <= 1.0:
        raise SystemExit("--beta must be in [0, 1]; got %r" % args.beta)

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    shard = out / ("shard_%03d.jsonl" % args.worker)

    from kagg.agents import neural
    student = neural.make_agent(args.checkpoint)
    opponent = load_teacher(args.teacher)

    print("student   %s" % args.checkpoint, flush=True)
    print("teacher   %s" % args.teacher, flush=True)
    print("beta      %.2f  (0 = the student drives every turn)" % args.beta, flush=True)

    t0, all_turns, all_err, all_taught = time.time(), 0, 0, 0
    student_wins = 0
    with shard.open("w") as fh:
        for g in range(args.games):
            seed = args.seed_base + args.worker * 100000 + g
            t1 = time.time()
            turns, banks, errs, taught = play(
                seed, fh, student, lambda: load_teacher(args.teacher), args.beta, opponent)
            all_turns += turns
            all_err += errs
            all_taught += taught
            if banks[0] > banks[1]:
                student_wins += 1
            # The bank is the instrument, not the loss. A student that draws every game at $0 is
            # indistinguishable from one that plays well by win rate alone -- money == money is
            # exact, so two do-nothing policies draw with certainty.
            print("w%02d game %3d seed %-9d turns %3d  student $%-9.0f teacher $%-9.0f "
                  "errs %d  %.1fs"
                  % (args.worker, g, seed, turns, banks[0], banks[1], errs, time.time() - t1),
                  flush=True)

    print("\nw%02d DONE %d games in %.1fs -> %s"
          % (args.worker, args.games, time.time() - t0, shard), flush=True)
    print("w%02d student won %d/%d   labelled %s states   student errors %d"
          % (args.worker, student_wins, args.games, format(all_taught, ","), all_err), flush=True)
    if all_err:
        print("w%02d *** the student raised on %d turns; those turns executed PASS, so this "
              "shard's states are only partly on-policy ***" % (args.worker, all_err), flush=True)


if __name__ == "__main__":
    main()
