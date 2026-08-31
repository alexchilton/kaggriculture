#!/usr/bin/env bash
# DAgger, properly: the STUDENT drives and the teacher labels. Warm-started from the fitted clone.
#
# WHY THIS AND NOT MORE BC
# Every 1.0000 measured on 2026-08-30 -- 64 trained towns, the latch table, 8 exact held-out towns
# -- came from `where_does_day_zero_first_diverge.py`, which states in its own docstring that the
# TEACHER drives and the student is scored on the same board every turn. The clone has never been
# measured driving itself for a season. Confidence is not the gap: the clone puts a geometric-mean
# 0.99958 on the teacher's unit op and 0.99516 on the teacher's bundle. The gap is distribution
# shift -- one slip and every later decision is off the states those numbers were measured on.
# That is exactly what DAgger addresses and what plain BC cannot.
#
# The previous DAgger runs died three times on the vocabulary guard at dagger_tape.py:984, because a
# vocabulary sampled on 16 towns cannot express what the teacher trades on 64. The s16 vocabulary
# measured 0 misses over 46,016 turns of 64 towns, so the guard should hold -- but STUDENT states
# are off-distribution by construction, and the teacher may trade something there that no town in
# the sample ever produced. `--save-data-every 1` is not optional for that reason: if the guard does
# fire, the reservoir survives and the run resumes rather than restarting from nothing.
exec 2>&1
cd /home/alex/kaggriculture

# Bypasses XLA's BFC allocator, whose internal assertion aborted the RL run at 23:17 on an empty
# card. Memory allocation only; nothing about the algorithm changes.
export XLA_PYTHON_CLIENT_ALLOCATOR=platform

CKPT=data/dagger_tape/towns64b-20260830-165514/offline_50epochs.pkl
VOCAB=data/il/bundle_vocab_kawa_s16.json
test -s "$CKPT" || { echo "NO CLONE at $CKPT"; exit 1; }
test -s "$VOCAB" || { echo "NO VOCAB at $VOCAB"; exit 1; }

# `--anneal-after-agree 0.98`: beta only starts falling once greedy agreement on FRESH states is
# high. The clone is already there, so the anneal begins immediately -- which is the point. The
# run on 2026-08-29 that annealed from a weak checkpoint collapsed to greedy op 0.6000 in one
# round; annealing is not the thing that broke it, annealing too early was.
# `--expert-cap 60000` of `--aggregate-cap 200000`: teacher-driven states keep a reserved floor so
# a uniform reservoir cannot dilute them, while student states take the majority as beta falls.
echo "=== dagger starting $(date)   init $CKPT"
.venv-cuda/bin/python -u scripts/dagger_tape.py \
  --init "$CKPT" --vocab "$VOCAB" \
  --rounds 20 --episodes 8 --seeds 4 --holdout 8 --horizon 719 \
  --beta0 1.0 --anneal-after-agree 0.98 --anneal-rounds 8 \
  --lr 1e-4 --epochs 1 --batch-turns 512 \
  --aggregate-cap 200000 --expert-cap 60000 --bundle-alpha 1.0 --day0-repeat 8 \
  --playout 1 --d-model 128 --heads 4 --layers 3 \
  --seed 0 --tag kawa_dagger --save-data-every 1
echo "=== dagger exit=$? $(date)"
