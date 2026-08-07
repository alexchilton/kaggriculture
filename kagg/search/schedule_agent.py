"""A schedule-driven agent that reads the board every turn. No emitter, no dead reckoning, no model.

`dayplan.emit` renders a schedule to a 720-turn tape by **predicting** the state it will act on, and that
prediction is where the season goes. Measured against the tape's own schedule -- ops EMITTED against ops
that actually LANDED:

                        ours emit/land    tape emit/land
    CARE                     312 / 150         308 / 308
    FEED                     312 / 142         319 / 319
    WATER                    766 / 455         851 / 846
    COLLECT_FERTILIZER       297 / 143         318 / 318
    HARVEST                  286 / 149         338 / 337

48% against ~100%. Eight separate silent bugs were fixed in a single day -- a hand waking on the locked
`(5,5)` corner, ops written to an unhired slot, a tour truncated past the end of the day, two parcels
ordered against a bank the day's own purchases had already spent, animals drawn from a shed before the
purchase settled -- and every one is the same bug: **emitting an op without checking the state it lands
in.**

The environment hands that state over for free, every turn:

    obs["farms"][me]["tiles"]     the board, with `watered_today`, `yield_units`, `fed_today`,
                                 `cared_today`, `fertilizer_available`, `consecutive_unwatered`
    obs["farms"][me]["farmer"]    where the farmer stands -- no dead reckoning
    obs["farms"][me]["hands"]     every hand, so an op cannot go to a unit we do not own
    obs["farms"][me]["money"]     so a purchase is never ordered against a bank that cannot pay
    obs["private"]["shed"]        so an animal is never drawn from an empty shed
    obs["private"]["seeds"]       so PLANT is never blocked by the atomic-seed rule

So this agent plans no tour. Each turn each unit either performs its op or takes one step towards it, and
next turn the board is read again. The whole failure class becomes unrepresentable rather than fixable one
bug at a time.

The schedule stays thin -- counts per day, no tile coordinates -- because that is what our own optimiser
can produce. `scripts/build_schedule.py` generates it; `scripts/schedule_ladder.py` scores it.
"""

import collections

from . import router as RT
from . import routines as R

TPD = R.TURNS_PER_DAY
SHED = set(R.shed_access_tiles())
SPAWN = tuple(R.SPAWN)
STEP = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
CROP = R.CROP_TABLE

#: `shedCapacity`, the env default. DROP does not clamp -- it `del`s every item after taking whatever
#: fits (`kaggriculture.py:333`), so dropping into a full shed destroys the load rather than refusing.
SHED_CAPACITY = 100

#: Days of feed to hold per animal. 1 is the consumption rate and leaves no slack; the tape carries
#: over two. Also the multiplier the sell guard protects, so raising it withholds more wheat from sale.
FEED_DAYS = 2

#: **TRIED and REVERTED: cap one BUY_PRODUCT to 4 so the day's feed is metered across the hours.**
#: The motivating measurement is real -- the leader places sixteen WHEAT buys of 1-6 across h1-h22 on
#: day 0 against our single block, and `market_price` moves with every unit -- but a ceiling per order
#: cannot fund a large herd. Seb runs 19 animals, which is 38 wheat a day at `FEED_DAYS = 2`, and the
#: herd starved out from day 15. Animals in pens, seed 11, Seb's schedule, day 16 onward:
#:
#:     cap = 4     7  8  8  8  8 ... 8
#:     no cap     17 17 17 17 17 ... 17
#:
#: Meter by placing MORE orders, never by shrinking the one order that feeds the herd.
FEED_ORDER_CAP = None

#: Most WHEAT bought in one order. **This is a cadence control, not the cap `FEED_ORDER_CAP` was.**
#: That one bounded the DAY's feed and starved a 19-animal herd; this bounds a single order while the
#: day's target is re-offered every turn, so the herd still gets everything it needs -- just spread.
#: `market_price` moves per unit inside one order and the shops restock every 4 steps, so eight orders
#: of 1 clear cheaper than one of 8. The tape buys 1 at a time, eight times, across hours 5-19.
BUY_DRIP = 1

#: Floor for the opportunistic mid-tour drop below. A unit standing at a depot mid-tour re-checks this
#: every time it is about to walk away, and pens sit ON depot tiles, so with no floor a unit banking
#: one or two units at a time turns every such moment into a 1-turn DROP.
MIN_OPPORTUNISTIC_DROP = 4

#: Whether the opportunistic mid-tour DROP below runs at all. A flag rather than an edit because it
#: was measured on final bank (-$8,292 over twelve seeds) and re-applied here without being measured
#: again on the day-by-day trace -- so it must be switchable to be attributable.
OPPORTUNISTIC_DROP = True

#: Whether `sells` is read as a CUMULATIVE target (a missed row is retried until it is filled) or as
#: the old per-day row (a row that landed on an empty shed is forfeited). Switchable for the same
#: reason as the flag above: it must be attributable on the day-by-day trace, not on a final bank.
CUMULATIVE_SELLS = True

#: Whether the crew is bought BEFORE the day's goods, and limited by where the next hand would land
#: rather than by a flat two-a-turn. Off restores the old behaviour exactly. Switchable for the same
#: reason as the flags above: it has to be attributable on the day-by-day trace, not on a final bank.
#:
#: Measured on Seb's tape, seed 11, by `scripts/when_the_crew_arrives.py`. He issues every HIRE at
#: hour 0; we dribble two an hour across hours 0-3 and append them LAST, after SELL, LAND, ANIMAL,
#: SEED and FEED have already spent the bank. Two costs, and they are independent:
#:
#:     ordering   day 6 we open on $711, want 8 hands, and go (0,$711) (0,$711) (1,$10) (1,$10)
#:                (2,$5) (2,$5) (3,$0) (3,$0) -- the bank is gone by hour 1, spent on seed and feed
#:                between our second hire and our third, so six of eight HIREs fail and the day is
#:                worked by five hands. `_hire_cost` is `mult * fib(hires_today)` and `hires_today`
#:                is a per-DAY counter, so the crew costs the same whenever it is bought. Dribbling
#:                saves nothing and lets a later order empty the bank first.
#:     the cap    two-a-turn is a proxy for a real trap: with the farmer on `(4,4)` the third hire of
#:                a turn lands on `(5,5)`, whose only neighbours `(4,5)` and `(5,4)` are LOCKED while
#:                we own NW alone, so it cannot move all day. But `LAND_ORDER = ["NE", "SW", "SE"]`
#:                unlocks `(5,4)` -- that hand's escape square -- with the FIRST parcel, and the cap
#:                then costs 12, 73, 12, 35 and 26 hand-turns on days 5-8 and 10 for nothing.
#:
#: A hand hired at hour 0 works 23 turns; the same hand at hour 4 works 19. Nothing downstream
#: recovers a turn that was never available, which is why this sits ahead of every routing question.
HIRE_FIRST = True

#: Ops whose VALUE decays with the hour they are served, so the work appearing is itself a reason to
#: replan. Empty disables the trigger and restores the old crew-change-or-idle rule exactly.
#:
#: PLACE is the whole list because what follows it is time-critical: an animal must be fed and cared
#: for on the day it lands, and a FEED costs a shed round trip of about eight turns against a budget
#: of `24 - hour - 1`. Placed at hour 18 it simply cannot be served. Nothing else on the board works
#: that way -- a melon watered at hour 3 or hour 20 yields the same melon.
#
# **Re-enabled 2026-08-07, and the reason it was off has expired.** It measured NET NEGATIVE once
# hiring was fixed -- 42 cells against 39 -- back when `build_nodes` offered a full-prize PLACE at
# every empty pen regardless of how many animals were in the shed. An urgent replan on a phantom node
# is an urgent replan onto nothing, so of course forcing more of them lost. `RT.SUPPLY_LEDGER` now
# retires the duplicates the moment one unit claims the animal, so the trigger fires on real work.
#
# Measured on Seb's tape, seed 11, day 4: the cow reaches the shed at hour 2 and `plan_routes` is not
# called again until a unit falls idle at hour 10, by which point the budget is 13 and the far pen at
# (0,3) plus the walk home no longer fits. It sits in the shed to hour 23. The tape picks it up at
# hour 2 and places at hour 15.
URGENT_OPS = ()

#: Whether an animal purchase may take the slot of the day's last HIRE when the turn's ten market
#: order slots are full. See the note at the BUY_ANIMAL block. Off restores the old flat `< 8` cap.
ANIMAL_OVER_HIRE = True

#: Whether to hire a hand that will spawn walled in -- on a shed-access corner whose neighbours are all
#: LOCKED. It cannot move or BUILD, but PICKUP and DROP test shed-adjacency only and it is standing on
#: a shed tile, so it works as a loader. Off restores the old refusal, which cost -17 hand-turns a day
#: on one quadrant: our day-0 crew ramped 0,2,2,4,4,6,7 against the tape's 0,7,7,7,7,7,7.
HIRE_ONTO_LOCKED = False

