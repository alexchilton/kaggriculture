# Fable review: is the animal-chain barrier exploration or gradient distance — and a correction to the premise

**Date:** 2026-08-03, night.
Requested to assess whether the melon-only policy's failure to engage the animal economy is a
gradient-distance problem (favoring hierarchy/options) or an exploration-probability problem
(favoring reverse curriculum), and to rank candidate fixes.

**Headline finding, ahead of everything else: the premise handed to me does not match the
project's own same-day history, and the mismatch is more informative than either of the two
hypotheses on offer.**
This project measured, today, a checkpoint where FEED fired **1,071–1,609 times per 32 games**
from a genuine day-0 start (`docs/HANDOFF_2026-08-03-evening.md` P4, confirmed in
`docs/bugs_found_2026-08-03-late.md`, and explicitly marked **"settled — do not relitigate"**:
*"'FEED fires ZERO times' is DEAD. It fires 1,071–1,609 times per 32 games."*).
The run I was asked to review — `day0-long-20260803-200350`, confirmed below to be the live run
behind the numbers in the prompt — shows FEED and CARE at a **literal, exact zero** in its most
recent raw op counts, not a rounding artifact.
So somewhere between those two checkpoints, on the same day, in the same codebase, the animal
chain went from firing over a thousand times per 32 games to never firing once.
That is not evidence of a structural barrier that requires new machinery.
It is evidence of a regression, and the same-day diff between the two configurations is sitting
in the project's own docs.
I read that diff before answering, and it changes the ranking at the end.

I also want to flag, per the instruction to challenge a wrongly-framed question: the two
hypotheses offered (exploration-probability vs. gradient-distance, resolved by hierarchy vs.
curriculum) are both live and I answer them below, but a third, cheaper, better-evidenced
explanation was sitting one `grep` away and should be ruled out first.
Doing that costs nothing new to build.

---

## 0. Which run this is, and what it actually shows

The prompt's numbers (`crop MELON:0.93`, `buyanimal` flat at ~5e-3, `feed:0.00% care:0.01%`,
bank at termination ~$16–20k, `ev 0.93`) match `data/jax_rl_runs/day0-long-20260803-200350/`,
confirmed from its `log.jsonl`: `bank_final_med: 18834.5`, `wr_farm: 0.159`, `wr_ranch: 0.224`,
`ev` in the high-0.9s in the human-readable log I tailed (`data/logs/run.log`, updates 986–995
before it was truncated by a concurrent write — the run is `kagg-train` on the Windows box,
confirmed still active).

Raw op counts from that log line (`op_counts_full`, indices per `kagg/sim/ops.py`:
`FEED=12, CARE=13, COLLECT_FERT=14, BUILD_COOP=16, BUILD_PASTURE=17`):

```
BUILD_COOP     3        BUILD_PASTURE   46        PLACE   21
FEED           0        CARE            0         cFEED (commit)   0
buy_animal_rate  [0.000122, 0.000122, 0.000244]   (GOOSE / COW / SHEEP)
```

Two things this refines beyond the prompt's summary, and both matter for the rest of the answer:

1. **`buy_animal` is not exactly zero.** It is ~0.01–0.02%, below the printed 3-decimal
   threshold — the exact rounding trap `docs/fable_review_animals_2026-08-03_evening.md` already
   caught once today on an earlier checkpoint (*"Sub-0.05% rounds to 0.000 at three decimals"*).
   So a handful of animals genuinely are bought.
2. **FEED and CARE are not rounding — they are exactly 0.0 in the raw count**, and so is the
   `cFEED` commit token. Given that BUILD_PASTURE fires 46 times and `buy_animal` is nonzero, some
   animals plausibly get bought and some pastures get built, and *still* nothing gets fed even
   once in this window. `PLACE` fires 21 times but is legal for two unrelated reasons
   (`jax_masks.py:94`: *"legal either as an animal placement or as a partial drop by the shed"*),
   so it cannot be read as 21 successful animal placements.

