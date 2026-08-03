"""P2b's state source: finding the turns where a payoff becomes available.

**Why ripening and not harvesting.** `docs/fable_review_day0_launch_2026-08-03.md` chose the
*opportunity* rather than the *event*: waiting for a HARVEST to fire and succeed is circular, because
HARVEST runs 0.18-0.24% of ops, so resume points would not exist until the problem P2b exists to fix
had half-solved itself. A ripening event needs only an earlier PLANT+WATER, and PLANT runs 1-3%, so
these appear in the trainee's own rollouts long before harvests do.

**Why a flip and not a level.** A board with one ripe melon on it is ripe on every subsequent turn
until something harvests it. Recording the level would emit hundreds of near-identical resume states
from one crop and drown the buffer; the *transition* fires once per crop per ripening.

These tests are on hand-built tiles because a real rollout ripens nothing inside a 32-turn window at
current planting rates -- every count would read zero, which is exactly how a broken implementation
would also look. That failure mode has already cost this project once, in `test_terminal_loss_share`.
"""

import numpy as np
import pytest

jnp = pytest.importorskip("jax.numpy")

from kagg.rl import opportunity as OPP           # noqa: E402
from kagg.sim import jax_sim as J                # noqa: E402

MELON = 4          # FIRST_YIELD_DAY 10 -- the slowest crop, so ages are unambiguous
WHEAT = 0          # FIRST_YIELD_DAY 2


def _tiles(b=1, **over):
    """A `Tiles` of all-empty land, with named fields overridden.

    Every field is `[B, N_PLAYERS, TILES]`; `animal` defaults to `NO_ANIMAL` rather than 0, since 0
    is a real animal id and defaulting it would put a goose on every tile of every test.
    """
    shape = (b, J.N_PLAYERS, J.TILES)
    base = {f: np.zeros(shape, np.int32) for f in J.Tiles._fields}
    base["kind"] = np.full(shape, J.EMPTY, np.int32)
    base["animal"] = np.full(shape, J.NO_ANIMAL, np.int32)
    for k, v in over.items():
        assert k in base, f"no such tile field: {k}"
        base[k] = np.asarray(v, np.int32)
    return J.Tiles(**{k: jnp.asarray(v) for k, v in base.items()})


def _plant(b=1, seat=0, tile=0, crop=MELON, planted_day=0, units=1):
    """One planted tile for one seat, everything else empty."""
    shape = (b, J.N_PLAYERS, J.TILES)
    kind = np.full(shape, J.EMPTY, np.int32)
    cr = np.zeros(shape, np.int32)
    pd = np.zeros(shape, np.int32)
    yu = np.zeros(shape, np.int32)
    kind[:, seat, tile] = J.PLANT
    cr[:, seat, tile] = crop
    pd[:, seat, tile] = planted_day
    yu[:, seat, tile] = units
    return _tiles(b, kind=kind, crop=cr, planted_day=pd, yield_units=yu)


def _day(b, d):
    return jnp.asarray(np.full((b,), d, np.int32))


# ---- crop_ready: the level ---------------------------------------------------------------------


def test_a_melon_is_not_ready_before_its_first_yield_day():
    """`FIRST_YIELD_DAY[MELON]` is 10, so day 9 is one short and must read False."""
    t = _plant(crop=MELON, planted_day=0)
    assert not bool(OPP.crop_ready(t, _day(1, 9))[0, 0, 0])


def test_a_melon_is_ready_on_exactly_its_first_yield_day():
    """The boundary is `>=`, matching `jax_masks.py:80`. Off by one here is off by a game-day."""
    t = _plant(crop=MELON, planted_day=0)
    assert bool(OPP.crop_ready(t, _day(1, 10))[0, 0, 0])


def test_readiness_is_measured_from_the_planted_day_not_the_calendar():
    """A melon planted on day 6 is ready on day 16, not on day 10."""
    t = _plant(crop=MELON, planted_day=6)
    assert not bool(OPP.crop_ready(t, _day(1, 10))[0, 0, 0])
    assert bool(OPP.crop_ready(t, _day(1, 16))[0, 0, 0])


def test_a_plant_with_nothing_left_on_it_is_never_ready():
    """`yield_units == 0` is a harvested or dead crop. `jax_masks.py:80` requires `units_held > 0`
    and so must this, or every spent tile would fire an opportunity forever."""
    t = _plant(crop=WHEAT, planted_day=0, units=0)
    assert not bool(OPP.crop_ready(t, _day(1, 20))[0, 0, 0])


def test_bare_land_is_never_ready():
    assert not bool(OPP.crop_ready(_tiles(), _day(1, 25)).any())


