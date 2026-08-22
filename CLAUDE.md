# Rules for this project

## Read these first

Before doing anything substantive, read in this order:

0. `docs/README.md` — the index, and what was deleted in the 2026-08-08 consolidation.
1. `docs/competition_brief.md` — what the competition is, measured facts, deadlines, env rules.
2. `docs/architecture.md` — **what the agent actually is**, and the flags that ship off.
3. `docs/REGISTER.md` — the live open/closed list. Check it before opening anything.
4. `docs/rl_feasibility.md` — the agreed position on RL vs planning, and why. The RL track is parked.
5. `docs/lessons_carried_over.md` — what went wrong in Orbit Wars and which lessons transfer.
6. `docs/economics_q5_findings.md` — the measured economics. Overrides the day-1 analysis.

`reference/` holds the competition docs and the full environment source (`kaggriculture.py`).
The env source is the ground truth for every rule question.
Read it rather than guessing, and rather than trusting the README where the two disagree.

## Testing discipline — NON-NEGOTIABLE

Carried over from `orbit_wars/CLAUDE.md`, because it was the single most useful rule there.

- Every theory about what is wrong MUST have a pytest unit test before any code change.
- One theory = one test. Write it. Run it. Read the output. Then fix.
- No code changes without a failing test that proves the problem first.
- No "I think the issue is X" without `assert X` in a test that fails.
- After fixing, the test must pass. That is the definition of done.

This environment is deterministic given a seed, so there is no excuse for an untested theory here.

## Measurement before theory

The Orbit Wars post-mortem's harshest finding was that half the diagnoses were guesses because
nothing was measured.
That must not repeat.

- Build the arena before building agents.
- Log explained variance and return mean/std every update, from the very first training run.
- `ret=0.00±0.00` means the reward is not reaching the algorithm. Treat it as a stop-everything signal.
- Read the logs before theorising. The tidy narrative is usually wrong.

## Lessons learned the hard way — do not repeat these

Each of these cost real time or a wasted submission. Full detail in `docs/experiment_log.md`.

- **The ladder starts at 600, not 1000.** Anything scored against the wrong baseline reads ~400
  points too harshly. v4 at 526 was genuinely losing; v5 at 613 is genuinely winning.
- **The opponent pool is diverse in crop allocation, not in play style.** Every member is
  `heuristic.make_agent` with different dials -- same routing, hiring and sell cadence. It tests
  robustness to crop mix and nothing else. Calling it "8 competing strategies" oversells it, and
  the real opponents that beat us differed in *how* they played, not just what they planted.
- **Never tune or evaluate against `starter` alone.** It sells almost nothing, so the market is
  never contested and every number is roughly **2x reality**. v4 scored $43.6k against `starter`,
  $21.2k against a copy of itself, and then lost its ranked matches at a rating of 429.9.
  Use `kagg.arena.evaluate` and the opponent pool.
- **Select on win rate, not money.** The leaderboard is an Elo-style rating. A $43k win and a $4k
  win score identically. Money is a fine dense training signal; it is the wrong selection criterion.
- **A mirror match is not a best response.** Mirror answers "what is best if both sides play it",
  which is a symmetric equilibrium. An Elo ladder rewards beating a *field*. Melon went 25 -> 12
  -> 25 because a mirror sweep pointed the wrong way.
- **Freeze the opponents.** Building pool opponents from the candidate's own parameters makes the
  opposition move with the candidate. That produced a confounded result that fully reversed.
- **Per-tile revenue rankings that ignore action cost are not decision-ready.** Cows measured
  $725/tile against wheat's $452 and are still net negative, because they need 4-6 actions a day
  plus a walk to the shed for feed. Routing was dropped as a standalone question; it came back.
- **Tuning needs held-out seeds and resampling.** A fixed 3-seed objective reported +40% where
  held-out seeds said +12.8%. And confirm a search winner on a fresh draw, or the winner's curse
  makes it wander: 11 accepted moves in 14 generations for +1.6%.
- **Seed variance is ~15%.** Identical parameters score $11.5k on one 8-seed set and $13.3k on
  another. Always quote the seed range.
- **Verify built artifacts actually run.** A hand-rolled `submission/main.py` spliced a docstring
  over line 1, failed to import, and banked exactly the $3000 start. Use
  `scripts/build_planner_submission.py`, which bundles the agent plus its schedule into one
  self-contained file and verifies the result imports and runs. Gate it with
  `scripts/gate_pool.py`, never against `starter` — see the rule two bullets up.

  *Corrected 2026-08-22.* This said `scripts/build_submission.py`, which was **deleted on
  2026-08-09** — `docs/competition_brief.md` has recorded that the whole time. It also said the
  gate is "beats `starter`", which contradicts this same file's rule that `starter` sells almost
  nothing and every number measured against it is roughly 2x reality. An instruction file that
  names a deleted script is worse than no instruction: it is followed.
