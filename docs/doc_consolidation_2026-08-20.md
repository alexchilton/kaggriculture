# docs/ consolidation — 2026-08-20

## Before / after

**Before:** 93 markdown files in `docs/`, most of them one-off session notes.
**After:** 19 files: 9 unchanged read-first documents (one, `SUPER_IMPORTANT_READ_THIS_FIRST.md`,
received zero edits per instruction; `REGISTER.md` likewise untouched), 9 subject-survivor documents
that absorbed everything else, and one file (`fable_where_next_2026-08-11.md`) kept standalone
because it is genuinely cross-cutting and had no single subject home.

No measurement was deleted.
Every folded section is dated, carries a `Folded in from docs/<original>.md.` attribution line, and
keeps tables and dollar figures verbatim or near-verbatim.
74 files were removed with `git rm`, so every one is recoverable from git history.

## Method

Twelve subject-area sonnet agents ran in parallel, each reading its target survivor document plus
its assigned source files in full, then editing the survivor in place.
Agents were instructed to flag, not force, any source file that on full read did not belong to their
group — six files were caught this way and rerouted by hand afterward (see "Files rerouted" below).
Agents were also instructed never to resolve a genuine contradiction by picking a winner; four such
contradictions survived the fold and are listed below and at the top of `docs/README.md`.

## Mapping: what was folded into what

| Survivor | Files folded in | Count |
|---|---|---|
| `economics_q5_findings.md` | allocation_bounds_2026-08-16, allocation_bounds_pass2_2026-08-16, cem_allocation_search_2026-08-15, decision_points_2026-08-16, fable_allocation_economics_2026-08-15, marginal_units_and_the_shared_book_2026-08-16, q4_variant_first_draft_2026-08-15, fable_fourth_quadrant_2026-08-15, fable_fourth_quadrant_reopened_2026-08-15, the_third_quadrant_arrives_a_day_late_2026-08-17 | 10 |
| `market_curves_and_the_q4_branch_2026-08-15.md` | the_market_2026-08-09, the_market_cadence_over_all_products_2026-08-10, the_market_is_the_late_season_2026-08-13, market_depth_and_the_morning_losses_2026-08-13, the_book_is_shallow_2026-08-09, fable_market_shape_2026-08-09, when_and_what_to_sell_2026-08-15, the_stranded_load_is_the_loss_2026-08-15, what_the_town_will_actually_eat | 9 |
| `the_greedy_is_a_mix_scorer_2026-08-20.md` | the_greedy_is_a_mix_scorer_2026-08-19, the_mix_and_the_routes_are_one_artifact_2026-08-19, the_route_is_precomputable_2026-08-12, router_tape_repoint_2026-08-09, spawn_ring_misprediction_2026-08-12, fable_spawn_ring_verdict_2026-08-12, kawashigi_one_board_2026-08-13, fable_matching_the_tape_2026-08-10, how_sebs_planner_works_2026-08-10, the_tape_column_does_not_replay_his_game_2026-08-09, fable_the_d4_d5_planner_2026-08-11, the_day_is_a_cash_ledger, replay_window_cannot_converge_2026-08-17 | 13 |
| `geometry_of_the_herd_2026-08-09.md` | how_seb_feeds_the_herd, the_goose_is_insurance_2026-08-15, fable_geese_audit_2026-08-15, d6_stranded_wool_2026-08-13, the_milk_must_be_in_the_shed_by_h05_2026-08-14, fable_the_d7_feed_2026-08-11, the_wheat_row_and_the_turns_own_spending_2026-08-14, fable_the_wheat_churn_2026-08-09 | 8 |
| `strawberry_watering_2026-08-16.md` | carrot_swap_2026-08-12, carrot_and_the_empty_book_2026-08-19, the_tapes_are_both_strawberry_rich_2026-08-19, d18_harvest_and_sells_2026-08-12, d16_fertilizer_starvation_2026-08-12, d6_water_2026-08-13, the_last_growing_days_water_2026-08-14, fable_watering_post_d8_2026-08-15, where_the_harvest_gap_is_2026-08-15, fable_the_discard_problem_2026-08-09 | 10 |
| `experiment_log.md` | arena_state_leak_2026-08-09, handoff_2026-08-15, handoff_plan_once_2026-08-09, parity_restored_on_1326_2026-08-09, plan_once_and_the_dawn_blind_spots_2026-08-09 | 5 |
| `the_ladder_is_two_scripts.md` | ladder_losses_2026-08-11, the_ladder_is_lost_by_a_nose_2026-08-13, three_ladder_games_2026-08-15, two_losses_2026-08-15b | 4 |
| `after_the_close_release_2026-08-15.md` | fable_close_the_season_2026-08-15, fable_brief_sell_the_close_2026-08-15, the_last_two_days_2026-08-17, wasted_late_turns_2026-08-17, fable_production_decay_d19_2026-08-15, the_late_season_is_one_defect_in_two_halves_2026-08-12 | 6 |
| `what_the_leaders_actually_grow_2026-08-09.md` | the_top_five_clusters_2026-08-09, what_saturates_and_what_does_not_2026-08-09, the_field | 3 |
| `kill_criteria_and_settled_positions.md` | dead_constant_audit_2026-08-17, stale_audit_2026-08-15, work_to_be_done_2026-08-16 | 3 |
| `rl_feasibility.md` | throughput_measurements, what_kind_of_problem_this_is | 2 |
| `architecture.md` | fable_stage1_review_2026-08-09 | 1 |
| **Total folded and deleted** | | **74** |
| **Kept standalone, not folded** | fable_where_next_2026-08-11 | 1 |

