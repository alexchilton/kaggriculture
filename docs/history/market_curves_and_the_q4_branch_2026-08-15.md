> Note added 2026-08-22: section 7's q4-branch number (+$465 mean, "not shippable") is a rougher
> precursor to `docs/q4_variant_first_draft_2026-08-15.md`, which isolates the routing handicap from
> the parcel+herd cost on a proper `shipped_live` baseline and gets -$716 mean, not distinguishable
> from zero. Prefer that file's number for section 7's question. Sections 1-6 (the market-curve
> tables) are unaffected and still the reference for this topic.

# The market curves, and what they say about allocation

Written 2026-08-15.
Everything here is computed from `reference/kaggriculture.py` or measured with one OS process per game.
Where a claim is one seed, it says so, because a single seed turned out to be worth almost nothing.

---

## 1. The shared book is the whole game

`_process_market` reads ONE market object off player 0's observation and drains it per unit in
lockstep between both seats (`reference/kaggriculture.py:544-547`).
Every unit the opponent sells lowers our price.
Prices are therefore a race, not a private resource.

`FEED` consumes exactly 1 WHEAT per animal per day, taken from the shed
(`reference/kaggriculture.py:505-512`), so wheat is a consumable as well as a product.

## 2. Every product's price curve, computed

Price as a function of book position, where negative means the town has eaten more than both farms
grew:

```
  surplus   WHEAT  CARROT  TOMATO   STRAW   MELON   MILK   WOOL    EGG
    -1200      60     906   5,004     411     312    461    261
     -800      53     267   1,884     358     309    406    257
     -400      45      66     300     288     303    334    251
     -100      35      43      72     204     290    247    240
       +0      25      35      60     120     250    160    200     50
     +100      21      23      35       1     150      1      1     42
     +200      21      19      24       1       1      1      1
     +400      20      12       9       1       1      1      1
    +1000      19       1       1       1       1      1      1     38
```

Three structural facts fall straight out of this.

**Wheat cannot be crashed, but it can be halved.**
Its whole downside is $25 to $19 even at +1000 surplus.
But the range actually in play is $21 (surplus) to $47 (deficit), and we grow ~800 units into that
book, so growing more wheat really does cost real money per unit.
"Monotonically safe" was wrong; "never goes to $1" is what is true.

**TOMATO and CARROT are the only two crops with a `hinge` undersupply curve**, which is quadratic
past `u = x/T > 1`.
Tomato at -400 deficit is $300, at -800 it is $1,884, at -1200 it is $5,004.
That, and not yield, is why tomato is "viable in ~50% of games": the top players grow zero tomato
across 40+ recorded games, so the supply side is empty by construction and the price is whatever the
shop draw makes it.
Melon is the opposite -- `log` on the upside, so it never spikes.

**EGG is the only animal product that cannot be crashed.**
Milk decays linearly and wool decays quadratically; both reach $1 at about +100 surplus.
Egg decays logarithmically and holds ~$38 at +1000.

## 3. When the books actually crash

Seed 3, contested, both seats shipped:

```
 day    MELON   STRAWB   TOMATO   CARROT    WHEAT
   0      250      120       60       35       25
  10      271      181       61       36       36
  13       94      195       62       36       40
  20       96      216       62       37       45
  26      111      147       63       38       42
  29      118       59       63       40       41
```

**Melon is a three-day race, d11 to d14.**
It climbs to $271 because the town eats it before anyone harvests, then both farms' melon lands and
it falls to $81.
Sell on d10-d11 and get $250+; sell on d14 and get $81.

**Strawberry peaks at $216 on d20** -- 80% over base, and worth more than double melon from d15 --
then collapses to $59 over the last six days as our own harvest lands.
We sell our best product in its worst week.

Melon recovers late (to $118 by d29) because its decay is `sq`: 10 units of town drain buys back $24
a unit near the top of the surplus.

In replay `93372504`, WOOL floored on **d16** at +59 surplus and MILK on **d24** at +76.
Our 10 cows against their 8 changed nothing -- both books died for both seats.

## 4. Which seeds want which crop

Both seats grow no tomato and no geese, so these columns are the town's appetite alone.
Scanned with real agents, because the shop draw comes off the same RNG that weed spawning consumes.

```
 seed  TOMATO d29  CARROT d29  EGG d29   shops by d6
    5          83          63      120   FARMERS_MARKET,BRUNCH_SPOT
    7          64          32      305   BRUNCH_SPOT,BAKERY
   11         216          75       75   FARMERS_MARKET,BAKERY
   15         356          62       59   FARMERS_MARKET,ICE_CREAM_SHOP
   16          72          40      211   BRUNCH_SPOT,BRUNCH_SPOT
```

`YARN_STORE` unlocks by d6 on **15 of 100 seeds**: `[3, 10, 17, 18, 22, 45, 47, 53, 60, 65, 66, 73,
79, 82, 95]`.
Shop frequencies in the first 7 days: BRUNCH_SPOT 28%, BAKERY 27%, PET_CAFE 26%, ICE_CREAM_SHOP 25%,
FARMERS_MARKET 21%, PIZZA_SHOP 19%, SMOOTHIE_SHOP 19%, YARN_STORE 15%.

