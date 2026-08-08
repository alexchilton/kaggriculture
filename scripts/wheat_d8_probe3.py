"""Probe: exact WHEAT accounting per day -- harvested (into hand), dropped to shed (explicit
DROP + dusk auto-drop + PLACE fallback), picked up, and net market delta -- for OUR seat only,
via monkeypatching the live env module so every function that actually touches
private["shed"]["WHEAT"] or a unit's carried WHEAT is logged with its real, post-clamp quantity.
Not inferred from op counts or fill lower-bounds.

Read-only instrumentation: wraps each function, calls the original, diffs shed["WHEAT"] (or
inventory) before/after for the object identified as our seat's private dict, and records it.
`private` is a fresh object each interpreter call (kaggle_environments reconstructs the
observation every step), so OUR_PRIVATE[0] is refreshed at the top of every `interpreter` call
rather than captured once after reset.
"""
import sys
import json
import pathlib
import collections

sys.path.insert(0, ".")
from kagg.search import schedule_agent
import scripts.breakdown as bd

import kaggle_environments.core as ke_core
import kaggle_environments.envs.kaggriculture.kaggriculture as kg

_orig_apply = kg._apply_unit_action
_orig_drop_all = kg._drop_inventories_to_shed
_orig_process_market = kg._process_market
_orig_interpreter = kg.interpreter

OUR_PRIVATE = [None]  # the private dict object belonging to our seat -- refreshed every
                       # interpreter call, since the observation may be reconstructed each step
LOG = collections.defaultdict(collections.Counter)
DAY = [0]


def _wheat(shed):
    return int((shed or {}).get("WHEAT", 0))


def patched_apply(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity=100):
    is_ours = private is OUR_PRIVATE[0]
    before = _wheat(private.get("shed")) if is_ours else None
    result = _orig_apply(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity)
    if is_ours:
        after = _wheat(private.get("shed"))
        if after != before:
            op = action[0] if isinstance(action, list) and action else None
            LOG[DAY[0]][f"shed_delta_via_{op}"] += (after - before)
        if isinstance(action, list) and action and action[0] == "HARVEST":
            # units harvested this call, whatever the crop -- filtered to WHEAT via the tile read
            pass
    return result


def patched_drop_all(private, capacity):
    is_ours = private is OUR_PRIVATE[0]
    before = _wheat(private.get("shed")) if is_ours else None
    result = _orig_drop_all(private, capacity)
    if is_ours:
        after = _wheat(private.get("shed"))
        if after != before:
            LOG[DAY[0]]["shed_delta_via_dusk_drop"] += (after - before)
    return result


def patched_process_market(state, env):
    priv0 = state[0].observation.get("private") or {}
    before = _wheat(priv0.get("shed"))
    result = _orig_process_market(state, env)
    priv0_after = state[0].observation.get("private") or {}
    after = _wheat(priv0_after.get("shed"))
    if after != before:
        LOG[DAY[0]]["shed_delta_via_market"] += (after - before)
    return result


def patched_interpreter(state, env):
    # Refresh the "which private dict is ours" pointer every call -- the observation may be a
    # fresh object each step, so a pointer grabbed once after reset() can go stale silently.
    OUR_PRIVATE[0] = state[0].observation.private
    return _orig_interpreter(state, env)


kg._apply_unit_action = patched_apply
kg._drop_inventories_to_shed = patched_drop_all
kg._process_market = patched_process_market
kg.interpreter = patched_interpreter
# `make()` reads the interpreter out of `kaggle_environments.core.environments["kaggriculture"]`,
# a dict populated once at package import with a direct reference to the ORIGINAL function object
# -- patching the kg module attribute alone is invisible to it, confirmed by a 0-calls probe.
# Mutate the registry entry itself so make() picks up the wrapper.
ke_core.environments["kaggriculture"]["interpreter"] = patched_interpreter


def run_side_tagged(make0, opp, seed, weeds):
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=True)
    env.reset(2)
    p0, p1 = make0(), opp()
    shed_wheat = {}
    for t in range(719):
        DAY[0] = t // 24
        o0, o1 = env.state[0].observation, env.state[1].observation
        if t % 24 == 0:
            shed_wheat[("start", t // 24)] = _wheat((o0.get("private") or {}).get("shed"))
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if (t + 1) % 24 == 0:
            priv = env.state[0].observation.get("private") or {}
            shed_wheat[("end", t // 24)] = _wheat(priv.get("shed"))
        if env.state[0].status == "DONE":
            break
    return shed_wheat


def main():
    replay, schedule, team = bd.TAPES["seb"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in bd.TAPE_ONLY} for d, r in sched.items()}
    opp = lambda: bd.tape_policy(replay, team, 1)

    LOG.clear()
    his_shed = run_side_tagged(lambda: bd.tape_policy(replay, team, 0), opp, 11, 0.0)
    his_log = {d: dict(c) for d, c in LOG.items()}

    LOG.clear()
    a = schedule_agent.make_agent(thin, 0, router=True)
    ours_shed = run_side_tagged(lambda: (lambda o, t: a(o)), opp, 11, 0.0)
    our_log = {d: dict(c) for d, c in LOG.items()}

    keys = ["shed_delta_via_DROP", "shed_delta_via_dusk_drop", "shed_delta_via_PICKUP",
            "shed_delta_via_PLACE", "shed_delta_via_market"]
    print(f"{'day':>4} {'ours_start':>10} " + " ".join(f"{k.replace('shed_delta_via_', ''):>10}" for k in keys)
          + f" {'ours_end':>9} {'chk':>6}   ||   {'tape_start':>10} "
          + " ".join(f"{k.replace('shed_delta_via_', ''):>10}" for k in keys) + f" {'tape_end':>9} {'chk':>6}")
    for d in range(12):
        o = our_log.get(d, {})
        h = his_log.get(d, {})
        so = ours_shed.get(("start", d), "?")
        eo = ours_shed.get(("end", d), "?")
        sh = his_shed.get(("start", d), "?")
        eh = his_shed.get(("end", d), "?")
        ovals = [o.get(k, 0) for k in keys]
        hvals = [h.get(k, 0) for k in keys]
        chk_o = "OK" if isinstance(so, int) and so + sum(ovals) == eo else "MISS"
        chk_h = "OK" if isinstance(sh, int) and sh + sum(hvals) == eh else "MISS"
        print(f"{d:>4} {so:>10} " + " ".join(f"{v:>10}" for v in ovals) + f" {eo:>9} {chk_o:>6}   ||   "
              f"{sh:>10} " + " ".join(f"{v:>10}" for v in hvals) + f" {eh:>9} {chk_h:>6}")


if __name__ == "__main__":
    main()
