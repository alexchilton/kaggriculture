"""Bundle the covering planner into one self-contained `submission/main.py`.

`scripts/build_submission.py` (deleted 2026-08-09) copied a single dependency-free file verbatim,
which was right for
`kagg/agents/contrarian.py` and useless here: the planner is four modules that import each other
plus a 64 KB schedule, and it is the agent that actually wins. Building the old way ships
contrarian and reports "submission verified" while none of the season's work is in the file --
which is exactly what happened on 2026-08-07, and is the `MEMORY.md` lesson about indirection
between the search space and the submission arriving in person.

## How it bundles

Each module's source is embedded **verbatim**, as an `r'''...'''` literal, and the round trip is
asserted before anything is written -- the builder parses its own output back and compares it to
the files on disk, byte for byte. A concatenated bundle was rejected: the four modules define
overlapping names (`ANIMALS`, `SHED`, `dist`) and flattening them would silently pick a winner.

At import the loader builds real module objects and installs them in `sys.modules` under their
real dotted names, in dependency order, so `from . import routines as R` resolves to the embedded
copy and never to anything on the Kaggle image. `kagg` and `kagg.search` are synthesised as
namespace packages with an empty `__path__`, so an accidental `import kagg.anything_else` fails
loudly instead of half-loading a repo that is not there.

None of the four modules touches the filesystem (no `__file__`, no `open`), which is what makes
this safe; the builder re-checks that rather than trusting this paragraph.

## The seat

`make_agent(schedule, me=...)` is bound to a seat, and a submission does not know its seat until
the first observation arrives. The entry point reads `obs["player"]` and builds lazily, one agent
per seat, and rebuilds at day 0 hour 0 so a second episode in the same process starts clean --
the agent carries a season of state (`pins`, `pen_for`, `planted`, `uncovered`) and reusing it
across games would be a slow, silent corruption rather than a crash.

Run: .venv/bin/python scripts/build_planner_submission.py
"""

import json
import kagg.plan as _PLAN
import pathlib
import sys

sys.path.insert(0, ".")

#: Dependency order, dotted name first. `schedule_agent` imports the three search modules; and
#: `routines` imports `kagg.economics.production` at module scope, inside `_crops_fertilizer_helps`,
#: to derive which crops fertilizer pays on. That import is the one that nearly shipped broken:
#: reaching it through the real `kagg/economics/__init__.py` pulls in `kagg.sim.town`, which reads
#: a JSON file off disk, and none of that exists on the Kaggle image. Bundling the leaf module and
#: stubbing the package it lives in keeps `routines.py` verbatim and never runs that `__init__`.
#: `production.py` itself imports only `typing` and the competition environment, which is by
#: definition present wherever this runs.
MODULES = (
    ("kagg.economics.production", "kagg/economics/production.py"),
    ("kagg.search.routines", "kagg/search/routines.py"),
    # **Before `cover`, which imports it at module scope.** The solved days are data, not code: the
    # offline visit orders `cover._apply_precomputed` seats. Without them the bundle imports fine and
    # then plays every day on the greedy, which is a silent 8-day regression rather than a crash.
    ("kagg.search.solved_days", "kagg/search/solved_days.py"),
    # **The 100-tile routes, for the four-quadrant branch only.** Data, like `solved_days`, and
    # loaded lazily by `q4_branch.install_the_fourth_quadrant` -- but it must be in the bundle or
    # the branch raises `ModuleNotFoundError` on the 15% of games that arm it, which is a crash in
    # a minority of games rather than an obvious one.
    ("kagg.search.solved_days_q4", "kagg/search/solved_days_q4.py"),
    # **The two STRAWBERRY solves, and the import check cannot see that they are needed.**
    # `melon_branch.install` and `q4_branch.install` reach them through
    # `importlib.import_module(self.SOLVE_FOR_STRAWBERRY)` -- a string, invisible to the AST walk
    # in `_check_imports` -- and both catch `ImportError` and carry on with the MELON routes. So a
    # bundle without these builds clean, passes every check, and plays the strawberry season on
    # routes solved for a board with different crops on different tiles from d5, where
    # `cover._apply_precomputed` keys a stop on `(tile, ops)` and the stops simply drop.
    #
    # That is the silent-regression shape this file's own docstring is about, one level deeper: not
    # "the wrong agent shipped" but "the right agent shipped with a quarter of its plan missing".
    #
    # **Both are OUT of the bundle as of 2026-08-16, and the reason is measured, not cautious.**
    # All four boards were re-solved that evening at 60s/day in day order, giving the strawberry
    # boards their own routes for the first time (1,234 and 1,528 stops). Rematched over 97 real
    # ladder games -- our live agent in our own seat, each opponent's RECORDED actions in theirs, on
    # the game's own `info.seed` so the shop draw is fixed -- the fresh solve was WORSE:
    #
    #     current code + committed routes    66/97 wins
    #     current code + the fresh solve     63/97 wins
    #
    # Same code, only the routes differing. A third measurement agreeing with two earlier ones (a
    # -$4,600 season on seed 11, and a confounded 63 vs 71 before the boards were isolated). The
    # files are kept out of the tree rather than shipped and hoped for; `melon_branch.install` and
    # `q4_branch.install` already catch `ImportError` and fall through to the melon routes, which is
    # what these 66/97 were measured with.
    #
    # This is NOT a verdict that a strawberry solve is worthless -- the arm demonstrably plays its
    # late season on routes that cannot match, and that is a real defect. It is a verdict that THIS
    # solve, at THIS budget, loses. Re-solving needs its own measurement before it ships.
    #
    # **BOTH ARE BACK IN as of 2026-08-17, on a fresh solve at 300s/day with two defects fixed that
    # the 2026-08-16 solve had.** `OPENING_GEOMETRY` had six squares of the opening carrying the
    # wrong crop, and `dump_day_jobs.py` was handing the solver the DAWN PREDICTION of each unit's
    # start tile rather than the tile it woke on -- 22 of 205 unit-days across d12-d29 wrong, and the
    # whole spawn ring rotated by one on d19. So the earlier negative was measured on routes solved
    # for a board we no longer play, from start tiles that were wrong.
    #
    # What IS measured tonight, on the same 97 ladder games with the seeds fixed, is the melon half:
    #
    #     HEAD                                          66/97
    #     + geometry, + start tiles, + melon q3 resolve  61/97
    #
    # Net -5, and NOT read as a regression: 15 of the 97 games changed result, 5 our way and 10
    # against, on margins as thin as $92, $240, $313 and $583. Fifteen flips splitting 10/5 is 1.3
    # standard deviations from even. It is churn, not signal.
    #
    # **The two strawberry tables themselves have no measurement.** They are shipped on Alex's
    # explicit call, to get the night's work onto the ladder rather than hold it for a rematch. If
    # the rating drops, these two lines are the first thing to pull -- `melon_branch.install` and
    # `q4_branch.install` both catch `ImportError`, so removing them restores the melon fallback
    # that the 66/97 was measured with.
    ("kagg.search.solved_days_straw", "kagg/search/solved_days_straw.py"),
    ("kagg.search.solved_days_straw_q4", "kagg/search/solved_days_straw_q4.py"),
    ("kagg.search.cover", "kagg/search/cover.py"),
    # **Before both branch modules, which import `Branch` from it at module scope.** A leaf: it
    # imports nothing from `kagg`. Its absence is what made this builder refuse to run at all --
    # `q4_branch.py: imports ['kagg.search.branch'], which the bundle does not carry`.
    ("kagg.search.branch", "kagg/search/branch.py"),
    # **`corner_the_book` IS bundled again as of 2026-08-25.** It was excluded earlier the same day
    # because the late-carrot swap had been cut from the agent -- `_sow_carrot_instead` capped the
    # PLANT rewrite and left the BUY_SEED rewrite uncapped, giving 546 seeds at the bell against 45
    # sown. The swap is restored with BOTH halves capped, `schedule_agent` imports this module at
    # line 43, and the builder refuses any module the agent imports but the bundle does not carry --
    # which is how the omission was caught, by `ImportError` on the standalone check rather than in
    # a game.
    #
    # A leaf: `import math` and nothing from `kagg`, so it can sit anywhere before `schedule_agent`.
    ("kagg.search.corner_the_book", "kagg/search/corner_the_book.py"),
    # **Before `schedule_agent`, which does `from . import melon_branch as _MB` at module scope.**
    # This is the d3 melon/strawberry decision; without it the bundle cannot import.
    ("kagg.search.melon_branch", "kagg/search/melon_branch.py"),
    # **Before `schedule_agent`, which imports it at module scope.** Its rows are embedded in the
    # module itself: a submission has no `data/` directory to read them from.
    ("kagg.search.q4_branch", "kagg/search/q4_branch.py"),
    # **After `cover`, and it is not optional.** `cover.plan` does `from . import crew as CREW` on
    # every call to pick the assignment routine, so a bundle without it imports fine, passes the
    # entry-point check, and then dies with `ImportError: cannot import name 'crew'` on the first
    # observation of a real game. `crew` imports `cover` at module scope and `cover` imports `crew`
    # inside the function, so this is the order that resolves.
    ("kagg.search.crew", "kagg/search/crew.py"),
    ("kagg.search.router", "kagg/search/router.py"),
    # **`schedule_agent.py` bundled UNDER the name `kagg.search.schedule_agent`.** The two
    # files diverged at `6f31999` (2026-08-09) and `schedule_agent.py` has had none of the work
    # since: no `PLAN_THE_CREW_THAT_ARRIVES`, no `WALK_THE_LOAD_HOME`, no `NEVER_SELL_TODAYS_RATION`,
    # no `_clear_the_spawn_ring`. Every grid, gate and sweep in this repo runs `_1455mh`; shipping
    # the other one would ship a measurement nobody has taken -- the exact indirection between the
    # search space and the artifact that put `contrarian` on the ladder on 2026-08-07.
    #
    # The dotted name stays `kagg.search.schedule_agent` because the entry point below and the
    # loader resolve `_SA` by it, and because `_1455mh` itself imports only its three siblings
    # (`cover`, `router`, `routines`), all of which are bundled above.
    ("kagg.search.schedule_agent", "kagg/search/schedule_agent.py"),
)

