# BC/imitation pipeline and the RL framing

This doc merges seven source files: the problem-framing doc, the throughput measurements, the
stage-1 offline schedule-search review, the 2026-08-20 BC pipeline defect list, the 2026-08-20
imitation/DAgger plan, and two same-day Fable reviews of the bundle head.
It covers what kind of problem kaggriculture is, what the sim/env can measure per second, whether
the offline chain-search stack should keep existing, what broke in the BC pipeline, what the
BC -> DAgger -> RL plan is, and where two reviews of the same branch disagree.
The RL kill-criteria ruling itself is NOT merged here.
It stays at `docs/rl_feasibility.md` and `docs/kill_criteria_and_settled_positions.md` — cross-referenced only.
Every number below carries its source file and date.
Where two files disagree, that is called out, not silently merged.

---

## 1. Problem framing

source: what_kind_of_problem_this_is.md, written 2026-08-05, status note added 2026-08-08

### The classification

Kaggriculture is a deterministic, open-loop, multi-dimensional knapsack with a time-phased budget,
played as a best response against a fixed field.
Three measured facts back each clause:

- The allocation is computable: closed form from the town's drains reproduces the leader's farm.
- The schedule genuinely needs search: greedy-by-payback under a cash simulation recovers only
  **23%** of what a beam finds.
- The simulator is the verifier, never the search engine.

### Why it is not an RL problem

- There is nothing to react to: the leaderboard top submits a fixed 720-turn tape, and four fresh
  replays of the leader are byte-identical in every derived quantity across four opponents and both
  seats.
- The environment is deterministic given the tape, so `Q(s,a) = V(s')` can be computed by
  simulation rather than estimated.
- The horizon is 30 decisions (one per unit-chain), not 720 turns.
- The reward is terminal and Elo-shaped: a $43k win and a $4k win score identically.
- RL becomes right again only if the field turns adaptive or the state space grows past exhaustive
  evaluation. Neither is true as of this doc. See `docs/rl_feasibility.md`.

### The structure, formally

Constraints table as recorded:

| constraint | value | notes |
|---|---|---|
| tiles | 100, non-overlapping | 25 owned at spawn; 75 after two parcels |
| units (slots) | one chain per unit | a unit's position is a cumulative sum; two chains on one unit interleave and both fail |
| turns | 23 work turns per unit-day | binding constraint on tiles per chain |
| market drain | 8 products, 2,086 crop + 1,122 animal units | how much the town removes before prices floor |
| cash | $3,000 at dawn on day 0 | a flow, not a stock |
| land | $1,000 / $2,000 / $4,000 in fixed order | `_do_buy_land` ignores which quadrant is requested |
| hires | Fibonacci in the day's hire count, resets daily | 12 hands is $376/day; 17 is $4,180/day |

The objective is nearly additive: chains interact through exactly three channels — shared price
curve per product, cash timing, tile/slot exclusivity.
That near-additivity plus price-curve concavity makes the **allocation** tractable (ranking by
marginal value per resource is near-optimal).
But cash timing is not a mild coupling: it is a precedence constraint that compounds over 30 days,
and measured, it is worth roughly **4x** the allocation itself.
Additivity buys the mix. It does not buy the schedule.

### What genuinely needs search

1. The schedule — the leader's timeline is a dependency chain (melon+wheat NW day 0-2 -> revenue
   day 3 -> NE parcel day 7, SW parcel day 10 -> strawberry on 41 tiles days 7-14). A hand-built
   farm cannot test this because every configuration either has the land or does not.
2. Inputs vs outputs — wheat's market ranks 7th of 8 yet the leader plants 40 tiles of it, because
   14 pens eat ~420 units/season and wheat is the only crop returning cash by day 3. A revenue
   ranking scores it last; a purely additive model computes 0 wheat tiles against his 40.
3. The opponent shares the drain — both players sell into the same town inventory. Against a fixed
   field this is still tractable (a best response), but it is a game, not solitaire optimisation.

### The tool ordering (as designed)

1. Compute the allocation (`scripts/allocation_calculator.py`) — a target, not a starting point.
2. Beam over chains for the basin (`scripts/beam_chains.py`) — exact joint max per slot; weak at
   restructuring, only re-times.
3. CEM/ES to restructure out of the basin (`scripts/search_chains.py --seed-genome`).
4. Verify on held-out seeds in the real environment (`scripts/arena_gate.py`) — not optional.

> **Status note, 2026-08-08** (carried forward as written in the source): the chain-search stack
> above is the offline half and is currently **parked**; what ships is the closed-loop schedule
> agent in `docs/architecture.md`. The problem classification is unchanged. Dollar figures from
> that stack are from a codebase that has since moved — treat them as evidence about method, not
> as current scores.

### The overfitting trap

`search_chains.py` had a defect until 2026-08-05: the board draw was cached on one seed, so 30
generations of 500 candidates all fit the same 16 games, and the incumbent could never be
displaced. Fixed: new draw every generation, incumbent re-scored alongside challengers, and a
`--holdout` pass that prints the in-search vs held-out gap.
**Seed variance is ~15%.** Always quote the range.

### Six misdiagnoses in one day (the tell: a measurement about the game was really a limitation of the chain builder)

| looked like | actually was |
|---|---|
| "animals do not pay" | `ranch()` never collected fertilizer; then capped the herd at 4 |
| "fertilizer does not help" | `grow()` emitted `FERTILIZE` and never ordered any |
| "day 0 is the right time to buy land" | catalog hardcoded `LAND_DAY_CHOICES.index(0)` |
| "strawberry loses to melon" | `BLOCK_SIZE = 4`, because `grow()` watered every tile every day |
| "four pens is the right herd" | 1 pen = 1 chain = 1 slot, so five pens ate five of eight slots |
| "weeds cost nothing" | true on our farms, false on a farm that replants — carrot +$2,055 with DIG |

`tests/test_catalog_covers_every_gene.py` now asserts every gene `decode()` reads takes more than
one value somewhere in the catalog, and caught a live instance on its first run.

### The shape of the target

The top of the board is a knife-edge: everyone banks $120k-$160k and the leader edges it by ~3%.
On the Elo ladder a $2,634 win scores what a $50,000 win scores.
The target is a small consistent edge over several near-equal fixed scripts, which — because they
are fixed — cannot punish anything.

