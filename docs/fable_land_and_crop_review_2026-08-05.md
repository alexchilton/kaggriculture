# Review: land timing, strawberry, sheep — 2026-08-05

Scope: `kagg/search/routines.py`, `kagg/search/chains.py`, `scripts/beam_chains.py`,
`kagg/economics/production.py`, plus the five named logs, plus whatever else the trail led to.
Review only — no code was edited.

## Read this first: the codebase moved under me

This is a git repo (`git status` works even though the environment banner says otherwise) and it is
mid-edit. Between the start of this review and now, three of the four "ALSO ASSESS" defects named in
the brief were fixed **in the uncommitted working tree**, with new tests, and I watched the test suite
go from 2 red / 3 red to green while reading:

- `kagg/search/chains.py` gained `working_units()` (skips the two dead SE-spawn slots per 8),
  `reachable_quadrants()` (skips a chain aimed at land it cannot afford, instead of letting it silently
  relocate), and a `fert_trade` gene (makes ranch-sells-vs-grow-buys-fertilizer a per-chain choice
  instead of a hardcoded collision).
- `kagg/search/routines.py` now spaces land orders one parcel per day instead of three in three
  consecutive turns of the same day (`tests/test_land_orders_are_spaced.py`, all green).
- `tests/test_locked_chain_relocates.py` went from 2 failing / 3 passing to **6/6 passing** — it
  gained a sixth test, `test_ground_bought_out_of_revenue_is_still_allowed`, which pins the claim
  that waiting for a late parcel is worth **up to +$22,911** and must not be refused just because the
  opening bank alone couldn't cover it.
- `git log` shows the last two commits are "Search over chain instances instead of over turns" and
  "Stop the seeded genome going bankrupt on day one" (Aug 4, 20:57 and 21:15); everything above is
  *further* uncommitted work on top of those, timestamped essentially "now."

