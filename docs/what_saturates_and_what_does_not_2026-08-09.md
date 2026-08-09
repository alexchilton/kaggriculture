# What saturates, what does not, and how much we throw away

2026-08-09, on `shaping-potential`. Pins `tests/test_the_planner_prices_volume.py`.

Stage 1's `revenue_rate` capped production at `DRAIN_UNITS * OPPONENT_SHARE` and valued every unit
at half base price.
Both halves are wrong, and the cap is the worse one: melon yields 12 units a tile against a cap of
15, so **two melon tiles and sixteen scored identically (62.50)** and the planner stopped buying
melon ground.
Correcting `DRAIN_UNITS` to 1.32.6 dropped melon's drain 140 -> 30 and made the error 4.67x worse.

The replacement prices volume on the environment's own `market_price`, with a rival-supply term.
By the time we have sold our `k`-th unit the book sits about `k * (1 + contest - drain/units)`
above `I0`.

## Where each product stops paying

First local peak, `CONTEST = 1.0`, i.e. the opponent sells as much as we do.

```
  product       base  drain  peak units     $/u   season $  tiles/head
  WHEAT           25    553         276    25.0      6,900         6.6
  CARROT          35    317         156    35.0      5,460         4.0
  TOMATO          60    209         104    60.0      6,240         6.5
  STRAWBERRY     120    452         224   120.0     26,880        18.7
  MELON          250     30          88   179.0     15,748         7.3
  MILK (cow)     160    322         160   160.0     25,600         2.4
  WOOL (sheep)   200    204         112   192.2     21,529         2.3
  EGG (goose)     50    256         128    50.0      6,400         1.2
  FERTILIZER     100      0        4000     4.1     16,250         n/a
```

**Read "first local peak" literally.** The global maximum is meaningless: once `market_price` bottoms
out at the $1 floor, revenue is `q * $1` and rises forever, so a global search returns "dump 3,000
units at $5". The first version of this table did exactly that and reported wheat, carrot, tomato,
melon, egg and fertilizer all saturating at 3,000 units. That is the search limit, not economics.

## Geese are the exception, and they are the only one

Priced per *head* rather than per unit, milk and wool go flat almost immediately and eggs do not:

```
  animal    1      2      4      6      8     12     16     20  head
  COW     480    960   1164   1164   1164   1164   1164   1164   <- flat from 4
  SHEEP   400    800    897    897    897    897    897    897   <- flat from 4
  GOOSE   200    343    652    955   1257   1845   2424   2998   <- still climbing at 20
```

A goose yields every day from day 4 (`interval` 1, `max_held` 4), so twenty geese make 2,080 eggs a
season, and egg's book is shallow enough that 2,080 units still realise ~$37 against a $50 base.
Milk and wool crash; eggs barely bend.
Geese are also the cheapest animal at $300 against a cow's $400 and a sheep's $500.

## Fertilizer is species-independent, and it has no drain

`kaggriculture.py:818` sets `tile["fertilizer_available"] = True` for **every animal tile, every
day**, outside the yield conditional.
`COLLECT_FERTILIZER` (502-508) adds exactly one unit and clears the flag.
So a $300 goose produces the same 1 fertilizer/day as a $500 sheep, regardless of species,
`interval`, `max_held`, or whether the animal was fed that day.
Twenty animals is ~600 units a season.

`TOWN_CENTER_PRODUCTS` excludes FERTILIZER (line 101) and no shop carries it, so its drain is
**zero** -- nothing ever leaves that book but our own sales.
`DRAIN_UNITS` has no entry for it, which is correct rather than an omission, and
`sale_revenue` now uses `.get(prod, 0)` for exactly this reason.

## The part that contradicts the leaders, and is therefore probably wrong

The model says four cows and four sheep, and does not move much with the contest assumption:

```
  saturation head-count by CONTEST
  animal       0.0    0.25     0.5     1.0     1.5
  COW            5       4       4       3       2
  SHEEP          5       4       3       3       2
  GOOSE        >32     >32     >32     >32     >32
```

Seb, rank 1 at 3,201, runs **9 cows and 11 sheep**. The `v23_fork` cluster runs 8 and 6. Our model
says everything past four is waste. One of those is wrong, and the rank-1 player is the less likely
candidate.

Candidate explanations, none measured yet:

* CARE compounding. `pending_care_bonus` adds to `yield_units` on a fed production day, so a cared
  herd yields more per head than `events * max_held` assumes, but that raises supply and would make
  saturation *worse*, not better.
* The book recovers continuously, and `drain * k / units` models that as a straight line. A herd
  that sells in small daily parcels realises more than one that dumps.
* `BUY_PRODUCT` conversion: buy cheap wheat, feed it, sell expensive milk. That values an animal by
  its conversion margin rather than by its product's book depth, and it is the one lever where
  `what_the_others_do.py` put us at only the 49th percentile.

**Do not act on the herd numbers in this document.** The saturation figures for crops are sound;
the animal figures contradict the strongest observed evidence on the ladder and need reconciling
first. `docs/the_top_five_clusters_2026-08-09.md` has the observed builds.
