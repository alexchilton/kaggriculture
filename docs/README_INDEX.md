# docs/ — full index, 2026-08-25

`docs/README.md` already exists and is itself an index (last restamped 2026-08-15), so this is a
**second, new file** rather than a rewrite of it.
Read `README.md` first for the project's own account of what was consolidated and why.
This file exists because 21 files landed after 2026-08-15 and were never folded into that account,
and because nobody had grouped all files by topic in one place.

**Note on the count:** the task this file was built for counted 96 markdown files in `docs/`.
`the_shed_is_the_bottleneck_2026-08-25.md` was committed mid-session (12:44, 2026-08-25) after that
count was taken, bringing the true total to 97 pre-existing files.
It is folded in below, under "The market and pricing."

Every description below was written after opening the file and reading its opening paragraph and
verdict line — not guessed from the filename.
Dates are the file's own dated content where the filename carries no date.

**Companion file:** `docs/what_is_still_true_2026-08-25.md` — a short digest of which findings below
are still live, which are superseded, and which are contradicted and unresolved.

**Do not delete anything named here without asking.** See "Candidates for removal" in the task
report this file was built alongside (not duplicated here — ask the session that built this index).

---

## Group counts

| Group | Files |
|---|---|
| Core reference | 7 |
| The market and pricing | 15 |
| The tape and replay | 10 |
| The solver and routing | 23 |
| The late season and endgame | 9 |
| Animals and the herd | 4 |
| Carrot and late-crop experiments | 7 |
| Ladder game post-mortems | 12 |
| RL and imitation (parked) | 2 |
| Process and measurement lessons | 6 |
| Infrastructure and throughput | 2 |
| **Total** | **97** |

---

## Core reference

Read these before anything else. `README.md`'s own "read first" table covers the same ground in
more detail.

| File | Date | What it says |
|---|---|---|
| `README.md` | restamped 2026-08-15 | The project's own index and consolidation history: what was merged, what was deleted and why, and the rules that survived each cull. |
| `REGISTER.md` | "last updated" 2026-08-15 | The live open/closed list — every OPEN item and every CLOSED item with the artifact that would go red if it reopened. Three version caveats stacked at the top (1.32.6, then the Seb-target correction, then the SELLABLE fix). |
| `architecture.md` | 2026-08-08, addenda to 2026-08-11 | What the shipped agent actually is: closed-loop reader of `obs` through `schedule_agent.py` and `router.py`/`cover.py`, why the emitter approach was replaced (48% landing vs ~100%), why the priced routing search was replaced by the covering planner (`cover.py`, `-$34,816` over 12 seasons), and the flags that ship OFF. Its own emitter and parity numbers are marked stale by a 2026-08-09 caveat. |
| `competition_brief.md` | living doc, latest addendum 2026-08-15 | The competition itself: $50k prize, deadline 2026-09-30, 720-turn two-player game, Elo scoring starting at 600, required `kaggle-environments >= 1.32.7`, and the catalogue of engine rules that have each cost a day. Its 1.32.2 baseline section is marked SUPERSEDED in-file. |
| `kill_criteria_and_settled_positions.md` | moved out of `CLAUDE.md` 2026-08-15 | The full evidence behind the kill criteria and settled RL positions that `CLAUDE.md` now states in three sentences: terminal reward only, RL parked, fast-sim parity passes 300/300. Every criterion is MET or CLOSED. |
| `what_kind_of_problem_this_is.md` | 2026-08-05, status note 2026-08-08 | Frames kaggriculture as "a deterministic, open-loop, multi-dimensional knapsack with a time-phased budget, played as a best response against a fixed field," and why that rules out RL. States its own offline chain-search stack is now parked in favour of the closed-loop schedule agent. |
| `economics_q5_findings.md` | undated, version caveats 2026-08-09/-11 | Master measured-economics doc: yields, town drain, supply, allocation, storage. Its §2 and market-ceiling table are marked superseded twice in-file (first by `the_market_2026-08-09.md`, then again by `what_the_town_will_actually_eat.md`). |

## The market and pricing

