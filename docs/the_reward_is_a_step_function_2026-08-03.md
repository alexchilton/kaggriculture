# The opponent pool has no rung between $0 and $3,000

**Date:** 2026-08-03.
**Found by:** Alex, reasoning from the win condition — *"wins against anything => more money at the
end — not a draw, more money => it has >0"*.

## The win condition, verified

```python
won = (money > money[:, ::-1]).astype(jnp.float32)          # train_jax_rl.py:499
...
reward = won + 0.5 * tie                                    # :522
```

Strictly more money than the opponent at the end. Loss 0, draw 0.5, win 1.
So a win is not "farm well" — it is **out-bank this specific opponent**, and every opponent's final
bank is a known constant.

## The ladder as it actually stands

| opponent | active | banks | we must reach |
|---|---|---:|---:|
| `pool` (frozen past selves) | 45% | $0 | **$1** |
| `idle` | 10% | $3,000 | $3,001 |
| `trade` | 0% | $3,368 | $3,369 |
| `carrot` | 0% | $3,410 | $3,411 |
| `ranch` | 20% | $12,078 | $12,079 |
| `farm` | 25% | $23,783–$30,292 | $30,293 |

We finish on **$0** (`docs/bankrupt_every_game_2026-08-03.md`).

## The problem this makes visible

**The reward is a step function in money, and the steps are $0, then $3,000, then nothing until
$12,078.**

Going from $0 to $2,999 changes not one terminal reward in the entire batch. Every scripted game is
still a loss and still pays 0. The policy would have massively improved — recovered its whole stake —
and PPO would see literally no difference. There is no partial credit anywhere on that interval,
because no opponent's final bank sits inside it.

That is a sharper statement than "the reward has no variance". The variance is not merely small; the
reward is **piecewise constant over exactly the range the policy currently occupies**, so the
gradient is zero by construction rather than by bad luck.

The one exception is `pool`, where the bar is $1 because the frozen opponent is equally broke. That
is the entire live gradient in the run, and it is why `pool` shows 0.473 win / 0.630 draw while every
scripted opponent shows 0.000 / 0.000. The policy is learning to end a season on $5 instead of $0,
because that is the only reward difference available to it.

## The thing that makes it concrete

**Doing nothing banks $3,000 and draws with `idle`.**
`train_jax_rl.py:392` says so directly: *"both sides doing nothing draw at exactly $3,000 each, and a
draw pays 0.5"*.

So the current policy is not merely untrained. It is **$3,000 worse than passing every turn**, and
the reward function cannot tell it that until it has clawed back the entire amount.

## What follows — and what does not

**Not reward shaping.** `CLAUDE.md` settles this: terminal win 1 / loss 0, gamma 1.0, Alex's call,
and four of the top finishers on record used a terminal signal. Adding a money term to the reward
would be treating the symptom and re-opening a decision that is closed.

**The fix is opponent design, which leaves the reward untouched.** The gap is $0 → $3,000 with
nothing in it. Scripted seats that bank intermediate amounts would restore partial credit across
exactly the interval the policy has to cross, and each one is a legitimate terminal win/loss — no
shaping, no dense reward, no change to the loss function.

Two cheap observations that make this easy:

1. An opponent that banks $500 or $1,500 is far simpler to write than `jax_heuristic`'s crop economy
   — it is `idle` that spends a fixed amount early. `idle` itself is already implemented as
   all-zeros (`:352-353`: *"`NOOP` is op 0 and bucket 0 of every market head is quantity 0, so
   all-zeros* is *that agent — no network, no parameters"*), so a "spend then stop" variant is a
   handful of lines in the same style.
2. `trade` ($3,368) and `carrot` ($3,410) are **already implemented and currently at 0%**. They add
   rungs above `idle` for free, but not below it — they do not close the gap that matters.

## The prediction to test against the live run

If this reading is right, `bank_final_med` will climb toward $3,000 and **`wr_idle` will stay at
exactly 0.000 the entire way**, snapping to a nonzero value only when the bank crosses $3,000.
A gradual rise in `wr_idle` would refute it.

That is worth watching at the 30M-turn checkpoint, because the two outcomes call for opposite
responses: a step means the pool needs intermediate rungs; a gradual climb means the frame is fine
and it only needs time.
