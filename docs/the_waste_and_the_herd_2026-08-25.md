# The waste, and the herd rule — 2026-08-25

## 1. The waste is ~$1,000 a game and it is ONE defect, not two

Measured on two downloaded ladder losses, reading `private["seeds"]` and tile `yield_units` at the
final step.

```
99370605  (lost by $329)
  us      unsown seed CARROT 8, WHEAT 12   $280   standing WHEAT 24 + STRAW 1 + CARROT 3   $1,004   total $1,284
  Khalid  unsown seed CARROT 1, WHEAT  8   $100   standing WHEAT  1 + STRAW 2              $65      total $165

99361310  (lost by $12,165)
  us      unsown seed CARROT 10, MELON 1, WHEAT 19  $470  standing WHEAT 13 + CARROT 2  $683  total $1,153
  them    unsown seed WHEAT 1                        $10  standing WHEAT 4              $184  total $194
```

99370605 was lost by $329. Our waste alone is $1,284. Fixing it flips that game.

### The per-day trace, 99370605

```
day |  seed held (dawn)          | BUY_SEED that day        | PLANTs
  6 | WHEAT 4                    | STRAWBERRY 3, CARROT 8   |  2
  7 | CARROT 8, STRAW 1, WHEAT 4 | STRAWBERRY 1, WHEAT 4    |  2
 ...  CARROT stays at exactly 8 every dawn from d7 to d29 ...
 26 | CARROT 8, WHEAT 12         | WHEAT 11                 | 13
 27 | CARROT 8, WHEAT 11         | WHEAT 12                 | 11
 28 | CARROT 8, WHEAT 12         | {}                       |  0
 29 | CARROT 8, WHEAT 12         | {}                       |  0
```

**Alex's read, and it is the correct one:** the wheat buffer and the standing wheat are the same
waste. Wheat's `first_yield_day` is 2, so a d27 planting ripens on **d29** — the last day. d28 and
d29 plant nothing and collect little, so the standing WHEAT 24 at the bell IS the d26/d27
plantings. The unsown seed is just the part that never got into the ground.

Consequence: a cap of the form `remaining_schedule_rows[crop] - held` is **too weak**. The tape's
own row genuinely asks for `WHEAT 11` on d27, so that cap authorises the buy. The bound must be
**harvestable**, not **plantable**: no buy and no plant unless `plant_day + first_yield_day` leaves
a day a unit will actually stand on that tile.

### The mechanism, and whether its old justification still holds

`schedule_agent.py:5244`

```python
short = max(short, _row_q - max(0, _bought))
```

The line above already nets held stock (`short = qty - seeds[crop]`). This floor replaces that with
the tape row's PURCHASE total, so the row is re-bought daily however full the store is.

Alex asked whether the reason at `:5231` is still valid. **The justification was measured where the
waste does not happen.** Its evidence is Seb's tape, seed 11, days 6-7 — inside the d4-d11 tape
zone. The waste is d20-d29, in the planner zone. Both can be true at once, which is why a cap that
only binds late leaves the old fix untouched.

### Still unexplained — do not skip this

- The d6 CARROT block: the row asks for **7**, we buy **8**, and never plant one of them for 23
  days. The over-buy by one and the total failure to route to them are both unexplained.
- kawa's own rows buy wheat on d27, so the tape does this deliberately and presumably collects it.
  Khalid ended with 1 unit standing against our 24. **The defect may be harvest routing at d28-29,
  not the planting decision.** `scripts/should_we_plant_that_far_that_late.py` prints planted_day x
  distance for standing vs collected tiles and is the discriminator. Run it before cutting plantings.

## 2. The herd rule: mirror and kawa-fit point OPPOSITE ways

`scripts/the_herd_against_the_drain.py` — shops forced via `scripts/force_the_shops.py`, revealed on
the real cadence (first at d3, one every third day), mirror against the shipped agent.

The live rule is `schedule_agent.py:3010-3019`, a **presence test**: one YARN_STORE in the first
three draws caps cows at 6 and pours every other head into sheep. It `return`s before the block at
`:3021-3041`, which ranks the species by `town_drain_remaining` + `expected_future_drain` and
assigns heads greedily. That demand-aware code exists and never executes.

