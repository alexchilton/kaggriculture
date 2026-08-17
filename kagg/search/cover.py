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

#: Whether a tile one dry night from weeding is covered BEFORE a pen that was fed yesterday.
#:
#: `REQUIRED_OPS` above argues that a pen fed yesterday can slip a day for free while one that
#: missed yesterday cannot. The same logic applies to tiles, and the pass order contradicted it:
#: the routine feeds went first and the dying tiles took what was left.
AT_RISK_TILE_OUTRANKS_A_FEED_THAT_CAN_SLIP = False

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

#: How many hands to try emptying for one job, cheapest to reach first, and how many stops may be
#: shed from one hand. Both bound the work: this pass is O(jobs x hands x stops x moves) in `slot`,
#: which is the call that disqualified submission 55352401 on time. It only runs at all when the
#: greedy, `COMPACT` and `REPAIR` have all left something on the board.
MAKE_ROOM_HANDS = 3
MAKE_ROOM_MOVES = 8

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

#: Days on which a job whose tile dies tonight is kept OFF the tail of a tour.
#:
#: `at_risk` already decides which jobs get COVERED -- the greedy passes run at-risk jobs early --
#: but it never touched WHERE in the tour they land, and `slot` takes the cheapest position, which
#: for an outlying tile is the end. That is the position that evaporates when a hand wakes one or two
#: turns from where its tour was priced. Every tile lost in a season dies that way.
#:
#: Scoped rather than global BY MEASUREMENT. Global is a loss (weeds 3 -> 5, two NEW weeds at d10):
#: on a genuinely full tour reordering does not save a stop, it only changes which stop is lost.
#: These are the days where an earlier slot exists inside the same budget. Measured, seed 11:
#: weeds one fewer EVERY day from d11, `strawb` d11 36/36 exact, `wheat` d13-d17 13/13 exact.
#:
#: A hard-coded day list, tuned on one seed, and expected to dissolve once the packer chooses
#: positions properly. Empty restores prior behaviour. NOT ladder-tested.
AT_RISK_NOT_LAST_DAYS = (11, 12, 13, 18, 19)
AT_RISK_TAIL_PENALTY = 2

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

