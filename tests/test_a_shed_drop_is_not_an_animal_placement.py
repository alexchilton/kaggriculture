"""`PLACE` is two different ops and a target row must only record one of them.

`reference/kaggriculture.py:377` -- PLACE puts an animal on a matching unoccupied structure when
`item in ANIMALS` and the unit stands on it. Otherwise, if the unit is orthogonally adjacent to the
shed, the SAME op is a shed drop that moves goods out of the hand and into the shed.

`scripts/extract_target_rows.py` recorded both into `places`, so the field meant for the herd filled
up with produce. Measured over 213 of カワシギ's seasons:

    STRAWBERRY 2794   WOOL 2218   COW 1936   MELON 1653   SHEEP 1496   FERTILIZER 1204   MILK 1039

The herd is a minority of its own field. Two consequences, both real:

- `kagg/search/schedule_agent.py` reads `row["places"]` to work out which animals are still to be
  put out, and died with `KeyError: 'FERTILIZER'` on d1 when handed one of these rows.
- Every distinct-row and coverage count computed from that field is inflated, because a day is
  split whenever two seasons carried different produce to the shed -- which is routing, not plan.

A shed drop belongs with DROP and PICKUP: it is how the day is executed, not what the day achieves.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.extract_target_rows import target_row      # noqa: E402

ANIMALS = ("GOOSE", "COW", "SHEEP")


def day_of(*turns):
    """Pad a list of actions out to a full 24-turn day."""
    idle = {"farmer": ["PASS"], "hands": [], "market": []}
    return list(turns) + [idle] * (24 - len(turns))


def test_a_shed_drop_does_not_become_a_placement():
    row = target_row(day_of({"farmer": ["PLACE", "STRAWBERRY", 3], "hands": [], "market": []},
                            {"farmer": ["PLACE", "FERTILIZER", 2], "hands": [], "market": []},
                            {"farmer": ["PLACE", "MILK", 1], "hands": [], "market": []}),
                     {}, 0)
    assert row["places"] == [], \
        "produce carried to the shed was recorded as a herd placement: %r" % (row["places"],)


def test_an_animal_placement_is_still_recorded():
    row = target_row(day_of({"farmer": ["PLACE", "COW"], "hands": [], "market": []},
                            {"farmer": ["PLACE", "SHEEP"], "hands": [], "market": []}),
                     {}, 0)
    assert row["places"] == ["COW", "SHEEP"], \
        "the herd placement was dropped along with the shed drops: %r" % (row["places"],)


def test_a_mixed_day_keeps_only_the_animals():
    row = target_row(day_of({"farmer": ["PLACE", "WOOL", 4], "hands": [["PLACE", "GOOSE"]],
                             "market": []},
                            {"farmer": ["PLACE", "COW"], "hands": [["PLACE", "WHEAT", 2]],
                             "market": []}),
                     {}, 0)
    assert row["places"] == ["COW", "GOOSE"], \
        "expected only the herd, got %r" % (row["places"],)


def test_the_field_is_only_ever_animals_across_the_real_library():
    """The regression as it was actually found: read the shipped library and check the field."""
    import collections
    import json

    lib = REPO / "data" / "target_rows_kawa_norm_dedup.json"
    if not lib.exists():                                    # pragma: no cover - data not extracted
        import pytest
        pytest.skip("%s not present; run scripts/extract_target_rows.py" % lib)

    seen = collections.Counter()
    for r in json.loads(lib.read_text()):
        seen.update(r["target"].get("places") or [])
    stray = {k: v for k, v in seen.items() if k not in ANIMALS}
    assert not stray, "non-animals in `places`: %r" % (dict(sorted(stray.items())),)
