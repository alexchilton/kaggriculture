"""The crop mix, checked against tetsuya's own recorded shop draws.

The plant-side counterpart of `test_the_herd_split_answers_tetsuyas_shop_draws.py`, and it exists
for the same reason: a schedule extracted from ONE replay copies one draw's answer. Only the corpus
can say which part of his mix is a habit and which part is a response.

Measured over his 78 recorded games (`data/logs/tets_all_games_crops_2026-08-19.log`):

    crop          min   max   mean    cv    games with any
    WHEAT          99   187  135.0  0.15         78/78
    STRAWBERRY     24    50   36.9  0.15         78/78
    MELON           8    19   12.9  0.18         78/78
    CARROT          0    65    2.2  4.07          9/78
    TOMATO          0    22    0.7  4.64          4/78
    straw+melon    32    65   49.8  0.12         78/78     <- the invariant

WHEAT, STRAWBERRY and MELON are on every board -- those are the habit. CARROT and TOMATO have a
coefficient of variation above 4.0 and appear in nine and four games: pure draw response. A constant
cannot be both.

Scored at the PLANT, never at the season total. He sows on a given day with a given set of shops
unlocked, and that is the only state a rule could have used; the end-of-season tally hands it a
day-29 draw nobody had on day 3.
"""
import collections
import inspect
import json
import pathlib

import pytest

from kagg.search import schedule_agent as SA

CORPUS = "data/seed_scripts"
PLAYER = "tetsuya"
CROPS = ("WHEAT", "STRAWBERRY", "MELON", "CARROT", "TOMATO")
#: Below this the seat never got a season going and its mix is noise.
MIN_PLANTS = 20


def _games():
    """(name, plants, shops_at_end) per game, where plants is [(day, shops_then, crop), ...]."""
    out, seen = [], set()
    for path in sorted(pathlib.Path(CORPUS).rglob("*.json")):
        if path.name in seen:
            continue
        try:
            rec = json.loads(path.read_text())
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue
        steps = rec.get("steps")
        if not steps or len(steps) < 700:
            continue
        obs = steps[-1][0].get("observation")
        if not isinstance(obs, dict):
            continue
        teams = (rec.get("info") or {}).get("TeamNames") or ["?", "?"]
        seat = next((i for i, n in enumerate(teams) if PLAYER in str(n).lower()), None)
        if seat is None:
            continue
        seen.add(path.name)
        plants = []
        for frame in steps[1:]:
            ob = (frame[0] or {}).get("observation") or {}
            act = (frame[seat] or {}).get("action") or {}
            then = list((ob.get("town") or {}).get("unlocked_shops") or [])
            day = int(ob.get("day", 0) or 0)
            for unit in [act.get("farmer")] + list(act.get("hands") or []):
                if unit and unit[0] == "PLANT" and len(unit) > 1:
                    plants.append((day, then, unit[1]))
        if len(plants) < MIN_PLANTS:
            continue
        out.append((path.name, plants, list((obs.get("town") or {}).get("unlocked_shops") or [])))
    return out


@pytest.fixture(scope="module")
def games():
    rows = _games()
    if len(rows) < 60:
        pytest.skip("recorded corpus not on disk (data/ is gitignored)")
    return rows


def _mix(plants):
    return collections.Counter(c for _d, _sh, c in plants)


def test_strawberry_plus_melon_is_his_invariant(games):
    """The premise: the dear crops are a fixed budget, and only their split with wheat moves.

    Individually strawberry and melon each swing 15-18% about their mean; their SUM swings 12%, and
    that is the number a rule should hold. If this stops holding, the plant side has no invariant
    and the rest of this file is measuring the wrong quantity.
    """
    sums = [_mix(p)["STRAWBERRY"] + _mix(p)["MELON"] for _n, p, _s in games]
    mean = sum(sums) / len(sums)
    sd = (sum((v - mean) ** 2 for v in sums) / len(sums)) ** 0.5
    assert 45 <= mean <= 55, "straw+melon mean is %.1f" % mean
    assert sd / mean < 0.20, "straw+melon cv is %.2f, not an invariant" % (sd / mean)


def test_carrot_and_tomato_are_draw_responses_not_habits(games):
    """The premise for the constants below: he plants these on a MINORITY of boards.

    A rule that sows them every game is not modelling a response, it is modelling a habit he does
    not have.
    """
    n = len(games)
    for crop, ceiling in (("CARROT", 0.30), ("TOMATO", 0.20)):
        seen = sum(1 for _name, p, _s in games if _mix(p)[crop])
        assert seen / n <= ceiling, (
            "%s now appears in %d of %d games (%.0f%%), so it may be a habit after all"
            % (crop, seen, n, 100 * seen / n))
        assert seen >= 2, "%s appears in %d games, too few to assert a response" % (crop, seen)


