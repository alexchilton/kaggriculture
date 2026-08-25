# What is still true, 2026-08-25

A digest of live findings across all 96 files in `docs/`, built by reading every file's opening
paragraph and verdict line.
Every claim below names the file it came from.
Where a later file contradicts an earlier one, the earlier one is marked SUPERSEDED and the
superseding file is named.
Where two docs disagree and neither dates nor content settle which is current, that is stated
plainly rather than guessed.

This file does not replace `docs/README.md` or `docs/REGISTER.md`.
It exists because both were last restamped 2026-08-15, and ten days of work since then
(`docs/*_2026-08-16.md` through `docs/*_2026-08-25.md`, 21 files) changed several of the pictures
those two files still show.

**`docs/the_shed_is_the_bottleneck_2026-08-25.md` was committed mid-session** (12:44, 2026-08-25),
after this digest's file count was first taken. It is folded into "Market and pricing" below.

## Rules that still bind, unchanged since the 2026-08-15 consolidation

Nothing found in the 2026-08-16 through 2026-08-25 files contradicts any of these.

- **The reward is terminal** (win 1, loss 0, gamma 1.0), never per-step. `rl_feasibility.md`,
  `kill_criteria_and_settled_positions.md`. RL is parked.
- **Select on win rate / Elo margin, not money.** A $43k win and a $4k win score identically.
  Applied throughout the carrot and geese work below.
- **The ladder is one fixed board per game**, not a random per-seed draw. Only the shop-unlock
  draw and weed placement vary. `kawashigi_one_board_2026-08-13.md` (16 downloaded games,
  identical world/market/tiles hash).
- **Seb's tape is not the strategic target.** His median bank halved when the town rebalanced and
  he has withdrawn from the ladder. `the_ladder_is_two_scripts.md` (2,744 seats). Every tape-matching
  mechanism doc dated 2026-08-09/-10/-11 is banded "TARGET SUPERSEDED" for this reason — the
  mechanism fixes inside them are still real, the tape they matched against is not the goal.
- **We plant a fifth of the wheat the field does** (24 tiles vs the field's 108-147). Still the
  largest single measured gap, unchanged by anything read since.
- **A gate only tests what it exercises**, and **judge a fix at the day it targets**, never on the
  season total. Both restated and used correctly throughout the 2026-08-16 to -25 work.

## Market and pricing

- Melon and fertilizer are always over-supplied (closing surplus always positive across 87 tapes);
  wheat is always scarce (closing deficit $40-59 above a $25 base).
  `what_the_town_will_actually_eat.md`. Not contradicted by anything more recent.
- Re-pricing our own sales downward (live-price selling, both `PRICE_AWARE_SELL_CAP` and
  `RESERVATION_SELL_CAP` shipped ON) turns 12 of 14 real ladder losses into wins in the original
  measurement. `the_market_2026-08-09.md`.
- **Milk and wool floor mid-season and we keep producing into the dead book.** Confirmed twice
  independently and recently: `the_market_is_the_late_season_2026-08-13.md` (COW 10/SHEEP 4 floods
  milk to $1-$5/unit vs $223 realized elsewhere) and `where_we_lose_2026-08-24.md` (milk/wool close
  at $1 in 5 of 6 real losses by d13-d20). This is the single most consistently re-confirmed market
  finding in the whole set.
- **Losses concentrate on d29, not mid-game.** `where_we_lose_2026-08-24.md` measured 5 of 6 real
  losses decided almost entirely on d29 — level or ahead through d28 in 4 of 6 — directly
  contradicting an earlier internal claim that "the game goes wrong at d12." This is the most
  recent market-shape finding (2026-08-24) and nothing newer contradicts it.
- **`fable_where_the_money_is_2026-08-24.md`** (same day, reviewing the above) reframes the cause as
  cadence — selling past a season's supply budget — rather than execution, and proposes a combined
  fix. Not yet measured as landed; treat as a proposal, not a result.
- **The mechanism behind the cadence problem: the shed jams at its 100-unit cap.**
  `the_shed_is_the_bottleneck_2026-08-25.md` (the newest file in `docs/`) measured 35 real ladder
  games: our shed sits within ten units of capacity 2,505 turns against opponents' 488 — five times
  as often. On the strawberry solver arm, d12-d23, this costs ten extra harvests but 177 fewer units
  sold (-$11,073), because overflow is silently discarded at dawn and further harvests have nowhere
  to go. The doc explicitly rules out routing and the walk to the shed as causes (routes are
  gap-free, DROP happens 1,425 times across the 35 games) and names sell cadence as the fix to try.
  It also proposes the direct mechanism behind the wool-price collapse flagged below: "a jammed shed
  forces exactly that behaviour: you dump whatever you can whenever you can, rather than metering
  sales to the price." **Not yet fixed or measured as a fix — this is a diagnosis, not a landed
  change.**

### SUPERSEDED in this group

- `when_and_what_to_sell_2026-08-15.md`'s headline "+$12,136 even spread" figure — superseded by
  `fable_allocation_economics_2026-08-15.md`'s "+$5,653," computed against a feasible baseline.
- `the_wheat_row_and_the_turns_own_spending_2026-08-14.md`'s "first milk day" section — superseded
  by `the_milk_must_be_in_the_shed_by_h05_2026-08-14.md`: right about the day, wrong about the fix.
- `fable_market_shape_2026-08-09.md` §4/§4.1/§5 — its pool numbers rest on a harness that
  `arena_state_leak_2026-08-09.md` found was reusing one shared stateful agent object across
  matches. Not re-measured since; treat the 14.6%→27.1% `LATE_SELL_BIAS` win-rate jump as
  unconfirmed until it is.

## Late season and endgame

- The season-close release shipped and measured: bank $150,728 → $152,974 vs the tape's $150,076,
  stranded units 62 → 16. `after_the_close_release_2026-08-15.md`, confirmed again the same week by
  `the_last_two_days_2026-08-17.md` (+$415 further, stranded gap closed 9/9).
- **Stranded d29 produce still exceeds the losing margin in real losses.** `the_stranded_load_is_the_loss_2026-08-15.md`
  measured this before the release above; `wasted_late_turns_2026-08-17.md` (2026-08-17, after the
  release shipped) still finds 11 units reachable-and-unharvested on d28-d29 in a real download, plus
  a separate hour-1-empty-hands defect losing ~300 unit-turns/season. **The release cut the problem;
  it did not close it.**
- Post-d19 production decay is thirst-killed strawberries and one-shot crops rotting past their
  window, not digging or discarding. `fable_production_decay_d19_2026-08-15.md`. Not contradicted.
- The DIG-then-nothing-replants defect near season end is still open and unfixed; the one tried fix
  cost -$2,898 and is reverted. `the_late_season_is_one_defect_in_two_halves_2026-08-12.md`. Nothing
  newer addresses this specific mechanism.

## Solver and routing

- Routes are precomputable offline because the board is identical every game.
  `the_route_is_precomputable_2026-08-12.md`. This premise underlies the whole
  `allocation_bounds_2026-08-16.md` / `allocation_bounds_pass2_2026-08-16.md` MILP line of work.
- **The leader's fixed MELON 20/STRAWBERRY 34 split is not near-optimal in any tested opponent
  scenario**, costing 1.78%-23%. No single fixed allocation is near-optimal across shop draws;
  melon oscillates toward a ~12-14 tile symmetric equilibrium under best-response iteration.
  `allocation_bounds_pass2_2026-08-16.md`, the most recent and most refined result in this line.
- `strawberry_watering_2026-08-16.md`'s `_trim_to_the_day` fix (+$1,165 mean over 12 seeds, weeds
  -34%) is the most recent shipped routing fix found. Its gate count moved the "wrong way" (356→359
  failed) but the doc argues, and nothing since contradicts, that this is a counting artifact rather
  than a regression.
