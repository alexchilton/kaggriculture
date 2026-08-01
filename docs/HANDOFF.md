# Handoff — 2026-07-31, end of day 1

Read `CLAUDE.md` first (rules and the "Lessons learned the hard way" list), then
`docs/experiment_log.md` (every experiment, its score, what it taught).
This file is the short version of where things stand and what to do next.

## The single most important thing — RESOLVED 2026-07-31 evening

**Parity now passes. 300/300 full-length episodes exact, 256/256 tests green.** Search, imitation
learning and per-turn RL are unblocked.

| configuration | result |
|---|---|
| one unit, no hiring | 60/60 full-length episodes exact |
| one unit, hiring + land | 60/60 exact |
| six-unit crew | 60/60 exact |
| six-unit crew + land | 60/60 exact |
| twelve-unit crew, heavy hiring | 60/60 exact |
| JAX sim vs numpy sim | 16/16 tests, field for field |

**"Broken under hiring" was wrong, and hiring had nothing to do with it.** The same failure
reproduced at 1/8 with hiring switched off entirely; what all the failing cases shared was driving
more than one unit *slot*. The harness filled six unit actions per player whether or not the farm
owned six units. The reference ignores a surplus action for movement and work, but
`interpreter` computes the atomic PLANT block over the actions *submitted* — so a plant request
from a hand that does not exist still cancels the farmer's plant. Every agent builds its action
from `[farmer, *farm["hands"]]`, so no real game can reach that. The harness now truncates the same
way, and `hire_rate` was raised for the gate because truncation would otherwise have quietly turned
it back into a single-unit test.

Four other things were wrong, three of them in code:

- **Both seats are paid the same price on a contested unit.** `_process_market` quotes both players
  before either commits; the sim re-quoted after seat 0, docking seat 1 a dollar a unit. Fixed in
  `game.py`, `market.py` and `jax_sim.py`. A passing test had asserted the wrong behaviour outright.
- **The JAX sim had no atomic-PLANT rule at all**, and spawned every hand on NW. It predates the
  commit that fixed both in numpy and was never re-gated. It was failing 3 of its own tests on
  `main` before any of this session's work.
- **Three of the five fixes were covered by nothing.** Backing each one out left the suite green.
  Each now has a test that goes red without it.

**The one real divergence left, deliberately:** the reference pairs the players' *i-th market
order*, while the sim settles product by product. It is real — a hand-built case swings $129 in one
turn — but **unreachable by any agent we have**: every pairing of `contrarian`/`heuristic`/`rancher`
over three seeds gives exactly $0 of error, because agents emit sells in a canonical product order,
so a shared product only misaligns when the products *before* it differ. Fixing it means replacing
`Actions.sell` (a quantity per product) with an ordered order book, touching `game.py`,
`executor.py`, `jax_sim.py` and `parity.py`. Worth doing before a *learned* policy sells, since its
ordering would be state-dependent. Not worth doing now.

Reproduce the gate with:

```python
from kagg.sim.parity import random_script, run_reference, run_sim, compare
import numpy as np
rng = np.random.default_rng(4242)
script = random_script(rng, steps=719, max_units=6, allow_hire=True, hire_rate=0.5)
ref, unlocks = run_reference(script, seed=1500)
sim = run_sim([script], unlocks=unlocks)[0]
print(compare(sim[:len(ref)], ref))     # []
```

## Agents, best first

| agent | what it is | evidence |
|---|---|---|
| `kagg/agents/contrarian.py` | **Best.** Reads the opponent's board to pick its crop; compact routing; per-product sell floors | beats `heuristic` 100% and `rancher` 100% head-to-head. **Submitted as v7.** |
| `kagg/agents/heuristic.py` | Melon quadrant + wheat, many hands, deferred selling | was v6 |
| `kagg/agents/rancher.py` | 6 animals, **zero hired hands**, ~6 tiles by the shed | ties `heuristic` untuned |

`contrarian`'s key insight: **melon is winner-take-all.** Only ~158 units fit above `I0` before its
`sq` glut curve floors the price, so two committed players cannot both be paid. It farms melon
while the opponent ignores it and switches to strawberry once they commit, because strawberry needs
89 tiles to saturate and is therefore uncontestable.

## Ladder

Submissions start at **600**, not 1000. Scores drift a lot at low game counts — v5 and v6 each
moved twice in a few hours, once reversing their order — so do not rank submissions on one reading.

| | score |
|---|---|
| v7 `contrarian` | submitted, pending |
| v6 | ~546-622 (unsettled) |
| v5 | ~584-613 (unsettled) |
| v4 | 526.4 |

`docs/ladder_analysis.md`: **local win rate predicts direction but not magnitude.** Local 72-91%
maps to real-ladder 42-63%. Useful as a compass, worthless as a yardstick.

## Open tasks, in the order I would do them

1. ~~**Close the sim parity gap under hiring** (task 9).~~ **Done** — see above. The simulator is
   no longer the blocker; the next constraint is which agent to build the pool around.
2. **Rebuild the opponent pool around `contrarian`** (task 5). Cheap, and it converts work already
   done into a decision. Every measurement before today was taken against a pool of near-clones of
   one engine, which we now know hid a 10.3-point weakness. Three structurally different agents
   exist and there is no trustworthy ranking between them.
3. **Finish the JAX GPU benchmark** (task 6). Parity passes 14/14 on the 3080 (`~/kagg-venv` on the
   Windows box, `PYTHONPATH=~/kagg`), but the speed table did not come through. Two untested
   assumptions: whether `float64` money can narrow to `float32` (the 3080 runs f64 at 1/32 rate),
   and whether the data-dependent `while_loop` over unit slots should be a fixed 24-iteration
   `scan` on GPU.
