# What the town will actually eat

Measured 2026-08-11 off the 87 recorded ladder games in `data/seed_scripts/top_guys`, by reading
each game's closing `market.inventory` against its own `town.unlocked_shops`.
No simulation and no agent is involved: the book and the shop list are both `shared: True` in the
observation, so these are facts the game hands us.

Two numbers per product.
**Appetite** is what the town removes over a season, from `_town_consume`: every `townShopSellInterval`
(4) steps each shop instance takes one of each product it sells, doubled if it sells only one, and
every `townCenterSellInterval` (24) steps the town centre takes one of everything except fertilizer.
Over 719 steps that is 179 shop ticks and 29 centre ticks.
**Surplus** is `closing inventory - 10000`: units that were sold and never eaten, which is what a
floored price is made of.

## The shop table

| product | shop types carrying it (of 8) | season appetite | closing surplus, 87 tapes |
|---|---|---|---|
| WHEAT | 5 | 745 – 1,282 | **−386 to −1,356** |
| CARROT | 2 (PET_CAFE single-product, counts double) | 29 – 924 | −12 to −1,002 |
| TOMATO | 2 | 208 – 924 | −30 to −678 |
| STRAWBERRY | 4 | 387 – 1,282 | −381 to +60 |
| MILK | 3 | 566 – 1,103 | −342 to +77 |
| EGG | 2 | 208 – 566 | −624 to +108 |
| WOOL | 1 (YARN_STORE, single-product, counts double) | 29 – 387 | −424 to +59 |
| MELON | **0** | **29 on every board** | **+38 to +158, always positive** |
| FERTILIZER | **0** | **0 on every board** | **+201 to +493, always positive** |

## Fertilizer pays well and then stops paying, permanently

`reference/kaggriculture.py:101` builds the town centre's list as `[p for p in PRODUCTS if p !=
"FERTILIZER"]`, and no shop lists it either.
So fertilizer demand is zero on every board there is — this is not a property of one town seed, it
is a property of the rules.

The price curve is `linear` with `above_target 0.40` and `T = 200`, so every unit sold knocks about
$0.40 off and nothing ever puts it back.
Every other product's book gets drained back down; fertilizer's only ratchets one way.

| units sold | marginal unit | cumulative | average |
|---|---|---|---|
| 50 | $90 | $4,755 | $95 |
| 100 | $80 | $9,010 | $90 |
| 150 | $70 | $12,765 | $85 |
| 200 | $60 | $16,020 | $80 |
| 250 | $50 | $18,775 | $75 |
| 400 | $20 | $24,040 | $60 |
| 500 | $1 | $25,052 | $50 |

So the first hundred units are excellent — $9,010, better per unit than anything else on the board —
and units 250 to 500 fetch $6,277 between them, less than the first seventy earned.

**Every one of the 87 tapes closes with fertilizer between $1 and $20**, against a base of $100.
The book is saturated at the end of every game that has ever been played here.
Both farms sell into it, so the question is never "is fertilizer worth selling" but "did we get
there before the other farm did".

## Melon is the same shape, and we plant 17 tiles of it

No shop carries melon, so the town centre's 29 units a season is the entire market, on every board.
17 tiles at a measured 12 units a tile is 204 units into an appetite of 29, and the melon price is
`sq` with `above_target 3.60` — it reaches $1 about 190 units above I0.

All 87 tapes close with a melon surplus, +38 to +158, so **every player over-plants melon**, the
winners included.
That makes it a shared inefficiency rather than a losing move, and therefore an edge available to
whoever fixes it first.
It is also **not a decision the shop draw can inform**, which is why `SHOP_ADAPT_CROPS` deliberately
leaves melon out of every swap pair: how much melon to plant is a fixed-quantity question and a
separate one.

## Wheat is the scarcest thing on the board

Wheat's closing surplus is negative in all 87 tapes, by 386 to 1,356 units — the town eats far more
than both farms together produce, so the price *rises*, closing at $40–$59 against a base of $25.
It is carried by five of the eight shop types, more than anything else.

That is worth holding next to the shipped comment in `schedule_agent.py` that calls growing
wheat "a bad trade" on the grounds that a tile yields six units.
The measured figure in `kagg/economics/production.py` is 28, or 42 fertilized.

## What this does not say

Appetite is a ceiling on what the town removes, not a prediction of what we will sell.
Both farms sell into one book, and none of this models turns, walking, watering, or the fact that a
tile has to be reached before it can be harvested.
These rank products; they do not price a season.
