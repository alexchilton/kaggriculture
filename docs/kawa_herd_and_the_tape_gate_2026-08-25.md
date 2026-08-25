# カワシギ: we match his placements, we beat him 60.5%, and he starves 42% of his sheep at d27

2026-08-25.
Scripts: `scripts/gate_tapes.py`, `scripts/kawa_placed_herd.py`, `scripts/how_many_sheep_does_he_kill.py`,
`scripts/his_last_feed_day.py`, `scripts/when_do_his_sheep_die.py`, `scripts/herd_three_ways.py`.
Logs: `data/logs/kawa_arm_old.log`, `data/logs/kawa_arm_matched.log`, `data/logs/kawa_placed.log`,
`data/logs/how_many_sheep.log`, `data/logs/his_last_feed_day.log`.

## CORRECTION: an earlier draft of this file led with "we lose to him 32.9%". That was the wrong arm.

The 32.9% was measured on `main_matched.py` -- a build made that afternoon to force the sheep down
to 2, which was then measured and **reverted**. It is not our code and never was. The shipped agent
is `main_ship.py`. Both ran the same 76 tapes with the same seatings:

    agent                              W    D    L   win rate   mean ours   mean theirs
    main_ship.py     (shipped)        46    0   30      60.5%      92,401        91,818
    main_matched.py  (REVERTED)       25    0   51      32.9%      90,465        93,604

Seat-0 break-even is ~54%. **We are winning against him at 60.5%.** Forcing the herd's sheep down to
2 cost **27.6 points**, which is the strongest single measurement of the day: sheep carry real money
and the temptation to cut them is expensive.

The same draft also said "we are not matching his placements, we run +2 cows / -2 sheep". That table
was read off `kawa_arm_matched.log` as well. It described the reverted arm.

## The placements DO match

    his PLACED (76 seats)          ours, shipped (same 76 games)
      10/4 = 14   41   53.9%         10/4 = 14   44   57.9%
      6/12 = 18   17   22.4%         6/12 = 18   16   21.1%
       6/8 = 14   12   15.8%          6/8 = 14   11   14.5%

`PLACE` is the right count: a unit op, emitted once, and you cannot place an animal you do not own.
`BUY_ANIMAL` is a market order the agent re-posts every turn and it overcounts
(`feedback_offers_are_not_fills`).

`_herd_split` (`schedule_agent:3006`) reproduces this and needs no change. Verified directly:

    season 12/2  bought {}                 -> {'COW': 10, 'SHEEP': 4}
    season 12/2  bought {'COW':10,'SHEEP':2} -> {'COW': 10, 'SHEEP': 4}
    season  7/7  bought {}                 -> {'COW': 10, 'SHEEP': 4}

## What we do NOT match: he lets 42% of his sheep go, and he does it at d27

    SHEEP LET GO PER SEAT              BY HOW MANY HE PLACED
       lost  seats   share               placed  seats  mean lost  mean kept
          0      6     7.9%                    4     41       1.71       2.29
          2     44    57.9%                    8     12       3.50       4.50
          4     14    18.4%                   12     17       5.12       6.88
          5      2     2.6%
          6     10    13.2%               he keeps 58.1% of the sheep he places
      mean 2.82

    COWS LET GO PER SEAT:  0 in 76 of 76 seats.

Not a fixed count -- **a fixed fraction, ~42%, at every herd size.** And never a cow.

There is no selling animals in this environment (Alex): an animal leaves the board exactly one way,
by not being fed. So this is deliberate.

### The day is d27, measured off his FEED ops

The board read cannot settle this on its own -- whether the drop lands at the d28 or the d29
rollover depends on whether the last recorded observation is before or after the final `_end_of_day`,
and that is an off-by-one not worth guessing at. Counting FEED **ops** has no such ambiguity.

    day   feeds   pens   share fed
     26   13.45  15.01     89.6%
     27    8.47  15.01     56.4%
     28    8.72  15.01     58.1%
     29    0.00  12.20      0.0%

His last day with any FEED is **d28, in 100% of seats**. Escape needs two unfed days
(`kaggriculture.py:817`), so the sheep he loses are the ones he stops feeding at **d27** -- they miss
d27 and d28 and are gone before d29 opens. The herd holds flat at 15.01 from d19 to d28: **nothing is
starved mid-season.**

`when_do_his_sheep_die.py` independently reports the first drop at d29 in 70 of 70 seats that lose
any, which is the same event seen from the board.

### Unexpected, and NOT acted on: he is on a feed cadence all season

The share-fed column above is not 100% from d13 onward -- 82.6% at d17, 71.7% at d21, 66.9% at d25 --
while the pen count stays flat. He feeds ~2-4 fewer pens a day than he owns, for about fifteen days,
and loses no animals doing it. `will_be_fed` (`router.py:839`) has a cadence written into it that is
unreachable behind an unconditional `return True`. Worth a separate look; not touched here.

