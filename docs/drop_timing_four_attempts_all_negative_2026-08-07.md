# Getting the harvest home earlier: four attempts, all negative

The full patch of the last attempt is kept at `data/logs/fable_drop_timing_attempt.patch`.
It is **not** applied — it measures a loss — but it is worth reading before anyone tries a fifth time.

## The symptom, which is real and traced

`scripts/where_the_cow_goes.py 11 --day 4`, on Seb's plan:

- the crew harvests from h5
- the FIRST `DROP` lands at **h19**
- so `SELL WHEAT` cannot be offered until h19, and the bank sits at $316 from h0 to h18
- a `BUY_ANIMAL` is bank-gated, so the COW only settles at h19
- at h19 the free pens are 3 steps off with 4 turns left, and PICKUP + 3 moves + PLACE is 5
- the cow is never placed: `PLACE 0 against the tape's 1`, `tile:animal 6 against 7`
- the next morning's seed order half-fills, so we plant 8 tiles against his 13

The return leg fires only when a unit's route is EMPTY, and a unit that keeps being topped up never empties until dark.

## What was tried

Baseline throughout: 12 seeds, `weedSpawnChance 0.005`, **$119,281** on our schedule and **$96,064** on Seb's.

| # | rule | result |
|---|---|---|
| 1 | at a depot, DROP if inventory exceeds `sum(n.needs)` over the remaining route | our $119,281 -> **$104,009**, Seb's $96,064 -> **$84,913**; broke `test_wheat_already_in_a_hand_feeds_the_herd_with_an_EMPTY_shed` |
| 2 | same, but per-item, with the route recomputed fresh and re-booked into `st["draw"]` for a same-depot redraw | broke the same test |
| 3 | farm-wide `FEED_DAYS * alive` threshold with no per-unit awareness | broke `test_feeding_three_pens_costs_exactly_one_shed_trip` and `test_a_hand_spawned_on_a_locked_shed_cell_walks_to_one_we_own` at FEED 0 — an endless PICKUP/DROP loop that never reached a pen |
| 4 | BOTH gates at once: this unit's own live `future_needs`, AND the farm-wide `FEED_DAYS * alive` reserve, AND a `MIN_OPPORTUNISTIC_DROP = 4` load floor, firing only when the tour-walk already chose a MOVE | tests green, **mechanism worked**, economics did not: our $119,281 -> **$110,989** |

## Why attempt 4 is the informative one

It **did** what it set out to do.
The first DROP of the day moved from **h19 to h5**, and the day-4 cow the whole trace was built around was placed.

And it still lost $8,292, because:

```
DROP     116 -> 137 a season
HARVEST  300 -> 294
```

Twenty-one extra shed trips bought six fewer harvests.
The turns spent banking the load outbid the fieldwork the earlier cash was meant to free.

That is the finding: **the harvest arriving late is not free money being left on the table — it is already priced.**
A unit standing at a depot is not idle; it is one step into its next job, and pens sit ON depot tiles by design (`_refresh_pins` prefers shed-access cells), so a unit servicing the herd passes a depot constantly. Every one of those moments is a candidate DROP, and taking them costs a turn each.

## The two failure modes any fifth attempt must survive

Both are recorded in the patch's own comments and both are subtle:

1. **Self-healing depends on units keeping their load.** When a unit's nodes fail (the depot-draw race on turn 0, when the shed is genuinely empty and `st["draw"]` silently clears), the unit goes idle and the `if idle:` top-up re-plans it using `load[u]` — *that unit's own current inventory* — which absorbs newly orphaned FEED nodes at zero depot cost, but only while the wheat is still physically in hand. Emptying the hand destroys the raw material the recovery runs on.
2. **A unit ferrying wheat to its own FEED stop must not read that wheat as surplus.** With the shed stocked past the reserve, a farm-wide-only test sees just-picked-up, still-in-transit wheat as spare and drops it back next turn, forever.

## Recommendation

Stop attacking this from the DROP side.
The measured cost of a late harvest is the *ordering* of the day, and four attempts say the turns needed to fix the ordering cost more than the ordering is worth.

If it is revisited, the promising direction is not "drop more often" but "**plan the depot as a node**" — let `plan_routes` place a shed visit in the tour where it is cheap, and pay for it honestly in the prize/cost ratio, rather than bolting an override onto the walk. That was listed in the original brief and never reached.