#!/usr/bin/env bash
# Launch the full-season (d0-d30) DAgger run on the Windows box, in the CUDA venv.
#
# Run it ON THE BOX: bash ~/kaggriculture/scripts/box_launch_season.sh
#
# `.venv-cuda`, never `.venv`. The CPU venv prints "Falling back to cpu" and runs anyway, which is
# indistinguishable from a slow GPU in the log.
#
# Beta does NOT anneal here: `--anneal-after-agree 2.0` is a bar agreement can never clear, so the
# teacher drives every rollout and this is plain behaviour cloning on teacher states. The PLAYOUT is
# hardcoded beta=0 regardless, so the "student alone" number in the log is unaffected by that choice.
set -u

cd "$HOME/kaggriculture" || exit 1
mkdir -p data/logs
LOG="$HOME/kaggriculture/data/logs/dagger_season.log"

# shellcheck disable=SC1091
source .venv-cuda/bin/activate

python -c "import jax; print('JAX DEVICES:', jax.devices())" > "$LOG" 2>&1

setsid python -u scripts/dagger_tape.py \
    --tag season \
    --rounds 400 \
    --episodes 4 \
    --horizon 719 \
    --vocab data/il/bundle_vocab_teacher.json \
    --beta0 1.0 \
    --anneal-rounds 10 \
    --anneal-after-agree 2.0 \
    --playout 1 \
    --epochs 3 \
    --batch-turns 512 \
    --aggregate-cap 60000 \
    --expert-cap 30000 \
    --save-data-every 10 \
    --lr 1e-4 \
    --bundle-alpha 1.0 \
    --day0-repeat 8 >> "$LOG" 2>&1 < /dev/null &

echo "launched pid $! -> $LOG"
