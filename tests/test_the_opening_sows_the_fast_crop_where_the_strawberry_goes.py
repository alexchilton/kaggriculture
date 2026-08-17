"""The d1 sowing puts WHEAT on the three squares d6's strawberry needs, and MELON on his three.

Measured 2026-08-17, seed 11, both three-quadrant tapes. Our d1 and his d1 sow the same COUNTS -- 12
melon and 7 wheat -- and differ only in which square gets which, on six tiles:

    we sow MELON, he sows WHEAT    (0,0)  (1,1)  (3,0)
    we sow WHEAT, he sows MELON    (3,2)  (2,3)  (0,4)

The reason it is not cosmetic: wheat sown on d1 is ripe and cleared by d5, which is what frees the
square for his d6 strawberry. Melon sown on d1 stands to about d10 and `PLANT` onto an occupied tile
is refused outright, so the square is lost for the rest of the season. Replaying his own d5-d11
actions against our board, the only failures were exactly these tiles -- his d5 h14 strawberry on
(0,0) and (1,1), and his d8 harvest-then-wheat on (3,0) -- and they account for the whole `strawb -2`
and `melon +3` that the replay could not close. See
`docs/replay_window_cannot_converge_2026-08-17.md`.

The cause is the sweep: crops are seated in `router.field_order` blocks, so melon claims the first
squares and wheat the remainder. He interleaves.
"""
import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
SEED = 11
#: Tile -> the crop his d1 sows there. A permutation of our own d1 multiset, so asserting it cannot
#: be satisfied by planting more of anything.
HIS_D1 = {(0, 0): "WHEAT", (1, 1): "WHEAT", (3, 0): "WHEAT",
          (3, 2): "MELON", (2, 3): "MELON", (0, 4): "MELON"}


@pytest.fixture(scope="module")
def d1_board():
    """Our own dawn-of-d1 board on seed 11, no replay, no handover."""
    pytest.importorskip("kaggle_environments")
    import sys
    sys.path.insert(0, str(REPO / "scripts"))
    import breakdown as B

    from kagg.search import schedule_agent
    B.schedule_agent = schedule_agent
    schedule_agent.REPLAY_OPENING_DAYS = ()

    replay, schedule, team = B.TAPES["kawashigi"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    seen = {}

    def mine():
        a = schedule_agent.make_agent(thin, 0, router=True)

        def f(obs, t=None):
            if int(obs.get("day", 0) or 0) == 1 and int(obs.get("hour", 0) or 0) == 0:
                seen["tiles"] = ((obs.get("farms") or [{}])[0] or {}).get("tiles") or []
            return a(obs)
        return f

    B.run(mine, lambda: B.tape_policy(replay, team, 1), SEED, 0.0, stop_day=2,
          economy=B.env_config(replay), shops=B.recorded_shops(replay))
    return seen["tiles"]


def _crop(tiles, x, y):
    c = tiles[y][x] if y < len(tiles) and x < len(tiles[y]) else None
    return (c if isinstance(c, dict) else {}).get("crop")


def test_the_opening_sows_the_fast_crop_where_the_strawberry_goes(d1_board):
    """(0,0), (1,1) and (3,0) carry WHEAT at dawn on d1, so d5 can clear them."""
    got = {t: _crop(d1_board, *t) for t, c in HIS_D1.items() if c == "WHEAT"}
    assert got == {t: "WHEAT" for t in got}, got


def test_the_opening_keeps_the_slow_crop_on_the_squares_he_keeps_it_on(d1_board):
    """The other half of the swap. Without it the wheat above is bought by planting less melon."""
    got = {t: _crop(d1_board, *t) for t, c in HIS_D1.items() if c == "MELON"}
    assert got == {t: "MELON" for t in got}, got


def test_the_opening_sows_the_same_counts_it_did_before(d1_board):
    """12 melon and 7 wheat on d1. The fix is a permutation; a count change is a different change."""
    counts = {}
    for row in d1_board:
        for c in row:
            if isinstance(c, dict) and c.get("crop"):
                counts[c["crop"]] = counts.get(c["crop"], 0) + 1
    assert counts.get("MELON") == 12, counts
    assert counts.get("WHEAT") == 7, counts
