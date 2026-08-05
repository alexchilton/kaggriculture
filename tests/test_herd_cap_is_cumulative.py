"""`plan.herd` must cap animals *bought over the season*, not animals *currently standing*.

`executor.py:571-577` sizes each species' order as::

    placed = (view.animal == a).sum(axis=1) + view.shed_animals[:, a]
    room   = min(max(plan.herd[:, a] - placed, 0), housing)

`placed` counts animals on a tile or in the shed. An animal that starved and escaped
(`consecutive_unfed >= 2`, `jax_sim.py:1057`) is in neither, so the cap silently re-opens and the
executor buys a replacement -- at full price, with the same feed shortfall waiting for it.

Measured 2026-08-04 running `P.leaders_genome()` against `library.opposition()`, seed 0
(`data/logs/diag_leaders_recheck.log`)::

    herd target [GOOSE 0, COW 8, SHEEP 6] = 14
    ordered      GOOSE 0, COW 16, SHEEP 5 = 21
    final bank $0 in all three games, against $37,083 / $7,019 / $2,998

Exactly 2x the COW target. The live-herd trace shows the mechanism: 0 alive on days 0/5/10, 3 alive
on day 15, 0.7 on day 20, 0 on day 25 -- a buy/starve/re-buy cycle that converts the entire $3,000
stake into escaped livestock and leaves nothing for the crop economy.

**Why this is the gate rather than the $0 bank.** A bank assertion would pass the moment anything
improved the season, without the cap ever being fixed. This asserts the specific invariant, so it
cannot be satisfied by an unrelated gain. Note also that the existing suite already gates feed
*per decision* (`test_executor_animals.py:162`, `test_feed_before_herd.py`) -- what nothing checked
until now is the cumulative total across a season, which is where a per-turn-legal rule goes wrong.
"""

import numpy as np
import pytest

from kagg.search import executor as X
from kagg.search import library, rollout
from kagg.search import plan as P
from kagg.sim.game import Actions, Game

# SKIPPED, deliberately and with the reason stated, rather than deleted: the code it
# covers still exists and may be revived. A silently green suite would be worse than a red one.
pytestmark = pytest.mark.skip(reason=(
    "tests the superseded plan/executor architecture (plan, library, rollout, executor). The live path is routines.py -> chains.py and imports none of it. See docs/executor_livestock_broken_2026-08-04.md."))

SEED = 0
WEED_CHANCE = 0.005
DAYS = 30


def _season(genome, opponents):
    """Play a full season and return (cumulative buy_animal [B, N_ANIMALS], plan, final money)."""
    rng = np.random.default_rng(SEED)
    schedule = rollout.sample_unlock_schedule(rng)
    batch = opponents.shape[0]
    mine = P.decode(np.repeat(genome[None, :], batch, axis=0))
    theirs = P.decode(opponents)

    game = Game(batch, weed_chance=WEED_CHANCE, rng=np.random.default_rng(SEED),
                unlock_schedule=schedule)
    actions = Actions(batch)
    ordered = np.zeros((batch, P.N_ANIMALS), dtype=np.int64)

    for step in range(DAYS * 24 - 1):
        day, hour = step // 24, step % 24
        for player in (0, 1):
            view = rollout.build_view(game, player, day, hour)
            decision = X.decide(view, (mine, theirs)[player])
            if player == 0:
                ordered += decision.buy_animal
            rollout._write(actions, player, decision)
        if game.step(actions):
            break
    return ordered, mine, game.money()


def test_the_season_never_buys_more_animals_than_the_plan_asked_for():
    """**The claim.** A herd target of 8 cows means 8 cows bought, not 8 cows standing at any moment."""
    ordered, plan, _money = _season(P.leaders_genome(), library.opposition())

    target = plan.herd[0]
    worst = (ordered - target[None, :]).max()
    assert worst <= 0, (
        "bought more animals than the plan's herd target, so escapes are being silently replaced:\n"
        + "\n".join(
            f"  {name}: ordered {ordered[:, a].tolist()} against a target of {int(target[a])}"
            for a, name in enumerate(P.ANIMAL_NAMES) if (ordered[:, a] > target[a]).any()))


def test_the_fixture_actually_asks_for_animals():
    """Anti-vacuity: a plan with a zero herd would pass the test above without exercising the cap."""
    plan = P.decode(P.leaders_genome()[None, :])
    assert int(plan.herd[0].sum()) > 0, "leaders_genome no longer stocks a herd -- fixture is stale"
    assert int(plan.feed_wheat[0]) > 0, "feed_wheat is 0, which disables livestock entirely"


@pytest.mark.slow
def test_animals_bought_are_still_alive_at_the_end_of_the_season():
    """The cap alone is not the goal: a herd bought once and starved once is equally worthless.

    Kept separate from the cap test so a fix to one cannot be credited to the other. This is the
    weaker statement deliberately -- it asks only that *some* of the herd survives, because the
    exact survival rate depends on feed economics this test is not trying to pin.
    """
    ordered, plan, _money = _season(P.leaders_genome(), library.opposition())
    assert ordered.sum() > 0, "no animals ordered at all -- nothing to survive"

    rng = np.random.default_rng(SEED)
    schedule = rollout.sample_unlock_schedule(rng)
    batch = library.opposition().shape[0]
    mine = P.decode(np.repeat(P.leaders_genome()[None, :], batch, axis=0))
    theirs = P.decode(library.opposition())
    game = Game(batch, weed_chance=WEED_CHANCE, rng=np.random.default_rng(SEED),
                unlock_schedule=schedule)
    actions = Actions(batch)
    for step in range(DAYS * 24 - 1):
        day, hour = step // 24, step % 24
        for player in (0, 1):
            view = rollout.build_view(game, player, day, hour)
            rollout._write(actions, player, X.decide(view, (mine, theirs)[player]))
        if game.step(actions):
            break

    alive = (game.tiles[0].animal >= 0).sum(axis=1)
    assert alive.max() > 0, (
        f"every animal died: ordered {ordered.sum(axis=1).tolist()} across the season and finished "
        f"with {alive.tolist()} standing")
