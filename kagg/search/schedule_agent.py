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
import itertools
import json
import pathlib

from . import cover as DP
from . import melon_branch as _MB
from . import q4_branch as _Q4
from . import router as RT



#: Turns remaining at or below which the walk back to the shed stops being charged. See `_solve`.
#:
#: **99 as of 2026-08-11 -- i.e. the closing trip is never charged.** The tape makes 10 DROPs across
#: d0-d16 and we made 63: Victor's produce reaches the shed on the overnight sweep
#: (`_drop_inventories_to_shed`, `kaggriculture.py:812`), which is free, and ours paid a walk home
#: for it. On the Victor grid, seed 11, against the old value of 2:
#:
#:     weeds d16   9 -> 5        money d16   17,649 -> 21,242
#:     water rose on five of the last six days; move fell 1494 -> 1474
#:
#: **The DROP count barely moves in any arm, and that is the thing to remember.** Rules 2 and 3 of
#: `cover.materialise` both emit `Depot(drop=True)` and substitute for each other -- kill the mid-day
#: ferry and the closing trip collects the goods, kill the closing trip and the ferry fires. Measured:
#: `DELIVER_MIN = inf` gave 64 drops, this gives 63, `WALK_THE_LOAD_HOME = False` gave 59, against a
#: baseline of 63. Any future attempt to cut the ferrying has to move both rules or neither.
DELIVER_CUTOFF_TURNS = 99

#: Days the closing walk home is planned anyway, whatever `DELIVER_CUTOFF_TURNS` says.
#:
#: **The reason 99 gives for never charging the trip does not hold on the melon flush.** It is that
#: "Victor's produce reaches the shed on the overnight sweep, which is free" -- true of money at
#: season end, false of a product whose price is a race. `_drop_inventories_to_shed`
#: (`kaggriculture.py:812`) banks the load at the ROLLOVER, which is after the market has closed for
#: that day. No shop stocks melon and the town takes one unit a day, so the book does not recover
#: overnight; a day late is a day of the opponent's own flush walking the price down ahead of us.
#:
#: Measured on seed 11 against the kawashigi tape. All thirteen ripe melon tiles get a HARVEST job
#: and all thirteen are seated -- the harvest is not the defect. No tour contains a shed stop:
#:
#:     u0   16/24  (3,2)W (3,1)WH (2,1)WH (1,1)WH (1,0)WH       ends at (1,0), 8 turns spare
#:     u8   23/23  (2,4)FCC (0,3)WH (0,2)WH (0,1)WH (0,0)WHPW   ends at (0,0), none spare
#:     u10  23/23  (4,3)FCCH (4,2)FCC (4,1)PW (4,0)WH (3,0)WH (2,0)WH
#:     u3    0/23  (idle)          u6   0/23  (idle)
#:
#:     d10 h00-h23   shed 0 all day, hands 0 -> 66, book 272 -> 246, nothing offered
#:     d11 h00       shed 72, SELL 60 at 246, then SELL 12 at 189
#:
#: Sixty-five melons carried to dusk while two hands hold 46 unused turns. `plan` appends the
#: closing trip out of turns the tour did NOT spend, so it can only ever use slack -- u0's eight
#: spare turns against a seven-step walk to the shed.
#:
#: **d10 ONLY, and d11 was measured OUT.** The first version was `(10, 11)` on the reasoning that
#: the flush spans both days. It does not: with d10 delivering, the whole tail is already in the shed
#: at d11 h00 and sells there, so d11 has nothing left to walk home -- and turning `deliver` on for it
#: put FOUR of its tours over budget, 29/26/25/24 turns against 23. That regression passed unnoticed
#: because the test asserted on d10 alone; it is now season-wide
#: (`tests/test_a_day_is_packed_against_the_tour_it_will_walk.py`).
#:
#: **One day, not a lower cutoff.** `DELIVER_CUTOFF_TURNS` was tuned on the victor grid across
#: d0-d16 and lowering it would reopen every one of those days. This is the smallest change that
#: reaches the flush, and d0-d9 cannot move under it by construction.
#:
#: **d29 added 2026-08-15, for a different reason: on the last day the free drop is too late.**
#: `_end_of_day` calls `_drop_inventories_to_shed`, so on every ordinary day a carried load reaches
#: the shed for nothing -- which is why カワシギ emits five DROPs in a whole season against 389
#: harvests. After d29's last turn that drop still runs, but there is no turn left to sell into, and
#: `_commit_unit` refuses a SELL unless the goods are already in `private["shed"]`. So produce held
#: at the close is not carried over, it is discarded.
#:
#: Measured at the final step of d29 on the kawashigi grid, seed 11:
#:
#:     US    carried and LOST  58 units  ~$1,430  {WHEAT 34, MILK 12, FERTILIZER 12}
#:     TAPE  carried and LOST   7 units    ~$245  {WHEAT 7}
#:
#: and the tape spends NINE DROPs on d29 against our two. That is the whole difference: it walks its
#: load in, we finish the season holding it.
#:
#: **The first attempt at (10, 29) recovered 7 of 58 units and was reverted**: a solved route
#: stores work stops, `plan` appends the closing walk out of turns the tour did not spend, and with
#: FEED/CARE still planned d29 had no slack to append into. `NO_UPKEEP_ON_THE_LAST_DAY` now frees
#: those turns first, which is what this flag was waiting for.
WALK_THE_LOAD_HOME_DAYS = (10, 29)



#: The last day whose carried load is banked overnight; d29's own drop lands after the final turn.
LAST_FREE_DROP_DAY = 28


def _at_risk_tiles(tiles, day=None):
    """Tiles where skipping today's work destroys something tonight. Read off the board, not priced.

    `consecutive_unfed`/`consecutive_unwatered` are already 1 -- one more missed day and the animal
    walks off or the tile weeds. A pen fed yesterday, or a tile watered yesterday, can slip a day for
    free, which is precisely how the tape feeds 16 of 19 pens on day 19 and loses nothing.

    The d28 "bank the field" branch that used to sit here was dead -- gated on a local hardcoded
    False, pointing at a `BANK_THE_FIELD_ON_D28` constant that no longer existed. It measured a null
    because d28 is a SOLVED day with slack, so promoting a ripe tile into the at-risk set changed no
    route. The deadline is real but it belongs in the PRICE, not in this set: see the d28 branch in
    `router.animal_ops`.
    """
    out = set()
    for y, row in enumerate(tiles):
        for x, cell in enumerate(row):
            if not isinstance(cell, dict):
                continue
            if cell.get("animal") and cell.get("consecutive_unfed", 0) >= 1:
                out.add((x, y))
            elif (cell.get("kind") == "PLANT"
                    and cell.get("consecutive_unwatered", 0) >= 1):
                out.add((x, y))
    return out


#: Stop tending a crop that cannot produce again before the season ends.
#:
#: Measured across 29 independent same-board days (`data/logs/all30_same_conditions.log`): the tape
#: lets 41 crops die of thirst on days 21-28 against our 14, and that is not incompetence -- a tile
#: that cannot reach another production day before day 29 is worth nothing, so every turn spent
#: watering it is stolen from a harvest that still pays. He stops; we keep watering.
LATE_SEASON_TRIAGE = True

#: Last day of the season, so a crop needs its production day at or before this to be worth a turn.
LAST_DAY = 29


def _pointless_tiles(tiles, day, plants_left):
    """Tiles whose work cannot pay back before the season ends. Dropped from the job list entirely.

    Two rules, both read off the crop table and the board rather than priced:

      - a PLANT holding nothing that cannot reach another production day by `LAST_DAY`
      - a WEED, when the schedule has no plantings left to put in the ground it would free

    Anything already holding `yield_units` is NEVER dropped: that is standing produce and it wants a
    HARVEST, not abandoning.
    """
    out = set()
    for y, row in enumerate(tiles):
        for x, cell in enumerate(row):
            if not isinstance(cell, dict):
                continue
            kind = cell.get("kind")
            if kind == "WEED":
                if not plants_left:
                    out.add((x, y))
                continue
            if kind != "PLANT" or not LATE_SEASON_TRIAGE:
                continue
            if int(cell.get("yield_units", 0)) > 0:
                continue                      # standing produce: harvest it, never abandon it
            info = RT.CROP.get(cell.get("crop"))
            if not info:
                continue
            # The crop table's keys are `first` and `max_day` -- NOT `first_yield_day` /
            # `max_yield_day`, which is what an earlier version of this guessed at and why it
            # abandoned every wheat tile past day 4.
            planted = int(cell.get("planted_day", day))
            if LAST_DAY - planted < info["first"]:
                out.add((x, y))               # cannot reach its first yield before the season ends
            elif not info["ongoing"] and day - planted > info["max_day"]:
                out.add((x, y))               # one-shot past its window: from here it only decays
    return out


#: Whether a day whose shopping list the bank cannot cover pulls its selling forward.
#:
#: **Alex's rule, and it is the general condition the hard-coded `DELIVER_REPLAN_DAYS = (6,)` was
#: standing in for:** if the schedule says buy things we do not have the cash for, harvest early and
#: get the produce to the shed, because the purchases are queued behind that money.
#:
#: Seed 11 day 6 is the case it was found on and it is not a special one. The row reads
#: `money_dawn: 15.0`, `BUY_ANIMAL COW 2` ($800), fourteen seeds and eight hires -- roughly $2,000 of
#: intent against fifteen dollars -- and `sells: {WOOL: 12}`, which is where the $2,000 is meant to
#: come from. The tape harvests at h0, drops and sells six at h2, harvests again at h2 and sells the
#: last six at h5; both cows are funded by hour five. We harvested at h4 and h10 and carried ten wool
#: to h19 with the bank on $20 all day, because a covering planner that counts every job as 1 has no
#: reason to take a HARVEST early, and the cheapest tour visits the far pens last.
#:
#: So on a short day the wool is not one job among forty -- it is the day's first constraint, and it
#: gets the treatment `at_risk` feeds get: covered first, and delivered as soon as it is in hand
#: rather than batched to `DELIVER_MIN`.
#:
#: **This is a rule read off the schedule, not a price.** It asks one question with a yes/no answer --
#: does today's shopping list exceed the bank -- from numbers that are all on the board at dawn. No
#: dollar figure enters the routing.
FUND_THE_DAY_WHEN_SHORT = True



#: Whether the DAWN plan routes the hands the day is about to hire, instead of waiting for them to
#: appear and rebuilding the plan around them.
#:
#: OFF restores the crew-change replan exactly: hour 0 is planned for the pre-hire crew, the hands
#: land in hour 0's market phase, and hour 1 sees `len(live)` jump and throws the plan away. That is
#: two plans a day minimum -- measured d0 at h1 AND h3, d1-d6 at h1 -- and the second one is what
#: actually covers 23 of the 24 hours.
PLAN_THE_CREW_THAT_ARRIVES = True

HARVEST_WHAT_YOU_STAND_ON = True

#: Whether a hand crossing a pen it has already fed today also CAREs it.
#:
#: **OFF, and measured.** The arithmetic is right -- one turn, no item, one extra unit of product on
#: the next production day -- and it still loses, because a care taken on the way past is a turn the
#: day had already promised to something else. Every hand crosses the pen on the shed tile, so the
#: rule fires constantly:
#:
#:                    d0    d1    d2    d3    d4    d5    d6
#:     care  ON      5/4   6/5   8/5   8/6  10/7   9/7   5/8
#:     care  OFF     4/4   5/5   5/5   6/6   6/7   7/7   7/8
#:
#: We overshoot the tape on five days and break day 0, which was exact. Day 6 pays for it hardest --
#: `feed` 7/8 -> 4/8 and `buy_product` 7/9 -> 1/9 -- so the turns come out of feeding and trading,
#: which is the wrong trade for one unit of product tomorrow.
#:
#: The `d4 care 6/7` this was written for is real, but it is ONE care, and this buys it by spending
#: nine others. A rule that fires only where the hand has slack would be a different arm.
CARE_WHAT_YOU_STAND_ON = True

#: On the LAST day, a loaded hand abandons what is left of its route at the last hour that still
#: reaches the shed. The runtime mirror of `cover.TRIM_HOME_DAYS`: the plan trims tails it can
#: price, but the executor re-derives work at every stop, so a tour runs a turn or two past its
#: costing and the planned walk starts too late -- the d29 trace shows u8 ending the season at
#: (4,3), ONE tile from the shed, holding 11 units. Work given up here would have made produce the
#: close discards anyway. Follows the `NO_UPKEEP_ON_THE_LAST_DAY` master switch.
LAST_DAY_DEADLINE_WALK = True

#: Turns of head start the walk gets, on top of `dist + 1`.
#:
#: **Three, and only one of them is the executor's.** The rule
#: fires on the hour the walk must begin, but the executor re-derives work at each stop and finishes
#: the current one first, so the first step happens the turn AFTER the rule says go.
#:
#: Measured on ladder game `93346440`, d29, our seat. u5 is at (7,1) at h18, five tiles from the
#: depot at (5,4): `need` is 6 and `24 - 18 == 6`, so the old bound fires exactly at h18 -- and the
#: unit does not move until h19 and arrives at h23 with no turn left to DROP:
#:
#:     hr   u4          u5           u7          u8
#:     21   (2,4):3     (7,4):12     (7,4):4     (2,3):11
#:     22   (3,4):3     (6,4):12     (6,4):4     (2,4):11
#:     23   (4,4):3     (5,4):12     (5,4):4     (3,4):11
#:
#: Three hands STAND ON a depot at h23 still holding, and u8 is one tile short. 3+12+4+11 = 30
#: units, the whole of that game's carried total, worth $2,334 at its closing book.
LAST_DAY_WALK_SLACK = 3


def must_walk_home_now(day, hour, pos, held, depots):
    """The last turn a loaded hand can still bank its load: walk `dist`, one turn to DROP, plus slack.

    `_drop_inventories_to_shed` runs after d29's final turn, when the market is gone, so a load
    still in a hand at the close is discarded -- leaving later than this bound loses all of it.
    Every earlier day banks the load in the sweep for free, so this must never fire there.

    The slack is `LAST_DAY_WALK_SLACK`; see there for the trace that sets it.
    """
    if not LAST_DAY_DEADLINE_WALK or not RT.upkeep_buys_nothing(day):
        return False
    if not any(v > 0 for v in (held or {}).values()):
        return False
    need = min(RT.dist(pos, t) for t in depots) + 1
    return (TPD - hour) <= need + LAST_DAY_WALK_SLACK


def _arrivals(units, n):
    """Where the day's `n` hires will land, in the order `farm["hands"]` will hold them.

    `_do_hire` appends `_spawn_hand(farm, board_size)` (`kaggriculture.py:520`): the least-occupied
    shed-access tile, ties broken by the NWSE order of `_shed_access_tiles`, counting the units
    standing there **at the moment that HIRE settles**.

    Several HIREs in one turn all settle. The atomic block runs once per ORDER SLOT, not once per
    turn -- `for i in range(max_len)` at `kaggriculture.py:550` re-enters `_do_hire` for every slot
    that holds one (`:564`), and `order_states[player_id] = None` only clears that slot for the
    market lockstep below it. So a pinned row of eight lands as eight hands in one turn, occupancy
    advancing one hire at a time inside it, and the returned list is exactly the order they are
    appended in -- which makes index `len(units) + k` here the same unit as index `len(units) + k`
    tomorrow morning. That identity is what lets the dawn plan route them.
    """
    tiles = list(R.shed_access_tiles())
    occ = {t: 0 for t in tiles}
    for pos in units:
        if tuple(pos) in occ:
            occ[tuple(pos)] += 1
    out = []
    for _ in range(n):
        t = min(occ.items(), key=lambda kv: (kv[1], tiles.index(kv[0])))[0]
        occ[t] += 1
        out.append(t)
    return out


def _clear_the_spawn_ring(units, unlocked, n):
    """Step the farmer off the spawn ring when doing so saves a hand from the dead corner.

    `_spawn_hand` counts `[farmer] + hands` when it picks the least-occupied shed-access tile, so a
    farmer standing on the ring is not a bystander -- it rotates where every one of the day's hires
    lands. The ring is `[(4,4), (5,4), (4,5), (5,5)]` and, while only the NW quadrant is owned, all
    four orthogonal neighbours of `(5,5)` are locked: a hand that spawns there cannot move, cannot
    work and cannot be walked home, and `_mobile` writes it off for the day.

    Seven hires over four tiles must strand ONE hand there whatever we do -- the tape strands one on
    d4 and its seat reads 0 work / 0 move / 23 idle, same as ours. What is ours to give away is the
    SECOND. With the farmer on `(4,4)` the rotation shifts a step and the 3rd and 7th hires both land
    on `(5,5)`; with the ring clear it is the 4th alone.

    Measured on d4 of `seb1326`, seed 11:

        Seb  farmer (4,3) as the hires settle   (4,4) (5,4) (4,5) (5,5) (4,4) (5,4) (4,5)   1 dead
        ours farmer (4,4), doing a PICKUP       (5,4) (4,5) (5,5) (4,4) (5,4) (4,5) (5,5)   2 dead

    Returns `(move, arrivals)` -- the compass step the farmer must take this turn, or `None` if
    standing still is no worse. The unit phase runs before the market phase (`kaggriculture.py:922`
    then `:928`), so the step lands BEFORE the hires and is what they see.

    The step is only ever taken onto an OWNED neighbour: walking the farmer into a locked quadrant
    would box IT in and trade one dead seat for another.
    """
    here = tuple(units[0])
    stay = _arrivals(units, n)
    if here not in set(R.shed_access_tiles()):
        return None, stay
    lost = sum(1 for p in stay if not _mobile(p, unlocked))
    best = None
    for name, (dx, dy) in STEP.items():
        step = (here[0] + dx, here[1] + dy)
        if not (0 <= step[0] < R.BOARD_SIZE and 0 <= step[1] < R.BOARD_SIZE):
            continue
        if not _owned(step, unlocked):
            continue
        alt = _arrivals([step] + list(units[1:]), n)
        if sum(1 for p in alt if not _mobile(p, unlocked)) < lost:
            best = (name, alt)
            break
    return best if best else (None, stay)


def _hires_this_turn(state, row, day, hour, money, shed=None, prices=None):
    """How many hands the market block below is about to buy. Read by the DAWN PLAN, which has to
    route them, so it must not diverge from what that block actually orders.

    Only the pinned path is modelled, and that is not a simplification: `HIRE_PINNED_DAYS` is every
    day, because the tape hires at hour 0 on every day (`scripts/when_the_crew_arrives.py`). The
    drip path is unreachable and a phantom crew cannot be planned against it anyway -- its whole
    premise is that arrivals are discovered.

    Affordability is checked because `_do_hire` fails SILENTLY when `farm["money"] < cost`
    (`kaggriculture.py:691`), and a hire that never lands leaves its route orphaned: work planned
    onto a unit that does not exist is work deleted, not work deferred.
    """
    if not (PLAN_THE_CREW_THAT_ARRIVES and HIRE_FIRST and day in HIRE_PINNED_DAYS and hour == 0):
        return 0
    want = int(row.get("hands", 0) or 0)
    # `mult * fib(hires_today)`, a per-DAY counter, so the ladder restarts every dawn -- but it
    # restarts at **`_fib(0) = 1`, not 0** (`kaggriculture.py:677`). Seven hires cost `1 1 2 3 5 8 13`
    # = 33. Starting at 0 charged `0 1 1 2 3 5 8` = 20, one position short the whole way up, so on any
    # bank between the two totals this predicted a hand the market phase could not pay for.
    # **The bank this turn's HIRE sees is the dawn bank PLUS what this turn's SELLs raise.**
    #
    # `_process_market` walks a turn's orders in slot order, so the sells queued alongside the hires
    # settle into the bank the hires then spend from. Sizing the crew off `money` alone models the
    # cost of the ladder and not the revenue that pays for it, and the two are in the same turn.
    #
    # Measured on カワシギ's plan, seed 11, d4. The day OPENS on $3 and his row asks for 5 hands.
    # The ladder is 1, 1, 2, 3, 5: against $3 it affords two and stops, so the dawn plan built
    # phantoms for TWO -- `budget [24, 23, 23]` in the day-4 fixture -- while five hands actually
    # landed, funded by that day's $384 of sells. Three real hands then stood with no route, and
    # every op on the day came up short in the same proportion: harvest 3/7, care 3/5, feed 3/5,
    # collect_fert 3/5, and the pen 0/1. A 400-restart seating search reported "no ordering beat
    # the shipped planner" because it was solving for three people.
    #
    # He opens d4 on $1 and hires the same five.
    #
    # Deliberately capped at what the shed can actually deliver: the row is a day TOTAL and
    # `n = min(have, row["sells"][p])` at the emission, so a row asking to sell stock we do not
    # hold raises nothing. Priced at the live quote where one is available, falling back to base --
    # under-estimating here only costs a hand, while over-estimating orphans a route, which is the
    # asymmetry `_do_hire`'s silent failure creates.
    proceeds = 0.0
    for product, qty in (row.get("sells") or {}).items():
        held = int((shed or {}).get(product, 0) or 0)
        n_sell = min(held, int(qty or 0))
        if n_sell <= 0:
            continue
        quote = (prices or {}).get(product) or RT.BASE_PRICE.get(product, 0)
        proceeds += n_sell * float(quote)

    bank, a, b, n = float(money) + proceeds, 1, 1, 0
    for _ in range(want):
        if bank < a:
            break
        bank -= a
        a, b = b, a + b
        n += 1
    return n


def _unwalled_landing_slots(tiles, units, want):
    """How many of the next `want` hires can be issued THIS TURN before one lands walled.

    A PREFIX, not a total, and the difference is the whole point. `_spawn_hand`
    (`kaggriculture.py`) takes the least-occupied shed-access tile, ties broken in
    `shed_access_tiles()` order, occupancy read at the moment each HIRE settles -- and it does NOT
    skip a bad square. With the farmer on `(4,4)` the ring fills `(5,4) (4,5) (5,5) (4,4)`, so on one
    quadrant the walled landing is the THIRD. Counting how many of four are fine gives 3 and still
    hires the stranded one; stopping before it gives 2, and the top-up places the rest on a later
    turn once the crew has walked off the ring and the occupancy has changed.

    A tile is walled when no orthogonal neighbour is unlocked. `tiles` is the LIVE board here, never
    `plan_tiles`: the question is where a hand can walk this turn, and the parcel has not settled.
    """
    shed_tiles = R.shed_access_tiles()
    occ = {t: 0 for t in shed_tiles}
    for pos in units:
        if tuple(pos) in occ:
            occ[tuple(pos)] += 1
    for n in range(int(want or 0)):
        x, y = min(occ.items(), key=lambda kv: (kv[1], shed_tiles.index(kv[0])))[0]
        occ[(x, y)] += 1
        if not any(0 <= b < len(tiles) and 0 <= a < len(tiles[0]) and tiles[b][a] != "LOCKED"
                   for a, b in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))):
            return n
    return int(want or 0)

def _land_this_turn(sched, day, hour, unlocked, money, n_hires, prices=None):
    """The quadrant the market block below is about to buy, or None. Read by the DAWN PLAN.

    Same contract as `_hires_this_turn`, for the same reason and with the same failure mode. The env
    applies unit actions BEFORE the market phase (`kaggriculture.py:922` then `:928`), so a
    `BUY_LAND` emitted at hour 0 settles at the END of hour 0 -- and the day is planned once, at
    dawn. Without this the twenty-five tiles that arrive are invisible to the only plan the day gets.

    Measured on the Victor grid, seed 11, day 10 -- the day his schedule takes the second parcel at
    hour 0 and plants 23 tiles, 18 of them on the new ground:

        plant  ours 1 / tape 23      water  ours 18 / tape 43      idle  ours 128 / tape 78

    on an identical crew of fourteen. `tests/test_the_dawn_plan_owns_the_land_it_buys_today.py` had
    it as `d10 bought ['SW'] and the dawn plan offered no job on it -- 29 jobs planned, all on
    ['NE', 'NW']`.

    **Which parcel is not a guess.** `_do_buy_land` takes `LAND_ORDER[len(unlocked) - 1]`
    (`kaggriculture.py:699-708`), so the name is deterministic from what we already own.

    **CERTAIN, not likely.** `_do_buy_land` returns silently on a short bank, and work planned onto
    ground that never unlocks is work deleted, not deferred -- every op aimed past the border no-ops
    for the rest of the day. So this predicts only from the bank standing at dawn, minus the hire
    bill, because HIRE sits in an earlier order slot than BUY_LAND in the same turn's queue. The
    market block's own test may still buy on `money + pending`, i.e. funded by the day's sales; that
    case is deliberately NOT predicted here. On the Victor schedule that is d6 -- $432 at dawn
    against a $1,000 parcel -- and it stays unplanned, which is the conservative direction.
    """
    if hour != 0:
        return None
    owned = len(unlocked) - 1
    if owned < 0 or owned >= len(LAND_PRICES):
        return None
    # The schedule's `land` day is a FLOOR -- the same running total the market block walks, so the
    # two cannot disagree about whether a parcel is due.
    need_by, run = None, 0
    for d in sorted(sched):
        run += int((sched[d] or {}).get("land", 0) or 0)
        if run > owned:
            need_by = d
            break
    if need_by is None or day < need_by:
        return None
    # `mult * fib(hires_today)` starting at `_fib(0) = 1` -- the same ladder `_hires_this_turn`
    # walks. Charged here because those orders settle first and the parcel is paid from what is left.
    bank, a, b = float(money), 1, 1
    for _ in range(int(n_hires or 0)):
        bank -= a
        a, b = b, a + b
    # **The plan and the buyer must apply the SAME test, or they disagree about the same parcel.**
    # The market block buys on `money + pending` -- the day's own sales settle in earlier order
    # slots, so a parcel is affordable out of revenue that has not landed at dawn. Reading `money`
    # alone here made the dawn plan strictly more pessimistic than the code that does the buying,
    # and Victor's d6 is the gap between them: we take the parcel at h13 on a bank of $53, three
    # hours EARLIER than the tape, and then leave 42 unit-turns idle because the plan that governs
    # the day was built as though the ground were never coming.
    #
    # The revenue is the schedule's own `sells` row at the day's opening prices. That is a forecast,
    # and the docstring above is right that a wrong one orphans routes onto locked ground -- so it
    # is deliberately the row and not a guess at what the shed might yield. The row is the plan's
    # statement of what the day sells; if it does not hold, the day was already wrong.
    revenue = 0.0
    row_sells = (sched.get(day) or {}).get("sells") or {}
    revenue = sum(float((prices or {}).get(p, 0.0)) * int(q) for p, q in row_sells.items())
    if bank + revenue < LAND_PRICES[owned]:
        return None
    return R.LAND_ORDER[owned]


def _days_bill(row):
    """Roughly what today's schedule row intends to spend. Compared against the bank, nothing else.

    Deliberately coarse: the hire ladder is `mult * fib(n)` (`kaggriculture.py:666`) and
    `BUY_PRODUCT` quotes off a live demand curve, so an exact figure is not available at dawn and is
    not needed. The question has a yes/no answer -- is the day asking for materially more than it
    holds -- and animals and land dominate it by an order of magnitude over seeds and hires.

    **The bank it is compared against is OURS, live, not the schedule's.** Every row carries the tape
    author's `money_dawn` (day 6 reads $15.00) and using that would be the wrong number twice over:
    it is a different farm's balance, and by day 6 ours has already diverged from it. The live figure
    is exact, is ours, and needs no field added to the schedule.
    """
    bill = 0.0
    for animal, qty in (row.get("animals_bought") or {}).items():
        bill += R.ANIMALS.get(animal, {}).get("cost", 0) * int(qty)
    # **`RT.SEED_COST`, not `R.CROP_TABLE`.** `CROP_TABLE["MELON"]` is
    # `{'first': 10, 'max_day': 12, 'max_yield': 6, 'ongoing': False, 'interval': 0}` -- it carries
    # growth, not price -- so `.get("seed", 0)` defaulted for every crop and seed contributed exactly
    # $0 to this bill. On Victor's d10 that is $2,730 of a $2,286 total: the row prices below its own
    # seed, `_days_bill_now` reads $1,286 against a $2,125 dawn bank, and the day declares itself
    # funded. `short_of_cash` is what tells the planner to get produce into the shed while the market
    # is open, so it was switched off on the one day in the grid that needed it -- thirty melon in
    # hands from h6 to h20 and four strawberry stops walked past empty.
    #
    # The docstring above is still right that this figure is coarse, but not that "animals and land
    # dominate it by an order of magnitude over seeds": d10's seed is nearly three times its parcel.
    for crop, qty in (row.get("seeds") or {}).items():
        bill += RT.SEED_COST.get(crop, 0) * int(qty)
    for product, qty in (row.get("buys") or {}).items():
        bill += RT.BASE_PRICE.get(product, 0) * int(qty)
    a, b = 1, 1
    for _ in range(int(row.get("hires") or 0)):            # `mult * fib(n)`, mult 1 by default
        bill += a
        a, b = b, a + b
    bill += _land_bill(row)
    return bill


def _land_bill(row):
    """What the row's parcels cost. Split out because they are the one thing NOT bought at dawn."""
    return sum(R.LAND_PRICES[:int(row.get("land") or 0)])


def _days_bill_now(row):
    """What the row spends AT HOUR 0, which is the only figure the dawn bank has to cover.

    `_days_bill` is the day's whole bill and answers a different question. Comparing THAT to the dawn
    bank is what put day 4's delivery deadline at hour 0: the row buys a $400 cow and a $1000 parcel,
    the bank holds $480, and summing them says the day is short by a thousand. It is not short at
    dawn -- the cow, the seven hires and one wheat come to about $461 and fit -- and the parcel is
    bought late, out of the day's own selling.

    The parcel is excluded rather than dated because the agent is never told the hour. `land_turns`
    is in `TAPE_ONLY` and is stripped before the schedule reaches us, so the land block buys on the
    first turn it can pay. An obligation with no due date cannot be a dawn one, and treating it as
    such rushes the whole row to the shed.

    Measured on tape 91422988 day 4: Seb buys his cow at h0 on a $45 bank, holds $12 from h2 to h18
    with nothing due, and funds the parcel at h21 out of the SELLs sitting in earlier order slots of
    that same turn. Nothing about his morning is short of cash.

    This is one slice of `docs/the_day_is_a_cash_ledger.md`.
    """
    return _days_bill(row) - _land_bill(row)


def _solve(units, nodes, budget, depots, carry, supply, at_risk=(), pointless=(), tiles=None,
           wanted=None, fund=False, day=None):
    """One day's assignment, by whichever planner is switched on. Same return shape either way.

    `tiles` feeds the yield prediction and `wanted` today's still-owed SELL row. Together they are
    what lets the shed trip be PLANNED -- the board says which pens are ripe and how much they hold,
    the row says what the market is waiting for, and both are readable at dawn. See
    `cover.materialise`.
    """
    jobs = [j for j in DP.from_nodes(nodes, tiles) if j.tile not in pointless]
    at_risk = set(at_risk)
    owed = collections.Counter({p: q for p, q in (wanted or {}).items() if q > 0})
    # **A pen the row is waiting on offers its HARVEST separately.** See
    # `cover.SPLIT_THE_FUNDING_HARVEST`. One tile's ops are atomic to one hand, which forces a ripe
    # pen's harvest to happen after its feed, care and collect -- the tape puts a second hand on the
    # tile that does nothing but harvest and run the produce to the shed, and that is the only way
    # d8's second cow reaches the market before it closes.
    if fund:
        jobs = DP.split_funding_harvest(jobs, owed)
    for j in jobs:
        if j.tile in at_risk:
            j.at_risk = True
        # See `FUND_THE_DAY_WHEN_SHORT`. A harvest only counts as funding the day if the market is
        # actually waiting for what it yields -- a ripe melon on a day whose row sells no melon pays
        # for nothing today and must not jump the queue.
        if fund and any(owed[p] > 0 for p in j.gives):
            j.funds = True
    # The closing shed trip is planned only while there is time to make it. With two turns or fewer
    # left a hand cannot both work and get back, and the overnight sweep banks the produce anyway --
    # so reserving it there only refuses the last harvest of the day. See `cover.materialise`.
    deliver = max(budget or [0]) > DELIVER_CUTOFF_TURNS or day in WALK_THE_LOAD_HOME_DAYS
    # `day` gates `cover.RESERVE_FROM_DAY`, which must never fire on d0-d9.
    out, _uncovered = DP.plan(units, jobs, budget, depots, carry, supply=supply, deliver=deliver,
                              wanted=owed, rush=fund, day=day)
    return out
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
#: **RAISED 2 -> 4 on 2026-08-08, and the evidence is a COUNT rather than a season total.** Six
#: seeds, seat 0, weeds off, against Seb's tape (`data/logs/feed_days_sweep.log`):
#:
#:     FEED_DAYS     mean $     ESCAPES over six seasons
#:             2     90,396           4
#:             3     94,087           2
#:             4     98,879           0
#:
#: Monotone in both columns, and escapes reaching zero is the part to trust: an escape is
#: irreversible, it costs $400-$500 plus every remaining day of that animal's production, and unlike
#: a bank figure it cannot be an artifact of the market. Held at 0 in the `feed_x_risk.log` 2x2 too.
#:
#: **This is what the tape does.** Seed 11, weeds off: his dawn shed runs 43, 51, 57, 47 wheat
#: against our 15-20, and he buys in BURSTS -- 105 on day 8, 95 on day 19, then nothing at all the
#: next day, which lets the shop's book refill before he draws on it again. He offers 929 wheat
#: across the season to our 405. At `FEED_DAYS = 1` our buffer was effectively ONE day: we bought
#: about seventeen and fed about seventeen, so any hiccup was a missed feed.
#:
#: `FEED_DAYS = 1` was tried in the other direction and measured -$6,236 over twelve seeds, which is
#: presumably why this sat at 2; nothing had ever tried going UP.
FEED_DAYS = 1

#: Days of feed held once the season turns TURN-BOUND. See `feed_days()`.
FEED_DAYS_LATE = 1

#: The day the buffer widens. This is the same hinge the register records for the whole season: up to
#: about here the farm is CASH-bound (dawn bank $28 on day 4, $15 on day 6, land parcels to fund) and
#: after it the farm is TURN-bound, with the bank past $10k and nothing to spend it on but feed.
FEED_DAYS_FROM_DAY = 16


#: **TRIED AND REVERTED 2026-08-10: target the wheat buffer from the SCHEDULE's placement rows.**
#: The idea is right in principle -- the schedule says when pens fill, so tomorrow's feed is
#: knowable tonight -- and it measured WORSE, per-process, 13 losses against 7 and $62,427 against
#: $65,940. Cumulative placements run ahead of the board whenever a placement slips (`place 0/4` on
#: d9/d10), so it buys feed for animals that do not exist. An "arrivals only" variant was worse
#: still. Do not re-derive: the board-read target at `FEED_DAYS = 1` is the measured best.

def feed_days(day):
    """Days of wheat to hold, as a function of the day. One, matching the tape.

    **Measured 2026-08-10 against Seb's own shed.** Reading `private["shed"]` out of his replay, his
    dawn WHEAT equals his PEN COUNT on every day of the season, in both recorded games. He runs a
    one-day buffer and tops it up continuously; the small constant buying and selling is a buffer
    controller, not market timing.

    Ours was 2 early and 4 late, which overshoots then stocks out -- seed 13 held 32 units for 7
    pens on d5 and ZERO on d9, with four animals at `consecutive_unfed >= 1` and two dead. Six
    seeds, whole season:

        FEED_DAYS=2 LATE=4   10 lost   mean $60,671      (was shipped)
        FEED_DAYS=1 LATE=1    7 lost   mean $65,940
        FEED_DAYS=2 LATE=2   10 lost   mean $60,001

    The old note below argued 4 late because escapes went 4 -> 0 on a sweep of this constant alone.
    That was measured on the volatile mechanism, where a bigger multiplier was the only way to keep
    the trough off zero. It is the VARIANCE that kills, not the mean, and 550 units a season already
    exceeds Seb's ~400.

    **A flat 4 measured better on escapes and worse on everything else, and both halves were real.**
    Six seeds, seat 0 (`data/logs/feed_days_sweep.log`): escapes 4 -> 0 going from 2 to 4, which is
    what a nineteen-animal herd needs. But the escapes all happen after day 16, and buying four days
    of feed for FOUR animals on day 4 spends a bank that reads $28 at dawn. `test_router.py` caught
    exactly that -- `PLACE 0/1`, `melon seed 5 of 6` with "the livestock spent the bank first",
    `WHEAT sold 13 against 17` -- because early feed money is land and seed money.

    The herd is 4-7 animals before day 8 and 19 after day 15, so the buffer follows it.
    """
    return FEED_DAYS_LATE if day >= FEED_DAYS_FROM_DAY else FEED_DAYS


#: Most WHEAT bought in one order. **This is a cadence control, not the cap `FEED_ORDER_CAP` was.**
#: That one bounded the DAY's feed and starved a 19-animal herd; this bounds a single order while the
#: day's target is re-offered every turn, so the herd still gets everything it needs -- just spread.
#: `market_price` moves per unit inside one order and the shops restock every 4 steps, so eight orders
#: of 1 clear cheaper than one of 8. The tape buys 1 at a time, eight times, across hours 5-19.
#: **That sentence is about SEB'S tape.** Victor orders `BUY_PRODUCT WHEAT 11` in one order at h00.
#: This still governs the HERD top-up; the schedule's own row is handled by `BUY_THE_ROW_AT_DAWN`.
BUY_DRIP = 1

