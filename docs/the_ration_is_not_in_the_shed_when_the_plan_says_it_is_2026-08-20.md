# The dawn plan credits wheat at hour 0 that the market delivers at hour 6

Measured 2026-08-20 on `data/seed_scripts/downloads_2026-08-19/94345389.json`, tetsuya seat 0,
seed 959074148, following `data/seed_scripts/tetsuya/schedule.json`.
Logs: `data/logs/loop_2026-08-20.log`, `stage3_2026-08-20.log`, `carry_2026-08-20.log`.

## The loop: router, plan, execution

Three checkpoints per pen per day, `_solve` wrapped to capture the node list going in and the
routes coming out. No code was edited.

    day  pen     animal  unfed | ROUTER  PLAN   EXEC   | verdict
    ------------------------------------------------------------------------------
    3    (4,3)   COW     0     | yes     yes    NO     | << EXEC failed (planned, not done)
    4    (3,3)   SHEEP   0     | yes     yes    NO     | << EXEC failed (planned, not done)
    4    (4,2)   COW     0     | yes     yes    NO     | << EXEC failed (planned, not done)
    4    (4,3)   COW     1     | yes     yes    NO     | << EXEC failed (planned, not done)
    ------  every other pen on d1-d6                   | ok

**The router offers a FEED on every pen on every day, and the plan commits to every one.** Four are
never carried out. Nothing is lost in stages 1 and 2, so `at_risk`, `will_be_fed`, the arrival
budget and the greedy ordering are all confirmed irrelevant -- they live upstream of the break.

## The break

    d3 h1  unit 1 at (4,4) shed  carrying={}               act=WEST               shed.WHEAT=0
    d3 h2  unit 1 at (3,4) pen   carrying={}               act=COLLECT_FERTILIZER shed.WHEAT=5
    d3 h3  unit 1 at (3,4) pen   carrying={FERTILIZER:1}   act=EAST               shed.WHEAT=2

    d4 h1  unit 0 at (4,4) shed  carrying={}               act=PICKUP COW 1       shed.WHEAT=0
    d4 h3  unit 0 at (3,4) pen   carrying={COW:1}          act=COLLECT_FERTILIZER shed.WHEAT=0
    d4 h6  unit 0 at (4,4) shed  carrying={}               act=PICKUP COW 1       shed.WHEAT=3
    d4 h9  unit 0 at (3,4) pen   carrying={COW:1,WHEAT:1}  act=WEST               shed.WHEAT=1

1. The dawn plan credits the row's full `buys={'WHEAT': 6}` at hour 0 and routes
   `(4,4)[PICKUP] -> pen[FEED, CARE, COLLECT_FERTILIZER]`.
2. The unit reaches the shed at h1 and the wheat is not there. The PICKUP loads nothing (d3) or a
   COW instead (d4).
3. It arrives at the pen with no ration. `FEED` takes a WHEAT from the **acting unit's carried**
   inventory (`reference/kaggriculture.py:505`, `inv = _farmer_inventory` at `:321`), so the op is
   not live and is dropped silently. `CARE` goes with it.
4. `COLLECT_FERTILIZER` is the only live op left at the stop. The turn goes to fertilizer and the
   unit walks away.
5. Wheat trickles in over h2-h6. By h9 unit 0 carries one and is walking past the pen with its stop
   already spent.

`RANK = dict(FEED=0, CARE=1, COLLECT_FERTILIZER=2, ...)` (`schedule_agent.py:1136`) was never
overridden. FEED lost the turn because it was never offered.

The second failure mode on d4 -- units 3 and 6 never reaching their pens at all -- is the same
day's tour arithmetic built on a shed credit that did not materialise. Those are the two hands that
show `PASS` in every hour of `data/logs/d4_2026-08-20.log`.

## What this costs

Pen (4,3) misses d3 and d4, hits `consecutive_unfed >= 2`, and escapes at d4 night
(`reference/kaggriculture.py:817`). Herd 7 on d4, 6 on d5, 1-3 short of his every day after.

## Not verified

Whether the h1 shed is empty because our own buy cadence drips the order across the day
(`BUY_DRIP` -- `schedule_agent.py:5291` records that a single large block walks `market_price` up
and fills LESS, and that the tape places sixteen separate WHEAT buys of 1-6 across h1-h22), or
because the book is too thin to fill at h0. **These need different fixes.** One probe separates
them: print the market orders we emit per hour against the shed delta per hour.

## The test to write first

d3 on this board and seed: the unit routed to feed pen (4,3) is carrying a WHEAT when it arrives.
Write it RED, confirm it goes red on revert, and judge the fix on the **d0-d10 grid**, not on the
test -- `SUPER_IMPORTANT_READ_THIS_FIRST.md` §4 records two feed fixes that passed their own tests
and lost the season.

## Caveat

One board, one seed.
