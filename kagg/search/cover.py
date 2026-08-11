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

#: Cache `slot` against the route it was computed for, and clear that unit's cache when its route
#: changes. **This is a pure speed change: it cannot alter a plan**, and the flag exists so that
#: claim stays falsifiable rather than merely asserted -- flipping it off restores the exact
#: recomputation and `tests/test_the_plan_is_identical_when_memoised.py` compares the two.
#:
#: It exists because time, not play, is what disqualified submission 55352401. See the long note
#: beside `slot_now` in `cover` for the profile and the episode.
MEMOISE_SLOT = True

#: Whether the shed limits EVERY item a job draws, or only the animals. See `claim` for the day-4
#: failure this fixes: six FEEDs planned against a shed holding no wheat, two performed.
#: `tests/test_day_four_feeds_the_whole_herd.py` is the reproduction.
#: **SHIPS OFF. Measured three times, worse every time.** The diagnosis behind it is correct and
#: worth keeping: day 4's dawn solve has one unit, which lifts all six wheat out of the shed, and
#: the hour-1 replan then covers six FEEDs against a shed holding zero -- five of them on hands
#: that can never obtain wheat. Two feeds happen, four animals go hungry with seventy idle turns.
#:
#: But refusing the job is the wrong answer to it. Seed 11, weeds off, against Seb's 1.32.6 tape,
#: `days 0-16 totals` and the d16 board:
#:
#:     setting                        work  idle   d16 money   d16 cow/sheep
#:     off (shipped)                  1144  1289       7,293        5 / 7
#:     on, needs | places             1025  1441       3,280        6 / 7   and the 4th parcel never bought
#:     on, FEED/FERTILIZE only         930  1372           0        3 / 0
#:
#: Each tightening moves work DOWN and idle UP, because a refused FEED is a hand with nothing to do
#: and an animal that starves anyway. The shed being empty is a funding problem -- Seb answers it
#: with 14-22 BUY_PRODUCT a day from d11 while we buy none -- and a planner constraint cannot buy
#: wheat. Turn this on only together with a rule that raises the shortfall as a purchase.
SUPPLY_LIMITS_EVERY_DRAW = False

#: The ops whose drawn item is genuinely SPENT at the tile, so the shed has to hold it before the
#: job can be planned. PLACE and BUILD are deliberately absent: their `needs` carry feed wheat that
#: the op does not consume, and constraining on it refused animal placements outright.
SUPPLY_CHECKED_OPS = ("FEED", "FERTILIZE")

#: Sentinel for "not in the cache", so a genuine `None` from `slot` -- which means "this job does
#: not fit this unit at all", the single most common answer -- is cached instead of recomputed.
_MISS = object()

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

#: Whether a hand already standing at the shed, holding produce today's row wants AND items later
#: jobs need, drops the lot and draws the latter straight back -- instead of carrying the produce to
#: the end of the tour because the drop cannot be selective. See the block in `materialise`.
REDRAW_RATHER_THAN_CARRY = True

#: Whether that re-draw refuses when the thing it means to draw back is on today's SELL row.
#:
#: **The re-draw is planned as a certainty and is not one.** `_process_market` runs AFTER the unit
#: phase in the same turn (`kaggriculture.py:922` then `:928`), so the drop lands in the shed and the
#: turn's SELL orders lift it out again before the hand comes back. On this board the row's produce
#: and the herd's dinner are the same commodity, which is what makes it reachable at all.
#:
#: Measured, seed 11 day 4, Seb's tape. The herd hand banks one fertilizer at h6 and sheds three
#: wheat with it -- `DROP` is all-or-nothing (`kaggriculture.py:333`) -- then asks for three back at
#: h8 and gets one, because that turn's row sold `WHEAT 1` and `FERTILIZER 1`. The shed then reads
#: empty from h9 to h18, so `FETCH_THE_FEED_AND_RETURN` cannot rescue it either: its gate is
#: `shed["WHEAT"] > 0`. The cow placed at `(3,3)` at h14 is never fed and never cared for.
#:
#: Seb does not make the trip. Same day, same board, same purchases (6 wheat in the shed at dawn and
#: 1 bought -- he is NOT better supplied): he draws the whole shed at dawn across two carriers,
#: sends a third hand out with the cow, and emits no DROP at all before h18. See
#: `docs/how_seb_feeds_the_herd.md`.
#:
#: Narrowed, not switched off. The day-1 case `REDRAW_RATHER_THAN_CARRY` was added for -- fertilizer
#: held from h5 to h16, four units sold for $2 less than the tape -- has nothing owed ahead that the
#: row also sells, so it still fires.
REDRAW_ONLY_WHAT_THE_MARKET_WONT_TAKE = True

#: How much of the row's produce a hand must already be HOLDING at the start of a `rush` tour before
#: the tour opens with a shed trip. See `materialise` rule 0.
#:
#: This is deliberately NOT a lowered `DELIVER_MIN`. The note at rule 2 records what lowering that
#: threshold on a short day actually did -- a shed trip after every stop, PICKUP 2 / DROP 12, eight
#: animals unfed. This fires at most ONCE per tour, before any work, and so cannot produce that
#: shape. It is the delivery half of `FUND_THE_DAY_WHEN_SHORT`: that rule reorders the day's WORK so
#: the sellable harvest happens first, and this one gets the result to the shed while the market is
#: still open.
RUSH_BANK_MIN = 4

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

