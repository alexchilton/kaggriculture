"""Goods in a hand's pocket cannot be sold. How fast does each farm get them into the shed?

`HARVEST` and `COLLECT_FERTILIZER` put units into the ACTING UNIT's inventory
(`_farmer_inventory`), and only `DROP` moves them to `private["shed"]`, which is the only place a
SELL can settle from. So the chain is

    HARVEST -> (carry) -> walk to a shed tile -> DROP -> sellable

and every turn a unit spends carrying is a turn that stock is invisible to the market. That makes
"more work" and "better selling" the same lever rather than two: the extra trips are what make the
goods sellable sooner.

This measures, per seat: units carried vs units in the shed (turn-weighted), the DROP rate, and how
long the average unit of product sits in a pocket.

    python -u scripts/pocket_to_shed.py 107642213 107646523 107041112 107674019
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def main():
    print(f"{'episode':>10} {'team':18}{'carried':>9}{'in shed':>9}{'carry%':>8}"
          f"{'HARVEST':>9}{'DROP':>7}{'drops/harv':>11}{'PASS':>7}{'bank':>10}")
    for ep in sys.argv[1:]:
        rep = json.loads(find(int(ep)).read_text())
        teams = rep["info"]["TeamNames"]
        for seat, team in enumerate(teams):
            carried = inshed = 0
            harv = drop = pas = 0
            for step in rep["steps"]:
                cell = (step[seat] if seat < len(step) else None) or {}
                priv = (cell.get("observation") or {}).get("private") or {}
                for iv in priv.get("inventories") or []:
                    carried += sum(int(v or 0) for v in (iv or {}).values())
                inshed += sum(int(v or 0) for v in (priv.get("shed") or {}).values())
                a = cell.get("action") or {}
                for op in [a.get("farmer")] + list(a.get("hands") or []):
                    if not op:
                        continue
                    if op[0] in ("HARVEST", "COLLECT_FERTILIZER"):
                        harv += 1
                    elif op[0] == "DROP":
                        drop += 1
                    elif op[0] == "PASS":
                        pas += 1
            rew = (rep.get("rewards") or [0, 0])[seat] or 0
            tot = carried + inshed
            print(f"{ep:>10} {team[:18]:18}{carried:>9,}{inshed:>9,}"
                  f"{100*carried/max(1,tot):>8.1f}{harv:>9,}{drop:>7,}"
                  f"{drop/max(1,harv):>11.2f}{pas:>7,}{rew:>10,.0f}")


if __name__ == "__main__":
    main()
