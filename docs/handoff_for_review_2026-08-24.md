# Review brief: kaggriculture endgame and where the money is going

Repo: `/Users/alexchilton/DataspellProjects/kaggriculture`

You are reviewing a Kaggle competition agent. I want ideas, not agreement. Where you think a
decision below is wrong, say so and say what you would measure to settle it.

---

## 1. What the competition is

`kaggriculture`: two farmers, one shared town, 30 game-days of 24 turns = 720 turns. Each turn you
submit ops for the farmer plus every hired hand, and up to ten market orders. You bank money by
selling produce into the town, whose price for each product **falls as you sell into it and recovers
as shops drain it**.

Scoring is an **Elo ladder, not money**. A $43k win and a $4k win score identically. That single fact
invalidates most "maximise the bank" reasoning and is the most common thing reviewers get wrong here.

Ground truth for every rule question is `reference/kaggriculture.py`. Read it rather than the README
where they disagree. Key tables are at the top: `CROPS` (seed cost, `first_yield_day`,
`max_yield_day`, `max_yield`, `ongoing`) and `ANIMALS` (cost, structure, `first_yield_day`,
`interval`, `max_held`, product).

Deadline 2026-09-30. Five submissions a day.

## 2. What the agent is

Not a policy network. A **deterministic day planner**: at hour 0 it plans the whole day for every
unit, then executes. It never replans mid-day.

    kagg/search/schedule_agent.py     ~6,200 lines. The agent. Day planning, market orders, hiring.
    kagg/search/router.py             Routing NODES and their PRIZES. What a tile is worth visiting.
    kagg/search/cover.py              The covering/tour planner that turns nodes into routes.
    kagg/search/crew.py               Hiring.
    kagg/sim/jax_sim.py               Fast batched simulator, parity-verified against reference.
    reference/kaggriculture.py        The competition environment. Ground truth.

A second, mostly separate track exists: `scripts/train_jax_rl.py` (PPO on the fast sim) and
`scripts/dagger_tape.py` (behaviour cloning from recorded games). Treat it as out of scope unless you
want to comment on it; the shipped artifact is the planner.

### The tape mechanism, which you must understand before reading any measurement

`schedule_agent.REPLAY_OPENING_DAYS` is a tuple of days on which the agent **replays a recorded
human game's actions verbatim** instead of planning. This differs by branch and it has repeatedly
invalidated experiments:

    ead81e2  (the shipped 2500er)   (4,5,6,7,8,9,10,11)    tape d4-d11, planner owns the rest
    current HEAD of main            tuple(range(30))       tape ALL 30 DAYS, planner never runs

Today three separate code changes came back byte-identical because they were measured on the
`range(30)` branch, where none of the planner code executes. **Check this constant before believing
any result.**

