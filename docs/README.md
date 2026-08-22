# docs/ — index

**Consolidated 2026-08-22.** 120 files, no index past 2026-08-15. This section is the current one —
read it first and stop there unless you need history. Everything below the `---` after "The rules
that survived the cull" is the 2026-08-08 through 2026-08-15 consolidation record, kept for history,
not rewritten. Full method, classification counts and every contradiction found this pass:
`docs/consolidation_2026-08-22.md`.

## Read first

| File | What it is |
|---|---|
| `SUPER_IMPORTANT_READ_THIS_FIRST.md` | **Not previously indexed — read this before touching agent code.** 2026-08-20. Docstrings that lie about what the code does (five found in one session); measure a rule at the decision, not the season census (11.5% → 55.8% → 77.9% on the SAME rule); the golden-output grid as the only refactor lock; a list of things measured DEAD that must not be resurrected (the kawashigi tape replay, the milk LINE rule, `_Q4.arm`/`_MB.arm`). |
| `REGISTER.md` | **The live open/closed list.** Owned live — read it, do not edit it outside its own process. Check before opening anything. |
| `competition_brief.md` | The rules, the scoring rule, and the version-skew history (1.32.2 → 1.32.6 → 1.32.7). Current — already carries the 1.32.7 "hinge" update. |
| `architecture.md` | What the agent is, and the flags that ship off. Current for design; its bottom parity/dollar table is 1.32.2-era, self-flagged. |
| `kill_criteria_and_settled_positions.md` | Every kill criterion: MET or CLOSED. The terminal-reward ruling and the RL-parked ruling live here, with the measurements. |
| `REGISTER.md`, `SUPER_IMPORTANT_READ_THIS_FIRST.md` and `stale_audit_2026-08-15.md` between them replace the need to read the 2026-08-08–15 layers below for day-to-day work. |

## The current field and strategy picture

| File | What it is |
|---|---|
| `the_field_is_a_monoculture_2026-08-21.md` | **Current, largest sample (1,010 games).** Of 58 sampled players only the top 4 ranked ones are genuinely distinct agents; 38 of 58 share one byte-identical opening. Kawashigi's one reactive rule: opponent melon tiles ≥9 at d3. |
| `the_field.md` | 2026-08-09-era "winners are open-loop scripts" finding. Structural claim still holds; dollar figures superseded (self-banered); now also points forward to `the_field_is_a_monoculture_2026-08-21.md`. |
| `the_ladder_is_two_scripts.md` | 2026-08-11, 2,744 seats. Recommended rebasing on Dmitry Belan or Efe Can Celiksoy. **unsure — needs an owner's eye:** nothing since has used either target, and `REGISTER.md` OPEN-10 (this exact item) is not marked closed. See `consolidation_2026-08-22.md` contradiction 5. |
| `kawashigi_one_board_2026-08-13.md` | The ladder deals one fixed board; only the shop-unlock draw and weeds vary. Current, with a note added this pass: qualified (not overturned) by `marginal_units_and_the_shared_book_2026-08-16.md` §9's finding that the draw is agent-dependent, not seed-only. |
| `kawashigi_algorithm_2026-08-21.md` | **Retracted the same day it was written** (its own banner) — see `the_middle_is_not_board_capacity_2026-08-21.md`. |
| `the_middle_is_not_board_capacity_2026-08-21.md` | Current. Falsifies the board-capacity claim: Kawashigi leaves the board non-full on 85.7% of mid-season days; his day is turn-bound, not menu-bound. |
| `the_opening_is_a_tape_the_middle_is_two_regimes_2026-08-21.md` | Current. d0-d12 replay matches the tape exactly (0 differing cells); reconciles with the board-capacity file rather than contradicting it. |
| `ryo_tetsuya_vs_kawashigi_2026-08-21.md` | Current. Both play a scalar wheat-fill mid-season; carrot is what separates a third player (Ryo). Self-corrects an earlier 9-seat sample. |
| `day_blocks_2026-08-20.md` | Current. A decision tree predicts Kawashigi's daily action block 83.6% at d6, collapsing to ~5% by d17+ — the season is a per-day problem a per-turn model can't see. Retracts an earlier "frozen five-day opening" claim as a 9-game artifact. |
| `the_arm_is_the_whole_model_2026-08-20.md` | Current. A board-free (day,hour,slot) lookup beats a board-keyed one; roadmap toward an arm classifier. |
| `the_library_agent_and_where_kawa_parts_2026-08-21.md` | Current, negative result: a modal-row library agent loses to the shipped greedy planner, $68,445 vs $109,270 — over-plants 45% for no extra harvest. |
| `decision_points_2026-08-16.md` | Current. The d6 YARN_STORE fourth-quadrant switch is real (+9.4pp); the d3 melon-threshold "switch" was never actually tested (the test opponent always holds 12 tiles by construction). |
| `allocation_bounds_2026-08-16.md` / `allocation_bounds_pass2_2026-08-16.md` | Pass1 SUPERSEDED by pass2 same day (banner added). Pass2 current: near-optimal allocation bands from an MILP, and an independent derivation of the same melon-threshold-9 finding as `decision_points_2026-08-16.md`. |
| `cem_allocation_search_2026-08-15.md` | unsure — needs an owner's eye. Still reads RESULT PENDING; no completion found. Banner added pointing at `allocation_bounds_pass2_2026-08-16.md`. |
| `the_top_five_clusters_2026-08-09.md`, `what_the_leaders_actually_grow_2026-08-09.md` | SUPERSEDED (own banners, confirmed still accurate). 15/20-replay-scale field descriptions, superseded by the 2,744-seat and 1,010-game samples above. |

## Matching a reference tape — mechanism work (read the file's own banner for its target)

Every file below diagnoses a real bug against a recorded tape. The **target** (whose tape) has moved
three times: Seb → Victor/Kawashigi → tetsuya. A file's bug-level finding usually survives a target
change; its "we now match X" framing usually does not. Files already carry their own banner where
this applies — trust the banner over the file title.

**Seb target — all carry "TARGET SUPERSEDED, added 2026-08-11" (Seb's tape was optimal under the
old economy; his bank halved and he withdrew from the ladder):**
`fable_matching_the_tape_2026-08-10.md`, `how_sebs_planner_works_2026-08-10.md`,
`how_seb_feeds_the_herd.md`, `the_day_is_a_cash_ledger.md`,
`the_market_cadence_over_all_products_2026-08-10.md`, `plan_once_and_the_dawn_blind_spots_2026-08-09.md`,
`handoff_plan_once_2026-08-09.md`, `router_tape_repoint_2026-08-09.md`,
`the_tape_column_does_not_replay_his_game_2026-08-09.md`. Read as HISTORICAL — the bug findings each
one names are still real per its own banner; the "matches Seb" framing is not the goal.

**Victor / Kawashigi / tetsuya target — current diagnostic lineage, in date order:**

