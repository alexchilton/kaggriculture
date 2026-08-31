#!/usr/bin/env bash
exec 2>&1
cd /home/alex/kaggriculture
tmux kill-session -t field2 2>/dev/null
sleep 2
: > data/logs/field_arms2.log
tmux new-session -d -s field2 "bash scripts/box_field_arms2.sh 2>&1 | tee -a data/logs/field_arms2.log"
sleep 30
echo "--- workers:"
ps -eo pid,args | grep -c "field_swee[p]"
echo "--- ps:"
ps -eo pid,etime,pcpu,args | grep "field_swee[p]" | head -3 || echo "  none"
echo "--- tmux:"
tmux ls
echo "--- log:"
cat data/logs/field_arms2.log
