# Kaggriculture

Agent for the Kaggle [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture)
competition. Featured, $50k, deadline **2026-09-30**.

Two-player farming sim, 720 turns, most money in the bank wins.

## Status

**2026-07-31 — design complete, no code written yet.**

## Start here

Read in this order:

| File | What it is |
|---|---|
| `CLAUDE.md` | Project rules, kill criteria, settled decisions |
| `docs/competition_brief.md` | The competition, measured facts, deadlines, API |
| `docs/rl_feasibility.md` | Why MaskablePPO + entity transformer, and the reward argument |
| `docs/lessons_carried_over.md` | Orbit Wars post-mortem, distilled |
| `docs/economics_analysis.md` | Where the money is (day-1 hypotheses, unverified) |
| `docs/superpowers/specs/2026-07-31-kaggriculture-agent-design.md` | The design |

`reference/` holds the competition docs and the **full environment source**.
`reference/kaggriculture.py` is ground truth for every rule question — read it rather than
guessing, and trust it over the README where they disagree.

## The three facts that matter most

1. **The bar is on the floor.** The built-in `starter` baseline, which most competitors will
   fork, finishes on **$3512 from a $3000 start** — $512 profit over a whole season.
2. **No online search is possible.** `actTimeout` is 1 second per turn with only 12 seconds
   banked for the entire episode. Everything expensive must happen offline.
3. **Env throughput is the bottleneck.** 1163 steps/sec single-threaded Python.
   Hence the vectorized sim.

## Next actions

1. Build `kagg/arena/` — fixed seeds, multiprocess, absolute money delta. **Before any agent.**
2. Answer verification question 5 in `docs/economics_analysis.md`: does town drain exceed
   player supply for premium goods? This decides "wheat volume" versus "premium timing"
   and is the highest-value unknown in the project.
3. Build the vectorized sim and its parity harness.

## Setup

```bash
pip install -U "kaggle-environments>=1.32.2"   # earlier versions lack the kaggriculture env
```

Training runs on the Windows box (RTX 3080 Laptop 16GB, WSL2) — see `CLAUDE.md`,
including the warning about not using the vLLM venv.

## Open questions

- CPU core count and system RAM on the training box — box was powered off on 2026-07-31.
- JAX versus numpy-batched for the vectorized sim. Decide by measurement; see the design doc.