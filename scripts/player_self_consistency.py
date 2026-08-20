"""Does one player play the SAME day-block across their own games -- and what splits it when not?

Alex, 2026-08-20: "based on shop draw and opponent melon amount at d3 -> per day board -> ... or we
work out what splits the following days after the d15 or so -> there is almost certainly a logic to
it -> maybe we just dont see it".

That is a hypothesis with a measurement, and this is its precondition. Before asking WHICH features
split a player's days, ask whether that player is self-consistent at all:

  If a player's own games repeat the same block for day N, the branch logic exists and can be
  found -- condition on candidate features and watch blocks-per-group fall towards 1.

  If a player's own games all differ at day N, there is no rule to recover from these replays. The
  variation is coming from board state we would have to reproduce exactly, not from a decision.

`count_tape_blocks.py` hints at the answer already: over ALL seasons the day-0 top block covers
24.7%, but over UNIQUE players only 11.8%. The gap is repeat players agreeing with themselves.
This measures that directly, per player, and reports the candidate split features alongside.

**These downloads are SELECTED LOSSES.** Nothing here ranks a player by outcome, and nothing
should.

    python -u scripts/player_self_consistency.py --dirs data/seed_scripts/top_guys --days 20
"""

import argparse
import collections
import glob
import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.count_day_blocks import canonical                    # noqa: E402

TURNS_PER_DAY = 24

#: Alex, 2026-08-20: "we know the algo for the animals so we match the days then put in the animals
#: after the day is returned". If the herd is GENERATED from the shop draw by a rule we already
#: have, a stored block never needs to carry it -- and the block only has to reproduce the plant
#: skeleton. That is a smaller thing to match, so it should be MORE determined by the d3 key.
#:
#: Every op below either buys, houses, feeds, tends or sells an animal. Strip them and what is left
#: is the route and the field work.
ANIMAL_NAMES = frozenset(("GOOSE", "COW", "SHEEP"))
ANIMAL_PRODUCTS_ALL = frozenset(("EGG", "MILK", "WOOL"))
ANIMAL_OPS = frozenset(("BUY_ANIMAL", "FEED", "CARE", "BUILD_PASTURE", "BUILD_COOP"))


def is_animal_op(op):
    """`op` is a list like ["PLACE", "COW"] or ["SELL", "MILK", 6]."""
    if not op:
        return False
    name = str(op[0])
    if name in ANIMAL_OPS:
        return True
    rest = {str(x) for x in op[1:]}
    return bool(rest & (ANIMAL_NAMES | ANIMAL_PRODUCTS_ALL))


def plant_only(action):
    """The same action with every animal op removed, so PASS-vs-FEED does not count as a mismatch."""
    keep_unit = lambda a: None if (a and is_animal_op(a)) else a          # noqa: E731
    return {"farmer": keep_unit(action.get("farmer")),
            "hands": [keep_unit(a) for a in (action.get("hands") or [])],
            "market": [o for o in (action.get("market") or []) if not is_animal_op(o)]}

#: The day the season's line is chosen. d3 is the first shop unlock (interval 3), and it is where
#: the leader's fixed 74-turn opening ends. Melon costs 80 a seed and first yields d10-12, so a d3
#: melon commitment is the largest irreversible bet in the game -- priced by base-market depth,
#: which the opponent's acreage sets, because NO shop buys melon.
KEY_DAY = 3


#: **The label format and the replay format are NOT the same, and reading one with the other's
#: names produces a constant.** In `label_games` output the observation carries `shops`; in a
#: downloaded replay it is `town.unlocked_shops`. Label tiles are strings; replay tiles are dicts
#: like {"crop": "WHEAT", "kind": "PLANT", "watered_today": false, ...}. The first version of this
#: script read `obs["shops"]` and tested `"MELON" in t` on a dict, so BOTH features were constant
#: across every game and the split table read 16.0 blocks per group -- i.e. one group, containing
#: everything. That is not "the features do not explain it"; it is "no features were measured".
def melon_of(obs, seat):
    """How much MELON the OPPONENT has in the ground -- one of Alex's candidate split features.

    Seeds are private, so the visible signal is planted tiles, which is also what a real agent
    could condition on.
    """
    farms = obs.get("farms") or []
    other = 1 - seat
    if other >= len(farms):
        return None
    tiles = (farms[other] or {}).get("tiles") or []
    return sum(1 for row in tiles for t in row
               if isinstance(t, dict) and t.get("crop") == "MELON")


