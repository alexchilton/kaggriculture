"""A test that changes a module-level global must put it back.

**This is why two files passed alone and failed under xdist.** `test_a_replayed_day_credits_what_
the_tape_planted` has a module-scoped fixture that sets

    SA.REPLAY_OPENING_DAYS = (4, 5, 6, 7, 8, 9, 10, 11)     # shipped value is tuple(range(30))
    MB.OPPONENT_MELON = 0                                    # shipped value is 9

and never restores either. Both are globals on imported modules, so every later test in the same
worker process saw an eight-day replay and a melon threshold that arms on any opponent at all.
Under `-n 0` the file runs last and nothing notices; under xdist the worker that picks it up
poisons whatever it is given next, and WHICH tests fail depends on the shard, so the same suite
gives different answers on different runs.

That is worse than a failing test. It is a suite whose result depends on scheduling, and this
project has already lost time to a correct number under an unstable label.

Run this file AFTER the polluting one to see it work:

    pytest tests/test_a_replayed_day_credits_what_the_tape_planted.py \
           tests/test_a_test_does_not_leave_a_global_changed_behind_it.py -n 0
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.search import melon_branch as MB                            # noqa: E402
from kagg.search import q4_branch as Q4                               # noqa: E402
from kagg.search import schedule_agent as SA                          # noqa: E402

#: The shipped values, written out rather than read from the module, because reading the module is
#: exactly what a polluted process gets wrong.
SHIPPED = (
    (SA, "REPLAY_OPENING_DAYS", tuple(range(30))),
    (MB, "OPPONENT_MELON", 9),
    (MB, "DECIDE_BY_DAY", 3),
    (Q4, "DECIDE_BY_DAY", 5),
)


def test_the_replay_span_is_still_the_whole_season():
    """The single most consequential global in the agent: it decides how many days are replayed."""
    assert SA.REPLAY_OPENING_DAYS == tuple(range(30)), (
        f"REPLAY_OPENING_DAYS is {SA.REPLAY_OPENING_DAYS!r}. An earlier test set it and did not "
        f"restore it, so every test after it in this process replayed a different season.")


def test_the_latch_thresholds_are_still_the_shipped_ones():
    """`OPPONENT_MELON = 0` arms the melon branch against every opponent, including a mirror."""
    for mod, name, want in SHIPPED[1:]:
        got = getattr(mod, name)
        assert got == want, (
            f"{mod.__name__}.{name} is {got!r}, shipped is {want!r}. An earlier test changed it "
            f"and left it changed.")


def test_no_test_file_assigns_a_module_global_outside_a_restore():
    """The general rule, checked by reading the tests rather than by running them.

    An assignment to `SA.SOMETHING` is only safe if the same file puts the old value back. This
    counts both and reports the files where they do not balance -- a heuristic, deliberately, since
    the alternative is an import-time sandbox nobody will maintain.
    """
    import collections                                                # noqa: PLC0415
    import re                                                         # noqa: PLC0415

    pat = re.compile(r"^\s*(SA|RT|MB|Q4|R|C)\.([A-Z_]{3,})\s*=", re.M)
    unbalanced = collections.OrderedDict()
    for p in sorted((REPO / "tests").glob("test_*.py")):
        if p.name == pathlib.Path(__file__).name:
            continue
        text = p.read_text(errors="ignore")
        if "monkeypatch" in text:
            continue                       # pytest restores those for us
        counts = collections.Counter(m.group(0).strip() for m in pat.finditer(text))
        # a global that is assigned an ODD number of times cannot have been set and restored
        odd = sorted(k for k, n in counts.items() if n % 2)
        if odd:
            unbalanced[p.name] = odd

    assert not unbalanced, "these files set a module global without restoring it:\n" + "\n".join(
        f"  {f}: {', '.join(k)}" for f, k in unbalanced.items())