| File | Date | What it says |
|---|---|---|
| `the_market_2026-08-09.md` | 2026-08-09, addenda to 2026-08-11 | Consolidates six deleted write-ups into the derived selling rule `N(L)=max(0, I_L−I_now)+D_rem`. Re-pricing our own sales downward turns 12 of 14 real ladder losses into wins. Both `PRICE_AWARE_SELL_CAP` and `RESERVATION_SELL_CAP` ship ON. |
| `the_book_is_shallow_2026-08-09.md` | 2026-08-09 | Same-day self-correction: the "delivery problem" framing (443 units stranded) was two stacked measurement errors. The real finding is realized price per unit varies 9x by seed (milk $252.66 vs $27.90/unit) with the identical agent and schedule. |
| `the_market_cadence_over_all_products_2026-08-10.md` | 2026-08-10 | Our buy/sell hours are systematically wrong versus Seb's (dawn dumps, morning sells before the town drains, front-loaded buys). Target marked SUPERSEDED, the cadence-mismatch finding itself still holds and the obvious fix (`SELL_AFTER_HOUR`) is unrun. |
| `fable_market_shape_2026-08-09.md` | 2026-08-09 | `LATE_SELL_BIAS` (no selling before hour 16) nearly doubles pool win rate, 14.6% → 27.1%, in an 8-seed A/B. `CAP_SELL_OFFER_SIZE` is a genuine but underpowered null. Its §4/§4.1/§5 pool numbers were later found contaminated by a shared-agent-object bug — see `arena_state_leak_2026-08-09.md`. |
| `fable_the_wheat_churn_2026-08-09.md` | 2026-08-09 | Wheat over-buying is a buy-side day-budget defect, not a sell-side one. `FEED_BUY_CEILING_DAYS = 2` cuts purchases 56% (1,800 → 797/season) with zero herd starvation. Shipped. |
| `what_the_town_will_actually_eat.md` | undated, built on 2026-08-11 data | From 87 recorded ladder tapes' closing inventory: melon and fertilizer always end in surplus (over-supplied by every player, ourselves included), wheat always ends in deficit ($40-59 above a $25 base). Current position on market economics per `README.md`. |
| `market_depth_and_the_morning_losses_2026-08-13.md` | 2026-08-13 | Two near-mirror losses came from shipping volume into products the town does not drain (melon, milk, strawberry) while under-shipping wool and carrot, which stayed above base all season. Self-corrects an earlier plant-count table same day. |
| `the_market_is_the_late_season_2026-08-13.md` | 2026-08-13 | Same-day self-correction: the "milk floor" reading in `breakdown.py` is a harness artifact (the tape reseats into a book it also sold into). The real gap is COW 10/SHEEP 4 flooding the milk book at $1-$5/unit vs $223 realized elsewhere. Withdraws the geese-kill evidence it had cited. |
| `balance_change_eggs_tomatoes_carrots_2026-08-15.md` | 2026-08-15 | Quotes the organisers' 1.32.7 price-change announcement (carrot/tomato/egg viable-but-not-universal via a "hinge" curve) and notes it lands directly on the sorest spot: these three products could not be sold at all until 2026-08-13, so the goose-deletion verdict was made under a bug. |
| `market_curves_and_the_q4_branch_2026-08-15.md` | 2026-08-15 | Every product's price curve computed from the reference source: WHEAT can only be halved, not crashed; TOMATO/CARROT follow a quadratic hinge curve; EGG is the only animal product that cannot be crashed. States plainly: "single-seed deltas are worthless." |
| `fable_allocation_economics_2026-08-15.md` | 2026-08-15 | Post-hinge (1.32.7) allocation analysis: unconditional wheat→carrot/tomato conversion has no edge; a conditional play gated on the d12-visible shop draw is worth ~$900/game mean in the ~26% of games where the hinge fires. Corrects `when_and_what_to_sell_2026-08-15.md` §3's headline figure from +$12,136 to +$5,653. |
| `when_and_what_to_sell_2026-08-15.md` | 2026-08-15 | A model, not a measured result (states this explicitly): sell timing/spreading worth ~$12k in the shipped plan, and the melon-swap rule may have its logic backwards. Superseded on its headline number by `fable_allocation_economics_2026-08-15.md`. |
| `marginal_units_and_the_shared_book_2026-08-16.md` | 2026-08-16 | Long, self-correcting doc (17 sections): revenue is the wrong objective, the book is shared so opponent volume dominates outcomes, and multiple prior goose/herd verdicts were artifacts of measuring "IN A MIRROR." Revises its own herd counts and shop-draw model mid-document. |
| `fable_where_the_money_is_2026-08-24.md` | 2026-08-24 | Losses trace to selling cadence past a season's supply budget (milk hits the $1 floor at ~76 units surplus by d13), not execution. Proposes a combined drain-budget cadence and deficit-gated terminal-dump experiment. |
| `the_shed_is_the_bottleneck_2026-08-25.md` | 2026-08-25 (committed mid-session, not in the original 96-file count) | Across 35 downloaded ladder games, our shed sits at/near its 100-unit cap five times as often as opponents' (2,505 turns at >=90 vs 488). On the strawberry solver arm, d12-d23: ten more harvests, 177 fewer units sold, -$11,073. Explicitly rules out routing and walk-to-shed as causes; names sell cadence as the likely fix and links directly to the wool-collapse finding in `where_99114898_went_2026-08-25.md`. |

