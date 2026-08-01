#!/usr/bin/env bash
# Does JAX-on-GPU work *inside a systemd unit*, as opposed to inside a login shell?
#
# The previous diagnostic ruled out the environment: a stripped `env -i` shell still gets
# `CudaDevice(id=0)` and compiles a matmul. What it did not test is the thing that actually differs
# -- systemd runs the process in its own cgroup, with its own device policy. WSL exposes the GPU
# through /dev/dxg, and a unit that cannot open it will initialise CUDA (the driver shim loads) and
# then die when it first tries to build a kernel. That is exactly the observed failure.
exec 2>&1
PY=/home/alex/kagg-venv/bin/python

echo "=== /dev/dxg ==="
ls -l /dev/dxg 2>/dev/null || echo "no /dev/dxg"
id alex

echo
echo "=== JAX inside a transient systemd unit ==="
sudo systemd-run --unit=jaxprobe --uid=alex --wait --collect \
  --setenv=PYTHONPATH=/home/alex/kagg \
  --setenv=XLA_PYTHON_CLIENT_PREALLOCATE=false \
  --property=StandardOutput=file:/tmp/jaxprobe.log \
  --property=StandardError=file:/tmp/jaxprobe.log \
  $PY -c "
import jax, jax.numpy as jnp
print('devices:', jax.devices())
x = jnp.ones((512,512))
print('matmul ok:', float((x@x).sum()))
" 2>&1 | tail -5
echo "--- probe output ---"
cat /tmp/jaxprobe.log 2>/dev/null | tail -20