(The `_milk`-computed-and-discarded block at `:2990` is behind
`HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE = False` and never runs. It is not the defect.)

### Mirror, 8 seeds, 144 games

```
arm                win   games   mean ours
ship               54%      48      91,114
greedy             98%      48      99,468
proportional       94%      48      98,536
```

`ship` at 54% is the **seat-0 baseline** — identical agent both sides, seat 0 holds the order-slot
edge. `greedy` is nothing new: `WOOL_SHOP_SETS_THE_HERD = False`, so `:3021` runs.

### Against 60 of カワシギ's own seats

```
rule            exact COW  within 1  mean |err|
ship                  62%       62%        1.43
greedy                 0%        0%        3.32
proportional           0%        0%        4.38
```

`greedy` reproduces him **0%** — it says COW 11-12 on nearly every town (his milk drain usually
exceeds his wool drain) where he plays 6 or 10.

**The two tests disagree and neither has been dismissed.** The likely reason: the mirror gives
greedy a FIXED opponent playing the shipped herd, so greedy may win by taking whatever product the
opponent is not flooding — anti-correlation, not town-reading. On a ladder of kawa clones that
exploit is real. But it is the same shape that reversed the melon sweep (25 -> 12 -> 25).

Deciding it needs greedy-vs-greedy and greedy-vs-pool, not another mirror.

### Running at the time of writing

`scripts/the_herd_against_the_drain.py` extended with `cow4..cow14` arms — 9 arms x 6 worlds x 8
seeds = 432 mirror games, pinning the cow count directly to find what actually wins per shop world,
rather than asking which rule predicts it. Log: `data/logs/herd_cow_sweep.log`, rows stream to
`data/logs/herd_cow_sweep.csv`. It was at 40/432 when this was written; **read the log, do not
assume it finished.**

## 3. Red test written, not yet made to pass

`tests/test_the_season_does_not_end_holding_seed_it_never_sowed.py` pins the outcome (a finished
season must not hold more than 6 of one seed) rather than the mechanism, so it survives the fix
moving. It has NOT been run.

## 4. Fable's open items — DO NOT LOSE THESE

Carried forward from `docs/fable_sell_optimisation_2026-08-25.md`. None are done.

1. **The herd COUNT, not the split.** Ours is pinned at 14 or 18 by the schedule's rows; the field
   runs 8-22. Measured today: `sssskilo` beat us by $13,562 on **COW 6 / SHEEP 6, total 12**, and
   `PLReddy23` beat us by $86 on total 14.

   The code exists and is switched off: `HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE = False`
   (`schedule_agent.py:2955`). On the early-yarn branch it returns `WOOL_SHOP_COW_CAP=6`,
   `EARLY_WOOL_SHEEP=6` — total 12 — and its own comment records **49/51 = 96.1%** fit to kawa's
   three-quadrant seats against 82.4% for the shipped rule (`data/logs/kawa_q3_rule_search.log`).

   It was parked because "dropping the total to twelve only pays if the freed capacity becomes
   crops... we have no logic that does that". **That reason may have expired.** Two fewer animals
   is two fewer FEED and two fewer CARE per day, and section 1 measures 21-31 harvestable units
   left standing at d24-29 — the freed turns now have a measured destination. This is an inference,
   NOT a measurement. Add it as an arm; do not flip it on the strength of a comment.

   It splits on the real games: it changes 99372734 (early yarn, 6/6 vs our 6/12) and does **not**
   change 99382090 (yarn at draw 5, so the `else` branch gives 10/4 — exactly what we lost with).

2. **Subordinate `HOLD_A_FLOORED_BOOK` to a dawn-overflow projection.** Holding a floored book is
   only right while the shed will not overflow at dawn.

3. **The wool / yarn-store branch** — $18,908 measured on identical production.

4. **The seed cutoff** — $370. Superseded in part by section 1 of this doc: the bound must be
   HARVESTABLE, not plantable.

## 5. Three more losses measured 2026-08-25

