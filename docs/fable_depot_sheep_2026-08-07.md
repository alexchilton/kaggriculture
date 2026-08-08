# The depot sheep: what puts SHEEP on (4,4), and why copying it regresses days 2-5

2026-08-07, seed 11, weeds 0.0, Seb's tape, `scripts/breakdown.py --days 7 --diff`.
Baseline defended throughout: `d0=7 d1=6 d2=4 d3=7 d4=7 d5=7 d6=14` (52 cells).
Every change below was reverted; the tree is back to its pre-experiment state
(both files verified byte-identical to backups taken before the first edit).

## Finding 1: nothing moves — the tape's day-0 label at (4,4) is simply wrong

The task asked what MOVES or re-places an animal, because `build_tiles` day 0 says `[[4,4] COW]`
while a SHEEP stands there on day 6.
Answer from a full-replay trace of both sides (PICKUP/PLACE/BUILD/BUY_ANIMAL with unit positions,
plus dawn pen occupancy, days 0-7): nothing moves.
The tape's u0 places SHEEP on (4,4) at day 0 hour 4 and it never changes.
The `build_tiles` label is bad metadata; the schedule's ordered `places` list is the good metadata.

Tape day 0, exactly:

    h0  u0@(4,4) BUILD_PASTURE          market BUY_ANIMAL COW 2
    h1  u0 PICKUP COW x2                market BUY_ANIMAL SHEEP 2
    h3  u0 PICKUP SHEEP x2              (u0 now holds 2 COW + 2 SHEEP)
    h4  u0@(4,4) PLACE SHEEP
    h6  u0@(4,3) PLACE SHEEP
    h11 u0@(3,3) PLACE COW
    h13 u0@(3,2) PLACE COW

So Seb holds both species at once and deliberately walks the sheep into the two shed-nearest pens,
then carries the cows outward.
`places: ['SHEEP','SHEEP','COW','COW']` in the schedule row is this, order-preserved.
Tape pens by day 6 dawn: SHEEP (4,4) (4,3); COW (3,3) (3,2) (2,3) (2,2) (1,3); (1,2) (5,4) empty.

Ours (baseline) day 0: u0 draws 2 COW, places COW on (4,4) at h3;
sheep end at (3,4) (h4) and (1,4) (h21).
Ours by day 6 dawn: COW (4,4) (2,4) (2,3) (1,3) (0,4); SHEEP (3,4) (1,4); (0,3) (5,4) empty.

Note the second structural difference, bigger than the occupant:
the tape's pens grow NORTH from the shed (column 3-4), ours grow WEST along row 4.
That geometry comes from `_next_ground`/`field_order`, and it is upstream of every
north/south/east/west move diff in the breakdown table on every day.

## Finding 2: our own code already knows the right animal, then throws it away

`_refresh_pins` (kagg/search/schedule_agent.py, ~line 403) labels the day-0 BUILD pins from the
ordered `places` list, and the labels are already correct:

    (4,4) BUILD SHEEP   (3,4) BUILD SHEEP   (2,4)..(2,3) BUILD COW x6

The label dies twice:

1. The pin is popped the moment the pen is built (`pins.pop` on BUILD, ~line 573),
   and the kept stop re-derives its PLACE via `_live_ops`,
   which iterates `R.ANIMAL_NAMES = [GOOSE, COW, SHEEP]` over the unit's inventory — COW wins.
2. On the next replan (hires trigger one every morning hour), `build_nodes` (kagg/search/router.py,
   PASTURE/COOP branch, ~line 515) prices a PLACE node for the now-empty pen in the same
   `ANIMAL_NAMES` order over the shed — COW wins again, so the serving unit's `draw` fetches COW.

## Arm measured: honour the pin's animal ("pen intent")

Implementation (all reverted): `state["pen_intent"][spot] = a` recorded in `_refresh_pins`;
`build_nodes(..., intent=)` and `_live_ops(..., intent=)` put the intended animal first in the
candidate order when it is actually available (shed/carried for nodes, inventory for live ops),
falling back to the old order otherwise; plumbed through `_route_actions`.
Two pytests written first and red first (new file `tests/test_depot_intent.py`, deleted on revert):
`build_nodes` and `_live_ops` each return `PLACE SHEEP` for a pen whose intent says SHEEP when both
animals are on offer.
Both went green with the change in.

Mechanically it does exactly what was asked.
Trace with the arm in: SHEEP placed on (4,4) h3 and (3,4) h4, cows outward,
all four animals in pens by h9 — against the baseline's last placement at h21.

Measured, full line (log `data/logs/fable_depot_intent_arm.log`):

    intent everywhere   d0=7  d1=6  d2=6  d3=8  d4=9  d5=8  d6=15   (59 cells)   LOSS

