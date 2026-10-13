"""First into a product's book versus second: what each side realises, same board, same crop.

The book is SHARED and `market_price` falls as it fills, so a sale is two things at once -- revenue
for the seller and a worse price for everyone else. Where the town drains the product back that is
temporary. Where it does not, it is permanent denial:

    FERTILIZER is carried by NO shop and is excluded from TOWN_CENTER_PRODUCTS, so its inventory
    never falls. Whoever sells it first takes the top of the curve and the opponent can never get
    it back.

That makes "dump the fertilizer" adversarial rather than careless, and the ladder is scored on match
outcome, not bank -- so revenue denied counts like revenue earned.

For each product in each episode this reports who filled FIRST and what each side realised per unit.

    python -u scripts/first_strike.py 107642213 107646523 107399673 107041112
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]
NEVER_DRAINS = ("FERTILIZER",)


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def fills_of(ep):
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
    return teams, fills.events


def main():
    score = collections.Counter()
    for ep in sys.argv[1:]:
        teams, ev = fills_of(int(ep))
        first, u, r = {}, collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
        for e in ev:
            if e["op"] != "SELL":
                continue
            k = (e["item"], e["seat"])
            t = e["day"] * 24 + e["hour"]
            if k not in first or t < first[k]:
                first[k] = t
            u[e["item"]][e["seat"]] += 1
            r[e["item"]][e["seat"]] += e["price"]
        print(f"\n=== {ep}: {teams[0]} vs {teams[1]} ===")
        print(f"{'product':12}{'first in':>18}{'their $/u':>11}{'other $/u':>11}"
              f"{'edge':>8}   drains?")
        for prod in sorted(u):
            t0, t1 = first.get((prod, 0)), first.get((prod, 1))
            if t0 is None or t1 is None:
                continue
            lead = 0 if t0 < t1 else 1
            a = r[prod][lead] / max(1, u[prod][lead])
            b = r[prod][1 - lead] / max(1, u[prod][1 - lead])
            drains = "no -- permanent" if prod in NEVER_DRAINS else "yes"
            print(f"{prod:12}{teams[lead][:16]:>18}{a:>11.0f}{b:>11.0f}{a-b:>8.0f}   {drains}")
            score["first_better" if a > b else "first_worse"] += 1
            if prod in NEVER_DRAINS:
                score["fert_first_better" if a > b else "fert_first_worse"] += 1
    print(f"\nfirst mover realised MORE on {score['first_better']} product-episodes, "
          f"LESS on {score['first_worse']}")
    print(f"   fertilizer alone (book never recovers): first better "
          f"{score['fert_first_better']}, worse {score['fert_first_worse']}")


if __name__ == "__main__":
    main()
