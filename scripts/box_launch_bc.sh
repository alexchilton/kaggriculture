#!/bin/bash
# Launch the BC round in a tmux session, with a log, and return immediately.
#
# **tmux rather than nohup.** The link to this box flaps -- WSL2 restarts and the Windows port proxy
# keeps the stale IP -- so a run has to survive a dropped connection AND be attachable afterwards to
# see what it is doing. nohup gives the first and not the second.
#
#     tmux attach -t bc          # watch it live
#     tmux capture-pane -pt bc   # last screenful without attaching
#     tail -f /home/alex/bc_run.log
#
# **Why the pipe lives in this file.** The whole call has to be metacharacter-free on the way in,
# because it crosses PowerShell:
#
#     ssh -i ~/.ssh/copilot_remote_ed25519 alexr@192.168.1.128 'wsl bash /home/alex/kaggriculture/scripts/box_launch_bc.sh'
#
# An inline launch lost its `>` in transit once already: nohup ran with no redirect, "LAUNCHED"
# printed, and the next line said the log did not exist.
set -u

SESSION=bc
LOG=/home/alex/bc_run.log
HERE="$(cd "$(dirname "$0")" && pwd)"

tmux kill-session -t "$SESSION" 2>/dev/null
pkill -f build_bc_rows.py 2>/dev/null
pkill -f box_bc_round0.sh 2>/dev/null

: > "$LOG"
tmux new-session -d -s "$SESSION" \
    "bash '$HERE/box_bc_round0.sh' 2>&1 | tee -a '$LOG'; echo; echo EXIT=\$?; sleep 86400"

echo "tmux session '$SESSION' started -> $LOG"
sleep 8
echo "--- first lines ---"
head -30 "$LOG"
echo "--- sessions ---"
tmux ls