## The change made

`router.pays_for_its_ration` + `SHEEP_GO_HUNGRY_FROM_DAY = 27`, gated through `will_be_fed` so that
the plan, `underfoot()` and the wheat-purchase sizing all get the same answer from one predicate.

From d27, an animal is fed only while what it can still bank -- the yields it has left plus the
product standing on it, because escape destroys `yield_units` with the animal
(`kaggriculture.py:819`) -- exceeds the wheat it will eat getting to the bell.

**It names no species, deliberately.** It separates sheep from cows because the book does: we flood
our own wool (ladder 99114898 took WOOL $239 -> $11 on 57 units) while milk holds, and a SHEEP eats
three wheat per unit of wool against a COW's two. A hardcoded "starve the sheep" would also starve
them on boards where wool is what is paying us -- and that is the arm that measured -27.6 points.

Test: `tests/test_the_sheep_go_when_the_wool_is_gone.py`. Red first at prize 1,000,511
(`CRITICAL` + the wool), with the three keep-alive cases passing before the fix.

### One test conflicts, and it has NOT been changed

`tests/test_the_last_day_does_no_upkeep.py::test_every_other_day_is_untouched[28]` asserts a hungry
pen is always offered FEED on d28. Its fixture is `_pen("COW", placed_day=0, yield_units=0)`, whose
d29 rollover is `(29-0-8) = 21` -- odd, so a COW at `interval` 2 **does not produce**, and it holds
nothing. The feed buys nothing, and the test's stated reason ("d28's feed still pays out at the d29
rollover") does not hold for its own pen.

The rule cannot be narrowed around it: a sheep needs d27 **and** d28 unfed to escape, so exempting
d28 makes the whole change a no-op. Left failing pending Alex's call.

## The late starve pays, and NOT for any of the reasons assumed

`main_starve.py` -- the first, species-agnostic cut -- against the shipped baseline on the same 76
tapes, 60 games pairing cleanly:

    win rate   60.5% -> 64.5%      W/D/L  46/0/30 -> 49/0/27
    money      mean +$480   sem 128   t=3.75   richer in 43/60
    flips      5 losses -> wins, 2 wins -> losses

Split by which species actually left the board:

    what died    games    mean $     sem  richer    cows sheep   W/L flips
    cows only       16      +775     172  14/16      5.3   0.0   +3
    sheep only      16      +715     259  12/16      0.0   3.7   +0
    both            14      +502     284  11/14      5.1   3.1   +0
    neither         14      -148     260   6/14      0.0   0.0   +0

**Three things this says, and two of them kill assumptions made earlier the same day.**

1. **The money is in the animal LEAVING, not in the ration or the turn.** The `neither` row is games
   where the rule skipped feeds and nothing died: **-$148**. Skipping the feed on its own is worth
   nothing. That retires "free the FEED turns for harvests" as the mechanism.

2. **Cow and sheep are worth the same per GAME, and the sheep is better per HEAD.** +775 from 5.3
   cows is $146 each; +715 from 3.7 sheep is $193 each. So matching him -- never a cow -- costs the
   `cows only` bucket but keeps the better per-head trade.

3. **He does this for a different reason than we would.** He PASSes **29.95 times on d28 and 45.46
   on d29** (`scripts/what_he_does_with_the_last_three_days.py`) -- he is not short of turns at the
   close. We are. The same act pays us and cannot be paying him, so his motive is still unexplained
   and the wheat a skipped feed saves (~12 units, ~$250) is the only candidate left.

### The strawberry hypothesis is refuted

Standing crop on his board at d27, cut by how many sheep the seat loses:

    lost  seats   crop units held (mean per seat)
       0      6   WHEAT 50.5  STRAWBERRY 35.0  CARROT 4.5
       2     44   WHEAT 52.8  STRAWBERRY 33.8  CARROT 4.5
       4     14   WHEAT 50.5  STRAWBERRY 33.6  CARROT 2.8
       6     10   WHEAT 55.5  STRAWBERRY 33.7  CARROT 1.3

Flat at ~34 units whether he starves none or six. He is not trading sheep for strawberry.

### The cadence, measured per pen

Tracking `consecutive_unfed` on each individual tile rather than counting FEED ops in aggregate
(`scripts/which_days_the_dying_sheep_go_unfed.py`):

    DYING SHEEP -- last day the pen is on the board     SURVIVING SHEEP -- highest counter reached
       day   pens   share                                  max   pens   share
        28    214   100.0%                                   0     74    24.6%
                                                             1    227    75.4%

Every dying pen is standing at the end of d28 and gone by d29, so its second miss landed at the d28
rollover: unfed on **d27 and d28**. And the control matters -- his season-long cadence reaches
`consecutive_unfed` 1 on three quarters of surviving pens and **never once reaches 2** in 301 pens.
Skipping a feed is routine; the second consecutive skip is the decision, and he makes it on one day.

