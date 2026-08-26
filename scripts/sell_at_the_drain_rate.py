"""Would selling at the town's drain rate have banked more? Priced by the ENVIRONMENT, not a model.

An offline model of the book was written first and thrown away: it failed its own validation column
by 41% on WHEAT and 88% on MELON. The environment already contains an exact pricer -- `market_price`
called per unit in lockstep from `_process_market` -- so the honest way to price an alternative sell
schedule is to play it.

Three arms, identical in every respect except the SELL orders:

- `ours`   -- the shipped agent untouched. Control.
- `drain`  -- sell only enough to keep each product's book at or below where it opened
              (`MARKET_I0`). The book is read live from `obs["market"]["inventory"]`, so this
              paces itself against the town's real consumption AND the opponent's supply.
- `hybrid` -- `drain`, plus a forced dump of whatever would otherwise exceed `shedCapacity` at
              dawn. This is the one that can actually be shipped: it never lets stock rot, but it
              never floods the book to do it either.

**Only the SELLs are replaced.** `_process_market` carries HIRE, BUY_LAND, BUY_SEED and
BUY_PRODUCT on the same channel; replacing the whole list switches hiring and purchasing off and
measures a dead farm. Our non-SELL orders are kept in place and the new sells are spliced in at the
position of the first sell, so an order funded by an earlier sale keeps its funding.

    python -u scripts/sell_at_the_drain_rate.py --range 700 8 --opponent contrarian
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys
import time
from concurrent.futures import ProcessPoolExecutor

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
#: `drain` and `hybrid` are kept because they are the control for the mistake they exposed: both
#: CAP total volume, sell 897 units against our own 1442, and lose $86,809 for the trivial reason
#: that the stock never leaves the farm. Neither says anything about WHICH product to sell.
#:
#: `mix` is the arm that answers that. It sells exactly the volume our agent already chose -- so it
#: cannot lose by under-selling -- and changes only the composition, cheapest-to-hold first. On top
#: of that it tops up whenever the shed is projected to spill at dawn, which is the only way rot is
#: ever avoided.
#: Three greedies for the same job -- free the `spill` units that the dawn drop would destroy --
#: differing only in which unit they pick each time. Swept against each other rather than one being
#: declared correct in advance:
#:
#:   no_rot       lowest gain-from-waiting  (dump what the book will not give back)
#:   spread       highest marginal price    (most cash today; self-limits as each book walks down)
#:   cheap_first  lowest marginal price     (keep the expensive stock alive to tomorrow)
ARMS = ("ours", "opt_dusk", "opt_season", "dusk_swap")
#: Days ahead the price projection looks. Swept with --horizon.
HORIZON_DAYS = 2
SHED_CAP = 100


def _play(job):
    arm, seed, opponent, from_day, module_name, shops = job
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG
    from kaggle_environments import make

    from kagg.arena.pool import OPPONENTS, _build

    # **His CADENCE, not his quantities.** `kawa_fill_schedule.json` gives the turns he sold on and
    # the lot he sold. Replaying the quantities measured his farm, not his rule: 271 of 797 units
    # clamped away because our stock at that instant is not his. `kawa_shape` keeps only the TURNS
    # and the LOT SIZE and fills them from whatever we happen to hold, so it is his rhythm applied
    # to our holdings -- which is the thing that was supposed to be tested and never was.
    kawa = {}
    if arm == "kawa_shape":
        kawa = json.loads((REPO / "data/logs/kawa_fill_schedule.json").read_text())

    SA = importlib.import_module(f"kagg.search.{module_name}")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
    env.reset(2)
    me = SA.make_agent(sched, 0, router=True)
    # **`self` is the MIRROR, and on this ladder the mirror is the field.** The opponents are
    # kawa clones and our own agent replays kawa's tape on d4-d11, so a second copy of ourselves
    # is a closer model of a ranked opponent than anything in the pool. It is also the only
    # opponent that reproduces the ladder's glut: WOOL peaking +60 above I0 with 158 units at the
    # $1 floor, against `contrarian` which never pushes a book past +6 and therefore cannot
    # express any rule about a crashed price. Eight arms measured against it on 2026-08-25
    # returned eight nulls, which is a statement about the harness.
    #
    # CLAUDE.md's "a mirror match is not a best response" was written about a DIVERSE field and
    # does not bind here.
    mirror = SA.make_agent(sched, 1, router=True) if opponent == "self" else None
    them = None if mirror is not None else _build(OPPONENTS[opponent], None)

    book0 = None
    #: **How many turns this arm actually changed the orders sent.** Reported BEFORE any money
    #: column, and an arm with `fired == 0` is a broken harness rather than a null result.
    #:
    #: Three separate arms today produced clean-looking tables while changing nothing: `hybrid`
    #: computed `sum(shed) - 100` on a shed the game has already capped at 100, so it was always 0;
    #: the carrot arm patched a constant that does not exist on this branch; and a `drain 0` world
    #: emptied the shop list entirely instead of only removing carrot demand. Each cost a run.
    fired = 0
    fill_turns = units_sold = 0
    prev_shed = prev_money = None
    shed_by_day = {}
    #: **The arm's own target, measured directly.** Bank cannot distinguish "the rot was prevented
    #: and the price impact ate the gain" from "the arm did nothing useful". Units destroyed at the
    #: dawn drop can. Measured as `(shed + carried at dusk) - (shed at dawn)`, per
    #: `_drop_inventories_to_shed` (`reference:843`), not inferred from money.
    rot_units = 0
    rot_value = 0.0
    held_dusk = None
    price_dusk = {}
    day_start_held = 0

    for t in range(30 * TPD):
        # **The shop draw is SET, not drawn.** `_town_consume` reads this list off the live
        # observation every turn, so pinning it makes the town's appetite an independent variable
        # instead of a seed we have to go hunting for. Verified in `scripts/force_the_shops.py`.
        if shops is not None:
            env.state[0].observation["town"]["unlocked_shops"] = list(shops)
        o0 = env.state[0].observation
        day = t // TPD
        priv = o0.get("private") or {}
        shed = {k: int(v or 0) for k, v in (priv.get("shed") or {}).items()}
        book = {k: int(v or 0)
                for k, v in (((o0.get("market") or {}).get("inventory")) or {}).items()}
        if book0 is None:
            book0 = dict(book)
        money = float(o0["farms"][0]["money"])
        if prev_shed is not None and money > prev_money:
            d = sum(max(0, prev_shed.get(k, 0) - shed.get(k, 0))
                    for k in set(prev_shed) | set(shed))
            if d > 0:
                fill_turns += 1
                units_sold += d
        prev_shed, prev_money = shed, money
        if t % TPD == 0:
            shed_by_day[day] = sum(shed.values())
            day_start_held = sum(shed.get(p, 0) for p in SA.SELLABLE)
            if held_dusk is not None:
                for p in set(held_dusk) | set(shed):
                    gone = held_dusk.get(p, 0) - shed.get(p, 0)
                    if gone > 0 and p in KG.PRODUCTS:
                        rot_units += gone
                        rot_value += gone * KG.market_price(p, price_dusk.get(p, KG.MARKET_I0))
        if t % TPD == TPD - 1:
            held_dusk = dict(shed)
            for inv in (priv.get("inventories") or []):
                for k, v in (inv or {}).items():
                    held_dusk[k] = held_dusk.get(k, 0) + int(v or 0)
            price_dusk = dict(book)

        a0 = me(o0, env.configuration)
        market = a0["market"]

        if arm == "kawa_shape" and day >= from_day:
            # His lot for this turn, in units, ignoring which product he chose.
            lot = sum(int(v) for v in (kawa.get(str(t)) or {}).values())
            new_sells = []
            if lot > 0:
                want = lot
                # Biggest holding first: his rhythm, our stock.
                for p in sorted((q for q in SA.SELLABLE if shed.get(q, 0) > 0),
                                key=lambda q: -shed.get(q, 0)):
                    if want <= 0:
                        break
                    take = min(shed.get(p, 0), want)
                    if take > 0:
                        new_sells.append(["SELL", p, int(take)])
                        want -= take
            market, placed = [], False
            for o in (a0["market"] or []):
                if isinstance(o, (list, tuple)) and o and str(o[0]).upper() == "SELL":
                    if not placed:
                        market.extend(new_sells)
                        placed = True
                    continue
                market.append(o)
            if not placed:
                market.extend(new_sells)
            market = market[:10]

        elif arm == "mix" and day >= from_day:
            # Volume our own agent chose this turn. Kept exactly -- only the split moves.
            want = sum(int(o[2]) for o in (a0["market"] or [])
                       if isinstance(o, (list, tuple)) and len(o) > 2
                       and str(o[0]).upper() == "SELL")
            # **What rots is shed PLUS what the hands are still carrying.** Crops land in the
            # per-farmer `inventories` during the day; `_drop_inventories_to_shed` tips them into
            # the shed at dawn and discards whatever does not fit (`reference:843, :878`). Reading
            # `sum(shed)` alone can never exceed the cap -- the cap is applied at dawn -- so the
            # earlier version of this line computed `100 - 100 = 0` on every turn of every season
            # and the rot top-up NEVER FIRED. `what_the_rot_is_actually_worth.py` had already
            # measured the right quantity this morning and it was not used here.
            carried = 0
            for inv in (priv.get("inventories") or []):
                carried += sum(int(v or 0) for k, v in (inv or {}).items() if k in SA.SELLABLE)
            at_risk = sum(shed.get(p, 0) for p in SA.SELLABLE) + carried
            want = max(want, at_risk - SHED_CAP)

            hours_left = TPD - (t % TPD)
            ticks = sum(1 for h in range(t + 1, t + hours_left) if h % 4 == 0)

            def gain(p):
                """What a unit is worth for waiting until the town has drained the book today.

                Priced with the environment's own `market_price`, not a re-implementation -- the
                offline model that re-implemented `_town_consume` was 41% wrong on WHEAT.
                """
                per_tick = 0
                for name in ((o0.get("town") or {}).get("unlocked_shops") or ()):
                    prods = KG.SHOPS.get(name, ())
                    if p in prods:
                        per_tick += 2 if len(prods) == 1 else 1
                b = book.get(p, 0)
                later = b - per_tick * ticks
                return KG.market_price(p, later) - KG.market_price(p, b)

            new_sells = []
            for p in sorted((q for q in SA.SELLABLE if shed.get(q, 0) > 0), key=gain):
                if want <= 0:
                    break
                take = min(shed.get(p, 0), want)
                if take > 0:
                    new_sells.append(["SELL", p, int(take)])
                    want -= take
            market, placed = [], False
            for o in (a0["market"] or []):
                if isinstance(o, (list, tuple)) and o and str(o[0]).upper() == "SELL":
                    if not placed:
                        market.extend(new_sells)
                        placed = True
                    continue
                market.append(o)
            if not placed:
                market.extend(new_sells)
            market = market[:10]

        elif arm == "spread" and day >= from_day:
            # **Marginal, per unit, not per product.** Alex, 2026-08-25: *"maybe over 50 wheat it
            # has an effect but not on small numbers ... it should probably not be an all or
            # nothing."* Right, and the fix is not a threshold.
            #
            # Exactly `spill` units are going to be destroyed at dawn. Freeing one unit of space
            # costs one unit sold, so the question is only WHICH unit. Take them one at a time,
            # each time selling the unit with the highest marginal price right now, and push the
            # book up by one as you go. Wheat gets taken while wheat is the best remaining unit and
            # stops the instant its walked-down price falls below the next product's -- so a few
            # units come off several books instead of fifty off one. That is the "sweet spot",
            # and it falls out of the pricing rather than being tuned in.
            carried = 0
            for inv in (priv.get("inventories") or []):
                carried += sum(int(v or 0) for k, v in (inv or {}).items() if k in SA.SELLABLE)
            spill = (sum(shed.get(p, 0) for p in SA.SELLABLE) + carried) - SHED_CAP
            if spill > 0:
                avail = {p: shed.get(p, 0) for p in SA.SELLABLE if shed.get(p, 0) > 0}
                taken = collections.Counter()
                for _ in range(int(spill)):
                    best, best_price = None, None
                    for p, have in avail.items():
                        if taken[p] >= have:
                            continue
                        price = KG.market_price(p, book.get(p, 0) + taken[p])
                        if best_price is None or price > best_price:
                            best, best_price = p, price
                    if best is None:
                        break
                    taken[best] += 1
                extra = [["SELL", p, int(n)] for p, n in taken.items() if n > 0]
                if extra:
                    market = (list(a0["market"] or []) + extra)[:10]

        elif arm == "foresight" and day >= from_day:
            # **One unit at a time, re-checking the shed and the rot after each.** Alex,
            # 2026-08-25: *"yes per unit not all ... and each time rerun and check the shed and rot
            # ... so its an iterative procedure to find and then sell however."*
            #
            # Each pass asks two questions and sells only if one says yes:
            #
            #   1. Is this unit going to ROT? Anything above zero beats losing it.
            #   2. Otherwise, is selling NOW worth more than selling later? Later means after the
            #      town has drained the book (price up) AND after our own remaining production has
            #      flooded it (price down).
            #
            # **Projecting only the drain was a bug.** Drain removes stock, which RAISES the price,
            # so with drain alone no price ever reads as falling, the rule never fired, and the run
            # came back byte-identical to the previous one. The flooding term is what makes a price
            # fall, and it is our own future output.
            #
            # Both prices are recomputed from the updated book after every unit, so the loop stops
            # itself: each sale walks today's price down toward the projected one, and when they
            # cross, waiting wins.
            hours_left = TPD - (t % TPD)
            ticks = sum(1 for h in range(t + 1, t + hours_left) if h % 4 == 0)
            horizon_ticks = ticks + 6 * HORIZON_DAYS          # 24 hours == 6 shop ticks

            def per_tick(p):
                n = 0
                for name in ((o0.get("town") or {}).get("unlocked_shops") or ()):
                    prods = KG.SHOPS.get(name, ())
                    if p in prods:
                        n += 2 if len(prods) == 1 else 1
                return n

            carried = 0
            for inv in (priv.get("inventories") or []):
                carried += sum(int(v or 0) for k, v in (inv or {}).items() if k in SA.SELLABLE)
            have_now = sum(shed.get(p, 0) for p in SA.SELLABLE) + carried
            elapsed = max(1, t % TPD)
            rate = max(0.0, (have_now - day_start_held) / elapsed)
            must_free = int(max(0, have_now + rate * (hours_left - 1) - SHED_CAP))

            # Our own output over the horizon, split by what we currently hold of each product.
            own_flow = {}
            for p in SA.SELLABLE:
                share = shed.get(p, 0) / max(1.0, float(have_now))
                own_flow[p] = rate * (hours_left - 1 + 24.0 * HORIZON_DAYS) * share

            taken = collections.Counter()
            sold_here = 0
            for _ in range(int(SHED_CAP)):
                rot_left = (must_free - sold_here) > 0
                best, best_key = None, None
                for p in SA.SELLABLE:
                    if taken[p] >= shed.get(p, 0):
                        continue
                    b = book.get(p, 0) + taken[p]
                    now = KG.market_price(p, b)
                    later = KG.market_price(
                        p, int(b - per_tick(p) * horizon_ticks + own_flow.get(p, 0.0)))
                    # Forced by rot: take the unit that fetches the most right now.
                    # Not forced: only a positive now-minus-later edge justifies selling.
                    key = now if rot_left else (now - later)
                    if best_key is None or key > best_key:
                        best, best_key = p, key
                if best is None:
                    break
                if not rot_left and best_key <= 0:
                    break
                taken[best] += 1
                sold_here += 1

            extra = [["SELL", p, int(n)] for p, n in taken.items() if n > 0]
            if extra:
                market, placed = [], False
                for o in (a0["market"] or []):
                    if isinstance(o, (list, tuple)) and o and str(o[0]).upper() == "SELL":
                        if not placed:
                            market.extend(extra)
                            placed = True
                        continue
                    market.append(o)
                if not placed:
                    market.extend(extra)
                market = market[:10]

        elif arm == "dusk_swap" and day >= from_day and (t % TPD) == TPD - 1:
            # **Alex's rule, stated literally, and nothing more.** 2026-08-25: *"i was saying not
            # saving ALL rot but saving SOME rot when it is valued more than a wheat ... if wool is
            # in the book at x and the shed is full then if x - wheat > 0 then its worth selling a
            # wheat."*
            #
            # Every other arm here forced away ALL projected spill, on EVERY turn -- 50 to 62 times
            # a season, each sale walking a book down, and each of them lost money. This one fires
            # at most ONCE a day and only at dusk, where `shed + carried` is the exact quantity the
            # dawn drop is about to act on. No projection, no extrapolated rate, no guessing.
            #
            # One unit sold frees one slot, so one unit that would have been destroyed survives.
            # The trade is worth doing while
            #
            #     value of the unit saved  >  price given up by dumping the cheap one
            #
            # and it STOPS when that goes negative -- so some rot is accepted, deliberately, which
            # is the part every earlier arm got wrong.
            carried = collections.Counter()
            for inv in (priv.get("inventories") or []):
                for k, v in (inv or {}).items():
                    if k in SA.SELLABLE:
                        carried[k] += int(v or 0)
            at_risk = collections.Counter(
                {p: shed.get(p, 0) + carried.get(p, 0) for p in SA.SELLABLE})
            spill = sum(at_risk.values()) - SHED_CAP
            if spill > 0:
                taken = collections.Counter()
                # Most valuable units first: these are what a freed slot rescues.
                saveable = sorted(
                    ((KG.market_price(p, book.get(p, 0)), p)
                     for p in SA.SELLABLE if at_risk.get(p, 0) > 0), reverse=True)
                for _ in range(int(spill)):
                    # Cheapest unit we can actually sell out of the shed, priced after what we have
                    # already dumped this turn.
                    cheap, cheap_price = None, None
                    for p in SA.SELLABLE:
                        if taken[p] >= shed.get(p, 0):
                            continue
                        pr = KG.market_price(p, book.get(p, 0) + taken[p])
                        if cheap_price is None or pr < cheap_price:
                            cheap, cheap_price = p, pr
                    if cheap is None or not saveable:
                        break
                    saved_value = saveable[0][0]
                    # The swap only pays while the rescued unit beats the one we give up.
                    if saved_value - cheap_price <= 0:
                        break
                    taken[cheap] += 1
                extra = [["SELL", p, int(n)] for p, n in taken.items() if n > 0]
                if extra:
                    market = (list(a0["market"] or []) + extra)[:10]

        elif arm in ("opt_dusk", "opt_season") and day >= from_day and (
                arm == "opt_season" or (t % TPD) == TPD - 2):
            # **The optimisation, not a ranking rule.** Alex, 2026-08-25: *"NOT THE CHEAPEST - you
            # have to use greedy to find the optimal of everything that is worth selling, based on
            # what is in the shed, the prices and the holding in the land."*
            #
            # One idea makes the whole thing fall out. Every unit has a value if we DON'T sell it
            # now, and that value is either
            #
            #     0                      -- because it is going to be destroyed at dawn, or
            #     price_later(product)   -- because it will still be there to sell
            #
            # so the gain from selling one more unit of `p` is `price_now(p) - future_value(p)`.
            # Take the best positive one, update the book by one, recompute -- because selling that
            # unit changes both `price_now` (walks it down) and how much is still going to rot
            # (one less). The loop stops itself when no product has a positive gain left.
            #
            # That is why the earlier arms all lost: they ranked products (cheapest, dearest, least
            # gain-from-waiting) and then sold a FIXED quantity. Ranking is not the decision; the
            # quantity is, and it is different for every product on every turn.
            #
            # `opt_dusk` runs once a day at h22 and only prices today. h22 rather than h23 on
            # purpose: `fills.py` records that an hour-23 SELL settles in the same `env.step` as
            # the shed rollover, and `dusk_swap` at h23 made rot WORSE (82 units against 74).
            # `opt_season` runs every turn and prices the rest of the season, including what is
            # still standing in the field.
            hours_left = TPD - (t % TPD)
            if arm == "opt_dusk":
                horizon_ticks = sum(1 for h in range(t + 1, t + hours_left) if h % 4 == 0)
                horizon_days = 1
            else:
                horizon_days = max(1, 30 - day)
                horizon_ticks = 6 * horizon_days

            def per_tick(p):
                n = 0
                for name in ((o0.get("town") or {}).get("unlocked_shops") or ()):
                    prods = KG.SHOPS.get(name, ())
                    if p in prods:
                        n += 2 if len(prods) == 1 else 1
                return n

            carried = collections.Counter()
            for inv in (priv.get("inventories") or []):
                for k, v in (inv or {}).items():
                    if k in SA.SELLABLE:
                        carried[k] += int(v or 0)

            # **What is still standing in the field.** `_new_plant` gives each PLANT tile a `crop`
            # and a `yield_units` already taken, and `CROPS[crop]["max_yield"]` is the ceiling, so
            # the units still to come off that tile are the difference. This is the term that
            # decides whether today's shed pressure is about to get worse or better.
            land = collections.Counter()
            for row in (o0["farms"][0].get("tiles") or []):
                for tile in row:
                    if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
                        continue
                    crop = tile.get("crop")
                    spec = KG.CROPS.get(crop)
                    if not spec or crop not in SA.SELLABLE:
                        continue
                    left = int(spec.get("max_yield", 0)) - int(tile.get("yield_units", 0) or 0)
                    if left > 0:
                        land[crop] += left

            held_total = sum(shed.get(p, 0) for p in SA.SELLABLE) + sum(carried.values())
            incoming = sum(land.values()) if arm == "opt_season" else 0

            taken = collections.Counter()
            for _ in range(int(SHED_CAP) * 2):
                sold = sum(taken.values())
                # Units that will be destroyed if we stop selling here. For the season arm the
                # field's output counts against the same 100 slots.
                rot_left = max(0, held_total + incoming - sold - SHED_CAP)
                best, best_gain = None, 0.0
                for p in SA.SELLABLE:
                    if taken[p] >= shed.get(p, 0):
                        continue
                    b = book.get(p, 0) + taken[p]
                    now = KG.market_price(p, b)
                    later = KG.market_price(
                        p, int(b - per_tick(p) * horizon_ticks + land.get(p, 0)))
                    # The whole decision, in one line: a unit about to rot is worth nothing later.
                    future = 0.0 if rot_left > 0 else float(later)
                    gain = now - future
                    if gain > best_gain:
                        best, best_gain = p, gain
                if best is None:
                    break
                taken[best] += 1

            extra = [["SELL", p, int(n)] for p, n in taken.items() if n > 0]
            if extra:
                market, placed = [], False
                for o in (a0["market"] or []):
                    if isinstance(o, (list, tuple)) and o and str(o[0]).upper() == "SELL":
                        if not placed:
                            market.extend(extra)
                            placed = True
                        continue
                    market.append(o)
                if not placed:
                    market.extend(extra)
                market = market[:10]

        elif arm == "cheap_first" and day >= from_day:
            # The third greedy, and the one that states Alex's trade literally: free the space by
            # selling the CHEAPEST unit available each time, so the expensive stock survives the
            # dawn drop. `spread` maximises cash today; this maximises what is still on the farm
            # tomorrow. They disagree exactly when a steep curve (WOOL is `sq`, T=105) makes today's
            # wool worth more than tomorrow's, which is the thing worth measuring.
            carried = 0
            for inv in (priv.get("inventories") or []):
                carried += sum(int(v or 0) for k, v in (inv or {}).items() if k in SA.SELLABLE)
            spill = (sum(shed.get(p, 0) for p in SA.SELLABLE) + carried) - SHED_CAP
            if spill > 0:
                avail = {p: shed.get(p, 0) for p in SA.SELLABLE if shed.get(p, 0) > 0}
                taken = collections.Counter()
                for _ in range(int(spill)):
                    best, best_price = None, None
                    for p, have in avail.items():
                        if taken[p] >= have:
                            continue
                        price = KG.market_price(p, book.get(p, 0) + taken[p])
                        if best_price is None or price < best_price:
                            best, best_price = p, price
                    if best is None:
                        break
                    taken[best] += 1
                extra = [["SELL", p, int(n)] for p, n in taken.items() if n > 0]
                if extra:
                    market = (list(a0["market"] or []) + extra)[:10]

        elif arm == "no_rot" and day >= from_day:
            # **Only rot prevention. Nothing else.** Our agent's own sells are untouched; this adds
            # sells ONLY for the units that `_drop_inventories_to_shed` would otherwise destroy at
            # dawn, and picks which product to dump by what the book will not give back.
            carried = 0
            for inv in (priv.get("inventories") or []):
                carried += sum(int(v or 0) for k, v in (inv or {}).items() if k in SA.SELLABLE)
            spill = (sum(shed.get(p, 0) for p in SA.SELLABLE) + carried) - SHED_CAP
            if spill > 0:
                hours_left = TPD - (t % TPD)
                ticks = sum(1 for h in range(t + 1, t + hours_left) if h % 4 == 0)

                def gain2(p):
                    per_tick = 0
                    for name in ((o0.get("town") or {}).get("unlocked_shops") or ()):
                        prods = KG.SHOPS.get(name, ())
                        if p in prods:
                            per_tick += 2 if len(prods) == 1 else 1
                    b = book.get(p, 0)
                    return KG.market_price(p, b - per_tick * ticks) - KG.market_price(p, b)

                extra = []
                for p in sorted((q for q in SA.SELLABLE if shed.get(q, 0) > 0), key=gain2):
                    if spill <= 0:
                        break
                    take = min(shed.get(p, 0), spill)
                    if take > 0:
                        extra.append(["SELL", p, int(take)])
                        spill -= take
                market = list(a0["market"] or []) + extra
                market = market[:10]

        elif arm in ("drain", "hybrid") and day >= from_day:
            held_total = sum(shed.get(p, 0) for p in SA.SELLABLE)
            spill = max(0, held_total - SHED_CAP)
            new_sells = []
            # Biggest holding first, so a forced dump comes off the pile that is causing the spill.
            for p in sorted(SA.SELLABLE, key=lambda q: -shed.get(q, 0)):
                have = shed.get(p, 0)
                if have <= 0:
                    continue
                room = book0.get(p, 0) - book.get(p, 0)      # units the book can absorb at par
                take = max(0, min(have, room))
                if arm == "hybrid" and spill > 0 and take < have:
                    extra = min(have - take, spill)
                    take += extra
                    spill -= extra
                if take > 0:
                    new_sells.append(["SELL", p, int(take)])
            market, placed = [], False
            for o in (a0["market"] or []):
                if isinstance(o, (list, tuple)) and o and str(o[0]).upper() == "SELL":
                    if not placed:
                        market.extend(new_sells)
                        placed = True
                    continue
                market.append(o)
            if not placed:
                market.extend(new_sells)
            market = market[:10]

        # The guard: did this arm actually change what gets sent? Compared as sent, not intended.
        if market != (a0["market"] or []):
            fired += 1

        n0 = len(o0["farms"][0].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"] or [])[:n0],
                   "market": market},
                  (mirror(env.state[1].observation, env.configuration) if mirror is not None
                   else them(env.state[1].observation, env.configuration))])
        if env.done:
            break

    farms = env.state[0].observation["farms"]
    return (float(farms[0]["money"]), float(farms[1]["money"]),
            fill_turns, units_sold, shed_by_day, fired, rot_units, rot_value)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default=None)
    ap.add_argument("--range", nargs=2, type=int, default=None, metavar=("FIRST", "COUNT"))
    ap.add_argument("--opponent", default="contrarian")
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--from-day", type=int, default=12)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--worlds", default="CARROT:8,STRAWBERRY:6,MILK:6,WOOL:8",
                    help="comma list of PRODUCT:drain shop worlds to force, plus 'as_drawn'")
    ap.add_argument("--out", default="data/logs/sell_at_the_drain_rate.csv")
    args = ap.parse_args()

    if args.seeds:
        seeds = [int(x) for x in args.seeds.split(",")]
    elif args.range:
        seeds = list(range(args.range[0], args.range[0] + args.range[1]))
    else:
        seeds = list(range(700, 708))

    # A shop WORLD is the independent variable, not a seed. Each entry is (label, shop list).
    from force_the_shops import shops_for_drain
    worlds = [("as_drawn", None)]
    for spec in (args.worlds or "").split(","):
        spec = spec.strip()
        if not spec:
            continue
        prod, _, lvl = spec.partition(":")
        got_shops, got = shops_for_drain(prod, int(lvl))
        worlds.append((f"{prod.lower()}{got}", got_shops))

    jobs = [(arm, s, args.opponent, args.from_day, args.module, w[1])
            for arm in ARMS for w in worlds for s in seeds]
    labels = [w[0] for w in worlds]
    print(f"{len(ARMS)} arms x {len(worlds)} shop worlds x {len(seeds)} seeds vs {args.opponent}, "
          f"from d{args.from_day} = {len(jobs)} seasons, {args.workers} workers")
    print(f"seeds  {seeds}")
    print(f"worlds {labels}\nrows -> {args.out}\n", flush=True)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("arm,world,seed,ours,theirs,win,fill_turns,units_sold,fired,rot_units,rot_value\n")
    fh.flush()

    label_of = {id(w[1]): w[0] for w in worlds}
    cell = collections.defaultdict(lambda: [0, 0, 0.0, 0, 0, 0, 0, 0.0])
    clock = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for job, r in zip(jobs, pool.map(_play, jobs)):
            arm, seed, world = job[0], job[1], label_of.get(id(job[5]), "as_drawn")
            ours, theirs, turns, units, shed_by_day, fired, rot_u, rot_v = r
            win = 1 if ours > theirs else 0
            fh.write(f"{arm},{world},{seed},{ours:.0f},{theirs:.0f},{win},{turns},{units},"
                     f"{fired},{rot_u},{rot_v:.0f}\n")
            fh.flush()
            c = cell[(arm, world)]
            c[0] += win
            c[1] += 1
            c[2] += ours
            c[3] += turns
            c[4] += units
            c[5] += fired
            c[6] += rot_u
            c[7] += rot_v
            print(f"  {arm:<11}{world:<12} seed {seed:<5} fired {fired:>4}  "
                  f"ours {ours:>10,.0f}  turns {turns:>3}  units {units:>5}", flush=True)
    fh.close()

    # **The guard, printed first.** An arm that never altered an order is a broken harness. Its
    # money column is the control's own number and reads as a perfect null, which is the most
    # expensive kind of wrong result -- it looks like an answer.
    print(f"\nturns on which each arm CHANGED the orders sent (0 = harness broken, not a null)\n")
    print(f"{'arm':<12}" + "".join(f"{lab:>14}" for lab in labels))
    dead = []
    for arm in ARMS:
        row = f"{arm:<12}"
        for lab in labels:
            w, n, money, turns, units, fired, rot_u, rot_v = cell[(arm, lab)]
            row += (f"{fired / n:>14.0f}" if n else f"{'-':>14}")
            if n and arm != "ours" and fired == 0:
                dead.append((arm, lab))
        print(row)
    if dead:
        print(f"\nREFUSING to interpret {len(dead)} dead cell(s): "
              + ", ".join(f"{a}/{w}" for a, w in dead))
        print("Fix the arm before reading any money below; those cells are not measurements.")

    print(f"\nmean bank, and the delta against `ours` in the SAME shop world\n")
    print(f"{'arm':<12}" + "".join(f"{lab:>22}" for lab in labels))
    for arm in ARMS:
        row = f"{arm:<12}"
        for lab in labels:
            w, n, money, turns, units, fired, rot_u, rot_v = cell[(arm, lab)]
            bw, bn, bmoney, _bt, _bu, _bf, _br, _brv = cell[("ours", lab)]
            if not n:
                row += f"{'-':>22}"
                continue
            d = money / n - (bmoney / bn if bn else 0.0)
            row += f"{money / n:>13,.0f}{d:>+9,.0f}"
        print(row)

    print(f"\nunits DESTROYED at dawn, and their value -- the arm's actual target\n")
    print(f"{'arm':<12}" + "".join(f"{lab:>22}" for lab in labels))
    for arm in ARMS:
        row = f"{arm:<12}"
        for lab in labels:
            w, n, money, turns, units, fired, rot_u, rot_v = cell[(arm, lab)]
            row += (f"{rot_u / n:>10.0f}{rot_v / n:>12,.0f}" if n else f"{'-':>22}")
        print(row)

    print(f"\nunits sold / fill turns, same layout")
    print(f"{'arm':<12}" + "".join(f"{lab:>22}" for lab in labels))
    for arm in ARMS:
        row = f"{arm:<12}"
        for lab in labels:
            w, n, money, turns, units, fired, rot_u, rot_v = cell[(arm, lab)]
            row += (f"{units / n:>13,.0f}{turns / n:>9.0f}" if n else f"{'-':>22}")
        print(row)

    print(f"\n{time.perf_counter() - clock:.0f}s")


if __name__ == "__main__":
    main()
