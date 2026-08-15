"""One day, hour by hour, unit by unit: our ops against the tape's, with the tile each acted on.

The grid in `breakdown.py` says *that* a day diverged -- `place 4/5` -- and can never say *where*.
This prints the day at full resolution so the missing op can be found at the hour it should have
happened.

Both sides play their own game from the same seed and schedule, so this is NOT teacher-forced: it is
the same run `breakdown.py` grades, which is the point. A teacher-forced trace answers "would we
agree on his board", and the acceptance criterion is our board.

Tiles are read from the PREVIOUS turn's observation, because `steps[t]` records where a unit ended
up after acting, not where it stood when it acted. At dawn the units are teleported home
(`kaggriculture.py:848-849`), so turn 0 of a day reads its own record instead. Same rule as
`extract_tape.py`; getting it wrong shifts every tile one move forward.

    python -u scripts/day_ops.py --day 0
    python -u scripts/day_ops.py --day 0 --only PLACE,FEED,CARE
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

import breakdown as B

TPD = 24
SKIP = {"PASS", "NORTH", "SOUTH", "EAST", "WEST"}


def positions(obs, seat):
    farm = obs["farms"][seat]
    out = [tuple(farm.get("farmer") or (4, 4))]
    for h in (farm.get("hands") or []):
        out.append(tuple(h if isinstance(h, (list, tuple)) else h.get("pos", (4, 4))))
    return out


def trace(make0, opp, seed, weeds, economy, day):
    """`{hour: [(unit, op, arg, tile), ...]}` plus the market orders, for one day of one policy."""
    from kaggle_environments import make
    env = make("kaggriculture", configuration=dict(economy or {}, seed=seed,
                                                   weedSpawnChance=weeds), debug=True)
    env.reset(2)
    p0, p1 = make0(), opp()
    ops = collections.defaultdict(list)
    orders = collections.defaultdict(list)
    money = {}
    prev = None
    for t in range((day + 1) * TPD):
        o0, o1 = env.state[0].observation, env.state[1].observation
        here = positions(o0, 0)
        at = here if t % TPD == 0 else (prev or here)
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        if t // TPD == day:
            h = t % TPD
            if h == 0:
                money["dawn"] = float(o0["farms"][0]["money"])
            for u, a in enumerate([a0["farmer"]] + list(a0["hands"] or [])[:n0]):
                if a and a[0] not in SKIP:
                    ops[h].append((u, a[0], (a[1] if len(a) > 1 else None),
                                   at[u] if u < len(at) else None))
            for o in (a0.get("market") or []):
                if o:
                    orders[h].append(tuple(o))
        prev = here
        env.step([a0, a1])
        if t // TPD == day and t % TPD == TPD - 1:
            money["dusk"] = float(env.state[0].observation["farms"][0]["money"])
    return ops, orders, money


def fmt(entries, only):
    out = []
    for u, op, arg, tile in entries:
        if only and op not in only:
            continue
        cell = f"{tile[0]},{tile[1]}" if tile else "?"
        out.append(f"u{u}:{op}{'/' + str(arg) if arg else ''}@{cell}")
    return " ".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="victor", choices=sorted(B.TAPES))
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--day", type=int, default=0)
    ap.add_argument("--only", default="", help="comma-separated ops to show, e.g. PLACE,FEED")
    ap.add_argument("--market", action="store_true", help="also print the market orders")
    args = ap.parse_args()

    only = {s.strip().upper() for s in args.only.split(",") if s.strip()}
    B.schedule_agent = importlib.import_module("kagg.search." + args.module)

    replay, schedule, team = B.TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    economy = B.env_config(replay)
    opp = lambda: B.tape_policy(replay, team, 1)

    his, his_ord, his_money = trace(lambda: B.tape_policy(replay, team, 0), opp,
                                    args.seed, args.weeds, economy, args.day)
    mine = lambda: (lambda a: (lambda o, t: a(o)))(
        B.schedule_agent.make_agent(thin, 0, router=True))
    ours, our_ord, our_money = trace(mine, opp, args.seed, args.weeds, economy, args.day)

    row = sched.get(args.day, {})
    print(f"day {args.day}   seed {args.seed}   tape {args.tape}")
    print(f"schedule row: hands={row.get('hands')} land={row.get('land')} "
          f"plants={len(row.get('plants') or [])} places={row.get('places')} "
          f"animals={row.get('animals_bought')} sells={row.get('sells')} buys={row.get('buys')}")
    print(f"money  ours {our_money.get('dawn', 0):,.0f} -> {our_money.get('dusk', 0):,.0f}   "
          f"tape {his_money.get('dawn', 0):,.0f} -> {his_money.get('dusk', 0):,.0f}")
    print()
    for h in range(TPD):
        o, t = fmt(ours.get(h, []), only), fmt(his.get(h, []), only)
        om = " ".join("".join(str(x) for x in c) for c in our_ord.get(h, [])) if args.market else ""
        tm = " ".join("".join(str(x) for x in c) for c in his_ord.get(h, [])) if args.market else ""
        if not (o or t or om or tm):
            continue
        mark = "   " if o == t else " * "
        print(f"h{h:02d}{mark}OURS {o}{('  | ' + om) if om else ''}")
        print(f"      TAPE {t}{('  | ' + tm) if tm else ''}")

    print()
    for name, d in (("ours", ours), ("tape", his)):
        c = collections.Counter(op for v in d.values() for _u, op, _a, _t in v)
        print(f"  {name}: {dict(sorted(c.items()))}")


if __name__ == "__main__":
    main()
