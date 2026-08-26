"""A named player's herd, counted THREE independent ways, on games that genuinely contain them.

Alex's point: the herd is visible from the buys and from the placings, not only from the board. Three
counts that must agree is the discipline this repo runs on -- when they disagree, the metric is
misread rather than reality being surprising.

    placed  -- `["PLACE", species, n]` in the farmer/hands streams. Unit ops, NOT market orders, so
               they are not re-posted each turn and can be counted directly.
    alive   -- `tile["animal"]` on the final board. A farm has NO `animals` key; its keys are
               farmer, hands, hires_today, money, tiles, unlocked_quadrants. Counting a
               `farm["animals"]` field returns None everywhere and reported 0 seats at 6/6 out of
               3,224 on 2026-08-25. That zero was a bug, not a finding.
    ordered -- `["BUY_ANIMAL", species, qty]` in the market stream. **These are OFFERS, not fills.**
               An agent re-posts a standing quota every turn, so this column OVERCOUNTS and is here
               only as an upper bound. Never quote it as a head count
               (`feedback_offers_are_not_fills`).

The name is matched EXPLICITLY against `info.TeamNames`. `replay_fills.seat_of` returns 0 when the
name is absent (`kagg/analysis/replay_fills.py:79-86`), which silently reads seat 0 of every
unmatched game; that produced a withdrawn "1291 kawa seats" table on 2026-08-25.

    python -u scripts/herd_three_ways.py --team カワシギ
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

SCAN_DIRS = ("downloads_2026-08-13", "downloads_2026-08-14to16", "downloads_2026-08-19",
             "downloads_2026-08-20", "downloads_2026-08-21", "top_guys", "leaders_2026-08-24",
             "leaders_2026-08-19", "field_leaders", "kawa_2026-08-24", "tetsuya", "ryo",
             "tetsuya_93866112", "victor", "kawashigi", "new_leader", "top2")

SPECIES = ("COW", "SHEEP")

#: The 2026-08-15 balance change put CARROT, TOMATO and EGG on a `hinge` price curve. Anything
#: recorded before it describes a DIFFERENT GAME (see CLAUDE.md), so the rows are split on it.
BALANCE_CHANGE_DIRS = ("downloads_2026-08-13", "downloads_2026-08-14to16", "top_guys", "top2",
                       "kawashigi", "victor")


def _counts(replay, seat):
    """`(placed, alive, ordered, tiles_owned, crops, money, sown)` for `seat`."""
    placed, ordered, sown = collections.Counter(), collections.Counter(), collections.Counter()
    for step in replay.get("steps") or []:
        if seat >= len(step):
            continue
        act = (step[seat] or {}).get("action") or {}
        streams = [act.get("farmer")] + list(act.get("hands") or [])
        for op in streams:
            if not op or len(op) < 2:
                continue
            if op[0] == "PLACE" and op[1] in SPECIES:
                placed[op[1]] += 1
            # A PLANT is emitted ONCE, unlike a market order the agent re-posts every turn, so the
            # sown counts are exact. This is how `decision_points.py` classified his 51 games into
            # MELON 20 / STRAW 34 (41 games) and MELON 12 / STRAW 42 (9 games) -- two distinct tapes.
            elif op[0] == "PLANT" and op[1]:
                sown[op[1]] += 1
        for op in (act.get("market") or []):
            if op and len(op) >= 3 and op[0] == "BUY_ANIMAL" and op[1] in SPECIES:
                ordered[op[1]] += int(op[2] or 0)

    obs = {}
    for step in reversed(replay.get("steps") or []):
        cand = (step[0] or {}).get("observation") or {}
        if cand.get("farms"):
            obs = cand
            break
    farms = obs.get("farms") or []
    if seat >= len(farms):
        return placed, collections.Counter(), ordered, 0, collections.Counter(), 0.0, sown
    farm = farms[seat]
    alive, owned, crops = collections.Counter(), 0, collections.Counter()
    for row in (farm.get("tiles") or []):
        for t in row:
            if t == "LOCKED":
                continue
            owned += 1
            if isinstance(t, dict):
                if t.get("animal"):
                    alive[t["animal"]] += 1
                if t.get("crop"):
                    crops[t["crop"]] += 1
    return placed, alive, ordered, owned, crops, float(farm.get("money", 0.0)), sown


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", default="カワシギ")
    ap.add_argument("--rows", type=int, default=25)
    args = ap.parse_args()

    files = []
    for d in SCAN_DIRS:
        p = REPO / "data/seed_scripts" / d
        if p.exists():
            files.extend((d, f) for f in sorted(p.glob("*.json")))

    seen, matched, rows = 0, 0, []
    for d, f in files:
        try:
            r = json.loads(f.read_text())
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(r, dict):
            continue
        names = (r.get("info") or {}).get("TeamNames") or []
        seen += 1
        if args.team not in names:
            continue
        seat = names.index(args.team)
        matched += 1
        placed, alive, ordered, owned, crops, money, sown = _counts(r, seat)
        rows.append({"dir": d, "game": f.stem, "seat": seat, "placed": placed, "alive": alive,
                     "ordered": ordered, "owned": owned, "crops": crops, "money": money, "sown": sown,
                     "post": d not in BALANCE_CHANGE_DIRS})

    print(f"team {args.team!r}   games scanned {seen}   games CONTAINING this team {matched}")
    if not rows:
        print("no games contain that team -- nothing to report")
        return

    disagree = sum(1 for r in rows
                   if (r["placed"]["COW"], r["placed"]["SHEEP"])
                   != (r["alive"]["COW"], r["alive"]["SHEEP"]))
    print(f"placed vs alive disagree on {disagree} of {len(rows)} seats "
          f"(deaths and unplaced stock both do this)")
    print()

    for label, want_post in (("POST balance change (2026-08-15+)", True),
                             ("PRE balance change -- a different game", False)):
        sub = [r for r in rows if r["post"] == want_post]
        if not sub:
            continue
        dist = collections.Counter((r["alive"]["COW"], r["alive"]["SHEEP"]) for r in sub)
        print(f"{label}: {len(sub)} seats")
        print(f"  {'COW/SHEEP':<12}{'seats':>7}{'total':>7}   share")
        for (c, s), n in dist.most_common(12):
            print(f"  {str(c) + '/' + str(s):<12}{n:>7}{c + s:>7}   {100.0 * n / len(sub):>5.1f}%")
        print(f"  seats at 6/6: {dist.get((6, 6), 0)}")
        print()

    # **Is 6/6 a different TAPE, or the same tape with a different herd?** `decision_points.py`
    # classified his games by PLANT emissions into MELON 20 / STRAW 34 and MELON 12 / STRAW 42.
    # If the herd split rides that classification, the herd is not a separate decision at all.
    post = [r for r in rows if r["post"]]
    print("HERD vs TAPE CLASS (post-change), by crops SOWN -- a PLANT is emitted once, so exact:")
    print(f"  {'COW/SHEEP':<10}{'seats':>6}  {'MELON sown':>12} {'STRAW sown':>11} "
          f"{'WHEAT sown':>11}  {'bank':>9}")
    by_herd = collections.defaultdict(list)
    for r in post:
        by_herd[(r["alive"]["COW"], r["alive"]["SHEEP"])].append(r)
    for herd, sub in sorted(by_herd.items(), key=lambda kv: -len(kv[1]))[:8]:
        n = len(sub)
        me = sum(r["sown"]["MELON"] for r in sub) / n
        st = sum(r["sown"]["STRAWBERRY"] for r in sub) / n
        wh = sum(r["sown"]["WHEAT"] for r in sub) / n
        bk = sum(r["money"] for r in sub) / n
        print(f"  {str(herd[0]) + '/' + str(herd[1]):<10}{n:>6}  {me:>12.1f} {st:>11.1f} "
              f"{wh:>11.1f}  {bk:>9,.0f}")
    print()

    src = post or rows
    print(f"TOP {args.rows} SEATS BY BANK ({'post-change' if post else 'all'}):")
    print(f"  {'bank':>9} {'C/S alive':>9} {'C/S placed':>10} {'ord':>7} {'tiles':>5}  "
          f"{'game':<12} crops")
    for r in sorted(src, key=lambda r: -r["money"])[:args.rows]:
        a = f"{r['alive']['COW']}/{r['alive']['SHEEP']}"
        p = f"{r['placed']['COW']}/{r['placed']['SHEEP']}"
        o = f"{r['ordered']['COW']}/{r['ordered']['SHEEP']}"
        mix = " ".join(f"{k}:{v}" for k, v in r["crops"].most_common(4)) or "-"
        print(f"  {r['money']:>9,.0f} {a:>9} {p:>10} {o:>7} {r['owned']:>5}  {r['game']:<12} {mix}")


if __name__ == "__main__":
    main()
