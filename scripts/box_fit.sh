#!/bin/bash
# The fit stage, on its own, so it can be re-run WITHOUT rebuilding the rows.
#
#     bash scripts/box_fit.sh /home/alex/rows_r0b <vocab.json> /home/alex/bc_bundle.pkl
#
# `box_bc_round0.sh` opens with `rm -rf $ROWS`, so re-running the whole driver to retry a failed
# fit destroys 16 shards and 100 minutes of row building. That is why this is a separate file.
#
# **Why the two XLA settings below exist.** The first GPU fit died at 20:08:48 on 2026-08-20 with
# SIGABRT, exit 134, after the rows built cleanly:
#
#   E cuda_executor.cc:1348] Failed to allocate device memory of 12.00GiB: CUDA_ERROR_OUT_OF_MEMORY
#     ... backing off 12.00 -> 10.80 -> ... -> 4.18 GiB, every one refused
#   F bfc_allocator.cc:1063] Check failed: central_gap_ == kInvalidChunkHandle
#     (509 vs. 18446744073709551615) spatial partitioning expects one central gap
#
# with the abort raised under `xla::Autotuner::GetTunedConfig -> ConfigRunner::ProfileCandidate ->
# RedzoneAllocator::AllocateBytes -> BFCAllocator::Extend`. Two separate faults, one after the
# other:
#
#   PREALLOCATE   jax grabs 75% of VRAM in ONE block at startup. WSL2's CUDA refuses an allocation
#                 that large even with 15,872 MiB of 16,384 free -- measured free, by nvidia-smi,
#                 minutes after the crash, with nothing else on the card. The network is 914,363
#                 parameters at batch 256; it wants a few hundred MB, not twelve gigabytes.
#
#   AUTOTUNE      With the pool that thin, XLA's autotuner asked its redzone allocator for 8.23 GiB
#                 of profiling scratch, and BFC hit an internal CHECK instead of returning an
#                 error. A CHECK failure is an abort inside XLA -- no Python exception exists to
#                 catch it, so no amount of care in `fit_bc.py` could have survived it.
#
# Level 0 means "use the default algorithm, do not profile alternatives". It costs some matmul
# throughput on a model this small and removes the code path that aborted.
set -uo pipefail

ROWS=${1:?rows dir}
VOCAB=${2:?vocab json}
OUT=${3:?output pkl}

REPO=/home/alex/kaggriculture
CUDA=$REPO/.venv-cuda/bin/python
[ -x "$CUDA" ] || CUDA=$REPO/.venv/bin/python

export XLA_PYTHON_CLIENT_PREALLOCATE=false
export XLA_FLAGS="--xla_gpu_autotune_level=0"

cd "$REPO" || exit 1

echo "XLA_PYTHON_CLIENT_PREALLOCATE=$XLA_PYTHON_CLIENT_PREALLOCATE"
echo "XLA_FLAGS=$XLA_FLAGS"
/usr/lib/wsl/lib/nvidia-smi --query-gpu=memory.total,memory.used,memory.free --format=csv 2>/dev/null
# A real matmul before the long run. `jax.devices()` succeeds even when every allocation the
# compiler goes on to make will fail, so it is not evidence that the card is usable -- it printed
# `[CudaDevice(id=0)]` eight minutes before the abort. This allocates, compiles and executes.
$CUDA -c "
import jax, jax.numpy as jnp
print('jax devices:', jax.devices())
x = jnp.ones((4096, 4096), jnp.float32)
print('matmul ok:', float((x @ x)[0, 0]))
" 2>&1 | tail -3 || { echo "GPU SMOKE FAILED -- not starting the fit"; exit 1; }

$CUDA -u scripts/fit_bc.py --rows "$ROWS" --vocab "$VOCAB" \
    --out "$OUT" --epochs 3 --batch 256
code=$?

echo "fit exit=$code"
/usr/lib/wsl/lib/nvidia-smi --query-gpu=memory.used,memory.free --format=csv 2>/dev/null
exit $code
