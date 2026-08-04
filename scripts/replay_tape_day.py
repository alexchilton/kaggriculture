"""Can we replicate a day turn by turn from the chains alone? Feed their tape in, compare the money.

Alex's question, and this is the only thing that answers it. No plan, no genome, no decision logic:
take the winner's **recorded actions** for both seats, push them through `kagg.sim`, and after every
single turn compare our money and squares against the money and squares the replay itself recorded.

If the numbers agree turn by turn, then the action space and the simulator can express and settle that
day exactly, and the remaining work is choosing the actions -- a search problem. If they disagree, the
disagreement is in the simulator or the action encoding, and no amount of searching would ever have
reproduced the season.

Both seats are driven, because the market is shared: prices move with the other player's orders, so a
one-sided replay would not settle the same way.

The replay records each observation **after** its own action, so `steps[t].observation.money` is the
money to compare against once turn `t` has been applied.

    PYTHONPATH=. python3 -u scripts/replay_tape_day.py --day 0 2>&1 | tee data/logs/replay_tape_day0.log
"""

import argparse
import json

import numpy as np

from kagg.search import agent as A
from kagg.search import executor as X
from kagg.sim.game import (
    ORDER_BUY_ANIMAL, ORDER_BUY_LAND, ORDER_BUY_PRODUCT, ORDER_BUY_SEED, ORDER_HIRE, ORDER_SELL,
    Actions, Game,
)
from kagg.sim.market import ITEM_INDEX, PRODUCTS
from kagg.sim.tiles import COOP, PASTURE
from kagg.sim.town import SHOP_INDEX

TURNS_PER_DAY = 24
OP_CODE = {name: code for code, name in A.OP_NAMES.items()}
CROP_INDEX = {c: i for i, c in enumerate(A.CROP_NAMES)}
PRODUCT_INDEX = {p: i for i, p in enumerate(PRODUCTS)}
ANIMAL_INDEX = {a: i for i, a in enumerate(A.ANIMAL_NAMES)}


def write_unit(actions, seat, slot, entry):
    """One recorded unit action into the `Actions` slots. Returns False if the op is unknown."""
    if not entry:
        return True
    op = entry[0]
    if op not in OP_CODE:
        return False
    actions.unit_op[0, seat, slot] = OP_CODE[op]
    if op == "PLANT" and len(entry) > 1:
        actions.unit_crop[0, seat, slot] = CROP_INDEX[entry[1]]
    elif op in ("PICKUP", "PLACE") and len(entry) > 1:
        actions.unit_item[0, seat, slot] = ITEM_INDEX[entry[1]]
        actions.unit_qty[0, seat, slot] = int(entry[2]) if len(entry) > 2 else 1
    return True


ORDER_OP = {"SELL": ORDER_SELL, "BUY_SEED": ORDER_BUY_SEED, "BUY_PRODUCT": ORDER_BUY_PRODUCT,
            "BUY_ANIMAL": ORDER_BUY_ANIMAL, "HIRE": ORDER_HIRE,
            "BUY_LAND": ORDER_BUY_LAND, "BUID_LAND": ORDER_BUY_LAND}
ORDER_ITEM = {"SELL": PRODUCT_INDEX, "BUY_PRODUCT": PRODUCT_INDEX,
              "BUY_SEED": CROP_INDEX, "BUY_ANIMAL": ANIMAL_INDEX}


def write_market(actions, seat, orders):
    """Recorded market orders into the **explicit slot list**, in the order they were written.

    Not the per-product totals: `SELL WHEAT 1 / BUY_PRODUCT WHEAT 2 / SELL WHEAT 2` collapses to
    `SELL 3 / BUY 2` under totals, which reprices the buy ($58 recorded against $33 merged) and is
    exactly where the day-0 replay used to break at turn 11.
    """
    slot = 0
    for o in orders or []:
        if not isinstance(o, list) or not o or slot >= actions.order_op.shape[2]:
            continue
        op = o[0]
        if op not in ORDER_OP:
            continue
        table = ORDER_ITEM.get(op)
        if table is not None and (len(o) < 3 or o[1] not in table):
            continue
        actions.order_op[0, seat, slot] = ORDER_OP[op]
        actions.order_item[0, seat, slot] = table[o[1]] if table is not None else 0
        actions.order_qty[0, seat, slot] = int(o[2]) if table is not None else 1
        slot += 1