| File | What it is |
|---|---|
| `fable_the_d4_d5_planner_2026-08-11.md`, `fable_the_d7_feed_2026-08-11.md` | Victor tape. Two shipped, tested fixes (`hold_farmer`/`farmer_start`, dawn-block persistence) closing d4-d7 divergence. |
| `fable_where_next_2026-08-11.md` | Victor tape. Prioritised roadmap; ranks the late-season strawberry/melon dump as the top open item. Superseded in confidence (not direction) by the 2026-08-15 fourth-quadrant pair below on its D6 item. |
| `ladder_losses_2026-08-11.md` | Real losses (10, explicitly a losses sample). Melon denial-play arithmetic; later extended by `marginal_units_and_the_shared_book_2026-08-16.md`. |
| `spawn_ring_misprediction_2026-08-12.md`, `fable_spawn_ring_verdict_2026-08-12.md` | Open, unfixed: dawn hand-arrival prediction disagrees with actual hour-0 position, costing a tile to weed. Real fix untried. |
| `the_route_is_precomputable_2026-08-12.md` | Current reasoning (map is fixed, offline solve is valid); the *specific* route tables it justifies are separately stale (see `SUPER_IMPORTANT_READ_THIS_FIRST.md` §8). |
| `d16_fertilizer_starvation_2026-08-12.md`, `d18_harvest_and_sells_2026-08-12.md` | Current, open. Same root mechanism (`FERTILIZER_RESERVE_LOOKAHEAD_DAYS`) at two different days. |
| `the_late_season_is_one_defect_in_two_halves_2026-08-12.md` | Diagnosis; note added pointing to where it was implemented (`the_market_is_the_late_season_2026-08-13.md`). |
| `d6_stranded_wool_2026-08-13.md` | Shipped fix: `SHIP_WHAT_NO_LATER_STOP_CAN_BANK`. Current. |
| `d6_water_2026-08-13.md` | HISTORICAL — measured a net loss same day, reverted. |
| `market_depth_and_the_morning_losses_2026-08-13.md` | Current. Full market-depth table; diagnoses 5 real losses to a `_herd_split` bug. |
| `the_market_is_the_late_season_2026-08-13.md` | Current. Implements `LATE_SEASON_PAIR`; self-corrects a milk-floor claim mid-file as a harness artifact. |
| `the_ladder_is_lost_by_a_nose_2026-08-13.md` | Current for loss-magnitude figures; self-corrects a win-rate claim inline (Alex: "I only download the losses"). |
| `the_last_growing_days_water_2026-08-14.md` | HISTORICAL — own banner: "DIAGNOSED, FIX REVERTED, DO NOT RETRY AS WRITTEN." |
| `the_milk_must_be_in_the_shed_by_h05_2026-08-14.md` | Current. Ships `BANK_ON_THE_PEN_THAT_FUNDS_THE_DAY`. |
| `the_wheat_row_and_the_turns_own_spending_2026-08-14.md` | HISTORICAL — own status line: diagnosed, reverted; ends by superseding its own framing. |
| `three_ladder_games_2026-08-15.md`, `two_losses_2026-08-15b.md` | Current, real downloaded losses. |
| `handoff_2026-08-15.md` | HISTORICAL — mid-investigation snapshot; the route regen it describes running is superseded by later work. |
| `fable_production_decay_d19_2026-08-15.md`, `fable_watering_post_d8_2026-08-15.md` | Current at the rule level; per-tile numbers self-flagged as route-sensitive. |
| `the_stranded_load_is_the_loss_2026-08-15.md` | CLOSED by `the_last_two_days_2026-08-17.md` (banner added). |
| `fable_close_the_season_2026-08-15.md`, `fable_brief_sell_the_close_2026-08-15.md` | Current / HISTORICAL (brief, answered by the first). |
| `after_the_close_release_2026-08-15.md` | Current — the release that followed. |
| `the_last_two_days_2026-08-17.md` | Current — closes the stranded-load gap; full season **+$415 ahead of tape**. See contradiction 6 in the consolidation doc against item below. |
| `replay_window_cannot_converge_2026-08-17.md` | HISTORICAL — settled dead end, diagnostic only. |
| `the_third_quadrant_arrives_a_day_late_2026-08-17.md`, `wasted_late_turns_2026-08-17.md` | Current, open, unfixed. |
| `dead_constant_audit_2026-08-17.md`, `flag_audit_2026-08-20.md` | Current — code-health audits (17 and 14+4 dead constants/lines found respectively). Read before deleting anything, per the NO FLAGS rule. |
| `strawberry_watering_2026-08-16.md` | Current, shipped fix (`_trim_to_the_day`). Flags `work_to_be_done_2026-08-16.md`'s baseline table as stale — see contradiction 7. |
| `marginal_units_and_the_shared_book_2026-08-16.md` | Current, but **read the whole file** — it self-voids three of its own earlier sections as it goes (§3, §5-6, §8). |
| `work_to_be_done_2026-08-16.md` | Current, most actionable punch list of the batch. One baseline table disagrees with `strawberry_watering_2026-08-16.md`'s re-measurement — see contradiction 7. |
| `our_geometry_is_not_his_2026-08-20.md`, `plant_is_a_money_problem_2026-08-20.md` | Current, complementary (geometry vs cash) diagnoses on the same tetsuya board. |
| `the_day_idles_while_the_herd_starves_2026-08-20.md` | Current — explains the `SUPER_IMPORTANT_READ_THIS_FIRST.md` headline "PASS 911 vs 679" mechanism directly. |
| `the_ration_is_not_in_the_shed_when_the_plan_says_it_is_2026-08-20.md`, `the_sells_land_after_the_hire_2026-08-20.md` | Current, companion diagnoses, same board. |
| `feed_is_measured_against_ops_he_wasted_2026-08-20.md` | Current — the FEED 73/76 correction `SUPER_IMPORTANT_READ_THIS_FIRST.md` cites. |
| `the_tape_dies_at_d13_2026-08-20.md` | Current — a `(day,hour,unit)` tape clone dies at d13 from a weed cascade; measures the q4 arm at ~+$15k median. |
| `d0_to_d3_cell_by_cell_2026-08-21.md`, `d1_bank_cadence_handoff_2026-08-21.md` | Current, in-progress; the second is an explicit open decision for Alex (a rule that wins on Seb's tape and loses 3 cells against Kawashigi's). |
| `seed_outranks_product_the_fix_and_its_cost_2026-08-21.md` | unsure — needs an owner's eye. A real fix (+$5,516 by d12) that regresses the shipped-agent gate (263→301 failing cells). Explicit "do not ship as-is." |
| `the_executor_cannot_play_his_own_row_2026-08-21.md` | Current — companion diagnosis to the file above, same game, same defect family. |
| `the_carrot_window_is_three_days_2026-08-21.md` | Current — narrows a broad carrot perturbation (a loss) to a 3-day window (near-break-even). |
| `the_tape_beats_our_planner_2026-08-21.md` | Current — most recent, most rigorous tape/planner comparison; fixes 3 one-line bugs; flags game `94469635` (tomato-heavy) as a possibly-worth-adopting fifth tape target. See contradiction 6. |

