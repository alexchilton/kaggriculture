"""Crop production and crop DEATH, per day, per crop, both sides.

`_daily_refresh_plants` (`reference/kaggriculture.py:738`) is the only place a crop tile grows
`yield_units`, and it is also the only place a crop tile DIES: two consecutive unwatered days turn
the plant into a WEED, in one line, with no signal anywhere in the observation. So a `strawb` row
that shows fewer tiles standing cannot be read as "we planted fewer" -- it is equally consistent
with "we planted the same and drowned none of them in water".

Per day and per crop this records, for each seat:

    made      yield_units added at the dusk refresh
    died      crop tiles replaced by a WEED for two consecutive unwatered days
    unwat     standing crop tiles that went unwatered that day (one strike)
    tiles     crop tiles standing at the refresh

    python -u scripts/probe_plant_yield.py --crop STRAWBERRY
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

REC = collections.defaultdict(collections.Counter)
DEATHS = []          # (seat, day, crop, age, yield_units, prize the router put on the rescue water)
CALLS = [0]
DAY = [0]


def install():
    from kaggle_environments.envs.kaggriculture import kaggriculture as kg
    if getattr(kg, "_plant_probe", False):
        return
    orig = kg._daily_refresh_plants

    def wrapped(farm, current_day, turns_per_day):
        # `_end_of_day` calls plants then animals per farm in seat order; this wrapper only counts
        # the plant call, so its own call parity is the seat.
        seat = CALLS[0] % 2
        CALLS[0] += 1
        before = {}
        for y, row in enumerate(farm["tiles"]):
            for x, t in enumerate(row):
                if isinstance(t, dict) and t.get("kind") == "PLANT":
                    before[(x, y)] = (t["crop"], int(t["yield_units"]),
                                      bool(t["watered_today"]),
                                      int(t.get("consecutive_unwatered", 0) or 0), dict(t))
        orig(farm, current_day, turns_per_day)
        for (x, y), (crop, yu, watered, unwat, raw) in before.items():
            t = farm["tiles"][y][x]
            k = (seat, DAY[0], crop)
            REC[k]["tiles"] += 1
            if not watered:
                REC[k]["unwat"] += 1
            if not (isinstance(t, dict) and t.get("kind") == "PLANT"):
                REC[k]["died"] += 1
                # What the router thought the rescue water was worth, evaluated on the tile as it
                # stood at dawn on the day it died -- `consecutive_unwatered` was already 1 then.
                from kagg.search import router as R
                probe = dict(raw)
                probe["consecutive_unwatered"] = 1
                probe["watered_today"] = False
                prize = [o for o in R.crop_ops(probe, DAY[0], True) if o[0] == "WATER"]
                DEATHS.append((seat, DAY[0], crop, DAY[0] - raw["planted_day"], yu,
                               prize[0][2] if prize else None))
                continue
            REC[k]["made"] += int(t["yield_units"]) - yu
    kg._daily_refresh_plants, kg._plant_probe = wrapped, True


def run(make0, opp, seed, weeds):
    from kaggle_environments import make
    install()
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=True)
    env.reset(2)
    CALLS[0] = 0
    REC.clear()
    p0, p1 = make0(), opp()
    for t in range(719):
        DAY[0] = t // 24
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="seb", choices=sorted(TAPES))
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--crop", default="STRAWBERRY")
    args = ap.parse_args()

    replay, schedule, team = TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    opp = lambda: tape_policy(replay, team, 1)

    run(lambda: tape_policy(replay, team, 0), opp, args.seed, args.weeds)
    HIS = {k: collections.Counter(v) for k, v in REC.items()}
    DEATHS.clear()
    a = schedule_agent.make_agent(thin, 0, router=True)
    run(lambda: (lambda o, t: a(o)), opp, args.seed, args.weeds)
    OUR = {k: collections.Counter(v) for k, v in REC.items()}

    print("  tiles that DIED of thirst, ours, seat 0 -- "
          "(day, crop, age, yield_units held and lost, prize `router.crop_ops` put on the "
          "rescue water at dawn that day)")
    for seat, d, crop, age, yu, prize in DEATHS:
        if seat == 0:
            print(f"    d{d:<3} {crop:<11} age {age:>2}  held {yu}  rescue-water prize "
                  f"{'(no WATER offered)' if prize is None else '$%d' % prize}")
    print()
    crops = [args.crop] if args.crop != "ALL" else sorted(
        {c for (_s, _d, c) in list(OUR) + list(HIS)})
    for crop in crops:
        print(f"\n{crop}   tape {args.tape} seed {args.seed} weeds {args.weeds}   ours | tape, "
              f"seat 0.  dusk refresh, from `_daily_refresh_plants`.")
        print(f"{'day':>4} | {'tiles':>6}{'made':>5}{'unwat':>6}{'died':>5} | "
              f"{'tiles':>6}{'made':>5}{'unwat':>6}{'died':>5}")
        tot = collections.Counter()
        for d in range(args.days):
            o = OUR.get((0, d, crop), collections.Counter())
            h = HIS.get((0, d, crop), collections.Counter())
            for k in ("tiles", "made", "unwat", "died"):
                tot["o" + k] += o[k]
                tot["h" + k] += h[k]
            if not (o or h):
                continue
            print(f"{d:>4} | {o['tiles']:>6}{o['made']:>5}{o['unwat']:>6}{o['died']:>5} | "
                  f"{h['tiles']:>6}{h['made']:>5}{h['unwat']:>6}{h['died']:>5}")
        print(f"  season  made {tot['omade']}/{tot['hmade']}   died {tot['odied']}/{tot['hdied']}"
              f"   unwatered-tile-days {tot['ounwat']}/{tot['hunwat']}"
              f"   tile-days {tot['otiles']}/{tot['htiles']}")


if __name__ == "__main__":
    main()
