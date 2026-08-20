# docs/ — index

**Rewritten 2026-08-20, in a full consolidation.**
`docs/` had grown to 93 markdown files, most of them one-off session notes.
This pass reduced it to 19, by folding every source file's measurements into a subject survivor
document as a dated, attributed section.
No number was deleted.
Every source file's content is either in a survivor doc below or, for the one file that had no
clean home, still on disk under its own name.
The mapping of what moved where is at the bottom of this file, and in full in
`docs/doc_consolidation_2026-08-20.md`.

## Unresolved contradictions — read before trusting a number below

Four contradictions surfaced during the fold.
None were resolved by picking a winner, per instruction.
Each is also marked `**UNRESOLVED CONTRADICTION — needs a measurement.**` inline, in the document
named.

1. **Does MILK actually floor at $1-5 on the real ladder?**
   In `market_curves_and_the_q4_branch_2026-08-15.md`, one 2026-08-13 section reads 3 real ladder
   episodes where MILK never floors; a different 2026-08-13 section in the same document reads 5
   *different* real ladder episodes the same day showing MILK closing at $1-$5 repeatedly.
   Neither source reconciles the other's episode set.
2. **Does keeping melon volume beat swapping to strawberry?**
   Same document. A model concludes keeping melon wins by $8,162 even in the melon-heavy case.
   A real lost ladder game (`92562037`) in a different section shows 19-for-19 melon closing at $25,
   read there as costly overplanting.
3. **What is the real stranded-produce threshold at season close?**
   In `after_the_close_release_2026-08-15.md`, a 2026-08-15 report measures stranded produce at 16
   units with `TOLERATED_UNITS = 12`.
   A 2026-08-17 report in the same document describes a differently-named test
   (`test_the_season_does_not_end_with_the_crew_holding_sellable_goods`, threshold 51 units) going
   fully XPASS with its marker removed.
   Neither source states whether this is the same xfail renamed and re-thresholded, or a different
   test on a different fixture.
4. **How many crew did Seb hire on day 0?**
   In `what_the_leaders_actually_grow_2026-08-09.md`, a private-bots notebook reports Seb's day-0
   hire count as 14.
   The document's own raw-episode table, extracted directly from the `HIRE` action stream, reports
   Seb's day-0 crew as 7, ramping to 12 by day 10.
   Both are dated 2026-08-09 and neither reconciles the other.

## REGISTER.md carries two stale claims — not fixed here, `REGISTER.md` is off limits for this pass

`docs/REGISTER.md` OPEN-14 (line ~461) says:

- `docs/fable_where_next_2026-08-11.md` was "folded in here; file deleted." **False.** The file was
  read during this consolidation and left as its own file — see below, it is genuinely cross-cutting
  and has no single subject home. It was never folded into `REGISTER.md` and was never deleted.
- `docs/kawashigi_one_board_2026-08-13.md` was "folded into `the_ladder_is_two_scripts.md`; file
  deleted." **Half right, as of today.** The file was not folded or deleted before this pass — it
  was still on disk 2026-08-20, content intact. It has now been folded, but into
  `the_greedy_is_a_mix_scorer_2026-08-20.md` (routing/planner/tape group), not
  `the_ladder_is_two_scripts.md`, and the file is now genuinely deleted.

Whoever next edits `REGISTER.md` should correct both lines.

## The 19 surviving documents

### Read first (unchanged from `CLAUDE.md`'s own list)

| File | What it is |
|---|---|
| `SUPER_IMPORTANT_READ_THIS_FIRST.md` | Top-level briefing. Current as of 2026-08-20. Not touched by this pass beyond receiving no edits at all, per instruction. |
| `competition_brief.md` | What the competition is: measured facts, deadlines, env rules. |
| `architecture.md` | What the agent actually is, and the flags that ship off. Received one folded section (the stage-1 chains/scheduler review). |
| `REGISTER.md` | The live open/closed item list. Left untouched, per instruction — see the stale-claims note above. |
| `rl_feasibility.md` | The agreed position on RL vs planning; the track is parked. Received two folded sections (throughput measurements, problem-framing). The deliberately-preserved, overruled per-step-reward argument is untouched. |
| `lessons_carried_over.md` | What went wrong in Orbit Wars and which lessons transfer. Not touched — no source file targeted it. |
| `economics_q5_findings.md` | The measured economics; overrides the day-1 analysis. Received 10 folded sections (allocation bounds, CEM search, decision points, fable allocation economics, marginal units, q4 variant, fourth-quadrant x2, third-quadrant-late). Now the largest document in `docs/`. |

