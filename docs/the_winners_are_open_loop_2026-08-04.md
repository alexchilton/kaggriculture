# The winning agents are fixed 720-turn scripts. They do not react to anything.

2026-08-04. Measured directly from six leaderboard replays in `data/episodes/`.
Script: `scratchpad/split_farm_vs_market.py`, log: `data/logs/split_farm_vs_market.log`.

## The measurement

For each player appearing in more than one replay, every turn's action was split into
`units` (the `farmer` + `hands` unit ops) and `market` (the trading orders), and compared
turn-by-turn between episodes.

```
senkin13        4 episodes, 6 pairwise comparisons, different opponents AND swapped seats
                units  identical 720/720  (100.0%)  in all six comparisons
                market identical 720/720  (100.0%)  in all six comparisons
                banks $121,538 - $145,034

syouya tobita   4 episodes, 6 pairwise comparisons
                units  identical 720/720        (100.0%)  in all six
                market identical 716-720/720    ( 99.4-100.0%)

Dmitry Larko    2 episodes
                units  identical 701/720  (97.4%)
                market identical 689/720  (95.7%)
```

Day-to-day repetition within a single season, all five players measured:

```
distinct daily unit-routines: 30/30      (every player, every episode)
```

## What it establishes

**`senkin13` submits a byte-identical 720-turn action sequence regardless of opponent, regardless of
seat, and banks $121k-$145k with it.**
Episode 89544610 has the seats swapped relative to the other three and the script is still identical,
so it does not even condition on which seat it holds.

The winning solution is therefore an **open-loop trajectory**, not a policy.
Nothing is being observed and reacted to.

Two design questions are closed by this:

- **No opponent model, and no market policy.** The market was the plausible place reactivity would
  pay, since both players' sells move the same prices. It does not: `senkin13` diverges on zero
  market turns across six comparisons, `syouya tobita` on at most four of 720. Reactivity is worth
  approximately nothing at the top of this leaderboard.
- **The action space is the full 720-turn sequence, not a repeated daily routine.**
  Every player shows 30/30 distinct daily unit-routines, so no two days are byte-identical. There is
  seasonal phase structure (planting, growth, harvest), but a "one routine, repeated" parameterisation
  cannot express what the winners play.

## Why this reframes everything done so far

Both tracks in this project have been optimising *parameters of hand-written heuristics* rather than
the action sequence:

- The CEM track searches 283 genes that `kagg/search/executor.py` then interprets, so the ceiling is
  the executor's expressiveness, not the search. When livestock failed it was because the 9-step
  animal chain was hand-coded and wrong (`docs/executor_livestock_broken_2026-08-04.md`).
- The RL track trains a reactive per-turn policy, paying the full cost of credit assignment over 719
  steps with one bit of terminal reward, to learn a behaviour that the evidence says needs no
  reactivity at all.

`CLAUDE.md` already warned about the first of these:
"A heuristic agent is a teacher and a sparring partner, never the final policy. This is the correction
to the Orbit Wars failure where heuristics became the policy and capped the ceiling."

Under direct trajectory optimisation, the problems both tracks have been fighting do not exist:

| Fought | Why it existed | Under trajectory optimisation |
|---|---|---|
| Credit assignment over 719 steps | RL must infer which action mattered | Exact: perturb a turn, measure the delta |
| Reward on ~11 of 8,192 rows | Terminal-only PPO | Objective evaluated exactly per rollout |
| Entropy vs. objective | Exploration proxy | No entropy term exists |
| 9 uncorrelated heads cannot form a chain | Factored policy marginals | The chain is written into the sequence |
| `ev_signal`, GAE, value margin, shaping | Critic machinery | No critic |

The livestock chain stops being something that must be hand-coded correctly. It is nine actions in a
row that the optimiser either finds profitable or does not.

## The immediate consequence: we hold a $145k script

`senkin13`'s exact 720-turn sequence is in `data/episodes/89541819.json`. That makes the next step
cheap and high-information:

1. Extract the sequence and replay it through our own simulator.
2. If it reproduces ~$145k, that is an **end-to-end economic validation** far stronger than the
   action-level parity gate -- and it specifically exercises the livestock economy, since ~35% of
   that revenue is milk and wool.
3. If it does not reproduce, the divergence localises a simulator bug against a known ground truth,
   which is the strongest debugging signal available in this project.
4. Either way the result is a **$145k starting point** for optimisation, against our own best
   measured $28,168.

## Caveats

- The board is identical every game, but weeds and shop unlock order are RNG. `senkin13` being
  720/720 identical across four episodes means it does not condition on weeds; it does not prove the
  environment is fully deterministic. Do not assume zero variance until measured.
- Six replays, five distinct players. The claim "the winners are open-loop" is well supported for
  `senkin13` and `syouya tobita` and weaker for `Dmitry Larko` at 97.4% units / 95.7% market, whose
  residual divergence is unexplained and may be a timeout or a genuine reactive component.
