# After the closing-day release: what shipped, and the three things measured since

Written 2026-08-15, after submission `55530699`.

## What shipped

`55530699`, built from `2a2e291`, merged at `081c24f`.
Eight deltas that stop the season ending with produce in the crew's hands.

    season close vs kawashigi tape   150,728 -> 152,974   (tape 150,076)
    stranded at the close            62 units -> 16       (tape 7)
    d29 feed 14->0  care 14->0  drop 3->7  sell fills 96->154  harvest 22->19

We harvest LESS and bank more, because produce not walked to the shed on d29 is discarded by
`_end_of_day` after the final turn and `_commit_unit` will not sell from a hand.

d0-d27 byte-identical. d28 moves only on the last delta.
Detail and every grid: `fable_close_the_season_2026-08-15.md`. Brief: `fable_brief_sell_the_close_2026-08-15.md`.

Measured on seed 11 and the kawashigi tape only.
No held-out seeds and no arena pool, by explicit decision — the slot was spent to get it on the
board rather than to validate it first.

The previous build, `55527916`, is at **1855.0**.

## 1. The fourth quadrant

Two losses downloaded after the release, neither close:

    93335778   us $89,518  vs Artem Voronov $103,607   -$14,089
    93337672   us $74,289  vs Anhad Mahajan  $77,703    -$3,414

Artem owns FOUR quadrants and 100 tiles to our 75.
Anhad owns three, like us, and that game is inside the close-day margin.

Quadrant unlock turns, from `data/logs/quadrant_timing_leaders.log`:

    player                  games   4q      NE       SW       SE
    alex chilton (archive)     69   66    d4h22    d8h20    d11h1
    カワシギ                    16    4     d6h5    d11h1    d12h1
    Seb (allegedly)            16   16    d4h22    d6h15   d10h14
    Victor @ Tufa Labs          7    0    d6h17    d10h1        -
    Francesco Montone           2    2     d5h0    d8h22   d10h16

Artem's line is `NE d6h5, SW d11h1, SE d12h1` — カワシギ's median to the hour.

Two facts that bound this:

- **We used to buy the fourth in 66 of 69 archived games, and EARLIER than Artem does** (SE d11h1
  against his d12h1, SW d8h20 against his d11h1). We stopped when we rebased onto Victor, who takes
  it in 0 of 7. That was not a decision about land; it arrived with the plan.
- Across all five downloaded losses our unlock turns are byte-identical — NW d0h0, NE d6h10,
  SW d11h1. Our opponents vary (NE d6h5 to d7h2). We do not adapt at all.

So the open question is not "can we afford a fourth" — demonstrably we could, sooner. It is what
the rebase traded that land for, and whether the trade still holds on 1.32.7.
The old timing is pre-rebalance, so its affordability does not carry over unexamined.

## 2. Tomato is conditional, and seed 11 is the wrong board to test it on

Both losses show TOMATO and EGG closing ABOVE base with real town demand and **nobody producing
either**:

                    93335778              93337672
    TOMATO    $74 of $60, drained 179   $165 of $60, drained 358
    EGG       $67 of $50, drained 537    $66 of $50, drained 358
    MILK       $1 of $160  FLOOR          $1 of $160  FLOOR
    STRAWBERRY $5 of $120                $43 of $120

The machinery to act on this already exists and is inert: `WHEAT_TILES_TO_TOMATO = 0`,
`WHEAT_TILES_TO_CARROT = 0`, `LATE_CROP_FROM_DAY = 12`.

Swept on seed 11 against the kawashigi tape (`data/logs/tomato_sweep.log`):

    tomato tiles   our money      tape     closing TOMATO   STRAWBERRY
          0         84,945      66,801          70              12
          4         83,203      69,250          74              12
          8         81,842      68,568          66              14
         12         82,888      69,779          69              12
         16         80,727      69,163          61              16
         24         78,231      69,781          53              20

**Unconditional tomato loses money on this board, monotonically.** The price column says why: TOMATO
never leaves 53-74, so the hinge never fires, and our own production pushes it DOWN.

This is not a verdict on tomato. The 2026-08-15 balance note states the intent directly: these
products become viable in roughly **50% of games for tomato, 26% carrot, 22% eggs** — deliberately
not universally, to create end-game decisions. At zero production seed 11 closes tomato at $70
against base $60, so seed 11 is one of the boards where it does not pay.

The switch is the shop draw's seasonal drain, which varies per game. A constant in the schedule can
only ever be right about half the time. `SHOP_ADAPT_CROPS` is the disabled machinery for exactly
this, and its own docstring says the pairs as written should not be re-enabled — but names the axis
it believes in: wheat against strawberry+melon.

Next step is `scripts/crop_seed_sweep.py`: the knobs crossed with 24 seeds against a field, with each
seed's drain recorded alongside, so the question "is the optimum a constant or a function of the
draw" can be answered rather than assumed.

## 3. The goose kill was 23 hours too early

`REGISTER.md`'s third version caveat already voids every geese/eggs verdict taken before `c99a8a5`
(2026-08-13), when `SELLABLE` finally held all nine products. The dating makes it sharper:

    2026-08-12 06:34   7a88d30   "Delete the geese rather than leave a losing flag in the tree"
    2026-08-13         c99a8a5   CARROT, TOMATO and EGG become sellable at all

The geese were deleted **before** an egg could be sold at any price. That measurement could only
have come out negative.

