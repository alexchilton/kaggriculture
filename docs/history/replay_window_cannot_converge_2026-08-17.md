# Why the d5-d11 tape replay cannot converge on his board

Measured 2026-08-17, seed 11, weeds 0.0, `REPLAY_OPENING_DAYS = (5, 6, 7, 8, 9, 10, 11)`.
Both three-quadrant tapes.
Logs: `data/logs/replay_q3_both_tapes_fixed_2026-08-17.log`, `data/logs/replay_failed_ops_2026-08-17.log`,
`data/logs/his_three_tiles_2026-08-17.log`.

## The argument that made this measurable

Inside the replay window the actions are HIS.
So if the tape is his and the replay is faithful, the two boards must converge day for day.
Any mismatch inside the window is a defect, not a strategy difference.
That is what turned a vague "we are behind" into three named tiles.

## What the grid said

Every cell is ours/tape of the same quantity, at the END of that day.

```
=== --tape kawashigi (his MELON season)        d6      d7      d8      d9     d10     d11     d12
melon                                       14/14   20/20   20/20   20/20    11/8    11/8    13/8
strawb                                        2/4     5/7    9/11    9/11    9/11   25/27   28/34
weeds                                         0/0     0/0     0/0     1/0     1/0     1/0     0/0
money  d6 959/957   d8 1433/1431   d10 12374/16162

=== --tape kawashigi_b3 (his STRAWBERRY season)
melon                                       12/12   12/12   12/12   12/12     3/0     3/0     0/0
strawb                                        4/6     6/8   17/19   17/19   17/19   35/37   36/39
weeds                                         0/0     0/0     0/0     1/0     1/0     1/0     0/0
money  d6 1570/1566   d8 1227/1223   d10 13020/16403
```

Strawberry is exactly **-2** every day from d6, in both arms, constant rather than compounding.
Melon is exactly **+3** at d10, in both arms.
Money tracks him to within $4 at d6 and d8, then loses $3.4k at d10 -- the same day as the melon gap.

## The three tiles

Replaying the window and resolving each of his PLANT and HARVEST actions against the board it landed
on gives 5 failures out of 71-73 watched ops, **identical in both arms**:

```
day  h   op       item        tile     before        after
  5 14  PLANT    STRAWBERRY  (0,0)    MELON         MELON      refused
  5 14  PLANT    STRAWBERRY  (1,1)    MELON         MELON      refused
  8 11  HARVEST  -           (3,0)    MELON         MELON      refused
  8 12  PLANT    WHEAT       (3,0)    MELON         MELON      refused
 10 19  PLANT    WHEAT       (3,2)    empty         empty      refused
```

His own board on the same tiles, read from the raw replay at each dawn:

```
 day  (0,0)        (1,1)        (3,0)     (3,2)
   1  WHEAT        WHEAT        WHEAT     MELON
   4  WHEAT        WHEAT        WHEAT     MELON
   5  None         None         WHEAT     MELON
   6  STRAWBERRY   STRAWBERRY   WHEAT     MELON
  11  STRAWBERRY   STRAWBERRY   WHEAT     WHEAT
```

**Our d0-d4 plants MELON on (0,0), (1,1) and (3,0); his plants WHEAT.**
Wheat planted on d1 is ripe and cleared by d5, which is what frees the tile for his d5 h14 strawberry.
Melon planted on d1 stands until about d10.
So his d5 strawberry and his d8 wheat both land on an occupied tile and are refused, and `PLANT` onto
an occupied tile is refused outright -- the divergence is permanent from d5.

One root cause explains both numbers exactly:

- melon `+3` = these three tiles still standing.
- strawb `-2` = two of them were to become strawberry at d5 h14.
- the third, (3,0), was to become wheat at d8.

(3,2) is separate and smaller: the tile is EMPTY on our board when his d10 wheat plant arrives, so the
refusal is not an occupancy problem. Not yet diagnosed; seeds are the first thing to check.

## The fix, and what it measured

`OPENING_GEOMETRY` in `schedule_agent.py` pins the six squares to the crop he sows, seated before the
sweep. Each pin spends its own crop's outstanding count, so the day's totals are untouched -- it is a
permutation of the same plantings. `OPENING_GEOMETRY_LAST_DAY = 4` keeps it out of mid-season.
Test: `tests/test_the_opening_sows_the_fast_crop_where_the_strawberry_goes.py`, red before, green after.

