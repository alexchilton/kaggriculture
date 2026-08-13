"""Do we harvest the day-10 melon late because we PLAN it late, or because we cannot get to it?

`scripts/how_seb_lands_the_melons.py` established the symptom: Seb's first melon HARVEST lands at
hour 6 and ours at hour 17, on the same eighteen melons. Framed as a delivery problem it has been
attacked seven times. This asks the upstream question instead -- at the moment `plan_routes`
returns, WHERE in each unit's tour does the melon HARVEST stop sit, and what hour does the tour
reach it?

It wraps `router.plan_routes`, so it reports the committed tour, not a reconstruction: for every
replan on the day, each unit's ordered stops with their ops, the cumulative walking ETA to each
stop, and a marker on every stop that harvests MELON.
"""
import json, pathlib, sys, collections
sys.path.insert(0, ".")
from kagg.search import schedule_agent as SA
from kagg.search import router as RT
from scripts.breakdown import DEFAULT_TAPE, TAPES, TAPE_ONLY, tape_policy
from kaggle_environments import make

DAY = int(sys.argv[1]) if len(sys.argv) > 1 else 10
PROD = "MELON"
replay, schedule, team = TAPES[DEFAULT_TAPE]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

HOUR = {"h": -1}
_real_plan = RT.plan_routes
LOG = []


def spy(units, nodes, budget, depots=RT.SHED, carry=None, supply=None):
    out = _real_plan(units, nodes, budget, depots, carry, supply)
    if HOUR["h"] >= 0:
        LOG.append((HOUR["h"], list(units), {u: list(st["route"]) for u, st in out.items()},
                    {u: st["depot"] for u, st in out.items()},
                    {u: dict(st["draw"]) for u, st in out.items()}, list(budget)))
    return out


def describe():
    for hour, units, routes, depot, draw, budget in LOG:
        print(f"\n--- replan at h{hour}  ({len(routes)} units planned) ---")
        for k in sorted(routes):
            start = units[k]
            eta = 0
            cur = start
            bits = []
            if depot.get(k) is not None:
                eta += RT.dist(cur, depot[k])
                cur = depot[k]
                bits.append(f"[depot{depot[k]}@h{hour + eta} draw={dict(draw[k])}]")
                eta += len(draw[k] or {})
            for n in routes[k]:
                eta += RT.dist(cur, n.tile)
                cur = n.tile
                ops = ",".join(o for o, _i in n.ops)
                mark = " <<< MELON" if any(o == "HARVEST" for o, _i in n.ops) else ""
                bits.append(f"{n.tile}{ops}@h{hour + eta}${n.prize:.0f}{mark}")
                eta += n.service
            if bits:
                print(f"  u{k} at {start} budget={budget[k]}: " + "  ".join(bits))


def main():
    RT.plan_routes = spy
    SA.RT.plan_routes = spy
    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    p0 = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)
    melon_tiles = set()
    for t in range(24 * (DAY + 1)):
        o0, o1 = env.state[0].observation, env.state[1].observation
        HOUR["h"] = (t % 24) if t // 24 == DAY else -1
        if t // 24 == DAY and t % 24 == 0:
            tiles = o0["farms"][0]["tiles"]
            for y, row in enumerate(tiles):
                for x, c in enumerate(row):
                    if isinstance(c, dict) and c.get("crop") == PROD:
                        melon_tiles.add((x, y))
                        print(f"  {PROD} tile ({x},{y}) planted_day={c.get('planted_day')} "
                              f"held={c.get('held')} age={DAY - int(c.get('planted_day', 0))}")
        a0 = p0(o0)
        a1 = opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    print(f"\n{PROD} tiles at day {DAY} dawn: {sorted(melon_tiles)}")
    describe()


main()
