# Marginal units, the shared book, and what the shop draw is worth

Measured 2026-08-16 on branch `kawashigi-plan` at `3f9fb83`.
All seasons are the straw arm, our live agent in seat 0, Kawashigi's recorded actions in seat 1,
`weedSpawnChance=0.0`, one season per arm.
Logs: `data/logs/pricedist_fert_off.log`, `data/logs/pricedist_fert_on.log`,
`data/logs/shop_draws_by_seed.log`, `data/logs/goose_tomato_arms.log`,
`data/logs/goose_late_arms.log`.

## 1. Revenue is the wrong objective, and it reversed a decision

The fertilizer sell exemption (`prod not in NEVER_DRAINED`, `NEVER_DRAINED = ("FERTILIZER",)`,
which lets fertilizer sell before `LATE_SELL_FROM_HOUR = 16`) was measured on seed 11 both ways.

Ours, revenue by product:

| product | fert OFF | fert ON | delta |
|---|---:|---:|---:|
| WOOL | 42,871 | 42,051 | -820 |
| WHEAT | 19,925 | 20,408 | +483 |
| FERTILIZER | 14,302 | 14,612 | +310 |
| MELON | 14,179 | 14,179 | 0 |
| MILK | 12,006 | 8,058 | -3,948 |
| STRAWBERRY | 10,942 | 5,970 | -4,972 |
| CARROT | 704 | 806 | +102 |
| **TOTAL** | **114,929** | **106,084** | **-8,845** |

Theirs:

| product | fert OFF | fert ON | delta |
|---|---:|---:|---:|
| WHEAT | 45,222 | 43,963 | -1,259 |
| WOOL | 20,954 | 20,715 | -239 |
| MILK | 18,130 | 12,117 | -6,013 |
| MELON | 16,648 | 16,648 | 0 |
| STRAWBERRY | 10,434 | 3,917 | -6,517 |
| FERTILIZER | 8,972 | 8,820 | -152 |
| **TOTAL** | **120,360** | **106,180** | **-14,180** |

Banks: ours 80,581 -> 71,254 (-9,327), theirs 61,474 -> 48,117 (-13,357),
**margin +19,107 -> +23,137 (+4,030)**.

Fertilizer's own revenue moves **+$310**. The exemption does not work by selling fertilizer better.
It frees the h0-h15 window, and the knock-on collapses the strawberry and milk books for **both**
players. We lose $8,920 on those two lines; he loses $12,530. We bank less and win by more.

**This is why a revenue table must never be used to rank an arm.** The same mistake had already
been made twice in one session: the new 4-board solve was shelved partly because it showed
STRAWBERRY $67,838 against the committed routes' $10,942, and that comparison measures nothing.
Only the margin, or the win, counts.

The exemption is **not** unconditionally good. On seed 3 it is **-2,081**. The rematch corpus put it
at 69/97 against 66/97 (7 gained, 4 lost, p~0.27). It is not established.

## 2. The book is shared, so our own count is not the lever

Seed 11, both seats, units into the same town inventory against the shops that drain it:

| product | ours | theirs | total | shop-slots draining it | our $/unit |
|---|---:|---:|---:|---:|---:|
| MILK | 186 | 249 | 435 | 1 | 64 |
| WOOL | 189 | 94 | 283 | 1 | 227 |
| STRAWBERRY | 277 | 261 | 538 | 4 | 40 |
| WHEAT | 469 | 1,062 | 1,531 | 6 | 42 |
| EGG | 0 | 0 | 0 | 6 | -- |

Milk is at the floor because 435 units go into one shop's worth of drain and **249 of them are
his**. Cutting our own cow count cannot fix a book he floods anyway. Wool holds $227 on the same
single slot only because 283 units exist in total.

## 3. Drain is not what sets the price -- supply is

Mean shop-slots draining each product, over seeds 1-40 (`data/logs/shop_draws_by_seed.log`):

| product | mean slots |
|---|---:|
| WHEAT | 5.22 |
| STRAWBERRY | 3.85 |
| MILK | 3.17 |
| EGG | 2.05 |
| TOMATO | 1.95 |
| CARROT | 1.65 |
| WOOL | 1.12 |

**WOOL is the least-drained product in the game and our best-priced at $227/unit.** So "is this a
good seed for crop X" cannot be read off the shop draw alone. What matters is units already in the
book, and the draw only matters where the book is contested.

Seed 11 is the extreme egg seed of the sample: `BRN BAK BRN BAK YRN BAK BRN SMO`, six of eight
shops draining EGG, zero draining TOMATO or CARROT.
Seed 3 is the best tomato seed of the sample: `BRN YRN ICE PIZ FRM FRM PIZ PIZ`, five slots.

## 4. One wheat tile to tomato: a null on both seeds

`WHEAT_TILES_TO_TOMATO = 1`, margin against the same base:

| seed | base | tomato1 | delta | tomato sold |
|---|---:|---:|---:|---|
| 11 (TOM 0 slots) | +19,107 | +19,093 | **-14** | 8 units @ $91 |
| 3 (TOM 5 slots) | +6,602 | +5,579 | **-1,023** | 7 units @ $63 |

On top of the fertilizer exemption: seed 11 -2,702, seed 3 +835.

So the answer is no, including on the best tomato seed in a 40-seed sample. The earlier
`WHEAT_TILES_TO_TOMATO = 24` result (49/97) was read as "flooding is bad, one unit might be fine".
One unit is not fine either. It is simply worth nothing.

**And it cannibalises carrot.** On seed 3 the base sells 12 CARROT at **$265/unit** -- our best
per-unit line on that board, better than wool -- and the tomato arm drops it to 11 units at $122.
Carrot at 12 units is the underexploited line here, not tomato.

