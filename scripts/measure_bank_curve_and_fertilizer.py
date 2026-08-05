"""Day by day: do we go all-in on day 0, and does fertilizer fund days 1-7?

Alex's point, and it reframes the whole gap. The leader ends day 0 on **$42**. He can only do that
because FERTILIZER sells from day 1 hour 8 -- a fed animal sets `fertilizer_available` every night and
COLLECT_FERTILIZER costs no action, so it is free revenue seven days before milk arrives on day 8. The
causal chain runs one way only:

    fertilizer income from day 1  ->  day-0 all-in is survivable  ->  capacity compounds

If we do not have the first, we cannot do the second, and nothing downstream matters. So the number
that decides everything is not the season total, it is the **dawn bank on days 0-10**. His:

    day  0  $3,000     day  5  $  621     day 10  $1,278  (buys a $2,000 parcel on it)
    day  1  $   42     day  7  $1,719     day 11  $3,236
    day  2  $  141                        day 12  $6,828
    day  3  $  217                        day 13  $14,622

This script plays a plan in the real environment and prints our curve against his, plus where the money
went, so "we ended day 0 holding thousands" stops being an inference and becomes a reading.

It also separates the two rival uses of fertilizer, which the search currently ties to one gene:

  sell        `ranch(sell_fertilizer=True)`  -- 23.1% of winner sales, and the day-1 cash above.
  apply       `grow(fertilize=True)`         -- doubles strawberry and tomato yield, worth nothing on melon.
  self-supply `sell_fertilizer=False` + `grow(buy_fertilizer=False)` -- the herd's free output walks to
              the crop block instead of being sold and bought back at $100 a unit through the same
              market. He does both: 318 collected, 107 applied, 445 offered.
"""

import argparse
import collections
import copy
import sys

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import routines as R
import build_script_submission as B

ap = argparse.ArgumentParser()
ap.add_argument("--opponent", default="starter")
ap.add_argument("--variants", default="baseline,apply_bought,self_supply,hold_only")
ap.add_argument("--mixes", default="", help="comma-separated names from MIXES, scored head to head")
ap.add_argument("--games", type=int, default=1,
                help="averaged, because the shop unlock order swings one game by ~30%%")
args = ap.parse_args()

SHED = R.shed_access_tiles()
FERT = R.PRODUCTS.index("FERTILIZER")

# Off his tape. `scripts/audit_leader_wheat.py` and the day-by-day trace in
# `tests/test_we_can_emit_the_leaders_cash_curve.py`.
HIS_BANK = {0: 3000, 1: 42, 2: 141, 3: 217, 5: 621, 7: 1719, 10: 1278,
            11: 3236, 12: 6828, 13: 14622}


def cluster(quadrant, n, taken):
    """`n` mutually adjacent tiles, nearest the shed first. Compactness, not proximity -- a diagonal
    ring costs two moves a step and four such pens need 25 of a 23-turn day."""
    pool = [t for t in [(x, y) for y in range(R.BOARD_SIZE) for x in range(R.BOARD_SIZE)]
            if R.quadrant_of(*t) == quadrant and t not in SHED and t not in taken]
    pool.sort(key=lambda t: abs(t[0] - 4) + abs(t[1] - 4))
    if not pool:
        return []
    out = [pool[0]]
    while len(out) < n:
        nxt = min((t for t in pool if t not in out
                   and any(abs(t[0] - o[0]) + abs(t[1] - o[1]) == 1 for o in out)),
                  key=lambda t: abs(t[0] - 4) + abs(t[1] - 4), default=None)
        if nxt is None:
            break
        out.append(nxt)
    return R.serpentine(out)


