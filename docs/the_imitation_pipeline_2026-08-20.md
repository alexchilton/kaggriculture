# BC -> DAgger -> RL: what is built, what is measured, what could still fail

Written 2026-08-20, after `docs/the_tape_dies_at_d13_2026-08-20.md` closed out the tape-clone track.

## Why this exists

The `(day, hour, unit)` tape reproduces kawashigi exactly to d12 and then rots: crops 53 -> 1, weeds
0 -> 48, bank flat from d19. That is a property of an open-loop sequence, not of the player.
A network keyed on the BOARD does not inherit it -- it does not care that it is standing on the
wrong tile, it looks at the tile it is actually on.

Alex's contribution that unblocked this: **use the shipped 2500 agent as the teacher.**
`kagg/il/bc.py` had parked DAgger for a stated reason -- "its only teacher that ever emits FEED is
`jax_rancher` at $12,078", which also burns 37-52% of its actions on a PICKUP thrash it would teach
along with the good behaviour.
A $90k-class queryable teacher retires that objection.
This is the "a decision to skip a fix can expire when the problem changes" lesson, landing on its
own example.

## The order

One network throughout, 726,647 parameters. Three data regimes, not three models.

1. **Round 0, beta = 1. This IS the BC stage.** Teacher self-play; teacher executes and labels.
2. **Rounds 1..N, beta annealed to 0. This is DAgger.** Student executes, teacher only labels, so
   every label lands on a state the student really produced.
3. **RL.** Terminal reward, win 1 / loss 0, gamma 1.0, frozen pool. The only leg that can exceed the
   teacher.

`scripts/bc_dagger.py` already frames beta exactly this way, so BC is not a separate stage to build.

**How long to run DAgger is a measurement, not a round count.** Stop when the student/teacher
disagreement *on the student's own states* plateaus -- that quantity IS covariate shift. Typically
5-8 rounds, which is where the existing `--rounds 8` default comes from. DAgger cannot exceed the
teacher, so "student matches teacher on the student's states" is the exit to RL.

## The box

    /home/alex/kagg-teacher     fresh git clone, commit ead81e2
    submission/main.py          sha256 b2e6808e38daaa76bc72949af40f69266435d8092c37a4716c9e13e82d9aaef7
    .venv                       kaggle-environments 1.32.7, CPU jax -- labelling
    .venv-cuda                  jax-cuda12-plugin + CUDA 12.9 -- training
    16 cores, 13 GB RAM, 733 GB free

**The leaderboard artifact is `ead81e2`, not `cfd6f53`.** Alex named `cfd6f53`, which changed
`kagg/search/cover.py` but did NOT rebuild the bundle; the next commit did.
`cfd6f53:submission/main.py` still reads `UNSOLVE_DAYS = (29,)` against `ead81e2`'s
`tuple(range(24, 30))`.
Building a teacher from the named commit would have quietly used an agent without the fix that
defines it.
Check what the bundle contains, not what the commit message says.

Two stale non-git copies exist on the box and were left alone: `~/kaggriculture` (17 G, Aug 15) and
`~/kagg` (12 G, Aug 9).

**Teacher smoke test:** 720 steps, both seats DONE, banks $142,002 / $147,440, **29.4s per mirror
season, 0.04s per turn.** The 3.99s dawn-solve figure in `main.py` profiles the SOLVER; the shipped
agent replays `PRECOMPUTED_ROUTES` and only solves `UNSOLVE_DAYS`. Labelling is cheap.

Under 16-way contention it is 53-90s per game, not 30s. 640 games ~ 50 minutes, ~10 GB.

## The teacher is sound in the late game

The check that mattered before teaching anything to a network: would DAgger clone a defect?
Mean over 120 game-seats, sampled at hour 12:

    day    our planner            kawashigi (holdout 94439800)   tape clone
    d13    crop 59.0  weed 1.0
    d18    crop 57.5  weed 2.4    crop 51  weed  1               crop 18  weed 34
    d29    crop 16.0  weed 3.6    crop  3  weed 17               crop  1  weed 48

**Our planner holds more crops than kawa at d18 and fewer weeds at d29. It never weeds over.**

And the second reading of that table matters more: **our planner farms better than kawa and earns
less.** It banks $87,149 mean -- from MIRROR self-play, which this project has repeatedly measured
as roughly 2x inflated on an uncontested book -- against kawa's $86k-$153k on a contested one.
The deficit is in the economy, not in routing, watering or crop management.
That is exactly where the bundle head goes.

## The market is one token: sized on OUR teacher

