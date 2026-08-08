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

from . import cover as DP
from . import router as RT

#: Solve the day as a COVERING problem -- cover every job the board offers -- instead of as a prize
#: auction. See `kagg/search/cover.py` for the argument; the short version is that we know the board
#: in advance, we know every job it will want, and Seb's tape proves a day of it is coverable, so
#: "which job is worth most" is a question the day does not actually pose.
#:
#: `router.build_nodes` still decides WHICH jobs exist -- that half is derived from the reference's
#: own mechanics and is worth keeping. What is dropped is `prize`, `MANDATORY` and `CRITICAL`: the
#: ranking, which is the half that measured wrong (-$34,816 over 12 seasons when a local search got
#: BETTER at it, `data/logs/planner_ab3.log`).
#:
#: Off restores `router.plan_routes` exactly.
COVER_PLANNER = True


#: Also treat a tile ONE dry day from becoming a WEED as at-risk, the way a pen one day from losing
#: its animal already is.
#:
#: It is the same rule twice. `consecutive_unfed >= 2` deletes the animal (`kaggriculture.py:786`)
#: and `consecutive_unwatered >= 2` turns the tile into a WEED (line 753); in both cases missing ONE
#: day is free and missing the second is total. Measured on seed 11 with weeds switched OFF -- so
#: every WEED on the board is a crop we let die of thirst, not a spawn -- ours finished with 7
#: against the tape's 0.
#:
#: **This is NOT the arm that measured -$2,804.** That one promoted every thirsty tile into the same
#: mandatory pass as fourteen pens, and the note on it says exactly why it failed: "a pass holding
#: fourteen pens AND every thirsty tile cannot triage". Here the animals keep their own pass and run
#: first; thirsty tiles get a second one, ahead of ordinary work but behind every pen.
#:
#: **ON. The season-total A/B said otherwise and it was the wrong instrument -- see below.**
#:
#: Days 16-18 in isolation, seed 11, with WHEAT and FERTILIZER stocked so supply cannot be the
#: constraint (`data/logs/d16_18_water_ab.log`). This asks only what DIED:
#:
#:     arm                     animals lost    tiles WEEDED
#:     WATER_AT_RISK off                  0               4
#:     WATER_AT_RISK on                   0               2
#:     Seb, same three days               0               1
#:
#: Day 16 alone goes 3 weeded to 0. And the capacity was never the issue: that day had 17 tiles that
#: HAD to be watered, we landed 26 waters, and three of the seventeen still died. We had the turns
#: and watered the wrong tiles, which is exactly what this flag orders.
#:
#: The earlier season-total 2x2 below reported the opposite. It is kept because the numbers are real,
#: but it cannot answer this question: a 30-day WEED count folds in every tile the SCHEDULE lets get
#: thirsty in the first place, and those swamp the handful this ordering decides. A three-day window
#: with supply held constant isolates the ordering; a season total measures the schedule.
#:
#: **The residual gap to the tape is upstream of here and is a cadence.** Arriving at day 16 he has
#: EIGHT tiles that must be watered; we have seventeen. He waters on alternate days and never builds
#: the debt, so he is never rescuing. He is not better at rescuing -- he never gets into the position.
#:
#: SUPERSEDED MEASUREMENT, kept so it is not re-run: six seeds, seat 0, weeds off, 2x2 against
#: `FEED_DAYS` (`data/logs/feed_x_risk.log`) -- WEED tiles at season end:
#:
#:     FEED_DAYS   water at-risk    mean $    escapes    WEEDS
#:             2            off    96,055          3       47
#:             2             on    96,302          4       58
#:             4            off    94,986          0       53
#:             4             on    98,382          0       58
#:
#: More weeds on BOTH rows. The money edge on the last row is ~3% on six samples, inside this
#: project's ~15% seed variance, and does not get to override a count moving the wrong way.
#:
#: **And the mechanism explains it.** `router.crop_ops` offers survival water ONLY at
#: `consecutive_unwatered >= 1`, so this arm can only ever RESCUE and never PREVENT -- and a rescue
#: competes for turns at the worst possible moment, displacing the ordinary waters that would have
#: stopped the next tile getting thirsty at all. The tape does not rescue because it never needs to:
#: it waters on a fixed alternate-day cadence (d0 17, d1 0, d2 17, d3 14) that holds every tile at 0
#: or 1 and takes zero weeds through day 7.
#:
#: So the real REMAINING fix for watering is a CADENCE in the schedule, upstream of this file. This
#: flag closes the half that is reachable from the day planner.
WATER_AT_RISK = True

#: Whether the final turn of a day is budgeted as workable. See the note in `_router_acts`.
#: Off restores `TPD - hour - 1`, which silently discarded one turn per hand per day -- 13 hands over
#: 29 days is ~377 unit-turns a season, and every tour that ended on a tile still holding produce lost
#: its HARVEST to it.
LAST_TURN_IS_WORKABLE = True

#: Turns remaining at or below which the walk back to the shed stops being charged. See `_solve`.
DELIVER_CUTOFF_TURNS = 2


