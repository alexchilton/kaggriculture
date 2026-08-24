"""The GRID, not the bank: does our board match カワシギ's, tile for tile, day by day?

Alex, 2026-08-24: *"the money is irrelevant it is the grid which is important."*

He is right and the bank is a bad instrument for this. Two boards can hold the same bank while one
is a field of ripe strawberry and the other is bare dirt; and a bank gap opens the turn one arm's
purchase is refused, then every later day inherits it whether or not anything else went wrong. The
board is the state the agent actually builds.

Both arms sit in HIS seat, on the game's own seed, against the same recorded opponent tape:

    tape   カワシギ's own actions, verbatim
    us     our agent from turn 0

Per day this compares the two boards cell by cell and reports:

    same    cells identical in both (crop and animal and kind)
    diff    cells that differ
    first   the first day any cell differs -- the day the clone stops being a clone

and then the per-crop tile counts on both boards, so a divergence can be read as "we planted wheat
where he planted strawberry" rather than just a number.

The zones are read off the code, not assumed (`schedule_agent.REPLAY_OPENING_DAYS`,
`cover.UNSOLVE_DAYS`):

    d0-d3 opening (planner)   d4-d11 REPLAY of a fixed tape   d12-d23 solver   d24-d29 planner
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

TPD = 24
ZONE = ([("opening",)] * 4 + [("replay",)] * 8 + [("solver",)] * 12 + [("planner",)] * 6)


def _cells(farm):
    """`(r,c) -> signature` for every tile that holds anything."""
    out = {}
    for r, row in enumerate(farm.get("tiles") or []):
        for c, t in enumerate(row):
            if not isinstance(t, dict):
                continue
            sig = (t.get("kind"), t.get("crop"), t.get("animal"))
            if any(sig):
                out[(r, c)] = sig
    return out


def _counts(cells):
    n = collections.Counter()
    for kind, crop, animal in cells.values():
        if crop:
            n[crop] += 1
        elif animal:
            n[animal] += 1
        elif kind:
            n[kind] += 1
    return n


def play_boards(rec, his_seat, seed, use_agent):
    """Returns day -> cells, for his seat."""
    from kaggle_environments import make
    import importlib
    import breakdown as B
    import us_in_his_seat as U

    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    steps = rec["steps"]
    them = 1 - his_seat

    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
    env.reset(2)
    agent = SA.make_agent(sched, his_seat) if use_agent else None

    boards = {}
    for t in range(30 * TPD):
        o = env.state[his_seat].observation
        if t % TPD == 0:
            boards[t // TPD] = _cells(o["farms"][his_seat])
        n_us = len(o["farms"][his_seat].get("hands") or [])
        n_them = len(o["farms"][them].get("hands") or [])
        if use_agent:
            a = agent(o)
            mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                    "market": a["market"]}
        else:
            a = U._recorded(steps, t, his_seat)
            mine = {"farmer": a.get("farmer") or ["PASS"],
                    "hands": list(a.get("hands") or [])[:n_us],
                    "market": a.get("market") or []}
        at = U._recorded(steps, t, them)
        yours = {"farmer": at.get("farmer") or ["PASS"],
                 "hands": list(at.get("hands") or [])[:n_them],
                 "market": at.get("market") or []}
        env.step([mine, yours] if his_seat == 0 else [yours, mine])
        if env.done:
            break
    return boards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", default="")
    ap.add_argument("--who", default="カワシギ")
    ap.add_argument("--detail", default="", help="episode to print the full per-day grid for")
    a = ap.parse_args()

    import glob
    files = set()
    for d in ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c",
              "leaders_2026-08-24", "kawa_2026-08-24", "losses", "top_guys", "top2",
              "field_leaders", "new_leader", "ladder", "our_games"):
        files |= set(glob.glob(str(REPO / f"data/seed_scripts/{d}/*.json")))
    files |= set(glob.glob("/Users/alexchilton/Downloads/*.json"))
    wanted = set(a.games.split(",")) if a.games else None

    print("THE GRID: our board vs his, same seat, same seed, same opponent tape.")
    print("d0-d3 opening | d4-d11 REPLAY | d12-d23 solver | d24-d29 planner\n", flush=True)

    t0 = time.time()
    rows = []
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
        try:
            tb = play_boards(rec, seat, seed, use_agent=False)
            ub = play_boards(rec, seat, seed, use_agent=True)
        except Exception as e:                                               # noqa: BLE001
            print(f"{ep:>10}  {e!r}", flush=True)
            continue

        first = None
        per_day = []
        for d in sorted(tb):
            if d not in ub:
                break
            keys = set(tb[d]) | set(ub[d])
            diff = sum(1 for k in keys if tb[d].get(k) != ub[d].get(k))
            per_day.append((d, len(keys) - diff, diff))
            if diff and first is None:
                first = d
        rows.append((ep, names[1 - seat], first, per_day, tb, ub))
        z = ZONE[first][0] if first is not None and first < len(ZONE) else "-"
        d29 = per_day[-1] if per_day else (0, 0, 0)
        print(f"{ep:>10}  first differs d{first if first is not None else '-':<3} "
              f"({z:>7})   d29 same {d29[1]:>3} diff {d29[2]:>3}   {names[1 - seat][:20]}",
              flush=True)

        if a.detail and ep == a.detail:
            print(f"\n--- {ep} per-day grid ---")
            print(f"{'day':>4} {'same':>5} {'diff':>5}   his board                       "
                  f"    our board")
            for d, same, diff in per_day:
                hc = ", ".join(f"{k} {v}" for k, v in sorted(_counts(tb[d]).items()))
                uc = ", ".join(f"{k} {v}" for k, v in sorted(_counts(ub[d]).items()))
                print(f"{d:>4} {same:>5} {diff:>5}   {hc[:40]:<40}  {uc[:40]}")
            print()
    print(f"\n({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
