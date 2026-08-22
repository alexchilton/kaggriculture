# Consolidation — 2026-08-22

Documentation-only pass. Nothing under `kagg/`, `scripts/`, `tests/`, `reference/` or `data/` was
touched. Nothing was deleted. `docs/README.md`, `docs/REGISTER.md`, `docs/status_2026-08-22.md` and
`docs/geese_verdict_status_2026-08-22.md` were either rewritten (README) or left untouched
(REGISTER, and the two live-status files another agent was writing at the same time).

Trigger: 120 markdown files, 21,786 lines, no index past 2026-08-15. Forty-eight files postdating
that index existed with zero pointer to them.

## Method

Read `docs/README.md`, `docs/REGISTER.md`, `docs/SUPER_IMPORTANT_READ_THIS_FIRST.md` and
`docs/stale_audit_2026-08-15.md` directly. Split the remaining 116 files into six batches of ~20 and
read every one of them in full via parallel sub-agents, each returning: the file's central claim
with numbers, any status banner already in the file, which other files it names as superseding or
superseded, a suggested classification, and any numeric or verdict conflict with another file. This
document is the synthesis of those six reports plus my own direct reading of the four files above.

No number in any file was re-measured. No experiment was run. Classification is about what a file
*says*, and about how a later file says something different, not a re-derivation of who is right.

## Classification counts

Of 120 files in `docs/` (excluding the two live-status files being written by another agent):

- **CURRENT** — roughly 70. Describes something still true and still relevant, or is a self-marked
  live diagnosis with no successor yet.
