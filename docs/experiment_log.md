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
| 4 | **v4 — melon quadrant + wheat** | **$43,540** | **12.4x** |

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
