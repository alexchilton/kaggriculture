# Kill criteria and settled positions — the full record

Moved out of `CLAUDE.md` on 2026-08-15. Every kill criterion below is either MET or CLOSED, and
the settled positions are all about the RL track, which is parked. `CLAUDE.md` now carries the
three sentences that still bind; this file is the evidence behind them.

Do not delete it. The reward-shape bullets exist to stop a future session restoring per-step
rewards from `docs/rl_feasibility.md`, which still argues for them at length.

---

## Kill criteria — committed up front

These were agreed before any code was written, specifically so they cannot be rationalised away later.

- Heuristic agent does not clear **$20k** final bank → the economics model is wrong, not the agent.
- **The simulator now models the whole game: all 18 unit ops and all 6 market orders.**
  It modelled 9 and 4 of them until 2026-08-01, and the missing half was the animal economy --
  which is what actually wins games. Episode 89197802, the top two agents playing each other,
  banked $106k and $113k against our `contrarian`'s ~$38k; the winner drew ~83% of its revenue from
  milk and wool by converting bought wheat into animal products, and the runner-up traded wheat
  with `BUY_PRODUCT`. Neither play was expressible, so anything trained then could only have become
  a very good crop farmer.

  **Parity does not imply coverage, and that is how this hid.** `parity.py` built its scripts from
  `SCRIPT_OPS`, which listed only the ops the simulator already had, so the gate could not emit
  `FEED` and therefore could not fail on `FEED`. "300/300 exact" was a true statement about a
  subset. When adding an op, add it to `SCRIPT_OPS` and to `_dense_actions` in `tests/test_jax_sim.py`
  in the same commit, or it is untested by construction.

- Fast-sim parity harness is not exact over 1000 random action sequences → **do not train on the fast sim**.
  **Status 2026-07-31 (evening): PASSING. 300/300 full-length episodes exact**, across five
  configurations from a single unit up to twelve-unit crews with land buying. The JAX sim matches
  the numpy sim field for field, 16/16.

  The route there is worth remembering, because the harness was wrong twice in opposite directions:

  - It first hard-coded `n_units = 1`, so "60/60 exact" was a claim about single-unit games read as
    a claim about the simulator. **Atomic PLANT** and **hand spawning** hid behind it.
  - Widened to six unit slots, it then drove six unit *actions* whether or not the farm owned six
    units. The reference ignores a surplus action for movement and work but still counts it in the
    atomic PLANT rule, so it blocked plants no agent could ever block. That, not a simulator bug,
    is what "8/12 under hiring" was. Agents submit one action per unit owned; the harness now does
    too. Hiring was never involved -- the same failure reproduced at 1/8 with hiring switched off.

  **Update 2026-08-01: order slotting is fixed too.** It had been left alone as unreachable -- every
  pairing of `contrarian`/`heuristic`/`rancher` gave $0 of error, because agents emit sells in a
  canonical product order. Adding `BUY_PRODUCT` made it reachable on ordinary turns, since a buy
  quotes at `inventory - 1` against a book the sells have already lifted. `Game._order_book` now
  compacts a turn's orders into ten slots and `_process_market` walks them in lockstep, verified by
  a 400-turn randomised differential test of the market phase alone against `kg._process_market`.

  Two divergences remain deliberate, both RNG-stream artifacts neutralised in the gate: the weed
  spawn sequence and the shop unlock order.
- PPO explained variance does not pass **0.5** early → the frame is wrong, not the hyperparameters.
  **Scope note:** this was written for the per-turn, 720-step, full-action-space policy. The
  strategy env clears 0.89 easily, but it is a 30-step problem with 9 discrete heads and hand-built
  features -- a far easier target. Clearing it there is *not* evidence the hard frame works.

## Things that are settled — do not relitigate without evidence

- **SUPERSEDED 2026-07-31 for the strategy env — read this before the bullet below.**
  `kagg/rl/env.py` makes one decision per *day*, so episodes are 30 steps, not 720. At that
  length the credit-assignment argument for per-step decomposition no longer applies, and the
  true objective is available directly: the ladder is an Elo rating, so **terminal win/loss
  (+1/-1/0) with gamma 1.0 is what `scripts/train_rl.py` actually trains on.**
  Money is logged but never rewarded.
- **SUPERSEDED 2026-08-01 for the per-turn policy too — Alex's call, made explicitly.**
  **The reward is terminal: win 1, loss 0, gamma 1.0. Never per step.** This now applies to
  *every* policy in the project, so the per-step bullet below no longer governs anything and is
  kept only so a future session does not "restore" it from `docs/rl_feasibility.md`.

  It is also what the evidence says. Of the top finishers whose write-ups we have, four used a
  terminal signal — Felix Neumann terminal -1/+1, simjeg terminal with gamma 0.995, Isaiah Pressman
  terminal, Billy Bradley's `ender` positive-only 0/1/2 with gamma 0.998 — and none used a
  per-step bank delta. The ladder is an Elo rating, so margin does not count, and a $43k win and a
  $4k win are the same result.

  If credit assignment over 720 steps stalls, the agreed next move is a **per-game-day** signal,
  not a per-step one, and only after `explained_variance` has been checked first.
- **~~Per-step bank delta is the reward, with gamma ≈ 1.0.~~ NO LONGER IN FORCE.** Superseded by
  the bullet above for every policy. Left in place because `docs/rl_feasibility.md` still argues
  for it at length, and a future session reading that doc alone would otherwise reintroduce it.
  The argument there is not wrong about credit assignment; it was simply overruled.
