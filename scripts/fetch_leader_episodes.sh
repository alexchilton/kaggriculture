#!/bin/bash
# Pull individual episodes from a daily kaggriculture episode dataset.
# The daily datasets are ~21 GB each; every episode in them comes from the high-rated
# sample (median avg score 3,068 on 2026-08-08), so a sample of 20 is a sample of leaders.
#   scripts/fetch_leader_episodes.sh <dataset-slug> <outdir> <file...>
set -u
K=/Users/alexchilton/Library/Python/3.12/bin/kaggle
SLUG="$1"; OUT="$2"; shift 2
mkdir -p "$OUT"
for f in "$@"; do
  if [ -s "$OUT/$f" ]; then echo "have $f"; continue; fi
  echo "--- $f"
  "$K" datasets download -d "$SLUG" -f "$f" -p "$OUT" --force 2>&1 | tail -1
  [ -s "$OUT/$f.zip" ] && (cd "$OUT" && unzip -o -q "$f.zip" && rm -f "$f.zip")
done
echo "=== done: $(ls -1 "$OUT" | wc -l) files, $(du -sh "$OUT" | cut -f1) ==="
