"""Nothing the row asks to sell is still riding in a hand at the bell.

Alex, 2026-08-26: *"because the schedule has sell wool 2 and we don't have any wool in the shed - we
know we need to shove 2 wool to the shed to sell"*.

The market reads the SHED and nothing else. `_drop_inventories_to_shed` sweeps every hand in at the
dawn rollover (`reference/kaggriculture.py:812`), which is after the market has closed -- so a
product that spends the day in a hand is a product sold a day late, or on the last day not at all.

Measured d12 of `clone_open`, seed 123641874, handover d12. Carried at h23, across all ten hands:

    product        in hand    row asks    we sold    base price    stranded
    MILK                 6           6          0           160        $960
    FERTILIZER           5          39         24           100        $500
    STRAWBERRY           2           4          2           120        $240
    WOOL                 1          11         11           200        $200

The clearest case is the milk: the row asks `MILK 6` at h21, we offer `MILK 6` at h23, and the shed
holds ZERO milk on every hour of the day, so that order raises nothing at all.

**Why it happens, and why the threshold is not the thing to remove.** `cover.materialise` rule 2
inserts a mid-tour shed trip only when one hand's carried, row-owed load reaches `DELIVER_MIN = 6`
(`kagg/search/cover.py:210`). Ten hands holding one or two units each never reach it. That constant
is priced against `DROP`, which is all-or-nothing (`reference/kaggriculture.py:344`) and bins the
feed ration with the produce -- at a threshold of 1 it measured `DROP 12, FEED 0, CARE 0` and eight
animals unfed on seed 11 d4. The constant is doing real work.

It is guarding the wrong tool. `PLACE <item> <n>` banks n of ONE named item in one turn and leaves
the rest of the hand alone (`reference/kaggriculture.py:394-410`), so none of the redraw cost
`DELIVER_MIN` exists to stop applies to it. `_bank` already emits exactly that shape, and
`schedule_agent` already executes `["PLACE", item, give]` with a real quantity.

The quantity is already computed, too: `owed_sale` at `schedule_agent.py:1953` is the row's sells
minus the shed -- "the row wants 2 wool, the shed has none, so 2 wool are owed". It only ever fed a
threshold test.

This asserts the BEHAVIOUR, not any particular mechanism.
"""

import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

ARM, SEED, HANDOVER, DAY = "clone_open", 123641874, 12, 12
TPD = 24

#: Base prices, `reference/kaggriculture.py:42-50`. Used only to rank the report, never to gate.
BASE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
        "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}


def _carried_at_dusk():
    """`({product: qty} still in hands at h23, row)` for `DAY`."""
    kaggle_env = pytest.importorskip("kaggle_environments")
    import kagg.plan as _PLAN
    import scripts.breakdown as B
    from kagg.search import schedule_agent as SA

    rel, sched_rel, team = B.TAPES[ARM]
    path = str(REPO / rel)
    economy, shops = B.env_config(path), B.recorded_shops(path)
    tape = B.tape_policy(path, team, 0)
    sched = {int(k): v for k, v in json.loads((REPO / sched_rel).read_text()).items()}
    ours = SA.make_agent({d: _PLAN.thin(r) for d, r in sched.items()}, 0,
                         router=True, start_day=HANDOVER)

    env = kaggle_env.make("kaggriculture", configuration=dict(economy, seed=SEED), debug=False)
    env.reset(2)
    opp = B.tape_policy(path, team, 1)
    carried = {}
    for t in range((DAY + 1) * TPD):
        for s in (0, 1):
            env.state[s].observation.town["unlocked_shops"] = list(shops(t))
        obs = env.state[0].observation
        act = tape(obs, t) if t < HANDOVER * TPD else ours(obs)
        if t == (DAY + 1) * TPD - 1:
            carried = {}
            for inv in ((obs.get("private") or {}).get("inventories") or []):
                for k, v in (inv or {}).items():
                    if int(v or 0) > 0:
                        carried[k] = carried.get(k, 0) + int(v)
        env.step([act, opp(env.state[1].observation, t)])
    return carried, sched[DAY]


def test_the_delivery_threshold_is_not_simply_removed():
    """`DELIVER_MIN` prices a real DROP cost and must stay; the fix is to use PLACE instead.

    Written down because "remove it" is the obvious move and it measured badly: at a threshold of 1,
    seed 11 d4 planned a shed trip after every stop, `DROP 12, FEED 0, CARE 0`, eight animals unfed.
    """
    import kagg.search.cover as C

    assert getattr(C, "DELIVER_MIN", 0) >= 6, (
        "DELIVER_MIN was lowered or removed. It prices DROP's redraw, which is real. Route the "
        "row's owed sells through PLACE, where that cost does not exist, and leave this alone.")


def test_no_product_the_row_sells_is_still_in_a_hand_at_the_bell():
    """The row's produce reaches the shed while the market is still open."""
    carried, row = _carried_at_dusk()
    sells = {p: int(q) for p, q in (row.get("sells") or {}).items() if int(q) > 0}
    stranded = {p: q for p, q in carried.items() if p in sells}
    worth = sum(q * BASE.get(p, 0) for p, q in stranded.items())
    assert not stranded, (
        f"d{DAY} ends with the row's own produce in hands: {stranded} "
        f"(~${worth:,} at base price). The row asks to sell {sells}. "
        "The overnight sweep banks it after the market has closed.")
