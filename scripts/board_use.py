"""What each farm does with its 100 tiles, and how much of the day its units spend working.

The market arms are exhausted: the sell HOUR moves margin by tens of thousands only because holding
stock backs up a 100-unit shed and throws away harvests -- a production effect wearing a market
rule's clothes. The board is where those tens of thousands actually live.

`farms[opp]["tiles"]` is shared, so this is readable for BOTH seats from any observation -- it is
also, therefore, a signal a live agent could act on.

    python -u scripts/board_use.py 107642213 107646523 107399673 107041112 107674019
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def main():
    print(f"{'episode':>10} {'team':18}{'tiles':>7}{'crop':>6}{'pen':>5}{'weed':>6}{'empty':>7}"
          f"{'hands':>7}{'busy%':>7}{'harv':>6}{'bank':>10}")
    for ep in sys.argv[1:]:
        rep = json.loads(find(int(ep)).read_text())
        teams = rep["info"]["TeamNames"]
        steps = rep["steps"]
        for seat, team in enumerate(teams):
            # board at its fullest -- day 20, past the build-out, before the final liquidation
            snap = ((steps[20 * 24][seat] or {}).get("observation") or {})
            farm = (snap.get("farms") or [{}, {}])[seat] or {}
            kinds = collections.Counter()
            owned = 0
            for row in farm.get("tiles") or []:
                for tl in row:
                    if tl == "LOCKED":
                        continue
                    owned += 1
                    if not isinstance(tl, dict):
                        kinds["empty"] += 1
                    else:
                        k = tl.get("kind")
                        kinds["crop" if k == "PLANT" else
                              "weed" if k == "WEED" else "pen"] += 1
            busy = idle = harv = 0
            for step in steps[1:]:
                a = ((step[seat] if seat < len(step) else None) or {}).get("action") or {}
                for op in [a.get("farmer")] + list(a.get("hands") or []):
                    if not op:
                        continue
                    if op[0] == "PASS":
                        idle += 1
                    else:
                        busy += 1
                    if op[0] == "HARVEST":
                        harv += 1
            rew = (rep.get("rewards") or [0, 0])[seat] or 0
            hands = len(farm.get("hands") or [])
            print(f"{ep:>10} {team[:18]:18}{owned:>7}{kinds['crop']:>6}{kinds['pen']:>5}"
                  f"{kinds['weed']:>6}{kinds['empty']:>7}{hands:>7}"
                  f"{100*busy/max(1,busy+idle):>7.1f}{harv:>6}{rew:>10,.0f}")


if __name__ == "__main__":
    main()
