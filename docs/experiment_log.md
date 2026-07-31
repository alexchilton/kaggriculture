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
| 5 | v5 — opponent-pool tuned, price-aware | **ladder 613.5** | first score above the 600 start |
| 6 | v6 — deferred selling, 8-strategy pool | ladder ~546-622 (unsettled) | 90.6% local |
| 7 | **v7 — contrarian: opponent-reading crop choice** | **beats v6 100% head-to-head** | submitted |

**Ladder submissions start at 600.** v4 at 526.4 was genuinely losing; v5 at 613.5 is genuinely
winning, if only modestly. v6 is newest and its rating has settled least -- v5 itself read 555
before rising to 613.5 with more games -- so it is not yet comparable.

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


## 6. Deferred selling — the money-versus-winning result

Holding produce for the last stretch of the season, then dumping at the endgame. Measured over
192 games (12 seeds x 2 seats x 8 opponents):

| hold_days | win rate | draws | mean money |
|---|---|---|---|
| 0 | 81.2% | 12.5% | $36,996 |
| **10** | **90.6%** | 6.2% | $37,060 |
| 14 | 77.6% | 7.3% | $37,505 |

**Money barely moves; win rate moves 9 points.** Holding converts narrow losses into wins without
changing what an average season banks — and `hold_days=14` banks the *most* money ($37,505) while
winning the *least* (77.6%). That is the Elo-versus-money distinction made concrete: had we
selected on mean bank, as v1-v4 did, we would have picked the worst of the three.

The mechanism is that town drain runs whether or not anyone sells, so an untouched market drifts
into scarcity. Holding banks that premium; selling early spends it. 14 days overshoots because the
shed (100 items, overflow destroyed) forces sales anyway and the endgame dump crashes the price.

## 7. The pool was too self-similar

v5 measured 72% locally and then lost ranked matches at 555. The pool was five strategies, all
variants of **our own agent**, so it shared our blind spots.

Replay evidence: one opponent won $24,984 to $18,997 farming **25 tiles of carrots** against our 50
tiles of wheat and melon. Another won with strawberry at $310/unit while our melon sat at $25.

Pool widened to eight, three copied from agents that actually beat us (`carrot_25`, `small_farm`,
`straw_small`), and a `max_tiles` parameter added to make small-farm play expressible. Carrot as a
filler crop was tested directly: 68.3% against wheat's 73.3%, so it is not our answer, but it is
now in the pool as an opponent.


## 8. Deferred selling is a dominant strategy, not a pool artifact

The worry was that `hold_days` only helps because every pool opponent dumps continuously -- i.e.
that it exploits a blind spot we share with our own opponents. Tested head-to-head against the
`melon_heavy` profile, varying **both** sides (12 seeds x 2 seats):

| | opponent holds 0 | opponent holds 10 |
|---|---|---|
| **we hold 0** | 20.8% win (58% draws) | **0.0% win** |
| **we hold 10** | **100.0% win** | 20.8% win (58% draws) |

Whoever holds beats whoever does not, 100% to 0%. When both hold, it returns to the symmetric
baseline. So it is a genuine **best response**, not an artifact -- and it is worth the most while
the field does not hold, which the day-1 median average score of 670 suggests is the case.

The corollary is that the edge decays if the field adopts it. It is worth banking now.

**A methodological note.** The first version of this test reported *identical* numbers for both
opponent settings, which is what exposed it as broken: `evaluate` runs matches in worker
processes, and those re-import the module fresh, so mutating `pool.BASELINE` in the parent never
reached them. Rerun in-process. That is the third test this session that looked green while
proving nothing -- after the vacuous season-parity test and the `starter`-only tuning. **Ask what
a passing test would look like if the mechanism were broken.**


## 9. The vectorized simulator, and the bug only the parity gate caught

