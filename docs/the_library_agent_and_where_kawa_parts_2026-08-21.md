# The library agent, and where it parts from Kawashigi

Built and measured 2026-08-21. Continues `docs/the_middle_is_not_board_capacity_2026-08-21.md`.

**Headline: the agent is built and it LOSES to the shipped greedy planner, 0-2 on seed 11.**
$68,445 against $109,270. It is not a candidate to ship and nothing here was submitted.

The interesting part is *why*, because it is not the reason Alex expected and it is not the reason
the previous block-agent attempt failed.

## What was built

    kagg/search/kawa_rows.py            the schedule: library rows at the ends, wheat in the middle
    kagg/search/kawa_library_agent.py   schedule_agent driven by that schedule
    tests/test_the_middle_is_planted_by_the_planner_not_the_row.py   120 tests

    d0-d12     the MODAL library row for that day. Strict. No greedy planting reaches these days.
    d13-d27    the modal row with its planting replaced by a whole board of WHEAT (see below)
    d28-d29    the MODAL library row
    all days   species substituted at play time by `schedule_agent._herd_split` from the live draw

The middle asks for `["WHEAT"] * 100` and carries no `seeds` order. Under `router=True` the executor
sites one PLANT pin per entry on ground empty at dawn and then buys seed for the remaining pins, so
a row longer than the board can never bind -- the empty-tile count and the tour bind first. That is
the design the capacity measurement forced: his count is turn-bounded, so ours must be set by our
own turn budget and not copied as a number.

## The seed

**Seed 11, and it provably does not matter here.** The recordings carry `seed: null`, so there is no
recorded seed to recover. `breakdown.py` injects the recorded shop draw every turn and defaults
`--weeds` to 0.0, which between them remove every observable effect of the RNG. Verified rather than
asserted: a full 30-day grid on seed 11 and on seed 777 is **byte-identical except the header line
that echoes the seed**.

    diff data/logs/breakdown_kawa_seed11_d30_2026-08-21.log \
         data/logs/breakdown_kawa_seed777_d30_2026-08-21.log
    1c1
    < tape kawashigi   seed 11   weeds 0.0   ...
    > tape kawashigi   seed 777  weeds 0.0   ...

The `68,080/69,880 on seed 11` figure in `breakdown.py`'s own docstring predates the shop injection
and describes the harness before that fix, not the harness today.

**Weeds are 0.0 on every run, per Alex.** That switches off RANDOM spawning only. A tile left two
days unwatered becomes a WEED regardless (`reference/kaggriculture.py:771`) and that path cannot be
disabled. The ladder runs 0.005, so every number here is a **clean-room number** and must not be
carried forward as a ladder estimate.

## Q1: where the middle starts. d13 belongs to the LIBRARY.

Both boundaries, seed 11, same tape, weeds 0.0:

    boundary                                   ours         tape
    library d0-d12, greedy d13-d27           138515       150076
    library d0-d13, greedy d14-d27           140057       150076
    delta                                     -1542

Putting d13 in the middle costs **$1,542**. They do not tie. `MID_SEASON_FROM = 14`, which is also
where the crop-shape measurement put it -- his d13 is still mixed STRAWBERRY+WHEAT.

## Q2: Alex's three candidates, answered separately

> "either you got the numbers wrong or the route??? or you are too greedy with the wheat planting"

Totals over d14-d27, the greedy phase, from the grid below. "shipped" is the current agent playing
this tape's own schedule; "library" is the new agent; "tape" is Kawashigi's own actions.

    d14-d27 totals        shipped     library        tape
      PLANT ops               109         158         112
      WATER ops               648         713         580
      HARVEST ops             299         299         295
      live crop tiles, mean  n/a         59.0        56.7

