# The "stupid extra buy of the wheat" is animal feed, and both changes starve the herd

**Netting the round trip measures WORSE: 106 differing cells to 130, and money at d12 falls from
$12,666 to $8,958.** It is implemented as asked and is NOT reverted — that is Alex's call. My
recommendation is to revert it, and the reason is the one he asked me to watch for.

**Separately: the 38 regressed cells on the shipped tape gate are SPREAD, not one day, and 43 of
the 74 newly-failing field-days are FEED, CARE and COLLECT_FERTILIZER.** The seed-first ordering
starves the herd from d6 on. Same mechanism, both changes.

## What was done

`kawa_rows.net_the_round_trip`, applied to **every day**, not only d0 — it is uniform and there is
no day where a same-day buy-and-sell of one product is wanted. For each product, the overlap between
`buys` and `sells` is cancelled and only the remainder kept. Net shed movement per product is
unchanged by construction. d0's `buys {WHEAT: 9}` + `sells {WHEAT: 3}` becomes `buys {WHEAT: 6}`.

One correction fell out of it: the transform now runs **before** the mode is taken, not after. Taking
the mode over raw rows and transforming the winner picks the mode of a distribution nobody plays, and
it made the played row's label match no library row at all — d0, d5, d9 and d10 all reported "0 of
228 seasons". `build` and `coverage` both clean and net first now.

Suite: 154 passed.

## The three states, d0-d12 on game 92498144's own rows

    per-day differing cells                                                          total   money d12
    before anything   d0=6 d1=5 d2=2 d3=4 d4=4 d5=7 d6=10 d7=12 d8=19 d9=15 d10=18 d11=16 d12=14   132   7150/15565
    seed-first only   d0=2 d1=5 d2=1 d3=6 d4=3 d5=4 d6=13 d7=11 d8=16 d9= 9 d10=16 d11=10 d12=10   106  12666/15565
    + netting         d0=3 d1=3 d2=1 d3=4 d4=3 d5=7 d6=16 d7=13 d8=19 d9=14 d10=17 d11=17 d12=13   130   8958/15565

**Exact days: 0 of 13, in all three states.**

d0 is not exact and got worse, 2 cells to 3:

    state  money        ours  13   tape  16   -3
    fill   SELL         ours   0   tape   3   -3
    fill   BUY_PRODUCT  ours   5   tape   8   -3

The round trip was not free money lost — it was money *gained*. Selling 3 at h1 banked ~$87 against
the ~$75 saved by buying 3 fewer, so removing it left the day on $13 instead of $100.

## The herd degrades after netting — the mechanism Alex asked me to watch

    d              d8    d9   d10   d11   d12
    animals  seed-first   7/10  12/12  12/12  14/14  14/14
             + netting    7/10  12/12  11/12  12/14  13/14
    feed     seed-first   7/10  11/11   9/12  14/14  14/14
             + netting    8/10   9/11   8/12  12/14  13/14

The herd loses two head by d11 and stays down. Weeds also start earlier: d6 under netting against
d10 without it.

**WHEAT is animal feed.** A FEED consumes one wheat. Buying nine and selling three is not a round
trip that cancels — the nine arrive as feed stock and the three leave from a shed that has already
been drawn down. Netting to six leaves the herd three rations short and the day $87 poorer. The
"nonsense" is deliberate.

## The 38 gate cells are spread, and they are the herd loop

    tests/test_each_day_matches_the_tape.py -- failing cells per day
     day   baseline   withfix    delta        day   baseline   withfix    delta
       0          4         0       -4         15         10        13       +3
       1          4         2       -2         16         13        12       -1
       2          1         0       -1         17         11        12       +1
       3          3         2       -1         18         10        11       +1
       4          3         2       -1         19         11        14       +3
       5          2         1       -1         20          8        11       +3
       6         11        12       +1         21         12        15       +3
       7         11        12       +1         22         10        14       +4
       8          9        10       +1         23         14        14       +0
       9          8        10       +2         24         10        14       +4
      10          8        13       +5         25         11        14       +3
      11         10        12       +2         26         11        12       +1
      12          9        14       +5         27         14        14       +0
      13          6        13       +7         28         10        10       +0
      14         12        11       -1         29          7         7       +0
                                              all        263       301      +38

**Answer: spread.** d0-d5 all IMPROVE, ten cells better. From d6 onward it is worse on eighteen of
twenty-four days, with no single day carrying it — the largest is d13 at +7.

The newly-failing fields say what it is. 74 field-days flipped:

    FEED                 16 days      DIG                  3 days
    CARE                 14 days      crop_STRAWBERRY      3 days
    COLLECT_FERTILIZER   13 days      WATER                2 days
    weed                  6 days      PLANT / hands / an_SHEEP / PLACE / HIRE / crop_WHEAT  1 day each
    HARVEST               6 days
    crop_MELON            5 days

**Forty-three of seventy-four are FEED, CARE and COLLECT_FERTILIZER** — the daily herd loop, and
COLLECT_FERTILIZER only fires on an animal that was fed. The ordering change puts BUY_PRODUCT WHEAT
last, it fills with whatever the seed and livestock leave, and from d6 the herd runs short of
rations every day.

So this is not "the ordering is player-specific" and not "the shipped grid was passing for the wrong
reason". It is a third answer neither of us proposed: **seed-first buys the ground and starves the
animals**, and the opening days improve while every later day pays for it.

## Recommendation

Both changes should be reverted, and neither is reverted here.

- **Netting**: measured worse on every headline (cells 106 to 130, d12 money -$3,708, herd -2 head).
  The hypothesis that it was nonsense is disconfirmed.
- **Seed-first ordering**: buys 26 cells on d0-d12 and gives back 48 across d6-d27 on the shipped
  gate, all in the herd loop. The right form is probably neither ordering but a *reservation* — feed
  wheat sized to the standing herd, taken out before both the seed row and the product row, which is
  what `SEED_BEFORE_LIVESTOCK`'s own docstring describes for a different pair.

Nothing is deleted, disabled or gated behind a flag. Both remain live for Alex to decide.

## A git accident I caused and repaired

`git stash push kagg/search/schedule_agent.py` found nothing to stash — the fix was already
committed — and returned 0 anyway, so the following `git stash pop` popped **Alex's** `stash@{0}`
instead. It conflicted and left `tests/test_router.py` in a `UU` state. Repaired with
`git checkout HEAD -- tests/test_router.py`; all four stash entries are intact and nothing was lost.
The true baseline was then taken by swapping in `git show 706d49b~1:kagg/search/schedule_agent.py`
rather than by stashing.

The earlier 263 figure was correct. The 301 I briefly labelled "baseline" was a with-fix run.

## Unverified

- One seed, one game, one tape.
- The feed mechanism is inferred from which fields flipped, not from a turn-level trace of a FEED
  failing for want of wheat. That trace has not been taken.
- Whether a feed reservation fixes both. Proposed, not measured.
- Netting was applied to all 30 days; no per-day breakdown of where it hurts most.
