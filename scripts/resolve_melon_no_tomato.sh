#!/bin/bash
# Re-solve the MELON arm d12-d23 now that the tomato tile is strawberry-arm only.
#
# The melon table solved earlier today was solved WITH a tomato tile in the mix. Turning the tile off
# on that arm leaves the routes solved for a mix the agent no longer plays -- the same mismatch that
# has produced every misleading number today. Measured before this ran: melon on tomato-solved routes
# is 136,516 with the tile and 140,396 without it (baseline 139,453), so the arm is worth re-solving
# for its real mix rather than shipping either mismatch.
#
# Waits for any solver already running, so the two do not contend for the CPU and the fixtures are not
# dumped against a half-installed table.
set -u
cd /Users/alexchilton/DataspellProjects/kaggriculture
export PYTHONPATH=.

while pgrep -f "scripts/resolve_days.py" > /dev/null; do
  echo "waiting for the running solve... $(date '+%H:%M:%S')"
  sleep 60
done

echo "############ melon-no-tomato  $(date '+%H:%M:%S')"
python -u scripts/resolve_days.py --days 12,13,14,15,16,17,18,19,20,21,22,23 \
    --tape kawashigi --arm melon --seed 1240813987 \
    --target kagg/search/solved_days.py \
    --log data/logs/resolve_melon_notom_2026-08-19.log 2>&1
echo "############ melon-no-tomato exit=$?  $(date '+%H:%M:%S')"
