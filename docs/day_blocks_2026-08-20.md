# Day blocks: the season is a decision tree with a shallow root

Written 2026-08-20, on branch `day-blocks`.
`bundle-head` still holds the per-turn BC work, untouched.

Alex's framing, which turned out to be right in almost every particular:

> i was expecting it to learn big block sequences and maybe 6 different ones over the whole 30 days
> depending on the shops

> based on shop draw and opponent melon amount at d3 -> per day board

> up to d12 the only criteria is melon and shops

## The headline

**A depth-4 decision tree picks a strong player's exact day-block on a game it has never seen,
83.6% of the time at d6 and 58.2% at d12 — and nothing at all from d17.**

The unit of decision is the DAY, not the turn.
That is the single most important finding, because the BC student we spent the day training is
per-turn and cannot express a day plan at all.

## Why the per-turn student scatters

`submission/main.py:13580` builds `_AGENTS[me]` once at d0 h0 and reuses that closure for all 720
turns; its own docstring says the per-day state must stay warm.
The route is planned once at h0 and executed for 24 hours.

So the teacher's action at h13 is a function of a plan made at h0.
The student sees only the board at h13, with `GLOBAL_FEATURES = 60` containing no plan and no
history.
Two different tours can leave an identical board at h13 and need different next moves.

**That is an observability gap, not a tuning gap, and DAgger cannot fix it.**
DAgger corrects distribution mismatch by labelling states the student reaches.
It cannot supply state the student cannot see.

Measured consequence, `bc_bundle.best.pkl` in the real environment, 4 games:

    W/D/L 0/0/4    student bank mean $438    teacher $141,812
    turns with orders 5.8% (teacher 21.1%)   PASS 83.7%
    legality: 0 slot-order errors, 0 bad quantities, 0 malformed

Held-out per-decision agreement was good — 0.888 bundle agreement on trading turns, up from 0.000
untrained. It learned the mapping and not the trajectory.

## How big is a day library?

カワシギ, 228 seasons, animal ops stripped from the label:

| day | distinct blocks | top share | blocks to cover 90% |
|---|---|---|---|
| 0 | 2 | 84.2% | 2 |
| 1-2 | 1 | 100.0% | 1 |
| 3 | 9 | 46.9% | 3 |
| 5 | 13 | 37.7% | 6 |
| 7 | 35 | 23.7% | 16 |
| 10 | 46 | 16.2% | 25 |
| 12 | 47 | 19.7% | 26 |
| 15 | 97 | 8.8% | 75 |
| 18 | 182 | 3.9% | 160 |
| 21 | 204 | 0.9% | 182 |
| 29 | 212 | 0.9% | 190 |

d0-d2 is one block. By d21, 204 distinct blocks across 228 games — every game unique.

## Can it be predicted? Held-out games, depth-4 tree

150 train game-seats, 63 held out. Split by GAME, never by row.

| day | classes | baseline | tree | gain |
|---|---|---|---|---|
| 3 | 8 | 56.7% | 83.6% | +26.9% |
| 5 | 12 | 44.8% | 77.6% | +32.8% |
| 6 | 22 | 26.9% | 83.6% | +56.7% |
| 7 | 30 | 29.9% | 65.7% | +35.8% |
| 9 | 34 | 25.4% | 73.1% | +47.8% |
| 12 | 43 | 22.4% | 58.2% | +35.8% |
| 15 | 78 | 7.5% | 29.9% | +22.4% |
| 17 | 123 | 4.5% | 6.0% | +1.5% |
| 18+ | 131+ | 3.0% | 3.0% | +0.0% |

**The cliff is d17.** From d3 to d16 the tree beats a constant by +12% to +57% every day.

## The criteria, at d5

The root split, chosen from 64 candidate features:

    |--- opp_crop_MELON <= 8.00
    |   |--- mkt_inv_WHEAT <= 9951.00
    |   |   |--- opp_money <= 547.00 ...
    |--- opp_crop_MELON >  8.00
    |   |--- opp_money <= 272.50
    |   |   |--- shop_plant_slots <= 3.00 ...

Opponent melon acreage, at 8 tiles.
Then market wheat inventory, opponent money, shop plant slots, our carrot seed, their cow and sheep
counts.

Opponent state dominates, which fits the mechanics: the market is shared, and **no shop buys
MELON** — it is absent from every entry of `SHOPS`, so melon revenue is base-market only and priced
by the opponent's acreage. A d3 melon commitment (80 a seed, first yield d10-12) is the largest
irreversible bet in the game.

