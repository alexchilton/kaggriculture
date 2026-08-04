"""The parity harness: drive the batched sim and the reference env with identical actions.

`CLAUDE.md` makes this the gate. **Do not train on the fast sim until parity is exact**, because a
divergent sim makes every downstream result fiction, and a divergence is silent -- nothing crashes,
the numbers are just quietly wrong.

The approach is to generate one random action script per game, run it through both implementations,
and compare the observable state after every step: each player's bank, the market inventory, and
the tile composition of both farms. Comparing every step rather than only the end matters, because
a divergence that cancels out by the final turn is still a divergence and will not cancel under a
different script.

Two things this harness got wrong before, both worth stating rather than burying:

- It hard-coded one unit per player, so "60/60 exact" was a claim about single-unit games that was
  read as a claim about the simulator. Two real divergences hid behind it.
- Having been widened, it then drove six unit actions per player whether or not the farm owned six
  units. The reference ignores a surplus action for movement and work but still counts it in the
  atomic PLANT rule, so it blocked plants that no agent could ever have blocked, and the simulator
  was recorded as broken under hiring when the harness was the thing that was broken. It now
  submits one action per unit owned, which is what every agent does.

The only remaining deliberate divergence is the weed spawn sequence (see `Game._spawn_weeds`),
neutralised here by running both sides at `weedSpawnChance` 0.

Because unit actions are truncated to units owned, `hire_rate` is what decides whether this gate
sees a crew at all: at the old 0.05 only about 15% of player-turns had a second unit. Drive it high
when the point is to test multi-unit play.
"""

import numpy as np

from kagg.sim import ops as O
from kagg.sim.farm import MAX_UNITS
from kagg.sim.game import Actions, Game
from kagg.sim.market import ANIMALS, ITEM_INDEX, ITEMS, PRODUCT_INDEX, PRODUCTS
from kagg.sim.tiles import COOP, CROPS, EMPTY, LOCKED, NO_ANIMAL, PASTURE, PLANT, WEED

# Every op the environment accepts. This list previously held only the ops the simulator already
# implemented, which is exactly why 300 exact episodes said nothing about `FEED`: a harness that
# cannot emit an op cannot fail on it. If an op exists in `_apply_unit_action`, it belongs here.
SCRIPT_OPS = (
    O.NOOP, O.NORTH, O.SOUTH, O.EAST, O.WEST, O.WATER, O.HARVEST, O.PLANT_OP, O.DIG,
    O.PICKUP, O.DROP, O.PLACE, O.FEED, O.CARE, O.COLLECT_FERT, O.FERTILIZE,
    O.BUILD_COOP, O.BUILD_PASTURE,
)
OP_NAMES = {
    O.NOOP: "PASS", O.NORTH: "NORTH", O.SOUTH: "SOUTH", O.EAST: "EAST", O.WEST: "WEST",
    O.WATER: "WATER", O.HARVEST: "HARVEST", O.DIG: "DIG", O.DROP: "DROP", O.FEED: "FEED",
    O.CARE: "CARE", O.COLLECT_FERT: "COLLECT_FERTILIZER", O.FERTILIZE: "FERTILIZE",
    O.BUILD_COOP: "BUILD_COOP", O.BUILD_PASTURE: "BUILD_PASTURE",
}
# Ops carrying an item and a count.
ITEM_OPS = {O.PICKUP: "PICKUP", O.PLACE: "PLACE"}


