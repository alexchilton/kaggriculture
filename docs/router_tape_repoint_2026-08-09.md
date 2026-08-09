# `tests/test_router.py`: repointing the tape fixture from `seb` to `seb1326`, and re-deriving every asserted day

Task #53.
`TAPE_REPLAY` / `TAPE_SCHEDULE` / `TAPE_TEAM` (added `a34cc1e`) repointed from
`data/seed_scripts/top_guys/90494364` (`seb`, played on 1.32.2) to
`data/seed_scripts/top_guys/90976060` (`seb1326`, played on 1.32.6).
The two tapes land quadrants on different days (5/9/11 vs 4/6/10), carry different pen counts
(~19 vs 21), and re-cut the herd from wool to milk (MILK 179→303, WOOL 230→104, MELON 132→96), so
every day-specific number in this file had to be re-derived rather than merely re-run.

## Method

Two scripts (temporary, not committed — logs kept under `data/logs/`):

- **`tape_truth.py`** replays the leader's own recorded actions against his real recorded opponent
  from the episode JSON. Because kaggriculture is deterministic given seed + actions, this
  reproduces the historical episode exactly — it is the ground-truth "tape" value every test
  docstring quotes. Output: `data/logs/tape_truth_90976060.log` (dawn bank, sells, op tallies, seed
  peaks, first-sell/first-buy hours, per day 0–11).
- **`day_by_day_diff.py`** runs the same replay for the tape's actions and for our
  `schedule_agent`-driven agent (playing against the same real opponent sequence), and diffs the
  op tally per day. Output: `data/logs/day_by_day_diff.log`.

Sanity check: replaying the OLD tape's own actions under the current 1.32.6 env gives dawn day 6 =
**$1,855**, matching the number already recorded in the `TAPE_REPLAY` comment block before this
pass started. Same method, same answer — the new-tape numbers below use the identical method.

## Finding that changes the shape of the triage: days 0–3 are no longer exact under `seb1326`

The day-4 gate's docstring claimed "days 0-3 already exact" — true of the old tape, false of the
new one. Op-for-op diff, our agent vs. the tape's own replayed actions, days 0–3:

```
day 0: {'FEED': '1/4', 'CARE': '1/4', 'SELL': '7/0'}
day 1: {'SELL': '2/4'}
day 2: {'SELL': '6/5'}
day 3: {'FEED': '4/6', 'CARE': '4/6', 'SELL': '7/5'}
```