- **Legality masking is fine and expected.** MaskablePPO is the intended trainer.
  The Orbit Wars warning was about masking no-op to *force* action, which is a quality judgment.
  Masking illegal ops is a legality fact and is explicitly blessed by our own post-mortem.
- **Ongoing crops yield `max_yield` once per lifetime, not per day.** Tomato is 8 units per tile
  per *season*, strawberry 6 — not 4.0 and 2.0 per day as the Object Types table reads.
  Animals are the reverse: no lifetime cap, so a goose gives 26 eggs a season against
  `max_held` of 4.
  Pinned by `tests/test_production.py`. Do not re-derive these from the published tables;
  the tables are misleading and cost this project a day-1 wrong turn.
- **A heuristic agent is a teacher and a sparring partner, never the final policy.**
  This is the correction to the Orbit Wars failure where heuristics became the policy and capped the ceiling.

---

## 2026-08-15 — Documentation staleness audit

Folded in from docs/stale_audit_2026-08-15.md.

Read-only audit, no code touched.
Method: read the current file content from the live checkout at
`/Users/alexchilton/DataspellProjects/kaggriculture` (the audit's own worktree was pinned at an old
commit, `7a3535e`, and could not see any file created or edited after 2026-08-03 — see the
limitation note at the end of this section), then dated every claim with
`git log --all -S"<string>" --format="%h %ad %s" --date=short`, run from that worktree without
touching the shared checkout's working tree (git object access only).

**Status update, added at fold-in time:** `docs/REGISTER.md:1-10` (this worktree, checked
2026-08-20) now carries a "Repaired 2026-08-15" banner confirming finding 1a below and describing
the fix.
Findings 1b through 1f are left as the audit recorded them — this fold-in did not re-verify them.

### 1. Confirmed stale — ranked most dangerous first

**1a. `docs/REGISTER.md` was reverted and corrupted — the mandatory "check before opening
anything" doc was missing a whole day's edits.**

`docs/REGISTER.md:1-3` read (at audit time):

```
is cl# Register — what is open, what is closed, and what keeps reopening

Last updated 2026-08-08, on `shaping-potential`.
```

