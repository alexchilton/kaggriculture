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
# **The outcome table, and it is the point of this script.**
#
# It used to tail the `[N]` header plus the commit mix. Those are the wrong numbers: the commit
# rates are INTENT -- did the chosen bundle commit to an op -- and they sawtooth with the
# termination cycle, so `cHARV` swung 0.29 to 4.26 across a window in which `END` never left $0.
# Reading a trend off them is reading the phase of a cycle.
#
# `END` is the only outcome number in the log, and it prints at the bottom of an eight-line block
# where nothing surfaces it. Terminations land roughly every 6 updates (719 turns / horizon), so a
# row per termination is the real resolution of this run -- everything between is the same season
# still in flight.
python3 - "$OUT" <<'PY'
import re, sys

rows, cur = [], None
for line in open(sys.argv[1], errors="replace"):
    m = re.match(r'\[\s*(\d+)\]', line)
    if m:
        if cur:
            rows.append(cur)
        cur = dict(up=int(m.group(1)), wr=None, term=0, end='-', med='-', mx='-', pool='-', tape='-')
        w = re.search(r'wr ([\d.]+|nan)/', line)
        if w and w.group(1) != 'nan':
            cur['wr'] = float(w.group(1))
        g = re.search(r'term (\d+)', line)
        cur['term'] = int(g.group(1)) if g else 0
    elif cur is not None:
        g = re.search(r'bank med \$([\d,-]+) max \$([\d,-]+)', line)
        if g:
            cur['med'], cur['mx'] = g.group(1), g.group(2)
        g = re.search(r'END \$?([\d,-]+|n/a)', line)
        if g:
            cur['end'] = g.group(1)
        for k in ('pool', 'tape'):
            g = re.search(k + r':([\d.]+)/(\d+)x/d(\d+)%', line)
            if g:
                # W = wr - D/2, since a draw pays half. Two broke farms draw with certainty
                # (`money == money` is exact), so a high draw share IS the $0 signature.
                wr, n, d = float(g.group(1)), int(g.group(2)), int(g.group(3)) / 100
                cur[k] = "%.0f/%.0f/%.0f%% %dx" % (100 * (wr - d / 2), 100 * d,
                                                   100 * (1 - (wr - d / 2) - d), n)
if cur:
    rows.append(cur)

term = [r for r in rows if r['term']] or rows[-3:]
print("terminations only -- W/D/L%% derived from wr and the draw share")
print("%4s %7s %10s %9s %9s   %-16s %-16s" %
      ("up", "wr", "END", "bank med", "bank max", "pool W/D/L", "tape W/D/L"))
for r in term[-10:]:
    print("%4d %7s %10s %9s %9s   %-16s %-16s" %
          (r['up'], "%.3f" % r['wr'] if r['wr'] is not None else "-",
           r['end'], r['med'], r['mx'], r['pool'], r['tape']))
if rows:
    print("\nlatest update %d (of %d logged); END prints only on a termination update"
          % (rows[-1]['up'], len(rows)))
PY