4. **Search follow-up** (task 8). It tied the heuristic rather than beating it, so it is not worth
   imitating yet. The obvious next target is searching *against `contrarian`*, the only opponent
   that beats everything. Its findings that contradict the heuristic: wheat nearly abandoned (5 of
   50 tiles), 9 tiles deliberately fallow, NE bought on day 0 and the other quadrants never, and
   per-product hold thresholds instead of one global window. Only the melon gene has strong
   statistical signal — the crop mix is the finding, the tile map is not.
5. **Resume RL** (task 7), lowest priority. It sets 9 strategy dials per day on top of the
   heuristic, so it inherits that heuristic's ceiling — and `contrarian` already beats it 100%.
   Fix first: `CheckpointCallback(save_freq=...)` counts *per-environment* steps, so with 10 envs
   the real trigger was 500k and a 448k-step run saved nothing.

## Things that will bite you

- **Never evaluate against `starter` alone.** It barely sells, so the market is never contested and
  every number comes out ~2x reality. This cost a submission. Use `kagg.arena.evaluate`.
- **Select on win rate, not money.** The ladder is Elo; margin does not count. `hold_days=14` banks
  the most money and wins the least.
- **`kagg.arena.evaluate` runs matches in worker processes**, which re-import modules. Mutating
  `PARAMS` or `pool.BASELINE` in the parent does **not** reach them. Three measurements this session
  were invalid for exactly this reason, and each one looked green.
- **"Changing the parameter does nothing" is a bug signature, not a finding.** Three separate bugs
  each pinned the rancher's herd at one animal and produced a flat, plausible score curve.
- **Do not use `git add -A` while subagents are writing.** It captured a broken mid-edit draft of
  `contrarian.py` and shipped it in a commit.
- **Do not run four parallel agents plus RL training.** Load hit 204 on 14 cores and everything
  crawled.
- **State the workload next to any throughput number.** A sim benchmark measured on an empty board
  with one idle unit produced "1,032x", repeated in three docs before being caught. The real figure
  is 30-200x.

## Where things live

```
kagg/agents/     heuristic, rancher, contrarian (all self-contained, submittable)
kagg/arena/      run_arena, and pool.py (the opponent pool + evaluate)
kagg/economics/  market and production models, parity-tested against live episodes
kagg/sim/        batched simulator, numpy + jax_sim.py, parity.py is the gate
kagg/search/     CEM over farm plans
kagg/rl/         Gymnasium env: one strategy decision per day, terminal win/loss reward
scripts/         build_submission.py (KAGG_AGENT env var picks the agent), benchmarks, tuner
docs/            experiment_log.md first, then ladder_analysis.md
```

Build and verify a submission: `.venv/bin/python scripts/build_submission.py` — it refuses to ship
anything that cannot beat `starter` from both seats.

## RL: the per-turn policy on the fast sim (2026-08-01)

The simulator now models the whole game, so the policy is per-turn over all 18 ops rather than
tuning a heuristic's dials. `scripts/train_jax_rl.py`, `kagg/rl/`, 643,351 parameters.

Start a run on the 3080 box with `kagg-train` (installed at `/usr/local/bin`, so no path to type);
`kagg-status`, `kagg-log`, `kagg-stop` do what they say. Runs survive disconnection -- verified by
leaving one for twelve minutes with no SSH sessions at all.

### The frame

Terminal reward, win 1 / loss 0, paid once on the turn the episode ends. gamma 0.97 **per game-day**
= 0.998732 per turn, so a terminal reward still carries 40% of its value at turn 0. Per-turn 0.97
would be 3e-10 -- the same number means two entirely different things depending on the unit, which
is why both are printed at startup.

### What was wrong, and how each was found

Five bugs, and only the first was found by reading the code:

1. **The terminal reward was paid on every turn after the episode ended.** `step_index > LAST_STEP`
   is a level, not an edge, so a 64-turn rollout paid it up to 34 times. Found by Alex asking
   whether the crash was in the episode-completion path -- it was not, but the question sent me to
   look at code no test had ever reached.
2. **Episodes never restarted inside the scan**, so the simulator ran past turn 719 into a season
   that does not exist, and those turns were trained on.
3. **The policy ran entirely in float64.** `jax_sim` enables x64 for parity, so anything that does
   not state its dtype -- including `self.param()` -- silently becomes f64, and this card runs f64
   at 1/32 rate. 24 turns/s against a simulator doing 44,700. Nothing in the logs looked wrong.
   A startup check now refuses to run unless every parameter is float32.
4. **`ev_signal` could never report a number.** It selected rows with `reward != 0`, which keeps
   only winners; every selected return was then 1.0, variance 0, EV undefined. The one honest
   kill-criterion metric had never once fired.
5. **Episodes ran in lockstep and structurally could not desynchronise.** `jax_sim.State` keeps
   `step_index` as a single scalar for the whole batch, so every game terminated on the same update:
   terminal reward arrived in one burst every ~11 updates and was absent from the other ten. The
   critic spent ten updates in eleven regressing onto its own predictions -- a bootstrap with no
   unique fixed point at gamma near 1 -- and drifted to a value of **1.315**, which is impossible
   when the reward is capped at 1. `explained_variance` read +0.98 throughout, because a critic that
   is self-consistently wrong explains its own targets perfectly.

   **Raising the batch size does not help**: with a shared scalar counter it makes the burst bigger,
   not more frequent. Fixed by holding `--n-phases` independent states at evenly spread points in
   the season and running them under `vmap`. No simulator change, so parity is untouched.

Number 5 was found by an external model review, not by me. I had been treating its symptoms.

### Also applied from that review

- **Only heads the chosen op reads are scored.** Every head is still sampled, but a crop head
  sampled when the op is not PLANT had no causal effect, so scoring it is zero-mean noise spread
  over four times more parameters than the decision involved. Entropy fell from ~100 nats to ~9
  when they stopped being scored -- that gap was the noise.
