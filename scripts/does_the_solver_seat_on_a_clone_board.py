"""Play the `main_replay12` path and count what the SOLVER actually seats, per day.

Alex, 2026-08-26: *"so you think the solver is really needed here?"*. I said "nominally on", which
is an argument, not a number. This is the number.

`PRECOMPUTED_ROUTES` was solved on the **kawashigi** schedule's boards. The replay arms hand over on
a **clone_open** board at d12. `_apply_precomputed` keys every stop on the exact `(tile, ops)` tuple
(`cover.py:1023`), so a stop only seats if that board grew the same crop on the same square and
wants the same ops on it. If the boards differ, the key misses, the stop is recorded in
`PRECOMPUTED_MISSES`, and the job falls through to the same cheapest-insertion the greedy uses.

So the question "is the solver needed" is exactly: **of the stops the fixture names, how many key-
match?** Not how much money the season makes -- a solver that seats nothing is byte-identical to no
solver at all, and would read as a null in an A/B for the wrong reason.

    stops       what the fixture named for that day
    seated      keys that matched a job on the live board
    missed      keys the board does not have  (`PRECOMPUTED_MISSES`)
    no_unit     tours written for a hand that did not arrive

`_apply_precomputed` is wrapped in this process only. Nothing is patched into the shipped path.
"""

import argparse
import collections
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

ROWS = collections.defaultdict(lambda: dict(stops=0, routed=0, missed=0, no_unit=0, calls=0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="clone_open")
    ap.add_argument("--handover", type=int, default=12)
    ap.add_argument("--seed", type=int, default=123641874)
    ap.add_argument("--weeds", type=float, default=0.005)
    args = ap.parse_args()

    from kagg.search import cover as C
    import scripts.breakdown as B

    plan_stops = {d: sum(len(w) for w in units.values())
                  for d, units in C.PRECOMPUTED_ROUTES.items()}

    inner = C._apply_precomputed

    def wrapped(day, jobs, units, *a, **k):
        before = len(C.PRECOMPUTED_MISSES)
        out = inner(day, jobs, units, *a, **k)
        row = ROWS[day]
        row["calls"] += 1
        if out is None:
            return out
        routes, _left = out
        row["stops"] += plan_stops.get(day, 0)
        # **NOT `sum(len(w) for w in routes.values())`.** `_apply_precomputed` runs
        # `_insert_leftovers` into the same `routes` dict before returning (cover.py:1057), so that
        # sum counts greedy insertions as solver seats -- it read 107% of the fixture's own stops on
        # d16 and 97% overall, which flattered the solver and contradicted the `missed` column in
        # the same table. A key matches or it does not; the matched count is what is left after the
        # misses and the re-homed tours.
        row["routed"] += sum(len(w) for w in routes.values())
        for d, msg in C.PRECOMPUTED_MISSES[before:]:
            if "skipped" in msg:
                row["missed"] += int(msg.split("skipped ")[1].split(" ")[0])
            elif "re-homed" in msg:
                row["no_unit"] += int(msg.split("; ")[1].split(" ")[0])
        return out

    # `breakdown.run` takes agent FACTORIES, not a tape name; the tape/handover wiring lives in
    # `main`. Drive the CLI so this probe measures the same composition the arm ships.
    C._apply_precomputed = wrapped
    sys.argv = ["breakdown", "--tape", args.tape, "--seed", str(args.seed),
                "--weeds", str(args.weeds), "--days", "30",
                "--handover", str(args.handover)]
    try:
        B.main()
    finally:
        C._apply_precomputed = inner

    print(f"\nsolver seating, tape {args.tape}, handover d{args.handover}, seed {args.seed}")
    print("  stops   = what the fixture named        matched = keys the live board had")
    print("  missed  = keys the board does not have  routed  = jobs in the returned routes,")
    print("                                                    INCLUDING greedy insertion\n")
    print(f"{'day':>5}{'stops':>8}{'matched':>9}{'missed':>8}{'no_unit':>9}{'match %':>9}{'routed':>9}")
    tot = collections.Counter()
    for day in sorted(ROWS):
        r = ROWS[day]
        if not r["stops"] and not r["calls"]:
            continue
        matched = r["stops"] - r["missed"] - r["no_unit"]
        for k in ("stops", "routed", "missed", "no_unit"):
            tot[k] += r[k]
        tot["matched"] += matched
        pct = 100.0 * matched / max(1, r["stops"])
        print(f"{day:>5}{r['stops']:>8}{matched:>9}{r['missed']:>8}{r['no_unit']:>9}"
              f"{pct:>8.0f}%{r['routed']:>9}")
    pct = 100.0 * tot["matched"] / max(1, tot["stops"])
    print(f"{'ALL':>5}{tot['stops']:>8}{tot['matched']:>9}{tot['missed']:>8}"
          f"{tot['no_unit']:>9}{pct:>8.0f}%{tot['routed']:>9}")


if __name__ == "__main__":
    main()
