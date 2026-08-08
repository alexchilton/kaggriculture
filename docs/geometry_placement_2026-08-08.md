# Tile geometry: does the depot ring go to the thing that is visited most?

2026-08-08.
Branch `shaping-potential`.
Nothing committed; the work is left in the tree.

**Verdict up front: the geometry lands exactly as designed and the season does not pay for it.**
`DEPOT_RING_FIRST` ships `None` (off).
The always-on arm is a clear loss; the narrowed arm is a null that reversed sign on a held-out draw.
The reusable finding is not the flag, it is the measurement underneath it: **we were never turn-starved by walking**, so freeing walk turns cannot buy anything, and the season's money rides on one or two animals instead.

---

## 1. The measurement

`scripts/where_the_walking_goes.py` replays a full season (seed 11, `weedSpawnChance=0.0`, our agent and separately Seb's tape, each in seat 0 against the tape's own recorded opponent) and reports, per tile that ever held anything: what it held, how many work turns landed on it, and its Manhattan distance to the nearest depot we own.

Log: `data/logs/geometry_measure.log` (baseline) and `data/logs/geometry_measure_ringon.log` (flag on).
Per-day turn budget: `data/logs/geometry_budget_perday.log`.

### 1a. Visits per tile, by content

The task's premise was that different contents demand wildly different numbers of visits.
That is true, and the split is **pen versus everything else** — not, as assumed, melon versus strawberry.

    OURS                                        tiles   visits   per tile
    pen, COW                                        7      991      141.6
    pen, SHEEP                                      8      579       72.4
    strawberry                                     37      592       16.0
    melon + wheat (replanted)                      10      192       19.2
    melon only                                      8       90       11.2

    TAPE
    pen, SHEEP                                     11      877       79.7
    pen, COW                                        8      681       85.1
    strawberry                                     30      613       20.4
    melon only                                     12      138       11.5

Nineteen pens absorb **63% of all our work turns**.
A pen is worth five to nine times more on the depot ring than a crop tile is.

The task's model of the crops was wrong, and it is worth recording why.
Strawberry does not want "almost no water at all": `crop_ops` waters an ongoing crop whenever `consecutive_unwatered >= 1`, which is every second day for the rest of the season, purely to stop it weeding.
So a strawberry planted on day 6 is a stop on 12 days and takes 16 work turns; a melon is a stop on 10 days and takes 10.
**Melon is the cheap one, not the expensive one.**
Within the crops there is nothing worth sorting on.

### 1b. Derived visit counts, and they check out against the season

`tests/test_router.py::_service_days` derives the count from the reference's own gates rather than from the published tables, and the derivation matches the replay:

| content | derivation | predicted stops | measured work turns |
|---|---|---|---|
| MELON, one-shot, `max_day` 12 | `ceil(6/2)` survival + 7 in-window waters | 10 | 10, 10, 10, 9 |
| STRAWBERRY, ongoing, planted d6 | `ceil(23/2)` survival waters | 12 | 16 (= 12 waters + 4 harvests) |
| pen, placed d0 | every remaining day, FEED is mandatory | 29 | 97-104, i.e. ~3.4 ops/day |

This under-weights a pen deliberately: every pen day also draws WHEAT at the shed, so its distance is a round trip while a crop's is paid once.

### 1c. Where the turns went, and the number that reframes the task

    season totals, ours / tape          work 2,814 / 2,703
                                        move 3,460 / 4,025
                                        idle 1,426 /   999
                                        mv/wk  1.23 /  1.49

**We already do more work than the tape, with less walking, and 427 more idle turns — and we lose by $12k.**
Idle runs 8-92 unit-turns a day from day 15 to the end, against the tape's 0-26.
Walking is not the binding constraint.

That does not make the placement waste unreal, and it is measurable:

    service demand = sum over work visits of dist(tile, nearest owned depot)

    ours   6,244 demand   rearrangement bound 4,600   placement waste 1,644  (26%)
    tape   6,857 demand   rearrangement bound 5,339   placement waste 1,518  (22%)

The bound holds the multiset of per-tile visit counts and the multiset of tile distances fixed and pairs them optimally.
Anything above it is attributable to placement and nothing else.
Our waste is 26% of demand against the tape's 22% — real, and not the gap that costs $12k.

### 1d. The specific defect

