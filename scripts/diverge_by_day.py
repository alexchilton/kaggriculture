"""Run the winner's genome and diff it against the winner's own per-day curves, day by day.

Alex's design, and it beats the abstract test it replaces: rather than assert "the genome cannot
express a ramp", *play* the encoded genome and print, for each of the 30 days, what our executor did
against what the seat actually did. The first day the two curves part names the gene block that
broke, and how.

The measured seat is episode 89113699 seat 1, $132,245: 28 pastures, 21 crop tiles, one land parcel
on day 10, and an animal count that holds at 4 for eleven days and then jumps to 17.

Columns, ours vs theirs: money, crew, live animals, pens standing, and -- ours only, because the
replay has no such thing -- animals lost to escape, which is the failure `consecutive_unfed >= 2`
delivers when a plan buys animals it cannot feed.

    PYTHONPATH=. python3 -u scripts/diverge_by_day.py 2>&1 | tee data/logs/diverge_by_day.log
"""

import argparse

import numpy as np

from kagg.search import executor as X
from kagg.search import library, plan as P, replay_plan as RP, rollout
from kagg.sim.game import Actions, Game
from kagg.sim.tiles import COOP, PASTURE

SEAT_UNDER_TEST = 0


def trace(seat_plans, unlock_schedule, weed_chance=0.005, rng=None):
    """Play a season, recording one row per day for the seat under test at that day's last hour."""
    batch = seat_plans[0].size
    game = Game(batch, weed_chance=weed_chance, rng=rng, unlock_schedule=unlock_schedule)
    actions = Actions(batch)
    rows = []
    # An animal that escapes vanishes from `tiles.animal`, so escapes are not directly observable;
    # count them as (animals ever placed) - (animals alive), tracked off the day-to-day drop.
    prev_live, escaped = 0, 0
    revenue, hire_spend = 0.0, 0.0

    for step in range(719):
        day, hour = step // 24, step % 24
        for player in (0, 1):
            view = rollout.build_view(game, player, day, hour)
            rollout._write(actions, player, X.decide(view, seat_plans[player]))
        if game.step(actions):
            break

        # **Sampled mid-day, not at hour 23.** The dawn reset dismisses every hand inside the
        # hour-23 `step`, so a row taken after it reports a crew of 1 every single day regardless of
        # how many hands were hired -- which is a fact about the sampling point, not about hiring.
        # Gross sales, accumulated from the decision rather than the money column, because 12-13
        # hires a day on a Fibonacci ladder swamp the balance and make revenue unreadable from cash.
        for player, pl in ((0, seat_plans[0]),):
            v = rollout.build_view(game, player, day, hour)
            dec = X.decide(v, pl)
            revenue += float((np.minimum(dec.sell[0], v.shed[0]) * v.prices[0]).sum())
            hire_spend += float(dec.hire[0])

        if hour == 12:
            tiles, farm = game.tiles[SEAT_UNDER_TEST], game.farms[SEAT_UNDER_TEST]
            live = int((tiles.animal[0] >= 0).sum())
            pens = int(((tiles.kind[0] == PASTURE) | (tiles.kind[0] == COOP)).sum())
            if live < prev_live:
                escaped += prev_live - live
            prev_live = live
            rows.append({
                "day": day,
                "money": float(farm.money[0]),
                "crew": int(farm.n_units[0]),
                "live": live,
                "pens": pens,
                "land": int(farm.n_land[0]),
                "unfed": int((tiles.consecutive_unfed[0] * (tiles.animal[0] >= 0)).max()),
                "escaped": escaped,
                "shed_animals": int(farm.shed[0, X.ANIMAL_ITEM_BASE:].sum()),
                "wheat": int(farm.shed[0, X.WHEAT_ITEM]),
                # The revenue engine. The $147k seat commits 63 tiles to crops (WHEAT 25,
                # STRAWBERRY 24, MELON 14) against 12 pens, so "is anything growing" is the
                # first question to ask of a season that ends on $0.
                "growing": int((tiles.crop[0] >= 0).sum()),
                "ripe": int(tiles.yield_units[0].sum()),
                "produce": int(farm.shed[0].sum() - farm.shed[0, X.WHEAT_ITEM]
                               - farm.shed[0, X.ANIMAL_ITEM_BASE:].sum()),
                "seeds": int(farm.seeds[0].sum()),
                "revenue": revenue,
                "hires_asked": hire_spend,
            })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", default="data/89113699.json")
    ap.add_argument("--seat", type=int, default=1)
    a = ap.parse_args()

    layout = RP.layout_from_replay(a.episode, seat=a.seat)
    genome = RP.genome_from_layout(layout)
    print(f"measured seat: ${layout.money:,.0f}   {layout.n_pasture} pasture  {layout.n_coop} coop  "
          f"{sum(layout.crop_counts.values())} crop  land {layout.land_days}\n")

    # What the genome asks for, decoded, so the table can be read against the intent.
    mine = P.decode(genome[None])
    lo, _ = P.gene_slice("herd")
    print("genome asks for:")
    print(f"  herd target      : " + "  ".join(
        f"{n}={int(mine.herd[0, i])}" for i, n in enumerate(P.ANIMAL_NAMES)))
    print(f"  stock_day        : {int(mine.stock_day[0])}")
    print(f"  feed_wheat/animal: {int(mine.feed_wheat[0])}")
    print(f"  land_day         : {list(np.asarray(mine.land_day[0]))}")
    print(f"  hires (per day)  : " + " ".join(f"{int(h):>2}" for h in mine.hires[0]))
    print(f"  HERD_LEVELS ladder tops out at {int(P.HERD_LEVELS.max())} per species\n")

    opp = P.decode(library.opposition())
    # One opponent, one schedule: this is a diagnostic of our own execution, not an evaluation.
    pair = (mine, opp.take([0]))
    rng = np.random.default_rng(0)
    schedule = rollout.sample_unlock_schedule(np.random.default_rng(0))
    rows = trace(pair, schedule, rng=rng)

    print("=" * 96)
    print(f"{'day':>3} | {'OURS money':>11} {'crew':>4} {'live':>4} {'pens':>4} {'land':>4} "
          f"{'grow':>4} {'seed':>4} {'ripe':>4} {'prod':>4} {'wheat':>6} {'esc':>4} "
          f"{'gross$':>10} | "
          f"{'THEIRS crew':>11} {'live':>4}")
    print("=" * 96)
    for r in rows:
        d = r["day"]
        their_crew = layout.crew_by_day[d] if d < len(layout.crew_by_day) else 0
        their_live = layout.animals_by_day[d] if d < len(layout.animals_by_day) else 0
        print(f"{d:>3} | {r['money']:>11,.0f} {r['crew']:>4} {r['live']:>4} {r['pens']:>4} "
              f"{r['land']:>4} {r['growing']:>4} {r['seeds']:>4} {r['ripe']:>4} {r['produce']:>4} "
              f"{r['wheat']:>6} {r['escaped']:>4} {r['revenue']:>10,.0f} | {their_crew:>11} {their_live:>4}")
    print("=" * 96)
    print(f"crop tiles the genome commits: {sum(layout.crop_counts.values())}  {layout.crop_counts}")

    last = rows[-1]
    print(f"\nfinal: ours ${last['money']:,.0f}   theirs ${layout.money:,.0f}   "
          f"gap ${last['money'] - layout.money:,.0f}")
    print(f"animals lost to escape: {last['escaped']}  "
          f"(each one cost its purchase price outright)")
    peak_theirs = max(layout.animals_by_day)
    peak_ours = max(r["live"] for r in rows)
    print(f"peak live animals: ours {peak_ours}, theirs {peak_theirs}")
    stuck = [r["day"] for r in rows if r["shed_animals"] > 0]
    if stuck:
        print(f"animals sitting in the shed, never placed, on days: {stuck[0]}..{stuck[-1]} "
              f"(peak {max(r['shed_animals'] for r in rows)})")


if __name__ == "__main__":
    raise SystemExit(main())
