# Geese, eggs, and what the arithmetic actually says

Written 2026-08-15, at Alex's instruction to *do the math, not an experiment*.
Everything here is computed from `reference/kaggriculture.py`, with opponent volumes read off the
three ladder replays downloaded the same day.
**No simulation of our agent is involved**, deliberately: whether our planner can currently execute
a plan is a separate question from whether the plan is right.

---

## 0. Why this was reopened

`HERD_GEESE` was measured on 2026-08-11/12 as a disaster — 0 birds 69.4% win, 2 birds 38.9%.
That verdict is **dead**, and the dates say so:

    2026-08-11/12   HERD_GEESE measured
    2026-08-13      c99a8a5 fixes SELLABLE

`SELLABLE` listed six of the env's nine products and is the iteration domain of the only loop that
emits a SELL. CARROT, TOMATO and **EGG could not be sold at all**. So the sweep measured geese that
produced eggs which could never be turned into money: pure cost, zero revenue, on any flag, on any
day. It is not evidence about geese.

This is the third time in this project that a mechanic-level negative turned out to be an artifact.
See `project_kaggriculture_animals_verdict`.

## 1. Production, from the env's own loop

`_daily_refresh_animals` (`reference/kaggriculture.py:805`), stepped exactly, one animal placed d5,
fed and cared every day, harvested as it fills:

    animal   cost  structure  first_yield  interval  max_held  product   units/season
    GOOSE    $300  COOP                 4         1         4  EGG                 46
    COW      $400  PASTURE              8         2         6  MILK                30
    SHEEP    $500  PASTURE              6         3         6  WOOL                30

**The model is validated against a real game**: it predicts 30 milk per cow, and game `93239838` has
9 cows producing ~290 milk — 32 per cow. Close enough to trust the rest.

The goose is the cheapest animal, starts four days earlier than a cow, and produces **every day**
against the cow's every-other and the sheep's every-third.

## 2. Revenue, with the opponent in the same book

The first version of this calculation priced our units into an empty book and reported milk at
$155/unit. Every real game contradicts that — milk closes at $1-$5. The error was leaving out the
**opponent's flow**, and correcting it is what produces the finding.

Both seats settle into ONE inventory. Measured opponent season volumes:

    MILK  250-410      WOOL  ~250      EGG  0    -- and ours is 0 too

> **RETRACTED 2026-08-15. These two volumes are summed sell OFFERS, not fills.** The agent re-posts
> an unfilled order every turn, so they are inflated by roughly 6x. Measured against market
> inventory instead: across 26 replays a no-yarn board ends at `inv - I0 = +59` units of wool for
> **both herds combined**, and `93240733` lands at +59 with the opponent running zero sheep. Real
> wool supply is ~8 units per sheep per season, so two full herds move ~60-70 units, not 500.
> Milk was checked the same way and is ~200-240 units per seat per season, realised at $37-$78 a
> unit on a milk-poor board and $231 on a milk-rich one. **Every number below that uses `theirs`
> is therefore wrong and the ranking must be re-derived from fills before this doc is used again.**
> See `feedback_offers_are_not_fills`, which this document violated.

Six animals, net of purchase cost:

                              2 shops draining it    ZERO shops draining it
    GOOSE   276 EGG,   0 theirs       $11,270                $9,818
    COW     180 MILK, 300 theirs      $10,392                  $556
    SHEEP   180 WOOL, 250 theirs      $32,910                $1,174

The goose loses **11%** when its drain disappears. The cow loses 77%, the sheep 88%.

## 3. Expectation over the real shop draw

Shops unlock one per three days on days 3..24 — eight draws, uniform over the eight types, with
replacement. So instances carrying a product is `Binomial(8, m/8)` for `m` carrier types. Exact:

    animal  product  types  P(zero)   E[revenue]  worst 10%    net E
    GOOSE   EGG          2    10.0%       12,678     11,618   10,878
    COW     MILK         3     2.3%       21,278      5,575   18,878
    SHEEP   WOOL         1    34.4%       22,590      4,174   19,590

**The math does NOT say switch to geese.** On expectation a cow or sheep beats a goose by about
$8,000 per six animals. Anyone quoting this doc for "geese are better" is misreading it.

What it says is that the goose is the only animal whose floor is close to its mean. Its worst-decile
revenue is more than double either alternative's, and the sheep — the highest expectation of the
three — returns $1,174 net on the **34.4%** of draws with no YARN_STORE.

Two structural reasons the egg book does not move:

1. EGG's curve is `log` with `above_target 0.2`, which is effectively undentable — the fragility
   table in `docs/when_and_what_to_sell_2026-08-15.md` puts EGG and WHEAT alone in that class.
2. **The opponents submit fixed 720-turn scripts.** They cannot start producing eggs in response.
   The egg book stays uncontested in every game, all season, by construction — which is a much
   stronger guarantee than any of our own price modelling.

## 4. What follows, and what does not

**Follows:** the herd choice should be conditional on the draw, and geese belong in the option set
as insurance against the egg-rich / yarn-poor corner. `SHOP_ADAPT_HERD` cannot express this — it
floats COW against SHEEP only.

**Does not follow:** a blanket switch to geese. The expectation says that loses money.

**The real cost of building it**, stated plainly because it is the reason this is not a flag flip:
`SHOP_ADAPT_HERD`'s swap is free *because COW and SHEEP both build a PASTURE*, so nothing in the
build schedule, the pen geometry or the routing changes. **A goose builds a COOP.** Adding it means
changing what gets built and where, which is a real change to the opening, and the opening is
matched to the tape.

## 5. Caveats a reader should hold

- `theirs` is three games. It is the right order of magnitude and the EGG=0 term is structural, but
  MILK 300 and WOOL 250 are estimates.
- Even production spreading is assumed. Real release is lumpier, which hurts the fragile products
  (milk, wool) more than the robust one (egg), so this if anything **understates** the goose's edge
  on the tail.
- Feed cost is not netted. Every animal eats one wheat a day, so it is close to a constant across
  the three and does not move the ranking, but the absolute nets are optimistic.
- No op-cost is charged. A goose fills at 4 units against the cow's 6, so it needs collecting more
  often — more HARVEST stops for the same crew. That is a real cost and it is NOT in these numbers.