def random_script(rng, steps, allow_hire=False, allow_land=False, max_units=1, hire_rate=0.05):
    """One game's worth of actions: a list of per-step dicts, both players.

    Deliberately biased toward ops that change state -- a uniform draw over 9 ops spends most of
    its time moving, and moves are the least likely thing to expose a divergence.

    `max_units` is an upper bound, not a promise: actions for units the farm has not hired are
    dropped when the script is played, so `hire_rate` is what actually decides how many units act.
    Hands are dismissed every night and the fee is Fibonacci within a day, so even `hire_rate=0.5`
    averages only about 1.6 units per player-turn -- it reaches six on 4.6% of them, against 0% at
    the 0.05 default.
    """
    script = []
    for step in range(steps):
        entry = {"units": [], "sell": [], "buy_seed": [], "hire": [], "buy_land": [],
                 "buy_product": [], "buy_animal": []}
        for _ in range(2):
            # Driving more than one unit is what exposes the atomic-PLANT rule: with a single unit
            # per player, "drop the excess" and "drop them all" are the same thing, so a
            # single-unit harness cannot see the difference. It missed a real divergence for
            # exactly this reason.
            n_units = max_units
            ops, crops, items, qtys = [], [], [], []
            for _ in range(n_units):
                roll = rng.random()
                if roll < 0.20:
                    ops.append(O.WATER)
                elif roll < 0.30:
                    ops.append(O.PLANT_OP)
                elif roll < 0.42:
                    ops.append(O.HARVEST)
                elif roll < 0.47:
                    ops.append(O.DIG)
                elif roll < 0.53:
                    ops.append(O.BUILD_PASTURE)
                elif roll < 0.56:
                    ops.append(O.BUILD_COOP)
                elif roll < 0.62:
                    ops.append(O.PLACE)
                elif roll < 0.68:
                    ops.append(O.PICKUP)
                elif roll < 0.72:
                    ops.append(O.DROP)
                elif roll < 0.79:
                    ops.append(O.FEED)
                elif roll < 0.83:
                    ops.append(O.CARE)
                elif roll < 0.87:
                    ops.append(O.COLLECT_FERT)
                elif roll < 0.90:
                    ops.append(O.FERTILIZE)
                else:
                    ops.append(int(rng.choice([O.NORTH, O.SOUTH, O.EAST, O.WEST, O.NOOP])))
                crops.append(int(rng.integers(len(CROPS))))
                # Bias PICKUP/PLACE toward wheat, fertilizer and animals -- the items that actually
                # move in a real game -- while still reaching the rest.
                if rng.random() < 0.6:
                    items.append(ITEM_INDEX[str(rng.choice(["WHEAT", "FERTILIZER"] + ANIMALS))])
                else:
                    items.append(int(rng.integers(len(ITEMS))))
                qtys.append(int(rng.integers(1, 4)))
            entry["units"].append((ops, crops, items, qtys))
            entry["sell"].append(
                {PRODUCTS[i]: int(rng.integers(0, 4)) for i in range(len(PRODUCTS))
                 if rng.random() < 0.15}
            )
            entry["buy_seed"].append(
                {CROPS[i]: int(rng.integers(1, 3)) for i in range(len(CROPS)) if rng.random() < 0.2}
            )
            entry["buy_product"].append(
                {p: int(rng.integers(1, 4)) for p in ("WHEAT", "FERTILIZER") if rng.random() < 0.12}
            )
            entry["buy_animal"].append(
                {a: 1 for a in ANIMALS if rng.random() < 0.03}
            )
            entry["hire"].append(bool(allow_hire and rng.random() < hire_rate))
            entry["buy_land"].append(bool(allow_land and rng.random() < 0.01))
        script.append(entry)
    return script


