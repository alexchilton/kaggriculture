"""The dawn bank, day by day, as the contract. Alex's call, and it is the right unit of measurement.

Every other number we have chased -- tiles, hands, animals, fertilizer ops -- is downstream of one
thing: **how much money the farm holds at each dawn.** A BUY_ANIMAL on an empty bank is a silent
no-op (`_do_buy_animal`), a BUY_LAND on an empty bank is a silent no-op (`_do_buy_land`), and a HIRE
on an empty bank is a silent no-op (`_do_hire`). So a plan that is broke does not fail loudly; it
quietly stops being the plan we wrote, and the census afterwards reports a farm nobody designed.

The two curves, measured. His off `data/seed_scripts/new_leader/90016067.json`, ours off
`scripts/measure_bank_curve_and_fertilizer.py` playing the leader-shaped fixture in the real
environment:

        day        HIS        OURS
          0     $3,000      $3,000
          1     $   42      $1,187     <- he is all-in; we are not
          2     $  141      $  935
          3     $  217      $  970
          4         --      $   43     <- and yet we are broke by day 4
          5     $  621      $  303
          7     $1,719      $   50
         10     $1,278      $  572
         11     $3,236      $  595
         12     $6,828      $1,055
         13    $14,622      $1,685     <- his inflection; we have none

Read together those two facts are not the same story I had been telling. We are **not** failing to
spend -- we end day 0 holding $1,187 he does not hold. We are failing to *earn*, and then spending
anyway, so days 4-13 run at a bank near zero where every order silently no-ops. He starts poorer and
compounds; we start richer and stall.

**Fertilizer is what makes his day 0 survivable, and it is load-bearing for us too.** Measured four
ways on the same plan:

        sell all, apply none          $28,816     the fixture today
        sell all, buy some back       $21,018     -$7,798, ~= 76 units at the $100 ask
        hold and apply (self-supply)  $     0     the farm dies
        hold and never use            $     0     the farm dies

So the day-1 fertilizer income is not an optimisation, it is the farm's only revenue before milk on
day 8, and diverting it to the crops kills the plan outright at our herd size. He can divert a third
of his (318 collected, 107 applied, 445 offered) because he has the volume; we cannot, yet.

These tests are the contract. They are meant to be red until the plan is solvent.
"""

import sys

import numpy as np
import pytest

from kagg.search import routines as R

sys.path.insert(0, "scripts")

# Every test here plays whole seasons in the real `kaggle_environments`, which is what the mark is for.
# The crew-cost contract that does NOT need an environment lives in
# `tests/test_the_crew_bill_must_not_dwarf_the_farm.py` and runs in 3s, deliberately.
pytestmark = pytest.mark.slow

# His dawn bank, off the tape. Blank days are ones the trace does not pin.
HIS_BANK = {0: 3000, 1: 42, 2: 141, 3: 217, 5: 621, 7: 1719, 10: 1278,
            11: 3236, 12: 6828, 13: 14622}

# The days that decide the season. Before day 8 there is no milk, so this window is funded by
# fertilizer and crops alone -- it is exactly where our curve flatlines.
EARLY = range(1, 11)


def _plan(**policy):
    from measure_bank_curve_and_fertilizer import leader_shaped_plan
    return leader_shaped_plan(**policy)


def _play(script):
    from measure_bank_curve_and_fertilizer import play_with_curve
    return play_with_curve(script, "starter")


@pytest.fixture(scope="module")
def baseline():
    """One real-environment game of the leader-shaped plan. Module-scoped: it takes ~20s and every
    test here reads a different property of the same curve."""
    script, used, refused = _plan(sell_fertilizer=True, fertilize=False, buy_fertilizer=False)
    final, theirs, curve, realised = _play(script)
    return dict(script=script, used=used, refused=refused, final=final,
                curve=curve, realised=realised)


# ------------------------------------------------------------------ the curve itself
def test_the_farm_is_never_broke_before_milk_arrives(baseline):
    """A bank at zero is not thrift, it is a plan that has stopped executing.

    Every purchase op in the reference checks `farm["money"] < cost` and returns silently. So the
    real cost of being broke on day 4 is not the missing $43 -- it is that the animals, land and
    hands scheduled for days 4-10 never happen, and nothing says so.
    """
    floor = min(baseline["curve"][d] for d in EARLY if d in baseline["curve"])
    assert floor >= 200, (
        f"the bank bottoms out at ${floor:,.0f} in days {EARLY.start}-{EARLY.stop - 1}; every order "
        f"scheduled at that dawn silently no-ops")


