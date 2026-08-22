# The last growing day's water: a real 2 units, and a $19,595 fix

**Status: DIAGNOSED, FIX REVERTED, DO NOT RETRY AS WRITTEN.**
Board: kawashigi, seed 11, `scripts/breakdown.py --tape kawashigi --days 17`.

## The defect is real

`crop_ops` appends WATER before HARVEST and `_live_ops` walks a stop's ops in order, so when both
are offered the sequence is right.
What decides whether the HARVEST is offered is `_one_shot_is_finished`, which reads
`age >= info["max_day"]`.

The water branch above it uses `in_window = (max_day + 1) // 2 <= age <= max_day` — **inclusive at
the top**.
So at `age == max_day` one more water is still worth one more unit, while the gate has already
declared the window shut.
A tour that reaches the tile before its water demolishes a crop with a unit still owed to it, and
the water lands afterwards on bare ground.

Wheat is `max_day 4`; sown on d0 it hits that on d4.
Every one of the seven tiles stands at `yield_units = 3` at d4 dawn.

    ours                                  tape
      h06 (3,2)  3 -> 0   reached first     h08 (4,1)  4 -> 0
      h07 (4,1)  4 -> 0   W h05, H h06      h10 (3,0)  4 -> 0
      h09 (2,2)  4 -> 0   W h07, H h08      h11 (1,4)  4 -> 0
      h14 (1,4)  3 -> 0   never watered     h14 (0,0)  4 -> 0
      h17 (0,4)  4 -> 0   W h15, H h16      h15 (1,1)  4 -> 0
      h18 (1,3)  4 -> 0   W h16, H h17      h16 (2,2)  4 -> 0
      h21 (2,3)  4 -> 0   W h19, H h20      h16 (1,3)  4 -> 0
      total 26                              total 28, every tile full

Five watered-then-harvested tiles bank 4; the two reached first bank 3.
His earliest harvest of the day is h08, after his watering round.

The two units never come back.
The wheat ledger — buys and sells from fills, harvest from board deltas, feeds from ops — closes
exactly against the dawn shed row and holds the gap at 2:

                   d0     d1     d2     d3      d4     d5     d6     d7      d8      d9
        buy       5/8    5/5    4/4    0/0     6/6    2/2    6/6    3/3    5/17   11/11
    harvest       0/0    0/0    0/0    0/0   26/28    0/0    0/0    0/0   11/12    0/0
       sell       0/3    0/0    0/0    0/0     0/0  18/18    0/0    0/0     0/0    8/8
       feed       2/2    4/4    4/4    4/4     5/5    6/6    6/6    8/9    2/10   11/11
       HELD       3/3    4/4    4/4    0/0   27/29    5/7    5/7    0/1   14/20   6/12

We open d7 holding **0 against his 1**, which is why a hand reaches the pen on `(4,2)` at h14 with
`inv_WHEAT = 0` and d7 reads `feed 8/9`.

Note d0 is **not** a loss: his buy 8 / sell 3 and our buy 5 / sell 0 both net +5, `HELD 3/3`.
The buy-9-sell-3 round trip is not a wheat-supply move and should not be read as one.

## The fix, and why it must not be retried as written

Gating the harvest on `watered_today` at `age == max_day`
(`HARVEST_WAITS_FOR_THE_LAST_GROWING_DAYS_WATER`) makes d4 bank 28 and the unit test pass.
It also loses **$19,595**.

    ours before -> after (tape)
      d4 wheat tiles standing     3 -> 6     (3)    harvests deferred, tiles never clear
      d7 buy_product              3 -> 0     (3)
      d8 buy_product              5 -> 4    (17)
      d8 animals                  9 -> 0    (10)    the entire herd starves
      d9 animals                 12 -> 2    (12)
      d16 animals                13 -> 5    (14)
      d16 money             30,585 -> 10,990 (32,566)

A deferred harvest is a tile that does not clear, so it does not replant, so the wheat pipeline
stalls, so the shed never refills, so every animal misses two consecutive feeds and is removed
(`kaggriculture.py:804`).
One unit of yield was traded for the herd.

**The lesson is the coupling, not the gate.** HARVEST is not only a collection here; on a one-shot
it is a demolition that frees ground, and the ground is on the critical path for the next sowing.
Any rule that delays a harvest has to be measured against the replant it blocks, not against the
units it collects. The same trap is already recorded one level up in `_one_shot_is_finished`'s own
docstring, where forcing harvests *earlier* late in the season also measured negative.

If this is retried, the shape to try is **ordering without delay** — reach the tile earlier, or make
the tour water before it harvests within the same visit — never withholding the HARVEST op.
