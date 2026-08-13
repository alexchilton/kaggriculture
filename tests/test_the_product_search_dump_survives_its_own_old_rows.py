"""`--analyse` must read a dump written by an older run, and must not condition on a guess.

Two separate contracts, both live right now because a sweep using this script is running on the
remote box and will append rows in the OLD shape for hours yet.

## 1. Old rows

The shape those rows have is `tag, seed, opponent, seat, ours, theirs, win` plus the six axis
values. Every field added since then must be optional on read: `--analyse` may not crash on a row
that lacks one, and may not silently drop it either -- a slice that quietly discards half the run
and prints a win rate for the rest is worse than one that fails.

## 2. The shop draw is not a function of the seed

The tempting shortcut is to re-derive each game's shop draw at analyse time: the unlocks look
seed-pure (`random.Random((seed * 1_000_003) ^ day)`, one `rng.choice` per unlock). They are not.
`_end_of_day` runs `_spawn_weeds` on that same generator first, once per EMPTY tile per player,
so where the draw lands in the stream depends on how much of the board each side had built on.

Measured across three seeds, with weeds on and off: the first unlock matches between two different
agent pairings and every later one diverges. So a derived draw would be right for day 3 and wrong
for the other seven, on every row. The draw is recorded at play time instead, and rows that predate
the field are reported as unconditioned rather than filled in.
"""

import json
import sys

import pytest

sys.path.insert(0, ".")

import scripts.product_search as ps

#: Exactly the fields the running sweep writes, and nothing else.
OLD_ROW = {"tag": "search", "seed": 1000, "opponent": "victor_0.json", "seat": 0,
           "ours": 91000.0, "theirs": 88000.0, "win": 1,
           "carrot": 4, "carrot_start": 21, "melon_shift": 2, "melon_day": 5,
           "cow_cap": 6, "geese": 0}


def write(tmp_path, rows):
    path = tmp_path / "product_search.jsonl"
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return str(path)


def test_analyse_reads_a_dump_with_only_the_old_fields(tmp_path, capsys):
    rows = []
    for i in range(8):
        row = dict(OLD_ROW, seed=1000 + i % 2, carrot=i % 3,
                   win=1 if i % 2 else 0, ours=90000.0 + i)
        rows.append(row)
    ps.analyse(write(tmp_path, rows))
    out = capsys.readouterr().out
    assert "8 games" in out
    assert "BEST COMBINATION PER SEED" in out


def test_a_row_without_the_shop_draw_is_reported_not_dropped(tmp_path, capsys):
    """The count of rows that could not be conditioned has to be on the page. Otherwise a slice
    over the 3 rows that carry the field reads exactly like a slice over all 11."""
    rows = [dict(OLD_ROW, seed=1000 + i, win=i % 2) for i in range(8)]
    rows += [dict(OLD_ROW, seed=2000 + i, win=i % 2,
                  shops=[["YARN_STORE", 2], ["BAKERY", 1]]) for i in range(3)]
    ps.analyse(write(tmp_path, rows))
    out = capsys.readouterr().out
    assert "11 games" in out
    assert "8" in out and "no shop draw recorded" in out.lower()


def test_the_shop_slice_counts_instances_carrying_the_product_not_shop_names(tmp_path, capsys):
    """The conditioning variable is how many unlocked INSTANCES sell the product, which is not the
    number of shops and not their names.

    Both groups below draw ONE distinct shop, twice. Counting shops puts them in the same bucket
    and reports a wash; counting strawberry carriers puts them at 0 and 2 and reports opposite
    win rates, which is the regime split this block exists to expose.
    """
    rows = [dict(OLD_ROW, seed=1000 + i, win=1,
                 shops=[["YARN_STORE", 2]]) for i in range(4)]
    rows += [dict(OLD_ROW, seed=2000 + i, win=0,
                  shops=[["SMOOTHIE_SHOP", 2]]) for i in range(4)]

    assert ps.carriers(rows[0], "STRAWBERRY") == 0
    assert ps.carriers(rows[-1], "STRAWBERRY") == 2
    assert ps.carriers(rows[0], "WOOL") == 2

    ps.analyse(write(tmp_path, rows), product="STRAWBERRY")
    out = capsys.readouterr().out
    assert "STRAWBERRY" in out
    carrier_line = next(l for l in out.splitlines() if l.strip().startswith("carriers"))
    assert "0=n4" in carrier_line and "2=n4" in carrier_line, carrier_line
    assert "0:[4=1.000]" in out and "2:[4=0.000]" in out, out


def test_two_instances_of_one_shop_carry_twice_as_much_as_one():
    """Shops are drawn WITH REPLACEMENT and each copy consumes independently, so the same name
    twice is two carriers -- and a `FARMERS_MARKET` is a carrier of four different products."""
    assert ps.carriers({"shops": [["YARN_STORE", 1]]}, "WOOL") == 1
    assert ps.carriers({"shops": [["YARN_STORE", 3]]}, "WOOL") == 3
    for product in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"):
        assert ps.carriers({"shops": [["FARMERS_MARKET", 1]]}, product) == 1
    assert ps.carriers({"shops": [["FARMERS_MARKET", 1]]}, "MILK") == 0


def test_the_shop_draw_is_not_a_function_of_the_seed():
    """The measurement behind the decision not to derive it. If this ever passes, the derivation
    becomes available and the recorded field becomes redundant -- but until then, deriving it is
    a guess printed as arithmetic."""
    pytest.importorskip("kaggle_environments")
    from kaggle_environments import make

    from kagg.agents import contrarian, heuristic, rancher

    def shops(a, b, seed):
        env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0},
                   debug=False)
        env.run([a, b])
        return env.steps[-1][0]["observation"]["town"]["unlocked_shops"]

    one = shops(heuristic.make_agent(), heuristic.make_agent(), 1000)
    two = shops(rancher.agent, contrarian.agent, 1000)
    assert one != two, ("the draw no longer depends on how the board was played; "
                        "re-read _spawn_weeds before trusting this either way")
    assert one[0] == two[0], "the FIRST unlock is stable; the divergence starts at the second"
