# The sells land after the hire

Board `data/seed_scripts/downloads_2026-08-19/94345389.json`, seat 0, seed 959074148, d0-d10.
Ours from a live run of `schedule_agent` against his recorded actions.
His from replaying **both** recorded action streams, so his column is his own game, not the
contaminated replay-against-us column.
Every sell figure is a `_commit_unit` fill via `kagg/analysis/fills.py`. No offers are counted.
`unattributed = 0`.

## The question this answers

PLANT is `57/68` on d0-d10. The router offers all 72 and the plan takes all 72; the losses are one
silently-failed hire on d7 and sixteen hours at a zero bank on d10
(`docs/plant_is_a_money_problem_2026-08-20.md`).
So the question became: is the produce harvested on time, and is it sold in time to pay for the
crew?

## Harvest is on time

| day | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HARVEST ours/his | 0/0 | 0/0 | 0/0 | 10/10 | 0/0 | 0/0 | 3/3 | 0/0 | 2/2 | 5/3 | 4/4 |

Exact on every day, and two ahead on d9.
Harvest timing is **not** a defect and should not be looked at again on this board.

## Selling fertilizer is his strategy too

d0-d10 fill totals, by product:

| | WHEAT | FERTILIZER | WOOL | MILK | revenue |
|---|---|---|---|---|---|
| ours | 28 | 58 | 22 | 9 | 12,473 |
| his | 35 | 66 | 27 | 12 | 13,968 |

Fertilizer is his single largest sell line, 66 units in eleven days.
Ours is 58. This is the same play, not a leak, and the "we are selling the fertilizer we should be
using" theory is refuted. Recorded so it is not re-derived.

## Where it actually diverges: he blocks at dusk, we dribble all day

Sell fills per hour.

    day   ours                                             his
    d3    h10:2 h11:2 h17:1 h22:9 h23:6                    h15:9 h17:3 h18:5 h20:6 h21:9 h22:3
    d5    h0:2 h7:1 h8:1 h10:1 h11:1 h12:1 h14:1 h17:1 h23:1   h0:2 h21:4 h23:4
    d6    h7:7 h16:7                                       h23:14
    d7    h0:9 h6:1 h10:1 h12:1 h13:1 h14:1 h18:1 h21:1 h23:1  h0:9 h17:2 h18:3 h20:3
    d9    h0:8 h7:4 h10:2 h15:1 h20:2 h23:1                h23:12
    d10   h0:9 h17:3 h19:2                                 h0:8 h21:4

His day ends in a block. Ours is spread over eight or nine separate hours.

## Why the block is at h23 and not anywhere else

An order placed at hour `h` settles at the END of `h` (`kaggriculture.py:922` unit phase, then
`:928` market phase). A block sold at h23 therefore arrives as cash at **h0 of the next day** --
which is the turn the crew is hired.

His two biggest hiring days are funded exactly this way:

| | block sold | cash at next h0 | hands that day |
|---|---|---|---|
| d6 h23 -> d7 | 14 units | **+$2,302** | 11 |
| d9 h23 -> d10 | 12 units | **+$1,543** | 9 |

Ours on the same two transitions:

| | block sold | cash at next h0 | hands that day |
|---|---|---|---|
| d6 h16 (last) -> d7 | sold h7:7 h16:7 | +$87 at h7 | 10 |
| d9 h23 -> d10 | **1 unit** | **+$81** | 7 |

We reach d10 dawn with $1,164 against his $2,073, and our first cash of the day is $81.
The bank is at **$0 from h2 to h17**, the `BUY_SEED CARROT 8 / WHEAT 9` order re-posts every hour
and cannot fill, and 11 of the day's 19 plantings die there.

This is the whole mechanism. He is not richer over the eleven days -- $13,968 against our $12,473,
a gap of $1,495. He has the money **at hour zero**, and we do not.

## Two genuine revenue holes, separate from the cadence

- **d3: he sells 30 WHEAT, we sell 15**, off the same ten harvested tiles.
  Either our tiles carry fewer `yield_units` at harvest or we hold/feed more of it.
  **Not yet separated -- do not act on this line until it is.**
- **d8: he sells 21 units for $3,213, we sell 7 for $975** -- MILK 12 against our 6.
  The largest single-day gap in the window, -$2,238.

## What not to do next

Nothing in the planting path will move `PLANT 57/68`. The router and the planner both already
emit and schedule all 72. The binding constraint is cash at h0.

## MEASURED NULL 2026-08-20: pricing a FEED at the care it releases

Do not re-derive this. `animal_ops` prices a non-hungry FEED at `MANDATORY + BASE_PRICE[product]`,
so on d7 the COW at `(3,4)` holding **seven banked days of care** and a COW holding none bid
identically (`assert 100160 > 100160`). Adding the releasable bonus to the prize --
`min(max_held, held + 1 + bank) - min(max_held, held + 1)`, times the product price -- is correct
economics and measured **byte-identical** on the d0-d10 grid. Reverted.

It is not on the path. The pen is not losing a ranking contest; it is losing for lack of stock:

    d7, pen (3,4)   shed WHEAT   unit on the pen (carried WHEAT)   action
      h2      8       u1: 0                                        WEST
      h4      1       u0: 2                                        WEST
      h8      0       u1: 1                                        WEST
      h15     0       u1: 0                                        COLLECT_FERTILIZER   << its stop
      h16     0       u1: 0                                        EAST

The shed is empty from h8. Unit 1 serves its own stop at h15 with an empty hand, FEED is skipped,
CARE is skipped because CARE is only offered on a pen already fed, and the stop collects fertilizer
only. `data/logs/d7wheat_2026-08-20.log`.

The patch is at `scratchpad/router_fix.patch` and is worth re-testing **after** the wheat supply is
fixed, not before -- it can only bind once there is stock to allocate.