## The tape and replay

| File | Date | What it says |
|---|---|---|
| `how_sebs_planner_works_2026-08-10.md` | 2026-08-10 | Reconstructs Seb's planner from four tapes: open-loop and identical for 96 turns until the first shop unlock, then one fixed role and tile block per hand. Target marked SUPERSEDED — Seb's tape was optimal only under the old economy. |
| `how_seb_feeds_the_herd.md` | undated (tape 91422988) | Seb's day-4 feed routing: loads wheat once at dawn, splits across two carriers, uses a third hand for itemless CARE/COLLECT. Target marked SUPERSEDED for the same reason. |
| `router_tape_repoint_2026-08-09.md` | 2026-08-09 | Repointed the router's tape fixture from `seb` (1.32.2) to `seb1326` (1.32.6) and re-derived every asserted day; 5 tests still fail on real, re-measured gaps. Target marked SUPERSEDED. |
| `the_tape_column_does_not_replay_his_game_2026-08-09.md` | 2026-08-09 | Replaying Seb's own recorded actions through a fresh 1.32.6 env diverges from his real bank starting turn 32 — a one-dollar wheat-pricing difference that compounds to 9% of his real bank by the end. A real, still-open fidelity bug. |
| `fable_matching_the_tape_2026-08-10.md` | 2026-08-10 | Traces a d4 sell shortfall to `DUSK_FEED_TOPUP` re-buying wheat the same turn it was just sold, and d9/d10 `place 0/4` to `SHOP_ADAPT_HERD` buying the wrong animal species. Target marked SUPERSEDED. |
| `d18_harvest_and_sells_2026-08-12.md` | 2026-08-12 | d18's apparent harvest/sell shortfalls are cadence artifacts; the one genuine deficit is FERTILIZER 0/8, caused by the sell reserve computing `have = max(0, 9-12) = 0`. |
| `the_milk_must_be_in_the_shed_by_h05_2026-08-14.md` | 2026-08-14 | Forcing the tape's exact d8 orders plus banking milk earlier changed nothing — milk must be banked by h05 specifically. Nets a partial win: +20 exact cells, -$603 at d16. Supersedes the "first milk day" section of `the_wheat_row_and_the_turns_own_spending_2026-08-14.md`. |
| `the_wheat_row_and_the_turns_own_spending_2026-08-14.md` | 2026-08-14 | Diagnoses a d8 wheat-row order-accounting defect, but both tried fixes cost an identical -$9,577. The document explicitly supersedes its own framing: the wheat row is a symptom, the real story is cows first yield milk on d8 and the agent never uses PLACE to deposit it. |
| `handoff_plan_once_2026-08-09.md` | 2026-08-09, superseded note 2026-08-11 | The planner now plans each day once at dawn; d0/d1 exact vs Seb's tape, d2-d6 close but not exact. Target marked SUPERSEDED. |
| `replay_window_cannot_converge_2026-08-17.md` | 2026-08-17 | Inside the d5-d11 tape-replay window, divergence traces to 3 tiles where our own d0-d4 planted melon where the tape planted wheat. Fixing it cut refusals 5→1 and closed the d10 gap, but season money on a real seed still trails the best replay window. |

