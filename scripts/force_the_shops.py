"""Set the town's shops directly instead of scanning seeds for a draw. Verified, not assumed.

Three days went into finding seeds whose CARROT drain landed in a bucket, and the last scan of 60
seeds produced **one** seed in bucket 7-9 and **none** in 10+. The draw does not need to be found:
`_town_consume` reads `town.get("unlocked_shops", [])` off the live observation on every turn
(`reference/kaggriculture.py:739`), and `_end_of_day` appends to that same list. Overwrite it each
turn and the drain is exactly what we choose.

CARROT appears in two shops:

    PET_CAFE        ["CARROT"]                                   -> multiplier 2 (single product)
    FARMERS_MARKET  ["WHEAT","CARROT","TOMATO","STRAWBERRY"]     -> multiplier 1

so `k` pet cafes give `2k` carrot units removed every `townShopSellInterval` (4) steps, plus 1 per
`townCenterSellInterval` (24) from the town centre. A target drain is a shop list, not a seed.

`MAX_SHOP_INSTANCES` still caps the list, and it is respected here rather than worked around.

This module is the mechanism plus its proof. `--verify` measures the CARROT book actually falling
in a real episode and checks it against the arithmetic above; if those disagree, the forcing does
not work and nothing built on it should be believed.

    python -u scripts/force_the_shops.py --verify
"""

import argparse
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}


def shops_for_drain(product, target):
    """A shop list whose per-tick drain of `product` is `target`, or as close as the cap allows.

    Greedy on the largest contributor first, so the instance cap buys the most drain. A single
    product shop counts double (`multiplier = 2 if len(products) == 1`), which is why PET_CAFE and
    YARN_STORE reach high drains that no mixed shop can.

    Returns `(shops, achieved)`. **Read `achieved`** -- MELON and FERTILIZER are in no shop at all,
    so their only sink is the town centre and any target above 0 is unreachable by construction.
    """
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG

    cap = getattr(KG, "MAX_SHOP_INSTANCES", 8)
    contributors = []
    for name, products in KG.SHOPS.items():
        if product in products:
            contributors.append((2 if len(products) == 1 else 1, name))
    contributors.sort(reverse=True)
    shops, got = [], 0
    for weight, name in contributors:
        while got + weight <= int(target) and len(shops) < cap:
            shops.append(name)
            got += weight
    return shops, got


def shops_for_carrot_drain(target):
    return shops_for_drain("CARROT", target)[0]


def force(env, shops):
    """Pin `town["unlocked_shops"]` on the live observation. Call before every `env.step`."""
    town = env.state[0].observation["town"]
    town["unlocked_shops"] = list(shops)


def carrot_drain_per_tick(shops):
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG

    n = 0
    for name in shops:
        products = KG.SHOPS.get(name, ())
        if "CARROT" in products:
            n += 2 if len(products) == 1 else 1
    return n


def verify(targets=(0, 2, 4, 6, 8, 10), days=6):
    """Play a PASS episode with the shops pinned and MEASURE the carrot book falling."""
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG
    from kaggle_environments import make

    print(f"{'target':>7}{'shops':>34}{'per tick':>10}{'measured/tick':>15}{'ok':>5}")
    ok_all = True
    for target in targets:
        shops = shops_for_carrot_drain(target)
        env = make("kaggriculture", configuration={"seed": 700}, debug=False)
        env.reset(2)
        first = last = None
        ticks = 0
        for t in range(days * TPD):
            force(env, shops)
            book = int((env.state[0].observation["market"]["inventory"]).get("CARROT", 0))
            if t == 0:
                first = book
            last = book
            if t and t % 4 == 0:
                ticks += 1
            env.step([PASS_ACTION, PASS_ACTION])
            if env.done:
                break
        # PASS games trade nothing, so every unit of movement is the town.
        centre = (days * TPD) // KG.get(env.configuration, "townCenterSellInterval", 24) \
            if hasattr(KG, "get") else (days * TPD) // 24
        fell = first - last
        measured = (fell - centre) / max(1, ticks)
        expect = carrot_drain_per_tick(shops)
        ok = abs(measured - expect) < 0.35
        ok_all &= ok
        print(f"{target:>7}{','.join(s[:8] for s in shops)[:33]:>34}"
              f"{expect:>10}{measured:>15.2f}{'YES' if ok else 'NO':>5}")
    print(f"\nforcing works: {ok_all}")
    if not ok_all:
        print("The pinned shop list is NOT driving the drain. Do not build a sweep on this.")
    return ok_all


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--days", type=int, default=6)
    args = ap.parse_args()
    if args.verify:
        verify(days=args.days)
    else:
        for t in (0, 2, 4, 6, 8, 10, 12):
            s = shops_for_carrot_drain(t)
            print(f"target {t:>3}  ->  {carrot_drain_per_tick(s):>3}  {s}")


if __name__ == "__main__":
    main()
