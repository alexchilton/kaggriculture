# The d4/d5 planner chain: the spawn-ring step deletes the depot draw

Fable, 2026-08-11.
Worktree `agent-abcebcdbb11b26b7e`, detached at `f847e7d` ("Day zero matches"), plus the two experimental edits described below (uncommitted, in `kagg/search/schedule_agent_1455mh.py`).
Everything here is measured on seed 11, Victor tape, `townCenterSellInterval 24`, `weeds 0.0`, via `python -u scripts/breakdown.py --module schedule_agent_1455mh --tape victor --days 12`.

## Verdict in one paragraph

The cost model is right and the executor is wrong.
u0's d4 tour is costed at 21 turns against a budget of 24 and that plan is achievable.
The executor spends 27, because `acts[0] = [step_off]` (line ~2777) overwrites the farmer's hour-0 action AFTER `_router_acts` has already walked the route for that hour — and on d4 that hour's action was `PICKUP WHEAT 2`, which the walk had already CONSUMED from the route state (`node.pick` emptied at `:1837-1841`, the local `shed` counter decremented).
The route then believes wheat is in hand that was never drawn.
Six unpriced turns follow — 2 for the step-off round trip, 4 for the recovery — and the tour's tail stop `(0,4)[WATER, HARVEST]` is 3 turns out of reach.
That one dropped stop is `water 14/15` and `harvest 4/5` on d4; the un-freed tile is d5's `plant 4/5` and `strawb 6/7` (confirming Alex's own dawn instrumentation: d5 needs six tiles and has five).
Deferring the walk instead of deleting the draw fixes d4 and d5 exactly and moves the first divergence to d6.

## 1. The traced mechanism (d4, hour by hour)

Full trace: `data/logs/fable_trace_d4.log` (route state, computed act, and emitted act per hour).
The plan: `Shed(4,4)[pick WHEAT 2] -> (2,4)[FEED,CARE,COLLECT] -> (3,4)[FEED,CARE,COLLECT] -> (1,4)[WATER] -> (2,3)[WATER] -> (0,4)[WATER,HARVEST]`, cost 21, budget 24.

    h00  (4,4)  computed PICKUP WHEAT 2 -- route consumes it (pick={}), shed 6->4 locally
                EMITTED NORTH (the overwrite).  Wheat never drawn; route thinks it was.
    h01  (4,3)  SOUTH -- walking back to the depot stop it believes is exhausted
    h02  (4,4)  depot pick empty -> stop POPPED -> WEST.  Standing ON the shed, draws nothing.
    h03-h04     WEST WEST to (2,4); COLLECT_FERTILIZER (planned)
    h05         `_live_ops` offered no FEED (no wheat in inventory);
                `FETCH_THE_FEED_AND_RETURN` inserts an UNPLANNED depot stop: EAST
    h06-h07     EAST; PICKUP WHEAT 2 at the shed -- the planned draw, taken 7 hours late
    h08-h09     WEST WEST back to (2,4)
    h10-h15     FEED CARE (2,4), EAST, FEED CARE COLLECT (3,4)
    h16-h21     the tour continues: WATER (1,4), WATER (2,3)
    h22-h23     SOUTH, WEST -- still 1 move + WATER + HARVEST short of (0,4) when the day ends

Waste, quantified: 2 turns (h00 step off + h01 walk back, never budgeted) + 4 turns (h05, h06, h08, h09 — the fetch round trip that exists only because of the phantom draw).
21 + 6 = 27 > 24, over by 3, which is exactly the walk+work remaining to `(0,4)` at midnight.

So, to Alex's direct question: the model under-charges only the 2 step-off turns; the other 4 are the executor wasting turns the model correctly never priced, because the work they redo was already done on paper at h00.

## 2. Where else it fires

The overwrite only matters when the farmer's h0 computed action MUTATES state.
A computed MOVE or PASS overwritten by the step costs nothing (the route was not touched).
Traced d0-d6 (`data/logs/fable_trace_d0_d5.log`, `fable_trace_d6_defer.log`):

    d0  h0 computed PASS  (WAIT_FOR_THE_MORNING_DELIVERY; shed empty)   no overwrite fired
    d1  h0 computed WEST                                                 no overwrite fired
    d2  h0 computed PASS                                                 no overwrite fired
    d3  h0 computed PICKUP WHEAT 2 -> OVERWRITTEN   6 wasted turns, absorbed by slack (only `pass` moves)
    d4  h0 computed PICKUP WHEAT 2 -> OVERWRITTEN   tail dropped: water 14/15, harvest 4/5
    d5  h0 computed PICKUP WHEAT 3 -> OVERWRITTEN   a water lost: 8/9
    d6  step_off is None all day (farmer works a clean 24-turn tour)