What it never saw:

    animal   cost  structure  first yield  interval  max_held  product
    GOOSE    $300  COOP       d4           1         4         EGG
    COW      $400  PASTURE    d8           2         6         MILK
    SHEEP    $500  PASTURE    d6           3         6         WOOL

The goose is the cheapest, the earliest and the fastest of the three, and EGG closed above base in
both losses while MILK sat at the floor.

Cautions before this becomes work. Animals in this repo have produced a **wrong negative five
separate times**; the standing lesson is to ask what the code could not express before trusting a
mechanic-level result, which is precisely what happened here. The real cost of an animal is the
daily FEED/CARE action load, not the purchase price. And EGG demand saturates at 358-537 units a
season, so this is a few geese, not a herd.

`plan.py` still carries `GOOSE`, `COOP` and `BUILD_COOP`, so the machinery is present.

## 2026-08-12 — The late season is one defect in two halves, and neither half pays alone

Folded in from docs/the_late_season_is_one_defect_in_two_halves_2026-08-12.md.

Measured, seed 11, tape victor.
**Both halves are currently UNFIXED** — the first was written, measured as a loss on its own, and
reverted.
Do not re-derive either from scratch.

### What the season looks like

State rows match the tape all the way to d24 — same land, same pens, same herd. Then:

    weeds    d24 1/1   d25 6/0   d26 7/0   d27 14/0   d28 17/1
    wheat    d24 43/44           d26 38/54          d28 17/23

Cumulative flow rows, where each stops reconciling:

    fertilize  127/71   +56   breaks at d23   <- the only row where we do MORE
    harvest    322/360  -38   breaks at d25
    plant      182/194  -12   breaks at d26
    water      906/965  -59   breaks at d26

### Half one: a DIG clears ground and nothing plants on it

`DIG` sets the cell to `None` (`kaggriculture.py:477`) exactly as a one-shot HARVEST does
(`:454-455`), and it is how `DIG_A_SPENT_ONGOING_CROP` clears a finished strawberry.
`REPLANT_A_CLEARED_TILE` chains a planting onto the HARVEST case and **not** onto the DIG case, so a
day that demolishes ground plants nothing on it — `_refresh_pins` only sites a PLANT on ground empty
at DAWN, and this ground does not exist until the day makes it.

Seed 11, d26, with d12-d25 solved: the schedule row asks for eleven WHEAT, the pool contains
`HARVEST/DIG x 11`, and PLANT ops offered = **0**. Live on the ladder in episode 92433651 the same
day dug 13 tiles and planted none.

This is the fourth instance of a pattern already fixed three times — `BUILD_THEN_PLACE`,
`PLANT_THEN_WATER`, `REPLANT_A_CLEARED_TILE` — all with the same one-line statement:
**the board the plan reasons about must be the board the day will have.**

**Fixed, measured, REVERTED.** Extending `REPLANT_A_CLEARED_TILE`'s condition to
`any(o == "DIG" ...) or (not ongoing and HARVEST in ops)` passed a four-test unit suite and went red
on revert. On the grid, routes off both sides, control -> fixed:

    money    d24 53031->51523   d26 56453->55259   d28 62743->59845   -$2,898
    weeds    d26  9/0 -> 2/0    d27 13/0 -> 7/0    d28 13/1 -> 7/1
    harvest  d23 23/25->18/25   d27 24/28->21/28
    plant    d26 0/11 -> 0/11   THE TARGET CELL DID NOT MOVE

Fewer weeds, less money, and the day it was written for is untouched — because of half two.

### Half two: `plant_prize` is zero from d26, so nothing is eligible to chain

    plant_prize('WHEAT', 25) = 75.0
    plant_prize('WHEAT', 26) =  0.0

`plant_prize` returns 0 when `days_left < info["max_day"]`, and the docstring is explicit about why:
a one-shot pays only through a HARVEST, and `_one_shot_is_finished` only offers one **once the yield
window has SHUT**. A wheat planted d26 reaches age 4 on d30, past the end, so under our own harvest
rule it can never be collected and is correctly priced at nothing.

**Victor does not play that way.** From his own recorded game (`data/seed_scripts/top2/91854176.json`):

    day  PLANT  HARVEST  WATER  DIG
    d25     12       25     50    1
    d26     11       14     42   10
    d27      0       28     39    0
    d28      0       20     39    6
    d29      0       26     21    0
    final crops: {'WHEAT': 2}

He plants eleven on d26 and harvests **26 on d29**, taking them PARTIALLY at age 2-3, and finishes
with two wheat standing. The env allows it: `HARVEST` takes whatever `yield_units` holds once
`day - planted_day >= first_yield_day` (`:441`), and clears the tile.

Note this is crop-specific and NOT a general "harvest early" rule. Measured on the same tape, every
MELON he harvests is `held 6 / max 6` at age exactly 10 — never partial. The 135 partial harvests in
his season are all WHEAT at age 4, `held 4 / max 6`, which is its last legal day anyway.

### The order to do them in

Half one alone plants tiles we then cannot collect: -$2,898.
Half two alone makes late plantings valuable with nothing clearing ground for them to go on.

So the pair is: teach the harvest rule to take a partial one-shot when the season is about to end,
which makes `plant_prize` non-zero at d26; THEN chain the planting onto the DIG. Measure the pair,
not the halves.

The eight solved routes are keyed to exact job lists, so either change invalidates all of them and
they must be re-solved IN DAY ORDER.

