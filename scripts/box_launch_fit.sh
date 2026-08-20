#!/bin/bash
# Launch the fit stage ALONE in tmux, with a log, and return immediately.
#
# Same reasoning as `box_launch_bc.sh`: tmux rather than nohup, because the link to this box flaps
# and a run has to survive a dropped connection AND stay attachable. The pipe lives in this file
# because the launch crosses PowerShell, which eats `>` and `|` in transit without a word.
#
#     tmux attach -t fit
#     tail -f /home/alex/fit_run.log
set -u

SESSION=fit
LOG=/home/alex/fit_run.log
REPO=/home/alex/kaggriculture
ROWS=/home/alex/rows_r0b
VOCAB=$REPO/data/il/bundle_vocab.json
OUT=/home/alex/bc_bundle.pkl

n=$(ls "$ROWS"/*.npz 2>/dev/null | wc -l)
[ "$n" = "16" ] || { echo "EXPECTED 16 row shards in $ROWS, found $n -- refusing to start"; exit 1; }

tmux kill-session -t "$SESSION" 2>/dev/null
pkill -f fit_bc.py 2>/dev/null

: > "$LOG"
tmux new-session -d -s "$SESSION" \
    "bash '$REPO/scripts/box_fit.sh' '$ROWS' '$VOCAB' '$OUT' 2>&1 | tee -a '$LOG'; echo; echo EXIT=\$?; sleep 86400"

echo "tmux session '$SESSION' started -> $LOG   ($n row shards)"
sleep 25
echo "--- first lines ---"
head -20 "$LOG"
