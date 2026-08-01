#!/usr/bin/env bash
# Start a long training run ON the box, fully detached from the SSH session.
#
# `nohup ... &` is not sufficient here. The command arrives as
# ssh -> PowerShell -> `wsl bash -c ...`, and when that wsl invocation returns, the session's
# process group is torn down and takes the background child with it -- the run dies seconds after
# launch, leaving an empty log and an idle GPU, which is exactly what happened.
#
# `setsid` puts the process in its own session with no controlling terminal, so it survives. stdin
# is redirected from /dev/null so it can never block waiting on a terminal that no longer exists.
exec 2>&1
cd /home/alex/kagg || exit 1
mkdir -p data/logs

export PYTHONPATH=/home/alex/kagg
export XLA_PYTHON_CLIENT_PREALLOCATE=false

LOG=/home/alex/kagg/data/logs/run.log
PID=/home/alex/kagg/data/train.pid

# Keep the previous run's log rather than truncating it: comparing a failed run against the one
# before it is most of debugging, and `>` would have silently destroyed the evidence.
if [ -s "$LOG" ]; then
  mv "$LOG" "data/logs/run-$(date +%Y%m%d-%H%M%S).log"
fi

setsid /home/alex/kagg-venv/bin/python -u scripts/train_jax_rl.py "$@" \
    < /dev/null > "$LOG" 2>&1 &
echo $! > "$PID"

sleep 3
if kill -0 "$(cat "$PID")" 2>/dev/null; then
  echo "launched pid $(cat "$PID") -- log: $LOG"
else
  echo "FAILED to launch; log follows:"
  cat "$LOG"
  exit 1
fi