def test_a_weed_is_never_ready():
    """WEED is not PLANT. It has no crop and no yield, but it is also not EMPTY, so a `!= EMPTY`
    test would wrongly pass it."""
    shape = (1, J.N_PLAYERS, J.TILES)
    kind = np.full(shape, J.EMPTY, np.int32); kind[:, 0, 0] = J.WEED
    yu = np.zeros(shape, np.int32); yu[:, 0, 0] = 3          # nonsense, but the mask must not care
    assert not bool(OPP.crop_ready(_tiles(kind=kind, yield_units=yu), _day(1, 25)).any())


# ---- animals -----------------------------------------------------------------------------------


def test_an_animal_holding_product_is_ready_and_an_empty_pen_is_not():
    shape = (1, J.N_PLAYERS, J.TILES)
    kind = np.full(shape, J.EMPTY, np.int32); kind[:, 0, :2] = J.COOP
    animal = np.full(shape, J.NO_ANIMAL, np.int32); animal[:, 0, 0] = 0      # tile 1 stays empty
    yu = np.zeros(shape, np.int32); yu[:, 0, :2] = 2
    got = OPP.animal_ready(_tiles(kind=kind, animal=animal, yield_units=yu))
    assert bool(got[0, 0, 0]), "an animal with product waiting is a collect opportunity"
    assert not bool(got[0, 0, 1]), "an empty coop is not, whatever its yield_units says"


def test_an_unfed_animal_is_a_feed_opportunity_and_a_fed_one_is_not():
    """FEED and CARE are the two ops `CLAUDE.md` measures as the best money predictors (+0.452,
    +0.441), and the op census reads FEED at 0.01%. This is the trigger for that half of the game."""
    shape = (1, J.N_PLAYERS, J.TILES)
    kind = np.full(shape, J.EMPTY, np.int32); kind[:, 0, :2] = J.PASTURE
    animal = np.full(shape, J.NO_ANIMAL, np.int32); animal[:, 0, :2] = 1
    fed = np.zeros(shape, np.int32); fed[:, 0, 1] = 1
    got = OPP.feed_ready(_tiles(kind=kind, animal=animal, fed_today=fed))
    assert bool(got[0, 0, 0])
    assert not bool(got[0, 0, 1])


# ---- newly_ready: the flip ---------------------------------------------------------------------


def test_a_crop_that_ripens_between_two_turns_fires_once():
    before = _plant(crop=MELON, planted_day=0)
    after = _plant(crop=MELON, planted_day=0)
    got = OPP.newly_ready(before, _day(1, 9), after, _day(1, 10))
    assert int(got.sum()) == 1
    assert bool(got[0, 0, 0])


def test_a_crop_that_was_already_ripe_does_not_fire():
    """**The reason this is a flip and not a level.** A ripe melon is ripe on every turn until it is
    harvested; recording the level would emit one resume state per turn per crop."""
    t = _plant(crop=MELON, planted_day=0)
    assert int(OPP.newly_ready(t, _day(1, 11), t, _day(1, 12)).sum()) == 0


def test_a_crop_harvested_between_the_turns_does_not_fire():
    """Ready -> not ready is not an opportunity. Only the rising edge counts."""
    before = _plant(crop=WHEAT, planted_day=0, units=1)
    after = _plant(crop=WHEAT, planted_day=0, units=0)
    assert int(OPP.newly_ready(before, _day(1, 5), after, _day(1, 5)).sum()) == 0


def test_a_freshly_planted_crop_does_not_fire_on_the_turn_it_is_planted():
    """PLANT is the *precondition* for an opportunity, not the opportunity. Wheat's
    `FIRST_YIELD_DAY` is 2, so a tile planted on day 4 is not ready on day 4."""
    before = _tiles()
    after = _plant(crop=WHEAT, planted_day=4)
    assert int(OPP.newly_ready(before, _day(1, 4), after, _day(1, 4)).sum()) == 0


def test_an_animal_becoming_collectable_fires():
    shape = (1, J.N_PLAYERS, J.TILES)
    kind = np.full(shape, J.EMPTY, np.int32); kind[:, 0, 0] = J.COOP
    animal = np.full(shape, J.NO_ANIMAL, np.int32); animal[:, 0, 0] = 0
    before = _tiles(kind=kind, animal=animal)                                  # yield_units 0
    yu = np.zeros(shape, np.int32); yu[:, 0, 0] = 1
    after = _tiles(kind=kind, animal=animal, yield_units=yu)
    assert int(OPP.newly_ready(before, _day(1, 3), after, _day(1, 3)).sum()) == 1


# ---- per-seat and per-game reduction ------------------------------------------------------------