#: Whether a tour DROPS what it is carrying at a depot it is already standing on -- zero detour,
#: one turn. See the note where it fires. This is the cheap half of the delivery defect above: it
#: never buys a walk, so it cannot take turns away from feeding the way the detour version did.
DROP_WHERE_THE_TOUR_ALREADY_STANDS = True

#: **Harvest all day, bank at dusk.** No mid-tour DROP while the tour still has produce to take.
#:
#: Read off Seb's own actions on day 4 of both tapes -- fourteen harvests each time, and not one
#: DROP until the harvesting was finished:
#:
#:     seb (interval 12)  HARVEST 4 6 7 8 9 11 12 12 13 14 15 15 15 17   DROP 20 20 21 22 23
#:     seb1326 (24)       HARVEST 4 6 8 9 10 11 11 13 14 14 14 14 15 18  DROP 18 21 21 21 22 23 23
#:
#: The env rebalance moved the sweep earlier and made it longer -- seven drops from h18 rather than
#: five from h20, because at `townCenterSellInterval` 24 the town absorbs less per tick -- and left
#: the ordering rule untouched. His algorithm did not change; the volume it has to move did.
#:
#: Ours on `seb1326` day 4 dropped at h14 and h16, sold those part-loads for $282 and $507, then
#: took its LAST drop at h21 while still harvesting at h21, h21 and h22 -- so that produce was in
#: hand when the day closed. The row asked `WHEAT 49, FERTILIZER 6`; we filled 27 and 3, and the
#: bank finished the day at $73 against his $1,107.
#:
#: All three mid-tour drop paths are gated on this, because the defect is in none of them
#: individually: each is locally reasonable and none looked AHEAD for produce still to come.
#: The closing drop is deliberately NOT gated -- it runs after every job by construction, and it is
#: what this rule funnels the whole day's load into.
#:
#: **NARROWED 2026-08-10 to HARVEST only.** It was written against `Job.yields()`, and `YIELDING` is
#: `("HARVEST", "COLLECT_FERTILIZER")` -- so a day whose only production is fertilizer could not bank
#: until its last pen was walked. Day 5 of `seb1326`, seed 11, held $17 from h03 to h19 with four
#: fertilizer in the crew's hands, re-offering a $100 strawberry seed on every one of those turns; it
#: arrived at h21 and was still in the bag at dusk. The tape gates on HARVEST and nothing else --
#: `d4 HARVEST 5..19 / DROP 19 22 22 22 23` against `d6 COLLECT_FERTILIZER 3 4 6 8 10 11 14 /
#: DROP 9 15 17 19`, where he banks with three collections still ahead. See `Job.harvests()`.
BANK_ONLY_AFTER_THE_LAST_HARVEST = True


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


#: `nearest` is a PURE function of `(depots, frm, to)` and it is the hot spot of the whole planner.
#: Profiled on the day-11 handover board (seed 11, the densest farm we plan on): 3.99s in the dawn
#: solve, of which `nearest` is 336,324 calls costing 0.95s cumulative -- and because it scores every
#: depot with two `dist` calls, it is also where 3.9M of the 3.94M `dist` calls and 7.9M of the
#: `abs` calls come from. Memoising it removes that entire subtree.
#:
#: Safe to cache without invalidation because nothing here reads mutable state: `depots` arrives as a
#: tuple of coordinates, `frm` and `to` are grid positions, and the tie-break is on coordinates, so
#: the result is a pure function of the key. The board is 10x10, so the key space is bounded by
#: (depot sets) x 100 x 101 and cannot grow without bound over a season.
_NEAREST = {}


class Job:
    """One tile and every op it wants today. `turns` is how long standing there costs."""

    __slots__ = ("tile", "ops", "turns", "needs", "gives", "required", "at_risk", "funds", "only",
                 "products")

    #: Never a shed trip. `materialise` inserts those and everything downstream keys off this to tell
    #: the two apart -- a depot stop is not work, does not get claimed against an idle unit, and is
    #: not re-derived from its cell by the executor.
    depot = False

    def __init__(self, tile, ops, needs=None, gives=None, at_risk=False, only=None,
                 products=frozenset()):
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
        #: Products this job WILL yield, quantity unknown. See `yield_products`.
        self.products = frozenset(products or ())
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

    def harvests(self):
        """Produce the day cannot bank ahead of -- see `BANK_ONLY_AFTER_THE_LAST_HARVEST`.

        A STRICT subset of `yields()`, and the difference is the whole point.  `YIELDING` also holds
        `COLLECT_FERTILIZER`, so gating the bank on `yields()` froze every fertilizer day's cash in
        the crew's hands: day 5 of `seb1326`, seed 11, sat on $17 from h03 to h19 re-offering a
        strawberry it could not afford, while four fertilizer -- $100 apiece -- walked around in its
        pockets.  Seb banks at h9 of his own day 6 with three collections still ahead.
        """
        return any(o == "HARVEST" for o, _i in self.ops)

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
    products = frozenset()
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

    def harvests(self):
        return False

    def __repr__(self):
        bits = (["DROP"] if self.drop else []) + [f"{i}x{q}" for i, q in sorted(self.pick.items())]
        return f"Shed{self.tile}[{'+'.join(bits) or '-'}]"