Pen distances, ours against the tape, same nineteen pens:

    ours  [0,0,0,0,1,1,1,1,2,2,3,3,4,4,4,5,6,7,8]   sum 52
    tape  [0,0,1,1,2,2,2,2,3,3,3,3,4,4,4,5]...      sum 45

Three of ours sit at distance 6, 7 and 8 — (7,0), (8,0), (9,0) — all sited on **day 9 at the tail of NE**, while the near band of SW sat empty.
`field_order` is quadrant-major, so it exhausts NE out to y=0 before it offers SW's near ground.
Two of those three pens were never even stocked (1 work turn each all season).

---

## 2. The test

`tests/test_router.py::test_the_depot_ring_goes_to_what_is_visited_most`.

One theory, one test: *the total tour length needed to service a season's placements under `field_order` is strictly worse than under a visit-weighted assignment.*

It builds the demand from Seb's own schedule through day 13 (pens first, then plants — the order `_refresh_pins` consumes ground), re-implements `_next_ground` locally so it does not depend on a module another workstream owns, and scores `service days x depot distance`.

    sweep  cost 3,668   pen distances [0,0,0,0,1,2,3,3,3,3,4,4,4,4,4,5,5,5,6]  sum 56
    ring   cost 3,222   pen distances [0,0,0,0,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3]  sum 33

Written first, confirmed red (`AttributeError: no attribute 'DEPOT_RING_FIRST'`), then implemented.
After implementing, the fix was backed out — the sort in `field_order` replaced with `if False:` — and both new tests went red, then green again with it restored.

**What the test cannot reach**, stated because a gate only tests what it exercises: it scores a static assignment.
No router, no turn budget, no market, no replan, no opponent.
A layout that is cheaper to service can still bank less, and section 4 is where that happened.

A second gap: `test_the_depot_ring_goes_to_what_is_visited_most` and `test_the_ring_order_is_monotone_in_depot_distance` both set the flag themselves, so **neither goes red if someone flips the shipped default**.
The A/B is the only thing pinning the default.

---

## 3. What changed

All of it in `kagg/search/router.py`, plus tests and two scripts.
`kagg/search/dayplan.py`, `kagg/search/schedule_agent.py` and `tests/test_dayplan.py` were not touched.

**`router.DEPOT_RING_FIRST`** — new module-level flag, shipped `None`.
`None` restores the plain quadrant-major sweep exactly.
An int is the minimum number of owned quadrants at which the sort applies — the only "how late is it" `field_order` can see, since it is handed `unlocked` and nothing else.
`1` means always; `3` means from the day SW is bought, around day 8, which is where the far pens actually appear.

When it applies, `field_order` stable-sorts its output by distance to the nearest **owned** shed-access cell.
Stable, so the boustrophedon sweep still orders every distance band and a block stays as compact as a Manhattan ring allows.

Two existing tests asserted the sweep's contiguity directly and are now pinned with the flag off, with the reason recorded on each: a Manhattan ring of 12 tiles tours in 14 steps, not 12, and that is the trade the flag makes on purpose.

**Why only the tile half of the task's proposal was implemented.**
The task asked to also rank pending placements by expected lifetime visit count.
That ranking lives in `schedule_agent._refresh_pins`, which is off limits this session — and it is already half-present, because `_refresh_pins` allocates pens before plants *within* a day.
What it cannot do is reserve near ground on day 0 for a pen that arrives on day 9; that needs the schedule and is upstream of anything reachable from `router.py`.

---

## 4. The A/B, and the verdict

6 seeds x both seatings, head to head against Seb's tape, weeds off.
`scripts/ab_geometry.py`.
Every seat-1 pairing is an artifact — the open-loop tape collapses to $1.2-2.8k when it is the one being reacted to — so those stay in the money column and are struck from the win rate.

### Arm `1` (always on): a LOSS

Log `data/logs/geometry_ab.log`.

    arm      mean $    median $     wins   valid wins
    None    122,406     121,854     8/12          2/6
       1    121,441     116,587     7/12          1/6

    non-artifact seats (seat 0 only)
    s11/0 +7,895   s7/0 -1,489   s23/0 -23,369   s3/0 -3,096   s42/0 +1,705   s101/0 -14,779
    sum -33,133    better on 2/6    and it costs a win (seed 23, WIN -> loss)

On seed 11 alone it does everything it promised: pen distance 52 -> 30, the three far pens gone, placement waste 1,644 -> 985, work 2,680 -> 2,895, idle 1,883 -> 1,423, bank $104,257 -> $117,844.
It does not generalise.

