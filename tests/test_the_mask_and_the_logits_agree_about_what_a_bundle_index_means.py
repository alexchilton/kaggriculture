"""The legality mask and the bundle head must index the SAME vocabulary.

    python -u -m pytest tests/test_the_mask_and_the_logits_agree_about_what_a_bundle_index_means.py -q

THE DEFECT
----------
`kagg/agents/neural.py` resolves the vocabulary correctly for DECODING -- it prefers the one
embedded in the checkpoint and says so:

    neural: checkpoint vocabulary is 256 bundles, data/il/bundle_vocab.json holds 197 --
            using the CHECKPOINT's, which is the one these weights were fitted against.

and then builds the legality MASK from a completely different one:

    _BUNDLE_SELLS = _MB.valid_table(_MB.load_vocab(), pad_to=_PP.N_BUNDLES)   # no path -> the 197

Measured 2026-08-28 on `data/bc_runs/bcr_kawa_v2-20260828-094747/latest.pkl`:

    index 1: ckpt = [SELL FERTILIZER]            mask table = [HIRE x10]
    index 2: ckpt = [SELL FERTILIZER, SELL WHEAT] mask table = [BUY_PRODUCT WHEAT]
    index 3: ckpt = [SELL WHEAT]                 mask table = [SELL FERTILIZER]

Every index means a different basket on the two sides. So `masks_for` decides whether basket *i* is
affordable and in stock by consulting a basket the network is not proposing, and `_masked_logits`
sends the network's actual choice to `-inf`. The head is left with EMPTY at index 0, which is legal
in every state.

**This is invisible in every offline number**, because the loss and the agreement metric both use
`bc._vocab()` for the labels AND the mask, and they match. It only appears in play. Measured cost:
the market head picks the exact right basket on **86.7%** of the teacher's traded turns at 75.8%
mean confidence, and the same checkpoint fires 11 market orders in 719 turns of a real game.

`bc.py` gets this right and says why -- "`_vocab()`, not a second independent `load_vocab()`: the
mask and the labels must be the same file or a bundle legal under one is a different basket under
the other". `neural.py` is the copy of that pairing that was never fixed.
"""
import pathlib
import pickle
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

CKPT = REPO / "data/bc_runs/bcr_kawa_v2-20260828-094747/latest.pkl"


def _checkpoint_with_its_own_vocab():
    if not CKPT.exists():
        pytest.skip(f"{CKPT} not on disk")
    ck = pickle.load(open(CKPT, "rb"))
    if not ck.get("vocab"):
        pytest.skip("checkpoint carries no embedded vocabulary")
    return ck


def test_the_agent_masks_with_the_vocabulary_it_decodes_with():
    """The head-to-head. A mask built from another file forbids the wrong baskets."""
    from kagg.agents import neural
    from kagg.il import market_bundles as MB

    ck = _checkpoint_with_its_own_vocab()
    embedded = MB.Vocabulary([tuple(tuple(p) for p in b) for b in ck["vocab"]])

    table = neural._bundle_sells(embedded)
    assert table.shape[0] >= embedded.size, (
        "the mask table has %d rows for a %d-bundle vocabulary" % (table.shape[0], embedded.size))

    # The real assertion: the table must have been built FROM `embedded`. Rebuilding it from the
    # same vocabulary must reproduce it exactly; rebuilding from the default must not (or the two
    # files happen to agree and this test proves nothing -- which is why that case skips).
    import numpy as np

    from kagg.rl import jax_policy as P

    want = np.asarray(MB.valid_table(embedded, pad_to=P.N_BUNDLES))
    assert np.array_equal(np.asarray(table), want), (
        "the agent's bundle mask was not built from the checkpoint's vocabulary")


def test_the_default_vocabulary_really_is_a_different_vocabulary():
    """Guards the test above from passing vacuously if the two files ever coincide."""
    from kagg.il import market_bundles as MB

    ck = _checkpoint_with_its_own_vocab()
    embedded = [[tuple(p) for p in b] for b in ck["vocab"]]
    default = MB.load_vocab()
    if default.size == len(embedded):
        pytest.skip("default and checkpoint vocabularies are the same size; nothing to discriminate")

    differing = [i for i in range(1, min(default.size, len(embedded)))
                 if list(default.bundle(i)) != embedded[i]]
    assert differing, (
        "the default vocabulary agrees with the checkpoint's on every index, so masking with the "
        "wrong one would be harmless and the test above cannot fail")
