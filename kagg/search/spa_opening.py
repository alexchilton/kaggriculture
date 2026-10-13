"""SpaTaro's opening geometry, executed reactively for days 0-6.

His turns cannot be copied: 62 seasons give 37 distinct openings reaching 37 distinct
states, sharing almost no turns. What IS invariant is the board he arrives at -- ten
tiles identical in 62/62 seasons (docs/spataro_architecture_2026-09-11.md §2). So this
names the tiles and the ops, and walks units to them, reading the board every turn.

Positions are (x, y), matching obs["farms"][me]["farmer"]. The geometry table in the doc
is keyed (y, x); it is transposed here once, deliberately, rather than at every use.

Board 10x10, NW unlocked is x<5 and y<5, shed access is the four inner corners of which
only (4,4) is in NW. Two of his cows sit on (4,4) and (3,4) -- on and beside the shed
access tile, so feeding them costs no walk. That is not incidental and is kept.

Ops are never emitted blind. PLANT needs an empty tile and a seed in private["seeds"];
BUILD_PASTURE needs an empty tile; PLACE needs the unit standing on a matching empty
structure with the animal in ITS OWN inventory, which means a PICKUP at (4,4) first.
"""

ANIMAL_TILES = [
    # (x, y), species, day it is wanted by
    ((3, 3), "SHEEP", 0),
    ((2, 4), "SHEEP", 0),
    ((3, 4), "COW", 0),
    ((4, 4), "COW", 0),
    ((1, 3), "COW", 3),
    ((4, 2), "COW", 4),
    ((1, 4), "COW", 5),
]
MELON_TILES = [(3, 1), (3, 2), (4, 3), (2, 1), (0, 4), (2, 0),
               (4, 1), (2, 3), (1, 2), (3, 0), (1, 1), (2, 2)]
WHEAT_TILES = [(0, 0), (1, 0), (0, 1), (0, 2), (0, 3), (4, 0), (3, 3)]

SHED_ACCESS = (4, 4)
TPD = 24


def _tile(tiles, x, y):
    return tiles[y][x]


def _step_toward(pos, target):
    px, py = pos
    tx, ty = target
    if px < tx:
        return ["EAST"]
    if px > tx:
        return ["WEST"]
    if py < ty:
        return ["SOUTH"]
    if py > ty:
        return ["NORTH"]
    return None


