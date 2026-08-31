#!/usr/bin/env bash
# RL from the fitted kawa clone. The fit and the held-out replay are already done -- re-running
# them costs 40 minutes and reproduces files that exist.
#
# `--batch 504` not 512: the trainer requires batch % n_phases == 0 and n_phases defaults to 12.
# 512 fails the check four seconds in, after the model and the rollout buffer are already built.
# 504 = 12 x 42, which is the grouping the trainer itself prints.
exec 2>&1
cd /home/alex/kaggriculture

# XLA's BFC allocator aborted this run at 23:17:32 on 2026-08-30, ~90s into compiling the first
# rollout scan:
#   F bfc_allocator.cc:1063] Check failed: central_gap_ == kInvalidChunkHandle (472 vs ...)
#   spatial partitioning expects one central gap
# That is an internal assertion in the allocator, not an out-of-memory: the card was measured empty
# at the time (0 MiB of 16,384 used, no compute apps, 50 C) and the run's own estimate was
# 1.30 GiB activations + 1.71 GiB rollout buffer. `platform` uses cudaMalloc directly and never
# builds BFC's chunk map, so the assertion cannot fire. It changes memory allocation only --
# nothing about the algorithm, the batch or the reward.
export XLA_PYTHON_CLIENT_ALLOCATOR=platform

CKPT=data/dagger_tape/towns64b-20260830-165514/offline_50epochs.pkl
VOCAB=data/il/bundle_vocab_kawa_s16.json
test -s "$CKPT" || { echo "NO CHECKPOINT at $CKPT"; exit 1; }

# `--gamma-per-day 1.0` and `--shaping-coef 0`: the settled position is a TERMINAL reward,
# win 1 / loss 0 / draw 0.5, undiscounted. The trainer defaults to 0.97, so gamma must be passed
# or the run silently discounts.
# `--vocab` explicitly: the default is the 197-entry DEFAULT_VOCAB and this checkpoint's bundle
# head is indexed against the 164-entry s16 vocabulary. Mismatched, every index is still a valid
# index and nothing raises -- it just decodes a different order than the one the head chose.
# No `--kl-prior`: `--init` already starts from the clone, and the `--init` docstring argues
# against anchoring to the same checkpoint you warm-started from.
echo "=== rl starting $(date)   init $CKPT"
.venv-cuda/bin/python -u scripts/train_jax_rl.py \
  --init "$CKPT" --vocab "$VOCAB" \
  --gamma-per-day 1.0 --shaping-coef 0 \
  --d-model 128 --heads 4 --layers 3 \
  --batch 504 --updates 2000 --ckpt-every 25 --seed 0 --tag rl_kawa
echo "=== rl exit=$? $(date)"
