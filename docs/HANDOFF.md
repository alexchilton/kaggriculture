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
