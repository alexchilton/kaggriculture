# Three ladder games, 2026-08-15 — one win, two losses

Read off the downloaded replays only.
No simulation for the market numbers, so none of them can be an artifact of our own harness.
The solver-seating section IS a local replay and says so.

    93237183   WIN    us $117,976  vs Farfadet        seat 0   seed 1158229392
    93239838   LOSS   us  $87,726  vs mashBrian254    seat 1   seed  702042888
    93242536   LOSS   us $111,741  vs Alexandre008    seat 1   seed  195279982

All three: `weedSpawnChance 0.005`, `townCenterSellInterval 24`.

Downloaded games are SELECTED — Alex downloads losses — so nothing here is a win rate.

---

## 1. Did the solver get used?

Yes, about two thirds of it, and **the seating does not predict the result**.

Replayed each game on its own `info.seed`, our shipped agent in our real seat, the recorded
opponent's actions in theirs, then read `cover.PRECOMPUTED_MISSES`.

    game       result   stops offered   skipped   seated
    93237183   WIN               1115       471      58%
    93239838   LOSS              1115       373      67%
    93242536   LOSS              1115       366      67%

    seed 11 vs the kawashigi tape (what they were solved on)   1115    0     100%

The win has the WORST seating of the three.
So the stale-route theory does not explain these losses.

Per-day, on 93239838 — the miss grows through the season:

     day  stops  missed  seated%
      12     44       8      82%
      13     61       7      89%
      14     54      14      74%
      15     62       8      87%
      16     58      18      69%
      17     64      15      77%
      18     60      30      50%
      19     64      21      67%
      20     73      22      70%
      21     70      22      69%
      22     71      25      65%
      23     70      31      56%
      24     71      34      52%
      25     65      31      52%
      26     69      25      64%
      27     72      32      56%
      28     51      18      65%
      29     36      12      67%
     ALL   1115     373      67%

This closes item (b)4 of `RETRACTIONS.md` — "that the regenerated routes generalise off seed 11".
They partly do.
Skipped stops are not dropped; they fall through to `_insert_leftovers`.
100% on the solving seed against 58-67% on a ladder board is the overfit, measured.

Log: `data/logs/solver_seated_93239838.log`, `..._93237183.log`, `..._93242536.log`.

---

## 2. Did the melon sell properly on d10?

No, and the reason is **delivery, not the sell gate**.

The sell rule sells out of the SHED. On d10 the melon is in HANDS all afternoon.
Identical shape in all three games — hour trace, our seat, `MELON`:

    93239838 (LOSS)                      93242536 (LOSS)
     h12  hands  6  book 272  --          h12  hands  6  book 272  --
     h13  hands 12  book 272  --          h16  hands 30  book 272  --
     h16  hands 42  book 272  --          h18  hands 48  book 250  --
     h18  hands 54  book 250  --          h19  hands 54  book 244  --
     h19  hands 48  book 250  SELL  6     h21  hands 48  book 232  SELL  6
     h21  hands 48  book 246  SELL  6     h22  hands 36  book 205  SELL 12
     h22  hands 18  book 226  SELL 30    d11 h00        book 144  SELL 36
    d11 h00 shed 12  book 213  SELL  6   d11 h21        book 106  SELL  6
    d11 h01          book 169  SELL 12

The first offer is h19 or h21.
For seven hours before that we hold 6 -> 54 ripe melons at a book of **$272** and cannot offer any of
them, because they are being carried and the market only sees the shed.

Realised on 93239838: 60 units for about **$218 each**.
Selling the same 60 from h12, walking the book down from 9989, averages about **$250**.
The prize is roughly **$1,900** — real, and not the reason either game was lost.

`SELL_AT_ONCE_DAYS = (10, 11)`, shipped this morning, is not what is binding on d10 — every sale is
past `LATE_SELL_FROM_HOUR = 16` anyway. It DOES bind on d11: 93239838 sells at h00 and h01, which
without the exemption would have waited until h16 while the opponent walked the book down.

**The open work is a mid-day DROP at the shed on the melon flush**, so the crop can be offered while
the book is still at $272 instead of on the closing walk.

---

## 3. What actually lost these games

The shop draw decides which products the town absorbs, and we produce the same mix regardless.

### 93239838 — the town wanted eggs and strawberry; we made milk and wool

    SHOPS  BAKERY x1, BRUNCH_SPOT x5, FARMERS_MARKET x1, SMOOTHIE_SHOP x1

    drained over the season      closing price     base
      WHEAT       1,253            $ 49            $ 25    starved
      STRAWBERRY  1,253            $268            $120    starved
      EGG         1,074            $154            $ 50    starved, nobody produced any
      MILK          179            $  3            $160    FLOORED
      CARROT        179            $ 46            $ 35
      TOMATO        179            $ 79            $ 60
      WOOL            0            $  1            $200    FLOORED, no YARN_STORE all season

