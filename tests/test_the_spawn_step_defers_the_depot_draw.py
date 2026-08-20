"""The spawn-ring step must DEFER the farmer's depot draw, never delete it.

The mechanism (traced 2026-08-11, victor tape, seed 11, day 4):

`agent()` computes the day's actions with `_router_acts`, which WALKS the committed tour --
a depot stop at the head of the farmer's route is consumed the moment it emits `PICKUP`
(`node.pick` emptied, the local shed counter decremented). The call site then overwrites
`acts[0]` with the `_clear_the_spawn_ring` step. The step is right; the order is wrong: the
route now believes wheat is in hand that was never drawn. At the first pen, `_live_ops`
offers no FEED (inventory gate), `FETCH_THE_FEED_AND_RETURN` inserts an unplanned shed round
trip, and the day pays 6 unpriced turns -- 2 for the step, 4 for the phantom draw. A tour
costed at 21 of 24 spends 27, and its tail stop `(0,4)[WATER, HARVEST]` is dropped:
`water 14/15`, `harvest 4/5`, one tile never freed, and d5 inherits a board one tile short
(`plant 4/5`, `strawb 6/7`).

The assertion is grid-level, on the two rows the dropped stop owns, because the route state
is a closure and the grid is this project's only acceptance criterion.
"""
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))

SEED = 11
WEEDS = 0.0


def test_day_4_keeps_the_tail_of_the_farmers_tour():
    import breakdown as B

    replay, schedule, team = B.TAPES["victor"]
    sched = {int(k): v for k, v in
             json.loads((REPO / schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    import kagg.search.schedule_agent_1455mh as sa

    def mine():
        a = sa.make_agent(thin, 0, router=True)
        return lambda o, t: a(o)

    economy = B.env_config(REPO / replay)
    ours, ops = B.run(mine, lambda: B.tape_policy(REPO / replay, team, 1),
                      SEED, WEEDS, stop_day=5, economy=economy)
    # The tape's day 4 is WATER 15 / HARVEST 5. Ours plans exactly that (`uncovered: []`)
    # and must also EMIT it: the phantom depot draw was worth one dropped stop, two rows.
    assert ops[4]["WATER"] == 15, f"d4 water {ops[4]['WATER']}/15 -- the tour tail was dropped"
    assert ops[4]["HARVEST"] == 5, f"d4 harvest {ops[4]['HARVEST']}/5 -- the tour tail was dropped"
