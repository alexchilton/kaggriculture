"""A SELL quantity pinned at the top class means "at least this much", not "exactly this much".

`jax_policy.MAX_QTY = 64` and `jax_act.py:321` states the quantity head's class index IS the
quantity, so the largest number the head can name is 63.

Measured over カワシギ's four tapes, 2,576 market orders (`data/logs/which_head_diverges.log` and the
census run on 2026-08-27):

    teacher SELL quantities   ... 30 x2, 32 x1, 34 x1, 41 x1, | 70 x1, 71 x1, 72 x2
    orders at exactly 63: 0      at 62: 0      at 61: 0
    highest under the cap: 41

There is a gap with no orders at all from 42 to 69. The teacher never names 63, so a head emitting
63 is SATURATION and nothing else -- the label it was fitted on was unrepresentable. All four such
orders are the same action: the final-day wheat dump on turn 697.

Cost, measured: `91906088` diverges from its teacher on exactly ONE market turn in 719 and loses
$1,930; `92498144` loses $656. Both are this order.

The fix is a decode-side read of the barn, not a wider head: `private["shed"]` says how much there
actually is, and `_do_market` sells what is there. Raising MAX_QTY would widen three head outputs
and force a retrain from scratch to buy the same $2,586.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def _uncap():
    from kagg.agents.neural import _uncap_sells
    return _uncap_sells


def test_a_sell_pinned_at_the_top_class_is_reread_from_the_shed():
    from kagg.rl.jax_policy import MAX_QTY
    cap = MAX_QTY - 1
    market = [["HIRE"], ["SELL", "WHEAT", cap], ["SELL", "WOOL", 4]]
    out = _uncap()(market, {"WHEAT": 72, "WOOL": 4})
    assert out[1] == ["SELL", "WHEAT", 72], out
    assert out[0] == ["HIRE"], "non-SELL orders must be untouched"
    assert out[2] == ["SELL", "WOOL", 4], "an unsaturated SELL must be untouched"


def test_an_unsaturated_sell_is_never_rewritten_even_with_a_full_shed():
    """The head asking for 41 with 200 in the barn means 41. Only the top class is ambiguous."""
    out = _uncap()([["SELL", "WHEAT", 41]], {"WHEAT": 200})
    assert out == [["SELL", "WHEAT", 41]], out


def test_a_saturated_sell_with_less_in_the_shed_keeps_the_capped_number():
    """`_commit_unit` fails a SELL silently when the shed is short (`reference:653`), so asking for
    more than there is would be a no-op, not a bigger sale."""
    out = _uncap()([["SELL", "WHEAT", 63]], {"WHEAT": 20})
    assert out == [["SELL", "WHEAT", 63]], out


def test_no_shed_leaves_every_order_alone():
    market = [["SELL", "WHEAT", 63]]
    assert _uncap()(market, None) == [["SELL", "WHEAT", 63]]
    assert _uncap()(market, {}) == [["SELL", "WHEAT", 63]]


def test_decode_action_ITSELF_applies_the_uncap():
    """The helper being correct says nothing about it being CALLED.

    Written because the first version of this file stayed green with `decode_action`'s call to
    `_uncap_sells` reverted: every test poked the helper directly, so the wiring -- the part that
    ships -- was covered by nothing. This project has now hit that three times; see the
    "revert the fix and confirm the test goes red" rule in CLAUDE.md.
    """
    import numpy as np

    from kagg.agents.neural import decode_action
    from kagg.il import market_bundles as MB
    from kagg.il.replays import encode_action
    from kagg.rl.jax_policy import MAX_QTY, N_BUNDLES

    action = {"farmer": ["PASS"], "hands": [], "market": [["SELL", "WHEAT", 72]]}
    vocab = MB.Vocabulary.from_bundles([(("SELL", "WHEAT"),)], max_size=N_BUNDLES)
    labels = encode_action(action, 1, vocab=vocab)
    seated = {}
    for k, v in labels.items():
        a = np.asarray(v)
        seated[k] = np.stack([a, a]) if a.ndim else np.asarray([a, a])

    capped = decode_action(seated, 1, vocab, seat=0, shed=None)
    sells = [o for o in capped["market"] if o and o[0] == "SELL"]
    assert sells, "the fixture must produce a SELL for this test to mean anything"
    assert int(sells[0][2]) == MAX_QTY - 1, (
        f"expected the label to arrive capped at {MAX_QTY - 1}, got {sells[0]}")

    fixed = decode_action(seated, 1, vocab, seat=0, shed={"WHEAT": 72})
    sells = [o for o in fixed["market"] if o and o[0] == "SELL"]
    assert int(sells[0][2]) == 72, (
        f"decode_action did not apply the uncap: {sells[0]}. The helper can be correct while "
        f"nothing calls it.")


def test_the_teacher_never_names_the_top_class():
    """The premise the rule rests on. If this goes red, 63 is a legitimate quantity and reading the
    shed on it would rewrite a deliberate order."""
    import collections
    import glob
    import json

    q = collections.Counter()
    for ep in ("92498144", "91906088", "91907974", "92466371"):
        hits = glob.glob(str(REPO / f"data/seed_scripts/*/{ep}.json"))
        if not hits:
            continue
        d = json.loads(pathlib.Path(hits[0]).read_text())
        names = (d.get("info") or {}).get("TeamNames") or []
        seat = next((i for i, t in enumerate(names) if "カワシギ" in (t or "")), None)
        if seat is None:
            continue
        for s in d["steps"][1:]:
            for o in ((s[seat] or {}).get("action") or {}).get("market") or []:
                if o and len(o) > 2 and o[0] == "SELL":
                    q[int(o[2])] += 1
    if not q:
        import pytest
        pytest.skip("tapes not present")

    from kagg.rl.jax_policy import MAX_QTY
    cap = MAX_QTY - 1
    assert q.get(cap, 0) == 0, f"the teacher names {cap} {q[cap]} times; it is not a saturation marker"
    under = [v for v in q if v < cap]
    assert max(under) < cap - 10, f"largest legitimate order is {max(under)}, too close to the cap"
