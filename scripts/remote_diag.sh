#!/usr/bin/env bash
# Why does JAX see the GPU in an interactive shell but not (or not survive) in a systemd service?
#
# Answers three things in one round trip, because each ssh round trip through PowerShell is a
# chance for another metacharacter to be eaten:
#   1. what the interactive environment actually contains
#   2. whether ptxas -- which XLA shells out to for every kernel -- is on PATH at all
#   3. whether JAX can compile a trivial GPU kernel under a *service-like* environment
#
# The third is the real test. CUDA initialising is not the same as CUDA being able to compile: the
# failing runs printed `devices: [CudaDevice(id=0)]` and then died at the first kernel build.
exec 2>&1
echo "=== interactive environment ==="
echo "PATH=$PATH"
echo "LD_LIBRARY_PATH=${LD_LIBRARY_PATH:-<unset>}"

echo
echo "=== ptxas / cuda toolkit ==="
command -v ptxas || echo "ptxas NOT on PATH"
ls -d /usr/local/cuda* 2>/dev/null || echo "no /usr/local/cuda*"
ls /usr/local/cuda/bin/ptxas 2>/dev/null || echo "no ptxas in /usr/local/cuda/bin"
python_bin=/home/alex/kagg-venv/bin/python
$python_bin -c "import nvidia, os, glob; p=os.path.dirname(nvidia.__file__); print('nvidia pip libs:', p); print(*sorted(os.listdir(p))[:12], sep=' ')" 2>/dev/null \
  || echo "no nvidia pip package"
find /home/alex/kagg-venv -name ptxas 2>/dev/null | head -3

echo
echo "=== JAX in an INTERACTIVE env ==="
$python_bin -c "
import jax, jax.numpy as jnp
print('devices:', jax.devices())
x = jnp.ones((512,512))
print('matmul ok:', float((x@x).sum()))
" 2>&1 | tail -5

echo
echo "=== JAX under a SERVICE-LIKE env (env -i, minimal PATH) ==="
env -i \
  PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  HOME=/home/alex \
  PYTHONPATH=/home/alex/kagg \
  XLA_PYTHON_CLIENT_PREALLOCATE=false \
  $python_bin -c "
import jax, jax.numpy as jnp
print('devices:', jax.devices())
x = jnp.ones((512,512))
print('matmul ok:', float((x@x).sum()))
" 2>&1 | tail -8
