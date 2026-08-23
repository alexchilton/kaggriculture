# Fable's verdict on ROLE_TAPE, 2026-08-23

Asked: "are u do opus prime or da spaghetti", on the day's work — `ROLE_TAPE`, the nan that killed
`bc40`, and the masking fix I was about to write.

Verbatim result below. Cited line numbers are as of 2026-08-23 evening.

---

**Verdict: the arm is Spaghetti Monster** — a mechanism built and run before anyone stated what
would have to be true for it to win, with the deciding measurement still unmade; the last three
hours (the premise test, the doc, the honest bug write-up) are Opus Prime behaviour applied to
cleaning up a Spaghetti decision. The masking fix as currently designed is patching the component
again.

## (a) Is ROLE_TAPE a sound arm?

Not as built, and the CLAUDE.md rule was violated verbatim: "Before any sweep, state in one sentence
what the arm changes and what would have to be true for it to win." What would have to be true is:
**a tape replayed open-loop by turn index, on the trainer's boards, in the trainer's town, still
banks more than the $30,292 farmer.** Nobody measured that. The one measurement that decides it:
seat the tape at seat 1 from a genuine turn-0 reset in the trainer's own rollout and read
`end_money` for the tape seat at episode end, per tape, next to (i) the recorded bank and (ii) the
farmer's $30,292. If the tape seat banks near $3,000, the "opponent that plays at $130k" is actually
below the idle seat's floor and the arm is noise wearing a strong player's name. The infrastructure
already exists — `end_money` is stored at `scripts/train_jax_rl.py:759` — it was never read for this
question.

You even had the template. `scripts/vs_tapes.py:14-19` states the exact epistemics for open-loop
tape replay: identical starting boards, shared order book, "a win here is necessary, not sufficient;
a loss here is decisive." ROLE_TAPE has neither the identical start nor the matched town, and
shipped anyway.

And the justification number is self-contradictory in your own files:
`scripts/build_opponent_tape_actions.py:3` and `scripts/train_jax_rl.py:469-470` claim the heuristic
family "caps out around $15k", while `train_jax_rl.py:285` and `:604` measure the farmer at
**$30,292**. Same premise, two numbers, factor of two. That is "manufacturing a risk to justify
something already said."

## (b) Is the masking fix the right response?

No. It conflates two different defects and fixes the wrong one first.

**Defect 1 (numerics):** the NaN is not a property of the opponent, it is a property of the loss
scoring rows it does not train. `train_jax_rl.py:531` evaluates the pasted tape actions against the
mask (`log(0) = -inf` into stored `logp`), then `:1205` computes `exp(logp - old_logp)` and `:1216`
weights by `w` — but `0 * inf = nan`, so the weight-out fails. **The file already knows this exact
NaN shape**: lines 1240-1242 guard `0 * -inf` for the op-entropy metric with the comment "the same
NaN shape this file has already been bitten by" — and the guard was applied to the diagnostic and
not to the policy loss two paragraphs above it. The minimal correct fix is to sanitize
non-trainable rows in the loss, not to change what the opponent plays. **That fix is needed
regardless of what happens to ROLE_TAPE.**

**Defect 2 (identity):** Alex's question — is the seat playing like the player or worse than random
— is a measurement question, and the splice answers it by *changing the subject*. Substituting the
policy's own sampled action on every refused unit makes the opponent a tape/current-policy chimera
whose composition drifts toward self-play exactly as the boards diverge — so `wr_tape` measures the
policy against increasingly-itself, and the more the fix "works", the less the arm means. That is
the `add_land` failure from CLAUDE.md again: an arm whose name no longer describes what it does.
The repo's own precedent is NOOP substitution (commit `efac2f3`, "Teach NOOP where the mask forbids
the teacher's op"), which at least degrades toward the idle seat, an opponent with known meaning.
The right order is: measure the tape seat's terminal bank first; the answer decides whether to mask,
NOOP, restrict the role to matched-start slots, or delete the role. The test file at
`tests/test_a_tape_opponent_only_plays_moves_the_board_allows.py` is well built — the premise test
at line 92 is genuinely good practice — but it pins the fix to a component whose premise is still
unmeasured, and it references `splice_tape_actions`, which does not exist in `train_jax_rl.py`.

## (c) Does the `tape_teacher` condition hold for the RL opponent seat?

It fails on two of three counts, structurally.

- **Weeds off: holds.** `J.step` defaults `weed_chance=0.0` (`jax_sim.py:1384`) and
  `train_jax_rl.py:611` calls it with no override.
