# Independent review of the trajectory-optimisation reframe

2026-08-04. Review conducted against the source and the raw replay JSON, not against the summary docs.
Three findings that change the reframe's evidence base, two corrections to specific technical claims,
and one independent confirmation in its favour.

---

## Finding A: the replay sample is inverted -- the strongest statistics are for a NON-leader

`docs/episode_teardown_2026-08-03.md:100-104` already recorded this and it was dropped when the
2026-08-04 docs were written:

> These are not the top five... What is measured above is a strong mid-field agent at ~$145k.

**`senkin13` and `syouya tobita` are not confirmed top-ranked.** Worse, they are a **mirror match** --
536/720 identical action dicts *between the two of them* -- which is precisely the sample type
`CLAUDE.md` already warns against generalising from: *"A mirror match is not a best response."*

The only two confirmed top-tier games are the `Dmitry Larko` pair (he appears with `IY` and
`Juste Me`, all three on the 08-03 top-five list). Those are the **weakest** open-loop evidence:
97.4% units / 95.7% market. And our own docs disagree on the figure --
`docs/market_finetune_design_2026-08-04.md:21` reports 673/720 = 93.5% for the same pair.

So the airtight case (100% across six comparisons, swapped seats, different opponents) belongs to a
player of unconfirmed rank, drawn from a mirror pair we were already warned not to generalise from;
and the one confirmed top-tier data point is noisier and points the other way.

**The open item that would settle it was already named on 08-03 and never done:** pull episodes for the
actual top-five names and re-run the same turn-by-turn diff. Do this *before* building the optimiser,
not after.

**The argument that survives independently:** *"manual player" ranks #3.* A human cannot compute
genuinely reactive per-turn decisions across 720 turns under a competition clock. That claim needs no
rank confirmation and should carry the weight, rather than the `senkin13` statistic.

---

## Finding B: there are zero weed events in the entire replay dataset

All six episodes checked for any tile marked `"WEED"` across all 720 turns: **zero, in all six**,
despite `weedSpawnChance: 0.005` in the configuration.

So "`senkin13` ignores weeds" is neither supported nor contradicted -- **it is untested**. There is no
weed event anywhere in this dataset against which to test non-reactivity. The existing caveat
("does not prove the environment is fully deterministic") understates the gap.

**Execution consequence:** optimising a 720-turn script against archived seeds that drew zero weeds,
then being graded on fresh seeds, risks an unbudgeted live hit that never appeared in validation.
Validate any final script across many random seeds before trusting a pure open-loop submission, and do
not present "zero variance" as established.

---

## Finding C: the hire-count bug IS the cause of the $0 replay -- confirmed with counts

Measured directly from the recorded script:

```
senkin13:       304 total hires,  106/720 turns with >1 HIRE in the same turn,  max 4 in one turn
syouya tobita:  identical
```

And turn 1 is one of them:

```
turn 1  market: [['HIRE'], ['HIRE'], ['BUY_ANIMAL','COW',1], ['BUY_SEED','MELON',6], ...]
turn 2  hands:  [['WEST'], ['NORTH']]        <- assumes two hands ALREADY exist
```

With `Actions.hire` as a bool only one of those two hires executes, so by turn 2 there is one hand
where the script addresses two. The recorded `hands` action for the non-existent second hand
misapplies or is dropped, and that cascades: wrong unit positions -> wrong planting -> wrong
harvesting. It matches `data/logs/replay_leader.log` exactly -- the $2 divergence at turn 2 becoming a
flat $0 by day 8.

**So the corrected framing was right that this is not a root cause of the project's training failures,
but there is a narrower question that correction did not ask, and its answer is "fix it, not
optional":** the `senkin13` validation cannot succeed while `hire` is a bool, because the script
batches hires within single turns on 14.7% of turns starting at turn 1. This is a concrete, located,
testable mechanism for the divergence already measured -- not abstract "loss of fidelity". It is a
small mechanical change and does not constitute scope creep, because it is the direct evidenced
blocker on the next planned action.

*(Status: this fix was implemented on 2026-08-04 -- `Actions.hire` and `Actions.buy_land` are integer
counts in both simulators, one order slot emitted per hire. Pinned by
`tests/test_multiple_hires_per_turn.py`, whose three ground-truth assertions cite the reference source
and the replay so the rule cannot be "fixed" back.)*

---

## Correction 1: the beam-search claim in the tutorial doc is wrong

The tutorial doc claims `CLAUDE.md` rejected beam search for lacking a partial-return score to prune
on, and that a deterministic evaluator makes that rejection "expire".

Both halves are wrong:

- `CLAUDE.md` **never mentions beam search**. The misattribution is to `kagg/search/cem.py:6-12`.
- That docstring **already considered rollout-based pruning explicitly** and rejected it for a
  different reason: *"Pruning on the true objective would need a rollout per node, at which point it
  is a population method with worse sample efficiency."*

So "rollout-based lookahead" is not an expired rejection. It is a return to an option already weighed
and priced as **inferior to CEM**. The reframe therefore has to argue why *direct-trajectory* CEM beats
*gene-space* CEM -- same paradigm, richer and less lossy parameterisation -- rather than claim novelty
it does not have.

## Correction 2: the coordinate-ascent cost estimate undercounts the dimensionality

"720 x alternatives" is wrong. A turn's action is a joint over up to 24 unit slots plus a 10-slot
market queue, so true coordinate granularity is roughly **(turn x slot) ~ 17,000+** single-choice
points, not 720.

Mechanically still tractable -- checkpoint state at turn `t` and `lax.scan` the remainder across a
batch dimension, which `kagg/sim/jax_sim.py:1214,1300-1308` supports cleanly -- but the docs must state
the real figure rather than imply 720 evaluations per sweep.

---

## Confirmation in the reframe's favour

Measured directly from the replay: `senkin13`'s farmer-unit **no-op rate is 7.2%** (52 of 720), against
our executor's ~88%.

That is independent evidence that waste elimination is a real and large lever rather than wishful
thinking, and it is the one part of the reframe's cost argument that strengthened under scrutiny.

---

## Revised next actions

1. Write the failing test for double-hire-in-one-turn using `senkin13`'s actual turn-1 action. **Done.**
2. Fix `Actions.hire` to an integer count. **Done.**
3. Re-run the `senkin13` replay: does it reach ~$145k, or does the divergence point at least move
   substantially past turn 2?
4. **In parallel, pull real top-five episodes** (open since 08-03) so the optimiser's seed script is not
   anchored to an unconfirmed-rank mirror match.
5. Only then build the optimiser.
6. Before any open-loop submission, validate across many random seeds because of Finding B.