def shops_of(obs):
    town = obs.get("town")
    if isinstance(town, dict):
        return tuple(sorted(str(s) for s in (town.get("unlocked_shops") or [])))
    # The label format keeps it flat. Accept both rather than silently returning ().
    flat = obs.get("shops")
    if flat is not None:
        return tuple(sorted(str(s) for s in flat))
    raise KeyError("no town.unlocked_shops and no shops; obs keys are %s" % sorted(obs.keys()))


#: Shop IDENTITY is hopeless as a key: 8 shops drawn WITH replacement every 3 days is 792 distinct
#: multisets by d15 and 6,435 by season end. What a decision actually turns on is the DEMAND the
#: draw induces, and many multisets collapse to the same profile -- so count, per product, how many
#: unlocked shops buy it.
SHOP_BUYS = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}


#: Alex, 2026-08-20: "its not particularly 'shop' draws its more plant friendly or animal friendly
#: types". Correct, and it collapses the space enormously: YARN_STORE is pure animal, PET_CAFE and
#: FARMERS_MARKET are pure plant, SMOOTHIE_SHOP is one of each.
ANIMAL_PRODUCTS = frozenset(("EGG", "MILK", "WOOL"))


def friendliness_of(shops):
    """(animal demand slots, plant demand slots) induced by the draw.

    **No shop buys MELON.** It is absent from every entry of SHOP_BUYS, so melon revenue comes
    only from the base market, whose depth is shared with the opponent. That is exactly why the
    opponent's melon acreage is a SEPARATE signal from the shop draw rather than a proxy for it.
    """
    animal = plant = 0
    for s in shops:
        for product in SHOP_BUYS.get(s, ()):
            if product in ANIMAL_PRODUCTS:
                animal += 1
            else:
                plant += 1
    return (animal, plant)


