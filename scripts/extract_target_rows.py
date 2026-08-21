"""Extract a player's day as a TARGET ROW -- what the day achieves -- not as an op tape.

Alex, 2026-08-21: "our first d12 is 'basically' the tape ... we really just play the tape from d4-d12
so if that goes wrong so early then our decision tree must be finding the wrong branch".

He was right that something was wrong, and it was not the branch. It was the label.

The shipped agent -- the one with 2600 on the board, exact to d12 -- plays from rows like:

    {"hands": 5, "hires": 5, "land": 0, "builds": 4,
     "places": ["SHEEP","COW","SHEEP","COW"], "feeds": 2, "cares": 2,
     "plants": ["WHEAT", ... "MELON"], "animals_bought": {"COW":2,"SHEEP":2},
     "seeds": {"WHEAT":7,"MELON":12}, "buys": {...}, "sells": {...}}

**No hours, no coordinates, no movement, and no WATER.** The row says what the day achieves; the
router works out how, against the live board, and `_live_ops` re-derives the work at every stop.

`build_day_rows.py` labelled a day with its literal 24-turn op tape instead. Replaying that put
waterings on tiles that were thirsty in KAWASHIGI's game and not in ours, so tiles dried out and
became weeds (`kaggriculture.py:771`, two days unwatered). Measured on seed 7000000: the block
agent had 7 weeds by d3, 14 by d11 and 32 by d16, against the planner's ZERO all season, and its
acreage fell to 22 crops against 49. The money gap followed the acreage gap; selling was downstream.

This also removes the noise that dominated the old label. The measured difference between two of
one player's days was ~55% movement and ~20% watering -- neither of which appears in a target row --
so two days that differed only in how the units walked collapse to the SAME target.

    python -u scripts/extract_target_rows.py --player カワシギ --days 30 \\
        --dirs data/seed_scripts/kawashigi --out data/target_rows_kawa.json
"""

import argparse
import collections
import glob
import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TURNS_PER_DAY = 24
ANIMAL_TOKEN = "ANIMAL"
ANIMAL_NAMES = frozenset(("GOOSE", "COW", "SHEEP"))

#: Ops that are ROUTING, not intent. They never enter a target row -- that is the whole point.
ROUTING = frozenset(("NORTH", "SOUTH", "EAST", "WEST", "PASS", "PICKUP", "DROP", "WATER"))


def target_row(actions, obs_dawn, seat):
    """One day's 24 actions -> what the day achieved. Counts, not positions."""
    plants, places = [], []
    feeds = cares = builds = harvests = fertilises = clears = 0
    hires = land = 0
    animals = collections.Counter()
    seeds = collections.Counter()
    buys = collections.Counter()
    sells = collections.Counter()

    for act in actions:
        for u in [act.get("farmer")] + list(act.get("hands") or []):
            if not u:
                continue
            op = str(u[0])
            if op in ROUTING:
                continue
            if op == "PLANT" and len(u) > 1:
                plants.append(str(u[1]))
            elif op == "PLACE" and len(u) > 1 and str(u[1]) in ANIMAL_NAMES:
                # **PLACE is two ops** (`reference/kaggriculture.py:377`). It puts an animal on a
                # matching unoccupied structure when `item in ANIMALS`; otherwise, standing next to
                # the shed, the same op is a SHED DROP that moves goods out of the hand.
                #
                # Recording both filled the herd field with produce -- over 213 seasons it held
                # STRAWBERRY 2611, WOOL 2084, MELON 1518, FERTILIZER 1123, MILK 953 alongside the
                # animals, so the herd was a minority of its own field. `schedule_agent` reads this
                # to work out which animals are still to be put out and died with
                # `KeyError: 'FERTILIZER'` on d1. Every distinct-row count taken from it was
                # inflated too, because two seasons that carried different produce to the shed split
                # into different rows for a difference that is routing, not plan.
                #
                # A shed drop belongs with DROP and PICKUP in `ROUTING`.
                places.append(str(u[1]))
            elif op == "FEED":
                feeds += 1
            elif op == "CARE":
                cares += 1
            elif op in ("BUILD_PASTURE", "BUILD_COOP"):
                builds += 1
            elif op == "HARVEST":
                harvests += 1
            elif op == "FERTILIZE":
                fertilises += 1
            elif op == "CLEAR":
                clears += 1
        for o in (act.get("market") or []):
            if not o:
                continue
            op = str(o[0])
            n = int(o[2]) if len(o) > 2 else 1
            if op == "HIRE":
                hires += 1
            elif op == "BUY_LAND":
                land += 1
            elif op == "BUY_ANIMAL" and len(o) > 1:
                animals[str(o[1])] += n
            elif op == "BUY_SEED" and len(o) > 1:
                seeds[str(o[1])] += n
            elif op == "BUY_PRODUCT" and len(o) > 1:
                buys[str(o[1])] += n
            elif op == "SELL" and len(o) > 1:
                # **Offers, not fills.** The agent re-posts an order every turn, so this is the
                # quota it ASKED for. `kagg/analysis/fills.py` is what gives realised volume. For a
                # target row the quota is the right quantity anyway -- it is the intent.
                sells[str(o[1])] = max(sells[str(o[1])], n)

    # **`hands` is read by the executor and was missing.** `schedule_agent.py:394` does
    # `want = int(row.get("hands", 0) or 0)`, so a row without it silently asks for a crew of ZERO
    # and the whole day runs on the lone farmer while the row still looks well formed. The crew
    # evaporates nightly and is rebuilt each morning, so the shipped rows carry hands == hires
    # (d0 5/5, d1 0/0, d2 4/4) and this mirrors that.
    return {"hands": hires,
            "hires": hires, "land": land, "builds": builds,
            "places": sorted(places), "feeds": feeds, "cares": cares,
            "plants": sorted(plants), "harvests": harvests,
            "fertilises": fertilises, "clears": clears,
            "animals_bought": dict(sorted(animals.items())),
            "seeds": dict(sorted(seeds.items())),
            "buys": dict(sorted(buys.items())),
            "sells": dict(sorted(sells.items()))}