Built numpy-batched rather than JAX, on the grounds that the hard part is the one-unit-at-a-time
market settlement and that is far easier to make exact with ordinary control flow. Measured
**499,543 env steps/sec at B=512**, against **484** on the training box: a **1,032x** speedup, well
past the ~100k target that a 10B-step run implies.

| Component | Parity tests |
|---|---|
| Market pricing and settlement | 27 |
| Tile state and nightly transitions | 16 |
| Unit operations | 77 |
| Town drain and shop schedule | 5 |
| Farm bookkeeping (money, seeds, shed, hiring, land) | 11 |
| **End-to-end episodes** | **4 in-suite, 60 in the full gate** |

**End-to-end parity: 60/60 full-length episodes exact**, including 30 with hiring and 15 with land
purchases.

### The bug, and why it matters more than the speedup

The first run of the gate scored **0 out of 40**. Every one of those 136 component tests passed,
and a 200-step end-to-end check passed. The composition was still wrong.

`ops.plant` only plants on an empty tile, but the game loop spent a seed regardless. A PLANT onto
an occupied tile is a free no-op in the reference; in the sim it silently burned a seed. The farm
starved gradually, so the divergence did not surface until step 130-320 -- past the length of the
short check. Fixed by returning which games actually planted and spending only those seeds.

Two lessons worth carrying:

1. **Unit tests verify components; only the gate verifies composition.** Every piece was correct
   and the assembly was not. `CLAUDE.md` demanding end-to-end parity before training is what caught
   this, and had it not, a policy would have trained in a world where seeds randomly vanish --
   with nothing crashing and no number looking obviously wrong.
2. **A short parity check is not a weak version of a long one, it is a different test.** Slow drift
   is invisible until it accumulates.

### Two deliberate divergences, stated rather than buried

- **Weed spawning is statistically faithful, not sequence-identical.** The reference draws from a
  per-day Python RNG shared by both farms, consuming one draw per empty tile. An exact port costs
  ~6000 Python-level RNG calls per game, over 3 million per batch at B=512, which would destroy the
  speedup entirely. The parity gate therefore runs with `weedSpawnChance=0` on both sides, making
  every deterministic mechanic exactly comparable, and weed behaviour is checked separately by rate.
- **Shop unlock order is supplied by the caller**, for the same reason: the choice consumes the
  same RNG stream after the weed draws, so it depends on board occupancy. Observed from a real
  episode for parity, sampled for training.


## 10. Animals are viable after all -- our conclusion was an artifact of our own routing

`docs/ladder_analysis.md` found that the three largest losses on the ladder -- $104k, $93k and
$84k -- were all **small 8-15 tile farms built almost entirely on pasture animals, two with zero
hired hands**. That contradicted experiment 5, which measured animals as clearly net negative.

The contradiction resolves cleanly: experiment 5 measured animals **inside our heuristic**, which
spreads over 50-100 tiles and hires 8-14 hands. In that layout an animal costs a walk to the shed
for feed every day, and the routing swamps the return. It was never a fact about animals.

`kagg/agents/rancher.py` inverts every choice the heuristic makes: **six animals, zero hired hands,
about six tiles, all adjacent to the shed** so feed pickup costs no movement.

| | rancher | heuristic |
|---|---|---|
| vs `starter` | $44,614 | $43,575 |
| head to head, 12 games | **$42,362, 41.7% win** | $43,575 |

An untuned agent with a completely different structure essentially matches our most-tuned one.
Herd size has a sharp optimum -- 4 gives $31.6k, **6 gives $45.7k**, 10 gives $15.9k -- and the
binding constraint is the **action budget**, not money: one farmer has 24 actions a day and each
animal needs feed, care and a harvest.

### Three bugs, each of which pinned the herd at exactly one animal

Worth recording because each looked like a strategy result and was not:

1. **Three of the four shed-access tiles start locked.** They sit in NE, SW and SE. The plot list
   handed back all four, so only one was ever usable.
2. **An occupied pasture keeps `kind == "PASTURE"`.** The "needs work" check matched the farmer's
   own tile at distance zero, so it selected itself every turn and never moved to build a second.