def unlock_schedule(steps):
    """`{day: shop_index}`, read off the replay's own `town.unlocked_shops`.

    **Not optional.** `_town_consume` drains the market for every unlocked shop every four steps, and
    the price curve is a function of that inventory, so a missing shop silently reprices everything.
    CLAUDE.md records that this schedule cannot be derived offline -- `_spawn_weeds` consumes RNG draws
    before `rng.choice` picks the shop -- and must be supplied by the caller, observed from a real
    episode when testing parity. Running without it is what made the first replay diverge from turn 97:
    the seat had SMOOTHIE_SHOP unlocked and we did not, so their STRAWBERRY and MILK inventories drained
    and ours did not.
    """
    schedule, seen = {}, set()
    for t, step in enumerate(steps):
        obs = step[0].get("observation") or {}
        for shop in (obs.get("town") or {}).get("unlocked_shops") or []:
            if shop not in seen:
                seen.add(shop)
                schedule[t // TURNS_PER_DAY] = SHOP_INDEX[shop]
    return schedule


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", default="data/episodes/89873723.json")
    ap.add_argument("--day", type=int, default=0)
    ap.add_argument("--days", type=int, default=None, help="run this many days instead of one")
    a = ap.parse_args()

    steps = json.loads(open(a.episode).read())["steps"]
    n_turns = (a.days or (a.day + 1)) * TURNS_PER_DAY
    start = 0 if a.days else 0

    schedule = unlock_schedule(steps)
    print(f"unlock schedule from the replay: {schedule}")
    game = Game(1, weed_chance=0.0, rng=np.random.default_rng(0), unlock_schedule=schedule)
    unknown = set()
    print(f"{a.episode}: driving BOTH seats from the tape, weeds off\n")
    print(f"{'turn':>5} {'d':>2} {'h':>2} | {'ours $':>10} {'theirs $':>10} {'delta':>9} | "
          f"{'crew':>4} {'pens':>4} {'crops':>5} {'animals':>7}")
    print("=" * 82)

    first_bad = None
    for t in range(start, min(n_turns, len(steps))):
        actions = Actions(1)
        for seat in range(2):
            cell = steps[t][seat]
            act = cell.get("action")
            if not isinstance(act, dict):
                continue
            units = [act.get("farmer")] + list(act.get("hands") or [])
            for slot, entry in enumerate(units[: X.MAX_EXEC_UNITS]):
                if not write_unit(actions, seat, slot, entry):
                    unknown.add(entry[0])
            write_market(actions, seat, act.get("market"))
        game.step(actions)

        obs = steps[t][0].get("observation") or {}
        farms = obs.get("farms")
        if not farms:
            continue
        theirs = float(farms[0]["money"])
        ours = float(game.farms[0].money[0])
        tiles = game.tiles[0]
        delta = ours - theirs
        if first_bad is None and abs(delta) > 0.5:
            first_bad = t
        flag = "" if abs(delta) < 0.5 else "  <<"
        if t % TURNS_PER_DAY == 0 or abs(delta) > 0.5 or t < 8:
            print(f"{t:>5} {t // TURNS_PER_DAY:>2} {t % TURNS_PER_DAY:>2} | {ours:>10,.0f} "
                  f"{theirs:>10,.0f} {delta:>+9,.0f} | {int(game.farms[0].n_units[0]):>4} "
                  f"{int(((tiles.kind[0] == PASTURE) | (tiles.kind[0] == COOP)).sum()):>4} "
                  f"{int((tiles.crop[0] >= 0).sum()):>5} "
                  f"{int((tiles.animal[0] >= 0).sum()):>7}{flag}")

    print("=" * 82)
    if unknown:
        print(f"unit ops with no code in `agent.OP_NAMES`: {sorted(unknown)}")
    print(f"first turn where money diverges: {first_bad}")


if __name__ == "__main__":
    raise SystemExit(main())
