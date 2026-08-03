# `seat_loss` demands a sum the discount makes impossible

**Date:** 2026-08-03 (late).
**Status:** a certain inconsistency, and a strong candidate root cause for P1. Found while launching
the from-scratch baseline, from the trainer's own startup banner. Run stopped after 90 seconds.

## The two lines

`train_jax_rl.py:1044`

```python
seat_loss = jnp.square(pairs.sum(axis=-1) - 1.0).mean()
```

applied to **every row**, at `--seat-coef 1.0` — the same order as the value loss at `--vf-coef 0.5`.

`train_jax_rl.py:1236`

```python
ap.add_argument("--gamma-per-day", type=float, default=0.97, ...)
```

and the banner the trainer prints from it:

```
discount: 0.97 per game-day = 0.998732 per turn
          terminal reward retains 0.401 of its value at t=0
```

## Why they cannot both be right

The reward is terminal and binary — 1 for a win, 0 for a loss, paid once. So for any state:

```
V(seat) = gamma^(turns remaining) * P(that seat wins)
```

and because exactly one seat wins, `P(seat0 wins) + P(seat1 wins) = 1`, giving

```
V(seat0) + V(seat1) = gamma^(turns remaining)          for every state, decided or not
```

Under the default discount that sum is **not 1** anywhere except the final turn:

| turn | turns remaining | true `V0 + V1` | what `seat_loss` demands | error it injects |
|---:|---:|---:|---:|---:|
| 0 | 719 | 0.402 | 1.0 | **0.598** |
| 240 | 479 | 0.544 | 1.0 | 0.456 |
| 480 | 239 | 0.738 | 1.0 | 0.262 |
| 700 | 19 | 0.976 | 1.0 | 0.024 |
| 718 | 1 | 0.999 | 1.0 | 0.001 |

`seat_loss` is therefore correct on the last row of an episode and wrong on all 718 others, most
wrongly at the start — which is where the overwhelming majority of rows are.

## Why this looks like the cause of the flat critic

The observed failure (`critic_terminal_blindness_2026-08-03.md`) is that value sits in a narrow band
around the middle and barely moves with the clock. That is the *least-loss* response to being told to
satisfy `V0 + V1 = 1` everywhere while the achievable sum ranges 0.402 to 1.0: a critic cannot both
track the discount and satisfy the constraint, and sitting near 0.5/0.5 minimises the penalty across
the batch.

The confirming detail is the one that previously read as reassuring. `V(hopeless, final turn) = 0.139`
with the seats summing to **1.00** — `tests/test_critic_terminal_blindness.py::test_the_two_seats_still_sum_to_one`
passes. Under `gamma = 0.998732` a true value function sums to 1 at *no turn but the last*, so a
critic that satisfies the constraint across the season is satisfying a false one. That test was
written to make the point that seat-sum consistency is necessary but not sufficient. It is worse than
that: **the constraint is not necessary, it is wrong.**

This also explains why the two shipped mitigations did not help, which the source doc left open.
`--n-phases` staggering changes when terminal rows arrive, not how many there are. `seat_coef` is the
other mitigation, and it is the thing doing the damage.

**Not yet proven.** The inconsistency is arithmetic and certain; that it is the dominant cause of the
flat critic is a hypothesis, and the test is a run. It is cheap to settle because the fix is one flag.

## Note on how this got in

`CLAUDE.md` records the settled decision as **"The reward is terminal: win 1, loss 0, gamma 1.0"**,
marked as Alex's call made explicitly and applying to every policy in the project. The code defaults
to `0.97` per game-day and no launch script has ever passed `--gamma-per-day`, so every run to date
has silently used a discount the project had decided against. With `gamma = 1.0` the seat-sum
constraint is exactly correct at every turn, which is presumably the assumption it was written under.

## The two consistent resolutions

1. **`--gamma-per-day 1.0`.** Restores the settled decision, makes `seat_loss` exactly right at every
   turn, and removes the attenuation of the terminal signal — the only reward in the game currently
   arrives at t=0 worth 40% of itself. One flag, no code change, no new mechanism. **Recommended.**
2. **Keep the discount and change the target** to `gamma^(turns remaining)` rather than 1.0. Defensible
   — simjeg used 0.995/turn and Ender 0.998 — but it is a change to the loss function, needs its own
   failing test first, and contradicts a decision on record.

Do not do both. They are alternatives.

## What this does to P1

P1 was "upweight terminal rows in the value loss", chosen because terminal rows are 0.14% of the
batch. That reasoning stands on its own, but it is now second in line: adding a third mechanism while
an existing one is pushing a wrong target would confound the measurement, and the source doc's own
instruction is to *measure why the shipped mitigations are insufficient before adding another*. This
is that measurement, and it says one of them is not insufficient but actively harmful.

Revised order: fix the inconsistency, re-run the from-scratch baseline, and only then decide whether
terminal-row upweighting is still needed.
