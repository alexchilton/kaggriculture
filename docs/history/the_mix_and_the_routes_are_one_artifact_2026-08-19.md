# The crop mix, the herd and the routes are ONE artifact

2026-08-19.
The single most expensive lesson of the day, confirmed independently four times.

`_apply_precomputed` keys every stop on `(tile, tuple(op_names))`.
A day whose work has changed no longer matches the route solved for it, the stop is demoted to
`_insert_leftovers`, and `_insert_leftovers` needs slack the day has not got.
So **any change to what the units DO must be measured against routes re-solved for it**, or the number
is measuring the mismatch and not the change.

The tell is an implausible magnitude.
No single tile and no single animal is worth $10,000, so a swing that size is a mismatch, not a
finding.
The second tell is the PLANTS column moving when only the shed should have.

## What it cost, and what it was worth once matched

| change | against old routes | against re-solved routes |
| --- | --- | --- |
| strawberry cap, straw arm | **-$10,553** | **+$4,022** |
| melon arm, no crop change at all | -- | **+$5,615** |
| 1 tomato tile, straw arm | -$1,117 | included above |
| 1 tomato tile, melon arm | -$3,880 | still negative, tile removed there |
| 2 geese, straw arm | -$62,866 | **-$63,417** (NOT rescued -- see below) |

The melon row is the important one: **its crop mix did not change at all**.
Strawberry stayed at 34, no tomato, cap never binds (3 drains -> cap 36, it plants 34).
The whole +$5,615 is route staleness -- the tables had been solved against an older schedule and had
drifted.
Any arm carrying stale routes is paying this silently.

## Route seating, measured

`cover.PRECOMPUTED_MISSES` counts stops that did not seat.
Straw arm after re-solving d12-d23: **19 skipped over twelve days**, with d12, d16 and d21 perfect.
q4_melon before its closing days were re-solved: **0 skipped in d12-d22 and 138 in d24-d29**, which is
where its -$12,308 came from -- `q4_branch.install` resets `cover.UNSOLVE_DAYS` to `()`, so the
four-quadrant arms run precomputed routes right through d29 while the three-quadrant arms hand the
close to the greedy.

## Shipped, and why the four-quadrant arms were left alone

Each arm uses a different end of tetsuya's drain-keyed strawberry table, and only the high end survived:

```
 arm        quads  straw-drains  cap  row   delta      verdict
 straw_q3     3         4         37   42   +4,022     binds, GOOD
 melon_q3     3         3         36   34   +5,615     never binds
 q4_straw     4         0         26   42     -214     binds hard
 q4_melon     4         0         26   34   -9,560     binds hard, worst arm
```

Both four-quadrant boards draw ZERO strawberry shops and so take the table's low end, where cutting
costs about $2,400 a tile.
tetsuya's 25.5 tiles at zero drains is HIS optimum for HIS season; ours has more ground and cannot go
there.
**A flat ceiling near 37 fits every row above** -- it reproduces straw and melon exactly and never
binds on q4 -- and is the next thing to test, with the q4 tables re-solved for it.

## `q4_armed`, not `len(unlocked)`

Both the cap and the tomato tile key on `state["q4_armed"]`, which `Q4Branch` decides at d6.
A live quadrant count is wrong here: **d12 is the very turn the fourth quadrant is bought**, so the
count reads 3 at dawn and 4 from d13.
A per-day test and a once-only test therefore disagree on exactly that day, which let the tomato tile
fire on the q4 board for -$1,031 while the cap looked correct.

## Seed at the close

Two separate leaks, one fixed and one not.

- **The replayed opening buys his seed counts.** d11 h0 issues `BUY_SEED STRAWBERRY 23`, sized for his
  42-tile season; the cap plants 37 and five sit in the shed to the final bell. Trimmed in the replay's
  order loop -- the same place `BUY_ANIMAL` is already re-labelled for the herd split. **+$560**, seed
  at close $590 -> $30, plants identical.
  **Three-quadrant boards only**: on a q4 board `q4_branch` installs its planting rows AFTER that turn,
  so the season total is short at d11 and the trim UNDER-buys -- **-$8,582 on q4_melon to save $170**.
- **Wheat, 2-4 at the close, ~$30, UNEXPLAINED.** Reached 0 on the pre-cap mix. Bounding `_later` by
  `RT.plant_prize(crop, day) > 0` was tried and did **not** move it, so rows past the crop's last useful
  day are not the cause. `test_no_wheat_seed_is_left_in_the_shed` is relaxed to `<= 3` and this is
  recorded there as an open regression, not a tidy-up.

## Stage 1 vs stage 2 -- the spike that separates them

Alex's original design, stated correctly (an earlier draft of this file had the two inverted):

