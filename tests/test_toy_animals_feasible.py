"""The toy's animal economy must be *runnable* without the macro, because in the real game it is.

**The theory this pins, stated before the fix.** `kagg/rl/toy_animals.py` was built to settle whether
the policy's refusal to touch livestock is a credit-distance problem (the *head*: buying an animal
costs money now and pays 100+ turns later) or an exploration problem (the *tail*: the FEED
conjunction is too improbable to stumble into). It offers two switches for exactly that --
`start_animal` removes the head, `tend` collapses the tail into one action.

It cannot answer the question as written, because **it makes the tail arithmetically impossible**.

`UNFED_ESCAPE = 2` with `unfed` incremented once per `step`, so a feed is due every 2 *turns*. A feed
without `tend` costs two actions, GET_WHEAT then FEED (`jax_masks.py:96`: `has_animal & ~fed &
carrying_wheat`). Two actions every two turns is the entire turn budget, leaving zero turns for
COLLECT. So no animal can ever be collected from unless `tend` is on, and `animal_upside()` quietly
assumes it -- it counts 28 collections plus 30 feeds in a 60-turn season, 58 actions, which only fits
if a feed is one action.

**The real rule is per DAY, not per turn.** `jax_sim.py:1147-1159` increments `consecutive_unfed` in
the nightly production pass and escapes at `>= 2`, and `TURNS_PER_DAY` is 24. So the real game gives
~48 turns to land two feeds, not 2. The toy overstates the cost of keeping an animal alive by more
than an order of magnitude.

**Why that matters more than a wrong constant.** An experiment run on this toy would have reported
that the macro is necessary -- with no arm able to show otherwise -- and that finding would have been
a restatement of the calibration, not a result. `CLAUDE.md`: *"Evaluate a technique against the
problem it was BUILT for"*, and *"a gate only tests what it cannot reach."* This one cannot reach the
arm it exists to test.
"""

import pytest

from kagg.rl import toy_animals as TA


def _feed_actions_per_cycle(tend):
    """Actions needed to keep one animal alive for one feed cycle."""
    return 1 if tend else 2                      # TEND, or GET_WHEAT + FEED


def test_the_real_game_gives_a_whole_day_between_feeds():
    """`consecutive_unfed` ticks once per day in `jax_sim.py`, so two missed feeds is ~48 turns."""
    J = pytest.importorskip("kagg.sim.jax_sim")
    assert J.TURNS_PER_DAY == 24
    assert TA.FEED_EVERY >= J.TURNS_PER_DAY, (
        f"the toy demands a feed every {TA.FEED_EVERY} turns; the real game allows "
        f"{J.TURNS_PER_DAY * TA.UNFED_ESCAPE}"
    )


def test_one_animal_is_sustainable_without_the_macro():
    """**The core property.** Keeping an animal alive and collecting from it must fit in the turn
    budget with `tend` OFF, or the baseline arm is measuring an impossibility rather than a policy."""
    per_cycle = _feed_actions_per_cycle(tend=False) + 1      # + one COLLECT
    assert per_cycle <= TA.FEED_EVERY, (
        f"one animal needs {per_cycle} actions per {TA.FEED_EVERY}-turn feed cycle without the "
        f"macro; there are only {TA.FEED_EVERY} turns in it"
    )


def test_the_animal_path_beats_crops_without_the_macro():
    """The toy's own docstring promises the animal economy is 'strictly better than crops if
    executed'. That promise has to hold in the arm where the macro is off, or 'the policy failed to
    learn animals' is the correct answer rather than a failure."""
    assert TA.animal_upside(tend=False) > 0, "one well-run animal must be net positive without TEND"


def test_a_played_out_season_can_actually_collect_without_the_macro():
    """End-to-end, not arithmetic: run the greedy chain by hand with `tend=False` and require at
    least one COLLECT to land. Under the pre-fix cadence this returns zero."""
    env = TA.ToyFarmAnimals(start_animal=True, tend=False)
    collected = 0
    done = False
    while not done:
        legal = env.legal()
        if legal[TA.COLLECT]:
            a = TA.COLLECT
            collected += 1
        elif env.unfed >= 1 and legal[TA.FEED]:
            a = TA.FEED
        elif env.unfed >= 1 and legal[TA.GET_WHEAT]:
            a = TA.GET_WHEAT
        elif legal[TA.GET_WHEAT] and not env.carrying:
            a = TA.GET_WHEAT
        else:
            a = TA.NOOP
        _, _, done = env.step(a)
    assert env.has_animal, "the animal escaped despite being fed at every opportunity"
    assert collected > 0, "no product was ever collectable without the macro"