#: Most WHEAT the HERD path may buy in one turn. Separate from `BUY_DRIP` because that one also caps
#: the schedule row (`min(owed, BUY_DRIP)`), so reusing it varies two things at once -- a sweep on it
#: alone could not attribute its own result, and `BUY_DRIP = 99` scored 166 against a 151 baseline
#: rather than reproducing it, which is how the confound showed up.
#:
#: `herd` subtracts `state["ordered"][("feed", "WHEAT")]`, so whatever this leaves unbought is
#: re-offered next turn. That is the difference from `FEED_ORDER_CAP`, which bounded the DAY and
#: starved a 19-animal herd from day 15.
#: Swept on Seb's tape, seed 11, against a 151-cell baseline. There is a cliff between 5 and 6 --
#: below it the herd cannot get its ration in a turn when it needs one, and d6-d9 break exactly the
#: way `FEED_ORDER_CAP` broke:
#:
#:     CAP   cells   d6 d7 d8 d9      d11 d12 d13 d14 d15 d16
#:     3     183      9  5  6 17       20  18  13  18  19  22
#:     4     174      9  5  6 17       16  16  14  17  19  20
#:     5     173      9  5  6 17       16  15  14  16  19  22
#:     6     144      8  4  7 12       13  12  12  14  17  16   <- taken
#:     8     145      8  4  7 12       13  13  12  13  16  19
#:     10    152      8  4  7 12       13  16  13  13  19  19
#:     none  151      8  4  7 12       14  13  14  15  18  17
#:
#: At 6 the first eleven days are BYTE-IDENTICAL to uncapped and every day from d11 improves, so the
#: gain is real and costs nothing earlier.
FEED_TURN_CAP = 6

#: Hour from which the dusk top-up may fire. **The LAST turn, measured, six seeds, whole season:**
#:
#:     h18   2 lost   $58,308      h22  16 lost   $57,407
#:     h21   3 lost   $53,441      h23   2 lost   $61,039
#:
#: **h18 ships, not h23, and that is a deliberate trade.** h23 is worth +$2,731 a season but leaves
#: d6 at `feed 2/7`; h18 puts d6 at `feed 7/7` and `care 7/7`, exact against the tape. d0-d6 matching
#: is the project's objective and the season money is downstream of it -- see `matching-the-tape`.
#:
#: Earlier hours interleave with the evening's selling and produce a round trip -- on d4 we sold 8
#: at h14, 8 at h17, then bought 6 at h18, sold 6 at h19, bought 6 at h21, and so on, paying the
#: spread each time and buying 21 units on a day the tape buys 1. Seb sits on 1 wheat and $12 from
#: h4 to h18 and then sells 5 at h19 and 12 at h23. One order, after the book work is done, is both
#: cheaper and exactly his shape.
DUSK_FEED_HOUR = 18

#: First day the dusk top-up may fire. **d0 and d1 are exact against the tape and must stay that
#: way** -- ungated, the top-up buys one extra wheat on d0 (`buy_product 9/8`) and both days go red.
DUSK_FROM_DAY = 2

#: Floor for the opportunistic mid-tour drop below. A unit standing at a depot mid-tour re-checks this
#: every time it is about to walk away, and pens sit ON depot tiles, so with no floor a unit banking
#: one or two units at a time turns every such moment into a 1-turn DROP.
MIN_OPPORTUNISTIC_DROP = 4

#: How many units of the day's still-owed SELL row a load must contain before the delivery above is
#: worth the turn. Swept on the day-by-day cells, days 0-11:
#:
#:     1   d0=7 d1=6 d2=5 d3=7 d4=7 d5=10 d6=13 d7=19 d8=21 d9=27 d10=20 d11=26   catastrophic
#:     2   d0=7 d1=6 d2=4 d3=7 d4=7 d5=8  d6=11 d7=15 d8=13 d9=15 d10=19 d11=20
#:     3   identical to 2
#:     4   identical to 2
#:     6   d0=7 d1=6 d2=4 d3=7 d4=7 d5=7  d6=11 d7=15 d8=13 d9=15 d10=19 d11=20   best
#:
#: **Treat this as "somewhere in 2 to 6", not as a tuned value.** 6 is separated from 2/3/4 by a
#: single day-5 cell on ONE seed, which is inside the noise this project has measured repeatedly.
#:     8   back to the unflagged baseline -- it stops firing
#:
#: At 1 it fires for a single fertilizer: DROP is all-or-nothing, so the re-PICKUP costs more turns
#: than the sale returns and `work` falls 25 ops on day 8 alone.
MIN_SELL_ROW_DROP = 6


#: Turns of slack held back before the ferry will divert. It exists because `Node.service` is
#: `len(ops)` fixed at plan time and the executor re-derives ops on arrival, so a tour's remaining
#: cost is under-stated by ~27% on field tiles (`docs/service_undercount_2026-08-07.md`). A flat
#: reserve rather than a multiplier, because the under-count is a property of the board's live state
#: and not of the tour's length.
DELIVER_FERRY_MARGIN = 3



def _trace_drop(sink, act, st, inv, shed, carried, tiles):
    """Name the first gate that refuses this drop. Pure observation; changes nothing."""
    if act[0] not in STEP:
        gate = f"not a STEP ({act[0]})"
    else:
        future_needs = collections.Counter()
        for n in st["route"]:
            future_needs.update(n.needs)
        alive = sum(1 for r in tiles for c in r if isinstance(c, dict) and "animal" in c)
        farm_wheat = shed.get("WHEAT", 0) + carried.get("WHEAT", 0)
        if any(future_needs.get(it, 0) > 0 for it, qty in inv.items() if qty > 0):
            gate = "own route needs it"
        elif not (inv.get("WHEAT", 0) == 0
                  or farm_wheat - inv.get("WHEAT", 0) >= feed_days(day) * alive):
            gate = "feed reserve"
        elif sum(inv.values()) < MIN_OPPORTUNISTIC_DROP:
            gate = f"under floor ({sum(inv.values())})"
        elif sum(shed.values()) + sum(inv.values()) > SHED_CAPACITY:
            gate = "shed full"
        else:
            gate = "fires"
    sink.append((act[0], gate))

#: Pen tiles to fill BEFORE the shed cells and the field sweep, in order. Empty is the shipping
#: behaviour and must stay empty on main -- this exists so the *ceiling* of a pen-geometry change can
#: be measured by pinning the tape's own tiles, before any general rule is written to earn them.
#:
#: **That ceiling has now been measured, and pen geometry is not a lever.** Our day-0 pens sit on
#: y=3,4 (the depot row) and his on y=2,3, which reads like a real difference and is not one: the
#: Manhattan sum from (4,4) is **22 for both blocks**. Handing ourselves his exact eight tiles, taken
#: off his own board rather than off `build_tiles` (which lists 4 tiles for a day he builds 8 pens on,
#: and mislabels their animals -- see docs/fable_depot_sheep_2026-08-07.md):
#:
#:               d0  d1  d2  d3  d4  d5  d6  d7  d8  d9 d10 d11   total
#:     baseline   7   6   4   7   7   7  14  21  15  16  23  23    150
#:     his tiles  6   7   7   6   8   7  14  21  15  14  25  18    148
#:
#: Two cells out of 150, with d1 6->7 and d2 4->7 going backwards. So the early-day move diffs are
#: NOT downstream of where the pens are, and any future "his layout is better" argument has to beat
#: this number rather than restate the geometry.
#:
#: **That verdict expired, and the reason it expired is the point.** It measured MOVES, and moves
#: are genuinely unchanged -- 22 Manhattan from the shed either way. What it could not measure is
#: WHICH SPECIES ends up on which tile, because at the time `_live_ops` re-decided that itself by
#: global species rank and ignored `pen_for` entirely; the ground could not have carried an
#: assignment even if it had been sited correctly. With the executor reading the reservation, the
#: ORDER these tiles are taken in is what maps the schedule's `places` row onto ground.
#:
#: We already reach the same six tiles by d5. We take them in a different order, so the row
#: `['SHEEP','COW','SHEEP','COW']` lands inverted -- our sheep on `(3,4) (4,4)`, his on `(4,3)
#: (3,3)` -- and four of six pens hold the wrong animal.
#:
#: Op counts are blind to it. A HARVEST on a sheep and on a cow are both `HARVEST 1`, so the grid
#: reads `HARVEST 5/5` while one hand carries wool and the other milk. Replaying his d8 onto our
#: board, `u2 HARVEST @ (3,4)` finds SHEEP where his finds COW, both his `PLACE MILK 6` move zero
#: units, and the `SELL MILK 12` in that same basket -- funding his eleventh hire and ten
#: strawberry seeds -- no-ops on an empty shed. That is a market defect with a geometric cause,
#: which is exactly the axis the move-count measurement above cannot see.
#:
#: Read off both his replays, which agree tile for tile and hour for hour: this is a fixed opening,
#: not a reaction to the board. NOT from `build_tiles`, which contradicts both (see above).
#: Ordered, because the order is the assignment. Everything past `(4,2)` is NE ground and simply
#: waits for `_owned`.
PEN_SPOTS = ((4, 3), (4, 4), (3, 3), (3, 4), (2, 4), (4, 2),
             (5, 3), (5, 4), (6, 4), (6, 3))


#: Alex's narrowing, and the numbers say it is the right one: the damage and the benefit are on
#: DIFFERENT DAYS. Every cell the rule above cost is on d0-d5, where our layout already matches his
#: distance exactly (22 vs 22 on d0, 23 vs 23 on d6). Every far pen it fixes arrives later --
#: (5,0) on d8, (8,0) on d9, (9,0) on d10 -- once the crop sweep has eaten NE's near tiles.
#:
#: So apply it only from this day on. `None` disables the gate entirely. Swept, seed 11, weeds off:
#:
#:                 d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 d10 d11  total
#:     OFF          7  6  4  7  7  7 11 15 13 14  19  20   130
#:     from d5..d9  7  6  4  7  7  7 11 15 13 12  18  20   127
#:     from d10     7  6  4  7  7  7 11 15 13 14  19  18   128
#:
#: d0-d8 byte-identical, d9 14 -> 12, d10 19 -> 18. Every threshold from 5 to 9 gives the SAME
#: result, so 9 is chosen: the latest one that still captures the whole gain, which is the least
#: exposure on the early days of a seed we have not measured. `from d10` is strictly worse under an
#: in-order metric -- it leaves d9 and d10 alone and only reaches d11.
#: **TURNED OFF 2026-08-07: this costs the day-10 land parcel.** It was taken on a 130 -> 127 cell
#: reading, and the cell metric was the wrong judge. Swept against the other two recent flags, the
#: result is deterministic -- EVERY configuration with this ON loses the fourth quadrant, and every
#: one with it OFF keeps it:
#:
#:     STEAL  PEN    FERRY    land@d10   cells
#:     False  False  False    OK          130
#:     False  False  True     OK          128
#:     False  True   False    LATE        125
#:     False  True   True     LATE        125
#:     True   False  False    OK          115   <- taken
#:     True   False  True     OK          119
#:     True   True   False    LATE        118
#:     True   True   True     LATE        118   <- was shipped
#:
#: Turning it off is better on BOTH counts: 118 -> 115 cells and the parcel lands on day 10. Over a
#: full season the end gap halves, $20,588 -> $8,177, and the `tiles` row disappears entirely.
#:
#: The lesson is the pricing, not the rule. Three cells on a per-day counter were traded for 25 tiles
#: idle for a day, and that compounds for twenty more days. A per-day cell count cannot see it,
#: because the parcel shows up as ONE cell on ONE day.
#: **Gated to 11, past the parcel.** Alex's call, and it is the third time this day-gating trick has
#: paid: the rule is right and the DAY it starts is what decides whether it helps. From day 11 the
#: pastures still go up near the shed, and the day-10 land purchase is left alone.
#:
#:     from-day  land@d10   cells   d11
#:     None      OK         115     18
#:     11        OK         114     17   <- taken
#:     12        OK         115     18
#:     13        OK         115     18
#:     9         LATE       118     19   <- what shipped, and what cost the quadrant
PEN_NEAREST_DEPOT_FROM_DAY = 11

#: Market orders that survive a turn (`kaggriculture.py:535` keeps `orders[:10]`).
ORDER_SLOTS = 10

def _order_sells(orders):
    """The same orders, with the SELLs ranked biggest-first among the slots they already occupy."""
    at = [i for i, o in enumerate(orders) if o and o[0] == "SELL"]
    if len(at) < 2:
        return orders
    # Rewrite only the SELL slots, leaving every other order exactly where it sits -- the atomic
    # orders' positions relative to the sells are load-bearing (a BUY settles after that slot's SELL)
    # and must not move.
    ranked = sorted((orders[i] for i in at),
                    key=lambda o: -int(o[2]) * RT.BASE_PRICE.get(o[1], 0))
    out = list(orders)
    for i, o in zip(at, ranked):
        out[i] = o
    return out


def _wheat_row_first(orders, hour):
    """Hour 0's wheat buy, moved in front of HIRE / BUY_ANIMAL / BUY_SEED. SELLs stay put.

    `buy_product` is a FILL, not an offer. `_process_market` walks the slots in order and
    `_do_buy_product` re-checks the bank per unit (`kaggriculture.py:666-673`), so a late slot is
    paid out of whatever the earlier ones left. Measured on the Victor grid, seed 11, d0 h00 --
    identical quantity, different slot:

        ours  HIRE x4  COW 1  SHEEP 4  MELON 5  WHEAT 5  BUY_PRODUCT WHEAT 11   -> 5 of 11 clear
        tape  BUY_PRODUCT WHEAT 11  HIRE x4  COW 1  SHEEP 4  WHEAT 5  MELON 5   -> 11 of 11

    A FEED eats one wheat, so those six units are the herd's first night.

    **SELLs are deliberately not moved.** A SELL settles before any atomic order in a LATER slot,
    which is what lets a thin day fund its own purchases -- the tape takes a $1,000 parcel on a $718
    bank that way. Sliding the wheat above a sell would break that and buy nothing: the wheat is
    cheap, and what it needs is to be ahead of the *spending*, not ahead of the income.

    This does not contradict `HIRE_FIRST`, which is about the HOUR a hand is bought. `_hire_cost` is
    `mult * fib(hires_today)` on a per-DAY counter, so the crew costs the same wherever in the turn
    it sits, and a hire in slot 5 of hour 0 still works 23 turns.
    """
    # See `WHEAT_ROW_OUTRANKS_SHOPPING_ALL_DAY`: the slot argument above is true on
    # every turn, and d8 is decided at h01.
    first_spend = next((i for i, o in enumerate(orders)
                        if o and o[0] in ("HIRE", "BUY_ANIMAL", "BUY_SEED")), None)
    if first_spend is None:
        return orders
    wheat = [i for i, o in enumerate(orders)
             if o and o[0] == "BUY_PRODUCT" and len(o) > 1 and o[1] == "WHEAT" and i > first_spend]
    if not wheat:
        return orders
    moved = [orders[i] for i in wheat]
    rest = [o for i, o in enumerate(orders) if i not in set(wheat)]
    return rest[:first_spend] + moved + rest[first_spend:]


def _fit_slots(orders, state):
    """The turn's orders, cut to what the env will actually accept, with the losers un-counted."""
    if len(orders) <= ORDER_SLOTS:
        return list(orders)
    # Drop surplus HIREs from the LAST one backwards: slot order is load-bearing for everything else
    # (a SELL only funds a BUY that sits in a later slot), and the hires are homogeneous, so which
    # one goes is free while where the others sit is not.
    over = len(orders) - ORDER_SLOTS
    hires = [i for i, o in enumerate(orders) if o[0] == "HIRE"]
    cut = set(hires[-over:]) if hires else set()
    state["hired"] -= len(cut)
    return [o for i, o in enumerate(orders) if i not in cut][:ORDER_SLOTS]


#: Whether `sells` is read as a CUMULATIVE target (a missed row is retried until it is filled) or as
#: the old per-day row (a row that landed on an empty shed is forfeited). Switchable for the same
#: reason as the flag above: it must be attributable on the day-by-day trace, not on a final bank.
#: Days that send the schedule's whole `hands` row at hour 0 instead of dripping it out against the
#: landing-square model. Day 4 was pinned first and took `unit-turns` 184/208 -> 208/208.
#:
#: **TRIED and REVERTED 2026-08-07: pin days 0-3 as well.** They are the only days left carrying a
#: crew deficit -- `unit-turns` 182/185 on all four, which is exactly the two hands missing at h1
#: plus the one missing at h2, since Seb has all 8 units standing by h1 and we reach 8 only at h3.
#: The deficit is real and it is NOT `_fit_slots` (day 0 hour 0 emits 9 orders, under the ten-slot
#: cap) -- it is this drip, which lands hires 5 / 1 / 1 across hours 0, 1 and 2.
#:
#: Pinning them recovers the three turns and measures clearly WORSE:
#:
#:                       d0 d1 d2 d3 d4 d5
#:     drip (day 4 only)  7  6  4  7  7  7
#:     pin days 0-3      10 11  8  9  9 10
#:
#: Twelve cells across the six earliest days, which under "days match IN ORDER" is the worst place
#: to spend them. Sending the crew out at hour 0 changes where every unit routes, and the movement
#: rows diverge by more than the extra turns are worth. Pinning ALL thirty days measures identically
#: to pinning 0-3, so nothing later is being left on the table either.
HIRE_PINNED_DAYS = frozenset(range(30))

CUMULATIVE_SELLS = True

#: Whether the final day ignores every sell cap and offers the whole shed. Stock has no terminal
#: value; the caps above it all exist to protect a future day that does not arrive. Measured OFF:
#: the season ends holding MILK 48 and WHEAT 27, $14,424 at quoted prices, against a $38,593 loss.
LIQUIDATE_LAST_DAY = True

#: The hour the liquidation starts. Not hour 0: the herd still eats on the last morning, and dumping
#: the whole book in one turn clears at what the LAST unit fetches -- one season's wool went 123
#: units to 138 while revenue fell $29,041 to $21,811. Starting mid-afternoon leaves several turns
#: for the town's own draw (every 4 steps, and every 12 at 4x from day 20) to lift the book between
#: offers.
#:
#: **Flat, not tuned.** Final bank swept on seed 11: h0 $119,666, h8 $119,732, h12 $119,788,
#: h16 $119,915, h20 $119,807. All five clear the shed to empty and the spread is $249. 16 is the
#: middle of a flat region, not a peak worth defending.
LIQUIDATE_FROM_HOUR = 16


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

#: Whether every purchase below the sell block may be funded by that same turn's sales, as BUY_LAND
#: already is. See the note above the seed bill for the day-6 measurement.
SELLS_FUND_THE_TURN = True


#: The day from which `STEAL_FROM_DAY_MARGIN` applies, or `None` to never steal. Same narrowing that
#: `PEN_NEAREST_DEPOT_FROM_DAY` needed, and for the same reason: the cost and the benefit are on
#: different days. Re-swept 2026-08-07 against a 127-cell baseline, ungated:
#:
#:              d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 d10 d11  total
#:     OFF       7  6  4  7  7  7 11 15 13 12  18  20   127
#:     margin 4  7  7  4  7  8  8 11  8 11 14  19  19   123
#:
#: Lowest total and DISQUALIFIED in order -- d1 6->7, d4 7->8, d5 7->8. But d7 15 -> 8 is the biggest
#: single-day gain anything has produced, and d8 goes 13 -> 11, so stealing is unlocking something
#: real once the crew is large. Early on a claim is worth honouring: the crew is small, every unit is
#: committed, and taking a stop off one just moves the work.
#:
#: Gated, swept on the day threshold at margin 4:
#:
#:               d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 d10 d11  total
#:     OFF        7  6  4  7  7  7 11 15 13 12  18  20   127
#:     from d6    7  6  4  7  7  7 11  8 11 14  19  19   120   <- taken
#:     from d5    7  6  4  7  7  8 11  8 11 14  19  19   121   d5 regresses
#:     from d4    7  6  4  7  8  8 11  8 11 14  19  19   122   d4 regresses
#:     from d7    7  6  4  7  7  7 11 17 14 15  23  17   135
#:     from d8    7  6  4  7  7  7 11 15 14 16  18  17   129
#:
#: d0-d6 byte-identical and d7 15 -> 8, the largest single-day gain measured in this project. It
#: gives back 2 on d9 and 1 on d10; under an in-order metric the earliest day touched is what counts
#: and that day improves by seven. Gating LATER than 6 is worse, not better -- d7 and d8 both make
#: d7 itself worse -- so this is not "steal late", it is "steal once the crew outgrows the work".
STEAL_FROM_DAY = 6
STEAL_FROM_DAY_MARGIN = 4

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


def _route_turns(pos, route, depots):
    """Turns a committed tour still needs: the legs, the service at each stop, and the walk home.

    The same quantity `plan_routes` charged against the budget when it accepted the tour, recomputed
    from where the unit actually stands. It inherits that model's known under-count -- `Node.service`
    is `len(ops)` fixed at plan time -- which is what `DELIVER_FERRY_MARGIN` holds back for.
    """
    at, turns = tuple(pos), 0
    for node in route:
        turns += RT.dist(at, node.tile) + node.service
        at = tuple(node.tile)
    return turns + min(RT.dist(at, d) for d in depots)


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


def _nearest_ground(order, tiles, taken, unlocked):
    """The free tile closest to a depot, across every quadrant we own. See `PEN_NEAREST_DEPOT`.

    Deliberately NOT the sweep. The sweep's job is to keep a CROP block compact, and it does that
    well; a pen is a fixed daily round trip and wants proximity, not compactness. Ties break on the
    sweep's own order so the choice stays deterministic and stays inside the crop block's shape.
    """
    depots = [c for c in R.shed_access_tiles() if _owned(c, unlocked)] or [SPAWN]
    best, best_d = None, None
    for t in order:
        if t in taken or tiles[t[1]][t[0]] is not None:
            continue
        d = min(abs(t[0] - c[0]) + abs(t[1] - c[1]) for c in depots)
        if best_d is None or d < best_d:
            best, best_d = t, d
    return best


def _place_order():
    """Animals in the order a bare pen should take them: least slack first, `ANIMAL_NAMES` on ties."""
    return sorted(R.ANIMAL_NAMES,
                  key=lambda a: R.ANIMALS[a]["first_yield_day"] - R.ANIMALS[a]["max_held"])


def _emit(op, item):
    if op == "BUILD":
        return ["BUILD_COOP" if R.ANIMALS[item]["structure"] == "COOP" else "BUILD_PASTURE"]
    if op == "PLANT":
        return ["PLANT", item]
    if op == "PLACE":
        return ["PLACE", item, 1]
    return [op]


def _live_ops(tile, cell, day, inv, pins, seeds, fertilizer_price=None, hour=0, pen_for=None):
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
            # **A plant needs a turn left to water it, or it is a weed by dawn.** A new plant
            # starts at `consecutive_unwatered = 1` (`reference:222`, "planting day counts as
            # unwatered"), the dusk rollover adds one (`:781`) and `>= 2` turns the tile to WEED
            # (`:783`). WATER is a separate turn and needs `kind == "PLANT"`, so it can only come
            # AFTER the plant and only on the same day -- there is no watering the ground first.
            #
            # On the last turn of the day that water cannot exist, for any unit, on any route. So
            # the plant is not a gamble that failed, it is a seed spent to create a weed, and the
            # ground is then blocked for the season because PLANT needs EMPTY. Measured seed 11
            # melon arm d6: `u4 PLANT/MELON` at h23 on (8,4) with 8 seeds in store, and the day
            # ends `crop_MELON 12 weed 2` against the tape's `14` and `1`. One action, two cells.
            if hour >= TPD - 1:
                return []
            return [("PLANT", item)] if seeds.get(item, 0) > 0 else []
        return [("BUILD", item)]
    if not isinstance(cell, dict):
        return []
    kind = cell.get("kind")
    if kind == "PLANT":
        ops = RT.crop_ops(cell, day, inv.get("FERTILIZER", 0) > 0, fertilizer_price,
                          tile=tile)
    elif "animal" in cell:
        ops = RT.animal_ops(cell, day, inv.get("WHEAT", 0) > 0)
    elif kind in ("PASTURE", "COOP"):
        # **The pen takes the animal the schedule ordered for it.** `_refresh_pins` reads the row's
        # ordered `places` -- d0 is `['SHEEP','COW','SHEEP','COW']` -- and reserves a tile per entry
        # in `pen_for`. `router.build_nodes` has honoured that reservation since `PEN_KEEPS_ITS_ANIMAL`;
        # the executor did not, and re-decided by `_place_order()`, a global species rank that never
        # sees the row. SHEEP outranks COW there, so a hand holding both placed sheep every time and
        # the row's alternation was lost: we laid `SHEEP,SHEEP,COW,COW` against the tape's
        # `SHEEP,COW,SHEEP,COW`.
        #
        # Same six animals, same counts, different TILES -- and the tiles are what the season reads:
        #
        #     ours   SHEEP (2,4) (3,4)   COW (4,4) (4,3) (3,3) (4,2)
        #     tape   SHEEP (4,3) (3,3)   COW (4,4) (3,4) (2,4) (4,2)
        #
        # Produce is harvested into the HAND, not the shed, and only a shed-adjacent DROP or
        # `PLACE item n` banks it (`reference:394`). His milking cows sit along the shed row so two
        # hands PLACE 6 milk each on d8 h5 and one `SELL MILK 12` clears it in the same turn; ours
        # run away from the shed and the same 12 units split into h5 and h9. At d6 the same swap put
        # wool in his hand and milk in ours, and the sell that funded his BUY_LAND no-oped for us.
        #
        # A preference, never a lock -- same rule as `build_nodes`. A pen with no reservation, or one
        # this hand cannot fill, falls through to `_place_order()` untouched, because a lock is what
        # left a SHEEP idle in the shed for three days.
        order = _place_order()
        want = (pen_for or {}).get(tile)
        if want in order:
            order = [want] + [a for a in order if a != want]
        ops = next(([("PLACE", a, 0)] for a in order
                    if R.ANIMALS[a]["structure"] == kind and inv.get(a, 0) > 0), [])
    elif kind == "WEED":
        # A DIG clears ground for a planting that must happen on a LATER day, so on the last day
        # it is a turn spent to tidy up -- the d29 trace shows u4 digging (1,0) and (3,0) while
        # 3 units strand in its hand. Same gate as FEED/CARE (`router.upkeep_buys_nothing`).
        ops = [] if RT.upkeep_buys_nothing(day) else [("DIG", None, 0)]
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
        # A shed trip is a stop but it is not a CLAIM. Pens sit on shed-access tiles by design
        # (`_refresh_pins`), so recording the depot here would let one unit's pickup close a pen to
        # every idle hand for the rest of the day.
        if not getattr(n, "depot", False):
            out.setdefault(n.tile, t)
        pos = n.tile
    return out


def _seed_need_order(units, routes):
    """Earliest turn any committed tour stands on a PLANT stop, per crop.

    A PLANT is refused outright when `private["seeds"][crop] <= 0` (`kaggriculture.py:412`), the route
    is a visit ORDER, and a stop that returns nothing is dropped silently. So the hour a crop's seed
    arrives has to beat the hour the tour reaches that crop's ground, or the tile is never sown -- the
    unit does not wait for it and does not come back.

    Seed rows were ordered dearest-BLOCK-first (`-SEED_COST[crop] * qty`), which is a price order.
    That rule is right about what it was measured on -- under a thin bank, filling the dear block
    whole beats spreading it -- and it never consulted WHEN the plan needs each crop. On Victor's d10,
    seed 11, the two orders disagree and the price order funds the wrong crop:

        plan holds       12 MELON + 11 STRAWBERRY, 23 stops
        first stop       MELON h2, STRAWBERRY h5
        block cost       STRAWBERRY 16 x $100 = $1,600  ->  bought h2, bank $2,125 -> $46
                         MELON      14 x  $80 = $1,120  ->  bought h18, after its last stop at h15
        emitted          11 -- every strawberry, not one melon

    Victor's own row buys `BUY_SEED MELON 5` at h1 and puts his strawberry at h12/h13/h15. Need order,
    not price order. Block cost stays as the tie-break, so days whose crops are wanted at the same
    hour keep the 2026-08-07 measurement exactly.

    `_eta_along` is the same walk `plan_routes` costs an insertion at, so "sooner" means the same
    thing here as it does to the planner.
    """
    first = {}
    for u, st in (routes or {}).items():
        if u >= len(units):
            continue
        route = st.get("route") or ()
        eta = _eta_along(units[u], route)
        for n in route:
            t = eta.get(getattr(n, "tile", None))
            if t is None:
                continue
            for o, item in getattr(n, "ops", ()):
                if o == "PLANT" and item and t < first.get(item, 1 << 30):
                    first[item] = t
    return first


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


#: **Dig a weed when the day's own planting row cannot find ground.**
#:
#: OFF is the behaviour before 2026-08-12: `router.crop_ops` gates a weed's DIG on
#: `tile in plantable`, and `_plantable` is built from PLANT pins, which are only ever sited on
#: EMPTY squares -- so a weed is never plantable, never dug, and its square is dead for the season.
#: Measured on seed 11 / tape victor: (7,1) is LOCKED until d6, spawns a weed the moment the
#: quadrant unlocks (`weedSpawnChance`, the env default on the ladder), and is still a weed on the
#: final day. Ground we paid $1,000-$2,000 for and never used.
#:
#: Gated on `_replant` being non-empty -- the row wanting ground it could not find -- because the
#: `plantable` rule is otherwise correct and was itself a fix: ungated, digs measured `dig 5/0` on
#: d5 against a tape that digs nothing all season, plus strays on d12-d14.
DIG_A_WEED_WHEN_THE_ROW_IS_SHORT_OF_GROUND = True


def _pens_due_before_more_land(sched, day):
    """How many pens the schedule builds after `day` but before it buys its next parcel."""
    nxt = min((d for d in sorted(sched)
               if d > day and int(sched[d].get("land", 0) or 0) > 0), default=None)
    return sum(int(sched[d].get("builds", 0) or 0) for d in sorted(sched)
               if d > day and (nxt is None or d < nxt))


def _outstanding_places(sched, day, tiles):
    """The schedule's placements through `day` that no animal is standing on yet, in row order.

    Earliest occurrences are matched off first, so the species left over are the ones the later rows
    asked for -- which is what the shed is about to hold.
    """
    seq = [a for d in sorted(sched) if d <= day for a in (sched[d].get("places") or [])]
    standing = collections.Counter()
    for row in tiles:
        for c in row:
            if isinstance(c, dict) and c.get("animal"):
                standing[c["animal"]] += 1
    out = []
    for a in seq:
        if standing.get(a, 0) > 0:
            standing[a] -= 1
        else:
            out.append(a)
    return out


#: Tile -> crop for the opening sowing, read off his board. **A permutation, not a count change.**
#:
#: Measured 2026-08-17, seed 11, both three-quadrant tapes. Our d1 and his d1 sow the same totals, 12
#: melon and 7 wheat, and differ only in which square gets which -- six tiles, three each way. The
#: cause is the sweep below: crops are seated in `router.field_order` order, so the first crop reached
#: claims a contiguous block of squares and the next takes the remainder. He interleaves.
#:
#:     ours d1              his d1            x across, y down
#:     ME ME ME ME ME      wh ME ME wh ME
#:     ME ME ME ME wh      ME wh ME ME wh
#:     ME ME wh wh  .      ME ME wh ME  .
#:     ME wh wh  .  .      ME wh ME  .  .
#:     wh wh  .  .  .      ME wh  .  .  .
#:
#: It is not cosmetic. Wheat sown on d1 is ripe and cleared by d5, which is what frees the square for
#: his d6 strawberry; melon sown on d1 stands to about d10, and `PLANT` onto an occupied tile is
#: refused outright, so the square is lost for the season. Replaying his own d5-d11 actions against
#: our board, the ONLY refusals were these squares -- his d5 h14 strawberry on (0,0) and (1,1), his d8
#: harvest-then-wheat on (3,0) -- and they are the whole of the `strawb -2` and `melon +3` the replay
#: could not close. `docs/replay_window_cannot_converge_2026-08-17.md` has the tables.
OPENING_GEOMETRY = {(0, 0): "WHEAT", (1, 1): "WHEAT", (3, 0): "WHEAT",
                    (3, 2): "MELON", (2, 3): "MELON", (0, 4): "MELON"}

#: Last day `OPENING_GEOMETRY` is consulted. The squares are occupied from d1 to d5 so the pins are
#: unreachable in between anyway; the bound is here so a tile cleared in mid-season is sown by the
#: ordinary rule rather than by a map that describes the opening.
OPENING_GEOMETRY_LAST_DAY = 4