Replay window d5-d11, both arms, seed 11:

```
                          BEFORE (ours/tape)          AFTER (ours/tape)
=== MELON arm            d10     d11    d12         d10     d11    d12
melon                   11/8    11/8   13/8         8/8     8/8   11/8
strawb                  9/11   25/27  28/34       10/11   26/27  28/34
money d10             12374/16162                16242/16162

=== STRAWBERRY arm
melon                    3/0     3/0    0/0         0/0     0/0    0/0
strawb                 17/19   35/37  36/39       18/19   36/37  38/39
money d10             13020/16403                16486/16403
```

Melon is now EXACT at d10 and d11 in both arms; the `+3` is gone.
Strawberry closed from `-2` to `-1`.
Money at d10 moved from $3.4k-$3.8k behind to level.
Refusals inside the window fell from 5 to **1**, the same one in both arms:

```
 day  h   op      item        tile     before   after
   5 14  PLANT   STRAWBERRY  (0,0)    WHEAT    WHEAT    refused
```

The wheat is in the right place now and is not cleared in time.
His (0,0) is already empty at DAWN on d5, so he harvests it during d4 -- our own day.
That d4 harvest is the next defect and it is worth exactly the remaining `strawb -1`.

**Season money is not measurable yet.** `solved_days*.py` was solved on the old geometry and
`_apply_precomputed` keys a stop on `(tile, ops)`, so the swapped squares' stops now drop rather than
adapt. d12-d29 needs re-solving on all four arms before any season total means anything.

## What this does and does not say

- It does **not** say the replay is broken. 71 of 76 of his watched ops succeed.
- It does say the replay's ceiling is set by our own **d0-d4 crop assignment**, which the window does
  not touch. Taping earlier days is the mechanical fix and was measured worse
  (`tape d4-d11` and `tape d3-d11` both 127,185 against 143,454 for d5-d11).
- The interesting fix is the other direction: put wheat rather than melon on (0,0), (1,1) and (3,0)
  in our own d0-d4 rows, so a fast crop frees the tile the way his does. Not measured yet.

## Season money, for the record

Every replay variant still loses on seed 11. Our own d0-d29 banks **153,492**; the best replay window
(d5-d11) banks **143,454**. The replay is a diagnostic here, not a candidate.

## Two bugs found on the way

- `replayed` keyed its tape lookup on `state["branch_armed"]`. Nothing writes that name --
  `MelonBranch.armed_key` is `"melon_armed"` -- so the melon latch was pinned False and the
  strawberry tape was unreachable by construction. The strawberry arm silently replayed his MELON
  season, which is what made the first `kawashigi_b3` grid read `melon 20/12`. Now read through
  `_MB.BRANCH.armed_key` so it cannot go stale again.
- `state["bought"]` kept the discarded planner's purchase increments on replayed turns, handing d12 a
  herd nobody ordered. Snapshotted and restored, then advanced by what the tape actually orders.

## The COW/SHEEP substitution

Built. On a replayed turn the species token in `BUY_ANIMAL`, `PICKUP` and `PLACE` is re-decided by
`_herd_split`, keeping the tape's count, hour and pen. Both species live on a PASTURE, so no pen, walk
or route stop moves; only the bill does, $400 against $500.

On seed 11 it is a **no-op by agreement**: the live branch targets `WOOL_SHOP_NO_YARN_COW = 10` cows
and the season herd is 14, giving COW 10 / SHEEP 4, which is exactly what the tape buys. Forcing the
target to 6 cows relabels d9 and d11 and lands COW 6 / SHEEP 8 with pens and herd size unchanged --
that is `tests/test_a_replayed_day_buys_the_species_the_shops_ask_for.py`, and two of its three tests
go red when the substitution is disabled.

**Caveat that matters:** `breakdown.run` forces the tape's RECORDED shop draw onto both columns, so
under that harness the herd target is pinned by the tape on every seed. The substitution is
structurally invisible in every grid in this document. Measuring it needs a harness with a free town
draw.
