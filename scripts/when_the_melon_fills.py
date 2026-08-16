"""Do we HARVEST the day-10 melon late, or DELIVER it late? The tile tells you which.

`scripts/how_seb_lands_the_melons.py` shows Seb's first melon HARVEST at h6 and ours at h17, and the
whole investigation has been framed as a delivery problem. But MELON is a one-shot crop
(`max_yield_day` 12, `max_yield` 6): a tile is not harvestable until it is FULL, because
`router._one_shot_is_finished` refuses HARVEST while `room > 0`, matching the env's rule that a
harvest demolishes the tile. So "harvest at h17" may be downstream of "the tile only filled at h16".

This prints, for every MELON tile at or past `first_yield_day` on the day, the `yield_units` and
`watered_today` flag hour by hour, for BOTH seats -- plus the hour each tile first becomes
harvestable. If ours fill hours after his, the harvest is not late, the WATER is.
"""
import json, pathlib, sys
sys.path.insert(0, ".")
from kagg.search import schedule_agent as SA
from kagg.search import router as RT
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy, DEFAULT_TAPE
from kaggle_environments import make

DAY = int(sys.argv[1]) if len(sys.argv) > 1 else 10
PROD = "MELON"
MAXY = RT.CROP[PROD]["max_yield"]
FIRST = RT.CROP[PROD]["first"]
replay, schedule, team = TAPES[DEFAULT_TAPE]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def ripe_tiles(tiles):
    out = []
    for y, row in enumerate(tiles):
        for x, c in enumerate(row):
            if isinstance(c, dict) and c.get("crop") == PROD and DAY - c["planted_day"] >= FIRST:
                out.append((x, y))
    return out


def trace(seat0, label):
    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    p0 = seat0()
    opp = tape_policy(replay, team, 1)
    keys, rows, full_at = None, [], {}
    for t in range(24 * (DAY + 1)):
        o0, o1 = env.state[0].observation, env.state[1].observation
        tiles = o0["farms"][0]["tiles"]
        if t // 24 == DAY:
            if keys is None:
                keys = ripe_tiles(tiles)
            cells = []
            for (x, y) in keys:
                c = tiles[y][x]
                if not isinstance(c, dict) or c.get("crop") != PROD:
                    cells.append("GONE ")
                    continue
                yu = int(c.get("yield_units", 0))
                cells.append(f"{yu}/{MAXY}{'w' if c.get('watered_today') else ' '}")
                if yu >= MAXY and (x, y) not in full_at:
                    full_at[(x, y)] = t % 24
            rows.append(f"  h{t % 24:>2}  " + "  ".join(cells))
        a0, a1 = p0(o0, t), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    print(f"\n===== {label} =====")
    print("  hr   " + "  ".join(f"{k}" for k in keys))
    print("\n".join(rows))
    print(f"  -> hour each tile first reached {MAXY}/{MAXY} (harvestable): "
          + ("  ".join(f"{k}=h{v}" for k, v in sorted(full_at.items())) or "NEVER on this day"))
    return full_at


trace(lambda: tape_policy(replay, team, 0), "SEB (the tape)")
trace(lambda: (lambda a: (lambda o, t: a(o)))(SA.make_agent(thin, 0, router=True)), "OURS")
