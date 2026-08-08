"""One day as what it actually is: a scheduling problem with constraints. Cover the job list.

    resources     k hands, each with `budget` turns (`TURNS_PER_DAY - hour - 1`)
    jobs          one per tile that wants work today; its length is how many ops it wants
    travel        Manhattan distance on the grid, paid between consecutive stops
    a depot stop  needed once per unit if its jobs need anything drawn from the shed
    a return leg  needed if the unit ends the day holding something sellable
    objective     COVER EVERY JOB. Ties broken on fewer turns.

**There is no price table in here, and that is the point.** The board is known in advance -- what is
planted where, which day each thing needs water, which pens need feed -- and Seb's tape proves a day
of it is coverable. So the question a day poses is not "which job is worth most", it is "can thirteen
hands cover forty-six jobs in twenty-three turns each". Every job counts 1.

The previous answer to this was `router.plan_routes`, which ranks candidates by `prize / marginal
cost` out of a derived price table, with MANDATORY and CRITICAL tiers layered on to stop the ratio
misbehaving. Measured over 12 seasons, a local search that got BETTER at that objective lost $34,816,
and the arm restricted to the mandatory tier alone lost most of all -- because "reach this pen" is
priced as lexicographically infinite while a $400 animal yielding ~$160/day plainly is not, so it
displaces four real jobs to serve one. The prizes and the tiers exist to let a per-turn router decide
in a millisecond. Neither is needed to answer a covering question.

Two moves, and no more:

    GREEDY    insert the job with the cheapest feasible insertion anywhere, and repeat
    REPAIR    for a job that fits nowhere, take one job OFF a unit, put the new one on, and
              re-home the displaced one on another unit -- accepted only if coverage rises

Deterministic by construction: every tie is broken on a total order, there is no randomness and no
wall-clock cutoff, so the same board always yields the same tours.
"""

import collections

from . import routines as R

TPD = R.TURNS_PER_DAY
SHED = tuple(R.shed_access_tiles())

#: Ops whose item is drawn at the shed before the job can be done.
DRAWN = ("FEED", "FERTILIZE", "PLACE", "BUILD")

#: Ops that put a sellable item into the unit's hand. The market only ever reads the SHED, so a tour
#: that ends holding one has not banked it -- it arrives overnight, a turn too late to sell.
YIELDING = ("HARVEST", "COLLECT_FERTILIZER")

#: Ops that are CONSTRAINTS rather than candidates: skip one and something is destroyed outright.
#:
#: `consecutive_unfed >= 2` removes the animal and leaves the structure (`kaggriculture.py:786`), so
#: a missed FEED is not "one job's worth of value forgone today" -- it is a $400-$500 asset written
#: off plus every remaining day of its production. That is a fact about the rules, not an estimate,
#: which is why it can live in a file with no price table in it.
#:
#: **Covering by COUNT alone cannot see this, and that is a real limit of the framing rather than a
#: bug.** A day is not independent of the next one: three cheap waters and one lost cow score +3 -1
#: on today's job count and are catastrophic across the fortnight the cow would have milked. So
#: required work is covered first, and only then is the rest of the day packed around it.
#:
#: SURVIVAL WATER IS DELIBERATELY NOT HERE. Two dry days does turn a tile into a WEED, which really
#: is the crop equivalent, and promoting it MEASURED -$2,804 over twelve seeds: a pass holding
#: fourteen pens AND every thirsty tile cannot triage, and watering lost more than feeding gained.
#:
#: **A FLAT `required` IS NOT ENOUGH, AND THE TAPE IS THE PROOF.** Seed 11, weeds off, whole season
#: (`data/logs/do_sebs_animals_die.log` against `data/logs/where_wheat_goes.log`):
#:
#:                     FEED ops   pens at end   animals lost
#:     Seb                  388            19              0
#:     ours                 387            18              1
#:
#: We feed as often as he does. He misses feeds too -- day 19 he feeds 16 of 19 pens -- and loses
#: nothing, because `consecutive_unfed >= 2` is what kills (`kaggriculture.py:786`) and he never
#: misses the SAME animal on two consecutive days. So the quantity was never the problem and neither
#: was the wheat: it is WHICH animal gets skipped.
#:
#: A flat `required` makes that worse rather than better. With nineteen equally-required feeds and
#: room for seventeen, the solver drops two arbitrarily -- possibly the same two it dropped
#: yesterday. `at_risk` is the discrimination that fixes it, and it is still a rule and not a price:
#: fed yesterday, may slip; missed yesterday, may not.
REQUIRED_OPS = ("FEED",)

