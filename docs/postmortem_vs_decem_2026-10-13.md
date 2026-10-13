# Post-mortem: our entry against DECEM's 5th place, 2026-10-13

Source thread: https://www.kaggle.com/competitions/kaggriculture/discussion/745367 (DECEM, posted 2026-10-03).
DECEM's code: https://github.com/Decem-Y/kaggriculture-bc.
The competition closed 2026-09-30. Nothing here can be submitted; this is lessons only.

## The numbers

Final leaderboard, downloaded 2026-10-13:

| who | rank | score |
|---|---|---|
| DECEM | 5 | 3037.6 |
| bronze cutoff (top 10%) | 1014 | 1838.4 |
| us ("alex chilton") | 2394 of 10,148 | 1480.1 |

We missed bronze by about 360 points.
Our last submission was 2026-09-24.
Our two active agents at that point were `melons_look22` (2571.3) and `v56_rc` (2309.6), from HANDOFF.md.
Both decayed against a field that kept shipping stronger forks until 2026-09-30.

## What DECEM did

- **Behaviour cloning of the top teams' newest versions.**
  An 8.2M-parameter entity Transformer, trained on about 10k replays of top agents.
  Recent games weighted up; team, version and win/loss given to the model as conditioning.
  A specialist fine-tune on one team at the end.
- **Decoding that does not compound errors.**
  Raw actions, decoded unit by unit (autoregressive), with a legality mask.
  Averaging over the top-8 plans instead of taking argmax.
  An expected-quantity accumulator for market orders.
- **Two hand rules only:** sell the overflow before the end-of-day unload, and drop off on the last day.
- **Evaluation on game flips.**
  A C++ engine, paired seeds, and a count of games that flip win↔loss, judged with a sign test.
  Forks of real ladder games as a second check (99 of 99 reproduced).
- **Keeping current was one config line:** which team's replays to clone.

## What we did

- Forks of the best public script ("chassis") plus our mods (room_guard / clamp_sells, `_ADV_LOOK`).
- Our behaviour cloning stopped on 2026-08-31 (`docs/fable_after_the_bc_ceiling_2026-08-31.md`).
  Self-driven greedy $89,665 against the teacher tape's $147,368.
  The diagnosis there: 6,818 op decisions × 719 bundle decisions at p=0.9995 each still compounds.
  It cloned one teacher's tapes, with argmax decoding.
- Our one dependable mod, room_guard + clamp_sells, is the same idea as DECEM's two rules.
  The field adopted it on 2026-09-23 (`docs/daily_2026-09-23.md`), and the edge went with it.
- Every new public chassis was ported by hand.

## Where the gap came from

1. **One submission gate was on dollars, once.**
   The project's objective was wins throughout: the RL reward was terminal 1/0 (`docs/rl_feasibility.md`), and HANDOFF.md says to rank builds by win rate.
   The exception was the chassis-submission gate set on 2026-09-22: t>3 on dollar margin on both seed blocks.
   On 2026-09-25 (`docs/daily_2026-09-25.md`) it blocked `igagent_look22`, which won **109 of 160 (68.1%, z=4.59)** against `melons_look22` but had t=2.20 on margin.
   That is one blocked submission, not a habit.
   It has nothing to do with the BC work.
2. **We stopped submitting on 2026-09-24.**
   With two active slots and a field that improves daily, a frozen agent loses rating.
   Six days with no resubmission is the largest single cost we can name.
   I have not measured how much rating that cost; the 2571 → 1480 drop includes all of it.
3. **Our BC collapsed off-tape because the teacher was a tape.**
   Our teacher was "a ~719-entry lookup keyed on the turn" (`docs/dagger_tape_teacher_2026-08-22.md`).
   Once the student deviated, the tape's answer was "frequently illegal and never a route back", so DAgger had no correct label to collect.
   The latches also drifted: off-tape, the melon read flipped and the rollout replayed a different tape than the board was recorded under.
   The $89,665 vs $147,368 numbers measured fidelity to the tape in dollars; they were never a win metric.

## How DECEM's BC survives deviation

