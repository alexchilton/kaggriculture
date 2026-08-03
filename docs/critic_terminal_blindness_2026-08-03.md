# The critic is terminal-blind — and item 3 of the 2026-08-03 handoff was the wrong fix

Measured 2026-08-03. Independently verified twice: once here, once by a separate Fable session
that re-derived every number from the source rather than taking the first pass on trust.

This supersedes **TO DO item 3** of `HANDOFF_2026-08-03.md`.

## The recommendation that was wrong, and had been made three times

> **Day / turns-remaining features into the value function.** `jax_obs.encode`, into `glob`.
> Recommended three times and never done. Every symptom — oscillating `ev_signal`, weak grip on
> terminal outcomes, feed/care squeezed toward zero — is consistent with a critic inferring game
> phase from scratch.

**The premise is false and was false every time it was made.**
`jax_obs.py:255-256` has put `day/30` and `hour/24` into `glob` since commit `629bd23`, the first
commit of the per-turn policy.
`jax_policy.py:126` projects `glob` into the global token before any attention block runs, and the
value head at `jax_policy.py:212` reads `gtok`.
So the network has linear access to day and hour at layer 1.

Confirmed by holding the entire state fixed and moving only `step_index`.
Exactly two `glob` columns move:

```
col 3 (day/30):   turn 0=0.000  240=0.333  360=0.500  600=0.833  715=0.967
col 4 (hour/24):  turn 0=0.000   12=0.500  715=0.792
```

`turns_remaining = 720 - (day*24 + hour)` is an exact affine function of two columns already
present, so the input `Dense` computes it for free.
There is nothing a wider input could supply.

The stated trap — "it changes the feature width, so `migrate_params` must widen the input
projection or no checkpoint will load" — is moot, because there is no width change to make.
Had the item been executed as written it would have invalidated every checkpoint, including the
`--kl-prior` anchor that reversed this project's decline, in exchange for a redundant column.

**The lesson is not "the item was wrong".
It is that it was recommended three times without anyone once running a two-line check on whether
the feature already existed.**
`CLAUDE.md` already carries this rule under "Check whether a doc already answers the question".
It now has a second instance: check whether the *code* already answers it.

## What the symptoms actually point at

Live checkpoint `league1-20260803-054444/latest.pkl`, update 1800.
Board held fixed at the opening position; only `step_index` and money varied.

```
level  3000 v 3000   d0=0.501  d15=0.487  d29=0.499   span 0.015
ahead  9000 v 3000   d0=0.630  d15=0.649  d29=0.654   span 0.024
behind 3000 v 9000   d0=0.376  d15=0.358  d29=0.347   span 0.029
crushed 0 v 30000    d0=0.167  d15=0.166  d29=0.164   span 0.003
```

The critic **does** use the day feature, and in the right direction — ahead rises with day, behind
falls, monotone in both.
The magnitude is ~0.02 across an entire season.

The decisive case is the last turns:

```
turn 718 (day 29, hour 22):  ahead 9k v 3k = 0.664   crushed 0 v 30k = 0.169
```

One turn from the terminal, holding $0 against $30,000, the critic says **0.169**.
The correct value is 0.0 and it is not a close call.
A 3x lead on the final turn reads 0.664 instead of ~1.0.

**So this is not a critic inferring phase from scratch.
It is a critic that has learnt a static, phase-invariant map from money-lead to a probability and
has never learnt that the game ends.
The last turn of the season looks like the first.**

### The synthetic-probe confound, and why the finding survives it

The sweep above holds the board at the reset configuration while jumping `step_index` to 715-718,
which is a combination training never produces — an empty board cannot occur on day 29.
A flat response there could be an out-of-distribution artifact rather than evidence.

So the check was repeated along **real self-play trajectories** — accumulated board, accumulated
money, real turn-by-turn state — reading the critic's own value at each turn:

- **vs farm:** final $897 against $30,292, decisively lost by day ~20.
  From turn 600 to 718 — all of the last five days, all already lost — `V(seat0)` sits in a tight
  **0.12-0.14** band. Correct value 0.0.
- **vs idle:** the policy's own bank drains to **$2** by day 29 against idle's flat $3,000.
  Over the last ~30 turns `V(seat0)` sits in a tight **0.32-0.33** band. Correct value 0.0.

Both rule out the OOD explanation.
The critic does not move even when the actual accumulated board makes the outcome unambiguous
turns before the end.

## Why, and why the two shipped mitigations are not enough

