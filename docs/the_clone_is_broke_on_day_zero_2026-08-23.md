# The DAgger clone spends its whole stake on day 0 and is idle for 29 days

Measured 2026-08-23 22:5x, Mac, `scripts/play_checkpoint.py`, 8 games per seating against `farm`,
checkpoint `data/dagger_tape/season_final2-20260823-125700/latest.pkl`,
vocab `data/il/bundle_vocab_teacher.json` (151).
Full output: `data/logs/where_money_goes.log`.

This is the checkpoint every RL run tonight is initialised from (`--init`).

## The number

```
policy in seat 0 vs farm        W/D/L  0 / 0 / 8
  policy $  median 0   mean 0   min 0   max 0
  farmer $  median 27,164

  money flow per day (median over games), + is income
      day       sell        buy       hire       land        net
        0        150     -3,075        -12         -0     -2,936
        1         55        -33         -0         -0         22
        2        151       -103         -0         -0         48
        3         84       -138        -10         -0        -64
        5         58        -71         -0         -0        -14
        8          0         -0         -0         -0          0
       10 .. 29    0          0          0          0          0

  season totals   SELL +2,626   buy -5,503   hire -126   land -0
  bank by day     d0:2  d5:4  d10:0  d15:0  d20:0  d25:0  d29:0
```

Seat 1 is the same shape: -$2,976 on day 0, 0/0/8, bank $0 from d10.

## What it is doing instead

```
E:33.55%  W:21.08%  N:19.48%  NOOP:16.65%  PICKUP:2.66%  WATER:2.59%  S:2.32%  PLANT:0.95%
FEED:0.0101% (raw count 1)   CARE:0.0000%   HARV:0.1410%
FERTILIZE:0.0000% (raw 0)    COLLECT_FERT:0.0000% (raw 0)
```

74% walking, 17% NOOP. It is not a farm.

## Why this matters more than the shaping work done the same night

`UNPICKED 0.5` and `EXPONENT 1.0` (commit `ae54bcb`) make HARVEST pay, and they measurably work --
`shape mean` went 2.86e-05 to 6.16e-04. But a potential that pays for picking a crop cannot pay a
policy with no crops and no money to plant them. The `cHARV/cPLANT` movement tracked during
`shaped2` (0.137 -> 0.425 -> 0.357) sits on top of a policy that is bankrupt before day 1.

`hire` is **not** the leak, which is worth recording because it was the standing suspicion: $126
across a whole season. The leak is `buy` at 2x `sell`, and nearly all of it lands on day 0.

Alex knows what the day-0 purchase is; it is not re-derived here.

## Four bugs found in `play_checkpoint.py` getting this number

All four had accumulated while nobody ran the script. Each one alone made it unusable, and the
vocabulary one would have produced plausible numbers rather than an error.

1. `to_sim_actions(act, batch)` -- gained a third `tables` argument in `f75174e` (2026-08-22).
   `train_jax_rl.py:99` carries the identical note about itself.
2. The bundle vocabulary defaulted silently to `bundle_vocab.json` (197) while every current
   checkpoint is trained on `bundle_vocab_teacher.json` (151). Every bundle index is a valid index
   in both, so this raises nothing and simply plays a different order than the one learned. Now read
   from the checkpoint's own saved args, overridable with `--vocab`, and printed either way.
3. Bundle tables were built inside the traced scan, leaking a tracer -- the same fault already fixed
   at `train_jax_rl.py:392`.
4. `tree_map` over `(sim_actions, heur)` handed `jnp.where` a `None` when a scripted opponent leaves
   a market field unset to mean ORDER_NONE. Fixed by substituting zeros, which is the correct
   reading: bucket 0 of every market head is quantity zero. `train_jax_rl.py` carries the same fix
   as `_blend_seat`.

`scripts/eval_policy.py:125` and `scripts/diagnose_policy.py:114` still have at least bug 1 and were
**not** touched.
