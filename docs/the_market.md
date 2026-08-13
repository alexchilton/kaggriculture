# The market — mechanism, cadence, and what actually moves the price

Merged 2026-08-13 from nine 2026-08-09/-10/-12/-13 write-ups (`the_market_2026-08-09.md`,
`what_the_town_will_actually_eat.md`, `what_saturates_and_what_does_not_2026-08-09.md`,
`fable_market_shape_2026-08-09.md`, `the_book_is_shallow_2026-08-09.md`,
`the_market_cadence_over_all_products_2026-08-10.md`, `the_market_is_the_late_season_2026-08-13.md`,
`the_late_season_is_one_defect_in_two_halves_2026-08-12.md`, `d18_harvest_and_sells_2026-08-12.md`)
plus the carrot economics file (`carrot_swap_2026-08-12.md`). All source files deleted; every number
below was copied across, not re-derived.

**Read `docs/market_depth_and_the_morning_losses_2026-08-13.md` first.** It is the current, most
recent authority on price mechanics (the base/shops/drain/price-at-N/floor-units table) and two real
ladder losses decomposed by product and by day. This file does not repeat that table — it holds
everything *else*: the derived sell rule, real-tape appetite measurements, fill-level (not offer-level)
analysis, intra-day cadence defects, the late-season investigation, and carrot.

> **SELLABLE correction, 2026-08-13.** `SELLABLE` excluded CARROT, TOMATO and EGG until commit
> `c99a8a5`. Every dollar figure below involving those three products, or geese/eggs, was measured
> with that revenue line disconnected and is flagged VOID inline, section by section.
>
> **1.32.6 correction.** All nine source files are dated 2026-08-09 or later, i.e. already
> post-town-rebalance (2026-08-08). No further version flag needed except where individually noted.

---

## 1. The sell rule, derived

Offer the largest `n` such that `market_price(p, I_now+n) ≥ max(λ_p, (1−slip)·market_price_now)`,
where `λ_p = market_price(p, I_now + Q_rem − contest·D_rem)` and `contest` (1.0 solo-optimal, 0.5
two-player-split) replaces a hardcoded day-total `allow`; `slip` replaces a hardcoded `rate[prod]`.

Both `PRICE_AWARE_SELL_CAP` and `RESERVATION_SELL_CAP` ship ON. The handover fixture went from
$71,976 / 331 units destroyed / 12 turns at cap to $75,866 / 82 destroyed / 2 (+$3,890, −75% waste).
A second fixture went from $62,868 / 86-165 destroyed / land days [4,6,15/16] to $64,667 / 39-107
destroyed / land [4,6,16] (+2.9% bank).

A second depth table, version-invariant, gives units above I0 to reach 0.9x/0.75x/0.5x of base —
finer-grained than market_depth's p@50/100/200:

```
product      to 0.9x base   to 0.75x   to 0.5x
WHEAT              20          2421      ~inf
EGG                24          1422      ~inf
FERTILIZER         53           128       253
MELON              51            80       113
CARROT             10            55       230
WOOL               19            30        42
TOMATO              7            38       144
MILK                 8            20        39
STRAWBERRY           7            16        32
```

**Note:** this table's own season-absorption numbers (WHEAT 525, STRAWBERRY 426, CARROT 327, MILK
327, TOMATO 228, EGG 228, WOOL 228, MELON 30, FERTILIZER 0) matched market_depth's `drain` column
exactly on cross-check and are dropped here as redundant — read market_depth for drain.

## 2. What the town actually eats — 87 real tapes, not simulation

Measured 2026-08-11 off 87 recorded ladder games (`data/seed_scripts/top_guys`), reading each game's
closing `market.inventory` against its own `town.unlocked_shops` directly — no simulation.

```
product      shops   appetite range   closing surplus range
WHEAT          5      745-1,282        -386 to -1,356    (negative on ALL 87)
CARROT         2       29-924           -12 to -1,002
TOMATO         2      208-924           -30 to -678
STRAWBERRY     4      387-1,282        -381 to +60
MILK           3      566-1,103        -342 to +77
EGG            2      208-566          -624 to +108
WOOL           1       29-387          -424 to +59
MELON          0       29 (fixed)       +38 to +158      (positive on ALL 87)
FERTILIZER     0        0 (fixed)      +201 to +493      (positive on ALL 87)
```

