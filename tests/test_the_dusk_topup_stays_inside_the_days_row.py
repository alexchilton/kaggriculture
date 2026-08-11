"""The dusk feed top-up may not take the day past the `buys` row.

`DUSK_FEED_TOPUP` buys wheat late in the day so the shed carries tomorrow's ration:
`gap = (alive + arriving) - shed - spare`. It is a safety net against a row that under-counts the
herd, and it fires on the shed alone, with no idea what the day has already bought.

On Victor's d6 that costs a unit. His row is `buys {WHEAT: 5}` and he drips exactly five, at h4, h6,
h8, h11 and h12. Ours:

    h00  BUY_PRODUCT WHEAT 3   filled 3   shed 7  pens 6  unfed 6
    h01  BUY_PRODUCT WHEAT 1   filled 1   shed 7  pens 6  unfed 6
    h10  BUY_PRODUCT WHEAT 1   filled 0
    h18  BUY_PRODUCT WHEAT 1   filled 1   shed 4  pens 6  unfed 0     <- top-up
    h19  BUY_PRODUCT WHEAT 1   filled 1   shed 5  pens 7  unfed 1     <- top-up

Four by h1, which is the row less one, and then the top-up adds two against a herd with nothing left
to feed -- `unfed 0` at h18. Six bought for a row of five.

The row is not a floor here and must not be treated as one: the sell side already learned this the
hard way (`NET_THE_TWO_LEGS`), and a wheat round trip pays the spread in both directions. The row is
the plan's own statement of the day's ration, and the top-up's job is to catch a row that is SHORT,
not to add to one that is already met.

The assertion is on FILLS per product per day, against the row. It says nothing about a day with no
`buys` row at all -- there the top-up is the only rule there is and remains unbounded.
"""
import collections
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))

SEED = 11
DAYS = 12
TPD = 24


@pytest.fixture(scope="module")
def bought():
    """`{day: Counter of BUY_PRODUCT units that actually filled}` for our seat."""
    import breakdown as B
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills
    import kagg.search.schedule_agent_1455mh as sa

    replay, schedule, team = B.TAPES["victor"]
    sched = {int(k): v for k, v in json.loads((REPO / schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}

    cfg = dict(B.env_config(REPO / replay), seed=SEED, weedSpawnChance=0.0)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    agent = sa.make_agent(thin, 0, router=True)
    tape = B.tape_policy(REPO / replay, team, 1)

    per_day = collections.defaultdict(collections.Counter)
    with record_fills(env) as fills:
        prev = collections.Counter()
        for t in range(TPD * DAYS):
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = agent(o0), tape(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            cur = collections.Counter({p: fills.units(0, "BUY_PRODUCT", p)
                                       for p in fills.products()})
            per_day[t // TPD] += cur - prev
            prev = cur
    return dict(per_day)


def _rows():
    raw = json.loads((REPO / "data/seed_scripts/victor/schedule.json").read_text())
    return {int(k): dict(v.get("buys") or {}) for k, v in raw.items()}


def test_the_premise_some_day_has_a_buys_row(bought):
    """Guard. With no row in range the assertion below is vacuous."""
    rows = _rows()
    assert any(rows.get(d) for d in range(DAYS)), f"no `buys` row in d0-d{DAYS - 1}"


@pytest.mark.parametrize("day", range(DAYS))
def test_the_day_does_not_outrun_its_buys_row(bought, day):
    want = _rows().get(day) or {}
    if not want:
        pytest.skip(f"d{day} has no buys row; the top-up is unbounded there by design")
    got = bought.get(day, collections.Counter())
    over = {c: (int(got.get(c, 0)), int(q)) for c, q in want.items() if int(got.get(c, 0)) > int(q)}
    assert not over, (
        f"d{day} row buys {want} and the day filled {dict(got)}; "
        + ", ".join(f"{c}: bought {g} against a row of {w}" for c, (g, w) in sorted(over.items()))
        + ". The dusk top-up fires on the shed alone and cannot see what the day already bought.")


@pytest.mark.parametrize("day", range(DAYS))
def test_the_day_also_meets_its_buys_row(bought, day):
    """The other side of the same cap, and the reason it needs one.

    Capping on ORDERS rather than fills cuts both ways. `state["ordered"]` is credited when an order
    is queued and a BUY_PRODUCT the env refuses is silent, so an order that loses the slot race still
    closes the row and the day never retries. d6 h10: bank $43, wheat $33, and the turn queues
    `SELL WOOL 5, SELL FERTILIZER 1, BUY_LAND, BUY_SEED STRAWBERRY 3, BUY_PRODUCT WHEAT 1`.
    `_process_market` walks the slots in order, so the $1,000 parcel and the seed take everything the
    wool raised and the wheat, last in the queue, fills nothing -- `buy_product 4/5`, with the bank
    back to $90 by dusk and nothing spending it.
    """
    want = _rows().get(day) or {}
    if not want:
        pytest.skip(f"d{day} has no buys row")
    got = bought.get(day, collections.Counter())
    short = {c: (int(got.get(c, 0)), int(q)) for c, q in want.items() if int(got.get(c, 0)) < int(q)}
    assert not short, (
        f"d{day} row buys {want} and the day filled {dict(got)}; "
        + ", ".join(f"{c}: bought {g} against a row of {w}" for c, (g, w) in sorted(short.items()))
        + ". An order that cannot fill still counts against the row, so the day stops retrying.")