## 5. One goose on a cow: the d0 result is an artifact, again

`HERD_GEESE = 1`, `HERD_GEESE_FROM = ("COW",)`. The swap took the **d0 cow at places index 1**:

    d0: BEFORE places ['SHEEP','COW','SHEEP','COW']   bought {COW:2, SHEEP:2}
         AFTER places ['SHEEP','GOOSE','SHEEP','COW']  bought {COW:1, SHEEP:2, GOOSE:1}

Margin seed 11 +19,107 -> **-12,494**. Seed 3 +6,602 -> **-2,801**.

That is not the goose. The eggs behaved exactly as predicted -- 54 units at $53 into an empty book,
$2,862 of revenue on both seeds. The damage is wool:

| | units | $/unit | revenue |
|---|---:|---:|---:|
| base | 189 | 227 | 42,871 |
| goose1cow | 88 | 53 | 4,664 |

**Wool fell $38,207.** A COOP displaced the COW that commit `3f9fb83` had just paired with the first
sheep on the prime zero-walk cell, and the sheep's feed/care cadence broke. `pending_care_bonus`
only rises on a night both fed and cared (`reference/kaggriculture.py:823`), so a broken pairing
halves the yield of the best product on the board.

This is the sixth time an animal verdict here has been an artifact of something the code could not
express or something unrelated that broke. See `CLAUDE.md` and
`project_kaggriculture_animals_verdict`.

The schedule buys cows on d0, d3, d5, d7, d9 and d11 -- ten cows and four sheep -- so the goose
should be able to take a late cow and leave the d0 pen untouched.

**It cannot. Every late swap is a no-op.** Margins on seeds 11 and 3, five arms
(`data/logs/goose_late_arms.log`, `data/logs/goose_d3_arms.log`):

| arm | seed 11 | seed 3 |
|---|---:|---:|
| base | +19,107 | +6,602 |
| goose1@d3 | +19,107 | +6,602 |
| goose1@d5 | +19,107 | +6,602 |
| goose1@d9 | +19,107 | +6,602 |
| goose2@d9,d11 | +19,107 | +6,602 |

Byte-identical, every product line included. `swap_in_geese` itself is fine -- called directly it
rewrites the right row at every floor:

    EARLIEST=(0,...)  d0  ['SHEEP','COW','SHEEP','COW'] -> ['SHEEP','GOOSE','SHEEP','COW']
    EARLIEST=(3,...)  d3  ['COW']                       -> ['GOOSE']
    EARLIEST=(5,...)  d5  ['COW']                       -> ['GOOSE']
    EARLIEST=(9,...)  d9  ['COW','COW']                 -> ['GOOSE','COW']
    EARLIEST=(11,...) d11 ['COW','COW']                 -> ['GOOSE','COW']

The rows are simply never acted on. Censused over a full season on seed 11, base and `goose1@d5`
emit exactly the same orders:

    BUY_ANIMAL: {COW: 4, SHEEP: 4}
    PLACE     : COW 6, SHEEP 8, FERTILIZER 6, WOOL 1

**The schedule asks for ten cows and four sheep. The live agent buys four and four.** The purchase
path is not `animals_bought` per row: `want_total` is a cumulative target
(`schedule_agent.py:4539`), and from `SHOP_ADAPT_FROM_DAY` on, `SHOP_ADAPT_HERD` overwrites
`want_total["COW"]` and `want_total["SHEEP"]` outright from `_herd_split` (`:4556-4588`). A GOOSE
inserted into a row it never reads changes nothing.

So the only swap that bites is d0, and d0 is the one that breaks the sheep pairing. **The goose
question remains unanswerable without a change to the purchase path** -- `_herd_split` decides a
two-species split and there is no third slot for a bird. That is a code change, not a flag.

Second finding, worth more than the goose: we run **four cows**, not eight or ten. The user's
"8 is too much on some boards" is already true at four -- 186 units of milk from four cows into a
book the opponent adds 249 to.

## What this closes and what it opens

- **Closed:** one wheat tile to tomato, on a dead tomato seed and on the best tomato seed. Null and
  a small loss. Do not retry at any small count.
- **Closed:** revenue as a ranking statistic for any arm.
- **Void, not closed:** the goose. The only two goose measurements this project has ever taken were
  both confounded -- the first by `SELLABLE` omitting EGG, the second by the d0 pen.
- **Open:** carrot at $265/unit on seed 3 off 12 units.
- **Open:** ten cows into a book the opponent floods with 249 units of his own.

## 6. The counterfactual: our milk is a weapon, not a revenue line

The agent does not need changing to answer this. The season is played once, then the MARKET is
replayed under a counterfactual supply using the env's own `market_price` and its own per-unit
lockstep (`scripts/what_one_animal_is_worth.py`, logs `data/logs/counterfactual_cow_to_goose.log` and
`data/logs/counterfactual_by_seed.log`).

**The model is validated before it is used.** Replaying the recorded season reproduces it:

    item     replay ours   recorded ours   replay theirs   recorded theirs
    MILK          12,010          12,006          18,128            18,130
    WOOL          42,871          42,871          20,954            20,954

Two mechanics decide everything here, both read off `reference/kaggriculture.py`:

- `_commit_unit`: **"Sales at $1 do not increase market supply."** Flooding self-limits at the floor.
- EGG is `base 50, below_target 0.4`, so an egg can **never** fetch more than **$70**. MILK is
  `base 160, above_target 1.6`, ceiling $256, floor $1.

### Take one of our four cows out, seed 11

    units ours   rev ours   $/unit  |  units theirs   rev theirs   $/unit
    base      186     12,010     64.6  |          249       18,128     72.8
    -1 cow    139     12,192     87.7  |          249       24,145     97.0
    delta     -47       +182           |                    +6,017