#: **The herd species is not part of the plan.** COW and SHEEP both build a PASTURE and which one
#: pays is decided by the shop draw, so `block_agent.preferred_pasture_animal` substitutes it at
#: play time from the live town. Hashing the species therefore splits one plan into several rows for
#: a difference the executor is going to overwrite anyway.
#:
#: Alex, 2026-08-21: "you keep making the same mistake - the 'moves or other things' like animals
#: are not unique but most is". Correct, and this is the third place the same over-splitting has
#: appeared: routing in the op-tape label, then species in the op-tape label, now species here.
def normalise_herd(row):
    """A copy of the row with the species blanked, keeping the COUNTS, which do matter."""
    out = dict(row)
    out["places"] = sorted(ANIMAL_TOKEN if p in ANIMAL_NAMES else p
                           for p in (row.get("places") or []))
    bought = row.get("animals_bought") or {}
    out["animals_bought"] = {ANIMAL_TOKEN: sum(int(v or 0) for v in bought.values())} \
        if bought else {}
    return out


def row_id(row):
    return hashlib.md5(json.dumps(normalise_herd(row), sort_keys=True).encode()).hexdigest()[:10]


def read(path, player, days):
    rep = json.loads(pathlib.Path(path).read_text())
    if not isinstance(rep, dict) or not rep.get("steps"):
        return []
    names = (rep.get("info") or {}).get("TeamNames") if isinstance(rep.get("info"), dict) else None
    if not names or player not in names:
        return []

    out = []
    for seat, nm in enumerate(names):
        if nm != player:
            continue
        turns = collections.defaultdict(dict)
        dawn = {}
        for step in rep["steps"]:
            if seat >= len(step):
                continue
            cell = step[seat]
            obs = cell.get("observation") or {}
            day, hour = int(obs.get("day", 0) or 0), int(obs.get("hour", 0) or 0)
            if day >= days or cell.get("action") is None:
                continue
            turns[day][hour] = cell["action"]
            if hour == 0:
                dawn[day] = obs
        for day, hh in turns.items():
            if len(hh) != TURNS_PER_DAY or day not in dawn:
                continue
            row = target_row([hh[h] for h in range(TURNS_PER_DAY)], dawn[day], seat)
            out.append({"game": pathlib.Path(path).stem, "seat": seat, "day": day,
                        "target": row, "target_id": row_id(row)})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--player", required=True)
    ap.add_argument("--dirs", nargs="+", required=True)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    paths = []
    for d in args.dirs:
        paths += sorted(glob.glob(d.rstrip("/") + "/*.json"))
    rows = []
    for p in paths:
        rows += read(p, args.player, args.days)

    games = {(r["game"], r["seat"]) for r in rows}
    print("%s: %d day-rows from %d game-seats\n" % (args.player, len(rows), len(games)))

    per_day = collections.defaultdict(collections.Counter)
    for r in rows:
        per_day[r["day"]][r["target_id"]] += 1
    print("%4s %8s %10s %8s %8s" % ("day", "games", "distinct", "top", "cover90"))
    for day in sorted(per_day):
        c = per_day[day]
        n = sum(c.values())
        run = need = 0
        for _k, v in c.most_common():
            run += v
            need += 1
            if run >= 0.9 * n:
                break
        print("%4d %8d %10d %7.1f%% %8d"
              % (day, n, len(c), 100.0 * c.most_common(1)[0][1] / n, need))

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows))
    print("\nwrote %s" % out)


if __name__ == "__main__":
    main()
