#!/usr/bin/env bash
# Launch the two-arm comparison in tmux. A script file, not an inline ssh string.
exec 2>&1
cd /home/alex/kaggriculture
tmux kill-session -t arms 2>/dev/null
: > data/logs/two_arms.log
tmux new-session -d -s arms "bash scripts/box_two_arms.sh 2>&1 | tee -a data/logs/two_arms.log"
sleep 30
echo "--- ps:"
ps -eo pid,etime,pcpu,args | grep "can_the_teacher_play_a_seed_it_has_never_see[n]" || echo "  none"
echo "--- tmux:"
tmux ls
echo "--- log:"
grep -v -E "cuda_executor|Source Location|external/xla|^    @ " data/logs/two_arms.log | tail -20