- **Value clipping**, the same trust region the policy gets.
- **Sigmoid value head.** Reward in {0,1} and gamma <= 1 means the true value is provably in [0,1].
  A guardrail, not the cure -- the staggering is the cure.
- **Opponent pool**, 25% of groups. Pure mirror self-play has a degenerate fixed point: both seats
  share parameters, so a mutual draw is stable and nothing pushes against it. A frozen past self
  does not co-operate in standing still. Its rows are weighted out of the loss -- their log-probs
  come from other parameters, and including them would make the PPO ratio a comparison of two
  unrelated policies.
- **EMA target network**, available via `--target-ema`, **off by default**: changing two things
  about the same mechanism at once breaks the one-delta-at-a-time rule.

### The missing measurement -- do this first

**`eval_policy.py` cannot yet play `contrarian`, and that is the gap that matters.**

It scores against random-legal (a floor) and frozen checkpoints (the only self-play signal both
sides cannot fake). It does not score against our heuristic agents, because they take the reference
environment's **dict observations** -- `farm["tiles"][y][x]`, `private["shed"]`, `market["prices"]`
-- while the policy plays on `jax_sim.State` arrays. Bridging them needs an adapter that renders a
`State` into the dict shape `heuristic.agent(obs, config)` expects, per game, per turn.

That adapter is worth building even though it is only for evaluation, because of what it would tell
us. The opponent pool is frozen copies of *itself*, so it is **not** heuristic-bounded -- the
opponent improves exactly as fast as the policy does. But self-play has a failure mode that no
internal metric can see: **a local equilibrium**. If neither side ever discovers the animal economy,
neither is ever punished for lacking it, and the pair converges happily on a crop-farming plateau
around $38k while the real frontier is $110k. Every win rate looks fine throughout.

`contrarian` is the yardstick that would expose it: if the policy plateaus at roughly contrarian's
level, we are in the valley. Train against it and we inherit its ceiling -- `CLAUDE.md` is explicit
that a heuristic is a sparring partner and never the policy -- but measure against it and we learn
where we stand.

### Open, in order

1. **Adapter so `eval_policy.py` can play `contrarian`.** The only thing that can currently detect
   a self-play plateau.
2. **Watch entropy.** It fell 9.3 -> 3.8 -> 3.0 over three updates once the noise heads stopped
   being scored. `--ent-coef 0.003` was chosen when entropy was ~100, so it is effectively a
   different knob now. If entropy reaches ~0 within the first few hundred updates, raise it.
3. **`ev_signal` must pass 0.5.** The committed kill criterion, and only now measurable at all.
   Ignore the bare `ev` column: on reward-free windows it is the critic scoring itself.
4. **Throughput.** ~400 turns/s at batch 128 puts 1B steps -- the scale that took 8th place on this
   same GPU -- at about a month. Batch 384 has the card at 100% against 14% before, and
   `scripts/sweep_batch.py` measures marginal (not cumulative) rate at several sizes. Compile time
   at batch 384 with 12 phase groups and the opponent pool is over ten minutes, which is worth
   attention on its own.
5. **Imitation from search or replays.** Self-play from scratch reached 8th place in a comparable
   competition at ~1B steps; the top finishers used 10-15B. Seeding past the early valley is what
   the post-mortem already recommends.

---

## Session 2 handoff — 2026-08-01, late morning

Two tracks ran in parallel: RL on the 3080, and a new heuristic agent. **The RL track is healthy
and running. The heuristic track is broken and should be picked up first**, because it is where the
score is.

### Context that reframes everything

A friend's *heuristic* scores **1230 Elo**. The ladder starts at 600 and our agents sit there.
630 Elo points is a ~2.6% win rate for `contrarian` against it. So heuristics are nowhere near the
ceiling in this game -- ours were simply weak -- and that changes the priority order: a strong
heuristic is both the fastest route to a score and the best imitation target for RL later.

### RL: running, and the critic bug is fixed

`kagg-train` on the box; `kagg-status`, `kagg-log`, `kagg-stop` alongside it. 36 updates, ~750
episodes, ~300k steps, 166 turns/s.

The first GPU run trained but did not learn: the critic climbed 0.59 -> 0.82 heading for 1.0 while
explained variance sat at zero and entropy collapsed. An external review found the mechanism with a
single measurement worth remembering:

> For a matched (game, turn) pair, `V(seat 0) + V(seat 1)` must equal **1** -- win plus loss, or two
> ties. It is arithmetic, true for any policy at any skill, and it holds on **100% of rows** against
> the ~0.14% that carry a terminal reward (one turn in 719).

It read 1.17 climbing to 1.34, with `sum` almost exactly `2 x V`: the critic was **seat-blind**,
emitting one global number for both sides of the same board. Adding that identity as an auxiliary
loss (`--seat-coef`, on by default) fixed it -- the critic now sits near 0.50 where symmetric
self-play says it belongs, and `ret` is falling (0.745 -> 0.661) rather than climbing.

Two metrics were blind and are now fixed. **Win rate was arithmetically pinned to 0.500** because it
summed reward across both seats of every game; it now measures the live policy's own seats and reads
0.501-0.506, which is the only signal that can move. `ev_signal` reports `n/a` when a batch's
terminal rows all share an outcome -- at ~22 terminal rows per update that happens often, so the
count is now logged next to it.

**Unexplained:** throughput fell from ~650 to 166 turns/s between runs at identical settings.
Possibly thermal on a laptop GPU after hours at 100%, but that is a guess -- measure it. At 166
turns/s, 30M steps is ~50 hours rather than ~13.

### Heuristic: `kagg/agents/converter.py` is BROKEN -- uncommitted, do not ship

