# The optimal carrot, measured — 2026-08-24

Alex had asked for this for days and kept getting diagnostics instead.
This is the grid.

Script: `scripts/the_optimal_carrot.py`.
Rows: `data/logs/optimal_carrot.csv`, `data/logs/optimal_carrot_big.csv`.

## Board

Ladder game **98495047**, seed 1640915609, lost to SOUTA Sakurai by **$29,384**.
Town drain 11 for CARROT — five `PET_CAFE` (single-product, 2/tick each) plus `FARMERS_MARKET`.
CARROT closed at **$517**.
This is the deepest carrot book in any game we hold: drain 11 appears in 2 of 118 games (1.7%).

## Method

Both tapes replayed verbatim to the d20 handover, so the board, the bank and the town's book are
the recorded ones, then our agent plays out.
Prices are endogenous — the same seed paid $270 for milk in a recording and $1 in a rematch — so a
re-sim from turn 0 would measure a different market.

An arm sets the first day the planner rewrites a scheduled `PLANT WHEAT` into `PLANT CARROT`, and
the total tiles it may convert.
`corner_the_book.plan` is replaced by the arm, otherwise the gate would size the position itself and
no arm would differ.

## The grid

`margin / carrot units held at d29 dawn`.

```
 tiles              d21              d23              d25              d27
     0      -25,191/  6      -25,191/  6      -25,191/  6      -25,191/  6
     8      -23,822/  6      -21,694/  6      -21,541/ 13      -23,161/  6
    16      -18,512/  3      -15,722/  6      -23,556/ 22      -21,185/  6
    24      -13,422/  3      -13,985/ 26      -19,923/ 26      -19,942/  6
    32       -9,473/ 12      -12,827/ 31      -18,696/ 26      -19,942/  6
    40       -7,197/ 27       -9,711/ 31      -15,290/ 26      -19,942/  6
```

Extended past the 40 cap, same handover:

```
 tiles              d21              d22              d23
    40       -7,197/ 27      -11,422/ 41       -9,711/ 31
    48       -4,155/ 39      -11,579/ 38       -9,735/ 31
    56       -2,086/ 42      -10,077/ 41       -7,907/ 31
    64       -4,210/ 42       -7,686/ 41       -6,480/ 31
```

**Optimum: 56 tiles from d21 → −$2,086, worth +$23,105 over planting none.**

## What it does not do

**It does not flip the game.** −$2,086 is still a loss. 79% of the gap, not 100%.

## What the shape says

- **Start day dominates count.** d21 beats d22 and d23 at every size. d27 is flat at −19,942
  regardless — too late for anything to ripen (CARROT is `first_yield_day 2`, `max_yield_day 3`).
- **d25 at 16–24 tiles LOSES** relative to 8 tiles, and leaves 22–26 units standing at d29.
  Converting late and wide plants a crop that cannot be collected and sold in time.
- **The conversions saturate.** 56 and 64 both end at 42 units held, so the real policy is
  "convert everything the schedule offers from d21"; the 56-vs-64 money difference is what else got
  planted, not more carrot.
- SOUTA reached 32 tiles and won. The optimum here is bigger than what beat us.

## Caveats that limit the number

- **The harness is kind to us by $4,193 before any arm acts.** The 0-tile baseline is −25,191
  against a recorded −29,384: our agent playing d20→d29 outscores what we actually did.
  Only the paired difference between arms is safe to read.
- **One board.** Drain 11 is 1.7% of games. Nothing here says what this policy costs on the
  drain-2/3 towns that are 45% of the field, and a rule this aggressive must be measured there
  before it can ship.
- The arm forces a tile count directly. A shipped version has to *decide* that count from the
  board, which is what `corner_the_book.plan` is for — and its current sizing pinned at the old
  `max_tiles=40` cap on this board, i.e. below the measured optimum.