## 2026-08-15 — Brief: copy カワシギ's close. Sell everything on d29, harvest everything on d28.

Folded in from docs/fable_brief_sell_the_close_2026-08-15.md.

Written 2026-08-15 as the handoff to Fable.
Alex's instruction, verbatim:

> we really need to copy kawa to get those items sold.
> no watering no feed and care just get shit sold on d29 and as much as possible on d28

### The loss this fixes, measured on three real ladder replays

| episode | our stranded | their stranded | result |
| --- | --- | --- | --- |
| 93318573 | 81 units ~$3,264 | 4 units ~$19 | lost by $645 |
| 93323101 | 55 units ~$3,526 | 0 units | lost by $3,919 |
| 93286476 | 70 units ~$2,238 | 0 units | lost by $962 |

The stranded value exceeds the losing margin in all three, and our shed is empty at the close.
Two of these three are wins if that produce reaches the shed.

### Why it strands

`_end_of_day` calls `_drop_inventories_to_shed`, so a carried load banks itself free at every
rollover. That is why the tape emits **5 DROPs in a whole season against 389 harvests**.

The pipeline is therefore **one day delayed**: harvest on day N is banked overnight and sold on
day N+1. Day 29 has no N+1. Its automatic drop fires after the final turn, and `_commit_unit`
refuses a SELL unless the goods are already in `private["shed"]`. So a d29 harvest that is not
walked to the shed **is worth exactly zero -- identical to not harvesting it at all.**

That is the key economic fact: turns spent walking home on d29 cost nothing real.
There is no trade-off to balance.

### The closing grid, ours/tape, seed 11, kawashigi tape

    row              d27       d28       d29
    feed           14/14     14/10     14/0
    care           14/12     14/9      14/0
    collect_fert   14/12     14/9      14/0
    harvest        31/35     29/32     26/19
    drop            0/0       2/0       2/9
    sell          ...       103/92    93/148
    pass          ...        48/32    30/56

He does **zero** feed, care and fertilizer collection on d29 against our 42 unit-turns.
He harvests 32 on d28 to our 27, banks it overnight free, and turns d29 into a selling day:
148 units to our 93, with 9 DROPs to our 2.

### Four fixes already tried. All failed. Do not re-try blind.

1. `WALK_THE_LOAD_HOME_DAYS = (10, 29)` -- recovered 7 of 58 units.
   A solved route stores work stops; `materialise` appends the shed trip out of **slack**, and d29
   has none.
2. `NO_UPKEEP_ON_THE_LAST_DAY = True` -- regressed harvest 396 -> 389 and sell 1489 -> 1474.
   `cover._apply_precomputed` matches a stop on `(tile, ops)` ONLY. Removing FEED/CARE changes the
   key, so the stop **leaves the solved route entirely** instead of getting cheaper. This is the
   central landmine.
3. `BANK_THE_FIELD_ON_D28` / `BANK_THE_FIELD_ON_THE_LAST_FREE_DROP_DAY` -- promoting a ripe d28
   tile to CRITICAL was byte-identical three separate ways (prize, at_risk, at_risk + re-solve).
   d28 is already saturated: every job with slack is seated, two hands idle, only 7 ripe units
   left at dusk.
4. `UNSOLVE_DAYS = (29,)` -- +13 sells, +$256, but stranded ROSE 51 -> 78.

Also ruled out: shed overflow (5 units/season), spreading the sale ($64), planting dates
(identical to the tape on d25 9/9, d26 9/9, d27 11/11).

### What is NOT explained

Why he harvests 32 on d28 to our 27 and 19 on d29 to our 27, when our plantings and our ripening
are identical to his. It is neither ranking nor planting date. If Fable finds this, it is the win.

### The fix Alex endorsed

> a delivery that's planned, not appended

`RESERVE_DAYS` already covers d29 and `cover.cost` already knows how to price a tour that ends at
the shed. Two things block it:

- the reserve is gated behind `deliver=True` via `PRICE_THE_TOUR_THE_CALLER_WILL_WALK`
  (`cover.py:1375`), and only d10 sets `deliver` (`schedule_agent.py:869`,
  `DELIVER_CUTOFF_TURNS = 99` against budgets of 23-24);
- d29 is precomputed, so `cover.cost` never runs on it at all.

Suspected third blocker: the reserve branch also requires a non-empty `wanted` row.

### Constraints

- **DO NOT REGRESS d0-d8.** Anything before d23 must stay byte-identical.
- One delta at a time. If two flags are live, measure the 2x2.
- Write the test RED first, then fix, then confirm it goes red on revert.
- Never sum offers. Use `kagg/analysis/fills.py` or shed/money deltas.
- Never call a mismatch "small". Never add a tolerance.
- Do not run the full pytest suite.

## 2026-08-15 — Closing the season: no upkeep on d29, and a delivery that is planned

Folded in from docs/fable_close_the_season_2026-08-15.md.

Fable, 2026-08-15, on the brief above (`docs/fable_brief_sell_the_close_2026-08-15.md`).
Baseline HEAD `eb8845e`, worktree branch `worktree-agent-a3a4f984a2182e056`.
All numbers seed 11, kawashigi tape, `ours/tape` unless said otherwise.

### Two instruments, and which world each number lives in

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

### The mechanism chain, as measured

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

### Delta 1 — `cover.MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE` (commit 798d459)

