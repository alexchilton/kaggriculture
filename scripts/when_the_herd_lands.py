"""When each animal actually starts producing -- ours against the tape.

`breakdown.py`'s `PLACE 4/4` says the counts match and hides the only thing that pays: an animal
produces from the turn it is placed, so two farms holding the same six animals are not in the same
position if one put them down eight hours earlier.

Measured seed 11, d0:

    ours   h07 SHEEP  h12 SHEEP  h17 COW  h20 COW      placement hours sum 56
    tape   h04 SHEEP  h04 COW    h05 SHEEP  h12 COW    placement hours sum 25

Thirty-one animal-hours on day 0, invisible in every row of the grid. It repeats on d3 (h09 vs h08)
and d5 (h13 vs h08). The tape also places two animals on the SAME turn at h04, with two different
units, which we never do.

This is NOT the COW-vs-SHEEP ranking recorded as reverted at `router.py:1170` -- both sides place
sheep first. It is purely how early the placements happen.

    python -u scripts/when_the_herd_lands.py --days 7
"""
import argparse
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

MELON_SEASON = "data/seed_scripts/kawashigi/92498144.json"
STRAWBERRY_SEASON = "data/seed_scripts/kawashigi/92466371.json"
TEAM = "カワシギ"
TPD = 24


def trace(use_tape, seed, weeds, days, sched, replay, SA, B):
    from kaggle_environments import make
    env = make("kaggriculture", configuration=dict(B.env_config(replay), seed=seed,
                                                   weedSpawnChance=weeds), debug=True)
    env.reset(2)
    agent = SA.make_agent(sched, 0)
    tape0 = B.tape_policy(replay, TEAM, 0)
    p1 = B.tape_policy(replay, TEAM, 1)
    placed, seen = [], set()
    for t in range(days * TPD):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0 = tape0(o0, t) if use_tape else agent(o0)
        env.step([a0, p1(o1, t)])
        d, h = divmod(t, TPD)
        for y, row in enumerate(env.state[0].observation["farms"][0]["tiles"]):
            for x, c in enumerate(row):
                if isinstance(c, dict) and c.get("animal") and (x, y) not in seen:
                    seen.add((x, y))
                    placed.append((d, h, c["animal"], (x, y)))
    return placed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=("straw", "melon"), default="melon")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.005)
    ap.add_argument("--days", type=int, default=7)
    a = ap.parse_args()

    import breakdown as B
    from kagg.search import melon_branch as _MB
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    _MB.OPPONENT_MELON = 0 if a.arm == "straw" else 99

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    replay = str(REPO / (STRAWBERRY_SEASON if a.arm == "straw" else MELON_SEASON))

    for use_tape, tag in ((False, "OURS"), (True, "TAPE")):
        placed = trace(use_tape, a.seed, a.weeds, a.days, sched, replay, SA, B)
        print(f"\n=== {tag}")
        for d, h, an, tile in placed:
            print(f"   d{d} h{h:02d}  {an:<6} at {tile}")
        by_day = collections.defaultdict(list)
        for d, h, _a, _t in placed:
            by_day[d].append(h)
        print("   herd:", dict(collections.Counter(an for _d, _h, an, _t in placed)))
        print("   placement hours per day:",
              {d: sorted(v) for d, v in sorted(by_day.items())},
              " sum:", sum(h for _d, h, _a, _t in placed))


if __name__ == "__main__":
    main()