5,752 player-turns from the pilot shards:

    non-empty market   1,225 (21.3%)
    distinct bundles   117            (tetsuya was 346)

    top  20 bundles cover  93.45%
    top  50 bundles cover  97.39%
    top 100 bundles cover  99.70%
    top 200 bundles cover 100.00%

A **128-class head is the whole distribution** for ~16k parameters on the global token, replacing
six heads whose joint decode is measured to emit nothing.

The bundle that has been costing money is rank 2:

    rank 2   113 turns   HIRE x10
    rank 7    59 turns   BUY_PRODUCT WHEAT, BUY_SEED WHEAT, HIRE, HIRE
    rank 9    49 turns   SELL FERTILIZER, SELL MILK, SELL STRAWBERRY, SELL WHEAT, SELL WOOL

Ten hires in one turn as ONE symbol. That is the d10 failure -- units 8 and 9 never hired, 20
planned ops dying with them -- becoming unrepresentable-as-broken rather than merely unlikely.

**Quantities need their own head, confirmed:** 52 of 116 non-empty bundles carry more than one
quantity vector; the five-way sell carries 48. Wrong quantity is graceful, wrong bundle is fatal.

Built: `kagg/il/market_bundles.py`, `tests/test_a_market_bundle_survives_the_round_trip.py`
(red 1 error -> green 6 passed).

## How we see whether it is learning

No offline number counts. Both have already lied here: 86.2% per-decision accuracy on teacher states
scored 79.3% error on its own trajectory, and six well-fit marginals compose into an agent that never
trades.

Three checks, cheapest first, after BC and after every DAgger round:

1. **Argmax distribution on one batch (seconds).** The parked BC track's signature was
   `P(move) = 6e-5 per unit-turn` -- across 13 units and 30 days you would expect ONE unit to ever
   leave the shed. Dead argmax means the loss or the label alignment is wrong.
2. **One replay (a minute).** Non-empty market rate against the teacher's **21.3%**, and FEED count.
   `FEED 0/85` was the tell that the board-keyed clone was dead while its totals looked fine.
   Zero market orders is the $3,000-bank failure.
3. **The board grid (five minutes).** Crops, weeds, bank per day against the teacher on PINNED
   seeds. Weeds at d18 is the most sensitive number we have.

They fail at different layers, and the cheap ones say which.

`kagg/il/bc.py` already carries three hard-won loss fixes: illegal labels hitting `NEG_INF = -1e9`
and producing a 5.3e7 loss that would not move; padding slots making ~85% of the objective constant;
conditioned heads scored under every trade mode rather than only mode 0.

**There is no KL anchor.** `bc_dagger.py` says so outright. It does not matter for stages 1-2; it
matters a lot for stage 3, where PPO can walk off the imitation prior in the first few updates.
`train_jax_rl.py` has `--kl-anneal`; it is simply not wired into this path.

## Reasons this might not work

1. **DAgger caps at the teacher.** Best case at the end of stage 2 is our own 2500 agent, in
   milliseconds instead of seconds. All the gain is in stage 3. If RL does not deliver, the chain
   returns a fast copy of the status quo. This is the real risk.
2. ~~Cloning a late-game defect~~ -- **CLOSED**, measured above. The teacher is clean.
3. **Bundle legality, not just identity.** The head fixes which orders go together; it does not know
   `SELL WHEAT` is illegal with an empty shed. Needs a legality mask over 128 bundles per state.
   Wrong masking gives silently rejected orders -- the same symptom as a broken decode, different
   cause.
4. **The encoder bridge.** Labels are Kaggle observations; `jax_obs.encode` wants a sim state, and
   `adapter.state_from_obs` bridges them. `adapter.py` itself warns a second encoder "is a thing
   that must agree forever and will not."
5. **Terminal reward is one bit per 720 turns.** Right call, and genuinely hard.
6. **Bundling for submission.** A hand-rolled bundle once banked exactly its $3,000 start here.
   `build_submission.py` is the guard.
7. **Seed variance is ~2x** on this teacher against ITSELF -- $59k to $114k across four seeds. Every
   A/B needs pinned seeds.

## Caveats on the numbers above

- All teacher figures are mirror self-play. The market is uncontested, so banks are inflated and the
  crop/weed curves are the trustworthy part.
- The kawashigi comparison column is ONE holdout game against 120 of ours.
- The bundle vocabulary is from 4 pilot games. It should be rebuilt on the full round-0 set before
  the head is sized finally -- 117 is a floor, not a ceiling.
