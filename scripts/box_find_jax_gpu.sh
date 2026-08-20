#!/bin/bash
# Find every Python environment on the box and report what jax it has, and whether that jax can see
# the GPU. Read-only: it starts nothing and kills nothing, so it is safe while a run is going.
#
# **Why look before installing.** `.venv-cuda` is named as though it is the GPU environment and is
# not -- it prints "An NVIDIA GPU may be present on this machine, but a CUDA-enabled jaxlib is not
# installed. Falling back to cpu." Installing over the top of the wrong environment is how the vLLM
# venv gets broken, and its torch 2.11.0+cu126 is ABI-linked to a compiled extension that must not
# be upgraded (CLAUDE.md).
#
# Importing jax is what settles it. `pip list` shows a package; only `jax.devices()` shows a
# backend that actually loads, and the plugin can be installed and still fail on a driver mismatch.
set -u

echo "=== driver / GPU ==="
nvidia-smi --query-gpu=name,driver_version,memory.total,clocks.sm,clocks.max.sm \
    --format=csv,noheader 2>&1 | head -3

echo
echo "=== CUDA toolkits ==="
ls -d /usr/local/cuda* 2>/dev/null

echo
echo "=== python environments ==="
# Depth-limited: a full scan of $HOME walks the model caches and takes minutes.
# NOT `-type f`: a venv's bin/python3 is a symlink to the interpreter, so the first version of this
# matched nothing at all and printed an empty section, which reads exactly like "no environments".
for py in $(find /home/alex -maxdepth 5 -name 'python3' -path '*/bin/*' 2>/dev/null | sort -u); do
    env_dir=$(dirname "$(dirname "$py")")
    echo
    echo "--- $env_dir"
    "$py" -c "
import sys
try:
    import jax, jaxlib
except Exception as exc:
    print('   jax: not installed (%s)' % type(exc).__name__)
    sys.exit()
print('   jax %s   jaxlib %s' % (jax.__version__, jaxlib.__version__))
try:
    devs = jax.devices()
    print('   devices: %s' % devs)
    print('   BACKEND: %s' % ('GPU' if any(d.platform == 'gpu' for d in devs) else 'cpu'))
except Exception as exc:
    print('   devices FAILED: %s' % exc)
" 2>&1 | grep -v "^$" | grep -viE "^(warning|an nvidia gpu may be present)" | head -8
    # The plugin packages are the tell for what an install would need to change.
    "$py" -m pip list 2>/dev/null | grep -iE "^(jax|jaxlib|jax-cuda|nvidia-cuda|torch)" | head -8 \
        | sed 's/^/   pip: /'
done

echo
echo "=== done ==="
