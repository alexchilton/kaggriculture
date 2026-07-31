# Rules for this project

## Read these first

Before doing anything substantive, read in this order:

1. `docs/competition_brief.md` — what the competition is, measured facts, deadlines.
2. `docs/rl_feasibility.md` — the agreed position on RL vs planning, and why.
3. `docs/lessons_carried_over.md` — what went wrong in Orbit Wars and which lessons transfer.
4. `docs/economics_q5_findings.md` — the measured economics. Overrides the day-1 analysis.
5. `docs/superpowers/specs/2026-07-31-kaggriculture-agent-design.md` — the design.

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

## Kill criteria — committed up front

These were agreed before any code was written, specifically so they cannot be rationalised away later.

- Heuristic agent does not clear **$20k** final bank → the economics model is wrong, not the agent.
- **The simulator models HALF the game. Read this before planning any training run.**
  It implements 9 of the environment's 18 unit ops and 4 of its 6 market orders:

  | implemented | **missing** |
  |---|---|
  | PASS, NORTH, SOUTH, EAST, WEST | **PLACE, BUILD_PASTURE, BUILD_COOP** |
  | WATER, HARVEST, PLANT, DIG | **FEED, CARE, COLLECT_FERTILIZER, FERTILIZE** |
  | SELL, BUY_SEED, HIRE, BUY_LAND | **PICKUP, DROP**, **BUY_ANIMAL, BUY_PRODUCT** |

  The missing half is the whole animal economy, and **that is what wins games**. Episode 89197802,
  the top two agents playing each other, banked $106k and $113k against our `contrarian`'s ~$38k.
  The winner drew 83% of its revenue from milk and wool, converting bought wheat into animal
  products; the runner-up drew 81% from trading wheat with `BUY_PRODUCT`. Neither play is
  expressible here. A policy trained on this simulator can only become a very good crop farmer.

  **Parity does not mean coverage.** `parity.py` builds its scripts from `SCRIPT_OPS`, which lists
  only the ops the simulator already has, so the gate cannot emit `FEED` and therefore cannot fail
  on `FEED`. "300/300 full-length episodes exact" is a true statement about the subset. Before
  quoting that number at anyone, quote this table with it.

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

  The named suspect (the reference pairs the players' *i-th market order*, the sim settles per
  product) is **real but not reachable by any agent we have**: replaying every pairing of
  `contrarian`/`heuristic`/`rancher` over three seeds gives $0 of error, because agents emit sells
  in a canonical product order. Fixing it needs an ordered order book in `Actions`. Left alone
  deliberately; revisit if an agent's sell ordering ever becomes state-dependent, which a *learned*
  policy's would.

  Three divergences remain deliberate: weed spawn sequence, shop unlock order and market order
  slotting.
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
  Money is logged but never rewarded. The bullet below still stands for any *per-turn* policy,
  where 720-step credit assignment is the problem it was written about.
- **Per-step bank delta is the reward, with gamma ≈ 1.0.** This is not reward shaping.
  See `docs/rl_feasibility.md` for the full argument.
  A future session will be tempted to "fix" this back to terminal-only because the Orbit Wars
  post-mortem says "never shape the reward". That ban was about *proxy* rewards. It does not apply here.
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