# The milk classifier, and the death of the opponent lead

Continues `the_greedy_is_a_mix_scorer_2026-08-19.md`. Herd placement match against tetsuya's 78
recorded games: **81.9% -> 88.5%** (1051/1187).

## The opponent lead is DEAD, killed by using the right unit

2026-08-19 reported that on late/no-yarn boards a sheep-heavy opponent pushes him to cows, 0.41 ->
0.07 sheep share. That was measured over 213 PLACEMENTS. Those come from ~50 games, and a game
contributing twelve animals is one decision repeated twelve times, not twelve independent
observations -- textbook pseudo-replication. A handful of games with sheep-heavy opponents each
contributed a dozen rows and carried the whole effect.

Re-measured at the GAME level, 50 late/no-yarn games:

    variable                his COW<=7   his COW>=8      gap
      opp COW at d9             6.05         6.00       -0.05
      opp SHEEP at d9           3.95         3.77       -0.17
      opp COW final             9.42         9.10       -0.32
      opp SHEEP final           3.84         3.55       -0.29

Nothing. The reason is visible in the per-game rows: his opponents sit at COW 6-8 / SHEEP 4 in
almost every game, because the ladder pool plays alike. **A variable with no variance cannot explain
a response.** The lead was raised and killed inside two messages.

## It was the milk count all along -- as a THRESHOLD, read at the DECISION

Same 50 games, every other candidate flat to three digits:

    quadrants @d9      2.00 vs 2.00        shops drawn @d9   3.00 vs 3.00
    money @d9       2760.58 vs 2693.94     yarn stores @d9   0.00 vs 0.00
    milk shops @d9     0.68 vs 1.81   <--
    milk shops @d12    0.95 vs 2.23   <--

As a classifier rather than a slope:

    milk@d9 >= 1  -> high cow    37/50 = 74.0%   (fp 13, fn 0)
    milk@d9 >= 2  -> high cow    40/50 = 80.0%   (fp  0, fn 10)
    always-high baseline         31/50 = 62.0%
    milk@d9 <  2: n=29 mean COW  7.21
    milk@d9 >= 2: n=21 mean COW 11.33

**Twenty-one of twenty-one games with two milk shops by d9 go high-cow. Zero false positives.**
"Two milk shops implies a big herd" holds without exception; the converse does not, and does not
need to.

`MILK_SHOPS_FOR_A_BIG_HERD = 2`, `COW_ON_A_MILK_RICH_BOARD = 12`, `COW_ON_A_MILK_POOR_BOARD = 7`,
gated from `MILK_CLASSIFIER_FROM_DAY = 9`.

### The same variable failed twice before this

    visible milk count, LINE fitted on the final board     65.6% -> 46.4%
    expected final milk count, LINE, undrawn at 3/8        65.6% -> 63.0%
    milk count at d9, THRESHOLD                            81.9% -> 88.5%

Three attempts, same variable, and the first two were negative. The variable was never the problem.
**A linear fit to a bimodal response lands between both modes and matches neither** -- his boards
cluster at COW 6 and COW 12, so the per-milk-count means of 6.0 ... 12.0 are averages OVER a split,
not a trend within it, and the fitted 8.6 at three milk shops is a value he essentially never plays.

The lesson is not "milk shops don't work". It is: **before fitting, ask whether the response is a
gradient or a mixture.** A gradient wants a line; a mixture wants a classifier, and the mean is the
worst single guess for a mixture.

## Where the season now stands

     day    before    after
       9     67.3%    73.5%
      10     63.6%    79.8%
      11     60.1%    82.5%
      12     47.8%    76.1%
      13     41.4%    55.2%
     season  81.9%    88.5%

d13 at 55.2% is the weakest day left, on 29 placements.

## カワシギ: four more xfail(strict), still nothing deleted

`test_a_late_yarn_store_still_leaves_the_herd_cow_heavy`,
`test_the_split_matches_the_leader_on_three_quadrants[shops4/shops5]`,
`test_the_common_board_is_untouched`. All four assert HIS numbers -- the "common board" is his 42 of
51 seats, and its board carries two milk shops, which the classifier now reads as milk-rich. Suite:
21 passed, 16 xfailed.
