"""The hour our bank parts from his, and the order that did it.

`92466371` replays its OWN recording -- 192 of 192 turns on d4-d11 are identical -- and our bank
still sits $119 below his from d5 onward, which costs the last HIRE of d7 and leaves us one hand
short for the rest of the season. A constant offset is one transaction, not drift, so this prints
the bank every hour for both arms and marks the hour the difference changes.
"""

import argparse
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="92466371")
    ap.add_argument("--who", default="カワシギ")
    ap.add_argument("--lo", type=int, default=3)
    ap.add_argument("--hi", type=int, default=7)
    a = ap.parse_args()

    import glob
    import importlib
    import breakdown as B
    import us_in_his_seat as U
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    f = next(p for d in ("kawashigi", "kawashigi_b3", "kawa_2026-08-24", "leaders_2026-08-24",
                         "losses", "top_guys", "top2", "ladder", "our_games", "new_leader")
            for p in glob.glob(str(REPO / f"data/seed_scripts/{d}/{a.game}.json")))
    rec = json.loads(pathlib.Path(f).read_text())
    names = (rec.get("info") or {}).get("TeamNames") or []
    seat = names.index(a.who)
    seed = (rec.get("info") or {}).get("seed")
    steps = rec["steps"]
    them = 1 - seat

    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
    env.reset(2)
    agent = SA.make_agent(sched, seat)

    print(f"{a.game}  seed {seed}  vs {names[1 - seat]}   seat {seat}\n")
    print(f"{'turn':>5} {'d':>3} {'h':>3} {'his bank':>9} {'our bank':>9} {'gap':>8} "
          f"{'d gap':>7}  what changed")
    prev_gap = None
    for t in range((a.hi + 1) * TPD):
        o = env.state[seat].observation
        ours = o["farms"][seat]["money"]
        his = (steps[t][seat]["observation"]["farms"][seat]["money"]
               if t < len(steps) else None)
        n_us = len(o["farms"][seat].get("hands") or [])
        n_them = len(o["farms"][them].get("hands") or [])
        act = agent(o)
        mine = {"farmer": act["farmer"], "hands": list(act["hands"] or [])[:n_us],
                "market": act["market"]}
        his_a = U._recorded(steps, t, seat)

        d, h = divmod(t, TPD)
        if his is not None and d >= a.lo:
            gap = ours - his
            dg = None if prev_gap is None else gap - prev_gap
            note = ""
            if dg:
                hm = [list(x) for x in (his_a.get("market") or [])]
                om = [list(x) for x in (mine["market"] or [])]
                note = f"his mkt {hm}  ours {om}"
            print(f"{t:>5} {d:>3} {h:>3} {his:>9,.0f} {ours:>9,.0f} {gap:>+8,.0f} "
                  f"{('' if not dg else format(dg, '+,.0f')):>7}  {note}"[:230])
            prev_gap = gap
        elif his is not None:
            prev_gap = ours - his

        at = U._recorded(steps, t, them)
        yours = {"farmer": at.get("farmer") or ["PASS"],
                 "hands": list(at.get("hands") or [])[:n_them],
                 "market": at.get("market") or []}
        env.step([mine, yours] if seat == 0 else [yours, mine])
        if env.done:
            break


if __name__ == "__main__":
    main()
