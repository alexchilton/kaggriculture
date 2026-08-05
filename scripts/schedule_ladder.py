"""How much of the tape survives each layer between it and the game. Fixed, matched seeds.

The question this answers is Alex's: the tape played straight into the game banks ~$127k, so **does the
schedule extracted from that tape, put back through our pipeline, bank the same?** If it does not, then
generating a schedule from an optimised choice of plants and animals is optimising into a lossy channel,
and no amount of search fixes it.

    1. tape A                          -> game        the anchor
    2. schedule WITH the tape's answers -> emitter -> game
    3. schedule with COUNTS ONLY        -> emitter -> game    what a scheduler can actually produce

**`env.reset()` draws a fresh random seed every call.** Nothing in `make("kaggriculture")` fixes it, and
`configuration.seed` defaults to None, so four replays of one identical tape banked $59,199 / $53,015 /
$48,965 / $48,144. A whole day of comparisons in this project were single draws from that spread, and one
of them inverted a real finding: the tape's tile coordinates measured as worth **-$4,368** (i.e. nothing)
on unfixed seeds and **+$23,470** once the seeds were matched.

`CLAUDE.md` already says "Seed variance is ~15%. Always quote the seed range." It was not being done.

So this script exists to make the comparison impossible to get wrong: every arm is played on the SAME
list of explicit seeds, both seats are driven, and the range is printed next to the mean.
"""

import argparse
import copy
import json
import pathlib
import statistics
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import dayplan
import build_script_submission as B

REPLAY = pathlib.Path("data/seed_scripts/new_leader/90016067.json")
SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
TEAM = "somewhere after"

#: The four fields only a REPLAY can supply. A generated schedule has none of them, so arm 3 is the
#: honest measure of our pipeline and arm 2 is an upper bound that smuggles in the tape's answers.
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


def tape_plans():
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    mine, theirs = [], []
    for step in d["steps"][1:]:            # index 0 is the reset placeholder and is never applied
        for src, dst in ((seat, mine), (1 - seat, theirs)):
            a = (step[src] or {}).get("action") or {}
            dst.append([a.get("farmer", ["PASS"]) or ["PASS"],
                        list(a.get("hands") or []), list(a.get("market") or [])])
    return mine, theirs


def play(plan, theirs, seed):
    """One season at an EXPLICIT seed, both seats driven. Returns our final bank."""
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=True)
    env.reset(2)
    for t in range(min(len(plan), 719)):
        obs = env.state[0].observation
        me = obs["farms"][0]
        f0, h0, m0 = plan[t]
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        n0 = len(me.get("hands") or [])
        n1 = len(obs["farms"][1].get("hands") or [])
        env.step([{"farmer": f0, "hands": list(h0)[:n0], "market": m0},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        if env.state[0].status == "DONE":
            break
    return float(env.state[0].observation["farms"][0]["money"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="11,22,33,44,55")
    args = ap.parse_args()
    seeds = [int(s) for s in args.seeds.split(",")]

    mine, theirs = tape_plans()
    full = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    thin = copy.deepcopy(full)
    for row in thin.values():
        for k in TAPE_ONLY:
            row[k] = []

    sa, ra = dayplan.emit(full)
    sb, rb = dayplan.emit(thin)
    arms = [("1. tape A                             -> game", mine),
            ("2. schedule WITH the tape's answers   -> game", B.build_plan(sa.arrays())),
            ("3. schedule with COUNTS ONLY          -> game", B.build_plan(sb.arrays()))]

    got = {}
    for label, plan in arms:
        got[label] = [play(plan, theirs, s) for s in seeds]

    base = statistics.mean(got[arms[0][0]])
    print(f"seeds {seeds}, both seats driven from the tape")
    print(f"{'':<46} {'mean':>10} {'min':>10} {'max':>10} {'% of tape':>10}")
    for label, _ in arms:
        v = got[label]
        print(f"  {label:<44} ${statistics.mean(v):>9,.0f} ${min(v):>9,.0f} "
              f"${max(v):>9,.0f} {100 * statistics.mean(v) / base:>9.0f}%")
    a, b, c = (statistics.mean(got[l]) for l, _ in arms)
    print()
    print(f"  cost of the schedule + emitter at all      ${a - b:>10,.0f}")
    print(f"  cost of losing the tape's tile coordinates ${b - c:>10,.0f}")
    print(f"  refusals: with the tape's tiles {len(ra['refused'])}, counts only {len(rb['refused'])}")


if __name__ == "__main__":
    main()
