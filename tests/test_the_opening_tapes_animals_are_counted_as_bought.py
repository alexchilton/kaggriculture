"""An animal the opening tape buys must count against the herd target, or it is bought twice.

Ladder game 99071595 and validation game 99067358, both played by submission 55764542 on
2026-08-25, finished with **14 animals placed and 4 standing in the shed** -- 2 COW and 2 SHEEP,
$1,800 of stock, bought on d12 and never placed, because all 14 pens the schedule builds were
already full. The last animal PLACE in either game is d11.

The schedule buys 14 animals and builds 14 pens, and buys nothing after d11, so the d12 order is not
its. Reading the agent's own counter through a season (`scripts/where_do_the_four_animals_come_from.py`,
seed 0) shows where it comes from:

     day |      want_total (season) |          state[bought] | orders that day
       0 |                          |                        | {'COW': 2, 'SHEEP': 2}
       3 |  {'COW': 10, 'SHEEP': 4} |                     {} | {'COW': 1}
      11 |  {'COW': 10, 'SHEEP': 4} | {'COW': 6, 'SHEEP': 2} | {'COW': 2}
      12 |  {'COW': 10, 'SHEEP': 4} | {'COW': 8, 'SHEEP': 2} | {'COW': 2, 'SHEEP': 2}

By d12 the season has really ordered COW 10 and SHEEP 4 -- the whole schedule. The counter reads
COW 8 and SHEEP 2. It is short by exactly the d0 row, and the buy loop asks for
`want_total[a] - state["bought"][a]`, so it buys that row a second time.

`REPLAY_OPENING_DAYS = (0, 1, 2, 4, ..., 11)`, so d0 is replayed. The replayed branch does credit
the tape's `BUY_ANIMAL` -- but only inside `if split and ...`, where `split = state["herd_split"]`,
which is written by the `SHOP_ADAPT_HERD and day >= SHOP_ADAPT_FROM_DAY` block and therefore does
not exist until d3. On d0 the order is appended verbatim and never counted.

The re-labelling genuinely needs the split. The COUNTING does not.

This is not the q4 board and not a land shortage: the q4 latch reads False all season, and the farm
holds 75 unlocked tiles against 14 pens.
"""

import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
THROUGH_DAY = 13          # d12 is where the duplicate lands; d13 gives it a turn to be placed.


def _play_to(day_stop, seed=0):
    """Mirror season to the end of `day_stop`. Returns (placed, shed, orders_by_day) for seat 0."""
    import breakdown as B
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    a0, a1 = SA.make_agent(sched, 0), SA.make_agent(sched, 1)
    orders = collections.Counter()
    for t in range((day_stop + 1) * TPD):
        o0, o1 = env.state[0].observation, env.state[1].observation
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o1["farms"][1].get("hands") or [])
        x, y = a0(o0), a1(o1)
        for od in (x["market"] or []):
            if od and od[0] == "BUY_ANIMAL":
                orders[(t // TPD, od[1])] += int(od[2]) if len(od) > 2 else 1
        env.step([{"farmer": x["farmer"], "hands": list(x["hands"] or [])[:n0],
                   "market": x["market"]},
                  {"farmer": y["farmer"], "hands": list(y["hands"] or [])[:n1],
                   "market": y["market"]}])
        if env.done:
            break

    o = env.state[0].observation
    placed = collections.Counter()
    for row in o["farms"][0]["tiles"]:
        for tile in row:
            if isinstance(tile, dict) and tile.get("animal"):
                placed[tile["animal"]] += 1
    shed = (o.get("private") or {}).get("shed") or {}
    return placed, {a: int(shed.get(a, 0) or 0) for a in ("COW", "SHEEP")}, orders


def test_the_opening_row_is_not_bought_a_second_time():
    """The season's animal rows total 14. No more than 14 may ever be ordered."""
    placed, shed, orders = _play_to(THROUGH_DAY)
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    want = sum(int(q) for r in raw.values()
               for a, q in (r.get("animals_bought") or {}).items() if a in ("COW", "SHEEP"))

    ordered = sum(orders.values())
    by_day = {d: {a: n for (dd, a), n in orders.items() if dd == d}
              for d in sorted({d for d, _ in orders})}
    assert ordered <= want, (
        f"the schedule's rows buy {want} animals; the agent ordered {ordered} by "
        f"d{THROUGH_DAY}. Per day: {by_day}")


def test_no_animal_is_left_standing_in_the_shed():
    """An animal in the shed is $400-$500 of stock producing nothing. There is no pen for it."""
    placed, shed, orders = _play_to(THROUGH_DAY)
    stranded = shed["COW"] + shed["SHEEP"]
    assert stranded == 0, (
        f"{stranded} animals stranded in the shed at the end of d{THROUGH_DAY} "
        f"({shed}), against {sum(placed.values())} placed ({dict(placed)}) -- "
        f"${shed['COW'] * 400 + shed['SHEEP'] * 500} of stock with nowhere to stand")
