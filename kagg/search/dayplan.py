"""Schedule in, tape out. A per-day op assigner, replacing the per-season job reservation.

`routines.py` gives a unit one job for the whole season: `grow()` claims turns on every day from
`plant_day` to the end, and `ranch()` does the same from `start_day`. That is why our tape and his
diverge in a way no search could close. Measured at his own schedule
(`scripts/measure_refusal_day.py`, `scripts/measure_his_op_budget.py`):

  - our hands run **11.5-16.4 of 23 work turns** a day against his 17.7-21.3, **and**
  - the same crew **refuses twelve of his plantings**, including all 31 tiles of his day-26 wave,
  - with **205 free turns sitting unused** across the crew on the one day a refusal was a turn
    shortage at all. The other eleven refusals were ground, not turns.

Idle hands and refused work in the same hour is not a capacity problem, and the fix is not a bigger
crew: the hire ladder is Fibonacci and resets every dawn, so the 16 hands that reservation forces
cost $2,583 a day against his 12 at $376. It is an assignment problem. A hand with eleven free turns
on day 4 refuses the day-4 job because its day 20 is full, and a tile is held for the season even
after its crop clears -- while his 131 plantings run over ~61 tiles, replanting each as it empties.

So this module inverts the loop. Instead of

    for each job:  reserve a unit for the season, lay out all 30 days

it runs

    for each day:  collect the ops the farm needs today, then pack them onto today's hands

which is what his tape does. A hand feeds a pen, waters four tiles and harvests a fifth on the same
day, and does something else tomorrow. His census shows no hand is single-purpose: hand 0 is
`WATER:75 FEED:60 PICKUP:46 CARE:41`, hand 1 is `WATER:77 COLLECT_FERTILIZER:39`.

What this module does NOT change, deliberately, because both were measured and neither is the bug:

  - **Routing.** Ours is 1.49 walk turns per work turn against his 1.44. Walking is not where the
    season goes, and `_path_ops` already handles the locked-quadrant trap that cost unit 2 two thirds
    of a melon block.
  - **The mix.** His 44/21 strawberry/melon, our calculator's 48/12 and both crosses all banked
    $15-$309 at our scale. The mix is downstream of being able to work the board at all.
"""

import collections
import math

from . import routines as R

TPD = R.TURNS_PER_DAY
WORK_TURNS = TPD - 1                    # turn 0 of a day is the market order
SPAWN = tuple(R.SPAWN)
SHED = set(R.shed_access_tiles())

#: Ongoing crops keep producing after a harvest; one-shot crops clear the tile back to EMPTY, which
#: is what makes his replanting possible. `max_day` is when a one-shot's window shuts -- miss it and
#: `_decay_plants` eats the yield.
CROP = R.CROP_TABLE


def _walk(src, dst):
    return R._path_ops(src, dst)


def _steps(src, dst):
    return len(_walk(src, dst))


class Farm:
    """Just enough farm state to know what work each day needs. Not a simulator.

    Deliberately thin: the real environment is the judge, and a second simulator here would be a
    second thing to keep true. This tracks only what decides *which op to emit* -- crop age, water
    debt, herd size -- and gets the rest wrong on purpose rather than expensively.
    """

    def __init__(self):
        self.crops = {}                 # tile -> dict(crop, planted, last_water, last_harvest)
        self.pens = {}                  # tile -> dict(animal, placed, last_feed)
        self.parcels = 0

    def free(self, tile):
        return tile not in self.crops and tile not in self.pens


def _board(parcels_by_day):
    """Tiles usable on each day, nearest the shed first.

    Order matters twice over: a tile close to `SPAWN` is cheap to reach every day for the whole
    season, and PICKUP/DROP only work on a shed-access tile, so the herd -- which draws wheat daily --
    wants the four cells around `(4,4)` and the crops want everything else.
    """
    all_tiles = [(x, y) for y in range(R.BOARD_SIZE) for x in range(R.BOARD_SIZE)]
    by_day = {}
    for day, parcels in parcels_by_day.items():
        usable = [t for t in all_tiles if R.land_purchases_for(t) <= parcels]
        usable.sort(key=lambda t: (_steps(SPAWN, t), t))
        by_day[day] = usable
    return by_day


def _nearest_free(farm, usable):
    """A free tile ADJACENT to ground we already work, falling back to nearest-the-shed.

    Distance-from-shed alone lays tiles out in a ring, so a hand working five of them walks the
    circumference: day 0 cost 128 turns for 50 ops against his 101 total, and the packer paid for the
    difference by dropping four of his plantings. Tiles that touch each other share their walk -- a
    serpentine tour of five adjacent tiles is four steps, the same five spread around a ring is
    twelve.
    """
    worked = set(farm.crops) | set(farm.pens)
    best = None
    for t in usable:
        if not farm.free(t) or t in SHED:
            continue
        touching = sum(1 for w in worked
                       if abs(w[0] - t[0]) + abs(w[1] - t[1]) == 1)
        key = (-touching, _steps(SPAWN, t), t)
        if best is None or key < best[0]:
            best = (key, t)
    return best[1] if best else None