#: How many turns sooner an idle unit must reach a claimed tile before it may take it off the unit
#: that claimed it. `None` disables stealing entirely and restores the old rule, where every tile in
#: a committed tour is off limits to everyone else for the rest of the day.
#:
#: **This is the open-loop problem again, moved from the schedule to the work.** `sells` forfeited a
#: row that could not be filled on its day; a claim forfeits work to a unit that cannot reach it.
#: Measured on Seb's tape, seed 11, day 0: a PLACE node is available from hour 9 and replans run at
#: hours 9, 14, 15, 16, 17 and 18 -- the work is visible and the planner IS running -- but the pen was
#: claimed at hour 6 by a unit with a long tour, so every idle unit after that was forbidden to take
#: it and the animal was placed at **hour 18**. Placed that late it cannot be fed: the shed is four
#: moves away and the budget at hour 20 is `24 - 20 - 1 = 3`, so it goes unfed and uncared, which is
#: `feed -2` and `care -2` against the tape on day 0.
#:
#: A claim is not a freehold. It is only worth honouring while the claimant is the one who gets there
#: first. If a stolen node's original owner arrives to find nothing to do it goes idle and is topped
#: up on the next turn, so the loss is bounded at one turn and the gain is the whole afternoon.
STEAL_MARGIN = None      # measured NET NEGATIVE once hiring was fixed: 46 cells against 39

#: How many days an uncovered sell row stays offerable. **The backlog must expire.** Carrying it
#: forever is not "cumulative", it is unbounded: on the old leader's plan the schedule asks to sell
#: more than we ever produce, so the uncovered remainder grew every day and the offer pinned at the
#: season's largest row on every turn from about day 19 -- byte-identical to the runaway `asked - sold`
#: ledger it was meant to replace, and money -19,407 -> -30,262 against that tape. The measured bug is
#: a ONE day slip (Seb's melons ripen a day after his `MELON: 18` row), so the window only has to be
#: wide enough to cover a late harvest.
SELL_CARRY_DAYS = 3

LAND_PRICES = R.LAND_PRICES

#: Task priority. Pen work first because it is nearly free -- the herd lives on the shed cells, so FEED,
#: CARE and COLLECT_FERTILIZER cost no walk -- and because two missed feeds and the animal is gone
#: outright (`kaggriculture.py:786`). A thirsty tile next: two dry days makes it a weed, and weeded ground
#: refuses PLANT until someone digs it, so the tile is dead for the season.
RANK = dict(FEED=0, CARE=1, COLLECT_FERTILIZER=2, WATER_THIRSTY=3, HARVEST=4,
            PLACE=5, BUILD=6, WATER=7, FERTILIZE=8, PLANT=9, DIG=10)


def _owned(tile, unlocked):
    return R.quadrant_of(tile[0], tile[1]) in unlocked


def _mobile(pos, unlocked):
    """Can this unit do anything at all today?

    A LOCKED tile no-ops every op except MOVE (`kaggriculture.py:322`), and MOVE onto a LOCKED tile is
    refused as well (:313). Hands wake on `(5,4)`, `(4,5)` and `(5,5)` in rotation, so while only NW is
    owned the third hand of every four wakes on `(5,5)` -- whose four orthogonal neighbours are all in
    locked quadrants -- and is boxed in for the whole day. It cannot even be walked home.

    That is the game's rule, not ours, and the tape pays it too. What is ours is what the planner did
    about it: it assigned that unit four jobs, the executor dropped them as unreachable, the unit read
    as idle, and the top-up handed it the SAME four jobs back on every turn to dusk. Work parked on a
    boxed-in hand was never offered to a hand that could reach it, so day 0 finished a pen short.
    """
    if _owned(pos, unlocked):
        return True
    x, y = pos
    return any(_owned((x + dx, y + dy), unlocked)
               for dx, dy in ((0, -1), (0, 1), (1, 0), (-1, 0))
               if 0 <= x + dx < R.BOARD_SIZE and 0 <= y + dy < R.BOARD_SIZE)


def _step_towards(src, dst, unlocked):
    """One legal step from `src` towards `dst`, or None.

    A move onto LOCKED is ignored by the environment without spending the turn, so the destination has to
    be CHECKED rather than assumed -- that check is the whole of what dead reckoning could not do.
    """
    src, dst = tuple(src), tuple(dst)
    if src == dst:
        return None
    here = abs(src[0] - dst[0]) + abs(src[1] - dst[1])
    order = []
    if dst[1] != src[1]:
        order.append("SOUTH" if dst[1] > src[1] else "NORTH")
    if dst[0] != src[0]:
        order.append("EAST" if dst[0] > src[0] else "WEST")
    order += [m for m in ("NORTH", "SOUTH", "EAST", "WEST") if m not in order]
    for m in order:
        dx, dy = STEP[m]
        nxt = (src[0] + dx, src[1] + dy)
        if not (0 <= nxt[0] < R.BOARD_SIZE and 0 <= nxt[1] < R.BOARD_SIZE):
            continue
        if not _owned(nxt, unlocked):
            continue
        if abs(nxt[0] - dst[0]) + abs(nxt[1] - dst[1]) < here:
            return m
    return None


def _nearest_empty(tiles, unlocked, origin, skip=frozenset()):
    """Nearest empty owned tile, preferring ground that touches what we already work.

    Adjacency beats raw distance because every tile is revisited ~20 times a season: five adjacent tiles
    is a four-step tour, five spread round a ring is twelve.
    """
    worked = {(x, y) for y, r in enumerate(tiles) for x, c in enumerate(r) if isinstance(c, dict)}
    best = None
    for y, r in enumerate(tiles):
        for x, c in enumerate(r):
            t = (x, y)
            if c is not None or t in skip or t in SHED or not _owned(t, unlocked):
                continue
            touch = sum(1 for w in worked if abs(w[0] - x) + abs(w[1] - y) == 1)
            key = (-touch, abs(x - origin[0]) + abs(y - origin[1]), t)
            if best is None or key < best[0]:
                best = (key, t)
    return best[1] if best else None


def _next_ground(order, tiles, taken):
    """The next tile in the placement sweep that the board says is free.

    Replaces `_nearest_empty`'s per-tile `(adjacency, distance)` score, which grew a snake out from
    whichever tile was planted first. Measured on tour length -- the thing paid ~20 times a season --
    the two are level inside one quadrant, and the sweep wins by 23-35% once land is bought:

        quadrants        tiles     sweep    adjacency-greedy
        NW               8-24      8-24     9-24
        NW NE SW         20        20       31
        NW NE SW         30        37       48

    That is the case the farm actually plays, because the parcels arrive around days 7-10 and the crew
    works twenty to thirty tiles from then on.
    """
    for t in order:
        if t not in taken and tiles[t[1]][t[0]] is None:
            return t
    return None


def _emit(op, item):
    if op == "BUILD":
        return ["BUILD_COOP" if R.ANIMALS[item]["structure"] == "COOP" else "BUILD_PASTURE"]
    if op == "PLANT":
        return ["PLANT", item]
    if op == "PLACE":
        return ["PLACE", item, 1]
    return [op]


def _live_ops(tile, cell, day, inv, pins, seeds):
    """The ops still worth doing at `tile`, **re-derived from the live board every turn**.

    This is the whole trick to committing to a tour without going back to predicting state. The route
    fixes *which tiles* a unit visits and in what order -- stable, because a tile is a tile. What it
    does when it gets there is read off the cell, so a stop whose work another unit already did, or
    whose crop weeded overnight, simply returns nothing and the stop is dropped.

    Item-bearing ops are gated on **this unit's** inventory rather than the shed. Gating on the shed is
    what let a unit stand on a pen emitting FEED with no wheat in hand, silently no-oping and re-picking
    the same op forever.
    """
    if tile in pins:
        op, item, _prize = pins[tile]
        if cell is not None:
            return []
        if op == "PLANT":
            return [("PLANT", item)] if seeds.get(item, 0) > 0 else []
        return [("BUILD", item)]
    if not isinstance(cell, dict):
        return []
    kind = cell.get("kind")
    if kind == "PLANT":
        ops = RT.crop_ops(cell, day, inv.get("FERTILIZER", 0) > 0)
    elif "animal" in cell:
        ops = RT.animal_ops(cell, day, inv.get("WHEAT", 0) > 0)
    elif kind in ("PASTURE", "COOP"):
        ops = next(([("PLACE", a, 0)] for a in R.ANIMAL_NAMES
                    if R.ANIMALS[a]["structure"] == kind and inv.get(a, 0) > 0), [])
    elif kind == "WEED":
        ops = [("DIG", None, 0)]
    else:
        ops = []
    return [(o, i) for o, i, _p in ops]


def _eta_along(start, route):
    """Turn each tile of a committed tour is actually reached, walking the tour in order.

    Manhattan distance plus service, which is what `plan_routes` costs an insertion at, so the two
    agree about what "sooner" means. Only the ORDER matters here, not the absolute turn.
    """
    out, t, pos = {}, 0, tuple(start)
    for n in route:
        t += abs(n.tile[0] - pos[0]) + abs(n.tile[1] - pos[1]) + n.service
        out.setdefault(n.tile, t)
        pos = n.tile
    return out


def _claimed_tiles(units, routes, idle, margin):
    """Tiles an idle unit may NOT take, given who claimed them and when they will actually arrive.

    The old rule was `every tile in any committed tour`, which makes a claim permanent: a pen claimed
    at hour 6 by a unit twenty steps away is closed to a unit standing next to it at hour 9. See
    `STEAL_MARGIN` for the measurement -- that is exactly how day 0's last two animals reached their
    pens at hour 18 and went unfed.

    A tile is released only when an idle unit reaches it at least `margin` turns sooner than its
    claimant, so a tour is never broken up for a marginal gain.
    """
    claimed = {}
    for u, st in routes.items():
        if u in idle:
            continue
        for tile, eta in _eta_along(units[u], st.get("route") or ()).items():
            if eta < claimed.get(tile, 1 << 30):
                claimed[tile] = eta
    if margin is None:
        return set(claimed)
    busy = set()
    for tile, eta in claimed.items():
        soonest = min((abs(tile[0] - units[u][0]) + abs(tile[1] - units[u][1]) for u in idle),
                      default=1 << 30)
        if soonest + margin >= eta:
            busy.add(tile)
    return busy


