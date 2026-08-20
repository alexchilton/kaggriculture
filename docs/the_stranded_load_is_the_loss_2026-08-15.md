# The season ends with the crew holding the margin

Measured 2026-08-15 off three downloaded ladder replays, at the final step of d29.
Read from the recordings, not simulated.

    episode     our stranded          their stranded     result
    93318573    81 units  ~$3,264      4 units  ~$19     lost by   $645
    93323101    55 units  ~$3,526      0 units    $0     lost by $3,919
    93286476    70 units  ~$2,238      0 units    $0     lost by   $962

**In all three the stranded value exceeds the losing margin.** Two of the three are wins if that
produce reaches the shed. Our shed is EMPTY at the close in all three; the goods are in hands.

## Why it happens

`_end_of_day` calls `_drop_inventories_to_shed`, so on any ordinary day a carried load reaches the
shed for free. That is why カワシギ emits **five** DROP ops in the whole of `92498144` against 389
harvests -- he almost never needs one.

On d29 that drop still runs, but it runs after the final turn, and `_commit_unit` refuses a SELL
unless the goods are already in `private["shed"]`:

    if op == "SELL":
        if private["shed"].get(item, 0) <= 0:
            return False

So the pipeline is **one day delayed**: harvest on day N, banked free at the N/N+1 rollover, sold on
day N+1. Anything harvested on d29 has no day N+1.

The tape solves it by spending **9 DROPs on d29** against our 2.

## The consequence that makes this cheap

A d29 harvest that is not delivered is worth **exactly zero -- the same as not harvesting it.**
So turns spent walking to the shed on d29 cost nothing real. There is no trade-off to balance.

## Three fixes tried, all measured, all recorded so they are not re-tried blind

1. `WALK_THE_LOAD_HOME_DAYS = (10, 29)` -- recovered 7 units of 58. A solved route stores work stops
   only; `materialise` appends the shed trip out of slack, and d29 has none.
2. `NO_UPKEEP_ON_THE_LAST_DAY` -- frees 28 turns (FEED and CARE on d29 pay out at a rollover into a
   day 30 that does not exist; the tape does zero of both). **Regressed** the grid: harvest
   396 -> 389, sell 1489 -> 1474, and d29 HARVEST fell 27 -> 20 while gaining 28 turns, because
   `cover._apply_precomputed` keys a stop on `(tile, ops)` -- change the ops and the stop leaves the
   route rather than getting cheaper.
3. `UNSOLVE_DAYS = (29,)` -- greedy plans d29 with `deliver=True`. Sell 1489 -> 1502, d29 sell
   93 -> 106, +$256, harvest 396 -> 393. Stranded rose 51 -> 78: the greedy harvests more than it
   walks in.

## Also measured and NOT the cause

- **d28 is not under-prioritising.** Its solved route seats every job with slack and two hands idle;
  only 7 ripe units remain unharvested at dusk. Promoting d28 harvests by prize, by `at_risk`, and
  by `at_risk` plus a d28 re-solve were all three byte-identical on the grid.
- **Planting dates are identical to the tape** -- d25 9/9, d26 9/9, d27 11/11 -- so his crops do not
  ripen earlier than ours.
- Shed overflow discards only 5 units a season.
- Spreading the sell across hours instead of one is worth $64.

So what gives him d28 harvest 32 to our 27, and d29 19 to our 27, is still unexplained. It is
neither ranking nor planting date.

## Where the fix has to go

`RESERVE_DAYS` already covers d29 and `cover.cost` already knows how to price a tour that ends at
the shed. Two things block it: the reserve is gated behind `deliver=True`
(`PRICE_THE_TOUR_THE_CALLER_WILL_WALK`), which only d10 sets, and d29 is precomputed so `cover.cost`
never runs at all. A fix needs the delivery to be a **planned stop** -- either stored in the solved
route, or budgeted before the work is seated -- rather than appended from slack that does not exist.
