"""The carrot grid on EVERY game in a drain band, not just the handful where we were a seat.

Alex, 2026-08-24, on a 7-game drain 7-8 result: *"nonsense, measure more games more opponents etc."*

He is right, and the sample was small for an artificial reason. `the_optimal_carrot.py` picked the
seat by `names.index("alex chilton")`, so it could only use games we had played -- 7 of the 138 rows
the corpus holds at drain 7-8. Our agent does not need to have played a game to be dropped into a
seat in it: both tapes are replayed verbatim to the handover, then ONE seat is handed to our agent
and the other keeps playing its recording. That works for any seat in any game.

So this selects games by the town's CARROT drain and plays our agent in whichever seat is asked
for, against the other seat's real recorded tape. Same harness, ~20x the sample, and a different
opponent in almost every game.

## What an arm changes and what would have to be true for it to win

An arm converts up to `--tiles` scheduled `PLANT WHEAT` into `PLANT CARROT`, starting `--start`.
For it to pay, the tiles must ripen before the bell, reach the shed, and the town's deficit must
still be past the hinge knee after our own dump lands. Measured already: it pays hugely at drain 11
(+$23,105 on one board) and loses $10k-$20k at drain 2-6, monotone in tile count. The 7-9 band is
what is unmeasured, and it is the band a shipped threshold has to be drawn through.

## Reading it

`0 tiles` is the baseline for that game and seat; ONLY the paired difference from it is meaningful.
Absolute levels carry the cost of handing a cold agent the farm at the handover, which the subagent
measured at up to $12,901 in either direction.
"""

import argparse
import collections
import glob
import importlib
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "reference"))

TPD = 24


def carrot_drain(obs, shops):
    d = 0
    for name in ((obs.get("town") or {}).get("unlocked_shops") or []):
        ps = shops.get(name) or []
        if "CARROT" in ps:
            d += 2 if len(ps) == 1 else 1
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-drain", type=int, default=7)
    ap.add_argument("--max-drain", type=int, default=9)
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--handover", type=int, default=20)
    ap.add_argument("--start", type=int, default=21)
    ap.add_argument("--tiles", default="0,16,56")
    ap.add_argument("--out", default="data/logs/carrot_at_scale.csv")
    ap.add_argument("--scan", default="data/logs/full_corpus_drain_scan.csv")
    a = ap.parse_args()

    import kaggriculture as KG
    book = importlib.import_module("does_the_book_reading_win_games")
    SA = importlib.import_module("kagg.search.schedule_agent")
    CORNER = importlib.import_module("kagg.search.corner_the_book")
    tiles = [int(x) for x in a.tiles.split(",")]

    # Selection comes from the corpus scan that already read every file
    # (`data/logs/full_corpus_drain_scan.csv`, 2,164 replays). Re-parsing 30 MB replays just to
    # read one integer off each took longer than the measurement it was feeding.
    import csv
    scan = REPO / a.scan
    wanted = {}
    for r in csv.DictReader(scan.open()):
        dr = r.get("drain", "")
        if not dr.isdigit() or not (a.min_drain <= int(dr) <= a.max_drain):
            continue
        # `seed 0` is a self-play mirror fixture, not a ladder game; both seats are ours.
        if str(r.get("seed")) in ("0", "None", ""):
            continue
        wanted.setdefault(r["episode"], (r["file"], int(dr), int(r["seed"])))

    by_ep = {}
    for d in sorted(pathlib.Path(REPO / "data/seed_scripts").iterdir()):
        if d.is_dir():
            for f in glob.glob(str(d / "*.json")):
                by_ep.setdefault(pathlib.Path(f).stem, f)

    picked = []
    for ep, (_fn, dr, seed) in sorted(wanted.items()):
        if len(picked) >= a.limit:
            break
        f = by_ep.get(ep)
        if f is None:
            continue
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                    # noqa: BLE001
            continue
        if not isinstance(rec, dict) or "steps" not in rec or "info" not in rec:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or ["?", "?"]
        rw = rec.get("rewards") or [0, 0]
        # Play the WINNER's seat: the arm has to beat a seat that was already doing well, which is
        # the honest test. Handing our agent the loser's seat flatters every arm.
        seat = 0 if rw[0] >= rw[1] else 1
        picked.append((pathlib.Path(f), rec, seed, seat, dr, names, rw))
        print(f"  picked {ep} drain {dr} seat {seat} "
              f"({names[seat][:18]} vs {names[1 - seat][:18]})", flush=True)

    out = REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("episode,seed,drain,seat,opponent," + ",".join(f"t{t}" for t in tiles) + "\n")
    fh.flush()

    print(f"\n{len(picked)} games, drain {a.min_drain}-{a.max_drain}, "
          f"our agent in the WINNER's seat, handover d{a.handover}, convert from d{a.start}.\n",
          flush=True)
    print(f"{'episode':>10} {'drain':>5} " + " ".join(f"{'t' + str(t):>10}" for t in tiles)
          + "   opponent", flush=True)

    live_days, live_plan = SA.CARROT_SWAP_DAYS, CORNER.plan
    agg = collections.defaultdict(list)
    t0 = time.time()
    try:
        for path, rec, seed, seat, dr, names, _rw in picked:
            got = {}
            for n in tiles:
                SA.CARROT_SWAP_DAYS = tuple(range(a.start, 28))
                CORNER.plan = lambda *_a, _n=n, **_k: (_n, f"arm {_n}")
                try:
                    r = book.play(path, seat, seed, a.handover, use_old_gate=False)
                    got[n] = r["ours"] - r["theirs"]
                except Exception as e:                                       # noqa: BLE001
                    print(f"  {path.stem} t{n}: {e!r}", flush=True)
                    got[n] = None
            if any(v is None for v in got.values()):
                continue
            base = got[tiles[0]]
            for n in tiles:
                agg[(dr, n)].append(got[n] - base)
            print(f"{path.stem:>10} {dr:>5} "
                  + " ".join(f"{got[n]:>+10,.0f}" for n in tiles)
                  + f"   {names[1 - seat][:20]}", flush=True)
            fh.write(",".join(str(x) for x in [path.stem, seed, dr, seat, names[1 - seat]]
                              + [round(got[n]) for n in tiles]) + "\n")
            fh.flush()
    finally:
        SA.CARROT_SWAP_DAYS, CORNER.plan = live_days, live_plan
        fh.close()

    print(f"\nDELTA vs {tiles[0]} tiles, by drain -- mean, median, and how often it HELPS\n")
    print(f"{'drain':>5} {'tiles':>6} {'n':>4} {'mean':>10} {'median':>10} {'better':>8}")
    for (dr, n) in sorted(agg):
        v = sorted(agg[(dr, n)])
        if n == tiles[0]:
            continue
        better = sum(1 for x in v if x > 0)
        print(f"{dr:>5} {n:>6} {len(v):>4} {sum(v) / len(v):>+10,.0f} "
              f"{v[len(v) // 2]:>+10,.0f} {better:>4}/{len(v):<4}")
    print(f"\n({time.time() - t0:.0f}s)  rows -> {out}")


if __name__ == "__main__":
    main()
