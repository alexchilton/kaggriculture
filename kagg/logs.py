"""A shared logger for long-running scripts: sweeps, searches, ladders, gates.

`CLAUDE.md`'s "Long-Running Commands MUST Be Visible" rule exists because bare `print()` to a
Bash tool's stdout is invisible to a human until the whole command finishes -- a ten-minute sweep
with no log file reads identically to a hung one. Before this module, every script that wanted a
visible log had to remember to `tee` it by hand and there was no consistent format, level or
timestamp across any of them.

Usage, at the top of a script's `main()` or module scope::

    from kagg.logs import get_logger
    log = get_logger(__name__)
    log.info("starting: %d jobs, %d workers", len(jobs), args.workers)

Every call also reaches stderr, so nothing about a script's terminal behaviour changes -- this
is additive (a file destination and a timestamp), not a replacement for reading the output live.

**What this is not for.** The per-day grid tables in `scripts/breakdown.py` and similar
human-facing report output are deliberate stdout, meant to be read or piped, not log lines with a
timestamp and a logger name stapled to every row. Leave those as `print()`.
"""

import logging
import pathlib
import sys
import time

#: Where every logger's file handler writes. Matches the path every long-running command in this
#: project is already told to log to by hand; this just makes it the default instead of something
#: each caller re-implements.
LOG_DIR = pathlib.Path("data/logs")

_FORMAT = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"
_DATEFMT = "%H:%M:%S"


def get_logger(name, filename=None, level=logging.INFO):
    """A `logging.Logger` that writes to stderr AND a timestamped file under `data/logs/`.

    `name` is usually `__name__`, so the log lines carry the module that emitted them. `filename`
    overrides the log file's basename (default: the last dotted component of `name`, e.g.
    `field_sweep` for `scripts.field_sweep`); the timestamp is always appended so two runs of the
    same script never clobber each other's log.

    Idempotent: calling this twice for the same `name` (a module re-imported, or a caller that
    builds the logger more than once) returns the same logger without adding a second pair of
    handlers, which would otherwise double every line.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(_FORMAT, _DATEFMT)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    base = filename or name.rsplit(".", 1)[-1]
    path = LOG_DIR / f"{base}_{stamp}.log"
    file_handler = logging.FileHandler(path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("logging to %s", path)
    return logger
