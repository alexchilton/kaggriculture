"""The cow/sheep cadence, checked against カワシギ's own recorded shop draws.

`test_the_herd_follows_the_wool_shop.py` drives `_herd_split` with hand-written shop lists. That
pins the mechanics and cannot say whether the rule is TRUE, because the input is invented. This
drives it with the `town.unlocked_shops` of every recorded game on disk and scores it against the
herd that seat actually finished with.

**It scores against the leader, not the field, and that distinction decides the test.** Measured
2026-08-13 over 451 recorded seats with a herd of 6+:

    population              early-yarn mean COW   COW <= 6   no-yarn mean COW
    whole field (451)                      7.26        41%               8.99
    top decile   (45)                      7.07        40%               9.40
    カワシギ      (67)                      6.00       100%               9.77

The field is bimodal at COW 6 and COW 8 even in its top decile, because it is a mix of players. He
is a step function. A rule fitted to the field's mean would be regression toward the players we beat
-- a drain-weighted linear fit was tried on that mean and rejected for exactly this reason. So these
tests assert HIS table, and the field is used only to show why it must not be the target.
"""
import collections
import json
import pathlib

import pytest

from kagg.search import schedule_agent as SA

#: Full recordings only. `field/` and `field_leaders/` hold the extracted `{team, actions}` form,
#: which has no observations and therefore no shop draw.
CORPUS = ("kawashigi", "top_guys", "top2", "ladder", "new_leader", "downloads_2026-08-13")
LEADER = "カワシギ"
#: Below this a seat never committed to an animal strategy and its split is noise, not a choice.
MIN_HERD = 6


def _seats():
    """(team, first-yarn draw index or None, cow, sheep) for every recorded seat with a herd."""
    out, seen = [], set()
    for folder in CORPUS:
        for path in sorted((pathlib.Path("data/seed_scripts") / folder).glob("*.json")):
            if path.name in seen:
                continue
            try:
                rec = json.loads(path.read_text())
            except Exception:
                continue
            steps = rec.get("steps") if isinstance(rec, dict) else None
            if not steps or len(steps) < 700:
                continue
            seen.add(path.name)
            obs = steps[-1][0].get("observation")
            if not isinstance(obs, dict):
                continue
            shops = (obs.get("town") or {}).get("unlocked_shops") or []
            first = next((i + 1 for i, s in enumerate(shops) if s == "YARN_STORE"), None)
            teams = (rec.get("info") or {}).get("TeamNames") or ["?", "?"]
            for seat in (0, 1):
                herd = collections.Counter()
                for row in obs["farms"][seat]["tiles"]:
                    for tile in row:
                        if isinstance(tile, dict) and tile.get("animal"):
                            herd[tile["animal"]] += 1
                if herd["COW"] + herd["SHEEP"] < MIN_HERD:
                    continue
                out.append((teams[seat], first, shops, herd["COW"], herd["SHEEP"]))
    return out


@pytest.fixture(scope="module")
def seats():
    rows = _seats()
    if len(rows) < 100:
        pytest.skip("recorded corpus not on disk (data/ is gitignored)")
    return rows


@pytest.fixture(scope="module")
def leader(seats):
    rows = [r for r in seats if r[0] == LEADER]
    if len(rows) < 40:
        pytest.skip("too few recorded %s seats" % LEADER)
    return rows


def _cow(shops, total=14, day=9, hour=0):
    """The rule's own cow count for a herd of `total`, decided on the draw `shops`."""
    return SA._herd_split({"COW": total, "SHEEP": 0}, {}, day, hour, list(shops))["COW"]


def test_the_leader_is_a_step_function_on_the_first_yarn_draw(leader):
    """The premise. If he stops being a step function, the rule is copying a habit he dropped."""
    early = [r for r in leader if r[1] is not None and r[1] <= SA.WOOL_SHOP_DRAW_LIMIT]
    late = [r for r in leader if r[1] is None or r[1] > SA.WOOL_SHOP_DRAW_LIMIT]
    assert len(early) >= 15 and len(late) >= 15
    assert all(r[3] == SA.WOOL_SHOP_COW_CAP for r in early), (
        "his early-yarn cow counts are %s, not all %d"
        % (sorted({r[3] for r in early}), SA.WOOL_SHOP_COW_CAP))
    assert min(r[3] for r in late) > SA.WOOL_SHOP_COW_CAP, (
        "a late-yarn seat came in at or under the cap: %s" % sorted({r[3] for r in late}))


