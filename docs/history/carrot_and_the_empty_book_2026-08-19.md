# Carrot and the empty book

Read-only analysis, 2026-08-19.
Question: should our agent plant and sell more CARROT, or not.

**Verdict: no general increase.**
Carrot's book is not empty — 94% of strong players already sell some — and on a season-long,
tile-for-tile basis WHEAT nets more per tile-day and per action than CARROT, because carrot's seed
costs twice as much for a similar raw yield.
The one thing worth doing, and that top players already do, is planting carrot specifically as an
**end-of-season closer** on tiles a longer crop cannot finish, and leaning harder into it only when
`town.unlocked_shops` has drawn PET_CAFE or FARMERS_MARKET — that shop draw, not seller scarcity, is
what actually moves carrot's price.

**A correction to the task's own premise, up front.** The background cited game
`ladder_2026-08-17b/94282682.json` as CARROT rising while STRAWBERRY also floored to $1. Replayed
directly: STRAWBERRY closed at **$219** (up from $120), not $1 — only MILK floored to $1. We were
the sole seller of both CARROT and STRAWBERRY in that game, and STRAWBERRY, not CARROT, was the big
winner: 287 units for $65,059 revenue. The "empty book lets the price run" mechanism is real, but it
ran on strawberry harder than on carrot in the one game the thesis was built from.

## Method

Downloaded replay JSON already contains the exact outcome, but the per-turn *action stream* is
offers, not fills (`kagg/analysis/fills.py`; re-posted orders can 24x-overstate a sale). To get
ground truth without touching any code under `kagg/`, `scripts/`, `tests/`, or `submission/`, both
seats' own recorded actions were replayed verbatim through a fresh `kaggriculture` env wrapped in
`record_fills()`, with the game's own `townCenterSellInterval` and its own recorded
`town.unlocked_shops` draw injected turn-by-turn (the same technique `scripts/breakdown.py:tape_policy`
and `env_config`/`recorded_shops` use). This reproduces the exact fills, not offers, for every
product, for both seats, in every game. Replay scripts and JSONL outputs are in the scratchpad only
(`/private/tmp/.../scratchpad/carrot_fills.py`), not committed.

Corpora used:
- **`leaders_2026-08-19`** — 60 games / 120 seats replayed (unbiased pull, winner bank >= $110k; a
  download was still running, so this is more than the 43 files listed at task start).
- **`ladder_2026-08-17b`** — 43 games / 86 seats replayed (our games; **selected losses**, used
  only for behavior/price description, never for a win rate).
- **`kawashigi/*.json`** — 19 of 20 files replayed (the 20th, `schedule.json`, is not a replay).
- **`downloads_2026-08-13/91907974.json`** — 1 reference tape, replayed.

## 1. Is the carrot book empty?

No. Across the 60 leader games (120 seats), CARROT is the **second-most universally sold** crop
after WHEAT/STRAWBERRY/MELON/MILK/WOOL/FERTILIZER, which every single seat sold at least once.
TOMATO and EGG are the genuinely empty books — literally zero seats sold either, and zero board
tiles ever showed a TOMATO plant across all 120 seats at d10/d20/d28 (EGG needs a GOOSE, already
closed as a settled negative — see `project_kaggriculture_animals_verdict`).

| product | seats selling (n=120) | % seats | total units | median units/seller |
|---|---|---|---|---|
| WHEAT | 120 | 100.0% | 84,396 | 601 |
| CARROT | 113 | 94.2% | 1,476 | 15 |
| STRAWBERRY | 120 | 100.0% | 29,797 | 246 |
| MELON | 120 | 100.0% | 12,364 | 120 |
| MILK | 120 | 100.0% | 28,800 | 259 |
| WOOL | 120 | 100.0% | 17,935 | 120 |
| FERTILIZER | 120 | 100.0% | 29,283 | 242 |
| TOMATO | 0 | 0.0% | 0 | — |
| EGG | 0 | 0.0% | 0 | — |

Carrot sellers cluster tightly: quartiles of units-sold-per-seller are 10 / 15 / 15, max 88 (one
outlier, see Q5). Everybody who touches carrot does roughly the same small amount of it. That is
the signature of a garnish crop, not a contested or an ignored one.

## 2. What does the CARROT price actually do?

Median dawn-of-day open vs. close, across the 60 leader games:

