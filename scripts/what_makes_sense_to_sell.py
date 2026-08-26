"""Per product, per day: what does a unit GAIN by waiting until h16 instead of selling now?

This is the number every version of the shed-release rule has been guessing at. It is not a
guess -- both halves are deterministic and both are in the observation.

**Price is a pure function of inventory.** `market_price` (`reference/kaggriculture.py:192`)
reads the book and nothing else, floored at `PRICE_FLOOR`.

**The drain is a fixed schedule.** `_town_consume` (`:728`) runs every `townShopSellInterval`
steps (default 4) over `town["unlocked_shops"]`, removing `2 if len(products) == 1 else 1` of each
of that shop's products, plus every `townCenterSellInterval` steps (default 24) one unit of each
`TOWN_CENTER_PRODUCTS` -- which excludes FERTILIZER (`:114`). Shops are drawn WITH REPLACEMENT
(`:888`), so a seed can hold three yarn stores or none, and the same product is a different asset
on different seeds. That is the whole point of computing this per game instead of hardcoding a
tuple.

So the gain from waiting is exact:

    gain_per_unit = market_price(item, inv_at_h16) - market_price(item, inv_now)

where `inv_at_h16 = inv_now - (drain events between now and h16)`.

**What this deliberately ignores:** our own SELLs and the opponent's both ADD to the book between
now and h16, so a positive gain here is an UPPER bound on what waiting really pays. It is the
right bound for the decision -- if waiting does not pay even before anyone sells into it, it
certainly does not pay after.
"""

import argparse
import collections
import importlib.util
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

_spec = importlib.util.spec_from_file_location("kagref", REPO / "reference" / "kaggriculture.py")
KAG = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(KAG)

TPD = 24
LATE_HOUR = 16
TAPES = {
    "kawashigi": ("data/seed_scripts/kawa_2026-08-24/97466318.json",
                  "data/seed_scripts/kawashigi/schedule.json", 1240813987),
    "kawa_straw": ("data/seed_scripts/kawa_2026-08-24/97466318.json",
                   "data/seed_scripts/kawa_straw/schedule.json", 468411728),
}


def drain_between(step_now, step_target, shops, shop_iv, center_iv):
    """Units each product loses from the book over (step_now, step_target]."""
    out = collections.Counter()
    for t in range(step_now + 1, step_target + 1):
        if t % shop_iv == 0:
            for name in shops:
                prods = KAG.SHOPS.get(name, [])
                mult = 2 if len(prods) == 1 else 1
                for item in prods:
                    out[item] += mult
        if t % center_iv == 0:
            for item in KAG.TOWN_CENTER_PRODUCTS:
                out[item] += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="kawa_straw")
    ap.add_argument("--module", default="schedule_agent")
    args = ap.parse_args()

    import breakdown as B
    from kaggle_environments import make

    tape_path, sched_path, seed = TAPES[args.tape]
    SA = importlib.import_module(f"kagg.search.{args.module}")
    B.schedule_agent = SA
    raw = json.loads((REPO / sched_path).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    rec = json.loads((REPO / tape_path).read_text())
    steps = rec["steps"]
    names = (rec.get("info") or {}).get("TeamNames") or []
    his = names.index("カワシギ") if "カワシギ" in names else 0
    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    shop_iv = max(1, int(cfg.get("townShopSellInterval", 4)))
    center_iv = max(1, int(cfg.get("townCenterSellInterval", 24)))

    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
    env.reset(2)
    agent = SA.make_agent(sched, 0)

    gains = collections.defaultdict(list)   # product -> per-unit gain from waiting
    held = collections.Counter()            # product -> unit-turns held while pressed
    shop_census = collections.Counter()

    for t in range(30 * TPD):
        o = env.state[0].observation
        priv = o.get("private") or {}
        shed = {k: int(v or 0) for k, v in (priv.get("shed") or {}).items()}
        market = o.get("market") or {}
        inv = market.get("inventory") or {}
        shops = list((o.get("town") or {}).get("unlocked_shops") or [])
        day, hour = t // TPD, t % TPD

        if day >= 12 and hour < LATE_HOUR and sum(shed.values()) >= 90:
            for s in shops:
                shop_census[s] += 1
            d = drain_between(t, day * TPD + LATE_HOUR, shops, shop_iv, center_iv)
            for item in KAG.PRODUCTS:
                if shed.get(item, 0) <= 0:
                    continue
                now = KAG.market_price(item, inv.get(item, 0))
                later = KAG.market_price(item, inv.get(item, 0) - d.get(item, 0))
                gains[item].append(later - now)
                held[item] += shed[item]

        n = len(o["farms"][0].get("hands") or [])
        a = agent(o)
        mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n], "market": a["market"]}
        at = steps[t + 1][his].get("action") if t + 1 < len(steps) else None
        at = at if isinstance(at, dict) else {}
        n2 = len(o["farms"][1].get("hands") or [])
        yours = {"farmer": at.get("farmer") or ["PASS"],
                 "hands": list(at.get("hands") or [])[:n2],
                 "market": at.get("market") or []}
        env.step([mine, yours])
        if env.done:
            break

    print(f"\n=== {args.tape}  seed {seed} ===")
    print(f"  shops unlocked during pressed turns: "
          f"{dict(collections.Counter(s for s in shop_census.elements()).most_common())}")
    print(f"\n  {'product':<12} {'turns':>6} {'unit-turns':>11} {'price now':>10} "
          f"{'price h16':>10} {'gain/unit':>10}")
    rows = []
    for item, g in gains.items():
        if not g:
            continue
        rows.append((sum(g) / len(g), item, len(g), held[item]))
    for mean_gain, item, n_turns, unit_turns in sorted(rows):
        print(f"  {item:<12} {n_turns:>6} {unit_turns:>11,} "
              f"{'':>10} {'':>10} {mean_gain:>+10.2f}")
    print("\n  gain/unit is the UPPER bound on what waiting to h16 pays, before anyone")
    print("  sells into the book. Negative or zero => selling now is free or better.")


if __name__ == "__main__":
    main()
