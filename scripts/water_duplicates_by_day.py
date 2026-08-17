"""Which days water the same tile twice -- ours and the tape's -- for the whole season.

`reference/kaggriculture.py:431`:

    if op == "WATER":
        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"): return
        if tile["watered_today"]: return
        tile["watered_today"] = True

**The second water on a tile in one day is a no-op.** It costs the turn and changes nothing. So the
`WATER n/m` row in `breakdown.py` counts submitted actions, not tiles served, and a day where the
tape "waters 33" to our 26 can be a day where we both serve 23 tiles.

Measured at d6 the two sides serve 16 tiles each while the row reads 17/19; at d8 it is 23 against
25 while the row reads 26/33. This prints the whole season so the row is never read as a tile count
again.

Tiles come from the PREVIOUS turn's observation, the same rule as `day_ops.py` -- `steps[t]` records
where a unit ENDED UP. A unit that waters does not move, so consecutive reads are stable, but a
repeat reported here is a repeat of POSITION and is worth confirming on a specific day before being
spent.

    python -u scripts/water_duplicates_by_day.py --days 30
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
TPD = 24


from kagg.search.routines import CROP_TABLE as _CROPS      # noqa: E402


def classify(cell, day):
    """What this water actually bought. See `reference/kaggriculture.py:431`."""
    if not isinstance(cell, dict) or cell.get("kind") != "PLANT":
        return "VOID"                      # not a crop tile at all -- the action does nothing
    if cell.get("watered_today"):
        return "NOOP"                      # second water today: returns immediately
    info = _CROPS.get(cell.get("crop")) or {}
    age = day - int(cell.get("planted_day", day))
    if not info.get("ongoing", True):
        lo = (info["max_day"] + 1) // 2
        if lo <= age <= info["max_day"] and cell.get("yield_units", 0) < info["max_yield"]:
            return "YIELD"                 # in-window one-shot water: this IS the produce
    if int(cell.get("consecutive_unwatered", 0)) >= 1:
        return "BRINK"                     # tile weeds tonight without it
    return "IDLE"                          # safe tile, no yield: buys nothing today


def positions(obs, seat):
    farm = obs["farms"][seat]
    out = [tuple(farm.get("farmer") or (4, 4))]
    for h in (farm.get("hands") or []):
        out.append(tuple(h if isinstance(h, (list, tuple)) else h.get("pos", (4, 4))))
    return out


def waters_by_day(make0, opp, seed, weeds, economy, shops, days):
    """`{day: [tile, ...]}` -- every WATER action seat 0 submitted, with the tile it stood on."""
    from kaggle_environments import make
    env = make("kaggriculture", configuration=dict(economy or {}, seed=seed,
                                                   weedSpawnChance=weeds), debug=True)
    env.reset(2)
    p0, p1 = make0(), opp()
    out = collections.defaultdict(list)
    prev = None
    for t in range(days * TPD):
        o0, o1 = env.state[0].observation, env.state[1].observation
        here = positions(o0, 0)
        at = here if t % TPD == 0 else (prev or here)
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        day = t // TPD
        tiles0 = o0["farms"][0].get("tiles") or []
        for u, a in enumerate([a0["farmer"]] + list(a0["hands"] or [])[:n0]):
            if a and a[0] == "WATER" and u < len(at):
                x, y = at[u]
                cell = None
                if 0 <= y < len(tiles0) and 0 <= x < len(tiles0[y]):
                    cell = tiles0[y][x]
                out[day].append(((x, y), classify(cell, day)))
        prev = here
        env.step([a0, a1])
        # The season ends on the env's own terms; stepping past it raises rather than returning.
        if env.done:
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=("straw", "melon"), default="melon")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.005)
    ap.add_argument("--days", type=int, default=30)
    a = ap.parse_args()

    import breakdown as B
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    _MB.OPPONENT_MELON = 0 if a.arm == "straw" else 99

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    replay = str(REPO / (STRAWBERRY_SEASON if a.arm == "straw" else MELON_SEASON))
    opp = lambda: B.tape_policy(replay, TEAM, 1)                      # noqa: E731
    economy, shops = B.env_config(replay), B.recorded_shops(replay)

    def ours():
        agent = SA.make_agent(sched, 0)
        return lambda o, t: agent(o)

    mine = waters_by_day(ours, opp, a.seed, a.weeds, economy, shops, a.days)
    his = waters_by_day(lambda: B.tape_policy(replay, TEAM, 0), opp,
                        a.seed, a.weeds, economy, shops, a.days)

    KINDS = ("YIELD", "BRINK", "IDLE", "NOOP", "VOID")
    print(f"arm {a.arm!r}, seed {a.seed}, weeds {a.weeds}, tape {pathlib.Path(replay).name}")
    print("what each water BOUGHT.  YIELD = in-window one-shot, the water IS the produce.")
    print("BRINK = tile weeds tonight without it.  IDLE = safe tile, no yield, buys nothing.")
    print("NOOP = already watered today, reference:434 returns immediately.\n")
    print(f"{'day':>4}   " + "".join(f"{k[:5]:>6}" for k in KINDS) + "  ours |  "
          + "".join(f"{k[:5]:>6}" for k in KINDS) + "  tape")
    tm = collections.Counter()
    th = collections.Counter()
    for d in range(a.days):
        cm = collections.Counter(k for _t, k in mine.get(d, []))
        ch = collections.Counter(k for _t, k in his.get(d, []))
        tm.update(cm); th.update(ch)
        print(f"{d:>4}   " + "".join(f"{cm[k]:>6}" for k in KINDS)
              + f"{sum(cm.values()):>6} | " + "".join(f"{ch[k]:>6}" for k in KINDS)
              + f"{sum(ch.values()):>6}")
    print("\n  season   " + "".join(f"{tm[k]:>6}" for k in KINDS)
          + f"{sum(tm.values()):>6} | " + "".join(f"{th[k]:>6}" for k in KINDS)
          + f"{sum(th.values()):>6}")
    print(f"\n  productive (YIELD+BRINK)   ours {tm['YIELD']+tm['BRINK']}   "
          f"tape {th['YIELD']+th['BRINK']}")
    print(f"  wasted (IDLE+NOOP+VOID)    ours {tm['IDLE']+tm['NOOP']+tm['VOID']}   "
          f"tape {th['IDLE']+th['NOOP']+th['VOID']}")


if __name__ == "__main__":
    main()
