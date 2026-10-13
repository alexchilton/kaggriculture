#!/bin/bash
# Fetch episode replays one at a time from Kaggle's public replay route.
#   scripts/fetch_episode_replays.sh <outdir> <delay-seconds> <episode-id...>
# Endpoint found in destbreso/x-ray-your-agent; www.kaggleusercontent.com/episodes/<id>.json
# 301-redirects to www.kaggle.com/competitions/episodes/<id>/replay.json, so -L is required.
# One request per file with a deliberate pause. Do not parallelise this.
exec 2>&1
set -u
OUT="$1"; DELAY="$2"; shift 2
mkdir -p "$OUT"
for id in "$@"; do
  if [ -s "$OUT/$id.json" ]; then echo "have $id"; continue; fi
  code=$(curl -sL -m 120 "https://www.kaggleusercontent.com/episodes/$id.json" \
         -o "$OUT/$id.json" -w "%{http_code}")
  size=$(stat -f%z "$OUT/$id.json" 2>/dev/null || echo 0)
  echo "$id  http=$code  ${size} bytes"
  [ "$code" = "200" ] || rm -f "$OUT/$id.json"
  sleep "$DELAY"
done
echo "FETCH_DONE $(ls -1 "$OUT" | wc -l) files, $(du -sh "$OUT" | cut -f1)"
