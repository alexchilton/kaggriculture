"""A wheat row refused a market slot at dawn is re-offered as a BLOCK, not left to the drip.

`BUY_THE_ROW_AT_DAWN` sizes the h00 wheat order at the whole remaining row, because at dawn the
bank is at its day maximum and the crew's depot draws start at h01-h05. But the append is gated on
`len(orders) < 9`, and on Victor's d7 the h00 queue already holds ten orders -- SELL WOOL, SELL
FERTILIZER, seven HIREs and the COW -- so the block is dropped on the floor. `state["ordered"]` is
honest here (nothing is credited), and from h01 the boost is gone (`hour == 0`), so the row falls
back to `BUY_DRIP = 1` per turn:

    h00  short=14  money=2512  norders=10   <- refused, no slot
    h01  short=1   ordered            1
    h02  u1 draws 3 of its 4, shed 0; u4's want {WHEAT: 3} is DELETED at the depot
    ...  one wheat per hour until h15

u4 walks to its first pen with no wheat, the pen still offers COLLECT so `FETCH_THE_FEED_AND_RETURN`
never fires there, and the FEED is dropped silently. The recovery trip at h05 draws for the two
FEED stops still in the route, not three. That one deleted draw is d7 `feed 9/10`, `care 9/10`
(CARE rides on a fed pen) and `collect_fert 6/7` (the recovery round trip eats the tour's tail).

The tape's own cadence is the fix: Victor's h01 queue is also exactly ten, and he ships
`BUY_PRODUCT WHEAT 6` as a block at h02 -- the first turn with a free slot. The dawn block must
survive a full queue and go out whole on the first turn that can take it.

The assertion is on the ORDERS we queue, deliberately -- the drop happens on the offer side, one
line before any fill exists. h00 + h01 together must carry the whole row: h00 for the days the
queue can take it (d0, d5 do this today), h01 for a day like d7 where it cannot.
"""
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))

SEED = 11
DAY = 7
TPD = 24


@pytest.fixture(scope="module")
def wheat_ordered_by_hour():
    """{hour: units of BUY_PRODUCT WHEAT our seat queued that hour} for day 7."""
    import breakdown as B
    from kaggle_environments import make

    import kagg.search.schedule_agent as sa

    replay, schedule, team = B.TAPES["victor"]
    sched = {int(k): v for k, v in json.loads((REPO / schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}

    cfg = dict(B.env_config(REPO / replay), seed=SEED, weedSpawnChance=0.0)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    agent = sa.make_agent(thin, 0, router=True)
    tape = B.tape_policy(REPO / replay, team, 1)

    per_hour = {}
    for t in range(TPD * (DAY + 1)):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = agent(o0), tape(o1, t)
        if t // TPD == DAY:
            per_hour[t % TPD] = sum(int(o[2]) for o in (a0["market"] or [])
                                    if o and o[0] == "BUY_PRODUCT" and o[1] == "WHEAT")
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                   "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                   "market": a1["market"]}])
    return per_hour


def test_the_dawn_row_survives_a_full_queue(wheat_ordered_by_hour):
    row = 14  # d7 `buys: {WHEAT: 14}`, and the dawn bank ($2,512 with pending) covers it
    early = wheat_ordered_by_hour.get(0, 0) + wheat_ordered_by_hour.get(1, 0)
    assert early >= row, (
        f"d7 queued only {early} of the {row}-wheat row by the end of h01 "
        f"(per hour: { {h: q for h, q in sorted(wheat_ordered_by_hour.items()) if q} }) -- "
        f"the dawn block was dropped for a full order queue and left to the 1/turn drip, "
        f"which is what deletes u4's depot want at h02 and costs the tenth FEED"
    )
