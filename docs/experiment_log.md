# Experiment log

Append-only record of what was tried, what it scored, and what it taught.
Newest last.
Scores are **mean final bank, seat-swapped, on held-out seeds never used for tuning**, against
the built-in `starter` baseline unless stated otherwise.

The point of this file is that several things in this project were "discovered" twice because a
measurement was made and then not written down.
If you measure something, put it here.

## Scoreboard

| # | What | Score | vs baseline |
|---|---|---|---|
| 0 | `starter` built-in baseline | $3,512 | 1.0x |
| 1 | Heuristic v1 — wheat only, timid hiring | $8,641 | 2.5x |
| 2 | v2 — fixed hiring and land timing | $11,296 | 3.2x |
| 3 | v3 — ES-tuned parameters | $13,486 | 3.8x |
| 4 | v4 — melon quadrant + wheat (**submitted, scored 429.9, lost**) | $43,540 | 12.4x |
| 5 | **v5 — opponent-pool tuned, price-aware** | **72% win vs pool** | see below |

From v5 on, the headline number is **win rate against a fixed opponent pool**, not money, because
the leaderboard is Elo and margin does not count.

Kill criterion in `CLAUDE.md` was $20k. **Cleared at v4**, so the economics model is vindicated
rather than falsified.

## 1. Wheat-only heuristic — $8,641

Many hands, staggered plantings, continuous selling, wheat everywhere.
Chosen because wheat measured 28 units/tile/season against strawberry's 6, and wheat's market is
nearly glut-proof (`above_func=log`): 2,800 units still clears about $19/unit.

**Diagnosis of the gap:** measurement, not guesswork. A per-day dump showed 15-18 tiles idle all
season and money down to $1,400 by day 4.
The first version of that dump reported `hands: 0` for the whole game, which was a *measurement
artifact* — hands are cleared nightly, so sampling at hour 0 always shows none.

## 2. Fixed hiring and land timing — $11,296

Two fixes:

- Land was bought on day 1, starving seed purchases. Now gated on 80% of owned tiles being
  planted **and** a cash multiple of the land price.
- Hiring formula was too timid. Raised, and split across two turns so the 10-order-per-turn cap
  stops eating the sell orders.

## 3. Evolutionary parameter search — $13,486

`scripts/tune_heuristic.py`, a (1+lambda) hill-climbing ES over seven parameters.
Chosen over RL for the parameter layer because the objective is a single scalar at the end of a
720-step episode, so the long delay between planting and payout never becomes a credit-assignment
problem, and it parallelises across CPU cores rather than needing the GPU.

**It refuted a doc claim the agent had inherited.**
`economics_analysis.md` said aggressive hiring is "close to free money".
The cost is Fibonacci *and resets every morning*, so it is paid 30 times: eight hands is $54/day
(~$1.6k a season), fourteen is $986/day (~$29.6k a season, more than the extra labour earns).
Search moved hiring **down** from 17 hands to 8.

**Two methodological failures, both worth remembering:**

1. **Seed overfitting.** With three fixed tuning seeds the search reported **+40%**. Held-out
   seeds said **+12.8%**. The baseline's tuning-vs-held-out gap was 8%; the tuned config's was
   35% — that gap *is* the overfitting signature. Fixed by resampling seeds every generation and
   re-scoring the incumbent on the same fresh seeds.
2. **Winner's curse.** After that fix the search still "moved" 11 times in 14 generations for
   +1.6% total. Taking the best of ten noisy estimates against an incumbent scored once biases
   every comparison upward. Fixed by re-evaluating the winner on a fresh draw before accepting.

**Seed variance is large:** identical parameters score $11.5k on one eight-seed set and $13.3k on
another. Small parameter differences are not resolvable at this sample size. Quote held-out
numbers with the seed range, always.

**Conclusion: the parameter layer is exhausted.** ES tunes numbers; it cannot invent structure.

## 4. Melon quadrant — $43,540

The economics model's central prediction, cashed in. Melon is the only product **no shop demands**
so its price is set purely by town-centre drain, which is identical on every seed. Measured
~$2.9k revenue per tile against wheat's ~$650.

Swept tile count on held-out seeds:

| melon tiles | 0 | 6 | 12 | 18 | 25 | 40 | 60 |
|---|---|---|---|---|---|---|---|
| mean bank | 13,218 | 26,656 | 39,085 | 39,087 | **43,602** | 39,572 | 37,912 |

Peak at **25 tiles — a full quadrant** — matching the offline model's estimate for the same
commitment. Beyond that, melon's shallow market (about 113 units at half base, against a season
drain of only 140) starts costing more than the extra tiles earn.

This is the strongest evidence so far that the offline economics work was worth doing: the model
predicted the best crop and the size of the commitment, and the agent confirmed both.

## What has NOT been tried

Ranked by expected value from the economics measurements:

- **Animals.** The only uncapped producer — no lifetime cap, unlike plants. A goose yields 26 eggs
  a season against a `max_held` of 4. They also emit free fertilizer daily.
