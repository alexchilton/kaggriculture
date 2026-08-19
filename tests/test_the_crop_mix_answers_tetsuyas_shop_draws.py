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


def test_the_tomato_constant_does_not_fire_on_every_board(games):
    """**`WHEAT_TILES_TO_TOMATO` is a constant standing in for a response.**

    It converts wheat tiles to tomato on EVERY board, unconditionally, at a fixed count. He plants
    tomato in 4 of 78 games and when he does he plants 8-22 tiles of it. So the constant is wrong in
    both directions at once: it fires roughly twenty times too often, and at a fraction of the size.

    RED as written on 2026-08-19 with `WHEAT_TILES_TO_TOMATO = 1`. Passing means the tomato decision
    has been made conditional on something -- the draw, the board, anything measured -- rather than
    pinned.
    """
    with_tom = [(_mix(p)["TOMATO"]) for _n, p, _s in games if _mix(p)["TOMATO"]]
    assert with_tom, "no tomato in the corpus; re-measure before asserting"
    share = len(with_tom) / len(games)
    fires_always = bool(SA.WHEAT_TILES_TO_TOMATO)
    assert not (fires_always and share < 0.5), (
        "WHEAT_TILES_TO_TOMATO = %r converts wheat on every board, but he plants tomato in "
        "%d of %d games (%.0f%%) and sows %d-%d tiles when he does"
        % (SA.WHEAT_TILES_TO_TOMATO, len(with_tom), len(games), 100 * share,
           min(with_tom), max(with_tom)))


def test_the_crop_choice_is_wired_to_the_shop_draw_at_all(games):
    """`SHOP_ADAPT_CROPS` is the only path by which a shop draw can reach the crop choice.

    With it off, every crop decision is a constant read off one extracted schedule, and no amount of
    tuning those constants can track a player whose carrot swings 0-65 tiles with the board.

    RED as written on 2026-08-19: `SHOP_ADAPT_CROPS = False`.
    """
    carrots = [_mix(p)["CARROT"] for _n, p, _s in games]
    assert max(carrots) - min(carrots) > 20, "his carrot no longer moves with the board"
    assert SA.SHOP_ADAPT_CROPS, (
        "SHOP_ADAPT_CROPS is off, so nothing connects the draw to the crop choice, while his "
        "carrot ranges %d-%d tiles across the corpus" % (min(carrots), max(carrots)))
