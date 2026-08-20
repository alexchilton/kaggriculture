"""Play a real game with a lookup clone of a teacher, and grade it on OPS, not money.

    python -u scripts/clone_play.py --team tetsuya \
        --dirs data/seed_scripts/downloads_2026-08-20 data/seed_scripts/downloads_2026-08-19 \
        --holdout <episode-id> --days 10

The clone is a table, not a network. Per UNIT it keys on `(day, hour, x, y, tile-underneath)` and
falls back to `(day, hour, tile-underneath)` then `(day, hour)` then PASS. The market keys on
`(day, hour, per-product drain counts)` and falls back to `(day, hour)` then no orders.

**Both feature sets are measured, not chosen.** Leave-one-game-out over 20 held-out games, the unit
op goes 70.1% (clock alone) -> 86.2% with position and tile; board WITHOUT the clock scores 35.9%,
which is the control that says this is signal and not near-duplicate retrieval. The market bundle
goes 58.6% (clock alone) -> 67.6% with drains. See
`docs/the_market_is_one_token_not_nine_heads_2026-08-20.md`.

**The held-out game is excluded from the table.** Grading a lookup on a game it memorised is not a
measurement, and this project has already made that exact error once today -- a shop-keyed table
read 98.6% in-sample and 39.0% held out.

Graded per day, op for op, against what the teacher actually did in that same game. Money is
deliberately not the headline: the market is shared, so a clone playing a different opponent banks
a different number for reasons that say nothing about the imitation.
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

SHOPS = {"BAKERY": ["EGG", "WHEAT"], "PIZZA_SHOP": ["MILK", "TOMATO", "WHEAT"],
         "BRUNCH_SPOT": ["EGG", "WHEAT", "STRAWBERRY"], "YARN_STORE": ["WOOL"],
         "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"], "PET_CAFE": ["CARROT"],
         "SMOOTHIE_SHOP": ["STRAWBERRY", "MILK"],
         "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"]}
PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL"]
MOVES = ("NORTH", "SOUTH", "EAST", "WEST")
GRID_OPS = ("PLANT", "WATER", "HARVEST", "FEED", "CARE", "COLLECT_FERTILIZER",
            "BUILD_PASTURE", "PLACE_ANIMAL", "PICKUP", "DROP", "PASS", "move")


def drains(shops):
    c = collections.Counter()
    for s in shops:
        for p in SHOPS.get(s, ()):
            c[p] += 1
    return tuple(c[p] for p in PRODUCTS)


def tile_kind(cell):
    if cell is None:
        return "."
    if isinstance(cell, dict):
        if "animal" in cell:
            return "A:%s:%d" % (cell["animal"], int(cell.get("yield_units", 0) or 0) > 0)
        if cell.get("kind") == "PLANT":
            return "P:%s:%d" % (cell.get("crop"), int(cell.get("yield_units", 0) or 0) > 0)
        return str(cell.get("kind"))
    return str(cell)


def unit_positions(farm):
    out = [tuple(farm.get("farmer") or (4, 4))]
    for h in (farm.get("hands") or []):
        out.append(tuple(h if isinstance(h, (list, tuple)) else h.get("pos", (4, 4))))
    return out


def build_tables(paths, team, holdout):
    """`(unit_table, market_table)` from every game of `team` EXCEPT `holdout`."""
    unit = collections.defaultdict(collections.Counter)
    tape = collections.defaultdict(collections.Counter)
    unit_u = collections.defaultdict(collections.Counter)
    unit_c = collections.defaultdict(collections.Counter)
    market = collections.defaultdict(collections.Counter)
    market_c = collections.defaultdict(collections.Counter)
    games = 0
    for p in paths:
        if p.stem == holdout:
            continue
        try:
            d = json.loads(p.read_text())
        except Exception:                                          # noqa: BLE001
            continue
        names = [str(n) for n in ((d.get("info") or {}).get("TeamNames") or [])]
        if team not in names:
            continue
        seat = names.index(team)
        games += 1
        steps = d.get("steps") or []
        for i, step in enumerate(steps):
            if i == 0:
                continue
            prev = (steps[i - 1][seat] or {}).get("observation") or {}
            if "day" not in prev or "farms" not in prev:
                continue
            day, hour = int(prev.get("day", 0) or 0), int(prev.get("hour", 0) or 0)
            farm = (prev.get("farms") or [None, None])[seat] or {}
            tiles = farm.get("tiles") or []
            act = (step[seat] or {}).get("action") or {}
            units = [act.get("farmer")] + list(act.get("hands") or [])
            for u, pos in enumerate(unit_positions(farm)):
                if u >= len(units) or not units[u]:
                    continue
                a = tuple(units[u])
                x, y = pos
                try:
                    under = tile_kind(tiles[y][x])
                except Exception:                                  # noqa: BLE001
                    under = "?"
                unit[(day, hour, x, y, under)][a] += 1
                # **The TAPE key: unit slot and clock, no board at all.** If the teacher is
                # open-loop -- the same sequence on every board, weeds included -- then unit `u`
                # at a given (day, hour) does the same thing regardless of what it is standing on.
                # Position-keyed lookups cannot express that, because position is an OUTPUT of the
                # sequence: one wrong move and every later key misses.
                tape[(day, hour, u)][a] += 1
                unit_u[(day, hour, under)][a] += 1
                unit_c[(day, hour)][a] += 1
            shops = sorted(str(v) for v in ((prev.get("town") or {}).get("unlocked_shops") or []))
            orders = tuple(tuple(o) for o in (act.get("market") or [])
                           if isinstance(o, (list, tuple)) and o)
            market[(day, hour, drains(shops))][orders] += 1
            market_c[(day, hour)][orders] += 1
    return (unit, unit_u, unit_c, tape), (market, market_c), games


TAPE_MODE = False


def make_clone(tables):
    (unit, unit_u, unit_c, tape), (market, market_c) = tables

    def act(observation, seat):
        farm = observation["farms"][seat]
        tiles = farm.get("tiles") or []
        day, hour = int(observation.get("day", 0) or 0), int(observation.get("hour", 0) or 0)
        chosen = []
        for u, pos in enumerate(unit_positions(farm)):
            if TAPE_MODE:
                c = tape.get((day, hour, u))
                chosen.append(list(c.most_common(1)[0][0]) if c else ["PASS"])
                continue
            x, y = pos
            try:
                under = tile_kind(tiles[y][x])
            except Exception:                                      # noqa: BLE001
                under = "?"
            for table, key in ((unit, (day, hour, x, y, under)),
                               (unit_u, (day, hour, under)),
                               (unit_c, (day, hour))):
                c = table.get(key)
                if c:
                    chosen.append(list(c.most_common(1)[0][0]))
                    break
            else:
                chosen.append(["PASS"])
        shops = sorted(str(v) for v in ((observation.get("town") or {}).get("unlocked_shops") or []))
        orders = ()
        for table, key in ((market, (day, hour, drains(shops))), (market_c, (day, hour))):
            c = table.get(key)
            if c:
                orders = c.most_common(1)[0][0]
                break
        return {"farmer": chosen[0], "hands": chosen[1:],
                "market": [list(o) for o in orders]}
    return act


def mix_of(path, team):
    """Crop and animal mix for one game: the vector the arms are actually defined on."""
    d = json.loads(pathlib.Path(path).read_text())
    names = [str(n) for n in ((d.get("info") or {}).get("TeamNames") or [])]
    if team not in names:
        return None
    seat = names.index(team)
    c = collections.Counter()
    for step in (d.get("steps") or [])[1:]:
        act = (step[seat] or {}).get("action") or {}
        for u in [act.get("farmer")] + list(act.get("hands") or []):
            if u and u[0] == "PLANT" and len(u) > 1:
                c["P:" + str(u[1])] += 1
        for o in (act.get("market") or []):
            if isinstance(o, (list, tuple)) and o and o[0] == "BUY_ANIMAL" and len(o) > 1:
                c["A:" + str(o[1])] += 1
    return c


def arm_mates(paths, team, holdout, within):
    """Games whose crop/animal mix is within `within` of the holdout's. The holdout stays out."""
    mixes = {p.stem: mix_of(p, team) for p in paths}
    target = mixes.get(holdout)
    if not target:
        return paths
    keys = set(target)
    for m in mixes.values():
        if m:
            keys |= set(m)
    keys = sorted(keys)

    def dist(m):
        tot = sum(max(target[k], m[k]) for k in keys)
        return sum(abs(target[k] - m[k]) for k in keys) / tot if tot else 1.0

    return [p for p in paths
            if p.stem == holdout or (mixes.get(p.stem) and dist(mixes[p.stem]) < within)]