def plan_turn(obs, me):
    """Return (farmer_cmd, hand_cmds) for this turn of the opening."""
    farm = obs["farms"][me]
    tiles = farm["tiles"]
    day = int(obs["day"])
    private = obs["private"]
    units = [list(farm["farmer"])] + [list(h) for h in farm["hands"]]
    invs = private["inventories"]
    seeds = private["seeds"]
    shed = private["shed"]

    # Priority order is forced by two engine rules, both two-strike:
    # a plant unwatered two days running becomes a WEED (_daily_refresh_plants),
    # and an animal unfed two days running escapes (_daily_refresh_animals).
    # So keeping what exists alive outranks adding to it, always. A first pass that
    # planted sixteen tiles and watered none lost the entire field by day 1.
    thirsty, hungry, weeds = [], [], []
    for y in range(5):
        for x in range(5):
            t = tiles[y][x]
            if not isinstance(t, dict):
                continue
            if t.get("kind") == "PLANT" and not t.get("watered_today"):
                thirsty.append(((x, y), t.get("consecutive_unwatered", 0)))
            elif t.get("animal") and not t.get("fed_today"):
                hungry.append(((x, y), t.get("consecutive_unfed", 0)))
            elif t.get("kind") == "WEED":
                weeds.append((x, y))
    # Most-starved first: a tile on its second dry day dies tonight.
    thirsty = [t for t, _ in sorted(thirsty, key=lambda kv: -kv[1])]
    hungry = [t for t, _ in sorted(hungry, key=lambda kv: -kv[1])]

    herd_jobs, plant_jobs = [], []
    for (x, y), species, by in ANIMAL_TILES:
        if day < by:
            continue
        t = tiles[y][x]
        if isinstance(t, dict) and t.get("animal"):
            continue
        if t is None:
            herd_jobs.append(((x, y), "BUILD_PASTURE", None))
        elif isinstance(t, dict) and t.get("kind") == "WEED":
            herd_jobs.append(((x, y), "DIG", None))
        elif isinstance(t, dict) and t.get("kind") == "PASTURE":
            herd_jobs.append(((x, y), "PLACE", species))

    # Never hold more crop than the crew can water: one unit services at most a few
    # tiles a day once walking is paid for, and an unwatered tile is worse than an
    # empty one. Two tiles per hand is the cap until this is measured properly.
    alive = sum(1 for y in range(5) for x in range(5)
                if isinstance(tiles[y][x], dict) and tiles[y][x].get("kind") == "PLANT")
    room = max(0, 3 * max(1, len(units)) - alive)
    for (x, y) in MELON_TILES[:min(len(MELON_TILES), 8 + day)]:
        if room <= 0 or seeds.get("MELON", 0) <= 0:
            break
        t = tiles[y][x]
        if t is None:
            plant_jobs.append(((x, y), "PLANT", "MELON")); room -= 1
        elif isinstance(t, dict) and t.get("kind") == "WEED":
            plant_jobs.append(((x, y), "DIG", None))
    for (x, y) in WHEAT_TILES:
        if room <= 0 or seeds.get("WHEAT", 0) <= 0:
            break
        if tiles[y][x] is None:
            plant_jobs.append(((x, y), "PLANT", "WHEAT")); room -= 1

    cmds = [["PASS"] for _ in units]
    taken = set()
    for i, pos in enumerate(units):
        inv = invs[i] if i < len(invs) else {}

        # 1. A unit already carrying an animal delivers it before anything else.
        held = next((s for s in ("COW", "SHEEP") if inv.get(s, 0) > 0), None)
        if held:
            tgt = next((t for (t, sp, _) in ANIMAL_TILES
                        if sp == held and t not in taken
                        and isinstance(tiles[t[1]][t[0]], dict)
                        and tiles[t[1]][t[0]].get("kind") == "PASTURE"
                        and not tiles[t[1]][t[0]].get("animal")), None)
            if tgt:
                taken.add(tgt)
                cmds[i] = _step_toward(pos, tgt) or ["PLACE", held]
                continue

        # 2. Feed, then water. Both are two-strike deaths.
        if hungry and inv.get("WHEAT", 0) > 0:
            tgt = next((t for t in hungry if t not in taken), None)
            if tgt:
                taken.add(tgt)
                cmds[i] = _step_toward(pos, tgt) or ["FEED"]
                continue
        if hungry and shed.get("WHEAT", 0) > 0 and inv.get("WHEAT", 0) == 0:
            cmds[i] = _step_toward(pos, SHED_ACCESS) or ["PICKUP", "WHEAT", 4]
            continue
        tgt = next((t for t in thirsty if t not in taken), None)
        if tgt:
            taken.add(tgt)
            cmds[i] = _step_toward(pos, tgt) or ["WATER"]
            continue

        # 2b. A seed in hand outranks fertilizer. A melon planted on day 0 yields from
        # day 10; fertilizer collected on day 0 is worth ~$85 once. A first pass put
        # fertilizer first and left 2 of 8 melon seeds unplanted with money at $14 --
        # action-starved, not cash-starved.
        if seeds.get("MELON", 0) > 0 or seeds.get("WHEAT", 0) > 0:
            job = next((j for j in plant_jobs if j[0] not in taken
                        and (j[1] != "PLANT" or seeds.get(j[2], 0) > 0)), None)
            if job:
                (x, y), op, arg = job
                taken.add((x, y))
                cmds[i] = _step_toward(pos, (x, y)) or ([op] if arg is None else [op, arg])
                continue

        # 3. Fertilizer: one action, no input, ~$85 of value, and the only revenue
        # before milk lands on day 8 (docs/history/the_field.md). It funds the herd.
        fert = [(x, y) for y in range(5) for x in range(5)
                if isinstance(tiles[y][x], dict) and tiles[y][x].get("fertilizer_available")
                and (x, y) not in taken]
        if fert:
            tgt = min(fert, key=lambda t: abs(t[0]-pos[0]) + abs(t[1]-pos[1]))
            taken.add(tgt)
            cmds[i] = _step_toward(pos, tgt) or ["COLLECT_FERTILIZER"]
            continue

        # 4. Only now build the herd and the field out.
        job = next((j for j in herd_jobs + plant_jobs if j[0] not in taken), None)
        if job:
            (x, y), op, arg = job
            if op == "PLACE":
                if shed.get(arg, 0) > 0:
                    taken.add((x, y))
                    cmds[i] = _step_toward(pos, SHED_ACCESS) or ["PICKUP", arg, 1]
                    continue
            else:
                taken.add((x, y))
                cmds[i] = _step_toward(pos, (x, y)) or ([op] if arg is None else [op, arg])
                continue

        # 5. Spare hands clear weeds so tiles come back.
        if weeds:
            tgt = next((t for t in weeds if t not in taken), None)
            if tgt:
                taken.add(tgt)
                cmds[i] = _step_toward(pos, tgt) or ["DIG"]
                continue
    return cmds[0], cmds[1:]