3. **PLACE draws from carried inventory, not the shed.** An empty pasture is rarely a shed tile, so
   a bought animal sat in the shed forever while the farmer walked back and forth.

Each produced a flat, plausible-looking score curve across herd sizes. "Changing the parameter does
nothing" is a bug signature, not a finding.

## 11. The pool was still one strategy in eight hats — `contrarian`, and what it exposed

Section 7 widened the pool from five members to eight and called it "eight competing strategies".
It was not.
Every member was `heuristic.make_agent()` with different dials: identical tile ordering, identical
hiring curve, identical job priorities, identical sell cadence.
The pool tested robustness to **crop mix** and to nothing else, which is precisely the axis the
ladder losses were *not* on.

`kagg/agents/contrarian.py` is one genuinely different agent, sharing no code and no decision rule
with the heuristic.
Four differences, each taken from a measurement rather than invented:

- **It reads the opponent's board.** Both farms are fully visible; nothing else in the pool looks.
  Melon is winner-take-all — only 158 units fit above `I0` before its `sq` glut curve puts the
  price on the floor — so it takes melon while the opponent leaves it alone and switches to
  strawberry once they commit.
- **Compact routing.** Tiles are worked in order of distance to the nearest shed-access tile and
  capped at 34, and land is bought for shed access rather than area (one extra quadrant only).
- **It waters before it harvests** on the last day of the watering window, which the heuristic
  does the other way round and which costs a unit per cycle.
- **Per-product sell floors from the curve shape**, not a global `hold_days` window: melon is
  dumped at 0.55 of base, strawberry is *held* above 1.85 of base.

`kagg/arena/pool.py` grew a third spec form, `("module", "kagg.agents.contrarian")`, so a pool
member can be any importable agent rather than only a dict of heuristic overrides.
It stays picklable, which a closure would not.

### What it measures

12 seeds x 2 seatings, held out, and the whole table was then re-run on a second independent draw.

| | seeds 300-311 | seeds 500-511 |
|---|---|---|
| heuristic vs the old 8-member pool | 92.2% | 93.2% |
| **heuristic vs the pool with `contrarian` in it** | **81.9%** | **82.9%** |
| `contrarian` vs the 8 heuristic-based members | 92.2%, $45,769 | 90.1%, $45,920 |
| `contrarian` head to head vs the heuristic | **100.0%**, $37,401 vs $30,115 | **100.0%**, $36,840 vs $30,129 |

**Adding one opponent costs the heuristic 10.3 points of measured win rate**, and it loses to that
opponent 48 games out of 48.
The pool was hiding a weakness, exactly as the ladder results implied it was: local win rate said
92% while ranked matches said otherwise.

`contrarian` also banks more against the same eight opponents than the heuristic does — $45.8k
against $37.1k — while winning at the same rate, which is a reminder that the two are not the same
question.

### The bug that made the first version look hopeless, and the one that made it look clever

Both are the same failure mode as section 10's: a plausible score that was really a defect.

1. **Buying land silently abandoned ten growing tiles.** Unlocking a quadrant makes tiles *closer*
   to the shed available, so a plain nearest-N set drops crops already in the ground; they go
   unwatered and `_daily_refresh_plants` turns them into weeds two days later. Measured in a live
   episode: land bought on day 7, ten weeds on day 9, and the agent scored **$9,052**. Keeping any
   tile that is already growing took the same agent to **$42,460** against the same opponent.
2. **The agent quit melon because it had successfully sold melon.** The contested test also read
   market inventory, on the theory that inventory is a durable record of a rival's sales. It is
   not: melon's `max_yield_day` is 12, so nobody can sell melon before day 12, while the last
   melon planting that can ripen goes in around day 17. Inside the window where the decision is
   live, an above-`I0` melon inventory is **always our own**. Cost: identical 92.2% win rate,
   $39,885 mean bank against $45,769 without the clause.

