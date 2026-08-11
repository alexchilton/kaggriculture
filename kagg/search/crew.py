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
#: **11, measured, 2026-08-10.** Same 12 recorded seats x 8 seeds, only this number moving:
#:
#:     ACTIVE_UNTIL_DAY =  7   0.271   (26W 70L)   new planner d0-d6, `cover.cover` after
#:     ACTIVE_UNTIL_DAY = 11   0.427   (41W 55L)   new planner d0-d10
#:     ACTIVE_UNTIL_DAY = 30   0.302   (29W 67L)   new planner all season
#:
#: So the whole-game extension is a LOSS as things stand: d11-d29 is territory this planner was
#: never tuned on, and it gives back more there than d7-d10 wins. 30 is the intended destination and
#: it is not ready; 11 is where it currently pays.
#:
#: **30 as of 2026-08-11, Alex's call, with that loss on the record.** Two things changed under the
#: sweep above, and both cut against 11:
#:
#:   - It was measured against SEB-era opponents and a Seb-shaped schedule (WHEAT 24). The target is
#:     now Victor's (WHEAT 139), so the d11-d29 the sweep priced is not the d11-d29 we now play.
#:   - The d11+ region is what `cover.cover` produces, and on the Victor baseline it OSCILLATES --
#:     idle unit-turns run 128, 11, 66, 12, 100, 8, 101 across d10-d16 against his 78, 57, 39, 48,
#:     38, 23, 49, with watering swinging 18, 58, 21, 45, 21, 43, 31 against his 43, 41, 46, 27, 45,
#:     35, 59. A tile weeds after two days unwatered, so a field watered on that rhythm sits on the
#:     threshold, and our first weed lands on d12 against a tape that never weeds once.
#:
#: So 11 is not a verdict that the sweep planner is worse late; it is a verdict that it was worse
#: late THERE. Re-measure on the Victor grid before treating either number as settled.
ACTIVE_UNTIL_DAY = 8

#: Days OUTSIDE the threshold that still use the crew planner.
#:
#: **d10 is not an ordinary day and must not be planned like one.** It is the third parcel plus
#: fourteen hires. Under `cover.cover` it stranded TWO hands for all 24 turns, bought six of a
#: twelve-wheat row, and read `pass 134/78`. The crew planner handles it.
#:
#: Measured over d0-d16 on the Victor grid, seed 11 -- final bank, weeds and strawberry tiles at
#: d16, the d8 placement, and moves per work op against the tape's 0.97:
#:
#:     lawn<30 (was)   $15,669   17 weeds   24/36   place 1/2   mv/wk 1.23
#:     lawn<11         $16,303    4 weeds   33/36   place 1/2   mv/wk 1.06
#:     lawn<9  + {10}  $15,341    3 weeds   33/36   place 1/2   mv/wk 1.05
#:     lawn<8  + {9,10}$19,123    4 weeds   32/36   place 2/2   mv/wk 1.09
#:     lawn<8  + {10}  $19,080    3 weeds   34/36   place 2/2   mv/wk 1.07   <- taken
#:
#: `lawn<8 + {10}` and `lawn<7 + {10}` are identical, so d7 plays the same under either planner.
#: `{9,10}` banks $43 more and gives back a weed and two strawberry tiles; money is not the
#: criterion. `lawn<9` losing the d8 placement is what says d8 specifically wants `cover.cover`.
ACTIVE_EXTRA_DAYS = frozenset({10})

#: Raise instead of returning a plan that leaves work on the board. A DEV INSTRUMENT: on a
#: workstation an uncovered day should stop the run and be looked at, and on Kaggle a raising agent
#: is marked errored and the season ends where it threw.
#:
#: **OFF as of 2026-08-10, because it is what everything is measured under.** It trips on day 8 at
#: seed 11 (`19 jobs left uncovered ... against crew budgets [24, 23, 23]`), so every grid, gate and
#: sweep in this session forced it off at runtime to get past d7. Leaving the file saying True while
#: no measurement ever ran that way is the worst of both -- and `build_planner_submission.py` refuses
#: to bundle a crew with it on, for the Kaggle reason above.
#:
#: Turn it back on deliberately, for a diagnostic run, not as a default.
STRICT_FEASIBILITY = False


