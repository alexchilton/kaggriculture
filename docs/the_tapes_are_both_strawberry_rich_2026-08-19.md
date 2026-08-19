# Both kawa tapes are strawberry-RICH boards, so neither can measure the strawberry float

Measured 2026-08-19, straight off the two replays we build on, counting standing crop tiles at dawn
and the strawberry-carrying shops unlocked at that moment.
No agent involved -- this is his own board in his own game.

Strawberry-carrying shops are `BRUNCH_SPOT`, `ICE_CREAM_SHOP`, `SMOOTHIE_SHOP`, `FARMERS_MARKET` --
four of the eight types.

## `92466371`, the strawberry arm (seed 70683142)

```
  d8    straw 8    wheat 3    melon 12   | straw-shops 2 of 2
  d10   straw 19   wheat 5    melon 12   | straw-shops 3 of 3
  d12   straw 37   wheat 17  melon  0   | straw-shops 4 of 4
  d14   straw 42   wheat 18  melon  0   | straw-shops 4 of 4
  d16   straw 38   wheat 12  melon  0   | straw-shops 5 of 5
  d20   straw 38   wheat 22  melon  0   | straw-shops 6 of 6
  d29   straw 1    wheat 14  melon  0   | straw-shops 7 of 8
```

## `92498144`, the melon arm (seed 1240813987)

```
  d8    straw 7    wheat 3    melon 20   | straw-shops 2 of 2
  d10   straw 11   wheat 5    melon 20   | straw-shops 3 of 3
  d12   straw 27   wheat 17  melon  8   | straw-shops 3 of 4
  d14   straw 34   wheat 17  melon  8   | straw-shops 3 of 4
  d16   straw 32   wheat 16  melon  8   | straw-shops 5 -> 3 carry straw
  d20   straw 31   wheat 28  melon  0   | straw-shops 4 of 6
  d29   straw 3    wheat 11  melon  0   | straw-shops 6 of 8
```

## What this means

**The tapes are not neutral ground for this question.** Both draws are strawberry-heavy: the
strawberry arm has all four of its first four shops carrying strawberry, and the melon arm three of
four. On those boards 37-42 strawberry tiles is the *correct* allocation, and it is what he plays.

Cross-checked against tetsuya's 79 seats, which key the allocation on strawberry-draining shops
visible by d12:

```
  straw-shops   0 -> 25.5 tiles   1 -> 26.4   2 -> 34.9   3 -> 36.4   4 -> 36.8
  wheat         0 -> 28.0         1 -> 21.8   2 -> 21.3   3 -> 19.0   4 -> 18.0
```

At 4 shops he plants 36.8 and kawa plants 37-42.
The two leaders agree, and our 42 is very close to right **on these two boards**.

So the flood we measured is not "we always plant too much strawberry".
It is that we plant 42 on *every* board, including the ~31% of draws with 0-1 strawberry shops where
both leaders plant 26.
Strawberry halves at 31 units above `I0`, so on a thin board 42 tiles is dumping into a book that
physically cannot take it -- and that is the case neither tape contains.

## Consequence for how the float gets judged

- On the strawberry arm a d12 cap of 37 trims 5 tiles. Small, and the right direction.
- On the melon arm (3 shops, target 36.4, we plant 34) it trims **nothing** -- a structural null,
  not a measurement.
- The change is aimed at boards that appear in neither tape. **A tape-arm A/B cannot validate it**,
  and a null there must not be read as the change being worthless.

It therefore needs a fresh-seed sweep with varying shop draws, scored on **win rate** over paired
seats -- which is exactly the instrument that correctly killed the unconditional carrot and tomato
arms, where mean money rose and win rate fell.

## MEASURED AND REVERTED: the float loses $28,259, and the reason is the solved routes

Implemented as `STRAWBERRY_TILES_BY_DRAIN = (26, 26, 35, 36, 37)` keyed on strawberry-draining shop
instances, floating from d12, capping `want["STRAWBERRY"]` in `_refresh_pins` and never retro-cutting
standing ground.
Measured against the seed-cap baseline `b35feee`, same harness, all four arms:

```
              baseline    with float    delta      strawberry   wheat
  straw_q3     155,601      145,048    -10,553      42 -> 37    124 -> 120
  melon_q3     139,453      139,453          0      34 -> 34    134 -> 134
  q4_melon      93,929       78,594    -15,335      34 -> 30    133 -> 125
  q4_straw      78,305       75,934     -2,371      42 -> 38    128 -> 124
```

