#!/usr/bin/env bash
# Tape arm vs planner arm, SAME fixed seeds. Step 1a's first command.
#
# WHY: `docs/fable_after_the_bc_ceiling_2026-08-31.md` built its step 1a on a $3,402 gap between a
# "tape $147,368" and a "planner $143,966". Both of those are the PLANNER arm. $147,368 is recorded
# in four places (schedule_agent.py:4063, does_the_net_market_survive_the_sell_override.py:11,
# submission/main_sell_h16_d26.py:11009, and the shed test) as REPLAY_OPENING_DAYS = (), 3 seeds,
# idle opponent, 2026-08-28. $143,966 carries no recorded conditions at all. So the gap the plan
# opens with has never been measured, and this is the measurement.
#
# Fresh seeds from 9000 on purpose: the ladder hands out seeds the four tapes have never seen, and
# that is the condition where a time-indexed replay and a board-reading planner should diverge most.
exec 2>&1
cd /home/alex/kaggriculture
export XLA_PYTHON_CLIENT_ALLOCATOR=platform

echo "=== two arms starting $(date)"
.venv/bin/python -u scripts/can_the_teacher_play_a_seed_it_has_never_seen.py \
  --seeds 8 --turns 719 --base-seed 9000
echo "=== two arms exit=$? $(date)"
