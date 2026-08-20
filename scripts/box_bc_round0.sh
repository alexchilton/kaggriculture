#!/bin/bash
# Unattended BC round 0 on the training box: build the rows across all cores, then fit.
#
# Launch it with `scripts/box_launch_bc.sh`, which puts this in a tmux session.
#
# **Files arrive by tarball over stdin, not by git and not by scp.** The repo needs credentials
# WSL2 does not have, so `git clone` creates the directory and leaves it with no commits -- twice,
# silently. Direct WSL2 SSH on port 2222 resets whenever WSL2 restarts and the Windows port proxy
# keeps the stale IP. What survives is:
#
#     tar czf - <files> | ssh alexr@box 'wsl tar xzf - -C /home/alex/kaggriculture'
#
# because nothing in that command line is a character PowerShell eats. Pipes, redirects, `$(...)`
# and `VAR=value` are all removed in transit without a word, which is why every non-trivial step
# lives in a script file here rather than in an ssh argument.
#
# **The labels are NOT regenerated.** /home/alex/labels_r0b is 920,320 rows of teacher self-play,
# 16 shards, complete. `label_games.py` writes raw observations and actions with no encoding in
# them -- quantities and bundles are encoded by `build_bc_rows.py` -- so the label set survives the
# head change and only the rows are rebuilt.
set -uo pipefail

REPO=/home/alex/kaggriculture
# **Two venvs, and they are not interchangeable.** `.venv` is CPU jax; `.venv-cuda` is the GPU one.
# Row building is 16 parallel CPU encoders and belongs on the first; the fit is one process doing
# dense matmuls and belongs on the second. Running the fit on `.venv` would train on CPU at a
# fraction of the speed while looking completely healthy in the log.
VENV=$REPO/.venv/bin/python
CUDA=$REPO/.venv-cuda/bin/python
[ -x "$CUDA" ] || CUDA=$VENV
LABELS=/home/alex/labels_r0b
ROWS=/home/alex/rows_r0b
VOCAB=$REPO/data/il/bundle_vocab.json

say() { echo; echo "=== $* ===  $(date '+%H:%M:%S')"; }

cd "$REPO" || exit 1

say "0/3 inputs"
echo "cpu    : $($VENV -V 2>&1)"
echo "cuda   : $CUDA"
echo "MAX_QTY: $($VENV -c 'from kagg.rl import jax_policy as P; print(P.MAX_QTY, P.N_BUNDLES)')"
wc -l "$LABELS"/*.jsonl | tail -1
ls -la "$VOCAB" || { echo "NO VOCABULARY -- stop"; exit 1; }

# **Waves of 4, not all 16 at once.** The first attempt ran all sixteen and the OOM killer took
# every one of them: no traceback, the worker logs simply stopping after "vocabulary 197 of 256
# slots", `free` showing nothing alive and the output directory empty. WSL2 has 13 GB. Each worker
# holds ~395 MB of output arrays plus its own jax interpreter, so sixteen does not fit even after
# the streaming fix in `build_bc_rows.build`. Four waves of four is under half the RAM and the box
# has 16 cores, so the wall clock barely moves.
WAVE=4
say "1/3 build rows, 16 shards in waves of $WAVE"
rm -rf "$ROWS"; mkdir -p "$ROWS"
fail=0
for start in $(seq 0 "$WAVE" 15); do
    pids=()
    for w in $(seq "$start" $((start + WAVE - 1))); do
        [ "$w" -gt 15 ] && continue
        $VENV -u scripts/build_bc_rows.py --shards "$LABELS" --vocab "$VOCAB" \
            --out "$ROWS" --only "$w" > "/home/alex/rows_w$w.log" 2>&1 &
        pids+=($!)
    done
    for p in "${pids[@]}"; do wait "$p" || fail=1; done
    echo "  wave from shard $start done (fail so far=$fail)  $(date '+%H:%M:%S')"
    free -g | head -2
done

say "rows built (fail=$fail)"
ls -la "$ROWS"
if [ "$fail" != "0" ]; then
    echo "A ROW WORKER FAILED -- tails follow, training NOT started"
    for w in $(seq 0 15); do echo "--- w$w ---"; tail -6 "/home/alex/rows_w$w.log"; done
    exit 1
fi

say "2/3 fit (GPU venv)"
$CUDA -c "import jax; print('jax devices:', jax.devices())" 2>&1 | tail -2
# Three epochs over 920,320 rows. Read the argmax mix against the teacher's 0.789, not the loss:
# a falling loss with a degenerate argmax is the failure this pipeline exists to catch.
$CUDA -u scripts/fit_bc.py --rows "$ROWS" --vocab "$VOCAB" \
    --out /home/alex/bc_bundle.pkl --epochs 3 --batch 256
code=$?

say "3/3 DONE exit=$code"
ls -la /home/alex/bc_bundle.pkl 2>/dev/null
exit $code