Our herd: **9 COW, 4 SHEEP** — the same as in the game we won.

WOOL, by day, our seat, from the shared book and our own shed:

    day  book inv  price   we sold   we got
     10     10016    185         1     $185
     13     10031    144         8   $1,152
     14     10059      1         5     $510
     15-29  10059      1        90      $90

The whole season's wool: about **130 units for $1,940**, against 4 sheep at $500 each plus feed and
CARE turns. The book floors between d13 and d14 and never moves again, because nothing drains it.

MILK floors at d19 the same way — drain 179 against roughly 290 units produced.

**MILK floored in all three games: $3, $5, $1.** That is not a seed, it is 9-10 cows.

### 93242536 — a different draw, same failure on the other product

    SHOPS  FARMERS_MARKET x1, ICE_CREAM_SHOP x2, PET_CAFE x2, SMOOTHIE_SHOP x1, YARN_STORE x2

      CARROT        895   $ 77 of $35   starved, we planted 63
      STRAWBERRY    716   $139 of $120
      WOOL          716   $236 of $200  fine here — YARN_STORE drawn twice
      MILK          537   $  1 of $160  FLOORED anyway
      WHEAT         537   $ 43 of $ 25

Here wool paid and carrot was the miss: 895 units of season demand at $77 a unit, and we planted 63.

---

## 3b. A cow starves on day 11, and we pay $400 to replace it

Alex asked whether the herd count ever changes. Across all 18 downloaded games of this agent:

    (COW, SHEEP)   games
    (6, 8)             9
    (10, 4)            5
    (9, 4)             4

    herd TOTAL:  14 in fourteen games, 13 in four games

The shipped plan asks for **COW 10 / SHEEP 4 = 14** (`kagg/plan.py:SHIPPED_PLAN`, rows d0 d3 d5 d7
d8 d9 d11). So `SHOP_ADAPT_HERD` is working — the split really does move, and sheep-heavy games are
the ones with YARN_STORE drawn — but **13 is not a choice, it is a loss.**

The four 13-animal games are exactly the four games with an animal escape:

    game        result   our escapes   where
    93182759    WIN            1       d16 (3,5) COW
    93186363    LOSS           1       d11 (6,4) COW
    93237183    WIN            1       d11 (6,4) COW
    93239838    LOSS           1       d11 (6,4) COW

`_daily_refresh_animals` (`reference/kaggriculture.py:817`): two consecutive unfed days and the
animal is removed, the structure left standing. Nothing else in the env removes a placed animal
(`:487` is explicit about it). Tile (6,4) in 93239838, straight off the replay:

    d8  h5   fed_today true, cared h6         consecutive_unfed 0
    d9  h0   fed_today false ... never fed all day
    d10 h0   consecutive_unfed 1, never fed all day
    d11 h00  {"kind": "PASTURE"}              the cow is gone
    d11 h7   a replacement cow placed, placed_day 11

The cow was placed on d7. `first_yield_day` is 8, so its first milk would have been d15. **It
starved before producing a single unit**, and the d11 purchase that looks like herd growth is
actually paying $400 again for a cow we already owned.

Two separate costs, both measurable: the wasted $400 and placement turns, and one pasture of
fourteen standing empty from d11 to d29.

The same tile and the same day in three of four cases says this is reproducible, not bad luck. It
is a FEED scheduling miss on d9 and d10, and FEED is the op with the highest correlation to money
in this project (+0.452).

Log: `data/logs/animal_escapes.log`, `data/logs/tile_6_4_93239838.log`.

## 4. What this points at

`SHOP_ADAPT_HERD` floats the cow/sheep SPLIT and keeps the COUNT — its own comment says so:
*"The COUNT the schedule asks for is kept exactly; only the species is re-decided."*

On 93239838 the right herd was the floor. `HERD_FLOOR_COW = 4`, `HERD_FLOOR_SHEEP = 1`; we ran 9 and
4 into a town that absorbed 179 milk and 0 wool.

Not proposed as a change here, and not measured. Three games is three games, and
`project_kaggriculture_animals_verdict` records that "animals don't pay" has been an artifact four
separate times. The next arm is the COUNT, not the split, and it needs the same A/B discipline as
the melon rule got.

The second, cheaper thread: STRAWBERRY, CARROT, WHEAT and EGG books were **starved in every one of
the three games** — every one closed above base, several at 2-3x. Nothing we grow is worth less for
growing more of it in those four.
