# The day-10 cliff, decomposed: the curriculum taught it to buy a farm it cannot afford

Handoff item 1, answered 2026-08-03 against the live `league1-20260803-054444` checkpoint at update
1800, 32 games per seating, both seatings, vs the scripted farmer.

Instrument: `jax_sim.step_accounted` — an exact per-turn split of every dollar into `hire` / `land`
/ `trade`, pinned by `tests/test_money_accounting.py` (9 tests, invariant asserted at `atol=0`).
The parity suite is still 54/54 after the change.

## What the cliff actually is

```
policy bank by day  d0:3,000  d5:2,970  d10:2,977  d15:1,188  d20:705  d25:355  d29:220

money flow per day (median over games), + is income      [seat 0]
    day      trade       hire       land        net
      0          0         -2         -0         -2
      5          0         -1         -0         -1
      8          0         -1         -0         -1
     10        -10         -2         -0        -12
     11       -154        -33         -0       -186     <-- everything starts at once
     12       -160        -54         -0       -214
     13        -50        -54         -0       -104
     14          0        -54         -0        -54
     15          6        -44         -0        -38
     20          0        -26         -0        -26
     25         21        -44         -0        -22
  season totals   trade -648   hire -1,192   land -1,000
```

**It is not one cause, it is three, and they all switch on together at day 10-11.** For ten days
the policy is quiescent — net -$1 to -$2 a day. Then on day 11 it starts buying on every channel
simultaneously: a land quadrant, a crew, and a burst of stock.

**The largest single drain of the whole season is `hire`, at -$1,192** — more than the land
purchase and more than everything it lost trading.

## Why hire is the load-bearing one

**There is no upkeep in this game.** `_end_of_day` and `_night` move no money at all, so the
handoff's requested "income / upkeep / purchase" split has no upkeep line to fill.

**But `n_units` resets to 1 every single night.** So a crew is not bought, it is *rented daily*,
and `HIRE_COST` is Fibonacci:

```
crew  8: $33/day     crew 10: $88/day     crew 12: $232/day
crew  9: $54/day     crew 11: $143/day
```

Now read the measured hire column again: **-33, -54, -54, -54, -44, -26, -44.**

Those are not approximately the ladder. They *are* the ladder. -33 is a crew of exactly 8, -54 is
exactly 9, -88 (seat 1, day 15) is exactly 10. The policy re-hires to a crew of 8-10 every morning
from day 11 to the end of the season, and pays for it every morning.

That is a recurring bill booked as a one-off purchase. It is invisible in a bank *level*, which is
why five days of per-game-day bank readings could show the cliff and never explain it.

## The root cause: the curriculum rungs teach "day ≥ 10 means you own a farm"

The training mix is `length:0:0.6,10:0.1,15:0.1,20:0.1,25:0.1`. Here is what the four late rungs
actually hand the policy, read straight out of `curriculum.states_at_day`:

| rung | money (median) | **units (median)** | land (median) |
|---|---|---|---|
| day 0 | $476 | **7.0** | 0.0 |
| **day 10** | $980 | **9.0** | **1.0** |
| day 15 | $11,688 | **11.0** | 1.0 |
| day 20 | $29,730 | **11.0** | 1.0 |
| day 25 | $58,333 | **11.0** | 1.0 |

**40% of training episodes begin at day ≥ 10 in a state that already owns a crew of 9-11 and a land
quadrant.** `day/30` is a feature the policy reads at layer one. So what it has learned is not a
strategy, it is a correlation that is true across nearly half its training distribution: *at day 10
and later, a farm has ten hands and a quadrant.*

Then it is deployed from a real $3,000 day-0 start, arrives at day 10 with one unit and no land, and
**makes the state match the day it thinks it is in.** It buys the quadrant ($1,000, exactly the
season total), hires to a crew of 8-10, and stocks up ($154-$395 of net buying on days 11-13).

It is not choosing badly. It is reproducing its training distribution. The distribution is the bug.

### Correction: the policy's day-response is SMOOTH, not a step at day 10

The paragraph above was written before the causal link was tested, and the test partly refutes it.
Holding the board completely fixed at a poor day-0 state — $3,000, one unit, no land — and moving
**only** `step_index`:

```
  day    P(hire)   P(buy_land)
    0     0.1605        0.0000
    8     0.1698        0.0001
   10     0.1913        0.0004
   14     0.2839        0.0063
   20     0.4107        0.1770
   28     0.4407        0.4767
```

