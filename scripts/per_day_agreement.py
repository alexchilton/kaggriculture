"""Does the student match the teacher op-for-op, day by day? Both on- and off-policy.

Alex's acceptance measure: "it needs to only really follow all the actions of each tape exactly per
d boundary." A season total cannot say that. `docs/../.claude/skills/matching-the-tape` makes the
same point about the planner -- days match IN ORDER, and an earlier day's failure is the one to fix,
because every later day inherits its board.

**Two runs, because they answer different questions and only the pair is interpretable.**

  OFF-POLICY (the teacher drives). Both agents see the teacher's board all season. The student's
  action is scored but never executed. This is pure imitation accuracy, with no compounding: it
  says whether the student LEARNED the mapping.

  ON-POLICY (the student drives). The student's own board, with the teacher labelling each state it
  reaches. This is what actually happens at play time, and the gap between the two curves IS the
  covariate shift -- measured at 86.2% per-decision on teacher states against 79.3% error on the
  policy's own trajectory, earlier in this project.

A student can be excellent off-policy and useless on-policy. If the on-policy curve falls off a
cliff at day N, day N is where to look, and no later day's number means anything until it is fixed.

    python -u scripts/per_day_agreement.py --checkpoint /home/alex/bc_bundle.best.pkl --games 2
"""

import argparse
import collections
import pathlib
import random
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.il import market_bundles as MB                      # noqa: E402

TURNS_PER_DAY = 24


def load_teacher(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("teacher_%d" % random.randrange(1 << 30), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.agent


def unit_ops(action):
    """The op NAME per unit slot, which is what 'op for op' means."""
    acts = [action.get("farmer")] + list(action.get("hands") or [])
    return [str(a[0]) if a else "PASS" for a in acts]


def compare(student_act, teacher_act, tally, day):
    """Score one turn: per-unit op agreement, and whether the market bundle matched exactly."""
    s_ops, t_ops = unit_ops(student_act), unit_ops(teacher_act)
    n = min(len(s_ops), len(t_ops))
    tally[day]["slots"] += n
    tally[day]["slots_agree"] += sum(1 for i in range(n) if s_ops[i] == t_ops[i])
    # A slot the teacher used and the student did not is a different failure from a mismatch.
    tally[day]["slot_count_delta"] += abs(len(s_ops) - len(t_ops))

    s_b = MB.bundle_of(student_act.get("market") or [])
    t_b = MB.bundle_of(teacher_act.get("market") or [])
    tally[day]["turns"] += 1
    tally[day]["bundle_agree"] += int(s_b == t_b)
    if t_b:
        tally[day]["teacher_traded"] += 1
        tally[day]["bundle_agree_traded"] += int(s_b == t_b)


def run(seed, student, teacher_factory, driver, days):
    """`driver` is 'teacher' (off-policy) or 'student' (on-policy)."""
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)

    labeller = teacher_factory()          # follows seat 0's board, whoever is driving it
    opponent = teacher_factory()
    tally = collections.defaultdict(collections.Counter)
    errors = 0

    while not env.done:
        ob0 = env.state[0].observation
        day = int(ob0.get("day", 0) or 0)
        if day >= days:
            break

        teacher_act = labeller(ob0, env.configuration)
        try:
            student_act = student(ob0, env.configuration)
        except Exception:                                     # noqa: BLE001
            errors += 1
            student_act = {"farmer": ["PASS"], "hands": [], "market": []}

        compare(student_act, teacher_act, tally, day)

        seat0 = teacher_act if driver == "teacher" else student_act
        env.step([seat0, opponent(env.state[1].observation, env.configuration)])

    return tally, errors


def table(title, tally, days):
    print("\n%s" % title)
    print("  %3s %8s %10s %10s %12s" % ("day", "turns", "op agree", "bundle", "bundle/traded"))
    for d in range(days):
        t = tally.get(d)
        if not t or not t["turns"]:
            continue
        op = t["slots_agree"] / max(1, t["slots"])
        bu = t["bundle_agree"] / max(1, t["turns"])
        tr = (t["bundle_agree_traded"] / t["teacher_traded"]) if t["teacher_traded"] else float("nan")
        print("  %3d %8d %10.3f %10.3f %12s"
              % (d, t["turns"], op, bu, "-" if t["teacher_traded"] == 0 else "%.3f" % tr))
    tot = collections.Counter()
    for t in tally.values():
        tot.update(t)
    print("  %3s %8d %10.3f %10.3f %12s"
          % ("all", tot["turns"], tot["slots_agree"] / max(1, tot["slots"]),
             tot["bundle_agree"] / max(1, tot["turns"]),
             "-" if not tot["teacher_traded"]
             else "%.3f" % (tot["bundle_agree_traded"] / tot["teacher_traded"])))
    return tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--teacher", default="submission/main.py")
    ap.add_argument("--games", type=int, default=1)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--seed-base", type=int, default=8_000_000)
    args = ap.parse_args()

    from kagg.agents import neural
    student = neural.make_agent(args.checkpoint)
    factory = lambda: load_teacher(args.teacher)               # noqa: E731

    for driver in ("teacher", "student"):
        merged = collections.defaultdict(collections.Counter)
        errs = 0
        for g in range(args.games):
            tally, e = run(args.seed_base + g, student, factory, driver, args.days)
            errs += e
            for d, t in tally.items():
                merged[d].update(t)
        label = ("OFF-POLICY: the TEACHER drives; pure imitation, no compounding"
                 if driver == "teacher" else
                 "ON-POLICY: the STUDENT drives; this is what play looks like")
        tot = table(label, merged, args.days)
        if errs:
            print("  (student raised on %d turns, scored as all-PASS)" % errs)
        if driver == "student":
            print("\n  The gap between the two tables is the covariate shift. A student that is")
            print("  strong above and weak here has learned the mapping and not the trajectory,")
            print("  which is exactly and only what DAgger fixes.")
        _ = tot


if __name__ == "__main__":
    main()
