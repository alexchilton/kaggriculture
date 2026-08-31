#!/usr/bin/env bash
# offline fit (early-stopped, checkpointed) -> held-out replay -> RL. One chain, no hand-offs.
#
# Replaces the fit/test tail of `full_chain.sh`, which had two defects this run exposed:
#   1. the fitter wrote its weights ONLY at epoch 400, so a crash at 399 cost the whole 4 hours;
#   2. line 34 hardcoded `offline_400epochs.pkl`, which early stopping does not produce.
# The checkpoint is now globbed, not named, and the fitter stops when agreement reaches --target.
exec 2>&1
cd /home/alex/kaggriculture

RUN=data/dagger_tape/towns64b-20260830-165514
VOCAB=data/il/bundle_vocab_kawa_s16.json

echo "=== fit starting $(date)"
.venv-cuda/bin/python -u scripts/does_movement_ever_leave_zero.py \
  --run "$RUN" --epochs 400 --every 25 --target 1.0 --patience 4
echo "=== fit exit=$? $(date)"

# Globbed, never named: the file carries the epoch the BEST weights came from, and early stopping
# means that is not --epochs.
CKPT=$(ls -t "$RUN"/offline_*epochs.pkl 2>/dev/null | head -1)
test -s "$CKPT" || { echo "NO FITTED CHECKPOINT in $RUN -- stopping"; exit 1; }
echo "=== ckpt $CKPT"

echo "=== held-out replay $(date)"
.venv-cuda/bin/python -u scripts/where_does_day_zero_first_diverge.py \
  --ckpt "$CKPT" --days 12 --episodes 13 --rng 777
echo "=== held-out exit=$? $(date)"

# `--gamma-per-day 1.0` and `--shaping-coef 0`: the settled position is a TERMINAL reward,
# win 1 / loss 0 / draw 0.5, undiscounted. The trainer's defaults are 0.97 and 0.0, so gamma must
# be passed explicitly or the run silently discounts.
# `--vocab` explicitly for the same reason: the default is the 197-entry DEFAULT_VOCAB, and the
# bundle head in this checkpoint is indexed against the 164-entry s16 vocabulary. Mismatched, every
# index is still a valid index and nothing fails -- it just decodes the wrong order.
echo "=== rl starting $(date)"
.venv-cuda/bin/python -u scripts/train_jax_rl.py \
  --init "$CKPT" --vocab "$VOCAB" \
  --gamma-per-day 1.0 --shaping-coef 0 \
  --d-model 128 --heads 4 --layers 3 \
  --batch 504 \

  --updates 2000 --ckpt-every 25 --seed 0 --tag rl_kawa
echo "=== rl exit=$? $(date)"
echo "=== ALL DONE $(date)"