So day 4's shortfall (below) is not purely a day-4 defect; it inherits upstream drift. Recorded in
the test's docstring; not separately gated, since no day-0/1/2/3 op-for-op test exists in this file
(day 0 and day 1's own gates are `@pytest.mark.skip`d for an unrelated reason — tour shape, not ops).

## Per-test table

| Test | Verdict | Number / finding | Source |
|---|---|---|---|
| `test_a_carried_sell_row_never_offers_more_than_the_biggest_day_ever_asked` | **real gap** (untouched) | Hand-built harness, no tape reference at all. `sched[0]["sells"]={"MELON":5}` twice, shed holds 20; agent offers `SELL MELON 20` instead of capping the carry at 5. | Pre-existing bug in `schedule_agent.py`'s carry-cap logic, independent of the tape. Out of scope — `schedule_agent.py` is owned by another agent. |
| `test_a_hand_full_of_the_days_sell_row_walks_it_in_when_there_are_turns_to_spare` | **real gap** (untouched) | Hand-built harness (`_mid_tour_state`), no tape reference. Unit holding MELON 12 with 12 turns of slack and a 5-turn detour home emits `NORTH` instead of `EAST`/`SOUTH` — it never triggers `DELIVER_FERRY`. | Pre-existing bug in `schedule_agent.py`'s deliver-ferry trigger, independent of the tape. Out of scope. |
| `test_the_sells_row_is_a_day_total_not_a_per_turn_quota` | **re-derived, still a real gap** | Day 4 target changed `{WHEAT:28, FERTILIZER:4}` → `{WHEAT:49, FERTILIZER:6}`. Our agent currently delivers `{FERTILIZER:3, WHEAT:19}` — well under, not over. | Target: `data/seed_scripts/top_guys/90976060/schedule.json` key `"4"`, `sells` field; cross-checked against `tape_truth_90976060.log` ("day 4: {'WHEAT': 49, 'FERTILIZER': 6}"). Gap traced to `test_day_four_matches_seb_on_every_op_it_works`'s HARVEST/WATER shortfall — less produce exists to sell. |
| `test_the_feed_top_up_counts_wheat_already_standing_ripe_in_the_field` | **re-derived, now passes** | Day 4 target changed `bought == 0` → `bought == 1`. Our agent already buys exactly 1. | Target: `schedule.json` key `"4"`, `buys` field = `{WHEAT: 1}` (was `{}` under the old tape); cross-checked against `tape_truth_90976060.log` ("day 4: ... 'BUY_PRODUCT': 1"). |
| `test_day_four_matches_seb_on_every_op_it_works` | **real gap** (docstring corrected, assertion untouched — it's a structural diff, not a number) | `HARVEST 11/14`, `WATER 12/17`, `SELL 22/55` (ours/tape). Also corrected the false "days 0-3 already exact" premise — see above. | `data/logs/day_by_day_diff.log`, day 4 row. |
| `test_the_biggest_sale_takes_the_earliest_slot` | **re-derived (assertion dropped), now passes** | Kept the slot-order invariant (still passes unmodified). Dropped `dawn6 >= 860` — its premise (day 6 needs $854 for an $800 strawberry order) no longer exists: day 6's seed row is `{}` under `seb1326`. The tape's own dawn-day-6 bank, replayed, is **$0**; ours is $26 — already ahead of the tape on this metric, so there is no gap to threshold. | `schedule.json` key `"6"` (`seeds: {}`); `tape_truth_90976060.log` dawn bank table (`day 6: 0`). |
| `test_wheat_drawn_this_turn_is_the_herds_reserve_not_extra_to_it` | **deleted** | Day 5's row is `sells: {FERTILIZER: 5}` under `seb1326` — no WHEAT key at all, so the wheat-reserve race this test measured on day 5 doesn't occur. Our agent still sells 10 unrequested wheat that day, possibly the same carry-logic family as the first row of this table, but that's a different, unopened question. | `schedule.json` key `"5"`; `tape_truth_90976060.log` ("day 5: {'FERTILIZER': 5}"). |
| `test_day_six_gets_a_load_to_the_shed_early_enough_to_fund_the_strawberry` | **deleted** | Day 6 has neither `animals_bought` nor `seeds` under `seb1326` (both `{}`) — no $800 bill to fund by hour 2. Was `xfail(strict=True)`, had started silently XPASSing from an unrelated hour-0 FERTILIZER carryover sale, not from anything the test's routing narrative describes. | `schedule.json` key `"6"`. |
| `test_day_six_sells_the_wool_as_soon_as_the_walk_allows` | **deleted** | Same day-6 board change as above; the specific sheep-pen geometry (`(1,4)`/`(3,4)` vs tape's `(4,4)`/`(4,3)`) this test traced belongs to the old tape's day 6, which no longer exists in this shape. Also spuriously XPASSing for the same unrelated reason. | `schedule.json` key `"6"`. |
| `test_day_six_plants_every_tile_the_row_asks_for` | **re-derived, still a real gap** | Day 6 target changed `planted == 14` → `planted == 4`. Our agent plants 6 — **over**-planting, not the under-planting (stuck-seed-order) bug the old test caught. | Target: `schedule.json` key `"6"`, `plants` list (4 entries: `MELON, MELON, STRAWBERRY, MELON`); cross-checked against `tape_truth_90976060.log` ("day 6: ... 'PLANT': 4"). |
| `test_the_days_seed_is_bought_before_the_days_livestock` | **deleted** | Day 6 has neither `animals_bought` nor `seeds` under `seb1326` — the livestock-vs-seed funding race this test measured doesn't occur that day. The mechanism (HIRE/LAND/ANIMAL settle before SEED, so livestock takes the bank first) still exists in the code; days 9 and 11 both carry simultaneous `animals_bought` + `seeds` rows and could host a rebuilt version, but that needs a fresh hour-by-hour trace this pass did not do. | `schedule.json` keys `"6"`, `"9"`, `"11"`. |

## Result

72 tests collected (was 76; 4 deleted).
**5 failing, all real gaps, none newly discovered by this pass** — they were already-known
divergences that the repoint re-measured against the correct target instead of a stale one:

```
FAILED test_a_hand_full_of_the_days_sell_row_walks_it_in_when_there_are_turns_to_spare
FAILED test_a_carried_sell_row_never_offers_more_than_the_biggest_day_ever_asked
FAILED test_the_sells_row_is_a_day_total_not_a_per_turn_quota
FAILED test_day_four_matches_seb_on_every_op_it_works
FAILED test_day_six_plants_every_tile_the_row_asks_for
```

61 passed, 6 skipped (unrelated, pre-existing `@pytest.mark.skip`s on tour-shape gates).
Confirmed by deselecting the 5 known-red tests and re-running the rest clean.

None of the fixes moved a threshold to whatever the code currently produces — every changed number
traces to `schedule.json`'s own row for that day, cross-checked against a full replay of the tape's
own recorded actions against its real recorded opponent (`tape_truth_90976060.log`).
