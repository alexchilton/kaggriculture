"""Play a trained checkpoint in the REAL environment against the planner, and report what happened.

**Why this is not `scripts/play_checkpoint.py`.** That one drives our own simulator, and a simulator
cannot see a defect that lives in the gap between the simulator and the environment. The review on
2026-08-20 found exactly one of those: `orders_from_heads` emitted every SELL last, because a bundle
is a sorted multiset and SELL sorts after HIRE, while the environment settles order slots in
sequence and both simulators lay them out sells-first. Every sim-side test passed. The real
environment would have refused the hires. Nothing in this repo would have caught it.

So this exists to run the actual `kaggle_environments` env, through the actual
`kagg.agents.neural.make_agent`, and report three things:

  1. **W/D/L and the banks** -- not a win rate. The reward pays 0.5 for a draw, and two policies
     that both bank $0 draw with certainty because `money == money` is exact. A rate near 0.5 and
     "draws everything" are the same number. This project has already drawn a whole day's
     conclusions from rates that a five-minute replay contradicted.
  2. **What the agent actually DID** -- the op mix and the market rate. A student that banks $3,000
     is a student that never traded, and the op mix says whether it also never farmed.
  3. **Whether the orders it emitted were legal and in slot order**, checked per turn against the
     environment's own rules rather than against our model of them.

    python -u scripts/play_in_the_real_env.py --checkpoint /home/alex/bc_bundle.best.pkl --games 4
"""

import argparse
import collections
import pathlib
import random
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.il import market_bundles as MB                      # noqa: E402

TEACHER = "submission/main.py"

#: The order the environment gives slots in. `kagg/sim/game.py:70-77`.
SLOT_RANK = {op: i for i, op in enumerate(MB.SLOT_ORDER)}


def load_teacher(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("teacher_%d" % random.randrange(1 << 30), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.agent


def audit(action, report):
    """Everything checkable about one emitted action, without trusting our own decoder."""
    market = action.get("market") or []
    report["turns"] += 1
    if market:
        report["turns_with_orders"] += 1
    if len(market) > 10:
        report["over_ten_orders"] += 1

    ranks = []
    for o in market:
        if not isinstance(o, (list, tuple)) or not o:
            report["malformed_orders"] += 1
            continue
        op = str(o[0])
        report["orders"][op] += 1
        ranks.append(SLOT_RANK.get(op, 99))
        if op in ("SELL", "BUY_PRODUCT", "BUY_SEED"):
            # The environment rejects a quantity-less or non-positive order outright.
            if len(o) < 3 or not isinstance(o[2], int) or o[2] <= 0:
                report["bad_quantities"] += 1
    if ranks != sorted(ranks):
        report["out_of_slot_order"] += 1

    for act in [action.get("farmer")] + list(action.get("hands") or []):
        if act:
            report["ops"][str(act[0])] += 1


def play(seed, student, teacher, report, student_seat):
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    agents = [None, None]
    agents[student_seat] = student
    agents[1 - student_seat] = teacher

    errors = 0
    while not env.done:
        acts = []
        for seat in (0, 1):
            ob = env.state[seat].observation
            try:
                a = agents[seat](ob, env.configuration)
            except Exception as exc:                          # noqa: BLE001
                if seat == student_seat:
                    errors += 1
                    if errors <= 3:
                        print("   student raised: %r" % (exc,), flush=True)
                a = {"farmer": ["PASS"], "hands": [], "market": []}
            if seat == student_seat:
                audit(a, report)
            acts.append(a)
        env.step(acts)

    banks = [(s.get("reward") or 0.0) for s in env.steps[-1]]
    return banks[student_seat], banks[1 - student_seat], errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--teacher", default=TEACHER)
    ap.add_argument("--games", type=int, default=4)
    ap.add_argument("--seed-base", type=int, default=7_000_000)
    args = ap.parse_args()

    from kagg.agents import neural
    student = neural.make_agent(args.checkpoint)
    teacher = load_teacher(args.teacher)

    report = collections.defaultdict(int)
    report["orders"] = collections.Counter()
    report["ops"] = collections.Counter()

    w = d = ll = 0
    rows = []
    t0 = time.time()
    for g in range(args.games):
        seed = args.seed_base + g
        # Alternate seats. Seat 0 acts first in each turn's ordering, and a result measured on one
        # seat only cannot tell a real edge from a seat advantage.
        seat = g % 2
        mine, theirs, errs = play(seed, student, teacher, report, seat)
        if mine > theirs:
            w += 1
        elif mine == theirs:
            d += 1
        else:
            ll += 1
        rows.append((g, seed, seat, mine, theirs, errs))
        print("game %d seed %-9d seat %d  student $%-10.0f teacher $%-10.0f errs %d"
              % (g, seed, seat, mine, theirs, errs), flush=True)

    print("\n=== %d games in %.0fs ===" % (args.games, time.time() - t0))
    print("W/D/L                : %d/%d/%d" % (w, d, ll))
    print("student bank mean    : $%.0f" % (sum(r[3] for r in rows) / max(1, len(rows))))
    print("teacher bank mean    : $%.0f" % (sum(r[4] for r in rows) / max(1, len(rows))))

    turns = max(1, report["turns"])
    print("\nWHAT THE STUDENT DID (%s turns)" % format(turns, ","))
    print("  turns with orders   : %.1f%%   (teacher's own rate is 21.1%%)"
          % (100.0 * report["turns_with_orders"] / turns))
    print("  market orders       : %s"
          % (", ".join("%s x%d" % (k, v) for k, v in report["orders"].most_common()) or "NONE"))
    print("  unit ops            : %s"
          % ", ".join("%s %.1f%%" % (k, 100.0 * v / max(1, sum(report["ops"].values())))
                      for k, v in report["ops"].most_common(8)))

    print("\nLEGALITY")
    for key, label in (("out_of_slot_order", "turns whose orders were NOT in slot order"),
                       ("bad_quantities", "orders with a missing or non-positive quantity"),
                       ("malformed_orders", "malformed orders"),
                       ("over_ten_orders", "turns emitting more than ten orders")):
        n = report[key]
        print("  %-46s %d%s" % (label, n, "   <-- BUG" if n else ""))

    # The two failure modes worth naming, because both look like a working agent from a distance.
    if report["turns_with_orders"] == 0:
        print("\n*** The student never placed a single order. It banked its $3,000 start and did "
              "nothing. This is the six-marginals failure, and no loss curve shows it. ***")
    if d == args.games:
        print("\n*** Every game drew. Two policies that both bank $0 draw with certainty, so a "
              "drawn sweep is evidence of doing nothing, not of being evenly matched. ***")


if __name__ == "__main__":
    main()
