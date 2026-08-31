"""Index 0 of a bundle vocabulary means DO NOTHING. A file that puts a basket there is corrupt.

`Vocabulary.index` returns 0 for any bundle it does not hold, and `Vocabulary.from_bundles` pins
`EMPTY` at 0 for exactly that reason. `load_vocab` does NOT go through `from_bundles` -- it builds
`Vocabulary(raw)` straight from the file -- so the invariant lives in the artifact, and nothing
checked it.

Measured 2026-08-28. `scripts/build_recorded_player_bundle_vocab.py` wrote its 256 baskets most
frequent first with no EMPTY, so `data/il/bundle_vocab_kawa.json` had `SELL FERTILIZER` at index 0.
Two failures, and the second one is silent:

    labelling  every SELL FERTILIZER turn labels to 0 = "place no orders". 16,600 of 287,600 rows
               (5.77%) came back as bundle misses, against the 0.38% the builder predicted.
    playing    every do-nothing turn ALSO labels to 0, and `to_orders(0)` is `[["SELL",
               "FERTILIZER"]]`. The student would post a fertilizer sale on the ~78% of turns the
               teacher trades nothing at all, and agreement would score all of it as correct.

The three vocabularies that predate this builder all have `[]` at entry 0, because they were
written from `Vocabulary.from_bundles`. This pins that.
"""
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from kagg.il import market_bundles as MB  # noqa: E402


def test_the_empty_bundle_is_index_zero_when_a_vocabulary_is_built():
    v = MB.Vocabulary.from_bundles([MB.bundle_of([["SELL", "WHEAT"]])] * 9)
    assert v.index(MB.bundle_of([])) == 0
    assert v.bundle(0) == MB.EMPTY
    assert v.to_orders(0) == []


def test_a_vocabulary_file_that_puts_a_basket_at_index_zero_is_refused(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text(json.dumps([[["SELL", "FERTILIZER"]], [["HIRE", ""]]]))
    with pytest.raises(ValueError, match="index 0"):
        MB.load_vocab(str(p))


def test_a_vocabulary_file_with_the_empty_bundle_first_is_accepted(tmp_path):
    p = tmp_path / "good.json"
    p.write_text(json.dumps([[], [["SELL", "FERTILIZER"]]]))
    v = MB.load_vocab(str(p))
    assert v.size == 2
    assert v.index(MB.bundle_of([])) == 0
    assert v.index(MB.bundle_of([["SELL", "FERTILIZER"]])) == 1


def test_a_basket_at_index_zero_would_be_played_on_every_silent_turn(tmp_path):
    """The failure the miss count cannot show: what index 0 DOES when the student emits it."""
    bad = MB.Vocabulary([MB.bundle_of([["SELL", "FERTILIZER"]])])
    assert bad.index(MB.bundle_of([])) == 0            # a turn with no orders labels to 0
    assert bad.to_orders(0) == [["SELL", "FERTILIZER"]]  # and 0 posts a sale


@pytest.mark.parametrize("name", sorted(p.name for p in (REPO / "data/il").glob("bundle_vocab*.json")))
def test_every_shipped_vocabulary_reserves_index_zero(name):
    raw = json.loads((REPO / "data/il" / name).read_text())
    assert raw[0] == [], f"{name} entry 0 is {raw[0]!r}, which means DO NOTHING everywhere it is read"
