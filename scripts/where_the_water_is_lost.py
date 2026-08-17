"""The plan offers 19 waters at d6 and the day performs 17. This says which two, and why.

`cover` seats a job; `_live_ops` re-derives the work when the unit ARRIVES
(`schedule_agent.py:1255`). A stop whose work is no longer there returns `[]` and is dropped with no
trace. So a water can be lost in two different places and they need telling apart:

    never offered      `crop_ops` did not emit it at dawn      -- fixed by the parity clause
    offered, seated,   `crop_ops` DID emit it at dawn and did  -- what this script finds
    then evaporated     not emit it on arrival

Every `_live_ops` call on a crop tile is logged with the cell state that decided it, so the two
tiles that lose their water are named along with the field that turned it off.

    python -u scripts/where_the_water_is_lost.py --arm melon --day 6
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

from kagg.search import melon_branch as _MB          # noqa: E402

MELON_SEASON = "data/seed_scripts/kawashigi/92498144.json"
STRAWBERRY_SEASON = "data/seed_scripts/kawashigi/92466371.json"
TEAM = "カワシギ"

CALLS = []          # (hour, tile, crop, watered_today, unwatered, age, gave_water)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=("straw", "melon"), default="melon")
    ap.add_argument("--day", type=int, default=6)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.005)
    a = ap.parse_args()

    import breakdown as B
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    _MB.OPPONENT_MELON = 0 if a.arm == "straw" else 99

    turn = {"t": 0}
    real = SA._live_ops

    def wrapped(tile, cell, day, inv, pins, seeds, fertilizer_price=None):
        out = real(tile, cell, day, inv, pins, seeds, fertilizer_price)
        if day == a.day and isinstance(cell, dict) and cell.get("kind") == "PLANT":
            CALLS.append((turn["t"] % 24, tuple(tile), cell.get("crop"),
                          bool(cell.get("watered_today")),
                          int(cell.get("consecutive_unwatered", 0)),
                          day - int(cell.get("planted_day", day)),
                          any(o[0] == "WATER" for o in out)))
        return out

    SA._live_ops = wrapped

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    replay = str(REPO / (STRAWBERRY_SEASON if a.arm == "straw" else MELON_SEASON))
    opp = lambda: B.tape_policy(replay, TEAM, 1)                      # noqa: E731

    def ours():
        agent = SA.make_agent(sched, 0)
        inner = [0]

        def step(o, t):
            turn["t"] = t
            inner[0] = t
            return agent(o)
        return step

    B.run(ours, opp, a.seed, a.weeds, stop_day=a.day + 1,
          economy=B.env_config(replay), shops=B.recorded_shops(replay))

    print(f"arm {a.arm!r}, day {a.day}, seed {a.seed}, weeds {a.weeds}")
    print(f"_live_ops calls on crop tiles: {len(CALLS)}\n")

    # A tile is "lost" when at least one visit asked about it and no visit gave a water.
    per_tile = collections.defaultdict(list)
    for h, tile, crop, wet, unw, age, gave in CALLS:
        per_tile[tile].append((h, crop, wet, unw, age, gave))

    gave_water = {t for t, rows in per_tile.items() if any(r[5] for r in rows)}
    no_water = {t for t in per_tile if t not in gave_water}

    print(f"crop tiles visited: {len(per_tile)}   gave a water: {len(gave_water)}   "
          f"gave none: {len(no_water)}\n")
    print(f"{'tile':>9}{'crop':>12}{'visits':>8}{'watered_today':>15}"
          f"{'unwatered':>11}{'age':>5}   hours")
    for tile in sorted(no_water):
        rows = per_tile[tile]
        h, crop, wet, unw, age, _g = rows[0]
        print(f"{str(tile):>9}{crop:>12}{len(rows):>8}{str(wet):>15}{unw:>11}{age:>5}   "
              + " ".join(f"h{r[0]:02d}" for r in rows))


if __name__ == "__main__":
    main()
