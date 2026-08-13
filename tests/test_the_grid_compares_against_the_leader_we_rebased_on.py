"""The default tape, the tape registry, and the CSV.

**The default.** `--tape` defaulted to `seb` from the day the argument was added, and the project
rebased onto Victor on 2026-08-11 and has worked against Victor since. Every grid run without an
explicit `--tape victor` was therefore comparing against the wrong leader, and the two disagree
materially: the `animals` row totals -4 over six days against Seb, oscillating, which reads as
timing jitter -- and -14 over fourteen days against Victor, one-directional, which is a defect. It
stayed invisible for two days.

It is not a preference. Seb's tape was recorded on `townCenterSellInterval = 12`, the PRE-rebalance
economy, so `breakdown.env_config` replays the whole comparison at an economy nobody plays any more.
Victor's is on 24, the one we play.

**The registry.** A `TAPES` entry that names a team not in its own recording silently compares
against the opponent, and one whose file is missing fails at the point someone needs the answer. Both
are cheap to check and neither was checked.

**The CSV.** A day per row, a field per column, and every column header names whether the number is
a board count, an offer, a fill, a dollar figure or a turn-budget term.
"""

import csv
import importlib
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

import scripts.breakdown as B

#: The prefixes a CSV column may carry. Every one of them says what KIND of number the cell is.
KINDS = ("board.", "offered.", "fill.", "cash.", "budget.")


def test_the_default_tape_is_the_leader_the_project_rebased_onto():
    assert B.DEFAULT_TAPE == "victor", (
        "the grid defaults to a tape recorded on townCenterSellInterval 12, an economy that has "
        "not been played since 2026-08-08")
    assert B.DEFAULT_TAPE in B.TAPES
    source = (REPO / "scripts/breakdown.py").read_text()
    assert 'default=DEFAULT_TAPE' in source, (
        "--tape must take its default from the constant, or the two can drift apart and the "
        "constant becomes documentation")


def test_kawashigi_is_in_the_registry():
    """The current #1 and the project's live reference. `TAPES` had no entry for him."""
    assert "kawashigi" in B.TAPES
    replay, schedule, team = B.TAPES["kawashigi"]
    assert (REPO / replay).exists(), replay
    assert (REPO / schedule).exists(), schedule


@pytest.mark.parametrize("name", sorted(B.TAPES))
def test_every_tape_names_a_team_that_is_actually_in_its_own_recording(name):
    """`tape_policy` does `TeamNames.index(team)`. A name that is not there raises; a name that is
    there but wrong is worse, because it silently drives the OPPONENT's actions into the tape
    column and the grid compares against the loser."""
    import json

    replay, _schedule, team = B.TAPES[name]
    path = REPO / replay
    if not path.exists():
        pytest.skip(f"{replay} not downloaded")
    names = json.loads(path.read_text())["info"]["TeamNames"]
    assert team in names, f"{name}: {team!r} is not in {names}"


def test_the_registry_records_which_economy_each_tape_was_played_on():
    """`env_config` reads `townCenterSellInterval` off the recording so both columns run the same
    economy. Kawashigi and Victor must be on 24, the rebalanced one; Seb is on 12 and that is the
    whole reason he is no longer the default."""
    import json

    def interval(name):
        path = REPO / B.TAPES[name][0]
        if not path.exists():
            pytest.skip(f"{B.TAPES[name][0]} not downloaded")
        return (json.loads(path.read_text()).get("configuration") or {}
                ).get("townCenterSellInterval")

    assert interval("kawashigi") == 24
    assert interval("victor") == 24
    assert interval("seb") == 12


def test_the_csv_is_one_row_per_day_and_names_the_kind_of_every_column(tmp_path):
    from kagg.agents import heuristic, rancher

    B.schedule_agent = importlib.import_module("kagg.search.schedule_agent")
    days = 3
    ours = B.run(heuristic.make_agent, lambda: (lambda o, t: rancher.agent(o)),
                 seed=11, weeds=0.0, stop_day=days + 1)
    tape = B.run(lambda: (lambda o, t: rancher.agent(o)),
                 lambda: (lambda o, t: rancher.agent(o)),
                 seed=11, weeds=0.0, stop_day=days + 1)

    out = tmp_path / "grid.csv"
    B.write_csv(str(out), ours, tape, days)
    rows = list(csv.DictReader(out.open()))

    assert len(rows) == days, "one row per day"
    assert rows[0]["day"] == "0"
    for column in rows[0]:
        if column == "day":
            continue
        assert column.startswith(KINDS), f"{column} does not say what kind of number it holds"
        assert column.endswith((".ours", ".tape", ".diff")), column
    # the triplet is complete for every field, so a reader can subtract without doing it by hand
    fields = {c.rsplit(".", 1)[0] for c in rows[0] if c != "day"}
    for field in fields:
        for side in ("ours", "tape", "diff"):
            assert f"{field}.{side}" in rows[0], f"{field} has no {side} column"


def test_no_csv_column_holds_a_market_order_count(tmp_path):
    """The standing constraint. `sell`, `buy_seed`, `buy_product`, `buy_animal`, `hire` and
    `buy_land` are the six the market settles, and every one of them must be under `fill.`."""
    from kagg.agents import heuristic, rancher

    B.schedule_agent = importlib.import_module("kagg.search.schedule_agent")
    ours = B.run(heuristic.make_agent, lambda: (lambda o, t: rancher.agent(o)),
                 seed=11, weeds=0.0, stop_day=2)
    out = tmp_path / "grid.csv"
    B.write_csv(str(out), ours, ours, 1)
    header = next(csv.reader(out.open()))

    for op in B.MARKET_FILL_OPS:
        offered = f"offered.{op.lower()}.ours"
        assert offered not in header, f"{offered} is a fill, not an offer"
    assert any(c.startswith("fill.sell.") for c in header)
    assert any(c.startswith("fill.hire.") for c in header)


def test_the_csv_diff_column_is_ours_minus_tape(tmp_path):
    from kagg.agents import heuristic, rancher

    B.schedule_agent = importlib.import_module("kagg.search.schedule_agent")
    ours = B.run(heuristic.make_agent, lambda: (lambda o, t: rancher.agent(o)),
                 seed=11, weeds=0.0, stop_day=3)
    tape = B.run(lambda: (lambda o, t: rancher.agent(o)),
                 lambda: (lambda o, t: rancher.agent(o)),
                 seed=11, weeds=0.0, stop_day=3)
    out = tmp_path / "grid.csv"
    B.write_csv(str(out), ours, tape, 2)
    rows = list(csv.DictReader(out.open()))
    differing = 0
    for row in rows:
        for column in row:
            if not column.endswith(".diff"):
                continue
            base = column[:-len(".diff")]
            assert (round(float(row[column]), 6)
                    == round(float(row[base + ".ours"]) - float(row[base + ".tape"]), 6)), column
            differing += 1 if float(row[column]) else 0
    assert differing, "the two columns were identical; the diff proved nothing"
