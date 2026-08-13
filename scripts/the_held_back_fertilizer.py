"""Day 3 sells 4 fertilizer where the row says 5, and the 5th is still in the shed at day-4 dawn.

That unit is worth ~$94 realised, which is exactly our day-4 dawn shortfall (388 against the tape's
482) -- and a COW costs 400. So one unsold fertilizer is why the day-4 cow is bought at hour 17
instead of hour 0, and therefore why it is never placed.

The suspect is the fertilizer reserve in `schedule_agent`: it withholds one unit per tile that
`crop_ops` would offer FERTILIZE on. This prints, per hour of day 3, the shed's fertilizer, how many
units the reserve is holding back, which tiles it is holding them for, and what we actually offered.
"""
import json, pathlib, sys
sys.path.insert(0, ".")
from kagg.search import schedule_agent, router as RT
from scripts.breakdown import DEFAULT_TAPE, TAPES, TAPE_ONLY, tape_policy
from kaggle_environments import make

replay, schedule, team = TAPES[DEFAULT_TAPE]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
env.reset(2)
agent = schedule_agent.make_agent(thin, 0, router=True)
opp = tape_policy(replay, team, 1)

for t in range(24 * 4):
    o0, o1 = env.state[0].observation, env.state[1].observation
    a0, a1 = agent(o0), opp(o1, t)
    n0 = len(o0["farms"][0].get("hands") or [])
    n1 = len(o0["farms"][1].get("hands") or [])
    if t // 24 == 3:
        shed = o0["private"]["shed"]
        tiles = o0["farms"][0]["tiles"]
        holders = [(x, y, c.get("crop"))
                   for y, r in enumerate(tiles) for x, c in enumerate(r)
                   if isinstance(c, dict) and c.get("kind") == "PLANT"
                   and any(o == "FERTILIZE" for o, _i, _p in RT.crop_ops(c, 3, True))]
        sells = [o for o in (a0["market"] or []) if o and o[0] == "SELL"]
        have = int(shed.get("FERTILIZER", 0))
        if have or sells or holders:
            print(f"  hr {t%24:>2}  shed_fert={have:<3} reserve={len(holders):<3} "
                  f"sellable={max(0, have - len(holders)):<3} money={int(o0['farms'][0]['money']):<6} "
                  f"offered={sells}")
            if holders and t % 24 in (0, 12, 23):
                print(f"          holding for: {holders}")
    env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
              {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
