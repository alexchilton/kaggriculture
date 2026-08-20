#!/bin/bash
# Start the BC round and the GPU install in two separate tmux sessions, and return.
#
# Two sessions rather than one script, because they must not block each other: the row build is
# 16 shards of CPU work and the install is a long download. They touch different environments --
# rows run on `.venv`, the install only writes `.venv-cuda` -- so they are safe in parallel.
#
#     ssh -i ~/.ssh/copilot_remote_ed25519 alexr@192.168.1.128 'wsl bash /home/alex/kaggriculture/scripts/box_launch_both.sh'
#
# Everything non-trivial lives here rather than in that command line, because it crosses PowerShell
# and PowerShell silently removes `>`, `|`, `$(...)` and `&&`.
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
BC_LOG=/home/alex/bc_run.log
GPU_LOG=/home/alex/jax_gpu_install.log

for s in bc jaxgpu; do tmux kill-session -t "$s" 2>/dev/null; done
pkill -f build_bc_rows.py 2>/dev/null
pkill -f box_bc_round0.sh 2>/dev/null

: > "$BC_LOG"
: > "$GPU_LOG"

tmux new-session -d -s bc \
    "bash '$HERE/box_bc_round0.sh' 2>&1 | tee -a '$BC_LOG'; echo EXIT=\$?; sleep 86400"
tmux new-session -d -s jaxgpu \
    "bash '$HERE/box_install_jax_gpu.sh' 2>&1 | tee -a '$GPU_LOG'; echo EXIT=\$?; sleep 86400"

echo "started:  bc -> $BC_LOG"
echo "          jaxgpu -> $GPU_LOG"
sleep 10
echo
echo "=== bc, first lines ==="
head -25 "$BC_LOG"
echo
echo "=== jaxgpu, first lines ==="
head -12 "$GPU_LOG"
echo
tmux ls
