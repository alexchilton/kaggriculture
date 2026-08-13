# docs/ — index

**Severe consolidation pass, 2026-08-13.** Went from 45 files (49 counting three that had never been
committed) down to the 15 below plus this index and `REGISTER.md`. Nothing was silently deleted —
every file removed had its measured numbers copied into a surviving doc first; the "Where each
deleted file's content went" table at the bottom names every one. This pass sits on top of an
earlier 2026-08-08 consolidation (87 files → 11) and a 2026-08-11 one (which added
`the_ladder_is_two_scripts.md` as the new strategic position); both are summarized further down.

## Two corrections that apply to almost everything measured before 2026-08-13

1. **`SELLABLE` excluded CARROT, TOMATO and EGG until commit `c99a8a5` (2026-08-13).** Our own agent
   could not emit a SELL for those three products regardless of market conditions. Any older
   conclusion about carrots not selling, or about geese/eggs being unprofitable, was measured with
   that revenue line disconnected and is void — flagged inline wherever it survived into a merged
   doc. `docs/REGISTER.md`'s version-caveat block has the full statement.
2. **The ladder moved to `kaggle-environments` 1.32.6 on 2026-08-07/08** — town-centre drain fell
   roughly 8x (`townCenterSellInterval` 12→24, the late-season demand ramp deleted). Any dollar
   figure dated before that is on a different economy; `docs/competition_brief.md` "Version skew"
   has the mechanics.

## Read in this order

0. This file.
1. `docs/competition_brief.md` — the competition, the scoring rule, engine rules that have each cost
   a day, the 1.32.2/1.32.6 version skew.
2. `docs/architecture.md` — what the agent actually is, the flags that ship OFF and why, the harness
   caveats, what the shipped agent scores against the pool.
3. `docs/REGISTER.md` — the live open/closed list. **Check it before opening anything** — items here
   reopen under new names, sometimes six times.
4. `docs/rl_feasibility.md` — the RL track's measurements and why it's parked.
5. `docs/lessons_carried_over.md` — the Orbit Wars post-mortem, distilled.
6. `docs/economics_q5_findings.md` — yields, allocation, storage. Largely version-independent; town
   drain specifically superseded by `the_market.md` §2.

`reference/` holds the competition docs and the environment source. The env source is ground truth;
read it rather than trusting any doc where the two disagree.

## The 15 surviving topic docs

| File | What it answers |
|---|---|
| `competition_brief.md` | The rules, the scoring, version skew. Core, unchanged this pass. |
| `architecture.md` | What ships, what's OFF and why, harness warnings, current pool score (94.4% win, $108,180 mean). |
| `rl_feasibility.md` | Why the RL track is parked, and what it measured that generalizes. |
| `lessons_carried_over.md` | Orbit Wars post-mortem, what transfers and what doesn't. |
| `economics_q5_findings.md` | Yields, per-quadrant supply vs drain, storage timing value. |
| `experiment_log.md` | Append-only history — every experiment, its score, its lesson. §1-26. |
| `the_field.md` | What real opponents do: open-loop scripts, the mixed economy, how the leader funds day 0. |
| `what_kind_of_problem_this_is.md` | The problem class (deterministic knapsack vs a fixed field), and which tools it rules out. |
| `throughput_measurements.md` | Measured env throughput on the training box; not version-dependent. |
| `the_ladder_is_two_scripts.md` | **Current position on strategy.** 2,744 ladder seats: two shared scripts, the field plants 108-147 wheat against our 24, the ladder is one fixed board, loss forensics (melon-as-fixed-pot, narrow-loss magnitude distribution). |
| `the_market.md` | **The marketplace.** The derived sell rule, 87-tape real appetite measurement, fill-vs-offer analysis, intra-day cadence defects, the late-season investigation (with the SELLABLE-voided geese/egg retraction), carrot economics (pool verdict voided, needs re-run), ranked levers. |
| `market_depth_and_the_morning_losses_2026-08-13.md` | **Current and authoritative on price mechanics.** The base/shops/drain/price-at-N/floor table, two real ladder losses decomposed by product and by day, the herd-starvation/bare-pasture finding. |
| `matching_the_tape_mechanisms.md` | Ten planner bugs found by diffing against a reference tape — Seb's route architecture, the tape-column harness bug, the plan-once dawn blind spots, the cash-ledger bug, and (not superseded) two live bugs found against Victor's tape, the current submission target. |
| `spawn_ring_and_routing.md` | The spawn-ring misprediction (hands land one ring slot early), the reverted pin-the-farmer fix, and why routing can be solved offline (the board is a deterministic constant; a real d12 assignment defect found that way). |
| `fertilizer_and_wheat_supply.md` | Two supply-management defects in the market emission block: fertilizer sold out from under its own fertilize stops (open), and the wheat purchase budget that had us buying 4x the field's volume (closed, fix shipped). |

