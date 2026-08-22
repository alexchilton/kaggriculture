# Two hands pass all day, three animals starve, and one escapes

Measured 2026-08-20 on tetsuya's board `data/seed_scripts/downloads_2026-08-19/94345389.json`,
seat 0, seed 959074148, following `data/seed_scripts/tetsuya/schedule.json`.
Raw hour-by-hour dump: `data/logs/d4_2026-08-20.log`.
Feed/care landed counts: `data/logs/feedcare_landed_2026-08-20.log`.

## The chain, end to end

    two hands never assigned  ->  3 pens unfed on d4  ->  escape at d4 night
       ->  herd 7 vs his 8 on d5, 1-3 short every day after
       ->  fewer mouths  ->  FEED and CARE counts trail his all season

Every link is measured. None of it is inference.

## d4, our side

Row is `feeds=8 places=['COW','COW'] buys={'WHEAT': 6}`. Seven pens reach the ground. Four are fed.

    h0   idle=1  PASS                                     pens=CO- SH- SH- CO- CO- SH-
    h9   idle=2  WEST,WATER,WEST,PASS,FEED,WEST,WEST,PASS  pens=CO- SH- SH- CO- CO- SH-
    h13  idle=2  FEED,CARE,WATER,PASS,FEED,EAST,WATER,PASS pens=COF SH- SH- CO- CO- CO- SHF
    h20  idle=5  PASS,WEST,SOUTH,PASS,PASS,SOUTH,EAST,PASS pens=COF SH- SHF COF CO- CO- SHF
    h22  idle=6  PASS,PASS,EAST,PASS,PASS,EAST,HARVEST,... pens=COF SH- SHF COF CO- CO- SHF
    h23  idle=6  PASS,PASS,DROP,PASS,PASS,EAST,NORTH,PASS  pens=COF SH- SHF COF CO- CO- SHF

Two observations, both plain in the dump:

- **Slots 4 and 8 are `PASS` in every hour of the day.** Two hands are never given a job at all.
- **Idle climbs 2 -> 6 after h17** and the day ends with three unfed pens standing.

About 67 unit-turns idle on d4. The three missing feeds and three missing cares cost six.

## Why it is expensive

`reference/kaggriculture.py:817` replaces an animal on `consecutive_unfed >= 2` with a bare
structure. One of d4's hungry pens had also missed d3, so it escapes overnight and our herd reads 7
on d4 and 6 on d5. The code comment at `schedule_agent.py` puts an escape at a $400-$500
write-off, and the pen has to be restocked to get back to level.

## What this reframes

`PASS 911 vs his 679` over d0-d10 was carried as a separate open item from `FEED`/`CARE`.
**It is the same item.** We idle exactly the turns that should feed the herd.

It also demotes the op-count gap. FEED and CARE trail his because our herd is smaller, and our herd
is smaller because we starved one. Chasing the op counts directly was chasing the last link.

## Not the cause -- ruled out by measurement

- **Wheat supply.** Every FEED we sent on d4 landed (4 sent, 4 landed). Nothing failed for lack of
  a carried ration.
- **The arrival budget.** `ARRIVAL_FEED_REMAINING = max(0, row_feeds - standing - arrived_fed)`
  computes 2 on d4 for two arrivals, which is correct. Standing pens do not consult it.
- **`will_be_fed`.** Standing animals are not on the arrival branch and reach the unconditional
  `return True`.
- **The market slot gate.** Measured inert twice; see `SUPER_IMPORTANT_READ_THIS_FIRST.md` §8.

## The test to write first

d4 on this board and seed: seven pens on the ground, seven feeds landed, and the herd still 7 at
dawn on d5. Write it RED, confirm it goes red on revert, and judge the fix on the **d0-d10 grid**,
not on the test -- §4 of `SUPER_IMPORTANT_READ_THIS_FIRST.md` records two feed fixes that passed
their own tests and lost the season.

## Caveat

One board, one seed. The idle-hand pattern should be confirmed on a second of his seats before a
fix is tuned to it. Seeds are not stored in the replays and have to be recovered by search, so this
is not free.