#: Whether a job the greedy could not place gets a second chance by displacing one that is placed.
#: Off leaves the plain cheapest-insertion greedy, which is what makes the repair attributable --
#: and what a test asserts against, so a green suite with it disabled fails loudly instead of quietly.
REPAIR = True

#: Whether covered jobs are shuffled between hands to CONSOLIDATE the leftovers before giving up.
#:
#: Spare turns are not spare capacity unless they are in one place. Measured on Seb's day-17 board
#: with our planner (`data/logs/why_no_harvest.log`), at hour 16: nine HARVEST jobs offered, three
#: covered, eight jobs uncovered, and **sixteen spare unit-turns** -- across thirteen hands, so 1.2
#: each, and nothing costs 1.2 turns. Every tour ends with a remainder too small to use, and over the
#: day that is 29 PASS turns against the tape's 3 while 28 tiles sit holding ripe produce.
#:
#: So this move changes nothing about WHICH jobs are covered, only where they sit: relocate a job to
#: whichever hand serves it most cheaply, accepted only on a strict fall in total turns. That pools
#: the remainders, and the insertion pass that follows can then spend them. Coverage never drops,
#: which is also why it terminates -- total cost is bounded below and strictly decreases.
COMPACT = True


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Job:
    """One tile and every op it wants today. `turns` is how long standing there costs."""

    __slots__ = ("tile", "ops", "turns", "needs", "required", "at_risk", "only")

    def __init__(self, tile, ops, needs=None, at_risk=False, only=None):
        self.tile = tuple(tile)
        self.ops = [tuple(o) for o in ops]
        # **A PLANT is two turns, not one, and the second one is not optional.** A tile is created at
        # `consecutive_unwatered = 1` and weeds at 2 (`kaggriculture.py:753`), so a planting that is
        # not watered the same day is a seed and two turns thrown away. Costing it at one turn let the
        # day-0 plan put its seventeenth planting on hour 23 with nothing left to water it -- measured
        # in `test_the_whole_day_zero_schedule_is_executed`, one WEED at (1,1) from a PLANT at h23.
        # The executor already emits the WATER on the next turn because `_live_ops` re-derives at the
        # tile; what was missing is the planner KNOWING it has to.
        self.turns = len(self.ops) + (1 if any(o == "PLANT" for o, _i in self.ops)
                                      and not any(o == "WATER" for o, _i in self.ops) else 0)
        self.needs = collections.Counter(needs) if needs is not None else collections.Counter(
            i for o, i in self.ops if i and o in DRAWN)
        self.required = any(o in REQUIRED_OPS for o, _i in self.ops)
        #: Skipping this one TODAY destroys something outright. A pen fed yesterday may slip a day;
        #: one that missed yesterday may not, and nor may a tile one dry day from weeding. Set from
        #: the BOARD (`consecutive_unfed`/`consecutive_unwatered`), never from a price.
        self.at_risk = bool(at_risk)
        #: Restrict this job to ONE hand, by index. Almost every job can be done by whoever is
        #: nearest, but a DELIVER cannot: only the hand actually holding the wool can carry it to
        #: the shed. `None` means anyone.
        self.only = only

    @property
    def service(self):
        """Alias for `turns`, so a `Job` is a drop-in for `router.Node` in the executor."""
        return self.turns

    def places(self):
        """Animals this job takes out of the shed. One COW cannot fill two pens."""
        return collections.Counter(i for o, i in self.ops if o == "PLACE")

    def yields(self):
        return any(o in YIELDING for o, _i in self.ops)

    def __repr__(self):
        return f"Job{self.tile}{[o for o, _i in self.ops]}/{self.turns}t"