#: Package stubs, created only where nothing real is already imported. Empty `__path__`, so an
#: import of anything NOT bundled fails loudly here instead of half-loading on the ladder.
PACKAGES = ("kagg", "kagg.economics", "kagg.search")

#: The schedule the planner runs. Thinned of the tape-only keys the agent never reads, so the
#: submission cannot accidentally depend on a replay it will not have.
#:
#: **2026-08-08: 90494364 -> 90976060. The shipped plan was calibrated for an economy that no longer
#: exists.** 90494364 was played on `townCenterSellInterval = 12`; the ladder runs 24 since the
#: 1.32.6 rebalance. Every `sells` row in it therefore assumes a town centre that drains the book
#: TWICE as fast as the real one, which is a mechanical explanation for the measurement in
#: `docs/the_shed_destroys_the_harvest_2026-08-08.md`: STRAWBERRY, MELON and WOOL driven to the $1
#: floor, wool below base on 558 of 719 turns, melon on 462. We were selling at a cadence the current
#: book cannot absorb.
#:
#: 90976060 is the same author on the CURRENT economy and is also his better game -- $128,518 against
#: 90494364's $110,820.
#:
#: **It also ends a measurement inconsistency worth naming.** Every fixture in the repo --
#: `scripts/handover.py`, `scripts/mirror`-style arms, `tests/test_the_shed_does_not_destroy_the_
#: harvest.py`, the reservation and price-aware measurements -- loads `TAPES["seb1326"]`, i.e.
#: 90976060, while this line shipped 90494364. So the local fixtures and the submission were
#: different agents, and their disagreement (mirror +2.9%, tape season -19%) was never about the sell
#: rule at all. One plan now, everywhere.
#: **VICTOR (91854176 seat 1), 2026-08-11.** Every fix in the eleven commits of 2026-08-11
#: was measured against THIS schedule and THIS tape on `scripts/breakdown.py --tape victor`.
#: Shipping 90976060 would put a planner tuned on one plan onto another -- the same
#: indirection between the search space and the artifact this file already records twice.
PLAN = _PLAN.SHIPPED_PLAN
#: Re-exported from `kagg.plan`, which owns it. Use `_PLAN.thin(row)`, never the comprehension.
TAPE_ONLY = _PLAN.TAPE_ONLY

#: The raw replay the plan was distilled from. `--replay-days N` embeds its author's ACTUAL per-turn
#: actions for days 0..N-1 and hands over to the planner on day N -- the shape `scripts/handover.py`
#: has measured all along and which, until 2026-08-09, was never available in a shipped artifact.
#:
#: **The schedule is a target sheet, not a tape.** `TAPE_ONLY` above strips `orders`, `plant_tiles`,
#: `build_tiles` and `land_turns`, so with `--replay-days 0` the submission holds no turn-level
#: action at all and re-derives every walk, plant and order itself from day 0. That is the shipped
#: behaviour and it is NOT what the handover fixture measures, which is why the same code reports a
#: 123-unit discard at handover-11 and 7 over a full season.
#:
#: The opening is board-dependent and the ladder's seed is not the one it was recorded on: a PLANT
#: onto a weed-spawned tile fails, and a SELL that filled at his prices may not fill at ours, so his
#: bank drifts and later purchases can fail. Weeds are rare (0.005) and the day-0 board is
#: deterministic -- 25 open tiles, 75 LOCKED, every seed -- so the opening should mostly land. That
#: is a measurement, not an assumption, and it is what building both artifacts is for.
#: **Pointed at the clone lineage on the `clone-lineage` branch, 2026-08-26.**
#: `data/logs/tape_reach.log`: grouping the 2026-08-25 field by its d0-d11 opening gives five
#: scripts, and this one -- `123c42fb5d`, 11 seats over ELEVEN DISTINCT SHOP DRAWS -- plays
#: **identical actions through d27**. That is not a tape that reaches further, it is an agent that
#: barely reads the board, which is exactly what a replay can reproduce.
#:
#: It is also the best of the five on the criterion that decides the ladder. On WIN RATE, not bank:
#:
#:     group        seats  WIN%  tape exact   mean bank
#:     123c42fb5d      11   55%      d27      $ 82,799
#:     356835aca0      29   48%      d12      $105,080
#:     d1f515b59d      49   45%      d14      $ 87,218
#:     62d81623f9      40   40%      d19      $ 84,045
#:     d198b9f673      10   30%      d11      $110,015
#:
#: The bank column runs the other way and is the trap this project has recorded since day one --
#: a $43k win and a $4k win score the same. Caveat: these seats largely play EACH OTHER, and when
#: both sides run one script one of them must lose, so intra-lineage rates sit near 50% by
#: construction. The ordering is suggestive, not decisive.
#:
#: Seat 1 of 98907591 is the best margin in the group, +$16,437 ($100,149 against $83,712), on its
#: own seed 123641874.
REPLAY = pathlib.Path("data/seed_scripts/clone_open/98907591.json")
REPLAY_SEAT = 1

#: **The three-way tape split, keyed on the shop draw.** `arm -> (recording, seat)`.
#:
#: The lineage plays three different seasons depending on when YARN_STORE unlocks, and the split is
#: buildable because the SIGNAL always arrives before the DIVERGENCE. Measured 2026-08-26,
#: `scripts/where_the_clone_tapes_split.py`, `data/logs/clone_split_points.log` -- first turn the
#: actions differ against first turn the shop lists differ:
#:
#:     pair                          actions split   shops differ   buildable
#:     clone_open vs clone_yarn3             d3h17          d3h00         YES
#:     clone_open vs clone_yarn6             d6h10          d3h00         YES
#:     clone_open vs clone_late              d6h21          d3h00         YES
#:     clone_yarn3 vs clone_yarn6            d3h17          d3h00         YES
#:     clone_yarn3 vs clone_late             d3h17          d3h00         YES
#:     clone_yarn6 vs clone_late             d6h10          d6h00         YES
#:
#: **All four tapes are byte-identical to d3h16**, so the first three days need no latch at all and
#: `ARM_DEFAULT` serves them. That ordering is what makes this safe, and it is the exact trap the
#: older `(melon_armed, q4_armed)` latch records at `schedule_agent.py:3826`: replaying a branch day
#: BEFORE its latch decides measured **mean -$96,897 over 14 games, better in only 2**.
#:
#: The key is read off `town["unlocked_shops"]`, which is exact -- not the 67.6% decision tree from
#: `scripts/learn_the_tape_selector.py`. That tree was fitted across 139 seats of five different
#: openings and answers a different question; here there are three tapes and the shop list names
#: which one directly.
#:
#: `clone_late` is deliberately NOT an arm. It parts from `clone_open` only at d6h21 and takes
#: YARN_STORE at d12, which is past every handover we ship; a fourth arm would add a branch that
#: the selector cannot distinguish from `clone_open` until after the opening has ended.
#: **Each arm carries its own stop day** -- the day the tape hands the season to the planner. A
#: single handover for all three throws away exact play on the arm that holds longest: `clone_open`'s
#: group (`123c42fb5d`, 11 seats over ELEVEN distinct shop draws) plays identical actions **through
#: d27** (`data/logs/tape_reach.log`), so stopping it at d12 replaces 15 days of exact tape with 15
#: days of approximation.
#:
#: The stop day per arm now comes from `STOP_TABLE`, measured. The values here are the LENGTH of
#: tape embedded, which must be at least the largest stop the table can ask for.
#: **The SCHEDULE is part of the arm, not a global.** `(recording, team, stop day, schedule)`.
#:
#: The planner does not plan from nothing -- it reads schedule rows, and those rows describe the
#: board the recording built. A bundle that replays `clone_yarn3`'s tape and then plans from
#: `kawashigi`'s rows hands the season to a planner describing a different lineage's farm, which is
#: what shipped until 2026-08-26: `PLAN = _PLAN.SHIPPED_PLAN` embedded one schedule for every arm.
#: The tape and the schedule are derived from the SAME recording and live in the same directory;
#: they must be selected together or the handover lands on rows that do not describe the board.
REPLAY_ARMS = {
    # **Raised 12 -> 28 on 2026-08-26 so the handover day can be MEASURED.** At 12 the bundle
    # embedded twelve days of yarn tape and no more, so a sweep that truncated the opening at d16,
    # d20, d24 and d28 truncated nothing and returned five identical seasons -- which reads exactly
    # like "the handover day does not matter" and is really "there was no tape there to move it
    # into". The stop day is now a real parameter on all three arms; where each one SHOULD sit is
    # what the sweep answers.
    "yarn3": (pathlib.Path("data/seed_scripts/clone_yarn3/98889302.json"), "WeAreFarmers", 28,
              pathlib.Path("data/seed_scripts/clone_yarn3/schedule.json")),
    "yarn6": (pathlib.Path("data/seed_scripts/clone_yarn6/98857364.json"), "Bharath Varma", 28,
              pathlib.Path("data/seed_scripts/clone_yarn6/schedule.json")),
    "open": (pathlib.Path("data/seed_scripts/clone_open/98907591.json"), "UjjwalPardeshi", 28,
             pathlib.Path("data/seed_scripts/clone_open/schedule.json")),
}
ARM_DEFAULT = "open"

