# The carrot window is d25-d27, and it is three days wide

2026-08-21.
Measured on the melon, strawberry and q4 tapes, and on seed 11 head to head.

## The question

Alex: *"how can we perturb kawa and add carrot without breaking stuff in the back half"*,
*"i am thinking on carrot friendly towns throw in some carrots in the backend instead of wheat"*.

The replay is exact for all thirty days, so the search space is no longer "which plan".
It is "which single op of his do we change", which is small enough that a win is attributable.

## The instrument

`kagg/search/tape_edit.py` rewrites ops inside a replayed opening and hands it back through
`EMBEDDED_OPENINGS`, a seam the submission bundler already uses.
Nothing ships as a flag.

Three environment facts constrain every edit, and all three are in the module docstring:

- **PLANT carries no coordinates.** The unit plants where it stands, so an edit can name the *n*th
  plant of a day and nothing finer.
- **Atomic PLANT is per crop** (`reference/kaggriculture.py:920-931`). A turn may mix
  `PLANT WHEAT` and `PLANT CARROT`, and each needs its own seed, which is why the edit has to move
  the `BUY_SEED` order and not merely relabel the op.
- **Ten market orders a turn**, and the eleventh is truncated silently
  (`reference/kaggriculture.py:551`).

`surplus_sells` offers shed stock his own order does not ask for.
Without it a crop he did not grow is never offered and sits in the shed to the final bell.
It is written to be silent on any turn he already covers, and that is measured, not asserted:
the control arm banks **$96,198 with the wrapper and $96,198 without it**.

`tests/test_an_edited_tape_sows_what_it_bought.py` holds the operator: 6 tests, all green.
Backing out `repoint_seed` turns the seed assertion red, so it is load-bearing.

## What the first sweep measured, and why it was wrong

Windows chosen from the archive — 2,430 of 2,702 winning seats sow their first carrot on d21-d22 —
so the first pass swept d18 to d28.

    seed 11, kawashigi opponent, live shops, weeds 0.005

    control                          $96,198
    carrot, 2 tiles/day, d20-d25     $89,411      -$6,787   for twelve tiles

$566 a tile is far more than a wheat crop is worth, so the loss is not crop economics.
It is lifespan.
`reference/kaggriculture.py:224` gives WHEAT `planted + 5` days and CARROT `planted + 4`, and
`:759-766` removes a yield unit every two steps past that and turns the tile into a **WEED**.

    day        18   19   20   21   22   23   24   25   26   27   28   29
    weed ctl    1    2    5    9    9    9   10   10   11   10   24   25
    weed arm    1    2    5    9    9    9   12   14   17   16   31   32
    money ctl  406  506  521  550  588  672  675  752  775  794  852  961   (hundreds)
    money arm  406  506  521  550  587  671  674  751  774  785  828  891   (hundreds)

Seven extra weeds, and the whole gap lands in the last two days' harvest.
Total PLANT ops are **203 in both runs**, so nothing was dropped by the atomic rule — the plants
went in and then died standing.

## The measurement that fixes it

The right question is not when winners plant carrot.
It is which of *his* tiles are lifted inside four days.
Read off the dawn boards of all three tapes, grouped by the day the tile was sown:

    sown          melon q3          straw q3          q4
    d0 .. d24     5 days, all       5 days, all       5 days, all
    d25           4 days   (7)      4 days   (9/11)   4 days  (14)
    d26           3 days   (9)      3 days  (11)      3 days   (5)
    d27           3 days  (11)      3 days  (12)      3 days  (10)

He is not being careless.
He sows on a five-day cadence the whole season and the final bell truncates the last three sowings.
**Those three days are the entire carrot window** — 27 tiles on the melon tape, 32 on the
strawberry, 29 on q4.
On them a carrot reaches its max yield (4 units at `max_yield_day 3`) where the wheat is cut off
before its own (6 units at `max_yield_day 4`).

## What the narrow window scores

    seed 11, kawashigi opponent, live shops, weeds 0.005

    arm                        bank        delta    weeds   plants
    control                  $96,198          +0       25      203
    carrot, all of d27       $96,139         -59       25      203
    carrot, all of d26-d27   $96,073        -125       25      203
    carrot, all of d25-d27   $95,807        -391       25      203
    tomato, 1 tile d12-d15   $95,758        -440       27      203