---

## 2. Measured environment throughput

source: throughput_measurements.md, measured 2026-07-31

### Reference-env (Python) throughput

`starter` vs `pass`, 100 games/row, 719 steps/game, reproduced with `scripts/bench_arena.py`:

| Machine | CPU | 1 worker | best multiprocess | 1B steps | 10B steps |
|---|---|---|---|---|---|
| Mac (dev) | 14-core Apple Silicon | 1,054 steps/s | 8,009 (12 workers) | 35 h | 347 h |
| Windows box (training) | AMD Ryzen 9 5900HX, 8c/16t | 484 steps/s | 4,221 (16 workers) | 66 h | 658 h |

The training box is **2.2x slower per core** than the dev Mac and **1.9x slower in aggregate**.
Scaling is poor: 16 workers gives only **8.7x** over one worker on an 8c/16t part.

**Correction to a previously recorded fact:** `README.md` recorded 1,163 steps/sec single-threaded
as measured; that is roughly the Mac rate and is **2.4x optimistic** for the training box, which
does 484.

Competitive runs in the comparable prior competition used 8-15B env steps (8th place ~1B on a
single 3080; 2nd place 10B; 1st place 15B).
On the training box: 1B steps = 66 hours (viable once, too slow to iterate); 10B steps = 658
hours / 27 days (not viable).
To reach 10B in 24 hours the sim must sustain ~116,000 steps/sec, about **27x** the Python env's
best multiprocess rate.
These figures are also optimistic: they use `starter` (a trivial random policy, no forward pass),
and `env.run()` cannot feed a GPU — it plays a whole episode with per-step callbacks inside a
worker process, so policy inference cannot be batched.

**Consequence:** the vectorized simulator is required, not optional, target ~100k+ steps/sec.
Multiprocessing on the reference env still buys a proof-of-life run: 100M steps in ~6.6 hours on
the training box, enough to test the RL frame against the explained-variance kill criterion before
committing to the sim build.

### Correction: the "1,032x" sim figure was an idle-profile measurement

Recorded 2026-07-31, after a JAX port measured the same code and could not reproduce it.
The original 499,543 steps/sec (and a later 752k) figures for the numpy sim were measured with
**one live unit per player on an empty board**, issuing WATER against nothing — almost every
masked update hit its `if not active.any(): continue` shortcut. That is the sim's best case, not
its working case.

Re-measured at B=512, units actually planting:

