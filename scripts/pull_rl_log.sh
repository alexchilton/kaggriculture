#!/bin/bash
# Pull the box's RL training log to data/logs/rl_<tag>_box.log and print the tail.
#
#   scripts/pull_rl_log.sh                # the live run, currently shaped2
#   scripts/pull_rl_log.sh tape           # an older run, data/logs/rl_tape.log on the box
#   scripts/pull_rl_log.sh shaped2 --raw  # keep the XLA allocator noise
#
# **The tag is an argument because hardcoding it went stale.** This file named `rl_tape.log` while
# the live run wrote `rl_shaped2.log`, so it fetched a dead log and printed its last update as if it
# were current -- the same failure as a stale harness default.
#
# The remote file is the source of truth. This is a snapshot; run it again for a fresh one.
# XLA prints ~110 lines of allocator probe noise at startup, stripped unless --raw.
set -u

TAG=shaped2
RAW=0
for a in "$@"; do
    case "$a" in
        --raw) RAW=1 ;;
        *)     TAG="$a" ;;
    esac
done

BOX=alex@192.168.1.128
KEY=~/.ssh/copilot_remote_ed25519
REMOTE=/home/alex/kaggriculture/data/logs/rl_${TAG}.log
SUPER=/home/alex/kaggriculture/data/logs/rl_${TAG}_supervisor.log
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/data/logs/rl_${TAG}_box.log"

if [ "$RAW" = 1 ]; then
    FILTER=cat
else
    FILTER='grep -v cuda_executor\|Source\ Location\|external/xla'
fi

ssh -o ConnectTimeout=15 -i "$KEY" -p 2222 "$BOX" "$FILTER $REMOTE" > "$OUT" 2>&1
echo "wrote $OUT ($(wc -l < "$OUT") lines)"

# Is it actually running, and did the supervisor have to restart it? A log that stopped growing
# reads exactly like a slow one, so say which.
echo
ssh -o ConnectTimeout=15 -i "$KEY" -p 2222 "$BOX" "exec 2>&1;
    if ps -eo args | grep -q '[t]rain_jax_rl.py'; then echo 'STATE: running'; else echo 'STATE: NOT RUNNING'; fi
    echo \"last write: \$(stat -c %y $REMOTE 2>/dev/null | cut -d. -f1)\"
    [ -f $SUPER ] && tail -3 $SUPER"

echo
grep -E '^\[ *[0-9]+\]' "$OUT" | tail -6
echo
grep 'vs idle' "$OUT" | tail -1
grep -E '^ +commit ' "$OUT" | tail -1
