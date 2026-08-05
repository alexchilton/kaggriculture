"""The leader's own funding profile, as a contract our emitter must be able to meet.

**These are meant to be red.** Every number in here is measured off his tape
(`data/seed_scripts/new_leader/90016067.json`, `scripts/audit_leader_wheat.py`,
`scripts/diff_emitter_vs_leader.py`) and every one of them is something our machinery cannot currently
produce. That is the point: the previous tests in this project asserted properties of our own code and
went green while the farm banked $40k against his $139k. A test that only checks what we already do
cannot tell us what is missing.

What the tape says, day by day, for the first fortnight:

    day  0  $3,000   BUY_ANIMALx4 BUY_PRODUCTx16 BUY_SEEDx4 HIREx4 SELLx12
    day  1  $   42   <- he ends day 0 on forty-two dollars
    day  2  $  141
    day  3  $  217
    day  5  $  621
    day  7  $1,719   BUY_LANDx1
    day 10  $1,278   BUY_LANDx1     <- a $2,000 parcel on a $1,278 dawn bank
    day 11  $3,236
    day 12  $6,828
    day 13  $14,622

Three properties follow, and none of them is about tiles:

1. **He goes all-in on day 0.** Four animals, ~51 wheat in small lots across all 24 hours, 18 seeds,
   4 hires. Our best plan ends day 0 holding thousands and never starts compounding.
2. **His early revenue is FERTILIZER, not milk.** Day 1 hour 8 he sells 4 units. A fed animal sets
   `fertilizer_available` every night and COLLECT_FERTILIZER costs no action, so this is free money from
   day 1 -- milk does not arrive until day 8. Census: his 318 collections against our **83**, and 107
   FERTILIZE ops against our **0**.
3. **He ramps the herd.** 4 animals on day 0, then +2, +1, +4, +1, +2 through day 10 to reach 14. Buying
   14 at once is insolvent -- measured: ordered 14, only 8 ever appeared, bank sat at $301 on day 10.

The reason we cannot do (1) is mechanical and worth stating, because it is the fix: **`ranch()` raises
one pen per day.** One chain of four pens buys its first animal on day 0 and its fourth on day 3, so our
day-1 bank was $2,301 against his $42 purely because three purchases had not happened yet. His shape is
**four multi-pen chains all starting day 0** -- four animals bought immediately, still only four hands.
"""

import collections

import numpy as np
import pytest

from kagg.search import routines as R

FERT = R.PRODUCTS.index("FERTILIZER")
SHED = R.shed_access_tiles()

# Measured off the tape. `scripts/audit_leader_wheat.py` and the day-by-day trace above.
HIS_DAY0_ANIMALS = 4
HIS_HERD_BY_DAY10 = 14
HIS_COLLECT_FERTILIZER = 318
HIS_HANDS = 12


def cluster(quadrant, n, taken):
    """`n` mutually adjacent tiles in `quadrant`, nearest the shed first.

    Compactness, not proximity: tiles sorted only by distance from the shed form a diagonal ring, each
    diagonal step costs two moves, and four such pens need 25 of the 23 work turns.
    """
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


