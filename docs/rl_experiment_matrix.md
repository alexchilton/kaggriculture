# RL experiment matrix

Written 2026-08-01 so that options stop being re-argued and start being crossed off.
Everything here shares one mechanism -- `--kl-prior` / `--kl-coef` / `--kl-anneal`, already committed
-- so the rows are **not** mutually exclusive and most compose.

## The failure every row is trying to beat

Per-turn PPO from random init reaches **95% NOOP within four updates** and never improves on its
initialisation.
It is rational, not broken: terminal reward pays 0.5 for a draw and 0 for acting incompetently, so a
policy that has not discovered farming is correct to stand still.
`explained_variance` sat at 0.08 against a committed 0.5 kill criterion.

The gate for every row below is the same and is cheap: **run ~50 updates and watch `noop%` in the op
census**. Falling means it is learning to act. Flat at 95% means it is not.
Second gate, only for anything using a *learned* prior: the **T=1 sampling sweep** -- `P(noop)` at
the spawn state must be well below 0.9999.

## The axes

| axis | options |
|---|---|
| **init** | random (today) / BC checkpoint (**`--init` does not exist yet**) |
| **prior** | none / hand-specified / BC checkpoint |
| **opponent** | frozen selves (today) / + idle / + BC checkpoint / + a trader |

## The rows, cheapest first

### 1. Hand-specified prior — ~1 hour, no dependencies

Ender's actual fix, and it is worth being precise that **he used no imitation learning at all**: he
reached 8th place from scratch, under $200, on this class of hardware.
His prior was two numbers -- `halt_init_prob=0.9`, `fraction_init_ratio=1:1:1:1:10` -- not a cloned
agent.

Ours is the mirror image, so the prior is roughly `P(noop) ~= 0.3` with the rest spread over legal
non-noop ops.

**Cannot cap the ceiling, and that is the point.** A two-number prior contains no strategy, so there
is no strategy to inherit. It is a *shape*, not a policy.

- cost: ~1 hour. The KL machinery is written; this is synthetic logits plus a flag.
- risk: low. Anneal to zero as Ender did.
- crosses off: "is the NOOP collapse fixable without imitation at all?"

### 2. BC as KL prior — **blocked**

Code exists. Currently unsafe.

Measured `P(noop) = 0.9999` at spawn means `log p_prior(move) ~= -9.7`, and `KL(policy || prior)`
taxes the policy for putting mass where the prior has none.
At `kl_coef=0.01` over a thirteen-unit crew that is roughly **0.044 per turn actively opposing the
one behaviour PPO needs to find** -- at the most-visited state in the curriculum, with `--ent-coef 0`
recommended alongside so nothing pushes back.
That is the NOOP collapse rebuilt through a new mechanism.

- blocked on: the T=1 sampling gate, after DAgger + label smoothing.
- ceiling risk: **real**. This is the row `CLAUDE.md` warns about -- a heuristic becoming the policy.
  Mitigation is `--kl-anneal`, which Ender found gave "significant further improvement".

### 3. BC as init — needs building, ~0.5 day

`train_jax_rl.py` has `--resume` (a PPO checkpoint) and `model.init` (random). **There is no
warm-start path from a BC checkpoint.** It was written up as plan item 1 and never wired.

- blocked on: the same T=1 gate. Warm-starting from a policy already at `P(noop)=0.9999` hands PPO
  the exact failure mode it is meant to escape.
- composes with rows 1 and 2 independently.

### 4. BC in the opponent pool — works today, currently pointless

`pool` holds the random initialisation plus frozen copies of a policy that has always been inert, so
it is entirely self-referential and cannot punish standing still.
A BC checkpoint is a network and runs natively inside the compiled scan, which `contrarian` and
`starter` cannot.

- harmless as-is, but until the T=1 gate passes it behaves like a second `--idle-frac` opponent.

### 5. Scripted trader opponent — ~2 hours

Measured: an agent that passes every turn and only trades wheat banks **$3,989** against a $3,000
start, using **zero crew actions** -- `BUY_PRODUCT` and `SELL` are absent from `_apply_unit_action`
and settle in the market phase.
It therefore *cannot draw* with a do-nothing policy, which the idle opponent can and does.

- crosses off: "is the draw available at all?"

### 6. Autoregressive micro-steps — 2-3 days, **not for the spawn bug**

Ruled out twice for that purpose: each unit's mask depends only on its own position, so sequencing
units cannot change the deadlocked unit's own marginal -- and the T=1 sampling result shows the
marginal *is* the whole problem.

Still likely needed for what it actually addresses: our joint action is 24 units x (op, crop, item,
qty) sampled independently, which is where "nine independent probably-nots compose into never" came
from.

- do **not** schedule as this bug's fix. Revisit after rows 1-5.

### 7. Bigger model — deferred

643,351 parameters against 4.3M-200M for comparable-competition finishers.
Not the binding constraint today: capacity does not fix a rational do-nothing optimum, and BC's
failure was covariate shift rather than underfitting.

## Crossed off already

- ~~tuning `ent_coef`~~ -- raised 6.7x for no measurable effect. Uniform is the wrong target in
  either direction, which is the whole reason row 1 exists.
- ~~tuning step size~~ -- `clip_frac` 0.012-0.169, well under the 0.3 warning line.
- ~~the seat-sum critic bug~~ -- `sum` 0.997-1.005, `seatL` 0.0000. Fixed, and a stale log made it
  look otherwise.
- ~~decode temperature on the op head~~ -- at T=1 it still emits PASS on all 719 turns.
- ~~"train BC longer"~~ as a fix for the deadlock -- it reproduces teachers closely at day 0 and day
  4 alike; the hole is in the *policy's* state distribution, not in accuracy.
