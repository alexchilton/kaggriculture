# Brief: the day-12 sheep that starves at (1,6)

Written for a fresh reviewer.
Everything below is measured, not theorised.

## The bar

Zero animal deaths.
An animal escapes when `consecutive_unfed >= 2` (`reference/kaggriculture.py:786`).

## The harness

`scripts/matched_days.py` replays Seb's tape to each dawn so the board is byte-identical,
stocks the shed (`WHEAT 200`, `FERTILIZER 100`), then runs ONE day with our planner.
29 independent experiments, seed 11, weeds off.
28 of the 29 days lose nothing.
Day 12 loses one SHEEP.

## What is known

The animal is the SHEEP at **(1, 6)**.
At dawn it has `consecutive_unfed = 1` — one missed feed from death, so it is flagged `at_risk`.
It receives no FEED all day.
Four OTHER at-risk animals are fed the same day, at h3, h6, h13 and h21.

The day's job list is fully covered: at h3 with 13 units the planner reports `uncovered_total=0`.
The FEED job at (1,6) is correctly `at_risk=True required=True`.
So the PLAN is right and the VISIT is what fails.

Turn by turn, the unit whose route contains (1,6):

    h0   owner=u0@(4,4)  act=['PICKUP','WHEAT',5]
         route=[SHED, (3,3), (2,3), (2,5), (2,6), (1,6)]
    h2   owner=u1@(4,4)  act=['PICKUP','WHEAT',3]
         route=[SHED, (4,7), (2,6), (1,6), (1,9)]
    h3   owner=u7@(4,5)  act=['WEST']
         route=[(2,5), (1,5), (1,6), (1,9), (0,9)]        <-- NO SHED STOP
    h5   u7@(2,5)  act=['COLLECT_FERTILIZER']              (a second at-risk pen, also not fed)
    h10  u7@(1,6)  inv={'FERTILIZER': 1}  act=['COLLECT_FERTILIZER']   <-- cannot FEED, no wheat
    h11+ (1,6) OWNED BY NOBODY

So ownership of the tile moves u0 -> u1 -> u7 across the first three hours, and the unit that
finally arrives holds no wheat because its route was materialised without a depot stop.

## What has been ruled out

`Node.needs` is NOT empty. `kagg/search/router.py:729` is

    self.needs = collections.Counter(i for o, i, _p in ops if i and o in DRAWN)

with `DRAWN = ("FEED", "FERTILIZE", "PLACE", "BUILD")`, and `animal_ops` emits
`("FEED", "WHEAT", prize)`. So the job correctly declares `needs == {WHEAT: 1}`.

`cover.materialise` inserts a `Depot(drop=False, pick=short)` whenever the running
`held` counter cannot cover `after[i]`, the suffix sum of `needs` from position i onward.
That mechanism demonstrably works — it is what feeds the other four at-risk animals.

## The question

Why does u7's h3 route contain two at-risk FEED jobs and no depot stop, when each of those
jobs declares `needs == {WHEAT: 1}` and u7 starts the tour empty?

Candidate directions, none confirmed:

- The reassignment itself. u0 and u1 both had (1,6) with a SHED stop in front of it. Something
  re-planned at h3 and handed the tile to a unit that was already mid-tour. Does the replan
  path pass the unit's LIVE inventory as `carry`/`held`, or does it assume the old owner's?
- `_eta_along` was changed in this rebuild to SKIP depot stops so a shed trip is not a claim.
  Check whether that makes an at-risk job look already-served by an earlier unit that in fact
  never reaches it.
- Whether a job that is dropped from one unit's route and picked up by another keeps its
  `at_risk` / `required` flags through the handover.

## Where to look

- `kagg/search/cover.py` — `materialise`, `plan`, `cost`. The suffix-sum draw logic.
- `kagg/search/schedule_agent.py` — `_solve`, `_router_acts`, the executor's depot branch,
  `_eta_along`.
- `tests/test_the_whole_day_is_planned_including_the_drop.py` — the rebuild's gate, 6 green.

## Rules of engagement

- One theory = one pytest test, written and RED before any code change.
- After fixing, revert the fix and confirm the test goes red again.
- Do not widen scope. The deliverable is the cause of THIS starvation.
- Re-measure with `PYTHONPATH=. python3 -u scripts/matched_days.py`; the bar is `animals lost 0`
  with harvest/idle not going backwards.
