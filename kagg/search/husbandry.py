"""Every decision for one stocked pen, in one place.

The animal sibling of `watering.py`, and split for the same reason: these rules were an if/elif
chain inside `router.animal_ops` interleaved with pricing, and a change aimed at one branch is hard
to land on the right one from inside it.

**Pure by construction.** Nothing here imports `router`, and every threshold, price and floor
arrives as an argument. The rules below are engine facts, all from `reference/kaggriculture.py`:

  * An animal escapes at `consecutive_unfed >= 2` (`:804`). The structure survives, the animal does
    not, and nothing buys it back the same day -- so a hungry pen is irreversible, not expensive.
  * Production does NOT read `fed_today`. `_daily_refresh_animals` (`:795-820`) adds `base = 1` on
    the interval whether or not the animal ate. A FEED resets `consecutive_unfed`, and on a
    production night it releases `pending_care_bonus`. On any other night it buys nothing.
  * `pending_care_bonus` is banked only on a night that is BOTH fed and cared, which is why CARE is
    offered only on a pen that is already fed.
  * Produce standing on a pen at dusk on d28 reaches the shed free (`_drop_inventories_to_shed`
    inside `_end_of_day`) and is sellable through d29. The same drop on d29 lands AFTER the final
    market, so milk left standing tomorrow can never be money.
"""


class Pen:
    """What a visit to a pen is for. Named, so a caller can say which rule it is changing."""

    FEED_HUNGRY = "FEED_HUNGRY"    # one missed day from the animal escaping: irreversible
    FEED_CYCLE = "FEED_CYCLE"      # on cycle, so a production night pays base + care bonus
    CARE = "CARE"                  # one extra unit on the next production day; needs a fed pen
    COLLECT = "COLLECT"            # fertilizer standing on the pen
    HARVEST = "HARVEST"            # produce standing on the pen
    NONE = "NONE"


def feed(*, fed_today, have_wheat, consecutive_unfed, on_cycle, price, animal_cost,
         remaining, critical, mandatory):
    """`(kind, prize, now_fed)` for the FEED decision.

    `on_cycle` is the caller's answer to "is this pen due a feed today" -- the every-night feed of an
    animal that has not STARTED producing is the waste, because survival alone is bought by one feed
    in two. The tape shows it plainly: seventeen pens on d7 and THREE feeds, then 11 of 17 by d9 and
    12 of 18 by d10 as the herd comes on line.

    A hungry pen is priced above everything because the loss is permanent, not merely costly.
    """
    if fed_today or not have_wheat or not on_cycle:
        return Pen.NONE, None, fed_today
    hungry = consecutive_unfed >= 1
    floor = critical if hungry else mandatory
    prize = floor + price + ((animal_cost + remaining) if hungry else 0)
    return (Pen.FEED_HUNGRY if hungry else Pen.FEED_CYCLE), prize, True


def care(*, cared_today, fed, price):
    """`(kind, prize)` for CARE. Only ever offered on a pen that is fed today."""
    if cared_today or not fed:
        return Pen.NONE, None
    return Pen.CARE, price


def collect(*, fertilizer_available, fertilizer_price):
    if not fertilizer_available:
        return Pen.NONE, None
    return Pen.COLLECT, fertilizer_price


def harvest(*, yield_units, price, day, last_free_bank_day, critical):
    """`(kind, prize)` for produce standing on the pen.

    On `last_free_bank_day` the prize carries `critical`: a crop reaches that floor on its own
    through its closing yield window, but a pen has no window, so nothing else ever promotes it and
    the produce sits while the crew idles.
    """
    if yield_units <= 0:
        return Pen.NONE, None
    prize = yield_units * price
    if day is not None and day == last_free_bank_day:
        prize += critical
    return Pen.HARVEST, prize


def last_day(*, fertilizer_available, yield_units, price, fertilizer_price, critical):
    """The whole of a pen's last-day worth: collect what is there, buy nothing that pays tomorrow.

    A standing harvest is the only thing that can still become money, so it is worth the tile rather
    than its units.
    """
    out = []
    if fertilizer_available:
        out.append((Pen.COLLECT, fertilizer_price))
    if yield_units > 0:
        out.append((Pen.HARVEST, critical + yield_units * price))
    return out
