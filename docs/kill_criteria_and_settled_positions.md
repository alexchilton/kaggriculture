# Kill criteria and settled positions — the full record

Moved out of `CLAUDE.md` on 2026-08-15. Every kill criterion below is either MET or CLOSED, and
the settled positions are all about the RL track, which is parked. `CLAUDE.md` now carries the
three sentences that still bind; this file is the evidence behind them.

Do not delete it. The reward-shape bullets exist to stop a future session restoring per-step
rewards from `docs/rl_feasibility.md`, which still argues for them at length.

---

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