Built from replay 89197802 (top two agents at $106k and $113k against our $38-52k). It scores
**$159-$3,859 against `contrarian`'s $51,000**. Eight attempted fixes did not converge, and the
last few were guesses. Everything below is *measured*, not theorised:

| symptom | measurement |
|---|---|
| never sold anything | `sold: {}` for a whole season, `HARVEST` absent from the op census |
| melon dies | 3 tiles at day 2, **0 by day 6** -- planted, watered a while, then dead |
| only 3 of 14 seeds planted | planting sat below the feed loop in priority |
| bank drains to $25 | 46 wheat hoarded in the shed for animals that did not exist |
| feed loop dominates | **517 PICKUP against 128 FEED** |
| livestock in storage | an earlier version ended with **37 sheep in the shed**, ~$20k idle |

Bugs already fixed (keep these): purchases are capped by free pens; placement outranks feeding;
crop harvesting was silently dropped when the loop was rewritten for per-unit animal ownership; pen
building is deferred to just before the herd arrives; crop and livestock phases are separated.

**What I would do next, and what I would not.** Do not tune the priority list further -- that is
what the eight failed iterations were. Instrument first: log per-day plant count, water count,
harvest count and revenue by product, and find where melon dies. The likely candidate is that
watering still loses to the wheat-pickup loop once any animal exists, so melon never reaches its
yield window. A cleaner structure than one global priority list is to **split the crew**: dedicate
N units to crops and the rest to livestock, with stable ownership on both sides, rather than having
every unit re-decide between the two economies every turn.

### What the replay and the review actually established

- **Melon is the opening economy and is winner-take-all.** Its `sq` glut curve fits only ~158 units
  above I0, so whoever commits first takes the pot. `contrarian` banks $51k in this matchup almost
  entirely from melon: 225 units off 24 tiles. Skipping melon to protect the opening bank hands that
  market over *and* leaves no money for livestock.
- **Wheat is an input with a guaranteed rising price.** The town drains it all season; measured $25
  -> $56 monotonically. Both winners bought rather than grew it. One made 81% of its revenue simply
  *trading* it -- a carry trade on a trend both players create with their own feed demand.
- **Feeding logistics are not the constraint.** 12 hands x 24 turns = 288 actions/day; a 20-animal
  herd needs ~140-160 including collection. The action ceiling is ~35-45 animals. What actually
  binds is capital, the 100-item shed cap, and market absorption.
- **The 52-58% PASS in days 0-8 is waste, not strategy.** Hands are dismissed nightly and the
  Fibonacci fee resets each morning, so crew size is a free, memoryless daily choice -- 12 hands cost
  $376/day against $12 for five. Carrying a full crew through the empty opening burns ~$2,900, close
  to the entire starting bank. **This is the one place to beat the replay rather than copy it**, and
  `converter` already sizes its crew to outstanding jobs.
- **CARE is nearly free** given the idle capacity, and should go on every animal every cycle.
- **Nobody buys SE (4000).** It does not relieve the binding constraint and has too few days left to
  amortise. Treat as settled.

### Also landed this session

- `kagg/rl/adapter.py` + `tests/test_adapter.py` (2/2). Rebuilds a `jax_sim.State` from the
  reference environment's dict observation, so a checkpoint can play the real game -- needed both to
  evaluate against `contrarian` and to submit. It reconstructs the State and reuses the *same*
  `jax_obs.encode` training uses, rather than adding a second encoder that would have to be kept in
  agreement forever.
- `scripts/eval_policy.py` -- run for the first time this session, which immediately found a bug in
  it: the seat swap only applied against another checkpoint, so every random-legal evaluation
  measured seat 0 twice. Also produced the first honest number for a trained policy: it beats
  random-legal 1.000 while **ending the season with $7** against a $3,000 start. It wins only
  because the opponent destroys more.
- Host-device syncs removed from the training loop: four full-array transfers per update, plus
  **256 host-to-device index transfers** (numpy shuffle, one dispatch per minibatch). Speedup not yet
  measured on GPU.

---

## Session 3 — 2026-08-01, afternoon

Three things landed: two real bugs out of `converter`, a graded fitness so the search has
something to climb, and two more blind metrics out of the RL loop.
Both jobs are running as this is written.

### The correction that matters most

**The previous entry's "critic is fixed, sitting near 0.50" is not what the log shows, and the
log column it was read from does not describe the network being trained.**
`traj["value"]` comes from `value_params`, which under `--target-ema` is the slow EMA copy.
An EMA of parameters is not a network any gradient has touched: at decay 0.99 it still carries
`0.99^n` of the random initialisation, which is 53% at update 63.
That run printed `V 0.606 sum 1.212` -- the exact signature of a seat-blind critic -- while
`seat_loss` on the live network read 0.0006, i.e. a seat sum of 1.02 and entirely healthy.
I spent a chunk of this session treating that as a live bug before checking which network produced
the number.
The columns now carry a `t` prefix when they describe the target net, and `seat_loss` is the one
to trust.
Measured after restarting without the EMA: `sum` 1.147 -> 1.021 -> 1.005 over three updates.

**`--target-ema 0.99` was on the command line at all**, against this file's own note that it is
off by default because changing two things about one mechanism at once breaks one-delta-at-a-time.
It is off again.

### `converter`: two bugs, both structural, neither found by reading the code

`tests/test_converter.py` plays a season and prints a day-by-day table of op mix against board
state.
It found both of these in one run, after eight rounds of hand-tuning had not.

1. **`yield_units > 0` is not the test for a harvestable crop.**
   `_new_plant` sets it to 1 at once for every crop with `ongoing=False`, while the environment's
   HARVEST silently returns until `first_yield_day` -- 10 days for melon.
   A unit picking HARVEST on that basis issues a **legal no-op that cannot clear its own
   precondition**, so it picks it again next turn: 89 in the first two days, all three units stood
   on their own melon, and nothing below the harvest branch ever reached.
