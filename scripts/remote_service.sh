#!/usr/bin/env bash
# Install and start the training as a **systemd service**, then report.
#
# Why a service rather than `nohup`/`setsid`: WSL2 reaps the distro's processes when the last
# session detaches, even with the VM kept alive by `vmIdleTimeout=-1`. A detached background job
# therefore dies the moment the SSH connection closes -- which looked exactly like a silent crash
# during startup, because the log simply stopped mid-way with no traceback, no OOM kill in dmesg,
# and a recycled PID in the pidfile. Foreground `smoke` runs survived only because the session
# stayed open for their whole duration.
#
# systemd is PID 1 here, so a unit it owns is not tied to any session. It also gives restart-on-
# failure, `systemctl status`, and journald -- none of which nohup provides.
exec 2>&1
UNIT=kagg-train
LOG=/home/alex/kagg/data/logs/run.log

mkdir -p /home/alex/kagg/data/logs
if [ -s "$LOG" ]; then
  mv "$LOG" "/home/alex/kagg/data/logs/run-$(date +%Y%m%d-%H%M%S).log"
fi

sudo tee /etc/systemd/system/$UNIT.service >/dev/null <<UNITFILE
[Unit]
Description=kaggriculture PPO self-play training
After=network.target

[Service]
Type=simple
User=alex
WorkingDirectory=/home/alex/kagg
Environment=PYTHONPATH=/home/alex/kagg
# JAX otherwise preallocates 75% of the card, which fails on this 16GB laptop GPU and produces a
# ladder of RESOURCE_EXHAUSTED messages that read like a fatal OOM.
Environment=XLA_PYTHON_CLIENT_PREALLOCATE=false
# Deliberately NO LD_LIBRARY_PATH or PATH overrides here. Setting LD_LIBRARY_PATH to
# /usr/lib/wsl/lib:/usr/local/cuda/lib64 looked like the obvious fix and silently *broke* GPU
# detection -- the run fell back to `CpuDevice` and trained at a useless speed while looking
# healthy. Measured directly: JAX gets `CudaDevice(id=0)` and compiles a matmul under a stripped
# `env -i` shell and inside a transient systemd unit, so the service environment was never the
# problem. ptxas comes from the venv's own nvidia pip package and is found without help.
# -u because Python block-buffers stdout when it is not a terminal, and a buffered log looks
# identical to a hung process.
ExecStart=/home/alex/kagg-venv/bin/python -u /home/alex/kagg/scripts/train_jax_rl.py $*
StandardOutput=append:$LOG
StandardError=append:$LOG
# Deliberately no Restart=: a crash loop that silently restarts would hide the very failures this
# project keeps being bitten by. If it dies, it should stay dead and be visible.
Restart=no

[Install]
WantedBy=multi-user.target
UNITFILE

sudo systemctl daemon-reload
sudo systemctl restart $UNIT
sleep 4
systemctl is-active $UNIT
systemctl status $UNIT --no-pager -n 5 | head -12

# journald on this box has a corrupted journal and drops the exit record, so the unit's own
# properties are the reliable way to learn *why* a run stopped. `ExecMainStatus` is the exit code
# and `ExecMainCode`/`Result` distinguish a clean exit from a signal -- the difference between "the
# script returned" and "something killed it", which guessing could not resolve.
echo "--- exit status (once it stops) ---"
systemctl show $UNIT -p Result -p ExecMainStatus -p ExecMainCode -p NRestarts
echo "--- log so far ---"
tail -5 "$LOG" 2>/dev/null || echo "(no log yet)"