def run_reference(script, seed):
    """Play a script through the real environment, recording state after every step."""
    from kaggle_environments import make

    # Weeds are disabled on BOTH sides so the comparison is exact. Their spawn RNG is a per-day
    # Python generator consuming one draw per empty tile, which cannot be ported without losing the
    # speedup the simulator exists for; the sim matches it statistically instead, tested separately.
    env = make(
        "kaggriculture",
        configuration={"seed": seed, "weedSpawnChance": 0.0},
        debug=False,
    )
    env.reset(num_agents=2)

    trace, unlocks = [], {}
    for entry in script:
        farms = env.state[0].observation["farms"]
        actions = []
        for p in range(2):
            ops, crops, items, qtys = entry["units"][p]
            def _as_action(op, crop, item=0, qty=1):
                if op == O.PLANT_OP:
                    return ["PLANT", CROPS[crop]]
                if op in ITEM_OPS:
                    return [ITEM_OPS[op], ITEMS[item], qty]
                return [OP_NAMES[op]]

            # One action per unit actually owned, which is what every agent submits:
            # they all build the list from `[farmer, *farm["hands"]]`. Surplus hand actions are
            # not merely ignored by the reference -- `interpreter` computes the atomic PLANT
            # block over the *submitted* actions, so a request from a hand that does not exist
            # still cancels the farmer's plant. Feeding the reference six unit actions while the
            # farm owned one is what made this harness report a divergence that no game can
            # reach, and it is why the sim was believed to be broken under hiring.
            n_hands = len(farms[p].get("hands", []))
            farmer = _as_action(ops[0], crops[0], items[0], qtys[0])
            hands = [
                _as_action(o, c, i, q)
                for o, c, i, q in zip(ops[1:], crops[1:], items[1:], qtys[1:])
            ][:n_hands]
            market = []
            for item, n in entry["sell"][p].items():
                if n:
                    market.append(["SELL", item, n])
            for crop, n in entry["buy_seed"][p].items():
                if n:
                    market.append(["BUY_SEED", crop, n])
            for item, n in entry["buy_product"][p].items():
                if n:
                    market.append(["BUY_PRODUCT", item, n])
            for animal, n in entry["buy_animal"][p].items():
                if n:
                    market.append(["BUY_ANIMAL", animal, n])
            if entry["hire"][p]:
                market.append(["HIRE"])
            if entry["buy_land"][p]:
                market.append(["BUY_LAND"])
            actions.append({"farmer": farmer, "hands": hands, "market": market[:10]})

        env.step(actions)
        obs = env.state[0].observation
        for shop in obs.get("town", {}).get("unlocked_shops", []):
            unlocks.setdefault(shop, obs.get("day", 0))
        # **`shed` and `carried` are compared as of 2026-08-04.** Money, market inventory and a tile
        # census were the only fields, and none of them move when an item shifts between a unit's hands
        # and the shed -- so a one-turn error in the dawn drop was invisible over 719 exact steps.
        # Found by replaying a real tape: our drop fired at the end of hour 23 while the reference
        # drops during hour 0, and a `SELL FERTILIZER` on that boundary settled for $99 in our sim and
        # $0 in theirs. `tiles` is still a census, so per-tile identity remains uncompared.
        privates = [st.observation.private for st in env.state]
        trace.append({
            "money": [obs["farms"][i]["money"] for i in range(2)],
            "inventory": dict(obs["market"]["inventory"]),
            "tiles": [_census(obs["farms"][i]["tiles"]) for i in range(2)],
            "shed": [{k: int(v) for k, v in (privates[i].get("shed") or {}).items() if v}
                     for i in range(2)],
            "carried": [[{k: int(v) for k, v in (inv or {}).items() if v}
                         for inv in (privates[i].get("inventories") or [])]
                        for i in range(2)],
        })
        if env.done:
            break
    return trace, {day: shop for shop, day in unlocks.items()}


def _census(tiles):
    """Tile composition as counts, which is what we compare rather than per-tile identity.

    Structures and animals are counted separately from plants: an empty pasture and a stocked one
    are the same `kind` in the reference and differ only by the `animal` key, and that difference
    is the whole animal economy.
    """
    counts = {"empty": 0, "locked": 0, "weed": 0, "plant": 0, "units": 0,
              "coop": 0, "pasture": 0, "animals": 0, "animal_units": 0, "fed": 0, "cared": 0}
    for row in tiles:
        for cell in row:
            if cell == "LOCKED":
                counts["locked"] += 1
            elif cell is None:
                counts["empty"] += 1
            elif isinstance(cell, dict):
                kind = cell.get("kind")
                if kind == "WEED":
                    counts["weed"] += 1
                elif kind == "PLANT":
                    counts["plant"] += 1
                    counts["units"] += cell.get("yield_units", 0)
                elif kind in ("COOP", "PASTURE"):
                    counts[kind.lower()] += 1
                    if "animal" in cell:
                        counts["animals"] += 1
                        counts["animal_units"] += cell.get("yield_units", 0)
                        counts["fed"] += bool(cell.get("fed_today"))
                        counts["cared"] += bool(cell.get("cared_today"))
    return counts


def _sim_census(tiles, game_index):
    kinds = tiles.kind[game_index]
    animal = tiles.animal[game_index]
    stocked = animal != NO_ANIMAL
    return {
        "empty": int((kinds == EMPTY).sum()),
        "locked": int((kinds == LOCKED).sum()),
        "weed": int((kinds == WEED).sum()),
        "plant": int((kinds == PLANT).sum()),
        "units": int(tiles.yield_units[game_index][kinds == PLANT].sum()),
        "coop": int((kinds == COOP).sum()),
        "pasture": int((kinds == PASTURE).sum()),
        "animals": int(stocked.sum()),
        "animal_units": int(tiles.yield_units[game_index][stocked].sum()),
        "fed": int(tiles.fed_today[game_index][stocked].sum()),
        "cared": int(tiles.cared_today[game_index][stocked].sum()),
    }


