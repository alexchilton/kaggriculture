#!/usr/bin/env bash
# Stop the DAgger run that reset the bundle head, stamp the checkpoint, start again.
exec 2>&1
cd /home/alex/kaggriculture
export XLA_PYTHON_CLIENT_ALLOCATOR=platform

# `dagger_tap[e]` not `dagger_tape`: the literal string matches this script's own command line.
pkill -f "dagger_tap[e]" 2>/dev/null
sleep 4
pkill -9 -f "dagger_tap[e]" 2>/dev/null
sleep 2
tmux kill-session -t dag 2>/dev/null

echo "--- stamping the clone with its vocabulary and feature widths:"
.venv-cuda/bin/python -u scripts/stamp_checkpoint_provenance.py \
  --ckpt data/dagger_tape/towns64b-20260830-165514/offline_50epochs.pkl \
  --vocab data/il/bundle_vocab_kawa_s16.json 2>&1 \
  | grep -v -E "cuda_executor|Source Location|external/xla"

: > data/logs/kawa_dagger.log
tmux new-session -d -s dag "bash scripts/box_dagger_proper.sh 2>&1 | tee -a data/logs/kawa_dagger.log"
sleep 45

echo "--- dagger:"
ps -eo pid,etime,args | grep "dagger_tap[e]" || echo "  none"
echo "--- tmux:"
tmux ls
echo "--- log (the RESET line must be GONE):"
grep -v -E "cuda_executor|Source Location|external/xla|^    @ " data/logs/kawa_dagger.log | tail -20
