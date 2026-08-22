# Day 6: the stranded wool, found and fixed

Seed 11, kawashigi grid, weeds 0, recorded shop draw injected.
The d6 row asks `sells={'FERTILIZER': 5, 'WOOL': 12}` and the board produces 9 wool across two shear jobs.
Baseline sold 10 of 17: the 5 fertilizer at h00 plus the 5 wool one hand dropped at h09.
The other 4 wool rode in a hand from h09 to dusk and reached the shed only via the overnight sweep, after the market had closed.

## Why that hand's tour contained no shed stop

The hinted theory — a pen whose `yield_units` is 0 at dawn producing an empty `gives` — is NOT what happens here.
Both sheep pens carry their wool on the board at dawn: (4,3) reads `yield_units 4` and (4,4) reads `yield_units 5`, so both shear jobs predict their load (`predict_yield`) and `held` in `materialise` is correct.

The plan (`cover.plan`, day 6, `deliver=False`, `rush=True`, `wanted={'WOOL': 12}`) gives the shear at (4,3) to the hand that then feeds the cows at (0,0) and (1,0).
Every delivery rule in `materialise` declined that hand, each for its own documented reason:

- Rule 0 (`RUSH_BANK_MIN`) fires only on a hand that STARTS the tour loaded; this one starts empty.
- The free drop (`DROP_WHERE_THE_TOUR_ALREADY_STANDS`) and the re-draw (`REDRAW_RATHER_THAN_CARRY`) fire only at a zero-detour depot, and neither (4,3) nor anything after it is one — (4,3) is not a shed-access tile, and the shed-access set is `{(4,4),(4,5),(5,4),(5,5)}`.
- Rule 2 refused on quantity: with `DELIVER_SURPLUS_NOT_THE_ROW = False` the load counts only the row's items, so WOOL 4 sat under `DELIVER_MIN = 6`.
- Rule 3, the closing trip, is never charged (`DELIVER_CUTOFF_TURNS = 99` makes `deliver` False on every 24-turn day).

The last two interlock, and that interlock is the defect.
`DELIVER_MIN`'s own docstring defers a small load to "the end of the tour, which ends at the shed anyway" — and with `deliver` False that clause is false.
This also explains mechanically why the `DELIVER_CUTOFF_TURNS = 12` arm was a measured null: this tour costs 21 of its 23-turn budget and the walk home from (1,0) costs 8 more, so `plan()` prices the `deliver=True` route at 29, refuses it as over budget, and keeps the tour without the closing drop.
No setting of the cutoff can deliver this wool; the tour has no later delivery at all.

## The fix: batch only for a delivery that exists

`SHIP_WHAT_NO_LATER_STOP_CAN_BANK = True` in `kagg/search/cover.py`, one new clause in rule 2.
When the closing trip is uncharged (`deliver` False) and neither the current position nor any remaining stop stands on a depot tile, a positive load of the ROW's produce ships now, `DELIVER_MIN` notwithstanding.
The ferry re-draws whatever the rest of the tour still needs on the same stop, exactly as the existing rule-2 ferry does, so the pens ahead still eat.
Tours that still touch a depot are untouched: the zero-detour rules own those, and their refusals (`REDRAW_ONLY_WHAT_THE_MARKET_WONT_TAKE`) are measured.
The `due` clock is not consulted for a stranded load, because `tail` prices a closing drop that `deliver=False` never plans.

The greedy prices the ferry like any other stop (`slot` -> `materialise` -> `turns`), so assignment rebalances instead of shipping an over-budget tour.
On d6 the planner now routes the wool through a shed stop at h08 and the SELL lands while the market is open.

Test: `tests/test_a_load_the_tour_can_never_deliver_is_ferried_not_batched.py`.
Red on HEAD, green with the fix, red again with the flag backed out (`-n0`), restored green.
A second test in the same file pins the guard: a tour whose remaining stops touch a depot buys no walking ferry.

## Measured, before -> after (ours/tape, `--tape kawashigi --days 17`)

d0-d5: byte-identical, every row.

d6, the target day:

| row | before | after |
|---|---|---|
| sell | 10/17 | **14/17** |
| sh:wool (end of day) | 4/0 | **0/0** |
| buy_seed | 7/15 | **15/15** |
| money | 3/957 | 358/957 |
| tiles | 50/50 | 50/50 |
| buy_land | 1/1 | 1/1 |
| plant / water / harvest | 2/2, 17/19, 2/2 | 2/2, 17/19, 2/2 |
| feed / care / collect | 6/6, 6/6, 6/6 | 6/6, 6/6, 6/6 |

14/17 is the ceiling of this fix by construction: the row asks WOOL 12 and the board only grows 9.
The last 3 need more sheep and remain a separate open item.

d7 reconciles to exact: `sell 10/6 -> 6/6` (the baseline was selling yesterday's swept wool a day late) and `buy_seed 5/4 -> 4/4`.
d4 `harvest 7/7` holds.

Downstream of d7 the board diverges as any d6 change makes it: the herd ends BIGGER (d16 cow+sheep 11 vs 10 baseline, d9 9/12 vs 8/12), d8 `feed 0/10 -> 1/10`, and d16 money closes 22,246 vs 19,067.
Two rows move the other way and are noted rather than hidden: the second sheep is lost on d8 (0/4 vs 1/4 baseline; both runs lose sheep inside the pre-existing d8 feed collapse, `feed 1/10`), and the weed row's timing shifts (weeds appear d12-d13 and are dug by d14/d16, against d14/d16 appearances in baseline; both runs end d16 within one weed).
Days match in order: d0-d6 strictly improved or identical, d7 exact, so the later jitter is inherited board state, not a gate.

## The two named gates are stale at this working state

`tests/test_each_day_matches_the_tape.py` errors at setup on every day: it asks for `breakdown.TAPES["seb"]`, and the seb tapes were removed from that dict on 2026-08-13.
`tests/test_the_first_seven_days_match_the_plan.py` drives the retired Seb schedule (90494364) and fails 7 of 15 with the fix OFF.
With the fix ON it fails 6 of 15 — `test_no_pen_stands_empty_at_dusk_beside_a_shed_holding_its_animal` goes green — so the fix strictly reduces that gate's failures and introduces none.
Both gates need rebasing onto the kawashigi tape; that is not this change.

## Environment note for reproduction

Commit `2ddffb6` alone does not run: `schedule_agent` calls `router.crop_ops(..., tile=tile)`, which only exists in the UNCOMMITTED `kagg/search/router.py` in the main checkout (the `WATER_ROTATION` work), and `scripts/breakdown.py` needs the untracked `kagg/plan.py`.
Both were mirrored into this worktree unchanged; they are not part of this fix.
