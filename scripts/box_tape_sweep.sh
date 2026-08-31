#!/usr/bin/env bash
# Search over single edits to the tape itself -- the only genotype that is live in the shipped arm.
#
# WHY THE TAPE AND NOT THE SCHEDULE. Of the 18 per-day schedule keys, exactly two change what the
# agent ships while `REPLAY_OPENING_DAYS = tuple(range(30))`: `animals_bought` (via the persisted
# `state["herd_split"]`, read at schedule_agent.py:6066) and `plants` (the BUY_SEED trim at :6163,
# and only when neither branch is armed). Every other key feeds `live = agent(obs)`, which
# `replayed()` computes each turn and discards -- the four tapes cover all 720 steps with 0 missing
# frames on every latch state, so `if step not in opening: return live` never fires. Sweeping
# `hires`, `land`, `builds`, `seeds` or `sells` in this arm returns byte-identical seasons.
#
# The arms below are the ones whose docstrings record them as UNTESTED or as the largest untested
# swing, not the carrot/tomato ones already measured negative:
#   herd_*    "_herd_split reads the shop draw and never farms[1 - me] ... the untested axis with
#             the largest measured price swing"
#   cow_d0/4  deciding the split at d0 rather than d8, when there is still herd left to buy
#   topup_*   add an order at hour h without moving his cadence (the sell_h* arms lose because
#             they MOVE the day's sale and the rest goes unoffered)
#
# Scored on MARGIN (ours - theirs) and wins, which the script already does -- the tomato arm was
# +$4,846 on our own bank and -$5,546 on margin, because thinning the wheat book lifts the price
# for an opponent who sells more wheat than we do. The ladder is Elo.
exec 2>&1
cd /home/alex/kaggriculture

STAMP=$(date +%Y%m%d-%H%M%S)
echo "=== tape sweep starting $(date)"
.venv/bin/python -u scripts/tape_edit_sweep.py \
  --seeds 11 42 7 899 1337 4096 13001 60013 \
  --arms control herd_cow_d8 herd_sheep_d8 herd_counter_d8 herd_book_d8 \
         herd_counter_d12 herd_book_d12 cow_d0 cow_d4 \
         topup_h12_all topup_h16_all topup_h16_d20 topup_h20_all \
  --opponents kawashigi kawashigi_b3 \
  --weeds 0.005 --jobs 14 \
  --out "data/sweeps/tape_edit_$STAMP.csv"
echo "=== tape sweep exit=$? $(date)"
