# Handoff: the static-line/draw hypothesis, mid-test

Date: 2026-08-24 evening. Written by the reviewer for the next session of the reviewer.
Reads first: `docs/handoff_for_review_2026-08-24.md`, then `docs/answers_for_review_2026-08-24.md`.
This file continues both and assumes them.

---

## Where this stands

A live hypothesis came out of the second review conversation and is **half-tested**: the measurement
script exists and has never been run.

**The hypothesis.** Shop awareness lives entirely in `schedule_agent`'s dawn planner and is
hand-built per product line. `cover.py` contains zero references to `unlocked_shops` -- the tour
solver is shop-blind end to end. The adaptive lines are WOOL (`_herd_split`'s undrawn-deck logic,
`schedule_agent.py:2961-2995`), MILK (`MILK_DRAINING_SHOPS` headroom, `:3063/:3082`), STRAWBERRY
(`STRAWBERRY_SHOPS`, `:1691`), TOMATO (`:4288`) and CARROT (`CARROT_DRAIN_MIN`). EGG has nothing,
and the WHEAT/FERTILIZER sell paths never read `unlocked_shops` at all.

**Prediction.** Our realised outcome on an ADAPTIVE line should be insensitive to how kindly the
town drew, because the planner re-plans around the draw. On a NON-adaptive line our outcome should
move with the draw, because nothing between the plan and the market reacts to it. Supporting
circumstantial evidence, both already documented elsewhere: EGG and TOMATO scored 0% realised price
in the 100-game audit (`answers_for_review` §1) -- the two products with no adaptive handling are
the two we do not sell at all; and the precomputed-day gap (`cover.cover` returns early on d12-14,
`work_to_be_done_2026-08-16.md`) sits exactly where even the adaptive half runs narrowest.

**Counter-evidence to respect.** The in-game dynamic re-solve was tried and measured slightly
WORSE than off (`the_route_is_precomputable_2026-08-12.md`, 0.25s budget). Whatever comes out of
this, "re-solve more days" is not the remedy. The remedy shape already agreed, if the hypothesis
survives: extend the existing pattern (`town_drain_remaining` is a function; wiring it into the
wheat sell cap is the same move as `PRICE_AWARE_SELL_CAP`, keyed on the draw instead of the price),
plus optionally a dawn predicate gate -- precomputed day executes unchanged if its shop-backed
stops are actually unlocked, else that day falls to the planner path.

## The immediate task: run the script

    python -u scripts/does_the_draw_move_our_market_share.py \
        --dirs downloads_2026-08-20,field_leaders --limit 100

Written this session, **never executed**. It computes, per product, our revenue share
(our rev / all rev, fills from inventory deltas, not offers) across games, and Pearson r between
that share and two draw features: instances of shops buying the product, and the step of the first
unlock of any such shop. Data dirs confirmed present: `data/seed_scripts/downloads_2026-08-20`
(600 files), `field_leaders` (129). Other usable dirs: `ours_ladder_new`, `leaders_2026-08-19`,
`top2`. Corpus caveat as always: these folders skew toward our games and losses -- fine for
correlation structure, not for win rates.

**Reading the output, decided in advance so nobody improvises:**

- r near 0 on the adaptive lines AND |r| clearly above ~0.3 on EGG (or wheat, if it ever becomes
  measurable -- it cannot, it has a second sink) => static-line defect confirmed. Next action is
  the per-product deficit table, then the sell-cap wiring.
- |r| < ~0.2 everywhere => the draw does not reach realised market outcomes through this channel.
  The theory dies here and cheaply. Do not rescue it with sub-splits; write the number down.
