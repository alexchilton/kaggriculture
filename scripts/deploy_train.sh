#!/usr/bin/env bash
# Sync, launch and watch the JAX training run on the 3080 box.
#
#   scripts/deploy_train.sh sync            # copy source across, verify checksums
#   scripts/deploy_train.sh bench           # jax_sim throughput (workload stated)
#   scripts/deploy_train.sh smoke           # 3 updates in the foreground, raw output
#   scripts/deploy_train.sh train [args]    # start under nohup, survives disconnect
#   scripts/deploy_train.sh watch [n]       # last n lines of the live log
#   scripts/deploy_train.sh follow          # stream the log until Ctrl-C
#   scripts/deploy_train.sh status          # is it alive? GPU use, last line, checkpoints
#   scripts/deploy_train.sh stop            # kill the run
#   scripts/deploy_train.sh pull            # copy checkpoints + log back here
#
# Two things this file exists to work around, both previously wasted time:
#  - Direct WSL2 SSH on port 2222 is flaky after a reboot, so everything goes through the
#    PowerShell fallback with `wsl bash -c`, as the global CLAUDE.md warns.
#  - PowerShell eats `>` inside the command string, so redirects must live in a script ON the box,
#    never in the ssh command line. That is why `train` writes a launcher remotely and runs it.
set -uo pipefail

HOST=alexr@192.168.1.128
KEY=~/.ssh/copilot_remote_ed25519
REMOTE=/home/alex/kagg
# `-u` is not optional. Python block-buffers stdout whenever it is piped rather than attached to a
# terminal, so every print() sits in an 8KB buffer while stderr flows freely -- which reads exactly
# like "the program produced no output and then died". It cost an hour here.
PY="/home/alex/kagg-venv/bin/python -u"
LOG=$REMOTE/data/logs/run.log

# JAX grabs 75% of the card up front by default. On this 16GB laptop GPU that request fails and XLA
# walks the size down (12.00 -> 10.80 -> ... -> 3.77 GiB), spraying RESOURCE_EXHAUSTED lines that
# look like a fatal OOM and are merely the preallocator negotiating. Turning preallocation off
# makes JAX allocate on demand: the noise goes away, and a genuine OOM becomes legible because it
# names the buffer that actually failed.
ENV_PREFIX="XLA_PYTHON_CLIENT_PREALLOCATE=false PYTHONPATH=$REMOTE"

# Remote stderr is merged into remote stdout **on the box**, with `2>&1` inside the command, before
# ssh ever sees it. This matters more than it looks: ssh delivers remote stderr onto *local* stderr,
# so the obvious `ssh ... 2>/dev/null` -- added to hide the post-quantum banner -- silently deletes
# every Python traceback from the remote process. That is exactly what happened here: two crashes
# read as "no output at all" because this function was eating the error message.
# So: merge on the far side, and only discard ssh's own chatter on the near side.
# No `2>&1` in the command string: PowerShell eats `>` before wsl ever sees it, which is the same
# bug that silently dropped a redirect earlier. Remote scripts merge their own streams with
# `exec 2>&1` instead. Local stderr is kept, so ssh failures are visible.
sh() {
  ssh -o ConnectTimeout=15 -o BatchMode=yes -i "$KEY" "$HOST" "wsl bash -c \"$1\"" | tr -d '\r'
}
put() { ssh -o ConnectTimeout=15 -o BatchMode=yes -i "$KEY" "$HOST" "wsl bash -c \"cat > $2\"" 2>/dev/null < "$1"; }

cmd=${1:-status}; shift || true