def _refresh_pins(state, sched, day, tiles, unlocked):
    """Keep the schedule-derived tiles PINNED until the board resolves them.

    A board task carries its own identity -- the tile *is* the task -- but `PLANT a strawberry` and
    `BUILD a pasture` have none until something assigns them ground. `_nearest_empty` re-derived that
    ground every turn, so a planned `PLANT at (2,3)` became `(2,4)` the next turn and the plan was
    dropped as stale: the committed-tour port banked **$0** with 211 work ops a season for exactly this
    reason. Pinning once, and only re-pinning when the board invalidates the choice, is the fix.

    Both targets are **cumulative**, because a per-day row that failed on a thin bank was never retried:
    5 pens all season against a schedule's 14, and therefore every animal figure at ~21% of the tape's.
    Plantings additionally expire -- `plant_prize` is 0 once the season cannot finish the crop -- so late
    ground is left empty rather than seeded with something that will never mature.
    """
    pins = state["pins"]
    order = RT.field_order(unlocked)
    for t in list(pins):
        x, y = t
        if tiles[y][x] is not None:                       # planted, built, or a weed took the ground
            pins.pop(t)
        elif pins[t][0] == "PLANT" and RT.plant_prize(pins[t][1], day) <= 0:
            pins.pop(t)
        elif not _owned(t, unlocked):
            pins.pop(t)
    taken = set(pins)

    structures = sum(1 for r in tiles for c in r
                     if isinstance(c, dict) and (c.get("kind") in ("PASTURE", "COOP")
                                                 or "animal" in c))
    want_pens = sum(int(sched.get(d, {}).get("builds", 0) or 0) for d in range(day + 1))
    wanted = [a for d in sorted(sched) if d <= day for a in (sched[d].get("places") or [])]
    have = structures + sum(1 for v in pins.values() if v[0] == "BUILD")
    while have < want_pens:
        a = wanted[have] if have < len(wanted) else "COW"
        # A pen ON a shed-access cell runs its whole daily loop -- draw feed, feed, care, collect,
        # harvest -- without a single move, so those four cells are worth more than any field tile.
        spot = next((c for c in R.shed_access_tiles()
                     if _owned(c, unlocked) and tiles[c[1]][c[0]] is None and c not in taken), None)
        spot = spot or _next_ground(order, tiles, taken)
        if spot is None:
            break
        pins[spot] = ("BUILD", a, R.ANIMALS[a]["cost"])
        taken.add(spot)
        have += 1

    want = collections.Counter()
    for d in sorted(sched):
        if d <= day:
            want.update(sched[d].get("plants") or [])
    live = collections.Counter(v[1] for v in pins.values() if v[0] == "PLANT")
    for crop, qty in want.items():
        if crop not in CROP or RT.plant_prize(crop, day) <= 0:
            continue
        for _ in range(qty - state["planted"][crop] - live[crop]):
            spot = _next_ground(order, tiles, taken)
            if spot is None:
                break
            pins[spot] = ("PLANT", crop, RT.plant_prize(crop, day))
            taken.add(spot)
    return pins


def _router_acts(state, sched, day, hour, tiles, units, invs, shed, seeds, unlocked):
    """One turn of the routed plan: replan if the crew or the work changed, then walk the tours."""
    pins = _refresh_pins(state, sched, day, tiles, unlocked)
    carried = collections.Counter()
    for iv in invs:
        carried.update(iv)
    budget = [max(0, TPD - hour - 1)] * len(units)
    routes = state["routes"]
    # Only shed cells inside a quadrant we own. A hand wakes on a LOCKED one and a LOCKED tile no-ops
    # before PICKUP is ever reached, so treating all four as depots strands the hand for the whole day.
    depots = tuple(c for c in R.shed_access_tiles() if _owned(c, unlocked)) or (SPAWN,)
    load = {u: collections.Counter(invs[u] if u < len(invs) else {}) for u in range(len(units))}

    def nodes_for(skip):
        return [n for n in RT.build_nodes(tiles, day, shed, carried, unlocked, pins, hour)
                if n.tile not in skip]

    # Only units that can legally act are vehicles. A boxed-in hand is not a slow vehicle, it is no
    # vehicle at all, and planning work onto it silently deletes that work for the day.
    live = [u for u in range(len(units)) if _mobile(units[u], unlocked)]

    # **New work is a replan trigger, not just new workers.** See `URGENT_OPS`. The crew stabilises by
    # mid-morning and every unit is committed, so between the last hire and the first idle unit nothing
    # replans -- on Seb's day 0 that is hours 10-13, exactly when four pens finish and become placeable.
    # The animals waited, went in at hour 18, and could no longer be fed.
    # Key on (tile, op), never on the tile alone. A pen is BUILT and then PLACEd on the SAME square, so
    # the tile is already sitting in the builder's route when the PLACE node appears -- subtracting
    # routed *tiles* silently swallowed every new placement and the trigger never fired once.
    urgent = {(n.tile, o) for n in RT.build_nodes(tiles, day, shed, carried, unlocked, pins, hour)
              for o, _i in n.ops if o in URGENT_OPS} if URGENT_OPS else set()
    routed = {(n.tile, o) for st in routes.values() for n in st["route"] for o, _i in n.ops}
    fresh = urgent - state["seen_urgent"] - routed
    state["seen_urgent"] = urgent

    if state["crew"] != len(live) or not routes:
        # A full replan only when the crew changes -- hands are hired through the morning, so the dawn
        # plan genuinely cannot know how many vehicles it has.
        sub = RT.plan_routes([units[u] for u in live], nodes_for(set()),
                             [budget[u] for u in live], depots,
                             {k: load[u] for k, u in enumerate(live)}, supply=shed)
        state["routes"] = routes = {u: sub[k] for k, u in enumerate(live)}
        state["crew"] = len(live)
    else:
        idle = [u for u in live if not routes.get(u, {}).get("route")]
        # **Fresh urgent work is an INSERTION, not a rebuild.** Rerunning the whole plan every time a
        # PLACE node appeared MEASURED as day 0 `place` 4/4 -> 3/4 and `build_pasture` 8/8 -> 7/8:
        # day 0 buys four animals, so it triggered four full replans and each one abandoned whatever
        # the crew was part-way through. That is the same thrash the per-turn greedy had.
        #
        # One unit is enough to serve it, and the cheapest one to divert is the one already nearest a
        # depot, since the animal has to be drawn from the shed before it can be placed. Everyone
        # else keeps their tour. Measured on Seb's tape, seed 11, day 4: the cow lands in the shed at
        # hour 2 and no unit falls idle until hour 10, by which time the budget is 13 and the far pen
        # plus the walk home no longer fits, so it sits there to dusk.
        # TRIED, both MEASURED WORSE on day 0, which comes first:
        #   full replan on `fresh`            place 4/4 -> 3/4, build_pasture 8/8 -> 7/8
        #   divert the unit nearest a depot   place 4/4 -> 3/4, feed and care 4/4 -> 2/4
        # Diverting one unit is still diverting a unit that was part-way through a tour. The day-4 cow
        # does not need a new trigger -- it needs to be in the shed by hour 1, when the crew-change
        # replan runs anyway.
        if idle:
            # **Top up the idle units only.** Replanning everybody would break the commitment of a unit
            # already three steps into a tour, which is the thrash the per-turn greedy had.
            busy = _claimed_tiles(units, routes, idle, STEAL_MARGIN)
            # **A top-up sees a shed that other units have already spoken for.** `busy` retires
            # claimed TILES, and the oversubscription is across tiles: with one COW and three empty
            # pens, the committed unit holds one pen and the other two are still on offer to whoever
            # goes idle next. So the supply handed to this pass is the shed net of every draw a busy
            # unit has booked and not yet collected.
            spoken = collections.Counter()
            for u, st in routes.items():
                if u in idle:
                    continue
                for it, qty in (st.get("draw") or {}).items():
                    spoken[it] += max(0, qty - load[u][it])
            free = {it: q - spoken[it] for it, q in shed.items()}
            sub = RT.plan_routes([units[u] for u in idle], nodes_for(busy),
                                 [budget[u] for u in idle], depots,
                                 {k: load[u] for k, u in enumerate(idle)}, supply=free)
            for k, u in enumerate(idle):
                routes[u] = sub[k]

    acts = []
    for u, pos in enumerate(units):
        inv = collections.Counter(invs[u] if u < len(invs) else {})
        st = routes.get(u)
        if st is None:
            acts.append(["PASS"])
            continue

        # ------------------------------------------------------------------ one shed trip, in bulk
        # `PICKUP` is unbounded -- `n = min(n, available)` then `_inv_add(inv, item, n)` -- so a unit
        # servicing six pens draws six wheat in ONE turn. Drawing one at a time, as the greedy did, made
        # every pen a shed round trip and is most of why FEED landed on 81% of animal-days.
        draw = None
        for item, qty in st["draw"].items():
            short = qty - inv.get(item, 0)
            if short > 0 and shed.get(item, 0) > 0:
                draw = (item, min(short, shed[item]))
                break
        if draw is None:
            st["draw"].clear()
        elif pos in depots:
            shed[draw[0]] -= draw[1]
            acts.append(["PICKUP", draw[0], draw[1]])
            continue
        else:
            home = min(depots, key=lambda c: abs(c[0] - pos[0]) + abs(c[1] - pos[1]))
            m = _step_towards(pos, home, unlocked)
            if m:
                acts.append([m])
                continue
            st["draw"].clear()

        # ------------------------------------------------------------------ walk the committed tour
        act = ["PASS"]
        while st["route"]:
            node = st["route"][0]
            if pos != node.tile:
                m = _step_towards(pos, node.tile, unlocked)
                if m is None:                       # unreachable: drop the stop rather than idle on it
                    st["route"].pop(0)
                    continue
                act = [m]
                break
            ops = _live_ops(node.tile, tiles[node.tile[1]][node.tile[0]], day, inv, pins, seeds)
            if not ops:
                st["route"].pop(0)
                continue
            op, item = ops[0]
            act = _emit(op, item)
            if op == "PLANT":
                state["planted"][item] += 1
                seeds[item] -= 1
                pins.pop(node.tile, None)
            elif op == "BUILD":
                # Keep the stop: next turn the cell reads PASTURE and `_live_ops` returns the PLACE,
                # so the animal goes in without a second trip.
                pins.pop(node.tile, None)
            break

        # ------------------------------------------------------------------ opportunistic mid-tour drop
        # Pens sit ON shed-access tiles by design (`_refresh_pins`), so a unit servicing them already
        # stands at a depot repeatedly through the day. Firing only when the tour-walk already chose a
        # MOVE means this never outranks a real op at the current tile.
        #
        # BOTH gates are required, and each one is a test that went red without it. `future_needs`,
        # recomputed fresh every turn, answers "does MY OWN remaining tour want this good" and stops
        # the PICKUP/DROP thrash -- a unit ferrying wheat to its own FEED stops is left alone.
        # `FEED_DAYS * alive`, the farm-wide reserve the SELL guard also protects, stops the theft of
        # the self-healing material: when a unit's nodes fail it goes idle and the `if idle:` top-up
        # re-plans it from `load[u]`, that unit's OWN inventory, which only works while the wheat is
        # still in hand.
        if (OPPORTUNISTIC_DROP and act[0] in STEP and pos in depots
                and any(v > 0 for v in inv.values())):
            future_needs = collections.Counter()
            for n in st["route"]:
                future_needs.update(n.needs)
            own_route_needs_it = any(future_needs.get(it, 0) > 0 for it, qty in inv.items() if qty > 0)
            alive = sum(1 for r in tiles for c in r if isinstance(c, dict) and "animal" in c)
            farm_wheat = shed.get("WHEAT", 0) + carried.get("WHEAT", 0)
            wheat_ok = (inv.get("WHEAT", 0) == 0
                        or farm_wheat - inv.get("WHEAT", 0) >= FEED_DAYS * alive)
            if (not own_route_needs_it and wheat_ok and sum(inv.values()) >= MIN_OPPORTUNISTIC_DROP
                    and sum(shed.values()) + sum(inv.values()) <= SHED_CAPACITY):
                for item, qty in inv.items():
                    if qty > 0:
                        shed[item] = shed.get(item, 0) + qty
                act = ["DROP"]

        # ------------------------------------------------------------------ the return leg
        # A one-way sweep cannot sell what it picks up. Measured against the tape on days 1-3 of seed
        # 11: `EAST 0/10, 0/17, 0/15` and `SOUTH 0/13, 0/14, 0/14` -- our crew never turned back towards
        # the shed on three consecutive days while the tape emitted DROP one to two times daily, so our
        # harvest could not reach the market until `_drop_inventories_to_shed` ran overnight.
        #
        # The turns cost nothing: this only fires once the tour is done and the unit would PASS. DROP
        # moves the WHOLE inventory and DELETES anything the shed has no room for
        # (`kaggriculture.py:333`), so it is refused when the shed is near full.
        # **TRIED and REVERTED: drop the surplus whenever standing on the shed, not only at tour end.**
        # The symptom is real and traced (`scripts/where_the_cow_goes.py`, seed 11 day 4 of Seb's plan):
        # the crew harvests from h5 and the first DROP lands at h19, so `SELL WHEAT` cannot be offered
        # until h19 and the bank sits at $316 all day. Everything bank-gated queues behind it -- the COW
        # settles at h19, by which point the free pens are three steps away with four turns left
        # (PICKUP + 3 moves + PLACE = 5), so it is never placed, and day 5's seed order half-fills.
        #
        # Dropping anything held beyond `Node.needs` for the rest of the tour MEASURED as a loss over
        # twelve seeds at weedSpawnChance 0.005: our schedule $119,281 -> $104,009, Seb's $96,064 ->
        # $84,913. It also broke `test_wheat_already_in_a_hand_feeds_the_herd_with_an_EMPTY_shed`: a
        # unit holding feed on a shed cell dumped it back, because `needs` is what the ROUTE will draw
        # at the depot and not what the unit is already carrying for the jobs ahead of it. Getting the
        # harvest home earlier is still the right goal; this accounting is not the way to it.
        if act == ["PASS"] and not st["route"] and any(v > 0 for v in inv.values()):
            if sum(shed.values()) + sum(inv.values()) <= SHED_CAPACITY:
                if pos in depots:
                    for item, qty in inv.items():
                        if qty > 0:
                            shed[item] = shed.get(item, 0) + qty
                    act = ["DROP"]
                else:
                    m = _step_towards(pos, min(depots, key=lambda c: abs(c[0] - pos[0])
                                               + abs(c[1] - pos[1])), unlocked)
                    act = [m] if m else act
        acts.append(act)
    return acts


