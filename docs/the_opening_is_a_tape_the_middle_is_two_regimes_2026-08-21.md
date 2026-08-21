# The opening is a tape. The middle is two regimes, not one.

Measured 2026-08-21, カワシギ, 213-226 game-seats depending on the cut.

## 1. d0-d12 is EXACT, and the fix was one line

```
REPLAY_OPENING_DAYS = ()   ->   (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
```

`scripts/breakdown.py --tape kawashigi --days 30 --diff`, seed 11, weeds 0.0, shop draw injected
from the recording:

```
per-day differing cells
  d0..d12   0 0 0 0 0 0 0 0 0 0 0 0 0
  d13..d29  10 11 11 13 12 11 11 11 14 14 14 15 15 12 16 16 10
```

Alex, repeatedly, and he was right every time: *"there is nothing in the logic to change or decide
we are using the tapes"*, *"there are NO problems till d12"*.

**A whole day went into debugging days that contain no decisions.** d0's market-order priority,
d1's fertilizer cadence, d2's $2, d3's early wheat harvest — every one of them was our planner
ranking things on a day whose content is fixed. `_replay_opening` sends his own actions and none of
them arise. Two agent sessions and four code changes were spent on defects that do not exist when
the tape is played.

The machinery was already built and had been **disarmed on 2026-08-20 for a reason that no longer
applied** — the agent was then pointed at tetsuya while replaying カワシギ's turns, which is
incoherent. That reason is preserved above the constant. It goes back to `()` if the agent is ever
pointed at tetsuya again.

Verified on ONE of four branches: `(False, False)`, the melon three-quadrant tape `92498144`.
`(True, False)`, `(False, True)` and `(True, True)` are **untested**.
`(True, True)` points at a three-quadrant tape, which was safe while the window ended at d11 and is
now questionable, since the q4 tape buys its fourth parcel during d12.

## 2. The decision tree is TWO binary reads, both already implemented

```
d3   melon_branch   opponent melon tiles >= 9    -> strawberry line   0 misclassifications / 67 games
d6   q4_branch      YARN_STORE unlocked by d6    -> four quadrants    fires on 15 of 100 seeds
```

Four combinations, four tapes, replayed verbatim. There is no classifier to fit and no library to
select from for the opening. Every class-count table computed for d0-d12 this session was answering
a question the architecture does not ask.

`q4_branch` has never measured as a gain — its own docstring records `-$4,626` mean on own routes,
`+$465` on live routes, `-$2,749` on unselected seeds. It is armed on Alex's judgement.

## 3. The middle is two regimes

Depth-3 tree, dawn board only, `my_seed_*` features dropped, split by GAME, baseline is the TRAIN
majority scored on held-out games. 64 held out.

```
 day |     sets     base     tree    gain |    multi     base     tree    gain
  13 |        3    68.8%    96.9%  +28.1 |       20    25.0%    70.3%  +45.3
  14 |        2    92.2%    95.3%   +3.1 |        6    31.2%    73.4%  +42.2
  15 |        1   100.0%   100.0%   +0.0 |       12    23.4%    59.4%  +35.9
  16 |        1   100.0%   100.0%   +0.0 |       10    37.5%    50.0%  +12.5
  17 |        2    82.8%    96.9%  +14.1 |       12    18.8%    46.9%  +28.1
  18 |        2    98.4%    98.4%   +0.0 |       21    25.0%    48.4%  +23.4
  19 |        2   100.0%   100.0%   +0.0 |       14    20.3%    20.3%   +0.0
  20 |        2    98.4%    96.9%   -1.6 |       12    28.1%    28.1%   +0.0
  21 |        4    64.1%    70.3%   +6.2 |       41     4.7%     6.2%   +1.6
  22 |        2    68.8%    75.0%   +6.2 |       42     4.7%     1.6%   -3.1
  23 |        2    75.0%    76.6%   +1.6 |       31    20.3%    17.2%   -3.1
  24 |        2    60.9%    62.5%   +1.6 |       37     7.8%     6.2%   -1.6
  25 |        2    76.6%    75.0%   -1.6 |       51     1.6%     1.6%   +0.0
  26 |        2    57.8%    60.9%   +3.1 |       44     0.0%     3.1%   +3.1
  27 |        1   100.0%   100.0%   +0.0 |       17    10.9%    21.9%  +10.9
```

**The COUNT is learnable d13-d18 and dead from d19.** +45, +42, +36, +13, +28, +23, then nothing.

**WHICH crops is nearly free.** d15, d16, d19 and d27 are a single class; d14, d18, d20 are
92-100% baseline. Only d13 has a real crop choice the tree wins (68.8% -> 96.9%). The d21-d26 gains
of +1.6 to +6.2 on 64 games are noise and must not be acted on.

### This RECONCILES the capacity finding rather than contradicting it

`docs/the_middle_is_not_board_capacity_2026-08-21.md` measured `corr(wheat, free_tiles_at_dawn) =
0.274` pooled over d14-d27 and concluded the count is turn-bounded, not chosen. That measurement
was correct and its conclusion was **pooled over fourteen days of which six carry real signal and
eight carry none**. Same trap as the `farm:0.445` per-opponent win rate: an aggregate over a unit
that is not uniform.

The d13 rule, board-only, depth 3:

```
my_empty <= 5.5
   my_shed_WHEAT <= 29.5          -> straw+wheat
   my_shed_WHEAT 29.5-34.5        -> wheat
   my_shed_WHEAT >  34.5          -> straw
my_empty > 5.5
   my_crop_STRAWBERRY <= 41.5
      my_shed_FERTILIZER <= 24.5  -> straw+wheat
      my_shed_FERTILIZER >  24.5  -> straw
   my_crop_STRAWBERRY >  41.5     -> wheat
```

With `my_seed_*` included the tree reaches 98.4% on `my_seed_STRAWBERRY` alone — but that seed was
bought on d12, so it reads a decision already paid for. Dropping the seed features costs 1.5 points,
which is the evidence that the board carries the information independently.

## 4. Where the season is actually lost

Full 30-day grid from an exact d12 handover, ours minus tape:

```
season money  -11,544        wheat  -89 tiles      sell   -126
work   +236   move  -315     idle   +171           buy_product -108
```

We do more work in a smaller radius, hold 89 fewer standing crops, trade far less, and **sit idle
171 more unit-turns than he does**. d22 alone is -$4,508 on `sell -72`.

d13-d18 — the over-planting window — is exactly where a tree can supply the count.

## Not established

- Three of four tape branches untested at d12.
- One seed, one opponent, one shuffle of the holdout. The +40s are clear of noise; the +1.6s are not.
- Whether feeding the tree's count to the planner actually fixes the 158-vs-112 over-planting.
  Proposed, not measured.
- The season grid is our SHIPPED agent against the tape's own game. It says nothing about a
  contested market against a different opponent.
