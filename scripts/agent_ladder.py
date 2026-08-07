"""Does the winner's own schedule, driven through OUR agent, bank what the winner banked?

This is the only input to this project that cannot be tuned against, and adopting it exposed that a
day of "improvements" had been measured on a schedule that was simultaneously being tuned to route
around the agent's faults -- 46% on that plan against 8% on the winner's. The gap was the size of the
self-deception, and it is the reason this script exists rather than a bench against our own plan.

    1. tape A                       -> game                the anchor, ~$127k
    2. winner's schedule -> agent(router=False) -> game    the per-turn greedy
    3. winner's schedule -> agent(router=True)  -> game    the Team Orienteering solve

Arms 2 and 3 differ in exactly one thing -- `kagg/search/router.py` -- and run in one process on one
explicit seed list, because `env.reset()` draws a fresh seed on every call and one identical tape
banked $59,199 / $53,015 / $48,965 / $48,144. An unseeded figure here is not a rough measurement, it
is no measurement.

Both seats are driven: the tape's opponent holds seat 1 in every arm, so the market is contested
identically. Weeds default OFF, which is how the agent work has been measured all along; `--weeds`
puts them back.
"""

import argparse
import collections
import json
import pathlib
import statistics
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent

REPLAY = pathlib.Path("data/seed_scripts/new_leader/90016067.json")
SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
TEAM = "somewhere after"

#: The four fields only a REPLAY can supply, stripped so the agent is measured on the shape our own
#: optimiser can actually emit: counts per day, and not one tile coordinate.
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


def tape_plans(replay=None, team=None):
    """Both seats' actions from a replay. `replay`/`team` default to the original leader's tape.

    Parameterised so fidelity can be measured against SEVERAL strong players rather than one. Fitting
    the executor to a single tape is how you end up tuning to that tape's quirks -- Seb buys all four
    quadrants by day 10 and runs 19 pens against the original's 14, so an executor that only ever met
    the original has never been asked to move a twelve-hand crew across a hundred tiles.
    """
    d = json.loads((replay or REPLAY).read_text())
    seat = d["info"]["TeamNames"].index(team or TEAM)
    mine, theirs = [], []
    for step in d["steps"][1:]:           # index 0 is the reset placeholder and is never applied
        for src, dst in ((seat, mine), (1 - seat, theirs)):
            a = (step[src] or {}).get("action") or {}
            dst.append([a.get("farmer", ["PASS"]) or ["PASS"],
                        list(a.get("hands") or []), list(a.get("market") or [])])
    return mine, theirs


def _env(seed, weeds):
    from kaggle_environments import make
    cfg = {"seed": int(seed), "weedSpawnChance": float(weeds)}
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    return env