def _tasks_for_day(farm, day, plant_orders, build_orders, fertilize, replant=None):
    """Every op the farm wants today, anchored to a tile. `(tile, [op names], {item: qty})`.

    Cadences are his, counted off the tape rather than chosen:

        FEED 319, CARE 308, COLLECT_FERTILIZER 318   against ~343 animal-days  -> daily
        WATER 851 over ~61 tiles x 30 days                                     -> every other day
        HARVEST 338, not 607                                                   -> only when ready

    That last one is the expensive difference. HARVEST is a silent no-op when nothing is ready
    (`doable` requires `units > 0`), so emitting it daily costs a turn and reports nothing. We burned
    269 turns a season on it -- more than a hand's entire day -- while refusing his plantings.
    """
    tasks = []
    replant = collections.Counter(replant or {})

    # ---- the herd. Fed daily; an unfed animal produces nothing and eventually escapes.
    for tile, pen in sorted(farm.pens.items()):
        # A pen raised today is already covered by its build task -- `emit()` inserts it into
        # `farm.pens` before calling this, so without the guard the tile carries two entries on its
        # first day. 15 phantom tasks a season, and feeding twice buys nothing
        # (`kaggriculture.py:791`, `:798`).
        if pen["placed"] == day:
            continue
        ops = ["FEED", "CARE", "COLLECT_FERTILIZER"]
        age = day - pen["placed"]
        # Every third day, not every second. An animal accumulates produce up to `max_held` and a
        # HARVEST takes the lot, so visiting more often does not collect more -- it collects the same
        # units in smaller pieces and pays a turn each time. Counted against his tape, a two-day
        # cadence emitted 21 harvests on day 12 against his 8.
        if age >= 2 and age % 3 == 0:
            ops.append("HARVEST")
        tasks.append(dict(tile=tile, ops=ops, need={"WHEAT": 1}, kind="pen"))

    # ---- crops already in the ground
    for tile, c in sorted(farm.crops.items()):
        info = CROP[c["crop"]]
        age = day - c["planted"]
        ops = []
        # **Harvest and replant in the same visit**, which is what makes his board arithmetic work.
        # He plants 17 + 1 + 1 + 10 = 29 tiles by day 4 and NW holds 25, so tiles must be recycling:
        # wheat's window shuts at `max_day` 4, so his day-0 wheat clears exactly as his day-4 wave
        # goes in. Freeing the tile only at dusk -- which is what this planner did first -- left the
        # day-4 planting with nowhere to go and refused all ten, and the same for days 7, 14, 15 and
        # the whole 31-tile day-26 wave. The walk is already paid for by the harvest, so the replant
        # costs one turn instead of a fresh trip.
        if not info["ongoing"] and age >= info["max_day"] and replant.get(c["crop"]):
            replant[c["crop"]] -= 1
            tasks.append(dict(tile=tile, ops=["HARVEST", "DIG", "PLANT", "WATER"], need={},
                              kind="replant", crop=c["crop"], was=c["crop"]))
            continue
        # **A one-shot crop's yield IS its watering, so inside the window it is watered every day.**
        #
        # `ops.py`/`kaggriculture.py:373-386`: WATER on a NON-ongoing crop, inside
        # `[(max_yield_day + 1) // 2, max_yield_day]`, adds 1 to `yield_units` directly -- 2 if the
        # tile is fertilized -- capped at `max_yield`. And `_daily_refresh_plants` skips one-shot
        # crops outright (`kaggriculture.py:756-757`, `if not cd["ongoing"]: continue`), so every unit
        # such a tile ever produces came from a WATER op inside that window. Wheat's window is three
        # days wide; watering every other day collects two of the three, forever, on every wheat tile.
        #
        # Ongoing crops are the opposite: the nightly refresh grows them on a fixed interval whether
        # or not anyone watered, and watering only prevents the two-dry-day death and gates the
        # fertilizer doubling. Measured in `routines.py:708-771` -- melon daily $15,575 against
        # $11,167 on alternate days (-28%), strawberry the reverse at +52%. One rule for both crop
        # kinds was wrong for three of the five.
        in_window = (not info["ongoing"]
                     and (info["max_day"] + 1) // 2 <= age <= info["max_day"])
        if in_window or day - c["last_water"] >= 2:
            ops.append("WATER")
        if info["ongoing"]:
            # Produces on a fixed interval once mature; harvesting between intervals is a wasted turn.
            if age >= info["first"] and (day - c["last_harvest"]) >= 3:
                ops.append("HARVEST")
        else:
            # One-shot: the window shuts at `max_day` and the tile clears to EMPTY, freeing it.
            if age >= info["max_day"]:
                ops.append("HARVEST")
        need = {}
        # **Ongoing crops only, and sparingly.** Fertilizer doubles a watered tile's yield for two
        # days, so on a one-shot crop it buys one harvest and on an ongoing crop it buys every
        # harvest inside the window. Applying it everywhere every time it lapsed emitted 315 ops
        # against his 107 -- 208 turns a season the crew did not have, which the packer then paid for
        # by dropping his plantings. He fertilizes about twice per tile per season; so do we.
        if (fertilize and "WATER" in ops and info["ongoing"]
                and c["fert_until"] <= day - 4 and age >= info["first"] - 2):
            ops.append("FERTILIZE")
            need["FERTILIZER"] = 1
        if ops:
            # One dry day already banked: skip today's water and `_daily_refresh_plants` weeds it.
            thirsty = "WATER" in ops and (day - c["last_water"]) >= 2
            tasks.append(dict(tile=tile, ops=ops, need=need, kind="crop", _thirsty=thirsty))

    # ---- new pens: build, draw the animal at the shed, place it
    for tile, animal in build_orders:
        tasks.append(dict(tile=tile, ops=["BUILD_PASTURE", "PLACE", "FEED", "CARE"],
                          need={animal: 1, "WHEAT": 1}, kind="build", animal=animal))

    # ---- new plantings. Seeds are ordered at dawn and settle before the PLANT, per the atomic rule.
    # **DIG immediately before every PLANT.** A weed makes PLANT a silent no-op on that tile, and an
    # open-loop tape cannot see which tile the RNG weeded -- so the dig is insurance, not a response.
    # Measured on our own tape in the real environment with no dig at all: WEED 9 on day 3, 17 on day
    # 8, 20 on day 12, while PLANT fell 9 -> 2 -> 1 and the bank hit $8 and stayed there. The farm was
    # being eaten alive and every downstream census reported a farm nobody planned. One turn per
    # planting against a tile that is otherwise dead ground for the rest of the season.
    for tile, crop in plant_orders:
        # **No dig on virgin ground.** The board starts clean and weeds spawn during the season, so a
        # dig before a first planting is a turn spent on nothing: his day 0 emits 17 PLANT and zero
        # DIG, and the insurance version of this emitted 16 digs on day 0 alone against his 25 for the
        # whole season. The replant path above keeps its dig, because that tile has been standing
        # empty since its harvest and is exactly where `_spawn_weeds` puts them.
        tasks.append(dict(tile=tile, ops=["PLANT", "WATER"], need={}, kind="plant", crop=crop))

    # **Order is priority, because the packer drops the tail when a day will not fit.**
    # It was pens, then crops, then builds, then plantings -- so plantings were always the tail, and
    # 66 of his 131 were dropped while the same days ran fertilizer ops we invented. Ranked by what
    # is unrecoverable if it is skipped: a pen not built and a tile not planted are capacity the rest
    # of the season never gets, feeding keeps the herd alive, water stops a tile dying in two days,
    # and a harvest missed today is mostly still there tomorrow.
    # **A watering that is due is unrecoverable, so it ranks with the build.**
    # `_daily_refresh_plants` turns a tile that has missed two waterings into a WEED
    # (`kaggriculture.py:752-753`), and a WEED makes PLANT a silent no-op, so the ground is dead for
    # the season too. Our cadence fires at a gap of two, which means the tile is ALREADY one dry day
    # in -- dropping that single op kills it outright.
    #
    # Measured with `crop` ranked last, behind every pen upkeep visit: 16 crop tiles on day 5 became
    # 4 by day 7 and 1 by day 13, with WEED climbing 2 -> 13 -> 18. The farm never earned again. A
    # CARE visit skipped today can happen tomorrow; a tile left dry today is gone.
    RANK = {"build": 0, "plant": 1, "replant": 2, "pen": 3, "crop": 4}
    for t in tasks:
        t["_rank"] = RANK.get(t["kind"], 5)
        if t["kind"] == "crop" and t.get("_thirsty"):
            t["_rank"] = 0
    tasks.sort(key=lambda t: (t["_rank"], _steps(SPAWN, t["tile"])))
    return tasks


def _cost(task, pos):
    """Turns to reach `task` from `pos` and do it, including a draw made at the stop itself.

    A stop on a shed cell draws what it needs where it stands, and those PICKUPs are turns like any
    other. Leaving them out of the estimate let the packer accept a tour it could not finish, and
    `seq[:budget]` then silently cut the tail -- which showed up as WATER and DROP falling when
    PICKUP rose.
    """
    n = _steps(pos, task["tile"]) + len(task["ops"])
    if task["tile"] in SHED and task["need"]:
        n += len(task["need"])
    return n


def _can_leave(spawn, parcels):
    """Can a unit standing on `spawn` move off it at all, given the land the farm owns?

    `(5,5)` is SE and BOTH its neighbours -- `(4,5)` in SW and `(5,4)` in NE -- are locked until two
    and one parcels are bought. `ops.py:86` ignores a move onto LOCKED and the unit simply loses the
    turn, silently, so every task handed to it that day is emitted and lost.

    Measured: 17 PLANT ops emitted on day 0 and 12 landed, with 6 seeds left in store and every one
    of the 17 tiles unlocked NW ground. The tiles were fine; the hand could not get to them.

    `R.dawn_crew` now hires two per turn precisely so no hand ever wakes here, which should make this
    a guard rather than a filter. It stays because the failure it catches is invisible.
    """
    for dx, dy in ((0, -1), (0, 1), (1, 0), (-1, 0)):
        n = (spawn[0] + dx, spawn[1] + dy)
        if not (0 <= n[0] < R.BOARD_SIZE and 0 <= n[1] < R.BOARD_SIZE):
            continue
        if R.land_purchases_for(n) <= parcels:
            return True
    return False


def _assign(script, day, tasks, max_hands, units, parcels=0, animal_ready=0):
    """Pack today's tasks onto today's hands. Nearest-neighbour tours, cheapest hand first.

    This is the whole point of the module, so it is worth being explicit about what it does *not* do:
    it does not look at tomorrow. A hand is free every dawn (`_end_of_day` teleports every unit back
    to spawn), so there is nothing to carry forward except where a unit stands mid-day, and that only
    matters when two routines share a day -- which no longer happens, because there are no routines.
    """
    pending = list(tasks)
    done, used_units = [], []
    # **Take the crew first, THEN drop the units that cannot move.** Filtering before the slice let a
    # dropped unit shift the whole window up: a crew of five became slots `[0, 1, 2, 4, 5]`, and the
    # farm owns slots 0-4 on a four-hand day, so every op written to slot 5 was dropped by the harness
    # before the environment saw it -- 7 ops on day 0 including the PLANT that is the whole of
    # `plants day 1: 16 against the tape's 17`. A unit that cannot leave its spawn leaves the crew a
    # worker short; it does not entitle us to a hand we never hired.
    #
    # **And the spawn tile comes from the hire cadence, not from a table.** `R.dawn_crew` hires two per
    # turn, which pins every hand to `(5,4)` or `(4,5)` -- one step from the shed and never the trapped
    # `(5,5)` corner -- at the cost of the pair not existing until the turn after its HIRE settles.
    batches, spawn, ready = R.dawn_crew(max(0, max_hands - 1))
    usable_units = [u for u in units[:max_hands]
                    if u in spawn and _can_leave(spawn[u], parcels)]

    # **A hand cannot draw an animal before the animal is paid for** -- PLACE needs it in the unit's own
    # inventory, PICKUP takes it from the shed, and BUY_ANIMAL only settles at the END of its turn.
    # Holding the leading units until the day's last purchase settled was tried and REVERTED: it cost
    # more than it bought, because those are the same units that plant. Judged on the criterion rather
    # than on money, plants went from matching the tape day by day to 12 against 17 on day 1, pens 7 -> 6
    # and animals 6 -> 1 by day 10. `animal_ready` is threaded through and deliberately unused; the fix
    # has to be per TASK, not per unit-day, so a hand can plant early and fetch its beast afterwards.
    for unit in usable_units:
        if not pending:
            break
        script.hold(day, unit, ready[unit])
        # One step onto `(4,4)`, always. Every tour then starts from the shed, which is both what the
        # PICKUP gate needs and what keeps the next hire batch's occupancy predictable.
        arrival = [(m, None, None) for m in _walk(spawn[unit], SPAWN)]
        cap = script.turns_left(day, unit)
        budget = cap - len(arrival)
        if budget <= 0:
            continue
        pos = SPAWN
        seq, carried = list(arrival), collections.Counter()

        # Everything a hand will carry must be drawn in one trip to the shed, before it leaves: PICKUP
        # is gated on a shed-access tile that is *unlocked* (`ops.py:216`), and only `(4,4)` is always
        # both. A hand that skips this and picks up in the field emits FEED and FERTILIZE ops that are
        # refused for want of a carried unit -- silently, which is why `fertilize=1` and `fertilize=0`
        # once scored identically to the dollar.
        # **Nearest next task, inside the priority band.** Taking them in list order made a hand
        # cross the board between two adjacent jobs because one was a plant and one a water; picking
        # the cheapest reachable task at each step keeps the tour serpentine without giving up the
        # ranking, since the band is only widened once nothing in it fits. This is what buys back the
        # turns that were being spent walking and then charged to his dropped plantings.
        want = collections.Counter()
        take, spent = [], 0
        cursor = SPAWN
        while len(take) < 14:
            best = None
            for task in pending:
                if task in take:
                    continue
                # Only what must be carried AWAY from the shed needs the outward trip.
                projected = want + (collections.Counter(task["need"])
                                    if task["tile"] not in SHED else collections.Counter())
                # Already standing on the shed, so the outward trip is the draw itself and no walk.
                prefix = len(projected) if projected else 0
                add = _cost(task, cursor)
                if prefix + spent + add > budget:
                    continue
                # **Rank picks the hand's FIRST stop; distance picks every stop after it.**
                # Sorting every pick by `(rank, add)` dragged a hand across the board between two
                # adjacent tiles because one was a plant and one a water. On day 0, working the
                # tape's own tiles, that cost 73 walk turns against the tape's 53 -- 20 turns on a
                # 115-turn day, which is the whole reason a 106-turn day did not fit.
                # The band still decides what gets done when a day is short, because the first task
                # taken is the highest-ranked one that fits; it just stops steering the tour.
                key = (task["_rank"], add)
                if best is None or key < best[0]:
                    best = (key, task, projected, add)
            if best is None:
                break
            _key, task, projected, add = best
            take.append(task)
            want = projected
            spent += add
            cursor = task["tile"]
        if not take:
            continue

        # **Draw at the shed tile you are already standing on, not in one trip before you leave.**
        # PICKUP needs a shed-access tile, and the herd lives on those four cells -- so a hand doing
        # pen work is already somewhere it can draw, for free. Pre-batching every item into a single
        # trip out of `SPAWN` emitted 193 pickups a season against the tape's 339, and paid a walk for
        # the ones it did emit. Only what is needed AWAY from the shed has to be carried out.
        away = collections.Counter()
        for task in take:
            if task["tile"] not in SHED:
                away.update(task["need"])
        if away:
            for m in _walk(pos, SPAWN):
                seq.append((m, None, None))
            pos = SPAWN
            for item, qty in sorted(away.items()):
                seq.append(("PICKUP", item, qty))
                carried[item] += qty

        # Nearest-neighbour from where the hand now stands. The tour is short (rarely over eight
        # stops) so the greedy order is within a step or two of optimal and costs nothing to compute.
        for nxt in take:
            for m in _walk(pos, nxt["tile"]):
                seq.append((m, None, None))
            # Standing on a shed cell, draw what this stop needs right here.
            if nxt["tile"] in SHED and nxt["need"]:
                for item, qty in sorted(nxt["need"].items()):
                    seq.append(("PICKUP", item, qty))
            pos = nxt["tile"]
            for name in nxt["ops"]:
                crop = nxt.get("crop") if name == "PLANT" else None
                item = nxt.get("animal") if name == "PLACE" else None
                seq.append((name, item, crop))
            done.append(nxt)
            pending.remove(nxt)

        # **Walk back to the shed and DROP when the hand is carrying produce.** DROP tests
        # shed-adjacency, so a hand that finishes out in a field cannot use it and its harvest sits in
        # `carried` until the dusk auto-deposit -- which means it cannot be SOLD until the next dawn.
        # Requiring the tour to happen to end on a shed tile emitted 8 drops a season against the
        # tape's 80. The walk is only worth it if the turns are there, so it is attempted and skipped
        # rather than forced.
        if any("HARVEST" in t["ops"] or "COLLECT_FERTILIZER" in t["ops"] for t in take):
            home = min(SHED, key=lambda c: _steps(pos, c))
            back = _walk(pos, home)
            if len(seq) + len(back) + 1 <= cap:
                for m in back:
                    seq.append((m, None, None))
                pos = home
                seq.append(("DROP", None, None))

        seq = seq[:cap]
        t0 = script.claim(day, unit, len(seq), what=f"day {day} tour")
        for i, (name, item, crop) in enumerate(seq):
            if name == "PICKUP":
                script.op(t0 + i, unit, "PICKUP", item=item, qty=crop or 1)
            elif name == "PLACE":
                script.op(t0 + i, unit, "PLACE", item=item, qty=1)
            else:
                script.op(t0 + i, unit, name, crop=crop)
        script.stand(day, unit, pos)
        used_units.append(unit)
    return done, pending, used_units


def emit(schedule, fertilize=True, sell=True, crop_for=None, placements=None):
    """Schedule -> tape.

    `schedule` is `data/seed_scripts/new_leader/schedule.json`: per day, how many pens are built,
    which crops are planted, whether a parcel is bought, and how many hands ran.

    `placements`, when given, is the tile-level form from `scripts/extract_tape.py`:
    `{day: {"plants": [(tile, crop), ...], "builds": [(tile, animal), ...]}}`. That is what makes
    extract and emit **inverses**. A tape cell is `["PLANT","MELON"]` with no coordinate -- the op
    acts on whatever tile the unit stands on -- so a schedule that keeps only a bag of crops per day
    forces this function to re-invent the placement, and an invention cannot round-trip. With the
    tiles supplied, `tape -> schedule -> tape` is a fair test of the emitter and nothing else.
    """
    # The schedule carries tiles when it has them (`plant_tiles` / `build_tiles`, written by
    # `scripts/extract_leader_schedule.py`), because a tape cell has no coordinate and re-inventing
    # the placement is measurably worse: $11,638 with the tape's tiles against $6,794 with ours, 2
    # refusals against 17, and one run in three banking $2. An explicit `placements` argument still
    # wins, so a search can override.
    if placements is None:
        from_schedule = {}
        for day, row in schedule.items():
            pl = [(tuple(t), c) for t, c in (row.get("plant_tiles") or [])]
            bl = [(tuple(t), a) for t, a in (row.get("build_tiles") or [])]
            if pl or bl:
                from_schedule[day] = dict(plants=pl, builds=bl)
        placements = from_schedule
    placements = placements or {}
    script = R.Script()
    farm = Farm()
    refused, report_days = [], []

    days = sorted(schedule)
    land_days = [d for d in days if schedule[d]["land"]]
    # **A parcel bought at dusk is not ground you can work that day.** LAND_PRICES is [1000, 2000, 4000]
    # and the tape buys the second one at day 10 **hour 20**, after a whole day of selling has taken it
    # to $4,051 -- so treating it as owned from that dawn routes twenty days of hands into SW across a
    # border that is still locked. `land_turns` carries the hour off the tape; anything past hour 2 only
    # counts from the following day.
    def _land_ready(d):
        turns = schedule[d].get("land_turns") or ([1] * int(schedule[d]["land"]))
        return sum(1 for h in turns if h <= 2)

    parcels_by_day = {}
    for d in range(R.SEASON_DAYS):
        parcels_by_day[d] = (sum(int(schedule[L]["land"]) for L in land_days if L < d)
                             + (_land_ready(d) if d in land_days else 0))
    board = _board(parcels_by_day)

    # **BUY_LAND gets a turn to itself.** `build_script_submission.py:90` appends it LAST and then
    # truncates the turn at `maxMarketOrdersPerTurn` = 10, so on a day that hires eight hands and
    # buys seed it falls off the end -- silently. Measured: the farm held ONE quadrant for the whole
    # season while carrying $1,494 on day 7 against a $1,000 parcel, so the tape's day-8 pens in NE
    # had nowhere to stand and the herd stalled at 8 against 14.
    # **At the hour the tape bought it.** Turn 1 bought the $1,000 parcel and silently lost the $2,000
    # one, because on day 10 the bank does not reach $2,000 until hour 20 -- the tape sells all day and
    # buys last. Ordering early is not conservative here; it is the difference between owning SW and
    # routing into it for twenty days.
    # **If the schedule carries the tape's own book, place it order for order at the recorded turn.**
    # Aggregating to a day total and re-inventing the lots loses the structure the market is priced on:
    # `market_price` quotes a BUY_PRODUCT at post-buy inventory, so a SELL and a BUY of one product in
    # the SAME turn net about zero, and the tape uses that all season to move wheat from the town into
    # the shed for free. Six equal buys and six equal sells on alternating turns pays the spread instead:
    # day 2 came to -$89 against the tape's +$76 on identical daily totals, and that $165 is where the
    # whole cash divergence starts -- day 3 opens $45 against $217, and a short bank silently kills
    # BUY_ANIMAL, which is why 11 pens ever held 5 animals.
    #
    # HIRE is the one exclusion. Its cost is the Fibonacci partial sum over the day and does not depend
    # on which turn each order sits in, while our two-per-turn cadence IS load-bearing -- `_spawn_hand`
    # picks by occupancy at settle time, so a third order in one turn puts a hand on the trapped `(5,5)`
    # corner and dead reckoning stops working.
    # **OFF, and this is not a silent disable -- it is a measured regression on the criterion.** The book
    # is right about the money: emitting it verbatim took day 3 from $45 to $196 against the tape's $217
    # and days 0-3 from a $172 gap to $21. It is wrong about the herd. The tape buys its day-0 animals at
    # hours 0-3, our tours draw from the shed at hour 1, and BUY_ANIMAL only settles at the END of its
    # turn -- so two of the four PLACEs no-op and day 1 holds 2 animals against the tape's 4. Animals
    # compound; cash on day 3 does not. Day-by-day state went 5 fail/2 pass to 6 fail/1 pass.
    #
    # Holding the leading units until the last purchase settles was tried and is also worse: those are
    # the units that plant, and 12 lost turns on day 0 took plants from matching to 12 against 17.
    #
    # The fix is per TASK, not per unit-day: an animal's PICKUP has to sit after its purchase turn while
    # the same hand still plants early -- which means the tour must be able to return to the shed
    # mid-day instead of drawing everything in one trip before it leaves. Until that exists this stays
    # off, `tests/test_the_market_book_is_the_tapes_turn_by_turn.py` stays red, and the $165 a day the
    # invented lot structure costs is a known open item rather than a forgotten one.
    USE_TAPE_BOOK = False
    book = {d: [o for o in (schedule[d].get("orders") or []) if o[1] != "HIRE"] for d in days}
    have_book = USE_TAPE_BOOK and any(book.values())
    if have_book:
        cols = {"SELL": (script.sell, R.PRODUCTS),
                "BUY_SEED": (script.buy_seed, R.CROPS),
                "BUY_PRODUCT": (script.buy_product, R.PRODUCTS),
                "BUY_ANIMAL": (script.buy_animal, R.ANIMAL_NAMES)}
        for d, orders in book.items():
            for hour, op, item, qty in orders:
                t = d * TPD + int(hour)
                if t >= script.T:
                    continue
                if op == "BUY_LAND":
                    script.buy_land[t] += int(qty)
                elif op in cols:
                    arr, names = cols[op]
                    if item in names:
                        arr[t, names.index(item)] += int(qty)
    else:
        for d in land_days:
            for h in (schedule[d].get("land_turns") or [1]):
                t = d * TPD + int(h)
                if t < script.T:
                    script.buy_land[t] += 1

    # **Ascending unit id, not nearest-the-shed.** `build_plan` maps unit 0 to the farmer and units
    # 1.. to the hands, so using unit k at all requires k hires -- and the ladder is the Fibonacci
    # partial sum, reset every dawn. Picking a unit because it spawns near the shed bought every rung
    # below it for the whole season: unit 9 is $88/day where unit 4 is $7. Distance is worth one turn
    # of walking; the index is worth the crew bill.
    unit_order = list(range(R.U_DEFAULT))

    for day in range(R.SEASON_DAYS):
        row = schedule.get(day, {})
        farm.parcels = parcels_by_day.get(day, 0)
        usable = board.get(day, [])

        # ---- ground for what the schedule asks for today
        build_orders, restock = [], []
        n_build = row.get("builds", 0)
        places = row.get("places") or []
        # `if want_builds:` and not `is not None` -- a day carrying plant tiles but no build tiles
        # gets an empty list, and treating that as "build nothing today" silently overrode the
        # schedule's own build count. Pens stopped being raised and the farm banked $11.
        want_builds = (placements.get(day) or {}).get("builds") or None
        if want_builds:
            n_build = len(want_builds)
        for i in range(n_build):
            animal = places[i] if i < len(places) else "COW"
            if animal not in R.ANIMAL_NAMES:
                animal = "COW"
            # The herd wants shed-access ground: it draws wheat every day and DROPs its produce, and
            # both ops test shed-adjacency. Failing that, as near the shed as the board allows.
            if want_builds is not None:
                spot, animal = tuple(want_builds[i][0]), want_builds[i][1] or animal
                # **A PLACE onto a tile that already holds a pen is a RESTOCK, not a build.**
                # The tape's day-10 `build_tiles` names (4,4), which has held a pen since day 0 -- it
                # is putting a fresh animal into a structure whose occupant escaped
                # (`kaggriculture.py:786`: two consecutive unfed days and the animal is gone, the
                # structure stays). Treating it as a build overwrote our own pen record and lost the
                # slot, which is why the herd stalled at 8 against the tape's 14 from day 9.
                if spot in farm.pens:
                    farm.pens[spot] = dict(animal=animal, placed=day, last_feed=day)
                    restock.append((spot, animal))
                    continue
            else:
                # **Only shed cells the farm actually owns.** `shed_access_tiles()` is the ring round
                # the shed -- the only cells where PICKUP, DROP and a shed PLACE work -- and the herd
                # wants them because it draws wheat every day. But the quadrant split puts three of
                # the four in land that starts LOCKED: (5,4) needs 1 parcel, (4,5) needs 2, (5,5)
                # needs 3. Only (4,4) is legal on day 0.
                #
                # Reaching for them in order without checking built three of the four day-0 pens on
                # ground we did not own, so BUILD_PASTURE, PLACE, FEED and CARE all silently no-oped
                # while the animals had already been paid for. The farm held 2 pens on day 1 against
                # the tape's 4 and never caught up -- 5 by day 29 against 14. Nothing raised: the
                # move onto LOCKED is ignored (`ops.py:86`) and `_apply_unit_action` bails before it
                # reaches the op.
                spot = next((t for t in R.shed_access_tiles()
                             if farm.free(t) and R.land_purchases_for(t) <= farm.parcels), None)
                spot = spot or next((t for t in usable if farm.free(t)), None)
            if spot is None:
                refused.append(f"day {day}: no ground for a pen")
                continue
            farm.pens[spot] = dict(animal=animal, placed=day, last_feed=day)
            build_orders.append((spot, animal))

        # A tile whose one-shot crop clears today is ground the schedule can plant on today, and it
        # has to be counted *before* the fresh-ground search or the wave is refused on a board that
        # is about to empty. This is the whole of his day-4, day-14, day-15 and day-26 arithmetic.
        clearing = collections.Counter(
            c["crop"] for c in farm.crops.values()
            if not CROP[c["crop"]]["ongoing"] and day - c["planted"] >= CROP[c["crop"]]["max_day"])
        replant = collections.Counter()

        replant_here = []
        want_plants = (placements.get(day) or {}).get("plants") or None
        wanted = ([(tuple(t), c) for t, c in want_plants] if want_plants is not None
                  else [(None, c) for c in (row.get("plants") or [])])

        plant_orders = []
        for fixed_tile, crop in wanted:
            if crop not in CROP:
                continue
            if fixed_tile is not None:
                # The tape says this tile, and it REPLANTS -- (4,1) is wheat on day 0 and strawberry
                # on day 4, 131 plantings over 64 tiles. A tile that still holds a crop has to be
                # harvested before it can be planted, in the same visit: dropping the old crop from
                # our model and emitting a bare PLANT left the tile occupied in the game, so the
                # PLANT was refused and the ground stayed dead. Measured: 18 live tiles on day 4
                # collapsing to 9 by day 6 while the tape held 18.
                if not farm.free(fixed_tile) and fixed_tile in farm.crops:
                    old = farm.crops.pop(fixed_tile)
                    replant_here.append((fixed_tile, crop))
                    script.buy_seed  # seeds come off the schedule; nothing to order here
                    continue
                spot = fixed_tile
            else:
                spot = _nearest_free(farm, usable)
            if spot is None:
                # Nothing free -- take a tile that clears today and replant it in the same visit.
                pick = next((k for k in clearing if clearing[k] > 0), None)
                if pick is not None:
                    clearing[pick] -= 1
                    replant[pick] += 1
                    continue
                refused.append(f"day {day}: no ground for a {crop} planting")
                continue
            farm.crops[spot] = dict(crop=crop, planted=day, last_water=day,
                                    last_harvest=day, fert_until=-1)
            plant_orders.append((spot, crop))

        # Seeds come off the schedule like every other market order. Counting one per planting we
        # managed to place under-ordered by 23 across the season, because the tape buys seed for the
        # plantings it intends, not for the ones a packer found room for.
        # **On a land day, spend nothing until the parcel is paid for.** `_do_buy_land` returns silently
        # when the bank is short, and the day's seed at turn 0 took $452 off a $1,239 dawn -- so a
        # $1,000 parcel was ordered against $787 and both of the season's purchases vanished without a
        # word. The tape buys its seed at hour 3, after the parcel at hour 2. `spend_turn` is 0 on every
        # other day, so nothing else moves.
        spend_turn = 3 if any(h <= 2 for h in (row.get("land_turns") or [])) else 0
        if not have_book:
            for crop, qty in (row.get("seeds") or {}).items():
                if crop in R.CROPS:
                    t = min(day * TPD + spend_turn, script.T - 1)
                    script.buy_seed[t, R.CROPS.index(crop)] += int(qty)

        tasks = _tasks_for_day(farm, day, plant_orders, build_orders, fertilize, replant)
        # Restocked pens: the structure already stands, so it is PICKUP, PLACE, FEED, CARE with no
        # BUILD. Ranked with the builds, because an empty pen earns nothing until it is filled.
        for tile, animal in restock:
            tasks.append(dict(tile=tile, ops=["PLACE", "FEED", "CARE"],
                              need={animal: 1, "WHEAT": 1}, kind="build", animal=animal, _rank=0))
        # Tiles the tape replants today: harvest the standing crop and sow the new one in one visit.
        for tile, crop in replant_here:
            tasks.append(dict(tile=tile, ops=["HARVEST", "DIG", "PLANT", "WATER"], need={},
                              kind="replant", crop=crop, _rank=2))
            farm.crops[tile] = dict(crop=crop, planted=day, last_water=day,
                                    last_harvest=day, fert_until=-1)

        # ---- the crew. His, not ours: the ladder resets every dawn and is Fibonacci, so hiring the
        # peak from day 0 costs more than the farm earns. `hire` is the count wanted that turn.
        want_turns = 0
        pos = SPAWN
        for t in tasks:
            want_turns += _cost(t, pos)
            pos = t["tile"]
        # `row["hands"]` counts his HANDS; the farmer works too, so his crew is one larger and so is
        # the unit budget. Reading it as the unit count cost us a whole worker every day of the
        # season -- 4 units on day 0 against his 5 -- while the packer dropped his plantings for want
        # of turns.
        # **Take the crew from the schedule, not from our own estimate of the work.**
        # `want_turns` is what OUR task generator asked for, and it under-generates: on day 7 it
        # wanted 9 waterings where the tape did 27. Deriving the crew from it closed a loop --
        # under-generate work, conclude fewer hands are needed, do less work, starve. Measured
        # against the tape on days 4-7 it ran 2-3 hands where the tape ran 6-8, and the bank went
        # from ahead on day 3 to 5% of the tape's by day 7 and never recovered.
        #
        # The schedule's hand count is a fact off the tape. Use it.
        workers = max(1, (row.get("hands", 0) or 0) + 1)

        # **Spread across the day, one animal a turn.** `_process_market` truncates each turn's
        # queue to `maxMarketOrdersPerTurn` = 10 (`reference/kaggriculture.py:534`) and drops the rest
        # silently, so a turn-0 dump of every seed, animal, wheat order and hire loses whatever falls
        # past the tenth slot. His day 0 issues 39 orders across 23 turns, buying animals one at a
        # time on turns 1-4 and wheat in 2-6 unit lots all day, interleaved with sells that fund the
        # next buy. Ours issued nine orders on turn 0 and nothing afterwards.
        # Everything below is READ off the schedule rather than invented. The schedule is the tape's
        # own market book -- what it bought, what it sold, how much and on which day -- and inventing
        # a substitute for it was the largest single divergence in the A/B diff: 320 units of SELL a
        # day against the tape's 17-55, and a third of its wheat.
        # **Animals are bought at dawn, before any hand tries to draw one.**
        # Spreading them across turns 1-4 the way the tape does looks faithful, but our hands PICKUP
        # theirs on turn 1 -- so the draw happened before the purchase and the PLACE silently no-oped.
        # Measured: 4 pens standing with 2 animals in them, and the farm never recovered.
        # The season total is unchanged, only the turn, so market fidelity is untouched.
        if not have_book:
            for a, qty in (row.get("animals_bought") or {}).items():
                if a in R.ANIMAL_NAMES and day * TPD < script.T:
                    t = min(day * TPD + spend_turn, script.T - 1)
                    script.buy_animal[t, R.ANIMAL_NAMES.index(a)] += int(qty)

        # The turn after the day's last BUY_ANIMAL settles. 0 on a day that buys none.
        animal_ready = max((int(h) + 1 for h, op, _i, _q in (row.get("orders") or [])
                            if op == "BUY_ANIMAL"), default=0)
        done, left, used = _assign(script, day, tasks, workers, unit_order,
                                   parcels=parcels_by_day.get(day, 0),
                                   animal_ready=animal_ready)

        # **Hire what the day actually used, not what it wanted.** The ladder is Fibonacci and resets
        # every dawn, so an unused hand is not free -- it is the most expensive rung of that day's
        # partial sum. Setting `hire` from the packer's result rather than from the estimate is what
        # keeps a quiet day at two hands instead of the six the turn-count guessed at.
        # Hire the highest HAND index touched, not a count: unit 0 is the farmer and costs nothing,
        # unit k is hand k and needs k hires. Counting units instead over-hired by one every day.
        # **One turn, not the whole day.** `hire[t]` is a COUNT of HIRE orders at turn `t`
        # (`build_script_submission.py:89`), and `_do_hire` walks the Fibonacci ladder once per order
        # within a day. Writing the crew size into all 24 turns emitted 96 hires on day 0 instead of
        # 4, climbing the ladder inside the day, and drained $3,000 to $76 before the farm existed --
        # the tape banked exactly $0 with an empty crew and an empty herd all season.
        #
        # It has to be re-issued EVERY dawn because `_end_of_day` does `farm["hands"] = []`
        # (`reference/kaggriculture.py:849`): the hands are dismissed nightly and the ladder resets,
        # which is why a crew of 12 costs its whole partial sum ($376) every single day.
        # **The schedule records the hires, so issue them.** Deriving the crew from `used` -- the
        # units our own packer happened to fill -- ran 2-3 hands on days 4-7 where the tape ran 6-8,
        # because our task generator under-generates and the crew was being sized from it. That closes
        # a loop: fewer hands, less work done, fewer hands next time.
        # **Two per turn, spread over the first turns of the day, not the whole crew at dawn.**
        # `_spawn_hand` picks the min-occupancy shed-access tile at the moment the HIRE settles, so a
        # crew hired in one turn puts hand 3 on `(5,5)` -- SE, both neighbours locked, unable to move at
        # all -- and every hand after it on a tile our dead reckoning does not predict. That is where 76
        # of 126 PLANT ops were being lost. `R.dawn_crew` chose the same batching to compute `spawn` and
        # `ready` above; this writes the orders that make it true. It matches the tape's own cadence,
        # `[(1, 2), (2, 2), (3, 2)]`, and it also keeps HIRE clear of the 10-slot market cap at turn 0.
        need = int(row.get("hires", 0) or 0) or (max(used) if used else 0)
        for turn, n in R.dawn_crew(need)[0]:
            t = day * TPD + turn
            if t < script.T:
                script.hire[t] = max(int(script.hire[t]), n)
        if left:
            refused.append(f"day {day}: {len(left)} of {len(tasks)} tasks unassigned "
                           f"({workers} workers, {want_turns} turns of work)")

        # ---- book-keeping so tomorrow knows what happened, including tiles that cleared
        wheat_needed = sum(t["need"].get("WHEAT", 0) for t in done)
        fert_needed = sum(t["need"].get("FERTILIZER", 0) for t in done)
        # The schedule's figure REPLACES our estimate rather than bounding it. Taking the larger of
        # the two over-bought 135 units of wheat across the season, which is cash spent on feed the
        # tape did not buy and produce the shed then has to hold.
        # Unconditional, including the days the schedule buys nothing. Applying it only where the
        # schedule happened to list a product left our own estimate firing everywhere else, which is
        # where the remaining 135 units of over-bought wheat were coming from.
        buys = row.get("buys") or {}
        wheat_needed = int(buys.get("WHEAT", 0))
        fert_needed = int(buys.get("FERTILIZER", 0))
        if have_book:
            wheat_needed = fert_needed = 0
        if wheat_needed:
            # In lots across the day rather than one block, for the slot cap above and because the
            # ask walks up with the town's inventory as a single large order eats through it.
            w = R.PRODUCTS.index("WHEAT")
            per = max(1, math.ceil(wheat_needed / 6))
            left = wheat_needed
            for k in range(6):
                if left <= 0:
                    break
                slot = day * TPD + spend_turn + 2 + k * 3   # turn 1 is reserved for BUY_LAND
                if slot < script.T:
                    script.buy_product[slot, w] += min(per, left)
                left -= per
        for t in done:
            tile = t["tile"]
            if t["kind"] == "crop":
                c = farm.crops.get(tile)
                if c is None:
                    continue
                if "WATER" in t["ops"]:
                    c["last_water"] = day
                if "FERTILIZE" in t["ops"]:
                    c["fert_until"] = day + 2
                if "HARVEST" in t["ops"]:
                    c["last_harvest"] = day
                    if not CROP[c["crop"]]["ongoing"]:
                        # Cleared to EMPTY tonight, so the tile is free for his next wave. This is
                        # the line that makes 131 plantings on ~61 tiles expressible at all.
                        del farm.crops[tile]
            elif t["kind"] == "replant":
                c = farm.crops.get(tile)
                if c is not None:
                    c.update(planted=day, last_water=day, last_harvest=day, fert_until=-1)
            elif t["kind"] == "pen":
                farm.pens[tile]["last_feed"] = day
        if fert_needed:
            slot = min(day * TPD + spend_turn + 2, script.T - 1)
            script.buy_product[slot, R.PRODUCTS.index("FERTILIZER")] += fert_needed

        report_days.append(dict(day=day, hands=need, workers=workers, tasks=len(tasks),
                                done=len(done),
                                turns=want_turns, pens=len(farm.pens), crops=len(farm.crops)))

    if sell and not have_book:
        _sell_from_schedule(script, schedule)

    return script, dict(refused=refused, days=report_days,
                        pens=len(farm.pens), crops=len(farm.crops))


def _sell_from_schedule(script, schedule):
    """Sell exactly what the schedule records, on the day it records it.

    The invented version ordered 8 products x 40 units every day -- 320 against the tape's 17-55 --
    and no lot size fixed it, because the shape was wrong and not the scale. The tape sells small
    amounts of whatever it happens to hold, all season, with one 358-unit dump on day 12. That is not
    a cadence to be guessed at; it is written down.
    """
    for day, row in schedule.items():
        for prod, qty in (row.get("sells") or {}).items():
            if prod not in R.PRODUCTS:
                continue
            qty = int(qty)
            i = R.PRODUCTS.index(prod)
            # Spread across the day so a busy market day cannot run past the ten-order cap.
            lots = max(1, min(6, qty))
            per, left = qty // lots, qty
            for k in range(lots):
                # **From turn 0, so the proceeds are in the bank before anything spends them.**
                # Starting at turn 2 put the day's seed and livestock buys ahead of its sales, and
                # `_do_buy_land` returns silently on a short bank: the farm held NW and nothing else for
                # all thirty days while ordering two parcels it could not pay for. The tape's day 7
                # sells at hours 0 and 1, buys the parcel at hour 2 and its seed at hour 3.
                t = day * TPD + k * 3
                n = per if k < lots - 1 else left
                if t < script.T and n > 0:
                    script.sell[t, i] += n
                left -= per


def _sell_everything(script, schedule):
    """Sell each product daily from the day it can first exist.

    His cadence is not this -- he spaces sales against the price curve and dumps 358 units on day 12
    -- and that is a separate, later question. This exists so the tape banks its produce at all
    rather than letting it sit in the shed, and it is deliberately the crudest thing that does that.
    """
    # One product per turn, late in the day. Eight SELL orders in the same turn as the day's buys
    # ran past the ten-slot cap and most of them were discarded before they were ever quoted -- and a
    # buy issued in that same turn quotes against a book the dropped sells never lifted.
    # **Small daily lots, not a standing 40 of everything.** The flat version ordered 320 units of
    # SELL every day against the tape's 17-55, and an order that large is not free even when the shed
    # cannot fill it: the town's posted price walks down as its inventory rises, so dumping a whole
    # day's produce in one order sells the tail of it into a market our own first units just spoiled.
    # The tape sells in small lots all season and saves its one big dump for day 12.
    products = ("WHEAT", "STRAWBERRY", "MELON", "MILK", "WOOL", "FERTILIZER", "CARROT", "TOMATO")
    for day in range(1, R.SEASON_DAYS):
        for i, p in enumerate(products):
            t = day * TPD + 2 + i * 2
            if t < script.T:
                script.sell[t, R.PRODUCTS.index(p)] += 8
