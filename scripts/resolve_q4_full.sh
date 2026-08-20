#!/bin/bash
# Re-solve BOTH four-quadrant tables end to end, d12-d29.
#
# **These tables are not merely stale, they are actively harmful, and that is measured.** On
# 2026-08-19 the greedy played d12-d29 with NO precomputed routes at all and beat the solved
# q4_straw table by $1,222 (79,527 against 78,305). A table you beat by deleting it is doing damage.
# q4_melon lost only $12,095 to the same treatment, against straw q3's $5,906 and melon q3's $7,539,
# so both q4 arms are carrying route drift the q3 arms are not.
#
# They are the only two tables never re-solved during the 2026-08-19 mix work: `resolve_all_arms.sh`
# was pointed at them but the crop mix moved again afterwards, and `_apply_precomputed` keys a stop
# on `(tile, op_names)` -- a day whose work changed no longer matches its fixture and falls to
# `_insert_leftovers`, which needs slack the closing days have not got.
#
# **d12-d29, not d12-d23.** `q4_branch.install` sets `cover.UNSOLVE_DAYS = ()` (q4_branch.py:294), so
# unlike the three-quadrant arms these run precomputed routes right through d29. Solving only to d23
# leaves exactly the range that measured 138 skipped stops and -$12,308.
#
# Until this finishes, no q4 experiment measures the idea being tested -- it measures the table.
set -u
cd /Users/alexchilton/DataspellProjects/kaggriculture
export PYTHONPATH=.

DAYS=12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29

# Do not overlap a solve with the mix sweep or another solve: both saturate the cores, and an edit
# to `schedule_agent.py` landing mid-solve is what made the q4melon d18-d19 fixtures inconsistent
# earlier today.
while pgrep -f "mixsweep.py|scripts/resolve_days.py" > /dev/null; do
  echo "waiting for a running job... $(date '+%H:%M:%S')"
  sleep 60
done

run_arm () {   # name arm target
  local name="$1" arm="$2" target="$3"
  echo "############ $name  arm=$arm -> $target  $(date '+%H:%M:%S')"
  python -u scripts/resolve_days.py --days "$DAYS" \
      --tape kawashigi_q4c --arm "$arm" --seed 244615642 --target "$target" --q4 \
      --log "data/logs/resolve_${name}_full_2026-08-19.log" 2>&1
  echo "############ $name exit=$?  $(date '+%H:%M:%S')"
}

run_arm q4straw straw kagg/search/solved_days_straw_q4.py
run_arm q4melon melon kagg/search/solved_days_q4.py

echo "Q4 FULL RE-SOLVE DONE $(date '+%H:%M:%S')"