## Shops: identity is useless, the abstraction is not

8 shops, drawn WITH replacement every 3 days, `MAX_SHOP_INSTANCES = 8`.

| draws | shop multisets | (animal, plant) classes | WHICH ANIMAL |
|---|---|---|---|
| 1 | 8 | 5 | 4 |
| 5 | 792 | 71 | 8 |
| 8 | 6,435 | 173 | 8 |

Alex's "plant friendly or animal friendly" collapses 6,435 configurations into **8 animal classes**,
saturating by the third draw. Each animal product has exactly one source:

    EGG  <- BAKERY, BRUNCH_SPOT                        -> GOOSE
    MILK <- PIZZA_SHOP, ICE_CREAM_SHOP, SMOOTHIE_SHOP  -> COW
    WOOL <- YARN_STORE                                 -> SHEEP

## Measured nulls, recorded so they are not re-derived

- **Stripping animal ops changes almost nothing.** Kawashigi d8 3.2 -> 3.2 blocks per group,
  tetsuya identical at every day, only ReCurSiON's d16/d18 reach 1.0. Generating the herd by rule
  still shrinks the library; it is not what makes a day matchable. The variation is in plant and
  route work.
- **More tape sources do not make a smaller library.** Across 76 distinct players there are 52
  different day-0 blocks and the most common covers 11.8%. One strong player is one block per day;
  the field is 52 alternatives. `main.py:4887`'s "all four tapes agree op-for-op until d4 h01" is
  true of those four and not of the field.
- **There is no seat advantage in selling.** `_process_market` settles SELL/BUY in per-unit
  lockstep and says so: "Both players see the same pre-commit inventory for this unit." Only HIRE
  and BUY_LAND are handled in player order, and those do not contend. Worth pinning, because this
  is the exact case the parity gate never exercised — 300 episodes without both players selling the
  same product.

## Wrong measurements made along the way

Four wrong field names in one session, each producing a clean and plausible fabricated result:

- `row["action"]` — labels use `act`. Every day hashed to the same empty block, giving "1 distinct
  block per day for all 29 days".
- `obs["unlocked_shops"]` — labels use `shops`, replays use `town.unlocked_shops`.
- `"MELON" in t` on a replay tile — replay tiles are dicts, not strings, so melon was always 0.
- Consequently the first split table read 16.0 blocks per group, i.e. one group containing
  everything. That is not "the features do not explain it"; it is "no features were measured".

All four now raise instead of defaulting, and the scripts print what they are reading before they
count.

**Blocks-per-group is an in-sample statistic and flatters a finer key.** At d18 there are 182
distinct blocks and the moving key reported 2.1 per group, implying ~87 groups over 228 games. That
is why the tree exists: held-out games cannot be bought with a finer partition.

## What is NOT established

- **The library is Kawashigi's, so copying it copies his strategy, not a winning one.** These
  downloads are selected losses. Nothing here ranks a block by outcome and nothing can.
- **Every number is measured on completed games.** Whether a block still works when replayed
  against a *different* opponent is untested — and the opponent is precisely what the melon signal
  is about.
- **`HERD_GEESE = 0`.** GOOSE appears in 4 of the 8 animal classes, and EGG demand appears with
  probability 25% at d3 and 76% by d15. The goose negative was measured while `SELLABLE` held six
  of nine product names and EGG was not one of them (`main.py:9961`), so it is void. `SELLABLE` is
  now complete. The file asks for a fresh measurement rather than a hand-tune.

## Scripts

| script | what it answers |
|---|---|
| `count_day_blocks.py` | distinct day-blocks in our teacher's own play |
| `count_tape_blocks.py` | the same across 87 downloaded replays |
| `player_self_consistency.py` | does one player repeat themselves, and what key splits them |
| `build_day_rows.py` | one row per (game, day): 64 named features -> block id |
| `fit_day_classifier.py` | the tree, held-out by game, and it prints its rules |

## The new #1: Ryo Hasegawa, and he is a third shape

Nine games, downloaded 2026-08-20 23:02, episodes 95029938-95381518.
Six of the nine are against tetsuya, two against Arman Tuganbaev.
He wins seven of nine, by margins of 1,760 to 14,163 — but nine SELECTED games cannot support a
win rate and none is claimed here.

