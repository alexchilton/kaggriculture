"""29 independent one-day tests from Seb's own board. Matched conditions. THE PLANNER ONLY.

Every season-long comparison against the tape confounds two things: whether our planner schedules a
day better than his, and whether the board it wakes up to is the one his planner would have built.
By day 16 those are wildly different boards -- different pens in different places, a different herd,
a different bank -- so a day-by-day column says nothing about the algorithm.

This removes the second one. For each day D, replay HIS tape from turn 0 to D's dawn, so the board,
the crew, the crops, the pens, the water debt and the shed are byte-identical, and then run ONE day
with each planner from that identical dawn. Twenty-nine independent experiments, no compounding.

The shed is stocked at each dawn (`WHEAT 200`, `FERTILIZER 100`) for the same reason: a planner that
cannot feed because the wheat is not there is not a planner failure, and leaving it in makes the
supply the experiment instead of the schedule.

Geometry is deliberately NOT an arm here and CANNOT be one: its whole effect is cumulative -- a pen
sited near the depot on day 3 pays back for twenty-five days -- and resetting to his board every dawn
erases exactly that. Geometry is measured over a full season instead.

Day 29 is excluded: the env raises `Environment done` on the final step.

    python -u scripts/matched_days.py 2>&1 | tee data/logs/matched29.log
"""
import argparse
import collections
import json
import pathlib

from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy, DEFAULT_TAPE


def _plants(obs):
    tiles = obs["farms"][0]["tiles"]
    return {(x, y): dict(c) for y, r in enumerate(tiles) for x, c in enumerate(r)
            if isinstance(c, dict) and c.get("kind") == "PLANT"}


def _pens(obs):
    tiles = obs["farms"][0]["tiles"]
    return {(x, y) for y, r in enumerate(tiles) for x, c in enumerate(r)
            if isinstance(c, dict) and c.get("animal")}


def one_day(day, use_ours, seed=11, flags=()):
    """Replay the tape to `day`'s dawn, then run that single day with one planner or the other.

    `flags` is `[(module_attr, value)]` set on `schedule_agent` before the day runs, so an arm is a
    command-line switch rather than an edit -- and so the two arms are guaranteed to differ in
    exactly the named constant. An in-process toggle that silently reset on import once made a revert
    check pass here that should have failed, which is why this sets them per call.
    """
    from kaggle_environments import make
    from kagg.search import schedule_agent as SA

    for name, value in flags:
        setattr(SA, name, value)

    replay, schedule, team = TAPES[DEFAULT_TAPE]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    tape0, opp = tape_policy(replay, team, 0), tape_policy(replay, team, 1)
    ours = SA.make_agent(thin, 0, router=True)
    work = collections.Counter()
    plants0 = pens0 = None
    for t in range(24 * (day + 1)):
        o0, o1 = env.state[0].observation, env.state[1].observation
        if t == 24 * day:
            priv = o0.get("private") or {}
            priv["shed"]["WHEAT"] = 200
            priv["shed"]["FERTILIZER"] = 100
            plants0, pens0 = _plants(o0), _pens(o0)
        a0 = ours(o0) if (use_ours and t >= 24 * day) else tape0(o0, t)
        a1 = opp(o1, t)
        if t >= 24 * day:
            for act in [a0["farmer"], *a0["hands"]]:
                if isinstance(act, list) and act:
                    work[act[0]] += 1
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    end = env.state[0].observation
    tiles = end["farms"][0]["tiles"]
    dead = [k for k in plants0
            if isinstance(tiles[k[1]][k[0]], dict) and tiles[k[1]][k[0]].get("kind") == "WEED"]
    thirst = [k for k in dead if not plants0[k].get("watered_today")
              and plants0[k].get("consecutive_unwatered", 0) >= 1]
    return dict(lost=len(pens0 - _pens(end)), thirst=len(thirst),
                h=work["HARVEST"], p=work["PASS"], drop=work["DROP"], pick=work["PICKUP"])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=29)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--no-fund", action="store_true",
                    help="switch FUND_THE_DAY_WHEN_SHORT off, to attribute the cash-shortfall rush")
    args = ap.parse_args()
    flags = [("FUND_THE_DAY_WHEN_SHORT", False)] if args.no_fund else []

    print(f"  arm: FUND_THE_DAY_WHEN_SHORT={not args.no_fund}")
    print(f"  {'day':>4} | {'ANIMALS':>9} | {'THIRST':>9} | {'HARVEST':>10} | {'PASS':>10} "
          f"| {'DROP':>9}")
    total, worse = collections.Counter(), []
    for day in range(args.days):
        a, b = one_day(day, True, args.seed, flags), one_day(day, False, args.seed, flags)
        for k in ("lost", "thirst", "h", "p", "drop"):
            total["us_" + k] += a[k]
            total["seb_" + k] += b[k]
        if a["lost"] > b["lost"] or a["thirst"] > b["thirst"]:
            worse.append(day)
        print(f"  {day:>4} | {a['lost']:>4} ({b['lost']:>2}) | {a['thirst']:>4} ({b['thirst']:>2}) "
              f"| {a['h']:>5} ({b['h']:>3}) | {a['p']:>5} ({b['p']:>3}) "
              f"| {a['drop']:>4} ({b['drop']:>2}) |"
              + ("  <-- WORSE" if day in worse else ""))
    print(f"\n  {args.days}-DAY TOTALS       ours     Seb")
    for k, label in (("lost", "animals lost"), ("thirst", "thirst deaths"),
                     ("h", "HARVEST ops"), ("p", "PASS turns"), ("drop", "DROP ops")):
        print(f"  {label:>20}  {total['us_' + k]:>6}  {total['seb_' + k]:>6}")
    print(f"  days we are worse: {worse}")


if __name__ == "__main__":
    main()