| live units per player | steps/sec |
|---|---|
| 1 (the original figure's shape) | 818,000 |
| 8 | 571,000 |
| 24 | 356,000 |

Even the 24-unit figure is optimistic: units start stacked on the spawn tile, so after the first
plants, the rest hit the occupied-tile early exit.
An independent measurement with units genuinely spread out and hiring each turn put the numpy sim
at **~15,000 steps/sec** at B=512 — though that run was taken at machine load 200, and the same
benchmark showed load can move absolute numbers by up to 2x.

**What to trust: ratios, not absolutes.** The speedup over the reference environment is somewhere
between **30x and 200x** on realistic workloads, not the 1,032x first recorded — still
transformative (a 1B-step run goes from 66 hours to 20 minutes-2 hours), but the headline number
was wrong and had already been repeated in several places.
Lesson stated in the source: a benchmark whose workload does nothing measures the shortcut, not
the code — state the workload alongside the number, always.

---

## 3. The offline schedule-search stack (stage 1)

source: fable_stage1_review_2026-08-09.md

Verified against `data/chain_search_scheduled/best_beam_genome.npz` (money $2,484, land days
11/15) and `data/logs/run_scheduler_v7.log`. Installed env at review time: 1.32.6.

### The headline: $2,484 is a decode veto, not a pricing error

Decoding the saved genome: `reachable_quadrants(g, 12) = 0`, `land_schedule(g, 12) = [11, 15]`,
decode used 7 chains, skipped 5.
The five skipped chains are every chain that needs land — melon block, all three strawberry
blocks, the fourth wheat block — the entire revenue expansion.
What actually plays: 2 cow pens, 2 sheep pens, 12 wheat tiles in NW. That farm banks $2,484 and
wins **0/16**.

Worse: `decode` (`chains.py:687-691`) emits `buy_land` orders from `land_schedule`
**unconditionally**, while `reachable_quadrants` gates only the chains — so the tape spends $3,000
on parcels on days 11 and 15 and then refuses every chain that would have used them.

### Why the gate says 0 parcels: three cash models disagreeing by 10x

- `scheduler.schedule()` (line 241-245): bank charges seed/animals/feed but **no crew at all**.
  Day-11 bank for this plan: ~$742-$1,963 depending on reserve.
- `chains.cash_curve()` (line 591-593): charges full crew from day 0 — $232/day for 11 hands here
  — even though half the slots start days 9-15. Its curve: `[1823, 741, -366, ..., 188, 108, 76,
  ...]`, **$108 on day 11**.
- The jax sim is the truth, in between.

`reachable_quadrants` breaks at `spent + follow_on > curve[day]` (chains.py:480): it needs ~$1,040
on day 11 and sees $108, so parcel 0 is refused and everything behind it dies.
The `chains.py:458` comment claiming "same rule as scheduler.schedule, so the gate and the
scheduler agree" is false in the way that matters: same rule, different bank.

### Why days 11/15, not the tape's 5/9/11

`revenue_rate` spreads a drain-capped, price-halved, share-halved season total evenly over 30 days
— a wheat block credits $140/day from day ~5, though real wheat cash is chunky.
Chains are placed before land is considered each day, so the bank pins near `reserve` and land
waits for the trickle to accumulate `price + follow_on + reserve` in one day's residual; `reserve`
is also double-counted (chain placement holds it back, and the land condition adds it again).
Re-running `schedule()` on the reproduced mix: reserves 0/300/800/1500 give parcel days 7/11,
8/11, 5/13, 7/14 — the days move ±4 with an arbitrary dial, i.e. noise around the trickle-crossing,
not a decision.

### Answer: is the revenue_rate cap the binding problem? No

The cap is real and the flat melon estimate is as bad as `test_the_planner_prices_volume.py` says,
but fixing it still scores $2,484-class results because the decode veto guts the plan downstream
of any pricing. Order of binding:

1. decode vetoes the plan (`reachable_quadrants` vs `schedule()` disagreement) — fatal today
2. decode buys land for chains it refuses — pays for the veto twice
3. trickle inflow mistimes land by ±5 days
4. the cap flattens melon/milk/wool estimates

`run_scheduler.py` already runs the full jitted jax sim per reserve arm to *score* the result — the
sim is cheap enough to be the objective, so a fifth cash-model proxy should not be built.
If stage 1 survives, replace "propose days from a cash model" with coordinate descent on
`start_day`/`land_day` genes scored directly by the sim; payback order survives as a search
initialisation.

### Answer: should stage 1 exist? Not in its current role

It optimises a proxy (`revenue_rate`) inside a proxy (genome -> decode, decode holding an
independent veto) against a phantom field (`heuristic,rancher,homestead,carrot` tapes, a pool
predating the cluster data and containing zero of the three real archetypes). It has never shipped
and its best output loses **16/16** to its own sibling.

The cluster doc changes the picture: the floor of the top five is a public agent available
locally — three of five run kaitofukami v23 byte-identical at 3,117-3,131 (verified running
locally), against our 1,123.5.
Highest-EV sequence recommended: (1) put v23 in the arena as opponent and measure win rate over
16+ seeds; (2) get into the v23 band first by hand-building the opening from cluster signatures
(worth ~2,000 points before any originality); (3) then search for the counter — Seb is rank 1
while banking the *least* money because he beats the v23 cluster consistently, which is exactly
what an exact simulator plus search is for.
Keep the chains/decode/sim machinery (the asset); retire the scheduler-as-cash-simulator and the
drain-capped revenue model; stage 1's question ("what mix, what days") stays, its cash-model answer
method goes.

### Everything else found in that pass

- `decode` buys land its own gate refused (chains.py:687-691 vs 674) — fix regardless of any other
  decision.
- `to_genome` silently truncates (scheduler.py:319): v7 scheduled 14 chains into 12 slots, the last
  two strawberry blocks vanished uncounted.
- The per-chain drain cap is not shared: `revenue_rate` applies `min(units, DRAIN*share)` *per
  chain*, so four melon chains "sell" 4x15 units into a 30-unit drain.
- `OPPONENT_SHARE = 0.5` vs `--share 1.0`: the mix un-halves the drain while `revenue_rate` still
  halves it two calls later — mix and cash model disagree about market size by 2x.
- CARE does not exist in the model: HealthStone (rank 2) is built on CARE compounding from sheep
  (+3/yield at interval 3), and no term in `revenue_rate`, `cash_curve`, or the mix knows CARE
  exists — same pattern as the animals verdict, ask what the code cannot express before trusting
  its negative.
- `expected_first_demand_day` draws shops without replacement (scheduler.py:99); 1.32.6 draws with
  replacement, so payback ordering used 1.32.2 unlock statistics — minor, noted for if payback
  order is kept as an initialiser.
- The opponent pool is the pre-cluster world: any stage-1 "wins" number, even fixed, is a statement
  about four of our own old tapes.

No files were modified in that review; the two `schedule()` traces and genome decode each ran in
seconds.

---

## 4. The BC pipeline: defects found 2026-08-20

source: the_bc_pipeline_2026-08-20.md, written the day BC round 0 first ran on 920,320 teacher
turns

**Headline: nine defects were found, and seven of them were invisible to a passing test suite; six
would have silently wasted or corrupted the training run.**

1. **`fit_bc` could not have taken a single gradient step.** `jax.value_and_grad` was called
   without `has_aux=True` while `bc.loss` returns `(total, per_head)` — every run would have died
   after labelling finished. Nothing caught it because `label_games`, `build_bc_rows` and `fit_bc`
   each had passing tests and the three had never been run in sequence. `scripts/bc_smoke.sh` is
   now that sequence: 2 games, rows, 2 epochs, about 60 seconds.
2. **Every SELL was emitted LAST at play time.** A bundle is a sorted multiset, alphabetical, so
   `BUY_ANIMAL < BUY_LAND < BUY_PRODUCT < BUY_SEED < HIRE < SELL`. `orders_from_heads` walked that
   stored order verbatim, but the env settles order slots in sequence and both simulators lay
   slots out sells-first (game.py:70-77, jax_sim._order_book). The jit path sold first; the
   real-environment path sold last — a student replaying the teacher's exact bundle had its hires
   refused on a thin bank. No sim-side number could show it, because the sim path was correct.
   Found by review, not internally; a three-decoder property test now exists.
3. **The row build was killed by the OOM killer, all 16 workers.** `build_bc_rows` read a whole
   1.2 GB shard into a list of dicts before sizing arrays; no traceback, logs stop after
   "vocabulary 197 of 256 slots", `free` showed nothing alive, output directory empty. Rows now
   stream, shards run in waves of 4 — 13 GB does not hold sixteen jax interpreters plus output
   arrays even after the fix.
4. **Market quantities were rounded to ladder rungs.** `SELL_BUCKETS = [0,1,3,10,30]` and
   `BUY_BUCKETS = [0,1,2,5]` were written down, never measured. Measured against the teacher's own
   play, 20,000 turns/shard:

   | op | orders | max | mean projection error |
   |---|---|---|---|
   | SELL | 70,411 | 68 | **27.2%** |
   | BUY_PRODUCT | ~18,000 | 134 | **35.3%** |
   | BUY_SEED | 28,123 | 23 | **16.5%** |

   The distribution is flat, not peaky — SELL uses every value 1-24 with no gaps — so the ladder
   was a lossy encoding of a continuous quantity. `SELL WHEAT 18` (played 2,983 times) came out as
   30. Replaced with a categorical whose class index *is* the quantity, capped at 64: exact for
   **99.79%** of SELL and **97.50%** of BUY_PRODUCT. HIRE is untouched and must stay so — all
   123,520 HIRE orders are quantity 1, because `HIRE x10` is ten orders and its multiplicity lives
   in the bundle symbol.
5. **`replays.encode_action` wrote `hire = 1`** — the exact bug the bundle head exists to fix,
   alive in the label path. The teacher hires ten hands in one turn on 18,666 of 920,320 turns.
6. **The play mask vetoed sells the teacher makes constantly.** `masks_for` refused any bundle
   selling a product the shed did not hold. Reference simply declines an unbacked sell
   (reference/kaggriculture.py:653) with no penalty. **48.75%** of the teacher's own SELL orders
   have a pre-turn shed of zero for that product, and **zero** of those 9,222 coincide with a
   same-turn DROP — they are the hourly re-offer. BC loss is permissive (teacher's action is legal
   by construction), so the strict mask vetoed bundles the student was trained to emit — **52%**
   of sell-turns — and the masked argmax handed that probability to the next-ranked bundle, which
   can be a live trade the teacher never made. A wrong trade, not a missing one.
7. **`masks_for` read a field that does not exist:** `state.private.shed` on a `State` with no
   `private`. It crashed on every call; 18 green tests never called it. Found by review.
8. **Two solve-cost probes were invalid in the same way.** First set `mod.UNSOLVE_DAYS = ()` on a
   module with no such attribute. Second patched `SOLVED_DAYS` and checked
   `getattr(mod, "PRECOMPUTED_ROUTES", {})`, also absent, so the guard read the default and passed
   for the wrong reason. Both returned ~1.0x and both nearly got reported as measurements. The name
   the code actually reads is `sys.modules["kagg.search.cover"].PRECOMPUTED_ROUTES`.
9. **The instrument measured the shard it had just trained on**, and compared only the marginal
   rate of empty bundles — which a model empty on exactly the wrong 78.9% of turns passes
   perfectly.

### Numbers that turned out to mean nothing

**`0.788` bundle agreement is what an UNTRAINED network scores.** Every head is zero-initialised
(jax_policy.py:195, `kernel_init=zero`), so logits are uniform, argmax picks index 0, and index 0
is the empty bundle — which the teacher plays on **78.9%** of turns. Without a fresh-init baseline
on the same rows, "learned the prior" and "learned nothing" are the same number.
`scripts/compare_checkpoints.py` exists for this.

What does carry signal, smoke run, 3 epochs on 2 games:

```
                      entropy   of max   distinct   agree   agree/tr
UNTRAINED  bundle       5.545    1.000          1   0.788      0.000
           op           3.135    1.000          1   0.139          -
after ep2  bundle       4.068    0.734          1   0.788      0.000
           op           2.639    0.842          3   0.273          -
```

An untrained head is at maximum entropy with one distinct argmax (uninformative); a collapsed head
is at low entropy with one distinct argmax (confidently wrong) — different failures, identical
agreement number. At 73% of maximum entropy the bundle head is underfit, not collapsed, so earlier
COLLAPSED warnings were reading the wrong side of that line.

### What is genuinely sound

- **Normalisation:** measured on the real npz, 20,000 rows: tiles `[-0.900, 1.750]` std 0.269,
  units `[-1.000, 2.699]` std 0.259, glob `[-1.394, 4.500]` std 0.442. Zero features with
  `|max| > 10`, zero inf, zero nan, nothing within 10% of the float16 ceiling (65,504). Money is
  scaled before storage.
- **The agent plays legally:** 2,876 turns through `kaggle_environments`, zero exceptions, zero
  orders out of slot order, zero bad quantities, zero over-length turns.
- **DAgger labelling is cheap:** forcing every day through the live solver costs **1.2x** (0.0108
  vs 0.0092 s/turn, seed 12345, d0-d12), not the ~100x assumed. 640 games on 16 workers: 5 minutes
  solved against 4 shipped.

### The constraint nobody chose

**13 of 115 input features are identically zero across 20,000 rows** — TOMATO as crop tile,
carried item, seed and shed; GOOSE as animal tile, carried and shed; EGG as carried and shed.
Cause is the teacher's repertoire, not the encoder: it never plants tomato and has no geese, so it
never holds eggs. Imitation cannot reach a mechanic the teacher never demonstrates, at any data
volume.

The Kaggle replays do contain them (25 replays):

| mechanic | turns | games |
|---|---|---|
| PLANT TOMATO | 164 | 17/25 |
| BUY_SEED TOMATO | 106 | 17/25 |
| SELL TOMATO | 90 | 15/25 |
| BUY_ANIMAL GOOSE | 45 | 7/25 |
| SELL EGG | 210 | 7/25 |

So BC on the tapes could reach what BC on this planner cannot, with two caveats: the downloads are
selected losses (common is not winning); and 164 tomato turns against 920,320 planner turns is
**0.02%** of a naive mixture — the student would ignore it, it needs upweighting or a separate
stage, not concatenation.
This interacts with a known bug: `SELLABLE` blocked CARROT, TOMATO and EGG from being sold at all
for a period, invalidating four carrot arms and the goose verdict — two of the three dead features
are exactly those products, so "our teacher does not do it" may descend from that bug rather than
from a judgement.

### Still open (as of this doc)

- Per-day op-for-op agreement (the acceptance measure) — `scripts/per_day_agreement.py` reports it
  both off-policy and on-policy; the gap is the covariate shift.
- `bc_dagger.py`'s loss is missing both padding corrections `bc.py` documents (not on the DAgger
  path used for round 0, but is the RL warm-start path).