**His first five days are a frozen 120-turn unit script.**

    day 0   8 pairs  unit ops IDENTICAL
    day 1   8 pairs  unit ops IDENTICAL -- but 2 turn-pairs differ in MARKET ORDERS ONLY
    day 2   8 pairs  unit ops IDENTICAL -- but 2 turn-pairs differ in MARKET ORDERS ONLY
    day 3   8 pairs  unit ops IDENTICAL
    day 4   8 pairs  unit ops IDENTICAL
    day 5   8 pairs  0.8 differing unit-slots per pair  (PLANT 50%, WATER 50%)
    day 6   8 pairs  34.8 per pair

Every move, plant and water identical across nine games, regardless of opponent or shop draw.
**In a five-day window where he varies nothing else, selling is the only thing he varies** — which
is Alex's "the selling cadence and positioning is the tricky bit", arriving as the sole degree of
freedom in an otherwise frozen opening.

| | fixed unit opening | mid-game | shape |
|---|---|---|---|
| Ryo Hasegawa | **d0-d4 exact, d5 near** | breaks at d6 | longest frozen script, selling free |
| カワシギ | d1-d2 exact | branch persists, tree 58% at d12 | structure carried across days |
| tetsuya | d0-d3 (d3 at 98%) | lawnmower, tree 3% at d12 | reactive routine |

Kawashigi's fixed opening was 74 turns, ending at the d3 shop unlock. Ryo's runs 120 turns to d5
and does not react to the first shop draw at all.

### His repertoire

    PLANT       WHEAT 1157   STRAWBERRY 312   CARROT 205   MELON 147   TOMATO 26
    BUY_ANIMAL  COW 85   SHEEP 28
    SELL(orders) FERTILIZER 672  MILK 415  STRAWBERRY 353  WHEAT 323
                 WOOL 174  MELON 95  CARROT 73  TOMATO 34

- **No geese, no eggs.** COW and SHEEP only. Independent of our own goose verdict, which was void
  because EGG was unsellable when it was measured — this does not prove geese are bad, but it is a
  data point agreeing with `HERD_GEESE = 0` for an unrelated reason.
- **Tomato in 3 of 9 games**, 26 plants against 1,157 wheat — about 2% of his planting.
- **Carrot in 6 of 9 games**, 205 plants. Genuinely part of the repertoire.
- Wheat is 63% of everything he plants.

Those SELL figures are **order counts, not fills** — the agent re-posts an order every turn, so the
ordering between products is distorted by re-offer frequency. Presence and absence are reliable;
volumes are not. `kagg/analysis/fills.py` gives real quantities.

### A fifth wrong measurement, caught by disagreement

`what_differs_between_blocks.py` computed its `total` excluding the market column and then printed
"IDENTICAL" when `total == 0`. It reported Ryo's d1-d4 as identical while the self-consistency table
said 78% for d2. Both could not be true, and a direct hash of the raw actions settled it:

    day 0: 9 games, 1 distinct
    day 1: 9 games, 2 distinct  (7 vs 2)
    day 2: 9 games, 2 distinct  (7 vs 2)
    day 3: 9 games, 1 distinct
    day 4: 9 games, 1 distinct

The label was wrong, and the case it mislabelled is the most interesting one in the file. It now
says "unit ops IDENTICAL -- but N turn-pairs differ in MARKET ORDERS ONLY".

## Wrong-pick cost: the hoped-for result did NOT appear

When the tree misses, is the block it chose a near neighbour of the right one, or unrelated?
Against a random block from the same day's library, カワシギ:

| day | exact | wrong: real | random: real | ratio |
|---|---|---|---|---|
| 3 | 83.6% | 7.5 | 15.5 | 0.48 |
| 6 | 83.6% | 1.7 | 3.7 | 0.46 |
| 7 | 65.7% | 34.2 | 34.0 | 1.00 |
| 9 | 73.1% | 22.2 | 23.3 | 0.95 |
| 11 | 47.8% | 46.9 | 40.3 | 1.16 |
| 12 | 58.2% | 35.4 | 48.7 | 0.73 |
| 16 | 26.9% | 67.9 | 73.8 | 0.92 |

Median ratio about 0.73, but d7, d9, d11, d14 and d16 sit at 0.92-1.16 — on those days a miss is as
far from the truth as a random pick. **Exact-match accuracy is not a large underestimate**, which is
the opposite of what was suggested before measuring.

Counterweight: the absolute numbers are small against a day of ~190 unit-slots — a wrong pick at d12
differs on ~35 and a random block on ~49, so even random agrees on three-quarters. Whether the
residual matters is a money question and this measures ops. The real test is a replay through the
fast sim, which is parity-exact at 300/300 full-length episodes.
