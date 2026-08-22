"""A bundle the vocabulary does not hold must be REPORTED, not silently labelled as EMPTY.

**The defect this pins.** `Vocabulary.index` returns 0 for an unknown bundle, and index 0 is the
empty bundle. `replays.encode_action` used that directly, so the teacher's opening --

    HIRE x5, BUY_ANIMAL COW 2, BUY_ANIMAL SHEEP 2, BUY_SEED WHEAT 7, BUY_SEED MELON 12,
    BUY_PRODUCT WHEAT 6

-- was labelled "place no orders". The student learned that target to 0.9983 agreement and banked
$0 for thirty seasons. Measured 2026-08-22 over the four tape teachers: 179 of 1451 traded turns,
12.3%, on every day of the season, containing 512 HIRE and 444 SELL orders.
Full write-up: `docs/the_vocabulary_labels_the_opening_as_nothing_2026-08-22.md`.

The fallback itself is deliberate and is pinned elsewhere
(`tests/test_a_market_bundle_survives_the_round_trip.py`), so it stays. What must change is that
LABELLING is not inference: at label time an unknown bundle is a defect in the artifact, and the
caller has to be able to see it happened.
"""

import numpy as np
import pytest

from kagg.il import market_bundles as MB, replays as RP

#: The teacher's turn 0, on all four tapes, verbatim from `data/logs/probe_send.log`.
OPENING = [["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"],
           ["BUY_ANIMAL", "COW", 2], ["BUY_ANIMAL", "SHEEP", 2],
           ["BUY_SEED", "WHEAT", 7], ["BUY_SEED", "MELON", 12],
           ["BUY_PRODUCT", "WHEAT", 6]]

ACTION = {"farmer": ["PASS"], "hands": [], "market": OPENING}


@pytest.fixture
def without():
    """A vocabulary that cannot say the opening -- the shape of the shipped 197-entry file."""
    return MB.Vocabulary.from_bundles([MB.bundle_of([]), MB.bundle_of([["HIRE"]] * 10)])


@pytest.fixture
def with_it():
    return MB.Vocabulary.from_bundles([MB.bundle_of([]), MB.bundle_of([["HIRE"]] * 10),
                                       MB.bundle_of(OPENING)])


def test_the_miss_is_reported(without):
    heads = RP.encode_action(ACTION, n_units=1, vocab=without)
    assert int(heads["bundle"]) == 0, "the fallback itself is unchanged"
    assert int(heads["w_bundle_miss"]) == 1, (
        "the opening was labelled EMPTY and nothing said so -- this is the whole defect")


def test_a_bundle_the_vocabulary_holds_is_not_a_miss(with_it):
    heads = RP.encode_action(ACTION, n_units=1, vocab=with_it)
    assert int(heads["bundle"]) != 0
    assert int(heads["w_bundle_miss"]) == 0
    assert with_it.bundle(int(heads["bundle"])) == MB.bundle_of(OPENING)


def test_an_empty_market_is_not_a_miss(without):
    """Index 0 is a real decision when the teacher really sent nothing. Do not cry wolf."""
    heads = RP.encode_action({"farmer": ["PASS"], "hands": [], "market": []},
                             n_units=1, vocab=without)
    assert int(heads["bundle"]) == 0
    assert int(heads["w_bundle_miss"]) == 0


def test_the_vocabulary_is_the_one_passed_in(without, with_it):
    """Two vocabularies, one bundle, two answers -- so the caller controls it, not a global.

    `encode_action` read `MB.load_vocab()` with no argument while `dagger_tape` passed `--vocab` to
    build the head tables. They happened to be the same file; nothing made them so.
    """
    a = int(RP.encode_action(ACTION, n_units=1, vocab=without)["bundle"])
    b = int(RP.encode_action(ACTION, n_units=1, vocab=with_it)["bundle"])
    assert a != b


def test_the_default_still_works():
    """Existing callers pass no vocabulary and must keep working."""
    heads = RP.encode_action(ACTION, n_units=1)
    assert "bundle" in heads and np.asarray(heads["bundle"]).size == 1
