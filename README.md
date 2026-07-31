# Kaggriculture

Agent for the Kaggle [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture)
competition. Featured, $50k, deadline **2026-09-30**.

Two-player farming sim, 720 turns, most money in the bank wins.

## Status

**2026-07-31 — v5 on the ladder at 555. PPO training overnight on the real env.**

v4 scored $43.5k locally and then **lost on the ladder at 429.9**, because it had been tuned
against `starter`, which does not compete for market prices. v5 is tuned against an eight-strategy
opponent pool — three of them copied from agents that actually beat us — and selected on **win
rate**, since the ladder is Elo. See `docs/experiment_log.md`; that failure is the most useful
thing this project has learned so far.

Ladder: **v5 at 613.5**, against a 600 start and a field top of ~1400. v4, tuned against
`starter`, scored 526.4 -- below the start. v6 is submitted and still converging.

`kagg/arena/` runs seat-swapped matches, `kagg/economics/` models the market and per-tile
production with exact live-env parity, `kagg/agents/` holds the playable agent. 42 tests pass.
Full history of what was tried and what it scored: `docs/experiment_log.md`.

**Leaderboard scoring is Elo, starting at 600.** Winning matters; margin does not.

## Start here

Read in this order:

| File | What it is |
|---|---|
| `CLAUDE.md` | Project rules, kill criteria, settled decisions |
| `docs/competition_brief.md` | The competition, measured facts, deadlines, API |
| `docs/rl_feasibility.md` | Why MaskablePPO + entity transformer, and the reward argument |
| `docs/lessons_carried_over.md` | Orbit Wars post-mortem, distilled |
| `docs/experiment_log.md` | **Every experiment, its score, and what it taught. Start here.** |
| `docs/economics_q5_findings.md` | **Measured** economics: yields, drain, sell timing |
| `docs/throughput_measurements.md` | **Measured** env throughput, and why the vectorized sim is mandatory |
| `docs/economics_analysis.md` | Day-1 hypotheses. Its revenue-per-tile table is **wrong** — see above |
| `docs/superpowers/specs/2026-07-31-kaggriculture-agent-design.md` | The design |

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
kagg/arena/       match running, and the opponent pool -- the measurement tools
kagg/economics/   offline market and production models, parity-tested
kagg/agents/      playable agents (heuristic.py is the current submission)
kagg/rl/          Gymnasium env: one strategy decision per day, terminal win/loss reward
kagg/sim/         numpy-batched simulator -- 1,032x, end-to-end parity exact
scripts/          benchmarks, analyses, tuner, RL training, submission builder
submission/       generated; build with scripts/build_submission.py
docs/             findings and decisions -- experiment_log.md first
reference/        competition docs and the full env source (ground truth)
data/             git-ignored scratch for replays, RL runs, checkpoints
```

## Measuring an agent

**Never evaluate against `starter` alone** — it does not sell, so the market is never contested and
every number comes out about 2x reality. That mistake cost a submission.

```python
from kagg.arena import evaluate
from kagg.agents import heuristic
print(evaluate(dict(heuristic.PARAMS), seeds=range(20)))   # 8 competing strategies, win rate
```

## Training

```bash
.venv/bin/python scripts/train_rl.py --steps 6000000 --envs 10 --tag overnight
tail -f data/rl_runs/overnight.log
tail -5 data/rl_runs/overnight-*/progress.csv
.venv/bin/tensorboard --logdir data/rl_runs
```

The policy sets strategy once a day, so episodes are 30 steps rather than 720. That is what makes
a **terminal win/loss reward** practical, and it is why RL can train on the real environment before
the fast simulator exists. Watch `train/explained_variance` — below 0.5 means the frame is wrong,
not the hyperparameters. `ret=0.00 +/- 0.00` means reward is not reaching the algorithm at all.

## Next actions

1. ~~Build `kagg/arena/`~~ **done** — fixed seeds, multiprocess, absolute money delta.
2. ~~Answer verification question 5~~ **done** — `docs/economics_q5_findings.md`.
   Neither "wheat volume" nor "premium timing": pick crops on measured yields, which are ~10x
   below what the day-1 table claimed, and sell late where storage allows (worth 1.14x-1.26x --
   an earlier 1.75x figure assumed storage the shed does not have).
3. ~~Charge routing cost against each crop~~ **dropped** — it falls out of the heuristic agent
   running in the arena, so a standalone model was redundant.
4. ~~Heuristic agent, then a first leaderboard submission~~ **done** — v4, submitted.
5. ~~Add animals and fertilizer~~ **built and switched off** — measured net negative because of
   routing cost. Revisit with animals placed on shed-access tiles, which removes the feed walk.
6. **Beat `melon_heavy`.** The one matchup v5 still loses (30%). Likely needs deferred selling so
   melon is not dumped into a market the opponent has already flooded.
7. ~~Opponent pool~~ **done** — `kagg.arena.evaluate`, five frozen competing strategies.
8. ~~Build the numpy-batched sim and its parity harness~~ **done** — 499k steps/sec (1,032x),
   60/60 full-length episodes exact. Unlocks offline search, IL, and a per-turn PPO policy.
9. **Use it**: offline search over action schedules, then imitation from the resulting teacher.
   This is the path past the heuristic's ceiling. JAX only if profiling says the env is still the
   bottleneck with a policy in the loop.

## Setup

```bash
pip install -U "kaggle-environments>=1.32.2"   # earlier versions lack the kaggriculture env
```

Training runs on the Windows box (RTX 3080 Laptop 16GB, WSL2) — see `CLAUDE.md`,
including the warning about not using the vLLM venv.

## Open questions

- JAX versus numpy-batched for the vectorized sim. Decide by measurement; see the design doc.
- Can a 150-unit melon harvest wave clear a 100-item shed inside one day? Until this is
  answered the melon revenue figure is an upper bound, not a plan.

Measured 2026-07-31: training box has **16 cores and 13 GB RAM** available to WSL2.