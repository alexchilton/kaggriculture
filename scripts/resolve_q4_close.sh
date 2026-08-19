#!/bin/bash
# Re-solve d24-d29 for the TWO Q4 ARMS ONLY.
#
# `q4_branch.install` sets `cover.UNSOLVE_DAYS = ()` (q4_branch.py:294) -- deliberately, and
# documented there -- so the four-quadrant arms use precomputed routes right through d29 while the
# three-quadrant arms hand d24-d29 to the greedy. A crop-mix change therefore leaves the q4 closing
# routes stale, and stale closing routes are expensive: measured 2026-08-19 on q4_melon, d12-d22 seated
# with ZERO skipped stops while d24-d29 skipped 138, for -$12,308 on the season.
#
# The q3 arms are NOT touched here. `cover.UNSOLVE_DAYS = (24..29)` giving them the greedy close is the
# change worth +98 Elo -- it is what gets the d28/d29 harvest in -- and it stays.
set -u
cd /Users/alexchilton/DataspellProjects/kaggriculture
export PYTHONPATH=.

DAYS=24,25,26,27,28,29

run_arm () {   # name arm target
  local name="$1" arm="$2" target="$3"
  echo "############ $name  arm=$arm -> $target  $(date '+%H:%M:%S')"
  python -u scripts/resolve_days.py --days "$DAYS" \
      --tape kawashigi_q4c --arm "$arm" --seed 244615642 --target "$target" --q4 \
      --log "data/logs/resolve_${name}_close_2026-08-19.log" 2>&1
  echo "############ $name exit=$?  $(date '+%H:%M:%S')"
}

run_arm q4straw straw kagg/search/solved_days_straw_q4.py
run_arm q4melon melon kagg/search/solved_days_q4.py

echo "Q4 CLOSING DAYS DONE $(date '+%H:%M:%S')"
