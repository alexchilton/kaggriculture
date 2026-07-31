# Kaggriculture

Agent for the Kaggle [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture)
competition. Featured, $50k, deadline **2026-09-30**.

Two-player farming sim, 720 turns, most money in the bank wins.

## Status

**2026-07-31 — v5 submitted. 72% win rate against a five-strategy opponent pool.**

v4 scored $43.5k locally and then **lost on the ladder at 429.9**, because it had been tuned
against `starter`, which does not compete for market prices. v5 is tuned against an opponent pool
and selected on win rate. See `docs/experiment_log.md` — that failure is the most useful thing
this project has learned so far.

`kagg/arena/` runs seat-swapped matches, `kagg/economics/` models the market and per-tile
production with exact live-env parity, `kagg/agents/` holds the playable agent. 42 tests pass.
Full history of what was tried and what it scored: `docs/experiment_log.md`.

**Leaderboard scoring is Elo (~1100-1400), not money.** Winning matters; margin does not.

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
kagg/arena/       seat-swapped match running -- the measurement tool
kagg/economics/   offline market and production models, parity-tested
kagg/agents/      playable agents
kagg/sim/         vectorized simulator (skeleton only)
scripts/          benchmarks, analyses, the tuner, the submission builder
submission/       generated; build with scripts/build_submission.py
docs/             findings and decisions
reference/        competition docs and the full env source (ground truth)
data/             git-ignored scratch for replays and checkpoints
```

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
8. **Build the numpy-batched sim and its parity harness.** Not started beyond a package skeleton.
   Required for offline search, IL and PPO. JAX after parity is green, not before.

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