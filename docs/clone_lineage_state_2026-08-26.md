# Clone lineage, state at 2026-08-26 end of day

Written because most of this session's measurements were void and the reasons must not be
re-derived tomorrow.

## The headline

**The old `e2500` line beats today's clone-lineage candidates in controlled local play.**

    local, same draws, same opponents, same seed
    draw 98818687   e2500 105,575   B 103,143   A  94,363
    draw 98818694   e2500  70,981   B  62,795   A  62,110

**Ladder scores must NOT be compared across dates.** Alex, 2026-08-26: *"the leaderboard moves,
2500 was scored highest 2600 but now not more than 1600 ish; the 1997 also is around the same now
at 1600; the board got harder."* The rating is Elo against a live field that keeps improving, and
each submission's number reflects a different number of games against a different field. So this
table is a record of what each artifact peaked at, NOT a ranking:

    peaked   settled   artifact                  submitted
    1991.9   ~1600     main.py                   2026-08-25
    1779.8     ?       e2500_shopprice.py        2026-08-24
    2600     ~1600     the e2500 line            2026-08-24
    1628.0     ?       e2500_carrot.py           2026-08-24
    1271.6     ?       main_baseline.py          2026-08-26

The 720-point "gap" between today's artifact and the best-ever number is therefore not a measured
regression -- it is two numbers taken against different fields at different times. **Only the
controlled local head-to-head above supports a comparison**, and it still favours e2500.

`e2500_shopprice.py` scored 1779.8 and **was never committed** -- it is not on disk and not in git.
Only `e2500_carrot.py` (1628.0) survives, recovered from commit `3003141`. The branch
`e2500-shopprice` still exists and could rebuild it.

## Three harness defects, each of which invalidated everything measured through it

1. **The tape played a clone of itself.** `tape_policy(replay, team, seat_wanted)` resolves `seat`
   for 0 and `1 - seat` for 1 (`breakdown.py:318`). Seven files passed 0 for BOTH seats. The same
   orders hit the book twice, so prices moved differently from the recording and the replay drifted:
   $3 on d0 became two silently failed wheat buys on d2 and 5 crops plus $782 by d12. With the real
   opponent the replay is EXACT -- money identical to the dollar d0-d12, board identical d0-d8, the
   only difference one weed spawned at d9 (`weedSpawnChance 0.005`, and recordings carry
   `seed: None`, so it cannot be reproduced). Fixed in 63b0567.

2. **The kawashigi branches replaced the schedule mid-season.** `melon_branch.install()` swapped the
   ENTIRE schedule for an embedded row set (`B3_ROWS_B64`) whenever the opponent showed enough melon
   at d3; `q4_branch` did the same to rows 9-29 on the yarn store at d6. So the agent played
   kawashigi's season while being measured against the clone tape. d12 of `clone_open`:

       running row (B3)              the arm's own row
       buys   {WHEAT: 9}             {}
       sells  {FERTILIZER 28, MILK 6} {FERTILIZER 39, WOOL 11, MILK 6, STRAWBERRY 4}
       plants [W,W,STRAW,W,STRAW]    [WHEAT] * 3
       feeds/cares 14/14             15/15

   Deleted in 1a6d534, 1,570 lines. This shipped: `main_baseline.py` carries `B3_ROWS_B64`.

3. **A baked table overrode the parameter under test, twice.** `_STOP_TABLE` shipped
   `{yarn3: 28, yarn6: 20, open_yarn_seen: 20, open_no_yarn: 12}` and the epilogue reads
   `stop = _stop(...) if _STOP_TABLE else _ARM_STOP[arm]`. It clamped the handover SWEEP (three of
   four rows byte-identical at d20/d24/d28, which read as a plateau) and it clamped the ARTIFACT
   (a bundle built `--replay-days 29` handed over at d12/d20). Draw 98818687, same seed and
   opponent: pure tape 95,776, d28 handover 93,751, the "d29" bundle 85,757. Emptied in e005fc8.

## What is measured and stands

**The planner loses on every day it plays.** 21 shop draws across 8 of the 9 yarn classes and all
three arms (`data/logs/handover_all_draws.log`): d28 is the best handover on EVERY draw, and the
tape with no planner beats it on every draw, by **$870 to $2,648**.

**The tape choice is the bigger lever.** Swapping the default arm's tape is worth up to **+$10,769**
on a single draw, where the entire planner-vs-tape gap is under $2,700.

**The default arm carries 72% of games** -- 87 of 120 draws, every class from d9 to `never` -- and
was the worst-chosen of the three. `98907591` (100,149) against `98884730` (141,250), same author.
Head to head on 14 draws across every class it serves: **proposed better on 13/14, mean +$3,028**,
best +10,769 (d21), worst -5,417 (d18).

**One arm was cloned from a MIRROR.** `98857364` has both seats sending identical actions on all 719
turns and both farms ending on 134,682; margin 0 is the tell. 10 of 120 recordings in
`daily_2026-08-26` have it. Replaced by `nao.kwmr / 98921350`, class-best real game, 133,792 on a
margin of 14,372.

**Seat 1 is slightly worse than seat 0**, about -$250 to -$280 (~0.4%) on two draws, consistent
direction -- the market slot ordering. Every sweep today used seat 0, so those numbers are
marginally optimistic.

## Why the nine-slot tape table does NOT work

A tape can only be switched to at a turn where it still agrees with what has been played, and the
yarn signal for class X arrives the day before X. So splitting off `d24` needs the last two tapes to
agree to d23h23. Measured over 110 usable recordings, tapes sharing one identical opening:

    d2h23  73     d5h23  53     d8h23  29     d11h23  9     d14h23  7     d17h23  1

The nine best-BANKING tapes are not prefix-compatible -- `d18` parts from `d3` at d0h23, before the
first decision point. Selecting on bank alone ignores the constraint that binds. Constrained
selection gives:

    splits at [3]      2 arms   mean bank of chosen tapes 134,165
    splits at [3,6]    3 arms   mean 134,041     <- the shape to ship
    splits at [3,6,9]  4 arms   mean 120,154     <- only a weak d9 candidate qualifies

So three arms is right, and the gain is in WHICH tapes fill them, not in more of them.

## Artifacts -- what is safe to pick up

    submission/main_restA.py   yarn3 98889302 | yarn6 98921350 | open 98907591   built, unmeasured on ladder
    submission/main_restB.py   yarn3 98889302 | yarn6 98921350 | open 98884730   built, unmeasured on ladder
    submission/e2500_carrot.py recovered from 3003141, scored 1628.0             the comparator

Both candidates replay d0-d28 and plan only d29, carry `_STOP_TABLE = {}`, and are kawashigi-free
(all remaining mentions are comments; zero live code).

**Do not pick up `main_baseline.py`, `main_perarm*.py`, `main_replay*.py`, `main_split*.py`,
`main_d28.py` or `main.py` expecting the clone lineage** -- they all carry the deleted branches.

## Why e2500 beats a tape replay -- and why the latch keys on the wrong signal

Alex asked whether the tape "screws up somehow on the replay". It does not. The same tape
(`98884730`) replayed on its own game and on two foreign draws sends BYTE-IDENTICAL orders with
identical no-op rates -- nothing refused, nothing blocked:

    order          sent   no-op        (all three draws)
    BUY_ANIMAL        7       0
    BUY_LAND          2       0
    BUY_PRODUCT      37     0-1
    BUY_SEED         39       0
    HIRE            282       0
    SELL            581   29-32

    final bank    HOME 138,131    FOREIGN never 109,940    FOREIGN d15 64,305

$73,826 apart with identical execution. The loss is entirely PRICE, and it tracks what the town
eats. `_town_consume` walks `unlocked_shops` and drains inventory per product:

    HOME     138,131   STRAWBERRY 6  MILK 5  WHEAT 5  TOMATO 2  WOOL 2  CARROT 1  EGG 1
    never    109,940   WHEAT 7  MILK 5  STRAWBERRY 3  TOMATO 3  EGG 2  CARROT 2
    d15       64,305   CARROT 4  WHEAT 3  STRAWBERRY 3  MILK 3  EGG 2  WOOL 2  TOMATO 1

That tape is a STRAWBERRY season. Its home town drains strawberry hardest; the d15 town halves it
and eats CARROT most, which the tape barely grows. So the tape sells into a town that does not eat
what it grows, and an agent that reads the live book (e2500) beats it there.

**The latch keys on the wrong signal.** We split arms on `YARN_STORE`, and yarn affects WOOL only --
2 units of drain out of ~22. The drain profile for strawberry, wheat, milk and carrot is what
decides the season and our decision tree cannot see any of it. That is why the `open` arm carrying
72% of draws performs so unevenly: those 87 draws have wildly different drain profiles and are
treated as one class.

The fix is cheap: `town["unlocked_shops"]` is in the observation from d0, so the drain profile is
readable immediately -- no waiting for a yarn signal at d15. Key the tape on which products the town
eats, and pick the recording whose crop mix matches.

## The tape corpus is exhausted as a source of default-arm gains

Every prefix-compatible non-yarn3/6 tape was replayed on 7 draws, one per class the default arm
serves, against each draw's real opponent, seed 123641874.
53 tapes completed all 7 (`data/logs/tape_full_sweep.log`, rows in `tape_full_sweep.csv`).

    current default   98907591  UjjwalPardeshi     105,158
    best single tape  98900762  G!vIOne            109,245    +4,087
    ORACLE, perfect per-draw choice over 53        110,580    +5,422
    e2500                                          111,697    +6,539

