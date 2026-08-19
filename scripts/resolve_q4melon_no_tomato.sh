#!/bin/bash
# Re-solve the Q4 MELON arm d12-d23 without the tomato tile.
#
# `melon_armed` is False on this arm, so the per-arm rule turns the tomato tile OFF here -- but its
# d12-d23 table was solved earlier today WITH the tile, while its d24-d29 table was solved after the
# rule landed and so is already tomato-free. A half-matched arm is worse than either consistent state:
# measured 93,929 baseline -> 81,621 (all-tomato routes, tile on) -> 79,961 (half-matched). This pass
# makes d12-d23 agree with the mix the arm actually plays.
#
# d24-d29 are NOT re-solved: they were solved at 16:21-16:50 with the tile already off. The q4 arms do
# run precomputed routes there, because `q4_branch.install` resets `cover.UNSOLVE_DAYS` to () -- the
# three-quadrant arms keep the greedy close, which is the +98 Elo change and stays untouched.
set -u
cd /Users/alexchilton/DataspellProjects/kaggriculture
export PYTHONPATH=.

while pgrep -f "scripts/resolve_days.py" > /dev/null; do
  echo "waiting for the running solve... $(date '+%H:%M:%S')"
  sleep 60
done

echo "############ q4melon-no-tomato d12-d23  $(date '+%H:%M:%S')"
python -u scripts/resolve_days.py --days 12,13,14,15,16,17,18,19,20,21,22,23 \
    --tape kawashigi_q4c --arm melon --seed 244615642 --q4 \
    --target kagg/search/solved_days_q4.py \
    --log data/logs/resolve_q4melon_notom_2026-08-19.log 2>&1
echo "############ q4melon-no-tomato exit=$?  $(date '+%H:%M:%S')"