- **Stage 1 -- the optimum animal and plant MIX, derived from the maths.** How many cows, sheep and
  geese; how many tiles of each crop. Decided from drains, price curves, yields per tile and the action
  cost of working them. Not copied off a leader.
- **Stage 2 -- the schedule.** The day-by-day plan that realises that mix: what is bought when, what is
  planted when, what is built when.
- Routing -- the lawnmower -- is downstream of both, and turns a day's rows into 24 turns of work.

Today's evidence is that stage 1 is where the gap to the #1 player is.

Our planner was handed tetsuya's schedule, on his own board, seat and seed (`94345389`, seed
959074148), against his own recorded opponent, with `REPLAY_OPENING_DAYS = ()` and
`cover.UNSOLVE_DAYS = range(0, 30)` -- so no taped opening and **no precomputed routes at all**:

```
  our planner on his schedule   $62,365
  his own recorded result       $55,330
                                +$7,035
  herd   COW 8  SHEEP 2  GOOSE 3
  plants WHEAT 161  STRAWBERRY 32  MELON 8  CARROT 8
```

**Our routing beats his, on his own schedule, with the worst routing we can give it.**
So the gap to the #1 player is not execution. It is stage 1 -- the mix itself.

Corroborated by utilisation, counting `NORTH/SOUTH/EAST/WEST` as movement and `PASS` as idle:

```
        tetsuya                     kawashigi
 day   work  move  PASS  idle%     work  move  PASS  idle%
 d14  107.2 142.3  45.7  15.5%     94.5 110.0   0.5   0.2%
 d20  147.8 116.2  30.6  10.4%    136.0 146.0   9.0   3.1%
 d23  131.8 123.5  39.4  13.4%    128.5 162.5   0.0   0.0%
```

kawa runs at the limit -- 0.0% idle at d23 -- and tetsuya never drops below 10%, while doing MORE work
with FEWER moves.
The tape we replay for d4-d11 is therefore one with no headroom, and any inefficiency downstream has
nothing to hide in.

**Stage 1 has never been built.** We inherit a leader's schedule wholesale -- Victor, then kawa -- which
is stage 2 handed to us with stage 1 already baked in and unavailable. Every crop and animal experiment
of 2026-08-19 (cap, tomato, geese, cow count) was a hand-poke at a stage-1 quantity through a stage-2
artifact, and each needed a two-hour route re-solve merely to be measurable.

The obstacle to searching stage 1 is that it is coupled to the routes through stage 2: every candidate
mix costs an hour of solving before it can be scored. Making it searchable needs either a much faster
solve, or a way to score a mix that does not require exact routes -- which is what deriving the mix from
the maths was for in the first place.

## His schedule does NOT transplant -- measured on 14 boards

One schedule, extracted from `94345389`, run on 14 of his other games: his seat, his seed, his recorded
opponent, no taped opening and no precomputed routes.

```
  record vs his opponents   7W - 7L   (0.50)
  mean vs his own bank      -$13,912
  our mean bank             $100,565     his $114,477
```

On the board the schedule came FROM, our routing beat his by +$7,035. On the other fourteen it is a
coin flip and $14k a game worse. His stage-2 rows carry that board's shop draw baked into them, so a
copy loses exactly the adaptation that makes him #1.

**So there is no shortcut through his schedule.** The thing worth having is the stage-1 logic that
GENERATES a mix from a board, not any schedule it happened to produce.

## Geese: the defect is `swap_in_geese`, not the bird

Fifth attempt at a goose verdict, and the first with a working instrument.

```
  2 geese via swap_in_geese, cow-solved routes      $97,317   seed at close $2,100
  2 geese via swap_in_geese, GEESE-solved routes    $96,766   seed at close $2,100
  no geese,                  geese-solved routes   $156,083   seed at close    $40
  no geese,                  cow-solved routes     $160,183   seed at close    $30
```

A matched re-solve did **not** rescue geese -- 96,766 against 97,317 -- while a cow season on the
geese-solved routes still banks $156,083. So the routes are fine and `swap_in_geese` is broken: it
reshapes the whole schedule (the d12 fixture goes WATER 38 -> 21, COLLECT_FERTILIZER 14 -> 6) and
inflates seed purchases by ~$2,000 in a way no route mismatch explains.

Geese from a schedule that natively contains coops are harmless: built on 9 of the 14 boards above,
one to three birds, no collapse and no seed explosion. Those boards went 6W-3L against 1W-4L without,
and averaged $8.7k better -- suggestive, but confounded, since a goose board is also an egg-shop board.

Previous goose verdicts were void for a different reason each time: `SELLABLE` omitted EGG so it could
never be sold, then cow-solved routes, now `swap_in_geese`. **Do not accept a goose measurement without
first stating which instrument produced it.**