#: **The stop day is per DRAW, not per arm.** Measured 2026-08-26,
#: `scripts/how_late_can_each_arm_hand_over.py`, `data/logs/handover_sweep2.csv` -- our bank against
#: the arm's own tape on four injected shop draws:
#:
#:     draw      arm         TAPE       d12       d16       d20       d24       d28    best
#:     yarn_d3   yarn3    126,577   103,572   109,079   116,406   118,770   120,581   d28  -5,996
#:     yarn_d6   yarn6    129,712   112,493   108,555   119,306   123,092   124,386   d28  -5,326
#:     yarn_d12  open     143,586   137,047   133,960   142,136   143,645   143,262   d24     +59
#:     yarn_d15  open      91,429    93,202    84,574    89,888    88,963    89,972   d12  +1,773
#:
#: The last two rows are the SAME ARM and they point opposite ways: on the `yarn_d12` draw the
#: planner should take over at d24-d26, and on the `yarn_d15` draw it should take over at d12 and
#: every later stop is below the tape. One stop day for `open` is wrong on one of those draws
#: whichever value is chosen.
#:
#: **This is buildable because the two decisions have different deadlines.** The TAPE must be picked
#: by d6, before the arms part at d6h09. The STOP DAY only binds when the season reaches it, so it
#: can be read at d12, by which time the draw has shown three more shops. `_stop` in the epilogue
#: reads it live and the agent is rebuilt if it moves.
#:
#: One seed per row. The ORDERING is what was measured; the dollar values run through an uncontested
#: market and are not quality numbers.
#: **Measured per YARN CLASS**, 18 draws sampled two per class from `daily_2026-08-26`, mean margin
#: against that arm's own tape on the same draw (`data/logs/handover_class.csv`):
#:
#:     yarn class  arm      n          d12       d20       d28   best
#:     yarn_d3     yarn3    2      -15,106    -6,124    -5,640   d28  -5,640
#:     yarn_d6     yarn6    2      -11,256    -2,876    -4,980   d20  -2,876
#:     yarn_d9     open     2      -19,358      -396    -1,426   d20    -396
#:     yarn_d12    open     2       -2,486      +258    -1,328   d20    +258
#:     yarn_d15    open     2         -376      +518      -770   d20    +518
#:     yarn_d18    open     2       +2,808      +716      -586   d12  +2,808
#:     yarn_d21    open     2         +266    +1,155      -516   d20  +1,155
#:     yarn_d24    open     2       -1,364      +882    -1,040   d20    +882
#:     yarn_none   open     2       +5,681      +848       +50   d12  +5,681
#:
#: Two rules fall out, and the second is the one that pays:
#:
#: - **Yarn early (d3, d6) -- our engine loses at every stop day.** Best case is -$2,876. The tape is
#:   simply better than us on those draws, so the stop goes as late as the tape reaches.
#: - **No yarn all season -- hand over at d12, worth +$5,681**, the largest margin in the table, on
#:   the largest class: 35 of 120 draws in the corpus have no YARN_STORE at all.
#:
#: `yarn_d18` preferring d12 is treated as noise: n=2, and both neighbours (d15, d21) prefer d20.
#:
#: **The stop day may be read LATE and the tape may not.** The tape is latched by d6, before the
#: recordings diverge at d3h16/d6h09; the stop only binds when the season reaches it, so "has yarn
#: appeared yet" can still be asked at d12. That asymmetry is what makes a no-yarn rule possible at
#: all -- at d6 there is no way to know yarn will never come.
#:
#: One seed per draw and two draws per class. The SHAPE is what was measured; the exact day is not
#: pinned closer than the d12/d20/d28 grid until the d14-d26 pass lands.
STOP_TABLE = {
    "yarn3": 28,
    "yarn6": 20,
    #: `open` splits on whether YARN_STORE has appeared at all by the time the stop is read.
    "open_yarn_seen": 20,
    "open_no_yarn": 12,
}

#: The first turn at which the arms are allowed to differ: **d3h16**, the earliest measured action
#: split (`clone_open` vs `clone_yarn3`). Everything before it is asserted identical across arms at
#: build time by `_openings`. The signal arrives at d3h00, sixteen turns earlier, which is the
#: margin that makes the latch honest rather than a guess.
#:
#: **d3h16, not d3h17.** `scripts/where_the_clone_tapes_split.py` reports d3h17 for the same turn
#: because it indexes `steps[t]` while `_opening` indexes `steps[1:][t]` -- step 0 is the initial
#: state and carries no action. The builder's convention is the one the shipped replay was verified
#: on, so it is the one that governs here. Set to 17, the build refuses with `arm 'yarn3' differs
#: at turn 88` -- which is this gate working, on its first run.
ARM_LATCH_TURN = 3 * 24 + 16

TARGET = pathlib.Path("submission/main.py")

PREAMBLE = '''\
# Generated by scripts/build_planner_submission.py -- do not edit.
# Edit kagg/search/*.py and rebuild, so the submitted file cannot drift from the tested one.
"""Kaggriculture: a covering day planner running a fixed seasonal schedule.

Every module below is a verbatim copy of its file in the repository. The loader installs them
under their real dotted names before the entry point runs, so the code here behaves exactly as
it does in the repository and in the tests.
"""

import json
import sys
import types

_ORDER = {order!r}
_PACKAGES = {packages!r}
_SOURCES = {{}}
'''

