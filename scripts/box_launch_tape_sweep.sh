#!/usr/bin/env bash
exec 2>&1
cd /home/alex/kaggriculture
tmux kill-session -t sweep 2>/dev/null
sleep 2
mkdir -p data/sweeps
: > data/logs/tape_sweep.log
tmux new-session -d -s sweep "bash scripts/box_tape_sweep.sh 2>&1 | tee -a data/logs/tape_sweep.log"
sleep 45
echo "--- workers:"
ps -eo pid,args | grep -c "tape_edit_swee[p]"
echo "--- tmux:"
tmux ls
echo "--- log:"
cat data/logs/tape_sweep.log
echo "--- csv rows so far:"
wc -l data/sweeps/tape_edit_*.csv 2>/dev/null | tail -3 || echo "  none yet"
