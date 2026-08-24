"""Rank every (seed, day) by the idle-hands defect: PASSing unit-turns while standing work rots.

Three separate losses were found by luck sharing this signature:

    d4  tetsuya board   two hands PASS every hour -> 3 pens unfed -> escape overnight
                        -> herd short 1-3 all season (`the_day_idles_while_the_herd_starves`)
    d12-14 game 93593633  idle 77/93/41 while strawberry died unwatered (`work_to_be_done` §2a)
    season vs kawa tape   +171 idle unit-turns, -$11,544 (`the_opening_is_a_tape...` §4)

None was found by looking. This script looks: it plays whole seasons -- our agent in seat 0, a
recorded kawashigi season in seat 1, shops left FREE and weeds at the ladder rate, because pinning
the draw makes seeds meaningless (`how_much_does_the_draw_move_us.py`) -- and scores every day:

    idle      PASSing unit-turns that day (farmer + hands)
    hungry    pens whose animal misses tonight's escape roll (fed_today False AND
              consecutive_unfed >= 1 -- one more miss and `kaggriculture.py:817` replaces it)
    dry       tiles one more dry night from weeding (not watered today AND
              consecutive_unwatered >= 1 -- `kaggriculture.py:783`)
    standing  yield_units still on the field at dusk, which decays or is discarded

A day with high idle AND nonzero deficit is a day the JOB GENERATOR failed -- work existed, crew
existed, and no node connected them. That is the layer this branch exists to fix, so the output is
ranked by `idle * (hungry*400 + dry*30 + standing)` -- escape-class losses weighted at the cost of
a restocked animal, tile-class at roughly a strawberry's worth, standing at its face value.

    python -u scripts/audit_idle_hands.py --seeds 6 --first-seed 11
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
SEASON_DAYS = 30
MELON_TAPE = "data/seed_scripts/kawashigi/92498144.json"
TEAM = "カワシギ"

#: Weights for the severity score, in dollars-ish. Escape = restock ($400-500) plus days of lost
#: yield; a weeded tile = seed plus re-growth time; standing units = what they would have banked.
W_ESCAPE, W_WEED, W_STANDING = 450.0, 30.0, 5.0


def dusk_deficits(obs, seat):
    """`(hungry pens, dry tiles, standing units)` from an end-of-day observation."""
    farm = obs["farms"][seat]
    tiles = farm["tiles"]
    hungry = dry = standing = 0
    for row in tiles:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if tile.get("kind") in ("PASTURE", "COOP") and tile.get("animal"):
                if not tile.get("fed_today", True) and tile.get("consecutive_unfed", 0) >= 1:
                    hungry += 1
            elif tile.get("kind") == "PLANT":
                if not tile.get("watered_today", True) and tile.get("consecutive_unwatered", 0) >= 1:
                    dry += 1
                standing += max(0, int(tile.get("yield_units", 0) or 0))
    return hungry, dry, standing


def _census(obs, seat):
    """{pos: animal} for every stocked pen, read at a fixed phase of the day."""
    out = {}
    for y, row in enumerate(obs["farms"][seat]["tiles"]):
        for x, tl in enumerate(row):
            if isinstance(tl, dict) and tl.get("kind") in ("PASTURE", "COOP"):
                out[(x, y)] = tl.get("animal")
    return out


def play(seed, weeds, economy, opp_policy, verbose=False):
    """One season. Returns per-day rows and final money."""
    from kaggle_environments import make

    import breakdown as B
    SA = __import__("kagg.search.schedule_agent", fromlist=["schedule_agent"])
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    cfg = dict(economy or {}, seed=seed, weedSpawnChance=weeds)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    agent = SA.make_agent(sched, 0)

    rows = []
    idle = hungry = dry = standing = 0
    prev_money = None
    prev_census = None
    escapes = 0
    placed_recently = set()
    for t in range(SEASON_DAYS * TPD):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0 = agent(o0)
        theirs = opp_policy(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o1["farms"][1].get("hands") or [])
        for slot in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
            if slot and slot[0] == "PASS":
                idle += 1
            if slot and slot[0] == "PLACE" and len(slot) >= 3:
                # A PLACE this turn or the last two can explain a vanished animal legally.
                pass
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                   "market": a0["market"]},
                  {"farmer": theirs.get("farmer") or ["PASS"],
                   "hands": list(theirs.get("hands") or [])[:n1],
                   "market": theirs.get("market") or []}])
        # Dusk = after the last turn of the day. The rollover has not run yet, so fed_today /
        # watered_today still say who missed TODAY, and tomorrow's escape/weed rolls are decided.
        if t % TPD == TPD - 1:
            o = env.state[0].observation
            h, d, s = dusk_deficits(o, 0)
            # Real escape detection: post-step(t=23) IS next dawn -- the rollover ran inside this
            # step. An animal present last dawn and gone now, with no PLACE to explain it, escaped.
            # (The dusk `hungry` flag above CANNOT see escapes: the escaped animal is already gone.)
            census = _census(o, 0)
            if prev_census is not None:
                for pos, animal in prev_census.items():
                    if animal and not census.get(pos):
                        escapes += 1
            prev_census = census
            money = float(o["farms"][0]["money"])
            rows.append({"day": t // TPD, "idle": idle, "hungry": h, "dry": d,
                         "standing": s, "escapes": escapes,
                         "banked": money - prev_money if prev_money is not None else 0.0})
            prev_money = money
            idle = 0
        if env.done:
            break
    return rows, float(env.state[0].observation["farms"][0]["money"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--first-seed", type=int, default=11)
    ap.add_argument("--stride", type=int, default=97)
    ap.add_argument("--weeds", type=float, default=0.005)
    a = ap.parse_args()

    import breakdown as B
    replay = str(REPO / MELON_TAPE)
    economy = B.env_config(replay)
    opp_factory = B.tape_policy(replay, TEAM, 1)

    all_rows = []
    finals = []
    for i in range(a.seeds):
        seed = a.first_seed + a.stride * i
        print(f"seed {seed} ...", flush=True)
        rows, final = play(seed, a.weeds, economy, opp_factory)
        finals.append(final)
        for r in rows:
            r["seed"] = seed
            r["score"] = (r["idle"] * (r["hungry"] * W_ESCAPE + r["dry"] * W_WEED
                                       + r["standing"] * W_STANDING))
            all_rows.append(r)
        season_escapes = rows[-1]["escapes"] if rows else 0
        print(f"    escapes this season: {season_escapes}")
        bad = [r for r in rows if r["hungry"] or (r["dry"] and r["idle"]) ]
        if bad:
            for r in bad:
                print(f"    d{r['day']:<3} idle={r['idle']:<4} hungry={r['hungry']} "
                      f"dry={r['dry']:<3} standing={r['standing']}")
        else:
            print("    clean")

    print(f"\n{len(all_rows)} player-days across {a.seeds} seeds; "
          f"final money mean {sum(finals)/len(finals):,.0f}\n")
    print(f"{'seed':>8} {'day':>4} {'idle':>5} {'hungry':>7} {'dry':>4} {'standing':>9} "
          f"{'banked':>10} {'score':>12}")
    for r in sorted(all_rows, key=lambda r: -r["score"])[:20]:
        print(f"{r['seed']:>8} d{r['day']:<3} {r['idle']:>5} {r['hungry']:>7} {r['dry']:>4} "
              f"{r['standing']:>9} {r['banked']:>10,.0f} {r['score']:>12,.0f}")

    tot_idle = sum(r["idle"] for r in all_rows)
    flagged = [r for r in all_rows if r["score"] > 0]
    print(f"\nsummary: {tot_idle} idle unit-turns total; "
          f"{len(flagged)} days carry a nonzero defect score; "
          f"escape-class days: {sum(1 for r in all_rows if r['hungry'])}")


if __name__ == "__main__":
    main()
