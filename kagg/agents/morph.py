"""Us, parametrised. One family of opponents, all built from our own shipped agent.

## The idea

Alex, 2026-08-24: *"start with 'us' then create copies of us which do differing amounts of whatever
via params, and one of those params will morph us into mr carrot -- some will be mr flippit and some
will maybe even be mr spaghetti. We will beat it still on most towns or behaviours, but not all."*

That is the right shape and it fixes two failures at once.

**Why our own agent and not a heuristic.** The pool's nine heuristics lose to the planner by
$166k-174k whatever their dials are set to, so no configuration of them reproduces a loss. Measured
2026-08-24, first attempt at a carrot opponent: `heuristic(filler_crop=CARROT, hold_days=6)` held 66
units, carrot never left $23-28, and we won by $166,256. A weak agent cannot pose a hard question.

**Why parametrised rather than hand-written.** Every sweep this project has run measured arms the
opponent field could not express. `CARROT_OPP_MAX = 7` shipped off 12,096 seasons in which six of
nine arms were identical by construction, because not one pool member ever withheld stock --
`docs/carrot_refine_2026-08-22.md` says so in its own conclusions. And the gate has read `94.4%`
for weeks because `(8 * 1.0 + 0.5) / 9` is exactly that: an identity, not a measurement.

## The axes, and what each one is for

    hinge_crop      which book to corner, or None for "play normally"
    swap_from       first day the planner's own PLANT WHEAT is rewritten to that crop
    swap_to         last such day
    release_day     the day withheld stock is finally sold
    withhold        products not sold at all before `release_day`
    floor_price     stop selling any product quoted below this (the cadence axis -- it is what
                    stops us flooding milk to $1 by d13, and it is orthogonal to the hinge)

`hinge_crop=None, floor_price=0` is **exactly our shipped agent** and is the origin of the space.
Every other point is a measured distance from it.

## What has to be true for a cell to beat us

The hinge (`reference/kaggriculture.py:61-73`, `HINGE_GAIN = 8.0`) is convex in the town's
*inventory deficit*, not in how much anyone holds. CARROT is `base 35, T 450, below_target 1.00`.
Price runs away only once the town's stock has been drained past `T` and nobody replenishes it.

So a cell wins only if it **abstains from the book early, converts ground late, and withholds**.
A cell that grows its hinge crop from day one supplies its own book, keeps it under the knee, and
is a null by construction. That is a prediction, and it is the calibration test below.

## Calibration: reproduce the game that beat us, or the grid is in the wrong place

Ladder game 98495047, seed 1640915609, we lost by **$29,384**. The opponent held 0 carrot until
d21, reached 32 tiles by d26, sold nothing, then cleared 76 units at $498 for $37,848 on d29.

Measured 2026-08-24 with `swap_from=21, release_day=29`:

    day  tiles  held  price  townInv      bank
     20      0     0     79     9493    27,767
     26     25     3    228     9239    34,713
     28     30    21    315     9156    36,392
     29     11     0    280     9187    59,047      +$22,655 on the last day

    final: ours $57,493  opponent $59,047   margin -$1,554

The **shape** reproduces -- abstain, convert, deficit grows, price climbs, dump, and it beats us.
The **magnitude** does not: $315 against $498, and 21 units held against 76.

The reason is structural and worth recording, because it is a limit on this whole approach:
`_sow_carrot_instead` only rewrites plantings **the planner has already scheduled**. It cannot
create them. Our plan happens to plant little on d21-d25 and a lot on d26-d27, and carrot planted on
d27 is not ripe until d29 -- 11 tiles were still standing when it sold. So `swap_from` is not a free
axis; it is bounded by where the underlying plan puts its plantings.

Until a cell of this grid takes ~$29k off us on that seed, the grid is not calibrated and any
sweep over it is measuring the wrong region.
"""

import importlib.util
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[2]

#: Products on the `hinge` price curve since the 2026-08-15 balance change. Only these reward
#: cornering; a flat-curve product earns nothing for being withheld and risks the nightly overflow.
HINGE_CROPS = ("CARROT", "TOMATO", "EGG")

DEFAULTS = {
    "hinge_crop": None,        # None == our shipped agent, the origin of the space
    "swap_from": 21,
    "swap_to": 27,
    "release_day": 29,
    "withhold": (),
    "floor_price": 0,          # 0 == sell at any price, which is what we ship today
}


def _load(bundle):
    """Import a built single-file submission as a module. Each call gets its own module object,
    so two morphs in one process cannot share mutated constants."""
    path = REPO / bundle
    spec = importlib.util.spec_from_file_location(f"_morph_{abs(hash(str(path)))}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_agent(bundle="submission/e2500_carrot.py", **params):
    """Our bundled agent, morphed by `params`. See `DEFAULTS` for the axes."""
    p = dict(DEFAULTS)
    p.update(params)
    mod = _load(bundle)

    # **Set the constant in the namespace the code actually reads.** The bundle's entry point calls
    # `_SA.make_agent(...)`, where `_SA` is the EMBEDDED `schedule_agent` module. `CARROT_SWAP_DAYS`
    # is defined and read inside that module, not in the bundle's own top-level namespace. Setting
    # it on the outer module is silent and does nothing: measured 2026-08-24, `swap_from` 14/17/19/21
    # returned four byte-identical games (-$1,554 each, 36 tiles, 21 units held). A parameter that
    # is not on the code path reads exactly like a measured null, and this project has lost days to
    # that before -- see the `SOLVED_DAYS` / `PRECOMPUTED_ROUTES` note in the global rules.
    tgt = getattr(mod, "_SA", mod)

    crop = p["hinge_crop"]
    if crop is not None:
        if crop not in HINGE_CROPS:
            raise ValueError(f"{crop} is not on the hinge curve; cornering it earns nothing")
        for name, value in (("CARROT_SWAP_DAYS",
                             tuple(range(p["swap_from"], p["swap_to"] + 1))),
                            ("CARROT_DRAIN_MIN", 0),
                            ("CARROT_OPP_MAX", 10_000)):
            if not hasattr(tgt, name):
                raise AttributeError(
                    f"{name} is not in {tgt.__name__}; this morph would be a silent no-op")
            setattr(tgt, name, value)

    inner = mod.agent
    withhold = tuple(p["withhold"]) or ((crop,) if crop else ())
    release, floor = p["release_day"], float(p["floor_price"])

    def agent(obs, config=None):
        act = inner(obs, config)
        day = int(obs.get("day", 0) or 0)
        orders = act.get("market") or []
        if not orders:
            return act
        prices = (obs.get("market") or {}).get("prices") or {}

        def keep(o):
            if len(o) < 2 or o[0] != "SELL":
                return True
            item = o[1]
            # Withheld until the release day: this is the cornering half.
            if item in withhold and day < release:
                return False
            # Priced below the floor: this is the cadence half, and it is what stops a book being
            # flooded to $1 by d13. Released unconditionally at the close, since stock left
            # unsold at the end scores nothing at all.
            if floor > 0 and day < release and float(prices.get(item, 0) or 0) < floor:
                return False
            return True

        act["market"] = [o for o in orders if keep(o)]
        return act

    return agent