2. **Planting outranked watering, and a seed planted today is dead by morning.**
   `_new_plant` opens at `consecutive_unwatered = 1` and two dry days turns the tile to WEED, so
   planting incurs a debt due within hours rather than deferring revenue.
   With planting first, `seeds > 0` kept every unit planting for the whole of day 0: the
   fourteenth seed went in at hour 23, nothing was watered, all fourteen were weeds at midnight.
   **Zero WATER actions in a 720-turn season.**

Measured on seed 4000: WATER 0 -> 128, melon standing on day 6 0 -> 13, and the second watering
step at the bottom of the priority list turned out to have been dead code all along.

**It still does not win a game.**
0/16 against `contrarian` both before and after, and mean money *fell* $4,458 -> $2,402: the
repaired crop funds an earlier collapse into the livestock phase.
That half is a separate bug and is left red as a strict xfail -- 562 PICKUP against 197 FEED.

### The reason eight tunings could not converge

**The fitness was saturated.** 0/16 before the fixes and 0/16 after.
Every candidate scored the same, so there was nothing to rank -- and no evolutionary method,
plain ES or CMA-ES or memetic or island, can select among candidates that all score identically.
Search cannot find a missing precondition, because a missing precondition is not in the space
being searched.

`kagg/arena/ladder.py` scores against opponents ordered by strength and takes the mean win rate
across all of them.
Measured on one seed it separates where a single opponent did not:

| candidate | score | pass | starter | rancher | heuristic | contrarian |
|---|---|---|---|---|---|---|
| `converter` | 0.100 | 0% | 50% | 0% | 0% | 0% |
| `rancher` | 0.600 | 100% | 100% | 0% | 100% | 0% |
| `contrarian` | 0.800 | 100% | 100% | 100% | 100% | 0% |

It also said something no previous measurement did: **`converter` loses to `pass`**, an agent that
takes no action and banks its $3,000 start.
It is below the do-nothing floor.
The problem is not that it farms badly, it is that it spends itself to $1,352.

`ladder.census` counts actions that changed nothing, by applying each through the environment's own
`_apply_unit_action` against a copy of the farm rather than re-deriving eighteen preconditions --
which is exactly how the no-op HARVEST loop was missed, since any check written from the same
misreading as the agent agrees with the agent.
Validated by reintroducing that bug and confirming the count jumps.
After the two fixes `converter`'s waste is 127 of 4,917 actions.

### Islands, and the axis that actually matters

`scripts/tune_converter.py` is an island ES over converter's dials where **the islands differ by
opponent, not by population**.
Demes facing the same opposition converge to the same place; this file already records a pool that
varied crop mix and nothing else, against which a candidate scored 72% locally and then lost three
ranked matches.
Migration carries a genome that survived one opposition into a population facing another, and it
becomes incumbent only by beating the resident on the resident's own rungs.
Seeds resample every generation and challengers re-confirm on a fresh draw, both because the
experiment log says so.

On memetic search specifically: it has effectively been tried here and the log records the result
-- 11 accepted moves in 14 generations for +1.6%, which is local search hill-climbing the ~15% seed
noise.
Local refinement is the phase that overfits a noisy objective, so it pays only once evaluation is
both cheap and low-variance.

### RL: a second pinned metric, and the bug it was hiding

**`wr` read 0.500 to three decimals for a whole run, and restricting it to `trainable` rows -- the
previous fix for exactly this -- does not unpin it.**
In a self-play group *both* seats are trainable, so both are counted and the pair sums to 1 whatever
either side did.
At `--opponent-frac 0.25` that is two pinned rows per self-play game against one free row per
cross-play game: 86% of the measurement fixed by arithmetic, and a policy winning *every* cross-play
game would have read 0.571.
`tests/test_train_metrics.py` pins that ceiling.

Restricting to cross-play rows then read `nan/0x` -- no qualifying rows at all -- which exposed a
real bug the pinned metric had been hiding.
**A game's index is its phase group, and a phase group is a fixed season position, so index order is
season order.**
`use_opp` took a *contiguous* block, and since episodes only end at the season boundary the games
that terminate are their own contiguous band.
Two blocks rotating at different rates mostly miss: the frozen opponent never played the endgame.
Strided, `wr` populates and moves for the first time -- 0.000/2x, 0.300/5x, 0.312/8x.

### Where to pick up

1. **The livestock phase**, which is where `converter`'s remaining loss lives: animals accumulate
   unplaced in the shed (`COW:6, SHEE:2` on day 25) and 562 PICKUP against 197 FEED.
   The xfail test is already there and strict.
2. **Read the island ES result** in `data/logs/tune_converter.log` and
   `data/tune_converter/best.json` before tuning anything by hand.
3. **Watch `ev_signal` against the committed 0.5 kill criterion.** It is now measurable every
   update and was reading around 0 early.
4. The `contrarian` rung gives 0% to a mirror match, so it cannot distinguish "draws" from "loses
   badly". Other rungs carry the signal, but a margin-aware tiebreak there would sharpen it.

---

## Session 4 — 2026-08-01, afternoon

**v8 submitted** (ref 55159760): the ES-tuned `converter`.
Note v7 came back at **538.4**, below v5's 584.1 and v6's 569.1 -- the agent it replaces was never
our best, and local head-to-head said otherwise.
Local win rate predicts direction, not magnitude. Again.

### The heuristic result

| | ladder (held-out) |
|---|---|
| `converter`, hand-tuned from the replay | **0.092** -- below `pass`, which does nothing |
| `converter`, island-ES tuned | **0.975** |
| `contrarian` (v7) | 0.825 |