def leader_shaped_plan():
    """Our emitter, driven at his shape: several multi-pen chains all starting on day 0.

    Deliberately built with `routines.py` directly rather than through a genome, so a failure here is a
    statement about the **emitter's capability** and not about the search's luck. If this cannot produce
    his profile, no amount of searching will.
    """
    script = R.Script()
    taken, used, refused = set(), [], []
    # **A unit is chosen for its SPAWN QUADRANT, not taken in order.** Hands fill the shed cells in
    # NWSE order and the cycle repeats every four, so units 0/4/8/12 wake in NW, 1/5/9/13 in NE and
    # 2/6/10/14 in SW. Handing an NW pen group to unit 1 makes it walk in from `(5,4)` every dawn:
    # measured, `4 pen(s) at [(2,2),(2,3),(1,4),(2,4)] from (5,4) needs 25 turns` of a 23-turn day, and
    # `ranch()` refuses it. The walk, not the pen count, is what breaks a group.
    pools = {q: [u for u in range(20) if R.quadrant_of(*R.spawn_tile(u)) == q]
             for q in ("NW", "NE", "SW", "SE")}
    def take(quadrant):
        return pools[quadrant].pop(0) if pools[quadrant] else None
    # Land on days 7 and 10, never SE -- exactly his tape. Farm-level, one parcel per day.
    for day in (7, 10):
        t = day * R.TURNS_PER_DAY
        if 0 <= t < script.T:
            script.buy_land[t] += 1

    # **Largest group and lowest unit that `ranch()` will actually accept.**
    # Hand-picking either one kept failing for a reason only the emitter knows: 4 pens at
    # [(2,2),(2,3),(1,4),(2,4)] need 25 of 23 turns even walking from the correct NW spawn (4,4),
    # because those tiles are 3-4 steps out. Group size has to shrink with distance from the shed, and
    # the only authority on what fits is `ranch()` itself. Lowest unit keeps the hire ladder short --
    # it is Fibonacci in the day's hire count and reset every dawn, so unit 16 is paid 30 times.
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
                            sell_fertilizer=True, build_every=build_every)
                    taken.update(group)
                    busy.add(unit)
                    used.append(("ranch", animal, len(group), f"u{unit}", f"d{start_day}"))
                    placed += len(group)
                    break
                else:
                    continue
                break
            else:
                refused.append(f"{animal}: nothing fits for the last {want - placed} pen(s) in {quadrant}")
                break
            if single_chain:
                break
        return placed

    busy = set()
    # 8 cows + 6 sheep = his 14, spread as his tape does it: NW from day 0, NE once the day-7 parcel
    # lands, SW after day 10.
    # **Four separate chains on day 0, not one big one.** `ranch()` raises one pen per day, so a chain
    # of four pens buys its first animal on day 0 and its fourth on day 3. Four chains of two buy FOUR
    # animals on day 0 -- his number -- and still occupy only four hands.
    # **Four chains on day 0, each as large as the day will take.** Both halves matter and they pull
    # against each other:
    #   - four separate chains, because `ranch()` raises one pen per day, so one chain of four buys its
    #     first animal on day 0 and its fourth on day 3 -- our day-1 bank was $2,301 against his $42;
    #   - each chain multi-pen, because a chain is a hand, and 14 pens over 6 chains took us to 11 hands
    #     and $11,056 where the same herd over 5 chains banked $31,557. The ladder is Fibonacci and
    #     reset every dawn, so a hand is paid 30 times.
    # He resolves it the same way: 14 pens over ~5 hands, 4 animals on day 0.
    # `build_every=3` because four chains each raising a pen a day buys FOUR animals a day for four
    # days -- $6,800 against a $3,000 bank, so most silently no-op while the feed and hire bills run.
    # At 3 the herd arrives on days 0, 3, 6, 9 per chain, which is his measured rate: 4 on day 0 then
    # +2, +1, +4, +1, +2 through day 10.
    for animal in ("COW", "COW", "COW", "SHEEP"):
        place_pens(animal, 4, "NW", 0, single_chain=True, build_every=3)
    place_pens("SHEEP", 2, "SW", 10)

    # And the crops, because he is not an animal farm: ~41 strawberry, ~20 melon. NE opens on day 7 and
    # SW on day 10, so their blocks cannot start before the parcel lands.
    for crop, size, quadrant, day in (("MELON", 6, "NW", 1), ("STRAWBERRY", 8, "NE", 8),
                                      ("STRAWBERRY", 8, "NE", 9), ("STRAWBERRY", 8, "SW", 11),
                                      ("MELON", 6, "SW", 12)):
        block = cluster(quadrant, size, taken)
        if not block:
            refused.append(f"no tiles for {crop}x{size} in {quadrant}")
            continue
        for unit in range(16):
            if unit in busy:
                continue
            probe = R.Script()
            try:
                R.grow(probe, crop, block, plant_day=day, unit=unit, buy_land=False, water_every=2)
            except ValueError:
                continue
            R.grow(script, crop, block, plant_day=day, unit=unit, buy_land=False, water_every=2)
            taken.update(block)
            busy.add(unit)
            used.append(("grow", crop, len(block), f"u{unit}"))
            break
        else:
            refused.append(f"no unit fits {crop}x{len(block)} in {quadrant} on d{day}")
    return script, used, refused