EPILOGUE = '''

def _install():
    """Put the embedded modules into `sys.modules` under their real names, in dependency order.

    Package stubs are created only where nothing is already imported, so loading this file inside
    the repository does not blind the rest of the process to `kagg.agents` or `kagg.arena`. The
    leaf modules are always installed from the embedded copies -- byte-identical to the repo, so
    overwriting is a no-op there and is the whole point everywhere else.
    """
    for name in _PACKAGES:
        if name not in sys.modules:
            pkg = types.ModuleType(name)
            pkg.__path__ = []          # nowhere to search: an unbundled import fails loudly
            sys.modules[name] = pkg
        head, _, tail = name.rpartition(".")
        if head:
            setattr(sys.modules[head], tail, sys.modules[name])
    for name in _ORDER:
        parent_name, _, short = name.rpartition(".")
        mod = types.ModuleType(name)
        mod.__package__ = parent_name     # what makes `from . import routines` resolve
        sys.modules[name] = mod
        setattr(sys.modules[parent_name], short, mod)
        exec(compile(_SOURCES[name], "<" + name + ">", "exec"), mod.__dict__)
    return sys.modules["kagg.search.schedule_agent"]


_SCHEDULE = json.loads(_PLAN_JSON)
_SA = _install()

# **The tape days, embedded.** A submission carries no `data/` tree, so `_replay_opening` would find
# no file, return `{}` as designed, and the replay would silently not happen -- an artifact that says
# it replays d4-d11 and does not. Only our own seat's `farmer`/`hands`/`market` for those days is
# needed, 23 KB a tape against a 30 MB replay file. JSON has no tuple keys, so the latch pair is
# stored as a two-element list and turned back into a tuple here.
_SA.EMBEDDED_OPENINGS = {tuple(json.loads(_k)): _v
                         for _k, _v in json.loads(_EMBEDDED_OPENINGS_JSON).items()}
# Same shape as `_SCHEDULE` above -- `json.loads` of the thinned rows, string keys and all. The keys
# are deliberately NOT converted: `_SCHEDULE` is built the same way and is what ships today, so a
# converted copy here would hand `make_agent` a differently-typed schedule on the split arms only.
_PLANS = json.loads(_PLANS_JSON)
_AGENTS = {}
_AGENT_ARM = {}
_ARM = {}


def _stop(obs, me, arm):
    """The day the tape hands over, read LIVE from the draw rather than fixed at build time.

    Measured per yarn class (see `STOP_TABLE` in the builder). The rule:

        arm yarn3                      -> 28    our engine loses at every stop; play the tape
        arm yarn6                      -> 20
        arm open, YARN_STORE seen      -> 20
        arm open, no YARN_STORE yet    -> 12    +$5,681, the biggest margin and the biggest class

    **This is read late ON PURPOSE, and it is the reason the no-yarn rule can exist at all.** The
    TAPE has to be latched by d6, before the recordings part at d3h16/d6h09. The STOP only binds
    when the season reaches it, so "has yarn appeared" can still be asked at d12 -- and at d6 there
    is no way to know yarn will never come. Two decisions, two deadlines.

    Not latched: as yarn arrives the answer moves 12 -> 20, which is correct. It can only move
    LATER, never earlier, so it can never retract a handover that has already happened.
    """
    if arm in _STOP_TABLE:
        return _STOP_TABLE[arm]
    seen = "YARN_STORE" in set(((obs.get("town") or {}).get("unlocked_shops")) or ())
    return _STOP_TABLE["open_yarn_seen"] if seen else _STOP_TABLE["open_no_yarn"]


def _arm(obs, me):
    """Which tape arm this game is on: `"yarn3"`, `"yarn6"` or `"open"`. Latched once, then frozen.

    The lineage plays a different season depending on when YARN_STORE unlocks, and the shop list is
    the whole signal -- read directly off `town["unlocked_shops"]`, no model and no guess:

        YARN_STORE present on day 3   -> "yarn3"    tapes part at d3h17
        YARN_STORE present on day 6   -> "yarn6"    tapes part at d6h10
        otherwise                     -> "open"

    Shops unlock on a fixed three-day cadence from d3, so the day-3 list holds exactly one shop and
    the day-6 list exactly two. The decision is therefore complete by d6h00, four turns before the
    latest arm needs it.

    **Latched, and never revisited.** YARN_STORE keeps unlocking on later days in every draw, so a
    rule re-evaluated each turn would flip an `"open"` game to `"yarn6"` the moment yarn arrived at
    d9 or d12 -- mid-replay, switching tapes under a board built by the other one. The arm is
    recorded per seat the first time day 6 is reached and read from the dict after that.

    Before the latch fires the arms are byte-identical (asserted at build time by `_openings`), so
    returning the default early cannot replay the wrong branch.
    """
    if me in _ARM:
        return _ARM[me]
    day = int(obs.get("day", 0) or 0)
    shops = set(((obs.get("town") or {}).get("unlocked_shops")) or ())
    if day < 3:
        return _ARM_DEFAULT
    if "YARN_STORE" in shops:
        arm = "yarn3" if day < 6 else "yarn6"
    elif day < 6:
        return _ARM_DEFAULT               # day 3 seen, no yarn: yarn6 is still open, do not latch
    else:
        arm = _ARM_DEFAULT
    _ARM[me] = arm
    return arm


def agent(obs, config=None):
    """Module-level entry point.

    **This must be the LAST callable defined in this file.** `kaggle_environments` does not look
    for a function called `agent`; `get_last_callable` execs the module and takes
    `[v for v in namespace.values() if callable(v)][-1]`. A `make_agent` helper defined below
    this one was therefore picked as the entry point and invoked as `make_agent(observation,
    configuration)`, which died on `int('remainingOverageTime')` -- the observation being iterated
    as if it were the schedule. The builder now asserts this ordering.

    Built lazily because the seat is not known until an observation arrives, and rebuilt at the
    top of day 0 so a process that plays more than one episode does not carry a season of pins
    and pen reservations into the next one.
    """
    me = int(obs.get("player", 0) or 0)
    fresh = int(obs.get("day", 0) or 0) == 0 and int(obs.get("hour", 0) or 0) == 0
    if fresh:
        _ARM.pop(me, None)
    arm = _arm(obs, me)
    # **The schedule travels with the tape.** `_PLANS` holds one thinned schedule per arm, read off
    # the same recording that arm replays. The agent is rebuilt when the latch resolves to a
    # different arm than the one it was constructed for -- which happens at most once, at d6, and
    # always before the handover, so the planner it hands to is the one that describes this board.
    stop = _stop(obs, me, arm) if _STOP_TABLE else _ARM_STOP.get(arm, _REPLAY_DAYS)
    # Rebuilt when EITHER the arm or the stop day moves. The stop is read live and can climb from 12
    # to 20 when yarn arrives, and `start_day` is fixed at construction -- an agent built for a d12
    # handover would otherwise catch up from the wrong day for the rest of the season.
    if _PLANS and _AGENT_ARM.get(me) not in (None, (arm, stop)):
        _AGENTS.pop(me, None)
    if fresh or me not in _AGENTS:
        # `start_day` exists only on the older `schedule_agent`. The module bundled here is
        # `schedule_agent`, which plans its opening rather than replaying one, and its
        # `make_agent` has no such parameter -- passing it unconditionally is a TypeError on the
        # first observation, i.e. a submission that banks the $3,000 start. Sent only when a replay
        # opening was actually asked for; `--replay-days` defaults to 0 and the builder refuses the
        # combination outright if the bundled module cannot honour it.
        sched = _PLANS.get(arm, _SCHEDULE)
        _kw = {"start_day": stop} if _REPLAY_DAYS else {}
        _AGENTS[me] = _SA.make_agent(sched, me, router=True, **_kw)
        _AGENT_ARM[me] = (arm, stop)
    live = _AGENTS[me](obs, config)

    # **The opening is replayed verbatim; the planner still SEES every turn.** It is driven above
    # unconditionally and its answer discarded during the opening, so its per-day state (pins, pen
    # reservations, the sold ledger) is warm at the handover. Constructing it fresh on day N
    # instead leaves `state["day"]` at -1 and it re-runs a whole first day inside day N.
    # **`day * 24 + hour`, NOT `obs["step"]`.** kaggle-environments gives `step` to seat 0 only --
    # at seat 1 it is None on every turn, so `obs.get("step", 0) or 0` was 0 for the whole season
    # and this replayed TURN 0 seven hundred and twenty times. Measured 2026-08-26: an artifact
    # built with `--replay-days 12` banked **$0** at seat 1 against $197,294, while seat 0 played
    # normally. Half of every ladder match is seat 1, so the feature was unusable from the day it
    # was written. `day` and `hour` are present and correct at both seats.
    step = int(obs.get("day", 0) or 0) * 24 + int(obs.get("hour", 0) or 0)
    # Cut to the stop day the draw asks for. `_OPENINGS` holds the full embedded tape; the slice is
    # what makes the handover a live decision rather than a build constant.
    opening = _OPENINGS.get(arm, _OPENING) if _OPENINGS else _OPENING
    opening = opening[:stop * 24] if _STOP_TABLE else opening
    if step < len(opening):
        farmer, hands, market = opening[step]
        owned = len((obs.get("farms") or [{}, {}])[me].get("hands") or [])
        # Truncated to the units this farm actually owns. The reference ignores a surplus unit
        # action for movement and work but still COUNTS it in the atomic-PLANT rule, so sending
        # more hand actions than we own blocks plants no real agent could block.
        return {"farmer": list(farmer), "hands": [list(h) for h in hands[:owned]],
                "market": [list(o) for o in market]}
    return live
'''


def _check_imports(name, path, text):
    """Every `kagg` import in the module -- at any depth -- must land on something bundled.

    This is the check that was missing. A grep of the file's top-level imports said the planner
    needed nothing outside `kagg/search/`, and it was wrong: `routines._crops_fertilizer_helps`
    imports `kagg.economics.production` from inside a function body, and the bundle would have
    imported fine in the repo (where an editable install answers the import) and died on the
    ladder. AST, not grep, and function bodies included.
    """
    import ast

    bundled = {n for n, _ in MODULES} | set(PACKAGES)
    package = name.rpartition(".")[0]
    bad = []
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.Import):
            wanted = [a.name for a in node.names if a.name.split(".")[0] == "kagg"]
        elif isinstance(node, ast.ImportFrom):
            root = package if node.level else (node.module or "")
            if node.level and node.module:
                root = f"{package}.{node.module}"
            if root.split(".")[0] != "kagg":
                continue
            # `from X import y` may name a module or an attribute; accept either reading.
            wanted = [f"{root}.{a.name}" if f"{root}.{a.name}" in bundled else root
                      for a in node.names]
        else:
            continue
        bad += [w for w in wanted if w not in bundled]
    if bad:
        raise SystemExit(
            f"{path}: imports {sorted(set(bad))}, which the bundle does not carry. "
            f"Add it to MODULES (and its package to PACKAGES) or the submission will die on Kaggle.")


def _literal(name, text):
    """Embed `text` verbatim as a raw triple-single-quoted literal, or refuse.

    Raw so no backslash in the source is reinterpreted, single-quoted because every docstring in
    these modules uses double quotes. Both assumptions are checked here rather than assumed: a
    quiet mangling would produce a file that imports and plays a subtly different game.
    """
    if "'''" in text:
        raise SystemExit(f"{name}: contains ''' and cannot be embedded raw")
    if text.rstrip("\n").endswith("\\"):
        raise SystemExit(f"{name}: ends in a backslash, which a raw literal cannot close")
    # No line continuation after the opening quotes: a raw literal keeps a trailing backslash
    # rather than swallowing the newline, which would prepend two stray characters to the module.
    return f"_SOURCES[{name!r}] = r'''{text}'''\n"


def _opening(days, path=None, team=None, seat=REPLAY_SEAT):
    """The replay author's own per-turn actions for days 0..days-1, as `(farmer, hands, market)`.

    Empty when `days` is 0, which is the historical behaviour: the submission then holds no
    turn-level action at all and the planner drives from day 0.

    `team` resolves the seat by name when given, because the three split arms come from three
    different recordings and the author does not hold the same seat in each -- a hard-coded
    `REPLAY_SEAT` would silently replay the OPPONENT's season on two of the three.
    """
    if not days:
        return []
    rep = json.loads((path or REPLAY).read_text())
    if team is not None:
        seat = rep["info"]["TeamNames"].index(team)
    steps = rep["steps"][1:]
    out = []
    for step in steps[:days * 24]:
        s = (step[seat] or {}) if seat < len(step) else {}
        a = s.get("action") or {}
        out.append([a.get("farmer") or ["PASS"],
                    list(a.get("hands") or []),
                    list(a.get("market") or [])])
    return out


def _openings(days):
    """`{arm: opening}` for every arm in `REPLAY_ARMS`, each cut to its OWN stop day.

    `days` is a CAP, not the length. Every arm replays `min(its own stop day, days)`, so
    `--replay-days 30` gives each arm its natural reach -- `open` to d28, `yarn3`/`yarn6` to d12 --
    while `--replay-days 12` still pins all three to d12 for a controlled comparison. One parameter,
    one meaning, and the old uniform behaviour is a value of it rather than a second switch.

    **The arms MUST agree over the turns before the latch can decide**, or the bundle replays a
    branch on information it does not have. `ARM_LATCH_TURN` in the epilogue is the first turn the
    selection is allowed to change the answer; every turn before it is asserted identical across
    arms here, at build time, so a future tape swap cannot reintroduce the blind-replay failure
    without the build refusing.
    """
    if not days:
        return {}
    out = {arm: _opening(min(stop, days), path, team)
           for arm, (path, team, stop, _sched) in REPLAY_ARMS.items()}
    base = out[ARM_DEFAULT]
    for arm, op in out.items():
        for t in range(min(ARM_LATCH_TURN, len(base), len(op))):
            if op[t] != base[t]:
                raise SystemExit(
                    f"arm {arm!r} differs from {ARM_DEFAULT!r} at turn {t} "
                    f"(d{t // 24}h{t % 24:02d}), which is BEFORE the latch decides at "
                    f"d{ARM_LATCH_TURN // 24}h{ARM_LATCH_TURN % 24:02d}. Replaying a branch before "
                    f"its signal arrives measured mean -$96,897 over 14 games "
                    f"(schedule_agent.py:3826). Refusing to build.")
    return out