### Subject survivors, built in this pass

| File | What it is |
|---|---|
| `market_curves_and_the_q4_branch_2026-08-15.md` | Prices, curves, book depth, sell timing. 9 sections folded in. Carries unresolved contradictions 1 and 2 above. |
| `the_greedy_is_a_mix_scorer_2026-08-20.md` | Routing, the day planner, the greedy mix scorer, tape-matching, replay convergence. 13 sections folded in — the largest fold, and now the second-largest document. |
| `geometry_of_the_herd_2026-08-09.md` | Animals: cows, sheep, geese, wool, feed, milk. 8 sections folded in, including the superseded goose-insurance verdict (kept, labelled SUPERSEDED, with the reason). |
| `strawberry_watering_2026-08-16.md` | Crops: watering, fertilizer, harvest, weeds, the shed-discard mechanism. 10 sections folded in, including one disproved hypothesis (kept, labelled DISPROVED, so it is not re-walked). |
| `experiment_log.md` | Session handovers, parity checks, plan-once mechanics. Received a new Part 4 (5 sections). Named in `CLAUDE.md` as the full detail behind the "lessons learned the hard way" list. |
| `the_ladder_is_two_scripts.md` | Current position on strategy vs the field. 4 sections folded in — all downloaded ladder LOSSES; no win rate is computed from them anywhere, per standing project rule. |
| `after_the_close_release_2026-08-15.md` | Late-game turns, d17-d29, season-close mechanics. 6 sections folded in. Carries unresolved contradiction 3 above. |
| `what_the_leaders_actually_grow_2026-08-09.md` | The field: opponent pool, crop mix, what saturates. 3 sections folded in. Carries unresolved contradiction 4 above. |
| `kill_criteria_and_settled_positions.md` | Dead code, stale-doc audits, settled positions. 3 sections folded in, including a punch-list (`work_to_be_done_2026-08-16.md`) that reads more like an economics todo list than kill-criteria — kept here anyway rather than left homeless. |
| `balance_change_eggs_tomatoes_carrots_2026-08-15.md` | The 1.32.7 `hinge` price-shape change. Untouched — cited by filename in `CLAUDE.md`, kept standalone on purpose. |

### Left standalone — no single subject fits it

| File | What it is |
|---|---|
| `fable_where_next_2026-08-11.md` | A prioritised-directions roadmap spanning strawberry dump economics, a parameter-sweep design, production oscillation, herd split and the fourth quadrant. Genuinely cross-cutting; folding it into any one group would have split its ranked-priority structure across five different documents. Kept whole, per the rule that a file with no clean home keeps its file. |

## What was folded where, and what was deleted — 2026-08-20

74 files were deleted with `git rm` (recoverable from git history) after their content was folded
into a survivor document, dated and attributed by source filename.
Full detail, including every contradiction and every misfiled-then-rerouted document, is in
`docs/doc_consolidation_2026-08-20.md`.

**Into `economics_q5_findings.md` (10):** `allocation_bounds_2026-08-16.md`,
`allocation_bounds_pass2_2026-08-16.md`, `cem_allocation_search_2026-08-15.md`,
`decision_points_2026-08-16.md`, `fable_allocation_economics_2026-08-15.md`,
`marginal_units_and_the_shared_book_2026-08-16.md`, `q4_variant_first_draft_2026-08-15.md`,
`fable_fourth_quadrant_2026-08-15.md`, `fable_fourth_quadrant_reopened_2026-08-15.md`,
`the_third_quadrant_arrives_a_day_late_2026-08-17.md`.

