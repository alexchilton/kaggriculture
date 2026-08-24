"""Alex, 2026-08-24: *"we decide based on a decision at d3 to have more melon or more strawberry
and it is dependent on the opponent -- if the opponent did different it would be the other branch."*

`MelonBranch.trigger` counts the OPPONENT's MELON tiles at d3 and arms the strawberry season at 9
or more (`melon_branch.py:73,76,217`). So the tape we replay from d4 is chosen by his opponent's
board, and picking the wrong one replays a season he did not play.

This tests that directly. For every kawa game:

    the opponent's MELON tiles at d3, and which arm that gives
    for each of the four canned tapes, how many of d4-d8's 120 turns match his RECORDED actions

If the arm we take is not the tape that matches best, the trigger is wrong and that is the fix.
If NO tape matches well, four tapes are not enough and the branch is not the problem.
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24


def _norm(a):
    if not isinstance(a, dict):
        return (("PASS",), (), ())
    return (tuple(a.get("farmer") or ["PASS"]),
            tuple(tuple(x) for x in (a.get("hands") or [])),
            tuple(sorted(tuple(x) for x in (a.get("market") or []))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", default="カワシギ")
    ap.add_argument("--lo", type=int, default=4)
    ap.add_argument("--hi", type=int, default=8)
    a = ap.parse_args()

    import importlib
    import breakdown as B
    import us_in_his_seat as U

    SA = importlib.import_module("kagg.search.schedule_agent")
    MB = importlib.import_module("kagg.search.melon_branch")
    BR = importlib.import_module("kagg.search.branch")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    days = tuple(range(a.lo, a.hi + 1))
    tapes = {key: SA._replay_opening(days, *tape)
             for key, tape in SA.REPLAY_OPENING_TAPE.items()}

    files = {}
    for d in ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c",
              "leaders_2026-08-24", "kawa_2026-08-24", "losses", "top_guys", "top2",
              "new_leader", "ladder", "our_games"):
        for f in glob.glob(str(REPO / f"data/seed_scripts/{d}/*.json")):
            files.setdefault(pathlib.Path(f).stem, f)
    for f in glob.glob("/Users/alexchilton/Downloads/*.json"):
        files.setdefault(pathlib.Path(f).stem, f)

    n_turns = len(days) * TPD
    keys = sorted(tapes)
    print(f"opponent MELON tiles at d3, and how many of d{a.lo}-d{a.hi}'s {n_turns} turns")
    print("each canned tape reproduces of his RECORDED actions.\n")
    print(f"{'episode':>10} {'opp':>4} {'arm':>18}   " +
          "  ".join(f"{str(k):>14}" for k in keys) + "   best")

    tally = collections.Counter()
    for ep, f in sorted(files.items()):
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                     # noqa: BLE001
            continue
        if not isinstance(rec, dict) or "steps" not in rec:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        if a.who not in names:
            continue
        seat = names.index(a.who)
        steps = rec["steps"]
        d3 = 3 * TPD
        if d3 >= len(steps):
            continue
        obs = steps[d3][seat]["observation"]
        try:
            opp = BR.count_tiles(obs, BR.opponent_seat(obs), crop="MELON")
        except Exception:                                                     # noqa: BLE001
            continue
        armed = opp >= MB.OPPONENT_MELON

        scores = {}
        for k, tape in tapes.items():
            hit = 0
            for t in range(a.lo * TPD, (a.hi + 1) * TPD):
                his = U._recorded(steps, t, seat)
                row = tape.get(t)
                mine = ({"farmer": row[0], "hands": row[1], "market": row[2]}
                        if row is not None else None)
                if mine is None:
                    continue
                n = len(his.get("hands") or [])
                mine = {"farmer": mine["farmer"], "hands": list(mine["hands"] or [])[:n],
                        "market": mine["market"]}
                his_t = {"farmer": his.get("farmer") or ["PASS"],
                         "hands": list(his.get("hands") or [])[:n],
                         "market": his.get("market") or []}
                hit += _norm(mine) == _norm(his_t)
            scores[k] = hit

        best = max(scores, key=lambda k: scores[k])
        ours = (armed, False)
        ours = ours if ours in scores else best
        tally[(ours == best)] += 1
        print(f"{ep:>10} {opp:>4} {str(ours):>18}   " +
              "  ".join(f"{scores[k]:>14}" for k in keys) +
              f"   {best} {scores[best]}" + ("" if ours == best else "   <-- WRONG ARM"))

    print(f"\narm we take is the best-matching tape: {tally[True]} games; "
          f"a different tape matches better: {tally[False]} games")


if __name__ == "__main__":
    main()
