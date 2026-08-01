#!/usr/bin/env bash
# Runs ON the 3080 box. Copied there by `deploy_train.sh`, then invoked with no arguments.
#
# Everything awkward lives in this file on purpose. The command line has to survive
# ssh -> PowerShell -> wsl bash -c -> bash, and each layer eats a different metacharacter:
# PowerShell swallows `>`, the nested quotes mangle `{ }` and `VAR=value` prefixes. A command
# string complex enough to set env vars and redirect output does not reliably arrive intact, and
# when it fails it fails *silently* -- which is why several runs produced no output at all.
# So: the remote invocation is `bash smoke.sh` and nothing else.
cd /home/alex/kagg || exit 1
mkdir -p data/logs

# Everything is written to a file ON THE BOX as well as to stdout. The file is the source of truth:
# it survives the SSH connection dropping, the laptop sleeping, and the run being watched from
# somewhere else later. Pulling it down is then a plain `cat`, which is far more robust than trying
# to keep a live pipe open across ssh -> PowerShell -> wsl for hours.
exec > >(tee -a data/logs/run.log) 2>&1
set -x                      # echo each command, so the log shows how far it got

echo "=== started $(date -Is) ==="

export PYTHONPATH=/home/alex/kagg
# JAX otherwise grabs 75% of the card up front; on this 16GB laptop GPU that fails and XLA walks
# the request down in 12 steps, printing RESOURCE_EXHAUSTED each time. It looks like a fatal OOM
# and is just the preallocator negotiating.
export XLA_PYTHON_CLIENT_PREALLOCATE=false

echo "=== host ==="
nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total --format=csv,noheader
echo "=== python ==="
# -u because Python block-buffers stdout when it is piped, so prints vanish while stderr flows.
/home/alex/kagg-venv/bin/python -u scripts/train_jax_rl.py \
    --batch "${1:-64}" \
    --horizon "${2:-32}" \
    --updates "${3:-3}" \
    --minibatch-size "${4:-128}" \
    --ckpt-every 1
echo "=== exit $? ==="
