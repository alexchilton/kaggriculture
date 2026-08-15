# docs/ — index

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
