"""`rank_seats` must be able to return one named teacher's seats, not just the richest ones.

`scripts/bc_replay.py` ranks every seat on disk by final bank. That is the right criterion when the
question is "clone the best play available", and the wrong one when the question is Alex's:
*"why do we not do entity transformer, full per-tile board for the kawa tapes"* -- which needs
カワシギ's seats and Crop Dusta's seats trained SEPARATELY, so the two clones can be compared.

Three things are pinned here, and the second is not hypothetical:

1. A team filter exists, and selects the named SEAT rather than the whole replay. A replay has two
   seats and only one is the teacher; taking both trains on the opponent as well.
2. It matches a name Kaggle stored JSON-escaped. `カワシギ` is written `\\u30ab\\u30ef\\u30b7\\u30ae`,
   and the identical mistake in `emit_dusta_bc_dataset.py` made the archive scan report `0 games`
   for him earlier today -- a broken filter that reads exactly like an empty archive. These tests
   write their fixtures with `json.dump`'s default `ensure_ascii=True`, so the escaping is real
   rather than assumed.
3. A cache entry written before `teams` existed is REFRESHED, not treated as a non-match. Silently
   dropping every pre-existing entry would report "0 seats" for a teacher we have 387 games of.
"""
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


def _replay(tmp, name, teams, banks):
    """The smallest file `replays.replay_summary` accepts, written the way Kaggle writes them."""
    p = tmp / name
    p.write_text(json.dumps({
        "info": {"TeamNames": list(teams), "EpisodeId": 1, "seed": 1},
        "steps": [[{"reward": float(b)} for b in banks]],
    }))                                   # ensure_ascii=True by default -- カワシギ comes out escaped
    return p


def test_the_fixture_really_is_escaped(tmp_path):
    """Guards the two tests below from passing for the wrong reason."""
    p = _replay(tmp_path, "a.json", ["カワシギ", "Yusuke Hayashi"], [120, 90])
    assert "カワシギ" not in p.read_text()
    assert "\\u30ab\\u30ef\\u30b7\\u30ae" in p.read_text()


def test_rank_seats_returns_only_the_named_teachers_seat(tmp_path):
    from kagg.il import bc

    a = _replay(tmp_path, "a.json", ["カワシギ", "Yusuke Hayashi"], [120, 90])
    b = _replay(tmp_path, "b.json", ["Crop Dusta", "カワシギ"], [50, 140])
    got = bc.rank_seats([a, b], cache=tmp_path / "idx.json", team="カワシギ")
    assert [(pathlib.Path(r.path).name, r.seat) for r in got] == [("b.json", 1), ("a.json", 0)], \
        "must pick the named seat in each replay, richest first"


def test_the_other_teacher_is_selectable_from_the_same_replays(tmp_path):
    from kagg.il import bc

    a = _replay(tmp_path, "a.json", ["カワシギ", "Yusuke Hayashi"], [120, 90])
    b = _replay(tmp_path, "b.json", ["Crop Dusta", "カワシギ"], [50, 140])
    got = bc.rank_seats([a, b], cache=tmp_path / "idx.json", team="crop dusta")
    assert [(pathlib.Path(r.path).name, r.seat) for r in got] == [("b.json", 0)]


def test_no_team_filter_still_returns_every_seat(tmp_path):
    """The existing behaviour must not move -- bc_replay's default path uses it."""
    from kagg.il import bc

    a = _replay(tmp_path, "a.json", ["カワシギ", "Yusuke Hayashi"], [120, 90])
    assert len(bc.rank_seats([a], cache=tmp_path / "idx.json")) == 2


def test_a_team_filter_composes_with_the_bank_band(tmp_path):
    from kagg.il import bc

    a = _replay(tmp_path, "a.json", ["カワシギ", "x"], [120, 90])
    b = _replay(tmp_path, "b.json", ["カワシギ", "x"], [10, 5])
    got = bc.rank_seats([a, b], cache=tmp_path / "idx.json", team="カワシギ", min_bank=100.0)
    assert [pathlib.Path(r.path).name for r in got] == ["a.json"]


def test_a_cache_entry_written_before_teams_existed_is_refreshed(tmp_path):
    """`data/replay_index.json` on disk has hundreds of entries with no `teams` key. If a missing
    key counted as "not this team", the first team-filtered run would report zero seats."""
    from kagg.il import bc

    a = _replay(tmp_path, "a.json", ["カワシギ", "Yusuke Hayashi"], [120, 90])
    st = a.stat()
    idx = tmp_path / "idx.json"
    idx.write_text(json.dumps({str(a): {"size": st.st_size, "mtime": int(st.st_mtime),
                                        "rewards": [120.0, 90.0]}}))      # no "teams"
    got = bc.rank_seats([a], cache=idx, team="カワシギ")
    assert [(pathlib.Path(r.path).name, r.seat) for r in got] == [("a.json", 0)]
    assert "teams" in json.loads(idx.read_text())[str(a)], "the refresh must be written back"


def test_replays_in_subdirectories_are_found(tmp_path):
    """`find_replays` promises "every downloaded episode replay under `root`" and globbed only the
    top level, so it saw 336 files while 2,814 sat in `data/seed_scripts/*/` -- every kawa and
    Dusta game among them. A teacher-filtered clone cannot work until this does."""
    from kagg.il import bc

    (tmp_path / "seed_scripts" / "kawashigi").mkdir(parents=True)
    _replay(tmp_path, "111.json", ["a", "b"], [1, 2])
    _replay(tmp_path / "seed_scripts" / "kawashigi", "222.json", ["カワシギ", "b"], [3, 4])
    found = {pathlib.Path(p).name for p in bc.find_replays(tmp_path)}
    assert found == {"111.json", "222.json"}, f"nested replay missed: {found}"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
