#!/bin/bash
# Durable safety net: records what was published to the Kaggriculture competition.
# Cannot judge or measure anything - that is the scheduled Claude session's job.
# Exists so that if the session dies, nothing published is silently missed.
exec 2>&1
D=$(date +%Y-%m-%d_%H%M)
OUT=/Users/alexchilton/DataspellProjects/kaggriculture/data/logs/kernels_$D.txt
{
  echo "=== swept $(date) ==="
  echo "--- by date ---"
  /usr/local/bin/python3 -m kaggle kernels list --competition kaggriculture --sort-by dateRun --page-size 25
  echo
  echo "--- by votes ---"
  /usr/local/bin/python3 -m kaggle kernels list --competition kaggriculture --sort-by voteCount --page-size 25
  echo
  echo "--- our submissions ---"
  /usr/local/bin/python3 -m kaggle competitions submissions -c kaggriculture --csv
} > "$OUT" 2>&1
ln -sf "$OUT" /Users/alexchilton/DataspellProjects/kaggriculture/data/logs/kernels_latest.txt