**A perfect split of the whole corpus loses to e2500 by 1,117.**
So "split more often" cannot be the answer, and no number of extra recordings changes that.
Splitting is worth only **+1,335** over picking the single best tape, and that is with foresight we
do not have at d3.

The corpus is also far less diverse than 53 suggests.
Whole blocks replay to within $200 of each other -- `98871034 / 98893887 / 98864187 / 98884743 /
98903047` give 104,4xx, 111,2xx, 134,3xx on the same three draws.
It is roughly six distinct seasons recorded many times.

**Selecting a tape by its own recorded bank does not work**, and the earlier 8-candidate pass did
exactly that.
Own bank against replayed mean: 98873431 banked 121,922 and replays 1st of the nine; 98884730 banked
141,250 and replays 3rd; 98832334 banked 134,469 and replays 8th.
The home bank is a number about the tape's own town.

### The one split that separates anything is CARROT, not YARN_STORE

Oracle minus e2500, per draw:

    draw        class   top drain     oracle    e2500       diff
    98818694     d15    CARR,WHEA     65,773   70,981     -5,208    <- carrot
    98832395      d9    WHEA,CARR     99,796  110,542    -10,746    <- carrot
    98818687     d24    STRA,WHEA    105,497  105,575        -78
    98818709   never    WHEA,MILK    112,306  112,826       -520
    98846100     d18    WHEA,STRA    140,824  143,373     -2,549
    98820898     d12    WOOL,STRA    107,150  103,692     +3,458
    98832334     d21    WHEA,STRA    142,713  134,892     +7,821

Both draws where CARROT is in the top-2 drain are e2500's two biggest wins.
Remove those two and the oracle tape split **beats** e2500 by a mean of 1,626.
The surviving comparator is named `e2500_carrot.py`.

CARROT is in the top-2 drain on **26 of the 87 default-arm draws (29.9%)**, so this is not a corner
case.
Top-2 drain frequency across those 87 draws: WHEAT 73 (83.9%), STRAWBERRY 46 (52.9%), CARROT 26
(29.9%), MILK 16 (18.4%), WOOL 5, TOMATO 5, EGG 3.

**REFUTED the same night.** Tested on 16 held-out draws -- 8 carrot, 8 not, none of the 7 above
(`data/logs/carrot_test.log`, rows in `carrot_test.csv`).
Best single tape `98900762` against `e2500_carrot.py`:

    group     tape     e2500   tape-e2500   tape wins
    CARROT  69,220    74,412      -5,192       2/8
    plain   81,827    87,159      -5,332       2/8

The tape loses by the same amount in both groups.
CARROT separates nothing.
The 2-draw signal was noise.

And the held-out gap is WIDER than the in-sample one, because `98900762` was selected on the 7
sweep draws:

    best-tape vs e2500      7 sweep draws (in-sample)   -2,452
                            16 held-out draws           -5,262    tape wins 4/16

Same winner's-curse effect the project already recorded at +40% in-sample against +12.8% held out.

**Conclusion: no tape split beats e2500 on the default arm.** Not a better default, not yarn, not
drain, not carrot, not a perfect oracle over all 53 compatible tapes.
Across 23 draws e2500 beats the best available tape on 19.
The tape is not losing on a keyable subclass -- it is worse everywhere, by about $5k.
Whatever e2500 does that wins is not in the tape corpus, so the next question is what that is, and
it is not answerable by choosing tapes.

Drain does NOT otherwise pick the winner: the two `WHEA,STRA` draws chose different tapes
(98832334 -> 98960039, 98846100 -> 98951018), and those two tapes are 6,330 apart on each other's
row.

## What is NOT known

- Whether either candidate beats `e2500` over more than two draws. On those two it loses.
- Whether any of today's five planner commits help. None has been on the ladder; the 1271.6
  predates all of them.
- Win rate for anything. Every number here is MONEY on fixed draws with recorded opponents. The
  ladder is Elo, where a $1,000 loss and a $30,000 loss score identically.

## The herd split already ships, and it is what the whole field does

Measured on 110 usable recordings (`data/logs/herd_census.log`), counting `BUY_ANIMAL` orders in the
winner's action stream.

    file            role          yarn   sheep   cow      own bank
    98889302        yarn3 arm       d3      10     6       127,080
    98921350        yarn6 arm       d6      10     6       133,792
    98884730        restB open     d15       4    11       141,250
    98907591        restA open     d15       4    11       100,149
    98900762        best single    d18       4    11        70,006
    98873431        2nd best       d21       4    11       121,922

The yarn arms are sheep-heavy and the default is cow-heavy, so the YARN_STORE latch is already
switching the herd.
Herd against the tape's own yarn day:

    yarn class    n   mean sheep   mean cow    mean bank
    d3           20         10.4        5.7     103,243
    d6           10         10.5        6.3     105,119
    d9            8          5.1        9.8      79,078
    d12           8          5.1        9.8      94,659
    d15          14          4.1       10.9      82,005
    d18           6          4.0       11.0      83,228
    d21           8          3.9        9.0     104,793
    d24           4          4.0       11.0      96,094
    never        32          4.0       10.8      88,833

Yarn by d6 gives ~10 sheep; yarn from d9 on gives ~4-5. A step, not a gradient.
The corpus is two herd families and little else: **66 tapes at 4 sheep / 11 cow, 23 at 10 / 6**, and
19 one-offs.

**This corrects the "the latch keys on the wrong signal" claim above.** That claim measured town
DRAIN, where WOOL is 2 units of ~22, and missed that YARN_STORE is a *herd* signal rather than a
demand signal. The latch is keying on the one axis the field agrees on.

A cow<->sheep swap is NOT expressible as a tape edit. `reference/kaggriculture.py:21`:

    COW    cost 400   first_yield_day 8   interval 2   max_held 6   MILK
    SHEEP  cost 500   first_yield_day 6   interval 3   max_held 6   WOOL

Yield fires on `(day - placed_day - first_yield_day) % interval == 0` (`:822`), so a cow placed on
day P yields P+8, P+10, P+12 and a sheep yields P+6, P+9, P+12. Swapping species moves every yield
day and a tape's HARVEST turns are fixed. A herd split needs two tapes, and the corpus has them.

## Trimming the herd: cows are a wash, the sheep arms are not a measurement

`data/logs/herd_trim.log`, tape 98900762 (SHEEP 4, COW 11), 10 draws, one delta each, cash saved and
nothing else moved.

    arm            mean   vs baseline   better
    baseline     97,000            +0     0/10
    cow8         95,435        -1,564     6/10
    cow6         88,354        -8,645     1/10
    cow4         79,969       -17,030     1/10
    sheep2       25,996       -71,004     0/10
    sheep0        5,270       -91,730     0/10

Cows are bought d4-d10 across six orders and degrade smoothly: trimming them is a wash at best.

**The sheep rows are uninterpretable and must not be quoted as a sheep result.** All 4 sheep are one
order on TURN 0. Cutting it to 2 leaves an extra $1,000 in the bank and still finishes at $26k
instead of $97k -- more cash, catastrophically worse, which can only be the opening desynchronising.
Unresolved whether that is the wrapper shifting market order SLOTS (slot order decides settlement,
`schedule_agent:3062`) or a real property of the tape. It is consistent with the arm latch sitting
at turn 88: the opening is not perturbable.

**Late-game carrots are not expressible as a tape edit either.** An inserted PLANT has no seed
bought, no hand routed to the tile, no water and no harvest, so it would measure the cost of a seed.
That is the `add_land` failure recorded in the global instructions. Carrots need the planner.

## The 53-tape sweep answered a narrower question than I reported

Alex asked whether the 4 sheep / 11 cow herd really suits 70% of shop draws, and whether some tapes
suit some shop systems better than others.
Checking that exposed a selection error in the sweep itself.

The sweep filtered the corpus to tapes whose **own yarn day was not d3 or d6**, meaning to exclude
the two yarn arms.
Yarn day is the herd signal: the census in the section above measures d3/d6 tapes at 10.4 mean sheep
and d9-plus tapes at 4.1.
So the filter removed every sheep-heavy tape in the corpus.

Cross-tabbing the sweep's own 371 rows by herd:

    === how many tapes in each herd class ===
      sheep<=4    53

All 53 tapes in the sweep buy 4 sheep and 11 cows.
The seven draws do span the shop space -- milk sinks 2 to 5, wool sinks 0 to 3 -- but every tape in
the comparison bought the same animals.
The per-draw winner moves around (`98960039`, `98951018`, `98900762`) across a spread of about $6k,
which is noise between near-identical seasons.
That is why the 53-tape oracle bought only $1,335 over the best single tape.

**"No split beats e2500" was measured on 53 recordings of one strategy.**
It is not a statement about splitting.

## Both herds sit in the same prefix family, so both are legal at the latch

Regrouping the corpus by the md5 of the turn 1..88 action prefix -- turn 88 is the shipped
`ARM_LATCH_TURN` -- gives 17 families across 110 usable tapes.
One family dominates:

    family       n   herds inside              yarn days                    mean own bank
    3f557fae    72   4/11 x53   10/6 x19       d3x15 d6x4 d9x3 d12x3 d15x12        90,925