class InfeasibleDay(AssertionError):
    """The planner could not fit a day that we know is playable.

    Carries the dropped jobs and the crew's budgets, because the useful question is never "did it
    fail" but "what did it think the work cost". `AssertionError` rather than a bare `Exception` so
    it reads as the broken invariant it is.
    """

    def __init__(self, day, uncovered, budget):
        self.day, self.uncovered, self.budget = day, list(uncovered), list(budget)
        ops = collections.Counter(o for j in self.uncovered for o, _i in j.ops)
        super().__init__(
            f"day {day}: {len(self.uncovered)} jobs left uncovered {dict(ops)}, "
            f"costing {sum(j.turns for j in self.uncovered)} job-turns against crew budgets "
            f"{self.budget}. Seb plays this day, so the pricing is wrong, not the day. "
            f"Tiles: {sorted(j.tile for j in self.uncovered)}")

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


def _fits(unit_pos, seq, held, depots, budget, wanted, rush, due=None):
    """Turns the tour costs, priced on the WORK -- `wanted` is deliberately not passed through.

    `wanted` is the day's still-owed sell row, and `materialise` uses it to insert a mid-tour trip
    to the shed whenever a hand is carrying enough of it to justify one. Sizing a lane through that
    charges the lane for deliveries that have not been decided yet, and charges them again and
    again as the lane grows. Measured on d4 at seed 11, where the row still owes 36 WHEAT:

        u1  lane 3 tiles   with wanted 23 turns (1 shed stop)   without 14
        u4  lane 4 tiles   with wanted 22 turns                 without 17
        u0  lane 4 tiles   with wanted 21 turns (3 shed stops)  without 19

    u1's three tiles are 14 turns of work quoted at 23, so the hand is declared full and refuses a
    tile ONE SQUARE away -- and then spends the day passing. That day drops 7 jobs and burns 64
    PASS turns at the same time, which is the contradiction this resolves.

    The deliveries are not lost by pricing them out here. `materialise` is called again on the lane
    that is actually committed, with `wanted` intact, and `cover.plan` adds the closing trip home
    afterwards out of the turns the tour did not spend. This is the same double charge in both
    places; only the sizing question is answered without it.
    """
    route = DP.materialise(unit_pos, seq, held, depots, None, False, rush)
    return DP.turns(unit_pos, route) <= budget


def _pack(unit_pos, run, held, depots, budget, wanted, rush, share=None, due=None):
    """Take as much of the front of `run` as fits, in order. The tail is returned to the caller.

    `share` caps the lane in job turns -- the hand's fair portion of the work still unassigned --
    so one hand cannot swallow the sweep and starve the hands behind it. `None` means uncapped,
    which is what the last hand of a crew gets.

    Deliberately NOT a knapsack. The run is a walk; dropping a tile out of its middle to fit a
    cheaper one later costs the walk between them and breaks the property the sweep was built for.
    A hand that finishes its block early idles -- Seb's do, on 2 of 8 hand-days at d0 and d3 -- and
    that is a better outcome than pulling it onto the far side of the board.
    """
    taken, acc = [], 0.0
    for i, job in enumerate(run):
        if share is not None and taken and acc + job.turns > share:
            break
        if not _fits(unit_pos, taken + [job], held, depots, budget, wanted, rush, due):
            break
        taken.append(job)
        acc += job.turns
    # `_fits` sized the lane on its work, so the deliveries are still to be paid for. Cost the lane
    # that is actually being committed, once, with the sell row in -- that is the route the executor
    # walks -- and give back tiles from the end until it fits. Trimming here rather than refusing
    # during growth is the whole point: growth asked the question once per candidate tile and
    # compounded a speculative ferry into every answer.
    while taken and DP.turns(unit_pos, DP.materialise(unit_pos, taken, held, depots, wanted,
                                                      False, rush, due=due)) > budget:
        taken.pop()
    return taken, run[len(taken):]


#: Order the ops of one tile must be taken in. A pen is BUILT, then FILLED, then FED -- all on the
#: same square, and nothing else in the plan orders them. Lower sorts first.
OP_ORDER = {"BUILD": 0, "PLACE": 1, "FEED": 2, "CARE": 3, "COLLECT_FERTILIZER": 4,
            "HARVEST": 5, "PLANT": 6, "WATER": 7}


def _tile_rank(job):
    return min((OP_ORDER.get(o, 9) for o, _i in job.ops), default=9)


