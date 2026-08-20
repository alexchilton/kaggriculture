"""The day's ration must be in the shed by the hour the dawn tour reaches the shed.

**The theory, stated before the fix.** The dawn plan credits the row's whole `buys` into
`plan_supply` at hour 0 (`schedule_agent.py:1886-1892`) and routes
`(4,4)[PICKUP] -> pen[FEED, CARE, COLLECT_FERTILIZER]`. The unit arrives at the shed at hour 1.
If the wheat has not landed by then the PICKUP loads nothing, the unit walks to the pen empty, and
`FEED` -- which takes a WHEAT from the ACTING unit's carried inventory
(`reference/kaggriculture.py:505`, `inv = _farmer_inventory` at `:321`) -- is not live and is
dropped silently. `CARE` goes with it. `COLLECT_FERTILIZER` is the only op left at the stop, so the
turn goes to fertilizer and the animal starves.

Measured on tetsuya's board `94345389`, seat 0, seed 959074148
(`data/logs/carry_2026-08-20.log`, `data/logs/loop_2026-08-20.log`):

    d3 h1  unit 1 at (4,4) shed  carrying={}   act=WEST               shed.WHEAT=0
    d3 h2  unit 1 at (3,4) pen   carrying={}   act=COLLECT_FERTILIZER shed.WHEAT=5

The router offers a FEED on every pen on every day and the plan commits to every one of them
(`ROUTER yes / PLAN yes` for all of d1-d6). Four are never carried out -- one on d3, three on d4 --
and pen (4,3) misses both, hits `consecutive_unfed >= 2` and escapes at d4 night
(`reference/kaggriculture.py:817`). So `at_risk`, `will_be_fed`, the arrival budget and the greedy
ordering are all upstream of the break and are NOT the cause.

**Why the ration is late.** The dawn block at `schedule_agent.py:5384` is appended only while
`len(orders) < 9`. On d3 and d4 the hour-0 queue is already full of hires and animals, so the
ration is refused a slot and falls through to the drip. tetsuya does not have this problem: he
places ONE WHEAT block per day at hour 1, sized to that day's `feeds`, and it fills whole --
`+5 +5 +5 +5 +6 +8 +8` on d0-d6 (`data/logs/cadence_2026-08-20.log`).

**What this file asserts.** Not "d3 feeds five animals" -- that is the symptom, and
`SUPER_IMPORTANT_READ_THIS_FIRST.md` §4 records two feed fixes that passed a symptom test and lost
the season. It asserts the mechanism: when a day's row asks for wheat, the wheat is drawable by the
hour the tour reaches the shed.

RED as written on 2026-08-20 for d3 and d4; d1 and d2 already pass and are the control.
"""
import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
TAPE = REPO / "data/seed_scripts/downloads_2026-08-19/94345389.json"
PLAN = REPO / "data/seed_scripts/tetsuya/schedule.json"
SEED = 959074148

#: The hour the dawn tour reaches the shed. The plan is built at h0, the units move at h1.
PICKUP_HOUR = 1


@pytest.fixture(scope="module")
def shed_by_hour():
    """`{(day, hour): shed_WHEAT}` as the UNIT sees it -- before that turn's market phase.

    The unit phase runs before `_process_market` (`kaggriculture.py:922` then `:928`), so an order
    placed at hour h is not drawable until hour h+1. Reading the observation at the top of the turn
    is exactly what the acting unit can draw on.
    """
    pytest.importorskip("kaggle_environments")
    from kaggle_environments import make
    from kagg.search import schedule_agent as A
    from kagg import plan as P

    d = json.loads(TAPE.read_text())
    seat = next(i for i, n in enumerate(d["info"]["TeamNames"]) if "tetsuya" in str(n).lower())
    other = 1 - seat
    opp = [((f[other] or {}).get("action") or {}) for f in d["steps"][1:]]
    cfg = dict(d.get("configuration") or {})
    cfg.pop("steps", None)
    cfg["seed"] = SEED

    env = make("kaggriculture", configuration=cfg, debug=False)
    env.reset(2)
    me = A.make_agent(P.load(str(PLAN)), me=seat)

    out = {}
    for t in range(719):
        if env.done:
            break
        ob = env.state[seat].observation
        day, hour = int(ob.get("day", 0) or 0), int(ob.get("hour", 0) or 0)
        if day > 6:
            break
        out[(day, hour)] = int(((ob.get("private") or {}).get("shed") or {}).get("WHEAT", 0) or 0)
        n = [len((env.state[0].observation["farms"][i] or {}).get("hands") or []) for i in (0, 1)]
        m = me(ob, t)
        st = opp[t] if t < len(opp) else {}
        act = [None, None]
        act[seat] = {"farmer": m["farmer"], "hands": list(m["hands"])[:n[seat]],
                     "market": m["market"]}
        act[other] = {"farmer": st.get("farmer") or ["PASS"],
                      "hands": list(st.get("hands") or [])[:n[other]],
                      "market": st.get("market") or []}
        env.step(act)
    return out


def _row(day):
    return json.loads(PLAN.read_text())[str(day)]


@pytest.mark.parametrize("day", [1, 2, 3, 4])
def test_a_day_that_buys_wheat_has_it_before_the_tour_reaches_the_shed(day, shed_by_hour):
    """d1 and d2 are the control: they already order at hour 0 and already pass."""
    row = _row(day)
    wanted = int((row.get("buys") or {}).get("WHEAT", 0) or 0)
    if not wanted:
        pytest.skip("day %d does not buy wheat" % day)
    have = shed_by_hour.get((day, PICKUP_HOUR))
    assert have, (
        "d%d asks for %d WHEAT and feeds %s animals, but the shed holds %r at hour %d -- the hour "
        "the dawn tour reaches it. The PICKUP loads nothing and every FEED on the tour is dropped."
        % (day, wanted, row.get("feeds"), have, PICKUP_HOUR))
