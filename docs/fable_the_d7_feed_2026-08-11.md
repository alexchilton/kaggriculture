# The d7 tenth feed: the dawn wheat block is dropped for a full order queue

Fable, 2026-08-11.
Worktree `agent-a3a2da1c905101655`, branch reset to `9bc5a6d` ("Do not queue the day's ration behind the parcel"), plus the one uncommitted fix described below in `kagg/search/schedule_agent_1455mh.py`.
Everything measured on seed 11, Victor tape, via `python -u scripts/breakdown.py --module schedule_agent_1455mh --tape victor --days 12`.

## Verdict in one paragraph

Alex's hypothesis was right: the answer is the market cadence, not a wait at the depot.
The dawn plan sizes the h00 wheat order at the whole 14-unit row (`BUY_THE_ROW_AT_DAWN`), the bank covers it ($2,512 with the same turn's wool pending), and the order is then **dropped on the floor** because d7's h00 queue already holds ten orders — `SELL WOOL`, `SELL FERTILIZER`, seven `HIRE`s and the `BUY_ANIMAL COW 2` — and the append is gated on `len(orders) < 9`.
`state["ordered"]` is honest here (nothing was credited), but from h01 the boost is gone (`hour == 0`), so the row falls back to `BUY_DRIP = 1` per turn and fourteen wheat arrive one an hour through h15.
The crew's depot draws at h02-h05 outpace that drip, u4's want is deleted against a momentarily empty shed, and the day closes `feed 9/10`, `care 9/10`, `collect_fert 6/7`.
The fix keeps the dawn boost live until the block is actually queued; it goes out whole at h01 — which is byte-for-byte the tape's own cadence, since Victor's h01 queue is also exactly ten and he ships `BUY_PRODUCT WHEAT 6` as a block at h02, his first turn with a free slot.
d7 now matches on every op row this investigation owns; d0-d6 are **byte-identical** to baseline.

## 1. The traced mechanism

Instrumented buy block, d7 hour by hour (`data/logs/fable_d7_buytrace.log`):

    FABLEBUY d7 h00 money=2512.0 quote=33 owed=14 herd=-12 short=14 shedW=2 ordered_buys=0 norders=10   <- refused: no slot
    FABLEBUY d7 h01 money=2207.0 quote=34 owed=14 herd=-12 short=1  shedW=2 ordered_buys=0 norders=2
    FABLEBUY d7 h02 money=1343.0 quote=34 owed=13 herd=-14 short=1  shedW=0 ordered_buys=1
    ... one wheat per hour ...
    FABLEBUY d7 h15 money=892.0  quote=35 owed=0  short=0  shedW=10 ordered_buys=14

`short=14` at h00 says the sizing and the funding were both correct; `norders=10` says the append gate `len(orders) < 9` refused it.
Note `money=2512` at h00 — `SELLS_FUND_THE_TURN` had already credited the wool, so "the bank was thin" is NOT the story; the queue was full.

The crew side (`data/logs/fable_d7_deltrace.log`, `fable_d7_day_ops.log`):

    h00  u0 draws WHEAT 3 (dawn shed 5 -> 2)
    h01  buy drip 1 fills end of turn -> shed 3 at h02
    h02  u1 (earlier in unit order) takes 3 of its 4 -> shed 0
    h02  FABLEDEL u4 item=WHEAT want=3 shed=0 critical=False        <- the whole want, deleted
    h02-h04  u4 walks its tour wheatless; its first pen still offers COLLECT_FERTILIZER,
             so `_live_ops` is non-empty and `FETCH_THE_FEED_AND_RETURN` (which fires only on
             an EMPTY ops list) never triggers there -- that pen's FEED is dropped silently
    h05  at the next pen the fetch DOES fire, sizes its draw off FEEDs still in the route
         (1 underfoot + 1 ahead = 2, not 3), takes 2, feeds two pens
    net  feed 9/10; care 9/10 because `router.animal_ops` offers CARE only on a pen it feeds;
         collect_fert 6/7 because the unplanned round trip eats the tour's tail

Two corrections to the working framing in the task brief, both from the trace:

- The deletion is at **h02, and it is the whole want (3), not a post-draw remainder of 1**.
  u4's h05 `PICKUP WHEAT 2` is not the planned depot stop short-changed; it is
  `FETCH_THE_FEED_AND_RETURN` inserting a new stop, correctly sized for the two FEEDs still
  visible in the route. The third FEED was already lost at h02-h04, before the fetch could see it.
- The reverted attempts extending `WAIT_FOR_THE_MORNING_DELIVERY` never touched `feed 9/10`
  because waiting at the depot only helps if the wheat comes; at 1/turn against three drawing
  units it does not come in time whatever the hand does. The defect is upstream of the depot.

## 2. Where else the same drop fires (`data/logs/fable_allday_h00_trace.log`)

    d0  h00 norders=8   sent (11 wheat, one block)      d7  h00 norders=10  DROPPED
    d1  h00 owed=0      nothing to send                 d8  h00 norders=9   DROPPED (gate is < 9)
    d2  h00 norders=3   sent                            d9  h00 norders=10  DROPPED
    d3  h00 norders=5   sent (money-shrunk to 3)        d10 h00 norders=15  short=0 (land-turn skip)
    d4  h00 norders=4   sent                            d11 h00 norders=10  DROPPED
    d5  h00 norders=8   sent                            d12 h00 norders=10  DROPPED
    d6  h00 norders=6   sent (money-shrunk to 3)

Every day from d7 with a big hire row drops its dawn block, and d8/d9's `feed 11/12`,
`care 11/12` carry the same signature.
A second `FABLEDEL` fires on d10 (u12, want 1).
Those days are beyond this investigation's frontier and were not chased; the fix reaches them
by construction, and the measured d8-d11 movement is toward the tape (below).

## 3. The fix

`kagg/search/schedule_agent_1455mh.py`, two lines of logic plus the daily reset:

- The `BUY_THE_ROW_AT_DAWN` boost condition `hour == 0` becomes
  `not state.get("dawn_row_sent", False)` — the boost stays live until the block is queued.
- `state["dawn_row_sent"] = True` is set at the append — even for a partial send shrunk by the
  money guard (today's thin-bank behaviour, unchanged), never by the slot gate refusing it.
- `dawn_row_sent=False` joins the daily `state.update(...)` reset.

Deliberately narrow: a day whose h00 block goes out (all of d0-d6) is bit-identical, because the
h00 append sets the flag exactly where `hour == 0` used to expire.
Only a day refused for a full queue changes, and it changes into the tape's own shape: the block
goes out whole on the first turn with a free slot.
On d10 the land-turn skip zeroes `short` before the append, so the flag stays unset and the row
now goes out as a block once the parcel's turn is over — previously it dripped; this is the one
behavioural change beyond the refused-queue days, and it moved d10 toward the tape
(`harvest 5/6 -> 6/6`, `money 3719 -> 5230` against 5630).

Test: `tests/test_the_dawn_row_survives_a_full_queue.py` — asserts the d7 row is fully queued by
the end of h01.
Red at baseline (`queued only 1 of the 14-wheat row ... per hour {h1..h14: 1 each}`), green with
the fix, and red again with the fix reverted to `hour == 0` (checked both directions).
The assertion is on the ORDERS deliberately: the defect is on the offer side, one line before any
fill exists, and the fill follows from a $2,207 bank against a ~$480 order.

## 4. The grid, before and after

Baseline (`data/logs/fable_d7_baseline_grid.log`):

                           d0           d1           d2           d3           d4           d5           d6           d7           d8           d9          d10          d11
    money               15/15        14/14      188/182      203/196      560/554      529/528        57/28      892/766       224/97    4139/1980    3719/5630    5933/6856
    tiles               25/25        25/25        25/25        25/25        25/25        25/25        50/50        50/50        50/50        50/50        75/75        75/75
    pens                  5/5          5/5          5/5          5/5          5/5          6/6          8/8        10/10        12/12        12/12        12/12        12/12
    weeds                 0/0          0/0          0/0          0/0          0/0          0/0          0/0          0/0          0/0          1/0          2/0          2/0
    wheat                 5/5          5/5          5/5          6/6          6/6          7/7          7/7        10/10        15/13        13/13        12/13        13/13
    strawb                0/0          0/0          0/0          3/3          3/3          7/7          8/8        18/18        18/20        19/20        30/31        32/36
    melon                 5/5          5/5          5/5          5/5          5/5          5/5          5/5          5/5          5/5          5/5         4/12        12/14
    cow                   1/1          1/1          1/1          1/1          1/1          2/2          3/3          6/6          7/8          7/8          8/8          8/8
    sheep                 4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4

    plant               10/10          0/0          0/0          4/4          5/5          5/5          1/1        14/14         8/10          3/1        14/23        14/11
    water               10/10          0/0        10/10          9/9        15/15          9/9        12/12        33/33        16/22        29/28        31/43        43/41
    harvest               0/0          0/0          0/0          0/0          5/5          0/0          4/4          1/1          4/6          5/5          5/6          3/4
    feed                  5/5          0/0          5/5          5/5          5/5          6/6          7/7         9/10        11/12        11/12        11/12        12/12
    care                  5/5          0/5          5/5          5/5          5/5          6/6          7/7         9/10        11/12        11/12        11/12        12/12
    collect_fert          0/0          5/5          5/5          5/5          5/5          5/5          6/6          6/7        10/10        11/12        11/12        12/12
    dig                   0/0          0/0          0/0          0/0          0/0          0/1          0/0          0/1          0/0          2/0          0/0          0/1
    build_pastur          5/5          0/0          0/0          0/0          0/0          1/1          2/2          2/2          2/2          0/0          0/0          0/0
    place                 5/5          0/0          0/0          0/0          0/0          1/1          1/1          3/3          1/2          0/0          1/0          0/0
    pickup                5/4          0/0          2/2          2/2          2/2          3/3          8/4          6/5          7/5          6/4          6/4          6/4
    drop                  0/0          3/0          2/0          2/0          1/0          2/0          4/1          2/0          4/0          5/0          6/5          4/0
    pass                44/48        31/28        12/21        31/27         2/18        12/27         12/5        23/22         8/23        17/44        84/78        16/57
    sell                  6/6          0/0          5/5          5/5          5/5        22/22        13/13        18/18          9/9        42/29        30/55        21/18
    buy_seed            10/10          0/0          0/0          4/4          5/5          5/5          4/4        11/12        10/10          1/1        31/31          3/4
    buy_product         11/11          0/0        11/11          5/5          2/2          7/7          5/5        14/14          7/7        10/10        12/12          6/6
    buy_animal            5/5          0/0          0/0          0/0          0/0          1/1          2/2          2/2          2/2          0/0          0/0          0/0
    buy_land              0/0          0/0          0/0          0/0          0/0          0/0          1/1          0/0          0/0          0/0          1/1          0/0
    hire                  4/4          1/1          2/2          3/3          3/3          3/3          4/4          7/7          6/6          7/7        14/14        10/10

With the fix (`data/logs/fable_d7_fixed_grid.log`, reproduced byte-identically by the cleaned
tree in `fable_d7_final_grid.log`):

                           d0           d1           d2           d3           d4           d5           d6           d7           d8           d9          d10          d11
    money               15/15        14/14      188/182      203/196      560/554      529/528        57/28      896/766       229/97    4155/1980    5230/5630    7497/6856
    tiles               25/25        25/25        25/25        25/25        25/25        25/25        50/50        50/50        50/50        50/50        75/75        75/75
    pens                  5/5          5/5          5/5          5/5          5/5          6/6          8/8        10/10        12/12        12/12        12/12        12/12
    weeds                 0/0          0/0          0/0          0/0          0/0          0/0          0/0          0/0          0/0          1/0          2/0          2/0
    wheat                 5/5          5/5          5/5          6/6          6/6          7/7          7/7        10/10        15/13        13/13        12/13        12/13
    strawb                0/0          0/0          0/0          3/3          3/3          7/7          8/8        18/18        18/20        19/20        30/31        33/36
    melon                 5/5          5/5          5/5          5/5          5/5          5/5          5/5          5/5          5/5          5/5         4/12        11/14
    cow                   1/1          1/1          1/1          1/1          1/1          2/2          3/3          6/6          7/8          7/8          8/8          8/8
    sheep                 4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4

    plant               10/10          0/0          0/0          4/4          5/5          5/5          1/1        14/14         8/10          3/1        15/23        13/11
    water               10/10          0/0        10/10          9/9        15/15          9/9        12/12        33/33        18/22        29/28        32/43        42/41
    harvest               0/0          0/0          0/0          0/0          5/5          0/0          4/4          1/1          4/6          5/5          6/6          3/4
    feed                  5/5          0/0          5/5          5/5          5/5          6/6          7/7        10/10        11/12        11/12        11/12        12/12
    care                  5/5          0/5          5/5          5/5          5/5          6/6          7/7        10/10        11/12        11/12        11/12        12/12
    collect_fert          0/0          5/5          5/5          5/5          5/5          5/5          6/6          7/7        10/10        11/12        11/12        12/12
    dig                   0/0          0/0          0/0          0/0          0/0          0/1          0/0          0/1          0/0          2/0          0/0          0/1
    build_pastur          5/5          0/0          0/0          0/0          0/0          1/1          2/2          2/2          2/2          0/0          0/0          0/0
    place                 5/5          0/0          0/0          0/0          0/0          1/1          1/1          3/3          1/2          0/0          1/0          0/0
    pickup                5/4          0/0          2/2          2/2          2/2          3/3          8/4          5/5          5/5          4/4          6/4          6/4
    drop                  0/0          3/0          2/0          2/0          1/0          2/0          4/1          2/0          2/0          4/0          7/5          4/0
    pass                44/48        31/28        12/21        31/27         2/18        12/27         12/5        21/22         6/23        20/44        79/78        19/57
    sell                  6/6          0/0          5/5          5/5          5/5        22/22        13/13        18/18          9/9        42/29        37/55        22/18
    buy_seed            10/10          0/0          0/0          4/4          5/5          5/5          4/4        11/12        10/10          1/1        31/31          3/4
    buy_product         11/11          0/0        11/11          5/5          2/2          7/7          5/5        14/14          7/7        10/10        12/12          6/6
    buy_animal            5/5          0/0          0/0          0/0          0/0          1/1          2/2          2/2          2/2          0/0          0/0          0/0
    buy_land              0/0          0/0          0/0          0/0          0/0          0/0          1/1          0/0          0/0          0/0          1/1          0/0
    hire                  4/4          1/1          2/2          3/3          3/3          3/3          4/4          7/7          6/6          7/7        14/14        10/10

Reading the diff (`diff fable_d7_baseline_grid.log fable_d7_fixed_grid.log`):

- **d0-d6: byte-identical**, every row, both tables.
- **d7: feed 9/10 -> 10/10, care 9/10 -> 10/10, collect_fert 6/7 -> 7/7.**
  `pickup 6/5 -> 5/5` and `pass 23 -> 21/22` come along (both exempt rows); money 892 -> 896/766.
- d8-d10 move toward the tape everywhere they move: d8 `water 16 -> 18/22`, d10
  `harvest 5/6 -> 6/6`, `money 3719 -> 5230` against 5630, d11 `plant 14 -> 13/11`,
  `water 43 -> 42/41`, `strawb 32 -> 33/36`.
- Three cells past the frontier move away by one: d11 `sell 21 -> 22/18`, d11 board
  `wheat 13/13 -> 12/13`, `melon 12 -> 11/14`. d11 sits behind d8's `feed 11/12` and d10's
  `plant 15/23`, so by the days-in-order rule these are inherited noise on a diverged board,
  not regressions of matched ground.

## 5. The new frontier

In order: d1 `care 0/5` (we are right — the reference banks the care bonus only on a fed animal,
`kaggriculture.py:816`), the no-op digs (d5/d7/d11, tape digs an empty tile), then
**d7 `buy_seed 11/12`** — present at baseline, untouched here, and now the first live op
divergence — then d8 (`plant 8/10`, `water 18/22`, `harvest 4/6`, `feed 11/12`, `care 11/12`,
`place 1/2`).
d8/d9 still drop their dawn blocks' SIBLING signature (`feed 11/12`) for what the h00 trace says
is at least partly the same class — d8's h00 queue holds 9 — but their remaining gap survives
this fix, so something else is also owed there.

## 6. What was NOT the answer, for the register

- **A wait at the depot** (the two reverted `WAIT_FOR_THE_MORNING_DELIVERY` extensions): the
  wheat does not arrive inside the window a waiting hand has, because the drip is 1/turn against
  three drawing units. Upstream cadence, not downstream patience.
- **Marking the FEED draw critical**: would have stood u4 at the shed from h02 collecting the
  drip one unit at a time, deforming the tour the same way the measured d4/d5 regressions did.
  Not attempted once the h00 trace showed the block was affordable and refused.
- **Re-slotting the queue** (wheat ahead of the cow or a hire): the tape itself does not do
  this — Victor's h01 queue is the same ten orders ours is, and his wheat waits for h02.

## Artifacts

- Fix: `kagg/search/schedule_agent_1455mh.py` (uncommitted; the `dawn_row_sent` flag, three
  edit sites, comment block at the boost).
- Test: `tests/test_the_dawn_row_survives_a_full_queue.py` (red at `9bc5a6d`, green with the
  fix, red again on revert — verified in both directions).
- Guards run: `test_the_dusk_topup_stays_inside_the_days_row.py`,
  `test_a_hire_waits_for_the_ground_that_frees_it.py`,
  `test_the_dawn_plan_owns_the_land_it_buys_today.py` — 31 passed, 34 skipped, 0 failed
  (`data/logs/fable_d7_guard_tests.log`).
- Logs: `data/logs/fable_d7_baseline_grid.log`, `fable_d7_fixed_grid.log`,
  `fable_d7_final_grid.log` (byte-identical to the previous — the cleaned tree reproduces its
  own measurement), `fable_d7_buytrace.log`, `fable_d7_deltrace.log`,
  `fable_allday_h00_trace.log`, `fable_d7_day_ops.log`, `fable_d7_sell_day.log`.
- Worktree housekeeping: this worktree was created at a stale 2026-08-03 commit and was reset
  to the task's stated `9bc5a6d`; `data/seed_scripts` is a symlink to the main repo's copy, and
  `scripts/day_ops.py` (untracked in the main repo) was copied in for the hour-by-hour trace.
