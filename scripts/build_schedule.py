"""Generate a counts-only schedule from a handful of parameters. No tape fields, no tile coordinates.

This is the input our own optimiser has to produce, so it is deliberately the *thin* shape:

    per day:  plants (crop -> count), animals_bought, builds, hires, land, buys, sells

and deliberately NOT `plant_tiles`, `build_tiles`, `land_turns` or `orders`. Those four exist only in a
schedule extracted from somebody's replay, they are worth $23,470 (`scripts/schedule_ladder.py`), and
optimising against them would both flatter us and be their work rather than ours.

Every parameter below is derived from a measurement, and the source is named. The leader's tape is used
the way you would use a strong opponent's game -- to calibrate the aggregates -- not copied row by row.

The economics, per tile-day at base price:

    MELON        6 units x $250 over ~13 days  = $115   the best crop, and the ONE that saturates
    WHEAT        6 units x  $25 over ~5 days   =  $30   the only 4-day crop: a tile recycler
    STRAWBERRY   4 units x $120, ongoing       =  $27   slow to start, then steady
    CARROT       4 units x  $35 over ~4 days   =  $35
    TOMATO       4 units x  $60, ongoing       =  low

So melon up to its demand cap, strawberry as the bulk, wheat to turn ground over and to catch the late
price ramp. `docs/market_game_framing_kimi_2026-08-05.md` measured melon as the sole thin product --
inventory +100, price halved 250 -> 150 -- and everything else clearing with prices RISING all season,
wheat +116%, because the town's eight shops unlock across days 3-24.

That price ramp is why late capacity is worth ~1.5-2x early capacity, and it is why a wave of fast wheat
near the end of the season is a real play rather than a quirk.

**Wheat has three jobs and only two are worth having.** Feed: 1 unit per animal per day, BOUGHT, because
a wheat tile yields six units and sits on ground worth $115/day as melon. Recycling: the 4-day cycle
turns tiles over. Flipping: the tape moves 648 surplus units at a 3.4% spread for +$9,106 and ~$29k of
tied-up capital -- refused here, because our own BUY_ANIMAL already fails on a $16 bank.
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import routines as R

SEASON = R.SEASON_DAYS

#: Calibrated to the leader's aggregates, which is what a strong opponent's game is for. Every one of
#: these is a scalar the search can move; none of them is a tile.
DEFAULTS = dict(
    # --- the herd. 14 pens, COW-heavy: a cow is $400 for 6 milk at $160 on a 2-day interval, a sheep
    # $500 for 6 wool at $200 on a 3-day interval. No geese: an egg is $50.
    herd=[(0, "COW", 3), (0, "SHEEP", 1), (5, "COW", 1), (5, "SHEEP", 1), (6, "COW", 1),
          (8, "SHEEP", 4), (9, "COW", 1), (10, "COW", 2)],
    # --- land. NE is $1,000, SW $2,000, SE $4,000. The DAY is a floor, not an instruction: the agent
    # buys on or after it, as soon as the bank covers the price, which is what the tape does at hour 20.
    land_days=[7, 10],
    # --- the crew. Fibonacci and reset every dawn, so 4 hands is $7/day and 12 is $376. Ramp, never
    # peak early: the tape pays the small number for the ten days it has no income.
    hands=[4, 4, 5, 5, 6, 6, 6, 8, 10, 11, 12] + [12] * (SEASON - 11),
    # --- crops. Counts per day, not tiles. Melon is capped by its own demand.
    melon_cap=16,
    plan=[(0, "MELON", 7), (0, "WHEAT", 10), (1, "WHEAT", 1), (2, "MELON", 1),
          (4, "MELON", 2), (4, "STRAWBERRY", 2), (4, "WHEAT", 6),
          (7, "MELON", 1), (7, "STRAWBERRY", 4), (7, "WHEAT", 4),
          (8, "STRAWBERRY", 8), (8, "WHEAT", 3), (9, "STRAWBERRY", 5),
          (10, "STRAWBERRY", 4), (10, "WHEAT", 1),
          (11, "MELON", 2), (11, "STRAWBERRY", 6), (11, "WHEAT", 2),
          (12, "MELON", 1), (12, "STRAWBERRY", 8), (12, "WHEAT", 1),
          (13, "MELON", 3), (13, "STRAWBERRY", 5),
          (14, "MELON", 2), (14, "STRAWBERRY", 2), (14, "WHEAT", 1),
          (15, "MELON", 2), (15, "WHEAT", 2), (16, "WHEAT", 2), (17, "WHEAT", 1),
          # The late wheat wave. Prices ramp with shop unlocks, so a 4-day crop sown here is worth
          # ~2x the same tiles on day 5, and it needs no new land.
          (26, "WHEAT", 31), (27, "WHEAT", 1)],
    # --- feed. Derived, not copied: one wheat per animal per day, plus a small buffer for the days a
    # hand cannot reach every pen. The tape's 967 units include ~650 of flipping we deliberately skip.
    feed_buffer=1.15,
)


def herd_size_by_day(herd):
    """Animals alive each day, assuming every purchase lands and nothing escapes."""
    alive = [0] * SEASON
    for day, _animal, n in herd:
        for d in range(day, SEASON):
            alive[d] += n
    return alive


def build(params=None):
    p = dict(DEFAULTS, **(params or {}))
    rows = {d: dict(plants=[], animals_bought={}, builds=0, places=[], hires=0, land=0,
                    seeds={}, buys={}, sells={}, money_dawn=None, hands=0,
                    plant_tiles=[], build_tiles=[], land_turns=[], orders=[])
            for d in range(SEASON)}

    # crew
    for d in range(SEASON):
        rows[d]["hands"] = rows[d]["hires"] = int(p["hands"][d])

    # herd
    for day, animal, n in p["herd"]:
        rows[day]["animals_bought"][animal] = rows[day]["animals_bought"].get(animal, 0) + n
        rows[day]["builds"] += n
        rows[day]["places"].extend([animal] * n)

    # land
    for d in p["land_days"]:
        rows[d]["land"] += 1

    # crops, with the melon cap enforced rather than trusted
    melons = 0
    for day, crop, n in p["plan"]:
        if crop == "MELON":
            n = min(n, max(0, p["melon_cap"] - melons))
            melons += n
        if n <= 0:
            continue
        rows[day]["plants"].extend([crop] * n)
        rows[day]["seeds"][crop] = rows[day]["seeds"].get(crop, 0) + n

    # feed: one wheat per animal per day, bought, with a buffer. NOT the tape's 967.
    alive = herd_size_by_day(p["herd"])
    for d in range(SEASON):
        need = int(round(alive[d] * p["feed_buffer"]))
        if need:
            rows[d]["buys"]["WHEAT"] = need

    # sells: everything the farm can hold, left for the agent to fill against the real shed. A
    # counts-only schedule cannot know what will be in store, so this is an upper bound per product and
    # the agent sells what it actually has.
    for d in range(1, SEASON):
        for prod in ("WHEAT", "STRAWBERRY", "MELON", "MILK", "WOOL", "FERTILIZER"):
            rows[d]["sells"][prod] = 99
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/seed_scripts/generated/schedule.json")
    args = ap.parse_args()
    rows = build()
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({str(d): r for d, r in rows.items()}, indent=1))

    tot = collections.Counter()
    for r in rows.values():
        tot.update(r["plants"])
    animals = collections.Counter()
    for r in rows.values():
        animals.update(r["animals_bought"])
    print(f"wrote {out}")
    print(f"  plantings {dict(tot)} = {sum(tot.values())}      (tape: WHEAT 66 STRAW 44 MELON 21 = 131)")
    print(f"  animals   {dict(animals)} = {sum(animals.values())}                (tape: COW 8 SHEEP 6 = 14)")
    print(f"  wheat feed bought {sum(r['buys'].get('WHEAT', 0) for r in rows.values())}"
          f"          (tape: 967, of which ~319 is feed and ~648 a flip we skip)")
    print(f"  land days {[d for d in rows if rows[d]['land']]}   peak crew {max(r['hands'] for r in rows.values())}")
    print(f"  tape-only fields carried: "
          f"{sum(len(r['plant_tiles']) + len(r['build_tiles']) + len(r['orders']) for r in rows.values())}"
          f"   <- must be 0")


if __name__ == "__main__":
    main()