**Candidate 3 is the live one, and it is exact.** The library agent plants **158 against the shipped
agent's 109 and the tape's 112 -- 45% and 41% more** -- waters 65 more times, and harvests
**exactly the same 299**. Forty-nine extra plantings and sixty-five extra waterings bought zero
extra harvest. That is over-planting relative to the watering budget, stated in the quantity that
pays rather than in weeds.

**Candidate 2, the route, is NOT failing.** Live crop tiles run 59.0 against the tape's 56.7 -- we
hold *more* standing crop than he does, every mid-season day. The route reaches the tiles. This is
also the sharpest contrast with the previous block-agent attempt, which fell to 22 live crop tiles
against 49; that failure mode is absent here.

**Candidate 1, the numbers, is not wrong -- it is absent by design.** The middle carries no count at
all; the row asks for a board and the pins decide. So there is no wrong number to fix. What the
measurement shows is that letting our router's own budget set the count produces 41% more planting
than his budget does, which is the same finding from the other side: our tour has slack his does
not, and it spends that slack on planting that does not pay.

## Q3: where it parts from the tape, and why d0-d12 does NOT match

> "i assume it matches d0-d12 with no problem?"

It does not, and the cause is not the executor. **The tape's own row is the row we play on 4 of the
13 strict days: d0, d1, d2 and d4.**

     day    phase       ours       tape    same?    modal%  his rank
       0  library 6e0fb73c37 6e0fb73c37      YES    100.0%      1/1
       1  library 84887b7a00 84887b7a00      YES    100.0%      1/1
       2  library e6f615cc57 e6f615cc57      YES    100.0%      1/1
       3  library 46f3a41758 a0336663a6       no     65.4%      2/4
       4  library 041b44e9e9 041b44e9e9      YES     98.7%      1/3
       5  library c386ca78ce 8fe983b533       no     61.8%      3/4
       6  library cb224b8d8e 681dd5ffbc       no     46.1%      4/9
       7  library 40a1f5fb16 52155583b6       no     24.6%      7/21
       8  library 5e7bab06da 3f018e4c67       no     22.8%      7/31
       9  library eb637c4a6c efe5849804       no     22.8%      5/25
      10  library c5101dd239 bcb6786cd3       no     20.2%      9/28
      11  library 6dda962dd3 5d021a1761       no     16.7%      7/44
      12  library a1e69070ec 25c506bbb3       no     20.2%      9/42
      13  library a11ed857c5 be3aa26d74       no     20.2%     33/35
      28  library 65a36c0579 66cc6fe41a       no     36.8%      2/7
      29  library ed25cef10b ed25cef10b      YES    100.0%      1/1

`his rank` is where this season's row sits in that day's frequency order. On d11 his plan is the 7th
most common of 44. **Game 92498144 is not the modal season from d3 on**, so a divergence on the grid
after d2 cannot be read as an execution defect -- we are playing a different plan on purpose.

This is the confound that has to be stated before any d0-d12 grid is used as a target: the grid
compares a modal-row agent against one specific season, and it cannot separate "our executor failed"
from "this season is not the one we chose to play".

The cost of that choice, measured: at **d13**, before the greedy middle starts, the library agent is
already **$4,644 behind** the shipped agent ($13,546 against $18,190). It finishes **$6,548** behind
($140,057 against $146,605). So roughly **71% of the whole gap is the opening**, and only 29% accrues
across the fourteen greedy days.

## Q4: win or loss. LOSS.

Library agent against the shipped greedy planner (`schedule_agent` on `kagg/plan.py`), seed 11,
weeds 0.0, both seatings:

    seating         library       greedy   result
    seat 0            68445       109270   LOSS
    seat 1            68445       109270   LOSS
    W/D/L  0/0/2

**The two seatings are not independent.** The raw finals mirror exactly -- `final[0]=68445,
final[1]=109270` becomes `final[0]=109270, final[1]=68445` -- so the seat swap really happened and
the result is genuinely seat-invariant to the dollar. Treat this as n=1, not n=2. One seed, one
opponent: this is a direction, not a rate.