- **A gate only tests what it exercises.** The parity harness drove one unit per player, so
  "60/60 exact" was a statement about single-unit games and was read as a statement about the
  simulator. Before trusting a gate, ask what it *cannot* reach. This has now cost time three
  times: single-unit scripts, then a JAX suite that passed 14/14 with no atomic-PLANT rule at all,
  then 300 full-length episodes that never once had both players selling the same product.
- **After fixing, revert the fix and confirm the test goes red.** Three of the five fixes in the
  parity work were, at first, covered by nothing: the suite stayed green with them backed out. A
  green suite after a fix says the fix broke nothing, not that anything checks it. The rare-window
  ones are the dangerous ones -- atomic PLANT only *discriminates* when `0 < seeds < demand`, a
  window that opened twice in 2,400 player-turns of random play and never landed a plant.
- **Check that a harness sends what an agent would send.** The reference's atomic PLANT rule counts
  the actions *submitted*, not the units that exist, so a harness filling every unit slot produced
  divergences unreachable in a real game -- and they were written up as a simulator bug in this
  file. When the gate and the product disagree about the calling convention, suspect the gate.
- **Unit tests verify components; only end-to-end parity verifies composition.** 136 component
  parity tests passed and a 200-step end-to-end check passed while the sim silently burned seeds on
  failed plants. The 719-step gate failed 40/40. A short parity check is a *different* test from a
  long one, not a weaker one -- slow drift is invisible until it accumulates.
- **Check whether a doc already answers the question.** The Elo scoring rule was already recorded
  in `competition_brief.md` while `rl_feasibility.md` contradicted it. Two hours of "discovery"
  was really an unresolved internal inconsistency.
- **Evaluate a technique against the problem it was BUILT for, not the problem in front of you.**
  Ender's autoregressive micro-steps were assessed here by asking "will this fix the spawn
  deadlock?" -- correctly answered *no*, twice, and the technique was struck off. But he built it
  for **action-space explosion**, which we independently have and had already measured three times:
  greedy argmax over per-head marginals emits zero market orders because nine independent "probably
  not sell" decisions compose into "never sell"; independent sampling from the same marginals banks
  $1; and the marginals are *good* (12:1 discrimination on `buy_product`), so it is the joint decode
  destroying the information, not the network. `jax_policy.py` states the assumption plainly --
  "conditionally independent given the state, so the joint log-prob is the sum -- exact, not an
  approximation" -- which is true for scoring a log-prob and false for producing an action.

  So before ruling a technique out, write down two things separately: (1) what problem its author
  built it for, and (2) whether we have that problem. Asking only "does it fix today's bug" gets a
  correct answer to the wrong question, and a correct *no* is indistinguishable from a real
  dead end.

  This applies with double force when delegating the assessment, because a reviewer answers the
  question asked. Both times a review here reached a wrong conclusion it was because the framing
  handed to it was wrong, not the reasoning inside it.

- **A metric can be correct per row and still meaningless, if its label is unstable over the thing
  it describes.** The per-opponent win rate was computed on exactly the right rows -- the live
  policy's own seat, in a finished game, against a named opponent -- and measured nothing, because
  the opponent was re-drawn every update while a game spans ~22.5 of them. A game faced a mean of
  4.9 distinct opponents; the label recorded whichever one held the seat on the final update. So
  before trusting an aggregate, ask what unit it is aggregating over and whether the label is
  constant across that unit. `farm:0.445` and a replay of the same checkpoint losing 32/32 while
  banking $0 against $30,292 were both accurate statements about different things.

- **Prefer a replay to an aggregate whenever the aggregate could be a tie.** The reward pays 0.5 for
  a draw, so a win rate near 0.5 is indistinguishable from "draws everything" -- and two policies
  that both bank $0 draw with certainty, since `money == money` is exact. `scripts/play_checkpoint.py`
  reports W/D/L and the bank curve for that reason. Every conclusion about the RL for a whole day
  came from rates that a five-minute replay contradicted.

- **Check the hardware before planning around a throughput number.** The GPU had been running at
  **210 MHz of 2100** under `SwThermalSlowdown` at 90 C, drawing 41-64 W. Every throughput figure in
  these docs was measured on a throttled card, and the "1B steps is about a month" estimate was out
  by 3x in the pessimistic direction. Cold it does ~1,100 turns/s and decays to ~370 within two
  minutes. `nvidia-smi --query-gpu=clocks.sm,clocks.max.sm` is one command and it closed an item
  that had been open as "unexplained" for two sessions.

- **Rank the ops by what correlates with winning before optimising any of them.** Across 312 real
  leaderboard seats, FEED (+0.452), CARE (+0.441) and harv/plant (+0.439) predict money, while
  PLANT (-0.358) and WATER (-0.276) predict *less* of it -- the top decile plants 1.27% of its
  actions against the bottom quartile's 3.77%. A whole day was spent celebrating a water/plant ratio
  climbing 0.30 -> 2.5, and water/plant correlates with money at **+0.100**. The measurement cost
  ten minutes and would have redirected the day.

