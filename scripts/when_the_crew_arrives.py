"""We hire the same number of hands as the tape and get fewer turns out of them. When do they land?

`scripts/breakdown.py` turned up a deficit that is present on day 0, before anything else has parted:

    unit-turns   d0 176/185   d1 176/185   d2 176/185   d3 176/185   d6 135/208   d9 70/276
    hire         d0     7/7   d1     7/7   d2     7/7   d3     7/7   d6     8/8   d9   11/11

Identical crew, fewer turns. Hands are dismissed nightly and re-hired each dawn, so the only way to
own seven hands and work them less is to hire them LATER IN THE DAY. A hand hired at hour 6 is worth
18 turns; the same hand at hour 1 is worth 23. Nothing downstream can recover the difference.

This prints, for each day, the number of hands standing at every one of the 24 hours, ours against
the tape, plus the hour each HIRE order was placed and the bank at that moment. If the tape's row
fills earlier the loss is hiring latency, and the question becomes what delays it -- the schedule's
`hires` row, the 9-order cap, or the bank.

    python -u scripts/when_the_crew_arrives.py --days 11
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy, DEFAULT_TAPE


def run(make0, opp, seed, weeds, days):
    """Return per-day hand counts by hour, HIRE hours, and the bank when each HIRE was sent."""
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=True)
    env.reset(2)
    p0, p1 = make0(), opp()
    hands = collections.defaultdict(list)      # day -> [hands standing at each hour]
    hires = collections.defaultdict(list)      # day -> [(hour, bank at that hour)]
    for t in range(719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        day, hour = t // 24, t % 24
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        if day < days:
            hands[day].append(n0)
            for o in (a0["market"] or []):
                if o and o[0] == "HIRE":
                    hires[day].append((hour, int(o0["farms"][0]["money"])))
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
    bad = [(s, env.state[s].status) for s in (0, 1) if env.state[s].status != "DONE"]
    if bad:
        raise RuntimeError(f"seat status {bad}")
    return hands, hires


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default=DEFAULT_TAPE, choices=sorted(TAPES))
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--days", type=int, default=11)
    args = ap.parse_args()

    replay, schedule, team = TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    opp = lambda: tape_policy(replay, team, 1)

    his, his_hires = run(lambda: tape_policy(replay, team, 0), opp, args.seed, args.weeds, args.days)
    a = schedule_agent.make_agent(thin, 0, router=True)
    ours, our_hires = run(lambda: (lambda o, t: a(o)), opp, args.seed, args.weeds, args.days)

    print(f"tape {args.tape}   seed {args.seed}   weeds {args.weeds}\n")
    print("  hands standing at each hour 0..23, and the hand-turns that buys\n")
    print(f"  {'day':>3}  {'who':<5} {'hours 0..23':<50} {'hand-turns':>11} {'delta':>7}")
    for d in range(args.days):
        o, h = ours.get(d, []), his.get(d, [])
        for lab, row in (("ours", o), ("tape", h)):
            turns = sum(row)
            delta = f"{turns - sum(h):+d}" if lab == "ours" else ""
            strip = "".join(f"{n:x}" if n < 16 else "+" for n in row)
            print(f"  {d if lab == 'ours' else '':>3}  {lab:<5} {strip:<50} {turns:>11} {delta:>7}")
        print()

    print("  HIRE orders -- (hour, bank when sent)\n")
    for d in range(args.days):
        print(f"  {d:>3}  ours {str(our_hires.get(d, [])):<58}")
        print(f"  {'':>3}  tape {str(his_hires.get(d, [])):<58}")


if __name__ == "__main__":
    main()