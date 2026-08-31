#!/usr/bin/env bash
# Launch the DAgger run in tmux. A script file, not an inline ssh string: a multi-line inline
# command was flattened to one line by the transport on 2026-08-30 and every `;`-separated stage
# after the first silently became an argument to `echo`.
exec 2>&1
cd /home/alex/kaggriculture

# `train_jax_r[l]` not `train_jax_rl`: the literal pattern matches the shell's OWN command line, so
# `pkill -f` kills the session running it. That has now happened four times in this project.
pkill -f "train_jax_r[l]" 2>/dev/null
sleep 4
pkill -9 -f "train_jax_r[l]" 2>/dev/null
sleep 2
tmux kill-session -t rl 2>/dev/null
tmux kill-session -t dag 2>/dev/null

: > data/logs/kawa_dagger.log
tmux new-session -d -s dag "bash scripts/box_dagger_proper.sh 2>&1 | tee -a data/logs/kawa_dagger.log"
sleep 45

echo "--- rl still alive?"
ps -eo pid,etime,args | grep "train_jax_r[l]" || echo "  none"
echo "--- dagger:"
ps -eo pid,etime,args | grep "dagger_tap[e]" || echo "  none"
echo "--- tmux:"
tmux ls
echo "--- log:"
grep -v -E "cuda_executor|Source Location|external/xla|^    @ " data/logs/kawa_dagger.log | tail -25
