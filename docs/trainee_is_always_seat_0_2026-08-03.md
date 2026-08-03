# The trainee is always seat 0, and seat 0 is not neutral

**Date:** 2026-08-03.
**Found by:** Alex, from a half-memory that seat 0 might win ties. The tie rule is fine; the seat
assignment is not.

## The tie rule is symmetric — that part checks out

```python
won = (money > money[:, ::-1])            # strict
tie = (money == money[:, ::-1])
reward = won + 0.5 * tie                  # train_jax_rl.py:499-522
```

Both seats receive 0.5 on an exact tie. `kagg/arena/arena.py:91-92` matches (`wins = m[0] > m[1]`,
`draws = m[0] == m[1]`). The only divergent convention is `kagg/arena/ladder.py:120`, which counts
`wins + (mine > theirs)` and tracks no draws, so a tie is a non-win there — still not a seat-0 win.

**Not verifiable from here:** `reference/kaggriculture.py:931` sets `s.reward` to the player's money
and nothing else, so the money → win/loss/tie conversion happens on Kaggle's server and is not in the
installed package. If the real ladder did break ties to seat 0 it would matter for our *training*
signal, since 63% of pool games are ties — but barely for the ladder, since real opponents bank $106k
and exact ties do not occur against them.

**A check that does not work:** `ret ≈ +0.5008` in the log does not discriminate between the two
conventions. The reward is zero-sum, so "0.5 each" and "1 to seat 0" both give a mean of exactly 0.5
over both seats.

## The real asymmetry

Every opponent role takes **seat 1**:

```
:328  take_opp   = use_opp[:, None]    & (seat == 1)
:354  take_idle  = use_idle[:, None]   & (seat == 1)
:360  use_trade | use_farm | use_ranch | use_carrot   & (seat == 1)
:599  trainable  = ~take_opp
```

So the policy occupies **seat 0 in every game it is trained on**, against every opponent including
the frozen pool. It has never played seat 1.

And seat 0 carries a measured advantage. `scripts/eval_policy.py`'s module docstring:

> *"Both seats are always played, and every seed is played twice with seats swapped: `_process_market`
> quotes both players against the same inventory but commits in seat order, so seat 0 has a real edge
> on contested trades. Reporting a one-seated result would flatter or damn the policy for free."*

`eval_policy` swaps seats deliberately. Training never does.

## How much this matters

**Today: probably little.** The edge is on *contested* trades, and the policy currently trades at
`BUY WHEAT 0.021` / `SELL WHEAT 0.026` with a market nobody else is competing in — `idle` and `farm`
do not contest wheat the way a real opponent would. There is not much edge to collect.

**Later: structurally.** On the real ladder the agent is seat 1 half the time and does not have the
edge then. A policy trained only as seat 0 has never seen the state distribution where its own order
settles second, and every training number in this project is a seat-0 number.

It also interacts with the `pool` degeneracy. Pool games are trainee-seat-0 against a frozen
seat-1 copy, so if the seat-order edge ever becomes worth anything, `wr_pool` will drift above 0.5
for a reason that has nothing to do with the policy improving — the same species of artifact as
`wr_trade` rising because our policy was demolishing the trader's market
(`HANDOFF_2026-08-02.md:446-448`).

## What to do

Nothing today — the run is mid-flight and this is not what is holding it back.

At the next config change, seat assignment should be randomised per episode rather than fixed: draw
the trainee's seat alongside the opponent role, which is redrawn per episode already at
`:633-634`. That makes `trainable` a drawn mask rather than the constant `~take_opp`, and it costs
one extra random draw. `--curriculum-symmetric` already exists in the neighbourhood of this question
and should be read before implementing anything.

Until then, treat every `wr_*` in this project as a seat-0 win rate, not a win rate.
