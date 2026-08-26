# The clone lineage: where its arms actually split

Measured 2026-08-26, `scripts/when_do_the_clones_stop_cloning.py` and a pairwise turn-by-turn diff of
the three extracted tapes. Log: `data/logs/tape_divergence.log`.

**Written because I registered three tapes and called them arms before measuring where they split.**
Alex: *"you said you are building 3 tapes arms - i assumed that meant you knew where they split"*.
The structure below is the measurement, not the assumption.

## They are not three tapes. They are one tape and two branch points.

```
first differing turn, pairwise:
   yarn3  vs yarn6   turn 194  = day 8  hour 02
   yarn3  vs late    turn 160  = day 6  hour 16
   yarn6  vs late    turn 160  = day 6  hour 16

turns identical across ALL THREE, per day:
   d0 24/24   d1 24/24   d2 24/24   d3 24/24   d4 24/24   d5 24/24
   d6 16/24   d7 0/24    d8 0/24 ...
```

```
d0 ─────────────── d6h16 ─────── d8h02 ─── d11 │ d12 ──── d23 │ d24 ── d29
  one shared opening   │            │           │              │
                       ├── late ────┴───────────┤   SOLVER     │  PLANNER
                       └── early ─┬─ yarn3 ─────┤              │
                                  └─ yarn6 ─────┤              │
```

- **d0-d5 is one tape.** Byte-identical across all three, 24 turns of 24. Storing three copies of it
  is waste.
- **First split d6 h16**, early-yarn against late.
- **Second split d8 h02**, yarn3 against yarn6.

## The bit is the yarn slot, but it is ACTED ON days after it is observable

A decision tree over the shop draw and the opponent's d3 board recovers the selector as one feature,
which slot `YARN_STORE` lands in -- 0.481 + 0.200 of the importance it uses
(`data/logs/tape_selector.log`).

**I assumed that meant the branch fires at d3, when the yarn store can first appear. It does not.**
Knowing yarn landed on d3 changes nothing for three days; yarn3 and yarn6 stay identical until
**d8 h02**. So the bit is observable at d3-d6 and acted on at d6h16 and d8h02.

That places both splits **inside the tape zone** (d4-d11), not at its boundary. Same shape as
`melon_branch`, which installs rows from d3 on カワシギ's melon-count bit, so the machinery for a
mid-tape branch already exists.

## What three schedules costs

The solver routes are per-schedule: `_apply_precomputed` keys a stop on `(tile, ops)`
(`cover.py:1020`), so routes solved for one branch's d12 board do not seat on another's. Three
branches therefore means:

- **three separate d12-d23 solves**, ~40-50 min each on the box at 300s/day
- **three `solved_days_*.py` modules**, chosen at runtime by the same bit

The repo already does exactly this for カワシギ's four arms -- `solved_days.py`,
`solved_days_straw.py`, `solved_days_q4.py`, `solved_days_straw_q4.py`.

**Only `clone_late` is being solved.** It is the largest branch (49 seats, 20 names) and the one we
are closest on (-$2,620 against -$11,627 and -$19,585). If it does not beat the current build on
`scripts/gate_against_the_clones.py`, the other two solves are not worth running.

## Why the solve is d12-d23 and not d12-d29

`cover.py:967` is `UNSOLVE_DAYS = tuple(range(24, 30))`, and the next line drops those days from
`PRECOMPUTED_ROUTES` at import. The first launch used `resolve_days.py`'s default of d12-d29 and
would have spent ~23 minutes of a ~68 minute run solving six days the agent discards. Alex caught it
by asking what range the solver covers.
