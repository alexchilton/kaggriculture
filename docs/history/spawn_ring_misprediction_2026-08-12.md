# Every hand is routed from a tile it does not wake on

2026-08-12, seed 11, tape `victor`.
Found while chasing why `(1, 2)` weeds at the end of d11 and costs `strawb 35/36` for the rest of the season.

## The finding

`_end_of_day` discharges the whole crew — `farm["hands"] = []` (`kaggriculture.py:867`).
Every hand is therefore a fresh `_spawn_hand` every morning, and the dawn plan can only *predict* where they land.

`_arrivals` (`schedule_agent.py:343`) is that prediction: least-occupied shed-access tile, ties in NWSE ring order `[(4,4), (5,4), (4,5), (5,5)]`, counting `[farmer] + hands` at the moment the HIRE settles.

The hires settle in the **market** phase, which runs **after** the unit phase (`kaggriculture.py:922` then `:928`).
So the ring the hires see is the ring *after* the farmer has taken its hour-0 action.

`_clear_the_spawn_ring` knows this, and handles the case where the farmer is stepped off **deliberately** — but it only steps off when the step saves a hand from the dead `(5,5)` corner.
Once the board is fully unlocked nothing is dead, so it returns `step_off=None` and predicts the ring with the farmer still on `(4,4)`.
The farmer's own routed tour then walks it off `(4,4)` at hour 0 anyway.

`(4,4)` reads empty when hire 1 settles, and **every hand of the day lands one ring slot early**:

    d11, seed 11, 11 units
      predicted  (5,4) (4,5) (5,5) (4,4) (5,4) (4,5) (5,5) (4,4) (5,4) (4,5)
      actual     (4,4) (5,4) (4,5) (5,5) (4,4) (5,4) (4,5) (5,5) (4,4) (5,4)

The prediction and the farmer's hour-0 move are **two separate decisions that disagree**.

## What it cost, exactly

u10 on d11, priced at 23 turns against a budget of 23 — zero slack:

    PLANNED   start (4,5)
      (4,5) PLANT                       2 turns
      (7,3) WATER HARVEST PLANT   5 mv + 4 = 9
      (6,2) WATER HARVEST PLANT   2 mv + 4 = 6
      (1,2) WATER                 5 mv + 1 = 6
                                        -- 23, fits to the turn

    ACTUAL    woke on (5,4), two turns away
      h01 WEST  h02 SOUTH   <- the two turns
      h03 (4,5) PLANT/WATER ... h19 (6,2) done, on schedule from there
      h20-h23 WEST x4 -> ends at (3,2), two tiles short of (1,2)

`(1,2)` weeded that night at `consecutive_unwatered >= 2` (`kaggriculture.py:770`).

## What is NOT the cause — all excluded with evidence

The job was **offered** (`crop_ops` emitted it), **covered** (`uncovered` empty), and **assigned** (to u10).
So it is not the node set, not triage, not priority, and not the assignment.
There is no DIG anywhere in u10's day; all 25 turns are accounted for.

Four earlier hypotheses were excluded the same day and are recorded in `REGISTER.md`: mid-day ferrying, pen siting, brink-water pricing, and the closing walk home.

## The obvious fix is a measured LOSS

Pin the farmer on a hire turn while it stands on the ring, reusing the `hold_farmer` machinery that already exists for the deliberate step.
That makes the prediction true by force, and the force is a turn of the 24-turn unit on nearly every hire day.

17-day grid, seed 11, `--tape victor`:

| | baseline | pinned |
|---|---|---|
| money @ d16 | **17,459**/15,759 | 16,044/15,759 |
| strawb from d11 | **35**/36 | 33/36 |
| weeds | **2**/0 | 4/0 |
| d11 move | 128/99 | **109**/99 |
| d11 idle | 23/57 | 40/57 |

`(1,2)` lived and `(0,2)`, `(1,4)` and `(2,1)` died in its place.
Reverted.

## The second cause, not yet chased

With the pin on, d11 went **fully green** and d10 from 14 wrong to 7.
The residual is a different mechanism: hands that arrive in a **later wave** (d10 hires across h0/h1/h2), by which time the h0 wave has walked off the ring, so the h0-computed `arriving` list is stale for them.
`_arrivals` predicts all of a turn's hires at once from the h0 ring.