def leader_shaped_plan(sell_fertilizer=True, fertilize=False, buy_fertilizer=False,
                       land_days=(7, 10), prebuy_wheat=0, prebuy_seeds=0, buy_feed=True):
    """The fixture from `tests/test_we_can_emit_the_leaders_cash_curve.py`, with the fertilizer
    policy exposed. Built through `routines.py` directly so a failure is a statement about the
    emitter and not about the search's luck."""
    script = R.Script()
    taken, used, refused, busy = set(), [], [], set()
    # **Land is bought on the day the bank can actually pay for it, not the day his tape does it.**
    # `_do_buy_land` returns silently when `farm["money"] < price`, so ordering the $1,000 NE parcel
    # on day 7 with $50 in hand does not fail -- it leaves NE LOCKED for the season and every crop
    # block scheduled there plants nothing. Measured: 30 of 36 crop tiles dead, `planted` = 0 from
    # day 7 to day 16. He can afford day 7 because his herd is already earning; we cannot.
    for day in land_days:
        t = day * R.TURNS_PER_DAY
        if 0 <= t < script.T:
            script.buy_land[t] += 1
    # A block cannot start before its quadrant is unlocked, so moving the purchase moves the planting.
    # **Day 0 is the cheapest day of the season, and he spends it on inventory rather than holding
    # cash.** Wheat opens at 25 and finishes at 54 as the eight shops unlock across days 3-24, so the
    # same feed bought hand-to-mouth on day 20 costs more than double. His day 0 is 4 animals, ~51
    # wheat in small lots across all 24 hours, 18 seeds and 4 hires -- $2,958 of $3,000, ending on $42.
    # Ours spends $1,820 and banks $1,187, then buys 4 wheat a day at a rising price forever.
    #
    # Faked here rather than derived, deliberately: hardcode his numbers first, measure whether they
    # are worth having, and only then work out why our machinery cannot produce them.
    if prebuy_wheat:
        # Spread across the day's turns, as his tape does. A single 51-unit order quotes against one
        # inventory level and walks itself up the price curve; small lots across 24 hours do not.
        w = R.PRODUCTS.index("WHEAT")
        for k in range(prebuy_wheat):
            script.buy_product[k % R.TURNS_PER_DAY, w] += 1
    if prebuy_seeds:
        script.buy_seed[0, R.CROPS.index("STRAWBERRY")] += prebuy_seeds

    ld = sorted(land_days)
    unlock = {"NW": 0,
              "NE": ld[0] + 1 if len(ld) > 0 else 99,
              "SW": ld[1] + 1 if len(ld) > 1 else 99}

    def place_pens(animal, want, quadrant, start_day, single_chain=False, build_every=1):
        placed = 0
        while placed < want:
            for size in range(min(4, want - placed), 0, -1):
                group = cluster(quadrant, size, taken)
                if len(group) < size:
                    continue
                for unit in range(16):
                    if unit in busy:
                        continue
                    probe = R.Script()
                    try:
                        R.ranch(probe, animal=animal, tile=group, start_day=start_day, unit=unit,
                                buy_land=False, feed_every=2, build_every=build_every)
                    except ValueError:
                        continue
                    R.ranch(script, animal=animal, tile=group, start_day=start_day, unit=unit,
                            buy_land=False, feed_every=2, collect_fertilizer=True,
                            sell_fertilizer=sell_fertilizer, build_every=build_every,
                            buy_feed=buy_feed)
                    taken.update(group)
                    busy.add(unit)
                    used.append(("ranch", animal, len(group), unit, start_day))
                    placed += len(group)
                    break
                else:
                    continue
                break
            else:
                refused.append(f"{animal}: nothing fits for the last {want - placed} in {quadrant}")
                break
            if single_chain:
                break
        return placed

    for animal in ("COW", "COW", "COW", "SHEEP"):
        place_pens(animal, 4, "NW", 0, single_chain=True, build_every=3)
    place_pens("SHEEP", 2, "SW", unlock["SW"])

    # **A block starts the day after its quadrant unlocks, not the day his tape starts it.**
    # `_apply_unit_action` bails on a LOCKED tile before it ever reaches the PLANT branch, so a
    # strawberry block scheduled on NE while NE is still locked plants nothing, all season, silently.
    for crop, size, quadrant, day in (("MELON", 6, "NW", 1),
                                      ("STRAWBERRY", 8, "NE", "NE"),
                                      ("STRAWBERRY", 8, "NE", "NE"),
                                      ("STRAWBERRY", 8, "SW", "SW"),
                                      ("MELON", 6, "SW", "SW")):
        day = unlock[day] if isinstance(day, str) else day
        if day >= R.SEASON_DAYS:
            refused.append(f"{crop}x{size}: {quadrant} never unlocks")
            continue
        block = cluster(quadrant, size, taken)
        if not block:
            refused.append(f"no tiles for {crop}x{size} in {quadrant}")
            continue
        for unit in range(16):
            if unit in busy:
                continue
            probe = R.Script()
            try:
                R.grow(probe, crop, block, plant_day=day, unit=unit, buy_land=False,
                       water_every=2, fertilize=fertilize, buy_fertilizer=buy_fertilizer)
            except ValueError:
                continue
            R.grow(script, crop, block, plant_day=day, unit=unit, buy_land=False,
                   water_every=2, fertilize=fertilize, buy_fertilizer=buy_fertilizer)
            taken.update(block)
            busy.add(unit)
            used.append(("grow", crop, len(block), unit, day))
            break
        else:
            refused.append(f"no unit fits {crop}x{len(block)} in {quadrant} on d{day}")
    return script, used, refused