## The solver and routing

| File | Date | What it says |
|---|---|---|
| `fable_stage1_review_2026-08-09.md` | 2026-08-09 | The offline stage-1 genome scores $2,484/0-of-16-wins because a decode veto refuses every land-dependent chain, not because of the pricing cap it was blamed on. Recommends stage 1 not exist in its current form. |
| `plan_once_and_the_dawn_blind_spots_2026-08-09.md` | 2026-08-09 | Diagnosed four real blind spots in the once-per-day dawn plan (crew, goods, animals, pens); every attempted fix scored worse than HEAD's 317 work turns. Target marked SUPERSEDED, architecture findings still stand. |
| `the_day_is_a_cash_ledger.md` | Alex, 2026-08-10 | `short_of_cash` collapses a whole day's obligations into one boolean, forcing "deliver everything at hour 0." The ledger bug is real; the tape it was measured against is marked SUPERSEDED. |
| `fable_the_d4_d5_planner_2026-08-11.md` | 2026-08-11 | d4/d5 divergence traced to the spawn-ring step-off overwriting the farmer's hour-0 action, costing 6 unpriced turns. A "defer, don't delete" fix restores d4/d5 exactly. |
| `fable_the_d7_feed_2026-08-11.md` | 2026-08-11 | d7's dropped feed ration traced to the dawn wheat order being discarded when the order queue is already full (`len(orders) < 9`). Fixed with a `dawn_row_sent` flag; d0-d6 byte-identical afterward. |
| `fable_the_discard_problem_2026-08-09.md` | 2026-08-09 | Same-day CORRECTION: every discard quantity in the original document was wrong by ~15x (a shed-delta proxy double-counted same-step sales). Corrected full-season discard is ~7 units. One real day-gating bug fixed and shipped. File still exists on disk despite `REGISTER.md` OPEN-12 claiming it was deleted. |
| `d16_fertilizer_starvation_2026-08-12.md` | 2026-08-12 | An apparent d16 routing bug traces to a d11-d14 selling decision: FERTILIZER sell rows drain the same shed stock the day's own fertilize stops need. |
| `spawn_ring_misprediction_2026-08-12.md` | 2026-08-12 | Hires settle after the farmer's own hour-0 move, so the dawn plan's ring-slot prediction is systematically one slot early, costing a strawberry tile. The obvious fix (pin the farmer) was tried and reverted as a net loss. |
| `fable_spawn_ring_verdict_2026-08-12.md` | 2026-08-12 | Recommends fixing tour-budget slack before the ring-slot prediction fix, and finds a new bug: `_hires_this_turn` omits the `_unwalled_landing_slots` cap the market block applies. |
| `the_route_is_precomputable_2026-08-12.md` | 2026-08-12 | Confirms the board/geometry is identical in every game (one RNG, used only for shop-unlock draw and weeds), so routes can be solved offline. d12 is a genuine assignment defect (48/49→49/49 fixable); d18 is not. |
| `geometry_of_the_herd_2026-08-09.md` | 2026-08-09 | Pen-placement geometry is not a lever, confirmed a third time on two fresh loss episodes: walk-per-work-op is actually better on the geometrically worse side. Corrects a previously-cited "1.86 vs 2.93" figure that does not reproduce. |
| `d6_stranded_wool_2026-08-13.md` | 2026-08-13 | 4 of 9 wool units rode uncollected past dusk on d6 because of a delivery-rule interlock. Fixed with `SHIP_WHAT_NO_LATER_STOP_CAN_BANK = True`. |
| `d6_water_2026-08-13.md` | 2026-08-13 | d6's two missing waters traced to an asymmetry in `router.crop_ops`; the fix was measured as a net loss (waters unchanged, 2 plants displaced) and reverted the same day. |
| `the_last_growing_days_water_2026-08-14.md` | 2026-08-14 | A real 2-unit wheat yield loss from a watering-window/harvest-eligibility mismatch. The tested fix cost -$19,595 by starving the whole herd. Status: DIAGNOSED, FIX REVERTED, DO NOT RETRY AS WRITTEN. |
| `the_late_season_is_one_defect_in_two_halves_2026-08-12.md` | 2026-08-12 | DIG clears ground but nothing replants on it (half one) because plant_prize is zero for late plantings under the current harvest rule (half two). Both halves currently UNFIXED; half one alone was tried and cost -$2,898. |
| `where_the_harvest_gap_is_2026-08-15.md` | 2026-08-15 | A hypothesis, explicitly not yet measured: `WATER_ROTATION` may cause more total work but less harvest conversion (water +65, harvest -19 over d9-d29). Grid it was read off was itself contaminated (72% seated routes). |
| `fable_watering_post_d8_2026-08-15.md` | 2026-08-15 | Superseded mid-session: summed d9-d29 water is ours 798 vs tape 795 — no volume shortfall exists. A tried preventive-watering fix lost -$1,051 by displacing rescue waters; reverted immediately. |
| `strawberry_watering_2026-08-16.md` | 2026-08-16 | `_apply_precomputed` seats solved-day stops without pricing them against the unit's turn budget. Adding `_trim_to_the_day` moved money +$1,165 mean over 12 seeds and cut weeded tiles 183→120. |
| `allocation_bounds_2026-08-16.md` | 2026-08-16 | A MILP finds the near-optimal allocation range per crop/species; the leader's MELON 20/STRAWBERRY 34 split is NOT inside the 1% near-optimal region in any of three opponent-supply scenarios, costing 1.78%-23%. |
| `allocation_bounds_pass2_2026-08-16.md` | 2026-08-16 | Refines pass-1 bands 24-32% via a tighter solver gap, daily-water maintenance, and geometry-based walk cost. No fixed allocation is near-optimal across shop draws; melon oscillates toward a ~12-14 tile symmetric equilibrium under best-response iteration. |
| `cem_allocation_search_2026-08-15.md` | 2026-08-15 | A CEM allocation search, written mid-run — results sections explicitly marked PENDING/unfilled. Documents three pre-search design fixes and that unsolving routes for shift days costs 3x wall clock with no collection benefit. |
| `the_third_quadrant_arrives_a_day_late_2026-08-17.md` | 2026-08-17 | Across 19 ladder replays, the third-quadrant land purchase lands on d11 in all 19 games vs opponents' d10, because cash arrives in a lump at d10 h23 rather than smoothly through the day — but this alone doesn't explain every loss. |

