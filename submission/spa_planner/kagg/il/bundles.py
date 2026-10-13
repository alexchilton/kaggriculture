"""The market as ONE token, and the clock-only baseline any clone has to beat.

**Why a bundle and not nine heads.** Measured over tetsuya's 78 games and 56,082 seat-turns
(`docs/the_market_is_one_token_not_nine_heads_2026-08-20.md`): the whole `market` list takes only
**346 distinct op+item shapes**, and the top 100 cover 98.5% of turns. Meanwhile **80.7% of turns
carry no market action at all**, so every per-product marginal has an overwhelming "no" base rate
and nine independent "probably no" decisions multiply into "certainly no". That is the arithmetic
behind the result in CLAUDE.md -- argmax over the marginals emitted ZERO orders while the marginals
themselves discriminated 12:1 on `buy_product`. No amount of head tuning fixes a product of nine
sub-0.5 probabilities; representing the joint does.

The bundle that makes the case is played 271 times:

    HIRE x7, SELL MILK, SELL STRAWBERRY, SELL WHEAT

Seven hires and three sells in ONE turn -- the sells take earlier order slots and settle first, so
they fund the hires in the same turn. That coordination is what we lose on d10, where units 8 and 9
were never hired and 20 planned ops died with them. As nine heads it is near unemittable. As one
token it is free, and correct by construction rather than by luck.

**Quantities are deliberately NOT in the token.** A wrong quantity is graceful (sell 4 instead of
5); a wrong bundle is catastrophic (never sell at all). Quantity is a separate head conditioned on
the drawn bundle, and that is where the modelling budget belongs.

## The baselines, and why accuracy is the wrong metric

`clock_baseline` scores the best possible (day, hour) lookup table. It exists because a clone must
be shown to have learned something the clock does not already say, and because plain accuracy is
actively misleading here:

    a model that ALWAYS predicts "empty market" scores 80.7%

That is the absorbing state `kagg/il/bc.py` already records -- `P(move) = 6e-5` per unit-turn and a
checkpoint that banked exactly its $3,000 start. So a clone is judged on three numbers, not one:

    market bundle, non-empty turns   beat 58.6%
    farmer op, all turns             beat 73.2%
    non-empty market rate            match ~19.3%

Measured on tetsuya. Re-measure for any other teacher rather than assuming these transfer.
"""

import collections
import json
import math
import pathlib

#: Turns whose market list is empty. Kept as an explicit symbol rather than None so it occupies a
#: real class in the categorical and its probability is trained like any other.
EMPTY = ()


def bundle_of(action):
    """The market token for one turn's action: the sorted multiset of (op, item).

    Sorted, so slot ORDER does not fragment the vocabulary -- `[SELL WHEAT, HIRE]` and
    `[HIRE, SELL WHEAT]` are the same decision. Order does matter to the ENVIRONMENT within a turn
    (earlier slots settle first, which is how a sell funds a hire), but that is a property of how
    the bundle is emitted, not of which bundle was chosen, and it is restored at emit time.
    """
    mk = (action or {}).get("market") or []
    return tuple(sorted(
        (str(o[0]), str(o[1]) if len(o) > 1 else "")
        for o in mk if isinstance(o, (list, tuple)) and o))


def _seat_of(replay, team):
    names = [str(n) for n in ((replay.get("info") or {}).get("TeamNames") or [])]
    return names.index(team) if team in names else None


def iter_actions(paths, team):
    """`(day, hour, action)` for `team`'s seat, over every replay that contains them."""
    for path in paths:
        try:
            d = json.loads(pathlib.Path(path).read_text())
        except Exception:                                          # noqa: BLE001
            continue
        seat = _seat_of(d, team)
        if seat is None:
            continue
        steps = d.get("steps") or []
        for i, step in enumerate(steps):
            if i == 0:
                continue
            prev = (steps[i - 1][seat] or {}).get("observation") or {}
            if "day" not in prev:
                continue
            yield (int(prev.get("day", 0) or 0), int(prev.get("hour", 0) or 0),
                   (step[seat] or {}).get("action") or {})