That second point is worth sitting with, because it is **the opposite of the working theory in
the prompt**: if the tail were the easy half — mask-legal, within GAE's reach, geometry-assisted
— then the rare animal that does get bought and housed should occasionally get fed. Zero across
this window says either the joint event (bought *and* placed *and* fed) is so rare that this
sample size cannot show it (very plausible — see the rounding point above, and the confirmed
precedent that a single update's op census undercounts what a full 32-game replay reveals), or
the tail is not actually as reliable as its mask/geometry support suggests. Section 2 gives the
cheap way to tell which.

---

## 1. Head vs. tail: the evidence says "mostly the head, but curriculum-mediated, not a hard wall"

The prompt's working theory: tail easy (mask-legal, geometry-assisted, inside GAE reach), head
hard (negative-looking one-step EV, payoff 100+ turns away, behind a weak critic). I think this
is *directionally* right but overstates how structural the head barrier is, on the project's own
evidence:

**The head has been crossed successfully, repeatedly, on this exact codebase, the same day.**
`docs/HANDOFF_2026-08-03-evening.md` P4 measured a checkpoint (`league1-20260803-054444`, update
1800) where FEED fired 1,071–1,609 times per 32 games from a bare $3,000 day-0 board — no
seeding, no forced state. `jax_masks.py:96` gates FEED on `has_animal & ~fed & carrying_wheat`,
so every one of those firings proves the full seven-step prefix (buy → build → place → pick up
wheat → carry → walk → feed) landed on its own, unaided, many times over. **That checkpoint is
proof the head is not a combinatorial wall this architecture cannot cross** — under *some*
configuration it crosses it over a thousand times in 32 games.

**What changed is curriculum composition, and the project already wrote down the mechanism.**
`docs/HANDOFF_NEXT.md` (`day0flip` section) states the tradeoff explicitly *before* it happened:
*"the flip cuts animal-op exposure ~3x (day-0 boards have no animals, so CARE/COLLFERT/FEED are
legal 0.00% at spawn)... judged acceptable — but if the animal ops die again, this is why."*
The 1,000+-FEED checkpoint ran a curriculum mix that included day-15/20/25 elite rungs, where
animals and structures already exist on 40% of training episodes (`docs/cliff_decomposed_2026-08-03.md`'s
own table: day-10 rung median 9 units and a land quadrant already in place). The current run,
`day0-long`, is — as its name says — the day-0-heavy configuration: 60% of episodes start on an
empty board with **zero** animal exposure at reset. So the policy that used to get walked past
the head's negative-looking one-step EV by curriculum seeding no longer gets that assist, and the
head's true, unassisted difficulty — buy $300–500 now, first plausible payoff 100+ turns away,
behind a critic P1 already measured as terminal-blind (`docs/critic_terminal_blindness_2026-08-03.md`:
*"one turn from the terminal, holding $0 against $30,000, the critic outputs 0.169"*) — is now
showing undiluted.

**So: gradient distance is the mechanism, but it is not a fixed property of the problem that only
architecture can fix — it is a property of the *current training distribution*, and the training
distribution changed today in a way predicted, in writing, to do exactly this.** That reframes the
choice in the prompt. Hierarchy (an option that "chooses the animal chain") would be solving a
problem that a curriculum change already solved once, then un-solved by removing the assist. The
cheaper move is restoring the assist, or replacing it with a better-designed version of the same
assist (Section 3).

I do not think this fully closes the head/tail question — the tail's exact-zero FEED count in
Section 0 is a live loose end — which is why Section 2 proposes measuring it directly rather than
assuming either side.

---

## 2. The decisive cheap experiments — two of them, cheaper than the one proposed

The proposed experiment (force the market head to buy an animal and build a pasture early, then
let the checkpoint play on) is a reasonable head-only probe, but it requires writing a bespoke
override of the market/build heads, and — more importantly — the project already has two
cheaper instruments that answer a sharper question with code that exists and has already run
today.

**2a. Re-run `play_checkpoint.py` on the current checkpoint before anything else — this is
close to free and the project has already been burned twice today by trusting the training
census's rounded percentages over a raw replay count.**
`docs/fable_review_animals_2026-08-03_evening.md`'s own headline was retracted for exactly this:
*"I claimed 'FEED has never once been legal.' That is false ... FEED fired against all four
opponents."* `docs/bugs_found_2026-08-03-late.md` marks the same claim **settled, dead, do not
relitigate**, off a different checkpoint. A training-log census over one 32-turn horizon window
has far fewer samples than a full 719-turn, 32-game replay, and the difference between "exactly
zero" and "rare but real" has flipped the diagnosis twice already today. Five minutes, no new
code, and it is the correct first move before designing anything else — including everything
below.

