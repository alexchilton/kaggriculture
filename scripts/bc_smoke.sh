#!/bin/bash
# End-to-end smoke for the BC pipeline: label -> rows -> fit. Two games, two epochs.
#
# This exists because every piece of the pipeline has its own passing test and NOTHING had ever run
# the three of them in sequence. `label_games` writes JSONL, `build_bc_rows` reads it through the
# real encoder, `fit_bc` reads the npz. Three schemas that must agree and were never made to.
set -euo pipefail
cd "$(dirname "$0")/.."

OUT=/private/tmp/claude-501/-Users-alexchilton-DataspellProjects-kaggriculture/1ceba71d-ed80-4dee-9d20-d544a8b98ee0/scratchpad/bc_smoke
rm -rf "$OUT"; mkdir -p "$OUT/labels" "$OUT/rows"

echo "=== 1/3 label 2 games with the shipped planner ==="
python3 -u scripts/label_games.py --games 2 --worker 0 \
    --out "$OUT/labels" --agent submission/main.py

echo; echo "=== 2/3 build rows through the real encoder ==="
python3 -u scripts/build_bc_rows.py --shards "$OUT/labels" \
    --vocab data/il/bundle_vocab.json --out "$OUT/rows"

echo; echo "=== 3/3 fit two epochs ==="
python3 -u scripts/fit_bc.py --rows "$OUT/rows" --vocab data/il/bundle_vocab.json \
    --out "$OUT/bc_smoke.pkl" --epochs 2 --batch 128

echo; echo "=== SMOKE OK ==="
ls -la "$OUT/rows" "$OUT"
