# We are cloning rank 9, and the leader is 261 points above him

Measured 2026-08-23 from `data/leaderboard_2026-08-21.json` (5,724 teams) and 6 replays per player.

## The standing that matters

     rank  team                       rating
        1  Ryo Hasegawa               3151.8
        2  tetsuya                    3046.4
        3  Arman Tuganbaev            3012.8
        4  Subramanya N               3007.9
        5  Izzoudine Mohamed KANTA    2990.9
        9  カワシギ                     2890.6   <- the player the shipped agent replays
       15  Seb (allegedly)            2820.8
       91  alex chilton               2565.1   <- us

**The ceiling of the current approach is roughly rank 9.**
A byte-perfect replay of カワシギ scores what カワシギ scores.
The 325 points between us and him are reachable by fixing the replay; the 261 between him and the
leader are not reachable by copying him at all.

This is the single most important number on this page and it was not measured until today.

## How the top two differ from our teacher

Six games each, our teacher's own seat, unit-op mix as a percentage of all unit actions.

                        #1 Ryo Hasegawa   #2 tetsuya      #9 カワシギ
    rating                     3151.8        3046.4          2890.6
    money mean                 96,314        94,102          88,998
    money range         63,931-165,959  61,414-147,879  44,933-121,562
    tiles owned mean             75.0          75.0            79.2
    PASS                          4.0%         18.9%            9.1%
    WATER                        16.3%         10.5%           13.7%
    HARVEST                       5.5%          5.5%            5.7%
    FEED                          4.2%          4.6%            4.7%
    animals (6 games)      65C / 28S    54C / 24S / 12G    46C / 35S

**PASS is the striking one.** The number one player idles on 4.0% of unit-actions against tetsuya's
18.9%, and he does it while owning FEWER tiles than カワシギ (75 against 79.2) and banking more.
That is not a bigger farm, it is a busier one, and WATER being his top op at 16.3% says where the
turns go.

Treat the money means as indicative only: each player faced a different field, so they are not
directly comparable. The op percentages are internal to a player and do not have that problem.

## Sell ORDERS posted -- offers, not fills

`kagg/analysis/fills.py` exists because the agent re-posts an order every turn. These are counts of
orders SUBMITTED and must never be read as revenue.

    Ryo        FERTILIZER  452, MILK 307, WHEAT  243, STRAWBERRY 200, WOOL 133, MELON 53, CARROT 22
    tetsuya    FERTILIZER  386, MILK 241, WHEAT  200, STRAWBERRY 165, WOOL 100, EGG   68, MELON 42
    カワシギ     FERTILIZER 1230, WHEAT 1126, WOOL 182, MILK 182, STRAWBERRY 153, MELON 64, CARROT 19

カワシギ posts **5 to 6 times more** fertilizer and wheat orders than either leader.
Because these are re-posts, a high count means an order sat on the book unfilled for many turns.
So our teacher is offering into a book that is not taking it, which is the same shape as the wool
finding measured today -- 38 WOOL held to the final bell at a price of 223.

Worth testing rather than assuming: whether the leaders post fewer orders because they size them to
the drain, or because they simply produce less of what the town will not buy.

## Geese

tetsuya runs 12 geese across 6 games. Ryo runs none, カワシギ runs none.
The geese branch here was measured and switched off (`c9c1c18`, `7a88d30`), which is consistent with
the two players either side of tetsuya in the standing.

## Caveats

- Six games per player. Small.
- The leaderboard snapshot is 2026-08-21, two days old, and our own rating has since had three
  submissions land on it.
- `top_guys/` is stale (newest 2026-08-09), but the wider corpus is not: **1,785 replay files newer
  than 2026-08-15** sit under `data/`. An earlier claim in this session that the corpus was two
  weeks stale was wrong and is retracted here.

## What this suggests, unmeasured

The imitation track is capped at カワシギ's rating by construction. Raising the ceiling needs either
a better teacher -- Ryo's replays are in the corpus, ~125 of them by extrapolation from a 400-file
sample -- or the policy-improvement step that imitation was always meant to bootstrap.
Neither is started, and this document does not argue for either; it records the number that makes
the question worth asking.
