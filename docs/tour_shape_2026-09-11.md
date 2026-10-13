# Tour shape, 2026-09-11: reducing shed trips relative to SpaTaro's tape

## Scope

Goal: match SpaTaro's tour shape (far fewer shed deposits per day than our planner makes), not just the d7 cell gate.
Two changes were tried today, both against `kagg/search/cover.py` and `kagg/search/crew.py`.
Both were measured and reverted.
This file records both, with numbers, so the next session does not retry them blind.

**IMPORTANT — a possible loss of uncommitted work.**
At the start of this session `git status` already showed `kagg/search/cover.py` as modified (`M`) against `HEAD`, meaning the working tree held some uncommitted change before this session touched it.
No backup of that pre-session version was taken before it was edited.
Later, to compare cleanly against a known baseline, the file was overwritten with `git show HEAD:kagg/search/cover.py`.
Whatever the pre-session uncommitted diff was, it is likely gone from disk — it was never staged, so it is not recoverable from git.
**Alex: check DataSpell's Local History on `kagg/search/cover.py` (right-click the file → Local History → Show History) before doing anything else with this file.** That is the IDE's own save-on-every-edit record and the only realistic recovery path.
`kagg/search/cover.py` is confirmed byte-identical to `HEAD` right now — nothing from today's two reverted experiments remains in it.
The other files this session found already modified (`kagg/plan.py`, `kagg/search/dayplan.py`, `scripts/breakdown.py`, `scripts/build_planner_submission.py`) were never opened or edited this session and still carry whatever was in them before.

## Baseline

Measured with `.venv-sub/bin/python -u scripts/d7_all_worlds.py --days 13`, crew.py and cover.py both at clean `HEAD`.
Run twice (`data/logs/allworlds_d13_baseline.log`, `data/logs/allworlds_d13_baseline2.log`) — identical both times, confirming the planner is deterministic.

d7 cells, all 9 worlds exact through d0-d6:

    bakery 13   brunch 10   fmarket 6   icecream 9   pet_cafe 8
    pizza  12   smoothie 8  yarn 11     spataro 6
    TOTAL 83

This matches the `d7c` baseline already on record.

## Change 1 — crew-split weighted by walked cost, not job turns (`kagg/search/crew.py`)

Applied before this session started (by "the coordinator" / an earlier pass on the same task); this session's first job was to read, verify, and act on the measurement.

**What it changed:** `weight(tiles)` in `crew.cover()` went from `sum(j.turns for t in tiles for j in at[t])` (job turns only, no walk, no shed ferries) to pricing each crew's sweep through `DP.materialise`/`DP.turns` — the planner's own cost model — so `k_herd` (hands assigned to the herd) is sized on what a hand actually walks, not on job-turn totals that treat herd work as costing as much per turn as crop work despite pens sitting on shed-access tiles.

**One sentence on the mechanism:** if over-crewing the herd is why each hand ends up holding its own small parcel of fertilizer and banking it separately, giving the herd fewer, more heavily-loaded hands should cut the number of separate deposits.

**Verified live, not a no-op:** diffed against `/tmp/crew.bak-before-split`; `hw, cw = weight(herd_tiles), weight(crop_tiles, far_first=True)` feeds directly into `k_herd = max(1, min(n-1, round(n * hw / (hw+cw))))`, which sizes `herd_hands`/`crop_hands`. Confirmed on the live path.

**Measured**, d7 cells:

    world       before  after
    bakery        13      13
    brunch        10       7
    fmarket        6       6
    icecream       9      11
    pet_cafe       8       8
    pizza         12      12
    smoothie       8       8
    yarn          11      11
    spataro        6       6
    TOTAL         83      82

**Verdict: mixed null, reverted.** Net -1 across 9 worlds is noise, and it is not a clean trade: icecream regressed on a BOARD property — `animals 7/8`, `herd_cow 5/6`, `feed 7/8`, `care 7/8` all started differing where they did not before, i.e. an animal that used to be placed and fed stopped being either. `drop` and `place` — the actual deposit counts — barely moved anywhere (e.g. spataro `drop 4/1`, `place 4/1` identical before and after). **The crew-split hypothesis does not explain the excess deposits.** Reverted to `/tmp/crew.bak-before-split`, byte-identical to `HEAD`.

## Change 2 — defer a zero-cost bank to the last qualifying stop (`kagg/search/cover.py::materialise`)

