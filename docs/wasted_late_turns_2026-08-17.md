# Late-game turns that could have been harvesting

Measured 2026-08-17 on `~/Downloads/93880775.json`, a fresh ladder download not yet mirrored into
`data/seed_scripts/ladder_2026-08-17/`.
`info.TeamNames = ['BSam79', 'alex chilton']`, so our seat is **1**.
720 steps, `day = i // 24`, `hour = i % 24`.

## The answer: yes, and one case is unambiguous

**On d28 a hand stood directly on top of a 3-unit ripe WHEAT tile `(9,1)` for seven consecutive
hours -- h14 to h22, Manhattan distance 0 -- emitting PASS every hour.**
Not near it. On it.

On d29 at h23, the final hour of the season, **all 8 hands were idle while 18 units stood on the
field**.

## Per-day, our seat, unit-turns from `action['hands']`

    day  unit-turns   work   movement   idle(PASS)   dawn standing
    25      252        141      111          0            119
    26      252        127      124          1            116
    27      252        122      129          1            134
    28      231        116      101         14            107
    29      186         59      106         21             49

Idle is ~0 through d27 then jumps on d28-d29 as the crew draws down (11 -> 10 -> 8 hands).

## Reachable and unharvested

Feasibility test: `hours_left = 24 - hour >= 2 * distance`, i.e. time to walk there and take it.

35 idle hand-hours across d28+d29; **20 of 35 were feasible**.
Deduplicated by `(day, tile)`:

    day  tile     kind           units
    28   (4,6)    WHEAT            1
    28   (9,1)    WHEAT            3
    29   (2,4)    COW pasture      3
    29   (4,6)    WHEAT            2
    29   (5,3)    COW pasture      2

**11 units reachable-and-unharvested. 7 of them were still standing at the actual close** -- the
d29 `(4,6)` wheat and both cow pastures, `(2,4)` and `(5,3)`, never milked.
The d28 `(9,1)` wheat was taken during d29, so it was a delay rather than a final loss.

Total end-of-game standing produce for our seat in this replay was **18 units**; the 7 above are the
subset directly attributable to an idle hand that had the time budget and did not go.

## A separate defect found on the way, NOT counted above

**At hour 1 of every day in d25-d29, `action['hands']` is an empty list while `farm['hands']` shows
10 positions still on the board** (d29: 8), and `action['market']` fires 10 HIRE orders in the same
turn.
So those hands do nothing that hour, without even an explicit PASS.

This is systematic on every day, not a late-game effect, so it was excluded from the harvest numbers
above.
At ~10 hands x 30 days it is on the order of 300 unit-turns a season.
It has not been diagnosed and should be looked at on its own.

## Data-shape trap, recorded because it produced a wrong map first

`farms[seat]['tiles']` is indexed **`tiles[y][x]`**, row then column, per the engine's own comment at
`kaggle_environments/envs/kaggriculture/kaggriculture.py:145` and `_apply_unit_action`
(`fx, fy = pos; tile = farm["tiles"][fy][fx]`).
Hand and farmer positions are stored `[x, y]`, the other way round.

The first pass used `tiles[x][y]` and produced a plausible but wrong tile map.
It was caught with a LOCKED-tile consistency check: `tiles[y][x]` puts all LOCKED hits on the four
legitimate shed-adjacent tiles `(4,4) (5,4) (4,5) (5,5)`, while `tiles[x][y]` produced 260 hits,
most of them bogus.