- **SUPERSEDED** — 12, of which 5 already carried their own banner before this pass
  (`the_top_five_clusters_2026-08-09.md`, `what_the_leaders_actually_grow_2026-08-09.md`,
  `kawashigi_algorithm_2026-08-21.md`, `fable_the_discard_problem_2026-08-09.md`'s headline numbers,
  `carrot_swap_2026-08-12.md`'s own arms). 7 got a new banner this pass (below).
- **HISTORICAL** — roughly 30. A settled decision, a measured-and-reverted arm, or a superseded
  imitation target — kept for the lesson, not for the number.
- **STALE** — 1 clean case (`when_and_what_to_sell_2026-08-15.md`), plus two files
  (`architecture.md`'s kill-criteria table, `REGISTER.md`'s own baseline command — not edited, see
  below) whose *specific claims* are stale while the surrounding file is current.
- **unsure — needs an owner's eye** — 4: `cem_allocation_search_2026-08-15.md` (abandoned mid-run),
  `the_goose_is_insurance_2026-08-15.md` (self-retracts its own numbers, conclusion agrees with the
  file that replaced it), `seed_outranks_product_the_fix_and_its_cost_2026-08-21.md` (an explicit
  open ship/no-ship decision), `the_ladder_is_two_scripts.md` (its rebase recommendation was never
  adopted or formally closed — see contradiction 5 below).

One non-markdown file, `why_we_lost_93318573_93323101.log`, is a raw script-output dump (83 lines,
per-game demand tables for two loss episodes) sitting in `docs/`. Not a doc, not indexed, flagged so
an owner can decide whether it belongs in `data/logs/` instead.

## Banners added (7 new; 5 files already had one)

Each is a one-line blockquote at the top of the file. The file's own content was not otherwise
touched.

| file | banner added |
|---|---|
| `when_and_what_to_sell_2026-08-15.md` | STALE — the +$12,136 total is an infeasible-baseline comparison (real value +$5,653, per `fable_allocation_economics_2026-08-15.md`); its own falsifiable prediction was tested on 960 games and lost (68.1% vs 67.9%, root `RETRACTIONS.md` item 7) |
| `allocation_bounds_2026-08-16.md` | SUPERSEDED by `allocation_bounds_pass2_2026-08-16.md`, same day |
| `fable_fourth_quadrant_2026-08-15.md` | SUPERSEDED by `fable_fourth_quadrant_reopened_2026-08-15.md`, same day — the $21,960 crew-cost closer is retracted |
| `the_stranded_load_is_the_loss_2026-08-15.md` | CLOSED by `the_last_two_days_2026-08-17.md` |
| `cem_allocation_search_2026-08-15.md` | unsure — still reads RESULT PENDING with no completion found anywhere; same question answered a day later in `allocation_bounds_pass2_2026-08-16.md` |
| `carrot_swap_2026-08-12.md` | SUPERSEDED by `carrot_and_the_empty_book_2026-08-19.md` — this file's own arms are already self-retracted, and `CARROT_SWAP` no longer exists in the code |
| `fable_bc_pipeline_review_2026-08-20.md` | cross-reference note — `fable_bundle_head_review_2026-08-20.md` (same day) found the mask mechanism this file analyzes has never executed |

Three more files got a short "read together with" or "note added" line, not a full SUPERSEDED
banner, because only part of the file is affected: `the_field.md` (points forward to
`the_field_is_a_monoculture_2026-08-21.md`), `market_curves_and_the_q4_branch_2026-08-15.md` (its
§7 q4 number, not the market-curve tables, is superseded by `q4_variant_first_draft_2026-08-15.md`),
`kawashigi_one_board_2026-08-13.md` (qualified, not overturned, by a later endogenous-shop-draw
finding), and `the_late_season_is_one_defect_in_two_halves_2026-08-12.md` (points forward to where
it was implemented and measured).

`docs/README.md` was rewritten with a new top section covering all 120 files by topic; the older
2026-08-08/09/11/15 consolidation layers below it were left in place, unedited, as history.

## Contradictions found

Ranked by how much they can cost a reader who doesn't know about them.

### 1. Two different measured population sizes disagree on the melon-swap rule's direction

`docs/when_and_what_to_sell_2026-08-15.md` (a model, not a game) and
`docs/work_to_be_done_2026-08-16.md` §4 (a direct A/B, `-$17,297/game`, 66.7% vs 0% win rate) both
say **keeping melon beats swapping**. The root-level `RETRACTIONS.md` item 7 reports a 960-game
population sweep where the shipped swap rule (`MELON_YIELD_OPPONENT_MELON = 7`) narrowly **beat**
turning it off (`= 99`) — 68.1% vs 67.9%. `RETRACTIONS.md` is outside `docs/` and outside this task's
scope to edit, but the disagreement is real and unresolved in any file that names it. Possible
reconciliation: the small-N arms may be measuring a different, narrower trigger condition than the
960-game population sweep's blanket rule — nobody has checked. Flag for an owner.

### 2. Whether the shop draw is seed-only or agent-dependent

`docs/kawashigi_one_board_2026-08-13.md`: "the seed's only job is the shop draw" (16 カワシギ games,
identical board, only the shop-unlock sequence varies). `docs/marginal_units_and_the_shared_book_2026-08-16.md`
§9: the weed-spawn RNG is consumed per-tile *before* the shop draw, so which agent plays shifts the
draw — the same seed produces different shop sequences under different agents. Both are measured;
neither doc cites the other. Noted in a banner added to the first file this pass; not reconciled.

### 3. `REGISTER.md`'s own baseline command names a tape that no longer exists

`docs/REGISTER.md` (not edited — out of scope, live-owned) still reads `baseline seed 11, weeds 0.0,
tape seb` and gives `python -u scripts/breakdown.py --tape seb ...` as "the only metric that counts."
`scripts/breakdown.py`'s `TAPES` dict contains only `victor` and `kawashigi`; `seb` is in
`RETIRED_TAPES` and the command errors on argparse before running anything. The same dead value is
repeated in `docs/experiment_log.md:432` and `docs/the_field.md:200`. First found by
`docs/stale_audit_2026-08-15.md` (2026-08-15); still true as of this pass (2026-08-22), seven days
later. Someone with write access to `REGISTER.md` needs to fix this; this pass could not.

### 4. Whether fast-sim parity is actually green right now is unverified, and CLAUDE.md states it as fact

`CLAUDE.md` (root, not edited): "Fast-sim parity PASSES — 300/300 full-length episodes exact,"
stated with no version qualifier as one of three still-binding rules.
`docs/architecture.md` (dated, still true as written): "2026-08-09: both simulators FAIL parity on
the installed 1.32.6 env — 8 failures... restored to exact parity the same day
(`docs/parity_restored_on_1326_2026-08-09.md`)." No file in `docs/` names a fresh full-episode parity
run since the 2026-08-15 `kaggle-environments` 1.32.7 "hinge" fix landed in `kagg/sim/market.py` and
`kagg/sim/jax_sim.py`. Code-level, both files do have a `hinge` branch now. Whether the 300/300 gate
has actually been re-run since is not established by any doc. First flagged in
`docs/stale_audit_2026-08-15.md`; still open.

### 5. The strategic rebase target recommended on 2026-08-11 was never adopted, and nothing says why

`docs/the_ladder_is_two_scripts.md` (2,744 ladder seats) recommends rebasing the schedule on
**Dmitry Belan** or **Efe Can Celiksoy**, explicitly not Seb. Every dated diagnostic file from
2026-08-12 onward instead measures against **Victor**, **Kawashigi**, or **tetsuya** — none of which
is Belan or Celiksoy. `docs/REGISTER.md`'s OPEN-10 (this exact recommendation) is not marked CLOSED.
No file explains the divergence. `docs/stale_audit_2026-08-15.md` flagged this as "may just be an
unclosed item rather than a wrong one" on 2026-08-15; seven days and dozens of files later, it is
still neither closed nor explained. Classified `the_ladder_is_two_scripts.md` as
**unsure — needs an owner's eye** rather than CURRENT or SUPERSEDED for this reason.

### 6. Two head-to-head "our agent vs the kawashigi tape" season numbers do not reconcile

`docs/the_last_two_days_2026-08-17.md`: full shipped season finishes **+$415 ahead** of the tape
(154,740 → 155,155 vs 150,076). `docs/the_tape_beats_our_planner_2026-08-21.md`: at a d24
tape-to-planner handover, the planner **loses $7,713** to a full tape replay, before that day's three
one-line bug fixes. The setups differ (full season vs. partial replay-then-planner), and neither
file cites the other or states whether the fixes since 08-17 changed the 08-21 number. Not
necessarily a real conflict — flagged so an owner reconciles rather than quotes either number as
"the" head-to-head result.

### 7. A same-day baseline table disagrees with itself

`docs/work_to_be_done_2026-08-16.md` records the tape-gate baseline as 311 failed / 590 passed.
`docs/strawberry_watering_2026-08-16.md`, written the same day, re-measures what should be the same
starting state as 356 failed / 545 passed, and says so explicitly ("flags `work_to_be_done`'s
baseline... as stale"). Neither number has been reconciled since.

### 8. `stale_audit_2026-08-15.md`'s own findings are now half resolved — it is not fully current either

Verified directly this pass: `docs/REGISTER.md` is **not** corrupted (finding 1a is resolved — the
file now reads cleanly with three dated version caveats) and `docs/competition_brief.md` **does**
already carry the 1.32.7 / hinge version-skew section (finding 1c is resolved — the file has a
"Version skew — and it has moved TWICE now" section naming PR #1399 and requiring
`kaggle-environments>=1.32.7`). Findings 1b (parity claim, see #4 above), 1d (dead `--tape seb`, see
#3 above), 1e (`when_and_what_to_sell`, now bannered) and 1f (`carrot_swap`, now bannered) are still
live. Read `stale_audit_2026-08-15.md` for its method and its still-open findings, not for 1a/1c.

## What was not done

No file was deleted. No number was corrected in place beyond the seven new banners above — the
instruction was to flag, not to re-derive. `RETRACTIONS.md` (repo root) and `CLAUDE.md` (repo root)
were read where cited but not edited — both are outside `docs/`. `docs/REGISTER.md`,
`docs/status_2026-08-22.md` and `docs/geese_verdict_status_2026-08-22.md` were not touched, per the
brief for this pass.