def nearest(depots, frm, to=None):
    """The depot cheapest to visit between `frm` and `to`. Ties broken on coordinates, so it is total.

    Memoised on `_NEAREST`; see the note there for why that is safe. The body below is the definition
    and stays the definition -- the cache only skips recomputing it, and
    `tests/test_nearest_is_memoised_without_changing_it.py` pins the two against each other over the
    whole reachable key space rather than trusting that claim.
    """
    # Callers are not all tuple-typed (`materialise` already converts, others pass lists), and an
    # unhashable key would raise rather than merely miss -- so normalise before touching the cache.
    if type(depots) is not tuple:
        depots = tuple(depots)
    frm = (frm[0], frm[1])
    key = (depots, frm, None if to is None else (to[0], to[1]))
    hit = _NEAREST.get(key)
    if hit is not None:
        return hit
    if to is None:
        out = min(depots, key=lambda c: (dist(c, frm), c))
    else:
        out = min(depots, key=lambda c: (dist(frm, c) + dist(c, to), c))
    _NEAREST[key] = out
    return out


def materialise(start, work, carry=None, depots=SHED, wanted=None, deliver=True, rush=False,
                wanted_only=False, due=None):
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

    `due` is **the cadence deadline**: turns from the START of this tour by which the row's produce
    has to be standing in the shed. `None` means no deadline is known and rule 2 fires on quantity
    alone, which is what every caller did before the deadline existed.

    It exists because rule 2 had no clock. `wanted` carries a quantity and no hour, so every unit of
    it read as due immediately and a hand holding `DELIVER_MIN` of the row bought a ~12-turn round
    trip -- however early in the day it was, and however soon it was going to walk past the shed
    anyway. On day 4 of tape 91422988 that is the whole of `water 11/17`: 17 WATER jobs offered, 11
    toured, 6 refused, every refused tile one square from the last tile taken and priced at twelve
    turns. Seb plays that day and makes **no drop before hour 18** -- all six of his are the closing
    walk home, and his sells follow at h18-h23. His justified ferry quantity is zero.

    So the trip is justified only for produce needed EARLIER than the hand would have reached the
    shed regardless. `left` below is when this tour delivers on its own; when that already beats the
    deadline, the ferry buys nothing but a shorter tour. It is deliberately a LOWER bound -- it counts
    the walk and the work still ahead but not the depot stops rules 1 and 2 have yet to insert -- so
    it errs towards "the hand gets home early", which errs towards refusing the ferry. That is the
    conservative direction here: the cost of a wrong refusal is produce banked by the closing trip
    instead of mid-tour, and the cost of a wrong ferry is a tile that never gets watered.

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
    # Built by copy-and-add rather than `after[i + 1] + work[i].needs`. `Counter.__add__` runs
    # `update` and then `_keep_positive` over the whole accumulator on every job, and this loop is
    # the single hottest thing in the planner: profiled on the day-11 handover board it was 300,609
    # `__add__` calls costing 0.31s, plus its share of 1.1M `Counter.__init__` calls, inside a 3.3s
    # solve. `needs` values are counts and never negative, so `_keep_positive` can only ever drop
    # zeros -- and a zero is never added below -- which is why this is the same suffix sum and not an
    # approximation of it. Every entry still ends up strictly positive, exactly as `__add__` left it.
    #
    # A fresh Counter per index, deliberately: the old code allocated one per iteration too, and
    # `after[0]` is handed to `Depot(pick=...)` which holds the reference. Sharing the object when a
    # job needs nothing would be faster still and would introduce aliasing this loop never had.
    after = [None] * (len(work) + 1)
    acc = collections.Counter()
    after[len(work)] = acc
    for i in range(len(work) - 1, -1, -1):
        acc = acc.copy()
        for _k, _v in work[i].needs.items():
            if _v > 0:
                acc[_k] += _v
        after[i] = acc

    # Suffix walk cost, for the deadline test at rule 2: `tail[i]` is the turns spent from ARRIVING at
    # `work[i].tile` until the closing drop is done. Same shape and the same reason as `after` above --
    # computed once, so the "would this hand have got home in time anyway" question is O(1) per job
    # rather than re-materialising the remainder inside the loop that materialises it.
    # Skipped entirely when no deadline was passed, since nothing then reads it.
    tail = None
    if due is not None and work:
        tail = [0] * (len(work) + 1)
        tail[len(work) - 1] = work[-1].turns + dist(work[-1].tile, nearest(depots, work[-1].tile)) + 1
        for i in range(len(work) - 2, -1, -1):
            tail[i] = work[i].turns + dist(work[i].tile, work[i + 1].tile) + tail[i + 1]

    route, pos = [], tuple(start)

    # **Rule 0, and only on a short day: a hand that STARTS the tour holding the row's produce banks
    # it before it works.** See `RUSH_BANK_MIN`.
    #
    # `rush` reaches here as `fund=short_of_cash` from `_solve`, and until now it only reordered WORK
    # -- `Job.funds` puts the sellable harvest first. That is half a rule. The other half is that the
    # result has to reach the SHED, because the market reads the shed and nothing else, and a unit
    # diverted by `BANK_THE_HAND_WHEN_SHORT` arrives here already carrying the goods. Without this it
    # is handed a fresh tour and the only drop it gets is the closing one at rule 3, after all of it.
    #
    # Measured, seed 11 day 4: u0 held 4 FERTILIZER and u6 held 2, from hour 8 to hour 15, while the
    # bank finished the day on $939 against a $1,000 parcel. Four is under `DELIVER_MIN`, so rule 2
    # never fired and the fertilizer was banked by the midnight sweep, hours after the market shut.
    #
    # The `owed` guard is the same one rule 2 and the free drop carry, for the same reason: `DROP` is
    # all-or-nothing (`kaggriculture.py:333`), so a hand holding the herd's dinner beside the harvest
    # would shed both. If ANY of what it carries is owed ahead, the tour keeps the lot and delivers
    # the ordinary way.
    if rush and work and not any(after[0][p] > 0 for p, q in held.items() if q > 0):
        spare = sum(min(held[p], q) for p, q in wanted.items() if q > 0 and held[p] > 0)
        if spare >= RUSH_BANK_MIN:
            d = nearest(depots, pos, work[0].tile)
            # Draws the whole remainder back on the same stop, exactly as rule 2 does, so the tour
            # does not pay for a second depot visit one job later.
            route.append(Depot(d, drop=True, pick=after[0]))
            held = collections.Counter(after[0])
            pos = d

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
        # **The drop that costs no walking.** See `DROP_WHERE_THE_TOUR_ALREADY_STANDS`. `_refresh_pins`
        # sites pens ON the shed-access tiles, so a herd tour is stood on a depot at most of its stops
        # and `nearest` returns a cell that adds nothing to the walk. There the produce reaches the
        # shed -- while the market is open -- for one turn and no travel, which is the entire
        # difference between this and the arm that lost three cows by inserting a detour.
        #
        # Deliberately NOT gated on `DELIVER_MIN`: the threshold exists to stop a small load buying a
        # WALK, and there is no walk here. It is gated on the detour being exactly zero, because at
        # one step it is a walk again and the measurement that matters is the season, not the hand.
        d = nearest(depots, pos, j.tile)
        free = dist(pos, d) + dist(d, j.tile) == dist(pos, j.tile)
        spare = sum(max(0, q - after[i][p]) for p, q in held.items() if q > 0)
        # **A DROP takes the WHOLE hand, so it may only fire on a hand with nothing owed ahead.**
        # `kaggriculture.py:333` -- DROP is all-or-nothing; the executor dumps the unit's entire
        # inventory, it cannot pick out the produce and keep the feed. The first version of this
        # planned as though it could (`held` was recomputed as `min(q, after[i][p])`) and the season
        # lost a cow and two sheep: a tour standing on a depot mid-round binned the wheat its next
        # four pens were about to eat, and `after[i]` said it still had it.
        #
        # So the condition is not "is there spare" but "is ALL of it spare". A herd tour still gets
        # its drop -- the produce accumulates and the feed is consumed as it goes, so the hand is
        # clean by the last pens -- it just gets it later than the greedy version wanted.
        owed_ahead = any(after[i][p] > 0 for p, q in held.items() if q > 0)
        # **What the market will sell, the hand cannot draw back.** See
        # `REDRAW_ONLY_WHAT_THE_MARKET_WONT_TAKE`. The drop and the day's SELL orders hit the same
        # shed on the same turn and the market goes second, so banking the herd's wheat on a day whose
        # row sells wheat does not cost a turn -- it costs the feed.
        contested = (REDRAW_ONLY_WHAT_THE_MARKET_WONT_TAKE
                     and any(wanted.get(p, 0) > 0 for p, q in after[i].items() if q > 0))
        # **Is there still a harvest ahead on this tour?** See `BANK_ONLY_AFTER_THE_LAST_HARVEST`.
        # `work[i:]` includes the job about to be walked to, which is right: a drop planned on the
        # way TO a harvest is as early as one planned between two.
        reaping = BANK_ONLY_AFTER_THE_LAST_HARVEST and any(w.harvests() for w in work[i:])
        if DROP_WHERE_THE_TOUR_ALREADY_STANDS and free and spare > 0 and not owed_ahead \
                and not reaping:
            route.append(Depot(d, drop=True))
            held = collections.Counter()
            pos = d
        elif (REDRAW_RATHER_THAN_CARRY and free and spare > 0 and owed_ahead and not contested
              and not reaping
              and any(wanted.get(p, 0) > 0 and q > 0 for p, q in held.items())):
            # **A hand standing at the shed holding the row's produce should bank it and take its
            # wheat straight back.** The free drop above refuses whenever anything in the hand is
            # owed to a later job, because `DROP` is all-or-nothing (`kaggriculture.py:333`) and
            # binning the feed for four pens ahead is how a season loses a cow. Correct -- but the
            # alternative it settles for is carrying the produce to the end of the tour, and the
            # market reads the SHED and nothing else.
            #
            # Traced on day 1 of Seb's tape, seed 11: u1 collects fertilizer at h5 STANDING ON the
            # shed tile, carrying 2 wheat for pens ahead, and holds that fertilizer through h9 and
            # h13 before dropping at h16. The tape has its first unit in at h4 and sells 2 @ $100,
            # 1 @ $100, 1 @ $99 across h4-h12 while we sell 1 @ $100 and then three at $99 in one
            # turn -- the same four units, $2 worse, and we cannot spread what is not in the shed.
            #
            # The trip is already being made: the hand is HERE. It costs the DROP plus one turn per
            # item drawn back, and it is only taken when the hand actually holds something the row
            # is waiting for -- never to shed a load nobody is buying today.
            back = collections.Counter({it: q for it, q in after[i].items() if q > 0})
            route.append(Depot(d, drop=True, pick=back))
            held = collections.Counter(back)
            pos = d
        # **Rule 2 now has a clock.** `left` is when this tour delivers under its own steam: what has
        # been walked so far, plus the step onto this job, plus every job and step still ahead, plus
        # the closing drop. A ferry is only worth its twelve turns when that lands AFTER the row needs
        # the goods. See the `due` paragraph in the docstring for the day-4 measurement.
        #
        # `turns(start, route)` rather than a running total, deliberately: it is O(len(route)) and it
        # runs only on the rare job that already cleared `DELIVER_MIN`, whereas a `spent` accumulator
        # would have to be kept correct at all six places this loop moves `pos` -- and this function
        # is the one place in the planner where the cost model must not be paraphrased.
        if load >= DELIVER_MIN and not reaping and (
                due is None or turns(start, route) + dist(pos, j.tile) + tail[i] > due):
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
    if deliver:
        ends_loaded = any(q > 0 for q in held.values()) or any(j.yields() for j in work)
        # `wanted_only` narrows rule 3 to tours that will produce something the row sells today.
        # See `RESERVE_THE_TRIP_FOR_TODAYS_HARVEST` for why this reads `products` and not `gives`.
        if ends_loaded and wanted_only:
            ends_loaded = (any(held.get(i, 0) > 0 for i in wanted)
                           or any(p in wanted for j in work for p in j.products))
        if ends_loaded:
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


