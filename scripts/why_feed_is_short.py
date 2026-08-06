"""Per-day: is there wheat, is there a herd, and did FEED land? One row per day, one seed.

The season aggregate says FEED 29 against the tape's 319 with fourteen pens built and fourteen animals
placed, which is one feeding round and then a herd that starves. Three things could produce that and
they are distinguishable only per day: no wheat in the shed, wheat in the shed that no unit draws, or
wheat drawn and a FEED that never reaches the pen.
"""

import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import router as RT
from kagg.search import schedule_agent
import agent_ladder as L


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    _mine, theirs = L.tape_plans()
    sched = {int(k): v for k, v in json.loads(pathlib.Path(L.SCHEDULE).read_text()).items()}
    for r in sched.values():
        for k in L.TAPE_ONLY:
            r[k] = []

    env = L._env(seed, 0.0)
    us = schedule_agent.make_agent(sched, 0, router=True)
    day_ops = collections.Counter()
    rows = []
    seen = -1
    for t in range(719):
        obs = env.state[0].observation
        day = int(obs.get("day", 0))
        if day != seen:
            if seen >= 0:
                rows.append((seen, snap, dict(day_ops)))
            day_ops = collections.Counter()
            seen = day
            snap = {}
        # **Sample at MIDDAY, not dawn.** Hands are dismissed every night and re-hired through the
        # morning, so a dawn reading of the crew is always 1 and says nothing. The first version of
        # this script reported "units 1" for all thirty days purely from sampling the wrong instant.
        if int(obs.get("hour", 0)) == 12:
            farm, priv = obs["farms"][0], obs["private"]
            tiles = farm["tiles"]
            carried = collections.Counter()
            for iv in priv.get("inventories") or []:
                carried.update(iv)
            snap = dict(
                animals=sum(1 for r in tiles for c in r if isinstance(c, dict) and "animal" in c),
                pens=sum(1 for r in tiles for c in r
                         if isinstance(c, dict) and c.get("kind") in ("PASTURE", "COOP")),
                shed_wheat=int((priv.get("shed") or {}).get("WHEAT", 0)),
                carry_wheat=int(carried.get("WHEAT", 0)),
                hungry=sum(1 for r in tiles for c in r if isinstance(c, dict)
                           and "animal" in c and c.get("consecutive_unfed", 0) >= 1),
                money=int(farm["money"]),
                units=1 + len(farm.get("hands") or []),
                nodes=len(RT.build_nodes(tiles, day, collections.Counter(priv.get("shed") or {}),
                                         carried, set(farm.get("unlocked_quadrants") or ["NW"]), {})),
            )
        ours = us(obs)
        for a in [ours["farmer"], *ours["hands"]]:
            if isinstance(a, list) and a:
                day_ops[a[0]] += 1
        n0 = len(obs["farms"][0].get("hands") or [])
        n1 = len(obs["farms"][1].get("hands") or [])
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        env.step([{"farmer": ours["farmer"], "hands": list(ours["hands"])[:n0],
                   "market": ours["market"]},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        if env.state[0].status == "DONE":
            break
    rows.append((seen, snap, dict(day_ops)))

    hdr = ("day", "unit", "pens", "anml", "hngry", "shedW", "carrW", "nodes", "money",
           "FEED", "CARE", "WATR", "HARV", "PICK", "PLNT", "PASS")
    print("".join(f"{h:>7}" for h in hdr))
    for day, s, ops in rows:
        if not s: continue
        vals = (day, s["units"], s["pens"], s["animals"], s["hungry"], s["shed_wheat"],
                s["carry_wheat"], s["nodes"], s["money"], ops.get("FEED", 0), ops.get("CARE", 0),
                ops.get("WATER", 0), ops.get("HARVEST", 0), ops.get("PICKUP", 0),
                ops.get("PLANT", 0), ops.get("PASS", 0))
        print("".join(f"{v:>7}" for v in vals))


if __name__ == "__main__":
    main()
