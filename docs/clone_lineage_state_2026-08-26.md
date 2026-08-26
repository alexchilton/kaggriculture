
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