def _refresh_pins(state, sched, day, tiles, unlocked, unlocked_shops=()):
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

    # A reservation lives from the moment the ground is chosen until an animal stands on it, which
    # is strictly longer than the pin. It dies with the tile, not with the pin.
    # `setdefault`, not `[]`: this function is called directly by tests that build `state` by hand,
    # and a new key in `make_agent`'s dict is not a new key in theirs.
    pen_for = state.setdefault("pen_for", {})
    for t in list(pen_for):
        x, y = t
        cell = tiles[y][x]
        if not _owned(t, unlocked) or (isinstance(cell, dict) and "animal" in cell):
            pen_for.pop(t)
        elif cell is not None and not isinstance(cell, dict):
            pen_for.pop(t)                       # a weed or a plant took the ground
        elif isinstance(cell, dict) and cell.get("kind") not in ("PASTURE", "COOP"):
            pen_for.pop(t)

    structures = sum(1 for r in tiles for c in r
                     if isinstance(c, dict) and (c.get("kind") in ("PASTURE", "COOP")
                                                 or "animal" in c))
    want_pens = sum(int(sched.get(d, {}).get("builds", 0) or 0) for d in range(day + 1))
    wanted = [a for d in sorted(sched) if d <= day for a in (sched[d].get("places") or [])]
    have = structures + sum(1 for v in pins.values() if v[0] == "BUILD")
    # See `PENS_ARE_RESERVED_FOR_THE_PLACEMENTS_STILL_OUTSTANDING`. `pen_for` is insertion-ordered
    # and pens are sited nearest-ground-first, so spending the outstanding row over its existing
    # keys hands the earliest placements to the closest pens -- the siting rule, unchanged.
    todo = _outstanding_places(sched, day, tiles)
    # **A reservation is sticky while its species is still owed.** Re-labelling every tile from the
    # outstanding row each call re-derives the whole map from whatever has been placed so far, so a
    # hand that reaches its pens out of siting order silently rewrites the ones behind it.
    #
    # Measured on d0. The row is `['SHEEP','COW','SHEEP','COW']` and `PEN_SPOTS` sites
    # `(4,3) (4,4) (3,3) (3,4)`, giving SHEEP COW SHEEP COW correctly at hour 0. One unit carries
    # all four animals and walks `(3,4) (4,4) (4,3) (3,3)` -- the fourth pen first. Its COW lands on
    # `(3,4)`, `_outstanding_places` drops a COW from the row, and the next refresh re-labels the
    # three survivors from `[SHEEP, SHEEP, COW]` in insertion order: `(4,4)` flips COW -> SHEEP and
    # `(3,3)` flips SHEEP -> COW. Two of six pens hold the wrong animal because of a walk order.
    #
    # Sticky keeps what the ground was chosen for and spends the row only on tiles that have no
    # claim yet. The siting rule above is untouched, and a reservation whose species is no longer
    # owed still falls through to be re-labelled -- that is what `PENS_ARE_RESERVED_FOR_THE_
    # PLACEMENTS_STILL_OUTSTANDING` is for, and it is the case that matters when a placement is
    # dropped rather than merely reordered.
    pool = collections.Counter(todo)
    sticky = {}
    for t in list(pen_for):
        a = pen_for[t]
        if pool[a] > 0:
            pool[a] -= 1
            sticky[t] = a
    #: The row's leftovers, still in row order, for the pens nobody has claimed.
    spare, left = [], collections.Counter(pool)
    for a in todo:
        if left[a] > 0:
            left[a] -= 1
            spare.append(a)
    took = 0
    for t in list(pen_for):
        if t in sticky:
            a = sticky[t]
        elif took < len(spare):
            a = spare[took]
            took += 1
        else:
            break
        pen_for[t] = a
        # The pin carries the animal too, and `router.build_nodes` chains its PLACE off the
        # pin's item (`BUILD_THEN_PLACE`), so a re-label that skipped it would leave the two
        # disagreeing about the same tile.
        if t in pins and pins[t][0] == "BUILD":
            pins[t] = ("BUILD", a, R.ANIMALS[a]["cost"])
    while have < want_pens:
        a = spare[took] if took < len(spare) else "COW"
        took += 1
        # A pen ON a shed-access cell runs its whole daily loop -- draw feed, feed, care, collect,
        # harvest -- without a single move, so those four cells are worth more than any field tile.
        spot = next((tuple(c) for c in PEN_SPOTS
                     if tuple(c) not in taken and _owned(tuple(c), unlocked)
                     and tiles[c[1]][c[0]] is None), None)
        spot = spot or next((c for c in R.shed_access_tiles()
                             if _owned(c, unlocked) and tiles[c[1]][c[0]] is None
                             and c not in taken), None)
        if PEN_NEAREST_DEPOT_FROM_DAY is not None and day >= PEN_NEAREST_DEPOT_FROM_DAY:
            spot = spot or _nearest_ground(order, tiles, taken, unlocked)
        spot = spot or _next_ground(order, tiles, taken)
        if spot is None:
            break
        pins[spot] = ("BUILD", a, R.ANIMALS[a]["cost"])
        # **Outlive the pin.** The pin pops the moment the pen is built -- that is what it is for --
        # and with it went the only record of WHICH animal this ground was chosen for. Since the
        # near tiles are sited first, that record is the schedule's ordered `places` row expressed
        # as geometry. See `router.PEN_KEEPS_ITS_ANIMAL`. Cleared in the sweep above once the tile
        # holds an animal, or is lost.
        pen_for[spot] = a
        taken.add(spot)
        have += 1

    want = collections.Counter()
    for d in sorted(sched):
        if d <= day:
            want.update(sched[d].get("plants") or [])
    live = collections.Counter(v[1] for v in pins.values() if v[0] == "PLANT")
    # **Float the crop on the shop draw -- see `SHOP_ADAPT_CROPS`.** The COUNT the schedule asks for
    # is kept exactly; only the crop is re-decided, and only inside a cadence pair so the tour shape
    # is untouched. Anchored on `planted + live`, which never falls, so this cannot inflate the total.
    if SHOP_ADAPT_CROPS and day >= CROP_ADAPT_FROM_DAY:
        want = _adapt_crops(want, state["planted"], live, day, unlocked_shops, LAST_DAY)
    # **Cap the strawberry at what the town can actually drain -- see `STRAWBERRY_TILES_BY_DRAIN`.**
    # The row asks for 41-42 on every board that exists, and the only thing that removes strawberry is
    # a shop that carries it, so on a thin draw the last dozen tiles are dumped into a book that halves
    # 31 units above `I0`.
    #
    # Deliberately a target read off the leaders, not a headroom model. `SHOP_ADAPT_CROPS`'s docstring
    # records why the headroom route fails: it treats the drain as a cliff when the price curve is a
    # slope, so it under-plants every steep-curve product. A tile count measured from 79 winning seats
    # has neither problem.
    #
    # Freed ground needs no counterpart rule. `_outstanding` seats the smallest ask first, so melon and
    # carrot take their few tiles and WHEAT -- outstanding in the hundreds all season, carried by 5 shop
    # types, 3,000 units of dump tolerance -- takes the rest. That is the leaders' wheat complement.
    #
    # `max(cap, standing)` never retro-cuts ground already sown; the cap only declines to seat MORE.
    #
    # **THREE-QUADRANT BOARDS ONLY, and that is measured, not cautious.** Each arm uses a different
    # end of the table, and only the high end survived:
    #
    #     arm        quads  drains  cap  row   delta      verdict
    #     straw_q3     3      4      37   42   +4,022     cap binds, GOOD
    #     melon_q3     3      3      36   34   +5,615     never binds
    #     q4_straw     4      0      26   42     -214     binds hard
    #     q4_melon     4      0      26   34   -9,560     binds hard, worst arm
    #
    # The four-quadrant boards both draw ZERO strawberry shops and so take the table's low end, where
    # cutting costs about $2,400 a tile. tetsuya's 25.5 tiles at zero drains is HIS optimum for HIS
    # season; ours has more ground and a different sell cadence and cannot go there. The high end is
    # validated and the low end is refuted, so the cap is confined to the boards it was measured good
    # on. `unlocked` is the live board, so this reads the quadrant count rather than trusting a branch
    # to have installed by now.
    #
    # A flat ceiling near 37 fits every row above -- it would reproduce straw and melon exactly and
    # never bind on q4 -- and is the next thing to test, with the q4 tables re-solved for it.
    #
    # The `not q4_armed` guard is GONE: nothing sets that key since the branches were disarmed, so
    # it read True on every board and was a condition in name only. The cap now applies whenever the
    # row asks for strawberry, which is what it always did in practice.
    if day >= STRAWBERRY_FLOAT_FROM_DAY and want["STRAWBERRY"]:
        _drains = sum(1 for s in (unlocked_shops or ()) if s in STRAWBERRY_SHOPS)
        _cap = STRAWBERRY_TILES_BY_DRAIN[min(_drains, len(STRAWBERRY_TILES_BY_DRAIN) - 1)]
        _standing = state["planted"]["STRAWBERRY"] + live["STRAWBERRY"]
        want["STRAWBERRY"] = min(want["STRAWBERRY"], max(_cap, _standing))
    # **A pin the row no longer wants is dropped.** The sweep at the top of this function releases a
    # pin for three reasons -- the tile filled, the crop expired, the land was lost -- and the seating
    # loop below only ever ADDS, since `range(qty - planted - live)` is empty rather than negative
    # when the count is met. So nothing reconciles a pin against a row that something ELSE satisfied.
    #
    # Our own units are not that something: a unit that plants its pin fills the tile and the sweep
    # takes the pin. A REPLAYED day is, because the planner is driven every turn and its answer thrown
    # away, so it pins `(4,8)` while the tape sows `(7,3)`. The tape's crop credits `state["planted"]`
    # and the pin on `(4,8)` is still empty ground.
    #
    # Measured 2026-08-18, strawberry arm, own seed 70683142, replay d4-d11: d12 dawn wants 39
    # cumulative, 37 stand, and FOUR strawberry are pinned -- (3,8) (4,8) (3,9) (4,9). d12's row of
    # two became four plants, each dragging a chained WATER (`router.PLANT_THEN_WATER`), and each a
    # tile still holding a crop at d29.
    #
    # Newest first, so the oldest commitment survives. Pinning exists to stop the chosen ground
    # wandering turn to turn, and dropping the tile picked first would be that same wander.
    for _crop, _held in list(live.items()):
        _over = state["planted"][_crop] + _held - want[_crop]
        if _over <= 0:
            continue
        for _t in [t for t in reversed(list(pins))
                   if pins[t][0] == "PLANT" and pins[t][1] == _crop][:_over]:
            pins.pop(_t)
            taken.discard(_t)
        live[_crop] -= _over
    # **Shed-access ground is held for a pen that is DUE, not for one ten days out.**
    # `router.field_order` leaves the four shed-access cells out of the sweep on purpose -- they are
    # worth more as pens, where FEED, CARE, COLLECT_FERTILIZER, PICKUP and DROP all happen without a
    # move -- and that is right while a pen is waiting for ground. `have >= want_pens` is exactly the
    # question "does the schedule owe a pen today", and it is already computed above for the BUILD
    # loop; when nothing is owed, the cells are ordinary soil and a pen that turns up later can take
    # ordinary soil too (the BUILD loop already falls through to `_next_ground` for that).
    #
    # d11, seed 11: the day owes eleven plantings. Six pins go onto the six empty squares in
    # `field_order`, four more ride on the wheat tiles a harvest clears
    # (`router.REPLANT_A_CLEARED_TILE`), and the eleventh -- the fifth strawberry -- has nowhere to
    # go while (4,5) sits empty. The schedule builds 15 pens; twelve are standing by d8 and the next
    # is **d21**. `plant 9/11`, and `water 38/41` because each of those plantings owes a water.
    plant_order = order
    if have >= want_pens:
        plant_order = list(order) + [c for c in R.shed_access_tiles() if _owned(c, unlocked)]
    # **Smallest outstanding ask first.** `want` is CUMULATIVE and a Counter iterates in insertion
    # order, so WHEAT -- first seen on d0, and standing at 139 for the season -- claimed every empty
    # square before any other crop was reached. A crop the schedule wants one of is then never
    # planted at all while a crop it wants a hundred of is outstanding, which is not a priority
    # decision, just dict order.
    #
    # Measured: the six CARROT the schedule asks for on d21-d26 landed one on d26 and five on d27,
    # all past the day they could still yield, because wheat took the ground every time. Ordering by
    # ascending outstanding count self-limits -- once carrot's single tile is placed its remainder is
    # 0 and wheat takes the whole rest of the day, which is the 1-2 carrot beside 4-11 wheat that all
    # 66 downloaded games of the leader show.
    def _outstanding(crop):
        return want[crop] - state["planted"][crop] - live[crop]

    # See `PLANTING_KEEPS_GROUND_FOR_THE_PENS_DUE_BEFORE_THE_NEXT_PARCEL`. Held nearest-first,
    # because that is the ground a pen is worth more on and the ground sowing is about to take.
    sow_order = plant_order
    owed_later = _pens_due_before_more_land(sched, day)
    if owed_later > 0:
        free_now = [t for t in plant_order
                    if t not in taken and tiles[t[1]][t[0]] is None]
        held = set(free_now[:owed_later])
        sow_order = [t for t in plant_order if t not in held]

    # See `OPENING_GEOMETRY`. Seated BEFORE the sweep so these squares carry the crop he sows rather
    # than whichever crop the sweep order happens to reach first. Each pin spends its own crop's
    # outstanding count -- `live` is incremented, and `_outstanding` reads it -- so the day's totals
    # are untouched and this is a permutation of the same plantings, not an extra one.
    if day <= OPENING_GEOMETRY_LAST_DAY:
        for spot, crop in OPENING_GEOMETRY.items():
            if crop not in CROP or RT.plant_prize(crop, day) <= 0:
                continue
            if spot in taken or not _owned(spot, unlocked):
                continue
            if tiles[spot[1]][spot[0]] is not None:
                continue
            if _outstanding(crop) <= 0:
                continue
            pins[spot] = ("PLANT", crop, RT.plant_prize(crop, day))
            taken.add(spot)
            live[crop] += 1

    for crop in sorted(want, key=lambda c: (_outstanding(c), c)):
        qty = want[crop]
        if crop not in CROP or RT.plant_prize(crop, day) <= 0:
            continue
        for _ in range(qty - state["planted"][crop] - live[crop]):
            spot = _next_ground(sow_order, tiles, taken)
            # A preference, never a loss: ordinary ground first, the held squares rather than
            # leave the row unsown.
            if spot is None:
                spot = _next_ground(plant_order, tiles, taken)
            if spot is None:
                break
            pins[spot] = ("PLANT", crop, RT.plant_prize(crop, day))
            taken.add(spot)
    return pins


def _router_acts(state, sched, day, hour, tiles, units, invs, shed, seeds, unlocked, money=0.0,
                 arriving=(), unlocked_shops=(), fertilizer_price=None, hold_farmer=False):
    """One turn of the routed plan. The plan is built ONCE, at dawn, and then only walked.

    `arriving` is where today's hires will land (`_arrivals`). They are planned as vehicles even
    though they do not exist yet, because `interpreter` applies unit actions BEFORE the market phase
    (`kaggriculture.py:922` then `:928`) -- so a hand bought at hour 0 first acts at hour 1, and a
    planner that waits to see it plans hour 0 for the pre-hire crew and then throws that plan away.
    """
    pins = _refresh_pins(state, sched, day, tiles, unlocked, unlocked_shops)
    # Ground is only worth clearing if something is going into it. See `DIG_ONLY_IF_REPLANTING`.
    plants_left = any((sched.get(d, {}) or {}).get("plants") for d in range(day, LAST_DAY + 1))
    carried = collections.Counter()
    for iv in invs:
        carried.update(iv)
    # **Turns left at `hour` is `TPD - hour`, not `TPD - hour - 1`.** Hours run 0..TPD-1 inclusive
    # and the env applies unit actions on every one of them, so the old expression made the LAST turn
    # of every day unreachable for every hand: at hour 23 the budget was 0, no tour could be planned
    # into it, and a hand standing on a ripe tile passed. Measured on Seb's day-17 board with supply
    # stocked (`data/logs/why_pass.log`): 26 idle turns, all in the evening, every one of them with
    # work still on the board -- nine hands passing at hour 23 with five HARVESTs offered. The `-1`
    # is the market/hire turn, which is spent once at dawn and was being charged again at dusk.
    # `tests/test_the_last_turn_of_the_day_is_worked.py` pins it; it goes red with the `-1` back.
    # **The crew the plan routes is the crew the day will have, not the crew standing at dawn.**
    # Phantoms sit at the end, on the squares `_arrivals` says they will land on, and their index
    # here is the index they will occupy in `farm["hands"]` -- so the route built for phantom k is
    # already waiting for the real unit k when it appears an hour later.
    plan_units = list(units) + [tuple(p) for p in arriving]
    budget = [max(0, TPD - hour)] * len(plan_units)
    # A hand bought in THIS turn's market phase cannot act in this turn's unit phase -- the unit
    # phase already ran. It works from `hour + 1`, so it is one turn poorer than everyone else.
    for k in range(len(units), len(plan_units)):
        budget[k] = max(0, budget[k] - 1)
    routes = state["routes"]
    # Only shed cells inside a quadrant we own. A hand wakes on a LOCKED one and a LOCKED tile no-ops
    # before PICKUP is ever reached, so treating all four as depots strands the hand for the whole day.
    depots = tuple(c for c in R.shed_access_tiles() if _owned(c, unlocked)) or (SPAWN,)
    load = {u: collections.Counter(invs[u] if u < len(invs) else {}) for u in range(len(plan_units))}
    # What today's SELL row still owes the shed. The market reads the shed and nothing else, so a
    # product the row wants is worth nothing while it rides in a hand. See `DELIVER_THE_SELL_ROW`.
    owed_sale = collections.Counter({p: int(q) for p, q in (sched.get(day, {}).get("sells") or {}).items()
                                     if int(q) > 0})
    for p, q in shed.items():
        if q > 0:
            owed_sale[p] -= q
    # **The herd's dinner is not stock, however much the row wants it.** `consecutive_unfed >= 2`
    # removes the animal outright (`kaggriculture.py:786`), so wheat the farm still owes its own pens
    # today is spoken for before the market ever sees it. Without this the two claims on WHEAT are
    # indistinguishable and the day eats itself: seed 11 day 4 sells `WHEAT: 28`, the crew grows from
    # one hand to eight through the morning, and every full replan hands the feeds to a different
    # unit -- leaving the one that already drew the wheat holding a "surplus" the row wants. Traced:
    # h0 `PICKUP WHEAT 2`, h1 `DROP`, h4 another four drawn, h5 dropped. Over the day PICKUP 2,
    # DROP 12, FEED 0, CARE 0, and eight animals unfed.
    #
    # The reserve is the same `feed_days(day) * hungry` figure the market block protects, so the sell
    # guard and the day planner cannot disagree about how much wheat is not for sale.
    hungry = sum(1 for r in tiles for c in r
                 if isinstance(c, dict) and "animal" in c and not c.get("fed_today"))
    if hungry and owed_sale.get("WHEAT", 0) > 0:
        owed_sale["WHEAT"] = max(0, owed_sale["WHEAT"] - feed_days(day) * hungry)
    # **Does today's shopping list cost more than the bank holds?** See `FUND_THE_DAY_WHEN_SHORT`.
    # If it does, the produce the row means to sell is what unblocks it, so it is harvested first and
    # delivered on sight rather than batched. Recomputed every turn: the moment the sales land the
    # day stops being short and the plan goes back to plain covering.
    # **Against the DAWN spend, not the day's whole bill.** The parcel is bought late and out of the
    # day's own selling, so counting it here says day 4 is $1,000 short at hour 0 when it is not
    # short at all -- and a short day sets `due = hour`, which drags the entire SELL row to the shed
    # before anything has grown. See `_days_bill_now`.
    short_of_cash = (FUND_THE_DAY_WHEN_SHORT and any(q > 0 for q in owed_sale.values())
                     and _days_bill_now(sched.get(day, {})) > money)

    # **The shed the plan reasons about is the shed the day will have, not the one it wakes to.**
    # `interpreter` runs the unit phase and only then `_process_market` (`kaggriculture.py:922` then
    # `:928`), so everything the `buys` and `animals_bought` rows order lands at the END of this
    # turn. A dawn plan reading the live shed sees none of it. `BUY_ANIMAL` commits to
    # `private["shed"]` exactly like a product (`:672`), and `build_nodes` gates its PLACE branch on
    # `shed.get(a, 0) > 0` -- so an empty pen the day means to fill offers NOTHING at dawn, which is
    # why d3 and d6 planned zero placements while owning the pen to put the animal in.
    #
    # Credited at hour 0 only, and only from the current day's row: that is the single turn where the
    # plan runs ahead of the purchase. The goods are drawable from hour 1, which is also the first
    # hour a hand hired alongside them can act, so no route needs them sooner.
    # What today's own market phase will put in the shed at the end of this turn. Read by the tour
    # walker, which must not throw a dawn draw away for a delivery that has simply not landed yet.
    _bought_today = set()
    for _row in ("buys", "animals_bought"):
        _bought_today.update(i for i, q in (sched.get(day, {}).get(_row) or {}).items() if int(q) > 0)

    plan_supply = shed
    if hour == 0:
        plan_supply = collections.Counter(shed)
        for row_name in ("buys", "animals_bought"):
            for item, qty in (sched.get(day, {}).get(row_name) or {}).items():
                if int(qty) > 0:
                    plan_supply[item] += int(qty)

    #: **The ground our plan will actually sow.** See the WEED branch of `router.build_nodes`.
    #: A weed blocks only its own tile, so digging one on ground nothing is going into is a turn
    #: spent tidying. `DIG_ONLY_IF_REPLANTING` asks the season-wide question and answers yes while
    #: most of the board is pasture or unplanned. A pin IS the plan, so "in our geometry" is exactly
    #: "pinned to be planted".
    _plantable = {t for t, p in (pins or {}).items() if p and p[0] == "PLANT"}

    #: **What the cumulative `plants` row still wants and could find no dawn ground for.**
    #: `_refresh_pins` sites a PLANT only where `tiles[y][x] is None`, so on a full board the row
    #: silently truncates -- d8 wants ten seeds, has seven free squares, spends two on builds and
    #: pins exactly five. The shortfall is real ground: the day's own one-shot HARVESTs clear their
    #: tiles, which is how the tape puts ten seeds on seven squares. Handed to `build_nodes` as a
    #: budget so a harvest node may carry a PLANT; see `router.REPLANT_A_CLEARED_TILE`.
    #:
    #: Counted the same way `_refresh_pins` counts it -- cumulative over days up to today, less what
    #: is already planted and already pinned -- because a row that failed on a thin board was never
    #: retried and that is what `state["planted"]` is for.
    _replant = collections.Counter()
    if RT.REPLANT_A_CLEARED_TILE:
        _pinned_plants = collections.Counter(p[1] for p in (pins or {}).values()
                                             if p and p[0] == "PLANT")
        for d in sorted(sched):
            if d <= day:
                _replant.update(sched[d].get("plants") or [])
        _replant -= collections.Counter(state["planted"])
        _replant -= _pinned_plants

    # **A weed on ground the day actually needs is dug; one on spare ground is furniture.**
    #
    # `router.crop_ops` offers a DIG on a WEED only where `tile in plantable`, and `_plantable`
    # above is built from PLANT pins -- which `_refresh_pins` only ever sites on EMPTY squares.
    # A weed is therefore never plantable, so never dug, so the square is dead for the season. The
    # tile does not have to be a crop we lost: (7,1) on seed 11 was LOCKED until d6 and spawned a
    # weed the moment the quadrant unlocked (`weedSpawnChance`, the env default on the ladder), so
    # it is ground we paid $1,000-$2,000 for and can never use.
    #
    # The `plantable` gate is right in general and must stay -- without it we measured `dig 5/0` on
    # d5 against a tape that digs nothing all season, plus stray digs on d12-d14. So the opening is
    # the narrow one: `_replant` is exactly "what the cumulative plants row still wants and could
    # find no dawn ground for". When that is non-empty the day is SHORT OF GROUND by its own
    # accounting, and a weed square is the cheapest ground there is -- one turn, no seed, no walk
    # beyond the tile itself. When it is empty we are not short and the weed stays furniture.
    if DIG_A_WEED_WHEN_THE_ROW_IS_SHORT_OF_GROUND and sum(_replant.values()) > 0:
        _plantable = set(_plantable) | {
            t for t, c in ((t, tiles[t[1]][t[0]]) for t in RT.field_order(unlocked))
            if isinstance(c, dict) and c.get("kind") == "WEED"}

    #: **What TODAY's row asked for, as distinct from the cumulative budget.**
    #: `_replant` carries every unmet planting since day 0, so by the late season it holds a large
    #: standing WHEAT figure that outbids any small dated request on `plant_prize` forever. This is
    #: today's row alone, less what is already pinned, and `_best_replant_crop` serves it first.
    #: One tile, once -- `build_nodes` decrements it, so the day's remaining cleared ground falls
    #: straight back to the standing budget. See `router._best_replant_crop`.
    _dated = collections.Counter(sched.get(day, {}).get("plants") or [])
    _dated -= collections.Counter(p[1] for p in (pins or {}).values()
                                  if p and p[0] == "PLANT")

    def nodes_for(skip):
        return [n for n in RT.build_nodes(tiles, day, plan_supply, carried, unlocked, pins, hour,
                                          pen_for=state.get("pen_for") or {},
                                          plantable=_plantable,
                                          fertilizer_price=fertilizer_price,
                                          replant=collections.Counter(_replant),
                                          dated=collections.Counter(_dated))
                if n.tile not in skip]

    # Only units that can legally act are vehicles. A boxed-in hand is not a slow vehicle, it is no
    # vehicle at all, and planning work onto it silently deletes that work for the day.
    live = [u for u in range(len(plan_units)) if _mobile(plan_units[u], unlocked)]

    # **New work is a replan trigger, not just new workers.** See `URGENT_OPS`. The crew stabilises by
    # mid-morning and every unit is committed, so between the last hire and the first idle unit nothing
    # replans -- on Seb's day 0 that is hours 10-13, exactly when four pens finish and become placeable.
    # The animals waited, went in at hour 18, and could no longer be fed.
    # Key on (tile, op), never on the tile alone. A pen is BUILT and then PLACEd on the SAME square, so
    # the tile is already sitting in the builder's route when the PLACE node appears -- subtracting
    # routed *tiles* silently swallowed every new placement and the trigger never fired once.
    urgent = {(n.tile, o) for n in RT.build_nodes(tiles, day, shed, carried, unlocked, pins, hour,
                                                 pen_for=state.get("pen_for") or {},
                                                 fertilizer_price=fertilizer_price)
              for o, _i in n.ops if o in URGENT_OPS} if URGENT_OPS else set()
    routed = {(n.tile, o) for st in routes.values() for n in st["route"] for o, _i in n.ops}
    fresh = urgent - state["seen_urgent"] - routed
    state["seen_urgent"] = urgent

    if not routes or (not PLAN_THE_CREW_THAT_ARRIVES and state["crew"] != len(live)):
        # **ONE plan, at dawn, and the crew is no longer an excuse to rebuild it.** The old trigger
        # was `state["crew"] != len(live)`, justified as "hands are hired through the morning, so the
        # dawn plan genuinely cannot know how many vehicles it has". It does know. The schedule row
        # says how many, `_hires_this_turn` says how many of those the bank can settle, and
        # `_arrivals` says which square each lands on -- so the only thing the dawn plan lacked was
        # the arithmetic, not the information.
        #
        # What the trigger cost: unit actions run BEFORE the market phase, so hour 0 was planned for
        # the pre-hire crew, the hands appeared at hour 1, and the whole plan was thrown away and
        # rebuilt for 23 hours. Every day, measured: d0 replanned at h1 and h3, d1-d6 at h1.
        # **The shed the plan draws on is the shed the day will have, not the one it wakes to.**
        # `interpreter` runs the unit phase and only then `_process_market` (`kaggriculture.py:922`
        # then `:928`), so everything the `buys` row orders lands at the END of this turn. A dawn
        # plan reading the live shed sees none of it and routes no work that needs it: day 0 buys
        # WHEAT 8, the plan saw 0, and FEED went 2/4 -> 0/4 with `pickup` 5/5 -> 1/5. That is not a
        # feed served late, it is a turn spent PASSing.
        #
        # Credited only at hour 0, and only for the CURRENT day's row, because that is the one turn
        # where the plan runs ahead of the purchase. The goods are drawable from hour 1, which is
        # also the first hour the hands hired alongside them can act, so no route needs them sooner.
        sub = _solve([plan_units[u] for u in live], nodes_for(set()),
                     [budget[u] for u in live], depots,
                     {k: load[u] for k, u in enumerate(live)}, supply=plan_supply,
                     at_risk=_at_risk_tiles(tiles, day),
                     pointless=_pointless_tiles(tiles, day, plants_left),
                     tiles=tiles, wanted=owed_sale, fund=short_of_cash, day=day)
        state["routes"] = routes = {u: sub[k] for k, u in enumerate(live)}
        state["crew"] = len(live)
    # **NO REPLAN, NO TOP-UP. The day is deterministic and is planned once, at hour 0.**
    # Everything a day contains is written down before it starts: `hires`, `animals_bought`,
    # `builds`, `places`, `plants` and `sells` all come off the schedule, and the board evolves
    # from them by rules we simulate exactly. So there is nothing for a mid-day replan to
    # discover, and the two that existed were both destroying work rather than adding it:
    #
    #   URGENT_OPS   already dead (empty tuple) -- rerunning the plan when a PLACE node appeared
    #                measured day 0 `place` 4/4 -> 3/4 and `build_pasture` 8/8 -> 7/8.
    #   the top-up   handed a unit that finished its tour a fresh job set. `materialise` only
    #                appends the walk home when a job `yields()` or the predicted hand is
    #                non-empty, and PLACE/FEED/CARE is none of those -- so the rebuilt route had
    #                no depot stop. Traced on d1, seed 11: u4 collects fertilizer at h12, is
    #                re-tasked at h14, and ends the day PASSing at (2,3) holding 2 units with the
    #                shed three steps away and four turns spare. Those 2 units are exactly the
    #                d1 sell shortfall (2 sold against a row of 4).
    #
    # `HIRE_PINNED_DAYS` is every day for the same reason: the dawn plan cannot route hands that
    # do not exist yet, and the schedule already says how many there will be.
    acts = []
    #: Tiles an underfoot CARE has already been claimed for THIS turn. `underfoot()` reads the board
    #: as it stood at the start of the turn, so without this every hand standing on the same uncared
    #: pen emits its own CARE and only the first banks the bonus. (4,4) is a pen ON a shed-access
    #: tile, so the whole dawn shift stands on it at h2: eight turns, thirteen wasted hand-turns over
    #: d0-d6, which was the entire overshoot that had this rule shipped OFF.
    cared_this_turn = set()
    #: Thirsty tiles an idle hand has committed to this turn, so two of them do not converge on one
    #: crop and spend two turns saving one. See `THIRSTY_CROP_PULLS_AN_IDLE_HAND`.
    thirsty_claimed = set()
    #: Tiles where a hand is standing on its own next WORK stop and so will be offered that tile's
    #: ops by `_live_ops` this turn. The underfoot rule is for a hand CROSSING a tile; letting a
    #: passer-by take the care first only moves the wasted turn onto the hand whose job it was.
    #: Depot stops are excluded: a DROP or PICKUP emits no CARE, so treating one as work would
    #: suppress a care nothing else takes.
    working_tiles = {
        tuple(st["route"][0].tile)
        for u2, st in routes.items()
        if st and st["route"] and not getattr(st["route"][0], "depot", False)
        and u2 < len(units) and tuple(units[u2]) == tuple(st["route"][0].tile)
    }
    for u, pos in enumerate(units):
        # The call site is about to overwrite the farmer's action with the spawn-ring step. Walking
        # its route here anyway CONSUMES the first stop -- a depot draw empties `node.pick` and
        # decrements the local shed for a PICKUP that is then never emitted -- so the route believes
        # stock is in hand that is not. The first pen then offers no FEED, `FETCH_THE_FEED_AND_RETURN`
        # inserts an unplanned shed round trip, and the tour spends 27 turns of a 21-turn budget.
        # Defer instead of delete: leave the route untouched and start it one turn late.
        if hold_farmer and u == 0:
            acts.append(["PASS"])
            continue
        inv = collections.Counter(invs[u] if u < len(invs) else {})
        st = routes.get(u)
        if st is None:
            acts.append(["PASS"])
            continue

        # ------------------------------------------------------------------ walk the committed tour
        # **The shed trips are stops in this tour, not a side channel.** They used to be neither: a
        # `draw` dict outside the route drove the pickups, and the deliveries were left to whatever
        # depot cell a unit happened to wander onto. See `cover.materialise` for what that cost on
        # day 6. A depot stop carries its own `drop` and `pick`, both consumed a turn at a time and
        # both surviving across turns because the stop object is the state.
        act = ["PASS"]
        at_shed = tuple(pos) in set(depots)
        # **The last-day deadline.** See `must_walk_home_now`. Handled here, before the tour walk
        # and before underfoot/thirsty can spend the turn: from this hour every remaining stop
        # makes produce the close will discard, and the load in hand is the only job left.
        if must_walk_home_now(day, hour, pos, inv, depots):
            st["route"].clear()
            if at_shed:
                if sum(shed.values()) + sum(inv.values()) <= SHED_CAPACITY:
                    act = ["DROP"]
            else:
                home = min(depots, key=lambda t: RT.dist(pos, t))
                m = _step_towards(pos, home, unlocked)
                if m is not None:
                    act = [m]
            acts.append(act)
            continue

        def underfoot():
            """The op worth doing on the tile this hand is STANDING on, or None.

            The route is a visit ORDER and `_live_ops` is consulted at STOPS, so a tile a hand
            merely crosses is never looked at. Both branches below emit a move, and putting this on
            only one of them measured as an exact null -- the hands that walked over the hungry pen
            at (1,4) on day 4 were in the DEPOT branch, on their way to drop.

            FEED only out of SURPLUS: the wheat a hand carries is drawn for the pens still on its
            own route, so spending it here would just move the hunger. It feeds what it holds above
            that count and the planned tour is untouched.

            CARE only on a pen already FED today. `pending_care_bonus` is consumed only on a day the
            animal is also fed (`router.animal_ops`), so a care on an unfed pen banks nothing, and
            this must never spend a turn on one. It costs no item at all -- `_apply_unit_action`
            just sets `cared_today` (`kaggriculture.py:511-517`) -- against one extra unit of
            product on the next production day.
            """
            here = tiles[pos[1]][pos[0]]
            if not (isinstance(here, dict) and "animal" in here):
                # **A ripe crop underfoot is the same defect as a hungry pen underfoot**, and this
                # function has always returned None on it -- the docstring above says "a tile a hand
                # merely crosses is never looked at" and then only ever implemented the animal case.
                #
                # Measured on d4, seed 11, the tape's `harvest 7` against our 6. The missing tile is
                # (1,4), a ripe wheat tile worth 3 units. Its owner is the last stop of the longest
                # tour (`cost 23` against a 23-turn budget) and reaches it at h23 with no turn left
                # to work it -- while THREE other hands cross it earlier and walk on:
                #
                #     h16  u4@(1,4) -> EAST      h19  u2@(1,4) -> WEST
                #     h23  u0@(1,4) -> EAST      h23  u2@(1,4) -> EAST
                #
                # HARVEST only, never WATER: a harvest is a turn for a whole yield and it clears the
                # tile for a replant, whereas watering a tile someone else is routed to merely moves
                # the turn around. `working_tiles` keeps it off a tile another hand is working THIS
                # turn, so two hands cannot harvest the same crop.
                if (not HARVEST_WHAT_YOU_STAND_ON
                        or not isinstance(here, dict) or "crop" not in here
                        or tuple(pos) in working_tiles or tuple(pos) in cared_this_turn):
                    return None
                ops = RT.crop_ops(here, day, inv.get("FERTILIZER", 0) > 0, fertilizer_price,
                                  tile=tuple(pos))
                # See `UNDERFOOT_LEAVES_A_CROP_THAT_CAN_STILL_GROW`. A water still on offer means
                # the tile has a unit left in it, and this hand is forbidden to water.
                if any(o == "WATER" for o, _a, _v in ops):
                    return None
                if any(o == "HARVEST" for o, _a, _v in ops):
                    cared_this_turn.add(tuple(pos))
                    return ["HARVEST"]
                return None
            # **Ask the same question the planner asked.** `underfoot` used to feed any unfed pen it
            # stood on, so a ration `will_be_fed` had deliberately declined went in anyway the moment
            # a loaded hand crossed the tile -- d0 planned two feeds and emitted three.
            if not here.get("fed_today") and inv.get("WHEAT", 0) > 0 and RT.will_be_fed(here, day):
                owed = sum(1 for nd in st["route"]
                           for o, _i in getattr(nd, "ops", ()) if o == "FEED")
                if inv["WHEAT"] > owed:
                    return ["FEED"]
            if (CARE_WHAT_YOU_STAND_ON and here.get("fed_today")
                    and not here.get("cared_today")
                    and not RT.upkeep_buys_nothing(day)
                    and tuple(pos) not in cared_this_turn
                    and tuple(pos) not in working_tiles):
                # Claimed on RETURN: both call sites consume a non-None `underfoot()`
                # unconditionally (`act = under; break`). A third caller that inspects without
                # emitting would need the claim moved to the call sites.
                cared_this_turn.add(tuple(pos))
                return ["CARE"]
            return None
        #: Stops already sent to the back of this tour THIS TURN, so a tour whose every remaining
        #: stop is waiting on seed rotates once and passes instead of spinning forever.
        deferred = set()
        while st["route"]:
            node = st["route"][0]
            if getattr(node, "depot", False):
                # Any shed-access tile serves. The plan named one so it could cost the detour, but
                # `_is_shed_adjacent` (`kaggriculture.py:325`) does not care which, and standing on
                # a different one is only ever cheaper than walking to the named one.
                if not at_shed:
                    m = _step_towards(pos, node.tile, unlocked)
                    if m is None:               # unreachable: drop the stop rather than idle on it
                        st["route"].pop(0)
                        continue
                    # Same rule as the travel branch below, and this is the branch that actually
                    # matters: the hands that walked over the hungry pen at (1,4) on day 4 were on
                    # their way to the shed to DROP, not between two work stops. Putting the check
                    # only on the travel branch changed nothing at all.
                    under = underfoot()
                    if under is not None:
                        act = under
                        break
                    act = [m]
                    break
                if node.drop:
                    node.drop = False           # consumed whether or not there was anything to shed
                    # DROP does not clamp -- it `del`s every item after taking whatever fits
                    # (`kaggriculture.py:333`) -- so a full shed DESTROYS the load rather than
                    # refusing it. Carrying it to the overnight sweep is strictly better.
                    if (any(v > 0 for v in inv.values())
                            and sum(shed.values()) + sum(inv.values()) <= SHED_CAPACITY):
                        for item, qty in inv.items():
                            if qty > 0:
                                shed[item] = shed.get(item, 0) + qty
                                owed_sale[item] -= qty
                        act = ["DROP"]
                        break
                    continue
                # **The selective drop.** `PLACE <item> <n>` beside the shed banks n of ONE item and
                # leaves the rest of the hand alone (`kaggriculture.py:381-395`), which is the whole
                # reason `cover._bank` can plan a stop that sheds the fertilizer and keeps the ration.
                # `DROP` cannot express it, and paying a turn to bin the wheat plus a turn to fetch it
                # back is what left day 1's fourth pen one turn outside a 24-turn budget.
                #
                # Unlike `DROP` this one CLAMPS rather than destroys -- the reference takes
                # `n = min(n, room)` -- so a full shed costs the bank, never the goods. The local
                # mirror clamps identically so `shed` does not drift from the board.
                if node.place:
                    item = min(node.place)      # a total order, so the tape is reproducible
                    qty = node.place.pop(item)
                    room = max(0, SHED_CAPACITY - sum(shed.values()))
                    give = min(qty, inv.get(item, 0), room)
                    if give <= 0:
                        continue
                    shed[item] = shed.get(item, 0) + give
                    owed_sale[item] -= give
                    act = ["PLACE", item, give]
                    break
                if node.pick:
                    item = min(node.pick)       # a total order, so the tape is reproducible
                    take = min(node.pick[item], shed.get(item, 0))
                    if take <= 0:
                        # **A momentary shortfall is not a refusal, but only for a draw that is
                        # CRITICAL.** The shed drains from the sell block and from every other unit's
                        # own draw inside the same replan, which `materialise` cannot see -- it plans
                        # each tour independently -- and it refills a few turns later off the ordinary
                        # `BUY_PRODUCT` drip. Popping the want unconditionally (as this used to, before
                        # checking `take`) threw a CRITICAL need away outright instead of losing only
                        # this one attempt at it -- exactly the day-12 SHEEP at (1,6):
                        # `Depot(pick={WHEAT: 2}, critical=True)` drew against a shed reading 0 at
                        # that hour and was discarded rather than retried once it read 6 two hours on.
                        #
                        # Ordinary (non-critical) draws keep the old behaviour -- drop this attempt and
                        # move on -- because standing and retrying EVERY momentary shortfall regressed
                        # day 4's land purchase and day 5's sell-slot ordering (`test_a_land_buy_may_
                        # be_funded_by_the_same_turns_sales`, `test_the_biggest_sale_takes_the_
                        # earliest_slot`): most shortfalls are not an animal about to escape, and
                        # blocking a hand on all of them shifts timing far beyond this one starvation.
                        # **At hour 0 an empty shed is not a shortfall, it is arriving early.**
                        # `interpreter` runs the unit phase and only then `_process_market`
                        # (`kaggriculture.py:922` then `:928`), so nothing the day buys is in the
                        # shed while hour 0 is being worked -- and the dawn plan is built against a
                        # shed credited with exactly those goods (`PLAN_TODAYS_PURCHASES`). Deleting
                        # the want here throws the draw away on the one turn it could never succeed.
                        #
                        # Traced on day 0, seed 11: u0 builds at (4,4) on h0 and (3,4) on h2, then
                        # PASSes for twenty-one turns with two PLACE stops still in its route, four
                        # animals in the shed from h1 and two empty pens under its feet. `place 2/4`,
                        # `feed 0/4` and `sheep 0/2` all come from that one discarded pickup.
                        #
                        # Only for an item the row actually buys today, and only at hour 0: a hand
                        # waits one turn for a delivery that is already ordered, and every other
                        # shortfall keeps the old behaviour, which is what the day-4 land purchase
                        # and the day-5 sell ordering were tuned against.
                        # **Waiting past hour 0 was tried here twice, on 2026-08-13, and BOTH are
                        # losses. Do not restore either without a grid.** The measured cause of the
                        # short feed days is real -- `feed` equals whatever the shed held at dawn,
                        # d3 2/4 on a shed of 2, d7 4/9 on a shed of 4, d8 0/10 on a shed of 0 --
                        # but making the hand stand and wait is not the fix.
                        #
                        #   wait on ANY shortfall while the row is still buying
                        #       d6 `tiles 25/50` -- the land purchase slips to d7 and takes
                        #       `plant 9/9 -> 0/9` with it. The hands standing at the shed are the
                        #       hands whose sales fund the parcel.
                        #   wait only on a CRITICAL draw (`Depot.critical`, which `cover` sets from
                        #   `at_risk`, and which this walker has never read)
                        #       same `tiles 25/50` land slip, for `feed 3/10` on d8.
                        #
                        # Hour 0 stays, because it is the one turn where an empty shed is certain to
                        # be a delivery not yet landed rather than a shortfall.
                        if hour == 0 and item in _bought_today:
                            break
                        # **An animal is not a contested draw.** See
                        # `THE_ANIMAL_WAITS_FOR_THE_PURCHASE_THAT_DELIVERS_IT`. The two rules above
                        # rescue a dawn draw only; the row buys day 8's SHEEP at h05, so the shed is
                        # empty of it for six hours and whichever hand arrives first bins the want,
                        # the PLACE behind it, and the FEED and CARE that travel with the PLACE.
                        #
                        # The animal and the job it fills both move one stop down the tour, so the
                        # hand keeps working and asks again when its own route puts it back at the
                        # shed. Only when there IS other work -- a hand with nothing else would be
                        # standing at the shed, which is the arm that lost the d6 land parcel twice.
                        if (item in R.ANIMAL_NAMES and item in _bought_today
                                and node.tile not in deferred):
                            tail = [n for n in st["route"][1:]
                                    if getattr(n, "needs", None) and n.needs.get(item, 0) > 0]
                            rest = [n for n in st["route"][1:] if n not in tail]
                            if rest:
                                deferred.add(node.tile)
                                want = node.pick.pop(item)
                                rest[1:1] = [DP.Depot(node.tile, pick={item: want},
                                                      critical=node.critical)] + tail
                                st["route"][1:] = rest
                                continue
                        del node.pick[item]
                        continue
                    node.pick[item] -= take
                    if node.pick[item] <= 0:
                        del node.pick[item]
                    elif hour == 0 and item in _bought_today:
                        # **The other half of the morning delivery.** See
                        # `CARRY_THE_UNFILLED_DRAW_FORWARD`. `WAIT_FOR_THE_MORNING_DELIVERY` covers a
                        # draw that gets NOTHING at hour 0 -- but a draw that gets SOME of what it
                        # asked for never reaches that branch, and the remainder is deleted on the
                        # next turn like any ordinary shortfall. It is not one: `_process_market` runs
                        # after the unit phase (`kaggriculture.py:922` then `:928`), so the rest of
                        # the order is still in flight, and the plan was built against a shed already
                        # credited with it (`PLAN_TODAYS_PURCHASES`).
                        #
                        # Moved to a stop the tour is already making, so it costs the PICKUP turn and
                        # no travel, and the hand never stands still -- which is what the two
                        # wait-for-it arms recorded below did, and both lost the d6 land parcel.
                        # Deliberately hour 0 ONLY: carrying every shortfall forward, all day, was
                        # measured on this grid and is a loss (d3 `feed 4/4 -> 3/4`, d7 `7/9 -> 4/9`,
                        # d16 $26,664 -> $22,418) -- past dawn a short shed is competition between
                        # hands, not a van that has not arrived.
                        # **And only to a stop that still has a pen AFTER it.** A draw taken at the
                        # end of the tour feeds nothing -- it spends a turn and, worse, lifts wheat
                        # out of a shed the other hands are drawing from, so the ration is not merely
                        # wasted, it is taken from someone. The unguarded version measured exactly
                        # that: d3 `feed 4/4 -> 3/4` and d7 `7/9 -> 4/9` on a day with five and eight
                        # hands, while d1 -- one farmer, nobody to steal from -- gained its fourth pen.
                        later, _rest = None, st["route"][1:]
                        for _k, _n in enumerate(_rest):
                            if getattr(_n, "depot", False) and any(
                                    getattr(_w, "needs", {}).get(item, 0) > 0
                                    for _w in _rest[_k + 1:]):
                                later = _n
                                break
                        if later is not None:
                            later.pick[item] += node.pick[item]
                            del node.pick[item]
                    shed[item] -= take
                    act = ["PICKUP", item, take]
                    break
                st["route"].pop(0)
                continue
            if pos != node.tile:
                m = _step_towards(pos, node.tile, unlocked)
                if m is None:                       # unreachable: drop the stop rather than idle on it
                    st["route"].pop(0)
                    continue
                # **Feed the animal under your feet before walking off it.** The route is a visit
                # ORDER and `_live_ops` is consulted at STOPS, so a tile a hand merely crosses is
                # never looked at -- nothing asks whether the ground it is standing on needs
                # something already in its hand.
                #
                # Traced on day 4, seed 11, at the pen (1,4) that ends the day unfed:
                #
                #     h13  u6@(1,4){WHEAT: 8} -> EAST
                #     h15  u5@(1,4){WHEAT: 8} -> EAST
                #
                # Two hands, eight wheat each, standing ON the hungry animal and walking over it.
                # Six of these across d3-d6, and they are `feed 6/7` on d4 and `feed 7/8` on d6.
                #
                # A FEED is not an optimisation. `consecutive_unfed >= 2` removes the animal outright
                # (`kaggriculture.py:786`), so this costs a $400-500 asset plus every remaining day of
                # its production, against one turn. `REQUIRED_OPS` already says so in the planner;
                # the executor simply never got asked.
                #
                # Only out of SURPLUS: the wheat a hand carries is drawn for the pens still on its
                # own route, and spending it here would just move the hunger to one of those. It
                # feeds only what it is carrying above that count, so the tour it was planned for is
                # untouched.
                under = underfoot()
                if under is not None:
                    act = under
                    break
                act = [m]
                break
            cell_here = tiles[node.tile[1]][node.tile[0]]
            ops = _live_ops(node.tile, cell_here, day, inv, pins, seeds, fertilizer_price,
                            hour=hour, pen_for=state.get("pen_for") or {})
            if not ops:
                # **Go back for the feed rather than abandon the animal you just placed.**
                # `SERVE_THE_ANIMAL_IT_PLACES` hangs the FEED and CARE off the placement node, and
                # after the PLACE lands `_live_ops` re-derives the tile as
                # `animal_ops(cell, day, inv["WHEAT"] > 0)`. A hand holding no wheat gets an empty
                # list, so the stop drops here and the pen is never revisited -- the animal it just
                # put in the ground starts its `consecutive_unfed` count (`kaggriculture.py:786`)
                # on day one.
                #
                # Traced on day 0, seed 11: u0 draws SHEEP 2 and WHEAT 4 and serves both its pens;
                # u4 draws COW 2 and no wheat because u0 took the only unit that had landed, places
                # at h4 and h7, and feeds neither -- with sixteen turns still in hand.
                #
                # This is what the tape does, watched on the same day. Its chain hand makes TWO shed
                # trips (h1-h3 and h8) and swaps its load mid-day -- picks up cows at h1, DROPs them
                # at h2, takes sheep instead at h3 -- and its feeder hand makes two more (h8, h14)
                # before FEEDing at h9, h11, h17 and h19. Nobody carries a whole day's supply out in
                # one go; they go back.
                #
                # Costed, not assumed: the round trip is the walk to the shed, the walk to the pen,
                # the PICKUP and the FEED, and it is only taken if that many turns are actually left.
                if (isinstance(cell_here, dict)
                        and "animal" in cell_here and not cell_here.get("fed_today")
                        and inv.get("WHEAT", 0) <= 0 and shed.get("WHEAT", 0) > 0):
                    def _md(a, b):
                        return abs(a[0] - b[0]) + abs(a[1] - b[1])
                    home = min(depots, key=lambda t: _md(pos, t))
                    trip = _md(pos, home) + _md(home, node.tile) + 2
                    if TPD - hour >= trip:
                        # Draw for every pen still ahead on this tour, not just the one underfoot.
                        # PICKUP is unbounded and costs one turn per ITEM (`kaggriculture.py:340`),
                        # so asking for four is the same turn as asking for one -- and a hand that
                        # takes one makes the whole round trip again for the next pen.
                        want = 1 + sum(1 for nd in st["route"][1:]
                                       for o, _i in getattr(nd, "ops", ()) if o == "FEED")
                        st["route"].insert(0, DP.Depot(home, pick={"WHEAT": want}))
                        continue
                # **Seed the day has not bought YET is not a stop somebody else did.** An empty op
                # list normally means the tile was served by another hand, and dropping the stop is
                # right. For a pinned PLANT it can also mean `private["seeds"][crop]` is 0 right now
                # -- `_apply_unit_action` refuses the op outright (`kaggriculture.py:412`) -- while
                # the row is still going to buy it. The unit phase runs BEFORE `_process_market`
                # (`:922` then `:928`), so seed ordered today lands hours after the tour was planned
                # around it.
                #
                # d10, seed 11: the row buys `{MELON 14, STRAWBERRY 16, WHEAT 1}` on $2,127. Melon is
                # ordered first because its stops come at h4 (`_seed_need_order`), which leaves $400
                # of strawberry affordable at h2 and puts the other twelve behind the day's sells --
                # store reads 4 at h2, 0 at h11, 12 at h16. Four committed strawberry stops fall in
                # that window: u12 (1,9) h12, u11 (0,6) h13, u8 (4,9) h11 and (3,8) h15. Each was
                # binned and each hand then passed to dusk standing on the tile -- 9, 11 and 12 idle
                # turns -- with seed in the store from h16. `plant 19/23`.
                #
                # It goes to the BACK of the tour rather than being held under foot, because u8's
                # (4,9) has a MELON stop behind it at (4,8) that it does go on to plant; blocking
                # the hand there would trade one planting for another. `deferred` caps it at one
                # rotation per stop per turn.
                if not isinstance(cell_here, dict):
                    pin = pins.get(node.tile)
                    if pin and pin[0] == "PLANT" and seeds.get(pin[1], 0) <= 0:
                        crop = pin[1]
                        owed = (int((sched.get(day, {}).get("seeds") or {}).get(crop, 0))
                                - (state["planted"][crop] - state["planted_dawn"][crop]))
                        if owed > 0 and node.tile not in deferred and len(st["route"]) > 1:
                            deferred.add(node.tile)
                            st["route"].append(st["route"].pop(0))
                            continue
                        if owed > 0:
                            break                       # last stop; wait here for the seed
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

        if act == ["PASS"] and any(v > 0 for v in inv.values()):
            if at_shed:
                # Same clamp as the planned drop: DROP `del`s every item after taking what fits
                # (`kaggriculture.py:333`), so a full shed DESTROYS the load rather than refusing it.
                if sum(shed.values()) + sum(inv.values()) <= SHED_CAPACITY:
                    act = ["DROP"]
            else:
                home = min(depots, key=lambda t: RT.dist(pos, t))
                m = _step_towards(pos, home, unlocked)
                if m is not None:
                    act = [m]
        acts.append(act)
    return acts