def cover(units, jobs, budget, depots=DP.SHED, carry=None, supply=None, deliver=True, wanted=None,
          day=None, rush=False, due=None):
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
                                                    wanted, False, rush, due=due))

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
    # **This split is known to be mis-weighted and is the next thing to fix.** Job turns omit the
    # walk and omit the shed ferries `materialise` inserts when a hand fills with harvest -- the
    # same blind spot that made `_split` and `_fits` wrong. Herd work sits on the shed's doorstep
    # and is cheap per op; crop work has to be carried. So proportioning by job turns over-crews the
    # cheap side: on d4 it gives 3 hands to 24 job turns of pen work and 3 to 31 job turns of crop
    # work whose materialised cost is nearer 94.
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

    def run_crew(tiles, hands, risk_first, far_first=False, mop=False):
        if not tiles or not hands:
            uncovered.extend(j for t in tiles for j in at[t])
            return
        seq = serpentine(tiles, depots[0])
        if far_first:
            # **Sweep from the far edge home, not from the shed out.** `serpentine` orders rows by
            # distance from the shed, and the pens sit ON the shed -- so a single pooled sweep in
            # that order makes every hand meet the pen block first, spend its budget there, and
            # drop the far crop edge. Reversing keeps the boustrophedon contiguous (a reversed walk
            # is still a walk) and puts the tiles that nobody can reach in front of the tiles that
            # everybody passes.
            seq.reverse()
        if risk_first:
            # A pen that missed yesterday dies tonight, so it leads regardless of where it sits in
            # the sweep. Everything else keeps the sweep order behind it.
            seq.sort(key=lambda t: not any(j.at_risk for j in at[t]))
        ordered = [j for t in seq for j in at[t]]
        # **A lane is cut to what its hand can walk.** No lane sizes are decided in advance: the
        # nearest free hand takes as much of the remaining sweep as its budget carries, and the next
        # hand resumes on the job it stopped at.
        #
        # Sizing lanes first, by equal job turns, was wrong. A run's real cost is its job turns PLUS
        # its walk PLUS the shed ferries `materialise` inserts when a hand fills up with harvest,
        # and none of that is in `job.turns`. Runs of equal weight therefore cost wildly different
        # numbers of turns, the expensive ones overflow, and `_pack` returned the tail straight to
        # `uncovered` -- ten crop ops binned on d4 at seed 11, exactly that day's `harvest 10/14`
        # and `water 11/17`.
        # **A hand comes BACK for a second lane.** Measured on d4, seed 11, before this loop cycled:
        #
        #     u0 used 15/24 spare  9      u1 23/23 spare  0      u2 12/23 spare 11
        #     u3 used 21/23 spare  2      u4 22/23 spare  1      u5 11/23 spare 12
        #     UNCOVERED  WATER 6, HARVEST 3   tiles (0,0) (0,1) (1,0) (2,0) (3,0) (4,0)
        #
        # **32 spare turns across three hands, and nine job-turns binned.** `pool.remove(pick)` took
        # each hand out and never put it back, so once every hand had had one lane the loop exited
        # and the rest of the sweep went straight to `uncovered` -- not because anyone was out of
        # turns, but because the crew had run out as a LIST. u2 stopped after two tiles at 12/23 and
        # u5 after two at 11/23, both capped by `share` and neither ever asked again.
        #
        # That is also the shape the tape has and we did not. Seb puts six of his seven hands on crop
        # work on d4, and three of them -- u0, u5, u6 -- do their pens and THEN go and water. There
        # is no herd crew and crop crew in his day; there are hands that finish one thing and pick up
        # another. A second pass is what that looks like from inside this planner.
        #
        # `share` is deliberately dropped after the first pass. It exists to stop the first hand
        # taking eight tiles and starving the last one (`place 4/4 -> 3/4`, a sheep left in the
        # shed), and by the time every hand has had a lane that balance has already been struck --
        # holding the cap past that point stops being fairness and becomes the loss above.
        # `mop` starts the loop already past its first pass: the share cap is a fairness rule for
        # dividing work nobody has yet, and a mop-up is dividing work everybody has already refused.
        # It also switches on the seat/spare arithmetic below, which is what a hand that already
        # walked a tour needs.
        i, first = 0, not mop
        while i < len(ordered):
            pool = [u for u in hands if budget[u] - used[u] > 0]
            if not pool:
                break
            start_of_pass = i
            while pool and i < len(ordered):
                head = ordered[i].tile
                pick = min(pool, key=lambda u: (DP.dist(units[u], head), u))
                pool.remove(pick)
                # **A fair share of what is LEFT, and never more than the hand can walk.**
                # Feasibility alone is not enough: letting each hand take everything that fits gave
                # u0 eight tiles at 24/24 and left the last hand of six with no lane at all, which
                # on d0 piles the pens onto hands that run out of turns before the animals go in --
                # `place 4/4 -> 3/4` and a sheep left standing in the shed. Balance alone is not
                # enough either; that is the equal-weight cut this replaces. The share is recomputed
                # against the REMAINING work each time, so a hand that could not walk its share
                # hands the surplus on rather than dropping it, and the last hand is capped only by
                # its budget.
                share = None
                if first and pool:
                    share = max(1.0, sum(j.turns for j in ordered[i:]) / (len(pool) + 1))
                # **On a second lane the hand starts where it stopped, on the turns it has left.**
                # `_pack` prices a tour from a start square against a budget, and after the first
                # pass neither of those is still `units[pick]` and `budget[pick]` -- pricing the
                # mop-up from the hand's dawn position would hand it a full day it has already
                # spent. `commit` then re-materialises the WHOLE of `work[u]` from the dawn square
                # and rewrites `used[u]`, so the true cost is still measured end to end here; this
                # only decides how much is offered.
                #
                # `held(pick)` is the dawn carry either way, which on a second lane is an
                # approximation -- the hand may have picked up or dropped since. It is the same
                # approximation the first pass makes and it is not made worse by cycling.
                seat = units[pick]
                spare = budget[pick]
                if not first and work[pick]:
                    seat = work[pick][-1].tile
                    spare = max(0, budget[pick] - used[pick])
                taken, _rest = _pack(seat, ordered[i:], held(pick), depots, spare,
                                     wanted, rush, share, due)
                # **The budget is checked against the WHOLE tour, because that is what gets walked.**
                # Pricing the mop-up from `seat` on the turns left over is how much to OFFER; it is
                # not the cost. The hand walks one tour from its dawn square, and `materialise`
                # re-derives every depot stop over the combined sequence -- a ferry the first lane
                # did not need can appear once the second lane's harvest is added to the same hand.
                #
                # Skipping this check measured d4 `u2 33/23` and `u5 28/23`: the crop rows covered,
                # and covered by tours ten and five turns longer than the day. A hand that runs out
                # mid-tour does not do a shortened version of the plan, it silently stops, so an
                # over-budget lane is not an optimistic plan -- it is a plan whose tail is fiction.
                # **Reserving the walk home on the mop-up was tried and is a LOSS. Do not
                # restore it without new evidence.** `deliver=True` here, measured against the tape
                # on the 17-day grid at seed 11:
                #
                #                     d4 water  d4 sell  d6 feed  d6 care  d4 money
                #     tape                  17       55        7        7      1063
                #     mop-up                15       34        5        5       115
                #     mop-up + deliver      13       38        3        3       395
                #
                # It buys money back and gives up the watering the pass exists for. The produce
                # problem it targets is real -- see the note below -- but charging the closing trip
                # up front refuses jobs, which is the same trade already recorded at `cover.cost`
                # (d10-d16, $1,722). The fix has to be to choose different WORK, not to price the
                # same work more pessimistically.
                while taken:
                    trial = work[pick] + taken
                    if DP.turns(units[pick],
                                DP.materialise(units[pick], trial, held(pick), depots,
                                               wanted, False, rush, due=due)) <= budget[pick]:
                        break
                    taken.pop()
                if taken:
                    commit(pick, taken)
                    i += len(taken)
            # No hand took anything this pass, so another pass would offer the same jobs to the
            # same hands and get the same answer. Stop rather than spin.
            if i == start_of_pass:
                break
            first = False
        uncovered.extend(ordered[i:])

    # **Measured 2026-08-10: one merged sweep is a trade, not a win, and the reason is ORDER.**
    # Pooling every tile into one serpentine and letting each hand take what it can reach makes the
    # herd rows exact -- d4 and d6 both `feed 7/7` and `care 7/7`, d0's missing care lands -- because
    # a hand collects a pen on its way past instead of a second crew walking out for it.
    #
    # It also destroys the crops: d2 `water 17/17 -> 12/17`, d3 `14/14 -> 9/14`, d4 `harvest 11/14
    # -> 6/14` and `sell 46/55 -> 19/55`, and the d4 parcel is never bought at all (`tiles 50/50 ->
    # 25/50`). `serpentine` orders rows by distance from the shed and the pens sit ON the shed, so
    # in a single sweep every hand meets the pen block first, spends its budget there, and the far
    # crop edge is what falls off the end. Splitting by type was accidentally ring-fencing hands for
    # the crops.
    #
    # So the partition is not what to keep -- the protection it gave the crops is. Do not restore
    # the merge without an ordering that reaches the far edge first.
    # **Measured 2026-08-10: both single-sweep variants lose. Do not restore either without new
    # evidence.** Pooling every tile into one serpentine and cutting it by reachability makes the
    # herd rows exact -- d4 and d6 `feed 7/7` and `care 7/7`, d0's missing care lands -- because a
    # hand collects a pen on its way past instead of a second crew walking out for it. It also
    # destroys the crops: d2 `water 17/17 -> 12/17`, d4 `harvest 11/14 -> 6/14`, `sell 46/55 ->
    # 19/55`, and the d4 parcel is never bought (`tiles 50/50 -> 25/50`).
    #
    # The diagnosis was ordering: `serpentine` runs shed-outward and the pens sit ON the shed, so
    # every hand meets them first and the far crop edge falls off the end. Reversing the sweep to
    # run far-edge-home was then measured too, and is worse again -- d0 `water 17/17 -> 12/17`,
    # d4 `harvest 4/14`, `sell 20/55`, d6 parcel gone -- because every lane then opens with a long
    # walk out and the shed trips land at the wrong end of the day.
    #
    # Note what the far-first run does to the tests in
    # `tests/test_a_lane_is_cut_to_what_its_hand_can_walk.py`: **all three pass.** Every crop job is
    # assigned and no hand is idle. Coverage is not the objective; executing the coverage is. A
    # green run there is necessary and nowhere near sufficient.
    # Everything already in `uncovered` at this point was refused for a STOCK reason, not a turns
    # reason: no animal in the shed to place, no seed to plant, nothing to feed with. Those refusals
    # are correct and the tape agrees with them -- d1 drops PLACE/FEED/CARE x3 against three empty
    # pens and one animal, and `place 1/1` matches Seb exactly. Only what the lane loop below bins
    # is a claim that the work does not FIT, which is the claim we know to be false.
    guarded = len(uncovered)
    run_crew(herd_tiles, herd_hands, risk_first=True)
    run_crew(crop_tiles, crop_hands, risk_first=False, far_first=True)

    # **A hand that finished its own crew's work goes and helps the other one.** This is NOT the
    # merged sweep ruled out above, and the difference is what makes it safe: the two crews are still
    # run first, separately, over their own tiles, so the crops keep every bit of the ring-fencing
    # that partition was worth. The mop-up only ever sees jobs BOTH crews have already given up on --
    # by this point they are otherwise on their way into `uncovered`, so the worst case is that
    # nobody can take them and we are exactly where we were.
    #
    # It is also the shape the tape has. On d4 Seb puts six of his seven hands on crop work and three
    # of them -- u0, u5, u6 -- work their pens and THEN go and water. He has no herd crew and crop
    # crew; he has hands that finish one thing and pick up another. Measured on our d4 before this:
    # u0 sat on 9 spare turns and u3 on 2 while six WATER and three HARVEST were binned, and no
    # amount of re-cutting the crop lanes could reach them, because u0 was in the wrong crew.
    left = uncovered[guarded:]
    if left:
        del uncovered[guarded:]
        # At-risk first for the same reason the herd crew leads with it: a pen that missed yesterday
        # dies tonight, and this is the last pass that can save it.
        run_crew(sorted({j.tile for j in left}), list(range(len(units))),
                 risk_first=True, mop=True)
    starved = uncovered[guarded:]

    # **A dropped job is a wrong constraint, not a full day. FAIL LOUDLY.** Alex's call, 2026-08-10.
    #
    # The day is feasible -- Seb plays it, on the same board, with the same crew. So when this
    # planner reports that a job will not fit, the arithmetic that priced it is wrong, and silently
    # binning the job hides that behind a plausible-looking grid. d4 is the worked example: 17 WATER
    # jobs offered, 11 toured, 6 dropped, and the executor emits exactly the 11 it was handed -- so
    # the entire `water 11/17` row is priced here, not lost downstream.
    #
    # The known-wrong constraint is the shed ferry. `DP.materialise` reads `wanted` as "deliver
    # before the next job" and inserts a ~12-turn round trip per crop tile.
    #
    # The right rule is **deliver by the hour the cadence needs it**. `wanted` carries a quantity
    # and no deadline, so every unit reads as due immediately. It is not due immediately and it is
    # not due at the closing trip either -- "closing trip" is merely what d4 looks like, because d4's
    # sells are late. A day whose row needs goods at h6 genuinely does want a ferry; it wants one
    # sized to the shortfall at h6, not to the whole row.
    #
    # So the ferry is justified only for the quantity needed EARLIER than the hand would have
    # reached the shed anyway, and only by however much the shed is short at that hour. Measured on
    # his d4 tape: Seb makes no drop before h18 -- all six are the closing walk home, sells follow at
    # h18-h23 -- so d4's justified ferry quantity is zero and we charge a trip per tile for it.
    #
    # Temporary and deliberately disruptive: it turns a quiet 6-op shortfall into a stack trace
    # naming the day. Delete it once the ferry is priced against the closing trip.
    if STRICT_FEASIBILITY and starved:
        raise InfeasibleDay(day, starved, budget)

    return work, uncovered