Inside that family:

     sheep  cow   n   mean own bank
         4   11  53         85,072
        10    6  19        107,252

All four shipped arms are in it:

      98889302  yarn3 arm    sheep 10 cow  6   yarn d3
      98921350  yarn6 arm    sheep 10 cow  6   yarn d6
      98884730  restB open   sheep  4 cow 11   yarn d15
      98907591  restA open   sheep  4 cow 11   yarn d15

So a herd switch at turn 88 is already expressible with tapes we hold.
The $22k own-bank gap is **confounded** -- the 19 sheep-heavy tapes are yarn-d3/d6 tapes, so they
played wool-rich draws by construction, and their authors differ.
It is not evidence that 10/6 is better.

What it does establish is that the 10/6 arm has **never been replayed on a default draw**.
The assumption that it loses there is what the yarn latch is built on, and nothing has tested it.

## Why the shop system is a real signal and we latch on only half of it

Shops are demand sinks (`reference/kaggriculture.py:733-740`): every `townShopSellInterval` steps
each unlocked instance drains its listed products out of the market inventory, which is what stops
the price collapsing as we sell into it.
`BUY_ANIMAL` is **not** shop-gated (`:604`, `:679`) -- it needs cash and shed room only -- so the
herd order always lands and the shops act purely on the sell side.

    MILK sinks:  PIZZA_SHOP, ICE_CREAM_SHOP, SMOOTHIE_SHOP     3 of 8 shop types
    WOOL sinks:  YARN_STORE                                    1 of 8

Shops are drawn **with replacement**, one every `townShopUnlockInterval` days, capped at
`MAX_SHOP_INSTANCES = 8` (`:886-891`), so the sink count per product varies widely per draw.
Across the 110 recordings both signals move the herd, in opposite directions:

    MILK sinks unlocked by end of d10   draws   mean cow   mean sheep   mean bank
      0                                    29        7.7          7.1      86,819
      1                                    48        9.3          5.9      86,011
      2                                    25       10.1          5.1     101,862
      3                                     8       11.5          4.0     128,240

    WOOL sinks (season end)             draws   mean cow   mean sheep   mean bank
      0                                    32       10.8          4.0      88,833
      1                                    55        9.2          5.8      92,161
      2                                    19        7.0          9.1      99,378
      3                                     3        6.0         10.0     112,882

**This is correlational and confounded** -- different players on different draws, and a draw with
more shops of any kind drains more of everything, so part of the bank gradient is just shop count.
It is not the experiment.
The experiment is `data/logs/herd_class_on_open_draws.csv`: the same draws, the same opponent, three
tapes of each herd class, swapping only the tape.

The shipped latch reads YARN_STORE, the 1-in-8 signal, and ignores the 3-in-8 one.

## The herd is decided on d3 information, and that is why it cannot be fixed with tapes

### Swapping the whole TAPE at the latch: cow11 wins the default draws

Three 4/11 tapes and three 10/6 tapes, all from prefix family `3f557fae`, replayed on the 27
open-arm draws (`YARN_STORE` not unlocked by d6, so neither yarn latch fires).
Same seed, same opponent per draw, only the tape changes.
`data/logs/herd_class_on_open_draws.csv`.

     milk_end   n       cow11     sheep10      delta  sheep10 wins
            0   4      75,177      71,419     -3,758         1/4
            1   3      70,473      62,523     -7,950         0/3
            2   5      72,771      67,015     -5,756         1/5
            3   5      79,854      77,829     -2,025         1/5
            4   5     108,025      92,737    -15,288         1/5
            5   4     108,776      88,308    -20,468         1/4
            6   1     102,770      80,360    -22,410         0/1
          ALL  27      87,157      77,583     -9,574         5/27

    tape       arm         mean bank   beats opponent
    98900762   cow11          87,817          16/27
    98873431   cow11          87,220          15/27
    98884730   cow11          86,435          13/27
    98916796   sheep10        81,406           7/27
    98889302   sheep10        77,122           3/27
    98921350   sheep10        74,220           3/27

The cell `98832334 / 98900762 = 139,821` is byte-identical to the same cell in the 53-tape sweep,
so the two harnesses agree.

The yarn latch is directionally right and the shipped default arm is the correct one.
The sheep penalty deepens monotonically with milk sinks, which is the sink model working.

Cut the same rows by WOOL instead and the sign flips:

     wool_end   n       cow11     sheep10      delta  sheep10 wins
            0  10      95,166      78,293    -16,873         1/10
            1  13      85,843      76,046     -9,798         1/13
            2   3      69,127      77,796     +8,669         2/3
            4   1      78,243      89,830    +11,587         1/1

**n = 4 on the winning side.** This is the sample size that produced this project's +40% in-sample
against +12.8% held-out. It is a hypothesis, not a result.

### Swapping the SPECIES instead of the tape: a large, clean loss

`BUY_ANIMAL COW`, `PICKUP COW` and `PLACE COW` rewritten to SHEEP after turn 88.
Order count and order SLOTS unchanged, unlike the count-trim wrapper that desynchronised the opening.
Legal at the latch because 98884730's first COW buy is turn 96 (d4h0), after `ARM_LATCH_TURN = 88`.
Mechanically sound: both species are structure PASTURE and `PLACE` only checks
`tile.kind == ANIMALS[item]["structure"]` (`reference/kaggriculture.py:377-390`), which is exactly
what the shipped `_PASTURE` tuple is derived for.

     WOOL sinks   n    baseline   cow2sheep      delta   swap wins
              0  10      95,166      42,023    -53,143       0/10
              1  13      85,843      47,482    -38,362       0/13
              2   3      69,127      59,466     -9,661       0/3
              4   1      78,243      46,146    -32,097       0/1

     MILK sinks   n    baseline   cow2sheep      delta   swap wins
              0   4      75,177      57,004    -18,173       0/4
              4   5     108,025      47,772    -60,253       0/5
              6   1     102,770      28,448    -74,323       0/1

            ALL  27      87,157      46,742    -40,415       0/27
    head-to-head:  baseline 44/81    cow2sheep 0/81

**REVERTED. Null recorded, code deleted, no flag.**
0 of 27 draws and 0 of 81 head-to-head, mean -$40,415.

The gradient is in the predicted direction on both axes, so the sink model is right and the
intervention is wrong.
Two reasons it loses far more than swapping the whole tape: 11 sheep overshoots the 10 the sheep
tapes actually buy, and the tape's collection stops are timed for cows (`first_yield_day` 8,
`interval` 2, `:822`) while sheep yield on 6 and 3, so a share of the harvest stops arrive at a tile
holding nothing.

**Correction to an earlier claim in this session.** I wrote that a cow/sheep swap is not expressible
as a tape edit. That was too strong: the route, pen, walk and stop are identical and the swap runs.
What shifts is the yield calendar, which is a cost, not a breakage. The measured cost is -$40,415.

### Why no latch can do better: the information is not there yet

Compatibility measured from a sheep tape as base, the reverse of the earlier table:

    base 98889302 (10/6)                   base 98921350 (10/6)
     latch turn  agreeing  4/11  10/6       latch turn  agreeing  4/11  10/6
          d3h16        72    53    19            d3h16        72    53    19
          d3h23        15     0    15            d3h23        57    53     4
          d5h23        14     0    14            d5h23        53    49     4
          d6h23        12     0    12            d6h23         1     0     1

From either direction, the last turn at which a cow tape and a sheep tape are BOTH reachable is
d5h23.
Shops unlock on the day boundary at d3, d6, d9 (`:886`), so at d5h23 exactly **one** shop instance
has been drawn.
After d6h23 every base collapses to one herd.

**The herd must be committed on one shop draw.**
`P(YARN_STORE)` is 1/8 per draw; MILK is drained by three shop types of eight.
Committing blind, 4 sheep / 11 cow is the correct marginal bet, and the yarn3/yarn6 latch is
capturing the only extra information that exists at the decision point.

The wool>=2 signal that predicts a sheep win arrives on d9 or later. It is unreachable by any tape
latch. Acting on it would require the planner to buy the animals rather than the tape -- which is
the "optimise the artifact, not a proxy" question, not a tape question.

## What each product actually FETCHES, and why the herd finding generalises

`data/logs/what_each_crop_realises.log`, tape 98884730 replayed on 8 open-arm draws, seed 123641874.
Units and cash are read by differencing the shed and the bank across the market phase, never by
summing offers.

    product      $/unit across 8 draws     % of base
    CARROT             $52 - $103         185% - 296%
    WHEAT              $28 -  $33         111% - 132%
    MILK               $26 - $165          16% - 103%
    STRAWBERRY         $32 - $144          27% - 115%
    MELON              $95 - $238          38% -  95%
    WOOL                $1 - $113           1% -  56%

**CARROT never sells below base on any draw, and is insensitive to its own sink count** -- $84, $92,
$77, $65, $103 per unit at 0, 1, 2, 3 and 4 sinks.
`T = 450` is the deepest book in the game, and the price sits ABOVE base everywhere, which means the
town drains more carrot than both players together supply.
The tape makes 49 units all season.

STRAWBERRY is the opposite and is the largest single exposure at 175 units:

     sinks   n   mean $/unit   % of $120 base
         2   1            32              27%
         3   2            65              55%
         4   1            45              38%
         5   3           123             102%
         6   1           138             115%

