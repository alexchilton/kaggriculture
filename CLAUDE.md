# Rules for this project

## Read these first

Before doing anything substantive, read in this order:

1. `docs/competition_brief.md` — what the competition is, measured facts, deadlines.
2. `docs/rl_feasibility.md` — the agreed position on RL vs planning, and why.
3. `docs/lessons_carried_over.md` — what went wrong in Orbit Wars and which lessons transfer.
4. `docs/superpowers/specs/2026-07-31-kaggriculture-agent-design.md` — the design.

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

## Kill criteria — committed up front

These were agreed before any code was written, specifically so they cannot be rationalised away later.

- Heuristic agent does not clear **$20k** final bank → the economics model is wrong, not the agent.
- Fast-sim parity harness is not exact over 1000 random action sequences → **do not train on the fast sim**.
- PPO explained variance does not pass **0.5** early → the frame is wrong, not the hyperparameters.

## Things that are settled — do not relitigate without evidence

- **Per-step bank delta is the reward, with gamma ≈ 1.0.** This is not reward shaping.
  See `docs/rl_feasibility.md` for the full argument.
  A future session will be tempted to "fix" this back to terminal-only because the Orbit Wars
  post-mortem says "never shape the reward". That ban was about *proxy* rewards. It does not apply here.
- **Legality masking is fine and expected.** MaskablePPO is the intended trainer.
  The Orbit Wars warning was about masking no-op to *force* action, which is a quality judgment.
  Masking illegal ops is a legality fact and is explicitly blessed by our own post-mortem.
- **A heuristic agent is a teacher and a sparring partner, never the final policy.**
  This is the correction to the Orbit Wars failure where heuristics became the policy and capped the ceiling.

## Environment / compute

- **Training box:** Windows machine at `192.168.1.128`, RTX 3080 Laptop 16GB, WSL2 Ubuntu.
  See the global `~/.claude/CLAUDE.md` for SSH details.
- **Do NOT train inside the vLLM venv on that box.** Its torch 2.11.0+cu126 is ABI-linked to the
  vLLM 0.23.0 compiled extension and must not be upgraded. Create a separate venv for this project.
- Make sure vLLM is not running during training runs or it will hold the VRAM.
- VRAM is not the bottleneck (see `docs/rl_feasibility.md`). Env throughput is.
- **Unmeasured:** CPU core count and system RAM on that box. Measure both when it is next powered on.

## Kaggle

- `kaggle-environments >= 1.32.2` is required. Earlier versions do not contain the `kaggriculture` env.
- **5 submissions per day.** Always test locally in the arena before submitting.
- Credentials are at `~/.kaggle/kaggle.json`. Never print or commit them.

## Scope and voice

- Global rules in `~/.claude/CLAUDE.md` apply, including scope discipline, git commit conventions
  (no Claude attribution), and semantic line breaks in long Markdown.
- Do not make changes beyond what was asked. Suggest, do not silently implement.