"""After the opening is banked, the herd should follow the shops. Today it does not.

`schedule_agent` builds its animal target from the reference schedule's `animals_bought` rows, so
the SPECIES is decided before the board is known:

    want_total = collections.Counter()
    for dd in sorted(sched):
        if dd <= day:
            for a, qty in (sched[dd].get("animals_bought") or {}).items():
                want_total[a] += int(qty)

Nothing in that path reads `town["unlocked_shops"]`, and the shop draw is what decides whether the
product an animal makes is worth anything.

Measured by `scripts/board_demand.py` (PASS vs PASS, so the town alone drains the book and the
figure is a property of the board with no agent involved):

    seed 13   WOOL absorption 570   (YARN_STORE drawn twice)
    seed 29   WOOL absorption  30   (YARN_STORE never drawn)

Our fixed schedule produces ~160 wool either way. On seed 29 that is a surplus of 130 against a
book that reaches the $1 floor 59 units above I0, and wool duly realises $39.65-$55 a unit there
against $229.23 on a board that drew the shop.

COW and SHEEP both build a PASTURE (`routines.ANIMALS`), so the species is interchangeable at no
cost to the build schedule -- only `cost` (400 vs 500), `first_yield_day` (8 vs 6), `interval`
(2 vs 3) and `product` (MILK vs WOOL) differ.

The opening is deliberately left alone: days 0-10 keep the reference schedule's mix, because only
20-55% of the season's shop demand is visible by then (unlocks land on days 3,6,9,... weighted by
their remaining drain days) and the early animals are the ones with the longest payback. The test
therefore asserts a DIRECTION over the whole season rather than an exact count, which also keeps it
robust to the incidental purchase failures a thin bank causes on one board and not the other.
"""

import collections
import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
PLAN = REPO / "data/seed_scripts/top_guys/90976060/schedule.json"
TAPE = REPO / "data/seed_scripts/top_guys/90976060.json"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")

#: `scripts/board_demand.py`, PASS vs PASS. Units of WOOL the town removes over the whole season.
WOOL_RICH_SEED, WOOL_RICH_ABSORPTION = 13, 570
WOOL_STARVED_SEED, WOOL_STARVED_ABSORPTION = 29, 30


def _thin():
    sched = {int(k): v for k, v in json.loads(PLAN.read_text()).items()}
    return {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def _animals_bought(seed):
    """BUY_ANIMAL orders our seat actually emits over a season, by species."""
    import kagg.search.schedule_agent as SA
    from kaggle_environments import make

    from kagg.arena.tape import build_tape_agent

    ours = SA.make_agent(_thin(), 0, router=True)
    rival = build_tape_agent(str(TAPE), 0)
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)

    bought = collections.Counter()
    for _t in range(24 * 30):
        if env.done:
            break
        o0 = env.state[0].observation
        a0 = ours(o0)
        for order in (a0.get("market") or []):
            if isinstance(order, list) and len(order) >= 2 and order[0] == "BUY_ANIMAL":
                bought[order[1]] += int(order[2]) if len(order) > 2 else 1
        n0 = len(o0["farms"][0].get("hands") or [])
        a1 = rival(env.state[1].observation)
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return bought


@pytest.mark.slow
def test_more_sheep_are_bought_on_a_board_that_can_actually_absorb_wool():
    rich = _animals_bought(WOOL_RICH_SEED)
    starved = _animals_bought(WOOL_STARVED_SEED)

    # Guard the guard: if the agent buys no animals at all the comparison is vacuous.
    assert sum(rich.values()) > 0 and sum(starved.values()) > 0, (
        f"no animals bought at all -- rich {dict(rich)}, starved {dict(starved)}; the fixture "
        f"cannot see the behaviour it exists to test"
    )

    assert rich["SHEEP"] >= starved["SHEEP"] + 2, (
        f"the herd does not follow the shop draw.\n"
        f"  seed {WOOL_RICH_SEED} (WOOL absorption {WOOL_RICH_ABSORPTION}): {dict(rich)}\n"
        f"  seed {WOOL_STARVED_SEED} (WOOL absorption {WOOL_STARVED_ABSORPTION}): {dict(starved)}\n"
        f"A board that removes {WOOL_STARVED_ABSORPTION} units of wool all season cannot pay for "
        f"the ~160 the schedule produces; the surplus sits above I0 where wool floors 59 units up. "
        f"COW and SHEEP share the PASTURE structure, so the species is free to swap."
    )
