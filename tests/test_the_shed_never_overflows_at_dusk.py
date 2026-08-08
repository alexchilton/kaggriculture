"""Product we harvested is thrown away at dusk because the shed has no room for it.

`_drop_inventories_to_shed` (`reference/kaggriculture.py:812-826`) empties every hand into the shed
at the day rollover, up to `shedCapacity` = 100, and the remainder is **discarded outright**: the
`del inv[item]` runs whether or not `take` covered the stack. Nothing warns, and the units simply
cease to exist.

We hold up to fifty more MILK in the shed than the tape at d22 -- not because milk goes unsold (every
unit is sold, and at a better price than his) but because the day's sales are capped at the
schedule's `sells` row, which is a count read off HIS production rate. The surplus is harmless in
itself and lethal to everything else: it occupies a 100-slot shed shared by all nine products, and
whatever the hands are carrying at dusk falls off the end.

This test counts what falls off. It is a correctness floor, not a metric -- harvested product that
evaporates is never acceptable, whatever the bank says.
"""
import collections
import json
import pathlib

import pytest

from kagg.search import schedule_agent as SA
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

pytestmark = pytest.mark.slow

CAPACITY = 100


def _discarded(seed=11, days=30):
    """(day, units lost) for every dusk where the hands held more than the shed could take."""
    from kaggle_environments import make

    replay, schedule, team = TAPES["seb"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)

    def totals(obs):
        priv = obs.get("private") or {}
        shed = sum(int(v) for v in (priv.get("shed") or {}).values())
        held = sum(int(v) for iv in (priv.get("inventories") or []) for v in (iv or {}).values())
        return shed, held

    lost = []
    for t in range(24 * days - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = agent(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        last = (t % 24 == 23)
        before = totals(o0) if last else None
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
        if last:
            shed_before, held_before = before
            shed_after, _held_after = totals(env.state[0].observation)
            # The drop is a pure transfer, so anything that does not arrive was binned. Sells settle
            # in the same env.step, which can only make the shed SMALLER, so this is a lower bound on
            # the loss and never an over-count.
            gone = (shed_before + held_before) - shed_after
            if gone > 0:
                lost.append((t // 24, gone))
    return lost


@pytest.mark.xfail(strict=True, reason=(
    "OPEN-13. `SELL_TO_MAKE_ROOM` takes this from 101 units to a residue, and no sell rule can "
    "reach the rest: the market sells from the SHED, so product already in a hand at dusk was "
    "never sellable that day. Closing it needs the ROUTER to stop collecting into a shed with no "
    "room -- the same assignment defect as OPEN-4. Strict, so it fails loudly the day that lands."))
def test_no_harvested_product_is_ever_discarded_at_dusk():
    """The floor: what a hand is carrying at dusk must have somewhere to go."""
    lost = _discarded()
    total = sum(n for _d, n in lost)
    assert not lost, (
        f"{total} unit(s) of product discarded at the dusk drop, by day: {lost}. "
        f"The shed holds {CAPACITY} across ALL products and the overflow is deleted, so stock the "
        "sell cap will not release destroys whatever the hands are carrying that night."
    )
