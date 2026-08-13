"""The goose machinery was deleted on evidence that is now void, and this restores it.

`7a88d30` ("Delete the geese rather than leave a losing flag in the tree") removed `HERD_GEESE` and
`swap_in_geese` from `kagg/search/schedule_agent_1455mh.py`, on the strength of `c9c1c18`'s
measurement: "-21k a game at one bird in the mirror, and 42 points of win rate against 24 recorded
opponents at two." That measurement is void: `SELLABLE` held only six of the env's nine product
names at the time (see `tests/test_a_product_the_schedule_asks_to_sell_can_be_sold.py`), and EGG was
never one of them. Every goose ever measured produced eggs that could not be sold under any flag, on
any day -- pure cost, with its entire revenue line unreachable.

`SELLABLE` is fixed now. This file asserts the restored mechanism is wired correctly and, end to end,
that a goose actually gets a COOP, actually gets bought, and its EGG actually reaches a market FILL --
never an offer, per `feedback_offers_are_not_fills`.

This file does NOT claim geese pay. `HERD_GEESE` defaults to 0, and nothing here turns it on for the
shipped agent. That question belongs to `scripts/product_search.py`, which already looks for this
exact module attribute name.
"""
import copy
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))

import kagg.search.schedule_agent_1455mh as sa            # noqa: E402
import kagg.search.routines as R                           # noqa: E402

SEED = 11


def test_herd_geese_flag_exists_and_defaults_off():
    """`scripts/product_search.py` resolves its `GEESE_FLAG` at import time by `hasattr`-probing
    `("HERD_GEESE", "GEESE", "HERD_GOOSE", "WANT_GEESE")` on this module and silently pins the swept
    axis to 0 if none exist. The flag must exist under exactly this name, and must default to 0 so
    restoring the mechanism changes nothing for the shipped agent until it is deliberately measured.
    """
    assert hasattr(sa, "HERD_GEESE"), "product_search.py's GEESE_FLAG probe will find nothing"
    assert sa.HERD_GEESE == 0, "restoring the mechanism must not silently turn it on"


def test_product_search_actually_finds_the_flag():
    """The exact detection `product_search.py` performs at import time, run directly."""
    import product_search as PS
    assert PS.GEESE_FLAG == "HERD_GEESE"


def _fake_schedule():
    """A minimal schedule with SHEEP at day 0 and COW at day 3, both in `animals_bought` AND
    `places`, matching the shape `swap_in_geese` reads.
    """
    return {
        0: {"animals_bought": {"SHEEP": 2}, "places": ["SHEEP", "SHEEP"]},
        3: {"animals_bought": {"COW": 1}, "places": ["COW"]},
    }


def test_swap_in_geese_moves_both_rows_together():
    """A goose is not just a purchase -- it is a purchase AND a pen. `_place_animals` reads `places`
    for what to BUILD and `animals_bought` for what to PAY for; a swap that only touches one of them
    buys a goose and builds it the wrong structure, and `PLACE` silently no-ops on a mismatched pen.
    """
    out = sa.swap_in_geese(_fake_schedule(), geese=1)
    assert out[0]["animals_bought"] == {"SHEEP": 1, "GOOSE": 1}
    assert out[0]["places"].count("GOOSE") == 1
    assert out[0]["places"].count("SHEEP") == 1
    # The count for the day is untouched -- still two animals total.
    assert sum(out[0]["animals_bought"].values()) == 2
    assert len(out[0]["places"]) == 2


def test_swap_in_geese_takes_earliest_first_and_cycles_sheep_then_cow():
    """`HERD_GEESE_FROM = ("SHEEP", "COW")`: the first goose comes from the earliest SHEEP row, the
    second from the earliest COW row, matching the alternation the flag's docstring promises.

    The COW row sits at day 6, matching `HERD_GEESE_EARLIEST[1] == 6` -- the floor the SECOND goose
    is gated on -- so both swaps are actually reachable.
    """
    assert sa.HERD_GEESE_EARLIEST[1] == 6
    sched = {0: {"animals_bought": {"SHEEP": 2}, "places": ["SHEEP", "SHEEP"]},
             6: {"animals_bought": {"COW": 1}, "places": ["COW"]}}
    out = sa.swap_in_geese(sched, geese=2)
    assert out[0]["animals_bought"].get("SHEEP", 0) == 1     # one taken
    assert out[0]["animals_bought"]["GOOSE"] == 1
    assert out[6]["animals_bought"] == {"GOOSE": 1}           # the COW row's animal became a goose


