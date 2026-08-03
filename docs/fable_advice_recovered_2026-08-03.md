# Recovered Fable advice, and what the handoffs lost

Recovered 2026-08-03 from the raw subagent transcript on disk:
`~/.claude/projects/-Users-alexchilton/a522e0b6-46a0-4c9e-bdf8-a38edc713f46/subagents/agent-a0a3c1416854dd80b.jsonl`
(`meta.json`: `"model":"fable"`, `"description":"RL learning-signal opinion"`) — a **four-round**
consultation from the session that wrote `HANDOFF_2026-08-03.md`.

**Read this before planning any curriculum work.** The handoff compressed four rounds into two
bullets and lost the ordering, which was load-bearing.

## 1. The case against the chain rung, at full strength

The handoff's two reasons are real but are a lossy compression. What was lost:

1. **The no-op control is not insurance — it is nearly the whole experiment.**
   Verbatim: *"if feed doesn't fire in days 1-3, that's close to sufficient on its own"*.
   A single missing FEED in the first three days already calls it. The handoff's "deploy only with
   a no-op control alongside" makes this sound like a costly extra arm. It is not.

2. **The "hold" has an expiry date, and the handoff records it as a general objection.**
   Verbatim: *"Adding new curriculum machinery on top of a foundation that changed hours ago
   reproduces the exact confound problem that made this whole investigation hard — you won't be
   able to tell whether any effect you see is the chain rung or the day-0 fix finally taking hold.
   Get one clean baseline first."*
   **Once a clean baseline exists under the corrected day-0 curriculum, this specific reason
   lapses.** It was never an argument that the rung is a bad idea.

3. **Fable never argued to kill it.** Across all four rounds the position is consistently
   "hold, with a cheap and nearly-conclusive control, until the preconditions clear".

4. **The cliff decomposition was ordered first by direct instruction**, not as an independent
   editorial choice. Handoff item 1 gets the sequence right but not the provenance — worth knowing
   before anyone resequences it.

## 2. Reverse-curriculum resume points — ranked ABOVE the chain rung, not a nice-to-have

The handoff calls this a "better follow-up". That undersells it. Verbatim:

> "A better intervention than the chain rung: build the curriculum start-states from the policy's
> OWN reachable states, not a scripted 'good economy' state. This keeps the actual mechanism that
> made `commit.py` work — get the payoff inside a horizon the value function can see — without the
> gifting problem… Concretely: sample resume points from the current policy's own rollout
> trajectories, at the moment just before a natural payoff opportunity exists (animals hungry +
> wheat present, crop ripe and harvestable), with cash intact, and start a fraction of episodes
> there. Push the resume point progressively earlier (backward curriculum / reverse curriculum
> generation, a known technique) as the near-payoff segment gets mastered."

And on ranking:

> "I'd still run the chain rung too (it's already built), but gated by the no-op control… and I'd
> treat the reverse-curriculum version as the **higher-value follow-up rather than a replacement**
> — it's more likely to produce something that transfers back to a true $3,000/day-0 start rather
> than relocating the failure to a different fixed point."

**Mechanics as given:**

- **Sampling.** During ordinary rollout, or a replay pass over recent checkpoints, scan the
  policy's own trajectories for payoff-adjacent states — animal hungry with wheat in the shed
  (FEED legal and consequential), crop ripe (HARVEST legal), cash intact — and bank those as
  resume points. Same "given, not judged" move `jax_obs` already makes for `is_ripe`/`needs_feed`.
- **Mastery criterion — a real gap.** Fable gave only the general reverse-curriculum pattern (walk
  the start point backward as the tail segment stops failing) and **no numeric threshold**. Something
  like "FEED/HARVEST fires within N turns of the resume point in ≥X% of episodes over a rolling
  window" would have to be designed, not retrieved.
- **Why its failure mode is better.** Verbatim: *"if it decays in 2-3 days, that decay is diagnostic
  of the policy's own maintenance failure rather than a mismatch between a hand-authored ideal state
  and what the policy can actually reach and sustain, which is exactly the confound risk in the
  current chain-rung proposal."*
  With the chain rung a bad outcome is ambiguous. Here it has one explanation, because the state
  came from the policy itself.

## 3. Advice that never reached any handoff

- **[High confidence] Shrink the 6-member league.** Verbatim: *"Shrink the 6-member league… More
  league members is more surface area for the next version of that bug \[the pool-identity
  chimera\], for a return you've already established isn't the constraint."*
  **This is in no handoff document and nothing since supersedes it.** Raise it with Alex as a
  standalone suggestion; do not action it silently.

- **[Medium confidence — methodology] Ask whether an aggregate's underlying entity is well-defined
  before reaching for a mechanism explanation.** Fable's own stated lesson from getting the
  seat-advantage call wrong: *"the tell was sitting right in the Fact-1 data… I should have flagged
  'is the opponent being measured well-defined as a single entity' as a prior question, before
  reaching for a game-mechanics explanation."*
  This is CLAUDE.md's "a metric can be correct per row and still meaningless" arrived at
  independently from a different failure. Worth cross-referencing the two.

