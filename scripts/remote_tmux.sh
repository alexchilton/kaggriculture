#!/usr/bin/env bash
# Start training inside tmux, which is the launch context that actually works on this box.
#
# Measured, with identical arguments:
#   foreground over ssh  -> enters the training loop, 413 turns/s, clean exit
#   systemd service      -> dies before `params:` prints, no log.jsonl, exit code 0
#   systemd + tiny GPU op-> fine
#
# So it is not the code, the args, the environment, the cgroup or memory. What foreground has and a
# service does not is a **pty**, and WSL2 routes GPU work through the Windows driver in a way that
# appears to depend on a real session. tmux keeps a pty alive after the SSH connection drops, which
# gives the working context *and* persistence -- the property `nohup`, `setsid` and systemd all
# failed to provide here for different reasons.
exec 2>&1
SESSION=kagg
cd /home/alex/kagg || exit 1
mkdir -p data/logs

tmux kill-session -t $SESSION 2>/dev/null
pkill -9 -f 'python.*train_jax_rl' 2>/dev/null
sleep 2

# `pipe-pane` mirrors everything the pty sees into a file, so the log is readable from outside
# without attaching -- and unlike a redirect it cannot be defeated by Python's stdout buffering.
tmux new-session -d -s $SESSION -c /home/alex/kagg \
  "PYTHONPATH=/home/alex/kagg XLA_PYTHON_CLIENT_PREALLOCATE=false \
   /home/alex/kagg-venv/bin/python -u scripts/train_jax_rl.py $*"
tmux pipe-pane -t $SESSION -o "cat >> /home/alex/kagg/data/logs/run.log"

sleep 5
echo "tmux sessions:"
tmux ls
echo "--- first output ---"
tail -6 /home/alex/kagg/data/logs/run.log 2>/dev/null || echo "(nothing yet)"
