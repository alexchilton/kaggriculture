# What the ladder losses actually say — 2026-08-11

Ten downloaded ladder episodes, `weedSpawnChance = 0.005`, `kaggle_environments 1.32.6`.
Every number here is read off the recordings; nothing is simulated, so nothing can be an artifact of
our own harness.

> **THIS IS A SAMPLE OF LOSSES, NOT A RECORD.** Alex downloads the games we lose; the one win in the
> table is incidental. So "1W 9L" says nothing about the win rate, and **any conclusion drawn by
> comparing us to the opponent is conditioned on our having lost** -- of course those games are
> close-but-behind on money. The "we out-earn them and spend the difference" finding at the bottom
> of this file carries that bias and must be re-measured on an unbiased sample before it is acted on.
>
> What is NOT biased: the shop-coverage table (read from the environment source, nothing to do with
> outcomes), the per-seed drain figures (a property of the seed draw), and our own fixed play --
> `MELON 69` and `COW 10 SHEEP 4` on every board -- which is visible in any sample whatsoever.
>
> The only unbiased score available is the ladder rating itself.

```
   episode seat opponent                    ours    theirs  res    margin
  91989194    1 Ahmet Abdullah Gültekin    67,479    82,289 LOSS   -14,810
  91997704    1 Thomas                   110,406   125,098 LOSS   -14,692
  92003395    0 Maksim Borisov            65,206    75,164 LOSS    -9,958
  91994863    1 Ahmet Abdullah Gültekin    58,925    68,349 LOSS    -9,424
  91992972    1 YassY_The_AlchemYst       94,903   102,207 LOSS    -7,304
  92007122    0 Maksim Borisov            60,662    67,908 LOSS    -7,246
  92005219    0 chunluran                126,598   128,330 LOSS    -1,732
  92077611    0 Subin An                 117,414   118,800 LOSS    -1,386
  91996770    0 kazwzn S                  54,991    55,566 LOSS      -575
  91986409    0 midori_farm              124,208    33,171  WIN    +91,037
```

## The finding that survived every challenge: no shop drains MELON

`SHOPS` in `reference/kaggriculture.py:90` is the whole demand side of the game:

```
    "BAKERY":         ["EGG", "WHEAT"],
    "PIZZA_SHOP":     ["MILK", "TOMATO", "WHEAT"],
    "BRUNCH_SPOT":    ["EGG", "WHEAT", "STRAWBERRY"],
    "YARN_STORE":     ["WOOL"],
    "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"],
    "PET_CAFE":       ["CARROT"],
    "SMOOTHIE_SHOP":  ["STRAWBERRY", "MILK"],
    "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"],
```

The union is `{EGG, WHEAT, STRAWBERRY, MILK, TOMATO, WOOL, CARROT}`.
**MELON is absent, on every seed, by construction.**
It was drained 0 units in 10 recordings out of 10 and closed at $4–$25 against a base of $250.

`schedule_agent.py:1372` already knows this — *"MELON: carried by no shop, so no draw can ever help
it"* — but the knowledge lives in the **sell** rule and never reached the **planting** rule.

## The consequence: the second melon wave is planted into a market we personally destroyed

Measured on 92077611 (loss by $1,386), from `private["shed"]` deltas, which for MELON are exact
fills — a melon leaves a shed only by being sold, it is not feed and not an input to anything.

```
   day   price |  ourShed  ourTiles  |  cumulative sold / revenue
  d10      272 |        0         9  |   30 units  $ 7,452     <- the d0 planting, 5 tiles x 6
  d19      183 |        0        14  |   30 units  $ 7,452     <- growing, not held
  d20      184 |        0         9  |   48 units  $10,188
  d21       54 |        0         1  |   96 units  $12,210     <- the d10 planting lands
  d22        4 |        0         0  |   96 units  $12,210
```

- **Wave 1** — 5 tiles planted d0, ripe d10, 30 units into an untouched book: **$7,452** (~$248/unit).
- **Wave 2** — 9 tiles planted d10, ripe d20, 66 units into the book wave 1 spent: **$4,758**
  (~$72/unit, ending at $1).

`ourShed` is **0 on every day of the season**: we sell a melon the turn it is harvested.
There is no holding defect, and an earlier session note claiming one was wrong.
Melon's `first_yield_day` is 10, so a tile planted on d10 *cannot* yield before d20.
The only lever is not planting it.

Those nine tiles held ground d10–d21 for $4,758.
As WHEAT — 4-day cycle, 6 units, the ~$45 the book actually paid, ~2.5 cycles — the same ground is
worth roughly **$6,075**, about +$1,300 against a $1,386 loss.