def play(make_us, theirs, seed, weeds, tally=None):
    """One season at an EXPLICIT seed. `make_us` builds a fresh seat-0 policy; seat 1 is the tape."""
    env = _env(seed, weeds)
    us = make_us()
    for t in range(719):
        obs = env.state[0].observation
        ours = us(obs)
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        n0 = len(env.state[0].observation["farms"][0].get("hands") or [])
        n1 = len(env.state[0].observation["farms"][1].get("hands") or [])
        if tally is not None:
            for a in [ours["farmer"], *ours["hands"]]:
                tally[a[0] if isinstance(a, list) and a else "PASS"] += 1
        env.step([{"farmer": ours["farmer"], "hands": list(ours["hands"])[:n0],
                   "market": ours["market"]},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        if env.state[0].status == "DONE":
            break
    farm = env.state[0].observation["farms"][0]
    return float(farm["money"]), env


def play_live(make_a, make_b, seed, weeds):
    """Both seats driven by LIVE agents, so the shared order book is genuinely contested.

    **Every other arm in this file drives seat 1 from a fixed replay, and that is a blind spot with a
    measured price.** Two of our own leaderboard games:

        opponent       our units sold   milk price d15-29   final
        Sophie                   1058               101.1   $103,367  LOST
        Mohit Babel              1017               225.1   $128,735  WON

    We sold MORE units in the game we lost and banked $25,368 less. `market_price` falls monotonically
    in a book BOTH seats sell into (`kaggriculture.py:177`), and it is shallow where we live -- fifty
    units of milk above I0 takes it from $160 to $55. A tape opponent contests only in whatever way
    that one recorded season happened to, so no measurement taken against it says anything about a
    game against a player selling the same goods at the same time.

    That is this project's own "never tune or evaluate against `starter` alone" rule, and both attempts
    to make selling cleverer -- the 0.5x price floor at -$16,025 and the per-day quota cap at -$2,653 --
    were scored in exactly that blind spot. Neither number is evidence about a contested market.

    A mirror is the HARSHEST contention available: identical crop mix, identical sell cadence, the same
    goods hitting the book on the same turn. It is deliberately not a selection criterion -- CLAUDE.md
    records that a mirror answers "what is best if both sides play it", which is a symmetric
    equilibrium and pointed the melon count the wrong way twice. Use it as a STRESS TEST for the
    market half, and select on the field.

    Returns `(bank_a, bank_b)`.
    """
    env = _env(seed, weeds)
    a, b = make_a(), make_b()
    for _t in range(719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        x, y = a(o0), b(o1)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": x["farmer"], "hands": list(x["hands"])[:n0], "market": x["market"]},
                  {"farmer": y["farmer"], "hands": list(y["hands"])[:n1], "market": y["market"]}])
        if env.state[0].status == "DONE":
            break
    farms = env.state[0].observation["farms"]
    return float(farms[0]["money"]), float(farms[1]["money"])


def play_tape(mine, theirs, seed, weeds):
    env = _env(seed, weeds)
    for t in range(min(len(mine), 719)):
        obs = env.state[0].observation
        f0, h0, m0 = mine[t]
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        n0 = len(obs["farms"][0].get("hands") or [])
        n1 = len(obs["farms"][1].get("hands") or [])
        env.step([{"farmer": f0, "hands": list(h0)[:n0], "market": m0},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        if env.state[0].status == "DONE":
            break
    return float(env.state[0].observation["farms"][0]["money"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="11,22,33,44,55")
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--schedule", default=str(SCHEDULE))
    ap.add_argument("--arms", default="tape,greedy,router")
    ap.add_argument("--replay", default=str(REPLAY))
    ap.add_argument("--team", default=TEAM)
    args = ap.parse_args()
    seeds = [int(s) for s in args.seeds.split(",")]
    arms = args.arms.split(",")

    mine, theirs = tape_plans(pathlib.Path(args.replay), args.team)
    sched = {int(k): v for k, v in json.loads(pathlib.Path(args.schedule).read_text()).items()}
    for r in sched.values():
        for k in TAPE_ONLY:
            r[k] = []

    got, ops = {}, {}
    if "tape" in arms:
        got["1. tape A                            -> game"] = [
            play_tape(mine, theirs, s, args.weeds) for s in seeds]
    for name, label, flag in (("greedy", "2. schedule -> agent(greedy) -> game", False),
                              ("router", "3. schedule -> agent(router) -> game", True)):
        if name not in arms:
            continue
        tally = collections.Counter()
        got[label] = [play(lambda: schedule_agent.make_agent(sched, 0, router=flag),
                           theirs, s, args.weeds, tally)[0] for s in seeds]
        ops[label] = tally

    # The contested arm. Seat 1 is our own agent, so both seats sell the same goods on the same turns
    # into one book -- the only arm here that can see market contention at all.
    mirror = None
    if "mirror" in arms:
        pairs = [play_live(lambda: schedule_agent.make_agent(sched, 0, router=True),
                           lambda: schedule_agent.make_agent(sched, 1, router=True),
                           s, args.weeds) for s in seeds]
        got["4. router vs ROUTER (contested book)"] = [p[0] for p in pairs]
        mirror = pairs

    base = statistics.mean(next(iter(got.values())))
    print(f"seeds {seeds}   weedSpawnChance {args.weeds}   both seats driven from the tape")
    print(f"{'':<40} {'mean':>10} {'min':>10} {'max':>10} {'% of arm 1':>11}")
    for label, v in got.items():
        print(f"  {label:<38} ${statistics.mean(v):>9,.0f} ${min(v):>9,.0f} "
              f"${max(v):>9,.0f} {100 * statistics.mean(v) / base:>10.0f}%")
    if mirror:
        # Money is not the point of this arm; contention is. Both seats run the SAME policy, so the
        # bank each ends on is a statement about the shared book, not about strategy -- and a mirror
        # win rate is 0.5 by construction, which is exactly why it must not be selected on.
        both = [b for pair in mirror for b in pair]
        print(f"\n  contested book: mean bank per seat ${statistics.mean(both):>9,.0f}   "
              f"min ${min(both):,.0f}   max ${max(both):,.0f}")
        solo = got.get("3. schedule -> agent(router) -> game")
        if solo:
            tax = statistics.mean(solo) - statistics.mean(both)
            print(f"  the same agent against a TAPE banks ${statistics.mean(solo):,.0f}, so a genuinely "
                  f"contested\n  order book costs ${tax:,.0f} a season "
                  f"({100 * tax / max(1.0, statistics.mean(solo)):.0f}%). Any change to the market half "
                  f"must be\n  scored HERE, not against the tape.")

    for label, tally in ops.items():
        n = len(seeds)
        work = {k: v // n for k, v in tally.items()
                if k not in ("PASS", "NORTH", "SOUTH", "EAST", "WEST")}
        moves = sum(v for k, v in tally.items() if k in ("NORTH", "SOUTH", "EAST", "WEST")) // n
        print(f"\n  {label}   per season, averaged over {n} seeds")
        print(f"    PASS {tally['PASS'] // n}   moves {moves}   "
              f"moves per work op {moves / max(1, sum(work.values())):.2f}")
        for k in sorted(work, key=lambda k: -work[k]):
            print(f"    {k:<20} {work[k]}")


if __name__ == "__main__":
    main()