**The mechanism this targets:** in `materialise`, two branches decide to bank mid-tour whenever the depot lies exactly on the hand's path (`free`, zero added walk) — one when nothing held is owed to a later job, one when something is owed but the row still wants what's spare. Because pens sit ON shed-access tiles (`_refresh_pins`), `pos` after a pen visit often already equals a depot tile, so `free` is true at nearly every subsequent pen. The branches fire on the FIRST such opportunity every time, so a herd tour visiting N pens can bank N-1 or N times instead of once.

**One sentence on what the change does and what has to be true for it to win:** peek one job ahead — `free`, `owed_ahead`-type and `contested` depend only on which item TYPES are involved, not on held quantity, so they can be evaluated for job `i+1` without actually banking at `i` — and skip banking now whenever the same opportunity would still hold at `i+1`; this wins only if the deposits are actually driven by firing-on-first-opportunity rather than by some other mechanism (e.g. one closing DROP per active hand).

**Verified live, not a no-op**, three ways:
1. Isolated repro (4 shed-adjacent pens, single hand, wheat-in/fertilizer-out): route went from two separate `PLACE:FERTILIZERx1` stops (22 turns) to one `PLACE:FERTILIZERx2` stop (21 turns) — the branch fires and consolidates exactly as designed.
2. Env-gated trace (`KAGG_TRACE_BANK=1`, temporary, removed before finalizing) on spataro's real d7 pipeline: `defer=True` observed live, ~50k times across the day's search/packing calls, with `FREE-DROP`/`BANK-REDRAW` fire counts visibly reduced.
3. A pre-existing, unrelated test failure (`tests/test_a_shed_stop_banks_the_surplus_without_dropping_the_ration.py::test_day_one_feeds_every_pen_it_owns`, kawashigi tape, d1 feed 3/4) was initially misattributed to this change; re-run against clean `HEAD` with **no** edit applied reproduced the identical failure, proving it predates this session's work entirely. Noted here so it is not re-investigated as a regression of this patch.

**Measured, d7 only** (`.venv-sub/bin/python -u scripts/d7_all_worlds.py --days 13`, two independent runs, identical both times — deterministic):

    world       before  after   place before/after   drop before/after
    bakery        13      13      6/1  ->  5/1          2/5  ->  2/5
    brunch        10      10      4/1  ->  4/1          -    ->  -
    fmarket        6       6      -    ->  -             4/0 ->  4/0
    icecream       9       9      5/2  ->  4/2          3/0  ->  3/0
    pet_cafe       8       8      6/1  ->  5/1          5/2  ->  5/2
    pizza         12      12      6/2  ->  5/2          4/1  ->  4/1
    smoothie       8       7      5/2  ->  4/2          3/0  ->  3/0
    yarn          11      11      6/2  ->  6/2          3/0  ->  3/0
    spataro        6       5      4/1  ->  3/1          4/1  ->  4/1
    TOTAL         83      81

Deposit shape: `place` fell by exactly 1 in six of nine worlds, `drop` did not move anywhere. This matches the mechanism precisely — the two branches this change touches only ever emit selective `PLACE`, never `DROP`, and consolidating them saves one `PLACE` per fired instance. `move`/`water` did not move at all in any world (the branch is genuinely zero-cost, as designed); `idle` shifted by exactly the turns saved.

**Measured, full window d7-d12** (own per-day CSV columns, `data/logs/w_<world>.csv`, excluding money-tagged fields; two clean paired 13-day runs, `/tmp/csv_baseline/` vs `/tmp/csv_defer/`):

    world       d7      d8      d9      d10     d11     d12    sum(d7-12)
    bakery      25->25  =       =       =       =       =       174->174
    brunch      22->22  =       =       =       27->29  33->34  167->170  (+3)
    fmarket     17->17  =       =       =       28->29  =       170->171  (+1)
    icecream    21->20  =       34->31  =       35->34  34->31  199->191  (-8)
    pet_cafe    20->20  36->37  28->33  36->39  33->37  35->36  188->202  (+14)
    pizza       23->23  =       =       =       =       =       199->199
    smoothie    16->16  25->24  =       =       35->37  33->37  177->182  (+5)
    yarn        24->24  =       =       =       =       =       205->205
    spataro     15->12  35->34  =       =       =       31->32  187->184  (-3)

    GRAND TOTAL d7-d12: 1666 -> 1678  (+12, worse)

