# Fable: stress-test of the Bellman route, and the `crop()` spec (2026-08-04)

Saved before relaying.
Follow-up to `docs/fable_how_to_build_a_competitor_2026-08-04.md`.
Question: is a 30-step MDP with chain-level actions and fitted-Q the route to a general agent, does
wheat-denial need it, and what exactly should `crop()` contain?

## Correction to the framing I gave it

**There are three separate RL systems in this repo, and the failures I cited belong to the one I was
not proposing to reuse.**

- `cliff_decomposed_2026-08-03.md` and `entropy_diffusion_2026-08-04.md` are both about the **raw
  720-turn per-turn policy** (`kagg/rl/jax_policy.py`, `commit.py`, seeded from
  `kagg/rl/curriculum.py`).
- `kagg/rl/env.py` `StrategyEnv` (ev 0.89) is a **third, different system** — 9 coarse buckets, no
  chains.
- The 30-step chain-action fitted-Q system **has never been built or tested**. None of the three
  measured failures is direct evidence about it. Some mechanisms transfer, some do not.

## (1) Ladder pairing, and whether wheat denial is even a thing

**Kaggle's actual matchmaking algorithm is documented nowhere in this repo.**
`ladder_analysis.md` and `leaderboard_snapshot_2026-08-03.md` measure rating *dynamics*, not the
pairing rule, and it is not in `reference/`.
So Alex's claim rests on general Kaggle simulation-competition behaviour, not on anything measured here.
Flag the gap rather than treat it as settled.

**Directionally he is right anyway, for a sharper reason:** our best submission is **600.5** against a
top-20 cluster at **2463-2723** — a 4.5x rating gap.
Whatever the pairing distribution is, the mass a 600-rated submission puts on a 2700-rated opponent is
negligible.

**But denial mostly evaporates on inspection, which makes the pairing argument nearly moot.**
`routines.py::ranch()` (lines 222-246) **already** emits `script.buy_product[d, wheat] += 1` every day
for every animal cell — it buys wheat as feed rather than growing it.
`mine_build_orders.log`: top 12 seats by money bought a mean of **1,963** wheat units a season against
the bottom 12's **128**, and this correlates with money, hires and animal count together — not with
anything about the opponent's wheat usage.

**It was never denial. It is supply-chain economics** — buying feed beats growing it on tiles that could
carry strawberry or melon, and it is unconditionally good regardless of the opponent.
`test_a_ranch_routine_pays_for_itself` already confirms `ranch()` nets positive against a passing
opponent with no denial mechanism in the loop.

The one thing not yet isolated: whether the wheat *purchase* specifically carries the value.
Clean ablation — take the CEM-winning genome, zero `buy_product[.., WHEAT]`, source feed only from grown
wheat, play against `idle`/`starter` (opponents that do not touch the wheat market at all).
Still wins → value was about our own herd, unconditional, already shipped in `ranch()`.
Collapses → value was the price effect on shared inventory, which is closer to real denial and does need
the pairing caveat.

Either way: **the unconditionally-good wheat lever is not a research question, it is a routine that
already exists and is already validated.** Nothing here justifies building a general adaptive agent to
unlock it.

## (2) Is the 30-step chain-action fitted-Q proposal sound?

**Sound as a frame, unproven as a system.** Two things would kill it, both with fixes already paid for
in this codebase.

**Genuinely defensible:**
- The day-boundary Markov argument is verified: `_end_of_day` (`jax_sim.py:1228-1236`) resets only
  `unit_pos`, `n_units`, `hires_today`, `carried`.
- Terminal reward at gamma 1.0 over 30 steps is a real, not cosmetic, improvement — Bellman backups
  propagate through 30 max-operations rather than 720.
- `StrategyEnv` clearing ev 0.89 is evidence the 30-step **frame** learns. It is **not** evidence that
  chain actions or fitted-Q work — different action space, different algorithm.

**(a) The action-space-explosion trap recurs one level up.**
CLAUDE.md's hardest-won lesson: independent per-head argmax on a factored action destroys the joint
action — nine independent "probably not sell" marginals compose into "never sell".
If a day's action is several independent discrete heads ("which chain, which block, which crop, how
much") under standard DQN argmax, **the identical failure rebuilds itself with chains as the
vocabulary**.
Either transplant the autoregressive/op-conditioned decode that already fixed it, or restrict the
day-action to a small **enumerable catalog** —
`{ranch(COW,·), ranch(SHEEP,·), crop(WHEAT,·), crop(MELON,·), buy_land, sell-cadence-adjust, no-op}`,
each parameterised by a handful of StrategyEnv-style buckets rather than raw tile/day — so one joint max
is tractable.
This must be decided **before** the network is written, not discovered after training stalls.