- MLflow is installed (3.10.1) and wired to nothing.
- The value head is untrained by BC, correctly (`bc.loss` has no value target); it enters RL at
  its initialisation.

---

## 5. The imitation/DAgger plan

source: the_imitation_pipeline_2026-08-20.md, written after `docs/the_tape_dies_at_d13_2026-08-20.md`
closed out the tape-clone track

### Why this exists

The `(day, hour, unit)` tape reproduces kawashigi exactly to d12 and then rots: crops 53 -> 1,
weeds 0 -> 48, bank flat from d19 — a property of an open-loop sequence, not of the player. A
network keyed on the BOARD does not inherit it.
The unblocking move: use the shipped 2500 agent as the teacher.
`kagg/il/bc.py` had parked DAgger because "its only teacher that ever emits FEED is `jax_rancher`
at $12,078," which also burns 37-52% of its actions on a PICKUP thrash. A $90k-class queryable
teacher retires that objection — an instance of "a decision to skip a fix can expire when the
problem changes."

### The order

One network throughout, 726,647 parameters, three data regimes not three models:

1. Round 0, beta = 1 — this IS the BC stage: teacher self-play, teacher executes and labels.
2. Rounds 1..N, beta annealed to 0 — DAgger: student executes, teacher only labels, so every label
   lands on a state the student really produced.
