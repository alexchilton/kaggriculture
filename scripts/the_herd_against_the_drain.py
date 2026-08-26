"""Does the herd mix follow the town's demand? Forced shop draws, mirror match.

Game 99361310 was lost by $12,165 in a town drawing YARN_STORE x1 and MILK-carrying shops x4 --
WOOL drain 2/tick against MILK drain 4/tick. We fielded SHEEP 12 / COW 6, WOOL bottomed at $1 for
136 turns, and MILK never left its base $160. The opponent fielded SHEEP 9 / COW 6.

The cause is `_herd_split` in `kagg/search/schedule_agent.py`:

    if WOOL_SHOP_SETS_THE_HERD:
        early = "YARN_STORE" in list(unlocked_shops or ())[:WOOL_SHOP_DRAW_LIMIT]
        target = WOOL_SHOP_COW_CAP if early else WOOL_SHOP_NO_YARN_COW
        if split["COW"] <= target:
            ...
            return split

That is a PRESENCE test. One yarn store in the first three draws caps cows at 6 and pours every
remaining head into sheep, whatever else the town wants. It also `return`s before the block at
`:3021-3041`, which ranks the two species by `town_drain_remaining` + `expected_future_drain` and
assigns heads greedily -- demand-aware herd logic that exists, is written, and never executes.

Three arms, all measured against the SHIPPED agent in the other seat, because the field are near
clones of the same tape:

    ship          the presence test, as it ships. The control.
    greedy        `WOOL_SHOP_SETS_THE_HERD = False` -- nothing new, just stops returning early and
                  lets `:3021` run. Reads real drain.
    proportional  sheep:cow set directly by the wool:milk drain ratio of the drawn shops.

The arm is applied to seat 0 only, by importing a SECOND copy of the module under a private name
and patching that copy. Patching the shared module would move both seats and measure nothing.

Shops are pinned with `scripts/force_the_shops.py`, revealed on the real cadence (first at d3, one
every third day) so the rule sees the list grow the way a real draw grows it.

**The control column is `herd`.** It prints the COW/SHEEP actually bought. Three arms this month
produced clean tables while changing nothing; if `herd` matches `ship`, the row is a null by
construction and the money column is noise.

    python -u scripts/the_herd_against_the_drain.py --range 700 8
"""

import argparse
import csv
import importlib.util
import json
import pathlib
import sys
from concurrent.futures import ProcessPoolExecutor

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
#: `cowN` pins the cow count to N and gives every remaining head to sheep. Sweeping N per shop
#: world answers the question the rules only approximate: what mix actually WINS in this town.
ARMS = ("ship", "greedy", "proportional",
        "cow4", "cow6", "cow8", "cow10", "cow12", "cow14")

#: (label, shops). YARN_STORE first wherever it appears, because `_early` slices the first three
#: draws and the lost game drew it first. MILK is carried by PIZZA_SHOP, ICE_CREAM_SHOP and
#: SMOOTHIE_SHOP; WOOL only by YARN_STORE, which is single-product and so drains 2 a tick.
WORLDS = (
    ("wool2_milk4", ["YARN_STORE", "PIZZA_SHOP", "PIZZA_SHOP", "ICE_CREAM_SHOP",
                     "PIZZA_SHOP", "FARMERS_MARKET", "FARMERS_MARKET", "BAKERY"]),
    ("wool6_milk0", ["YARN_STORE", "YARN_STORE", "YARN_STORE", "BAKERY",
                     "FARMERS_MARKET", "PET_CAFE", "BAKERY", "FARMERS_MARKET"]),
    ("wool2_milk0", ["YARN_STORE", "BAKERY", "FARMERS_MARKET", "BAKERY",
                     "PET_CAFE", "FARMERS_MARKET", "BRUNCH_SPOT", "BAKERY"]),
    ("wool6_milk4", ["YARN_STORE", "YARN_STORE", "YARN_STORE", "PIZZA_SHOP",
                     "PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP", "BAKERY"]),
    ("wool0_milk4", ["PIZZA_SHOP", "PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP",
                     "BAKERY", "FARMERS_MARKET", "BAKERY", "FARMERS_MARKET"]),
    ("wool4_milk2", ["YARN_STORE", "YARN_STORE", "PIZZA_SHOP", "ICE_CREAM_SHOP",
                     "BAKERY", "FARMERS_MARKET", "BAKERY", "PET_CAFE"]),
)


