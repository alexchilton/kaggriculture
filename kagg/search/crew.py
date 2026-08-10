"""A dawn planner that hands each unit a contiguous block and does not re-rank it.

Drop-in for `cover.cover`: same signature, same `({unit: [Job, ...]}, uncovered)` return, so
`cover.plan` materialises the result unchanged and nothing downstream knows the difference.

**Why this exists.** The greedy in `cover.cover` ranks every job against every unit by marginal
insertion cost, so a unit's next stop is whatever scores best from where it now stands. That is a
good tour and a bad *day*: measured over a full season our crop tiles get watered in an oscillation
-- d11 waters 40 of 41 plants, d12 waters 13 of 52 while 136 unit-turns are spent PASSing, d13
waters 43 of 50, d14 waters 18 of 52 -- and 16 plants (14 strawberry, 2 melon) die of thirst, every
one of them after d9. A tile at `consecutive_unwatered = 0` prices low, so on the day after a full
watering nothing looks worth doing and the hands stand still; the next morning every tile is at 1,
everything is critical at once, and whatever the crew cannot reach in 24 hours weeds over.

**What was measured BEFORE writing this, and what it ruled out.** Two obvious explanations were
tested against Seb's tape (`91422988`) first, and both are wrong:

    role purity   ours 49% of hand-days mix crop and herd work; HIS is 52%. He mixes MORE.
                  So "a waterer must never be pulled onto a feed" is not the rule and a planner
                  built on it would be built on nothing.
    walking       ours 1.10 move-turns per work op; his 1.50. We already walk LESS than he does.

What is left, and what this module implements, is the thing visible in his routes and in nothing
else: **a hand is given a contiguous run of tiles at dawn and walks it in order.**

    d0  u6  spawn(4,5)  h03(3,4)PLANT h04(3,4)WATER  h06(2,4)PLANT h07(2,4)WATER
                        h09(1,4)PLANT h10(1,4)WATER  h12(0,4)PLANT h13(0,4)WATER
                        h15(0,3)PLANT h16(0,3)WATER  h18(0,2)PLANT h19(0,2)WATER

Down the column `y=4`, then along the row `x=0`. One block, one hand, no revisits, and a tile is
finished where it stands. Full analysis in `docs/how_sebs_planner_works_2026-08-10.md`.

**Scope.** `ACTIVE_UNTIL_DAY` gates it. It is 0 -- OFF -- until it has been measured day by day
against the tape; the days it is switched on for are the days whose grid has been read. d0-d3 is
where all four tapes agree op-for-op (they part at d4 h01, and only because the richer economy
affords an eighth hand), so it is the region where "correct" is a fact rather than an opinion.
"""
import collections

from . import cover as DP

#: Days `[0, ACTIVE_UNTIL_DAY)` are planned here; everything else falls through to `cover.cover`.
#: **d0-d6, Alex's call.** The 17-day grid at seed 11 against tape 91422988, this against 0:
#:
#:              d4 care  d4 water  d4 sell  d5 feed  d5 water  d6 feed  d6 land  d4 money
#:     off        5/7      16/17    28/55     7/4      13/14     6/7      1/1        21
#:     d0-d6      6/7      11/17    40/55     4/4      14/14     4/7      0/1       515
#:
#: d5 lands EXACTLY on both feed and water, d4 gains a care, twelve sells and $494. What it costs
#: is d4's watering and the d6 land parcel, and the parcel is NOT the planner's doing -- see the
#: wool note below. d0-d3 is byte-identical at every setting.
ACTIVE_UNTIL_DAY = 7

#: **The d6 land parcel slips for want of a WOOL sale, not for want of turns or money.** Traced
#: hour by hour at seed 11: Seb sells `WOOL 6` at h09 and `WOOL 6` again at h13, taking his bank
#: $5 -> $1,349, and buys the parcel at h13. We sell `WOOL 1` at h07 and `WOOL 5` at h19, so we
#: hold $47 at h13 and do not reach $1,400 until h23 -- by which point the day is over. The row is
#: `sells {'WOOL': 12}` and we do sell twelve; we sell them ten hours late. Same shape as the wheat
#: reserve fixed in b52e210: the right quantity at the wrong hour. It is a market-cadence defect
#: and it lives in the sell block, not here.