On the last day only, a stop whose exact key misses is still seated on the unit the solve chose,
provided the job at that tile has ops a SUBSET of the solved stop's. Earlier days keep the exact
key (pinned by `tests/test_a_last_day_stop_survives_losing_its_upkeep.py`, red/green/red cycle).

Measured alone: byte-identical in both worlds; d29 exact-key misses fall 14 -> 9.
The five reduced pen stops seat where the solve put them. Null on its own, by construction.

### Delta 2 — `NO_UPKEEP_ON_THE_LAST_DAY = True`, gated once for every path (commit c1c49f7)

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

### Delta 3 — `WALK_THE_LOAD_HOME_DAYS = (10, 29)` (commit 30ad651)

The endorsed shape: `deliver=True` on d29, so `plan()` materialises each tour's closing walk and
takes it when it fits the budget the upkeep just freed. The first recorded attempt recovered 7 of
58 precisely because that slack did not exist yet.

Test world: stranded 51 -> 28 (~$672), d29 sell fills 123 -> 148 — the tape's own d29 number —
money $83,826 -> $84,560.
Grid world: op rows byte-identical, sold $9,547 -> $9,543 (a -$4 fill-price slide). On that board
d29 harvests 26 and the tours are full, so the appended walk fits nowhere. Not a regression;
kept for the test-world gain.

### Delta 4 — survival waters, rotation waters and weed digs (commit efd3dfa)

