"""Are the dear crops PLANTED nearer the shed than the cheap ones?

Delivery is a walk: `HARVEST` fills the acting unit's inventory and only a `DROP` on a shed-access
tile makes the goods sellable. The shed tiles are fixed at the board's centre -- (4,4) (5,4) (4,5)
(5,5) -- so the distance from a planted tile to the shed is a property of the LAYOUT, decided when
the crop goes in the ground, hours before any selling decision.

If the carry ranking measured earlier (Majkel1337 delivers melon first and leaves wheat in pockets)
is supported by geometry rather than by routing alone, the dear crops sit closer.

Distance is Chebyshev: a unit may move diagonally, so `max(|dx|, |dy|)` is the turn count.

    python -u scripts/crop_geometry.py 107642213 107041112 107646523
"""
import collections, json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import kaggle_environments.envs.kaggriculture.kaggriculture as K

DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]
SHED = [(4, 4), (5, 4), (4, 5), (5, 5)]


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def dist(x, y):
    return min(max(abs(x - sx), abs(y - sy)) for sx, sy in SHED)


def main():
    pooled = collections.defaultdict(list)
    for ep in sys.argv[1:]:
        rep = json.loads(find(int(ep)).read_text())
        teams = rep["info"]["TeamNames"]
        print(f"\n=== {ep}: {teams[0]} vs {teams[1]} ===")
        print(f"{'crop':12}{'base $':>8}" + "".join(f"{t[:17]:>20}" for t in teams))
        print(f"{'':12}{'':8}" + "".join(f"{'median dist / n':>20}" for _ in teams))
        # every tile that ever carried a PLANT of each crop, and where pens sit
        seen = [collections.defaultdict(set), collections.defaultdict(set)]
        for step in rep["steps"]:
            for seat in range(len(teams)):
                obs = ((step[seat] if seat < len(step) else None) or {}).get("observation") or {}
                farm = (obs.get("farms") or [None, None])[seat]
                if not farm:
                    continue
                for y, row in enumerate(farm.get("tiles") or []):
                    for x, tl in enumerate(row):
                        if isinstance(tl, dict):
                            if tl.get("kind") == "PLANT":
                                seen[seat][tl.get("crop")].add((x, y))
                            elif tl.get("animal"):
                                seen[seat]["pen:" + str(tl.get("animal"))].add((x, y))
        def base_of(k):
            """Market base price of what a tile YIELDS -- a pen is named by its animal."""
            if str(k).startswith("pen:"):
                a = str(k).split(":", 1)[1]
                yields = {"COW": "MILK", "SHEEP": "WOOL", "GOOSE": "EGG"}.get(a)
                k = yields or a
            return (K.MARKET_PARAMS.get(k, {}) or {}).get("base", 0) if hasattr(K, "MARKET_PARAMS") \
                else 0

        keys = sorted(set(seen[0]) | set(seen[1]), key=lambda k: -base_of(k))
        for k in keys:
            row = f"{str(k)[:12]:12}{base_of(k):>8.0f}"
            for seat in range(len(teams)):
                d = [dist(x, y) for x, y in seen[seat][k]]
                row += f"{f'{statistics.median(d):.1f} / {len(d)}':>20}" if d else f"{'-':>20}"
                if d and not str(k).startswith("pen"):
                    pooled[(teams[seat], k)] += d
            print(row)


if __name__ == "__main__":
    main()
