# Kaggriculture

Agent for the Kaggle [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture)
competition. Featured, $50k, deadline **2026-09-30**.

Two-player farming sim, 720 turns, most money in the bank wins.

## Status

**2026-08-31, and this is where the work stopped.**

What ships is a **tape replayer**, not a planner. `REPLAY_OPENING_DAYS = tuple(range(30))`
(`kagg/search/schedule_agent.py:3919`) replays a recorded human player's actions for all 30 days,
choosing between four recordings on two closed-loop bits — whether the opponent holds 9+ melon
tiles at day 3, and whether the yarn store is open by day 5. The planner
(`kagg/search/cover.py`) still runs every turn, and its answer is discarded.

Measured against 24 recorded ladder opponents, both seatings, 576 games, replicated on two seed
ranges:

| arm | win rate | mean ours | mean theirs |
|---|---|---|---|
| tape (`range:30`, ships) | **95.5%** | 99,288 | 65,988 |
| planner (`range:0`) | 82.3% | 97,881 | 76,374 |

It wins by **suppressing the opponent**, not by earning more: our own money moves +$1,407 between
arms while theirs drops −$10,386. That is why an idle-opponent measurement inverts the answer —
and it did, reading the planner $15,483 *ahead*. Never evaluate this agent against an idle or
non-selling opponent.

**Leaderboard scoring is Elo, starting at 600.** Winning matters; margin does not.

### The learned track is closed

Behaviour cloning of the tape agent reproduces it exactly *with the teacher driving* — 1.0000
unit-op agreement on 64 towns across all four latch arms, and 8 of 13 unseen towns exact
op-for-op through day 11. Driving itself under sampling it banks a median **$16**.

The gap is not confidence (geometric-mean p(teacher action) is 0.99958); it is distribution shift.
DAgger cannot close it, because the teacher is time-indexed `TAPE[key][step]` and answers "at turn
t do X" for a board the student is no longer standing on. PPO cannot start from it, because at
update 0 — before any gradient step — the sampled policy already banks $16.

Read `docs/fable_after_the_bc_ceiling_2026-08-31.md` for the decision and
`docs/tape_arm_and_first_tape_sweep_2026-08-31.md` for the measurements behind it.

The numpy port (`kagg/rl/numpy_obs.py`, `numpy_act.py`, `kagg/agents/numpy_neural.py`) is finished
and pinned exact against the jax path, so a net *can* ship with no jax or flax. Nothing currently
needs it.

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
| `docs/the_field.md` | What the opponents actually do, measured from replays |
| `docs/what_kind_of_problem_this_is.md` | The problem class, and what each clause rules out |
| `docs/rl_feasibility.md` | The RL track: what it measured, and why it is parked |
| `docs/throughput_measurements.md` | **Measured** env throughput |

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
   See `docs/throughput_measurements.md`.

## Layout

```
kagg/search/      the shipping agent: cover.py (day planner), schedule_agent.py (executor),
                  router.py (which jobs the board offers), routines.py
kagg/arena/       match running, and the opponent pool -- the measurement tools
kagg/economics/   offline market and production models, parity-tested
kagg/agents/      hand-written agents, used as sparring partners and pool members
kagg/rl/          the parked RL track
kagg/sim/         batched simulator (numpy + JAX), 30-200x, end-to-end parity exact
scripts/          benchmarks, analyses, probes, submission builders
submission/       generated; build with scripts/build_planner_submission.py
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