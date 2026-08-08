# The PLACE gate, generalised off the calendar

`PLACE_IS_MANDATORY_FROM_DAY = 14` was fitted to one seed and one tape.
This replaces it with `PLACE_IS_MANDATORY_WHEN_HELD_OVERNIGHT`, which reads the animal's age in the
shed and never reads the date.

**Read the "What this does NOT fix" section before trusting it.**
The generalisation lands its target day exactly and it is not a free win: on one of the five seeds
measured it is materially worse than the constant it replaces.

## The rule

> A PLACE joins the MANDATORY pool when the animal it would place **has stood in the shed
> continuously since this day's dawn** -- that is, it was already there yesterday and has had a
> whole day in which this pen stood open and nobody came.

An animal bought this morning is not covered.
It still has today to be placed on merit, which is exactly what day 0 does with four of them, and
what the original sweep found: gates of 0 and 6 -- which make every placement mandatory on arrival --
pinned the herd at 16 for the rest of the season.

The refusal being fixed is a **budget** refusal, not a price.
That part is unchanged and was already measured: every `plan_routes` refusal of the stranded pen on
seed 11 was `used + cdelta > cap`, not a ratio loss, and a 2x/3x/5x/10x sweep of the PLACE prize left
the season identical to the dollar.
Being in the mandatory pool does not let a placement jump the budget either; it only gives it first
claim on turns that are otherwise gone by the time it is offered.

## What is plumbed, and why it is the raw fact and not a verdict

`build_nodes` sees one turn at a time and has no memory, which is precisely why the gate it used to
consult was a hard-coded day number.
It now takes `held_since_dawn`, maintained in `schedule_agent.make_agent`:

- at the day rollover, `state["held_since_dawn"] = Counter(shed)` -- the shed as it stood at dawn;
- on every turn after, `state["held_since_dawn"] &= Counter(shed)`.

`Counter.__and__` is elementwise min, so the value ends up as the **lowest** the shed has held of
each item at any point today, which is exactly the count of this dawn's units still unplaced.
Without the floor, a shed that goes `SHEEP 1 -> 0` (placed) `-> 1` (bought again at noon) would
report the new sheep as having waited overnight, and it would jump the queue on the day it arrived.

It is passed as the raw board fact rather than as a precomputed "these animals are stranded" set,
for three reasons.
Every other pricing rule in `build_nodes` reads the board directly, so a caller-computed verdict
would be the only one that did not.
A verdict would split the rule across two modules, so changing it would mean changing both.
And it would make `test_an_animal_held_since_dawn_is_mandatory_and_one_that_just_arrived_is_not` a
test of the plumbing rather than of the rule -- the test could only check that MANDATORY is added
when the caller says to, which is a tautology.

`None` means "no memory of yesterday", which is what day 0 and every direct unit-test call have.
`_router_acts` reads `state["held_since_dawn"]` strictly, not with `.get`, so a future state that
forgets to carry it fails loudly instead of quietly losing the rule.

## Tests

Written before the change, and both were red:

- `test_the_place_gate_does_not_read_the_calendar` -- one empty pasture and one sheep in the shed,
  priced on every day 0..29; the verdict must not change.
  Failed with `the verdict flips at [14]. That is a date, not a fact about the farm.`
- `test_an_animal_held_since_dawn_is_mandatory_and_one_that_just_arrived_is_not` -- both directions,
  on days 0, 6, 13, 14 and 26.
  Failed with `TypeError: build_nodes() got an unexpected keyword argument 'held_since_dawn'`,
  i.e. the fact the rule needs was not expressible at all.

Reverting the fix turns both red again (the first on its assertion, the second on the signature).
`test_a_far_pen_is_refused_for_budget_and_not_on_ratio` was updated to pass `held_since_dawn` rather
than rely on `day=14`, so it tests the gate and not the calendar.

Fast suite after: **780 passed, 93 skipped, 6 xfailed, 0 failed**.
The 5 errors in `tests/test_replay_plan.py` are `FileNotFoundError` on `data/*.json` and are an
artifact of the agent worktree not carrying the gitignored `data/` tree; they are unrelated.

## Seed 11, per day -- the target day is hit exactly

