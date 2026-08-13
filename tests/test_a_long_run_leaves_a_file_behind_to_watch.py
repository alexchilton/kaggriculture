"""Progress from a long run has to land in a file, because stdout does not reach the user.

`CLAUDE.md`, "Long-Running Commands MUST Be Visible": a Bash tool call's stdout goes to the agent,
not to the person waiting. A ten-minute gate with no log file is indistinguishable from a hung one,
and the standing instruction is to state the absolute log path BEFORE starting anything slow.

`kagg/logs.py` makes that the default instead of something every caller re-implements by hand with
a `tee`. This pins two things:

- the logger itself writes to stderr AND to a timestamped file, and is idempotent, because the
  scripts that use it are imported by multiprocessing workers and a second set of handlers doubles
  every line;
- the gates and sweeps that run for minutes actually use it.

**Result TABLES are deliberately not logged.** They are output -- meant to be read or piped -- and
stapling a timestamp and a logger name onto every row of a per-day grid makes them worse. The
distinction is progress versus product, and only progress moves.
"""

import logging
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.logs import get_logger

#: Scripts that run for minutes and whose progress a human needs to watch. `field_sweep.py` is
#: deliberately absent: it has uncommitted changes in the working tree and converting it here would
#: collide with them.
LONG_RUNNERS = ("arena_gate.py", "tape_gate.py", "mirror_gate.py", "tape_sweep.py",
                "product_search.py", "episode_index.py")


def test_the_logger_writes_a_file_and_says_where(tmp_path, monkeypatch, capsys):
    import kagg.logs

    monkeypatch.setattr(kagg.logs, "LOG_DIR", tmp_path)
    log = get_logger("test_a_long_run_unique_name")
    log.info("hello %d", 7)

    files = list(tmp_path.glob("*.log"))
    assert len(files) == 1, files
    body = files[0].read_text()
    assert "hello 7" in body
    assert str(files[0]) in body, "the log has to name its own path, it is the thing to open"
    assert "hello 7" in capsys.readouterr().err, "stderr must still get everything"


def test_asking_twice_does_not_double_every_line(tmp_path, monkeypatch):
    """These modules are re-imported in every multiprocessing worker."""
    import kagg.logs

    monkeypatch.setattr(kagg.logs, "LOG_DIR", tmp_path)
    first = get_logger("test_a_long_run_idempotent")
    handlers = list(first.handlers)
    second = get_logger("test_a_long_run_idempotent")
    assert second is first
    assert second.handlers == handlers
    for handler in handlers:
        if isinstance(handler, logging.FileHandler):
            handler.close()


def test_the_long_runners_log_their_progress():
    for name in LONG_RUNNERS:
        source = (REPO / "scripts" / name).read_text()
        assert "from kagg.logs import get_logger" in source, (
            f"{name} runs for minutes and its progress is invisible without a log file")
        assert source.count("log.") >= 2, f"{name} imports the logger and does not use it"


def test_no_progress_counter_is_left_on_stdout():
    """A `k/n` counter is progress by definition, and progress is the thing a person watching a
    ten-minute run needs. A result TABLE row may stay a `print` -- it is the product."""
    import re

    counter = re.compile(r"\{\w+\}/\{|%d/%d|/\{len\(")
    for name in LONG_RUNNERS:
        for line in (REPO / "scripts" / name).read_text().splitlines():
            if "print(" in line and counter.search(line):
                raise AssertionError(f"{name}: progress counter still on stdout -- {line.strip()}")
