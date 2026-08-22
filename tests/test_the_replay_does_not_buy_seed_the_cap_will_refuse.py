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

---

**REVERSED FOR THIS ARM BY `b105d05`, and this file did not follow. Corrected 2026-08-22.**

Everything above is still true about the seed. What it does not price is that the bank is SHARED
state on a replayed day: `_do_hire` fails silently on a thin bank
(`reference/kaggriculture.py:691`) at `mult * fib(hires_today)`, so the $60 the trim saves at d6
buys us a hand at d8 that the tape could not afford, and the seasons diverge from there.

    scripts/seed_tape_grid.py --vs-all --live-shops --opponent kawashigi_b3, 16 towns, d0-d29

    trim on all arms      10 seeds 130-132,   5 seeds 60-62,  1 seed 40
    trim off strawberry    5 seeds   0,      10 seeds    25,  1 seed 40

So the trim ships on the MELON arm only -- `not q4_armed and not melon_armed`
(`schedule_agent.py:5900`) -- where seed 11 measures +$240 with it and level without.

This fixture forces `MB.OPPONENT_MELON = 0`, which ARMS the melon latch, so the trim does not run
in any test in this file. Two assertions here were describing its effects anyway and had been red
since that commit: `STRAWBERRY == 37` against an untrimmed 42, and `money >= 159,623` against a
measured 147,036. Both are the pre-`b105d05` numbers, kept alive by nobody re-reading them.

`test_the_trim_is_off_on_the_strawberry_arm_and_that_is_measured` now guards the decision itself,
which nothing did before.
"""
import collections
import inspect
import json
import pathlib

import pytest

@pytest.fixture(autouse=True, scope="module")
def _put_the_globals_back():
    """Restore every module global this file changes.

    Autouse and module-scoped, so it is torn down after the fixture that does the changing -- which
    means this needs no knowledge of where in that fixture the assignment happens. The direct
    edit did need that knowledge, got it wrong on a multi-line `return {`, and left three files
    unparseable.

    Without this the leak is invisible under `-n 0` (the file runs last) and decides which tests
    fail under xdist (the worker poisons whatever it is handed next).
    """
    from kagg.search import melon_branch
    saved = [(melon_branch, 'OPPONENT_MELON', melon_branch.OPPONENT_MELON)]
    yield
    for mod, name, value in saved:
        setattr(mod, name, value)


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
    """Trimming must not cost a TILE.

    **Rewritten 2026-08-22. This read `== 37` and was measuring the trim on the arm the trim was
    taken OFF.** `b105d05` -- "Keep the tape's seed order on the strawberry arm, because our saving
    buys his refused hire" -- restricted the trim to the melon arm, and the shipped guard is
    `not q4_armed and not melon_armed` (`schedule_agent.py:5900`). This fixture forces
    `MB.OPPONENT_MELON = 0`, so the melon latch arms and the trim never runs here.

    The equality was also the wrong shape for its own docstring, which says "if this drops BELOW 37
    the ceiling is too tight". 37 is a floor, not a target: the untrimmed season plants 42, and
    `== 37` calls that a failure. A cap that lets MORE strawberry into the ground is not the defect
    this test was written to catch.
    """
    got = the_season["plants"].get("STRAWBERRY", 0)
    assert got >= 37, (
        f"strawberry plantings fell to {got}; 37 is what the cap allows, so anything less means "
        f"the purchase ceiling is under-buying and the trim is costing a tile rather than a seed")


def test_the_trim_is_off_on_the_strawberry_arm_and_that_is_measured(the_season):
    """The decision `b105d05` made, which nothing was guarding.

    The trim is sound on its own terms and is NOT free on a replayed day, because the bank is shared
    state and the reference hires off it. `_do_hire` fails SILENTLY on a thin bank
    (`reference/kaggriculture.py:691`) at `mult * fib(hires_today)`, so $60 saved at d6 buys us a
    hand at d8 that HE COULD NOT AFFORD, and the seasons part company from there.

    `scripts/seed_tape_grid.py --vs-all --live-shops --opponent kawashigi_b3`, 16 towns, d0-d29,
    cells differing from the tape the latches chose:

        trim on all arms      10 seeds 130-132,   5 seeds 60-62,  1 seed 40
        trim off strawberry    5 seeds   0,      10 seeds    25,  1 seed 40

    Worst case 132 -> 40, and five seeds exact for all thirty days. The melon arm keeps it and that
    is measured too: seed 11 at `--replay-days 30` ends +$240 with it and level at 0 cells without.

    Asserted through the shipped module rather than by re-running the grid, so it is a fast test
    that still goes red if someone widens the condition back over both arms.
    """
    from kagg.search import schedule_agent as SA
    src = inspect.getsource(SA.make_agent)
    i = src.find('o[0] == "BUY_SEED"')
    assert i > 0, "the BUY_SEED trim is gone from make_agent entirely"
    guard = src[i:i + 220]
    assert "_MB.BRANCH.armed_key" in guard and "_Q4.BRANCH.armed_key" in guard, (
        "the BUY_SEED trim no longer checks BOTH latches. It ships on the melon arm only "
        f"(`not q4_armed and not melon_armed`). Guard now reads:\n    {guard.strip()[:200]}\n"
        "  On the strawberry arm the trim measured 132 differing cells against 40 without it, "
        "because the $60 it saves buys a hire the tape was refused.")


def test_the_season_is_not_worse_off(the_season):
    """The strawberry arm's measured season, with the trim OFF where it belongs.

    **Was `>= 159_623`, which is the number from BEFORE `b105d05` took the trim off this arm.** A
    floor carried across the change that invalidated it: the run banks 147,036 and has done since
    that commit, so this was red for four days while describing a configuration that no longer
    ships.

    Kept as a floor rather than deleted, because a real regression on this arm should still show.
    It is set to the measured value, and the number is dated so the next person can tell whether it
    has aged the same way.
    """
    assert the_season["money"] >= 147_036, (
        f"season banked {the_season['money']} against 147,036 measured 2026-08-22 on the strawberry "
        f"arm with the trim off. Below this and something in the opening has changed.")
