"""One gate every schedule must pass before anything runs on it.

**Why this exists, and why it RAISES instead of warning.** His recorded orders are not what he does.
He offers `BUY_PRODUCT WHEAT 48` on a day the engine fills 11 of, and asks 1.41x the strawberry and
1.62x the melon he actually plants -- the engine drops the rest silently and he plays on. Our planner
obeys the number in the row, so an over-ask spends money he never spent, and the money it spends is
always the next animal: measured on the d7 handover, `buy_animal 0/1`, `animals 7/8`, and therefore
`feed 7/8` and `care 7/8`, with the bank closing $419 against his $4 on the yarn world.

Alex: "i did say remove the over asks from the schedules ... because u is stupid and will forget that
in future and get confused - i cant be bothered to keep repeating the fix. or might forget too ...
then its a problem."

So it is not a step in a runbook. `seeds == Counter(plants)` is checked structurally, and the market
rows are checked against a stamp that only `tape_fills` writes, so a schedule built by the old path,
hand-edited, or left over from an earlier session fails at load with the command that fixes it --
rather than quietly costing an animal a day.
"""
import collections
import json
import pathlib

STAMP = "FILLS"          #: what `meta.json["market"]` must say for the market rows to be trusted


def check(sched, path):
    """Raise unless `sched` carries LANDED seeds and engine-measured market rows."""
    path = pathlib.Path(path)
    bad = []
    for d in sorted(sched, key=lambda k: int(k)):
        row = sched[d] or {}
        want = collections.Counter(row.get("plants") or [])
        got = collections.Counter({k: int(v) for k, v in (row.get("seeds") or {}).items() if v})
        if want != got:
            bad.append(f"    d{d}: seeds {dict(got)} != plants {dict(want)}")
    if bad:
        raise ValueError(
            f"{path}: `seeds` is his REQUESTED buy, not what he planted -- it over-asks 1.41x on "
            f"STRAWBERRY and 1.62x on MELON across 179 seasons, and the difference is the day's "
            f"animal.\n" + "\n".join(bad[:8])
            + f"\n  rebuild it:  .venv-sub/bin/python scripts/spataro_branch_schedules.py")

    meta = path.parent / "meta.json"
    stamped = ""
    if meta.exists():
        try:
            stamped = (json.loads(meta.read_text()) or {}).get("market") or ""
        except ValueError:
            stamped = ""
    if stamped != STAMP:
        raise ValueError(
            f"{path}: market rows are not engine-measured fills ({meta.name} market={stamped!r}, "
            f"wanted {STAMP!r}). His `buys` are OFFERS -- d7 offers WHEAT 48 and fills 11 -- and "
            f"obeying the offer spends the next animal's money.\n"
            f"  fix it:  .venv-sub/bin/python scripts/tape_fills.py --replay <replay> "
            f"--schedule {path} --write")
    return sched


def load(path):
    """Read a schedule JSON and check it. Keys stay as written; callers cast as they already do."""
    sched = json.loads(pathlib.Path(path).read_text())
    return check(sched, path)


def same_season(schedule, replay):
    """Raise unless the schedule's rows came from the season the replay plays.

    `--handover N` has the replay put a board down through d N-1 and our planner take over with these
    rows. Rows from a different season describe different ground, and the planner then plans onto
    tiles that are not there -- silently, because a PLANT or a BUILD onto an occupied tile is a no-op
    (`reference/kaggriculture.py:499`). Nothing in the output says "wrong season"; it just reads as a
    planner that cannot follow its own rows.

    The episode number is the replay's filename and the schedule's `meta.json["episode"]`, so this
    costs nothing and cannot drift.
    """
    ep = None
    meta = pathlib.Path(schedule).parent / "meta.json"
    if meta.exists():
        try:
            m = json.loads(meta.read_text()) or {}
            ep = (m.get("schedule_from") or {}).get("episode") or m.get("episode")
        except ValueError:
            ep = None
    if ep is None:
        return                      # nothing claimed, nothing to contradict
    stem = pathlib.Path(replay).stem
    if stem.isdigit() and int(stem) != int(ep):
        raise ValueError(
            f"{schedule} carries episode {ep} but the tape replays {stem}. The board and the rows "
            f"must be the same season -- rebuild with "
            f"`scripts/spataro_branch_schedules.py --default-episode {stem}`, or pair the arm with "
            f"data/replays_spa_sub/{ep}.json.")