def run_sim(scripts, seed=None, weed_chance=0.0, unlocks=None):
    """Play a list of scripts (one per game) through the batched sim, recording the same state."""
    from kagg.sim.town import SHOP_INDEX

    batch = len(scripts)
    schedule = {d: SHOP_INDEX[s] for d, s in (unlocks or {}).items()}
    game = Game(batch, weed_chance=weed_chance, unlock_schedule=schedule)
    traces = [[] for _ in range(batch)]

    for step in range(len(scripts[0])):
        actions = Actions(batch)
        for b, script in enumerate(scripts):
            entry = script[step]
            for p in range(2):
                ops, crops, items, qtys = entry["units"][p]
                for u, (op, crop, it, q) in enumerate(zip(ops, crops, items, qtys)):
                    actions.unit_op[b, p, u] = op
                    actions.unit_crop[b, p, u] = crop
                    actions.unit_item[b, p, u] = it
                    actions.unit_qty[b, p, u] = q
                for item, n in entry["sell"][p].items():
                    actions.sell[b, p, PRODUCT_INDEX[item]] = n
                for crop, n in entry["buy_seed"][p].items():
                    actions.buy_seed[b, p, CROPS.index(crop)] = n
                for item, n in entry["buy_product"][p].items():
                    actions.buy_product[b, p, PRODUCT_INDEX[item]] = n
                for animal, n in entry["buy_animal"][p].items():
                    actions.buy_animal[b, p, ANIMALS.index(animal)] = n
                actions.hire[b, p] = entry["hire"][p]
                actions.buy_land[b, p] = entry["buy_land"][p]

        game.step(actions)
        money = game.money()
        for b in range(batch):
            traces[b].append({
                "money": [float(money[b, 0]), float(money[b, 1])],
                "inventory": {p: int(game.inventory[b, PRODUCT_INDEX[p]]) for p in PRODUCTS},
                "tiles": [_sim_census(game.tiles[i], b) for i in range(2)],
                "shed": [_shed_dict(game.farms[i], b) for i in range(2)],
                "carried": [_carried_list(game.farms[i], b) for i in range(2)],
            })
    return traces


def _shed_dict(farm, b):
    """The farm's shed as a sparse name->count dict, matching the reference's `private["shed"]`."""
    from .market import ITEMS
    return {ITEMS[i]: int(v) for i, v in enumerate(farm.shed[b]) if v}


def _carried_list(farm, b):
    """Per-unit carried inventories, one sparse dict each, trimmed to the units that exist."""
    from .market import ITEMS
    n = int(farm.n_units[b])
    return [{ITEMS[i]: int(v) for i, v in enumerate(farm.carried[b, u]) if v} for u in range(n)]


def compare(sim_trace, ref_trace, label="",
            fields=("money", "inventory", "tiles", "shed", "carried")):
    """Return a list of human-readable divergences, empty if parity holds."""
    problems = []
    for step, (s, r) in enumerate(zip(sim_trace, ref_trace)):
        if "money" in fields and s["money"] != r["money"]:
            problems.append(f"{label}step {step}: money {s['money']} != {r['money']}")
        if "inventory" in fields:
            for product in PRODUCTS:
                if s["inventory"][product] != r["inventory"][product]:
                    problems.append(
                        f"{label}step {step}: {product} inventory "
                        f"{s['inventory'][product]} != {r['inventory'][product]}"
                    )
        if "shed" in fields and s.get("shed") != r.get("shed"):
            problems.append(f"{label}step {step}: shed {s.get('shed')} != {r.get('shed')}")
        if "carried" in fields and s.get("carried") != r.get("carried"):
            problems.append(
                f"{label}step {step}: carried {s.get('carried')} != {r.get('carried')}")
        if "tiles" in fields and s["tiles"] != r["tiles"]:
            problems.append(f"{label}step {step}: tiles {s['tiles']} != {r['tiles']}")
        if problems:
            break   # the first divergence is the informative one; the rest is noise
    return problems
