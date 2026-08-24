"""Every animal tile, day by day: where it stands, when it was placed, what it holds.

Alex, 2026-08-24: *"the order of the sheep/cow feed care and needing 5 turns to get the bonus as
opposed to 4, and it is only visible on an exact cow or sheep position."*

`kaggriculture.py:805-833` keys the yield off `placed_day`, not the buy:

    days_since_first = next_day - tile["placed_day"] - a["first_yield_day"]
    if days_since_first >= 0 and days_since_first % a["interval"] == 0:
        bonus = tile.pop("pending_care_bonus", 0) if tile["fed_today"] else 0
        tile["yield_units"] += 1 + bonus
    if tile["cared_today"] and tile["fed_today"]:
        tile["pending_care_bonus"] += 1

    COW    first_yield_day 8   interval 2   max_held 6   -> MILK
    SHEEP  first_yield_day 6   interval 3   max_held 6   -> WOOL

So placing an animal one day late shifts every yield it ever gives, and a CARE on a day without a
FEED banks nothing. Neither is visible in the shed -- `yield_units` sits on the TILE until a
HARVEST moves it -- which is why an earlier pass here read `MILK 0 / WOOL 0` and concluded, wrongly,
that nothing was being produced.

Both arms are his seat, on the game's own seed, against the same recorded opponent tape.
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
PLANNER = (4, 5, 6, 7, 8, 9, 10, 11)
TAPE = (0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11)


def _animals(farm):
    """`(x,y) -> (animal, placed_day, yield_units, pending_care_bonus, consecutive_unfed)`."""
    out = {}
    for y, row in enumerate(farm.get("tiles") or []):
        for x, t in enumerate(row):
            if isinstance(t, dict) and t.get("animal"):
                out[(x, y)] = (t["animal"], t.get("placed_day"), t.get("yield_units", 0),
                               t.get("pending_care_bonus", 0), t.get("consecutive_unfed", 0))
    return out


def play(rec, seat, seed, window, upto, live):
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
    agent = SA.make_agent(sched, seat) if live else None

    per_day, shed = {}, {}
    for t in range((upto + 1) * TPD):
        d, h = divmod(t, TPD)
        o = env.state[seat].observation
        farm = o["farms"][seat]
        if h == 0:
            per_day[d] = _animals(farm)
            shed[d] = collections.Counter((o.get("private") or {}).get("shed") or {})
        n_us = len(farm.get("hands") or [])
        n_them = len(o["farms"][them].get("hands") or [])
        if live:
            a = agent(o)
            mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                    "market": a["market"]}
        else:
            a = U._recorded(steps, t, seat)
            mine = {"farmer": a.get("farmer") or ["PASS"],
                    "hands": list(a.get("hands") or [])[:n_us],
                    "market": a.get("market") or []}
        at = U._recorded(steps, t, them)
        yours = {"farmer": at.get("farmer") or ["PASS"],
                 "hands": list(at.get("hands") or [])[:n_them],
                 "market": at.get("market") or []}
        env.step([mine, yours] if seat == 0 else [yours, mine])
        if env.done:
            break
    return per_day, shed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="92417234")
    ap.add_argument("--who", default="カワシギ")
    ap.add_argument("--upto", type=int, default=8)
    ap.add_argument("--window", default="planner", choices=("planner", "tape"))
    a = ap.parse_args()

    f = next(p for d in ("kawashigi", "kawashigi_b3", "kawa_2026-08-24", "leaders_2026-08-24",
                         "losses", "top_guys", "top2", "ladder", "our_games", "new_leader")
             for p in glob.glob(str(REPO / f"data/seed_scripts/{d}/{a.game}.json")))
    rec = json.loads(pathlib.Path(f).read_text())
    names = (rec.get("info") or {}).get("TeamNames") or []
    seat = names.index(a.who)
    seed = (rec.get("info") or {}).get("seed")
    win = PLANNER if a.window == "planner" else TAPE

    ours, oshed = play(rec, seat, seed, win, a.upto, live=True)
    his, hshed = play(rec, seat, seed, win, a.upto, live=False)

    print(f"{a.game}  seed {seed}  vs {names[1 - seat]}   window={a.window} {win}\n")
    print("HIS recording, then OURS. Each animal: kind@(x,y) placed=d  held=n  carebank=n")
    for d in sorted(set(ours) & set(his)):
        def line(m, sh):
            if not m:
                return "(none)"
            return "  ".join(
                f"{v[0][:2]}@{k} pl={v[1]} held={v[2]} cb={v[3]}"
                + ("!" if v[4] else "")
                for k, v in sorted(m.items())) + f"   shed MILK {sh['MILK']} WOOL {sh['WOOL']}"
        print(f"\n d{d}")
        print(f"   his   {line(his[d], hshed[d])}")
        print(f"   ours  {line(ours[d], oshed[d])}")
        if set(his[d]) != set(ours[d]):
            print(f"   -> tiles differ: his {sorted(set(his[d]) - set(ours[d]))}  "
                  f"ours {sorted(set(ours[d]) - set(his[d]))}")


if __name__ == "__main__":
    main()
