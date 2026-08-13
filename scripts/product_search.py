"""Search the PRODUCT MIX jointly -- carrot, herd, geese, melon/strawberry -- on win rate.

`scripts/field_sweep.py` sweeps ONE module flag at a time. That is the wrong instrument for this
question and today proved it twice: carrot only paid in combination with a change to how ground is
allocated, and the sign of that combination flipped depending on which opponent it was measured
against (+$4,194 against the victor tape, -$5,478 against Seb). A knob measured alone, on one seed,
against one opponent, has produced a false negative here four times for carrot and five times for
animals (`CLAUDE.md`, "animals don't pay" was an artifact four separate times).

Two of the four dials are not flags at all. Carrot count and the melon/strawberry split are rows in
`data/seed_scripts/victor/schedule.json`, so this mutates the SCHEDULE in memory as well as setting
module flags, and never writes to disk.

## What is scored

**Win rate. Never money.** The ladder is Elo: a $43k win and a $4k win score identically. Mean bank
is printed beside it purely as a liveness check -- an arm banking ~$3,000 did nothing at all and its
win rate is meaningless (`CLAUDE.md`, "verify built artifacts actually run").

## What this is NOT

The field is the opponents we happened to record, and Alex downloads LOSSES, so the sample is
conditioned on the outcome. Read every number here as "does this arm beat these opponents better
than that arm does", which is a valid RELATIVE comparison. It is not a rating and cannot be
converted into one.

## What each game records, and which of it is a fill

The dump's first seven keys -- `tag, seed, opponent, seat, ours, theirs, win` -- plus the six axis
values are FROZEN. A sweep appending to `data/logs/product_search.jsonl` writes exactly that shape,
so `--analyse` reads every later field with `.get` and reports rows that lack one rather than
dropping them.

The later fields are all fills or board counts, never order quantities:

- **`planted`** -- tiles that really carry a crop, from `buy_seed fills - seeds left in hand`.
  `private["seeds"]` has two writers and only two, so this is exact. It is NOT the arm's `carrot`
  value: that is a number of rows added to a schedule, and the schedule already had some.
- **`sold_units`** -- units that committed through `_commit_unit`, per product.
- **`seed_units`** -- `BUY_SEED` units that committed.
- **`shops`** -- the town's actual draw, `[[name, instances], ...]`.

**The shop draw is recorded, not derived, and that is a correction.** It looks like a pure function
of the seed: `random.Random((seed * 1_000_003) ^ day)`, one `rng.choice` per unlock. It is not.
`_end_of_day` spends that same generator on `_spawn_weeds` first, once per EMPTY tile per player, so
where the draw lands in the stream depends on how much of the board each side had built on. Measured
across three seeds with weeds off: the first unlock matches between two different agent pairings and
every later one diverges. A derived draw would be right for day 3 and wrong for the other seven.

## Held-out seeds

`--seeds` are the search seeds and `--holdout` a disjoint set the search never sees. The winner is
re-scored on the holdout and both numbers are reported. A fixed 3-seed objective once reported +40%
where held-out seeds said +12.8%, and a search confirmed only on its own seeds wandered for 14
generations to gain 1.6%. An arm that wins on search seeds and not on holdout is the winner's curse,
not a finding.

    PYTHONPATH=. .venv/bin/python -u scripts/product_search.py --arms 40 --seeds 6 --holdout 6
"""
import argparse
import collections
import itertools
import json
import pathlib
import random
import statistics
import sys
import time
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, ".")

from reference.kaggriculture import SHOPS

REPO = pathlib.Path(__file__).resolve().parent.parent
PLAN = REPO / "data/seed_scripts/victor/schedule.json"
FIELD = REPO / "data/seed_scripts/field"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders",
             "money_dawn", "money_dusk", "bank", "tiles", "weeds")