### Arm `3` (from the SW purchase): a NULL

Logs `data/logs/geometry_ab_from_sw.log` and `data/logs/geometry_ab_heldout.log`.

| seed set | money sum | better | valid wins |
|---|---|---|---|
| 11, 7, 23, 3, 42, 101 | **+20,526** | 9/12 | 2/6 -> 2/6 |
| 19, 22, 33, 44, 55, 77 (held out) | **-11,111** | 6/12 | 1/6 -> **3/6** |
| pooled, 24 seats | +9,415 | 15/24 | 3/12 -> 5/12 |

+$392 a seat is well inside the ~15% seed noise, and **the money sign reversed on the fresh draw** — the winner's curse this repo has been bitten by before.
The win rate gained two valid seats and lost none (McNemar exact, p = 0.25), and it gained them *only* on the held-out half, which the tuning half did not see.

Two unconfirmed halves pointing opposite ways is a null.
Shipped off.

### Why the always-on arm loses

Land purchases are **byte-identical on every seed and both arms** (quadrant timelines match exactly), so this is not the land-parcel artifact that `PEN_NEAREST_DEPOT_FROM_DAY` hit.

What moves is the herd, and per this repo's own rule an animal verdict is judged on animals standing in pens:

    seed  11   animals 17 -> 18    money +$7,895
    seed  23   animals 17 -> 16    money -$23,369
    seed 101   animals 16 -> 15    money -$14,779

One animal either way, and $15-23k of season follows it.
The money is dominated by herd trajectory, and shuffling the ground moves that in both directions for reasons that have nothing to do with walking.

There is also a mechanical reason the pen gain is smaller than it looks.
`schedule_agent.PEN_NEAREST_DEPOT_FROM_DAY` is already 11, so from day 11 pens *already* take nearest ground.
The marginal effect of arm `1` on pens is therefore days 0-10 only — where our layout already matches the tape's distance exactly, 22 against 22 on day 0 — and most of what it actually moves is **crops**, which are the low-visit class the visit-weighting says should *not* get the near ground.
Crop distance sum barely moves (252 -> 260) while contiguity is given up.
That is why `3`, which starts around day 8, is the better-behaved of the two.

---

## 5. What I would do next, and what I would not

**Would not:** widen the ladder on arm `3` hoping the null resolves.
24 seats already say +$392 with a reversed sign; that is a request for a bigger sample to confirm noise.

**Would:** the reachable version of the task's actual proposal, which is a *reservation*, not a sort.
`_refresh_pins` knows the whole schedule — it already sums `builds` cumulatively — so it can count the pens the schedule still owes and hold that many near tiles back from the crop sweep.
That fixes the real defect (a day-0 strawberry taking ground a day-9 pen needs) instead of re-sorting after the fact, and it is one function in `schedule_agent.py`, which another workstream owns right now.

**Would also:** chase the idle, not the walking.
1,426 idle unit-turns against the tape's 999, concentrated after day 15, is a bigger and better-evidenced target than 1,644 depot-steps of placement waste — and section 1c says the two are not the same problem.

---

## 6. Files touched

    kagg/search/router.py                    DEPOT_RING_FIRST flag + the sort in field_order
    tests/test_router.py                     2 new tests, 2 existing pinned with the flag off,
                                             plus _service_days / _demand_from_seb / _service_cost
    scripts/where_the_walking_goes.py        NEW  the per-tile visit + distance measurement
    scripts/ab_geometry.py                   NEW  the flag A/B ladder
    docs/geometry_placement_2026-08-08.md    NEW  this file

Test state, `tests/test_router.py` + `tests/test_dayplan.py`, measured by stashing the change and re-running against the tree as it stood at the end of the session:

    without my change   74 passed, 7 failed
    with my change      76 passed, 7 failed      <- the same 7, plus my 2 new tests

**Zero new failures.**
The seven are pre-existing on this branch and the set grew during the session as another workstream edited `schedule_agent.py`, `dayplan.py` and `scheduler.py` underneath — at the start of the session the same command gave 2 failures, not 7, with my change in place either way.
The wider suite carries a further ~18 failures and 4 errors, mostly `dayplan.Farm` no longer existing.
None of that is mine; do not read the raw suite count as a verdict on this change without re-baselining, because the tree moves.