#: Whether a hand may bank produce **today's row is selling** at a zero-detour depot while harvests
#: remain -- using the QUANTIFIED `PLACE`, never the all-or-nothing `DROP`.
#:
#: `BANK_ONLY_AFTER_THE_LAST_HARVEST` is read off Seb's day 4, where the harvest is REVENUE: nothing
#: that day depends on it, so it can ride to the closing trip. Day 8 of the Kawashigi tape inverts
#: that. `COW` is `first_yield_day 8`, so the two cows placed on day 0 open d8 holding six units
#: each -- and both boards agree on it, ours `CO@3,4 y6 CO@4,4 y6` against his `CO@4,3 y6 CO@4,4 y6`,
#: with the full care bonus consumed on both sides. The row is `sells {FERTILIZER 6, MILK 12}` and
#: `buys {WHEAT 17}` on a $4 dawn bank, so the milk is not revenue, it is the day's WORKING CAPITAL:
#: the wheat it pays for is what feeds ten animals. Measured, seed 11:
#:
#:     h05 u4 HARVEST   h08 u4 HARVEST   h09-h17 twelve milk in hand, bank $13
#:     h17 u4 DROP      h18 shed 12, SELL MILK 12   h19 bank $1,873 -- every stop already walked
#:
#: We harvest all twelve and sell all twelve, thirteen hours late. The tape banks the same milk at
#: h05 with two `PLACE/MILK` and spends it through the day; it closes `feed 10/10 care 10/10`
#: against our 2 and 2. The whole d8 deficit is delivery LATENCY -- not production, not routing
#: (`crew.cover` covers 39/39), not the size of the wheat row.
#:
#: **Why this is not `BANK_MID_TOUR_WHEN_THE_DAY_IS_UNFUNDED` again.** That one gated on `rush`, the
#: short-of-cash signal -- which was False on the d10 it was written for and True on d6, where the
#: extra drops shifted the cash timing and cost `buy_product 5/5 -> 4/5`. The gate here is not
#: poverty, it is **"the hand is carrying what today's row sells"**: `wanted` is the sell row, so the
#: stop only opens where the day's own plan is waiting on those goods. d6's hands are not carrying
#: d6's produce at the blocked stops, which is the difference the measurement has to confirm.
#:
#: **It has to be folded into `reaping` itself, not into one branch.** Traced on d8, all 1,678
#: blocked stops look like `free=True spare=7 owed=False held={FERTILIZER 1, MILK 6} after={}` --
#: nothing owed ahead, so they fall to the FREE DROP and never reach the selective `_bank` branch,
#: which requires `owed_ahead`. An exemption written for the selective branch alone measured as a
#: byte-identical d8. And the free drop is safe here by construction: it already refuses whenever
#: anything in the hand is owed ahead, so the all-or-nothing `DROP` cannot bin a ration.
BANK_THE_ROWS_PRODUCE_WHILE_REAPING = False

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
        #
        # **A WATER already in the list only covers the PLANT if the tile is not being harvested
        # first.** A mature tile that is reaped and immediately re-sown reads
        # `[WATER, HARVEST, PLANT]`, and that water is the OLD crop's -- on a one-shot it *is* the
        # yield (`router.crop_ops`), which is why it precedes the HARVEST. The seed that goes in
        # afterwards still needs its own. Victor's d8: u6 waters (0,2) at h17, harvests h18, plants
        # h19 and waters again h20 -- four turns against a job costed at three -- so a tour costed at
        # exactly its 23-turn budget reached its last stop at h22 with three ops and two hours, and
        # the day's tenth planting was never emitted.
        _plants = any(o == "PLANT" for o, _i in self.ops)
        _waters = any(o == "WATER" for o, _i in self.ops)
        _reaps = any(o == "HARVEST" for o, _i in self.ops)
        self.turns = len(self.ops) + (1 if _plants and (_reaps or not _waters) else 0)
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

    `place` is the third way, and it is the one that CAN pick the wool out of that hand: a
    shed-adjacent `PLACE <item> <n>` banks n of one item and nothing else
    (`kaggriculture.py:381-395`). `_bank` decides between it and `drop` on cost alone.
    """

    __slots__ = ("tile", "drop", "pick", "place", "critical")

    depot = True
    needs = ()
    gives = ()
    products = frozenset()
    required = False
    at_risk = False
    only = None

    def __init__(self, tile, drop=False, pick=None, critical=False, place=None):
        self.tile = tuple(tile)
        self.drop = bool(drop)
        self.pick = collections.Counter({i: q for i, q in (pick or {}).items() if q > 0})
        #: Items to bank with `PLACE <item> <n>` instead of dumping the hand. A shed-adjacent PLACE
        #: is a QUANTIFIED shed drop (`kaggriculture.py:381-395`): it moves n of one item and leaves
        #: the rest of the inventory alone. `DROP` cannot -- it is all-or-nothing
        #: (`kaggriculture.py:333`) -- which is why a stop that banks produce and keeps its ration
        #: has to pay twice with `drop`, and once with this. See `BANK_THE_SURPLUS_NOT_THE_HAND`.
        self.place = collections.Counter({i: q for i, q in (place or {}).items() if q > 0})
        #: Whether this draw serves a job that dies TONIGHT if it is skipped (`Job.at_risk and
        #: Job.required` -- an animal one missed feed from escaping). Set by `materialise`, which
        #: alone knows which jobs the draw is FOR; the executor reads it to decide whether a shed
        #: that cannot fill the want right now is worth standing at and retrying, or worth walking
        #: away from as before. See the note where the executor reads it.
        self.critical = bool(critical)

    @property
    def turns(self):
        # One turn per PLACE, because PLACE names one item: `kaggriculture.py:381` reads
        # `action[1]` and `action[2]`, so two items to bank is two turns.
        return (1 if self.drop else 0) + len(self.place) + len(self.pick)

    @property
    def service(self):
        return self.turns

    @property
    def ops(self):
        out = [("DROP", None)] if self.drop else []
        out += [("PLACE", i) for i in sorted(self.place)]
        return out + [("PICKUP", i) for i in sorted(self.pick)]

    def places(self):
        return collections.Counter()

    def yields(self):
        return False

    def harvests(self):
        return False

    def __repr__(self):
        bits = ((["DROP"] if self.drop else [])
                + [f"PLACE:{i}x{q}" for i, q in sorted(self.place.items())]
                + [f"{i}x{q}" for i, q in sorted(self.pick.items())])
        return f"Shed{self.tile}[{'+'.join(bits) or '-'}]"


def _bank(tile, held, need, critical=False):
    """The cheapest shed stop that arrives holding `held` and leaves holding `need`.

    Two ways to do it, and they cost differently:

        DROP  + PICKUP per item still owed        1 + len(need - held ... all of need)
        PLACE per item banked + PICKUP per short  len(held - need) + len(need - held)

    The second is what `BANK_THE_SURPLUS_NOT_THE_HAND` buys. Both leave the hand holding exactly
    `need`, so this is a cost choice and nothing else; whichever is cheaper wins, ties to `DROP`
    because that is the behaviour every measurement in this file was taken against.

    **An animal in the hand forces `DROP`.** `PLACE` on a built, empty pen puts the beast in the pen
    rather than the shed (`kaggriculture.py:370-378`), and `_refresh_pins` sites pens ON shed-access
    tiles -- so the selective drop is not selective for livestock, it is a placement.
    """
    drop = Depot(tile, drop=True, pick=need, critical=critical)
    if any(q > 0 and i in R.ANIMALS for i, q in held.items()):
        return drop
    give = collections.Counter({i: q - need.get(i, 0) for i, q in held.items()
                                if q > need.get(i, 0)})
    take = collections.Counter({i: q - held.get(i, 0) for i, q in need.items()
                                if q > held.get(i, 0)})
    keep = Depot(tile, pick=take, place=give, critical=critical)
    return keep if keep.turns < drop.turns else drop


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
        contested = (any(wanted.get(p, 0) > 0 for p, q in after[i].items() if q > 0))
        # **Is there still a harvest ahead on this tour?** See `BANK_ONLY_AFTER_THE_LAST_HARVEST`.
        # `work[i:]` includes the job about to be walked to, which is right: a drop planned on the
        # way TO a harvest is as early as one planned between two.
        # `rush` exempts it: see `BANK_MID_TOUR_WHEN_THE_DAY_IS_UNFUNDED`. A day that cannot pay its
        # own bill needs the produce in the shed while the market is open, not swept there overnight
        # by `_drop_inventories_to_shed` after it has closed.
        # **A short day, and the hand is holding what that day's row SELLS.** See
        # `BANK_THE_ROWS_PRODUCE_WHILE_REAPING`. Both halves are load-bearing and neither works
        # alone: `rush` by itself is the reverted `BANK_MID_TOUR_WHEN_THE_DAY_IS_UNFUNDED`, which
        # fired on fertilizer rounds too; the row test by itself is true on Seb's day 4, where
        # fourteen wheat harvests meet a `WHEAT 49` row and the dusk rule is exactly right.
        funding = (BANK_THE_ROWS_PRODUCE_WHILE_REAPING and rush
                   and any(wanted.get(p, 0) > 0 and q > 0 for p, q in held.items()))
        reaping = (any(w.harvests() for w in work[i:])
                   
                   and not funding)
        if free and spare > 0 and not owed_ahead \
                and not reaping:
            route.append(Depot(d, drop=True))
            held = collections.Counter()
            pos = d
        elif (free and spare > 0 and owed_ahead and not contested
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
            route.append(_bank(d, held, back))
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
        # **A load with no later delivery ships now, `DELIVER_MIN` notwithstanding.** See
        # `SHIP_WHAT_NO_LATER_STOP_CAN_BANK`: with the closing trip uncharged and no remaining stop
        # on a depot tile, there is nothing to batch FOR -- the load is stranded by construction.
        # The `due` clock is deliberately not consulted for it: `tail` prices a closing drop that
        # `deliver=False` never plans, so "the tour delivers in time on its own" is fiction here.
        stranded = (not deliver and load > 0
                    and pos not in depots
                    and all(tuple(w.tile) not in depots for w in work[i:]))
        if not reaping and (stranded or (load >= DELIVER_MIN and (
                due is None or turns(start, route) + dist(pos, j.tile) + tail[i] > due))):
            d = nearest(depots, pos, j.tile)
            # The drop takes the wheat with it, so the same stop draws back everything still ahead --
            # unless `_bank` can shed the produce alone with PLACE and keep the ration in hand.
            back = collections.Counter({it: q for it, q in after[i].items() if q > 0})
            route.append(_bank(d, held, back))
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
        # **Bank on the pen, before moving on.** See `BANK_ON_THE_PEN_THAT_FUNDS_THE_DAY`. Every
        # path above plans its stop as part of the walk to the next job, so none of them can say
        # "bank here, now" -- and standing on a pen IS standing on the shed, because `_refresh_pins`
        # sites pens on shed-access tiles. One turn, no movement, and `_bank` keeps the ration.
        # The test is on what THIS PEN yielded, not on what the hand happens to be carrying: a hand
        # holding the herd's wheat on a day whose row sells wheat would otherwise bank at every pen.
        # Same shape as `funds` itself in `_solve` -- `any(owed[p] > 0 for p in j.gives)`.
        _earns = any((wanted or {}).get(p, 0) > 0 and q > 0 for p, q in j.gives.items())
        if j.funds and pos in depots and _earns:
            keep = collections.Counter({it: q for it, q in after[i + 1].items() if q > 0})
            route.append(_bank(pos, held, keep))
            held = collections.Counter(keep)
        elif (j.funds and _earns
                and pos not in depots
                and all(o == "HARVEST" for o, _i in j.ops)):
            # **The errand.** See `THE_FUNDING_HARVEST_RUNS_ITS_LOAD_IN`. Scoped to a job that is
            # ONLY a harvest, which is exactly what `split_funding_harvest` produces -- a tending
            # stop that happens to hold produce is not worth a trip and is left to the ordinary
            # delivery rules. Aimed at the depot nearest the next stop, so the walk is shared.
            _nxt = work[i + 1].tile if i + 1 < len(work) else pos
            d = nearest(depots, pos, _nxt)
            keep = collections.Counter({it: q for it, q in after[i + 1].items() if q > 0})
            route.append(_bank(d, held, keep))
            held = collections.Counter(keep)
            pos = d

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


#: Days it applies. d4 is the day it exists for: 28 wheat and 4 fertilizer in hands at dusk against
#: a row asking for 49 and 6.
RANK_HOME_DAYS = frozenset({4})

#: Whether a tour that cannot get its load home gives up trailing jobs until it can. Never a trade:
#: the produce those jobs make is stranded by definition, so the turns buy nothing as things stand.
TRIM_A_TAIL_THAT_CANNOT_COME_HOME = True

#: The days the trim may fire. **Only the last day, and the reason is the overnight sweep.** On
#: every other day `_drop_inventories_to_shed` banks whatever a tour ends up holding, so a kept job
#: always beats a walk and the trim is a pure loss -- which is why it shipped False for d4. On d29
#: the sweep lands after the market is gone and the kept job's produce is DISCARDED, so the walk
#: is worth strictly more than the job by construction. The reserve pricing cannot reach a
#: precomputed day (`_apply_precomputed` seats stops without pricing them); this trim in `plan` is
#: the one place a solved d29 tour can shed work for its delivery.
TRIM_HOME_DAYS = frozenset({29})


#: **Routes solved OFFLINE and replayed, keyed by day.** `{day: {unit: [(tile, (ops...)), ...]}}`
#:
#: The board has no random terrain -- `_initial_tile` is a pure function of coordinates and the only
#: RNG in `kaggriculture.py` (line 858) drives the shop draw and weed spawns -- so geometry, depots
#: and every walking distance are identical in every game. A day solved once is reusable, and the
#: 1s/turn `actTimeout` stops being a limit on route QUALITY: solve it offline with as long as it
#: takes (`scripts/solve_day.py`), ship the answer. See
#: `docs/the_route_is_precomputable_2026-08-12.md`.
#:
#: Measured on d12, seed 11: the greedy seats 45 of 47 and leaves `(9,0)` and `(9,1)` while 51 turns
#: of slack sit across the crew. The offline solve seats 47/47 in 169 turns with TWO hands never
#: leaving the shed.
#:
#: **Never silently.** Every stop a day could not fill is recorded in `PRECOMPUTED_MISSES`, so a
#: route that did nothing is distinguishable from a route that ran -- a silent no-op reads exactly
#: like a measured null, which this project has been bitten by.
#:
#: Loaded from `solved_days.py`, which is generated by `scripts/solve_day.py`. Set to `{}` to switch
#: the whole mechanism off and run the greedy everywhere.
from .solved_days import SOLVED_DAYS                                          # noqa: E402

#: **Days the greedy plans itself even though a solved route exists.**
#:
#: A solved route stores WORK STOPS only -- `(tile, ops)` -- and `materialise` appends the shed trip
#: afterwards out of whatever turns the tour did not spend. That is fine on any day whose load is
#: banked for free by `_end_of_day`, and it is exactly wrong on the LAST day, where the automatic
#: drop happens after the final turn and `_commit_unit` will not sell out of a hand. d29 has no
#: slack to append into, so the walk home never gets planned and the season ends with the crew
#: holding sellable produce.
#: **MEASURED AND PARKED 2026-08-15.** `(29,)` lets the greedy plan the last day with `deliver=True`
#: and is a real but small gain -- sell 1489 -> 1502, d29 sell 93 -> 106, season +$256, harvest
#: 396 -> 393. It does NOT fix the problem: stranded units rose 51 -> 78, because the greedy
#: harvests more on d29 than it can walk in.
#:
#: **The reason it is parked is that d29 is the wrong day to fix.** カワシギ harvests 32 on d28 to
#: our 27 and only 19 on d29 to our 27, then spends d29 selling -- 148 units to our 93, with 56 PASS
#: turns. `_end_of_day` delivers d28's load to the shed overnight for free. He never plans a d29
#: delivery because he does not need one. We back-load 10 harvests into d23-d29 (195 against his
#: 185) while d0-d22 are level (201 against 204). Move the work to d28 and the delivery is free.
UNSOLVE_DAYS = ()

PRECOMPUTED_ROUTES = {d: {u: [(tuple(t), tuple(ops)) for t, ops in seq]
                          for u, seq in units.items()}
                      for d, units in SOLVED_DAYS.items() if d not in UNSOLVE_DAYS}

#: **On the LAST day a stop whose ops shrank keeps its solved seat.** `_apply_precomputed` keys a
#: stop on the exact `(tile, ops)` tuple, which is right on an ordinary day -- a tuple that stops
#: matching means the board is not the board the day was solved for -- and is the recorded landmine
#: on d29: `NO_UPKEEP_ON_THE_LAST_DAY` strips FEED/CARE from a pen's job, the key stops matching,
#: and the stop leaves the solved route for greedy insertion instead of getting two turns cheaper.
#: Measured as harvest 396 -> 389, sell 1489 -> 1474 (see `router.NO_UPKEEP_ON_THE_LAST_DAY`).
#:
#: The fallback fires only on `SEASON_DAYS - 1`, only when the exact key misses, and only for a job
#: at the SAME tile whose op set is a SUBSET of the solved stop's -- a reduced form of the work the
#: solve described, never new work. Everything else stays a recorded miss, and every earlier day
#: keeps the exact-key rule byte-identical.
MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE = True

#: Days where a precomputed route was offered and did not fit today's jobs. Read it after a run --
#: if the day under test is in here, the route never ran and the numbers mean nothing.
PRECOMPUTED_MISSES = []


def _apply_precomputed(day, units, jobs, budget, depots, carry, wanted, deliver, rush, due):
    """Seat `jobs` per `PRECOMPUTED_ROUTES[day]`. Partial matches are kept, not thrown away.

    **This used to be all-or-nothing and that made the routes useless off their own tape.** A solved
    day names each stop by `(tile, ops)`. Seeds do not move that list -- the board has no random
    terrain, so d12 and d16 matched exactly on seed 11 and seed 14 alike -- but an OPPONENT does,
    because our shed depends on what the market gave us and `build_nodes` gates animal work on
    having wheat. Measured against three other tapes, d12 and d16 each missed by exactly ONE job:

        tape victor seed 11   MISSES: []          tape seb        (12, "no job (6,4) FEED/CARE/...")
        tape victor seed 14   MISSES: []          tape seb1326    identical
                                                  tape oldleader  identical

    One job in sixty, and the whole solved day was discarded for it. Now a stop the day cannot fill
    is skipped and everything else is still seated; the jobs left over go through the same cheapest
    feasible insertion the greedy uses, so they are routed rather than dropped.

    A crew SMALLER than the plan expects is not a bail either: unit indices are positional, so a tour
    written for a hand that does not exist cannot be seated on someone else, but its jobs are simply
    left for the insertion below rather than thrown away with the rest of the day.

    The one remaining fallback is a plan that matches NOTHING, which means it describes a board this
    game never reached. There the greedy is the known-good path and this has no information to add.
    """
    plan = PRECOMPUTED_ROUTES.get(day)
    if not plan:
        return None
    pool = {}
    for j in jobs:
        pool.setdefault((tuple(j.tile), tuple(o[0] for o in j.ops)), []).append(j)
    routes = {u: [] for u in range(len(units))}
    missed, no_unit = [], 0
    for u_str, work in plan.items():
        u = int(u_str)
        for tile, ops in work:
            key = (tuple(tile), tuple(ops))
            if not pool.get(key):
                # The last day only: seat a REDUCED form of the solved stop -- same tile, ops a
                # subset of what the solve described. See `MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE`.
                fallback = None
                if MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE and day == R.SEASON_DAYS - 1:
                    fallback = next((k for k, lst in pool.items()
                                     if lst and k[0] == tuple(tile) and set(k[1]) <= set(ops)),
                                    None)
                if fallback is None:
                    missed.append(key)
                    continue
                key = fallback
            if u >= len(units):
                no_unit += 1          # the hand never arrived; its work goes through insertion
                continue
            routes[u].append(pool[key].pop())
    if no_unit:
        PRECOMPUTED_MISSES.append((day, "crew is %d units, plan wants more; %d stop(s) re-homed"
                                   % (len(units), no_unit)))
    if missed:
        PRECOMPUTED_MISSES.append((day, "skipped %d stop(s) the board does not have: %s"
                                   % (len(missed), missed[:4])))

    seated = {id(j) for work in routes.values() for j in work}
    left = [j for j in jobs if id(j) not in seated]
    # **A hand is never given more tour than its day can walk.** See `_trim_to_the_day`. The stops
    # this releases join `left`, so they go through the same at-risk-first insertion as everything
    # else rather than sitting past the end of a tour nobody priced.
    left += _trim_to_the_day(routes, units, budget, depots, carry, wanted, deliver, rush, due)
    if left:
        left = _insert_leftovers(routes, left, units, budget, depots, carry, wanted, deliver, rush,
                                 due)
    return routes, left


def _trim_to_the_day(routes, units, budget, depots, carry, wanted, deliver, rush, due):
    """Drop the tail of any seated tour that costs more turns than the unit has. Returns the drops.

    **A hand is never given more tour than its day can walk.**

    Every other seating path in this file already obeys that rule: `slot`/`claim` price a job
    against `budget[u]` before taking it, and `_insert_leftovers` prices each insertion the same
    way. `_apply_precomputed` is the exception -- it seats the solved stops by name and prices
    nothing, which `TRIM_HOME_DAYS`' note above states outright. A day is 24 turns whether or not
    anyone counted them, so the surplus stops do not happen; they are simply never reached, and
    nothing reports it. `PRECOMPUTED_MISSES` records a stop the board could not FILL and has no
    entry for a stop that was seated and then never walked to.

    Measured on tape `kawashigi`, seed 11, `weedSpawnChance` 0.005 (`data/logs/over_budget_-
    kawashigi_s11.log`): ten tours across d16-d28 are planned past the day, u3 on d23 by ten turns,
    and eleven WATER stops sit past the cut. The tiles those waters name are the tiles that weed
    that same night -- (1,4) and (0,4) on d16, (0,5) on d19, (6,2) on d26, (8,7) on d27. A
    STRAWBERRY is `ongoing`, so a tile at `consecutive_unwatered == 1` has exactly one water
    between it and a WEED, and that water was being planned into turns nobody had.

    Trimming from the END is not a preference, it is what the runtime already does -- the tour is
    walked in order and stops when the turns run out. The difference is that a released stop is now
    VISIBLE: it joins `left`, and `_insert_leftovers` sorts `left` at-risk first, so a water on a
    tile that dies tonight is re-seated on whichever hand still has slack instead of being
    abandoned on the hand that ran out.

    **TRIED AND REVERTED: give up the last SLIPPABLE stop rather than the last one**, so a tile one
    dry night from weeding outranks a stop that only costs a day's delay. The clause is not dead --
    on seed 11 it fires on 2 of the 13 over-budget tours and picks a different stop
    (`data/logs/does_slip_fire_s11.log`) -- and it is a MEASURED NULL: the acceptance gates return
    a byte-identical failing set (359 failed, 542 passed, 115 xfailed, 35 xpassed) and the season
    weeds exactly the same nine tiles on exactly the same days. The reason is that the released
    stop goes to `_insert_leftovers` either way, and that already sorts at-risk first, so the
    ordering was being applied twice. Reverted per protocol; recorded so it is not re-derived.

    This does not decide what to give up when the day is genuinely too full. That was already
    `_insert_leftovers`' job; this only makes it reachable on a solved day.
    """
    dropped = []
    for u, seq in routes.items():
        held = (carry or {}).get(u) or {}

        def fits(work):
            tour = materialise(units[u], list(work), held, depots, wanted, deliver, rush, due=due)
            return tour is not None and turns(units[u], tour) <= budget[u]

        if fits(seq):
            continue
        # `deliver` is the same question `plan` asks of the finished tour, so a tour trimmed here
        # is trimmed against the cost model it will actually be charged at.
        keep = list(seq)
        while keep and not fits(keep):
            dropped.append(keep.pop())
        routes[u] = keep
    return dropped


def _insert_leftovers(routes, left, units, budget, depots, carry, wanted, deliver, rush, due):
    """Cheapest feasible insertion for jobs a partial route did not seat. Returns what would not fit.

    Priced through `materialise`/`turns` like everything else here, so an insertion that claims to
    fit really does fit the same cost model the tour was solved under.
    """
    def cost(u, seq):
        tour = materialise(units[u], list(seq), (carry or {}).get(u), depots, wanted, deliver, rush,
                           due=due)
        return None if tour is None else turns(units[u], tour)

    over = []
    for j in sorted(left, key=lambda j: (-int(bool(j.at_risk)), -int(bool(j.required)))):
        best = None
        for u, seq in routes.items():
            base = cost(u, seq) or 0
            for pos in range(len(seq) + 1):
                c = cost(u, seq[:pos] + [j] + seq[pos:])
                if c is None or c > budget[u]:
                    continue
                if best is None or c - base < best[0]:
                    best = (c - base, u, pos)
        if best is None:
            over.append(j)
            continue
        _d, u, pos = best
        routes[u] = routes[u][:pos] + [j] + routes[u][pos:]
    return over


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
    pre = _apply_precomputed(day, units, jobs, budget, depots, carry, wanted, deliver, rush, due)
    if pre is not None:
        return pre
    routes = {u: [] for u in range(len(units))}
    left = list(jobs)
    stock = collections.Counter(supply) if supply is not None else None
    booked = collections.Counter()

    def load(u):
        return carry.get(u) or {}

    #: Whether `slot` ranks candidate positions by the tour INCLUDING its trip home. See the note
    #: in `slot`. Scoped to the same day set as the hard reserve plus the days that strand produce.
    rank_home = False

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
        #
        # **And it may only price a tour the caller is going to ASK FOR.** `deliver` decides whether
        # `plan` ever materialises the closing walk, and the shipped agent sets
        # `deliver = max(budget) > DELIVER_CUTOFF_TURNS` with the cutoff at 99 against budgets of
        # 23-24 -- so `deliver` is always False and the closing walk is never planned. Pricing the
        # reserve anyway measured a tour that does not exist, and it measured it CHEAP: with no walk
        # home, `materialise` inserts mid-tour shed trips instead so the load is not stranded past
        # market close, and those trips are not in the delivering tour. Seed 11, day 10, unit 9, one
        # sequence priced both ways:
        #
        #     deliver=True, wanted_only=True   21 turns   SHED -> (7,4) -> (6,4) -> (6,3) -> (5,3) -> SHED
        #     deliver=False                    29 turns   SHED -> (7,4) -> SHED -> (6,4) -> SHED -> (6,3) -> (5,3)
        #
        # Budget 23. The packer admitted 21 turns of work, the day walked 29, and the last two stops
        # were never reached -- both of them FEEDs. `consecutive_unfed >= 2` deletes the animal
        # (`kaggriculture.py:817`), so the same overrun two days running is a $400 asset gone and a
        # pasture idle for the rest of the season. Seen on the ladder in 93186363, 93237183 and
        # 93239838, each losing tile (6,4) on day 11.
        if deliver and wanted and day in RESERVE_DAYS:
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
    for j in jobs:
        if any(o == "BUILD" for o, _i in j.ops):
            build_at[tuple(j.tile)] = j

    def slot(u, j, base, limit=None):
        """Cheapest position for `j` in unit `u`'s `base` sequence within `limit` turns, `(cost, i)`."""
        if j.only is not None and j.only != u:
            return None
        first = 0
        if any(o == "PLACE" for o, _i in j.ops):
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
            if (day in AT_RISK_NOT_LAST_DAYS and j.at_risk
                    and i == len(base) and len(base) > 0):
                rank += AT_RISK_TAIL_PENALTY
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
                        # **A second funding pen prefers a hand that has none.** See
                        # `ONE_HAND_PER_FUNDING_PEN`. Leads the key, so it outranks travel cost --
                        # the value of these two stops is the HOUR they finish, not the walk they
                        # cost. It only ever discriminates between feasible slots, so a funding pen
                        # with nowhere else to go is still placed by the same pass.
                        stacked = (j.funds
                                   and any(x.funds for x in routes[u]))
                        key = (stacked, got[0] - used[u], u, j.tile, got[1])
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
    if AT_RISK_TILE_OUTRANKS_A_FEED_THAT_CAN_SLIP:
        # **A tile that weeds tonight is an asset lost outright; a pen fed yesterday can slip a day
        # for free.** That is this file's own argument for `at_risk`, applied to the other half of
        # the board. Ordered the other way, a routine feed took the turn and the tile died: measured
        # on live ladder games 2026-08-16, (8,4) STRAWBERRY died d9 last watered d6, (9,1) WHEAT and
        # (9,2) STRAWBERRY died d11 last watered d8, and the same coordinates die across independent
        # games and seeds. At d8 dusk eight tiles sat one night from death while sixteen others were
        # watered.
        #
        # NOT the d28 null recorded at `schedule_agent.BANK_THE_FIELD_ON_D28`: that measured RIPE
        # tiles on a SOLVED day with two hands idle and slack in the route. These are DRY tiles on
        # d7-d11, which are unsolved and turn-constrained.
        greedy([j for j in left if j.at_risk and not j.required])  # a tile that weeds tonight
        greedy([j for j in left if j.required and not j.at_risk])  # the rest of the herd
    else:
        greedy([j for j in left if j.required and not j.at_risk])  # the rest of the herd
        greedy([j for j in left if j.at_risk and not j.required])  # a tile that weeds tonight
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
                        # **Compaction must not undo the funding spread.** See
                        # `ONE_HAND_PER_FUNDING_PEN`. This loop accepts any move that lowers total
                        # turns, and stacking the second funding pen back onto the hand already
                        # standing on the first always does -- which is how the spread was measured
                        # to survive `greedy` and then vanish before the tour was built.
                        if (j.funds and v != u
                                and any(x.funds for x in routes[v])):
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

    # ---------------------------------------------------------------------------------- make room
    # See `MAKE_ROOM`. Everything above ranks on turns SAVED; this ranks on turns FREED, on the one
    # hand that can reach the job. Commits only when the job actually seats, so coverage is
    # monotone and the outer loop terminates on a bounded quantity.
    def _reach(u, j):
        """Marginal cost of `j` on `u`'s route with the budget ignored. `None` if it cannot go."""
        got = slot(u, j, routes[u], limit=float("inf"))
        return None if got is None else got[0] - used[u]

    def _make_room(u, j):
        """Shed stops off `u` onto hands that can pay for them until `j` fits. `(routes, used)`."""
        trial = {v: list(routes[v]) for v in range(len(units))}
        tused = dict(used)
        for _ in range(MAKE_ROOM_MOVES + 1):
            got = slot(u, j, trial[u])                 # `slot` caps at `budget[u]`
            if got is not None:
                trial[u] = trial[u][:got[1]] + [j] + trial[u][got[1]:]
                tused[u] = got[0]
                return trial, tused
            best = None
            for m in list(trial[u]):
                rest = [x for x in trial[u] if x is not m]
                after = cost(u, rest)
                saved = tused[u] - after
                if saved <= 0:
                    continue
                for v in range(len(units)):
                    if v == u or (m.only is not None and m.only != v):
                        continue
                    g = slot(v, m, trial[v])           # the receiving hand must genuinely afford it
                    if g is None:
                        continue
                    key = (-saved, g[0] - tused[v], v)
                    if best is None or key < best[0]:
                        best = (key, m, v, g[0], g[1], rest, after)
            if best is None:
                return None
            _k, m, v, vc, vi, rest, uc = best
            trial[u], tused[u] = rest, uc
            trial[v] = trial[v][:vi] + [m] + trial[v][vi:]
            tused[v] = vc
        return None

    moved = True
    while moved and left:
        moved = False
        for j in sorted(left, key=lambda j: (not (j.at_risk and j.required), not j.funds,
                                             not j.required, not j.at_risk, j.tile)):
            reach = sorted((r, u) for u, r in
                           ((u, _reach(u, j)) for u in range(len(units))
                            if (j.only is None or j.only == u) and affordable(claim(u, j)))
                           if r is not None)
            for _r, u in reach[:MAKE_ROOM_HANDS]:
                room = _make_room(u, j)
                if room is None:
                    continue
                trial, tused = room
                for v in range(len(units)):
                    if trial[v] != routes[v]:
                        routes[v], used[v] = trial[v], tused[v]
                        touch(v)
                booked.update(claim(u, j))
                left.remove(j)
                moved = True
                break
            if moved:
                break                              # `left` has changed; rescan it

    return routes, left


