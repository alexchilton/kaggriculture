"""Every water decision for one planted tile, in one place.

Pulled out of `router.crop_ops`, where the four rules below sat as an if/elif chain interleaved
with FERTILIZE and HARVEST pricing, each branch carrying a paragraph of history. Three separate
changes this session landed on the wrong branch of that chain because the branches are hard to tell
apart from inside it -- a water cap aimed at the safe one-shot tile went onto the ongoing tile and
measured as a null, and the ordering of the tests is load-bearing in a way nothing announced.

**Pure by construction.** Nothing here imports `router`, and nothing here reads a module-level
constant of its own. Every threshold the rules need arrives as an argument, so a caller can see what
a decision depended on, and a test can set it. That is the point of the split: the rules stop being
entangled with whatever else `crop_ops` happens to have in scope.

The engine facts these rules encode, all from `reference/kaggriculture.py`:

  * `consecutive_unwatered` starts at 1 on the planting day (`:222`), the dusk rollover adds one,
    and the tile becomes a WEED at 2 (`:771`). So a tile watered yesterday is safe tonight, and only
    a tile already at 1 dies if skipped.
  * Water does not GROW anything. `_daily_refresh_crops` advances `yield_units` off the calendar
    alone and reads `was_watered` only to weed the tile and to gate the fertilizer doubling
    (`:783`, `:799`). The exception is a one-shot crop inside its window, where the water IS the
    yield.
  * A one-shot tile's window is `(max_day + 1) // 2 <= age <= max_day`.
"""


class Water:
    """The four kinds of water, as named outcomes rather than positions in an if/elif chain."""

    FILLS = "FILLS"        # one-shot, inside its window: this water IS a unit of yield
    SAVES = "SAVES"        # at `consecutive_unwatered >= 1`: the tile weeds tonight without it
    PRODUCES = "PRODUCES"  # ongoing, produces tomorrow: water gates the fertilizer doubling
    TOPS_UP = "TOPS_UP"    # safe tile, watered to keep it off the brink tomorrow
    NONE = "NONE"


def one_shot_window(age, max_day):
    """Is a one-shot crop inside the window where a water adds yield?"""
    return (max_day + 1) // 2 <= age <= max_day


def fertilize_one_shot(*, room, age, max_day, season_days, day, price, fert_price,
                       fertilized, have_fertilizer, fertilized_until_day, fertilize_until_day):
    """`(prize, True)` if this one-shot tile is worth fertilizing now, else `(None, fertilized)`.

    Worth it only when the waters the window still has cannot fill the tile on their own, so the
    doubling buys units that would otherwise never arrive.

    **Clipped to the SEASON, not just to the window.** A tile whose window runs past the last day is
    otherwise credited with waters nobody will ever give it, and the FERTILIZER it spends is a
    product that could have been sold instead.
    """
    if fertilized or not have_fertilizer or room <= 0:
        return None, fertilized
    if day >= fertilize_until_day or fertilized_until_day >= day:
        return None, fertilized
    waters_left = min(max_day - age + 1, season_days - day)
    if waters_left >= room:
        return None, fertilized
    gain = min(room, waters_left * 2) - min(room, waters_left)
    if gain * price <= fert_price:
        return None, fertilized
    return gain * price, True


def one_shot_water(*, in_window, watered_today, consecutive_unwatered, day, price, fertilized,
                   remaining, late_truncated_plant_day, upkeep_pointless, top_up_discount):
    """`(kind, prize)` for a one-shot tile, or `(Water.NONE, None)`.

    The three cases are mutually exclusive and this is the only place their order is decided.

    `FILLS` -- inside the window the water is a unit, two if fertilized. A melon water is $250, the
    highest-value single op in the game, and a melon water OUTSIDE its window is worth nothing.
    A tile can be in its window AND on the brink on the same day, so the price is the larger of the
    two: at one unit the brink case lost every auction and the tile weeded.

    `SAVES` -- outside the window, water buys survival and nothing else, and only on the day the
    tile would otherwise weed. This is the every-second-day rule, derived rather than tuned.

    `TOPS_UP` -- a safe tile, discounted because the tile is not in danger and the visit competes
    with work that banks today.
    """
    if watered_today:
        return Water.NONE, None
    if in_window:
        unit = price * (2 if fertilized else 1)
        if day >= late_truncated_plant_day and consecutive_unwatered >= 1:
            unit = max(unit, remaining)
        return Water.FILLS, unit
    if consecutive_unwatered >= 1 and not upkeep_pointless:
        return Water.SAVES, remaining
    if not upkeep_pointless:
        return Water.TOPS_UP, remaining / top_up_discount
    return Water.NONE, None


def ongoing_water(*, watered_today, consecutive_unwatered, produces_tomorrow, room, fertilized,
                  day, price, remaining, fertilize_until_day, upkeep_pointless, top_up_discount,
                  alternates):
    """`(kind, prize)` for an ongoing tile, or `(Water.NONE, None)`.

    An ongoing crop produces at dawn whatever it was given, so water here is survival plus the
    fertilizer bonus on a production day. `PRODUCES` is the only water a safe tile can be offered
    once fertilizing has stopped, because `fertilized` is False by construction from then on.

    `alternates` is the caller's answer to "may a safe tile be topped up today". Offering EVERY safe
    ongoing tile every day is the shape that measured $79,905 -> $63,645; offering half, flipping
    daily, keeps `consecutive_unwatered` below the 2 that weeds a tile without doubling the load.
    """
    if watered_today:
        return Water.NONE, None
    if consecutive_unwatered >= 1:
        return Water.SAVES, remaining
    if produces_tomorrow and room > 0 and (fertilized or day >= fertilize_until_day):
        return Water.PRODUCES, price
    if alternates and not upkeep_pointless:
        return Water.TOPS_UP, remaining / top_up_discount
    return Water.NONE, None