He does not claim to fix deviation directly, and he ran no DAgger.
What his post describes instead:

- **Teachers that react.** ~10k real ladder games, all seats, many teams. Each label comes from an agent that was responding to the board in front of it, including boards where it was behind.
  Our labels came from one recording that could not respond.
- **Labels relative to the board, not the clock.** The task label is the next non-move action until the end of the day, and the target is a tile.
  The raw action is conditioned on the unit's offset (Δx, Δy) to that tile.
  So after a deviation the model still says "go to tile X and do Y" from wherever the unit is.
  Ours predicted op and bundle per turn, with the clock as input.
- **Decoding that keeps units consistent.** Units decoded in order, each seeing what earlier units claimed; a legality mask replaying the turn; marginalising the raw action over the top-8 plans.
- **Expected-quantity accumulator.** With argmax per step, a model unsure about timing says 0 every step and never buys.
  Our 08-22 note saw the same thing from the training side: ~79% of turns place no order, so the `qty_*` heads learned "predict zero".

**HYPOTHESIS (unverified):** the diversity of 10k reacting games is what covers the recovery states. His post gives no self-driven fidelity number to check this against.

## Our replay BC (2026-08-01) against DECEM's, side by side

We did start with BC on many replays: `scripts/bc_replay.py`, `kagg/il/bc.py`, `kagg/il/replays.py`, commits 799bed0 to 25a0b50 (2026-08-01 to 08-02).
It did not work at all: the checkpoint banked exactly its $3,000 start.
DECEM's code is at https://github.com/Decem-Y/kaggriculture-bc (read 2026-10-13).