## The row library has a defect, and it is not cosmetic

`places` in `data/target_rows_kawa_norm.json` is **mostly not animals**:

    STRAWBERRY 2794   WOOL 2218   COW 1936   MELON 1653   SHEEP 1496
    FERTILIZER 1204   MILK 1039

The reference's `PLACE` branch puts an animal on a matching empty structure and otherwise falls back
to dropping the named item into the shed. Kawashigi uses the second form constantly, and
`scripts/extract_target_rows.py` appends `u[1]` verbatim, so the two ops are recorded as one field.
`schedule_agent._outstanding_places` reads every entry as `R.ANIMALS[a]["first_yield_day"]`, so one
product in that list kills the day on its first turn -- `KeyError: 'FERTILIZER'` at
`schedule_agent.py:3862`, which is how it was found, on d1.

`kawa_rows.only_animals_get_placed` filters it. It also changes the label: dropping the shed-drop
cadence took d13 from 58 distinct rows to 35. **`scripts/extract_target_rows.py` should be fixed at
source**, and every distinct-row count in `docs/kawashigi_algorithm_2026-08-21.md` is inflated by it.
Not done here -- that file is Alex's uncommitted work.

## The label: sells and buys are execution after the land buy

Modal share of the day, under three labels:

    day    all ten keys    minus sells    minus sells and buys
    d22            1%             1%                      2%
    d27            1%             1%                      1%
    d28            1%            13%                     27%
    d29            1%            98%                     98%

d29 is the whole case: **224 of 228 seasons play the same closing day**, and hashing the sell quota
reported 212 distinct plans for it. `SELLS_ARE_EXECUTION_FROM_DAY = 13`, which is Alex's own recorded
position at the foot of `scripts/executor_label.py`. The row still carries its orders and the
executor still plays them; only the *choice* of row is made blind to them.

It does not rescue the middle -- d22-d27 stay at 1-2% under every label.

## Modal coverage, which is the case for a selector

Share of the day's 228 seasons that the chosen row speaks for, after the `places` fix:

    d0  100.0%   d5  61.8%   d10 20.2%   d15 14.5%   d20  7.9%   d25 1.8%
    d1  100.0%   d6  46.1%   d11 16.7%   d16 10.5%   d21  3.9%   d26 2.6%
    d2  100.0%   d7  24.6%   d12 20.2%   d17 12.3%   d22  3.1%   d27 4.8%
    d3   65.4%   d8  22.8%   d13 20.2%   d18 11.8%   d23  3.9%   d28 36.8%
    d4   98.7%   d9  22.8%   d14 21.5%   d19 11.4%   d24  3.1%   d29 100.0%

The instruction was to measure the constant before building a selector. It is measured. **d0-d2 and
d29 are constants and need nothing. d3-d6 are 46-99% and a modal row is defensible. d7-d13 are
17-25%, so the modal row is wrong four times in five, and that is exactly the window that costs
$4,644 by d13.** A selector for d7-d13 is the next thing worth building, and it is now justified by a
number rather than by the shape of a distribution.

## Unverified

- One seed, one opponent, one tape. The head-to-head is n=1 in effect.
- Whether a d7-d13 selector recovers the $4,644. Not measured -- it is the proposal, not a result.
- Whether trimming the middle's planting toward his 112 recovers the remaining ~$1,900. The
  measurement says 49 plantings bought no harvest; it does not say what they cost, because the
  turns they consumed might have had nothing better to do.
- Every number is at `weedSpawnChance = 0.0`. The ladder runs 0.005.
- `SHOP_ADAPT_CROPS = False` was confirmed, so nothing re-aims the crop on the strict days. If it is
  ever switched on, d6-d12 stops being strict row matching, because `CROP_ADAPT_FROM_DAY = 6` and
  `CROP_SWAP_PAIRS` contains `("WHEAT", "CARROT")`.