Second arm, to isolate the cause: intent honoured ONLY on the four depot tiles
(`tile in SHED_SET`), everything else exactly baseline
(log `data/logs/fable_depot_intent_depot_only.log`):

    intent depot-only   d0=7  d1=6  d2=6  d3=8  d4=9  d5=8  d6=15   (59 cells)   LOSS, identical

Identical to the cell.
So the whole regression is caused by the (4,4)/(3,4) occupant swap itself, not by any wider
reshuffle — and it is also numerically identical to what DEPOT_PEN_BY_LOAD measured on d2-d6.
Three different mechanisms (value ranking, load ranking, schedule intent) that all end with
SHEEP on the depot pen all land on the same 59-cell line.
The occupant IS the variable; every route to it costs the same.

## Why it regresses: the swap breaks day-0 feeding and strands two wheat

d0 stays at 7 cells but its CONTENT changes, which the count hides:

    baseline d0 diffs: pass north south west east pickup drop
    intent   d0 diffs: pass north south west drop feed(-2) care(-2)

With the arm in, two animals are never fed or cared on day 0 despite being placed by h9,
and a new persistent row appears from d1 onward: `sh:wheat +2` every dawn, all season.
The resequenced draws (u0 now draws SHEEP, u1 draws the 2 COW) leave the feed wheat in the shed;
two day-0 FEEDs are skipped and the two wheat bought for them sit in the shed forever.
The d2-d5 regressions are the knock-on: `pickup +2` appears on d2/d3, east/pass shift,
and d6 gains a cell.
So the arm's failure is not "sheep at the depot is wrong" — it is that our draw/feed sequencing
cannot yet survive the resequencing the swap causes.
The tape's u0 shows the required shape: pick up BOTH species in two consecutive shed turns and
place while holding both, feeding afterwards.

Also noted (coordinator's finding, not mine, not fixed): market orders are truncated to
`orders[:10]` at schedule_agent.py:1377 while `state["bought"]` and the money deduction happen
anyway — any future arm that "placed" a BUY_ANIMAL that never appears in the env is that defect.

## Day 6 itself: the sheep swap alone does not close it

Even with wool coming off (4,4), d6 measured 15, not better.
The wool still reaches the shed too late to fund the h1 strawberry, because `animal_ops` serves
FEED, CARE, COLLECT_FERTILIZER before HARVEST and the first DROP still lands mid-morning —
which is exactly what the YIELD_FIRST arm was about, and that arm alone left d6 unchanged too.
Day 6 needs the conjunction: sheep on the depot pen AND harvest-first at that pen AND a dawn DROP,
so the WOOL 6 sale settles before the BUY_SEED STRAWBERRY order (the slot rule at
kaggriculture.py:535 already does the rest).
Each ingredient measured alone regresses an earlier day, so the conjunction is currently unpayable.

## What I would do next, in order

1. Fix the day-0 draw/feed sequencing UNDER the swap first, as its own arm with its own test:
   a unit that places an animal it drew must still complete that pen's FEED the same day
   (the tell is `feed -2, care -2, sh:wheat +2` on d0/d1).
   Only then re-measure pen intent; d2-d5 should stop moving, and only then can d6's conjunction
   be attempted without paying earlier days for it.
2. Consider pinning day-0 BUILDs at the tape's own `build_tiles` POSITIONS (they are in the
   schedule; `TAPE_ONLY` currently strips them before the agent sees them) while taking the
   animal from `places` order, not from the (unreliable) build_tiles labels.
   That attacks the north-vs-west pen geometry, which is upstream of most move diffs on ALL days —
   but it widens the schedule format, so it is Alex's call, not a quiet change.
3. Treat the tape's u0 hold-both-species pattern as the model for the placement tour:
   two consecutive PICKUPs at the depot, place-nearest-first with the intended animal.

## State of the tree (session 1)

All experiments reverted; `kagg/search/router.py` and `kagg/search/schedule_agent.py` verified
byte-identical to pre-experiment backups; `tests/test_depot_intent.py` deleted.
Logs kept: `data/logs/fable_depot_baseline.log`, `fable_depot_intent_arm.log`,
`fable_depot_intent_depot_only.log`, `fable_depot_revert_check.log`.

---

# Session 2, same day: the draw/feed sequencing fix, measured both ways, both losses

Baseline moved after the orders[:10] truncation fix (28a694a) and PEN_SPOTS (5247b1b, inert).
Confirmed at HEAD 5247b1b before touching anything
(`data/logs/fable_seq_baseline.log`):

    baseline   d0=7 d1=6 d2=4 d3=7 d4=7 d5=7 d6=14 d7=21 d8=15 d9=16 d10=23 d11=23   (150 cells)

## The premise "the bug is visible with the swap off" is HALF true

