"""Tape opening, then our planner: Otter Vibe's shape, built from parts we already have.

The #2 agent on the ladder plays a fixed four-day opening and then adapts. The
planner bundle already supports exactly that -- `_OPENING` replays verbatim while
the planner is driven underneath every turn so its per-day state is warm at the
handover -- but the builder sources its opening from a recorded replay. This
injects the imported Shop Router 0909 tape instead.

`_REPLAY_DAYS` stays 0 on purpose: the bundled `make_agent(schedule, me, router)`
has no `start_day` parameter, and passing one is a TypeError, i.e. a submission
that banks the $3,000 start.

    .venv-sub/bin/python -u scripts/build_hybrid.py --days 12 --tape 0
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "submission" / "main_own.py"
TAPES = ROOT / "submission" / "shop0909" / "actions.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, required=True, help="replay the tape for days 0..N-1")
    ap.add_argument("--tape", type=int, default=0)
    ap.add_argument("--out")
    args = ap.parse_args()

    src = BUNDLE.read_text()
    tape = json.loads(TAPES.read_text())[args.tape]
    turns = args.days * 24
    if turns > len(tape):
        raise SystemExit(f"tape has {len(tape)} turns, asked for {turns}")

    opening = [[step.get("farmer") or ["PASS"],
                list(step.get("hands") or []),
                list(step.get("market") or [])] for step in tape[:turns]]

    pattern = re.compile(r"^_OPENING = json\.loads\(r'''.*?'''\)$", re.M | re.S)
    if not pattern.search(src):
        raise SystemExit("could not find the _OPENING line in the bundle")
    src = pattern.sub("_OPENING = json.loads(r'''" + json.dumps(opening) + "''')", src)
    src = re.sub(r"^_REPLAY_DAYS = \d+$", "_REPLAY_DAYS = 0", src, flags=re.M)

    out = Path(args.out) if args.out else ROOT / "submission" / f"hybrid_d{args.days}.py"
    out.write_text(src)
    print(f"wrote {out}  opening {turns} turns from tape {args.tape}, "
          f"planner takes over at day {args.days}")

    # The artifact must import and play, or it is a $3,000 submission.
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"_hybrid{args.days}", out)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print(f"imports OK, _OPENING carries {len(module._OPENING)} turns, "
          f"_REPLAY_DAYS={module._REPLAY_DAYS}")


if __name__ == "__main__":
    main()
