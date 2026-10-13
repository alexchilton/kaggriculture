"""The whole board, assigned once, before the game starts.

**What this replaces.** `_refresh_pins` chooses ground a tile at a time, from the days it has already
seen:

    want = collections.Counter()
    for d in sorted(sched):
        if d <= day:                                 # only days up to TODAY
            want.update(sched[d].get("plants") or [])
    ...
        spot = _next_ground(order, tiles, taken)     # first free tile in sweep order

So it never reserves ground for a crop that is due later, and pens compete with crops for the same
free pool on a first-come basis. The board that comes out is ragged. Measured at d4 dawn, seed 11,
ours against the tape (`data/logs/probe_geom.log`), shed at (4,4):

      OURS                        SEB
    me me wh wh wh              wh wh wh wh wh
    me wh wh wh wh              me me me me me
    wh wh wh wh C*              wh st st st S*
    wh wh  .  . C*               .  .  . S* S*
    wh C* C* S*  S               .  .  . C*  S

His `y=0` is entirely wheat and `y=1` entirely melon, and his five pens are one block hugging the
shed. Ours has melon in the far corner, wheat wrapping round a hole at (2,3)/(3,3), and two pens at
(1,4) and (2,4) sitting *inside* the crop rows -- so the herd hand walks through the crop lanes and
the crop hands walk around pens. A lawnmower over his shape is one clean lane per row; over ours it
crosses itself however it is cut.

That difference is not something the sweep can fix. It is chosen at plant time, and the information
needed to choose better -- every day's `plants` and `builds`, and the `land` rows that say when each
quadrant arrives -- is all in the schedule before turn 0.

**What this does.** One pass over the schedule, pre-game, returning a matrix: tile -> what that tile
is for, all season. Pens are allocated first, as one block against the shed, because a pen on a
shed-access cell runs its entire daily loop -- draw feed, feed, care, collect -- without a single
move. Then each crop takes a contiguous run of the sweep, whole-season quantity at once, ordered by
the day that crop is first needed.

**Quadrants.** The board grows 25 -> 100 tiles and `field_order` is quadrant-major over
`("NW",) + LAND_ORDER`, so the owned set on any day is just NW plus the first N of `LAND_ORDER`,
where N is the number of `land` purchases the schedule makes before that day. A crop is therefore
laid out over the ground that will exist when it is first planted, never over ground bought later.
"""
import collections

from . import routines as R
from . import router as RT

#: Quadrants in the order they are bought. `field_order` uses the same order, so the two agree by
#: construction rather than by coincidence.
QUAD_ORDER = ("NW",) + tuple(R.LAND_ORDER)


def quads_owned(n_bought):
    """The unlocked set after `n_bought` parcels. NW is owned from turn 0."""
    return set(QUAD_ORDER[:1 + max(0, int(n_bought))])


def _first_day_of(sched, key):
    """Day each item under `key` is first wanted, so blocks are laid out in the order they are
    needed rather than in whatever order a Counter happens to iterate."""
    seen = {}
    for day in sorted(sched):
        for item in ((sched[day] or {}).get(key) or []):
            seen.setdefault(item, day)
    return seen


def _occupies_for(crop):
    """Days a planted `crop` holds its square before the ground comes back.

    `ongoing` crops -- strawberry, tomato -- keep fruiting on an interval and are never cleared, so
    they hold their tile for the rest of the season. The rest are harvested once at `max_day` and
    the square is ground again the next morning.
    """
    row = R.CROP_TABLE.get(crop)
    if row is None:
        return R.SEASON_DAYS
    return R.SEASON_DAYS if row.get("ongoing") else int(row["max_day"]) + 1


def _land_by_day(sched):
    """Parcels bought STRICTLY BEFORE each day.

    Strictly before, because a parcel is bought during its own day -- Seb takes d4's at hour 21 --
    and the unit phase runs before the market phase (`kaggriculture.py:922` then `:928`). Ground
    bought today is not plantable today, so laying a crop onto it would pin a tile no hand can
    reach and the plant would be dropped in silence.
    """
    out, running = {}, 0
    for day in sorted(sched):
        out[day] = running
        running += int((sched[day] or {}).get("land") or 0)
    return out