- **A prior that is a shape is not a prior that is a policy, and only the second one caps the
  ceiling.** Ender's was `halt_init_prob=0.9` -- one number meaning "mostly do nothing", containing
  no strategy to inherit. "Buy land on day 10" is read off replays and is strategy. `--spend-prior`
  is deliberately the first kind: it says transacting is rare, never which purchase or when, and
  `--kl-anneal` decays it so it is a starting condition rather than a constraint. The test that it
  has not capped anything is that trained spend rates finish **above** the prior, not pinned to it.

- **A decision to skip a fix can expire when the problem changes.** `hand_prior_heads` declined to
  shape the market heads for a stated and correct reason: their failure was *under*-firing from a
  broken joint decode, and a flat prior would not fix a missing correlation. The autoregressive
  decode landed and the failure inverted to over-firing -- `buy_seed` on 29.1% of turns, bank at $0
  by day five. Same code, same argument, opposite problem. Re-read the reason a thing was rejected
  before assuming it still holds.

## Kill criteria and settled positions

Full record, with the measurements behind each one: `docs/kill_criteria_and_settled_positions.md`.
All of it is either MET or CLOSED. Three things still bind:

- **The reward is TERMINAL: win 1, loss 0, gamma 1.0. Never per step.** Alex's call, and what four
  of the top finishers used. `docs/rl_feasibility.md` still argues for a per-step bank delta at
  length; it was overruled, and reading that doc alone must not be allowed to reintroduce it.
- **The RL track is PARKED. An IMITATION track was opened 2026-08-22 and is not the same thing.**
  The winners submit fixed 720-turn schedules, not policies, and the shipped artifact is still the
  tape-replaying agent. Do not reopen RL without evidence that changes.

  What was opened, on Alex's direction, is DAgger from the shipped agent as teacher
  (`scripts/dagger_tape.py`, `docs/dagger_tape_teacher_2026-08-22.md`): a net trained to REPRODUCE
  the tape agent, measured by action agreement, not by reward. No reward function is involved and
  nothing about the terminal-reward ruling above is reopened.

  The RL step -- KL-anchored policy improvement on top of the cloned net -- is **still parked**, and
  is explicitly gated on the imitation step first reaching high agreement. It has not been started.
  If agreement plateaus low, the gate has not been met and RL does not open.
- **Fast-sim parity PASSES** -- 300/300 full-length episodes exact, all 18 unit ops and 6 market
  orders. When adding an op, add it to `SCRIPT_OPS` and to `_dense_actions` in
  `tests/test_jax_sim.py` in the same commit, or it is untested by construction.

## Environment / compute

- **Training box:** Windows machine at `192.168.1.128`, RTX 3080 Laptop 16GB, WSL2 Ubuntu.
  See the global `~/.claude/CLAUDE.md` for SSH details.
- **Do NOT train inside the vLLM venv on that box.** Its torch 2.11.0+cu126 is ABI-linked to the
  vLLM 0.23.0 compiled extension and must not be upgraded. Create a separate venv for this project.
- Make sure vLLM is not running during training runs or it will hold the VRAM.
- VRAM is not the bottleneck (see `docs/rl_feasibility.md`). Env throughput is.
- **Measured 2026-07-31:** 16 CPU cores and 13 GB RAM visible to WSL2 (the RAM figure is WSL2's
  default cap, raisable via `.wslconfig` if the host has more).
  Direct WSL2 SSH on port 2222 was timing out; the PowerShell fallback with `wsl bash -c "..."`
  worked, as the global CLAUDE.md warns.

## Kaggle

- **`kaggle-environments >= 1.32.7` is required** (2026-08-15 balance change, PR #1399).
  1.32.2 is only the version that first contained the `kaggriculture` env at all; it is not the
  version the ladder runs. 1.32.6 -> 1.32.7 put CARROT, TOMATO and EGG on a new `hinge` price shape,
  which our own sims did not have — `kagg/sim/market.py` died on `KeyError: 'hinge'` and
  `kagg/sim/jax_sim.py` would have priced all three at flat base **in silence**.
  Any baseline measured before 2026-08-15 describes a different game. See
  `docs/balance_change_eggs_tomatoes_carrots_2026-08-15.md` and
  `tests/test_the_market_curve_matches_the_reference.py`, which pins our curve to `reference/`.
- **5 submissions per day.** Always test locally in the arena before submitting.
- Credentials are at `~/.kaggle/kaggle.json`. Never print or commit them.

## Scope and voice

- Global rules in `~/.claude/CLAUDE.md` apply, including scope discipline, git commit conventions
  (no Claude attribution), and semantic line breaks in long Markdown.
- Do not make changes beyond what was asked. Suggest, do not silently implement.