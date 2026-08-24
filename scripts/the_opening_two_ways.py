"""d0-d2 played by our PLANNER and by his TAPE, side by side, in one pass.

Alex, 2026-08-24: *"what is the difference between the tape and the planner d0-d2 that would cause
it -- a pass to a pasture would make no sense. I am still convinced the reason we can do the hires
is due to the feed/care of the sheep and cow in the right order, which means the sale of the wool
and milk in the right order."*

`305dc2b` gave d0-d2 to the tape. Measured over 35 kawashigi games, that took the number short of a
hand at d7 from 12 to 18, and deepened several of the twelve. So the two openings end d2 in
different states, and this prints what differs rather than guessing.

Both arms sit in his seat, on the game's own seed, against the same recorded opponent tape. The only
difference between them is `REPLAY_OPENING_DAYS`:

    planner   (4,5,6,7,8,9,10,11)          -- d0-d3 is our own planner, the pre-305dc2b behaviour
    tape      (0,1,2,4,5,6,7,8,9,10,11)    -- d0-d2 replays him, d3 is ours

Every turn of d0-d3 goes to a CSV: bank, shed MILK/WOOL/FERTILIZER, the farmer op, the hand ops and
the market orders, for both arms. The terminal gets the dawn table and the turns that differ.
"""

import argparse
import collections
import csv
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
PLANNER = (4, 5, 6, 7, 8, 9, 10, 11)
TAPE = (0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11)
WATCH = ("MILK", "WOOL", "FERTILIZER")


def _ops(a):
    return ([a.get("farmer") or ["PASS"]], list(a.get("hands") or []))


def _fmt(a):
    f, h = _ops(a)
    return (",".join(map(str, f[0])),
            " ".join("".join(str(y)[0] for y in x) for x in h),
            "  ".join(",".join(map(str, o)) for o in (a.get("market") or [])))


def play(rec, seat, seed, window, upto):
    """One arm. Returns `{turn: row}` and `{day: dawn}`."""
    import importlib
    import breakdown as B
    import us_in_his_seat as U
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    SA.REPLAY_OPENING_DAYS = tuple(window)
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    steps = rec["steps"]
    them = 1 - seat
    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
    env.reset(2)
    agent = SA.make_agent(sched, seat)

    rows, dawn = {}, {}
    for t in range((upto + 1) * TPD):
        d, h = divmod(t, TPD)
        o = env.state[seat].observation
        farm = o["farms"][seat]
        priv = o.get("private") or {}
        shed = collections.Counter(priv.get("shed") or {})
        n_us = len(farm.get("hands") or [])
        n_them = len(o["farms"][them].get("hands") or [])
        a = agent(o)
        mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                "market": a["market"]}
        fop, hop, mop = _fmt(mine)
        counts = collections.Counter()
        for op in [mine["farmer"]] + list(mine["hands"]):
            if op:
                counts[op[0]] += 1
        rows[t] = dict(turn=t, day=d, hour=h, bank=farm["money"], hands=n_us,
                       farmer=fop, hand_ops=hop, market=mop,
                       feed=counts["FEED"], care=counts["CARE"],
                       **{k.lower(): shed[k] for k in WATCH})
        if h == 0:
            dawn[d] = rows[t]
        at = U._recorded(steps, t, them)
        yours = {"farmer": at.get("farmer") or ["PASS"],
                 "hands": list(at.get("hands") or [])[:n_them],
                 "market": at.get("market") or []}
        env.step([mine, yours] if seat == 0 else [yours, mine])
        if env.done:
            break
    return rows, dawn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="97204026")
    ap.add_argument("--who", default="カワシギ")
    ap.add_argument("--upto", type=int, default=3)
    ap.add_argument("--csv", default="data/logs/the_opening_two_ways.csv")
    a = ap.parse_args()

    f = next(p for d in ("kawashigi", "kawashigi_b3", "kawa_2026-08-24", "leaders_2026-08-24",
                         "losses", "top_guys", "top2", "ladder", "our_games", "new_leader")
             for p in glob.glob(str(REPO / f"data/seed_scripts/{d}/{a.game}.json")))
    rec = json.loads(pathlib.Path(f).read_text())
    names = (rec.get("info") or {}).get("TeamNames") or []
    seat = names.index(a.who)
    seed = (rec.get("info") or {}).get("seed")

    pr, pd = play(rec, seat, seed, PLANNER, a.upto)
    tr, td = play(rec, seat, seed, TAPE, a.upto)

    out = pathlib.Path(REPO / a.csv)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as fh:
        w = None
        for t in sorted(set(pr) | set(tr)):
            for arm, src in (("planner", pr), ("tape", tr)):
                r = src.get(t)
                if r is None:
                    continue
                r = dict(arm=arm, **r)
                if w is None:
                    w = csv.DictWriter(fh, fieldnames=list(r))
                    w.writeheader()
                w.writerow(r)
    print(f"{a.game}  seed {seed}  vs {names[1 - seat]}\nrows -> {a.csv}\n")

    print("DAWN, planner arm vs tape arm")
    print(f"{'day':>4} {'bank pl/tp':>16} {'hands':>9} {'MILK':>9} {'WOOL':>9} {'FERTILIZER':>13}")
    for d in sorted(set(pd) & set(td)):
        p, q = pd[d], td[d]
        print(f"{d:>4} {p['bank']:>7,.0f}/{q['bank']:<8,.0f} {p['hands']:>4}/{q['hands']:<4} "
              f"{p['milk']:>4}/{q['milk']:<4} {p['wool']:>4}/{q['wool']:<4} "
              f"{p['fertilizer']:>6}/{q['fertilizer']:<6}")

    print("\nFEED and CARE per day, planner vs tape")
    for d in range(a.upto + 1):
        pf = sum(r["feed"] for r in pr.values() if r["day"] == d)
        tf = sum(r["feed"] for r in tr.values() if r["day"] == d)
        pc = sum(r["care"] for r in pr.values() if r["day"] == d)
        tc = sum(r["care"] for r in tr.values() if r["day"] == d)
        print(f"  d{d}  FEED {pf:>3}/{tf:<3}   CARE {pc:>3}/{tc:<3}")

    print("\nturns that differ, d0-d2")
    for t in sorted(set(pr) & set(tr)):
        p, q = pr[t], tr[t]
        if p["day"] > 2:
            break
        if (p["farmer"], p["hand_ops"], p["market"]) == (q["farmer"], q["hand_ops"], q["market"]):
            continue
        print(f"  d{p['day']} h{p['hour']:<2}  ${p['bank']:>6,.0f}/{q['bank']:<6,.0f}")
        print(f"     planner  {p['farmer']:<20} | {p['hand_ops']:<16} | {p['market']}")
        print(f"     tape     {q['farmer']:<20} | {q['hand_ops']:<16} | {q['market']}")


if __name__ == "__main__":
    main()