def drain_per_tick(shops, product):
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG

    n = 0
    for name in shops:
        products = KG.SHOPS.get(name, ())
        if product in products:
            n += 2 if len(products) == 1 else 1
    return n


def _fresh_module():
    """A private second copy of `schedule_agent`, so patching seat 0 cannot move seat 1."""
    # The name must sit INSIDE `kagg.search`. `schedule_agent.py:43` does `from . import
    # corner_the_book`, and a relative import resolves off `__package__` -- a bare top-level name
    # gives `ImportError: attempted relative import with no known parent package`.
    import kagg.search  # noqa: F401  -- the parent package must be imported first

    path = REPO / "kagg/search/schedule_agent.py"
    name = "kagg.search._arm_schedule_agent"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _proportional(mod, shops):
    """Replace `_herd_split` with one that sets the mix from the wool:milk drain ratio.

    Same floors and the same total as the shipped rule -- only the SPLIT moves, so a difference in
    the money column cannot come from buying more or fewer animals.
    """
    def split_fn(want_total, bought, day, hour, unlocked_shops, last_day=29):
        total = want_total["COW"] + want_total["SHEEP"]
        split = {a: bought.get(a, 0) for a in ("COW", "SHEEP")}
        split["COW"] = max(split["COW"], min(mod.HERD_FLOOR_COW, total))
        split["SHEEP"] = max(split["SHEEP"], min(mod.HERD_FLOOR_SHEEP, total - split["COW"]))
        seen = list(unlocked_shops or ())
        wool = drain_per_tick(seen, "WOOL")
        milk = drain_per_tick(seen, "MILK")
        if wool + milk <= 0:
            # No sink for either product yet. Leave the floors and let later turns decide.
            return split
        sheep_t = int(round(total * wool / float(wool + milk)))
        cow_t = total - sheep_t
        split["COW"] = max(split["COW"], min(cow_t, total))
        split["SHEEP"] = max(split["SHEEP"], min(sheep_t, total - split["COW"]))
        return split

    mod._herd_split = split_fn


def _fixed_cow(mod, n):
    """Pin the cow count at `n`, sheep take the rest. The schedule's TOTAL is still the ceiling."""
    def split_fn(want_total, bought, day, hour, unlocked_shops, last_day=29):
        total = want_total["COW"] + want_total["SHEEP"]
        split = {a: bought.get(a, 0) for a in ("COW", "SHEEP")}
        split["COW"] = max(split["COW"], min(n, total))
        split["SHEEP"] = max(split["SHEEP"], total - split["COW"])
        return split

    mod._herd_split = split_fn


