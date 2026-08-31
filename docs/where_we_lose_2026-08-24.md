# Third brief: where these games are actually lost

Repo: `/Users/alexchilton/DataspellProjects/kaggriculture`
Release worktree: `.claude/worktrees/e2500`, branch `e2500-shopprice`, commits `00229c8`, `9ffda3c`.
Read `docs/handoff_for_review_2026-08-24.md` and `docs/answers_for_review_2026-08-24.md` first.

You said the game goes wrong at d12. It does not, in this sample. Here is the measurement, the
mechanism I think replaces it, and the two places I am least sure.

Everything below is read straight off recorded ladder replays -- no simulation, so nothing depends
on our agent reproducing anything. `scripts/where_the_game_is_lost.py`.

---

## 1. Six losses. Five of them are one loss, on d29.

`gap` is theirs minus ours, so positive means behind.

    game        margin   gap@d20   gap@d28   d29 swing   their d29   our d29
    98495047   -29,384    +2,221      -542     +29,926      36,941      7,015
    98494953    -3,472    -4,136      -417      +3,889      10,095      6,206
    98428765    -1,783      +779    -1,682      +3,465      11,718      8,253
    98499540    -1,940    -3,530      +506      +1,434       6,954      5,520
    98460892      -614    +2,462      -427      +1,041       5,189      4,148
    98501831    -6,070    +3,929    +6,384        -314       3,885      4,199

We are level or **ahead** at the end of d28 in four of six. The entire margin appears on the last
day, and the opponent out-banks us on d29 in five of six.

98501831 is the one genuine exception -- $6,384 behind at d28, and we gained on d29. If you want a
game where something upstream is wrong, that is the one to read.

A per-day table for 98495047 is in `data/logs/where_lost_98495047.log`. The gap never exceeds
$3,560 across d0-d28. At d12 we are **ahead by $694**.

## 2. The mechanism: the animal book dies mid-season and we are still selling into it

Closing prices, and the first day each product sat under $20:

    game     MILK  WOOL  CARROT  WHEAT | milk<20 from | wool<20 from
    98495047    1     1     498     38 |     d15      |     d15
    98494953   74   158      59     38 |     d20      |     d14
    98499540    1     1      52     44 |     d15      |     d13
    98501831    1     1      54     36 |     d20      |     d19
    98428765  270   144      50     21 |    never     |    never
    98460892    1     1     124     43 |     d20      |     d15

Milk and wool are at $1 by d13-d20 in five of six. They do not recover. Crops do not do this:
carrot and wheat close between $36 and $498 in every game.

This is our own supply -- the town's drain is fixed and small, and we out-produce it. It is the
same finding as the realized-price audit in the previous brief, seen from the other end: our
**price per transaction** is fine (96-111% of theirs) while our **terminal inventory** is worthless.

### The extreme case, and it is the biggest loss in the set

Game 98495047, seed 1640915609, lost by $29,384. Holdings entering d29 (shed plus every hand):

    ours     73 units   $5,607     WHEAT 41, FERTILIZER 14, CARROT 7, MILK 6
    theirs  100 units  $37,842     CARROT 72, WHEAT 11, FERTILIZER 7, MILK 6

    closing book:  CARROT 498   WHEAT 38   MILK 1   WOOL 1

They banked $36,941 on d29 against our $7,015. Roughly 65 extra carrots at ~$450 is the whole
margin. Note they cleared 72 units into that book **without collapsing it** -- it closed at $498 --
so the town had room for both of us.

## 3. Board clearing: real, and not the cause

We leave far more standing than anyone else:

    ours    28-42 units left at the close     worth   $587 - $2,274
    theirs   2- 9 units                       worth    $76 -   $324

But only $380-$1,566 of ours was ever reachable (ripe by d28). Against a $29,384 loss that is
noise. Worth fixing, not worth calling the problem. Our `planted` count tracks theirs closely all
season (56/56 at d12, 61/61 at d19), so "planting too much" is not visible in this sample either.

## 4. What was fixed today, and what it cannot reach