def _at_risk_tiles(tiles):
    """Tiles where skipping today's work destroys something tonight. Read off the board, not priced.

    `consecutive_unfed`/`consecutive_unwatered` are already 1 -- one more missed day and the animal
    walks off or the tile weeds. A pen fed yesterday, or a tile watered yesterday, can slip a day for
    free, which is precisely how the tape feeds 16 of 19 pens on day 19 and loses nothing.
    """
    out = set()
    for y, row in enumerate(tiles):
        for x, cell in enumerate(row):
            if not isinstance(cell, dict):
                continue
            if cell.get("animal") and cell.get("consecutive_unfed", 0) >= 1:
                out.add((x, y))
            elif (WATER_AT_RISK and cell.get("kind") == "PLANT"
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

#: Do not clear a weed on ground we are never going to replant.
#:
#: `DIG` costs a turn and buys nothing unless something goes into the hole. The register records the
#: final board as ours WEED=8 empty=72 against his WEED=42 empty=37 -- he leaves them, and the 35
#: unit-turns we spend clearing ours are pure loss once the schedule has no plantings left.
DIG_ONLY_IF_REPLANTING = True

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
                if DIG_ONLY_IF_REPLANTING and not plants_left:
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


#: Minimum units of the day's still-owed SELL row a hand must hold before a DELIVER stop is planned.
#:
#: **The planner had no delivery job at all, and that is what the day-6 cash hole is.** Seed 11, day
#: 6, schedule row `WOOL: 12` (`data/logs/d6_wool.log`). The tape harvests at h0, drops and sells 6
#: at h2, harvests again at h2, drops and sells the last 6 at h5 -- twelve wool banked by hour five,
#: which funds two cows at h2. We harvest at h4 and h10, and then the crew CARRIES ten wool through
#: h11, 12, 13, 14, 15, 16, 17 and 18, drops four at h19 and takes six into the night. The bank sits
#: at $20 all day, the second cow is deferred, and `buy_product` is suppressed for days after.
#:
#: `DELIVER_FERRY` was supposed to cover this and cannot: it only fires when a hand is ALREADY
#: walking and has slack (`act[0] in STEP`), so a hand working through its tour never diverts however
#: much it is carrying. Delivery was opportunistic; it has to be scheduled. Lowering
#: `MIN_SELL_ROW_DROP` does not help and measured worse -- that constant gates the ferry, which is
#: the wrong mechanism, not a mis-tuned one.
#:
#: **SET AT 6 BY MEASUREMENT, NOT BY TASTE.** A delivery stop costs turns, and at 2 or 4 it takes
#: them out of day 6's planting: `test_day_six_plants_every_tile_the_row_asks_for` and
#: `test_the_biggest_sale_takes_the_earliest_slot` both go red. At 6 the suite is back to its two
#: pre-existing failures and day 6 still orders BOTH cows the schedule asks for, against one before.
#: So this catches the big loads and leaves the small ones to the opportunistic ferry.
#:
#:     DELIVER_MIN   router failures   d6 cows ordered
#:     none                        2                 1
#:     2 and 4                     5                 2
#:     6 and 8                     2                 2
#:
#: What it does NOT fix: we harvest the sheep at h7 and h10 where the tape harvests at h0 and h2, so
#: the first delivery still lands at h15 against his h2. Delivery cannot precede harvest, and the
#: covering planner has no reason to take a HARVEST early just because the SELL row wants it today.
#: That is the next defect and it is a scheduling question, not a delivery one.
DELIVER_MIN = 6


#: Days on which a hand CARRYING sellable goods is replanned even though it is still busy.
#:
#: **A HARD-CODED DAY, and it is a placeholder for a condition we have not found.** Alex's call, to
#: unblock: the mechanism below is real and general, the trigger is not yet known, and guessing at it
#: has already cost two wrong theories today (see `FUND_THE_DAY`, reverted, and the cash-shortfall
#: flag in `data/logs/cash_trigger.log` which fires on four days the tape does nothing special on).
#:
#: THE MECHANISM, which is not a guess. `_deliver_jobs` pins a delivery to the hand holding the goods
#: -- only that hand can carry them -- but the mid-day top-up replans only IDLE units. So the job is
#: offered on every replan to units that cannot possibly do it, and refused on every replan, until the
#: carrier finally runs out of tour. Measured on seed 11 day 6 (`data/logs/d6_wool.log`): planner runs
#: at h12, h16, h17 and h18 each offering a deliver job, all of them refused, while a hand sits on ten
#: wool from h11; it delivers four at h19 and takes six into the night. The bank is on $20 all day and
#: the wool is worth ~$220 a unit.
#:
#: The cost of relaxing this generally is known and is why it is gated: replanning a BUSY unit throws
#: away a tour it is part-way through, which is the thrash this file's `URGENT_OPS` was disabled for.
#: Widening it to every day, or replacing the day list with a real condition, must be measured on the
#: day-by-day cells and not on a season total.
DELIVER_REPLAN_DAYS = (6,)


def _deliver_jobs(units, invs, owed_sale, depots, unlocked):
    """A shed stop for every hand holding goods today's SELL row still wants. One per hand.

    Pinned to that hand with `Job.only` -- the wool is in ITS pocket, so no other unit can take it --
    and placed on the depot nearest to where it currently stands. `DROP` is all-or-nothing per item
    and empties the hand, so one stop clears whatever it is carrying.
    """
    out = []
    for u in range(len(units)):
        inv = invs[u] if u < len(invs) else {}
        carrying = sum(min(int(q), int(owed_sale.get(it, 0)))
                       for it, q in (inv or {}).items()
                       if int(q) > 0 and int(owed_sale.get(it, 0)) > 0)
        if carrying < DELIVER_MIN:
            continue
        home = min(depots, key=lambda c: (RT.dist(c, units[u]), c))
        out.append(DP.Job(home, [("DROP", None)], needs={}, only=u))
    return out


def _solve(units, nodes, budget, depots, carry, supply, at_risk=(), pointless=(), deliver_jobs=()):
    """One day's assignment, by whichever planner is switched on. Same return shape either way."""
    if not COVER_PLANNER:
        return RT.plan_routes(units, nodes, budget, depots, carry, supply=supply)
    jobs = [j for j in DP.from_nodes(nodes) if j.tile not in pointless]
    jobs.extend(deliver_jobs)
    if at_risk:
        for j in jobs:
            if j.tile in at_risk:
                j.at_risk = True
    # The walk home is charged only while there is time to make it. With two turns or fewer left a
    # hand cannot both work and get back, and the overnight drop banks the produce anyway -- so
    # reserving it there only refuses the last harvest of the day. See `cover.turns`.
    deliver = max(budget or [0]) > DELIVER_CUTOFF_TURNS
    out, _uncovered = DP.plan(units, jobs, budget, depots, carry, supply=supply, deliver=deliver)
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
#: across the season to our 405. At `FEED_DAYS = 2` our buffer was effectively ONE day: we bought
#: about seventeen and fed about seventeen, so any hiccup was a missed feed.
#:
#: `FEED_DAYS = 1` was tried in the other direction and measured -$6,236 over twelve seeds, which is
#: presumably why this sat at 2; nothing had ever tried going UP.
FEED_DAYS = 2

#: Days of feed held once the season turns TURN-BOUND. See `feed_days()`.
FEED_DAYS_LATE = 4

#: The day the buffer widens. This is the same hinge the register records for the whole season: up to
#: about here the farm is CASH-bound (dawn bank $28 on day 4, $15 on day 6, land parcels to fund) and
#: after it the farm is TURN-bound, with the bank past $10k and nothing to spend it on but feed.
FEED_DAYS_FROM_DAY = 16


def feed_days(day):
    """Days of wheat to hold, as a function of the day. Two early, four late.

    **A flat 4 measured better on escapes and worse on everything else, and both halves were real.**
    Six seeds, seat 0 (`data/logs/feed_days_sweep.log`): escapes 4 -> 0 going from 2 to 4, which is
    what a nineteen-animal herd needs. But the escapes all happen after day 16, and buying four days
    of feed for FOUR animals on day 4 spends a bank that reads $28 at dawn. `test_router.py` caught
    exactly that -- `PLACE 0/1`, `melon seed 5 of 6` with "the livestock spent the bank first",
    `WHEAT sold 13 against 17` -- because early feed money is land and seed money.

    The herd is 4-7 animals before day 8 and 19 after day 15, so the buffer follows it.
    """
    return FEED_DAYS_LATE if day >= FEED_DAYS_FROM_DAY else FEED_DAYS

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

#: Floor for the opportunistic mid-tour drop below. A unit standing at a depot mid-tour re-checks this
#: every time it is about to walk away, and pens sit ON depot tiles, so with no floor a unit banking
#: one or two units at a time turns every such moment into a 1-turn DROP.
MIN_OPPORTUNISTIC_DROP = 4

#: Whether the opportunistic mid-tour DROP below runs at all. A flag rather than an edit because it
#: was measured on final bank (-$8,292 over twelve seeds) and re-applied here without being measured
#: again on the day-by-day trace -- so it must be switchable to be attributable.
OPPORTUNISTIC_DROP = True

#: Whether a unit standing at a depot delivers a load containing product today's SELL row still owes,
#: ignoring the `own_route_needs_it` and `MIN_OPPORTUNISTIC_DROP` gates. A flag because the broad
#: version of this ("drop any surplus at any shed visit") measured -$15,272 over twelve seeds, and the
#: narrowing is the whole claim -- so it has to be switchable to stay attributable.
#:
#: **ON.** Measured on Seb's tape, seed 11, weeds off, at `MIN_SELL_ROW_DROP = 6`:
#:
#:     day 9 SELL units      10/22  ->  16/22      closer
#:     day 10 dawn bank    1552/3104 -> 2509/3104  +$957
#:     day-by-day cells, d0-d9        identical
#:     day-by-day cells, season  531  ->  540      9 WORSE, first regression on d10
#:
#: It was nearly left OFF on the cell count. The argument for ON, which is Fable's and is right:
#: **day 10's OFF-match is two errors cancelling.** OFF, day 9 ships 10 of 22 and leaves 12 units of
#: backlog, which `CUMULATIVE_SELLS` re-offers, so day 10 offers 23 + 12 = 35 and coincidentally
#: equals his 35. ON, day 9 ships 16, leaves 6, and day 10 offers 29. The match was the backlog, not
#: the behaviour, and it dissolves the moment any earlier day is fixed -- d0-d8 still carry 4 to 15
#: cells each. Suppressing the tape's own verified mechanism to preserve an accidental match is
#: optimising the proxy. The earliest day the two configurations differ in substance is day 9, and
#: there ON is strictly closer on both measures the cell counter is too coarse to score: `sell` is
#: one differing cell whether we ship 10 or 16.
#:
#: Day 9 `work` also goes 89/91 -> 91/91, exact.
#:
#: What this does NOT fix: day 10 idle is 72 without it and 73 with it. That is a separate defect.
DELIVER_THE_SELL_ROW = True

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

#: **A late-delivery exemption to this floor was built, measured, and REVERTED. Do not rebuild it.**
#:
#: The diagnosis behind it is correct and still stands. Day 6, seed 11: the row asks
#: `{WOOL: 12, FERTILIZER: 7}`, `collect_fertilizer` is 7/7 so we gather everything the tape does,
#: and both sides sell all 12 wool. The fertilizer splits:
#:
#:     ours  1@90 h8, 2@90 h13, 1@90 h14, 1@89 h15                  = 5 of 7, last sale h15
#:     tape  1 h2, 1 h5, 1@90 h18, 1@90 h20, 2@89 h21, 1@89 h22     = 7 of 7
#:
#: $627 to our $449, which is the bulk of day 7's dawn gap of -$137, and the two we never shipped are
#: exactly the `sh:ferti 2/0` in that dawn's shed. Same signature at day 8's dawn and at day 11's
#: (`sh:melon 18/0`, against a day-10 row asking for exactly 18 melons of which we sold none). It is
#: a TIME-OF-DAY problem, not a load-size one, which is why neither `DELIVER_THE_SELL_ROW` nor the
#: deliver ferry reaches it: both wait for a six-unit load that never forms.
#:
#: The fix -- drop the census to 1 from hour H, and let the ferry skip its slack test after H, since
#: in the evening the tour is not resumed and slack is near zero by construction -- turned
#: `test_the_afternoons_collections_reach_the_shed_before_the_market_closes` green and made the
#: day-matching WORSE. Swept on H against the 120-cell steal-gate baseline:
#:
#:               d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 d10 d11  total
#:     OFF        7  6  4  7  7  7 11  8 11 14  19  19   120
#:     from h16   7  6  4  7  9  8 14 12 10 12  17  20   126
#:     from h18   7  6  4  7  7  7 12 11 11 13  17  20   122
#:     from h19   7  6  4  7  7  7 11  9 11 14  19  18   120
#:     from h20   7  6  4  7  7  7 11  8 11 14  19  19   120   byte-identical to OFF
#:     from h21   (identical to OFF)
#:     from h22   (identical to OFF)
#:
#: h20 and later are INERT -- nothing is left to divert that late, so they are OFF with extra code.
#: h19 ties on total and is disqualified in order: it pays d7 8 -> 9 to buy d11 19 -> 18. h16 and h18
#: are simply worse, and the shape says why -- d4, d5 and d6 all regress at h16, because pulling a
#: hand off work to walk home costs more than the goods. A melon WATER is worth ~$250; the fertilizer
#: being rescued is $90.
#:
#: So the two stranded fertilizer are real and the delivery rule is not how to get them. The unit
#: should not have been holding them at h13 in the first place -- u2 carries 1 from h13 to h23, does
#: no work at all after h14, and walks PAST the depot at (4,3) at h18. That is a ROUTING failure, not
#: a delivery-threshold one, and it is where the next attempt belongs.
#: **Send a carrier home mid-tour, then resume it.** `DELIVER_THE_SELL_ROW` can only fire on a depot
#: cell, so it waits for an incidental visit -- which is the 16-of-22 ceiling on day 9 and the 12
#: melons still in two hands at hour 23 of day 10 (`docs/idle_at_h10_2026-08-07.md` 2e). A rule that
#: only fires AT the shed cannot send a unit there.
#:
#: This is the mirror of the draw ferry below: preempt the tour, walk home, act, resume. It replaces
#: a MOVE with a different MOVE, so it can never delete a work op on the turn it fires, and it needs
#: no new drop code -- on arrival `DELIVER_THE_SELL_ROW` fires as it stands.
#:
#: **The test is SLACK against the detour, never the load's value against the route's.** The route is
#: resumed, not abandoned, so the two are never traded off. Where the slack genuinely is not there
#: the answer is "keep the route": an abandoned FEED can cost an animal outright, while a load that
#: sells tomorrow instead of today gives up roughly a tenth of its price.
#:
#: Deliberately NOT in `build_nodes`. Fable's second review (`docs/fable_delivery_node_2026-08-07.md`)
#: withdrew the delivery-node proposal on measurement: priced honestly a delivery node's prize is
#: gating value, which is not computable at plan time, so it inserts last and is always refused;
#: made mandatory it is placed first unconditionally and re-permutes every yielding tour's spine.
#: Either way it pays the d2 permutation tax (see `router.py`) on days that are currently exact.
#:
#: **ON, but measured as very nearly inert, and the census below is why.** Seed 11, weeds off, d0-d11:
#:
#:     day-by-day cells   d9 15 -> 14, every other day byte-identical.  No regression.
#:     sellables in hands at hour 23   IDENTICAL on all twelve days (d10 stays 14, d11 stays 20)
#:
#: So it does NOT fix the defect it was built for. Gate census over the 818 off-depot unit-turns that
#: were holding a sellable (`scratchpad/ferry_gates.py`, `data/logs/ferry_gates.log`):
#:
#:      304  37.2%   today's row still owes only 1 of the load
#:      182  22.2%   ... owes 0
#:      174  21.3%   no committed route -- the return leg already covers these
#:       57   7.0%   no slack
#:      100  12.2%   ... owes 2 to 5
#:        1   0.1%   FIRES
#:
#: The binding constraint is the CENSUS, not the slack: `owed_sale` is the row minus what the shed
#: already holds, so by mid-morning the row rarely still owes six units of precisely what one unit
#: happens to carry. The 12 melons stranded in hands on day 10 are not owed by the row at all -- that
#: day's `sell` is 35/35, exact. They are surplus the row never names, which is a DIFFERENT and much
#: riskier change (the broad version of it measured -$15,272 over twelve seeds).
#:
#: Kept ON because it is a strict in-order improvement with nothing regressed, and because it is the
#: right structure for that change if the census is ever relaxed. It is NOT load-bearing today.
#: **TURNED OFF 2026-08-07.** Costs 4 cells (115 -> 119) for something already documented above as
#: near-inert: it fires once in 818 candidate unit-turns and hands-at-dusk are identical ON vs OFF.
DELIVER_FERRY = False

#: Turns of slack held back before the ferry will divert. It exists because `Node.service` is
#: `len(ops)` fixed at plan time and the executor re-derives ops on arrival, so a tour's remaining
#: cost is under-stated by ~27% on field tiles (`docs/service_undercount_2026-08-07.md`). A flat
#: reserve rather than a multiplier, because the under-count is a property of the board's live state
#: and not of the tour's length.
DELIVER_FERRY_MARGIN = 3

#: Diagnostic sink for the opportunistic drop. `None` ships. Set it to a list and every unit-turn
#: spent standing on a depot holding something appends one `(act, gate)` pair naming the FIRST gate
#: that refused, or `"fires"`. It exists because lowering `MIN_OPPORTUNISTIC_DROP` to 3 and to 2
#: measured byte-identical to 4 while `scripts/depot_chances.py` showed the chances arriving as often
#: as the tape's -- so the threshold is not the gate, and guessing which one is has already cost a
#: day elsewhere in this file.
DROP_TRACE = None


def _trace_drop(sink, act, st, inv, shed, carried, tiles):
    """Name the first gate that refuses this drop. Pure observation; changes nothing."""
    if not OPPORTUNISTIC_DROP:
        gate = "flag off"
    elif act[0] not in STEP:
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
PEN_SPOTS = ()

#: **Site a pen at the free tile NEAREST a depot, across every quadrant we own.**
#:
#: The measurement above is sound and its conclusion does not generalise, because day 0 is the one day
#: on which the two layouts are distance-identical -- 22 either way, and 23 either way on day 6. The
#: gap opens when the later quadrants unlock. At day 11's dawn:
#:
#:     ours  dist sum 51, 15 pens, including (5,0), (8,0), (9,0) -- 22 of the 51 in three pens
#:     his   dist sum 44, 15 pens, furthest (8,4) at 4; the rest go SOUTH into SW at
#:           (1,6), (2,5), (2,6), (4,6), (4,7), every one within 5
#:
#: `field_order` is near-first WITHIN a quadrant -- a boustrophedon sweep anchored at that quadrant's
#: shed corner -- but it is quadrant-MAJOR, and pens draw from the same sweep as crops. By day 10 the
#: near tiles of NE are planted, so a new pen falls to the tail of NE at y=0, nine steps out, while
#: SW's near band sits empty. A pen is a permanent daily FEED + CARE + COLLECT, so that distance is
#: paid ~20 times a season; a crop tile is watered once a day and harvested once.
#:
#: **OFF. It does exactly what it says and the cell metric punishes it.** Measured, seed 11, weeds off:
#:
#:                 d0 d1 d2 d3 d4  d5 d6 d7 d8 d9 d10 d11  total
#:     baseline     7  6  4  7  7   7 11 15 13 14  19  20   130
#:     nearest      8  7  7  7  9  10 11 15 12 17  18  22   143
#:
#: The geometry lands -- `test_a_pen_is_not_built_on_the_far_edge_while_near_ground_is_free` goes
#: GREEN with this on, no pen beyond 5 steps at day 11 -- and d0, d1, d2, d4 and d5 all go backwards.
#:
#: The reason is worth stating, because it is a property of the METRIC and not of the change. We are
#: scored on resembling Seb. His day-0 block sums to 22 from the depot; nearest-first sums to **14**.
#: That is less walking every day for twenty days and it reads as a REGRESSION, because it is further
#: from him. Any real improvement he did not himself make will score the same way.
#:
#: So this is the first arm in the project that is plausibly right and is refused by the objective
#: rather than by the board. It should be re-measured on BANK, head to head, before it is written off.
PEN_NEAREST_DEPOT = False

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

#: Whether an order that does not fit the turn is UN-COUNTED, so it is retried, instead of being
#: silently deleted while its bookkeeping stands.
#:
#: We appended freely and truncated at the end, so from day 11 every turn built 13-15 orders:
#:
#:     d11  n=14  {HIRE: 12, SELL: 2}      d13  n=15  {HIRE: 12, SELL: 3}
#:     d12  n=14  {HIRE: 12, SELL: 2}      d14  n=13  {HIRE: 12, SELL: 1}
#:
#: Ten survived. The 2-5 lost HIREs still incremented `state["hired"]`, and every BUY_ANIMAL -- which
#: the animal block appends LAST -- was deleted outright while `state["bought"]` and the bank were
#: both charged for it. Both counters then read as satisfied, so neither was ever retried. The
#: animal block's own comment is careful that "a failed order does not increment it (the `money >=`
#: test guards that)"; truncation is a second way to fail that the guard cannot see.
#:
#: Measured on Seb's tape, seed 11: the schedule buys nine SHEEP across days 9-14 and we sent the env
#: ZERO, herd stuck at the 2 we started with while nine pens stood empty and wheat we would have
#: converted to wool piled to 63 units against his flat 19. Hires ran 2-6 short of his from day 10,
#: which is the 23%-smaller crew and the late-season idle.
#:
#: HIRE is what spills, because deferring one inside a day is free -- `hires_today` is a per-DAY
#: fibonacci counter, so 5+1+1 costs exactly the $33 that 7-at-once costs (measured, day 3). A
#: deferred PLACE loses the day's feed and care with it, so the animal keeps the slot.
FIT_ORDER_SLOTS = True


#: Whether the turn's SELLs are ranked biggest-first among themselves before they are sent.
#:
#: `_process_market` walks slot `i` across BOTH players, so a sale in slot 1 trades only after every
#: slot-0 sale has walked the book down -- the opponent's included. Which of our own sells goes first
#: is therefore priced whenever the opponent is selling the same product, and we were emitting them
#: in product-loop order, which is arbitrary with respect to size.
#:
#: Measured on Seb's tape, seed 11, day 5 hour 0 -- identical goods, identical eight hires:
#:
#:     ours  [SELL FERTILIZER 2, SELL WHEAT 17, 8x HIRE]   316 -> 925   (+663 net of $54 of hires)
#:     tape  [SELL WHEAT 17, SELL FERTILIZER 2, 8x HIRE]   320 -> 965   (+699)
#:
#: $36 for putting a 2-unit sale ahead of a 17-unit one, and that is the entire day-6 dawn gap.
#: Ranking is by `n * BASE_PRICE`, not by the live quote: the bases are what the router already plans
#: against precisely because the ORDER they induce is stable while the quotes move.
SELL_BIGGEST_FIRST = True


def _order_sells(orders):
    """The same orders, with the SELLs ranked biggest-first among the slots they already occupy."""
    if not SELL_BIGGEST_FIRST:
        return orders
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


def _fit_slots(orders, state):
    """The turn's orders, cut to what the env will actually accept, with the losers un-counted."""
    if not FIT_ORDER_SLOTS:
        return orders[:ORDER_SLOTS]
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
HIRE_PINNED_DAYS = frozenset({4})

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

#: How far ahead the sell loop looks when deciding what stock is SURPLUS. `None` = the whole rest of
#: the season, which is the conservative reading: only stock that no remaining row will EVER name is
#: released early. A small integer treats stock as surplus unless the next N days ask for it, which
#: releases far more, far sooner.
#:
#: **Why the conservative setting is the shipped one.** See the block above the sell loop for the
#: measurement -- we meet every milk row exactly, on the day, all season, and still finish day 28
#: holding 67 milk to the tape's 16, because we simply produce more than his rows name. Only the
#: surplus is ours to release; the rest is his plan and it works.
#:
#: **A short horizon was measured and it is much worse.** Swept on the `seb` tape, seed 11, weeds
#: off, 30 days, by `scripts/breakdown.py --diff`. `money` is the season SUM of the daily
#: ours-minus-tape gap, `d29` that gap on the last day alone, `cells` the independent differing-cell
#: count, and `sh:milk` the summed milk-stock gap:
#:
#:     horizon   money sum      d29   sh:milk   cells   first day it fires   d6-d11 cells
#:     OFF        -107,267   +6,247      +521     384   never (d29 dump)     8 4 7 12 12 13
#:     None (on)   -89,307   +5,533      +446     383   d25                  8 4 7 12 12 13
#:     10         -189,721  -13,414       -82     439   d6                  10 11 9 16 16 20
#:     5          -199,371  -16,928      -109     444   d6                  10 11 9 16 16 20
#:
#: The short horizons fail through the mechanism this file already documents twice. They first fire
#: on day 6, on WOOL, and day 6 goes from $137 behind the tape to $1,430 behind on the day the extra
#: wool clears -- `market_price` falls monotonically in inventory, and wool is the product where that
#: was measured hardest (123 units -> 138 for revenue $29,041 -> $21,811). They also overshoot:
#: `sh:milk` swings from +521 to -109, which is not tracking the tape, it is missing it from the
#: other side. Every day from d6 on has MORE differing cells, so the in-order rule rejects them on
#: their own terms and not on the dollar.
SELL_SURPLUS_HORIZON = None

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

#: Whether the day's outstanding seed bill is reserved before any BUY_ANIMAL is queued. See the
#: block above the hire loop for the day-6 measurement. Off restores livestock-first spending.
SEED_BEFORE_LIVESTOCK = True

#: Whether every purchase below the sell block may be funded by that same turn's sales, as BUY_LAND
#: already is. See the note above the seed bill for the day-6 measurement.
SELLS_FUND_THE_TURN = True

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

#: The products the sell block actually offers, in its long-standing order. Named so the
#: make-room release below can rank the same set by holding size without duplicating the tuple.
SELLABLE = ("MELON", "WOOL", "MILK", "STRAWBERRY", "FERTILIZER", "WHEAT")

#: `shedCapacity`, the ONE limit shared by all nine products (`reference/kaggriculture.py:835`).
SHED_CAPACITY = 100

#: Whether a sale may exceed the schedule's row purely to keep room for tonight's dusk drop.
#:
#: `_drop_inventories_to_shed` empties every hand into the shed at the rollover and DISCARDS whatever
#: does not fit -- `del inv[item]` runs whether or not `take` covered the stack, silently. Measured on
#: Seb's tape, seed 11, weeds off, before this flag: **101 units destroyed across 15 days**, peaking
#: at 22 on day 24.
#:
#: This is deliberately NOT the parked `shed_dusk` arm and must not be merged with it. That one sells
#: down to a target EVERY day and costs $5,471 of final bank (+5,533 -> +62) to tidy a stock curve
#: that was never the problem: every unit of milk is sold in the end, at $243.9 against the tape's
#: $240.0 while moving 30% more volume. Holding stock for a better price is a strategy worth keeping.
#: Losing it off the back of the shed is not. This releases stock ONLY when the shed physically
#: cannot take what the hands are already holding, and only from genuine surplus -- stock no
#: remaining row will ask for -- so the trading behaviour is untouched on every other day.
SELL_TO_MAKE_ROOM = True

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
        spot = next((tuple(c) for c in PEN_SPOTS
                     if tuple(c) not in taken and _owned(tuple(c), unlocked)
                     and tiles[c[1]][c[0]] is None), None)
        spot = spot or next((c for c in R.shed_access_tiles()
                             if _owned(c, unlocked) and tiles[c[1]][c[0]] is None
                             and c not in taken), None)
        if PEN_NEAREST_DEPOT or (PEN_NEAREST_DEPOT_FROM_DAY is not None
                                 and day >= PEN_NEAREST_DEPOT_FROM_DAY):
            spot = spot or _nearest_ground(order, tiles, taken, unlocked)
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
    budget = [max(0, TPD - hour - (0 if LAST_TURN_IS_WORKABLE else 1))] * len(units)
    routes = state["routes"]
    # Only shed cells inside a quadrant we own. A hand wakes on a LOCKED one and a LOCKED tile no-ops
    # before PICKUP is ever reached, so treating all four as depots strands the hand for the whole day.
    depots = tuple(c for c in R.shed_access_tiles() if _owned(c, unlocked)) or (SPAWN,)
    load = {u: collections.Counter(invs[u] if u < len(invs) else {}) for u in range(len(units))}
    # What today's SELL row still owes the shed. The market reads the shed and nothing else, so a
    # product the row wants is worth nothing while it rides in a hand. See `DELIVER_THE_SELL_ROW`.
    owed_sale = collections.Counter({p: int(q) for p, q in (sched.get(day, {}).get("sells") or {}).items()
                                     if int(q) > 0})
    for p, q in shed.items():
        if q > 0:
            owed_sale[p] -= q

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
        sub = _solve([units[u] for u in live], nodes_for(set()),
                     [budget[u] for u in live], depots,
                     {k: load[u] for k, u in enumerate(live)}, supply=shed,
                     at_risk=_at_risk_tiles(tiles),
                     pointless=_pointless_tiles(tiles, day, plants_left),
                     deliver_jobs=_deliver_jobs(units, invs, owed_sale, depots, unlocked))
        state["routes"] = routes = {u: sub[k] for k, u in enumerate(live)}
        state["crew"] = len(live)
    else:
        idle = [u for u in live if not routes.get(u, {}).get("route")]
        # A hand holding goods today's SELL row wants is not idle, but it is the ONLY unit that can
        # deliver them -- and the pinned job is refused on every replan it is absent from. See
        # `DELIVER_REPLAN_DAYS`.
        if day in DELIVER_REPLAN_DAYS:
            carrying = [u for u in live if u not in idle
                        and sum(min(int(q), int(owed_sale.get(it, 0)))
                                for it, q in (invs[u] if u < len(invs) else {}).items()
                                if int(q) > 0 and int(owed_sale.get(it, 0)) > 0) >= DELIVER_MIN]
            idle = idle + [u for u in carrying if u not in idle]
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
            margin = STEAL_MARGIN
            if STEAL_FROM_DAY is not None and day >= STEAL_FROM_DAY:
                margin = STEAL_FROM_DAY_MARGIN
            busy = _claimed_tiles(units, routes, idle, margin)
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
            sub = _solve([units[u] for u in idle], nodes_for(busy),
                         [budget[u] for u in idle], depots,
                         {k: load[u] for k, u in enumerate(idle)}, supply=free,
                         at_risk=_at_risk_tiles(tiles),
                         pointless=_pointless_tiles(tiles, day, plants_left),
                         deliver_jobs=_deliver_jobs(units, invs, owed_sale, depots, unlocked))
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
            # **A DELIVER stop, which `_live_ops` cannot re-derive.** Every other stop's work is read
            # off the CELL, but a delivery is a fact about the unit's pocket, not about the tile, so
            # the depot cell reports nothing and the stop would be popped unworked. See
            # `_deliver_jobs`: this is the scheduled shed trip the tape makes at h2 and h5 and we
            # were only ever stumbling into at h19.
            if pos == node.tile and any(o == "DROP" for o, _i in node.ops):
                st["route"].pop(0)
                if tuple(pos) in set(depots) and any(v > 0 for v in inv.values()):
                    for item, qty in inv.items():
                        if qty > 0:
                            shed[item] = shed.get(item, 0) + qty
                    act = ["DROP"]
                    break
                continue
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

        # ------------------------------------------------------------------ the deliver ferry
        # See `DELIVER_FERRY`. Placed AFTER the tour walk has chosen `act`, so a real op at the tile the
        # unit is standing on always wins, and before the opportunistic drop, which it cannot reach
        # anyway -- that one requires a depot cell and this one only fires off them.
        #
        # `deliverable` is the census `DELIVER_THE_SELL_ROW` uses below, computed here so both share
        # one definition: only what TODAY'S row still owes counts, so a unit ferrying wheat to its own
        # FEED stops is never diverted.
        deliverable = sum(min(q, owed_sale.get(it, 0)) for it, q in inv.items()
                          if q > 0 and owed_sale.get(it, 0) > 0)
        if (DELIVER_FERRY and act[0] in STEP and pos not in depots
                and deliverable >= MIN_SELL_ROW_DROP
                and sum(shed.values()) + sum(inv.values()) <= SHED_CAPACITY):
            home = min(depots, key=lambda c: RT.dist(pos, c))
            nxt = tuple(st["route"][0].tile) if st["route"] else home
            slack = (TPD - hour - (0 if LAST_TURN_IS_WORKABLE else 1)) - _route_turns(pos, st["route"], depots)
            detour = RT.dist(pos, home) + 1 + RT.dist(home, nxt) - RT.dist(pos, nxt)
            if detour <= slack - DELIVER_FERRY_MARGIN:
                m = _step_towards(pos, home, unlocked)
                if m:
                    act = [m]

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
        if DROP_TRACE is not None and pos in depots and any(v > 0 for v in inv.values()):
            _trace_drop(DROP_TRACE, act, st, inv, shed, carried, tiles)
        if (OPPORTUNISTIC_DROP and act[0] in STEP and pos in depots
                and any(v > 0 for v in inv.values())):
            future_needs = collections.Counter()
            for n in st["route"]:
                future_needs.update(n.needs)
            own_route_needs_it = any(future_needs.get(it, 0) > 0 for it, qty in inv.items() if qty > 0)
            alive = sum(1 for r in tiles for c in r if isinstance(c, dict) and "animal" in c)
            farm_wheat = shed.get("WHEAT", 0) + carried.get("WHEAT", 0)
            wheat_ok = (inv.get("WHEAT", 0) == 0
                        or farm_wheat - inv.get("WHEAT", 0) >= feed_days(day) * alive)
            if (not own_route_needs_it and wheat_ok and sum(inv.values()) >= MIN_OPPORTUNISTIC_DROP
                    and sum(shed.values()) + sum(inv.values()) <= SHED_CAPACITY):
                for item, qty in inv.items():
                    if qty > 0:
                        shed[item] = shed.get(item, 0) + qty
                act = ["DROP"]

        # ------------------------------------------------------------------ deliver the day's sell row
        # **The market reads the SHED.** Produce in a hand is worth nothing until it is dropped, and
        # the reference resolves unit actions BEFORE the market phase inside a turn -- so a DROP and
        # the SELL of what that drop just delivered settle together. The tape does exactly this: seed
        # 11 day 9 hour 7 it holds WOOL 8 and orders `SELL WOOL 8` on the same turn.
        #
        # Day 9 is where the season broke. At its dawn we were $76 AHEAD; by day 10's we were $1,552
        # behind, with plant 9/9, water 31/31, harvest 4/4 and hire 11/11 -- only the selling differed,
        # 10 units against the row's 22. Not for want of goods: at h12 the crew held WOOL 8, MILK 6,
        # FERTILIZER 10, WHEAT 6 and the shed read EMPTY, still empty at h23.
        #
        # This is deliberately NARROWER than the arm that was tried and cost $15,272 over twelve seeds
        # ("drop the surplus whenever standing on the shed"). That one dumped ANY load at ANY shed
        # visit, including the feed a unit was carrying for its own stops. This fires only when the
        # load contains a product TODAY'S SELL ROW STILL OWES, so a wheat-only ferry is never touched.
        #
        # `own_route_needs_it` and the `MIN_OPPORTUNISTIC_DROP` floor are both skipped here on purpose.
        # DROP is all-or-nothing (`kaggriculture.py:333`), so a mixed load cannot shed its wool without
        # its wheat -- but the wheat lands in the shed on the tile the unit is standing on, and the
        # `PICKUP` branch above draws it straight back next turn. One turn, against a product that
        # would otherwise sit unsold until the overnight sweep.
        if (DELIVER_THE_SELL_ROW and (act[0] in STEP or act == ["PASS"]) and pos in depots
                and deliverable >= MIN_SELL_ROW_DROP
                and sum(shed.values()) + sum(inv.values()) <= SHED_CAPACITY):
            for item, qty in inv.items():
                if qty > 0:
                    shed[item] = shed.get(item, 0) + qty
                    owed_sale[item] -= qty
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
            # `planted` is cumulative for the season, so a day's own progress is the difference from
            # this mark. Only the non-router seed path needs it: under `router` the demand is read off
            # the live PLANT pins, which pop as they are planted and so reconcile themselves.
            state["planted_dawn"] = collections.Counter(state["planted"])

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
        last_day = max(sched) if sched else day
        pending = 0          # cash this turn's sells will have banked by the time BUY_LAND settles
        rate = collections.Counter()
        # Everything the rest of the season will EVER ask for, per product. Stock above this can only
        # leave the shed on the last day, so it is what `still_owed` below releases early. Days after
        # today only: today's own row is `today`, and double-counting it would hide real surplus.
        still_owed = collections.Counter()
        horizon = day + (SELL_SURPLUS_HORIZON if SELL_SURPLUS_HORIZON is not None else len(sched))
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
        if SELL_TO_MAKE_ROOM:
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
        for prod in SELLABLE:
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
                have = max(0, have - max(0, feed_days(day) * alive - ripe_wheat - carried_wheat
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
                n = min(have, allow, rate[prod])
                # **The row is a DAY TOTAL, and re-offering it every turn made it a per-turn quota.**
                # `rate` bounds one offer; nothing bounded the day. Seb's day-4 row asks
                # `WHEAT 28, FERTILIZER 4` and he sells exactly that -- 28 and 4. We sold 34 and 5,
                # and day 5 then sold 10 against his 26 with the stock already gone. The carry above
                # is what recovers a genuinely missed row; it is not a licence to outrun a met one.
                n = min(n, allow - state["ordered"][("sold", prod)])
                # **Then top up to keep room for the drop.** Applied AFTER the caps rather than
                # through `allow`, because `allow` is bounded by `rate[prod]` two lines up and the
                # whole point is that the row cannot know about a full shed. It can only ever
                # increase a sale, never block one.
                #
                # Only genuine surplus is released -- stock above what every remaining row will ask
                # for -- so a product a later day still needs is never dumped to make space for
                # tonight. That is what keeps this from becoming the `shed_dusk` arm by accident.
                if release[prod] > 0:
                    n += min(max(0, have - n), release[prod])
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
                if money < R.ANIMALS[a]["cost"] + (seed_bill if SEED_BEFORE_LIVESTOCK else 0):
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
        for crop, qty in sorted(want_seed.items(),
                                key=lambda kv: -RT.SEED_COST.get(kv[0], 0) * int(kv[1])):
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
        herd = feed_days(day) * alive - fed_today - on_hand - state["ordered"][("feed", "WHEAT")]
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

        return {"farmer": acts[0] if acts else ["PASS"], "hands": acts[1:],
                "market": _order_sells(_fit_slots(orders, state))}

    return agent