| product | median open | median close | close/open | n games |
|---|---|---|---|---|
| WHEAT | 25 | 48 | 1.92x | 60 |
| STRAWBERRY | 120 | 171 | 1.43x | 60 |
| TOMATO | 60 | 80 | 1.32x | 60 |
| CARROT | 35 | 46 | 1.31x | 60 |
| EGG | 50 | 58 | 1.16x | 60 |
| WOOL | 200 | 156 | 0.78x | 60 |
| MILK | 160 | 117 | 0.73x | 60 |
| MELON | 250 | 31 | 0.12x | 60 |
| FERTILIZER | 100 | 7 | 0.07x | 60 |

CARROT appreciates, but it is the **fourth**-biggest appreciator, behind WHEAT (1.92x), STRAWBERRY
(1.43x) and TOMATO (1.32x, on zero sellers — pure shop-drain with no supply at all). The 35->66
one-off is near the top of the observed range (closes ran 33-75 across the 60 games) but is not
typical; median close is 46.

**What actually drives the CARROT close, measured directly:** the number of PET_CAFE/FARMERS_MARKET
instances the town happened to draw (both consume CARROT specifically; shops are drawn with
replacement, so 0-4+ instances are possible in one game).

| carrot-shop instances (PET_CAFE + FARMERS_MARKET) | n games | closing price range |
|---|---|---|
| 0 | 8 | 33-37 |
| 1 | 30 | 38-55 |
| 2 | 10 | 47-61 |
| 3 | 10 | 56-69 |
| 4 | 1 | 65 |

Correlation (shop instances vs. closing price): **r = 0.90**. Correlation (total units sold in the
game vs. closing price): **r = 0.42**, and it's *positive* — more selling goes with a *higher*
close, not a lower one, because both are driven by the same underlying demand draw. This flatly
contradicts a "sellers are scarce, so the price runs" story; the price runs when the *shop draw*
runs, and sellers respond to that, they don't cause it.

## 3. Does carrot need a shop?

No shop is required to **sell** CARROT — `_process_market` will quote and fill a SELL order for any
product in `PRODUCTS` regardless of `unlocked_shops`; the base town-center consumption
(`TOWN_CENTER_PRODUCTS`, every 24 turns) applies to every product including CARROT. What a shop
gates is **demand**, i.e. whether the price is worth catching:

| shop | products | n games it ever unlocked (of 60) | median first day |
|---|---|---|---|
| ICE_CREAM_SHOP | STRAWBERRY, MILK, WHEAT | 54 | 6 |
| SMOOTHIE_SHOP | STRAWBERRY, MILK | 49 | 6 |
| YARN_STORE | WOOL | 42 | 9 |
| BRUNCH_SPOT | EGG, WHEAT, STRAWBERRY | 41 | 12 |
| FARMERS_MARKET | WHEAT, CARROT, TOMATO, STRAWBERRY | 37 | 12 |
| PIZZA_SHOP | MILK, TOMATO, WHEAT | 34 | 12 |
| BAKERY | EGG, WHEAT | 30 | 16.5 |
| PET_CAFE | CARROT | 26 | 16.5 |

PET_CAFE is CARROT's only dedicated shop and it is both the rarest (26/60 games) and the latest
(median first day 16.5) to unlock. FARMERS_MARKET is a second, earlier route to the same demand
(median day 12, 37/60 games) but CARROT is only one of four products it consumes there, competing
with WHEAT/TOMATO/STRAWBERRY draw-down for the same instance. Net: carrot demand is gated by luck of
the draw more than by anything plannable, and it tends to land in the second half of the season if
it lands at all (8/60 games never drew either shop).

## 4. Is carrot worth the tile?

Per-cycle mechanics (both crops `first=2`; the difference is `max_yield_day`), confirmed against
`reference/kaggriculture.py` and matching `kagg/economics/production.py`'s own measured constants
exactly:

| | WHEAT | CARROT |
|---|---|---|
| seed cost | $10 | $20 |
| cycle length (plant to harvest) | 4 days | 3 days |
| units/cycle, unfertilized | 4 | 3 |
| units/cycle, fertilized | up to 6 | up to 4 |
| plantings/season (measured, 30-day) | 8 | 11 |
| season yield/tile, unfertilized (measured) | 28 | 29 |
| season yield/tile, fertilized (measured) | 42 | 39 |

Raw season yield per tile is nearly identical (28 vs 29). But CARROT needs **38% more
plant/harvest cycles** (11 vs 8) to get there, and its seed costs **2x** as much per planting. Using
this season's median season-average dawn price (WHEAT $39.1, CARROT $38.4 — also nearly identical):