```
99372734   LOST BY $86        us COW  6 SHEEP 12 | unsown CARROT 8, WHEAT 26 $420 | 31 harvestable units missed
                              them COW 6 SHEEP  8 | unsown $220                    |  2
99382090   LOST BY $13,562    them COW 6 SHEEP  6 (total 12!) | 8 missed
                              us   COW 10 SHEEP 4 | unsown CARROT 8, WHEAT 10 $260 |  6
99370605   LOST BY $329       see section 1
```

**CARROT 8 unsown in four games out of four** (99370605, 99361310 had 10, 99382090, 99372734). Same
number every time, so it is one code path, ~$160 a game, and needs no sweep to confirm. Chase this
first.

### The distance theory is DEAD

99370605, spawn (4,4) on a 10x10. Our uncollected tiles sit at distance **2-4**. Khalid's two sit at
distance **5**. We miss tiles CLOSER than the ones he misses.

```
planted TOO LATE to collect (ripe on/after d29):  6 tiles,  7 units
ripe with days to spare and NEVER collected    :  7 tiles, 21 units
```

**75% of the standing units were harvestable.** Worst: STRAWBERRY at (2,2), ripe on d23, stood 6
days, distance 2 from spawn. It is a harvest-routing defect at d24-29, not a planting-distance one.

## 6. The carrot was never a bug of ours — CLOSED, and half fixed

Corrected: an earlier version of this doc, and of the session, said the d6 CARROT block was
unexplained and that kawa plants zero carrot.
Both came from reading `plant_tiles`, which is EMPTY on d3, d5, d6 and d18-d25.
The field that records what was actually sown is `plants`.

Counted correctly over the whole schedule:

```
crop          bought  planted  never sown
CARROT            16        8           8     <- d3 buys 1, d6 buys 7, sows neither
WHEAT            144      136           8
MELON             20       20           0
STRAWBERRY        34       34           0
```

Kawa plants 8 carrot, on d21/22/24/25, and buys 8 more on d3 and d6 that he never sows.
The CARROT 8 we hold at every bell is his, transcribed faithfully by a schedule whose seed rows are
a record of his `BUY_SEED` actions.
MELON and STRAWBERRY reconcile exactly, so the rows are trustworthy and only these two crops carry
a gap.

### The fix, and what it does not do

`schedule_agent.py` — new `_plants_still_to_sow(sched, day)` beside `_pens_due_before_more_land`,
and the floor at the seed-buy site now reads:

```python
_headroom = _plants_still_to_sow(sched, day).get(crop, 0) - int(seeds.get(crop, 0))
if _headroom > 0:
    short = max(short, min(_row_q - max(0, _bought), _headroom))
```

`short = qty - seeds[crop]` is the REAL demand and is untouched, so nothing that would have been
planted goes unbought.
Only the floor — the part that deliberately orders above demand — is bounded, and only by the tape's
own remaining plantings for that crop.
At d7 the tape still has 30-odd strawberry to sow, so the headroom is wide and the `:5231` fix
behaves exactly as before.

Measured vs `contrarian`, seeds 700 and 701:

```
                 BEFORE                          AFTER
       bought  sown  held@bell  $        bought  sown  held@bell  $
s700
CARROT    13     5      8      160    ->     9     5      4       80
WHEAT    134   123     11      110    ->   134   123     11      110
s701
CARROT    15     7      8      160    ->     9     7      2       40
WHEAT    151   124     27      270    ->   139   124     15      150

season waste  s700 $270 -> $190      s701 $430 -> $190
```

**The wheat half is NOT fixed and the test is still RED** (`WHEAT 11` and `WHEAT 15` against a
`MAX_DEFENSIBLE_CARRY` of 6).
The reason is structural: the tape plans 136 wheat plantings and we make 123, so the tape's own
remaining-plantings figure stays wide until d27 and the cap does not bind.
Closing it needs the bound to come from OUR planting rate rather than the tape's, which is a larger
change and is not made.

## 7. What we grow and never collect — the harvest ledger

`scripts/what_we_buy_and_never_harvest.py`. Seed 700 vs `contrarian`.