def read(path, days):
    """-> (player_name, seat, {day: block}, {day: features}) per seat, or None if not a replay."""
    rep = json.loads(pathlib.Path(path).read_text())
    if not isinstance(rep, dict) or not rep.get("steps"):
        return []
    info = rep.get("info")
    names = info.get("TeamNames") if isinstance(info, dict) else None
    if not names:
        names = ["%s#0" % pathlib.Path(path).stem, "%s#1" % pathlib.Path(path).stem]

    turns = collections.defaultdict(list)
    feats = {}
    for step in rep["steps"]:
        for seat, cell in enumerate(step):
            obs = cell.get("observation") or {}
            day, hour = int(obs.get("day", 0) or 0), int(obs.get("hour", 0) or 0)
            if day >= days:
                continue
            act = cell.get("action")
            if act is None:
                continue
            turns[(seat, day)].append(
                (hour, canonical(act), canonical(plant_only(act))))
            if hour == 0:
                feats[(seat, day)] = (friendliness_of(shops_of(obs)), melon_of(obs, seat))

    out = []
    for seat in (0, 1):
        blocks, plants, f = {}, {}, {}
        for day in range(days):
            t = turns.get((seat, day)) or []
            if len(t) != TURNS_PER_DAY:
                continue
            t = sorted(t)
            blocks[day] = hashlib.md5(
                "|".join(a for _h, a, _p in t).encode()).hexdigest()[:10]
            plants[day] = hashlib.md5(
                "|".join(p for _h, _a, p in t).encode()).hexdigest()[:10]
            f[day] = feats.get((seat, day))
        name = names[seat] if seat < len(names) else "seat%d" % seat
        out.append((name, blocks, plants, f))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="+", required=True)
    ap.add_argument("--days", type=int, default=20)
    ap.add_argument("--min-games", type=int, default=4)
    args = ap.parse_args()

    paths = []
    for d in args.dirs:
        paths += sorted(glob.glob(d.rstrip("/") + "/*.json"))

    per_player = collections.defaultdict(list)      # name -> [(blocks, plants, feats)]
    for p in paths:
        for name, blocks, plants, feats in read(p, args.days):
            if blocks:
                per_player[name].append((blocks, plants, feats))

    counts = sorted(((len(v), k) for k, v in per_player.items()), reverse=True)
    print("players: %d   seasons: %d" % (len(per_player), sum(n for n, _ in counts)))
    print("\nbest-covered players:")
    for n, name in counts[:8]:
        print("  %3d seasons   %s" % (n, name))

    good = [(n, k) for n, k in counts if n >= args.min_games]
    if not good:
        raise SystemExit("\nNo player has >= %d seasons. Self-consistency is not measurable here."
                         % args.min_games)

    print("\nSELF-CONSISTENCY: of one player's own games, what share play the modal block?")
    print("%-28s %7s %s" % ("player", "games", "  ".join("d%-2d" % d for d in range(0, args.days, 2))))
    for n, name in good[:6]:
        seasons = per_player[name]
        cells = []
        for day in range(0, args.days, 2):
            bs = [b[day] for b, _p, _f in seasons if day in b]
            if not bs:
                cells.append("  - ")
                continue
            top = collections.Counter(bs).most_common(1)[0][1]
            cells.append("%3.0f%%" % (100.0 * top / len(bs)))
        print("%-28s %7d %s" % (name[:28], n, " ".join(cells)))

    # **The decision point is d3, not "today".** Alex: "the melon number of opponent is the d3 most
    # important factor". So the key is read ONCE at d3 and used to explain every later day, which
    # is a claim about a season LINE being chosen, not about each day reacting to its own state.
    # Conditioning on today's state instead would measure something weaker and easier.
    print("\nDO THE FEATURES SPLIT IT?  blocks per group, key read ONCE at d3:")
    print("    (shop animal/plant slots at d3, opponent MELON tiles at d3)")
    print("%-28s %7s %6s %s"
          % ("player", "games", "groups", "  ".join("d%-2d" % d for d in range(2, args.days, 2))))
    def split_table(title, which):
        print("\n%s" % title)
        print("%-24s %6s %6s %s"
              % ("player", "games", "groups",
                 "  ".join("d%-2d" % d for d in range(2, args.days, 2))))
        for n, name in good[:6]:
            keyed = [(s[which], s[2].get(KEY_DAY)) for s in per_player[name]
                     if s[2].get(KEY_DAY) is not None]
            if not keyed:
                print("%-24s %6d   none  (no d%d observation)" % (name[:24], n, KEY_DAY))
                continue
            cells = []
            for day in range(2, args.days, 2):
                groups = collections.defaultdict(set)
                for blocks, key in keyed:
                    if day in blocks:
                        groups[key].add(blocks[day])
                cells.append("%4.1f" % (sum(len(v) for v in groups.values()) / len(groups))
                             if groups else "  - ")
            print("%-24s %6d %6d %s"
                  % (name[:24], n, len({k for _b, k in keyed}), " ".join(cells)))

    split_table("A) WHOLE DAY -- blocks per group, key read ONCE at d3:", 0)
    split_table("B) PLANT SKELETON ONLY -- animal ops stripped, herd generated by rule:", 1)

    # **Alex, 2026-08-20: "up to d12 the only criteria is melon and shops".** Tables A and B freeze
    # the key at d3, which throws away every later unlock -- shops arrive at d3, d6, d9 and d12, so
    # by d12 a d3-only key is three draws out of date. This keeps melon fixed at d3, because that is
    # the irreversible commitment, and lets the shop half move with the town.
    print("\nC) MELON AT d3 + SHOPS AS THEY UNLOCK -- the key Alex actually described:")
    print("%-24s %6s %s"
          % ("player", "games", "  ".join("d%-2d" % d for d in range(2, args.days, 2))))
    for n, name in good[:6]:
        seasons = per_player[name]
        cells = []
        for day in range(2, args.days, 2):
            groups = collections.defaultdict(set)
            for blocks, plants, f in seasons:
                key3, today = f.get(KEY_DAY), f.get(day)
                if day not in plants or key3 is None or today is None:
                    continue
                # (melon at d3, shop class TODAY)
                groups[(key3[1], today[0])].add(plants[day])
            cells.append("%4.1f" % (sum(len(v) for v in groups.values()) / len(groups))
                         if groups else "  - ")
        print("%-24s %6d %s" % (name[:24], n, " ".join(cells)))
    print("\n1.0 means the d3 key fully determines that day for that player.")
    print("B below A is Alex's split working: the day is matchable once the herd is not stored.")


if __name__ == "__main__":
    main()
