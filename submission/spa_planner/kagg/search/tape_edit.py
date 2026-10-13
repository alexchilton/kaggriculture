"""Rewrite ops inside a replayed tape, so a sweep can perturb カワシギ instead of replacing him.

Alex, 2026-08-21: *"how can we perturb kawa and add carrot without breaking stuff in the back
half"*, *"on carrot friendly towns throw in some carrots in the backend instead of wheat"*.

The replay is exact for thirty days (`REPLAY_OPENING_DAYS`), so the search space worth sweeping is
no longer "which plan" -- it is "which single op of his do we change". This module is the edit
operator for that search. It transforms an `opening` dict, the same
`{step: (farmer, hands, market)}` shape `schedule_agent._replay_opening` returns, and hands it back
through `EMBEDDED_OPENINGS` -- a seam the agent already has, so nothing here ships as a flag.

## Three facts that constrain every edit

**PLANT carries no coordinates** (`['PLANT', 'WHEAT']`). The unit plants where it stands, so an
edit cannot name a tile. It can only name the *n*th plant of a day, and which tile that lands on is
whatever the route put under that unit. `scripts/how_long_does_his_wheat_stand.py` measures the
consequence: about 78% of his wheat stands five days, one day past a carrot's lifespan, so only
28-38 tiles a season can take a carrot without weeding. This module does not enforce that -- it
lets the season score it, because a weeded tile shows up in the bank.

**Atomic PLANT is per CROP** (`reference/kaggriculture.py:920-931`): the turn's plant requests are
counted per crop and *all* of that crop's requests are dropped if the seeds are short. So a turn may
mix `PLANT WHEAT` and `PLANT CARROT` freely, and each needs its own seed in the shed. This is why
`swap_plants` must re-point the seed order and not merely relabel the op.

**Ten market orders a turn** (`maxMarketOrdersPerTurn`, `reference/kaggriculture.py:551`), and the
surplus beyond ten is *truncated*, silently. Every function here that appends an order checks the
slot count first and drops the addition rather than push one of his orders off the end.

## Why the sell side is not optional

The whole market is his: `schedule_agent.replayed` sends the tape's own SELL orders and discards
ours. Grow a crop he did not grow and nobody offers it -- it sits in the shed to the final bell and
the edit measures as a pure loss of the wheat it replaced. `surplus_sells` is the correction: each
turn, anything held above what his own order for that product asks for is offered in a free slot.
"""

import collections

#: Ten, and the eleventh order is dropped by the environment rather than queued.
MAX_ORDERS = 10


def copy_opening(opening):
    """A deep copy of `{step: (farmer, hands, market)}`, safe to edit in place."""
    return {int(s): (list(f), [list(h) for h in hs], [list(o) for o in m])
            for s, (f, hs, m) in opening.items()}


