"""A town that cannot buy milk should not be stocked with ten cows.

`_herd_split`'s milk-poor branch is gated on `"YARN_STORE" not in _seen`:

    elif "YARN_STORE" not in _seen and _milk <= MILK_POOR_SHOP_COUNT:
        cow_t, sheep_t = MILK_POOR_COW, MILK_POOR_SHEEP

Whether WOOL has a buyer says nothing about whether MILK has one. So a town that
draws **zero** milk shops but any yarn store -- including one arriving at d15,
which the code's own `WOOL_SHOP_DRAW_LIMIT = 3` comment says the leader ignores --
falls straight through to `WOOL_SHOP_NO_YARN_COW = 10` and we stock the full herd
into a book with no drain.

Measured on the ladder, 2026-08-17: game `93849246` drew NO milk shop at all and we
ran COW 10 / SHEEP 4 anyway. Across six analysed losses we ran COW 10 / SHEEP 4 on
every board, at milk-shop counts of 0, 2, 3, 3, 3 and 5. The split never moved.
MILK floors at $1 with no drain, and a 5-seed mirror leaves COW 12 standing in the
field at the close in every single seed.

**What this test does NOT settle.** Cutting cows raises sheep, and `MILK_POOR_SHEEP`
is 6 -- but WOOL needs a yarn store, so on a town poor in BOTH the re-mix trades
unsold milk for unsold wool and banks nothing either way. The right answer there is
probably a SMALLER herd, not a different one. That is a separate decision and this
test deliberately does not encode it: it pins only that the milk decision must be
made on milk evidence.
"""
import importlib

import pytest

SA = importlib.import_module("kagg.search.schedule_agent")


def _split(unlocked, want=None, bought=None):
    """`_herd_split` on a fresh herd, so only the shop draw can move the answer."""
    return SA._herd_split(want or {"COW": 10, "SHEEP": 4},
                          bought or {}, day=6, hour=0, unlocked_shops=list(unlocked))


#: A milk shop, and a yarn store that lands far too late for the wool rule to want it.
#: `WOOL_SHOP_DRAW_LIMIT = 3` slices the first three draws, so anything at index 3+ is
#: outside the window the leader responds to.
LATE = ["GENERAL_STORE", "BAKERY", "BAKERY", "YARN_STORE"]


def test_the_milk_rule_reads_milk_shops_and_not_the_yarn_store():
    """The defect. Zero milk shops, one late yarn store: the milk rule must still fire."""
    milk_shops = [s for s in LATE if "MILK" in (SA._KG.SHOPS.get(s) or ())]
    assert not milk_shops, (
        f"this fixture is meant to have NO milk buyer, but {milk_shops} buys milk; "
        f"re-pick the shops before trusting the assertion below")
    assert "YARN_STORE" not in LATE[:SA.WOOL_SHOP_DRAW_LIMIT], (
        "the yarn store must land OUTSIDE the wool window, or the early-wool branch "
        "answers this instead and the test measures the wrong rule")

    got = _split(LATE)
    assert got["COW"] <= SA.MILK_POOR_COW, (
        f"the town draws no milk shop at all and we stocked COW {got['COW']}, because "
        f"`_herd_split`'s milk branch is gated on `\"YARN_STORE\" not in _seen` and a "
        f"single late yarn store sends it to WOOL_SHOP_NO_YARN_COW="
        f"{SA.WOOL_SHOP_NO_YARN_COW}. Whether wool sells is not evidence about milk.")


def test_a_milk_rich_town_still_gets_its_cows():
    """The other side, so the fix cannot be "always cut the cows"."""
    rich = ["ICE_CREAM_SHOP", "PIZZA_SHOP", "SMOOTHIE_SHOP"]
    n = sum(1 for s in rich if "MILK" in (SA._KG.SHOPS.get(s) or ()))
    assert n > SA.MILK_POOR_SHOP_COUNT, f"fixture is not milk-rich: only {n} milk buyers"
    got = _split(rich)
    assert got["COW"] >= SA.WOOL_SHOP_NO_YARN_COW, (
        f"a town with {n} milk buyers and no yarn store should carry the full cow "
        f"count, got COW {got['COW']}")
