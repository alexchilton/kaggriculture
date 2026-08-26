# The "6/6 plus an extra parcel of crops" pattern is a story

2026-08-25.
Question from Alex: the players who ran COW 6 / SHEEP 6 well did it by also buying an extra parcel
and putting effective crops on it -- is that real, and do tetsuya or Ryo do it?

Answer: **no.** Two independent reasons, below.

## Method

303 seats where `info.TeamNames` EXPLICITLY contains `tetsuya` (119 seats) or `Ryo Hasegawa`
(184 seats), across `data/seed_scripts/{ryo, downloads_2026-08-19, downloads_2026-08-20,
downloads_2026-08-21, kawa_2026-08-24, leaders_2026-08-24}`.
Games without a name match were SKIPPED, not guessed -- `replay_fills.seat_of` returns 0 on a miss
and that bug produced a withdrawn "1291 kawa seats" table earlier the same day.
`tetsuya/tape.json` and `tetsuya_93866112/schedule.json` carry no `info.TeamNames` and are excluded.

## Land is universal, so it cannot distinguish anything

**303 of 303 matched seats finish with 3 quadrants (NW + NE + SW).**

    tetsuya   buys NE on day 7 in 119/119 games, SW on day 9-11
    Ryo       buys NE on day 5-6,                SW on day 9-10

Every named seat buys land. A variable with no variance explains nothing, so "6/6 *plus* land"
cannot be what separates good 6/6 runs from bad ones.

## 6/6 is their WORST herd, not their winning one

25 seats finish 6/6 (19 tetsuya, 6 Ryo).

    tetsuya   6/6      mean 73,103   n=19
    tetsuya   non-6/6  mean 97,567   n=100
    tetsuya   best 4 COW / 10 SHEEP  113,171  n=9
    tetsuya   best 12 COW / 3 SHEEP  110,628  n=22

    Ryo       6/6      mean 82,438   n=6
    Ryo       non-6/6  mean 96,141   n=178
    Ryo       best 14 COW / 2 SHEEP  141,660  n=8

When these players land on 6/6 they earn LESS. Nobody "ran 6/6 successfully".

## What is actually on the extra ground: animals, not crops

Across all 119 tetsuya seats the extra quadrants hold **368 SHEEP, 333 COW, 246 WHEAT** tiles
against only **59** tiles of tomato/strawberry/carrot combined.
For the 19 tetsuya 6/6 seats: 57 SHEEP, 19 COW, 27 WHEAT, 20 berry/carrot.

The parcel is a pasture-and-feed extension, not a crop expansion. The wheat on it is feed.

Representative games:

    downloads_2026-08-19/93887862.json  seat 0  tetsuya  97,315   NE d7  SW d11
                                        extra: 1 WHEAT 3 SHEEP 1 COW 5 STRAWBERRY
    ryo/94404229.json                   seat 1  Ryo     122,717   NE d5  SW d9
                                        extra: 4 COW 1 SHEEP 4 WHEAT
    downloads_2026-08-19/93896734.json  seat 1  tetsuya  59,997
                                        extra: 1 WHEAT 1 COW 3 SHEEP

## The real pattern, and what would have to be true for it to pay for US

Two extra quadrants by about day 10, used as pasture plus wheat feed, scaling the herd to ~14-15
animals.

For that to pay for us the added heads must go into the animal whose book we are NOT flooding --
**cows**. Consistent with ladder game 99114898, where 12 sheep took WOOL from $239 to $11 on 57 units
and cows out-earned sheep per head. More sheep on new ground only deepens our own wool crash.

## NOT checked -- stated so it is not read as covered

- **Final step only.** Animals sold before day 30 are invisible, so "6/6" means "FINISHED 6/6",
  not "ran 6/6".
- Whether extra-ground WHEAT is fed or sold, and how hands are allocated to the new parcels.
- カワシギ (407 seats) and peikopon (206 seats) -- the question named tetsuya and Ryo only.
- Two duplicate episodes are double-counted (`94381641` in both `downloads_2026-08-19` and `-08-20`;
  `94442273` in `ryo/` and `downloads_2026-08-20`). Removing them moves no mean by more than ~1%.
- **Association only, not causality.** Opponent strength and per-game price context were not
  controlled, so "6/6 seats earn less" is not "6/6 causes earning less".
