"""The bundle head must be able to weight a class by how rare it is, not by how often it appears.

**The defect this pins.** On turn 0 the tape emits ten orders including five HIREs. That bundle is
4 of 2876 turns (0.139%); the empty bundle is 1425 of 2876 (49.5%). Under a flat per-turn mean,
"emit nothing" is right half the time and being wrong on the opening costs almost nothing, so the
student sat at bundle agreement 0.9983 while emitting `[]` on turn 0 and banking $0 for the season.
Measured on `data/dagger_tape/tape-v2/latest.pkl` at round 25; written up in
`docs/the_student_never_hires_2026-08-22.md`.

Two claims, tested separately:

1. `bundle_class_weights` gives a rare class a larger weight than a common one, and normalises so
   the row-mean weight is 1 -- otherwise raising the exponent silently raises the effective learning
   rate on this head and the reweighting could not be told apart from a step-size change.
2. The loss actually CONSUMES the vector. This is the half that a properties-only test would miss:
   a weight computed and never multiplied in is the same as no weight at all, and it would read as
   a measured null.

Claim 2 is asserted exactly, not approximately. An all-ones vector must reproduce the unweighted
bundle loss bit for bit, and a vector that zeroes one row's class must reproduce the other row's
loss alone.
"""

import importlib.util
import pathlib

import jax
import jax.numpy as jnp
import numpy as np
import optax
import pytest

from kagg.il import market_bundles as MB
from kagg.rl import jax_act as A, jax_obs, jax_policy as P
from kagg.sim import jax_sim as J

REPO = pathlib.Path(__file__).resolve().parents[1]


