"""The first turn our agent's action differs from his recorded one -- and WHY.

Alex, 2026-08-24: *"the same first shop gives five different divergence days -- I assume he doesn't
always manage to buy the land or whatever the difference is. Do we need to behave differently like
him then?"*

That is the hypothesis this tests. The shop draw does NOT explain the divergence day
(`data/logs/what_breaks_the_replay.log`: SMOOTHIE_SHOP towns break at d8, d9, d10, d11 and d13
alike), so the cause is something continuous rather than a branch. The obvious candidate is the
BANK: a purchase his recording could afford, ours cannot, because the market was contested
differently -- `matching-the-tape` records a case where **$35** flipped a $4,000 land purchase.

Both arms are his seat, on the game's own seed, against the same recorded opponent tape. At every
turn this compares the action our agent SUBMITS against the action he recorded, and stops at the
first difference, printing:

    the turn, day and hour
    both banks at that moment
    his action and ours, side by side

If the first difference is a purchase that he made and we did not, with our bank below its price,
the hypothesis is confirmed and the fix is about money arriving earlier, not about branching.
If the first difference is a MOVE or a work op with both banks equal, it is not the bank.

`prices` matter here: a SELL that filled at his prices may not fill at ours, so the bank can drift
before any action differs. The bank columns are printed for exactly that reason.
"""

import argparse
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
BUYS = ("BUY_LAND", "BUY_ANIMAL", "BUY_SEED", "BUY_PRODUCT", "HIRE")


def _norm(a):
    """A comparable form: farmer op, hand ops, market orders."""
    if not isinstance(a, dict):
        return (("PASS",), (), ())
    f = tuple(a.get("farmer") or ["PASS"])
    h = tuple(tuple(x) for x in (a.get("hands") or []))
    m = tuple(tuple(x) for x in (a.get("market") or []))
    return (f, h, m)


def run(rec, his_seat, seed, stop_after=None):
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
    agent = SA.make_agent(sched, his_seat)

    out = []
    for t in range(30 * TPD):
        o = env.state[his_seat].observation
        our_bank = o["farms"][his_seat]["money"]
        his_bank = (steps[t][his_seat]["observation"]["farms"][his_seat]["money"]
                    if t < len(steps) else None)
        n_us = len(o["farms"][his_seat].get("hands") or [])
        n_them = len(o["farms"][them].get("hands") or [])

        a = agent(o)
        mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                "market": a["market"]}
        his = U._recorded(steps, t, his_seat)
        his_trim = {"farmer": his.get("farmer") or ["PASS"],
                    "hands": list(his.get("hands") or [])[:n_us],
                    "market": his.get("market") or []}

        if _norm(mine) != _norm(his_trim):
            out.append((t, our_bank, his_bank, his_trim, mine))
            if stop_after is not None and len(out) >= stop_after:
                return out

        at = U._recorded(steps, t, them)
        yours = {"farmer": at.get("farmer") or ["PASS"],
                 "hands": list(at.get("hands") or [])[:n_them],
                 "market": at.get("market") or []}
        # The env is driven by OUR agent's action, so the board follows our arm from here on.
        env.step([mine, yours] if his_seat == 0 else [yours, mine])
        if env.done:
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", default="97204026,97210773,97219939")
    ap.add_argument("--who", default="カワシギ")
    ap.add_argument("--show", type=int, default=6, help="how many differing turns to print")
    a = ap.parse_args()

    import glob
    files = {}
    for d in ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c",
              "leaders_2026-08-24", "kawa_2026-08-24", "losses", "top_guys", "top2",
              "new_leader", "ladder", "our_games"):
        for f in glob.glob(str(REPO / f"data/seed_scripts/{d}/*.json")):
            files.setdefault(pathlib.Path(f).stem, f)

    for ep in a.games.split(","):
        f = files.get(ep)
        if f is None:
            print(f"{ep}: not found")
            continue
        rec = json.loads(pathlib.Path(f).read_text())
        names = (rec.get("info") or {}).get("TeamNames") or []
        if a.who not in names:
            continue
        seat = names.index(a.who)
        seed = (rec.get("info") or {}).get("seed")
        print(f"\n########## {ep}  seed {seed}  vs {names[1 - seat]}")
        diffs = run(rec, seat, seed, stop_after=a.show)
        if not diffs:
            print("  no differing action all season")
            continue
        for t, ours_bank, his_bank, his, mine in diffs:
            d, h = divmod(t, TPD)
            print(f"\n  turn {t} = d{d} h{h}   his bank ${his_bank:,.0f}   "
                  f"our bank ${ours_bank:,.0f}   gap ${ours_bank - (his_bank or 0):+,.0f}")
            print(f"    his   farmer {his['farmer']}  hands {his['hands']}")
            print(f"          market {his['market']}")
            print(f"    ours  farmer {mine['farmer']}  hands {mine['hands']}")
            print(f"          market {mine['market']}")
            hm = {tuple(o)[:1] for o in his["market"] if o}
            om = {tuple(o)[:1] for o in mine["market"] if o}
            missing = [o for o in his["market"] if o and o[0] in BUYS
                       and tuple(o) not in {tuple(x) for x in mine["market"]}]
            if missing:
                print(f"    -> he BUYS what we do not: {missing}")


if __name__ == "__main__":
    main()