## The late season and endgame

| File | Date | What it says |
|---|---|---|
| `fable_brief_sell_the_close_2026-08-15.md` | 2026-08-15 | Alex's handoff brief: copy カワシギ's close (sell everything d29, harvest d28, skip watering/feed/care on the last day). Real losses had stranded produce ($2,238-$3,526) exceeding the losing margin. Lists four previously-failed fixes not to retry blind. |
| `fable_close_the_season_2026-08-15.md` | 2026-08-15 | Six sequential deltas raise season close from $150,728 to $152,974 and cut stranded units 58-62 → 16, but the strict `TOLERATED_UNITS=12` xfail is still not met. |
| `fable_production_decay_d19_2026-08-15.md` | 2026-08-15 | Post-d19 decay is not caused by digging live crops or discarded production (both near-zero); it is thirst-killed strawberries (13 vs tape's 0) and one-shot crops rotting past their harvest window. |
| `the_stranded_load_is_the_loss_2026-08-15.md` | 2026-08-15 | In three downloaded ladder losses, stranded (undelivered) d29 produce value exceeds the losing margin, because the free shed-drop runs after the final turn — a d29 harvest not manually delivered banks nothing. |
| `after_the_close_release_2026-08-15.md` | 2026-08-15 | Documents what shipped (submission 55530699): season close 150,728→152,974 vs the tape's 150,076, stranded 62→16. Also: land-buy timing regressed since rebasing onto Victor, and tomato conversion is conditional, not universal. |
| `the_last_two_days_2026-08-17.md` | 2026-08-17 | d29's inventory drop happens after the final market process, so end-of-season stranded goods bank nothing. Fixed a dead `banking=False` flag and closed the stranded-load gap (9/9 drop matches tape), netting +$415 vs the tape. |
| `wasted_late_turns_2026-08-17.md` | 2026-08-17 | On a real ladder download: 11 units reachable-and-unharvested on d28-d29, plus a systematic defect where hour-1 hands are empty every day d25-d29 while HIRE orders fire the same turn (~300 unit-turns/season lost). |
| `fable_where_next_2026-08-11.md` | 2026-08-11 | Ranks six forward directions by measured EV, headlined by a late-season strawberry/melon sell dump costing ~$22.3k vs the Victor tape. File still exists on disk despite `REGISTER.md` OPEN-14 claiming it was deleted. |
| `the_late_season_is_one_defect_in_two_halves_2026-08-12.md` | 2026-08-12 | *(cross-listed — see solver-and-routing above; the doc is equally a late-season and a routing finding: DIG-then-nothing-replants near season end.)* |

## Animals and the herd

| File | Date | What it says |
|---|---|---|
| `what_saturates_and_what_does_not_2026-08-09.md` | 2026-08-09 | Corrects an earlier herd-revenue model that overstated output 4-6x. Corrected flat-saturation points: 16 cows, 16 sheep, 8 geese. Self-retracts its own goose-scaling claim the same day. |
| `the_goose_is_insurance_2026-08-15.md` | 2026-08-15 | Pure arithmetic: geese are not better than cows/sheep on expectation (~$8,000/six animals worse) but are the best insurance against a no-YARN_STORE draw (34.4% chance). Reopens the question the earlier `HERD_GEESE` verdict had closed under a bug. Retracts its own mid-document `theirs`-volume section same day. |
| `fable_geese_audit_2026-08-15.md` | 2026-08-15 | Audits the insurance case and finds geese lose on the Elo margin objective even though they win on raw money — margin-best in only 0.9% of shop draws, expected margin -$11,758 per six animals. States the `HERD_GEESE` deletion "was right by accident." |
| `q4_variant_first_draft_2026-08-15.md` | 2026-08-15 | First measurement of a fourth-quadrant (SE land + 4 sheep) branch: wins 11/11 vs shipped's 10/11, but the money delta (-$716 ± $2,837 SE) is indistinguishable from zero because the branch never relocates any planting onto the new ground. |

## Carrot and late-crop experiments

All seven files are from 2026-08-12 or 2026-08-24, i.e. the two sessions where carrot got serious
attention — the intervening ten days it was mostly unsellable (`SELLABLE` fixed 2026-08-13).

| File | Date | What it says |
|---|---|---|
| `carrot_swap_2026-08-12.md` | 2026-08-12 | Twice self-retracted (first because the schedule never sold the grown carrot, then because the whole "swap" frame was wrong). Final pool-sweep result: CARROT_SWAP costs -7.8 to -10.4 win-rate points over 384 games; stays OFF. `stale_audit_2026-08-15.md` flags this result itself as measured while carrot was unsellable and recommends deleting the file. |
| `the_optimal_carrot_2026-08-24.md` | 2026-08-24 | Grid-searches carrot conversion start day/tile count on the deepest-demand board on record: optimum is 56 tiles from d21, worth +$23,105 over planting none — but still a net loss of -$2,086 on that board. |
| `carrot_drain_gaps_2026-08-24.md` | 2026-08-24 | Extends the above by scanning 2,364 replay files: drain 10 never occurs, drain 9 has no games with us seated, and the drain 7-8 band is a coin flip (one loss→win swing +$21,922, one win→loss swing -$7,801) with no clean direction. |
| `souta_25_games_2026-08-24.md` | 2026-08-24 | Downloaded 25 of Souta's games: the carrot corner that beat us $29,384 appears in only 1 of 25. He is 19-6 overall and strong without it. Self-corrects an earlier session read that called him weak off the single game. |
| `stealth_the_carrot_mechanism_2026-08-24.md` | 2026-08-24 | An outside collaborator's analysis: Souta's carrot corner was deliberate — his 32 tiles were replanted from spent strawberry/wheat ground starting d22, not new plantings. Recommends a daily re-read gate plus an abstention rule. Flags an unreconciled number vs a separate analyst's figure, explicitly: "Do not average them." |
| `abstention_is_a_loss_2026-08-24.md` | 2026-08-24 | The abstention gate recommended above was implemented, tested, and measured to lose money on both towns where it fired (-$21,872 and -$88) because holding units to dump at once walks the price down further than selling gradually. Reverted, per the standing rule that a measured null is deleted, not left behind a switch. |
| `prompt_for_review_carrot_stuck_2026-08-24.md` | 2026-08-24 | A carrot-cornering theory reproduces the shape of a $29,384 loss in near-mirror replay but contributes zero difference across all six replayed real losses in the acceptance test. |

## Ladder game post-mortems

| File | Date | What it says |
|---|---|---|
| `the_field.md` | undated, addenda 2026-08-09/-11 | Top players submit fixed 720-turn open-loop scripts, running mixed economies (not the "83% milk and wool" single-episode myth this doc's own earlier read produced). |
| `the_top_five_clusters_2026-08-09.md` | 2026-08-09 | 15 replays cluster into three opening strategies; our best submission is roughly a third of the way to the public meta's floor. Marked SUPERSEDED IN SCALE by the 2,744-seat sample below. |
| `what_the_leaders_actually_grow_2026-08-09.md` | 2026-08-09, superseded 2026-08-11 | 18 of 20 downloaded top-ladder episodes are one mirrored public script. Concludes "we do not need a new tape" — explicitly marked SUPERSEDED: the field plants 108-147 wheat tiles to our 24. |
| `the_ladder_is_two_scripts.md` | measured 2026-08-11 | 1,372 episodes / 2,744 seats: the field runs two shared fixed scripts plus one reactive #1. Our best submission (1,257.9) doesn't appear in the sample at all; field median ~3,079. **This is the file most other docs' "TARGET SUPERSEDED" notes point back to.** |
| `ladder_losses_2026-08-11.md` | 2026-08-11 | 10 downloaded losses (explicitly flagged as a biased loss-only sample): melon is drained by no shop on any seed, so a fixed second melon wave dumps into a book we already sold into. |
| `kawashigi_one_board_2026-08-13.md` | 2026-08-13 | All 16 downloaded カワシギ games plus 4 of our own share an identical opening world/market/tiles hash; he is not open-loop past d3, going 15-1 on an identical board. File still exists on disk despite `REGISTER.md` OPEN-14 claiming it was deleted. |
| `the_ladder_is_lost_by_a_nose_2026-08-13.md` | 2026-08-13 | Same-day CORRECTION from Alex: the 60 downloaded games are losses-only, so every win-rate claim in the file was worthless and removed. What survives: losses are often narrow (median -$8,900). |
| `three_ladder_games_2026-08-15.md` | 2026-08-15 | 1 win + 2 losses: solver route-seating percentage does not predict outcome; real losses trace to the shop draw mismatching our fixed crop/herd mix, plus a reproducible FEED-scheduling miss. |
| `two_losses_2026-08-15b.md` | 2026-08-15 | Two more losses: feed/starvation fix holds live (0 animal losses); wool floors from oversupply but doesn't decide either game; real melon gap is production volume, not sell timing; both games had a $4-7k lead at d28 that decayed to a loss by d29. |
| `decision_points_2026-08-16.md` | 2026-08-16 | Tests whether カワシギ's two apparent decision rules beat a better constant tape: decision point 1 (melon vs strawberry at d3) is untested due to a confound; decision point 2 (four quadrants at d6, gated on YARN_STORE) is a real, measured +9.4% win, paired 19-1. |
| `where_we_lose_2026-08-24.md` | 2026-08-24 | Directly contradicts a prior claim that games go wrong at d12: 5 of 6 real losses are decided almost entirely on d29, driven by milk/wool collapsing to $1 mid-season while we keep producing into the dead book. |
| `where_99114898_went_2026-08-25.md` | 2026-08-25 (most recent file in `docs/`) | A real loss (-$26,277) attributed to the `q4_branch` land-latch firing on Alex's call despite its own docstring saying it never measured as a gain, plus `WOOL_SHOP_SETS_THE_HERD` flooding the wool book (price collapses $239→$11 on a 57-unit overshoot). |

## RL and imitation (parked)

| File | Date | What it says |
|---|---|---|
| `rl_feasibility.md` | ruling dated 2026-08-01 | States the reward is terminal (win 1, loss 0, gamma 1.0), per Alex's explicit call, overruling this file's own earlier argument for a per-step bank-delta reward. RL is parked because the field's top agents submit deterministic tapes with nothing to react to. The file has already self-corrected to match the ruling that `CLAUDE.md` states; do not read the ruling as still contested. |
| `lessons_carried_over.md` | undated | Distills the Orbit Wars RL post-mortem: measure before theorizing, heuristic-as-teacher-never-policy, one delta at a time. Contains an explicit correction that the terminal-reward rule now applies project-wide (this file used to argue the opposite). |

## Process and measurement lessons

| File | Date | What it says |
|---|---|---|
| `arena_state_leak_2026-08-09.md` | 2026-08-09 | `run_arena` passed one shared stateful agent object into every match, killing it after its first season and contaminating a market-shape investigation's numbers 17.8x. The actual submission gate (`gate_pool.py`) is confirmed unaffected. |
| `experiment_log.md` | append-only, spans 2026-07-31 onward | The full chronological experiment log across three eras. Its own version caveat says entries before 2026-08-07/08 are not comparable to anything measured since. |
| `dead_constant_audit_2026-08-17.md` | 2026-08-17 | Audits 40 module-level boolean constants in `kagg/search/` by reading each guard, not grepping. Finds 17 have an unreachable branch, and that `HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE = False` is dead code explaining why the herd never responds to the milk draw. |
| `stale_audit_2026-08-15.md` | 2026-08-15 | Read-only audit: `REGISTER.md` was checked in reverted/corrupted (missing a day of citation repairs, garbled first line, wrong date stamp); `CLAUDE.md`'s "parity PASSES" claim had already gone silently stale once before on the identical pattern. |
| `handoff_2026-08-15.md` | 2026-08-15 | The ladder went backwards two submissions running (1890.2 → 1428.4 → 1030.0) because precomputed routes were solved against a stale plan — only 143 of 571 stops were seated. |
| `work_to_be_done_2026-08-16.md` | 2026-08-16 | End-of-session open-threads log. Flags a regression found the same day: the day-matching gate moved from 260/520 failing to 303/477 failing, unnoticed, before this session caught it. |

## Infrastructure and throughput

| File | Date | What it says |
|---|---|---|
| `parity_restored_on_1326_2026-08-09.md` | 2026-08-09 | Both simulators made exact against installed `kaggle-environments` 1.32.6 again after fixing four unencoded rule changes (locked-tile movement, DROP/PICKUP/PLACE ordering, shed-capacity caps, shop unlock with replacement). |
| `throughput_measurements.md` | measured 2026-07-31 | Env throughput on the Mac (1,054 steps/s single-thread) vs the real Windows training box (484 steps/s, 2.2x slower per core). Corrects an earlier "1,032x" sim-speedup figure that was measured on a degenerate idle workload, down to a real 30x-200x range. |

---

## A note on files REGISTER.md says are deleted but are not

Three files in this index are cited in `docs/REGISTER.md` as "folded in here; file deleted," but all
three were confirmed present and readable on disk while building this index:

- `fable_the_discard_problem_2026-08-09.md` (REGISTER OPEN-12)
- `kawashigi_one_board_2026-08-13.md` (REGISTER OPEN-14)
- `fable_where_next_2026-08-11.md` (REGISTER OPEN-14)

This is reported here as a documentation accuracy issue, not acted on — no file was touched.
See the task's final report for the full list of candidates for removal and the reasoning behind
each.