**Dropping a cow costs us $0 and hands him $6,017.** The 47 units lost are the $1 ones; the
remaining 139 reprice 64.6 -> 87.7 and cancel the loss exactly. His 249 units reprice 72.8 -> 97.0.

Our milk is not a revenue line. It is a **denial** instrument, and its value is proportional to
**his** volume, not ours. That inverts how every animal arm in this project has been judged.

### It flips sign on the shop draw and on his volume

| seed | milk shops | egg shops | straw shops | his milk units | our milk units | denial value | our cost |
|---|---:|---:|---:|---:|---:|---:|---:|
| 11 | 2 | 2 | 3 | 249 | 186 | +6,017 | +182 |
| 4 | 3 | 4 | 5 | 249 | 277 | +12,305 | +5,632 |
| 3 | 1 | 2 | 1 | 179 | 267 | +676 | -668 |
| 33 | 1 | 4 | 2 | 179 | 267 | +676 | -668 |

Cow -> goose, margin:

| seed | 1 egg/night | 2 eggs/night | 4 eggs/night |
|---|---:|---:|---:|
| 11 | -4,461 | -3,150 | -764 |
| 4 | -5,132 | -3,636 | -763 |
| 3 | +205 | +1,711 | +4,610 |
| 33 | +499 | +2,194 | +5,284 |

Where he lands 249 milk units the cow denies him $6k-$12k and no goose can replace it. Where he
lands 179 the denial is $676 and the goose wins. **The goose is a conditional buy, not a flat
yes or no** -- which is why every unconditional goose verdict this project has taken was wrong.

Cow -> strawberry, margin:

| seed | +22 units | +66 units |
|---|---:|---:|
| 11 | -2,995 | +1,195 |
| 4 | -2,315 | +4,553 |
| 3 | +244 | +2,158 |
| 33 | +1,485 | +6,334 |

**Positive on all four at +66, negative on two at +22.** Same mechanism: at volume our strawberry
denies him more than the milk did -- on seed 33 his strawberry revenue falls **-$5,019**. A half
swap gives up the milk denial without buying enough strawberry denial to replace it.

### What this does not measure

- **One opponent.** Every seed is Kawashigi's tape, so his cow COUNT never varies. His milk units
  moved 179 vs 249 only as a price side effect. "It depends how many cows he has" is the right
  question and is **not answered here**; it needs a second opponent tape.
- **The strawberry arm is a market estimate, not a plan.** It assumes a cow's ~3 actions a day
  convert into +66 strawberry units. Whether the planner can grow and water them is unproven.
- Both arms hold all actions fixed. Correct for the opponent, whose fills are shed-limited; an
  approximation for us.

## 7. CORRECTION to sections 5 and 6: the herd count was wrong

**Section 5's claim "the live agent buys four cows and four sheep" is WRONG.** It came from counting
`BUY_ANIMAL` **orders** in the action stream -- the offers-are-not-fills mistake this project has a
standing rule against (`feedback_offers_are_not_fills`). The board census run beside it iterated
rows instead of cells, returned `{}`, and that empty result was not flagged.

Counted off the tiles, seed 11:

    end d 0  OURS {SHEEP 2, COW 2}   THEIRS {SHEEP 2, COW 2}
    end d 6  OURS {COW 4, SHEEP 2}   THEIRS {COW 4, SHEEP 2}
    end d 9  OURS {COW 6, SHEEP 4}   THEIRS {COW 8, SHEEP 3}
    end d20  OURS {COW 6, SHEEP 8}   THEIRS {COW 9, SHEEP 3}

**We run 6 cows and 8 sheep -- 14 animals. He runs 9 cows.** Placement days, both sides:

    OURS   COW d0x2 d3 d5 d7x2      SHEEP d0x2 d7 d8 d10x2 d12x2
    THEIRS COW d0x2 d3 d5 d7x4 d18  SHEEP d8

What this invalidates:

- per-cow yield is 186/6 = 31 units, not 46.5, so "his 249 milk is 5.4 cows" was wrong -- he has 9
- the section 6 counterfactual scaled our milk by 3/4; one cow out of six is 5/6, so every denial
  figure in that section is scaled wrong and must be re-run
- `the_best_answer_to_his_herd.py --pens 8` was clamped from the wrong number; it is 14

What survives: the goose row swaps are genuinely no-ops, and `SHOP_ADAPT_HERD` is why -- it
re-decides the schedule's 10 cows / 4 sheep into 6/8 and never reads a GOOSE row.

## 8. Production is exact, so the grid can be solved rather than sampled

`_daily_refresh_animals` (`reference:823`) makes a season's yield a pure function of species and
placement day, under best play (fed and cared every night, collected on every production day):

| animal | d0 | d3 | d6 | d9 | d12 |
|---|---:|---:|---:|---:|---:|
| COW | 39 | 33 | 30 | 24 | 21 |
| SHEEP | 38 | 34 | 30 | 26 | 22 |
| GOOSE | **56** | 50 | 44 | 38 | 32 |

Validated: our 6 cows on their real slots predict 202 milk against 186 sold (92%); 8 sheep predict
227 wool against 189 sold (83%). The shortfall is unfed nights and unsold stock.

**A goose out-produces a cow 56 units to 39** -- it just sells into a $70 ceiling instead of $256.

### Both players 0..14 cows, seed 11 (`data/logs/cow_grid_exact.log`)

