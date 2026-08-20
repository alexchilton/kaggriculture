#!/bin/bash
# Launch the BC round detached, with its own log, and return immediately.
#
# **Why this exists as a file.** The launch used to be written inline:
#
#     ssh alexr@box 'wsl bash -c "nohup bash box_bc_round0.sh > /home/alex/bc_run.log 2>&1 &"'
#
# PowerShell silently ate the `>` on the way through, so nohup ran with no redirect and the log
# never appeared -- `LAUNCHED` printed, and the next line said the file did not exist. CLAUDE.md
# names this: PowerShell eats `>`, `|`, `$(...)` and `VAR=value` out of command strings, so anything
# non-trivial goes in a script on the box.
#
# The whole call is now metacharacter-free:
#
#     ssh -i ~/.ssh/copilot_remote_ed25519 alexr@192.168.1.128 'wsl bash /home/alex/kagg2/scripts/box_launch_bc.sh'
set -u

LOG=/home/alex/bc_run.log
HERE="$(cd "$(dirname "$0")" && pwd)"

pkill -f box_bc_round0.sh 2>/dev/null
pkill -f build_bc_rows.py 2>/dev/null

: > "$LOG"
nohup setsid bash "$HERE/box_bc_round0.sh" >> "$LOG" 2>&1 < /dev/null &
echo "launched pid $! -> $LOG"
sleep 2
echo "--- first lines ---"
head -20 "$LOG"