**WHEAT closes negative on every single one of 87 tapes** — the town eats more than both farms
together produce, and price *rises* to $40-$59 against a $25 base. This directly rebuts a shipped
comment in `schedule_agent_1455mh.py` calling wheat "a bad trade" on a 6-unit yield assumption; the
measured `production.py` yield is 28 (42 fertilized).

**MELON and FERTILIZER close positive on every one of 87 tapes without exception.** Melon's only
consumer is the town centre (29 units/season, fixed by rule); 17 tiles at ~12 units/tile is 204
units into a 29-unit appetite — every player over-plants melon, winners included, so it is a shared
inefficiency, not a losing move relative to the field. Fertilizer demand is zero on every board by
rule (`kaggriculture.py:101` excludes it from the town-centre list, no shop carries it), not by seed
draw. Marginal price: 50u→$90 (cum $4,755), 100u→$80 ($9,010), 150u→$70 ($12,765), 200u→$60
($16,020), 250u→$50 ($18,775), 400u→$20 ($24,040), 500u→$1 ($25,052) — every one of the 87 tapes
closes fertilizer at $1-$20 against its $100 base, i.e. the book is saturated by season's end in
every game ever recorded here.

CARROT/TOMATO/STRAWBERRY/MILK/EGG/WOOL show mixed positive/negative surplus across the 87-tape
range, reflecting shop-draw variance. This measurement reads **other players'** closing inventory
from real games, not our own agent's sell behaviour — it is not filtered by our own SELLABLE list
and is not subject to the SELLABLE correction.

Appetite is a ceiling, not a prediction: this table models neither turns, walking, watering nor
reachability.

## 3. Where each product's revenue actually saturates

First-local-peak table under `CONTEST=1.0` (splitting season demand with one other seller):

```
product           peak units   price     season $    tiles/head-equiv
WHEAT                 276      $25.0      $6,900       6.6
CARROT                 156     $35.0      $5,460       4.0
TOMATO                 104     $60.0      $6,240       6.5
STRAWBERRY              224    $120.0    $26,880      18.7
MELON                    88    $179.0    $15,748       7.3
MILK (cow)              160    $160.0    $25,600       2.4
WOOL (sheep)             112    $192.2    $21,529       2.3
EGG (goose)              128     $50.0     $6,400       1.2   -- VOID, see below
FERTILIZER             4,000      $4.1    $16,250        --
```

**Read "first local peak" literally** — a naive global maximum returns nonsense once price has
crashed through the $1 floor (revenue then rises forever with volume); an earlier pass made exactly
this mistake.

Corrected per-head animal production (fixing a bug that computed herd output as `events × max_held`
when an animal makes one unit per event — every herd had been overstated 4-6x):

```
head        1     2     4     8    12    16    20    24
COW        80   160   320   640   960  1164  1164  1164   (flat from 16)
SHEEP      67   133   267   533   800   897   897   897   (flat from 16)
GOOSE      50   100   200   246   246   246   246   246   (flat from 8)
```

This brackets rank-1 Seb's observed 9 cows / 11 sheep — an earlier, buggy model had wrongly
predicted saturation at only 4 head and contradicted him.

Fertilizer production is species-independent: `tile["fertilizer_available"]=True` for every animal
tile every day regardless of species (`kaggriculture.py:818`) — a $300 goose makes fertilizer at the
same rate as a $500 sheep.

**VOID pending re-measurement, SELLABLE correction:** the EGG row's $6,400-season peak and the
$246/day herd cap it implies were computed against `market_price` for a product that could not
actually be sold until commit `c99a8a5` (2026-08-13). Only the underlying egg *production-count*
table above (50/100/200/246 eggs at 1/2/4/8+ geese, flat from 8 head) is a yield fact independent of
sellability and survives.

## 4. Fills vs offers: what really moved the price

A fill-level (not offer-level) comparison of Seb's tape, our loss, and the opponent who beat us in
that same loss found Seb's realized price 51-65% above both — but the small/late-order theory does
**not** explain it: the winning opponent's own single-product orders were *larger* than Seb's (mean
7.8 vs 4.0 units, max 31 vs 16) while realizing a *lower* average price ($85.84/unit vs Seb's
$141.35). Our own losing game sold 85% of its single-product covered volume in wheat and fertilizer
(both under $75/unit) while the winning opponent sold 70% of its volume in strawberry at $161/unit
without collapsing the price. **The gap reads as product mix, not order shape.**