Margin in $k, our cow count down, his across, remainder sheep, purchase cost included:

    our\his     0     2     4     6     8    10    12    14
          0   0.9  -5.4   0.7   2.5   3.0   7.7   7.5   9.3
          2   8.5   1.8   6.1   7.3   8.6  15.1  14.9  16.7
          4   3.7  -0.2   3.2   5.6  11.7  28.3  30.4  37.7
          5   0.8  -2.0   1.1   4.6  15.4  31.2  36.7  41.9
          6  -1.0  -3.6  -0.8   4.4  14.7  30.1  34.8  39.7
          8  -0.8  -5.4  -2.8   1.1   9.2  21.5  25.9  30.5
         10  -3.1  -9.8 -12.1 -11.3  -1.7  10.1  14.6  19.2
         14  -9.9 -26.9 -40.6 -31.1 -20.2  -8.5  -3.8   0.8

Our best reply to his cow count:

    his cows  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
    our cows  2  2  2  2  2  2  2  6  5  5  5  5  5  5  5

**He plays 9. Our best reply is 5. We play 6.** So the herd is already close to right, worth about
$1k -- and the $30k+ in that table is not ours to take, it is his 9 cows into a one-MILK-shop seed.

The reply function is a step, not a slope: **2 cows while he is under-invested, 5 once he floods.**
Under 7 of his cows the milk book still pays, and the cheapest way to hold price is to stay out of
it; above that the book is dead either way and the extra cows are pure denial.

Caveats that bound this table: it forces all 14 slots to COW or SHEEP, so geese and crop are
excluded -- on seed 11, with 6 EGG shops and 1 MILK shop, the costed surface picks geese instead.
The single fixed point at 2 is a symmetric read, not an equilibrium: his placement slots differ
from ours, so a proper equilibrium needs his best reply iterated too, which is not run.

## 9. CORRECTION: the shop draw is ENDOGENOUS, and the 40-seed scan is void

`_spawn_weeds` consumes the day's rng **once per tile** before `rng.choice(sorted(SHOPS))` runs
(`reference:876-891`). Tile count therefore moves every later draw, and tile count is decided by
land purchases. The draw is a function of play, not of the seed.

Measured, same seed, same config, only the agents differ:

    seed 11  PASS: BRUNCH BAKERY BRUNCH BAKERY YARN BAKERY BRUNCH SMOOTHIE
    seed 11  REAL: PET_CAFE PIZZA YARN ICE_CREAM BAKERY BRUNCH FARMERS YARN
    seed  3  PASS: BRUNCH YARN ICE PIZZA FARMERS FARMERS PIZZA PIZZA
    seed  3  REAL: BAKERY BAKERY PET PET PET PET SMOOTHIE PET

**Section 3 is void.** The mean shop-slots-per-product table, "seed 11 is the extreme egg seed",
and "seed 3 is the best tomato seed" were all measured with PASS agents and describe draws that do
not occur in a played game. Section 8's grid is also void: it took its drain series from a PASS run.

It does explain the section 4 carrot result. Seed 3 under real play draws **five PET_CAFEs**, and
PET_CAFE is single-product so it drains CARROT at x2. Carrot realised $265/unit there because the
drain was enormous and we sold 12 units.

### The corrected grid (`data/logs/cow_grid_real_shops.log`)

Our best reply in cows, remainder sheep, 14 animals, exact production, purchase cost included:

    seed 11   CARROT:2 EGG:2 MILK:2 STRAWBERRY:3 TOMATO:2 WHEAT:5 WOOL:2
      his cows  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
      our cows  8  7  5  5  4  4  5  4  4  4  3  3  3  3  3     fixed point 4

    seed  3   CARROT:5 EGG:2 MILK:1 STRAWBERRY:1 WHEAT:2
      his cows  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
      our cows  2  2  2  2  2  2  2  2  3  5  8  8  8  8 10     fixed point 2

**Two milk shops supports 4-8 cows; one supports 2.** The margin scale moves with it as well --
seed 11 reaches +$53.8k, seed 3 only +$13.8k, because with one milk shop and no yarn store both
animal books saturate and livestock cannot win much at all.

**Against his real 9 cows on seed 11, our best is 4 and we run 6: about $7k.** The PASS-agent grid
put the same gap at $1k.

### What this means for strategy, and it is not a table lookup

Because the draw responds to play, a seed-keyed lookup is impossible in principle. Conditioning
must happen at RUNTIME -- shops unlock every 3 days and `town.unlocked_shops` is fully observable.
That is what `SHOP_ADAPT_HERD` already attempts; what it lacked was a correct target, which the
grid now supplies.

### Standing rule this adds

Never characterise a seed from a run whose actions differ from the shipped agent's. The draw, the
drain and therefore every price in the season are downstream of what was played.

## 10. The goose is conditional on the YARN_STORE, and that is why every verdict was wrong

Optimal (cows/sheep/geese) against his 9 cows / 3 sheep, synthetic drain, exact production,
purchase cost included. `data/logs/optimal_herd_14_vs_18_slots.log`,
`data/logs/optimal_herd_18_slots.log`.

A milk shop drains 1 per event (all are multi-product). A YARN_STORE drains **2** (single-product
multiplier), so one yarn store absorbs roughly twice what one milk shop does.

### 14 slots

| milk | yarn | cows | sheep | geese | margin | margin with geese BANNED |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 3 | 3 | **8** | +13,089 | -2,355 |
| 1 | 0 | 5 | 2 | **7** | +11,276 | -2,001 |
| 2 | 0 | 7 | 2 | **5** | +6,395 | -1,744 |
| 3 | 0 | 10 | 2 | 2 | +5,323 | +2,535 |
| 0 | 1 | 1 | 9 | 4 | +35,119 | +28,568 |
| 1 | 1 | 4 | 8 | 2 | +29,161 | +28,054 |
| 2 | 1 | 6 | 8 | 0 | +21,678 | +21,678 |
| 2 | 2 | 5 | 9 | 0 | +26,753 | +26,753 |

**Geese rescue exactly the boards with no yarn store** -- a $15,444 swing at `0 milk / 0 yarn`,
$13,277 at `1 milk / 0 yarn`. At two or more yarn stores they leave the optimum entirely.