Per plant -- 38 strawberry plants produce 175 units (4.6 each), 20 carrot plants produce 49 (2.5):

    98845865  STRA 2 sinks    strawberry $147/plant    carrot $191/plant
    98841506  STRA 6 sinks    strawberry $635/plant    carrot $258/plant

Seed cost is $100 against $20.
So substituting carrot for strawberry is right on strawberry-poor draws and badly wrong on
strawberry-rich ones -- and STRAWBERRY is planted d2 to d11, before the sink count is known.

### Why the swap lost, measured rather than argued

`data/logs/why_the_swap_loses.log`. Not cadence, and only mildly production.

    draw        arm         bank    MILK sold  $/unit   WOOL sold  $/unit
    98818709 w0 baseline  109,940        158     165          96       5
    98818709 w0 swap       46,689          0       -         192      12
    98832334 w1 baseline  134,165        157     154          92      27
    98832334 w1 swap       78,581          0       -         192      18
    98850459 w2 baseline   69,024        157      46          92     113
    98850459 w2 swap       88,725          0       -         192     132
    98950829 w2 baseline   73,541        157      26          92     113
    98950829 w2 swap       84,940          0       -         192      90

    produce harvested off the tiles:  baseline 249-254 units, swap 192

Sheep produce 23% fewer units.
The price per unit moves by a factor of 33.
The same 192 units of wool fetch $2,356 on a draw with no yarn store and $25,326 on one with two.

**Cadence was NOT the mechanism, and my earlier claim that it was is withdrawn.**
`HARVEST` takes every accumulated unit and zeroes the tile (`reference/kaggriculture.py:469-471`)
and `max_held` is 6 for both species, so a stop can be 18 days late on sheep before a unit is lost.
Every animal is placed in a d4-d10 window, so they all shift phase together.

**The mirror case is the important one.** On 98950829 the BASELINE sold 157 units of milk at $26 --
that draw drew zero milk sinks. The cow tape does to milk exactly what the sheep tape does to wool.
Correcting the herd to the draw is worth $10k to $60k per season, against the $1,335 that choosing
between 53 tapes buys.

### The corrected species-swap number

The first run rewrote only the 24 ops naming COW and left 131 naming MILK -- 11 `PLACE MILK` shed
drops and 120 `SELL MILK` orders addressing a product the farm no longer produced.
`PLACE` takes `item = action[1]` and `SELL` aborts when the shed holds none of `item`, so the wool
was harvested into unit inventories and never reached the shed.
**The -40,415 reported for that run is withdrawn: it measured a severed pipeline.**

    arm                        ALL 27      wool >= 2 (n=3)   head-to-head
    broken pipeline           -40,415  0/27    -9,661  0/3        0/81
    product tokens rewritten  -25,573  2/27    +6,447  2/3        3/81

Fixing the tokens was worth +$14,842. **The arm still loses and is REVERTED, no flag.**

The wool signal survived a change of mechanism, which is the only reason it is still open:

                            wool 0-1     wool >= 2
    swap the whole TAPE      -12,874       +9,399   (3/4)
    swap the SPECIES         -30,470       +6,447   (2/3)

Two independent interventions, same sign flip at the same threshold, still n = 3-4.

### The timing conflict, which is the actual blocker

`SHOP_ADAPT_HERD = True` and `SHOP_ADAPT_FROM_DAY = 3` are LIVE in the shipped artifact, with
`HERD_FLOOR_COW = 4` and `HERD_FLOOR_SHEEP = 1`. The float exists.
Its own note already records the trap:

> A first version used day 11 ... That reasoning was right about the evidence and wrong about the
> decision, because it ignored what is left to decide: `split` is anchored on `state["bought"]`,
> which never decreases. The schedule's rows all sit at day 10 or earlier, so by day 11 there was
> almost nothing left to steer.

The tape buys its cows on d4, d6, d6, d7, d8 and d10 -- **all 11 committed before the d11/d12
handover.** Shop-weighted demand visible: 20% by d3, 39% by d6, 55% by d9, 68% by d12.
The information matures one day after the last decision it could have changed.

NOT YET VERIFIED: whether the tape's `BUY_ANIMAL` rows actually pass through `_herd_split`'s
relabelling during the replayed days. The loop at `main_restB.py:12097` looks like they do. If they
do not, the float is inert for the entire herd.

## How the three shipped arms differ on PRODUCT

A build ships THREE arms. There are four tapes here because there are two builds:

               yarn3       yarn6       open
    restA    98889302    98921350    98907591
    restB    98889302    98921350    98884730

Counted with `kagg.analysis.fills.record_fills`, six open-arm draws, seed 123641874,
`data/logs/arms_by_product_fills.log`.

    product        yarn3    yarn6   open-A   open-B
                    units    units    units    units
    MILK              137      116      241      257     open arms sell ~2x the milk
    WOOL              224      243      125      128     yarn arms sell ~1.9x the wool
    STRAWBERRY        177      188      298      269     open arms sell ~1.5x the strawberry
    CARROT             19       24       57       57     open arms sell ~2.6x the carrot
    MELON              66       60       57       62     same
    FERTILIZER        258      258      262      269     same
    WHEAT (net)    +5,993   +4,533   +6,459   +6,474     same

    BANK           83,709   79,465   90,486   92,069

**The arms differ on four products, not just the herd.** The yarn arms are wool-led with materially
less crop throughput; the open arms are milk plus strawberry plus carrot. So a whole-tape swap is
NOT a controlled herd experiment -- it moves the crops too, which is why the tape swap and the
species swap gave different numbers at wool>=2 (+9,399 against +6,447).

**open-B beats open-A on all six draws**, mean bank 92,069 against 90,486. First direct comparison
of the two builds on the slot that separates them.

### Wheat trading is a wash and must not be read as an arm difference

    arm      tape        WHEAT bought    $ paid   WHEAT sold    $ got      net
    yarn3    98889302           1,461    67,515        1,553    73,508   +5,993
    yarn6    98921350             123     4,799          183     9,332   +4,533
    open-A   98907591              98     3,753          201    10,212   +6,459
    open-B   98884730              97     3,713          200    10,187   +6,474

`yarn3` turns over fifteen times the wheat volume for the same ~$6k net. WHEAT's above-curve is
`log` at 0.20, almost flat, so the extra volume neither earns nor costs. `BUY_PRODUCT` is legal for
WHEAT and FERTILIZER only (`:601`).

### A measurement error of mine, and the correction to the correction

The first version of this table differenced the shed against the bank. That is failure mode 3 in
`kagg/analysis/fills.py`'s own docstring -- PICKUP and FEED move the shed, so units shuttled out to
feed the herd were booked as sales. Cash was worse: the `len(movers) == 1` guard dropped most fills
and reported STRAWBERRY at $4,080 against the true $24,210.

**I then called `yarn3 WHEAT 1,553` impossible for 132 planted tiles. That reasoning was also
wrong** -- it forgot `BUY_PRODUCT`. The figure is correct and `record_fills` reproduces it. The
table was wrong; the number I picked to prove it was not.

Use `record_fills` for every market quantity. This is the fourth time this repo has got the same
answer wrong with a plausible proxy.

## The player we ship has TWO arms, not three, and the rule is exact

All four tapes are the same player, `UjjwalPardeshi`. Thirteen of his games are in the corpus
(`data/logs/ujjwal_spread.log`), and they contain exactly two strategies:

    tape      d3 shop         d6 shop added    WHEAT STRAW CARR MELON  SHEEP COW  W/L      bank
    98836697  FARMERS_MARKET  BAKERY             134    38   20    11      4  11    W    62,491
    98907591  SMOOTHIE_SHOP   BAKERY             134    41   20    11      4  11    W   100,149
    98912171  FARMERS_MARKET  BRUNCH_SPOT        134    38   20    11      4  11    W    67,278
    98914508  ICE_CREAM_SHOP  BRUNCH_SPOT        134    38   20    11      4  11    W   105,370
    98852727  PET_CAFE        FARMERS_MARKET     134    41   20    11      4  11    W    60,856
    98834418  PIZZA_SHOP      ICE_CREAM_SHOP     134    38   20    11      4  11    W    80,378
    98898462  SMOOTHIE_SHOP   PET_CAFE           134    38   20    11      4  11    W    84,599
    98884730  SMOOTHIE_SHOP   PIZZA_SHOP         134    38   20    11      4  11    W   141,250
    98845865  PET_CAFE        SMOOTHIE_SHOP      134    41   20    11      4  11    W    63,882
    98859585  YARN_STORE      PIZZA_SHOP         132    32   12    11     10   6    W    78,677
    98916796  YARN_STORE      SMOOTHIE_SHOP      132    32   12    11     10   6    L   126,578
    98923606  YARN_STORE      SMOOTHIE_SHOP      132    32   12    11     10   6    L    81,982
    98889289  ICE_CREAM_SHOP  YARN_STORE         128    39   12    11     10   6    W    97,875

**`YARN_STORE` in either of the first two draws -> 10 sheep / 6 cow and 12 carrots all planted on
d26. Otherwise -> 4 sheep / 11 cow and 20 carrots spread d11-d26.** Nine cow games, four sheep
games, no exception. The d6 shop matters only when it IS the yarn store (`98889289`).

The 38-against-41 strawberry difference is NOT a branch: the three tapes at 41 saw BAKERY,
SMOOTHIE_SHOP and FARMERS_MARKET at d6, no pattern, and they mean $74,962 against the 38-group's
$90,228. Re-tried plants, not a decision.

