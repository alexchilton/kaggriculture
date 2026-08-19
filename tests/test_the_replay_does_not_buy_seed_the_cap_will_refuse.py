"""The replayed opening buys 23 strawberry seed on d11; the cap only ever plants 18 of them.

`REPLAY_OPENING_DAYS` sends the tape's MARKET orders as well as its unit actions, so d11 h0 issues his
`BUY_SEED STRAWBERRY 23` -- sized for the 42-tile season he played. `STRAWBERRY_TILES_BY_DRAIN` holds
us to 37, so five of those seeds are never sown. Traced 2026-08-19 on his own seed 70683142:

    BUY_SEED STRAWBERRY   d5 h0 x2   d6 h0 x3   d7 h0 x1   d8 h0 x1   d11 h0 x23
    seed held / standing  d11: 0 / 19      d12: 5 / 37      d13..d29: 5 / ...

The five sit untouched from d12 to the final bell -- $500 at `router.SEED_COST`, dead for eighteen
days, on a ladder whose median margin is $1,983 and whose narrowest losses are $20 and $85.

`emit_seed`'s own cap cannot reach this and was measured byte-identical trying: the purchase happens
on a REPLAYED turn, where our market orders are discarded and the tape's are sent.

The fix belongs in the replay's order loop, which already re-labels `BUY_ANIMAL` for the herd split
under the rule "the count and the turn stay the tape's; only the species is ours". Here the turn stays
his and the COUNT becomes ours -- trimmed to the most strawberry the season can plant, never below it.

**Ceiling is `max(STRAWBERRY_TILES_BY_DRAIN)`, not the day's own drain count.** Shops unlock on
3,6,9,12, so d11 sees three draws and d12 sees four; pricing the purchase off d11's count would buy for
a cap of 36 when d12's cap is 37, and under-buying costs a whole tile rather than a spare seed.
"""
import collections
import json
import pathlib

import pytest

DATA = pathlib.Path("/Users/alexchilton/DataspellProjects/kaggriculture")
TAPE = DATA / "data/seed_scripts/kawashigi/92466371.json"
PLAN = DATA / "data/seed_scripts/kawashigi_b3/schedule.json"
TEAM = "カワシギ"
SEED = 70683142
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


@pytest.fixture(scope="module")
def the_season():
    """A full season on the strawberry arm, his seat, his seed, his opponent."""
    pytest.importorskip("kaggle_environments")
    from kaggle_environments import make

    from kagg.search import melon_branch as MB, schedule_agent as SA
    MB.OPPONENT_MELON = 0

    d = json.loads(TAPE.read_text())
    s = d["info"]["TeamNames"].index(TEAM)
    o = 1 - s
    opp = [((f[o] or {}).get("action") or {}) for f in d["steps"][1:]]
    cfg = dict(d.get("configuration") or {})
    cfg.pop("steps", None)
    cfg["seed"] = SEED
    thin = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
            for k, r in json.loads(PLAN.read_text()).items()}

    env = make("kaggriculture", configuration=cfg, debug=False)
    env.reset(2)
    agent = SA.make_agent(thin, s, router=True)
    plants = collections.Counter()
    for t in range(720):
        if env.done:
            break
        ob = env.state[s].observation
        n = [len((env.state[0].observation["farms"][i] or {}).get("hands") or []) for i in (0, 1)]
        m = agent(ob)
        for u in [m["farmer"]] + list(m["hands"])[:n[s]]:
            if u and u[0] == "PLANT":
                plants[u[1]] += 1
        st = opp[t] if t < len(opp) else {}
        a = [None, None]
        a[s] = {"farmer": m["farmer"], "hands": list(m["hands"])[:n[s]], "market": m["market"]}
        a[o] = {"farmer": st.get("farmer") or ["PASS"],
                "hands": list(st.get("hands") or [])[:n[o]], "market": st.get("market") or []}
        env.step(a)

    ob = env.state[s].observation
    return {
        "seeds": {k: int(v) for k, v in ((ob.get("private") or {}).get("seeds") or {}).items() if v},
        "money": int(((ob.get("farms") or [{}, {}])[s] or {}).get("money", 0) or 0),
        "plants": dict(plants),
    }


def test_no_strawberry_seed_is_left_unsown(the_season):
    """The five the cap was always going to refuse must never be bought."""
    assert the_season["seeds"].get("STRAWBERRY", 0) == 0, (
        f"{the_season['seeds'].get('STRAWBERRY')} STRAWBERRY seed unsown at the final bell; the "
        f"replayed d11 order buys 23 for a 42-tile season while the cap plants 37. "
        f"Full shed: {the_season['seeds']}")


def test_the_strawberry_still_all_goes_in(the_season):
    """Trimming must not cost a TILE. If this drops below 37 the ceiling is too tight and the change
    is buying back $500 with a crop worth more than that."""
    assert the_season["plants"].get("STRAWBERRY", 0) == 37, (
        f"strawberry plantings fell to {the_season['plants'].get('STRAWBERRY')}; 37 is what the cap "
        f"allows and what the untrimmed season plants, so anything less means the purchase ceiling "
        f"is under-buying")


def test_the_season_is_not_worse_off(the_season):
    """$159,623 is the measured season before this change. The seed is worth $500, so the floor is
    the old number -- a trim that pays for itself cannot bank less."""
    assert the_season["money"] >= 159_623, (
        f"season banked {the_season['money']} against 159,623 before the trim; buying less seed "
        f"cannot cost money unless it has changed something else in the opening")
