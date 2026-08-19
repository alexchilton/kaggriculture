#!/bin/bash
# Tomato on/off across seeds, on BOTH three-quadrant arms.
#
# The shipped rule plants a tomato tile on the strawberry arm and not the melon arm. That rests on one
# seed per arm, and neither number is clean: the melon -$3,880 is a single board, and the straw
# +$14,073 is mostly the penalty for running cap-only against tomato-solved routes, not the tile's
# value. If the real axis is the BOARD -- tomato-draining shops, ground pressure -- then there are
# melon boards where it pays and straw boards where it does not, and the arm split is a coincidence of
# two seeds.
#
# A different seed re-rolls the shop draw, so the d4-d11 replay is no longer an exact reproduction of
# his game. Both sides of each pair face that identically, so the pairing stays fair.
set -u
cd /Users/alexchilton/DataspellProjects/kaggriculture
export PYTHONPATH=.
SP=/private/tmp/claude-501/-Users-alexchilton-DataspellProjects-kaggriculture/1ceba71d-ed80-4dee-9d20-d544a8b98ee0/scratchpad
while pgrep -f "scripts/resolve_days.py" > /dev/null; do
  echo "waiting for the geese solve... $(date '+%H:%M:%S')"; sleep 120
done
for arm in melon straw; do
  echo "===== $arm arm ====="
  for seed in 1240813987 70683142 1300 1301 1302 1303; do
    for tom in 0 1; do
      TOM=$tom python -u $SP/tom_seeds.py $seed $arm
    done
  done
done
echo "TOMATO SEED SWEEP DONE $(date '+%H:%M:%S')"