On a third seed set the tuned agent beats `contrarian` **87.5% over 16 seat-swapped games,
+$15,010**.
The ES went the *opposite* way to hand-tuning on all three structural dials: herd 20 -> 12,
expand_day 8 -> 3, max_hands 14 -> 17.
Eight rounds of hand-tuning never converged on any of them.

### Two bugs, and two failed fixes worth remembering

Fixed: `yield_units > 0` is not "harvestable" (melon advertises a crop for 10 days before
`first_yield_day` and HARVEST silently returns, so units re-picked a legal no-op forever), and
planting outranked watering (a seed dies overnight unless watered the same day).
WATER over a season went 0 -> 128.

**Failed, and reverted:** an affordability gate on hiring. The diagnosis was right -- 390 HIRE
orders, $45,280 in against $44,258 out, bank at $18 -- but every one of seven configurations scored
at or below the unfixed agent, because `money` is read before the turn's sales settle and the gate
can veto the `min_hands` floor. The fix that works is simply a lower `max_hands`.
**Also failed:** clustering animal ownership by distance from the shed. It cut movement 2,655 ->
2,356 and left the walking *ratio* at 68% either way; 2.1 moves per work action turns out to be
close to inherent for a 10x10 board with a central shed, and my 50% threshold was an assumption.

### RL: it is not broken, it is rationally doing nothing

The op census -- printed every update now -- settled in one line what two of us had been arguing
about from scalars:

```
[ 0] tstd 0.478   ops noop:88%
[ 4] tstd 0.000   ops noop:95%
[ 8] tstd 0.000   ops noop:95%
```

`tstd` is the return spread over rows that actually resolved. At init the random policy acts and
outcomes vary; within four updates it converges to 95% NOOP, and once both sides do nothing every
game draws at $3,000 and the spread is exactly zero.

**The draws are an outcome, not a cause, and the behaviour is rational.** With terminal-only reward,
doing nothing draws (0.5) while acting incompetently loses (0.0). A policy that has not discovered
farming is correct to stand still.

That rules out the tuning fixes: `clip_frac` 0.012-0.083, `seat_sum` 0.997-1.005, `seatL` 0.0000,
entropy stable at 2.5-2.9 with `ent_coef` already raised 6.7x for no effect.
My `--idle-frac` opponent *is* the attractor rather than an escape from it.

**Two corrections I got wrong on the way, both from reading scalars instead of behaviour:**
`ret_std` is taken over every rollout row, and since ~0.14% of rows carry a reward it tracks
`value_mean` and describes the *critic's* spread, not outcomes -- so "std 0.003 means everything
draws" did not follow. And I relayed a review's `clip_frac 0.18-0.33` and climbing `seat_sum` as
live problems when they came from a stale 5-update log predating the day's fixes; the current run
has neither.

**Do not add a prior against NOOP.** Illegal ops are already masked -- `sample_head` applies
`_masked_logits` before sampling, and `unit_op_mask` excludes ops that would do nothing. Forcing
action is the quality-masking anti-pattern `CLAUDE.md` records as an Orbit Wars failure.

### Imitation learning: the data is here

`scripts/fetch_replays.py` pulls from the daily dumps behind
`kaggle/kaggriculture-episodes-index`. 2026-07-31 averages **1427** at the top against our ~600.
**156 replays on disk, 3.1 GB, ~112,000 winner turns**, keeping only episodes whose winner banked
$60k. Best teachers: $128k, $123k, $121k, $121k, $118k.

`kagg/il/replays.py` turns them into supervised pairs. Both seats record a full observation
including `private` -- checked, not assumed. `encode_action` inverts an action dict into head
labels and the round trip through `jax_act.to_sim_actions` is tested, because labels that quietly
mean something else are invisible in a loss curve.

### Optimal execution is worth more than it sounds

`market_price(item, inventory)` is a pure deterministic function and `_process_market` re-quotes
after **every unit**, so selling is a price-impact problem -- Almgren-Chriss, not Black-Scholes,
and easier than either because there is no volatility term. Measured cost of dumping rather than
spreading:

| product | qty | dump | spread | lost |
|---|---|---|---|---|
| MELON | 225 | $26,552 | $56,250 | **$29,698 (53%)** |
| WOOL | 120 | $7,989 | $24,000 | $16,011 (67%) |
| MILK | 120 | $6,225 | $19,200 | $12,975 (68%) |

`contrarian` banks $51k in total. The melon execution loss alone is about $30k.
(The spread column assumes the town fully drains between batches, so it is an optimistic bound --
but the direction is not in doubt.)

### Randomness: there is almost none

Exactly two RNG draws in the whole environment, both from `random.Random((seed * 1_000_003) ^ day)`:
weed spawning at `weedSpawnChance = 0.005` per empty tile per day, and which shop unlocks every
three days. Everything else -- prices, growth, yields, town drain, hire costs -- is deterministic.

So a game is fully reproducible given its seed, which is why parity can be bit-exact; the ~15% seed
variance across games comes from those two draws. **It is not an optimisation problem, and the RNG
is not the reason: it is a two-player game on a shared market.** The dominant uncertainty is the
opponent. That is why mirror sweeps point the wrong way and why a graded ladder worked where
single-opponent tuning did not.

### Next

1. **BC on the 156 replays**, then that checkpoint as PPO init *and* as a frozen JAX opponent
   (which also solves the curriculum problem -- a Python heuristic cannot run inside the scan).
2. **Optimal execution** in `converter`'s sell rule. Biggest measured single number on the board.
3. **FERTILIZE**, which no agent emits. It does not raise melon's ceiling but reaches it in three
   watered days instead of five -- see `tests/test_fertilizer.py`.
4. Watch `noop%` in the op census. Falling means it is learning to act; flat at 95% means it is not.

---

## Session 5 — 2026-08-01, afternoon and evening