Measured over 24 seeds under REAL play (`data/logs/shop_draws_real_play.log`), **38% of draws have
no yarn store**: seeds 2, 3, 4, 7, 9, 13, 14, 19, 23. Two of 24 (8%) have `milk<=1 and yarn 0`.

So the goose is worth five figures on 38% of boards and nothing on the other 62%. Every previous
verdict measured ONE board and generalised. `SELLABLE` blocking EGG was one artifact; the d0 pen
pairing that cost $38,207 of wool was another; **conditioning on the wrong variable was the third
and the one that mattered.**

### 18 slots -- and Q4 costs $7,000, which is NOT in these numbers

| milk | yarn | 14 slots | 18 slots | Q4 gain |
|---:|---:|---|---|---:|
| 0 | 0 | 3/3/8 +13,089 | 3/3/12 +17,077 | +3,988 |
| 1 | 0 | 5/2/7 +11,276 | 5/3/10 +15,191 | +3,915 |
| 2 | 0 | 7/2/5 +6,395 | 8/3/7 +12,358 | +5,963 |
| 0 | 1 | 1/9/4 +35,119 | 2/9/7 +42,488 | +7,369 |
| 2 | 1 | 6/8/0 +21,678 | 7/8/3 +32,325 | +10,647 |
| 1 | 2 | 3/11/0 +40,357 | 3/15/0 +56,610 | +16,253 |
| 2 | 2 | 5/9/0 +26,753 | 6/12/0 +47,112 | +20,359 |
| 4 | 2 | 8/6/0 +12,102 | 9/9/0 +36,389 | +24,287 |

**No yarn store: the extra pens gain $3,900-$6,000 against a $7,000 quadrant -- Q4 does not pay for
itself on animals.** Two yarn stores: +$13k to +$24k, and it is one of the best buys in the game.

The optimum always fills every slot that exists; the extras go to **sheep on yarn boards, geese on
no-yarn boards**. At `0 milk / 0 yarn` geese take 12 of 18.

### The decision rule, on two observable integers

Both counts are readable from `town.unlocked_shops` as shops unlock every 3 days, which is what
`SHOP_ADAPT_HERD` already watches -- it has never had a correct target.

    yarn 0:  geese-heavy. cows 3/5/7/10/13 as milk shops go 0->4, sheep 2-3, geese take the rest
    yarn 1:  1/9/4, 4/8/2, 6/8/0, 8/6/0, 9/5/0
    yarn 2+: no geese. 0/14, 3/11, 5/9, 8/6

His herd changes how much we WIN, not what we should DO: against 6 cows/6 sheep instead of 9/3, the
optimal allocation differs in two cells of twenty, by one animal each, while margins move by up to
$19k (`data/logs/optimal_herd_vs_6_6.log`).

### Limits, and they are not small

- Sections 8-10 are synthetic drain plus exact production. **Not one played season.** Today's
  record is that every unreplayed claim here needed correcting.
- The 18-slot placement days (d14/16/18/20) are an ESTIMATE of when Q4 pens come online, not
  measured. Late slots are where the yield curve is steepest, so this assumption carries weight.
- The sweep never leaves a slot empty when an animal has positive value, so it cannot find the
  seed-3 played answer of running nine animals rather than fourteen.

## 11. What section 10 assumes about the opponent, and which assumptions were tested

Assumed: **9 cows, 3 sheep** on his real placement slots
`[0,0,0,3,5,7,7,7,7,8,18,18,18,18]`, read off seed 11's board at season end; **zero geese**;
**no crops at all** -- only MILK, WOOL and EGG are priced; and Kawashigi's tape as the opponent on
every seed.

### Tested: does the goose survive an opponent who also buys geese?

Board `0 milk / 0 yarn / 2 egg`, his 14 slots split across cows/sheep/geese
(`data/logs/goose_vs_opposing_geese.log`):

| his geese | his cow | his sheep | our cow | our sheep | our geese | margin |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 10 | 4 | 3 | 3 | 8 | +18,802 |
| 2 | 9 | 3 | 2 | 2 | 10 | +12,407 |
| 4 | 7 | 3 | 2 | 2 | 10 | +7,472 |
| 6 | 6 | 2 | 2 | 2 | 10 | +5,323 |
| 8 | 4 | 2 | 2 | 2 | 10 | +2,039 |
| 12 | 1 | 1 | 2 | 2 | 10 | +5,314 |

**Our best response never leaves geese** -- it rises 8 -> 10 and stays there even against 12 of his.
What collapses is the board's VALUE: +$18,802 -> +$2,039.

Same structure as milk in section 6. A contested book pays almost nothing to either side, and you
hold the position to DENY rather than to earn. **The recommendation is robust; the prize is not.**

### Not tested, and these matter more

- **The crop books are absent.** His strawberry, wheat and carrot are not modelled. On seed 3 the
  real money was five PET_CAFEs draining CARROT at x2 -- a book this sweep cannot see. So the herd
  optimum is chosen while ignoring what those pen slots could have grown instead, which is the same
  half-measure trap the cow->strawberry arms exposed in section 6: giving up the milk denial without
  buying enough of the replacement.
- **One opponent tape** on every seed. His herd is fixed at whatever Kawashigi ran.
- **No played season** confirms any cell in sections 8-11.

## 12. The ideal split given our BLIND opening -- the decision-ready table

No shop exists before d3 (`townShopUnlockInterval = 3`), so the opening cannot be conditioned on
the draw. Slots d0,d0,d0,d0,d3,d5 are fixed at **3 cows + 3 sheep** -- what we play now. The eight
later slots (d7,d7,d7,d8,d10,d10,d12,d12) are free and CAN react, because by d7 two shops are out.