`step_off` can only ever fire at hour 0: `_hires_this_turn` returns 0 for `hour != 0`, so `_clear_the_spawn_ring` gets `n=0`, `lost=0`, and returns `None` on every later hour.

## 3. The fix that keeps BOTH the step and the draw: defer, don't delete

Alex's suspicion was right: the fix lives in how the route advances when the emitted action is overridden, not in the overwrite itself.
Delta 1 (`hold_farmer`): when the call site is going to overwrite the farmer's action, `_router_acts` must not walk u0's route at all that turn — emit a placeholder, leave the depot stop unconsumed.
The tour then starts one turn late instead of one stop short: the farmer steps NORTH at h00, walks back at h01, takes the REAL pickup at h02, and the whole tour fits (21 + 2 = 23 ≤ 24).

Why the two reverted attempts had to lose, for the record:

- Removing the step-off entirely re-ran the spawn rotation: on d3-d5 the farmer's h0 act is a PICKUP that keeps it ON `(4,4)` as the hires settle, so a second hand lands on the dead `(5,5)` corner and idles 23 turns (`_clear_the_spawn_ring`'s own measured table). d3 `water 4/9` is that hand's whole route, gone.
- "Only overwrite a MOVE" is the same change wearing a guard: on exactly the days the bug fires (d3-d5, PICKUP days), the guard suppresses the step, which is the removal case above. That is why it left d4 `harvest 4/5` untouched AND wrecked d3.

Delta 2 (`farmer_start`): additionally cut u0's tour from the tile the step lands on, one turn poorer, so the plan charges the step.
Measured on top of delta 1: byte-identical grid except d4 `pass 2 -> 1` (one idle turn becomes a move; both exempt rows).
A near-null here — the trigger (a farmer tour planned tighter than 22) never occurs on this tape — but it is the honest cost model and the insurance against a tight day.
Alex's call whether it stays; the project's revert-a-null rule argues against, the plan-once doctrine ("crew arrival is planned for, not discovered") argues for.

Both edits are in the worktree, flagged as EXPERIMENT with my name on them.
Test: `tests/test_the_spawn_step_defers_the_depot_draw.py` — red at `f847e7d` (`d4 water 14/15 -- the tour tail was dropped`), green with delta 1, verified in both directions.

## 4. The grid, before and after

Baseline (`f847e7d`, `data/logs/fable_baseline_grid.log`) — first non-exempt op divergences: d1 `care 0/5`, then d4:

    plant               10/10  0/0  0/0  4/4  5/5  4/5  1/1   9/14  11/10   6/1  17/23  13/11
    water               10/10  0/0 10/10 9/9 14/15  8/9 12/12 26/33  22/22 27/28 36/43  45/41
    harvest              0/0   0/0  0/0  0/0  4/5   0/0  4/4   1/1    6/6   5/5   4/6    4/4
    strawb (board)       0/0   0/0  0/0  3/3  3/3   6/7  7/8  14/18  16/20 20/20 31/31  32/36
    weeds                0/0 throughout

With the fix (`data/logs/fable_defer_plus_charge_grid.log`, reproduced by the final tree in `fable_final_grid.log`):

    plant               10/10  0/0  0/0  4/4  5/5  5/5  0/1  15/14   7/10   3/1  15/23  17/11
    water               10/10  0/0 10/10 9/9 15/15  9/9 11/12 33/33  17/22 29/28 31/43  47/41
    harvest              0/0   0/0  0/0  0/0  5/5   0/0  4/4   1/1    6/6   5/5   5/6    4/4
    strawb (board)       0/0   0/0  0/0  3/3  3/3   7/7  7/8  17/18  17/20 17/20 29/31  30/36
    weeds                0/0   0/0  0/0  0/0  0/0   0/0  0/0   1/0    1/0   2/0   2/0    3/0

d4 and d5 now match on every non-exempt row except d5 `dig 0/1` and the sell shortfall that predates the fix (d5 `sell 15/22`, baseline 14/22).
On the d5 dig: Victor's tape digs on d5/d7/d11 as unconditional open-loop script actions; our fixed board has no weed on d5, so there is nothing to dig and `0/1` is the honest state.
Baseline's `1/1` was our agent digging SOMETHING on its own diverged board — I did not trace what, and it should not be read as a matched behaviour.

