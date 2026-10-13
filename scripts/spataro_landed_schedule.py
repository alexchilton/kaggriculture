"""SpaTaro's schedule built from what LANDED, not from what he asked for.

`scripts/spataro_plan_rows.py` counted submitted orders, and on the `land` row that is wrong in
162 of 179 seasons: he submits BUY_LAND speculatively and most of them never fund. Episode
107068412 orders four parcels (d3, d6 x2, d10) and gains two -- its board is 25 tiles until d7.
A planner handed `land: 2` on day 6 builds routes onto ground it will never own, which is the
`add_land` failure in CLAUDE.md inverted: not an arm that buys land and never farms it, but a plan
that farms land it never buys.

So every field the planner treats as a COMMITMENT -- it reserves money, builds a route, or seats a
walk against it -- is derived here from the board CHANGING, turn to turn:

    land      len(farm["unlocked_quadrants"]) going up
    builds    a tile going from empty to {"kind": PASTURE|COOP} -- a count of TRANSITIONS
    pens      structures STANDING at the end of the day. This, not a cumulative sum of `builds`, is
              what the planner targets: a tile built, lost and rebuilt counts twice in `builds`
    places    a structure gaining an "animal", by species
    plants    a tile gaining a crop that is not WEED
    hires     farm["hires_today"], the engine's own per-day counter
    escapes   a structure LOSING its animal -- the cull's footprint, and the only herd exit
              (`DIG` cannot remove a placed animal; `reference/kaggriculture.py:817`)

`seeds` is the crop tally of `plants` -- the seed that goes IN THE GROUND, not the seed he asks
for. The old note here claimed an over-ask was "a no-op on both sides"; it is not. The engine drops
an unaffordable `BUY_SEED` silently and he moves on, while our planner holds the order in a market
slot ahead of the HIREs and the `BUY_ANIMAL` and re-offers it every turn until the day is gone.
Measured on 179 seasons, the over-ask is not spread evenly -- it sits on exactly the two dear
seeds, and the cheap ones are honest:

    STRAWBERRY  asks 37.76  plants 26.69  1.41x   ($100)
    MELON       asks 17.88  plants 11.03  1.62x   ($80)
    WHEAT       asks 173.79 plants 167.39 1.04x
    CARROT      asks 56.70  plants 55.12  1.03x

and worst early, where the bank is thinnest: d2 2.86x, d3 2.76x, d4 2.20x, d7 1.43x. On the d7
handover his row read `plants [STRAWBERRY, STRAWBERRY]` beside `seeds {STRAWBERRY: 6}` -- a $600
intent on a $33 dawn bank, which cost the COW, four of the seven hires, and 27 waterings.

Seed bought on day N for a plant on day N+1 needs no special case: that plant is in day N+1's
`plants`, so the buy simply moves a day later and the tile still lands on the same day.

`buys` and `sells` stay as REQUESTED. The planner clamps them with the same rule the engine does --
`n = min(have, row["sells"][prod])` at emission (`schedule_agent.py:5111`), and affordability on
the buys. `animals_bought` is set to what was PLACED, because an animal bought and never placed is
money spent on nothing and we do not want to copy it.
"""
import argparse, json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEASON, TPD = 30, 24
CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
PRODUCTS = CROPS + ("MILK", "WOOL", "EGG", "FERTILIZER")
ANIMALS = ("COW", "SHEEP", "GOOSE")
BUYABLE = ("WHEAT", "FERTILIZER")
STRUCTS = ("PASTURE", "COOP")
TEAM = "SpaTaro"


def _tiles(obs, seat):
    farms = obs.get("farms") or []
    return (farms[seat].get("tiles") or []) if len(farms) > seat else []


