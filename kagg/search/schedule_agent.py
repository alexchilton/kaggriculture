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

from . import routines as R

TPD = R.TURNS_PER_DAY
SHED = set(R.shed_access_tiles())
SPAWN = tuple(R.SPAWN)
STEP = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
CROP = R.CROP_TABLE
LAND_PRICES = R.LAND_PRICES

#: Task priority. Pen work first because it is nearly free -- the herd lives on the shed cells, so FEED,
#: CARE and COLLECT_FERTILIZER cost no walk -- and because two missed feeds and the animal is gone
#: outright (`kaggriculture.py:786`). A thirsty tile next: two dry days makes it a weed, and weeded ground
#: refuses PLANT until someone digs it, so the tile is dead for the season.
RANK = dict(FEED=0, CARE=1, COLLECT_FERTILIZER=2, WATER_THIRSTY=3, HARVEST=4,
            PLACE=5, BUILD=6, WATER=7, FERTILIZE=8, PLANT=9, DIG=10)


def _owned(tile, unlocked):
    return R.quadrant_of(tile[0], tile[1]) in unlocked


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


def make_agent(schedule, me=0):
    """`agent(obs, config) -> action`. Holds only which tile each unit is working, and re-reads the rest."""
    sched = {int(k): v for k, v in schedule.items()}
    state = dict(assigned={}, hired=0, day=-1, tour={}, bought=collections.Counter())

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
            state.update(day=day, assigned={}, hired=0, ordered=collections.Counter(), tour={})

        units = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]

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
        # SELL first: the proceeds have to be in the bank before anything below spends them, and that
        # ordering is exactly what decided whether BUY_LAND cleared at all.
        for prod in ("MELON", "WOOL", "MILK", "STRAWBERRY", "FERTILIZER", "WHEAT"):
            have = int(shed.get(prod, 0))
            # **Hold back a few fertilizer.** Applied to a watered, producing tile it doubles the yield --
            # a strawberry tile is 4 units at $120, so doubling beats the $100 the unit sells for. Dumping
            # the whole shed every turn is why FERTILIZE never fired at all.
            if prod == "FERTILIZER":
                have = max(0, have - 4)
            n = min(have, int((row.get("sells") or {}).get(prod, 0)))
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
            # Everything we already have of this animal: alive, in an empty pen's slot, in the shed, in a
            # hand, or ordered earlier this season.
            alive_a = sum(1 for r in tiles for c in r
                          if isinstance(c, dict) and c.get("animal") == a)
            held = (alive_a + int(shed.get(a, 0))
                    + sum(collections.Counter(iv).get(a, 0) for iv in invs)
                    + state["bought"][a])
            for _ in range(max(0, qty - held)):
                if money >= R.ANIMALS[a]["cost"] and len(orders) < 8:
                    orders.append(["BUY_ANIMAL", a, 1])
                    state["bought"][a] += 1
                    money -= R.ANIMALS[a]["cost"]

        for crop, qty in (row.get("seeds") or {}).items():
            short = int(qty) - int(seeds.get(crop, 0)) - state["ordered"][("seed", crop)]
            if short > 0 and len(orders) < 9:
                orders.append(["BUY_SEED", crop, short])
                state["ordered"][("seed", crop)] += short

        # Feed: one wheat per animal per day, BOUGHT. A wheat tile yields six units and sits on ground
        # worth far more as melon, so growing feed is a bad trade.
        alive = sum(1 for r in tiles for c in r if isinstance(c, dict) and "animal" in c)
        short = alive - int(shed.get("WHEAT", 0)) - state["ordered"][("feed", "WHEAT")]
        if alive and short > 0 and len(orders) < 9 and money >= 60 * short:
            orders.append(["BUY_PRODUCT", "WHEAT", short])
            state["ordered"][("feed", "WHEAT")] += short

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
