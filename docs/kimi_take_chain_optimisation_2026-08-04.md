# Kimi's take: optimise on chains, not slots (2026-08-04)

Verbatim response from Kimi (K2.6 Instant) to `docs/kimi_prompt_trajectory_optimisation.md`.
Saved before assessment so the source is on disk and not paraphrased away.
Our assessment follows at the bottom, clearly separated.

---

## 1. The Core Shift: Mutate Templates, Not Actions

A chain is a parameterized subroutine that expands into a coherent block of raw actions.
Your mutation operator should be:

    mutate(template_type, start_day, parameters)

Not:

    mutate(slot_idx, new_action)

### Example Chain Templates

| Template | Parameters | Expands To |
|---|---|---|
| `LivestockChain` | `(start_day, animal, count, pasture_loc)` | Buy animal → build pasture → walk unit → pick up → place → count × feed loop → sell at maturity |
| `CropIntensive` | `(start_day, crop, plots, unit_ids)` | Buy seeds → plow → plant → water schedule → harvest schedule |
| `MarketArbitrage` | `(day, product, qty, expected_price)` | Sell/buy order sequence |
| `Expansion` | `(day, land_count)` | Save money → buy land → reallocate units |

A single mutation now touches 30–200 raw slots coherently.

## 2. How to Build the Chain Library

You do not need to hand-write every chain from scratch. Extract them from your data:

**A. Replay Differencing.**
Take your seed trajectory ($23.8k) and a top-player trajectory ($145k).
Align them day-by-day.
Find contiguous blocks where the top player is doing something your seed is not.
Extract those blocks as candidate chains.

**B. Prefix Profit Analysis.**
Replay your seed and compute the exact marginal bank balance per turn.
Look for long sequences where money is locked up (negative cash flow) followed by a large payoff.
Those are chains.
The `BUILD_PASTURE → BUY_COW → ... → SELL_BEEF` sequence will show up as a deep V-shaped cash-flow pattern.

**C. Hand-Write the Obvious Ones.**
You know livestock is 35% of leader revenue and your seed has zero.
Hand-write a `LivestockChain` template with parameters `(start_day, cow_count)`.
That alone is probably worth +$20k if placed correctly.

## 3. The Search Algorithm: Forward Locking with Chain Insertion

Since your simulator is deterministic and prefix-replayable, the most powerful technique is forward
locking.
Do not optimize the full 720-turn script at once.
Build it prefix-by-prefix.

```python
best_script = seed_script  # $23.8k baseline

for phase_start in [0, 30, 60, 90, ..., 690]:
    phase_end = phase_start + 30

    # 1. Cache the exact state at phase_start from best_script
    cached_state = simulator.run(best_script[:phase_start])

    # 2. Generate candidates: best_script with ONE chain inserted in [phase_start:phase_end]
    candidates = []
    for chain in chain_library:
        for start_day in range(phase_start, phase_end - chain.min_duration):
            mutated = best_script.copy()
            mutated[start_day : start_day+len(chain)] = chain.expand()
            candidates.append(mutated)

    # 3. Evaluate from cached_state (not from turn 0)
    scores = jax.vmap(lambda s: simulator.run_from_state(cached_state, s[phase_start:]))(candidates)

    # 4. Keep the best full script (may be best_script itself if no improvement)
    best_idx = jnp.argmax(scores)
    if scores[best_idx] > current_best_score:
        best_script = candidates[best_idx]
        current_best_score = scores[best_idx]
```

Why this works:

- You evaluate a chain in the exact context it will run in.
- Prefix caching makes each eval ~30x cheaper than a full rollout.
- You are never trying to optimize day 500 while day 5 is still garbage.
- If a chain requires 25 days to pay off, you see the payoff within the phase (or the next phase).

**Neutral Drift Variant.**
If all candidates score worse than the baseline (common when a chain requires a setup turn that
looks like a pure cost), allow temporary regression:

- Keep a Pareto frontier of `(early_money, late_money)` or `(money_at_day_30, money_at_day_720)`.
- A chain that drops day-30 money but raises day-720 money is accepted.

## 4. Chain Evaluation: Exact Finite Differences

Your superpower is exact replay.
Use it to compute the exact value of a chain rather than noisy sampling.

```python
def chain_marginal_value(chain, base_script, insertion_day):
    state_t = simulator.run_prefix(base_script, insertion_day)
    baseline_final = simulator.run_from_state(state_t, base_script[insertion_day:])

    variant_script = base_script.copy()
    variant_script[insertion_day : insertion_day+len(chain)] = chain.expand()
    variant_final = simulator.run_from_state(state_t, variant_script[insertion_day:])

    return variant_final - baseline_final  # Exact, noiseless
```

Since this is exact, you can rank every chain in your library at every possible insertion point and
pick the top-K to actually test.
This is a pre-filter that costs almost nothing.

## 5. Handling Chain Interactions (The Hard Part)

Chains compete.
`LivestockChain(day=5, cows=3)` and `CropIntensive(day=5, plots=10)` both need money and units.