3. RL: terminal reward, win 1 / loss 0, gamma 1.0, frozen pool. The only leg that can exceed the
   teacher.

`scripts/bc_dagger.py` already frames beta this way, so BC is not a separate stage to build.
How long to run DAgger is a measurement, not a round count: stop when student/teacher disagreement
on the student's own states plateaus (that quantity IS covariate shift). Typically 5-8 rounds,
where the existing `--rounds 8` default comes from.

### The box

```
/home/alex/kagg-teacher     fresh git clone, commit ead81e2
submission/main.py          sha256 b2e6808e38daaa76bc72949af40f69266435d8092c37a4716c9e13e82d9aaef7
.venv                       kaggle-environments 1.32.7, CPU jax -- labelling
.venv-cuda                  jax-cuda12-plugin + CUDA 12.9 -- training
16 cores, 13 GB RAM, 733 GB free
```

**The leaderboard artifact is `ead81e2`, not `cfd6f53`.** Alex named `cfd6f53`, which changed
`kagg/search/cover.py` but did NOT rebuild the bundle; the next commit did.
`cfd6f53:submission/main.py` still reads `UNSOLVE_DAYS = (29,)` against `ead81e2`'s
`tuple(range(24, 30))` — building a teacher from the named commit would have quietly used an agent
without the fix that defines it. Check what the bundle contains, not what the commit message says.
Two stale non-git copies exist on the box and were left alone: `~/kaggriculture` (17 G, Aug 15) and
`~/kagg` (12 G, Aug 9).

**Teacher smoke test:** 720 steps, both seats DONE, banks $142,002 / $147,440, **29.4s per mirror
season, 0.04s per turn.** The 3.99s dawn-solve figure in `main.py` profiles the SOLVER; the shipped
agent replays `PRECOMPUTED_ROUTES` and only solves `UNSOLVE_DAYS`. Under 16-way contention it is
53-90s per game, not 30s; 640 games ~50 minutes, ~10 GB.

### The teacher is sound in the late game

Check that mattered before teaching anything to a network: would DAgger clone a defect? Mean over
120 game-seats, sampled at hour 12:

```
day    our planner            kawashigi (holdout 94439800)   tape clone
d13    crop 59.0  weed 1.0
d18    crop 57.5  weed 2.4    crop 51  weed  1               crop 18  weed 34
d29    crop 16.0  weed 3.6    crop  3  weed 17               crop  1  weed 48
```

Our planner holds more crops than kawa at d18 and fewer weeds at d29 — it never weeds over.
Second reading matters more: our planner farms better than kawa and earns less. It banks $87,149
mean from MIRROR self-play (measured elsewhere in this project as roughly 2x inflated on an
uncontested book) against kawa's $86k-$153k on a contested one. The deficit is in the economy, not
routing, watering or crop management — exactly where the bundle head goes.

### The market is one token: sized on OUR teacher

5,752 player-turns from the pilot shards:

```
non-empty market   1,225 (21.3%)
distinct bundles   117            (tetsuya was 346)

top  20 bundles cover  93.45%
top  50 bundles cover  97.39%
top 100 bundles cover  99.70%
top 200 bundles cover 100.00%
```

A 128-class head is the whole distribution for ~16k parameters on the global token, replacing six
heads whose joint decode is measured to emit nothing.
The bundle that has been costing money is rank 2:

```
rank 2   113 turns   HIRE x10
rank 7    59 turns   BUY_PRODUCT WHEAT, BUY_SEED WHEAT, HIRE, HIRE
rank 9    49 turns   SELL FERTILIZER, SELL MILK, SELL STRAWBERRY, SELL WHEAT, SELL WOOL
```

Ten hires in one turn as ONE symbol — that is the d10 failure (units 8 and 9 never hired, 20
planned ops dying with them) becoming unrepresentable-as-broken rather than merely unlikely.
**Quantities need their own head, confirmed:** 52 of 116 non-empty bundles carry more than one
quantity vector; the five-way sell carries 48. Wrong quantity is graceful, wrong bundle is fatal.
Built: `kagg/il/market_bundles.py`, `tests/test_a_market_bundle_survives_the_round_trip.py` (red 1
error -> green 6 passed).

### How to see whether it is learning

No offline number counts alone — both have already lied: 86.2% per-decision accuracy on teacher
states scored 79.3% error on its own trajectory, and six well-fit marginals compose into an agent
that never trades. Three checks, cheapest first, after BC and after every DAgger round:

1. Argmax distribution on one batch (seconds). The parked BC track's signature was
   `P(move) = 6e-5 per unit-turn` — across 13 units and 30 days you'd expect ONE unit to ever leave
   the shed. Dead argmax means the loss or label alignment is wrong.
2. One replay (a minute): non-empty market rate against the teacher's 21.3%, and FEED count.
   `FEED 0/85` was the tell that the board-keyed clone was dead while its totals looked fine.
3. The board grid (five minutes): crops, weeds, bank per day against the teacher on PINNED seeds.
   Weeds at d18 is the most sensitive number available.

`kagg/il/bc.py` already carries three hard-won loss fixes: illegal labels hitting `NEG_INF = -1e9`
producing a 5.3e7 loss that would not move; padding slots making ~85% of the objective constant;
conditioned heads scored under every trade mode rather than only mode 0.
**There is no KL anchor.** `bc_dagger.py` says so outright. Not important for stages 1-2; matters a
lot for stage 3, where PPO can walk off the imitation prior in the first few updates.
`train_jax_rl.py` has `--kl-anneal`; not wired into this path.

### Reasons this might not work

1. DAgger caps at the teacher — best case at end of stage 2 is our own 2500 agent, in milliseconds
   instead of seconds. All the gain is in stage 3; if RL does not deliver, the chain returns a fast
   copy of the status quo. The real risk.
2. ~~Cloning a late-game defect~~ — CLOSED, measured above; the teacher is clean.
3. Bundle legality, not just identity — the head fixes which orders go together, not that
   `SELL WHEAT` is illegal with an empty shed. Needs a legality mask over 128 bundles per state.
4. The encoder bridge — labels are Kaggle observations, `jax_obs.encode` wants a sim state, and
   `adapter.state_from_obs` bridges them; `adapter.py` warns a second encoder "is a thing that must
   agree forever and will not."
