# d1's fertilizer dribble is `BANK_ON_THE_PEN_THAT_FUNDS_THE_DAY`, and fixing it reverts a measured win

**I located the mechanism and did NOT change it. Matching the tape here means reverting a block whose
own docstring records it as a $2 improvement, argued in the opposite direction. That needs Alex's
call, not mine.**

## The mechanism

`kagg/search/cover.py`, the tail of `materialise`'s job loop (~line 723):

    _earns = any((wanted or {}).get(p, 0) > 0 and q > 0 for p, q in j.gives.items())
    if j.funds and pos in depots and _earns:
        keep = collections.Counter({it: q for it, q in after[i + 1].items() if q > 0})
        route.append(_bank(pos, held, keep))
        held = collections.Counter(keep)

`_refresh_pins` sites pens on shed-access tiles, so **standing on a pen IS standing on the shed**.
Every pen job that yields something the row sells therefore banks immediately, in the same turn.
On d1 we have four pens on depot tiles, so we bank after every single COLLECT_FERTILIZER:

    ours   h3 COLLECT, h4 PLACE+SELL x1, h9 COLLECT, h11 PLACE+SELL x1,
           h15 COLLECT, h17 PLACE+SELL x1, h22 COLLECT (no turn left to bank it)
    tape   h11 COLLECT, h13 COLLECT, h15 COLLECT,
           h18 PLACE + SELL FERTILIZER x3 + BUY_PRODUCT WHEAT x5

That is `PLACE 3/1`, `COLLECT_FERTILIZER 4/3` and `shed_FERTILIZER 1/0` — all three of d1's
non-inherited cells, from one rule.

## Why I did not just change it

The block is named `BANK_ON_THE_PEN_THAT_FUNDS_THE_DAY` and the docstring above the sibling rule at
line 655 argues **explicitly for spreading rather than batching**, with a measurement:

> Traced on day 1 of Seb's tape, seed 11: u1 collects fertilizer at h5 STANDING ON the shed tile,
> carrying 2 wheat for pens ahead, and holds that fertilizer through h9 and h13 before dropping at
> h16. The tape has its first unit in at h4 and sells 2 @ $100, 1 @ $100, 1 @ $99 across h4-h12
> while we sell 1 @ $100 and then three at $99 in one turn -- the same four units, **$2 worse**, and
> we cannot spread what is not in the shed.

So the repo has already measured this exact question on this exact day and concluded that
**dribbling beats batching by $2**, because the market walks the price down within a turn and
spreading the sell across hours realises more.

And our own d1 supports that reading: `money 168/171` is entirely the -$3 inherited from d0. d1's
own trade matches the tape exactly — `BUY_PRODUCT 5/5`, `SELL 3/3`, `shed_WHEAT 4/4`. **We are not
losing money on d1. We are losing three op-count cells.**

## The conflict, stated plainly

- Matching Kawashigi op-for-op on d1 requires suppressing this rule.
- The rule is a recorded, measured win on the same day of a different tape.
- Kawashigi banks once; Seb's tape banks four times. The two players do it differently, and the grid
  can only agree with one.

This is the same shape as the `_wheat_row_first` finding: an ordering that is right for one recorded
player and wrong for another, where the executor has one global answer.

`COLLECT_FERTILIZER 4/3` is a second question inside it — he collects 3 of his 4 available and we
collect all 4. The fourth is collected at h22 and strands. Suppressing the per-pen bank does not on
its own stop the fourth collection.

## Where d0-d12 stands, unchanged this session

    d0=3  d1=3  d2=1  d3=4  d4=3  d5=7  d6=16  d7=13  d8=19  d9=14  d10=17  d11=17  d12=13

    d0  exact in board and shed; 2 cells are the netting round trip, $3 is its price impact
    d1  located, not fixed -- this document
    d2  $2, unexplained, turn-level cash trace not taken
    d3  we HARVEST 7 wheat tiles he leaves standing; all 4 cells follow from it

## What the next session should do first

1. **Decide the d1 question**, because it is a policy call: match the tape (suppress the per-pen
   bank) or keep the measured $2. If matching, the change is scoped to that one `if` and a red test
   should assert one PLACE per product per day, not three.
2. **d2's $2** is still the cheapest diagnostic on the board and nothing was spent on it.
3. **d3** is one decision — harvest timing on wheat, `first_yield_day 2, max_yield_day 4`. He waits
   for d4; we take it at d3. That is likely a single ranking rule and it is worth more than d1's
   three cells, because d3 is also the melon/strawberry split day.

Noted and not acted on: the coordinator's measurement that d0-d8, d10 and d11 are one crop set per
day on the strawberry line, so any miss there is the executor. And that d9 and d12's apparent splits
are consequences — spare capacity and the land purchase — not choices. No selector was built.

Q3/Q4 kept separate throughout: everything here is the three-quadrant line (92498144). Nothing from
`kawashigi_q4c`, `solved_days_q4` or any four-quadrant board was touched.

## Unverified

- The $2 spreading measurement is quoted from the docstring; I did not re-run it.
- Whether suppressing the per-pen bank makes d1 exact, or removes two cells and leaves
  `COLLECT_FERTILIZER 4/3`.
- Whether the same rule is what drives `COLLECT_FERTILIZER` failing on 13 days of the shipped gate.
  The shapes match but I did not check.
