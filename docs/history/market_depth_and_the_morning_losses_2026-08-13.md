# How deep each market is, and why the two losses of 2026-08-13 happened

Both losses are near-mirrors decided in the last third of the season, and both point at the same
thing: **we ship volume into products the town does not drain, and under-ship the one it does.**

## The depth table (computed from `reference/kaggriculture.py`, not from play)

`market_price` depends on **market inventory only**. Shops move the price solely by draining that
inventory, so exactly two numbers matter per product: how much the town absorbs over a season
(= the sustainable sell rate) and how much net excess takes the price to $1.

    product      base  shops   drain     p@50    p@100    p@200     to $1
    ------------------------------------------------------------------------
    WHEAT          25      5     525       22       21       21     never
    CARROT         35      2     327       27       23       19       842
    TOMATO         60      2     228       42       35       24       529
    STRAWBERRY    120      4     426       24        1        1        62
    MELON         250      0      30      225      150        1       158
    EGG            50      2     228       43       42       41     never
    MILK          160      3     327       55        1        1        76
    WOOL          200      1     228       55        1        1        59
    FERTILIZER    100      0       0       90       80       60       493

`drain` is the expected season total: instance N unlocks on day 3N so it is live for `180 - 18N`
four-step ticks (792 tick-instances over eight draws), shops are drawn **with replacement** from the
eight names, and a single-product shop consumes double (`_town_consume`).
`p@N` is the price after N units of net excess sit in the book.

Read off it:

- **WHEAT and EGG never floor.** Both decay as `log`, so the price is essentially flat: 200 wheat
  still fetches $21 of a $25 base, and 200 eggs $41 of $50. These are the two bottomless markets.
- **WOOL, MILK and STRAWBERRY are shallow to the point of fragility** — 59, 76 and 62 units of
  excess and they are at $1. Wool and milk are also the two highest-value products, so they are
  simultaneously the best and the easiest to destroy.
- **MELON has no shop at all.** Its only buyer is the town centre, 1 unit per 24 steps, 30 a season.
  A $250 base with a 30-unit season of real demand.

**The EGG line matters for the goose axis.** Egg is one of the two products that cannot be flooded,
and it was unsellable until `c99a8a5` — so every previous goose measurement was taken with the
revenue line disconnected. That is now in the running sweep as a live axis.

## `92550780` — lost $69,881 to $77,275 (-$7,394)

The town drew `YARN_STORE` **three times** and `PET_CAFE` twice, so it wanted **1,074 wool** and
**716 carrot** over the season.

    WOOL   closed $252  of base $200   drained 1,074   <-- ABOVE base all season
    CARROT closed $ 42  of base $ 35   drained   716   <-- ABOVE base all season
    MILK   closed $  5  of base $160   drained   358
    STRAW  closed $  3  of base $120   drained   179
    MELON  closed $ 25  of base $250   drained     0

Wool closing **above** its base means total supply never caught the drain: every additional wool
unit that season was worth about $250 and there was room for it. We had **8 sheep to Densike's 4**
and shipped a fraction of the wool they did — on the slice of turns where attribution is
unambiguous, 28 units / $6,738 against 115 units / $28,158.

At the same time we put milk and strawberry on the floor, in a game where the town drained only 358
and 179 of them.

## `92562037` — lost $129,161 to $133,724 (-$4,563)

A true mirror: both sides ~148 wheat, both ~13 animals, near-identical sell cadence.
The one large divergence is **melon — we planted 136 to their 19**, into the product with zero
shops. It closed at **$25 of a $250 base**.

## Both losses are lost after day 18

    92550780   d18 -$84       d21 -$10,532     d29 -$7,394
    92562037   d18 +$6,363    d21 -$1,155      d29 -$4,563   (their last day +$10,469 to our +$4,080)

The opening is not the problem in either game. The late season is.
The first `SELL CARROT` is step **598** and **617** — day 25 — in games where the town was draining
carrot from day 3.

## Attribution caveat

