# Documentation staleness audit — 2026-08-15

Read-only audit. No code touched. Method: read the current file content from the live checkout
at `/Users/alexchilton/DataspellProjects/kaggriculture` (this worktree is pinned at an old commit,
7a3535e, and cannot see any file created or edited after 2026-08-03 — see the note at the end),
then dated every claim with `git log --all -S"<string>" --format="%h %ad %s" --date=short`, run
from this worktree without touching the shared checkout's working tree (git object access only).

---

## 1. CONFIRMED STALE — ranked most dangerous first

### 1a. `docs/REGISTER.md` is reverted and corrupted — the mandatory "check before opening
anything" doc is missing a whole day's edits

`docs/REGISTER.md:1-3` currently reads:

```
is cl# Register — what is open, what is closed, and what keeps reopening

Last updated 2026-08-08, on `shaping-potential`.
```

Line 1 is garbled (`is cl#` in front of the title — a splice artifact, the same failure class
CLAUDE.md already warns about: *"a hand-rolled `submission/main.py` spliced a docstring over line
1, failed to import"*). The date stamp is wrong by five days on a file that names its own
freshness as load-bearing.

**Dated evidence it should not read this way:**

- `bbc2a31` (2026-08-13, "Restamp REGISTER.md's last-updated date after today's pass") explicitly
  changes the line to `Last updated 2026-08-13, on \`shaping-potential\`.`
- `e4e0c65` (2026-08-13, "Fold README.md's index into REGISTER.md, and correct stale herd/citation
  claims") adds a whole new top section, `## What is in which file`, immediately after that line,
  and rewrites every citation inside `REGISTER.md` that pointed at a file deleted in the 2026-08-13
  pass.
- Neither the 2026-08-13 date stamp nor the `## What is in which file` section is present in the
  file as it currently reads. `git show 3b2a379:docs/REGISTER.md` (the most recent commit that
  touched the file, 2026-08-15) reproduces the same garbled line 1 and the same 2026-08-08 stamp —
  this is not an uncommitted local edit, it is checked in.
- Tracing parents: `3b2a379`'s parent is `c4236e9`, whose parent is `931fda6` (both 2026-08-15).
  `git log c4236e9 -- docs/REGISTER.md` stops at `513fff7` (2026-08-11) — this lineage never
  incorporated `bf43f62` / `bbc2a31` / `e4e0c65` (all 2026-08-13). Two branches diverged around
  2026-08-11 and only one carries the 2026-08-13 register cleanup; the checked-out one does not.

**Why this is the most dangerous item on this list:** `CLAUDE.md` names `REGISTER.md` as the doc to
"check before opening anything," and its own ground rule says an item is closed only if a named
artifact backs it. A session trusting the current file's citations is working from a version that
is missing a full day of citation repair, with no visible sign anything is wrong beyond the garbled
first line.

### 1b. `CLAUDE.md`'s own "three things still bind" section is contradicted by `CLAUDE.md`'s own
Kaggle section, written the same day

`CLAUDE.md:168`:

> **Fast-sim parity PASSES** -- 300/300 full-length episodes exact, all 18 unit ops and 6 market
> orders.

No version qualifier. Presented as one of the three things that still bind, unconditionally.

`CLAUDE.md:187-194` (Kaggle section, added the same day):

> `kaggle-environments >= 1.32.7` is required (2026-08-15 balance change, PR #1399) ... `kagg/sim/
> market.py` died on `KeyError: 'hinge'` and `kagg/sim/jax_sim.py` would have priced all three at
> flat base **in silence**.

**Dated evidence the parity claim has already gone stale on this exact pattern once:**

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

**What I could NOT confirm either way:** whether the 300/300 full-episode fast-sim gate has been
re-run and passed since the 1.32.7 `hinge` fix landed in `kagg/sim/market.py` and
`kagg/sim/jax_sim.py` (both files do have a `hinge` branch now — code-level, this is fixed). No doc
or log names a fresh full-suite run. Treat the CURRENT truth value of "parity passes" as
**unverified**, separate from the confirmed finding above, which is that the claim in `CLAUDE.md`
carries no version caveat and has already been silently wrong once on an identical version bump.

### 1c. `docs/competition_brief.md` — read-first item #1 — has no mention of the 1.32.7 balance
change and tells a reader to install a version two behind current

`docs/competition_brief.md:248`: `pip install -U "kaggle-environments>=1.32.2"    # earlier
versions lack the env`. Zero occurrences of `hinge` or `1.32.7` anywhere in the file (grepped).

`CLAUDE.md:187`: **`kaggle-environments >= 1.32.7` is required** (2026-08-15 balance change, PR
#1399) ... "Any baseline measured before 2026-08-15 describes a different game."

A session reading the docs in `CLAUDE.md`'s own prescribed order (`README.md` → `competition_brief.
md` → ...) hits the install instruction before it hits the correction. Installing 1.32.2 per this
doc silently mis-prices CARROT, TOMATO and EGG (the `hinge` shape).

### 1d. `REGISTER.md`'s own "the only metric that counts" command names a retired tape and cannot
run

`docs/REGISTER.md:555,571`:

```
baseline        seed 11, weeds 0.0, tape seb, days 0-29
...
python -u scripts/breakdown.py --tape seb --seed 11 --weeds 0.0 --days 30 --diff --no-moves
```

`scripts/breakdown.py:118-119`: `RETIRED_TAPES = {"seb": "90494364, townCenterSellInterval 12 --
pre-rebalance, and its bank does not replay" ...}`; `:497` sets `choices=sorted(TAPES)` on the
`--tape` argument, and `TAPES` (`:83`) contains only `victor` and `kawashigi`. `seb` is not a legal
choice — this command fails immediately with `argparse` `error: argument --tape: invalid choice:
'seb'`, before it does anything.

The same dead value appears in `docs/experiment_log.md:432` and `docs/the_field.md:200`, both
naming `--tape seb` as the metric/tape currently in use. This is the exact failure pattern already
confirmed today for `tests/test_each_day_matches_the_tape.py` and `KeyError: 'seb'` — same retired
name, different call site.

### 1e. `docs/when_and_what_to_sell_2026-08-15.md` carries two numbers/claims a same-day doc says
were corrected, and the correction was never actually applied

`docs/fable_allocation_economics_2026-08-15.md:186-187`:

> `docs/when_and_what_to_sell_2026-08-15.md` §3 carries a correction block now: the +$12,136 "even
> spread" number compared against an infeasible baseline; the real release value is +$5,653.

But `docs/when_and_what_to_sell_2026-08-15.md:87` still reads `TOTAL 152,792 164,928 +12,136` with
no correction block anywhere in the file (grepped for `5,653`, `12,136`, `correction` — the only
hit is the original uncorrected number). The claimed edit was never made.

Second, unrelated correction that also never landed in this file: `RETRACTIONS.md` item 7
(2026-08-15) reports the prediction in `docs/when_and_what_to_sell_2026-08-15.md` §7 —
`MELON_YIELD_OPPONENT_MELON = 99` (rule off) should beat `= 7` (rule as shipped) — was tested on
960 games and **falsified** (68.1% vs 67.9%, a null, not a loss; "the model behind the prediction
swapped 120 units when the real switch is 8 tiles ... a 15x scaling error"). §4 of the same file
(`"Even in the melon-heavy case the rule exists for, keeping melon beats swapping by $8,162"`) and
§7's falsifiable prediction are both still presented as open/live, with no retraction note, even
though the prediction has already resolved.

### 1f. `docs/carrot_swap_2026-08-12.md` measures a flag's win-rate effect while carrot was
unsellable, and the flag no longer exists in code

Dated 2026-08-12, one day before commit `c99a8a5` (2026-08-13, "Three of the nine products could
never be sold, and the wool rule fired too late") fixed `SELLABLE` to include CARROT. The doc's
"deciding measurement" (`:266-281`) reports `CARROT_SWAP = 0` winning 65.1%/67.2% against
`CARROT_SWAP = 1` at 54.7%/59.4% across 384 games — entirely built on carrot revenue that could not
reach the market at the time it was measured. Same defect class as the HERD_GEESE verdict the task
brief already confirmed dead.

`grep -rn "CARROT_SWAP" kagg/ scripts/ tests/` returns nothing — the flag does not exist in the
current tree. See §4 below for the deletion recommendation.

---

## 2. SUSPECTED, UNVERIFIED — not confirmed, do not treat as fact

1. **Whether fast-sim parity is actually green right now, on 1.32.7.** Code-level, `hinge` is
   handled in both `kagg/sim/market.py` and `kagg/sim/jax_sim.py`. I found no doc or log naming a
   fresh 300/300-style full-episode run since that fix landed. This is the live half of finding 1b
   — plausible it passes, not shown to.
2. **`REGISTER.md` OPEN-10's rebase recommendation (Dmitry Belan or Efe Can Celiksoy) may be
   superseded by what the project actually did.** `scripts/breakdown.py`'s `TAPES` dict comments
   name `victor` as "the rebase target, 2026-08-11" and `kawashigi` as the tape driving the shipped
   plan since 2026-08-13 — neither is Dmitry Belan or Efe Can Celiksoy. I did not find a doc that
   explicitly closes OPEN-10 or explains the divergence from its own recommendation; this may just
   be an unclosed item rather than a wrong one, and I have not read every 2026-08-11/12/13 doc
   closely enough to be sure which.
3. **Whether `docs/kill_criteria_and_settled_positions.md`'s parity claim carries any version
   caveat elsewhere in the file.** Grepped the whole 96-line file for `1.32.6`/`1.32.7`/`parity` and
   found no caveat near the "PASSING... 300/300... 1.32.2" text, but I did not close-read every
   line for an indirect qualifier.
4. **Whether `REGISTER.md`'s missing citation-repair pass (finding 1a) broke any specific pointer
   a reader would actually follow.** I confirmed the section and the date stamp are absent; I did
   not diff every individual citation in the file against `e4e0c65`'s fixes to say which ones are
   currently wrong versus coincidentally still right.

---

## 3. DEAD REFERENCES

| Reference | Where cited | Status |
|---|---|---|
| `--tape seb` | `docs/REGISTER.md:555,571`, `docs/experiment_log.md:432`, `docs/the_field.md:200` | In `RETIRED_TAPES`, `scripts/breakdown.py:118`; not a legal `--tape` choice, argparse rejects it |
| `CARROT_SWAP` flag | `docs/carrot_swap_2026-08-12.md` (whole file) | Absent from `kagg/`, `scripts/`, `tests/` — does not exist in the current tree |
| `docs/REGISTER.md`'s `## What is in which file` section and 2026-08-13 citation fixes | Should exist per `e4e0c65`, does not exist in the checked-out file | See finding 1a |

---

## 4. Docs that should be DELETED outright

- **`docs/carrot_swap_2026-08-12.md`** — measured entirely through the SELLABLE bug (carrot could
  not be sold when this was written), tests a flag (`CARROT_SWAP`) that does not exist anywhere in
  the current code, and `grep -rln "carrot_swap_2026-08-12"` across `docs/` and `CLAUDE.md` returns
  nothing — no other file points at it, so nothing breaks by removing it. This is a clean case of
  "stale-but-plausible artifact," the exact hazard this audit was commissioned to find.

No other file in `docs/` showed both (a) a stale, superseded conclusion and (b) zero remaining
references from other docs — everything else found above is a live doc with a stale passage inside
it, which needs correcting in place, not deleting.

---

## Note on this audit's own limitation

This worktree (`agent-a957e5eefe24b2b9f`) is checked out at commit `7a3535e` ("Add jax_homestead as
an opponent role, and the JAX agent round-robin"), which predates every file this brief asked me to
read — `docs/README.md`, `RETRACTIONS.md`, `docs/kill_criteria_and_settled_positions.md`,
`docs/handoff_2026-08-15.md`, `kagg/plan.py`, commit `c99a8a5` — none of these exist in this
worktree's working tree. `git log --all` and `git show <rev>:<path>` still see the full object
history from here (no working-tree redirect), so all dating in this report is real. But the current
file *content* used above was read directly from the shared checkout at
`/Users/alexchilton/DataspellProjects/kaggriculture` via the `Read` tool (not `git`, not `cd`, not
`-C`), since that is the only accessible copy of the current tree. If that checkout's working
directory has further uncommitted edits beyond what `3b2a379` records, this audit would not see
them — I found no evidence of that (the one file I diffed byte-for-byte against its committed blob,
`docs/REGISTER.md`, matched exactly), but I did not diff every file that way.
