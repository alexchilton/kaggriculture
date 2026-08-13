"""What does day N actually require, and how does the tape spend its turns against how we spend ours?

Days 0-3 only. The routing patches all failed the same way -- each moved one op a few hours and paid
for it somewhere else -- because they tuned the inputs of a greedy insertion heuristic instead of
solving the day. Before writing an optimiser, this establishes the ground truth it has to beat:

    the task list    what the schedule row and the board REQUIRE today, with the precedence between
                     them (BUILD -> PLACE -> FEED/CARE, and a PICKUP before anything that consumes)
    the tape's day   per unit, per hour: what it did and where it stood
    our day          the same, side by side

The whole day is deterministic given the crew and the purchases -- weeds are off and the only genuine
uncertainty is the bank, which constrains buying and not routing. So a day plan can be solved once at
dawn rather than repaired hour by hour, and this measures the gap that has to close.

    python -u scripts/the_day_plan.py --day 0
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent
from scripts.breakdown import DEFAULT_TAPE, TAPES, TAPE_ONLY, tape_policy

WORK = ("PLANT", "WATER", "HARVEST", "FERTILIZE", "FEED", "CARE", "COLLECT_FERTILIZER",
        "DIG", "BUILD_COOP", "BUILD_PASTURE", "PLACE", "PICKUP", "DROP")
MOVES = ("NORTH", "SOUTH", "EAST", "WEST")


def timeline(policy_factory, opp_factory, seed, weeds, day):
    """Per-unit action and position for every hour of `day`, plus the dawn board."""
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=True)
    env.reset(2)
    p0, p1 = policy_factory(), opp_factory()
    rows, dawn = [], None
    for t in range(24 * (day + 1)):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        if t // 24 == day:
            if dawn is None:
                dawn = o0
            pos = [tuple(o0["farms"][0]["farmer"])] + [tuple(h) for h in
                                                       (o0["farms"][0].get("hands") or [])]
            acts = [a0["farmer"]] + list(a0["hands"] or [])[:n0]
            rows.append((t % 24, pos, [list(a) if a else ["PASS"] for a in acts],
                         int(o0["farms"][0]["money"])))
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
    return rows, dawn


def render(rows, label, width=8):
    """One column per unit, one row per hour. First letter of the op; '.' for a pass."""
    short = {"PLANT": "P", "WATER": "W", "HARVEST": "H", "FERTILIZE": "F", "FEED": "f",
             "CARE": "c", "COLLECT_FERTILIZER": "g", "DIG": "D", "BUILD_PASTURE": "B",
             "BUILD_COOP": "B", "PLACE": "L", "PICKUP": "u", "DROP": "d", "PASS": ".",
             "NORTH": "^", "SOUTH": "v", "EAST": ">", "WEST": "<"}
    print(f"\n  {label}   ^v>< = move, . = idle, upper = field work, lower = shed/herd\n")
    print(f"  {'hr':>3} {'bank':>7}  " + "".join(f"u{u}" .ljust(3) for u in range(width)))
    for hour, pos, acts, money in rows:
        cells = "".join(short.get(a[0], "?").ljust(3) for a in acts[:width])
        print(f"  {hour:>3} {money:>7}  {cells}")
    tally = collections.Counter(a[0] for _h, _p, acts, _m in rows for a in acts)
    work = sum(v for k, v in tally.items() if k in WORK)
    move = sum(v for k, v in tally.items() if k in MOVES)
    print(f"      work {work}   move {move}   idle {tally['PASS']}   "
          f"ops {dict(sorted((k, v) for k, v in tally.items() if k in WORK))}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default=DEFAULT_TAPE, choices=sorted(TAPES))
    ap.add_argument("--day", type=int, default=0)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    args = ap.parse_args()
    # Was capped at day 3 while the pre-land-buy window was the whole scope. Days 0-3 now match on
    # every plant, animal, feed and purchase, so the scope is the first land buy (day 4) to the
    # second (day 8).
    assert args.day <= 8, "days 0-8 only -- the window runs to the second land buy"

    replay, schedule, team = TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    opp = lambda: tape_policy(replay, team, 1)

    row = sched.get(args.day, {})
    print(f"tape {args.tape}   day {args.day}   seed {args.seed}   weeds {args.weeds}")
    print(f"\n  the day's REQUIREMENT, from the schedule row:")
    for k in ("hands", "hires", "builds", "places", "plants", "seeds", "buys", "sells",
              "animals_bought", "land"):
        if row.get(k):
            v = row[k]
            if isinstance(v, list):
                v = dict(collections.Counter(v))
            print(f"      {k:<16} {v}")

    his, _ = timeline(lambda: tape_policy(replay, team, 0), opp, args.seed, args.weeds, args.day)
    a = schedule_agent.make_agent(thin, 0, router=True)
    ours, _ = timeline(lambda: (lambda o, t: a(o)), opp, args.seed, args.weeds, args.day)

    render(his, "TAPE")
    render(ours, "OURS")


if __name__ == "__main__":
    main()