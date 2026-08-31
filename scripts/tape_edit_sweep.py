"""Perturb カワシギ one op at a time and see which perturbation banks more than he does.

Alex, 2026-08-21: *"try sweeping somehow across arms and town shops and items and see if there are
any improvements"*, *"run the sweep first with the ideas we had and ignore geese to begin with --
but try and vary the play as well of the opponent a little"*.

The replay is exact for thirty days, so this is no longer a search over plans. It is a search over
single edits to a plan that already works, which is a far smaller space and the only one where a
win is attributable. `kagg/search/tape_edit.py` is the operator; this is the sweep around it.

## Three axes, and why each is here

**The crop edit.** `WHEAT -> CARROT` in the back half, `WHEAT -> TOMATO` around d12-d15. Both come
off measurements already in `docs/`: 2,430 of 2,702 winning seats plant their first carrot on
d21-d22, and the 81 seats whose town drains TOMATO bank a median $91,501 against $63,580 for the
six without. He already plants 5-8 carrots, so the question is not *whether* carrot pays but
whether he is at the optimum -- and the answer is allowed to be yes.

**The town.** `--live-shops` is the default here, unlike `seed_tape_grid.py`: the seed draws its own
town, so a carrot arm is being asked "do you beat him on a PET_CAFE town and lose on a BAKERY one",
which is the only version of the question with a decision in it. Both seats always get the same
draw.

**The opponent.** `melon_branch` reads the opponent's melon tiles at d3 and is the whole
melon/strawberry latch, so an opponent held fixed is a sweep that can never fire it. Three recorded
seat-1 policies are available and they differ: `kawashigi` seat 1 plants 5 melon, `kawashigi_b3`
plants 9, which is exactly `melon_branch.OPPONENT_MELON`.

## What the control arm is for

`--arms control` runs the unedited replay through the identical code path, including
`surplus_sells`, whose rule is written so that it is silent on a turn the tape already covers. Every
delta printed is against the control on the SAME seed and the SAME opponent. Season totals move
$33k on the town draw alone -- an arm quoted against a pooled mean is measuring the draw.

    python -u scripts/tape_edit_sweep.py --seeds 11 12 13 --arms control carrot3_20_26
    python -u scripts/tape_edit_sweep.py --seeds 11 12 13 14 15 16 17 18 --opponents kawashigi kawashigi_b3
"""

import argparse
import collections
import functools
import typing
import json
import multiprocessing
import os
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import breakdown as B                                                        # noqa: E402
from kagg.search import tape_edit as E                                       # noqa: E402
from kagg.search import schedule_agent as SA                                 # noqa: E402

#: The three tape keys, usable as opponents by name. `--pool` is the real field; these stay because
#: `kawashigi_b3` is the one opponent known to arm the strawberry branch and is a useful control.
OPPONENTS = ("kawashigi", "kawashigi_b3", "kawashigi_q4c")

#: Built by `scripts/build_opponent_pool.py`. Twelve players spanning `melon_at_d3` from 0 to 12,
#: which is the field that decides WHICH of our four tape branches arms -- see `build_opponent_pool`.
POOL_FILE = REPO / "data/opponent_pool.json"

#: Chosen to span `melon_at_d3` (0, 4, 5, 5, 7, 8, 11, 12, 12, 12, 12, 12) rather than to span bank.
#: Holding the opponent at Yusuke Hayashi (5) left the strawberry branch unreachable across 96 runs,
#: so an opponent below the `melon_branch.OPPONENT_MELON` threshold of 9 and one above it are not
#: two samples of the same experiment -- they are two different seasons of ours.
POOL_NAMES = ("tetsuya", "ReCurSiON", "Crop Dusta", "Victor @ Tufa Labs", "Arman Tuganbaev",
              "Subramanya N", "Ryo Hasegawa", "Matteo123383iend", "Utkarsh #2",
              "Efe Can Celiksoy", "Kobe BRYANT", "カワシギ")


def load_pool(names=POOL_NAMES):
    """`{name: (replay_path, seat)}` for the sweep's opponent field."""
    if not POOL_FILE.exists():
        raise SystemExit("no %s -- run scripts/build_opponent_pool.py --write %s"
                         % (POOL_FILE, POOL_FILE))
    rows = {r["name"]: r for r in json.loads(POOL_FILE.read_text())}
    missing = [n for n in names if n not in rows]
    if missing:
        raise SystemExit("not in the pool file: %s" % missing)
    return {n: (str(REPO / rows[n]["replay"]), rows[n]["seat"], rows[n]["melon_at_d3"])
            for n in names}