def market_turn(obs, me):
    """Day-0 crew, herd and seed, then wheat in small lots as cash allows."""
    farm = obs["farms"][me]
    day, hour = int(obs["day"]), int(obs["hour"])
    money = farm["money"]
    orders = []
    if day == 0 and hour == 0:
        for _ in range(6):
            orders.append(["HIRE"])
        orders.append(["BUY_ANIMAL", "COW", 2])
        orders.append(["BUY_ANIMAL", "SHEEP", 2])
        orders.append(["BUY_SEED", "MELON", 8])
        orders.append(["BUY_SEED", "WHEAT", 6])
        return orders[:10]
    if day <= 6:
        shed = obs["private"]["shed"]
        # Sell first: the market resolves orders in list order, so proceeds from these
        # are available to the purchases below in the same turn (field actions are not).
        for p in ("FERTILIZER", "MILK", "WOOL", "EGG"):
            q = shed.get(p, 0)
            if q > 0:
                orders.append(["SELL", p, q])
        target = 6 if day == 0 else 8
        if len(farm["hands"]) < target and int(farm.get("hires_today", 0) or 0) == 0:
            orders.append(["HIRE"])
        # The herd additions SpaTaro makes on d3, d4 and d5, bought only when the
        # money is actually there rather than scheduled blind.
        wanted = sum(1 for (_, _, by) in ANIMAL_TILES if by <= day)
        have = sum(1 for (x, y), _, _ in ANIMAL_TILES
                   if isinstance(farm["tiles"][y][x], dict) and farm["tiles"][y][x].get("animal"))
        # Feed supply gates the herd. Each animal eats one WHEAT a day and an animal
        # unfed twice escapes, so buying a cow the crew cannot feed loses BOTH animals.
        # A first pass reserved cash for cows instead of wheat and the whole herd left.
        ration = shed.get("WHEAT", 0) + sum(i.get("WHEAT", 0) for i in obs["private"]["inventories"])
        if wanted > have + shed.get("COW", 0) + shed.get("SHEEP", 0) and ration >= 2 * (have + 1):
            species = next((sp for (x, y), sp, by in ANIMAL_TILES if by <= day
                            and not (isinstance(farm["tiles"][y][x], dict)
                                     and farm["tiles"][y][x].get("animal"))), "COW")
            if money >= (400 if species == "COW" else 500):
                orders.append(["BUY_ANIMAL", species, 1])
        price = obs["market"]["prices"].get("WHEAT", 60)
        room = 100 - sum(shed.values())
        # Wheat comes before cash reserves: it is the feed, and the ration gate above
        # will stop the herd growing on its own if the wheat is not there.
        ration = shed.get("WHEAT", 0) + sum(i.get("WHEAT", 0) for i in obs["private"]["inventories"])
        need = 3 * max(1, have)
        keep = 0 if ration < need else 450
        n = int(min(6, room, max(0, (money - keep) // max(price, 1))))
        if n > 0:
            orders.append(["BUY_PRODUCT", "WHEAT", n])
    return orders[:10]


def agent_action(obs, me):
    farmer, hands = plan_turn(obs, me)
    return {"farmer": farmer, "hands": hands, "market": market_turn(obs, me)}
