# The top of the ladder is two shared scripts, and we are not playing either

Measured 2026-08-11 from the official episode datasets, `kaggle/kaggriculture-episodes-2026-08-09`
and `-08-10`: 1,372 episodes, 2,744 seats, 40 GB of replays.
Extracted by `scripts/episode_index.py` (parallel, one JSONL row per seat) into
`data/episodes_2026-08-09.jsonl` and `data/episodes_2026-08-10.jsonl`.

## Where we actually stand

| | rating |
|---|---|
| THUNDER THUNDER (#1) | 3,210.9 |
| Victor @ Tufa Labs (#2) | 3,149.8 |
| median episode in the dataset | ~3,079 |
| **our best submission ever** | **1,257.9** |
| our submission of 2026-08-11 | 845.1 |

**None of our games appear in the two-day sample at all** — 0 of 2,744 seats.
This is not a tuning gap. The field is at ~3,000 and we are at ~1,000, and the ladder starts at 600.

## The field is running two scripts

Median values per player, players with 5+ games in the sample:

| player | n | bank | WHEAT | STRAW | MELON | COW | SHEEP | GOOSE | buy wheat | sell wheat |
|---|---|---|---|---|---|---|---|---|---|---|
| Haramball forever! | 5 | 97,828 | 143 | 37 | 19 | 9 | 4 | 0 | 212 | 455 |
| Natalia Mawyin | 16 | 94,116 | 147 | 38 | 17 | 9 | 6 | 0 | 257 | 446 |
| Mohammed Nomaan | 23 | 94,006 | 147 | 38 | 17 | 9 | 6 | 0 | 257 | 446 |
| Dmitry Belan | 35 | 93,921 | 143 | 37 | 19 | 9 | 4 | 0 | 212 | 455 |
| Ueddy | 25 | 90,219 | 143 | 37 | 19 | 9 | 4 | 0 | 212 | 455 |
| THUNDER THUNDER | 111 | 90,112 | 144 | 36 | 19 | 9 | 5 | 0 | 245 | 430 |
| Efe Can Celiksoy | 53 | 87,378 | 146 | 37 | 19 | 10 | 4 | 0 | 234 | 459 |
| Changyuan Chen | 11 | 93,674 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 305 |
| Mohamed abdelrazik | 32 | 91,682 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 397 |
| CemBas | 13 | 89,846 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 305 |
| SHAURYA SHARMA | 32 | 89,262 | 108 | 42 | 24 | 8 | 6 | 0 | 267 | 302 |
| janson | 24 | 88,990 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 305 |
| tao wu11 | 10 | 88,462 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 305 |

Nine separate accounts report **WHEAT 108 / STRAW 42 / MELON 24 / COW 8 / SHEEP 6 / buy 266 / sell 305**
to the unit.
Seven more report **WHEAT ~144 / STRAW ~37 / MELON ~19 / COW 9 / SHEEP 4-6**.
That is not convergent evolution, it is two shared scripts.

## Timing

**Script A** (wheat ~144): 1 COW + 4 SHEEP on d0, the bulk of the cows on **d5-d8**, then a trickle
to d19. First PLANT at d0 turn 6. First SELL on d2, median sell day 21.

**Script B** (wheat 108): ~2 COW + 2 SHEEP on d0, cows on **d7-d10**, sheep on **d10-d11**.
First PLANT at d0 turn 8. First SELL on d0, median sell day 21.

## What separates us from all of them

- **Wheat.** They plant it 108-147 times a season; our schedule plants **24**. Wheat's book is
  starved in all 87 recorded tapes and closes at $40-59 against a $25 base, so it is the one product
  the market never saturates. They grow their own feed and sell the surplus; we buy 505 units.
- **Herd size and mix.** They run 13-16 head, cow-heavy (COW 8-10, SHEEP 4-6). Our schedule runs 21,
  and on the analysed loss `SHOP_ADAPT_HERD` bought **16 sheep and 5 cows**.
- **Geese.** Nobody in the top 16 owns a single goose.
- **Re-posting.** Measured by whether a SELL repeats the same `(item, qty)` on the next turn:
  the field is at **3-7%**. Ours re-posts its quota on all 24 turns of a day. We are the only agent
  in the sample that does this.

## Open-loop

Per-day action hashes, compared between games by the same player. One differing turn kills a whole
day, so this is a strict lower bound on similarity.

    Haramball forever!   24/30 days identical      Efe Can Celiksoy   18/30
    janson               21/30                     Mohamed abdelrazik 17/30
    Dmitry Belan         21/30                     SHAURYA SHARMA     11/30
    CemBas               21/30                     THUNDER THUNDER     7/30
    Mohammed Nomaan      19/30                     Ueddy               5/30

Most of the field is scripted. **THUNDER THUNDER, the #1, is the most reactive of the lot** — and on
a separate turn-by-turn diff, two of its same-seat games were only 1.2% identical, diverging at
d0h3. Victor @ Tufa Labs is the opposite extreme: 97-99% of turns identical across seven games on
both seats, with byte-identical season SELL totals.

So the top two are a reactive agent and a fixed script, at 3,210 and 3,149. Both work.

## Does the field adapt to the board? Mostly no — and the one that does, leads

Range across each player's own games. Every game is a distinct shop draw.

| player | n | COW | SHEEP | WHEAT | distinct draws |
|---|---|---|---|---|---|
| Dmitry Belan | 35 | 9..9 | 4..4 | 142..143 | 35/35 |
| Mohamed abdelrazik | 32 | 8..8 | 6..6 | 108..108 | 32/32 |
| janson | 24 | 8..8 | 6..6 | 108..108 | 24/24 |
| **THUNDER THUNDER** | 111 | **6..11** | **4..12** | **132..152** | 108/111 |
| Ueddy | 25 | 6..10 | 4..11 | 142..150 | 25/25 |
| Raiden.B | 27 | 1..15 | 5..19 | 55..120 | 27/27 |

Mohamed abdelrazik played 32 games on 32 different boards and bought exactly 8 cows and 6 sheep and
planted exactly 108 wheat in every one.
The fixed scripts sit at ~3,100; THUNDER, which floats cow/sheep, is #1 at 3,210.

**So adaptive herd is real and worth roughly 110 rating points. The gap from us to a fixed script is
2,255.** Do the base plan first.

## Why our schedule is the wrong target: Seb was optimal under the OLD economy

`townCenterSellInterval` went 12 -> 24 on 2026-08-08, cutting the town's drain ~8x.
Seb's 16 recorded games, split by the economy they were played under:

| | games | median bank | COW | SHEEP | WHEAT | STRAW | MELON |
|---|---|---|---|---|---|---|---|
| interval 12 (old) | 5 | **$137,747** | 5..9 | 10..15 | 19..28 | 41..45 | 18..24 |
| interval 24 (now) | 11 | **$77,737** | 5..13 | 5..20 | 20..36 | 38..43 | 14..25 |

His bank halved while he kept the same low-wheat shape, and he has since withdrawn from the ladder.
The field's answer to the new economy is the thing he does not do: plant 108-147 wheat.

**`data/seed_scripts/top_guys/90976060/schedule.json` — the plan this repo matches op-for-op — is
his interval-12 shape, asking for WHEAT 24 / STRAWBERRY 41 / MELON 17.**
That is the 845-vs-3,100 gap. It is not the planner, the watering or the market logic; it is the
target. Note also that Seb floats COW 5..13 and SHEEP 5..20 — he adapts more than the current field.

## Best tape to rebase on

**Dmitry Belan** (35 games, `COW 9..9 SHEEP 4..4 WHEAT 142..143 STRAW 36..37`) — near-zero variance
makes it a pure script, so the plan reads noise-free.
**Efe Can Celiksoy** (53 games, WHEAT 143..146) is an equally clean second source for cross-checking.
Not THUNDER: it is reactive (7/30 days identical; 1.2% on one same-seat pair), so there is no fixed
plan to extract — it is a sparring opponent and the evidence that adaptive cow/sheep pays.

## What was tried on the crop dynamic, and why all of it is off

`SHOP_ADAPT_CROPS` in `kagg/search/schedule_agent.py` carries the full record. Summary:

- **`WHEAT<->CARROT` and `TOMATO<->STRAWBERRY`** — shipped, measured 0.806 vs HEAD's 0.871 over 232
  matched games. They swap toward crops the ladder plants 0.2% and 0.0% of the time.
- **`STRAWBERRY<->MELON`** — produces an identical 54/4 split on every board tested. No shop carries
  melon, so its drain is 29 everywhere; a pair with one board-independent member cannot adapt.
- The shared cause: **the headroom model treats the town's drain as a cliff when the price curve is
  a slope.** A melon past its drain still fetches $229 at +50 and $166 at +100. Any rule scoring on
  "units the town will eat" under-plants every steep-curve, low-drain product. The fix is to price
  the marginal unit off `market_price`, and it is unbuilt.

## 2026-08-11 — What the ladder losses actually say

Folded in from docs/ladder_losses_2026-08-11.md.

Ten downloaded ladder episodes, `weedSpawnChance = 0.005`, `kaggle_environments 1.32.6`.
Every number here is read off the recordings; nothing is simulated, so nothing can be an artifact of
our own harness.

> **THIS IS A SAMPLE OF LOSSES, NOT A RECORD.** Alex downloads the games we lose; the one win in the
> table is incidental. So "1W 9L" says nothing about the win rate, and **any conclusion drawn by
> comparing us to the opponent is conditioned on our having lost** -- of course those games are
> close-but-behind on money. The "we out-earn them and spend the difference" finding at the bottom
> of this section carries that bias and must be re-measured on an unbiased sample before it is acted
> on.
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

### The finding that survived every challenge: no shop drains MELON

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

### The consequence: the second melon wave is planted into a market we personally destroyed

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

#### That swap is WRONG, and the reason is the whole point about melon

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

### We play the identical season on every seed

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

### What is NOT the problem

- **Late-season watering.** Weeds from a missed watering, us vs them across the ten:
  `47/23, 39/57, 47/30, 39/17, 34/29, 19/33, 33/33, 43/30, 34/0, 32/20`.
  We are worse in five and better in four, and lost regardless.
  A whole session went into tour execution against the tape while the losses were decided elsewhere.
- **WOOL.** Wool is drained 0 in six of the ten (only `YARN_STORE` carries it) and we keep sheep
  regardless — but in 92077611 the opponent ran **6 sheep to our 4** into a zero-drain wool book and
  still won. It cannot be the differentiator.
- **Crop revenue, in the close games.** On 92077611 realized fills were **ours $135,999 vs theirs
  $132,961** — we out-sold him by $3,038 and lost by $1,386.

### The open lead: spending, not earning

Money is `3000 + revenue - spend`. On 92077611 that gives **us $21,585 spent against their $17,161**
— $4,424 more, on a game we lost by $1,386.
Their closing-week buy counts run 15–67 a day against our fixed 4.

This is unmeasured. It is the next thing to look at, ahead of anything else in this section.
As of 2026-08-15 (see below) it is still open: the closest measurement is the last-day
value-conversion finding, which is related but not the same claim.

### Method notes

- `why_we_lost.py` reports **sells offered**, which are re-posted every turn and are not volumes.
  Do not quote that column. Use `private["shed"]` deltas against `market["prices"]`, which are fills.
- The scratchpad instruments used here are `melon_race.py` (per-product fills and revenue, both
  seats) and `melon_hold.py` (shed holdings vs standing tiles).
  Both take an episode path and a product name.

## 2026-08-13 — The losses are narrow (not a win rate)

Folded in from docs/the_ladder_is_lost_by_a_nose_2026-08-13.md.

> **CORRECTION, same day, from Alex: "our win rate is nothing like what you say -- i only download
> the losses".** The 60 games in `data/seed_scripts/ours_ladder/` were downloaded BECAUSE they were
> losses. Every win-rate number that was in this section originally -- "5-54", "win rate 0.085", and
> the whole "+$6,000 takes us to 0.475" table -- was computed on a sample conditioned on the thing
> being measured, and is worthless. They were removed from the source file rather than annotated, so
> nobody re-derives them, and they stay removed here too.
>
> This is the `farm:0.445` lesson in CLAUDE.md a second time: a number correct per row and
> meaningless in aggregate, because of what defines the rows.
>
> **What survives the correction** is the only thing the sample can legitimately show: *given that
> we lost, by how much did we lose.* That is unbiased within the set of losses, and it is the useful
> part.
>
> Per the project's known selection bias (Alex downloads losses to study, not a random sample): any
> win rate computed from these downloaded games is invalid and must not be re-derived or implied
> elsewhere in this document either.

Measured on **60 downloaded ladder games** of our own agent (`data/seed_scripts/ours_ladder/`),
2026-08-13. **These were downloaded because they were losses.** Nothing here is a win rate and
nothing here supports one.

### How big are the losses, given that we lost

    54 losses          median  -$8,900        mean  -$11,600
    inside  $600        6
    inside $2,100      11
    inside $6,000      23
    inside $10,000     31

Two are inside $150 -- `-$70` against TrebolNoir_ and `-$135` against Mirza Yasir Abdullah Baig.
Twenty-three of the 54 are inside $6,000.

**What that does and does not license.** It says that when we lose, we frequently lose by an amount
a single good day would cover. It says nothing about how often we lose, and any claim of the form
"+$X a game buys Y% win rate" needs an unbiased sample -- a full ladder pull, or an arena run over a
fixed seed set. That measurement has not been made.

It remains true, independently of this sample, that the ladder is an Elo rating and a $70 loss
costs what a $39,200 loss costs (`CLAUDE.md`). So a change worth $2,000 is not a rounding error
against a $71k season. The sample cannot tell us how many games that flips.

### The five wins in the set are not evidence either

The set does contain five wins -- by $13.9k, $13.5k, $78.4k, $91.0k and $65.2k -- but they are
whatever happened to be downloaded alongside, not a sample of our wins. The only thing worth noting
is that they are all large, which is consistent with "win big, lose small" but does not establish
it.

### What is NOT the cause

Checked and closed the same day, so they are not re-derived:

- **Stranded stock.** The final shed on seed 11 is completely empty -- 0 units of all nine products,
  $0 of value. `LIQUIDATE_LAST_DAY` does its job. There is no unsold inventory to recover.
- **A single catastrophic matchup.** The losses are spread across 54 distinct opponents with no
  repeat structure; the worst is -$39,200 and the median is about -$8,900.

### The timeout is separate and unquantified

`91304798` is a self-play validation episode on seed 0 that ended `TIMEOUT/TIMEOUT` at step 531 of
720. One game out of 60, and it is our own agent on both seats, so it does not sit in the ladder
sample above. It is recorded here because a timeout is a loss no dollar figure can show, the env
allows 1s/turn, and nothing in this project currently measures our per-turn latency.

## 2026-08-15 — Three ladder games: one win, two losses

Folded in from docs/three_ladder_games_2026-08-15.md.

Read off the downloaded replays only.
No simulation for the market numbers, so none of them can be an artifact of our own harness.
The solver-seating section IS a local replay and says so.

    93237183   WIN    us $117,976  vs Farfadet        seat 0   seed 1158229392
    93239838   LOSS   us  $87,726  vs mashBrian254    seat 1   seed  702042888
    93242536   LOSS   us $111,741  vs Alexandre008    seat 1   seed  195279982

All three: `weedSpawnChance 0.005`, `townCenterSellInterval 24`.

Downloaded games are SELECTED — Alex downloads losses — so nothing here is a win rate.

### 1. Did the solver get used?

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

### 2. Did the melon sell properly on d10?

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

### 3. What actually lost these games

The shop draw decides which products the town absorbs, and we produce the same mix regardless.

#### 93239838 — the town wanted eggs and strawberry; we made milk and wool

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

#### 93242536 — a different draw, same failure on the other product

    SHOPS  FARMERS_MARKET x1, ICE_CREAM_SHOP x2, PET_CAFE x2, SMOOTHIE_SHOP x1, YARN_STORE x2

      CARROT        895   $ 77 of $35   starved, we planted 63
      STRAWBERRY    716   $139 of $120
      WOOL          716   $236 of $200  fine here — YARN_STORE drawn twice
      MILK          537   $  1 of $160  FLOORED anyway
      WHEAT         537   $ 43 of $ 25

Here wool paid and carrot was the miss: 895 units of season demand at $77 a unit, and we planted 63.

### 3b. A cow starves on day 11, and we pay $400 to replace it

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

**Follow-up, same day (see the 2026-08-15 "Two more losses" section below): the FEED fix was shipped
and confirmed holding — zero starvations across two further downloaded games, on both seats.**

### 4. What this points at

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

## 2026-08-15 — Two more losses: 93286476 and 93285579

Folded in from docs/two_losses_2026-08-15b.md.

Read off the recordings only. No simulation, so nothing here is a harness artifact.
Volumes are **fills** (shed decreases), never offers.

    93286476   LOSS   us $78,254  vs  Light      $79,216    -$962      seat 0
    93285579   LOSS   us $56,805  vs  Mutte1904  $63,697  -$6,892      seat 1

They are two different losses and must not be pooled.
Downloaded games are SELECTED (Alex downloads losses) — nothing here is a win rate either.

### 1. Animals: the feed fix holds

Tracked every animal tile, every turn, both seats, both games.

    93286476   US  animals lost mid-season: 0      THEM: 1  (SHEEP, d29 h00)
    93285579   US  animals lost mid-season: 0      THEM: 1  (SHEEP, d29 h00)

Zero starvations on our side in either game.
The d9/d10 stranded-FEED defect (see the 93239838 cow, above) is closed in live play, not just on
the grid.

### 2. Sheep: the problem is confirmed again, and it decided neither game

WOOL closed at **$1.00, the floor**, in both games, with **zero** yarn drain — no YARN_STORE
unlocked on either board.
We ran 4 sheep anyway.

The price trace shows how fast our own supply broke it:

    day     inventory    WOOL price
    d6         9,994          $217
    d9        10,009          $195
    d12       10,021          $174
    d15       10,058            $5
    d18       10,059            $1
    d21..d29  10,059            $1

Sixty-five units of net supply took wool from $217 to $1 inside nine days, and it never recovered
because nothing was draining it.

**But it is not why we lost these two.** They ran *five* sheep to our four, into the same dead book.
Both seats ate the same mistake and they ate more of it.
So `SHOP_ADAPT_HERD` is still the right fix — 4 sheep is $2,000 of purchase plus a season of FEED
and CARE ops for a product worth $1 — it is just not the differentiator in this pair.

### 3. Melon: we sell it faster than they do, we simply have less of it

The opposite of the natural guess. Fills per day, with the price at that moment:

    93286476                                   93285579
    day  us  them   melon inv   price          day  us  them   melon inv   price
    d11  18    18      10,090    $169          d11   6    18      10,072    $198
    d12  12     0      10,107    $136          d12   6     0      10,083    $181
    d15   0     6      10,116    $115          d15   0     6      10,092    $165
    d21   0     2      10,116    $115          d21   0     2      10,092    $165
    d23   0     6      10,126     $91          d23   0     6      10,102    $146
    d24   0     6      10,131     $78          d24   0     6      10,107    $136
    d26   0     6      10,147     $34          d26   0     6      10,123     $99
    d27   0     6      10,152     $19          d27   0     6      10,128     $86
    d28   0    12      10,158      $1          d29   0    12      10,138     $60
    season  us 30   them 62                    season  us 12   them 62

We clear our whole melon stock on d11-d12 at the two best prices of the season and then sell none
for seventeen days.
They dribble theirs out to the last day at prices falling to $1.
Our *timing* is better.

The gap is production: **12 melon fills against 62** in 93285579.
At the prices they realised that is roughly $3,700 — over half the $6,892 loss.

*This is a different claim from the same-day "three ladder games" section above, which found a real
but smaller ($1,900) intraday melon delivery/timing defect (hands vs shed) in a different pair of
games. Both stand: the delivery defect is real but was not decisive there; in this pair, total melon
output (not delivery timing) is the binding constraint. Not a contradiction — different games,
different bottleneck.*

### 4. 93285579: TOMATO closed at eleven times base and neither seat grew it

    TOMATO   closed $660   base $60   drained 895 units
    shops    FARMERS_MARKET x3, PIZZA_SHOP x2, BAKERY x2, ICE_CREAM_SHOP x1

`MARKET_PARAMS["TOMATO"]` uses the `hinge` below-curve added in 1.32.7, and it is explosive:

    inventory    price
       10,000      $60
        9,800      $84
        9,600     $300
        9,400     $900
        9,200   $1,884
        9,000   $3,252

TOMATO is `ongoing`, `first_yield_day 8`, `interval 1`, `max_yield 4`, seed $50 — planted d12 it
fruits from d20 and yields daily to the end.
This is the conditional Fable recommended (2+ tomato-stocking instances visible by d12, ~26% of
draws) and the payoff on this board was far above what base-price arithmetic suggests.

Caveat: the curve is this steep in both directions. Supplying it also collapses it fast, so the
sizing matters and is not established here.

### 5. 93286476: we led on bank AND field at d28, and lost anyway

Bank plus standing produce plus shed, both seats, priced at the live market. Same method both
sides, so the comparison holds even though it overstates the level.

    93286476        our bank  our field | their bank their field |  our TOTAL their TOTAL   edge
    d24               44,408     17,579 |     43,095     19,840 |     61,987      62,935    -948
    d26               58,963     14,220 |     57,700     12,975 |     73,183      70,675  +2,508
    d28               69,106     11,756 |     66,567      8,984 |     80,862      75,551  +5,311
    d29 dawn          73,879      6,724 |     69,771      8,201 |     80,603      77,972  +2,631
    final                                                                          -962

    93281072        our bank  our field | their bank their field |  our TOTAL their TOTAL   edge
    d26               70,147     18,366 |     68,899     12,649 |     88,513      81,548  +6,965
    d28               83,485     13,242 |     81,038     11,186 |     96,727      92,224  +4,503
    d29 dawn          89,821      7,829 |     85,138     11,640 |     97,650      96,778    +872
    final                                                                        -1,562

(The second table's game ID, `93281072`, is as recorded in the source file — distinct from the two
games named in this section's header. Kept verbatim rather than silently corrected.)

Two games, same shape: a $4-7k lead in total value at d28 decaying to roughly nothing by d29 dawn
and turning negative at the close.
**We convert standing value into cash worse than they do over the last two days.**

It is not a d29 routing miss. Both boards finish clean:

    93286476   ripe units left standing at the final step:  US 2 WHEAT   THEM 2 WHEAT
    93285579                                                US 4 WHEAT   THEM 2 WHEAT

The d29 op counts say the same thing — they had more to take, not that we failed to take ours:

    93286476   d29   US HARVEST 25   THEM HARVEST 38
    93285579   d29   US HARVEST 26   THEM HARVEST 38

And leftover unsold stock is negligible on our side (6 WHEAT + 2 FERTILIZER in 93286476).

93285579 does **not** have this shape — we were behind on total value from d24 (-$6,889) and never
led. That one is the melon and tomato game.

### 6. Killed here: "we dump in one hour and they spread the sale"

We post SELL orders in far fewer hours than they do — 68 hours across the season against 319, and
in the back half it is ~2/day against ~15/day.
That looked like a price-impact leak. **It is worth $64.**

`_process_market` quotes per unit at the live inventory, so the walk down the curve is identical
whether the units are posted in one hour or twelve; the only recovery between hours is the town's
drain, and at our volumes that is negligible. Priced on our real d29 order in 93286476:

    item          qty     inv    one hour   spread 12h      gain
    WHEAT          35   9,241       1,823        1,826        +3
    MILK            9  10,073          21           63       +42
    STRAWBERRY      8   9,860       1,745        1,764       +19
    CARROT          9   9,779         468          468        +0
    WOOL            4  10,059           4            4        +0
    FERTILIZER     14  10,409         237          237        +0

Null. Do not re-derive it.

### What this changes

1. The last-day conversion item stays open and is now **two** games with the total-value table
   behind it, not one game with a bank number.
2. `SHOP_ADAPT_HERD` stays the next fix, unchanged, but these two games are not its evidence.
3. Tomato moves up: a board drained 895 units of a product on the hinge curve and nobody supplied it.
4. Melon output, not melon timing.
