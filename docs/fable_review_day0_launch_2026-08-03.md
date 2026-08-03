# Fable's review of the from-scratch day-0 launch, and what verified

**Date:** 2026-08-03 (late). Requested before committing 20,000 updates to a config nobody had read
end to end. Every claim below was re-checked against the source here; the citations are to lines I
opened, not to Fable's summary.

## Verified findings — act on these

### 1. `--ent-coef` is not an entropy bonus in this config at all

`kl_fraction(kl_anneal, it)` returns **1.0 for the whole run** whenever `--kl-anneal` is 0, which is
the default (`train_jax_rl.py:937-945`). `blend_regulariser` then returns `reg_coef * kl_prior` and
the entropy term's weight, `(1 - kl_frac)`, is **permanently zero** (`:948-969`). Because
`--hand-prior 0.15` and `--spend-prior 0.05` are nonzero, `kl_active` is True (`:1126`), so this
applies for all 20,000 updates.

This is the *documented* default rather than a bug — the `--kl-anneal` help text says 0 "keeps it
flat, which is byte-identical to the behaviour before the handover existed", and
`blend_regulariser`'s docstring argues correctly that under Ender's structure the KL *replaces*
entropy rather than adding to it.

**The consequence is still a problem.** The shape prior is never released, so the `op` head and the
four `SPEND_HEADS` are pulled toward a static 15%-noop / 5%-spend shape for the entire run.
`hand_prior_heads`'s own docstring names the check (`:801-803`): trained spend rates must finish
**above** `spend_p`, and "a rate that sits exactly on the prior means the anneal is too slow". The
`--spend-prior` help text (`:1291-1293`) says outright "Anneal it with `--kl-anneal`." The config set
the prior without its documented release valve.

`CLAUDE.md` already carries this as a lesson — "A prior that is a shape is not a prior that is a
policy, and only the second one caps the ceiling... The test that it has not capped anything is that
trained spend rates finish above the prior, not pinned to it." Without an anneal that test cannot
pass by construction.

**Action: pass `--kl-anneal`.** The value is a judgement call; the prior is meant to be a starting
condition, so releasing it over the first fifth of the run is a reasonable default.

### 2. There is zero live-mirror self-play, by arithmetic accident

`role_p[ROLE_SELF] = 1.0 - role_p[1:].sum()` (`:1790`), and the requested fractions sum to exactly
1.00 (0.45 + 0.25 + 0.20 + 0.10 + 0.00). So `ROLE_SELF` lands at **0%**, and the trainer printed it:

```
seat-1 roles, sticky per episode: self:0%  pool:45%  farm:25%  trade:0%  idle:10%  ranch:20%  carrot:0%
```

Arguably correct rather than accidental — the code's own reason for `--opponent-frac` is that mirror
self-play has a stable 0.5 mutual-draw fixed point (`:311-315`), and the 45% pool share is still
self-play against *frozen past selves*, which does not have that failure mode. But it is a knife-edge
produced by the numbers happening to sum to 1.00, not a choice anyone made.

**Action: keep it at 0% deliberately, or lower `--opponent-frac`. Either way, on purpose.**

### 3. My learning-rate premise was wrong

I claimed `3e-5` was a *resume* learning rate. It is not. The code default is `3e-4`
(`:1239`), and `HANDOFF.md:694` records the switch to `3e-5` as adopting Ender's value; the next
full-length run after it, `ppo-20260801-194804`, is described at `HANDOFF.md:1031` as "sticky roles,
**from scratch**" and used it. So `3e-5` is the only value this project has ever run on this
architecture, fresh or resumed, and there is no LR ablation on record in either direction.

`optax.adam(args.lr)` has **no schedule** (`:1673`) — no warmup, no decay, verified by grep. Whatever
is chosen applies at full strength on update 19,999 exactly as on update 0, so a 6.7x jump to `2e-4`
sustained flat is a real intervention rather than a tweak.

**Action: settle it with a short probe** — ~300 updates at `3e-5` and at `2e-4`, everything else
identical, reading `clip_frac` and `ev`/`ev_signal` over the first 50. Those are the instruments
`CLAUDE.md` already nominates for exactly this ("clip_frac as early warning"). With a flat schedule,
an LR that does not blow up `clip_frac` early is unlikely to become dangerous later.

### 4. Two fears that do not materialise

- **The pool is never empty.** `pool.add(jax.device_get(params))` runs before update 0 (`:1702`), so a
  pool draw at update 0 is a frozen mirror of the same init, diverging as `--pool-every 25` rotates
  newer snapshots in. No wasted slots.
- **`--n-phases 256` is genuinely active and is not a repeat of B2.** B2 was `--curriculum-mix`
  overwriting the staggered state; this config passes no mix, so `cur_mix` is falsy (`:1552`) and
  `staggered_states` survives (`:1538`). One phase per game is what the docstring calls the fix
  (`:137-139`).

## On P2b's trigger

Fable chose **(a) resume before the opportunity**, sourced from the *current policy's own* rollouts —
not a scripted baseline's and not the replay archive's. The argument for (a) over (b) is that (b) is
circular: HARV measured 0.4–0.9% of actions, so waiting for the terminal action to fire and succeed
means resume points do not exist until the problem P2b exists to fix has half-solved itself. (a)'s
precondition is strictly weaker — a ripening event only needs an earlier PLANT+WATER, and PLANT ran
1–3%, so ripening events appear in the trainee's own rollouts long before harvests do.

It also named the axis that actually matters, which my framing had buried: **the data source**, not the
event type. Own-trajectory vs scripted vs archived replay is precisely the axis that discredited the
day-10/15/20/25 rungs, which were off-policy and taught "continue" rather than "create".

**Mechanism:** walk the PPO rollout buffer already collected each update; flag turns where
`harvestable`/`feedable` flips true on a tile or animal the trainee itself planted or is feeding;
record the state one turn earlier; bucket by opportunity type and day.

**Mastery criterion:** every K updates, replay 32 games resumed from each active tier under the current
policy against the scripted farm and log **W/D/L, never a bare rate** — per the standing rule that a
rate cannot distinguish "wins half" from "draws everything". Retire a tier when the win rate crosses a
bar fixed *before* looking at data (e.g. 0.75), sustained over two consecutive windows to survive the
measured ~15% seed variance. On retirement, step resume points one **opportunity** earlier in the same
trajectories — not one calendar day earlier, since the goal is the next-hardest link in the chain, not
a day index.

## On sequencing

Fable confirmed day-0-only is the right control for P1 on a mechanism rather than by assertion: a
curriculum starts episodes later, which shortens them and mechanically *raises* terminal density —
the opposite of what you want when the thing under test is behaviour at the true 0.14%.

It added a gap worth taking: the critic doc's own item 1 — measure what share of the value-loss
gradient comes from terminal-adjacent rows, with staggering on — is read-only, still not done, and can
be taken from run 1's *own* early rollouts now that `--n-phases 256` is live. Treating "run 1 → P1" as
finish-then-launch means picking P1's upweighting factor by guesswork. Instrument run 1 from the start
and the factor is known by the time run 1 is mature enough to serve as the control. Still one delta at
a time; the delta just gets sized by measurement.

## What Fable was not asked, and did not find

The `seat_loss`-versus-discount inconsistency
(`docs/seat_sum_fights_the_discount_2026-08-03.md`) was found here, independently, from the trainer's
startup banner, and was not in the brief. It changes the sequencing conclusion above: if the seat-sum
regulariser is the dominant cause of the flat critic, terminal-row upweighting may not be needed at
all. Take Fable's instrumentation advice regardless — the gradient-share measurement is read-only and
settles the question either way.
