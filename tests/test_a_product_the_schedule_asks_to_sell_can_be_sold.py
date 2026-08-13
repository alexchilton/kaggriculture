"""Three of the nine products cannot be sold by this agent at all, under any flag.

`SELLABLE` is the tuple the whole market loop iterates -- `for prod in SELLABLE` at
`schedule_agent_1455mh:3495`, the shed-eviction ranking at `:3452`, and `LIQUIDATE_LAST_DAY` at
`:3820`, which is nested inside that same loop. It reads:

    SELLABLE = ("MELON", "WOOL", "MILK", "STRAWBERRY", "FERTILIZER", "WHEAT")

against the env's nine (`reference/kaggriculture.py:25`). **CARROT, TOMATO and EGG are missing**, so a
schedule row saying `sells {CARROT: 55}` is read by nothing. There is no flag that reaches it and no
day on which it fires.

This is what every carrot arm has actually been measuring. Traced end to end on seed 11 with carrot
in the plants row AND the sells row, the chain is intact everywhere except the last link:

    seed bought 55  ->  planted 38  ->  tiles alive 43 on d26  ->  HARVEST fires
    ->  shed 36 on d27, 60 on d28, **92 on d29**  ->  SELL orders emitted: ZERO  ->  banked: $0

So the four measured carrot arms (`docs/carrot_swap_2026-08-12.md`) compared 55 tiles of wheat
against 55 tiles of nothing, and the answer "carrot loses $5,727" is a statement about the missing
wheat. The same holds for the goose arms: EGG is likewise unreachable, so `docs/fable_spawn_ring_
verdict_2026-08-12.md` and the two commits that deleted the geese rest on a season of eggs that
could never have been sold either.

Related: the `animals don't pay` entry in CLAUDE.md -- "always ask what the code could not express
before trusting a mechanic-level negative" -- and `feedback_offers_are_not_fills`. This is the same
failure a fourth and fifth time.
"""
import collections
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))

import kagg.search.schedule_agent_1455mh as sa            # noqa: E402
import kagg.search.routines as R                          # noqa: E402

SEED = 11
TPD = 24


def test_every_product_the_env_trades_is_reachable_by_the_sell_loop():
    """The premise, and the whole defect in one line.

    `SELLABLE` is not a policy choice about what is worth selling -- it is the iteration domain of
    the only loop that emits a SELL. A product absent from it is not deprioritised, it is invisible.
    """
    missing = [p for p in R.PRODUCTS if p not in sa.SELLABLE]
    assert not missing, (
        "the schedule may name any of the env's nine products in a `sells` row, but the market loop "
        "iterates only %r, so a row naming %r is silently discarded" % (list(sa.SELLABLE), missing))


def test_the_two_definitions_of_sellable_agree():
    """`SELLABLE` is defined TWICE at module level (`:1248` and `:2998`); the second wins.

    A fix applied to the first one is a no-op, which is exactly the kind of edit that reads as
    correct in a diff and changes nothing at runtime.
    """
    src = (REPO / "kagg/search/schedule_agent_1455mh.py").read_text().splitlines()
    defs = [ln for ln in src if ln.startswith("SELLABLE = ")]
    assert len(defs) == 1, (
        "SELLABLE is defined %d times; the last one silently wins and the earlier edits are dead: %r"
        % (len(defs), defs))


@pytest.mark.slow
def test_carrot_the_schedule_planted_and_harvested_actually_reaches_the_market():
    """End to end, because the structural test above cannot show the shed filling up.

    Asserts on FILLS, never on offers. The board is driven with a schedule that plants carrot in the
    late window and asks to sell it; the assertion is that the units the shed receives are the units
    that trade, not that carrot is profitable -- profitability is the question this defect has been
    preventing anyone from asking.
    """
    import breakdown as B
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills

    replay, schedule, team = B.TAPES["victor"]
    sched = {int(k): v for k, v in json.loads((REPO / schedule).read_text()).items()}

    # Build the carrot window in memory rather than depending on the state of the untracked
    # `schedule.json` on disk -- the same reason `scripts/carrot_late_window.py` exists.
    for day in (23, 24, 25, 26):
        row = sched.get(day)
        if not row:
            continue
        row["plants"] = ["CARROT" if c == "WHEAT" else c for c in (row.get("plants") or [])]
        seeds = dict(row.get("seeds") or {})
        if "WHEAT" in seeds:
            seeds["CARROT"] = seeds.pop("WHEAT")
        row["seeds"] = seeds
    for day in (26, 27, 28, 29):
        row = sched.get(day)
        if row is not None:
            row["sells"] = dict(row.get("sells") or {}, CARROT=55)

    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    cfg = dict(B.env_config(REPO / replay), seed=SEED, weedSpawnChance=0.0)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    agent = sa.make_agent(thin, 0, router=True)
    tape = B.tape_policy(REPO / replay, team, 1)

    peak_shed = 0
    with record_fills(env) as fills:
        for t in range(719):
            o0, o1 = env.state[0].observation, env.state[1].observation
            peak_shed = max(peak_shed, int((o0["private"].get("shed") or {}).get("CARROT", 0)))
            a0, a1 = agent(o0), tape(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            if env.state[0].status == "DONE":
                break
        units, revenue = fills.sold(0, "CARROT")

    assert peak_shed > 0, "the schedule never got carrot into the shed; this tests the wrong link"
    assert units > 0, (
        "%d carrot reached the shed and NONE of it was ever offered for sale -- the season ends "
        "holding it" % peak_shed)
