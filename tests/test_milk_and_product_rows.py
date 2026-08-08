"""The two biggest unexplained rows in the `seb` baseline: `sh:milk +464` and `buy_product -164`.

Both were framed as losses. Measured against the environment's own commit points rather than against
`breakdown.py`'s shed-delta estimator, one of them is not a difference at all and the other is not a
loss:

- **`buy_product -164` is a COVERAGE ARTIFACT.** `breakdown.py` can only read a fill on a turn clean
  of DROP/PICKUP/PLACE and says so, and our clean fraction is 49% against the tape's 68% -- so the
  row compares two differently-censored lower bounds. `_commit_unit` returns True exactly when one
  unit changes hands, so wrapping it is the ground truth: we buy **more** wheat than the tape, not
  164 units fewer.

- **`sh:milk +464` is real, exact (it is a state row) and is a TIMING difference, not unsold stock.**
  Every unit of milk we make is sold. The identity closes to the unit on both sides:
  `made == sold + yield_units still standing on the cows at season end`.

The tests below pin those two facts, plus the mechanism behind the extra milk (the CARE bonus in
`_daily_refresh_animals`) and the *separate*, still-open loss that co-occurs with it -- strawberry
tiles dying of thirst while unit-turns idle.

Marked slow: each fixture plays two full 719-turn games in the real environment.
"""

import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import schedule_agent                                    # noqa: E402
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy               # noqa: E402
import scripts.probe_animal_yield as PA                                   # noqa: E402
import scripts.probe_market_fills as PM                                   # noqa: E402
import scripts.probe_plant_yield as PP                                    # noqa: E402

SEED, WEEDS, TAPE = 11, 0.0, "seb"

pytestmark = pytest.mark.slow


