#!/bin/bash
# Unattended BC round 0 on the training box. Pull, build the vocabulary, build the rows across all
# cores, fit. One log, one absolute path, no interactive step.
#
# Run it from the Windows hop, which is the connection that stays up:
#
#   ssh -i ~/.ssh/copilot_remote_ed25519 alexr@192.168.1.128 \
#       'wsl bash -c "nohup bash /home/alex/kagg2/scripts/box_bc_round0.sh > /home/alex/bc_run.log 2>&1 &"'
#
# **Why a fresh clone rather than the existing tree.** /home/alex/kaggriculture is a copied
# directory, not a git checkout, so it cannot pull. Direct WSL2 SSH on port 2222 keeps resetting --
# WSL2 restarts and the Windows port proxy holds the stale IP -- so scp is not reliable enough to
# push eleven changed files. git over HTTPS from inside WSL2 is.
#
# The labels are NOT re-generated. /home/alex/labels_r0b is 920,320 rows of teacher self-play,
# 16 shards, already complete, and `label_games.py` writes raw observations and actions with no
# encoding in them -- the quantity and bundle encoding happens in `build_bc_rows.py`. So the
# label set survives the head change and only the rows are rebuilt.
set -uo pipefail

REPO=/home/alex/kagg2
VENV=/home/alex/kaggriculture/.venv/bin/python
LABELS=/home/alex/labels_r0b
ROWS=/home/alex/rows_r0b
BRANCH=bundle-head

say() { echo; echo "=== $* ===  $(date '+%H:%M:%S')"; }

say "0/4 checkout $BRANCH"
if [ -d "$REPO/.git" ]; then
    cd "$REPO" && git fetch --all -q && git checkout -q "$BRANCH" && git reset -q --hard "origin/$BRANCH"
else
    rm -rf "$REPO"
    git clone -q --branch "$BRANCH" https://github.com/alexchilton/kaggriculture.git "$REPO"
    cd "$REPO"
fi
git log --oneline -1
cd "$REPO"

say "labels present"
wc -l "$LABELS"/*.jsonl | tail -1

say "1/4 bundle vocabulary"
# Rebuilt rather than copied: data/il is gitignored, and a vocabulary that disagrees with the one
# the labels were written against makes every bundle index mean something else, silently.
mkdir -p "$REPO/data/il"
$VENV -u scripts/build_bundle_vocab.py --shards "$LABELS" --out "$REPO/data/il/bundle_vocab.json" \
    || { echo "VOCAB FAILED"; exit 1; }

say "2/4 build rows, 16 workers"
rm -rf "$ROWS"; mkdir -p "$ROWS"
pids=()
for w in $(seq 0 15); do
    $VENV -u scripts/build_bc_rows.py --shards "$LABELS" \
        --vocab "$REPO/data/il/bundle_vocab.json" --out "$ROWS" --only "$w" \
        > "/home/alex/rows_w$w.log" 2>&1 &
    pids+=($!)
done
fail=0
for p in "${pids[@]}"; do wait "$p" || fail=1; done
say "rows built (fail=$fail)"
ls -la "$ROWS" | tail -18
if [ "$fail" != "0" ]; then
    echo "AT LEAST ONE ROW WORKER FAILED -- tails follow, training NOT started"
    for w in $(seq 0 15); do echo "--- w$w ---"; tail -5 "/home/alex/rows_w$w.log"; done
    exit 1
fi

say "3/4 fit"
$VENV -u scripts/fit_bc.py --rows "$ROWS" --vocab "$REPO/data/il/bundle_vocab.json" \
    --out /home/alex/bc_bundle.pkl --epochs 3 --batch 256
code=$?

say "4/4 DONE exit=$code"
ls -la /home/alex/bc_bundle.pkl 2>/dev/null
exit $code