Shipped as `e2500_close.py`, commit `00229c8`. `CRITICAL = 1_000_000` was being added to crop
harvest prizes in the close and, after this morning's shop-price fix, not to pen harvests. Every
crop therefore outranked every pen by six orders of magnitude:

    wheat tile, 3 units, town paying $21    3 * 25 + 1,000,000 = 1,000,075
    cow pen,    3 milk,  town paying $270   3 * 270            =       810

Now both are priced at the live quote with no constant, on d28 and d29
(`router.the_close`). Measured on 24 of our own ladder games, both tapes replayed verbatim to
d28 h0 so the board and book are real, paired against the same games with the change reverted:

    ALL        n=24  mean +$1,199  median +$1,278  better in 20/24
    q3 boards  n=16  mean +$1,445  better in 15/16
    q4 boards  n=8   mean   +$706  better in  5/8

Harness: `scripts/the_close_on_the_real_book.py`. Gate 94.4% over 216 games.

**It cannot reach section 2.** It orders what gets collected on the last two days. It does not
change what we are holding when the last day starts, and that is where the $29,384 was.

## 5. The carrot arm, and why it did not help

`e2500-carrot` (`f1b73c9`) sows carrot on d25-d27 when the town's carrot drain is high. Two gates:

    CARROT_DRAIN_MIN = 5     town drain must be at least 5
    CARROT_OPP_MAX   = 7     opponent must hold at most 7 carrot tiles

Run against the real d25 observations of all six games:

    game       drain  fires?  opp carrot tiles  close CARROT  they held d29    margin
    98495047      11    YES         10               498            72       -29,384
    98460892       6    YES          2               124             6          -614
    98494953       2     no          0                59             0        -3,472
    98499540       2     no          0                52             0        -1,940
    98501831       2     no          0                54             0        -6,070
    98428765       3     no          0                50             0        -1,783

Four of six are not carrot towns and the drain gate correctly stands down. On the one game where
the drain qualifies, **`CARROT_OPP_MAX = 7` blocks it at 10 tiles.** So `e2500 + carrot` would have
played the $29,384 loss identically.

The crop calendar says the instrument is capable: CARROT is `first_yield_day 2, max_yield_day 3,
max_yield 4`, one-shot. Sown d25 it is full by d28. 72 units is ~18 tiles.

So my reading is that the gate's **sign** is wrong, not its threshold: it treats an opponent holding
carrot as evidence the book is taken, when in a drain-11 town it is evidence the book is rich. But
this rests on **one game**, and the check exists because two sellers collapsing one book is a real
failure mode. `CARROT_DRAIN_MIN = 5` has 12,096 seasons behind it; `CARROT_OPP_MAX = 7` does not,
as far as I can find.

## 6. What I want from you

1. Is "terminal inventory in the surviving product" the right frame, or is the real error earlier --
   that we keep animals producing into a book we killed at d15? Those imply very different fixes.
2. Is there a principled rule for when to STOP selling a product, as opposed to sizing the order?
   `LIQUIDATE_FROM_HOUR`, `CAP_SELL_OFFER_SIZE`, `HOLD_A_FLOORED_BOOK` exist and are barely tuned.
3. `CARROT_OPP_MAX`: tune, invert, or delete? What result would convince you either way?
4. Read 98501831 -- the one loss that was already gone by d28. Is it a different failure or the same
   one earlier?

## 7. Reproducing

    python -u scripts/where_the_game_is_lost.py 98495047
    python -u scripts/what_the_endgame_left_behind.py data/seed_scripts/losses/98495047.json
    python -u scripts/the_close_on_the_real_book.py 98428765 --handover 28
    python -u scripts/the_close_on_the_real_book.py --dirs ladder_2026-08-17b --limit 24

Replays are in `data/seed_scripts/losses/`. **These are selected losses** -- never compute a win
rate from them. Prices are endogenous: the same seed that paid $270 for milk in the recording paid
$1 in our rematch, which is why every measurement above replays both tapes rather than re-simulating
from turn 0.
