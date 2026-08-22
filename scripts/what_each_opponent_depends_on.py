"""What does each pool opponent plant and herd -- and therefore what could we take away from them?

Alex, 2026-08-21: *"if we know the opponent has tomato or something if not to gain extra cash but
as an adversarial we should also do tomato - not so we gain $ but to stop the opponent...etc. for
that we need an opponent with tomato"*, and the same for *"the combi of the opponent going hard on
animal a,b and the shop"* deciding our cow/sheep split.

This is a different question from every arm measured so far. Those asked "does the crop pay us".
This asks "does contesting it cost him more than it costs us", which is a question about the
MARKET, not the field -- and the evidence that the channel is real is already in hand, running the
wrong way: the tomato arm withdrew four wheat tiles, put 115 fewer wheat units into the book, and
handed the opponent **$38,201** on seed 42 through the price alone
(`docs/the_carrot_window_is_three_days_2026-08-21.md`).

Read off the thin action tapes, which is all that is needed:

  **`BUY_SEED <crop>`** is a clean tile count. Seeds are bought to be sown and a surplus is rare.
  **`BUY_ANIMAL <species>`** is the herd, exactly -- animals are bought once and placed.
  **SELL is NOT counted.** The tapes re-post an order every turn, so summing `SELL` counts offers,
  not fills (`feedback_offers_are_not_fills`). Revenue per product needs a simulated season with
  `kagg/analysis/fills.py` and is deliberately not guessed at here.

    python -u scripts/what_each_opponent_depends_on.py
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

POOL = REPO / "data/opponent_pool_ranked.json"
TAPE_DIR = REPO / "data/opponent_tapes"

CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
SPECIES = ("COW", "SHEEP", "GOOSE")


def read_tape(row):
    path = TAPE_DIR / ("%s_seat%d.json" % (pathlib.Path(row["replay"]).stem, int(row["seat"])))
    if not path.exists():
        return None
    return json.loads(path.read_text())["actions"]


def profile(actions):
    """`(seed_counts, animal_counts, first_day, plant_counts)` for one recorded season."""
    seeds, animals, first, plants = collections.Counter(), collections.Counter(), {}, collections.Counter()
    for t, a in enumerate(actions):
        day = t // 24
        for o in a.get("market") or []:
            if len(o) >= 3 and o[0] == "BUY_SEED":
                seeds[o[1]] += int(o[2])
                first.setdefault(o[1], day)
            elif len(o) >= 3 and o[0] == "BUY_ANIMAL":
                animals[o[1]] += int(o[2])
                first.setdefault(o[1], day)
        for act in [a.get("farmer") or ["PASS"]] + list(a.get("hands") or []):
            if len(act) >= 2 and act[0] == "PLANT":
                plants[act[1]] += 1
    return seeds, animals, first, plants


def main():
    rows = json.loads(POOL.read_text())
    rows.sort(key=lambda r: r["rank"])
    print("Seeds bought and animals bought, per recorded season. `first` is the day of the first")
    print("purchase of that item -- the day an adaptive rule would have to have decided by.\n")
    hdr = ("%-26s %5s %5s" % ("opponent", "rank", "band")
           + "".join("%9s" % c[:6] for c in CROPS)
           + "".join("%7s" % s[:5] for s in SPECIES))
    print(hdr)
    print("-" * len(hdr))
    tomato_players, herds = [], []
    for r in rows:
        acts = read_tape(r)
        if acts is None:
            print("%-26s %5d %5s   no thin tape" % (r["name"][:26], r["rank"], r["band"]))
            continue
        seeds, animals, first, _ = profile(acts)
        print("%-26s %5d %5s" % (r["name"][:26], r["rank"], r["band"])
              + "".join("%9s" % ("%d@d%d" % (seeds[c], first[c]) if seeds[c] else "-")
                        for c in CROPS)
              + "".join("%7s" % (animals[s] or "-") for s in SPECIES))
        if seeds["TOMATO"]:
            tomato_players.append((r["name"], seeds["TOMATO"], first.get("TOMATO")))
        herds.append((r["name"], animals["COW"], animals["SHEEP"], animals["GOOSE"]))

    print("\n\nOPPONENTS WHO PLANT TOMATO -- the ones an adversarial tomato arm needs")
    if tomato_players:
        for n, q, d in sorted(tomato_players, key=lambda x: -x[1]):
            print("  %-28s %3d seeds, first at d%s" % (n[:28], q, d))
    else:
        print("  NONE in this pool. An adversarial tomato arm cannot be measured against it,")
        print("  and the pool needs rebuilding around the behaviour rather than the rank.")

    print("\n\nHERD SPLIT -- what a cow/sheep counter-pick would be answering")
    print("  %-28s %6s %6s %6s   %s" % ("opponent", "cow", "sheep", "goose", "leans"))
    for n, c, s, g in sorted(herds, key=lambda x: -(x[1] + x[2] + x[3])):
        lean = "COW" if c > s else "SHEEP" if s > c else "even"
        print("  %-28s %6d %6d %6d   %s" % (n[:28], c, s, g, lean if (c or s) else "-"))


if __name__ == "__main__":
    main()