def draws(route, carry=None):
    """What this route must pick up at the depot, after what the unit already carries.

    The TURN cost of the depot stop is the number of distinct ITEMS, not their total: `PICKUP` is
    unbounded (`kaggriculture.py:340`), so one turn draws the whole day's wheat and a unit servicing
    fourteen pens needs one shed trip, not fourteen.
    """
    held = collections.Counter(carry or {})
    need = collections.Counter()
    for j in route:
        for item, qty in j.needs.items():
            if qty > held[item]:
                need[item] += qty - held[item]
            held[item] = max(0, held[item] - qty)
    return need


def turns(start, route, carry=None, depots=SHED, deliver=True):
    """Exact turns one unit spends walking `route` in this order. The only cost model in the file.

    `deliver` is whether the walk back to the shed is charged. It normally must be: the market reads
    the SHED and nothing else, so produce still in a hand is unsold. But at the very end of the day
    that reserve buys nothing -- `_drop_inventories_to_shed` (`kaggriculture.py:812`) empties every
    hand into the shed at the rollover, so a last-turn HARVEST banks itself overnight for free, while
    reserving a walk home for it just refuses the harvest outright.

    Measured on Seb's day-17 board: a full melon UNDER THE FARMER'S FEET at hour 23 costs 1 turn to
    take and was priced at 2 -- one for the op, one for a walk home there was no time to make -- so
    it was left standing. Nine of thirteen hands passed that hour with five ripe harvests offered.
    """
    if not route:
        return 0
    need = draws(route, carry)
    pos, total = start, 0
    if need:
        home = min(depots, key=lambda c: (dist(c, start), c))
        total += dist(start, home) + len(need)
        pos = home
    for j in route:
        total += dist(pos, j.tile) + j.turns
        pos = j.tile
    if deliver and any(j.yields() for j in route):
        total += min(dist(pos, d) for d in depots)
    return total


