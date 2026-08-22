# Closing the season: no upkeep on d29, and a delivery that is planned

Fable, 2026-08-15, on the brief `docs/fable_brief_sell_the_close_2026-08-15.md`.
Baseline HEAD `eb8845e`, worktree branch `worktree-agent-a3a4f984a2182e056`.
All numbers seed 11, kawashigi tape, `ours/tape` unless said otherwise.

## Two instruments, and which world each number lives in

The brief's numbers (harvest 396, sell 1489, 58 stranded) come from TWO different runs and that
matters for reading everything below.

- **Grid world**: `scripts/breakdown.py --days 30` — recorded economy, recorded shop draw,
  `make_agent(thin, 0, router=True)`. This is where harvest 396 / sell 1489 / $150,728 live.
- **Test world**: the fixture of `tests/test_the_last_day_puts_its_load_in_the_shed.py` — plain
  `make("kaggriculture", seed 11, weeds 0)`, no recorded shops, `make_agent(sched, me=0)`.
  This is where the stranded count lives, and it is the world the xfail target is judged in.
  My instrument is `close_report.py` (scratchpad), which mirrors that fixture exactly and adds
  per-day op counts and sell fills via `kagg.analysis.fills`.

The same HEAD measures 62 stranded in the test world against the docstring's 58 — the doc numbers
were taken on an earlier HEAD. Every comparison below is same-instrument, same-HEAD.

## The mechanism chain, as measured

1. `_end_of_day` banks a carried load free at every rollover — except after d29's last turn,
   when the market is gone. `_commit_unit` refuses a SELL from a hand. So d29 upkeep buys nothing
   and d29 harvest that is not walked in is worth exactly zero.
2. The recorded landmine: `cover._apply_precomputed` keyed a stop on the exact `(tile, ops)`
   tuple, so stripping FEED/CARE from a pen's job threw the stop out of the solved route
   (harvest 396 -> 389 in the parked attempt).
3. The unrecorded landmine, found this session: **the executor re-adds the upkeep the planner
   drops.** The route is a visit order; `underfoot()` (`schedule_agent:2458`) feeds any pen
   `will_be_fed` says yes to and cares with no day gate at all. With only `animal_ops` gated,
   d29 measured `feed 14, care 13` — the flag looked on and was doing nothing.

## Delta 1 — `cover.MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE` (commit 798d459)

On the last day only, a stop whose exact key misses is still seated on the unit the solve chose,
provided the job at that tile has ops a SUBSET of the solved stop's. Earlier days keep the exact
key (pinned by `tests/test_a_last_day_stop_survives_losing_its_upkeep.py`, red/green/red cycle).

Measured alone: byte-identical in both worlds; d29 exact-key misses fall 14 -> 9.
The five reduced pen stops seat where the solve put them. Null on its own, by construction.

## Delta 2 — `NO_UPKEEP_ON_THE_LAST_DAY = True`, gated once for every path (commit c1c49f7)

