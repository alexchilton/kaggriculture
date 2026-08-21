"""Where does the block agent rupture, and why? A per-day grid against the planner on ONE seed.

Alex, 2026-08-21: "where and why does it go wrong? ... use the grid to see where the ruptures happen
and then try and see why".

The block agent banked $29,010 where the planner alone banked $78,250 on the same seed. A season
total cannot say which day broke it, and the days compound -- an earlier day's failure is inherited
by every later one, so the FIRST rupture is the only one worth diagnosing.

Both columns are seat 0 on the same seed against the same opponent, so every row is comparable:

    BLOCK   the day-block agent  (blocks d0-d16, planner d17+)
    PLAN    the planner alone

For the block agent it also counts what the block ASKED for against what the board DID. That is the
"why": the reference silently ignores an op it cannot perform -- a PLANT with no seed in hand, a
HARVEST on bare soil, a move into a locked quadrant -- so a block can be executed faithfully and
still do nothing at all. `_live_ops` in the planner exists precisely to re-derive work from the live
board; a stored block has no such step.

    python -u scripts/block_grid.py --artifact data/block_agent_kawa.pkl --seed 7000000
"""

import argparse
import collections
import importlib.util
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")


def load_planner():
    spec = importlib.util.spec_from_file_location("grid_planner", REPO / "submission/main.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.agent


def snapshot(obs, seat):
    farms = obs.get("farms") or []
    me = farms[seat] if seat < len(farms) else {}
    private = obs.get("private") or {}
    crops = weeds = thirsty = 0
    for row in (me.get("tiles") or []):
        for t in row:
            if not isinstance(t, dict):
                continue
            if t.get("crop"):
                crops += 1
            if str(t.get("kind")) == "WEED":
                weeds += 1
            if (t.get("consecutive_unwatered") or 0) >= 1:
                thirsty += 1
    shed = private.get("shed") or {}
    seeds = private.get("seeds") or {}
    return {"money": float(me.get("money", 0) or 0),
            "hands": len(me.get("hands") or []),
            "quads": len(me.get("unlocked_quadrants") or []),
            "crops": crops, "weeds": weeds, "thirsty": thirsty,
            "shed": sum(int(v or 0) for v in shed.values()),
            "seeds": sum(int(v or 0) for v in seeds.values())}


def run(seed, seat0_factory, count_ops):
    from kaggle_environments import make
    ours = seat0_factory()
    opp = load_planner()
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)

    per_day, asked = {}, collections.defaultdict(collections.Counter)
    while not env.done:
        ob0 = env.state[0].observation
        day, hour = int(ob0.get("day", 0) or 0), int(ob0.get("hour", 0) or 0)
        if hour == 0:
            per_day[day] = snapshot(ob0, 0)
        act = ours(ob0, env.configuration)
        if count_ops:
            for u in [act.get("farmer")] + list(act.get("hands") or []):
                if u:
                    asked[day][str(u[0])] += 1
            for o in (act.get("market") or []):
                if o:
                    asked[day]["MKT_" + str(o[0])] += 1
        env.step([act, opp(env.state[1].observation, env.configuration)])

    final = env.state[0].observation.farms
    return per_day, asked, float(final[0]["money"]), float(final[1]["money"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact", default="data/block_agent_kawa.pkl")
    ap.add_argument("--seed", type=int, default=7000000)
    ap.add_argument("--days", type=int, default=20)
    args = ap.parse_args()

    from kagg.agents import block_agent

    print("seed %d, seat 0, same planner opponent in both runs\n" % args.seed)
    b_days, b_ops, b_end, b_opp = run(
        args.seed, lambda: block_agent.make_agent(args.artifact), True)
    p_days, _p_ops, p_end, p_opp = run(args.seed, load_planner, False)

    print("FINAL   block $%.0f (opp $%.0f)   planner $%.0f (opp $%.0f)"
          % (b_end, b_opp, p_end, p_opp))

    print("\n%4s %19s %11s %11s %9s %9s %9s"
          % ("day", "money  block/plan", "crops", "shed", "seeds", "weeds", "crew"))
    first_rupture = None
    for day in range(args.days):
        b, p = b_days.get(day), p_days.get(day)
        if not b or not p:
            continue
        gap = b["money"] - p["money"]
        if first_rupture is None and day > 0 and gap < -1000:
            first_rupture = day
        print("%4d %9.0f/%-9.0f %5d/%-5d %5d/%-5d %4d/%-4d %4d/%-4d %4d/%-4d%s"
              % (day, b["money"], p["money"], b["crops"], p["crops"],
                 b["shed"], p["shed"], b["seeds"], p["seeds"],
                 b["weeds"], p["weeds"], b["hands"], p["hands"],
                 "   <-- first rupture" if day == first_rupture else ""))

    print("\nWHAT THE BLOCK ASKED FOR, per day (block agent only)")
    print("%4s %s" % ("day", "ops emitted"))
    for day in range(min(args.days, 17)):
        c = b_ops.get(day)
        if not c:
            continue
        unit = {k: v for k, v in c.items() if not k.startswith("MKT_")}
        mkt = {k[4:]: v for k, v in c.items() if k.startswith("MKT_")}
        top = ", ".join("%s %d" % (k, v) for k, v in
                        sorted(unit.items(), key=lambda kv: -kv[1])[:6])
        mk = ", ".join("%s %d" % (k, v) for k, v in
                       sorted(mkt.items(), key=lambda kv: -kv[1])[:4])
        print("%4d %s   | market: %s" % (day, top, mk or "none"))


if __name__ == "__main__":
    main()