14 animals total, exact production, purchase cost in, opponent 9 cows / 3 sheep / no geese, 2 egg
shops. `data/logs/ideal_split_fixed_opening.log`.

| milk | yarn | the 8 reactive slots | TOTAL c/s/g | margin |
|---:|---:|---|---|---:|
| 0 | 0 | 8 goose | 3/3/8 | +13,680 |
| 1 | 0 | 8 goose | 3/3/8 | +7,562 |
| 2 | 0 | 4 cow + 4 goose | 7/3/4 | -1,421 |
| 3 | 0 | 8 cow | 11/3/0 | -1,538 |
| 0 | 1 | 7 sheep + 1 goose | 3/10/1 | +34,729 |
| 1 | 1 | 7 sheep + 1 goose | 3/10/1 | +28,611 |
| 2 | 1 | 6 sheep + 2 cow | 5/9/0 | +12,451 |
| 3 | 1 | 3 sheep + 5 cow | 8/6/0 | +727 |
| 0 | 2 | 8 sheep | 3/11/0 | +41,493 |
| 1 | 2 | 8 sheep | 3/11/0 | +35,375 |
| 2 | 2 | 6 sheep + 2 cow | 5/9/0 | +14,614 |
| 3 | 2 | 5 sheep + 3 cow | 6/8/0 | +1,933 |
| 4 | any | 8 cow | 11/3/0 | ~+550 |

### The rule for the reactive eight

    no yarn store  + 0-1 milk  ->  all geese
    no yarn store  + 2   milk  ->  half cows, half geese
    any yarn store + 0-1 milk  ->  all sheep
                   + 2   milk  ->  6 sheep, 2 cows
                   + 3   milk  ->  5 sheep, 3 cows
                   + 4   milk  ->  all cows

**Cows only earn a slot at 3+ milk shops.** Below that the eight go to sheep if a yarn store exists
and geese if one does not.

### The margin column matters more than the split

Holding yarn fixed and raising milk shops: +41,493 -> +14,614 -> +1,933 -> +550.

**A milk shop makes the board WORSE for us regardless of allocation**, because it subsidises
whoever is the bigger dairy farmer and that is him: 9 cows against our 3-11. A yarn store is the
mirror gift -- he keeps 3 sheep, so the wool drain is nearly ours alone (+13,680 -> +41,493 going
0 -> 2 yarn stores at the same milk count).

So the draw sets the size of the prize; the herd only decides whether we collect it.

### The live misallocation

Our shipped 6 cows / 8 sheep is optimal at `3 milk / 2 yarn` -- **a board worth $1,933**. On the
boards actually worth winning (0-1 milk, 2+ yarn, worth $35k-42k) the answer is **3 cows / 11
sheep** and we run nearly twice the cows. Unlike the $7k in section 8 this is not an artifact of a
forced constraint: the opening is pinned to what we actually play.

Caveats from section 11 still bind in full -- no crop books, one opponent tape, synthetic drain,
and **no played season confirms any cell here.**

## 13. The d7 decision is under UNCERTAINTY, and that changes the answer

Section 12 assumed the shop counts were known when the eight reactive slots are filled. They are
not. Shops unlock every 3 days to 8 instances (d3..d24), so **at d7 only two exist and six are
still to be drawn**.

The three animal books never share a shop, so the remaining draws are multinomial:

    milk-draining  PIZZA, ICE_CREAM, SMOOTHIE   3/8
    egg-draining   BAKERY, BRUNCH               2/8
    wool-draining  YARN_STORE                   1/8
    neither        PET_CAFE, FARMERS_MARKET     2/8

This predicts `1 - (7/8)^8 = 65.6%` of boards carry a yarn store; the 24-seed real-play scan
measured 62%. The uniform model is sound.

### Committing all eight at d7 is expensive

`data/logs/d7_decision_under_uncertainty.log`:

| known at d7 | EV-best 8 slots | EV margin | perfect info | VOI |
|---|---|---:|---:|---:|
| 0milk 0yarn 0egg | 4cow 4sheep 0goose | -1,947 | +9,455 | +11,403 |
| 0milk 0yarn 1egg | 4cow 2sheep 2goose | -1,572 | +10,207 | +11,779 |
| 0milk 0yarn 2egg | 4cow 1sheep 3goose | +581 | +12,089 | +11,507 |
| 1milk 0yarn 0egg | 8cow 0sheep 0goose | -1,902 | +3,879 | +5,781 |
| 0milk 1yarn 0egg | 2cow 6sheep 0goose | +10,721 | +14,576 | +3,854 |
| 2milk 0yarn 0egg | 8cow 0sheep 0goose | +128 | +1,572 | +1,444 |

**Geese enter only in proportion to egg shops ALREADY SEEN** -- 0 seen: 0 geese; 1 seen: 2 geese;
2 seen: 3 geese. So `HERD_GEESE = 0` is the CORRECT d7 choice on a blind board, and was only ever
wrong as a season-long constant. The bird belongs in the d10/d12 slots once BAKERY or BRUNCH_SPOT
has actually appeared.

Section 12's confident "8 geese at 0 milk / 0 yarn" does not survive uncertainty: six unknown draws
will most likely deliver milk shops, so the EV answer is the hedge 4 cows / 4 sheep.

### Staging recovers most of it

Commit only the three d7 slots, decide the other five informed
(`data/logs/d7_staged_vs_commit.log`; the last five get perfect information, so this is an UPPER
bound on staging):