def count_ops(opening, op, arg=None):
    """`{day: n}` for a unit op across the whole opening. The measurement the tests assert on."""
    out = collections.Counter()
    for step, (farmer, hands, _) in opening.items():
        for a in [farmer] + list(hands):
            if len(a) >= 1 and a[0] == op and (arg is None or (len(a) > 1 and a[1] == arg)):
                out[step // 24] += 1
    return dict(out)


def swap_plants(opening, days, frm, to, per_day):
    """Rewrite the first `per_day` `PLANT frm` ops of each day in `days` to `PLANT to`.

    Returns `(opening, {day: n_swapped})`. The count is returned rather than assumed because a day
    may hold fewer than `per_day` plants of `frm`, and the seed re-point has to buy the number
    actually swapped, not the number asked for.

    Turn order decides which plants are taken: within a turn, the farmer first and then the hands in
    slot order. That is arbitrary with respect to the board, and deliberately so -- there is no tile
    to aim at (see the module docstring), so the sweep varies `per_day` and the day window and lets
    the bank rank the outcomes.
    """
    out = copy_opening(opening)
    done = collections.Counter()
    for step in sorted(out):
        day = step // 24
        if day not in days or done[day] >= per_day:
            continue
        farmer, hands, _ = out[step]
        for a in [farmer] + list(hands):
            if done[day] >= per_day:
                break
            if len(a) >= 2 and a[0] == "PLANT" and a[1] == frm:
                a[1] = to
                done[day] += 1
    return out, dict(done)


def repoint_seed(opening, swapped, frm, to):
    """Move `n` seeds a day from `frm` to `to`, so the swapped plants have something to sow.

    His `BUY_SEED frm` for the day is reduced first, earliest order first, and a `BUY_SEED to` for
    the same count is merged into an existing order for `to` if the day has one, or inserted at the
    turn his seed order was sent if it does not.

    **The insert goes at his seed turn, not at hour 0.** Slot ORDER is load-bearing in this
    environment -- a SELL only funds a BUY that sits in a later slot (`schedule_agent:3062`) -- so
    an order moved to a different turn is a different order. A day with no `BUY_SEED frm` at all
    falls back to hour 0 and is the one case where that guarantee is not available; he plants from
    stock on those days, so there is no funding order to sit behind.
    """
    out = copy_opening(opening)
    for day, n in sorted(swapped.items()):
        if n <= 0:
            continue
        steps = sorted(s for s in out if s // 24 == day)
        left, anchor = n, None
        for step in steps:
            for o in out[step][2]:
                if len(o) >= 3 and o[0] == "BUY_SEED" and o[1] == frm:
                    if anchor is None:
                        anchor = step
                    take = min(left, int(o[2]))
                    o[2] = int(o[2]) - take
                    left -= take
        merged = False
        for step in steps:
            for o in out[step][2]:
                if len(o) >= 3 and o[0] == "BUY_SEED" and o[1] == to:
                    o[2] = int(o[2]) + n
                    merged = True
                    break
            if merged:
                break
        if not merged:
            step = anchor if anchor is not None else (steps[0] if steps else None)
            if step is None:
                continue
            market = out[step][2]
            if len(market) < MAX_ORDERS:
                market.insert(0, ["BUY_SEED", to, n])
        # A zero-quantity order is a wasted slot and a different action from no order at all.
        for step in steps:
            m = out[step][2]
            out[step] = (out[step][0], out[step][1],
                         [o for o in m if not (len(o) >= 3 and o[0] == "BUY_SEED"
                                               and int(o[2]) <= 0)])
    return out


def swap(opening, days, frm, to, per_day):
    """`swap_plants` then `repoint_seed` -- the whole crop edit, and what the sweep calls."""
    edited, done = swap_plants(opening, days, frm, to, per_day)
    return repoint_seed(edited, done, frm, to), done


def add_land(opening, day, hour=0):
    """Insert a `BUY_LAND` at `day`/`hour`, so a three-quadrant season buys the fourth parcel.

    Alex, 2026-08-22: *"land maybe on the q3 - sometimes helps"*.

    The q3 tapes farm 75 tiles to the final bell while both q4 tapes reach 100 by d18, and that gap
    alone was worth about +$20k a game when the `(True, True)` key was pointed at a q4 recording --
    the crop mix did not matter, the parcel did.

    The cash is there. `BUY_LAND` turns and the bank at that moment:

        92466371 q3   d6 h4 ($406)   d11 h0 ($16,403)
        92498144 q3   d6 h4 ($116)   d11 h0 ($16,162)
        91907974 q4   d6 h4 ($101)   d11 h0 ($16,149)   d12 h0 ($12,717)

    q4 buys its third parcel holding $12,717. Both q3 tapes reach d12 holding MORE than that, and
    their dawn cash never falls below $12,385 for the rest of the season. They simply do not buy.

    The order goes FIRST in the turn, because a purchase only settles against cash already banked
    and anything queued ahead of it can spend the money first. If the bank is short on the day the
    environment refuses it like any other order, which is the honest outcome rather than a crash.
    """
    out = copy_opening(opening)
    step = day * 24 + hour
    if step not in out:
        return out
    farmer, hands, market = out[step]
    if any(o and o[0] == "BUY_LAND" for o in market):
        return out
    out[step] = (farmer, hands, ([["BUY_LAND"]] + list(market))[:MAX_ORDERS])
    return out


def move_sells(opening, days, hour):
    """Re-time every SELL of each day in `days` to `hour`, keeping the day's totals.

    Alex, 2026-08-21: *"we looked at the agent 2500 on the leaderboard and discovered it was better
    when we sold at h=16 as opposed to 0 4,8 or 23 - i think that is a test to be run maybe from
    d20 or so"*.

    There is a mechanism that makes the hour matter. `_town_consume` drains every unlocked shop
    every `townShopSellInterval` (4 turns) AND the town centre every `townCenterSellInterval` (24
    turns, i.e. at hour 0). Hour 0 is the only hour carrying both drains, so it is the deepest
    inventory dip of the day and therefore the highest price. Measured across the archive, the whole
    top of the ladder concentrates there -- Ryo Hasegawa h0, tetsuya h0, Subramanya N h0, ReCurSiON
    h0, Arman Tuganbaev h1 -- while our own submission concentrates at h16.

    Quantities are summed per product and re-emitted as one order, and SELLs are stripped from every
    other turn of the day. Non-SELL orders stay exactly where they are.

    **This can break a purchase, and that is a real cost, not an artifact.** A SELL only funds a BUY
    that sits in a LATER slot on the SAME turn (`schedule_agent:3062`), so a buy that was funded by
    a morning sale can be refused once the sale moves to the evening. That is why the arm is aimed
    at the back half, where the schedule has few purchases left.
    """
    out = copy_opening(opening)
    for day in sorted(set(days)):
        steps = sorted(s for s in out if s // 24 == day)
        if not steps:
            continue
        target = day * 24 + hour
        if target not in out:
            continue
        total = collections.Counter()
        for step in steps:
            farmer, hands, market = out[step]
            keep = []
            for o in market:
                if len(o) >= 3 and o[0] == "SELL":
                    total[o[1]] += int(o[2])
                else:
                    keep.append(o)
            out[step] = (farmer, hands, keep)
        farmer, hands, market = out[target]
        # SELLs go in FIRST so they settle before anything on this turn that needs the cash.
        merged = [["SELL", p, n] for p, n in sorted(total.items()) if n > 0] + list(market)
        out[target] = (farmer, hands, merged[:MAX_ORDERS])
    return out


#: COW gives MILK, SHEEP gives WOOL. Both live on a PASTURE, so re-labelling a head moves no pen,
#: no walk and no route stop -- the replay already relies on this to keep his count and his turn
#: while taking the species. Only the bill differs: COW 400, SHEEP 500.
HERD_PRODUCT = {"COW": "MILK", "SHEEP": "WOOL"}


def carrot_when_it_pays(agent, drain_min=4, opp_tiles_max=7, days=(25, 26, 27), me=0):
    """Sow carrot on d25-d27 only when the TOWN wants it and the OPPONENT is not already in it.

    Alex, 2026-08-22: *"naturally the carrot needs to be conditional on town and opponent"*.

    Both conditions are measured, and crossing them is what separates a real rule from a wash. 528
    configurations, 48 towns, `x_carrot` against the unedited replay:

        town CA>=4  opp CA 1-14   n=125   mean +1143   median  +503   75% improved
        town CA>=4  mirror        n= 25   mean +1659   median  +787   92% improved
        town CA>=4  opp CA=0      n=100   mean  +273   median  -358   46% improved
        town CA>=4  opp CA 15+    n= 25   mean  -510   median -1219   28% improved
        town CA<4   every bucket                       negative        0-11% improved

    Unconditionally the same arm is **-$237**, because the losing towns cancel the winning ones.
    The town test is the strong one; the opponent test only removes the 15+ bucket.

    Decided once, on the first turn of the first day in `days` -- by d25 the opponent's carrot is
    long since standing and the town has drawn all eight shops, so nothing is being guessed at.
    Rewrites `PLANT WHEAT` to `PLANT CARROT` and re-points that day's `BUY_SEED`, the same two
    moves `swap` makes statically; doing it at runtime is what lets the decision see the board.
    """
    days = set(days)
    state = {"on": None}

    def decide(obs):
        from kaggle_environments.envs.kaggriculture import kaggriculture as KG  # noqa: PLC0415
        drain = 0
        for name in ((obs.get("town") or {}).get("unlocked_shops") or []):
            products = KG.SHOPS.get(name) or []
            if "CARROT" in products:
                drain += 2 if len(products) == 1 else 1
        farms = obs.get("farms") or []
        seat = int(obs.get("player", me) or 0)
        theirs = 0
        if len(farms) > 1:
            theirs = sum(1 for row in (farms[1 - seat].get("tiles") or []) for t in row
                         if isinstance(t, dict) and t.get("crop") == "CARROT")
        return drain >= drain_min and theirs <= opp_tiles_max

    def wrapped(obs, config=None):
        act = agent(obs, config)
        if int(obs.get("day", 0) or 0) not in days:
            return act
        if state["on"] is None:
            state["on"] = decide(obs)
        if not state["on"]:
            return act
        acts = [list(act.get("farmer") or ["PASS"])] + [list(h) for h in (act.get("hands") or [])]
        swapped = 0
        for a in acts:
            if len(a) >= 2 and a[0] == "PLANT" and a[1] == "WHEAT":
                a[1] = "CARROT"
                swapped += 1
        # **Re-point EVERY wheat seed order on these days, not only on turns that also planted.**
        # He buys seed on turns with no planting, so gating the rewrite on `swapped` left the day
        # buying wheat it would never sow: measured `d25-27 plants {CARROT 30} seeds {WHEAT 11,
        # CARROT 19}` against the static edit's clean `{CARROT 30} / {CARROT 30}`.
        market = [list(o) for o in (act.get("market") or [])]
        reseeded = False
        for o in market:
            if len(o) >= 3 and o[0] == "BUY_SEED" and o[1] == "WHEAT":
                o[1] = "CARROT"
                reseeded = True
        if not swapped and not reseeded:
            return act
        return {"farmer": acts[0], "hands": acts[1:], "market": market[:MAX_ORDERS]}

    return wrapped


def herd_species(agent, mode, decide_day=8, me=0):
    """Re-label `BUY_ANIMAL` COW/SHEEP, choosing the species from the TOWN and the OPPONENT.

    Alex, 2026-08-21: *"if the combi of the opponent going hard on animal a,b and the shop changes
    the split of cow sheep"*.

    `_herd_split` already answers the town half -- `WOOL_SHOP_SETS_THE_HERD` reads whether a
    YARN_STORE unlocked by d9. It never reads `farms[1 - me]`. That is the gap this fills, and the
    prize is large rather than marginal: on a town with no yarn store, WOOL runs 206 -> 3 across the
    season and is under $5 from d18, because both players dump fleeces into a book nothing drains.
    A 98% price collapse against the 2% an hour-of-day choice can reach.

    Only the SPECIES is rewritten. The count, the turn and the order slot stay the tape's, and the
    `PICKUP`/`PLACE` re-label already in `schedule_agent.replayed` follows the shed and the unit's
    inventory, so no pen or walk moves. Modes:

        cow / sheep   force one species -- the two ends of the axis, for a gradient
        counter       take the species the OPPONENT is not taking
        book          take the species with the better (town drain - opponent head count)

    `decide_day` is when the opponent's board is read. Before it, orders pass through untouched: his
    opening is `SHEEP SHEEP SHEEP COW COW` on d0 in 78 of 78 recorded games and there is nothing to
    react to yet.
    """
    state = {"pick": None}

    def choose(obs):
        farms = obs.get("farms") or []
        seat = int(obs.get("player", me) or 0)
        if len(farms) <= 1:
            return None
        theirs = collections.Counter()
        for row in (farms[1 - seat].get("tiles") or []):
            for t in row:
                if isinstance(t, dict) and t.get("animal") in HERD_PRODUCT:
                    theirs[t["animal"]] += 1
        if mode == "counter":
            if theirs["COW"] == theirs["SHEEP"]:
                return None
            return "SHEEP" if theirs["COW"] > theirs["SHEEP"] else "COW"
        if mode == "book":
            # Drain read from the environment's own SHOPS table, not a hand-written list: a
            # single-product shop consumes at double rate (`_town_consume`), which is exactly the
            # YARN_STORE, and that doubling is the whole reason wool can be worth having.
            from kaggle_environments.envs.kaggriculture import kaggriculture as KG  # noqa: PLC0415
            drain = collections.Counter()
            for name in ((obs.get("town") or {}).get("unlocked_shops") or []):
                products = KG.SHOPS.get(name) or []
                mult = 2 if len(products) == 1 else 1
                for prod in products:
                    if prod in ("MILK", "WOOL"):
                        drain[prod] += mult
            score = {a: drain[HERD_PRODUCT[a]] - theirs[a] for a in HERD_PRODUCT}
            if score["COW"] == score["SHEEP"]:
                return None
            return max(score, key=score.get)
        return None

    def wrapped(obs, config=None):
        act = agent(obs, config)
        day = int(obs.get("day", 0) or 0)
        if day < decide_day:
            return act
        pick = mode.upper() if mode in ("cow", "sheep") else state["pick"]
        if pick is None and mode in ("counter", "book"):
            state["pick"] = pick = choose(obs)
        if pick not in HERD_PRODUCT:
            return act
        market = [list(o) for o in (act.get("market") or [])]
        touched = False
        for o in market:
            if len(o) >= 2 and o[0] == "BUY_ANIMAL" and o[1] in HERD_PRODUCT and o[1] != pick:
                o[1] = pick
                touched = True
        if not touched:
            return act
        act = dict(act)
        act["market"] = market
        return act

    return wrapped


def herd_shift(agent, delta, from_day=1, me=0):
    """Convert up to `abs(delta)` head from one species to the other, AFTER his opening.

    Alex, 2026-08-21: *"you said you only tested increasing sheep not cows"*. He is right, and the
    two arms that looked like the ends of an axis were not:

      `herd_cow_d8`  measured -$1,048 and could barely act. By d8 the herd is mostly bought, and on
                     a town with no yarn store `_herd_split` has already taken cows to their cap --
                     so it changed nothing on the dry towns (+403, -103) and only bit on wool towns
                     where sheep was a deliberate choice (-4,718).
      `herd_cow_d0`  measured -$54k to -$88k, which is not a measurement at all: it overwrites the
                     opening, and his opening is `SHEEP SHEEP SHEEP COW COW` on d0 in 78 of 78
                     recorded games.

    So a real test of "more cows than he takes" has to leave d0 alone and move a BOUNDED number of
    later heads. `delta > 0` buys cows where he bought sheep, `delta < 0` the reverse, and once the
    budget is spent every remaining order is his. That makes the arm a gradient with the control at
    `delta = 0`, rather than an all-or-nothing override.

    Species only -- the count, the turn and the order slot stay the tape's, and COW and SHEEP share
    a PASTURE so no pen, walk or route stop moves. The bill differs, $400 against $500, so a swap
    can still be refused on a thin bank like any other order.
    """
    frm, to = ("SHEEP", "COW") if delta > 0 else ("COW", "SHEEP")
    left = [abs(int(delta))]

    def wrapped(obs, config=None):
        act = agent(obs, config)
        if left[0] <= 0 or int(obs.get("day", 0) or 0) < from_day:
            return act
        market, touched = [list(o) for o in (act.get("market") or [])], False
        for o in market:
            if left[0] <= 0:
                break
            if len(o) >= 3 and o[0] == "BUY_ANIMAL" and o[1] == frm:
                n = int(o[2])
                take = min(n, left[0])
                if take >= n:
                    o[1] = to
                else:
                    o[2] = n - take
                    market.append(["BUY_ANIMAL", to, take])
                left[0] -= take
                touched = True
        if not touched:
            return act
        act = dict(act)
        act["market"] = market[:MAX_ORDERS]
        return act

    return wrapped


def top_up_at_hour(agent, products, hour, from_day=0):
    """Offer whatever is STANDING in the shed at `hour`, on top of the tape's own cadence.

    Alex, 2026-08-21: *"so there is nothing to gain from selling some at h16?"* -- which
    `move_sells` does not answer. That operator MOVES the day's whole sale to one hour and loses
    heavily, because a single order can only sell what the shed holds at that instant and the rest
    of the day's harvest is never offered. This one ADDS an order and takes nothing away.

    It is worth asking because his cadence demonstrably leaves stock standing. Seed 11, town 0,
    WHEAT in the shed by hour: `d22  h0:22 h3:0 h6:0 h9:8 h12:8 h15:8 h18:8 h21:2`. Eight units sat
    unsold from h9 to h18.

    **Fires on ONE hour a day, unlike `surplus_sells`.** The unbounded every-turn version measured
    a catastrophe on WHEAT -- $330 against a $70,687 control -- by re-offering the spare every turn
    and walking its own price into the floor. A single daily order cannot do that.
    """
    want = set(products)

    def wrapped(obs, config=None):
        act = agent(obs, config)
        if int(obs.get("hour", 0) or 0) != hour or int(obs.get("day", 0) or 0) < from_day:
            return act
        shed = collections.Counter((obs.get("private") or {}).get("shed") or {})
        market = list(act.get("market") or [])
        offered = collections.Counter()
        for o in market:
            if len(o) >= 3 and o[0] == "SELL":
                offered[o[1]] += int(o[2])
        for prod in sorted(want):
            if len(market) >= MAX_ORDERS:
                break
            extra = shed[prod] - offered[prod]
            if extra > 0:
                market.append(["SELL", prod, extra])
        act = dict(act)
        act["market"] = market
        return act

    return wrapped


def surplus_sells(agent, products, from_day=0):
    """Wrap `agent` so shed stock his own order does not ask for gets offered in a free slot.

    Without this an edit that grows a crop he did not grow banks nothing: the whole market on a
    replayed turn is the tape's, so an unsold harvest sits in the shed to the final bell and the
    edit scores as a pure loss of whatever it replaced.

    The rule is deliberately the smallest one that can work. It offers `held - his_offer` and only
    for the named products, so on every turn he already covers, and for every product not being
    swept, the action is byte-identical to the unedited replay. That matters: it makes the `per_day
    = 0` arm of a sweep a true control rather than a fourth variant.
    """
    want = set(products)

    def wrapped(obs, config=None):
        act = agent(obs, config)
        if int(obs.get("day", 0) or 0) < from_day:
            return act
        shed = collections.Counter((obs.get("private") or {}).get("shed") or {})
        market = list(act.get("market") or [])
        offered = collections.Counter()
        for o in market:
            if len(o) >= 3 and o[0] == "SELL":
                offered[o[1]] += int(o[2])
        for p in sorted(want):
            if len(market) >= MAX_ORDERS:
                break
            extra = shed[p] - offered[p]
            if extra > 0:
                market.append(["SELL", p, extra])
        act = dict(act)
        act["market"] = market
        return act

    return wrapped