All filenames above omit the trailing `.md` for brevity; the full names are in `docs/README.md`.

## Files rerouted after the first-pass grouping was wrong

Six files were assigned to a group by filename at planning time and turned out, on full read, not to
belong there. The agent handling that group correctly declined to force them in and flagged the
better home instead:

- `the_day_is_a_cash_ledger.md` — planned for the field/opponents group; is actually about our own
  `sell_deadline`/ledger design bug. Rerouted to the routing/planner group.
- `replay_window_cannot_converge_2026-08-17.md` — planned for the season-close group; is actually
  about d5-d11 tape-replay convergence, an early/mid-game mechanic. Rerouted to the routing/planner
  group.
- `fable_the_discard_problem_2026-08-09.md` — planned for the market group; is actually about
  shed-overflow discard of harvested product. Rerouted to the crops/watering group.
- `the_wheat_row_and_the_turns_own_spending_2026-08-14.md` — planned for the crops/watering group; is
  actually about order-slot bank debiting and the milk shed-deposit mechanic. Rerouted to the
  animals/herd group.
- `fable_the_wheat_churn_2026-08-09.md` — planned for the crops/watering group; is actually about the
  herd's feed-buy day budget. Rerouted to the animals/herd group.
- `fable_where_next_2026-08-11.md` — planned for the session/parity group; is a cross-cutting
  prioritised-directions roadmap with no single subject. Left standalone, not folded anywhere.

## Unresolved contradictions found

Four. None were resolved by picking a winner. Each is marked
`**UNRESOLVED CONTRADICTION — needs a measurement.**` inline in the document named, and all four are
also listed at the top of `docs/README.md`.

1. **Does MILK actually floor at $1-5 on the real ladder?**
   `market_curves_and_the_q4_branch_2026-08-15.md`: one 2026-08-13 section reads 3 real ladder
   episodes where MILK never floors; a different 2026-08-13 section in the same document reads 5
   different real ladder episodes the same day showing MILK closing at $1-$5 repeatedly.
2. **Does keeping melon volume beat swapping to strawberry?**
   Same document: a model concludes keeping melon wins by $8,162; a real lost ladder game
   (`92562037`) elsewhere in the document shows 19-for-19 melon closing at $25, read there as costly
   overplanting.
3. **What is the real stranded-produce threshold at season close, 16 units or 51?**
   `after_the_close_release_2026-08-15.md`: a 2026-08-15 report measures 16 units against
   `TOLERATED_UNITS = 12`; a 2026-08-17 report describes a differently-named test at a 51-unit
   threshold going fully XPASS. Neither source states whether this is the same fixture renamed.
4. **How many crew did Seb hire on day 0, 14 or 7?**
   `what_the_leaders_actually_grow_2026-08-09.md`: a private-bots notebook says 14; the document's
   own raw-episode table, extracted from the `HIRE` action stream, says 7 ramping to 12 by day 10.

## Things noticed along the way, not part of the ask, reported for the record

- **`docs/REGISTER.md` carries two stale claims**, found while folding the routing group.
  `OPEN-14` (line ~461) says `fable_where_next_2026-08-11.md` was "folded in here; file deleted" —
  false, the file exists and was never folded into `REGISTER.md`.
  It also says `kawashigi_one_board_2026-08-13.md` was "folded into `the_ladder_is_two_scripts.md`;
  file deleted" — false before this pass (the file was still on disk, untouched), and now half-true:
  the file is deleted as of this consolidation, but it was folded into
  `the_greedy_is_a_mix_scorer_2026-08-20.md`, not `the_ladder_is_two_scripts.md`.
  `REGISTER.md` was left untouched per instruction; both lines need a manual fix by whoever next
  edits that file.
- **One same-day self-retraction, kept explicit rather than deleted:** `fable_fourth_quadrant_2026-08-15.md`
  concluded "no path, closed by the crew cost" ($21,960); `fable_fourth_quadrant_reopened_2026-08-15.md`,
  same author, same day, retracted that after reading 60 fresh episodes and found a narrow conditional
  path worth ~+$7.5k. Both sections are in `economics_q5_findings.md` in full, with the retraction made
  explicit — this was not tagged as an unresolved contradiction because the second document explicitly
  retracts the first in its own text.
- **One same-day supersession, kept labelled rather than deleted:** the 2026-08-19 "opponent lead"
  classifier finding in the routing group was killed by a 2026-08-20 re-measurement (pseudo-replication,
  placement-level vs game-level). Both versions are in `the_greedy_is_a_mix_scorer_2026-08-20.md`, the
  earlier one labelled superseded with the mechanism stated.
- **One self-corrected contradiction resolved by the source itself, not by an agent:** in the
  crops/watering fold, `where_the_harvest_gap_is_2026-08-15.md`'s premise (water +65 over the tape)
  is numerically incompatible with `fable_watering_post_d8_2026-08-15.md`'s later, independently
  instrumented count on the same tape (water 798 vs 795, no shortfall). `where_the_harvest_gap_is`
  is self-labelled DISPROVED in its own source text, so this was not a live contradiction for the
  agent to adjudicate — it was folded in already marked disproved, with its original hypothesis and
  unrun experiment preserved verbatim underneath, per the rule not to delete reasoning that prevents
  a repeat.

## Commits

Twelve `git rm` + commit passes, one per subject group, plus this report and the `README.md`
rewrite. All on the working branch, not pushed, not merged, not rebased.