def plan_board(sched):
    """Assign every square the schedule will ever use. Returns `{tile: (op, item)}`.

    `op` is `"BUILD"` or `"PLANT"`; `item` is the animal or the crop. Pure -- no board state, no
    RNG -- so the same schedule always yields the same matrix and it can be built before turn 0.
    """
    sched = {int(k): v for k, v in (sched or {}).items()}
    layout, taken = {}, set()
    land_before = _land_by_day(sched)

    # ---- pens, first, as one block on the shed ---------------------------------------------------
    # Every pen the season will ever build, sited before any crop takes ground. The four shed-access
    # cells lead because a pen there needs no movement at all; after that, nearest free ground to the
    # shed, so the block stays tight instead of stringing out along a sweep row.
    animals = [a for d in sorted(sched) for a in ((sched[d] or {}).get("places") or [])]
    n_pens = sum(int((sched[d] or {}).get("builds") or 0) for d in sorted(sched))
    pen_day = {}
    i = 0
    for d in sorted(sched):
        for _ in range(int((sched[d] or {}).get("builds") or 0)):
            pen_day[i] = d
            i += 1

    for k in range(n_pens):
        owned = quads_owned(land_before.get(pen_day.get(k, 0), 0))
        depots = [c for c in R.shed_access_tiles()
                  if R.quadrant_of(c[0], c[1]) in owned] or [R.SPAWN]
        spot = next((c for c in R.shed_access_tiles()
                     if c not in taken and R.quadrant_of(c[0], c[1]) in owned), None)
        if spot is None:
            free = [t for t in RT.field_order(owned) if t not in taken]
            if not free:
                break
            spot = min(free, key=lambda t: (min(abs(t[0] - c[0]) + abs(t[1] - c[1])
                                                for c in depots), t))
        layout[spot] = ("BUILD", animals[k] if k < len(animals) else "COW")
        taken.add(spot)

    # ---- crops, one contiguous block each --------------------------------------------------------
    # Whole-season quantity in one go, in the order each crop is first needed. That is the whole
    # point: a crop planted across four different days lands on four adjacent squares instead of
    # wherever the frontier happened to be on each of those days.
    # Day by day, because ground unlocks over the season and a crop cannot be laid onto a quadrant
    # that does not exist yet. Taking each crop's WHOLE-season total at its first-use day was tried
    # and is wrong: on this tape MELON and WHEAT are both first planted on d0, MELON sorts first,
    # its season total is 25, and it swallowed the entire NW quadrant -- leaving wheat, the crop the
    # first four days actually live on, with no ground at all.
    #
    # Contiguity comes from allocating SEGMENTS, not tiles.
    #
    # Picking a tile at a time cannot produce a block, however the tile is scored, because a crop
    # planted on d0, d3 and d9 is separated on the board by whatever the OTHER crops claimed on d1
    # and d2. Both per-tile rules were built and measured on this schedule:
    #
    #     nearest free tile to the crop's own block   MELON 21 tiles /  5 islands, wheat stranded
    #                                                 as singletons at (8,1), (1,6), (9,9)
    #     resume from the crop's own sweep cursor     MELON 21 tiles / 16 islands
    #
    # The cursor is worse precisely because it is honest: it refuses to strand a tile far away, so
    # instead it steps over the intervening crops and lands one square past them, every time.
    #
    # So the sweep is modelled as an ordered list of per-crop segments instead. Growing a crop by
    # one tile increments its segment and SHIFTS every later segment one place along the sweep --
    # the operation a per-tile rule cannot express, because by then the later tiles are already
    # committed. Segments are ordered by the day each crop is first planted, so the crop the early
    # days live on gets the ground nearest the shed.
    #
    # Quadrant availability needs no explicit check. Total segment length after day `d` is exactly
    # the number of plants the schedule makes through day `d`, and the sweep is quadrant-major over
    # ground already bought, so the run can only reach ground the schedule itself has paid for.
    # A segment is sized to PEAK CONCURRENT tiles, never to the season total.
    #
    # Crops are not static. A tile is occupied from the day it is planted until the crop is
    # harvested off it, and then it is ground again -- so the same square carries wheat in week one
    # and melon in week three. Reserving each crop its whole-season count was the first thing built
    # here and it is simply wrong arithmetic: 79 plants over the season claimed all 100 squares,
    # because every replant was given fresh ground instead of the ground it was replacing.
    #
    # Pens are the opposite and that is why they are allocated above, permanently. A pen is a
    # structure; it is never harvested and never hands its square back.
    length = collections.Counter()
    for crop in {c for d in sorted(sched) for c in ((sched[d] or {}).get("plants") or [])}:
        held = _occupies_for(crop)
        for day in sorted(sched):
            live = sum(collections.Counter((sched[d] or {}).get("plants") or [])[crop]
                       for d in range(max(0, day - held + 1), day + 1) if d in sched)
            length[crop] = max(length[crop], live)

    first_day = _first_day_of(sched, "plants")
    owned_end = quads_owned(sum(int((sched[d] or {}).get("land") or 0) for d in sorted(sched)))
    ground = [t for t in RT.field_order(owned_end) if t not in taken]
    at = 0
    for crop in sorted(length, key=lambda c: (first_day.get(c, 0), c)):
        for t in ground[at:at + length[crop]]:
            layout[t] = ("PLANT", crop)
            taken.add(t)
        at += length[crop]

    return layout


def as_matrix(layout, board_size=R.BOARD_SIZE):
    """The layout as a printable grid. Diagnostics only -- nothing plans off this."""
    rows = []
    for y in range(board_size):
        row = []
        for x in range(board_size):
            v = layout.get((x, y))
            if v is None:
                row.append(" . ")
            elif v[0] == "BUILD":
                row.append(v[1][:1].upper() + "* ")
            else:
                row.append(v[1][:2].lower() + " ")
        rows.append("".join(row))
    return "\n".join(rows)
