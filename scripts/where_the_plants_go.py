"""The schedule asks for 86 plants. Where do they die between the row and the ground?

`scripts/why_the_land_is_bare.py` cleared the extractor: the `plants` rows match the tape day for
day and crop for crop on both tapes. So the deficit is in the executor, and there are exactly four
places a wanted planting can be lost:

    no ground     `_next_ground` returns None -- every owned tile is occupied, weeded or pinned
    no seed       `_live_ops` refuses PLANT at `seeds[item] <= 0`; the BUY_SEED never landed, or
                  landed short because the bank or the 9-order cap ate it
    expired       `plant_prize(crop, day) <= 0` un-pins it -- the season can no longer finish it
    no turns      the pin is alive and seeded and simply never reached: the tour ran out of crew

Each needs a different fix, so the per-day counters below separate them. `idle` is the discriminator
for the last one -- crew-turns that ended in PASS while a PLANT pin was standing is the "hired hands
are not busy" case, and it means routing, not supply.

    python -u scripts/where_the_plants_go.py
"""

import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent, router as RT


TAPE = "data/seed_scripts/top_guys/90494364.json"
SCHEDULE = "data/seed_scripts/top_guys/90494364/schedule.json"
TEAM = "Seb (allegedly)"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


def tape_policy(replay, team, seat_wanted):
    d = json.loads(pathlib.Path(replay).read_text())
    seat = d["info"]["TeamNames"].index(team)
    src = seat if seat_wanted == 0 else 1 - seat
    acts = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[src] or {} for step in d["steps"][1:])]
    idle = {"farmer": ["PASS"], "hands": [], "market": []}
    return lambda obs, t: acts[t] if t < len(acts) else idle


def main(seed=11, weeds=0.0):
    from kaggle_environments import make

    sched = {int(k): v for k, v in json.loads(pathlib.Path(SCHEDULE).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=True)
    env.reset(2)
    agent = schedule_agent.make_agent(thin, 0, router=True)
    opp = tape_policy(TAPE, TEAM, 1)

    rows = []
    per_day = collections.defaultdict(lambda: collections.Counter())
    for t in range(719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        day, hour = t // 24, t % 24
        a0 = agent(o0)
        a1 = opp(o1, t)
        acts = [a0["farmer"]] + list(a0["hands"] or [])
        c = per_day[day]
        for a in acts:
            if a and a[0] == "PLANT":
                c["PLANT"] += 1
            elif not a or a[0] == "PASS":
                c["idle"] += 1
            c["turns"] += 1
        for o in (a0["market"] or []):
            if o and o[0] == "BUY_SEED":
                c["seeds_ordered"] += int(o[2])

        if hour == 0:
            farm = o0["farms"][0]
            priv = o0.get("private") or {}
            tiles = farm["tiles"]
            unlocked = farm.get("unlocked_tiles") or farm.get("tiles_owned")
            empty = sum(1 for y, row in enumerate(tiles) for x, cell in enumerate(row)
                        if cell is None)
            weedy = sum(1 for row in tiles for cell in row
                        if isinstance(cell, dict) and cell.get("kind") == "WEED")
            seeds = collections.Counter(priv.get("seeds") or {})
            # What the CUMULATIVE schedule still owes, exactly as `_refresh_pins` computes it.
            want = collections.Counter()
            for d in sorted(sched):
                if d <= day:
                    want.update(sched[d].get("plants") or [])
            rows.append(dict(day=day, empty=empty, weed=weedy, seeds=sum(seeds.values()),
                             want=sum(want.values()),
                             expired=sum(q for cr, q in want.items()
                                         if cr in RT.CROP and RT.plant_prize(cr, day) <= 0),
                             money=int(farm["money"]),
                             hands=len(farm.get("hands") or [])))

        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break

    tape_per_day = collections.Counter()
    d = json.loads(pathlib.Path(TAPE).read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    for t, step in enumerate(d["steps"][1:]):
        act = (step[seat] or {}).get("action") or {}
        for a in [act.get("farmer") or ["PASS"]] + list(act.get("hands") or []):
            if a and a[0] == "PLANT":
                tape_per_day[t // 24] += 1

    print(f"seed {seed}  weeds {weeds}   Seb's schedule, our executor\n")
    print(f"  {'day':>4}{'want cum':>10}{'planted':>9}{'tape':>6}{'shortfall':>11}"
          f"{'seeds':>7}{'empty':>7}{'weed':>6}{'expired':>9}{'idle':>7}{'turns':>7}"
          f"{'hands':>7}{'money':>9}")
    cum_planted = cum_tape = 0
    for r in rows:
        c = per_day[r["day"]]
        cum_planted += c["PLANT"]
        cum_tape += tape_per_day[r["day"]]
        print(f"  {r['day']:>4}{r['want']:>10}{cum_planted:>9}{cum_tape:>6}"
              f"{r['want'] - cum_planted:>11}{r['seeds']:>7}{r['empty']:>7}{r['weed']:>6}"
              f"{r['expired']:>9}{c['idle']:>7}{c['turns']:>7}{r['hands']:>7}{r['money']:>9,}")
    print(f"\n  season PLANT ours {cum_planted}  tape {cum_tape}   "
          f"seeds ordered {sum(per_day[d]['seeds_ordered'] for d in per_day)}")
    print(f"  season idle crew-turns {sum(per_day[d]['idle'] for d in per_day)} "
          f"of {sum(per_day[d]['turns'] for d in per_day)}")


if __name__ == "__main__":
    main()