**RETRACTED.** Earlier in this session I read the d6h20 divergence between `98907591` and `98884730`
-- BAKERY against PIZZA_SHOP -- as a milk-axis branch. The differing action was a single
`SELL FERTILIZER 1`. There is no milk branch in his play.

## Three arms is one too many

All four tapes on eight draws of each class, same seed, each draw's own recorded opponent
(`data/logs/do_we_need_three_arms.csv`).

    per-class mean bank
    class          yarn3     yarn6    open-A    open-B
    yarn3         97,412    90,893    74,038    73,071
    yarn6        107,497   104,023    86,223    86,486
    open          83,852    79,956    96,306    99,086

**`yarn3` beats `yarn6` on yarn6's OWN class**, 107,497 against 104,023, best on 5 of those 8 draws.

    policy                                mean bank      wins
    2-arm: any yarn -> yarn3, else open-B   101,332    10/24
    shipped 3-arm (yarn3/yarn6/open-B)      100,174     9/24
    shipped 3-arm with open-A (restA)        99,247     6/24
    always yarn3                             96,254     5/24
    always yarn6                             91,624     4/24
    always open-A                            85,522     3/24
    always open-B                            86,214     6/24
    ORACLE over the four tapes              102,292     9/24

Collapsing to two arms, which is the structure the player himself uses, is worth **+$1,158 and one
more win**, and lands within $960 of the four-tape oracle. `98921350` and `98907591` both drop out.

Also settled: **restB beats restA**, 100,174 against 99,247 and 9 wins against 6.

The win counts printed in `data/logs/do_we_need_three_arms.log` under the summary block are WRONG --
that code compared every arm's bank against open-B's opponent bank, and the opponent's bank depends
on which arm we play. The per-class rows in the same log, and the table above, are recomputed
per-arm from the CSV and are correct.

## CORRECTION: Ujjwal has FOUR strategies and THREE latch points, and I twice said two

Alex pushed back on the grouping twice -- "there are 4 different strawberry values", "there are 5
different strawberry values and 3 wheat - how is that 3 UNIQUE strategies" -- and he was right both
times. Bucketing the tapes destroyed the signal. The per-day grids
(`data/logs/ujjwal_by_day.log`) locate every difference exactly.

STRAWBERRY is identical on every day except **d10**:

    tape       tot    d2 d3 d5 d6 d7 d8 d9 d10 d11   yarn
    98845865    41     2  1  4  5  8  1  1  11   8     d9
    98852727    41     2  1  4  5  8  1  1  11   8    d15
    98907591    41     2  1  4  5  8  1  1  11   8    d15
    98834418    38     2  1  4  5  8  1  1   8   8    d15
    98836697    38     2  1  4  5  8  1  1   8   8   never
    98884730    38     2  1  4  5  8  1  1   8   8    d15
    98898462    38     2  1  4  5  8  1  1   8   8   never
    98912171    38     2  1  4  5  8  1  1   8   8   never
    98914508    38     2  1  4  5  8  1  1   8   8   never

**41 against 38 is one decision on d10: eleven strawberries or eight.**
I called it "re-tried plants, not a decision". That was an assertion and it was wrong.
d10 is the day after the d9 unlock.

The animal cadence separates a fourth group:

    tape       SH CO      d0   d4   d6   d7    d8    d9
    98859585   10  6      S4   C1   C4   S2  S2C1    S2
    98916796   10  6      S4   C1   C4   S2  S2C1    S2
    98923606   10  6      S4   C1   C4   S2  S2C1    S2
    98889289   10  6      S4   C1   C4   S2    S1  S3C1     <- its own cadence
    (all nine cow tapes identical:  S4  C1  C5  C2  C1  .  C2 on d10)

His four:

    #  trigger                  SHEEP/COW  WHEAT  STRAW  CARROT        tapes
    1  yarn at d3                   10/6    132     32   12 (d26)      98859585 98916796 98923606
    2  yarn at d6                   10/6    128     39   12 (d26)      98889289
    3  no yarn, d10 -> 8 straw      4/11    134     38   20 (d11+d26)  6 tapes
    4  no yarn, d10 -> 11 straw     4/11    134     41   20 (d11+d26)  98845865 98852727 98907591

### Three latch points, not one

How long each tape stays byte-identical to `98884730`:

    group                          tape       agrees to    = day/hour
    1 yarn-d3                      98859585          88       d3h16
                                   98916796          88       d3h16
                                   98923606          88       d3h16
    2 yarn-d6                      98889289         153        d6h9
    3 open straw-8                 98884730         719      d29h23
                                   98898462         222        d9h6
                                   98834418         359      d14h23
    4 open straw-11                98852727         242       d10h2
                                   98907591         164       d6h20
                                   98845865          44       d1h20

Each group peels off exactly one shop draw after the last:

    latch  turn            decides                  on what he had just seen
      1     88  = d3h16    sheep tape or not        the d3 unlock
      2    153  = d6h9     the d6 sheep tape        the d6 unlock
      3    242  = d10h2    11 strawberries or 8     the d9 unlock

`ARM_LATCH_TURN = 88` reaches only the first. Branches 2 and 3 are prefix-compatible and unused.

### The shipped arms are three different players

    98889302  yarn3 arm     WeAreFarmers
    98921350  yarn6 arm     nao.kwmr
    98884730  open arm      UjjwalPardeshi
    98907591  restA open    UjjwalPardeshi

We stitch three unrelated seasons at one latch. Ujjwal's own yarn-d3 and yarn-d6 games
(`98859585`/`98916796`/`98923606` and `98889289`) are in the corpus and are not used.
That is why the arms looked incoherent on product, and it makes the earlier "yarn3 beats yarn6 on
yarn6's own class" a comparison between two strangers rather than between two branches.

**NOT YET MEASURED:** an all-Ujjwal arm set at three latch points against the shipped mixed set.
That is the next run.

### No signal separates the two open tapes

80 open-class draws, both open tapes, `data/logs/what_selects_open_a.csv`.
open-A wins 19 of 80. Every candidate separator available at d6 -- the d3 shop, the d6 shop, the
instance count, and the milk, wool, strawberry, carrot and wheat sink counts -- yields a perfect-split
gain of **exactly $0** over always playing open-B.

    always open-B    86,391
    ORACLE           86,656     headroom +265

The headroom itself is $265 across 80 draws, so this pair is not where the value is. The d10
strawberry branch is a different question and has not been tested.

## The four splits, built and measured

Alex: *"just build the 4 splits ... but just split the fucking 4th one on that criteria"*.
`/tmp/four_splits.py`, results in `data/logs/four_splits.csv`.

    latch  turn           test                          arm         agrees to
      1     88  d3h16     YARN_STORE unlocked by d3     98859585    turn 88
      2    153  d6h9      YARN_STORE unlocked by d6     98889289    turn 153
      3    242  d10h2     opponent money > 650          98852727    turn 242
      -    default                                      98884730    -

Every arm is UjjwalPardeshi, so the arms are prefix-compatible by construction rather than by luck.

### The d10 split is real, and it keys on the OPPONENT's bank

First: it is a decision, not re-tried plants. Counted on the BOARD, not on the action stream --
`PLANT` ops on d10 and the strawberry tiles standing before and after:

    tape       PLANT ops d10   straw TILES d10h0   straw TILES d11h0   net new
    98845865              11                  21                  32       +11
    98852727              11                  21                  32       +11
    98907591              11                  21                  32       +11
    98834418               8                  21                  27        +6
    ... all six straw-8 tapes identical ...

**I claimed twice that this was re-tried plants. It is not.** 32 strawberry tiles against 27.

Second: no shop signal separates the two groups -- `98907591` (plants 11) and `98834418` (plants 8)
have identical STRAWBERRY 2 / MILK 2 draws at d9. Board state at d10h0 is identical too: 6
strawberry seeds, 1 free tile, 0 weeds, 50 tiles, in all nine games. The only field that varies is
money, and it does not order the decision.

The opponent's bank does, perfectly and with no overlap:

    tape       straw  OPPONENT           opp$ at d10   our$ at d10
    98907591      11  fufufukakaka             2,192         1,495
    98845865      11  GPTatoes                 1,270         1,701
    98852727      11  Jiachen Li                 795           795
    98914508       8  GPTatoes                   507         1,098
    98836697       8  shinamonmon                507         1,098
    98912171       8  shinamonmon                507         1,098
    98834418       8  Ömer Faruk Yüce            507         1,098
    98898462       8  Ömer Faruk Yüce            502         1,093
    98884730       8  GPTatoes                   487         1,078

`GPTatoes` appears in BOTH groups, so it is not opponent identity -- it is their cash.
Threshold 650 is the midpoint of the 507-to-795 gap. **Three points on the winning side.**

