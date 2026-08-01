#!/usr/bin/env bash
# Kill every training/benchmark process on the box, then report what the GPU and RAM look like.
#
# Runs ON the box, as a file, because the command line cannot carry this safely: PowerShell reads
# `[t]` as an array index, and a bare `pkill -f train_jax_rl` matches the very shell running it and
# kills itself before printing anything. Both happened.
#
# This exists because a cancelled SSH command does **not** stop the remote process. Ten training
# runs accumulated that way -- one per attempt -- each holding 1.5-2.2 GB on a 13 GB box, until
# everything OOMed and nothing could compile. Any launcher should call this first.
exec 2>&1

# `pgrep -f` on a pattern that cannot match this script: match the python entry point specifically.
pids=$(pgrep -f 'python.*train_jax_rl' || true)
pids="$pids $(pgrep -f 'python.*gpu_bench' || true)"
pids=$(echo $pids | tr ' ' '\n' | grep -v '^$' | grep -v "^$$\$" | sort -u | tr '\n' ' ')

if [ -n "${pids// /}" ]; then
  echo "killing: $pids"
  kill -9 $pids 2>/dev/null
  sleep 4
else
  echo "nothing to kill"
fi

echo "remaining: $(pgrep -fc 'python.*train_jax_rl' || echo 0)"
echo "--- gpu ---"
nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader
echo "--- ram ---"
free -g | head -2