def mix_plan(cow=8, sheep=6, strawberry=41, melon=20, land_days=(7, 10), build_every=3,
             sell_fertilizer=True, combine=False, wheat_buy=0, wheat_sell_days=()):
    """A named MIX, placed by the same emitter, so two mixes can be compared and nothing else differs.

    Alex's question: the closed-form calculator says 48 strawberry / 12 melon and the leader actually
    plants 44 / 21 (measured off the tape -- `PLANT` ops by crop). Is his mix better than ours, or is
    the calculator right and he is leaving money on the table? The only way to answer is to run both
    through the same emitter against the same opponent and read the banks.

    Pens are filled first and nearest the shed, because the walk is what refuses a group; crop tiles
    take what is left, largest block first, and any tile in a quadrant we never unlock is reported as
    refused rather than silently planted on locked ground.
    """
    script = R.Script()
    taken, used, refused, busy = set(), [], [], set()
    for day in land_days:
        t = day * R.TURNS_PER_DAY
        if 0 <= t < script.T:
            script.buy_land[t] += 1
    ld = sorted(land_days)
    unlock = {"NW": 0,
              "NE": ld[0] + 1 if len(ld) > 0 else 99,
              "SW": ld[1] + 1 if len(ld) > 1 else 99}

    def place_ranch(animal, want):
        """Groups of at most 4, walking outward, in whichever quadrant is open earliest."""
        placed = 0
        for quadrant in ("NW", "NE", "SW"):
            start = unlock[quadrant]
            if start >= R.SEASON_DAYS:
                continue
            while placed < want:
                # **Do not cap the group at 4 -- ask the emitter.** The cap was read off an old
                # measurement ("4 fit in NW, NE needs 25 turns") and turned into a rule, which forces
                # 14 pens onto 4-5 units and the crop blocks onto 8 more: 15 chains, 15 hands,
                # $47,880 of crew a season, and the farm banks $2,609. `tests/
                # test_the_crew_bill_must_not_dwarf_the_farm.py` places the same 14 pens and 61 tiles
                # inside 12 hands purely by letting the group grow and `ranch()` say no.
                for size in range(min(8, want - placed), 0, -1):
                    group = cluster(quadrant, size, taken)
                    if len(group) < size:
                        continue
                    order = (sorted(busy) + [u for u in range(16) if u not in busy]
                             if combine else [u for u in range(16) if u not in busy])
                    for unit in order:
                        if not combine and unit in busy:
                            continue
                        probe = copy.deepcopy(script)
                        try:
                            R.ranch(probe, animal=animal, tile=group, start_day=start, unit=unit,
                                    buy_land=False, feed_every=2, build_every=build_every)
                        except ValueError:
                            continue
                        R.ranch(script, animal=animal, tile=group, start_day=start, unit=unit,
                                buy_land=False, feed_every=2, collect_fertilizer=True,
                                sell_fertilizer=sell_fertilizer, build_every=build_every)
                        taken.update(group)
                        busy.add(unit)
                        used.append(("ranch", animal, len(group), unit, start))
                        placed += len(group)
                        break
                    else:
                        continue
                    break
                else:
                    break
        if placed < want:
            refused.append(f"{animal}: {want - placed} of {want} pens never placed")
        return placed

    def place_grow(crop, want):
        placed = 0
        for quadrant in ("NW", "NE", "SW"):
            start = unlock[quadrant]
            if start >= R.SEASON_DAYS:
                continue
            while placed < want:
                for size in range(min(8, want - placed), 0, -1):
                    block = cluster(quadrant, size, taken)
                    if len(block) < size:
                        continue
                    # **Units already holding a pen group are tried FIRST when combining.**
                    # The hire ladder is Fibonacci and reset every dawn, so the crew size -- not the
                    # tile count -- is the dominant running cost: 8 hands is $54/day and 16 hands is
                    # $2,583/day, a 48x step for the same farm. He runs 14 pens and ~61 tiles on 12
                    # hands by sharing units; giving every block its own unit takes us to 16 and
                    # $77,490 a season, which is why every mix above banked ~$0.
                    order = (sorted(busy) + [u for u in range(16) if u not in busy]
                             if combine else [u for u in range(16) if u not in busy])
                    for unit in order:
                        if not combine and unit in busy:
                            continue
                        # **Probe a COPY of the real script, not a fresh one.** A fresh `Script` has
                        # all 23 turns free on every unit, so it says yes to a block that will not
                        # fit beside a pen group already claiming 12 of them -- and `grow()` can
                        # raise part-way through the season, after writing earlier days.
                        probe = copy.deepcopy(script)
                        try:
                            R.grow(probe, crop, block, plant_day=start + 1, unit=unit,
                                   buy_land=False, water_every=2)
                        except ValueError:
                            continue
                        R.grow(script, crop, block, plant_day=start + 1, unit=unit,
                               buy_land=False, water_every=2)
                        taken.update(block)
                        busy.add(unit)
                        used.append(("grow", crop, len(block), unit, start + 1))
                        placed += len(block)
                        break
                    else:
                        continue
                    break
                else:
                    break
        if placed < want:
            refused.append(f"{crop}: {want - placed} of {want} tiles never placed")
        return placed

    place_ranch("COW", cow)
    place_ranch("SHEEP", sheep)
    place_grow("STRAWBERRY", strawberry)
    place_grow("MELON", melon)

    # ------------------------------------------------------------------ the wheat book, hardcoded
    # His largest line by volume and one we do not run at all: 967 units BOUGHT and 1,131 SOLD across
    # the season, of which 319 go to FEED (which takes one carried WHEAT per animal per day) and ~648
    # are resold. It is not a day-0 pre-buy -- the by-day trace is a continuous ~35 bought and ~38
    # sold every day, with two dumps that move his bank on their own: 204 units on day 12, the day he
    # goes $6,828 -> $14,622, and 176 on the last day.
    #
    # Faked here at his measured daily rate, spread across the day's turns as his tape does it. A
    # single large order quotes against one inventory level and walks itself down the price curve;
    # small lots across 24 hours do not.
    if wheat_buy:
        w = R.PRODUCTS.index("WHEAT")
        for day in range(R.SEASON_DAYS):
            for k in range(wheat_buy):
                t = day * R.TURNS_PER_DAY + (k % (R.TURNS_PER_DAY - 1)) + 1
                if t < script.T:
                    script.buy_product[t, w] += 1
    for day, qty in wheat_sell_days:
        t = day * R.TURNS_PER_DAY
        if t < script.T:
            script.sell[t, R.PRODUCTS.index("WHEAT")] += qty
    return script, used, refused


