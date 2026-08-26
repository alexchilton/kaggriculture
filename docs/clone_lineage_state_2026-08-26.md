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
