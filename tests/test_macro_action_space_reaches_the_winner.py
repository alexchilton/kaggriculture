"""The macro action space must be able to express the play that actually wins.

`kagg/rl/env.py` factors the problem the right way -- one decision per game day, 30 steps instead of
720, terminal win/loss reward -- and its own docstring states the cost plainly: "a policy that only
tunes the heuristic's knobs inherits the heuristic's ceiling."

This pins *where* that ceiling is, against a measured target rather than an opinion. Episode
89873723 seat 0 banked $147,178 and our simulator now reproduces its tape turn for turn
(`tests/test_tape_parity.py`), so its play is a fact, not a guess:

    animals bought on days 0, 5, 6, 8, 9, 10   (14 animals)
    BUILD_PASTURE on turn 1, PLACE on turn 3, FEED on turn 5
    945 FEED / CARE / COLLECT_FERT ops, 31.5 per day, every day of the season
    2 quadrants unlocked
    306 hires

`ACTION_BUCKETS` has a `cow_tiles` head, so it can allocate tiles to animals. It has no head that
starts the herd and no head that holds feed for it -- which is the identical half-open chain
measured in `executor.py:416` and logged in `data/logs/diverge_by_day_147k.log`: pens built, animals
bought, `shed_wheat` 0 on all thirty days, 14 animals escaped at full purchase price, season ended
on $0. Roughly 35% of leader revenue is livestock, and 83% in the top episode we hold.

**Why this is the gate rather than a win-rate measurement.** A win rate cannot distinguish "the
policy searched the space and rejected livestock" from "livestock was never in the space". CLAUDE.md
already records that exact confusion costing a day. This test asks the cheap structural question
first: is the winning play *reachable at all*.

**DEFERRED 2026-08-04, marked `xfail(strict=True)` rather than deleted or silently skipped.**
The gap these tests describe is real, but `StrategyEnv` is not the active track. `kagg/search/routines.py`
already implements the chain-as-unit-of-search representation, and it answers the valley better than
widening these heads would: a routine emits the whole chain or nothing, so a money-negative partial
chain is not merely discouraged, it is *unrepresentable*. Widening `ACTION_BUCKETS` would also stack a
fourth mechanism onto a critic measured terminal-blind (`docs/critic_terminal_blindness_2026-08-03.md`)
and a policy currently diffusing under excess entropy (`docs/entropy_diffusion_2026-08-04.md`).

`strict=True` so that whenever these heads *are* added, the xfail turns into a failure and forces the
marker off. See `docs/fable_review_macro_action_plan_2026-08-04.md`.
"""

import pytest

from kagg.search import plan as P

env = pytest.importorskip("kagg.rl.env", reason="gymnasium not installed")

pytestmark = pytest.mark.xfail(
    strict=True,
    reason="deferred: routines.py is the active representation, not StrategyEnv's heads")

# Measured from `data/seed_scripts/replay_89873723_seat0.npz`; see the module docstring.
WINNER_FIRST_STOCK_DAY = 0
WINNER_HERD = 14
WINNER_QUADRANTS = 2


def test_the_day_heads_cover_the_plan_knobs_that_carry_the_strategy():
    """**The claim.** Every lever the winner's season turns has to have a head.

    `Plan` is the parameter set `kagg/search/executor.py` already interprets, and it is the natural
    macro-action vocabulary: these are knobs, not canned plays, so exposing them does not hand the
    policy a strategy the way a behavioural prior would.
    """
    required = {
        "stock_day": "when to start buying animals -- winner starts day 0",
        "feed_wheat": "wheat held per animal; without it the herd starves and escapes",
        "herd": "target headcount per species -- winner reaches 14",
        "land_day": "when to unlock each quadrant -- winner unlocks 2",
        "hires": "per-day headcount target -- winner hires 306 times",
        "dump_day": "when to stop holding produce and clear the shed",
    }
    missing = {k: why for k, why in required.items()
               if not any(k in head for head in env.ACTION_KEYS)}

    assert not missing, (
        "the macro action space cannot express these levers, so no amount of training can find "
        "them:\n" + "\n".join(f"  {k}: {why}" for k, why in missing.items())
        + f"\nheads present: {list(env.ACTION_KEYS)}")


def test_those_knobs_really_are_plan_fields_and_not_invented_here():
    """Anti-vacuity: if `Plan` did not carry these, the test above would be demanding fiction."""
    plan = P.decode(P.random_genomes(1, seed=0) if hasattr(P, "random_genomes")
                    else P.zero_genome()[None, :])
    for field in ("stock_day", "feed_wheat", "herd", "land_day", "dump_day", "hires"):
        assert hasattr(plan, field), f"Plan has no {field} -- the required-heads list is wrong"


def test_a_head_that_allocates_animal_tiles_without_stocking_them_is_the_known_trap():
    """Pins the specific shape of the bug, so widening the space cannot half-fix it.

    `cow_tiles` exists. That is what makes this dangerous rather than merely incomplete: the space
    can build pens it can never fill, which spends the opening stake and returns nothing. Measured
    over a full season -- 14 animals escaped, $0 final bank.
    """
    assert "cow_tiles" in env.ACTION_KEYS, "fixture is stale -- cow_tiles was the tile allocator"
    stocking = [h for h in env.ACTION_KEYS if "stock" in h or "feed" in h]
    assert stocking, (
        "cow_tiles can allocate pens while nothing can stock or feed them -- the half-open animal "
        "chain that ended a measured season on $0 with 14 animals escaped")