- Mixed (one non-adaptive line moves, another doesn't) => plausible but weakens the "hand-built per
  product" story toward something product-specific; investigate only the line that moved.

EGG may be unmeasurable too -- we sold zero units in the 100-game audit, so its share column will
be empty or degenerate. If EGG produces no variance, the honest statement is: the theory is
untestable on the corpus as it stands, and the cheapest probe becomes an intervention (an arm that
sells EGG when BAKERY/BRUNCH_SPOT are drawn) rather than an observation.

## The queue behind it, in the order already argued

1. **Per-product deficit table** from `what_we_actually_get_paid.py`'s fills, grouped by product
   and game -- decides which lines lose money and feeds the gate design.
2. **EGG/TOMATO economics under the post-1.32.7 hinge curve.** Every prior tomato/geese verdict
   predates the balance change and describes a different game. tetsuya runs 12 geese while the
   players either side of him run none -- current contrary evidence to the old kill.
3. **The combination submission** (carrot gate + shop-price fix, commit `4649af9` on
   `e2500-carrot`, never bundled). WITHOUT `LAST_DAY_SELL_TURNS` or with it measured first -- it
   has never been tested on a branch where the planner runs (see `answers_for_review` §3).
4. **Ratio-vs-margin split** on the same 100 games: per-game realised-price ratio against game
   margin, to finish whether episodic flooding predicts losses. This also decides the priority of
   FEED/CARE live pricing (`router.py:1425,1497`).
5. Then, only if 4 says floods predict losses: `crop_ops` HARVEST live pricing, CRITICAL collision
   instrumentation, the rest of the §4 list in the answers file.

## Things settled in this conversation, so they are not re-derived

- **Tape re-pointing is structurally untestable, not merely expensive.** A recorded action stream
  is valid only on the board trajectory that produced it; teachers diverge from each other by d1;
  swapping one teacher's d4-d11 onto another's opening is the ROLE_TAPE chimera again
  (`fable_verdict_on_role_tape_2026-08-23.md`, section c). Full-tape bank comparisons across
  players are confounded by field. And the value of perfect cloning is bounded by the measured
  fact that playing Kawashigi's whole recorded season finishes only +$240 over our planner
  (`the_tape_beats_our_planner_2026-08-21.md`). Both "improve the teacher" routes -- net cloning
  and tape re-pointing -- are closed on measurement-theory grounds.
- **Market flooding split into two claims.** Average realised prices are at parity
  (`answers_for_review` §1, 96/111/158/94%). Episodic flooding in individual losing games is still
  open and is exactly queue item 4. The old "$1 milk for a whole season" finding is a harness
  artifact per `the_tape_and_planner.md`'s correction; do not quote it as a ladder fact.
- **Exact tape clones fail on animal harvest cadence**, not just buying: FEED depends on winning
  wheat off a shared contested book, a missed FEED shifts the pen's yield calendar, and every
  later recorded HARVEST fires against an empty pen. This is why our clone beats exact clones.
- **The ladder is deflating league-wide**: the identical 2472.7 artifact re-uploaded reads
  1688.7. Cross-day arm scores are unreadable until convergence; gate locally, treat the ladder as
  slow confirmation. A fresh leaderboard pull against `data/leaderboard_2026-08-21.json` would put
  a number on the drift rate and has not been done.
- `LAST_DAY_SELL_TURNS = 4` sits uncommitted-reverted and **unmeasured**, because its null was
  read off a `range(30)` branch where the planner never runs. Same audit before believing any
  byte-identical result: check `REPLAY_OPENING_DAYS` on the branch actually measured.

---

## RESULT (2026-08-24, later): the script ran. The theory is closed.

The two dirs named above are wrong for this measurement and contain zero games with our seat:
`downloads_2026-08-20` is leader-vs-leader episodes, and `field_leaders` is seed-script tape format
(`team/episode/seat_in_recording/actions`), not episode JSONs. Our ladder name is `alex chilton`.
The corpus actually used: every dir under `data/seed_scripts/` whose episode JSONs carry our seat
(`ladder`, `ladder_1943`, `ladder_2026-08-16/17/17b`, `losses*`, `our_games`, `ours_1326`,
`ours_ladder_new`, `ours_weeds`, `top_guys`) -- **220 games**. One script fix on first run:
`audit()` now skips non-dict JSON (some dirs hold top-level lists).

    product      handles draw?   our share      r vs count   r vs first unlock
    MILK         yes            53% ±11        -0.02        -0.05
    WOOL         yes            54% ±15        +0.13        -0.09
    STRAWBERRY   yes            56% ±16        -0.05        -0.05
    CARROT       yes            65% ±43 (137g) -0.09        +0.12
    EGG          NO             0% ±0 (12g)    nan          nan
    TOMATO       gate (yes)     8% ±27 (13g)   +0.04        -0.21
    MELON        control        49% ±14        nan          nan

Reading, per the pre-decided rules: the adaptive half of the prediction is confirmed -- |r| <= 0.13
everywhere we contest. But the discriminating cell is EMPTY: the two non-adaptive lines are EGG and
TOMATO, and we sell almost none of either, so there is no variance for a draw to correlate with.
The honest statement is the one pre-written above: **untestable by observation on this corpus**,
because the static lines are exactly the products absent from our book. Not rescued with sub-splits.

Two corrections to how this thread should be weighted, from Alex:

- **Milk share ~53% is not a weak number.** Both seats write into one inventory, so our selling
crashes THEIR realised price too (`economics_q5_findings.md` §6). Share, not $/unit, is the metric
in a contested market; denial value does not show up in our own price column.
- **Geese are not reopened by this table.** Three closures already stand (`fable_geese_audit_2026-08-15`
margin arithmetic, closed-by-absence over 4,022 replay seats, plus the void-but-superseded sweep).
The only live residue is that the margin arithmetic predates the 2026-08-15 EGG hinge change;
re-running it against post-1.32.7 prices is an afternoon of reference arithmetic, not a submission.

Status of the static-line/draw thread: **CLOSED as untestable-by-observation.** An intervention arm
(sell EGG when BAKERY/BRUNCH_SPOT are drawn) remains the only way to test it, and only becomes
interesting if selling EGG at all is first justified on economics.
