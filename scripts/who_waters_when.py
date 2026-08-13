"""Waters, plant tiles and weeds per day, ours against the tape.

`router.py:243` carries a table claiming the tape waters 18 times on day 1 to our 1, and uses it to
justify offering WATER every day rather than on the brink. `breakdown.py --diff` now reports the
reverse for Seb: water d1 = +17, i.e. the tape waters NOTHING on day 1. One of the two is measuring
a different tape. This settles it, and also counts the weeds each policy leaves behind, since the
whole argument for daily watering was that alternate-day watering self-inflicts weeds.
"""

import argparse, collections, json, pathlib, sys
sys.path.insert(0, ".")
from kagg.search import schedule_agent
from scripts.breakdown import DEFAULT_TAPE, TAPES, TAPE_ONLY, tape_policy


def run(make0, opp, seed, weeds, days):
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=True)
    env.reset(2)
    p0, p1 = make0(), opp()
    water = collections.Counter()
    board = {}
    for t in range(24 * days):
        o0, o1 = env.state[0].observation, env.state[1].observation
        day, hour = t // 24, t % 24
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        if hour == 0:
            tiles = o0["farms"][0]["tiles"]
            cnt = collections.Counter()
            dry = 0
            for row in tiles:
                for c in row:
                    k = c.get("kind") if isinstance(c, dict) else c
                    cnt[k] += 1
                    if isinstance(c, dict) and k == "PLANT":
                        dry += int(c.get("consecutive_unwatered", 0))
            board[day] = (cnt["PLANT"], cnt["WEED"], dry)
        for a in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
            if a and a[0] == "WATER":
                water[day] += 1
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
    return water, board


ap = argparse.ArgumentParser()
ap.add_argument("--tape", default=DEFAULT_TAPE, choices=sorted(TAPES))
ap.add_argument("--days", type=int, default=8)
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--weeds", type=float, default=0.0)
args = ap.parse_args()

replay, schedule, team = TAPES[args.tape]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
opp = lambda: tape_policy(replay, team, 1)

hw, hb = run(lambda: tape_policy(replay, team, 0), opp, args.seed, args.weeds, args.days)
a = schedule_agent.make_agent(thin, 0, router=True)
ow, ob = run(lambda: (lambda o, t: a(o)), opp, args.seed, args.weeds, args.days)

print(f"tape {args.tape}   seed {args.seed}   weeds {args.weeds}\n")
print(f"  {'day':>3}  {'waters o/t':>12}  {'plant tiles o/t':>16}  {'weeds o/t':>10}  {'dry-debt o/t':>13}")
for d in range(args.days):
    op, owd, odry = ob.get(d, (0, 0, 0))
    hp, hwd, hdry = hb.get(d, (0, 0, 0))
    print(f"  {d:>3}  {ow[d]:>5}/{hw[d]:<6}  {op:>7}/{hp:<8}  {owd:>4}/{hwd:<5}  {odry:>6}/{hdry:<6}")