**2b. If 2a confirms a genuine near-zero: seed from an existing day-15/20/25 curriculum rung
(or from `jax_rancher` rollout states just after a successful FEED), not from a hand-forced
market head.** This is the same experiment the prompt proposes, generalized, and it is cheaper
to run because the machinery already exists and was already used successfully today:
`curriculum.py`'s `states_at_day` produces exactly this kind of animal-present board, and it is
what fed the 1,000+-FEED checkpoint in the first place. Concretely: run the *current* checkpoint
starting from a day-15 or day-20 curriculum-rung state (one CLI flag, `--curriculum-mix`, no new
code) and read raw FEED counts.

- **If FEED fires readily once an animal already exists on the board** — confirms the tail is
  fine and the head is the bottleneck, exactly as the prompt's working theory holds, and the
  fix is state-distribution (P2b / re-adding rungs), not architecture.
- **If FEED still does not fire even with a pre-placed, already-fed-once animal and wheat in
  the shed** — the tail itself is broken, which would contradict the working theory and point at
  something more specific: possibly the active `--kl-prior` anchor (this run logs `kl_prior`
  losses of 0.37–0.50, meaning a real, non-decayed pull toward whatever the anchor checkpoint
  does — and if that anchor was trained on an earlier, more animal-averse configuration, the KL
  term is an active force suppressing exploration of FEED specifically, independent of any
  credit-assignment argument). This is a concrete, checkable, code-level hypothesis, not
  speculation — `train_jax_rl.py`'s `kl_to_prior` and the anchor checkpoint's own op census are
  both inspectable in an afternoon.

Both of these are cheaper and more decisive than the proposed forced-market-head experiment,
because they reuse tooling and states this project has already built and already validated today,
rather than writing a new override path.

---

## 3. Ranked candidate fixes

**(d) — promoted to first: re-add an animal-present curriculum rung (or literally the old
`10:0.1,15:0.1,20:0.1,25:0.1` mix) as an A/B against the current day-0-heavy mix, before building
anything new.** This is not a new idea or new machinery — it is re-enabling a configuration that,
on this same codebase, the same day, produced 1,000+ FEEDs per 32 games. Cost is a CLI flag and a
restart. If FEED/CARE/`buy_animal` recover, the diagnosis is "curriculum regression," not
"structural barrier," and every item below can wait. `docs/p2b_state_source_2026-08-03.md`
already flags the sharper version of this — the *current* policy's own trajectories have no
payoffs to resume from, so any reverse-curriculum design needs a state source that isn't the
collapsed self-play distribution, and the elite rungs (or `jax_rancher`) are exactly that.

**(a) reverse curriculum from `jax_rancher` states via `opportunity.py` — high value, low-medium
cost, and it specifically avoids the trap `p2b_state_source_2026-08-03.md` already found.**
`opportunity.py`'s rising-edge detector (`newly_ready`, `resume_turns`) is built and 21 tests
pass; it has never been wired to a state *source* that actually produces payoffs. Sourcing resume
points from `jax_rancher` rollouts (which do reach FEED reliably, per its own docstring — it is
"the only opponent in the pool that uses the animal economy") rather than from the live policy's
own trajectories sidesteps exactly the blocker that killed the first P2b design: *"there is no
state in league1's trajectory distribution that is 'just before a payoff', because there are no
payoffs."* This is strategy-neutral in the sense `CLAUDE.md` already blesses — it changes where
episodes start, not what is rewarded, and the agent still has to win from wherever it lands.

**(b) `COMMIT_PLACE` + an `empty_structure` geometry feature — medium value, low cost, do
regardless of what else is chosen.** This is not new advice; `docs/fable_review_animals_2026-08-03_evening.md`
already identified it as *"the one architecturally missing link"* and ranked it first, on the
grounds that it follows the exact precedent `COMMIT_PICKUP` already set (measured 77% miss rate
on an unassisted FEED walk, fixed by adding a commitment) rather than crossing any new line. It
closes a real, specific, previously-measured gap — `jax_obs.py` exposes `needs_water`, `is_ripe`,
`needs_feed`, and `empty`, but nothing for "empty structure I am carrying an animal toward" — and
it is legality/geometry scaffolding, not strategy, by the same test every other `COMMIT_*` token
already passed (`commit.py`: offered uniformly, decided by the policy, never orders two ops).