case "$cmd" in
sync)
  sh "mkdir -p $REMOTE/kagg/sim $REMOTE/kagg/rl $REMOTE/scripts $REMOTE/data"
  for f in kagg/sim/*.py kagg/rl/*.py scripts/train_jax_rl.py; do
    put "$f" "$REMOTE/$f"; echo "sent $f"
  done
  echo "--- checksums ---"
  for f in kagg/sim/jax_sim.py kagg/rl/jax_policy.py scripts/train_jax_rl.py; do
    l=$(md5 -q "$f"); r=$(sh "md5sum $REMOTE/$f" | awk '{print $1}')
    [ "$l" = "$r" ] && echo "  ok   $f" || echo "  DIFF $f  local=$l remote=$r"
  done
  ;;

bench)
  sh "cd $REMOTE && PYTHONPATH=$REMOTE $PY gpu_bench.py"
  ;;

kill)
  put scripts/remote_kill.sh "$REMOTE/kill.sh"
  sh "bash $REMOTE/kill.sh"
  ;;

smoke)
  # Foreground, unfiltered, small. Run this before every long run. Output goes to the terminal and
  # to data/logs/gpu_smoke.log, so it can be opened in an editor while it runs.
  #
  # The remote side is a *file*, not a command string: see scripts/remote_smoke.sh for why.
  #
  # Killing first is not paranoia. A cancelled ssh command leaves the remote process running, so
  # ten runs once accumulated on this box -- one per attempt -- and between them exhausted a 16 GB
  # GPU and a 13 GB machine. Every launch clears the decks.
  mkdir -p data/logs
  put scripts/remote_kill.sh "$REMOTE/kill.sh"
  sh "bash $REMOTE/kill.sh"
  put scripts/remote_smoke.sh "$REMOTE/smoke.sh"
  sh "bash $REMOTE/smoke.sh ${1:-64} ${2:-32} ${3:-3} ${4:-128}" | tee data/logs/gpu_smoke.log
  ;;

train)
  # Runs as a systemd service, not a background job: WSL2 reaps session-owned processes when the
  # last SSH connection closes, which killed several runs and looked like a startup crash.
  ARGS="${*:---batch 128 --horizon 64 --updates 20000 --minibatch-size 256 --ckpt-every 20}"
  put scripts/remote_kill.sh "$REMOTE/kill.sh"
  sh "bash $REMOTE/kill.sh"
  put scripts/remote_service.sh "$REMOTE/service.sh"
  sh "bash $REMOTE/service.sh $ARGS"
  ;;

getlog)
  # Pull the box's log down to a local file, which can sit open in an editor. This is the intended
  # way to watch a long run: the box owns the log, we take copies. Nothing depends on holding a
  # connection open, so a dropped SSH session or a closed laptop costs nothing.
  mkdir -p data/logs
  sh "cat $REMOTE/data/logs/run.log" > data/logs/run.log
  echo "pulled $(wc -l < data/logs/run.log) lines -> data/logs/run.log"
  tail -"${1:-25}" data/logs/run.log
  ;;

poll)
  # Pull every N seconds until interrupted. Prints only what is new each time.
  n=${1:-60}
  mkdir -p data/logs
  prev=0
  while true; do
    sh "cat $REMOTE/data/logs/run.log" > data/logs/run.log 2>/dev/null
    now=$(wc -l < data/logs/run.log)
    if [ "$now" -gt "$prev" ]; then
      tail -n +$((prev + 1)) data/logs/run.log
      prev=$now
    fi
    sleep "$n"
  done
  ;;

watch)
  sh "tail -${1:-40} $LOG"
  ;;

follow)
  ssh -o ConnectTimeout=15 -i "$KEY" "$HOST" "wsl bash -c \"tail -f $LOG\"" 2>/dev/null | tr -d '\r'
  ;;

status)
  # Defers to `kagg-status` on the box so there is one definition of "how is it going", whether it
  # is asked from here or from a terminal there.
  sh "kagg-status"
  ;;

stop)
  sh "sudo systemctl stop kagg-train; systemctl is-active kagg-train"
  ;;

pull)
  mkdir -p data/jax_rl_runs
  latest=$(sh "ls -td $REMOTE/data/jax_rl_runs/*/ 2>/dev/null | head -1")
  [ -z "$latest" ] && { echo "no runs on the box"; exit 1; }
  name=$(basename "$latest")
  mkdir -p "data/jax_rl_runs/$name"
  for f in latest.pkl best.pkl log.jsonl; do
    ssh -i "$KEY" "$HOST" "wsl bash -c \"cat $latest$f\"" 2>/dev/null > "data/jax_rl_runs/$name/$f" \
      && echo "pulled $f"
  done
  ;;

*)
  echo "usage: $0 {sync|bench|smoke|train|watch|follow|status|stop|pull}" >&2
  exit 1
  ;;
esac