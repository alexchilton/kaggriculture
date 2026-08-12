# Day 18: the harvest gap and the sell gap are cadence. One real deficit: FERTILIZER.

Diagnosis by Fable, 2026-08-12, read-only, in `breakdown.py`'s OWN harness.
Script `<scratchpad>/diag_d18.py`, log `data/logs/diag_d18_sell_harvest.log`.

## Why this run is trustworthy where two earlier ones were not

Twice on 2026-08-12 a hand-rolled comparison seated the tape opposite our own agent.
`breakdown.run` plays BOTH sides as seat 0 against the SAME opponent, so those runs were a different
game and their numbers did not describe the grid.
This run copies `breakdown.run`'s loop exactly, installs the d12/d16/d18 routes, confirms
`PRECOMPUTED_MISSES == []`, and **reproduces the stated grid cell for cell**: d18 harvest 11/14,
water 53/54, feed 12/12, care 12/12, fertilize 4/4, sell 35/61, money 25596/22551.

## Q1 — `harvest 11/14` is NOT three missing harvests. We took them on d17.

    tape 14 = 8 pens (4 SHEEP yield 4, 4 COW yield 3) + 6 STRAWBERRY (planted d6 x1, d7 x3, d8 x2)
    ours 11 = 8 pens (the same 8)                     + 3 STRAWBERRY (planted d6 x1,          d8 x2)

The three extra are the tape's d7-cohort strawberries at `(7,2) (8,2) (9,2)`, each holding
`yield_units = 2` produced at **dawn d17** — STRAWBERRY is `first_yield_day 10, interval 2`, so a d7
planting yields on d17 and again on d19 (`reference/kaggriculture.py:778-789`).
The tape's d17 tours reached only 7 of its 10 d7-cohort tiles, so three carried their units overnight.

We harvested **all ten** of ours on d17 (our d17 harvest is 22 ops against the tape's 18), so at dawn
d18 the whole cohort reads `yield_units = 0` and `crop_ops` correctly offers nothing
(`kagg/search/router.py:705`, `held > 0` fails; the env would refuse it anyway at
`reference/kaggriculture.py:436`).

**Cumulative d16-d18 harvest ops are exactly 46/46.** Strawberry units over d17+d18: ours 40, tape 39.
The tape is a day behind on those tiles and catches up on d18. There is nothing to fix.

The crops both sides leave standing at d18 h23 are MELON planted d10/d11 — age 7-8 against
`first_yield_day 10`, genuinely unharvestable (`:440`) — and filling WHEAT planted d15-d17, which the
tape also leaves.

## Q2 — `sell 35/61` is the mirror of `sell 90/39` on d17.

Both sides follow the same schedule row, so "the row asks for less" is false by construction.
Exact fills from `_commit_unit` via `kagg/analysis/fills.py`, seat 0, ours/tape:

    day    total    STRAW    MILK    WHEAT    FERT    WOOL
    d16    52/56    14/14    18/21   13/13    7/0     0/8
    d17    90/39    16/2     27/3    38/25    9/9     0/0
    d18    35/61    20/27    3/18    0/8      0/8     12/0
    d19    31/45    8/25     18/3    1/1      0/0     4/16

**Cumulative SELL units at the end of d18: ours 499, tape 489.** Money 25596/22551, we are $3,045 up.
The d18 deficit of -26 is the mirror of the d17 surplus of +51.

The mechanism is our own late-sell bias (`LATE_SELL_FROM_HOUR = 16`,
`kagg/search/schedule_agent_1455mh.py:2278/2282`). The tape posts the row at h0 against a dawn shed
still holding yesterday's production; we sell late on the same day and sweep our own production as it
lands. So our dawn-d18 shed holds only STRAW 20 and MILK 3, which is exactly what we offer — and
**every unit we offered on d18 filled**. WOOL 12/0 is `CUMULATIVE_SELLS` retrying the d16 row; wool
reconciles to 84/84 by the end of d19.

### The one genuine deficit: FERTILIZER 0/8

Our shed held 9-13 fertilizer all through d18 and the row asks for 8, but the sell reserve
(`FERTILIZER_RESERVE_LOOKAHEAD_DAYS = 1`, `:2937`, applied `:3492-3499`) computes
`want = max(today, tomorrow)` tiles offering FERTILIZE = **12**, so `have = max(0, 9 - 12) = 0` and
nothing is offered. The tape sells its 8 at d18 h23 and still fertilizes 12 on d19.

Cumulative FERTILIZER is -8 at the end of d18 and **still -8 at the end of d19** — the only
per-product deficit in the window that does not reconcile.

Whether releasing it is safe is NOT established. The comment at `:3480-3490` records d16 firing 6 of
12 FERTILIZEs when the shed was starved, which is why the reserve exists. Diagnosis only.

## Side observation, not investigated

On d18 our agent buys a COW where the schedule row says `SHEEP 1`
(fills: ours `BUY_ANIMAL:COW 1`, tape `BUY_ANIMAL:SHEEP 1`).