## 5. The season is chaotic, and single-seed deltas are worthless

The sim is deterministic -- the same baseline run twice on seed 3 gave $133,221 both times.
Deterministic is not the same as well-conditioned.

- Swapping ONE sheep for ONE goose moved our bank $82,953 -> $105,738 and the frozen opponent's
  $82,615 -> $119,462 on one seed. One sheep is ~8 wool units a season.
- In a 38-config sweep over 14 seeds, **seed 8 gave 37 of 37 configs a median +$24,368** and seed 20
  gave only 8 of 37 anything positive, median -$9,523.
  Those two seeds drove the entire table.

Any harness must therefore average many seeds, resample them, and never read one row.

After removing those two seeds, two configs survive with a consistent sign:

```
config                    mean w/o 8,20      sd    seeds up
STRAWBERRY->WHEAT x4          +$3,647     5,366     9/12
WHEAT->MELON x2               +$2,499     2,597    10/12
```

Melon up, strawberry down -- which is what the curves in section 2 predict, and what Kawashigi's own
four-quadrant games run (MELON 20 / STRAWBERRY 34 against our 12 / 41).
Neither is confirmed on win rate.

## 6. Geese are UNMEASURED, not dead

`HERD_GEESE` exists at `schedule_agent.py:3583` and is 0.
Its 2026-08-11/12 negative verdict predates the `SELLABLE` fix (`c99a8a5`, 2026-08-13) that first
allowed EGG to be sold at all, so that verdict measured birds whose product could not be sold.

Two defects in the knob, found today and unfixed:

- `HERD_GEESE >= 2` returns a herd of **13** where 0 and 1 return 14 -- the second conversion places
  its goose and loses the animal it replaced.
- It saturates at 2 geese; `HERD_GEESE = 4` is byte-identical to 3.

Eggs do now sell: one goose sold 51 eggs, and the egg book finished at **$95 with a 445-unit
deficit** -- nine more geese would not have filled it.

A pool run gave geese 0 at 89.1% win and geese 1 at 88.5%.
**That result is not evidence.**
Five of the six opponents were saturated at 100% in both arms, so the entire difference rested on 16
mirror games and amounted to half a game.
A discriminating test needs opponents we do not already beat every time.

## 7. The four-quadrant branch

Kawashigi's four-quadrant tape (`91907974`) extracted to `data/seed_scripts/kawashigi_q4/`.
Composed with our shipped tape at **d9**, the first day the two disagree, into
`data/seed_scripts/kawashigi_q4c/`.
Through d8 they are the same plan, so the opening cannot regress by construction.

```
land bought d6, d11, d12   -> quadrants unlock d7, d12, d13
herd COW 6 / SHEEP 12 = 18 -> against our COW 10 / SHEEP 4 = 14
202 tile-plantings, 12 hands
```

It runs: on seed 3 it buys the fourth quadrant on d13, builds COW 6 / SHEEP 12, and banks $148,406
against $133,221.

**Run on every seed it LOSES**: mean -$2,749, median -$5,286, 5/14 seeds up, wins 4/14 against
q3's 5/14.
That is the expected result for a branch that should fire on ~15% of games.

The unexpected finding is that `COW 6 / SHEEP 12` appeared on **only seeds 3 and 10 -- exactly the
two YARN_STORE seeds in that set**.
`WOOL_SHOP_SETS_THE_HERD` is already reading the yarn draw by itself.

Measured directly on the SHIPPED q3 arm, to pin down how much of the package already exists:

```
armed seed 17    COW 6, SHEEP 8    (14)
unarmed seed 5   COW 10, SHEEP 4   (14)
```

So the shipped agent already shifts sheep-ward on an armed seed, but only to **6/8**.
The q4 tape reaches **6/12** by buying four more animals.
What the tape adds is therefore the parcel, four extra sheep, and the plantings to fill the ground --
not the sheep-ward shift itself.

### Measured on the 15 armed seeds

```
mean +465   median +4,553   sd 11,220   8/15 seeds up
wins:  q3 10/15   q4 12/15
```

Against the same comparison run on an unselected seed set (-$2,749, 4/14 wins), the trigger is doing
its job: a $3,214 swing and the win column flips.
But on the armed set alone q4 is break-even on money -- $465 against a standard error of ~$2,900 --
and +2 wins on 15 games.
Not shippable.

Both arms ran routes live from d9.
That handicaps q4 harder, because it has 100 tiles and 18 animals against 75 and 14, and the solved
routes were built for the three-quadrant board.
A re-solve on the 100-tile board is outstanding and should move q4 only.

`kagg/search/solved_days.py` is backed up to `solved_days.py.q3_backup_2026-08-15` before any
in-place rewrite.

## Open

- q4 measured on the 15 armed seeds, with routes re-solved for 100 tiles.
- Whether the tape's MELON 20 / STRAWBERRY 34 mix survives the agent's own melon/strawberry
  adaptation, which currently overrides it.
- Geese against a field that discriminates.
- Live market prices in `router.BASE_PRICE`, which is a hardcoded table -- `grep market_price
  kagg/search/router.py` returns nothing, so the planner values melon at $250 on d20 while it trades
  at $96.