def split_funding_harvest(jobs, wanted):
    """Ripe pens the row is waiting on, with their HARVEST offered as its own job."""
    want = {p: q for p, q in (wanted or {}).items() if q > 0}
    if not want:
        return jobs
    out = []
    for j in jobs:
        harvest = [o for o in j.ops if o[0] == "HARVEST"]
        rest = [o for o in j.ops if o[0] != "HARVEST"]
        earns = {p for p in j.products if want.get(p, 0) > 0}
        if not harvest or not rest or not earns:
            out.append(j)
            continue
        h_gives = {p: q for p, q in j.gives.items() if p in earns}
        r_gives = {p: q for p, q in j.gives.items() if p not in earns}
        if not h_gives:
            out.append(j)
            continue
        out.append(Job(j.tile, harvest, gives=h_gives, products=frozenset(earns)))
        out.append(Job(j.tile, rest, needs=j.needs, gives=r_gives, at_risk=j.at_risk,
                       only=j.only, products=j.products - earns))
    return out


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
    # **A solved day is routed by the planner that can read the solution.** `PRECOMPUTED_ROUTES` is
    # consulted only inside `cover` -- `crew.py` does not contain the name -- so a route solved for a
    # day the crew planner owns is written, loaded, and never read. That is the byte-identical null
    # this repo has shipped three times (`CHAIN_OPS` under an unreachable `COVER_PLANNER`,
    # `SOLVED_DAYS` against the name the code actually read, `RESERVATION_SLIP`). Inert while every
    # solved day is d12+, and the guard is what makes solving an early day mean something.
    assign = (CREW.cover if day is not None and day not in PRECOMPUTED_ROUTES
              and (day < CREW.ACTIVE_UNTIL_DAY
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
            elif TRIM_A_TAIL_THAT_CANNOT_COME_HOME and wanted and day in TRIM_HOME_DAYS:
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
