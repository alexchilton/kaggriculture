# Three layers, and the third one is not a detail

Alex's framing at the end of the 2026-08-05/06 session, and the session's measurements support it:

| layer | question it answers | method | status |
|---|---|---|---|
| **genome** | what mix of crops and animals | deterministic constrained optimisation | largely done |
| **schedule** | how many of what, on which day | search on win rate, batched in `Game` | not started properly |
| **agent** | which tile, which unit, in what order | assignment + routing optimisation | **the current bottleneck** |

The third layer was treated as plumbing for the whole project.
It is not.
Driving the **same** schedule on the **same** five seeds, execution alone moved the bank from $10,134 to
$59,716 — 8% of the winner's $127,266 to 47%.
No schedule change was involved in any of it.

## The gate that made this measurable

`scripts/schedule_ladder.py`, and specifically **the winner's schedule through our agent**.
It is the only input that cannot be tuned against, and adopting it immediately exposed that a day of
"improvements" had been measured on a schedule I was simultaneously tuning to route around the agent's
faults — 46% on my plan against 8% on theirs.
That spread was the size of the self-deception, and it closed to within 2% once the agent was fixed rather
than the schedule.

**Every dollar figure needs a fixed, matched seed list.** `env.reset()` draws a fresh seed each call, and
one identical tape banked $48,144–$59,199 across four runs. An unseeded figure is not a rough measurement,
it is no measurement.

## What layer 3 actually consists of

Four things, in the order their absence cost money:

1. **Tile uniqueness.** A tile assigned to a unit must stay assigned. `_nearest_empty` re-derives a tile
   every turn from the live board, so a planned `PLANT at (2,3)` becomes `(2,4)` next turn and the plan is
   dropped as stale. This is why the committed-tour port banked $0 with 211 work ops a season: every
   schedule-derived step went stale on the turn after it was planned.
   Board-derived tasks (WATER, FEED, HARVEST at a tile) already have stable identity — the tile *is* the
   task. Schedule-derived tasks (PLANT a strawberry, BUILD a pasture) have none until something pins them.

2. **Tour commitment.** `dayplan._assign` had a turn budget, consumed tasks as it assigned them, planned a
   whole day up front, and priced each stop from the cursor so tours came out serpentine. The agent re-picks
   from the entire pool every turn, so two units contend for one tile and a unit walking to a target reverses
   when another takes it. Every attempt to tune the priority made it worse — more tasks raised idling 23% →
   33%, distance-primary banked $809, forcing pen work first took the harness 47% → 35%. **There was no plan
   to perturb.**

3. **Tile placement.** Adjacency dominates distance: five adjacent tiles is a four-step tour, five round a
   ring is twelve, and every tile is revisited ~20 times a season. Pens belong on the four shed-access cells,
   where FEED, CARE, COLLECT_FERTILIZER, PICKUP and DROP all happen without a single move. Quadrant legality
   is per-day, not static.

4. **Zoning.** The herd lives at the shed and the crops are in the field. A unit that switches to
   distance-primary after its first op never returns to the pens, so only units whose *first* stop is a pen
   ever feed anything — ~12 first stops against ~33 pen tasks a day. FEED lands on 81% of animal-days, and at
   81% a herd does not survive: it built to 8 by day 13 and decayed to 3 by day 16 while the bank climbed
   $9,273 → $43,938. Two consecutive missed feeds and the animal is gone.

## What the agent already gets right, and must keep

Closed-loop legality. It reads `obs` and never predicts:

    op landing        emitter 48%      agent 100%
    tape's tile list  worth $23,470    worth $0
    tape's order book required          not needed
    BUY_LAND          fixed hour, lost the $2,000 parcel   fires when the bank covers it
    BUY_ANIMAL        silently no-oped on a thin bank      only ordered when affordable

Seven of the nine emitter bugs simply cannot occur in it. That is the property to preserve while adding
layers 1–4 above — the port must add commitment *without* going back to predicting state.

## Hypotheses that died to measurement, so they are not retried

- sell orders 60–90% unfilled — the tape's own orders measure identically; the replay observation is
  post-market
- fertilizer lost to the 100-unit shed cap — we bin 27 units a season, the tape bins 7
- ongoing crops wasting production at their yield cap — `atcap` is 0 for both sides all season
- wheat as an appreciating store of value — tried twice; FEED went *down* as more was bought, because wheat
  bought is animals not bought
- crop deaths as the cause of a small farm — watering every tile every day cut deaths 39 → 31 and raised peak
  crops 30 → 37, and cost $18,569
- BFS routing — correct on a non-convex board, zero measurable effect
- market timing, front-running, withholding — ~3% of money and 0% of wins
  (`market_game_framing_kimi_2026-08-05.md`)

## Method notes worth more than any single fix

- **Per-day and per-turn verdict tables find in one run what reasoning does not find in hours.** Every fix
  that worked today came from one; every failed attempt came from a season aggregate plus a guess.
- **An identical result means the change did not take effect, not that it had no effect.** This happened
  four times: a wheat-stock test, a fertilize task gated on the shed, a feed buffer, a pen-target fix.
- **A check that fails into doing nothing is the defect class of this project.** `_step_towards` returning
  None, `PLACE` gated on the shed while the animal was in a hand, `FEED` queued behind wheat that never
  arrived — each one silently burned turns instead of reporting.

Related: [[schedule_ladder]], [[market_game_framing_kimi_2026-08-05]], [[the_winners_are_open_loop_2026-08-04]].