- Pen-placement geometry is confirmed, a third time, not to be a lever. `geometry_of_the_herd_2026-08-09.md`.
- Q3 (the third land quadrant) lands on d11 in 19 of 19 real downloaded games vs opponents' d10,
  because cash arrives in a lump at d10 h23. `the_third_quadrant_arrives_a_day_late_2026-08-17.md`.
  This alone does not explain every loss (a same-lag opponent was still beaten by $5,275) — reported
  as a partial cause, not settled as a full explanation.

### An unnoticed regression, flagged and apparently not yet re-closed

`work_to_be_done_2026-08-16.md` records that the day-matching gate moved from 260/520 failing to
303/477 failing (43 cells regressed) with nobody having flagged it before that session. No later doc
in this set reports the gate count again. **Status of this regression as of 2026-08-25 is unknown from
the docs alone** — worth checking the live test output before trusting any day-matching claim dated
after 2026-08-16.

## Animals and the herd

The geese/goose verdict has been reversed or re-qualified at least four times across the docs read
for this index, most of them within a five-day window:

1. `HERD_GEESE` deleted (commit `c9c1c18`, referenced but not itself a `docs/` file) — geese lose to
   the mirror and to the field.
2. `the_goose_is_insurance_2026-08-15.md` reopens the question: geese lose on expectation but are
   the best insurance against a no-YARN_STORE draw (34.4% chance). Notes the original verdict was
   taken while EGG was unsellable (`SELLABLE` bug, fixed 2026-08-13) and so is void.
3. `fable_geese_audit_2026-08-15.md` (same day) audits the insurance case on the Elo margin
   objective and closes it again: margin-best in only 0.9% of shop draws, expected margin -$11,758
   per six animals.
2026-08-16, `marginal_units_and_the_shared_book_2026-08-16.md` calls the *original* c9c1c18 verdict
"garbage... measured IN A MIRROR" and says the goose question is "Void, not closed" — this reads as
consistent with step 2/3 above (attacking the pre-2026-08-15 verdict, not `fable_geese_audit`'s
margin-based one), but the file does not say so explicitly and I cannot confirm that from content
alone.

**Conservative read: geese are currently closed on the Elo-margin objective per `fable_geese_audit_2026-08-15.md`
(the most specific, most recent audit that directly targets the ranking objective), but the verdict
has reversed enough times that it should not be treated as durable without re-checking
`marginal_units_and_the_shared_book_2026-08-16.md` in full before relying on it.**

