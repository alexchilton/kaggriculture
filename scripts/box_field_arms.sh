#!/usr/bin/env bash
# Tape arm vs planner arm against the RECORDED FIELD, scored on win rate.
#
# The idle-opponent run gave the planner a +$15,483 median over 8 fresh seeds. Two reasons that is
# not yet a decision, both this project's own rules:
#   - an idle opponent contests no market, and every number measured that way runs ~2x reality
#     (the `starter` lesson in CLAUDE.md). The two arms sell on different cadences, so the gap
#     could be an artefact of an empty book.
#   - the ladder is Elo. Select on win rate, never money.
# `field_sweep.py` fixes both: real recorded ladder opponents who sell into the same book, both
# seatings, win rate reported per opponent.
exec 2>&1
cd /home/alex/kaggriculture

echo "=== field arms starting $(date)"
PYTHONPATH=. .venv/bin/python -u scripts/field_sweep.py \
  --flag REPLAY_OPENING_DAYS --values range:0,range:30 \
  --seeds 6 --opponents 24 --workers 14
echo "=== field arms exit=$? $(date)"