`router.upkeep_buys_nothing(day)` is the one gate: `animal_ops` (the plan), `will_be_fed`
(the executor's underfoot FEED and the wheat-purchase sizing), and `underfoot()`'s CARE branch.

Grid world, d0-d28 byte-identical, every change a d29 cell:

    row            baseline     delta 2
    d29 feed          14/0        0/0
    d29 care          14/0        0/0
    d29 harvest      27/19       26/19
    d29 sell        93/148     120/148
    d29 sold        $7,474      $9,547
    season close  $150,728    $152,801     (tape $150,076 — we now out-bank the tape)

Season harvest 396 -> 395, sell 1489 -> 1516.
Test world: stranded 62 -> 51, money $82,305 -> $83,826, d29 sell fills 96 -> 123.
d29 pass rose 30 -> 41 in the grid world: the freed turns were not yet spent.

The half-step in between is worth keeping: with ONLY `animal_ops` gated (the parked attempt's
shape, now with delta 1 in place), the season measured WORSE than baseline in the test world —
harvest 384 -> 377, money -$157 — because the planner planned small stops and the executor spent
the turns anyway. `data/logs/fable_d2_noupkeep_stranded.log` records it.

## Delta 3 — `WALK_THE_LOAD_HOME_DAYS = (10, 29)` (commit 30ad651)

The endorsed shape: `deliver=True` on d29, so `plan()` materialises each tour's closing walk and
takes it when it fits the budget the upkeep just freed. The first recorded attempt recovered 7 of
58 precisely because that slack did not exist yet.

Test world: stranded 51 -> 28 (~$672), d29 sell fills 123 -> 148 — the tape's own d29 number —
money $83,826 -> $84,560.
Grid world: op rows byte-identical, sold $9,547 -> $9,543 (a -$4 fill-price slide). On that board
d29 harvests 26 and the tours are full, so the appended walk fits nowhere. Not a regression;
kept for the test-world gain.

## Delta 4 — survival waters, rotation waters and weed digs (commit efd3dfa)

The d29 trace (`data/logs/fable_d29_trace.log`) showed u4 DIGging weeds at (1,0) and (3,0) at
h17/h20 and ending the season at (3,1) holding 3 units. Three more "buys only a tomorrow" ops,
gated on the same master switch: the survival WATER (saves a tile from tonight's rollover), the
rotation WATER (the same purchase spread over two days), and the WEED DIG that `_live_ops`
re-derives at any visited tile whatever the plan priced. The in-window water is deliberately
KEPT — it adds a yield unit the same day, and the tape emits 11 of them on its own d29.

Grid world: d29 dig 5/0 -> 0/0, sell 120 -> 123, close $152,848; weeds at close 1 -> 6, which is
free (the tape closes at 14). Test world: stranded 28 -> 26, d29 sell 148 -> 153, money $84,699.

## Delta 5 — trim the tail that cannot come home, d29 only (commit 407d08d)

`TRIM_A_TAIL_THAT_CANNOT_COME_HOME = True` behind a new `TRIM_HOME_DAYS = {29}`. On every other
day the sweep banks a kept job's load free, so trimming is a pure loss (why it shipped False for
d4); on d29 the kept job's produce is discarded, so the walk beats the job by construction. The
reserve pricing cannot reach a precomputed day — this trim in `plan()` is the one place a solved
d29 tour sheds work for its delivery.

The two delivery fixes cover each other's world, and the split is the measurement:

    world                     delta 3 (planned walk)    delta 5 (trim)
    test  (walk fits)         stranded 51 -> 28         byte-identical
    grid  (tours fuller)      -$4, op rows identical    sell 123 -> 129, close $152,974

Grid world delta 5: d29 water 18/11 -> 16/11, harvest 26/19 -> 25/19, drop 5 -> 6,
sold $9,594 -> $9,720. d0-d28 byte-identical throughout.

## Delta 6 — the last-day deadline walk (executor, commit d0a21f1)

After deltas 1-5 the re-trace (`data/logs/fable_d29_trace_after.log`) leaves exactly two hands:
u8 harvests to h19, walks, and ends at (4,3) — ONE tile short — holding 11; u7 works to h22
three tiles out and strands 12. Executor-vs-plan drift: `_live_ops` re-derives work at stops, a
tour runs a turn or two past its costing, and the planned walk starts too late.

`must_walk_home_now(day, hour, pos, held, depots)`: on the last day a loaded hand with
`24 - hour <= dist + 1` turns left (the +1 is the DROP) abandons its remaining stops and walks.
The runtime mirror of the trim. `LAST_DAY_DEADLINE_WALK`, following the same master switch.

Test world: stranded 26 -> 16, d29 harvest 22 -> 19 (all three forgone would have stranded).
Grid world: harvest 25 -> 23, water 16 -> 14, closing shed wheat 2 -> 4. **Money unchanged in
both worlds** — the recovered wheat reaches the shed and does not sell, which exposed the
quota finding below. The post-fix trace (`data/logs/fable_d29_trace_d6.log`) shows the bound is
exact: u7 and u8 both fire at h19 and arrive for an h23 DROP, the last turn whose market phase
could still sell them.

## Null, reverted: `feed_days(29) = 0`

After delta 6 the recovered wheat sat in the d29 shed unsold (money moved $0 in both worlds), and
the feed reserve — `feed_days(day) * herd` wheat held back from sale — was the suspect. Measured
**byte-identical in both worlds** and reverted the same hour. The binding constraint on d29 wheat
sales is the SCHEDULE's sell row: the agent offers what the row still owes
(`CUMULATIVE_SELLS`/`SELL_CARRY_DAYS`), the d29 wheat quota was already filled, and wheat beyond
the row is never offered whatever the reserve says. Logs: `fable_d7_sellguard_*.log`.
A "flush the whole shed at the close" sell rule is the open follow-up if that money is wanted;
it is a market-block change, not a routing one.

## Null, reverted: the yield gate (`yield_is_deliverable`)

"On the last day do not pick what cannot be carried home" — a filter at the `_live_ops` site and
the underfoot HARVEST, `24 - h >= dist + 2`. **Byte-identical in both worlds and reverted.**
The mechanism: it was designed against the PRE-delta-6 trace (u7's h20 harvest six tiles out).
With the deadline walk live, a hand is either loaded — and the deadline clears its route before
any undeliverable stop is reached — or empty, and no empty hand in either world reaches a
yielding stop past the bound. The gate guarded a path the deadline had already closed. Designed
off a stale trace: re-trace after every behavior change before building on one.
Logs: `fable_d8_yieldgate_*.log`.

## The quota finding

The d29 schedule row asks for exactly 148 units (`{WHEAT 92, WOOL 8, FERT 9, STRAW 6, MILK 27,
CARROT 6}` — the tape's own close) and we fill 153-154 with the cumulative carry. From there the
market block offers nothing more whatever sits in the shed: the deadline walk's recovered wheat,
and the feed-reserve null above, are both bounded by the ROW, not by the shed or the reserve.
Selling past the plan's row at the close is the open money question — a market-block change,
out of scope here.

## Secondary target — d28 pen HARVEST priced CRITICAL (commit 5dbff17)

`BANK_THE_FIELD_ON_THE_LAST_FREE_DROP_DAY = True` makes all 7 of
`tests/test_the_second_to_last_day_banks_the_field.py` pass. The recorded null re-confirmed:
grid world byte-identical (d28's solved route already seats everything with slack). Kept ON for
the pricing the test pins, and because the test-fixture world shows what it buys when a d28
does differ: d28 water 35 -> 37, one drop moves d28 -> d29, money $84,699 -> $84,945 (+$246).

## Where it stands

    seed 11, kawashigi                     baseline eb8845e     final 5dbff17
    GRID world (recorded economy+shops)
      season close (ours/tape)          $150,728/$150,076    $152,974/$150,076
      season harvest / sell                    396 / 1489           392 / 1525
      d29 feed,care,dig                          14,14,5                 0,0,0
      d29 sell (ours/tape)                        93/148               129/148
    TEST world (the xfail fixture)
      stranded at its snapshot            58-62u ~$2,414          16u ~$324
      season money (ours/tape)          $82,305/$66,919      $84,945/$66,801

**The strict xfail stays.** `TOLERATED_UNITS = 12` against our 16 at the fixture's measure.
Two caveats on that 16, measured off `fable_d29_trace_d6.log`: the fixture plays
`range(719)` — it never plays the game's final turn and snapshots hands BEFORE the h22 step —
while u4 drops at h22, and u7/u8 arrive for h23 drops that a real 720-turn game executes. By
that instrument the tape itself "strands" 7. And the marginal units are quota-bound (above), so
the h22/h23 arrivals cost ~$0 either way. I chose not to widen the deadline bound to satisfy an
instrument cutoff the real game does not have; if the 12 is to be met by the letter, the honest
route is fixing the fixture to play all 720 turns and measure the terminal sweep, which changes
the tape's own number too — Alex's call, not mine.

## Remaining candidates, unexplored

- Mid-tour drops on d29 for shed-adjacent tours (u8 worked the (4,x) column all afternoon one
  tile from the shed, holding milk from mid-day; `DELIVER_MIN` never triggered).
- Gate `THIRSTY_CROP_PULLS_AN_IDLE_HAND` on the last day — its water buys a tile that dies at
  scoring, and delta 4 newly creates dying d29 tiles for it to chase. Unmeasured; possibly null.
- Sell past the row at the close (the quota finding).
- The brief's open question — why the tape harvests 32 on d28 to our 27 with identical
  plantings — is still unexplained; nothing here touched d28 seating.

## Logs

All under `data/logs/`: `fable_close_baseline_{stranded,grid30}.log`,
`fable_d1_keying_*.log`, `fable_d2_noupkeep_*.log` (the half-step),
`fable_d2b_noupkeep_*.log`, `fable_d3_deliver_*.log`, `fable_d4_notomorrow_*.log`,
`fable_d5_trim_*.log`, `fable_d6_deadline_*.log`, `fable_d7_sellguard_*.log` (null),
`fable_d8_yieldgate_*.log` (null), `fable_d9_bankfield_*.log`, and the three traces
`fable_d29_trace.log` (baseline+d3), `fable_d29_trace_after.log` (after d5),
`fable_d29_trace_d6.log` (after d6).