### The ablation, which is the actual case for reading the opponent

Same 8 opponents, seeds 300-311:

| variant | win rate | mean bank |
|---|---|---|
| reads the opponent's board | **92.2%** | $45,769 |
| hard-wired to melon | 90.1% | $41,087 |
| hard-wired to strawberry | 74.5% | $26,306 |

Neither fixed choice is as good as the branch, and the gap is largest exactly where it should be:
hard-wired melon collapses to $23.5k against `melon_heavy` and 29% against its own mirror, while
the branch holds 100% and $37.3k against `melon_heavy`.

Worth noting *why* the branch beats hard-wired strawberry by 17.7 points: the opponent's board is
empty on day 0, so melon always goes in first and the plan moves to strawberry as their commitment
becomes visible. The early melon cycle is what funds the season. A latched decision would lose it.

### What this does not show

`contrarian` has had no parameter search at all — every number in its `PARAMS` was reasoned from
the market curves or copied from a measurement, and none was tuned.
It has not been submitted, so there is no ladder evidence either way.
And its 100% head-to-head record is against **one** opponent that it was, unavoidably, developed
while looking at; the pool result is the less flattering and more trustworthy number.


## 12. The JAX port, and a throughput figure that was wrong

`kagg/sim/jax_sim.py`: one jitted graph per step, scanned for rollouts, parity-checked against the
numpy sim over full 719-step episodes comparing **all 22 state arrays after every step** -- not the
final bank. Prices are bit-identical over a 150,000-wide inventory range.

| Workload, B=512 | numpy | JAX (scan) |
|---|---|---|
| farmer (1 live unit) | 95k | 434k (4.6x) |
| full crew (24 units) | 15k | 151k (10.0x) |
| full crew, B=16384 | 11k | 470k (**42x**) |

JAX loses in exactly one place: an all-NOOP empty board at B=512-1024, where it is 0.7-0.8x. Under
`lax.scan` it never loses.

**The scaling direction matters more than the ratio.** numpy peaks around B=512-1024 and then
declines; JAX keeps climbing. If the policy dominates the loop -- which an entity transformer
will -- the right response is the largest batch that fits, and that is precisely where numpy is
worst and JAX is best. JAX also keeps state on-device, removing the per-turn host/device
marshalling a numpy env forces on a GPU policy.

### The correction it forced

The port could not reproduce the numpy sim's recorded 499k steps/sec. It was right not to.

That figure, and a later 752k, were measured with **one live unit on an empty board issuing WATER
against nothing**, so nearly every masked update hit its `if not active.any(): continue` shortcut.
It benchmarked the shortcut. Re-measured at B=512 with units actually planting: 818k at one unit,
571k at eight, 356k at twenty-four -- and even that is optimistic, since the units start stacked on
the spawn tile and the later ones hit the occupied-tile early exit.

**The real speedup over the reference is 30-200x on realistic workloads, not 1,032x.** Still
decisive -- a 1B-step run drops from 66 hours to between 20 minutes and 2 hours -- but the headline
was repeated in commit messages, the README and two docs before being caught.

Absolute throughput on this Mac moves by up to 2x with machine load, so **only ratios measured
against a same-time control are trustworthy**. State the workload next to the number, always.

### Not yet measured on the 3080

Two things need checking before relying on any of this for training. Money is `float64`, which the
3080 runs at 1/32 rate -- it is provably integral and well under 2^24, so float32 should be exact,
but that needs testing rather than assuming. And the unit-slot loop is a data-dependent
`while_loop`, which on GPU serialises up to 24 kernel launches; a fixed 24-iteration `scan` may
invert the tradeoff there.


## 10. Offline plan search on the fast simulator — a tie, from a worse starting point

First use of the batched simulator for anything. Code in `kagg/search/`, driver
`scripts/search_plans.py`, tests in `tests/test_search_{plan,executor,transfer}.py`.

### What was searched, and what was rejected