**v8 scored 712 Elo.** First submission meaningfully above the 600 start, against v5's 584, v6's
569, v7's 538 and v4's 526.
It is the ES-tuned `converter`; the hand-tuned version of the same agent scored **0.092** on the
local ladder, below an agent that does nothing, so essentially all of +174 came from the search.

That is the day's only ladder movement, and it came from the track that was nearly deprioritised on
the argument that Ender proved RL sufficient without imitation.
Worth remembering the next time a track is called a distraction.

It also gives a second anchor on local -> real, which this project has never had:
`contrarian` 0.825 -> 538, `converter` 0.963 -> 712.
Not a calibration at two points, but the first sign the local ladder tracks *magnitude* and not only
direction.

### The correction that matters most

**"95% NOOP" was mostly a measurement artifact, and it drove most of a day's decisions.**
The op census counted all 24 unit slots while a crew is about **three**, so roughly 88% of the
figure was slots the farm does not own -- NOOP by construction.
Counting owned slots only, real noop is 17-18%.

The bug was in the *diagnostic only*, never the loss: `unit_op_mask` already forces dead slots to a
point mass, so they contributed exactly zero gradient.
Training was never corrupted. The reading was.

It is the same padding mistake found and fixed in the behaviour-cloning loss earlier the same day
and not carried across. **Any rate computed over `MAX_UNITS` is wrong** -- check for others.

### What is actually broken, measured cleanly

On full-season rows, over the first dozen updates:

```
upd   plant   water   harv    crew
  0   5.66%   1.72%   0.00%    3.8
  5   3.17%   1.25%   0.04%    2.8
 12   2.39%   0.74%   0.02%    1.3
```

It plants roughly three times more often than it waters, and an unwatered plant dies in two days --
so it plants and abandons.
A competent agent waters about ten times per plant, so the ratio is inverted by roughly thirty-fold.
This is the identical bug fixed in `converter` this morning, where planting outranked watering; the
difference is that here it has to be learned rather than reordered.

**And the crew is shrinking, which is the policy learning the wrong lesson correctly.** Hands cost
money and it has no productive use for them, so dismissing them is the cheapest way to stop losing.
`wr` creeps up in step. It is converging on "spend nothing", which beats the idle seat's $3,000 and
loses to the farmer's $23,783.
That also means `terminal_ret_std` reaching 0.500 -- the first real win/loss variance all day -- may
be cost discipline rather than crop revenue, and it is worth knowing which before celebrating it.

### Bugs fixed in the training loop

Found mostly by reading Ender's actual source at `github.com/sinking-point/ender` rather than his
write-up, at Alex's insistence. That was the single most productive hour of the session.

- **The KL port was wrong.** He has no separate `kl_coef`: the KL substitutes for entropy *inside*
  the entropy term and shares `entropy_coef`, and heads without a prior keep plain entropy. Our help
  text told the operator to set `--ent-coef 0` alongside a separate `--kl-coef`, which under his
  structure zeroes the KL too. **Two runs therefore had no regulariser at all.**
- **`--kl-anneal` was parsed and never read** -- a dead flag for the one mechanism his write-up
  singles out. It could not have worked anyway: `ent_coef` was captured as a Python float in a
  closure and baked into the compiled graph.
- **`--early-limit 150` truncated before melon could ripen.** There are 24 turns to a day and melon
  yields at day 10 = turn 240. Half the batch reset four days early, structurally incapable of a
  legal HARVEST, and the census aggregated them with full-season rows -- so `harv 0.00%` was part
  policy and part arithmetic. Now 288, and the census reports full-season rows separately.
- **League priority EMA credited each checkpoint with games against other opponents.** Ported his
  `_select_league_opponent` verbatim, then fed it `crossplay`, which is true for the idle, trader
  and farmer seats too.
- Cross-play games were selected as a **contiguous block** of indices, and a game's index is its
  phase, so the frozen opponent never played the endgame and the win rate saw zero qualifying rows.
- Hyperparameters: lr 3e-4 -> **3e-5** (his), ent-coef 0.02 -> 0.01, TF32 on.

### Built

- `kagg/rl/jax_heuristic.py` -- a crop-economy farmer in pure array ops that **banks $23,783** and
  runs natively inside the compiled scan. `contrarian` and `converter` cannot: they are Python
  agents over dict observations. I had called that impossible; it is not, `jax.pure_callback` exists,
  it is merely expensive. This was the cheaper route.
- Three scripted opponents forming a ladder: idle $3,000, wheat trader $3,368, farmer $23,783.
  The trader matters because our null action is a *stable* $3,000 where Ender's game punished
  standing still on its own -- his recipe was never going to be sufficient here unaided.
- Autoregressive market decode: `sell`/`buy_product` emit one slice per coarse trade mode, sampled
  first, so `p(trade) * prod_i p(product_i | trade)` is exact rather than mean-field. Fixes an agent
  that emitted **zero** market orders under argmax (nine "probably not sell" marginals composing
  into "never") and banked $1 under independent sampling.
- Early-game envs, league priority sampling, `tests/test_jax_act.py` pinning that `evaluate`
  reproduces `sample`'s log-prob.

### The BC track, parked

Gate failed: `P(noop)` at spawn 0.9920 against a 0.98 bar, and the checkpoint banks **$0**.
DAgger moved the marginal nearly an order of magnitude and the agent does now move, but the
corrective labels were 96.7% non-noop and **entirely WEST and NORTH** -- the learner never leaves
spawn, so `converter` never demonstrates anything else.
The directional check flagged an identical favoured op on all five seeds.

The checkpoint reproduces its teachers closely on *teacher* states at day 0 and day 4 alike,
including their idle turns. It plays well from a state a good player produced and cannot produce
one. Ordinary covariate shift.

### Where to pick up

1. **Read the run.** Gate is `water` overtaking `plant` and `harv` leaving zero, on full-season rows.
   At update 12 both were still falling. If that holds at 50, more compute will not reverse it.
