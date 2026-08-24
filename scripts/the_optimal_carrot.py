"""How many carrot tiles, converted from which day, actually maximises money on a real board.

Not a gate, not a diagnostic. The grid.

## What each arm changes, and what would have to be true for it to win

An arm sets two numbers: the first day the planner rewrites a scheduled `PLANT WHEAT` into
`PLANT CARROT`, and the total number of tiles it is allowed to convert across the window.

For a big arm to win, three things all have to hold: the converted tiles must RIPEN before the bell
(CARROT is `first_yield_day 2`, `max_yield_day 3`, so a tile sown on d27 is collectable on d29 and
competes with the closing walk); the units must reach the shed rather than stand in the field; and
the town's deficit must still be past the hinge knee after our own dump lands. It loses when the
carrot displaces wheat that would have sold for more, or when the dump walks our own close down --
which is exactly what the 2026-08-24 abstention arm measured, -$21,872 by holding 80 units to d29.

So the grid must be allowed to say "0 tiles" and "start late", and the answer is expected to be
board-dependent: 98495047 is drain 11 and closes at $517, while a drain-2 town closes near $50.

## Method

`does_the_book_reading_win_games.play` replays BOTH tapes verbatim to the handover, so the board,
the bank and the town's book are the real recorded ones, then our agent plays out. Prices are
endogenous -- the same seed paid $270 for milk in a recording and $1 in a rematch -- so a re-sim
from turn 0 would measure a different market and answer a different question.

The handover is d20, before the earliest arm starts, so no arm inherits another arm's board.

Reported per arm: our money minus theirs at the bell, and the carrot units held at d29 dawn, which
is the position the arm actually built.
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

US = "alex chilton"
DEEP = "98495047"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", default=DEEP)
    ap.add_argument("--handover", type=int, default=20)
    ap.add_argument("--starts", default="21,23,25,27")
    ap.add_argument("--tiles", default="0,8,16,24,32,40")
    ap.add_argument("--out", default="data/logs/optimal_carrot.csv")
    a = ap.parse_args()

    book = importlib.import_module("does_the_book_reading_win_games")
    SA = importlib.import_module("kagg.search.schedule_agent")
    CORNER = importlib.import_module("kagg.search.corner_the_book")

    starts = [int(x) for x in a.starts.split(",")]
    tiles = [int(x) for x in a.tiles.split(",")]

    out = REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("episode,seed,start_day,max_tiles,margin,carrot_at_d29\n")
    fh.flush()

    live_days, live_plan = SA.CARROT_SWAP_DAYS, CORNER.plan
    t0 = time.time()
    try:
        for ep in a.games.split(","):
            path = book._find(ep)
            if path is None:
                print(f"{ep}: not downloaded", flush=True)
                continue
            rec = json.loads(path.read_text())
            names = rec["info"]["TeamNames"]
            if US not in names:
                continue
            seat = names.index(US)
            seed = rec["info"]["seed"]
            rw = rec.get("rewards") or [0, 0]

            print(f"\n########## {ep}  seed {seed}  recorded margin "
                  f"{rw[seat] - rw[1 - seat]:+,.0f}", flush=True)
            print(f"{'tiles':>6} " + " ".join(f"{'d' + str(s):>16}" for s in starts), flush=True)

            grid = collections.defaultdict(dict)
            for n_tiles in tiles:
                cells = []
                for start in starts:
                    SA.CARROT_SWAP_DAYS = tuple(range(start, 28))
                    # The arm IS the tile count, so the book-reading gate is replaced by it. Left
                    # in place it would size the position itself and no arm would differ.
                    CORNER.plan = (lambda *_a, n=n_tiles, **_k:
                                   (n, f"arm: {n} tiles from d{start}"))
                    try:
                        r = book.play(path, seat, seed, a.handover, use_old_gate=False)
                        m = r["ours"] - r["theirs"]
                        c = r["carrot_at_close"]
                    except Exception as e:                                   # noqa: BLE001
                        print(f"  {n_tiles}@d{start}: {e!r}", flush=True)
                        continue
                    grid[n_tiles][start] = (m, c)
                    cells.append(f"{m:>+11,.0f}/{c:>3}")
                    fh.write(f"{ep},{seed},{start},{n_tiles},{round(m)},{c}\n")
                    fh.flush()
                print(f"{n_tiles:>6} " + " ".join(f"{c:>16}" for c in cells), flush=True)

            best = max(((m, n, s) for n, row in grid.items() for s, (m, _c) in row.items()),
                       default=None)
            if best:
                print(f"  BEST: {best[1]} tiles from d{best[2]}  ->  {best[0]:+,.0f}", flush=True)
                base = grid.get(0, {})
                if base:
                    z = max(m for m, _c in base.values())
                    print(f"  vs 0 tiles ({z:+,.0f}):  {best[0] - z:+,.0f}", flush=True)
    finally:
        SA.CARROT_SWAP_DAYS, CORNER.plan = live_days, live_plan
        fh.close()
    print(f"\n({time.time() - t0:.0f}s)  rows -> {out}", flush=True)


if __name__ == "__main__":
    main()
