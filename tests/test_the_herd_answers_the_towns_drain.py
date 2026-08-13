"""The herd must answer how much the town actually drains, not just which species.

Four separate defects, one per test, all measured on the five ladder games downloaded 2026-08-13
(`docs/market_depth_and_the_morning_losses_2026-08-13.md`):

1. `_herd_split` may only redistribute `want_total`, so a town draining 1,074 wool gets the same
   fourteen animals as one draining 228. In `92550780` the town drew YARN_STORE three times, wool
   closed at $252 -- ABOVE its $200 base, i.e. undersupplied all season -- and we ran 8 sheep.
2. The wool branch `return`s before the drain-aware greedy, so the one allocator that counts shop
   INSTANCES is bypassed in exactly the games where the drain is extreme.
3. The branch is guarded by `split["COW"] <= WOOL_SHOP_COW_CAP`, and the schedule buys 8 cows by
   day 8. Draw #3 lands on day 9, so the guard can never pass -- `WOOL_SHOP_DRAW_LIMIT = 3` is dead
   as written. Verified across five games: the rule fired at draw #1 and #2 and at no other.
4. Day 0 commits COW 1 + SHEEP 4 before the first draw exists (day 3). Blind, MILK is carried by
   three of the eight shops and WOOL by one, so the uninformed buy should favour COW, not four SHEEP.
"""

import pytest

from kagg.search import schedule_agent_1455mh as SA


YARN_EARLY = ["YARN_STORE", "SMOOTHIE_SHOP", "BAKERY"]          # 92550780: draw #1
YARN_LATE = ["BRUNCH_SPOT", "ICE_CREAM_SHOP", "YARN_STORE"]     # 92562037: draw #3
NO_YARN = ["ICE_CREAM_SHOP", "BAKERY", "FARMERS_MARKET"]        # 92565805: none all season


def _total(split):
    return split["COW"] + split["SHEEP"]


def test_a_town_draining_three_yarn_stores_gets_more_animals_than_the_schedule_asked_for():
    """Defect 1. The schedule's count is a starting point, not a ceiling, when the drain says so."""
    want = {"COW": 6, "SHEEP": 8}
    split = SA._herd_split(want, {"COW": 6, "SHEEP": 4}, day=9, hour=0,
                           unlocked_shops=["YARN_STORE", "YARN_STORE", "YARN_STORE"])
    assert _total(split) > 14, (
        "three yarn stores drain 1,074 wool a season and eight sheep make about 100; "
        "the herd must be allowed to grow past the schedule's 14, got %r" % (split,))
    assert split["SHEEP"] > 8, "the growth must go to the species the town is draining: %r" % (split,)


def test_the_wool_branch_does_not_skip_the_drain_aware_greedy():
    """Defect 2. The wool branch used to `return`, so the headroom greedy never ran behind it.

    The observable consequence is the SPECIES the growth goes to. A town draining wool must add
    sheep; a town that drew no yarn store at all must not, because its wool book is empty -- in
    `92565805` wool drained 0 units and closed at the $1 floor. Under the old early `return` both
    towns produced the identical herd, because the only allocator that reads the drain was skipped.

    This is asserted on species rather than on total because the total is bounded by
    `HERD_GROWTH_CAP`, which is set by the feed bill and binds first in both towns.
    """
    want = {"COW": 6, "SHEEP": 8}
    wool = SA._herd_split(want, {"COW": 6, "SHEEP": 4}, day=9, hour=0,
                          unlocked_shops=["YARN_STORE", "YARN_STORE", "YARN_STORE"])
    dry = SA._herd_split(want, {"COW": 6, "SHEEP": 4}, day=9, hour=0, unlocked_shops=NO_YARN)
    assert wool["SHEEP"] > dry["SHEEP"], (
        "a three-yarn town drains 1,074 wool and a no-yarn town drains none; the herd must not be "
        "the same in both; got wool=%r dry=%r" % (wool, dry))


def test_the_wool_rule_still_steers_the_remaining_budget_once_the_cows_are_bought():
    """Defect 3. Eight cows are bought by day 8; draw #3 arrives on day 9 and must still bind.

    This one is a REGRESSION GUARD, not a red test: the wool branch's `split["COW"] <= 6` guard
    cannot pass once eight cows exist, but the drain-aware greedy below it already sends the
    remaining budget to sheep, so the behaviour is right today by a different route. The test exists
    so that route cannot be removed by accident.
    """
    want = {"COW": 10, "SHEEP": 4}
    split = SA._herd_split(want, {"COW": 8, "SHEEP": 4}, day=9, hour=0, unlocked_shops=YARN_LATE)
    assert split["COW"] == 8, "a bought cow can never be un-bought: %r" % (split,)
    assert split["SHEEP"] > 4, (
        "a yarn store inside the draw limit must send every REMAINING animal to sheep even when the "
        "cows already exceed WOOL_SHOP_COW_CAP; got %r" % (split,))


def test_the_blind_opening_buy_is_decided_at_all():
    """Defect 4, and it is a GATE, not a bug inside the split.

    `_herd_split` already gets day 0 right on its own -- the schedule's row is `COW 1 + SHEEP 4`,
    and the floors alone turn that into `COW 4 + SHEEP 1`, which is the direction the expectation
    wants (MILK is carried by three of the eight shops, WOOL by one). The problem is that the caller
    never asks: `if SHOP_ADAPT_HERD and day >= SHOP_ADAPT_FROM_DAY`, with the constant at 3.

    So five animals -- the single largest uninformed commitment of the season -- are bought on the
    tape's mix, and in `92565805` that meant four sheep in a town that drew no yarn store at all and
    closed wool at the $1 floor.
    """
    assert SA.SHOP_ADAPT_FROM_DAY <= 0, (
        "the day-0 row is bought before any shop exists; the split must be consulted for it, "
        "got SHOP_ADAPT_FROM_DAY = %r" % (SA.SHOP_ADAPT_FROM_DAY,))
    split = SA._herd_split({"COW": 1, "SHEEP": 4}, {}, day=0, hour=0, unlocked_shops=[])
    assert split["COW"] > split["SHEEP"], (
        "with no shops drawn, the expectation favours milk (3 of 8 shops) over wool (1 of 8); "
        "got %r" % (split,))


def test_growth_stops_when_a_new_animal_cannot_reach_its_first_yield():
    """The guard on defect 1: a sheep bought on day 27 yields nothing and must not be bought."""
    want = {"COW": 6, "SHEEP": 8}
    split = SA._herd_split(want, {"COW": 6, "SHEEP": 8}, day=27, hour=0,
                           unlocked_shops=["YARN_STORE", "YARN_STORE", "YARN_STORE"])
    assert _total(split) == 14, (
        "a SHEEP bought on day 27 first yields on day 33, past the end of the season; "
        "the herd must not grow, got %r" % (split,))