def make_agent(schedule, me=0, router=True):
    """`agent(obs, config) -> action`.

    `router=True` solves the day as a Team Orienteering Problem (`kagg/search/router.py`): tiles are
    pinned, tours are committed, and each stop's ops are re-derived from the live board. `router=False`
    is the earlier per-turn greedy, kept only so the two can be measured on one seed list.
    """
    sched = {int(k): v for k, v in schedule.items()}
    state = dict(assigned={}, hired=0, day=-1, tour={}, bought=collections.Counter(),
                 pins={}, routes={}, crew=-1, seen_urgent=set(),
                 planted=collections.Counter(),
                 ordered=collections.Counter(), shed_max=collections.Counter(),
                 uncovered=collections.deque(maxlen=SELL_CARRY_DAYS))

    def agent(obs, config=None):
        day = int(obs.get("day", 0) or 0)
        hour = int(obs.get("hour", 0) or 0)
        farms = obs.get("farms") or []
        if len(farms) <= me:
            return {"farmer": ["PASS"], "hands": [], "market": []}
        farm = farms[me]
        priv = obs.get("private") or {}
        shed = collections.Counter(priv.get("shed") or {})
        seeds = collections.Counter(priv.get("seeds") or {})
        invs = priv.get("inventories") or [{}]
        tiles = farm["tiles"]
        money = float(farm["money"])
        unlocked = set(farm.get("unlocked_quadrants") or ["NW"])
        row = sched.get(day, {})

        if day != state["day"]:              # hands are dismissed nightly, so every claim is stale
            # **Carry forward only the part of yesterday's sell row the shed could never have covered.**
            # The observation carries no fill log, so a fill cannot be counted directly -- but the offer
            # stands on every one of the 24 turns, so the largest the shed reached yesterday is the most
            # that row could possibly have shifted. What is left is demand that never had a chance, and
            # it is the only part worth retrying. A cumulative `asked - sold` ledger was tried first and
            # ran away: the credit under-counts whenever a DROP lands on the same turn as a fill, so
            # `owed` never reached zero and the offer pinned at the season's largest row every turn from
            # about day 19 -- 63 strawberries at a time. On the old leader tape that turned a trace that
            # was better on every field through day 18 into money -19,407 -> -30,262.
            for d in range(max(0, state["day"]), day):
                left = collections.Counter()
                for p, q in ((sched.get(d, {}) or {}).get("sells") or {}).items():
                    # **`shed_max` is peak STOCK, which is not what was sold.** Fertilizer arrives one
                    # unit at a time and clears on the turn it lands, so the shed never holds more than
                    # one of it however many we sell. Day 3 sold its whole row of 5 and `shed_max` read
                    # 1, booking a phantom shortfall of 4 -- which day 4 then "recovered" by selling a
                    # fifth fertilizer against a row of 4, while the tape sells exactly 4.
                    # The offers we actually placed are the honest measure; keep `shed_max` as a floor
                    # for a day that was skipped entirely and has no tally.
                    short = int(q) - max(state["shed_max"][p], state["ordered"][("sold", p)])
                    if short > 0:
                        left[p] = short
                state["uncovered"].append(left)
                state["shed_max"] = collections.Counter()
            # `ordered` is per-day book-keeping for market orders that must happen ONCE, not once per
            # turn. Without it the agent re-issued the day's animals and seed on all 24 turns -- day 0
            # bought four animals at turn 0 and four more at turn 1 until the bank was empty, which is why
            # it reached day 1 on $61 and could then never afford a hand again.
            state.update(day=day, assigned={}, hired=0, ordered=collections.Counter(), tour={},
                         routes={}, crew=-1, seen_urgent=set())   # `pins` and `planted` survive by design

        units = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]

        # The unit phase decrements `shed` for every PICKUP it issues this turn, and `invs` was read
        # before it ran, so the drawn units are in neither by the time the market block costs the
        # herd's reserve. Keep the pre-draw level; the difference is the draw.
        shed_before = collections.Counter(shed)

        if router:
            acts = _router_acts(state, sched, day, hour, tiles, units, invs, shed,
                                seeds, unlocked)
        else:
            # ------------------------------------------------------------------ what the BOARD needs now
            # Carried stock, computed once: a task whose input is neither in the shed nor in a hand must not be
            # queued at all, or the unit that takes it deadlocks holding a job it can never start.
            wheat_carried = any(collections.Counter(iv).get("WHEAT", 0) > 0 for iv in invs)
            tasks = []
            for y, r in enumerate(tiles):
                for x, cell in enumerate(r):
                    t = (x, y)
                    if not isinstance(cell, dict):
                        continue
                    kind = cell.get("kind")
                    if kind == "PLANT":
                        info = CROP[cell["crop"]]
                        age = day - cell["planted_day"]
                        if not cell["watered_today"]:
                            thirsty = cell["consecutive_unwatered"] >= 1
                            in_window = (not info["ongoing"]
                                         and (info["max_day"] + 1) // 2 <= age <= info["max_day"])
                            if thirsty or in_window or info["ongoing"]:
                                tasks.append((RANK["WATER_THIRSTY"] if thirsty else RANK["WATER"],
                                              t, "WATER", None))
                        if cell["yield_units"] > 0 and age >= info["first"]:
                            tasks.append((RANK["HARVEST"], t, "HARVEST", None))
                        # **FERTILIZE, which the agent never did at all.** It doubles a tile's yield, but only
                        # on a day the tile is ALSO watered: `_daily_refresh_plants` computes
                        # `fertilized = was_watered and fertilized_until_day >= current_day`, and the one-shot
                        # WATER bonus is `2 if fertilized else 1`. It lasts three days (day..day+2), so it is
                        # worth applying just before a producing stretch and worthless outside one. The tape
                        # applies 107; we applied 0 and sold the fertilizer instead.
                        # Fertilizer in the shed OR already in a hand. A unit that has just run
                        # COLLECT_FERTILIZER is carrying one, and testing the shed alone found none -- because
                        # the sell list dumps every unit of FERTILIZER from the shed each turn, so it is gone
                        # before any tile can be fertilized. FERTILIZE fired 0 times against the tape's 107.
                        carried = any(collections.Counter(iv).get("FERTILIZER", 0) > 0 for iv in invs)
                        if (cell["fertilized_until_day"] < day
                                and age >= info["first"] - 2
                                and (shed.get("FERTILIZER", 0) > 0 or carried)):
                            tasks.append((RANK["FERTILIZE"], t, "FERTILIZE", "FERTILIZER"))
                    elif "animal" in cell:
                        # **Only queue a FEED if the wheat exists somewhere.** Without this a unit took the
                        # job, walked to the shed, found it empty, PASSed -- and because it still HELD the job
                        # it re-picked the same FEED next turn and froze there. Measured on the winner's
                        # schedule: FEED 0 with 83 idle unit-turns and live animals in the pens, day after day,
                        # because rank 0 kept every hand queued behind wheat that never arrived. Same silent
                        # shape as the rest: a failed precondition that does nothing instead of reporting.
                        if not cell["fed_today"] and (shed.get("WHEAT", 0) > 0 or wheat_carried):
                            tasks.append((RANK["FEED"], t, "FEED", "WHEAT"))
                        if not cell["cared_today"]:
                            tasks.append((RANK["CARE"], t, "CARE", None))
                        if cell["fertilizer_available"]:
                            tasks.append((RANK["COLLECT_FERTILIZER"], t, "COLLECT_FERTILIZER", None))
                        if cell["yield_units"] > 0:
                            tasks.append((RANK["HARVEST"], t, "HARVEST", None))
                    elif kind == "WEED":
                        tasks.append((RANK["DIG"], t, "DIG", None))
                    elif kind in ("PASTURE", "COOP"):
                        # An empty structure -- restock it if a matching animal is in the shed **or already in
                        # a hand**. Testing the shed alone dropped the task the instant the animal was picked
                        # up, so a unit that had just built a pen and was holding a cow forgot to place it:
                        # day 0 raised 4 pens and stocked 1.
                        for a in R.ANIMAL_NAMES:
                            if R.ANIMALS[a]["structure"] != kind:
                                continue
                            if shed.get(a, 0) > 0 or any(collections.Counter(iv).get(a, 0) > 0
                                                         for iv in invs):
                                tasks.append((RANK["PLACE"], t, "PLACE", a))
                                break

            # pens the schedule still wants, on shed cells first: a pen on `(4,4)` runs its whole daily loop
            # -- draw feed, feed, care, collect, harvest, deposit -- without a single move.
            standing = sum(1 for r in tiles for c in r
                           if isinstance(c, dict) and c.get("kind") in ("PASTURE", "COOP"))
            want_by_now = sum(int(sched.get(d, {}).get("builds", 0) or 0) for d in range(day + 1))
            claimed_spots = {t for _r, t, _o, _i in tasks}
            # **The schedule is a running TARGET, not a one-shot instruction.** Iterating only today's `places`
            # meant a pen we could not afford on its named day was never built again: 5 pens all season against
            # the schedule's 14, so 72 animal-days against the tape's 343 -- and every animal figure was ~21% of
            # the tape's purely because the herd was 21% the size. Servicing was already perfect at that size:
            # CARE 100% of animal-days, fertilizer collected 100%. Catch up whenever a beast is in the shed.
            want_animals = [a for d in sorted(sched) if d <= day
                            for a in (sched[d].get("places") or [])]
            for a in want_animals:
                if standing >= want_by_now or shed.get(a, 0) <= 0:
                    break
                spot = next((c for c in R.shed_access_tiles()
                             if _owned(c, unlocked) and tiles[c[1]][c[0]] is None
                             and c not in claimed_spots), None)
                spot = spot or _nearest_empty(tiles, unlocked, SPAWN, skip=claimed_spots)
                if spot is None:
                    break
                tasks.append((RANK["BUILD"], spot, "BUILD", a))
                claimed_spots.add(spot)
                standing += 1

            # plantings the schedule wants today, on ground the BOARD says is empty
            held = collections.Counter()
            for crop in (row.get("plants") or []):
                if seeds.get(crop, 0) - held[crop] <= 0:
                    continue
                spot = _nearest_empty(tiles, unlocked, SPAWN, skip=claimed_spots)
                if spot is None:
                    break
                held[crop] += 1
                claimed_spots.add(spot)
                tasks.append((RANK["PLANT"], spot, "PLANT", crop))

            tasks.sort(key=lambda z: z[0])

            # ------------------------------------------------------------------ one op per unit
            claimed, acts = set(), []
            for u, pos in enumerate(units):
                inv = collections.Counter(invs[u] if u < len(invs) else {})
                job = state["assigned"].get(u)
                if job and not any((t, o, i) == job for _r, t, o, i in tasks):
                    job = None                    # the board says it is done or gone
                if job is None:
                    # **Distance first, rank only to break ties among tasks that are equally close.** Keying
                    # `(rank, distance)` made rank dominate, so every unit sprinted across the board for the
                    # highest-priority task anywhere -- twelve hands heading for the same three pens -- and the
                    # crew spent 78% of its turns walking, ~7 move turns per work turn against the tape's 1.44.
                    # `dayplan._assign` already carried this lesson in a comment and it was not brought over:
                    # "Rank picks the hand's FIRST stop; distance picks every stop after it."
                    # **Rank picks the hand's FIRST stop; distance picks every stop after it.**
                    # `(rank, distance)` throughout made rank dominate, so every unit sprinted across the board
                    # for the highest-priority task anywhere -- twelve hands converging on three pens -- at ~7
                    # move turns per work turn against the tape's 1.44. `(distance, rank)` throughout fixed the
                    # walking to 1.04 and banked $809, because the nearest task is never the important one and
                    # the herd starved. So: a unit with no tour under way chooses by rank, and a unit that has
                    # just finished an op continues to whatever is nearest. `dayplan._assign` carried this
                    # lesson in a comment and it was not brought across.
                    touring = state["tour"].get(u, False)
                    best = None
                    for rank, t, op, item in tasks:
                        if t in claimed:
                            continue
                        d = abs(t[0] - pos[0]) + abs(t[1] - pos[1])
                        key = (d, rank) if touring else (rank, d)
                        if best is None or key < best[0]:
                            best = (key, (t, op, item))
                    if best is None:
                        acts.append(["PASS"])
                        continue
                    job = best[1]
                state["assigned"][u] = job
                tile, op, item = job
                claimed.add(tile)

                # Anything carried is drawn at a shed cell, and only when it is actually in store.
                if item and op in ("FEED", "PLACE", "FERTILIZE") and inv.get(item, 0) <= 0:
                    if pos in SHED and shed.get(item, 0) > 0:
                        shed[item] -= 1
                        acts.append(["PICKUP", item, 1])
                        continue
                    if shed.get(item, 0) <= 0:
                        # Nothing to fetch. RELEASE the job so this hand does something useful, instead of
                        # standing on a shed cell passing while it holds the highest-priority task on the board.
                        state["assigned"].pop(u, None)
                        claimed.discard(tile)
                        acts.append(["PASS"])
                        continue
                    home = min(SHED, key=lambda c: abs(c[0] - pos[0]) + abs(c[1] - pos[1]))
                    m = _step_towards(pos, home, unlocked)
                    acts.append([m] if m else ["PASS"])
                    continue

                if pos != tuple(tile):
                    m = _step_towards(pos, tile, unlocked)
                    if m is None:
                        state["assigned"].pop(u, None)
                        acts.append(["PASS"])
                    else:
                        acts.append([m])
                    continue

                if op == "BUILD":
                    acts.append(["BUILD_COOP" if R.ANIMALS[item]["structure"] == "COOP"
                                 else "BUILD_PASTURE"])
                    state["assigned"][u] = (tile, "PLACE", item)      # place it next turn, same tile
                elif op == "PLANT":
                    acts.append(["PLANT", item])
                    state["assigned"].pop(u, None)
                    state["tour"][u] = True
                elif op == "PLACE":
                    acts.append(["PLACE", item, 1])
                    state["assigned"].pop(u, None)
                    state["tour"][u] = True
                else:
                    acts.append([op])
                    state["assigned"].pop(u, None)
                    state["tour"][u] = True

        # ------------------------------------------------------------------ the market, bank-aware
        orders = []
        # How many mouths there are, needed BEFORE the sell loop so the herd's feed is not sold.
        alive = sum(1 for r in tiles for c in r if isinstance(c, dict) and "animal" in c)
        # SELL first: the proceeds have to be in the bank before anything below spends them, and that
        # ordering is exactly what decided whether BUY_LAND cleared at all.
        #
        # **`sells` is a CUMULATIVE target, like every other target in this file.** `plants`, `builds`
        # and `animals_bought` were each converted from a per-day row for the same reason: a row that
        # could not be filled on the day it appeared was silently forfeited and never retried. Sells
        # was the last one left per-day, and it was the largest divergence on Seb's tape. He sells
        # `MELON: 18` on day 10 and asks for no melon again until day 16; our melons ripen one day
        # later, so the day-10 row fired against an EMPTY shed. We then held those 18 melons from day
        # 11 to day 15 on **$2**, could not afford the $4,000 third parcel until day 16, and farmed 25
        # fewer tiles for six days -- a plant deficit that tracked the missing land almost unit for
        # unit (-26 plants against -25 tiles on day 12) and is the source of the harvest gap.
        #
        for p, q in shed.items():
            state["shed_max"][p] = max(state["shed_max"][p], int(q))
        # Wheat standing RIPE in the field: accrued `yield_units`, one HARVEST from the hand. It is
        # stock for the herd on both sides of the market -- see the feed reserve below and the feed
        # top-up further down -- and it is NOT the same as wheat still growing, which yields nothing
        # today and must never be counted.
        ripe_wheat = sum(int(c.get("yield_units", 0) or 0) for r in tiles for c in r
                         if isinstance(c, dict) and c.get("kind") == "PLANT"
                         and c.get("crop") == "WHEAT")
        prices = (obs.get("market") or {}).get("prices") or {}
        pending = 0          # cash this turn's sells will have banked by the time BUY_LAND settles
        rate = collections.Counter()
        for d in sorted(sched):
            if d > day:
                break
            for p, q in (sched[d].get("sells") or {}).items():
                rate[p] = max(rate[p], int(q))
        for prod in ("MELON", "WOOL", "MILK", "STRAWBERRY", "FERTILIZER", "WHEAT"):
            have = int(shed.get(prod, 0))
            # **Hold back fertilizer the FIELD can use -- not a constant.** Applied to a watered,
            # producing tile it doubles the yield (a strawberry tile is 4 units at $120, so doubling
            # beats the $100 the unit sells for), and dumping the whole shed every turn is why
            # FERTILIZE never fired at all. But the reserve used to be a flat 4, which on any day the
            # shed holds four or fewer cancels the sale ENTIRELY, whether or not a single tile could
            # take it. Measured on Seb's day 1, where his plan and ours are otherwise near-identical:
            # he sells 4 and ends on $356, we sell 0 and end on $189. Four fertilizer at the realised
            # ~$42 is the whole $167 gap -- on the day the bank has to start compounding if the day-4
            # parcel is ever to clear. `crop_ops` already knows which tiles fertilizing pays on, so
            # ask it rather than guessing a number.
            if prod == "FERTILIZER":
                want = sum(1 for r in tiles for c in r
                           if isinstance(c, dict) and c.get("kind") == "PLANT"
                           and "FERTILIZE" in [o for o, _i, _p in RT.crop_ops(c, day, True)])
                have = max(0, have - want)
            # **Never sell the herd's feed.** WHEAT is both a crop we grow and the feed we buy, and the
            # sell list dumps whatever the shed holds. Measured per turn on day 13 with eleven animals:
            #     h0  BUY_PRODUCT WHEAT 11   shed 0 -> 11
            #     h1  SELL        WHEAT  6   shed 11 -> 0
            # every day, all season, which is why `shed WHEAT` read 0 at midday on all thirty days while
            # the bank climbed to $85,000 and the herd decayed from eleven animals to four. Only the
            # surplus above one wheat per animal may go.
            #
            # **Measured against the FIELD as well as the shed.** On day 4 of Seb's tape the reserve
            # is 14 against a shed of 6, so nothing was sellable until the harvest pushed the shed
            # past it at hour 18 -- bank $29 from hour 2 to hour 18, then SELL WHEAT 17 into the last
            # hour of the book, and the $1,000 parcel he takes at hour 22 slipped to day 5. Fourteen
            # ripe tiles feed the herd perfectly well; the reserve is against starving it, not against
            # counting what it is standing in.
            # **Wheat already drawn for the herd is the reserve, not extra to it.** `_router_acts`
            # runs before this block and decrements `shed` on the turn a unit PICKUPs, so a feed
            # round trip is subtracted twice -- once out of the shed and once again as reserve.
            # Measured on Seb's tape, seed 11, day 5: seven animals, shed 27 at dawn, four wheat
            # drawn on the same turn, so `have` reads 23 - 14 = 9 and we offer `SELL WHEAT 9`
            # against a row of 17. He sells the whole 17 at hour 0 and buys four back at hours
            # 6, 7 and 9. `on_hand` on the buy side has always counted hands; this is the same sum.
            #
            # **And wheat the row says we will BUY today is stock too.** The reserve is against
            # starving the herd, and `buys` is a commitment the same turn loop honours further down.
            # Day 5's row is `sells WHEAT 17, buys WHEAT 4`: he sells the whole 17 at hour 0 holding
            # ten, then tops back up to fourteen at hours 6, 7 and 9. Counting the draw but not the
            # purchase still capped us at 13.
            if prod == "WHEAT":
                carried_wheat = sum(collections.Counter(iv).get("WHEAT", 0) for iv in invs)
                drawn = max(0, int(shed_before.get("WHEAT", 0)) - int(shed.get("WHEAT", 0)))
                will_buy = int((row.get("buys") or {}).get("WHEAT", 0))
                have = max(0, have - max(0, FEED_DAYS * alive - ripe_wheat - carried_wheat
                                         - drawn - will_buy))
            # **The carry recovers a MISSED row; it is not a licence to dump the shed.** `market_price`
            # falls monotonically in inventory and a SELL walks n units down that curve one at a time,
            # so a bigger offer clears at a worse mean price -- measured as wool 123 units -> 138 for
            # REVENUE $29,041 -> $21,811. `rate` is the largest single day the schedule ever asks for,
            # so two missed rows of 5 are recovered 5 at a time over as many turns as it takes, and the
            # per-offer rate the standing offer relies on is unchanged.
            if CUMULATIVE_SELLS:
                today = int((row.get("sells") or {}).get(prod, 0))
                carry = sum(u[prod] for u in state["uncovered"])
                n = min(have, today + carry, rate[prod])
                # **The row is a DAY TOTAL, and re-offering it every turn made it a per-turn quota.**
                # `rate` bounds one offer; nothing bounded the day. Seb's day-4 row asks
                # `WHEAT 28, FERTILIZER 4` and he sells exactly that -- 28 and 4. We sold 34 and 5,
                # and day 5 then sold 10 against his 26 with the stock already gone. The carry above
                # is what recovers a genuinely missed row; it is not a licence to outrun a met one.
                n = min(n, today + carry - state["ordered"][("sold", prod)])
            else:
                n = min(have, int((row.get("sells") or {}).get(prod, 0)))
            # **Do not sell into a collapsed book.** `market_price` falls monotonically in inventory
            # (`kaggriculture.py:177`) and a SELL walks n units down that curve one at a time, so the
            # whole stack clears near what the LAST unit fetches. Measured over one season as the herd
            # came right: wool 123 units -> 138, and wool REVENUE $29,041 -> $21,811. Fifteen extra
            # units cost $7,230 because the mean price went $234 -> $158.
            #
            # Holding is not a loss. Shops drain inventory every 4 steps and the town centre every 12,
            # at 4x from day 20 (`kaggriculture.py:706-716`), so a collapsed price recovers on its own.
            #
            # **Re-offering the day's quota on every turn is correct, and two attempts to "fix" it both
            # lost money.** The quota looks like a dump -- one season's wool went 123 units to 138 while
            # wool REVENUE fell $29,041 to $21,811 -- but neither remedy survived twelve seeds:
            #
            #     refuse to sell below 0.5 x base price      -$16,025   goods never clear at all
            #     cap the quota to a day total, not a turn    -$ 2,653   misses the book's recovery
            #
            # `market_price` does fall in inventory, but shops drain it every 4 steps and the town
            # centre every 12, at 4x from day 20 (`kaggriculture.py:706-716`), so the book refills
            # continuously and a standing offer collects each recovery. An order is only a request:
            # it fills one unit at a time and stops when the shed empties, so re-offering is free.
            if n > 0 and len(orders) < 5:
                orders.append(["SELL", prod, n])
                state["ordered"][("sold", prod)] += n
                # Proceeds this turn will settle BEFORE any atomic order queued below, because
                # `_process_market` walks the slots and clears each slot's atomic order after every
                # earlier slot has traded. Quoted at the current price, which is a slight
                # over-estimate since a SELL walks the book down one unit at a time -- and an
                # over-estimate is safe here, since `_do_buy_land` simply returns on a short bank
                # and the order is re-offered next turn.
                pending += n * int(prices.get(prod, 0) or 0)

        # **The crew comes before the goods.** See `HIRE_FIRST`. SELL stays above this because it only
        # raises the bank; everything BELOW spends it, and a hand that is not standing at dawn cannot be
        # bought back later in the day -- the turns are simply gone. The cost is unchanged either way:
        # `_hire_cost` is `mult * fib(hires_today)`, a per-DAY counter.
        #
        # The limit is not a count but a landing square, and it has to be computed from where the crew
        # ACTUALLY stands. `_spawn_hand` takes the least-occupied shed-access tile, ties NWSE, counting
        # the units present at the moment the HIRE settles -- so occupancy must come from `units`, not
        # from a spawn table. `routines.spawn_order` was tried here and is wrong for this: it models
        # every unit as still sitting on its spawn tile, but by hour 1 the dawn pair has walked off to
        # the fields, which frees `(5,4)` and `(4,5)` again. Assuming otherwise reported `(5,5)` as the
        # next landing square from hour 1 onward and refused to hire for the rest of the day -- crew
        # collapsed to two hands and 70 unit-turns a day against the tape's 208, measured, far worse
        # than the flat cap it replaced.
        #
        # The only bad tile is one with no unlocked orthogonal neighbour to step out to. On one quadrant
        # that stops at 2, as the old flat cap did; on two or more it stops at nothing, because the first
        # parcel unlocks NE at `(5,4)` and that is `(5,5)`'s way out.
        # ------------------------------------------------------------------ PINNED, day 4
        # The schedule row says 8 and the tape sends all 8 at hour 0, so this is not a guess: the
        # crew is held at the known-correct value to take it out of the diff. `unit-turns` on day 4
        # goes 184/208 -> 208/208. Everything still differing on day 4 is therefore NOT the crew.
        #
        # The drip below is left alone on every other day because it is what makes days 0-3 exact --
        # hires land better spread over three hours than all in one, since `_spawn_hand` reads
        # occupancy at the moment each HIRE settles and by hour 1 the dawn pair has walked off.
        HIRE_PINNED_DAY = 4
        if HIRE_FIRST and day == HIRE_PINNED_DAY and hour == 0:
            for _ in range(int(row.get("hands", 0) or 0)):
                orders.append(["HIRE"])
                state["hired"] += 1
        elif HIRE_FIRST:
            target = int(row.get("hands", 0) or 0)
            if state["hired"] < target and hour < 8:
                shed_tiles = R.shed_access_tiles()
                occ = {t: 0 for t in shed_tiles}
                for pos in units:
                    if tuple(pos) in occ:
                        occ[tuple(pos)] += 1
                for _ in range(target - state["hired"]):
                    x, y = min(occ.items(), key=lambda kv: (kv[1], shed_tiles.index(kv[0])))[0]
                    walled = not any(0 <= b < len(tiles) and 0 <= a < len(tiles[0])
                                     and tiles[b][a] != "LOCKED"
                                     for a, b in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)))
                    # A walled-in hand is stuck, not useless: it spawns ON a shed-access tile, and
                    # PICKUP and DROP test shed-adjacency only, so it can load and unload all day. It
                    # cannot BUILD and cannot walk. Refusing the hire outright cost -17 hand-turns a
                    # day while we owned one quadrant, and the tape takes all seven and uses the stuck
                    # ones as shed loaders. `_hire_cost` is per-DAY, so the crew price is unchanged.
                    # **Skip the walled slot, do not stop hiring.** Of the four shed-access tiles only
                    # `(5,5)` is genuinely walled while we own NW alone: `(5,4)` and `(4,5)` both have
                    # `(4,4)` as an unlocked neighbour and step out fine. The spawn order for seven
                    # hires is `(5,4) (4,5) (5,5) (4,4) (5,4) (4,5) (5,5)`, so only the 3rd and 7th are
                    # stuck -- and `break` threw away hires 3 to 7, four of which were perfectly good.
                    # That is what forced the old two-a-turn dribble and cost -17 hand-turns a day.
                    if walled and not HIRE_ONTO_LOCKED:
                        occ[(x, y)] += 1     # this slot is taken; the NEXT hire lands elsewhere
                        continue
                    occ[(x, y)] += 1
                    orders.append(["HIRE"])
                    state["hired"] += 1

        # **Land: the schedule's day is a FLOOR, and the agent buys the first turn it can pay.** The tape
        # takes the $2,000 parcel at day 10 hour 20, after selling all day. Ordering on a fixed hour lost
        # it silently and cost 25 tiles for the rest of the season.
        owned = len(unlocked) - 1
        if owned < len(LAND_PRICES):
            need_by = None
            run = 0
            for d in sorted(sched):
                run += int(sched[d].get("land", 0) or 0)
                if run > owned:
                    need_by = d
                    break
            # **The bank at the start of the turn is not the bank the parcel is paid from.** See
            # `test_a_land_buy_may_be_funded_by_the_same_turns_sales`. Every SELL queued above sits in
            # an earlier order slot and settles first, so the tape takes the day-4 parcel at hour 22
            # on a bank of $718. Reading `money` alone we sat on $778 at that same hour and slipped
            # the parcel to day 5, opening day 5 on one quadrant against his two.
            if need_by is not None and day >= need_by and money + pending >= LAND_PRICES[owned]:
                orders.append(["BUY_LAND"])
                money -= LAND_PRICES[owned]
            # **Do NOT reserve the parcel by starving everything else.** Tried: once a parcel is
            # overdue, zero the spendable bank so nothing cheaper can outbid it. On the original
            # schedule that was +$895; on Seb's plan, where the parcel stays overdue for ten days, it
            # took the season from $59,816 to **$2,345 with a $0 minimum** -- the farm cannot buy feed,
            # so the herd starves and there is never any revenue to buy the land with either.
            #
            # The land is late because the farm is poor, not because the land is outbid. Reserving
            # treats the symptom and removes the only mechanism that could fix the cause.

        # Animals: only when the bank covers the cost, so the purchase can never silently no-op.
        # **Buy against the CUMULATIVE target, not today's row.** `animals_bought` is a per-day figure and
        # `ordered` resets every dawn, so a purchase that failed on a thin bank was never retried. Measured
        # per turn on the winner's schedule: days 8-10 failed on $2-$38, and from day 11 the schedule's rows
        # are empty -- so the agent sat on $8,259 from day 12 to the end of the season and never bought
        # another animal. 5 pens and 2 animals against a target of 14, which is why every animal figure was
        # ~21% of the tape's while CARE and fertilizer collection were already at 100% of animal-days.
        want_total = collections.Counter()
        for dd in sorted(sched):
            if dd <= day:
                for a, qty in (sched[dd].get("animals_bought") or {}).items():
                    want_total[a] += int(qty)
        for a, qty in want_total.items():
            if a not in R.ANIMALS:
                continue
            # **Compare a PURCHASE target against PURCHASES MADE.** `want_total` is what the schedule
            # says to buy, so the only correct counter is how many we have bought. It used to compare
            # against livestock HELD -- alive plus shed plus carried plus bought -- which counted every
            # living animal twice and bought roughly half the herd the schedule asked for.
            #
            # Counting holdings has a second, worse reading: it turns the line into "replace anything
            # that escapes". Measured, that is a $47,933 mistake. Both arms collapsed -- the greedy from
            # 45% of the tape to 8% -- because replacing an animal you cannot feed is a deterministic
            # $400-$500 loss (`kaggriculture.py:786`), and it repeats every two days until the bank is
            # empty. PLACE went 12 -> 61 a season and the money went with it.
            #
            # `bought` never being decremented is therefore the correct behaviour, not a leak: a failed
            # order does not increment it (the `money >=` test guards that), so a purchase blocked by a
            # thin bank is still retried, while one that succeeded and then starved is not repeated.
            # **An animal outranks the marginal hire.** Only ten market orders survive the turn
            # (`orders[:10]`), and on day 4 the pinned block sends eight HIREs alongside two SELLs, so
            # the day's COW was silently truncated away and went in at hour 1 instead of hour 0. It
            # therefore reached the shed at hour 2, one turn after the crew-change replan, and no
            # further replan ran until a unit fell idle at hour 10 -- by then the budget was 13 and
            # the far pen plus the walk home no longer fit. It sat in the shed to dusk.
            #
            # A hire deferred an hour costs nothing: `hires_today` is a per-DAY counter, so the
            # fibonacci price is the same at hour 1, and the hand simply starts an hour later. A
            # placement deferred loses the feed and the care with it.
            for _ in range(max(0, qty - state["bought"][a])):
                if money < R.ANIMALS[a]["cost"]:
                    continue
                if len(orders) >= (10 if ANIMAL_OVER_HIRE else 8):
                    if not ANIMAL_OVER_HIRE:
                        continue
                    last = next((i for i in range(len(orders) - 1, -1, -1)
                                 if orders[i][0] == "HIRE"), None)
                    if last is None:
                        continue
                    orders.pop(last)
                    state["hired"] -= 1
                orders.append(["BUY_ANIMAL", a, 1])
                state["bought"][a] += 1
                money -= R.ANIMALS[a]["cost"]

        # **Seed against the PINS, not today's row.** A planting deferred because the ground or the bank
        # was not ready still needs its seed on the day it finally happens, and the pins are the only
        # record of what is still outstanding. Falls back to the row when the pins are not in play.
        want_seed = collections.Counter()
        if router:
            want_seed.update(v[1] for v in state["pins"].values() if v[0] == "PLANT")
        else:
            want_seed.update({c: int(q) for c, q in (row.get("seeds") or {}).items()})
        for crop, qty in want_seed.items():
            short = int(qty) - int(seeds.get(crop, 0)) - state["ordered"][("seed", crop)]
            if short > 0 and len(orders) < 9:
                orders.append(["BUY_SEED", crop, short])
                state["ordered"][("seed", crop)] += short

        # Feed: one wheat per animal per day, BOUGHT. A wheat tile yields six units and sits on ground
        # worth far more as melon, so growing feed is a bad trade.
        # Count wheat a unit is CARRYING as stock. The router draws a whole day's feed in one PICKUP, so
        # the shed reads empty while the crew holds plenty, and buying against the shed alone re-bought
        # the same feed every day.
        # **TRIED and REVERTED: counting wheat standing ripe in our own field as stock.** The waste it
        # targets is real -- we bought five wheat on Seb's day 4, a day whose HARVEST of 14 wheat is
        # identical in both columns, so ~$300 went on feed we already owned. But owned is not
        # AVAILABLE: standing wheat needs a HARVEST, a DROP and a walk, and most of the season's wheat
        # is still growing. Counting it silences the feed order and the herd starves. Twelve seeds at
        # weedSpawnChance 0.005: our schedule $118,761 -> $87,403, Seb's $92,773 -> $54,419. The feed
        # chain needs stock it can pick up THIS turn, which is the shed and the crew, and nothing else.
        # **Wheat standing RIPE in the field is stock; wheat still growing is not.** That is the whole
        # distinction, and the pinned negative directly above is about the second kind. A tile with
        # accrued `yield_units` is one HARVEST from the hand -- `crop_ops` already offers HARVEST on
        # exactly these tiles and the tape spends the day taking them. Measured on Seb's tape, seed 11,
        # day 4: his row is `buys: {}` and he buys no wheat at all, covering seven animals out of a
        # fourteen-tile harvest, while we bought seven at $33:
        #
        #     hr0   bank 484   HIRE x8 ($54) + BUY_PRODUCT WHEAT 7 ($231)  ->  199
        #     hr17  the $400 COW first becomes affordable, off the day's sales; never placed
        #           place 0/1, feed 6/7, care 6/7
        #
        # The $231 is the entire reason the cow is unaffordable at dawn.
        # The same turn's PICKUPs are in neither `shed` (already decremented) nor `invs` (read
        # before the unit phase), so without the draw this under-counts and over-buys: day 5 sells 17,
        # the shed reads 6 against a real 10, and the top-up orders 8 where the tape orders 4.
        on_hand = int(shed.get("WHEAT", 0)) + ripe_wheat + sum(
            collections.Counter(iv).get("WHEAT", 0) for iv in invs) + max(
            0, int(shed_before.get("WHEAT", 0)) - int(shed.get("WHEAT", 0)))
        # **Buy two days, not one.** `alive` is the day's CONSUMPTION, and ordering exactly the
        # consumption leaves no slack anywhere in shed -> PICKUP -> walk -> FEED. Measured over thirty
        # days: `FED 291 against the tape's 319`, `CARE 290 against 308`, 315 animal-days against 325,
        # and 227 wheat-unit-days in the shed against the tape's 990 -- it runs a buffer of more than
        # two days per animal. Wool realises an identical price in both runs ($236 against $234) and we
        # still bank $10,575 less of it, so the shortfall is animal-days not worked, not price.
        # **Buy what the bank covers, not all-or-nothing.** `money >= 60 * short` cancelled the WHOLE
        # order when it could not pay for it, so a thin bank fed nothing at all. Measured on Seb's day 1
        # with four animals and an empty shed: the order is eight wheat, needs $480, the bank held $189,
        # and we bought ZERO -- FEED ran 3 against his 5 while his shed carried wheat all afternoon.
        # Protecting $189 by starving four animals is the wrong trade twice over: an escape is a
        # deterministic $400-$500 write-off (`kaggriculture.py:786`) and a fed animal produces today.
        # `ordered` accumulates, so the balance is retried on later turns as the day's sales land.
        # **Budget at the LIVE quote, not a hardcoded $60.** WHEAT's `I0` is 10,000 against a book that
        # opens at exactly 10,000, so its price runs from $25 at the season's open toward $125 as the
        # shops drain it (`kaggriculture.py:177`). A flat $60 is wrong in both directions at once: it
        # under-buys 2.4x on an open book -- $300 buys twelve wheat at $25 and the guard allowed five --
        # and over-orders 2x on a drained one, where the surplus silently fails to fill.
        #
        # **Keep the throttle the wrong price was applying by accident.** Feed is a recurring daily
        # cost; seed, pens and land are the one-offs that compound. On a cheap book the true quote lets
        # the whole bank go on two days of feed, and twelve seeds at weedSpawnChance 0.005 say that is
        # worse than being throttled: live quote alone took our schedule $118,761 -> $112,913. Half the
        # bank, at the right price, is $119,281 and takes Seb's plan $92,773 -> $96,064.
        quote = int(((obs.get("market") or {}).get("prices") or {}).get("WHEAT", 60)) or 60
        # **Sizing this order is not the lever; the number of orders is.** Feeding the SCHEDULED herd
        # rather than the living one (`max(alive, cumulative animals_bought through day+1)`) was tried
        # here and made day 1 worse, not better: seed 11, ours minus tape, WHEAT -13 -> -15 with the
        # bank $124 HIGHER, i.e. the bigger order filled less. The reason is one line further out --
        # every order this agent places lands at hour 0 or 1 and then the market half is silent for
        # 22 hours, so a single 8-unit block walks `market_price` up the curve inside one order. The
        # tape places sixteen separate WHEAT buys of 1-6 across h1-h22, interleaved with ten sells,
        # and the shops restock every 4 steps so the book recovers between them. Fix the cadence
        # before touching the size.
        #
        # **The schedule's own `buys` row was never read.** Wheat came only from the herd formula above,
        # so day 0 bought `FEED_DAYS * alive` as the herd grew -- 2, then 2, then 1, then 1 = 6 -- while
        # the row asks for 8 and the tape takes exactly 8. Same bug class as `sells`: a row the executor
        # simply ignores. Measured on Seb's tape, seed 11, day 0:
        #
        #     tape   1 wheat at hours 5, 7, 9, 11, 12, 14, 17, 19   = 8, one per order
        #     ours   2 at hr3, 2 at hr7, 1 at hr14, 1 at hr22       = 6, in blocks
        #
        # The row is the day's target and the herd formula is a FLOOR under it, never a ceiling -- a
        # herd bigger than the schedule planned must still eat. `BUY_DRIP` meters it one unit per turn,
        # which is the cadence the comment above asks for: `market_price` moves per unit inside a single
        # order, and the shops restock every 4 steps, so eight orders of 1 clear cheaper than one of 8.
        wanted = int((row.get("buys") or {}).get("WHEAT", 0) or 0)
        owed = wanted - state["ordered"][("buys", "WHEAT")]
        # **The drip meters the schedule top-up; it NEVER bounds what the herd must eat.** That is the
        # whole difference from `FEED_ORDER_CAP`, which capped the herd's own need at 4 and starved a
        # 19-animal herd from day 15. The herd floor goes out at full size in one order; only the part
        # of the row above that floor is spread across the day.
        herd = FEED_DAYS * alive - on_hand - state["ordered"][("feed", "WHEAT")]
        short = max(herd, min(max(0, owed), BUY_DRIP))
        short = min(short, int(money * 0.5 // quote))
        if (alive or owed > 0) and short > 0 and len(orders) < 9:
            orders.append(["BUY_PRODUCT", "WHEAT", short])
            state["ordered"][("feed", "WHEAT")] += short
            state["ordered"][("buys", "WHEAT")] += short
            # Debit at the price we just QUOTED, not the old hardcoded $60. Charging $60 for wheat
            # bought at $25 understates the running bank by $35 a unit, and every later order on the
            # same day -- seed, animals, the second feed top-up -- is sized against that wrong bank.
            money -= quote * short

        if not HIRE_FIRST:
            # Hire TWO a turn. `_spawn_hand` picks by occupancy when the HIRE settles, so a third order in
            # one turn puts a hand on `(5,5)` in SE with both neighbours locked, unable to move all day.
            # **Count ORDERS issued today, not orders plus hands.** `have = len(units) - 1 + hired` counted
            # every landed hire twice -- once in `hands` and once in `hired` -- so a target of 4 was
            # reported met at 2 and the crew never grew. Hands are dismissed nightly and `hires_today`
            # resets with them, so the orders issued today are exactly the crew we should end up with.
            target = int(row.get("hands", 0) or 0)
            if state["hired"] < target and hour < 8:
                for _ in range(min(2, target - state["hired"])):
                    orders.append(["HIRE"])
                    state["hired"] += 1

        return {"farmer": acts[0] if acts else ["PASS"], "hands": acts[1:], "market": orders[:10]}

    return agent