The GAE terminal handling is **correct** and is not the bug.
`train_jax_rl.py:609` cuts the bootstrap on `done` and deliberately keeps it on `trunc`, with the
reasoning written out in place.

The cause is terminal sparsity, which this codebase already documents independently:
`train_jax_rl.py:954` and `:1788` both state *"the ~0.14% that carry a terminal reward (one turn in
719)"* verbatim.
The critic trains almost entirely on its own bootstrapped targets — **and a value function that is
flat in day is perfectly self-consistent under bootstrapping.**
That is the same fact as `ev` reading 0.79 while `ev_signal` oscillates around 0.4.

Two countermeasures already ship and are **active by default in the live run**:

- `seat_coef` (default 1.0, `train_jax_rl.py:1169`) — a loss term forcing
  `V(seat0) + V(seat1) = 1` on 100% of rows regardless of terminal sparsity (`:965`).
- `--n-phases` (default 12, `:1280`) — phase staggering built specifically to put
  "a genuine terminal reward in every update" (`:153`).

The checkpoint shows the collapsed response **despite both**, which is the informative part:

> **Seat-sum consistency is necessary but not sufficient.**
> It forces the two seats' values to mirror each other and says nothing about how far from 0.5 they
> should sit.
> A critic that always predicts exactly 0.5/0.5 satisfies the constraint perfectly while being
> useless.

That is exactly what the numbers show — "ahead" and "behind" sum to roughly 1 at every day, so the
constraint is holding, and the critic is still weakly calibrated around the middle rather than
pushing toward the extremes a near-certain outcome deserves.

Note also that staggering does not buy as much as it looks: 719/32 ≈ 22, so each phase group still
touches its own terminal transition only about once every 22 updates.

## The replacement TO DO item

**Fix the critic's terminal-blindness.**
Value stays in a narrow 0.12-0.33 band in real, decisively-lost games all the way to the last turn,
despite two already-shipped mitigations that target exactly this.
**Measure why they are insufficient before adding a third mechanism.**

Candidates, one test each per `CLAUDE.md`'s one-theory-one-test rule:

1. How much of the value-loss gradient in a typical update actually comes from terminal-adjacent
   rows, *with* staggering on. This is a measurement, not a change, and goes first.
2. Oversample or upweight terminal / near-terminal rows in the value loss, rather than relying on
   seat-sum symmetry alone.
3. Whether the sigmoid value head's zero-init and `vf_coef` let the value loss get outweighed by the
   policy and KL terms precisely at the rows that matter most.

### Where it ranks

**Third — the same slot item 3 held. Not promoted.**

- **Item 1** (decompose the day-10→15 cliff in the farmer replay) stays first: read-only, zero
  risk, and unrelated to this.
- **Item 2** (decouple KL from entropy) stays second and unchanged. Any experiment on the value
  loss wants entropy and KL reading cleanly to interpret its side effects, and item 2 is explicitly
  what blocks a clean read of both right now.
- This item is real, and probably underlies some of the `ev_signal` oscillation and the feed/care
  squeeze the handoff flags — but it touches the loss function, needs its own failing test first,
  and is a bigger and riskier change than either item ahead of it.

## Open, not chased

A real-trajectory replay of the **current** checkpoint (update 1800) against `idle` had the
policy's own bank drain to **$2** by day 29 — a clean loss to a do-nothing opponent.

The handoff's headline, "it learnt capital preservation, not production", and its replay numbers
(`vs carrot $2,988`, `vs farm d15:29 d20:0`) describe a different and presumably earlier checkpoint.
Which checkpoint those headline numbers came from was not chased down.

**If "capital preservation" is still being treated as the current dominant failure mode in
planning, re-confirm it against the current checkpoint first** — what update 1800 does in a real
game looks more like actively losing money than passively holding it.

## Reproducing

Scripts, written for this and kept:

- `scratchpad/check_day.py` — feature presence: move `step_index` alone, diff the encoding.
- `scratchpad/value_vs_day.py` — the value sweep and the final-turns table.
- `scratchpad/value_along_real_game.py`, `scratchpad/value_along_vs_idle.py` — the real-trajectory
  cross-check that rules out the OOD confound.

API gotchas that cost time, recorded so they do not cost it again:
`J.reset(batch)` takes batch first, not a key; `State` is a `NamedTuple`, so `._replace`, not
`.replace`; the flatten helper is `kagg.rl.jax_act._flat`, not `adapter._flat`.

**Worth promoting to a real test under `tests/`:** assert that value at turn 718 with a hopeless
position is below some threshold. Nothing currently pins it, which is why this went unnoticed for
1,800 updates.