## The untried direction

Fix the **prediction**, not reality: re-plan once after the farmer's hour-0 move is known.
Costs one extra solve on a hire turn and **no game turn**.
Risk is that the second solve moves the farmer somewhere else again — it is a fixed point with no convergence guarantee, so it would need a cap and a measurement.

## Artifacts

- `tests/test_a_hand_starts_the_day_on_the_tile_it_was_routed_from.py` — red on the mechanism, **green on the d9 control** (8 units, farmer parked, all eight predictions exact). Marked `xfail` because the defect is open.
- `data/logs/is_it_assigned_2026-08-12.log` — the offered/uncovered/assigned/walk trace.
- `data/logs/grid_baseline_2026-08-12.log`, `data/logs/grid_pin_farmer_2026-08-12.log` — the A/B.
- `data/logs/which_tile_dies_2026-08-12.log`, `..._pinned_...`, `..._baseline_...` — which tile weeds.

## Standing context this sits in

The alternate-day watering cadence (`router.crop_ops:650`) waters only tiles at `consecutive_unwatered >= 1`.
The counter starts at 1 on the planting day and weeds at 2, so a tile watered yesterday is safe tonight — which means **~20 tiles sit one miss from death every day, all season**.
There is zero margin, so any day that loses turns converts directly into a permanent tile loss.
That is the reason a 2-turn misprediction is worth a season of `strawb 35/36`.

## Everything ruled out on 2026-08-12, with the measurement

All on seed 11, tape `victor`, 20-day grid. Do not re-derive any of these.

| attempt | result |
|---|---|
| Pin the farmer on hire turns (`hold_farmer`) | **LOSS.** money@d16 17,459 -> 16,044; weeds 2 -> 4. `(1,2)` lived, `(0,2)`/`(1,4)`/`(2,1)` died. Costs a turn of the 24-turn unit nearly every day. |
| Predict the farmer walks off the ring | **BREAKS THE CONTROL.** d9 goes red — the farmer *stays* on d9 and *leaves* on d0/d1/d6/d10/d11. Its hour-0 behaviour is day-dependent, so no constant prediction is right. |
| Two-pass re-solve | **DOES NOT FIT.** A full hour-0 solve is 0.37-0.5s by d10-d17 against a 1s `actTimeout`; d10 would need three. Measured, not assumed. |
| Tour slack (`START_SLACK_TURNS` 1 and 2) | **LOSS on the farm.** d19 weeds 3 -> 7, strawb 33/33 -> 30/33, work 149 -> 126. Money rises (26,889 -> 27,538) only because we sell instead of tending — the wrong trade on an Elo ladder. It does not redistribute; it just does less work, and the dropped jobs are the brink waters. |
| Buy fertilizer (today's demand, and tomorrow's) | **NULL both ways.** `fertilize` d16 stays 10/13 at 0, today and tomorrow. Buying for today is too late by construction: `_process_market` runs after the unit phase, so stock lands after the crew drew at h1-h3. And the premise had already expired — see below. |
| `COVER_PLANNER = False` (the "old planner") | **BIT-ROTTED, not slower.** money d19 0/27,133, work 0/145, 18 weeds. It banks the $15 start and flatlines from d12. There is no comparison to be had. It is a stale runnable artifact and a trap. |

## Two corrections to earlier claims in this document's neighbourhood

- **"The tape wastes turns watering pastures" is WRONG and was my methodology.** The script compared
  the tape's watered tiles against *our* board state. Our pen placement differs from his, so a tile
  that reads PASTURE for us may well be planted for him. Nothing can be concluded about his tiles
  from our board. Retracted. The consequence runs against us: d16's water gap is the full 6 tiles.