def _visible(shops, day):
    """The real unlock cadence: first shop at d3, one more every third day."""
    if day < 3:
        return []
    return list(shops[:min(len(shops), (day - 3) // 3 + 1)])


def _play(job):
    seed, arm, world_name, shops = job
    from kaggle_environments import make

    import kagg.search.schedule_agent as SHIP

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    mine = _fresh_module()
    if arm == "greedy":
        mine.WOOL_SHOP_SETS_THE_HERD = False
    elif arm == "proportional":
        _proportional(mine, shops)
    elif arm.startswith("cow"):
        _fixed_cow(mine, int(arm[3:]))

    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
    env.reset(2)
    me = mine.make_agent(sched, 0, router=True)
    them = SHIP.make_agent(sched, 1, router=True)

    for t in range(30 * TPD):
        day = t // TPD
        env.state[0].observation["town"]["unlocked_shops"] = _visible(shops, day)
        env.state[1].observation["town"]["unlocked_shops"] = _visible(shops, day)
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = me(o0, env.configuration), them(o1, env.configuration)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o1["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"] or [])[:n0],
                   "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"] or [])[:n1],
                   "market": a1["market"]}])
        if env.done:
            break

    obs = env.state[0].observation
    ours = int(obs["farms"][0].get("money", 0))
    theirs = int(obs["farms"][1].get("money", 0))
    cow = sheep = 0
    for row in obs["farms"][0].get("tiles") or []:
        for cell in row:
            # A placed animal is identified by the `animal` key, NOT by `kind` -- `kind` carries the
            # STRUCTURE (`reference/kaggriculture.py:388,469,819`), and a tile reverts to a bare
            # structure when its animal is gone.
            if isinstance(cell, dict) and "animal" in cell:
                if cell["animal"] == "COW":
                    cow += 1
                elif cell["animal"] == "SHEEP":
                    sheep += 1
    book = obs["market"]["inventory"]
    return {"seed": seed, "arm": arm, "world": world_name, "ours": ours, "theirs": theirs,
            "win": int(ours > theirs), "cow": cow, "sheep": sheep,
            "wool_book": int(book.get("WOOL", 0)), "milk_book": int(book.get("MILK", 0))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--range", nargs=2, type=int, default=[700, 8], metavar=("FIRST", "COUNT"))
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--out", default="data/logs/herd_vs_drain.csv")
    a = ap.parse_args()

    seeds = list(range(a.range[0], a.range[0] + a.range[1]))
    jobs = [(s, arm, name, shops)
            for name, shops in WORLDS for arm in ARMS for s in seeds]
    print(f"{len(ARMS)} arms x {len(WORLDS)} worlds x {len(seeds)} seeds "
          f"= {len(jobs)} mirror games, {a.workers} workers")
    print(f"seeds {seeds}")
    print(f"rows -> {a.out}\n", flush=True)

    out = REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    cols = ["seed", "arm", "world", "ours", "theirs", "win", "cow", "sheep",
            "wool_book", "milk_book"]
    rows = []
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        fh.flush()
        with ProcessPoolExecutor(max_workers=a.workers) as pool:
            for i, r in enumerate(pool.map(_play, jobs), 1):
                w.writerow(r)
                fh.flush()
                rows.append(r)
                if i % 10 == 0:
                    print(f"  {i}/{len(jobs)}", flush=True)

    print(f"\n{'world':<14}{'wool':>6}{'milk':>6}{'arm':>14}"
          f"{'win':>8}{'herd C/S':>11}{'mean ours':>12}{'mean theirs':>13}")
    for name, shops in WORLDS:
        wl = drain_per_tick(shops, "WOOL")
        mk = drain_per_tick(shops, "MILK")
        for arm in ARMS:
            sel = [r for r in rows if r["world"] == name and r["arm"] == arm]
            if not sel:
                continue
            n = len(sel)
            print(f"{name:<14}{wl:>6}{mk:>6}{arm:>14}"
                  f"{sum(r['win'] for r in sel) / n * 100:>7.0f}%"
                  f"{sum(r['cow'] for r in sel) / n:>6.1f}/"
                  f"{sum(r['sheep'] for r in sel) / n:<4.1f}"
                  f"{sum(r['ours'] for r in sel) / n:>12,.0f}"
                  f"{sum(r['theirs'] for r in sel) / n:>13,.0f}")
        print()

    print(f"{'arm':<14}{'win':>8}{'games':>8}{'mean ours':>12}")
    for arm in ARMS:
        sel = [r for r in rows if r["arm"] == arm]
        n = max(1, len(sel))
        print(f"{arm:<14}{sum(r['win'] for r in sel) / n * 100:>7.0f}%{len(sel):>8}"
              f"{sum(r['ours'] for r in sel) / n:>12,.0f}")
    print("\nThe `herd C/S` column is the control. An arm whose herd matches `ship` changed")
    print("nothing and its money column is noise.")


if __name__ == "__main__":
    main()
