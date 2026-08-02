"""The staged curriculum's gate, and the ways an unguarded stage handover goes wrong silently.

Every case here pins a failure this project has already paid for, in the guise it would take on if
the schedule were driven stage by stage rather than by the anneal clock.

**The two flag bugs must be unrepresentable, not documented.** `--ent-coef 0` alongside `--kl-prior`
removes the regulariser entirely because the KL shares the entropy coefficient; that instruction was
in the help text, cost two runs via `--kl-coef`, was fixed there, and survived into `--kl-prior`
anyway. `--early-limit` non-zero with a curriculum truncates every early env on its first turn and
reports `wr nan` rather than an error. Both are cheap to raise on and expensive to re-diagnose, so
the builder raises.

**The gate must refuse a stage that only held its inheritance.** The trainee is seeded into the
richer seat by default, so a win rate above 0.5 is available for free and says nothing. The bank
against the seed day is the figure that cannot be inherited: `money_med` on the update-0 line is the
freshly-seeded bank, because every slot is seeded at that point.

**The gate must refuse a flat value gap.** That is the whole premise of walking the day back -- if
the critic cannot see the animal economy at day 25, it will not learn to at day 20, and the schedule
would advance on a clock into states that are strictly harder.

**A constant outcome must stop the ladder.** `terminal_ret_std` near zero is what 1,300 wasted
updates looked like, and it is invisible in a win rate, which reads 0.5 for "draws everything".
"""

import json

import pytest

from scripts import stage_curriculum as S


def _rows(n=250, bank_start=69_000.0, bank_end=72_000.0, ev=0.2, ent=11.5, tstd=0.5):
    """A plausible healthy stage log. Bank rises from the seed value, ev positive, outcomes varying."""
    return [{
        "update": i,
        "money_med": bank_start + (bank_end - bank_start) * i / max(1, n - 1),
        "ev_signal": ev, "entropy": ent, "win_rate": 0.55, "wr_farm": 0.4, "wr_idle": 0.6,
        "terminal_ret_std": tstd, "n_terminal": 150.0, "kl_prior": 0.2,
    } for i in range(n)]


# --------------------------------------------------------------------------- metrics


def test_seed_bank_is_the_first_line_not_the_lowest():
    """Update 0 is the only line on which every slot is freshly seeded.

    Taking the minimum instead would silently measure "the worst the policy ever got" and would
    report a gain whenever a stage dipped and recovered, which is not the same claim.
    """
    rows = _rows(n=50, bank_start=69_000.0, bank_end=72_000.0)
    rows[20]["money_med"] = 10_000.0            # a dip partway through
    m = S.stage_metrics(rows)
    assert m["seed_bank"] == pytest.approx(69_000.0)


def test_bank_gain_is_measured_against_the_seed_day():
    m = S.stage_metrics(_rows(bank_start=69_000.0, bank_end=72_000.0), tail=25)
    assert m["bank_gain"] > 0
    flat = S.stage_metrics(_rows(bank_start=69_000.0, bank_end=69_000.0), tail=25)
    assert flat["bank_gain"] == pytest.approx(0.0, abs=1.0)


def test_nan_and_missing_values_do_not_poison_the_averages():
    """`win_rate` is nan until the first episode terminates, and `ev_signal` until the critic has a
    target. A mean that propagates nan would make the gate unevaluable for reasons unrelated to the
    policy."""
    rows = _rows(n=30)
    rows[0].update({"win_rate": float("nan"), "ev_signal": float("nan"), "money_med": None})
    rows[1].pop("ev_signal")
    m = S.stage_metrics(rows, tail=30)
    assert m["win_rate"] == pytest.approx(0.55)
    assert m["ev_signal"] == pytest.approx(0.2)
    # money_med None on line 0 must not become the seed bank.
    assert m["seed_bank"] is not None


def test_a_half_written_trailing_line_is_skipped(tmp_path):
    """The trainer appends while running, so reading a live run can catch a partial write."""
    (tmp_path / "log.jsonl").write_text(
        json.dumps({"update": 0, "money_med": 1.0}) + "\n"
        + json.dumps({"update": 1, "money_med": 2.0}) + "\n"
        + '{"update": 2, "money_me')
    rows = S.load_rows(tmp_path)
    assert [r["update"] for r in rows] == [0, 1]


# --------------------------------------------------------------------------- gate


