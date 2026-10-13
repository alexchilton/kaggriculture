"""The teacher's play as a chain of turns keyed on `(day, hour, shops)`, with a fallback.

**Why a table and not a network, at least first.** Measured on tetsuya, 99 games, 71,181 turns
(`data/logs/shop_conditioning_2026-08-20.log`):

    conditioning                  acc%    H bits
    MARKET | day,hour             88.2     0.530
    MARKET | day,hour,shops       98.6     0.034
    FARMER | day,hour             72.9     0.973
    FARMER | day,hour,shops       96.1     0.097

He is a deterministic function of the clock and the shop draw to 98.6%. At 0.034 bits there is
almost nothing left for a model to learn, so the honest first implementation is a lookup: exact,
instant, no decode step, no absorbing state, and no training run to go wrong.

**The one thing a table cannot do is the unseen draw, and that is the whole risk.** There are 87
distinct end-of-window shop draws across 99 games, so nearly every new game presents a key the
table has never seen. `lookup` therefore degrades in three steps -- exact `(day, hour, shops)`,
then the nearest shop set at that `(day, hour)`, then the modal action at that `(day, hour)`
regardless of shops. `evaluate_holdout` measures how much is lost at each step, which is the number
that decides whether a model is needed at all.

Shops are a MULTISET, not a set: a draw can carry `YARN_STORE` twice and the second one is real
drain. Counted, sorted, and compared by multiset overlap for that reason.
"""

import collections
import json
import pathlib

from kagg.il.bundles import bundle_of


def shops_at(observation):
    """The unlocked shop multiset for one observation, as a sorted tuple."""
    town = (observation or {}).get("town") or {}
    return tuple(sorted(str(s) for s in (town.get("unlocked_shops") or [])))


def action_key(action):
    """What the teacher did this turn, compactly: farmer op, hand ops, market bundle.

    Enough to score imitation and to identify a repeat. NOT enough to emit -- emission needs the
    op arguments too, which `turns()` keeps alongside.
    """
    act = action or {}
    fa = act.get("farmer")
    hands = tuple((h[0] if h else "-") for h in (act.get("hands") or []))
    return ((fa[0] if fa else "-"), hands, bundle_of(act))


def turns(paths, team):
    """`(game_id, day, hour, shops, action)` for every recorded turn of `team`'s seat."""
    for path in paths:
        p = pathlib.Path(path)
        try:
            d = json.loads(p.read_text())
        except Exception:                                          # noqa: BLE001
            continue
        names = [str(n) for n in ((d.get("info") or {}).get("TeamNames") or [])]
        if team not in names:
            continue
        seat = names.index(team)
        steps = d.get("steps") or []
        for i, step in enumerate(steps):
            if i == 0:
                continue
            prev = (steps[i - 1][seat] or {}).get("observation") or {}
            if "day" not in prev:
                continue
            yield (p.stem, int(prev.get("day", 0) or 0), int(prev.get("hour", 0) or 0),
                   shops_at(prev), (step[seat] or {}).get("action") or {})


def build(rows):
    """`{(day, hour): {shops: Counter(action_key)}}` from `turns()` rows."""
    table = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for _gid, day, hour, shops, act in rows:
        table[(day, hour)][shops][action_key(act)] += 1
    return table


def _overlap(a, b):
    """Multiset intersection size. `YARN_STORE` twice is two drains, not one."""
    ca, cb = collections.Counter(a), collections.Counter(b)
    return sum((ca & cb).values())


def lookup(table, day, hour, shops):
    """`(action_key, how)` -- `how` is 'exact', 'nearest', 'clock' or 'miss'.

    Degrades deliberately rather than failing: an unseen draw is the common case, not the edge.
    """
    slot = table.get((day, hour))
    if not slot:
        return None, "miss"
    if shops in slot:
        return slot[shops].most_common(1)[0][0], "exact"
    best, best_score = None, -1
    for cand, counter in slot.items():
        score = _overlap(shops, cand)
        if score > best_score:
            best, best_score = counter, score
    if best is not None and best_score > 0:
        return best.most_common(1)[0][0], "nearest"
    pooled = collections.Counter()
    for counter in slot.values():
        pooled.update(counter)
    return (pooled.most_common(1)[0][0], "clock") if pooled else (None, "miss")


def evaluate_holdout(paths, team, folds=None):
    """Leave-one-game-out: build on every other game, predict the held-out one.

    This is the measurement that decides whether the table is enough. Training accuracy on a
    memorised table is 100% by construction and means nothing.
    """
    rows = list(turns(paths, team))
    by_game = collections.defaultdict(list)
    for r in rows:
        by_game[r[0]].append(r)
    ids = sorted(by_game)
    if folds:
        ids = ids[:folds]

    tally = collections.Counter()
    hit = collections.Counter()
    for held in ids:
        train = [r for gid, rs in by_game.items() if gid != held for r in rs]
        table = build(train)
        for _gid, day, hour, shops, act in by_game[held]:
            want = action_key(act)
            got, how = lookup(table, day, hour, shops)
            tally[how] += 1
            tally["all"] += 1
            if got is not None:
                if got == want:
                    hit["all_exactmatch"] += 1
                    hit[how] += 1
                if got[2] == want[2]:
                    hit["market"] += 1
                    if want[2]:
                        hit["market_nonempty"] += 1
                if got[0] == want[0]:
                    hit["farmer"] += 1
            if want[2]:
                tally["nonempty"] += 1
    return tally, hit, len(ids)
