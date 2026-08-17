#!/bin/bash
# Re-solve d12-d29 on ALL FOUR boards, against the trajectory the agent actually ships.
#
# Why this exists: `_apply_precomputed` keys a stop on `(tile, ops)`, so changing which crop sits on
# which square drops the stop rather than adapting it. `OPENING_GEOMETRY` swapped six squares in the
# opening, so every one of the four route tables now describes a board we no longer play.
#
# `melon/q3` runs ALONE first, because it writes `kagg/search/solved_days.py` and `cover` imports that
# at module load in every other arm's dump step. The remaining three write their own target files and
# only READ the melon table, so they run in parallel once it is stable.
#
# `resolve_days.py --days` defaults to d12..d29 -- and it is a COMMA LIST, not a count. Do not pass
# `--days 29` expecting 29 days; that solves ONE day.
set -u
cd /Users/alexchilton/DataspellProjects/kaggriculture
export PYTHONPATH=.
SECS="${1:-300}"
D=data/logs
STAMP=2026-08-17

say () { echo "[$(date +%H:%M:%S)] $*"; }

say "budget ${SECS}s per day, d12-d29, four arms"
say "=== arm 1/4  melon q3 -> kagg/search/solved_days.py   (alone, everything imports it)"
python -u scripts/resolve_days.py --tape kawashigi --seconds "$SECS" \
  --arm melon --target kagg/search/solved_days.py \
  --log "$D/resolve_geom_melon_q3_$STAMP.log" > "$D/resolve_geom_melon_q3_stdout_$STAMP.log" 2>&1
say "melon q3 exit $?"

say "=== arms 2-4/4 in parallel: melon q4, straw q3, straw q4"
python -u scripts/resolve_days.py --tape kawashigi --seconds "$SECS" \
  --arm melon --q4 --target kagg/search/solved_days_q4.py \
  --log "$D/resolve_geom_melon_q4_$STAMP.log" > "$D/resolve_geom_melon_q4_stdout_$STAMP.log" 2>&1 &
P2=$!
python -u scripts/resolve_days.py --tape kawashigi --seconds "$SECS" \
  --arm straw --target kagg/search/solved_days_straw.py \
  --log "$D/resolve_geom_straw_q3_$STAMP.log" > "$D/resolve_geom_straw_q3_stdout_$STAMP.log" 2>&1 &
P3=$!
python -u scripts/resolve_days.py --tape kawashigi --seconds "$SECS" \
  --arm straw --q4 --target kagg/search/solved_days_straw_q4.py \
  --log "$D/resolve_geom_straw_q4_$STAMP.log" > "$D/resolve_geom_straw_q4_stdout_$STAMP.log" 2>&1 &
P4=$!
say "pids melon_q4=$P2 straw_q3=$P3 straw_q4=$P4"
wait $P2; say "melon q4 exit $?"
wait $P3; say "straw q3 exit $?"
wait $P4; say "straw q4 exit $?"

say "=== ALL FOUR ARMS DONE"
for f in solved_days solved_days_q4 solved_days_straw solved_days_straw_q4; do
  n=$(grep -cE '^    [0-9]+: \{' "kagg/search/$f.py" 2>/dev/null || echo 0)
  say "  $f.py  days present: $n"
done