The weed count returns to the control's 25, so the mechanism is gone.
The loss collapses from $6,787 to $59.

**This is one seed and one town, and it is not the town the arm was built for.**
Seed 11 has no carrot drain.
CARROT drains at or above WHEAT on 4 of 16 towns measured earlier — seeds 1337, 4096, 13001, 60013 —
and those are where the arm has to be judged.
The sweep across those towns and three opponents is what runs next.

## The eight-town run, scored twice, and the two scorings disagree

Twelve arms, eight seed-drawn towns, `kawashigi` seat 1, weeds 0.005.
`mean money` is our bank against the control's.
`mean margin` is `(ours - theirs)` against the control's `(ours - theirs)`.

    arm                    mean money mean margin   wins
    control                        +0         +0    4/8
    carrot2_d25d27                -92       -105    4/8
    carrot_d26_all               -110       -126    4/8
    carrot_d25_all               -206       -258    4/8
    carrot4_d25d27               -293       -317    4/8
    carrot_d27_all               -300       -302    4/8
    carrot_d26d27_all            -439       -458    4/8
    carrot_d25d26d27_all         -869       -957    4/8
    carrot2_20_26               -3239      -3770    4/8
    tomato1                     +4846      -5546    4/8
    tomato2                     +4455      -8633    4/8
    tomato3                      +286     -11579    4/8

**Tomato is +$4,846 on money and -$5,546 on margin.**
The two columns have opposite signs, and the margin column is the one the ladder pays.
This is the `Select on win rate, not money` lesson in `CLAUDE.md`, arriving in the most expensive
possible form: an arm that looks like a $4.8k win in every table that does not print the opponent.

The mechanism is the wheat book.
The tomato arm plants four fewer wheat tiles, so we put less wheat into the market.
Seed 42, market inventory at d29: **WHEAT 9,532 with tomato against 9,647 in the control** -- 115
units we did not add.
Lower inventory is a higher price, for both seats, and he sells far more wheat than we do:

    seed 42       ours      theirs     margin
    control     70,443      74,451     -4,008
    tomato1     91,960     112,652    -20,692

We got $21,517 richer and $16,684 further behind.
Planting less wheat is a transfer to the opponent, not a gain.

**No arm changed the win count.** Control is 4W-4L and so is every one of the eleven arms, on the
same four seeds. Nothing here is worth shipping.

## The sample is eight towns, and that is not enough

**CORRECTED later the same day:** the town unlocks **eight** shops, at d3, d6, d9, d12, d15, d18,
d21 and d24, drawn **with replacement** from eight types -- カワシギ's own town draws SMOOTHIE_SHOP
four times. So the space is 8**8, about 16.7 million draws, not seventy, and enumeration is out.
These eight towns were drawn by seed, four of them picked *because* they drain carrot, which biases
the carrot arms upward if anything.
`breakdown.run` takes an explicit `shops` argument, so the town can be enumerated directly instead
of sampled. That is the correct instrument and it is what runs next.

## Not established

- Whether any town makes the carrot arm positive. On seed 11 it is a small negative.
- Whether the opponent moves it. Only `kawashigi` seat 1 has been run.
- Tomato. One arm on one seed, -$440, with weeds up 2. Not a verdict.
- Geese. Held back on instruction, and the old goose verdict is void anyway because it was measured
  while `SELLABLE` blocked EGG.

---

# What the 3,648-season town grid found, and what it could not see

Added 2026-08-21, later the same day.
48 sampled towns x 19 opponents x 4 arms, scored on margin, raw rows in
`data/logs/town_arm_grid_rows_2026-08-21.csv`.

## Carrot pays, but only on a carrot town, and the band is narrow