Full per-source numbers: coverage of SELL-emitting turns 81% Seb / 41% us / 76% opponent (money-
conservation method; shed-delta only caught 18/244 clean turns for Seb, a >90% undercount). Revenue:
Seb 113 events / 1,064 qty / $150,395 / $141.35 mean / order size 4.0 mean, 16 max. Us: 130 events /
1,053 qty / $98,072 / $93.14 mean / 2.0 mean, 6 max. Opponent (won): 79 events / 1,209 qty / $103,777
/ $85.84 mean / 7.8 mean, 31 max. By hour bucket ($/unit, h0-7/h8-15/h16-23): Seb $149.17/$130.35/
$138.68 (flat-to-down late); us $108.66/$60.62/$86.89 (mid-day worst); opponent $76.65/$150.42/
$95.68 (no pattern).

**`LATE_SELL_BIAS`** (block all sells before hour 16, last-day liquidation exempted) was confirmed:
8-seed × 3-opponent × both-seatings arena A/B (48 games/state) took pool win rate 14.6%→27.1%
(+12.5pp), mean money $16,146→$24,535 (+$8,389). Per-opponent: heuristic 8,672/12.5%→23,196/25.0%;
rancher 21,450/6.2%→28,612/31.2%; contrarian 18,317/25.0%→21,798/25.0% — positive or flat on every
individual opponent.

**`CAP_SELL_OFFER_SIZE`** (cap any single offer at 30 units) was verified to work correctly when
triggered (seed 2 vs contrarian: 43-unit offer capped to exactly 30, $10,268→$10,265) but came back
byte-identical on the 8 held-out A/B seeds because none of them produced an over-30 offer — a genuine
null from an under-powered test, not evidence the cap is useless. A wider 24-seed×opponent sweep
found exactly two over-30 offers, both `SELL WHEAT 43` on d29 h0 against contrarian only.

Two false leads retracted the same day they were raised: a "delivery problem" (443 units apparently
stranded in hands at dusk on seed 13) dissolved once fills were counted properly — 100-109% of
everything produced gets sold, 0 units left in shed or hands at season end across four seeds; the
apparent gap was comparing agents with different herd sizes plus sampling only at the single worst
instant (dusk). And a claimed "board property" for shop-draw absorption was wrong because
`_spawn_weeds` consumes the same per-day RNG stream *before* the shop draw, so which shops unlock is
agent-play-dependent, not seed-pure — seed 29 looked wool-starved under a PASS-only game and draws
YARN_STORE under real play.

**Same agent, same code, same schedule, same opponent tape banked $16,888-$163,036 across 36
seed×opponent seasons** (6 tapes × 6 seeds) with milk realizing $27.90-$252.66/unit purely from board
variance. MILK is board-driven (spread 88.5 holding opponent fixed) because it sits in 3 of 8 shops
(P(never drawn in 8) = 2.3%); WOOL is opponent-driven (spread 73.1 holding seed fixed) because it
sits in exactly 1 of 8 (YARN_STORE, P(never drawn) = 34.4%) — whoever else dumps wool sets its
price. `town["unlocked_shops"]` is fully observable every turn (`shared: True`) even though the
underlying seed is hidden, yet the production side of the agent — animal and crop targets — is fixed
before the board is known and never consults the draw: a board with no YARN_STORE still buys full-
price sheep.

Shop-draw probability (never drawn in 8): WHEAT 5/8 shops, 0.2%; STRAWBERRY 4/8, 2.3%; MILK 3/8,
2.3%; WOOL 1/8, **34.4%**; MELON 0/8, always.

Separately: animal loss from two consecutive unfed days is irreversible and invisible in final-bank
terms — shipped agent loses 1 animal on seed 13, one variant loses 4, another 8-11. A distinct
defect from price collapse, not to be traded against it.

Across 14 real ladder losses, re-pricing only our own sales downward turns 12/14 into wins.
Recoverable money by product at the optimal multiplier: WOOL +$135,250 (0.7x), STRAWBERRY +$57,433
(0.7x), MILK +$57,163 (0.5x), MELON +$4,447, WHEAT $0 (1.0x — no gain), FERTILIZER $0 (1.0x). Wool
is specifically a volume problem, not a cadence one (episode 91122388: $5,278 observed vs $23,794 at
0.7x). Cutting dominates over spreading: downscaled-only +$254,293 (best 16/56), spread-only
+$87,343 (best 16/56), both together +$252,611 (best 17/56) — spreading adds little once cutting is
already applied.

## 5. Intra-day cadence: when we sell, not just how much

