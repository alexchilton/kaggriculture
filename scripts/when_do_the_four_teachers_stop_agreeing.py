"""If the start board is identical, what is the first turn at which the tapes disagree?

    python -u scripts/when_do_the_four_teachers_stop_agreeing.py

ALEX'S QUESTION
---------------
*"why does the replay see the start board and say no this is different to what i expect - what is
the net getting as a signal that says its all different when the start board is identical - what is
its learning signal which is overloading it"*

It is the right question and it has a number. All replays start from the same board -- same tiles,
NW only, $3,000, no shops (`project_kaggriculture_start_state_is_fixed`). So at turn 0 the four
tapes present the network with **identical features**. Two cases, and they are opposite:

  they AGREE on the action    identical input, identical label. Nothing to overload. The opening is
                              learnable exactly and should transfer to any seed, because no board
                              feature distinguishes seed 9000 from a tape at turn 0.

  they DISAGREE               identical input, four different labels. The net cannot do better than
                              average them, by construction and regardless of capacity. That IS the
                              overloaded signal, and it would show up as a confident wrong opening
                              on every seed including the tapes' own.

So this walks the four action streams together and reports the FIRST turn at which any two differ,
plus what each of them was doing there. The board diverges for two reasons and they start on
different days -- weeds spawn at the end of every day from `weedSpawnChance = 0.005`, and the first
shop unlocks at the end of day 2 for day 3 -- so the turn number says WHICH one first forced the
teachers apart.
"""
import collections
import itertools
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

TAPES = {
    "92498144": "data/seed_scripts/kawashigi/92498144.json",
    "92466371": "data/seed_scripts/kawashigi/92466371.json",
    "91906088": "data/seed_scripts/downloads_2026-08-13/91906088.json",
    "91907974": "data/seed_scripts/downloads_2026-08-13/91907974.json",
}


def seat_of(doc, team="カワシギ"):
    names = [str(t or "") for t in ((doc.get("info") or {}).get("TeamNames") or [])]
    for i, n in enumerate(names):
        if team.lower() in n.lower():
            return i
    raise SystemExit(f"{team} not in {names}")


def stream(path):
    doc = json.loads(pathlib.Path(path).read_text())
    seat = seat_of(doc)
    out = []
    for step in doc["steps"][1:]:
        act = ((step[seat] or {}).get("action") or {})
        out.append((
            tuple(act.get("farmer") or ()),
            tuple(tuple(h) for h in (act.get("hands") or ())),
            tuple(sorted(tuple(o) for o in (act.get("market") or ()) if o)),
        ))
    return seat, out


def main():
    streams, seats = {}, {}
    for name, path in TAPES.items():
        seats[name], streams[name] = stream(path)
    n = min(len(s) for s in streams.values())
    print(f"{len(streams)} tapes, {n} comparable turns")
    for name in TAPES:
        print(f"  {name}  seat {seats[name]}  {len(streams[name])} turns")

    first = None
    for t in range(n):
        vals = {name: streams[name][t] for name in streams}
        if len({v for v in vals.values()}) > 1:
            first = t
            break

    print()
    if first is None:
        print("the four tapes NEVER disagree over the compared turns")
        return

    print(f"FIRST DISAGREEMENT at turn {first}  (day {first // 24}, hour {first % 24})")
    for name in TAPES:
        f, h, m = streams[name][first]
        print(f"  {name}  farmer {f}  hands {len(h)}  market {list(m)}")

    # How far the agreement extends is the size of the opening a net could learn without any
    # board feature to key on -- and therefore the part that should transfer to a fresh seed.
    print(f"\nturns 0..{first - 1} are IDENTICAL across all four tapes "
          f"({first} turns, {first / 24:.1f} days).")

    # Then: how often do they agree after that? A high rate means the tapes are mostly one policy
    # with occasional branches; a low one means four different games from here on.
    agree_after = sum(1 for t in range(first, n)
                      if len({streams[name][t] for name in streams}) == 1)
    print(f"turns {first}..{n - 1}: all four agree on {agree_after:,} of {n - first:,} "
          f"({agree_after / max(1, n - first):.1%})")

    # Pairwise, because "all four agree" is a harsh test -- two tapes matching is still a label the
    # net can learn from a shared board feature.
    print("\npairwise agreement over ALL turns:")
    for a, b in itertools.combinations(TAPES, 2):
        same = sum(1 for t in range(n) if streams[a][t] == streams[b][t])
        print(f"  {a} vs {b}   {same:>5,}/{n:,}  {same / n:>6.1%}")

    # And the thing that actually overloads a per-turn label: how many DISTINCT actions the four
    # tapes present for the same turn index, averaged. 1.0 means a clock lookup is well defined.
    distinct = [len({streams[name][t] for name in streams}) for t in range(n)]
    hist = collections.Counter(distinct)
    print("\ndistinct actions at the same turn index, across the four tapes:")
    for k in sorted(hist):
        print(f"  {k} distinct   {hist[k]:>5,} turns  {hist[k] / n:>6.1%}")
    print(f"  mean {sum(distinct) / n:.3f}   (1.000 would mean the tape is a pure clock lookup)")


main()