### Result, scored on WINS because the ladder is Elo

    110 draws
      policy                                wins    rate   mean margin
      FOUR SPLITS (all Ujjwal)            49/110   44.5%          -121
      shipped (3 players, 1 latch)        41/110   37.3%        -1,640
      always 98884730 (straw-8)           37/110   33.6%        -6,135
      always 98852727 (straw-11)          39/110   35.5%        -4,123

      by draw class          n     FOUR    shipped
      yarn3                 20     6/20      4/20
      yarn6                 10     4/10      1/10
      open                  80    39/80     36/80

      differs from shipped on 38/110 draws
        turns a LOSS into a WIN:  8
        turns a WIN into a LOSS:  0

    draw        cls              shipped                  four
    98921350.j  yarn6   102,362/112,754      127,775/121,197   GAIN
    98875614.j  yarn6    79,024/ 99,951       91,416/ 90,657   GAIN
    98951020.j  yarn6    72,525/ 79,048       71,926/ 71,513   GAIN
    98829909.j  yarn3   115,520/118,523      117,110/116,353   GAIN
    98859585.j  yarn3    77,646/ 79,981       78,620/ 78,585   GAIN
    98846100.j  open    134,412/135,627      138,519/132,092   GAIN
    98882460.j  open     69,336/ 72,309       69,325/ 69,025   GAIN
    98962237.j  open     66,933/ 67,875       67,586/ 66,215   GAIN

On `98882460` our own bank FALLS $11 and the game flips from loss to win, because the opponent
drops $3,284. Scoring on money hides that entirely.

**IN-SAMPLE. Not yet held out.** The 650 threshold was read off nine of Ujjwal's games that are in
this corpus, and the arm tapes' own draws are among the 110. This is the shape of the recorded
+40% in-sample against +12.8% held-out precedent. The absolute win rate is also not a ladder
prediction: every opponent here is a recorded leaderboard seat.

### Money is the wrong score and I used it all evening

Alex, twice: *"dollar value doesnt matter"*, and CLAUDE.md already says so -- *"Select on win rate,
not money. A $43k win and a $4k win score identically."*

The measurement that shows why: switching between the two open tapes moves OUR bank by a median
$1,694 and the OPPONENT's by a median $1,764, and **on 43 of 80 draws it moves them more than us**.
Ten of the 24 result-flips between those two tapes are driven mainly by the opponent's bank moving,
not ours. A bank-only comparison cannot see half the effect.

## Crop Dusta sizes his carrot programme to the town's carrot sinks

146 unique Crop Dusta games -- 95 already on disk across five corpora, plus Alex's pull of ~50 more
into `~/Downloads` on 2026-08-27. `data/logs/crop_dusta_146.log`, rows cached at `/tmp/cd146.json`.

**The era worry is CLOSED and was mine.** I asserted the older folders might predate the 2026-08-08
drain change or the 2026-08-15 hinge change. Checked directly: `94348150`, `98884730` and
`99831028` all record `module_version 1.32.7`, `marketParams {}`, `weedSpawnChance 0.005`,
`townShopSellInterval 4` and identical opening prices. Same economy. All 146 are usable.

    carrot sinks   games   mean carrots   mean margin        W
               0      16            0.0       +10,576    12/16
               1      31            4.4       +16,375    23/31
               2      46           23.0       +13,203    41/46
               3      39           31.5       +12,182    34/39
               4      12           44.4       +15,447    10/12
               5       1           36.0       +22,791      1/1
               6       1           59.0        +2,163      1/1

Monotone 0 -> 4.4 -> 23.0 -> 31.5 -> 44.4.
**At the 11-game sample this looked like noise and I reported it as such.** It is a policy.

And the programme starts earlier the bigger it is:

     carrots  games  share   mean bank   mean margin       W   starts
           0     68    47%     110,866       +11,387   53/68        -
        1-14     15    10%     111,010       +13,889   12/15      d26
       15-29     10     7%      97,985       +26,050   10/10      d24
       30-44     19    13%      95,076       +14,388   17/19      d22
         45+     34    23%      84,242       +13,326   30/34      d21

52 distinct carrot counts from 0 to 82, and 12-plus distinct (sheep, cow) pairs. He does not select
from a menu of arms the way the clone family does -- he sizes continuously.

**The bank column falls as carrots rise while the margin does not.** Third time in this session that
money points the opposite way to the quantity that scores.

### Why this is reachable and the herd is not

Shops unlock on d3, 6, 9, 12, 15, 18, 21 and 24. A decision at **d21 sees seven of the eight draws**.
The carrot programme is late by design, so its information is essentially complete when the decision
is made. The herd closes on d10 with one shop visible, which is why no herd latch can do better.

Our clone plants 20 carrots on every draw -- 8 on d11 and 12 on d26 -- whether the town drew zero
carrot sinks or four. And CARROT is the only product measured that never sells below base
(185-296% across eight draws, insensitive to its own sink count, `T = 450`, the deepest book).

**NOT MEASURED YET:** whether adding a sink-sized carrot programme from d21 to the clone tape wins.
It needs free tiles and hand-turns in d21-d26, which is the idle-hand census that has not been run.

    122W / 24L across the 146, mean margin +13,491.
    This is a SELECTED download set. It is NOT a win rate and must never be quoted as one.

## Crop Dusta cannot be cloned: 145 distinct seasons out of 146

    CARROT count only      51 distinct across 146 games
    all 5 crop counts     145 distinct across 146 games
    crops + herd          145 distinct across 146 games

The single repeat is one episode present twice on disk. An md5 of the full 720-turn action sequence
for his seat agrees exactly: **145 distinct full-season scripts.** Where they separate:

    identical up to      distinct scripts
      turn  24  (d1)                    3
      turn  88  (d3h16)                20
      turn 168  (d7)                  118
      turn 242  (d10)                 143
      turn 719  (d29)                 145

He shares an OPENING -- three variants through d1, twenty through d3h16 -- and then plays a
different season every time. **He is an adaptive agent, not an open-loop tape player.** The
clone-lineage architecture cannot copy him: there is no tape library to replay. What is copyable is
the RULE, carrots sized to the carrot sinks with the programme starting d21-d26, and that is a
policy, not a recording.

This is the opposite of the clone family, where 72 tapes are byte-identical to turn 88 and hold only
four distinct strategies between them.

## There is no slack for a carrot programme in the shipped tape

`data/logs/idle_hands_late.log`, tape 98884730 on its own draw, seed 123641874. Free tiles are owned
tiles holding nothing; a weed is not free. Idle hand-turns are slots emitting PASS or nothing.

     day   free tiles at dawn   weeds   hand-slots   PASS   IDLE %
      21                    6       1          296      9       3%
      22                    3       5          274      6       2%
      23                    4       2          252     12       5%
      24                    3       4          296      7       2%
      25                    3       0          252      6       2%
      26                    3       0          340     10       3%
      27                    1       0          296     17       6%
      28                    0       0          274     16       6%
      29                   18       0          198     15       8%

    d21-d29: 98 idle hand-turns of 2,478 (4%)

**Three to six free tiles and four percent idle hands.** A carrot cycle needs PLANT + WATER +
HARVEST on a free tile. Crop Dusta plants up to 82 from d21; this tape has room for a handful and
its crew is saturated.

So the carrot programme **cannot be inserted into a tape**. Adding it means displacing existing
work, which is a planner decision. This is the same wall as `add_land`: an insert with no seed, no
routed hand and no free tile measures nothing.

The finding still stands and is still the largest unexploited one: CARROT never sells below base
(185-296% across eight draws), its book is the deepest in the game at `T = 450`, the d21 decision
sees seven of the eight shop draws, and we plant 20 on every draw regardless. It is a planner task,
not a tape task.

## Crop Dusta sizes EVERY product to its own sinks, not just carrots

From `/tmp/cd146.json`, 146 games. All four are monotone in the count of shops that drain them:

    CARROT      by carrot sinks    0 -> 4.4 -> 23.0 -> 31.5 -> 44.4
    STRAWBERRY  by straw sinks    16 -> 24 -> 26 -> 32 -> 34 -> 37 -> 44
    COW         by milk sinks     4.0 -> 4.7 -> 6.1 -> 6.4 -> 8.1 -> 10.3 -> 12.0
    SHEEP       by wool sinks     3.3 -> 7.6 -> 10.7 -> 13.1

One rule, not four: **size each product to the number of shops that drain it.**

What pays for the carrots is the HERD, not the other crops:

     carrots   n   WHEAT  CARROT  TOMATO  STRAW  MELON  SHEEP   COW  animals  crop tiles
           0  68     123       0       4     32     16    7.8   7.7     15.4         175
        1-14  15     104       8      10     29     18   10.1   6.9     16.9         169
       15-29  10     109      24       6     31     16    7.8   6.4     14.2         187
       30-44  19      92      36      13     29     18    5.9   6.5     12.4         188
         45+  34     100      59       2     28     18    6.8   6.1     12.9         206

    CARROT vs total animals   -0.33      CARROT vs total crops   +0.52
    CARROT vs WHEAT           -0.26      CARROT vs STRAWBERRY    -0.19
    CARROT vs bank            -0.52      CARROT vs margin        +0.05

Animals fall 15.4 -> 12.9 while crop tiles rise 175 -> 206: livestock capital converted into tile
throughput. And once more, bank and margin point opposite ways.

## Is e2500 adaptable? Partly -- and the open window is d24-d29

    UNSOLVE_DAYS = tuple(range(24, 30))
    SOLVED_DAYS covers days 12..29, but 24-29 are excluded from PRECOMPUTED_ROUTES

    days     how they are played                       adaptable
    0-11     router solves live from the schedule      YES
    12-23    frozen (tile, ops) tours                  no
    24-29    excluded from the route table             YES

`_apply_precomputed` keys a stop on the exact `(tile, ops)` tuple, so a solved day is a frozen tour,
not a target: change what is planted and the stop stops matching. The clone arms are worse still --
they replay recorded actions verbatim.