**A. Resource Budgeting.**
Add a virtual resource tracker to your chain templates.
Each chain declares its peak cash need and unit usage.
Before evaluating a candidate, check if the budget is feasible given the prefix state.
If not, skip the eval.

**B. Co-Evolution of Chain Sets.**
Instead of inserting one chain at a time, maintain a genome of chain slots:

    Genome = [(chain_id, start_day, params), (chain_id, start_day, params), ...]

The decoder expands all chains into the script, resolving conflicts (e.g. two chains asking for the
same unit on the same day) with a priority rule.
Now your search is over which chains to include and when, not over raw actions.

Use a GA with crossover that swaps entire chain tuples between parents.
A child inherits Parent A's livestock schedule and Parent B's crop schedule.
This respects the chain structure.

## 6. The Closed-Loop Test (Do This Now)

Before you sink compute into chain optimization, run the falsification experiment:

1. Take your current best open-loop script.
2. Train a tiny closed-loop policy (even a decision tree or 32-unit MLP) by behavioral cloning on it.
3. Fine-tune with exact rollouts against your 4 opponents.
4. Does it beat the open-loop script?

If yes, your chain optimization should target closed-loop chain templates (e.g. a
`ReactiveMarketChain` that reads current prices).
If no, proceed with open-loop chains.

## 7. Concrete Next Steps (Priority Order)

| Step | Action | Expected Outcome |
|---|---|---|
| 1 | Hand-write `LivestockChain(start_day, count)` and `CropIntensive(start_day, crop, plots)` | Immediate +$10–30k if placed well |
| 2 | Implement prefix-cached forward locking (30-day phases) | Escape local optima by building coherent prefixes |
| 3 | Extract 5–10 candidate chains from top-player replay diffs | Data-driven chain discovery |
| 4 | Run exact marginal ranking of all chain x day combinations against your seed | Know exactly where to place chains |
| 5 | Switch to GA with chain-tuple crossover on a population of 500 | Combine livestock + crop + market chains |
| 6 | Run the closed-loop falsification test | Validate or invalidate the open-loop premise |

## Bottom Line

Optimizing on chains means your genome is a build order, not an action list.
You are playing StarCraft, not tic-tac-toe.
The right frame is real-time strategy search: find the best composition and timing of economic build
orders, then let a compiler resolve them into unit-level actions.

Your seed has zero livestock.
One well-placed `LivestockChain` is probably worth more than 1,000 iterations of single-slot
hill-climbing.
Start there.

---

# Our assessment (2026-08-04, after implementing `kagg/search/routines.py`)

## Confirmed by measurement

The core shift is right and is now built and green (`tests/test_routines.py`, 8 passed).
One COW in the `(4,4)` shed cell, measured in our own simulator:

    do-nothing baseline      $ 3,000
    1x GOOSE on (4,4)        $ 4,604   net  +$1,604
    1x COW   on (4,4)        $11,119   net  +$8,119
    1x SHEEP on (4,4)        $ 9,510   net  +$6,510

**Section 4 (exact finite differences via prefix caching) is the strongest idea in the take** and is
independently correct for a reason Kimi did not know -- see the daily reset below, which makes day
boundaries exact resynchronisation points.

## Where the take is wrong on the game's actual rules

1. **"count x feed loop" and "sell at maturity" understate the obligation.**
   `consecutive_unfed >= 2` escapes the animal (`kaggriculture.py:786`).
   Feeding is a *daily* commitment for the rest of the season, not a bounded loop.
   And `pending_care_bonus` accumulates +1 per fed+cared day and dumps entirely on the next
   production day capped at `max_held`, so daily harvest is near-optimal and a single sale at
   maturity throws most of the yield away.

2. **"+$20k from livestock" is not supported.**
   There are only four shed-access tiles `(4,4) (5,4) (4,5) (5,5)`, and they are the only tiles where
   PICKUP/DROP work.
   The zero-movement ranch therefore caps at four animals.
   Our measured +$8,119 is also an *upper bound*: it was scored against a do-nothing opponent, and
   the reason it is that large is that `_town_consume` drains market inventory while nothing refills
   it, so MILK climbed $212 -> $333 across the season.
   A real opponent selling milk removes most of that.

3. **Turn/day units are conflated.** `phase_start in [0, 30, ..., 690]` over a 720-*turn* script is
   30-turn phases, i.e. 1.25 days at `turnsPerDay=24`. The natural phase is the day.

4. **Forward locking has a specific failure here: land.**
   `LAND_ORDER` is `['NE','SW','SE']` at `[1000, 2000, 4000]`, bought strictly in sequence, and
   `_do_buy_land` silently no-ops when money is short.
   Saving for a $4,000 purchase looks exactly like doing nothing to a prefix-greedy optimiser, so
   forward locking will never fund it.
   Land timing has to be a global plan parameter, not a locally discovered one.
   Kimi's Pareto variant helps but does not fix this.

5. **The closed-loop falsification test is partly already answered.**
   Across leader replays, market actions are **720/720 identical** between episodes against
   different opponents while unit actions differ on 6 of 30 days
   (`data/logs/open_loop_subin.log`).
   The market half of the artifact is demonstrably open-loop already.
