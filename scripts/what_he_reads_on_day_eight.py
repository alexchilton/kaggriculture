"""What does his d8 seed order key on?

Alex, 2026-08-24. Two of his own games, both against `researchstudio.site`, differ at d8 by one
market order and nothing else:

    92466371 d8   SELL FERTILIZER 6, HIRE x5, BUY_PRODUCT WHEAT 9, BUY_SEED STRAWBERRY 1
    92441493 d8   SELL FERTILIZER 6, HIRE x5, BUY_PRODUCT WHEAT 9, BUY_SEED WHEAT 3

92466371 IS the melon tape, so we replay `STRAWBERRY 1` into a game whose own play was `WHEAT 3`.
That is $69 spent one hour before a $131 hire block, and hires 6-10 then come up two dollars short:
he ends d8 with 11 hands, we end with 10, and the board first differs at d8 in eight games.

We already replay the tape's market verbatim (`schedule_agent.py:5635`), so there is nothing to
correct in the replay. The tape is simply the wrong day. To key a third tape on this, we first have
to know what HE is reading -- so this reads his RECORDED observation at d8 for every game and puts
the candidate discriminators next to the order he actually sent.

Reads JSON only. No simulation.
"""

import argparse
import collections
import csv
import glob
import json
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
DIRS = ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c", "kawa_2026-08-24",
        "leaders_2026-08-24", "losses", "top_guys", "top2", "ladder", "our_games", "new_leader")
TPD = 24


def _first_market(steps, seat, day, hours=6):
    """His first non-empty market order of the day, and the hour it landed on."""
    for h in range(hours):
        t = day * TPD + h
        if t >= len(steps):
            break
        a = steps[t][seat].get("action") or {}
        mk = [list(o) for o in (a.get("market") or []) if o]
        if mk:
            return h, mk
    return None, []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", default="カワシギ")
    ap.add_argument("--day", type=int, default=8)
    ap.add_argument("--out", default="data/logs/what_he_reads_on_day_eight.csv")
    a = ap.parse_args()

    files = {}
    for d in DIRS:
        for f in glob.glob(str(REPO / f"data/seed_scripts/{d}/*.json")):
            files.setdefault(pathlib.Path(f).stem, f)

    rows = []
    for ep, f in sorted(files.items()):
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                     # noqa: BLE001
            continue
        if not isinstance(rec, dict) or "steps" not in rec:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        if a.who not in names:
            continue
        seat = names.index(a.who)
        steps = rec["steps"]
        t0 = a.day * TPD
        if t0 >= len(steps):
            continue
        obs = steps[t0][seat]["observation"]
        priv = obs.get("private") or {}
        farm = obs["farms"][seat]
        shed = collections.Counter(priv.get("shed") or {})
        seeds = collections.Counter(priv.get("seeds") or {})
        town = obs.get("town") or {}
        shops = tuple(sorted(town.get("unlocked_shops") or []))

        crops = collections.Counter()
        owned = 0
        for row in farm.get("tiles") or []:
            for t in row:
                if t == "LOCKED" or t is None:
                    owned += t is None
                    continue
                owned += 1
                if isinstance(t, dict) and t.get("crop"):
                    crops[t["crop"]] += 1

        hour, mk = _first_market(steps, seat, a.day)
        seed_order = {o[1]: int(o[2]) for o in mk if o[0] == "BUY_SEED" and len(o) >= 3}
        rows.append(dict(
            episode=ep, seed=(rec.get("info") or {}).get("seed"),
            opponent=names[1 - seat], hour=hour,
            seed_order=json.dumps(seed_order),
            bank=farm["money"],
            seeds_STRAWBERRY=seeds["STRAWBERRY"], seeds_WHEAT=seeds["WHEAT"],
            seeds_MELON=seeds["MELON"],
            shed_FERTILIZER=shed["FERTILIZER"], shed_WHEAT=shed["WHEAT"],
            tiles_STRAWBERRY=crops["STRAWBERRY"], tiles_WHEAT=crops["WHEAT"],
            tiles_MELON=crops["MELON"], owned=owned,
            n_shops=len(shops), shops=",".join(shops)))

    out = REPO / a.out
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    print(f"his d{a.day} seed order, grouped\n")
    g = collections.defaultdict(list)
    for r in rows:
        g[r["seed_order"]].append(r)
    for order, rs in sorted(g.items(), key=lambda kv: -len(kv[1])):
        print(f"  {order}   n={len(rs)}")
        for k in ("seeds_STRAWBERRY", "seeds_WHEAT", "seeds_MELON", "shed_FERTILIZER",
                  "tiles_STRAWBERRY", "tiles_WHEAT", "tiles_MELON", "owned", "n_shops", "bank"):
            vals = sorted({r[k] for r in rs})
            print(f"      {k:<20} {vals if len(vals) <= 8 else str(vals[:8]) + ' ...'}")
        print(f"      episodes            {[r['episode'] for r in rs]}")
        print()
    print(f"rows -> {a.out}")


if __name__ == "__main__":
    main()
