# Kaggriculture

Agent for the Kaggle [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture)
competition. Featured, $50k, deadline **2026-09-30**.

Two-player farming sim, 720 turns, most money in the bank wins.

## What this is

A record of nine approaches to one problem, the measurement that settled each, and the one that
ships. Work stopped **2026-08-31**.

The interesting content is not the winner. It is that most of these were closed by a number that
contradicted the plan which produced them, and both the code and the contradicting measurement are
still here.

**Leaderboard scoring is Elo, starting at 600.** Winning matters; margin does not — which is why
every verdict below is a win rate and not a bank.

## The approaches

| # | Approach | Where | How it ended |
|---|---|---|---|
| 1 | **Hand-written heuristic** | `kagg/agents/heuristic.py` | Baseline and sparring partner. Still the opponent pool. |
| 2 | **Covering day planner** — plan the whole day at dawn from the live board, one plan, no replan | `kagg/search/cover.py`, `kagg/search/dayplan.py`, `kagg/search/router.py` | Works, and is beaten by the tape (82.3% vs 95.5%). Still runs every turn under the shipped agent. |
| 3 | **Offline route solver** — solve each day's tour once, ship the routes as tables | `scripts/solve_day_offline.py`, `scripts/resolve_days.py` | Solved routes ship as 179 KB of precomputed tables. The solver never runs at play time. |
| 4 | **CEM over crop allocation** | `kagg/search/cem.py`, `scripts/cem_allocation.py` | Taught the lesson that a fixed 3-seed objective reports +40% where held-out seeds say +12.8%. |
| 5 | **Chain / beam search over day plans** | `kagg/search/chains.py`, `kagg/search/chain_mutate.py`, `scripts/beam_chains.py` | Superseded by replaying a human who already solved it better. |
| 6 | **Behaviour cloning** of a recorded top player | `kagg/il/`, `scripts/bc_replay.py` | Reproduces the teacher exactly *with the teacher driving* — 1.0000 unit-op agreement on 64 towns, all four latch arms, 8 of 13 unseen towns exact through d11. Banks a median **$16** driving itself. |
| 7 | **DAgger** from the shipped agent as teacher | `kagg/il/tape_teacher.py`, `scripts/dagger_tape.py` | **Cannot work here, by construction.** The teacher is time-indexed `TAPE[key][step]`, so it answers "at turn t do X" for a board the student is no longer standing on. |
| 8 | **PPO**, terminal reward, on a vectorised JAX sim | `kagg/rl/`, `kagg/sim/jax_sim.py`, `scripts/train_jax_rl.py` | Cannot start from the clone: at update 0, before any gradient step, the sampled policy banks $16 and clips 100%. Sim parity is exact — 300/300 full-length episodes. |
| 9 | **Tape replay with two closed-loop latches** | `kagg/search/schedule_agent.py:3919` | **Ships.** 95.5% win rate. |

Two pieces of machinery are worth more than the approaches that motivated them:

- **The market-bundle vocabulary** (`kagg/il/market_bundles.py`) collapses nine correlated order
  heads into one categorical. Nine independent "probably don't sell" decisions compose into "never
  sell", so the joint decode was destroying information the marginals had.
- **The numpy port** (`kagg/rl/numpy_obs.py`, `kagg/rl/numpy_act.py`, `kagg/agents/numpy_neural.py`)
  reimplements the observation encoder, the action masks and the policy exactly, pinned against the
  jax path by four test files, so a trained net ships in one file with no jax and no flax.

## What ships, and the measurement behind it

`REPLAY_OPENING_DAYS = tuple(range(30))` replays a recorded human player's actions for all 30 days,
choosing between four recordings on two bits read from the live board: whether the opponent holds
9+ melon tiles at day 3, and whether the yarn store is open by day 5.

Against 24 recorded ladder opponents, both seatings, 576 games, replicated on two seed ranges:

| arm | win rate | mean ours | mean theirs |
|---|---|---|---|
| tape (ships) | **95.5%** | 99,288 | 65,988 |
| planner | 82.3% | 97,881 | 76,374 |

It wins by **suppressing the opponent**, not by earning more: our own money moves +$1,407 between
arms while theirs drops −$10,386. That is why an idle-opponent measurement inverts the answer — and
it did, reading the planner $15,483 *ahead*. Never evaluate this agent against a non-selling
opponent.

