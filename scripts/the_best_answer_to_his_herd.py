"""The best allocation against a given opponent herd, solved on the market maths rather than played.

**Why this is not another sweep.** Every allocation question in this project has been answered by
playing a season, which costs ~90s and answers for exactly one opponent. But the market is
deterministic: `market_price` (`reference/kaggriculture.py:191`) is a pure function of inventory,
`_process_market` is a per-unit lockstep, and the town drain is a fixed function of the shop draw.
So if you know WHEN each side puts units into a book, the revenue both sides get is arithmetic.

That makes the whole allocation question a surface that can be enumerated:

    ours   (cows, sheep, geese, and the strawberry the freed pens pay for)
    theirs (cows, sheep, strawberry volume)

and evaluated exactly, for every combination, in the time one season takes to play.

**What is measured and what is assumed.**

Measured, from a played season (`what_one_animal_is_worth.py` validates the same replayer against
the recorded fills to 0.03%):

- the per-turn SHAPE of each side's supply into each book
- the drain schedule, from the seed's own shop draw
- the per-animal yield: our 186 milk from 4 cows and 189 wool from 4 sheep give 46.5 and 47.3
  units a season, which also reads the tape's herd off his volume

Assumed, and these are the numbers to argue with:

- supply scales LINEARLY in animal count and keeps its timing. True for the book (a cow yields on
  a fixed cadence); false at the margin where a bigger herd starves for feed actions.
- a pen slot converted to crop is worth `STRAW_PER_SLOT` strawberry units. This is a planner
  question, not a market one, and nothing here measures it -- so it is swept, not fixed.
- both sides sell everything they produce. The floor rule ("sales at $1 do not increase market
  supply", `_commit_unit`) means dumping into a dead book is free, so this is close to true.

    python -u scripts/the_best_answer_to_his_herd.py --seed 11
    python -u scripts/the_best_answer_to_his_herd.py --seed 11 --straw-per-slot 40,66,100
"""
import argparse
import collections
import importlib
import importlib.util
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "scripts"))

_spec = importlib.util.spec_from_file_location("kg", str(REPO / "reference/kaggriculture.py"))
KG = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(KG)

TPD = 24
DAYS = 30
#: Units a season, measured on seed 11: 186 milk / 4 cows, 189 wool / 4 sheep.
PER_COW, PER_SHEEP = 46.5, 47.3
#: GOOSE yields every night from day 4 (`reference:823`, `first_yield_day 4, interval 1`).
#: `max_held 4` is the ceiling; 1/night is the floor and is what an unfed-some-nights bird gives.
GOOSE_PER_NIGHT = 2.0
#: `reference/kaggriculture.py:ANIMALS`.
COST = {k: KG.ANIMALS[k]["cost"] for k in ("COW", "SHEEP", "GOOSE")}


def play_base(seed):
    """One season. Returns per-turn per-seat unit counts, and the shop list per turn."""
    import breakdown as B
    from kagg.search import melon_branch as _MB
    from kaggle_environments import make
    from kagg.analysis.fills import record_fills
    SA = importlib.import_module("kagg.search.schedule_agent"); B.schedule_agent = SA
    _MB.OPPONENT_MELON = 0
    SA.NEVER_DRAINED = (); SA.HERD_GEESE = 0
    rep = str(REPO / "data/seed_scripts/kawashigi/92466371.json")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY} for k, r in raw.items()}
    env = make("kaggriculture", configuration=dict(B.env_config(rep), seed=seed, weedSpawnChance=0.0),
               debug=True)
    env.reset(2); p0 = SA.make_agent(sched, 0); p1 = B.tape_policy(rep, "カワシギ", 1)
    shops = []
    with record_fills(env) as f:
        for t in range(TPD * DAYS):
            o0, o1 = env.state[0].observation, env.state[1].observation
            shops.append(list(o0["town"]["unlocked_shops"]))
            a0, a1 = p0(o0, t), p1(o1, t)
            n0 = len(o0["farms"][0].get("hands") or []); n1 = len(o1["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                      {"farmer": a1.get("farmer") or ["PASS"], "hands": list(a1["hands"])[:n1],
                       "market": a1.get("market") or []}])
            if env.done: break
        prof = {}
        for seat in (0, 1):
            for d, h, op, it, pr in f.at_turn(seat):
                if op != "SELL":
                    continue
                prof.setdefault(it, [[0] * (TPD * DAYS), [0] * (TPD * DAYS)])
                prof[it][seat][d * TPD + h] += 1
    while len(shops) < TPD * DAYS:
        shops.append(shops[-1] if shops else [])
    return prof, shops