Swap off, day 0 is CLEAN at count level: 4 FEEDs (h4 h17 h19 h22) and 4 CAREs on both sides.
The defect exists but is compensated: `PLACE_DRAWS_FEED` adds a WHEAT need only to PLACE nodes,
and on day 0 every pen is a BUILD pin, so a builder's draw carries the animal and no feed —
baseline u0 draws `{COW:3, WHEAT:1}` where the single WHEAT comes from the one already-built pen's
PLACE node, not from the two BUILD pins on its route.
The compensation is the idle-replan recovery: tours finish, FEED nodes get planned, wheat is drawn
on a second trip, and the feeds land late (h17-h22 against the tape's h9-h19) but they LAND.
Counts match, so nothing shows in the breakdown; only the hours differ.

Swap on (intent arm re-applied for the trace), the recovery fails and it shows:
u0 draws `{SHEEP:1, WHEAT:1}` and feeds its (4,4) sheep at h4 — fine —
but u1 takes over the two cow placements at the h2 crew replan with draw `{COW:2}` and NO wheat,
places at h6 and h9, and the recovery serves only ONE of the three remaining unfed pens
(u1 re-draws a single WHEAT at h13-h17, FEED h19, CARE h20; the other two pens are never fed).
FEED 2/4, CARE 2/4, and the two wheat bought for the skipped feeds are `sh:wheat +2` forever.

## Arm A: BUILD-for-a-pen draws the feed its placement creates (swap OFF)

Test-first (`tests/test_build_draws_feed.py`, red then green, deleted on revert):
`Node((4,4), [("BUILD","COW",400)]).needs["WHEAT"] == 1`.
Implementation: one edit in `Node.__init__` —
`if o == "PLACE" or (o == "BUILD" and i in R.ANIMALS): needs["WHEAT"] += 1`.
Checked first that `claim`/`in_stock` gate only PLACE animal claims,
so the extra need cannot cause the node to be dropped; it only adds to the depot draw.

    fix alone  d0=9 d1=12 d2=8 d3=8 d4=10 d5=11 d6=16 d7=25 d8=18 d9=22 d10=25 d11=24  (188)  LOSS

d0 7->9 and d1 6->12: the fix does NOT stand on its own merits.
Why it backfires: day-0 wheat arrives as a one-per-hour drip (`BUY_PRODUCT WHEAT 1` from h1),
so a dawn draw demanding wheat that is not in the shed yet re-routes the whole morning —
units loiter at the depot or make extra trips, and every downstream hour shifts.
The tape does NOT carry feed with the day-0 animals either:
its u0 carries only animals (h1, h3, h8) while a separate unit (u1) draws wheat at h8/h14 and
does all four feeds at h9/h11/h17/h19 — a dedicated feeder, not a heavier builder.
The Node comment's "the tape picks up at hours 1, 3 AND 8, moving animals and wheat together"
is contradicted by the replay: h8 is `u0 PICKUP COW x2` and `u1 PICKUP WHEAT x2`, two units.

## Arm B: same fix plus the pen-intent swap

    fix+swap   d0=9 d1=11 d2=7 d3=8 d4=10 d5=11 d6=18 d7=21 d8=18 d9=15 d10=19 d11=19  (166)  LOSS

Also a loss on the days that count first (d0 7->9, d1 6->11), so rejected under the in-order rule.
Noted for honesty, not as an argument: d9-d11 improve (16/23/23 -> 15/19/19),
meaning the late-season herd is genuinely better served when feed travels with placements —
but not from day 0, where the wheat does not exist yet.

## Corrected diagnosis for the next attempt

The swap's real casualty is the RECOVERY, not the builder's load-out.
With three unfed pens, wheat in the shed from h9, and idle units available,
`plan_routes` assigned exactly one FEED stop (u1, draw `{WHEAT:1}` at h13).
The open question is why the other two FEED nodes were never planned or never survived:
candidates are the idle top-up's `spoken`/`free` supply accounting
(`_router_acts`, the `if idle:` branch), the `st["draw"].clear()` that forgets a shortfall item
the moment the first missing item empties the draw (both in `schedule_agent.py`),
and budget-pruning of FEED insertions for committed units whose budgets are stale.
Instrument THAT — log every FEED node built vs planned vs served between h9 and dusk under the
swap — before writing any more Node economics.
A day-0-only alternative shaped like the tape also remains untried:
one dedicated feeder unit that draws wheat mid-morning and walks the pens,
which is a routing pattern, not a needs edit.

## State of the tree (session 2)

Both arms reverted via `git checkout` (files were clean at HEAD 5247b1b this session);
`tests/test_build_draws_feed.py` deleted; the diagnostic intent-arm copy lives only in scratchpad.
Logs kept: `data/logs/fable_seq_baseline.log`, `fable_seq_fix_alone.log`,
`fable_seq_fix_plus_swap.log`.
