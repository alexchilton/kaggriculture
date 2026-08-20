#!/bin/bash
# Install a CUDA-capable jax into `.venv-cuda`, and prove it sees the GPU.
#
# **Why it is needed.** `.venv-cuda` is named as though it is the GPU environment and is not: it
# prints "An NVIDIA GPU may be present on this machine, but a CUDA-enabled jaxlib is not installed.
# Falling back to cpu." A sweep of every environment on the box (`box_find_jax_gpu.sh`, 2026-08-20)
# found jax in NO other environment either -- sana, sglang, sglang2, tq_pytorch, turboquant and
# vllm are all torch. So there is nothing to reuse and this is a fresh install, not a repair.
#
# **`.venv-cuda` and nothing else.** `vllm_env` holds torch 2.11.0+cu126 that is ABI-linked to the
# vLLM 0.23.0 compiled extension and must not be upgraded (CLAUDE.md). This script never touches it.
# The CPU `.venv` is left alone too: the 16 row workers run there and a half-swapped environment
# would break a run in progress.
#
# `jax[cuda12]` pulls its own CUDA libraries as wheels, so it does not care which of the box's
# toolkits (/usr/local/cuda-12.6, /usr/local/cuda-13.0) is on the path.
set -uo pipefail

VENV=/home/alex/kaggriculture/.venv-cuda
PY=$VENV/bin/python

echo "=== before ==="
$PY -V
$PY -c "import jax, jaxlib; print('jax', jax.__version__, 'jaxlib', jaxlib.__version__)" 2>&1 | tail -1
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader 2>&1 | head -1

echo
echo "=== installing jax[cuda12] ==="
$PY -m pip install --upgrade "jax[cuda12]" 2>&1 | tail -25

echo
echo "=== after ==="
# The import is the test. `pip list` shows a package; only `jax.devices()` shows a backend that
# actually loads, and a plugin can install cleanly and still fail on a driver mismatch.
$PY -c "
import jax, jaxlib
print('jax', jax.__version__, 'jaxlib', jaxlib.__version__)
devs = jax.devices()
print('devices:', devs)
gpu = [d for d in devs if d.platform == 'gpu']
print('BACKEND:', 'GPU' if gpu else 'cpu')
if gpu:
    import jax.numpy as jnp, time
    x = jnp.ones((4096, 4096))
    (x @ x).block_until_ready()
    t = time.time()
    for _ in range(20):
        y = (x @ x)
    y.block_until_ready()
    el = time.time() - t
    print('4096^3 matmul x20: %.2fs  (%.0f GFLOP/s)' % (el, 20 * 2 * 4096**3 / el / 1e9))
" 2>&1 | tail -12

echo
echo "=== the CPU venv is untouched ==="
/home/alex/kaggriculture/.venv/bin/python -c "import jax; print('cpu venv jax', jax.__version__)" 2>&1 | tail -1
echo "=== done ==="
