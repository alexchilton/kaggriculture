"""P3: the observation must say what the crew already owned costs to KEEP.

**The measured problem.** There is no upkeep line in this game -- `_end_of_day` and `_night` move no
money -- but `_night` does `n_units = ones_like(n_units)` (`jax_sim.py:1138`), so the crew is
dismissed every night and a crew of N is *rented* at `sum(HIRE_COST[:N-1])` every morning.
`HIRE_COST` is Fibonacci, so that is $54/day at nine units, $143 at eleven, $376 at thirteen.

Measured on the stopped `league1` checkpoint, the per-day hire column reads
`-54, -88, -88, -116, -143, -88, -143` through the back half of the season -- crews of 9, 10 and 11
rebuilt each morning -- for a season total of **-$2,122**, more than the entire season's gross sales
of $2,300. It is the largest single drain in the game and it did not move when the frozen-market bug
was fixed.

**What the policy was told about it.** `hire_afford = HIRE_COST[hires_today] / money`, and
`hires_today` resets each morning, so at the moment the day's hiring decision is made `next_hire` is
`HIRE_COST[0]` = **$1**. That is true of the first hire and says nothing about the $143 the day's
programme will actually cost, nor that the bill repeats every day to the bell.

This is a fact, not a judgment -- the same side of `CLAUDE.md`'s line as the existing `land_afford`
and `hire_afford`. It says what keeping the crew costs, never whether to keep it.
"""

import numpy as np
import pytest

jnp = pytest.importorskip("jax.numpy")

from kagg.rl import jax_obs, jax_policy as P
from kagg.sim import jax_sim as J

# The width before this feature was added, kept as a guard: if `glob` grows for some *other* reason
# the arithmetic in every assertion below is silently measuring the wrong column.
GLOB_WIDTH_BEFORE = 59


def _state(n_units=1, money=3000.0, batch=1):
    st = J.reset(batch)
    farm = st.farm._replace(
        n_units=jnp.full_like(st.farm.n_units, int(n_units)),
        money=jnp.full_like(st.farm.money, float(money)))
    return st._replace(farm=farm)


def _rehire_col(state):
    """The new feature's column, addressed from the end so an insertion above it cannot shift it."""
    _t, _u, g = jax_obs.encode(state)
    return np.asarray(g)[..., jax_obs.REHIRE_AFFORD_INDEX]


# ---- the table -------------------------------------------------------------------------------


def test_hire_ladder_matches_the_measured_per_day_spend():
    """The ladder the A/B's hire column landed on, pinned against `HIRE_COST` itself."""
    h = np.asarray(J.HIRE_COST)
    want = {8: 33, 9: 54, 10: 88, 11: 143, 12: 232, 13: 376}
    for crew, cost in want.items():
        assert int(h[:crew - 1].sum()) == cost, f"crew {crew} rebuild cost"


def test_cumulative_table_is_the_prefix_sum():
    cum = np.asarray(jax_obs.HIRE_REBUILD_COST)
    h = np.asarray(J.HIRE_COST)
    assert len(cum) >= J.MAX_UNITS + 1, "table must cover every reachable crew size"
    for n in range(1, J.MAX_UNITS + 1):
        assert cum[n] == pytest.approx(h[:n - 1].sum()), f"crew {n}"


# ---- the feature -----------------------------------------------------------------------------


def test_glob_grew_by_exactly_one_column():
    _t, _u, g = jax_obs.encode(J.reset(2))
    assert g.shape[-1] == GLOB_WIDTH_BEFORE + 1


def test_a_lone_farmer_costs_nothing_to_keep():
    """`n_units == 1` is the state every night resets to, so there is nothing to re-hire."""
    assert _rehire_col(_state(n_units=1, money=3000.0)) == pytest.approx(0.0)


@pytest.mark.parametrize("crew,cost", [(8, 33), (9, 54), (10, 88), (11, 143), (12, 232)])
def test_feature_is_rebuild_cost_over_bank(crew, cost):
    got = _rehire_col(_state(n_units=crew, money=10_000.0))
    assert got == pytest.approx(cost / 10_000.0, rel=1e-5)


def test_feature_is_monotone_in_crew_size_at_fixed_bank():
    # `_rehire_col` is [batch, seats]; every entry is identical here, so take one.
    vals = [float(_rehire_col(_state(n_units=n, money=5_000.0)).ravel()[0])
            for n in range(1, 13)]
    assert vals == sorted(vals)
    assert vals[-1] > vals[0]


def test_feature_clips_like_its_two_neighbours():
    """`land_afford` and `hire_afford` both clip at 4.0; an unbounded ratio would dominate the token."""
    assert _rehire_col(_state(n_units=13, money=1.0)) == pytest.approx(4.0)
    assert _rehire_col(_state(n_units=12, money=1.0)) == pytest.approx(4.0)