def test_opportunities_are_reported_per_seat():
    """`trainable` is seat 0 only (`train_jax_rl.py:599`), so an opponent's ripening crop must not
    produce a resume point -- it is not a position the trainee built or can be credited for."""
    before = _plant(seat=1, crop=MELON, planted_day=0)
    after = _plant(seat=1, crop=MELON, planted_day=0)
    got = OPP.newly_ready(before, _day(1, 9), after, _day(1, 10))
    assert int(got[0, 0].sum()) == 0, "seat 0 planted nothing"
    assert int(got[0, 1].sum()) == 1, "seat 1's crop ripened"


def test_any_opportunity_reduces_to_one_flag_per_game_and_seat():
    """Two crops ripening on the same turn is still one resume point, not two."""
    shape = (2, J.N_PLAYERS, J.TILES)
    kind = np.full(shape, J.EMPTY, np.int32); kind[0, 0, :3] = J.PLANT
    cr = np.zeros(shape, np.int32); cr[0, 0, :3] = MELON
    yu = np.zeros(shape, np.int32); yu[0, 0, :3] = 1
    before = _tiles(2, kind=kind, crop=cr, yield_units=yu)
    got = OPP.any_opportunity(before, _day(2, 9), before, _day(2, 10))
    assert got.shape == (2, J.N_PLAYERS)
    assert bool(got[0, 0]) and not bool(got[0, 1])
    assert not bool(got[1].any()), "the second game has an empty board"


# ---- picking the resume turn --------------------------------------------------------------------


def test_the_resume_turn_is_before_the_opportunity_not_on_it():
    """**The whole point of P2b.** Resuming *on* the ripe turn hands the policy a free harvest and
    teaches nothing about getting there. Resuming `lookback` turns earlier leaves a short chain whose
    payoff is inside GAE's ~20-turn reach."""
    fires = np.zeros((12, 3), bool); fires[7, 1] = True
    got = OPP.resume_turns(jnp.asarray(fires), lookback=4)
    assert got.tolist() == [[3, 1]]


def test_a_resume_turn_never_goes_below_the_start_of_the_window():
    """A crop ripening at turn 2 with a lookback of 8 clamps to 0 rather than wrapping to the end,
    the same off-by-one species as `test_the_near_window_does_not_wrap_around_the_horizon`."""
    fires = np.zeros((10, 1), bool); fires[2, 0] = True
    assert OPP.resume_turns(jnp.asarray(fires), lookback=8).tolist() == [[0, 0]]


def test_no_opportunities_yields_no_resume_turns():
    """The common case in a 32-turn window today, and the one a caller must handle."""
    assert OPP.resume_turns(jnp.zeros((6, 4), bool), lookback=2).shape == (0, 2)


def test_every_firing_turn_is_reported_not_just_the_first():
    fires = np.zeros((10, 2), bool)
    fires[3, 0] = fires[8, 0] = fires[5, 1] = True
    got = sorted(tuple(r) for r in OPP.resume_turns(jnp.asarray(fires), lookback=1).tolist())
    assert got == [(2, 0), (4, 1), (7, 0)]


# ---- turning indices into states ---------------------------------------------------------------


def test_gather_states_picks_the_right_turn_and_game_from_a_stacked_rollout():
    """`jax.lax.scan` stacks its outputs as `[T, B, ...]`, so a resume point is a (turn, game) pair
    and every leaf of the pytree must be indexed with the same pair. Getting the axes the wrong way
    round produces a valid-looking state from the wrong game, which no shape check would catch."""
    T, B = 6, 4
    stacked = J.Tiles(**{
        f: jnp.asarray(np.arange(T * B * J.N_PLAYERS * J.TILES, dtype=np.int32)
                       .reshape(T, B, J.N_PLAYERS, J.TILES) + i * 1000)
        for i, f in enumerate(J.Tiles._fields)})
    idx = jnp.asarray([[4, 1], [0, 3]], dtype=jnp.int32)
    got = OPP.gather_states(stacked, idx)
    assert got.kind.shape == (2, J.N_PLAYERS, J.TILES)
    assert np.array_equal(np.asarray(got.kind[0]), np.asarray(stacked.kind[4, 1]))
    assert np.array_equal(np.asarray(got.kind[1]), np.asarray(stacked.kind[0, 3]))
    # A second leaf, because indexing one field correctly and another by position is the real risk.
    assert np.array_equal(np.asarray(got.crop[0]), np.asarray(stacked.crop[4, 1]))


def test_gather_states_on_no_resume_points_returns_an_empty_leading_axis():
    """The common case today. It must be an empty batch, not a crash and not a phantom row."""
    T, B = 3, 2
    stacked = J.Tiles(**{f: jnp.zeros((T, B, J.N_PLAYERS, J.TILES), jnp.int32)
                         for f in J.Tiles._fields})
    got = OPP.gather_states(stacked, jnp.zeros((0, 2), jnp.int32))
    assert got.kind.shape == (0, J.N_PLAYERS, J.TILES)
