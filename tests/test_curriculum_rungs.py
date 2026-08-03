"""Rung bookkeeping: synthetic-rung weighting, the two mix parsers, and the day-0 window.

Three separate defects found in the 2026-08-03 sweep, all in code that P7 (deploying the chain
rung) is about to depend on:

- the synthetic rung `-1` was length-weighted as a **31-day** episode when `chain_states` produces a
  ~5-day one, so it received 6.2x the slots its requested share called for;
- `parse_mix` accepted `-1` behind the `length:` prefix and rejected it in the plain form, so the
  two parsers disagreed about the key space;
- `_turn_indices(n, 0)` returned `(1, 48)` -- turn 0 unreachable, and the median landing in game-day
  1 rather than day 0.
"""

import numpy as np
import pytest

from kagg.rl import curriculum as C
from kagg.sim import jax_sim as J

TPD = J.TURNS_PER_DAY


# ---- B3: the synthetic rung's episode length --------------------------------------------------


def test_chain_rung_start_day_is_a_shared_constant():
    """The weighting and `chain_states`' default must not be able to drift apart."""
    import inspect

    default = inspect.signature(C.chain_states).parameters["start_day"].default
    assert C.SYNTHETIC_START_DAY[-1] == default == C.CHAIN_START_DAY


def test_synthetic_rung_is_weighted_by_its_real_length():
    """**The bug.** `-1` is a day-25-length episode and was weighted as a 31-day one.

    Self-evidencing: rung `-1` and rung `25` produce episodes of identical length and here request
    an identical 0.1 share, so they cannot correctly receive different slot allocations. Measured
    before the fix, `-1` got 0.1286 of slots against day 25's 0.0207 -- 6.2x.
    """
    mix = C.length_weighted_mix({0: 0.6, -1: 0.1, 15: 0.1, 20: 0.1, 25: 0.1})
    assert mix[-1] == pytest.approx(mix[25], rel=1e-9), (
        f"rung -1 got {mix[-1]:.4f} of slots against day 25's {mix[25]:.4f} for the same "
        f"requested share and the same episode length")


def test_synthetic_rung_delivers_the_requested_episode_share():
    """Episodes arrive as `slots / length`, so equal shares must come out equal after the divide."""
    mix = C.length_weighted_mix({0: 0.5, -1: 0.25, 25: 0.25})
    length = {d: (30 - C.SYNTHETIC_START_DAY.get(d, d)) for d in mix}
    episodes = {d: mix[d] / length[d] for d in mix}
    total = sum(episodes.values())
    assert episodes[-1] / total == pytest.approx(0.25, abs=1e-9)
    assert episodes[25] / total == pytest.approx(0.25, abs=1e-9)
    assert episodes[0] / total == pytest.approx(0.50, abs=1e-9)


# ---- B4: the two parsers must agree about the key space ---------------------------------------


def test_plain_mix_rejects_synthetic_rungs_but_says_why():
    """**The rejection is deliberate and stays**, contra the first reading of this as a bug.

    A synthetic rung's defect is that its key is not its episode length, so it only means anything
    once length weighting is applied -- which is what the `length:` prefix turns on. Accepting
    `-1:0.1` in the plain form would hand it a raw *slot* share and reintroduce B3's mis-allocation
    from the other side. `test_a_day_outside_the_season_is_refused` already pinned this; what was
    missing was the message telling the caller which spelling to use.
    """
    with pytest.raises(ValueError, match="outside the season"):
        C.parse_mix("-1:0.5,0:0.5")
    with pytest.raises(ValueError, match="length:"):
        C.parse_mix("-1:0.5,0:0.5")
    assert C.parse_mix("length:-1:0.5,0:0.5")[-1] > 0


def test_plain_mix_rejects_a_real_out_of_range_day_without_the_hint():
    with pytest.raises(ValueError, match="outside") as exc:
        C.parse_mix("30:0.5,0:0.5")
    assert "length:" not in str(exc.value), "day 30 is not a synthetic rung; no hint applies"
    with pytest.raises(ValueError, match="outside"):
        C.parse_mix("-2:0.5,0:0.5")