**(c) longer horizon / higher `gae-lambda` — low priority, and arguably the wrong lever right
now.** The chain closing 1,000+ times per 32 games on an earlier config is itself evidence that
the absolute 20-turn GAE reach is not what blocks it in principle — a trained value function is
supposed to carry credit past the horizon truncation regardless of how long the horizon is,
*if the critic is informative*. `docs/critic_terminal_blindness_2026-08-03.md` (P1) already
diagnosed that it currently is not, independent of horizon length, and is explicitly still
unfixed. Raising horizon multiplies compute roughly linearly and does not address P1; it would
very plausibly just delay the same weak terminal signal by more turns. Fix P1 (or measure why the
two shipped mitigations for it are insufficient, which is P1's own next step) before spending
compute on a longer window for a critic that cannot use it.

**(e) hierarchical RL / an explicit livestock macro-option — do not build yet, and this is not a
fresh call.** `commit.py`'s own docstring already declined this, in writing, *despite* a measured
77% miss rate on the FEED leg alone: *"the next step is the seven-op animal-acquisition chain,
and by then the script is the strategy."* Everything measured today reinforces rather than
overturns that call: the chain has been shown to close on its own, unaided, 1,000+ times in 32
games under one configuration. That is direct evidence against "this needs a hand-authored
option to be reachable at all" and for "this needs the training distribution that already
produced it once." If (d) and (a) are both tried and the chain still cannot be induced without a
hand-built macro, that would be new evidence and would justify revisiting this — but that
evidence does not exist yet, and CLAUDE.md's own line applies directly: *"a prior that is a shape
is not a prior that is a policy, and only the second one caps the ceiling"* — a buy→place→feed→
care→sell macro is a policy, not a shape, exactly like the case the project already ruled out
once.

---

## 4. What the numbers suggest that is not in the prompt's frame at all

**The `hire` drain may be crowding out the animal purchase, independent of credit assignment.**
`docs/bugs_found_2026-08-03-late.md` measured `hire` at **-$2,122 to -$2,600 per season, larger
than the entire season's gross sales** — the single biggest line item in the game, dwarfing a
$300–500 animal purchase. A policy under pressure to fund a growing crew every single morning
(cost is Fibonacci in crew size, `docs/cliff_decomposed_2026-08-03.md`) has less slack for a
speculative purchase whose payoff is 100+ turns away than one would compute from the animal
economics in isolation. This is P3 in the current handoff and is described as merged
(`rehire_afford` feature added), but its *effect* on `buy_animal` specifically has not been
measured. Worth a look before assuming the animal aversion is purely about the animal's own
economics.

**`ranch` win rate is climbing (0.000 at update ~492 per `docs/thrift_is_optimal_2026-08-03.md`,
~0.17–0.22 by update ~990) without any FEED at all**, because `ranch` itself only banks $12,078 —
less than what pure wheat/melon farming now reliably clears. This matters for how much marginal
policy-gradient pressure currently exists to learn the animal chain at all: beating `ranch` does
not require it, and beating `farm` ($23–30k, the harder scripted opponent, `wr_farm` still only
~0.03–0.16) plausibly *does* eventually require it per `CLAUDE.md`'s economics finding, but that
is a distant, weak, low-probability-of-attribution signal compared to the cheap, immediate wins
still available from intensifying melon. This is consistent with, and probably compounds, the
curriculum-regression story above — there is currently no opponent in the mix whose defeat
*specifically* requires the animal economy, so even a correctly-functioning credit signal has a
smaller marginal incentive to explore it than the CLAUDE.md-recorded leaderboard economics would
suggest in isolation. Worth considering `farm` itself replaced or supplemented by an opponent
that banks in the $30k+ range specifically *via* the animal economy — `jax_homestead.py`'s `home`
role is a step in that direction (crops + ranching combined) and is already 6–8% of the pool.

---

## Bottom line

1. **Do not accept the flat-zero premise without a raw replay first** — this project's own
   history shows the training census has misled on this exact question twice today, in both
   directions.
2. **The head/tail question is real but is not a fixed property of the architecture** — the same
   codebase produced the tail 1,000+ times per 32 games under a curriculum that has since been
   replaced with one explicitly predicted, in writing, to suppress it. Check that before building
   anything new.
3. **The cheapest decisive experiment is re-adding an animal-present curriculum rung**, not
   forcing the market head — it reuses code that already worked today.
4. **If a fix is still needed after that**, the reverse curriculum sourced from `jax_rancher`
   (not from the collapsed policy's own trajectories, which `p2b_state_source_2026-08-03.md`
   already ruled out) and `COMMIT_PLACE` are the two cheap, precedented, non-strategy-capping
   moves. Hierarchy/options remain the last resort, not the first one, on the project's own
   standing argument and on today's added evidence.
