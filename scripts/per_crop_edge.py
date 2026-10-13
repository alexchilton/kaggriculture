"""Per crop, head to head on the same board: who realises more per unit, and by how much.

Both seats trade one book on one seed, so a per-product $/unit gap between them is a like-for-like
comparison -- same price curve, same drain clock, same 30 days. Aggregating across episodes hides
which goods the edge is actually in.

Units and revenue come from `kagg/analysis/fills.py` (per-unit truth), so no offers are counted.

    python -u scripts/per_crop_edge.py 107642213 107646523 ...
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
    out = {}
    for seat, team in enumerate(teams):
        u, r, hrs = collections.Counter(), collections.Counter(), collections.defaultdict(list)
        for e in fills.events:
            if e["seat"] == seat and e["op"] == "SELL":
                u[e["item"]] += 1
                r[e["item"]] += e["price"]
                hrs[e["item"]].append(e["day"])
        out[seat] = (team, u, r, hrs)
    return out


def main():
    for ep in sys.argv[1:]:
        res = one(int(ep))
        (t0, u0, r0, h0), (t1, u1, r1, h1) = res[0], res[1]
        print(f"\n=== {ep}:  {t0}  vs  {t1} ===")
        print(f"{'product':12}{t0[:13]:>26}{t1[:13]:>26}{'$/u gap':>10}{'median day':>14}")
        print(f"{'':12}{'units  $/u  rev':>26}{'units  $/u  rev':>26}")
        for p in sorted(set(u0) | set(u1)):
            a = r0[p] / u0[p] if u0[p] else 0
            b = r1[p] / u1[p] if u1[p] else 0
            d0 = sorted(h0[p])[len(h0[p]) // 2] if h0[p] else -1
            d1 = sorted(h1[p])[len(h1[p]) // 2] if h1[p] else -1
            print(f"{p:12}{u0[p]:>8,}{a:>7.0f}{r0[p]:>11,.0f}"
                  f"{u1[p]:>8,}{b:>7.0f}{r1[p]:>11,.0f}{b - a:>10.0f}{f'{d0} vs {d1}':>14}")
        print(f"{'TOTAL':12}{sum(u0.values()):>8,}"
              f"{sum(r0.values())/max(1,sum(u0.values())):>7.0f}{sum(r0.values()):>11,.0f}"
              f"{sum(u1.values()):>8,}"
              f"{sum(r1.values())/max(1,sum(u1.values())):>7.0f}{sum(r1.values()):>11,.0f}")


if __name__ == "__main__":
    main()