def landed_rows(steps, seat):
    rows = {d: dict(plants=[], places=[], builds=0, pens=0, land=0, hires=0, hands=0,
                    feeds=0, cares=0, waters=0, harvests=0,
                    seeds=Counter(), buys=Counter(), sells=Counter(),
                    animals_bought=Counter(), escapes=Counter(), money_dawn=None)
            for d in range(SEASON)}
    prev = None
    for i, s in enumerate(steps):
        obs = s[seat].get("observation") or {}
        farms = obs.get("farms") or []
        if len(farms) <= seat:
            continue
        farm = farms[seat]
        day = min(i // TPD, SEASON - 1)
        r = rows[day]
        if i % TPD == 0:
            r["money_dawn"] = farm.get("money")
        # `hires_today` is the engine's own per-day counter and resets at dawn, so the last value
        # seen in the day is the crew that actually landed -- not the HIRE orders submitted.
        r["hires"] = max(r["hires"], int(farm.get("hires_today") or 0))
        cur = _tiles(obs, seat)
        # **`pens` is what STANDS at the end of the day; `builds` is a count of TRANSITIONS.**
        # They are not the same number and the planner must target the first. A tile that is built,
        # lost -- dug, or taken by a weed -- and built again counts twice in `builds`, so the
        # cumulative sum of `builds` runs ahead of his board. Measured against his own replays:
        #
        #     ep 107673950 (ice cream)  d0 cum_builds 5 vs 4 standing ... d7 13 vs 11
        #     ep 107454405 (pizza)      exact to d6, then d7 15 vs 14, d8 16 vs 13
        #     ep 107028825 (bakery)     exact to d6, then d7 13 vs 12, d8 15 vs 14
        #     ep 107068412 (milk)       exact on every day
        #
        # which is why this never showed: the one season the work was done on is the one where the
        # two agree. `_refresh_pins` took `want_pens = sum(builds for d <= day)` and so built a pen
        # too many on five of the nine worlds -- `pens 13/12`, `14/12`, `12/11`, `15/14`, `16/14` --
        # and the extra pen takes ground a planting needed: ice cream is `pens 12/11` beside
        # `plant 0/2`.
        r["pens"] = max(int(r["pens"]), sum(
            1 for row_ in cur for c in row_
            if isinstance(c, dict) and (c.get("kind") in STRUCTS or "animal" in c)))
        quads = len(farm.get("unlocked_quadrants") or [])
        if prev is not None:
            pt, pq, pday = prev
            pr = rows[pday]                       # attribute the change to the day that caused it
            if quads > pq:
                pr["land"] += quads - pq
            for y, row in enumerate(cur):
                for x, t in enumerate(row):
                    o = pt[y][x] if y < len(pt) and x < len(pt[y]) else None
                    if t == "LOCKED" or o == "LOCKED":
                        continue
                    od = o if isinstance(o, dict) else None
                    td = t if isinstance(t, dict) else None
                    if td and td.get("kind") in STRUCTS and not (od and od.get("kind") in STRUCTS):
                        pr["builds"] += 1
                    if td and "animal" in td and not (od and "animal" in od):
                        pr["places"].append(td["animal"])
                        pr["animals_bought"][td["animal"]] += 1
                    if od and "animal" in od and not (td and "animal" in td):
                        pr["escapes"][od["animal"]] += 1
                    oc = (od or {}).get("crop")
                    tc = (td or {}).get("crop")
                    if tc and tc != "WEED" and tc != oc:
                        pr["plants"].append(tc)
        prev = (cur, quads, day)
        # Ops we can only read from the action, and which commit no money: FEED, CARE, WATER,
        # HARVEST.
        #
        # **WATER had no row at all, and it is the largest single gap on the gate.** Every other
        # quantity the day is judged on is stated -- `plants`, `feeds`, `cares`, `pens`, `places`,
        # `builds`, `buys`, `sells` -- so the planner has a target for each and the solver could be
        # given one. Water was whatever fell out of the routing, and it falls out short: d8 spataro
        # `water 21/41`, d10 bakery `21/53`. Nothing could match a number nobody stated.
        # Alex: "the values need to be properly passed so we know about watering numbers".
        #
        # Counted from the ACTION, exactly as `feeds` and `cares` are, because that is the side the
        # gate compares: `offered.water`. Reading it off the board instead would compare a fill
        # against an offer, which is the mistake `seeds` used to make in the other direction.
        a = s[seat].get("action") or {}
        for c in [a.get("farmer") or []] + list(a.get("hands") or []):
            if not c:
                continue
            if c[0] == "FEED":
                r["feeds"] += 1
            elif c[0] == "CARE":
                r["cares"] += 1
            elif c[0] == "WATER":
                r["waters"] += 1
            elif c[0] == "HARVEST":
                r["harvests"] += 1
        for o in (a.get("market") or []):
            if not o:
                continue
            q = o[2] if len(o) > 2 and isinstance(o[2], int) else 1
            if o[0] == "BUY_SEED" and o[1] in CROPS:
                pass                       # seeds come from `plants` below, not from the ask
            elif o[0] == "BUY_PRODUCT" and o[1] in BUYABLE:
                r["buys"][o[1]] += q
            elif o[0] == "SELL" and o[1] in PRODUCTS:
                r["sells"][o[1]] += q
    for r in rows.values():
        r["hands"] = r["hires"]
        r["seeds"] = Counter(r["plants"])
        for k in ("seeds", "buys", "sells", "animals_bought", "escapes"):
            r[k] = dict(r[k])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="+",
                    default=["data/replays_spa_sub", "data/replays_2026-09-07",
                             "data/replays_2026-09-08", "data/replays_2026-09-09"])
    ap.add_argument("--ids", default="/tmp/spa_new_ids.txt")
    ap.add_argument("--out", default="data/spataro_landed_rows.json")
    args = ap.parse_args()

    allow = None
    p = Path(args.ids)
    if p.exists():
        allow = {int(x) for x in p.read_text().split()}
        print(f"restricting to {len(allow)} episodes of one submission", flush=True)

    seasons, seen = [], set()
    for d in args.dirs:
        folder = ROOT / d
        if not folder.exists():
            continue
        for f in sorted(folder.glob("*.json")):
            if f.name.endswith("summary.json"):
                continue
            try:
                ep = int(f.stem)
            except ValueError:
                continue
            if ep in seen or (allow is not None and ep not in allow):
                continue
            r = json.loads(f.read_text())
            names = (r.get("info") or {}).get("TeamNames") or []
            if TEAM not in names:
                continue
            seen.add(ep)
            seat = names.index(TEAM)
            rows = landed_rows(r["steps"], seat)
            seasons.append({"ep": ep, "bank": r["rewards"][seat],
                            "seed": (r.get("info") or {}).get("seed"),
                            "opponent": names[1 - seat] if len(names) == 2 else None,
                            "rows": {str(k): v for k, v in rows.items()}})
            if len(seasons) % 25 == 0:
                print(f"  {len(seasons)} seasons", flush=True)

    print(f"\n{len(seasons)} seasons of submission 56114097", flush=True)
    out = ROOT / args.out
    out.write_text(json.dumps(seasons, separators=(",", ":")))
    print(f"wrote {out} ({out.stat().st_size:,} B)")

    tot_land = Counter()
    for s in seasons:
        tot_land[sum(s["rows"][str(d)]["land"] for d in range(SEASON))] += 1
    print(f"\nparcels gained per season: {dict(sorted(tot_land.items()))}")
    esc = Counter()
    for s in seasons:
        for d in range(SEASON):
            esc.update(s["rows"][str(d)]["escapes"])
    print(f"escapes across all seasons: {dict(esc)}")


if __name__ == "__main__":
    main()