def test_his_tomato_tracks_the_shop_draw(games):
    """**His tomato is a shop response, and a clean one.**

    Tomato drains to PIZZA_SHOP and FARMERS_MARKET (`reference/kaggriculture.py:105,111`), and shops
    are drawn WITH replacement, so the COUNT of draining shops varies where presence barely does.
    Measured over the 78:

        tomato-draining shops    0    1    2    3    4    5
        games                   10   24   25    9    7    3
        games with tomato        0    0    1    0    1    2

    Not one tomato tile across all 34 games with fewer than two draining shops, and two of the three
    games with five. That is the variable.

    **This test does NOT assert on `WHEAT_TILES_TO_TOMATO`.** An earlier version did, read its
    docstring's word "unconditional", and was wrong: line 3919 gates the conversion on
    `melon_armed and not q4_armed`, so the constant alone says nothing about whether a tile is
    sown. Asserting on a name the branch does not read is how a change measures as a null.
    """
    by = collections.defaultdict(list)
    for _n, plants, shops in games:
        drain = sum(1 for s in shops if s in ("PIZZA_SHOP", "FARMERS_MARKET"))
        by[drain].append(_mix(plants)["TOMATO"])
    thin = [t for k, v in by.items() if k <= 1 for t in v]
    assert len(thin) >= 20, "too few thin-draw games to assert on"
    assert not any(thin), (
        "he now plants tomato on a board with at most one draining shop: %s" % sorted(t for t in thin if t))
    rich = [t for k, v in by.items() if k >= 4 for t in v]
    assert sum(1 for t in rich if t) / len(rich) > sum(
        1 for t in thin if t) / len(thin), "the drain-count signal has gone"


def test_the_tomato_tile_is_not_gated_on_the_shop_draw(games):
    """**The gate is a STRATEGY condition where his tomato is a SHOP response.**

    `_tom` fires on `melon_armed and not q4_armed` -- which arm the season is running, and nothing
    about the town. His own tomato is decided by the number of tomato-draining shops, and is zero
    across all 34 games with fewer than two of them.

    So the tile can be sown on a board he would never plant tomato on, and withheld on the five-shop
    boards where he plants 10-22 tiles. Passing means the decision reads the draw.

    RED as written on 2026-08-19.
    """
    src = inspect.getsource(SA)
    gate = "melon_armed" in src and "WHEAT_TILES_TO_TOMATO" in src
    assert not gate or "TOMATO_DRAIN_SHOPS" in src, (
        "the tomato tile is gated on the season's arm (`melon_armed`/`q4_armed`) and reads nothing "
        "about the town, while his tomato is zero on every board with <2 draining shops and present "
        "on 2 of 3 boards with five")


def test_carrot_is_the_crop_with_no_predictor_yet(games):
    """**An open question pinned as a fact, not a demand for a gate I cannot specify.**

    An earlier version of this test asserted `SHOP_ADAPT_CROPS`, on the premise that with it off
    nothing connects the shop draw to the crop choice. That premise is false: `STRAWBERRY_TILES_BY_
    DRAIN` caps strawberry on the draw and runs OUTSIDE `SHOP_ADAPT_CROPS`, and the tomato gate now
    reads the draw too. Two of the four crops are already wired.

    Carrot is the one that is not, and the reason is that no measured variable predicts it. Tomato
    was easy -- zero tiles below two draining shops. Carrot's nine games sit at drain counts
    1,1,1,2,2,2,3,3,3, evenly spread, and the five games with FOUR draining shops have none at all.
    Non-monotone, so drain count is the wrong variable, and demanding a gate before knowing what to
    gate on is how the milk line cost sixteen points on the herd side.

    What this test does assert: the non-monotonicity is real, so nobody fits a line to it. When a
    predictor is found this test should be replaced by one that asserts it.
    """
    by = collections.defaultdict(list)
    for _n, plants, shops in games:
        drain = sum(1 for s in shops if s in ("PET_CAFE", "FARMERS_MARKET"))
        by[drain].append(_mix(plants)["CARROT"])
    share = {k: sum(1 for t in v if t) / len(v) for k, v in by.items() if len(v) >= 5}
    assert len(share) >= 3, "too few populated drain buckets to judge monotonicity"
    keys = sorted(share)
    rising = all(share[a] <= share[b] for a, b in zip(keys, keys[1:]))
    assert not rising, (
        "carrot is now monotone in the drain count %s -- it has become fittable, so replace this "
        "test with the gate" % {k: round(share[k], 2) for k in keys})