MIXES = {
    # Measured off `data/seed_scripts/new_leader/90016067.json`: PLANT ops by crop are MELON 21,
    # STRAWBERRY 44, WHEAT 66, and BUY_ANIMAL is COW 8 / SHEEP 6.
    "his_mix":        dict(cow=8, sheep=6, strawberry=44, melon=21),
    # `scripts/allocation_calculator.py`, closed form off the measured drains.
    "calculated_mix": dict(cow=8, sheep=6, strawberry=48, melon=12),
    # The two differences isolated, so the comparison attributes rather than just ranks.
    "his_melon_only": dict(cow=8, sheep=6, strawberry=48, melon=21),
    "his_straw_only": dict(cow=8, sheep=6, strawberry=44, melon=12),

    # ---- the crew bug, isolated. Same farm, units shared instead of one thing per unit.
    "his_combined":   dict(cow=8, sheep=6, strawberry=44, melon=21, combine=True),
    "calc_combined":  dict(cow=8, sheep=6, strawberry=48, melon=12, combine=True),
    # A farm small enough to fund, to see whether size or shape is what kills us.
    "small_combined": dict(cow=4, sheep=2, strawberry=16, melon=8, combine=True),

    # ---- and the wheat book on top of the crew fix.
    "his_plus_wheat": dict(cow=8, sheep=6, strawberry=44, melon=21, combine=True,
                           wheat_buy=32, wheat_sell_days=((12, 204), (29, 176))),
    "wheat_only":     dict(cow=8, sheep=6, strawberry=44, melon=21, combine=True,
                           wheat_buy=32),
}