5. Terminal reward is one bit per 720 turns. Right call, genuinely hard.
6. Bundling for submission — a hand-rolled bundle once banked exactly its $3,000 start here;
   `build_submission.py` is the guard.
7. Seed variance is ~2x on this teacher against ITSELF — $59k to $114k across four seeds. Every A/B
   needs pinned seeds.

### Caveats on the numbers above

All teacher figures are mirror self-play (uncontested market, banks inflated; crop/weed curves are
the trustworthy part). The kawashigi comparison column is ONE holdout game against 120 of ours. The
bundle vocabulary is from 4 pilot games — 117 is a floor, not a ceiling, and should be rebuilt on
the full round-0 set before the head is sized finally.

---

## 6. Bundle head reviews, 2026-08-20: two reviews, same day, one supersedes the other's premise

Two Fable reviews of the `bundle-head` branch were written the same day. They must be read
together, not independently, because **`fable_bundle_head_review_2026-08-20.md` found that the sell
mask mechanism `fable_bc_pipeline_review_2026-08-20.md` analyzes in its P1-1 section has never
actually executed.** `fable_bc_pipeline_review_2026-08-20.md` itself carries this correction as a
header note, added after the fact:

> Read together with `docs/fable_bundle_head_review_2026-08-20.md` (same day, same branch). That
> review found `masks_for` has never once executed (`state.private.shed` does not exist) — which
> undercuts this doc's P1-1 analysis, since it treats the sell-mask mechanism as live and firing.
> This file's P0 order-sort bug and its other findings are independent of that and still stand.

So: the P0 finding (SELL ordered last at play time) and most P2 findings in the pipeline review are
independent of the crash and still hold. The P1-1 sell-mask analysis (which numbers 48.75%/52.13%
by re-running the mask logic) describes a mechanism that, at the time of that review, could never
have run in the branch under test — it crashed on `state.private.shed` before it could veto
anything. Both reviews are below in full, in the order written.

### 6a. `fable_bundle_head_review_2026-08-20.md` — the two that stop everything

Requested 2026-08-20, read-only, on branch `bundle-head`. Two headline claims verified
independently before relaying; both hold.

**1. The branch has never executed. `masks_for` crashes on every call.**
`kagg/rl/jax_act.py:80` reads `state.private.shed`. Verified: `State` fields are
`('step_index', 'tiles', 'farm', 'inventory', 'unlock_day', 'unlock_shop', 'key')` — `has private:
False`. `farm.shed` shape is `(1, 2, 12)`, `N_PRODUCTS = 9`, `N_ITEMS = 12` — the shed is
`state.farm.shed` and is `N_ITEMS` wide (products AND animals), so even the corrected attribute
needs `[..., :N_PRODUCTS]` before it can meet `bundle_sells [N_BUNDLES, N_PRODUCTS]`.
**The flagship legality mask has never once been computed.**
`tests/test_the_bundle_head_reaches_the_simulator.py` passes because it hand-builds action dicts
and never calls `masks_for` or `sample` — CLAUDE.md's "a gate only tests what it exercises," the
fourth recorded instance.

**2. The teacher is an open-loop tape for 24 of 30 days.**
`UNSOLVE_DAYS = tuple(range(24, 30))` (submission/main.py:3349);
`PRECOMPUTED_ROUTES = {d: ... for d in SOLVED_DAYS if d not in UNSOLVE_DAYS}`.
So d0-d23 replay `PRECOMPUTED_ROUTES` and only d24-d29 are solved live.
The 0.04s/turn labelling cost that made "640 games in 50 minutes" possible **depends on** that.
Queried on a student's divergent state before d24, the teacher returns route slots for a board the
student does not have — the failure `docs/the_tape_dies_at_d13_2026-08-20.md` measured rotting a
board from d13. `cover._apply_precomputed` keys stop on `(tile, ops)` and drop mismatches
**silently** (main.py:3322, 4574, 4783), so on a divergent board the teacher degrades rather than
adapts. **DAgger's corrective labels are therefore wrong exactly where correction was the point.**
The fix exists (label with full solving, `UNSOLVE_DAYS = ()` style) but at ~4s per dawn solve
instead of 0.04s/turn — roughly **two orders of magnitude** on the labelling budget: 50 minutes for
640 games vs days. This must be priced before committing a long run; it is the load-bearing
assumption of the whole plan and neither party had checked it.
Caveat measured in the other direction: our planner holds 57.5 crops / 2.4 weeds at d18 and never
rots on its own trajectory — the teacher is sound on-distribution and unproven off-distribution,
exactly where DAgger needs it.

**P0, the rest:**

- Bundle mask width is `vocab.size` (197), head width is `N_BUNDLES` (256). `sell_table` returns
  `vocab.size` rows and nothing pads. Reproduced: `sample_head FAILS: Incompatible types for
  broadcasting: bool[2,197] vs bool[2,256]`. Fix must pad AND mark the 59 padding rows illegal —
  JAX gathers clamp out-of-range indices under jit, so an unmasked dead index would silently play
  the highest-ranked real bundle instead of erroring.
- Seven-plus call sites still use the one-argument `masks_for`, including `train_jax_rl.py:316`
  (the only leg that can beat the teacher) and `play_checkpoint.py:120` (the replay check the plan
  names as its main dead-policy detector), plus four test files. Red tests say the suite was not
  run after the signature change.
- `kagg/agents/neural.py` was never migrated: its local `MARKET_HEADS` is still the old six;
  `decode_action` reads `heads["sell"]`, `heads["hire"]`, `heads["buy_land"]`, which `Policy` no
  longer emits. No vocabulary is loaded anywhere in the file. Consequence: no out-of-scan DAgger,
  no submission, no replay check. Prerequisite, not cleanup.
- `kagg/il/replays.py:112` still does `hire = np.int32(1)` — the exact bug this change exists to
  fix, still live in the replay-label path. `bc.build_rows` will KeyError on `y_bundle`.

**P1, design faults that survive the syntax fixes:**

- The sell mask models FILLS; the teacher's labels are POSTS. Unit phase runs before market phase
  (kaggriculture.py:922 then :928), so a DROP-at-shed lands before that hour's sell settles, while
  `masks_for` reads the pre-turn shed. `bc_dagger.py:181` zeroes illegal labels, so those turns
  silently leave the loss. **Measure before training:** fraction of teacher sell-bundle turns
  where a sold product has pre-turn `shed == 0`. If not ~0, drop the sell mask or compute it
  against shed-plus-carried.