`python -u scripts/pen_census.py --seed 11 --gate {off,day14,stale}`, Seb's tape, weeds 0.0.
`penned` is animals STANDING IN PENS at dusk; `shed` is animals held; `empty` is open pens.

| day | off penned/shed | day14 penned/shed | held-overnight penned/shed |
|----:|:----------------|:------------------|:---------------------------|
| 0-5 | 4,5,5,6,7,7 / -- | identical | identical |
| 6   | 8 / COW 1       | 8 / COW 1         | 8 / COW 1 |
| 7-8 | 9, 10 / --      | identical         | identical |
| 9   | 11 / --         | 11 / --           | 11 / -- |
| 10-12 | 13, 15, 16 / -- | identical       | identical |
| 13  | 17 / SHEEP 1    | 17 / SHEEP 1      | 17 / SHEEP 1 |
| **14** | **17 / SHEEP 2** | **19 / --**   | **19 / --** |
| 15  | 17 / SHEEP 2    | 19 / --           | 19 / -- |
| 16  | 17 / SHEEP 2    | 17 / --           | 17 / -- |
| 17-18 | 17 / SHEEP 2  | 17 / --           | 17 / -- |
| 19-24 | 17 / SHEEP 2  | 17 / --           | **16 / --** |
| 25-28 | 18 / SHEEP 1  | 17 / --           | 16 / -- |
| final money | 113,382   | 112,409           | 111,828 |
| stranded-overnight days | **15** | **0**    | **0** |

At the day it targets the generalised rule is the day-14 gate, exactly: 19 in pens, shed empty,
two empty pens filled, and $2,951 against $2,963 -- twelve dollars apart.
Animals in pens are **identical to the day-14 gate on every day d0 through d18**.

Against `scripts/breakdown.py --tape seb --seed 11 --weeds 0.0 --days 30 --diff --no-moves`,
differing cells per day, day-14 gate -> held-overnight:

    d0=3   d1=3   d2=3   d3=5   d4=3   d5=3     unchanged, byte-identical
    d6=8                                        unchanged
    d7   6 -> 10      d8   8 -> 10              WORSE
    d9  13 -> 11                                better
    d10=14  d11=14                              unchanged
    d12 13 -> 15                                WORSE
    d13 13 -> 11                                better
    d14=13                                      unchanged -- and `sheep` and `place` are exact on it
    total 414 -> 419 cells,  0/30 days exact either way

**d0-d13 are NOT byte-identical, and the reason is that the day-14 gate was under-firing.**
This tape leaves a COW in the shed at the d6 dusk beside an empty pasture -- the same bug, one day
long -- so the rule correctly fires on d7 as well.
d0-d6 are byte-identical, the placement counts do not move on any of d7-d13, and the hard constraint
(no regression on d0-d5) holds: money and pens are identical to the dollar through d5 on every arm.

The `sheep` row still reads -2 from d16 to d29 under both gates.
That is **not** this bug and it is not a failure to buy or to place: we reach eleven standing sheep
on d14, the same as the tape, and then lose two between d15 and d16 with the shed empty.
They starve and escape, because filling 19 pens is more than the feed cadence carries.
That is the defect already recorded against `PLACE_IS_MANDATORY_FROM_DAY` and it is out of scope
here -- fixing it means touching feeding, which this task was bounded against.

## Five seeds -- and this is where it is not a clean win

Same tape and weeds 0.0 throughout; only the env seed moves.

| seed | arm | stranded-overnight days | penned mean | penned max | final money |
|-----:|:----|------------------------:|------------:|-----------:|------------:|
| 11 | off | 15 | 13.52 | 18 | 113,382 |
| 11 | day14 | 0 | 13.52 | 19 | 112,409 |
| 11 | **held-overnight** | **0** | 13.17 | 19 | 111,828 |
| 3  | off | 15 | 13.52 | 18 | 84,749 |
| 3  | day14 | 0 | 13.52 | 19 | 85,198 |
| 3  | **held-overnight** | **0** | 13.52 | 19 | 85,197 |
| 7  | off | 10 | 13.52 | 18 | 109,474 |
| 7  | day14 | 8 | 13.34 | 18 | 111,073 |
| 7  | **held-overnight** | **8** | 13.34 | 18 | 120,068 |
| 19 | off | 15 | 13.52 | 18 | 110,030 |
| 19 | day14 | 0 | 13.52 | 19 | 106,102 |
| 19 | **held-overnight** | **0** | 13.17 | 19 | 107,559 |
| 23 | off | 5 | 13.21 | 17 | 94,605 |
| 23 | day14 | 3 | 13.69 | 18 | 96,454 |
| 23 | **held-overnight** | **10** | 13.48 | 19 | 80,572 |