Per-seat units are computed from the shared market ledger,
`inv(t) - inv(t-1) = sold_us + sold_them - bought - town_drain`, which is exact only on turns where
one side alone trades that product. Most volume lands in a `shared` bucket (1,260 and 1,803 units)
and is **not** split by a guess. The wool ratio above is the unambiguous slice, not the season total.

## The melon/strawberry answer is CONDITIONAL, and the running sweep cannot find it

Strawberry floors after **62 units** of excess, and its drain swings from 179 to 895 units a season
purely on how many strawberry-carrying shops the town draws.
That makes the melon/strawberry split a *conditional* answer, not a constant one:

    92562037   5 instances carry STRAWBERRY   drained 895   closed $187 (above base)
               -> a melon tile converted to strawberry was worth several times more
    92550780   1 instance  carries STRAWBERRY  drained 179   closed $  3 (floored)
               -> the swap buys nothing; that town wanted WOOL and CARROT

The stake is 19 melon tiles against 36 strawberry tiles, not the hundreds an earlier draft of this
doc claimed — see the correction below. The per-unit gap is real (strawberry realised about $211 a
unit in `92562037` against melon's $25 close); the tile count it applies to is small.

**`scripts/product_search.py` varies `melon_day` and `melon_shift` globally**, across whatever shop
draws the seeds happen to produce. If the truth is "strawberry when the town draws strawberry shops,
melon otherwise", then a global axis averages the two regimes together and reports a **wash** — the
arm that wins on one draw loses on the other, and the marginal comes out flat.

A flat marginal on that axis is therefore **not** evidence that the split does not matter. It is the
expected result of asking a global question about a conditional quantity. The same trap would have
hidden `WOOL_SHOP_SETS_THE_HERD`, which only reads as a rule once the games are split by the draw.

The fix is to slice the dump by shop draw rather than to add another axis — `--analyse` already
keeps every game, and the shop list is recoverable per seed.

## The closing days: a bare pasture, and one starved cow

Alex spotted an empty pasture. It is real, it is in every game checked, and there are two separate
causes behind it.

`kaggriculture.py:804`: **two consecutive unfed days and the animal escapes, leaving the structure.**

    92550780   final herd COW 6 SHEEP  8   bare structures 1   escapes 0
    92562037   final herd COW 9 SHEEP  4   bare structures 2   escapes 1  (COW, day 24, -$400)
    92548920   final herd COW 6 SHEEP  8   bare structures 1   escapes 0

So one bare pasture per game is a pen **built and never stocked**, and in `92562037` a second one is
a cow that starved on day 24 — $400 of stock plus five days of milk, in a game lost by $4,563.

The bare pen appears on day 24 and is still bare on day 29 in both losses. We were holding $53k and
$95k at that point; a sheep costs $500.

## Why the herd was too small in `92550780`, specifically

The town drew **`YARN_STORE` three times** — at draw #1 (d3), #4 (d12) and #6 (d18). Three
instances is 6 wool a tick, 1,074 a season. Eight sheep produce roughly 100 units in a season (first
yield day 6, one unit every 3 days). The town wanted ten times what we could make, which is why wool
closed **above** base at $252 and never came down.

**The split rule fired correctly and the COUNT is what failed.** Every `BUY_ANIMAL` we issued:

    d0  COW 1, SHEEP 4     d4 COW 1   d5 COW 1   d6 COW 1   d7 COW 2
    d8  SHEEP 2            d12 SHEEP 1          d18 SHEEP 1
    ------------------------------------------------------------------
    total requested        COW 6, SHEEP 8   =  14 animals

`WOOL_SHOP_SETS_THE_HERD` did exactly what it is written to do: yarn was in the first three draws,
so cows were held at `WOOL_SHOP_COW_CAP = 6` and every remaining animal went to sheep. But the
rule's own reference table says a draw-#1 yarn store means **COW 6, SHEEP 12, total 18**, and we
ran a total of **14**. `_herd_split` re-splits a `want_total` it is handed and is explicitly
forbidden from growing it ("capped at the schedule's own count"), so the sheep-heavy half of the
rule landed and the extra four animals never did. `92548920` — yarn at draw #2 — is the same:
COW 6, SHEEP 8, total 14, where the table says 18.

**And the early return skips the one branch that does count instances.** Below the wool rule,
`_herd_split` runs a greedy over `town_drain_remaining(...) + expected_future_drain(...)`, which is
genuinely instance-aware and would have seen three yarn stores. The wool rule `return`s before it.
So the code's drain-aware allocation is bypassed in precisely the case where the drain is extreme.

**The bare pen is the same story from the other end.** Fifteen `BUILD_PASTURE` ops, and pens are
still being built on d21 (2) and d24 (1) — after the last animal purchase on **d18**. Fifteen pens,
fourteen animals.

## `92566708` — the herd starved to death on day 12

Lost $56,006 to $109,034, the worst of the five. **Twelve of fourteen animals escaped on days 10-13**
— $5,200 of stock, plus every unit of milk and wool for the remaining seventeen days. The agent
never rebuilt: it finished with **2 cows and 13 bare pens**, feeding exactly 2 animals a day from
day 20 to the close.

    day  feeds  harv  wheat_shed  money  hands
      8      9     1           0    137      6
      9     10     4           0  1,377      7
     10      1     1           0      1     14     <-- first escape
     11      0     0           0     75     10
     12      0    13           0     22     10     <-- eight escape in one day
     13      0     0           7    167      8

`FEED` takes one WHEAT from the acting hand's inventory (`kaggriculture.py:496`), and two consecutive
unfed days releases the animal (`:804`). The shed held **zero wheat from day 8 through day 12** while
the bank sat at $1, $75 and $22 — so neither the stock nor the cash to buy it existed, and a herd of
fourteen needs fourteen wheat every single day.

This is a **liquidity failure that converts directly into destroyed capital**, and nothing in the
agent treats the feed bill as a committed liability the way `RESERVE_THE_SEED_BILL` treats seeds.

## Five games, one repeated waste

Across all five games downloaded on 2026-08-13:

> **CORRECTION, same day.** An earlier version of this table read melon and carrot counts out of
> `why_we_lost.py`'s `crops planted (offers)` column, which prints **BUY_SEED order quantities**, not
> plants. The agent re-posts a standing order every turn, so those numbers are re-offers. Alex caught
> it: *"we have a carrot plant of 6 i dont understand how we planted 42"*. Real plants, counted off
> tile transitions, are the same in every game: **WHEAT 138, STRAWBERRY 36, MELON 19, CARROT 6.**
> The claim "we planted 136 melon to their 19" was an artifact — both sides plant 19.

    game       MELON plants   MELON closed   EGG drained   EGG closed   geese   CARROT plants
    92550780        19            $25            179          $59          0          6
    92562037        19            $25            537          $67          0          6
    92564858        18            $19            537          $70          0          5
    92565805        19            $16            537          $70          0          6
    92566708        19            $10          1,074          $88          0          6

**Melon closed between $10 and $25 of a $250 base in every single game.** It has no shop and the town
absorbs 30 units a season, so nineteen plants a side is already enough to bury it.

**Carrot is the sharper number.** Six tiles at 4 units each is about 24 units of carrot, against
towns draining **716, 895 and 716** — and carrot closed ABOVE base every time it was drawn. Carrot
also has the deepest glut tolerance of any crop (842 units to the floor), so there is no price risk
in growing far more of it.

**EGG closed ABOVE base in all five**, between $59 and $88, with the town draining up to 1,074 units
— and we ran zero geese in all five, because EGG was unsellable when the goose flag was measured.

## On the forum claim ("multiply base by shop count")

Half right, and the half that is wrong is the half that matters. Shop count sets the **sustainable
rate**, not the price: the price is a pure function of inventory. Milk with three shops still floors
after 76 units of excess, which is why our own milk has repeatedly closed at $1-$5 while the claim
says it "sells above 160 most of the season". Both statements are true at different volumes — the
drain is about 327 milk a season, roughly 11 a day, and a herd that produces faster than that puts
its own price on the floor no matter how many shops are open.
