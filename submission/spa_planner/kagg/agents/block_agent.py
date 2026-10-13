"""Play a stored day-block chosen by a decision tree, swap the herd species, fall back to the greedy.

Alex's spec, 2026-08-20:

    "build the decision tree with days from kawa and natually change in the dynamic animals where
     appropriate"
    "and where it breaks change to the greedy and defo greedy after d28"

Three layers, which is what the measurements support:

  SELECT   at hour 0, read 64 features off the live observation, run that day's tree, and take the
           block it names. Held out by game on カワシギ's 228 seasons: 83.6% at d6, 73.1% at d9,
           58.2% at d12, and nothing from d17 -- so only d0-d16 are in the artifact at all.

  SUBSTITUTE  the block's species is not part of the plan. COW and SHEEP are interchangeable: both
           build a PASTURE, and which one pays depends on whether the town drew MILK shops or the
           YARN_STORE. GOOSE is NOT substituted in -- it needs a COOP rather than a PASTURE, and
           `HERD_GEESE = 0` pending a fresh measurement.

  FALL BACK  to the planner when the day is not covered, when the block does not fit the board, and
           unconditionally from d28. The last days are specifically tuned (`NO_UPKEEP_ON_THE_LAST_DAY`,
           `MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE`) and a copied block has no business there.

**The planner is driven on EVERY turn even when its answer is thrown away.** `submission/main.py`
builds its agent once at d0 h0 and carries per-day state -- pins, pen reservations, the sold ledger.
Its own docstring records that constructing it fresh on day N leaves `state["day"]` at -1 and makes
it re-run a whole first day inside day N. So the fallback has to be warm before it is needed.
"""

import pathlib
import pickle
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

TURNS_PER_DAY = 24
GREEDY_FROM_DAY = 28

#: Which animal makes which product, and which shops buy it. Only the PASTURE pair is swappable.
ANIMAL_OF = {"MILK": "COW", "WOOL": "SHEEP"}
SWAPPABLE = frozenset(("COW", "SHEEP"))
SHOP_BUYS = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}


def shops_of(obs):
    town = obs.get("town")
    if isinstance(town, dict):
        return [str(s) for s in (town.get("unlocked_shops") or [])]
    return [str(s) for s in (obs.get("shops") or [])]


def preferred_pasture_animal(obs):
    """COW or SHEEP, whichever the town is buying more of. None when the draw says nothing.

    MILK comes from three shops and WOOL from one, so a draw with no YARN_STORE points at COW and a
    draw with YARN_STORE and no milk shop points at SHEEP. A tie leaves the block alone -- there is
    no reason to prefer our guess to what the player actually did.
    """
    milk = wool = 0
    for s in shops_of(obs):
        for p in SHOP_BUYS.get(s, ()):
            if p == "MILK":
                milk += 1
            elif p == "WOOL":
                wool += 1
    if milk == wool:
        return None
    return "COW" if milk > wool else "SHEEP"


def _swap(op, want):
    """Rewrite one op's species, leaving everything else -- including quantities -- untouched."""
    if not op or want is None:
        return op
    out = list(op)
    for i in range(1, len(out)):
        if str(out[i]) in SWAPPABLE and str(out[i]) != want:
            out[i] = want
    return out


def substitute_herd(action, want):
    return {"farmer": _swap(action.get("farmer"), want),
            "hands": [_swap(a, want) for a in (action.get("hands") or [])],
            "market": [_swap(o, want) for o in (action.get("market") or [])]}


def owned_hands(obs, seat):
    farms = obs.get("farms") or []
    return len((farms[seat] or {}).get("hands") or []) if seat < len(farms) else 0


def trim(action, hands):
    """Truncate the block's hand actions to the units this farm actually owns, at EMIT time.

    **Not a whole-day precondition.** The first version of this rejected a block if ANY of its 24
    turns drove more units than the farm held at hour 0 -- and the crew GROWS during the day, since
    Kawashigi starts d0 with one farmer and hires as he goes. That check rejected every block on
    every day: the agent silently played the planner for all 30 days and returned perfectly healthy
    money ($78,250 against $66,139) while the thing under test never ran once.

    The reference ignores a surplus unit action for movement and work but still COUNTS it in the
    atomic-PLANT rule, so sending more hands than we own can block plants no real agent could
    block. `submission/main.py` solves it exactly this way, per-turn.
    """
    return {"farmer": action.get("farmer"),
            "hands": list(action.get("hands") or [])[:hands],
            "market": action.get("market") or []}


def make_agent(artifact, teacher="submission/main.py"):
    """`artifact` is the pickle written by scripts/export_block_agent.py."""
    with open(artifact, "rb") as fh:
        payload = pickle.load(fh)
    feature_names = payload["features"]
    days = payload["days"]

    import importlib.util
    import numpy as np
    from scripts.build_day_rows import features as extract

    spec = importlib.util.spec_from_file_location("block_teacher", REPO / teacher)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    planner = mod.agent

    state = {"day": None, "block": None, "source": None, "error": None}

    def agent(obs, config=None):
        seat = int(obs.get("player", obs.get("seat", 0)) or 0)
        day = int(obs.get("day", 0) or 0)
        hour = int(obs.get("hour", 0) or 0)

        # ALWAYS drive the planner, whatever we end up returning. It carries per-day state and a
        # cold planner re-runs a whole first day inside day N.
        fallback = planner(obs, config)

        if day != state["day"]:
            state["day"] = day
            state["block"] = None
            state["source"] = "greedy"
            entry = days.get(day)
            if entry is not None and day < GREEDY_FROM_DAY and hour == 0:
                try:
                    x = extract(obs, seat)
                    row = np.array([[float(x.get(n, 0.0)) for n in feature_names]])
                    chosen = entry["tree"].predict(row)[0]
                    block = entry["blocks"].get(chosen) or entry["blocks"].get(entry["fallback"])
                except Exception as exc:                             # noqa: BLE001
                    block = None
                    # **Never swallow this silently.** A broad except that sets `block = None` and
                    # moves on is indistinguishable, in the output, from a day that legitimately
                    # falls back -- and the whole agent reads as working while never running.
                    state["error"] = "d%d %s: %s" % (day, type(exc).__name__, exc)
                if block and len(block) == TURNS_PER_DAY:
                    want = preferred_pasture_animal(obs)
                    state["block"] = [substitute_herd(a, want) for a in block]
                    state["source"] = "block"

        if state["block"] is not None and hour < TURNS_PER_DAY:
            return trim(state["block"][hour], owned_hands(obs, seat))
        return fallback

    agent.state = state
    return agent
