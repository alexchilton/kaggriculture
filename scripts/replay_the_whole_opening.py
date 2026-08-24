"""Does replaying his tape from d0 beat playing our own first four days?

Alex, 2026-08-24: *"and if we do d0-d11 with his tapes?"*

The shipped agent replays `REPLAY_OPENING_DAYS = (4..11)` and plays d0-d3 from its own planner.
That is why our very first action differs from his: at d0 h0 he does `BUILD_PASTURE` and buys 6
WHEAT as feed, we `PASS` and buy none. The boards converge by d4 and drift apart again from d5.

## The arm, and what would have to be true for it to win

    control    REPLAY_OPENING_DAYS = (4..11)     -- what ships
    treatment  REPLAY_OPENING_DAYS = (0..11)     -- his tape from turn 0

For the treatment to win, his recorded d0-d3 unit work has to be better than what our planner
derives on these boards. It is NOT a full clone even so: the replay deliberately takes only the
**unit actions and the SELL cadence** from the tape and keeps every purchase ours, because the
melon/strawberry arm and the COW/SHEEP split are decided around d3-d6 and expressed as purchases --
handing those to the tape discarded both arms when it was tried (`melon 15/8`, `strawb 24/34` at
d12, the strawberry season never installed).

So this arm gives us his `BUILD_PASTURE` and his routing, not his `BUY_PRODUCT WHEAT 6`.

It could easily LOSE: his d0-d3 unit actions were recorded against a bank his own purchases
produced. Ours differ from turn 0, so a recorded PICKUP may reach for an animal we have not bought
yet, and a recorded move may walk to a pen that does not exist. A replayed op that cannot apply
does nothing and the turn is wasted.

Both arms: our agent in HIS seat, on the game's own seed, against that game's recorded opponent
tape. `tape` is his own actions verbatim, for reference.
"""

import argparse
import glob
import importlib
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import us_in_his_seat as U                                                  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", default="カワシギ")
    ap.add_argument("--limit", type=int, default=14)
    ap.add_argument("--out", default="data/logs/replay_whole_opening.csv")
    a = ap.parse_args()

    SA = importlib.import_module("kagg.search.schedule_agent")
    shipped = SA.REPLAY_OPENING_DAYS

    files = {}
    for d in sorted(pathlib.Path(REPO / "data/seed_scripts").iterdir()):
        if d.is_dir():
            for f in glob.glob(str(d / "*.json")):
                files.setdefault(pathlib.Path(f).stem, f)

    out = REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("episode,seed,opponent,tape,d4_d11,d0_d11,delta\n")
    fh.flush()

    print(f"shipped REPLAY_OPENING_DAYS = {shipped}")
    print("control = replay d4-d11 (what ships).  treatment = replay d0-d11.")
    print("our agent in his seat, game's own seed, his recorded opponent.\n", flush=True)
    print(f"{'episode':>10} {'tape':>10} {'d4-d11':>10} {'d0-d11':>10} {'delta':>10}  opponent",
          flush=True)

    t0 = time.time()
    rows = []
    try:
        for ep, f in sorted(files.items()):
            if len(rows) >= a.limit:
                break
            try:
                rec = json.loads(pathlib.Path(f).read_text())
            except Exception:                                                # noqa: BLE001
                continue
            if not isinstance(rec, dict) or "steps" not in rec or "info" not in rec:
                continue
            names = (rec.get("info") or {}).get("TeamNames") or []
            if a.who not in names:
                continue
            seed = (rec.get("info") or {}).get("seed")
            if seed in (None, 0):
                continue
            seat = names.index(a.who)

            try:
                th, to, _ = U.play(rec, seat, seed, use_agent=False)
                SA.REPLAY_OPENING_DAYS = shipped
                ch, co, _ = U.play(rec, seat, seed, use_agent=True)
                SA.REPLAY_OPENING_DAYS = tuple(range(0, 12))
                wh, wo, _ = U.play(rec, seat, seed, use_agent=True)
            except Exception as e:                                           # noqa: BLE001
                print(f"{ep:>10}  {e!r}", flush=True)
                continue
            finally:
                SA.REPLAY_OPENING_DAYS = shipped

            tm, cm, wm = th - to, ch - co, wh - wo
            rows.append((wm - cm, ep, tm, cm, wm, names[1 - seat]))
            print(f"{ep:>10} {tm:>+10,.0f} {cm:>+10,.0f} {wm:>+10,.0f} {wm - cm:>+10,.0f}  "
                  f"{names[1 - seat][:20]}", flush=True)
            fh.write(",".join(str(x) for x in [ep, seed, names[1 - seat], round(tm),
                                               round(cm), round(wm), round(wm - cm)]) + "\n")
            fh.flush()
    finally:
        SA.REPLAY_OPENING_DAYS = shipped
        fh.close()

    if rows:
        d = sorted(r[0] for r in rows)
        n = len(d)
        print(f"\nn={n}   mean {sum(d) / n:>+,.0f}   median {d[n // 2]:>+,.0f}   "
              f"better in {sum(1 for x in d if x > 0)}/{n}")
        cw = sum(1 for r in rows if r[3] > 0)
        ww = sum(1 for r in rows if r[4] > 0)
        print(f"wins: d4-d11 {cw}/{n}   d0-d11 {ww}/{n}")
    print(f"\n({time.time() - t0:.0f}s)  rows -> {out}")


if __name__ == "__main__":
    main()