## Where each deleted file's content went, this pass (2026-08-13)

**Into `docs/the_market.md`** (10 files): `the_market_2026-08-09.md`, `what_the_town_will_actually_eat.md`,
`what_saturates_and_what_does_not_2026-08-09.md`, `fable_market_shape_2026-08-09.md`,
`the_book_is_shallow_2026-08-09.md`, `the_market_cadence_over_all_products_2026-08-10.md`,
`the_market_is_the_late_season_2026-08-13.md`, `the_late_season_is_one_defect_in_two_halves_2026-08-12.md`,
`d18_harvest_and_sells_2026-08-12.md`, `carrot_swap_2026-08-12.md`.

**Into `docs/the_ladder_is_two_scripts.md`** (6 files): `the_top_five_clusters_2026-08-09.md`,
`what_the_leaders_actually_grow_2026-08-09.md`, `kawashigi_one_board_2026-08-13.md`,
`ladder_losses_2026-08-11.md`, `the_ladder_is_lost_by_a_nose_2026-08-13.md` (all as new sections),
plus `fable_where_next_2026-08-11.md` (its measured facts split between here and `REGISTER.md` OPEN-14).

**Into `docs/matching_the_tape_mechanisms.md`** (10 files): `fable_matching_the_tape_2026-08-10.md`,
`how_sebs_planner_works_2026-08-10.md`, `how_seb_feeds_the_herd.md`, `the_day_is_a_cash_ledger.md`,
`plan_once_and_the_dawn_blind_spots_2026-08-09.md`, `handoff_plan_once_2026-08-09.md`,
`router_tape_repoint_2026-08-09.md`, `the_tape_column_does_not_replay_his_game_2026-08-09.md`,
`fable_the_d4_d5_planner_2026-08-11.md`, `fable_the_d7_feed_2026-08-11.md`.

**Into `docs/spawn_ring_and_routing.md`** (3 files): `fable_spawn_ring_verdict_2026-08-12.md`,
`spawn_ring_misprediction_2026-08-12.md`, `the_route_is_precomputable_2026-08-12.md`.

**Into `docs/fertilizer_and_wheat_supply.md`** (2 files): `d16_fertilizer_starvation_2026-08-12.md`,
`fable_the_wheat_churn_2026-08-09.md`.

**Into `docs/REGISTER.md`** (4 files, as new OPEN items or extended CLOSED entries):
`fable_the_discard_problem_2026-08-09.md` (OPEN-12, the feed-reserve eviction throttle),
`arena_state_leak_2026-08-09.md` (OPEN-13, the unfixed seat-swap defect — headline already in
`architecture.md`), `geometry_of_the_herd_2026-08-09.md` (extends C-21 with a third confirmation and
corrected ring-depth figures), and part of `fable_where_next_2026-08-11.md` (OPEN-14).

**Into `docs/architecture.md`**: the parity-restoration headline and the shipped-pool-score table
from `parity_restored_on_1326_2026-08-09.md` and `arena_state_leak_2026-08-09.md`.

**Into `docs/experiment_log.md`** (as new closed entries, §25-26): the technical abandonment reasons
from `fable_stage1_review_2026-08-09.md`, and a pointer to the wheat-supply fix now documented in
full in `fertilizer_and_wheat_supply.md`.

