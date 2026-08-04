# Fable: how to generate a competitor of our own (2026-08-04)

Saved before relaying, per standing rule.
Question asked: given the market appears to have a computable ceiling and Subin An sits at ~97% of it,
what is the credible route to a strong tape that is *ours* — construction, search, or RL?

Files Fable read: `kagg/economics/market.py`, `kagg/sim/jax_sim.py`,
`kagg/search/{rollout,cem,routines,chain_mutate,script_mutate,plan,boards}.py`,
`kagg/search/executor.py:400-628`, `scripts/optimise_script.py`, `kagg/rl/env.py`,
`docs/{competition_brief,rl_feasibility,economics_q5_findings,the_winners_are_open_loop_2026-08-04,review_of_the_reframe_2026-08-04,kimi_take_chain_optimisation_2026-08-04,fable_chain_genome_review_2026-08-04,fable_review_macro_action_plan_2026-08-04,bankrupt_every_game_2026-08-03,executor_livestock_broken_2026-08-04}.md`,
plus `data/logs/{optimise_from_winner,cem_seeded,mine_build_orders}.log`.

## (a) The ceiling, denial, and whether anything beats $147k

**The arithmetic is directionally right but "ceiling" oversells it.**
`price()` floors at `PRICE_FLOOR = 1` (`jax_sim.py:522-533`), so overselling past the drain rate still
earns positive marginal revenue all the way down to $1 a unit.
Total extractable revenue is therefore not capped at $302,380 — what bounds it is tile, hire and land
capacity.
`economics_q5_findings.md` measured that capacity is severe for the high-value goods (strawberry needs
89 tiles to saturate one quadrant's demand, milk needs 40 cows) but *not* severe for wheat and carrot,
which a 100-tile farm can oversupply several times over.
So there is uncounted headroom in bulk crops — likely thousands, not tens of thousands, because the
shape functions decay slowly.

**The number that strengthens the argument, and which we had not computed:**
in episode 89873723 the two banks sum to **$294,300 = 97.3% of the $302,380 at-base ceiling, combined**.
Both players together are already taking almost the whole simple pie.
That leaves two levers, different in kind.

### 1. Redistribution — denial

Zero-sum by construction, and two mechanisms are real in the code:

- **A sell depresses the price for whoever sells that product next, including across turns.**
  `_process_market` (`jax_sim.py:966-1001`) raises `inventory` on a sell; price falls along the glut
  curve and recovers only via `town_drain`.
  `economics_q5_findings.md`'s "sell late beats sell early" is this dynamic working against whoever
  sells first — currently read as a solo-optimisation fact, not as a weapon.
- **`BUY_PRODUCT` on WHEAT starves a wheat-dependent opponent.**
  Wheat is the only crop buyable back; buying removes a unit from inventory and raises the price.
  `mine_build_orders.log` shows top real seats buying **3,700-4,100 wheat units a season** — they run
  livestock on bought feed, not grown feed.
  Front-running that raises the price they pay.
  **Unmeasured and unexplored anywhere in the docs.**
  Fable's pick for the one denial idea worth testing this week.

Against it: `the_winners_are_open_loop_2026-08-04.md` measures `senkin13` diverging on **zero** market
turns across six comparisons.
But `review_of_the_reframe_2026-08-04.md` already flags that sample as a mirror match of unconfirmed
rank, so "denial isn't happening at the top" is not evidence that it fails — it may be untried.

### 2. The scarcity premium, attacked selectively rather than globally

Our sweep tested one variable — delay everything by N days — and it collapses past day 2 on working
capital.
It never tried *selective* holding.
Strawberry and milk are low-volume, high-margin, and mature late anyway, so they need almost no working
capital to hold, unlike wheat's ~700 units.
The $196,866 gap between the at-base and hold-back ceilings is concentrated in exactly the SKUs that
are cheapest to hold.
Nobody has swept "hold only the two or three lowest-volume products, drip-sell the rest normally."

## (b) Constructing a tape from a weak start

**This is already working, as of today, and it is the finding that most changes the picture.**
`data/logs/cem_seeded.log` shows the gene-space CEM seeded at the leaders' allocation going from
`pop mean 0.03` at generation 0 to `win 1.00` by generation 2 and `delta +47,872` by generation 19,
then starting a round 2 in which the round-1 winner joins the opposition.
That run goes through `rollout.evaluate`, which shares one unlock schedule across all candidates and
averages — so unlike the tape optimiser's numbers, these are not board noise.

Fable attributes the unblocking to three executor defects fixed earlier today
(`executor.py:421-437, 507-525, 583-609, 611-614`): herd size uncapped, feed undersized, and three
purchases each independently checking `view.money` and over-committing.
The livestock genome is no longer banking $0.

**Decision variables, ranked by worth:**

1. Land timing (`land_day`, 3 discrete, sequential NE→SW→SE) — real seats buy the first parcel day
   9-11, never all three.
2. Animal portfolio (species × count × start day) — top seats stock 20-25 sheep/cows almost
   immediately, not gradually. `routines.py::ranch()` already emits the whole coherent chain and is
   measured at **+$8,119/cow** against a do-nothing opponent.
3. Crop allocation and phase per tile (100 tiles × 5 phase buckets).
4. Hire ramp per day (8-14 hands, not flat).
5. **Feed as purchase, not as crop** — 3,700-4,100 wheat units bought per season.
6. Sell cadence per product per day-block, sell-late biased: top seats sell 65-79% of volume in the
   final third.

**Method: not MILP/CP.**
No admissible heuristic exists (checked against the reference in
`fable_chain_genome_review_2026-08-04.md:44`), the price function is nonlinear (log/sqrt/log10,
`jax_sim.py:508-519`), and a relaxation tight enough to be exact would have to reproduce the dawn reset
and the per-unit chain dependencies — i.e. re-derive the simulator inside a solver.
Given a validated fast batchable simulator already exists, simulation-based search dominates.

The recommended representation is a **chain-instance genome**:
`ChainInstance = {type, start_day, unit_id, tile, params}`, unordered, decoded day by day, evolved with
CEM/GA.
Illegal or wasteful chains simply score worse — no legality machinery, the same argument
`script_mutate.py` already relies on.
The Markov structure sits at the **day boundary** (verified against `_end_of_day`: everything except
unit positions and hires survives the reset), so a 7-10 day rollout under a fixed auto-pilot ranks beam
nodes without paying for a full 30-day rollout per candidate.

**Budget: cheap.** A few hundred candidates × 20-30 generations × 4-8 (opponent × board) pairs is
50k-300k full-season rollouts; the 20-generation run above finished in under two hours on CPU.
Orders of magnitude cheaper than any RL run in this project.

**What is actually missing:** a crop-tile routine analogous to `ranch()` (the largest coverage gap —
everything built so far is livestock), and the beam/DP orchestration over chain instances.
The primitives and the mining data exist; nothing wires them together.

## (c) RL over the raw 720-turn action space

**No, not on current evidence.** Fable would not keep funding it this week. What is measured:

- `bankrupt_every_game_2026-08-03.md`: the policy loses to `idle` **3,183/3,183** games — 95% CI upper
  bound on true win rate 0.094%. To beat `idle` it needs to do *less* than the action space can already
  express, and 1M+ turns have not found it.
- `HANDOFF_NEXT.md`: turn-0 replay is **0/0/16** W/D/L every seating, 100% movement, zero productive
  actions — after commitment tokens, KL-to-prior, autoregressive op-conditioned decode and symmetric
  starts.
- `entropy_diffusion_2026-08-04.md`: critic `ev_signal` rose 0.42 → 0.60 while the policy got *worse*.
- `cliff_decomposed_2026-08-03.md`: every curriculum rung leaks a day↔wealth correlation, so apparent
  improvement is partly reading `step_index` as a proxy for "should be rich by now".

Contrast: `cem_seeded.log` reached 100% win rate against the same opponent class in hours on CPU.

**If RL is pursued regardless**, the only defensible version is RL over the *same chain-instance action
space* the search track uses — choose which chain to start, where, when, every few days, riding
`routines.py`'s tested decoder so the policy never rediscovers FEED/CARE/PLACE sequencing.
Tens of decisions per game rather than 17,000+ single-choice points.
`kagg/rl/env.py` (one decision per day, 9 heads, ev > 0.5) is proof a coarsened space on this game
learns cleanly — it is the raw per-turn space that is the trap.
Even so, Fable ranks it below finishing the search track, not alongside it.

**Compute honesty:** `rl_feasibility.md` puts a competitive 10B-step run at ~27 days on the vectorised
JAX sim, before the credit-assignment and reward-density problems above — which are not compute
problems, and there is no argument for why more steps would fix them in the remaining ~8 weeks.

## (d) Ranked for this week

1. **Fix the day-0 crop-tile routine gap and wire a beam/CEM orchestrator over chain instances.**
   Highest EV; targets the gap with a representation validated today. 1-2 days, CPU only.
2. **Re-run slot-vs-chain tape mutation under the `boards.py` fix.**
   Confirmed by timestamp that `op_compare_{slot,chain}.log` predate the fix — they are the confounded
   run. The script already has `--boards`; it just has not been rerun. Hours.
3. **Fix the executor's land-affordability decoder gap** — unconditional `["BUY_LAND"]` at order-slot 0
   every turn until bought, rather than the single-check-per-turn gate at `executor.py:614`. Hours.
4. **Pull the confirmed top-five replays (task #10)** and rerun the open-loop diff against them rather
   than the unconfirmed-rank mirror pair. An hour, and epistemically load-bearing for everything built
   on "the winners are open-loop".
5. **Test the wheat-buying denial hypothesis** inside the existing search harness — free once (1) runs.
6. **Validate any script across many weed/unlock seeds** before spending a submission slot.
   `review_of_the_reframe_2026-08-04.md` Finding B: zero weed events across all six replays despite
   `weedSpawnChance=0.005`, so "the winners ignore weeds" is untested, not established.
7. **Pause the raw-per-turn RL track this week.** Not killed — the evidence is not "RL cannot work
   here", it is "this has not worked in weeks and a cheaper alternative is already ahead".

## Where this contradicts what I had told Alex

- I said the executor was "$230 and shit". That was `leaders_genome()`, a hand-encoded fixture.
  CEM-searched genomes reach win 1.00 / +$47,872.
- I presented $302,380 as a hard ceiling. It is one policy's revenue; the real bound is farm capacity,
  and the floor at $1 means revenue is not capped.
- I said the optimiser had already searched market timing and found nothing. It searched *local*
  timing under a broken score. Selective holding of low-volume SKUs is untested.
