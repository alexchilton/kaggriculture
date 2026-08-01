#!/usr/bin/env bash
# Did training actually happen? `log.jsonl` is written per update, independently of stdout, so it
# answers that even when the stdout capture is broken -- which is the situation this exists for.
exec 2>&1
cd /home/alex/kagg || exit 1

echo "=== newest run dirs ==="
ls -dt data/jax_rl_runs/*/ 2>/dev/null | head -4

for d in $(ls -dt data/jax_rl_runs/*/ 2>/dev/null | head -3); do
  echo
  echo "=== $d ==="
  if [ -f "$d/log.jsonl" ]; then
    echo "log.jsonl: $(wc -l < "$d/log.jsonl") update rows"
    tail -2 "$d/log.jsonl"
  else
    echo "log.jsonl: MISSING (no update ever completed)"
  fi
  ls -la "$d" | grep -E 'pkl|jsonl' || echo "  (no checkpoints)"
done

echo
echo "=== service ==="
systemctl show kagg-train -p ActiveState -p Result -p ExecMainStatus -p ExecMainPID
echo "=== stdout log tail ==="
tail -4 data/logs/run.log 2>/dev/null