**Board-property check** (never-acceptable regressions, per standing rule), `pet_cafe`:
- d9: `pens 16/16` (exact) -> `15/16` — a pen match that held before is now missing.
- d10: `pens 19/19` (exact) -> `18/16` — same, a second day.
- d8-d12: `crop_strawberry` and `crop_melon` move further from the tape every day this change is on (e.g. `crop_strawberry` d9 `5/7`->`4/7`, d10 `5/7`->`3/7`, d11 `5/7`->`3/7`, d12 `7/9`->`5/9` — a growing, one-directional gap), while d7 itself is completely unchanged for this world (`20->20`). pet_cafe gets ZERO d7 benefit and a compounding loss every day after.

**Verdict: right mechanism, wrong scope — reverted.**
This is not an implementation error: the branch is confirmed live (trace + isolated repro + the predicted `place`-only, `move`-neutral signature measured across 6/9 worlds). It is not simply a wrong hypothesis either: the targeted mechanism (fire-on-first-opportunity fragmenting one bank into several) is real and the fix does what it says on d7. But judged on the window that matters (d7-d12, per explicit instruction), it is a net loss — +12 cells — carried almost entirely by `pet_cafe`, which gets no d7 upside at all and a monotonically growing board-state regression (missing pens, undercovered crops) for five straight days after. `icecream` and `spataro` genuinely improve and hold up across the window (-8, -3), so the mechanism is real on SOME worlds; it is not safe to ship globally with a one-step lookahead, because deferring a bank changes which hand ends up carrying what into the NEXT job in ways the one-step peek does not fully account for once the real multi-hand packer (`_pack`/`_fits` in `crew.py`, which prices lanes with `wanted=None` during growth and the real `wanted` only at commit) is in the loop. Reverted; `kagg/search/cover.py` is byte-identical to `HEAD`.

## What the evidence points to next (not attempted — out of this session's remaining budget)

Per-world deposit counts at d7 (DROP+PLACE, ours/his), before either change:

    bakery 7/6   brunch 7/4   fmarket 4/0   icecream 7/2   pet_cafe 10/3
    pizza 9/3    smoothie 7/2   yarn 9/2   spataro 7/2

The excess is overwhelmingly `place` (ours 3-6, his 1-2, every world over) rather than `drop` (ours 2-5, his 0-5 — bakery is actually BELOW him, 2 vs 5). `fmarket` is the clean counter-case: `place 0/0` (never fires) but `drop 4/0` — four real DROPs where he makes none, with the selective-PLACE path never in play at all, so on that world the excess cannot be a PLACE-vs-DROP choice problem; it has to be about WHEN/WHETHER a DROP fires.

Two things worth checking directly, not yet done:
1. **Is `_bank()` (cover.py:397) choosing PLACE where he'd make one whole DROP?** It picks selective PLACE whenever it prices cheaper than DROP+redraw, which on a small load it almost always will — meaning small, frequent selective placements may be individually "optimal" while his tape prefers one bigger DROP. Print, for one world's d7, whether each deposit lands as DROP or PLACE, the item, the quantity, and which branch inserted it (`_bank` call site) — direct evidence, not inferred from op counts.
2. **On `fmarket`, why 4 DROPs against his 0** with the selective path never touched — check whether that is one DROP per active hand's closing trip (rule 3, the `deliver`-gated route-end drop), which would mean the deposit-count problem has at least two independent causes: fragmented mid-tour PLACE (worlds with `place` excess) and one-closing-drop-per-hand (worlds with `drop` excess, independent of crew size — already shown not to respond to `k_herd`).

## Summary table

    world       baseline  crew-split  bank-defer
    bakery         13        13          13
    brunch         10         7          10
    fmarket         6         6           6
    icecream        9        11           9
    pet_cafe        8         8           8
    pizza          12        12          12
    smoothie        8         8           7
    yarn           11        11          11
    spataro         6         6           5
    TOTAL          83        82          81

Both changes reduce the TOTAL by one or two cells. Neither is a clean win once checked against board properties and the wider day window, and both were reverted. `kagg/search/crew.py` and `kagg/search/cover.py` are byte-identical to `HEAD` at the end of this session.

## d0-d6

Exact on all 9 worlds throughout — baseline, crew-split, and bank-defer. Never at risk in any of the three states measured.