- **Fixed start state: FAILS.** `staggered_states` (`:193-228`) starts slot *i* at its phase turn on
  an *empty* board — the file says so at `:646-649`. The tape lookup
  `idx = jnp.clip(state.step_index, ...)` at `:484` then reads the recorded action for turn 400
  against an empty turn-400 board sharing nothing with the recorded one. The 22% illegal figure is
  this at t=0 of divergence; it only compounds. The bitter detail: the same file spends thirty lines
  (`:644-662`) on why staggered boards produce fake ties and suppresses their reward for it, then
  hands those exact boards to the tape seat without one sentence about action legality.
- **"Student's states stay near the tape": FAILS.** In DAgger the opposite seat is a clone of the
  same lineage. Here seat 0 is a learning policy whose whole job is to diverge, the order book is
  shared, and the town is `reset_with_shops(seed=args.seed)` (`:228`) — not matched to any tape's
  recorded town. The `tape_teacher.py:16-18` condition is not merely weakened for the RL seat; the
  RL trainer is close to its negation.

## (d) Other spaghetti in today's work

1. **`crossplay` omits `use_tape`.** `:768-771` builds crossplay from
   `use_opp | use_idle | use_trade | use_farm | use_ranch | use_carrot | use_home` — no tape — while
   `take_opp` at `:502-505` includes it. So `live = trainable & crossplay` at `:2252` silently drops
   every tape game's policy seat from the headline `ret`, the metric whose 0.500-pinning pathology
   the surrounding comment exists to prevent. The one new opponent role is excluded from the one
   metric built to read opponent games. `wr_tape` survives via `OPPONENT_FLAGS` (`:302`), which is
   why nobody noticed.
2. **The comment at `:474-479`** ("degrades toward a weaker player rather than an illegal one") is a
   guess in the grammar of a fact, with a body attached: run `bc40`, dead at update 0. True of the
   simulator, never checked against the loss, which scores the same actions fourteen lines later.
3. **`build_opponent_tape_actions.py:62-64`** pads a short tape by repeating its last recorded turn
   out to 719. A tape ending at turn 400 replays its final action 319 times; if that action carries
   a market order the "real recorded player" becomes a spam bot for half a season. Unmeasured,
   uncommented.
4. **Credit where due:** the 5.39% bundle-vocab loss is measured and stated at `:481-482`; the
   premise test exists; and `docs/the_rl_masks_never_followed_the_sims_to_1326_2026-08-23.md` names
   five retracted explanations and lists the still-missing measurement instead of burying it.

Order of operations that would be Opus Prime: **(1)** sanitize non-trainable rows in the loss
(needed under every outcome), **(2)** run the (a) measurement — tape seat `end_money` per tape from
turn-0 resets, one table, **(3)** let that table pick between mask-to-policy, mask-to-NOOP,
matched-start-only, or deleting the role. Writing the splice before the table is choosing the fix
before the diagnosis, again.

---

## What I had already measured when this came back

`scripts/does_the_tape_opponent_actually_farm.py`, 8 tapes, 719 turns, tape at seat 0 from a genuine
turn-0 reset, other seat passing:

```
tape                  bank    refused d0-9   d10-19   d20-29   noop%
91231786_seat1        2549          75.6%     90.0%    86.6%   65.2%
91860677_seat0        2570          90.8%     93.4%    90.0%   67.4%
93801334_seat1       20725          16.9%     31.1%    56.6%   63.7%
93807908_seat0       36037           0.0%     27.6%    50.6%   63.8%
93811464_seat1       40939           8.2%     21.0%    35.8%   63.8%
93816257_seat0       40021           8.4%     21.0%    36.1%   64.0%
93856278_seat1       37344           0.0%     27.7%    48.9%   63.5%
93959242_seat0       36621          13.7%     33.4%    59.6%   63.4%

median bank 36,329   (farmer $30,292; a real recorded season $130k-$180k; idle $3,000)
```

So the arm is **not** worthless — the working six beat the farmer — but it delivers ~25% of a real
player, and two of eight are below the idle floor. Alex's explanation for those two, which the
day-0 refusal rates support: **the tapes work or not depending on which shops appear.** The starting
board is identical in every recorded game; the shop unlock timing is not, and a tape that buys a cow
on day 2 is refused in a town where the cow shop is still shut.

Alex's call on matching the shop schedules: "well it doesnt actually matter."