def _embedded_openings():
    """`{"[melon_armed, q4_armed]": {step: [farmer, hands, market]}}` for the bundled agent.

    Read through the agent's own `_replay_opening`, so the bundle replays exactly what the repo
    replays -- a second extractor here is a second thing to keep in step, and the last time this
    file reconstructed something instead of copying it, the reconstruction was what shipped wrong.

    Returns `{}` when the agent is not configured to replay anything, which is the no-replay variant.
    """
    import importlib
    sa = importlib.import_module("kagg.search.schedule_agent")
    days = tuple(getattr(sa, "REPLAY_OPENING_DAYS", ()) or ())
    if not days:
        return {}
    out = {}
    for key, (tape, team) in sa.REPLAY_OPENING_TAPE.items():
        op = sa._replay_opening(days, tape, team)
        if not op:
            raise SystemExit(f"tape {tape} for latch {key} produced no opening; refusing to ship a "
                             f"bundle whose replay would silently do nothing")
        out[json.dumps([bool(key[0]), bool(key[1])])] = {str(s): list(v) for s, v in op.items()}
    return out


def build(replay_days=0, target=TARGET):
    sources = {}
    for name, path in MODULES:
        text = pathlib.Path(path).read_text()
        # **The substring scan for `__file__`, `open(`, `read_text` and `pathlib` is GONE.** It was a
        # grep, not an analysis: it could not tell a disk read on the shipped path from one behind a
        # switch that is off, and it refused to bundle `schedule_agent.py` for holding the tape replay
        # -- code that is unreachable with an empty `REPLAY_OPENING_DAYS`, and which returns `{}`
        # rather than raising when the file is absent, which is the case the gate was written for.
        #
        # A gate that blocks a legitimate build has to be paid for by deleting real work, and on
        # 2026-08-17 it was: the replay was removed from the agent to get a bundle out. That is a
        # worse failure than the one it prevents.
        #
        # What actually protects the bundle is downstream and empirical: the standalone import runs a
        # full 30-day season in a fresh namespace, the entry-point check resolves `agent()`, and the
        # `env.run` against `starter` refuses to ship anything that cannot beat it -- which is what
        # caught the artifact that banked exactly the $3,000 opening stake. A crash from a missing
        # `data/` tree cannot survive any of those.
        _check_imports(name, path, text)
        sources[name] = text

    def _thin(path):
        return {d: _PLAN.thin(row) for d, row in json.loads(path.read_text()).items()}

    thin = _thin(PLAN)
    # **One schedule per arm, from the SAME recording as that arm's tape.** The planner reads
    # schedule rows to decide the day, and those rows describe the board the recording built; an arm
    # that replays `clone_yarn3` and then plans from `kawashigi`'s rows hands over to a planner
    # describing a different farm. Paired by directory, so the tape and the rows cannot drift apart.
    plans = ({arm: _thin(sched) for arm, (_p, _t, _s, sched) in REPLAY_ARMS.items()}
             if replay_days else {})

    out = [PREAMBLE.format(order=[n for n, _ in MODULES], packages=list(PACKAGES))]
    out += [_literal(name, sources[name]) for name, _ in MODULES]
    arms = _openings(replay_days)
    opening = _opening(min(REPLAY_ARMS[ARM_DEFAULT][2], replay_days) if replay_days else 0)
    # **`start_day` is the EARLIEST handover, not the default arm's.** It guards the catch-up loop
    # in `make_agent`, which invents a day's debt for every schedule row before it; setting it to
    # `open`'s d28 would make the planner skip d12-d27 of catch-up on a game that latched to
    # `yarn3` and handed over at d12. The shortest arm is the only safe value.
    start = min((min(s, replay_days) for _a, _t, s, _sc in REPLAY_ARMS.values()),
                default=replay_days) if replay_days else 0
    out.append(f"_PLAN_JSON = r'''{json.dumps(thin, indent=0)}'''\n")
    out.append(f"_REPLAY_DAYS = {int(start)}\n")
    out.append(f"_OPENING = json.loads(r'''{json.dumps(opening)}''')\n")
    # The three shop-keyed arms. `_OPENING` above stays as the single-tape fallback so a bundle
    # built with an empty `REPLAY_ARMS` behaves exactly as it did before the split existed.
    out.append(f"_ARM_DEFAULT = {ARM_DEFAULT!r}\n")
    out.append(f"_OPENINGS = json.loads(r'''{json.dumps(arms)}''')\n")
    out.append(f"_PLANS_JSON = r'''{json.dumps(plans, indent=0)}'''\n")
    out.append(f"_STOP_TABLE = json.loads(r'''{json.dumps(STOP_TABLE if replay_days else {})}''')\n")
    out.append(f"_ARM_STOP = json.loads(r'''"
               f"{json.dumps({a: min(s, replay_days) for a, (_p, _t, s, _sc) in REPLAY_ARMS.items()} if replay_days else {})}''')\n")
    # The tape days the bundled agent will replay, extracted from the recordings on disk. Empty when
    # `REPLAY_OPENING_DAYS` is empty, which is the no-replay variant.
    out.append(f"_EMBEDDED_OPENINGS_JSON = r'''{json.dumps(_embedded_openings())}'''\n")
    out.append(EPILOGUE)
    text = "".join(out)

    _assert_verbatim(text, sources, thin)
    # **Per ARM, not one length.** This read `replay_days * 24` when every arm stopped on the same
    # day; with `open` running to d28 and the yarn arms to d12 it fired on the default arm being
    # 672 turns against a 720-turn cap, which is correct behaviour rather than a fault. Each arm is
    # now checked against its OWN stop day, so a recording that is short still refuses to build.
    for arm, (_p, _t, stop, _sc) in (REPLAY_ARMS.items() if replay_days else ()):
        want = min(stop, replay_days) * 24
        got = len(arms.get(arm) or ())
        if got != want:
            raise SystemExit(f"arm {arm!r} opening is {got} turns, expected {want} "
                             f"(stop day {min(stop, replay_days)})")
    if replay_days and len(opening) != min(REPLAY_ARMS[ARM_DEFAULT][2], replay_days) * 24:
        raise SystemExit(f"default opening is {len(opening)} turns, expected "
                         f"{min(REPLAY_ARMS[ARM_DEFAULT][2], replay_days) * 24}")
    target.parent.mkdir(exist_ok=True)
    target.write_text(text)
    return target


def _assert_verbatim(text, sources, thin):
    """Parse the generated file's own literals back and compare. Trust the round trip, not the code.

    This runs before the file is written, so a bundle that would have shipped a mangled module is
    never on disk to be submitted by mistake.
    """
    import ast

    tree = ast.parse(text)
    got = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Constant):
            continue
        target = node.targets[0]
        if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) \
                and target.value.id == "_SOURCES":
            got[ast.literal_eval(target.slice)] = node.value.value
        elif isinstance(target, ast.Name) and target.id == "_PLAN_JSON":
            got["__plan__"] = node.value.value

    for short, text_in in sources.items():
        if got.get(short) != text_in:
            raise SystemExit(f"{short}: embedded copy is not byte-identical to kagg/search/{short}.py")
    if json.loads(got.get("__plan__", "null")) != thin:
        raise SystemExit("the embedded schedule does not round-trip")


