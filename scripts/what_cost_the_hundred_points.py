"""Which of the three `e2500_close` changes cost 101 rating points?

`e2500_shopprice` sits at 1808.6 on the ladder. `e2500_close` sits at 1707.2. It bundled three
changes, so the loss was never attributable. This splits them, paired, on the six real boards.

The window is the point. Handing the wheel to our own agent at d27 -- three days -- costs a mean
**-$7,329** against our own recorded ladder play continuing on the same board
(`data/logs/bias_vs_handover.log`). Five of those six games were lost by $614 to $6,070. So whatever
is wrong in the last three days is larger than every margin it needs to close.

## The arms

    tape        both tapes replayed to the bell; our agent never called. The zero.
    ship        the code as it stands.
    flat_price  `product_price` forced to None, so `crop_ops` and `animal_ops` fall back to
                `BASE_PRICE`. Reverts change (a): ranking the day's work at the town's live price.
    no_close    `router.the_close` forced False. Reverts change (b): the last two days no longer
                suppress the CRITICAL harvest promotion.
    neither     both of the above. The endgame as it was before `e2500_close`.

Change (c) -- deleting the d28 pen CRITICAL promotion -- is not separable by monkeypatch because the
code was removed, so `neither` is the closest available control and is a lower bound on (c).

## What would have to be true for an arm to win

`the_close` was built on the reasoning that a harvest in the last two days is priced at the SHOP,
not at base, so the CRITICAL promotion that forces an ageing crop to be picked is wrong there. If
that reasoning is right, `ship` beats `neither` in the last three days. The ladder says the opposite
by 101 points, and the ladder is the only measurement of the three changes together.
"""

import argparse
import importlib
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

US = "alex chilton"
GAMES = ("98495047", "98460892", "98494953", "98499540", "98501831", "98428765")


def _patched(flat_price, no_close):
    """Context-manager-ish: returns a restore callable."""
    R = importlib.import_module("kagg.search.router")
    saved = {"crop_ops": R.crop_ops, "animal_ops": R.animal_ops, "the_close": R.the_close}

    if flat_price:
        _cr, _an = saved["crop_ops"], saved["animal_ops"]
        R.crop_ops = lambda *a, **k: _cr(*a, **{**k, "product_price": None})
        R.animal_ops = lambda *a, **k: _an(*a, **{**k, "product_price": None})
    if no_close:
        R.the_close = lambda day: False

    def restore():
        for name, fn in saved.items():
            setattr(R, name, fn)
    return restore


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--handover", type=int, default=27)
    ap.add_argument("--games", default=",".join(GAMES))
    ap.add_argument("--out", default="data/logs/hundred_points.csv")
    a = ap.parse_args()

    book = importlib.import_module("does_the_book_reading_win_games")

    arms = [("ship", False, False), ("flat_price", True, False),
            ("no_close", False, True), ("neither", True, True)]

    out = REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("episode,seed,tape," + ",".join(n for n, _, _ in arms) + "\n")
    fh.flush()

    print(f"handover d{a.handover}: our agent plays the last {30 - a.handover} days, "
          f"both tapes replayed to there")
    print("every number is OUR money minus THEIRS. `tape` is our own recorded ladder play "
          "continuing.\n", flush=True)
    print(f"{'episode':>10} {'tape':>10} " + " ".join(f"{n:>11}" for n, _, _ in arms), flush=True)

    t0 = time.time()
    totals = {n: 0 for n, _, _ in arms}
    tape_total = 0
    rows = 0
    for ep in a.games.split(","):
        path = book._find(ep)
        if path is None:
            print(f"{ep:>10}  not downloaded", flush=True)
            continue
        rec = json.loads(path.read_text())
        names = rec["info"]["TeamNames"]
        if US not in names:
            continue
        seat = names.index(US)
        seed = rec["info"]["seed"]

        z = book.play(path, seat, seed, None, use_old_gate=False)
        zm = z["ours"] - z["theirs"]
        got = {}
        for name, flat, noclose in arms:
            restore = _patched(flat, noclose)
            try:
                r = book.play(path, seat, seed, a.handover, use_old_gate=False)
            finally:
                restore()
            got[name] = r["ours"] - r["theirs"]
            totals[name] += got[name]
        tape_total += zm
        rows += 1
        print(f"{ep:>10} {zm:>+10,.0f} " + " ".join(f"{got[n]:>+11,.0f}" for n, _, _ in arms),
              flush=True)
        fh.write(",".join(str(x) for x in [ep, seed, round(zm)]
                          + [round(got[n]) for n, _, _ in arms]) + "\n")
        fh.flush()
    fh.close()

    if rows:
        print(f"\n{'mean':>10} {tape_total / rows:>+10,.0f} "
              + " ".join(f"{totals[n] / rows:>+11,.0f}" for n, _, _ in arms))
        base = totals["ship"]
        print("\nagainst `ship`:")
        for n, _, _ in arms:
            if n != "ship":
                print(f"  {n:>11}  {(totals[n] - base) / rows:>+11,.0f} per game")
    print(f"\n({time.time() - t0:.0f}s)  rows -> {out}")


if __name__ == "__main__":
    main()
