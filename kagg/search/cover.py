"""One day as what it actually is: a scheduling problem with constraints. Cover the job list.

    resources     k hands, each with `budget` turns (`TURNS_PER_DAY - hour`)
    stops         a tile and the work done standing on it -- SHED TRIPS INCLUDED
    travel        Manhattan distance on the grid, paid between consecutive stops
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


## A SHED TRIP IS A STOP

The first version of this file got that wrong, and it is worth stating why, because the mistake is
easy to make twice: it modelled a tour as a list of TILES TO WORK, and charged the shed trips inside
the cost function -- one notional draw at the front if anything needed drawing, one notional walk
home at the back if anything was harvested. Both numbers were right. Neither was a stop.

So nothing in a route ever said "be at the shed at this point", and the executor had nothing to walk
to. Getting produce to market was left to four separate opportunistic mechanisms -- a ferry, a drop
on any incidental depot visit, a sell-row drop, an end-of-tour return leg -- each firing off whatever
tile a unit happened to be standing on, and a fifth `draw` side-channel outside the route entirely
for the pickups.

Seed 11 day 6 is the bill. The row reads `WOOL: 12` and buys two COWs out of the proceeds. The tape
harvests at h0, drops and sells six at h2, harvests again at h2, drops and sells the last six at h5;
both cows are funded by hour five. We harvested at h4 and h10, then CARRIED ten wool through h11,
h12, h13, h14, h15, h16, h17, h18, dropped four at h19 and took six into the night. The bank sat on
$20 all day and the second cow slipped, which the whole rest of the season inherits.

Every input needed to plan that at dawn was on the board at dawn: which pens hold sheep, how much
each carries, and what the row wants. `harvest -> shed` is a plan, not a discovery.

Hence `materialise`: the search decides the WORK SEQUENCE, and the shed trips are derived from it
deterministically and inserted as real stops, costed where they actually happen. A route is now
exactly what walking it costs, which is also what makes the search honest -- it was previously
optimising a number that no tour matched.


Three moves, and no more:

    GREEDY       insert the job with the cheapest feasible insertion anywhere, and repeat
    COMPACT      relocate covered jobs to pool the leftover turns, accepted only on a strict fall
    REPAIR       for a job that fits nowhere, take one job OFF a unit, put the new one on, and
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

#: Ops that put something into the unit's hand.
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

#: How much of today's still-owed SELL row a hand must be carrying before a MID-TOUR shed trip is
#: planned for it. Below this the load rides to the end of the tour, which ends at the shed anyway.
#:
#: A trip is not free: `DROP` is all-or-nothing (`kaggriculture.py:333`), so it dumps the feed wheat
#: with the wool and the same stop has to draw the wheat back for the pens still ahead. That is one
#: turn plus one per distinct item, on top of the detour. Batching until the load justifies it is the
#: whole content of this constant.
#:
#: SET AT 6 BY MEASUREMENT, not by taste, and carried over from the mechanism this replaces: at 2 and
#: at 4 the trip takes its turns out of day 6's planting and `test_day_six_plants_every_tile_the_row_
#: asks_for` and `test_the_biggest_sale_takes_the_earliest_slot` both go red; at 6 and 8 they do not,
#: and day 6 orders both cows.
DELIVER_MIN = 6

#: Whether a hand is judged for a shed trip by what it CARRIES (True) or by what today's sell row
#: still owes (False, shipped). See the long note in `materialise` for the defect it targets, which
#: is real and measured: animal produce rides in a hand all day and reaches the shed only via the
#: rollover sweep, so we sell yesterday's production every day of the season.
#:
#: **OFF, because the obvious fix costs more than the defect.** Measured, seed 11, weeds off, d0-d16,
#: stacked on the day-12 stranded-feed fix:
#:
#:               money@d16   cows   work   idle
#:     both off     16,363    5/8   1273   1381
#:     this on      14,342    3/8   1198   1436
#:
#: The extra trips come straight out of work turns, and work turns are feeds. Delivering produce is
#: still the right objective -- what is wrong is paying for it with a whole extra walk. The version
#: worth trying next routes the drop into a stop the tour was ALREADY making, rather than adding one:
#: pens sit on shed-access tiles by design, so a herd tour stands on a depot at most of its stops and
#: the drop can be free. That is a different change to this one and needs its own measurement.
DELIVER_SURPLUS_NOT_THE_ROW = False


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Job:
    """One tile and every op it wants today. `turns` is how long standing there costs."""

    __slots__ = ("tile", "ops", "turns", "needs", "gives", "required", "at_risk", "funds", "only")

    #: Never a shed trip. `materialise` inserts those and everything downstream keys off this to tell
    #: the two apart -- a depot stop is not work, does not get claimed against an idle unit, and is
    #: not re-derived from its cell by the executor.
    depot = False

    def __init__(self, tile, ops, needs=None, gives=None, at_risk=False, only=None):
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
        #: What this job puts INTO the hand, by product. Predicted from the tile's `yield_units`
        #: before the day starts, which is the whole reason the delivery can be planned rather than
        #: discovered. An empty `gives` on a yielding job is a safe under-estimate: it only means the
        #: load is never judged big enough for a mid-tour trip, so it rides to the end of the tour.
        self.gives = collections.Counter(gives or {})
        self.required = any(o in REQUIRED_OPS for o, _i in self.ops)
        #: Skipping this one TODAY destroys something outright. A pen fed yesterday may slip a day;
        #: one that missed yesterday may not, and nor may a tile one dry day from weeding. Set from
        #: the BOARD (`consecutive_unfed`/`consecutive_unwatered`), never from a price.
        self.at_risk = bool(at_risk)
        #: This job's produce is what pays for today's shopping list. Set only on a day whose bill
        #: exceeds the bank (`schedule_agent.FUND_THE_DAY_WHEN_SHORT`), and it buys two things: the
        #: job is covered before the general pool, and its load goes to the shed as soon as it is in
        #: hand instead of batching to `DELIVER_MIN`. The purchases are queued behind that money, so
        #: on a short day this harvest is not one job among forty -- it is the day's first
        #: constraint, in the same sense a feed that dies tonight is.
        self.funds = False
        #: Restrict this job to ONE hand, by index. `None` means anyone, which is now the only value
        #: anything passes -- the pinned DELIVER job this existed for is gone, because a delivery is
        #: no longer a job at all. Kept because a future PLACE-the-animal-you-are-carrying job wants
        #: exactly this and the alternative is reinventing it.
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


class Depot:
    """A shed trip, as a stop in the tour like any other. Emitted by `materialise`, never searched.

    `drop` empties the hand into the shed; `pick` draws items back out. Both on one stop, in that
    order, because `DROP` is all-or-nothing (`kaggriculture.py:333`) -- a hand carrying wool for the
    market and wheat for three more pens cannot shed one without the other, so it sheds both and
    takes the wheat straight back. `PICKUP` is unbounded (`kaggriculture.py:340`), so the draw costs
    one turn per distinct ITEM and not one per unit: fourteen pens is one wheat pickup.
    """

    __slots__ = ("tile", "drop", "pick", "critical")

    depot = True
    needs = ()
    gives = ()
    required = False
    at_risk = False
    only = None

    def __init__(self, tile, drop=False, pick=None, critical=False):
        self.tile = tuple(tile)
        self.drop = bool(drop)
        self.pick = collections.Counter({i: q for i, q in (pick or {}).items() if q > 0})
        #: Whether this draw serves a job that dies TONIGHT if it is skipped (`Job.at_risk and
        #: Job.required` -- an animal one missed feed from escaping). Set by `materialise`, which
        #: alone knows which jobs the draw is FOR; the executor reads it to decide whether a shed
        #: that cannot fill the want right now is worth standing at and retrying, or worth walking
        #: away from as before. See the note where the executor reads it.
        self.critical = bool(critical)

    @property
    def turns(self):
        return (1 if self.drop else 0) + len(self.pick)

    @property
    def service(self):
        return self.turns

    @property
    def ops(self):
        out = [("DROP", None)] if self.drop else []
        return out + [("PICKUP", i) for i in sorted(self.pick)]

    def places(self):
        return collections.Counter()

    def yields(self):
        return False

    def __repr__(self):
        bits = (["DROP"] if self.drop else []) + [f"{i}x{q}" for i, q in sorted(self.pick.items())]
        return f"Shed{self.tile}[{'+'.join(bits) or '-'}]"


def nearest(depots, frm, to=None):
    """The depot cheapest to visit between `frm` and `to`. Ties broken on coordinates, so it is total."""
    if to is None:
        return min(depots, key=lambda c: (dist(c, frm), c))
    return min(depots, key=lambda c: (dist(frm, c) + dist(c, to), c))


def materialise(start, work, carry=None, depots=SHED, wanted=None, deliver=True, rush=False):
    """Turn a WORK SEQUENCE into the tour that actually gets walked, shed trips included.

    This is the whole of the day-planning model. The search above chooses which tiles a hand works
    and in what order; every shed trip is derived from that choice here, deterministically, and
    inserted as a real stop. Nothing is charged that is not in the returned route, and nothing in the
    returned route is uncharged.

    Three rules, in this order at each step of the sequence:

    1. **The hand cannot do the next job.** It needs an item it is not holding, so a stop is inserted
       before that job. The draw covers the whole REMAINDER of the sequence, not just the next job:
       `PICKUP` is unbounded, so one stop of one turn per item serves fourteen pens.
    2. **The hand is carrying enough of today's row to justify a trip.** See `DELIVER_MIN`. The stop
       drops everything and immediately re-draws whatever the rest of the sequence still needs.
    3. **The tour ends holding something.** A closing drop, if `deliver`.

    `deliver` is whether the closing trip is charged AT ALL. It normally must be: the market reads
    the SHED and nothing else, so produce still in a hand is unsold. But at the very end of the day
    that reserve buys nothing -- `_drop_inventories_to_shed` (`kaggriculture.py:812`) empties every
    hand into the shed at the rollover, so a last-turn HARVEST banks itself overnight for free, while
    reserving a walk home for it just refuses the harvest outright. Measured on Seb's day-17 board: a
    full melon UNDER THE FARMER'S FEET at hour 23 cost 1 turn to take and was priced at 2, so it was
    left standing while nine of thirteen hands passed that hour.
    """
    depots = tuple(depots) or SHED
    wanted = collections.Counter(wanted or {})
    held = collections.Counter(carry or {})
    work = list(work)

    # Suffix sums of what the remaining sequence draws, so rule 1 can ask "what does the rest of the
    # day need" in O(1) instead of rescanning. Computed once: `materialise` sits inside the innermost
    # loop of the greedy and is called O(jobs x units x positions) times per pass.
    after = [collections.Counter() for _ in range(len(work) + 1)]
    for i in range(len(work) - 1, -1, -1):
        after[i] = after[i + 1] + work[i].needs

    route, pos = [], tuple(start)
    for i, j in enumerate(work):
        short = collections.Counter({it: q - held[it] for it, q in after[i].items() if q > held[it]})
        # **Deliverable is the SURPLUS: what the hand holds that this tour will not itself CONSUME.**
        #
        # The consumption half is load-bearing and was learned the hard way -- the row's product and
        # the herd's dinner are the same thing. Seed 11 day 4 sells `WHEAT: 28` on a $28 bank, so
        # three wheat carried to three pens read as $75 of goods the market was waiting for:
        # `feed 7 -> 0`, `care 7 -> 0`, `drop 5 -> 13`, moves 80 -> 124, not one animal fed all day.
        # `after[i]` is what excludes it, and it excludes it for every item, which is why the second
        # condition below could be dropped without bringing that back.
        #
        # **It used to be gated on TODAY'S SELL ROW as well, and that was the bug.** `wanted` is
        # transcribed from Seb's board, so a product his row does not name contributed nothing here
        # and no shed trip was ever inserted for it -- however much of it the hand was carrying. It
        # then rode around until `_drop_inventories_to_shed` swept every hand into the shed at the
        # rollover (`kaggriculture.py:812`), after the market had closed. We sold yesterday's
        # production every day, all season. Measured, seed 11, weeds off:
        #
        #     d14 h6  shed 0 hand  6      that day's row asks MILK 0
        #         h13 shed 0 hand 15      fifteen milk carried around all day
        #     d15 h0  shed 15 -> SELL 15  exactly what the sweep left, against a row of 24
        #     d16 h0  shed  3 -> SELL  3  against a row of 24, which the tape fills
        #
        # and wool worse: the d16 row asks 19, the tape sells 19, we sold 0. Nothing blocked those
        # sales -- 60-95 free shed slots all day and an open market. We never carried it home.
        #
        # So the hand is judged by what it is CARRYING, not by what today's row happens to name.
        # `wanted` survives as a parameter because `plan` still uses it to decide what to draw BACK,
        # and because `Job.funds` reads the row to decide what to harvest FIRST on a thin day.
        #
        # No price list here, deliberately: `cover` ranks nothing and prices nothing, so "surplus"
        # is a count of items, not of dollars. `DELIVER_MIN` remains the only threshold.
        load = (sum(max(0, q - after[i][p]) for p, q in held.items() if q > 0)
                if DELIVER_SURPLUS_NOT_THE_ROW else
                sum(min(max(0, held[p] - after[i][p]), q)
                    for p, q in (wanted or {}).items() if q > 0))
        # **`DELIVER_MIN` holds on a short day too, and dropping it to 1 there was a real mistake.**
        # The intuition was that on a day whose purchases are queued behind the money, a single unit
        # in hand is worth banking. It is not, because a shed trip costs a turn even when it costs no
        # travel -- and pens sit ON shed-access tiles by design (`_refresh_pins`), so a tour round
        # the herd stands on a depot at almost every stop. At a threshold of one, seed 11 day 4
        # planned this for its first hand:
        #
        #     Shed[WHEATx2] (3,4)[FEED CARE COLLECT] Shed[DROP+WHEATx1] (4,4)[FEED CARE COLLECT]
        #     Shed[DROP] (4,3)[WATER HARVEST] Shed[DROP] (3,3)[WATER HARVEST] Shed[DROP]
        #
        # -- a shed trip after every stop, each one dumping the feed wheat it then has to draw back.
        # Over the day: PICKUP 2, DROP 12, FEED 0, CARE 0, eight animals unfed. The tape drops five
        # times on that day and feeds seven.
        #
        # What a short day actually needs is different work FIRST, not more trips: see `Job.funds`,
        # which is `rush`'s real job. Delivery batching is a separate question and its answer does
        # not change with the bank.
        if load >= DELIVER_MIN:
            d = nearest(depots, pos, j.tile)
            # The drop takes the wheat with it, so the same stop draws back everything still ahead.
            back = collections.Counter({it: q for it, q in after[i].items() if q > 0})
            route.append(Depot(d, drop=True, pick=back))
            held = collections.Counter(back)
            pos = d
        elif short:
            d = nearest(depots, pos, j.tile)
            # A draw is critical when SOME job it is FOR dies tonight if skipped -- read straight off
            # `REQUIRED_OPS`/`at_risk`, never priced. Scoped to jobs that actually need one of the
            # short items, so a draw serving only ordinary work is never marked critical by a
            # coincidental critical job elsewhere later in the same tour.
            critical = any(w.at_risk and w.required for w in work[i:]
                          if any(w.needs.get(it, 0) > 0 for it in short))
            route.append(Depot(d, drop=False, pick=short, critical=critical))
            held += short
            pos = d
        route.append(j)
        held -= j.needs
        held += j.gives
        pos = j.tile

    # **`yields()`, not just a non-empty hand.** `gives` is a prediction and is empty whenever the
    # board cannot supply one -- a tile whose `yield_units` is still 0 at dawn because the WATER that
    # fills it happens in this same visit, or any job built without `tiles`. Closing on the hand
    # alone would silently drop the walk home for exactly those, which is the whole return leg for a
    # one-shot crop. The op is the fact; the quantity is the estimate.
    if deliver and (any(q > 0 for q in held.values()) or any(j.yields() for j in work)):
        route.append(Depot(nearest(depots, pos), drop=True))
    return route


def turns(start, route):
    """Exact turns spent walking a MATERIALISED route. The only cost model in the file.

    No hidden legs at either end: a route costs what walking it costs, which is the property
    `test_the_cost_of_a_route_is_the_route_and_nothing_else` pins.
    """
    total, pos = 0, tuple(start)
    for stop in route:
        total += dist(pos, stop.tile) + stop.turns
        pos = tuple(stop.tile)
    return total


def draws(route):
    """Everything a materialised route picks up, summed. Reporting only -- the stops are the truth."""
    out = collections.Counter()
    for stop in route:
        if getattr(stop, "depot", False):
            out += stop.pick
    return out


def cover(units, jobs, budget, depots=SHED, carry=None, supply=None, deliver=True, wanted=None,
          rush=False):
    """Cover as many jobs as the crew can reach. Returns `(work, uncovered)`.

    `work` is `{unit_index: [Job, ...]}` -- the WORK SEQUENCE, without shed trips; run it through
    `materialise` to get the tour. `uncovered` is the jobs no unit could take. `supply` caps how many
    animals may be drawn from the shed across the whole plan.
    """
    depots = tuple(depots) or SHED
    carry = carry or {}
    routes = {u: [] for u in range(len(units))}
    left = list(jobs)
    stock = collections.Counter(supply) if supply is not None else None
    booked = collections.Counter()

    def load(u):
        return carry.get(u) or {}

    def cost(u, work):
        # **The closing shed trip is NOT charged while the work is being packed, and that is
        # measured.** It used to be, and it cost a turn per yielding tour that could not be bought
        # back: over 29 matched days against the tape, HARVEST fell 325 -> 301 and PASS rose
        # 834 -> 956 (`data/logs/matched29_rebuild.log` against `data/logs/matched29.log`) purely on
        # reserving it. Roughly 170 tours a season end holding produce, so charging the DROP op
        # inside the budget refuses one job on each of them.
        #
        # And it buys nothing to reserve it, because `_drop_inventories_to_shed`
        # (`kaggriculture.py:812`) empties every hand into the shed at the rollover. Getting home is
        # worth turns only for produce the market is waiting for TODAY -- which is the MID-TOUR drop,
        # and that one is still costed here, inside `materialise`, where it happens.
        #
        # So the closing trip is opportunistic: `plan` appends it afterwards out of whatever turns
        # the tour did not spend. Same rule the old executor's return leg followed by accident -- it
        # only ever fired on a turn the unit would have passed -- now stated in the plan instead of
        # discovered at dusk.
        return turns(units[u], materialise(units[u], work, load(u), depots, wanted, False, rush))

    used = {u: 0 for u in range(len(units))}

    def slot(u, j, base, limit=None):
        """Cheapest position for `j` in unit `u`'s `base` sequence within `limit` turns, `(cost, i)`."""
        if j.only is not None and j.only != u:
            return None
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

    # Four passes, and the FIRST one is the whole point. See `REQUIRED_OPS`: an animal that missed
    # yesterday dies tonight if it misses again, while one fed yesterday can slip a day for free --
    # which is exactly how the tape feeds 16 of 19 pens on day 19 and loses nothing. A flat
    # `required` cannot express that and drops the same animal twice.
    greedy([j for j in left if j.at_risk and j.required])        # an animal that dies tonight
    greedy([j for j in left if j.funds])                          # the day's shopping list, unpaid
    greedy([j for j in left if j.required and not j.at_risk])     # the rest of the herd
    greedy([j for j in left if j.at_risk and not j.required])     # a tile that weeds tonight
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
        greedy([j for j in left if j.funds])
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
        for j in sorted(left, key=lambda j: (not (j.at_risk and j.required), not j.funds,
                                             not j.required, not j.at_risk, j.tile)):
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


