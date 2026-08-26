"""Per day, what the schedule row ASKS for against what we actually emit.

Alex, 2026-08-26: *"implement it solve each day and let me know how and why you are not doing it"*,
after finding that d12's row names 60 units of sells across four products and we emitted none.

This is the compliance report that should have existed before any of the day's theories. Every row
field that maps onto an emitted action is counted from the ACTION STREAM -- what the agent actually
sent to the environment -- and put next to the number the row asked for.

    sells       row `sells` totals, against SELL orders emitted. **Orders are not fills**, so this
                counts what we ASKED to sell; a shortfall here is ours, a shortfall in fills could
                be the book. See `feedback_offers_are_not_fills`.
    plants      row `plants` length, against PLANT ops
    seeds       row `seeds` totals, against BUY_SEED orders
    places      row `places` length, against PLACE ops
    feeds       row `feeds`, against FEED ops
    cares       row `cares`, against CARE ops
    hires       row `hires`, against HIRE orders

A row asks for a DAY TOTAL, so these are day totals. The point is not that every number matches --
the board can refuse a PLANT, the shed can be empty -- it is to see WHICH fields we systematically
under-deliver, and from which day.
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
FIELDS = ("sells", "plants", "seeds", "places", "feeds", "cares", "hires")


def asked(row):
    """What the row wants, as one integer per field."""
    def total(v):
        if isinstance(v, dict):
            return sum(int(x or 0) for x in v.values())
        if isinstance(v, list):
            return len(v)
        return int(v or 0)
    return {f: total(row.get(f)) for f in FIELDS}


def emitted(actions):
    """What we actually sent that day, counted the same way."""
    got = collections.Counter()
    for a in actions:
        for op in [a.get("farmer") or ["PASS"]] + list(a.get("hands") or []):
            name = op[0] if op else "PASS"
            if name == "PLANT":
                got["plants"] += 1
            elif name == "PLACE":
                got["places"] += 1
            elif name == "FEED":
                got["feeds"] += 1
            elif name == "CARE":
                got["cares"] += 1
        for o in (a.get("market") or []):
            if not o:
                continue
            if o[0] == "SELL":
                got["sells"] += int(o[2] if len(o) > 2 else 0)
            elif o[0] == "BUY_SEED":
                got["seeds"] += int(o[2] if len(o) > 2 else 0)
            elif o[0] == "HIRE":
                got["hires"] += 1
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="clone_open")
    ap.add_argument("--seed", type=int, default=123641874)
    ap.add_argument("--handover", type=int, default=12)
    ap.add_argument("--from-day", type=int, default=12)
    ap.add_argument("--to-day", type=int, default=29)
    args = ap.parse_args()

    from kaggle_environments import make
    import scripts.breakdown as B
    from kagg.search import schedule_agent as SA

    rel, sched_rel, team = B.TAPES[args.tape]
    path = str(REPO / rel)
    economy = B.env_config(path)
    shops = B.recorded_shops(path)
    tape = B.tape_policy(path, team, 0)

    raw = json.loads((REPO / sched_rel).read_text())
    sched = {int(k): v for k, v in raw.items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    ours = SA.make_agent(thin, 0, router=True, start_day=args.handover)

    env = make("kaggriculture", configuration=dict(economy, seed=args.seed), debug=False)
    env.reset(2)
    opp = B.tape_policy(path, team, 1)

    by_day = collections.defaultdict(list)
    for t in range(719):
        env.state[0].observation.town["unlocked_shops"] = list(shops(t))
        env.state[1].observation.town["unlocked_shops"] = list(shops(t))
        obs = env.state[0].observation
        a0 = tape(obs, t) if t < args.handover * TPD else ours(obs)
        by_day[t // TPD].append(a0)
        env.step([a0, opp(env.state[1].observation, t)])

    print(f"tape {args.tape}  seed {args.seed}  handover d{args.handover}")
    print("row ASKS / we EMIT, per day\n")
    print(f"{'day':>4}  " + "".join(f"{f:>14}" for f in FIELDS))
    short = collections.Counter()
    for day in range(args.from_day, args.to_day + 1):
        want = asked(sched.get(day) or {})
        got = emitted(by_day.get(day) or [])
        cells = []
        for f in FIELDS:
            w, g = want[f], got[f]
            cells.append(f"{g:>6}/{w:<7}" if w or g else f"{'-':>14}")
            if g < w:
                short[f] += w - g
        print(f"{day:>4}  " + "".join(cells))

    print(f"\ntotal SHORTFALL d{args.from_day}-d{args.to_day} (row asked, we did not do):")
    for f, n in short.most_common():
        print(f"   {f:<10}{n:>6}")


if __name__ == "__main__":
    main()