**d24-d29 is the window and the timing is ideal.** Shops unlock on d3, 6, 9, 12, 15, 18, 21 and 24,
so a decision on d24 sees ALL EIGHT draws. Crop Dusta's own 1-14 band starts d26 and his 15-29 band
d24; only his 45+ band needs d21-d22, which is inside our frozen region.

So a sink-sized carrot row for d24-d29 is a schedule-level edit inside a window the router already
plans live. It needs no handover change and no new architecture.

**NOT MEASURED:** whether e2500 has free tiles and spare hand-turns in d24-d29. The idle-hand census
in this file was taken on the CLONE TAPE (3 free tiles at d24-d26, 4% idle hands), which is a
different agent on a different board. That number must be taken on e2500 before any of this is real.

### Hazard: SOLVED_DAYS exists in FOUR copies and only the last is live

`submission/e2500_carrot.py` lines 1314, 1586, 1858 and 2130 each define `SOLVED_DAYS`, all covering
days 12-29 with the same day keys and differing tours. Python keeps the last. `PRECOMPUTED_ROUTES`
is derived from it at import.

This is verbatim the failure already recorded in the global rules -- *"SOLVED_DAYS was patched while
the code read PRECOMPUTED_ROUTES, derived from it at import, and 'changes nothing' was reported"*.
Any edit to the first three copies is a silent no-op.

## The handover measurement in the shipped file does not survive more draws

`make_agent`'s docstring claims d20 handover banks 94,496 against the tape's 94,000 and that the
boundary is *"worth +$11,256 over the d11 we ship"*, on its own stated basis of ONE seed and ONE tape.

Three sweeps from 2026-08-26 disagree. `stop` is the handover day; day 30 is the tape playing the
whole season:

    handover day    mean bank   vs full tape   beats tape
      all_draws (27 draws)
            12         82,040        -12,411        0/27
            20         86,151         -8,300        0/27
            28         92,498         -1,953        0/27
      fine (18 draws)
            14         95,129         -1,437       10/18
            18         92,570         -3,996        5/18
            22         96,429           -137       12/18
            24         95,074         -1,492        4/18
            26         94,767         -1,799        1/18
      class (18 draws)
            12         91,989         -4,577        6/18
            20         96,008           -558        9/18
            28         94,762         -1,804        2/18

**The planner is worse than the tape at every handover day tested.** Best is d22 at -$137 mean, and
even there only 12 of 18 draws improve. Two caveats: these sweeps carry no opponent bank, so they
are scored on MONEY, which this session has established is the wrong metric; and they disagree with
each other badly (d12 is -12,411 in one and -4,577 in another), so variance across draw sets is large.

## Tomato and melon complete the rule -- and give it a mechanism

Alex spotted both: *"and also tomato - melon looks vaguely constant"*. Measured on the 146
(`data/logs/all_sinks.log`):

    quantity      sink types   corr with own sinks   planted range
    SHEEP  (wool)          1                +0.71            2-17
    STRAWBERRY             4                +0.64            8-52
    COW    (milk)          3                +0.62            3-13
    TOMATO                 2                +0.57            0-25
    CARROT                 2                +0.55            0-82
    WHEAT                  5                +0.13          43-212
    MELON                  0                  flat           10-23

**MELON is constant BY CONSTRUCTION.** It appears in no shop (`reference/kaggriculture.py:103-112`);
its only buyer is the town centre, which is identical on every draw. Sink count is 0 in all 146
games and he plants 16.6 +/- 2.7. There is no signal to adapt to, so he does not adapt.

**TOMATO is a GATE, not a slope:**

    tomato sinks    n   mean planted
               0   16            0.0
               1   32            0.0
               2   47            5.2
               3   38           11.1
               4    8            8.6
               5    5           17.2

Zero tomatoes until TWO sinks exist -- 48 of 146 games, not one tomato planted. Then it ramps.
That is a threshold rule and it is directly implementable.

### The mechanism

**The fewer shop types drain a product, the more its quantity varies with the draw.**

WOOL is carried by one shop of eight, so whether the yarn store appears is a large update, and SHEEP
has the strongest response of anything measured (+0.71). WHEAT is in five of eight, so it is drained
on nearly every board -- little variance to react to, and it doubles as animal feed, so its count is
driven by the herd rather than the market (+0.13). MELON is in none and is flat.

This inverts an earlier framing in this file. WOOL being 1-of-8 was written up as what makes it
DANGEROUS -- `sq` above-curve, T=105, the harshest flood penalty in the table. It is the same fact
that makes it the most INFORMATIVE: the product where knowing the draw is worth the most. Both are
true and they are the same property seen from the two sides.

For the d24-d29 window in e2500, this ranks what to make dynamic first: sheep, then strawberry, then
cows, then tomato and carrot. Wheat and melon are not worth wiring to the shop draw at all.

## Crop Dusta's opening is version drift, and the current version is worth $13k more

Alex proposed: copy his d0-d3, then apply the sink ratios. The opening is NOT one script.

    d1 opening    n    episode id range              mean margin      W
    9c61d7       84    94,545,368 .. 97,518,736           +7,410   65/84   (77%)
    ad56f6       59    97,601,003 .. 98,951,023          +20,850   54/59   (92%)
    a8326b        2    97,609,790 .. 97,696,699          +50,034     2/2

**The id ranges do not overlap.** That is version drift, not adaptation -- and it cannot be
adaptation, because no shop unlocks before d3, so d0-d1 carries no information to branch on. He
rewrote the agent around episode ~97.5M and gained +$13,440 of margin and 15 points of record.

How far the CURRENT opening holds:

    identical through    current-version games sharing it
      turn 24  (d1)      59 of 59      <- one script
      turn 48  (d2)      58 of 59
      turn 72  (d3)      52 of 59
      turn 88  (d3h16)   45 of 59, in three groups (27 / 10 / 8)

**d0-d2 is a single script across every current game**, fragmenting at d3h16 -- the first shop draw.

So the plan needs two corrections: copy `ad56f6` specifically, and the copyable prefix is d0-d2.

## Alex's 2026-08-27 pull is the current agent and the best block in the corpus

    directory                n    episode ids                    mean margin
    Downloads (today)       51    97,601,003 .. 97,710,447           +25,115    48W/3L
    leaders_2026-08-24       3    97,204,025 .. 97,235,932           +15,576
    downloads_2026-08-20    30    94,545,368 ..  94,639,447           +7,837
    downloads_2026-08-21    24    94,742,828 ..  95,702,942           +7,815
    daily_2026-08-26        11    98,852,910 ..  98,951,023           +6,028
    kawa_2026-08-24         27    97,245,055 ..  97,518,736           +5,669

**Do not compare margins across those folders.** Each is a different selection, not a random sample:
`daily_2026-08-26` holds the NEWEST ids and the second-worst margin, which fits the standing note
that those downloads are biased toward losses. What is valid is that all 51 of today's are
post-drift, so they are the current agent.

### The sink rule survives the version change

    quantity      ALL 146     OLD 84     NEW 62
    CARROT          +0.55      +0.54      +0.53
    STRAWBERRY      +0.64      +0.71      +0.51
    COW             +0.62      +0.58      +0.66
    SHEEP           +0.71      +0.76      +0.70

He rewrote the agent and kept the principle. That is evidence the sizing is deliberate rather than
an artefact of one implementation.

Current agent's carrot ladder, steeper than the pooled one:

    carrot sinks    n   mean carrots   mean margin      W
               0    3            0.0       +19,588    2/3
               1   12           11.2       +39,133  12/12
               2   22           23.7       +19,451  22/22
               3   17           32.8       +12,852  13/17
               4    6           47.0       +24,578    6/6

    current agent mean margin  +21,729       old agent  +7,410

At one sink the new version plants 11.2 where the old planted 4.4. It got more aggressive on carrots
and tripled its margin.

## CORRECTION: the herd is not committed by the information, it is committed by the SCHEDULE

Earlier in this file I concluded that the herd "must be committed on one shop draw" and that no latch
could do better, because from either base the last turn at which a cow tape and a sheep tape are both
reachable is d5h23. **That is true of the CLONE, and it is not a property of the game.**

Crop Dusta, 61 current-version games (`data/logs/dusta_herd_timing.log`):

     day   SHEEP    COW   GOOSE   total   cum %
       0     122    183       0     305     33%
       6     101    115      28     244     61%
       8      95      7       4     106     73%
       9      44     21       2      67     80%
      10      58     17       5      80     89%
      11      13     15       1      29     92%
      12       4     20       9      33     96%
      15      15      8       0      23     99%
      16       4      1       1       6    100%
      18-19    4      0       0       4    100%

Our clone buys on d0, d4, d6, d7, d8 and d10 and is 100% done by d10. He is 33% done at d0, 89% by
d10, and still buying at d19. Last-purchase day per game runs 6, 8, 9, 10, 11, 12, 13, 15, 16, 19.

**And the herd is bought AFTER the demand is visible:**

    SHEEP against YARN_STORE          COW against the first MILK sink
      bought before it appeared  23%    before  47%
      bought after  it appeared  61%    after   52%
      it never appeared          16%    never    1%

