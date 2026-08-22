# docs/ — index

**Consolidated 2026-08-22, in three passes.** 124 files down to 20 top-level docs, and the five
topic docs down from 6,343 lines to 372.
Every original file is preserved, unedited, in `docs/history/` — nothing was deleted.

- **Pass 1** (`consolidation_2026-08-22.md`) read all 124 files and classified them. It reduced
  nothing; it is the input the other two passes used, and neither re-judged any file's status.
- **Pass 2** merged 110 files into five topic docs and `git mv`'d the originals into `history/`.
  It concatenated rather than decided, so the result was 6,343 lines in five files instead of
  6,343 lines in 110 — the same mess in fewer bowls.
- **Pass 3** cut those five to a settled-facts sheet each: one claim per line, the number and date
  that settle it on the line, and the `history/<file>.md` it came from at the end of the line.

That trailing pointer is what makes the cut safe. A line here is an index entry, never a
replacement for the file it points at. Contradictions are carried under their own heading and are
never resolved — an unresolved disagreement is information.

| topic doc | lines |
|---|---:|
| `market_and_economics.md` | 95 |
| `the_tape_and_planner.md` | 85 |
| `field_and_strategy.md` | 79 |
| `bc_and_rl_pipeline.md` | 60 |
| `animals_and_the_herd.md` | 53 |

## Read first

| File | What it is |
|---|---|
| `SUPER_IMPORTANT_READ_THIS_FIRST.md` | Read this before touching agent code. Docstrings that lie about what the code does; measure a rule at the decision, not the season census; the golden-output grid as the refactor lock; a list of things measured DEAD that must not be resurrected. |
| `REGISTER.md` | **The live open/closed list.** Owned live — read it, do not edit it outside its own process. Check before opening anything. |
| `stale_audit_2026-08-15.md` | What in this corpus is measured on a tape no longer shipped, through a bug now fixed, or against a flag that no longer exists. Some of its own findings are since resolved — `docs/consolidation_2026-08-22.md` §"contradiction 8" says which. |
| `competition_brief.md` | The rules, the scoring rule, and the version-skew history (1.32.2 → 1.32.6 → 1.32.7). |
| `architecture.md` | What the agent actually is, and the flags that ship off. |
| `kill_criteria_and_settled_positions.md` | Every kill criterion: MET or CLOSED. The terminal-reward ruling and the RL-parked ruling live here, with the measurements. |
| `experiment_log.md` | Every experiment, its score, and what it taught. Referenced directly by root `CLAUDE.md`. |

## The 20 top-level docs

Seven keep fixed paths because root `CLAUDE.md` or other tooling opens them by name:
`README.md`, `competition_brief.md`, `architecture.md`, `REGISTER.md`, `rl_feasibility.md`,
`lessons_carried_over.md`, `economics_q5_findings.md`.
Four more are kept at their own path because they are cross-referenced by name from elsewhere in
this project: `kill_criteria_and_settled_positions.md`, `experiment_log.md`,
`SUPER_IMPORTANT_READ_THIS_FIRST.md`, `stale_audit_2026-08-15.md`.
Four are live status, written 2026-08-22, and were not touched by this pass:
`status_2026-08-22.md`, `geese_verdict_status_2026-08-22.md`, `consolidation_2026-08-22.md`,
`test_plan_2026-08-22.md`.
The remaining five are new merged topic docs, each replacing a batch of dated diagnostic files:

