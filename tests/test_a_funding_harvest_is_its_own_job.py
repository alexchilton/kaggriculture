"""A ripe pen the day's row is waiting on offers its HARVEST as a SEPARATE job.

`Job` is one tile and every op that tile wants, atomic to one hand.  That is right for ordinary
work and it is what makes the tape's day-8 plan INEXPRESSIBLE for us.  He splits a ripe pen across
two hands -- one tends it, another does nothing but harvest and run the milk to the shed:

    his u0   h03 (4,3) FEED   h04 (4,3) CARE   h05 (4,3) COLLECT_FERT    <- never harvests it
    his u2   h04 HARVEST                        h06 (4,4) PLACE/MILK      <- harvest only, then banks

Ours bundles them, so the harvest is structurally forced to happen FOURTH:

    (3,4)  ['FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST']  4t

Our day-8 dawn, seed 11: bank $4, shed WHEAT 1 / FERTILIZER 7, and ZERO hands -- all eleven are
hired during the day.  Ripe cows at (3,4) and (4,4); shed-access tiles are (4,4), (4,5), (5,4),
(5,5), so (4,4) is both a ripe cow and shed ground.

Cow A is already banked at h03.  Cow B at (3,4) cannot be: even as job 0 on a hand that spawns at
the shed at h01, four bundled ops put the harvest at ~h06 and the deposit at ~h08, against a sale
his row asks at h05.  **No reordering or route-pinning can beat that**, which is why hardcoding the
visit sequence into `SOLVED_DAYS` changed nothing -- the constraint is inside one job, not between
jobs.  Split, the same hand does `NORTH, HARVEST, SOUTH, PLACE` and lands at h05.

The tending job keeps `needs` (the wheat a FEED eats), `at_risk`, and therefore `required` --
`REQUIRED_OPS` is `("FEED",)`, so the harvest-only job is correctly neither required nor at risk.

See `SPLIT_THE_FUNDING_HARVEST`.
"""
import importlib

import pytest

DP = importlib.import_module("kagg.search.cover")


@pytest.fixture(autouse=True)
def _flag(monkeypatch):
    monkeypatch.setattr(DP, "SPLIT_THE_FUNDING_HARVEST", True)


def _pen(tile, ripe=True, at_risk=False):
    ops = [("FEED", "WHEAT"), ("CARE", None), ("COLLECT_FERTILIZER", None)]
    gives = {"FERTILIZER": 1}
    products = set()
    if ripe:
        ops.append(("HARVEST", None))
        gives = {"FERTILIZER": 1, "MILK": 6}
        products = {"MILK"}
    return DP.Job(tile, ops, needs={"WHEAT": 1}, gives=gives, at_risk=at_risk,
                  products=frozenset(products))


def _split(jobs, wanted):
    return DP.split_funding_harvest(jobs, wanted)


def _by_ops(jobs, tile):
    return {tuple(o for o, _i in j.ops): j for j in jobs if j.tile == tile}


def test_the_ripe_pen_offers_its_harvest_separately():
    out = _split([_pen((3, 4))], {"MILK": 12})
    got = _by_ops(out, (3, 4))
    assert ("HARVEST",) in got, (
        "the harvest is still bundled, so it cannot go to a second hand\n"
        f"  jobs: {[[o for o, _i in j.ops] for j in out]}"
    )
    assert ("FEED", "CARE", "COLLECT_FERTILIZER") in got, (
        f"the tending ops were lost\n  jobs: {[[o for o, _i in j.ops] for j in out]}"
    )


def test_the_harvest_job_carries_the_produce_and_the_tending_job_does_not():
    out = _split([_pen((3, 4))], {"MILK": 12})
    got = _by_ops(out, (3, 4))
    h, r = got[("HARVEST",)], got[("FEED", "CARE", "COLLECT_FERTILIZER")]
    assert h.gives.get("MILK") == 6, f"harvest job lost its yield: {dict(h.gives)}"
    assert not r.gives.get("MILK"), f"tending job still claims the milk: {dict(r.gives)}"
    assert r.gives.get("FERTILIZER") == 1, (
        f"the collect's fertilizer went with the wrong job: {dict(r.gives)}")


def test_the_tending_job_keeps_the_feed_and_stays_required():
    """The feed is what keeps the animal alive; splitting must not weaken it."""
    out = _split([_pen((3, 4), at_risk=True)], {"MILK": 12})
    got = _by_ops(out, (3, 4))
    h, r = got[("HARVEST",)], got[("FEED", "CARE", "COLLECT_FERTILIZER")]
    assert r.needs.get("WHEAT") == 1 and r.required and r.at_risk, (
        f"tending job: needs={dict(r.needs)} required={r.required} at_risk={r.at_risk}")
    assert not h.required and not h.at_risk, (
        f"harvest job wrongly marked required/at_risk: {h.required}/{h.at_risk}")


def test_a_pen_the_row_is_not_waiting_on_is_left_whole():
    """Only the produce the day is SELLING justifies a second hand walking there."""
    out = _split([_pen((3, 4))], {"WHEAT": 20})
    assert len(out) == 1 and len(out[0].ops) == 4, (
        f"split a pen the row does not sell\n  jobs: {[[o for o, _i in j.ops] for j in out]}")


def test_a_pen_with_nothing_ripe_is_left_whole():
    out = _split([_pen((3, 4), ripe=False)], {"MILK": 12})
    assert len(out) == 1, f"split a pen holding nothing: {[j.ops for j in out]}"