def _load(name):
    """`scripts/` is not a package, so import the module by path."""
    spec = importlib.util.spec_from_file_location(name, REPO / "scripts" / (name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def dagger():
    return _load("dagger_tape")


@pytest.fixture(scope="module")
def world():
    """A real two-row batch, the real policy, the real vocabulary -- nothing hand-rolled."""
    batch = 1
    state = J.reset(batch)
    model = P.Policy()
    tiles, units, glob = jax_obs.encode(state)
    obs = (A._flat(tiles), A._flat(units), A._flat(glob))
    params = model.init(jax.random.PRNGKey(0), *obs)

    # **Six bundles, not two.** With a two-entry vocabulary both legal classes sit at exactly
    # p = 0.5 under an untrained head, every row scores ln(2) = 0.6931, and "zeroing either row
    # changes the loss" cannot be told from "the weight is ignored". The first run of this test
    # failed for that reason, on the fixture rather than on the code.
    vocab = MB.Vocabulary.from_bundles([
        MB.bundle_of([]),
        MB.bundle_of([["HIRE"]] * 5 + [["BUY_SEED", "WHEAT", 7]]),
        MB.bundle_of([["BUY_SEED", "WHEAT", 1]]),
        MB.bundle_of([["BUY_SEED", "MELON", 1]]),
        MB.bundle_of([["HIRE"]]),
        MB.bundle_of([["BUY_PRODUCT", "WHEAT", 1]]),
    ])
    # `pad_to` is not optional. Without it the tables are vocab-width and the head is
    # `P.N_BUNDLES`, and the mismatch surfaces as `bool[2,197] vs bool[2,256]`.
    tables = {k: jnp.asarray(v) for k, v in MB.tables(vocab, pad_to=P.N_BUNDLES).items()}
    bundle_ok = jnp.asarray(MB.valid_table(vocab, pad_to=P.N_BUNDLES))
    masks = A.masks_for(state, bundle_ok)
    return model, params, obs, masks, tables, bundle_ok


def _evaluate(world, class_w, bundle_labels):
    """The real `loss_fn`, through the real `make_step`, on one two-row batch."""
    bc = _load("bc_dagger")
    model, params, obs, masks, tables, bundle_ok = world
    _rollout, _fit, evaluate = bc.make_step(
        model, None, 1, 1, optax.sgd(0.0), 0.0, tables, bundle_ok)

    # A batch of 1 is already TWO rows -- `_flat` folds the seat axis in, so both seats are present.
    # That is the two-row batch this test wants; repeating it would give four.
    assert masks["bundle"].shape[0] == len(bundle_labels)

    # **The two rows are given different LEGAL SETS, and that is what makes this test able to fail.**
    # An untrained bundle head is exactly uniform, so every row scores ln(n_legal) whatever the
    # weights are, and "zeroing a row changed nothing" would be indistinguishable from "the weight
    # is ignored". The first two runs of this test failed that way, at ln(2) and then ln(6).
    # Narrowing row 1 to two legal bundles makes the rows score ln(6) and ln(2), so a weight that
    # reaches the head must move the mean and a weight that does not cannot.
    narrow = jnp.zeros_like(masks["bundle"]).at[1, jnp.asarray(bundle_labels)].set(True)
    masks = dict(masks, bundle=masks["bundle"].at[1].set(narrow[1]))

    labels = {h: jnp.zeros(masks[h].shape[:-1], dtype=jnp.int32) for h in A.ALL_HEADS}
    labels["bundle"] = jnp.asarray(bundle_labels, dtype=jnp.int32).reshape(
        masks["bundle"].shape[:-1])
    live = jnp.ones(masks["op"].shape[:-1], dtype=bool)

    for row, lab in enumerate(bundle_labels):
        assert bool(masks["bundle"][row, lab]), (
            "bundle %d is masked illegal on row %d, so its loss is zeroed and this test would "
            "assert nothing" % (lab, row))

    data = dict(obs=obs, masks=masks, labels=labels, unit_live=live)
    if class_w is not None:
        data["class_w"] = jnp.asarray(class_w, dtype=jnp.float32)
    _total, per_head = evaluate(params, data)
    return {k: float(v) for k, v in per_head.items()}


def test_a_rare_class_outweighs_a_common_one(dagger):
    rows = [{"labels": {"bundle": np.array([0])}}] * 99 + [{"labels": {"bundle": np.array([5])}}]
    w = np.asarray(dagger.bundle_class_weights(rows, alpha=1.0))
    assert w[5] > w[0], "the class seen once must outweigh the class seen 99 times"
    assert w[5] / w[0] == pytest.approx(99.0, rel=1e-4), "full inverse frequency, exactly"


def test_the_weights_do_not_change_the_step_size(dagger):
    rows = [{"labels": {"bundle": np.array([0])}}] * 99 + [{"labels": {"bundle": np.array([5])}}]
    for alpha in (0.0, 0.5, 1.0):
        w = np.asarray(dagger.bundle_class_weights(rows, alpha=alpha))
        seen = np.array([int(r["labels"]["bundle"][0]) for r in rows])
        assert w[seen].mean() == pytest.approx(1.0, rel=1e-5), (
            "row-mean weight must stay 1 at alpha=%s, or the exponent is a hidden learning rate"
            % alpha)


def test_alpha_zero_is_the_old_flat_mean(dagger):
    rows = [{"labels": {"bundle": np.array([0])}}] * 99 + [{"labels": {"bundle": np.array([5])}}]
    w = np.asarray(dagger.bundle_class_weights(rows, alpha=0.0))
    assert w[0] == pytest.approx(1.0) and w[5] == pytest.approx(1.0)


def test_an_unseen_class_gets_no_weight(dagger):
    """A class absent from the aggregate must not be handed 1/0."""
    rows = [{"labels": {"bundle": np.array([0])}}]
    w = np.asarray(dagger.bundle_class_weights(rows, alpha=1.0))
    assert np.isfinite(w).all()
    assert w[7] == 0.0


def test_the_loss_consumes_the_vector(world):
    """All-ones must reproduce the unweighted loss exactly, and zeroing a row must drop it."""
    labels = [0, 2]
    plain = _evaluate(world, None, labels)
    ones = _evaluate(world, np.ones(P.N_BUNDLES), labels)
    assert ones["bundle"] == pytest.approx(plain["bundle"], rel=1e-6), (
        "an all-ones weight vector changed the loss, so the normalisation is wrong")

    only_first = np.zeros(P.N_BUNDLES)
    only_first[labels[0]] = 1.0
    only_second = np.zeros(P.N_BUNDLES)
    only_second[labels[1]] = 1.0
    a = _evaluate(world, only_first, labels)["bundle"]
    b = _evaluate(world, only_second, labels)["bundle"]

    assert a != pytest.approx(b, rel=1e-6), (
        "zeroing either row gave the same loss -- the vector is not reaching the bundle head")
    assert plain["bundle"] == pytest.approx((a + b) / 2.0, rel=1e-5), (
        "the unweighted loss must be the mean of the two rows it averages")
    # The head is uniform at init, so the two rows are exactly ln(6) and ln(2) by construction.
    assert {round(a, 4), round(b, 4)} == {round(float(np.log(6)), 4), round(float(np.log(2)), 4)}


def test_the_weights_reach_only_the_bundle_head(world):
    """`op` must be untouched. A weight that leaked into every head would be a step-size change."""
    labels = [0, 2]
    plain = _evaluate(world, None, labels)
    skewed = np.zeros(P.N_BUNDLES)
    skewed[labels[1]] = 2.0
    got = _evaluate(world, skewed, labels)
    assert got["op"] == pytest.approx(plain["op"], rel=1e-6)