| known at d7 | commit 3 at d7 | staged | all 8 at d7 | staging gain | perfect |
|---|---|---:|---:|---:|---:|
| 0milk 0yarn 0egg | 3 cow | +6,490 | -1,947 | +8,437 | +9,455 |
| 0milk 0yarn 1egg | 2 cow + 1 goose | +7,142 | -1,572 | +8,714 | +10,207 |
| 0milk 0yarn 2egg | 2 cow + 1 goose | +9,333 | +581 | +8,752 | +12,089 |
| 1milk 0yarn 0egg | 3 cow | +3,120 | -1,902 | +5,022 | +3,879 |
| 0milk 1yarn 0egg | 3 sheep | +14,279 | +10,721 | +3,557 | +14,576 |
| 0milk 1yarn 1egg | 3 sheep | +14,554 | +10,721 | +3,832 | +14,851 |
| 1milk 1yarn 0egg | 2 cow + 1 sheep | +5,145 | +2,928 | +2,217 | +5,960 |
| 2milk 0yarn 0egg | 3 cow | +1,525 | +128 | +1,397 | +1,572 |

Staging captures **74%** of the value of perfect information on a blind board.

### The d7 rule

    yarn store already seen  ->  3 sheep
    no yarn, egg shop seen   ->  2 cows + 1 goose
    nothing useful seen      ->  3 cows

**Cows are the HEDGE at d7**, not the preference -- milk is the modal shop type at 3/8 against
wool's 1/8. You buy cows on a blind board because they are the most likely to be right, and you
keep the d10/d12 slots free to correct.

Caveats from section 11 still bind: no crop books, one opponent tape, synthetic drain, and no
played season confirms any cell in sections 8-13.

## 14. MEASURED AND REVERTED: the milk-conditioned cow cap

`EARLY_YARN_COW_BY_MILK = (4, 4, 5, 6)` replacing the flat `WOOL_SHOP_COW_CAP = 6` on the
early-yarn branch of `_herd_split`.

**Rematch corpus, 97 recorded ladder games: 63/97 against a baseline of 66/97. Reverted.**
`data/logs/rematch_milk_conditioned_cap.log`.

Four played seeds said the opposite, on margin:

| seed | yarn at | flat 6 | milk cap | delta |
|---|---|---|---|---:|
| 10 | draw 1 | 6c/12s +27,650 | 4c/14s +32,110 | +4,460 |
| 12 | draw 1 | 6c/12s +29,502 | 4c/14s +31,754 | +2,252 |
| 15 | draw 1 | 6c/12s +37,516 | 4c/14s +42,208 | +4,692 |
| 18 | draw 1 | 6c/12s +22,887 | 5c/13s +21,972 | -915 |

Mean +$2,622 of margin, and three fewer wins. **Bigger margin, fewer wins.** The same divergence
the fertilizer exemption showed pointing the other way (banks $9k less, wins $4k more). Selecting
on money remains wrong even when the money is a MARGIN rather than a bank.

### Two facts worth keeping from the attempt

- **The change is unreachable unless YARN_STORE lands at draw 1 or 2.** `bought` floors the split
  and the opening buys four cows by d5, six by d7; `WOOL_SHOP_DRAW_LIMIT = 3` looks through d9.
  On seeds 11 and 3 the edit was byte-identical. By the leader's own distribution that is ~31% of
  boards. Any future cap change below 6 has to move the OPENING, not `_herd_split`.
- **Solved days do not block it.** Base solves d12-29, q4 solves d9-29; cows are bought d0-d7 and
  the four seeds above are all q4 (18 animals), yet the herd still moved 6/12 -> 4/14 with the
  total intact. A precomputed route is a visit ORDER and `_live_ops` re-derives the op at each stop,
  so a pen stop places whatever is in the shed.

### What this says about sections 8-13

Every number there is a MARGIN computed on the market maths. Section 14 is the first time one of
them met the win-rate evaluator, and it did not survive. **Treat the whole surface as a generator of
hypotheses about money, not about wins**, until a cell is tested on the rematch corpus.

## 15. Marginal value per crop unit -- wheat is the worst thing on the board

Priced on the real books of a played season, adding units to our own supply and repricing both
sides (`data/logs/marginal_value_per_crop.log`).

| product | seed 11 $/unit | seed 3 $/unit | his units in book (11 / 3) |
|---|---:|---:|---|
| MELON | **268** | 187 | 106 / 64 |
| CARROT | 63 | **219** | 0 / 0 |
| EGG | 51 | 59 | 0 / 0 |
| STRAWBERRY | 105 | 44 | 261 / 192 |
| WHEAT | **21** | **20** | 1,062 / 951 |

Per PLANTING (both wheat and melon cap at `max_yield 6`): melon $1,608 against wheat $126 on
seed 11 -- **12.8x**.

### The wheat denial theory is dead

Adding 72 of our wheat units costs him **$82**. The book holds 1,531 units, the curve is flat that
far out, and the `_commit_unit` floor rule stops dumping from moving supply at all once price hits
$1. Being the larger seller does not make him vulnerable in a saturated book.

Melon is the opposite profile and is where denial actually works: +12 melon units cost him
**-$1,730** on seed 11. Small book (178 units both sides), high price ($197-250), and he is in it.

### Correction to section 14's arithmetic

I priced 72 marginal wheat units at the season AVERAGE $42 to get ~$3,024. They earn **$1,432**,
about $20 each. Average price where marginal price applies -- the same error class as the offers/
fills and PASS-agent mistakes earlier in this document.

### What Kawashigi actually does with two freed pens

His three-quadrant 6-cow/6-sheep seats against his 10/4 seats (`data/logs/kawa_plants_by_herd.log`,
n=3 vs n=38, so weak):

| crop | 6/6 | 10/4 | delta |
|---|---:|---:|---:|
| WHEAT | 139.3 | 127.1 | +12.2 |
| STRAWBERRY | 34.0 | 35.7 | -1.7 |
| MELON | 20.0 | 18.3 | +1.7 |
| CARROT | 7.7 | 6.1 | +1.6 |

