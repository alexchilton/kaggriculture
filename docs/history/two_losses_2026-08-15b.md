# Two more losses, 2026-08-15: 93286476 and 93285579

Read off the recordings only. No simulation, so nothing here is a harness artifact.
Volumes are **fills** (shed decreases), never offers.

    93286476   LOSS   us $78,254  vs  Light      $79,216    -$962      seat 0
    93285579   LOSS   us $56,805  vs  Mutte1904  $63,697  -$6,892      seat 1

They are two different losses and must not be pooled.

---

## 1. Animals: the feed fix holds

Tracked every animal tile, every turn, both seats, both games.

    93286476   US  animals lost mid-season: 0      THEM: 1  (SHEEP, d29 h00)
    93285579   US  animals lost mid-season: 0      THEM: 1  (SHEEP, d29 h00)

Zero starvations on our side in either game.
The d9/d10 stranded-FEED defect is closed in live play, not just on the grid.

## 2. Sheep: the problem is confirmed again, and it decided neither game

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

## 3. Melon: we sell it faster than they do, we simply have less of it

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

## 4. 93285579: TOMATO closed at eleven times base and neither seat grew it

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

## 5. 93286476: we led on bank AND field at d28, and lost anyway

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

## 6. Killed here: "we dump in one hour and they spread the sale"

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

## What this changes

1. The last-day conversion item stays open and is now **two** games with the total-value table
   behind it, not one game with a bank number.
2. `SHOP_ADAPT_HERD` stays the next fix, unchanged, but these two games are not its evidence.
3. Tomato moves up: a board drained 895 units of a product on the hinge curve and nobody supplied it.
4. Melon output, not melon timing.
