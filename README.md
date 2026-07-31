# Kaggriculture

Agent for the Kaggle [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture)
competition. Featured, $50k, deadline **2026-09-30**.

Two-player farming sim, 720 turns, most money in the bank wins.

## Status

**2026-07-31 — arena built, economics question 5 answered, no agent yet.**

`kagg/arena/` runs seat-swapped matches. `kagg/economics/` models the market and per-tile
production, validated step-for-step against live episodes. 32 tests pass.

## Start here

Read in this order:

| File | What it is |
|---|---|
| `CLAUDE.md` | Project rules, kill criteria, settled decisions |
| `docs/competition_brief.md` | The competition, measured facts, deadlines, API |
| `docs/rl_feasibility.md` | Why MaskablePPO + entity transformer, and the reward argument |
| `docs/lessons_carried_over.md` | Orbit Wars post-mortem, distilled |
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
2. **No online search is possible.** `actTimeout` is 1 second per turn with only 12 seconds
   banked for the entire episode. Everything expensive must happen offline.
3. **Env throughput is the bottleneck, and worse than first recorded.**
   The training box does **484 steps/sec** single-threaded and **4,221** across 16 workers —
   the earlier 1163 figure was a dev-Mac rate and is 2.4x optimistic.
   10B env steps, which is what competitive runs in the comparable previous competition used,
   would take **27 days**. The vectorized sim is required, not optional.
   See `docs/throughput_measurements.md`.

## Next actions

1. ~~Build `kagg/arena/`~~ **done** — fixed seeds, multiprocess, absolute money delta.
2. ~~Answer verification question 5~~ **done** — `docs/economics_q5_findings.md`.
   Neither "wheat volume" nor "premium timing": sell *late* (worth 1.16x-1.75x on every crop)
   and pick crops on measured yields, which are ~10x below what the day-1 table claimed.
3. **Charge routing cost against each crop** (old question 3). Every revenue figure in the
   findings doc assumes the harvest gets harvested; movement is an action and units only act on
   the tile they stand on. This is now the highest-value unknown.
4. Heuristic agent, then a first leaderboard submission.
5. Build the vectorized sim and its parity harness.

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