**(b) The curriculum day→wealth leak is not specific to the per-turn action space.**
The mechanism (day feature at layer one, monotone `P(hire)`/`P(buy_land)` ramps, no threshold needed
given `HIRE_COST`'s Fibonacci convexity) is about what the training data shows the network.
Seed 30-step chain episodes from replay snapshots the way `states_at_day` does and you hand the value
function the same "day ≥ 10 implies a farm" correlation, with 30 decision points to notice it in instead
of 720.
Given day index has to be in the state, this is the single most important thing to guard.

**(c) `entropy_diffusion`'s specific mechanism does not transfer** — there is no entropy term in a TD
loss.
But its root cause does: a replay buffer dominated by draws and constant losses gives few informative
Bellman targets.
`bankrupt_every_game_2026-08-03.md` recorded the `pool` opponent alone producing **63% exact-tie draws**.
Rerun that per-opponent breakdown on any new system before trusting a win rate from it.

## (3) The state vector

Use `StrategyEnv._observe()` (`env.py:134-153`, 41 dims) as the template — it under-serves two
constraints.

**Include:**
- **Money, own and opponent, log-scaled**: `sign(x) * log1p(|x|) / log1p(150_000)`.
  `StrategyEnv`'s linear `/50_000` compresses the entire **$0-$3,000 opening — where land-day and
  first-hire decisions live — into 0-0.06 of the range**, and clips $250k and $150k to the same 1.0.
  The season spans four orders of magnitude.
- **Days remaining, not day index**: `(30 - day) / 30`.
  It is the quantity that governs affordability (a chain must earn its cost back before the season
  ends), and raw `day/30` is exactly the feature found being read as a wealth proxy.
- **Derived affordability ratios rather than raw day + cash separately** — `cliff_decomposed`'s own
  unimplemented suggestion: `recurring_hire_cost / (money+1)`, `next_land_price / (money+1)`, and for
  chains `chain_upfront_cost / (money+1)`, `chain_payback_days / days_remaining`.
  **This is the direct antidote to the leak**: a network given `day` and `money` separately can learn
  "day ≥ 10 implies rich"; one given `land_price/money` cannot, because the ratio is honest regardless
  of which day-wealth combinations appeared in training.
- **9 market prices** (normalised by base) **and 9 market inventories separately**, as
  `inventory/I0 - 1` (0 baseline, negative scarce, positive glut).
- **Own farm as aggregates, not per-tile**: per-crop tile counts (5), growth-phase buckets (4 is enough
  — just-planted / in bonus-water window / mature-unharvested / ongoing-producing), animals per species
  (3), quadrants unlocked (1), hands (1), shed inventory per product (9, own only — the shed is private).
- **Opponent farm, same aggregates** — the board is fully visible
  (`competition_brief.md:146-153`, "you can see exactly what the opponent is growing").

**Exclude:**
- **Unit positions.** `_end_of_day` teleports every unit to spawn each dawn, so at a day boundary the
  value is always the same — pure noise dimensionality, and the Markov argument already says it does not
  survive the reset.
- **100 tiles × crop × phase per-tile.** ~3,000 dims invites overfitting given how few terminal labels a
  30-step MDP generates on this hardware in 8 weeks, and chains act on blocks, not individual tiles.
  Individual tile identity within a homogeneous block is a symmetry the network should not have to learn
  away.
- **Any hand-built "expected bank for this day" feature** — that is re-injecting the leak deliberately.

## (4) Does market-inventory-in-state actually support denial?

**It holds in the code but is weaker and more confounded than I credited.**
`State.inventory` is `[B, N_PRODUCTS]` (`jax_sim.py:228`), shared, and both `SELL` and `BUY_PRODUCT`
flow through the same `_process_market` (`jax_sim.py:893-1026`).

But wheat's town drain alone is **662 units/season, pushing price to $51 = 2.04x base, with zero player
sales at all**, and the unlock schedule driving it is per-episode random.
So wheat inventory movement is dominated by a large exogenous random process, and the opponent's
activity is a small perturbation on top — confirmed by the numbers, not just plausible.

**The clean channel is already in the state: the opponent's farm is fully visible.**
"Opponent has 15 PASTURE tiles" is a direct fact; "wheat inventory is 12% below I0" is that same fact
confounded with the town's random schedule.
`ladder_analysis.md:136-143` shows this working in practice — the three worst real-ladder losses were
identifiable as small PASTURE-heavy farms from the visible board.
Keep inventory in the state (useful for our own selling), but the farm-composition features do the real
work.
Given (1), deprioritise both relative to shipping `crop()` and a sound chain catalog.

## (5) `crop(script, crop_name, tile, plant_day, unit=None)`

**Materially harder than `ranch()`, for one specific reason worth stating first:**
`ranch()`'s entire safety property comes from binding the routine to one of the four shed-access tiles,
so **it never needs a movement op** (`routines.py:21-27`, `test_a_ranch_never_emits_a_movement_op`).
There are only 4 such tiles and animals need them.
Crop tiles are the other ~96, so **`crop()` cannot inherit the zero-movement trick — it has to solve
routing**, which is the project's flagged-unmeasured problem ("whether those instalments are routable
inside the action budget is not tested") and what previously made cows net-negative despite $725/tile.

1. **The daily re-walk is mandatory.** `_end_of_day` teleports every unit to spawn every dawn — exactly
   the bug `ranch()` records fixing ("walked once... and silently starved every animal outside (4,4)").
   `crop()` must re-emit the full spawn→tile path **every day**, not once at `plant_day`.
2. **Water every day, both crop types, or the plant dies.** `_daily_refresh_plants`
   (`jax_sim.py:1155-1176`): `unwatered >= 2` kills any `PLANT` tile regardless of `ONGOING[c]`.
   The bonus-yield window only pays for non-ongoing crops (`jax_sim.py:632-636`), but the **death rule
   applies to both** — a routine that skips watering strawberry because "it doesn't help ongoing crops"
   will kill it.
3. **Harvest timing splits by crop type:**
   - *One-shot (wheat/carrot/melon):* `HARVEST` legal once `age >= FIRST_YIELD_DAY[c]`
     (`jax_sim.py:645`), and clears the tile to `EMPTY` (line 651) — which is what makes multi-cycle
     planting possible and where wheat's measured 28 units/tile/season comes from.
     `harvest_day` should be an explicit parameter like `ranch()`'s `land_day`, with a real tradeoff:
     harvest at `FIRST_YIELD_DAY` for more cycles, or wait to `MAX_YIELD_DAY` for a bigger single
     harvest (the bonus-water window closes at `MAX_YIELD_DAY[c]`).
   - *Ongoing (tomato/strawberry):* production accrues at night to a lifetime cap
     (`production_count <= MAX_YIELD[c]`, line 1189), and **the moment the cap is hit
     `max_lifespan_step` is set and `_decay_plants` (1140-1151) eats 1 unit every 2 steps** — about a
     day's accumulated yield gone within a day if unharvested.
     Schedule `HARVEST` no later than one day after the final production event.
4. **The atomic PLANT rule at multi-instance scale.** `jax_sim.py:565-582`: seed demand is computed once
   per turn across all units against seeds held at turn start, and if demand exceeds supply **every**
   plant for that crop fails, not just the excess.
   Two `crop()` calls for the same crop on the same day must combine into **one correctly-sized
   `BUY_SEED`** — the `maximum(...)` pattern `ranch()` already uses for hires (`routines.py:220`), not
   `+=`.
5. **`DROP` is usually unnecessary.** `_end_of_day` unconditionally calls `_drop_to_shed(farm)`
   (`jax_sim.py:1230`), so carried inventory auto-deposits at night.
   Only walk to the shed if the harvest must be **sold the same day** — otherwise the round trip wastes
   the turn budget, and turn budget *is* the routing problem.
6. **Scope path planning down for v1:** take a *block* (contiguous, inside the unlocked NW quadrant)
   rather than one tile, with a boustrophedon path from spawn through the block and back, re-emitted
   daily.
   Movement is blocked by `LOCKED` at the target cell, so a block spanning an unbought quadrant needs
   the same `land_day`-before-route ordering `ranch()` already has.
   Do not solve cross-quadrant path planning in v1.

**Tests, mirroring `test_routines.py`:**
- `test_a_crop_is_watered_every_remaining_day`
- `test_a_crop_routine_re_walks_from_spawn_every_day` — the bug class `ranch()` made unreachable and
  `crop()` reintroduces
- `test_an_ongoing_crop_is_harvested_before_it_decays`
- `test_two_crop_calls_for_the_same_crop_share_one_seed_order`
- `test_a_crop_routine_pays_for_itself`
- `test_planting_before_land_is_bought_is_impossible`

## (6) Ranking, ~8 weeks

**Finish the search track first; run Bellman alongside once `crop()` exists, not instead of it, with a
hard day-3 kill gate.**

The search track is the only thing in this project's history that has produced a strong reproducible
result — `cem_seeded.log`'s win 1.00 / +$47,872 in a few hours of CPU, from a weak start.
The Bellman route is unbuilt and carries a real risk of reproducing factored-action collapse if the
catalog decision is not made up front.

**`crop()` is a shared dependency and therefore zero sunk cost** — the search track needs it as a chain
primitive, a chain-action fitted-Q needs the identical primitive in its action catalog.

**Smallest one-week version:** do not build new infrastructure.
Repurpose `StrategyEnv`'s working loop (`scripts/train_rl.py`), extend `ACTION_BUCKETS` with a few
chain-triggering choices ("start `ranch(COW)` on the free block now: yes/no"), each bucketed the way
`melon_tiles`/`hold_days` already are — not raw tile/day.
Swap the trainer for a small DQN with **Double-DQN target averaging**, to blunt the overestimation bias
that 30 sequential bootstraps compound.
Reuse `states_at_mix`'s length-weighting if seeding at all, biased explicitly to decorrelate day from
wealth.

**The day-3 kill number:** CEM reaches win 1.00 against a comparable opponent class in under 2 hours.
That is the bar.
If after 3 days of wall-clock on the 3080 fitted-Q has not cleared **win rate > 0.7 against the same
frozen pool CEM beats at 1.00**, or the TD residual is not visibly decreasing, **stop** — a value method
needing three days to approach what a population search cleared in two hours has lost the compute
argument for the remaining 7.5 weeks, regardless of eventual convergence.
