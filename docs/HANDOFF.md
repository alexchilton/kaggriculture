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