def test_a_healthy_stage_passes():
    passed, reasons, _w = S.gate(S.stage_metrics(_rows()), gap=0.12, prev_gap=0.08)
    assert passed, reasons


def test_a_flat_value_gap_holds_the_ladder():
    """The handoff's stated criterion: 'If it stays at +0.05, the schedule will regress and more
    days will not help.'"""
    passed, reasons, _w = S.gate(S.stage_metrics(_rows()), gap=0.05, prev_gap=0.05)
    assert not passed
    assert any("did not grow" in r for r in reasons)


def test_a_shrinking_value_gap_holds_the_ladder():
    passed, reasons, _w = S.gate(S.stage_metrics(_rows()), gap=0.03, prev_gap=0.12)
    assert not passed
    assert any("did not grow" in r for r in reasons)


def test_the_first_stage_has_no_baseline_and_is_allowed_through():
    """Refusing the first stage for not having grown would make the ladder unstartable."""
    passed, reasons, warnings = S.gate(S.stage_metrics(_rows()), gap=0.12, prev_gap=None)
    assert passed, reasons
    assert any("baseline" in w for w in warnings)


def test_an_inherited_position_is_refused_even_with_a_winning_win_rate():
    """The trainee is seeded into the richer seat, so 0.55 is free. A bank level with the seed day
    means the position was held rather than grown, and that is the failure the handoff names."""
    rows = _rows(bank_start=69_000.0, bank_end=69_000.0)
    for r in rows:
        r["win_rate"] = 0.62                     # comfortably winning, and irrelevant
    passed, reasons, _w = S.gate(S.stage_metrics(rows), gap=0.2, prev_gap=0.1)
    assert not passed
    assert any("inherited" in r for r in reasons)


def test_a_constant_outcome_holds_the_ladder():
    """terminal_ret_std near zero is what 1,300 updates of no gradient looked like, and a win rate
    cannot see it: 0.5 reads the same for 'wins half' and 'draws everything'."""
    passed, reasons, _w = S.gate(S.stage_metrics(_rows(tstd=0.02)), gap=0.2, prev_gap=0.1)
    assert not passed
    assert any("constant-outcome" in r for r in reasons)


def test_a_negative_ev_signal_holds_the_ladder():
    passed, reasons, _w = S.gate(S.stage_metrics(_rows(ev=-0.05)), gap=0.2, prev_gap=0.1)
    assert not passed
    assert any("critic is not learning" in r for r in reasons)


def test_too_few_updates_holds_the_ladder():
    passed, reasons, _w = S.gate(S.stage_metrics(_rows(n=40)), gap=0.2, prev_gap=0.1,
                                 min_updates=200)
    assert not passed
    assert any("updates" in r for r in reasons)


def test_a_missing_probe_cannot_pass():
    """`--skip-probe` is for a fast look, and the gate must not read its absence as success."""
    passed, reasons, _w = S.gate(S.stage_metrics(_rows()), gap=None, prev_gap=0.1)
    assert not passed
    assert any("value probe" in r for r in reasons)


def test_rising_entropy_warns_but_does_not_hold():
    """Entropy rising was the tell for the failure this work fixed, but it was measured oscillating
    11.3 -> 12.6 -> 11.3 on the healthy run, so a single rise must not stop a working schedule."""
    rows = _rows(n=250, ent=11.0)
    for r in rows[-25:]:
        r["entropy"] = 13.0
    passed, _r, warnings = S.gate(S.stage_metrics(rows), gap=0.2, prev_gap=0.1)
    assert passed
    assert any("erosion tell" in w for w in warnings)


# --------------------------------------------------------------------------- command guards


def test_ent_coef_zero_is_refused():
    """The bug that has now cost this project two runs twice over: the KL shares the coefficient."""
    with pytest.raises(ValueError, match="removes the regulariser"):
        S.build_command(20, prior="p.pkl", init="p.pkl", ent_coef=0)


def test_a_nonzero_early_limit_is_refused():
    """It truncates every early env on its first turn and reports `wr nan`, not an error."""
    with pytest.raises(ValueError, match="early-limit"):
        S.build_command(20, prior="p.pkl", init="p.pkl", early_limit=600)


def test_a_stage_without_a_prior_is_refused():
    """Re-anchoring is the entire reason this script exists rather than --curriculum-anneal."""
    with pytest.raises(ValueError, match="both --kl-prior and --init"):
        S.build_command(20, prior=None, init="p.pkl")