A **closed-loop farm plan** of 277 categorical genes: crop and planting phase for each of the 100
tiles, target headcount for each of the 30 days, sell quantity per product per five-day block, a
price floor per product, a harvest-ripeness dial per crop, the three land-purchase days, the day
planting stops and the day everything is dumped. A deliberately mechanical interpreter
(`kagg/search/executor.py`) carries the plan out and owns no strategy of its own: it splits the
farmed tiles into one contiguous block per live unit and walks each unit to the nearest outstanding
job in its own block. There is no crop priority, no filler crop, no sell cadence and no hiring
formula to inherit.

Raw per-turn action sequences were rejected on **transferability**, not size. An open-loop script
assumes it knows where every unit is standing, and the simulator's documented hand-spawn divergence
desynchronises it on the first hire. Beam search over per-day decisions was rejected because there
is no partial score worth pruning on: the measured economics say money banked early is money not
invested, so pruning on partial return prunes exactly the late-maturing, slow-ramp strategies the
economics identify as the prize.

CEM over a factored categorical distribution was chosen partly because the fitted distribution is
itself the readable answer -- after the run, `p(tile i = MELON)` is a direct statement about that
tile.

### Two silent divergences the parity gate could not have caught

Both found while building the interpreter, both invisible when broken:

1. **Atomic PLANT.** The reference drops *every* PLANT for a crop when a turn's requests exceed the
   seeds held; the simulator instead spends seeds greedily unit by unit. The parity harness never
   exposed this because its random scripts drive **one** unit per player. Neutralised by never
   requesting more plants than seeds held.
2. **Market order slots.** The simulator settles each product with both players alternating; the
   reference pairs the players' *i-th order*. They agree only if both players put the same product
   in the same slot, so the agent emits a **fixed 8-slot order list** padded with
   `["SELL", crop, 0]`, which `_parse_order` rejects while the slot still lines up. This also keeps
   the list inside `maxMarketOrdersPerTurn`, which the simulator does not model at all.

### Transfer, measured before trusting any search result

Same plans, both implementations, weeds off, the reference's own unlock draw
(`tests/test_search_transfer.py`):

| seed | real | simulator | drift |
|---|---|---|---|
| 101 | $29,593 / $5,684 | $31,284 / $5,651 | +5.7% / -0.6% |
| 202 | $29,377 / $4,304 | $31,061 / $4,181 | +5.7% / -2.9% |

The residual is hand spawning. The simulator is optimistic by about 6% for the stronger side.

### Opposition, and why it was calibrated first

Round 1 searched against three hand-written plans; round 2 added round 1's winner. The three were
checked in the **real** environment against `kagg.arena.pool.COMPETITIVE` first, because a weak
field inflates everything:

| opposition plan | win rate | mean bank |
|---|---|---|
| `melon_wheat` (the heuristic's shape in the plan language) | 72.2% | $28,567 |
| `wheat_only` | 13.0% | $3,978 |
| `carrot_small` | 11.1% | $4,939 |

So the field was one genuinely strong opponent and two weak ones. Adding the round-1 winner in
round 2 is what re-opened the discrimination: the population's best fell from a saturated 1.00
against three opponents to 0.50 against four, and climbed back to 1.00 over sixteen generations.

### Result — real environment, `COMPETITIVE` pool, both seatings

| agent | seeds 400-411 | seeds 500-511 | ex-mirror (400 / 500) |
|---|---|---|---|
| heuristic (`kagg/agents/heuristic.py`) | 81.5% / $36,227 | 82.9% / $36,247 | 87.5% / 87.0% |
| **searched plan** | **80.1% / $45,583** | **78.2% / $45,562** | **87.5% / 87.5%** |
| `melon_wheat`, the search's starting point | 69.9% / $28,498 | — | 75.0% / — |

216 games per cell (12 seeds x 2 seats x 9 opponents). Both agents are stable across the two seed
sets to within $30 of mean bank, so the ~15% seed variance seen elsewhere is not in play at this
sample size.

**Read it as a tie, not a win and not a loss.** Against the eight opponents that are not the
candidate itself, the searched plan and the heuristic are identical: both beat every pool member
100% of the time and both lose to `contrarian` 100% of the time. The whole headline gap is the
`mirror` column, where the searched plan draws against itself far more often (mirror 21% and 4%
win, against the heuristic's 33% and 50%) -- and `CLAUDE.md` already records that a mirror match is
not a best response and points the wrong way. Money is 26% higher, which counts for nothing on an
Elo ladder and is recorded only because it is a large, stable difference.

The thing that makes it interesting is the starting point: the same interpreter running the
heuristic's own strategy scores 69.9%. Search closed a 10-point gap and produced a plan that
contradicts the heuristic on almost every choice it makes.

### What the search found, and where it disagrees with the heuristic

The chosen plan owns 50 tiles (NW plus NE). On those 50:

| crop | searched | heuristic |
|---|---|---|
| MELON | 20 | 25 |
| CARROT | 6 | 0 |
| STRAWBERRY | 5 | 0 (set to 0 "against theory") |
| TOMATO | 5 | 0 |
| WHEAT | 5 | 25 |
| FALLOW | 9 | 0 |

- **Wheat is nearly abandoned.** Five tiles of fifty, against the heuristic's "wheat fills every
  tile not claimed". The economics doc's case for wheat was units per tile-season and market depth;
  the search prefers three crops the heuristic sets to zero.
- **Nine of fifty owned tiles are left fallow on purpose.** The heuristic farms everything it owns.
- **NE is bought on day 0**, spending a third of the $3,000 start before any revenue exists, and
  **SW and SE are never bought**. The heuristic gates land on 3x its price plus 80% of tiles
  planted, which delays the first purchase to roughly day 6-12 and eventually buys all four
  quadrants. Both halves of that are contradicted.
- **Tomato is never sold before the dump day** -- its price floor came out at 1.1x base, which the
  market cannot reach, so the floor is a hold. Deferred selling was rediscovered, per product,
  rather than as the heuristic's single global `hold_days` window.
- **Melon's floor came out at 0.0** -- sell at any price. The heuristic's 0.55 floor exists
  specifically to stop melon being dumped at $7, and the search says that insurance costs more than
  it saves when melon is only 40% of the farm rather than 100% of a quadrant.
- **Strawberry is left to accumulate to its 4-unit cap before cutting**, where the heuristic
  harvests ongoing crops eagerly so the cap never blocks production.
- **Planting stops on day 20 and everything is dumped from day 24**, both earlier than the
  heuristic's 28.
- **Headcount averages about 8** across the season under the fitted distribution, which is the
  number `scripts/tune_heuristic.py` independently converged on, and is markedly lower on days 0-2
  and 26-29.

Only the melon gene carries a strong signal in the fitted distribution: `p(MELON) = 0.33` per tile
against a uniform 0.167, while every other crop and FALLOW sit near 0.13. Sixteen generations of
192 is not enough to resolve 100 tile genes individually, so the specific scatter above is one
sample from a distribution that is still mostly flat -- **the crop mix is the finding, the tile map
is not**.

### Honest limitations

- **Selection degenerates to money once win rate saturates.** With three or four opponents the
  elite set hits 1.00 win and the tie-break -- mean bank -- takes over. Round 2 delayed it; it did
  not remove it. More opponents, or a rating rather than a win count, is the fix.
- **The plan language cannot express DROP or PICKUP**, because the parity-gated simulator has no
  such op. So a searched plan can only get produce into the shed at the nightly drop, capped at 100
  items, while the heuristic drops mid-day and sells the same day. That is a structural handicap in
  the substrate, not a choice of the search.
- **Animals are absent** for the same reason.
- **Nothing was searched against `contrarian`**, the only pool member that is not our own heuristic
  wearing a hat, and the only one that beats both agents 100% of the time. That is the obvious next
  target.
