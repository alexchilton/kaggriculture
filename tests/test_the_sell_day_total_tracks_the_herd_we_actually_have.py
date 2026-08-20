"""A sells row recorded from ANOTHER herd caps the day below what OUR herd produces.

The `sells` row is an absolute count read off Kawashigi's trajectory, and his herd is COW 10 /
SHEEP 4.
`SHOP_ADAPT_HERD` re-species our purchases on the live shop draw, so the herd that fills our shed
is not the herd the rows describe -- on seed 11 we end COW 6 / SHEEP 8.
Measured on real ladder replays, the mismatch is the milk failure: 27 units sold at $108-213
against 90 dumped below $42, because the day total (`allow`) releases his row while our herd
produces at its own rate, and the surplus leaves late, into a book we crashed ourselves.

The mechanism under test: from `HERD_SELL_FROM_DAY`, the day total for an animal product is
floored at the CURRENT herd's own daily production rate, so stock leaves at the speed the herd
makes it.
The floor widens `allow` only (`max`), so a row asking for more still fires in full -- the
refuse-to-sell arm that cost -$16,025 is unreachable -- and `rate[prod]` still bounds every
single offer, so the one-turn dump that cost $111,238 -> $77,587 of mean money is unreachable too.

The fixture shrinks the schedule's MILK rows on d11-d13 to 1 while the seed-11 herd makes
~9 milk a day, and asserts on FILLS (never offers): three days at a row of 1 must still sell
the shed at the herd's rate, not at the row's.
"""
import collections
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))

import kagg.search.schedule_agent as sa            # noqa: E402
import kagg.search.routines as R                   # noqa: E402

SEED = 11
TPD = 24
LAST_DAY = 14          # drive d0..d13 inclusive; milk first reaches the shed on d11 on this seed


def test_the_herd_rate_is_read_off_the_board():
    """The floor's input: a board with 6 cows and 8 sheep produces ~9 milk and ~10 wool a day.

    (1 + interval) / interval per animal, because a fed-and-cared animal banks one care bonus per
    day and consumes them all on its production day -- `reference/kaggriculture.py:822-828`.
    """
    tiles = [[{"kind": "PASTURE", "animal": "COW"} for _ in range(6)]
             + [{"kind": "PASTURE", "animal": "SHEEP"} for _ in range(8)]]
    rate = sa._herd_daily_rate(tiles)
    assert rate["MILK"] == 9, rate      # 6 cows x 3 units / 2 days
    assert rate["WOOL"] == 11, rate     # 8 sheep x 4 units / 3 days, rounded
    assert "WHEAT" not in rate, "crops are not the herd's; the floor must not touch them"


@pytest.mark.slow
def test_a_row_from_his_herd_does_not_cap_milk_below_our_herds_rate():
    import breakdown as B
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills

    replay, schedule, team = B.TAPES["kawashigi"]
    sched = {int(k): v for k, v in json.loads((REPO / schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    # d8 asks MILK 12 while the shed's first milk lands on d11, so the schedule's own d8 row would
    # go down as MISSED and the carry -- which exists to recover a missed row -- would release 12
    # on d11 whatever this fixture does. Zero it: the mechanism under test is the day total, and
    # the fixture must not owe anything for the carry to recover.
    for d, q in ((8, 0), (11, 1), (12, 1), (13, 1)):
        thin[d] = dict(thin[d])
        thin[d]["sells"] = dict(thin[d].get("sells") or {})
        thin[d]["sells"]["MILK"] = q
    cfg = dict(B.env_config(REPO / replay), seed=SEED, weedSpawnChance=0.0)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    agent = sa.make_agent(thin, 0, router=True)
    tape = B.tape_policy(REPO / replay, team, 1)

    with record_fills(env) as fills:
        for t in range(TPD * LAST_DAY):
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = agent(o0), tape(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
        sold = fills.units(0, "SELL", "MILK")

    # The seed-11 herd holds ~6 milk in the shed at each of the three dawns and makes ~9 a day.
    # Rows of 1 release at most 3 units over the window (the carry recovers only a MISSED row,
    # and a row of 1 is met).  Selling at the herd's rate clears the shed's ~6 each day.
    assert sold >= 10, (
        "d11-d13 rows of MILK 1 against a herd making ~9/day: %d units filled -- the day total is "
        "reading his row, not our herd" % sold)
