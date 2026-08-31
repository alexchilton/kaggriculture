# submission/

**Generated. Nothing here is source, so nothing here is tracked.**

A bundle is a single self-contained file of ~14,000 lines: the agent, its schedule and its four
recorded tapes stitched together, because a Kaggle submission runs with no `data/` tree and no
package alongside it.

Three of them were tracked until 2026-08-31 and came to 28,497 lines — 20% of the Python in this
repo — all of it build output that git had no reason to hold.

## Build one

    python -u scripts/build_planner_submission.py --out submission/main.py

It bundles `kagg/search/schedule_agent.py` with `data/seed_scripts/kawashigi/schedule.json` and the
four tapes, fills `EMBEDDED_OPENINGS` so the artifact carries its own recordings, and verifies the
result imports and plays a season. That verification is not optional: a hand-rolled bundle once
spliced a docstring over line 1, failed to import, and banked exactly the $3,000 start.

The tape-only variant, which `scripts/where_the_animals_die.py` and
`scripts/probe_tape_submission.py` load by path:

    python -u scripts/build_tape_submission.py --out submission/main_tape.py

## Gate it before submitting

    python -u scripts/gate_pool.py --agent submission/main.py

**Never gate against `starter` alone.** It sells almost nothing, so the market is never contested
and every number comes out roughly 2x reality. That mistake cost a submission.

Five submissions per day. Always measure locally first.