Comparing exact committed fills against Seb's own schedule orders hour-by-hour across d0-d7 (seed
11, tape `91422988`) found quantities roughly match but hours are systematically wrong in the same
direction on every product:

1. **Unfilled sell quotas carry forward and dump at hour 0.** 14 wheat units dumped at dawn across
   d5-d7 recovering an unfilled d4 row. Hour 0 is triply the worst hour: no harvest yet, town hasn't
   drained yet, and it's the same hour `BUY_PRODUCT` fires, paying the spread twice.
2. **Our sells fire in the morning, Seb's fire in the evening.** With the town draining once a day,
   selling before the drain sells at the bottom of the curve every time. FERTILIZER shown day-by-day:
   ours d2 h07/08/12/13 vs his h15/19; d3 ours h07/12/13/14 vs his h15/18; d5 ours h04/13/14/18 vs
   his h17/19/20; d7 ours h05/19 vs his h17/22/23.
3. **Our buys front-load into a block; Seb's drip.** d0 identical quantity, opposite distribution:
   ours h01-h08 (8 consecutive turns) vs his h05/07/09/11/12/14/17/19 (spread across 15). Shops
   restock every 4 steps, so his spacing buys into a restocked book while ours buys the second half
   into a book its own first half already lifted.

Priced concretely: on d6 Seb funds a land parcel by hour 13 from two wool sells at h09/h13 (bank $5
→ $1,349); our equivalent wool sale timing leaves us $47 short until h23, missing the same-day land
purchase by ten hours. Also d4: our single 25-unit wheat lump at h16 clears at a materially worse
mean than Seb's four smaller blocks (h18/21/22/23, 5/12/12/20) with restocks between.

**Caveat carried forward: the tape this was measured against (Seb, `91422988`) is now known to be
tuned for the pre-1.32.6 economy** (his median bank has since halved and he has withdrawn from the
ladder) — the target is superseded, but the hour-shape mechanism (sell-after-drain, drip not
block-buy) is argued to still generalize and is untested against a current target. Whether moving
sells later is worth it in money was explicitly left unmeasured.

### The d16-d19 reconciliation: why daily deltas often look worse than they are

A fill-by-fill reconciliation (seed 11, tape victor) found most apparent day-level deficits are
phase-shift artefacts. `harvest 11/14` on d18 is not three missed harvests — they were taken a day
early on d17 (cumulative d16-d18 harvest reconciles exactly, 46/46). `sell 35/61` on d18 is the exact
mirror of a `90/39` surplus on d17 (cumulative sells at end of d18: ours 499 vs tape 489, and we're
$3,045 ahead in money at that point) — caused by our own `LATE_SELL_FROM_HOUR=16` policy: the tape
posts its sell row at dawn against yesterday's still-unsold shed, while we sell late the same day and
sweep our own same-day production as it lands, so our dawn-d18 shed genuinely only holds what we
then offer, and every unit offered that day fills.

**One deficit does NOT reconcile: FERTILIZER 0/8 on d18, still −8 by end of d19.** The shed held
9-13 fertilizer all day but `FERTILIZER_RESERVE_LOOKAHEAD_DAYS=1` computed a 12-tile reservation need
against a 9-unit shed and withheld the entire offer. The reserve exists because an earlier incident
(d16) fired only 6 of 12 scheduled FERTILIZE ops when the shed ran dry — relaxing it is not
established as safe on this evidence alone.

## 6. The late season specifically

Three candidate explanations for the late-season gap were tested and killed in one session (seed 11,
tape victor):

- **More crew hands is not the answer.** +4 hands on d26-d29 cost −$3,350; the extra hands idled
  (hire d26 10→14, pass 36→124, water unchanged 36→36).
- **We already do more ops than the tape and still lose.** 2,978 vs 2,800 work ops, 862 vs 935 idle
  ops, and we finish $11k behind.
- **Routing is not the constraint either.** The greedy solver already covers 60/60, 61/61, 48/51→
  51/51, 25/25 on d26-d29, but dropping days from `SOLVED_DAYS` on "coverage looks fine" reasoning
  cost −$2,277 and returned weeds to 5/day — coverage and visit order are different claims.