`docs/fable_after_the_bc_ceiling_2026-08-31.md` is the decision;
`docs/tape_arm_and_first_tape_sweep_2026-08-31.md` has the measurements, including the one that
found a $3,402 gap the plan had been built on did not exist.

## Start here

**Resuming after a break? Read `docs/README.md`** — it indexes what survived the 2026-08-08 docs
consolidation and says where everything else went.

Then, in this order:

| File | What it is |
|---|---|
| `CLAUDE.md` | Project rules, kill criteria, settled decisions |
| `docs/competition_brief.md` | The competition, measured facts, deadlines, and the env rules that have each cost a day |
| `docs/architecture.md` | **What the agent actually is**, and the flags that ship off with their numbers |
| `docs/REGISTER.md` | The live open/closed list |
| `docs/experiment_log.md` | **Every experiment, its score, and what it taught** |
| `docs/economics_q5_findings.md` | **Measured** economics: yields, drain, allocation, selling |
| `docs/rl_feasibility.md` | The RL track: what it measured, and why it is parked |

`reference/` holds the competition docs and the **full environment source**.
`reference/kaggriculture.py` is ground truth for every rule question — read it rather than
guessing, and trust it over the README where they disagree.

## The three facts that matter most

1. **The bar is on the floor.** The built-in `starter` baseline, which most competitors will
   fork, finishes on **$3512 from a $3000 start** — $512 profit over a whole season.
2. **No *per-turn* online search.** `actTimeout` is 1 second per turn, with **60 seconds** banked
   for the whole episode (the source says 60; an earlier note said 12). Not enough for MCTS at
   every one of 720 turns, but enough for a planning burst at turn 0.
3. **Env throughput is the bottleneck, and worse than first recorded.**
   The training box does **484 steps/sec** single-threaded and **4,221** across 16 workers —
   the earlier 1163 figure was a dev-Mac rate and is 2.4x optimistic.
   10B env steps, which is what competitive runs in the comparable previous competition used,
   would take **27 days**. The vectorized sim is required, not optional.

## Layout

```
kagg/search/      the shipping agent: cover.py (day planner), schedule_agent.py (executor),
                  router.py (which jobs the board offers), routines.py
kagg/arena/       match running, and the opponent pool -- the measurement tools
kagg/economics/   offline market and production models, parity-tested
kagg/agents/      hand-written agents, used as sparring partners and pool members
kagg/il/          imitation: the tape teacher, replay loading, and the market-bundle
                  vocabulary that turns nine correlated order heads into one categorical
kagg/rl/          the policy (flax transformer, 965,711 params), its observation encoder
                  and action masks -- AND an exact numpy reimplementation of all three,
                  so a trained net can ship in one file with no jax and no flax
kagg/sim/         batched simulator (numpy + JAX), 30-200x, end-to-end parity exact
scripts/          benchmarks, analyses, probes, submission builders. Each is named as the
                  question it answers, and holds the answer in its module docstring
submission/       generated, and not tracked -- see submission/README.md
docs/             findings and decisions -- docs/README.md is the index
reference/        competition docs and the full env source (ground truth)
data/             git-ignored scratch for replays, runs, checkpoints, logs
```

## Measuring an agent

**Never evaluate against `starter` alone** — it does not sell, so the market is never contested and
every number comes out about 2x reality. That mistake cost a submission.

```python
from kagg.arena import evaluate
from kagg.agents import heuristic
print(evaluate(dict(heuristic.PARAMS), seeds=range(20)))   # 8 competing strategies, win rate
```

## The metric that counts

Day-by-day, field-by-field, against a reference tape:

```bash
python -u scripts/breakdown.py --tape seb --seed 11 --weeds 0.0 --days 30 --diff --no-moves
```

Judge a fix **at the day it targets**, never on the season total — the `money` row is an area, not
a deficit. Market rows are fills; everything else is offers. See `docs/architecture.md` for the
harness caveats, every one of which has mis-scored an arm at least once.

## What is open

`docs/REGISTER.md`. The largest open defect is that animal produce rides in a unit's hand all day
and only reaches the shed via the overnight sweep, so we sell yesterday's production.

## Setup

```bash
pip install -U "kaggle-environments>=1.32.2"   # earlier versions lack the kaggriculture env
```

Training runs on the Windows box (RTX 3080 Laptop 16GB, WSL2) — see `CLAUDE.md`,
including the warning about not using the vLLM venv.

Measured 2026-07-31: training box has **16 cores and 13 GB RAM** available to WSL2.