**Correction to section 1 of this doc.** The earlier "21-31 harvestable units left standing, 75% of
the standing total" was measured by watching `yield_units` fall.
That is wrong.
`HARVEST` on a non-ongoing crop takes EVERY unit and sets the tile to `None`
(`reference/kaggriculture.py:464-469`), so a successful harvest makes the tile vanish and there is no
decrement to see.
Every collected tile was therefore scored as abandoned.
The real discriminator is what replaces the tile: `None` is COLLECTED, `{"kind": "WEED"}` is lost
(`:764-766` lifespan, `:783` unwatered).

```
2. EVERY PLANTING, BY FATE
    145 plantings  collected
     24 plantings  ROTTED, ripe and left to weed
     13 plantings  STOOD AT BELL, ripe and never walked to
      0 plantings  NEVER RIPE

   units left standing by crop: {'WHEAT': 29, 'STRAWBERRY': 7}
   HARVEST BY DAY  d20:68 d21:65 d22:40 d23:52 d24:51 d25:67 d26:54 d27:51 d28:56 d29:39
   season total harvested: 836
```

Three things follow, and two of them kill open theories:

- **d28 and d29 are not idle.** 56 and 39 units. The "we have optimised away the last two days"
  theory is dead.
- **Nothing is planted that cannot ripen.** `NEVER RIPE` is 0 of 182 plantings.
- **The one real block of pointless planting is d27 wheat.**

```
 planted  ripe  crop    tiles                                    took  LEFT
      27    29  WHEAT   (0,7)(1,9)(2,0)(3,6)(5,1)(9,1)(9,2)(9,4)    0     1 each
```

Eight seeds sown on d27, ripe exactly at the bell, each ending with one unit nobody walks to.
$80 of seed and eight PLANT actions for zero return.
Not fixed.

## 8. Fable's herd COUNT item is CLOSED — NEGATIVE

`docs/fable_herd_total12_2026-08-25.md` (in worktree `agent-a63df8cab88b0a862`), 48 games per arm,
6 forced shop worlds, 8 seeds.

```
arm                win   games   mean ours   mean theirs
ship               54%      48      91,114        91,106
total12            15%      48      83,270        94,573
```

Against the 54% seat-0 baseline, not 50%.

**The herd total never reached 12, in 0 of 48 games.** `_herd_split` runs from day 0 and the first
shop lands at d3, so with `unlocked_shops` empty the `MILK_POOR` branch fires and buys COW 8 /
SHEEP 6 during d0-d2. From d3 the early-yarn branch does ask for COW 6, but `bought` floors it and
`max()` cannot unbuy a cow. The arm measured COW 8 / SHEEP 6 = 14, not 6/6 = 12.

So this refutes 8/6. **COW 6 / SHEEP 6 remains untested** — testing it needs the day-0 branch
suppressed, and the existing `cow6` arm is not it (it pins cows at 6 and pours the rest into sheep,
giving 18).

Two things worth carrying:

- The 96.1% fit was measured on kawa's FINAL boards; the live path decides on day 0 against an
  undrawn deck. Same census-vs-decision error `WOOL_SHOP_NO_YARN_COW` already recorded at -16 points.
- The `agent-a63df8cab88b0a862` branch already fixed this, opening `_herd_split` with
  `if not unlocked_shops: return split`. The `corner` branch has no such guard.

Against the freed-capacity theory: `mean theirs` RISES in four of the five worlds where the arm
fires. Seat 1 is a fixed agent, so the only channel is the shared market — withdrawing sheep
un-floors the WOOL book and the opponent collects it.

Limit: one fixed mirror opponent, the shape that reversed the melon sweep. A negative is stronger
here than a positive would be, but it is still one opponent.

### The tape gate, baseline against the cap

`tests/test_each_day_matches_the_tape.py`, HEAD vs the working tree.

```
BASELINE (HEAD)   290 failed, 490 passed, 90 xfailed, 30 xpassed
WITH CAP          289 failed, 491 passed, 90 xfailed, 30 xpassed
```

Failures by day are identical in both except d21, 16 -> 15.
d0-d5 pass in both.
The cap costs nothing on the gate.

The 289 are pre-existing and are NOT a regression from this change.
They start at d6 and are dominated by `an_COW` / `an_SHEEP` (21 days each), which is the herd count
disagreement, not a seed one.