def op_label(a):
    if not a:
        return "PASS"
    return "move" if a[0] in MOVES else a[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", required=True)
    ap.add_argument("--dirs", nargs="+", required=True)
    ap.add_argument("--holdout", required=True)
    ap.add_argument("--days", type=int, default=10)
    # **Keep the played game IN the table.** Not a cheat when the question is drift: if a clone
    # cannot reproduce a game it has memorised, the failure is compounding error on its own
    # trajectory, not a missing entry. That is the difference between needing more data and
    # needing on-policy correction, and they have opposite fixes.
    ap.add_argument("--memorise", action="store_true")
    ap.add_argument("--arm", type=float, default=None,
                    help="build the tape ONLY from games in the same crop/animal-mix arm as the "
                         "holdout, within this distance. Oracle arm selection: it isolates "
                         "'does the arm fix planting' from 'can we pick the arm'.")
    ap.add_argument("--tape", action="store_true",
                    help="key units on (day, hour, unit slot) only -- the open-loop tape")
    args = ap.parse_args()

    from kaggle_environments import make

    paths = []
    for d in args.dirs:
        paths.extend(sorted(pathlib.Path(d).glob("*.json")))
    held = next(p for p in paths if p.stem == args.holdout)
    d = json.loads(held.read_text())
    names = [str(n) for n in ((d.get("info") or {}).get("TeamNames") or [])]
    seat = names.index(args.team)
    other = 1 - seat

    if args.arm is not None:
        paths = arm_mates(paths, args.team, args.holdout, args.arm)
        print("arm: %d games share the holdout's crop/animal mix within %.2f"
              % (len(paths), args.arm), flush=True)
    ut, mt, games = build_tables(paths, args.team,
                                 None if args.memorise else args.holdout)
    tables = (ut, mt)
    print("table built from %d games of %r, %s\n"
          % (games, args.team,
             "game INCLUDED (memorised)" if args.memorise
             else "holding out %s" % args.holdout),
          flush=True)
    global TAPE_MODE
    TAPE_MODE = args.tape
    clone = make_clone(tables)

    cfg = dict(d.get("configuration") or {})
    cfg.pop("steps", None)
    env = make("kaggriculture", configuration=cfg, debug=False)
    env.reset(2)
    opp = [((f[other] or {}).get("action") or {}) for f in d["steps"][1:]]

    ours = collections.defaultdict(collections.Counter)
    for t in range(719):
        if env.done:
            break
        ob = env.state[seat].observation
        day = int(ob.get("day", 0) or 0)
        if day > args.days:
            break
        n = [len((env.state[0].observation["farms"][i] or {}).get("hands") or []) for i in (0, 1)]
        m = clone(ob, seat)
        for a in [m["farmer"]] + list(m["hands"])[:n[seat]]:
            ours[day][op_label(a)] += 1
        st = opp[t] if t < len(opp) else {}
        a = [None, None]
        a[seat] = {"farmer": m["farmer"], "hands": list(m["hands"])[:n[seat]],
                   "market": m["market"]}
        a[other] = {"farmer": st.get("farmer") or ["PASS"],
                    "hands": list(st.get("hands") or [])[:n[other]],
                    "market": st.get("market") or []}
        env.step(a)

    his = collections.defaultdict(collections.Counter)
    steps = d["steps"]
    for i, step in enumerate(steps):
        if i == 0:
            continue
        prev = (steps[i - 1][seat] or {}).get("observation") or {}
        if "day" not in prev:
            continue
        day = int(prev.get("day", 0) or 0)
        if day > args.days:
            break
        act = (step[seat] or {}).get("action") or {}
        for a in [act.get("farmer")] + list(act.get("hands") or []):
            if a:
                his[day][op_label(a)] += 1

    print("clone / teacher, same board, d0-d%d\n" % args.days)
    print("%-4s %s" % ("day", " ".join("%11s" % o[:11] for o in GRID_OPS)))
    print("-" * (5 + 12 * len(GRID_OPS)))
    tot_o, tot_h = collections.Counter(), collections.Counter()
    for day in range(args.days + 1):
        cells = []
        for o in GRID_OPS:
            a_, b_ = ours[day][o], his[day][o]
            tot_o[o] += a_
            tot_h[o] += b_
            cells.append("%11s" % ("%d/%d" % (a_, b_)))
        print("%-4d %s" % (day, " ".join(cells)))
    print("-" * (5 + 12 * len(GRID_OPS)))
    print("%-4s %s" % ("sum", " ".join("%11s" % ("%d/%d" % (tot_o[o], tot_h[o]))
                                       for o in GRID_OPS)))
    work = [o for o in GRID_OPS if o not in ("PASS", "move", "PICKUP", "DROP")]
    err = sum(abs(tot_o[o] - tot_h[o]) for o in work)
    tot = sum(tot_h[o] for o in work)
    print("\nwork ops (excl PASS/move/PICKUP/DROP): teacher %d, clone off by %d (%.1f%%)"
          % (tot, err, 100.0 * err / max(1, tot)))


if __name__ == "__main__":
    main()
