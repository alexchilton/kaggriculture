"""The market is one token. This pins the token's contract before anything trains on it.

The measured reason for the head: 78.7% of the teacher's turns carry no market action, so six
independent "probably no" heads multiply into "certainly no" -- greedy argmax over the marginals
emits ZERO orders while the marginals discriminate 12:1. See
`docs/the_market_is_one_token_not_nine_heads_2026-08-20.md`.

A bundle is the multiset of `(op, item)` pairs in one turn's market list. Quantities are NOT part of
the identity: 52 of 116 non-empty bundles carry more than one quantity vector and the five-way sell
carries 48, so quantities get their own head conditioned on the drawn bundle.
"""

import pytest

from kagg.il import market_bundles as MB


def test_the_empty_bundle_is_index_zero():
    """The majority label must be a real class, not an absence.

    78.7% of turns are empty. If "no orders" is represented by falling off the end of the
    vocabulary, the head cannot express the commonest decision the teacher makes.
    """
    vocab = MB.Vocabulary.from_bundles([(), (("SELL", "WHEAT"),)])
    assert vocab.index(()) == 0
    assert vocab.bundle(0) == ()


def test_a_bundle_ignores_order_and_quantity():
    """`SELL WHEAT 4, SELL MILK 2` and `SELL MILK 9, SELL WHEAT 1` are the same decision."""
    a = MB.bundle_of([["SELL", "WHEAT", 4], ["SELL", "MILK", 2]])
    b = MB.bundle_of([["SELL", "MILK", 9], ["SELL", "WHEAT", 1]])
    assert a == b


def test_repeated_ops_are_kept_not_collapsed():
    """`HIRE x10` is rank 2 in the teacher's vocabulary and is ONE decision.

    A set would collapse it to a single HIRE, which is the d10 failure -- units 8 and 9 never hired
    and 20 planned ops died with them. It is a multiset.
    """
    ten = MB.bundle_of([["HIRE"]] * 10)
    one = MB.bundle_of([["HIRE"]])
    assert ten != one
    assert len(ten) == 10


def test_every_bundle_round_trips_through_its_index():
    orders = [
        [],
        [["HIRE"]] * 10,
        [["BUY_PRODUCT", "WHEAT", 3], ["BUY_SEED", "WHEAT", 2], ["HIRE"], ["HIRE"]],
        [["SELL", "FERTILIZER", 5], ["SELL", "MILK", 2], ["SELL", "WHEAT", 8]],
    ]
    vocab = MB.Vocabulary.from_bundles([MB.bundle_of(o) for o in orders])
    for o in orders:
        b = MB.bundle_of(o)
        assert vocab.bundle(vocab.index(b)) == b


def test_an_unseen_bundle_falls_back_to_empty_not_to_a_crash():
    """At play time the student can only emit vocabulary entries, but the LOSS sees teacher labels
    from a fresh game. An unseen bundle must be labellable, not an exception."""
    vocab = MB.Vocabulary.from_bundles([(), (("SELL", "WHEAT"),)])
    assert vocab.index((("SELL", "MELON"),)) == 0


def test_coverage_reports_what_the_head_would_miss():
    """Sizing the head is a measurement, not a guess: 128 classes covered 99.7% of our teacher."""
    bundles = [()] * 80 + [(("SELL", "WHEAT"),)] * 15 + [(("SELL", "MELON"),)] * 5
    vocab = MB.Vocabulary.from_bundles(bundles, max_size=2)
    assert vocab.size == 2
    assert vocab.coverage(bundles) == pytest.approx(0.95)
