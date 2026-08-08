"""`DRAIN_UNITS` is a copy of a measurement, and nothing checked it against the source.

The planner sizes every chain against `kagg.search.chains.DRAIN_UNITS` -- the number of units the
town removes from the book over a season, i.e. how much can be sold before the price collapses. It
has to be a hard-coded table, because the planner runs before an episode exists.

It was measured on `kaggle-environments` 1.32.2 and the competition moved to 1.32.6, which doubled
`townCenterSellInterval` from 12 to 24 and deleted the day-10/day-20 demand ramp. Nothing went red,
because no test compared the table to the environment. These do.

Melon is the sharp case and is exact: no shop carries it, so its only drain is the town centre, and
the season total is a constant with zero variance across seeds. Everything else depends on the shop
unlock draw -- 1.32.6 draws **with replacement**, so a product served by a repeated shop drains
twice as fast -- which makes each of those a distribution. The table stores the mean over a pinned
seed range, so the check here recomputes over that same range and demands an exact match.
"""

import pytest

from kagg.economics import market as M
from kagg.search import chains as C

#: The seed range `scripts/drain_table.py` uses. Pinned so the expected value is reproducible;
#: widening it changes the mean and is a deliberate re-baseline, not a free choice.
SEEDS = range(1000, 1032)


def season_drain(seed):
    return {k: sum(v) for k, v in M.drain_per_day(M.observe_unlocks(seed)).items()}


@pytest.mark.parametrize("seed", [1000, 1007, 1019, 1031])
def test_melon_absorbs_exactly_thirty_units_a_season_on_every_seed(seed):
    """No shop carries MELON, so its drain is the town centre alone and does not vary.

    719 playable steps at one tick every 24 turns is 30 ticks, one unit each. The 140 that
    `DRAIN_UNITS` held is 60 ticks at the old 12-turn interval, ramped x2 from day 10 and x4 from
    day 20 -- three separate 1.32.2 facts compounding, which is why this row was the furthest out.
    """
    assert season_drain(seed)["MELON"] == 30


def test_melon_in_the_table_matches_what_the_town_actually_absorbs():
    """The row the planner reads, against the row the environment produces.

    Kept separate from the parametrised check above so a failure says which of the two is wrong:
    the environment moved, or the copy of it did.
    """
    assert C.DRAIN_UNITS["MELON"] == 30, (
        f"the planner sizes melon against {C.DRAIN_UNITS['MELON']} units a season and the town "
        "absorbs 30. Every melon above the 30th is sold into a book that never recovers, because "
        "no shop carries melon and the town centre is its only buyer."
    )


@pytest.mark.slow
def test_the_whole_table_matches_the_environment_over_the_pinned_seeds():
    """Every product, against the mean of the same seed range `scripts/drain_table.py` reports.

    Exact rather than tolerant on purpose. A tolerance band is what let a 4.67x error sit unnoticed;
    if this needs re-baselining, `scripts/drain_table.py` prints the replacement table.
    """
    measured = [season_drain(s) for s in SEEDS]
    expected = {item: round(sum(d[item] for d in measured) / len(measured))
                for item in C.DRAIN_UNITS}
    assert C.DRAIN_UNITS == expected, (
        "DRAIN_UNITS has drifted from the environment. Regenerate with "
        "`PYTHONPATH=. python3 -u scripts/drain_table.py --seeds 32`.\n"
        + "\n".join(f"  {k:<12} table {C.DRAIN_UNITS[k]:>5}   env {expected[k]:>5}"
                    for k in sorted(expected) if C.DRAIN_UNITS[k] != expected[k])
    )