#: Whether a PLACE is pinned to the hand that builds its pen. See the block in `cover`'s greedy
#: commit for the mechanism and the day-0 trace. OFF lets the two land on different hands, which
#: silently drops the placement.
PLACE_FOLLOWS_ITS_BUILD = True

#: **End a tour at the shed when that tour will HARVEST something today's row is selling.**
#:
#: Not the blanket reserve -- that one charges every tour that ends holding anything, was measured at
#: HARVEST 325 -> 301 and PASS 834 -> 956, and is a loss. This fires only on the tours that produce a
#: product the day's `sells` row names, which on a typical day is two or three of thirteen.
#:
#: It has to key on `Job.products` and not on `Job.gives`: `gives` is the predicted QUANTITY and is
#: empty whenever `yield_units` is still 0 at dawn, which is the normal state of a crop that ripens
#: during the day. That is exactly the case this exists for -- 12 melons harvested h12-h15 on d10 and
#: carried to h23 with the row asking for 18 and the shed empty all day.
RESERVE_THE_TRIP_FOR_TODAYS_HARVEST = True

#: First day the reserve may fire. **d0-d6 is deliberately untouched -- Alex's instruction, and the
#: measurement agrees**: without the reserve those days are exact on `harvest 14/14`, `water 17/17`
#: and `feed 7/7`, and with it d4 falls to `harvest 10/14`, `water 12/17`, `feed 6/7`. The opening is
#: not where produce is stranded; the herd is small, the tours are short and the shed is reached.
#: Every animal we lose dies from d9 on, once the herd outgrows the crew.
RESERVE_FROM_DAY = 10