The marginal 14 plantings are 88% wheat, but priced by section 15 the **+1.7 melon is worth ~$2,700
and the +12.2 wheat ~$1,514**. Seven times fewer plantings, nearly twice the value. The wheat is
filler; the mix is the point.

### Eggs versus the freed pens

| | seed 11 | seed 3 |
|---|---:|---:|
| +72 wheat | +1,514 | +1,467 |
| +70 eggs | +3,632 | +4,194 |

Eggs beat the wheat conversion 2.4x on market value. Against melon or carrot they lose.

### The standing conclusion

**Melon and carrot are worth 4-10x everything else at the margin, both are shop-conditional, and
neither is reactive in our agent.** Tomato remains dead for the reason it always was: nobody is in
the book, so there is nothing to deny and the price is simply base.

All of section 15 is MARGIN. Section 14 showed twice in one night that margin does not reliably
convert to wins on the rematch corpus.

## 16. Crop value versus the OPPONENT'S holding -- an inverted U, and one negative

His supply of a product is scaled on a fixed board (seed 11), so the shop draw is held constant and
only his holding moves. `data/logs/crop_value_vs_his_holding.log`.

Margin to us of adding units:

| we add | his x0 | his x0.5 | his x1.0 | his x2.0 |
|---|---:|---:|---:|---:|
| 12 MELON | +2,493 | +2,719 | **+3,217** | +946 |
| 24 STRAWBERRY | **-3,657** | +1,492 | **+2,518** | +1,916 |
| 12 CARROT | +750 | +750 | +750 | +750 |
| 70 EGG | +3,592 | +3,592 | +3,592 | +3,592 |
| 72 WHEAT | -316 | +1,514 | +1,514 | +1,444 |

### Two structures, not one

**Contested crops (melon, strawberry) are an inverted U in his holding.** Too little of his supply
and we simply flood our own book -- strawberry with him absent is **-$3,657**, actively negative,
because our existing 277 units reprice down and nobody absorbs the damage. Too much of his and the
book is already floored -- melon falls $3,217 -> $946 when his 106 units become 212. The peak sits
near where he actually plays.

**Uncontested crops (carrot, egg) are perfectly FLAT.** Identical value whatever he does, because
he is never in those books. Lower ceiling, zero variance, and they need no read on the opponent --
only on the shop draw.

### This retires the "we only have one tape" objection, for crops

Scaling his supply on a fixed board isolates the dependence without needing a second opponent. The
answer is that melon and strawberry are bankable only because the field is homogeneous: the
124-game census put 21.5% of all field plantings on strawberry and 11.7% on melon, so an opponent
is reliably in both books. That is what makes the fragile crops safe, and it is the first thing
that would break if the field changed.

For ANIMALS the objection still stands -- his herd is fixed at whatever Kawashigi ran.

### Practical split

- **Robust bets, shop-conditional only:** CARROT (needs PET_CAFE / FARMERS_MARKET), EGG (needs
  BAKERY / BRUNCH_SPOT, and no yarn store competing for the pens).
- **High-ceiling fragile bets, needing the opponent in the book:** MELON, STRAWBERRY.
- **Filler:** WHEAT at ~$20/unit, and negative if the opponent ever leaves that book.

Still margin, not wins. Section 14 stands: the one cell of this surface that met the rematch
corpus lost 63/97 against 66/97.

## 17. The mirror: what a Kawashigi-vs-Kawashigi board actually pays

Seed 11, per-unit realised price. `solo` = only we sell; `actual` = the played season; `mirror` =
both sides selling HIS volume. `data/logs/mirror_glut.log`.

| product | solo $/u | actual $/u | mirror $/u | mirror vs solo |
|---|---:|---:|---:|---:|
| MILK | 231.3 | 64.6 | 51.1 | **-78%** |
| STRAWBERRY | 134.8 | 39.5 | 40.9 | **-70%** |
| MELON | 243.2 | 196.9 | 147.0 | -40% |
| WHEAT | 31.2 | 19.8 | 19.6 | -37% |
| WOOL | 236.7 | 226.8 | 224.3 | **-5%** |
| CARROT | 64.0 | 64.0 | -- | he sells none |
| EGG | -- | -- | -- | neither sells any |

**Wool is the only product that survives a mirror.** He runs 3 sheep (94 units), so even doubled
the YARN_STORE's x2 drain absorbs it. Everything else he plays falls 37-78%.

Read the CARROT and EGG rows correctly: they are blank in the mirror because a Kawashigi mirror
sells **zero** of both, not because they crash. Those books are untouched by construction.

### What this explains

- **Why every optimal-herd table in sections 10-13 piles into sheep.** Wool is the one animal book
  a homogeneous field cannot crush.
- **Why carrot realised $265/unit on seed 3** while we sold 12 units. Nobody is in it.
- **Why the old goose verdict was garbage.** "-$21k a game at one bird" was measured IN A MIRROR
  (commit `c9c1c18`), where both sides buy geese and glut the one book that was otherwise free. The
  deleting commit `7a88d30` even states that a mirror "gluts a shared book by construction and then
  measures the glut". That is precisely what happened. Combined with `SELLABLE` omitting EGG and the
  d0 pen pairing, the bird has now been condemned three times by three unrelated artifacts.

### The standing strategic shape

Against a field that all plays the same tape, revenue lives in **WOOL, CARROT and EGG**. The
contested books -- MILK, STRAWBERRY, MELON, WHEAT -- are worth entering for DENIAL, not for
revenue, and section 16 gives the band of opponent holding where that denial actually pays.

This is the `CLAUDE.md` lesson restated as prices: the edge is in the dimensions where the field is
homogeneous, because those payoffs are contested and the value of deviating rises with how many
people share the convention.
