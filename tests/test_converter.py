"""Instrumentation for the converter agent, and the regressions it exposed.

`converter` banks $159-$3,859 against `contrarian`'s $51,000. Eight rounds of reordering its
priority list did not converge, and none of them was measured -- this file is the measurement that
should have come first. `play_with_census` runs a real episode and records, per turn, what the agent
*did* (its op mix) alongside what the board *looked like* (live crops, herd, shed, bank), so a
symptom can be traced to the turn it starts on rather than inferred from the final bank.

Run the census on its own with:

    .venv/bin/python -m pytest tests/test_converter.py -s -k report
"""

from collections import Counter

import pytest
from kaggle_environments import make
from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.agents import contrarian, converter

CROP_TILES = ("MELON", "WHEAT", "STRAWBERRY", "CARROT", "TOMATO")


def _board_census(obs, me):
    """Count what is standing on our farm this turn."""
    farm = obs["farms"][me]
    crops, weeds, animals, dry = Counter(), 0, 0, Counter()
    for row in farm["tiles"]:
        for cell in row:
            if not isinstance(cell, dict):
                continue
            if "animal" in cell:
                animals += 1
            elif cell.get("kind") == "WEED":
                weeds += 1
            elif cell.get("kind") == "PLANT":
                crop = cell.get("crop")
                crops[crop] += 1
                if not cell.get("watered_today"):
                    dry[crop] += 1
    return crops, weeds, animals, dry


def play_with_census(seed=4000, opponent=None, seat=0, agent=None):
    """Play a full episode, returning (records, final_money).

    Each record is one turn as *our* agent saw it, taken before the action is applied, plus the
    action it chose. `ops` counts the verb of every unit action, so a turn where twelve hands all
    walk reads as twelve moves rather than one.
    """
    agent = agent or converter.agent
    opponent = opponent or contrarian.agent
    records = []

    def spy(obs, config=None):
        action = agent(obs, config)
        me = obs["player"]
        farm = obs["farms"][me]
        crops, weeds, animals, dry = _board_census(obs, me)
        units = [action["farmer"]] + list(action["hands"])
        records.append({
            "day": obs.get("day", 0),
            "hour": obs.get("hour", 0),
            "money": farm["money"],
            "hands": len(farm.get("hands", [])),
            "ops": Counter(u[0] for u in units),
            "market": Counter(o[0] for o in action["market"]),
            "crops": crops,
            "dry": dry,
            "weeds": weeds,
            "animals": animals,
            "shed": dict(obs["private"].get("shed", {})),
            "seeds": dict(obs["private"].get("seeds", {})),
        })
        return action

    seating = [opponent, spy] if seat else [spy, opponent]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(seating)
    final = env.steps[-1]
    return records, (final[seat]["reward"], final[1 - seat]["reward"])


def by_day(records):
    """Fold the per-turn records into one row per game-day."""
    days = {}
    for r in records:
        d = days.setdefault(r["day"], {
            "ops": Counter(), "market": Counter(), "turns": 0,
            "melon": 0, "dry_melon": 0, "weeds": 0, "animals": 0,
            "money": r["money"], "hands": 0, "shed": {},
        })
        d["ops"] += r["ops"]
        d["market"] += r["market"]
        d["turns"] += 1
        d["melon"] = max(d["melon"], r["crops"].get("MELON", 0))
        d["dry_melon"] = max(d["dry_melon"], r["dry"].get("MELON", 0))
        d["weeds"] = max(d["weeds"], r["weeds"])
        d["animals"] = max(d["animals"], r["animals"])
        d["hands"] = max(d["hands"], r["hands"])
        d["money"] = r["money"]
        d["shed"] = r["shed"]
    return days


def test_report_the_season_day_by_day(capsys):
    """Not an assertion -- the measurement itself. Prints the table the eight tunings lacked."""
    records, money = play_with_census()
    days = by_day(records)

    with capsys.disabled():
        print(f"\nconverter {money[0]:,.0f} vs contrarian {money[1]:,.0f}\n")
        print(f"{'day':>3} {'money':>8} {'hnd':>3} {'mel':>3} {'dry':>3} {'wd':>3} {'anm':>3} "
              f"  {'shed':<34} ops")
        for d in sorted(days):
            row = days[d]
            shed = ", ".join(f"{k[:4]}:{v}" for k, v in sorted(row["shed"].items()) if v)
            ops = " ".join(f"{k[:4].lower()}:{v}" for k, v in row["ops"].most_common(6))
            mkt = " ".join(f"{k[:4].lower()}:{v}" for k, v in row["market"].most_common(4))
            print(f"{d:>3} {row['money']:>8,.0f} {row['hands']:>3} {row['melon']:>3} "
                  f"{row['dry_melon']:>3} {row['weeds']:>3} {row['animals']:>3}   "
                  f"{shed[:34]:<34} {ops}  | {mkt}")

        total = Counter()
        for row in days.values():
            total += row["ops"]
        print(f"\nseason op census: {dict(total.most_common())}")