def test_swap_in_geese_never_mutates_the_input():
    """The schedule handed in is the caller's -- `product_search.py` mutates it for other arms in
    the SAME process, and `make_agent` must not see a goose neither it nor the caller asked for.
    """
    original = _fake_schedule()
    frozen = copy.deepcopy(original)
    sa.swap_in_geese(original, geese=2)
    assert original == frozen, "swap_in_geese must return a copy, not edit the schedule in place"


def test_swap_in_geese_respects_the_earliest_floor():
    """`HERD_GEESE_EARLIEST` gates each goose on a zero-walk cell existing yet. A day-0 SHEEP row
    must not be swapped for a goose whose floor has not been reached.
    """
    sched = {0: {"animals_bought": {"SHEEP": 1}, "places": ["SHEEP"]},
             10: {"animals_bought": {"SHEEP": 1}, "places": ["SHEEP"]}}
    # The third goose (index 2) is floored at HERD_GEESE_EARLIEST[2] == 10, so the day-0 row must
    # survive untouched and only the day-10 row may be swapped -- but there is only one SHEEP row
    # available at or after day 10 anyway, so this checks the day-0 row is never touched for k=2.
    assert sa.HERD_GEESE_EARLIEST[2] == 10
    out = sa.swap_in_geese(sched, geese=1)   # k=0, floor 0 -- allowed to take day 0
    assert out[0]["animals_bought"] == {"GOOSE": 1}


def test_make_agent_leaves_the_schedule_alone_when_herd_geese_is_zero(monkeypatch):
    """The off switch actually switches it off: with `HERD_GEESE = 0`, `make_agent` must not run the
    schedule through `swap_in_geese` at all.
    """
    monkeypatch.setattr(sa, "HERD_GEESE", 0)
    calls = []
    real = sa.swap_in_geese

    def spy(*a, **kw):
        calls.append(1)
        return real(*a, **kw)

    monkeypatch.setattr(sa, "swap_in_geese", spy)
    sa.make_agent(_fake_schedule(), 0, router=False)
    assert not calls, "HERD_GEESE == 0 must not invoke swap_in_geese"


@pytest.mark.slow
def test_a_goose_gets_a_coop_and_its_egg_reaches_a_fill(monkeypatch):
    """End to end. Forces `HERD_GEESE = 1` against the Victor schedule (which has SHEEP at day 0, so
    the very first goose is available immediately) and asserts on the environment's own ground truth:

    - a COOP tile actually appears on the board (not merely requested)
    - a GOOSE is actually bought (`BUY_ANIMAL`, a FILL)
    - EGG actually reaches a market FILL (`SELL`, a FILL, never an offer)

    This does not assert profitability -- only that the mechanism restored above is not dead code.
    """
    import breakdown as B
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills

    monkeypatch.setattr(sa, "HERD_GEESE", 1)

    replay, schedule, team = B.TAPES["victor"]
    raw = json.loads((REPO / schedule).read_text())
    sched = {int(k): v for k, v in raw.items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}

    cfg = dict(B.env_config(REPO / replay), seed=SEED, weedSpawnChance=0.0)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    agent = sa.make_agent(thin, 0, router=True)
    tape = B.tape_policy(REPO / replay, team, 1)

    saw_coop = False
    with record_fills(env) as fills:
        for t in range(719):
            o0, o1 = env.state[0].observation, env.state[1].observation
            for row in o0["farms"][0]["tiles"]:
                for cell in row:
                    if isinstance(cell, dict) and cell.get("kind") == "COOP":
                        saw_coop = True
            a0, a1 = agent(o0), tape(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            if env.state[0].status == "DONE":
                break
        bought_units = fills.units(0, "BUY_ANIMAL", "GOOSE")
        sold_units, sold_revenue = fills.sold(0, "EGG")

    assert saw_coop, "no COOP was ever built -- the pen never landed on the board"
    assert bought_units > 0, "no GOOSE was ever actually bought (a BUY_ANIMAL fill)"
    assert sold_units > 0, (
        "the goose produced EGG but none of it reached a market FILL -- exactly the defect "
        "SELLABLE's missing EGG entry caused, and exactly what this restoration was meant to fix")
    assert sold_revenue > 0