| | ours, 2026-08-01 | DECEM, 2026-09-22 to 09-30 |
|---|---|---|
| Role | a warm start for PPO | the submitted agent |
| Teachers | 34 replays, the 25 richest seats (`--top 25`), winner seat only | ~10k episodes from the last two weeks, every seat |
| Open-loop tapes | kept; in August the winners *were* tapes (`docs/experiment_log.md` §16, 2026-08-09: senkin13's 720-turn sequence replays to 0.2%) | **dropped**: `build_census.py` removes any team replaying a byte-identical action stream twice, because they "are open-loop and teach nothing" |
| Rows | 17,975 (the cache in 25a0b50) | ~10k episodes × 2 seats × 720 steps |
| Conditioning | none; filtered to winners | team, date bucket, won |
| Encoder | entity attention over tiles, units and a global token: 3 layers, d_model 128, 4 heads (`kagg/rl/jax_policy.py`) | the same idea, larger: 237 tokens, 8 layers, d_model 256, 8 heads, 2-D axial RoPE |
| Unit label | the op this turn, moves included | the task: the next non-move action today, plus its target tile; the raw move conditioned on the offset to that tile |
| Units | independent heads, one per slot | decoded in order, each seeing earlier units' claims, with a legality mask |
| Market | independent per-product heads, argmax | per-product quantity bins, expected-quantity accumulator |
| What failed | ACTED accuracy 0.392 (ac48c95); P(move) = 6e-5 per unit-turn at the spawn state, "about one unit to ever leave the shed"; nine independent "probably not sell" heads composed into "never sell" | 5th place |

**How close we were.** The encoder was the same design at a smaller size.
Every place ours failed is a place where DECEM's design differs:

1. **Moves.** We labelled the raw move with no target, so from the spawn state "move" was noise and PASS won by 9.7 nats. His move is conditioned on a target tile, so it is predictable.
2. **Market.** Our nine "probably not" heads became "never". His accumulator exists for exactly this.
3. **Teachers.** We cloned open-loop tapes, whose actions do not depend on the board, so the board cannot predict them. He throws those out.
4. **Data.** About 18k rows against millions.

**Timing mattered.** In August the top of the ladder was open-loop tapes.
By 2026-09-10 the top agent was adaptive in all 50 worlds we tested (`docs/what_the_top_plays_2026-09-10.md`).
DECEM switched to BC on 09-22.
**HYPOTHESIS (unverified):** ladder BC only became possible once the teachers reacted to the board; in August there was nothing to clone that a model could learn from observations.
I could not re-check the August replays.
The code is intact in git (no deletions under `kagg/il`, `kagg/rl` or the BC scripts), but `data/` is git-ignored, and the data is gone.
`data/README.md` (2026-08-31) says the directory held ~91 GB; on 2026-10-13 it holds 21 GB.
The 2,814-replay archive under `data/seed_scripts/`, the `data/bc_runs/` checkpoints and the `bc_rows*.npz` caches no longer exist on this laptop.

We had three BC versions, not one:

- `scripts/bc_replay.py` (08-01): replays of the ladder winners, as above.
- `scripts/bc_dagger.py`: DAgger with a live JAX teacher; its only teacher that fed animals was `jax_rancher` at $12,078 (`kagg/il/bc.py` docstring).
- `scripts/dagger_tape.py` (08-22): DAgger with a recorded tape as teacher; it collapsed off-tape (section above).

The 1st-place recipe, BC warm start then self-play PPO with heuristic teachers, is the JAX track we built (`kagg/rl/`, `scripts/train_jax_rl.py`, `kagg/rl/league.py`).

## 4th place (thread 745119): pure BC, a draft and a corrector

betmyex. "No RL, no search." Two A100s plus free notebook GPUs.
This is the write-up closest to our BC failures, point by point.

| Their finding | Our version of the same problem |
|---|---|
| **Train on what the engine executed, not what was requested.** One teacher had 30% of requested sells filled, two others ~2%; their first teacher never executed 87% of requested goods purchases. Clean labels took a clone from 3 of 24 to 12 of 24 wins against their previous best; with the feed guard, 23 of 24. | We measured it on 2026-08-20 (7f24249): 48.75% of the teacher's SELL orders had an empty shed, "the hourly re-offer". We went the other way: we removed the play mask so the student *could* emit them, and kept training on the requested orders. |
| **Movement by an exact shortest-path rule.** Every teacher step they measured was a shortest-path step toward the next job's tile; the net predicts the tile, the rule walks. | P(move) = 6e-5 at the spawn state; "about one unit to ever leave the shed" (`kagg/il/bc.py` docstring). |
| **Validation accuracy correlated negatively with money**, rank correlation −0.86 over eight versions. They select checkpoints only by money on paired seeds. | The DAgger student reached 0.9983 bundle agreement while banking $0 (72662d1). |
| **Logit adjustment:** subtract the training class priors at play time, β = 1. +$3.2k, 44 of 48. | ~79% of turns place no order, so the quantity heads learned "predict zero" (c5f2169); nine "probably not sell" heads became "never". |
| **Rules for states the teacher never visited:** feed guard (buy wheat for unfed animals), night-shed sell, end sell. Six other "common sense" rules were neutral or negative. | Our teachers rarely fed animals; the only live teacher that fed them was `jax_rancher` at $12,078. |
| **Spurious correlations found by watching games:** a clone at 0.937 validation accuracy lost $86k because it learned "buy land when wheat per animal is low". Fixed by randomly shifting shed wheat on 30% of rows: +$45k. | The latch drift in `dagger_tape_teacher_2026-08-22.md`: off-tape, the melon read flipped. |
| **Reactive players cloned cleanly; long-horizon planners did not.** | Our teachers were open-loop tapes, the extreme case of a planner. |
| **RL gave a few thousand dollars per game** for days of GPU; relabelling the data gave more in an afternoon. | Our RL track, `docs/rl_feasibility.md`. |

They disagree with DECEM and 24th place on one point.
For them, a pooled multi-team corpus with team embeddings was weaker than one consistent teacher: a clone matched its own teacher on 88% of unit actions, while top teams agreed with each other on only 66-68%.
Their recipe was pretrain on many teams, fine-tune on one, then average the weights of two fine-tunes on the same team (+$3.3k, 46 of 48).
DECEM also ends with a single-team specialist fine-tune, so the three agree that the last stage is one team.

**The two most transferable lessons for us:** label with the executed state change, and select by paired-seed money or wins, never by imitation accuracy.

## The 1st-place team (thread 745073)

msd0110 / morim3 / Piiiiiiiii / qistripute, "BC, Self-Play PPO, and Heuristics".
Repo: https://github.com/msdsm/kaggriculture-solution.

- BC from public replays and from their own heuristic planner, alternated with self-play PPO.
  PPO is on-policy, so it trains on the student's own deviations; that is the direct fix for compounding.
- The final 10M model's lineage includes about **8.29 million self-play games**.
  Compute: up to 17 A100 + 29 A30 for the 10M run (average ~7 A100 + 20 A30), up to 26 A100 for the 20M run.
- A second BC pass on a PPO model lost **100 of 100** against the checkpoint before it, then passed it after about 60,000 more PPO games.
- "Final B" (rule-aware PPO, sequential action masks) beat "Final A" (BC/PPO + rule patch): 57.1% and 92.6% against Victor Mercklé's two agents, against 36.7% and 75.9% for A.

That is tens of datacentre GPUs, against DECEM's one RTX 5090.
DECEM's own RL at the action level moved neither margin nor win rate; his ES and PPO on a 16-dim style offset gave about +$1k per game.

Against our own RL track, this was our plan, at a different scale:

- **Same recipe.** BC warm start, terminal win/loss reward, self-play PPO, a heuristic planner as a second teacher (ours: the planner arm, $143,966).
- **Scale.** `docs/rl_feasibility.md` already says "step-bound by roughly two orders of magnitude, not capacity-bound".
  The one episode count we recorded there is 23,684, many of them curriculum starts late in the season; theirs is 8.29M games.
- **PPO from the clone died at update 0** for us (`docs/fable_after_the_bc_ceiling_2026-08-31.md`): sampled from the clone banked a median ~$16, so sampling gave PPO nothing to climb.
  Their clone came from reacting teachers, so sampling from it plays a real game. **HYPOTHESIS (unverified):** that is the difference, not the PPO settings.
- Their 100-of-100 loss after a second BC pass, recovered after ~60k games, says a dip after a warm start is normal. We never ran anywhere near 60k games past one.
- Our training pool topped out at $27,340 against a field at $90,000-$123,000. They trained against themselves and the public replays.

## 24th place (thread 745783): Macro BC + Day Compiler

ttyn4519 / Pavel Savchenkov. Repo: https://github.com/PavelSavchenkov/kaggriculture/tree/main/final_handoff.
Built in the last ~5 days, with Claude Opus 5.5.

**This is our planner track, finished.**
Our `kagg/search/dayplan.py` and `schedule_agent.py` split the same way: a schedule says what the farm does, a packer puts today's ops onto today's hands.
The difference is where the schedule came from.

| | 24th place | our planner (to 2026-09-11) |
|---|---|---|
| Macro decisions | a BC network, once per day at dawn: what to plant and buy, land, per-group counts to water / harvest / feed | one teacher's recorded schedule ("his") |
| Training data | 1.45M player-days from 29k games of strong teams; conditioned on strength, date and team | one tape |
| Day planning | ~4,000 lines of deterministic C++: routes, placement, crew size, funding, night shed room | the Python packer |
| Selling | hourly DP per product, against a learned forecast of the opponent's sales | sell rules (`_sell_the_shed_once_a_day`, late carrot) |
| Result | 24th | $129,640 against the teacher's $157,032 at the day-7 handover (`docs/the_plan_2026-09-11.md:513`) |

Why it bears on our collapse question:

- **About 30 network decisions per game, not 6,818.** One DayIntent per dawn; the compiler re-plans exactly from whatever board it wakes up on.
  A deviation cannot compound inside a day, because no learned decision is made inside a day.
- **Outcomes, not actions, as labels.** `new_cow = 2` means "two cows alive tonight"; how to get there is the compiler's job.
  The converter from expert day to label had 0 failures on 1.45M days.
- **Conditioning beat filtering.** Filtering to the strongest players lost $11.3k per game; 13x more data with conditioning raised their local win rate from 79% to 88%.

What they measured that we never did:

- **The opponent sales forecast was their largest component.** Without it, the same agent lost 20 of 20 games to itself with it, by $4.2k per game.
  An oracle of the opponent's sale *timing* was worth +$8.3k per game; of its totals, +$4.5k.
- **Many gains were denial.** Their fresh-data network won mostly because the opponent made $4.6k less. They read our money and the opponent's money separately, as DECEM did.
- **Gates:** paired games, sequential reading at 24 / 48 / 96 / 192 games, and adopt only after at least 4 seed sets.
  One 40-game mirror set "can produce a false winner".
  Beds with real opponent behaviour come first, because their own agents sell later than real teams and overrate early-selling changes.
- **Every iteration came from a lost game traced to its cause** (third sheep lost on day 0, all-or-nothing budget trim, shed overflow at night), each with a measured effect.

**HYPOTHESIS (unverified):** our planner with a learned dawn-only macro network in place of "his" schedule is the version of our work that could have competed.
We stopped the planner track on 2026-09-11 and moved to forking public scripts.

## The split between learning and rules: our "mini actions"

Alex's idea was to split where learning is used instead of all or nothing.
It was built on 2026-08-02 as multi-turn commitments, `kagg/rl/commit.py` (191e42c): a `COMMIT_*` token freezes a target, the unit walks there, and the arrival op fires on contact.
It worked in RL: COLLECT_FERT went from never to 2.01% of ops, CARE 0.07% → 1.98%, and with the BC prior restored, bank median $32 → $30,665 and vs_farm 0.589 → 0.707 (7c49e7f).

It was built deliberately small, and the top teams built the same idea without the limits:

| | our commitments | DECEM / 4th place |
|---|---|---|
| Who picks the tile | not the net: the nearest tile needing that job (`_nearest`) | the net: a pointer over all 100 tiles |
| How long | capped at `MAX_COMMIT_TURNS = 4` | until the job is done (to the end of the day) |
| Kinds | 5: WATER, HARVEST, FEED, PLANT, PICKUP | 14 tasks (DECEM), every action (4th) |
| Where used | RL only; the BC labels stayed per-step primitive ops | it *is* the BC label |

The cap was a rule, not a measurement.
The `commit.py` docstring says a longer commitment "starts scripting the unit's schedule, and then any win-rate gain belongs to the script rather than to the policy", and "If a future session finds that raising it 'works better', that is the signal it has crossed the line, not a tuning result."
The top teams crossed that line on purpose: 4th place walks every unit by an exact shortest-path rule, and 24th place scripts the whole day in C++.
The gain belonging to the script was fine; the ladder scores the agent, not the policy.

## Model size: Alex was right

Alex argued for a bigger network throughout; the project's answer was no.
The written basis is `docs/rl_feasibility.md:155-157`: "step-bound ... not capacity-bound", "Scaling the model was measured as the wrong lever".
I can find no such measurement in the repo: every BC and RL script defaults to `--d-model 128` with 3 layers, and no run at another size is recorded.
The comparison it cites argues the other way: the 2nd and 3rd places it names had 4.3M and 6.2M parameters, while ours was well under 1M (my estimate from d_model 128, 3 layers, 4 heads; not counted).
Kaggriculture's top BC agents: DECEM 8.2M, 4th place 21.5M, 1st place 10M and 20M lines (both reached #1).

A bigger net alone would not have fixed the August failures (open-loop teachers, raw-move labels, requested-not-executed orders).
But it was the one lever we argued down without testing it.

## What to take next time

- Gate submissions on win flips with a sign test, as the rest of the project already did.
- Keep resubmitting to the end. Put a resubmit on a schedule if no one is there.
- If imitation is tried again: reacting teachers (many real games), board-relative labels, and DECEM's decoder. Not a recorded tape.
- His evaluation harness (paired seeds, flip counts, ladder forks) is the part most worth copying.
- For BC: label with what the engine executed; walk units by shortest path to a predicted tile; select checkpoints by paired-seed results, never by imitation accuracy (4th place).
- Learn only the decisions that pay off on later days; plan the rest exactly (24th place). Forecast the opponent's sale timing.