def build_vocabulary(paths, team, coverage=1.0):
    """`(vocab, stats)` -- every distinct bundle, most frequent first.

    **`coverage` defaults to 1.0 and should stay there. Truncating measured actively harmful.**
    At 0.985 the overall out-of-vocabulary rate is a comfortable 1.49% -- and **16.6% of every turn
    containing a HIRE falls outside the kept set** (`data/logs/hire_counts_2026-08-20.log`).

    The cut lands there because coverage optimises TOTAL turns while hire bundles are rare per
    symbol: they fragment across nine distinct counts (x1 to x9, with x5/x6/x7 carrying 75% of them)
    times the sell combinations they ride with. Rare per symbol, and the highest-consequence
    decision on the board -- a missing hire cost d10 twenty planned ops
    (`docs/plant_is_a_money_problem_2026-08-20.md`).

    That is the same defect as `replays.encode_action` storing `hire` as a binary, reached by a
    different route: a representation that cannot express "hire seven" caps the clone below the
    teacher no matter how well it fits. There is no safe place to cut, so do not cut.

    352 classes against 68,305 samples is not a problem worth optimising.
    """
    counts = collections.Counter(bundle_of(a) for _d, _h, a in iter_actions(paths, team))
    total = sum(counts.values())
    vocab, seen = [], 0
    for b, n in counts.most_common():
        vocab.append(b)
        seen += n
        if total and seen / total >= coverage:
            break
    nonempty = total - counts.get(EMPTY, 0)
    return vocab, {
        "turns": total,
        "distinct": len(counts),
        "kept": len(vocab),
        "coverage": (seen / total) if total else 0.0,
        "empty_rate": (counts.get(EMPTY, 0) / total) if total else 0.0,
        "nonempty_rate": (nonempty / total) if total else 0.0,
    }


def _modal_accuracy(table):
    total = hit = 0
    for c in table.values():
        total += sum(c.values())
        hit += c.most_common(1)[0][1]
    return (hit / total) if total else 0.0, total


def _conditional_entropy(table):
    total = sum(sum(c.values()) for c in table.values())
    if not total:
        return 0.0
    out = 0.0
    for c in table.values():
        n = sum(c.values())
        out += (n / total) * -sum((v / n) * math.log2(v / n) for v in c.values() if v)
    return out


def clock_baseline(paths, team):
    """What a perfect `(day, hour)` lookup table achieves. The floor a clone must clear.

    Returns market accuracy over ALL turns, over NON-EMPTY turns, farmer-op accuracy, and the
    conditional entropies. The non-empty figure is the one that matters: the all-turns figure is
    dominated by the empty class and a do-nothing policy scores well on it.
    """
    market = collections.defaultdict(collections.Counter)
    nonempty = collections.defaultdict(collections.Counter)
    farmer = collections.defaultdict(collections.Counter)
    for day, hour, act in iter_actions(paths, team):
        b = bundle_of(act)
        market[(day, hour)][b] += 1
        if b:
            nonempty[(day, hour)][b] += 1
        fa = act.get("farmer")
        farmer[(day, hour)][fa[0] if fa else "-"] += 1
    m_acc, m_n = _modal_accuracy(market)
    n_acc, n_n = _modal_accuracy(nonempty)
    f_acc, _f_n = _modal_accuracy(farmer)
    return {
        "market_all": m_acc, "market_all_turns": m_n,
        "market_nonempty": n_acc, "market_nonempty_turns": n_n,
        "farmer_op": f_acc,
        "H_market_given_clock": _conditional_entropy(market),
        "H_nonempty_given_clock": _conditional_entropy(nonempty),
        "H_farmer_given_clock": _conditional_entropy(farmer),
    }