def per_day(arr):
    out = collections.Counter()
    a = np.asarray(arr)
    for t in range(a.shape[0]):
        v = int(a[t].sum()) if a[t].ndim else int(a[t])
        if v:
            out[t // R.TURNS_PER_DAY] += v
    return out


# ---------------------------------------------------------------- 1. all-in on day 0
def test_four_animals_are_bought_on_day_zero():
    """His day 0 buys four. Ours buys one, because `ranch()` raises a pen a day.

    This is the single most consequential difference in the whole season: it is why our day-1 bank is
    $2,301 against his $42, and a farm that keeps its money cannot start compounding.
    """
    script, used, refused = leader_shaped_plan()
    day0 = per_day(script.buy_animal).get(0, 0)
    assert day0 >= HIS_DAY0_ANIMALS, (
        f"day 0 orders {day0} animal(s) against his {HIS_DAY0_ANIMALS}. refused: {refused}")


def test_the_herd_reaches_fourteen_by_day_ten():
    """His ramp: 4, +2, +1, +4, +1, +2. Not 14 at once -- that was measured insolvent, 8 of 14 arriving."""
    script, used, refused = leader_shaped_plan()
    by_day = per_day(script.buy_animal)
    cumulative = sum(v for d, v in by_day.items() if d <= 10)
    assert cumulative >= HIS_HERD_BY_DAY10, (
        f"only {cumulative} animals ordered by day 10 against his {HIS_HERD_BY_DAY10}. "
        f"refused: {refused}")


# ---------------------------------------------------------------- 2. fertilizer is the early engine
def test_fertilizer_is_sold_from_day_one():
    """Day 1, hour 8: `SELL FERTILIZER x4`. Milk does not arrive until day 8, so this funds the ramp."""
    script, used, refused = leader_shaped_plan()
    fert_by_day = per_day(np.asarray(script.sell)[:, [FERT]])
    early = [d for d in fert_by_day if d <= 2]
    assert early, (
        "no FERTILIZER sold in the first three days; his first sale is day 1 hour 8 and it is the only "
        "revenue he has before milk on day 8")


def test_fertilizer_is_collected_at_his_rate():
    """318 collections against our measured 83. A fed animal sets it nightly and the collect is free."""
    script, used, refused = leader_shaped_plan()
    n = int((np.asarray(script.unit_op) == R.OP["COLLECT_FERTILIZER"]).sum())
    assert n >= HIS_COLLECT_FERTILIZER * 0.75, (
        f"{n} COLLECT_FERTILIZER ops against his {HIS_COLLECT_FERTILIZER}; every missed night abandons "
        f"a free unit of the product that is 23.1% of winner sales")


# ---------------------------------------------------------------- 3. it has to stay solvent
def test_the_plan_stays_solvent_through_the_ramp():
    """Ordering capacity is not owning it: `buy_animal` silently no-ops when money is short.

    Measured on a hand-built 14-animal plan: 14 ordered, **8** realised, bank $301 on day 10. So the
    test is on realised animals, not ordered ones -- the distinction the whole season turns on.
    """
    import jax.numpy as jnp
    from kagg.sim import jax_sim as J

    fields = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
              "buy_product", "buy_animal", "hire", "buy_land")
    script, used, refused = leader_shaped_plan()
    a = script.arrays()
    state = J.reset_with_shops(1, seed=0)
    money = []
    for t in range(script.T):
        money.append(float(np.asarray(state.farm.money)[0, 0]))
        acts = {f: jnp.asarray(np.stack([np.asarray(a[f][t]),
                                         np.zeros_like(np.asarray(a[f][t]))])[None])
                for f in fields}
        state = J.step(state, J.Actions(**acts), weed_chance=0.0)
    final = float(np.asarray(state.farm.money)[0, 0])
    ordered = int(np.asarray(script.buy_animal).sum())
    assert min(money[24:]) >= 0, "the farm went negative, which the sim does not even allow"
    assert final > 40_000, (
        f"a leader-shaped plan banks ${final:,.0f} from {ordered} ordered animals; his profile is worth "
        f"$139,121 and our searched 6-chain plan already makes $38,948, so this shape is not yet "
        f"paying. plan={used} refused={refused}")


def test_his_whole_farm_fits_twelve_hands():
    """He does 14 pens plus ~60 tiles with 12 hands. Any plan needing materially more pays the ladder."""
    script, used, refused = leader_shaped_plan()
    hired = int(np.asarray(script.hire).max())
    assert hired <= HIS_HANDS, (
        f"{hired} hands hired against his {HIS_HANDS}; the Fibonacci ladder resets every dawn so this "
        f"is paid 30 times")