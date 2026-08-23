#!/bin/bash
# Pull the box's RL training log to data/logs/rl_tape_box.log and print the tail.
#
# The remote file is the source of truth. This is a snapshot; run it again for a fresh one.
# XLA prints ~110 lines of allocator probe noise at startup, which is stripped here --
# pass --raw to keep it.
set -u

BOX=alex@192.168.1.128
KEY=~/.ssh/copilot_remote_ed25519
REMOTE=/home/alex/kaggriculture/data/logs/rl_tape.log
OUT="$(cd "$(dirname "$0")/.." && pwd)/data/logs/rl_tape_box.log"

if [ "${1:-}" = "--raw" ]; then
    FILTER=cat
else
    FILTER='grep -v cuda_executor\|Source\ Location\|external/xla'
fi

ssh -o ConnectTimeout=15 -i "$KEY" -p 2222 "$BOX" "$FILTER $REMOTE" > "$OUT" 2>&1
echo "wrote $OUT ($(wc -l < "$OUT") lines)"
echo
grep -E '^\[ *[0-9]+\]' "$OUT" | tail -6
echo
grep 'vs idle' "$OUT" | tail -1
