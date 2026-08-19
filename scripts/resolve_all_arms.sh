#!/bin/bash
# Re-solve all four route tables against the CURRENT crop mix, in arm order.
#
# The mix and the routes are one artifact: `_apply_precomputed` keys a stop on an exact `(tile, ops)`
# tuple, so a table solved for 42 strawberry measures the mismatch when the agent plants 35. Any crop
# change therefore has to be in the module BEFORE this runs, and the A/B afterwards is
# new-mix-on-new-routes against old-mix-on-old-routes.
#
# Backups of the four tables as they were before this ran: data/logs/solved_backup_2026-08-19/
set -u
cd /Users/alexchilton/DataspellProjects/kaggriculture
export PYTHONPATH=.

# **d12-d23 ONLY, never d24-d29.** `cover.UNSOLVE_DAYS = (24..29)` hands the closing days to the
# greedy, and that is the change worth +98 Elo: it is what gets the d28/d29 harvest in. Solving those
# six days burns 30 minutes an arm producing routes the agent deliberately does not use, and leaves a
# live fixture that would activate if UNSOLVE_DAYS were ever narrowed. d28 stays greedy.
DAYS=12,13,14,15,16,17,18,19,20,21,22,23

run_arm () {   # name tape arm seed target extra
  local name="$1" tape="$2" arm="$3" seed="$4" target="$5" extra="${6:-}"
  echo "############ $name  tape=$tape arm=$arm seed=$seed -> $target  $(date '+%H:%M:%S')"
  python -u scripts/resolve_days.py --days "$DAYS" \
      --tape "$tape" --arm "$arm" --seed "$seed" --target "$target" \
      --log "data/logs/resolve_${name}_2026-08-19.log" $extra 2>&1
  echo "############ $name exit=$?  $(date '+%H:%M:%S')"
}

run_arm melon   kawashigi     melon  1240813987  kagg/search/solved_days.py
run_arm q4straw kawashigi_q4c straw  244615642   kagg/search/solved_days_straw_q4.py --q4
run_arm q4melon kawashigi_q4c melon  244615642   kagg/search/solved_days_q4.py --q4

echo "ALL ARMS DONE $(date '+%H:%M:%S')"