The stale Seb gates (`test_each_day_matches_the_tape.py` 6F/1P, `test_the_first_seven_days_match_the_plan.py` 7F/7P/1x — both still target tape `90494364`) fail IDENTICALLY with the fix on and off.
No pinned test regresses.

## 5. The new frontier: d6, and the weeds

The fix moves the first divergence (after d1 `care 0/5`, see §7) from d4 to d6, and d6 was never clean: baseline already had `build 0/2`, `place 0/1`, `pens 6/8`, `cow 2/3`, `buy_seed 1/4` there.
Under the fix d6 also slips `water 12->11 (/12)` and `plant 1->0 (/1)`, because d5 now ends with the NW quadrant FULL (19 crops + 6 pens = 25/25; baseline had 24) — the tape's own board is identical, so this is ground Victor handles and we do not.
The step-off is NOT involved: it never fires on d6, and the farmer's d6 tour executes cleanly to h23 (`data/logs/fable_trace_d6_defer.log`).
d6's `idle 42/5` with uncovered work on the board says plan gap, not executor waste — a separate investigation.

**The weeds are a latent router defect the fix made reachable, with a measured mechanism.**
`reference/kaggriculture.py:209`: a new plant is created with `consecutive_unwatered: 1` — "planting day counts as unwatered".
The nightly refresh (`:766-771`) increments and weeds at 2.
So ANY plant not watered the same day becomes a weed that night, seed burned, dig owed.
Measured: tile `(5,3)` went `LOCKED -> None (d6 h13, the parcel purchase) -> WEED (d7 h23)` without ever being sampled as a plant (`data/logs/fable_trace_cell53.log`) — one of d7's 15 plants landed in the day's FINAL hour and was weeded by the same step's refresh.
The router pairs a pinned PLANT with its WATER (`PLANT_THEN_WATER`) but prices the water as a prize, not a co-requisite, and nothing forbids a PLANT so late it cannot be watered.
Baseline never tripped this only because its d7 planted fewer (9 vs 15).
The rule to encode, when this is picked up: a PLANT whose same-day WATER cannot also be executed is worth LESS than nothing — it converts a seed into a weed.

## 6. The retracted replant line — why attempt 3 could not have worked (code-read, not measured)

Alex retracted "replant the tile you just harvested", so I did not re-run his attempts; but the code answers why attempt 3 failed even with `HARVEST_THEN_PLANT` in `build_nodes`.
The pinned-tile gate exists in TWO places:

- `router.build_nodes:956`: `if tile in pinned or not isinstance(cell, dict): continue` — the planner side he patched.
- `_live_ops:1349-1352` (`schedule_agent_1455mh.py`): a pinned tile whose cell is not `None` returns `[]` — the EXECUTOR side.

The route is a visit order and `_live_ops` re-derives the work at each stop, so even a correctly emitted HARVEST+PLANT node on a pinned occupied tile is dropped silently at execution.
Any future variant of this idea must patch both, or it is deleted at the second gate it never saw.

## 7. Loose ends, stated so they are not lost

- **d1 `care 0/5` is an op divergence EARLIER than d4** and was absent from the working summary.
  The tape cares its 5 animals on d1 while feeding none; we do neither.
  Present at baseline and unchanged by this fix.
  By the days-match-in-order rule it is technically the first open day.
- d5 `sell 15/22` (baseline 14/22) and the money drift from d5 on predate the fix and are the sell chain, not this chain.
- Delta 2's cost model charges 1 turn (plan cut from the stepped tile); the true round trip is 2 when the tour's first stop is the shed itself.
  If a future day plans the farmer at exactly 23, this halves the safety margin — worth revisiting if a tail ever drops again on a step-off day.

## Artifacts

- Experimental edits: `kagg/search/schedule_agent_1455mh.py` (uncommitted; `hold_farmer` + `farmer_start`, both flagged EXPERIMENT).
- Test: `tests/test_the_spawn_step_defers_the_depot_draw.py` (red on `f847e7d`, green with delta 1).
- Logs: `data/logs/fable_baseline_grid.log`, `fable_defer_grid.log` (delta 1 alone), `fable_defer_plus_charge_grid.log` (delta 1+2), `fable_final_grid.log` (byte-identical to the previous — the tree reproduces its own measurement), `fable_trace_d4.log`, `fable_trace_d0_d5.log`, `fable_trace_d6_defer.log`, `fable_trace_weed.log`, `fable_trace_cell53.log`.
