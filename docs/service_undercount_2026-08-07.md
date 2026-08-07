# `Node.service` under-counts, worst at the depot

Measured 2026-08-07, seed 11, weeds off, against Seb's replay, days 0-12.
Probe: `scratchpad/service_probe.py` wraps `plan_routes` to capture the service it assumed for every
`(day, unit, tile)` stop, then watches each unit's position turn by turn and counts the turns it
actually spends working there.

## The finding

`plan_routes` costs a stop at `Node.service`, which is `len(ops)` fixed at plan time
(`router.py:470`).
The executor does not replay that list.
It re-derives the tile's ops from the live board via `_live_ops` on arrival and only leaves once
they are exhausted, so a tile planned as one WATER can offer WATER *and* HARVEST when the unit gets
there.

Restricted to stops the unit actually reached:

| | visited stops | planned | actual | overrun |
|---|---|---|---|---|
| depot cells `(4,4) (5,4) (4,5) (5,5)` | 30 | 77 | 114 | 19 stops, 63% |
| field tiles | 260 | 410 | 454 | 70 stops, 27% |

Every day from d3 onward is positive.
Worst single stops are all depots: d0 u0 at `(4,4)` planned **1** and took **7**; d11 u9 at `(5,5)`
planned 1 took 5; d9 u1 at `(4,5)` planned 1 took 5.

## Why the depot is worse

`Node.service = len(ops)` and `ops` never contains PICKUP or DROP.
Those are emitted by the executor's own depot logic (`_router_acts`: the `if pos in SHED and
shed.get(item, 0) > 0` PICKUP branch, the opportunistic drop, `DELIVER_THE_SELL_ROW`, and the
return leg), none of which exist as nodes.
So a depot stop is priced at zero-to-one turn and routinely takes five to seven.

## Why it matters upstream of everything else

Under-costed tours mean `plan_routes` accepts more stops than the day can execute.
Tours then do not finish, which is the mechanism behind the defect measured separately all day:
goods stay in hands, the shed is empty when the market reads it, and `pickup` runs ahead of `drop`
by a margin that grows monotonically from d0 (cumulative 73/56 against 53/66 by d10).

This is why it must be fixed **before** a delivery node is added to `build_nodes`.
A delivery node's whole value is that the router can weigh it against other work; if the cost model
under-prices every existing stop by 11% in the field and 48% at the depot, the comparison it makes
is wrong, and `router.py` already records two reverted closed-tour attempts that both broke
`d3 sell 5/5 -> 3/5`.

## Caveat on the first reading

The first aggregate compared all 600 planned stops against 426 observed work sites and reported the
estimate as *over*-counting on most days.
That was confounded: a stop planned but never reached contributes its service with zero actual and
says nothing about the estimate.
Only stops with `actual > 0` are evidence, and on those the sign reverses.
