"""On a downloaded game: could the town have absorbed a bigger cow herd, or would milk have crashed?

Alex, on the 99523212 loss (6 cows / 12 sheep, WOOL $167 -> $11, MILK steady at $239):
*"so you think that one should have been more cow than wool"*.

**The trap this answers.** "Milk was $239, so more cows would have banked more" does not follow.
Milk may be at $239 *because* only six cows were selling into it -- the price is endogenous, and it
is the same mechanism that took wool to $11. Twelve cows might simply have crashed milk instead.

What decides it is the town's DRAIN: how many units it will pull between now and the bell, which is
fixed by which shops are unlocked and does not depend on our supply (`_town_consume`,
`kaggriculture.py:696-717`). Supply above the drain is what floods a book.

So this prints, per product:

    drain      units the town pulls all season, from THIS game's unlocked shops
    made       units our herd actually produced, from the animals' own intervals
    headroom   drain - made, i.e. how much more it could have taken

A product where `made` already exceeds `drain` was over-supplied and more animals make it worse.
One with headroom left is where the herd was too small.
"""

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.search import schedule_agent as SA                             # noqa: E402
from kagg.search import router as RT                                     # noqa: E402

US = "alex chilton"
TPD = 24
LAST_DAY = 29


def _placed_days(replay, seat):
    """`[(species, placed_day)]` for every animal we put on the board."""
    out = []
    for t, step in enumerate(replay.get("steps") or []):
        if seat >= len(step):
            continue
        act = (step[seat] or {}).get("action") or {}
        for op in [act.get("farmer")] + list(act.get("hands") or []):
            if op and len(op) >= 2 and op[0] == "PLACE" and op[1] in ("COW", "SHEEP"):
                out.append((op[1], t // TPD))
    return out


def _made(species, placed_day):
    """Units this animal produces from `placed_day` to the bell, per `_daily_refresh_animals`."""
    a = RT.ANIMALS[species]
    return sum(1 for d in range(placed_day, LAST_DAY)
               if (d + 1) - placed_day - a["first_yield_day"] >= 0
               and ((d + 1) - placed_day - a["first_yield_day"]) % a["interval"] == 0)


def main(paths):
    for p in paths:
        f = pathlib.Path(p)
        r = json.loads(f.read_text())
        names = (r.get("info") or {}).get("TeamNames") or []
        seat = names.index(US) if US in names else 0
        steps = r.get("steps") or []
        last = (steps[-1][0] or {}).get("observation") or {}
        shops = list((last.get("town") or {}).get("unlocked_shops") or [])
        farms = last.get("farms") or []
        ours = float(farms[seat].get("money", 0)) if seat < len(farms) else 0.0
        theirs = float(farms[1 - seat].get("money", 0)) if 1 - seat < len(farms) else 0.0

        made = {"MILK": 0, "WOOL": 0}
        herd = {"COW": 0, "SHEEP": 0}
        for sp, day in _placed_days(r, seat):
            herd[sp] += 1
            made[RT.ANIMALS[sp]["product"]] += _made(sp, day)

        print(f"=== {f.stem}   ours ${ours:,.0f} v ${theirs:,.0f}  "
              f"{'WIN' if ours > theirs else 'LOSS'}")
        print(f"    herd placed: COW {herd['COW']}  SHEEP {herd['SHEEP']}")
        print(f"    shops: {', '.join(shops) or '(none recorded)'}")
        print(f"    {'product':<9}{'drain':>8}{'made':>7}{'headroom':>10}   per extra animal")
        for prod, sp in (("MILK", "COW"), ("WOOL", "SHEEP")):
            # The whole season's pull, counted from step 0.
            drain = SA.town_drain_remaining(prod, 0, shops)
            head = drain - made[prod]
            a = RT.ANIMALS[sp]
            # What one more animal placed on the median day would add.
            extra = _made(sp, 10)
            note = (f"+{extra} units, {'FITS' if head >= extra else 'FLOODS'}")
            print(f"    {prod:<9}{drain:>8}{made[prod]:>7}{head:>10}   {note}")
        print()


if __name__ == "__main__":
    main(sys.argv[1:])
