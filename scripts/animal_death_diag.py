"""Per-death diagnosis of animal loss (`consecutive_unfed >= 2`) on the SHIPPED agent.

Runs the shipped `kagg.search.schedule_agent` agent mirrored against itself (both seats identical,
default flags -- no herd-mix, no sell-side flags changed), full 720-turn season, and tracks every
animal tile on both farms turn by turn. `tiles` are PUBLIC (`reference/kaggriculture.json`: "Per-
player public farm state visible to all agents (tiles, ...)"), so this reads them straight off
`obs["farms"][i]["tiles"]` for both farms from either player's own observation -- no cheating,
just reading what is already shared. `private.shed` and `private.inventories` (farmer + hands) are
per-observation and read from each side's own obs.

FEED only ever affects `farm["tiles"][fy][fx]`, i.e. the unit's OWN current tile
(`reference/kaggriculture.py:299-306` for the fx,fy=pos[0],pos[1] and the FEED handler at
:489-500), so "was a hand there with wheat" is an exact position match with the animal tile, not
an adjacency check.
"""
import collections
import copy
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kaggle_environments import make

from kagg.search import schedule_agent as SA

SEEDS = [11, 13, 17, 19, 23, 29, 41]
TPD = 24

SCHED_PATH = pathlib.Path("data/seed_scripts/top_guys/90976060/schedule.json")


#: Matches `mirror_gate.py`'s own `_thin()` -- EXCLUSION, not a whitelist. The whitelist copied
#: from `tests/test_reservation_sell_cap.py` (`... "animals" ...`) was checked against the real
#: schedule keys and is wrong for this purpose: the schedule's actual field is `"animals_bought"`,
#: not `"animals"` (which does not exist and is always absent), so that whitelist silently drops
#: every animal purchase and the agent buys ZERO animals all season. Confirmed directly: the first
#: version of this script showed peak_herd=0 on all 7 seeds, both farms -- the "0 deaths" it
#: reported was trivially true (no animals existed to die), not a finding. Using the exclusion list
#: mirror_gate.py itself uses (already verified live: its own runs report real MILK/WOOL/MELON/
#: STRAWBERRY sales) fixes this.
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


def thin_schedule():
    sched = {int(k): v for k, v in json.loads(SCHED_PATH.read_text()).items()}
    return {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def shed_tiles(board_size):
    half = board_size // 2
    return {(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)}


def dist_to_shed(pos, board_size):
    sx, sy = pos
    return min(abs(sx - tx) + abs(sy - ty) for tx, ty in shed_tiles(board_size))


def animal_snapshot(tiles, board_size):
    out = {}
    for y in range(board_size):
        for x in range(board_size):
            t = tiles[y][x]
            if isinstance(t, dict) and "animal" in t:
                out[(x, y)] = {
                    "animal": t["animal"], "fed_today": t["fed_today"],
                    "consecutive_unfed": t["consecutive_unfed"], "placed_day": t["placed_day"],
                }
    return out


def hand_state(obs_priv, obs_farm):
    """[(label, pos, inventory_dict), ...] for the farmer and every hand."""
    out = [("farmer", tuple(obs_farm["farmer"]), dict(obs_priv["inventories"][0] or {}))]
    for i, hp in enumerate(obs_farm.get("hands") or []):
        inv = obs_priv["inventories"][i + 1] if i + 1 < len(obs_priv["inventories"]) else {}
        out.append((f"hand{i}", tuple(hp), dict(inv or {})))
    return out


def run_seed(seed):
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0})
    env.reset(2)
    sched = thin_schedule()
    a0 = SA.make_agent(sched, 0, router=True)
    a1 = SA.make_agent(sched, 1, router=True)
    agents = [a0, a1]

    board_size = None
    prev_animals = [dict(), dict()]
    # per-farm, per-day: {"shed_wheat_dawn": n, "hand_log": [(hour, [(label,pos,inv)...], action)]}
    day_log = [collections.defaultdict(dict), collections.defaultdict(dict)]
    deaths = []
    peak_herd = [0, 0]
    herd_by_day = [collections.defaultdict(int), collections.defaultdict(int)]

    for _t in range(720):
        if env.done:
            break
        obs = [env.state[0].observation, env.state[1].observation]
        if board_size is None:
            board_size = len(obs[0]["farms"][0]["tiles"])
        day, hour = obs[0]["day"], obs[0]["hour"]

        acts = []
        for p in (0, 1):
            o = obs[p]
            farm_p = o["farms"][p]
            priv_p = o["private"]
            n = len(farm_p.get("hands") or [])
            a = agents[p](o, env.configuration)
            acts.append({"farmer": a["farmer"], "hands": list(a["hands"])[:n], "market": a["market"]})

            # -- per-farm bookkeeping, using farm p's OWN observation for its own private state --
            if hour == 0:
                day_log[p][day]["shed_wheat_dawn"] = int(priv_p["shed"].get("WHEAT", 0))
            hs = hand_state(priv_p, farm_p)
            day_log[p][day].setdefault("hand_log", []).append((hour, hs, a))

            # -- animal snapshot + death detection, using farm p's tiles from EITHER obs (public) --
            cur = animal_snapshot(farm_p["tiles"], board_size)
            peak_herd[p] = max(peak_herd[p], len(cur))
            if hour == 0:
                herd_by_day[p][day] = len(cur)
            prev = prev_animals[p]
            for pos, info in prev.items():
                if pos not in cur:
                    deaths.append({
                        "farm": p, "day": day, "hour": hour, "pos": pos,
                        "species": info["animal"], "placed_day": info["placed_day"],
                        "dist_to_shed": dist_to_shed(pos, board_size),
                        "consecutive_unfed_before_death": info["consecutive_unfed"],
                    })
            prev_animals[p] = cur

        env.step(acts)

    return {"deaths": deaths, "day_log": day_log, "board_size": board_size,
            "peak_herd": peak_herd, "herd_by_day": herd_by_day}


