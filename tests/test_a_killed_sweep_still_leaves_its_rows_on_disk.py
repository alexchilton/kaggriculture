"""A sweep that is interrupted keeps the seasons it already finished.

`town_arm_grid.py` used to open its rows CSV **after the last season**. Any run that was killed,
crashed, or hit a traceback wrote nothing at all -- not a partial file, not a header, nothing.

Measured 2026-08-22, the morning this was found:

    big_carrot      8,448 seasons planned   ran >1h   log held only its own header, 0 rows
    carrot_seeds   21,120 seasons planned   ran >1h   log held only its own header, 0 rows

Both were killed when the box was taken for the tape shootout. 29,568 planned seasons produced
nothing readable. The same end-of-run write had already hidden a `TypeError` in `rows_line` (11
format specifiers against 12 arguments) behind the entire run, so a sweep of any length ended in a
traceback and no CSV -- the failure could not be seen until the very moment the data was due.

The fix is not "be careful": the header goes down before the pool starts and every row is flushed
on arrival. This pins that, because the old behaviour is invisible right up until it costs hours.

    python -u -m pytest tests/test_a_killed_sweep_still_leaves_its_rows_on_disk.py -q
"""
import os
import pathlib
import re
import signal
import subprocess
import sys
import time

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
GRID = REPO / "scripts/town_arm_grid.py"


def test_the_header_is_written_before_the_pool_runs():
    """Static guard, and the cheap one.

    The whole defect is an ordering: `open(raw, "w")` after the season loop instead of before it.
    A reader of this file should be able to see that ordering without waiting for a subprocess.
    """
    src = GRID.read_text()
    open_at = src.index('open(raw, "w")')
    # Anchor on the CALL, not the word: the first draft matched `imap_unordered` inside the comment
    # that explains this very fix, which sits above the open() and inverted the result.
    pool_at = src.index("mp.imap_unordered(")
    assert open_at < pool_at, (
        "the rows CSV is opened AFTER the season loop. A killed or crashed sweep writes nothing; "
        "29,568 planned seasons produced zero rows on 2026-08-22 this way.")
    tail = src[open_at:pool_at]
    assert "rows_header()" in tail and "flush()" in tail, (
        "the header must be written and flushed between opening the file and starting the pool, "
        f"so an interrupted run is still readable. Got:\n{tail}")


def test_every_row_is_flushed_as_it_lands():
    """The header alone is not enough -- buffered rows die with the process."""
    src = GRID.read_text()
    loop = src[src.index("mp.imap_unordered("):]      # the call, not the word -- see the test above
    body = loop[:loop.index("\n    print(") if "\n    print(" in loop else 2000]
    assert re.search(r"fh\.write\(rows_line\(", body), (
        "rows are not written inside the season loop; they are still being accumulated and "
        "written at the end")
    assert re.search(r"fh\.flush\(\)", body), (
        "rows are written but not flushed inside the loop. Python block-buffers a file object, so "
        "a killed process loses everything still in the buffer -- which is the whole failure.")


@pytest.mark.slow
def test_a_sweep_killed_mid_run_leaves_readable_rows():
    """End to end: start a real sweep, kill it, read what survived.

    The static guards above check the shape of the code. This checks the property the shape is for,
    because the two have come apart before -- `rows_line` was extracted and unit-tested on 2026-08-22
    while the writer that called it still ran once, at the end.
    """
    out = REPO / "data/logs/test_killed_sweep_rows.csv"
    out.unlink(missing_ok=True)
    env = dict(os.environ, GRID_ROWS=str(out), PYTHONUNBUFFERED="1")
    proc = subprocess.Popen(
        [sys.executable, "-u", str(GRID), "--towns", "8", "--seeds", "11",
         "--arms", "control", "--jobs", "2"],
        cwd=REPO, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True)
    try:
        deadline = time.time() + 240
        while time.time() < deadline:
            if out.exists() and len(out.read_text().splitlines()) >= 2:
                break
            if proc.poll() is not None:
                pytest.skip("the sweep finished before it could be interrupted")
            time.sleep(1)
        else:
            pytest.fail("no rows appeared within 240s; the CSV is still written at the end")

        # Kill it the way the box killed the carrot sweeps.
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        proc.wait(timeout=30)
    finally:
        if proc.poll() is None:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)

    lines = out.read_text().splitlines()
    out.unlink(missing_ok=True)
    assert len(lines) >= 2, f"killed sweep left {len(lines)} lines; it must keep finished seasons"
    header = lines[0].split(",")
    assert header[0] == "town" and "drain_CARROT" in header, f"bad header: {lines[0]}"
    for row in lines[1:]:
        assert len(row.split(",")) == len(header), (
            f"row has {len(row.split(','))} cells against {len(header)} named columns: {row}")
