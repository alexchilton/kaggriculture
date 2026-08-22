# Geese verdict status, checked 2026-08-22

## What I claimed

"The geese machinery exists and ships OFF; the old goose verdict is VOID because it was measured
while SELLABLE blocked EGG entirely."

## What the evidence actually says

### The machinery exists and ships off

`HERD_GEESE = 0` in the current working tree, `kagg/search/schedule_agent.py:3153`.
This is the flag `swap_in_geese` (`kagg/search/schedule_agent.py:3177-3251`) reads to decide how
many of the schedule's cow/sheep purchases become geese.
`swap_in_geese` itself is live code, not deleted.
True, as claimed.

### The mechanism's history: deleted, then restored

Commit `c9c1c18` (2026-08-12 06:30, "Geese lose to the mirror and to the field; keep the machinery,
switch it off") measured "-21k a game at one bird in the mirror, and 42 points of win rate against
24 recorded opponents at two" — quoted verbatim in `kagg/search/schedule_agent.py:3123-3124`.
Commit `7a88d30` (2026-08-12 06:34, four minutes later, "Delete the geese rather than leave a losing
flag in the tree") deleted the mechanism on the strength of that measurement.
Commit `bce37fb` ("Restore the geese SELLABLE couldn't reach, and leave the flag off") put it back.
The restoration comment is explicit: `kagg/search/schedule_agent.py:3122`, "RESTORED... That
measurement is void."

### The SELLABLE bug: real, dated, and it does cover this window

`SELLABLE` is defined at `kagg/search/schedule_agent.py:3532`.
Commit `c99a8a5` (2026-08-13 06:53, "Three of the nine products could never be sold, and the wool
rule fired too late") is the fix.
Before that commit, `SELLABLE` held six of the env's nine product names — CARROT, TOMATO and EGG
were not in the loop that emits SELL, so the agent could never sell them regardless of market
conditions.
This is stated in the code (`kagg/search/schedule_agent.py:3125-3127`) and in
`docs/REGISTER.md:34-42` ("third version caveat, added 2026-08-13").

The `HERD_GEESE` sweep that produced the "-21k a game" verdict was measured 2026-08-11/12
(`c9c1c18` is timestamped 2026-08-12 06:30, before `c99a8a5` at 2026-08-13 06:53).
So: **that specific sweep is void, because it ran before the SELLABLE fix, and geese produce EGG,
which the SELLABLE bug made unsellable.**
True, as claimed, and this is not a novel finding — it is stated almost word for word in
`docs/the_carrot_window_is_three_days_2026-08-21.md:158` ("Geese. Held back on instruction, and the
old goose verdict is void anyway because it was measured while `SELLABLE` blocked EGG") and in
`docs/README.md:16`.

### What the claim leaves out: a second, later, valid verdict also closes geese

`docs/the_goose_is_insurance_2026-08-15.md` reopened the question on 2026-08-15, after the SELLABLE
fix, with hand arithmetic against `reference/kaggriculture.py` directly (not our agent's code, so
SELLABLE cannot taint it).
That doc's own conclusion, on the MONEY objective: "a cow or sheep beats a goose by about $8,000 per
six animals... anyone quoting this doc for 'geese are better' is misreading it"
(`docs/the_goose_is_insurance_2026-08-15.md:82-83`).

`docs/fable_geese_audit_2026-08-15.md` audited and corrected that arithmetic the same day, still
computed directly from the real production/price functions, and closed geese on the Elo/margin
objective: "goose is best in **0.9%** of draws... -$11,758 of expected MARGIN per six animals"
(`docs/fable_geese_audit_2026-08-15.md:12-16`).
Its own policy section states: "Zero geese" (`docs/fable_geese_audit_2026-08-15.md:112`).
It also states plainly that the original deletion and the corrected arithmetic land in the same
place for different reasons: "The `HERD_GEESE` deletion (`7a88d30`) was right by accident: the sweep
it rested on measured unsellable eggs, but the corrected arithmetic reaches the same end state"
(`docs/fable_geese_audit_2026-08-15.md:117-118`).

`docs/README.md:13` (2026-08-15 index) records this as the standing position: "**Geese are closed on
the Elo objective**."
This is a *different, SELLABLE-independent* verdict, and it is not void.

### Independent, later evidence from real replays also says geese are closed

`docs/the_tape_beats_our_planner_2026-08-21.md:98-115`, from `scripts/who_plays_tomato_or_geese.py`
across 4,022 seats of the downloaded replay tree: "the best goose seat plays 3-4 in a season.
Nobody builds around them," headed "**Geese: closed by absence.**"
This measurement reads real Kaggle replay data, not our own agent's sell logic, so SELLABLE cannot
be the explanation.

### Does the tape we ship (kawashigi) place geese?

Not established directly.
The 43-of-78-games / mean 1.2 / max 4 / days 6-13 goose-placement statistic in
`kagg/search/schedule_agent.py:2886-2888` and `2942-2954` is measured over **tetsuya's** 78 games
("Measured over tetsuya's 78 games," `kagg/search/schedule_agent.py:2886-2887"), not カワシギ's.
`REPLAY_OPENING_TAPE` (`kagg/search/schedule_agent.py:3758-3761,3817`) — the tape the current
submission actually replays — resolves every key to a カワシギ game.
No doc found quantifies カワシギ's own goose count specifically.
A different, earlier sample (`docs/what_the_leaders_actually_grow_2026-08-09.md:401-409`, 20 WIN-row
leader seats including "Seb's") reports GOOSE=0 in every single row, and states goose usage is
"untested past a boundary nobody approaches" and "n=0 across every leader seat and both our
losses."
`docs/the_ladder_is_two_scripts.md:61` similarly reports "Nobody in the top 16 owns a single goose,"
from a 2,744-seat sample.
Both of those samples predate or are independent of the tetsuya statistic and do not name
カワシギ specifically either.
So: real-player evidence is mixed between "effectively zero" (top-16/leader samples) and "sparing,
opportunistic" (tetsuya, one player, 78 games) — but no source in this repo isolates カワシギ's own
goose count.

## Verdict

**Partially true.**

True:
- The machinery exists (`swap_in_geese`) and currently ships off (`HERD_GEESE = 0`,
  `kagg/search/schedule_agent.py:3153`).
- The original `HERD_GEESE` sweep (measured 2026-08-11/12, `c9c1c18`) is void, because it ran
  before the SELLABLE fix (`c99a8a5`, 2026-08-13) and geese's only product, EGG, could not be sold
  at the time it was measured.

False, or at least incomplete, if the claim is read as "so the goose question is currently open" or
"so there is no valid verdict against geese":
- A second, later verdict (`docs/fable_geese_audit_2026-08-15.md`, 2026-08-15) was computed directly
  from the reference environment's production and pricing functions, is not affected by the
  SELLABLE bug, and independently closes geese on the metric the ladder actually pays (Elo margin,
  not money): goose is margin-best in 0.9% of shop draws, -$11,758 worse than cow/sheep per six
  animals.
- A third, still later line of evidence (`docs/the_tape_beats_our_planner_2026-08-21.md`, real
  replay data, 4,022 seats) independently reports geese closed by absence in actual ladder play.
- `docs/README.md`'s own 2026-08-15 index records the standing position as "Geese are closed on the
  Elo objective," not "open."

So "the old verdict is void" is correct but describes a verdict that has already been superseded by
a valid one reaching the same conclusion (zero geese) for an unrelated reason.
Citing only the voiding, without the newer closure, understates how settled the current position is.

## What is genuinely still open about geese

- カワシギ's own goose count, specifically — not established in any doc found here.
- Whether a mixed herd (not the 6-of-one-species portfolios `fable_geese_audit_2026-08-15.md`
  compares) changes the margin ranking — the doc's own caveat section says this was not tested
  (`docs/fable_geese_audit_2026-08-15.md`, section 5, "Only 6-of-one-species portfolios were
  compared... Mixed herds interpolate; nothing in the margin table rewards mixing geese in" — so the
  audit addresses this but has not run it).
- Whether the corrected op-cost and release-timing findings (`docs/fable_geese_audit_2026-08-15.md`,
  section 2 and section 3's release-timing corollary) change anything once
  `SHOP_ADAPT_HERD`'s cow/sheep float is itself re-tuned — flagged as future work in
  `docs/REGISTER.md:528` ("Shop-adaptive herd shipped and measured; floors still open").
