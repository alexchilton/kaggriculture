"""The rows file must have one field per header column.

**This crashed a 6,048-season run at the very end, having written nothing.** The header names
eleven columns and then appends one per drain key; the row format carried eleven `%` specifiers and
was handed twelve arguments, the twelfth being the joined drain values. Python raises
`TypeError: not all arguments converted during string formatting` -- but only when the LAST season
is done and the file is opened, so 1.7 hours of compute produced a traceback and no CSV.

The seasons themselves were fine. Nothing about the measurement was wrong. The run was lost to a
format string, which is the cheapest possible test to write and was not written.
"""
import sys
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import town_arm_grid as G                                              # noqa: E402


def test_the_row_has_one_field_per_header_column():
    drains = {p: i for i, p in enumerate(sorted(G.DRAIN_KEYS))}
    header = G.rows_header()
    row = G.rows_line(3, "yarn_early", "tt_straw_q4_128k", "Ryo Hasegawa", "top", 1,
                      "control", 11, 145_000, 132_000, 4, drains)

    assert header.endswith("\n") and row.endswith("\n"), "both lines must terminate"
    n_head, n_row = len(header.strip().split(",")), len(row.strip().split(","))
    assert n_head == n_row, (
        f"header names {n_head} columns, the row writes {n_row}. A CSV that does not line up is "
        f"read by column INDEX later and silently mis-attributes every value after the gap.")


def test_every_drain_key_reaches_the_row():
    """The drain vector is the axis the whole sweep conditions on, so a dropped key is fatal."""
    drains = {p: i + 1 for i, p in enumerate(sorted(G.DRAIN_KEYS))}
    fields = G.rows_line(0, "uniform", "t", "o", "low", 400, "a", 7, 1, 2, 3,
                         drains).strip().split(",")
    tail = fields[-len(G.DRAIN_KEYS):]
    assert tail == [str(i + 1) for i in range(len(G.DRAIN_KEYS))], (
        f"drain columns came out {tail}, expected 1..{len(G.DRAIN_KEYS)} in sorted-key order")


def test_a_comma_in_an_opponent_name_does_not_add_a_column():
    """Opponent names are free text off the leaderboard and one of them will contain a comma."""
    drains = dict.fromkeys(G.DRAIN_KEYS, 0)
    n_head = len(G.rows_header().strip().split(","))
    row = G.rows_line(0, "uniform", "t", "Smith, John", "low", 400, "a", 7, 1, 2, 3, drains)
    assert len(row.strip().split(",")) == n_head, (
        "a comma in the opponent name shifted every later column; it must be stripped or quoted")
