# Fable review: the macro-action RL plan (2026-08-04, evening)

Commissioned after a session that (a) proved both simulators reproduce episode 89873723's 720-turn
tape exactly, (b) watched direct trajectory optimisation plateau at +1.6%, and (c) derived a
three-stage "macro-action layer -> RL -> seed the trajectory optimiser" plan from measurements of the
winner's tape.

The framing handed over was deliberately open ("what is the highest-value next move, and what is
wrong with the plan we have") rather than a request to validate, because `CLAUDE.md` records that
both previous wrong reviews here came from the framing, not the reasoning inside it.

**Verdict: the plan's stage 1 already exists, and stages 2-3 race a track that is already running
and has none of RL's currently-active failure modes.**

## What I had missed

`kagg/search/routines.py` (13 KB, plus `tests/test_routines.py`, both dated 2026-08-04 11:29).
Its docstring states the design this session re-derived from scratch, and states it better:

> A sub-action search cannot find the animal economy, and that is a structural fact rather than a
> tuning problem. [...] Every prefix of the chain is money-negative and every complete chain needs
> ~15 coordinated edits at specific tiles on specific days. [...] The fix is not a better optimiser.
> It is a representation in which a partial chain **cannot be expressed**. A routine emits the whole
> chain or nothing, so the valley is not crossed -- it is not in the space. What the search then owns
> is *which* routine, *where*, *when* and *how many*, which is strategy, while correctness lives in
> the decoder.

That last sentence is a sharper answer to the day-1-to-day-10 valley than either option this session
proposed. A reverse curriculum crosses the valley; a routine representation removes it.

Nine other docs dated 08-03/08-04 also went unread this session and bear directly on the questions
asked.

## The four RL failures a bigger action space does not touch

Cited by Fable from existing docs; recorded here as relayed, not independently re-verified.

| doc | measurement |
|---|---|
| `bankrupt_every_game_2026-08-03.md` | policy loses to `idle` **3,183/3,183**; never finished above its $3,000 start across 98 updates; ~55% of the batch has zero outcome variance, ~17% of rows carry terminal signal |
| `critic_terminal_blindness_2026-08-03.md` | on decisively-lost trajectories the value function sits flat at 0.12-0.33 to the final turn instead of collapsing to 0. Unfixed, ranked third, not promoted |
| `entropy_diffusion_2026-08-04.md` | run `shaped-20260804-000658`: critic `ev_signal` 0.424 -> 0.604 while the **policy got worse** (`wr_ranch` 0.931 -> 0.806). Entropy is paid on all 8,192 rows, ~11 carry terminal reward; `term_leverage` 26x and outvoted |
| `cliff_decomposed_2026-08-03.md` | the curriculum teaches a spurious day -> wealth/crew correlation; deployed policy re-hires a crew of 8-10 every morning from day 11, draining $1,192 (Fibonacci `HIRE_COST`, `n_units` resets nightly) |

None of these are decode failures. Coarsening the action space is a real answer to the joint-decode
problem the project has measured on the market heads, but it is not an answer to reward density,
critic calibration, or curriculum leakage.

## The two valley-crossing options this session proposed are both unsafe here

- **Reverse curriculum** would re-trigger the bug diagnosed yesterday. `cliff_decomposed` shows every
  rung tried so far (day 10/15/20/25) leaks a day-wealth correlation the net reads straight off
  `day/30`: `P(hire)` ramps 0.16 -> 0.44 and `P(buy_land)` ~0 -> 0.48 as a function of `step_index`
  with the board held fixed. Starting episodes mid-season with a herd already established is the same
  mechanism. It would need day decorrelated first (mask the day feature in early rungs, or match
  rungs on assets rather than day).
- **KL-to-the-winner's-tape** is a *policy* prior, not a shape prior, and `CLAUDE.md` already settles
  that this is the kind that caps the ceiling.
- **Third option Fable prefers: self-imitation learning** from the policy's own winning trajectories,
  `(R - V(s))_+ . -log pi(a|s)`. No fixed external target for PPO's gradient to fight; self-anneals as
  the critic catches up. Already planned in `entropy_diffusion_2026-08-04.md`. Its stated limit is
  real: it can only reinforce behaviour the policy already emits, so it cannot discover the animal
  chain by itself.

## The strongest argument against the plan, which I had not made

The RL track and the chain-genome search track are racing to produce **the same artifact** -- a
strong 720-turn tape -- and the search track has none of RL's open failure modes, runs on CPU, and is
already trending (`executor_livestock_broken_2026-08-04.md`: seeded CEM pop mean 0.03 -> 0.95).

Stage 3 presupposes a trained macro-RL policy would roll out a tape in a *better basin than the
winner's own*. A policy that currently loses to a do-nothing opponent 100% of the time does not make
that a defensible near-term expectation.

## Open-loop is less settled than this session relayed

`review_of_the_reframe_2026-08-04.md` already caught it the same day:

- The airtight 100%-identical result belongs to `senkin13`, whose **rank is unconfirmed**, from a
  pair that is a **mirror match** (536/720 identical actions between the two seats) -- the exact
  sample type `CLAUDE.md` warns against generalising from.
- The one confirmed top-tier player, `Dmitry Larko`, is the *weakest* evidence: 97.4% units / 95.7%
  market by one doc, **93.5% by another** (`market_finetune_design_2026-08-04.md:21`). Two internal
  docs disagree and nobody has reconciled them.
- The winner's bank curve does not distinguish the hypotheses: a fixed build-order that is optimal
  given the economics produces the same shape as an adaptive policy converged on the same timing.

The settling test is task #10 -- pull the confirmed top-five replays and rerun the diff. Named on
08-03, still not done.

## Fable's recommended order

1. Do **not** build an RL-specific macro-action layer. Reuse/extend `routines.py` if RL needs one later.
2. Finish the three diagnosed `executor.py` fixes -- herd cap not enforced (29 animals ordered against
   14 specified), feed not bought (15 wheat vs the leaders' 967), and `_do_buy_land` silently no-ops on
   insufficient money, so the fix is an unconditional `["BUY_LAND"]` at order-slot 0 every turn, "a
   decoder bug, not a search problem". Then re-run the seeded CEM chain search.
3. Run task #10 (top-five replay diff) before betting further runway on either framing.
4. On RL: fix entropy first, re-check critic terminal-blindness, and only then consider curriculum or
   priors. Do not stack a fourth mechanism on a terminal-blind critic.
5. If capacity allows, run the market fine-tune experiment -- smaller, has a committed kill criterion,
   targets a $30k-of-$51k gap independent of everything above.
