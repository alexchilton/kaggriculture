"""Turn the target algorithm into a planner schedule. No change to `schedule_agent` at all.

The planner already buys against a CUMULATIVE target -- `want_total` sums `animals_bought` over
every day up to today (`schedule_agent.py:5372`) -- and already floats the cow/sheep split on the
shop draw (`SHOP_ADAPT_HERD`, `_herd_split`). So a target state does not need new machinery in the
agent: differencing the targets day to day produces exactly the per-day rows it already consumes,
and its cumulative logic then does the steering.

That is the whole reason for building it this way. The alternative -- computing targets live inside
the agent -- means editing a 6,000-line file whose every branch is load-bearing, to reach the same
place.

What comes from where:

    animals_bought, places   differenced from the COW/SHEEP targets, floored at zero
    plants, seeds            differenced from the crop targets
    land                     differenced from the `owned` target, in parcels of 25
    builds                   one pen per animal that has no pen yet
    hires/hands, buys, sells the cluster's representative season, unchanged

`sells` and `buys` stay as recorded on purpose: the planner clamps them with the engine's own rule
(`n = min(have, row["sells"][prod])`, `schedule_agent.py:5111`). **An over-ask on `buys` is NOT a
no-op** -- the sentence that used to end here said it was. The engine drops an unaffordable
`BUY_PRODUCT` silently and he plays on, while our planner holds the order in a market slot and spends
the money: at d7 he offers `WHEAT 48` on a world that fills 11. `buys` and `sells` must come from
`scripts/tape_fills.py`, and `scripts/schedule_guard.py` refuses a schedule where they did not. The
clamp below is only about
sides. The herd and the field are what a wrong number actually costs.

**Floored at zero, and this is not a detail.** A target that falls -- his sheep peak at d27 and end
at p50 2 -- is reached by NOT FEEDING, never by a negative purchase. The drop is the season
boundary (216 escapes on d27, 472 on d28) and it is free money, not a plan to copy. So a falling
target means "buy nothing more", and the feed rule handles the rest.
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.spa_targets import (CLUSTERS, QUANTITIES, Ridge, Matrix, load, shops_by_day)

SEASON = 30
CROPS = ("WHEAT", "STRAWBERRY", "CARROT", "MELON", "TOMATO")
TILES_PER_PARCEL = 25

#: The pen order, measured over 179 seasons (`scripts/spataro_geometry.py`): which tile is used
#: k-th, with the two swapped pairs resolved to their more common order. NOT read by the planner --
#: it seats pens itself from `PEN_SPOTS` -- but recorded here because it is the geometry half of
#: layers 1 and 2, and the first thing to check if the board comes out wrong.
PEN_ORDER = ((4, 4), (3, 4), (2, 4), (3, 3), (4, 2), (1, 3), (1, 4), (6, 3), (8, 3), (5, 4))

#: Species for the first six slots, hard-wired because they do not float: COW 100/90%, SHEEP 94/96%,
#: COW 87/85%. Slot 6 on is the algorithm's, and slot 6 is day 5-6 -- when the first shop is known.
PEN_SPECIES = ("COW", "COW", "SHEEP", "SHEEP", "COW", "COW")


def rising(series):
    """Day-to-day increases only. A falling target is reached by not feeding, never by unbuying."""
    out, prev = [], None
    for v in series:
        out.append(0 if prev is None else max(0, int(round(v)) - int(round(prev))))
        prev = max(prev, v) if prev is not None else v   # a dip must not create a phantom rebuy
    return out


def build(model, shops_timeline, base_rows, start_day=3):
    """`{day: row}` for a whole season, given when each shop opens and a base for days < start_day.

    `shops_timeline` is `[(day, shop)]` -- what the world will do. Offline this comes from a
    cluster's typical draw; live it is read off `town.unlocked_shops` as it happens.
    """
    def shops_at(day):
        return tuple(s for d, s in sorted(shops_timeline) if d <= day)

    tgt = {d: model.predict(d, shops_at(d)) for d in range(SEASON)}
    series = {q: [tgt[d][q] for d in range(SEASON)] for q in QUANTITIES}
    delta = {q: rising(series[q]) for q in ("COW", "SHEEP", "GOOSE") + CROPS}
    # Land in whole parcels, from the `owned` target. **He funds exactly TWO in all 179 seasons**
    # (`scripts/spataro_landed_schedule.py`), so a schedule asking for three is asking for a season
    # he does not play -- and a parcel planned and not bought leaves routes seated on ground we
    # never own, which is the `add_land` failure in CLAUDE.md.
    #
    # The days before `start_day` come from the base row verbatim, so their parcels must advance
    # the running total from the BASE row and not from the model. Taking the model's answer for
    # days whose row is then discarded counted the opening's parcel twice and asked for three.
    owned = [int(round(v)) for v in series["owned"]]
    land = []
    have = owned[0] if owned else TILES_PER_PARCEL
    for d, v in enumerate(owned):
        if d < start_day:
            got = int((base_rows.get(str(d)) or {}).get("land") or 0)
            land.append(got)
            have += got * TILES_PER_PARCEL
            continue
        want = max(0, (v - have) // TILES_PER_PARCEL)
        land.append(want)
        have += want * TILES_PER_PARCEL

    out, pens = {}, 0
    for d in range(SEASON):
        if d < start_day:
            out[str(d)] = dict(base_rows[str(d)])
            # **Carry the BASE row's standing-pen count, do not re-derive it from `builds`.**
            # `builds` counts transitions -- a tile built, lost and rebuilt is two -- so a running
            # sum of it overshoots the board. The base rows carry `pens` as an absolute
            # end-of-day count (`scripts/spataro_landed_schedule.py`); trust that.
            pens = int(out[str(d)].get("pens") or pens + int(out[str(d)].get("builds") or 0))
            continue
        base = dict(base_rows.get(str(d)) or {})
        bought = {a: delta[a][d] for a in ("COW", "SHEEP", "GOOSE") if delta[a][d]}
        places = []
        for a, n in bought.items():
            places += [a] * n
        # One pen per animal that does not have one. `places` is what the pen planner reads
        # (`_place_animals`), so the two must agree or an animal is bought and never placed.
        need = len(places)
        row = dict(base)
        row["animals_bought"] = bought
        row["places"] = places
        row["builds"] = need
        # **`pens` is the ABSOLUTE count the day ends on -- what `_refresh_pins` now targets.**
        # The matrix gives animal counts, and one pen holds one animal, so the pen count is the
        # running total of pens ever needed. It is written out rather than left for the planner to
        # sum, because summing `builds` is the bug this field exists to remove (measured at d7:
        # ice cream 13 pens against his 11, pizza 15/14, bakery 13/12).
        pens += need
        row["pens"] = pens
        row["land"] = land[d]
        row["plants"] = [c for c in CROPS for _ in range(delta[c][d])]
        seeds = Counter(row["plants"])
        row["seeds"] = dict(seeds) if seeds else {}
        out[str(d)] = row
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="data/seed_scripts/spataro/schedule.json",
                    help="days 0..start_day-1 and the buys/sells/hires columns come from here")
    ap.add_argument("--out-dir", default="data/seed_scripts/spa_targets")
    ap.add_argument("--start-day", type=int, default=3)
    ap.add_argument("--alpha", type=float, default=1.0)
    args = ap.parse_args()

    seasons = load()
    model = Ridge(args.alpha).fit(seasons)
    mat = Matrix().fit(seasons)
    base_rows = json.loads((ROOT / args.base).read_text())
    out_dir = ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"fitted on {len(seasons)} seasons\n")

    # The typical unlock timeline per cluster: his own median unlock DAY per shop position, with the
    # cluster's own shop first. A schedule is generated per cluster because the schedule is fixed at
    # make_agent time while shops open during the game; the router installs the right one at d3.
    for cluster, shops in CLUSTERS.items():
        timeline = [(3, shops[0]), (6, "PIZZA_SHOP"), (9, "FARMERS_MARKET"),
                    (12, "BAKERY"), (15, "BRUNCH_SPOT")]
        timeline = [(d, s) for d, s in timeline if s != shops[0] or d == 3]
        sched = build(model, timeline, base_rows, args.start_day)
        (out_dir / f"{cluster}.json").write_text(json.dumps(sched, indent=1))
        herd = Counter()
        crops = Counter()
        for d in range(SEASON):
            herd.update(sched[str(d)].get("animals_bought") or {})
            crops.update(sched[str(d)].get("plants") or [])
        print(f"{cluster:12} herd {dict(herd)}  land "
              f"{sum(sched[str(d)]['land'] for d in range(SEASON))}  "
              f"plants {dict(crops)}")

    (out_dir / "meta.json").write_text(json.dumps(
        {"model": "ridge alpha=%g on 8 shop-open indicators" % args.alpha,
         "seasons": len(seasons), "start_day": args.start_day,
         "pen_order": PEN_ORDER, "pen_species": PEN_SPECIES,
         "base": args.base,
         "source": "scripts/targets_to_schedule.py"}, indent=1))
    print(f"\nwrote {out_dir}/*.json")


if __name__ == "__main__":
    main()
