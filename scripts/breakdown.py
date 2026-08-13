"""Every number, ours AND the tape's, side by side, for each day. No deltas, no selection.

`scripts/fidelity.py` prints eight scalars as differences, which is right for finding the day a run
parts but wrong for reading what actually happened -- a delta of 0 hides whether both sides had two
cows or twenty, and a summary that shows only the fields that look good is worthless.

This prints the raw pair `ours/tape` for:

    board       money, hands, tiles owned, pens, live crop tiles PER CROP, weeds
    herd        animals standing in a pen PER SPECIES
    shed        units held PER PRODUCT, fertilizer included
    ops         every op either side emitted that day, counted -- EXCEPT sell, buy_product,
                buy_animal and buy_seed, which are FILLS (see below), not raw counts of what
                was emitted

    An emitted order is not a landed one: our agent re-offers an order every turn until it lands,
    because the env silently refuses one it can't afford, so counting emissions inflates any row
    that gets re-offered. sell/buy_product/buy_animal settle straight against `private["shed"]`
    (`_commit_unit` in `reference/kaggriculture.py`), so a turn's shed delta IS the fill -- PROVIDED
    no DROP/PICKUP/PLACE for that item also fired that turn (they touch the same field). Turns where
    that can't be guaranteed are dropped, not guessed, so these three rows are a LOWER BOUND, with
    the fraction of clean turns printed as "fill coverage". buy_seed is the same idea against
    `private["seeds"]`, which only DROP/PICKUP/PLACE never touch, so it has no coverage caveat.

    python -u scripts/breakdown.py --days 11
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys

sys.path.insert(0, ".")

#: Bound in `main()` from `--module`. The comparison is worthless if it silently runs a different
#: agent than the one under discussion, and this file hardcoded `schedule_agent` while every base
#: decision in the project was about `schedule_agent_1455*`.
schedule_agent = None

TAPES = {
    # Downloaded 2026-08-07 21:16. Seb WINS this one 143,772 to Leon Christians' 127,114 and holds all
    # four quadrants to Leon's three. A materially more aggressive plan than `seb` below: land on days
    # 4, 6 and 10 against 5, 9 and 11, and 23 pens against ~15.
    # Its `configuration` records `townCenterSellInterval = 12`, i.e. it was played on the PRE-rebalance
    # economy -- same as the ladder, which had not picked up 1.32.6 as of that evening. Check that field
    # on any future download before trusting a comparison against it.
    "seb2": ("data/seed_scripts/top_guys/90751101.json",
             "data/seed_scripts/top_guys/90751101/schedule.json", "Seb (allegedly)"),
    # Seb on the REBALANCED economy (townCenterSellInterval 24), banking $128,518 against
    # kakuteki's $70,886. The first tape we have of a top player on the game now being played.
    # Against `seb` below he moves the second parcel to day 6, builds 21 pens instead of 19,
    # and re-cuts the herd from wool to milk: MILK 179 -> 303, WOOL 230 -> 104, MELON 132 -> 96.
    "seb1326": ("data/seed_scripts/top_guys/90976060.json",
                "data/seed_scripts/top_guys/90976060/schedule.json", "Seb (allegedly)"),
    # Downloaded 2026-08-09 by Alex, straight off Kaggle. Seb banks $104,699 against Valmorlee's
    # $94,320, seated SECOND (`TeamNames` is ['Valmorlee', 'Seb (allegedly)']) -- the only tape here
    # where he is not seat 0, so anything reading seat 0 by hand gets the opponent.
    # `townCenterSellInterval = 24`: the REBALANCED economy, i.e. the game we actually play.
    # d0-d3 are identical to `seb` below; it diverges from d4, with 21 builds against 19, six of them
    # on d7, the third parcel on d6 rather than d8, and the crew dipping to 6 on d6.
    "seb2988": ("data/seed_scripts/top_guys/91422988.json",
                "data/seed_scripts/top_guys/91422988/schedule.json", "Seb (allegedly)"),
    # **`townCenterSellInterval = 12` -- the PRE-rebalance economy.** The town drains at half the rate
    # of the game we play, so prices move differently and his recorded bank is NOT reproducible here:
    # replaying both seats' own actions on seed 11 diverges at turn 32 (d1 h8) by one dollar on a
    # single BUY_PRODUCT and ends at $10,264 against his recorded $110,820.
    # It is still a valid target for the SCHEDULE and for the op sequence, which is what we generate.
    # It is not a target for money, fills, or any state row.
    # See `docs/the_tape_column_does_not_replay_his_game_2026-08-09.md`.
    "seb": ("data/seed_scripts/top_guys/90494364.json",
            "data/seed_scripts/top_guys/90494364/schedule.json", "Seb (allegedly)"),
    "oldleader": ("data/seed_scripts/new_leader/90016067.json",
                  "data/seed_scripts/new_leader/schedule.json", "somewhere after"),
    # **The rebase target, 2026-08-11.** Victor @ Tufa Labs is #2 on the ladder at 3,149.8 and is a
    # fixed script -- 97-99% of turns identical across seven games on both seats, with byte-identical
    # season SELL totals -- so the plan reads off one tape without averaging. This is his best of the
    # ten downloaded, $119,407 against Efe Can Celiksoy's $108,925, seated SECOND.
    # `townCenterSellInterval = 24`, i.e. the economy we actually play, unlike `seb`/`seb2`.
    # Why not Seb: his tape is the interval-12 shape (WHEAT 24 / STRAWBERRY 41), his own bank halved
    # when the economy changed and he withdrew. See `docs/the_ladder_is_two_scripts.md`.
    "victor": ("data/seed_scripts/top2/91854176.json",
               "data/seed_scripts/victor/schedule.json", "Victor @ Tufa Labs"),
    # **The current #1, and the highest bank in anything downloaded.** カワシギ takes $149,998 off
    # Yusuke Hayashi's $143,436 -- against Victor's best of $119,407 -- seated FIRST, which is the
    # opposite of `victor` and `seb2988` and worth checking before reading any seat by hand.
    # `townCenterSellInterval = 24`, i.e. the economy actually being played, same as `victor`.
    # The middle element drives OUR agent, never the tape column: `main()` feeds it to
    # `schedule_agent.make_agent` while the tape column comes from `tape_policy(replay, team, 0)`.
    # Nothing has been extracted from his games yet, so it reuses Victor's plan and the comparison
    # is "our Victor-derived plan against Kawashigi's recorded season". Pinned by
    # `tests/test_the_grid_compares_against_the_leader_we_rebased_on.py`.
    "kawashigi": ("data/seed_scripts/kawashigi/92498144.json",
                  "data/seed_scripts/victor/schedule.json", "\u30ab\u30ef\u30b7\u30ae"),
}

#: **The tape the grid compares against unless told otherwise, and it is not a preference.**
#: This defaulted to `seb` from the day `--tape` was added on 2026-08-07. The project rebased onto
#: Victor on 2026-08-11 and has worked against Victor since, so every run without an explicit
#: `--tape victor` was comparing against the wrong leader for two days. The two disagree in kind,
#: not in degree: the `animals` row totals -4 over six days against Seb, oscillating, which reads
#: as timing jitter -- and -14 over fourteen days against Victor, one-directional, which is a
#: defect. It was invisible the whole time.
#:
#: The deeper reason is the economy. `env_config` takes `townCenterSellInterval` off the recording
#: so both columns run the same one, and Seb's tape records **12** -- the PRE-rebalance economy,
#: retired on 2026-08-08. Defaulting to it replays every comparison at a town that drains at half
#: the rate of the game being played. Victor's and Kawashigi's record 24.
DEFAULT_TAPE = "victor"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
CROPS = ("WHEAT", "STRAWBERRY", "MELON", "TOMATO", "CARROT")
ANIMALS = ("COW", "SHEEP", "CHICKEN", "GOOSE", "PIG")
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
#: The env's unit vocabulary, read off `reference/kaggriculture.py` rather than remembered: four
#: `FARMER_MOVES` plus fourteen work ops. This tuple listed `"BUILD"`, which matches nothing -- the
#: real ops are `BUILD_COOP` and `BUILD_PASTURE` -- so every build was falling into the catch-all and
#: being reported as a MOVE. Anything still unrecognised now lands in `OTHER`, loudly, instead of
#: inflating the one row the routing argument rests on.
MOVES = ("NORTH", "SOUTH", "EAST", "WEST")
WORK = ("PLANT", "WATER", "HARVEST", "FERTILIZE", "FEED", "CARE", "COLLECT_FERTILIZER",
        "DIG", "BUILD_COOP", "BUILD_PASTURE", "PLACE", "PICKUP", "DROP")
OPS = WORK + ("PASS",) + MOVES

#: The turn-budget block, and the reason it is a module constant rather than a list built inside
#: `main()` behind an `if args.moves`. `work + move + idle == unit-turns` is an identity, and a
#: block that prints three of its four terms is a table a reader cannot add up -- which is exactly
#: the complaint this file was reworked to answer. `--moves` hides the four COMPASS rows, which are
#: tour shape and not a defect; it must never again hide a term of this sum.
BUDGET_ROWS = (("_turns", "unit-turns"), ("_work", "work"), ("_move", "move"), ("_pass", "idle"))


#: Configuration keys a recording carries that CHANGE THE GAME, and so must be taken from the
#: recording rather than from whatever version of the env happens to be installed. `seed` and
#: `weedSpawnChance` are deliberately NOT here: the recordings carry `seed: None`, and an unpinned
#: seed makes every number downstream noise (see `project_kaggriculture_fix_the_seed`).
ECONOMY_KEYS = ("townCenterSellInterval",)


def env_config(replay):
    """The economy the tape was PLAYED on, read off the recording.

    Without this the grid replays a tape on whatever economy is installed today. On 2026-08-08 the
    env went to 1.32.6 and `townCenterSellInterval` moved 12 -> 24, so `seb` (recorded at 12) was
    being replayed at 24: his sells filled differently, his d4 parcel was refused for want of $35,
    and the tape column reported him on 25 tiles, 8 pens and 6 melon at d6 where his own file
    records 50, 9 and 13. Three false leads came off those cells in a single session.

    Pinned by `tests/test_the_tape_column_reproduces_the_tape.py`, which replays each tape and
    requires it to land on the board it recorded.
    """
    cfg = json.loads(pathlib.Path(replay).read_text()).get("configuration") or {}
    return {k: cfg[k] for k in ECONOMY_KEYS if cfg.get(k) is not None}


def tape_policy(replay, team, seat_wanted):
    d = json.loads(pathlib.Path(replay).read_text())
    seat = d["info"]["TeamNames"].index(team)
    src = seat if seat_wanted == 0 else 1 - seat
    acts = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[src] or {} for step in d["steps"][1:])]
    idle = {"farmer": ["PASS"], "hands": [], "market": []}
    return lambda obs, t: acts[t] if t < len(acts) else idle


def snap(obs, seat):
    farm = obs["farms"][seat]
    n = collections.Counter()
    for r in farm["tiles"]:
        for t in r:
            if t == "LOCKED":
                continue
            n["owned"] += 1
            if not isinstance(t, dict):
                continue
            k = t.get("kind")
            if k == "PLANT":
                n["crop_" + str(t.get("crop"))] += 1
            elif k == "WEED":
                n["weed"] += 1
            else:
                n["pen"] += 1
            if t.get("animal"):
                n["an_" + str(t["animal"])] += 1
                # **The herd, not the species mix.** COW and SHEEP are interchangeable head-count
                # here and the two sides drift by one in opposite directions -- `cow 10/9` beside
                # `sheep 4/5` reads as two faults where the herd is identical at 14/14. Two false
                # signals from one true equality. `--species` splits them again.
                n["animals"] += 1
    shed = (obs.get("private") or {}).get("shed") or {}
    for p in PRODUCTS:
        n["shed_" + p] = int(shed.get(p, 0) or 0)
    n["money"] = int(farm["money"])
    n["hands"] = len(farm.get("hands") or [])
    return n


#: Market ops that settle straight against `private["shed"]` inside `_commit_unit` -- confirmed by
#: reading `reference/kaggriculture.py` rather than assumed. SELL takes from shed, BUY_PRODUCT and
#: BUY_ANIMAL add to shed; BUY_SEED touches `private["seeds"]` instead (handled separately, below).
SHED_MARKET_OPS = ("SELL", "BUY_PRODUCT", "BUY_ANIMAL")
#: Unit-phase ops that ALSO move product across the shed boundary, so a shed delta on a turn where
#: one of these fired cannot be attributed to a market order with confidence:
#:   DROP    -- dumps the WHOLE inventory of the acting unit into the shed; which items and how much
#:              is not visible from the action alone, so it taints every item, not just one.
#:   PICKUP  -- moves a named item shed -> inventory; taints that one item.
#:   PLACE   -- normally places an animal onto a matching empty structure and never touches the shed,
#:              but falls back to a shed drop of the named item if the tile is not a valid structure
#:              (`_apply_unit_action`, the `PLACE` branch) -- which branch fired is not visible from
#:              the action either, so it taints that one item too.
#: HARVEST, FEED, COLLECT_FERTILIZER and CARE never touch `private["shed"]` directly -- they read or
#: write the acting unit's own inventory (`_farmer_inventory`) or tile state, and reach the shed only
#: via a later DROP. So, unlike the identity `total_after = total_before + produced - consumed +
#: bought - sold` this docstring originally assumed, production and consumption are NOT confounders
#: for a shed-only reading -- only DROP/PICKUP/PLACE are, because those are the only other ops that
#: touch the same field SELL/BUY_PRODUCT/BUY_ANIMAL commit against.


#: The four ops `_commit_unit` settles one unit at a time. Read from `fills`, never from the shed.
#: The six ops the market settles, all of them read from `fills`, none of them from the action
#: stream. `HIRE` and `BUY_LAND` joined the list once `kagg/analysis/fills.py` learned to wrap
#: `_do_hire` and `_do_buy_land`: both are refused silently when the bank is short, so an emitted
#: one is an offer exactly like a SELL, and they had been sitting in the same table as the fills
#: under a heading that called everything in it "emitted".
MARKET_FILL_OPS = ("SELL", "BUY_PRODUCT", "BUY_SEED", "BUY_ANIMAL", "HIRE", "BUY_LAND")


def run(make0, opp, seed, weeds, stop_day=None, economy=None):
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills
    # `economy` comes from the tape via `env_config`. BOTH sides of the comparison play on it --
    # ours and the tape's -- because a grid whose two columns ran different economies compares
    # nothing. Defaults to the installed env when a caller has no tape in hand.
    cfg = dict(economy or {}, seed=seed, weedSpawnChance=weeds)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    p0, p1 = make0(), opp()
    days, ops = [], collections.defaultdict(collections.Counter)
    #: day -> op -> dollars that op actually moved. The units row says what happened; this says
    #: what it cost, and the two together are what closes the day's cash against its money row.
    cash = collections.defaultdict(collections.Counter)
    filled = {op: 0 for op in MARKET_FILL_OPS}
    spent = {op: 0.0 for op in MARKET_FILL_OPS}
    # Entered/exited by hand rather than with a `with`, purely so the loop body below keeps its
    # indentation and this change stays a readable diff.
    _cm = record_fills(env)
    fills = _cm.__enter__()
    # `stop_day` plays only days 0..stop_day-1. The d0-d6 gate is a unit test and must
    # not pay for 30 days of season to answer a question about 7.
    last = 719 if stop_day is None else min(719, 24 * stop_day)
    for t in range(last):
        o0, o1 = env.state[0].observation, env.state[1].observation
        if t % 24 == 0:
            days.append(snap(o0, 0))
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        # **Count what the env EXECUTES, not what the policy emitted.** `env.step` truncates to the
        # hands actually owned, and a replayed tape can emit more hand slots than it has units --
        # the reference ignores the surplus for movement and work. Counting the untruncated list
        # credited the tape with turns it never took, which is the one number the routing argument
        # divides by. Same list the step below sends, or the comparison is against a fiction.
        drop_any = False
        taint_items = set()
        for a in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
            if a:
                op = a[0]
                ops[t // 24][op if op in OPS else "OTHER"] += 1
                # Turn budget. Every unit that acted spent a turn, and it went to exactly one of three
                # places: walking, working, or nothing. This is the denominator the routing question
                # actually needs -- a raw MOVE count says nothing without the work it bought.
                ops[t // 24]["_turns"] += 1
                ops[t // 24]["_move" if op in MOVES else
                             "_pass" if op == "PASS" else "_work"] += 1
                if op == "DROP":
                    drop_any = True
                elif op in ("PICKUP", "PLACE") and len(a) > 1:
                    taint_items.add(a[1])
        # **The four market ops are read from `_commit_unit`, not inferred.** They used to be
        # reconstructed from the shed level across the step, counted only on turns "clean" of
        # DROP/PICKUP/PLACE for that item -- because a hand putting wheat in the shed and a wheat
        # purchase are the same delta. That made the row a LOWER BOUND whose tightness depended on
        # how much the agent moved goods around, and our agent moves far more than a tape does:
        # coverage ran 27%/32% for us against 23%/68% for the tape, so the instrument understated
        # US specifically and every comparison drawn from it was biased against our own agent.
        # `kagg/analysis/fills.py` wraps the one function that moves shed and money together, per
        # unit, and its docstring already lists three earlier versions of this same mistake.
        for o in (a0["market"] or []):
            if o and o[0] not in MARKET_FILL_OPS:
                ops[t // 24][o[0]] += int(o[2]) if len(o) > 2 else 1
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        for op in MARKET_FILL_OPS:
            now = fills.units(0, op)
            ops[t // 24][op] += now - filled[op]
            filled[op] = now
            value = fills.spent(0, op)
            cash[t // 24][op] += value - spent[op]
            spent[op] = value
        if env.state[0].status == "DONE":
            break
    # Only a run that was meant to reach the end must be DONE. A `stop_day` run is cut deliberately.
    if stop_day is None:
        bad = [(s, env.state[s].status) for s in (0, 1) if env.state[s].status != "DONE"]
        if bad:
            raise RuntimeError(f"seat status {bad}")
    days.append(snap(env.state[0].observation, 0))
    # **Day N is the state at the END of day N, not its dawn.** `days` is collected at each dawn plus
    # one final snapshot, so `days[N + 1]` is the board after day N's actions -- which is what lines
    # up with the op counts, which are that day's actions. Reading a dawn snapshot beside the same
    # column's ops means reading YESTERDAY'S outcome next to TODAY'S work, and it caused a real
    # misreading: `money` at d12 is the result of d11, so the d10 land purchase showed up a column
    # late and a step change got attributed to the wrong day twice.
    _cm.__exit__(None, None, None)
    # A fill whose farm could not be resolved to a seat is dropped rather than guessed, so a nonzero
    # count here means the seat map is broken and every market row is understated. It must be zero.
    if fills.unattributed:
        raise RuntimeError(f"{fills.unattributed} fills could not be attributed to a seat")
    return days[1:], ops, dict(cash), days[0]


#: Board rows the CSV carries. Fixed and full, unlike the terminal grid's `live` filter: a column
#: of zeros is information in a spreadsheet (it sorts, it charts, it subtracts) and a column that
#: appears and disappears between runs cannot be pasted beside another run's.
CSV_BOARD = (("money", "money"), ("hands", "hands"), ("owned", "tiles"), ("pen", "pens"),
             ("weed", "weeds"), ("animals", "animals"))


def write_csv(path, ours, tape, days):
    """The whole grid as one spreadsheet: **a row per day, a column per field**.

    Alex, on the terminal version: "can you do it so it is not interweaved or is as a csv i can
    open in excel". The terminal grid is transposed -- days across, fields down -- because that is
    what fits in eighty columns, and that transposition is exactly what makes it unreadable. A
    spreadsheet wants the opposite: a day is an observation and a field is a variable, so days go
    down and fields go across, and then sorting, charting and filtering all work.

    **One file with a column triplet per field**, `<field>.ours`, `<field>.tape`, `<field>.diff`,
    rather than three files. Three files means three sheets and a VLOOKUP before you can see a gap;
    the triplet puts ours, the tape and the difference side by side in the one place a reader is
    already looking, and `.diff` is `ours - tape` so its sign reads the same way as the terminal
    `--diff` block.

    **Every column header says what KIND of number the cell holds**, because a spreadsheet strips
    away the surrounding prose that a terminal table can carry above it:

        board.*    a count or level of real board state at the END of that day
        offered.*  unit ops EMITTED that day -- the env silently ignores an illegal one
        fill.*     UNITS that committed, from `_commit_unit` / `_do_hire` / `_do_buy_land`
        cash.*     DOLLARS that actually moved, at the price each unit fetched
        budget.*   the turn budget; work + move + idle == unit-turns

    No market op appears under `offered.` -- all six the market settles are fills.
    """
    import csv

    our_days, our_ops, our_cash, our_dawn = ours
    his_days, his_ops, his_cash, his_dawn = tape

    columns = []                                   # (header base, ours-getter, tape-getter)
    for key, label in CSV_BOARD:
        columns.append((f"board.{label}",
                        lambda d, k=key: our_days[d][k], lambda d, k=key: his_days[d][k]))
    for crop in CROPS:
        columns.append((f"board.crop_{crop.lower()}",
                        lambda d, c=crop: our_days[d]["crop_" + c],
                        lambda d, c=crop: his_days[d]["crop_" + c]))
    for animal in ANIMALS:
        columns.append((f"board.herd_{animal.lower()}",
                        lambda d, a=animal: our_days[d]["an_" + a],
                        lambda d, a=animal: his_days[d]["an_" + a]))
    for product in PRODUCTS:
        columns.append((f"board.shed_{product.lower()}",
                        lambda d, p=product: our_days[d]["shed_" + p],
                        lambda d, p=product: his_days[d]["shed_" + p]))
    for op in OPS + ("OTHER",):
        columns.append((f"offered.{op.lower()}",
                        lambda d, o=op: our_ops[d][o], lambda d, o=op: his_ops[d][o]))
    for op in MARKET_FILL_OPS:
        columns.append((f"fill.{op.lower()}",
                        lambda d, o=op: our_ops[d][o], lambda d, o=op: his_ops[d][o]))
    for op, label in (("SELL", "sold"), ("BUY_PRODUCT", "product"), ("BUY_SEED", "seed"),
                      ("BUY_ANIMAL", "animal"), ("HIRE", "hire"), ("BUY_LAND", "land")):
        columns.append((f"cash.{label}",
                        lambda d, o=op: round(our_cash.get(d, {}).get(o, 0)),
                        lambda d, o=op: round(his_cash.get(d, {}).get(o, 0))))
    columns.append(("cash.open",
                    lambda d: our_dawn["money"] if d == 0 else our_days[d - 1]["money"],
                    lambda d: his_dawn["money"] if d == 0 else his_days[d - 1]["money"]))
    columns.append(("cash.close", lambda d: our_days[d]["money"], lambda d: his_days[d]["money"]))
    for key, label in BUDGET_ROWS:
        columns.append((f"budget.{label.replace('-', '_')}",
                        lambda d, k=key: our_ops[d][k], lambda d, k=key: his_ops[d][k]))

    header = ["day"]
    for base, _o, _t in columns:
        header += [f"{base}.ours", f"{base}.tape", f"{base}.diff"]
    with open(path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        for day in range(days):
            row = [day]
            for _base, get_ours, get_tape in columns:
                a, b = get_ours(day), get_tape(day)
                row += [a, b, a - b]
            writer.writerow(row)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default=DEFAULT_TAPE, choices=sorted(TAPES),
                    help="which recorded season the tape column replays. Defaults to "
                         "%(default)s, the leader the project rebased onto -- `seb` is on the "
                         "pre-rebalance townCenterSellInterval 12 economy and comparing against "
                         "him replays the whole grid at a town nobody plays any more.")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--days", type=int, default=11)
    # **Movement and shed levels are OFF by default, and that is deliberate.**
    # The compass rows record which way a hand walked, which is a tour-shape difference and not a
    # defect: we work the board westward and the tape works it southward. They filled a third of the
    # table with rows nobody can act on.
    # The `sh:*` rows are worse than useless. They sample the shed ONCE per day, so they are a
    # snapshot of a flow -- the same error `docs/the_book_is_shallow_2026-08-09.md` records twice
    # (dusk sampling, and a raw count compared across different herd sizes) and that
    # `kagg/analysis/fills.py` exists to replace. A shed that reads 0 at dawn may have passed 40
    # units through that day. Read fills, never levels.
    ap.add_argument("--moves", action="store_true",
                    help="show the NORTH/SOUTH/EAST/WEST rows and the mv/wk ratio (tour shape, "
                         "not a defect -- off by default)")
    ap.add_argument("--species", action="store_true",
                    help="split the herd back into COW/SHEEP/... rows. Off by default: the species "
                         "mix drifts by one in opposite directions and reads as two faults where "
                         "the herd is identical.")
    ap.add_argument("--cum", action="store_true",
                    help="after the op table, print the same flow rows CUMULATIVELY. A day-by-day "
                         "count cannot show cadence: harvest read 11/14 on d18 and 46/46 cumulative "
                         "over d16-d18, because the tape picked on d18 what we picked on d17. Use "
                         "this before calling any flow cell a defect.")
    ap.add_argument("--shed", action="store_true",
                    help="show the sh:* dawn shed levels. They are a snapshot of a flow and lie; "
                         "use fills instead. Off by default.")
    ap.add_argument("--diff", action="store_true",
                    help="list EVERY field that differs, per day, instead of the wide tables")
    # **Hand the first N days to the tape, then take over.** The tape's actions replayed from turn 0
    # reproduce its board field for field -- the starting board is deterministic and, with weeds off,
    # the only unmatched RNG is the shop unlock order. `--handover 11` therefore means HE plays days
    # 0 to 10 INCLUSIVE, including the day-10 parcel, and our agent opens day 11 on his board.
    #
    # This is what separates "our opening is behind" from "our selling is behind". Without it every
    # late-season deficit can be blamed upstream, and usually was. See `scripts/handover.py`, which
    # reports the same run as eight scalars plus the shed-discard count.
    ap.add_argument("--handover", type=int, default=None, metavar="DAY",
                    help="tape plays days 0..DAY-1, our agent plays DAY onwards")
    ap.add_argument("--csv", metavar="PATH",
                    help="also write the whole grid to a spreadsheet: a ROW PER DAY, a column per "
                         "field, with an ours/tape/diff triplet for each. Every header is prefixed "
                         "board./offered./fill./cash./budget. so a cell's kind travels with it. "
                         "The terminal output is unchanged.")
    ap.add_argument("--module", default="schedule_agent",
                    help="which agent to compare against the tape, e.g. schedule_agent_1455mh")
    args = ap.parse_args()

    global schedule_agent
    schedule_agent = importlib.import_module("kagg.search." + args.module)

    replay, schedule, team = TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    opp = lambda: tape_policy(replay, team, 1)

    # **Play only as far as we print.** `--days 7` used to simulate two full 30-day seasons to
    # show seven, which is a 4x cost on the loop being iterated hardest. `run` needs one day
    # beyond the last printed column, because column d is the board at the END of day d.
    horizon = args.days + 1 if args.handover is None else None
    economy = env_config(replay)
    his, his_ops, his_cash, his_dawn = run(lambda: tape_policy(replay, team, 0), opp, args.seed,
                                           args.weeds, stop_day=horizon, economy=economy)

    def mine():
        # `start_day` only exists on HEAD's agent, and only --handover needs it. Passing it
        # unconditionally made every older base (1455*) die on import of the comparison itself.
        kw = {} if args.handover is None else {"start_day": args.handover}
        a = schedule_agent.make_agent(thin, 0, router=True, **kw)
        if args.handover is None:
            return lambda o, t: a(o)
        tape = tape_policy(replay, team, 0)

        def f(o, t):
            if t // 24 < args.handover:
                a(o)                  # drive our agent anyway so its per-day state is warm
                return tape(o, t)
            return a(o)
        return f

    ours, our_ops, our_cash, our_dawn = run(mine, opp, args.seed, args.weeds, stop_day=horizon,
                                            economy=economy)

    if args.csv:
        # Before the terminal blocks, and before `--diff`'s early return: a flag that silently does
        # nothing in combination with another flag is the kind of thing this pass exists to stop.
        write_csv(args.csv, (ours, our_ops, our_cash, our_dawn),
                  (his, his_ops, his_cash, his_dawn), args.days)
        print(f"  wrote {args.days} day-rows to {args.csv}")

    fields = ([("money", "money"), ("hands", "hands"), ("owned", "tiles"), ("pen", "pens"),
               ("weed", "weeds")]
              + [("crop_" + c, c.lower()[:6]) for c in CROPS]
              + ([("an_" + x, x.lower()[:6]) for x in ANIMALS] if args.species
                 else [("animals", "animals")])
              + ([("shed_" + p, "sh:" + p.lower()[:5]) for p in PRODUCTS] if args.shed else []))
    live = [(k, lab) for k, lab in fields
            if any(d[k] for d in ours[:args.days + 1]) or any(d[k] for d in his[:args.days + 1])]

    print(f"tape {args.tape}   seed {args.seed}   weeds {args.weeds}   "
          + "".join(f"{k} {v}   " for k, v in economy.items())
          + f"CUMULATIVE_SELLS={schedule_agent.CUMULATIVE_SELLS} "
          f"SELL_CARRY_DAYS={schedule_agent.SELL_CARRY_DAYS} "
          f"HIRE_FIRST={schedule_agent.HIRE_FIRST}")
    print("  state rows are the board at the END of that day; flow rows are that day's actions.")
    print("  the four blocks below are: a board COUNT, unit ops OFFERED, market FILLS, and a "
          "turn budget that sums to unit-turns. Every cell is ours/tape of the SAME quantity.")
    print("  the compass rows are HIDDEN -- --moves brings them back; dawn shed levels too, but a "
          "shed level is one sample of a flow and lies about it. Read the fills.")


    if args.diff:
        # Every field that is not identical, per day. The wide tables above are for reading what
        # happened; this is for answering "is it exact yet", where a single unrecorded row is the
        # whole answer and eyeballing a 20x11 grid is how a mismatch gets called a match.
        ops_all = sorted(set(OPS) | {"OTHER"} | set(MARKET_FILL_OPS))
        budget = BUDGET_ROWS
        compass = {"NORTH", "SOUTH", "EAST", "WEST"}
        rows = ([("state", lab, [(ours[d][k], his[d][k]) for d in range(args.days)])
                 for k, lab in fields]
                + [("op", o.lower(), [(our_ops[d][o], his_ops[d][o]) for d in range(args.days)])
                   for o in ops_all if args.moves or o not in compass]
                # Derived: `idle` IS the `pass` op, `move` is the four directions summed, `work` the
                # work ops summed, `unit-turns` all three. Kept because they are the readable summary,
                # flagged because counting them alongside their own parts double-counts the total.
                + [("=sum", lab, [(our_ops[d][k], his_ops[d][k]) for d in range(args.days)])
                   for k, lab in budget])

        live = [(k, lab, c) for k, lab, c in rows if any(o != h for o, h in c)]
        live.sort(key=lambda r: (r[0] == "=sum", -abs(sum(o - h for o, h in r[2]))))
        indep = sum(sum(1 for o, h in c if o != h) for k, lab, c in live if k != "=sum")
        derived = sum(sum(1 for o, h in c if o != h) for k, lab, c in live if k == "=sum")

        print(f"\n  ours MINUS tape, days 0-{args.days - 1}.  blank = identical.\n")
        head = "".join(f"{('d' + str(d)):>7}" for d in range(args.days))
        print(f"  {'field':<20}{head}{'days':>6}{'total':>8}")
        print(f"  {'-' * (20 + 7 * args.days + 14)}")
        for kind, lab, cells in live:
            if kind == "=sum":
                print(f"  {'-' * (20 + 7 * args.days + 14)}")
            body = "".join(f"{'' if o == h else f'{o - h:+d}':>7}" for o, h in cells)
            n = sum(1 for o, h in cells if o != h)
            print(f"  {lab:<20}{body}{n:>6}{sum(o - h for o, h in cells):>+8}")
        print(f"\n  {indep} independent differing cells; the {derived} below the rule are derived "
              f"(idle IS pass, move is n/s/e/w summed, work the work ops, unit-turns all three).")

        # **Exact means zero. There is no "essentially exact".** This verdict exists because the
        # summary written above a table is where a 67-cell gap got called "near-exact" -- twice. A day
        # counts only if EVERY independent field matches, and the headline is the count, not an
        # adjective. If a number has to be described rather than shown, it is not a match.
        per_day = [sum(1 for k, lab, c in live if k != "=sum" and c[d][0] != c[d][1])
                   for d in range(args.days)]
        exact = [d for d, n in enumerate(per_day) if n == 0]
        print("\n  per-day differing cells: "
              + "  ".join(f"d{d}={n}" for d, n in enumerate(per_day)))
        # The denominator matters as much as the count: "67 cells differ" reads very differently
        # against 210 tracked cells than against 80. Fields that are zero on both sides all season
        # are not evidence of agreement, so they are excluded from the base.
        base = [(k, lab, c) for k, lab, c in rows
                if k != "=sum" and any(o or h for o, h in c)]
        cells = len(base) * args.days
        rowsdiff = sum(1 for k, lab, c in base if any(o != h for o, h in c))
        print(f"  VERDICT: {'EXACT' if indep == 0 else 'NOT EXACT'} -- "
              f"{len(exact)}/{args.days} days exact, "
              f"{rowsdiff}/{len(base)} tracked fields differ somewhere, "
              f"{indep}/{cells} cells differ.")
        return
    # END of the day, not dawn: `run` returns `days[1:]`, so column d is the board AFTER day d's ops,
    # which is the only alignment under which a state row and an op row describe the same day. The
    # heading said DAWN for both and it was simply wrong.
    print("\n  board and herd at END of day -- ours/tape\n")
    print(f"  {'':<12}" + "".join(f"{('d' + str(d)):>13}" for d in range(args.days)))
    for k, lab in live:
        cells = "".join(f"{str(ours[d][k]) + '/' + str(his[d][k]):>13}" for d in range(args.days)
                        if d < len(ours) and d < len(his))
        print(f"  {lab:<12}{cells}")

    print("\n  unit ops OFFERED that day, one per unit that acted -- ours/tape\n")
    print(f"  {'':<12}" + "".join(f"{('d' + str(d)):>13}" for d in range(args.days)))
    compass = {"NORTH", "SOUTH", "EAST", "WEST"}
    def live_ops(names):
        return [o for o in names if (args.moves or o not in compass)
                and any(our_ops[d][o] or his_ops[d][o] for d in range(args.days))]

    def op_rows(names):
        for o in names:
            cells = "".join(f"{str(our_ops[d][o]) + '/' + str(his_ops[d][o]):>13}"
                            for d in range(args.days))
            print(f"  {o.lower()[:12]:<12}{cells}")

    unit_ops = live_ops(OPS + ("OTHER",))
    fill_ops = live_ops(MARKET_FILL_OPS)
    op_rows(unit_ops)

    # **The market block is separated because it is a different KIND of number.** A unit op row is
    # what the unit was told to do; the env silently ignores an illegal one, so it is an offer. A
    # market row here is a unit that committed, read from `_commit_unit` (and `_do_hire` /
    # `_do_buy_land`) via `kagg/analysis/fills.py`. Both were printed in one table under the single
    # heading "ops emitted that day", which was true of half the rows.
    print("\n  market FILLS that day, UNITS that committed -- ours/tape\n")
    print(f"  {'':<12}" + "".join(f"{('d' + str(d)):>13}" for d in range(args.days)))
    op_rows(fill_ops)
    seen = unit_ops + fill_ops

    # **Cumulative, because a day-by-day flow count cannot show cadence.** Two sides doing identical
    # work on alternate days read as a fault on every single column. Day 18 harvest read `11/14` and
    # was nothing at all: the tape picked on d18 the strawberries we had picked on d17, and the
    # running total over d16-d18 is 46/46. That cell cost most of a session and three wrong
    # diagnoses. A flow row only means something once its running total stops reconciling -- for
    # harvest that is d24, where the gap goes -3 -> -17 and never comes back.
    if args.cum:
        print("\n  CUMULATIVE from d0 -- ours/tape. A gap that oscillates is cadence; "
              "a gap that grows is lost work.\n")
        print(f"  {'':<12}" + "".join(f"{('d' + str(d)):>13}" for d in range(args.days)))
        for o in seen:
            co = ct = 0
            cells = []
            for d in range(args.days):
                co += our_ops[d][o]
                ct += his_ops[d][o]
                cells.append(f"{str(co) + '/' + str(ct):>13}")
            print(f"  {o.lower()[:12]:<12}" + "".join(cells))

    # Where the day's unit-turns went. `move` on its own is not a verdict: walking to do more work is
    # not the same failure as walking further to do the same work. `mv/wk` separates them -- it is the
    # movement each side paid per unit of work done, so a higher number is strictly worse routing.
    # **`move` is always shown here, whatever `--moves` says.** `--moves` hides the four COMPASS
    # rows, which are tour shape and not a defect. Hiding `move` from the BUDGET is a different
    # thing: it leaves three rows that cannot be added up, and a table a reader cannot add up is
    # the complaint this pass exists to answer. work + move + idle == unit-turns, always, and the
    # line under the block says so out loud.
    print("\n  turn budget -- ours/tape.  work + move + idle == unit-turns\n")
    print(f"  {'':<12}" + "".join(f"{('d' + str(d)):>13}" for d in range(args.days)))
    for key, lab in BUDGET_ROWS:
        cells = "".join(f"{str(our_ops[d][key]) + '/' + str(his_ops[d][key]):>13}"
                        for d in range(args.days))
        print(f"  {lab:<12}{cells}")
    broken = [(d, side) for d in range(args.days) for side, c in (("ours", our_ops), ("tape", his_ops))
              if c[d]["_work"] + c[d]["_move"] + c[d]["_pass"] != c[d]["_turns"]]
    if broken:
        raise RuntimeError(f"turn budget does not sum on {broken}; the op vocabulary is incomplete")
    if args.moves:
        for lab, src in (("mv/wk", None),):
            cells = ""
            for d in range(args.days):
                o = our_ops[d]["_move"] / max(1, our_ops[d]["_work"])
                h = his_ops[d]["_move"] / max(1, his_ops[d]["_work"])
                cells += f"{f'{o:.2f}/{h:.2f}':>13}"
            print(f"  {lab:<12}{cells}")
    # **The one block that has to close to the dollar.** Every term is a fill with the price that
    # unit actually fetched, so `open + sold - bought - seed - animal - hire - land` IS the money
    # row, and a reader can add the column up and land on it. That is the whole point: until this
    # existed, the grid's numbers reconciled only if you knew which three caveats to apply to which
    # rows. If a row here does not tie, the instrument is wrong and says so rather than printing a
    # plausible number.
    print("\n  cash, ours/tape -- FILLS at the price each unit actually fetched. "
          "the column adds up.\n")
    print(f"  {'':<12}" + "".join(f"{('d' + str(d)):>13}" for d in range(args.days)))
    ledger = [("open", None), ("+ sold", "SELL"), ("- product", "BUY_PRODUCT"),
              ("- seed", "BUY_SEED"), ("- animal", "BUY_ANIMAL"), ("- hire", "HIRE"),
              ("- land", "BUY_LAND"), ("= close", None)]
    opens = ([our_dawn["money"]] + [ours[d]["money"] for d in range(args.days)],
             [his_dawn["money"]] + [his[d]["money"] for d in range(args.days)])
    mismatch = []
    for lab, op in ledger:
        cells = []
        for d in range(args.days):
            if lab == "open":
                pair = (opens[0][d], opens[1][d])
            elif lab == "= close":
                pair = (ours[d]["money"], his[d]["money"])
            else:
                pair = (round(our_cash.get(d, {}).get(op, 0)),
                        round(his_cash.get(d, {}).get(op, 0)))
            cells.append(f"{str(pair[0]) + '/' + str(pair[1]):>13}")
        print(f"  {lab:<12}" + "".join(cells))
    for d in range(args.days):
        for side, cash, col in (("ours", our_cash, ours), ("tape", his_cash, his)):
            flow = (cash.get(d, {}).get("SELL", 0)
                    - sum(cash.get(d, {}).get(o, 0) for o in MARKET_FILL_OPS if o != "SELL"))
            opened = (our_dawn if side == "ours" else his_dawn)["money"] if d == 0 \
                else (ours if side == "ours" else his)[d - 1]["money"]
            if round(opened + flow) != col[d]["money"]:
                mismatch.append((side, d, round(opened + flow), col[d]["money"]))
    if mismatch:
        raise RuntimeError(
            "the cash ledger does not close: %s. Every dollar a farm gains or loses passes through "
            "_commit_unit, _do_hire or _do_buy_land, so a gap here means a path is unwrapped."
            % mismatch)
    print("  every column closes: open + sold - the five costs == close, to the dollar.")

    tot = lambda c: (sum(c[d]["_move"] for d in range(args.days)),
                     sum(c[d]["_work"] for d in range(args.days)),
                     sum(c[d]["_pass"] for d in range(args.days)))
    om, ow, op_ = tot(our_ops)
    hm, hw, hp = tot(his_ops)
    print(f"\n  days 0-{args.days - 1} totals   work {ow}/{hw}   move {om}/{hm}   idle {op_}/{hp}"
          f"   mv/wk {om / max(1, ow):.2f}/{hm / max(1, hw):.2f}")


if __name__ == "__main__":
    main()