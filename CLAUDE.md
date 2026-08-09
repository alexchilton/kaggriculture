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
  `scripts/build_submission.py`, which refuses to ship an agent that cannot beat `starter`.
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

## Kill criteria — committed up front

These were agreed before any code was written, specifically so they cannot be rationalised away later.

- Heuristic agent does not clear **$20k** final bank → the economics model is wrong, not the agent.
- **The simulator now models the whole game: all 18 unit ops and all 6 market orders.**
  It modelled 9 and 4 of them until 2026-08-01, and the missing half was the animal economy --
  which is what actually wins games. Episode 89197802, the top two agents playing each other,
  banked $106k and $113k against our `contrarian`'s ~$38k; the winner drew ~83% of its revenue from
  milk and wool by converting bought wheat into animal products, and the runner-up traded wheat
  with `BUY_PRODUCT`. Neither play was expressible, so anything trained then could only have become
  a very good crop farmer.

  **Parity does not imply coverage, and that is how this hid.** `parity.py` built its scripts from
  `SCRIPT_OPS`, which listed only the ops the simulator already had, so the gate could not emit
  `FEED` and therefore could not fail on `FEED`. "300/300 exact" was a true statement about a
  subset. When adding an op, add it to `SCRIPT_OPS` and to `_dense_actions` in `tests/test_jax_sim.py`
  in the same commit, or it is untested by construction.

- Fast-sim parity harness is not exact over 1000 random action sequences → **do not train on the fast sim**.
  **Status 2026-07-31 (evening): PASSING. 300/300 full-length episodes exact**, across five
  configurations from a single unit up to twelve-unit crews with land buying. The JAX sim matches
  the numpy sim field for field, 16/16.

  The route there is worth remembering, because the harness was wrong twice in opposite directions:

  - It first hard-coded `n_units = 1`, so "60/60 exact" was a claim about single-unit games read as
    a claim about the simulator. **Atomic PLANT** and **hand spawning** hid behind it.
  - Widened to six unit slots, it then drove six unit *actions* whether or not the farm owned six
    units. The reference ignores a surplus action for movement and work but still counts it in the
    atomic PLANT rule, so it blocked plants no agent could ever block. That, not a simulator bug,
    is what "8/12 under hiring" was. Agents submit one action per unit owned; the harness now does
    too. Hiring was never involved -- the same failure reproduced at 1/8 with hiring switched off.

  **Update 2026-08-01: order slotting is fixed too.** It had been left alone as unreachable -- every
  pairing of `contrarian`/`heuristic`/`rancher` gave $0 of error, because agents emit sells in a
  canonical product order. Adding `BUY_PRODUCT` made it reachable on ordinary turns, since a buy
  quotes at `inventory - 1` against a book the sells have already lifted. `Game._order_book` now
  compacts a turn's orders into ten slots and `_process_market` walks them in lockstep, verified by
  a 400-turn randomised differential test of the market phase alone against `kg._process_market`.

  Two divergences remain deliberate, both RNG-stream artifacts neutralised in the gate: the weed
  spawn sequence and the shop unlock order.
- PPO explained variance does not pass **0.5** early → the frame is wrong, not the hyperparameters.
  **Scope note:** this was written for the per-turn, 720-step, full-action-space policy. The
  strategy env clears 0.89 easily, but it is a 30-step problem with 9 discrete heads and hand-built
  features -- a far easier target. Clearing it there is *not* evidence the hard frame works.

## Things that are settled — do not relitigate without evidence

- **SUPERSEDED 2026-07-31 for the strategy env — read this before the bullet below.**
  `kagg/rl/env.py` makes one decision per *day*, so episodes are 30 steps, not 720. At that
  length the credit-assignment argument for per-step decomposition no longer applies, and the
  true objective is available directly: the ladder is an Elo rating, so **terminal win/loss
  (+1/-1/0) with gamma 1.0 is what `scripts/train_rl.py` actually trains on.**
  Money is logged but never rewarded.
- **SUPERSEDED 2026-08-01 for the per-turn policy too — Alex's call, made explicitly.**
  **The reward is terminal: win 1, loss 0, gamma 1.0. Never per step.** This now applies to
  *every* policy in the project, so the per-step bullet below no longer governs anything and is
  kept only so a future session does not "restore" it from `docs/rl_feasibility.md`.

  It is also what the evidence says. Of the top finishers whose write-ups we have, four used a
  terminal signal — Felix Neumann terminal -1/+1, simjeg terminal with gamma 0.995, Isaiah Pressman
  terminal, Billy Bradley's `ender` positive-only 0/1/2 with gamma 0.998 — and none used a
  per-step bank delta. The ladder is an Elo rating, so margin does not count, and a $43k win and a
  $4k win are the same result.

  If credit assignment over 720 steps stalls, the agreed next move is a **per-game-day** signal,
  not a per-step one, and only after `explained_variance` has been checked first.
- **~~Per-step bank delta is the reward, with gamma ≈ 1.0.~~ NO LONGER IN FORCE.** Superseded by
  the bullet above for every policy. Left in place because `docs/rl_feasibility.md` still argues
  for it at length, and a future session reading that doc alone would otherwise reintroduce it.
  The argument there is not wrong about credit assignment; it was simply overruled.
- **Legality masking is fine and expected.** MaskablePPO is the intended trainer.
  The Orbit Wars warning was about masking no-op to *force* action, which is a quality judgment.
  Masking illegal ops is a legality fact and is explicitly blessed by our own post-mortem.
- **Ongoing crops yield `max_yield` once per lifetime, not per day.** Tomato is 8 units per tile
  per *season*, strawberry 6 — not 4.0 and 2.0 per day as the Object Types table reads.
  Animals are the reverse: no lifetime cap, so a goose gives 26 eggs a season against
  `max_held` of 4.
  Pinned by `tests/test_production.py`. Do not re-derive these from the published tables;
  the tables are misleading and cost this project a day-1 wrong turn.
- **A heuristic agent is a teacher and a sparring partner, never the final policy.**
  This is the correction to the Orbit Wars failure where heuristics became the policy and capped the ceiling.

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

- `kaggle-environments >= 1.32.2` is required. Earlier versions do not contain the `kaggriculture` env.
- **5 submissions per day.** Always test locally in the arena before submitting.
- Credentials are at `~/.kaggle/kaggle.json`. Never print or commit them.

## Scope and voice

- Global rules in `~/.claude/CLAUDE.md` apply, including scope discipline, git commit conventions
  (no Claude attribution), and semantic line breaks in long Markdown.
- Do not make changes beyond what was asked. Suggest, do not silently implement.