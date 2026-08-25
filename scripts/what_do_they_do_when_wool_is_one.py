"""In the towns where WOOL and MILK hit $1, what does the OPPONENT do that we do not?

`do_we_lose_the_glutted_towns.py` established that deep-glut towns are where we lose: 10 games with
200+ turns at the $1 floor win 30% with a mean margin of -$575, against 49% and +$11,869 elsewhere.

Alex: *"well the question is what do we do different to kawa on the milk = wool = 1 towns??"*

Everything needed is public in a replay, for BOTH seats, on every turn:

    farms[i]["tiles"]              the herd -- every PASTURE/animal structure, so supply is visible
    market["inventory"]            the shared book, so the price is exact
    steps[t][i]["action"]          what each side actually ordered

So this compares, restricted to the turns AFTER a product first hits a floored price:

    animals held      are they still carrying the herd that floods it?
    units offered     do they keep dumping into a $1 book, or stop?
    when they sold    did they clear their stock BEFORE the floor arrived?

The prior worth testing first, because it is already recorded in this project's memory:
`WOOL_SHOP_SETS_THE_HERD` sizes the flock from a COUNT and never reads the book, and ladder game
99114898 has 12 sheep taking WOOL from $239 to $11 on 57 units over I0. If we hold more wool
producers than the opponent in exactly the towns where wool is worthless, that is the difference and
it is a production decision, not a sell rule.

**Offers are not fills.** Order quantities are read as OFFERS and labelled as such -- an agent
re-posts its quota every turn, so these counts are an upper bound on intent, never on trade. The
herd counts and the book are exact.

    python -u scripts/what_do_they_do_when_wool_is_one.py
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
US = "alex chilton"
WATCH = ("WOOL", "MILK")


def herd(farm, KG):
    """Animal structures on a farm, by kind. Exact -- read off the tiles, not inferred."""
    c = collections.Counter()
    for row in (farm.get("tiles") or []):
        for cell in row:
            if not isinstance(cell, dict):
                continue
            kind = cell.get("kind")
            if kind and kind not in ("PLANT", "WEED"):
                c[str(kind)] += 1
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", default="~/Downloads,data/seed_scripts/ladder_2026-08-16b,"
                                      "data/seed_scripts/top_guys")
    ap.add_argument("--limit", type=int, default=120)
    ap.add_argument("--floor-turns", type=int, default=120,
                    help="turns at <=25% of base before a game counts as glutted")
    a = ap.parse_args()

    import kaggle_environments.envs.kaggriculture.kaggriculture as KG

    paths = []
    for d in a.dirs.split(","):
        root = pathlib.Path(d.strip()).expanduser()
        if not root.is_absolute():
            root = REPO / root
        paths += sorted(glob.glob(str(root / "*.json")))

    games = []
    seen = set()
    for p in paths[:a.limit]:
        try:
            raw = json.loads(pathlib.Path(p).read_text())
        except Exception:
            continue
        steps = raw.get("steps") if isinstance(raw, dict) else None
        if not steps or len(steps) < 600:
            continue
        info = raw.get("info") or {}
        names = info.get("TeamNames") or []
        if US not in names:
            continue
        ep = str(info.get("EpisodeId") or pathlib.Path(p).stem)
        if ep in seen:
            continue
        seen.add(ep)
        games.append((ep, names.index(US), steps))

    print(f"{len(games)} games with our seat, floor threshold {a.floor_turns} turns\n", flush=True)

    agg = {"deep": collections.defaultdict(float), "ok": collections.defaultdict(float)}
    counts = collections.Counter()
    detail = []

    for ep, seat, steps in games:
        them = 1 - seat
        base = {p: KG.MARKET_PARAMS[p]["base"] for p in WATCH}
        cheap_turns = collections.Counter()
        first_cheap = {}
        for t, st in enumerate(steps):
            inv = ((st[0].get("observation") or {}).get("market") or {}).get("inventory")
            if not inv:
                continue
            for p in WATCH:
                if p not in inv:
                    continue
                if KG.market_price(p, int(inv[p])) <= 0.25 * base[p]:
                    cheap_turns[p] += 1
                    first_cheap.setdefault(p, t)

        glutted = sum(cheap_turns.values()) >= a.floor_turns
        bucket = "deep" if glutted else "ok"
        counts[bucket] += 1

        # Herd at the moment the book first went cheap, and at the end.
        t0 = min(first_cheap.values()) if first_cheap else len(steps) - 1
        obs0 = (steps[t0][0].get("observation") or {}).get("farms") or []
        our_h = herd(obs0[seat], KG) if len(obs0) > seat else collections.Counter()
        their_h = herd(obs0[them], KG) if len(obs0) > them else collections.Counter()

        # Units OFFERED into a floored book, after it went cheap. Offers, not fills.
        our_after = their_after = 0
        for t in range(t0, len(steps)):
            for who, sink in ((seat, "our"), (them, "their")):
                act = steps[t][who].get("action") if t < len(steps) else None
                if not isinstance(act, dict):
                    continue
                for o in (act.get("market") or []):
                    if (isinstance(o, (list, tuple)) and len(o) > 2
                            and str(o[0]).upper() == "SELL" and o[1] in WATCH):
                        if sink == "our":
                            our_after += int(o[2])
                        else:
                            their_after += int(o[2])

        last = (steps[-1][0].get("observation") or {}).get("farms") or []
        ours = float(last[seat].get("money", 0)) if len(last) > seat else 0.0
        theirs = float(last[them].get("money", 0)) if len(last) > them else 0.0

        our_animals = sum(v for k, v in our_h.items())
        their_animals = sum(v for k, v in their_h.items())
        agg[bucket]["n"] += 1
        agg[bucket]["our_animals"] += our_animals
        agg[bucket]["their_animals"] += their_animals
        agg[bucket]["our_after"] += our_after
        agg[bucket]["their_after"] += their_after
        agg[bucket]["win"] += 1 if ours > theirs else 0
        agg[bucket]["margin"] += ours - theirs

        if glutted:
            detail.append((ep, ours - theirs, our_animals, their_animals,
                           our_after, their_after, dict(our_h), dict(their_h)))

    print("=== the glutted games, one row each ===")
    print(f"{'episode':>10}{'margin':>11}{'our animals':>13}{'their':>7}"
          f"{'our offers after':>18}{'theirs':>9}")
    for ep, marg, oa, ta, oaf, taf, oh, th in sorted(detail, key=lambda r: r[1]):
        print(f"{ep:>10}{marg:>+11,.0f}{oa:>13}{ta:>7}{oaf:>18,}{taf:>9,}")
        print(f"{'':>10}  ours {oh}   theirs {th}")

    print(f"\n{'':<26}{'deep glut':>12}{'healthy':>12}")
    for label, key in (("games", "n"), ("win rate", None), ("mean margin", "margin"),
                       ("our animals at floor", "our_animals"),
                       ("their animals at floor", "their_animals"),
                       ("our units offered after", "our_after"),
                       ("their units offered after", "their_after")):
        row = f"{label:<26}"
        for bucket in ("deep", "ok"):
            n = agg[bucket]["n"] or 1
            if key is None:
                row += f"{agg[bucket]['win'] / n:>12.0%}"
            elif key == "n":
                row += f"{agg[bucket]['n']:>12.0f}"
            else:
                row += f"{agg[bucket][key] / n:>12,.0f}"
        print(row)

    print("\nIf we hold MORE animals than the opponent in exactly the towns where wool and milk")
    print("are worthless, the difference is the herd rule, not the sell rule -- and")
    print("`WOOL_SHOP_SETS_THE_HERD` sizes the flock from a count without reading the book.")


if __name__ == "__main__":
    main()
