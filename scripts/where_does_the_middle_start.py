"""Does d13 belong to the library or to the planner? And does the library agent beat the greedy?

Two questions, one command, one seed, so the two arms cannot silently differ in anything else.

**Q1, the boundary.** Alex, 2026-08-21: "the greedy wheat planting should only be in the days 13 plus
or whenever it is seen... till d12 it should just be tape matching". "Or whenever it is seen" is the
part that has to be measured: the crop-shape data says his pure-wheat run starts at d14, because d13
is still mixed STRAWBERRY+WHEAT, so d13 can be argued into either phase. Both are run against
Kawashigi's own recorded season and reported as a pair.

**Q2, win or loss.** Against the shipped greedy planner -- `schedule_agent` on `kagg/plan.py`'s
schedule -- on the same seed, BOTH SEATINGS. The leaderboard is Elo, so the selection criterion is
win/loss, never money (`CLAUDE.md`). Money is printed because a $2 win and a $40,000 win are
different information about the same result, not because it is the criterion.

**Weeds are 0.0** on every run here, per Alex 2026-08-21: "do it with weeds off to begin with".
That switches off RANDOM spawning only. A tile left two days unwatered becomes a WEED regardless
(`reference/kaggriculture.py:771`) and that path cannot be disabled, so a weed appearing at 0.0 is
our own missed watering. The ladder runs 0.005, so every number here is a CLEAN-ROOM number and must
not be carried forward as a ladder estimate.

    python -u scripts/where_does_the_middle_start.py --seed 11
"""

import argparse
import collections
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

import scripts.breakdown as BD                                              # noqa: E402
from kagg.search import kawa_library_agent, kawa_rows                       # noqa: E402

TAPE = "kawashigi"
WEEDS = 0.0
CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")


def live_crops(snapshot):
    return sum(snapshot.get("crop_" + c, 0) for c in CROPS)


def against_the_tape(mid_from, seed, days=30):
    """Play the library agent through Kawashigi's own recorded season. Returns the daily grid."""
    BD.schedule_agent = BD.load_agent_module("schedule_agent")
    replay, _schedule, team = BD.TAPES[TAPE]
    economy = BD.env_config(replay)
    shops = BD.recorded_shops(replay)
    opp = lambda: BD.tape_policy(replay, team, 1)                           # noqa: E731

    def mine():
        a = kawa_library_agent.make_agent(None, 0, router=True, mid_from=mid_from)
        return lambda o, t: a(o)

    ours, our_ops, _cash, _dawn = BD.run(mine, opp, seed, WEEDS, stop_day=days + 1,
                                         economy=economy, shops=shops)
    his, his_ops, _c2, _d2 = BD.run(lambda: BD.tape_policy(replay, team, 0), opp, seed, WEEDS,
                                    stop_day=days + 1, economy=economy, shops=shops)
    return ours, our_ops, his, his_ops


def head_to_head(seed, days=30):
    """The library agent against the shipped greedy planner, both seatings, weeds off."""
    from kaggle_environments import make

    import kagg.plan as PLAN
    from kagg.search import schedule_agent as SA

    thin = PLAN.load()
    out = []
    for swapped in (False, True):
        env = make("kaggriculture",
                   configuration={"seed": seed, "weedSpawnChance": WEEDS}, debug=False)
        env.reset(2)
        mine_seat = 1 if swapped else 0
        lib = kawa_library_agent.make_agent(None, mine_seat, router=True)
        greedy = SA.make_agent(thin, 1 - mine_seat, router=True)
        seats = [greedy, lib] if swapped else [lib, greedy]
        env.run([lambda o, _c=None, a=seats[0]: a(o), lambda o, _c=None, a=seats[1]: a(o)])
        final = env.steps[-1]
        ours = final[mine_seat]["reward"]
        theirs = final[1 - mine_seat]["reward"]
        out.append((("seat 1" if swapped else "seat 0"), ours, theirs))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=11,
                    help="fixed, and quoted in every result. env.reset() draws a fresh one "
                         "otherwise and the same tape has banked $48k-$59k across runs.")
    ap.add_argument("--days", type=int, default=30)
    a = ap.parse_args()

    print("seed %d   weeds %.3f (CLEAN ROOM -- the ladder runs 0.005)   tape %s"
          % (a.seed, WEEDS, TAPE))
    print("MID_SEASON_FROM ships at %d\n" % kawa_rows.MID_SEASON_FROM)

    grids = {}
    for mid_from in (13, 14):
        ours, our_ops, his, his_ops = against_the_tape(mid_from, a.seed, a.days)
        grids[mid_from] = (ours, our_ops, his, his_ops)

    # ---- Q1 --------------------------------------------------------------------------------
    print("Q1  WHERE THE MIDDLE STARTS -- final bank against Kawashigi's own season")
    print("%-34s %12s %12s" % ("boundary", "ours", "tape"))
    for mid_from in (13, 14):
        ours, _oo, his, _ho = grids[mid_from]
        print("%-34s %12d %12d"
              % ("library d0-d%d, greedy d%d-d27" % (mid_from - 1, mid_from),
                 ours[a.days - 1]["money"], his[a.days - 1]["money"]))
    d13, d14 = grids[13][0][a.days - 1]["money"], grids[14][0][a.days - 1]["money"]
    print("  delta (d13 in the middle) - (d13 in the library) = %+d" % (d13 - d14))
    if d13 == d14:
        print("  THEY TIE. The boundary does not move the result on this seed.")

    # ---- the two quantities that pay ----------------------------------------------------------
    for mid_from in (13, 14):
        ours, our_ops, his, his_ops = grids[mid_from]
        print("\nlibrary d0-d%d, greedy d%d-d27   -- ours/tape, weeds 0.0"
              % (mid_from - 1, mid_from))
        print("  %-16s %s" % ("day", " ".join("%7d" % d for d in range(a.days))))
        for lab, fn in (("live crop tiles", lambda s, o: live_crops(s)),
                        ("plant ops", lambda s, o: o["PLANT"]),
                        ("harvest ops", lambda s, o: o["HARVEST"]),
                        ("water ops", lambda s, o: o["WATER"]),
                        ("money", lambda s, o: s["money"])):
            cells = []
            for d in range(a.days):
                cells.append("%7s" % ("%d/%d" % (fn(ours[d], our_ops[d]), fn(his[d], his_ops[d]))))
            print("  %-16s %s" % (lab, " ".join(cells)))

    # ---- Q2 --------------------------------------------------------------------------------
    print("\nQ2  LIBRARY AGENT vs THE SHIPPED GREEDY PLANNER, seed %d, both seatings" % a.seed)
    print("%-10s %12s %12s   %s" % ("seating", "library", "greedy", "result"))
    wins = losses = draws = 0
    for seating, ours, theirs in head_to_head(a.seed, a.days):
        verdict = "WIN" if ours > theirs else ("LOSS" if ours < theirs else "DRAW")
        wins += verdict == "WIN"
        losses += verdict == "LOSS"
        draws += verdict == "DRAW"
        print("%-10s %12d %12d   %s" % (seating, ours, theirs, verdict))
    print("  W/D/L  %d/%d/%d  on seed %d" % (wins, draws, losses, a.seed))


if __name__ == "__main__":
    main()
