#!/usr/bin/env bash
exec 2>&1
cd /home/alex/kaggriculture
tmux kill-session -t field 2>/dev/null
: > data/logs/field_arms.log
tmux new-session -d -s field "bash scripts/box_field_arms.sh 2>&1 | tee -a data/logs/field_arms.log"
sleep 30
echo "--- ps:"
ps -eo pid,etime,pcpu,args | grep "field_swee[p]" | head -4 || echo "  none"
echo "--- workers:"
ps -eo pid,args | grep -c "field_swee[p]"
echo "--- tmux:"
tmux ls
echo "--- log:"
cat data/logs/field_arms.log