## Market mechanics, economics and the animal-produce books

| File | What it is |
|---|---|
| `the_market_2026-08-09.md` | Current for the sell-rule mechanism and §5; §2's absorption table is self-flagged superseded — read `what_the_town_will_actually_eat.md` instead. |
| `what_the_town_will_actually_eat.md` | Current. 87 tapes: melon and fertilizer always oversupplied, wheat always scarce. |
| `what_saturates_and_what_does_not_2026-08-09.md` | Current, corrected saturation table. Its CARROT/TOMATO/EGG rows predate the 2026-08-15 hinge change — not re-verified since. |
| `economics_q5_findings.md` | Current for §1/§3/§5 (yields, supply, storage); §2/§4 self-flagged superseded by `what_the_town_will_actually_eat.md`. |
| `market_curves_and_the_q4_branch_2026-08-15.md` | Current for the market-curve tables (§1-6); §7's q4 number is superseded — note added pointing to `q4_variant_first_draft_2026-08-15.md`. |
| `q4_variant_first_draft_2026-08-15.md` | Current — the more rigorous q4 measurement, -$716 mean, not distinguishable from zero, 11/11 win on armed seeds. Own verdict: "worth pursuing, not in this form." |
| `market_depth_and_the_morning_losses_2026-08-13.md` | Current — full depth/floor table, 5 real losses diagnosed. |
| `when_and_what_to_sell_2026-08-15.md` | **STALE** (banner added) — its headline total and its own falsifiable prediction are both contradicted elsewhere and never corrected in the file. |
| `the_book_is_shallow_2026-08-09.md` | Current for the surviving claims (self-corrected banner already present: price-curve math and the melon-no-shop finding survive; the absorption-by-seed method does not). |
| `carrot_and_the_empty_book_2026-08-19.md` | Current — clean, fills-not-offers measurement: carrot nets 13-25% less than wheat as a season staple; use only as an end-of-season closer. |
| `carrot_swap_2026-08-12.md` | SUPERSEDED (banner added) by the file above; its own arms were already self-retracted twice in-file. |
| `fable_allocation_economics_2026-08-15.md` | Current — post-1.32.7. No unconditional edge to wheat→carrot/tomato conversion; conditional on the d12 shop draw. |
| `fable_market_shape_2026-08-09.md` | Current, with a caveat: `LATE_SELL_BIAS`'s +12.5pp win-rate gain is real on 8 seeds but not yet confirmed on the wider sweep this project otherwise requires. |
| `balance_change_eggs_tomatoes_carrots_2026-08-15.md` | Current — primary source for the 1.32.7 "hinge" pricing rule and the required version bump. |
| `the_greedy_is_a_mix_scorer_2026-08-19.md` / `_2026-08-20.md` | Current — read as a pair; the 08-20 file retracts one subclaim of the 08-19 file (an "opponent lead" correlation, re-measured per-game rather than per-placement) and extends the rest to 88.5% herd-placement match. |
| `the_mix_and_the_routes_are_one_artifact_2026-08-19.md` | Current — a melon arm with zero crop-mix change gained +$5,615 purely from re-solving stale routes; resolves the geese question again (`swap_in_geese` itself is the defect). |
| `the_tapes_are_both_strawberry_rich_2026-08-19.md` | HISTORICAL — own "MEASURED AND REVERTED" marker; a strawberry cap lost $28,259 across four arms. |
| `the_market_is_one_token_not_nine_heads_2026-08-20.md` | Current — explains why nine independent per-head market marginals emit zero orders; flags its own target risk (tetsuya no longer #1 as of 2026-08-20). |
| `arena_state_leak_2026-08-09.md` | Current — `run_arena` state-leak bug found and fixed; resolves an old 94.4%-vs-14.6% discrepancy as measurement contamination. |
| `geometry_of_the_herd_2026-08-09.md` | Current — pen geometry confirmed not a lever a third time; corrects an older "1.86 vs 2.93" figure in-file. |
| `parity_restored_on_1326_2026-08-09.md` | Current for the four 1.32.6 rule fixes; its specific price-literal table predates the 1.32.7 hinge change. |
| `fable_the_discard_problem_2026-08-09.md` | Own banner: headline discard numbers were 15x overstated, corrected in-file. The day-gate bug fix and harness-stability finding survive. |
| `fable_the_wheat_churn_2026-08-09.md` | Current, shipped fix (`FEED_BUY_CEILING_DAYS = 2`). |
| `fable_stage1_review_2026-08-09.md` | Bug findings current; the priority call (chase a public agent's opening before reviving stage 1) was point-in-time. |

## Herd, animals, geese

`REGISTER.md` OPEN-17 is the live entry. Read these in date order — the goose question has been
re-derived at least six times in this corpus:

| File | What it is |
|---|---|
| `fable_geese_audit_2026-08-15.md` | Current — closes geese on the Elo (margin) objective: best in only 0.9% of shop draws, because withdrawing from the milk/wool books gifts the opponent price suppression. |
| `the_goose_is_insurance_2026-08-15.md` | unsure — needs an owner's eye. Self-retracts its own dollar figures mid-file (opponent volumes were offers, not fills); its qualitative conclusion (geese are insurance, not a general win) agrees with the file above. |
| `the_market_is_the_late_season_2026-08-13.md`, `the_mix_and_the_routes_are_one_artifact_2026-08-19.md` | Both re-derive a geese verdict and both call theirs "the fifth" — the numbering across files disagrees; treat as roughly the fifth and sixth independent re-derivations, not a contradiction to resolve. |
| `three_ladder_games_2026-08-15.md`, `two_losses_2026-08-15b.md` | Current — real losses showing milk/wool floored, a cow starved by a feed miss. |

## BC / imitation pipeline and the RL ruling

| File | What it is |
|---|---|
| `the_bc_pipeline_2026-08-20.md` | Current — essential pre-read before trusting any BC training metric; nine defects found, including a 52%-of-legal-sells mask veto. |
| `the_imitation_pipeline_2026-08-20.md` | Current — active BC→DAgger→RL plan. |
| `fable_bundle_head_review_2026-08-20.md` | Current, most fundamental of the pair below: the flagship legality mask (`masks_for`) has never once executed (`state.private.shed` does not exist). |
| `fable_bc_pipeline_review_2026-08-20.md` | Current, with a cross-reference note added this pass to the file above. |
| `rl_feasibility.md` | Current — the RL ruling, self-corrected in-file (terminal reward, RL parked). |
| `kill_criteria_and_settled_positions.md`, `lessons_carried_over.md` | Current — settled positions and the Orbit Wars distillation. |
| `throughput_measurements.md` | HISTORICAL — its strategic conclusion ("build a vectorized sim for RL") is superseded by the RL-parked ruling; the throughput numbers themselves are presumably still accurate. |
| `what_kind_of_problem_this_is.md` | Current framing; dollar figures inside self-flagged as pre-1.32.6 / method-only. |
| `fable_stage1_review_2026-08-09.md` | See market section above. |

## Losses analyzed (read the bias warning in each)

| File | What it is |
|---|---|
| `ladder_losses_2026-08-11.md` | Self-flags: "THIS IS A SAMPLE OF LOSSES, NOT A RECORD." |
| `the_ladder_is_lost_by_a_nose_2026-08-13.md` | Self-corrects a win-rate claim the same day (Alex: downloaded games are losses only). |
| `three_ladder_games_2026-08-15.md`, `two_losses_2026-08-15b.md`, `wasted_late_turns_2026-08-17.md` | Current, real losses, each states its own sample size. |
| `why_we_lost_93318573_93323101.log` | Not a doc — raw script-output dump for two loss episodes. Not indexed further; consider moving to `data/logs/`. |

## Known unresolved contradictions

Full detail, with numbers, in `docs/consolidation_2026-08-22.md`. In order of how much they can
cost a reader:

1. Melon-swap direction: two in-repo docs vs. root `RETRACTIONS.md` item 7's 960-game sweep disagree.
2. Whether the shop draw is seed-only or agent-dependent (`kawashigi_one_board_2026-08-13.md` vs
   `marginal_units_and_the_shared_book_2026-08-16.md` §9).
3. `REGISTER.md`'s own baseline command names a retired tape (`seb`) and cannot run as written.
4. Whether fast-sim parity is actually green right now is unverified; `CLAUDE.md` states it as fact
   with no version qualifier.
5. The 2026-08-11 rebase recommendation (Dmitry Belan / Efe Can Celiksoy) was never adopted and
   `REGISTER.md` OPEN-10 is not marked closed.
6. Two "our agent vs the kawashigi tape" season numbers, from different measurement setups, do not
   reconcile (`the_last_two_days_2026-08-17.md` vs `the_tape_beats_our_planner_2026-08-21.md`).
7. `work_to_be_done_2026-08-16.md`'s tape-gate baseline disagrees with the same-day re-measurement in
   `strawberry_watering_2026-08-16.md`.

---

**Updated 2026-08-15.** Read this section before anything below it: several of the framings further
down were overturned today, and the file dated 2026-08-11 that follows still states them.

## Read first, 2026-08-15

| File | What it is |
|---|---|
| `REGISTER.md` | **The live open/closed list.** Repaired today — it was corrupted at line 1 and seven days stale on this branch. Check it before opening anything. |
| `stale_audit_2026-08-15.md` | What else in here is measured on a tape we no longer ship, through a bug now fixed, or against a flag that no longer exists. Start here before trusting any older doc. |
| `fable_allocation_economics_2026-08-15.md` | The 1.32.7 hinge priced and validated against the organisers' own figures (carrot 25.8 / tomato 53.4 / egg 22.4%). Unconditional wheat->carrot/tomato conversion has **no edge**; the play is conditional on 2+ tomato shops visible by d12. |
| `fable_geese_audit_2026-08-15.md` | **Geese are closed on the Elo objective** — margin-best in 0.9% of shop draws, because exiting the flooded milk/wool books gifts the opponent ~$9-10k of price suppression. Corrects the goose yield (44, not 46) and my own cow/sheep revenue model. |
| `fable_fourth_quadrant_2026-08-15.md` | No path to a 4th quadrant. Land is affordable from d11; the fibonacci hire curve costs ~$21,960 against at most $15,298 of crop. |
| `three_ladder_games_2026-08-15.md` | Read off real ladder replays: neither the escaped animal nor solved-route seating predicts the result. Both animal books flooring does — 1W/4L against 10W/3L. |
| `the_goose_is_insurance_2026-08-15.md` | My own arithmetic, **superseded on its conclusion** by the audit above. Kept only for the dating that reopened the question: `HERD_GEESE` was measured 2026-08-11/12 and `c99a8a5` fixed `SELLABLE` on 2026-08-13, so that verdict was taken while every egg was unsellable. |
| `where_the_harvest_gap_is_2026-08-15.md` | A hypothesis I then **disproved** — labelled as such inside. `WATER_ROTATION` is not the cause of `harvest -19`; crop decay and unseated harvests are. |

**Two mechanism findings from 2026-08-15 that are not in any older doc:**

- `_decay_plants` runs on **every step**, not the rollover, so a one-shot crop's safe harvest window
  is **exactly one day wide** and water does not extend it. That is a second weed source alongside
  `consecutive_unwatered >= 2`, and `cover.py` cannot see it.
- `cover._apply_precomputed` returns before the budget check and matches jobs on `(tile, ops)`
  alone, so on **d12-d29 neither the turn budget nor a job's prize is enforced**.

---

**Consolidated 2026-08-11**, on top of the 2026-08-09 consolidation below.
The trigger: `scripts/episode_index.py` pulled the official episode datasets for 2026-08-09 and
-08-10 — 1,372 episodes, 2,744 seats — giving this project its first population-scale read of the
field, alongside a fresh reading of 87 recorded ladder tapes' closing market state. Two things it
found overturn the working assumption behind most of this week's "matching-the-tape" work: **Seb's
tape is not the strategic target** (his own median bank halved when the town rebalance landed, and
he has since withdrawn from the ladder), and **wheat, not melon or strawberry, is the scarcest thing
on the board** — the field plants 108-147 WHEAT tiles a season; our schedule plants 24.

**Read `the_ladder_is_two_scripts.md` and `what_the_town_will_actually_eat.md` first.** They are the
current position on strategy and market economics and supersede the *framing* — not the mechanism
findings — of everything below built around matching Seb's tape.

| File | What it is |
|---|---|
| `the_ladder_is_two_scripts.md` | **Current position on strategy.** 2,744 ladder seats: the field is two shared scripts plus one reactive #1 (THUNDER THUNDER, adaptive cow/sheep, worth ~110 rating points over a fixed script). Plants 108-147 WHEAT against our 24. Names Dmitry Belan or Efe Can Celiksoy as the rebase target, not Seb. |
| `what_the_town_will_actually_eat.md` | **Current position on market economics.** 87 tapes' closing inventory against `town.unlocked_shops`, not simulation: wheat's book never saturates (closing surplus always negative, $40-59 against a $25 base); melon and fertilizer are always oversupplied (closing surplus always positive) — every player over-plants melon, ourselves included, which makes it a shared inefficiency rather than a losing move. |

## What today's finding changes in the docs below

- **The "matching-the-tape" line of work is not wrong, its target is.** `the_ladder_is_two_scripts.md`
  says this explicitly: *"It is not the planner, the watering or the market logic; it is the target."*
  Every planner bug found and fixed in `fable_matching_the_tape_2026-08-10.md`,
  `how_sebs_planner_works_2026-08-10.md`, `how_seb_feeds_the_herd.md`, `the_day_is_a_cash_ledger.md`,
  `the_market_cadence_over_all_products_2026-08-10.md`, `plan_once_and_the_dawn_blind_spots_2026-08-09.md`,
  `handoff_plan_once_2026-08-09.md`, `router_tape_repoint_2026-08-09.md` and
  `the_tape_column_does_not_replay_his_game_2026-08-09.md` is still real. Each is banded at the top:
  the tape they match against (Seb's) is a known-suboptimal reference now, not a stand-in for "the
  top of the ladder."
- **`what_the_leaders_actually_grow_2026-08-09.md`'s central conclusion is contradicted** — it said
  "we do not need a new day-0-10 tape" and "our schedule already matches Seb's build on the levers
  that matter most." Banded SUPERSEDED.
- **`the_top_five_clusters_2026-08-09.md`'s field description (15 replays, 3 per team) is superseded
  in scale** by the 2,744-seat sample. Its `counter_meta` (Seb, rank #1 at 3,201.1 in that sample) is
  the same player whose bank has since halved. Banded.
- **`SHOP_ADAPT_CROPS` (`kagg/search/schedule_agent.py`) is OFF.** Three pairs were tried —
  `WHEAT<->CARROT`, `TOMATO<->STRAWBERRY`, `STRAWBERRY<->MELON` — and all three failed for reasons
  recorded in the flag's own docstring; read it before proposing a fourth. `REGISTER.md` C-23.
- **Fertilizer is now priced off the live market quote, not its $100 base, when deciding whether to
  fertilize a tile.** Shipped, unconditional. `REGISTER.md` C-24.
- **Two claims were raised and retracted on 2026-08-11 before ever landing in a doc file** (checked:
  neither phrase appears anywhere in `docs/`, recorded here so a future session does not rediscover
  them): **"melon should be 7 tiles"** — the headroom model that produced it treats the town's drain
  as a cliff when the price curve is a slope, so it under-prices every steep-curve, low-drain product;
  see `the_ladder_is_two_scripts.md`'s "what was tried on the crop dynamic" section. **"Dripping sales
  is worth +77% on milk"** — wrong on the premise; the shipped agent already drips sales.

Consolidated 2026-08-09, on top of the 2026-08-08 consolidation below.
The trigger this time: the ladder moved to `kaggle-environments` 1.32.6 on 2026-08-07/08, which made
a large fraction of this project's dollar figures wrong by up to 4.67x (melon), and the marketplace
became the dominant open topic with six overlapping same-week write-ups nobody had merged.
**Wrong docs are worse than no docs.** The bar for keeping a file: does it describe a mechanism that
still exists, and does every number in it say which env version produced it?

## Read in this order

| File | What it is |
|---|---|
| `competition_brief.md` | The competition, the scoring rule, the **1.32.2 vs 1.32.6 version skew**, and the env rules that have each cost a day. Ground truth is `reference/kaggriculture.py`. |
| `architecture.md` | **What the agent actually is today**, the flags that ship off with the numbers that turned them off, and the harness caveats. Restamped 2026-08-09: both simulators fail parity on 1.32.6. |
| `REGISTER.md` | **The live open/closed list.** Check it before opening anything — items here reopen under new names. Restamped 2026-08-09 with a version caveat on its STATE block. |
| `the_market_2026-08-09.md` | **The marketplace — mechanism, current shipped status, and the open prescription.** New. Merges six 2026-08-08/09 write-ups; see "What was merged" below. This is the main open topic right now. |
| `the_top_five_clusters_2026-08-09.md` | **SUPERSEDED IN SCALE 2026-08-11** — the field, from an outside notebook, 15 replays. Superseded by `the_ladder_is_two_scripts.md` (2,744 seats). Read before believing any older "we are close" framing. |
| `what_the_leaders_actually_grow_2026-08-09.md` | **SUPERSEDED 2026-08-11** — its conclusion ("we already match Seb's build, no new tape needed") is contradicted: the field plants 108-147 WHEAT, we plant 24. Also documents that 18 of 20 downloaded "leader" episodes are one public script mirroring itself, which still holds. |
| `what_saturates_and_what_does_not_2026-08-09.md` | Corrected per-product and per-head saturation points on 1.32.6, replacing the stage-1 `DRAIN_UNITS` model. Retracts and corrects its own goose-scaling claim same-day. |
| `fable_the_discard_problem_2026-08-09.md` | The shed-eviction mechanism, tested rather than assumed: a real day-gating bug fixed, the broader "release the reserve" fix measured mixed (not a win), the router's "unreachable room" claim partially confirmed. |
| `fable_market_shape_2026-08-09.md` | Seb vs us on FILLS, not offers: the price gap is real but is a product-mix story, not an order-shape one. `LATE_SELL_BIAS` (no selling before hour 16) nearly doubles pool win rate (14.6% -> 27.1%) in an 8-seed A/B — the strongest single result of the day, not yet shipped pending a wider seed sweep. `CAP_SELL_OFFER_SIZE` is a verified-live but under-tested null. Also resolves the 94.4%-vs-14.6% pool comparison as not apples-to-apples. |
| `geometry_of_the_herd_2026-08-09.md` | Pen-placement geometry, measured on two fresh episodes: not a lever. Confirms `REGISTER.md` C-21 independently. |
| `economics_q5_findings.md` | The measured economics: yields, allocation, storage. Restamped 2026-08-09 — §2 (town drain) and the market-ceiling table in §4 are 1.32.2 and superseded by `the_market_2026-08-09.md` §2. |
| `experiment_log.md` | Every experiment, its score, and what it taught. Restamped with a version caveat — entries before 2026-08-07/08 are 1.32.2 scores. |
| `the_field.md` | What the opponents actually do, measured from 1.32.2-era replay JSON. Restamped: the structural claim (winners are open-loop) still holds; the dollar figures don't. |
| `fable_stage1_review_2026-08-09.md` | Why the offline schedule-search stack (`chains.py`, `scheduler.py`) is not the highest-value next move, and what is. |
| `what_kind_of_problem_this_is.md` | The problem class, and which family of tools each clause rules out. |
| `rl_feasibility.md` | The RL track: what it measured, and why it is parked. |
| `lessons_carried_over.md` | Orbit Wars post-mortem, distilled. Not version-dependent. |
| `throughput_measurements.md` | Measured env throughput on the training box. Not version-dependent. |

## Added since the table above was written (2026-08-09 and -10), not previously indexed

The table above stopped at 2026-08-09. These landed after and were never folded in. Grouped by
whether today's finding bands them.

**Banded 2026-08-11 (TARGET SUPERSEDED — mechanism findings stand, the tape they match is stale):**

| File | What it is |
|---|---|
| `router_tape_repoint_2026-08-09.md` | Repointed the router's tape fixture from `seb` (1.32.2) to `seb1326` (1.32.6) and re-derived every asserted day. |
| `the_tape_column_does_not_replay_his_game_2026-08-09.md` | Proved the harness diverges from Seb's own recorded bank by turn 32 on a one-dollar 1.32.2-vs-1.32.6 charge — a real fidelity bug, still open. |
| `plan_once_and_the_dawn_blind_spots_2026-08-09.md` | Four blind spots in planning the day once, at dawn, against Seb's tape. |
| `handoff_plan_once_2026-08-09.md` | Session handoff: the day is now planned once; d0/d1 exact against Seb's tape. |
| `how_sebs_planner_works_2026-08-10.md` | Route-level reconstruction of Seb's opening from four tapes: open-loop through day 3, reactive from day 4. |
| `how_seb_feeds_the_herd.md` | Seb's day-4 feed routing, read off tape `91422988`. |
| `the_day_is_a_cash_ledger.md` | Fixed a `short_of_cash` bug that conflated an already-funded purchase with a real shortfall, diagnosed against Seb's day-4 bill. |
| `the_market_cadence_over_all_products_2026-08-10.md` | Our fills run 4-8 hours earlier than Seb's, on every product, same direction every time. |
| `fable_matching_the_tape_2026-08-10.md` | d4 sell shortfall and d9/d10 `place 0/4`, measured against tape `seb2988`. |

**Not banded — mechanism-only, not target-dependent, no economy-sensitive numbers:**

| File | What it is |
|---|---|
| `the_book_is_shallow_2026-08-09.md` | Corrects its own same-day mistake: weed spawning is agent-dependent (shifts the RNG stream), so absorption cannot be measured PASS-vs-PASS. Price-curve math and the melon-has-no-shop finding survive. |
| `parity_restored_on_1326_2026-08-09.md` | Both simulators made exact against 1.32.6 again — four behavioural rule changes fixed (locked-tile movement, DROP/PICKUP/PLACE ordering, shed-capacity caps on BUY, shop unlock with replacement). |
| `arena_state_leak_2026-08-09.md` | `run_arena` was driving one agent object through every match, corrupting closures across seasons. Fixed; `gate_pool.py` and `arena_gate.py` were never affected. |
| `fable_the_wheat_churn_2026-08-09.md` | The wheat "churn" is a buy-side day-budget defect: we buy 1,099 units against the field's 266-392. Measured on 66 of our own 1.32.6 (`townCenterSellInterval=24`) replays — already the current economy, not banded. |

`CLAUDE.md` at the repo root holds the rules, the kill criteria, and the "lessons learned the hard
way" list. It is not superseded by anything here.

## Moved out of CLAUDE.md (2026-08-15)

- `kill_criteria_and_settled_positions.md` — the full kill criteria and the settled RL positions,
  with the measurements behind each. Every one is MET or CLOSED, so `CLAUDE.md` now carries only the
  three sentences that still bind. **Do not delete this file:** the reward-shape bullets exist to
  stop a future session restoring per-step rewards from `rl_feasibility.md`, which still argues for
  them at length.
- `fable_watering_post_d8_2026-08-15.md` — watering post-d8 closed as a measured negative. The
  preventive-watering fix cost $1,051 and killed one more tile by displacing a rescue.
- `fable_production_decay_d19_2026-08-15.md` — why standing crop decays from d19. Digs, fertilize
  and cap-discards all ruled out; the mechanism is thirst-killed strawberries (13 of ours complete
  their lifecycle against his 31) and one-shots rotting past their window.

## The rules that survived the cull, in one place

- **Check the env version before trusting a number.** `kaggle-environments` moved 1.32.2 -> 1.32.6
  on 2026-08-07/08: town centre drain halved, melon absorption fell 140 -> 30, and the
  `BUY_PRODUCT`-bypasses-`shedCapacity` loophole closed (commit `a810dc8`). Both simulators
  currently fail parity on 1.32.6 (8 failures).
- **The ladder is Elo and starts at 600.** Winning matters, margin does not. Select on win rate.
- **We are not close to the field.** Best submission 1,123.5 against a field floor around 3,117 and
  a median of 3,067.75 (2026-08-08 episode index). Treat any older "the gap is a few percent"
  framing as answering a different, smaller question.
- **Never evaluate against `starter` alone, the arena pool, or the handover fixture as the whole
  story** — the arena pool is saturated at 94.4% and cannot discriminate a selling change; the
  handover fixture's opponent barely sells. `scripts/vs_tapes.py` against `oldleader` is the
  instrument that currently discriminates.
- **A mirror match is not a best response.** An Elo ladder rewards beating a *field*.
- **Seed variance is ~15%.** Quote the range, use held-out seeds, and confirm a search winner on a
  fresh draw or the winner's curse makes it wander.
- **Judge a fix at the day it targets, field by field.** Season totals are a weak signal, and
  `breakdown.py --diff`'s `money` row is an *area*, not a deficit.
- **A gate only tests what it exercises.** Ask what a passing test could not reach.
- **After fixing, revert the fix and confirm the test goes red.**
- **Before believing a measurement about a mechanic, ask what the code could not express.**
  "Animals do not pay" was an artifact of our own code four separate times.
- **Prefer a replay to an aggregate whenever the aggregate could be a tie.**
- **The town centre's cadence halved again on 2026-08-08** (`townCenterSellInterval` 12 -> 24, inside
  the 1.32.6 move) and Seb's own median bank halved with it ($137,747 -> $77,737); he has since
  withdrawn from the ladder. His tape is still useful as a bug-finding harness, not as the target —
  see `docs/the_ladder_is_two_scripts.md`.
- **We plant a fifth of the wheat the field does.** 24 tiles against the field's 108-147, measured
  from 2,744 ladder seats. This is the largest single measured gap to the field right now, larger
  than anything the market or planner work has targeted this week.
- **Match a technique's sample size before trusting it over a bigger one.** The 20-episode and
  15-replay field descriptions from 2026-08-09 read the field roughly right in shape but wrong on the
  one number that mattered (our wheat volume); the 2,744-seat sample is what should be quoted now.

## What was deleted today (2026-08-09), and why

Seven files, all folded into `the_market_2026-08-09.md` or dropped as superseded. No measurement
named in any of them is lost — every real number quoted below is now in the merged doc.

| deleted | why |
|---|---|
| `fable_market_technique_2026-08-08.md` | The core derivation (the `N(L)`/reservation-price rule, absorption tables, depth tables, handover-fixture measurement). Folded into `the_market_2026-08-09.md` §1-2, §4. |
| `fable_market_selling_2026-08-08.md` | The `PRICE_AWARE_SELL_CAP` measurement history (arena runs, the dump-shape trap). Folded into §4. Its "ships OFF" status line is now wrong — the flag is `True` in the current tree, corrected in the merged doc. |
| `the_shed_destroys_the_harvest_2026-08-08.md` | The shed-discard mechanism (331 units destroyed, why `allow` collapses to the schedule row) and the handover-fixture before/after. Folded into §3-4. |
| `the_planner_prices_the_wrong_market_2026-08-08.md` | The 1.32.2-vs-1.32.6 `DRAIN_UNITS` overstatement table. Folded into §2; the per-head saturation half of it is superseded by `what_saturates_and_what_does_not_2026-08-09.md`, which corrects a bug (`events * max_held` overstated every herd 4-6x) this doc's table inherited. |
| `brief_market_selling_2026-08-08.md` | A task brief to an agent, not a finding. Its content is fully answered inside the write-ups it commissioned, all now merged. |
| `we_oversell_into_a_contested_book_2026-08-09.md` | The current best actionable finding — 12/14 real losses reversible by selling wool/milk/strawberry at 0.5-0.7x, the opponent-net-trade inference formula, the `vs_tapes.py` partial result. This is now `the_market_2026-08-09.md` §5, verbatim on every number. |
| `fable_plan_2026-08-09.md` | A phased roadmap whose central premise — "the opening is solved, the gap is a 5-10% money-at-equal-board fix" — is contradicted by `the_top_five_clusters_2026-08-09.md`, discovered the same day: we are roughly a third of the way up the field, not a few percent behind it. Its still-valid, non-duplicated action items (shed eviction by value density, fertilizer front-loading, gate every change on `vs_tapes.py`) are folded into `the_market_2026-08-09.md` §7. |

### Withdrawn claims that must not resurface as fact

Two claims were raised and retracted within the same session on 2026-08-09, before ever landing in
a doc file (checked: neither phrase appears anywhere in `docs/`, so nothing needed deleting here —
recorded so a future session does not rediscover and re-write them):

- **A "wheat churn loop"** (buy ~1,971 wheat, sell ~1,344 back). Wrong: it summed *offered*
  quantities from the action stream, and the agent re-offers the same day's quota on every one of 24
  turns, so a quota of 8 counted as up to 192. `docs/fable_the_discard_problem_2026-08-09.md` §0
  records the retraction.
- **A "plant execution gap"** (we execute 47% of scheduled plants). Wrong: it compared `PLANT` op
  counts against schedule plant-entry counts, different units. Seb's schedule plants 82 tiles and we
  plant ~81 — we match.

## What the 2026-08-08 consolidation deleted (kept for reference)

Consolidated 2026-08-08 from **87 markdown files / 17,774 lines down to 11 files / ~2,670 lines**.
Most of what was there was session narration, superseded diagnosis, or an advisor write-up whose
recommendation was measured and rejected.

### Session diaries and handoffs — 6 files, ~3,900 lines

`HANDOFF.md`, `HANDOFF_NEXT.md`, `HANDOFF_2026-08-02.md`, `HANDOFF_2026-08-02-evening.md`,
`HANDOFF_2026-08-03.md`, `HANDOFF_2026-08-03-evening.md`.

Each explicitly superseded the one before, and all six described the RL training track — the running
config, which checkpoint was live, which systemd unit to tail. `REGISTER.md` is the successor for
state; the measurements worth keeping are in `rl_feasibility.md` and `experiment_log.md`.

### Docs built on mechanisms that no longer exist — 9 files

The deliver ferry, `DELIVER_REPLAN_DAYS`, the end-of-tour return leg, the `draw` side-channel, and
`router.plan_routes` as the day planner have all been replaced by `kagg/search/cover.py`, a covering
planner with no price table, in which **shed trips are real stops inserted by `materialise`**.
Anything whose *recommendation* was a change to one of those is obsolete even where its diagnosis
was sound.

`fable_delivery_node_2026-08-07.md`, `fable_return_leg_2026-08-07.md`,
`fable_sell_row_delivery_2026-08-07.md`, `fable_stranded_carrier_2026-08-07.md`,
`idle_at_h10_2026-08-07.md`, `service_undercount_2026-08-07.md`,
`drop_timing_four_attempts_all_negative_2026-08-07.md`,
`fable_did_we_break_d0_d8_2026-08-07.md`, `melon_reality_check_2026-08-07.md`.

Preserved: the four negative drop-timing arms and the informative fourth one
(`experiment_log.md` §20); the `Node.service` under-count and why repaying it is *not* a fix
(§22, C-22); the day-10 idle being surplus at plan time (OPEN-6); the melon findings (C-1 to C-4).

### Conclusions later reversed — deleted rather than presented alongside the correction

- `economics_analysis.md` — its revenue-per-tile table read a lifetime yield as a daily rate and
  overstated tomato by 15x and strawberry by 10x. The correction is `economics_q5_findings.md` §1.
- `harvest_ordering_2026-08-08.md` — its own conclusion superseded the seven delivery arms; folded
  into `experiment_log.md` §19 and C-19.
- `the_reward_is_a_step_function_2026-08-03.md`, `money_scaled_reward_2026-08-03.md`,
  `graded_idle_ladder_2026-08-03.md`, `thrift_is_optimal_2026-08-03.md` (superseded within the same
  hour by its own correction), `cliff_decomposed_2026-08-03.md`, `bankrupt_every_game_2026-08-03.md`,
  `entropy_diffusion_2026-08-04.md`, `lr_probe_2026-08-03.md`, `model_size_2026-08-03.md`,
  `seat_sum_fights_the_discount_2026-08-03.md`, `trainee_is_always_seat_0_2026-08-03.md`,
  `p2b_state_source_2026-08-03.md`, `critic_terminal_blindness_2026-08-03.md`,
  `rl_experiment_matrix.md`, `market_finetune_design_2026-08-04.md`, `ideas.md` — the RL track's
  diagnosis chain. The cause turned out to be temporal (`commit.py`) and the track is parked;
  everything durable is condensed in `rl_feasibility.md`.

### Advisor write-ups — 20 files

Kept only where the *measurement* survived; the recommendation in most cases was measured and
rejected, and one line recording that is worth more than the argument.

| deleted | verdict, preserved |
|---|---|
| `fable_delivery_node_2026-08-07.md` | delivery node withdrawn on measurement; a mandatory node re-permutes every yielding tour, an honestly-priced one always inserts last. C-22. |
| `fable_depot_sheep_2026-08-07.md` | pen intent measured **59 cells against 52**, three mechanisms landing identically. `experiment_log.md` §21. |
| `fable_d5_buy_product_2026-08-07.md` | the day-5 fifth wheat unit is `fed_today` not being subtracted from the herd floor. Fix landed. |
| `fable_d12_unfed_2026-08-08.md`, `brief_d12_unfed_sheep_2026-08-08.md` | `node.pick.pop` was unconditional, so a dry shed discarded a critical draw outright. Fix landed; the retry half ships OFF (`STAND_AT_A_DRY_SHED`), `architecture.md`. |
| `fable_cover_planner_confer_2026-08-08.md` | the `HIRE`-then-`BUY_ANIMAL` phantom purchase — now **OPEN-8**; and the reason matched-day superiority does not translate to season money, now the `matched_days.py` caveat in `architecture.md`. |
| `fable_herd_cap_and_retraction_2026-08-04.md` | a raw agent transcript, never converted to a document. |
| `fable_review_*` (6 files), `fable_advice_recovered_2026-08-03.md`, `opus_review_2026-08-03.md`, `review_of_the_reframe_2026-08-04.md` | RL-era reviews of a parked track. |
| `fable_bellman_route_and_crop_spec_2026-08-04.md`, `fable_how_to_build_a_competitor_2026-08-04.md`, `fable_chain_genome_review_2026-08-04.md`, `fable_land_and_crop_review_2026-08-05.md`, `fable_small_errors_review_2026-08-05.md`, `fable_wrong_assumptions_2026-08-05.md`, `fable_emitter_task_generation_2026-08-05.md`, `fable_day0_turn_budget_2026-08-05.md`, `fable_fertilizer_and_wheat_yield.md` | chain-search-era reviews. The stack is parked; the method findings are in `what_kind_of_problem_this_is.md`. |
| `kimi_prompt_trajectory_optimisation.md`, `kimi_take_chain_optimisation_2026-08-04.md`, `market_game_framing_kimi_2026-08-05.md` | "this is a market game" was answered by measurement: market timing, front-running and withholding are ~3% of money and **0% of wins**. `economics_q5_findings.md` §6 (1.32.2). |

### Duplicated findings — 14 files folded into the survivors

`the_winners_are_open_loop_2026-08-04.md`, `episode_teardown_2026-08-03.md`,
`new_leader_somewhere_after_2026-08-05.md`, `how_the_leader_actually_funds_it_2026-08-05.md`,
`public_meta_2026-08-03.md`, `leaderboard_snapshot_2026-08-03.md`, `ladder_analysis.md`
-> **`the_field.md`**.

`tutorial_how_this_game_is_actually_optimised.md`, `three_layers_2026-08-06.md`,
`executor_livestock_broken_2026-08-04.md`, `emitter_ab_state_2026-08-05.md`,
`handoff_fidelity_2026-08-07.md` -> **`experiment_log.md` Part 2** and **`architecture.md`**.

`env_1326_town_rebalance_2026-08-07.md`, `ruled_out_melon_harvest_gate_2026-08-06.md`,
`pens_on_the_depot_ring_2026-08-08.md` -> **`competition_brief.md`**, "engine rules that have each
cost a day" and "version skew".

`breakdown_fills_not_offers_2026-08-08.md`, `bugs_found_2026-08-03-late.md`,
`geometry_placement_2026-08-08.md`, `reactive_selling_and_the_seb_gap_2026-08-07.md`,
`wheat_d8_2026-08-08.md` -> **`experiment_log.md` Part 3** and **`REGISTER.md`** CLOSED.

`docs/superpowers/specs/2026-07-31-kaggriculture-agent-design.md` -> **`architecture.md`**. The
original spec described an RL pipeline that is not what ships and recorded the inference budget as
12 banked seconds when the source says 60. `CLAUDE.md`'s "read these first" item 5 now points at
`architecture.md`.

`docs/fable_drop_timing_attempt.patch` — a patch that measures a loss and is not applied; the
finding is `experiment_log.md` §20.

## Where a deleted doc's content went

Some docstrings in `kagg/`, `scripts/`, `tests/` and `submission/` still cite deleted filenames.
Code was not edited as part of either consolidation. Use this table.

| cited path | now in |
|---|---|
| `docs/HANDOFF.md` | `REGISTER.md` (state), `rl_feasibility.md` (RL measurements) |
| `docs/episode_teardown_2026-08-03.md` | `the_field.md`, "the mixed economy, torn down" |
| `docs/the_winners_are_open_loop_2026-08-04.md` | `the_field.md`, "the winners submit fixed 720-turn scripts" |
| `docs/new_leader_somewhere_after_2026-08-05.md` | `the_field.md`, "the leader `somewhere after`" |
| `docs/public_meta_2026-08-03.md` | `the_field.md`, "the public meta" |
| `docs/tutorial_how_this_game_is_actually_optimised.md` | `experiment_log.md` §16, `what_kind_of_problem_this_is.md` |
| `docs/executor_livestock_broken_2026-08-04.md` | `experiment_log.md` §16 (the leaders' plan through our executor banks $0) |
| `docs/market_game_framing_kimi_2026-08-05.md` | `economics_q5_findings.md` §6 |
| `docs/idle_at_h10_2026-08-07.md` | `REGISTER.md` OPEN-6 |
| `docs/service_undercount_2026-08-07.md` | `experiment_log.md` §22, `REGISTER.md` C-22 |
| `docs/geometry_placement_2026-08-08.md` | `experiment_log.md` §21, `REGISTER.md` C-21 |
| `docs/fable_delivery_node_2026-08-07.md` | `REGISTER.md` C-22, `architecture.md` |
| `docs/fable_depot_sheep_2026-08-07.md` | `experiment_log.md` §21 |
| `docs/brief_d12_unfed_sheep_2026-08-08.md` | `architecture.md`, `STAND_AT_A_DRY_SHED` |
| `docs/fable_emitter_task_generation_2026-08-05.md` | `architecture.md`, "why closed-loop" |
| `docs/fable_herd_cap_and_retraction_2026-08-04.md` | `what_kind_of_problem_this_is.md`, the beam's structural weakness |
| `docs/critic_terminal_blindness_2026-08-03.md` | `rl_feasibility.md` |
| `docs/entropy_diffusion_2026-08-04.md` | `rl_feasibility.md` |
| `docs/bankrupt_every_game_2026-08-03.md` | `rl_feasibility.md` |
| `docs/the_reward_is_a_step_function_2026-08-03.md` | `rl_feasibility.md`, "the ruling on reward" |
| `docs/opus_review_2026-08-03.md` | `rl_feasibility.md` |
| `docs/seat_sum_fights_the_discount_2026-08-03.md` | `rl_feasibility.md` |
| `docs/fable_review_day0_launch_2026-08-03.md` | `rl_feasibility.md` |
| `docs/fable_review_animals_2026-08-03_evening.md` | `rl_feasibility.md`, `the_field.md` |
| `docs/fable_review_macro_action_plan_2026-08-04.md` | `rl_feasibility.md` |
| `docs/fable_bellman_route_and_crop_spec_2026-08-04.md` | `what_kind_of_problem_this_is.md` |
| `docs/economics_analysis.md` | `economics_q5_findings.md` (its table was wrong) |
| `docs/ideas.md` | `rl_feasibility.md`, "the ruling on reward" (money/net-worth potential) |
| `docs/rl_postmortem_and_fix_plan.md` | never existed here — it is in the `orbit_wars_jax` repo |
| `docs/superpowers/specs/2026-07-31-...-agent-design.md` | `architecture.md` |
| `docs/fable_market_technique_2026-08-08.md` | `the_market_2026-08-09.md` §1-2, §4 |
| `docs/fable_market_selling_2026-08-08.md` | `the_market_2026-08-09.md` §4 |
| `docs/the_shed_destroys_the_harvest_2026-08-08.md` | `the_market_2026-08-09.md` §3-4 |
| `docs/the_planner_prices_the_wrong_market_2026-08-08.md` | `the_market_2026-08-09.md` §2, `what_saturates_and_what_does_not_2026-08-09.md` |
| `docs/brief_market_selling_2026-08-08.md` | `the_market_2026-08-09.md` (its questions are answered throughout) |
| `docs/we_oversell_into_a_contested_book_2026-08-09.md` | `the_market_2026-08-09.md` §5 |
| `docs/fable_plan_2026-08-09.md` | `the_market_2026-08-09.md` §7, `the_top_five_clusters_2026-08-09.md` (corrected gap size) |
