"""Is the pocket-vs-shed gap uniform across crops, or only some? And does price gate the DROP?

Goods in a unit's inventory cannot be sold; only DROP makes them sellable. The aggregate gap is
large -- Majkel1337 carries 38-43% of his stock against binghua's 91% -- but an aggregate cannot say
whether that is one habit applied to everything or a decision taken per product.

Two cuts, same pass:

  per product   turn-weighted units carried vs units in the shed, so a crop that is always dropped
                fast is separable from one that rides around in a pocket all season
  vs price      the quoted price at the turns a DROP happens, against the product's own season
                median -- if the delivery is timed to a high market, DROP turns sit above it

    python -u scripts/carry_by_crop.py 107642213 107646523 107041112
"""
import collections, json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def main():
    for ep in sys.argv[1:]:
        rep = json.loads(find(int(ep)).read_text())
        teams = rep["info"]["TeamNames"]
        print(f"\n=== {ep}: {teams[0]} vs {teams[1]} ===")
        print(f"{'product':12}" + "".join(f"{t[:17]:>20}" for t in teams))
        print(f"{'':12}" + "".join(f"{'carried / shed':>20}" for _ in teams))
        carry = [collections.Counter(), collections.Counter()]
        shed = [collections.Counter(), collections.Counter()]
        droppx = [collections.defaultdict(list), collections.defaultdict(list)]
        allpx = collections.defaultdict(list)
        for t, step in enumerate(rep["steps"]):
            for seat in range(len(teams)):
                cell = (step[seat] if seat < len(step) else None) or {}
                obs = cell.get("observation") or {}
                priv = obs.get("private") or {}
                for iv in priv.get("inventories") or []:
                    for k, v in (iv or {}).items():
                        carry[seat][k] += int(v or 0)
                for k, v in (priv.get("shed") or {}).items():
                    shed[seat][k] += int(v or 0)
                px = (obs.get("market") or {}).get("prices") or {}
                if seat == 0:
                    for k, v in px.items():
                        allpx[k].append(v)
                a = cell.get("action") or {}
                for op in [a.get("farmer")] + list(a.get("hands") or []):
                    if op and op[0] == "DROP":
                        # DROP dumps the whole inventory; credit every product the unit could hold
                        for k, v in px.items():
                            droppx[seat][k].append(v)
        for p in PRODUCTS:
            row = f"{p:12}"
            for seat in range(len(teams)):
                c, s = carry[seat][p], shed[seat][p]
                if c + s == 0:
                    row += f"{'-':>20}"
                else:
                    row += f"{f'{100*c/(c+s):.0f}% / {s:,}':>20}"
            print(row)
        print(f"\n{'':12}price at DROP turns vs season median, per product")
        for p in PRODUCTS:
            pool = [x for x in allpx.get(p, []) if x is not None]
            if not pool:
                continue
            med = statistics.median(pool)
            row = f"{p:12}median {med:>6.0f}   "
            for seat in range(len(teams)):
                v = droppx[seat][p]
                row += (f"{teams[seat][:12]}: {statistics.median(v):>6.0f}   " if v
                        else f"{teams[seat][:12]}:      -   ")
            print(row)


if __name__ == "__main__":
    main()
