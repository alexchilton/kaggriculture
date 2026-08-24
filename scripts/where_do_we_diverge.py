"""In each kawa game, WHICH SUBSYSTEM loses the money -- opening, replay, solver or planner?

Alex, 2026-08-24: *"is it the d0-d4 or the d4-d11 tape or the solver or the planner -- in each case."*

The shipped agent hands the season to four different things, and the boundaries are read off the
code rather than assumed (`schedule_agent.REPLAY_OPENING_DAYS`, `cover.UNSOLVE_DAYS`):

    d0  - d3    opening    the planner, from the schedule's target rows
    d4  - d11   replay     a FIXED recorded tape, embedded in the agent
    d12 - d23   solver     `cover.PRECOMPUTED_ROUTES`, routes solved offline
    d24 - d29   planner    live routing again, the solved table is withheld here

Note this contradicts `project_kaggriculture_tape_vs_schedule`, which says the shipped agent replays
nothing. That memory is stale for this build: `REPLAY_OPENING_DAYS = (4,...,11)` is set.

**The replay is the suspicious one and here is why.** The tape it replays was recorded in ONE game.
Played on another seed the shops unlock differently, the opponent sells differently and the bank
follows a different path, so a purchase that succeeded in the recording can be refused here and a
PLANT can land on a weeded tile. Nothing detects it; the day just does less.

## What is attributed

Both arms are our seat: `tape` is カワシギ's own actions, `us` is our agent, same seed, same
opponent tape. `d(zone)` is how much of the final gap opened inside that zone -- the change in
(us bank - tape bank) across the zone's days. They sum to the total by construction.

A zone's number is where the money was LOST, not necessarily where the CAUSE is: a refused purchase
in the replay shows up as a smaller field in the solver. Read the earliest non-trivial zone first.
"""

import argparse
import collections
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import us_in_his_seat as U                                                  # noqa: E402

ZONES = [("opening", 0, 4), ("replay", 4, 12), ("solver", 12, 24), ("planner", 24, 30)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", default="")
    ap.add_argument("--who", default="カワシギ")
    ap.add_argument("--out", default="data/logs/where_do_we_diverge.csv")
    a = ap.parse_args()

    import glob
    files = set()
    for d in ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c",
              "leaders_2026-08-24", "kawa_2026-08-24", "losses", "top_guys", "top2",
              "field_leaders", "new_leader", "ladder", "our_games"):
        files |= set(glob.glob(str(REPO / f"data/seed_scripts/{d}/*.json")))
    files |= set(glob.glob("/Users/alexchilton/Downloads/*.json"))
    wanted = set(a.games.split(",")) if a.games else None

    out = REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("episode,seed,opponent,total," + ",".join(z[0] for z in ZONES) + "\n")
    fh.flush()

    print("where the gap opens: change in (our bank - his tape's bank) inside each zone.")
    print("d0-d3 opening | d4-d11 REPLAY of a fixed tape | d12-d23 solver | d24-d29 planner")
    print("only games whose tape arm reproduces its own recording are shown.\n", flush=True)
    print(f"{'episode':>10} {'total':>9} " + " ".join(f"{z[0]:>9}" for z in ZONES)
          + "  opponent", flush=True)

    t0 = time.time()
    tot = collections.Counter()
    n = 0
    for f in sorted(files):
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                    # noqa: BLE001
            continue
        if not isinstance(rec, dict) or "steps" not in rec:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        if a.who not in names:
            continue
        ep = pathlib.Path(f).stem
        if wanted and ep not in wanted:
            continue
        seed = (rec.get("info") or {}).get("seed")
        if seed is None:
            continue
        seat = names.index(a.who)
        rw = rec.get("rewards") or [0, 0]
        try:
            th, to, tb = U.play(rec, seat, seed, use_agent=False)
            uh, uo, ub = U.play(rec, seat, seed, use_agent=True)
        except Exception as e:                                               # noqa: BLE001
            print(f"{ep:>10}  {e!r}", flush=True)
            continue
        if abs((th - to) - (rw[seat] - rw[1 - seat])) > 1.0:
            continue                                                    # stale, pre-hinge game

        def gap(day):
            if day >= 30:
                return uh - th
            return ub.get(day, 0) - tb.get(day, 0)

        parts = [gap(hi) - gap(lo) for _z, lo, hi in ZONES]
        total = uh - th
        for (z, _l, _h), v in zip(ZONES, parts):
            tot[z] += v
        n += 1
        print(f"{ep:>10} {total:>+9,.0f} " + " ".join(f"{v:>+9,.0f}" for v in parts)
              + f"  {names[1 - seat][:20]}", flush=True)
        fh.write(",".join(str(x) for x in [ep, seed, names[1 - seat], round(total)]
                          + [round(v) for v in parts]) + "\n")
        fh.flush()
    fh.close()

    if n:
        print(f"\n{'MEAN':>10} {sum(tot.values()) / n:>+9,.0f} "
              + " ".join(f"{tot[z] / n:>+9,.0f}" for z, _l, _h in ZONES) + f"   (n={n})")
    print(f"\n({time.time() - t0:.0f}s)  rows -> {out}", flush=True)


if __name__ == "__main__":
    main()
