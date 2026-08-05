"""Turn a leaderboard replay's action tape into a seed script for the trajectory optimiser.

`scripts/optimise_script.py` hill-climbs a 720-turn action script and has been seeded from
`data/seed_scripts/heuristic_seed0.npz` -- our own heuristic agent's play. That is a weak starting
point: the heuristic builds no structure, buys no animal and never unlocks a quadrant, so the search
spends its early budget rediscovering things a leader already does on day 0.

A real seat's tape is a far better start, and as of 2026-08-04 it is a *trustworthy* one:
`tests/test_tape_parity.py` shows the numpy sim reproduces episode 89873723 turn for turn against the
reference interpreter, and `tests/test_jax_ordered_order_book.py` shows the JAX sim agrees with that.
So the actions written here are known to produce, in our simulator, the season they produced on Kaggle.

**What this seed is and is not.** It is the winner's *actions*, not their result. Those actions earned
$147,178 against the specific opponent and shop schedule of that episode; replayed against our
opponent pool on a different schedule they will score far less, and that is expected rather than a
bug. The value is the shape of the play -- when it hires, when it stocks, when it buys land -- which
is what the optimiser then adapts. Anything selected from here still has to clear
`scripts/validate_script.py` across fresh seeds before it goes anywhere near a submission.

**Market orders are flattened to per-product totals**, because that is the space
`kagg/search/script_mutate.py` searches. The one thing that loses is a turn interleaving orders on the
same product (`SELL WHEAT 1 / BUY_PRODUCT WHEAT 2 / SELL WHEAT 2`), worth ~$25 on the turn it appears.
Both simulators can now express it; the mutation operator cannot, so it is dropped here rather than
silently mis-slotted, and the count is reported so the loss is visible.

    PYTHONPATH=. python3 -u scripts/seed_from_replay.py --episode data/episodes/89873723.json --seat 0
"""

import argparse
import collections
import importlib.util
import json
import pathlib
import sys

import numpy as np

from kagg.search import executor as X
from kagg.sim.game import Actions

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty",
          "sell", "buy_seed", "buy_product", "buy_animal", "hire", "buy_land")
TURNS_PER_DAY = 24


def _rtd():
    spec = importlib.util.spec_from_file_location("rtd", "scripts/replay_tape_day.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["rtd"] = module
    spec.loader.exec_module(module)
    return module


def _interleaved_turns(steps):
    """How many turns repeat an `(op, item)` with something else in between -- the lossy case."""
    n = 0
    for step in steps:
        for seat in range(2):
            act = step[seat].get("action")
            if not isinstance(act, dict):
                continue
            seen, broken = {}, False
            for i, o in enumerate(act.get("market") or []):
                if not isinstance(o, list) or len(o) < 2:
                    continue
                key = (o[0], o[1])
                if key in seen and i - seen[key] > 1:
                    broken = True
                seen[key] = i
            n += int(broken)
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", default="data/episodes/89873723.json")
    ap.add_argument("--seat", type=int, default=0)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    rtd = _rtd()
    episode = pathlib.Path(a.episode)
    payload = json.loads(episode.read_text())
    steps = payload["steps"]
    rewards = payload.get("rewards") or []

    frames = {f: [] for f in FIELDS}
    crew_curve = []
    # Per-turn money for both seats, `[T, P]`, matching `extract_seed_script.py`. The optimiser prints
    # `money[-1]` as the seed's baseline, so a scalar here is an IndexError at startup.
    money_curve = []
    op_census = collections.Counter()

    # `steps[0].action` is the reset placeholder; applying it shifts every day boundary by a
    # turn and costs two thirds of the season ($43,443 against $147,178). See
    # `tests/test_tape_parity.py`.
    for t in range(1, len(steps)):
        actions = Actions(1)
        crew = [1, 1]
        for seat in range(2):
            act = steps[t][seat].get("action")
            if not isinstance(act, dict):
                continue
            units = [act.get("farmer")] + list(act.get("hands") or [])
            units = [u for u in units if u]
            crew[seat] = max(len(units), 1)
            for slot, entry in enumerate(units[: X.MAX_EXEC_UNITS]):
                rtd.write_unit(actions, seat, slot, entry)
                if seat == a.seat:
                    op_census[entry[0]] += 1
            # Per-product totals, deliberately: see the module docstring.
            _write_totals(actions, seat, act.get("market"))
        # The seat under study is written to slot 0 so the optimiser's `[:, 0]` convention holds,
        # with the opponent kept at slot 1 so the market stays contested.
        for f in FIELDS:
            arr = np.asarray(getattr(actions, f))[0]
            if a.seat == 1:
                arr = arr[::-1].copy()
            frames[f].append(arr)
        crew_curve.append(np.array(crew[::-1] if a.seat == 1 else crew))
        recorded = (steps[t][a.seat].get("observation") or {}).get("farms")
        banks = ([float(recorded[i]["money"]) for i in range(2)] if recorded
                 else (money_curve[-1] if money_curve else [0.0, 0.0]))
        money_curve.append(np.array(banks[::-1] if a.seat == 1 else banks, dtype=np.float64))

    script = {f: np.stack(frames[f]) for f in FIELDS}
    crew = np.stack(crew_curve)
    out = pathlib.Path(a.out or f"data/seed_scripts/replay_{episode.stem}_seat{a.seat}.npz")
    out.parent.mkdir(parents=True, exist_ok=True)
    money = np.stack(money_curve)
    np.savez_compressed(out, **script, money=money, crew=crew)
    final = float(rewards[a.seat]) if a.seat < len(rewards) else float(money[-1, 0])

    lossy = _interleaved_turns(steps)
    print(f"{episode} seat {a.seat}: ${final:,.0f} over {len(steps)} turns -> {out}")
    print(f"crew per turn: mean {crew[:, 0].mean():.1f}, max {crew[:, 0].max()}")
    print(f"unit ops written: {dict(op_census.most_common())}")
    print(f"market orders: {int(script['sell'].sum())} sold, "
          f"{int(script['buy_seed'].sum())} seeds, {int(script['buy_product'].sum())} products, "
          f"{int(script['buy_animal'].sum())} animals, {int(script['hire'].sum())} hires, "
          f"{int(script['buy_land'].sum())} land")
    print(f"turns whose order list interleaves one product and is therefore flattened: {lossy}")


def _write_totals(actions, seat, orders):
    """Sum a recorded order list into the per-product arrays the mutation operator searches."""
    rtd = sys.modules["rtd"]
    for o in orders or []:
        if not isinstance(o, list) or not o:
            continue
        op = o[0]
        if op == "HIRE":
            actions.hire[0, seat] += 1
        elif op in ("BUY_LAND", "BUID_LAND"):
            actions.buy_land[0, seat] += 1
        elif len(o) < 3:
            continue
        elif op == "SELL":
            actions.sell[0, seat, rtd.PRODUCT_INDEX[o[1]]] += int(o[2])
        elif op == "BUY_SEED":
            actions.buy_seed[0, seat, rtd.CROP_INDEX[o[1]]] += int(o[2])
        elif op == "BUY_PRODUCT":
            actions.buy_product[0, seat, rtd.PRODUCT_INDEX[o[1]]] += int(o[2])
        elif op == "BUY_ANIMAL":
            actions.buy_animal[0, seat, rtd.ANIMAL_INDEX[o[1]]] += int(o[2])


if __name__ == "__main__":
    raise SystemExit(main())
