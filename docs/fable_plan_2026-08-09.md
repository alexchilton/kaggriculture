# Plan for the next phase — 2026-08-09

Fable, 2026-08-08 evening.
Answers the six questions in the planning brief, ranked by expected value per unit of effort.
Everything cited is either in `docs/` (post-consolidation), in `CLAUDE.md`, or a measurement quoted in the brief itself.

## The one-paragraph verdict

The 26-game record says the opening is solved and the gap is money-at-equal-board: wins and losses have the same 97 tiles, the same herd, the same parcel days, and a $26k money difference.
The per-product audit says exactly where that money goes: we sell melon at the $1 floor on 462/719 turns, wool on 558/719, fertilizer on 684/719, while milk never leaves base and egg/carrot/tomato are never offered at all.
That is not a timing subtlety — it is a **product-mix and allocation defect**, priced against an economy (1.32.2) the ladder no longer runs.
So the actual win is **question 4** — feed the market model back into the schedule search so production matches absorption — with **question 6's shed and product fixes as the fast partial payments on the same defect**, and question 5 kept small as Q4's inner loop.
Questions 1 and 2 are worth a constrained slice each.
Question 3 I would not do, and I say why.

Two of the eight losses are within 4% and two more within ~11%.
A money-at-equal-board improvement of 5-10% — which the milk line alone nearly covers — plausibly flips 2-3 losses: 18/26 → 20-21/26.
That is the size of the prize, and it is all in the market half.

---

## Phase 0 — Re-baseline before believing anything (½-1 day). Not optional.

Every number driving this plan predates the current build.
The 26-game ladder record is the agent **before** `PRICE_AWARE_SELL_CAP` / `RESERVATION_SELL_CAP` landed, and the flood/starve audit (melon 462/719 at floor, etc.) was measured on our days 11-29 of that same era.
The two caps may already have bought part of the win.
Measuring first is the project's own first rule.

