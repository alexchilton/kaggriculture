#!/bin/bash
# One DAgger round, end to end: roll the student, label with the planner, rebuild rows, continue
# the fit, gate in the real environment.
#
#     bash scripts/dagger_round.sh 1 /home/alex/bc_bundle.best.pkl
#
# **The four steps are one script because they have to agree about three things** -- the vocabulary,
# the round's label directory, and which checkpoint is the parent -- and every time one of those was
# passed by hand this week it was passed wrong. The vocabulary especially: it is not rebuilt here,
# it is INHERITED, because a vocabulary rebuilt from round N's labels would renumber every bundle
# and silently invalidate the checkpoint being continued. `fit_bc --init` refuses a size mismatch
# for the same reason.
#
# **Rounds accumulate; they do not replace.** The fit reads round 0's rows AND every later round's,
# because DAgger's guarantee comes from fitting the union of all states visited so far. Training on
# round N alone lets the student forget what round 0 taught and oscillate.
set -uo pipefail

ROUND=${1:?usage: dagger_round.sh <round> <parent-checkpoint>}
PARENT=${2:?usage: dagger_round.sh <round> <parent-checkpoint>}

REPO=/home/alex/kaggriculture
VENV=$REPO/.venv/bin/python
CUDA=$REPO/.venv-cuda/bin/python
[ -x "$CUDA" ] || CUDA=$VENV
VOCAB=$REPO/data/il/bundle_vocab.json
LABELS=/home/alex/labels_r$ROUND
ROWS=/home/alex/rows_r$ROUND
ALLROWS=/home/alex/rows_all
OUT=/home/alex/bc_r$ROUND.pkl
GAMES=${GAMES:-10}          # per worker
WAVE=${WAVE:-4}             # concurrency; 16 at once is what the OOM killer took last time

say() { echo; echo "=== $* ===  $(date '+%H:%M:%S')"; }
cd "$REPO" || exit 1

say "round $ROUND  parent $PARENT"
ls -la "$PARENT" || { echo "no parent checkpoint"; exit 1; }

say "1/4 roll the student, label with the planner"
rm -rf "$LABELS"; mkdir -p "$LABELS"
fail=0
for start in $(seq 0 "$WAVE" 15); do
    pids=()
    for w in $(seq "$start" $((start + WAVE - 1))); do
        [ "$w" -gt 15 ] && continue
        $VENV -u scripts/dagger_planner.py --checkpoint "$PARENT" --games "$GAMES" \
            --worker "$w" --out "$LABELS" --beta 0.0 --seed-base $((1000000 * (ROUND + 1))) \
            > "/home/alex/dag${ROUND}_w$w.log" 2>&1 &
        pids+=($!)
    done
    for p in "${pids[@]}"; do wait "$p" || fail=1; done
    echo "  wave $start done (fail=$fail)  $(date '+%H:%M:%S')"
done
[ "$fail" != "0" ] && { echo "A ROLLOUT WORKER FAILED"; for w in 0 1 2 3; do tail -6 "/home/alex/dag${ROUND}_w$w.log"; done; exit 1; }
wc -l "$LABELS"/*.jsonl | tail -1

# How often did the student win, and how often did it raise? Printed here because these are the two
# numbers that say whether the round's states are worth learning from at all.
say "rollout summary"
grep -h "student won" /home/alex/dag${ROUND}_w*.log
grep -h "student errors" /home/alex/dag${ROUND}_w*.log | head -3

say "2/4 build rows (vocabulary INHERITED, not rebuilt)"
rm -rf "$ROWS"; mkdir -p "$ROWS"
for start in $(seq 0 "$WAVE" 15); do
    pids=()
    for w in $(seq "$start" $((start + WAVE - 1))); do
        [ "$w" -gt 15 ] && continue
        $VENV -u scripts/build_bc_rows.py --shards "$LABELS" --vocab "$VOCAB" \
            --out "$ROWS" --only "$w" > "/home/alex/dagrows${ROUND}_w$w.log" 2>&1 &
        pids+=($!)
    done
    for p in "${pids[@]}"; do wait "$p" || fail=1; done
done
[ "$fail" != "0" ] && { echo "A ROW WORKER FAILED"; exit 1; }

# Symlinks rather than copies: the rows are hundreds of MB a round and the fit only reads them.
say "3/4 fit, continuing from the parent"
mkdir -p "$ALLROWS"
for f in /home/alex/rows_r0b/*.npz; do ln -sf "$f" "$ALLROWS/r0_$(basename "$f")"; done
for r in $(seq 1 "$ROUND"); do
    for f in /home/alex/rows_r$r/*.npz; do
        [ -e "$f" ] && ln -sf "$f" "$ALLROWS/r${r}_$(basename "$f")"
    done
done
ls "$ALLROWS" | wc -l

$CUDA -u scripts/fit_bc.py --rows "$ALLROWS" --vocab "$VOCAB" --init "$PARENT" \
    --out "$OUT" --epochs 2 --batch 256
code=$?
[ "$code" != "0" ] && { echo "FIT FAILED $code"; exit "$code"; }

say "4/4 gate in the real environment"
# The number that matters. Agreement with the teacher is imitation; this is play.
$VENV -u scripts/play_in_the_real_env.py --checkpoint "${OUT%.pkl}.best.pkl" --games 4 \
    --seed-base $((7000000 + 1000 * ROUND))

say "round $ROUND DONE"
ls -la "${OUT%.pkl}"*.pkl
echo "next:  bash scripts/dagger_round.sh $((ROUND + 1)) ${OUT%.pkl}.best.pkl"