#: Ops that belong to the crop sweep. A tile carrying any of these is swept, not routed.
CROP_OPS = frozenset({"PLANT", "WATER", "HARVEST"})
#: Ops that belong to the herd circuit -- the pens, in one walk, with the wheat carried out and the
#: fertilizer carried back. `PICKUP`/`DROP` are not here: `materialise` inserts those.
HERD_OPS = frozenset({"FEED", "CARE", "COLLECT_FERTILIZER"})
#: Ops that change the board's structure. These pair up -- a PLACE is only legal on a pen that is
#: already built -- so they are assigned before anything else and always to one hand.
STRUCT_OPS = frozenset({"BUILD", "PLACE"})


def _class(job):
    ops = {o for o, _i in job.ops}
    if ops & STRUCT_OPS:
        return "struct"
    if ops & HERD_OPS:
        return "herd"
    if ops & CROP_OPS:
        return "crop"
    return "other"


def serpentine(tiles, shed):
    """Order tiles as a boustrophedon sweep, starting from the row nearest the shed.

    Rows are walked alternately left-to-right and right-to-left, so consecutive tiles in the
    ordering are adjacent on the board and a contiguous SLICE of the ordering is a contiguous WALK.
    That is the whole property the caller needs: it can then cut the list anywhere and each piece is
    still a sensible route.

    Sorting by raw `(y, x)` instead would make every row change a full-width jump back, which is
    exactly the walk the sweep exists to avoid.
    """
    sy = shed[1] if shed else 0
    rows = collections.defaultdict(list)
    for t in tiles:
        rows[t[1]].append(t)
    out = []
    for i, y in enumerate(sorted(rows, key=lambda y: abs(y - sy))):
        out.extend(sorted(rows[y], key=lambda t: t[0], reverse=bool(i % 2)))
    return out


