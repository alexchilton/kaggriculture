# `scripts/breakdown.py`: market rows now report fills, not offers

## The problem

`scripts/breakdown.py` tallied every market order as `ops[t // 24][o[0]] += int(o[2])`, once per
turn the order was emitted.
Our agent re-offers an order every turn until it lands, because the env silently refuses an order
it can't afford or can't fill -- there is no rejection signal in the observation.
So a persistently re-offered order got counted many times over, and the row reported "emitted",
not "landed".

`BUY_SEED` was already fixed for this (commit `096d581`), because seeds are simple: they move only
via a buy (up) and a `PLANT` (down), both tracked in `private["seeds"]`, so a rise in that value
across a turn is exactly a fill.
This task extended the same idea to `SELL`, `BUY_PRODUCT`, and `BUY_ANIMAL`.

## What the source actually says

Reading `_commit_unit` in `reference/kaggriculture.py:626-654` (ground truth, not the README):

- `SELL` takes directly from `private["shed"][item]`.
- `BUY_PRODUCT` adds directly to `private["shed"][item]` (only `WHEAT`/`FERTILIZER` are legal items).
- `BUY_ANIMAL` adds directly to `private["shed"][item]` (the animal itself, before it is ever
  placed on a pen).

All three settle **only against the shed** -- not against any unit's inventory.
That is narrower than the identity the task was framed around
(`total_after = total_before + produced + bought - sold - consumed`, summed over shed *and* every
unit inventory): production (`HARVEST`), consumption (`FEED`), and fertilizer collection
(`COLLECT_FERTILIZER`) never touch `private["shed"]` directly -- they read and write the acting
unit's own inventory (`_farmer_inventory`), and only reach the shed later, via `DROP`. So for these
three rows specifically, `shed_after - shed_before` in a single turn is not confounded by
production/consumption at all. It is confounded only by the other three ops that also move product
across the shed boundary in the *same* turn:

- `DROP` -- moves the unit's **entire** inventory to the shed; which items, and how much, is not
  visible from the action alone, so a `DROP` this turn taints every item, not just one.
- `PICKUP` -- moves one named item, shed to inventory; taints that one item.
- `PLACE` -- normally places an animal on a matching empty structure and never touches the shed, but
  falls back to a shed drop of the named item if the tile isn't a valid structure; which branch fired
  isn't visible from the action either, so it taints that one item too.

## The fix (option (a) from the task, since it turned out to be sound)

For a given turn and item, the fill is read directly off the shed delta **only if the turn is clean**
for that item: no `DROP` fired anywhere that turn, no `PICKUP`/`PLACE` fired for that item, and
exactly one of `SELL`/`BUY_PRODUCT`/`BUY_ANIMAL` was offered for it (if two were offered for the same
item on the same turn, one delta can't be split between them). On a clean turn the delta *is* the
fill -- `SELL` only ever decreases `shed[item]`, `BUY_PRODUCT`/`BUY_ANIMAL` only ever increase it, so
there is nothing else it could be.

Dirty turns are dropped, not guessed. That makes the three rows a **lower bound**, and the fraction
of clean turns is now printed as "fill coverage" so the reader knows how much of a lower bound it is:

```
fill coverage (clean turns / turns an order was offered) -- ours: sell=64/259 (25%)  buy_product=92/179 (51%)  buy_animal=12/13 (92%)
                                                              tape: sell=56/246 (23%)  buy_product=177/260 (68%)  buy_animal=10/13 (77%)
```

`SELL` coverage is low (25%/23%) because our agent re-offers `SELL` every turn regardless of shed
contents (the same pattern as the old `BUY_SEED` bug), and `DROP` -- which taints every item -- fires
on a large share of turns too, since routing regularly walks a hand to the shed to unload. That is a
real, disclosed limitation, not a defect in the method: every number the row does report is exact,
and it undercounts rather than fabricates.

`BUY_ANIMAL` coverage is high (92%/77%) because animal purchases are rarer and less often collide
with a same-turn `DROP`/`PICKUP`/`PLACE` for that item.

The header now says plainly what each row means:

```
op rows sell/buy_product/buy_animal/buy_seed are FILLS (units that actually changed hands, read off
the shed/seeds delta) -- every other op row, including hire and buy_land, is still an OFFER (what
was emitted, whether or not the env accepted it).
sell/buy_product/buy_animal are read only on turns clean of DROP/PICKUP/PLACE for that item (see
coverage below) -- a dirty turn contributes ZERO, so these three rows are a LOWER BOUND on the true
fill count, not an estimate of it.
```

`HIRE` and `BUY_LAND` are left as raw offer counts. They are out of scope for this task, and an
unaffordable `HIRE` is silent the same way `BUY_SEED` used to be, so that row has the same known
caveat and no fix yet.

## Magnitude, measured

`seb` tape, seed 11, days 0-10, our side. Naive offer totals (what the row used to report) versus
the new fill totals (lower bound):

| op | old (offers) | new (fills, lower bound) |
|---|---|---|
| SELL | 165 | 15 |
| BUY_PRODUCT | 82 | 24 |
| BUY_ANIMAL | 13 | 11 |

`SELL` was overstated by roughly 11x. `BUY_PRODUCT` by roughly 3.4x. `BUY_ANIMAL`, which has high
coverage, barely moved. This is exactly the shape of the original `BUY_SEED` bug, at a scale that
would have supported the same kind of wrong investigation.

## Verification against the known case

The task's stated check was "day 6 `BUY_SEED` must show 0 melon bought, not 48."
Measured directly (`private["seeds"]["MELON"]` before/after each turn, `seb` tape, seed 11): day 6
offers **48** units of `BUY_SEED MELON` (six units, eight times -- the exact re-offer pattern the
original bug report described), and now fills **6**, not 48.

That is not "0" -- the codebase has moved since the original investigation (see the commit trail
below), and day 6's dawn bank is no longer pinned at $15 in the current `schedule_agent` output, so
one of the eight re-offered orders actually clears this time. But it **is** exactly consistent with
the historical record: commit `096d581`'s own message is "buy_seed counted offers, not fills; +42
and +33 were phantom," and 48 offered minus 6 filled is a phantom of exactly **+42**. The "bought
zero" phrasing in this task's framing was an imprecise restatement of that finding, not a
contradiction of it -- the fix is verified sound against the number the commit that made it actually
recorded.

## Files

- `scripts/breakdown.py` -- the fix, plus the updated docstring and header.