def test_feature_distinguishes_what_hire_afford_cannot():
    """**The point of the feature.** At the start of a day `hire_afford` reads the same for a lone
    farmer and for a crew of eleven, because `hires_today` is 0 in both and `HIRE_COST[0]` is $1.
    """
    _t, _u, g1 = jax_obs.encode(_state(n_units=1, money=3000.0))
    _t, _u, g11 = jax_obs.encode(_state(n_units=11, money=3000.0))
    hire_afford_1 = np.asarray(g1)[..., jax_obs.HIRE_AFFORD_INDEX]
    hire_afford_11 = np.asarray(g11)[..., jax_obs.HIRE_AFFORD_INDEX]
    assert hire_afford_1 == pytest.approx(hire_afford_11), (
        "guard: hire_afford is expected to be blind here, which is why P3 exists")

    assert _rehire_col(_state(n_units=1, money=3000.0)) != pytest.approx(
        _rehire_col(_state(n_units=11, money=3000.0)))


def test_no_nan_when_the_farm_is_broke():
    """The bank reaches exactly $0 in these runs, so the divide has to be guarded."""
    v = _rehire_col(_state(n_units=11, money=0.0))
    assert np.isfinite(v).all() and v == pytest.approx(4.0)


# ---- the migration ---------------------------------------------------------------------------


def _model():
    return P.Policy(d_model=32, n_heads=2, n_layers=1)


def _params_for_glob_width(model, width, key=0):
    """Init the policy against a `glob` of the given width, standing in for an older checkpoint."""
    import jax

    t = jnp.zeros((2, J.TILES, jax_obs.encode(J.reset(1))[0].shape[-1]), jnp.float32)
    u = jnp.zeros((2, J.MAX_UNITS, jax_obs.encode(J.reset(1))[1].shape[-1]), jnp.float32)
    g = jnp.zeros((2, width), jnp.float32)
    return model.init(jax.random.PRNGKey(key), t, u, g)


def test_migrate_widens_the_glob_projection_with_zeros():
    """**The trap this feature carries.** `glob` widening grows the input projection's LEADING axis.

    `migrate_params` only ever handled growth on the trailing axis (the op head), so without this
    branch no checkpoint loads -- including the `--kl-prior` anchor, which the project records as
    the change that reversed its decline.
    """
    model = _model()
    old = _params_for_glob_width(model, GLOB_WIDTH_BEFORE)
    new = _params_for_glob_width(model, GLOB_WIDTH_BEFORE + 1)

    migrated = P.migrate_params(old, new)

    from flax.traverse_util import flatten_dict
    fo, fm, fn = flatten_dict(old), flatten_dict(migrated), flatten_dict(new)
    grown = [p for p in fn if jnp.shape(fo[p]) != jnp.shape(fn[p])]
    assert len(grown) == 1, f"expected exactly the glob kernel to grow, got {grown}"

    path = grown[0]
    assert jnp.shape(fm[path]) == jnp.shape(fn[path])
    old_rows = np.asarray(fo[path])
    got = np.asarray(fm[path])
    assert np.array_equal(got[:GLOB_WIDTH_BEFORE], old_rows), "trained rows must be preserved"
    assert np.all(got[GLOB_WIDTH_BEFORE:] == 0.0), "the new feature's row must start at zero"


def test_migrated_network_is_behaviourally_identical_on_day_one():
    """A zero row means the new column cannot change any output until it is trained."""
    import jax

    model = _model()
    old = _params_for_glob_width(model, GLOB_WIDTH_BEFORE)
    new = _params_for_glob_width(model, GLOB_WIDTH_BEFORE + 1)
    migrated = P.migrate_params(old, new)

    key = jax.random.PRNGKey(7)
    t = jax.random.normal(key, (2, J.TILES, jax_obs.encode(J.reset(1))[0].shape[-1]))
    u = jax.random.normal(key, (2, J.MAX_UNITS, jax_obs.encode(J.reset(1))[1].shape[-1]))
    g_old = jax.random.normal(key, (2, GLOB_WIDTH_BEFORE))
    # Any value at all in the new column, to prove the zero row really does ignore it.
    g_new = jnp.concatenate([g_old, jnp.full((2, 1), 3.7)], axis=-1)

    h_old, v_old = model.apply(old, t, u, g_old)
    h_new, v_new = model.apply(migrated, t, u, g_new)

    assert np.allclose(np.asarray(v_old), np.asarray(v_new), atol=1e-5)
    for k in h_old:
        assert np.allclose(np.asarray(h_old[k]), np.asarray(h_new[k]), atol=1e-5), k


def test_load_or_migrate_routes_a_narrow_checkpoint():
    model = _model()
    old = _params_for_glob_width(model, GLOB_WIDTH_BEFORE)
    new = _params_for_glob_width(model, GLOB_WIDTH_BEFORE + 1)
    out = P.load_or_migrate(old, new)
    from flax.traverse_util import flatten_dict
    assert all(jnp.shape(v) == jnp.shape(flatten_dict(new)[p])
               for p, v in flatten_dict(out).items())


def test_load_or_migrate_leaves_a_matching_checkpoint_alone():
    model = _model()
    new = _params_for_glob_width(model, GLOB_WIDTH_BEFORE + 1)
    assert P.load_or_migrate(new, new) is new


def test_a_checkpoint_needing_nothing_still_raises_in_migrate():
    """The existing guard against a silently no-op migration must survive the new branch."""
    model = _model()
    new = _params_for_glob_width(model, GLOB_WIDTH_BEFORE + 1)
    with pytest.raises(ValueError, match="nothing was migrated"):
        P.migrate_params(new, new)