#: Days that take a carrot planting, in the leader's own window. He plants 1-2 a day on d21-d26
#: BESIDE 4-11 wheat, for a season total of 1-8 across all 66 downloaded games -- 8 is a ceiling he
#: never crosses. The search deliberately runs PAST it, to 12, because "the leader does not" is not
#: evidence that it does not pay; he may simply be leaving it there.
CARROT_DAYS = (21, 22, 23, 24, 25, 26)
CARROT_SELL_DAYS = (24, 25, 26, 27, 28, 29)
CARROT_SEED_DAY = 6

#: The axis the leader trades: MELON 20/STRAWBERRY 34 in 51 games, MELON 12/STRAWBERRY 42 in 14.
#: A strict binary for him, decided at d5 h2 on a single BUY_SEED. For us it is just a ratio in the
#: plants row, so it is swept continuously across and beyond his two points.
MELON_BASE = 19

#: Crops an arm can move, so a per-game plant count has somewhere to go.
CROP_AXES = ("WHEAT", "MELON", "STRAWBERRY", "CARROT", "TOMATO")


def base_schedule():
    raw = json.loads(PLAN.read_text())
    return {int(k): {kk: vv for kk, vv in row.items() if kk not in TAPE_ONLY}
            for k, row in raw.items()}


def apply_arm(sched, arm):
    """Mutate a schedule dict IN MEMORY for one arm. Never touches disk."""
    sched = {d: {k: (list(v) if isinstance(v, list) else dict(v) if isinstance(v, dict) else v)
                 for k, v in row.items()} for d, row in sched.items()}

    # ---- carrot: N tiles spread over the leader's own window, ADDED beside the wheat.
    n = arm["carrot"]
    if n > 0:
        per = [n // len(CARROT_DAYS)] * len(CARROT_DAYS)
        for i in range(n % len(CARROT_DAYS)):
            per[i] += 1
        days = tuple(arm["carrot_start"] + j for j in range(len(CARROT_DAYS)))
        for day, k in zip(days, per):
            if k and day in sched:
                sched[day]["plants"] = list(sched[day].get("plants") or []) + ["CARROT"] * k
        if CARROT_SEED_DAY in sched:
            s = dict(sched[CARROT_SEED_DAY].get("seeds") or {})
            s["CARROT"] = s.get("CARROT", 0) + n
            sched[CARROT_SEED_DAY]["seeds"] = s
        # `max_yield` 4, but a plain water inside a two-day window realistically lands 2-3.
        quota = max(1, (n * 3 + len(CARROT_SELL_DAYS) - 1) // len(CARROT_SELL_DAYS))
        for day in CARROT_SELL_DAYS:
            if day in sched:
                s = dict(sched[day].get("sells") or {})
                s["CARROT"] = s.get("CARROT", 0) + quota
                sched[day]["sells"] = s

    # ---- melon/strawberry: move `shift` tiles from melon to strawberry, or back.
    # **Only from `melon_day` onward.** A re-aim applied to the whole season cannot tell us
    # whether the DAY matters, which is the question the leader's d5 h2 branch poses.
    shift = arm["melon_shift"]
    if shift:
        moved = 0
        want = abs(shift)
        src, dst = ("MELON", "STRAWBERRY") if shift > 0 else ("STRAWBERRY", "MELON")
        for day in sorted(d for d in sched if d >= arm["melon_day"]):
            plants = sched[day].get("plants") or []
            if src not in plants:
                continue
            out = []
            for c in plants:
                if c == src and moved < want:
                    out.append(dst)
                    moved += 1
                else:
                    out.append(c)
            sched[day]["plants"] = out
            if moved >= want:
                break
    return sched


#: The module attribute that controls the goose count, or None if the machinery is not in the tree.
#: **It currently is not.** `7a88d30` deleted it ("Delete the geese rather than leave a losing flag
#: in the tree"), and that deletion rests on goose arms measured while EGG was absent from
#: `SELLABLE` -- i.e. while no egg this farm produced could ever be sold. Resolved at import rather
#: than with a `hasattr` at the call site, because a per-worker `hasattr` that silently skips turns
#: a swept axis into a no-op and still prints a win rate for it.
GEESE_FLAG = next((n for n in ("HERD_GEESE", "GEESE", "HERD_GOOSE", "WANT_GEESE")
                   if hasattr(__import__("kagg.search.schedule_agent_1455mh",
                                         fromlist=["x"]), n)), None)


def _play(job):
    """One seating of one seed against one recorded opponent, for one arm."""
    arm, seed, opp_file, swapped, field = job
    # **The field path travels IN THE JOB.** A module-level global set in the parent is
    # not inherited by a spawned worker on every platform, and a worker that silently
    # falls back to the default directory would score a different field than the header
    # printed -- the exact class of error this file exists to avoid.
    field = pathlib.Path(field)
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills
    from kagg.search import schedule_agent_1455mh as SA

    # Module flags. Set per worker process, which is why the pool is `ProcessPoolExecutor` -- a
    # thread pool would race on module state and silently mix arms.
    SA.WOOL_SHOP_COW_CAP = arm["cow_cap"]
    if GEESE_FLAG:
        setattr(SA, GEESE_FLAG, arm["geese"])

    me_seat = 1 if swapped else 0
    me = SA.make_agent(apply_arm(base_schedule(), arm), me_seat, router=True)

    acts = json.loads((field / opp_file).read_text())["actions"]
    idle = {"farmer": ["PASS"], "hands": [], "market": []}

    def them(obs, config=None):
        t = int(obs.get("step", 0) or 0)
        if t >= len(acts):
            return idle
        farmer, hands, market = acts[t]
        owned = len((obs.get("farms") or [{}, {}])[1 - me_seat].get("hands") or [])
        return {"farmer": list(farmer), "hands": [list(h) for h in hands[:owned]],
                "market": [list(o) for o in market]}

    pair = (them, me) if swapped else (me, them)
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    # **Additive, and deliberately outside the scored quantities.** `record_fills` wraps the env's
    # own `_commit_unit`; it observes and changes nothing. `mine`/`theirs` below are read from the
    # rewards exactly as before, so the win rate this search selects on cannot move.
    with record_fills(env) as fills:
        env.run(list(pair))
    final = env.steps[-1]
    mine = float(final[me_seat]["reward"] or 0)
    theirs = float(final[1 - me_seat]["reward"] or 0)

    # The shop draw the town actually made. RECORDED, not derived: it looks like a pure function of
    # the seed and is not -- `_end_of_day` runs `_spawn_weeds` on the same generator first, once per
    # empty tile per player, so where the draw lands in the stream depends on how the board was
    # played. Measured on three seeds with weeds off: the FIRST unlock matches between two different
    # agent pairings and every later one diverges.
    shops = sorted(collections.Counter(
        env.steps[-1][0]["observation"]["town"].get("unlocked_shops") or []).items())

    # Fills, not offers. The arm's `carrot` axis is a number of rows in a SCHEDULE; whether a carrot
    # was planted, and whether a planted one ever sold, are different questions and the action
    # stream answers neither -- the agent re-posts a standing order on every turn until it fills.
    seeds_left = env.state[me_seat].observation.private.get("seeds") or {}
    sold_units = {p: fills.sold(me_seat, p)[0] for p in fills.products()
                  if fills.sold(me_seat, p)[0]}
    seed_units = {c: fills.units(me_seat, "BUY_SEED", c) for c in CROP_AXES
                  if fills.units(me_seat, "BUY_SEED", c)}
    # `private["seeds"]` has two writers and only two: BUY_SEED adds one, PLANT removes one.
    planted = {c: n - int(seeds_left.get(c, 0) or 0) for c, n in seed_units.items()
               if n - int(seeds_left.get(c, 0) or 0) > 0}
    return (arm["id"], seed, opp_file, swapped, mine, theirs,
            {"shops": shops, "sold_units": sold_units, "seed_units": seed_units,
             "planted": planted})


def opponents(limit, min_money):
    out = []
    for p in sorted(FIELD.glob("*.json")):
        rec = json.loads(p.read_text())
        if rec["team"] == "alex chilton" or rec.get("their_money") is None:
            continue
        if rec["their_money"] < min_money:
            continue
        out.append(p.name)
    return out[:limit] if limit else out


def sample_arms(n, rng):
    """Random search over the JOINT space, amounts AND timing.

    The grid is ~12 x 6 x 9 x 5 x 4 x 3 = 39,000 arms and the axes are not independent, so a random
    sample finds an interaction far sooner than a sweep of any one axis. Timing is in here because
    the leader's melon/strawberry choice is not a quantity at all -- it is a single BUY_SEED at
    **d5 h2**, and everything before that hour is identical across all 66 of his games. If the
    day matters, an axis that only varies the amount can never show it.
    """
    arms = []
    for i in range(n):
        arms.append({
            "id": i,
            # amounts
            "carrot": rng.choice(list(range(0, 13))),
            "melon_shift": rng.choice([-6, -4, -2, 0, 2, 4, 6, 8]),
            "cow_cap": rng.choice([4, 6, 8, 10]),
            "geese": rng.choice([0, 2, 4]),
            # timing
            #: First day of the carrot window. His is d21; earlier means competing with wheat for
            #: ground it has not cleared yet, later means the crop cannot finish.
            "carrot_start": rng.choice([17, 19, 21, 23, 25]),
            #: The day the melon/strawberry re-aim takes effect. HIS IS d5. Sweeping it is the whole
            #: point: if d5 is special the win rate should peak there and nowhere else.
            "melon_day": rng.choice([3, 5, 7, 9, 12]),
        })
    return arms


def label(a):
    return ("carrot %2d@d%-2d  melon %+d@d%-2d  cow %2d  geese %d"
            % (a["carrot"], a["carrot_start"], -a["melon_shift"], a["melon_day"],
               a["cow_cap"], a["geese"]))


def score(results, arm_id):
    rows = [r for r in results if r[0] == arm_id]
    if not rows:
        return 0.0, 0.0, 0
    wins = sum(1 for r in rows if r[4] > r[5])
    draws = sum(1 for r in rows if r[4] == r[5])
    return ((wins + 0.5 * draws) / len(rows),
            statistics.mean(r[4] for r in rows), len(rows))


def run(arms, seeds, opps, workers):
    jobs = [(a, s, o, sw, str(FIELD))
            for a in arms for s in seeds for o in opps for sw in (False, True)]
    out = []
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for k, r in enumerate(ex.map(_play, jobs, chunksize=1), 1):
            out.append(r)
            if k % 50 == 0:
                print("    %5d/%d games  %.0fs" % (k, len(jobs), time.time() - t0), flush=True)
    return out


def dump(path, arms, rows, tag):
    """Every game, one JSON object per line, so any slice can be taken later WITHOUT re-running.

    A search that prints only its own summary forces a re-run for every new question, and the
    questions here are conditional ones -- which arm wins on which seed, against which opponent,
    at which timing. Those are slices of the same games, not new experiments.
    """
    by_id = {a["id"]: a for a in arms}
    with open(path, "a") as fh:
        for aid, seed, opp, swapped, mine, theirs, extra in rows:
            a = by_id[aid]
            # **The original seven keys plus the six axes come first and their shape never
            # changes.** A sweep landing on the remote box appends rows in exactly that form and
            # `--analyse` has to keep reading them, so everything below is additive and every
            # reader of it uses `.get`.
            fh.write(json.dumps({
                "tag": tag, "seed": seed, "opponent": opp, "seat": 1 if swapped else 0,
                "ours": mine, "theirs": theirs, "win": 1 if mine > theirs else (
                    0.5 if mine == theirs else 0),
                **{k: v for k, v in a.items() if k != "id"},
                **(extra or {})}) + "\n")


AXES = ("carrot", "carrot_start", "melon_shift", "melon_day", "cow_cap", "geese")


def carriers(row, product):
    """Unlocked shop INSTANCES that sell `product` in this game, or None if the row predates the
    field. Instances, not names: two `YARN_STORE` drain WOOL twice as hard as one, and a
    `FARMERS_MARKET` carries four products at once, so a slice keyed on a shop NAME means nothing.
    """
    shops = row.get("shops")
    if shops is None:
        return None
    return sum(int(n) for name, n in shops if product in (SHOPS.get(name) or []))


def analyse(path, product="STRAWBERRY"):
    """Slice a dumped run: best combination per seed, per opponent, per timing, per shop draw.

    **Reads rows written before any of the extra fields existed.** The dump's original shape is
    `tag, seed, opponent, seat, ours, theirs, win` plus the six axes, and a sweep is appending rows
    in exactly that shape right now. Everything added since is read with `.get`, and a row missing
    one is counted and reported rather than dropped -- a slice that quietly discards half a run and
    prints a win rate for the rest is worse than one that refuses.
    """
    rows = [json.loads(l) for l in open(path) if l.strip()]
    print("%d games in %s\n" % (len(rows), path))

    def wr(rs):
        return sum(r["win"] for r in rs) / len(rs) if rs else 0.0

    def key(r):
        return tuple(r[a] for a in AXES)

    print("=" * 92)
    print("BEST COMBINATION PER SEED  (an arm that only wins on one seed is seed variance, not a find)")
    print("=" * 92)
    seeds = sorted({r["seed"] for r in rows})
    for sd in seeds:
        rs = [r for r in rows if r["seed"] == sd]
        by = collections.defaultdict(list)
        for r in rs:
            by[key(r)].append(r)
        best = max(by.items(), key=lambda kv: (wr(kv[1]), len(kv[1])))
        print("  seed %-6s n=%-5d best %.3f  carrot %2d@d%-2d melon %+d@d%-2d cow %2d geese %d"
              % (sd, len(rs), wr(best[1]), best[0][0], best[0][1], -best[0][2], best[0][3],
                 best[0][4], best[0][5]))

    print("\n" + "=" * 92)
    print("BEST COMBINATION PER OPPONENT  (the sign flipped by opponent once already today)")
    print("=" * 92)
    for opp in sorted({r["opponent"] for r in rows}):
        rs = [r for r in rows if r["opponent"] == opp]
        by = collections.defaultdict(list)
        for r in rs:
            by[key(r)].append(r)
        best = max(by.items(), key=lambda kv: (wr(kv[1]), len(kv[1])))
        print("  %-26s n=%-5d overall %.3f  best %.3f  carrot %2d@d%-2d melon %+d@d%-2d cow %2d"
              % (opp[:26], len(rs), wr(rs), wr(best[1]), best[0][0], best[0][1],
                 -best[0][2], best[0][3], best[0][4]))

    print("\n" + "=" * 92)
    print("EACH AXIS ON ITS OWN  (marginal; the axes interact, so read it as a hint)")
    print("=" * 92)
    for axis in AXES:
        by = collections.defaultdict(list)
        for r in rows:
            by[r[axis]].append(r)
        print("  %-13s %s" % (axis, "  ".join(
            "%s=%.3f(n%d)" % (k, wr(v), len(v)) for k, v in sorted(by.items()))))

    print("\n" + "=" * 92)
    print("THE d5 QUESTION: melon_day against melon_shift, win rate")
    print("=" * 92)
    days = sorted({r["melon_day"] for r in rows})
    shifts = sorted({r["melon_shift"] for r in rows})
    print("      " + "".join("%9s" % ("mel%+d" % -sh) for sh in shifts))
    for d in days:
        cells = []
        for sh in shifts:
            rs = [r for r in rows if r["melon_day"] == d and r["melon_shift"] == sh]
            cells.append("%9s" % ("%.3f" % wr(rs) if rs else "-"))
        print("  d%-3d" % d + "".join(cells))
    print("\n  If d5 is special the column structure changes at d5 and nowhere else. If every row")
    print("  looks alike, the DAY does not matter to us and his d5 branch is about something the")
    print("  schedule does not express.")

    print("\n" + "=" * 92)
    print("CONDITIONED ON THE SHOP DRAW: %s carriers against each axis, win rate" % product)
    print("=" * 92)
    unconditioned = [r for r in rows if carriers(r, product) is None]
    conditioned = [r for r in rows if carriers(r, product) is not None]
    if unconditioned:
        print("  %d of %d rows have NO SHOP DRAW RECORDED and are excluded from this block only."
              % (len(unconditioned), len(rows)))
        print("  They are rows from a run that predates the field. The draw is NOT recoverable")
        print("  from the seed -- `_end_of_day` spends the same generator on `_spawn_weeds` first,")
        print("  once per empty tile per player, so it depends on how the board was played. Only")
        print("  the first unlock is stable. Re-run those arms to condition them.")
    if not conditioned:
        print("  nothing to slice.")
        return
    print("\n  Why this block exists: a global marginal averages two opposite regimes into a wash.")
    print("  STRAWBERRY drained 179 units in one downloaded game and closed at the $1-3 floor, and")
    print("  1,074 in another and closed at $187, above its base -- and the number of unlocked shop")
    print("  instances carrying it runs 1 to 5 between games. 'this knob does nothing' and 'this")
    print("  knob does opposite things in two regimes' are the same global number.\n")
    buckets = sorted({carriers(r, product) for r in conditioned})
    print("  %-13s %s" % ("carriers", "  ".join("%d=%s" % (
        b, "n%d" % len([r for r in conditioned if carriers(r, product) == b]))
        for b in buckets)))
    for axis in AXES:
        cells = []
        for b in buckets:
            rs = [r for r in conditioned if carriers(r, product) == b]
            by = collections.defaultdict(list)
            for r in rs:
                by[r[axis]].append(r)
            cells.append("%d:[%s]" % (b, " ".join(
                "%s=%.3f" % (k, wr(v)) for k, v in sorted(by.items()))))
        print("  %-13s %s" % (axis, "  ".join(cells)))

    print("\n" + "=" * 92)
    print("WHAT THE ARMS ACTUALLY DID  (fills and board counts -- never an order quantity)")
    print("=" * 92)
    with_fills = [r for r in rows if r.get("planted") is not None]
    if not with_fills:
        print("  no row carries a fill record; those rows predate it. Nothing to say here that")
        print("  is not an offer count, so nothing is printed.")
    else:
        print("  the `carrot` axis is a number of rows added to a SCHEDULE. These are the tiles")
        print("  that were really planted and the units that really sold, per game, averaged.\n")
        print("  %-8s %6s %10s %12s %12s" % ("carrot", "games", "planted", "sold u", "win"))
        by = collections.defaultdict(list)
        for r in with_fills:
            by[r["carrot"]].append(r)
        for n, rs in sorted(by.items()):
            planted = statistics.mean((r.get("planted") or {}).get("CARROT", 0) for r in rs)
            sold = statistics.mean((r.get("sold_units") or {}).get("CARROT", 0) for r in rs)
            print("  %-8d %6d %10.1f %12.1f %12.3f" % (n, len(rs), planted, sold, wr(rs)))
        if len(with_fills) < len(rows):
            print("\n  %d of %d rows carry no fill record and are excluded from this block only."
                  % (len(rows) - len(with_fills), len(rows)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analyse", metavar="JSONL",
                    help="slice a previous run's dump instead of playing anything")
    ap.add_argument("--condition-on", default="STRAWBERRY", metavar="PRODUCT",
                    help="product whose SHOP CARRIER COUNT the --analyse slice conditions on. "
                         "Whether melon or strawberry pays depends on how many unlocked shop "
                         "instances carry it, which runs 1 to 5 between games; a marginal averaged "
                         "over both regimes reads as a wash.")
    ap.add_argument("--dump", default="data/logs/product_search.jsonl",
                    help="where every game is recorded, append-only")
    ap.add_argument("--arms", type=int, default=24)
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--holdout", type=int, default=4)
    ap.add_argument("--first-seed", type=int, default=1000)
    ap.add_argument("--opponents", type=int, default=6)
    ap.add_argument("--min-money", type=float, default=40000,
                    help="drop recorded seats poorer than this; a farm that banked little contested "
                         "no market and measures nothing")
    ap.add_argument("--workers", type=int, default=12)
    #: **Which opponents to play.** Defaults to the LEADER field, not the loss set. Alex's downloads
    #: are conditioned on losing, and those opponents are ones the current candidate should beat
    #: anyway -- an arm that only separates against weak seats has not been tested. 66 seats of the
    #: #1 player are in `field_leaders/`, extracted from his own side of his own games.
    ap.add_argument("--field", default="data/seed_scripts/field_leaders",
                    help="directory of extracted opponent action streams")
    ap.add_argument("--seed", type=int, default=7, help="RNG for the arm sample")
    args = ap.parse_args()

    if args.analyse:
        return analyse(args.analyse, product=args.condition_on)

    global FIELD
    FIELD = REPO / args.field if not pathlib.Path(args.field).is_absolute() else pathlib.Path(args.field)

    rng = random.Random(args.seed)
    arms = sample_arms(args.arms, rng)
    if GEESE_FLAG is None:
        # Loudly, and by pinning the axis to a constant rather than leaving it varying-but-inert.
        print("!! NO GOOSE FLAG IN THE TREE -- the machinery was deleted in 7a88d30, so the geese\n"
              "   axis is PINNED to 0 and is not being searched. Restore it before believing any\n"
              "   statement about geese. The deletion rests on arms measured while EGG was missing\n"
              "   from SELLABLE, i.e. while no egg could be sold at all.\n")
        for a in arms:
            a["geese"] = 0
    search_seeds = list(range(args.first_seed, args.first_seed + args.seeds))
    hold_seeds = list(range(args.first_seed + 500, args.first_seed + 500 + args.holdout))
    opps = opponents(args.opponents, args.min_money)

    print("arms %d   search seeds %s   holdout %s   opponents %d   workers %d"
          % (len(arms), search_seeds, hold_seeds, len(opps), args.workers))
    print("scoring on WIN RATE; mean bank is a liveness check only\n")

    print("SEARCH")
    res = run(arms, search_seeds, opps, args.workers)
    dump(args.dump, arms, res, "search")
    table = sorted(((score(res, a["id"]), a) for a in arms), key=lambda z: -z[0][0])
    print("\n  %-46s %8s %11s %6s" % ("arm", "win", "mean bank", "games"))
    for (wr, bank, n), a in table:
        print("  %-46s %8.3f %11.0f %6d" % (label(a), wr, bank, n))

    # **Confirm on seeds the search never saw.** An arm that leads here and not there is the
    # winner's curse; the project has paid for that lesson twice.
    top = [a for _s, a in table[:3]]
    print("\nHOLDOUT (top 3, seeds the search never saw)")
    res2 = run(top, hold_seeds, opps, args.workers)
    dump(args.dump, top, res2, "holdout")
    print("\n  %-46s %8s %8s %11s" % ("arm", "search", "holdout", "mean bank"))
    for a in top:
        s_wr = score(res, a["id"])[0]
        h_wr, h_bank, _n = score(res2, a["id"])
        print("  %-46s %8.3f %8.3f %11.0f" % (label(a), s_wr, h_wr, h_bank))

    print("\nper-axis marginal win rate (search seeds; read as a hint, not a verdict --")
    print("the axes interact, which is the whole reason this is a joint search)")
    for axis in ("carrot", "melon_shift", "cow_cap", "geese"):
        agg = collections.defaultdict(list)
        for a in arms:
            agg[a[axis]].append(score(res, a["id"])[0])
        print("  %-12s %s" % (axis, "  ".join(
            "%s=%.3f(n%d)" % (k, statistics.mean(v), len(v)) for k, v in sorted(agg.items()))))


if __name__ == "__main__":
    sys.exit(main())