**`LATE_SEASON_PAIR`** (`FERTILIZE_UNTIL_DAY=26`, `LATE_TRUNCATED_PLANT_DAY=26`,
`HARVEST_A_TRUNCATED_ONE_SHOT`, gated to d26+) measured as a pair: stale routes −$1,863, re-solved
routes **−$370**, routes dropped −$2,647 (control $72,184 both times). With routes re-solved, per-op
rows land almost exactly on tape (plant d26 0→12 vs tape 11; water d28 26→38 vs tape 39; harvest d28
17→30 vs tape 20). **−$370 is explicitly undecided, not a win** — inside the ~15% seed-variance
band; the decider is `field_sweep.py` against recorded opponents.

### The DIG/PLANT/HARVEST chaining defect behind it

The late-season plant/harvest gap is one defect needing two changes together, neither of which pays
alone. Half one: `DIG` clears ground exactly like a one-shot HARVEST does, but the replant-chaining
rule only fires on the HARVEST case — ground DIG clears stays empty for the rest of the season (seed
11 d26: 11 DIGs, 0 PLANTs offered; confirmed live on ladder episode `92433651`, 13 tiles dug and 0
planted the same day). This is the fourth instance of a recurring pattern already fixed three times
(`BUILD_THEN_PLACE`, `PLANT_THEN_WATER`, `REPLANT_A_CLEARED_TILE` itself). Implementing the DIG chain
alone was measured and **reverted**: it cost −$2,898 and the target d26 plant count did not move at
all, because half two blocks it independently.

Half two: `plant_prize('WHEAT', 25)=75.0` but `plant_prize('WHEAT', 26)=0.0` — correctly zeroed under
the rule that a one-shot only pays through a full-window HARVEST, since a d26 planting can't reach
its harvest day before season end. But Victor's own recorded play (`91854176.json`) plants 11 wheat
on d26 and takes a genuinely **partial** harvest on d29 (26 units at age 2-3, not the full 4-day
window) — the environment allows this, and it is wheat-specific: every melon Victor harvests is a
full `held 6/max 6` at exactly age 10, never partial.

**Fix order matters:** teach the harvest rule to accept a partial one-shot near season end first
(which makes late `plant_prize` non-zero), then chain the DIG-to-replant fix on top. Measuring
either half alone will misread as a loss or a no-op. Route note: the 8 pre-solved routes are keyed
to exact job lists, so either change invalidates all of them and requires re-solving in day order.

### The milk-floor correction, and where the SELLABLE bug hid inside it

**Correction, 2026-08-13: "the milk floor is partly a harness artefact."** Three real downloaded
ladder episodes (`92450417`, `92443929`, `92442061`) carry market price at each day's close: MILK
does not floor in these three — 169→279, 169→258, 169→154 (WOOL dips to 82 on d10 in one, then
recovers to 245). `breakdown.py` seats our agent against a *replayed* tape, and both sides sell into
one shared book, so a tape that sold 303 milk in its own real game sells it *again* next to us in the
harness — glutting a book no real game gluts. **`market_depth_and_the_morning_losses_2026-08-13.md`'s
own two real ladder losses show MILK closing at $5 and $3** — both real ladder data, both post this
correction. Not a strict contradiction (milk floors in some real games and not others, consistent
with "cow count is causal" below) but "never floors" is too strong; read as **"milk does not always
floor on the ladder; whether it does depends on cow count relative to the opponent's."**

What does replicate across 11 real ladder losses: **every game where `SHOP_ADAPT_HERD` cut cows to 6
closed MILK above base ($169/$235/$249); every game running 8-9 cows floored it at $1. The cow COUNT
is causal.** `SHOP_ADAPT_HERD` floats the cow/sheep split on which shops *exist*, never reads
realized price — we run COW 10/SHEEP 4 against every recorded opponent's COW 8/SHEEP 6.