def test_the_rule_reproduces_the_leaders_cow_count_on_his_own_draws(leader):
    """The whole point: replay his real draw, and our answer must be his answer.

    **Five of his 67 seats are unreachable by any constant and the test says so explicitly.** On a
    draw with no yarn store at all he runs COW 10 in 22 games and COW 8 in 5, so no single number
    can satisfy all 27 -- 62/67 is the ceiling for a rule of this shape, and `WOOL_SHOP_NO_YARN_COW`
    takes the mode. The assertion is that every remaining disagreement is one of those five, not
    that there are at most five: a new mismatch of a different shape must fail here even though it
    would keep the count inside the budget.
    """
    wrong = [(r[1], r[3], _cow(r[2])) for r in leader if _cow(r[2]) != r[3]]
    # **The no-yarn seats split BOTH ways and neither answer can win them all.** He runs COW 10 on
    # most no-yarn draws and COW 8 on a minority, and since 2026-08-15 `MILK_POOR_SHOP_COUNT` picks
    # COW 8 when the board also carries at most one MILK shop. That converts most of the old
    # mismatches into matches and creates one of the opposite shape: a seat with one milk shop where
    # he still ran COW 10. Measured on his 51 three-quadrant seats the exchange is worth
    # 49/51 = 96.1% exact on (COW, SHEEP) against 42/51 = 82.4% before -- see
    # `tests/test_the_herd_total_drops_on_an_early_wool_board.py` and
    # `data/logs/kawa_q3_rule_search.log`. Both directions are allowed here, and only on a no-yarn
    # draw; a mismatch of any other shape must still fail.
    unreachable = [w for w in wrong if w[0] is None and w[1] in (8, 10)]
    assert wrong == unreachable, (
        "%d of %d seats disagree in a way the no-yarn COW 8/10 minority does not explain "
        "(first-yarn-draw, his COW, our COW): %s"
        % (len(wrong), len(leader), [w for w in wrong if w not in unreachable][:8]))
    assert len(unreachable) <= 5, "the no-yarn minority has grown to %d" % len(unreachable)


def test_the_draw_limit_is_where_his_behaviour_actually_changes(leader):
    """`WOOL_SHOP_DRAW_LIMIT` is a measured boundary, not a tuned one.

    Slid one step either way it must misclassify him, or the number is arbitrary.
    """
    by_draw = collections.defaultdict(set)
    for _team, first, _shops, cow, _sheep in leader:
        by_draw[first].add(cow)
    assert by_draw.get(SA.WOOL_SHOP_DRAW_LIMIT) == {SA.WOOL_SHOP_COW_CAP}, (
        "draw #%d should still be capped, his counts there are %s"
        % (SA.WOOL_SHOP_DRAW_LIMIT, sorted(by_draw.get(SA.WOOL_SHOP_DRAW_LIMIT) or [])))
    beyond = by_draw.get(SA.WOOL_SHOP_DRAW_LIMIT + 1)
    if beyond:
        assert SA.WOOL_SHOP_COW_CAP not in beyond, (
            "draw #%d is NOT capped for him, his counts there are %s"
            % (SA.WOOL_SHOP_DRAW_LIMIT + 1, sorted(beyond)))


def test_the_field_average_is_not_the_target(seats, leader):
    """**Why this file scores the leader and not the corpus.**

    Kept as an executable statement of the trap: the field's early-yarn population is nowhere near
    the cap even in its top decile, so a rule fitted to its mean would abandon a classifier that is
    perfect on the player we are trying to beat.
    """
    field = [r for r in seats if r[0] != LEADER and r[1] is not None
             and r[1] <= SA.WOOL_SHOP_DRAW_LIMIT]
    assert len(field) >= 50
    at_cap = sum(1 for r in field if r[3] == SA.WOOL_SHOP_COW_CAP) / len(field)
    assert at_cap < 0.6, (
        "the field now agrees with the leader (%.0f%% at the cap) -- if this holds, fitting the "
        "field is no longer a trap and this file's premise should be revisited" % (100 * at_cap))


def test_the_split_never_invents_or_loses_an_animal(seats):
    """Whatever draw really occurred, the rule returns exactly the total it was handed."""
    for _team, _first, shops, cow, sheep in seats:
        total = cow + sheep
        split = SA._herd_split({"COW": total, "SHEEP": 0}, {}, 9, 0, list(shops))
        # **The total is now a CEILING, not an identity.** Until 2026-08-15 the rule could only
        # redistribute the schedule's count, so this asserted equality. On a board whose first
        # YARN_STORE lands in draws 1-3 the leader buys TWELVE animals on three quadrants, not
        # fourteen, and `HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE` now reproduces that. Buying
        # fewer needs no new pens, so it is expressible where raising the total is not.
        assert split["COW"] + split["SHEEP"] <= total, shops[:3]
        assert split["COW"] >= 0 and split["SHEEP"] >= 0, shops[:3]


def test_the_total_is_the_part_the_split_rule_cannot_reach(leader):
    """**A measured record of the remaining gap, not a bug in the split.**

    His herd TOTAL moves with the draw too -- and the comment above `WOOL_SHOP_SETS_THE_HERD` has
    the size of it wrong. It claims SHEEP 12 / total 18 on draws #1-#2; measured over all 67 of his
    seats it is SHEEP 9.1-9.3 / total ~15, and draw #3 is total 12, not 14. `_herd_split` may only
    redistribute the count the schedule fixed, so it cannot close this either way. `xfail(strict)`
    so that a schedule change which does close it fails here loudly instead of passing unnoticed.
    """
    early = [r for r in leader if r[1] is not None and r[1] <= 2]
    assert len(early) >= 15
    mean_total = sum(r[3] + r[4] for r in early) / len(early)
    assert abs(mean_total - 14) < 0.5, (
        "on draws #1-#2 he runs a herd of %.2f, the schedule fixes 14" % mean_total)


test_the_total_is_the_part_the_split_rule_cannot_reach = pytest.mark.xfail(
    strict=True, reason="measured: he runs ~15 on an early yarn draw, the schedule fixes 14"
)(test_the_total_is_the_part_the_split_rule_cannot_reach)