def cover(units, jobs, budget, depots=SHED, carry=None, supply=None, deliver=True):
    """Cover as many jobs as the crew can reach. Returns `(routes, uncovered)`.

    `routes` is `{unit_index: [Job, ...]}` in visiting order; `uncovered` is the jobs no unit could
    take. `supply` caps how many animals may be drawn from the shed across the whole plan.
    """
    depots = tuple(depots) or SHED
    carry = carry or {}
    routes = {u: [] for u in range(len(units))}
    left = list(jobs)
    stock = collections.Counter(supply) if supply is not None else None
    booked = collections.Counter()

    def load(u):
        return carry.get(u) or {}

    def cost(u, route):
        return turns(units[u], route, load(u), depots, deliver)

    used = {u: 0 for u in range(len(units))}

    def slot(u, j, base, limit=None):
        """Cheapest position for `j` on unit `u`'s `base` route within `limit` turns, `(cost, index)`."""
        if j.only is not None and j.only != u:
            return None                 # this hand is not carrying it, so it cannot deliver it
        cap = budget[u] if limit is None else limit
        best = None
        for i in range(len(base) + 1):
            c = cost(u, base[:i] + [j] + base[i:])
            if c <= cap and (best is None or c < best[0]):
                best = (c, i)
        return best

    def claim(u, j):
        """Animals this job makes unit `u` draw FROM THE SHED, after what it already carries.

        **A hand carrying the cow claims nothing.** `Job.places()` is static and cannot know that,
        and netting it off is not optional: the moment a unit draws the animal the shed reads zero,
        so an un-netted claim makes the PLACE permanently unassignable and the hand carries the
        beast to dusk beside an empty pen. Measured on seed 11 day 1 -- cow in the shed at h1, drawn
        at h4, four empty pens standing free, no PLACE all day, dropped back overnight and finally
        placed on day 2 h9. One animal-day lost, and it repeats, which is the whole of `cow 7/8`.
        """
        held = collections.Counter(load(u))
        return collections.Counter({i: q - held[i] for i, q in j.places().items() if q > held[i]})

    def affordable(new_places):
        """Does this many animal draws still fit what the shed holds?"""
        if stock is None:
            return True
        return all(booked[i] + q <= stock[i] for i, q in new_places.items() if q > 0)

    # ------------------------------------------------------------------------------------- greedy
    # Cheapest insertion, globally, one job at a time -- but UNDER A FAIR-SHARE CAP that relaxes in
    # `len(units)` steps.
    #
    # **Global cheapest-insertion on its own packs one vehicle and starves the rest, and that is
    # measured, not theoretical.** Units are hired for the whole day whether they move or not, so an
    # idle unit's turns are free and the scarce resource is per-unit TIME, not total walking. On a
    # serpentine field the difference is decisive: appending the next tile to the unit already
    # standing on the previous one costs 2, while starting an idle unit from the shed costs 6, so the
    # plain rule always does the former. Day 0 of seed 11 measured `10, 9, 2, 0, 0` across five units
    # -- two saturated against a budget of 21, two given nothing -- and six of twenty-one jobs never
    # started. Leaving this cap out of the first version of this file reproduced it exactly: 2,173
    # jobs uncovered over a season and $117,732 -> $84,702 (`data/logs/cover_ab.log`).
    #
    # Pure round-robin overcorrects the other way -- it hands a job to a distant idle unit even when a
    # loaded one is standing beside it, measured at 776 idle turns converted into 742 extra MOVES for
    # no extra work. So the cap only bites once a unit reaches its share of the day, and the final
    # pass has `cap == budget`, so nothing is left uncovered that the plain rule would have covered.
    n_u = max(1, len(units))

    def greedy(pool):
        for step in range(1, n_u + 1):
            cap = {u: budget[u] * step / n_u for u in range(len(units))}
            while pool:
                best = None
                for j in pool:
                    for u in range(len(units)):
                        if cap[u] - used[u] < j.turns:
                            continue               # cannot fit even standing still: skip the scan
                        # Per UNIT, not per job: whether a placement is affordable depends on which
                        # hand does it, because a hand already carrying the animal draws nothing.
                        if not affordable(claim(u, j)):
                            continue
                        got = slot(u, j, routes[u], cap[u])
                        if got is None:
                            continue
                        key = (got[0] - used[u], u, j.tile, got[1])
                        if best is None or key < best[0]:
                            best = (key, j, u, got[1], got[0])
                if best is None:
                    break                          # nothing more fits under this cap; relax it
                _k, j, u, i, c = best
                routes[u].insert(i, j)
                used[u] = c
                booked.update(claim(u, j))
                pool.remove(j)
                left.remove(j)

    # Three passes, and the FIRST one is the whole point. See `REQUIRED_OPS`: an animal that missed
    # yesterday dies tonight if it misses again, while one fed yesterday can slip a day for free --
    # which is exactly how the tape feeds 16 of 19 pens on day 19 and loses nothing. A flat
    # `required` cannot express that and drops the same animal twice.
    greedy([j for j in left if j.at_risk and j.required])       # an animal that dies tonight
    greedy([j for j in left if j.required and not j.at_risk])    # the rest of the herd
    greedy([j for j in left if j.at_risk and not j.required])    # a tile that weeds tonight
    greedy([j for j in left if not j.required and not j.at_risk])

    # ----------------------------------------------------------------------------------- compact
    # Pool the leftovers, then spend them. See `COMPACT`: sixteen spare turns spread one apiece
    # across thirteen hands is not capacity, and every tour ends with exactly that kind of remainder.
    # Relocation is coverage-neutral by construction -- the job moves, it never leaves -- so this can
    # only ever make room, and each accepted move strictly lowers total turns, which bounds the loop.
    if COMPACT:
        moving = True
        while moving:
            moving = False
            for u in range(len(units)):
                for j in list(routes[u]):
                    rest = [x for x in routes[u] if x is not j]
                    without = cost(u, rest)
                    best = None
                    for v in range(len(units)):
                        base = rest if v == u else routes[v]
                        got = slot(v, j, base)
                        if got is None:
                            continue
                        gain = ((used[u] - got[0]) if v == u
                                else (used[u] + used[v]) - (without + got[0]))
                        if gain > 0 and (best is None or gain > best[0]):
                            best = (gain, v, got[1], got[0])
                    if best is None:
                        continue
                    _g, v, i, c = best
                    if v == u:
                        routes[u] = rest[:i] + [j] + rest[i:]
                        used[u] = c
                    else:
                        routes[u] = rest
                        used[u] = without
                        routes[v].insert(i, j)
                        used[v] = c
                    moving = True
        # The turns that freed up are only worth having if something gets done with them.
        greedy([j for j in left if j.at_risk and j.required])
        greedy([j for j in left if j.required])
        greedy([j for j in left if j.at_risk])
        greedy(list(left))

    # ------------------------------------------------------------------------------------ repair
    # A job that fits nowhere is not necessarily unreachable -- it is often reachable from a unit
    # whose turns are already spent on work another unit could equally do. So: take one job OFF that
    # unit, put this one on, and find the displaced job a new home. Accepted only when coverage
    # rises, which is also why it terminates: coverage is bounded and never decreases.
    changed = REPAIR
    while changed and left:
        changed = False
        for j in sorted(left, key=lambda j: (not (j.at_risk and j.required), not j.required,
                                             not j.at_risk, j.tile)):
            done = False
            for u in range(len(units)):
                for m in list(routes[u]):
                    keep = [x for x in routes[u] if x is not m]
                    got = slot(u, j, keep)
                    if got is None:
                        continue
                    # `m` is DISPLACED, not dropped -- it is about to be re-homed on another unit, so
                    # it keeps its claim on the shed. Netting it out here let two units be sent for
                    # the same single COW.
                    if not affordable(claim(u, j)):
                        continue
                    # Re-home the displaced job, cheapest elsewhere. If nowhere takes it, this move
                    # is coverage-neutral at best and is refused.
                    home = None
                    for v in range(len(units)):
                        if v == u:
                            continue
                        alt = slot(v, m, routes[v])
                        if alt is not None and (home is None or alt[0] - used[v] < home[0]):
                            home = (alt[0] - used[v], v, alt[1], alt[0])
                    if home is None:
                        continue
                    _d, v, vi, vc = home
                    routes[u] = keep[:got[1]] + [j] + keep[got[1]:]
                    used[u] = got[0]
                    routes[v].insert(vi, m)
                    used[v] = vc
                    booked.update(claim(u, j))     # `m` moved unit; only `j` is newly claimed
                    left.remove(j)
                    changed = done = True
                    break
                if done:
                    break

    return routes, left


