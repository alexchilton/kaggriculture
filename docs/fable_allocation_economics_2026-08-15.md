# Allocation economics after the hinge — carrot, tomato, egg (Fable, 2026-08-15)

Every number below is either computed from `reference/kaggriculture.py` (1.32.7, hinge live)
or measured in real 1.32.7 games against the recorded ladder field.
Scripts: `scripts/optimal_release.py` (melon fix, in this worktree),
the paired sweep rows at `data/logs/fable_carrot_paired_sweep.jsonl` (216 games),
and the reruns in `data/logs/fable_optimal_release_rerun.log` / `data/logs/fable_breakdown30.log`.

## Headlines

1. **The deficit model is validated to the organiser's own numbers.**
   Monte Carlo over the shop draw gives P(hinge fires by d29, zero production) =
   CARROT 25.8%, TOMATO 53.4%, EGG 22.4% against the announced 26% / 50% / 22%.
   The mechanism is exactly as modelled: the town drain is unconditional, inventory is linear,
   and the premium is a function of which shops the RNG unlocked and when.
2. **Unconditional conversion has no edge, and the paired sweep shows why in dollars:
   wheat is itself on a starved book.** Five of eight shops stock wheat, so a zero-production
   wheat book reaches $48 by d29 on its own; our arm-0 games realise **$45.2/unit** on wheat.
   The extra carrots realise **$42-43/unit**. The "premium" crop pays LESS per unit than the
   crop it replaces, in the median game.
3. **The hinge is real but it is a CONDITIONAL play, and the condition is public.**
   The shop draw is in `obs.town.unlocked_shops`. By d12, four draws are visible and they
   separate the games sharply: with 2+ tomato-stocking instances visible (26% of games) the
   tomato hinge fires with certainty and the d29 book quotes a median of **$216/unit**;
   with 0-1 visible it quotes $70-91. Same shape for carrot and egg (tables below).
4. **Melon corrected: the release optimiser now front-loads it and the shipped agent is
   nearly optimal already** — ACTUAL $20,285 vs OPTIMAL $21,638, so melon leaves **+$1,353**
   on the table, not the -$11,929 the broken trickle model printed.
   Total release value for the seed-11 game: **+$5,653**.

## 1. The mechanism, from the env source

`market_price` below I0 (`reference/kaggriculture.py:198-201`):

    price = base * (1 + below_target * hinge(x / T)),   x = I0 - inventory
    hinge(u) = u + 8.0 * max(0, u - 1)^2                 (:68-73)

`_town_consume` (`:728-749`) subtracts stock **unconditionally** — one unit per shop instance
per stocked product, 6 ticks/day, doubled for single-product shops, plus 1/day town centre —
so with no production the deficit x grows linearly in each instance's active days.
Shops unlock at d3, d6, ..., d24, drawn uniformly WITH replacement from the eight names (`:886-891`).

Because inventory is linear, **the end-of-season deficit depends only on totals, but the price
each unit fetches depends on when it is sold** — below I0 the deficit only deepens, so for a
pure scarcity play the optimal release is to hold and dump at d29 (shed cap permitting), and
every unit sold lifts the book and decays the premium for the next one.

## 2. What the book quotes, by day (zero production, quantiles over 20k shop draws)

    CARROT (base 35, T 450, bt 1.00)      TOMATO (base 60, T 200, bt 0.40)     EGG (base 50, T 332, bt 0.40)
    day   p25  med  p75  p90   max        p25  med  p75  p90   max             p25  med  p75  p90  max
    10     36   38   41   43    50         61   63   67   69    72              51   51   54   54   56
    15     37   41   46   51    68         63   68   72   76    90              51   53   56   58   64
    20     39   45   53   60   180         67   73   80   88   298              53   57   60   63   81
    25     44   53   63   74   500         71   80  101  160   956              56   60   65   70  202
    29     49   58   71  116  1068         77   86  165  317  1803              58   63   69   83  397

    WHEAT, same premise (base 25, sqrt below-curve, FIVE shops stock it):
    d10 33, d15 37, d20 41, d25 45, d29 48 (medians)

Selling into the starved book decays the premium slowly (T is large):
a d29 dump at the median draw pays CARROT $51-56/unit even out to 120 units,
TOMATO $73-82, EGG $57-61; at the p90 draw CARROT $79-102, TOMATO $154-258, EGG $69-76.
Volume is not the binding problem — the level of the premium is.

## 3. What a tile is worth (through real yields)