2. **The heuristic track is where the points are.** 712 with the livestock half of `converter` still
   broken -- 562 PICKUP against 197 FEED, animals accumulating unplaced. The ES has an obvious next
   run once that is fixed.
3. **Optimal execution** remains the largest single measured number on the board: ~$30k of
   `contrarian`'s $51k lost to price impact on melon alone.
4. **`--init` still does not exist.** `train_jax_rl.py` has `--resume` (a PPO checkpoint) and random
   init, and nothing that warm-starts from BC. It was written up as plan item 1 twice and never
   wired.
5. GPU runs at **84-90 C** and throttles: 646 t/s early, 150-180 t/s sustained. Plan timings on the
   throttled rate. `--minibatch-size 1024` dies with a real OOM; 512 fits.

### Landed after the session-5 writeup — read this before starting the RL

Three more fixes, and **the training run on the box is stale**: it was started before the last two
and is still using the old observation.
**Restart it before reading anything into its numbers.**

```
kagg-train --batch 256 --horizon 32 --updates 4000 --minibatch-size 512 --epochs 2 \
  --n-phases 256 --opponent-frac 0.15 --idle-frac 0.05 --trade-frac 0.15 --farm-frac 0.30 \
  --early-limit 288 --seat-coef 1.0 --ent-coef 0.01 --lr 3e-5 --pool-every 50 --ckpt-every 50
```

**1. The trader opponent was in 0% of games.**
Each opponent type picked its own strided set of indices and dropped any another type had claimed.
The strides share residue classes -- the farmer lands on `it + 2 (mod 3)` and every trader pick
`j*6 + it + 2` is in that same class -- so **every** trader pick collided and was filtered out.
Measured against what was asked: pool 15 -> 14.8%, farmer 30 -> 30.1%, trader 15 -> **0.0%**,
idle 5 -> 2.7%, self-play 35 -> **52.3%**.
The trader is the seat that exists *because* it banks $3,368 and so cannot draw with a passive
policy -- the entire point of it -- and it had never appeared in a game.
Now one rotating partition, so shares are exact and collisions impossible.

**2. Two claims in the session-5 writeup above are wrong, corrected here rather than edited out.**

- *"The crew is shrinking, which is the policy learning cost discipline."* **There is no dismiss
  action.** `jax_sim._end_of_day` does `n_units=jnp.ones_like(...)` -- the engine resets the crew to
  one every night unconditionally. What is falling is the *hire* rate, and it is a vicious circle,
  not discipline: fewer units means fewer chances to stumble into a completed maintenance loop,
  which means less evidence that hiring pays, which means hiring less. Real winners run crews of
  10-17 banking $50k-$110k. 1.3 is a collapse to the cheapest thing that does not lose -- the same
  shape as the noop finding one level up.
- *"It builds pastures twice as often as it plants."* Partly a confound: `BUILD_PASTURE` and
  `BUILD_COOP` are masked only on `kind == EMPTY` with **no cost check at all**, while `PLANT`
  requires a seed already bought. `PLACE` is the clean comparison -- it is *more* gated than PLANT
  and still fires at a third of its rate, while water/care/feed are an order of magnitude rarer
  again. The setup-versus-maintenance split survives; that one comparison did not support it.

**3. Each unit now gets the direction to its nearest job** (`kagg/rl/jax_obs.py`).
Four targets -- nearest tile needing water, nearest ripe tile, nearest unfed animal, nearest free
tile -- each as signed dx, dy and an inverted distance, so "nothing to do" and "very far" both read
near zero while a job underfoot reads one. Unit features 16 -> 28.

The reasoning, which is the transferable part: **precompute the geometric fact rather than making
the network derive it through reward.** `jax_obs.py` already does this ("Age drives every yield
rule, so give it directly rather than making the net subtract"), and Ender's entire target-selection
pipeline is built on it -- he precomputes orbital intercept geometry and hands it to the policy
rather than teaching a transformer orbital mechanics from raw positions. Ours is the trivial version:
Manhattan distance on a static 10x10 grid.
It is a fact, not a quality judgment -- it says where the nearest dry plant is, not that watering is
what the unit should do, so it stays the right side of `CLAUDE.md`'s line about masking to *force*
an action.

**This changes the observation width, so existing checkpoints will not load.** Acceptable: the BC
track is parked and the run it invalidates was 20 updates old.

**The cheap falsification test to run first, before trusting the feature:** does the policy's action
distribution shift toward WATER when a unit is adjacent to a dry tile versus far from one? If it
shifts, the problem was the length of the walk and this feature is the right lever. If it does not
shift even when adjacent, something more basic is wrong and the feature is fixing the wrong thing.

### The state of the RL, honestly

Every run so far converges toward *less* activity, not more. Latest, on full-season rows:
plant 5.66% -> 2.39%, water 1.72% -> 0.74%, harvest never leaving ~0.02%, hire rate collapsing.
It is not paralysed and it is not failing to explore -- it tries seventeen of eighteen ops. It does
setup and skips maintenance, in **both** economies: 4,591 animals placed against 12 fed, 13,439
crops planted against 98 harvested.

Fable's read, which I agree with: this is an exploration base-rate problem convolved with credit
assignment, not a horizon problem. Gamma handles the horizon fine. The issue is that completing a
maintenance loop needs several correct movement steps followed by the right op on arrival, repeated
across days, with the reward arriving 8-12 days later -- and with 98 successes in 413k actions there
is essentially no completed trajectory in the data for the critic to learn from.

**Do not just let it run longer without landing a change first.** The direction is currently away
from activity and the hire collapse is self-reinforcing, so more hours will tighten a dead end
rather than escape it. The geometry feature is that change; run the ~19-update owned-unit census
again and see whether water and harvest move at all before committing hours.
