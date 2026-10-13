"""Units that ACTUALLY traded per SELL, from the engine -- not the number written in the order.

`shedCapacity` is 100, so `SELL CARROT 1000` cannot move 1000 units: the engine fills
`min(order, shed)` one unit at a time, and a 1000 written in an order is a "sell everything I hold"
sentinel. Comparing the NUMBERS in two agents' orders therefore compares their idioms, not their
trading, and reading a dump into a 1000 is wrong.

This replays a recorded episode through the real engine with both sides' recorded actions and reads
`kagg/analysis/fills.py`, which wraps `_commit_unit` -- the one function that moves shed and money
together, once per unit. That gives units and revenue per turn per product, per seat, exactly.

    python -u scripts/real_sell_sizes.py 107041112
"""
import collections, json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def main():
    ep = int(sys.argv[1])
    path = find(ep)
    rep = json.loads(path.read_text())
    teams = rep["info"]["TeamNames"]
    seed = rep["info"]["seed"]
    cfg = dict(rep.get("configuration") or {})
    cfg.pop("seed", None)

    def tape(seat):
        acts = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
                 "hands": list((s.get("action") or {}).get("hands") or []),
                 "market": list((s.get("action") or {}).get("market") or [])}
                for s in (step[seat] or {} for step in rep["steps"][1:])]
        idle = {"farmer": ["PASS"], "hands": [], "market": []}
        box = {"t": 0}

        def f(obs):
            i = box["t"]
            box["t"] += 1
            return acts[i] if i < len(acts) else idle
        return f

    from kaggle_environments import make
    from kagg.analysis.fills import record_fills
    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=True)
    env.reset(2)
    with record_fills(env) as fills:
        env.run([tape(0), tape(1)])

    print(f"episode {ep}  seed {seed}  teams {teams}\n")
    for seat, team in enumerate(teams):
        per_turn = collections.defaultdict(collections.Counter)   # (day,hour,item) -> units
        rev = collections.Counter()
        for e in fills.events:
            if e["seat"] != seat or e["op"] != "SELL":
                continue
            per_turn[(e["day"], e["hour"], e["item"])]["n"] += 1
            per_turn[(e["day"], e["hour"], e["item"])]["$"] += e["price"]
            rev[e["item"]] += e["price"]
        sizes = [v["n"] for v in per_turn.values()]
        if not sizes:
            print(f"{team}: no sells recorded")
            continue
        print(f"{team}: {len(sizes)} product-turns traded, {sum(sizes):,} units, "
              f"${sum(rev.values()):,.0f}")
        print(f"   units per product-turn: median {statistics.median(sizes):.0f}  "
              f"mean {statistics.mean(sizes):.1f}  p90 {sorted(sizes)[int(.9*len(sizes))]}  "
              f"max {max(sizes)}  >=20: {100*sum(1 for s in sizes if s>=20)/len(sizes):.1f}%")
        byp = collections.defaultdict(list)
        for (d, h, it), v in per_turn.items():
            byp[it].append(v["n"])
        print("   " + "  ".join(f"{k[:5]}:{statistics.median(v):.0f}"
                                for k, v in sorted(byp.items())))


if __name__ == "__main__":
    main()