#: The days the trip home is worth a job.
#:
#: **d4 was tried and measured and is NOT in this set, and the reason is worth keeping.** On paper
#: it is the day that wants it most: turned on for d4 alone, `sell` goes 41/55 -> 54/55,
#: `buy_product` 21/1 -> 15/1, and the `BUY_LAND` the tape makes that day becomes affordable
#: (`tiles 50/50`). It still loses, twice over.
#:
#: It loses the day: d4 banks **$542 selling 54 units against $774 selling 41**. `market_price`
#: falls as the town's inventory rises, and the reserve lands the whole load in two DROP waves where
#: the tape lands it in four -- h18 5, h21 12, h22 12, h23 20. Matching the COUNT while bunching the
#: fills is worse than missing the count. That is the same lesson as `RESERVATION_SELL_CAP`, arrived
#: at from the other side.
#:
#: And it loses the week: d4 pays for it in `water 12/17`, `harvest 10/14`, `feed 6/7`, `care 6/7`,
#: and the thinner bank starves d5-d8 -- d6 `feed 6/7` where it had been exact, d8 `unit-turns
#: 162/231`. Season money at d16 goes $9,975 -> $8,821.
RESERVE_DAYS = frozenset({2, 3}) | frozenset(range(RESERVE_FROM_DAY, 30))

#: Whether the greedy ranks an insertion by the tour plus its walk home rather than the tour alone.
#: Unlike `RESERVE_DAYS` this never refuses a job -- it only changes WHICH hand gets it.
RANK_BY_THE_TRIP_HOME = False

#: Days it applies. d4 is the day it exists for: 28 wheat and 4 fertilizer in hands at dusk against
#: a row asking for 49 and 6.
RANK_HOME_DAYS = frozenset({4})

