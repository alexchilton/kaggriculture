# Market fine-tune: scripted body, learned market brain

Alex's decomposition, 2026-08-04.
Deliberately **not** built on `scripts/train_jax_rl.py` -- that trainer exists to learn the whole game
from terminal reward, and this is a different and much smaller problem.

## The idea

```
scripted plan  ->  unit actions (12 hands, 18 ops)     FROZEN, no gradient
small MLP      ->  market orders only                  TRAINED
reward         ->  terminal win/loss, gamma 1.0        UNCHANGED
```

## Why it follows from what we measured

`docs/episode_teardown_2026-08-03.md`, all verified from replay JSON:

- Every game starts on the **same board** -- 25 EMPTY, 75 LOCKED, NW quadrant, no shops. Checked across
  seeds 877757993 and 37447535: byte-identical.
- `Dmitry Larko` plays **673/720 identical actions across two different seeds and two different
  opponents**. The only divergences are weeds (`DIG` instead of `PLANT`).
- Where the two mirror agents diverge at t=50, it is **only the market list**.
- The top three agents submit byte-identical plans and **ignore the opponent entirely**.

So the farm half is a solved deterministic script that we can copy, and the market half is the only
place anything differs -- and the only place the field is weak.

## The three problems it solves at once

**1. Credit distance collapses from ~700 turns to ~1.**
Every failure diagnosed on 2026-08-03 was long-horizon credit on the farm chain: FEED at 0.00%,
FERTILIZE at raw 0, `ev_signal` 0.30, buy a goose on turn 100 and win or lose on turn 719. A market
decision's price impact is realised **the same turn** (`price(inventory)` moves as the order fills).
That is the regime PPO handles well, and it needs no shaping, no reverse curriculum and no macro.

**2. The gradient problem, which is the one that actually matters.**
Today the policy loses **0/1,350** against `farm`. A uniformly negative advantage says "everything you
did was bad" with no successful example to point at -- directionless, which is why entropy climbed 5 ->
9 rather than falling. If our body *is* the leaders' script, self-play is mirror against mirror, both
sides bank ~$100k, and the game is decided by **who executed the market better**. Win rate sits near
0.5 by construction: the maximum-gradient regime, with all of that gradient on the thing being trained.

**3. The action space collapses**, from 12 hands x 18 ops x arguments to ~7 market heads.

And the prize is measured. `CLAUDE.md`: *"Optimal execution remains the largest single measured number
on the board: ~$30k of `contrarian`'s $51k lost to price impact on melon alone."* Nearly 60% of a bank,
and the leaders leave it there -- they dump 1,108 wheat and 536 strawberries on a fixed schedule
whoever they are playing.

## Why a much smaller net

The market decision does not need per-tile geometry. "Should I sell 10 melons" does not depend on where
a unit is standing; it depends on prices, the town's inventory, what I hold, and **what is about to be
harvested**. So the observation is ~90 aggregate scalars, not 125 tokens x 27 features, and the net is
an MLP rather than an entity transformer.

| | current policy | market brain |
|---|---:|---:|
| observation | 100 tiles x 27 + 24 units x 28 + 60 | ~90 scalars |
| architecture | 3-layer transformer, d_model 128 | MLP 128 x 2 |
| parameters | **727,055** | **~47,000** |

~15x smaller. It also removes the transformer forward from both the rollout *and* two PPO epochs,
which was ~17 TFLOP per update -- so throughput should improve as well, though the simulator remains
the dominant cost (`docs/model_size_2026-08-03.md`).

**A forecast feature is the one non-obvious input.** A market policy has to know what supply is coming:
`yield_units` already standing, plus what will ripen in the next few days. Without it, selling is blind
to the fact that 40 melons land tomorrow.

## The known-fragile part, now the whole model

`CLAUDE.md` records the market heads failing in both directions:

- greedy argmax over per-head marginals emits **zero** orders, because nine independent "probably not
  sell" decisions compose into "never sell";
- independent sampling from the same marginals banks **$1**;
- and the marginals are *good* -- 12:1 discrimination on `buy_product`. It is the **joint decode**
  destroying the information, not the network.

That was one problem among many. Here it is the only one, so the decode gets an **autoregressive**
treatment over ~7 heads: each head's logits are conditioned on the decisions already made. Cheap at
this size, and it is exactly the problem Ender's micro-steps were built for (`CLAUDE.md`: evaluate a
technique against the problem its author built it for).

## Ordering, and the honest dependency

The body has to exist first. `kagg/search/executor.py` does not yet read the livestock genes added in
`d14bb94`, so the cloned plan cannot build a pasture or buy a cow.

**But the harness does not have to wait.** `jax_heuristic` already drives unit ops end to end and banks
$28,168, so the fine-tune can be built and validated against *that* body immediately, then have the
cloned plan swapped in. Same interface, better body.

1. `market_obs.py` -- the aggregate encoder. **This document's deliverable.**
2. `market_net.py` -- MLP + autoregressive market heads.
3. `scripts/train_market.py` -- PPO over market heads only, scripted body, terminal reward.
4. Swap the body from `jax_heuristic` to the cloned leader plan once `executor.py` grows animals.

## Kill criterion, committed up front

If the market brain on a `jax_heuristic` body does not beat plain `jax_heuristic` head-to-head within
50M turn-steps, the market is not where the edge is and this is wrong. Measured with weeds on and a
seed range, per `CLAUDE.md`.

Related: [[episode_teardown_2026-08-03]], [[ideas]], [[model_size_2026-08-03]].