**RETRACTED, SELLABLE correction:** the same 2026-08-13 file also claimed "not one egg is ever sold"
across a full season with `HERD_GEESE=2` (animals 10, season money $48,196 vs $71,814 without geese,
sell revenue $188,908 vs $214,385) and concluded "the geese verdict was measuring our own bug" —
diagnosing the zero-egg-sales as a routing/outcome-only-sweep artefact. **This diagnosis is itself
almost certainly wrong: `market_depth_and_the_morning_losses_2026-08-13.md` confirms EGG was
unsellable by our own agent until commit `c99a8a5`, landed the same day.** The true cause of zero
egg sales was that the agent could not emit a SELL EGG order at all, not a routing artefact. **This
is the fifth time an animal verdict in this project has turned out to be an artefact of our own
code** (see `docs/REGISTER.md`'s SELLABLE caveat). Geese/eggs are a live, re-openable axis in the
running product-mix sweep now that the fix has landed.

## 7. Carrot economics — pool verdict VOID, needs re-run

`carrot_swap_2026-08-12.md`'s own investigation independently discovered, one day before the official
fix, that the schedule's `sells` rows never emitted CARROT — every tape-mutation arm in that file
banked $0 of carrot revenue by construction. It also found the framing itself was wrong: real leader
play (カワシギ's tapes) plants carrot d21-d26 as an **addition** to otherwise-idle late-season ground
(wheat can no longer finish there; carrot's `first_yield_day=2` still can), never as a wheat
substitute.

**Because `SELLABLE` excluded CARROT entirely until `c99a8a5` (2026-08-13), the file's pool-level
"deciding measurement" was also run against the real game engine before the fix landed, and must be
treated as void alongside the tape arms until re-run:**

```
CARROT_SWAP=1     seeds 1300-1303 (192 games/arm)  win rate 65.1% -> 54.7%   (-10.4pts)
                   seeds 1306-1309                  win rate 67.2% -> 59.4%   (-7.8pts)
CARROT_TILES=4     768 games                        win rate 72.2% -> 71.1%  (-1.1pt, null)
```

`CARROT_SWAP` shipped OFF on this evidence; that verdict is now unsafe to rely on. If SELLABLE
blocked carrot sales throughout the measurement, a negative win-rate result is unsurprising and
uninformative — it may simply re-measure "carrot revenue is zero because the engine blocks it," not
"carrot is uneconomical."

**The one plausibly-durable number, because it's planner-independent price-curve arithmetic rather
than a played-out measurement:** carrot's market book tops out at **$3,502 on the best of 16 towns
and $91 on the worst** (vs strawberry's $29,172 and wheat's $12,246 on the same town) — the flattest,
shallowest book of any crop measured, which caps how much even a perfect planner could ever extract
from it as a wheat substitute.

Whether carrot pays as a **late-season addition** on otherwise-idle ground (the real question, opened
by `LATE_TRUNCATED_PLANT_DAY=26` above) remains genuinely untested and is the live open question, not
"does carrot substitute for wheat."

## 8. Validated levers, ranked

A 124-seat/62-game lever-correlation table: sell_orders +0.384, feed +0.359, harvest +0.334, care
+0.327, hires +0.301, buy_product +0.255, herd +0.258, tiles +0.149, plant −0.050. Money: ours
$73,977, field $68,091, top-20% $116,407. `buy_product` (feed conversion) is the one lever still at
only the 49th percentile against a top-quintile value of 1,156 — everything else is already matched
or beaten against the field.

**`vs_tapes.py` against `oldleader`, not the arena pool, is the discriminating fixture.** We lose 4/4
to `oldleader` (a real top player who reacts, margins −$4,268 to −$8,982) but beat Seb's own tape by
+$98,483 on one seed — the tape we copied our schedule from is not a hard opponent. The 94.4%
arena-pool figure and the non-discriminating handover fixture should never be read as "we're close";
gate future selling changes on `vs_tapes.py`/`oldleader`.

Opening-vs-tape test: our planner from day 0 wins 0/6 (mean $47,756); tape opening + our agent from
day 11 wins 4/6 (mean $67,181).

## 9. Open items, collected

- Re-confirm `LATE_SELL_BIAS` on a wider seed set (the 12.5pp win-rate gain is real on 8 seeds, not
  yet reconfirmed against a current pool).
- Re-test `CAP_SELL_OFFER_SIZE` specifically against contrarian, the only opponent that produced an
  over-30 offer in the wider sweep.
- Wire `opponent_net_trade` into the reservation-price call site (§1's `λ_p` formula).
- **Re-run the carrot pool verdict and the geese/EGG measurement now that `c99a8a5` has landed** —
  both were void under SELLABLE.
- Meter milk sell rate or cut cow count toward the field's COW 8/SHEEP 6 — "this is where the ~$11k
  gap is" per the cow-count-is-causal finding above.
- `FERTILIZER_RESERVE_LOOKAHEAD_DAYS` relaxation is not established as safe; the d16 incident it
  guards against (6/12 FERTILIZE fired) has not been re-tested with a smarter reserve.
- Field-sweep `LATE_SEASON_PAIR` (currently −$370 on one seed, inside seed variance) to a decision.
- Fill the DIG-to-replant chain, but only after the partial-one-shot-harvest fix lands first.
