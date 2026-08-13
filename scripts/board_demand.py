"""Which boards can absorb what we produce, and does Seb change what he produces?

**Part A -- the board's absorption, measured exactly rather than modelled.**
Run PASS against PASS. Nobody sells, so `market["inventory"]` only ever falls, and the drop from
`MARKET_I0` is precisely the number of units the town removes over the season on that board. That
is the quantity both players are competing to sell into: sell more than it between them and the
surplus sits above `I0`, where WOOL reaches the $1 floor 59 units up and MILK 76
(`docs/the_book_is_shallow_2026-08-09.md`).

No agent behaviour is involved, so the figure is a property of the board alone.

**Part B -- does the strongest adaptive opponent change his production?**
Seb is the one top-ranked player whose traces are not identical game to game. If his PLANT and
BUY_ANIMAL decisions differ across games that drew different shops, adaptation of the production
mix is a thing real leaders do, and our fixed target sheet is giving something away. If they are
constant and only his selling moves, the schedule is fine and the whole gap is in the market.

    PYTHONPATH=. python3 -u scripts/board_demand.py
"""

import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
HI = ("MILK", "WOOL", "STRAWBERRY", "MELON")

#: What our fixed schedule actually produces in a season, measured over seeds 13/17/29/41
#: (`data/logs/why_not_sold_seeds.log`). Used only to say whether a board can take it.
OUR_OUTPUT = {"MILK": 235, "WOOL": 160, "STRAWBERRY": 280, "MELON": 82}


def absorption(seed):
    """Units the town removes over a whole season, per product. Board property, no agent involved."""
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    idle = [{"farmer": ["PASS"], "hands": [], "market": []} for _ in (0, 1)]
    for _t in range(24 * 30):
        if env.done:
            break
        env.step(idle)
    o = env.state[0].observation
    inv = (o.get("market") or {}).get("inventory") or {}
    shops = list((o.get("town") or {}).get("unlocked_shops") or [])
    sys.path.insert(0, str(REPO / "reference"))
    import kaggriculture as kg
    return ({p: kg.MARKET_I0 - int(inv.get(p, kg.MARKET_I0)) for p in HI}, shops)


def seb_production():
    """PLANT crops and BUY_ANIMAL orders for every Seb seat we hold, one row per game."""
    out = []
    for path in sorted(glob.glob(str(REPO / "data/seed_scripts/top_guys/*.json"))):
        try:
            d = json.loads(pathlib.Path(path).read_text())
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        names = (d.get("info") or {}).get("TeamNames") or []
        seats = [i for i, n in enumerate(names) if "Seb" in str(n)]
        if not seats:
            continue
        cfg = d.get("configuration") or {}
        for seat in seats:
            plants, animals = collections.Counter(), collections.Counter()
            for step in (d.get("steps") or []):
                if seat >= len(step):
                    continue
                act = (step[seat] or {}).get("action") or {}
                if not isinstance(act, dict):
                    continue
                farmer = act.get("farmer") or []
                if isinstance(farmer, list) and len(farmer) >= 2 and farmer[0] == "PLANT":
                    plants[farmer[1]] += 1
                for hand in (act.get("hands") or []):
                    if isinstance(hand, list) and len(hand) >= 2 and hand[0] == "PLANT":
                        plants[hand[1]] += 1
                for o in (act.get("market") or []):
                    if isinstance(o, list) and len(o) >= 2 and o[0] == "BUY_ANIMAL":
                        animals_offered[o[1]] += int(o[2]) if len(o) > 2 else 1
            out.append({"game": pathlib.Path(path).stem, "seat": seat,
                        "interval": cfg.get("townCenterSellInterval"),
                        "plants": dict(plants), "animals_offered": dict(animals)})
    return out


def main():
    print("=" * 100)
    print("PART A -- what each board will absorb (PASS vs PASS: nobody sells, so this is the town alone)")
    print("=" * 100)
    print(f"{'seed':>5} " + "".join(f"{p:>13}" for p in HI) + "   verdict")
    print(f"{'ours':>5} " + "".join(f"{OUR_OUTPUT[p]:>13}" for p in HI)
          + "   <- units our fixed schedule produces")
    print("-" * 100)

    rows = []
    for seed in [13, 17, 29, 41, 53, 67, 11, 19, 23, 31, 37, 43]:
        drain, shops = absorption(seed)
        short = [p for p in HI if drain[p] < OUR_OUTPUT[p] * 0.5]
        rows.append((seed, drain, shops, short))
        verdict = ("OK" if not short else "STARVED: " + ",".join(short))
        print(f"{seed:>5} " + "".join(f"{drain[p]:>13}" for p in HI) + f"   {verdict}")

    print("\n  A board absorbing under half what we make cannot pay for it at any sell cadence:")
    print("  the surplus sits above I0 where the price is on its way to the floor.\n")
    for seed, drain, shops, short in rows:
        if short:
            print(f"  seed {seed:>3}  shops drawn: {collections.Counter(shops)}")

    print()
    print("=" * 100)
    print("PART B -- does Seb change what he PRODUCES between games?")
    print("=" * 100)
    for r in seb_production():
        print(f"  {r['game']:<12} seat {r['seat']}  interval={r['interval']}")
        print(f"      plants  {r['plants']}")
        print(f"      animals {r['animals_offered']}")


if __name__ == "__main__":
    sys.exit(main())