def from_nodes(nodes, tiles=None):
    """`router.Node` -> `Job`, keeping the node's own `needs` rather than re-deriving them.

    `build_nodes` decides WHICH jobs exist -- a thirsty tile offers water, a fed animal does not
    offer feed -- and that half is derived from the reference's mechanics and is worth keeping. What
    is dropped here is `prize` and `mandatory`: the RANKING, which is the half that measured wrong.
    `Node.needs` also carries the wheat a PLACE implies (`PLACE_DRAWS_FEED`), which is invisible in
    `ops` and would be lost by re-deriving.

    `at_risk` comes from `Node.critical`, which `animal_ops` sets from `consecutive_unfed >= 1`.
    That is a reading of the BOARD, not of the price table -- even though on the router's side it is
    expressed as a number so it can compete in a ratio.

    `tiles` is optional and only feeds `gives`, the predicted yield that lets a delivery be planned
    at dawn rather than discovered at dusk. Without it every job reports an empty hand, which is safe
    -- no mid-tour shed trip is ever judged worthwhile, so loads ride to the end of the tour as they
    did before there was a `gives` at all.
    """
    return [Job(n.tile, n.ops, n.needs, gives=predict_yield(n, tiles),
                at_risk=getattr(n, "critical", False)) for n in nodes]


