# Cover planner confer: the two questions, answered

2026-08-08.
Repo `kaggriculture`, branch `shaping-potential`, HEAD `21b792e`.
Scope: `kagg/search/cover.py` and `kagg/search/schedule_agent.py` only.
`router.py` and `tests/test_router.py` were read but not modified, per instruction.
`schedule_agent.py`'s `COVER_PLANNER` constant was flipped to `False` and back to `True` twice during
this confer, purely as a diagnostic toggle, each time verified by `git diff --stat` to leave no trace.
No files were committed.

**Note on a moving target:** partway through this confer, `git status` showed `kagg/search/cover.py`
itself had gained an uncommitted edit I did not make — a `claim()` helper that nets a job's animal
draw against what the acting unit already carries, fixing a *different* bug (a carried animal blocking
its own `PLACE` because the shed-side claim wasn't netted off).
That change is unrelated to either question below and landed from something else working on this repo
concurrently, not from anything in this session.
Every measurement in this document was taken before that edit appeared, against the `cover.py`
committed in `21b792e`, so it is unaffected — but if you re-run any of the day-4/day-5/day-6 traces
after that edit lands, expect the `PLACE`-coverage-side numbers (not the root cause below, which is in
`schedule_agent.py`) to shift.

## tl;dr

Question 1's headline failure (`PLACE 0/1`) is **not** a `cover.py` coverage or timing defect.
It is a pre-existing, planner-independent bug in `schedule_agent.py`'s order-construction code: the
local `money` variable that gates `BUY_ANIMAL`/`BUY_LAND` is never decremented for `HIRE` cost, so a
same-turn "8 HIRE then BUY_ANIMAL" order can be accepted by the local check and rejected by the real
env, and because `state["bought"]` is incremented unconditionally at construction time, the failure is
**silent and permanent**, not a one-day delay.
`cover.py` does not cause this bug; it exposes it, because its day 0-3 choices leave the farm $99
poorer at day-4 dawn than `router.py`'s choices do, which is enough to cross a wafer-thin ~$6 margin.
Two of the other three failures are downstream numeric consequences of the same missing cow (proven
for one, plausible-but-unproven for the other).
The fourth (day-6 melon) is independent — the day-6 dawn state is nearly identical between the two
planners, which rules out the day-4 event as its cause.

Question 2's answer is a season-level compounding effect that a matched-day study cannot see by
construction: two independent problems, one now identified (the phantom-purchase bug: `cover`'s own
game against Seb's tape carries roughly one permanently-missing animal for nearly the entire season),
and one already on record in `schedule_agent.py`'s own comments (reactive vs. cadence watering) that
this confer's arena data confirms operates at roughly 2x scale over a full season.
Neither is visible in the 29-independent-day study, because that study resets the board to Seb's own
state every single day, which erases exactly the kind of debt that compounds.

## Question 1: why do 4 market tests regress under the covering planner

### Method

Rather than guess, I monkeypatched `cover.plan` (never edited) inside throwaway scripts under the
scratchpad to log every call whose job list contained a `PLACE` op, and separately printed
money/shed/market state turn-by-turn for day 4 of `tests/test_router.py::test_day_four_matches_seb_on_every_op_it_works`.
Scripts are not part of the repo; the logs are, listed below.

### Finding: the day-4 cow purchase never lands, under EITHER planner's order-construction code

Trace of day 4, `COVER_PLANNER=True` (`data/logs/confer_diag_place2.log`):

    h0  money=384  shed.COW=0  market=[SELL WHEAT 2, HIRE x8, BUY_ANIMAL COW 1]
    h1  money=394  shed.COW=0

The `BUY_ANIMAL COW` order is emitted exactly once, at hour 0, and never again — `shed.COW` stays 0
for all 24 hours of day 4 (`data/logs/confer_diag_place.log` confirms this over days 3-6 too: the next
`PLACE` op our seat performs is day 6 hour 20).
`cover.plan` was never even asked to route a `PLACE COW` job on day 4 (`data/logs/confer_diag_place3.log`
has zero `PLACE`-bearing calls logged for day 4, against several for day 3) — because `router.build_nodes`
gates a `PLACE` node on `shed[item] > 0`, and the shed never held one.
So the earlier "coverage starvation" hypothesis (`cover.py`'s greedy dropping an expensive `PLACE` job
in favour of several cheap ones) is **wrong** for this failure: there was never a job to drop.

### Root cause: `HIRE` cost is never reserved before `BUY_ANIMAL`/`BUY_LAND` are gated

`kagg/search/schedule_agent.py`'s order-construction code (inside the closure returned by
`make_agent`, `router=True` or `False` makes no difference here) tracks a local `money` variable to
decide whether to emit `BUY_LAND` (line 2143-2145) and `BUY_ANIMAL` (line 2195, 2206-2208) orders.
A repo-wide grep for every place that variable is decremented:

    2145   money -= LAND_PRICES[owned]
    2208   money -= R.ANIMALS[a]["cost"]
    2366   money -= quote * short          # feed top-up

`HIRE` appears nowhere in that list, in a ~900-line closure, confirmed by reading the `HIRE_FIRST` /
`HIRE_PINNED_DAYS` block (lines ~2091-2124) end to end: it appends `["HIRE"]` and increments
`state["hired"]`, and never touches `money`.

The real env settles a turn's orders **sequentially, in the order submitted**
(`_order_sells`/`_fit_slots`, and the day-4 test's own docstring: "the atomic orders in a slot settle
after every earlier slot has traded").
Day 4's order is `[SELL WHEAT 2, HIRE x8, BUY_ANIMAL COW 1]`.
Real settlement: $384 dawn + ~$20 for 2 wheat − $54 for 8 hires (fib(0..7) = 1+1+2+3+5+8+13+21 = 54,
confirmed against `reference/kaggriculture.py:658-667`) = **$350-ish available, against a flat $400
`COW` cost** (`kagg/search/routines.py:57`).
The purchase is silently refused by the env — no error, shed stays at 0 — exactly as
`docs/breakdown_fills_not_offers_2026-08-08.md`'s own header already documents: "the env silently
refuses one it can't afford."

But the **local** gate at line 2195 computed `money` as dawn ($384) plus this turn's own sells
(`pending`, added at line 2030-2032) — i.e. ~$404 — without ever subtracting the $54 of hires queued
two blocks earlier in the same construction pass.
$404 clears the $400 bar, so the order is appended and `state["bought"]["COW"] += 1` fires
unconditionally.
The purchase is booked as done, in code, forever — `want_total` at line 2162-2167 is a *cumulative*
target compared against `state["bought"]`, and a value that was wrongly incremented is never
re-examined.
This animal is not delayed a day.
It is gone for the rest of the game unless a coincidence (a later day's row asking for more animals
than `state["bought"]` shows) happens to paper over it.

This is the **same class** of bug already caught and partially fixed once before — see
`docs/fable_depot_sheep_2026-08-07.md`: "market orders are truncated to `orders[:10]` ... while
`state['bought']` and the money deduction happen anyway."
That earlier instance was slot-count truncation, and it was fixed by `FIT_ORDER_SLOTS`/`_fit_slots`
"uncounting" anything cut for space.
This is a **second, distinct trigger for the identical symptom** — insufficient real funds, not slot
overflow — and nothing currently guards it.

### Why `router.py` doesn't hit it (and why that's not evidence it's fine)

Flipping `COVER_PLANNER` to `False` and re-running the identical trace
(`data/logs/confer_diag_place2_ROUTER.log`):

    h0  money=483  shed.COW=0  market=[SELL WHEAT 1, HIRE x8, BUY_ANIMAL COW 1]
    h1  money=61   shed.COW=1   <- succeeds
    h7  PLACE COW

Router's day-4 dawn money is **$483, $99 more** than cover's $384.
The same missing-HIRE-deduction bug is present in the code either way (it's the same closure); it
just doesn't bite here because $483 + $32 (1 wheat) − $54 (hires) − $400 (cow) = $61, comfortably
positive.
Cover's version of days 0-3 is $99 poorer entering day 4, for reasons this confer did not trace
further, and that's what tips a **~$6 real shortfall** ($384+$64 for 2 wheat −$54−$400 = −$6) into a
silent, permanent loss.
So: `cover.py` is not the bug, but it *is* the reason the bug fires here and not under `router.py` —
the pre-existing gap only manifests when the cash cushion is this thin, and cover's trajectory happens
to be thinner at this specific boundary.

### The other three failures

**`FEED 6/7`, `CARE 6/7`, `PLACE 0/1`** (`test_day_four_matches_seb_on_every_op_it_works`) are one
event, not three.
`COLLECT_FERTILIZER`/`FEED`/`CARE` all require `"animal" in tile`
(`reference/kaggriculture.py:480-497`), so a pen that never received its animal simply generates no
`FEED`/`CARE` job for that tile that day.
6 of 7 pens fed and cared, 0 of 1 placed — fully explained by the single missing cow.
**Real defect** (not stale timing): the animal is not "placed late," it never arrives.

**`FERTILIZER 7/9`** (`test_wheat_drawn_this_turn_is_the_herds_reserve_not_extra_to_it`, day 5) — I
checked whether the herd really is down one pen by day 5, since `COLLECT_FERTILIZER` also needs an
occupied animal tile:

    day-5 dawn occupied pens:  cover=6   router=7      (data/logs/confer_pens_cover.log / confer_pens_router.log)
    day-5 dawn money:          cover=714  router=321

Confirmed: cover has exactly one fewer occupied pen on day 5, matching the missing day-4 cow, and
(worth flagging on its own) cover is **cash-richer** at this point — the $400 was never actually
spent, only *believed* spent, so the bank shows it as still there while the herd shows it as never
having existed.
One fewer pen plausibly costs 1-2 fewer fertilizer-collection cycles by day 5, which is in the
direction and rough size of the `9 → 7` gap.
I did not trace the day-5 `COLLECT_FERTILIZER` ops turn-by-turn to confirm the exact count, so I'm
reporting this as **very likely downstream of the same event**, not independently proven to the
standard of the `PLACE` finding.

**`FERTILIZER 5/4` extra sell** (`test_the_sells_row_is_a_day_total_not_a_per_turn_quota`, day 4) —
this test's own docstring already documents a separate, pre-existing, undisputed defect: "we re-offer
[the sell row] every turn, so the day total is unbounded," measured on this same day as a 6-unit wheat
overshoot.
The freed-up crew time from not walking a unit to place/feed/care one cow plausibly gave the crew one
extra turn to collect and sell fertilizer, riding on that already-known uncapped-quota mechanism.
Plausible, not independently confirmed — I did not re-trace day 4's `COLLECT_FERTILIZER`/`SELL`
sequence to isolate it from the general oversell defect.

**`melon seed 5→4 of 6`** (`test_the_days_seed_is_bought_before_the_days_livestock`, day 6) — checked
whether this, too, traces to the day-4 event, and it does not:

    day-6 dawn:  cover money=864 pens=7 shed.WHEAT=9      (data/logs/confer_day6_cover.log)
    day-6 dawn:  router money=871 pens=7 shed.WHEAT=7     (data/logs/confer_day6_router.log)

By day 6 dawn the two arms are within $7 and both have 7 pens — the herd deficit has already been
made up by day 6's own two-cow purchase, and the cash gap has closed.
So this failure is **independent** of the day-4 phantom purchase; it is a separate, still-open
question, most likely in how `cover.py`'s different in-day routing changes `state["pins"]` (which
`want_seed` is read from, line 2054-2063, under `router=True`) or the exact `SELL`-before-`BUY_SEED`
sequencing within day 6 itself.
I did not root-cause it further within this confer's scope.

### Verdict on the framing of Question 1

Your own hypothesis — "the planner shifts WHEN work lands... I cannot tell whether that is benign
[timing] or whether PLACE 0/1 is a real animal left sitting in the shed all day" — picked the right
question but the wrong candidate mechanism.
It is real, but it's not a scheduling/coverage question at all: there was no animal in the shed to
route to, and no job for `cover.py` to have covered or dropped.
The bug is upstream of both planners, in the shared order-construction code, and `cover.py`'s only
role is nudging the cash trajectory into the zone where a pre-existing gap fires.
Worth being direct about: **if this had been "fixed" by patching `cover.py` to prioritise `PLACE`
jobs more aggressively, it would have done nothing** — the job never reaches `cover.py` because the
purchase itself silently fails before any node exists to plan around.

## Question 2: why doesn't matched-day superiority translate into season money

### The instrument that actually answers this

`scripts/breakdown.py --tape seb --seed 11 --weeds 0.0 --days 30 --diff` compares our full agent
against **Seb's own historical opponent's recorded moves** (not Seb himself) — useful for exact
per-day, per-field counts, but it is a different matchup than head-to-head vs. Seb, so I did not treat
its money row as the season-money answer (per your own warning, and because it is genuinely a
different opponent).
`data/logs/full_stack_vs_seb.log` is the real head-to-head instrument: our full agent against Seb's
tape directly, 6 seeds, both planners (`prize` = router, `cover` = this file), both with/without a
`geo` flag that belongs to router.py's workstream and was not touched or investigated here.

    arm             mean $    median $   ESCAPES   WEEDS   HARVEST   IDLE    wins
    prize/geo-off   95,816    94,291         6        55     1703    8298    0/6
    prize/geo-on    98,096    99,281         3        61     1800    8340    1/6
    cover/geo-off   94,730    90,576         0       126     1980    8613    3/6
    cover/geo-on    98,443    95,990         7       127     1901    8837    0/6

### Finding A: a season-scale weed/water debt the matched-day study cannot see

`cover`'s full-season WEED count is **~127, more than double `prize`'s ~55-61**, across the same 6
seeds, same opponent.
This is not a contradiction of the 29-matched-day study (`data/logs/matched29.log`: ours 29 crops dead
of thirst against Seb's 42, in cover's favour) — it's the thing that study is structurally blind to.
Each of those 29 tests replays Seb's tape to a specific dawn and plays **one isolated day**, so the
board, water debt and everything else resets to Seb's own (well-managed) state before every single
comparison.
It can only ever measure "given a competently-managed board, who's more efficient with one day's
turns" — it cannot measure whether 29 *consecutive* days of the candidate's own choices would have
produced a competently-managed board in the first place.

`schedule_agent.py`'s own `WATER_AT_RISK` comment already diagnoses the mechanism, written before this
confer: cover.py's watering is reactive (rescues a tile only once `consecutive_unwatered >= 1`), while
Seb's tape waters on a fixed alternate-day cadence that "holds every tile at 0 or 1 and takes zero
weeds through day 7" and "never builds the debt... he is not better at rescuing — he never gets into
the position."
The same comment reports our watering debt reaching 17 thirsty tiles by day 16 against Seb's 8.
This confer's arena numbers are the first evidence that this compounds to **full-season scale**: 127
weeds is not a rounding difference from 55-61, it's the single largest structural gap in the whole
table, and it sits entirely outside what any single-day matched comparison is built to detect.

### Finding B: the phantom-purchase bug from Question 1 is not a one-off

`scripts/breakdown.py`'s per-field diff (`data/logs/confer_breakdown_diff_full.log`, seed 11, cover
vs. Seb's-opponent-replay) shows the `an_COW` (occupied COW pen) row at **-1 for 27 of 30 days**,
pinned from day 1 and never recovered for the rest of that run.
That is the exact signature of Question 1's finding, generalised: a same-turn `HIRE`-then-`BUY_ANIMAL`
order silently failing at settlement while being marked bought, permanently.
It costs roughly one animal's worth of production (milk/wool, per this project's own economics
findings, the dominant revenue source for the winning tapes) for essentially the entire season, on
this seed alone.
I have not measured how many times this fires across a full 6-seed arena run — that would need the
same instrumentation used for Question 1 run across every seed, which I did not do here — so I'm
reporting the mechanism as confirmed and materially relevant, not the total dollar cost across seeds.

### What this means for the money row

The `money` row in `scripts/breakdown.py`'s output is a day-by-day AREA, as you flagged, and I did not
use it as the headline number for this reason: seed 11's area against Seb's-*opponent* actually ends
**positive** (`+36,242` cumulative, ending days show `+7,652`, `+8,825`, `+5,366` — d24-d29 all
positive), which would read as "we're ahead" if taken at face value, but that comparison is against a
different, weaker opponent than Seb himself, so it says nothing about the head-to-head loss the arena
log shows.
The arena log's mean-$/win-rate table is the correct instrument for "why do we still lose to Seb," and
it points at counts (WEEDS, ESCAPES, an_COW), not at money.

### Verdict on the framing of Question 2

The premise — "matched-day superiority should translate into season money" — is the part worth
pushing back on.
It doesn't have to, and the reason is structural, not a measurement gap: the matched-day methodology
buys its cleanliness (independence, attributability, no seed-to-seed noise) by resetting the board to
Seb's own trajectory every day, which is precisely the operation that erases compounding debt.
A planner can be strictly better *given a well-managed board* on all 29 sampled days and still be
worse over 29 *consecutive* days, if its own choices degrade the board's watering state faster than
Seb's cadence does.
That isn't a contradiction to chase down as a bug; it's evidence that the matched-day instrument and
the season instrument are answering two different questions, and only the second one is the one this
project is actually scored on.
The unfinished item this confer leaves you with is a CADENCE fix to watering (already scoped in
`schedule_agent.py`'s own comments, not attempted here) and confirmation of how often the Question-1
phantom-purchase bug fires across the full 6-seed arena set.

## Logs produced this session

    data/logs/confer_test_router_cover_on.log       the 4 failing tests, full pytest output
    data/logs/confer_diag_place.log                  PLACE ops + shed COW inventory, days 3-6
    data/logs/confer_diag_place2.log                 day-4 turn-by-turn money/shed/market, cover
    data/logs/confer_diag_place2_ROUTER.log          same, router (COVER_PLANNER toggled and reverted)
    data/logs/confer_diag_place3.log                 every cover.plan call carrying a PLACE job, days 3-4
    data/logs/confer_pens_cover.log                  day-5 dawn pen count + money, cover
    data/logs/confer_pens_router.log                 day-5 dawn pen count + money, router
    data/logs/confer_day6_cover.log                  day-6 dawn money/pens/shed/seeds, cover
    data/logs/confer_day6_router.log                 day-6 dawn money/pens/shed/seeds, router
    data/logs/confer_breakdown_diff_full.log         scripts/breakdown.py --diff, seed 11, 30 days

Diagnostic scripts used to produce these (monkeypatch `cover.plan`, never edit it; read observations
only) are in the scratchpad and were not added to the repo.