**Into `market_curves_and_the_q4_branch_2026-08-15.md` (9):** `the_market_2026-08-09.md`,
`the_market_cadence_over_all_products_2026-08-10.md`, `the_market_is_the_late_season_2026-08-13.md`,
`market_depth_and_the_morning_losses_2026-08-13.md`, `the_book_is_shallow_2026-08-09.md`,
`fable_market_shape_2026-08-09.md`, `when_and_what_to_sell_2026-08-15.md`,
`the_stranded_load_is_the_loss_2026-08-15.md`, `what_the_town_will_actually_eat.md`.

**Into `the_greedy_is_a_mix_scorer_2026-08-20.md` (13):** `the_greedy_is_a_mix_scorer_2026-08-19.md`,
`the_mix_and_the_routes_are_one_artifact_2026-08-19.md`, `the_route_is_precomputable_2026-08-12.md`,
`router_tape_repoint_2026-08-09.md`, `spawn_ring_misprediction_2026-08-12.md`,
`fable_spawn_ring_verdict_2026-08-12.md`, `kawashigi_one_board_2026-08-13.md`,
`fable_matching_the_tape_2026-08-10.md`, `how_sebs_planner_works_2026-08-10.md`,
`the_tape_column_does_not_replay_his_game_2026-08-09.md`, `fable_the_d4_d5_planner_2026-08-11.md`,
`the_day_is_a_cash_ledger.md`, `replay_window_cannot_converge_2026-08-17.md`.

**Into `geometry_of_the_herd_2026-08-09.md` (8):** `how_seb_feeds_the_herd.md`,
`the_goose_is_insurance_2026-08-15.md`, `fable_geese_audit_2026-08-15.md`,
`d6_stranded_wool_2026-08-13.md`, `the_milk_must_be_in_the_shed_by_h05_2026-08-14.md`,
`fable_the_d7_feed_2026-08-11.md`, `the_wheat_row_and_the_turns_own_spending_2026-08-14.md`,
`fable_the_wheat_churn_2026-08-09.md`.

**Into `strawberry_watering_2026-08-16.md` (10):** `carrot_swap_2026-08-12.md`,
`carrot_and_the_empty_book_2026-08-19.md`, `the_tapes_are_both_strawberry_rich_2026-08-19.md`,
`d18_harvest_and_sells_2026-08-12.md`, `d16_fertilizer_starvation_2026-08-12.md`,
`d6_water_2026-08-13.md`, `the_last_growing_days_water_2026-08-14.md`,
`fable_watering_post_d8_2026-08-15.md`, `where_the_harvest_gap_is_2026-08-15.md`,
`fable_the_discard_problem_2026-08-09.md`.

**Into `experiment_log.md` (5):** `arena_state_leak_2026-08-09.md`, `handoff_2026-08-15.md`,
`handoff_plan_once_2026-08-09.md`, `parity_restored_on_1326_2026-08-09.md`,
`plan_once_and_the_dawn_blind_spots_2026-08-09.md`.

**Into `the_ladder_is_two_scripts.md` (4):** `ladder_losses_2026-08-11.md`,
`the_ladder_is_lost_by_a_nose_2026-08-13.md`, `three_ladder_games_2026-08-15.md`,
`two_losses_2026-08-15b.md`.

**Into `after_the_close_release_2026-08-15.md` (6):** `fable_close_the_season_2026-08-15.md`,
`fable_brief_sell_the_close_2026-08-15.md`, `the_last_two_days_2026-08-17.md`,
`wasted_late_turns_2026-08-17.md`, `fable_production_decay_d19_2026-08-15.md`,
`the_late_season_is_one_defect_in_two_halves_2026-08-12.md`.

**Into `what_the_leaders_actually_grow_2026-08-09.md` (3):** `the_top_five_clusters_2026-08-09.md`,
`what_saturates_and_what_does_not_2026-08-09.md`, `the_field.md`.

**Into `kill_criteria_and_settled_positions.md` (3):** `dead_constant_audit_2026-08-17.md`,
`stale_audit_2026-08-15.md`, `work_to_be_done_2026-08-16.md`.

**Into `rl_feasibility.md` (2):** `throughput_measurements.md`, `what_kind_of_problem_this_is.md`.

**Into `architecture.md` (1):** `fable_stage1_review_2026-08-09.md`.

**Not folded, kept as its own file (1):** `fable_where_next_2026-08-11.md`.
