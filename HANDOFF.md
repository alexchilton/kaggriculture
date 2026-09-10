# Handoff — 2026-09-10

## State

Branch `main`, commit `c0e2d4d`, freshly re-cloned from GitHub.
The working copy had been deleted from the Mac; `gh repo clone alexchilton/kaggriculture` restored it.
The Windows box copy at `alex@192.168.1.128:~/kaggriculture` is **not a git repo** — it is a tar-transferred tree and holds 422 files newer than 2026-08-25 (`data/bc_runs/`, `data/seed_scripts/clone_late/`, `data/sweeps/tape_edit_20260831-*.csv`) that GitHub does not have.

Local venv for this work: `.venv-sub`, `kaggle_environments 1.32.7`, numpy 2.5.3.

## Submitted today

Two archives, both third-party Apache-2.0 imports, both carrying the same 13 x 719-turn route tapes.

| ref | bundle | what it is |
|---|---|---|
| 56142330 | `submission/e182/submission.tar.gz` | Dmitrii Gluzdov E182: Shop Router 0909 plus a seven-turn terminal collection planner |
| 56142332 | `submission/shop0909/submission.tar.gz` | Yusuke Hayashi Shop Router 0909, unmodified — the control |

Provenance and the exact hashes are in `docs/imported_public_agents.md`.
Ratings were not in yet when this was written.

## Measured, engine 1.32.7, this commit

Baseline, our own agent: `PYTHONPATH=. .venv-sub/bin/python -u scripts/build_planner_submission.py --out submission/main_own.py`
builds a 14,275-line bundle that banks **$137,491 vs `starter`** on the builder's own check.

Head-to-head, 8 seeds x both seats, `data/logs/own_vs_shop0909.csv`:

    PYTHONPATH=. .venv-sub/bin/python -u scripts/smoke_shop0909.py \
      --left submission/shop0909/main.py --right submission/main_own.py \
      --out data/logs/own_vs_shop0909.csv \
      --seeds 11 4242 70683142 244615642 1240813987 99114898 7 123456

**Shop Router 0909 beats our planner bundle 16/16, margins +$28,607 to +$38,827.**
Seeds 11, 4242, 70683142, 244615642, 1240813987, 99114898, 7, 123456.

E182 versus its own parent, `data/logs/smoke_shop0909.csv`: seed 11 identical play (the rescue does not fire, the +-180 is seat advantage), seed 4242 **+$5 in both seats**.
The terminal planner is real but tiny on these two seeds.

Ladder context, measured 2026-09-10: our best live score is **1924.0** (`main_diment_clone.py`, 2026-08-30); the two 2026-09-04 submissions scored 1409.5 and 1286.2.
Rank 2290 / 8493. Top of the ladder is SpaTaro at 3071.6; yhay81 himself sits rank 9 at 2958.2.
Deadline 2026-09-30.

## Not measured, do not quote as if it were

- No estimate of what either import will actually rate. The author's 2958.2 is **his live agent**, not this published artifact, and his tapes are public so the field can counter-tune them. `pilkwang/kaggriculture-structured-economic-policy` argues the fixed-schedule family "has reached its shelf life" and forked Kaito Fukami's v58 closed-loop agent instead.
- E182 versus 0909 on more than 2 seeds.
- Anything about win rate against the real ladder field. Local numbers here are one opponent.

## Next

1. Read the two ladder ratings when they settle and compare E182 against its control. That is the only clean read on whether the seven-turn rescue is worth carrying.
2. If the tapes rate near 2900, the question becomes the one `kaitofukami/238-238-known-streams-v58-minimax-closed-loop` answers: public-state best-response at a few checkpoints instead of a fixed stream. Disproof: if a v58-style fork rates no better than the plain 0909 tapes, then the counter-tuning story is wrong and the tapes are not the bottleneck.
3. `ashok205/top10-replay-dataset-archive` (2026-09-09) is fresh top-10 replay data for the clone pipeline in `scripts/bc_replay.py`.

## Untracked work in this checkout

`scripts/build_imported_submission.py` and `scripts/smoke_shop0909.py` are new source and are **not committed**.
`submission/` and `.venv-sub/` are build output.
