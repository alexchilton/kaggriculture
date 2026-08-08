# Day 12's unfed sheep: root cause, fix, and its cost

Written for `docs/brief_d12_unfed_sheep_2026-08-08.md`. That brief already traces the turn-by-turn
symptom and rules out `Node.needs` being empty; this fills in the mechanism it asked for and the fix.

## Root cause

`cover.materialise` plans u7's tour correctly: at hour 3 it opens with `Depot(pick={WHEAT: 2})`
before the two FEED jobs at (2,5) and (1,6), because u7 starts the tour holding nothing. The plan is
right, confirmed by instrumenting `_solve` directly on the real day-12 board (seed 11, weeds off).

The bug is in the executor. `_router_acts`'s depot-walk branch, at the moment it tries to serve that
draw, reads a **live shed at `WHEAT: 0`** -- drained by the sell block plus three other units'
own draws inside the same hour-3 replan (u0, u1, u2 were carrying 5+3+2 WHEAT between them, so the
FEED nodes were still correctly offered -- `have_wheat` in `build_nodes` checks `shed OR carried` --
but the literal shed had nothing left for the fourth unit). The old code:

```python
item = min(node.pick)
want = node.pick.pop(item)          # removed BEFORE checking whether the shed can supply it
take = min(want, shed.get(item, 0))
if take <= 0:
    continue                        # node.pick is now missing `item` regardless of the outcome
```

`node.pick.pop(item)` is unconditional. On the very next loop iteration `node.pick` reads empty, the
depot stop pops itself off the route unworked, and the WHEAT need is gone -- not "gone until the shed
refills" but gone outright. The shed genuinely does refill a few turns later off the ordinary
`BUY_PRODUCT` drip (measured on the same trace: `WHEAT` reads 0 at hour 3, 6 by hour 6), but nothing
in the model remembers the pen was owed a second attempt. `build_nodes` also stops re-offering FEED
for (1,6) once no unit is left holding wheat in hand (`have_wheat` goes false), so no later replan or
idle top-up ever revisits it. That combination is why the pen is "OWNED BY NOBODY" from hour 11 on.

## The fix

Two changes, `kagg/search/cover.py` and `kagg/search/schedule_agent.py`:

1. `cover.Depot` gained a `critical` flag, set by `materialise` when a draw serves a job that is both
   `at_risk` and `required` (an animal one missed feed from escaping tonight,
   `consecutive_unfed >= 1` and `FEED` in its ops -- the exact rule `REQUIRED_OPS`/`_at_risk_tiles`
   already use elsewhere). Scoped to jobs that actually need one of the short items, so a draw serving
   only ordinary work is never marked critical by a coincidental critical job later in the tour.

2. `_router_acts`'s depot branch: the pick is no longer destructively popped before checking `take`,
   and a shortfall on a **critical** draw makes the unit stand and retry next turn instead of
   discarding the need. An ordinary (non-critical) shortfall keeps the old behaviour -- drop this
   attempt and move on -- deliberately: see below.

```python
if node.pick:
    item = min(node.pick)
    take = min(node.pick[item], shed.get(item, 0))
    if take <= 0:
        if node.critical:
            break                    # stand and retry; the animal is critical, not this stop
        del node.pick[item]
        continue                     # ordinary shortfall: give up on this attempt, as before
    node.pick[item] -= take
    if node.pick[item] <= 0:
        del node.pick[item]
    shed[item] -= take
    act = ["PICKUP", item, take]
    break
```

## Why "critical-only", not "retry every shortfall"

