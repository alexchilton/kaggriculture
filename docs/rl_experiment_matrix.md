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

### 2. BC as KL prior — **blocked, and deprioritised**

**Stop new investment here.** Making BC trustworthy as a prior now needs the op-head fix *and* its
own version of the market-head correlation fix, which converges on the same architecture work the
non-BC path needs anyway, plus all the BC-specific collection, calibration and gating on top. That
is strictly more expensive for the option whose selling point -- encoded skill -- is the part
flagged as risky. Ender reached 8th place with no imitation learning at all.

Let the retrain and gate finish, since they are sunk. If the gate passes, keep the checkpoint as a
cheap frozen opponent. Do not start DAgger round 2 or build loss-reweighting on spec.

**If the gate fails, the order is fixed** -- written down now so it is not re-argued under time
pressure:

1. **DAgger round 2 with `mix_expert > 0`.** The parameter already exists in `dagger.py`; round 1
   used 0.0 deliberately. Letting the expert occasionally take a turn carries the rollout *past* the
   stuck point, so the labels stop being 21,570 near-identical "walk toward the field" examples and
   start containing WATER, PLANT and HARVEST. This is the fix for both the coverage problem and the
   directional-bias risk at once.
2. **Only then** build per-row loss weighting. It is a real code change -- `loss_fn` threads a
   `live` mask and nothing else -- so it should not be built speculatively.
3. **Hand prior as the fallback**, not the first move, because DAgger stays diagnostically
   informative even when it is slower.

**And on the runtime kick, which is a different question with a clean answer: kick the data
collection, never the deployed checkpoint.** A scripted override inside `dagger.py`'s rollout is the
same category as using `converter` as the expert at all, which `CLAUDE.md` blesses, and it directly
produces the richer corrective set point 1 is after. Baked into the artifact used as a prior it is
something else -- a heuristic wearing a BC label, with a new hand-tuned dial for when the kick fires
-- and at that point row 1's hand-specified prior is strictly cleaner: the same non-adversarial
guarantee, no pretence of encoding skill it does not have.


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

### 6. Autoregressive decode over market heads — ~half a day, and it is a real bug

**This row was nearly struck off for the wrong reason.** It was assessed by asking "will it fix the
spawn deadlock?" -- correctly answered no, twice, because each unit's mask depends only on its own
position and the T=1 sampling result shows that marginal is the whole problem. But Ender built
micro-steps for **action-space explosion**, and we have that independently, measured three times:

- greedy argmax over per-head marginals emits **zero** market orders, because nine independent
  "probably not sell" decisions compose into "never sell";
- independent sampling from the same marginals banks **$1**, firing combinations the joint
  distribution never produces;
- the marginals themselves are *good* -- 12:1 discrimination on `buy_product` -- so the decode is
  destroying information the network has.

`jax_policy.py` states the assumption plainly: "conditionally independent given the state, so the
joint log-prob is the sum -- exact, not an approximation". True for scoring a log-prob. False for
producing an action. It is a mean-field factorisation, and a teacher liquidating the shed is making
one coordinated decision across products, not nine coin flips.

**Scope is much smaller than the 2-3 days first estimated**, because only the six market heads need
it -- there is no evidence one hand's op must condition on another's:

| version | cost |
|---|---|
| one coarse "trade today, roughly how much" head that the nine product heads condition on | ~half day |
| autoregressive decode over the ten order slots `Game._order_book` already uses | ~1-1.5 days |

- **sequencing:** it does not block the deadlock and does not compete with rows 1-5. A policy can
  escape spawn, plant, water and harvest with the market heads exactly as they are. What it caps is
  *monetisation* -- roughly $30k of `contrarian`'s $51k is optimal execution -- so do it after PPO
  demonstrably explores, and before trusting any measured ceiling on banked money.
- the per-head thresholds in `neural.py` are a hand-tuned workaround for this, and need
  recalibrating for every checkpoint. This replaces them.

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
