#!/usr/bin/env bash
# Stop the tape-teacher DAgger run. The teacher is time-indexed (`TAPE[key][step]`), so annealing
# beta labels student states with the tape's t-th action rather than a recovery action -- which is
# the one thing DAgger exists to provide. Recorded in tape_teacher.py's own docstring.
exec 2>&1
cd /home/alex/kaggriculture
pkill -f "dagger_tap[e]" 2>/dev/null
sleep 4
pkill -9 -f "dagger_tap[e]" 2>/dev/null
sleep 2
tmux kill-session -t dag 2>/dev/null
echo "--- still running?"
ps -eo pid,etime,args | grep "dagger_tap[e]" || echo "  none"
echo "--- run dir kept:"
ls -l data/dagger_tape/kawa_dagger-20260831-083332/ 2>/dev/null || echo "  (no files written yet)"