def predict_yield(node, tiles):
    """What this node puts in the hand, read off the board. `{}` when it cannot be known.

    HARVEST moves `tile["yield_units"]` of the crop (or the animal's product) into the inventory and
    zeroes the tile (`kaggriculture.py:388`); COLLECT_FERTILIZER adds exactly one
    (`kaggriculture.py:490`). Both are on the board at dawn.

    A one-shot crop watered inside its window gains yield BEFORE the harvest in the same visit, so
    this under-reads those by one or two. That is deliberate: `gives` only ever gates whether a load
    is worth a mid-tour trip, and under-reading defers a trip while over-reading books one for
    produce that does not exist.
    """
    if tiles is None:
        return {}
    x, y = node.tile
    try:
        cell = tiles[y][x]
    except (IndexError, TypeError):
        return {}
    if not isinstance(cell, dict):
        return {}
    out = collections.Counter()
    for op, _item in node.ops:
        if op == "COLLECT_FERTILIZER":
            out["FERTILIZER"] += 1
        elif op == "HARVEST":
            units = int(cell.get("yield_units", 0) or 0)
            if units <= 0:
                continue
            if "animal" in cell:
                product = R.ANIMALS[cell["animal"]]["product"]
            else:
                product = cell.get("crop")
            if product:
                out[product] += units
    return out


def plan(units, jobs, budget, depots=SHED, carry=None, supply=None, deliver=True, wanted=None,
         rush=False):
    """`cover`, materialised, in the shape `schedule_agent` already consumes."""
    depots = tuple(depots) or SHED
    work, left = cover(units, jobs, budget, depots, carry, supply, deliver, wanted, rush)
    out = {}
    for u, seq in work.items():
        held = (carry or {}).get(u) or {}
        route = materialise(units[u], seq, held, depots, wanted, False, rush)
        cost = turns(units[u], route)
        # The closing trip, out of the turns the tour did not spend. See the note in `cover.cost`:
        # it is worth having and it is never worth a job, so it goes on last and only if it fits.
        if deliver:
            home = materialise(units[u], seq, held, depots, wanted, True, rush)
            if turns(units[u], home) <= budget[u]:
                route, cost = home, turns(units[u], home)
        out[u] = dict(route=route, draw=draws(route),
                      depot=(next((s.tile for s in route if getattr(s, "depot", False)), None)),
                      cost=cost)
    return out, left