def test_the_bank_compounds_through_the_second_week(baseline):
    """His inflection is days 11-13: $3,236 -> $6,828 -> $14,622, better than doubling daily.

    That is what a farm looks like when capacity bought early is earning. A curve that crawls has
    capacity that never came online -- which is the same defect as the test above, one week later.
    """
    curve = baseline["curve"]
    assert curve.get(13, 0) > 4 * max(curve.get(10, 1), 1), (
        f"day 10 ${curve.get(10, 0):,.0f} -> day 13 ${curve.get(13, 0):,.0f}: no compounding. His "
        f"$1,278 -> $14,622 over the same three days is 11x")


def test_day_zero_is_spent_not_banked(baseline):
    """He ends day 0 on $42 of $3,000. Cash held at dawn on day 1 is capacity not bought.

    This is the one test here that our plan could pass by simply ordering more, which is why it is
    stated as a ceiling and not a target: holding $1,187 through the day the board is cheapest is
    the most expensive idle money in the season.
    """
    day1 = baseline["curve"].get(1)
    assert day1 is not None, "no day-1 reading; the harness did not run"
    assert day1 < 400, (
        f"we end day 0 holding ${day1:,.0f} against his $42 -- roughly a cow and a half of unbought "
        f"capacity, on the day it compounds for the longest")


# ------------------------------------------------------------------ what we own, not what we ordered
def test_the_herd_we_ordered_is_the_herd_we_own(baseline):
    """Ordered vs realised, which a broke plan silently divorces.

    Measured before: 16 animals ordered, and the farm owned 8. The plan on paper and the farm in the
    game were different farms, and every downstream census described the second one.
    """
    ordered = int(np.asarray(baseline["script"].arrays()["buy_animal"]).sum())
    owned = max(a for a, _p, _h in baseline["realised"].values())
    assert owned >= ordered - 1, (
        f"ordered {ordered} animals, ever owned {owned}: {ordered - owned} BUY_ANIMAL orders hit an "
        f"empty bank and no-oped")


def test_the_herd_reaches_his_fourteen_by_day_ten(baseline):
    """His measured ramp: 4 on day 0, then +2, +1, +4, +1, +2 to 14 by day 10.

    Stated as a date and not a count, because buying 14 at once is insolvent -- that was measured
    too. The ramp is the point.
    """
    owned_d10 = baseline["realised"].get(10, (0, 0, 0))[0]
    assert owned_d10 >= 14, f"day 10 herd is {owned_d10}, his is 14"


def test_four_animals_exist_on_day_zero(baseline):
    """The first rung of the ramp, and the one `ranch()` could not express until `build_every`.

    One chain of four pens raises one pen a day, so its fourth animal arrives on day 3. Four chains
    of one buy four animals on day 0 for the same four hands.
    """
    owned = baseline["realised"].get(1, (0, 0, 0))[0]
    assert owned >= 4, f"only {owned} animals exist at dawn on day 1; his tape shows 4 bought on day 0"


# ------------------------------------------------------------------ fertilizer, priced not assumed
def test_selling_the_herds_fertilizer_is_what_funds_the_early_season(baseline):
    """Not a claim about yield -- a claim about solvency, and it is the strong one.

    Withholding the herd's output to dose the crops instead banks **$0**: the farm loses its only
    revenue before milk on day 8 and never recovers. So `sell_fertilizer` is not a free parameter for
    the search to sweep at our herd size; it is the plan's working capital.
    """
    script, _u, _r = _plan(sell_fertilizer=False, fertilize=True, buy_fertilizer=False)
    final, _theirs, curve, _realised = _play(script)
    assert final > 0, (
        "holding the fertilizer banks $0 -- expected, and the reason it must not be swept blindly")


def test_buying_fertilizer_back_off_the_market_never_pays(baseline):
    """The farm trading with itself, paying the spread twice.

    `ranch(sell_fertilizer=True)` sells every unit it collects and `grow(buy_fertilizer=True)` buys
    units back at the $100 ask to dose the same farm's crops. Measured: -$7,798 for 76 applications,
    which is the ask almost to the dollar. Strawberry doubling cannot pay $100 a tile-dose at this
    scale, so if fertilizer is ever applied it has to come from the herd -- and that means having
    enough herd to spare it.
    """
    script, _u, _r = _plan(sell_fertilizer=True, fertilize=True, buy_fertilizer=True)
    final, _theirs, _curve, _realised = _play(script)
    assert final >= baseline["final"], (
        f"buying fertilizer back costs ${baseline['final'] - final:,.0f}; it must not be reachable "
        f"as a default in the genome")