class Arm(typing.NamedTuple):
    """Everything about one perturbation, in ONE object.

    **This exists because the same bug happened twice in one day.** An arm used to be a bare tuple
    of ops, and what it MEANT was spread across three functions that had to be kept in sync by
    hand: `edited_openings` decided what it edited, `build_agent` decided which runtime wrappers it
    got, and `swap_products` decided which crops it offered for sale. An arm registered in two of
    the three ran as something else entirely, silently:

      `cond_carrot_d4_o7`  planted `{CARROT 30}` and bought `{CARROT 30}`, identical to the static
                           arm on the field, and banked $4,412 less -- because it was missing from
                           `swap_products`, so its carrot was never offered and stood in the shed.
      `x_cow`              overwrote his d0 opening and read -$54k to -$88k. Not a measurement.

    Alex, 2026-08-22: *"the bugs hid cos you still have milli vanilli spaghetti"*. Correct -- the
    structure invited the mistake rather than merely permitting it.

    `sells` is DERIVED from the ops by `arm()` below, not declared, so it cannot drift out of step
    with what the arm actually grows.
    """

    name: str
    #: Static edits to the replayed opening: ("swap", days, frm, to, n) / ("sellhour", days, hour)
    #: / ("retape", latch_key, target).
    opening: tuple = ()
    #: Runtime wrappers, applied outermost-last: ("topup", days, hour, products) /
    #: ("herd", mode, day) / ("herdshift", delta, from_day) / ("condcarrot", drain_min, opp_max).
    wrappers: tuple = ()
    #: Products to offer beyond the tape's own orders. Derived; see `arm()`.
    sells: tuple = ()


#: Crops an edit can INTRODUCE, mapped to what must then be offered. WHEAT is deliberately absent:
#: topping up wheat crashed our own book, $330 against a $70,687 control.
_INTRODUCES = {"swap": lambda op: op[3], "condcarrot": lambda op: "CARROT"}


def arm(name, opening=(), wrappers=()):
    """Build an `Arm`, deriving `sells` from the ops so it cannot be forgotten."""
    sells = set()
    for op in tuple(opening) + tuple(wrappers):
        fn = _INTRODUCES.get(op[0])
        if fn:
            sells.add(fn(op))
    return Arm(name, tuple(opening), tuple(wrappers), tuple(sorted(sells - {"WHEAT"})))


#: Swap every plant the day has. Any number above his biggest day's plant count does this; 99 is
#: chosen so the arm NAME says "all of them" rather than encoding a tape's largest day.
ALL = 99


