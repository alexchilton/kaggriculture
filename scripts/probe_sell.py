"""Per-turn trace of one product's shed level, hand-held stock, and the SELL we offered.

The sell caps in `schedule_agent` are a stack of four (`have`, the row, the carry, `rate`, and a
day-total) and the breakdown table only shows the day's outcome, so which cap bound an offer is not
readable from it. This prints, for every turn of a chosen day range, both sides' shed level, what we
were holding in hands, and the SELL order each side emitted -- which is enough to attribute a
shortfall to a cap rather than guess at one.

    python -u scripts/probe_sell.py --prod MILK --from-day 10 --to-day 17
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy


def trace(make0, opp, seed, weeds, prod, d0, d1):
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=True)
    env.reset(2)
    p0, p1 = make0(), opp()
    rows = []
    for t in range(719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        day, hour = t // 24, t % 24
        if d0 <= day < d1:
            priv = o0.get("private") or {}
            shed = int((priv.get("shed") or {}).get(prod, 0) or 0)
            hands = sum(collections.Counter(iv).get(prod, 0)
                        for iv in (priv.get("inventories") or []))
            sold = sum(int(o[2]) for o in (a0["market"] or [])
                       if o and o[0] == "SELL" and o[1] == prod)
            rows.append((day, hour, shed, hands, sold,
                         int(o0["farms"][0]["money"]),
                         int((o0.get("market") or {}).get("inventory", {}).get(prod, 0) or 0)))
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="seb", choices=sorted(TAPES))
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--prod", default="MILK")
    ap.add_argument("--from-day", type=int, default=10)
    ap.add_argument("--to-day", type=int, default=17)
    args = ap.parse_args()

    replay, schedule, team = TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    opp = lambda: tape_policy(replay, team, 1)

    his = trace(lambda: tape_policy(replay, team, 0), opp, args.seed, args.weeds,
                args.prod, args.from_day, args.to_day)
    a = schedule_agent.make_agent(thin, 0, router=True)
    ours = trace(lambda: (lambda o, t: a(o)), opp, args.seed, args.weeds,
                 args.prod, args.from_day, args.to_day)

    print(f"{args.prod}   ours | tape.   shed = in the shed at the START of the turn, "
          f"hand = held by units, sell = units OFFERED that turn, book = market inventory")
    print(f"{'day':>4}{'hr':>3} | {'shed':>5}{'hand':>5}{'sell':>5}{'book':>6} | "
          f"{'shed':>5}{'hand':>5}{'sell':>5}{'book':>6}")
    day_o = collections.Counter()
    day_h = collections.Counter()
    for (d, h, s, hd, sl, _m, bk), (d2, h2, s2, hd2, sl2, _m2, bk2) in zip(ours, his):
        assert (d, h) == (d2, h2)
        day_o[d] += sl
        day_h[d] += sl2
        if sl or sl2 or h == 23:
            print(f"{d:>4}{h:>3} | {s:>5}{hd:>5}{sl:>5}{bk:>6} | {s2:>5}{hd2:>5}{sl2:>5}{bk2:>6}")
        if h == 23:
            row = int(((sched.get(d) or {}).get("sells") or {}).get(args.prod, 0))
            print(f"     >> day {d}: OFFERED ours {day_o[d]}  tape {day_h[d]}   row asks {row}")
    print(f"\n  season-to-date offered: ours {sum(day_o.values())}  tape {sum(day_h.values())}")


if __name__ == "__main__":
    main()
