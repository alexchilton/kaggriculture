"""Per-day herd census: animals STANDING IN PENS, animals stranded in the shed, empty pens.

The correctness floor for any change to how animals are bought or placed, and the thing
`scripts/breakdown.py` cannot answer on its own -- it prints ours-minus-tape, and a delta of zero
says nothing about whether both sides had two cows or twenty.

It exists because this project has twice nearly shipped an animal change on the strength of cells
and money alone. `FEED_ORDER_CAP = 4` collapsed animals-in-pens from 17 to 8. The PLACE gate below
places every animal it is given and still finishes the season one animal short, because the two it
places starve at d16. Both are invisible in a total.

Three arms, so a gate can be measured against the thing it replaced rather than only against off:

    python -u scripts/pen_census.py --seed 11 --gate off      # no mandatory PLACE at all
    python -u scripts/pen_census.py --seed 11 --gate day14    # the retired `FROM_DAY = 14` constant
    python -u scripts/pen_census.py --seed 11 --gate stale    # today's held-since-dawn rule

`--gate current` reads whatever `router.py` ships with and changes nothing.

"STRANDED OVERNIGHT" is the headline: an animal held in the shed at dusk on two CONSECUTIVE days
with a pen standing empty on the second. One dusk alone is just an animal bought late today; two is
one that has had a whole day and an open pen and still is not in it.
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent
from kagg.search import router as RT
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy


def census(seat_obs):
    farm = seat_obs["farms"][0]
    penned = collections.Counter()
    empty = 0
    for r in farm["tiles"]:
        for t in r:
            if not isinstance(t, dict):
                continue
            if t.get("kind") in ("PASTURE", "COOP"):
                if t.get("animal"):
                    penned[t["animal"]] += 1
                else:
                    empty += 1
    shed = (seat_obs.get("private") or {}).get("shed") or {}
    held = {k: int(v) for k, v in shed.items() if k in RT.R.ANIMAL_NAMES and int(v or 0) > 0}
    return penned, empty, held, int(farm["money"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--tape", default="seb")
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--gate", default="current",
                    choices=("current", "off", "day14", "stale"))
    args = ap.parse_args()

    if args.gate == "off":
        RT.PLACE_IS_MANDATORY_WHEN_HELD_OVERNIGHT = False
    elif args.gate == "stale":
        RT.PLACE_IS_MANDATORY_WHEN_HELD_OVERNIGHT = True
    elif args.gate == "day14":
        # Reconstruct the OLD constant exactly, without putting a day number back in product code:
        # the old gate was "mandatory iff day >= 14 and the animal is in the shed", which is the new
        # gate with `held_since_dawn` forced to the live shed on and after day 14, and to empty
        # before it. Same predicate, same branch, so the arms differ only in the gate.
        RT.PLACE_IS_MANDATORY_WHEN_HELD_OVERNIGHT = True
        real = RT.build_nodes

        def as_of_day_14(tiles, day, shed, carried, unlocked, pinned, hour=0, held_since_dawn=None):
            return real(tiles, day, shed, carried, unlocked, pinned, hour,
                        dict(shed) if day >= 14 else {})

        RT.build_nodes = as_of_day_14

    replay, schedule, team = TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": args.seed, "weedSpawnChance": args.weeds},
               debug=True)
    env.reset(2)
    agent = schedule_agent.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)

    rows = []
    stranded_overnight = []
    prev_dusk_held = {}
    for t in range(719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        day, hour = t // 24, t % 24
        if day >= args.days:
            break
        a0 = agent(o0)
        a1 = opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if hour == 23:
            penned, empty, held, money = census(env.state[0].observation)
            rows.append((day, sum(penned.values()), empty, dict(held), money, dict(penned)))
            # "stranded overnight" = an animal held in the shed at dusk on two CONSECUTIVE days
            # while a pen stood empty on the second of them. One dusk alone is an animal bought
            # late today; two is one that has had a whole day and a pen and still is not placed.
            for a, n in held.items():
                if empty and prev_dusk_held.get(a, 0) > 0:
                    stranded_overnight.append((day, a, n, empty))
            prev_dusk_held = held
        if env.state[0].status == "DONE":
            break

    print(f"seed {args.seed}  tape {args.tape}  weeds {args.weeds}  gate={args.gate}  "
          f"HELD_OVERNIGHT={RT.PLACE_IS_MANDATORY_WHEN_HELD_OVERNIGHT}")
    print(f"{'day':>4} {'penned':>7} {'empty':>6} {'shed':>22} {'money':>9}")
    for day, penned, empty, held, money, by in rows:
        print(f"{day:>4} {penned:>7} {empty:>6} {str(held or '-'):>22} {money:>9}")
    print(f"  penned mean {sum(r[1] for r in rows) / max(1, len(rows)):.2f}  "
          f"min {min((r[1] for r in rows), default=0)}  max {max((r[1] for r in rows), default=0)}  "
          f"final money {rows[-1][4] if rows else 0}")
    if stranded_overnight:
        print("  STRANDED OVERNIGHT (animal held at dusk two days running with a pen empty):")
        for d, a, n, e in stranded_overnight:
            print(f"    day {d}  {a} x{n}  {e} empty pens")
    else:
        print("  STRANDED OVERNIGHT: none")


if __name__ == "__main__":
    main()