The d29 trace (`data/logs/fable_d29_trace.log`) showed u4 DIGging weeds at (1,0) and (3,0) at
h17/h20 and ending the season at (3,1) holding 3 units. Three more "buys only a tomorrow" ops,
gated on the same master switch: the survival WATER (saves a tile from tonight's rollover), the
rotation WATER (the same purchase spread over two days), and the WEED DIG that `_live_ops`
re-derives at any visited tile whatever the plan priced. The in-window water is deliberately
KEPT — it adds a yield unit the same day, and the tape emits 11 of them on its own d29.

Grid world: d29 dig 5/0 -> 0/0, sell 120 -> 123, close $152,848; weeds at close 1 -> 6, which is
free (the tape closes at 14). Test world: stranded 28 -> 26, d29 sell 148 -> 153, money $84,699.

### Delta 5 — trim the tail that cannot come home, d29 only (commit 407d08d)

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

### Delta 6 — the last-day deadline walk (executor, commit d0a21f1)

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

### Null, reverted: `feed_days(29) = 0`

After delta 6 the recovered wheat sat in the d29 shed unsold (money moved $0 in both worlds), and
the feed reserve — `feed_days(day) * herd` wheat held back from sale — was the suspect. Measured
**byte-identical in both worlds** and reverted the same hour. The binding constraint on d29 wheat
sales is the SCHEDULE's sell row: the agent offers what the row still owes
(`CUMULATIVE_SELLS`/`SELL_CARRY_DAYS`), the d29 wheat quota was already filled, and wheat beyond
the row is never offered whatever the reserve says. Logs: `fable_d7_sellguard_*.log`.
A "flush the whole shed at the close" sell rule is the open follow-up if that money is wanted;
it is a market-block change, not a routing one.

### Null, reverted: the yield gate (`yield_is_deliverable`)

"On the last day do not pick what cannot be carried home" — a filter at the `_live_ops` site and
the underfoot HARVEST, `24 - h >= dist + 2`. **Byte-identical in both worlds and reverted.**
The mechanism: it was designed against the PRE-delta-6 trace (u7's h20 harvest six tiles out).
With the deadline walk live, a hand is either loaded — and the deadline clears its route before
any undeliverable stop is reached — or empty, and no empty hand in either world reaches a
yielding stop past the bound. The gate guarded a path the deadline had already closed. Designed
off a stale trace: re-trace after every behavior change before building on one.
Logs: `fable_d8_yieldgate_*.log`.

### The quota finding

The d29 schedule row asks for exactly 148 units (`{WHEAT 92, WOOL 8, FERT 9, STRAW 6, MILK 27,
CARROT 6}` — the tape's own close) and we fill 153-154 with the cumulative carry. From there the
market block offers nothing more whatever sits in the shed: the deadline walk's recovered wheat,
and the feed-reserve null above, are both bounded by the ROW, not by the shed or the reserve.
Selling past the plan's row at the close is the open money question — a market-block change,
out of scope here.

### Secondary target — d28 pen HARVEST priced CRITICAL (commit 5dbff17)

`BANK_THE_FIELD_ON_THE_LAST_FREE_DROP_DAY = True` makes all 7 of
`tests/test_the_second_to_last_day_banks_the_field.py` pass. The recorded null re-confirmed:
grid world byte-identical (d28's solved route already seats everything with slack). Kept ON for
the pricing the test pins, and because the test-fixture world shows what it buys when a d28
does differ: d28 water 35 -> 37, one drop moves d28 -> d29, money $84,699 -> $84,945 (+$246).

### Where it stands

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

(This xfail's fate after 2026-08-17 is recorded in the next dated section below: the fixture was
not changed, but a different, apparently later-numbered stranded-load test went XPASS at 0
units. See the **UNRESOLVED CONTRADICTION** flagged there.)

### Remaining candidates, unexplored

- Mid-tour drops on d29 for shed-adjacent tours (u8 worked the (4,x) column all afternoon one
  tile from the shed, holding milk from mid-day; `DELIVER_MIN` never triggered).
- Gate `THIRSTY_CROP_PULLS_AN_IDLE_HAND` on the last day — its water buys a tile that dies at
  scoring, and delta 4 newly creates dying d29 tiles for it to chase. Unmeasured; possibly null.
- Sell past the row at the close (the quota finding).
- The brief's open question — why the tape harvests 32 on d28 to our 27 with identical
  plantings — is still unexplained; nothing here touched d28 seating.

### Logs

All under `data/logs/`: `fable_close_baseline_{stranded,grid30}.log`,
`fable_d1_keying_*.log`, `fable_d2_noupkeep_*.log` (the half-step),
`fable_d2b_noupkeep_*.log`, `fable_d3_deliver_*.log`, `fable_d4_notomorrow_*.log`,
`fable_d5_trim_*.log`, `fable_d6_deadline_*.log`, `fable_d7_sellguard_*.log` (null),
`fable_d8_yieldgate_*.log` (null), `fable_d9_bankfield_*.log`, and the three traces
`fable_d29_trace.log` (baseline+d3), `fable_d29_trace_after.log` (after d5),
`fable_d29_trace_d6.log` (after d6).

## 2026-08-15 — Why planted ground stops producing from d19: ground-turnover latency, not digs, fert or caps

Folded in from docs/fable_production_decay_d19_2026-08-15.md.

Seed 11, tape `kawashigi`, weeds 0.0, worktree at `af3db5d` with the OLD
(victor-solved) `solved_days.py`. 30-day replay on the grid environment (recorded economy + shop
draw). Probe: scratchpad `decay_probe.py`, logs `data/logs/fable_decay_probe.log` / `_v2.log`,
`fable_spent_dig_trace.log`. **Per-tile counts here are route-sensitive and will shift when the
solved_days regeneration lands; the rule-level mechanics will not.**

### The mechanics that govern everything below (from `reference/kaggriculture.py`)

- An ongoing crop has exactly `max_yield` production events (strawberry: 4, every 2 days from age
  10). Each event adds 1 unit (2 if the tile was watered that day AND fertilized), **clamped at
  `max_yield` held** (`:795-800`).
- At the final production, `max_lifespan_step` is set (`:801-802`) and from the NEXT day the tile
  DECAYS: `_decay_plants` runs **every step** (`:944`), eats 1 held unit every 2 steps, and turns
  the tile into a WEED when it hits 0 (`:752-766`). A harvested spent tile (0 units held) weeds
  **within 2 turns of the next dawn**. So the final-production day is a one-day window to harvest
  AND dig, or the square stalls as a weed.
- Weeds therefore have TWO origins with weeds off: thirst (`consecutive_unwatered >= 2`) and
  decay. The project's standing memory "every weed is a missed water" is incomplete -- decay weeds
  outnumber thirst weeds on both farms.

### Q1 -- Are we digging crops he keeps? NO. We dig the same things, LATE.

Every DIG classified by what stood under it (ours 54 / tape 40 this run):

    ours, season:  18 PLANT(STRAWBERRY, y=0, SPENT)   21 WEED(decay)   14 WEED(thirst)   1 other
    tape, season:  31 PLANT(STRAWBERRY, y=0, SPENT)    5 WEED(decay)    0 WEED(thirst)   4 other

`DIG_A_SPENT_ONGOING_CROP` (`router.py:1096`, offer at `:765-769`) is correct and both sides play
it -- the tape digs MORE spent strawberries than we do, promptly, and replants behind them. Our
surplus digs are the bill for weeds we created: **34 weed births vs his 10**
(ours: 13 thirst + 21 decay; his: 0 thirst + 10 decay). Nothing fires too early; tiles die and the
corpse then sits as a WEED holding ground that late-season replanting could use (strawberry
replant stops paying at d19: `plant_prize` needs `days_left >= first = 10`).

No rule digs live crops: zero PLANT digs with units held, zero unspent PLANT digs, both farms.

### Q2 -- Is the extra fertilize buying anything? YES, at near-tape efficiency. Not the thief.

    ours:  100 ops  = 49 STRAWBERRY + 51 WHEAT, 98 effective / 2 no-op
           bonus units actually banked: 88 ongoing + 97 one-shot = 185  ->  1.85 units/op
    tape:   72 ops  = 72 STRAWBERRY, all effective
           bonus units banked: 142 ongoing + 0 one-shot         ->  1.97 units/op

The +28-45 op gap is us fertilizing WHEAT, which he never does, at 1.9 banked units/op -- each op
costs a turn plus a fertilizer that would sell for $20-50 late, against ~2 wheat units (~$50 base).
Marginal in dollars, defensible, and NOT a mechanism for the harvest gap. If anything is trimmed
here it should be measured on its own; expected effect is small either way.

### Q3 -- Are ongoing tiles sitting at cap discarding production? NO. Zero, both farms, all season.

Replaying the refresh arithmetic on every h23 board: **0 production units discarded at cap for us,
0 for the tape, over 30 days**. Harvests always intervene before a tile fills. The cap-discard
theory is dead; do not re-derive it.

Units lost to DECAY of spent tiles are near-parity too: ours 92, tape 82 -- both sides harvest the
final production a little late sometimes; this is not where the gap lives either.

### What the d19+ decay actually is: standing-crop attrition + stalled squares

    harvest d19+ (this run):   ours 247 / tape 275
    weed births:               ours 34  / tape 10
    strawberry lifecycles completed:  ours 13 / tape 31

Two attrition channels, neither of them the briefed hypotheses:

1. **Thirst kills our live strawberries mid-life** (13 vs his 0), so the ongoing population that
   should still be producing at d19-d27 is 5/14. Each death also removes every future production
   and leaves a WEED to dig.
2. **One-shots left past their window rot into decay weeds** (the bulk of our 21 vs his 10) --
   yield already grown is eaten at 1 unit per 2 turns and the square stalls until dug.

Fewer standing producers -> fewer harvests -> the late sell collapse. The board-state rows
(animals/pens/tiles/hands identical) stay clean because none of this touches the herd.

Caveat on the 13 thirst weeds: `LATE_SEASON_TRIAGE` deliberately stops watering tiles that cannot
produce again before d29, so part of the post-d19 thirst count is policy, not defect. Splitting
those by remaining value is the first step of any fix here.

### The spent-tile DIG lifecycle, traced (`fable_spent_dig_trace.log`)

Caveat first: one-shots carry `max_lifespan_step >= 0` from PLANTING (`kaggriculture.py:224`), so
"spent" filters must be ongoing-only; the trace's clean rows are the strawberries, d23-d28.

    our spent strawberries, whole season:            13   (the tape completes 31)
      DIG offered same day:                          11   (the 2 d28 non-offers are correct:
      dug same day:                                   9    `plant_prize` = 0, digging pays nothing)
      DIG covered but LOST at execution:              2   (9,4)@d23 cost 23/23, (9,2)@d24 cost 22/23
                                                          -- both on OLD precomputed days, both
                                                          zero/one-margin tours, only HARVEST ran

Two conclusions. First, the reason the tape digs 31 spent strawberries to our 18 is not diligence
we lack -- it is that **2.4x more of his strawberries live long enough to finish**. Ours die young
of thirst (the lost-rescue family in the watering doc); his 0 thirst weeds against our 13 is the
same fact from the other side. Second, our 21 decay weeds are mostly NOT strawberries at all: they
are **one-shots (wheat/melon) left past their window holding yield until `_decay_plants` rots them
to weeds** -- the already-documented unharvested-wheat defect (`_one_shot_is_finished`'s TRIED
note: 32 of 66 wheat standing at season end; the forced-harvest fix measured -$92 and was
reverted because the harvest could not reach a sale in time).

### The shared root, and the candidate lever (NOT implemented -- routes are being regenerated)

This is the same single-window reliability shape as the watering deaths in
`docs/fable_watering_post_d8_2026-08-15.md`: a job that MUST run on one specific day, seated in
zero-margin or over-budget tours (packing cost model vs shipped `materialise` disagree on
RESERVE_DAYS; 25/23 and 26/23 tours observed on d15), where a 1-2 turn arrival slip
(`docs/spawn_ring_misprediction_2026-08-12.md`) deletes the tail stop. Two symptoms, one defect.

Candidate rule-level delta for after the regen: `_at_risk_tiles` (`schedule_agent.py:142`) marks
"skipping today's work destroys something tonight" for unfed animals and unwatered crops -- but a
tile on its final-production day IS in that class (it decays and weeds overnight) and is not
marked. Marking `max_lifespan_step >= 0` (or final-production-today) tiles at_risk would route
their harvest+dig early through the exact machinery that already protects feeds and brink waters.
Red-first test shape: "a tile whose last production lands today is covered as at_risk". Must be
day-gated >= 9 (d0-d8 tape-match) -- first spent strawberries appear ~d17-d19, so the gate is free.

### Route-sensitive vs durable

Route-sensitive (will shift with solved_days regen): every per-day count, the 46%/76% split, the
specific tours. Durable: the decay clock and one-day window, two weed origins, zero cap discards,
fertilize efficiency ratios, `plant_prize` positivity through ~d28, the at_risk gap for spent
tiles, and the negative verdicts on all three briefed hypotheses.

## 2026-08-17 — The last two days: what was dead, what was fixed, what is still open

Folded in from docs/the_last_two_days_2026-08-17.md.

Measured 2026-08-17, branch `kawashigi-plan`, seed 11, shipped `kawashigi` plan.
Grids: `data/logs/d29_baseline_2026-08-17.log`, `data/logs/d29_after_2026-08-17.log`.

### The mechanism

`_end_of_day` runs `_drop_inventories_to_shed`, so a load carried at dusk reaches the shed for free.
On d29 that same drop lands AFTER the final `_process_market` (`kaggriculture.py:942` then `:946`),
so produce held at the close is discarded and produce left standing is never money.
d28 is therefore the last day a harvest banks itself.

### Two things were dead or stale

**`banking = False`** (`schedule_agent.py:137`) gated the d28 "bank the field" branch on a hardcoded
False, pointing at a `BANK_THE_FIELD_ON_D28` constant that no longer existed anywhere in `kagg/`.
It measured a null originally because d28 is a SOLVED day with slack, so promoting a ripe tile into
the at-risk set changed no route.
Deleted; the deadline belongs in the price, not in that set.
(This is the same feature the 2026-08-15 brief above lists under both names,
`BANK_THE_FIELD_ON_D28` / `BANK_THE_FIELD_ON_THE_LAST_FREE_DROP_DAY`, as tried-and-null three ways;
`BANK_THE_FIELD_ON_THE_LAST_FREE_DROP_DAY` is the surviving name, shipped in commit `5dbff17` above.)

**The stranded-load gap is CLOSED.**
`test_the_season_does_not_end_with_the_crew_holding_sellable_goods` was `xfail(strict=True)` over 51
units (~$1,192).
It went XPASS: the marker did its job and reported the day had landed.
d29 `drop` is now 9/9 against the tape.
`NO_UPKEEP_ON_THE_LAST_DAY` freed the turns and `cover.MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE` reseated
the reduced stop; both halves the old note asked for.
Marker removed so a regression is a plain failure.

**UNRESOLVED CONTRADICTION — needs a measurement.**
The 2026-08-15 report above (`fable_close_the_season_2026-08-15.md`, "Where it stands") measured
stranded at **16 units** against `TOLERATED_UNITS = 12`, kept the xfail strict, and gave two
named caveats (the fixture plays `range(719)`, not the full 720 turns, and the marginal units are
quota-bound). This 2026-08-17 report describes a *different* test name
(`test_the_season_does_not_end_with_the_crew_holding_sellable_goods`, threshold 51 units) going
fully XPASS with its marker removed. It is not written down here whether this is the SAME xfail
target renamed and re-thresholded between the two dates, or two different tests measuring
different fixtures, and if the former, what changed the measured 16 down to 0.
Both source documents are kept verbatim above and here; resolve by reading both test files at
their current HEAD and confirming which (if either) still xfails.

### The one real gap, implemented

A ripe **pen** on d28 was never promoted.
A crop reaches CRITICAL through `_last_safe_age` because it has a filling window that closes; a pen
has no such window, so nothing ever promoted it.
`router.animal_ops` now adds CRITICAL to a HARVEST prize on `SEASON_DAYS - 2`, d28 only.

Red first, on record in `data/logs/lastday_tests_2026-08-17.log`:
`d28 pen HARVEST priced at 640, below CRITICAL`.
All 20 last-day tests pass after.

### What it measured, and the ceiling it hit

    row          d25      d26      d27      d28        d29
    harvest    27/29    24/14    26/35    32/32      19/19      unchanged, before and after
    sell       95/149   87/80    92/72    84 -> 87   160 -> 159
    drop        2/0      2/0      0/0      0 -> 1     9/9
    pass        2/0      0/1      0/0      0 -> 13    22/56

    final money   154,740 -> 155,155   (+$415), tape 150,076

**d0-d27 money is byte-identical between the two runs**, so the delta is attributable, not seed
noise.

**Harvest did not move, and that is the finding.**
d28 and d29 are both in `SOLVED_DAYS` (12-29, `UNSOLVE_DAYS = ()`); d29 is a stored solution of 37
stops.
`_apply_precomputed` seats stops by their `(tile, ops)` key and never prices them, so changing a
job's prize cannot move a solved day -- it only reaches the leftover greedy.
The +$415 is that margin and nothing more.

**A price change to a solved day requires re-solving that day.**
`scripts/resolve_days.py --days 28,29` was running when this was written; its result is not in here.

### Traps hit today, recorded so they are not re-hit

- `scripts/diagnose_season.py` hardcodes `top_guys/90976060/schedule.json`, NOT the shipped
  `kawashigi` plan. It reports a $52k season against the real $155k. Numbers read off it early in
  this session were discarded.
- **Seeds do not vary this harness.** `--seed 11` and `--seed 14` produce a byte-identical grid:
  shops come from the replay, `--weeds 0`, and board terrain is a pure function of coordinates.
  A "second seed" check here is vacuous.
- `tests/test_the_second_to_last_day_banks_the_field.py` quotes d28 27/32 and d29 27/19 in its
  docstring. The live grid is 32/32 and 19/19 -- the back-loading it was written against is gone.

### Open: eight red tests in the planner gate

`tests/test_the_first_seven_days_match_the_plan.py`, 8 failed / 6 passed, and they PRE-DATE this
work (confirmed by stashing the edits and re-running).
They are live defects with coordinates, not test rot:

- a hand walks off a tile holding a hungry animal **while carrying its feed**, 14 times over d0-d6
- animals unfed at dusk with wheat on the farm: d0 leaves 4 hungry with 8 WHEAT in the shed
- a PLACE planned onto a hand that does not build that pen (d0, tile (4,3): BUILD u1, PLACE u4)
- SELL and BUY_PRODUCT diverge from the plan on d2-d6

### The four new losses are a different shape

`data/seed_scripts/ladder_2026-08-17/`, 23 replays now.
93850943 and 93849246 are byte-identical in every op count for BOTH seats -- same board, same
opponent script, different names. Three distinct games, not four.

                           water       harvest     plant      feed       care
    93850943 / 93849246   1221/1010    386/390    194/199    316/290    318/967
    93850122              1225/946     385/394    182/187    321/321    323/318
    93846497              1171/947     385/394    176/187    321/321    321/318

    93850943  vs kaggricultureomnidimensionalut  100,033/106,095  LOSS -6,062
    93850122  vs Пётр П                          125,613/131,285  LOSS -5,672
    93849246  vs Panchajanya Banerjee             54,940/ 60,306  LOSS -5,366
    93846497  vs Sirui Zeng                       89,509/ 98,615  LOSS -9,106

**Harvest is LEVEL in all of them.** These are not harvest-deficit losses, so the d28/d29 work in
this doc would not have flipped any of the four.
We out-water by 200-275, as in every game including the wins.
Plant is 5-11 behind.
One opponent runs CARE 967 to our 318 -- above the ~570 ceiling of one-per-pen-per-day, so it is
re-emitting CARE on already-cared pens; offers, not fills, and unchecked.

Losses of $5.4k-$9.1k against this morning's $158-$1,521.

**Correction on the CARE number above.** 967 is CARE EMITTED, not CARE landed. `cared_today` gates
the effect, so a repeat CARE on an already-cared pen is a silent no-op and at most one lands per pen
per day (~570 ceiling). It says their agent spams CARE. It does NOT say they care 3x more than us.
Same class of error as summing sell offers; see `feedback_offers_are_not_fills`.

### The herd never moves, and one board had ZERO milk shops

Milk slots counted from the FINAL town draw; cow/sheep counted off the final board.

    game       milk slots   our herd            their herd          result
    93849246       0        COW 10 / SHEEP 4    COW  8 / SHEEP 4    LOSS -5,366
    93846497       2        COW 10 / SHEEP 4    COW 10 / SHEEP 4    LOSS -9,106
    93850943       3        COW 10 / SHEEP 4    COW  8 / SHEEP 4    LOSS -6,062
    93839424       3        COW 10 / SHEEP 4    COW  9 / SHEEP 4    LOSS   -158
    93836751       3        COW 10 / SHEEP 4    COW 10 / SHEEP 4    LOSS -7,727
    93850122       5        COW 10 / SHEEP 4    COW 10 / SHEEP 4    LOSS -5,672

**We run 10 cows / 4 sheep in all six, across milk slots of 0, 2, 3, 3, 3 and 5.**
The split never moves.
On 93849246 the town draws NO milk shop at all and we still stock ten cows -- milk floors at $1 with
zero drain and we flood a book with no buyer.
The opponents do vary (8 cows on the milk=0 board, 10 on milk=5), though not cleanly monotone: at
milk=2 they also run 10.

This is `MILK_POOR_SHOP_COUNT = 1` again, now with a milk=0 board proving it does not fire.

**Caveat that has to be checked before acting.** Milk slots here are the FINAL town; the herd is
committed around d3-d7 when few shops have unlocked. This is not yet evidence the decision was
knowable at the time it was made. Measure the shop set AT the herd decision before changing the
rule.

## 2026-08-17 — Late-game turns that could have been harvesting

Folded in from docs/wasted_late_turns_2026-08-17.md.

Measured 2026-08-17 on `~/Downloads/93880775.json`, a fresh ladder download not yet mirrored into
`data/seed_scripts/ladder_2026-08-17/`.
`info.TeamNames = ['BSam79', 'alex chilton']`, so our seat is **1**.
720 steps, `day = i // 24`, `hour = i % 24`.

### The answer: yes, and one case is unambiguous

**On d28 a hand stood directly on top of a 3-unit ripe WHEAT tile `(9,1)` for seven consecutive
hours -- h14 to h22, Manhattan distance 0 -- emitting PASS every hour.**
Not near it. On it.

On d29 at h23, the final hour of the season, **all 8 hands were idle while 18 units stood on the
field**.

### Per-day, our seat, unit-turns from `action['hands']`

    day  unit-turns   work   movement   idle(PASS)   dawn standing
    25      252        141      111            0            119
    26      252        127      124            1            116
    27      252        122      129            1            134
    28      231        116      101           14            107
    29      186         59      106           21             49

Idle is ~0 through d27 then jumps on d28-d29 as the crew draws down (11 -> 10 -> 8 hands).

### Reachable and unharvested

Feasibility test: `hours_left = 24 - hour >= 2 * distance`, i.e. time to walk there and take it.

35 idle hand-hours across d28+d29; **20 of 35 were feasible**.
Deduplicated by `(day, tile)`:

    day  tile     kind           units
    28   (4,6)    WHEAT            1
    28   (9,1)    WHEAT            3
    29   (2,4)    COW pasture      3
    29   (4,6)    WHEAT            2
    29   (5,3)    COW pasture      2

**11 units reachable-and-unharvested. 7 of them were still standing at the actual close** -- the
d29 `(4,6)` wheat and both cow pastures, `(2,4)` and `(5,3)`, never milked.
The d28 `(9,1)` wheat was taken during d29, so it was a delay rather than a final loss.

Total end-of-game standing produce for our seat in this replay was **18 units**; the 7 above are the
subset directly attributable to an idle hand that had the time budget and did not go.

### A separate defect found on the way, NOT counted above

**At hour 1 of every day in d25-d29, `action['hands']` is an empty list while `farm['hands']` shows
10 positions still on the board** (d29: 8), and `action['market']` fires 10 HIRE orders in the same
turn.
So those hands do nothing that hour, without even an explicit PASS.

This is systematic on every day, not a late-game effect, so it was excluded from the harvest numbers
above.
At ~10 hands x 30 days it is on the order of 300 unit-turns a season.
It has not been diagnosed and should be looked at on its own.

### Data-shape trap, recorded because it produced a wrong map first

`farms[seat]['tiles']` is indexed **`tiles[y][x]`**, row then column, per the engine's own comment at
`kaggle_environments/envs/kaggriculture/kaggriculture.py:145` and `_apply_unit_action`
(`fx, fy = pos; tile = farm["tiles"][fy][fx]`).
Hand and farmer positions are stored `[x, y]`, the other way round.

The first pass used `tiles[x][y]` and produced a plausible but wrong tile map.
It was caught with a LOCKED-tile consistency check: `tiles[y][x]` puts all LOCKED hits on the four
legitimate shed-adjacent tiles `(4,4) (5,4) (4,5) (5,5)`, while `tiles[x][y]` produced 260 hits,
most of them bogus.
