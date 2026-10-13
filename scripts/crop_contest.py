"""Realised price against BASE price, per crop -- which books are crowded and which are empty.

A crop's worth is not its base price. `market_price` falls as the book fills, so what a crop pays is
base x (how much the town absorbs) / (how much BOTH farms push into it). A crop nobody else plants
keeps a thin book and trades ABOVE base; a crop everyone grows trades far below.

That makes an "obviously weak" crop the interesting one: TOMATO's base is 60, four of the eight
shops carry it, and on 107642213 Majkel1337 sold 127 units at $86 -- 43% ABOVE base -- against an
opponent who planted none.

Prices come from `kagg/analysis/fills.py`, so these are realised, not offered.

    python -u scripts/crop_contest.py 107642213 107646523 107041112 107674019 107399673
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import kaggle_environments.envs.kaggriculture.kaggriculture as K

DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def main():
    rows = collections.defaultdict(list)
    for ep in sys.argv[1:]:
        rep = json.loads(find(int(ep)).read_text())
        teams, seed = rep["info"]["TeamNames"], rep["info"]["seed"]
        cfg = dict(rep.get("configuration") or {})
        cfg.pop("seed", None)

        def tape(seat):
            acts = [(s or {}).get("action") or {} for s in (step[seat] for step in rep["steps"][1:])]
            idle = {"farmer": ["PASS"], "hands": [], "market": []}
            box = {"t": 0}

            def f(obs):
                i = box["t"]
                box["t"] += 1
                if i >= len(acts):
                    return idle
                a = acts[i]
                return {"farmer": a.get("farmer", ["PASS"]) or ["PASS"],
                        "hands": list(a.get("hands") or []), "market": list(a.get("market") or [])}
            return f

        from kaggle_environments import make
        from kagg.analysis.fills import record_fills
        env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=True)
        env.reset(2)
        with record_fills(env) as fills:
            env.run([tape(0), tape(1)])
        u = collections.defaultdict(collections.Counter)
        r = collections.defaultdict(collections.Counter)
        for e in fills.events:
            if e["op"] == "SELL":
                u[e["item"]][e["seat"]] += 1
                r[e["item"]][e["seat"]] += e["price"]
        for item in u:
            tot = sum(u[item].values())
            for seat in u[item]:
                base = (K.MARKET_PARAMS.get(item) or {}).get("base", 0)
                got = r[item][seat] / max(1, u[item][seat])
                rows[item].append((teams[seat], u[item][seat], tot, got, base))
    print(f"{'crop':12}{'base':>6}{'realised':>10}{'vs base':>9}{'units in book':>15}"
          f"{'seasons':>9}")
    for item in sorted(rows, key=lambda i: -(sum(x[3] for x in rows[i]) / len(rows[i])
                                             / max(1, rows[i][0][4]))):
        v = rows[item]
        got = sum(x[3] for x in v) / len(v)
        base = v[0][4]
        tot = sum(x[2] for x in v) / len(v)
        print(f"{item:12}{base:>6}{got:>10.0f}{100*got/max(1,base)-100:>8.0f}%{tot:>15,.0f}"
              f"{len(v):>9}")


if __name__ == "__main__":
    main()
