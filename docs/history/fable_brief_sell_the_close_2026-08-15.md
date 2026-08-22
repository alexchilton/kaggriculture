# Brief: copy カワシギ's close. Sell everything on d29, harvest everything on d28.

Written 2026-08-15 as the handoff to Fable.
Alex's instruction, verbatim:

> we really need to copy kawa to get those items sold.
> no watering no feed and care just get shit sold on d29 and as much as possible on d28

## The loss this fixes, measured on three real ladder replays

| episode | our stranded | their stranded | result |
| --- | --- | --- | --- |
| 93318573 | 81 units ~$3,264 | 4 units ~$19 | lost by $645 |
| 93323101 | 55 units ~$3,526 | 0 units | lost by $3,919 |
| 93286476 | 70 units ~$2,238 | 0 units | lost by $962 |

The stranded value exceeds the losing margin in all three, and our shed is empty at the close.
Two of these three are wins if that produce reaches the shed.

## Why it strands

`_end_of_day` calls `_drop_inventories_to_shed`, so a carried load banks itself free at every
rollover. That is why the tape emits **5 DROPs in a whole season against 389 harvests**.

The pipeline is therefore **one day delayed**: harvest on day N is banked overnight and sold on
day N+1. Day 29 has no N+1. Its automatic drop fires after the final turn, and `_commit_unit`
refuses a SELL unless the goods are already in `private["shed"]`. So a d29 harvest that is not
walked to the shed **is worth exactly zero -- identical to not harvesting it at all.**

That is the key economic fact: turns spent walking home on d29 cost nothing real.
There is no trade-off to balance.

## The closing grid, ours/tape, seed 11, kawashigi tape

    row              d27       d28       d29
    feed           14/14     14/10     14/0
    care           14/12     14/9      14/0
    collect_fert   14/12     14/9      14/0
    harvest        31/35     29/32     26/19
    drop            0/0       2/0       2/9
    sell          ...       103/92    93/148
    pass          ...        48/32    30/56

He does **zero** feed, care and fertilizer collection on d29 against our 42 unit-turns.
He harvests 32 on d28 to our 27, banks it overnight free, and turns d29 into a selling day:
148 units to our 93, with 9 DROPs to our 2.

## Four fixes already tried. All failed. Do not re-try blind.

1. `WALK_THE_LOAD_HOME_DAYS = (10, 29)` -- recovered 7 of 58 units.
   A solved route stores work stops; `materialise` appends the shed trip out of **slack**, and d29
   has none.
2. `NO_UPKEEP_ON_THE_LAST_DAY = True` -- regressed harvest 396 -> 389 and sell 1489 -> 1474.
   `cover._apply_precomputed` matches a stop on `(tile, ops)` ONLY. Removing FEED/CARE changes the
   key, so the stop **leaves the solved route entirely** instead of getting cheaper. This is the
   central landmine.
3. `BANK_THE_FIELD_ON_D28` / `BANK_THE_FIELD_ON_THE_LAST_FREE_DROP_DAY` -- promoting a ripe d28
   tile to CRITICAL was byte-identical three separate ways (prize, at_risk, at_risk + re-solve).
   d28 is already saturated: every job with slack is seated, two hands idle, only 7 ripe units
   left at dusk.
4. `UNSOLVE_DAYS = (29,)` -- +13 sells, +$256, but stranded ROSE 51 -> 78.

Also ruled out: shed overflow (5 units/season), spreading the sale ($64), planting dates
(identical to the tape on d25 9/9, d26 9/9, d27 11/11).

## What is NOT explained

Why he harvests 32 on d28 to our 27 and 19 on d29 to our 27, when our plantings and our ripening
are identical to his. It is neither ranking nor planting date. If Fable finds this, it is the win.

## The fix Alex endorsed

> a delivery that's planned, not appended

`RESERVE_DAYS` already covers d29 and `cover.cost` already knows how to price a tour that ends at
the shed. Two things block it:

- the reserve is gated behind `deliver=True` via `PRICE_THE_TOUR_THE_CALLER_WILL_WALK`
  (`cover.py:1375`), and only d10 sets `deliver` (`schedule_agent.py:869`,
  `DELIVER_CUTOFF_TURNS = 99` against budgets of 23-24);
- d29 is precomputed, so `cover.cost` never runs on it at all.

Suspected third blocker: the reserve branch also requires a non-empty `wanted` row.

## Constraints

- **DO NOT REGRESS d0-d8.** Anything before d23 must stay byte-identical.
- One delta at a time. If two flags are live, measure the 2x2.
- Write the test RED first, then fix, then confirm it goes red on revert.
- Never sum offers. Use `kagg/analysis/fills.py` or shed/money deltas.
- Never call a mismatch "small". Never add a tolerance.
- Do not run the full pytest suite.