- `bundle_index_of`'s empty-bundle fallback is silent, and DAgger is where it fires — the
  vocabulary came from mirror self-play; DAgger queries the teacher on STUDENT states, where it
  can emit combinations self-play never produced, so the fallback teaches "do nothing" precisely
  on the recovery states DAgger exists to label.
- The qty heads are ungated in `_score` and in `bc_dagger`'s loss. `build_bc_rows.py` got the
  gating right; `bc_dagger.py` — the script the plan runs — did not. With 78.9% empty turns the
  head collapses to bucket 0, and the floor-at-1 decode then turns every sell and buy into
  quantity 1.
- The quantity ladders cannot express the teacher: `BUY_BUCKETS = [0,1,2,5]` against a measured
  `BUY_SEED CARROT 8 / WHEAT 9` in one order: `nearest()` maps both to 5, a ~40% under-buy on the
  purchase that gates planting.

**P2, and where the framing was wrong:**

- The factorisation worry was misdirected — what is implemented is not `p(qty | bundle)`; qty
  heads read `gtok` only, the bundle gates which entries are read, never the distribution. For
  imitating a deterministic teacher, any state-conditioned factorisation is exact in principle
  (target conditional is a point mass); the 3,233 quantity vectors are variation across states,
  and shed/bank are in the observation. Two genuine leaks (both second-order): the planner's dawn
  plan is hidden state (an h12 label depends on an h0 plan, multimodal given only current
  observation); in stage-3 RL a stochastic policy's sampled bundle cannot covary with sampled
  quantities. **Do not restructure the heads for this now.**
- Delete the threshold calibration — a single categorical fitted to a deterministic teacher has
  per-state argmax equal to the teacher's action regardless of the 78.9% marginal. If under-firing
  shows up later, the right form is ONE scalar threshold calibrated to 21.1%, not six.
- Minor: `bundle_index_of` compares sells as flags so duplicate `(op,item)` pairs alias; stale
  measurement snapshots disagree across files (78.7%/117/5,752 vs 78.9%/197/920,320);
  `build_bc_rows.market_labels` sets `w_qty_*` even when `vocab.index` fell back to EMPTY.

Bottom line from this review: the bundle-not-marginals argument and the hire-count fix both survive
review; everything else needs work — a design was built on top of code that had never run, and a
plan was priced on a teacher property that was never checked.

### 6b. `fable_bc_pipeline_review_2026-08-20.md` — read subject to the correction above

Read-only review of branch `bundle-head`. Files reviewed: `kagg/il/market_bundles.py`,
`kagg/rl/jax_act.py`, `kagg/rl/jax_policy.py`, `kagg/il/bc.py`, `kagg/il/replays.py`,
`scripts/build_bc_rows.py`, `scripts/fit_bc.py`, `scripts/label_games.py`, `scripts/bc_dagger.py`,
`kagg/agents/neural.py`, `scripts/measure_solve_cost.py`, `scripts/measure_quantity_ladders.py`,
plus reference/kaggriculture.py (market phase), sim order-book code, relevant tests, and the live
vocabulary artifact `data/il/bundle_vocab.json` (197 bundles, rewritten same day 16:49).

**P0 — `orders_from_heads` emits the bundle in sorted order, putting every SELL LAST; the env
settles slots in sequence, so decoded buys/hires spend a bank the sells have not yet filled.** (This
finding is independent of the mask crash and stands.) Mechanism: `reference/kaggriculture.py:544`
`_process_market` walks order slots in sequence and fully settles slot `i` before parsing slot
`i+1`; `_commit_unit` checks `farm["money"] < price` per unit. The three decoders:
`kagg/sim/game.py:70-77`/`:267-279` and `kagg/sim/jax_sim.py:869-905` use canonical order SELL,
BUY_SEED, BUY_PRODUCT, BUY_ANIMAL, HIRE, BUY_LAND (correct — sells first); `market_bundles.py:59`
`bundle_of` returns `tuple(sorted(pairs))`, which sorts alphabetically
(`BUY_ANIMAL < BUY_LAND < BUY_PRODUCT < BUY_SEED < HIRE < SELL`); `market_bundles.py:300`
`orders_from_heads` iterates in that stored sorted order, so the real-env play path
(`neural.py:118-123 decode_action`) emits BUY_ANIMAL, BUY_LAND, BUY_PRODUCT, BUY_SEED, HIRE, and
**SELL last**. Consequence: a student replaying the teacher's exact bundle fails buys/hires that
the teacher's same-turn sells would have funded — silent (env returns no error, the order just
dies), invisible in sim-side evaluation (sim path is correct), appears only when `neural.make_agent`
plays the real `kaggle_environments` env. Example from the live vocab:
`(BUY_ANIMAL COW, BUY_ANIMAL SHEEP, HIRE x7, SELL FERTILIZER)` — two animals and seven hires
attempted before the fertilizer sale settles. Fix (no flag): iterate the bundle in the sim's
canonical kind order inside `orders_from_heads`, add a test asserting SELL precedes HIRE in a mixed
bundle. `Vocabulary.to_orders` has the same defect and no callers — fold into the fix or delete.

**P1-1 (subject to the header correction — analyzes a mechanism the other review found never
executes) — the sell mask: strict at play, permissive at train, colliding mainly with offer-spam.**
Measured in this review, 25 Kaggle replays, both seats: turns with a SELL 10,140; SELL orders total
18,915; SELL orders with pre-turn shed == 0: **9,222 (48.75%)**, of those with same-turn DROP: 0;
sell-turns containing a masked-illegal sell: **5,286 (52.13%)** of sell-turns. So the drop-then-sell
same-hour case the mask would wrongly forbid never occurs in this sample, but half of submitted
SELL orders name a product the shed does not hold (agents re-offer quotas hourly — "offers are not
fills," now in the label path). As analyzed (pending re-verification against the crash finding
above): training is permissive so the student is trained to emit shed-empty sell bundles; at play
`masks_for` vetoes exactly those, and the masked argmax renormalises onto whichever bundle ranks
next — potentially a live trade never selected against anything. Caveat already in the source: the
48.75% is measured on Kaggle winners, not the planner teacher; measure it on the 920,320-turn
planner shards before deciding. Recommendation as written: pick one consistent side everywhere —
either drop the shed-empty sell constraint from play/DAgger masking, or keep the mask and apply it
in the BC loss too.