def standalone():
    """Import the built file from a directory with no repository in sight.

    This venv installs the repository as an EDITABLE package, which works through a `.pth` file
    that registers a finder on `sys.meta_path`. Neither `-I` nor emptying `sys.path` disables it,
    so the first version of this probe passed while quietly importing the real `kagg` -- a green
    check on exactly the thing it existed to rule out. The finder is removed by name before the
    bundle is loaded, which makes the process as blind to this repository as Kaggle is.
    """
    import subprocess
    import tempfile

    probe = (
        "import importlib.util, sys\n"
        # Strip the editable-install finder, then prove `kagg` is genuinely unreachable.
        "def _tag(f):\n"
        "    return (getattr(f, '__module__', '') + getattr(f, '__name__', '')\n"
        "            + type(f).__module__ + type(f).__name__).lower()\n"
        "sys.meta_path = [f for f in sys.meta_path if 'editable' not in _tag(f)]\n"
        # Drop only entries that actually contain a `kagg/` package. Matching the repo by NAME
        # also deleted this venv's site-packages, whose path contains "kaggriculture" too, and
        # took `kaggle_environments` down with it.
        "import os\n"
        "sys.path = [p for p in sys.path if not os.path.isdir(os.path.join(p or '.', 'kagg'))]\n"
        "try:\n"
        "    import kagg.arena\n"
        "    raise SystemExit('FAIL: the repository is still importable; probe proves nothing')\n"
        "except ImportError:\n"
        "    pass\n"
        f"spec = importlib.util.spec_from_file_location('sub', {str(TARGET.resolve())!r})\n"
        "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
        "installed = sorted(k for k in sys.modules if k == 'kagg' or k.startswith('kagg.'))\n"
        "for k in installed:\n"
        "    f = getattr(sys.modules[k], '__file__', None)\n"
        "    assert f is None, 'leaked a real file: ' + k + ' -> ' + str(f)\n"
        "assert callable(m.agent) and len(m._SCHEDULE) >= 29, len(m._SCHEDULE)\n"
        # Replicate `kaggle_environments.agent.get_last_callable` exactly: it execs the file and
        # takes the LAST callable in the namespace, not the one named `agent`. Getting this wrong
        # is silent -- the file imports, plays, and every game ends with a null reward.
        "ns = {}\n"
        f"exec(compile(open({str(TARGET.resolve())!r}).read(), 'sub', 'exec'), ns)\n"
        "last = [v for v in ns.values() if callable(v)][-1]\n"
        "assert last is ns['agent'], (\n"
        "    'the runtime would call ' + getattr(last, '__name__', repr(last))\n"
        "    + '(), not agent(): agent must be the LAST callable defined in the file')\n"
        "print('standalone import OK:', len(m._SCHEDULE), 'days;', ', '.join(installed))\n"
        "print('entry point OK: the last callable is agent()')\n"
    )
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp) / "probe.py"
        path.write_text(probe)
        env = {"PATH": "/usr/bin:/bin", "HOME": str(pathlib.Path.home()), "PYTHONPATH": ""}
        # `-E`, NOT `-I`. `-I` implies `-s`, which drops the USER site-packages -- and on a machine
        # where `kaggle_environments` is a user install (`~/Library/Python/3.x/...`, the default for
        # `pip install --user`) that made the probe unable to import it. The bundle imports it at
        # module scope, so every build failed with `ModuleNotFoundError: kaggle_environments`,
        # identically for the shipped agent, for an environmental reason that says nothing about the
        # artifact. Kaggle's runtime obviously HAS kaggle_environments -- it is what calls us.
        #
        # Blinding the probe to this REPOSITORY is the point, and that is not what `-I` was doing:
        # it is done by the meta_path strip, the `kagg/` path filter, `cwd=tmp` and `PYTHONPATH=""`,
        # and it is self-verifying -- the probe asserts `import kagg.arena` raises ImportError before
        # it loads the bundle, so a hole here fails loudly rather than passing a weakened check.
        r = subprocess.run([sys.executable, "-E", str(path)], cwd=tmp, env=env,
                           capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


#: Seed 11, weeds off, against Seb's replayed tape -- the season every number in `docs/` is
#: quoted on. `ours` is the gate; it must land to the dollar, because the environment is
#: deterministic given a seed and any drift at all means the bundle is not the measured code.
#:
#: The tape's own bank is recorded but NOT gated. It was $116,635 when the head-to-head was run
#: through `scripts/breakdown.py` and is $126,445 through this harness, on a season where our
#: side is bit-identical -- so the two harnesses differ in how they drive the REPLAY, not in how
#: they drive us. Gating on a number produced by a different harness would fail this build for a
#: property it is not testing. The bundle-versus-repo check below is the real equality test.
#: **Rebaselined 2026-08-08: 127,846 -> 71,894.** That figure was measured on env **1.32.2**, which
#: the ladder no longer runs. 1.32.6 halved the town centre's draw (`townCenterSellInterval` 12 -> 24)
#: and deleted the late-season demand ramp, so every bank in this project moved -- the same schedule
#: that banked $127,846 banks $63.5k on the new economy. Holding the old number gated every build
#: against an economy that does not exist.
#:
#: This is a tripwire, NOT the correctness check, and it is worth being explicit about that because
#: raising a reference to make a build pass is exactly how a regression gets shipped. The real test
#: is `ours == repo` on the line below: the bundle must reproduce the repo modules to the dollar.
#: That passed at $71,894 on both sides before this constant was touched, which is what makes the
#: rebaseline a record of a changed environment rather than a loosened gate.
#:
#: Also live in this build, and the reason the number is not simply "the old code on the new env":
#: `PRICE_AWARE_SELL_CAP = True` (see its docstring for the five-seed evidence).
#: **71,894 -> 58,104 on 2026-08-08** when `RESERVATION_SELL_CAP` was enabled. Recorded rather than
#: waved through: this fixture is DOWN 19% while the two that motivated the flag are up (mirror
#: 62,868 -> 64,667, handover +$2,822). Three fixtures, two up small, one down large -- the flag went
#: to the ladder on that mixed evidence deliberately, because the arena pool is saturated at 94.4%
#: and cannot discriminate a sell rule at all. If the ladder rating falls, this line is the first
#: thing to look at and the flag is the first thing to turn off.
#: **58,104 -> 57,595 on 2026-08-08** when the WHEAT feed reserve stopped counting `ripe_wheat`
#: (standing crop) as though it were feed. Flat on this fixture; the gain is elsewhere -- the herd now
#: matches the tape exactly (13 cows to 13, was 7), land parcel 3 moves d16 -> d12, and the mirror
#: goes 64,667 -> 69,228.
#: **57,595 -> 77,885 on 2026-08-08, +35%**, when `PLAN` moved off the 1.32.2-economy schedule
#: (90494364, `townCenterSellInterval = 12`) onto the same author's 1.32.6 game (90976060, interval
#: 24). The old plan's sell rows assumed a town centre draining the book twice as fast as the real
#: one; the new plan halves WOOL (230 -> 104) and cuts MELON (132 -> 96) -- the two steep `sq` price
#: curves we were driving to the $1 floor -- and puts the volume into MILK (179 -> 303), the one
#: product measured never to trade below base all season.
#: **Rebaselined 2026-08-09: 77,885 -> 75,595.** Alex's call, made explicitly after the figure was
#: surfaced. The drift was NOT new that day -- it had been invisible because `standalone()` launched
#: its probe with `python -I`, which drops user site-packages and so could not import
#: `kaggle_environments`. Every build died at the import probe and never reached this check. Fixing
#: the probe is what exposed it, which is worth remembering: a gate that cannot run is not a gate
#: that passes, and this one had been dark long enough for the season to move $2,290 underneath it.
#: **RE-MEASURED 2026-08-11: 75595 was stale and had been failing every build, including HEAD's.**
#: Built from a detached worktree at `9f1f25e` with no working-tree changes at all, this same check
#: reported `tape season: bundle $17,170 ... reference $75,595` and `BUILD FAILED`. A tripwire that
#: fires on an unmodified baseline is not detecting a regression, it is detecting its own staleness,
#: and while it is red it cannot report a real one -- which is the same "a gate that cannot run is
#: not a gate that passes" failure recorded directly above, one rung further along.
#:
#: The number moved because the fixture's economy did: it was measured against a
#: `townCenterSellInterval` of 12 and the ladder has run 24 since 2026-08-08, so the town drains a
#: fraction of what the constant assumes and the same play banks far less.
#:
#: This is NOT a tolerance added to make a gate pass -- the real check, `ours == repo`, is untouched
#: and still demands the bundle reproduce the repo modules to the dollar. It passed on both builds.
#: What is re-anchored is only the absolute figure, to the current tree measured on the current
#: economy. Re-measure it whenever the environment version moves, and record the version here.
#: Re-anchored 2026-08-11 (evening) after twelve commits and the swap of PLAN to Victor.
#: The previous $24,603 was measured on the 90976060 plan and is not comparable.
#: **Rebaselined 2026-08-13: 89,054 -> 87,927, a DELIBERATE -$1,127.** `LATE_SEASON_PAIR` and the
#: re-solved d26-d29 routes (`67d639d`) change the late season on purpose: fertilize stops at d26,
#: Seed and market interval for the reproduce harness. **No season figure: the `ours` tripwire was
#: removed 2026-08-13** -- see `reproduce()` for why a dollar equality on one seed against one tape
#: is the wrong thing to gate a ship on when the ladder scores Elo. Season money is printed by
#: `reproduce()` for reading, and nothing asserts it.
REFERENCE = {"seed": 11, "interval": 24}

#: `actTimeout` is 1s per turn, but `remainingOverageTime` is a 60s bank for the whole episode and
#: disqualification happens only when the bank goes negative. So the constraint is total overage,
#: not the worst turn -- the day solve is always going to cost more than a second.
ACT_TIMEOUT, OVERAGE_BANK = 1.0, 60.0

#: **The local overage is not the number that matters, and reporting it alone shipped a
#: disqualification.** Submission 55352401 measured 2.8s of overage here and was charged 61.7s on
#: the ladder, which is not the ~2x a "slower worker" intuition suggests. The charge is
#: `max(0, t - 1)` per turn, so it is not linear in machine speed: a 3.8x slower box drags a whole
#: cohort of 0.3-0.9s turns across the one-second line AND charges for each of them. Same season,
#: same code, 22x the bill.
#:
#: 3.8x is measured, not assumed -- worst turn 7.39s on Kaggle against 1.96s here, on the same
#: agent. The gate charges at 6x so there is real headroom above the observed figure rather than a
#: margin chosen by feel, which is the mistake the first release made.
#: **6.0, and it was lowered to 3.8 once and that submission died. Do not lower it again.**
#:
#: 2026-08-09: `main_replay11.py` was built with this at 3.8 (the then-"measured" ladder slowdown)
#: and shipped. Episode 91304798 ran 530 turns of 719 and returned SubmissionStatus.ERROR with no
#: stderr -- a pure timeout. The evidence, from the episode's own per-turn durations:
#:
#:     local worst turn   1.252s        ladder worst turn   6.386s      => 5.1x, not 3.8x
#:     turns over 1s: 28          slowest: d11h1 6.39s, d18h1 5.79s, d15h1 5.53s
#:
#: 3.8x had been read off a different, LIGHTER agent; the multiplier is not a constant of the box,
#: it grows with the work a turn does, so the plain planner's 3.8x said nothing about a build whose
#: dawn solve is 4x heavier. 6.0 covered the real 5.1 and would have refused this build. It did
#: refuse it. That refusal was overridden and the experiment was lost.
KAGGLE_SLOWDOWN = 6.0


def _season(policy, days=30, seed=None):
    """Play `policy` against a recorded tape and return (our bank, tape bank, per-turn seconds).

    The tape only supplies an OPPONENT to time against and to play a full season into. Nothing is
    asserted about the money: the season tripwire was removed on 2026-08-13 (see the note on `ok`),
    and the surviving gate is `ours == repo`, a statement about bundling. `seb` was retired from
    `breakdown.TAPES`, and this reference was not moved with it -- the build died on
    `KeyError: 'seb'` after every other gate had already passed.
    """
    import time

    from kaggle_environments import make

    from scripts.breakdown import TAPES, tape_policy

    replay, _schedule, team = TAPES["kawashigi"]
    env = make("kaggriculture",
               configuration={"seed": seed or REFERENCE["seed"], "weedSpawnChance": 0.0})
    env.reset(2)
    opp = tape_policy(replay, team, 1)

    times = []
    for t in range(24 * days):
        if env.done:                      # the env closes the season itself; do not step past it
            break
        o0, o1 = env.state[0].observation, env.state[1].observation
        clock = time.perf_counter()
        a0 = policy(o0)
        times.append(time.perf_counter() - clock)
        a1 = opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    farms = env.state[0].observation["farms"]
    return round(float(farms[0]["money"])), round(float(farms[1]["money"])), times, team


def plays_a_real_game(seed=700):
    """Hand the FILE to `env.run`, the way the arena and Kaggle do, and require a real reward.

    Everything above drives `bundle.agent` directly, which is a different calling convention from
    the one the ladder uses: `env.run` picks the entry point itself, enforces `actTimeout`, and
    sets `reward = None` for an agent that errors, times out, or returns a malformed action. So a
    file can pass every check above and still score nothing -- which is exactly what happened, and
    `run_arena`'s own gate is what caught it. A null reward here is a build failure.
    """
    from kaggle_environments import make

    env = make("kaggriculture", configuration={"seed": seed}, debug=True)
    env.run([str(TARGET), "starter"])
    final = env.steps[-1]
    reward, status = final[0]["reward"], final[0]["status"]
    # **`starter` is the partner here on purpose, and it is NOT the quality gate.** It banks ~$3,512
    # and tuning against it reads roughly 2x reality, so it can only ever answer "did this file run
    # at all". That is precisely the question this function exists to ask: a bundle that fails to
    # import banks exactly the $3,000 start, and one that errors or times out gets `reward = None`.
    # The strength gate is `beats_the_repo_agent()` below, against a real opponent over many seeds.
    #
    # The threshold is the project's own kill criterion -- an agent that cannot clear $20k against
    # the weakest thing in the game is broken, not merely worse.
    ok = status == "DONE" and reward is not None and reward > 20_000.0

    # **The same file again, SEATED SECOND.** This check ran only as player 0 for its whole life,
    # and that is what let a `--replay-days` artifact ship "verified" while banking $0 in half its
    # games: the shipped epilogue indexed its replay opening on `obs["step"]`, which
    # kaggle-environments provides to seat 0 only, so at seat 1 it replayed turn 0 for all 720
    # turns. Every other check here -- the import, the entry point, `reproduce()`, and
    # `beats_the_repo_agent`'s own driving -- reads `farms[0]` or drives the agent directly, so not
    # one of them could reach the defect.
    #
    # A ladder match seats us second half the time, so a file that only works first is broken, not
    # merely worse. This is the cheapest possible statement of that: one more `env.run`.
    env2 = make("kaggriculture", configuration={"seed": seed}, debug=True)
    env2.run(["starter", str(TARGET)])
    f2 = env2.steps[-1]
    reward1, status1 = f2[1]["reward"], f2[1]["status"]
    ok1 = status1 == "DONE" and reward1 is not None and reward1 > 20_000.0
    if not ok1:
        print(f"  SEAT 1: status {status1}, reward "
              f"{'null' if reward1 is None else f'${reward1:,.0f}'} -- REFUSED")
    else:
        print(f"  seat 1 OK: ${reward1:,.0f}")
    return (ok and ok1), status, reward, final[1]["reward"]


def beats_the_repo_agent(seeds=(4001, 4002, 4003, 4004, 4005, 4006), floor=0.40):
    """The real quality gate: the BUILT FILE against the repo's current agent, both seats.

    `starter` cannot rank anything -- it sells almost nothing, so the market is never contested and
    every number against it is roughly 2x reality. The tape field cannot rank anything either: it
    returned 100.0%, 100.0% and 99.4% for three materially different agents
    (`data/logs/tape_gate_three.log`), because a tape is open-loop and cannot contest a book it did
    not expect to be contested.

    A mirror against the repo modules can. Both sides sell into one shared book on the same turns,
    which is the condition that actually separates two versions of this agent, and it is also what
    Kaggle validation runs. The opponent is written out as a thin wrapper that imports the repo
    rather than a pinned copy, so the gate is always "is the bundle at least as good as what is in
    the tree", with nothing to keep up to date.

    `floor` is deliberately below 0.5: the bundle and the repo agent are meant to be the SAME agent,
    so this is a regression tripwire for a packaging fault, not a search criterion. Use
    `scripts/mirror_gate.py` to decide whether a CHANGE is an improvement -- it reports a paired
    margin and a t-statistic, which is the measurement that can actually tell 78% from noise.
    """
    from kaggle_environments import make

    opponent = TARGET.parent / "_repo_opponent.py"
    opponent.write_text(
        "import json, pathlib\n"
        "from kagg.search.schedule_agent import make_agent\n"
        f"_P = pathlib.Path({str(PLAN.resolve())!r})\n"
        "_S = {int(k): v for k, v in json.loads(_P.read_text()).items()}\n"
        "_DROP = ('plant_tiles', 'build_tiles', 'land_turns', 'orders')\n"
        "_T = {d: {k: v for k, v in r.items() if k not in _DROP} for d, r in _S.items()}\n"
        "_A = {}\n"
        "def agent(obs, config=None):\n"
        "    me = obs['player']\n"
        "    if me not in _A:\n"
        "        _A[me] = make_agent(_T, me, router=True)\n"
        "    return _A[me](obs)\n"
    )
    try:
        w = d = ln = 0
        for seed in seeds:
            for ours_first in (True, False):          # both seats: a seat edge is not skill
                env = make("kaggriculture", configuration={"seed": seed}, debug=False)
                pair = ([str(TARGET), str(opponent)] if ours_first
                        else [str(opponent), str(TARGET)])
                env.run(pair)
                final = env.steps[-1]
                mine = final[0 if ours_first else 1]["reward"]
                theirs = final[1 if ours_first else 0]["reward"]
                if mine is None:
                    return False, 0.0, "the bundle returned a null reward -- error or timeout"
                if mine > theirs:
                    w += 1
                elif mine == theirs:
                    d += 1
                else:
                    ln += 1
        n = max(1, w + d + ln)
        rate = (w + 0.5 * d) / n
        return rate >= floor, rate, f"W{w} D{d} L{ln} over {n} games"
    finally:
        opponent.unlink(missing_ok=True)


def reproduce(days=30, replay_days=0, verbose=True):
    """Play the BUILT FILE, and the repo modules, through one identical harness.

    The point is the word *built*. Every season number in `docs/` was produced by importing
    `kagg.search.schedule_agent` directly; none of them says anything about the artifact that
    gets uploaded. This plays the artifact, then plays the repo the same way, and requires the
    two to agree to the dollar -- which is a statement about the bundling, and is the only thing
    this script is in a position to prove.
    """
    import importlib.util
    import json as _json
    import pathlib as _pathlib

    spec = importlib.util.spec_from_file_location("_bundle", TARGET.resolve())
    bundle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bundle)

    ours, tape, times, team = _season(bundle.agent, days=days)

    # The repo, driven the way every doc in this project drove it.
    from kagg.search import schedule_agent as SA

    # **`PLAN`, not a tape name.** This must be the SAME schedule the bundle embeds or the equality
    # check below compares two different agents and can never pass -- which is exactly what a
    # hard-coded `TAPES["seb"]` did the moment `PLAN` moved to 90976060.
    sched = {int(k): v for k, v in _json.loads(PLAN.read_text()).items()}
    thin = {d: _PLAN.thin(r) for d, r in sched.items()}
    # **The repo side must be given the SAME opening as the bundle**, or a replay build compares two
    # deliberately different agents and the gate can never pass -- which is not a finding, it is the
    # harness measuring the change it was told to make. This mirrors the epilogue exactly: the live
    # planner is called on every turn so its clock and ledger stay warm, its answer is discarded for
    # the replayed days, and `start_day` stops the missed-row catch-up inventing debt for days
    # somebody else played (see `schedule_agent.make_agent`).
    # Same conditional as the bundled entry point: `start_day` belongs to the older
    # `schedule_agent`, and the module bundled here plans its opening rather than replaying one.
    # **The repo side is built per ARM too, schedule and stop day together.** Comparing a bundle that
    # picks one of three schedules against a repo agent pinned to `PLAN` measures the difference the
    # harness itself introduced. Built lazily at the latch, exactly as the bundle does.
    _repo_plans = ({a: {d: _PLAN.thin(r)
                        for d, r in _json.loads(sc.read_text()).items()}
                    for a, (_p, _t, _s, sc) in REPLAY_ARMS.items()} if replay_days else {})
    _repo_stop = ({a: min(s, replay_days)
                   for a, (_p, _t, s, _sc) in REPLAY_ARMS.items()} if replay_days else {})
    _repo_agents = {}
    opening = _opening(min(REPLAY_ARMS[ARM_DEFAULT][2], replay_days)) if replay_days else []
    # The repo side gets the SAME arms and the SAME latch as the bundle, for the same reason it gets
    # the same opening: a harness that plays one tape against a bundle that picks between three is
    # comparing two agents, and any difference it reports is its own.
    arms = _openings(replay_days) if replay_days else {}
    latched = {}

    def _repo_arm(obs):
        if 0 in latched:
            return latched[0]
        day = int(obs.get("day", 0) or 0)
        shops = set(((obs.get("town") or {}).get("unlocked_shops")) or ())
        if day < 3:
            return ARM_DEFAULT
        if "YARN_STORE" in shops:
            latched[0] = "yarn3" if day < 6 else "yarn6"
        elif day < 6:
            return ARM_DEFAULT
        else:
            latched[0] = ARM_DEFAULT
        return latched[0]

    def repo_play(obs):
        a = _repo_arm(obs)
        # **The repo side reads the stop day LIVE, exactly as the epilogue's `_stop` does.** It did
        # not, and the build refused with "the bundle does not reproduce the measured season" --
        # correctly, because a bundle whose handover moves with the draw and a repo agent whose
        # handover is fixed per arm are two different agents and the reproduce check compares them
        # turn for turn. Mirrored rather than approximated: same table, same fallback.
        if STOP_TABLE and replay_days:
            if a in STOP_TABLE:
                st = STOP_TABLE[a]
            else:
                _seen = "YARN_STORE" in set(((obs.get("town") or {}).get("unlocked_shops")) or ())
                st = STOP_TABLE["open_yarn_seen" if _seen else "open_no_yarn"]
        else:
            st = _repo_stop.get(a, replay_days)
        key = (a, st)
        if key not in _repo_agents:
            _repo_agents.clear()          # one arm at a time, mirroring the bundle's rebuild
            _repo_agents[key] = SA.make_agent(
                _repo_plans.get(a, thin), 0, router=True,
                **({"start_day": st} if replay_days else {}))
        live = _repo_agents[key](obs)
        op = arms.get(a, opening) if arms else opening
        op = op[:st * 24] if (STOP_TABLE and replay_days) else op
        # Same index as the bundled epilogue: `day * 24 + hour`, never `obs["step"]`. This side
        # always plays SEAT 0, where `step` happens to be present -- which is precisely why the
        # verification passed while the shipped artifact banked $0 at seat 1. A gate only tests
        # what it exercises.
        step = int(obs.get("day", 0) or 0) * 24 + int(obs.get("hour", 0) or 0)
        if step < len(op):
            farmer, hands, market = op[step]
            owned = len((obs.get("farms") or [{}, {}])[0].get("hands") or [])
            return {"farmer": list(farmer), "hands": [list(h) for h in hands[:owned]],
                    "market": [list(o) for o in market]}
        return live

    repo, repo_tape, _t, _team = _season(repo_play, days=days)

    overage = sum(max(0.0, s * KAGGLE_SLOWDOWN - ACT_TIMEOUT) for s in times)
    local = sum(max(0.0, s - ACT_TIMEOUT) for s in times)
    if verbose:
        # Season money is REPORTED, never asserted -- see the note on `ok` below.
        print(f"tape season: bundle ${ours:,} vs {team} ${tape:,}  "
              f"(repo modules ${repo:,} vs ${repo_tape:,})")
        print(f"turn time over {len(times)} turns: worst {max(times) * 1000:.0f} ms, "
              f"mean {sum(times) / max(len(times), 1) * 1000:.0f} ms, "
              f"turns over {ACT_TIMEOUT:.0f}s: {sum(s > ACT_TIMEOUT for s in times)}")
        # Where the slow turns are matters more than how slow. The planner solves the whole day at
        # dawn and replays the committed tour for the other 23 hours, so cost concentrates on
        # hour 0 and grows with the crew and the tile count.
        slow = sorted(((s, i) for i, s in enumerate(times)), reverse=True)[:6]
        print("slowest turns: " + ", ".join(
            f"d{i // 24}h{i % 24} {s * 1000:.0f}ms" for s, i in slow))
        print(f"overage bank: {local:.1f}s here, {overage:.1f}s projected at {KAGGLE_SLOWDOWN:.0f}x "
              f"(measured ladder slowdown 3.8x), against a {OVERAGE_BANK:.0f}s bank")
        for f in (2, 3, 3.8, 5, 6, 8):
            o = sum(max(0.0, s * f - ACT_TIMEOUT) for s in times)
            print(f"    at {f:>3}x slower: worst {f * max(times):5.2f}s  "
                  f"turns over 1s {sum(s * f > ACT_TIMEOUT for s in times):3d}  "
                  f"overage {o:6.1f}s  {'ok' if o < OVERAGE_BANK else 'DISQUALIFIED'}")
    # **`ours == repo` is the whole gate, and it is the only claim this script can prove.** The
    # artifact must reproduce the repo modules to the dollar; that is a statement about BUNDLING,
    # which is what this file exists to verify.
    #
    # **The REFERENCE season tripwire was removed 2026-08-13, permanently, on Alex's call.** It
    # required `ours == REFERENCE["ours"]` -- a dollar equality against ONE seed and ONE tape -- so
    # it gated shipping on exactly the criterion CLAUDE.md says never to select on: the ladder is an
    # Elo rating, and a $43k win and a $4k win score the same. It blocked a build whose measured
    # effect flips sign with the opponent (+$4,194 against the victor tape, -$5,478 against Seb),
    # i.e. it was one draw of a two-sided distribution quoted to the dollar and treated as a verdict.
    #
    # What still gates a build, all of it stronger than a season total: the bundle imports
    # standalone, plays a real game to DONE, beats `starter`, wins >= a floor against the repo's own
    # agent over both seats, and reproduces the repo modules exactly. Season money is now REPORTED
    # and never asserted.
    ok = (ours == repo)
    return ok, ours, tape, overage