**This was asserted before it was checked.** An earlier version of this file gave d27 as measured
when only "his last FEED day is d28" had been measured and d27 was inferred from the escape rule.
The inference happened to be right. It was still a guess wearing the grammar of a fact.

## The cow guard: costs money, costs no wins, and the selection criterion decides it

Three builds, same 76 tapes, 60 pairing cleanly. `no cow guard` is the species-agnostic rule that
reads only the book; `cow guard` adds `if animal != "SHEEP": return True`.

                                             n    money   sem     t     wins    flips
    baseline -> no cow guard                60    +480   128   3.75   34->37   +5/-2
    baseline -> cow guard                   60    +263   115   2.29   34->38   +4/-0
    no cow guard -> cow guard               60    -217    91  -2.38   37->38   +2/-1

      baseline       W34/60    cows lost in  0 games   sheep lost in  0
      no cow guard   W37/60    cows lost in 30 games   sheep lost in 30
      cow guard      W38/60    cows lost in  1 game    sheep lost in 30

**Both beat the baseline.** The guard costs about half the money, exactly as the bucket split
predicted (+263 against +480, the `cows only` bucket being +775 over 16 games).

**On money the unguarded arm wins; on wins they are tied.** 38 against 37 with three discordant
games out of sixty is noise. And this repo selects on **win rate, not money** -- the ladder is Elo,
where a $480 win and a $263 win score identically (`CLAUDE.md`).

The one asymmetry that is not noise-shaped: the guarded arm goes **+4/-0** and the unguarded one
**+5/-2**. Matching him regressed nothing; letting cows go gave two wins back.

**A prediction that was half wrong, recorded because the halves came apart.** Before the guarded arm
finished it was called at "+200 to +300, a weaker result". The money was right. "Weaker" was wrong,
and wrong because it was measured against the wrong quantity -- the criterion here is wins, and on
wins the guard is not weaker. The same error the repo already records as *select on win rate, not
money*, made again inside a session that quoted that rule.

## Why the tape gate exists

`gate_pool`'s members are all `heuristic.make_agent` with different dials: same routing, same hiring,
same sell cadence. It varies crop mix and nothing else, and it is saturated -- nine of ten opponents
pinned at 100% at 8 seeds AND at 24 seeds (480 games), returning 95.0% for two different herd rules.
A recorded leader differs in HOW it plays.

`gate_tapes.py` pins three things, each a mistake already made in this repo:

  * `env_config`     -- the economy the tape was recorded on (`townCenterSellInterval` 12 -> 24).
  * `recorded_shops` -- the shop draw READ off the recording, not derived from a seed.
  * `--team`         -- without it the opponent is whoever WON each game, which on `top_guys` is
                        Seb, Sophie and OUR OWN past ladder seats.

76 of 1180 files in the post-change dirs contain him. He sat at seat 0 in 33 and seat 1 in 43; we
always seat him at 1, so in 33 games he replays with worse market priority than he recorded, which
understates him.

## Three changes tried today, and what happened

| change | verdict | evidence |
|---|---|---|
| carrot seed cap | **KEPT** | carrot held at bell 8 -> 4 (s700), 8 -> 2 (s701); 1-4 across 8 seeds |
| d27 bell guard | **REVERTED, negative** | worse in 27 of 38 paired tapes, sign test p~0.012, mean -$302 |
| greedy herd | **REVERTED, null** | mean +199, sem 1,022, t=0.19 over 38 paired tapes |
| sheep absolute target | **REVERTED, -27.6 points** | 60.5% -> 32.9% on the 76 kawa tapes |
| late starve at d27 | **MEASURING** | `data/logs/kawa_arm_starve.log` |

## Measurements withdrawn today, and why

- **"1291 kawa seats, mode 10/4"** -- `replay_fills.seat_of` returns 0 when the name is absent, so
  the scan read seat 0 of every unmatched game. Real: 407 games contain him, 76 post-change.
- **"0 seats at 6/6 out of 3,224"** -- a farm has no `animals` key. Livestock is `tile["animal"]`.
- **"the gain came at d23/d26"** -- three changes stacked in one comparison. Isolated, byte-identical.
- **"we lose to him 32.9%"** and **"we run +2 cows / -2 sheep"** -- both read off the reverted arm's
  log. See the correction at the top.
- **"he stops feeding once the wool book is crushed"** -- a hypothesis in the earlier draft, written
  as if measured. The timing is calendar-driven: d27, flat herd until then.

## Still not checked

- Whether the freed FEED turns convert into harvests. That is what the running arm measures.
- The season-long feed cadence above.
- Wheat seed over-buy: 12-20 seeds unsown every season, $120-200. Confirmed, unfixed.
