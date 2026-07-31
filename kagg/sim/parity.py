"""The parity harness: drive the batched sim and the reference env with identical actions.

`CLAUDE.md` makes this the gate. **Do not train on the fast sim until parity is exact**, because a
divergent sim makes every downstream result fiction, and a divergence is silent -- nothing crashes,
the numbers are just quietly wrong.

The approach is to generate one random action script per game, run it through both implementations,
and compare the observable state after every step: each player's bank, the market inventory, and
the tile composition of both farms. Comparing every step rather than only the end matters, because
a divergence that cancels out by the final turn is still a divergence and will not cancel under a
different script.

Known deliberate approximation, stated here rather than buried: hand spawning. The reference
balances new hands across the four shed-access tiles by current occupancy (`_spawn_hand`); the sim
spawns them all on the NW tile. Scripts that hire are therefore compared on bank and market state
only, not on unit positions. Everything else is expected to match exactly.
"""

import numpy as np

from kagg.sim import ops as O
from kagg.sim.farm import MAX_UNITS
from kagg.sim.game import Actions, Game
from kagg.sim.market import PRODUCT_INDEX, PRODUCTS
from kagg.sim.tiles import CROPS, EMPTY, LOCKED, PLANT, WEED

# Ops a random script may emit. PLANT is included but gated on seeds held, as the env does.
SCRIPT_OPS = (O.NOOP, O.NORTH, O.SOUTH, O.EAST, O.WEST, O.WATER, O.HARVEST, O.PLANT_OP, O.DIG)
OP_NAMES = {
    O.NOOP: "PASS", O.NORTH: "NORTH", O.SOUTH: "SOUTH", O.EAST: "EAST", O.WEST: "WEST",
    O.WATER: "WATER", O.HARVEST: "HARVEST", O.DIG: "DIG",
}


def random_script(rng, steps, allow_hire=False, allow_land=False, max_units=1):
    """One game's worth of actions: a list of per-step dicts, both players.

    Deliberately biased toward ops that change state -- a uniform draw over 9 ops spends most of
    its time moving, and moves are the least likely thing to expose a divergence.
    """
    script = []
    for step in range(steps):
        entry = {"units": [], "sell": [], "buy_seed": [], "hire": [], "buy_land": []}
        for _ in range(2):
            # Driving more than one unit is what exposes the atomic-PLANT rule: with a single unit
            # per player, "drop the excess" and "drop them all" are the same thing, so a
            # single-unit harness cannot see the difference. It missed a real divergence for
            # exactly this reason.
            n_units = max_units
            ops, crops = [], []
            for _ in range(n_units):
                roll = rng.random()
                if roll < 0.30:
                    ops.append(O.WATER)
                elif roll < 0.45:
                    ops.append(O.PLANT_OP)
                elif roll < 0.60:
                    ops.append(O.HARVEST)
                elif roll < 0.68:
                    ops.append(O.DIG)
                else:
                    ops.append(int(rng.choice([O.NORTH, O.SOUTH, O.EAST, O.WEST, O.NOOP])))
                crops.append(int(rng.integers(len(CROPS))))
            entry["units"].append((ops, crops))
            entry["sell"].append(
                {PRODUCTS[i]: int(rng.integers(0, 4)) for i in range(len(PRODUCTS))
                 if rng.random() < 0.15}
            )
            entry["buy_seed"].append(
                {CROPS[i]: int(rng.integers(1, 3)) for i in range(len(CROPS)) if rng.random() < 0.2}
            )
            entry["hire"].append(bool(allow_hire and rng.random() < 0.05))
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
        actions = []
        for p in range(2):
            ops, crops = entry["units"][p]
            def _as_action(op, crop):
                return ["PLANT", CROPS[crop]] if op == O.PLANT_OP else [OP_NAMES[op]]

            farmer = _as_action(ops[0], crops[0])
            hands = [_as_action(o, c) for o, c in zip(ops[1:], crops[1:])]
            market = []
            for item, n in entry["sell"][p].items():
                if n:
                    market.append(["SELL", item, n])
            for crop, n in entry["buy_seed"][p].items():
                if n:
                    market.append(["BUY_SEED", crop, n])
            if entry["hire"][p]:
                market.append(["HIRE"])
            if entry["buy_land"][p]:
                market.append(["BUY_LAND"])
            actions.append({"farmer": farmer, "hands": hands, "market": market[:10]})

        env.step(actions)
        obs = env.state[0].observation
        for shop in obs.get("town", {}).get("unlocked_shops", []):
            unlocks.setdefault(shop, obs.get("day", 0))
        trace.append({
            "money": [obs["farms"][i]["money"] for i in range(2)],
            "inventory": dict(obs["market"]["inventory"]),
            "tiles": [_census(obs["farms"][i]["tiles"]) for i in range(2)],
        })
        if env.done:
            break
    return trace, {day: shop for shop, day in unlocks.items()}


def _census(tiles):
    """Tile composition as counts, which is what we compare rather than per-tile identity."""
    counts = {"empty": 0, "locked": 0, "weed": 0, "plant": 0, "units": 0}
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
    return counts


def _sim_census(tiles, game_index):
    kinds = tiles.kind[game_index]
    return {
        "empty": int((kinds == EMPTY).sum()),
        "locked": int((kinds == LOCKED).sum()),
        "weed": int((kinds == WEED).sum()),
        "plant": int((kinds == PLANT).sum()),
        "units": int(tiles.yield_units[game_index][kinds == PLANT].sum()),
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
                ops, crops = entry["units"][p]
                for u, (op, crop) in enumerate(zip(ops, crops)):
                    actions.unit_op[b, p, u] = op
                    actions.unit_crop[b, p, u] = crop
                for item, n in entry["sell"][p].items():
                    actions.sell[b, p, PRODUCT_INDEX[item]] = n
                for crop, n in entry["buy_seed"][p].items():
                    actions.buy_seed[b, p, CROPS.index(crop)] = n
                actions.hire[b, p] = entry["hire"][p]
                actions.buy_land[b, p] = entry["buy_land"][p]

        game.step(actions)
        money = game.money()
        for b in range(batch):
            traces[b].append({
                "money": [float(money[b, 0]), float(money[b, 1])],
                "inventory": {p: int(game.inventory[b, PRODUCT_INDEX[p]]) for p in PRODUCTS},
                "tiles": [_sim_census(game.tiles[i], b) for i in range(2)],
            })
    return traces


def compare(sim_trace, ref_trace, label="", fields=("money", "inventory", "tiles")):
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
        if "tiles" in fields and s["tiles"] != r["tiles"]:
            problems.append(f"{label}step {step}: tiles {s['tiles']} != {r['tiles']}")
        if problems:
            break   # the first divergence is the informative one; the rest is noise
    return problems