**P1-2 — `bc_dagger.py`'s in-scan loss commits both padding mistakes `bc.py` documents and
avoids.** Unit heads weighted by `unit_live * legal` only, no `active_unit_heads` factor, so
crop/item/qty labels are scored on every live slot regardless of teacher op (trains the crop head
toward WHEAT on non-PLANT slots). Market quantity heads weighted by `legal` only with all-ones
masks, no `w_qty_*` equivalent, so quantity heads score on all products every turn with label 0
wherever the bundle selected nothing — with ~79% empty turns this trains quantity heads toward
class 0, and the floor-at-1 decode turns every sell/buy into quantity 1. The 920k-row run goes
through `fit_bc.py` -> `bc.loss`, which has both weightings correctly, so this does not corrupt the
imminent run — but `bc_dagger.py` is the in-scan half of the chain, and if it labels any future
round, that round is wasted.

**P1-3 — the vocabulary is not pinned to the checkpoint; the artifact was rewritten the same
day.** Every module says the vocab "must be the SAME file everywhere" but nothing enforces it:
`fit_bc.py` stores only `vocab_size`/`n_bundles` in the checkpoint; `neural.make_agent` loads
whatever `data/il/bundle_vocab.json` currently contains and never compares it to the checkpoint;
the file had mtime 2026-08-20 16:49 (rewritten that day), so any checkpoint trained against an
earlier build silently reinterprets every bundle index at play; `load_vocab`'s default path is
relative, adding a cwd dependency. Three loaders exist for the same artifact and currently agree
only by accident (all counts tie at 1, sort is stable, EMPTY already at index 0).

**P1-4 — the fit_bc instrument can be satisfied by a model that fires on the wrong turns, probes
only training data, and watches none of the quantity heads.** Probe slice is
`shards[0][0:4096]` — data the model trained on this epoch, nothing held out anywhere. `empty_rate`
compares marginal frequencies only: a model firing non-empty 21% of the time on the wrong 21% of
turns matches the teacher's 0.789 exactly; detects only total collapse above a 0.98 tripwire (a
student at 0.95 empty vs teacher 0.789 passes without comment). No instrument reads quantity heads
at all. Cheap fixes recommended: hold out one shard and probe it; per-row bundle agreement on
non-empty rows (top-1/top-5); mean |argmax(qty) - y_qty| over cells where `w_qty_* == 1`.

**P2, smaller findings:** `scripts/measure_quantity_ladders.py` crashes at import (reads
`P.SELL_BUCKETS`/`P.BUY_BUCKETS`, deleted from `jax_policy.py` the same day) — loud, not silent, but
it is the instrument that justified `MAX_QTY`. `neural.py` carries dead code referencing removed
heads (`_fire`, `calibrate`, `MARKET_HEADS`) — any call is a KeyError; house rule: delete dead code,
don't document it. `bundle_of` counts orders the env rejects as decisions (`_parse_order` returns
None for SELL/BUY_* with `len < 3` or `qty <= 0`, but `bundle_of` includes them). `jax_act._score`
scores `qty_*` heads for all products every turn (PPO path — wastes variance rather than corrupting
BC, but a warm-started PPO run will pay it). `sell_table` padding rests on an assumption ("no shed
ever holds all nine") that can be violated late-season; consequence graceful, still a wart.
`replays.encode_action` re-loads/re-parses the vocab JSON on every call — quadratic-feeling on a
920k-row build. Smoothing note: `--smooth 0.02` bounds the label-vs-rest logit gap at ~9.4 nats
(~8.1 for the 64-way); the parked BC track's absorbing-state gap was 9.7 nats, so at these widths
smoothing is a mild regulariser, not the gap-bound the docstring credits it as. Several stale
docstrings flagged as highest-value cheap edits post-fix.

**Checks that came back clean:** quantity round-trip (clamp to 63, never wrap, all three decoders
floor at 1, pinned by test); HIRE as a count (consistent everywhere); the live vocabulary (197
bundles, EMPTY at index 0, no bundle exceeds the 10-order cap, no repeated non-HIRE pair, zero
pattern-aliased groups); `fit_bc`'s permissive masks are the right call for teacher-state BC (the
asymmetry with play is the actual problem, per P1-1); `bc.loss` weighting is correct as specified;
`label_games.obs_snapshot` stores everything `adapter.state_from_obs` reads;
`measure_solve_cost.py` now patches the names the bundle actually reads and hard-stops on a
zero-route shipped arm; **`masks_for` is now executed by tests**
(`tests/test_the_policy_can_take_a_turn.py` calls it five times on a real state); shed contents are
in the observation (`jax_obs.py:314`, `shed / 50` capped at 3.0).

**What is missing that would make the result uninterpretable:** the real-env gate (nothing plays
`neural.make_agent` through `kaggle_environments` against the arena pool — `play_checkpoint.py` is
in-sim only, so it can never surface the P0 ordering skew or adapter drift); a per-day op-for-op
agreement report against the teacher; a three-decoder agreement test (no test compares
`orders_from_heads`, `to_sim_actions`, `to_sim_fields` on the same drawn heads across the whole
vocabulary — would have caught the P0); vocab identity enforcement (P1-3); a held-out shard and
per-row/quantity instruments in fit_bc (P1-4); and a note for `dagger_planner.py` (in progress at
review time) that OOV teacher bundles are labelled EMPTY, so student states driving the planner
into bundles the 197-entry vocab lacks are silently taught as "do nothing" — log the OOV rate per
round.

**What was NOT checked in this review:** `adapter.state_from_obs`'s tile reconstruction and
`jax_obs.encode`'s feature semantics beyond the shed feature; `jax_masks.unit_op_mask` /
`unit_crop_mask` / `unit_item_mask` correctness; `kagg/rl/commit.py` interaction with the op head
beyond widths; float16 storage precision in `build_bc_rows`; whether the planner teacher actually
relies on same-turn sell-to-hire funding on specific days (argued from reference settlement
semantics, not measured on shards); anything about the submission bundle, `train_jax_rl.py`, or RL
loss beyond `_score`. The 48.75% measurement is 25 of ~160 local Kaggle replays, both seats, not
resampled.
