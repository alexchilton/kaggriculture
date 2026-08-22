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
#
# **There is no early stopping.** `dagger_tape`'s round loop is a plain `range(first_round,
# args.rounds)` with no break; the only agreement-driven mechanism is the beta anneal, switched off
# above. So `--rounds` is a hard count. Measured 2026-08-22: round 0 of this configuration took
# 909 s, so 60 rounds is ~15 hours.
#
# That is a ceiling rather than a commitment. `latest.pkl` is written EVERY round and carries params,
# optimiser state, the reservoir and the RNG, so killing this run costs at most the round in flight:
#
#   kill <pid>                                            # stop whenever the numbers flatten
#   python -u scripts/dagger_tape.py --resume <run_dir>   # continue exactly where it left off
set -u

cd "$HOME/kaggriculture" || exit 1
mkdir -p data/logs
LOG="$HOME/kaggriculture/data/logs/dagger_season.log"

# shellcheck disable=SC1091
source .venv-cuda/bin/activate

python -c "import jax; print('JAX DEVICES:', jax.devices())" > "$LOG" 2>&1

setsid python -u scripts/dagger_tape.py \
    --tag season \
    --rounds 60 \
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