### That swap is WRONG, and the reason is the whole point about melon

The arithmetic above counts our gain and assumes the opponent's revenue is unchanged.
It is not.
Melon has no drain, so the melon money in a season is a **fixed pot that goes to whoever sells
first**, and our wave 2 is what emptied it:

```
              ours                    theirs
  d19    30 units  $ 7,452      66 units  $13,362
  d20    48 units  $10,188      66 units  $13,362
  d21    96 units  $12,210      96 units  $13,608
  d24    96 units  $12,210     138 units  $13,701
```

His last **72 units fetched $339 — $4.71 each**, because our 48 hit the book first.
Ours in the same window fetched **$72 each**.
Vacating d20 hands him a book at ~$184 for those 72 units; that is plausibly $6–7k to him against
$1,300 to us, on a game lost by $1,386.

**So melon wave 2 is a denial play, and it is working.**
We win melon on price ($127/unit against his $99) and lose it on volume (96 units to his 138).

**Rule:** melon is a race for a fixed pot, not a crop with a yield.
The lever is not planting less, it is **ripening earlier** — `first_yield_day` is 10, so a wave
planted d8 lands d18 and takes the book before the opponent's second wave exists.
Any change here must be scored on the *margin*, never on our own revenue, because every melon we do
not sell is one the opponent sells at a price we chose not to destroy.

## We play the identical season on every seed

```
  episode      our herd            our crops                         town's top demand
  91997704   COW 10 SHEEP 4   WHEAT 115  STRAWB 57  MELON 69    STRAWBERRY 1,074
  92003395   COW 10 SHEEP 4   WHEAT 113  STRAWB 66  MELON 69    CARROT     1,253
  92007122   COW 10 SHEEP 4   WHEAT 110  STRAWB 75  MELON 69    WHEAT      1,074
  91996770   COW 10 SHEEP 4   WHEAT 117  STRAWB 74  MELON 69    WHEAT      1,253
  91986409   COW 10 SHEEP 4   WHEAT 117  STRAWB 76  MELON 69    STRAWBERRY 1,074
  92077611   COW 10 SHEEP 4   WHEAT 171  STRAWB 93  MELON 69    WHEAT      1,253
```

`MELON 69` on six different seeds with six different towns.
`router.py:88` states the cause plainly: *"WHEAT/STRAWBERRY/MELON only -- confirmed by reading
`data/seed_scripts/new_leader/schedule.json`"*.
The crop list was copied off one leader's schedule and is not a function of the town.

**We never plant CARROT or TOMATO.**
Both closed **above base in 10 games out of 10** (CARROT $40–42 on base $35; TOMATO $77–118 on base
$60), because both are drained by shops and neither seat ever supplies them.

TOMATO is not a general replacement — at ~8 units/season it is ~$39/tile-day against WHEAT's ~$67
and STRAWBERRY's ~$65.
Its value is that its price is **drain-supported**, so it is the right home for the ground currently
growing the second melon wave.

## What is NOT the problem

- **Late-season watering.** Weeds from a missed watering, us vs them across the ten:
  `47/23, 39/57, 47/30, 39/17, 34/29, 19/33, 33/33, 43/30, 34/0, 32/20`.
  We are worse in five and better in four, and lost regardless.
  A whole session went into tour execution against the tape while the losses were decided elsewhere.
- **WOOL.** Wool is drained 0 in six of the ten (only `YARN_STORE` carries it) and we keep sheep
  regardless — but in 92077611 the opponent ran **6 sheep to our 4** into a zero-drain wool book and
  still won. It cannot be the differentiator.
- **Crop revenue, in the close games.** On 92077611 realized fills were **ours $135,999 vs theirs
  $132,961** — we out-sold him by $3,038 and lost by $1,386.

## The open lead: spending, not earning

Money is `3000 + revenue - spend`. On 92077611 that gives **us $21,585 spent against their $17,161**
— $4,424 more, on a game we lost by $1,386.
Their closing-week buy counts run 15–67 a day against our fixed 4.

This is unmeasured. It is the next thing to look at, ahead of anything else in this file.

## Method notes

- `why_we_lost.py` reports **sells offered**, which are re-posted every turn and are not volumes.
  Do not quote that column. Use `private["shed"]` deltas against `market["prices"]`, which are fills.
- The scratchpad instruments used here are `melon_race.py` (per-product fills and revenue, both
  seats) and `melon_hold.py` (shed holdings vs standing tiles).
  Both take an episode path and a product name.
