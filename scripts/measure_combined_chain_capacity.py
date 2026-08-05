"""How much can ONE unit really do in a day, now that a pen group and a crop block can share it?

The wall: covering the leader's farm needed 14 chains, one unit each, which forces unit 17 and
$125,400 of season hires -- more than he banks. He does the same work with twelve hands because his
hands tend a pen *and* crop tiles on the same day. `Script.claim` now makes that expressible.

Expressible is not the same as affordable in turns, and the first fixture tried here did not fit: a
2-pen shed group claims 12-13 of the 23 work turns and the cheapest 4-tile block wants 16. So this
sweeps the geometry rather than asserting an arithmetic that was already wrong once.

For every (pen group, crop block, cadence) it reports the worst day's turn count, because a chain is
only legal if *every* day fits -- the expensive days are the replant days, not the steady state.

Read the output as the answer to one question: what is the largest tiles-per-unit a combined chain can
carry, and does it beat the leader's ~11 tiles per hand?
"""

import itertools

from kagg.search import routines as R

SHED = R.shed_access_tiles()


def cost(fn):
    """Worst-day turn count for a chain, or None if it cannot be built at all."""
    s = R.Script()
    try:
        fn(s)
    except ValueError:
        return None
    # `_claimed` starts at 1 because turn 0 is the market order, so work turns used is
    # `claimed - 1` = `TURNS_PER_DAY - turns_left - 1`. Out of `TURNS_PER_DAY - 1` = 23.
    used = [R.TURNS_PER_DAY - s.turns_left(d, 0) - 1 for d in range(R.SEASON_DAYS)]
    return max(used)


def nw_block(n):
    """`n` NW tiles in serpentine order, nearest the shed first -- the cheapest walk available."""
    cand = [(x, y) for y in range(4, -1, -1) for x in range(4, -1, -1)
            if (x, y) not in SHED and R.land_purchases_for((x, y)) == 0]
    cand.sort(key=lambda t: (abs(t[0] - 4) + abs(t[1] - 4)))
    return cand[:n]


print("=" * 100)
print("ONE UNIT, ONE DAY: what fits in 23 work turns")
print("=" * 100)
print(f"{'pens':>5} {'feed':>5} {'tiles':>6} {'water':>6} {'pen only':>9} {'crop only':>10} "
      f"{'combined':>9} {'fits?':>6}")

best = []
for n_pen, feed_every in itertools.product((0, 1, 2), (1, 2)):
    pens = [t for t in SHED if R.land_purchases_for(t) == 0][:n_pen] or None
    if n_pen and pens is None:
        continue
    for n_tiles, water_every in itertools.product((0, 2, 4, 6, 8, 10, 12), (1, 2)):
        if not n_pen and not n_tiles:
            continue
        tiles = nw_block(n_tiles)
        if n_tiles and len(tiles) < n_tiles:
            continue

        def build(s, pens=pens, tiles=tiles, fe=feed_every, we=water_every):
            if pens:
                R.ranch(s, "COW", pens, 0, unit=0, buy_land=False, feed_every=fe)
            if tiles:
                R.grow(s, "STRAWBERRY", tiles, 1, unit=0, buy_land=False, water_every=we)

        pen_only = cost(lambda s, p=pens, fe=feed_every: (
            R.ranch(s, "COW", p, 0, unit=0, buy_land=False, feed_every=fe) if p else None)) or 0
        crop_only = cost(lambda s, t=tiles, we=water_every: (
            R.grow(s, "STRAWBERRY", t, 1, unit=0, buy_land=False, water_every=we) if t else None)) or 0
        both = cost(build)
        fits = both is not None
        if not (n_pen and n_tiles):
            continue                       # the interesting rows are the genuinely combined ones
        print(f"{n_pen:>5} {feed_every:>5} {n_tiles:>6} {water_every:>6} {pen_only:>9} "
              f"{crop_only:>10} {str(both or 'RAISES'):>9} {'yes' if fits else 'NO':>6}")
        if fits:
            best.append((n_pen + n_tiles, n_pen, n_tiles, feed_every, water_every, both))

print()
print("=" * 100)
print("THE BEST COMBINED CHAINS -- most work on one unit, cheapest first")
print("=" * 100)
best.sort(key=lambda r: (-r[0], r[5]))
for total, n_pen, n_tiles, fe, we, turns in best[:8]:
    print(f"  {n_pen} pen(s) + {n_tiles:>2} tiles = {total:>2} things on one unit "
          f"(feed_every={fe}, water_every={we}, worst day {turns}/23 turns)")

if best:
    top = best[0]
    print()
    print(f"best combined chain carries {top[0]} things per unit against the leader's ~11 tiles/hand")
    print(f"so the leader's 14 pens + ~100 tiles needs about "
          f"{-(-114 // max(top[0], 1))} units, not 14")
else:
    print("  nothing combined fits -- the geometry, not the writer, is the wall")