def wheat_carrier_events(day_log, farm_idx, pos, day):
    """Every turn on `day` a hand/farmer stood on `pos` -- and whether it carried WHEAT and what
    it did instead of FEED."""
    out = []
    for hour, hs, action in day_log[farm_idx].get(day, {}).get("hand_log", []):
        for label, hpos, inv in hs:
            if hpos == pos:
                wheat = int(inv.get("WHEAT", 0))
                if label == "farmer":
                    act = action["farmer"]
                else:
                    idx = int(label.replace("hand", ""))
                    hands = action["hands"]
                    act = hands[idx] if idx < len(hands) else None
                out.append({"hour": hour, "label": label, "wheat": wheat, "action": act})
    return out


def main():
    all_deaths = []
    results = {}
    for seed in SEEDS:
        r = run_seed(seed)
        results[seed] = r
        all_deaths.extend((seed, d) for d in r["deaths"])
        print(f"seed {seed}: {len(r['deaths'])} death(s)   peak herd farm0={r['peak_herd'][0]} "
              f"farm1={r['peak_herd'][1]}   herd@d29 farm0={r['herd_by_day'][0].get(29)} "
              f"farm1={r['herd_by_day'][1].get(29)}")

    print(f"\nTOTAL deaths across {len(SEEDS)} seeds, mirror (both seats), "
          f"{len(SEEDS) * 2} agent-seasons: {len(all_deaths)}")

    for seed, d in all_deaths:
        r = results[seed]
        day_log = r["day_log"]
        farm = d["farm"]
        pos = d["pos"]
        death_day = d["day"]
        print("\n" + "=" * 90)
        print(f"seed {seed} farm {farm}: {d['species']} at {pos}, placed day {d['placed_day']}, "
              f"deleted day {death_day} hour {d['hour']}, dist_to_shed={d['dist_to_shed']}, "
              f"consecutive_unfed at moment of deletion={d['consecutive_unfed_before_death']}")
        fresh = (death_day - d["placed_day"]) <= 2
        print(f"  FRESH PURCHASE (placed <=2 days before death): {fresh}")
        for day in range(max(0, death_day - 2), death_day + 1):
            sw = day_log[farm].get(day, {}).get("shed_wheat_dawn")
            print(f"  day {day}: shed WHEAT at dawn = {sw}")
            events = wheat_carrier_events(day_log, farm, pos, day)
            if not events:
                print(f"    no hand/farmer ever stood on {pos} this day")
            else:
                for e in events:
                    print(f"    hour {e['hour']:>2} {e['label']:<7} wheat_carried={e['wheat']:<3} "
                          f"action={e['action']}")


if __name__ == "__main__":
    sys.exit(main())
