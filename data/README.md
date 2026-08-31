# data/

`data/*` is git-ignored. **Eighty-two files are force-added, and they are not scratch — the agent
does not run without them.**

Locally this directory holds ~91 GB of downloaded Kaggle episode replays, leaderboard snapshots and
training checkpoints. None of that is tracked. What is tracked is the minimum needed to build a
submission and reproduce the measurements in the README.

## What is tracked, and why

| Path | Size | Why it cannot be ignored |
|---|---|---|
| `seed_scripts/kawashigi/schedule.json` | 37 KB | The 30 per-day target rows. `kagg/plan.py:34` loads it as `SHIPPED_PLAN`. |
| `seed_scripts/kawashigi/92498144.json` | 30 MB | Tape for latch `(melon=False, q4=False)` |
| `seed_scripts/kawashigi/92466371.json` | 29 MB | Tape for `(melon=True, q4=False)` |
| `seed_scripts/downloads_2026-08-13/91907974.json` | 31 MB | Tape for `(melon=False, q4=True)` |
| `seed_scripts/downloads_2026-08-13/91906088.json` | 31 MB | Tape for `(melon=True, q4=True)` |
| `seed_scripts/field/` | 4.7 MB, 44 files | The recorded ladder opponents every win rate in the README is measured against |
| `opponent_tapes/` | 3.6 MB, 31 files | Thin action tapes — the same games with the observations stripped |
| `il/bundle_vocab_kawa_s16.json` | 18 KB | The 164-entry market-bundle vocabulary the policy's bundle head is indexed against |

`kagg/search/schedule_agent.py:3935-4017` names the four tapes by path and replays them for all 30
days. They were git-ignored until 2026-08-31, which meant the repository could build no submission
and reproduce no measurement without a directory that existed on one laptop.

## The 121 MB is mostly padding, and that is a known compromise

`_replay_opening` (`schedule_agent.py:4026`) reads exactly three things from a tape:
`info.TeamNames`, and per frame the seat's `action.farmer`, `action.hands` and `action.market`.
A recording is ~99.6% observations that no shipped code path touches.

`opponent_tapes/` in the table above is what the thinned form looks like: 31 games in 3.6 MB against
375 MB as raw recordings. The four latch tapes were **not** thinned, because several diagnostics
read their observations for board state and the equivalence was not verified before the work
stopped. Thinning them is the obvious next cleanup, and the test it needs is that
`_replay_opening` returns an identical dict for the thin and the full file.
