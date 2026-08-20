# Watering post-d8: a well-evidenced negative, and what actually kills the odd tile

2026-08-15, seed 11, tape `kawashigi`, weeds 0.0, worktree on `af3db5d`.
Grid: `PYTHONPATH=. python -u scripts/breakdown.py --tape kawashigi --module schedule_agent --days 17`.
**Superseded mid-session by Alex's 30-day measurement: summed d9-d29 water is ours 798 / tape 795.
There is no volume shortfall. This file records the evidence so nobody re-derives the lead.**

## Watering is NOT under-planned -- the per-day cells that said so are a distribution artifact

The d10 25/32 and d12 30/40 cells are real, but they cancel against d9 29/23, d13 47/41,
d15 46/41, d16 41/37: summed d9-d16 on the 17-day grid the baseline waters **299 against the
tape's 274**, and d9-d29 it is 798/795. Any fix shaped as "create more WATER nodes" is aimed at a
gap that does not exist.

## The one fix tried, and its measured LOSS (do not rebuild it)

`ONGOING_TOP_UP_FROM_DAY = 9` in `router.crop_ops`: a safe ongoing crop (strawberry/tomato) was
offered a discounted preventive water (`_crop_remaining / 8`) from d9, on the argument that ongoing
crops have no preventive cadence at all -- `TOP_UP_SAFE_TILES = False` at `router.py:743` means a
safe strawberry is offered NOTHING, so it is watered exclusively by rescue at
`consecutive_unwatered == 1`, one lost stop from death every other day.

d0-d8: **zero changed cells** (verified cell-for-cell, `scratchpad/grid_diff.py`, logs
`data/logs/fable_water_baseline.log` vs `data/logs/fable_water_fix1.log`). But on the true grid
environment (recorded economy + shop draw, `data/logs/fable_probe_grid_baseline.log` vs
`fable_probe_grid_fix1.log`):

    post-d9 weed births   baseline: (0,3)@d16, (0,5)@d16                    = 2
                          fix:      (6,1)@d14 MELON, (0,8)@d16, (0,9)@d16   = 3
    money @ d16           32,794  ->  31,743   (-$1,051)
    d13 waters            baseline 45 offered / 45 watered
                          fix      54 offered / 51 watered, and one of the 3 lost was the
                                   (6,1) MELON survival rescue -> tile dead

The extra cheap offers displaced a rescue -- the exact failure mode of the pin experiment in
`docs/spawn_ring_misprediction_2026-08-12.md` ("(1,2) lived and (0,2), (1,4), (2,1) died in its
place"). Reverted immediately; the red-first test
(`tests/test_a_safe_ongoing_crop_is_offered_a_preventive_water.py`) was confirmed red again on
revert and deleted with the fix.

## What actually kills the 2-3 tiles a season: covered rescues on tours that cannot run

Where the water decision is made, for the record:

- Offers: `router.crop_ops` (`kagg/search/router.py:590`), called per tile by `build_nodes`
  (`router.py:1178` at `:1202`). `cover.py` creates no WATER jobs; it covers what it is handed.
- Assignment: `cover.plan` (`cover.py:1893`) from the single dawn solve at
  `schedule_agent.py:2245` (`_solve` at `:752`). `crew.cover` owns d0-d7 only
  (`crew.ACTIVE_UNTIL_DAY = 8`); precomputed routes exist for d12, 16, 18, 23-29
  (`cover.SOLVED_DAYS`).

Per-tile forensics on the grid environment (probe in scratchpad `water_probe.py`, log
`fable_probe_grid_baseline.log`): every killed tile's survival water was **offered, covered and
routed**, and died at execution. `data/logs/fable_d15_routes.log` has the smoking gun, d15 dawn:

    u6 start=(4,5) budget=23 cost=25  <-- OVER BUDGET
        DEPOT(4,5)pick{WHEAT:1} -> (4,5)[FEED,CARE,COLLECT] -> (1,4)[HARVEST] -> (0,4)[HARVEST]
        -> DEPOT(4,4)drop -> (0,3)[WATER] -> (0,5)[WATER]
    u9 start=(5,4) budget=23 cost=26  <-- OVER BUDGET

Both of u6's trailing waters -- the two tiles that weed into d16 -- sit at the tail of a tour the
plan itself prices at 25 turns against a 23-turn budget. The packer's admission check
(`cover.cover`'s `cost`, `cover.py:1280`) prices d10+ days with the closing trip charged
(`RESERVE_DAYS`, `deliver=True, wanted_only=True`), while the shipped route is materialised with
`deliver=False`, where `SHIP_WHAT_NO_LATER_STOP_CAN_BANK` inserts the mid-tour DEPOT drop instead.
Two different cost models price the same tour, a tour can fit under one and ship under the other,
and the difference lands on whatever stops sit at the tail. On d16 the same shape appears at
exactly 23/23 -- zero margin, which the spawn-ring arrival slip (1-2 turns, see
`fable_spawn_ring_verdict_2026-08-12.md`) then eats.

This is a RELIABILITY defect in tour pricing, not a node-count defect, it destroys ~2-3 tiles a
season on this seed, and it is route-sensitive: the solved_days regeneration in flight will move
which tiles it lands on. Left open deliberately -- fixing it is a cover/materialise cost-model
reconciliation, global to all days, and cannot be gated to d9+ without new machinery.

## Numbers in this file that are route-sensitive

The specific tiles ((0,3), (0,5), (6,1)), the d15/d16 tour dumps, and anything touching d12/d16
(precomputed days under the old victor-solved routes). The rule-level findings -- no volume
shortfall, top-up displacement risk, the two-cost-model over-budget mechanism, `crop_ops` branch
map -- survive a re-route.

## Verdict

Watering post-d8 is not improvable by planning more water, and the attempt measured as a loss.
The residual watering loss (2-3 tiles/season) is an execution-reliability problem in tour pricing
shared with the spawn-ring family, already documented and owned in the 2026-08-12 docs.