Pooled, the full carrot arm is -$370 and looks like every other null.
Split by the town's CARROT drain it is not:

    carrot_d25d26d27_all   CAdrain  towns  mean dmargin   median   win%
                                 0     10        -2133    -1774    26%
                                 1      9        -1443    -1353    25%
                                 2     11        -1845    -1726    37%
                                 3      3         -381     -390    23%
                                 4      7         -460      -94    35%
                                 5      5          -43     +369    49%
                                 6      3        +1937    +1714    40%

    best towns   town24 +3990  CA6 WH4 MI4 ST3 TO2      worst  town30 -3484  WH8 MI5 TO4 EG3 ST3
                 town28 +2049  CA6 WH5 ST5 WO2 EG2             town34 -3340  WH7 MI4 ST3 EG3 TO2

The two best towns are the two `CA6` towns; the three worst are `WH7-8`/`MI5` towns with `CA1-2`.
Drain 6 is **11% of towns** on the true draw distribution (drain >= 4 is 36.7%), so a conditional
rule would fire on about one game in nine and is worth roughly **+$210 per game in expectation**.
It rests on 3 towns and 57 seasons. Thin.

## Tomato is dead at every drain level

    tomato1   CAdrain 0..6   -4731  -3847  -7040  -861  -4591  -5773  -675

No band is positive, and against the mirror its win rate is 2%.

## The herd

    arm                 dmargin   wins    wool6    wool2      dry      dry
    herd_cow_d8           -1048   5/12    -4718     +225     -103     +403
    herd_sheep_d8        -19651   1/12   -26552    -5473   -37736    -8844
    herd_counter_d8      -13217   3/12   -19261    -3317   -24196    -6094
    herd_counter_d12       -808   5/12    -3230       +0       +0       +0

The `d12` rows read `+0` on three towns because the herd is already bought by then.
`herd_cow_d8` is **not** a test of "more cows": on a dry town `_herd_split` has already taken cows
to their cap, so the arm has nothing to change, and it only bites on wool towns where sheep was
deliberate. `herd_cow_d0` measured -$54k to -$88k, which is not a measurement either -- it
overwrites his opening, `SHEEP SHEEP SHEEP COW COW` on d0 in 78 of 78 games.
`tape_edit.herd_shift` replaces both: it moves a BOUNDED number of heads after d0, so the control
sits at delta = 0. First reading, one town, one opponent: **+4 cows -$34,089, -4 cows -$9,459** --
a local optimum in both directions.

## Two coverage failures, both invisible until instrumented

**The q4 tape never armed.** 0 of 76 combinations, so 3,648 seasons and the whole herd probe ran on
the melon and strawberry tapes only -- and q4 is the tape that leans hardest on animals.
`q4_branch.DECIDE_BY_DAY = 5` needs a YARN_STORE in the **d3** slot, and uniform town draws put one
there rarely. Fixed by `stratified_towns`, which forces a third of towns to a d3 yarn store; the
grid now logs the armed tape on every row.

**The opponent pool spans rank, not behaviour.** Ranked by leaderboard it came out 7 cow-leaning to
2 sheep-leaning, with the three strongest sheep players absent (StackKnight 6/12 rank 29, Bruce
6/12 rank 38, Eddy Despradel 6/8 rank 45), carrot bunched at 0-14 with one outlier at 60, and
tomato zero for eight of ten. So the herd arms were judged against a cow-heavy field and the crop
arms against a field that barely contests those books. `BEHAVIOUR_SPAN` in
`scripts/town_arm_grid.py` is the replacement: cow 3-10, sheep 3-12, carrot 0-60, tomato 0-22.

## Timing is closed

Five independent ways, all negative. Moving the day's sale to a fixed hour loses $4,698 (h23) to
$26,601 (h0) -- a single order can only sell what the shed holds at that instant, so the rest of the
day's harvest goes unoffered. Adding an order without removing his is a wash (-$185 to -$236 at
h8/h12/h16/h20), and from d0 rather than d20 it is -$66,798. The intraday WHEAT price range is
**under 2%** (42.4 to 43.2) and holds in the mirror. No top-six agent sizes an offer against the
book (median r ~ 0). Against that, the SEASONAL gradient is WHEAT +81%, STRAWBERRY +58%, MILK +30%
and WOOL **-98%** -- the day and the product matter, the hour does not.