- Corrected flat-saturation points, current: 16 cows, 16 sheep, 8 geese.
  `what_saturates_and_what_does_not_2026-08-09.md`. Not contradicted since.
- The fourth-quadrant animal package (SE land + 4 sheep) wins games (11/11 vs 10/11) but the money
  delta is statistically indistinguishable from zero in the first measurement, because the branch
  never relocates any planting onto the new ground. `q4_variant_first_draft_2026-08-15.md`.
  **This branch shipped anyway** — see the flagged risk below.

## Carrot and late-crop experiments

No profitable carrot policy has been found as of the most recent file in this group.

- The best measured carrot-conversion policy, optimized by grid search on the single deepest-demand
  board on record, still nets a **loss** of -$2,086 (vs +$23,105 over doing nothing on that board).
  `the_optimal_carrot_2026-08-24.md`.
- The carrot corner that produced the headline $29,384 loss is rare in the field: 1 of 25 of that
  opponent's own games. `souta_25_games_2026-08-24.md`.
- The recommended abstention-gate response was implemented and measured to **lose** money on both
  towns where it fired (-$21,872, -$88) and was reverted the same day. `abstention_is_a_loss_2026-08-24.md`.
  This directly undercuts the abstention-rule recommendation made in `stealth_the_carrot_mechanism_2026-08-24.md`,
  filed earlier the same day — read the later file as the operative one.
- `carrot_drain_gaps_2026-08-24.md`: the drain 7-8 band is a coin flip with no clean direction, and
  drain 10 never occurs in a 2,364-file corpus scan. Drain 9 has no games with us seated at all.
- `carrot_swap_2026-08-12.md`'s CARROT_SWAP=False verdict (-7.8 to -10.4 win-rate points) still
  stands as the shipped state, but was measured before carrot could be sold at all
  (`stale_audit_2026-08-15.md` flags this and recommends deletion — see candidates for removal).
- `where_we_lose_2026-08-24.md` flags `CARROT_OPP_MAX=7` as possibly wrong-signed with **no
  measurement behind it at all**, contrasted with `CARROT_DRAIN_MIN=5`, which has 12,096 seasons of
  evidence. This is a live, unresolved risk, not a settled finding.

## Ladder targeting

- The rebase target is Dmitry Belan or Efe Can Celiksoy, not Seb. `the_ladder_is_two_scripts.md`.
  Nothing since 2026-08-15 revisits this recommendation directly.
- カワシギ is not open-loop past d3 (the first shop-unlock draw); response tracks the shop draw, not
  the opponent. `kawashigi_one_board_2026-08-13.md`. His decision-point-2 rule (four quadrants at
  d6, gated on YARN_STORE) is a real, measured +9.4% win, paired 19-1 — the most recent confirmed
  win in the ladder-postmortems group. `decision_points_2026-08-16.md`.

## Flagged risks in the two newest files (2026-08-25)

`where_99114898_went_2026-08-25.md` reports a real loss (-$26,277) with two named causes:

1. `q4_branch`'s land-latch fired on d11-d12. Its own docstring says plainly it was "shipped to be
   tried on the ladder, on Alex's call, not because it measured as a gain." This matches the
   inconclusive result in `q4_variant_first_draft_2026-08-15.md` above — the branch is live in
   production without a positive measurement behind it.
2. `WOOL_SHOP_SETS_THE_HERD` flooded a shallow wool book, collapsing price from $239 to $11 on a
   57-unit overshoot.

`the_shed_is_the_bottleneck_2026-08-25.md`, committed later the same day, proposes a mechanism for
cause 2: a jammed shed (ours sits at/near its 100-unit cap five times as often as opponents') forces
dumping instead of metered selling. It does not yet test this against the specific wool collapse in
`where_99114898_went_2026-08-25.md` — the connection is the later doc's own stated hypothesis, not a
confirmed shared cause.

Neither `q4_branch`'s land-latch nor the shed-cadence diagnosis has a follow-up fix documented
anywhere in `docs/` as of this index. All three are open as of 2026-08-25.

## Contradictions found that this file does not resolve

- **Geese**, above: four reversals in ten days, the last two (`fable_geese_audit_2026-08-15.md` vs
  `marginal_units_and_the_shared_book_2026-08-16.md`) not explicitly reconciled in text.
- **`stealth_the_carrot_mechanism_2026-08-24.md` vs `abstention_is_a_loss_2026-08-24.md`**: the
  first recommends an abstention rule, the second (same day) measures that exact class of rule as a
  loss. Filenames and content make the sequence clear (abstention was tried after being proposed),
  but both remain in `docs/` with no single file stating "the recommendation in the other file is
  withdrawn."
- **`REGISTER.md`'s "file deleted" claims** for `fable_the_discard_problem_2026-08-09.md`,
  `kawashigi_one_board_2026-08-13.md`, and `fable_where_next_2026-08-11.md` are contradicted by the
  filesystem — all three exist and are readable. Not a content contradiction, but worth knowing
  before trusting `REGISTER.md`'s account of what survived the 2026-08-11/-13 consolidations.
