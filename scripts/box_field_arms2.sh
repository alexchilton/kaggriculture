#!/usr/bin/env bash
# Replication of the tape-vs-planner field sweep on a FRESH seed range (1400-1405).
#
# Two reasons to re-run rather than trust the 1300-1305 table:
#   - it reported `mean ours` identical to the dollar (98,705) for both arms across 288 games each,
#     while per-opponent win rates swung 25% -> 100%. Those two cannot both be true. At 8 games the
#     columns differ normally (127,300 vs 109,680), so there is no structural bug -- but the
#     anomaly is unexplained and the shipping decision rests on this table.
#   - the standing rule: confirm a winner on a fresh draw. Seed variance here is ~15%.
exec 2>&1
cd /home/alex/kaggriculture
echo "=== field arms 2 starting $(date)"
PYTHONPATH=. .venv/bin/python -u scripts/field_sweep.py \
  --flag REPLAY_OPENING_DAYS --values range:0,range:30 \
  --seeds 6 --first-seed 1400 --opponents 24 --workers 14
echo "=== field arms 2 exit=$? $(date)"
