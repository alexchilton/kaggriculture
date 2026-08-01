#!/usr/bin/env bash
# Report whether training is alive, what the GPU is doing, and the newest checkpoint.
#
# A file rather than an ssh command string because `$(...)` in a command string is expanded by
# PowerShell on the way through, which turned `$(cat /home/alex/kagg/data/train.pid)` into a lookup
# of `C:\home\alex\kagg\data\train.pid`.
exec 2>&1
cd /home/alex/kagg || exit 1

PID=data/train.pid
echo "=== process ==="
if [ -f "$PID" ] && kill -0 "$(cat "$PID")" 2>/dev/null; then
  pid=$(cat "$PID")
  echo "RUNNING pid $pid, up $(ps -o etime= -p "$pid" | tr -d ' ')"
else
  echo "NOT RUNNING"
fi
# Catch any run that was started outside this launcher, so a stale process cannot hide.
echo "python procs: $(pgrep -fc 'python.*train_jax_rl' 2>/dev/null || echo 0)"

echo "=== gpu ==="
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader

echo "=== newest checkpoints ==="
ls -lt data/jax_rl_runs/*/latest.pkl 2>/dev/null | head -3 || echo "none"

echo "=== ram / swap ==="
free -m | head -3

# A run that dies with no Python traceback was almost certainly killed by the kernel, not by an
# exception. XLA compilation of the rollout scan is the memory-hungry phase, and it happens before
# the first update prints -- so "the log stops mid-startup" and "the OOM killer fired" look
# identical from the outside. Check rather than infer.
echo "=== recent OOM kills ==="
dmesg 2>/dev/null | grep -iE 'killed process|out of memory' | tail -3 || echo "  (dmesg unavailable)"

echo "=== last log lines ==="
tail -12 data/logs/run.log 2>/dev/null || echo "no log yet"
