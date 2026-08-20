"""The held-out instrument must not run a bigger forward pass than training does.

The theory this pins, measured on the box 2026-08-20 at 20:37:01:

    jax.errors.JaxRuntimeError: RESOURCE_EXHAUSTED: Out of memory while trying to allocate
    4.79GiB with allocator GPU_0_bfc on device 0 [executable_name='jit_argmax_mix']

`fit_bc.main` trained batches of 256 all the way through epoch 0 -- fifteen shards, about eight
minutes -- and then called `argmax_mix` ONCE on 8,192 held-out rows. That is 32x the training
batch, and the entity transformer's attention is quadratic in its 124 tokens per row, so the single
call asked for 4.79 GiB and the epoch's weights were lost: the traceback lands at line 237, before
both the print and the checkpoint save.

The failure is invisible on CPU, where an oversized allocation is slow rather than fatal, and
invisible on a small holdout, because `sl` is `min(8192, len(...))` -- a smoke run with two games
never reaches 8,192 rows and so never builds the big pass.
"""

import pathlib
import sys

import numpy as np
import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def _load_helper():
    """Import `argmax_in_chunks` from fit_bc without importing jax or running main()."""
    fit_bc = pytest.importorskip("scripts.fit_bc")
    return fit_bc.argmax_in_chunks


def test_the_instrument_never_forwards_more_rows_than_the_chunk():
    """The whole point: no single call may exceed the chunk, however big the holdout is."""
    argmax_in_chunks = _load_helper()
    seen = []

    def fake(tiles, units, gfeat):
        seen.append(len(tiles))
        return np.zeros(len(tiles), np.int32), np.zeros((len(tiles), 3), np.int32)

    n = 8192
    argmax_in_chunks(fake, np.zeros((n, 4)), np.zeros((n, 2)), np.zeros((n, 5)), chunk=256)

    assert seen, "the helper never called the model at all"
    assert max(seen) <= 256, (
        "a forward pass of %d rows -- this is the 4.79 GiB allocation that killed the run, and it "
        "is bigger than the 256 the training loop proved fits" % max(seen))


def test_chunking_does_not_change_the_answer():
    """A cheaper instrument that reports different numbers is worse than no instrument."""
    argmax_in_chunks = _load_helper()
    rng = np.random.default_rng(0)
    n = 1000
    tiles, units, gfeat = rng.normal(size=(n, 4)), rng.normal(size=(n, 2)), rng.normal(size=(n, 5))

    def fake(t, u, g):
        # Row-wise and deterministic, so chunking is only correct if the split is clean.
        return (t.sum(axis=1) * 1000).astype(np.int32), (u * 10).astype(np.int32)

    whole_b, whole_o = fake(tiles, units, gfeat)
    part_b, part_o = argmax_in_chunks(fake, tiles, units, gfeat, chunk=256)

    np.testing.assert_array_equal(np.asarray(part_b), whole_b)
    np.testing.assert_array_equal(np.asarray(part_o), whole_o)


def test_a_ragged_tail_is_not_dropped():
    """8192 divides by 256; a holdout of 8,000 does not. The remainder must still be scored."""
    argmax_in_chunks = _load_helper()
    n = 1001
    tiles, units, gfeat = np.arange(n)[:, None], np.arange(n)[:, None], np.arange(n)[:, None]

    def fake(t, u, g):
        return t[:, 0].astype(np.int32), u[:, 0].astype(np.int32)

    b, _o = argmax_in_chunks(fake, tiles, units, gfeat, chunk=256)
    assert len(b) == n, "dropped %d rows of the holdout" % (n - len(b))
    np.testing.assert_array_equal(np.asarray(b), np.arange(n))


def test_the_instrument_call_site_actually_uses_the_helper():
    """The three tests above pin the helper. The bug was one line in `main` that did not call it.

    A correct helper nobody calls fixes nothing, and this is the regression that would reappear:
    someone reads `argmax_mix` and passes it the whole probe slice again. Checking the source is
    crude, but the alternative -- running `main` -- needs jax, a GPU and 8,192 rows of npz, which
    is exactly the combination that let the defect ship in the first place.
    """
    import inspect

    fit_bc = pytest.importorskip("scripts.fit_bc")
    src = inspect.getsource(fit_bc.main)

    assert "argmax_in_chunks(" in src, (
        "the held-out instrument in fit_bc.main no longer chunks its forward pass; a single "
        "8,192-row call asks for 4.79 GiB and aborts the run after a full epoch has trained")
    assert "chunk=args.batch" in src, (
        "the instrument chunks, but not at the training batch size -- that size is the only one "
        "the epoch just finished proved fits on this card")