def test_it_does_not_harvest_immature_crops():
    """The root cause of every symptom in the handoff's table.

    `_new_plant` sets `yield_units = 1` immediately for any crop with `ongoing=False`, and melon's
    `first_yield_day` is 10 -- so `yield_units > 0` reads true from the moment the seed goes in,
    while the environment's HARVEST silently returns for ten days. A unit that picks HARVEST on that
    basis is issuing a legal no-op which cannot clear its own precondition, so it re-picks it every
    turn and nothing below it in the priority list is ever reached.
    """
    wasted = []

    def spy(obs, config=None):
        action = converter.agent(obs, config)
        me, day = obs["player"], obs.get("day", 0)
        tiles = obs["farms"][me]["tiles"]
        positions = ([tuple(obs["farms"][me]["farmer"])]
                     + [tuple(h) for h in obs["farms"][me].get("hands", [])])
        for pos, act in zip(positions, [action["farmer"]] + list(action["hands"])):
            if act[0] != "HARVEST":
                continue
            cell = tiles[pos[1]][pos[0]]
            if not (isinstance(cell, dict) and cell.get("kind") == "PLANT"):
                continue
            if day - cell["planted_day"] < kg.CROPS[cell["crop"]]["first_yield_day"]:
                wasted.append((day, obs.get("hour"), pos, cell["crop"]))
        return action

    env = make("kaggriculture", configuration={"seed": 4000}, debug=False)
    env.run([spy, contrarian.agent])

    assert not wasted, (
        f"{len(wasted)} no-op HARVEST actions on immature crops, first few: {wasted[:5]}")


def test_it_waters_on_the_day_it_plants():
    """A seed planted today is dead by morning unless it is watered today.

    `_new_plant` opens with `consecutive_unwatered = 1` -- the planting day already counts against
    the crop -- and `_daily_refresh_crops` turns any tile at 2 into a WEED. So planting carries a
    same-day watering debt, and a day that plants more tiles than it waters is a day that throws
    seed away. Measured before the fix: fourteen melon planted across day 0, the last at hour 23,
    zero watered, all fourteen weeds by morning.
    """
    records, _ = play_with_census()
    days = by_day(records)

    debt = {d: (days[d]["ops"]["PLANT"], days[d]["ops"]["WATER"])
            for d in sorted(days) if days[d]["ops"]["PLANT"]}
    unpaid = {d: pw for d, pw in debt.items() if pw[1] < pw[0]}

    assert not unpaid, f"planted more than it watered on {unpaid} (day: plant, water)"


def test_the_melon_crop_survives_the_opening():
    """The measured symptom: 3 tiles at day 2, 0 by day 6.

    Melon is the opening economy and pays for the herd, so losing it loses the game on day 6
    whatever happens afterwards. `PARAMS["melon_tiles"]` is 14; this asks for most of them alive
    at the point the replay's winners were expanding.

    Green since the maturity check and the watering order went in: 13 of the 14 stand from day 2
    to day 10 and are harvested, against 3 planted and 0 surviving before.
    """
    records, _ = play_with_census()
    days = by_day(records)

    alive = {d: days[d]["melon"] for d in sorted(days) if d <= 8}
    assert alive.get(6, 0) >= 10, f"melon dies in the opening: {alive}"


def test_it_harvests_what_it_plants():
    """Zero HARVEST across a season was the root symptom under the last rewrite.

    Nothing harvested means nothing in the shed, nothing sold, no bank, and so no herd either.
    """
    records, _ = play_with_census()
    total = Counter()
    for r in records:
        total += r["ops"]

    assert total["HARVEST"] > 0, f"nothing was ever harvested: {dict(total)}"


@pytest.mark.xfail(strict=True, reason="diagnosed and measured; the obvious fix made it worse")
def test_it_never_hires_a_crew_it_cannot_pay_for():
    """The wage bill is Fibonacci and the hire block never checks the bank.

    `_hire_cost` is `fib(n)` for the n-th hire of the day, so a crew costs $376/day at twelve,
    $609 at thirteen and **$986 at fourteen** -- hands 13 and 14 together cost more than the first
    twelve combined. `max_hands` is 14.

    `reserve` is honoured for wheat, animals and land, and ignored for wages: `target_hands` is
    derived from the job count alone and the order is appended with no reference to `money`. In the
    livestock phase the job count is always large, so it hires to the cap every day regardless.
    Measured: 390 HIRE orders against 52 SELLs, $45,280 in and $44,258 out, and a bank sitting at
    $18-$67 for days 13-14 and 22-26 -- permanently one turn from being unable to act.

    **Left failing on purpose: the obvious fix is worse than the bug.** Gating the hire on
    `money - reserve` against the marginal `fib(n)` fee was tried across seven configurations and
    every one scored at or below the unfixed agent on the ladder -- 0.000 for most, 0.033 at best,
    against 0.100 for doing nothing about it. The gate reads `money` during the market block, which
    is *before* the turn's sales settle, and it can veto even the `min_hands` floor, so the farm
    collapses to the lone farmer and stops earning at all. The diagnosis stands; the remedy has to
    price the hand against what it will *produce*, not against the cash in hand at that instant.
    """
    records, _ = play_with_census()

    broke = [(r["day"], r["hour"], r["money"]) for r in records
             if r["money"] < converter.PARAMS["reserve"] and r["market"].get("HIRE")]

    assert not broke, (
        f"hired below the ${converter.PARAMS['reserve']:.0f} reserve on {len(broke)} turns, "
        f"first few: {broke[:5]}")


@pytest.mark.xfail(strict=True, reason="the livestock phase is still broken -- next piece of work")
def test_the_feed_loop_does_not_dominate_the_crew():
    """517 PICKUP against 128 FEED: the crew spent its season walking wheat, not farming.

    A PICKUP carries up to six wheat, so a healthy ratio is well under one pickup per feed.

    Still 562 against 197, and unaffected by either crop fix -- this is the livestock half of the
    agent and it is a separate bug. `strict=True` so that whatever fixes it is told immediately
    rather than leaving a stale xfail behind.
    """
    records, _ = play_with_census()
    total = Counter()
    for r in records:
        total += r["ops"]

    assert total["PICKUP"] <= max(4, total["FEED"]), (
        f"feed logistics dominate: {total['PICKUP']} PICKUP vs {total['FEED']} FEED")
