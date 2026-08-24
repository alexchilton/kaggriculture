# Withholding the carrot is a LOSS — measured 2026-08-24

Stealth's item 1, "abstention gate first (smallest diff, unblocks D)", was implemented and measured.
**It loses money.** Recorded here before reverting, so it is not re-derived.

## What was built

`schedule_agent.hold_the_book(orders, day, withholding)` drops `SELL` orders for a crop we are
cornering until `SELL_THE_SHED_FROM_DAY`.
Wired into the wrapper with the corner's decision moved *before* the order build, so the window's
first day can see it.
Six unit tests, red first, then green (`tests/test_we_do_not_supply_the_book_we_are_cornering.py`).

Two supply paths were closed by the one rule:

1. The planner's own sell cadence, which emits `SELL CARROT` on d21–d25.
2. `sell_all_the_wool`, which — despite the name — operates on
   `_SELL_THE_WHOLE_SHED = ("WOOL", "CARROT")` and is applied on **every** day, while its sibling
   `top_up_the_sell_orders` is gated to d29.
   So any accumulation day the cadence touched carrot, the order was resized to the entire shed.

I called that second one a defect. **It is not. It is where the money comes from.**

## The measurement

Paired, same seed, same replayed prefix to d21, both arms on the new deficit-reading gate.
`control` = no abstention. `treat` = abstention.
`tape` replays both tapes to the bell and never calls our agent; it reproduces `recorded` to the
dollar on all six, so the harness is faithful.

```
   episode   recorded       tape    control      treat       bias  flip  tiles   d29 c/t  price  deficit
  98495047    -29,384    -29,384     -5,313    -27,185    +24,071            0     32/80    316      845
  98460892       -614       -614    -11,885    -11,973    -11,271            0      6/69     96      562
  98494953     -3,472     -3,472    -24,350    -24,350    -20,878            1       3/3     60      327
  98499540     -1,940     -1,940    -11,229    -11,229     -9,289            0       6/6     52      223
  98501831     -6,070     -6,070    -12,887    -12,887     -6,817            0       6/6     54      242
```

Abstention only *changes* anything on the two deep towns — the four drain-2/3 towns are identical in
both arms, which is the gate correctly standing down.
On the two where it fires:

    98495047   -5,313 -> -27,185     -21,872     position 32 -> 80
    98460892  -11,885 -> -11,973          -88     position  6 -> 69

## Why holding loses

The hinge curve cuts both ways.
Holding 80 units to d29 and dumping them at once walks our own close down to $316.
Selling 48 of them across d21–d28 took the price the book offered each day and never paid the
walk-down.
The corner's arithmetic in `corner_the_book.plan` sizes the position so we stay above the knee
*after our own dump* — and on 98495047 it still landed us $21,872 behind simply selling as we went.

This does not refute the SOUTA decomposition.
He banked 76 units at $498 where our 80 fetched $316, and the difference is that **his opponent was
not also dumping**.
In our replay the recorded opponent sells his own carrot into the same close, so two dumps split one
book, exactly as Stealth predicted in Q4 — but the split is not benign at our size.

## What this does NOT say

- It does not say the deficit-reading gate is wrong.
  The gate is doing its job: it built an 80-unit position in a drain-11 town and a 6-unit one in a
  drain-2 town.
- It does not say the money column is trustworthy in absolute terms.
  `bias` runs to −$20,878 — our agent taking the wheel at d21 on a board it did not plan, running
  kawashigi's schedule. Only the paired `control` vs `treat` difference is readable.
- It does not test a *partial* hold. Every unit was held. A rule that holds half and sells half was
  not measured.

## Reverted

Per the standing rule, a measured null or loss is deleted, not left behind a switch.