The first arm tried was unconditional: any failed draw makes the unit stand and retry. It fixes day
12 but regresses `test_router.py`'s day-4/5/6 continuity tests hard -- day 6 dawn bank fell from a
passing $830 to $15 against a required $860, and day 6 over-plants (20 of the tape's 14). Those tests
replay days 0-N *continuously*, so a hand standing idle at a depot for a few extra turns early in the
week cascades. Scoping the retry to `at_risk and required` draws only (the same test the covering
search already uses to decide what must not be skipped) recovers almost all of it:
`test_a_land_buy_may_be_funded_by_the_same_turns_sales` goes back to green, and day 6's over-plant
narrows from 20 to 16.

**It does not close it completely.** Three `test_router.py` tests still move, all in the same day
4-6 area the project's own comments already flag as fought-over and unresolved
(`router.py`'s `YIELD_FIRST`/`DEPOT_PEN_BY_LOAD`/`CASH_SHORT_SELL_FIRST` notes -- "held gate, not
solved", three arms tried and reverted):

- `test_the_biggest_sale_takes_the_earliest_slot` -- day 6 dawn bank $830 -> $309 (needs >= 860).
- `test_day_six_plants_every_tile_the_row_asks_for` -- day 6 planted 14 -> 16 (needs == 14).
- `test_day_six_gets_a_load_to_the_shed_early_enough_to_fund_the_strawberry` -- was a documented
  `xfail(strict=True)` ("held gate, not solved"); now XPASSes, which strict-xfail treats as a
  failure. This one is arguably an *improvement* (the gate it names moves), not a regression, but it
  changes test state and needs the marker revisited rather than silently accepted.

These are full-season, chained-day tests (`_seb_tape` replays turn 0 onward), a different measurement
regime from `matched_days.py`'s 29 *independent* single-day replays. A more surgical fix would need
to distinguish "this unit's OWN critical draw failed" from "some other unit's critical draw is also
competing for the same momentarily-empty item", or thread slack budget so a stand-and-retry never
eats into a day's land-purchase timing. That is real follow-up work, flagged rather than attempted
here per the instruction not to widen scope beyond this starvation.

Four pre-existing `test_router.py` failures (`test_day_four_matches_seb_on_every_op_it_works`,
`test_the_sells_row_is_a_day_total_not_a_per_turn_quota`,
`test_a_hand_full_of_the_days_sell_row_walks_it_in_when_there_are_turns_to_spare`,
`test_wheat_drawn_this_turn_is_the_herds_reserve_not_extra_to_it`) were failing before this change
too (confirmed on a clean revert) and are not attributed to it, though one
(`test_a_hand_full_of_...`) now fails on a different assertion inside the same test, which is worth a
second look but is not this bug.

## Test

`tests/test_a_stranded_feed_survives_a_dry_shed.py::test_a_depot_draw_the_shed_cannot_fill_yet_survives_to_be_retried`.
Two calls of the same `make_agent` closure, one hour apart, same day: a farmer standing on a depot
tile with an at-risk SHEEP pen elsewhere, plus a second hand far away already carrying WHEAT (so
`have_wheat` is true from the crew's carried stock exactly as on the real board, even though the
literal shed reads 0). Hour 3: shed empty, asserts the farmer does not fabricate a PICKUP. Hour 4:
shed refilled to 6, asserts the farmer NOW draws `["PICKUP", "WHEAT", 1]` -- proving the need survived
rather than being discarded at hour 3.

Confirmed RED on the unmodified code (`AssertionError: hour 4 returned ['NORTH'] ...`), GREEN with
the fix, RED again after manually reverting just the fix and re-running (file diffed byte-identical
to the pre-fix version at that point), GREEN again after reapplying.

## Measurement

`PYTHONPATH=. python3 -u scripts/matched_days.py`, seed 11, weeds off, log
`data/logs/matched29_d12_fix.log` against the immediately-prior baseline
`data/logs/matched_pen_identity.log`:

               before   after
    animals lost    1       0
    thirst deaths  25      25
    HARVEST ops   348     348
    PASS turns    984     976
    DROP ops       57      57
    days worse   11,12,15,19   11,15,19

Day 12 no longer loses an animal and no longer appears in "days worse". Thirst, HARVEST and DROP are
byte-identical; PASS improved (984 -> 976, not just "did not regress"). No other day's animal or
thirst count moved.

Fast test suite (`pytest tests/ -m "not slow"`): 835 passed / 8 failed before and after in raw count,
but the composition changed -- `test_a_land_buy_may_be_funded_by_the_same_turns_sales` fixed,
`test_a_stranded_feed_survives_a_dry_shed` (this fix's own test) added and passing, and the three
day-4/5/6 continuity items above are the net new cost, discussed above rather than hidden.