def test_the_command_reanchors_both_prior_and_init_to_the_same_checkpoint():
    cmd = S.build_command(20, prior="/r/data/x/latest.pkl", init="/r/data/x/latest.pkl")
    assert cmd[cmd.index("--kl-prior") + 1] == "/r/data/x/latest.pkl"
    assert cmd[cmd.index("--init") + 1] == "/r/data/x/latest.pkl"
    assert cmd[cmd.index("--curriculum-day") + 1] == "20"
    assert cmd[cmd.index("--early-limit") + 1] == "0"


def test_the_band_is_emitted_and_stays_off_the_low_end():
    """The $15-35k band puts 45 of 48 day-25 boards at 0-4 animals, which makes FEED illegal on
    almost every board and hands back the DIG/NOOP attractor."""
    cmd = S.build_command(20, prior="p", init="p")
    lo = float(cmd[cmd.index("--curriculum-min-bank") + 1])
    hi = float(cmd[cmd.index("--curriculum-max-bank") + 1])
    assert lo >= 35_000 and hi <= 70_000
    assert "--curriculum-min-bank" not in S.build_command(20, prior="p", init="p", band=None)


def test_behind_is_opt_in():
    assert "--curriculum-behind" not in S.build_command(20, prior="p", init="p")
    assert "--curriculum-behind" in S.build_command(20, prior="p", init="p", behind=True)


# --------------------------------------------------------------------------- ladder


def test_the_ladder_walks_down_in_five_day_steps_and_ends_at_zero():
    days, day = [], 25
    while day is not None:
        days.append(day)
        day = S.next_day(day)
    assert days == [25, 20, 15, 10, 5, 0]


def test_day_zero_is_the_last_rung():
    assert S.next_day(0) is None


def test_an_off_ladder_day_falls_to_the_next_rung_below():
    """A run launched at day 23 by hand should still be able to hand over, rather than crash."""
    assert S.next_day(23) == 20
    assert S.next_day(1) == 0


# --------------------------------------------------------------------------- remote paths


def test_a_local_run_path_maps_onto_the_box_keeping_the_data_segment():
    """The first version of this dropped `data/` and emitted
    `/home/alex/kagg/jax_rl_runs/...`, which does not exist on the box. A run launched against it
    dies on startup, so it is loud -- but the same slip one level up would anchor the next stage to
    the wrong checkpoint and look like a working handover."""
    got = S.remote_path("data/jax_rl_runs/ppo-20260802-091956/latest.pkl", "/home/alex/kagg")
    assert got == "/home/alex/kagg/data/jax_rl_runs/ppo-20260802-091956/latest.pkl"


def test_an_absolute_local_path_still_maps_on_the_data_segment():
    got = S.remote_path("/Users/x/proj/data/jax_rl_runs/r/latest.pkl", "/home/alex/kagg")
    assert got == "/home/alex/kagg/data/jax_rl_runs/r/latest.pkl"


def test_a_trailing_slash_on_the_root_does_not_double_up():
    assert S.remote_path("data/x/latest.pkl", "/home/alex/kagg/") == \
        "/home/alex/kagg/data/x/latest.pkl"


def test_a_path_with_no_data_segment_is_passed_through_not_guessed_at():
    """Guessing would risk a plausible-but-wrong path, which is the failure that hides."""
    assert S.remote_path("/opt/models/bc.pkl", "/home/alex/kagg") == "/opt/models/bc.pkl"


# --------------------------------------------------------------------------- state file


def test_the_previous_gap_is_the_last_recorded_one(tmp_path):
    path = tmp_path / "stages.json"
    S.write_state({"stages": [{"day": 25, "value_gap": 0.11}, {"day": 20, "value_gap": 0.19}]}, path)
    assert S.previous_gap(S.read_state(path)) == pytest.approx(0.19)


def test_a_stage_recorded_without_a_gap_is_skipped_when_looking_back(tmp_path):
    """`--skip-probe` can record a stage with no gap. That must not read as a baseline of None-is-0
    and let the next stage through on nothing."""
    path = tmp_path / "stages.json"
    S.write_state({"stages": [{"day": 25, "value_gap": 0.11}, {"day": 20, "value_gap": None}]}, path)
    assert S.previous_gap(S.read_state(path)) == pytest.approx(0.11)


def test_a_missing_state_file_reads_as_no_stages(tmp_path):
    assert S.previous_gap(S.read_state(tmp_path / "nope.json")) is None
