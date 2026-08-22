# Parity restored against kaggle-environments 1.32.6

2026-08-09.
Both simulators are exact against the installed environment again.
The eight failures handed to this session are closed, and eleven others that were already red went
green with them.

`python3 -c "import kaggle_environments; print(kaggle_environments.__version__)"` → **1.32.6**, and
`reference/kaggriculture.py` is byte-identical to the installed
`kaggle_environments/envs/kaggriculture/kaggriculture.py`.
So the reference in this repo is ground truth and was already current; what had not moved was the
simulator.

## The verdict up front

It was the encoding of 1.32.2 rules, as suspected — but **verified rather than assumed**, and the
list is longer than the town drain.
Diffing the 1.32.2 env source (`git show 909e5f6^:reference/kaggriculture.py`) against 1.32.6 gives a
closed list: everything in that diff is either a comment or one of **six** behavioural changes.
Two of the six (`townCenterSellInterval` 12 → 24, and the deletion of `TOWN_CENTER_DEMAND_SCHEDULE`)
had already been handled in `kagg/sim/town.py` by commit 909e5f6.
The other four had not, and they are what this session fixed.

| # | Rule in 1.32.6 | Was | Site |
|---|---|---|---|
| 1 | Movement onto a `LOCKED` tile is allowed | blocked | `ops.move`, `jax_sim` movement |
| 2 | `DROP`/`PICKUP`/`PLACE` resolve **before** the `LOCKED` guard | after | `ops.shed_adjacent`, `jax_sim` `on_shed` |
| 3 | `BUY_PRODUCT`/`BUY_ANIMAL` fail once the shed is full | uncapped | `game._commit`, `jax_sim` market commit |
| 4 | Shops unlock **with replacement**, capped at `MAX_SHOP_INSTANCES` | all distinct | `town.drain_at`, `Game.unlocked_shops`, `jax_sim` unlock arrays, `parity.run_reference` |

Every one was measured against the installed environment before a line of simulator changed, and
each has a test that goes red when the fix is backed out.
`tests/test_parity_1326_rules.py` holds one test per rule.

## Why #4 is the one that mattered most

The env's own comment is easy to read as an edge case:

> `unlocked_shops` may list the same shop more than once (shops are drawn with replacement); each
> instance consumes independently.

It is not an edge case.
Eight instances drawn from eight shops are all distinct with probability 8!/8⁸ = **0.24%**, so a
duplicate is the norm.
Every seed the parity gate uses duplicates — 700, 701, 800, 1500, 1501, 1502 — and
`observe_unlocks(11)` opens YARN_STORE on days 12, 15 **and** 21.
A simulator holding unlocks as a set of booleans therefore under-drains essentially every game.

This had spread further than the simulator.
`kagg/economics/market.py` already modelled instances correctly, which is why
`tests/test_sim_town.py::test_drain_matches_the_validated_economics_model_at_every_step` had been
failing at "step 360, WOOL: 3 != 5" — three being one YARN_STORE plus the centre, five being two
YARN_STOREs plus the centre.
The bool-mask assumption was in the *simulator and its test helper*, not in the economics model.

The representation change runs all the way down.
`Game.unlocked_shops` is now instance **counts** rather than flags, recomputed each step rather than
accumulated (accumulating counts would add one per shop per step).
`jax_sim` moved from a shop-indexed `unlock_day [B, N_SHOPS]` — a shape that cannot express a
duplicate at all — to an instance-indexed pair, `unlock_day` and `unlock_shop`, each
`[B, MAX_INSTANCES]`.
All the existing input forms still work: a `{day: shop}` dict, the new `{day: [shop, ...]}` list, and
a `[B, N_SHOPS]` day array from `random_unlock_days` / `boards.unlock_array`.

## The harness could not see it, which is the recurring lesson

`parity.run_reference` recorded unlocks as `unlocks.setdefault(shop, day)` — keyed by **shop name**.
That collapses a duplicate before the simulator is ever asked about it, so the gate handed our sim
half the drain and then compared the two.
It now records `day -> [shop names appended that day]`, which is what the env's list actually is.

This is the same failure mode CLAUDE.md already lists three times, and it recurred twice in this
session alone.

**The second instance is worth stating plainly, because the fix would otherwise have shipped
untested.**
Rule #3 — buying stops at `shedCapacity` — is *unreachable* by the existing 719-step scripts.
Measured across all five of them, the shed peaks at **8 to 11 items in a 100-item shed**.
A simulator ignoring the rule entirely passes every one of those episodes.
Confirmed directly: backing rule #3 out leaves all five original full-length tests **green**.

So `random_script` gained `buy_rate` / `buy_max`, `run_reference` / `run_sim` gained
`starting_money`, and `tests/test_sim_parity.py` gained
`test_full_length_episode_against_a_full_shed_is_exact`, which holds both farms at the 100-item cap
for **1,429 of 1,438 player-steps**.
Backing rule #3 out now fails exactly those two cases and nothing else — which is both the proof the
gate works and the proof the old gate never could.

## The tape fixture was testing a game that no longer exists

`tests/test_tape_parity.py` was the failure worth being most careful about, because the brief flagged
that the **numpy** sim was failing it and warned that chasing JAX while its reference is wrong wastes
the run.
It was not a numpy bug.

The episode's own recorded configuration says so:

```
data/episodes/89873723.json  ->  "module_version": "1.32.3",  "townCenterSellInterval": 12
```

The fixture pinned `EXPECTED_BANK = 147_178`, the bank that action tape produced on the ladder that
recorded it.
Driving the identical tape into the **installed** environment banks **$92,313**.
The recorded number is not reachable under 1.32.6 and a simulator that reproduced it today would be
wrong.