def drain_at(item, shops_t, step):
    d = 0
    if step % 4 == 0:
        for s in shops_t:
            ps = KG.SHOPS[s]
            if item in ps:
                d += 2 if len(ps) == 1 else 1
    if step % 24 == 0 and item in KG.TOWN_CENTER_PRODUCTS:
        d += 1
    return d


_DRAIN = {}


def drain_series(item, shops):
    """Per-turn drain for one product. Cached: it depends only on the shop draw, not on supply."""
    key = item
    if key not in _DRAIN:
        _DRAIN[key] = [drain_at(item, shops[t], t) for t in range(TPD * DAYS)]
    return _DRAIN[key]


def book(item, ours, theirs, shops):
    """Replay one product's book. `ours`/`theirs` are per-turn unit counts. Returns (rev_a, rev_b)."""
    inv = KG.MARKET_PARAMS[item]["I0"]
    ra = rb = 0.0
    price = KG.market_price
    dr = drain_series(item, shops)
    for t in range(TPD * DAYS):
        na, nb = ours[t], theirs[t]
        if na or nb:
            while na > 0 or nb > 0:
                p = price(item, inv)
                add = 0
                if na > 0:
                    ra += p; na -= 1; add += 1 if p > 1 else 0
                if nb > 0:
                    rb += p; nb -= 1; add += 1 if p > 1 else 0
                inv += add
        inv -= dr[t]
    return ra, rb


def scaled(profile, factor):
    """Scale a per-turn profile, carrying the fraction so the season total is right."""
    out = [0] * len(profile)
    carry = 0.0
    for t, n in enumerate(profile):
        want = n * factor + carry
        k = int(want)
        carry = want - k
        out[t] = k
    return out


def goose_profile(n_geese, per_night):
    out = [0] * (TPD * DAYS)
    carry = 0.0
    for day in range(4, DAYS):
        want = n_geese * per_night + carry
        k = int(want); carry = want - k
        out[day * TPD + 18] = k
    return out