| Topic doc | Merges | What it covers |
|---|---:|---|
| `field_and_strategy.md` | 19 files | What the opponent field actually does; the rebase-target question; board/turn-capacity limits; allocation bounds; the arm-classifier idea. |
| `the_tape_and_planner.md` | 58 files | Every planner/routing/watering bug diagnosed against a reference tape, Seb-era through the current Victor/Kawashigi/tetsuya lineage. The largest merge — organised chronologically in three parts. |
| `market_and_economics.md` | 22 files | The sell mechanism, the 2026-08-15 hinge/balance change, saturation and absorption tables, carrot/tomato/egg economics, crop-mix and route scoring, simulator parity fixes, pen geometry. |
| `animals_and_the_herd.md` | 5 files | The cow/sheep/goose mix, the geese verdict (money vs. margin/Elo objective), real ladder losses from animal-book flooring, pen-placement geometry. |
| `bc_and_rl_pipeline.md` | 7 files | Problem framing, measured env/sim throughput, the offline schedule-search stack, BC pipeline defects, the imitation/DAgger plan. Cross-references `rl_feasibility.md` rather than duplicating it. |

`docs/history/` holds all 110 originals these five docs were built from, unedited, exactly as
written — open a file there directly if you need a merged doc's full original context, a number this
index dropped, or the file's own superseded/retracted framing in full.

## Known unresolved contradictions

Carried forward from `docs/consolidation_2026-08-22.md`, and repeated inside the relevant topic doc
so a reader hits them in context, not only here.

1. **Melon-swap direction.** Root `RETRACTIONS.md` (outside `docs/`, not edited by any pass) item 7
   reports a 960-game population sweep where the shipped rule narrowly beat turning it off (68.1% vs
   67.9%). Two in-repo docs (in `market_and_economics.md` and `the_tape_and_planner.md`) say the
   opposite on smaller samples. Not reconciled — see `market_and_economics.md` §3.
2. **Whether the shop draw is seed-only or agent-dependent.** `field_and_strategy.md` (from
   `kawashigi_one_board_2026-08-13.md`) says the seed alone decides it; `the_tape_and_planner.md`
   (from `marginal_units_and_the_shared_book_2026-08-16.md` §9) found the weed-spawn RNG is consumed
   per-tile before the shop draw, so which agent plays shifts it. Both measured, neither cites the
   other.
3. **`REGISTER.md`'s own baseline command names a retired tape** (`seb`) and errors before running.
   Not edited by this pass — `REGISTER.md` is live-owned.
4. **Whether fast-sim parity is green right now is unverified.** Root `CLAUDE.md` states 300/300
   pass as fact with no version qualifier; no doc names a full-episode parity run since the
   2026-08-15 1.32.7 hinge change landed.
5. **The 2026-08-11 rebase recommendation** (Dmitry Belan or Efe Can Celiksoy, not Seb) was never
   adopted and `REGISTER.md` OPEN-10 is not marked closed. See `field_and_strategy.md`.
6. **Two "our agent vs. the tape" season numbers do not reconcile**: one full season finishes +$415
   ahead of the tape; a d24 handover measurement has the planner losing $7,713 to a full replay,
   before that day's fixes. Different setups, neither cites the other. See `the_tape_and_planner.md`.
7. **A same-day tape-gate baseline disagrees with itself**: 311 failed/590 passed vs., measured the
   same day, 356 failed/545 passed. See `the_tape_and_planner.md`.

Full detail and two more meta-findings (about `stale_audit_2026-08-15.md` itself) are in
`docs/consolidation_2026-08-22.md`.

## Today's live status

Read these for where things stand right now — written 2026-08-22, not touched by this pass:

- `status_2026-08-22.md`
- `geese_verdict_status_2026-08-22.md`
- `consolidation_2026-08-22.md` — the first pass's method, full classification, and contradiction
  detail behind the summary above.
- `test_plan_2026-08-22.md` — a running test queue, landed on the branch mid-consolidation (commit
  `116b042`). Explicitly not yet run ("nothing here has been run") — not merged or moved by this
  pass, same treatment as the three files above.

## RL

`rl_feasibility.md` and `kill_criteria_and_settled_positions.md` carry the full RL ruling and are
not merged into anything — read them directly. The RL track is parked; see root `CLAUDE.md`.

`lessons_carried_over.md` is the Orbit Wars post-mortem, distilled; not version-dependent.