Line 1 was garbled (`is cl#` in front of the title — a splice artifact, the same failure class
`CLAUDE.md` already warns about: *"a hand-rolled `submission/main.py` spliced a docstring over
line 1, failed to import"*).
The date stamp was wrong by five days on a file that names its own freshness as load-bearing.

Dated evidence it should not have read this way:

- `bbc2a31` (2026-08-13, "Restamp REGISTER.md's last-updated date after today's pass") explicitly
  changed the line to `Last updated 2026-08-13, on \`shaping-potential\`.`
- `e4e0c65` (2026-08-13, "Fold README.md's index into REGISTER.md, and correct stale herd/citation
  claims") added a whole new top section, `## What is in which file`, immediately after that line,
  and rewrote every citation inside `REGISTER.md` that pointed at a file deleted in the 2026-08-13
  pass.
- Neither the 2026-08-13 date stamp nor the `## What is in which file` section was present in the
  file as it read at audit time.
  `git show 3b2a379:docs/REGISTER.md` (the most recent commit that touched the file, 2026-08-15)
  reproduced the same garbled line 1 and the same 2026-08-08 stamp — not an uncommitted local edit,
  checked in.
- Tracing parents: `3b2a379`'s parent is `c4236e9`, whose parent is `931fda6` (both 2026-08-15).
  `git log c4236e9 -- docs/REGISTER.md` stops at `513fff7` (2026-08-11) — this lineage never
  incorporated `bf43f62` / `bbc2a31` / `e4e0c65` (all 2026-08-13).
  Two branches diverged around 2026-08-11 and only one carried the 2026-08-13 register cleanup;
  the checked-out one did not.

Why this was the most dangerous item on the list: `CLAUDE.md` names `REGISTER.md` as the doc to
"check before opening anything," and its own ground rule says an item is closed only if a named
artifact backs it.
A session trusting the file at audit time was working from a version missing a full day of
citation repair, with no visible sign anything was wrong beyond the garbled first line.

**1b. `CLAUDE.md`'s own "three things still bind" section was contradicted by `CLAUDE.md`'s own
Kaggle section, written the same day.**

`CLAUDE.md:168` (at audit time):

> **Fast-sim parity PASSES** -- 300/300 full-length episodes exact, all 18 unit ops and 6 market
> orders.

No version qualifier. Presented as one of the three things that still bind, unconditionally.

`CLAUDE.md:187-194` (Kaggle section, added the same day):

> `kaggle-environments >= 1.32.7` is required (2026-08-15 balance change, PR #1399) ... `kagg/sim/
> market.py` died on `KeyError: 'hinge'` and `kagg/sim/jax_sim.py` would have priced all three at
> flat base **in silence**.

Dated evidence the parity claim had already gone stale on this exact pattern once:

- `git log -S"Fast-sim parity PASSES" CLAUDE.md` → `d56d1be`, 2026-08-15 (the commit that moved
  this text out of the old "Kill criteria" section, unchanged in substance since 2026-07-31).
- `git log -S"KeyError: 'hinge'" CLAUDE.md` → `2e548e8`, 2026-08-15 — same day.
- `docs/architecture.md:254`: **"2026-08-09: both simulators FAIL parity on the installed 1.32.6
  env — 8 failures, not just the JAX one."**
- `docs/REGISTER.md:275`: `Sim | parity exact... | passing on 1.32.2 (300/300); failing on 1.32.6,
  8 failures, unfixed as of 2026-08-09`.
- Parity for 1.32.6 was later restored the same day (`docs/parity_restored_on_1326_2026-08-09.md`),
  so the claim did become true again — but only after an unqualified copy of it had already been
  wrong for part of a day.

What could not be confirmed either way at audit time: whether the 300/300 full-episode fast-sim
gate had been re-run and passed since the 1.32.7 `hinge` fix landed in `kagg/sim/market.py` and
`kagg/sim/jax_sim.py` (both files did have a `hinge` branch by then — code-level, fixed).
No doc or log named a fresh full-suite run.
Treat the truth value of "parity passes" as **unverified** at that time, separate from the
confirmed finding above, which is that the claim in `CLAUDE.md` carried no version caveat and had
already been silently wrong once on an identical version bump.

**1c. `docs/competition_brief.md` — read-first item #1 — had no mention of the 1.32.7 balance
change and told a reader to install a version two behind current.**

`docs/competition_brief.md:248`: `pip install -U "kaggle-environments>=1.32.2"    # earlier
versions lack the env`.
Zero occurrences of `hinge` or `1.32.7` anywhere in the file (grepped).

`CLAUDE.md:187`: **`kaggle-environments >= 1.32.7` is required** (2026-08-15 balance change, PR
#1399) ... "Any baseline measured before 2026-08-15 describes a different game."

A session reading the docs in `CLAUDE.md`'s own prescribed order (`README.md` → `competition_brief.
md` → ...) hit the install instruction before the correction.
Installing 1.32.2 per this doc silently mis-prices CARROT, TOMATO and EGG (the `hinge` shape).

**1d. `REGISTER.md`'s own "the only metric that counts" command named a retired tape and could
not run.**

`docs/REGISTER.md:555,571` (at audit time):

```
baseline        seed 11, weeds 0.0, tape seb, days 0-29
...
python -u scripts/breakdown.py --tape seb --seed 11 --weeds 0.0 --days 30 --diff --no-moves
```

`scripts/breakdown.py:118-119`: `RETIRED_TAPES = {"seb": "90494364, townCenterSellInterval 12 --
pre-rebalance, and its bank does not replay" ...}`; `:497` sets `choices=sorted(TAPES)` on the
`--tape` argument, and `TAPES` (`:83`) contained only `victor` and `kawashigi`.
`seb` is not a legal choice — this command failed immediately with `argparse` `error: argument
--tape: invalid choice: 'seb'`, before doing anything.

The same dead value appeared in `docs/experiment_log.md:432` and `docs/the_field.md:200`, both
naming `--tape seb` as the metric/tape currently in use.
Same failure pattern already confirmed the same day for `tests/test_each_day_matches_the_tape.py`
and `KeyError: 'seb'` — same retired name, different call site.

**1e. `docs/when_and_what_to_sell_2026-08-15.md` carried two numbers/claims a same-day doc said
were corrected, and the correction was never actually applied.**

`docs/fable_allocation_economics_2026-08-15.md:186-187`:

> `docs/when_and_what_to_sell_2026-08-15.md` §3 carries a correction block now: the +$12,136 "even
> spread" number compared against an infeasible baseline; the real release value is +$5,653.

But `docs/when_and_what_to_sell_2026-08-15.md:87` still read `TOTAL 152,792 164,928 +12,136` with
no correction block anywhere in the file (grepped for `5,653`, `12,136`, `correction` — the only
hit was the original uncorrected number).
The claimed edit was never made.

Second, unrelated correction that also never landed in this file: `RETRACTIONS.md` item 7
(2026-08-15) reports the prediction in `docs/when_and_what_to_sell_2026-08-15.md` §7 —
`MELON_YIELD_OPPONENT_MELON = 99` (rule off) should beat `= 7` (rule as shipped) — was tested on
960 games and **falsified** (68.1% vs 67.9%, a null, not a loss; "the model behind the prediction
swapped 120 units when the real switch is 8 tiles ... a 15x scaling error").
§4 of the same file (`"Even in the melon-heavy case the rule exists for, keeping melon beats
swapping by $8,162"`) and §7's falsifiable prediction were both still presented as open/live, with
no retraction note, even though the prediction had already resolved.

**1f. `docs/carrot_swap_2026-08-12.md` measured a flag's win-rate effect while carrot was
unsellable, and the flag no longer exists in code.**

Dated 2026-08-12, one day before commit `c99a8a5` (2026-08-13, "Three of the nine products could
never be sold, and the wool rule fired too late") fixed `SELLABLE` to include CARROT.
The doc's "deciding measurement" (`:266-281`) reported `CARROT_SWAP = 0` winning 65.1%/67.2%
against `CARROT_SWAP = 1` at 54.7%/59.4% across 384 games — entirely built on carrot revenue that
could not reach the market at the time it was measured.
Same defect class as the HERD_GEESE verdict already confirmed dead elsewhere.

`grep -rn "CARROT_SWAP" kagg/ scripts/ tests/` returned nothing — the flag does not exist in the
tree. See "Docs that should be deleted outright" below.

### 2. Suspected, unverified — not confirmed, do not treat as fact

1. Whether fast-sim parity was actually green on 1.32.7 at audit time.
   Code-level, `hinge` was handled in both `kagg/sim/market.py` and `kagg/sim/jax_sim.py`.
   No doc or log named a fresh 300/300-style full-episode run since that fix landed.
   This is the live half of finding 1b — plausible it passed, not shown to.
2. `REGISTER.md` OPEN-10's rebase recommendation (Dmitry Belan or Efe Can Celiksoy) may be
   superseded by what the project actually did.
   `scripts/breakdown.py`'s `TAPES` dict comments name `victor` as "the rebase target,
   2026-08-11" and `kawashigi` as the tape driving the shipped plan since 2026-08-13 — neither is
   Dmitry Belan or Efe Can Celiksoy.
   No doc found that explicitly closes OPEN-10 or explains the divergence from its own
   recommendation; this may just be an unclosed item rather than a wrong one.
3. Whether `docs/kill_criteria_and_settled_positions.md`'s parity claim carries any version
   caveat elsewhere in the file.
   Grepped the whole 96-line file (as it then was) for `1.32.6`/`1.32.7`/`parity` and found no
   caveat near the "PASSING... 300/300... 1.32.2" text, but not every line was close-read for an
   indirect qualifier.
4. Whether `REGISTER.md`'s missing citation-repair pass (finding 1a) broke any specific pointer a
   reader would actually follow.
   Confirmed the section and the date stamp were absent; did not diff every individual citation in
   the file against `e4e0c65`'s fixes to say which ones were wrong versus coincidentally still
   right.

### 3. Dead references

| Reference | Where cited | Status |
|---|---|---|
| `--tape seb` | `docs/REGISTER.md:555,571`, `docs/experiment_log.md:432`, `docs/the_field.md:200` | In `RETIRED_TAPES`, `scripts/breakdown.py:118`; not a legal `--tape` choice, argparse rejects it |
| `CARROT_SWAP` flag | `docs/carrot_swap_2026-08-12.md` (whole file) | Absent from `kagg/`, `scripts/`, `tests/` — does not exist in the current tree |
| `docs/REGISTER.md`'s `## What is in which file` section and 2026-08-13 citation fixes | Should exist per `e4e0c65`, did not exist in the checked-out file at audit time | See finding 1a |

### 4. Docs that should be deleted outright

- **`docs/carrot_swap_2026-08-12.md`** — measured entirely through the SELLABLE bug (carrot could
  not be sold when this was written), tests a flag (`CARROT_SWAP`) that does not exist anywhere in
  the current code, and `grep -rln "carrot_swap_2026-08-12"` across `docs/` and `CLAUDE.md`
  returned nothing — no other file points at it, so nothing breaks by removing it.
  A clean case of "stale-but-plausible artifact," the exact hazard this audit was commissioned to
  find.

No other file in `docs/` showed both (a) a stale, superseded conclusion and (b) zero remaining
references from other docs — everything else found was a live doc with a stale passage inside it,
needing correction in place, not deletion.

### Note on this audit's own limitation

The audit's worktree (`agent-a957e5eefe24b2b9f`) was checked out at commit `7a3535e` ("Add
jax_homestead as an opponent role, and the JAX agent round-robin"), which predates every file the
audit brief asked it to read — `docs/README.md`, `RETRACTIONS.md`,
`docs/kill_criteria_and_settled_positions.md`, `docs/handoff_2026-08-15.md`, `kagg/plan.py`, commit
`c99a8a5` — none of these existed in that worktree's working tree.
`git log --all` and `git show <rev>:<path>` still saw the full object history from there (no
working-tree redirect), so all dating in the report is real.
But the current file *content* used above was read directly from the shared checkout at
`/Users/alexchilton/DataspellProjects/kaggriculture` via the `Read` tool (not `git`, not `cd`, not
`-C`), since that was the only accessible copy of the current tree at the time.
If that checkout's working directory had further uncommitted edits beyond what `3b2a379` records,
the audit would not have seen them — no evidence of that was found (the one file diffed
byte-for-byte against its committed blob, `docs/REGISTER.md`, matched exactly), but not every file
was diffed that way.

---

## 2026-08-16 — Work to be done: planner defects, watering, melon fork, refactor plan, allocation LP

Folded in from docs/work_to_be_done_2026-08-16.md.

**This source is mostly an economics/allocation/planner-defect work list, not a kill-criteria or
settled-position doc.**
It is folded in here anyway because "open work items" is in scope for this consolidation group and
several of its results are measured nulls or flag-status findings that belong next to the dead
constant audit below.
But most of its content (strawberry mechanics, the melon fork's economics, the allocation LP,
open/unexplained economics questions, live submission inventory) reads as a handoff/economics todo
list and would fit better in an economics- or allocation-focused survivor doc, or in
`docs/REGISTER.md`'s OPEN list, if one of those consolidation passes wants it.
Flagging this per instruction rather than silently deciding.

Written at the end of a long session so the open threads would not be re-derived the next day.
Everything has a measurement behind it; where it does not, that is said explicitly.

### 1. The opening, d1 to d8 — the largest known defect (at the time)

The per-cell gate (`tests/test_each_day_matches_the_tape.py`, 30 days x 26 rows) failed 260 cells.
Days match IN ORDER, so the lowest failing day is the one to fix.

    d1  COLLECT_FERTILIZER  4/3      + PLACE          <- lowest failing day
    d3  WATER              13/14
    d4  WATER              16/15
    d5  WATER              12/13
    d6  WATER              16/19     + PLACE, crop_MELON, weed
    d6  BUY_LAND           ours h9 / tape h4          five hours late
    d7  WATER              28/27     + crop_MELON, weed
    d8  WATER              17/33     + PLANT 8/9, DIG, crop_MELON, crop_WHEAT

The cadence gate (`tests/test_the_money_lands_on_his_turn.py`) added a second, independent defect:
**we buy seed at dawn, he defers it to dusk.**

    d10  BUY_SEED  ours h[1,1,1]   tape h[20,21,22,23]
    d12  BUY_SEED  ours h[1 x9]    tape h[14,16,18]
    d15  BUY_SEED  ours h[1,1,1]   tape h[16,16,18,18,20,22,22,23]

Seed is for TOMORROW's planting.
He keeps the bank liquid through the day; we commit it at h1 on days that open at $4, and
`_do_hire` fails SILENTLY on a short bank.

### 2. Watering priority — a fix that exists, is measured, and is switched off

`cover.AT_RISK_TILE_OUTRANKS_A_FEED_THAT_CAN_SLIP` was uncommitted and False.
It makes a tile one dry night from weeding outrank a pen that was fed yesterday, which is
`REQUIRED_OPS`' own argument applied to the other half of the board.

Measured on seed 11 at `weedSpawnChance` 0: kills the two d8 weeds, d8 feed 9/10 -> 10/10, plant
6/9 -> 9/9 EXACT, strawberry 10/11 -> 11/11 EXACT — but costs d10 sell 95 -> 68 and $4,619, because
d10 is a `WALK_THE_LOAD_HOME_DAYS` day and the at-risk tiles take the turns the melon delivery
needs.
By d13 the money is a wash ($18,960 vs $18,880) and the weed count is WORSE — it kills the d8 weed
and grows a new one at d11 that survives to d13.

Next step identified at the time: exempt the walk-home days (10, 29) and re-run.
And re-measure at `weedSpawnChance` 0.005, the ladder value — the numbers above are from a board
nobody plays.

**2a. It is TWO defects, and only one of them had a fix written.**

Added 2026-08-16, later the same day.
The pass-order fix above is aimed at **turn-constrained days, d7 to d11**.
It cannot be the mechanism for the d12-d14 deaths, and the idle counts said so outright.

    day  unit-turns  idle  water  dig      game 93593633, planner, LOST
     12         256    77     22    0
     13         275    93     27    0
     14         211    41     29    0      <- eight strawberry tiles die here
     15         294    30     41   17

A cheapest-insertion greedy with 77 spare unit-turns places every job it is HANDED.
So on d12 the WATER job for those tiles was never in the pool.
That makes the d12-d14 failure a **job-generation** defect, not a pass-order one, and the fix at
`cover.py:1584` would not touch it.

The mechanism suspected was the precomputed path.
`cover.cover` returns EARLY on any day in `PRECOMPUTED_ROUTES`:

    pre = _apply_precomputed(day, units, jobs, ...)
    if pre is not None:
        return pre

So on those days **none of the greedy machinery runs** — not the `at_risk` pass order, not
`REPAIR`, not `COMPACT`.
A job the solved route has no stop for goes to `_insert_leftovers`, a cheapest FEASIBLE insertion
into tours that are already built, and whatever will not fit is simply not done.
The solved days start at **d12** on a three-quadrant board and **d9** on a four-quadrant one, which
is exactly where the deaths start.

**2a-i. Measured, and the d12 half of it is a NULL.**

`scripts/what_the_solved_day_drops.py`, seed 11, `weedSpawnChance` 0.005, kawashigi schedule.
Two arms: the shipped gate, and `--fork` forcing `MELON_YIELD_OPPONENT_MELON` to 0.
Logs at `data/logs/precomputed_drops_2026-08-16.log` and `..._fork_2026-08-16.log`.

     day    jobs seated ins DROP water  |  jobs seated ins DROP water      no fork -> fork
      12      43     37   6    0     0  |    39     32   7    0     0
      13      62     56   6    0     0  |    63     53  10    0     0
      14      52     48   4    0     0  |    45     38   7    0     0
      18      57     49   8    0     0  |    59     31  28    0     0
      20      72     60   8    4     3  |    71     51  15    5     5
      23      70     58  11    1     1  |    70     47  19    4     4
      24      73     49  14   10    10  |    69     39  16   14    14
      25      70     53  14    3     2  |    70     43  18    9     4
      27      71     58   7    6     6  |    72     47  17    8     7
      29      37     16  21    0     0  |    38     14  24    0     0

**Zero jobs are dropped on d12-d19 in either arm.**
The hypothesis that a d12 water job goes unoffered or unplaced is not reproduced on this seed, and
should not be carried forward as though it were.
Game 93593633 was a different board, seed and opponent, so this does not refute it either — it
means the mechanism has not been caught in a sim yet.

What the run DID measure, and it is the fork's real cost on the back half:

- On the fork board the solved day stops MATCHING. d18 seats 31 of 59 stops against 49 of 57
  unforked; d24 seats 39 against 49. The solve is roughly half discarded, and `_insert_leftovers`
  carries the rest — 28 insertions on d18 against 8.
- Tiles whose WATER is dropped on two or more solved days go **3 -> 8** with the fork on.
  `(0,7)` and `(9,4)` are dropped on three days each. Two dry days is a weed, so a tile appearing
  here twice on consecutive days is one killed by our own hand.
- The damage is at **d20-d27**, not d12-d14. d24 drops 14 waterings with the fork against 10
  without.

This is one seed. The direction is consistent with the ladder replays; the magnitude is not
established.

**2b. The solved tail is per BOARD SHAPE, and there are four shapes, not three.**

Alex's point, 2026-08-16.
Two independent branches decide the back half of the season, and their product is four boards:

                    3 quadrants (75 tiles)      4 quadrants (100 tiles)
    melon  (34 st)  A3  91919278                Q4  91907974
    straw  (42 st)  B3  91891131                MISSING

The strawberry-forked four-quadrant board is the worst case on both axes at once — 42 permanently
watered tiles spread across 100 tiles — and it is the one branch with no recorded tape and no
solved tail at the time.
That is the most likely reason the strawberry deaths cluster in fork games.

So "fix the watering" on the tape path means recording or synthesising **B4**.
On the planner path it is one solver, but the solved days still have to be re-solved per shape,
which is the same four cases.

**1a (numbered as in source). REGRESSION, found 2026-08-16 — the gate moved and nobody said so.**

The grid gate was **303 failed / 477 passed** at `c5831f9`, against **260 / 520** at `8b74e05`.
Forty-three cells went from green to red.
Bisected by running the CURRENT gate file against each commit in a worktree, with the CWD inside
the worktree so `import kagg` resolves there — the first two attempts silently imported the main
repo's `kagg` and reported a false "no change":

    8b74e05   260 failed  520 passed   Delete eight flags whose ON branch has never executed
    ed927fe   300 failed  480 passed   The four-quadrant herd is COW 6 / SHEEP 10          <- +40
    6a01c59   303 failed  477 passed   Restore the q4 herd to COW 6 / SHEEP 12             <- +3
    c5831f9   303 failed  477 passed   (docs and scripts; no change)

The failing rows were led by `an_SHEEP` (21 days) and `an_COW` (21 days).
**Seed 11 arms the four-quadrant branch**, so the q4 herd numbers are live in the gate, and the
note (elsewhere, in the refactor status) that the gate "held at 311/590/115/35 through all three
deletions" described only the deletions — it was never re-run after the herd work.

This was a d1-onward regression that shipped in the tape bundles at the time. Flagged to fix
before anything else.

### 3. Strawberry is what actually dies, and the fork makes it worse

Live ladder game 93593633 (planner, LOST $90,355 v $101,782), tile by tile:

    21 tiles became WEED. 20 were ours. NINETEEN were STRAWBERRY.

    d9 1   d10 4   d11 4   d12 1   d14 8   d15 1   d27 1

    day  unit-turns  idle  water  dig
     12         256    77     22    0
     13         275    93     27    0
     14         211    41     29    0
     15         294    30     41   17

We idle 77 and 93 unit-turns on d12-d13, eight strawberry tiles die on d14 (a crop weeds after two
dry days), and d15 spends 17 turns digging the corpses. **It is not a turn shortage.**

The mechanism is in the reference: MELON is `ongoing: False` — water it to day 10-12, harvest once,
tile spent. STRAWBERRY is `ongoing: True` — water it EVERY day to the end of the season or it
weeds, harvest every 2 days. The melon fork takes strawberry from 34 tiles to 42, converting eight
finite obligations into eight permanent ones.

**The fork fires on 44% of real games** (32 of 72 downloaded replays). Real opponents cluster at 8
and 12 melon tiles at d3, and the rule's threshold of 9 splits those clusters exactly.

**3a. The fork CAUSES the deaths; it does not by itself decide the game.**

Measured on submission 55548563's real 28-episode ladder record, pulled from the Kaggle API rather
than from `~/Downloads` — see the selection-bias warning at the bottom of this section.

                     games   weed tile-days   strawberry tiles died   mean margin
    fork FIRED / W       8             62.0                    11.9         +42,798
    fork FIRED / L       4             43.8                    13.0          -6,904
    fork quiet / W      15             43.7                     5.5         +16,722
    fork quiet / L       1             20.0                    10.0         -10,716

Two readings, and they point in different directions:

- **The fork more than doubles strawberry deaths — 5.5 without it, 12.4 with it.**
  That holds in both the wins and the losses, so it is a property of the fork rather than of the
  games it happened to be drawn into. The mechanism is confirmed.
- **It does not separate wins from losses.** Within fork games the death count barely moves
  (11.9 in wins, 13.0 in losses), and fork-fired wins still average +$42,798.

The observational data cannot go further than that, because the fork's trigger — opponent melon
>= 9 at d3 — is itself a proxy for opponent strength.
Against 12-melon builds the fork ALWAYS fires, so there is no control group.
The only clean test identified: a ladder A/B, the same bundle with the fork off, against the same
population.
If fork-off also goes ~50/50 against 12-melon opponents, the fork is innocent.

**3b. Two more games, 2026-08-16 12:59.**

    episode    our seat   ours       theirs     margin    opp melon d3   fork    straw died   weed tile-days
    93605352   1          153,932    155,937    -2,005    12             FIRED    4           18
    93606247   0           87,539     85,733    +1,806     5             quiet    4           97

Both inside $2,100, and both fit the pattern: the loss is a 12-melon opponent with the fork armed,
the win is a 5-melon opponent with the fork quiet.
The loss killed only **four** strawberry tiles, so this one is not a watering blowout — it is a
close game against a strong build, which is the reading 3a leaves open.
Planner record at the time: 24W-6L.

### 4. The melon fork is NOT implementable as a tape rewrite — measured NULL

Measured, 24 games against the frozen opponent: token-swapping MELON to STRAWBERRY inside a tape
recorded for melon scores **0.0% win rate against 66.7% with the swap off**, -$17,297 a game.
Adding a dig-guard lifts it to 12.5% and no further.
**This is a measured null for the tape-rewrite implementation approach — not evidence against the
fork idea itself, which belongs in the planner instead (see below).**

Product level, seed 3: the swap is +$2,966 on CROPS (fewer melons at $233 rather than $170, because
we stop crashing our own book) and -$8,365 on ANIMAL products. **The animal side is unexplained.**

One cause is identified and is a bug in the guard: keeping the strawberry alive leaves the tile
occupied, and the tape then plants on it — 12 wasted PLANTs against 1 with the swap off. The guard
must also suppress the REPLANT that follows the dig it cancelled.

The fork belongs in the planner, which knows each tile's crop and `ongoing` flag. A tape cannot
adapt maintenance to a crop it was not recorded for.

### 5. Refactoring — started, not finished (dead-code / flag-deletion status at 2026-08-16)

    done   plan_routes + _two_opt + _path_len + COVER_PLANNER     -319 lines, 10 tests deleted
    done   board_layout.py, sa_hiscadence_probe.py                -269 lines
    done   8 hard-OFF flags and their unreachable branches
           the three live files: 9,881 -> 9,245 lines

    left   10 hard-OFF flags  blocked by scripts/tests that set them at runtime
           101 hard-ON flags  same delete, keeping the branch that runs
           63 tests           assert a constant equals itself; they die with their flag
           3 constants        defined TWICE in the same file, the second silently wins:
                              SELLS_FUND_THE_TURN, URGENT_OPS, STEAL_FROM_DAY (read nowhere)
           victor             still a live tape in TAPES with 3 tests bound to it

The gate for every delete: both acceptance suites must report **311 failed, 590 passed, 115
xfailed, 35 xpassed**. Unchanged through all three deletions so far. A moved number means the code
was live.
(See section 2, item "1a" above: this gate figure was measured again on 2026-08-16 and had in fact
moved to 303 failed / 477 passed after the herd work — the "held through all three deletions" claim
covered only the deletions themselves and was not re-checked after.)

`coverage --branch` over five seeds says 25 scripts import the 0%-coverage modules and 22 of them
run, so `chains`, `dayplan`, `executor`, `library` and `replay_plan` are load-bearing for tooling
even though they never execute in a season. They are NOT free deletes.

**5a. The end state, agreed 2026-08-16: split `make_agent`.**

The file length is not the problem and never was.
`schedule_agent.py` is 5,156 lines of which **2,696 are comments and 365 are blank — 2,095 lines of
code.**
The problem is the shape:

    47 top-level defs, two of which are most of the code

      1,638 lines   make_agent      line 3519
        666 lines   _router_acts    line 1643
        154 lines   _refresh_pins
        101 lines   reservation_units

One 1,638-line function holding pins, hires, land, market orders, seed rows, the herd split and the
dusk top-up in a single mutable closure.
That is where "nobody can say whether the code being edited is live" comes from.

**How it is split does not matter much, as long as it makes sense.** Alex's call.
The point is that it stops being spaghetti — a reader should be able to find where a thing is
decided without reading 1,638 lines of one closure.

`kagg/search/q4_branch.py` is a reasonable example of the target readability: a trigger, a decision
taken once, and what changes when it fires, in one file you can read end to end.

Order of work agreed at the time, and the reasons are dependencies rather than preference:

1. Finish the flag deletions. Every flag is a cross-cutting condition; splitting around one means
   carrying it into two modules.
2. Resolve the eight doubly-defined constants FIRST. At the time, the second definition silently
   won and the file still worked. Split the file with a duplicate still in it and the two halves
   get different values — a real bug where there is currently only a readability defect.
3. Collect the surviving numbers into one block per file. Several of the remaining flags fold into
   a number, and they should land somewhere deliberate rather than beside whatever function used
   them.
4. Then split, one module at a time, gates green between each.

Not started at the time, and not to be started while the watering work is live in the same three
files.

### 6. What the allocation LP said (`docs/allocation_bounds_2026-08-16.md`)

The leader's MELON 20 / STRAWBERRY 34 is **not** inside the 1% near-optimal region: -1.78% against
a zero opponent, -3.9% against his own supply, -23% against double supply. Melon alone is the
cause — ~30 units of town demand a season, `sq` crash above threshold, and no shop ever sells melon
seed. Strawberry 34 IS inside the 1% interval in two of three scenarios.

Melon's 1% interval slides `[14,42] -> [0,31] -> [0,12]` with the opponent, so no fixed melon count
is near-optimal against all three — an argument FOR a melon fork, though not for the one shipped at
the time.

Geese become obligatory against a flooder (`[8,22]` at double supply) because egg's log-flat price
is the only crash-proof product. Geese were shipped off as a result.

Caveats: these are LP-relaxation OUTER bounds, MILP gaps 0.4-2.0%, and Z* swings
$129k / $93k / $53k with the shop draw.

### 7. Open and unexplained, at 2026-08-16

- The animal-product loss under the melon swap (-$8,365 on milk and wool, on one seed).
- Why swap-OFF wastes 19 FEED, 19 CARE and 17 COLLECT ops while swap-ON wastes none, yet earns more.
- The ~550 rating points between fe7aad6's 1947.9 and the-then-current builds. The close package
  was ruled out by ablation (+41.7pp of win rate, carried by NO_UPKEEP_ON_THE_LAST_DAY and
  WALK_THE_LOAD_HOME_DAYS; the other four exact nulls).
- The q4 branch fires on ~15% of seeds by the old count, but **the yarn-store unlock is not a pure
  function of the seed** — it depends on how the town is played, and both seats affect it. Seed 3
  arms against the frozen opponent and not against an idle one; seed 7 is the reverse.

### 8. Live submissions at the end of the 2026-08-16 session

    55548563  planner  post-1947.9 lineage, q4 armed, melon fork d3>=9    ~1500
              KNOWN DEFECT AT THE TIME: its q4 rows carry SHEEP 10, the herd standing at season end.
              The tape BUYS SHEEP 12. Fixed in 6a01c59, AFTER this bundle was built.
    55549820  tape3    two tapes, dig inserted with day-slack and must-dig, both swaps

Selection bias warning for any analysis of `~/Downloads`: those replays are LOSSES, chosen by hand.
Within-sample comparisons are fine; a win rate computed from them is not.

---

## 2026-08-17 — Dead-constant audit of `kagg/search/`

Folded in from docs/dead_constant_audit_2026-08-17.md.

40 module-level boolean constants checked, each by reading the guard that consumes it, not by grep.
**17 have a branch that cannot execute.**
Nothing was deleted; this is the report the NO FLAGS rule asks for before anything is removed.

### The one that matters most

    HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE = False    schedule_agent.py:2761
    guard: 2796  if WOOL_SHOP_SETS_THE_HERD and HERD_FOLLOWS_...:

Block 2796-2814 is unreachable.
`MILK_POOR_COW`, `MILK_POOR_SHEEP` and `MILK_POOR_SHOP_COUNT` (2769-2771) are read **only** inside
it, so all three are dead.
That is why the herd has never responded to the milk draw: the rule is switched off, not
mis-gated.
The live branch is at 2816 and reads the yarn store only.

### Other dead branches

    constant                                    file:line              value  what is dead
    AT_RISK_TILE_OUTRANKS_A_FEED_THAT_CAN_SLIP  cover.py:113           False  the at-risk greedy pass (1404)
    SUPPLY_LIMITS_EVERY_DRAW                    cover.py:170           False  the ops-based supply check (1319)
    DELIVER_SURPLUS_NOT_THE_ROW                 cover.py:240           False  the surplus-count arm (655)
    BANK_THE_ROWS_PRODUCE_WHILE_REAPING         cover.py:274           False  `funding` always False, reaping exemption (719)
    STRICT_FEASIBILITY                          crew.py:126            False  `raise InfeasibleDay` (626)
    SHOP_ADAPT_CROPS                            schedule_agent.py:2624 False  the `_adapt_crops(...)` call (1621)
    MEMOISE_SLOT                                cover.py:148           True   unmemoised `slot_now` fallback (1283)
    BRANCH_ON_THE_YARN_STORE                    q4_branch.py:60        True   the early-disable return (292)
    LIVESTOCK_ENABLED                           plan.py:327            True   the CEM gene-zeroing block (340)
    PLAN_THE_CREW_THAT_ARRIVES                  schedule_agent.py:236  True   old crew-count replan trigger (1861)
    LATE_SEASON_PAIR                            router.py:665          True   both `else 99` arms (667, 676)
    HIRE_FIRST                                  schedule_agent.py:1057 True   old "hire two a turn" block (4966-4977)
    ANIMAL_OVER_HIRE                            schedule_agent.py:1081 True   the `8`-slot ternary arm and skip-buying (4636-4637)

`LATE_SEASON_PAIR = True` means `FERTILIZE_UNTIL_DAY` and `LATE_TRUNCATED_PLANT_DAY` can only ever
be 26.

**Note, at fold-in time:** `AT_RISK_TILE_OUTRANKS_A_FEED_THAT_CAN_SLIP` above is the same flag
measured in section 2 of the 2026-08-16 work-to-be-done record above — dead per this audit, and per
that record's own measurement, a wash on money and worse on weeds on the seed tested (though not
yet re-measured with the walk-home-day exemption or at the ladder's real `weedSpawnChance`).

### Orphaned: defined, never read as a live condition, named only in comments

    CLOSED_TOUR              router.py:230
    TOP_UP_SAFE_TILES        router.py:429
    SEED_BEFORE_LIVESTOCK    schedule_agent.py:3265

### Confirmed LIVE — both outcomes reachable, or no `else` to be dead

`REPAIR`, `COMPACT`, `TRIM_A_TAIL_THAT_CANNOT_COME_HOME`, `MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE`,
`PLACE_DRAWS_FEED`, `LATE_SEASON_TRIAGE`, `FUND_THE_DAY_WHEN_SHORT`, `HARVEST_WHAT_YOU_STAND_ON`,
`CARE_WHAT_YOU_STAND_ON`, `LAST_DAY_DEADLINE_WALK`, `CUMULATIVE_SELLS`, `LIQUIDATE_LAST_DAY`,
`SELLS_FUND_THE_TURN`, `DIG_A_WEED_WHEN_THE_ROW_IS_SHORT_OF_GROUND`, `PRICE_AWARE_SELL_CAP`,
`RESERVATION_SELL_CAP`, `HOLD_A_FLOORED_BOOK`, `LATE_SELL_BIAS`, `SHOP_ADAPT_HERD`,
`WOOL_SHOP_SETS_THE_HERD` (its 2816 use), `PLANT_THEN_WATER`, `REPLANT_A_CLEARED_TILE`,
`NO_UPKEEP_ON_THE_LAST_DAY`.

### Not an oversight

`DELIVER_SURPLUS_NOT_THE_ROW` is recorded in `docs/REGISTER.md` (OPEN-1) as a deliberately-off arm,
measured and rejected at -$15,272 over twelve seeds.
Dead, but on purpose.

### Note on `HARVEST_WHAT_YOU_STAND_ON`

Listed live here, and `docs/wasted_late_turns_2026-08-17.md` measures a hand standing on a ripe
3-unit wheat tile for seven consecutive hours emitting PASS.
"Live" means the guard can execute, not that it fires when it should.
Those two facts together are the open question.