Per PLANTING (one stop), unfertilized / fertilized, from the env source and confirmed against
`kagg/economics/production.py`: WHEAT 4/6 units, CARROT 3/4, TOMATO 4/8 (harvest between events).
Measured in the sweep: 28 carrot conversions produced +84.0 sold units/game = **3.0/stop**,
and cost -70.8 wheat units/game = **2.5/stop** of wheat actually forgone.

    one late stop (d12+)         units   $/unit realised/modelled       gross    seed     net
    WHEAT (what it does today)     2.5   $45.2 measured (arm 0)          $113     $10    $103
    CARROT, agent cadence          3.0   $42.2-42.8 measured             $127     $20    $107
    CARROT, held to d29, median    3.0   ~$55 modelled                   $165     $20    $145
    CARROT, 2+ relevant shops      3.0   $81-187 modelled                $243+    $20    $223+
    TOMATO, held to d29, median    4     ~$80 modelled                   $320     $50    $270
    TOMATO, 2+ relevant shops      4     $150-216 modelled               $600+    $50    $550+

So even played optimally, carrot in the MEDIAN game is worth ~+$40/stop over wheat before the
costs below — noise. The conditional plays are worth 2-5x a wheat stop, in ~26% of games.

**EGG / goose:** cost 300 + coop + place; FEED takes 1 WHEAT/day whose opportunity cost is the
same ~$45 starved-book wheat; fed+cared it yields 2 eggs/day from placement+4.
Median realised ~$55-60/egg late season: (2 x 57 - 45) = ~$69/day gross, minus 3 unit-ops/day
and the ferry, ~17 days from a d12 start = **roughly $870/goose net of the animal, before op
costs, in the median game**. The egg hinge fires in 22% of games and needs TWO egg shops
(bakery/brunch) drawn early — visible by d12 like the others. Egg is the weakest of the three:
the same wheat scarcity that feeds the hinge thesis is the goose's feed bill.

## 4. Why the field sweep said conversion loses win rate — resolved

Paired re-run: `WHEAT_TILES_TO_CARROT` 0/8/28, 12 richest recorded opponents, seeds 1300-1302,
both seatings — 72 paired boards per arm, per-product FILLS recorded both seats
(`data/logs/fable_carrot_paired_sweep.jsonl`). The parent sweep's percentages resolve to
100/144, 88/144, 92/144, 95/144, i.e. 24 opponents x 3 seeds x 2 seatings.

    arm    win     margin delta vs 0 (paired)    sign of margin delta
      0   80.6%              —                          —
      8   83.3%    mean +12, median +906         44/72 positive
     28   77.8%    mean -1,614, median -1,883    52/72 NEGATIVE  (sign test p < 0.001)

The arm-28 loss decomposes, per game:

    direct swap:      carrot +84u -> +$3,524   wheat sold -70.8u -> -$2,616     net  +$908
    gift to opponent: THEIR wheat +$725 on the SAME units (+0.2u)               net  -$725
    feed cascade:     our MILK -18.6u, WOOL -11.1u; our str/milk/wool -$1,981,
                      their milk/wool +$1,474                                   net ~-$1,800

Four mechanisms, in order of size:

1. **Wheat's own scarcity premium.** The forgone wheat unit sells at $45, the gained carrot
   unit at $42. The direct swap is a wash in the median game (+$32/stop at arm 28); the
   whole "carrot pays a premium" framing forgot that wheat's below-I0 book is starved too.
2. **The book is shared, so withdrawing supply is a price gift.** The recorded opponents sell
   1.5-2x our wheat volume. Selling 70 fewer wheat units leaves their book less lifted and
   hands them +$725/game on unchanged units. Our bank does not record this; the margin does.
   This is also the precise reason "carrot raised mean money while lowering win rate":
   money is our side of a two-sided ledger, and Elo pays the sign of the difference.
3. **The wheat buffer feeds the herd on the margin.** The flag's own docstring says the herd
   is fed entirely out of purchases (422 bought vs 329 fed) — true on average, false at the
   margin: at 28 conversions our milk drops 18.6u and wool 11.1u per game. Those are missed
   FEED days. At 8 conversions the effect is absent (milk -0.3u, wool -0.0u) — 8 is inside
   the buffer, 28 is not.
4. **Three of twelve opponents already produce the "no production" crops**
   (tawashi 58 carrots/game, YassY 24; HoJoonYun 24 tomatoes), so in a quarter of the field
   games the premise is partly false before we plant anything.

Note the honest discrepancy: in MY 12-opponent field, arm 8 was a slight paired WIN (+2.7pt,
44/72 positive) while the parent's 24-opponent run had 8 losing 8.3pt. Both are inside noise
for a ~$0 mean effect; the strong, replicable result is arm 28's paired loss.

## 5. The play this buys, if any

Not a fixed conversion — the sweep is right to reject that. The candidate worth testing is:

- **Gate on the observed draw at d12** (below). Convert to TOMATO only with 2+ relevant
  instances visible (26% of games, hinge certain, d29 median $216); carrot likewise
  (26% of games, d29 median $81+). 0-1 visible: plant wheat, as today.