- **The fertilizer starvation premise expired.** It was real when written (shed 1-4 against the
  tape's 12) and `FERTILIZER_RESERVE_LOOKAHEAD_DAYS = 1` fixed it: we now hold **14-20 against the
  tape's 12-13**, i.e. more than he does, and still fertilize less. Verified per-unit — u13 asks the
  shed for 6 FERTILIZER and now **gets all 6**, where it got 0 before. Supply is solved.

## What the tour probe actually found on d16

Comparing our plan against our own execution — no tape involved, so no board-state contamination:

    day 16: only 2 assigned jobs whose unit never stood on the tile
      u13  (5,0)  ['FERTILIZE']
      u13  (6,0)  ['FERTILIZE']
    u13: start=(5,4) budget=23 priced_cost=20  SLACK=3
         actual walk begins h02 at (4,4)     <- wrong tile AND a turn late

So **execution is not the problem**. 39 waters offered, nothing uncovered, all executed; 50 idle
turns and 96 turns of priced slack left over. The water row is a difference in what gets OFFERED,
and with the boards diverged by d16 that cannot be attributed to a defect from our side alone.

## The open question, restated

`cover.cover` is a **greedy insertion heuristic** — insertion positions per unit, cheapest that fits,
plus displace-and-rehome and `_make_room`. No global search, no restarts, no backtracking, no
optimality guarantee. How far its output sits from feasible-best has never been measured, and that
number decides the next move: near the frontier means the lever is the node set and the schedule;
well short means the planner itself is the lever. d18 is the day to measure it on — we spend 263 of
275 unit-turns, Victor spends 235 of 272 and does more.

## The d16 water gap: PARTLY a counting artifact, but we DO lose tiles he does not

Settled by replaying both sides and reading **each side's own board** — the earlier attempt read his
actions against *our* tiles, which is invalid once the boards diverge.

    day 16   ours: 53 water ops on 45 distinct tiles
             tape: 59 water ops on 45 distinct tiles

**Identical tile coverage.** The `water 53/59` row counts OPS, not tiles.

`_apply_unit_action` makes a repeat water a no-op — `if tile["watered_today"]: return`
(`kaggriculture.py`, WATER branch) — and a water on a non-PLANT returns immediately. So:

- his 59 ops on 45 tiles are **14 wasted turns**, plus two spent on PASTURE cells on his own board
- ours are **8 wasted turns**

We are *more* efficient per tile than the tape. Of the 14 tiles he waters and we do not, **12 are
non-comparable** — his board genuinely differs by d16 (he holds `WHEAT planted_d12 yield=3` where we
hold `STRAWBERRY planted_d5`; two are PASTURE for him too).

**DO NOT read the above as "nothing to fix" — that conclusion was wrong and is retracted.**

Matching tile COUNTS is not matching tile SETS. Of the 45 each side waters, only **31 overlap**:
14 he waters that we do not, 14 we water that he does not. Nearly a third of the day's watering is
different tiles.

And the decisive row was on screen the whole time: **weeds 3/0**. He loses ZERO tiles all season.
We lose three:

    (1,2)  STRAWBERRY  dead end of d11
    (2,0)  WHEAT       dead end of d14
    (9,0)  WHEAT       dead end of d18

So the water cadence IS deficient. What the board-vs-board harness legitimately establishes is only
the narrower claim that the raw `water 53/59` op-count gap is not itself the deficiency — six of his
extra ops are no-ops. The deficiency is which tiles we skip, and it costs three tiles.

**The cadence question is crop-dependent and was not being treated that way.** From `CROPS`:

    WHEAT       ongoing False  max_yield_day 4   max_yield 6   window = age 2..4
    MELON       ongoing False  max_yield_day 12  max_yield 6   window = age 6..12
    STRAWBERRY  ongoing True   interval 2
    TOMATO      ongoing True   interval 1

The WATER branch adds yield ONLY for `ongoing: False` crops, inside `window_start =
(max_yield_day + 1) // 2`. So for WHEAT and MELON every missed day inside the window is yield gone
permanently, not merely weed risk — a melon has 7 days to bank 6 units. For STRAWBERRY and TOMATO
water adds NO yield at all and buys only survival. Two of our three dead tiles are WHEAT.

Caveats worth re-checking before leaning hard on it: the exact 45-45 equality is striking (plausible
— both farms hold 75 tiles under the same cadence, so ~45 on the brink is an equilibrium — but not
verified twice), and tile attribution reads the previous turn's positions, which can be off by one.
That noise applies equally to both sides, so the comparison survives it.

**The one actionable thing this found is ours:** we spend ~8 turns a day watering tiles that are
already watered. Small, free, and the opposite of the problem being hunted.

Harness: `scratchpad/board_vs_board.py`.