def _split(ordered, k, weight):
    """Cut `ordered` into `k` contiguous runs of roughly equal weight.

    Contiguous is the point. Round-robin or nearest-unit assignment over the same tiles produces
    interleaved routes -- every hand crossing every other hand's block -- which is the thing being
    replaced.
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


def _fits(unit_pos, seq, held, depots, budget, wanted, rush):
    """Turns the tour costs once `materialise` has put the shed trips in. Same question `cover.cost`
    asks, asked the same way, so a run accepted here is a run the executor can actually walk."""
    route = DP.materialise(unit_pos, seq, held, depots, wanted, False, rush)
    return DP.turns(unit_pos, route) <= budget


def _pack(unit_pos, run, held, depots, budget, wanted, rush):
    """Take as much of the front of `run` as fits, in order. The tail is returned uncovered.

    Deliberately NOT a knapsack. The run is a walk; dropping a tile out of its middle to fit a
    cheaper one later costs the walk between them and breaks the property the sweep was built for.
    A hand that finishes its block early idles -- Seb's do, on 2 of 8 hand-days at d0 and d3 -- and
    that is a better outcome than pulling it onto the far side of the board.
    """
    taken = []
    for i, job in enumerate(run):
        if not _fits(unit_pos, taken + [job], held, depots, budget, wanted, rush):
            return taken, run[i:]
        taken.append(job)
    return taken, []


#: Order the ops of one tile must be taken in. A pen is BUILT, then FILLED, then FED -- all on the
#: same square, and nothing else in the plan orders them. Lower sorts first.
OP_ORDER = {"BUILD": 0, "PLACE": 1, "FEED": 2, "CARE": 3, "COLLECT_FERTILIZER": 4,
            "HARVEST": 5, "PLANT": 6, "WATER": 7}


def _tile_rank(job):
    return min((OP_ORDER.get(o, 9) for o, _i in job.ops), default=9)


def cover(units, jobs, budget, depots=DP.SHED, carry=None, supply=None, deliver=True, wanted=None,
          day=None, rush=False):
    """Assign every job to a unit as a contiguous block. Returns `(work, uncovered)`.

    **The unit of ownership is the TILE, not the op.** A pen's whole day -- build it, put the animal
    in, feed it, care for it, take the fertilizer -- belongs to one hand. That is not a stylistic
    choice; it is what makes the two orderings in this game hold without a rule to enforce them:

      - a PLACE is only legal on a pen that is already built, and the route is a visit ORDER, so a
        hand arriving at a square whose pen is not up yet reads bare ground and the stop is dropped
        silently, animal still in its hand;
      - an animal placed today must be FED today, and `build_nodes` cannot emit a FEED for a tile
        until an animal is standing on it, so the feed is invisible at plan time.

    The first cut of this module assigned by OP CLASS -- structural work first, then a herd walk,
    then the crop sweep -- and both pairings broke. Measured on the tape, d0-d3 with it switched on:
    `place 3/4` and one sheep never placed, `feed 3/4`, and by d3 the bank was $28 against $478 with
    the baseline planner scoring $480. Grouping by tile makes all of that a non-question.

    So the day is two crews over two sets of tiles:

    1. **The herd**, every tile carrying an animal op or a structure op, serpentined and cut into
       contiguous runs -- one run per herd hand. At-risk pens lead: `consecutive_unfed >= 2` removes
       the animal outright tonight.
    2. **The crops**, everything else, same treatment over the remaining hands.

    Crew sizes come from the work, not from a constant: hands are split in proportion to the turns
    each side is asking for, with at least one hand on the herd whenever there are animals.
    """
    depots = tuple(depots) or DP.SHED
    carry = carry or {}
    work = {u: [] for u in range(len(units))}
    used = {u: 0 for u in range(len(units))}
    uncovered = []
    stock = collections.Counter(supply) if supply is not None else None

    def held(u):
        return carry.get(u) or {}

    def commit(u, seq):
        work[u].extend(seq)
        used[u] = DP.turns(units[u], DP.materialise(units[u], work[u], held(u), depots,
                                                    wanted, False, rush))

    # ---- group every job onto its tile, in the order that tile's ops must be taken ---------------
    at = collections.defaultdict(list)
    for j in jobs:
        at[j.tile].append(j)
    for t in at:
        at[t].sort(key=_tile_rank)

    def is_herd(t):
        return any(_class(j) in ("herd", "struct") for j in at[t])

    herd_tiles = [t for t in at if is_herd(t)]
    crop_tiles = [t for t in at if not is_herd(t)]

    # **One animal fills one pen.** `build_nodes` prices a PLACE per destination tile and gates it
    # only on the shed holding one, so three empty pens and one COW produce three placements each
    # worth the full animal. Nothing below would notice; the second and third hands walk out and
    # come back with the animal still in hand.
    if stock is not None:
        keep = []
        for t in sorted(herd_tiles, key=lambda t: DP.dist(t, depots[0])):
            need = collections.Counter()
            for j in at[t]:
                need += j.places()
            if need and any(stock[a] < q for a, q in need.items()):
                # Drop only the placement; the pen may still want feeding or a build.
                at[t] = [j for j in at[t] if not j.places()]
                uncovered.extend(j for j in jobs if j.tile == t and j.places())
                if not at[t]:
                    continue
            else:
                stock -= need
            keep.append(t)
        herd_tiles = keep

    def weight(tiles):
        return sum(j.turns for t in tiles for j in at[t])

    # ---- how many hands go to each crew ----------------------------------------------------------
    n = len(units)
    hw, cw = weight(herd_tiles), weight(crop_tiles)
    if not herd_tiles:
        k_herd = 0
    elif not crop_tiles:
        k_herd = n
    else:
        k_herd = max(1, min(n - 1, round(n * hw / max(1.0, hw + cw))))

    # Herd hands are the ones nearest the shed: the circuit opens with a wheat pickup and closes with
    # a fertilizer drop, so a hand that starts at the depot is already on its route.
    order_by_shed = sorted(range(n), key=lambda u: (DP.dist(units[u], depots[0]), u))
    herd_hands = order_by_shed[:k_herd]
    crop_hands = order_by_shed[k_herd:]

    def run_crew(tiles, hands, risk_first):
        if not tiles or not hands:
            uncovered.extend(j for t in tiles for j in at[t])
            return
        seq = serpentine(tiles, depots[0])
        if risk_first:
            # A pen that missed yesterday dies tonight, so it leads regardless of where it sits in
            # the sweep. Everything else keeps the sweep order behind it.
            seq.sort(key=lambda t: not any(j.at_risk for j in at[t]))
        ordered = [j for t in seq for j in at[t]]
        runs = _split(ordered, len(hands), lambda j: j.turns)
        pool = list(hands)
        for run in runs:
            if not pool:
                uncovered.extend(run)
                continue
            pick = min(pool, key=lambda u: (DP.dist(units[u], run[0].tile), u))
            pool.remove(pick)
            taken, rest = _pack(units[pick], run, held(pick), depots, budget[pick], wanted, rush)
            if taken:
                commit(pick, taken)
            uncovered.extend(rest)

    run_crew(herd_tiles, herd_hands, risk_first=True)
    run_crew(crop_tiles, crop_hands, risk_first=False)

    return work, uncovered
