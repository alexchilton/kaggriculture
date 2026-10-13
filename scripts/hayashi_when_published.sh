#!/bin/bash
# Wait for the 2026-09-10 daily episode dataset, then pull Yusuke Hayashi's live
# episodes and classify them against the 13 tapes he published.
#
# His live submission 56136071 (rating 2960.7, W80-L29) plays episodes
# 107,336,033-107,520,852. Every published daily snapshot tops out at
# 107,288,328, so none of his current games are downloadable until the 09-10
# dataset appears just after midnight.
#
# Polls every 30 minutes. One `kaggle datasets files` call per poll, nothing else.
exec 2>&1
set -u
cd ~/DataspellProjects/kaggriculture
DS=kaggle/kaggriculture-episodes-2026-09-10
IDS=data/logs/hayashi_episode_ids.txt
OUT=data/replays_2026-09-10
K=/Users/alexchilton/Library/Python/3.12/bin/kaggle

echo "waiting for $DS  (started $(date))"
while true; do
  listing=$("$K" datasets files "$DS" --page-size 5 2>&1)
  if echo "$listing" | grep -qE "^[0-9]+\.json"; then
    echo "$(date): dataset published"
    break
  fi
  sleep 1800
done

# Full file list, paged.
: > /tmp/files_2026-09-10.txt
tok=""
for i in $(seq 1 8); do
  if [ -z "$tok" ]; then r=$("$K" datasets files "$DS" --page-size 200 2>/dev/null)
  else r=$("$K" datasets files "$DS" --page-size 200 --page-token "$tok" 2>/dev/null); fi
  echo "$r" | grep -oE "^[0-9]+\.json" >> /tmp/files_2026-09-10.txt
  tok=$(echo "$r" | grep -oE "Next Page Token = \S+" | sed 's/.*= //')
  [ -z "$tok" ] && break
done
sort -u /tmp/files_2026-09-10.txt | sed 's/.json//' | sort > /tmp/day10_ids.txt
echo "day 09-10 holds $(wc -l < /tmp/day10_ids.txt) episodes"

comm -12 <(sort "$IDS") /tmp/day10_ids.txt > /tmp/hayashi_available.txt
echo "Hayashi episodes available: $(wc -l < /tmp/hayashi_available.txt) of $(wc -l < $IDS)"
[ -s /tmp/hayashi_available.txt ] || { echo "none present; his games are newer than this snapshot too"; exit 0; }

mkdir -p "$OUT"
bash scripts/fetch_leader_episodes.sh "$DS" "$OUT" $(sed 's/$/.json/' /tmp/hayashi_available.txt | tr '\n' ' ')

.venv-sub/bin/python -u scripts/classify_ladder_agents.py "$OUT"
.venv-sub/bin/python -u scripts/hayashi_tape_diff.py "$OUT"
echo "DONE $(date)"
