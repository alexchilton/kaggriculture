"""The animal block is a step, and the step bankrupts the plan on day 0.

Alex's test design, and it localised the fault where three abstract "the representation cannot express
X" tests would not have: encode the $132,245 seat's own layout, play it, and diff our per-day curves
against the seat's measured ones (`scripts/diverge_by_day.py`,
`data/logs/diverge_by_day.log`). Hiring, pens and land all track the measurement. One row does not:

    day |  OURS money crew live  wheat escaped | THEIRS crew live
      0 |         253    5    2      0       0 |           4    2
     14 |          31   13   16      0       3 |          12   25
     29 |           0    1    0      0      19 |          13   28

Day 0 spends $2,747 of the $3,000 stake on five animals against the seat's two. Everything after is
downstream: no cash for wheat, so `wheat` is 0 all season, so FEED never fires, so 19 animals escape
at full purchase price, so the crew cannot be paid from day 15, so $0.

The cause is that `herd` is one target per species and `stock_day` is one day, which decodes to
"acquire up to the target as fast as cash and pens allow, from that day". The seat holds 4 animals
for eleven days while cash builds and then jumps to 17 on the day land and crew arrive. That ramp is
not a refinement of the plan, it *is* the cash-flow plan, and no assignment of the two genes says it.

`plan.py:289-293` already anticipated the symptom -- "a big herd on a small stake starves ... the
search will find that". It cannot: `docs/fable_herd_cap_and_retraction_2026-08-04.md` shows CEM is a
product-of-marginals model, so a pasture tile only pays when it co-occurs with a matching herd,
stock day and feed reserve, and the marginal for PASTURE gets pushed *down* by every sample that
draws the tile without the rest. Starving is not a point the search prices correctly; it is a point
the search is driven away from for the wrong reason.
"""

import itertools

import numpy as np
import pytest

from kagg.search import library, plan as P, replay_plan as RP, rollout

EPISODE = "data/89113699.json"
SEAT = 1


@pytest.fixture(scope="module")
def layout():
    return RP.layout_from_replay(EPISODE, seat=SEAT)


def _plateaus(curve, min_days=3):
    """Runs of >= `min_days` consecutive days at the same positive headcount, as (level, length)."""
    out = []
    for level, group in itertools.groupby(curve):
        n = len(list(group))
        if level > 0 and n >= min_days:
            out.append((level, n))
    return out


def test_the_measured_ramp_has_two_plateaus_so_one_target_cannot_say_it(layout):
    """A representation claim, checked against the measurement rather than asserted.

    Decoding `(herd, stock_day)` yields a single non-decreasing approach to a single target, so the
    headcount it describes has exactly one sustained positive level. The seat has two, an order of
    magnitude apart. Two levels need two (level, day) pairs; the genome has one.
    """
    levels = _plateaus(layout.animals_by_day)
    assert len(levels) >= 2, (
        f"expected the measured curve to hold at two different headcounts, got {levels}")
    low, high = min(l for l, _ in levels), max(l for l, _ in levels)
    assert high >= 4 * low, (
        f"the two plateaus must be far enough apart that no single target covers both: "
        f"{low} then {high}")

    # And the low plateau is early, the high one late -- it is a ramp, not noise around one target.
    first_high = next(d for d, n in enumerate(layout.animals_by_day) if n >= high * 0.8)
    assert first_high >= 8, f"the jump to {high} happens on day {first_high}, not at the start"


def test_encoding_the_winner_stays_solvent_and_keeps_its_animals(layout):
    """What we require, not what currently happens. Fails today; the fix is what makes it pass.

    Playing the $132,245 seat's own layout must not go bankrupt. Selection is on win rate elsewhere;
    this asserts on money and on escapes deliberately, because the failure being fixed is insolvency
    and the loss of paid-for animals, and those are the quantities that say so.

    Current measured behaviour, for the record (`data/logs/diverge_by_day.log`): day 0 ends on $253
    against the stake of $3,000, no wheat is ever affordable, 19 animals escape, season ends on $0.
    """
    genome = RP.genome_from_layout(layout)
    mine = P.decode(genome[None])
    opp = P.decode(library.opposition()).take([0])
    schedule = rollout.sample_unlock_schedule(np.random.default_rng(0))
    rows = _trace(mine, opp, schedule)

    day0 = rows[0]
    assert day0["money"] >= 1000, (
        f"day 0 ends on ${day0['money']:,.0f} of the $3,000 stake -- stocking must not spend the "
        f"working capital the wheat-into-milk conversion runs on. The seat itself held 2 animals on "
        f"day 0 and 4 for the following ten days.")

    # An animal bought and then starved is a pure loss of its purchase price, so the plan must not
    # own more animals than the crew can feed.
    assert rows[-1]["escaped"] <= 2, (
        f"{rows[-1]['escaped']} animals escaped; each cost its full purchase price. An animal is "
        f"only worth buying if there is feed and a hand to deliver it.")
    assert max(r["wheat"] for r in rows) >= 20, "feed must be affordable at some point in the season"
    assert rows[-1]["money"] > 3000, (
        f"the season ends on ${rows[-1]['money']:,.0f}, below the opening stake")


def _trace(mine, opp, schedule):
    """Per-day rows for the seat under test, sampled mid-day.

    Mid-day, not at hour 23: the dawn reset dismisses every hand inside the hour-23 step, so a row
    taken after it reports a crew of 1 every day whatever the hire gene says. Sampling there once
    produced a confident and wrong "hiring is inert" reading.
    """
    from kagg.search import executor as X
    from kagg.sim.game import Actions, Game
    from kagg.sim.tiles import COOP, PASTURE

    game = Game(1, rng=np.random.default_rng(0), unlock_schedule=schedule)
    actions = Actions(1)
    rows, prev_live, escaped = [], 0, 0
    for step in range(719):
        day, hour = step // 24, step % 24
        for player, pl in ((0, mine), (1, opp)):
            rollout._write(actions, player, X.decide(rollout.build_view(game, player, day, hour), pl))
        if game.step(actions):
            break
        if hour == 12:
            tiles, farm = game.tiles[0], game.farms[0]
            live = int((tiles.animal[0] >= 0).sum())
            if live < prev_live:
                escaped += prev_live - live
            prev_live = live
            rows.append({
                "day": day, "money": float(farm.money[0]), "live": live,
                "pens": int(((tiles.kind[0] == PASTURE) | (tiles.kind[0] == COOP)).sum()),
                "wheat": int(farm.shed[0, X.WHEAT_ITEM]),
                "shed_animals": int(farm.shed[0, X.ANIMAL_ITEM_BASE:].sum()),
                "escaped": escaped,
            })
    return rows