Three files that existed only uncommitted in the working tree (`fable_spawn_ring_verdict_2026-08-12.md`,
`spawn_ring_misprediction_2026-08-12.md`, `fable_where_next_2026-08-11.md`) were folded in the same
way as their committed siblings — nothing was lost for having never been committed.

## What survived this pass unmerged, and why

`competition_brief.md`, `architecture.md`, `REGISTER.md`, `rl_feasibility.md`,
`lessons_carried_over.md`, `economics_q5_findings.md`, `experiment_log.md`, `the_field.md`,
`what_kind_of_problem_this_is.md` and `throughput_measurements.md` were already single-topic,
already load-bearing (cross-referenced from `CLAUDE.md` and from each other), and already the
product of the 2026-08-08 consolidation below — there was nothing left to merge them into.
`market_depth_and_the_morning_losses_2026-08-13.md` was written the same day as this pass and is
current; its numbers were not rewritten, only cross-referenced from `the_market.md`.

## The rules that survived every cull, in one place

- **Check the env version before trusting a number.** 1.32.2 → 1.32.6 on 2026-08-07/08: town-centre
  drain halved (then halved again on the later `townCenterSellInterval` 12→24 move — 8x total), melon
  absorption fell, the `BUY_PRODUCT`-bypasses-`shedCapacity` loophole closed.
- **Check SELLABLE before trusting a carrot/tomato/egg/goose number.** Fixed 2026-08-13, `c99a8a5`.
- **The ladder is Elo and starts at 600.** Winning matters, margin does not. Select on win rate.
- **We are not close to the field.** Best submission 1,257.9 against a field top of ~3,210 (2,744
  ladder seats, `the_ladder_is_two_scripts.md`).
- **The ladder deals one fixed board, not a random draw per seed.** "Seed variance ~15%" describes
  `kagg.arena`'s randomly-drawn boards, not the ladder.
- **Never evaluate against `starter` alone, the arena pool, or the handover fixture as the whole
  story.** `vs_tapes.py` against `oldleader` is the instrument that currently discriminates.
- **A mirror match is not a best response.** An Elo ladder rewards beating a *field*.
- **Judge a fix at the day it targets, field by field.** Season totals are a weak signal, and
  `breakdown.py --diff`'s `money` row is an *area*, not a deficit.
- **A gate only tests what it exercises.** Ask what a passing test could not reach.
- **After fixing, revert the fix and confirm the test goes red.**
- **Before believing a measurement about a mechanic, ask what the code could not express.** Animal
  economics have been an artifact of our own code five separate times now (see
  `docs/REGISTER.md`'s note on the pattern).
- **Prefer a replay to an aggregate whenever the aggregate could be a tie.**
- **We plant a fifth of the wheat the field does.** 24 tiles against the field's 108-147.
- **The cow COUNT is what floors our own milk price**, not sell timing — every recent real loss
  where `SHOP_ADAPT_HERD` cut cows to 6 closed milk above base; every one at 8-9 cows floored it.

## Earlier consolidations, condensed

**2026-08-11:** the official episode datasets (1,372 episodes, 2,744 seats) gave the project its
first population-scale read of the field and overturned the working assumption behind most of the
"matching-the-tape" line of work: Seb's tape was optimal only under the old economy and is no longer
the strategic target (his own median bank halved when the town rebalance landed, and he withdrew
from the ladder). This produced `the_ladder_is_two_scripts.md`, which this 2026-08-13 pass extended
rather than replaced.

**2026-08-08:** consolidated 87 markdown files / 17,774 lines down to 11 files / ~2,670 lines. Most
of what was cut was session narration, superseded diagnosis, or an advisor write-up whose
recommendation had been measured and rejected. Full detail (session diaries, dead-mechanism docs,
reversed conclusions, advisor write-ups, duplicated findings, and a table of which deleted doc's
content went where) is preserved in git history — `git log --follow -- docs/README.md` and the
commit that first wrote the 2026-08-08 version of this file — rather than reproduced here a second
time. `CLAUDE.md`'s "Read these first" list and the "Lessons learned the hard way" section carry the
durable rules from that pass forward regardless.

`CLAUDE.md` at the repo root holds the project rules, the kill criteria, and the "lessons learned the
hard way" list. It is not superseded by anything here.
