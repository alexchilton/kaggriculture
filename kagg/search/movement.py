"""How the crew's tiles are ORDERED and CUT into lanes. One place, no flags.

Pulled out of `crew.py`, where the sweep, the lane cut and the at-risk promotion sat in three
different places and the third quietly undid the first. Both routines below are pure: they take
tiles and return tiles, and every weight or shed position they need is an argument.

**The property both callers depend on is CONTIGUITY.** `order` returns a sequence whose consecutive
tiles are adjacent on the board, so any contiguous SLICE of it is itself a walk. `split` then cuts
it anywhere and every piece is still a sensible route. A reversed sequence is still a walk, which is
what lets the caller sweep from the far edge home.

Anything that re-sorts a finished sequence breaks that property, and the breakage is invisible --
the lanes still look like lanes. See `split`.
"""
import collections


def serpentine(tiles, shed):
    """Boustrophedon sweep, rows ordered by distance from the shed, direction alternating.

    Alternating is the whole point: sorting by raw `(y, x)` makes every row change a full-width jump
    back, which is exactly the walk the sweep exists to avoid.
    """
    sy = shed[1] if shed else 0
    rows = collections.defaultdict(list)
    for t in tiles:
        rows[t[1]].append(t)
    out = []
    for i, y in enumerate(sorted(rows, key=lambda y: abs(y - sy))):
        out.extend(sorted(rows[y], key=lambda t: t[0], reverse=bool(i % 2)))
    return out


def split(ordered, k, weight):
    """Cut `ordered` into `k` contiguous runs of roughly equal weight.

    Contiguous is the point. Round-robin or nearest-unit assignment over the same tiles produces
    interleaved routes -- every hand crossing every other hand's block -- which is the thing this
    replaces.
    """
    if k <= 0 or not ordered:
        return []
    total = sum(weight(t) for t in ordered)
    target = total / k
    runs, cur, acc = [], [], 0.0
    for t in ordered:
        cur.append(t)
        acc += weight(t)
        if acc >= target and len(runs) < k - 1:
            runs.append(cur)
            cur, acc = [], 0.0
    if cur:
        runs.append(cur)
    return runs