## 3. Branches and what is on them

    ead81e2            the 2500er. Scored 2472.7 on the ladder. No carrot.
    e2500-carrot       ead81e2 + f1b73c9 (late carrot) + 4649af9 (today's fix)
    e2500-shopprice    ead81e2 + bd6cb6e (today's fix, cherry-picked)   <- release candidate

Worktree for both: `.claude/worktrees/e2500`.

Alex is currently running with-carrot and without-carrot on the ladder simultaneously. **Without
carrot is winning.**

Built artifact: `submission/e2500_shopprice.py` (13,437 lines, self-contained, verified importable,
worst turn 390 ms against a 1s/turn limit with a 60s bank).

## 4. What was found and fixed today

Downloaded loss: game `98335212`, seed `34935263`, our seat 0. **Lost by $781 of $85,177.**

At the final turn we had **4 wool standing in a pasture worth $732** — 94% of the losing margin —
while the closing turns hauled milk the town was paying **$1** for.

Root cause, `router.animal_ops`, the last-day harvest prize:

```python
price = BASE_PRICE[a["product"]]                                  # a module CONSTANT
out.append(("HARVEST", None, CRITICAL + cell["yield_units"] * price))   # CRITICAL = 1_000_000
```

Two defects, and the second hid the first:

1. **`BASE_PRICE` is static.** The real price is endogenous — it is largely set by what *we* dumped
   into the book earlier in the season. Two runs of the same seed:

       recorded submission     WOOL $183   MILK $1
       our own rematch         WOOL $5     MILK $214

   Same board, opposite ranking. No constant can be right in both.

2. **`CRITICAL` swamps the value term.** A cow holding 3 milk at $214 priced 1,000,642; a sheep
   holding 4 wool at $5 priced 1,000,020. A $642 pen and a $20 pen differing by 0.06%, so the route
   took pens in whatever order the board offered.

Fix: thread the live price from the observation through `build_nodes` into `animal_ops`, and make the
last-day prize `units * price` with no constant.

Measured, our agent in our seat against their recorded actions on the game's own seed:

    branch                     ours      margin   left in field   captured
    submitted (recorded)     $84,396      -$781       $942          --
    e2500 carrot + fix       $85,007      -$131       $241         97.2%
    e2500 NO carrot + fix    $85,099       -$57       $241         97.3%

The sheep now sells at h21 and what gets left is the $1 milk. **One seed — read the delta, not the
level.**

## 5. Things tried today that did NOT work, with numbers

Do not re-propose these without a new argument:

    harvest en route on the walk home    -$48   collected more field, banked less
    d28 value-ordering instead of flat     $0   byte-identical
    reserving a sell turn in the walk      $0   byte-identical
    handing d28/d29 to the planner on   -$1,426 (on the range(30) branch, where the tape's own
      the tape branch                            endgame was already capturing 99.3%)

## 6. Facts that have cost real time here. Please internalise before reviewing

- **Offers are not fills.** The agent re-posts each market order every turn. Summing the action
  stream over-counts by ~24x. Use shed/money deltas or `kagg/analysis/fills.py`.
- **Prices are endogenous.** We flood our own book. Milk has been measured floored at $1-$5 for a
  whole season while another game had it at $214.
- **A byte-identical result means you changed code that does not run.** It is information. Find the
  live path rather than tuning harder.
- **`CRITICAL = 1_000_000` is added in many places in `router.py`.** Anywhere it is *added* to a
  value, it destroys the ability to compare two values. Today's fix removed it from one site. There
  are others — `HARVEST_CRITICAL_FROM_DAY`, the d28 pen promotion, the FEED floor. Whether each is
  a real defect is an open question and a good thing to review.
- **On d29 a turn budget needs four legs: harvest, walk, DROP, and a market turn to SELL.** Goods
  dropped on the final turn reach the shed after the last `_process_market` and are worth zero. Two
  separate rules in this codebase got this wrong by omitting the last leg.
- **The unit phase runs BEFORE the market phase** in a turn (`kaggriculture.py:922` then `:928`), so
  a DROP and a SELL in the same turn do work — but only up to the final turn.
- Alex's standing instruction: **judge a fix on the day it targets**, per-day, not on a season total.
  Seed variance is ~15%.

## 7. Where I think the remaining money is — argue with this

1. **$241 is still left standing** at the close, and I measured twice that going back for it costs
   more than it is worth. My read: the fix is not in d28/d29 collection at all, but two days
   earlier — **do not have crops ripening in the far corner of the board on d29**. That is a
   planting and routing decision around d24-d26. Untested.
2. **We lose narrowly and often.** Of 54 downloaded losses, 11 are inside $2,100. Endgame value is
   the right size of lever for that population.
3. **The market is the biggest unexplained gap.** We flood our own book; a season sold 159 units of
   milk at $1-$5 while other agents realised $223/unit. Sell cadence and quantity sizing are barely
   tuned. `LIQUIDATE_FROM_HOUR`, `CAP_SELL_OFFER_SIZE`, `LATE_SELL_BIAS` are the relevant dials.
4. **Carrot vs no-carrot is unresolved by measurement.** One seed put them $92 apart, which is
   noise. The ladder says no-carrot. A run of both arms across the loss corpus would settle it and
   needs no GPU.

## 8. How to reproduce anything above

    # replay one of our real ladder games with the LIVE agent in our seat and
    # THEIR recorded actions in theirs, on the game's own seed
    python -u scripts/rematch_the_losses.py --dir data/seed_scripts/losses --only 98335212

    # grade only the last two days: what reached the shed, what was left standing, at what price
    python -u scripts/what_the_last_two_days_banked.py 98335212

    # build and self-verify a submission
    python -u scripts/build_planner_submission.py --out submission/<name>.py

    # gate it against the opponent pool. NEVER gate against `starter`: it sells almost
    # nothing, so the market is never contested and every number is ~2x reality.
    python -u scripts/gate_pool.py --agent submission/<name>.py --seeds 12

Downloaded games live in `data/seed_scripts/`. Note they are **selected losses** — never compute a
win rate from them.

## 9. What I want from you

Read `kagg/search/router.py` (prizes), `kagg/search/schedule_agent.py` (the day plan and the market
order block), and `reference/kaggriculture.py` (the rules). Then:

1. Where else does a constant destroy a value comparison the way `CRITICAL` did?
2. Is the endgame framing right at all, or is the money somewhere else entirely?
3. What would you measure first, and what result would change your mind?

Concrete and falsifiable beats broad. If you think the whole endgame line of attack is worth less
than the market-flooding problem, say that plainly.