#: Whether a tour that cannot get its load home gives up trailing jobs until it can. Never a trade:
#: the produce those jobs make is stranded by definition, so the turns buy nothing as things stand.
TRIM_A_TAIL_THAT_CANNOT_COME_HOME = False


def cover(units, jobs, budget, depots=SHED, carry=None, supply=None, deliver=True, wanted=None,
          day=None,
          rush=False, due=None):
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

    #: Whether `slot` ranks candidate positions by the tour INCLUDING its trip home. See the note
    #: in `slot`. Scoped to the same day set as the hard reserve plus the days that strand produce.
    rank_home = bool(RANK_BY_THE_TRIP_HOME and wanted and day in RANK_HOME_DAYS)

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
        #
        # **Charging it is a FEASIBILITY constraint, not a preference, and that is why it is per
        # day.** A tour that cannot afford the walk home refuses the job outright; if no other unit
        # is near enough, the job goes uncovered and the turns it would have used sit idle. Expressed
        # as a preference between positions that already fit, it changes d4 not at all -- u1's tour
        # is 18 turns of work against a 7-turn trip on a 23-turn budget, so no ordering has both --
        # and costs d10-d16 $1,722. The trade is real; `RESERVE_DAYS` says on which days it is worth
        # taking.
        if RESERVE_THE_TRIP_FOR_TODAYS_HARVEST and wanted and day in RESERVE_DAYS:
            return turns(units[u], materialise(units[u], work, load(u), depots, wanted, True, rush,
                                               wanted_only=True, due=due))
        return turns(units[u], materialise(units[u], work, load(u), depots, wanted, False, rush,
                                           due=due))

    used = {u: 0 for u in range(len(units))}

    # **A pen is BUILT and FILLED on the same square, and nothing else orders those two.** The route
    # is a visit ORDER -- `_live_ops` re-derives the work from the live board at each stop
    # (`schedule_agent:1201`) -- so a hand that arrives at a square whose pen is not up yet reads
    # bare ground, gets no ops back, and the stop is dropped. The animal rides home in its hand and
    # the walk is spent. Between two DIFFERENT hands there is no ordering at all.
    #
    # Traced on the day-0 dawn plan, seed 11, with the day planned once: u3 was sent to fill (2,4)
    # while u4 was the hand building it. `place` measured 2/4, and the wasted walks are where
    # `build_pasture` 6/8 and `plant` 16/17 went.
    #
    # Expressed as a feasibility rule rather than a pin on `Job.only`, because a pin set when the
    # BUILD commits is too late whenever the PLACE commits first -- which the greedy is free to do,
    # it ranks on insertion cost and knows nothing about the pair. As a rule it holds in both
    # orders: a placement may only enter a sequence that ALREADY contains its build, and only at a
    # position after it. Placements still compete for turns on their merits; they just compete on
    # the one hand that can actually serve them.
    build_at = {}
    if PLACE_FOLLOWS_ITS_BUILD:
        for j in jobs:
            if any(o == "BUILD" for o, _i in j.ops):
                build_at[tuple(j.tile)] = j

    def slot(u, j, base, limit=None):
        """Cheapest position for `j` in unit `u`'s `base` sequence within `limit` turns, `(cost, i)`."""
        if j.only is not None and j.only != u:
            return None
        first = 0
        if PLACE_FOLLOWS_ITS_BUILD and any(o == "PLACE" for o, _i in j.ops):
            b = build_at.get(tuple(j.tile))
            if b is not None and b is not j:
                if b not in base:
                    return None
                first = base.index(b) + 1
        cap = budget[u] if limit is None else limit
        best = None
        for i in range(first, len(base) + 1):
            seq = base[:i] + [j] + base[i:]
            c = cost(u, seq)
            if c > cap:
                continue
            # **Rank on the round trip, admit on the one-way.** The greedy chose positions by what
            # the tour costs to WALK OUT, so the far crops landed on whichever hand was cheapest to
            # reach them with -- and that hand then ended the day six steps from the shed holding
            # eight wheat. d4 sells 26 of 55 with 28 units in hands at dusk for exactly this reason.
            #
            # Charging the trip in `cost` instead makes it a feasibility test, which REFUSES the job:
            # no other unit is near enough, it goes uncovered, and the turns idle anyway (d4
            # `work 53/62` with `idle 62`, three cows gone by d8). Ranking is the version that has
            # neither failure -- the same jobs are covered, they are simply given to the hand that
            # can also bring them back.
            rank = c
            if rank_home:
                rank = turns(units[u], materialise(units[u], seq, load(u), depots, wanted, True,
                                                   rush, wanted_only=True, due=due))
            if best is None or rank < best[0]:
                best = (rank, i)
        return (cost(u, base[:best[1]] + [j] + base[best[1]:]), best[1]) if best else None

    # **The same `slot` is recomputed for units that have not moved, and that is the whole cost of
    # this file.** Every loop below rescans all jobs against all units, but a single accepted move
    # changes at most two routes -- so the other N-2 answers are the ones just computed, thrown away
    # and computed again. Profiling days 12-16 of seed 11: 99.7% of agent time inside `_solve`, and
    # `slot` reached 354,811 calls to `materialise`, each of which rebuilds an entire tour.
    #
    # That is what disqualified submission 55352401. Episode 91023699 seat 0 played 482 turns of 719
    # and timed out with the 60s overage bank at -1.7s; all 61.7s of charge came from 22 turns at
    # hours 1 and 2, which is the day solve and nothing else.
    #
    # `slot(u, j, routes[u], limit)` is a pure function of the unit's position, the job, that unit's
    # route and the limit. The first two never change inside a `cover` call and the last is explicit
    # in the key, so caching against the route and clearing the moment the route is touched is
    # exactly equivalent -- not approximately. `tests/test_the_plan_is_identical_when_memoised.py`
    # is the evidence, comparing whole plans over forty randomised boards.
    #
    # Per-unit dicts rather than one dict with a version in the key: invalidation is then `clear()`
    # on one unit, which is O(1) and bounds the memory instead of letting dead entries accumulate
    # for the length of the solve.
    memo = [{} for _ in range(max(1, len(units)))]

    def touch(u):
        """`routes[u]` changed, so every cached answer about it is stale."""
        memo[u].clear()

    def slot_now(u, j, limit=None):
        """`slot` against unit `u`'s CURRENT route. Only valid where the base IS `routes[u]`."""
        if not MEMOISE_SLOT:
            return slot(u, j, routes[u], limit)
        key = (j, limit)                  # `Job` hashes by identity and outlives this call
        got = memo[u].get(key, _MISS)
        if got is _MISS:
            got = memo[u][key] = slot(u, j, routes[u], limit)
        return got

    def claim(u, j):
        """What this job makes unit `u` draw FROM THE SHED, after what it already carries.

        **A hand carrying the cow claims nothing.** `Job.places()` is static and cannot know that,
        and netting it off is not optional: the moment a unit draws the animal the shed reads zero,
        so an un-netted claim makes the PLACE permanently unassignable and the hand carries the
        beast to dusk beside an empty pen. Measured on seed 11 day 1 -- cow in the shed at h1, drawn
        at h4, four empty pens standing free, no PLACE all day, dropped back overnight and finally
        placed on day 2 h9. One animal-day lost, and it repeats, which is the whole of `cow 7/8`.
        """
        held = collections.Counter(load(u))
        # **The wheat a FEED eats is as finite as the cow a PLACE takes, and it was never checked.**
        # This read `j.places()` -- PLACE ops only -- so `affordable` constrained animals and nothing
        # else. Day 4, seed 11, against Seb's 1.32.6 tape: the dawn solve has ONE unit, which picks up
        # all six wheat in the shed. The crew lands at hour 1, the shed reads zero, and the six-unit
        # replan covers all six FEEDs anyway -- five of them assigned to hands that can never obtain
        # wheat. Two feeds happen. Four animals go hungry with seventy unit-turns idle, and
        # `consecutive_unfed >= 2` takes two cows on day 7 (5 -> 3 while the tape holds at 5). By d16
        # that is 5 cows against 13 and $7,293 against $15,026.
        #
        # `needs` already carries the animal for a PLACE (`PLACE_DRAWS_FEED` puts the wheat there
        # too), so union rather than sum: `Counter |` takes the max per item and cannot double-count
        # a beast that appears in both.
        # **Only what the op CONSUMES at the tile, never what it carries along.** Using `j.needs`
        # wholesale blocked PLACE: `PLACE_DRAWS_FEED` puts a day's wheat into `needs`, so an empty
        # shed refused the animal itself. Day 4 measured `place 0/1` and `cow 4/5` against `1/1` and
        # `5/5` before -- one cow placed a day late, for want of wheat the PLACE does not spend.
        want = j.places()
        if SUPPLY_LIMITS_EVERY_DRAW:
            want = want | collections.Counter(
                i for o, i in j.ops if i and o in SUPPLY_CHECKED_OPS)
        return collections.Counter({i: q - held[i] for i, q in want.items() if q > held[i]})

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
                        got = slot_now(u, j, cap[u])
                        if got is None:
                            continue
                        key = (got[0] - used[u], u, j.tile, got[1])
                        if best is None or key < best[0]:
                            best = (key, j, u, got[1], got[0])
                if best is None:
                    break                          # nothing more fits under this cap; relax it
                _k, j, u, i, c = best
                routes[u].insert(i, j)
                touch(u)
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
                        # `rest` is not `routes[u]` -- it is `routes[u]` minus `j` -- so the memo
                        # cannot answer for the home unit. Every other unit is untouched and can.
                        got = slot(v, j, rest) if v == u else slot_now(v, j)
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
                        touch(u)
                    else:
                        routes[u] = rest
                        used[u] = without
                        routes[v].insert(i, j)
                        used[v] = c
                        touch(u)
                        touch(v)
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
                        alt = slot_now(v, m)
                        if alt is not None and (home is None or alt[0] - used[v] < home[0]):
                            home = (alt[0] - used[v], v, alt[1], alt[0])
                    if home is None:
                        continue
                    _d, v, vi, vc = home
                    routes[u] = keep[:got[1]] + [j] + keep[got[1]:]
                    used[u] = got[0]
                    routes[v].insert(vi, m)
                    used[v] = vc
                    touch(u)
                    touch(v)
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
                at_risk=getattr(n, "critical", False),
                products=yield_products(n, tiles)) for n in nodes]


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
    # **`node.tile` is `(x, y)` and the board is `tiles[y][x]`. This is NOT a transposition bug.**
    # Written down because it was "fixed" once, on 2026-08-10, on the strength of the d4 pen block
    # -- pens at `tiles[3][3] [3][4] [4][2] [4][3] [4][4]` against jobs `Job(3,3) Job(3,4) Job(4,2)
    # Job(4,3) Job(4,4)`, which is very nearly symmetric and fits BOTH readings. The decisive case
    # is a job off that diagonal: on `seb1326` d4 the FEED job's tile is `(1,4)`, there is no animal
    # at `tiles[1][4]`, and there is one at `tiles[4][1]`. `_router_acts` reads
    # `tiles[node.tile[1]][node.tile[0]]` for the same reason.
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


