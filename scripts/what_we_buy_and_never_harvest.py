"""What we buy that we never sow, and what we grow that we never collect.

Two questions Alex asked on 2026-08-25, answered on the shipped agent rather than on a downloaded
replay, because the replays are the artifact of one board and this is the code that ships.

1. "why do we need to buy more than we ever plant" -- per crop, BUY_SEED total against PLANT total
   for a whole season. The gap is unconditional loss at `RT.SEED_COST`.

2. "which harvest things we never harvest ... anything we always dont harvest probably doesnt need
   planting or buying in the first place" -- every planting episode, whether it ever became
   harvestable, and how many units were standing on it when it died or when the bell rang.

The distinction that matters, from `reference/kaggriculture.py`:

    :453   a HARVEST needs `day - planted_day >= first_yield_day`
    :224   a non-ongoing crop dies at `(planted_day + max_yield_day + 1) * turns_per_day`

So a planting has three possible fates, and only the third is a routing defect:

    NEVER RIPE      planted_day + first_yield_day > 29   -- could not have been collected. Do not
                    plant it, and do not buy the seed.
    EXPIRED         it ripened, then passed max_lifespan_step with units still on it.
    STOOD AT BELL   it ripened, it was still alive on the last turn, nobody walked to it.

Usage:
    python -u scripts/what_we_buy_and_never_harvest.py --seeds 700 701
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
LAST_DAY = 29
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


def _fate_of_gone_tile(obs, seat, x, y):
    """What replaced a crop tile tells you whether it was collected.

    `HARVEST` on a non-ongoing crop takes EVERY unit and sets the tile to `None`
    (`reference/kaggriculture.py:464-469`), so a successful harvest makes the tile vanish -- there is
    no `yield_units` decrement to watch for. A tile that runs past `max_lifespan_step` instead decays
    one unit at a time and becomes `{"kind": "WEED"}` (`:764-766`), as does one left unwatered two
    days running (`:783`).

    So: gone-to-None is COLLECTED, gone-to-WEED is LOST. Reading the units instead scores every
    successful harvest as an abandonment, which is exactly the error this function exists to undo.
    """
    tiles = obs["farms"][seat].get("tiles") or []
    try:
        t = tiles[y][x]
    except (IndexError, TypeError):
        return "unknown"
    if t is None:
        return "COLLECTED"
    if isinstance(t, dict) and t.get("kind") == "WEED":
        return "WEEDED"
    return "REPLACED"


def _board(obs, seat):
    """Yield (x, y, tile) for every planted tile of `seat`.

    A tile is `None` (empty), the string `"LOCKED"` (unowned quadrant) or a string naming a
    structure, or a dict for a crop. Only the dicts carry `crop`/`planted_day`/`yield_units`.
    """
    tiles = obs["farms"][seat].get("tiles") or []
    for y, row in enumerate(tiles):
        for x, t in enumerate(row):
            if isinstance(t, dict):
                yield x, y, t


def _play(seed, opponent="contrarian"):
    from kaggle_environments import make

    from kagg.arena.pool import OPPONENTS, _build
    import kagg.search.schedule_agent as SA

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
    env.reset(2)
    me = SA.make_agent(sched, 0, router=True)
    them = _build(OPPONENTS[opponent], None)

    # key: (x, y, planted_day, crop) -> dict of the episode
    episodes = {}
    prev_seeds = collections.Counter()
    bought = collections.Counter()
    planted = collections.Counter()
    harv_by_day = collections.Counter()
    prev_key = {}

    for step in range(30 * TPD):
        o0 = env.state[0].observation
        day = step // TPD

        # --- seed ledger. private["seeds"] has exactly two writers: BUY_SEED adds, PLANT removes.
        cur = collections.Counter({k: int(v) for k, v in
                                   ((o0.get("private") or {}).get("seeds") or {}).items()})

        # --- board, before the turn is taken
        live = {}
        for x, y, t in _board(o0, 0):
            crop = t.get("crop")
            if not crop:
                continue
            key = (x, y, int(t.get("planted_day", day)), crop)
            live[(x, y)] = key
            ep = episodes.setdefault(key, {"crop": crop, "planted_day": key[2],
                                           "peak": 0, "last_units": 0, "last_step": step,
                                           "harvested": 0})
            u = int(t.get("yield_units", 0) or 0)
            if u < ep["last_units"]:
                # units left the tile: a HARVEST took them (nothing else decrements it)
                ep["harvested"] += ep["last_units"] - u
                harv_by_day[day] += ep["last_units"] - u
            ep["peak"] = max(ep["peak"], u)
            ep["last_units"] = u
            ep["last_step"] = step

        for pos, key in prev_key.items():
            if pos not in live and key in episodes:
                ep = episodes[key]
                if "gone_step" not in ep:
                    ep["gone_step"] = step
                    ep["gone_as"] = _fate_of_gone_tile(o0, 0, pos[0], pos[1])
                    if ep["gone_as"] == "COLLECTED":
                        ep["harvested"] += ep["last_units"]
                        harv_by_day[day] += ep["last_units"]
                        ep["last_units"] = 0
        prev_key = live

        a0 = me(o0, env.configuration)
        n0 = len(o0["farms"][0].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"] or [])[:n0],
                   "market": a0["market"]},
                  them(env.state[1].observation, env.configuration)])

        nxt = collections.Counter({k: int(v) for k, v in
                                   (((env.state[0].observation.get("private")) or {})
                                    .get("seeds") or {}).items()})
        # plants this turn = tiles that appeared with planted_day == day
        new_plants = collections.Counter()
        for x, y, t in _board(env.state[0].observation, 0):
            crop = t.get("crop")
            if crop and int(t.get("planted_day", -1)) == day and (x, y) not in live:
                new_plants[crop] += 1
        for c in set(nxt) | set(cur) | set(new_plants):
            planted[c] += new_plants[c]
            bought[c] += nxt[c] - cur[c] + new_plants[c]
        prev_seeds = nxt

        if env.done:
            break

    held = {k: int(v) for k, v in
            (((env.state[0].observation.get("private")) or {}).get("seeds") or {}).items()
            if int(v or 0) > 0}
    return bought, planted, held, episodes, harv_by_day


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[700, 701])
    ap.add_argument("--opponent", default="contrarian")
    args = ap.parse_args()

    crop_meta = {
        "WHEAT": (2, 4), "CARROT": (2, 3), "TOMATO": (8, 8),
        "STRAWBERRY": (10, 10), "MELON": (10, 12),
    }
    cost = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "MELON": 80, "STRAWBERRY": 100}

    for seed in args.seeds:
        bought, planted, held, episodes, harv_by_day = _play(seed, args.opponent)

        print(f"\n{'='*78}\nSEED {seed}   vs {args.opponent}\n{'='*78}")
        print("\n1. SEED LEDGER -- bought against sown, whole season")
        print(f"{'crop':<12} {'bought':>7} {'planted':>8} {'unsown':>7} {'held@bell':>10} {'$ wasted':>9}")
        waste = 0
        for c in sorted(set(bought) | set(planted)):
            un = bought[c] - planted[c]
            w = max(0, un) * cost.get(c, 0)
            waste += w
            print(f"{c:<12} {bought[c]:>7} {planted[c]:>8} {un:>7} {held.get(c,0):>10} {w:>9}")
        print(f"{'':<12} {'':>7} {'':>8} {'':>7} {'TOTAL':>10} {waste:>9}")

        print("\n2. EVERY PLANTING, BY FATE")
        fate = collections.Counter()
        lost_units = collections.Counter()
        rows = []
        for (x, y, pd, crop), ep in episodes.items():
            fy, my = crop_meta.get(crop, (2, 4))
            ripe_day = pd + fy
            standing = ep["last_units"]
            gone_as = ep.get("gone_as")
            if gone_as == "COLLECTED":
                f = "collected"
                standing = 0
            elif ripe_day > LAST_DAY:
                f = "NEVER RIPE -- could not have been collected"
            elif gone_as == "WEEDED":
                f = "ROTTED, ripe and left to weed"
            elif "gone_step" not in ep:
                f = "STOOD AT BELL, ripe and never walked to"
            else:
                f = f"gone as {gone_as}"
            fate[f] += 1
            if standing > 0 or ripe_day > LAST_DAY:
                lost_units[crop] += standing
                rows.append((pd, ripe_day, crop, (x, y), ep["harvested"], standing, f))

        for f, n in fate.most_common():
            print(f"   {n:>4} plantings  {f}")

        print("\n3. THE PLANTINGS THAT LOST UNITS  (planted -> ripe, units taken/left)")
        print(f"{'planted':>8} {'ripe':>5} {'crop':<11} {'tile':<8} {'took':>5} {'LEFT':>5}  fate")
        for r in sorted(rows):
            print(f"{r[0]:>8} {r[1]:>5} {r[2]:<11} {str(r[3]):<8} {r[4]:>5} {r[5]:>5}  {r[6]}")
        print(f"\n   units left standing by crop: {dict(lost_units)}")

        print("\n4. HARVEST BY DAY  (units actually taken off tiles)")
        print("   " + "  ".join(f"d{d}:{harv_by_day.get(d,0)}" for d in range(20, 30)))
        print("   season total harvested units:", sum(harv_by_day.values()))


if __name__ == "__main__":
    main()