Three losses, one structural null, **-$28,259 in total**. Reverted.

**The mechanism is in the wheat column, and it is not a tuning miss.** Cutting strawberry did not hand
the ground to wheat -- wheat went DOWN on every arm that moved (124->120, 133->125, 128->124). We lost
the strawberry tiles *and* wheat tiles. Strawberry seed also sat unsown in the shed, $400-$500 an arm,
because the purchase was already committed before the cap declined the pin.

The SUSPECTED cause is the precomputed route tables. They are solved for days 12-23 **against the
schedule's own crop counts**, and `_apply_precomputed` keys every stop on the exact `(tile, ops)` tuple;
a miss demotes the job to `_insert_leftovers`, which needs slack the day does not have. Changing the crop
mix after d11 would then desynchronise the day from the route solved for it.

**This mechanism is NOT established, and the one isolation test run so far points the other way.**
Recorded here because the first version of this doc asserted it as fact.

The isolation is a 2x2: drop the solved routes (`cover.UNSOLVE_DAYS = range(12, 30)`) and then add the
crop change. If route conflict is the cause, the change should do BETTER with the routes gone.

```
  straw_q3            routes ON    routes OFF
    tomato 0           155,601      150,291      -5,310 = the cost of losing the routes
    tomato 1           154,484      137,135
    tomato delta        -1,117      -13,156      <- WORSE without routes, not better
```

So on the strawberry board tomato's loss is real crop economics -- 0 tomato-draining shops at d12 -- and
not route desync. The route hypothesis is refuted for tomato on this arm.

`melon_q3` returned **byte-identical** money on both route settings (139,453 at tomato 0, 145,145 at
tomato 1, either way), so that arm's override never took: the melon/q4 branch resets `UNSOLVE_DAYS`,
which is the trap `q4_branch`'s own note warns about -- "an A/B there that reads byte-identical means
the reset line was left in". That half of the 2x2 is a non-experiment and nothing may be read from it.

**The strawberry isolation has NOT been run.** For strawberry the only evidence is the wheat column
above, which is suggestive and not decisive.

## What has to happen before any crop mix can be tested

Solving the routes for 42 strawberry and then planting 37 measures the MISMATCH, not the allocation.
So the order is:

1. Choose the target mix (tetsuya's table, or a swept variant).
2. Re-solve all four tables -- `solved_days`, `solved_days_q4`, `solved_days_straw`,
   `solved_days_straw_q4` -- against that mix, days 12-23.
3. A/B mix-vs-mix, each running on its OWN routes.
4. Score on paired-seat win rate, not money. That is the instrument that correctly killed the
   unconditional carrot and tomato arms, where mean money rose and win rate fell.

Until step 2 exists, every crop-mix number on the tape arms is confounded by the route tables, and a
loss there is not evidence the allocation is wrong.

The same confound applies to `WHEAT_TILES_TO_CARROT` and `WHEAT_TILES_TO_TOMATO`, which rewrite
`sched[day]` rows from `LATE_CROP_FROM_DAY = 12` -- inside the solved range.

## Tomato, for the record

Measured against the seed-cap baseline, one tile from `LATE_CROP_FROM_DAY = 12`:

```
              baseline   tomato=1    tomato=2    tomato-shops at d12
  melon_q3    139,453     +5,692      -3,178     1  (FARMERS_MARKET)
  straw_q3    155,601     -1,117      -4,365     0
  q4_melon     93,929    -11,655      -2,134     0
  q4_straw     78,305     -1,031        +836     0
```

The gate suggested by the top row -- plant tomato only where something drains it -- would score
+$5,692 on the one qualifying arm and change nothing on the other three.
**Not shipped, because it rests on a single board whose own sign flips at two tiles.** A +$5,692 that
becomes -$3,178 when one more tile is added is not an effect that can be sized, and n=1 with an
unexplained sign flip is exactly the shape of the confounded results this project has been burned by.
It needs the re-solve above, then fresh seeds with varying tomato-shop draws, scored on win rate.

## Timing constraint from the taped opening

d4-d11 are replayed from the tape, so the opening's strawberry is committed whatever the draw says:
37 of 42 tiles are already standing at d12 dawn on the strawberry arm.
A float can only ever move what is left after d11.
Reaching the 26-tile behaviour on a thin board would mean changing the taped opening, which is out
of scope -- the tape is the basis by instruction.
The honest ceiling for a post-d11 float is therefore the last few tiles, plus the replant decisions
from d12 on.