def build_arms():
    """`{name: [(days, frm, to, per_day)]}` -- the edit list for each arm, control first.

    ## The carrot window is d25-d27, and it was measured, not chosen

    A first pass swept d18-d28 and lost **$6,787 on seed 11 for twelve tiles**, which is $566 a
    tile and far more than a wheat crop is worth. The mechanism is not the crop economics, it is the
    lifespan: `reference/kaggriculture.py:224` gives WHEAT `planted + 5` days and CARROT
    `planted + 4`, and `:759-766` turns the tile into a **WEED** once the units run out. Weeds at
    d29 went 25 -> 32 and the whole loss landed in the last two days' harvest.

    So the question is not "when do winners plant carrot" but "which of HIS tiles are lifted inside
    four days". Read off the dawn boards of all three tapes, grouped by the day the tile was sown:

        sown        d0 .. d24      d25        d26        d27
        melon q3    5 days, all    4 days     3 days     3 days
        straw q3    5 days, all    4 days*    3 days     3 days
        q4          5 days, all    4 days     3 days     3 days

    (*two of eleven stand five.) He is not being careless -- he sows on a five-day cadence all
    season and the final bell truncates the last three sowings. **Those three days are the entire
    carrot window**, 27-34 tiles a season, and on them a carrot reaches its max yield (4 units at
    `max_yield_day 3`) where the wheat is cut off before its own (6 units at `max_yield_day 4`).

    Tomato stays at d12-d15: 8 days to first yield, so anything later never fruits.
    """
    arms = {"control": arm("control")}
    late = ((25,), (26,), (27,), (26, 27), (25, 26, 27))
    for days in late:
        tag = "".join("d%d" % d for d in days)
        arms["carrot_%s_all" % tag] = arm("carrot_%s_all" % tag, opening=(("swap", days, "WHEAT", "CARROT", ALL),))
    for n in (2, 4):
        arms["carrot%d_d25d27" % n] = arm("carrot%d_d25d27" % n, opening=(("swap", (25, 26, 27), "WHEAT", "CARROT", n),))
    # **The arm the first pass measured, kept deliberately.** It is the negative control: if a run
    # ever shows it break even, the weed mechanism above has changed and the window is wrong.
    arms["carrot2_20_26"] = arm("carrot2_20_26", opening=(("swap", tuple(range(20, 26)), "WHEAT", "CARROT", 2),))
    for n in (1, 2, 3):
        arms["tomato%d" % n] = arm("tomato%d" % n, opening=(("swap", tuple(range(12, 16)), "WHEAT", "TOMATO", n),))
    # **The gradient points down, so the arm that tests it points the other way.** Every carrot arm
    # above is negative and the loss grows with the number of tiles, which says his optimum is at or
    # below the carrot he already plants. These take it OUT. If they win, he is over-planting it.
    for n in (2, ALL):
        _n = "decarrot%s" % ("all" if n == ALL else n)
        arms[_n] = arm(_n, opening=(("swap", tuple(range(30)), "CARROT", "WHEAT", n),))
    # **Sell-hour arms.** Alex, 2026-08-21: *"we looked at the agent 2500 on the leaderboard and
    # discovered it was better when we sold at h=16 as opposed to 0 4,8 or 23 - i think that is a
    # test to be run maybe from d20 or so"*.
    #
    # There is a mechanism. `_town_consume` drains each unlocked shop every 4 turns and the town
    # CENTRE every 24, at hour 0 -- so h0 is the only hour with both drains, the deepest inventory
    # dip and the highest price. The archive agrees: Ryo Hasegawa, tetsuya, Subramanya N and
    # ReCurSiON all concentrate their sell volume at h0, Arman Tuganbaev at h1, while our own
    # submission concentrates at h16. That disagreement is the thing being tested.
    for h in (0, 4, 8, 12, 16, 20, 23):
        arms["sell_h%d_d20" % h] = arm("sell_h%d_d20" % h, opening=(("sellhour", tuple(range(20, 30)), h),))
        arms["sell_h%d_all" % h] = arm("sell_h%d_all" % h, opening=(("sellhour", tuple(range(30)), h),))
    # **ADD an order, do not MOVE the day's sale.** `sell_h*` moves and loses heavily because the
    # rest of the day's harvest then goes unoffered. These keep his cadence intact and offer only
    # what is left standing at that hour -- the arm that answers "sell SOME at h16".
    for h in (8, 12, 16, 20):
        arms["topup_h%d_d20" % h] = arm("topup_h%d_d20" % h, wrappers=(("topup", tuple(range(20, 30)), h, ("WHEAT",)),))
        arms["topup_h%d_all" % h] = arm("topup_h%d_all" % h, wrappers=(("topup", tuple(range(30)), h, ("WHEAT",)),))
    # **Herd counter-pick.** `_herd_split` reads the shop draw and never `farms[1 - me]`; the
    # opponent's split swings 10-4 COW to 6-12 SHEEP across the field, and WOOL collapses 98% on a
    # town with no yarn store. This is the untested axis with the largest measured price swing.
    for mode in ("cow", "sheep", "counter", "book"):
        for dd in (8, 12):
            arms["herd_%s_d%d" % (mode, dd)] = arm("herd_%s_d%d" % (mode, dd), wrappers=(("herd", mode, dd),))
    # **A cow arm that can actually ADD cows.** `herd_cow_d8` measured -$1,048 and looked like a
    # test of "more cow"; it was not. By d8 he has bought most of the herd, and on a town with no
    # yarn store `_herd_split` has already taken cows to its cap -- so the arm had nothing to
    # change (+403, -103 on the two dry towns) and only bit on wool towns where he chose sheep
    # deliberately (-4,718). Deciding at d0 is what actually moves the split.
    for dd in (0, 4):
        arms["cow_d%d" % dd] = arm("cow_d%d" % dd, wrappers=(("herd", "cow", dd),))
        arms["sheep_d%d" % dd] = arm("sheep_d%d" % dd, wrappers=(("herd", "sheep", dd),))

    # A gradient with the control at delta = 0, instead of two all-or-nothing ends.
    for d in (2, 4, 6, 8):
        arms["cowshift_p%d" % d] = arm("cowshift_p%d" % d, wrappers=(("herdshift", d, 1),))
        arms["cowshift_m%d" % d] = arm("cowshift_m%d" % d, wrappers=(("herdshift", -d, 1),))

    # **Does `(True, True)` belong on the strawberry tape at all?** It currently maps to
    # `92466371`, the same file as `(True, False)`, so a q4 trigger is discarded whenever the melon
    # latch also fired. Measured 2026-08-21 on 4,224 stratified seasons, the unedited replay wins
    # **92% on `(False, True)` -> 91907974** and **11% on `(True, True)` -> 92466371**. Those two
    # rows face different opponents by construction, so this arm is the clean A/B: same town, same
    # opponent, only the tape moves.
    # **Buy the fourth parcel on the three-quadrant seasons.** See `tape_edit.add_land` for the
    # cash evidence: q4 buys its third parcel at d12 holding $12,717 and the q3 tapes reach d12
    # holding $16,403 and $16,162.
    for d in (12, 13, 14, 16, 18):
        arms["land_d%d" % d] = arm("land_d%d" % d, opening=(("addland", d, 0),))

    # **The shootout for `(True, True)`.** The key describes "opponent shows 9+ melon AND a yarn
    # store unlocked by d5". Candidates, with what each recording actually IS:
    #
    #     91906088   opp 12 melon, yarn by d5  -> a genuine (True,True) season, 42 straw / 12 melon,
    #                banked 128,408. The right SHAPE, and it was never registered.
    #     92488785   opp  9 melon, yarn by d5  -> also genuine, but banked only 80,864.
    #     91907974   opp  5 melon, yarn by d5  -> a (False,True) season: 34 straw / 20 MELON. Wrong
    #                shape, and yet it beat the old mapping 13/14 -- which says how wrong the old
    #                one was, not that this one is right.
    #     92466371   opp  9 melon, NO yarn     -> the old mapping, a (True,False) season.
    #
    # Shipped today: 91907974, on 14 configurations and one seed. This lets the sweep replace it.
    for tag, tgt in (("q4melon", "data/seed_scripts/downloads_2026-08-13/91907974.json"),
                     ("straw_q4_128k", "data/seed_scripts/downloads_2026-08-13/91906088.json"),
                     ("straw_q4_81k", "data/seed_scripts/kawashigi/92488785.json"),
                     ("straw_q3_old", "data/seed_scripts/kawashigi/92466371.json"),
                     ("straw_q4_136k", "data/seed_scripts/leaders_2026-08-19/93459936.json")):
        arms["tt_%s" % tag] = arm("tt_%s" % tag, opening=(("retape", (True, True), tgt),))

    # The conditional version: same edit, fired only where the cross of town drain and opponent
    # carrot says it pays. Thresholds are arms so the sweep can move them.
    for dmin in (3, 4, 5):
        for omax in (3, 7, 99):
            arms["cond_carrot_d%d_o%d" % (dmin, omax)] = arm("cond_carrot_d%d_o%d" % (dmin, omax), wrappers=(("condcarrot", dmin, omax),))

    # **The 2x2x2.** Every arm so far was one-at-a-time and `CLAUDE.md` requires the 2x2 when two
    # things are in the tree. Carrot is the only factor with a positive region (drain 6), so the
    # combinations worth paying for are the ones containing it.
    CARROT = ("swap", (25, 26, 27), "WHEAT", "CARROT", ALL)
    TOMATO = ("swap", tuple(range(12, 16)), "WHEAT", "TOMATO", 1)
    COW = ("herd", "cow", 0)
    arms["x_carrot"] = arm("x_carrot", opening=(CARROT,))
    arms["x_tomato"] = arm("x_tomato", opening=(TOMATO,))
    arms["x_cow"] = arm("x_cow", wrappers=(COW,))
    arms["x_carrot_tomato"] = arm("x_carrot_tomato", opening=(CARROT, TOMATO))
    arms["x_carrot_cow"] = arm("x_carrot_cow", opening=(CARROT,), wrappers=(COW,))
    arms["x_tomato_cow"] = arm("x_tomato_cow", opening=(TOMATO,), wrappers=(COW,))
    arms["x_carrot_tomato_cow"] = arm("x_carrot_tomato_cow", opening=(CARROT, TOMATO), wrappers=(COW,))

    arms["topup_h16_d20_all_products"] = arm(
        "topup_h16_d20_all_products",
        wrappers=(("topup", tuple(range(20, 30)), 16,
                   ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL")),))
    return arms


def swap_products(edits):  # noqa: D401  (kept for callers outside this module)
    """Crops an edit INTRODUCES, so `surplus_sells` knows what to offer. WHEAT is never topped up.

    **`condcarrot` counts too, and leaving it out cost $4,412.** The conditional arm plants exactly
    what the static one does -- measured `{CARROT 30}` plants and `{CARROT 30}` seeds in both -- but
    without an entry here it got no surplus seller, so its carrot stood in the shed to the final
    bell. The two arms then differed by their sell side while looking identical on the field, which
    is the hardest kind of difference to see.
    """
    out = {e[3] for e in edits if e[0] == "swap"}
    out |= {"CARROT" for e in edits if e[0] == "condcarrot"}
    return sorted(out - {"WHEAT"})


@functools.lru_cache(maxsize=None)
def _base_openings():
    """The four unedited openings, read once per worker process.

    **This is a 5x speed-up, not a tidy-up.** `_replay_opening` parses a 30 MB recording, and there
    are three distinct files behind the four latch keys, so rebuilding them per season costs ~90 MB
    of JSON per season. Measured on the box 2026-08-21: 200 of 4,560 seasons in 816s, a 5.2-hour
    grid. The openings do not depend on the town, the opponent or the seed -- only on the tape.
    """
    return {tuple(key): SA._replay_opening(SA.REPLAY_OPENING_DAYS, path, team)
            for key, (path, team) in SA.REPLAY_OPENING_TAPE.items()}


@functools.lru_cache(maxsize=None)
def edited_openings(edits):
    """Every key of `REPLAY_OPENING_TAPE`, edited, ready for `EMBEDDED_OPENINGS`.

    The edit is applied to all four latch keys because which one arms is decided in-game, at d3 and
    d5, by the opponent and the town. Editing only the key we expect to arm makes the arm silently
    become the control on any seed that latches the other way -- a null that reads like a measured
    null and is not one.

    `edits` must be a tuple of tuples so it can be cached; an arm is asked for hundreds of times
    across a grid and the answer never changes.
    """
    # **An `Arm` is not a tuple of edits, and iterating one yields its FIELDS.**
    # `season` passes the `Arm` straight in, so `for e in edits` walked
    # `("control", (), (), ())` and `()[0]` raised IndexError -- on the control arm, which means
    # every arm. Normalise here rather than at the call site: this is the function that documents
    # `edits` as "a tuple of tuples", so it is the one that should enforce it.
    if isinstance(edits, Arm):
        edits = tuple(edits.opening) + tuple(edits.wrappers)

    # A "retape" edit re-points a LATCH KEY at a different recording before any op edit runs.
    # A "retape" edit re-points a latch key either at another KEY's opening or at a FILE.
    remap = {e[1]: e[2] for e in edits if e[0] == "retape"}
    out = {}
    for key, opening in _base_openings().items():
        if key in remap:
            tgt = remap[key]
            if isinstance(tgt, tuple):
                opening = _base_openings()[tgt]
            else:
                # **A missing tape must stop the sweep, not degrade it.** `_replay_opening` returns
                # `{}` when the file is not on disk, deliberately: a submission bundle carries no
                # `data/` tree and must fall back to a planned opening rather than raise. That is
                # right for the artifact and wrong here -- an arm whose whole definition is "replay
                # THIS recording" silently becomes "replay nothing" and still reports a number.
                #
                # Measured 2026-08-22: three of the five `(True, True)` shootout candidates were
                # never synced to the Windows box, and the grid ran 80 minutes and 2,800 seasons
                # with `tt_straw_q4_128k`, `tt_straw_q4_81k` and `tt_straw_q4_136k` all quietly
                # playing the planner. No error, no warning, three arms measuring the same nothing.
                path = REPO / tgt
                if not path.exists():
                    raise FileNotFoundError(
                        f"arm re-tapes {key} to {tgt}, which is not on this machine. "
                        f"Sync it before running, or the arm silently replays nothing.")
                opening = SA._replay_opening(SA.REPLAY_OPENING_DAYS, str(path),
                                             "\u30ab\u30ef\u30b7\u30ae")
                if not opening:
                    raise ValueError(
                        f"arm re-tapes {key} to {tgt}, which yielded an EMPTY opening. "
                        f"Check the team name and REPLAY_OPENING_DAYS.")
        for e in edits:
            if e[0] == "swap":
                _, days, frm, to, per_day = e
                opening, _ = E.swap(opening, set(days), frm, to, per_day)
            elif e[0] in ("topup", "herd", "herdshift", "retape", "condcarrot"):
                continue
            elif e[0] == "addland":
                _, day, hour = e
                opening = E.add_land(opening, day, hour)
            elif e[0] == "sellhour":
                _, days, hour = e
                opening = E.move_sells(opening, days, hour)
            else:
                raise ValueError("unknown edit %r" % (e,))
        out[key] = opening
    return out


#: Thin action tapes written by `scripts/extract_opponent_tapes.py`. A pool opponent's 30 MB
#: recording is 99.6% observations the sweep never reads; the twelve-opponent pool is 375 MB as
#: recordings and 1.4 MB as actions. Preferred whenever present, which is what makes the box sync a
#: few seconds instead of a 1.13 GB push.
TAPE_DIR = REPO / "data/opponent_tapes"

IDLE = {"farmer": ["PASS"], "hands": [], "market": []}

#: Read off three recorded games rather than remembered: a shop unlocks at hour 0 of d3, d6, d9,
#: d12, d15, d18, d21 and d24 -- **eight of them, not four** -- and they are drawn **with
#: replacement**. カワシギ's own town draws `SMOOTHIE_SHOP` four times. So the town space is 8**8,
#: enumeration is out, and the axis that matters is the resulting DRAIN VECTOR: how many times a
#: season the town takes each product off the book.
UNLOCK_DAYS = (3, 6, 9, 12, 15, 18, 21, 24)

SHOP_NAMES = ("BAKERY", "PIZZA_SHOP", "BRUNCH_SPOT", "YARN_STORE", "ICE_CREAM_SHOP",
              "PET_CAFE", "SMOOTHIE_SHOP", "FARMERS_MARKET")


def town_shops(draw):
    """`turn -> unlocked shop list`, the shape `breakdown.run` injects."""
    return lambda t: [s for s, d in zip(draw, UNLOCK_DAYS) if t // 24 >= d]


def drain_vector(draw):
    """`{product: drains per shop-interval}` -- a single-product shop drains at double rate.

    `reference/kaggriculture.py:_town_consume`: every unlocked shop consumes one of each of its
    products every `townShopSellInterval`, and a shop with ONE product consumes two. This is the
    number a carrot arm should be conditioned on -- not the seed, and not the shop names.
    """
    from kaggle_environments.envs.kaggriculture import kaggriculture as KG    # noqa: PLC0415
    out = collections.Counter()
    for s in draw:
        products = KG.SHOPS[s]
        mult = 2 if len(products) == 1 else 1
        for p in products:
            out[p] += mult
    return out


def thin_policy(path):
    """`agent(obs, turn)` replaying a thin action tape. Same contract as `B.tape_policy`."""
    acts = json.loads(pathlib.Path(path).read_text())["actions"]
    return lambda obs, t: acts[t] if t < len(acts) else IDLE


def opponent_spec(name, pool):
    """A picklable description of the opponent, resolved to a policy inside the worker.

    A pool entry is that player's OWN action stream, so `seat_wanted=0` against their own name. A
    `TAPES` key is カワシギ's game and we want the other chair, so `seat_wanted=1` against his.
    Getting this backwards silently puts a second copy of him opposite the replay, which mirrors
    and draws rather than measuring anything.
    """
    if name in pool:
        replay, seat, _ = pool[name]
        cut = TAPE_DIR / ("%s_seat%d.json" % (pathlib.Path(replay).stem, seat))
        if cut.exists():
            return {"kind": "thin", "path": str(cut)}
        return {"kind": "replay", "replay": replay, "team": name, "seat": 0}
    replay, _, team = B.TAPES[name]
    return {"kind": "replay", "replay": replay, "team": team, "seat": 1}


def make_opponent(spec):
    if spec["kind"] == "thin":
        return thin_policy(spec["path"])
    return B.tape_policy(spec["replay"], spec["team"], spec["seat"])


def season(edits, seed, opponent, weeds, base_tape, stop_day=None):
    """One full game. Returns `(our_money, their_money, end_of_season_crop_tiles, ops)`.

    `their_money` is read off the OPPONENT's own turn, at the last turn it is asked for an action,
    so it is short by that turn's market settlement. `breakdown.run` snapshots seat 0 only and
    widening it is a change to a file forty other scripts import. Good enough to see a win flip;
    do not quote it as a final bank.
    """
    # **Never top up WHEAT.** Measured 2026-08-21: the `decarrot` arm banked $330 against the
    # control's $70,687 purely because `surplus_sells` was offering every spare wheat unit every
    # turn and walking its own price into the floor. With WHEAT excluded the same arm is $70,374 --
    # a $313 wash -- and the PLANT count is 181 in both, so nothing was ever dropped. His wheat
    # cadence is the one thing in the tape that is unambiguously tuned; adding offers to it only
    # competes with ourselves.
    products = tuple(edits.sells) if isinstance(edits, Arm) else ()
    _, base_schedule, _ = B.TAPES[base_tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(base_schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    economy = B.env_config(B.TAPES[base_tape][0])

    def mine():
        # The seam is `EMBEDDED_OPENINGS`, which the bundler already uses -- so an edited season
        # runs the shipped `replayed()` unmodified, and nothing here needs a flag in the agent.
        saved = SA.EMBEDDED_OPENINGS
        SA.EMBEDDED_OPENINGS = edited_openings(edits) if edits else {}
        try:
            a = SA.make_agent(thin, 0, router=True)
        finally:
            SA.EMBEDDED_OPENINGS = saved
        a = _apply_wrappers(a, edits)
        a = E.surplus_sells(a, products) if products else a
        return lambda o, t: a(o)

    theirs = [0]

    def opp():
        p = make_opponent(opponent)

        def watched(obs, t):
            farms = obs.get("farms") or []
            seat = int(obs.get("player", 1) or 1)
            if len(farms) > seat:
                theirs[0] = int(farms[seat].get("money", 0) or 0)
            return p(obs, t)

        return watched

    days, ops, _, _ = B.run(mine, opp, seed, weeds, stop_day=stop_day, economy=economy, shops=None)
    last = days[-1]
    # **Weeds, not the end-of-season crop count.** Every tile is bare at d29, so `crop_CARROT`
    # reads 0 on the arm and 0 on the control and says nothing. The weed count is what separates a
    # swap that harvested from one whose lifespan ran out -- it is the mechanism that killed the
    # first carrot window and it belongs on every line of the sweep.
    crops = {c: last.get("crop_" + c, 0) for c in B.CROPS}
    crops["weed"] = last.get("weed", 0)
    crops["plant"] = sum(ops[d]["PLANT"] for d in ops)
    return last["money"], theirs[0], crops, ops


def _apply_wrappers(agent, edits):
    """Wrap `agent` with the arm's runtime wrappers, outermost-last.

    **This was missing entirely.** `Arm.wrappers` was declared, populated by `arm()` and stored,
    and then nothing ever read it: `edited_openings` skips every wrapper op with `continue`
    (`:355`), and `season.mine()` applied only `surplus_sells`. The class docstring names a
    `build_agent` that "decided which runtime wrappers it got" and no such function exists in this
    file. So every wrapper-only arm -- all `herd_*`, `cow_*`, `sheep_*`, `cowshift_*`, `topup_*`,
    `cond_carrot_*`, `x_cow` -- ran as a byte-identical copy of the control and would have reported
    a measured null.

    The operators themselves were never missing; they are in `kagg/search/tape_edit.py`. Only the
    wiring between the arm table and them was gone.

    An unknown wrapper raises. A sweep that silently ignores an arm it does not understand is the
    failure this whole function exists to undo.
    """
    if isinstance(edits, Arm):
        edits = tuple(edits.wrappers)
    for e in edits:
        kind = e[0]
        if kind == "topup":
            _, days, hour, prods = e
            agent = E.top_up_at_hour(agent, prods, hour, from_day=min(days))
        elif kind == "herd":
            _, mode, day = e
            agent = E.herd_species(agent, mode, decide_day=day, me=0)
        elif kind == "herdshift":
            _, delta, from_day = e
            agent = E.herd_shift(agent, delta, from_day=from_day, me=0)
        elif kind == "condcarrot":
            _, drain_min, opp_max = e
            agent = E.carrot_when_it_pays(agent, drain_min=drain_min, opp_tiles_max=opp_max, me=0)
        elif kind in ("swap", "sellhour", "addland", "retape"):
            continue                       # static opening edits; applied in `edited_openings`
        else:
            raise ValueError("unknown wrapper %r" % (e,))
    return agent


def _job(spec):
    """One (opponent, arm, seed) season. Top level so `multiprocessing` can pickle it."""
    opp_name, opp, arm_name, edits, seed, weeds, base_tape, days = spec
    money, theirs, crops, _ = season(edits, seed, opp, weeds, base_tape, days)
    return opp_name, arm_name, seed, money, theirs, crops["weed"], crops["plant"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+",
                    default=[11, 42, 7, 899, 1337, 4096, 13001, 60013,
                             23, 101, 555, 2718, 31415, 8191, 77, 9001])
    ap.add_argument("--arms", nargs="+", default=None, help="default: every arm")
    ap.add_argument("--opponents", nargs="+", default=None,
                    help="pool player names and/or %s; default is the whole pool" % (OPPONENTS,))
    ap.add_argument("--weeds", type=float, default=0.005,
                    help="the ladder's rate, not zero -- an unwatered swap weeds and must be paid for")
    ap.add_argument("--base-tape", default="kawashigi")
    ap.add_argument("--days", type=int, default=None, help="stop early; default is the full season")
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--out", default=None,
                    help="CSV written one row per finished season, flushed immediately. Without "
                         "it a killed sweep prints nothing at all -- 29,568 planned seasons once "
                         "produced 0 rows here for exactly that reason.")
    args = ap.parse_args()

    pool = load_pool()
    all_arms = build_arms()
    names = args.arms or list(all_arms)
    bad = [n for n in names if n not in all_arms]
    if bad:
        ap.error("unknown arm(s) %s; have %s" % (bad, list(all_arms)))
    if "control" not in names:
        names = ["control"] + names
    opps = args.opponents or list(pool)
    bad = [o for o in opps if o not in pool and o not in OPPONENTS]
    if bad:
        ap.error("unknown opponent(s) %s" % bad)

    print("seeds      %s" % " ".join(map(str, args.seeds)))
    print("arms       %s" % " ".join(names))
    print("opponents  %s" % ", ".join("%s(melon@d3=%s)" % (o, pool[o][2] if o in pool else "?")
                                      for o in opps))
    print("weeds      %s   live shops -- each seed draws its own town, both seats the same" % args.weeds)
    print("jobs       %d   %d seasons\n" % (args.jobs, len(opps) * len(names) * len(args.seeds)))

    jobs = [(o, opponent_spec(o, pool), n, all_arms[n], s, args.weeds, args.base_tape, args.days)
            for o in opps for n in names for s in args.seeds]

    # The header goes down BEFORE the pool starts, and every row is flushed as it lands. A sweep
    # that writes at the end is a sweep that returns nothing when it is killed.
    csv = None
    if args.out:
        path = pathlib.Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        csv = open(path, "w", buffering=1)
        csv.write("opponent,arm,seed,money,theirs,margin,weed,plant\n")
        print("rows       %s (flushed per season)" % path, flush=True)

    got, t0 = {}, time.time()
    with multiprocessing.Pool(args.jobs) as mp:
        for k, (o, n, s, money, theirs, weed, plant) in enumerate(mp.imap_unordered(_job, jobs), 1):
            got[(o, n, s)] = (money, theirs, weed, plant)
            if csv is not None:
                csv.write("%s,%s,%d,%.0f,%.0f,%.0f,%d,%d\n"
                          % (o, n, s, money, theirs, money - theirs, weed, plant))
                csv.flush()
                os.fsync(csv.fileno())
            if k % 25 == 0 or k == len(jobs):
                print("  %4d/%d   %5.0fs" % (k, len(jobs), time.time() - t0), flush=True)
    if csv is not None:
        csv.close()

    # **Scored on MARGIN, not on money.** Measured 2026-08-21: the tomato arm is +$4,846 on our own
    # bank and -$5,546 on `ours - theirs`, because planting less wheat leaves the wheat book thinner
    # and lifts the price for the opponent, who sells more wheat than we do. The ladder is Elo. A
    # table that prints only our bank recommends the arm that loses.
    print("\n%-22s %-22s %11s %11s %8s  %s"
          % ("opponent", "arm", "d money", "d margin", "wins", "per-seed d margin"))
    print("-" * 130)
    best = []
    for o in opps:
        for n in names:
            have = [s for s in args.seeds if (o, n, s) in got and (o, "control", s) in got]
            if not have:
                continue
            dm = [got[(o, n, s)][0] - got[(o, "control", s)][0] for s in have]
            mg = [got[(o, n, s)][0] - got[(o, n, s)][1] for s in have]
            bs = [got[(o, "control", s)][0] - got[(o, "control", s)][1] for s in have]
            dg = [a - b for a, b in zip(mg, bs)]
            w = sum(1 for s in have if got[(o, n, s)][0] > got[(o, n, s)][1])
            print("%-22s %-22s %+11.0f %+11.0f %5d/%-2d  %s"
                  % (o[:22], n, sum(dm) / len(dm), sum(dg) / len(dg), w, len(have),
                     " ".join("%+6d" % x for x in dg[:12])))
            if n != "control":
                best.append((sum(dg) / len(dg), o, n, w, len(have)))

    print("\nPOOLED over every opponent, on margin -- the only column that decides anything")
    print("%-22s %11s %11s %10s" % ("arm", "d margin", "median", "wins / total"))
    print("-" * 60)
    for n in names:
        dg, w, tot = [], 0, 0
        for o in opps:
            for s in args.seeds:
                if (o, n, s) in got and (o, "control", s) in got:
                    dg.append((got[(o, n, s)][0] - got[(o, n, s)][1])
                              - (got[(o, "control", s)][0] - got[(o, "control", s)][1]))
                    w += 1 if got[(o, n, s)][0] > got[(o, n, s)][1] else 0
                    tot += 1
        if dg:
            srt = sorted(dg)
            med = srt[len(srt) // 2] if len(srt) % 2 else (srt[len(srt) // 2 - 1] + srt[len(srt) // 2]) / 2.0
            print("%-22s %+11.0f %+11.0f %6d/%-4d" % (n, sum(dg) / len(dg), med, w, tot))


if __name__ == "__main__":
    main()