# ==== GRAFTED FROM HEAD 2026-08-09 ====================================================
# This commit is the 1455 artifact and predates every market mechanism. Transplanted
# VERBATIM, so the comparison is 'this planner WITH market pricing' rather than 'a
# reimplementation of it' -- a rewrite would confound the one thing being measured.
# ======================================================================================
try:                                                                        # pragma: no cover
    from kaggle_environments.envs.kaggriculture import kaggriculture as _KG
except Exception:                                                           # pragma: no cover
    _KG = None


PRICE_AWARE_SELL_CAP = True
RESERVATION_SELL_CAP = True
HOLD_A_FLOORED_BOOK = True
RESERVATION_CONTEST = 0.5
RESERVATION_SLIP = 0.10
#: **Hold a sale until the town has drained the book -- unless today still has to be paid for.**
#:
#: `townCenterSellInterval = 24` on this economy, so the book drains once a day; `market_price`
#: falls monotonically in inventory (`kaggriculture.py:177`) and recovers as the shops restock every
#: 4 steps. Selling before the drain is selling into the bottom of the curve.
#:
#: Read off Seb's tape, and it is NOT a constant hour -- his sell hour tracks his cash need:
#:
#:     d2   SELL FERTILIZER  h15x3 h19x2      nothing to fund
#:     d3   SELL FERTILIZER  h15x4 h18x1      nothing to fund
#:     d6   SELL WOOL        h09x6 h13x6      BUY_LAND at h13, bank $5 -> $1,349
#:
#: `LATE_SELL_BIAS` has shipped OFF this whole time, and switched on FLAT it is strictly worse on
#: d6: it delays the wool past h13 and the parcel that the wool was for. The gate below is the
#: missing half, and it is Alex's framing -- once the bank covers the day the timing is free money,
#: while it does not the timing IS the purchase.
LATE_SELL_BIAS = True
LATE_SELL_FROM_HOUR = 16
#: Products no shop consumes, so the within-day recovery `LATE_SELL_BIAS` waits for never arrives.
#: FERTILIZER is drainless too (not even a town-centre product) but is held out of v1: no measurement
#: says it is costing us, and each extra product widens what the A/B has to explain.
NO_DRAIN_PRODUCTS = ("MELON",)
SELL_AT_ONCE_FROM_DAY = 18

#: **The flush days, exempted individually rather than by lowering the floor.**
#:
#: The floor above is 18 and the melon flush is d10-d11, so the exemption could never fire on the
#: days it was written for. Traced on seed 11 against Kawashigi's tape: 67 melons are ripe at d10 h00
#: -- more than the tape's 60 -- they reach the shed at h21-h23 so only 35 clear that day, and the
#: remaining **37 sit in the shed from d11 h00 to d11 h16** while the tape sells his own d11 melon
#: into the same book. Melon recovers ONE unit a day, so every one of those sixteen hours makes the
#: price strictly worse. There is no recovery to wait for.
#:
#: **Two days, not a lower floor.** Lowering `SELL_AT_ONCE_FROM_DAY` to 10 would also release
#: d12-d17, which nothing here has measured and where the original "nothing to win before d18"
#: reasoning still stands. This is the smallest change that reaches the defect.
#:
#: d0-d9 cannot move under any value here, so the matched opening is out of reach by construction.
SELL_AT_ONCE_DAYS = (10, 11)


def market_price(prod, inventory):
    """`kaggriculture.market_price`, or `BASE_PRICE` flat if the env is not importable."""
    if _KG is None:                                                         # pragma: no cover
        return float(RT.BASE_PRICE.get(prod, 0))
    return _KG.market_price(prod, int(inventory))


#: `townCenterSellInterval`: 12 through 1.32.5, 24 from the 1.32.6 town rebalance.
#:
#: **Read from the live CONFIGURATION, never from the env's spec file on disk.** The first version
#: opened `kaggriculture.json` from the installed env's own directory, the right instinct -- do not
#: hard-code
#: a number the env has already changed once -- but it cannot ship: `build_planner_submission.py`
#: refuses to bundle a module that touches the filesystem, because on Kaggle there is no repo and no
#: env directory to read. The `try/except` around it did not help; the bundler rejects the reference
#: statically, and correctly, since a silent fallback would have shipped a guess.
#:
#: The configuration is handed to `agent(obs, config)` every turn and carries the real value, so
#: `_note_config` below adopts it on the first call. 24 is the 1.32.6 default and only stands in for
#: the turns before a configuration has been seen.
_CENTER_INTERVAL = 24


def expected_future_drain(prod, day, n_unlocked, last_day=29,
                          unlock_interval=3, shop_interval=4, max_instances=8):
    """Units of `prod` the town will remove via shops NOT YET DRAWN, in expectation.

    `town_drain_remaining` counts only unlocked shops, which is correct for a sell decision -- you
    cannot sell into demand that does not exist yet. It is the wrong input for a PRODUCTION decision
    taken at day 6, because the herd bought now produces for the rest of the season, by which time
    most of the draws have happened.

    Each future unlock is uniform over the eight shop types, so the expected units it contributes
    per shop tick is `sum over shops selling prod of (2 if that shop sells only prod else 1) / 8`.
    For WOOL that is 2/8 = 0.25 (YARN_STORE alone, double because it is single-product); for MILK
    3/8 = 0.375. Multiplying by the ticks left after each unlock day gives the expectation.

    This is the expectation, not a strict min-max: the worst case is simply "no more useful shops",
    which the `HERD_FLOOR_*` values already bound. Taking the expectation here and the floor there
    covers the same ground as minimising regret without pretending we know the draw.
    """
    kg = _KG
    if kg is None:
        return 0.0
    shops = kg.SHOPS
    per_draw = sum((2.0 if len(prods) == 1 else 1.0)
                   for prods in shops.values() if prod in prods) / max(1, len(shops))
    if per_draw <= 0:
        return 0.0                       # MELON: carried by no shop, so no draw can ever help it
    end_step = (last_day + 1) * 24
    total = 0.0
    drawn = n_unlocked
    d = day + 1
    while d <= last_day and drawn < max_instances:
        if d % unlock_interval == 0:
            drawn += 1
            # Ticks this hypothetical shop would serve, from its unlock day to the season's end.
            total += per_draw * max(0, (end_step - d * 24)) / shop_interval
        d += 1
    return total


#: **SHOP_ADAPT_HERD -- float the cow/sheep split on the shop draw once the opening is banked.**
#:
#: The schedule's `animals_bought` rows fix the SPECIES before the board is known, and the species
#: decides which product the herd makes. Measured RED by
#: `tests/test_the_herd_follows_the_shop_draw.py`: seed 13 (WOOL absorption 570, YARN_STORE drawn
#: twice) and seed 29 (WOOL absorption 30, never drawn) both produce exactly `COW 13, SHEEP 8`.
#:
#: WOOL is carried by ONE shop of eight, and shops are drawn with replacement to a maximum of eight
#: instances, so P(no YARN_STORE all season) = 34%. On such a board the town removes 30 units of
#: wool all season against the ~160 the schedule produces, and wool floors 59 units above `I0`.
#: A sheep there is worth `8 units x ~$40 - $500` = NEGATIVE. `scripts/board_demand.py` measures the
#: absorption directly, PASS vs PASS, so it is a property of the board with no agent involved.
#:
#: **The swap is free.** COW and SHEEP both build a PASTURE (`routines.ANIMALS`), so nothing in the
#: build schedule, the pen geometry or the routing changes -- only cost (400 vs 500), first yield
#: (8 vs 6), interval (2 vs 3) and product (MILK vs WOOL).
#:
#: **The opening is deliberately untouched.** Unlocks land on days 3,6,9,...,24; weighting each by
#: its remaining drain days (27,24,21,...,6; total 132), only 20% of the season's shop demand is
#: visible by day 3 and 39% by day 6, against 55% by day 9 and 68% by day 12. The early animals also
#: have the longest payback, so they are the ones least worth gambling on a third of the evidence.
#: `SHOP_ADAPT_FROM_DAY` is where the floor ends and the floating part begins.
#:
#: Precedent: Seb varies COW 5-13 and SHEEP 5-20 across 15 games while holding STRAWBERRY at 38-45
#: and WHEAT at 19-36 (`scripts/board_demand.py` part B). He floats exactly this axis.
SHOP_ADAPT_HERD = True

#: Days strictly before this keep the reference schedule's species mix; from here the cow/sheep
#: split is re-derived from the shops on every turn.
#:
#: **Day 3, because that is the first unlock and the herd is bought early.**
#: A first version used day 11, on the reasoning that 55% of the season's shop-weighted demand is
#: visible by then against 20% at day 3. That reasoning was right about the evidence and wrong about
#: the decision, because it ignored what is left to decide: `split` is anchored on `state["bought"]`,
#: which never decreases, so every animal already purchased is already committed. The schedule's
#: rows all sit at day 10 or earlier, so by day 11 there was almost nothing left to steer, and the
#: test measured it -- seed 29 (WOOL drain 19) still ended with MORE sheep than seed 13 (drain 247).
#:
#: One shop is weak evidence, but it is evidence about the only thing that matters here: whether
#: YARN_STORE exists. It is one shop of eight, so seeing it at day 3 is a large update, and not
#: seeing it is a small one -- which is the right asymmetry, since the floor bounds the downside of
#: guessing wrong early while the upside of guessing right compounds over 27 remaining days.
#: **Day 6, which is where the tapes actually diverge.** All ten Seb games are identical through
#: `d4:COW`; the first differing purchase is day 6 (`90997714` d6:COW) or day 7 (`91267247` d7:SHEEP).
#: Day 6 is also the SECOND unlock, so he treats one shop as not enough and two as enough -- which
#: matches the arithmetic: after one draw, P(YARN_STORE still to come) is 1 - (7/8)**7 = 61%.
SHOP_ADAPT_FROM_DAY = 3

#: The floor: animals bought regardless of what the town turns out to want. Everything the schedule
#: asks for ABOVE this floats on the shop draw from `SHOP_ADAPT_FROM_DAY`.
#:
#: The reference schedule asks for COW 13 / SHEEP 8, so 21 total with 17 floating at these values.
#: The floor is deliberately the public meta's own opening -- the C-cluster family is described as a
#: "3 cows + 1 sheep floor" in `reference/community_notebooks/kaggriculture-findings-from-zero-to-
#: top-meta/` -- rather than a number chosen here, because the opening is the part no shop evidence
#: can inform: barely a fifth of the season's shop-weighted demand is on the board by day 3.
#:
#: A floor above zero is not merely a hedge. Animals produce fertilizer daily whatever the price of
#: their product, and MILK is carried by three shops of eight, so P(no milk shop at all) is 2.3%.
#: **Read off the tapes, not chosen.** All ten of Seb's 1.32.6 games open with the identical five
#: purchases -- `d0:COW d0:SHEEP d1:COW d3:COW d4:COW` -- and only diverge from day 6 onward. Four
#: cows and one sheep is therefore his committed opening, and the minimum of each column across all
#: ten games is exactly 5 COW and 5 SHEEP, so nothing below this is ever regretted.
HERD_FLOOR_COW = 2
HERD_FLOOR_SHEEP = 3

#: **SHOP_ADAPT_CROPS -- float the crop inside a cadence pair on the shop draw. The herd's rule, one
#: field over.**
#:
#: `_refresh_pins` builds its planting target from the schedule's `plants` rows and reads nothing
#: else, so the same 24 WHEAT / 17 MELON / 41 STRAWBERRY goes into the ground on every board. That is
#: the identical defect `SHOP_ADAPT_HERD` was written for, and the draw moves crop demand further
#: than it moves the herd's. Measured over the 87 recorded ladder tapes in
#: `data/seed_scripts/top_guys`, reading each game's closing `market.inventory` against its own
#: `town.unlocked_shops` -- units the town removes in a season:
#:
#:     STRAWBERRY      387 .. 1282       4 shop types of 8 carry it
#:     TOMATO          208 ..  924       2 of 8
#:     CARROT           29 ..  924       2 of 8, but PET_CAFE is single-product so it counts double
#:     WHEAT           745 .. 1282       5 of 8, the most widely carried
#:
#: A 32x swing on carrot is not noise, and it is not a guess: shops are `shared: True` in the
#: observation, so this is a fact handed to us every turn and currently thrown away.
#:
#: **The swap is free only inside a cadence pair.** The herd's swap costs nothing because COW and
#: SHEEP both build a PASTURE. The crop analogue of "same pen" is "same cadence", because cadence is
#: what the tour is cut against -- swap a one-shot for an ongoing crop and every watering and harvest
#: rhythm downstream moves:
#:
#:     WHEAT       first_yield_day  2   one-shot   max_yield_day  4
#:     CARROT      first_yield_day  2   one-shot   max_yield_day  3
#:     TOMATO      first_yield_day  8   ongoing    interval 1
#:     STRAWBERRY  first_yield_day 10   ongoing    interval 2
#:
#: **MELON is deliberately in no pair.** Its appetite is 29 on every board that exists -- no shop
#: carries it, so only the town centre eats it, and the 87 tapes close with a melon SURPLUS of +38 to
#: +158 without exception. Whether to plant melon is therefore a fixed-quantity question that no draw
#: can inform, and a different one; bundling it here would confound the two.
#: **OFF as of 2026-08-11, on evidence from 2,744 ladder seats. Do not switch it back on with these
#: pairs.** `docs/the_ladder_is_two_scripts.md` counts every PLANT action in the official episode
#: datasets for 2026-08-09 and -10:
#:
#:     WHEAT       362,044   69.3%
#:     STRAWBERRY  104,461   20.0%
#:     MELON        54,795   10.5%
#:     CARROT          796    0.2%
#:     TOMATO            3    0.0%   (three actions, in one game, all season)
#:
#: Both pairs below swap TOWARD the two crops the entire ladder has priced at zero. Carrot growers
#: bank below the field median ($79,847 vs $82,136); the single tomato grower banked $58,119. The
#: local sweep measured the same thing independently -- 0.806 against HEAD's 0.871 over 232 matched
#: games -- so two instruments agree and the cadence-pair reasoning was simply pointed the wrong way.
#: It was correct that the pairs are interchangeable at no cost to the routing, and that is not the
#: question that decides a crop.
#:
#: **The obvious replacement pair does not work either, and the reason is worth keeping.**
#: `STRAWBERRY <-> MELON` is the axis the field actually varies (Script A 37/19, Script B 42/24,
#: THUNDER 31..39) and it is cadence-compatible -- same first-yield day, both hold the tile to the
#: end. But `_adapt_crops` scores on `town_drain_remaining`, and melon's drain is 29 units a SEASON,
#: so the headroom goes negative after three tiles and the rule would cap melon at ~3 where every
#: winning script plants 19-24.
#:
#: That is the real defect, and it is upstream of the pairs: **the headroom model treats the town's
#: drain as a cliff when the price curve is a slope.** A melon sold past the drain still fetches $229
#: at 50 units above I0 and $166 at 100. Any rule built on "units the town will eat" will therefore
#: under-plant every steep-curve, low-drain product. The proper fix is to score the marginal unit off
#: `market_price` at the inventory everything already committed leaves behind -- not a constant, not
#: a drain count.
#:
#: **`STRAWBERRY <-> MELON` was tried on 2026-08-11 and is STRUCTURALLY INCAPABLE of adapting.**
#: It is the pair the field actually varies (Script A 37/19, Script B 42/24, THUNDER 31..39) and it
#: is cadence-compatible -- same first-yield day, both hold their tile to the season's end -- so it
#: looked like the one defensible pair left. Measured on the schedule's own row (STRAWBERRY 41 /
#: MELON 17) across four very different draws:
#:
#:     4x SMOOTHIE (strawberry-rich)     STRAW 54   MELON 4
#:     no strawberry shop at all         STRAW 54   MELON 4
#:     the 91888327 loss board           STRAW 54   MELON 4
#:     2 strawberry shops (typical)      STRAW 54   MELON 4
#:
#: **Identical on every board**, and it moves melon from 17 to 4 against a field that plants 19-24.
#: The reason is not a tuning miss: no shop carries melon, so its drain is 29 units on EVERY board
#: that can be drawn. With one side of the pair constant, the only thing that can move is
#: strawberry's headroom, and that is always large enough to take everything after melon's fourth
#: tile. **A pair whose member has board-independent demand cannot produce a board-dependent split.**
#:
#: The weeds argument for melon -- that a tile lost to a missed watering never delivers its 12 units,
#: so the field's 19-24 tiles are sized for what survives -- is a good reason to think melon is worth
#: MORE than the drain implies. It is not a reason this pair can adapt, because nothing on the board
#: moves melon's side of the comparison either way.
#:
#: The axis the field really trades is **wheat against strawberry+melon** (Script A plants 144 wheat
#: and 56 straw+melon; Script B 108 and 66). Wheat's demand does vary with the draw -- 5 of 8 shop
#: types carry it, 745 to 1,461 units. That is the pair worth building, and it needs the marginal-
#: revenue scoring above plus a schedule that plants wheat at all. Ours plants 24.
SHOP_ADAPT_CROPS = False

#: Kept so the disabled machinery stays readable and its tests keep running. Every pair tried so far
#: is recorded on the flag above; none of them should be re-enabled as written.
CROP_SWAP_PAIRS = (("WHEAT", "CARROT"), ("TOMATO", "STRAWBERRY"))

#: Days strictly before this keep the schedule's own crops; from here the mix floats every turn.
#:
#: **Day 6, the same day and for the same reason as `SHOP_ADAPT_FROM_DAY`.** Unlocks land on days
#: 3,6,9,...,24; weighting each by the drain days left to it, 20% of the season's shop demand is
#: visible at day 3 and 39% at day 6. One draw of eight is too little to commit ground to, two is
#: enough to move on, and the tapes put Seb's first divergent purchase on exactly day 6.
#:
#: Unlike the herd there is no separate numeric floor, and that is not an omission. A floor bounds
#: the downside of reading the draw wrong; here `min(units, headroom)` already does it -- a crop
#: whose book is spoken for scores zero rather than negative, so a pair whose demand has gone can
#: never be pushed past the point where it stops paying, and the day gate protects the opening.
CROP_ADAPT_FROM_DAY = 6


