# The third quadrant arrives a day late

Measured 2026-08-17 on 19 ladder replays in `data/seed_scripts/ladder_2026-08-17/`.
Scripts: `scripts/where_the_day_went.py`, logs under `data/logs/*_2026-08-17.log`.

## Two theories died

**"We over-water."** Dead.
We out-water every opponent on the ladder by +190 to +970 waterings in d11-d29, and we win most of
those games.

    water d11-29    us/them      result
    BeyondAnalytics  988/368     WIN +69,104
    Borys Tymchenko  971/0       WIN +84,068
    Akira Imae      1002/821     LOSS -5,508
    koren sabag     1015/821     LOSS   -158

The water count does not separate wins from losses. It is a property of our agent, not a defect.

**"The problem starts around d20."** Dead.
Cumulative plantings, us/them, against the script that beats us:

    day         4       6       8      10      12      15      20      29
    us/them  22/19   26/25   45/50   50/74   84/94   97/99  130/128  197/199

The deficit opens at d8, peaks at **d10 (50 vs 74)** and is closed by d15.
We plant the same 197 seeds all season, three to five days later each.

## What actually happens

    93839424 vs koren sabag -- quadrants owned, end of day
    day        6     7     8     9    10    11
    us         1     2     2     2     2     3
    them       2     2     2     2     3     3

We are one day behind on quadrant 2 *and* quadrant 3.

The d10 hour trace:

    d  h |     us $ usQ |   them $ themQ
    9 23 |    1,129   2 |    2,655     2
    10 1 |      986   2 |    3,064     3   <== they buy Q3
    10 23|    6,395   2 |    6,511     3
    11 1 |    6,824   3 |    7,121     3   <== we buy Q3

`LAND_PRICES = [1000, 2000, 4000]` (`reference:97`), so Q3 costs **$2,000**.
At d10 h1 we hold **$986**. We do not attempt the purchase — the only `BUY_LAND` we emit all season
is at d11 h1. `_do_buy_land` also fails **silently** on a thin bank (`reference:717-718`), so an
early attempt would leave no trace either.

The constraint is cash at d10 h1, and it is set on **d9**: we end d9 on $1,129, they end on $2,655.
Our money arrives in a lump at d10 h23 ($1,527 -> $6,395); theirs arrives smoothly across the day.
`LATE_SELL_FROM_HOUR = 16` is the obvious suspect and is **not yet tested**.

## It is our fixed schedule, not the seed and not the shops

First day each quadrant is owned, across all 19 replays:

    Q2    us: d6 in 14 games, d7 in 5        them (821-script): d6
    Q3    us: d11 in 19 of 19                them: d10
    Q4    us: never (one game, d12)          them: never

**Q3 lands on d11 in every single game.** Zero variance over seeds, shop draws and opponents, so
this is a hard-coded day in our plan rather than a board-dependent decision.

Planted tiles at d10 end, us/them, against the 821-script: 29/56, 35/56, 30/55, 35/56, 35/56,
35/56 — about half their acreage.

Two open items this raised:

- We have **never** bought quadrant 4 ($4,000), one game aside. Nor does anyone in this sample,
  so it may be correct, but it has never been tested.
- Q2 slips d6 -> d7 in 5 of 19 games. That one *is* variable and is unexplained.

## Cost

21 tiles lose a full day of growth, in every game against this opponent.

## What this is NOT

- It does not explain the MilanJoshi loss (-$7,727). There the quadrant timing is **identical**
  (both reach 3 quadrants at d11) and the difference is crop mix: at d10 we hold 19 STRAWBERRY /
  7 MELON against his 11 / 8. Different cause, still open.
- It is not sufficient to flip a game on its own. **Tom Yim runs the same script with the same
  50/74 profile and we beat him by $5,275.** The lag is a standing handicap, not the trigger.

## The opponent field

Three distinct scripts, identifiable by their d11-d29 signature:

    water/harv/plant     games                                      our record
    821 / 363 / 199      Moshel, Yan, INDRAJIT, Akira, koren,       1 W, 5 L
                         Tom Yim, Sankalp                           (+2 W at 812)
    734 / 364 / 187      MilanJoshi, Dmitry Larko                   1 W, 1 L
    715 / 327 / 174      Tita, Issac, Rheal                         3 W

The 821-script is the one to beat. We now hold seven examples of it.

## Next test, untried

Get $2,000 into the bank by d10 h1 and buy Q3 on d10 instead of d11.
Judge it on the d10 planting count (50 -> ~74) and the d11-d29 harvest count, replayed against the
821-script tape, **not** on season money.

Risk to check first: d12-d29 runs on precomputed routes, and a route is a visit ORDER over tiles.
Moving the quadrant a day earlier changes the board at the d11 handover, so stops can be dropped
silently. Prove the route survives before trusting the money.
