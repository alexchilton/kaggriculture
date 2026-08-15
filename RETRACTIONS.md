# Retractions — session of 2026-08-15

Written at Alex's request. Every claim I made and then corrected, every claim still unmeasured, and
the short list of things actually proved with numbers.

---

## (a) Claims I made and later corrected

### 1. "The precomputed routes change nothing"

**Claimed:** ran an A/B setting `SOLVED_DAYS = {}` and reported the 30-day grid byte-identical, so
the precomputed routes had no effect.

**Correction:** the A/B was a silent no-op. `cover.py` builds `PRECOMPUTED_ROUTES` from
`SOLVED_DAYS` **at import**, so rebinding `SOLVED_DAYS` afterwards changes nothing. The comment
three lines above the code says exactly this: *"a silent no-op reads exactly like a measured null,
which this project has been bitten by."* Re-run against the right name:

    precomputed ON (shipped)     d29 $139,025    work 2979  move 3036  idle 987
    PRECOMPUTED_ROUTES = {}      d29 $118,660    work 2895  move 3150  idle 957

The routes are worth **+$20,365**, not nothing.

### 2. "The stale routes are still working well"

**Claimed:** read the +$20,365 as the routes doing their job.

**Correction:** Alex pushed back that it made no logical sense. `cover.PRECOMPUTED_MISSES` shows only
**143 of 571 stops** are seated — d23 is down to 9 of 74. The geometry is free (terrain is a pure
function of coordinates), so a quarter of a stale artifact beats the greedy. That is a statement
about how weak the greedy is, not about the routes.

### 3. "We place 18 animals to his 36 — half the herd"

**Claimed:** built a story that he rotates stock into the same 14 pens ~2.5 times a season.

**Correction:** Alex flagged that `place 18/36` cannot coexist with `animals 14/14`. It does not.
`PLACE` is overloaded in the env (`reference/kaggriculture.py:377`): animal placement **and** shed
deposit. The herd is 14/14 all season. I invented a mechanism to reconcile two numbers instead of
reading what the quantity counts.

Worse, the follow-up measurement killed the replacement story too: the **greedy** does 35 places
against his 36, and the stale precomputed routes drop it to 18. So we do not under-bank at the shed
as a strategy — the stale routes destroy 17 shed deposits.

### 4. "The water shortfall is in the plan"

**Claimed:** briefed a sub-agent to make `build_nodes` create more WATER jobs, citing d10 25/32 and
d12 30/40.

**Correction:** over d9–d29, **water ours 798 / tape 795**. We water three MORE times than he does.
The per-day gaps are cancelled by days we over-water (d13 47/41, d23 41/31). The sub-agent built the
preventive-watering rule anyway and measured it: **−$1,051** and one extra tile death, because the
extra watering displaced a rescue the baseline had executed. Reverted.

### 5. "The victor tape default gave me a false null"

**Claimed:** in the first version of commit `af3db5d`'s message, that the stale `DEFAULT_TAPE` caused
a sell-rule change to read as a null.

**Correction:** it did not. The null was real on **both** tapes. The stale default is a genuine bug
worth fixing and it has so far cost nothing measurable. Commit message amended.

### 6. "The `shed_dusk` sell-down will reproduce the recorded +$5,533 → +$62"

**Claimed:** extracted `shed_dusk` into all 30 schedule rows expecting the recorded gain.

**Correction:** measured **−$1**. Cause: **MILK appears in his dusk shed on 0 of 30 days**, so the
branch cannot fire for milk at all. It is a wheat rule. One command would have shown this before the
extraction.

---

## (b) Still UNVERIFIED — no measurement behind them

1. **That regenerating the routes will close the harvest gap.** The mechanism is plausible and
   partly evidenced (routing alone moved harvest 276 → 335 with only 25% of stops matching), but the
   regenerated set has not been measured end to end. **This is the whole thesis of the session and it
   is not yet proved.**
2. **That the stale routes caused the ladder drop 1890 → 1428 → 1030.** The timing fits — the plan
   switched to Kawashigi on 2026-08-13 and the routes did not — but 30+ commits sit between those
   submissions and nothing isolates the cause.
3. **That the melon rule is hurting.** It ships live, fires in 68% of games, and went out on tape
   evidence alone. The A/B (`MELON_YIELD_OPPONENT_MELON 7 vs 99`, 1,440 games) is queued, not
   reported.
4. **That the regenerated routes generalise off seed 11.** They are solved against our job pool on
   one seed. Board geometry is seed-independent, but which jobs exist depends on what the market
   gave us, which varies with the opponent. Risk of overfit; checkable via `PRECOMPUTED_MISSES`
   against ladder opponents.
5. **The sub-agent's over-budget finding** — that tours ship priced 25–26 turns against 23-turn
   budgets because the packer admits on one cost model and ships another. Reported with log
   references, not independently reproduced by me.
6. **That `_at_risk_tiles` should mark a final-production-day ongoing tile.** Suggested, not built,
   not measured.

---

## (c) Actually PROVED, with numbers

1. **The precomputed routes are worth +$20,365 and only a quarter of them still apply.**

       precomputed ON   d29 $139,025      OFF  d29 $118,660
       stops seated     143 of 571 (25%)       d23 worst at 9 of 74

   They were solved against the **victor** plan; we have shipped **kawashigi** since 2026-08-13.

2. **The harvest gap is a coverage problem, not a job-creation problem.** Over d19–d29 the board
   offers **335** HARVEST jobs, we take **247**, the tape takes **280**. 88 offered harvests go
   unseated and 33 of them would match him. The worst days are the ones that never had a route at
   all — d20 (11 of 26), d22 (17 of 37).

3. **Two flags are confirmed losses on the ladder field** — 12 recorded opponents, both seatings,
   env-default weeds:

       HERD_GEESE             0 → 69.4% win, +$15,502 margin
                              2 → 38.9% win,  −$2,432
                              4 → 41.7% win,  −$1,338
       WHEAT_TILES_TO_CARROT  0 → 69.4%   8 → 61.1%   16 → 63.9%   28 → 66.0%
       WHEAT_TILES_TO_TOMATO  0 → 69.4%   8 → 61.1%   16 → 63.9%   28 → 68.1%

   Carrot raises mean money (88,810 → 90,080) while lowering win rate. On an Elo ladder that is
   strictly worse.

4. **Watering is not the problem.** water d9–d29 **ours 798 / tape 795**, and the one fix built
   against the opposite belief measured −$1,051 with one extra tile death.

5. **The dead-agent trap was real and measurable.** `schedule_agent.py` was a dead 3,610-line
   predecessor while the shipped agent was `schedule_agent_1455mh.py` bundled under that same name.
   **75 scripts imported the dead one**, including all three sell diagnostics.

---

## Handoff, using only (c)

`docs/handoff_2026-08-15.md`.
