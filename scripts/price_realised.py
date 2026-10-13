"""Dollars per unit actually sold, per product, per seat -- the clean measure of sell timing.

Units and revenue both come from `kagg/analysis/fills.py`, which wraps `_commit_unit`, so this is
what traded and what it fetched. Two agents on the SAME board share one book and one price curve,
so their $/unit is directly comparable: the one with the higher figure chose better moments for the
same goods.

Order SIZE cannot answer this -- `shedCapacity` is 100 and `SELL x 1000` is a "sell all I hold"
sentinel that fills a handful of units like any other.

    python -u scripts/price_realised.py 107041112 107064978 ...
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def one(ep):
    rep = json.loads(find(ep).read_text())
    teams, seed = rep["info"]["TeamNames"], rep["info"]["seed"]
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
    out = {}
    for seat, team in enumerate(teams):
        u, r = collections.Counter(), collections.Counter()
        for e in fills.events:
            if e["seat"] == seat and e["op"] == "SELL":
                u[e["item"]] += 1
                r[e["item"]] += e["price"]
        out[seat] = (team, u, r)
    return out


def main():
    tot = collections.defaultdict(lambda: [collections.Counter(), collections.Counter()])
    for ep in sys.argv[1:]:
        try:
            res = one(int(ep))
        except Exception as e:
            print(f"{ep}: {type(e).__name__} {e}", flush=True)
            continue
        line = []
        for _seat, (team, u, r) in res.items():
            tot[team][0].update(u)
            tot[team][1].update(r)
            line.append(f"{team} {sum(r.values())/max(1,sum(u.values())):.1f}/u")
        print(f"{ep}: " + "   vs   ".join(line), flush=True)
    print(f"\n{'team':22}{'units':>9}{'revenue':>13}{'$/unit':>9}   per-product $/unit")
    for team, (u, r) in sorted(tot.items(), key=lambda kv: -sum(kv[1][1].values())/max(1, sum(kv[1][0].values()))):
        pp = "  ".join(f"{k[:5]}:{r[k]/u[k]:.0f}" for k in sorted(u) if u[k])
        print(f"{team[:22]:22}{sum(u.values()):>9,}{sum(r.values()):>13,.0f}"
              f"{sum(r.values())/max(1,sum(u.values())):>9.1f}   {pp}")


if __name__ == "__main__":
    main()
