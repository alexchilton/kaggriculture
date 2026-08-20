# The tape dies at d13, and the unit slot is why

Measured 2026-08-20 on kawashigi, 191 downloaded games, holdout `94439800`, full 30-day seasons in
the real environment.
Scripts: `scripts/why_the_clone_is_poor.py`, `scripts/clone_play.py`.
Logs: `data/logs/why_clone_poor2.log`, `data/logs/kawa_tape_control.log`, `data/logs/kawa_4arms.log`.

## The headline

The `(day, hour, unit)` tape clone matches the teacher's op counts to 6.5% and banks **$22,592
against his $153,443**.
It is exact through d18 and then flat.

    day    clone $     teacher $
    d11     17,419       17,025      clone AHEAD
    d16     27,757       24,705      clone AHEAD
    d18     35,977       35,321      level
    d19     40,141       44,712      breaks
    d24     43,395       91,154
    d29     42,976      139,400

$2,835 earned across d19-d29 against his $94,688, and the bank FALLS on d24-d26.
Falling money means the farm is paying crew rent and producing nothing.

## The cause is unwatered crops, not spawned weeds

    day    clone board                    teacher board
    d12    crop 53  weed 0                crop 54  weed 0
    d13    crop 53  weed 2                crop 55  weed 0
    d15    crop 45  weed 11               crop 56  weed 1
    d17    crop 27  weed 26               crop 58  weed 0
    d18    crop 18  weed 34               crop 51  weed 1
    d29    crop  1  weed 48               crop  3  weed 17

`weedSpawnChance` is 0.005 for both seats in the same game, and the teacher holds 0-1 weeds until
d28.
Every one of our 48 weeds is a water we missed: two days unwatered turns a tile into WEED
(`kaggriculture.py:771`).

The seeds confirm the second half of the loop.
PLANT needs EMPTY, so once a tile weeds over the tape's later plants on it fail and the bought seed
has nowhere to go:

    day    clone seeds                        teacher seeds
    d15    WHEAT  5, CARROT 8, STRAW 1        CARROT 8, WHEAT 7
    d17    WHEAT 18, CARROT 8, STRAW 1        CARROT 8, WHEAT 8
    d18    WHEAT 20, CARROT 8, STRAW 1        CARROT 8, WHEAT 8

He buys and plants the same day and holds a steady 8.
We buy at the same hours and stack to 20.

**The chain:** phase drift by d12 -> WATER fires on the wrong tile -> tiles go two days dry ->
WEED -> PLANT blocked -> seeds stack, crops collapse 53 to 1 -> production stops, wages continue.

**Nothing changes in the tape at d19.** The rot starts at d13, right after the third quadrant opens.
d19 is only where the money finally goes flat.

## The 6.5% op figure never measured execution

`clone_play.py` counts ops from the action dict BEFORE `env.step`, and the teacher's column comes
from his recorded actions.
Both sides are *requests*.
A HARVEST on a bare tile, a FEED with no wheat carried and a PLANT onto a weed all score as matches.

The op NAMES match. The tile ARGUMENTS do not. That is the whole of the $131k gap.

This is the ROUTER / PLAN / EXEC distinction from `CLAUDE.md` reappearing inside the grader.
Any future op-fidelity number must be read off the board after the step, not off the action dict.

## The unit slot is not stable between games

The arm-vs-arm tape diff read 42-55% of slots differing, almost all of them moves.
The control says that number is meaningless:

    within-arm, 47 v 47 games, 5 random splits    17.2  18.1  17.9  19.6  22.0 %
    arm vs arm                                    42.1  51.8  55.2 %
    two INDIVIDUAL games, same arm                35.7  61.5  48.0 %

Two games in the SAME arm differ on up to 61.5% of slots -- more than the arm-vs-arm figure.
The examples say why:

    d0  h4  u4   BUILD_PASTURE   ->  WEST
    d0  h4  u5   WEST            ->  BUILD_PASTURE
    d11 h3  u3   PICKUP COW 1    ->  PICKUP SHEEP 1
    d11 h11 u3   PLACE COW 1     ->  PLACE SHEEP 1

The same two jobs, swapped between units 4 and 5.
Hands are indexed in hire/arrival order, which varies between games, so `u` conflates "which hand"
with "what job".

**This is not only a measurement problem.** The modal tape averages over unit permutations, so the
action at `(day, hour, u)` can be drawn from games where unit `u` was on a different tour.
The clone therefore walks a blend of two incompatible tours.
A chunk of the phase drift that kills the board at d13 is baked in when the table is built, not
accumulated during play.

**Next test:** canonicalise the unit index by job or spawn position rather than hire order, rebuild
the tape, and re-measure the weed curve.
Cheap, and it is the only candidate so far that could push the safe range past d12.

## The arms are two binary decisions, at d6 and d12

    arm                    n    median $      min $      max $
    melon-12  no q4       94      86,974     39,905    161,918
    melon-20  no q4       45      91,981     47,303    153,443
    melon-12  q4 on d12   32     103,431     50,745    142,761
    melon-20  q4 on d12   20     100,577     58,028    127,151

    land days      139 games [6, 11]     52 games [6, 11, 12]
    late animals   139 games none        52 games {SHEEP: 2}

Cumulative melon planted, by day:

    day    melon-12 arm   melon-20 arm
    0-5           12.0           12.0
    6             12.0           14.0
    7             12.0           19.6
    9             12.0           20.0

Every game is identical to d5.
The melon branch opens on **d6**; the land branch opens on **d12** and always bundles the fourth
quadrant with two late SHEEP -- never one without the other.
Everything else is +/- 1-2 plants of jitter, which is what made an exact-count grouping produce a
spurious 31 trunk signatures and 150 late ones.

At the branch itself the melon arm is two plants on one unit:

    d6  h18 u4    PLANT STRAWBERRY  ->  PLANT MELON
    d6  h21 u4    PLANT STRAWBERRY  ->  PLANT MELON

We currently ship the **weakest** of the four lines (melon-12 / no q4, $86,974 median).
The q4 arm is worth about **$15k of median bank** and is the later, easier decision.

## What this constrains

- An open-loop tape has a shelf life of about **twelve days** on a board it did not create. This
  independently re-derives the d12 handover the shipped agent already uses.
- The d6 melon branch is inside the safe range. The **d12 q4 branch sits exactly at the edge**: the
  tape can make the decision but cannot execute the eighteen days after it. An extra quadrant with
  no closed-loop watering is just more tiles to weed over.
- Perturbing the tape is not a local edit under a `(day, hour, unit)` key. Position is an output of
  the sequence, so changing one plant invalidates every later route slot.

## Caveats

- One holdout game, one arm (7 games within 0.02, table built from 5). The weed curve has not been
  repeated on a second holdout.
- `configuration.seed` is `None` in every downloaded replay, so `env.reset()` draws a fresh seed.
  The start board is fixed but shop-unlock timing is not: our town diverges from the teacher's at
  **d6** and shares almost nothing with it by d24. Money tracked his exactly through d18 despite
  that, so the shop draw is not what kills d13 -- but it is uncontrolled, and any late-season money
  comparison inherits it.
- The `hands` column in the first version of this trace was sampled at hour 0, when crew is rented
  and not yet hired, and read 0 for both sides all season. It is sampled at hour 12 now. The same
  mistake was made once before in `money.py`.