def from_nodes(nodes):
    """`router.Node` -> `Job`, keeping the node's own `needs` rather than re-deriving them.

    `build_nodes` decides WHICH jobs exist -- a thirsty tile offers water, a fed animal does not
    offer feed -- and that half is derived from the reference's mechanics and is worth keeping. What
    is dropped here is `prize` and `mandatory`: the RANKING, which is the half that measured wrong.
    `Node.needs` also carries the wheat a PLACE implies (`PLACE_DRAWS_FEED`), which is invisible in
    `ops` and would be lost by re-deriving.

    `at_risk` comes from `Node.critical`, which `animal_ops` sets from `consecutive_unfed >= 1`.
    That is a reading of the BOARD, not of the price table -- even though on the router's side it is
    expressed as a number so it can compete in a ratio.
    """
    return [Job(n.tile, n.ops, n.needs, at_risk=getattr(n, "critical", False)) for n in nodes]


def plan(units, jobs, budget, depots=SHED, carry=None, supply=None, deliver=True):
    """`cover`, in the shape `schedule_agent` already consumes from `router.plan_routes`."""
    depots = tuple(depots) or SHED
    routes, left = cover(units, jobs, budget, depots, carry, supply, deliver)
    out = {}
    for u, route in routes.items():
        load = (carry or {}).get(u) or {}
        need = draws(route, load)
        out[u] = dict(route=route, draw=need,
                      depot=(min(depots, key=lambda c: (dist(c, units[u]), c)) if need else None),
                      cost=turns(units[u], route, load, depots, deliver))
    return out, left