# **The size sweep.** A farm one quarter of his banked $33,427 and won 3/3 where his own mix banked
# $17 and won nothing, so scale -- not mix, not schedule -- is what we have been getting wrong. The
# Fibonacci crew ladder is superexponential in hands, and hands rise with chains, so there is an
# interior optimum and it is nowhere near the top. This finds it, and it is a 1-D sweep.
for _k in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
    MIXES[f"size_{_k}"] = dict(cow=_k, sheep=max(1, _k * 3 // 4),
                               strawberry=_k * 4, melon=_k * 2, combine=True)
    MIXES[f"size_{_k}_wheat"] = dict(cow=_k, sheep=max(1, _k * 3 // 4),
                                     strawberry=_k * 4, melon=_k * 2, combine=True,
                                     wheat_buy=32, wheat_sell_days=((12, 204), (29, 176)))


VARIANTS = {
    # what the fixture does today: every collected unit is sold, no crop is ever fertilized.
    "baseline":     dict(sell_fertilizer=True,  fertilize=False, buy_fertilizer=False),
    # sell the herd's output AND buy units back off the same market to dose the crops. The farm
    # trading with itself, paying the spread twice -- but both revenue streams are live.
    "apply_bought": dict(sell_fertilizer=True,  fertilize=True,  buy_fertilizer=True),
    # the herd's output walks to the crop block instead. No market leg at all, and no day-1 cash.
    "self_supply":  dict(sell_fertilizer=False, fertilize=True,  buy_fertilizer=False),
    # hold it and never use it, to price the day-1 cash on its own.
    "hold_only":    dict(sell_fertilizer=False, fertilize=False, buy_fertilizer=False),

    # ---------------------------------------------------------------- when the land is bought
    # **The whole season turns on day 0.** We end day 0 holding $1,187 -- more than the $1,000 NE
    # parcel we then order on day 7 with $50 in hand and silently fail to buy. The idle cash on the
    # cheapest day of the season *is* the quadrant we never own. His day 7 works for him because his
    # herd is already earning by then; ours is not, so the same schedule leaves NE locked all season.
    "land_d0":      dict(land_days=(0,)),
    "land_d0_d12":  dict(land_days=(0, 12)),
    "land_d0_d16":  dict(land_days=(0, 16)),
    "land_d1_d14":  dict(land_days=(1, 14)),
    "land_his":     dict(land_days=(7, 10)),

    # ---------------------------------------------------------------- day 0 as inventory, not cash
    # His day-0 shape, hardcoded. `buy_feed=False` because the point is to live off the day-0 stock
    # rather than re-buy at the day's price -- ordering both would pay twice.
    "prebuy_51":    dict(prebuy_wheat=51, buy_feed=False),
    "prebuy_51_s":  dict(prebuy_wheat=51, prebuy_seeds=18, buy_feed=False),
    "prebuy_100":   dict(prebuy_wheat=100, buy_feed=False),
    "prebuy_both":  dict(prebuy_wheat=51, buy_feed=True),
}


def _resolve(name):
    import importlib
    try:
        return getattr(importlib.import_module(f"kagg.agents.{name}"), "agent")
    except ModuleNotFoundError:
        return name


def play_many(script, opponent, games):
    """Mean final bank over `games`, plus the curve from the first one.

    **Averaged on purpose.** The shop unlock order is randomised across days 3-24, and the same plan
    measured $28,816 and $20,338 on two single games -- a 30% swing. Any conclusion drawn from one
    game is a conclusion about one unlock order.
    """
    finals, wins, curve0, realised0 = [], 0, None, None
    for g in range(games):
        final, theirs, curve, realised = play_with_curve(script, opponent)
        finals.append(final)
        wins += int(final > theirs)
        if curve0 is None:
            curve0, realised0 = curve, realised
    return (float(np.mean(finals)), float(np.min(finals)), float(np.max(finals)),
            wins, games, curve0 or {}, realised0 or {})


def play_with_curve(script, opponent):
    """Final bank plus the dawn bank of every day, read off the real environment's own steps."""
    from kaggle_environments import make

    plan = B.build_plan(script.arrays())

    def agent(obs, config=None):
        step = int(obs.get("step", 0) or 0)
        if step >= len(plan):
            return {"farmer": ["PASS"], "hands": [], "market": []}
        farmer, hands, market = plan[step]
        farms = obs.get("farms")
        n_hands = 0
        if farms:
            me = int(obs.get("player", 0) or 0)
            if me < len(farms):
                n_hands = len(farms[me].get("hands", []) or [])
        return {"farmer": farmer, "hands": hands[:n_hands], "market": market}

    env = make("kaggriculture", debug=False)
    res = env.run([agent, _resolve(opponent)])
    curve, realised = {}, {}
    for t, step in enumerate(res):
        obs = (step[0] or {}).get("observation") or {}
        farms = obs.get("farms") or []
        if len(farms) == 2 and t % R.TURNS_PER_DAY == 0:
            curve[t // R.TURNS_PER_DAY] = float(farms[0]["money"])
            # **What actually exists, not what was ordered.** A BUY_ANIMAL on an empty bank is a
            # silent no-op, so the herd we ordered and the herd we own are different numbers and
            # only the second one earns.
            realised[t // R.TURNS_PER_DAY] = _census(farms[0])
    obs = (res[-1][0] or {}).get("observation") or {}
    farms = obs.get("farms") or []
    final = float(farms[0]["money"]) if len(farms) == 2 else 0.0
    theirs = float(farms[1]["money"]) if len(farms) == 2 else 0.0
    return final, theirs, curve, realised


def _census(farm):
    """`(animals, planted, hands)` owned right now. `tiles` is a nested 10x10 list of dicts, with no
    x/y keys -- iterating it directly yields rows, which is how an earlier audit reported zero of
    everything on a working farm."""
    animals = planted = 0
    for row in farm.get("tiles") or []:
        for cell in (row if isinstance(row, list) else [row]):
            if not isinstance(cell, dict):
                continue
            if cell.get("animal"):
                animals += 1
            if cell.get("plant") or cell.get("crop"):
                planted += 1
    return animals, planted, len(farm.get("hands") or [])


FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]
PRICE_GUESS = {"WHEAT": 30, "FERTILIZER": 100}


def spend_by_day(script):
    """What each day ORDERS, priced at the day-3 table, split by category.

    Priced approximately on purpose -- the point is the ranking of the categories and the shape over
    days, not the cent. Hires are exact, because the Fibonacci ladder resets every dawn and it is the
    one cost that is a pure function of the crew size.
    """
    from kagg.economics import production as P
    a = script.arrays()
    animals = np.asarray(a["buy_animal"])
    products = np.asarray(a["buy_product"])
    seeds = np.asarray(a["buy_seed"])
    hires = np.asarray(a["hire"])
    land = np.asarray(a["buy_land"])
    sells = np.asarray(a["sell"])
    rows = []
    for day in range(R.SEASON_DAYS):
        lo, hi = day * R.TURNS_PER_DAY, (day + 1) * R.TURNS_PER_DAY
        n_hire = int(hires[lo:hi].max()) if hi <= len(hires) else 0
        rows.append(dict(
            day=day,
            animals=sum(int(animals[lo:hi, i].sum()) * _animal_price(i)
                        for i in range(animals.shape[1])),
            feed=sum(int(products[lo:hi, i].sum()) * PRICE_GUESS.get(R.PRODUCTS[i], 50)
                     for i in range(products.shape[1])),
            seeds=sum(int(seeds[lo:hi, i].sum()) * _seed_price(i) for i in range(seeds.shape[1])),
            hires=sum(FIB[:n_hire]),
            n_hire=n_hire,
            land=int(land[lo:hi].sum()),
            sell_units=int(sells[lo:hi].sum()),
        ))
    return rows


ANIMAL_NAMES = list(R.ANIMALS)


def _animal_price(i):
    return int(R.ANIMALS[ANIMAL_NAMES[i]]["cost"])


def _seed_price(i):
    """Seed cost is not in `production.py`; the env's own table is the authority."""
    from kagg.search.routines import CROPS
    return 20


def ordered(script):
    a = script.arrays()
    return dict(
        animals=int(np.asarray(a["buy_animal"]).sum()),
        seeds=int(np.asarray(a["buy_seed"]).sum()),
        products=int(np.asarray(a["buy_product"]).sum()),
        fert_bought=int(np.asarray(a["buy_product"])[:, FERT].sum()),
        fert_sold=int(np.asarray(a["sell"])[:, FERT].sum()),
        hires=int(np.asarray(a["hire"]).sum()),
        collect=int((np.asarray(a["unit_op"]) == R.OP_NAMES.index("COLLECT_FERTILIZER")).sum()),
        apply=int((np.asarray(a["unit_op"]) == R.OP_NAMES.index("FERTILIZE")).sum()),
    )


if args.mixes:
    print("=" * 104)
    print(f"MIX HEAD TO HEAD -- same emitter, same opponent, mean of {args.games} game(s)")
    print("=" * 104)
    print(f"{'mix':>16} {'cow':>4} {'shp':>4} {'straw':>6} {'melon':>6} | {'mean $':>10} "
          f"{'min':>9} {'max':>9} {'wins':>6} | {'pens':>5} {'tiles':>6} {'chains':>7}")
    for name in [m.strip() for m in args.mixes.split(",") if m.strip()]:
        if name not in MIXES:
            print(f"  unknown mix {name}")
            continue
        spec = MIXES[name]
        script, used, refused = mix_plan(**spec)
        mean, lo, hi, wins, n, curve, realised = play_many(script, args.opponent, args.games)
        pens = sum(u[2] for u in used if u[0] == "ranch")
        tiles = sum(u[2] for u in used if u[0] == "grow")
        print(f"{name:>16} {spec['cow']:>4} {spec['sheep']:>4} {spec['strawberry']:>6} "
              f"{spec['melon']:>6} | {mean:>10,.0f} {lo:>9,.0f} {hi:>9,.0f} {wins:>3}/{n:<2} "
              f"| {pens:>5} {tiles:>6} {len(used):>7}")
        for r in refused:
            print(f"{'':>16} REFUSED {r}")
    print()
    print("  Both mixes ask for ~60 crop tiles across three quadrants. If the refusals are identical,")
    print("  the comparison is measuring land we do not own rather than the mix -- read those first.")
    sys.exit(0)

print("=" * 104)
print("DAY-BY-DAY BANK, and what fertilizer policy does to it")
print("=" * 104)

rows = {}
for name in args.variants.split(","):
    name = name.strip()
    if name not in VARIANTS:
        print(f"  unknown variant {name}")
        continue
    script, used, refused = leader_shaped_plan(**VARIANTS[name])
    o = ordered(script)
    final, lo, hi, wins, n, curve, realised = play_many(script, args.opponent, args.games)
    theirs = 0.0
    rows[name] = (final, theirs, curve, o, used, refused, realised,
                  spend_by_day(script), lo, hi, wins, n)
    print(f"\n{name:>14}  final ${final:>10,.0f}   opp ${theirs:>9,.0f}   "
          f"chains {len(used):>2}  animals ordered {o['animals']:>3}  hires {o['hires']:>3}")
    print(f"{'':>14}  fertilizer: collected {o['collect']:>4}  applied {o['apply']:>4}  "
          f"sold {o['fert_sold']:>4}  bought {o['fert_bought']:>4}")
    if refused:
        for r in refused:
            print(f"{'':>14}  REFUSED {r}")

print()
print("=" * 104)
print("DAWN BANK.  his numbers are measured off 90016067.json; a blank means the tape does not say")
print("=" * 104)
hdr = f"{'day':>4} {'HIS':>10}"
for name in rows:
    hdr += f" {name:>14}"
print(hdr)
for day in range(0, 20):
    line = f"{day:>4} {('$' + format(HIS_BANK[day], ',')) if day in HIS_BANK else '':>10}"
    for name, row in rows.items():
        v = row[2].get(day)
        line += f" {('$' + format(int(v), ',')) if v is not None else '-':>14}"
    print(line)

# --------------------------------------------------------------- where the money actually goes
first = next(iter(rows))
_f, _t, curve, _o, _u, _r, realised, spend = rows[first]
print()
print("=" * 104)
print(f"CASH FLOW, plan `{first}`.  ORDERED spend by category against the bank it had to come from")
print("=" * 104)
print(f"{'day':>4} {'bank':>8} {'animals':>8} {'feed':>7} {'seeds':>6} {'hires':>6} "
      f"{'crew':>5} {'land':>5} {'sold':>6} | {'OWN: animals':>13} {'planted':>8} {'hands':>6}")
for r in spend[:20]:
    day = r["day"]
    bank = curve.get(day)
    a, p, h = realised.get(day, (0, 0, 0))
    out = r["animals"] + r["feed"] + r["seeds"] + r["hires"]
    print(f"{day:>4} {('$' + format(int(bank), ',')) if bank is not None else '-':>8} "
          f"{r['animals']:>8} {r['feed']:>7} {r['seeds']:>6} {r['hires']:>6} {r['n_hire']:>5} "
          f"{r['land']:>5} {r['sell_units']:>6} | {a:>13} {p:>8} {h:>6}"
          + ("   <- ordered more than the bank held" if bank is not None and out > bank else ""))

print()
print("=" * 104)
print("READ IT LIKE THIS")
print("=" * 104)
print("  Our day-1 bank far above his $42 -> we are NOT all-in, so nothing compounds. That is the gap,")
print("  and fertilizer income from day 1 is what makes going all-in survivable.")
print("  A variant whose day-1..7 curve collapses to $0 has spent money it had no income to cover.")