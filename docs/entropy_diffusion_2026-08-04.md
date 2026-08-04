# The shaped run did not hit a local maximum. It diffused.

2026-08-04. Run `shaped-20260804-000658`, resumed from `day0-long-20260803-200350/best.pkl` at
update 861, killed at update 2275.

## What was measured

Block means over 200 updates, `nan`-skipping (see the methodology warning below).

```
   upd      farm  ranch   home   pool  ev_sig    ent  op_ent  kl_pri
 861-1060   0.331  0.698  0.755  0.585   0.424   7.56   0.206   0.489
1061-1260   0.502  0.919  0.936  0.523   0.465   8.17   0.238   0.529
1261-1460   0.530  0.931  0.926  0.530   0.543   8.23   0.227   0.502   <- win-rate peak
1461-1660   0.491  0.812  0.789  0.545   0.559   9.06   0.285   0.532
1661-1860   0.458  0.797  0.765  0.515   0.605   8.70   0.263   0.488
1861-2060   0.450  0.799  0.763  0.486   0.561   9.14   0.297   0.552
2061-2260   0.476  0.806  0.770  0.509   0.604   9.86   0.360   0.673
2261-2275   0.485  0.813  0.780  0.515   0.538   9.93   0.391   0.665
```

Run config: `--ent-coef 0.01 --lr 3e-5 --shaping-coef 6.0 --value-margin 0.75 --kl-anneal 4000`,
batch 256, horizon 32, minibatch 512, 2 epochs.

## The diagnosis

**The critic improved while the policy got worse.**
`ev_signal` rose 0.424 -> 0.604, clearing the project's 0.5 kill criterion around update 1300 and
continuing past it.
Over the same span `wr_ranch` fell 0.931 -> 0.806 and `wr_home` fell 0.926 -> 0.770.

That combination rules out a local optimum.
A local optimum is entropy *collapsing* onto one confident strategy with a flattened gradient.
Here entropy *rose* monotonically -- 7.56 -> 9.93, `op_entropy` 0.206 -> 0.391 -- and `kl_prior`
drifted 0.489 -> 0.673, meaning the policy was moving steadily away from its own anchor.
The policy was becoming more random, not more stuck.

**Why entropy wins, in numbers from the same log:**

- `rewarded_frac` = 0.00137, i.e. ~11 reward-bearing rows in an 8,192-row batch.
- `term_leverage` = 26x: those ~11 rows carry 26 times their proportional share of the value loss.
- `ent_coef` 0.01 is applied to **all 8,192 rows**.

The entropy bonus is paid on every row; the win/loss objective exists on eleven of them.
The objective is outvoted, and because a more diffuse policy generates weaker returns, the effect
compounds -- which is the shape of the observed decline.

This is the fourth sighting of the same failure mode in this project.
`docs/rl_lessons_felix_neumann.md` records the entropy schedule as *the* decisive knob.
Alex's friend runs SB3 `ent_coef` at 0.0005; this run was at 0.01.

## Methodology warning: nan-poisoned aggregates

The first pass at this table used `np.mean` and reported `ev_signal` as `nan` in every block after
1061, which was read as "our one honest diagnostic stopped being written".
It had not.
`ev_signal` is non-`nan` on 86.8% of updates (1,228 of 1,415) and records through update 2275.
`np.mean` over a list containing a single `nan` returns `nan`, so 13.2% missing values erased 100%
of the signal.

The 13.2% is also correct behaviour rather than a defect.
`ev_sig_d` is `jnp.where(r_var > 1e-8, ..., jnp.nan)`, and with ~11 terminal rows per batch those
rows sometimes all carry the same return -- `terminal_ret_std` has a minimum of 0.0, i.e. every
resolved game in that batch drew.
`r_var` is then genuinely zero and the metric is genuinely undefined.

Generalisation worth keeping: **when a metric is legitimately undefined some of the time, aggregate
it with `nanmean` or not at all.** A sparse-signal run will always have undefined batches.

## On the sparse-PPO advice that prompted this

An external model was asked why sparse PPO plateaus here, and diagnosed a stable local optimum with
entropy collapse, prescribing `ent_coef` raised 2-5x.
Applied to this run that would have accelerated the failure.
It was reasoning from the environment's name -- it stated it could not find the environment -- so
the diagnosis was generic rather than wrong-headed.

Two of its framings do not survive contact with this project's own evidence:

- *"Sparse PPO fails at long horizons (>100-200 steps)."*
  Four Orbit Wars top finishers won with terminal-only reward at comparable or longer horizons
  (simjeg, Isaiah Pressman, Felix Neumann, Billy Bradley).
  The rule predicts none of them could have.
  Their fixes were scale, entropy scheduling, and action-space parameterisation -- never dense reward.
- *"Does a random agent ever succeed?"*
  We pass trivially. Reward is delivered every episode, both seats always finish, win rates sit at
  0.45-0.93. There is no exploration-to-first-reward problem here, which is the premise most of the
  advice was built on.

Correctly identified, and the one item not already tried: **self-imitation learning**.

## SIL vs BC, and which one applies

**BC** minimises `-log pi(a_teacher | s)` against a fixed external target, everywhere, regardless of
whether the teacher's action helps this policy's return.
PPO's gradient opposes it throughout, and when the BC weight anneals the policy snaps back.
That is the observed history in this project.

**SIL** (Oh et al. 2018) minimises `(R - V(s))_+ * -log pi(a | s)` -- imitate an action only where
the realised return beat the critic's prediction. Two consequences:

- The gradient is zero wherever the behaviour is not already better than expectation, so there is no
  fixed target to fight. It is PPO's own positive-advantage update, replayed.
- It self-anneals: as the critic catches up, `(R - V)_+` closes on its own. No hand-set decay
  schedule that eventually permits drift.

**SIL from the scripted executor is rejected.** That teacher banks $0 (see
`docs/executor_livestock_broken_2026-08-04.md`), so the construction is advantage-gated BC toward a
losing policy. The policy *should* fight it.

**SIL from the policy's own winning trajectories is the candidate.** It raises the effective density
of reward-bearing gradient against 8,192 rows of entropy pressure, which is exactly the imbalance
measured above.
Its hard limit: it can only reinforce behaviour the policy already emits, so it will never discover
the animal chain. It is the fix for this regression, not for the livestock question.

## Next move

One delta, against a measured regression: resume from the update-~1400 checkpoint with `ent_coef`
reduced (0.01 -> ~0.001, flat or annealed) and nothing else changed.
`ev_signal` is healthy and rising, so the critic is not the problem and should not be touched.
SIL only if the policy diffuses again with entropy controlled.