Sixty-one percent of his sheep are bought after he can see the yarn store. That is what makes the
+0.70 correlation causal rather than coincidental.

    yarn arrives    games   mean SHEEP   mean COW   mean margin
    d0-d6              19         13.5        5.1      +28,595
    d7-d12              5         12.6        4.6       +5,149
    d13+               14          5.0        6.6      +19,912
    never              23          3.2        8.1      +20,973

**The constraint was never that the information arrives late. It is that our tape has spent the
money by d10.** He solves it by DEFERRING the purchase, not by predicting the draw.

For e2500: 89% of his herd lands by d10, inside e2500's live window (d0-d11), so most of the rule is
expressible there. The d15-d19 tail falls in the frozen d12-d23 block and is not reachable without
unfreezing those days.

## The goose kill stands, on better evidence than the kill itself had

Alex spotted GOOSE purchases in Crop Dusta's day table. This repo killed geese (`Geese lose to the
mirror and to the field`, then `Delete the geese rather than leave a losing flag in the tree`), so
the question is whether the strongest player in the corpus buying them reopens that.

**Do not re-raise the `SELLABLE`/unsellable-EGG bug in this context.** It was fixed long ago, Alex
has corrected it repeatedly, and the stale memory asserting it invalidated the goose verdict was
deleted on 2026-08-27. The goose verdict does not depend on it.

Re-asked against 61 current-version Crop Dusta games (`data/logs/dusta_geese.log`):

    21 of 61 games use geese (34%), mean 2.4 birds when used

    corr(EGG sinks, GEESE bought) = +0.16
      compare  SHEEP/wool +0.70   COW/milk +0.66   CARROT +0.53   STRAWBERRY +0.51

                     games   mean GOOSE   SHEEP   COW   mean margin       W
    with geese          21          2.4     5.0   5.1       +18,535   20/21
    no geese            40          0.0     9.0   7.3       +23,524   36/40

**Geese are the ONE thing he does not size to its own sinks** -- +0.16 against +0.70 for sheep.
Every other product in his repertoire tracks its own demand. Geese are occasional filler, usually a
single `d6: 3` order, and his goose games carry less margin while running 5.0/5.1 sheep and cows
against 9.0/7.3 without.

GOOSE mechanics for the record (`reference/kaggriculture.py:20`): cost 300, structure COOP,
first_yield_day 4, interval 1, max_held 4, product EGG. Interval 1 is the fastest yield in the game.
EGG is base 50, T=332, above_func `log` at 0.20 -- one of the flattest above-curves. So the birds are
cheap and fast and the book resists flooding; they still do not pay here.

**Correlational and confounded**, n=21, selected download set, NOT a controlled A/B. But it is a top
player's revealed preference across 61 current games and it points the same way as our kill.

**The goose kill stands and nothing here justifies reopening the machinery.**

### A reading caution about the day tables in this file

The per-day animal table above is **summed across all 61 games**, not per game. `d6: 28 GOOSE` means
28 birds bought on d6 across the whole set, and `d0: 122 SHEEP` is about two per game. Alex misread
it as one game buying 28 and the header was the reason. Say "summed over N games" whenever one of
these is quoted.

## HELD OUT: the four-arm build survives, 122/138 against 97/138

`data/logs/four_arm_heldout.csv`. 138 draws from `leaders_2026-08-24` and `downloads_2026-08-19` --
corpora used for nothing in this work. Every arm tape and the 650 threshold came from
`daily_2026-08-26`, so none of these draws had a hand in choosing anything.

The BUILT artifact (`submission/main_four_arm.py`) against the shipped three-arm structure, both
driven the same way, each draw's own recorded opponent, seed 123641874:

    policy                     wins    rate    mean margin
    FOUR ARM (built)        122/138   88.4%        +13,063
    shipped 3-arm            97/138   70.3%         +7,976

    differs on 120/138 draws
      turns a LOSS into a WIN: 25
      turns a WIN into a LOSS:  0

    draw class      n      four   shipped
    yarn3          16     13/16     12/16
    yarn6          16     14/16      4/16
    open          106    95/106    81/106

**Twenty-five losses turned into wins and none the other way**, the same strictly-dominant shape as
in-sample. The winner's curse did not bite -- which is worth saying plainly, because this project's
recorded precedent is +40% in-sample against +12.8% held out.

**`yarn6` is where the gain lives: 4/16 -> 14/16.** That arm was `nao.kwmr`'s season; it is now
UjjwalPardeshi's own d6 branch. The single largest effect in the build is simply using one player's
own branches instead of three strangers' seasons.

**The absolute rates are NOT comparable between the two sets and neither is a ladder prediction.**
88% here against 44.5% in-sample is a difference in which games were downloaded, not in the agent.
Every corpus here is a selected set. What is valid is the head-to-head: same draws, same opponents,
only the policy changes. Both sets agree on direction and both show zero regressions.

### The artifact reproduces the harness exactly

Driven through its own `agent()` on the original 110 draws: 49/110, mean margin -121, per-class
6/20, 4/10, 39/80 -- identical to the composed-policy harness in every cell. Build-time prefix gate
passes with zero slack. Worst turn time 3 ms.

Arm usage across those 110: `open` 72 (35 wins), `yarn3` 20 (6), `yarn6` 10 (4), `rich` 8 (4). The
opponent-money latch fires on only 8 of 80 open-class draws, so the part of the design rested on
nine games and a hand-picked threshold is also the part contributing least.

## Milan Leonard (rank 2, 3031.5): not a clone, not a tape, and he reads the OPPONENT on day one

41 of his games, fetched 2026-08-27 into `data/seed_scripts/downloads_2026-08-27`.
Found via `ListEpisodes({"submissionId": 55801896})` rather than by scraping.

    identical to turn   distinct scripts
        24  (d1h0)                    1     all 41 share the opening day
        88  (d3h16)                   8
       153  (d6h9)                   28
       242  (d10h2)                  39
       719  (d29h23)                 41     every season unique

**41 distinct full seasons of 41 -- adaptive, like Crop Dusta, unlike the clone family.**
And his crop signature is nowhere near ours: WHEAT 182-233 against the clone family's fixed 128-134,
MELON pinned at 12, STRAWBERRY 36-38, CARROT 6-28, herd 4-9 sheep / 5-10 cow. Zero of his 41
signatures match any of the four known clone signatures.

### The latches, found from pairwise divergence rather than guessed cuts

820 pairs, first turn at which each pair differs:

       turn  = day/hour   pairs   share
         30        d1h6     544   66.3%
         97        d4h1      86   10.5%
         31        d1h7      36    4.4%
         52        d2h4      20    2.4%
         90       d3h18      18    2.2%
         50        d2h2      17    2.1%
        120        d5h0      16    2.0%
         98        d4h2      12    1.5%

Those eight turns carry **91%** of all pair divergences.

**d1h6 is before any shop exists** -- the first unlock is d3 -- so his main branch cannot be reading
the town at all.

### What the d1h6 branch reads: the opponent's bank

Grouping his 41 games by the action taken at turn 30:

    n=18   opp_money = 0            hands [PLACE FERT, WEST, PASS,  SOUTH]   BUY_PRODUCT WHEAT 3
    n=13   opp_money = 2, 18, 61    hands [PLACE FERT, WEST, WEST,  SOUTH]   BUY_PRODUCT WHEAT 3
    n=10   opp_money = 72, 109      hands [PLACE FERT, WEST, WEST,  SOUTH]   BUY_PRODUCT WHEAT 2

    my_money    OVERLAPS      opp_money    SEPARATES CLEANLY
    my_weeds    OVERLAPS      opp_hands    OVERLAPS
    my_planted  OVERLAPS      opp_planted  OVERLAPS
    my_hands    OVERLAPS      opp_weeds    OVERLAPS

His own board is identical in all 41 at that turn -- 19 planted, 4 hands, 0 weeds, farmer at (3,3).
The only thing that varies is what the opponent has done.

**TWO CAVEATS, both real:**

1. **Confounded with opponent identity.** The high-money group is only `Ryo Hasegawa` and `tetsuya`.
   With 41 games, "reads the opponent's bank" and "these two opponents play a style he answers"
   cannot be separated.
2. **The action deltas are tiny** -- one wheat unit, one hand moving WEST instead of PASS. That reads
   more like a REACTIVE CONTROLLER whose first visible disagreement lands at d1h6 because that is
   when the opponent's play has moved the observable state, than like a discrete strategy latch. The
   66% concentration argues for a branch; the size of the difference argues for continuous reaction.
   Not settled by this data.

**What is solid:** he is not a clone, not open-loop, and he conditions on the opponent from day one.
Every clone we hold ignores the opponent entirely, and `submission/main_four_arm.py` does not look
at the opponent until **d10h2** -- 212 turns later.

### How his games were found, for repeating it

`POST https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes` with
`{"submissionId": <id>}` returns that submission's episode list, agents and rewards. Intersect those
ids with the daily dataset's own file listing before downloading, because:

- `GetEpisodeReplay` and `DownloadEpisode` do not exist (404); `GetEpisode` exists but rejected every
  body tried.
- **The daily datasets are a SAMPLE, not the full day** -- 687 episodes for 2026-08-26. Asking for an
  id that is not in the sample is a 404 per request, which is the flooding to avoid.
- Of Milan's 85 episodes: 41 were in the published sample and fetched, 28 were not sampled, and 16
  finished after today's cutover and land in tomorrow's dataset.

Crop Dusta's current submission ids, from the same agent records: **55714246** and **55714252**.
He is rank 1 at 3107.0.