def _play(make0, opp):
    """One full game with all three env probes installed, returning their tallies for seat 0."""
    from kaggle_environments import make
    PM.install()
    PA.install()
    PP.install()
    PM.REC.clear()
    PA.REC.clear()
    PP.REC.clear()
    PP.DEATHS.clear()
    PA.CALLS[0] = PP.CALLS[0] = 0
    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": WEEDS}, debug=True)
    env.reset(2)
    p0, p1 = make0(), opp()
    idle = collections.Counter()
    for t in range(719):
        PM.TURN[0] = PA.DAY[0] = PP.DAY[0] = t // 24
        PM.TURN[0] = t
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        for a in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
            if a and a[0] == "PASS":
                idle[t // 24] += 1
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
    onbeast = sum(int(c["yield_units"])
                  for r in env.state[0].observation["farms"][0]["tiles"] for c in r
                  if isinstance(c, dict) and c.get("animal") == "COW")
    return {"market": list(PM.REC),
            "animal": {k: collections.Counter(v) for k, v in PA.REC.items()},
            "plant": {k: collections.Counter(v) for k, v in PP.REC.items()},
            "deaths": [d for d in PP.DEATHS if d[0] == 0],
            "idle": idle,
            "cow_yield_units_left": onbeast}


@pytest.fixture(scope="module")
def sides():
    replay, schedule, team = TAPES[TAPE]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    opp = lambda: tape_policy(replay, team, 1)
    tape = _play(lambda: tape_policy(replay, team, 0), opp)
    a = schedule_agent.make_agent(thin, 0, router=True)
    ours = _play(lambda: (lambda o, t: a(o)), opp)
    return ours, tape


def _fills(side, op, seat=0):
    return sum(1 for r in side["market"] if r["seat"] == seat and r["op"] == op and r["ok"])


def _sold(side, item, seat=0):
    return sum(1 for r in side["market"]
               if r["seat"] == seat and r["op"] == "SELL" and r["item"] == item and r["ok"])


def _tot(side, key, kind="animal", species="COW"):
    return sum(c[key] for (s, _d, sp), c in side[kind].items() if s == 0 and sp == species)


def test_buy_product_row_is_a_coverage_artifact_not_a_missing_play(sides):
    """`buy_product -164` says we skip the winner's wheat-into-animals play. We do not skip it.

    `breakdown.py` reports these rows as a disclosed LOWER BOUND -- a turn with a DROP contributes
    zero -- and our coverage is 49% against the tape's 68%, so the row is two differently-censored
    counts subtracted from one another. Counted at `_commit_unit`, where a True return IS one unit
    changing hands, we buy MORE wheat than the tape does.
    """
    ours, tape = sides
    o, h = _fills(ours, "BUY_PRODUCT"), _fills(tape, "BUY_PRODUCT")
    assert o >= h, f"exact BUY_PRODUCT fills ours {o} tape {h}"
    # ...and nowhere near the 164-unit deficit the row reports.
    assert o - h > -20, f"exact BUY_PRODUCT fills ours {o} tape {h}, breakdown row says -164"


def test_only_a_couple_of_buys_are_ever_refused(sides):
    """If the play were being refused for budget, the refusals would be many. There are two."""
    ours, _tape = sides
    refused = [r for r in ours["market"]
               if r["seat"] == 0 and r["op"] == "BUY_PRODUCT" and not r["ok"]]
    assert len(refused) <= 5, [(r["t"] // 24, r["money"], r["price"]) for r in refused]
    # Every refusal that does happen is a budget refusal, not a legality one.
    assert all(r["money"] < r["price"] for r in refused)


def test_every_unit_of_milk_we_make_is_sold(sides):
    """`sh:milk +464` is a stock held longer, not a stock never moved.

    Milk leaves the farm in exactly one way (SELL) and enters it in exactly one way (the dusk
    refresh in `_daily_refresh_animals`), so `made - sold` must equal what is still sitting
    unharvested on the cows when the season ends. It does, on both sides, to the unit.
    """
    ours, tape = sides
    for side, lab in ((ours, "ours"), (tape, "tape")):
        made, sold, left = _tot(side, "made"), _sold(side, "MILK"), side["cow_yield_units_left"]
        assert made - sold == left, f"{lab}: made {made} sold {sold} left-on-cow {left}"
    # And we sell MORE milk than the tape, not less -- the pile-up is timing, not a sales failure.
    assert _sold(ours, "MILK") > _sold(tape, "MILK")


def test_the_extra_milk_comes_from_the_care_bonus(sides):
    """CARE is the mechanism: `pending_care_bonus` is only banked on a day the tile is fed AND cared.

    So the extra milk should track extra cared-tile-days, not extra cows. The herd is identical.
    """
    ours, tape = sides
    assert _tot(ours, "tiles") == pytest.approx(_tot(tape, "tiles"), rel=0.05)
    assert _tot(ours, "cared") > _tot(tape, "cared")
    assert _tot(ours, "bonus") > _tot(tape, "bonus")
    extra_made = _tot(ours, "made") - _tot(tape, "made")
    extra_bonus = _tot(ours, "bonus") - _tot(tape, "bonus")
    # The whole of the production gain is bonus, not base rate: same cows, same interval.
    assert abs(extra_made - extra_bonus) <= 5, (extra_made, extra_bonus)


def test_no_cow_ever_starves(sides):
    """Correctness floor for the milk finding specifically: the milk herd never shrinks.

    The COW herd is identical to the tape's all season, which is what makes "we make more milk from
    the same cows" a statement about CARE rather than about herd size.
    """
    ours, _tape = sides
    escaped = sum(c["escaped"] for (s, _d, sp), c in ours["animal"].items()
                  if s == 0 and sp == "COW")
    assert escaped == 0


@pytest.mark.xfail(strict=True, reason="OPEN BUG, found by this work and not owned by it: two "
                                       "SHEEP starve at d15/d16 (two consecutive unfed days, "
                                       "`_daily_refresh_animals`), on days we finished with 13 and "
                                       "16 idle unit-turns. Herd 11 -> 9 for the rest of the "
                                       "season; the tape keeps all 11. This is the `sheep -2` row "
                                       "and most of the wool gap, and it is NOT a milk trade.")
def test_no_animal_of_any_species_starves(sides):
    """The wool loss is a feeding failure with spare capacity, not the price paid for the milk."""
    ours, tape = sides
    ours_esc = collections.Counter()
    for (s, _d, sp), c in ours["animal"].items():
        if s == 0 and c["escaped"]:
            ours_esc[sp] += c["escaped"]
    tape_esc = sum(c["escaped"] for (s, _d, _sp), c in tape["animal"].items() if s == 0)
    assert tape_esc == 0, "the tape starves nothing; this test's premise"
    assert not ours_esc, dict(ours_esc)


@pytest.mark.xfail(strict=True, reason="OPEN BUG, not owned by the milk/product work: the router "
                                       "prices every one of these rescue waters at $360-$480, the "
                                       "highest prize on the board, and still leaves 12-29 "
                                       "unit-turns idling on each of the six days one dies.")
def test_no_crop_tile_dies_of_thirst_while_units_idle(sides):
    """The strawberry loss is NOT the price paid for the milk -- there was spare capacity for both.

    `strawb -94` and `sh:straw -78` look like the other half of a milk-for-strawberry trade. They
    are not: 12 strawberry tiles die of two consecutive dry days (the tape loses zero), and on every
    day one dies we finished the day with idle unit-turns to spare. Nothing was traded away; the
    water was simply never served.
    """
    ours, tape = sides
    deaths = ours["deaths"]
    tape_deaths = sum(c["died"] for (s, _d, _c), c in tape["plant"].items() if s == 0)
    assert tape_deaths == 0, "the tape loses no crop to thirst; this test's premise"
    assert all(ours["idle"][d[1]] > 0 for d in deaths), \
        "a death on a day with zero idle turns WOULD be a capacity trade"
    assert not deaths, [(f"d{d[1]}", d[2], f"prize ${d[5]}") for d in deaths]
