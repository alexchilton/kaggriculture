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
        return [n for n in RT.build_nodes(tiles, day, shed, carried, unlocked, pins)
                if n.tile not in skip]

    # Only units that can legally act are vehicles. A boxed-in hand is not a slow vehicle, it is no
    # vehicle at all, and planning work onto it silently deletes that work for the day.
    live = [u for u in range(len(units)) if _mobile(units[u], unlocked)]

    if state["crew"] != len(live) or not routes:
        # A full replan only when the crew changes -- hands are hired through the morning, so the dawn
        # plan genuinely cannot know how many vehicles it has.
        sub = RT.plan_routes([units[u] for u in live], nodes_for(set()),
                             [budget[u] for u in live], depots,
                             {k: load[u] for k, u in enumerate(live)})
        state["routes"] = routes = {u: sub[k] for k, u in enumerate(live)}
        state["crew"] = len(live)
    else:
        idle = [u for u in live if not routes.get(u, {}).get("route")]
        if idle:
            # **Top up the idle units only.** Replanning everybody would break the commitment of a unit
            # already three steps into a tour, which is the thrash the per-turn greedy had.
            busy = {n.tile for u, st in routes.items() if u not in idle for n in st["route"]}
            sub = RT.plan_routes([units[u] for u in idle], nodes_for(busy),
                                 [budget[u] for u in idle], depots,
                                 {k: load[u] for k, u in enumerate(idle)})
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

        # ------------------------------------------------------------------ the return leg
        # A one-way sweep cannot sell what it picks up. Measured against the tape on days 1-3 of seed
        # 11: `EAST 0/10, 0/17, 0/15` and `SOUTH 0/13, 0/14, 0/14` -- our crew never turned back towards
        # the shed on three consecutive days while the tape emitted DROP one to two times daily, so our
        # harvest could not reach the market until `_drop_inventories_to_shed` ran overnight.
        #
        # The turns cost nothing: this only fires once the tour is done and the unit would PASS. DROP
        # moves the WHOLE inventory and DELETES anything the shed has no room for
        # (`kaggriculture.py:333`), so it is refused when the shed is near full.
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
                 pins={}, routes={}, crew=-1, planted=collections.Counter(),
                 ordered=collections.Counter())

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
            # `ordered` is per-day book-keeping for market orders that must happen ONCE, not once per
            # turn. Without it the agent re-issued the day's animals and seed on all 24 turns -- day 0
            # bought four animals at turn 0 and four more at turn 1 until the bank was empty, which is why
            # it reached day 1 on $61 and could then never afford a hand again.
            state.update(day=day, assigned={}, hired=0, ordered=collections.Counter(), tour={},
                         routes={}, crew=-1)          # `pins` and `planted` survive the night by design

        units = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]

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
                have = max(0, have - min(4, want))
            # **Never sell the herd's feed.** WHEAT is both a crop we grow and the feed we buy, and the
            # sell list dumps whatever the shed holds. Measured per turn on day 13 with eleven animals:
            #     h0  BUY_PRODUCT WHEAT 11   shed 0 -> 11
            #     h1  SELL        WHEAT  6   shed 11 -> 0
            # every day, all season, which is why `shed WHEAT` read 0 at midday on all thirty days while
            # the bank climbed to $85,000 and the herd decayed from eleven animals to four. Only the
            # surplus above one wheat per animal may go.
            if prod == "WHEAT":
                have = max(0, have - FEED_DAYS * alive)
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
            if need_by is not None and day >= need_by and money >= LAND_PRICES[owned]:
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
            for _ in range(max(0, qty - state["bought"][a])):
                if money >= R.ANIMALS[a]["cost"] and len(orders) < 8:
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
        on_hand = int(shed.get("WHEAT", 0)) + sum(collections.Counter(iv).get("WHEAT", 0)
                                                 for iv in invs)
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
        short = FEED_DAYS * alive - on_hand - state["ordered"][("feed", "WHEAT")]
        short = min(short, int(money // 60))
        if alive and short > 0 and len(orders) < 9:
            orders.append(["BUY_PRODUCT", "WHEAT", short])
            state["ordered"][("feed", "WHEAT")] += short
            money -= 60 * short

        # Hire TWO a turn. `_spawn_hand` picks by occupancy when the HIRE settles, so a third order in one
        # turn puts a hand on `(5,5)` in SE with both neighbours locked, unable to move for the whole day.
        # **Count ORDERS issued today, not orders plus hands.** `have = len(units) - 1 + hired` counted
        # every landed hire twice -- once in `hands` and once in `hired` -- so a target of 4 was reported
        # met at 2 and the crew never grew. Hands are dismissed nightly and `hires_today` resets with them,
        # so the orders issued today are exactly the crew we should end up with.
        target = int(row.get("hands", 0) or 0)
        if state["hired"] < target and hour < 8:
            for _ in range(min(2, target - state["hired"])):
                orders.append(["HIRE"])
                state["hired"] += 1

        return {"farmer": acts[0] if acts else ["PASS"], "hands": acts[1:], "market": orders[:10]}

    return agent