Answering the question as asked -- *is any animal ever left in the shed overnight beside an empty
pen?*

- **seed 11: no.** 15 days -> 0.
- **seed 3: no.** 15 days -> 0.
- **seed 19: no.** 15 days -> 0.
- **seed 7: yes, still.** 10 days -> 8, and two sheep instead of one. Identical to the day-14 gate,
  which also leaves them: the pens on that board are refused on budget even from the mandatory pool.
  The rule fires; `plan_routes` still cannot fit the trip.
- **seed 23: yes, and worse.** 3 days under the day-14 gate -> 10. On that board the shed carries a
  sheep from d9, so the rule starts firing at d10, and d13 stands 15 animals against the day-14
  gate's 17. This is the same shape as the retired gate-0 and gate-6 arms: forcing a far PLACE into
  the mandatory pool *early* costs placements rather than winning them, because the pool is assigned
  first against an empty budget and a ten-turn trip taken by one vehicle displaces the work that
  would otherwise have been done. It costs **-$15,882** against the day-14 gate on that seed.

Aggregated over the five, held-overnight against day14: penned mean **-0.18 animals per day**,
money **-$1,202** mean and **-$581** median, stranded-overnight days 8+10 against 8+3.

So: it removes the magic number, it is exact at the day the number was fitted to, it clears the
stranding on three seeds and matches the constant on a fourth -- and on the fifth it is a real
regression on both the correctness floor and the bank.

## The correctness floor, explicitly

`FEED_ORDER_CAP = 4` collapsed animals-in-pens 17 -> 8 and was nearly shipped because only cells and
money were measured.
This change was measured against that floor: `penned` per day, per seed, both arms, all 29 days.
It does **not** starve the herd -- max pens rises 18 -> 19 on four of five seeds and the mean moves
by less than a fifth of an animal -- but it is not a herd improvement either, and on seed 23 it
stands 0.21 fewer animals a day than the constant it replaces.

`scripts/pen_census.py` is committed so the floor can be re-run rather than re-derived.

## What I did NOT check

- **Whether these five seeds are actually five different problems.** With `weedSpawnChance = 0.0`,
  a fixed schedule and a replayed opponent tape, the seed moves very little: penned d0-d12 is
  identical on seeds 3, 11 and 19 and nearly so on 7. This is a weak test of generality and should
  not be read as one. A stronger one needs weeds on, or a live opponent, or both.
- **The opponent.** Every run above is against the same replayed `seb` tape, on seeds where that
  tape's fixed action sequence is not a response to the board it is playing. Nothing here says
  anything about `kagg.arena.evaluate` or the opponent pool, and nothing here is a win-rate.
- **Win rate, at all.** Every number in this document is money or animals. The ladder is Elo and
  this project's own rule is to select on win rate. Not measured.
- **Whether the seed-23 regression is causal or drift.** It is deterministic and reproducible, but I
  did not isolate which firing causes it; the d10 firing and the d14 firing are confounded in a
  single run.
- **The feed pipeline.** Two sheep starve at d16 on seed 11 under both gates. Bounded out of this
  task deliberately -- the fix is in feeding and another agent may be near that code.
- **Weeds on.** Every run is `--weeds 0.0`.
- **`seb2` and `oldleader` tapes.** Only `seb`.
- **The slow suite.** Only the fast suite was run to completion after the change.

## Files

- `kagg/search/router.py` -- `PLACE_IS_MANDATORY_WHEN_HELD_OVERNIGHT`, `build_nodes(..., held_since_dawn)`.
- `kagg/search/schedule_agent.py` -- the dawn snapshot and its per-turn floor; passed into both
  `build_nodes` call sites.
- `tests/test_router.py` -- two new tests, one updated.
- `scripts/pen_census.py` -- the three-arm herd census.