The corroborating detail is the unlock list: that recording opens eight *distinct* shops, the 0.24%
event under 1.32.6 and the guaranteed outcome under 1.32.2.

So the test now gates the claim it always actually made — *given these actions, our simulator equals
the environment* — by replaying the tape into the installed env and comparing against that, rather
than against a stale recording.
It costs about four seconds and is version-proof.
Result: **exact, all 719 turns, both simulators**, $92,313.

`test_the_recorded_bank_is_a_1_32_3_number_and_is_not_the_target` was added so nobody restores the
old constant, and it goes red if a future release ever makes $147,178 reachable again — which would
be the correct signal, since it would mean the town rebalance had been reverted.

One trap re-confirmed while doing this: the unlock schedule must be read out of **the env run being
compared against**, never hard-coded. `_spawn_weeds` consumes a draw per empty tile before
`rng.choice` picks the shop, so the same seed with weeds on and off produces different shops.

## Verification

Each fix was reverted individually and the suite re-run, per CLAUDE.md.
None of them is covered by nothing:

| Fix reverted | Goes red |
|---|---|
| 1 movement onto LOCKED | its own test + 8 full-length parity cases |
| 2 shed ops on a LOCKED tile | its own test + 7 full-length parity cases |
| 3 shed capacity on buys | its own test + **only** the 2 new full-shed cases |
| 4 duplicate shop instances | its own test + 7 parity cases + the tape test |

Rule #2's test is worth a note: it *passed* before rule #1 was fixed, for a confounded reason — the
farmer could not walk onto the locked tile, so `PICKUP` ran from the unlocked one and succeeded.
It only discriminates once movement is correct.

Suite movement, measured by diffing failures against a copy of the working tree with only these
files reverted:

- **slow suite: 24 failed → 13 failed, zero regressions.**
- **fast suite: 26 failed → 21 failed, one regression** (below).

## What is still red, and why none of it is a parity divergence

**1. `test_locked_chain_relocates::test_two_different_far_tiles_are_not_the_same_farm` — the one
regression, and a real finding for issue #26. Needs a decision from that issue's owner; deliberately
not touched here.**

That module was written about a search-layer bug: a chain aimed at ground the farm never unlocks
walks to the border, stops, and then builds *somewhere else*, so the plan is fiction.
Its docstring says `ops.py:86` ignores a move onto a LOCKED tile — which was true, and is now false.

Under 1.32.6 the unit walks onto the locked tile and the tile ops no-op there, so **no pen is built
at all**.
That fixes the relocation half of #26 for free: `test_a_pen_on_unaffordable_ground_does_not_appear_somewhere_else`
now passes, and `test_the_border_tile_is_where_it_actually_lands` takes its own built-in skip
("relocation no longer happens; this mechanism test has served its purpose").

But it makes the **degeneracy half worse**, which is what the failing test measures.
Every unreachable SE tile used to collapse onto a different border row; they now all collapse onto
the identical *empty* farm, so the beam cannot tell any of them apart at all.
The remedy is the design choice the module already names — reject the chain in `decode()` so it
reads as `skipped` — and that is a search decision, not a simulator one.

**2. Eight `test_shop_unlocks.py` failures — stale 1.32.2 price literals. CLOSED during this session
by concurrent work; the file is green as of `560b95b`. Recorded here because the measured table is
the thing to check the docs against.**

These were already red before this session.
The module constants were re-baselined for 1.32.6 by the town-rebalance commit
(`FROZEN_WHEAT_DRAIN = 30`, `REFERENCE_WHEAT_DRAIN = 588`, both of which now pass) but the inline
price literals were not.
The measured values against 1.32.6:

| product | frozen town | test pins | reference schedule | test pins |
|---|---|---|---|---|
| WHEAT | 30 | 37 | 49 | 51 |
| TOMATO | 64 | 77 | 85 | 98 |
| EGG | 52 | 58 | 69 | 76 |
| MILK | 208 | 263 | 315 | 340 |
| STRAWBERRY | 166 | 219 | 274 | 297 |

`test_frozen_town_baseline_is_what_the_bug_was_measured_at` documents itself as *"Guard. If this
moves, every figure quoted in the bug report is stale."*
Going red was the signal it exists to raise, so the numbers being updated is only half the job: the
**figures quoted in the docs are still the 1.32.2 ones** and need re-checking against the table
above. That is a separate, deliberate piece of work and is not done.

**3. The remaining ~13 failures** (router, planner, feed-reserve, water-cadence, stock rows) are all
pre-existing and untouched, in the search layer another agent is working in.

## Collateral fixed on the way

Adding `unlock_shop` to the JAX `State` broke two constructors, both now corrected:

- `kagg/rl/adapter.py` — missing field, a hard `TypeError`.
- `kagg/rl/curriculum.py` — three sites. One was a `TypeError`; the other two would have been
  **silent**. `_replace(unlock_day=...)` without its companion would have inherited the adapter's
  all-zero array and read as eight instances of shop 0, and the shuffle permuted `unlock_day` without
  `unlock_shop`, pairing one game's days with another's shops.

`jax_sim.shop_ids_for_days(batch)` exists so that pairing is explicit at the call site rather than
implicit, because both of those failures are wrong *drains*, not crashes.

One dtype trap: `jnp.sum` with x64 enabled accumulates int32 into int64, and `rollout`'s `lax.scan`
rejects a carry whose dtype changed. `_drain` now passes `dtype=_I` explicitly; the old
`unlocked @ SHOP_PULL` had kept int32 for free.
