"""The d13-d18 plant count is clamped to what a measured decision tree reads off the dawn board.

Source: docs/history/the_opening_is_a_tape_the_middle_is_two_regimes_2026-08-21.md. The season
grid measured -$11,544 against the tape with -89 standing wheat and +171 idle unit-turns, and the
over-planting concentrates in d13-d18 -- exactly where that doc's depth-3 tree predicts the day's
planting from four board features (+45/+42/+36/+13/+28/+23 points over baseline, d13 through d18).
From d19 the same tree is at chance, so the gate is hard: nothing outside 13 <= day <= 18 moves.

The tree is board-only on purpose. With `my_seed_*` features it reaches 98.4% on `my_seed_STRAWBERRY`
alone, but that seed was bought on d12 -- it would read a decision already paid for.

Each leaf names a crop family; the per-day budget is カワシギ's own row for that day
(`data/seed_scripts/kawashigi/schedule.json`, `plant_tiles`), filtered to that family:

                 d13 d14 d15 d16 d17 d18   total
    straw+wheat   8   4   3   2   1   0      18
    wheat         0   1   1   2   1   0       5
    straw         8   3   2   0   0   0      13

Applied as a CAP on the plan's `plants` row, once per day, in the day-change block of
`schedule_agent.make_agent` -- the same place the melon branch and the late-crop shifts rewrite
rows. Crops already in the ground are never touched: a cap can only shrink what is sown from
today onward, and a row already under its budget passes through unchanged.
"""

#: First/last day the clamp may fire. The doc is explicit that the signal is DEAD from d19.
CLAMP_FROM_DAY = 13
CLAMP_TO_DAY = 18

#: Master switch.
#:
#: **SHIPS OFF, measured 2026-08-24** (`scripts/tree_clamp_ab.py`, six seeds vs the unclamped
#: control on identical seeds, kawashigi tape opponent, shop draw injected): banking during the
#: window improves -- +$5,832 mean over d13-d18, positive on every seed -- but the SEASON pays for
#: it: -$4,496 mean at the close, negative on all six seeds (-$1,984 to -$8,811). The tiles the cap
#: keeps out of the ground in the window were going to pay later; the window saves seed and water
#: spend and loses more harvest than it saves. A null/negative result is written down and stopped,
#: not tuned away: no softer budget was swept.
TREE_CLAMP = False

#: Per-day planting budgets per leaf, read off his own d13-d18 rows (see module docstring).
BUDGETS = {
    "straw+wheat": {13: 8, 14: 4, 15: 3, 16: 2, 17: 1, 18: 0},
    "wheat":       {13: 0, 14: 1, 15: 1, 16: 2, 17: 1, 18: 0},
    "straw":       {13: 8, 14: 3, 15: 2, 16: 0, 17: 0, 18: 0},
}

#: What each leaf's family allows into the ground. `None` means everything his row names. Melon
#: rides with strawberry: no leaf names it, and it is sown in the same early-window days his
#: strawberry rows occupy.
REGIME_CROPS = {
    "straw+wheat": None,
    "wheat": ("WHEAT",),
    "straw": ("STRAWBERRY", "MELON"),
}


def dawn_features(tiles, shed):
    """The four board features, counted the way `breakdown.snap` counts them.

    `my_empty` is owned bare ground: cells that are neither LOCKED nor a dict. A WEED tile or a pen
    is occupied ground and does not count -- both are spoken for by other work either way.
    """
    my_empty = 0
    my_crop_strawberry = 0
    for row in tiles:
        for cell in row:
            if cell == "LOCKED":
                continue
            if not isinstance(cell, dict):
                my_empty += 1
            elif cell.get("kind") == "PLANT" and cell.get("crop") == "STRAWBERRY":
                my_crop_strawberry += 1
    return {
        "my_empty": my_empty,
        "my_shed_WHEAT": int(shed.get("WHEAT", 0) or 0),
        "my_shed_FERTILIZER": int(shed.get("FERTILIZER", 0) or 0),
        "my_crop_STRAWBERRY": my_crop_strawberry,
    }


def regime(feats):
    """The fitted depth-3 tree, thresholds verbatim from the source doc."""
    if feats["my_empty"] <= 5.5:
        if feats["my_shed_WHEAT"] <= 29.5:
            return "straw+wheat"
        if feats["my_shed_WHEAT"] <= 34.5:
            return "wheat"
        return "straw"
    if feats["my_crop_STRAWBERRY"] <= 41.5:
        return "straw+wheat" if feats["my_shed_FERTILIZER"] <= 24.5 else "straw"
    return "wheat"


def apply(sched, day, obs, me=0):
    """Cap today's `plants` row at the leaf's budget. Mutates the row IN PLACE, like every branch.

    Returns True when the row changed. False outside the window, when the switch is off, when the
    day has no row, or when the row was already inside its budget -- a cap never stretches a row up.
    """
    if not TREE_CLAMP or not (CLAMP_FROM_DAY <= day <= CLAMP_TO_DAY):
        return False
    farms = obs.get("farms") or []
    if len(farms) <= me:
        return False
    farm = farms[me]
    row = sched.get(day)
    if not row:
        return False
    priv = obs.get("private") or {}
    feats = dawn_features(farm["tiles"], priv.get("shed") or {})
    leaf = regime(feats)
    allowed = REGIME_CROPS[leaf]
    plants = list(row.get("plants") or [])
    if allowed is not None:
        plants = [c for c in plants if c in allowed]
    plants = plants[:BUDGETS[leaf][day]]
    if plants == list(row.get("plants") or []):
        return False
    row["plants"] = plants
    return True