- **Cap at ~8 stops** (inside the feed buffer; mechanism 3 starts somewhere between 8 and 28).
- **Hold the crop and release late** — selling on arrival realises $42 where holding
  realises $55+; below I0 the deficit only deepens.

    visible by d12     P(games)   P(tomato hinge)   tomato d29 med   carrot: P(hinge)  carrot d29 med
    0 relevant           31%            4%                $70              0%              $43
    1 relevant           42%           61%                $91             16%              $60
    2 relevant           21%          100%               $216             68%              $81
    3+ relevant           5%          100%               $546+            96%             $187+

    (relevant = PIZZA_SHOP/FARMERS_MARKET for tomato; PET_CAFE/FARMERS_MARKET for carrot;
     BAKERY/BRUNCH_SPOT for egg. Egg: 2 visible -> 68% fire, d29 median $72 — not worth a goose.)

Expected value of the gated tomato play, before cascade costs: ~26% of games x 8 stops x
(~$550 - $103) = **~$900/game mean, concentrated as ~$3,600 in the fired games** — real but
modest, and it must be bought without disturbing the schedule (mechanisms 2 and 3 still apply
to the 8 wheat stops given up: about -$200 of gift and, at 8 stops, no feed cascade measured).
A well-implemented version is worth one careful sweep; an unconditional one is settled: no.

## 6. Melon: the front-load fix and the corrected number

`scripts/optimal_release.py` grew a `release()` dispatcher: drain <= `NO_DRAIN_THRESHOLD` (1)
front-loads (sell on arrival), else `water_fill` as before.
Red-first test: `tests/test_a_no_drain_product_is_sold_the_day_it_arrives.py`
(3 tests; red before the fix, green after; fix backed out -> red again; restored -> green).

One finding from the test itself, worth keeping: **with no opponent melon flow, trickling is
harmless** — above I0 the book recovers at the 1/day drain. The race exists because the
recorded opponents dump 114-120 melons into the same book; against that flow, whoever sells
first gets the fresh book and anything held meets the floor on d29. The first draft of the
test used `THEIRS = 0` and correctly failed the revenue assertion; the premise was wrong,
not the fix.

Corrected release table (seed 11, tape kawashigi, rerun in
`data/logs/fable_optimal_release_rerun.log`):

    product      produced  we sold  drain   ACTUAL $  OPTIMAL $  left on table
    WHEAT             531      471     31     10,367     11,710         +1,343
    CARROT             12        6     19        204        404           +200
    STRAWBERRY        212      204     31     11,464     12,502         +1,038
    MELON             114      114      1     20,285     21,638         +1,353
    MILK              177      171     13     12,194     13,163           +969
    WOOL              193      176     13     29,273     30,023           +750
    TOTAL                                     83,787     89,440         +5,653

`docs/when_and_what_to_sell_2026-08-15.md` §3 carries a correction block now: the +$12,136
"even spread" number compared against an infeasible baseline; the real release value is +$5,653.

## 7. Code changes, and the d0-d8 gate

- `scripts/optimal_release.py`: `NO_DRAIN_THRESHOLD`, `front_load()`, `release()`; `main()`
  now calls `release()`. Analysis script only.
- `tests/test_a_no_drain_product_is_sold_the_day_it_arrives.py`: new, 3 tests, all green.
- `docs/when_and_what_to_sell_2026-08-15.md`: correction block in §3.
- **No agent code was touched** — `schedule_agent.py`, `cover.py`, the router and the schedule
  are byte-identical to the session start, so the d0-d8 grid cannot have moved. Confirmed by
  running the full 30-day grid (`data/logs/fable_breakdown30.log`): the season closes
  ours $149,207 / tape $150,076 on seed 11, every cash column reconciling to the dollar.

## 8. Nulls, losses, and honest caveats

- **My first test premise was wrong** (melon trickle vs front-load with zero opponent flow:
  front-load does NOT win there; the book recovers 1/day). Kept in the test as a comment.
- **Arm 8 vs arm 0 is a null**: mean margin +12 on 72 paired games. The parent's -8.3pt at
  arm 8 and my +2.7pt cannot both be treated as signal; the mean effect is ~$0.
- **The zero-production price tables are a premise, not a forecast**: our own selling decays
  the premium (quantified in §2), our shipped plan already grows ~12 carrots, and 3/12
  recorded opponents produce carrot or tomato.
- The conditional-play EV in §5 is a model number, not a measured one — it inherits the
  d29-dump release assumption and charges no routing cost for the late harvest/water pattern
  (tomato planted d12 wants ~12 daily waters and harvests d20-23; the grid currently carries
  13-90 idle unit-turns/day mid-season, so turns exist, but the router has to actually reach
  the tiles).
- The paired sweep field skews to games Alex kept, which skews to losses (CLAUDE.md); win
  rates here are "vs these opponents", never a rating.