- **Fertilizer.** Doubles ongoing-crop output (tomato 8→16, strawberry 6→12) and lifts wheat
  28→42. Buying it at $100 does not pay; collecting it free from animals does. This is the
  wheat → animals → fertilizer → premium-crop loop, and nothing in the agent touches it.
- **Deferred selling.** Worth a measured 1.14-1.26x. The agent sells continuously.
- **Market denial.** Dumping a good just before the opponent harvests it. Scoped out of v1.

## The field, measured on day 1 (2026-07-31)

From the live leaderboard and the official episodes index (`data/manifest.csv`):

| Metric | Value |
|---|---|
| Top team rating | 1398 |
| 20th team rating | 1093 |
| Top *average* score, 2026-07-30 episodes | 1152 |
| **Median** average score, same day | **670** |
| Episodes archived that day | 864 |

A median of ~670 is essentially the starting rating, so most of the field is running forked or
barely-modified baselines. Every top-20 submission is dated the competition's first day.

**Consequence for imitation learning.** The daily top-episodes datasets are ordered by *current*
rating, so today they contain agents near the $3,512 baseline while ours banks $43k. Imitating
them now would cap us an order of magnitude below what we already have — the "teacher caps the
ceiling" failure from the Orbit Wars post-mortem, in a worse form because the teacher is not even
ours. Their immediate value is an **opponent pool** and **scouting**, not IL. Re-check for IL once
leaderboard scores exceed our own.

## Infrastructure results

- **Env throughput** (`docs/throughput_measurements.md`): training box does 484 steps/sec
  single-threaded, 4,221 across 16 workers. 10B steps would be 27 days. The vectorized sim is
  required, not optional.
- **Market model parity** is exact against live episodes, every product, every step, 3 seeds.
- **Submission builds are verified, not assumed.** A hand-rolled `submission/main.py` once spliced
  a docstring over the first line, the module failed to import, the env fell back to no-ops, and
  the agent banked exactly its $3,000 start. `scripts/build_submission.py` now rebuilds verbatim
  and refuses to pass anything that does not beat `starter` from both seats.


## 5. The submission that lost, and what it cost us to learn — v4 → v5

v4 scored **$43,540** locally and **429.9** on the ladder, below the ~1000 starting rating. Both
downloaded replays were losses: **$27,119 vs $33,520** and **$27,640 vs $41,595**.

Not a crash and not a timeout — measured max turn latency was **18.9 ms** against a 1000 ms limit,
and no exceptions. The agent worked. **The measurement was wrong.**

| Opponent | v4 bank |
|---|---|
| `starter`, which we tuned against | $43,636 |
| a copy of itself | $21,200 |

`starter` sells almost nothing, so the market was never contested and every number we had was
roughly **twice reality**. This was economics question 4 — "does the opponent's selling measurably
change your bank?" — listed on day 1 and never answered. It halves it.

### What the replays showed

- The winner farmed **strawberry at $310/unit** against a $120 base, while we crashed **melon to
  $7**. They left **54 tiles as weeds** and still won: the win came from crop choice, not execution.
- We owned only **50 tiles**; they had all 100. Our land gate was too strict.
- Our bank *fell* from day 18 onward — buying $80 melon seed while melon sold for $25.

### Fixes, and three reversals worth remembering

1. **Opponent pool** (`kagg/arena/pool.py`): five competing strategies, judged on win rate.
   Opponents are built from a **frozen** BASELINE. The first version built them from the
   candidate's own parameters, so changing the candidate changed the opposition — which produced a
   confounded result (cows appeared to lift win rate from 62% to 81%) that reversed once fixed.
2. **Price-aware selling and planting**: hold below 55% of base, refuse seed below 45% of base,
   dump everything from day 28. Roughly neutral on score — the shed fills and forces the sale
   anyway — but it removes the $7 dumping, so it is kept as insurance.
3. **Animals: measured, and switched off.** Per-tile arithmetic said cows were the best tile in the
   game ($725, or $2116 with CARE, against wheat's $452). Against the frozen pool they are net
   negative: **70% win / $33.3k with none, 62% / $23.0k with ten, and total collapse to $467 at
   sixteen** — a capital death spiral at $400 a cow from a $3000 start. The gap is **routing**: a
   cow needs 4-6 actions a day plus a walk to the shed for feed, against wheat's ~1.5 per tile.
   Per-tile revenue rankings that ignore action cost are not decision-ready. The machinery is
   built and tested; only the count is zero.
4. **Melon: 25 → 12 → 25.** Against `starter`, 25 looked best. In mirror matches 12 looked best.
   Against the frozen pool on win rate, 25 is best again (77% vs 67%). **Mirror optimises the
   symmetric case** — what is best if both sides play it — **which is not what an Elo ladder
   rewards.** The thing to measure is a best response to a field.

### v5 result

**72% win rate, 16% draws, $35,544 mean** over 100 games (10 seeds x 2 seats x 5 opponents).
Beats wheat-only, strawberry and cow-heavy 100%; 30% against melon-heavy and its own mirror.
Melon-heavy remains the unsolved matchup.
