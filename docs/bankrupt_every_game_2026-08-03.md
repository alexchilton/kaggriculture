# The policy ends every season on $0, and that is where the gradient went

**Date:** 2026-08-03.
**Found by:** Alex asking why `money_max` read below the $3,000 every game starts with.

## First, the question that started it

`money_max` is not the peak a game reached. It is

```python
"money_max": float(np.asarray(jax.device_get(state.farm.money))[:, 0].max())   # train_jax_rl.py:2416
```

— `[:, 0]` is seat 0 (the live policy) across all 256 games, and `.max()` is over the **game axis at
one instant**, not over time.
With `--n-phases 256` staggering every game to a different point in its season, almost none is ever
at turn 0, so `$3,000` shows up only when a game happens to be near its start.
Over the probe run `money_max` does reach exactly `$3,000`. A reading of `max $315` means that at
that moment all 256 games had already spent down.

Not a bug. But the question is the right one, and `bank_final_med` answers it properly.

## The finding

`bank_final_med` is the median bank of games that **actually finished**, on the live policy's seat —
the field `CLAUDE.md` and `HANDOFF_2026-08-03-evening.md` both say to use instead of `money_med`.

| run | updates with a finished game | min | median | max | updates beating the $3,000 start |
|---|---|---|---|---|---|
| probe arm 1 (`3e-5`, 120 updates) | 98/120 | $0 | **$0** | $5 | **0 / 98** |
| `day0-long` (live, first 48) | 26/48 | $0 | **$0** | $0 | **0 / 26** |

**The policy takes $3,000 and finishes the season with nothing. Every game. Never once above the
start.** The best single update in 98 was a median of $5.

## What that does to the training signal

Per-opponent over probe arm 1's last 40 updates:

| opponent | games | win rate | draw rate |
|---|---:|---:|---:|
| `pool` (frozen past selves) | 17,226 | 0.473 | 0.630 |
| `farm` | 7,931 | **0.000** | **0.000** |
| `ranch` | 7,210 | **0.000** | **0.000** |
| `idle` | 3,183 | **0.000** | **0.000** |

So roughly **55% of the batch has no outcome variance at all** — every scripted game is a loss, so
every terminal reward on those rows is 0 and there is nothing for a policy gradient to push against.

The remaining 45% is `pool`, which is 63% draws, because *both* sides bank $0 and `money == money` is
exact — the tie condition `CLAUDE.md` already warns about. That leaves ~37% of 45%, about **17% of
the batch, carrying any outcome signal at all** — and what those games are deciding is whether a
season ends on $5 or on $0.

This is Position A's premise from `docs/opus_review_2026-08-03.md`, now with data behind it rather
than inference. It is not that the reward is noisy. It is that on most rows the reward is a constant.

## The sharpest statement of it

**`idle` passes every turn and banks its opening $3,000. The policy loses to it 3,183 times out of
3,183.**

To beat `idle` the policy does not need to farm, trade, or route anything. It needs only to *not
spend*. That is close to the simplest thing this action space can express, and 1.0M turns of training
has not found it.

This also retires the caveat I raised earlier today. 278 games could not distinguish a 0% win rate
from a 1% one — but 3,183 games with zero wins rules out any true rate above **0.094%** at 95%
confidence. Against `idle`, "it never wins" is now established rather than merely observed.

## What is not the cause

The obvious suspect is the shape prior forcing purchases, and the numbers do not support it:

- `kl_prior` decays 1.649 → 0.091 over the 120 updates, so `--kl-anneal 4000` is releasing it.
- `seed_rate` settles at **0.042 against a `--spend-prior` of 0.05** — *below* the prior, not pinned
  to it. `hand_prior_heads`' own test (`:801-803`) is that trained rates finish above the prior if it
  has capped anything; this is the opposite, so the policy is actively pushing spend down.
- `hire_rate` 0.017, `land_rate` 0.001.

The policy is already learning "spend less" and it is nowhere near enough: 0.042 over 719 turns is
still ~30 seed purchases a season, against a stake of $3,000 and revenue of nothing, because harvest
runs 0.18–0.24% of ops.

So the failure is not that the prior forces ruin. It is that **spending is learnable and earning is
not** — the policy can find the cheap half of "end with more than you started" and cannot find the
half that requires a plant-water-wait-harvest-sell chain whose payoff arrives hundreds of turns after
the first action in it.

## What this does and does not imply

It does **not** mean the frame is dead. Every number here is from 1.0M turns, roughly 3% of an Atari
run, and the policy is visibly moving in the right direction on the one thing it can currently reach.

It does mean the live 4.2-day run has a specific, checkable prediction attached to it now:
**`bank_final_med` must come off $0.** Until it does, `ev_signal` cannot be trusted to mean the critic
is learning the game rather than learning that everything is a loss — a critic that predicts "0" on
every scripted row is perfectly accurate and completely useless.

That is a better gate for the 30M-turn checkpoint than `ev_signal` alone, and it costs nothing: the
field is already logged.
