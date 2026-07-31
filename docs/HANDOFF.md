# Handoff — 2026-07-31, end of day 1

Read `CLAUDE.md` first (rules and the "Lessons learned the hard way" list), then
`docs/experiment_log.md` (every experiment, its score, what it taught).
This file is the short version of where things stand and what to do next.

## The single most important thing

**The vectorized simulator is NOT parity-exact under hiring. Do not train on it yet.**

| case | status |
|---|---|
| one unit per player | 60/60 full-length episodes exact |
| several units, no hiring | 6/6 exact |
| **with hiring** | **8/12 — broken** |

This blocks offline search, imitation learning and any per-turn RL policy, because all three
depend on the simulator being right.

`CLAUDE.md` made end-to-end parity a hard gate and the gate was passed — but `parity.py` hard-coded
`n_units = 1`, so it never drove more than one unit per player.
Two real divergences hid behind that and were found by a *search agent using* the sim, not by the
gate testing it:

- **Atomic PLANT.** The reference drops **every** PLANT request for a crop when the total exceeds
  seeds held. The sim spent seeds greedily unit by unit. With one unit the two rules are identical.
- **Hand spawning.** The reference puts each hand on the least-occupied shed-access tile (ties
  NWSE). The sim put every hand on NW, and this was written up as an acceptable approximation. It
  was not: a hand standing elsewhere takes different actions, so money diverged within a few
  hundred steps of the first hire. Porting the real rule moved hiring parity from 0/12 to 8/12.

**Prime suspect for the remaining gap:** the reference pairs the players' *i-th market order*,
while `kagg/sim/game.py::_process_market` settles per product with the players alternating. These
agree only when both players put the same product in the same order slot.

Reproduce with:

```python
from kagg.sim.parity import random_script, run_reference, run_sim, compare
import numpy as np
rng = np.random.default_rng(4242)
script = random_script(rng, steps=719, max_units=6, allow_hire=True)
ref, unlocks = run_reference(script, seed=1500)
sim = run_sim([script], unlocks=unlocks)[0]
print(compare(sim[:len(ref)], ref))
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

1. **Close the sim parity gap under hiring** (task 9). Blocks everything downstream.
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