# ---- B6 / P5: the day-0 window ---------------------------------------------------------------


def test_turn_zero_is_reachable():
    """**The bug.** `lo = max(1, ...)` meant turn 0 could never be drawn for any day."""
    lo, _hi = C._turn_indices(720, 0)
    assert lo == 0, "turn 0 -- the only true game start on disk -- was unreachable"


def test_day_zero_window_stays_inside_day_zero():
    """The requested day must remain the *centre* of the window after the low-side clip.

    Before: `(1, 48)`, median turn 24, which is game-day 1 -- and the handoff measured that rung
    starting on $476 with 7 units, a full game-day of play already spent.
    """
    lo, hi = C._turn_indices(720, 0)
    median_turn = (lo + hi) // 2
    assert median_turn // TPD == 0, (
        f"median turn {median_turn} is game-day {median_turn // TPD}, not day 0")
    assert hi <= TPD, f"the day-0 window reaches turn {hi}, inside game-day {hi // TPD}"


@pytest.mark.parametrize("day", [1, 5, 10, 15, 20, 25])
def test_interior_days_are_centred_and_unchanged(day):
    """The fix must not move any day that was already correct."""
    lo, hi = C._turn_indices(720, day)
    assert lo == (day - C.DAY_WINDOW) * TPD
    assert hi == (day + C.DAY_WINDOW + 1) * TPD
    assert ((lo + hi) // 2) // TPD == day


def test_a_recording_too_short_for_the_day_still_signals_unavailable():
    """`states_at_day` skips a replay on `hi <= lo`, so a short recording must keep returning that.

    Clamping `lo` here would destroy the caller's rejection signal and silently hand back day-25
    turns for a day-29 request.
    """
    lo, hi = C._turn_indices(600, 29)
    assert hi <= lo, "a 600-step recording must not satisfy a day-29 request"


# ---- B5: `virgin` must not discard a legitimately seeded first episode ------------------------


def _load_trainer():
    import importlib.util
    import pathlib

    path = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "train_jax_rl.py"
    spec = importlib.util.spec_from_file_location("train_jax_rl_rungs", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_virgin_is_only_for_staggered_states():
    """`virgin` exists because `staggered_states` starts mid-season on an EMPTY board -- an
    inconsistent position whose terminal reward is an artifact. A curriculum-seeded board is a real
    recorded position (or `J.reset` at turn 0 for the day-0 rung), so its first episode is a genuine
    result and must be paid. It was being suppressed on every process start and every `--resume`.
    """
    trainer = _load_trainer()
    assert trainer.initial_virgin(seeded=False) is True
    assert trainer.initial_virgin(seeded=True) is False


# ---- B2: `--n-phases` is inert under a curriculum, and must say so ---------------------------


def test_per_group_dead_code_is_gone():
    """`per_group = batch // n_phases` was assigned and never read."""
    import pathlib

    src = (pathlib.Path(__file__).resolve().parent.parent
           / "scripts" / "train_jax_rl.py").read_text()
    assert "per_group" not in src, "dead per_group assignment is still present"


def test_curriculum_overrides_phase_staggering_loudly(capsys):
    """A flag that silently does nothing gives a false model of what is running.

    `state = staggered_states(...)` at startup is overwritten by `state = seed_states` whenever a
    curriculum is set, so `--n-phases` stops controlling episode-start staggering entirely -- while
    the evening handoff listed it as an active mitigation for P1.
    """
    trainer = _load_trainer()
    trainer.warn_if_phases_inert(n_phases=12, seeded=True)
    out = capsys.readouterr().out
    assert "n-phases" in out and "curriculum" in out.lower()
    trainer.warn_if_phases_inert(n_phases=12, seeded=False)
    assert capsys.readouterr().out == ""