**There is no step at day 10.** `P(hire)` is a smooth monotone ramp from 0.16 to 0.44 across the
season, and `P(buy_land)` from ~0 to 0.48. So "it copies the day-10 state" is wrong as stated.

What is right, and is what the probe actually establishes:

1. **The day feature drives spending propensity hard and monotonically**, on a state where nothing
   else has changed. That is the curriculum correlation showing up in the policy, just as a ramp
   rather than a threshold.
2. **The cliff in dollars needs no cliff in behaviour, because `HIRE_COST` is Fibonacci.** Cost is
   convex in crew size — crew 3 is $2/day, crew 8 is $33, crew 10 is $88. A modest, smooth rise in
   hire propensity turns into a 20-30x jump in spend. The cliff is manufactured by the price
   ladder, not by a decision boundary.
3. **`P(buy_land)` peaks at day 28 (0.48).** Buying a quadrant with two days left is indefensible
   — nothing planted in it can mature. A propensity to buy land that *rises* monotonically to the
   end of the season is the wrong sign economically and is very hard to explain except as
   inherited from rich late-game rung states.

**Caveat on the probe, stated because the same confound was already caught once today:** it holds
the board at the reset configuration while moving the day, which is a combination training never
produces — an empty board cannot occur on day 28. It isolates the day feature's effect cleanly,
which is what it is for, but it does not measure what the policy does on a *real* day-28 board.
The real trajectory moves day and accumulated state together.

**This is the same species as the day-0 bug already found and fixed** — "the policy was trained to
*continue* an elite opening and deployed to *make* one" — except it was only fixed for the day-0
rung. The identical defect is sitting in all four remaining rungs, and it is worse there, because
those rungs are not merely rich, they are rich *in a way that is keyed to a feature the policy can
read*.

## Two consequences that change the standing diagnosis

**1. "It learnt capital preservation, not production" is dead.** That headline described an earlier
checkpoint. Update 1800 spends **$2,840 of its $3,000** and finishes on $220, losing 32/32 in both
seatings. It is not frugal. It is dormant for ten days and then buys a farm it cannot run. Fable's
independent replay found the same thing from the other direction — draining to $2 against a
do-nothing opponent.

**FEED is also no longer zero.** It fires 1,071 times (1.23% of live-unit actions) in seat 0 and
1,609 (1.82%) in seat 1, with `cFEED` commitments chosen 2-3% of the time. The handoff's "FEED
fires ZERO times" is stale.

**2. It compounds the terminal-blindness finding rather than competing with it.**
See `critic_terminal_blindness_2026-08-03.md`. A critic that cannot tell a won position from a lost
one near the end has no way to learn that a crew of ten on day 11 with $2,900 is fatal while the
same crew on day 20 with $30,000 is correct. The value function is exactly the machinery that would
have to represent "this purchase is affordable *given how much season is left and how much I have*",
and it is the machinery measured as near-flat.

## What follows

1. **Audit the d10/d15/d20/d25 rungs** — handoff item 4, no longer read-only-and-optional. This is
   now the leading candidate for the whole failure. The question is whether those rungs should be
   drawn from states the policy could plausibly reach, or matched on assets rather than on day, or
   have their day feature masked.
2. **`states_at_day(0)` is still returning replay states** — $476, 7 units, `step_index` median 24
   (day 1), not a game start. Training now special-cases day 0 to `J.reset` so the live run is
   fine, but the function itself was never fixed and the next caller will get the old bug.
3. **The policy has no feature for what a crew costs to keep.** `glob` carries `hire_afford` — the
   price of the *next* hire against the bank — and nothing for the recurring cost of the crew it
   already has, because from the simulator's point of view there is no such thing: every morning is
   a fresh purchase. A "cost to re-hire current crew, as a share of bank" feature would be a fact,
   not a judgment, and the same side of `CLAUDE.md`'s line as `land_afford`. **Suggestion only —
   not implemented.**
4. Fable predicted this shape unprompted, before anyone read the upkeep code: *"a background wage
   drain that's small early (few hired) and steepens if hire frequency or crew size increases
   mid-game"*, on the grounds that inaction is smooth and cannot produce a cliff. See
   `fable_advice_recovered_2026-08-03.md`.

## Reproducing

```
PYTHONPATH=. python3 scripts/play_checkpoint.py <ckpt> --games 32 --opponent farm
```

The `money flow per day` block is the new output. `data/logs/cliff_decomposition.log` holds this
run.