**0a. Confirm the shipped stack is on the 1.32.6 economy end to end.**
The ladder moved 2026-08-08 (memory: `project_kaggriculture_ladder_is_1326`).
Check, in order:
the installed `kaggle-environments` pin;
that `scripts/build_planner_submission.py` embeds a schedule extracted from a 1.32.6 game (`data/seed_scripts/v1326/`, or seb's `top_guys/90976060`) — the +35% swap measurement in the brief must be *shipped*, not just measured;
and the known real sim divergence: `kagg/sim/ops.py` still blocks movement onto LOCKED, which 1.32.6 allows (3 red tests in `test_sim_ops`, per `competition_brief.md`).
Fixing the LOCKED rule is also a free routing gain — `_step_towards` and `_mobile` in the live agent currently detour around ground they may cross.
Pytest first: un-xfail/fix the three `test_sim_ops` cases; add a routing test that a path across a locked tile is taken on 1.32.6.

**0b. Build the discriminating fixture, because none of our instruments can currently see a loss.**
The arena pool is saturated (94.4%, `the_shed_destroys_the_harvest` §5); the handover fixture wins 10/10 arms; the tape is uncontested.
The fixture that matches the ladder is: **our agent vs the extracted top-1.32.6 tapes replayed as opponents** — `healthstone_130k`, `rayk_130k`, `lester_125k`, `syed_125k`, `mohamed_107k`, `seb1326` (`data/seed_scripts/v1326/`).
The winners are open-loop (`the_field.md`), so a replayed tape is a faithful copy of what that seat does on the ladder, and the shared book makes the market genuinely contested even though their unit ops ignore us.
`scripts/vs_tapes.py` already exists and was never run (`fable_market_technique` "Open").
Run it both seatings, ≥8 seeds, and record **W/L per opponent** plus the money margins.
This is the selection instrument for every arm below.
Known limitation to write at the top of its output: a tape does not react, so absolute money runs high; the W/L and the margins are the signal.

**0c. Re-run the flood/starve audit on the current build.**
Same measurement as the brief's (per-product: turns at floor, units offered, realised $/unit, book min/max), on the 0b fixture.
Two specific checks with tests first:

- **A test that we never OFFER at the price floor** except under `LIQUIDATE_LAST_DAY`.
  Selling at $1 is revenue-free by construction ("Sales at $1 do not increase market supply", `reference/kaggriculture.py:626-635`) and 684/719 fertilizer floor-turns on the old build means the composition was inert there — the exact `max(rate, reservation)` trap that already nearly shipped once (`fable_market_technique`, "the trap this hit").
  If the current build still floors, that is a live bug and jumps the queue.
- Reconcile the **duplicate implementation**: `kagg/economics/market.py:reservation_price` (17/18 red on a `TypeError` at `market.py:224`) vs `schedule_agent.reservation_units`.
  One must go; the economics one has the better property tests, the schedule_agent one is what ships.
  This is an hour and removes a standing trap.

Deliverable of phase 0: a one-page table — per opponent W/L, per product offered/realised/floor-turns — that every later arm is judged against.

---

## Phase 1 — Quick wins (question 6), 2-3 days total, each independently shippable

These are all the same defect wearing different products: **the shed and the sell block allocate by leftover schedule rows, not by value.**
Ranked by confidence × size.

**1.1 Shed slot allocation by value density (the one the brief smelled — I agree).**
Wheat holds 41-45 of 100 slots at base $25 while milk sits at 0-9 at base $160, and the shed is the *only* sell buffer (`SELL` sees only the shed).
A shed slot's value is `price × depth-of-book`, and wheat is the deepest book in the game (2,421 units to 0.75·base) — wheat is the product that least needs a buffer.
Fix at the two places that decide what occupies the shed:
`SELL_TO_MAKE_ROOM` / the `room_needed` block (`schedule_agent.py:~2285`) should evict in ascending value order — sell wheat above the herd-feed floor first, never milk/wool;
and the sell block should treat shed-resident high-base product as always offerable up to its reservation size.
Hard constraint: never release wheat below the feed reserve (19/day herd floor; `consecutive_unfed >= 2` kills the animal — correctness floors are not traded).
Tests first: (a) eviction order is value-ascending, (b) feed reserve survives eviction, (c) fixture-level: milk shed occupancy > 9 slots on days 15-25, destroyed ≤ 82.
Measure on 0b: milk realised units (was 16 all season into a book that touched $315 — the single largest number on the table) and W/L.
Effort: 1 day. Confidence: high.

**1.2 The milk probe, before the milk fix.**
"16 units of milk sold" has two candidate causes: the sell rule never releases it, or the router never lands it in the shed same-day (OPEN-1's dusk-sweep symptom, and the shed row 0-9 points here).
One script — shed milk by hour, per day — says which.
If it is supply, the cure is **narrow**: a planned shed stop after the milking pass for the milk-carrying unit only, via `cover.materialise` (a shed trip is already a first-class stop).
Do NOT rebuild `DELIVER_SURPLUS_NOT_THE_ROW` (-$15,272/12 seeds) or `STAND_AT_A_DRY_SHED` (cost 3 cows) — both numbers are posted in `architecture.md` and must be beaten, not ignored.
Effort: ½ day probe, then bounded. Confidence in the probe: certain; in the cure: medium.

**1.3 Fertilizer is a race and we start four days late.**
Zero town drain, so the book only ratchets down; first 200 units worth $16,020 vs the last 200's $8,020; the tape's largest early line (322 units/season, first move d2, ours d6).
Fix: front-load fertilizer sells from day 0-1 — it is already collected (`COLLECT_FERTILIZER` runs at 100%), this is a sell-priority change, not a routing change.
Combined with 0c's no-floor test, fertilizer becomes "sell early, then stop forever" instead of "flood at $1 for 684 turns".
Measure: realised $/unit (target ≥ the tape's), first-sale day ≤ 2.
Effort: ½ day. Confidence: high.

**1.4 Melon ≤ its 1.32.6 absorption.**
Season absorption on 1.32.6 is ~30 units (no shop stocks melon; centre only).
If the reservation rule computes `D_rem` from the live env spec, this should already bind post-fix — 0c tells us.
If it does not, cap it; and hand "we were planting for 96+ melon sales" to phase 2, because the surplus melon *tiles* are the real waste.
Effort: free-to-½ day.

Ship gate for phase 1: each item must not regress the 0b W/L table, judged per target day per the SELECTION RULE in `REGISTER.md`.
These are 1-2 submissions' worth of ladder tests, run early in the day so ratings have hours to climb.

---

## Phase 2 — The actual win: market-aware schedule search (question 4), 4-6 days

**The claim.** Phase 1 makes selling honest given what we produce; phase 2 fixes *what we produce*.
The schedule search (`kagg/search/plan.py`, `scheduler.py`) prices production with `revenue_rate`/`payback_days` off base-ish prices, so it optimises production and discovers the price collapse afterwards.
The evidence this is the binding defect:
top 1.32.6 plans sell 305-649 wheat against wheat's 525-unit absorption — they are selling the town's wheat budget — while we sell 71;
we plant 77 tiles to the tape's 45 and destroy the difference or floor it;
and OPEN-3's `buy_product -164` is very likely the winners' core play (buy wheat → feed → milk/wool, ~83% of the $113k winner's revenue, `the_field.md`) that our schedule never expresses.

**The objective function** — this is the part to get right, everything else is machinery:

- Inner (dense, for the search): final bank in the parity-tested sim, **with the marginal-revenue market model, not base prices**.
  Value of the k-th unit of product p = `market_price(p, I_baseline(t) + k)` integrated against the deterministic 1.32.6 drain — i.e. the `N(L)` machinery from `fable_market_technique` Q1, already derived and unit-tested.
  This single change makes "the 96th melon" worth ~$1 to the optimiser instead of ~$250, which is the whole point.
  `I_baseline(t)` includes a frozen opponent's sells (a fixed top-tape's recorded market orders), because a solo book overstates every price — the `starter`-alone lesson in market form.
- Outer (selection): **win rate on the 0b tape-pool fixture, train seeds ∩ held-out seeds disjoint**, money margin as tiebreak only.
  Money alone is proven anti-correlated in exactly this domain (Seb's 1.32.6 sell mix: more money on every seed, 0/8 head-to-head — `brief_market_selling` trap 1).

**Search setup (this is question 5, kept deliberately small):**

- Space: the per-day schedule genome that already exists (`plan.py` `Plan`/`decode`/`probs_around`, `kagg/search/script_mutate.py`, `scripts/optimise_script.py`).
  Drop the sell rows from the genome entirely — selling is now the reservation rule's job at runtime — which shrinks the space, exactly the `optimise_the_artifact` direction.
  Add/verify genes for `BUY_PRODUCT WHEAT` (the feed-import play); if the genome cannot express it, that is the first edit, with a test.
- Seeds: mutate-and-accept from three starts — our current schedule, the seb1326 mix, and a mined wheat-heavy mix (see Q1 below).
  No CMA over everything; the documented winner's-curse protocol instead: propose on 8 train seeds, **accept only if ≥ +1σ on 8 held-out seeds, then confirm the accepted winner on a fresh draw** before it is called real (the +40%-vs-+12.8% lesson, verbatim from `CLAUDE.md`).
- Budget: hundreds of evaluations, not millions — the sim does full seasons fast and the space after removing sell rows is small.
  Weeds off for search, weed-seeds on for the confirm step.

**Deliverable:** a new `best_plan.json` + rebuilt submission that beats the current build on the 0b fixture win rate, both seatings, held-out seeds.
Tests first: the marginal-revenue valuation gets its own pytest (known-book cases, melon-vs-wheat ordering flips at the measured depths) before it is wired into the search.

**Why this ranks first:** it is the only item pointed at the measured gap (money at equal board), it consumes the market model we already built instead of leaving it as a runtime patch, and every phase-1 item makes its search landscape more honest.

---

## Phase 3 — Reactivity (question 2), 1 day, after phase 2

Most of the exploitable reactivity **already ships**: `market_price` is a pure function of `I_now`, and the reservation rule re-reads `I_now` every turn, so when the opponent dumps 20 wool the wool reservation tightens the same turn without any new code.
The one genuinely missing read is the strongest item in my Q3 list: the opponent's net trade is exactly inferable per product per turn —
`opp_net(p,t) = Δinventory − our_sales + drain(p,t)` —
which turns the `contest` dial (their claim on the remaining town drain) from an assumed 0.5 into a per-product measurement, and their visible board (sheep count → wool coming, cows → milk coming) bounds their future supply.
Implementation is ~40 lines in the sell block reading fields already in `obs`; test with a scripted opponent whose dumps are known.
Timescale answer for the brief: the read is per-turn, but the *action* it changes is on the day scale — sell ahead of their inferred glut, hold into their inferred scarcity.
Do it after phase 2 because its value is a second-order correction to a first-order mix fix, and measure it on the 0b fixture like everything else.
Expected size: small; several losses are 3-4%, so small is still worth one day.

---

## What I would NOT do, and why

**Question 3 — anti-mirror exploits: no.**
Three reasons, each sufficient.
(1) A mirror game contributes ~50% expected score whatever we do, and Elo rewards beating the *field*; the project has already burned itself twice tuning toward mirrors ("a mirror match is not a best response", melon 25→12→25).
(2) Any "sell one turn earlier than my own schedule" exploit changes the schedule, which changes what the mirror does next submission — an arms race against ourselves with no fixed point, exactly the confounded moving-opponent failure `CLAUDE.md` documents ("freeze the opponents").
(3) The profitable part is already covered for free: in a mirror both seats flood the same shallow books simultaneously; phase 1's no-floor rule and depth caps make our seat stop first, which *is* the best response, without any opponent-modelling.

**Question 1 as policy extraction / behavioural cloning: no.**
The label does not exist — the winners are open-loop scripts, so `SELL WHEAT 28` is a constant fitted to somebody else's board, and there is no counterfactual in a replay (already argued to death in `fable_market_technique` Q2a; cloning it is `feedback_optimise_the_artifact` by construction).
**Question 1 as calibration mining: yes, one constrained day, inside phase 2.**
Two extractions from the ~48 replays in `~/Downloads/9*.json` (checking `configuration.townCenterSellInterval` on every file first — mixed versions poison the set):
(a) the winners' *production mixes and buy_product volumes* on 1.32.6, to seed phase 2's search starts;
(b) a validation table for the analytical model — realised $/unit vs book state at their sell moments; if the winners' realised prices systematically beat what `N(L)` predicts is available, the model is missing a mechanism and phase 2 would inherit the error.
Regress nothing; tabulate.

**Question 5 as a standalone evolutionary program: no.**
An ES needs a discriminating, cheap, honest objective; before phase 0b exists there is none (pool saturated, fixture wins 10/10, money anti-correlated), so a big search would optimise a proxy known to point the wrong way at a resolution ~15% seed noise cannot support.
After 0b it is phase 2's inner loop, sized in the hundreds of evaluations with the held-out accept gate.
The machinery already in the repo (`optimise_script.py`, `script_mutate.py`) is enough; building a population framework is busywork.

**Rebuilding either OFF flag** (`DELIVER_SURPLUS_NOT_THE_ROW`, `STAND_AT_A_DRY_SHED`) without beating the posted numbers. They are posted for that reason.

---

## Ranking, effort, and the measurement that proves each

| rank | item | effort | expected value | proof measurement |
|---|---|---|---|---|
| 1 | Phase 0: 1.32.6 alignment + tape-pool fixture + re-audit | ½-1 d | prerequisite for everything; possibly finds an inert-cap bug outright | 0b W/L table; no-floor test red/green |
| 2 | 1.1 shed slots by value (+1.2 milk probe) | 1½ d | high — milk is the largest single number on the board | milk realised units 16 → 50+, W/L on 0b |
| 3 | 1.3 fertilizer race + 1.4 melon cap | 1 d | medium, high confidence | fert first-sale ≤ d2, realised $/unit; melon offered ≤ absorption |
| 4 | Phase 2: market-aware schedule search | 4-6 d | **the win** — targets the measured $26k gap directly | held-out win rate vs tape pool, both seatings, fresh-draw confirm |
| 5 | Q1 mining (mix seeds + model validation only) | 1 d | medium, de-risks phase 2 | winners' realised price vs model prediction |
| 6 | Phase 3: measured `contest` / opponent net-trade | 1 d | small but cheap; two losses are <4% | scripted-dump test; 0b margins |
| — | Q3 anti-mirror | 0 | negative (arms race, mirror ≈ 50% regardless) | — |
| — | Q5 as standalone ES | 0 | negative until 0b exists; then subsumed | — |

## Ladder protocol for the whole phase

- Local gate before any submission: `scripts/vs_tapes.py` both seatings ≥8 held-out seeds, plus `breakdown.py` at the target day, plus the herd floor (animals-in-pens per day — a correctness floor, never traded).
- Spend at most 2 of the 5 daily slots on ladder tests, submitted early; ratings start at 600 and climb for hours, so never read a fresh submission against an aged one.
- Every theory above gets its failing pytest before its code change; after each fix, revert it once and confirm the test goes red.

## The two risks I would keep pinned above the desk

1. **The tape-pool fixture inherits the open-loop caveat**: tapes do not react, so money runs 2-3x real and a strategy that only works against non-reactors could sneak through.
   Mitigation: the pool's members are the actual ladder's top seats, W/L not money is the criterion, and the real ladder record after each submission is the final judge.
2. **Phase 2's valuation could be confidently wrong** in a way the search will exploit ruthlessly (optimisers find model errors before they find wins).
   Mitigation: Q1's validation table before the search runs long, and the fresh-draw confirm step on every accepted winner.