def yield_products(node, tiles):
    """WHICH products a yielding node will put in the hand. Quantity deliberately not consulted.

    `predict_yield` answers "how many", and returns nothing at all when `yield_units` is still 0 at
    dawn -- which is the normal state of a one-shot crop that ripens during the day. That is the
    right under-estimate for deciding whether a load justifies a MID-TOUR detour.

    It is the wrong question for deciding whether the tour needs to end at the shed. Measured on
    91422988, seed 11, day 10: u9 harvests 12 MELON between h12 and h15 and carries them to h23. The
    row asks for MELON 18, the shed reads empty from h1 to h23, the bank sits at $37, the d10 wheat
    order is never placed, and the cow at (4,2) misses d10 and d11 and is removed on d13. Every
    melon tile read `yield_units = 0` at dawn, so `gives` was empty and no delivery was ever planned.

    The PRODUCT is knowable at dawn even when the quantity is not: it is the crop in the ground, or
    the animal in the pen. That is all this returns.

    **`node.tile` is `(x, y)` and the board is `tiles[y][x]`. That is not a bug -- see
    `predict_yield`, where the decisive measurement is recorded.** This read was "corrected" to
    `tiles[i][j]` on 2026-08-10 off a near-symmetric pen block that fits either reading, which is
    exactly how a convention gets flipped by accident.
    """
    if tiles is None:
        return frozenset()
    x, y = node.tile
    try:
        cell = tiles[y][x]
    except (IndexError, TypeError):
        return frozenset()
    if not isinstance(cell, dict):
        return frozenset()
    out = set()
    for op, _item in node.ops:
        if op == "COLLECT_FERTILIZER":
            out.add("FERTILIZER")
        elif op == "HARVEST":
            out.add(R.ANIMALS[cell["animal"]]["product"] if "animal" in cell else cell.get("crop"))
    return frozenset(p for p in out if p)