if __name__ == "__main__":
    import argparse

    _ap = argparse.ArgumentParser()
    _ap.add_argument("--replay-days", type=int, default=0,
                     help="embed the replay author's OWN actions for days 0..N-1 and hand over to "
                          "the planner on day N. 0 (default) is the historical behaviour: the "
                          "planner drives from day 0 and no turn-level action is shipped at all.")
    _ap.add_argument("--out", default=str(TARGET),
                     help="where to write, so both artifacts can exist side by side")
    _ap.add_argument("--days", type=int, default=30, help="days for the reproduce check")
    _args = _ap.parse_args()

    # Rebound so `standalone()`, `plays_a_real_game()` and `reproduce()` verify the file that was
    # just built rather than whatever is at the default path. They all read TARGET at call time.
    TARGET = pathlib.Path(_args.out)
    # **Refuse to ship a dev instrument that RAISES.** `crew.STRICT_FEASIBILITY` turns a day the
    # planner cannot fully cover into an `InfeasibleDay` exception. That is the right behaviour on a
    # workstation, where an uncovered day should stop the run and be looked at, and it is fatal on
    # the ladder: `kaggle_environments` marks a raising agent as errored and the season ends where
    # it threw. It currently trips on day 8 at seed 11.
    _crew_src = pathlib.Path("kagg/search/crew.py").read_text()
    if "\nSTRICT_FEASIBILITY = True" in _crew_src:
        sys.exit("refusing to build: kagg/search/crew.py has STRICT_FEASIBILITY = True.\n"
                 "  It raises InfeasibleDay on a day the planner cannot cover, which on Kaggle is a\n"
                 "  dead agent from that day on. Set it False to ship, or bundle a crew that has it\n"
                 "  off. This is a deliberate refusal, not a failure -- nothing has been written.")
    # **Refuse a replay opening the bundled module cannot honour**, rather than emitting a file that
    # raises `TypeError` on its first observation and banks the $3,000 start. `start_day` is a
    # parameter of the OLD `schedule_agent`; `MODULES` above bundles `schedule_agent`, which
    # plans its opening instead of replaying one.
    if _args.replay_days:
        import inspect as _inspect
        _agent_src = pathlib.Path(dict((d, p) for d, p in MODULES)["kagg.search.schedule_agent"])
        if "start_day" not in _agent_src.read_text().split("def make_agent", 1)[-1].split(")", 1)[0]:
            sys.exit(f"--replay-days {_args.replay_days} was asked for, but {_agent_src} has no "
                     f"`start_day` on make_agent. Bundle a module that does, or build with 0.")
    path = build(replay_days=_args.replay_days, target=TARGET)
    if _args.replay_days:
        print(f"opening: replayed to each arm's own stop day, capped at {_args.replay_days}")
        for _a, (_p, _t, _s, _sc) in REPLAY_ARMS.items():
            _d = min(_s, _args.replay_days)
            print(f"  arm {_a:<7}{_p.name:<16}tape d0-d{_d - 1}, planner from d{_d}"
                  f"{'   (default)' if _a == ARM_DEFAULT else ''}")
    print(f"wrote {path} ({len(path.read_text().splitlines())} lines, "
          f"{path.stat().st_size / 1024:.0f} KB)")
    ok, out = standalone()
    print(out)
    if not ok:
        print("BUILD FAILED: the bundle does not import on its own", file=sys.stderr)
        sys.exit(1)
    ok, status, reward, opp = plays_a_real_game()
    print(f"env.run vs starter: status {status}, reward "
          f"{'null' if reward is None else f'${reward:,.0f}'} vs "
          f"{'null' if opp is None else f'${opp:,.0f}'}")
    if not ok:
        print("BUILD FAILED: the runtime does not get a valid game out of this file",
              file=sys.stderr)
        sys.exit(1)

    ok, rate, detail = beats_the_repo_agent()
    print(f"vs the repo agent, both seats: {detail}, win rate {100 * rate:.1f}%")
    if not ok:
        print(f"BUILD FAILED: the bundle wins only {100 * rate:.1f}% against the repo's own agent. "
              f"They should be the SAME agent, so this is a packaging fault, not a strategy one.",
              file=sys.stderr)
        sys.exit(1)

    ok, ours, tape, overage = reproduce(days=_args.days, replay_days=_args.replay_days)
    if not ok:
        print("BUILD FAILED: the bundle does not reproduce the measured season", file=sys.stderr)
        sys.exit(1)
    if overage > OVERAGE_BANK:
        print(f"BUILD FAILED: {overage:.1f}s of projected overage at {KAGGLE_SLOWDOWN:.0f}x "
              f"against a {OVERAGE_BANK:.0f}s bank -- this is what a TIMEOUT looks like before "
              f"it happens", file=sys.stderr)
        sys.exit(1)
    print("submission verified")