- **[Retracted — do not resurrect] Seat advantage as the cause of `wr_pool` 0.97-0.99.** Argued
  across rounds 1-2, wrong, and Fable says so itself: *"Own the miss up front: the seat-advantage
  call was wrong… What I got wrong was the hypothesis itself."*
  **Keep the method, discard the hypothesis** — the mirror-match design it proposed (identical
  weights, swapped seats, ≥300 games) was sound and is what was actually run (54/48, noise).

## 4. Provenance of things already shipped

Confirmed against current code, and not attributed anywhere in the docs:

- `--hand-prior 0.05` — round 3, *"NOOP_P: 0.05 (down from 0.15)"*. Matches the live launch exactly.
- `COMMIT_PRIOR_SHARE = 0.40` (`train_jax_rl.py:706`) — exactly Fable's round-3 number:
  *"40% is a defensible working number… raw flat-token share ≈ 21.7%… weighting by ~2x gives
  roughly 40-45%"*. The class-split at `train_jax_rl.py:789-810` is the mechanism it defended as
  structural rather than strategic. The handoff's "Do not touch" cites the very evidence Fable
  predicted would be the tell.
- Idle at 5%, day-0 only — round 2, adopted, confirmed correct in round 3.
- Handoff items 2, 4 and 6 (decouple KL, audit d10/d15/d20, BC accuracy by op class) are all
  Fable's, near verbatim.
- **The pool-seat fix was NOT Fable's.** It guessed seat advantage; the real pool-identity-redraw
  bug was found independently.

## 5. Why item 3 was wrong three times running

**The consultation format is the direct cause, and it is worth recording as a process failure.**

Round 1's opening instruction: *"Do NOT read any files or run any tools — everything you need is
below."* Necessary for what round 1 was (a fast, cheap gut-check). **Still in force in round 4**,
when Fable made the value-function recommendation for the third time:
*"day/turns-remaining/asset-state features into the value function. This was flagged twice already
and hasn't moved."*

**Fable never once checked `jax_obs.py`. It could not. Nobody else did either, for three rounds.**

So the lesson is not "Fable was wrong". It is: *a subagent that is explicitly forbidden from reading
the code cannot verify a claim about the code, and its repetition of that claim is not
corroboration.* Three repetitions of an unverified claim read as mounting evidence and were one
claim counted three times.

Separating what was right from what was wrong:

- **Wrong: the causal story.** `jax_obs.py:255-256` has had `day/30` and `hour/24` in `glob` since
  the first commit. There is no width to add.
- **Right: the symptom.** *"a value function that has to infer game phase from scratch instead of
  being told it"* described something real. The critic has the feature, uses it in the right
  direction, and the effect is ~0.02-0.03 across a whole season — negligible next to how badly it
  fails to approach 0/1 near a settled terminal (0.12-0.33 in real, unambiguously lost games).
  **Not blind to phase. Blind to terminal certainty** — a narrower defect no wider input can touch.

## 6. New: both curricula are candidate treatments for terminal-blindness

Fable's own new analysis, not from the original consultation:

Starting at day 25 collapses episode length from ~719 turns to ~120, which at horizon 32 raises how
often a rollout window contains a **real terminal transition by roughly 5-6x**. `train_jax_rl.py`
already records terminal rows at ~0.14% of a full-length batch even with `--n-phases 12` active.

So both curricula are candidate treatments for the terminal-blindness problem, **independent of
anything they teach about feeding** — a use neither the consultation nor the handoff considered,
because the finding did not exist yet.

**This promotes the reverse-curriculum resume points specifically**, over the chain rung, as the way
to test it: same short-episode terminal density, without the state-gifting confound, so the result
is interpretable as being about the critic.

**If run for this purpose the metric is not bank and not win rate** — it is whether `V` at those
denser terminal rows starts spreading toward 0/1, i.e. re-running the `value_along_real_game.py`
probe against a checkpoint trained with more terminal-dense episodes in the mix.

**Do not let the two questions merge.** If the chain rung is run at all, keep it scoped to its
original question (did the policy learn the last link) with the no-op control. Merging them is the
same confound the whole session was fighting.

## 7. Fable predicted the wage-bleed cliff, unprompted

Round 4, before anyone had looked at upkeep code, offering a leading candidate for the
-21/day → -552/day shape:

> *"a background wage drain that's small early (few hired) and steepens if hire frequency or crew
> size increases mid-game"*

— on the grounds that a pure frugality story cannot produce a cliff, because inaction is smooth.

What has now been found in the source is a cleaner version of the same shape: **there is no upkeep
line at all** — `_end_of_day` and `_night` move no money — but `n_units` resets to 1 every night, so
sustaining a crew of N costs the full Fibonacci `sum(HIRE_COST[:N])` **again every morning**. A crew
of 8 is $54/day, 12 is $376/day, 14 is $986/day. Negligible for a small crew, brutal for a large one
— exactly the predicted signature, though driven by crew size rather than the feed-linked mechanism
Fable specifically guessed.

**Next check:** whether crew size in the farmer replay actually grows across days 10-15 in a way
that lines up with the per-day dollar figures. That is what `jax_sim.step_accounted` and the
`play_checkpoint` accounting were built for.