def plan(units, jobs, budget, depots=SHED, carry=None, supply=None, deliver=True, wanted=None,
         rush=False, day=None, due=None):
    """`cover`, materialised, in the shape `schedule_agent` already consumes."""
    depots = tuple(depots) or SHED
    # **The crew planner, on the days it has been measured for.** Same signature, same return shape,
    # so everything below is unchanged. Imported here and not at module scope because `crew` imports
    # this module. `crew.ACTIVE_UNTIL_DAY` is 0 until a day's grid says otherwise.
    from . import crew as CREW
    assign = (CREW.cover if day is not None and (day < CREW.ACTIVE_UNTIL_DAY
                                                or day in getattr(CREW, 'ACTIVE_EXTRA_DAYS', ()))
              else cover)
    work, left = assign(units, jobs, budget, depots, carry, supply, deliver, wanted, day, rush, due)
    out = {}
    for u, seq in work.items():
        held = (carry or {}).get(u) or {}
        route = materialise(units[u], seq, held, depots, wanted, False, rush, due=due)
        cost = turns(units[u], route)
        # The closing trip, out of the turns the tour did not spend. See the note in `cover.cost`:
        # it is worth having and it is never worth a job, so it goes on last and only if it fits.
        if deliver:
            home = materialise(units[u], seq, held, depots, wanted, True, rush, due=due)
            if turns(units[u], home) <= budget[u]:
                route, cost = home, turns(units[u], home)
            elif TRIM_A_TAIL_THAT_CANNOT_COME_HOME and wanted and day in RANK_HOME_DAYS:
                # **The trailing job is producing goods that will be STRANDED, so dropping it is a
                # gain and not a trade.** u1 on d4 harvests (2,1) at h15 and (1,1) at h18, ends six
                # steps from the shed with eight wheat and passes to dusk; the rollover sweeps it
                # into the shed after the market has closed. Give up the second harvest and the
                # first four units get sold. The turns were being spent either way.
                #
                # Only when the tour cannot come home AND ends holding something today's row wants
                # -- `materialise(deliver=True, wanted_only=True)` is that question -- so a tour
                # carrying nothing the market is waiting for is never shortened.
                trimmed = list(seq)
                while trimmed:
                    trimmed.pop()
                    alt = materialise(units[u], trimmed, held, depots, wanted, True, rush,
                                      wanted_only=True, due=due)
                    if not any(getattr(st, "depot", False) and st.drop for st in alt):
                        break            # nothing left worth carrying home; keep the longer tour
                    if turns(units[u], alt) <= budget[u]:
                        route, cost = alt, turns(units[u], alt)
                        break
        out[u] = dict(route=route, draw=draws(route),
                      depot=(next((s.tile for s in route if getattr(s, "depot", False)), None)),
                      cost=cost)
    return out, left