#: Shop types whose drain removes STRAWBERRY from the town -- four of the eight in `routines.SHOPS`.
#: Shops are drawn WITH REPLACEMENT, so this counts INSTANCES, not distinct types: two SMOOTHIE_SHOPs
#: drain twice as much as one.
STRAWBERRY_SHOPS = ("BRUNCH_SPOT", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP", "FARMERS_MARKET")

#: **Strawberry tiles to hold, indexed by strawberry-draining shop INSTANCES unlocked at
#: `STRAWBERRY_FLOAT_FROM_DAY`.**
#:
#: Our rows ask for 41-42 on every board. `market_price` is a pure function of persistent town stock and
#: the only thing that removes strawberry is a shop that carries it, so the right tile count is a
#: function of the draw -- and strawberry halves just 31 units above `I0`, the second-most fragile book
#: in the game after wool.
#:
#: Read off tetsuya's 79 recorded seats (#1, rating 3156.4): tiles standing at d20 against the
#: strawberry-draining shops visible at d12.
#:
#:     drains   0 -> 25.5    1 -> 26.4    2 -> 34.9    3 -> 36.4    4 -> 36.8
#:     wheat    0 -> 28.0    1 -> 21.8    2 -> 21.3    3 -> 19.0    4 -> 18.0
#:
#: The step sits between 1 and 2 drains rather than sloping, which is what makes this a table.
#:
#: **A first cut of this lost $28,259 and it was NOT this table that was wrong.** Capping strawberry
#: while leaving the route tables solved for 41-42 tiles measured the mismatch, not the allocation:
#: wheat fell too on every arm that moved (124->120, 133->125, 128->124), because
#: `_apply_precomputed` keys each stop on an exact `(tile, ops)` tuple and a day whose crop mix has
#: changed no longer matches the route solved for it. The routes and the mix are one artifact and have
#: to move together. See `docs/the_tapes_are_both_strawberry_rich_2026-08-19.md`; this version ships
#: only alongside route tables re-solved against it.
STRAWBERRY_TILES_BY_DRAIN = (26, 26, 35, 36, 37)

#: Days strictly before this keep the row's own strawberry count.
#:
#: **Day 12, because that is where the evidence is and where our authority starts.** The table above is
#: keyed on shops visible at d12 -- four draws, 68% of the season's shop-weighted drain. It is also the
#: first day we decide anything: d4-d11 are replayed from the tape, so the opening's strawberry is
#: committed whatever the draw says, and 37 of 42 tiles already stand at d12 dawn on the strawberry arm.
#:
#: **The draw is read from the LIVE observation, never from a tape file.** A forced `cfg["seed"]`
#: re-rolls the shops, and the shop draw is one of only two RNG consumers in the environment. Reading
#: the tape JSONs instead cost a wrong three-board table and a reverted tomato gate on 2026-08-19.
STRAWBERRY_FLOAT_FROM_DAY = 12


#: **WOOL_SHOP_SETS_THE_HERD -- an EARLY YARN_STORE makes the herd sheep-heavy.**
#:
#: Re-measured 2026-08-15 over **74 distinct** downloaded games of the #1 player -- every replay on
#: disk carrying his seat, deduplicated by episode id. Shops unlock every third day, so draw #N
#: lands on day 3N. Against the position of the FIRST yarn store:
#:
#:     yarn first at draw #1 (d3)    : COW  6, SHEEP 9.05, total 15.05   n=21   quads 4.00
#:     yarn first at draw #2 (d6)    : COW  6, SHEEP 9.26, total 15.26   n=23   quads 4.00
#:     yarn first at draw #3 (d9)    : COW  6, SHEEP 6.00, total 12.00   n= 7   quads 3.00
#:     yarn first at draw #4+ (d12+) : COW 10, SHEEP 4.00, total 14.00   n=34   quads 3.00
#:     no yarn store at all          : COW 9.64, SHEEP 4.36, total 14    n=56   quads 3.00
#:
#: **The earlier version of this table said "SHEEP 12, total 18" on draws #1-#2 and it was wrong.**
#: He never runs 18 animals; the maximum over all 74 seats is 16. The correction was already
#: recorded in `tests/test_the_herd_split_answers_the_recorded_shop_draw.py` on 2026-08-13 and never
#: propagated to here or to `tests/test_the_herd_follows_the_wool_shop.py`, which is how a wrong
#: number survived two weeks and sent a session chasing a herd size that does not exist.
#:
#: So `COW == 6` iff a yarn store is among the FIRST THREE draws: 24/24 yes, 0/42 no. A perfect
#: classifier over 66 games, and the reason this flag now carries a draw limit. **The 16 games at
#: draw #4 or later are what the first version of this rule got wrong** -- it fired on a yarn store
#: appearing at any point in the season, and would have cut the herd to 6 cows on a d12 unlock where
#: he keeps 10. Wool arriving at d12 has only six production cycles left; that is the whole content
#: of the cutoff.
#:
#: Milk-shop count predicts nothing that yarn does not already explain -- COW 6 occurs at one milk
#: shop and at two, and at 0 milk shops the mean cow count is still 6.57. The headroom greedy below
#: ties to COW on the reasoning that "MILK is carried by three shops against WOOL's one", which is a
#: true statement about the shop table and the wrong way round as a conclusion: three shops sharing
#: milk is what floors the milk price. Measured on our own fills, wool went out at
#: $160/$109/$181/$146 on d24-d28 while milk took $1-$5 all season.
#:
#: **The herd TOTAL moves too -- but only on FOUR quadrants, and that closes the question for us.**
#: Cross-tabulating the same 74 seats by quadrants owned:
#:
#:     quads  herd   n
#:         3    12    4
#:         3    14   47          <- three quadrants NEVER exceeds 14, 51 seats
#:         4    13    1
#:         4    14    4
#:         4    15    9
#:         4    16    9
#:
#: We play three quadrants, and on three quadrants he caps at 14 -- exactly the count the schedule
#: fixes. So there is no herd-total gap to close at our board size, and `_herd_split` being unable
#: to raise `want_total` costs nothing. Growing the herd is part of buying the fourth parcel, not a
#: separate change: see `docs/fable_fourth_quadrant_reopened_2026-08-15.md`, which reaches the same
#: place from the field data.
WOOL_SHOP_SETS_THE_HERD = True

#: What the leader holds cows to once an early wool shop is on the board. 24 of 24 such games ran
#: exactly 6 cows and put the entire remaining budget into sheep; no yarn game ran any other number.
WOOL_SHOP_COW_CAP = 6

#: How many of the town's draws count as "early" for the rule above. Three, because draw #3 lands on
#: d9 and is the last one he responds to -- see the table: #3 still gives COW 6, #4 does not.
WOOL_SHOP_DRAW_LIMIT = 3

#: **What he runs when NO yarn store lands early -- the other half of the same step function.**
#:
#: Measured 2026-08-13 over all 67 recorded カワシギ seats, by the draw his first yarn store lands on:
#:
#:     first yarn at draw #1 (d3)   n=10   COW  6.00   SHEEP 9.10
#:     first yarn at draw #2 (d6)   n=11   COW  6.00   SHEEP 9.27
#:     first yarn at draw #3 (d9)   n= 3   COW  6.00   SHEEP 6.00
#:     first yarn at draw #4+       n=16   COW 10.00   SHEEP 4.00
#:     no yarn store at all         n=27   COW  9.63   SHEEP 4.37   (22 at COW 10, 5 at COW 8)
#:
#: The cap branch below reproduced the top three rows 24/24. The bottom two were left to the
#: drain-aware greedy, **and it gives 13 where he runs 10** -- wrong on 43 of his 67 seats. Pinning
#: both branches takes it to 62/67; the greedy alone scores 1/67. The five that remain are
#: unreachable by any constant, because he himself runs COW 10 in 22 of those games and COW 8 in 5.
#:
#: **Fitted to him alone, deliberately.** Across the 451 recorded seats of the whole field the same
#: split is mush -- early-yarn mean COW 7.26, only 41% at the cap even in the top decile. A
#: drain-weighted linear fit scored better against that mean and was rejected: it would have
#: replaced a classifier that is perfect on the player we are trying to beat with regression toward
#: the players we already beat. `tests/test_the_herd_split_answers_the_recorded_shop_draw.py` keeps
#: the trap executable.
WOOL_SHOP_NO_YARN_COW = 10

#: **The earliest day a goose goes in.** Measured over tetsuya's 78 games: his first bird lands on
#: day 6 and there is nothing at all on d0-d5. `data/logs/tets_rule_fit_2026-08-19.log`.
GOOSE_FROM_DAY = 6

#: The shop types that drain MILK (`reference/kaggriculture.py:105,108,110`).
MILK_DRAINING_SHOPS = ("PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP")
#: **A classifier, not a slope.** Two milk shops visible by d9 implies a big herd in 21 of 21 of his
#: late/no-yarn games -- zero false positives. Fitting a LINE through the same variable measured
#: -16 points, because his response is bimodal at COW 6 and COW 12 and a line lands between them.
MILK_SHOPS_FOR_A_BIG_HERD = 2
COW_ON_A_MILK_RICH_BOARD = 12
COW_ON_A_MILK_POOR_BOARD = 7
#: Three shops are drawn by d9; before that the count carries no evidence. d0-d7 already runs at
#: ~90% on the opening and the gradient, so the classifier is kept out of it.
MILK_CLASSIFIER_FROM_DAY = 9


#: **Fit the whole herd to the leader's THREE-QUADRANT seats, which is the board we play.**
#:
#: Measured 2026-08-15 over 74 distinct episodes on disk carrying his seat, restricted to the 51
#: that own three quadrants. Seat alignment verified on `92498144`, where `farms[0]` is カワシギ at
#: $149,998 and matches `rewards[0]`. He has exactly three answers there:
#:
#:     COW  SHEEP  total   n
#:       6      6     12    4     every one has its first YARN_STORE in draws 1-3
#:       8      6     14    5     four of five have exactly ONE milk shop and no yarn store
#:      10      4     14   42
#:
#: Exhaustive search over both thresholds (`data/logs/kawa_q3_rule_search.log`) puts the best fit at
#: **DELETED 2026-08-19: the better-FITTING herd rule, which is not the better rule for us.**
#:
#: `HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE` and its four constants (`EARLY_WOOL_SHEEP = 6`,
#: `MILK_POOR_SHOP_COUNT = 1`, `MILK_POOR_COW = 8`, `MILK_POOR_SHEEP = 6`) shipped off from
#: 2026-08-15 and are gone. Keep the finding, not the code:
#:
#: It predicted the leader's (COW, SHEEP) at **49/51 = 96.1%** against the shipped rule's
#: 42/51 = 82.4% (`data/logs/kawa_q3_rule_search.log`), by taking the herd TOTAL down to twelve.
#: That only pays if the freed capacity becomes crops -- he converts it into ~12 more plantings and
#: ~29 more waters at an unchanged hire count -- and **we have no logic that does that**, so we
#: would take the cost and idle the gain. We already idle 1365 unit-turns a season against his 660.
#: Worse, the early-yarn branch fires exactly where wool is well drained ($24-$248 a close, drain
#: 240-504), so it surrenders ~16 units at up to $240 each to save $1,000.
#:
#: Re-derive it only alongside logic that spends the freed turns on planting.


def _herd_split(want_total, bought, day, hour, unlocked_shops, last_day=29):
    """Re-decide the cow/sheep species mix, keeping the schedule's COUNT exactly.

    Extracted from `_place_animals` so it can be tested directly; the body below the wool rule is
    unchanged. Anchored on what is already BOUGHT, so the target can only grow and the total is
    capped at the schedule's own count -- a split recomputed from scratch each turn buys up to both
    ceilings as the choice flips, measured once at COW 20 + SHEEP 18 against a schedule asking 21.
    """
    total = want_total["COW"] + want_total["SHEEP"]
    split = {a: bought.get(a, 0) for a in ("COW", "SHEEP")}
    # **The geese are carried, not decided.** He finishes with at least one in 43 of his 78 games,
    # a mean of 1.2 a game and never more than 4, always placed on days 6-13. Nothing measured so
    # far says WHICH boards get them, so this invents no rule: the count the schedule rowed is
    # passed straight through, and only COW/SHEEP are re-split below.
    #
    # It has to be a key of the returned split even so. Without one the caller's greedy has no
    # GOOSE bucket to spend, so every goose he places scores as a miss against a rule that is
    # structurally unable to name it -- 91 of 1187 placements before this line existed.
    #
    # **And not before `GOOSE_FROM_DAY`.** He places his first bird on day 6 and never earlier --
    # measured over the 78, the distribution is d6:3 d7:8 d8:3 d9:9 d10:8 d11:28 d12:23 d13:13, with
    # nothing at d0-d5. Offered at day 0 the bucket gets spent on the opening and displaces a sheep,
    # which is a miss twice over: the goose is early and the sheep is missing.
    if want_total.get("GOOSE") and day >= GOOSE_FROM_DAY:
        split["GOOSE"] = max(bought.get("GOOSE", 0), int(want_total["GOOSE"]))
    # The floor is a commitment, so honour it even if the book for its product looks empty.
    # **Sheep first, and that ordering is the opening.** Measured over all 78 recorded tetsuya
    # games: every single one places `SHEEP SHEEP SHEEP COW COW` on day 0, 78/78, no exceptions.
    # The floors are applied in that order so the greedy that spends them reproduces it.
    split["SHEEP"] = max(split["SHEEP"], min(HERD_FLOOR_SHEEP, total))
    split["COW"] = max(split["COW"], min(HERD_FLOOR_COW, total - split["SHEEP"]))

    # **An undrawn deck is not a known deck.** On day 0 `unlocked_shops` is EMPTY, and the wool
    # branch below read that as "this board has no yarn store" and jumped straight to
    # `WOOL_SHOP_NO_YARN_COW` -- ten cows, decided before a single shop had landed. That is the
    # single biggest source of disagreement with him: his first five animals are the opening above
    # and ours were cows.
    #
    # Returning here allocates only what the opening commits to and leaves the rest of the herd for
    # the draws that have not happened yet. `_herd_split` is called again every turn, so the moment
    # the first shop lands the full rule below takes over with real evidence.
    if not unlocked_shops:
        return split

    # **The wool shop decides it, and it decides it outright.** Cows are held at the cap and every
    # animal still unbought goes to sheep, which is what reproduces his 6/8 at a herd of 14 and his
    # 6/12 at 18. `bought` still floors the cows, so this can never unbuy one that exists.
    #
    # **Only the first three draws count.** `unlocked_shops` is in unlock order and a draw lands
    # every third day, so slicing it is slicing by day: [:3] is "unlocked by d9". He does not respond
    # to a yarn store that arrives at d12 or later -- 16 games, all COW 10 -- and the unsliced test
    # would have cut those to 6.
    if WOOL_SHOP_SETS_THE_HERD:
        # **Both branches of his step function are pinned, not just the capped one.** An early yarn
        # store means 6 cows; anything else means 10. Leaving the second case to the greedy below
        # was wrong on the majority of his recorded seats -- see `WOOL_SHOP_NO_YARN_COW`.
        # **He is a GRADIENT in the draw, not a step.** カワシギ is two-valued -- 6 cows on an early
        # yarn store, 10 otherwise -- and that is what this line used to encode. Tetsuya walks up
        # with the draw instead, measured over his 78 games:
        #
        #     first YARN_STORE at draw   #1    #2    #3
        #     his COW count               4     5     6      (8/8, 10/11, 5/9 at the median)
        #
        # which is `3 + draw`, and it is written below as `CAP - (LIMIT - draw)` so it still passes
        # through `WOOL_SHOP_COW_CAP` at `WOOL_SHOP_DRAW_LIMIT` -- the old behaviour is the last
        # point of the new line, not a case beside it.
        _draw = next((i + 1 for i, s in enumerate(list(unlocked_shops or ()))
                      if s == "YARN_STORE"), None)
        if _draw is not None and _draw <= WOOL_SHOP_DRAW_LIMIT:
            target = WOOL_SHOP_COW_CAP - (WOOL_SHOP_DRAW_LIMIT - _draw)
        else:
            # **A late or absent yarn store is decided by MILK demand, not by wool.** His 50
            # late/no-yarn games are bimodal at COW 6 and COW 12, so the yarn index cannot separate
            # them -- but the count of milk-draining shops can, and the response is linear in it.
            # PIZZA_SHOP, ICE_CREAM_SHOP and SMOOTHIE_SHOP all take MILK
            # (`kaggriculture.py:105,108,110`). Measured over those 50 games:
            #
            #     milk shops    1     2     3     4     5     6
            #     mean COW    6.0   7.5   8.6   9.8  10.9  12.0
            #
            # which is `4.8 + 1.2 * milk` to within 0.2 everywhere.
            # `data/logs/tets_bimodal_2026-08-19.log`.
            #
            # **The count is the EXPECTED FINAL one, never the count visible today.** Fitting on the
            # final board and reading `unlocked_shops` straight is the census-vs-decision error, and
            # it measured -16 points when tried that way: at day 3 two shops have landed, the milk
            # count is near zero, and the line asks for 6 cows on a board that ends at 12.
            #
            # Shops are drawn WITH REPLACEMENT from eight types, capped at `MAX_SHOP_INSTANCES` = 8
            # (`kaggriculture.py:104-117`), and three of the eight drain milk -- so every undrawn
            # instance is worth 3/8 of a milk shop in expectation. The corpus agrees: a mean of 3.3
            # milk shops per 8 draws is 0.41 against the uniform 0.375, which is small-sample noise
            # rather than a biased deck.
            # **REVERTED 2026-08-19. Measured twice, negative both times, and the second run says
            # why the first one failed for a DIFFERENT reason than I thought.**
            #
            #     visible milk count, fitted on the final board      65.6% -> 46.4%
            #     expected final milk count, undrawn at 3/8 each     65.6% -> 63.0%
            #     flat `WOOL_SHOP_NO_YARN_COW`                       65.6%
            #
            # The expectation correction recovered thirteen of the sixteen lost points, so reading a
            # partial draw as if it were final WAS a real defect. It was not the only one.
            #
            # **A linear fit to a bimodal response lands between both modes and matches neither.**
            # His late/no-yarn boards are not spread around a mean, they cluster at COW 6 and COW
            # 12; the per-milk-count means of 6.0 ... 12.0 are averages OVER that split, not a
            # trend within it. At three milk shops nine of his boards go low and eight go high, so
            # the fitted 8.6 is a value he essentially never plays. The flat 10 wins because it at
            # least sits on the larger mode.
            #
            # A rule that beats the flat number has to CLASSIFY -- find whatever separates his 6
            # boards from his 12 boards -- not interpolate.
            #
            # **2026-08-20: it IS the milk count. It had to be a THRESHOLD, and read at the
            # decision.** Re-measured at the GAME level (50 late/no-yarn games, not 213 placements
            # -- a game contributing twelve animals is one decision repeated, and the placement-level
            # cut was pseudo-replication). Against his cow count, every other candidate is flat to
            # three digits: quadrants 2.00 vs 2.00, shops drawn 3.00 vs 3.00, money 2760 vs 2694, and
            # the OPPONENT's herd -0.05 to -0.32. Milk shops visible at d9 is 0.68 vs 1.81.
            #
            #     milk@d9 >= 1  -> high cow    37/50 = 74.0%   (fp 13, fn 0)
            #     milk@d9 >= 2  -> high cow    40/50 = 80.0%   (fp  0, fn 10)
            #     always-high baseline         31/50 = 62.0%
            #
            # Twenty-one of twenty-one games with two milk shops by d9 go high-cow. The FALSE
            # POSITIVE count is zero, which is what makes it usable: "two milk shops implies a big
            # herd" holds without exception, even though the converse does not.
            # `data/logs/tets_split6v12_2026-08-20.log`.
            #
            # Gated from `MILK_CLASSIFIER_FROM_DAY` because the evidence does not exist before it --
            # three shops are drawn by d9 -- and because d0-d7 already runs at ~90% on the opening
            # and the gradient. This only touches the region that is broken.
            target = WOOL_SHOP_NO_YARN_COW
            if day >= MILK_CLASSIFIER_FROM_DAY:
                _milk = sum(1 for s in (unlocked_shops or ()) if s in MILK_DRAINING_SHOPS)
                target = (COW_ON_A_MILK_RICH_BOARD if _milk >= MILK_SHOPS_FOR_A_BIG_HERD
                          else COW_ON_A_MILK_POOR_BOARD)
        if split["COW"] <= target:
            split["SHEEP"] = max(split["SHEEP"], total - max(split["COW"], target))
            split["COW"] = max(split["COW"], min(target, total - split["SHEEP"]))
            return split

    step_now = day * TPD + hour
    days_left = max(0, last_day - day)
    headroom, per_animal = {}, {}
    for a in ("COW", "SHEEP"):
        spec = R.ANIMALS[a]
        # Yields left for an animal bought NOW: nothing before `first_yield_day`, then one every
        # `interval` days. A late sheep is worth much less than a late cow -- 6 days then every 3,
        # against 8 days then every 2.
        per_animal[a] = max(0, (days_left - spec["first_yield_day"]) // spec["interval"])
        # **Count the shops that have NOT been drawn yet.** `town_drain_remaining` counts only what
        # is unlocked, so reading it alone treats the draws so far as final.
        headroom[a] = (town_drain_remaining(spec["product"], step_now, unlocked_shops)
                       + expected_future_drain(spec["product"], day, len(unlocked_shops), last_day)
                       - split[a] * per_animal[a])
    # One animal at a time: each assignment consumes the headroom that justified it, so the
    # objective is separable and concave in the count per species -- where greedy is optimal.
    for _ in range(max(0, total - split["COW"] - split["SHEEP"])):
        pick = "COW" if headroom["COW"] >= headroom["SHEEP"] else "SHEEP"
        split[pick] += 1
        headroom[pick] -= per_animal[pick]
    return split


def _herd_through_day(sched, day, split):
    """Today's cumulative COW/SHEEP target: the schedule's rows in day order, re-labelled to `split`.

    Walks every row from day 0 so the allowance is consumed in the order the season buys in, and
    counts only the heads rowed on or before `day`. A head whose scheduled species still has season
    allowance keeps it; one whose species is exhausted takes the other, which is how a board that
    wants a different mix still gets it. Species other than COW and SHEEP are not the split's
    business and are left to the caller's own accumulation.
    """
    room = {"COW": int(split["COW"]), "SHEEP": int(split["SHEEP"])}
    out = collections.Counter()
    for dd in sorted(sched):
        for a in ("COW", "SHEEP"):
            for _ in range(int((sched[dd].get("animals_bought") or {}).get(a, 0) or 0)):
                pick = a if room[a] > 0 else ("SHEEP" if a == "COW" else "COW")
                if room[pick] <= 0:
                    continue
                room[pick] -= 1
                if dd <= day:
                    out[pick] += 1
    return out


#: **How many of the schedule's animals become GEESE, swapped in place and as early as possible.**
#:
#: RESTORED. `7a88d30` ("Delete the geese rather than leave a losing flag in the tree") deleted this
#: mechanism on the strength of `c9c1c18`'s measurement: "-21k a game at one bird in the mirror, and
#: 42 points of win rate against 24 recorded opponents at two." **That measurement is void.**
#: `SELLABLE` (above, see its docstring) held only six of the env's nine product names for most of
#: this project's life, and EGG was never one of them -- so every goose in every arm that was ever
#: measured produced eggs that could not be sold under any flag, on any day. The geese paid every
#: cost (the $300 purchase, the COOP, the daily FEED and CARE) and banked none of their only revenue
#: line. "Geese lose $21k a game" measured a bird with its market amputated, which is exactly the
#: `CLAUDE.md` pattern -- "animals don't pay" has now been an artifact of something the code could
#: not express five separate times.
#:
#: A goose is still, on paper, the cheapest animal in the game and the fastest to first yield:
#:
#:     GOOSE   cost $300   first_yield_day 4   interval 1   max_held 4   product EGG
#:     COW     cost $400   first_yield_day 8   interval 2   max_held 6   product MILK
#:     SHEEP   cost $500   first_yield_day 6   interval 3   max_held 6   product WOOL
#:
#: -- it yields DAILY from day 4, against a cow's every second day from day 8 and a sheep's every
#: third from day 6, so it is also the animal most sensitive to sitting off a zero-walk cell (see
#: `HERD_GEESE_EARLIEST`).
#:
#: **Left at 0.** Restoring the mechanism is not a claim that geese pay -- it is a claim that the
#: question can now be asked, because EGG reaches the market. The joint search (`scripts/
#: product_search.py`, which already looks for this exact name) is what should decide the count; do
#: not hand-tune this flag without a fresh measurement taken with the SELLABLE fix in place.
#:
#: **The swap is free.** GOOSE builds a COOP rather than a PASTURE, but `BUILD_COOP` and
#: `BUILD_PASTURE` are the same op cost (`kaggriculture.py:480,486`) and the pen-placement code in
#: this file (`_place_animals`, the `kind in ("PASTURE", "COOP")` branches) is already generic over
#: `R.ANIMALS[a]["structure"]`, so nothing about the board geometry or the routing changes -- only
#: the species, and therefore the structure kind and the product.
HERD_GEESE = 0

#: The order geese are taken in, cycled. See `HERD_GEESE`.
HERD_GEESE_FROM = ("SHEEP", "COW")

#: **The earliest day each successive goose may be bought -- one per zero-walk cell.**
#:
#: A pen ON a shed-access tile runs its whole daily loop -- draw feed, feed, care, collect, harvest
#: -- without a single move (`routines.py`, "the ranch cell"). Off those cells the pen pays a walk
#: every visit, and a GOOSE is the animal visited most often: `interval 1`, so it produces every
#: night, against a COW's every second and a SHEEP's every third. So the goose is exactly the animal
#: that most needs a zero-walk cell, and there are only four -- of which one is owned at the start:
#:
#:     (4,4)  NW   0 parcels               day 0
#:     (5,4)  NE   1 parcel   $1,000       the reference schedule buys NE around day 6
#:     (4,5)  SW   2 parcels  $3,000       ~day 10
#:     (5,5)  SE   3 parcels  $7,000       late, if ever
#:
#: Pen spots are already allocated shed-access-first (`_place_animals`'s `PEN_SPOTS` search), and
#: `swap_in_geese` rewrites the `places` row in order, so a goose whose row is late enough takes its
#: cell by construction; this table is what stops one being bought before its cell exists.
HERD_GEESE_EARLIEST = (0, 6, 10, 21)


def swap_in_geese(schedule, geese=None):
    """A COPY of `schedule` with `geese` of its animals turned into GOOSE, in place and earliest first.

    A copy, because the schedule handed in is Victor's recording and every other reader of that dict
    would otherwise see the swap too.

    "In place" means the row keeps its animal COUNT: a day that bought two animals still buys two.
    That matters because the pen-build schedule (`want_pens` in `_place_animals`) is paced to those
    counts, so changing them strands an animal in the shed or leaves a pen empty -- and `PLACE` on a
    missing structure silently no-ops.
    """
    geese = HERD_GEESE if geese is None else geese
    out = {int(d): dict(row) for d, row in schedule.items()}
    for d in out:
        out[d]["animals_bought"] = dict(out[d].get("animals_bought") or {})
        if out[d].get("places"):
            out[d]["places"] = list(out[d]["places"])
    days = sorted(out)

    def _take_bought(species, not_before):
        """Turn one `species` into a GOOSE in the earliest `animals_bought` row at or after `not_before`."""
        for d in days:
            if d < not_before:
                continue
            row = out[d]["animals_bought"]
            if int(row.get(species, 0)) > 0:
                row[species] = int(row[species]) - 1
                if not row[species]:
                    del row[species]
                row["GOOSE"] = int(row.get("GOOSE", 0)) + 1
                return True
        return False

    def _take_place(species, not_before):
        """The same, in the `places` row.

        **`places` is a SECOND statement of the species and both must move together.** The pen
        planner reads `places`, not `animals_bought` (`_place_animals`: `wanted = [a for d ... for a
        in sched[d]["places"]]`), and pins `("BUILD", a, ...)` from it -- so swapping only the
        purchase buys a goose and builds it a PASTURE. `PLACE` is a silent no-op on the wrong
        structure, so the bird sits in the shed for the rest of the season.
        """
        for d in days:
            if d < not_before:
                continue
            for i, a in enumerate(out[d].get("places") or ()):
                if a == species:
                    out[d]["places"][i] = "GOOSE"
                    return True
        return False

    taken = 0
    for k in range(max(geese, 0)):
        # **One goose per zero-walk cell, and not before that cell exists.** See `HERD_GEESE_EARLIEST`.
        floor = HERD_GEESE_EARLIEST[k] if k < len(HERD_GEESE_EARLIEST) else HERD_GEESE_EARLIEST[-1]
        for species in itertools.islice(itertools.cycle(HERD_GEESE_FROM), k, k + len(HERD_GEESE_FROM)):
            # **Both rows or neither.** Checked BEFORE either is touched, because a swap that moves
            # the purchase and not the pen is exactly the failure this guards against: the pen
            # planner reads `places`, so a half-applied swap buys a goose and builds it a PASTURE,
            # and `PLACE` is a silent no-op on the wrong structure.
            has_buy = any(int(out[d]["animals_bought"].get(species, 0)) > 0
                          for d in days if d >= floor)
            has_place = any(species in (out[d].get("places") or ())
                            for d in days if d >= floor)
            if not (has_buy and has_place):
                continue
            _take_bought(species, floor)
            _take_place(species, floor)
            taken += 1
            break
        else:
            # No species has both rows available this late. Another goose would have no cell and no
            # row, so stop rather than pushing one onto ordinary ground.
            break
    return out


def _adapt_crops(want, planted, live, day, unlocked_shops, last_day=29):
    """Re-decide the CROP inside each pair; never the number of tiles. Mirrors the herd's split.

    `want` is the schedule's cumulative planting target. Returns a new Counter with the same total
    per pair and the crops re-aimed at whatever the town now says it will eat.

    **Anchored on ground already committed, which is what caps the total.** The herd anchors its
    split on `state["bought"]`, because a target recomputed from scratch each turn against a counter
    that only ever grows buys up to BOTH ceilings as the choice flips -- measured at COW 20 + SHEEP
    18 against a schedule asking for 21. `planted + live` is the same anchor for ground: it never
    falls, so the target can only grow, and only up to the count the schedule itself asked for.

    **Greedy one at a time, which is provably right rather than merely careful.** Each tile consumes
    the headroom that justified it, so the objective is separable and concave in the count per crop
    -- the case where greedy is optimal. Handing the whole remainder to whichever crop leads on the
    first tile would ignore the diminishing returns: past enough strawberry the book is spoken for
    and the next tile should be tomato even on a strawberry board. Recomputed every turn, so the
    unlocks on days 9, 12, 15, 18, 21 and 24 keep moving the tiles that are still unplanted.

    **Scored in dollars, not units.** The herd could rank on unmet units alone because MILK and WOOL
    are worth $160 and $200. TOMATO and STRAWBERRY are $60 and $120, so a rule that chased units
    would trade a strawberry tile for a tomato tile whenever tomato demand ran 2:1 -- which is a
    loss. What a tile is worth is the demand it can actually capture, priced.
    """
    if _KG is None:                                                         # pragma: no cover
        return want
    out = collections.Counter(want)
    step_now = day * TPD
    for pair in CROP_SWAP_PAIRS:
        anchor = {c: planted.get(c, 0) + live.get(c, 0) for c in pair}
        # **The remainder is a PAIR total, not a sum of per-crop remainders.** Clamping each crop
        # separately throws away the surplus of whichever crop the swap has been feeding: once the
        # schedule's strawberry row has been going into tomato ground, TOMATO stands at `want 0,
        # anchor 8` and its -8 is discarded, so the pair is handed strawberry's full remainder on top
        # of the eight tiles it has already spent. Measured on the d0-d16 grid: 38 strawberry AND 22
        # tomato against a schedule asking for 41 tiles in total.
        #
        # This is the same overshoot `state["bought"]` was introduced to stop on the herd, and it
        # hid here for the same reason it hides everywhere -- the unit test built a fresh state on
        # every call, so `anchor` was always zero and the clamp never had a negative to drop.
        floating = max(0, sum(want.get(c, 0) for c in pair) - sum(anchor.values()))
        if floating <= 0:
            continue
        headroom, per_tile = {}, {}
        for c in pair:
            price = RT.BASE_PRICE[c]
            # **A tile is re-sown, so it must be costed over the season, not over one planting.**
            # `plant_prize` values ONE planting -- 3 units of wheat, 4 of strawberry -- and it is
            # already 0 once the season cannot finish the crop, which is what stops a late swap
            # planting something that never matures. But a season-wide headroom runs to the hundreds
            # of units, so scoring a 3-unit planting against it means saturation never binds and the
            # rule collapses into a fixed price comparison that ignores the draw entirely. Measured:
            # every board planted the identical mix.
            #
            # A cycle is how long the ground is occupied before it can be re-sown: `max_day` for a
            # one-shot, and for an ongoing crop the run to its last yield, `first + (max_yield-1) *
            # interval`. Checked against `kagg.economics.production`, which probed the real env --
            # TOMATO 11 days a cycle over 30 gives 2 cycles x 4 = 8, and `TILE_YIELD_PER_SEASON`
            # measures exactly 8.
            info = RT.CROP[c]
            cycle = (info["max_day"] if not info["ongoing"]
                     else info["first"] + (info["max_yield"] - 1) * max(1, info["interval"]))
            cycles = max(1, (last_day - day) // max(1, cycle))
            per_tile[c] = cycles * (RT.plant_prize(c, day) / price if price else 0.0)
            # **Count the shops NOT YET DRAWN.** `town_drain_remaining` counts only what is already
            # unlocked, which is right for a sell decision and wrong for a planting one: at day 6
            # that is two draws of eight, so "no carrot shop yet" is weak evidence and committing
            # the field against it is the largest-regret move on the board.
            headroom[c] = (town_drain_remaining(c, step_now, unlocked_shops)
                           + expected_future_drain(c, day, len(unlocked_shops), last_day)
                           - anchor[c] * per_tile[c])
        alloc = dict(anchor)
        for _ in range(floating):
            # Ties fall to the pair's first member, which is the cheaper seed. A crop whose book is
            # already spoken for scores 0, so a dead pair simply keeps the schedule's own choice.
            pick = max(pair, key=lambda c: (min(per_tile[c], max(0.0, headroom[c]))
                                            * RT.BASE_PRICE[c], -pair.index(c)))
            alloc[pick] += 1
            headroom[pick] -= per_tile[pick]
        for c in pair:
            out[c] = alloc[c]
    return out


def town_drain_remaining(prod, step, unlocked_shops, end_step=720,
                         shop_interval=4, center_interval=None):
    """Units of `prod` the town will remove from the market from `step` up to `end_step`.

    Mirrors `_town_consume` (`reference/kaggriculture.py:696-717`) exactly: a shop tick on every
    step divisible by `shop_interval` pulls 1 for each of its products (2 if it sells only one),
    and the town centre pulls `center_mult` for every product except FERTILIZER on every step
    divisible by `center_interval`.

    **Future unlocks are NOT counted, deliberately.** Which shop unlocks on which day is drawn from
    an RNG that `_spawn_weeds` has already consumed from, so it is not predictable
    (`kagg/economics/market.py:9-11`). Ignoring them under-states `D_rem`, which lowers the
    reservation price and makes the rule sell SOONER -- the safe direction, since the measured
    failure is under-selling (331 units binned, `docs/the_shed_destroys_the_harvest_2026-08-08.md`).
    """
    if _KG is None:                                                         # pragma: no cover
        return 0
    if center_interval is None:
        center_interval = int(getattr(_KG, "TOWN_CENTER_SELL_INTERVAL", 0) or 0) or _CENTER_INTERVAL
    shops = _KG.SHOPS
    per_shop_tick = 0
    for name in (unlocked_shops or []):
        products = shops.get(name)
        if not products:
            continue
        if prod in products:
            per_shop_tick += 2 if len(products) == 1 else 1
    # Ticks strictly inside [step, end_step): the drain at `step` itself lands AFTER this turn's
    # market phase (`_step` runs `_process_market` then `_town_consume`, `kaggriculture.py:909-910`),
    # so it is still available to a later offer and must be counted.
    n_shop = len(range(-(-step // shop_interval), -(-end_step // shop_interval)))
    total = per_shop_tick * n_shop
    if prod in _KG.TOWN_CENTER_PRODUCTS:
        schedule = getattr(_KG, "TOWN_CENTER_DEMAND_SCHEDULE", [(0, 1)])
        for s in range(-(-step // center_interval) * center_interval, end_step, center_interval):
            total += next(m for th, m in schedule if (s // 24) >= th)
    return int(total)


def _note_config(config):
    """Adopt whatever the host tells us, instead of trusting constants copied into this file.

    Idempotent and cheap; called on every turn.

    All three of these are *configuration*, not game constants, and each has a default baked into
    this file that is right only for the version it was last read against. That is exactly how this
    machine spent 2026-08-08 measuring `kaggle-environments` 1.32.2 while the ladder ran 1.32.6:
    `townCenterSellInterval` moved 12 -> 24, every fixture silently described a different game, and
    nothing detected it. The host hands us its own configuration, so none of them needs guessing.

    `shedCapacity` earns its place here as of 2026-08-09: `release_order` and the whole eviction
    argument are sized against it, and `_drop_inventories_to_shed` discards the overflow silently.
    """
    global _CENTER_INTERVAL, SHED_CAPACITY
    if not config:
        return
    if not hasattr(config, "get"):                                          # pragma: no cover
        return
    for key, name in (("townCenterSellInterval", "_CENTER_INTERVAL"),
                      ("shedCapacity", "SHED_CAPACITY")):
        try:                                                                # pragma: no cover
            got = config.get(key)
            if got:
                globals()[name] = int(got)
        except Exception:                                                   # pragma: no cover
            pass


def reservation_units(prod, inventory, step, unlocked_shops, supply,
                      contest=None, slip=None, end_step=720):
    """How many units of `prod` this ONE offer may carry, read off the live book.

    This is the derived replacement for `rate[prod]` -- "the largest single day the schedule ever
    asked for", a number transcribed off one 1.32.2 replay. `rate` was standing in for a real
    market fact (a big offer walks its whole size down the curve in one lockstep: wool 123 units ->
    138 took revenue $29,041 -> $21,811) and that fact is computable, per product, every turn.

    Two bounds, and the offer is whichever is larger:

    `slip` -- **the depth cap.** Every unit is quoted at the inventory the previous unit left
    (`_process_market`, `reference/kaggriculture.py:566-596`) and `_commit_unit` raises inventory by
    exactly one per unit sold (`:626-635`), so the size at which an offer stops being price-neutral
    is a property of `market_price` and nothing else. From a balanced book the units sellable before
    the price falls 10% are WHEAT 20, FERTILIZER 53, MELON 51, WOOL 19, MILK 8, STRAWBERRY 7 -- a
    seven-fold spread that a single transcribed `rate` cannot express in either direction.

    `contest` -- **the reservation floor.** `market_price` is monotone decreasing above `I0` and
    `_town_consume` (`:696-717`) lowers inventory by a deterministic `D_rem`, so the units that can
    ever clear at a price of at least `L`, across BOTH players, over the rest of the season are

        N(L) = max(0, I_L - I_now) + D_rem

    -- the gap between here and the level where the price is `L`, plus every unit the town removes,
    since each removal is one re-sale at that level. Inverting at our own remaining `supply` gives
    the price the marginal unit can actually expect, with no fitted constant:

        lambda = market_price(prod, I_now + supply - contest * D_rem)

    When `supply` exceeds the town's remaining absorption, `lambda` is BELOW the current price and
    the offer widens: there is no future in which that stock clears at today's price, so waiting
    only moves it closer to the deadline. When supply is thin, `lambda` sits at the current price
    and the offer narrows to the units that share it -- a trickle rather than a freeze, which is
    deliberate: on a book at a deficit the price is an integer plateau tens of units wide.

    `supply` is everything we still expect to sell -- shed plus hands plus standing yield.
    Both `market.inventory` and `town.unlocked_shops` are `shared: True` in the observation spec, so
    every input here is free.
    """
    if _KG is None:                                                         # pragma: no cover
        return 0
    contest = RESERVATION_CONTEST if contest is None else contest
    slip = RESERVATION_SLIP if slip is None else slip
    supply = int(supply)
    inventory = int(inventory)
    if supply <= 0:
        return 0
    d_rem = town_drain_remaining(prod, step, unlocked_shops, end_step)
    # **Hold only what the town can still take.** Waiting is worth something only if the book can
    # come back, and it comes back at `d_rem`. Replaying this rule over 24 real ladder losses with
    # the guard absent: WOOL +$341,759, STRAWBERRY +$162,355, MILK +$153,871 -- and MELON **minus
    # $73,143**. Melon's book crashes 158 units above `I0` and the town removes 30 across a whole
    # season, so the price it holds out for never arrives, the stock strands mid-season and the
    # sales it refuses were the profitable ones. `d_rem >= supply` is the condition that separates
    # the two: wool at day 16 has 182 of drain left against ~140 held, melon has 14 against ~60.
    if HOLD_A_FLOORED_BOOK and d_rem >= supply:
        # **Supply above the town's remaining absorption is worth the floor AND costs the rest.**
        #
        # The rule below used to widen the offer when `supply` exceeded `d_rem`, on the argument
        # that stock which cannot clear at today's price should go now rather than later. That is
        # true about the stock and false about the money. Episode 91122388, WOOL: the book reaches
        # `d = 59` above `I0` on day 16 -- exactly where `200 - 0.058*d^2` hits the floor -- and we
        # sell another 140 units into it at $1-$5 for the rest of the season, because the town
        # drains a few and we refill them immediately. The book never recovers because we are
        # holding it there.
        #
        #     day  units   book d   price got  |  book d @0.7x   price @0.7x
        #      16     14       58           5  |           51            49
        #      19      9       58           5  |           39           112
        #      22      4       58           5  |           27           158
        #      27      8       59           1  |            6           198
        #
        # Selling 30% less lets the drain outrun our supply, the book falls all season, and the same
        # goods realise $149/unit against $24. The 59 withheld units were worth $1 each -- $59 --
        # and withholding them is what raises the other 160 from $1 to $150.
        #
        # So the reservation price is set by where the book goes if we DON'T sell: only
        # `min(supply, d_rem)` can ever be absorbed, and the town removes `d_rem` regardless, so the
        # book we should price against is `inventory + min(supply, d_rem) - d_rem`, never worse than
        # balanced. `slip` keeps its meaning -- how far below that we will still trade -- and now
        # measures from a price the market can actually return to instead of from a crashed one.
        #
        # Across 14 real ladder losses this is worth +$135,250 on wool, +$57,433 on strawberry and
        # +$57,163 on milk, and flips 12 of the 14. See
        # `docs/we_oversell_into_a_contested_book_2026-08-09.md` and `scripts/less_or_slower.py`.
        # `inventory - d_rem`, NOT `inventory + min(supply, d_rem) - d_rem`. The first version wrote
        # the latter, which collapses to `inventory` for exactly the case that matters -- whenever
        # `supply > d_rem` the `min` is `d_rem`, the terms cancel, and the reservation is read off
        # the crashed price again. It fixed MILK and STRAWBERRY and left WOOL and MELON untouched.
        i0 = _KG.MARKET_PARAMS[prod]["I0"]
        target = max(i0, inventory - d_rem)
        floor_price = (1.0 - slip) * market_price(prod, target)
    else:
        target = max(inventory, inventory + supply - int(contest * d_rem))
        floor_price = max(market_price(prod, target),
                          (1.0 - slip) * market_price(prod, inventory))
    n = 0
    while n < supply and market_price(prod, inventory + n) >= floor_price:
        n += 1
    return n



#: `SEED_BEFORE_LIVESTOCK` was DELETED 2026-08-19: it had no reader. Seed is reserved ahead of any
#: BUY_ANIMAL unconditionally -- see the block above the hire loop for the day-6 measurement.
#: The products the sell block actually offers, in its long-standing order. Named so the
#: make-room release below can rank the same set by holding size without duplicating the tuple.
#:
#: **This is the iteration domain of the ONLY loop that emits a SELL**, and for most of this
#: project's life it held six of the env's nine names. CARROT, TOMATO and EGG were absent, so a
#: schedule row saying `sells {CARROT: 55}` was read by nothing at all -- not deprioritised, not
#: outbid, simply never looked at. The same tuple governs the shed-eviction ranking and
#: `LIQUIDATE_LAST_DAY`, so there was no day and no flag that could reach them.
#:
#: Traced end to end on seed 11 (`tests/test_a_product_the_schedule_asks_to_sell_can_be_sold.py`):
#: 55 carrot seeds bought, 38 planted, harvested on schedule, **92 units standing in the shed on
#: d29**, zero SELL orders emitted, $0 banked. All four carrot arms in
#: `docs/carrot_swap_2026-08-12.md` were therefore comparing 55 tiles of wheat against 55 tiles of
#: nothing, and "carrot loses $5,727" measured the missing wheat. EGG was unreachable on exactly the
#: same line, which puts the goose verdict in the same position.
#:
#: The three are appended rather than merged into the order: the existing six keep their precedence
#: for the ten order slots, so a board that grows none of the new three is byte-identical.
#:
#: Derived from `R.PRODUCTS` so a product added to the env cannot go missing here again.
SELLABLE = ("MELON", "WOOL", "MILK", "STRAWBERRY", "FERTILIZER", "WHEAT") + tuple(
    p for p in R.PRODUCTS if p not in ("MELON", "WOOL", "MILK", "STRAWBERRY", "FERTILIZER", "WHEAT"))

#: How many days ahead the FERTILIZER sell reserve looks. 0 restores the old one-day rule.
#: Three, because `FERTILIZE` sets `fertilized_until_day = day + 2` (`kaggriculture.py:468`) and so
#: covers a three-day window; the stock has to survive from the day it is collected to the day the
#: field asks for it. See the note at the reserve itself.
FERTILIZER_RESERVE_LOOKAHEAD_DAYS = 1



#: **Turn late WHEAT plantings into CARROT / TOMATO.** Sweepable integers: how many wheat plant
#: stops, from `LATE_CROP_FROM_DAY` onward, are re-crewed to each.
#:
#: The 2026-08-15 balance change (PR #1399) put both on a `hinge` scarcity curve, and CARROT's
#: `below_target` went 0.20 -> 1.00 on top of that. Measured on two ladder replays of our own agent:
#:
#:     end-of-season scarcity     x      T   x/T   old $   new $
#:     CARROT                   456    450  1.01      42      71     +69%
#:     TOMATO                   228    200  1.14      87      91      +5%
#:     TOMATO (other replay)    387    200  1.94     108     274    +154%
#:
#: Carrot's gain is the target change and applies at ANY depth; tomato's is the hinge and needs
#: x ~ 2T, which it reached in one of two games. So carrot is the steady one and tomato is a lottery
#: on how hard the shops drain it -- expect tomato to need far more seeds to separate from noise.
#:
#: **Wheat is the right thing to spend.** FEED takes one WHEAT from the acting hand, so wheat looks
#: load-bearing; it is not. Measured on the same two replays, we buy far more wheat as PRODUCT than
#: we ever eat -- 422 bought against 329 fed, and 420 against 316 -- so the herd is fed entirely out
#: of purchases and every wheat TILE is grown purely to sell. Reallocating them costs no feed at all.
#:
#: Both default to 0, which is a no-op, so this is inert until a sweep sets it.
WHEAT_TILES_TO_CARROT = 0
#: **ONE tile, unconditional, and it ships only with routes solved for it.**
#:
#: Measured 2026-08-19 on the four tape arms against routes solved for a NO-tomato mix, one tile from
#: `LATE_CROP_FROM_DAY = 12`: melon_q3 +$5,692, straw_q3 -$1,117, q4_straw -$1,031, q4_melon -$11,655.
#: Those losses do NOT establish that tomato loses, because the routes were solved for a mix without it
#: -- the same confound that made the first strawberry cap read as -$28,259.
#:
#: **Unconditional, because the shop condition was tried and refuted.** A gate firing only where a
#: tomato-draining shop was visible was built and measured; on the seeds actually played the draws are
#: 4 / 2 / 1 tomato-draining shops and the results are -$1,117 / +$5,692 / -$11,655, so there is no
#: monotone condition to gate on. The earlier table claiming 1/0/0/0 was read out of the tape JSONs,
#: which describe a different draw than a forced `cfg["seed"]` produces.
#:
#: **One, not two.** On melon_q3 the second tile cost $8,870 with every other crop count identical --
#: WHEAT 133, MELON 20, STRAWBERRY 34, CARROT 8 at both. Tomato is `interval 1`, so each tile demands a
#: harvest visit on every one of its four yield days; one fits the day's slack and the second one's
#: visits displace better work. Not saturation: tomato takes 135 units above `I0` before halving and a
#: tile yields 4. This is the cows lesson -- per-tile revenue that ignores action cost is not
#: decision-ready -- and it is exactly the cost a re-solve is able to route around, which is why the
#: tile goes in before the solver runs rather than after.
#:
#: **2026-08-19: the "unconditional" claim above is now wrong, and so was the refutation.** A shop
#: gate WAS tried and rejected here -- "on the seeds actually played the draws are 4 / 2 / 1
#: tomato-draining shops and the results are -$1,117 / +$5,692 / -$11,655, so there is no monotone
#: condition to gate on". That asked whether a gate raises MONEY on four tape arms whose route
#: tables were solved without tomato. It is a different question from whether the tile fires on the
#: boards the player we follow would plant on, and the second one has a clean answer: zero tomato
#: across all 34 of his games with fewer than two draining shops. See `TOMATO_DRAIN_SHOPS_NEEDED`.
#:
#: The word "unconditional" was also never true of the code. Two conditions already applied at the
#: use site -- `melon_armed and not q4_armed` -- and reading this docstring instead of that branch
#: is what produced a test asserting on a name the branch does not read.
WHEAT_TILES_TO_TOMATO = 1

#: The shop types that drain TOMATO (`reference/kaggriculture.py:105,111`).
TOMATO_DRAINING_SHOPS = ("PIZZA_SHOP", "FARMERS_MARKET")
#: **Two, because that is where his first tomato appears.** Zero tomato across all 34 of his games
#: with 0 or 1 draining shop; present from 2 and on two of the three boards with five.
#: `data/logs/tets_crop_fit_2026-08-19.log`.
TOMATO_DRAIN_SHOPS_NEEDED = 2

#: **Every crop against every other, as `(src, dst, tiles)` triples.** The two integers above can
#: only ever spend wheat; this can also take melon away, or buy wheat with strawberry.
#:
#: Why the general form is needed, measured on ladder game `93346440` -- a game we WON by $70,525:
#:
#:     product        base   inv close   price close
#:     MELON           250       10157        $  4     1.6% of base, book UP 157 units
#:     WHEAT            25        9419        $ 49     ~2x base, deepest drain on the board
#:     STRAWBERRY      120        9916        $197     above base
#:     TOMATO           60        9916        $ 70     above base
#:     CARROT           35       10032        $ 28     we supplied it, nobody drained it
#:
#: and on a second board (GUI, 2026-08-15): EGG $141 of $50, CARROT $80 of $35, WHEAT $48 of $25,
#: MELON $1 of $250, MILK $1 of $160, WOOL $11 of $200.
#:
#: Neither melon's collapse nor wheat's premium is reachable with a wheat-only knob, and
#: `SHOP_ADAPT_CROPS`'s own docstring names that exact axis -- "wheat against strawberry+melon" --
#: as the one worth building.
#:
#: Applied from `LATE_CROP_FROM_DAY`, in the order given, each budget season-wide and draining as it
#: is spent. Inert at `()`, so this ships as a no-op until a sweep sets it.
CROP_TILE_SHIFTS = ()

#: Late only. The early rows are the opening this repo matches op-for-op, and both crops are scarcity
#: plays whose price is highest once the shops have had a season to drain the book.
LATE_CROP_FROM_DAY = 12


def _recrew(row, src, dst, budget):
    """Re-crew up to `budget` of this row's `src` plant stops to `dst`. Returns (row, spent).

    `plants` is an ORDERED LIST of crop names, one per stop, and the order is the planting order the
    tour is built from -- so a stop is renamed in place and nothing moves. `seeds` is a `{crop: qty}`
    dict and is moved by the same count, which is what keeps the day's bill honest: the crops do
    not cost the same (`RT.SEED_COST` WHEAT 10, CARROT 20, TOMATO 50, MELON 80, STRAWBERRY 100) and
    `_days_bill` prices the row, so swapping the plants without the seeds would under-bill the day
    and mis-set `short_of_cash`.

    **Any crop to any crop, which `_wheat_to` could not express.** That mattered: it could ask for
    more tomato but never for less melon, and melon is the worst-realising crop we grow. Ladder game
    `93346440`, a $70,525 WIN, closed melon at $4 against a base of $250 while wheat closed at $49
    against a base of $25. A knob that only spends wheat cannot reach either.
    """
    if budget <= 0 or src == dst:
        return row, 0
    plants = list(row.get("plants") or [])
    idx = [i for i, c in enumerate(plants) if c == src][:budget]
    if not idx:
        return row, 0
    n = len(idx)
    for i in idx:
        plants[i] = dst
    seeds = dict(row.get("seeds") or {})
    take = min(n, int(seeds.get(src, 0) or 0))
    if take > 0:
        seeds[src] = int(seeds[src]) - take
        if seeds[src] <= 0:
            seeds.pop(src)
    # The stop is being planted either way, so the seed must be bought even if this row's source
    # order was smaller than its plant count (`SEED_ROW_IS_A_FLOOR` tops the rest up in play).
    seeds[dst] = int(seeds.get(dst, 0) or 0) + n
    out = dict(row)
    out["plants"] = plants
    out["seeds"] = seeds
    return out, n


def _wheat_to(row, crop, budget):
    """Back-compat shim: `_recrew` with WHEAT as the source. Kept so the two integer knobs below,
    and the tests that pin them, keep working unchanged."""
    return _recrew(row, "WHEAT", crop, budget)


#: Which days are played from the tape instead of planned. A DAY SET, not a prefix count: d0-d5 are
#: ours. That is not a limitation to work around, it is what makes the handover legal -- our own
#: d0-d5 already tracks the tape to within a few dollars (`money` closes 13/16, 168/171, 44/42, 3/1,
#: 113/111, 43/43), so the board the tape's d6 actions assume is the board we hand it. The further
#: back a replay starts the less true that is.
#: `resolve_days.py` and `breakdown.py` both read this, so the routes are solved for the trajectory
#: we actually play.
#: **DISARMED 2026-08-20. Following tetsuya's schedule while replaying カワシギ's recorded actions
#: for eight days is incoherent, and it was silently overriding the rule this week was spent on.**
#:
#: Every tape in `REPLAY_OPENING_TAPE` below is a カワシギ game. With the agent pointed at tetsuya --
#: his crop mix, his herd gradient, his opening, his goose timing -- days 4-11 were still playing a
#: different player's turns, on a board his plan does not describe.
#:
#: The size of it: 620 of tetsuya's 1187 recorded placements fall in d4-d11, **52%**. That includes
#: d9, d10 and d11, the exact days `MILK_CLASSIFIER_FROM_DAY` lifted from 60-67% to 73-83%. Measured
#: as a function, `_herd_split` matches him on 88.5% of placements; with this armed, half of those
#: decisions never reached the board. A rule that cannot execute is not a rule.
#:
#: This costs the d4-d11 tape opening that the current route tables were solved against, so money on
#: the existing arms is unmeasured until they are re-solved. Alex's call, made explicitly.
#:
#: And there is no tetsuya tape to swap in: his opening is a PLAN we follow, not a
#: recording we play back.
#:
#: **RE-ARMED 2026-08-21. The reason for disarming was tetsuya, and we are not on tetsuya.**
#: Every line above is about following tetsuya's schedule while replaying カワシギ's turns. The work
#: this week is カワシギ's own line -- his melon/strawberry split at d3, his herd, his tape -- so the
#: incoherence that justified `()` does not exist. If the agent is ever pointed back at tetsuya, this
#: goes back to `()` and the paragraphs above are the reason.
#:
#: Alex, 2026-08-21: "there is nothing in the logic to change or decide we are using the tapes",
#: "there are NO problems till d12".
#:
#: He is right, and the measurements agree. d0-d12 has nothing to decide: the start state is
#: identical in every recorded game (same board, NW only, $3000, no shops), and d0-d8, d10 and d11
#: are ONE crop set per day across all 226 of his seasons on the strawberry line. Feeding those days
#: to the planner instead put our ranking rules in charge of a day that has no choices in it, and
#: cost cells on every one of them -- d1's fertilizer cadence, d3's early wheat harvest, d0's market
#: order priority. None of those are decisions the day contains. `_replay_opening` sends his own
#: actions and none of them arise.
#:
#: d4 is IN the window deliberately: `router.py:1208` records that without it we harvest the (0,0)
#: wheat at d4 h11 and re-sow it, so his d5 h14 strawberry lands on an occupied tile and does
#: nothing, losing the square for the season.
#: **24 -> 30 on 2026-08-21. The planner was holding d24-d29 and losing $7,713 doing it.**
#: The boundary was left at 24 on Alex's instruction, given before this was measured. Same seed,
#: same tape, only the handover day moving -- money is a LEVEL, our bank minus his at day end:
#:
#:                       d21  d22  d23   d24    d25   d26    d27   d28    d29
#:     replay d0-d23     +40  +80  +80  -1160  -4117  -543  -3872  -280  -7713
#:     replay d0-d27     +40  +80  +80  +120   +160   +160  +240    +29  -1615
#:     replay d0-d29     +40  +80  +80  +120   +160   +160  +240   +240   +240
#:
#:     handover   season money vs tape   cells d24-d29
#:       d24            -$7,713          13 14 15 16 14 8
#:       d28            -$1,615           2  2  1  2 12 10
#:       none            +$240            2  2  1  2  1  1
#:
#: The planner turns 2 differing cells a day into 13-16 the moment it takes over, wherever that is.
#: That includes d28 and d29, which were separately optimised -- his tape beats them by $1,855 here.
#:
#: The +$240 is not a different plan. It is his ops exactly, minus the seed he buys and never sows;
#: see the `BUY_SEED` trim, which is kept on this arm for precisely that reason.
REPLAY_OPENING_DAYS = tuple(range(30))

#: `{(melon_armed, q4_armed): {step: [farmer, hands, market]}}`, filled by
#: `scripts/build_planner_submission.py`. Empty in the repo, where the tapes are read off disk.
#: This is what makes the replay actually happen inside a submission, which carries no `data/`.
EMBEDDED_OPENINGS = {}

#: The tape the opening comes from, keyed on which branch armed. Must be the tape the plan rows in
#: force were read off, or the handover lands on a board those rows do not describe -- and by d6 the
#: melon branch (d3) and the quadrant branch (d6) have both latched, so which tape is correct is
#: already determined when the first replayed turn arrives.
#: Keyed `(melon_armed, q4_armed)`. **Both latches, not just q4.** `melon_branch` decides on d3 and
#: replaces rows from d3; `q4_branch` decides on d6 and replaces rows from d9. Only the q4 ROUTE
#: table starts at d12 -- its plan rows are live inside any d5-d11 replay window, so a single tape
#: keyed on one latch replays the wrong season's actions on the other arm.
REPLAY_OPENING_TAPE = {
    (False, False): ("data/seed_scripts/kawashigi/92498144.json", "カワシギ"),
    (True, False): ("data/seed_scripts/kawashigi/92466371.json", "カワシギ"),
    (False, True): ("data/seed_scripts/downloads_2026-08-13/91907974.json", "カワシギ"),
    # **The three-quadrant strawberry tape, and this is exact rather than a compromise.** The note
    # here used to say no four-quadrant strawberry game had been identified, and that was simply
    # false -- six kawashigi seats qualify, separated from the melon ones by MELON 84 against
    # MELON 164 over the season:
    #
    #     owned  straw%  money    game
    #       100   55.2%  136,045  field_2026-08-17/93459936
    #       100   52.5%  135,162  kawashigi/92508348
    #       100   56.6%  132,069  field_2026-08-17/93506985
    #       100   56.2%  128,408  downloads_2026-08-13/91906088
    #       100   56.0%   80,864  kawashigi/92488785
    #       100   55.6%   68,372  kawashigi/93545421
    #
    # It does not matter, because over `REPLAY_OPENING_DAYS` -- d4 to d11 -- the q3 strawberry tape
    # and all three of the good q4 strawberry tapes are INDISTINGUISHABLE. Measured 2026-08-18,
    # tiles owned and strawberry standing at dawn:
    #
    #                      d4  d5  d6  d7  d8  d9  d10 d11 | d12 d13
    #     93459936  q4     25  25  25  50  50  50  50  50  |  75 100      land
    #     92466371  q3     25  25  25  50  50  50  50  50  |  75  75
    #     93459936  q4      0   0   4   6   8  19  19  19  |  38  38      strawberry
    #     92466371  q3      0   0   4   6   8  19  19  19  |  37  39
    #
    # They part company at d12, which is PAST the handover -- and our own planner then buys the
    # third parcel on d12 and the fourth on d13, which is the q4 tapes' own timing. So switching
    # this key to a q4 tape is a byte-identical change to the replay, and the four-quadrant board is
    # the solver's job (`solved_days_straw_q4.py`), not the tape's.
    #
    # The melon q4 tape is the one that would be wrong here: `0 0 4 4 10 11 11 11` strawberry
    # against `0 0 4 6 8 19 19 19`, because it sows melon on the squares this arm wants strawberry
    # on. Land, pens and animals are identical in every tape through d12, so crop is the only axis
    # this choice has.
    (True, True): ("data/seed_scripts/kawashigi/92466371.json", "カワシギ"),
}

#: The two species the herd split may exchange, derived rather than written down so it cannot go stale
#: if a third animal is ever added. Both are PASTURE, which is the whole reason a swap is safe inside a
#: replay: the pen, the walk and the route stop are identical and only the species token differs.
_PASTURE = tuple(a for a in R.ANIMAL_NAMES if R.ANIMALS[a]["structure"] == "PASTURE")


def _replay_opening(days, tape=None, team=None):
    """`{step: (farmer, hands, market)}` for every turn of every day in `days`, from the tape's seat.

    Keyed on absolute step, so the days need not be contiguous and need not start at 0.

    **Returns `[]` when the tape is not on disk, deliberately.** The submission bundle carries no
    `data/` tree; it embeds its own `_OPENING` list in the epilogue. A missing file here must
    degrade to a planned opening, never raise -- an exception on the first observation is a
    submission that banks the $3,000 start and nothing else.
    """
    if tape is None:
        tape, team = REPLAY_OPENING_TAPE[(False, False)]
    path = pathlib.Path(tape)
    if not days or not path.exists():
        return {}
    wanted = set(days)
    d = json.loads(path.read_text())
    seat = d["info"]["TeamNames"].index(team)
    out = {}
    # `steps[0]` is the reset state and carries no action, so step N's action is `steps[N + 1]`.
    for step, frame in enumerate(d["steps"][1:]):
        if step // 24 not in wanted:
            continue
        a = (frame[seat] or {}).get("action") or {}
        out[step] = (a.get("farmer") or ["PASS"],
                     list(a.get("hands") or []),
                     list(a.get("market") or []))
    return out


def make_agent(schedule, me=0, router=True):
    """`agent(obs, config) -> action`.

    `router=True` solves the day as a Team Orienteering Problem (`kagg/search/router.py`): tiles are
    pinned, tours are committed, and each stop's ops are re-derived from the live board. `router=False`
    is the earlier per-turn greedy, kept only so the two can be measured on one seed list.
    """
    # **The species is ours; the count and the cadence are the schedule's.** See `HERD_GEESE`.
    sched = swap_in_geese(schedule) if HERD_GEESE else {int(k): v for k, v in schedule.items()}
    state = dict(assigned={}, hired=0, day=-1, tour={}, bought=collections.Counter(),
                 pins={}, routes={}, crew=-1, seen_urgent=set(),
                 planted=collections.Counter(), pen_for={},
                 ordered=collections.Counter(), shed_max=collections.Counter(),
                 uncovered=collections.deque(maxlen=SELL_CARRY_DAYS))

    def agent(obs, config=None):
        day = int(obs.get("day", 0) or 0)
        hour = int(obs.get("hour", 0) or 0)
        # **The four-quadrant branch.** Decides once on d6, and only when the yarn store is already
        # unlocked -- the read three top players make. On an armed draw it rewrites rows 9-29 of
        # `sched` IN PLACE with the leader's four-quadrant tape and installs the 100-tile routes.
        # **DISARMED 2026-08-20, same reason as `REPLAY_OPENING_DAYS`: it is カワシギ's plan
        # overwriting tetsuya's.** `Branch.install` does `target.clear(); target.update(row)` -- it
        # WIPES every row from `split_day` on and replaces it with the branch's own, which is read
        # off カワシギ games.
        #
        # Measured on tetsuya's own board and seed, holding a reference to the live schedule object
        # rather than re-reading the file:
        #
        #     crop rows BEFORE the season   WHEAT 164  STRAWBERRY 32  MELON 8  CARROT 8
        #     crop rows AFTER  the season   WHEAT 127  STRAWBERRY 45  MELON 0  CARROT 5
        #
        # His melon is deleted outright. The season we play is not the season the plan names, and
        # the docstring above already recorded that these measurements do NOT show a gain.
        #
        # It is also what made two measurements on 2026-08-19 return phantom nulls:
        # q4-vs-q3 read +$0 on twelve seeds because BOTH arms armed it and got identical
        # rows. tetsuya never buys the fourth quadrant at all.
        #
        # **RE-ARMED 2026-08-21, with `REPLAY_OPENING_DAYS` and for the same reason: the disarm was
        # about tetsuya, and we are on カワシギ's own line.** Every paragraph above describes
        # カワシギ's rows overwriting tetsuya's; there is no tetsuya plan here to overwrite. If the
        # agent is ever pointed back at tetsuya this call goes, and the paragraphs above are why.
        #
        # Leaving it out was not neutral. `_replay_opening` keys the tape on
        # `(melon_armed, q4_armed)` read off `state` EVERY turn, and nothing writes either key
        # unless these two `arm` calls run -- so the key was `(False, False)` on every turn of every
        # seed and all four entries of `REPLAY_OPENING_TAPE` resolved to the melon tape. Three of
        # the four tapes were unreachable by construction. Measured 2026-08-21,
        # `scripts/seed_tape_grid.py`, five seeds each, weeds 0.0:
        #
        #     --tape kawashigi        d0-d20 exact, 0 cells       the melon tape, the one played
        #     --tape kawashigi_b3     first bad day d3, 148 cells the day melon and berry part
        #     --tape kawashigi_q4c    first bad day d5, 216 cells the day q3 and q4 part
        #
        # Both bad days land exactly where the tapes first disagree. That is what a wrong-tape
        # replay looks like: the ops are sent faithfully, into a board the plan does not describe.
        # Pinned by `tests/test_the_latches_choose_which_tape_gets_replayed.py`.
        _Q4.arm(sched, state, obs, day)
        farms = obs.get("farms") or []
        if len(farms) <= me:
            return {"farmer": ["PASS"], "hands": [], "market": []}
        farm = farms[me]
        priv = obs.get("private") or {}
        shed = collections.Counter(priv.get("shed") or {})
        seeds = collections.Counter(priv.get("seeds") or {})
        invs = priv.get("inventories") or [{}]
        tiles = farm["tiles"]
        # **Today's arrivals are fed to the schedule's own count.** Recomputed every turn rather
        # than latched at dawn, because a pen placed today does not exist at dawn -- PLACE happens
        # mid-day -- so there is nothing to latch. `_arrived` counts the pens that arrived today and
        # `_arrived_fed` how many of those are already fed, both straight off the live board, so the
        # remaining allowance is self-correcting and needs no entry in `state`.
        _row_feeds = int((sched.get(day, {}) or {}).get("feeds", 0) or 0)
        if _row_feeds > 0:
            _arrived = _arrived_fed = _standing = 0
            #: The earliest first production among today's arrivals that are STILL UNFED, which is
            #: what `will_be_fed` spends the allowance on. Read off the same sweep so the two
            #: numbers can never describe different boards. Unfed only: once the sheep have taken
            #: their feeds the cows become the earliest still waiting and the rest of the allowance
            #: reaches them in the same day.
            #:
            #: **The row counts too, not just the board.** d0 places `SHEEP COW SHEEP COW` and our
            #: route lays the cows first, at h6 and h11, with the sheep not reaching the ground
            #: until h16 and h19. A board-only read sees one COW at h7, calls it the earliest
            #: arrival there is, and hands it the allowance eight hours before the sheep that
            #: needed it exist. So the pens the row has still to fill today count as arrivals: they
            #: are as certain as the ones already standing, the schedule named both.
            _soonest = None
            for _a in _outstanding_places(sched, day, tiles):
                _y = R.ANIMALS[_a]["first_yield_day"]
                _soonest = _y if _soonest is None else min(_soonest, _y)
            for _r in tiles:
                for _c in _r:
                    if not (isinstance(_c, dict) and _c.get("animal")):
                        continue
                    if int(_c.get("placed_day", -1)) == day:
                        _arrived += 1
                        if _c.get("fed_today"):
                            _arrived_fed += 1
                        else:
                            _y = R.ANIMALS[_c["animal"]]["first_yield_day"]
                            _soonest = _y if _soonest is None else min(_soonest, _y)
                    else:
                        _standing += 1
            RT.ARRIVAL_FEED_REMAINING = max(0, _row_feeds - _standing - _arrived_fed)
            RT.ARRIVAL_FEED_EARLIEST_YIELD = _soonest
            # Arrivals still wanting a ration: placed today and unfed, plus the row's placements not
            # yet on the ground. Same two populations `_soonest` is taken over, so the count and the
            # priority can never describe different boards.
            RT.ARRIVAL_FEED_OWED = ((_arrived - _arrived_fed)
                                    + len(_outstanding_places(sched, day, tiles)))
        else:
            RT.ARRIVAL_FEED_REMAINING = 0
            RT.ARRIVAL_FEED_EARLIEST_YIELD = None
            RT.ARRIVAL_FEED_OWED = 0
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
                         routes={}, crew=-1, seen_urgent=set(),
                         dawn_row_sent=False)   # `pins`, `planted` and `pen_for` survive by design
            # `planted` is cumulative for the season, so a day's own progress is the difference from
            # this mark. Only the non-router seed path needs it: under `router` the demand is read off
            # the live PLANT pins, which pop as they are planted and so reconcile themselves.
            state["planted_dawn"] = collections.Counter(state["planted"])
            # The seed already in hand when the day opened. With `planted` above it gives the day's
            # own purchases exactly -- `bought = seeds_now + planted_today - seeds_dawn` -- which is
            # what the `seeds` row must be netted against. See `SEED_ROW_IS_A_FLOOR`.
            state["seeds_dawn"] = collections.Counter(seeds)

            # **The leader's melon branch, as the season he actually recorded for that board.**
            # See `kagg/search/melon_branch.py`. Decided once at d3 off the opponent's melon tiles
            # and installed from d3, which is the first day the two three-quadrant tapes disagree.
            #
            # **DISARMED 2026-08-20 with `_Q4.arm` above, and RE-ARMED 2026-08-21 with it.** The
            # disarm reason was that this branch is read off カワシギ games and installs through
            # `Branch.install`, which clears every row from its split day on -- カワシギ's rows
            # overwriting tetsuya's, with nothing to switch TO because we followed one tetsuya plan.
            # We are on カワシギ's own line now, so that reason does not apply. It comes back out
            # if the agent is ever pointed at tetsuya again.
            if _MB.arm(sched, state, obs, day):
                row = sched.get(day) or row

            # **Spend late wheat tiles on the two crops the balance change repriced.**
            # See `WHEAT_TILES_TO_CARROT`. Budgets are season-wide and drain as they are spent, so a
            # sweep value means "this many tiles over the whole season", not per day. Inert at 0.
            if day >= LATE_CROP_FROM_DAY and (WHEAT_TILES_TO_CARROT or WHEAT_TILES_TO_TOMATO):
                if "late_crop_left" not in state:
                    # **The tomato tile belongs to the STRAWBERRY season only.** `melon_armed` is set
                    # by `MelonBranch` at d3 -- and note the name is inverted from what it reads like:
                    # the class is "his strawberry season, taken when the opponent has committed to
                    # melon", so armed means we are playing STRAWBERRY, on `solved_days_straw`.
                    #
                    # This is per-arm PLAN CONTENT, not a flag. The two arms already run different
                    # schedules and different route tables for exactly this reason, and the tile is
                    # part of one season's plan, so it belongs where the rest of that divergence lives.
                    #
                    # Measured 2026-08-19, each arm on routes solved for its own mix:
                    #
                    #     straw arm   155,601 -> 159,623   +4,022   with the tile
                    #     melon arm   139,453 -> 136,516   -2,937   with the tile
                    #                         -> 140,396     +943   without it
                    #
                    # **It is NOT a shop condition, and the draw says so.** Read live at d12 with the
                    # agent playing, the straw board has ZERO tomato-draining shops and gains, the melon
                    # board has one and loses. That is backwards for a demand story, so the tile is not
                    # being paid for by tomato demand and no drain-count gate can express this.
                    # **Not on a four-quadrant board either, and for the same reason the strawberry cap
                    # carries that condition: the tile only exists where a route table was solved for
                    # it.** The q4 arms run the pre-2026-08-19 tables, which have no tomato stop, so a
                    # tile there is exactly the mismatch this day was spent removing -- measured at
                    # -$1,031 on q4 straw, the same figure the tile scored against those tables in the
                    # morning.
                    #
                    # **`q4_armed`, NOT `len(unlocked)`.** The budget is created once, on the first day
                    # at `LATE_CROP_FROM_DAY`, and d12 is the very turn the fourth quadrant is bought:
                    # the live count still reads 3 at dawn and 4 from d13. So a quadrant test here fired
                    # on the q4 board anyway while the cap -- re-evaluated every day -- correctly stayed
                    # off, which is how one condition can look right and the other wrong on one board.
                    # `Q4Branch` decides at d6 and the key is stable by d12.
                    # **And the town has to want it.** The two conditions above are about which arm
                    # the season is running; neither reads the shop draw, and his tomato is decided
                    # by exactly that. Tomato drains to PIZZA_SHOP and FARMERS_MARKET
                    # (`kaggriculture.py:105,111`), drawn WITH replacement, so the COUNT varies where
                    # presence does not. Measured over his 78 games:
                    #
                    #     tomato-draining shops    0    1    2    3    4    5
                    #     games                   10   24   25    9    7    3
                    #     games with tomato        0    0    1    0    1    2
                    #
                    # Not one tile across all 34 games with fewer than two draining shops, and two of
                    # the three with five. `data/logs/tets_crop_fit_2026-08-19.log`.
                    #
                    # This is a GATE and not a size: the tile count stays exactly as it was, so the
                    # only change is which boards get it. One delta.
                    #
                    # Read off `obs` the same way line 4044 does. NOT off the local `unlocked`,
                    # which is `unlocked_quadrants` -- quadrant names never match shop names, so
                    # that spelling scores 0 on every board and switches the tile permanently off
                    # while looking like a working gate.
                    _tom_drain = sum(1 for s in ((obs.get("town") or {}).get("unlocked_shops") or ())
                                     if s in TOMATO_DRAINING_SHOPS)
                    # `melon_armed` / `q4_armed` are GONE from this condition. Nothing sets them
                    # since the branches were disarmed, so leaving them here pinned `_tom` at 0 and
                    # made `TOMATO_DRAIN_SHOPS_NEEDED` -- added two commits earlier -- unreachable.
                    # The draw is the whole condition now, which is what the corpus supports anyway.
                    _tom = (int(WHEAT_TILES_TO_TOMATO)
                            if _tom_drain >= TOMATO_DRAIN_SHOPS_NEEDED else 0)
                    state["late_crop_left"] = {"CARROT": int(WHEAT_TILES_TO_CARROT),
                                               "TOMATO": _tom}
                # **Only touch a day that HAS a row, for the reason spelled out on `CROP_TILE_SHIFTS`
                # twelve lines down.** `sched.get(day) or {}` followed by an unconditional
                # `sched[day] = _r` inserts an EMPTY row on every day from here that the schedule does
                # not plant on. That changes the season identically for every budget, so it lands inside
                # the measurement of whatever is being swept and reads as the swept effect -- which is
                # exactly how ten different `CROP_TILE_SHIFTS` configs all returned +$4,691. The same
                # defect was live on this block and was found on 2026-08-19 while measuring tomato.
                # Both integers ship at 0, so fixing it changes nothing that runs today.
                if sched.get(day):
                    _r = sched[day]
                    for _crop in ("CARROT", "TOMATO"):      # a total order, so a sweep is reproducible
                        _r, _spent = _wheat_to(_r, _crop, state["late_crop_left"][_crop])
                        state["late_crop_left"][_crop] -= _spent
                    sched[day] = _r
                    row = _r

            # **The general form: any crop onto any other.** See `CROP_TILE_SHIFTS`. Applied after
            # the two wheat integers so a sweep that sets both is still a total order.
            # **Only touch a day that HAS a row, and only write back if something moved.**
            # `sched.get(day) or {}` followed by an unconditional `sched[day] = _r` inserted an
            # EMPTY row on every day the schedule does not plant -- which changed the season
            # identically for every shift, including ones with nothing to re-crew. A fork
            # comparison then returned the same +$4,691 for all ten configs.
            if day >= LATE_CROP_FROM_DAY and CROP_TILE_SHIFTS and sched.get(day):
                if "crop_shift_left" not in state:
                    state["crop_shift_left"] = [int(n) for _, _, n in CROP_TILE_SHIFTS]
                _r, _moved = sched[day], 0
                for _i, (_src, _dst, _) in enumerate(CROP_TILE_SHIFTS):
                    _r, _spent = _recrew(_r, _src, _dst, state["crop_shift_left"][_i])
                    state["crop_shift_left"][_i] -= _spent
                    _moved += _spent
                if _moved:
                    sched[day] = _r
                    row = _r

        units = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]

        # The unit phase decrements `shed` for every PICKUP it issues this turn, and `invs` was read
        # before it ran, so the drawn units are in neither by the time the market block costs the
        # herd's reserve. Keep the pre-draw level; the difference is the draw.
        shed_before = collections.Counter(shed)

        if router:
            # The dawn plan has to route the hands this turn's market phase is about to buy, so the
            # arithmetic the market block does at the BOTTOM of this function has to be available at
            # the top. `_hires_this_turn` is that block's rule stated once; if the two ever disagree
            # the plan orphans a route, so they must be read together.
            n_hires = _hires_this_turn(state, sched.get(day, {}) or {}, day, hour, money,
                                       shed=shed,
                                       prices=(obs.get("market") or {}).get("prices") or {})
            # **The farmer is not a bystander to where its own crew lands.** See
            # `_clear_the_spawn_ring`: `_spawn_hand` counts it, so standing on the ring rotates every
            # spawn and puts a second hand on the dead `(5,5)` corner -- 23 turns, on d4 the
            # difference between banking the row and carrying 43 wheat to midnight.
            #
            # The step and the arrivals are computed TOGETHER and used together. They have to be:
            # `_arrivals` is what the dawn plan routes phantoms onto, so an arrivals list that
            # assumed a step the farmer then did not take would orphan a route -- the exact failure
            # `PLAN_THE_CREW_THAT_ARRIVES` exists to avoid.
            step_off, arriving = _clear_the_spawn_ring(units, unlocked, n_hires)
            # **The ground the plan works is the ground the day will have.** See `_land_this_turn`.
            # `_clear_the_spawn_ring` above keeps the REAL set deliberately: it decides where hands
            # physically land this turn, and at hour 0 the parcel is not ours yet.
            #
            # The residual cost is stated rather than hidden: a unit routed into the new quadrant at
            # hour 0 has its MOVE refused (`kaggriculture.py:313`) and loses that one turn, and a
            # shed cell inside the parcel is treated as a depot an hour early. That is at most one
            # turn per unit on one day of the season, against the 128 idle unit-turns d10 spends now.
            _land = _land_this_turn(sched, day, hour, unlocked, money, n_hires,
                                    prices=(obs.get("market") or {}).get("prices") or {})
            plan_unlocked = (unlocked | {_land}) if _land else unlocked
            # **Owning the quadrant is not enough -- the CELLS have to read empty too.** They are the
            # string `"LOCKED"` until `_do_buy_land` rewrites them to `None` (`kaggriculture.py:709-713`),
            # and `build_nodes` offers a plantable tile only where the cell is empty. Flagging the
            # quadrant owned while every cell still says LOCKED left d10's dawn plan with exactly the
            # 29 NW/NE jobs it had before, which is how the first cut of this fix measured as nothing.
            # Copied, never mutated in place: `tiles` is the live observation and the market block
            # below reads it (`tiles[b][a] != "LOCKED"`) to place the day's pens.
            plan_tiles = tiles
            if _land:
                plan_tiles = [list(row) for row in tiles]
                for _y, _row in enumerate(plan_tiles):
                    for _x, _cell in enumerate(_row):
                        if _cell == "LOCKED" and R.quadrant_of(_x, _y) == _land:
                            _row[_x] = None
            # The shop draw decides which crop goes in the ground (`SHOP_ADAPT_CROPS`), so the plan
            # needs it BEFORE the market block below reads it for the sell rule. `shared: True` in
            # the observation spec, so both seats see the same list.
            # **What a fertilizer unit would fetch RIGHT NOW is the cost of putting it in the
            # ground.** Nothing eats fertilizer, so its book only ratchets up: it is at $50 by day
            # 17 and $20 by day 26 in 85 of 85 recorded games. Pricing it at the $100 base means
            # refusing to fertilize a tile because the unit is notionally worth five times what
            # anyone will pay. The quote is in the observation, so it need not be estimated.
            _fert = ((obs.get("market") or {}).get("prices") or {}).get("FERTILIZER")
            acts = _router_acts(state, sched, day, hour, plan_tiles, units, invs, shed,
                                seeds, plan_unlocked, money, arriving=arriving,
                                unlocked_shops=list((obs.get("town") or {}).get("unlocked_shops")
                                                    or []),
                                fertilizer_price=_fert, hold_farmer=step_off is not None)
            if step_off is not None and acts:
                # The plan was cut from where the farmer STANDS, so its first stop is simply reached
                # a turn later. That is the whole price: one farmer turn against a hand's twenty-three.
                acts[0] = [step_off]
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
        # Which BUY_PRODUCT orders came from the DUSK TOP-UP rather than the row. Held by identity
        # rather than index because `NET_THE_TWO_LEGS` runs after several later appends. Only these
        # may cancel a sell -- see the netting block for why the row's own buys must not.
        topup_orders = set()
        # How many mouths there are, needed BEFORE the sell loop so the herd's feed is not sold.
        #
        # **Mouths we will actually FEED, once feeding is not nightly.** `RT.animal_ops` offers a
        # FEED only to a pen that is hungry or already producing (`FEED_ONLY_WHEN_IT_BUYS_SOMETHING`),
        # so counting every pen reserves a ration for animals nobody is going to feed. That is not a
        # rounding error: the reserve is `feed_days(day) * alive` and it is netted against `drawn`,
        # the wheat that really left the shed this turn. Feed half as often and `drawn` halves while
        # the reserve does not, so the guard holds back roughly twice the herd's appetite and the day
        # stops selling -- d2 `sell 4/5 -> 2/5`, d3 money $448 -> $95, season $9,975 -> $5,774.
        alive = sum(1 for r in tiles for c in r
                    if isinstance(c, dict) and "animal" in c
                    and RT.will_be_fed(c, day))
        # **An animal today's row will PLACE is a mouth today, and `alive` cannot see it.** `alive`
        # is a board read, so on the morning of a placement it is short by exactly the animals still
        # sitting in the shop. Day 4 is where that first costs something, because it is the first
        # row that places an animal AND sells wheat: shed 6, pens 6, `places ['COW']`,
        # `sells {'WHEAT': 49}`. The sell row is meant to come out of the fourteen-tile wheat
        # harvest, which reaches a hand at h14 and the shed at h23; at h00 the only wheat on the
        # board is the herd's dinner, and we sold one unit of it and bought the same unit back at
        # h01. Seb buys his seventh wheat at h02 and never sells before h18. Six wheat reached our
        # hands, six of seven pens were fed, and `feed 5/7` on d6 is the same shape a day later.
        #
        # **Today's row only, netted against the board.** The cumulative variant is the one recorded
        # as TRIED AND REVERTED at `feed_days` -- it ran ahead of the board whenever a placement
        # slipped (`place 0/4` on d9/d10) and bought feed for animals that did not exist. Reading
        # one row, minus the animals already standing that were placed today, bounds the error at
        # the day's own placements, and errs toward holding a spare wheat rather than selling a
        # ration: the spread costs pennies, a missed feed costs the animal-day and the care chain.
        #
        # Gated through `RT.will_be_fed` on a synthetic cell rather than a second copy of the
        # cadence, so that from `FEED_CADENCE_FROM_DAY` a pen placed today and not yet producing
        # reserves nothing -- which is what the router will actually do with it.
        placed_today = sum(1 for r in tiles for c in r
                           if isinstance(c, dict) and "animal" in c
                           and int(c.get("placed_day", -1)) == day)
        arriving = sum(1 for a in list((row.get("places") or []))[placed_today:]
                       if RT.will_be_fed({"animal": a, "consecutive_unfed": 0,
                                          "placed_day": day}, day))
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
        last_day = max(sched) if sched else day
        pending = 0          # cash this turn's sells will have banked by the time BUY_LAND settles
        rate = collections.Counter()
        # Everything the rest of the season will EVER ask for, per product. Stock above this can only
        # leave the shed on the last day, so it is what `still_owed` below releases early. Days after
        # today only: today's own row is `today`, and double-counting it would hide real surplus.
        still_owed = collections.Counter()
        horizon = day + len(sched)
        for d in sorted(sched):
            for p, q in (sched[d].get("sells") or {}).items():
                if d <= day:
                    rate[p] = max(rate[p], int(q))
                elif d <= horizon:
                    still_owed[p] += int(q)
        # **Room for tonight's drop.** See `SELL_TO_MAKE_ROOM`. Everything the hands are carrying
        # comes home at the rollover and the part that does not fit is deleted, so the shed's free
        # space is a real constraint that no `sells` row knows anything about.
        #
        # Computed once per turn and spent across products below, because the limit is on the SHED,
        # not on any one product: nine products share one hundred slots.
        #
        # **Released from the LARGEST holding, and NOT gated on `still_owed`.** The first version
        # only released genuine surplus -- stock above everything the remaining rows will ask for --
        # and it fired zero times. At day 24 the shed holds 57 MILK while the last five rows ask for
        # about 80, so "surplus" is negative and the guard blocked the release while 22 units were
        # binned that night. Future rows are fed by future production, not by tonight's stock, and
        # the trade is not close: a missed row is recoverable through `SELL_CARRY_DAYS`, a discarded
        # unit is gone. Largest-first so the pile that is actually causing the crowding is the one
        # that moves, rather than whichever product the loop happens to reach first.
        room_needed = 0
        release = collections.Counter()
        carried_home = sum(int(v) for iv in invs for v in (iv or {}).values() if int(v) > 0)
        room_needed = max(0, int(sum(shed.values())) + carried_home - SHED_CAPACITY)
        # **TRIED and REJECTED: forecast the day's inflow at dawn instead of reacting to it.**
        # Counting the standing `yield_units` on every pen and ripe crop as arriving today, and
        # pacing the release over `TPD - hour` turns, is the better-shaped idea and it does move
        # the right fields -- discards 101 -> 47, `sh:milk` +181 -> +80, differing cells 417 ->
        # 412, and the land parcels stay identical to the tape on every day. It costs **$4,385
        # of final bank** (d29 +1,097 -> -3,288), because selling earlier walks the price down by
        # more than the saved product is worth. On an Elo ladder the bank is the result and the
        # tidier stock curve is not, so it is not being kept.
        #
        # Neither version closes the floor, and no sell rule can: **the market sells from the
        # SHED, and product sitting in a hand at dusk was never sellable that day.** When the
        # crew carries 40 units home to a shed with room for 15, the 25 die whatever the market
        # did. The residue is exactly that shape -- 17 units on d21, 10 on d23. Closing it needs
        # the ROUTER to stop collecting into a shed that cannot take the load, which is the same
        # assignment defect as OPEN-4. See `docs/REGISTER.md`.
        for p in sorted(SELLABLE, key=lambda p: -int(shed.get(p, 0))):
            if room_needed <= 0:
                break
            take = min(int(shed.get(p, 0)), room_needed)
            release[p] = take
            room_needed -= take
        # Everything still to sell, not just what is in store: standing `yield_units` and whatever
        # the crew is carrying are both stock the season has to clear, and understating supply
        # understates the glut, which is the direction that already cost 331 destroyed units.
        #
        # **Named `standing_supply`, not `standing`, on purpose.** This commit already binds
        # `standing` to an INT -- the pasture/coop count -- in the same function, and reusing the
        # name would silently clobber it wherever the two blocks both run.
        standing_supply = collections.Counter()
        for _r in tiles:
            for _c in _r:
                if not isinstance(_c, dict):
                    continue
                _y = int(_c.get("yield_units", 0) or 0)
                if _y <= 0:
                    continue
                if _c.get("kind") == "PLANT":
                    standing_supply[_c.get("crop")] += _y
                elif _c.get("animal"):
                    standing_supply[R.ANIMALS.get(_c.get("animal"), {}).get("product", "")] += _y
        for _iv in invs:
            for _k, _v in (_iv or {}).items():
                standing_supply[_k] += int(_v)
        market_inv = (obs.get("market") or {}).get("inventory") or {}
        unlocked_shops = list((obs.get("town") or {}).get("unlocked_shops") or [])
        # **Does the rest of today still cost more than the bank holds?** See `LATE_SELL_BIAS`.
        # Recomputed every turn, because the answer changes as the day's sales land: a morning that
        # opens short sells until it is funded and then stops, which is exactly the d6 shape on the
        # tape -- `WOOL 6` at h09, `WOOL 6` at h13, `BUY_LAND` at h13, and nothing after.
        #
        # `_days_bill` is the WHOLE row -- animals, seed, feed, hires and land -- not just the land.
        # Land dominates it by an order of magnitude, but a day that cannot afford its cows is just
        # as stuck, and the melon/strawberry rows on d5 and d7 are the cases Alex named alongside it.
        # Deliberately gross rather than net of what has already been bought: `state["ordered"]` does
        # not scope per category, and over-selling by one turn on a funded day is a far cheaper error
        # than under-funding a $1,000 parcel. If that proves too blunt, the fix is a per-category
        # remainder, not a tolerance.
        unfunded = (money + pending) < _days_bill(row)
        for prod in SELLABLE:
            have = int(shed.get(prod, 0))
            # What the EVICTION may reach, which is `have` for everything except wheat. See
            # `FEED_RESERVE_YIELDS_TO_OVERFLOW`.
            releasable = have
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
            #
            # **NOT the cause of d1 selling 2 against a row of 4 -- checked, 2026-08-09.** Flooring
            # the reserve at the row changes the d0-d6 table by nothing at all, because the reserve
            # is not what binds: `have` reads `shed[FERTILIZER]`, and on d1 the shed holds ZERO
            # fertilizer on all 24 turns. We collect 4, exactly as he does, and it sits in a hand.
            # The two sales that do happen are on the turns straight after a DROP. See the router.
            # **The reserve is one day deep and the demand is not.** `crop_ops` offers FERTILIZE only
            # while a tile is near its producing stretch, so the day's want arrives in a lump:
            # offered 0 on d11, 2 on d12, 4 on d14, **12 on d16**. A reserve that asks only about
            # today therefore sells the whole stock into d11's `FERTILIZER: 24` row and leaves d16's
            # twelve tiles nothing. Measured, dawn shed fertilizer ours/tape:
            #
            #     d10 15/15  d11 10/12  d12 4/9  d13 4/12  d14 1/12  d15 4/12  d16 10/12
            #
            # We track him exactly to d10 and never recover, on identical production -- `collect_fert`
            # is 12/12 every one of those days. d16 then routes 12 FERTILIZE stops and fires 6,
            # because `_inv_take` returns silently on an empty hand (`kaggriculture.py:465`) and the
            # walk is spent for nothing. Ask the same question over the window a fertilize actually
            # covers -- `fertilized_until_day = day + 2`, so three days -- instead of only today.
            if prod == "FERTILIZER":
                want = max(
                    sum(1 for r in tiles for c in r
                        if isinstance(c, dict) and c.get("kind") == "PLANT"
                        and "FERTILIZE" in [o for o, _i, _p in RT.crop_ops(c, day + k, True)])
                    for k in range(FERTILIZER_RESERVE_LOOKAHEAD_DAYS + 1))
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
                # **What is still to be BOUGHT, not what the row buys all day.** Once the purchase
                # has actually gone out it is sitting in `shed`, and counting the row's whole-day
                # figure as well counts the same unit twice. Measured on d4: suppressing the h00
                # sale moved it to h01 and changed nothing else -- shed 7, `alive + arriving` 7,
                # and `will_buy` still reading 1, so `reserve = 7 - 0 - 1 = 6` released the same
                # wheat one hour later. `owed` further down already nets the counter this way for
                # the buy side; this is the same subtraction on the sell side.
                #
                # NOT the over-suppression recorded at `DUSK_FEED_TOPUP` ("minus what it already
                # ordered -- 14 lost"). That one netted prior orders out of a GAP that was already
                # measured against the shed those orders had filled. Here the term is a forecast of
                # stock not yet in the shed, so once it arrives the forecast is spent by definition.
                will_buy = max(0, int((row.get("buys") or {}).get("WHEAT", 0))
                               - int(state["ordered"][("buys", "WHEAT")]))
                # **`ripe_wheat` is NOT feed and must not cancel the reserve.** It is wheat standing
                # in the FIELD. Subtracting it treated an unharvested crop as though it were already
                # in a hand, so a full field released the shed's real stock to the market and the
                # herd was sold its own dinner. Traced on day 11, seed 11:
                #
                #     h0   14 animals, 14 UNFED, shed wheat 14   ->  SELL WHEAT 7
                #     h2   shed wheat 0, and it stays 0 for the remaining 22 hours
                #     h0-h23  FEED fires TWICE, because feeding needs wheat in a hand and a hand
                #             draws from a shed we had emptied
                #     d12 dawn  16 animals -> 14, evicted at `consecutive_unfed >= 2`
                #
                # The note that defended it -- "fourteen ripe tiles feed the herd perfectly well" --
                # is true only if those tiles are harvested, carried and dropped BEFORE the animals
                # go hungry. On the days this fires the crew is planting instead, and standing wheat
                # feeds nothing. Across the season it cost us 7 cows against the tape's 13.
                #
                # The other three terms stay: `carried_wheat` is in a hand right now, `drawn` already
                # left the shed this turn, and `will_buy` is a commitment the same turn loop honours.
                # All three are wheat that exists or is being bought; standing crop is neither.
                # **`carried_wheat` comes out of the reserve, because the top-up cannot see it.**
                # Both sides guard the same floor -- `feed_days(day) * alive`, 7 on day 4 -- from
                # different stock. Netting off the 28 wheat in hands leaves a reserve of 0, so the
                # shed is offered bare; `DUSK_FEED_TOPUP` then reads `(alive + arriving) - shed`,
                # sees an empty shed and buys the cap straight back. d4 h19, h22 and h23 each SELL
                # WHEAT and BUY_PRODUCT WHEAT in the SAME turn, paying the spread on both legs, and
                # the day closes `buy_product 21/1` against a tape that buys one wheat.
                #
                # Making the two agree by teaching the top-up about hands was measured and is worse
                # -- see the table at `DUSK_FEED_TOPUP`, 8 animals lost against 2. Wheat in a hand at
                # dusk is already earmarked for a pen, so it is not spare on EITHER side. The reserve
                # is the side that was wrong.
                # `alive + arriving`: the mouths TODAY, not the pens standing at dawn. Without
                # `arriving` the ration bought for the day's new animal is subtracted from the
                # reserve that protects it -- `will_buy` is that purchase -- so d4 h00 read
                # `6 - (1*6 - 0 - 1) = 1` sellable out of a shed that was exactly tight.
                reserve = feed_days(day) * (alive + arriving) - drawn - will_buy
                reserve -= carried_wheat
                # **TODAY'S dinner is never released against a purchase that has not cleared.**
                # See `NEVER_SELL_TODAYS_RATION`. `will_buy` is a forecast, and the terms above can
                # net the reserve to nothing on the strength of it: `seb1326` d6, row `buys WHEAT 7`,
                # gave `7 - 0 - 7 = 0` and the day sold six of the seven wheat in the shed at h00.
                # The buy-back went out at h01 for six and filled THREE. Four wheat reached a hand,
                # four of seven animals ate, and two cows walked off between d7 and d8
                # (`kaggriculture.py:804`).
                #
                # The floor is one wheat per mouth not yet fed, less what the crew already carries --
                # the immediate, un-hedgeable need. It is deliberately NARROWER than `reserve`: the
                # multi-day buffer may still be released by a forecast, because a forecast that fails
                # only costs tomorrow's margin. Today's costs the animal.
                unfed = sum(1 for r in tiles for c in r
                            if isinstance(c, dict) and "animal" in c and not c.get("fed_today"))
                reserve = max(reserve, unfed + arriving - carried_wheat)
                have = max(0, have - max(0, reserve))
                # **The reserve yields slots rather than let the harvest be binned.** The full
                # `feed_days(day)` buffer stands for ordinary rows; only the eviction may dip below
                # it, and only as far as `FEED_DAYS_FLOOR`. `max(have, ...)` so this can never
                # RESTRICT what an ordinary sale could already reach.
                #
                # **The floor takes NO offsets, unlike the reserve above.** Subtracting
                # `carried_wheat`, `drawn` and `will_buy` is right for the reserve, which asks "does
                # this much wheat exist anywhere" -- but the floor asks a narrower question: is
                # there a day of feed standing IN THE SHED at dusk, where FEED can draw on it
                # tomorrow morning. Wheat in a hand may be eaten before the rollover ever returns it.
                # With the offsets the floor collapsed to zero and the eviction emptied the shed on
                # days 21, 22, 25 and 28 with a herd of nineteen.
                # **Gated to the phase it was built for.** Every comment on this flag describes a
                # late-season lever -- "from day 16 the farm is TURN-bound" -- and nothing in the
                # design says day 0 against a four-animal herd. The `if` below carried no day check
                # and changed the dawn WHEAT/money row on 15 of 16 days before `FEED_DAYS_FROM_DAY`,
                # `money@d15` moving 2,252 -> 1,931 on seed 11 alone (`test_the_feed_gate_is_a_late_
                # season_lever.py`). It is early cash-flow divergence, not a discard fix: the herd is
                # 4-9 animals here and the shed is nowhere near its 100-slot cap.
            # **The carry recovers a MISSED row; it is not a licence to dump the shed.** `market_price`
            # falls monotonically in inventory and a SELL walks n units down that curve one at a time,
            # so a bigger offer clears at a worse mean price -- measured as wool 123 units -> 138 for
            # REVENUE $29,041 -> $21,811. `rate` is the largest single day the schedule ever asks for,
            # so two missed rows of 5 are recovered 5 at a time over as many turns as it takes, and the
            # per-offer rate the standing offer relies on is unchanged.
            if CUMULATIVE_SELLS:
                today = int((row.get("sells") or {}).get(prod, 0))
                carry = sum(u[prod] for u in state["uncovered"])
                # **Stock no remaining row will ever name is dead stock, and it must be released.**
                # The row is an ABSOLUTE count read off HIS board, so it only fits our board while
                # the two produce the same amount. Measured on the `seb` tape, seed 11, weeds off,
                # with `scripts/probe_sell.py --prod MILK`: we meet every single milk row exactly, on
                # the day, all season -- 6/6 on day 10, 3/3 on day 11, 6/6 on day 12, 24/24 on day 15
                # -- and still finish day 28 holding 67 milk to his 16, because 44 extra CARE ops
                # produce milk the schedule has no line for. `sh:milk` is the largest state row in
                # the table at +521 and NONE of it is a missed row, so the carry cannot touch it.
                #
                # `LIQUIDATE_LAST_DAY` below already concedes the principle -- "stock has no terminal
                # value" -- and then dumps all 51 surplus units into one day's book. The same argument
                # holds on any day for stock the REMAINING rows will never ask for, and it is worth
                # more there because `rate` still bounds each offer, so it goes out spread over days
                # instead of down one price curve. The release re-reads `have` every turn, so it
                # shrinks as the shed drains and stops of its own accord at `still_owed`.
                #
                # **What it is worth, and what it does NOT fix.** The whole-season horizon only
                # becomes binding on day 25, so d0-d24 are byte-identical to before and the milk
                # divergence at d12-d24 is untouched. From d25 the daily money gap goes
                # -8,886/-8,404/-6,798/-6,575/+6,247 to -8,384/-4,613/-1,330/+2,338/+5,533, i.e.
                # closer to the tape on all five days, and the season sum of that gap improves
                # -107,267 -> -89,307 with one fewer differing cell (d26, 17 -> 16). The day-29 bank
                # is $714 lower in absolute dollars, which is the cost of not dumping into one book.
                #
                # d12-d24 needs a different fix and it is NOT a sell rule: the tape ends day 12
                # holding 9 milk and we end holding 12 having both sold exactly 6, so hitting his
                # number requires knowing his number. `sells` is the only trace of his inventory in
                # the schedule and it does not carry it. See `SELL_SURPLUS_HORIZON` for the two
                # shorter horizons that were tried instead, and how much they cost.
                allow = max(today + carry, have - still_owed[prod])
                # **If the schedule records what HE held at dusk, sell down to it.** This is the only
                # rule that can reach d12-d24, for the reason above: his number is not derivable from
                # `sells`, it has to be recorded. It is a FLOOR on the release and never a cap on the
                # row -- `max`, so a row asking for more than the surplus still fires in full.
                # Refusing to sell is the arm that cost -$16,025 and is not being reintroduced here.
                #
                # **NOTHING SETS THIS FIELD YET AND THAT IS DELIBERATE -- read before wiring it up.**
                # No schedule on disk carries `shed_dusk`, so this branch never fires in the
                # submission and the two caps above are the whole live rule. It is here because it is
                # the only way `scripts/probe_shed_target.py` can measure the arm, and the arm is
                # worth a lot and is not yet safe. Injecting the tape's own dusk shed (read from the
                # replay's `private.shed` at the FOLLOWING dawn, the same instant `breakdown.snap`
                # samples) on `seb`, seed 11, weeds off:
                #
                #                        money sum   d29 money   sh:milk   state cells   d4  d5
                #     without              -89,307      +5,533      +446           168    1   0
                #     sell down to it      -24,582         +62       +46           181    2   2
                #
                # It very nearly erases the milk pile-up and lands the season's final bank within $62
                # of his, from $5,533 -- but it costs d4 and d5, which currently match, and d0-d5 is
                # the one line that does not move. The regression is `sh:wheat`, -2 from day 4 and
                # widening to -4 by day 8: we end those days holding LESS wheat than he does. The
                # obvious explanation was that WHEAT and FERTILIZER net a reserve out of `have` while
                # `shed_dusk` is a whole-shed figure, so the reserve is subtracted twice -- that was
                # tested by targeting the raw shed instead and it is NOT the cause. It got worse on
                # every axis (money -118,360, 194 cells, `sh:wheat` -2 at d4 unchanged, and a land
                # purchase lost at d10 costing 25 tiles). So the cause is still open, and until it is
                # found this stays unfed.
                target = (row.get("shed_dusk") or {}).get(prod)
                if target is not None:
                    allow = max(allow, have - int(target))
                # **PRICE_AWARE_SELL_CAP: relax the DAY TOTAL, never the PER-OFFER size.** `allow`
                # (via `still_owed`/carry) bounds how much of a product is sold across the whole
                # day -- a fact about ONE REPLAY's row, not about the market -- and that is what
                # this drops when the live price says the product is not glutted. `rate[prod]`
                # bounds a SINGLE OFFER and stays in force even when the flag fires: it is what
                # stops one turn's harvest from being walked down the price curve in one dump, the
                # exact failure this file already measured on wool (123 units -> 138, revenue
                # $29,041 -> $21,811, `LIQUIDATE_FROM_HOUR`'s docstring). A first version of this
                # flag set `n = have` outright and was measured on the arena pool, seeds 500-505,
                # `PRICE_AWARE_SELL_CAP` vs off: win rate unchanged (94.4%, pool saturated) but MEAN
                # MONEY fell ~30% against every single opponent ($111,238 -> $77,587,
                # `data/logs/price_aware_arena_2026-08-08.log`) -- exactly the dump signature, since
                # a turn with a big `have` (right after a harvest lands) emitted it as one order and
                # walked the whole thing down in a single turn's lockstep instead of spreading it
                # across turns the way the shipped `rate[prod]` cap always has.
                price_ok = (PRICE_AWARE_SELL_CAP
                            and prices.get(prod, RT.BASE_PRICE.get(prod, 0)) >= RT.BASE_PRICE.get(prod, 0))
                # **The row governs on EVERY path.** `allow` -- the day's `sells` row plus any
                # genuinely missed row carried forward -- and the day-total cap used to live only in
                # the `else` branch below. So whenever `price_ok` held, which is every turn the book
                # sits at or above base and therefore the whole opening, the plan stopped binding and
                # the offer became whatever `rate` or the book's depth permitted.
                #
                # Measured on d0 of Seb's tape, whose `sells` row is EMPTY: we bought 8 WHEAT at $27
                # and sold 7 of them straight back at $27 on hours 2 and 4-9. A wash trade the plan
                # never asked for -- and the $189 it banked is exactly what let our d4 `BUY_LAND`
                # clear, where his was refused for want of cash and did not land until d8. So
                # `tiles 50/25` from d4, and the ~$1,000 money gap behind it, are this branch rather
                # than three separate defects. Losing the day total on the same path is d4 selling
                # 35 against a row of 28.
                #
                # The price and reservation rules stay, but only as what they claim to be: caps.
                # They may shrink an offer the row allows. They may not create one it does not.
                # **The row is a DAY TOTAL, and re-offering it every turn made it a per-turn quota.**
                # `rate` bounds one offer; nothing bounded the day. Seb's day-4 row asks
                # `WHEAT 28, FERTILIZER 4` and he sells exactly that. The carry inside `allow` is what
                # recovers a genuinely missed row; it is not a licence to outrun a met one.
                n = min(have, allow, rate[prod])
                n = min(n, allow - state["ordered"][("sold", prod)])
                # **RESERVATION_SELL_CAP: the per-offer size, read off the live book.**
                # `rate[prod]` above is the largest single day ONE 1.32.2 replay ever asked for.
                # `reservation_units` computes the same quantity from `market.inventory` and
                # `town.unlocked_shops`, both `shared: True` in the observation, so it is a fact
                # about the market rather than about his production.
                #
                # **It replaces `rate[prod]`, in both directions, and that is the point -- but it
                # was replacing `allow` too, and nothing here ever argued for that.** The
                # argument below is about `rate`: the largest single day one 1.32.2 replay
                # asked for, a guess at his production. `allow` is not a guess, it is the plan,
                # and it lived in the other branch purely by accident of layout. A
                # first wiring took `max(n, reservation)` on the argument that a rule which can
                # only widen an offer cannot regress -- and it was a no-op: five seeds of
                # `scripts/handover.py` came back byte-identical, ours $140,455/$138,003/
                # $151,325/$151,075/$149,039 with the flag on and off
                # (`data/logs/reservation_off.log`, `..._on.log`). `rate[prod]` was already the
                # larger number on every turn it mattered, so "only ever raises" bought nothing
                # except a flag that looked live and was not. The whole content of the rule is
                # in the direction that shrinks an offer -- MELON's book absorbs ~140 units a
                # season on 1.32.2 and ~30 on 1.32.6 because no shop carries it at all, and on
                # this fixture we push 96 of the 125 units that crash it to $144.
                #
                # Every reserve netted into `have` above -- the wheat feed floor, the fertilizer
                # hold-back -- still binds, and `LIQUIDATE_LAST_DAY` below still overrides on the
                # final day, so the deadline case is not this rule's to get wrong.
                if price_ok and RESERVATION_SELL_CAP:
                    n = min(n, reservation_units(
                        prod, market_inv.get(prod, _KG.MARKET_I0 if _KG else 10000),
                        day * TPD + hour, unlocked_shops, have + standing_supply[prod]))
                # **Then top up to keep room for the drop.** Applied AFTER the caps rather than
                # through `allow`, because `allow` is bounded by `rate[prod]` two lines up and the
                # whole point is that the row cannot know about a full shed. It can only ever
                # increase a sale, never block one.
                #
                # Only genuine surplus is released -- stock above what every remaining row will ask
                # for -- so a product a later day still needs is never dumped to make space for
                # tonight. That is what keeps this from becoming the `shed_dusk` arm by accident.
                if release[prod] > 0:
                    n += min(max(0, releasable - n), release[prod])
            else:
                n = min(have, int((row.get("sells") or {}).get(prod, 0)))
            # **On the last day, hold everything the shed has: stock has no terminal value.**
            # Every cap above exists to protect a FUTURE day -- the row is a day total, `rate` bounds
            # one offer, and the whole "holding is not a loss" argument below rests on shops draining
            # the book every 4 steps and the town centre every 12 so a collapsed price recovers. All
            # of that is true right up until there is no next day, and then it is exactly backwards.
            #
            # Measured, seed 11 weeds off against Seb's replay: the season ends with MILK 48 and
            # WHEAT 27 in the shed at quoted prices of $269 and $56 -- $14,424 that simply evaporates,
            # against a $38,593 loss. Day 29's row asks `MILK 16` and we sold precisely 16 of the 64
            # we held, because the row is an absolute count read off HIS trajectory: he reaches the
            # last day holding little milk having sold it all season, and we reach it holding four
            # times the row because we under-sold earlier. The carry recovers a row we MISSED; there
            # was nothing at all for stock the row never named.
            #
            # Raw shed stock, not `have`: the reserves netted out above are a feed buffer and a
            # fertilizer hold-back for tiles that will never be worked again.
            if LIQUIDATE_LAST_DAY and day >= last_day and hour >= LIQUIDATE_FROM_HOUR:
                n = int(shed.get(prod, 0))
            # **CAP_SELL_OFFER_SIZE / LATE_SELL_BIAS -- see the flags' own docstring above.** Both
            # apply AFTER the last-day liquidation override, so neither can touch the one turn this
            # file already puts off limits: stock has no terminal value on the last day, and every
            # other cap in this loop already exempts it on that same principle.
            last_day_liquidating = LIQUIDATE_LAST_DAY and day >= last_day and hour >= LIQUIDATE_FROM_HOUR
            if (LATE_SELL_BIAS and hour < LATE_SELL_FROM_HOUR and not last_day_liquidating
                    and not unfunded
                    and not (prod in NO_DRAIN_PRODUCTS
                             and (day >= SELL_AT_ONCE_FROM_DAY
                                  or day in SELL_AT_ONCE_DAYS))):
                n = 0
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
            # Six products and a cap of five: on the last day the whole shed must fit, so the cap
            # lifts to nine and leaves one slot for anything queued below.
            if n > 0 and len(orders) < (9 if (LIQUIDATE_LAST_DAY and day >= last_day
                                              and hour >= LIQUIDATE_FROM_HOUR) else 5):
                orders.append(["SELL", prod, n])
                state["ordered"][("sold", prod)] += n
                # Proceeds this turn will settle BEFORE any atomic order queued below, because
                # `_process_market` walks the slots and clears each slot's atomic order after every
                # earlier slot has traded. Quoted at the current price, which is a slight
                # over-estimate since a SELL walks the book down one unit at a time -- and an
                # over-estimate is safe here, since `_do_buy_land` simply returns on a short bank
                # and the order is re-offered next turn.
                pending += n * int(prices.get(prod, 0) or 0)

        # **Everything below spends this turn's sales, not just BUY_LAND.** `_process_market` walks the
        # order slots in order and the atomic orders in a slot settle AFTER every earlier slot has
        # traded, so a purchase queued below the day's sells is funded by them. That is already how the
        # day-4 parcel clears on a bank of $718; `money + pending` was simply never extended past the
        # land gate, so seed and livestock could only ever spend yesterday's money.
        #
        # Measured on Seb's tape, seed 11, day 6. He buys `BUY_ANIMAL COW 2` and `BUY_SEED MELON 6` --
        # $1,280 of orders -- at hour 2 on a bank of **$15**, in the same turn as `SELL WOOL 6` and
        # `SELL FERTILIZER 1`. Ours cannot, so the melon waits for the money to land and the day runs
        # out of seed.
        if SELLS_FUND_THE_TURN:
            money += pending
            pending = 0

        # **Seed against the PINS, not today's row.** A planting deferred because the ground or the bank
        # was not ready still needs its seed on the day it finally happens, and the pins are the only
        # record of what is still outstanding. Falls back to the row when the pins are not in play.
        #
        # **Costed HERE, above the livestock, because a seed not bought on its day is a plant not
        # made.** The order below is SELL, HIRE, BUY_LAND, BUY_ANIMAL, BUY_SEED, so a thin bank was
        # always spent on animals first. Measured on Seb's tape, seed 11, day 6 -- the day after the
        # board doubles to 50 tiles, asking `plants {STRAWBERRY: 8, MELON: 6}` against a dawn bank of
        # $802 and a seed bill of $1,280:
        #
        #     tape  h0  BUY_SEED STRAWBERRY 8 + 8 HIRE, bank 869 -> 15
        #     tape  h2  BUY_ANIMAL COW 2 and BUY_SEED MELON 6, funded by that turn's SELL WOOL 6
        #     ours  h0  BUY_ANIMAL COW 1 x2 + 8 HIRE, bank 802 -> 348
        #     ours  h1  BUY_SEED MELON 6, BUY_SEED STRAWBERRY 8  ->  four melon, no strawberry at all
        #
        # A BUY_SEED fills only what the bank covers. Those four seeds are exactly the four plants we
        # make -- one unit, hours 5, 8, 11, 14 -- and from hour 15 the board is seedless while seven
        # units walk: `plant` 4/14, `water` 7/17, `move` 123 against his 93 on identical unit-turns.
        # He defers the cows himself, to hour 2. This does not say animals are a bad buy; it says the
        # seed is due first on the day the ground is waiting for it.
        want_seed = collections.Counter()
        if router:
            want_seed.update(v[1] for v in state["pins"].values() if v[0] == "PLANT")
        else:
            for c, q in (row.get("seeds") or {}).items():
                # The static row does not shrink as the day is planted, so net off today's own plants.
                done = state["planted"][c] - state["planted_dawn"][c]
                want_seed[c] = max(0, int(q) - done)
        seed_bill = sum(RT.SEED_COST.get(c, 0) * max(0, int(q) - int(seeds.get(c, 0)))
                        for c, q in want_seed.items())
        # **The `seeds` row is bought; it is not re-derived from what today can plant.**
        # `seeds` and `plants` are separate rows and they deliberately disagree. Victor's d6 asks
        # `seeds {WHEAT 1, STRAWBERRY 3}` against ONE plant: he buys four, plants one, and carries
        # three into d7, which needs fifteen seeds for fourteen plants. Seed lives in
        # `private["seeds"]`, never the shed, so a surplus carries with no capacity cost at all.
        #
        # Under `router`, `want_seed` is the remaining PLANT pins, and pins are sited only on ground
        # that is empty AT DAWN. So a full board buys nothing: `buy_seed 1/4` on d6, and on d8 the
        # row's `{WHEAT 8, STRAWBERRY 2}` is offered as WHEAT 8 and no strawberry at all -- which is
        # why all seven of d8's plants come out wheat and `strawb` sticks at 18/20.
        #
        # **Applied to the EMISSION only, never to `seed_bill`.** That is the whole reason three
        # earlier attempts at this failed. `seed_bill` is reserved out of the bank before any
        # BUY_ANIMAL (see `SEED_BEFORE_LIVESTOCK`), so folding the row into it makes seed outrank
        # livestock: d0 went `buy_animal 5/5 -> 4/5`, `place 5/5 -> 4/5`, `sheep 4/4 -> 3/4` and
        # stopped matching. The bill stays exactly what the pins justify; only what is OFFERED is
        # floored at the row.
        emit_seed = collections.Counter(want_seed)
        for c, q in (row.get("seeds") or {}).items():
            # **Net off seed BOUGHT today, never seed sown today.** The row is a purchase total,
            # and a planting can be paid for out of the carry -- seed lives in `private["seeds"]`
            # and rides between days at no capacity cost, which is the whole reason d6 buys four
            # and plants one. Netting against plantings makes those carried-seed plantings cancel
            # units off the day's own buy.
            #
            # d7 is where it shows: `seeds {WHEAT 3, STRAWBERRY 9}` = 12 against FOURTEEN plants,
            # opening on a store of `{WHEAT 1, STRAWBERRY 2}`. Two hours in, `done` is 2 and the
            # strawberry floor has fallen 9 -> 8. `buy_seed 11/12`, and d7 ends on an empty store
            # where the tape ends holding one strawberry. `plant 14/14` and `strawb 18/18` both
            # matched, which is why it read as harmless. That seed is untouched through d8, d9 and
            # d10 and then buys a planting on d11: `buy_seed 3/4`, `plant 9/11`, `water 38/41`.
            #
            # The purchases need no new tally -- the store and the plantings give them exactly.
            done = state["planted"][c] - state["planted_dawn"][c]
            bought = int(seeds.get(c, 0)) + done - int(state["seeds_dawn"].get(c, 0))
            emit_seed[c] = max(int(emit_seed.get(c, 0)), max(0, int(q) - max(0, bought)))

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
        if HIRE_FIRST and day in HIRE_PINNED_DAYS and hour == 0:
            want = int(row.get("hands", 0) or 0)
            # **A hand walled in for the whole day is a loader; one walled in until lunchtime is a
            # loss.** `_spawn_hand` fills the ring `(4,4) (5,4) (4,5) (5,5)` by occupancy, and while
            # NW is the only quadrant `(5,5)` has no unlocked neighbour to step out to. On a day that
            # buys nothing that is permanent and fine -- d0 strands one, the TAPE strands one, and d0
            # matches op for op. On a day that buys a parcel it is premature: the parcel is NE and NE
            # is `(5,5)`'s way out. Victor plays it explicitly, HIRE at h0/h0/h0 and the fourth at
            # h17, one hour after his BUY_LAND at h16.
            #
            # So hold back exactly the hires that would land walled, and let the top-up below place
            # them once the ground exists. Held, never cancelled: `state["hired"]` is not credited,
            # so the day still reaches its `hands` row.
            if int(row.get("land", 0) or 0) > 0:
                want = min(want, _unwalled_landing_slots(tiles, units, want))
            for _ in range(want):
                orders.append(["HIRE"])
                state["hired"] += 1
        elif HIRE_FIRST:
            target = int(row.get("hands", 0) or 0)
            # **The top-up runs all day on a land day.** `hour < 8` is right for the ordinary drip --
            # a hand hired at dusk buys nothing -- but the square a held hire is waiting for opens
            # when the parcel settles, and on this schedule that is h13. Gating the top-up at 8 would
            # hold the hire back and then never place it.
            deadline = TPD if (int(row.get("land", 0) or 0) > 0) else 8
            if state["hired"] < target and hour < deadline:
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
                    if walled:
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

        # **Float the cow/sheep split on the shop draw -- see `SHOP_ADAPT_HERD`'s docstring.**
        # The COUNT the schedule asks for is kept exactly; only the species is re-decided, and only
        # for animals the schedule places from `SHOP_ADAPT_FROM_DAY` on. Days before that keep the
        # reference mix, because barely a third of the season's shop demand is on the board yet.
        #
        # `town_drain_remaining` is the same function the sell rule uses and mirrors `_town_consume`
        # exactly, so "how much of this product will the town still take" is a fact read off
        # `town.unlocked_shops` and the step, not an estimate. Headroom is that drain minus what the
        # animals we have already bought will themselves produce over the days that remain; each
        # assignment then spends its own animal's production out of the headroom it chose, so a run
        # of assignments cannot all claim the same units.
        if SHOP_ADAPT_HERD and day >= SHOP_ADAPT_FROM_DAY:
            # **The floor is a COUNT, not a set of days.** Every one of the reference schedule's 21
            # animals sits on a row at day 10 or earlier -- the note at the top of this block records
            # that "from day 11 the schedule's rows are empty" -- so splitting the rows by day leaves
            # nothing to reallocate. What actually floats is the herd ABOVE the floor, and because a
            # purchase blocked by a thin bank is retried for the rest of the season, an animal on a
            # day-9 row is routinely still unbought at day 15, when the shops are known.
            # **Re-decide every turn, but only ever allocate the REMAINING budget.**
            #
            # A split recomputed from scratch each turn buys up to BOTH ceilings as the choice flips,
            # because the loop below buys `want_total[a] - bought[a]` and `bought` never decreases:
            # measured at COW 20 + SHEEP 18 = 38 animals against a schedule asking for 21.
            #
            # Latching the decision at day 11 fixes that and throws away real information -- seed 41
            # draws its YARN_STORE on day 12, one day after the latch, and would be locked to the
            # 5-sheep floor on a board that ends up absorbing wool.
            #
            # Anchoring the split on what has ALREADY been bought gives both: the target can only
            # grow, so the total is capped at the schedule's own count, while every animal still
            # unbought is re-aimed at whatever the shops now say. Shops keep unlocking to day 24, so
            # this keeps improving as the evidence arrives.
            # **Ask about the SEASON, spend along the schedule's rows -- see
            # `HERD_SPLIT_IS_A_SEASON_DECISION`.** Handing the split today's partial herd made it
            # decide the buying ORDER as well as the mix, and its cows-first fill deferred every
            # floating sheep to the end of the herd.
            _season = collections.Counter()
            for dd in sched:
                for a, qty in (sched[dd].get("animals_bought") or {}).items():
                    _season[a] += int(qty)
            _s = _herd_split(_season, state["bought"], day, hour, unlocked_shops, last_day)
            # Published so a replayed day can re-label the tape's heads to the same target. The
            # season target is a property of the shop draw, not of who is driving the turn, so
            # there is one answer and both callers must read it rather than compute their own.
            state["herd_split"] = dict(_s)
            _through = _herd_through_day(sched, day, _s)
            want_total["COW"], want_total["SHEEP"] = _through["COW"], _through["SHEEP"]
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
            # **One order per SPECIES, not per head.** `maxMarketOrdersPerTurn` is 10
            # (`kaggriculture.py:538`), `_parse_order` takes any `n > 0` (`:626-635`) and the lockstep
            # loop commits one animal per unit-iteration, so `SHEEP 4` fills four pens in ONE slot.
            #
            # The cost of not doing this is a slot famine at hour 0, not a price. Victor's d0 h00 is
            # `BUY_PRODUCT WHEAT 11`, four HIREs, `COW 1`, `SHEEP 4` and both BUY_SEED rows -- nine of
            # ten slots, the whole day's shopping. Ours was four HIREs and five single-head animal
            # orders, also nine, and the wheat block below is guarded by `len(orders) < 9` -- so the
            # day's wheat row was refused for want of a SLOT while the bank still held $3,000. It
            # then dribbled out from h01 against a bank the hires and animals had emptied, reaching
            # four of eleven. A FEED eats one wheat, so `feed 4/5` and `care 4/5` on the five animals
            # placed that day are the same defect one step further down.
            #
            # The per-head loop stays for the ACCOUNTING -- affordability, the seed-bill reserve and
            # the hire eviction still decide one head at a time -- and only the emission is batched.
            # A partly affordable batch is safe: `_do_buy_animal` re-checks the bank per unit
            # (`:666-673`) and stops, exactly as the per-order form did.
            want = 0
            for _ in range(max(0, qty - state["bought"][a])):
                if money < R.ANIMALS[a]["cost"] + seed_bill:
                    continue
                # The slot is charged once, for the first head of this species.
                if want == 0 and len(orders) >= (10 if ANIMAL_OVER_HIRE else 8):
                    if not ANIMAL_OVER_HIRE:
                        continue
                    last = next((i for i in range(len(orders) - 1, -1, -1)
                                 if orders[i][0] == "HIRE"), None)
                    if last is None:
                        continue
                    orders.pop(last)
                    state["hired"] -= 1
                want += 1
                state["bought"][a] += 1
                money -= R.ANIMALS[a]["cost"]
            if want:
                orders.append(["BUY_ANIMAL", a, want])

        # **TAKEN 2026-08-07: order the seed rows dearest crop first.** A BUY_SEED fills only what
        # the bank covers, so under a thin bank the row order decides which crop gets planted, and the
        # tape places its day-6 strawberry ($800) before its melon ($480) on a bank of $802. Copying
        # that ordering measured WORSE on the day it was derived from: `plant` 8/14 -> 7/14 and
        # `sell` 18/19 -> 10/19. Filling the cheap block whole plants more tiles than filling the dear
        # one whole, and the tiles are what the day is for.
        #
        # **RE-MEASURED 2026-08-07 once the bank was repaired, because the first reading was taken
        # against a bank this ordering could not survive.** Day 6's dawn was $830 then and $869 now
        # (the sell-slot fix), and $869 - $54 of hires clears the $800 strawberry where $830 did not.
        # So the arm genuinely changed meaning, and on the re-measurement it is TAKEN:
        #
        #                    d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 d10 d11   total
        #     without         7  6  4  7  7  7 13 20 15 15  24  22    147
        #     dearest first   7  6  4  7  7  7 12 18 17 17  24  23    149
        #
        # Read on its own it was a TRADE, not a free win: it bought d6 and d7, the two earliest
        # unfixed days, and paid for them with d8 and d9. Days are matched IN ORDER, so buying the
        # earlier pair was the improvement even though the total rose by 2.
        #
        # Its price was that the melon block stopped filling -- `peak["MELON"] < 6`, exactly the
        # mechanism the paragraph above describes -- which is what exposed the missing retry below.
        # With that fixed the trade-off is GONE: the dear block fills first and the cheap one is
        # re-offered until the day's sales cover it, so both land. d6-d11 read 11 15 13 15 18 20.
        # **Need order first, block cost as the tie-break.** See `_seed_need_order` for the d10
        # measurement: the price order buys the crop the plan reaches at h5 and starves the one it
        # reaches at h2. A crop with no PLANT stop in any committed tour sorts last, which is where
        # the old rule already put anything the day was not about to plant.
        _need = _seed_need_order(units, state.get("routes") or {})
        for crop, qty in sorted(emit_seed.items(),
                                key=lambda kv: (_need.get(kv[0], 1 << 30),
                                                -RT.SEED_COST.get(kv[0], 0) * int(kv[1]))):
            # **No cross-turn `ordered` credit on the seed row.** A BUY_SEED the env rejects for want of
            # funds is silent -- there is no failure in the observation, only seed that never arrives --
            # and crediting the attempt made the rejection PERMANENT for the rest of the day. Day 6 of
            # Seb's tape, seed 11: dearest-first spends $800 of the $869 dawn on strawberry, the melon
            # is offered at h1 against $15, it is refused, and the row's 6 melon are never re-offered.
            # Peak melon held all day: 0. The tape offers its melon at h2 in the same order list as
            # `SELL WOOL x6`, sell first, so the wool funds the seed inside one turn.
            #
            # Re-offering every turn cannot run away, because both terms are live: under `router`
            # `want_seed` is the remaining PLANT pins, which pop as they are planted, and `seeds` is
            # what is actually held. Once the buy lands, `short` is zero on the next turn by itself.
            short = int(qty) - int(seeds.get(crop, 0))
            # **The row floors the ORDER, not the requirement.** Netting the store off `qty` is right
            # for the pins -- seed already held plants a pin without buying anything -- but it also
            # cancels the row against the carry, and the row is a PURCHASE total the tape actually
            # placed. d7 asks for `STRAWBERRY 9` on 10 pins over a store of 2: `short` comes out 8, we
            # buy 11 of the row's 12, and the day ends on an empty store where the tape ends holding
            # one. Three days later that seed is `plant 9/11` and `water 38/41` on d11.
            #
            # Netted against seed BOUGHT today, which the store and the plantings give exactly, so
            # the floor cannot re-order what has already landed.
            _row_q = int((row.get("seeds") or {}).get(crop, 0))
            _done = state["planted"][crop] - state["planted_dawn"][crop]
            _bought = (int(seeds.get(crop, 0)) + _done
                       - int(state["seeds_dawn"].get(crop, 0)))
            short = max(short, _row_q - max(0, _bought))
            # **Never buy seed no remaining row can plant.** The floor above is the tape's purchase
            # total, which is right while later days still have plantings to spend the carry on and
            # wrong on the last planting day: `d27` asks `WHEAT 12` against a board the pins can only
            # seat 8 of, and the difference is money sitting in the shed at the final bell. Measured
            # on ladder game 94282682 we close holding 9 WHEAT and 9 CARROT -- $270 at `SEED_COST` --
            # on a ladder where 41% of games are decided inside $3,000 and the narrowest losses are
            # $20 and $85. カワシギ carries the same 8+8, so it is value the whole field abandons.
            #
            # The cap is today's REAL pins plus whatever LATER rows still ask for -- never today's row
            # slack. That preserves the carry the row floor exists for (d6 buys four and plants one
            # because d7 needs fifteen) and trims only seed the season has no planting left for.
            # **A later row is only a reason to carry seed if that day can still GROW the crop.**
            # `_later` counted every remaining row, including days past the last on which the crop can
            # finish -- `RT.plant_prize` is already 0 there, and `_refresh_pins` drops such a pin, so
            # those rows are never sown and the seed bought for them is dead. It is the tail of the
            # wheat residue: we close holding 3 WHEAT on the straw arm, and ladder games show 2 and 4.
            _later = sum(collections.Counter(sched.get(_d, {}).get("plants") or [])[crop]
                         for _d in range(day + 1, R.SEASON_DAYS)
                         if RT.plant_prize(crop, _d) > 0)
            # **The 5 STRAWBERRY seed we close holding cannot be recovered here, and it was tried.**
            # Capping this purchase by the strawberry ceiling measured a byte-identical season on all
            # four arms -- same money, same seed left. The seed is bought during the REPLAYED opening
            # d4-d11, before `STRAWBERRY_FLOAT_FROM_DAY`, so it is already spent by the time any cap
            # can act, and seed cannot be sold back (`private["seeds"]` is not a market product). The
            # only way to reach it is to stop replaying the tape's own BUY_SEED, which changes the
            # opening this whole agent is built on. Recorded so it is not re-derived: $500 on the straw
            # arm, $400 on each q4 arm, and it is sunk, not leaking.
            short = min(short, max(0, int(want_seed.get(crop, 0)) + _later
                                   - int(seeds.get(crop, 0))))
            if short > 0 and len(orders) < 9:
                orders.append(["BUY_SEED", crop, short])

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
        # KAWASHIGI tape places sixteen separate WHEAT buys of 1-6 across h1-h22, interleaved with ten
        # sells, and the shops restock every 4 steps so the book recovers between them.
        #
        # **That is kawashigi's cadence and it is NOT the leader's. Corrected 2026-08-20.** Measured
        # on tetsuya's board `94345389`, seat 0, seed 959074148 (`data/logs/cadence_2026-08-20.log`):
        # he places ONE WHEAT block per day, at hour 1, sized to that day's `feeds`, and it fills
        # WHOLE every time -- d0-d6 are +5 +5 +5 +5 +6 +8 +8 and the shed reads 5 5 5 5 6 8 8 at h1.
        # An 8-unit single order does not walk the price far enough to matter at these sizes on this
        # book. His shed then drains to 0 by h2-h3, so nothing is carried.
        #
        # Ours on the same board: 3 at h6 on d0 where he buys 5 at h1; `+3 +1 +1 +1` dribbled across
        # h5-h9 on d4; and 10-36 units of dead stock sitting in the shed on d4-d6 while we keep
        # ordering. The drip is spreading an order the leader places in one piece.
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
        # **A mouth already fed today is not a mouth to buy for.** The floor targets a fixed two-day
        # supply on EVERY turn and never shrank as the day's own FEED ops consumed it: FEED takes one
        # wheat from the hand per animal and cannot re-fire once `fed_today` is set
        # (`reference/kaggriculture.py:480-488`), so `on_hand` falls all afternoon for a completely
        # legitimate reason and the floor reads the drop as a shortfall.
        #
        # Measured on Seb's tape, seed 11, day 5. The top-up correctly buys 4 at hour 1, matching the
        # row. By hour 8 six of seven animals are fed, `on_hand` has fallen 14 -> 9 purely from that
        # feeding, and the floor reads `14 - 9 - 4 = 1` and fires a fifth order. `feed` lands 7/7
        # either way, so the extra unit is never eaten -- it shows up one for one as excess wheat in
        # day 6's dawn shed, `sh:wheat 8/7`.
        fed_today = sum(1 for r in tiles for c in r
                        if isinstance(c, dict) and "animal" in c and c.get("fed_today"))
        herd = (feed_days(day) * alive - fed_today - on_hand
                - state["ordered"][("feed", "WHEAT")])
        # **The drip has to bound the HERD path too, or it bounds nothing that matters.** This read
        # `max(herd, min(max(0, owed), BUY_DRIP))`: the row was dripped and the herd's whole remaining
        # need then overrode it, so the one order `BUY_DRIP` exists to spread was the one it never
        # touched. Day 9 bought 8 in a single order at hour 1 and sat on $22 until hour 16.
        #
        # This is NOT `FEED_ORDER_CAP`, which bounded the DAY and starved a 19-animal herd. `herd`
        # subtracts `state["ordered"][("feed", "WHEAT")]`, so the remainder is re-offered every turn
        # and the herd still gets its full ration -- just spread across the hours, which is what the
        # constant's own docstring already claimed it did.
        short = min(max(herd, min(max(0, owed), BUY_DRIP)), FEED_TURN_CAP)
        # **The schedule's row is an instruction, not a cadence.** `BUY_DRIP` and `FEED_TURN_CAP`
        # exist to spread the HERD's ration across the day; applying them to `owed` metered the row
        # too. Traced hour by hour on the Victor grid, seed 11, d0:
        #
        #     h00  owed=11  short=1  money=600  cap=12  orders=8
        #     h04  owed= 7  short=0  money= 33  cap= 0     <- dead for the rest of the day
        #
        # Twelve were affordable at dawn and we ordered one; by h04 the bank was $33, the
        # affordability cap was 0, and the remaining seven were never bought. `buy_product 4/11`,
        # and since a FEED eats one wheat, only four of the five animals placed that day could eat
        # -- `feed 4/5`, `care 4/5`, and the herd's missed night inherited by every later day.
        #
        # Scoped to hour 0 deliberately. The whole-day version was tried
        # (`max(min(herd, FEED_TURN_CAP), min(owed, BUY_DRIP))`) and took d7 `buy_product` 14/14 ->
        # 0/14: spending earlier at every hour starves the later orders. At dawn the bank is at its
        # maximum for the day and the row is exactly what the schedule says the day needs.
        # **A block refused a slot is still the dawn block.** The append below is gated on
        # `len(orders) < 9`, and on Victor's d7 the h00 queue already holds ten orders -- two
        # sells, seven hires and the cow -- so the 14-wheat row is dropped on the floor with
        # $2,512 standing ready to pay for it, and from h01 the `hour == 0` gate hands it to the
        # 1/turn drip. u1 then drains the shed at h02, u4's depot want `{WHEAT: 3}` is deleted
        # against a shed reading 0, and the day closes `feed 9/10`, `care 9/10`, `collect_fert
        # 6/7`. The tape's own cadence on the same day: Victor's h01 queue is also exactly ten,
        # and he ships `BUY_PRODUCT WHEAT 6` as a block at h02, the first turn with a free slot.
        # So the boost stays live until the block is actually QUEUED -- not until h00 has passed.
        # `dawn_row_sent` is set at the append, never by the slot gate refusing it; a partial
        # send shrunk by the money guard still counts as sent, which is today's behaviour for a
        # thin bank, and `SKIP_THE_RATION_ON_A_LAND_TURN` zeroing `short` leaves it unsent so a
        # land day re-offers once the parcel's turn is over.
        if owed > 0 and not state.get("dawn_row_sent", False):
            short = max(short, owed)
        # **The ration is not discretionary spending and is not held to half the bank.** This line
        # used to read `short = min(short, int(money * 0.5 // quote))`. On a thin dawn that floors to
        # ZERO: d1 opens on $44 against a quote of $28, so `int(44 * 0.5 // 28) == 0` and the row of
        # five buys nothing for six hours, then dribbles 2+1+1 and lands three. d5 is the same shape,
        # `cap50 == 1` against a row of two. The tape buys its five outright.
        #
        # Those one- and two-unit misses are the whole chain: d3's dawn shed holds exactly 2 wheat
        # and the day feeds exactly 2 of 4, the sheep miss production days, and d6 shears 9 where the
        # tape shears 12 -- which is the $599 that leaves d7 unable to afford its third animal and d8
        # opening on an empty shed.
        #
        # A half-bank reserve is the right instinct for a purchase that can wait. FEED cannot: two
        # unfed days remove the animal outright (`kaggriculture.py:804`), and the order is already
        # bounded three ways -- by `owed` (the day's own row), by `BUY_DRIP`, and by the env refusing
        # what the bank cannot cover. The cap was a fourth bound on the one purchase that needed none.
        # **What n units COST, not n times the sticker price.** `market_price` moves per unit inside
        # one order -- said twice above, as the whole reason `BUY_DRIP` exists -- and this guard did
        # not use it. `int(money // quote)` prices four wheat at 4 x $28 when the book charges
        # 28 + 29 + 30 + 31 = $118, so the last unit does not fill. And it is not merely lost: the row
        # is closed on orders QUEUED (`state["ordered"]` below), so the shortfall is never re-offered.
        #
        # Measured d1, seed 11, offered against FILLED: h04 bank $13, price $28, offered 4, filled 3;
        # h11 offered 1, filled 1. The $26 the book left is exactly the bank h11 opens on. The row of
        # five closed at four, and that fifth wheat is d3's fourth feed.
        #
        # `market.inventory` is `shared: True` in the observation spec, so this is the real book and
        # not a guess. Falls back to the flat divide if the env is not importable, which is what
        # `market_price` already does.
        _book = int(((obs.get("market") or {}).get("inventory") or {}).get("WHEAT", 0) or 0)
        _purse, _n = money, 0
        while _n < short:
            _unit = market_price("WHEAT", _book - _n)
            if _unit > _purse:
                break
            _purse -= _unit
            _n += 1
        short = _n
        # **Do not queue the ration behind the parcel.** `state["ordered"]` is credited when an order
        # is QUEUED, and a BUY_PRODUCT the env refuses is silent, so an order that loses the slot race
        # still closes the row and the day never retries. d6 h10: bank $43, wheat $33, and the turn
        # queues `SELL WOOL 5, SELL FERTILIZER 1, BUY_LAND, BUY_SEED STRAWBERRY 3, BUY_PRODUCT WHEAT
        # 1`. `_process_market` walks the slots in order, so the $1,000 parcel and the seed take
        # everything the wool raised and the wheat -- last in the queue -- fills nothing. The row of
        # five closed at four and the bank was back to $90 by dusk with nothing spending it.
        #
        # Skipped rather than resized: the turn a parcel clears is not a turn that can also feed the
        # herd, and holding the order costs nothing because the row is re-offered every turn.
        if any(o and o[0] == "BUY_LAND" for o in orders):
            short = 0
        # **TRIED AND REVERTED 2026-08-20: `< ORDER_SLOTS` instead of `< 9`.** On tetsuya's d0 the
        # turn sends six HIREs, two BUY_ANIMALs and a BUY_SEED -- exactly nine -- so the slot gate
        # looked like the reason one wheat reached the shed and one of five animals got fed. It is
        # not: opening the tenth slot left `feed 1/5` on d0 byte-for-byte and moved d0-d10 PASS from
        # 911 to 959.
        #
        # The gate is downstream of `(alive or owed > 0)`, and at hour 0 no animal is on the board
        # yet -- the row's five are placed h05-h08. A board read cannot see them, so the ration is
        # never sized in the first place and the slot it would have taken is irrelevant.
        #
        # Whatever fixes this has to make the DAWN order know what the row will place, not find it
        # a slot.
        # **The ORDER_SLOTS gate is NOT the constraint. Measured twice, inert both times.**
        # Alone: d0 feed 1/5 byte-for-byte. On top of the arrival-ration fix: d0 feed 3/5
        # byte-for-byte, identical to the ration fix by itself. Left at 9.
        #
        # **The PRE-TRIM was the constraint, and it is not the same thing. Removed 2026-08-20.**
        # Both measurements above raised the pre-trim from 9 to 10 -- one more slot, with the ration
        # still queued BEHIND the spending, where `_fit_slots` cuts from the tail. That is why they
        # were inert. This drops the pre-trim from the ration entirely and lets the two functions
        # that already exist for this do their job: `_wheat_row_first` slides a BUY_PRODUCT WHEAT
        # ahead of the first HIRE/BUY_ANIMAL/BUY_SEED, and `_fit_slots` drops a surplus HIRE from the
        # last one backwards rather than the ration. Neither could ever run, because the order was
        # never appended.
        #
        # What it cost, on tetsuya's board `94345389` seed 959074148: d3's hour-0 queue is already
        # full of hires and animals, so the row's 5 WHEAT is dropped on the floor and falls through
        # to the 1/turn drip. The shed reads 0 at h1 -- the hour the dawn tour reaches it -- so the
        # PICKUP loads nothing, the unit walks to the pen empty, and FEED is not live because it
        # takes a WHEAT from the ACTING unit's carried inventory (`reference/kaggriculture.py:505`).
        # The stop spends its turn on COLLECT_FERTILIZER instead. Pen (4,3) misses d3 and d4, hits
        # `consecutive_unfed >= 2` and escapes at d4 night. See
        # `docs/the_ration_is_not_in_the_shed_when_the_plan_says_it_is_2026-08-20.md`.
        if (alive or owed > 0) and short > 0:
            orders.append(["BUY_PRODUCT", "WHEAT", short])
            # The dawn block is SENT the moment any order sized by its boost is queued -- even one
            # the money guard shrank -- and never by the slot gate refusing it. See the note at the
            # boost above.
            state["dawn_row_sent"] = True
            state["ordered"][("feed", "WHEAT")] += short
            state["ordered"][("buys", "WHEAT")] += short
            # Debit at the price we just QUOTED, not the old hardcoded $60. Charging $60 for wheat
            # bought at $25 understates the running bank by $35 a unit, and every later order on the
            # same day -- seed, animals, the second feed top-up -- is sized against that wrong bank.
            money -= quote * short

        # **End the day holding tomorrow's ration.** See `DUSK_FEED_TOPUP`.
        if (day >= DUSK_FROM_DAY and hour >= DUSK_FEED_HOUR
                and len(orders) < 9):
            # **Tomorrow's animals are tomorrow's wheat bill.** Pre-buying a ration for a pen that
            # will not exist until the next day is one purchase too many on the day it fires, and on
            # d2 that single wheat is the whole gap: `buy_product 6/5`, money $624 against $654, one
            # unit at ~$31. The tape places a COW on d3 and buys its feed ON d3, where its row says
            # `buys: {WHEAT: 7}` against d2's 5.
            arriving = 0
            # **Shed only, and re-evaluated every turn.** Three variants were measured and this is
            # the one that works, over six seeds, whole season:
            #
            #     shed only                       2 lost   mean $58,308   <-- this
            #     minus wheat in hands            8 lost   mean $59,475
            #     minus `on_hand` (adds ripe)     6 lost   mean $59,735
            #     minus what it already ordered  14 lost   mean $60,639
            #
            # Wheat in a hand at dusk was DRAWN for a pen and is already earmarked, so counting it as
            # spare inventory under-buys; `ripe_wheat` is standing crop and is only ours if it gets
            # harvested. Subtracting its own prior orders over-suppresses because `state["ordered"]`
            # does not scope the way that needs. The naive form is the correct one.
            # **Only the SURPLUS in hands counts.** Wheat a hand is carrying is drawn for pens it
            # still has to serve today; counting it as spare stock under-buys and the pen it was
            # for goes hungry -- d6 `feed 7/7 -> 5/7` with the raw sum. What is held ABOVE the pens
            # still unfed is genuinely ours at the rollover.
            carried_now = sum(collections.Counter(iv).get("WHEAT", 0) for iv in invs)
            unfed_now = sum(1 for r in tiles for c in r
                            if isinstance(c, dict) and "animal" in c and not c.get("fed_today"))
            spare = max(0, carried_now - unfed_now)
            gap = (alive + arriving) - int(shed.get("WHEAT", 0)) - spare
            gap = min(gap, FEED_TURN_CAP, int(money // quote))
            # **And never past what the day's own `buys` row still owes.** The top-up reads the shed
            # and nothing else, so it cannot see what the day has already bought. Victor's d6 row is
            # `buys {WHEAT 5}` and he drips exactly five; we take four by h01 and the top-up adds two
            # more at h18 and h19 -- the first of them against a herd with `unfed 0`, nothing left to
            # feed tonight. Six for a row of five, and the same over-run on d10 (14/12) and d11 (7/6).
            #
            # The row is the plan's statement of the day's ration. This rule exists to catch a row
            # that is SHORT, not to add to one already met, and a wheat round trip pays the spread
            # both ways -- the same lesson `NET_THE_TWO_LEGS` records on the sell side.
            #
            # A day with no `buys` row keeps the top-up unbounded: there the formula is the only rule
            # there is.
            row_buys = int((row.get("buys") or {}).get("WHEAT", 0) or 0)
            if row_buys > 0:
                gap = min(gap, row_buys - int(state["ordered"][("buys", "WHEAT")]))
            if gap > 0:
                orders.append(["BUY_PRODUCT", "WHEAT", gap])
                topup_orders.add(id(orders[-1]))
                state["ordered"][("feed", "WHEAT")] += gap
                state["ordered"][("buys", "WHEAT")] += gap
                money -= quote * gap

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

        # ------------------------------------------------------------------- net the two legs
        # **A turn that sells wheat and buys wheat has already lost, whatever the reserves say.**
        # Two guards protect the same floor -- `feed_days(day) * alive`, 7 on day 4 -- from different
        # stock: the sell guard nets off wheat carried in hands, `DUSK_FEED_TOPUP` counts the shed
        # alone. So the sell empties the shed, the top-up sees it empty, and both fire in the same
        # turn: d4 h19 `SELL WHEAT 6` beside `BUY_PRODUCT WHEAT 1`, again at h22, and inverted at
        # h23. Nine such turns over d0-d16, and `buy_product 21/1` on d4 against a tape that buys
        # ONE wheat all day.
        #
        # Made to agree at the source it is worse, and that was measured rather than argued -- see
        # `RESERVE_COUNTS_WHEAT_IN_HANDS` for the arm and `DUSK_FEED_TOPUP` for the three top-up
        # variants. Both of those change how much is held back, which changes what the day can sell
        # at all. Netting changes neither: the same reserve, the same target, minus the round trip
        # that cancels itself. The larger leg survives at its net size and the smaller disappears.
        sells = collections.Counter()
        buys = collections.Counter()
        for o in orders:
            if o and o[0] == "SELL":
                sells[o[1]] += int(o[2])
            elif o and o[0] == "BUY_PRODUCT" and id(o) in topup_orders:
                # **Only the TOP-UP leg counts as the accident.** The round trip this rule was
                # written for is the sell guard and `DUSK_FEED_TOPUP` disagreeing about the same
                # stock, which is this order and no other. The row's own `buys` line is not an
                # accident: Victor's d5 sells WHEAT 17 at dawn and buys seven singles back
                # through the day on purpose, and netting the two deleted seven real sales and
                # then, once the counter gave them back, two real purchases instead.
                buys[o[1]] += int(o[2])
        for prod_ in set(sells) & set(buys):
            cancel = min(sells[prod_], buys[prod_])
            if cancel <= 0:
                continue
            for side, want in (("SELL", cancel), ("BUY_PRODUCT", cancel)):
                left = want
                for o in orders:
                    if left <= 0:
                        break
                    if side == "BUY_PRODUCT" and id(o) not in topup_orders:
                        continue
                    if o and o[0] == side and o[1] == prod_:
                        take = min(left, int(o[2]))
                        o[2] = int(o[2]) - take
                        left -= take
            # The buy legs were debited against `state["ordered"]` when queued; a cancelled buy
            # is one we never place, so the running total has to give it back or the next turn
            # sizes its top-up against a purchase that did not happen.
            state["ordered"][("feed", prod_)] = max(
                0, state["ordered"][("feed", prod_)] - cancel)
            state["ordered"][("buys", prod_)] = max(
                0, state["ordered"][("buys", prod_)] - cancel)
            # **And the SELL leg the same way, for exactly the same reason.** It was credited
            # with the full offer when queued, above, and nothing here gave any of it back --
            # so a day that offered 17 and shipped 10 spent the rest of the day believing its
            # row was met, and `CUMULATIVE_SELLS` never re-offered the seven. Victor's d5 is a
            # deliberate 17-at-dawn against seven singles bought back through the day; the
            # netting is welcome to keep cancelling the overlap, but it may not also mark the
            # cancelled units as sold.
            state["ordered"][("sold", prod_)] = max(
                0, state["ordered"][("sold", prod_)] - cancel)
        orders = [o for o in orders if not (len(o) > 2 and int(o[2]) <= 0)]

        return {"farmer": acts[0] if acts else ["PASS"], "hands": acts[1:],
                "market": _order_sells(_fit_slots(_wheat_row_first(orders, hour), state))}

    if not REPLAY_OPENING_DAYS:
        return agent

    # **The tape supplies the unit actions and the SELL cadence. The buying stays ours.** The planner
    # is still driven on every replayed turn and its unit answer thrown away, so its pins, pen
    # reservations and `uncovered` sell ledger are warm at the handover and no row is recorded as
    # missed. That is the same construction `scripts/breakdown.py --handover` uses, and it is why
    # neither needs the `start_day` parameter that `fa96ace` deleted with the predecessor agent.
    #
    # **Why the buys are not the tape's.** Both of our allocation decisions -- the melon/strawberry
    # arm and the COW/SHEEP split -- are taken around d3-d6 and then EXPRESSED as purchases on the
    # replayed days. Handing those to the tape as well silently discards both. Measured on seed 11
    # with the whole market replayed, ours/tape at d12: `melon 15/8` against 7 normally,
    # `strawb 24/34` against 33, `wheat 22/15` against 15. The strawberry season never installed and
    # the melon it should have cleared stood all season.
    #
    # It lives HERE rather than in the submission bundler because `scripts/resolve_days.py` drives
    # this module: a route solved without the opening is solved for a trajectory we no longer play,
    # and `PRECOMPUTED_ROUTES` is keyed on `(tile, ops)` state, not on geometry.
    # Both arms' openings, loaded once. Which one applies is read off the q4 latch at the first
    # replayed turn -- by then `_Q4.arm` has decided, since `DECIDE_BY_DAY = 6` and the first
    # replayed day is 6.
    # **From `EMBEDDED_OPENINGS` when the bundler filled it, off disk otherwise.** A submission has no
    # `data/` tree, so a bundle that reads the tape from a path finds nothing, `_replay_opening`
    # returns `{}` as designed, and the replay silently does not happen -- an artifact that claims to
    # replay and does not. The whole 30 MB replay is not needed for that: only our own seat's
    # `farmer`, `hands` and `market` for the days in `REPLAY_OPENING_DAYS`, which is 23 KB a tape
    # against 30 MB, so the bundler embeds it and sets this.
    openings = ({tuple(k): {int(s): v for s, v in op.items()}
                 for k, op in EMBEDDED_OPENINGS.items()} if EMBEDDED_OPENINGS else
                {key: _replay_opening(REPLAY_OPENING_DAYS, *tape)
                 for key, tape in REPLAY_OPENING_TAPE.items()})

    def replayed(obs, config=None):
        # Snapshot before driving the planner, because a replayed turn throws its answer away and
        # must not keep its side effects on the purchase counter -- see below.
        bought_before = dict(state["bought"])
        planted_before = dict(state["planted"])
        live = agent(obs, config)
        step = int(obs.get("step", 0) or 0)
        # Both latches, read through the branches' OWN `armed_key` rather than a string written here.
        # A hand-written `"branch_armed"` pinned the melon latch False -- nothing writes that name,
        # `MelonBranch.armed_key` is `"melon_armed"` -- so the strawberry tape was unreachable by
        # construction and the strawberry arm silently replayed his melon season.
        opening = openings[(bool(state.get(_MB.BRANCH.armed_key)),
                            bool(state.get(_Q4.BRANCH.armed_key)))]
        if step not in opening:
            return live
        # **`state["bought"]` must count what the TAPE ordered, not what the discarded planner would
        # have.** It is a purchase-INTENT counter, incremented where the `BUY_ANIMAL` row is queued,
        # and on a replayed turn that row is never sent. Left alone it hands d12 a herd nobody
        # bought, and `_herd_split` anchors on it, so the species target drifts with it.
        state["bought"].clear()
        state["bought"].update(bought_before)
        # **And the same for `state["planted"]`, for the same reason and with worse consequences.**
        # `_refresh_pins` accumulates `want` over every row up to today and seats pins for
        # `want - planted - live`, so a crop the tape put in the ground and the counter never saw is
        # a debt the planner chases for the rest of the season. Measured 2026-08-18, strawberry arm,
        # own seed 70683142: 37 strawberry standing at d12 and the counter reading 0, so d12's row of
        # 5 became 10 plants and `router.PLANT_THEN_WATER` chained a WATER onto each. The melon arm's
        # 8 melon squatting to d22 is the same counter, other crop.
        state["planted"].clear()
        state["planted"].update(planted_before)

        farmer, hands, market = opening[step]
        me_ = int(obs.get("player", me) or 0)
        farms_ = obs.get("farms") or []
        # Truncated to the hands this farm owns: the reference ignores a surplus unit action for
        # movement and work but still COUNTS it in the atomic-PLANT rule, so sending more than we
        # own blocks plants no real agent could block.
        owned = len((farms_[me_] if len(farms_) > me_ else {}).get("hands") or [])
        priv_ = obs.get("private") or {}
        shed_ = collections.Counter(priv_.get("shed") or {})
        invs_ = priv_.get("inventories") or []

        # **The COUNT and the TURN stay the tape's; only the species is ours.** COW and SHEEP both
        # live on a PASTURE (`routines.ANIMALS`), so re-labelling a head moves no pen, no walk and no
        # route stop -- the board shape the whole replay depends on is untouched. What does move is
        # the bill, $400 against $500, so a swap can be refused on a thin bank like any other order.
        #
        # This is NOT the earlier "keep our own buys" experiment, which measured -$35,022 by sending
        # his hands to water tiles our purchases never created. Here every purchase he makes is still
        # made, on his turn, in his quantity.
        split = state.get("herd_split") or {}
        acts = [list(farmer)] + [list(h) for h in hands[:owned]]
        for i, a in enumerate(acts):
            if len(a) < 2 or a[1] not in _PASTURE:
                continue
            if a[0] == "PICKUP":
                # Take what the shed actually holds. The purchase this pickup was written for may
                # have been re-labelled, or refused on the extra $100 a swap costs.
                if not shed_[a[1]]:
                    alt = next((s for s in _PASTURE if s != a[1] and shed_[s]), None)
                    if alt:
                        a[1] = alt
                shed_[a[1]] -= 1
            elif a[0] == "PLACE":
                # Place what the unit is CARRYING. The PICKUP happened turns earlier and already
                # settled the species, so the inventory answers it and no ledger is needed.
                held = collections.Counter(invs_[i] if i < len(invs_) else {})
                if not held[a[1]]:
                    alt = next((s for s in _PASTURE if s != a[1] and held[s]), None)
                    if alt:
                        a[1] = alt

        # **The rest of the market is the tape's, sells included.** Keeping our own sell cadence
        # while replaying his unit actions is the pairing that broke: his hands harvest into a book
        # our own offers had already walked down.
        orders = []
        for o in market:
            o = list(o)
            # **His seed COUNT is sized for his season, not ours, and the surplus is never sown.**
            # He buys `BUY_SEED STRAWBERRY 23` at d11 h0 for a 42-tile season;
            # `STRAWBERRY_TILES_BY_DRAIN` holds us to 37, so five of them sit in the shed from d12 to
            # the final bell -- $500 at `R.SEED_COST`, dead for eighteen days. `emit_seed`'s own cap
            # cannot reach it and measured byte-identical trying, because on a replayed turn our
            # market orders are discarded and his are sent. So the trim belongs here.
            #
            # Same rule as the `BUY_ANIMAL` re-label below, one field over: the TURN stays his, and
            # what we own is the count rather than the species. No unit action, tile or route stop
            # moves -- only how much seed is bought.
            #
            # **Ceiling is the table's MAXIMUM, never the day's own drain count.** Shops unlock on
            # 3,6,9,12, so d11 sees three draws where the cap is decided on four: pricing this off
            # d11 would buy for a cap of 36 against d12's 37 and cost a whole TILE to save a seed.
            # Buying to the season's best case can only ever leave a spare, and `test_the_strawberry_
            # still_all_goes_in` is what holds that line.
            #
            # **Every crop, not just strawberry.** The same order block carries his wheat and carrot,
            # sized for his season, and the q4 arms close holding 11 and 8 WHEAT. The general bound is
            # what the season has left to PLANT -- plantings, not tiles, since a one-shot crop re-sows
            # the same ground many times over -- less what is already in the shed.
            # **THREE-QUADRANT BOARDS ONLY, and that is measured.** `_season` is read off `sched`, and
            # on a four-quadrant board `q4_branch` installs its extra planting rows AFTER this turn, so
            # the total is short at d11 and the trim UNDER-buys. The tell is that the plantings move
            # rather than just the shed: measured 2026-08-19,
            #
            #     arm        shipped    trimmed    delta   plants
            #     straw_q3   159,623    160,183     +560   identical
            #     melon_q3   145,068    145,068        0   identical
            #     q4_straw    78,305     78,325      +20   identical
            #     q4_melon    93,929     85,347   -8,582   WHEAT 133->126, CARROT 7->6
            #
            # Trading -$8,582 for the $170 of seed those arms leave is not a trade, so they keep the
            # tape's counts until the season total can be known before the opening ends.
            # **The MELON arm only, and the strawberry exclusion is measured, not cautious.**
            # Trimming his seed order leaves us richer than he was on the same turn, and on a
            # replayed day that surplus is not neutral -- `_do_hire` fails SILENTLY on a thin bank
            # (`reference/kaggriculture.py:691`) and the cost is `mult * fib(hires_today)`. So a
            # saving of $60 buys a hand HE COULD NOT AFFORD, and one extra hand for the rest of the
            # season is not a rounding error.
            #
            # Measured 2026-08-21, seed 7 against `kawashigi_b3`'s seat 1, d0-d9 field by field:
            #
            #     d6   money +60  buy_seed -3        the trim
            #     d8   hands +1  hire +1  plant +2  water +1  harvest +1  ...  9 cells
            #          our hands 11, tape 10 -- his 11th hire was refused, ours cleared
            #
            # Seed 899's town is richer, its 11th hire clears too, and that season stays exact. That
            # is the whole 130-vs-60 split the strawberry arm showed: not the herd, not the tape,
            # just whether his d8 hire happened to be affordable on that town.
            #
            # `scripts/seed_tape_grid.py --vs-all --live-shops --opponent kawashigi_b3`, 16 towns,
            # d0-d29, differing cells against the strawberry tape:
            #
            #     with the trim      10 seeds 130-132,  5 seeds 60-62,  1 seed 40
            #     without it          5 seeds  0,      10 seeds    25,  1 seed 40
            #
            # And it is kept on the melon arm because there it is the entire margin: seed 11,
            # `--replay-days 30`, with the trim ends **+$240** on the leader and without it ends
            # level at 0 cells on all 30 days. He wastes that seed; we should not copy the waste.
            #
            # Per-arm PLAN CONTENT, not a flag -- the same distinction `WHEAT_TILES_TO_CARROT`'s
            # tomato tile draws, and for the same reason: the arms already run different schedules
            # and different route tables, and this is part of one arm's plan.
            if (len(o) > 2 and o[0] == "BUY_SEED" and o[1] in R.CROPS
                    and not state.get(_Q4.BRANCH.armed_key)
                    and not state.get(_MB.BRANCH.armed_key)):
                _crop = o[1]
                _held = int((priv_.get("seeds") or {}).get(_crop, 0) or 0)
                _season = sum(collections.Counter(_r.get("plants") or [])[_crop]
                              for _r in sched.values())
                _room = max(0, _season - state["planted"][_crop] - _held)
                # Strawberry is additionally held to the tile cap, which is a SEASON total and so
                # bounds plantings directly -- the crop is ongoing, so a tile is sown once.
                if _crop == "STRAWBERRY":
                    _tiles = (farms_[me_] if len(farms_) > me_ else {}).get("tiles") or []
                    _standing = sum(1 for _r in _tiles for _c in _r
                                    if isinstance(_c, dict) and _c.get("crop") == _crop)
                    _room = min(_room, max(0, max(STRAWBERRY_TILES_BY_DRAIN) - _standing - _held))
                o[2] = min(int(o[2]), _room)
                if o[2] <= 0:
                    continue
            if split and len(o) > 2 and o[0] == "BUY_ANIMAL" and o[1] in _PASTURE:
                # One head at a time against the target, so a row of two cows can come back split.
                for _ in range(int(o[2])):
                    a = o[1]
                    if state["bought"][a] >= int(split.get(a, 0)):
                        alt = next(s for s in _PASTURE if s != a)
                        if state["bought"][alt] < int(split.get(alt, 0)):
                            a = alt
                    state["bought"][a] += 1
                    if orders and orders[-1][0] == "BUY_ANIMAL" and orders[-1][1] == a:
                        orders[-1][2] += 1
                    else:
                        orders.append(["BUY_ANIMAL", a, 1])
                continue
            orders.append(o)

        # **Credit the tape's PLANTs, the same way the planner credits its own.** `:2374` increments
        # on EMISSION, not on the crop appearing, so this matches the convention exactly -- a plant
        # the board refuses is counted by both, and `_refresh_pins` re-derives from the live board
        # anyway. Counted off `acts`, which is the truncated list actually sent, so a hand action the
        # reference drops for want of a unit is not credited either.
        for a in acts:
            if a and a[0] == "PLANT" and len(a) > 1:
                state["planted"][a[1]] += 1

        return {"farmer": acts[0], "hands": acts[1:], "market": orders}

    return replayed