def straw_extra(profile, extra_units):
    """Add `extra_units` spread over the days the base profile already sells on."""
    live = [t for t, n in enumerate(profile) if n > 0]
    out = list(profile)
    if not live or extra_units <= 0:
        return out
    for i in range(int(extra_units)):
        out[live[i % len(live)]] += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--pens", type=int, default=8,
                    help="animal slots BOTH sides can actually work. Not the pen count: the "
                         "schedule asks for 14 animals and the live agent buys 8, because FEED "
                         "and CARE are action-limited (`SHOP_ADAPT_HERD`/`_herd_split`). "
                         "14 is the pen ceiling and is not the binding constraint.")
    ap.add_argument("--no-cost", action="store_true",
                    help="price the market only, ignoring what the animals cost to buy")
    ap.add_argument("--straw-per-slot", default="66",
                    help="comma list: strawberry units a freed pen slot buys")
    a = ap.parse_args()

    print(f"seed {a.seed}: playing one season to measure the supply shapes ...", flush=True)
    prof, shops = play_base(a.seed)
    z = [0] * (TPD * DAYS)
    g = lambda it, seat: (prof.get(it) or [list(z), list(z)])[seat]
    our_milk, his_milk = g("MILK", 0), g("MILK", 1)
    our_wool, his_wool = g("WOOL", 0), g("WOOL", 1)
    our_straw, his_straw = g("STRAWBERRY", 0), g("STRAWBERRY", 1)

    base_cows = max(1e-9, sum(our_milk) / PER_COW)
    base_sheep = max(1e-9, sum(our_wool) / PER_SHEEP)
    his_cows0 = max(1e-9, sum(his_milk) / PER_COW)
    his_sheep0 = max(1e-9, sum(his_wool) / PER_SHEEP)
    print(f"  ours: milk {sum(our_milk):>4} ({base_cows:.1f} cows)  wool {sum(our_wool):>4} "
          f"({base_sheep:.1f} sheep)  straw {sum(our_straw):>4}")
    print(f"  his : milk {sum(his_milk):>4} ({his_cows0:.1f} cows)  wool {sum(his_wool):>4} "
          f"({his_sheep0:.1f} sheep)  straw {sum(his_straw):>4}")
    ns = collections.Counter()
    for sh in shops[-1]:
        for pp in KG.SHOPS[sh]:
            ns[pp] += 1
    print("  shops draining: " + "  ".join(f"{k}:{v}" for k, v in sorted(ns.items())))
    print()

    N = a.pens
    HIS = list(range(0, 15, 2))
    HIS_STRAW = [0.0, 0.5, 1.0]

    # **The books are independent, so the surface is separable.** MILK depends only on
    # (our cows, his cows), WOOL only on sheep, EGG only on our geese, STRAWBERRY only on the
    # freed slots and his volume. 14x14x3 opponents against 680 own allocations is 130,560
    # evaluations; memoised per product it is ~300.
    milk = {(c, hc): (lambda r: r[0] - r[1])(book("MILK", scaled(our_milk, c / base_cows),
                                                  scaled(his_milk, hc / his_cows0), shops))
            for c in range(N + 1) for hc in HIS}
    wool = {(s, hs): (lambda r: r[0] - r[1])(book("WOOL", scaled(our_wool, s / base_sheep),
                                                  scaled(his_wool, hs / his_sheep0), shops))
            for s in range(N + 1) for hs in HIS}
    egg = {gg: (lambda r: r[0] - r[1])(book("EGG", goose_profile(gg, GOOSE_PER_NIGHT), z, shops))
           for gg in range(N + 1)}

    for sps in [float(x) for x in a.straw_per_slot.split(",")]:
        straw = {(fr, hst): (lambda r: r[0] - r[1])(
                     book("STRAWBERRY", straw_extra(our_straw, fr * sps),
                          scaled(his_straw, hst), shops))
                 for fr in range(N + 1) for hst in HIS_STRAW}

        def best_against(hc, hs, hst):
            bb = None
            for c in range(N + 1):
                for sq in range(N + 1 - c):
                    for gg in range(N + 1 - c - sq):
                        fr = N - c - sq - gg
                        m = milk[(c, hc)] + wool[(sq, hs)] + egg[gg] + straw[(fr, hst)]
                        if not a.no_cost:
                            # `reference:ANIMALS` -- COW $400, SHEEP $500, GOOSE $300. A one-off,
                            # but on a $20k margin eight of them are not a rounding error.
                            m -= c * COST["COW"] + sq * COST["SHEEP"] + gg * COST["GOOSE"]
                        if bb is None or m > bb[0]:
                            bb = (m, c, sq, gg, fr)
            return bb

        for hst in HIS_STRAW:
            print(f"########## {sps:.0f} strawberry units per freed pen slot, "
                  f"his strawberry at {hst:.0%} of the tape")
            print("   our best (cow/sheep/goose/free) against his herd\n")
            print(f"{'':>12}" + "".join(f"{'sheep ' + str(h):>14}" for h in HIS))
            for hc in HIS:
                row = f"{'his cows ' + str(hc):>12}"
                for hs in HIS:
                    m, c, sq, gg, fr = best_against(hc, hs, hst)
                    row += f"{f'{c}/{sq}/{gg}/{fr}':>14}"
                print(row, flush=True)
            print()
            print(f"{'':>12}" + "".join(f"{'sheep ' + str(h):>14}" for h in HIS)
                  + "     <- MARGIN, and gain over our current 4/4/0/6")
            for hc in HIS:
                row = f"{'his cows ' + str(hc):>12}"
                for hs in HIS:
                    m, c, sq, gg, fr = best_against(hc, hs, hst)
                    cur = milk[(4, hc)] + wool[(4, hs)] + egg[0] + straw[(max(0, N - 8), hst)]
                    if not a.no_cost:
                        cur -= 4 * COST["COW"] + 4 * COST["SHEEP"]
                    row += f"{f'{m:+,.0f}({m-cur:+,.0f})':>14}"
                print(row, flush=True)
            print()


if __name__ == "__main__":
    main()