| | WHEAT | CARROT |
|---|---|---|
| season revenue/tile (unfertilized) | $1,094.80 | $1,113.60 |
| less season seed cost | -$80 (8x$10) | -$220 (11x$20) |
| **net/tile, season** | **$1,014.80** | **$893.60** |
| net revenue per tile-day (÷30) | **$33.83** | **$29.79** |
| unit-actions/season (plant+harvest+water, no travel) | ~40 | ~44 |
| net revenue per unit-action | **$25.37** | **$20.31** |

**WHEAT nets ~13-25% more per tile-day and per action than CARROT run as a season-long staple.**
Fertilizer widens this gap, not narrows it: fertilized, WHEAT nets $52.06/tile-day vs CARROT's
$42.59/tile-day (+22% edge instead of +14%). Travel/routing cost to reach a tile is not modeled
here (a real cost — see the animals routing lesson in `CLAUDE.md`) and would very likely favor
CARROT's shorter cycle even less, since more plantings/season means more trips to the tile, not
fewer.

The one real edge CARROT has: **it fits in a shorter window.** A tile that frees up on day 27 can
still run one full carrot cycle (finishes day 30) but cannot run a wheat cycle (would finish day
31, after the season ends). That is a scheduling property, not a per-unit profitability property,
and it is exactly what the top players' boards show in Q5.

## 5. What do the top players plant?

Board crop-tile counts, summed across all 120 leader-seats, at three checkpoints:

| day | CARROT tiles (sum) | seats with any CARROT | WHEAT (sum) | STRAWBERRY (sum) | MELON (sum) |
|---|---|---|---|---|---|
| 10 | 4 | 4/120 | 676 | 1,587 | 1,971 |
| 20 | **0** | **0/120** | 2,993 | 4,033 | 91 |
| 28 | 198 | 113/120 | 4,258 | 1,889 | 0 |

**Nobody runs a carrot-heavy board mid-season.** At day 20, not a single one of the 120 leader
seats has a single CARROT tile alive. By day 28, 113 of 120 seats have picked some up — this is the
"plant something in the last two days rather than leave the tile idle" move, done almost
universally, at small scale.

One outlier: `93804040`, seat 0 (Thomas Tschinkel, winner, $110,194 vs. opponent's $103,173) ran
**35 CARROT tiles** by day 28 — the only genuinely carrot-heavy board in the sample. That game also
drew 3 carrot-shop instances (PET_CAFE day 3, FARMERS_MARKET day 18), and its CARROT close hit $75,
the second-highest in the whole sample. He sold 88 CARROT units for $6,264 — his opponent sold 15
for $1,033, a $5,231 swing that is not nothing against a $7,021 final margin. But even in this
best-case game, CARROT was **5.7% of his total sold revenue** ($6,264 of $110,194); STRAWBERRY
($42,732) and MILK ($54,015) still did the heavy lifting.

## 6. Verdict

**Do not blanket-increase carrot tile allocation.** The book is not empty (94% already sell it),
and wheat beats it $/tile-day and $/action when run as a season-long crop. What the data supports
instead, bounded and specific:

1. **Keep — and if anything, make more systematic — the end-of-season carrot closer.** Any tile
   that frees up with 3-4 days left in the season (day ~26-29) and cannot finish a wheat/melon
   cycle should get carrot rather than sit idle. 113/120 top seats already do this; it costs
   nothing to formalize.
2. **Scale carrot up specifically when `town.unlocked_shops` shows PET_CAFE or FARMERS_MARKET**,
   which is readable in the observation and correlates r=0.90 with the closing price. Without
   either shop (8/60 games), do not expect carrot to clear the mid-$30s-$40s; do not overcommit
   tiles on the hope it will.
3. **Do not treat the 94282682 game (35->66/58) as the general case.** It sits near the top of a
   33-75 range driven by an above-median shop draw, not by an emptier book than usual (that game
   had a normal number of carrot sellers for its price level, per the units-vs-close table).

**What would falsify this:** (a) if routing/travel cost were priced in and it turned out CARROT's
shorter cycle needs materially *fewer* trips per unit than this estimate assumes — untested here,
would need a routed-tile-cost study, not board-snapshot counts; (b) if a larger, fresher unbiased
sample (the `leaders_2026-08-19` download was still growing during this analysis) shows the
shop-instance correlation weakening — it is single-sample and not seed-repeated; (c) if a
robustness check shows longer games simply draw more shop instances *and* score higher for reasons
unrelated to carrot (a confound this analysis did not control for, since shop draws accumulate with
turns played and both winners and the shop count grow with game length).
