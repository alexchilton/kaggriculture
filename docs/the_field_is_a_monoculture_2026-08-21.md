# The field is a monoculture, and its one reactive rule is the one we already copied

2026-08-21.
All of it read off `data/action_cache.jsonl` — 1,010 de-duplicated games — plus the live Kaggle
leaderboard (5,724 teams, pulled the same day).

## 38 of 58 players share one opening

Turns 0-71 run before any shop unlocks, both boards start identical every game, and weeds need two
unwatered days.
Two players emitting the same 72 turns are running the same code.

    kawa's opening, 38 players:  peikopon 7, カワシギ 9, James Holland 17, u 20, Michael Timbs 25,
      StackKnight 29, Syed Gillani 36, Bruce 38, Eddy Despradel 45, Lucien 47, Galaxantic 56,
      SCLim 64, HKmgikao 65, NCK 66, Utkarsh #2 77, Khalid 83, Ueddy 96, ReinFARMent 99,
      Moshel 101, TIM 151, shiggriculture 153, boatlee 244, Akhil Chinta 297, Gekkotron 374,
      automatylicza 384, Jince 402, Matteo 404, One-For-All 457, Arda Ceylan 460, hetspookjee 494,
      DeeperNet 532, Dmitry Larko 548, RicardoLópez 554, yaphel lee 562, ych~sun 775,
      Thomas Tschinkel 784, Atakan Aldemir 1288, katya barzova (unranked)

    unique openings:  Ryo Hasegawa 1, tetsuya 2, Arman Tuganbaev 3, Subramanya N 4,
                      Xiaowenhao404 11, Seb 15, Kostiantyn 16, Efe Can Celiksoy 18
    Izzoudine 5 + Kobe BRYANT 10 share one.
    ReCurSiON 13 + Victor @ Tufa Labs 21 share one.

**The only distinct agents above us are the top four.**
The same opening spans rank 7 to rank 1288, so the opening is not what separates them.

**We are in the big cluster too** — we replay his tape.
Most of our ladder games are near-mirrors, which is why every arm measured today reads plus or
minus a hundred dollars: against a copy of yourself, small edges are the only edges available.

**Consequence for any opponent pool.**
Sampling players uniformly over-weights whichever agent has the most clones.
Of the eighteen in `data/opponent_pool_ranked.json`, roughly twelve are the same agent — the whole
"mid" band and most of "low".
Effective sample size is about five.
Sample over OPENINGS, not players.

## His d3 decision reads the OPPONENT, not the town

26 of his games, 325 pairs, asking where two of his seasons first disagree:

    opponent melon>=9 same?   first-shop same?   diverge exactly at d3?   pairs
    True                      True                        0%    (0/21)
    True                      False                       0%    (0/144)
    False                     True                      100%   (16/16)
    False                     False                     100%  (144/144)

The shop draw makes no difference.
The opponent's melon count decides it outright, and the split falls exactly at 9 — which is
`melon_branch.OPPONENT_MELON`, reverse-engineered before this measurement existed.

**This corrects a claim made earlier the same day.**
`is_the_field_open_loop.py` showed カワシギ diverging at d3 in 65% of pairs and that was written up as
"he re-plans on the shop draw".
It was attributed to the only d3 event that had been thought of.
d3 is when the first shop unlocks AND when the opponent's melon count becomes decisive, and the
table above separates them.

## Nobody times the market

SELL quantity against the product's price, at a FIXED `(day, hour)` cell across a player's games, so
time is held constant.
Restricted to cells where the quantity actually varies — an earlier version averaged over all cells,
86% of which hold a constant zero, and reported `+0.00` for everyone, which was an artifact.

    player                  games   cells  median r  |r|>0.4  |r|>0.7
    Ryo Hasegawa                8     556     +0.05      35%      11%
    tetsuya                     8     289     -0.06      41%      10%
    カワシギ                      8     599     -0.13      31%       7%
    Arman Tuganbaev             8     411     -0.11      44%      11%
    Subramanya N                8     428     +0.10      37%      11%
    Kobe BRYANT                 8     349     +0.00      11%       2%

Median r is ~0 for all six, and at n=8 a third of cells clearing |r|>0.4 is what noise gives.
No evidence that anyone sizes an offer against the book.

An earlier attempt to answer this from SELL emission times is void: agents re-post orders every
turn, so the median player "sells" in 23 of 24 hours and the hour-set comparison is saturated.
Offers are not fills, one level up.

## Where that leaves the search

Reactive play exists at the top, but it is **one binary read, on one crop, at one instant**, and it
is copied across 38 players. Not established: whether anyone reads the opponent's herd, their wheat
volume, or anything after d3. Those are the open questions, and the market — not the field — is the
channel, since a four-tile wheat withdrawal moved $38,201 to the opponent on a single seed.

## Not established

- Whether anyone is opponent-reactive after d3. The `<d3` divergence column is confounded by
  players resubmitting different agents over weeks and must not be read as reaction.
- Whether the melon read is really about melon, or about how a melon-heavy opponent sells.
  Either way it is opponent-reaction.
- Whether the clone cluster's 1,245-place spread is tuning, later divergence, or submission age.
