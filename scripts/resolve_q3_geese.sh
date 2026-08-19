#!/bin/bash
# Re-solve the two THREE-QUADRANT arms with `HERD_GEESE = 2` live.
#
# A goose yields EVERY day (`interval 1`) against a cow's 2 and a sheep's 3, so it changes the daily
# COLLECT/CARE stops on its tile -- and `_apply_precomputed` keys a stop on `(tile, op_names)`. Species
# swaps between COW and SHEEP are route-neutral only because both sit on a PASTURE with similar
# cadence; a goose is not, and measuring one against cow-solved routes is the same confound that made
# the strawberry cap read -$28,259 before its tables were re-solved.
#
# Measured on cow-solved routes, which is what this run exists to replace:
#     straw_q3  160,183 -> 97,317   melon_q3  145,068 -> 98,697
# with seed at close exploding $30 -> $2,100 and $10 -> $1,960. That seed is the tell: desynced routes
# drop plantings, so bought seed is never sown. It is a symptom of the mismatch, not a seed defect.
#
# d12-d23 only. `cover.UNSOLVE_DAYS` keeps d24-d29 with the greedy on these arms -- the +98 Elo change
# that brings the d28/d29 harvest in -- and the q4 arms are not touched at all here.
#
# Backups before this ran: scratchpad/schedule_agent.PRE_GEESE.py, solved_days{,_straw}.PRE_GEESE.py
set -u
cd /Users/alexchilton/DataspellProjects/kaggriculture
export PYTHONPATH=.

DAYS=12,13,14,15,16,17,18,19,20,21,22,23

while pgrep -f "scripts/resolve_days.py" > /dev/null; do
  echo "waiting for a running solve... $(date '+%H:%M:%S')"
  sleep 60
done

echo "############ geese straw  $(date '+%H:%M:%S')"
python -u scripts/resolve_days.py --days "$DAYS" \
    --tape kawashigi_b3 --arm straw --seed 70683142 \
    --target kagg/search/solved_days_straw.py \
    --log data/logs/resolve_geese_straw_2026-08-19.log 2>&1
echo "############ geese straw exit=$?  $(date '+%H:%M:%S')"

echo "############ geese melon  $(date '+%H:%M:%S')"
python -u scripts/resolve_days.py --days "$DAYS" \
    --tape kawashigi --arm melon --seed 1240813987 \
    --target kagg/search/solved_days.py \
    --log data/logs/resolve_geese_melon_2026-08-19.log 2>&1
echo "############ geese melon exit=$?  $(date '+%H:%M:%S')"

echo "GEESE RE-SOLVE DONE $(date '+%H:%M:%S')"
