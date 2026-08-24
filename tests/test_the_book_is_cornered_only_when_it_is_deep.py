"""The cornering decision must fire on the town that beat us and stand down on the thin ones.

This is a behavioural test against SIX REAL LADDER OBSERVATIONS, not synthetic boards, because the
rule it replaces was shipped on a pool that could not produce the situation at all.

    game       town drain  opponent carrot  close price   what happened
    98495047       11           10 tiles        $498      lost by $29,384 -- they took 76 units
    98460892        6            2 tiles        $124      lost by $614
    98494953        2            0 tiles         $59      lost by $3,472, nothing to do with carrot
    98499540        2            0 tiles         $52      lost by $1,940
    98501831        2            0 tiles         $54      lost by $6,070
    98428765        3            0 tiles         $50      lost by $1,783

`CARROT_DRAIN_MIN = 5` gets these right. `CARROT_OPP_MAX = 7` is what stood us down on 98495047 --
the only one of the six where the book was worth taking -- because the opponent held 10 tiles. Their
carrot was read as "the book is taken" when at drain 11 it meant "the book is rich".

So the discriminating case is exactly one game, and any rule that cannot fire on it while refusing
the other five is not worth shipping.
"""

import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "reference"))

from kagg.search import corner_the_book as C                                # noqa: E402

TPD = 24
US = "alex chilton"

#: `(episode, town carrot drain, should we corner it)`. The verdicts are read off the outcome:
#: 98495047 closed at $498 with 76 units cleared into it, so the book was there to be taken.
GAMES = [
    ("98495047", 11, True),
    ("98460892", 6, True),
    ("98494953", 2, False),
    ("98499540", 2, False),
    ("98501831", 2, False),
    ("98428765", 3, False),
]


def _shops():
    import kaggriculture as KG                                              # noqa: PLC0415
    return KG.SHOPS


def _obs(episode, day=25):
    """Our seat's own observation at dawn on `day`, from the recorded game."""
    hits = list((REPO / "data/seed_scripts").rglob(f"{episode}.json"))
    if not hits:
        pytest.skip(f"{episode}.json not downloaded")
    rec = json.loads(hits[0].read_text())
    names = rec["info"]["TeamNames"]
    if US not in names:
        pytest.skip(f"{episode} is not one of ours")
    seat = names.index(US)
    return rec["steps"][day * TPD][seat]["observation"], seat


@pytest.mark.parametrize("episode,drain,should_fire", GAMES)
def test_it_fires_only_where_the_book_is_deep(episode, drain, should_fire):
    obs, seat = _obs(episode)
    tiles, why = C.plan(obs, _shops(), me=seat, product="CARROT")
    if should_fire:
        assert tiles > 0, f"{episode} (drain {drain}) should corner but stood down: {why}"
    else:
        assert tiles == 0, f"{episode} (drain {drain}) should stand down but wants {tiles}: {why}"


def test_the_opponents_carrot_does_not_veto_a_deep_book():
    """The exact inversion of `CARROT_OPP_MAX`, on the game it cost us.

    Their 10 tiles at d25 tripped the old gate. Here they are subtracted as supply and the book is
    still deep enough, which is the whole behavioural difference between the two rules.
    """
    obs, seat = _obs("98495047")
    theirs = C.opponent_units(obs, "CARROT", seat)
    assert theirs > 0, "this game is the test fixture precisely because they hold carrot"
    tiles, why = C.plan(obs, _shops(), me=seat, product="CARROT")
    assert tiles > 0, f"stood down with {theirs} opponent units in a drain-11 town: {why}"


def test_the_price_curve_matches_the_town_that_beat_us():
    """Our inverted curve must agree with what the env actually quoted.

    d25 of 98495047: inventory 9261, so deficit 739, and the tape recorded $208.
    """
    obs, _ = _obs("98495047")
    d = C.deficit_now(obs, "CARROT")
    quoted = ((obs.get("market") or {}).get("prices") or {}).get("CARROT")
    assert d == 739, f"deficit read {d}, expected 739"
    assert C.price_at("CARROT", d) == pytest.approx(quoted, rel=0.02), (
        f"our curve says {C.price_at('CARROT', d):.0f}, the town quoted {quoted}")


def test_it_will_not_sell_itself_past_the_knee():
    """Sizing must leave the book above `T` after our own dump lands."""
    obs, seat = _obs("98495047")
    tiles, _ = C.plan(obs, _shops(), me=seat, product="CARROT")
    projected = (C.deficit_now(obs, "CARROT")
                 + C.drain_per_day(obs, "CARROT", _shops()) * (C.RELEASE_DAY - 25)
                 - C.opponent_units(obs, "CARROT", seat))
    after = projected - tiles * C.YIELD_PER_TILE["CARROT"]
    assert after >= C.HINGE["CARROT"][1], (
        f"{tiles} tiles takes the deficit to {after:.0f}, under the knee at "
        f"{C.HINGE['CARROT'][1]:.0f} -- that is selling into our own collapse")