**Practical consequence:** `data/logs/arena_gate.log` (the "4 melon + 4 cow, no straw, no sheep, 1.000
win rate" result) was generated *before* `working_units()` and `reachable_quadrants()` landed, using
the genome saved in `data/chain_search_s8/best_beam_genome.npz` — which I confirmed by loading it is
literally the $64,146 genome that `test_locked_chain_relocates.py` uses as its worked example, i.e. the
one where three of four ranch chains silently relocated. **The "no strawberry / no sheep" result you're
asking me to explain was partly produced by a search that didn't know two of its eight slots were dead
and that three of its ranch tiles didn't exist where it thought they did.** I re-ran the beam search
against the current, fixed code (`data/logs/fable_review_beam_rerun_2026-08-05.log`, started during
this review, background PID 58156) to see whether the mix changes; see the Appendix for however far it
got.

None of this makes the three suspicions moot — the structural argument below (slot budget vs. leader
scale) is independent of these particular bugs and I'd expect it to survive a re-run. But cite the
$64,146/arena_gate.log numbers as **pre-fix**, not current.

## Ranked findings

1. **(A) Land-day-0 conclusion is confounded, and the fix for the confound is already landing.**
   High confidence, high impact. See below.
2. **(B)/(C) unified: an 8-slot, 4-tile-block genome cannot reach the leader's scale, so it can never
   observe the regime where strawberry/sheep pay.** High confidence, high impact, and it is a search
   design ceiling, not a bug in `grow()`/`ranch()` — the crop and ranch chains are not defective.
3. **Ranch-sells / grow-buys fertilizer self-trade** — real, measured, and already turned into a search
   choice (`fert_trade` gene) rather than a hardcoded default. Medium impact, already actioned.
4. **Dead SE-spawn slots (units 3, 7)** — real, now fixed (`working_units()`). Medium impact per slot,
   already actioned.
5. **Locked-tile chain relocation** — real, now fixed (`reachable_quadrants()`). High mechanism-level
   importance (it explains why several earlier measurements, including the land-timing ones, were
   unreliable), already actioned.
6. **Sell cadence hardcoded to daily** — real but small, unmeasured directly; lower priority.

---

## (A) "Buying land on day 0 is wrong"

**Verdict: the user's instinct is right, and the reason our own measurement said otherwise is now
identified and partly fixed.**

### What the leader actually does (verified directly from the tape)

I loaded `data/seed_scripts/replay_89873723_seat0.npz` myself rather than trusting the docstring quote:

```
buy_land turns: [169 260] -> days: [7, 10]
buy_animal (GOOSE, COW, SHEEP) totals: [0, 8, 6]
buy_seed (WHEAT, CARROT, TOMATO, STRAWBERRY, MELON) totals: [66, 0, 0, 44, 21]
hire per day (sampled every 24 turns): 2,2,2,2,2,2,2,2,3,3,...,3,3,10,10,...
```

Confirmed exactly: land on day 7 and day 10, never a third parcel; 8 cows + 6 sheep; crew held at
**2-3 hands for the first 25 days** and only jumps to 10 in the last few days. This crew-ramp shape is
the same one documented independently in `tests/test_herd_ramp.py` / `data/logs/diverge_by_day.log`
for a *different* leader episode (89113699, the $132,245 seat): crew held at 2 animals for 11 days,
then jumps to a much higher level once land and cash both arrive.

### Why `cash_gates_the_herd.log` says day 0 wins, and why that's not the right comparison

`cash_gates_the_herd.log`'s "HERD SIZE x LAND TIMING" table sweeps a single `day` parameter and shows
1-cow and 2-cow herds monotonically getting *worse* as `day` increases (0 → 4 → 7 → 10 → 14). But
1 and 2 cows sit on shed cells that **cost $0 of land** — there is nothing to "time" about land for
them. The only thing that can be getting delayed by that "day" parameter is the **start day of the
whole ranch chain itself** (`ranch()`'s `start_day`, coupled to `land_day` in whatever ad hoc script
produced this log — the script itself no longer exists in the repo, so I can't inspect it directly,
only its output). That is a materially different question from "when do you buy land": delaying
*when an already-affordable animal starts producing* is obviously bad, and has nothing to do with the
leader's actual move, which is to keep the herd small and cheap early while *land* purchases wait for
revenue. The table's 3-cow/4-cow rows make the same point from the other side: every single cell is
`$0, !0` except day 14 in the melon-funded table — a "pens only" farm (no crop income at all) can never
afford the second/third land parcel *no matter which day you ask*, because there's no revenue to fund
it with. That's not evidence land timing doesn't matter; it's evidence this table cannot express the
leader's actual strategy (cheap animals now, land later, funded by crops) because it only has one knob
where two are needed.

**What would confirm this:** re-run a version of that sweep with `land_day` and `start_day` varied
*independently* for the 3-4 cow cases, holding melon/wheat income fixed. I did not have the generating
script to do this without writing new code, which would exceed "review only" — flagging it as the
concrete next measurement.

### `land_timing.log`'s "day 0 was right after all" is the more serious case, and I think it's an artifact

This one *does* test the real genome (`data/chain_search_s8` era, 8 slots), and it does vary
`land_day` while holding the rest of the genome fixed, converging back to day 0 every time
(`$50,916` at day 0 vs `$44,885` at day 4, `$44,483` at day 8, etc. — monotonically worse with delay).
But the genome under test there is drawn from the **same pre-fix search** whose ranch chains at SE/SW
cells silently relocated to whatever land was already affordable (confirmed above: the identical tile
list `(1,1)/(7,8)/(2,8)/(6,9)` appears in both `land_timing.log`'s "slots standing on bought land"
and `test_locked_chain_relocates.py`'s worked example of relocation). If "land day 0" in that genome
never actually meant "SE is unlocked by day 0" — because $7,000 against a $3,000 bank silently buys
only the first $1,000-$2,000 of it and the pen walks to wherever that gets it — then the sweep never
tested "genuinely wait for SE," only "how good is the accidental near-border farm this collapses to,"
at various values of a parameter that mostly doesn't do what its name says. **`reachable_quadrants()`
in the current `chains.py` (line ~191) is a direct, already-written answer to this**: it now refuses to
credit a chain with land it cannot afford on the day it orders it, *and* it explicitly allows land
bought later out of revenue rather than the opening bank (the `EARLIEST_REVENUE_DAY = 3` cutoff), with
the comment recording "waiting is worth up to +$22,911" for exactly this reason. I could not find
`data/logs/land_day7.log`, the log that number is attributed to, anywhere on disk — either deleted
after use or never written to that path — so I can't independently re-derive the $22,911 figure
myself, but the mechanism it's attached to (`reachable_quadrants`) is real, tested, and currently green
(`tests/test_locked_chain_relocates.py::test_ground_bought_out_of_revenue_is_still_allowed` passes).

**Bottom line on A:** day-0 land is not "provably right" — it's the answer a search gave while (a) two
of its measurement scripts conflated land timing with chain start timing, and (b) its own genome
decoder was silently rewriting "buy SE" into "build wherever the walk to SE stops." Both are now
understood, and (b) is fixed in the working tree. I'd expect a fresh beam search on current code to
push land later than day 0 for at least the second and third parcels; whether it reaches the leader's
exact day-7/day-10 is an open question the Appendix re-run is trying to answer.

---

## (B) "No strawberry is a bug"

**Verdict: `grow()`'s strawberry chain is not defective. The search cannot reach the tile-count regime
where strawberry would win, because of a self-imposed 8-slot / 4-tile-block ceiling — and that ceiling
is the same one that also explains (C).**

### The chain itself is fine

- `CROP_TABLE["STRAWBERRY"]` (`routines.py:392`) correctly marks it `ongoing: True`, and `grow()`
  correctly harvests ongoing crops "every eligible day" rather than waiting for one big harvest
  (`routines.py:564-565`), which is what the CLAUDE.md-pinned once-per-lifetime rule requires.
  `kagg/economics/production.py`'s pinned, live-measured numbers (6 units/tile plain, 12 fertilized)
  match the numbers quoted in the task brief exactly, and `does_fert_pay.log` reproduces them
  end-to-end through the real chain (`STRAWBERRY $6,182` alone, `$5,762` fertilized — fertilizer is a
  net loss here at market price, see the fertilizer section below, but the chain is doing real work,
  not producing zeros).
- Sell cadence is correctly deferred to next-dawn for a remote block (`routines.py:495-501`,
  `test_a_crop_routine_pays_for_itself` in the docstring's citation) — same-day selling on an
  off-shed block is the one thing documented to bank exactly zero, and `grow()` already avoids it.

### Where strawberry actually loses: the reachable-scale measurement is capacity-bound, not price-bound

`scale_melon_vs_straw.log` sweeps 0-6 blocks (0-24 tiles) of a single crop, all inside NW (the only
quadrant with zero land cost), alongside two shed cows. Melon's marginal per block stays positive
through block 4 (16 tiles: `+$4,637`) and turns negative at block 5 (`-$1,516`) — consistent with its
140-unit town-drain ceiling (140/12 ≈ 11.7 tiles, close to the observed block-3→4 knee). Strawberry's
marginal is already **negative by block 4** (`-$224`) — far short of its own 572-unit drain ceiling
(572/6 ≈ 95 tiles unfertilized, or ≈48 fertilized). The measured collapse point (16 tiles) is nowhere
near the theoretical one (48-95 tiles): **this test cannot even ask the question it needs to**, because
NW only has 6 blocks (24 tiles) total, shared with everything else on the farm. The leader's 40
strawberry tiles alone would already exceed the entire NW quadrant's tile budget.

The genome-level version of the same ceiling: an 8-slot genome with `BLOCK_SIZE = 4` can field at most
8 crop blocks (32 tiles) if every slot is a crop and none is an animal — and the leader's real
allocation needs roughly 10 blocks of strawberry (40 tiles) *plus* 11 melon (≈3 blocks) *plus* 14
ranch pens, i.e. on the order of 13+ crop-slots and 14 ranch-slots, far past 8 total. `melon_sweep.log`
shows the same signature from the crop side: melon's own marginal per block goes to zero by block 3
(`$27,915` at 3 blocks, unchanged at 4/5/6 blocks — "melon inv" flatlines at ~9,949 units of unsold
inventory, meaning the book stops clearing and extra blocks are pure waste). **Given only 8 slots, and
melon dominating strawberry roughly 4:1 per tile up to melon's own saturation point (`crop_pays.log`'s
`+$3,182` vs `+$803`, cited in `chains.py`'s own docstring), a beam search maximizing money per slot has
no reason to ever prefer strawberry until melon and the best animals are already spoken for — and 8
slots isn't enough to get there.** This is exactly what `arena_gate.log`'s genome shows: 4 melon blocks
(right at melon's own saturation point) + 4 cows, 0 slots left over.

**What would confirm this further:** the diminishing-marginal numbers already in hand suggest that a
5th/6th melon block (`-$1,516`, `-$1,490`) or a 3rd/4th cow (`does_fert_pay.log`: 3 cows `$21,034` vs 2
cows `$22,655`, i.e. -$1,621 marginal) should already be *worse* than a strawberry block's marginal at
that point (~+$3,000-3,100 per the block-2/block-3 deltas). If a fresh, fixed-code beam search still
fills slots 5-8 with more melon/cow instead of strawberry, that would be a real remaining defect in the
beam's diversity handling (or in how it explores mixed portfolios) rather than a capacity story, and
would be worth a direct one-slot swap test (`with_slot` a beam-found genome's slot 7 from `cow` to
`strawberry`, compare money). I did not have time to run that specific swap before this document was
due; see the Appendix for the live re-run, which is the closest available evidence.

### A secondary note, not chased to ground

`scale_melon_vs_straw.log`'s "STRAW+fert" column is **byte-identical to the plain "STRAWBERRY" column
at every single block count (1 through 6)** — `26,028 / 29,214 / 32,328 / 32,104 / 31,173 / 30,833`,
twice. `does_fert_pay.log`, run ten minutes earlier the same evening, shows fertilizing strawberry
*does* change the outcome (if only negatively: `$6,182` plain vs `$5,762` fertilized). Two measurements
of the same crop, same evening, disagreeing about whether `fertilize=True` does anything at all, is
exactly the kind of discrepancy this project's own rules say to chase with a test before trusting
either number. I did not find the script that produced `scale_melon_vs_straw.log` (see the note below),
so I can't tell whether this is a real interaction with the "two cows on the shed" setup (e.g. the
crop-unit's turn budget going over 24 with fertilizer's extra PICKUP detour, silently dropping the
fertilize option per `grow()`'s own fallback at `routines.py:610-614`) or a copy-paste artifact in
whatever printed the table. Flagging it; not folding it into the verdict above.

---

## (C) "No sheep is a bug"

**Verdict: partially wrong as stated, for reasons independent of (B)'s capacity story — but the capacity
story still applies and is probably the dominant effect.**

`does_fert_pay.log`'s own numbers, measured in the real chain, are a clean, direct rebuttal of "sheep
must be a search bug" at small scale:

```
ranch COW (4,4)   $13,673  (+10,673 over empty)
ranch SHEEP (4,4) $12,245  (+9,245 over empty)      <- cow beats sheep, alone
1 x COW   $13,673   2 x COW   $22,655   3 x COW   $21,034   4 x COW   $19,343
1 x SHEEP $12,245   2 x SHEEP $20,102   3 x SHEEP $18,381   4 x SHEEP $ 7,030
```

Cow beats sheep at **every single herd size measured, 1 through 4**, and the gap widens sharply at 4
(sheep collapses to $7,030, a steeper fall than cow's). At the scale our 8-slot genome can reach (at
most 4 ranch cells before running into unowned land), sheep is never the better animal by this
measurement, so a search correctly avoiding it there is not a bug — it's the right call for the regime
it can see.

The reason the *leader* still runs 6 sheep alongside 8 cows is almost certainly the same capacity
ceiling as (B): with only 4 ranch cells reachable inside our genome (the leader uses ~14 pens), we have
never measured what happens to the 9th-14th animal's marginal value once milk itself is saturating —
which is exactly the regime where diversifying into wool would start to pay, the same way strawberry
only starts to pay once melon (and, per this section, cows) have saturated. `does_fert_pay.log`'s own
"2 x COW" number already shows the *3rd* cow going marginal-negative on a shed cell (`$21,034` vs
`$22,655`) — we're already seeing milk saturate at n=3 on a single shared board, well before the leader's
scale of 8. I'd expect that if we could genuinely field 8 cows, the marginal 9th-14th animal would flip
to sheep being the better buy, exactly mirroring the melon→strawberry story. This is inference from the
saturation pattern already measured, not a new measurement — flagging it as such.

**What would confirm this:** the same swap-test recipe as (B) — take a genome with 4+ cows already
placed (once the herd cap of 4 is lifted enough to test it, which needs either more ranch tiles off-shed
or more slots) and check whether SHEEP beats COW for the marginal pen. Currently blocked by the same
4-ranch-cell / 8-slot ceiling.

---

## The "ALSO ASSESS" items

### Ranch sells fertilizer / grow buys fertilizer — same farm trading with itself

Real, measured, and it is the thing `fert_trade` (the new 7th gene) exists to fix. The old code path:
`ranch(collect_fertilizer=True, sell_fertilizer=True)` by default (`routines.py:186-187`) sold every
unit a fed animal produced, same day; `grow(fertilize=True, buy_fertilizer=True)` by default bought
fertilizer from the market for any crop chain wanting it — on a farm running both, the pen's free output
was sold into the same market the crop unit then bought back from, "paying the spread twice"
(`routines.py:355-362`, `chains.py:172-179`). `chains.py`'s new comment states "selling beat applying
about 6:1" as the one measurement behind making it a per-chain choice rather than a fixed default,
explicitly flagged there as "one 4-tile block with two cows... exactly the kind of narrow measurement
this project has been burned by" — i.e., the author of that comment already holds the same doubt the
task brief does, and has deliberately handed the choice to the search rather than hard-coding either
answer. I could not reproduce a clean 6:1 ratio from the two logs I have (`does_fert_pay.log`'s closest
comparable pair, `1 cow(s) SELL fert, plain crop $16,825` vs `1 cow(s) FEED crop, no sale $14,604`, is
about 1.15:1, not 6:1) — but that log predates the `fert_trade` gene and may not be measuring the same
comparison the 6:1 figure refers to. The application path is not "broken" in the sense of no-opping —
`test_fertilizer_is_actually_sourced.py` (all green) confirms FERTILIZE ops now really do get sourced
fertilizer and really do change the season's money — it's a genuine economic trade-off, now correctly
exposed as one, rather than a bug. Whether selling really does beat applying 6:1 in general (vs. 1.15:1
in the one comparable case I could check) is exactly the kind of claim this project's own testing
discipline says needs a dedicated test before being trusted either way.

### Sell cadence hardcoded to daily

Confirmed as described: both `ranch()` and `grow()` emit a sell order every day something is harvested,
with no spacing parameter. The leader's own tape does space its higher-value sells — I measured this
directly from `replay_89873723_seat0.npz`: STRAWBERRY sells on 16 of 30 days, MELON on 15 of 26
available days (with gaps up to 6 days), while WHEAT and FERTILIZER sell on 28-29 of 29 days each. So
the leader visibly throttles premium-good sales and dumps the cheap byproducts constantly. Whether this
costs us anything is genuinely unmeasured here — I found no log that isolates cadence from mix, and
since `grow()` only harvests-and-sells an ongoing crop once it's mature and the amounts per day are
already small (`max_yield` per event, not a season's backlog), the naive daily cadence may already
behave similarly to batching in its effect on the shared inventory curve. Lower priority than A/B/C;
flagging rather than asserting a cost.

### Units 3 and 7 dead on arrival (SE spawn, locked)

Confirmed exactly as described, and now fixed. `routines.py:83-105`'s `spawn_order`/`spawn_tile`
already documented that unit 3 (and 7, 11, ...) spawn on `(5,5)`, whose only neighbours `(4,5)`/`(5,4)`
are themselves locked until SE is bought — `ops.py:83-86` silently drops a move onto locked ground, so
that unit cannot leave its spawn tile all season under any plan the search has found. `chains.py`'s new
`working_units()` remaps slot→unit to skip these (`[0,1,2,4,5,6,8,9]` for 8 slots), with
`tests/test_slots_skip_dead_units.py` (5/5 green) pinning both the mechanism and the measured recovery
(unit 3's melon-block value went from $1,920 to within 85% of unit 2's $15,515 once given a working
unit index).

### Locked-tile relocation (chain aimed at unaffordable land silently rebuilds elsewhere)

Confirmed exactly as described, and now fixed. This was the single most consequential bug of the four:
because `ops.py` doesn't error on a blocked move, a chain ordering land it can't afford doesn't fail —
it silently walks to the border and builds there, so the genome's own printed description
(`used = [("ranch", "COW", (7,8), ...), ...]`) was **fiction** for exactly the genome
(`data/chain_search_s8/best_beam_genome.npz`, $64,146) currently sitting in `arena_gate.log` and
`land_timing.log`. `chains.py`'s new `reachable_quadrants()` computes what land a genome can really
afford given when it orders it, and `decode()` now skips (and counts as `skipped`) any chain whose
target tile needs land beyond that, rather than emitting a chain that will silently teleport.
`tests/test_locked_chain_relocates.py` is 6/6 green as of this review (it was 2 failing when I started
reading it 90 minutes ago). This bug is the reason I'm treating both `land_timing.log`'s and (to a
lesser extent) `cash_gates_the_herd.log`'s "day 0 is optimal" conclusions as unreliable rather than
settled — they were measured through this exact silent-relocation path.

---

## Appendix: live re-run status

Started during this review (background, PID 58156 then continued as background task `byxjz7mj2`):

    PYTHONPATH=. python3 -u scripts/beam_chains.py --beam 4 --refine 1 --boards 2 \
        --opponents heuristic,rancher
    log: data/logs/fable_review_beam_rerun_2026-08-05.log

This uses the *current*, fixed `chains.py`/`routines.py` (working units, land-affordability skipping,
`fert_trade`), unlike every number quoted above from the pre-existing logs. Partial output as of writing:

    slot 0 |   481 evaluated | best 0/4 $ 14,794 | ('grow', 'MELON', block, day 2)
    slot 1 |  1924 evaluated | best 2/4 $ 25,300 | ('grow', 'MELON', block, day 2)
    slot 2 |  1924 evaluated | best 4/4 $ 35,759 | ('grow', 'MELON', block, day 2)   (224s elapsed)

Melon is still the first three picks, consistent with the capacity argument above (melon dominates
until its own saturation point, which later slots haven't reached yet this early). At ~100s/slot the
remaining five slots plus the refine pass will take on the order of 10-15 more minutes, past this
review's window. Whether slots 5-8 turn to strawberry/sheep, and whether the refine pass pushes any
`land_day` later than 0, is not yet known — reduced `--boards 2` and only two opponents to make the
run finish faster, so treat this as a smoke test, not a competitive number (the script's own closing
message says as much). **The run is still going in the background (log path above); check it directly
for the finished result rather than re-running from scratch.**
