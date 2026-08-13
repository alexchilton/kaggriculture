# We are not losing badly. We are losing narrowly, 54 times.

Measured on **60 downloaded ladder games** of our own agent (`data/seed_scripts/ours_ladder/`),
2026-08-13.

    59 scored games      5 wins, 54 losses      win rate 0.085
     1 further game      TIMEOUT / TIMEOUT at step 531 of 720 (91304798, self-play, seed 0)

The margin distribution is the whole story, and it is not what a 0.085 win rate suggests.

## What a dollar buys, in wins

    gain per game    losses flipped    wins    win rate
             $0                  0       5       0.085
           $500                  3       8       0.136
         $1,000                  5      10       0.169
         $2,000                  9      14       0.237
         $3,000                 13      18       0.305
         $4,000                 16      21       0.356
         $5,000                 18      23       0.390
         $6,000                 23      28       0.475
         $8,000                 28      33       0.559
        $10,000                 31      36       0.610
        $15,000                 42      47       0.797

**+$6,000 a game is the difference between 8.5% and 47.5%.** Eleven of the 54 losses are inside
$2,100, six inside $600, and two inside $150 -- `-$70` against TrebolNoir_ and `-$135` against Mirza
Yasir Abdullah Baig.

This is the concrete form of the standing rule in `CLAUDE.md` that the ladder is an Elo rating and
money is the wrong selection criterion. A $70 loss and a $39,200 loss cost the same rating, and we
have far more of the first kind than anyone reading a season total would guess. The five wins are
by $13.9k, $13.5k, $78.4k, $91.0k and $65.2k -- we win big and lose small, which is precisely the
shape that scores worst on an Elo ladder.

## What this changes about prioritisation

A change worth $2,000 a game is not a rounding error to be dismissed against a $71k season. It is
+15 points of win rate. Every arm in `docs/carrot_swap_2026-08-12.md` was judged against a season
total and called a loss; the right question was always how many of the 54 it would have flipped.

It also means the search should stop optimising the mean and start optimising the count. Two
candidate framings, neither measured yet:

- **The near-miss set.** Eleven games are inside $2,100. Their seeds are known. A sweep that scores
  on those eleven alone answers "does this flip a game" directly, instead of inferring it from a
  mean that a single $91k win dominates.
- **Margin-aware selection.** Selecting on `sum(money)` across a seed set rewards the $91k win that
  was already won. Selecting on `count(margin > 0)` is the actual objective.

## What is NOT the cause

Checked and closed the same day, so they are not re-derived:

- **Stranded stock.** The final shed on seed 11 is completely empty -- 0 units of all nine products,
  $0 of value. `LIQUIDATE_LAST_DAY` does its job. There is no unsold inventory to recover.
- **A single catastrophic matchup.** The losses are spread across 54 distinct opponents with no
  repeat structure; the worst is -$39,200 and the median is about -$8,900.

## The timeout is separate and unquantified

`91304798` is a self-play validation episode on seed 0 that ended `TIMEOUT/TIMEOUT` at step 531 of
720. One game out of 60, and it is our own agent on both seats, so it does not sit in the ladder
sample above. It is recorded here because a timeout is a loss no dollar figure can show, the env
allows 1s/turn, and nothing in this project currently measures our per-turn latency.
